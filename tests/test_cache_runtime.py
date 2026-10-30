"""Regression checks for real-response accounting and fresh source reuse.

Remote and local model acceptance is exercised separately by the real verifiers.
"""
import json
import os
import sqlite3
import tempfile
import threading
import types
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel.context import ModelTokenLedger


class CacheRuntimeTests(unittest.TestCase):
    @staticmethod
    def usage(raw):
        return cc.OllamaClient._usage_tokens({'raw': raw})

    def test_provider_cache_absence_zero_and_hit_remain_distinct(self):
        unknown = self.usage({'prompt_eval_count': 100, 'eval_count': 10})
        zero = self.usage({'usage': {'prompt_tokens': 100, 'completion_tokens': 10,
                                    'prompt_tokens_details': {'cached_tokens': 0}}})
        hit = self.usage({'usage': {'prompt_tokens': 100, 'completion_tokens': 10,
                                   'prompt_tokens_details': {'cached_tokens': 70}}})
        self.assertIsNone(unknown['cached_input_tokens'])
        self.assertFalse(unknown['cache_metrics_available'])
        self.assertEqual(zero['cached_input_tokens'], 0)
        self.assertEqual(hit['cache_hit_ratio'], 0.7)
        self.assertEqual(hit['total_tokens'], 110)
        ledger = ModelTokenLedger()
        for usage in (unknown, zero, hit):
            ledger.note_cache(usage)
        stats = ledger.snapshot()['cache']
        self.assertEqual((stats['reported_calls'], stats['input_tokens'], stats['cached_input_tokens']), (2, 200, 70))
        self.assertEqual(ModelTokenLedger(state=ledger.snapshot()).snapshot()['cache'], stats)

    def test_anthropic_cache_charges_input_and_responses_details_do_not_double_count(self):
        native = self.usage({'usage': {'input_tokens': 20, 'output_tokens': 10,
                                      'cache_read_input_tokens': 70, 'cache_creation_input_tokens': 30,
                                      'total_tokens': 30}})
        responses = self.usage({'usage': {'input_tokens': 120, 'output_tokens': 10,
                                         'input_tokens_details': {'cached_tokens': 70}}})
        self.assertEqual(native['prompt_tokens'], 120)
        self.assertEqual(native['total_tokens'], 130)
        self.assertEqual(responses['prompt_tokens'], 120)
        self.assertEqual(native['cached_input_tokens'], responses['cached_input_tokens'])

    def test_native_empty_object_tool_arguments_and_thinking_fragments(self):
        client = cc.OllamaClient('http://127.0.0.1:11434', 'qwen3.6:latest')
        client.context_token_limit, client.strict_output_token_limit = 48000, True
        rows = [
            {'message': {'thinking': 'Part '}}, {'message': {'thinking': 'two.'}},
            {'message': {'tool_calls': [{'function': {'name': 'list_files', 'arguments': {}}}]}},
            {'done': True, 'done_reason': 'stop', 'prompt_eval_count': 20, 'eval_count': 10},
        ]
        with mock.patch.object(client, '_iter_response_lines_url_with_retries', return_value=iter(map(json.dumps, rows))) as transport:
            result = client.chat([{'role': 'user', 'content': 'List files'}], tools=[{
                'type': 'function', 'function': {'name': 'list_files', 'parameters': {'type': 'object', 'properties': {}}}}],
                max_tokens=256, think=False)
        self.assertEqual(result['tool_calls'][0]['function']['arguments'], {})
        self.assertNotIn('args_error', result['tool_calls'][0])
        self.assertEqual(result['thinking'], 'Part two.')
        payload = transport.call_args.args[1]
        self.assertIs(payload['think'], False)
        self.assertEqual(payload['options'], {'temperature': 0.2, 'num_predict': 256, 'num_ctx': 48000})

    def test_native_stream_preserves_whitespace_and_split_inline_tags(self):
        client = cc.OllamaClient('http://127.0.0.1:11434', 'qwen3.6:latest')
        client.context_token_limit = 48000
        pieces = ['<thi', 'nk>private reasoning</thi', 'nk>', '```json\n', '{"text": "a ', 'b",\n', '"count": 2}', '\n```']
        rows = [{'message': {'content': piece}} for piece in pieces] + [{'done': True}]
        with mock.patch.object(client, '_iter_response_lines_url_with_retries', return_value=iter(map(json.dumps, rows))):
            result = client.chat([{'role': 'user', 'content': 'Return JSON'}])
        self.assertEqual(cc.decode_model_json_object(result['content']), {'text': 'a b', 'count': 2})
        self.assertEqual(result['thinking'], 'private reasoning')

    def test_reasoning_cannot_inflate_reserved_output_budget(self):
        client = cc.OllamaClient('https://example.invalid', 'claude-test', provider='anthropic')
        client.reasoning_supported, client.reasoning_style = True, 'anthropic'
        client.strict_output_token_limit = True
        with mock.patch.object(client, '_chat_anthropic', return_value={'content': 'ok'}) as transport:
            client.chat([{'role': 'user', 'content': 'Review'}], max_tokens=3000, effort='high')
        self.assertEqual(transport.call_args.kwargs['max_tokens'], 3000)
        self.assertLess(transport.call_args.kwargs['reasoning']['payload']['thinking']['budget_tokens'], 3000)

    def test_source_cache_reuses_unchanged_and_invalidates_same_size_mtime_edit(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'source.py'
            session = cc.SessionState.__new__(cc.SessionState)
            session._long_content_source_cache = {}
            session._source_fingerprint_cache = {}
            path.write_text('old value\n')
            first, fingerprint = session._read_text_and_fingerprint(path, 'source.py')
            original_stat = path.stat()
            again, _ = session._read_text_and_fingerprint(path, 'source.py')
            self.assertEqual(again, first)
            self.assertEqual(session.source_cache_hits, 1)
            path.write_text('new value\n')
            os.utime(path, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
            newer, new_fingerprint = session._read_text_and_fingerprint(path, 'source.py')
            self.assertEqual(newer, 'new value\n')
            self.assertEqual(fingerprint['source_size'], new_fingerprint['source_size'])
            self.assertNotEqual(fingerprint['source_sha256'], new_fingerprint['source_sha256'])
            session._read_text_and_fingerprint(path, 'source.py', fresh=True)
            self.assertEqual(session.source_cache_misses, 3)

    def test_telemetry_migrates_old_rows_and_counts_only_reported_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'telemetry.sqlite'
            with sqlite3.connect(path) as connection:
                connection.execute('CREATE TABLE telemetry_events (id INTEGER PRIMARY KEY, ts REAL, boot_id TEXT, kind TEXT, '
                    'user_hash TEXT, session_id TEXT, app_id TEXT, name TEXT, status TEXT, duration_ms REAL, '
                    'prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER, provider TEXT, model TEXT)')
            store = cc.TelemetryStore(path)
            for cached in (None, 0, 70):
                store.record('llm_call', status='success', provider='test', model='m',
                    prompt_tokens=100, completion_tokens=10, total_tokens=110, cached_input_tokens=cached)
            dashboard = store.dashboard(types.SimpleNamespace(_lock=threading.RLock(), _session_mgrs={}))
            self.assertEqual(dashboard['tokens']['cache_measured_calls'], 2)
            self.assertEqual(dashboard['tokens']['cache_reported_prompt_tokens'], 200)
            self.assertEqual(dashboard['tokens']['cached_input_tokens'], 70)
            self.assertEqual(dashboard['models'][0]['cache_measured_calls'], 2)

    def test_live_clock_changes_only_after_stable_instruction_prefix(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = cc.SessionState('cache-prefix', 'Prefix', root/'sessions', 'http://127.0.0.1:11434', 'qwen3.6:latest',
                root/'skills', cc.CryptoBox(root/'Codes'), root/'repo', js_lib_root=root/'js',
                js_lib_download_enabled=False, web_search_enabled=False, defer_initial_persist=True)
            with mock.patch.object(session, '_runtime_environment_context_prompt_block', side_effect=['CLOCK_A', 'CLOCK_B']):
                first, second = session._system_prompt(), session._system_prompt()
            self.assertEqual(first.split('CLOCK_A')[0], second.split('CLOCK_B')[0])
            self.assertGreater(first.index('CLOCK_A'), 4000)


if __name__ == '__main__':
    unittest.main()
