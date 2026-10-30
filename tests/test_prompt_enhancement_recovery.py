"""Prompt enhancement must reach the model before using any local template."""
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import Clouds_Coder as cc


class PromptEnhancementRecoveryTests(unittest.TestCase):
    def app(self):
        directory = tempfile.TemporaryDirectory(); self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        session = SimpleNamespace(ui_language='en', active_profile_id='test',
            model_profiles={'test': {'provider': 'openai', 'model': 'test-model', 'base_url': 'https://example.invalid/v1'}},
            ollama=SimpleNamespace(model='test-model', provider='openai', base_url='https://example.invalid/v1'),
            lock=threading.RLock(), telemetry_callback=None, snapshot_safe=lambda **kwargs: {'conversation_feed': []})
        app = cc.AppContext.__new__(cc.AppContext)
        app._ide_session = lambda *_: session
        app.ide_resolve_workspace = lambda _u, _s, _r, path: (root, root/path, {'kind': 'workspace', 'label': 'fixture'})
        return app

    def reply(self):
        return {'content': json.dumps({'intent_summary': 'Preserve compatibility.',
            'enhanced_prompt': 'MODEL: Update literal/path.py and verify UTF-8 support.',
            'execution_steps': [{'title': 'Implement', 'action': 'Update literal/path.py', 'completion_check': 'Tests pass.'}]})}

    def test_real_chat_entry_accepts_unlimited_timeout_for_every_budget(self):
        for budget in ('low', 'medium', 'high', 'xhigh', 'middle'):
            with self.subTest(budget=budget):
                app = self.app()
                def answer(client, *args, **kwargs):
                    self.assertIsNone(client.timeout)
                    self.assertIsNone(client._effective_request_timeout())
                    return self.reply()
                with mock.patch.object(cc.OllamaClient, '_chat_impl', autospec=True, side_effect=answer) as call:
                    out = app.ide_enhance_agent_prompt('user', 'session', {'message': 'Keep literal/path.py compatible.', 'budget': budget})
                self.assertEqual(call.call_count, 1)
                self.assertEqual(out['source'], 'model')
                self.assertIn('MODEL:', out['enhanced_prompt'])
                self.assertEqual(out['budget'], 'medium' if budget == 'middle' else budget)

    def test_malformed_then_empty_thinking_then_complete_semantic_repair(self):
        app = self.app()
        damaged = {'content': '{"enhanced_prompt":"broken', 'finish_reason': 'length'}
        thinking = {'content': '', 'thinking': 'INTERNAL_ONLY_THOUGHT'}
        with mock.patch.object(cc.OllamaClient, '_chat_impl', side_effect=[damaged, thinking, self.reply()]) as call:
            out = app.ide_enhance_agent_prompt('u', 's', {'message': 'Keep literal/path.py compatible.', 'budget': 'low'})
        self.assertEqual(call.call_count, 3)
        self.assertEqual(out['source'], 'model')
        self.assertNotIn('INTERNAL_ONLY_THOUGHT', out['enhanced_prompt'])
        self.assertNotIn('INTERNAL_ONLY_THOUGHT', call.call_args.args[0][-1]['content'])
        self.assertIn('independent_semantic_repair', [row['stage'] for row in out['stages']])
        self.assertEqual([item.kwargs['max_tokens'] for item in call.call_args_list], [1800, 3600, cc.AGENT_MAX_OUTPUT_TOKENS])

    def test_three_invalid_outputs_use_explicit_fallback_after_model_attempts(self):
        with mock.patch.object(cc.OllamaClient, '_chat_impl', return_value={'content': '{"bad":'}) as call:
            out = self.app().ide_enhance_agent_prompt('u', 's', {'message': 'Fix literal/path.py.', 'budget': 'medium'})
        self.assertEqual(call.call_count, 3)
        self.assertEqual(out['source'], 'fallback')
        self.assertEqual(out['fallback_reason'], 'invalid_output')
        self.assertIn('Fix literal/path.py.', out['enhanced_prompt'])

    def test_complete_plain_model_prompt_survives_missing_analysis_fields(self):
        with mock.patch.object(cc.OllamaClient, '_chat_impl', return_value={'content': 'MODEL BODY: Preserve the public API and test the parser.'}) as call:
            out = self.app().ide_enhance_agent_prompt('u', 's', {'message': 'Preserve the public API.'})
        self.assertEqual(call.call_count, 1)
        self.assertEqual(out['source'], 'hybrid')
        self.assertIn('MODEL BODY:', out['enhanced_prompt'])

    def test_recovery_respects_the_admin_output_limit(self):
        app = self.app(); app.max_output_tokens = 2500
        with mock.patch.object(cc.OllamaClient, '_chat_impl', side_effect=[{'content': ''}, {'content': ''}, self.reply()]) as call:
            out = app.ide_enhance_agent_prompt('u', 's', {'message': 'Fix literal/path.py.', 'budget': 'xhigh'})
        self.assertEqual(out['source'], 'model')
        self.assertEqual([item.kwargs['max_tokens'] for item in call.call_args_list], [2500, 2500, 2500])

    def test_provider_raw_truncation_is_not_hidden_by_normalization(self):
        for raw in [{'choices': [{'finish_reason': 'length'}]}, {'done_reason': 'length'},
                    {'stop_reason': 'max_tokens'}, {'candidates': [{'finishReason': 'MAX_TOKENS'}]}]:
            with self.subTest(raw=raw):
                truncated = dict(self.reply(), raw=raw)
                with mock.patch.object(cc.OllamaClient, '_chat_impl', side_effect=[truncated, self.reply()]) as call:
                    out = self.app().ide_enhance_agent_prompt('u', 's', {'message': 'Keep literal/path.py compatible.'})
                self.assertEqual(call.call_count, 2)
                self.assertEqual(out['stages'][0]['status'], 'output_truncated')
                self.assertEqual(out['source'], 'model')

    def test_enhancer_sends_native_thinking_off_for_hybrid_model(self):
        app = self.app()
        app._ide_session().model_profiles['test']['model'] = 'deepseek-v4.1-flash'
        raw = {'choices': [{'message': {'content': self.reply()['content']}, 'finish_reason': 'stop'}]}
        with mock.patch.object(cc.OllamaClient, '_post_json_url', autospec=True, return_value=raw) as post:
            out = app.ide_enhance_agent_prompt('u', 's', {'message': 'Keep literal/path.py compatible.', 'budget': 'low'})
        self.assertEqual(out['source'], 'model')
        self.assertEqual(post.call_args.args[2]['thinking'], {'type': 'disabled'})

    def test_text_blocks_and_native_structured_result_are_model_outputs(self):
        body = self.reply()['content']
        for response in [{'content': [{'type': 'output_text', 'text': body}]},
                         {'content': '', 'tool_calls': [{'function': {'arguments': json.loads(body)}}]}]:
            with self.subTest(response=response):
                with mock.patch.object(cc.OllamaClient, '_chat_impl', return_value=response) as call:
                    out = self.app().ide_enhance_agent_prompt('u', 's', {'message': 'Keep literal/path.py compatible.'})
                self.assertEqual(call.call_count, 1)
                self.assertEqual(out['source'], 'model')

    def test_skill_refinement_also_regenerates_truncated_output(self):
        app = self.app()
        store = SimpleNamespace(skills={'fixture': {'body': 'Inspect first; verify the result.'}})
        app._ide_prompt_skill_catalog = lambda: (store, [{'id': 'fixture', 'name': 'fixture', 'description': 'Parser checks'}], False)
        first = json.loads(self.reply()['content'])
        first['selected_skills'] = [{'id': 'fixture'}]
        damaged = {'content': '{"enhanced_prompt":"partial', 'finish_reason': 'length'}
        final = {'content': json.dumps({'enhanced_prompt': 'REFINED: Verify literal/path.py using fixture.'})}
        with mock.patch.object(cc.OllamaClient, '_chat_impl', side_effect=[{'content': json.dumps(first)}, damaged, final]) as call:
            out = app.ide_enhance_agent_prompt('u', 's', {'message': 'Fix literal/path.py.', 'skills_awareness': True})
        self.assertEqual(call.call_count, 3)
        self.assertIn('REFINED:', out['enhanced_prompt'])
        self.assertEqual(out['selected_skills'][0]['id'], 'fixture')

    def test_provider_think_prefix_is_hidden_but_literal_json_content_is_preserved(self):
        for content, expected in [('<think>HIDDEN_REASON</think>## Goal\nFix the parser.', 'Fix the parser.'),
                                  (json.dumps({'enhanced_prompt': 'Keep literal <think> marker unchanged.'}), 'literal <think>')]:
            with self.subTest(content=content):
                with mock.patch.object(cc.OllamaClient, '_chat_impl', return_value={'content': content}):
                    out = self.app().ide_enhance_agent_prompt('u', 's', {'message': 'Keep the parser compatible.'})
                self.assertNotEqual(out['source'], 'fallback')
                self.assertIn(expected, out['enhanced_prompt'])
                self.assertNotIn('HIDDEN_REASON', out['enhanced_prompt'])

    def test_deadline_override_bounds_an_unlimited_client_and_restores_state(self):
        client = cc.OllamaClient('http://unused.invalid', 'test'); client.timeout = None
        def answer(*args, **kwargs):
            self.assertGreater(client._effective_request_timeout(), 0)
            self.assertLessEqual(client._effective_request_timeout(), .5)
            return self.reply()
        with mock.patch.object(client, '_chat_impl', side_effect=answer):
            client.chat([{'role': 'user', 'content': 'test'}], request_timeout=.5)
        self.assertIsNone(client._effective_request_timeout())
        self.assertEqual(client._request_local().deadline, 0)
        client._request_local().deadline = time.monotonic()-1
        with self.assertRaises(cc.OllamaError):client._effective_request_timeout()
