"""Regressions from real Ark response shapes and actual session evidence boundaries."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import test_single_no_plan_todo_bootstrap as bootstrap_fixtures

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.agentic import TaskWorkspace, normalize_task_design, task_config


class LiveResponseParsingTests(unittest.TestCase):
    def test_entropy_redaction_happens_after_structured_response_parsing(self):
        with tempfile.TemporaryDirectory() as temp:
            app = cc.AppContext.__new__(cc.AppContext)
            app.liquid_kernel = LiquidKernelControlPlane(Path(temp))
            profile = {'provider': 'ollama', 'base_url': 'http://127.0.0.1:11434', 'model': 'qwen3.6:latest'}
            response = {'content': 'A' * 150 + '\n```json\n{"score_a":97,"score_b":97,"rationale":"Equivalent evidence."}\n```',
                        'tool_calls': [], 'raw': {'done_reason': 'stop', 'prompt_eval_count': 20, 'eval_count': 10}}
            with mock.patch.object(app, '_liquid_kernel_profile', return_value=profile), \
                 mock.patch.object(cc.OllamaClient, 'chat', return_value=response):
                result = app._liquid_kernel_transport_call('Independent review', '{}', 'local', 1024)
            self.assertEqual(result['score_a'], 97)
            self.assertEqual(result['rationale'], 'Equivalent evidence.')

    def test_blind_review_format_recovery_disables_tools_and_forces_json(self):
        from liquid_kernel.context import RECALL_TOOL
        with tempfile.TemporaryDirectory() as temp:
            app = cc.AppContext.__new__(cc.AppContext)
            app.liquid_kernel = LiquidKernelControlPlane(Path(temp))
            profile = {'provider': 'ollama', 'base_url': 'http://127.0.0.1:11434', 'model': 'qwen3.6:latest'}
            replies = iter(['Examples:\n```python\nx=1\n```\n```json\n{"score_a":97,"score_b":97}\n```',
                            '{"score_a":97,"score_b":97,"rationale":"Equivalent evidence."}'])
            calls = []
            def chat(client, *args, **kwargs):
                calls.append((kwargs['tools'], client.structured_json_output, kwargs['label']))
                return {'content': next(replies), 'tool_calls': [], 'raw': {'done_reason': 'stop', 'prompt_eval_count': 20, 'eval_count': 10}}
            packet = json.dumps({'messages': [{'role': 'user', 'content': 'Compare the frozen evidence.'}],
                                 'tools': [RECALL_TOOL], 'require_json_final': True})
            with mock.patch.object(app, '_liquid_kernel_profile', return_value=profile), \
                 mock.patch.object(cc.OllamaClient, 'chat', new=chat):
                result = app._liquid_kernel_transport_call('Independent review: return JSON scores', packet, 'local', 1024)
            self.assertEqual(result['score_a'], 97)
            self.assertEqual(calls[0][:2], ([RECALL_TOOL], False))
            self.assertEqual(calls[1], (None, True, 'evolution_json_recovery'))
            self.assertGreaterEqual(result['_evolution_usage']['total_tokens'], 60)

    def test_native_recall_identifiers_survive_redaction_and_known_credentials_do_not(self):
        from liquid_kernel.context import RECALL_TOOL
        with tempfile.TemporaryDirectory() as temp:
            app = cc.AppContext.__new__(cc.AppContext)
            app.liquid_kernel = LiquidKernelControlPlane(Path(temp))
            profile = {'provider': 'ollama', 'base_url': 'http://127.0.0.1:11434', 'model': 'qwen3.6:latest', 'api_key': 'actual-secret-value',
                       'headers': {'Content-Type': 'application/json'}}
            archive_id = 'f625e580218618e18b212263017472aab0bc16a731bdc23cd5f3c19d801a0684'
            response = {'content': '', 'tool_calls': [{'id': 'recall', 'function': {'name': 'context_recall', 'arguments': {
                'archive_id': archive_id, 'query': 'application/json actual-secret-value'}}}], 'raw': {'done_reason': 'stop'}}
            packet = json.dumps({'messages': [{'role': 'user', 'content': 'Inspect frozen source'}], 'tools': [RECALL_TOOL]})
            with mock.patch.object(app, '_liquid_kernel_profile', return_value=profile), \
                 mock.patch.object(cc.OllamaClient, 'chat', return_value=response):
                result = app._liquid_kernel_transport_call('Inspect evidence', packet, 'local', 1024)
            args = result['tool_calls'][0]['arguments']
            self.assertEqual(args['archive_id'], archive_id)
            self.assertEqual(args['query'], 'application/json [secret redacted]')

    def test_complete_json_wrappers_preserve_unicode(self):
        for text in ['{"任务":"继续修复"}', '```json\n{"任务":"继续修复"}\n```', 'Result:\n{"任务":"继续修复"}\nDone.']:
            self.assertEqual(cc.decode_model_json_object(text), {"任务": "继续修复"})

    def test_markdown_fences_inside_json_strings_are_data(self):
        source = {"content": "```python\nprint('hello')\n```"}
        self.assertEqual(cc.decode_model_json_object(json.dumps(source)), source)
        with self.assertRaises(ValueError):
            cc.decode_model_json_object('{"partial":"```json\n{\"wrong\":true}\n```"')

    def test_partial_outer_object_cannot_be_replaced_by_a_nested_object(self):
        for text in ['{"patch":{"valid":true}', '[{"valid":true}]', '{"a":1}{"b":2}', 'thinking only', '']:
            with self.assertRaises(ValueError):
                cc.decode_model_json_object(text)

    def test_retired_opt_out_is_migrated_to_task_execution(self):
        self.assertTrue(task_config("Thinking", {"enabled": False})["enabled"])
        self.assertNotIn('id="evolutionTaskBenchmarks"', cc.ADMIN_INDEX_HTML)

    def test_actual_service_aliases_are_normalized_before_freezing(self):
        task = {"goal": "Create result.json from input.json", "starter_files": {"input.json": "{}"},
                "followups": [{"after_round": 3, "content": "Add a verified flag."}],
                "checks": [{"kind": "json_equals", "path": "result.json", "expected": {"verified": True}},
                           {"kind": "command", "cmd": 'python3 -c "assert True"', "expected_exit_code": 0}]}
        _starter, _followups, checks = normalize_task_design(task, task_config("Thinking"))
        self.assertEqual(checks[0]["value"], {"verified": True})
        self.assertEqual(checks[1]["exit_code"], 0)
        task["checks"][0]["path"] = "unstated-result.json"
        with self.assertRaisesRegex(ValueError, "not declared"):
            normalize_task_design(task, task_config("Thinking"))

    def test_observed_type_and_line_count_aliases_execute_real_assertions(self):
        task = {"goal": "Create page.html with at least 1500 lines and a static SVG diagram in the source code.", "starter_files": {},
                "followups": [{"after_round": 3, "content": "Include a table in page.html."}],
                "checks": [{"type": "min_lines", "path": "page.html", "value": 1500},
                           {"type": "content_contains", "path": "page.html", "value": "<svg"}]}
        _, _, checks = normalize_task_design(task, task_config("Thinking"))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'page.html'
            path.write_text('<svg></svg>\n' + '<p>line</p>\n' * 1499)
            rows = TaskWorkspace(temp, lambda: None).evaluate(checks)
            self.assertTrue(all(row['ok'] for row in rows))
            self.assertEqual(rows[0]['actual_lines'], 1500)
            path.write_text('<svg></svg>\n')
            self.assertFalse(TaskWorkspace(temp, lambda: None).evaluate(checks)[0]['ok'])

    def test_native_trajectory_keeps_ids_results_and_later_user_steering(self):
        rows = [{"role": "user", "content": "Read input.txt"},
                {"role": "assistant", "content": json.dumps({"tool_calls": [
                    {"name": "read_file", "arguments": {"path": "input.txt"}},
                    {"name": "read_file", "arguments": {"path": "other.txt"}}]})},
                {"role": "tool", "content": json.dumps([{"name": "read_file", "ok": True, "output": "alpha"},
                                                         {"name": "read_file", "ok": True, "output": "beta"}])},
                {"role": "user", "content": "Now change the output format"}]
        rendered = cc.evolution_worker_chat_messages(rows)
        self.assertEqual([row['role'] for row in rendered], ['user', 'assistant', 'tool', 'tool', 'user'])
        calls = rendered[1]['tool_calls']
        self.assertEqual([r['tool_call_id'] for r in rendered[2:4]], [r['id'] for r in calls])
        self.assertEqual([json.loads(r['content'])['output'] for r in rendered[2:4]], ['alpha', 'beta'])
        self.assertEqual(rendered[-1]['content'], 'Now change the output format')
        self.assertEqual(cc.OllamaClient._sanitize_openai_tool_history(rendered), rendered)

    def test_observed_judge_confidence_label_does_not_destroy_valid_scores(self):
        app = cc.AppContext.__new__(cc.AppContext)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        app.liquid_kernel = cc.LiquidKernelControlPlane(Path(temporary.name))
        for raw, numeric, label in [('high', None, 'high'), (0, 0, ''), (.8, .8, ''), ('NaN', None, '')]:
            with self.subTest(raw=raw), mock.patch.object(app, '_liquid_kernel_model_call', return_value={
                'score_a': 97, 'score_b': 97, 'rationale': 'Identical observed trajectories', 'confidence': raw}):
                result = app._liquid_kernel_judge_call({}, 'profile', 1024)
                self.assertEqual(result['incumbent'], 97)
                self.assertEqual(result['candidate'], 97)
                self.assertEqual(result['confidence'], numeric)
                self.assertEqual(result['confidence_label'], label)

    def test_successful_large_write_is_archived_only_in_transported_history(self):
        body = 'x' * 30000
        rows = [{'role': 'user', 'content': 'Create long.html'},
                {'role': 'assistant', 'content': json.dumps({'tool_calls': [{'name': 'write_file', 'arguments': {'path': 'long.html', 'content': body}}]})},
                {'role': 'tool', 'content': json.dumps([{'name': 'write_file', 'ok': True, 'output': {'written': 'long.html'}}])}]
        rendered = cc.evolution_worker_chat_messages(rows)
        self.assertLess(len(json.dumps(rendered)), 5000)
        self.assertEqual(json.loads(rows[1]['content'])['tool_calls'][0]['arguments']['content'], body)
        observed = json.loads(rendered[2]['content'])
        self.assertEqual(observed['archived_write']['chars'], 30000)
        self.assertEqual(observed['output']['written'], 'long.html')

    def test_local_task_budget_becomes_failure_and_leaves_global_budget(self):
        import contextlib

        from liquid_kernel.agentic import AgenticBenchmark
        from liquid_kernel.control import BASELINE_KERNEL_FILES
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            plane._token_limit, plane._tokens_used = 10000, 0
            @contextlib.contextmanager
            def budget():
                plane._rollout_token_ceiling = plane._tokens_used + 500
                try:
                    yield
                finally:
                    plane._rollout_token_ceiling = 0
            def model(*args, **kwargs):
                plane._record_model_tokens('', {'_evolution_usage': {'total_tokens': 600, 'transport_accounted': True}})
            task = {'id': 'budget', 'split': 'train', 'fingerprint': 'frozen', 'goal': 'Create result.txt',
                    'starter_files': {}, 'followups': [], 'checks': [{'kind': 'file_exists', 'path': 'result.txt'}], 'minimum_tool_calls': 3}
            result = AgenticBenchmark(model, lambda: plane._check_cancel(''), budget_scope=budget).run_task(
                BASELINE_KERNEL_FILES, task, {'max_rounds': 200, 'task_timeout_seconds': 30, 'turn_max_tokens': 16384, 'max_tool_calls': 1600})
            self.assertFalse(result['success'])
            self.assertIn('task_token_budget_exhausted', result['error'])
            self.assertEqual(plane._rollout_token_ceiling, 0)
            self.assertEqual(plane._tokens_used, 600)
            plane._check_cancel('')

    def test_normal_chat_transport_archives_large_writes_without_mutation(self):
        body = '<p>ordinary session content</p>\n' * 1800
        original = [{'role': 'user', 'content': 'Create a page'},
                    {'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'normal-write', 'type': 'function',
                     'function': {'name': 'write_file', 'arguments': {'path': 'large.html', 'content': body}}}]},
                    {'role': 'tool', 'tool_call_id': 'normal-write', 'name': 'write_file', 'content': 'File written', 'result_ok': True}]
        snapshot = json.dumps(original)
        client = cc.OllamaClient('http://127.0.0.1:11434', 'test')
        for provider in ['openai_compat', 'ollama', 'anthropic']:
            with self.subTest(provider=provider):
                prepared = client._prepare_request_messages(original, provider)
                self.assertLess(len(json.dumps(prepared)), 5000)
                self.assertEqual(prepared[1]['tool_calls'][0]['id'], 'normal-write')
                self.assertEqual(prepared[2]['tool_call_id'], 'normal-write')
                self.assertIn('successful-write-history', prepared[2]['content'])
        self.assertEqual(json.dumps(original), snapshot)
        original[2]['result_ok'] = False
        prepared = client._prepare_request_messages(original, 'openai_compat')
        self.assertIn(body, json.loads(prepared[1]['tool_calls'][0]['function']['arguments'])['content'])

    def test_large_incomplete_normal_write_keeps_original_size_and_cannot_be_repaired_into_partial_success(self):
        raw = '{"path":"large.html","content":"' + 'x' * 20000
        client = cc.OllamaClient('http://127.0.0.1:11434', 'test')
        calls = client._normalize_tool_calls([{'function': {'name': 'write_file', 'arguments': raw}}])
        self.assertGreater(calls[0]['raw_arguments_chars'], 20000)
        self.assertTrue(calls[0]['args_error'])
        session = bootstrap_fixtures.SingleNoPlanTodoBootstrapTests().bare_session()
        ok, args, note = session._recover_tool_args_from_malformed(name='write_file', raw_args=raw, pinned_selection='test')
        self.assertFalse(ok)
        self.assertEqual(args, {})
        self.assertIn('not executed', note)
        self.assertIn('compact generation script', note)

    def test_reused_call_id_only_matches_its_own_tool_exchange(self):
        body = 'x' * 12000
        def call():
            return {'role': 'assistant', 'tool_calls': [{'id': 'reused', 'function': {'name': 'write_file', 'arguments': {'path': 'same.html', 'content': body}}}]}
        rows = [call(), {'role': 'tool', 'tool_call_id': 'reused', 'content': 'Error: failed', 'result_ok': False},
                {'role': 'user', 'content': 'retry'}, call(),
                {'role': 'tool', 'tool_call_id': 'reused', 'content': 'Written', 'result_ok': True}]
        compact = cc.compact_successful_write_history(rows)
        self.assertEqual(compact[0]['tool_calls'][0]['function']['arguments']['content'], body)
        self.assertLess(len(compact[3]['tool_calls'][0]['function']['arguments']['content']), 3000)


class AdminRoundAndSessionSourceTests(unittest.TestCase):
    def test_admin_round_limit_survives_strength_and_saved_legacy_caps(self):
        with tempfile.TemporaryDirectory() as temp:
            runtime = {"max_rounds": 500, "max_run_seconds": 3500, "max_output_tokens": 16384}
            plane = LiquidKernelControlPlane(Path(temp), task_runtime_limits=lambda: runtime)
            for mode in ("Tuning", "Thinking", "Aggressive"):
                cfg = plane.save_config({"mode": mode, "task_benchmark": {"max_rounds": 24}})["config"]
                self.assertEqual(cfg["task_benchmark"]["max_rounds"], 500)
                self.assertEqual(cfg["task_benchmark"]["max_tool_calls"], 4000)
                self.assertEqual(cfg["task_benchmark"]["task_timeout_seconds"], 3500)
                self.assertEqual(cfg["task_benchmark"]["turn_max_tokens"], 16384)
            runtime["max_rounds"] = 777
            self.assertEqual(plane.config()["task_benchmark"]["max_rounds"], 777)

    def test_human_ledger_recovers_goal_hidden_by_compaction(self):
        with tempfile.TemporaryDirectory() as temp:
            state = {"user_bubble_log": [{"text": "逐篇生成不少于1500行的 HTML，并加入 SVG 和表格", "ts": 10},
                                         {"text": "继续执行", "ts": 20}],
                     "messages": [{"role": "user", "content": "[file_buffer:context.txt]", "ts": 10},
                                  {"role": "user", "content": "<compact-resume>summary", "ts": 11}]}
            rows = cc.AppContext._liquid_kernel_human_requests(state, Path(temp))
            self.assertIn("1500", rows[0]["content"])
            self.assertEqual(len(rows), 2)
            self.assertTrue(all(row["request_source"] == "user_bubble_log" for row in rows))


class TodoEnvelopeRegressionTests(unittest.TestCase):
    def session(self):
        return bootstrap_fixtures.SingleNoPlanTodoBootstrapTests().bare_session()

    def test_tool_envelope_is_unwrapped_without_metadata_rows(self):
        session = self.session()
        envelope = {"id": "chatcmpl-tool-8ed64aafdc82ef", "type": "function", "role": "developer",
                    "function": {"name": "TodoWrite", "arguments": json.dumps({"todos": [{"content": "检查中文接口", "status": "in_progress"}]}, ensure_ascii=False)}}
        rows = session._todo_payload_items(envelope)
        self.assertEqual([row['content'] for row in rows], ["检查中文接口"])
        self.assertEqual(session._extract_text_items_from_raw_args(envelope), ["检查中文接口"])

    def test_raw_transport_and_partial_json_do_not_become_tasks(self):
        session = self.session()
        raw = 'tool: TodoWrite\nTodoWrite\n〇\ndeveloper\nchatcmpl-tool-8ed64aafdc82ef\nee\ndd2c83ff58af5331\n2fab242caf0096d4ff2af188'
        self.assertEqual(session._extract_text_items_from_raw_args(raw), [])
        partial = '{"id":"chatcmpl-tool-abcd","name":"TodoWrite","arguments":{"todos":[{"content":"检查中文接口","status":"pending"},{"content":"运行测试"'
        self.assertEqual(session._extract_text_items_from_raw_args(partial), ["检查中文接口", "运行测试"])

    def test_loaded_pollution_is_removed_and_legitimate_task_prose_is_retained(self):
        session = self.session()
        rows = [{"content": text, "status": "pending"} for text in ["TodoWrite", "developer", "ee", "dd2c83ff58af5331", "修复 TodoWrite 工具的参数解析"]]
        clean = session._normalize_loaded_todo_rows(rows, [])
        self.assertEqual([row['content'] for row in clean], ["修复 TodoWrite 工具的参数解析"])


class SessionContinuationEvidenceTests(unittest.TestCase):
    def make_session(self, root):
        return cc.SessionState('followup', 'Cache continuation', root/'sessions', 'http://127.0.0.1:11434', 'offline-test',
                               root/'skills', cc.CryptoBox(root/'Codes'), root/'repo', js_lib_root=root/'js',
                               js_lib_download_enabled=False, web_search_enabled=False, defer_initial_persist=True)

    def test_real_session_cache_survives_completed_boundary_and_reload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = self.make_session(root)
            (session.files_root/'facts.txt').write_text('cutoff = 0.35 eV\ntemperature = 300 K\n')
            output = session._run_read('facts.txt')
            session._record_read_context('facts.txt', {'path': 'facts.txt'}, output, role='developer')
            board = session._ensure_blackboard()
            board['status'] = 'COMPLETED'
            board['original_goal'] = 'Read facts.txt and prepare the first report'
            board['code_artifacts'] = {'report.md': {'path': 'report.md'}}
            previous = session._previous_task_context_snapshot(board)
            session._reset_blackboard_plan_state_locked(new_goal='继续，补充温度', previous_context=previous,
                                                         clear_progress=True, reset_agent_contexts=True)
            session._prepare_continuation_memory('继续，补充温度', previous)
            block = session._read_context_prompt_block(for_role='developer')
            self.assertIn('<continuation-evidence>', block)
            self.assertIn('0.35 eV', block)
            self.assertIn('300 K', block)
            detail = json.loads(session._tool_memory_tool({'mode': 'detail', 'id': next(iter(session.tool_memory_registry))}, 'developer'))
            self.assertIn('0.35 eV', detail['items'][0]['cached_preview'])
            session._persist()
            restored = self.make_session(root)
            cached = restored._run_read('facts.txt')
            self.assertIn('continuation_cache=true', cached)
            self.assertEqual(restored.continuation_cache_hits, 1)
            fresh = restored._run_read('facts.txt', fresh=True)
            self.assertNotIn('continuation_cache=true', fresh)
            self.assertEqual(restored.continuation_cache_hits, 1)
            self.assertIn('<continuation-evidence>', restored._read_context_prompt_block(for_role='developer'))
            self.assertIn('0.35 eV', restored._read_context_prompt_block(for_role='developer'))
            (restored.files_root/'facts.txt').write_text('cutoff = 0.40 eV\ntemperature = 310 K\n')
            block = restored._continuation_memory_prompt_block()
            self.assertIn('stale=true', block)
            self.assertNotIn('0.35 eV', block)
            self.assertNotIn('300 K', block)

    def test_new_unrelated_goal_does_not_inherit_previous_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.make_session(Path(temp))
            (session.files_root/'facts.txt').write_text('obsolete unrelated subject\n')
            session._record_read_context('facts.txt', {'path': 'facts.txt'}, session._run_read('facts.txt'), role='developer')
            session._prepare_continuation_memory('Build a new calendar widget', {})
            self.assertEqual(session._continuation_memory_prompt_block(), '')


if __name__ == '__main__':
    unittest.main()
