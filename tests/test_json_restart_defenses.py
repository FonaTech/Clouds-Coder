import json
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.context import HistoryArchive, ReviewEvidence
import test_single_no_plan_todo_bootstrap as bootstrap


class StructuredOutputDefenses(unittest.TestCase):
    def app(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = LiquidKernelControlPlane(Path(directory.name))
        app._liquid_kernel_profile = lambda _: {'provider': 'ollama', 'base_url': 'http://localhost:11434', 'model': 'test'}
        return app

    def test_complete_local_literals_and_reasoning_wrapper_preserve_data(self):
        cases = [(' <think>hidden {bad}</think> {"ok":true,"rows":[1,2,],}', {'ok': True, 'rows': [1, 2]}),
                 ("```python\n{'任务': '继续', 'ok': True}\n```", {'任务': '继续', 'ok': True}),
                 ('{"content":"literal ,} and ```python\\ncode```",}', {'content': 'literal ,} and ```python\ncode```'})]
        for text, expected in cases:
            self.assertEqual(cc.standard_model_json_object(text), expected)
        for text in ['<think> {"wrong":true}', '{"partial":{"score":99}', '[{"score":99}]', '{"score":NaN}', "{'score': (1, 2)}", "{1:'x'}", '{"a":1}{"b":2}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                cc.standard_model_json_object(text)

    def test_semantic_refusal_empty_source_or_fabricated_values_are_rejected(self):
        for reply, source in [('{"repair_status":"unrecoverable","missing":["source truncated"]}', 'scoreA:97'),
                              ('{"score_a":99}', 'scoreA:97'), ('{"score_a":97}', ''),
                              ('{"content":"invented code"}', 'content:missing')]:
            with self.subTest(reply=reply), self.assertRaises(ValueError):
                cc.validate_semantic_json_repair(reply, source)
        self.assertEqual(cc.validate_semantic_json_repair('{"score_a":97,"score_b":97}', 'scoreA=97; scoreB=97'), {'score_a':97,'score_b':97})

    def test_evolution_last_attempt_uses_isolated_semantic_engine_and_accounts_all_calls(self):
        app = self.app()
        replies = ['scoreA=97; scoreB=97', 'scoreA=97; scoreB=97', '{"score_a":97,"score_b":97}']
        calls = []
        def chat(*args, **kwargs):
            calls.append((args, kwargs))
            return {'content': replies.pop(0), 'raw': {'done_reason': 'stop'}, 'tool_calls': []}
        with mock.patch.object(cc.OllamaClient, 'chat', side_effect=chat):
            result = app._liquid_kernel_transport_call('Return JSON score_a/score_b from observed evidence.', '{}', 'test', 1024)
        self.assertEqual(result['score_a'],97)
        self.assertEqual(len(calls),3)
        self.assertIn('semantic normalization engine', calls[2][1]['system'])
        self.assertIsNone(calls[2][1]['tools'])
        self.assertEqual(calls[2][1]['label'], 'evolution_json_semantic_repair')
        self.assertGreater(result['_evolution_usage']['total_tokens'],0)

    def test_evolution_persistent_failure_is_bounded_and_never_returns_success(self):
        app = self.app()
        with mock.patch.object(cc.OllamaClient, 'chat', return_value={'content':'ambiguous', 'raw': {'done_reason':'stop'}}) as chat:
            with self.assertRaises(cc.LiquidKernelError) as error:
                app._liquid_kernel_transport_call('Return JSON.', '{}', 'test',1024)
        self.assertEqual(chat.call_count,3)
        self.assertEqual(error.exception.code, 'invalid_model_output')
        self.assertEqual(len(error.exception.details['attempts']),3)

    def test_structured_final_envelope_cannot_bypass_semantic_recovery(self):
        from liquid_kernel.context import RECALL_TOOL
        app = self.app()
        packet = json.dumps({'messages':[{'role':'user','content':'Compare A and B.'}],
                             'tools':[RECALL_TOOL], 'require_json_final':True})
        replies = [json.dumps({'final':'scoreA=97; scoreB=97'}),
                   json.dumps({'final':'scoreA=97; scoreB=97'}), '{"score_a":97,"score_b":97}']
        calls = []
        def chat(*args, **kwargs):
            calls.append(kwargs)
            return {'content':replies.pop(0),'raw':{'done_reason':'stop'}}
        with mock.patch.object(cc.OllamaClient,'chat',side_effect=chat):
            result = app._liquid_kernel_transport_call('Return JSON scores score_a, score_b.',packet,'test',1024)
        self.assertEqual(result['score_a'],97)
        self.assertEqual(len(calls),3)
        self.assertIsNone(calls[-1]['tools'])
        self.assertEqual(calls[-1]['label'],'evolution_json_semantic_repair')
        with mock.patch.object(cc.OllamaClient,'chat',return_value={
                'content':json.dumps({'final':{'final':{'score_a':97,'score_b':97}}}),
                'raw':{'done_reason':'stop'}}) as chat:
            result = app._liquid_kernel_transport_call('Return JSON scores.',packet,'test',1024)
        self.assertEqual(result['score_b'],97)
        self.assertEqual(chat.call_count,1)

    def test_repair_cannot_bypass_phase_budget(self):
        app = self.app()
        app.liquid_kernel._token_limit = 100000
        app.liquid_kernel._rollout_token_ceiling = 2
        app.liquid_kernel._model_budget_label = 'proposal'
        with mock.patch.object(cc.OllamaClient, 'chat') as chat:
            with self.assertRaisesRegex(TimeoutError,'proposal_token_budget_exhausted'):
                app._liquid_kernel_transport_call('Return JSON.', '{}', 'test',1024)
        chat.assert_not_called()

    def test_normal_review_uses_same_semantic_engine_without_tools(self):
        session = bootstrap.SingleNoPlanTodoBootstrapTests().bare_session()
        session.context_token_upper_bound = 8000
        session.max_agent_rounds = 10
        replies = iter(['passed=true; score=97', 'passed=true; score=97', '{"passed":true,"score":97}'])
        calls = []
        def chat(*args, **kwargs):
            calls.append(kwargs)
            return {'content':next(replies)}
        session.ollama = types.SimpleNamespace(chat=chat)
        with tempfile.TemporaryDirectory() as directory:
            reader = ReviewEvidence(HistoryArchive(Path(directory)/'history.jsonl'))
            result = session._read_only_review_json('Review observed evidence.', 'Return JSON passed, score.', reader)
        self.assertTrue(result['passed'])
        self.assertEqual(len(calls),3)
        self.assertIsNone(calls[2]['tools'])
        self.assertIn('semantic normalization engine', calls[2]['system'])

    def test_normal_tool_recovery_uses_semantic_engine_and_large_writes_stay_blocked(self):
        session = bootstrap.SingleNoPlanTodoBootstrapTests().bare_session()
        with mock.patch.object(session,'_continue_truncated_assistant_output', return_value=('path=demo.txt', '', {})), \
             mock.patch.object(session,'_parse_tool_args_text', return_value=({},'invalid')), \
             mock.patch.object(session,'_chat_with_same_model_retry', return_value={'content':'{"path":"demo.txt"}'}) as chat:
            ok,args,note = session._recover_tool_args_from_malformed(name='read_file',raw_args='path=demo.txt',pinned_selection='test')
        self.assertTrue(ok)
        self.assertEqual(args,{'path':'demo.txt'})
        self.assertEqual(note,'semantic-repaired')
        self.assertIsNone(chat.call_args.kwargs['tools'])
        with mock.patch.object(session,'_chat_with_same_model_retry') as chat:
            ok,args,note = session._recover_tool_args_from_malformed(name='write_file', raw_args='{"path":"a","content":"'+'x'*20000,pinned_selection='test')
        self.assertFalse(ok)
        chat.assert_not_called()


class RestartDefenses(unittest.TestCase):
    def test_slow_optional_download_does_not_block_readiness(self):
        entered, release = threading.Event(), threading.Event()
        app = types.SimpleNamespace(workspace=Path('/tmp'),js_lib_download_enabled=True)
        def download(*args, **kwargs):
            entered.set()
            release.wait(5)
            return {'available':1}
        with mock.patch.object(cc,'ensure_offline_js_libs', side_effect=download):
            start = time.monotonic()
            worker = cc._start_offline_js_warmup(app)
            self.assertLess(time.monotonic()-start,1)
            self.assertTrue(entered.wait(1))
            self.assertEqual(app.offline_js_warmup['state'],'running')
            release.set()
            worker.join(2)
        self.assertEqual(app.offline_js_warmup['state'],'completed')
        self.assertEqual(app.offline_js_summary['available'],1)

    def test_supervisor_verifies_exact_child_and_bypasses_proxy(self):
        import urllib.request
        config = cc._admin_factory_config()
        config.update(host='127.0.0.1',port=18999)
        process = types.SimpleNamespace(pid=123456,poll=lambda:None)
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({'boot_id':'new','pid':123456,'restart_verified':True}).encode()
        opener = mock.Mock()
        opener.open.return_value = response
        with tempfile.TemporaryDirectory() as directory, \
             mock.patch.object(cc.subprocess,'Popen', return_value=process) as launch, \
             mock.patch.object(urllib.request,'build_opener',return_value=opener) as build:
            self.assertTrue(cc._admin_supervised_restart(config,config,restart_nonce='test',restart_from_boot_id='old',error_path=Path(directory)/'restart_error.json',timeout_seconds=5))
        self.assertEqual(build.call_args.args[0].proxies,{})
        self.assertEqual(launch.call_args.kwargs['stderr'],cc.subprocess.STDOUT)


if __name__=='__main__':
    unittest.main()
