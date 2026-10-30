"""Storage, quota and isolation invariants; live model tasks run separately."""
import copy
import json
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.context import (
    BudgetExceeded,
    ContextWindow,
    HistoryArchive,
    ModelTokenLedger,
    ReviewEvidence,
)
from liquid_kernel.control import normalize_evolution_config


class SharedContextRuntimeTests(unittest.TestCase):
    def test_repeated_premature_finals_receive_frozen_body_in_both_review_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            body = 'header\n' * 1000 + 'ACTUAL_BODY_EVIDENCE\n' + 'tail\n' * 1000
            session = self.session(root)
            session._ensure_llm_gate()
            reader = ReviewEvidence(HistoryArchive(root / 'review-fallback.jsonl'))
            reader.add('long.py', body)
            seen = []

            def ordinary(messages, **kwargs):
                seen.append(copy.deepcopy(messages))
                observed = 'host_read_only_frozen_evidence' in json.dumps(messages)
                return {'content': json.dumps({'passed': not observed}), 'tool_calls': []}

            with mock.patch.object(session.ollama, '_chat_impl', side_effect=ordinary):
                verdict = session._read_only_review_json('Inspect the frozen body.', 'Independent review', reader)
            self.assertFalse(verdict['passed'])
            self.assertEqual(len(seen), 3)
            self.assertIn('ACTUAL_BODY_EVIDENCE', json.dumps(seen[-1]))
            self.assertFalse(reader.pending)

            app = cc.AppContext.__new__(cc.AppContext)
            app.liquid_kernel = plane = LiquidKernelControlPlane(root / 'kernel')
            plane._token_limit, plane._tokens_used = 0, 0
            packet = {'score': 90, 'rows': [{'task_id': 't', 'artifacts': {'long.py': body}}]}
            calls = []

            def evolution(system, prompt, *_):
                calls.append(json.loads(prompt))
                return {'score_a': 90, 'score_b': 90, 'rationale': 'Frozen evidence reviewed'}

            with mock.patch.object(app, '_liquid_kernel_model_call', side_effect=evolution):
                scores = app._liquid_kernel_judge_call({'observations': {'incumbent': packet, 'candidate': packet}}, 'judge', 2048)
            self.assertEqual(scores['incumbent'], 90)
            self.assertEqual(len(calls), 4)
            self.assertIn('host_read_only_frozen_evidence', json.dumps(calls[-1]))

    def test_long_task_compute_quota_does_not_expand_edit_strength(self):
        config = normalize_evolution_config({'mode': 'Tuning', 'budget': {'max_tokens': 800000, 'max_files': 999, 'max_changed_lines': 99999}})
        self.assertEqual(config['budget']['max_tokens'], 800000)
        self.assertEqual(config['budget']['max_files'], 5)
        self.assertEqual(config['budget']['max_changed_lines'], 99999)

    def test_admin_user_limits_also_bound_real_task_rollouts(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), task_runtime_limits=lambda: {
                'max_rounds': 333, 'max_run_seconds': 3000, 'context_token_limit': 48000, 'max_run_tokens': 90000})
            cfg = plane._apply_task_runtime_limits(normalize_evolution_config({'mode': 'Thinking', 'task_benchmark': {'max_task_tokens': 120000}}))
            self.assertEqual(cfg['task_benchmark']['max_rounds'], 333)
            self.assertEqual(cfg['task_benchmark']['context_token_limit'], 48000)
            self.assertEqual(cfg['task_benchmark']['max_task_tokens'], 120000)

    def test_ide_and_web_submission_reach_the_same_session_and_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp), max_run_tokens=5000, max_task_tokens=3000)
            app = cc.AppContext.__new__(cc.AppContext)
            app.manager_for_user = lambda _user: types.SimpleNamespace(get=lambda _sid: session)
            app.scheduler_limits_enabled = lambda: False
            app._publish_collaboration_agent_state = lambda *_args, **_kwargs: None
            app._ide_session = lambda *_args: session
            app.ide_resolve_workspace = lambda *_args: (session.files_root, session.files_root, {'label': 'session', 'kind': 'workspace'})
            with mock.patch.object(session, 'accept_user_message', return_value={'ok': True}) as accepted:
                app.submit_user_message('user', session.id, 'Continue the WebUI task')
                app.ide_agent_task('user', session.id, {'message': 'Continue the IDE task'})
            self.assertEqual(accepted.call_count, 2)
            self.assertIn('Continue the WebUI task', accepted.call_args_list[0].args[0])
            self.assertIn('Continue the IDE task', accepted.call_args_list[1].args[0])
            ledger = session._ensure_llm_gate().model_token_ledger
            self.assertEqual((ledger.run_limit, ledger.task_limit), (5000, 3000))

    def session(self, root, **kwargs):
        return cc.SessionState('archive', 'Archive recovery', root/'sessions', 'http://127.0.0.1:11434', 'offline-test',
            root/'skills', cc.CryptoBox(root/'Codes'), root/'repo', js_lib_root=root/'js',
            js_lib_download_enabled=False, web_search_enabled=False, defer_initial_persist=True, **kwargs)

    def test_old_middle_of_write_survives_file_overwrite_context_removal_and_encrypted_reload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = self.session(root)
            body = 'before\n' * 1700 + 'def original_fee(q): return q * 17 + 29\n' + 'after\n' * 1700
            session.messages = [{'role': 'assistant', 'content': '', 'tool_calls': [
                {'id': 'original', 'type': 'function', 'function': {'name': 'write_file', 'arguments': {'path': 'policy.py', 'content': body}}}]},
                {'role': 'tool', 'tool_call_id': 'original', 'name': 'write_file', 'content': '{"ok":true}', 'result_ok': True}]
            session._microcompact()
            (session.files_root/'policy.py').write_text('def original_fee(q): return 0\n')
            session.messages = [{'role': 'user', 'content': '继续，使用最初版本的费率'}]
            session._persist()
            restored = self.session(root)
            result = json.loads(restored._context_recall({'path': 'policy.py', 'tool_call_id': 'original', 'field': 'content', 'query': 'original_fee'}))
            original = result['matches'][0]
            self.assertIn('q * 17 + 29', original['content'])
            self.assertEqual(original['start_line'], 1697)
            overview = json.loads(restored._context_recall({'tool_call_id': 'original', 'field': 'content'}))['matches'][0]
            self.assertIn({'name': 'original_fee', 'line': 1701}, overview['symbols'])
            self.assertEqual(overview['next_start_line'], 41)
            alias = json.loads(restored._context_recall({'tool_call_id': 'original', 'field': 'body', 'query': 'original_fee'}))
            self.assertIn('q * 17 + 29', alias['matches'][0]['content'])
            self.assertEqual(alias['field_alias']['resolved'], 'content')
            exact = json.loads(restored._context_recall({'archive_id': original['archive_id'], 'field': 'content', 'start_line': 1701, 'line_count': 1}))
            self.assertEqual(exact['matches'][0]['content'], 'def original_fee(q): return q * 17 + 29\n')
            self.assertEqual((session.files_root/'policy.py').read_text(), 'def original_fee(q): return 0\n')

    def test_microcompression_archives_complete_tool_observations_before_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp))
            text = 'x' * 12000 + 'middle evidence token' + 'y' * 12000
            rows = [{'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'read1', 'function': {'name': 'read_file', 'arguments': {'path': 'x.txt'}}}]},
                    {'role': 'tool', 'name': 'read_file', 'tool_call_id': 'read1', 'content': text}]
            rows += [{'role': 'tool', 'content': 'other ' * 1000, 'tool_call_id': str(i)} for i in range(4)]
            session._microcompact_agent_messages(rows, keep_recent=1)
            recalled = session._full_history_archive().recall({'tool_call_id': 'read1', 'query': 'middle evidence token'})
            self.assertIn('middle evidence token', recalled['matches'][0]['content'])

    def test_archive_failure_prevents_lossy_mutation(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp))
            rows = [{'role': 'tool', 'content': 'full output ' * 1000} for _ in range(5)]
            before = copy.deepcopy(rows)
            with mock.patch.object(session._full_history_archive(), 'record', side_effect=OSError('disk full')):
                with self.assertRaises(OSError):
                    session._microcompact_agent_messages(rows, keep_recent=1)
            self.assertEqual(rows, before)

    def test_full_compression_carries_unseen_evidence_and_native_call_as_one_group(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp))
            rows = [{'role': 'assistant', 'content': '', 'tool_calls': [{'id': 'recall', 'function': {'name': 'context_recall', 'arguments': {'query': 'fee'}}}]},
                    {'role': 'tool', 'tool_call_id': 'recall', 'name': 'context_recall', '_unseen': True,
                     'content': 'fresh exact evidence\n' * 1000}]
            before = copy.deepcopy(rows)
            compressed = session._priority_compress_messages(rows, 1000, 3)
            self.assertEqual(compressed, before)

    def test_runtime_tags_quoted_inside_tool_evidence_do_not_clear_the_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp))
            rows = [{'role': 'tool', 'content': '{"source":"full_history","quote":"<compact-resume>data</compact-resume>"}'}]
            self.assertEqual(session._strip_archival_runtime_hints(rows), rows)

    def test_context_window_preserves_human_order_and_complete_native_exchanges(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = HistoryArchive(Path(temp)/'history.jsonl')
            rows = [{'role': 'user', 'content': 'Original constraint: retain decimals.'}]
            for index in range(12):
                rows += [{'role': 'assistant', 'content': '', 'tool_calls': [{'id': str(index), 'function': {'name': 'read_file', 'arguments': {'path': 'file'}}}]},
                         {'role': 'tool', 'tool_call_id': str(index), 'content': 'data\n' * 3000}]
                if index == 8:
                    rows.append({'role': 'user', 'content': 'Later constraint: also retain units.'})
            window = ContextWindow(archive, 12000)
            prepared = window.prepare(rows, output_tokens=1000)
            self.assertGreater(window.compactions, 0)
            self.assertEqual([row['content'] for row in prepared if row.get('role') == 'user' and 'constraint:' in row['content']],
                             ['Original constraint: retain decimals.', 'Later constraint: also retain units.'])
            pending = set()
            for row in prepared:
                if row.get('role') == 'assistant':
                    pending.update(call['id'] for call in row.get('tool_calls', []))
                elif row.get('role') == 'tool':
                    self.assertIn(row['tool_call_id'], pending)
                    pending.remove(row['tool_call_id'])
            self.assertFalse(pending)
            self.assertEqual(len(list(archive.entries())), len(rows))

    def test_nested_quotas_reserve_concurrent_calls_and_restore_usage(self):
        ledger = ModelTokenLedger(1600, 900)
        first, cap = ledger.reserve(200, 600, task='one', generation=7)
        self.assertEqual(cap, 600)
        with self.assertRaises(BudgetExceeded):
            ledger.reserve(100, 300, task='one', generation=7)
        second, cap = ledger.reserve(100, 300, task='two', generation=7)
        ledger.settle(first, 350)
        ledger.settle(second, None)
        restored = ModelTokenLedger(1600, 900, ledger.snapshot())
        self.assertEqual(restored.snapshot()['used'], 750)
        third, cap = restored.reserve(200, 1000, task='one', generation=7)
        self.assertEqual(cap, 350)
        restored.settle(third, 550)
        with self.assertRaises(BudgetExceeded):
            restored.reserve(10, 128, task='one', generation=7)
        fourth, _ = restored.reserve(100, 128, task='two', generation=7)
        restored.settle(fourth, 228)
        with self.assertRaises(BudgetExceeded):
            restored.reserve(1, 128, task='three', generation=7)

    def test_ordinary_client_includes_input_tools_and_review_in_one_ledger(self):
        with tempfile.TemporaryDirectory() as temp:
            session = self.session(Path(temp), max_run_tokens=2000, max_task_tokens=1200)
            gate = session._ensure_llm_gate()
            response = {'content': 'observed result', 'tool_calls': [], 'raw': {'usage': {'prompt_tokens': 100, 'completion_tokens': 500, 'total_tokens': 600}}}
            with mock.patch.object(session.ollama, '_chat_impl', return_value=response) as model:
                session.ollama.chat([{'role': 'user', 'content': 'Do the work'}], max_tokens=600)
                session.ollama.chat([{'role': 'user', 'content': 'Review the work'}], max_tokens=300)
                with self.assertRaises(BudgetExceeded):
                    session.ollama.chat([{'role': 'user', 'content': 'Retry'}], max_tokens=300)
                self.assertEqual(model.call_count, 2)
            self.assertEqual(gate.model_token_ledger.snapshot()['used'], 1200)
            self.assertEqual(gate.model_token_ledger.snapshot()['reserved'], 0)

    def test_independent_review_can_retrieve_missing_middle_but_cannot_execute_worker_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            app = cc.AppContext.__new__(cc.AppContext)
            app.liquid_kernel = plane = LiquidKernelControlPlane(Path(temp)/'kernel')
            plane._token_limit, plane._tokens_used = 100000, 0
            packet = {'score': 90, 'rows': [{'task_id': 't', 'artifacts': {'long.txt': 'head\n' * 1200 + 'decisive middle evidence\n' + 'tail\n' * 1200}}]}
            calls = []
            def model(system, prompt, _profile, _tokens):
                payload = json.loads(prompt)
                calls.append(payload)
                self.assertEqual([tool['function']['name'] for tool in payload['tools']], ['context_recall'])
                if len(calls) == 1:
                    self.assertNotIn('decisive middle evidence', prompt)
                    return {'tool_calls': [{'name': 'context_recall', 'arguments': {'query': 'decisive middle evidence'}},
                                           {'name': 'bash', 'arguments': {'command': 'touch forbidden'}}]}
                observations = [json.loads(row['content']) for row in payload['messages'] if row.get('role') == 'tool']
                self.assertIn('decisive middle evidence', json.dumps(observations[0]))
                self.assertIn('read-only', observations[1]['error'])
                return {'score_a': 90, 'score_b': 90, 'rationale': 'Verified frozen evidence'}
            with mock.patch.object(app, '_liquid_kernel_model_call', side_effect=model):
                result = app._liquid_kernel_judge_call({'observations': {'incumbent': packet, 'candidate': packet}}, 'judge', 2048)
            self.assertEqual(result['incumbent'], 90)
            self.assertEqual(len(calls), 2)
            self.assertFalse((Path(temp)/'forbidden').exists())

    def test_ordinary_review_refuses_uninspected_excerpt_and_keeps_fresh_read_only_context(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = self.session(root)
            session.messages = [{'role': 'assistant', 'content': 'Private worker scratchpad must not enter review.'}]
            session._ensure_llm_gate()
            reader = ReviewEvidence(HistoryArchive(root/'review.jsonl'), excerpt_head=1600, excerpt_tail=0, max_inline_chars=1600)
            reader.add('policy.py', 'header\n' * 1700 + 'def decisive_fee(q): return q * 17 - 29\n' + 'tail\n' * 1700)
            seen = []
            def model(messages, **kwargs):
                seen.append(copy.deepcopy(messages))
                self.assertNotIn('Private worker scratchpad', json.dumps(messages))
                self.assertEqual([tool['function']['name'] for tool in kwargs['tools']], ['context_recall'])
                if len(seen) == 1:
                    return {'content': '{"passed":true}', 'tool_calls': []}
                if len(seen) == 2:
                    self.assertIn('Review cannot finish', messages[-1]['content'])
                    return {'content': '', 'tool_calls': [
                        {'id': 'inspect', 'function': {'name': 'context_recall', 'arguments': {'path': 'policy.py', 'query': 'decisive_fee'}}},
                        {'id': 'forbidden', 'function': {'name': 'bash', 'arguments': {'command': 'touch forbidden'}}}]}
                outputs = [json.loads(row['content']) for row in messages if row.get('role') == 'tool']
                self.assertIn('q * 17 - 29', json.dumps(outputs[0]))
                self.assertIn('read-only', outputs[1]['error'])
                return {'content': '{"passed":false,"decision":"repair","reason":"Observed incorrect fee sign"}', 'tool_calls': []}
            with mock.patch.object(session.ollama, '_chat_impl', side_effect=model):
                result = session._read_only_review_json('Audit the positive fee requirement.', 'Independent review', reader)
            self.assertFalse(result['passed'])
            self.assertEqual(len(seen), 3)
            self.assertFalse(reader.pending)
            self.assertFalse((root/'forbidden').exists())


if __name__ == '__main__':
    unittest.main()
