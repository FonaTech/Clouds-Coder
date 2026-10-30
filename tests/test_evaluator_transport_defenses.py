"""Prevent evaluator faults and generic transport names from distorting results."""
import copy
import json
import shlex
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import URLError

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config
from liquid_kernel.agentic import AgenticBenchmark, TaskWorkspace, canonicalize_task_bank, digest, normalize_task_design
from liquid_kernel.context import EvaluationDefinitionError, normalize_executable_command
from liquid_kernel.control import BASELINE_KERNEL_FILES, LiquidKernelError


class EvaluatorTransportDefenses(unittest.TestCase):
    def plane(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return LiquidKernelControlPlane(Path(temp.name))

    def bank(self):
        task = {'id': 'real-task', 'source_id': 'source-a', 'split': 'train',
                'goal': 'Write result.txt and verify its exact bytes',
                'starter_files': {}, 'followups': [{'after_round': 2, 'content': 'Keep the exact bytes'}],
                'checks': [{'kind': 'file_exists', 'path': 'result.txt'},
                           {'kind': 'command', 'command': "import pathlib; assert pathlib.Path('result.txt').read_bytes() == b'a\\n\\x00z'", 'exit_code': 0}]}
        task['fingerprint'] = digest(task)
        return {'tasks': [task], 'fingerprint': digest([task]), 'train_count': 1, 'holdout_count': 0}

    def test_python_assertion_source_and_literals_are_preserved_exactly(self):
        bank = self.bank()
        source = bank['tasks'][0]['checks'][1]['command']
        canonical = canonicalize_task_bank(bank)
        command = canonical['tasks'][0]['checks'][1]['command']
        self.assertEqual(shlex.split(command), ['python3', '-c', source])
        self.assertEqual(bank, self.bank())
        self.assertNotEqual(canonical['fingerprint'], bank['fingerprint'])
        self.assertFalse(canonical['evaluator_lineage']['assertions_changed'])
        self.assertEqual(canonical['evaluator_lineage']['previous_bank_fingerprint'], bank['fingerprint'])
        self.assertEqual(canonicalize_task_bank(canonical), canonical)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'result.txt').write_bytes(b'a\n\x00z')
            rows = TaskWorkspace(root, lambda: None).evaluate(canonical['tasks'][0]['checks'])
        self.assertTrue(all(row['ok'] for row in rows), rows)

    def test_explicit_python_and_fences_validate_before_execution(self):
        for command, language in [('assert 2 + 2 == 4', 'python'), ('```python\nassert True\n```', '')]:
            normalized = normalize_executable_command(command, language, validate_shell=True)
            self.assertTrue(normalized['command'].startswith('python3 -c '))
        for command, language in [('import sys; assert (', ''), ('if then', 'shell')]:
            with self.assertRaises(EvaluationDefinitionError):
                normalize_executable_command(command, language, validate_shell=True)

    def test_task_definition_supports_typed_code_without_changing_assertions(self):
        task = self.bank()['tasks'][0]
        check = task['checks'][1]
        check['code'] = check.pop('command')
        check['language'] = 'python'
        cfg = normalize_evolution_config({'mode': 'Thinking'})['task_benchmark']
        _, _, checks = normalize_task_design(task, cfg)
        self.assertEqual(shlex.split(checks[1]['command'])[-1], check['code'])

    def test_invalid_frozen_checker_aborts_before_any_model_call(self):
        model = mock.Mock()
        benchmark = AgenticBenchmark(model, lambda: None)
        cfg = normalize_evolution_config({'mode': 'Thinking'})['task_benchmark']
        with self.assertRaises(EvaluationDefinitionError):
            benchmark.run(BASELINE_KERNEL_FILES, self.bank()['tasks'], cfg)
        model.assert_not_called()

    def test_evaluator_does_not_turn_definition_failure_into_score_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            workspace = TaskWorkspace(Path(temp), lambda: None)
            with self.assertRaises(EvaluationDefinitionError):
                workspace.evaluate(self.bank()['tasks'][0]['checks'])
            with mock.patch.object(workspace, 'command', side_effect=EvaluationDefinitionError('runtime unavailable')):
                with self.assertRaises(EvaluationDefinitionError):
                    workspace.evaluate([{'kind': 'command', 'command': 'true', 'exit_code': 0}])
            # An explicitly expected nonzero exit remains a valid assertion.
            with mock.patch.object(workspace, 'command', return_value={'exit_code': 127, 'output': ''}):
                self.assertTrue(workspace.evaluate([{'kind': 'command', 'command': 'exit 127', 'exit_code': 127}])[0]['ok'])

    def test_legacy_scores_flagged_without_mutating_history_or_bank(self):
        plane = self.plane()
        run = plane.registry.create_run(plane.config(), 'test')
        plane.registry.update_run(run, 'rejected', result_json={'incumbent': {'hard': 33.3}})
        bank_path = plane.registry.experience_root/run/'task_bank.json'
        bank_path.parent.mkdir(parents=True)
        bank_path.write_text(json.dumps(self.bank()))
        before = bank_path.read_bytes()
        with sqlite3.connect(plane.registry.root/'registry.sqlite') as conn:
            result_before = conn.execute('select result_json from runs where run_id=?', (run,)).fetchone()[0]
        detail = plane.registry.run_detail(run)
        self.assertFalse(detail['score_summary']['evaluation_valid'])
        self.assertEqual(detail['score_summary']['incumbent']['hard'], 33.3)
        self.assertEqual(before, bank_path.read_bytes())
        with sqlite3.connect(plane.registry.root/'registry.sqlite') as conn:
            self.assertEqual(result_before, conn.execute('select result_json from runs where run_id=?', (run,)).fetchone()[0])

    def test_manual_approval_rejects_invalid_historical_evidence(self):
        plane = self.plane()
        plane.save_config({'mode': 'Thinking'})
        run = plane.registry.create_run(plane.config(), 'test')
        plane.registry.update_run(run, 'awaiting_approval')
        path = plane.registry.experience_root/run/'task_bank.json'
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(self.bank()))
        with self.assertRaises(LiquidKernelError) as caught:
            plane.approve(run)
        self.assertEqual(caught.exception.code, 'invalid_evaluation_definition')

    def test_ordinary_bash_reports_missing_interpreter_before_execution(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session._rewrite_shell_virtual_paths = lambda command, cwd: command
        session._shell_timeout_mode = lambda: 'auto'
        session._shell_async_handoff_seconds = lambda: 1
        with mock.patch.object(cc.subprocess, 'Popen') as execute:
            result = session._run_shell_meta('import pathlib; assert True', Path('/tmp'), 10)
        execute.assert_not_called()
        self.assertEqual(result['exit_code'], -1)
        self.assertIn('interpreter', result['error'])
        self.assertTrue(result['suggested_command'].startswith('python3 -c '))

    def app(self, profile=None):
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = self.plane()
        app._liquid_kernel_profile = lambda _: copy.deepcopy(profile or {
            'model': 'online-thinking-model', 'provider': 'openai',
            'base_url': 'https://online.example/v1', 'request_timeout': 900})
        return app

    def test_evolution_honors_profile_timeout_and_remaining_task_deadline(self):
        app = self.app()
        with mock.patch.object(cc.OllamaClient, 'chat', return_value={'content': '{"ok":true}'}) as chat:
            self.assertTrue(app._liquid_kernel_transport_call('Return JSON', '{}', '', 1024)['ok'])
            self.assertEqual(chat.call_args.kwargs['request_timeout'], 900)
            app.liquid_kernel._active_deadline = time.monotonic()+37
            app._liquid_kernel_transport_call('Return JSON', '{}', '', 1024)
            self.assertGreater(chat.call_args.kwargs['request_timeout'], 35)
            self.assertLessEqual(chat.call_args.kwargs['request_timeout'], 37)

    def test_deadline_diagnostic_does_not_impersonate_server_http408(self):
        error = cc.OllamaError('model request total deadline exhausted', status=408)
        error.deadline_exhausted = True
        app = self.app()
        run = app.liquid_kernel.registry.create_run(app.liquid_kernel.config(), 'test')
        app.liquid_kernel.active_run_id = run
        with mock.patch.object(cc.OllamaClient, 'chat', side_effect=error):
            with self.assertRaises(LiquidKernelError) as caught:
                app._liquid_kernel_transport_call('Return JSON', '{}', '', 1024)
        details = caught.exception.details
        self.assertEqual(details['error_code'], 'request_deadline_exhausted')
        self.assertEqual(details['http_status'], 0)
        self.assertEqual(details['endpoint_host'], 'online.example')
        self.assertNotIn('OllamaError', str(caught.exception))
        activity = app.liquid_kernel.registry.run_detail(run)['progress']['activity']
        for row in activity:
            if row['kind'] in {'model_request_failed', 'model_transport_error'}:
                self.assertEqual(row['error_code'], 'request_deadline_exhausted')
                self.assertEqual(row['http_status'], 0)

    def test_http408_auth_rate_limit_and_connection_timeout_are_distinct(self):
        self.assertEqual(cc.OllamaError('HTTP 408', 408).diagnostics()['http_status'], 408)
        self.assertEqual(cc.OllamaError('HTTP 401', 401).diagnostics()['error_code'], 'model_auth_failed')
        self.assertEqual(cc.OllamaError('HTTP 429', 429).diagnostics()['error_code'], 'model_rate_limited')
        try:
            raise URLError(TimeoutError('timed out'))
        except URLError as cause:
            error = cc.OllamaError('Connection error')
            error.__cause__ = cause
        self.assertEqual(error.diagnostics()['error_code'], 'request_timeout')

    def test_old_generic_timeout_is_explained_without_rewriting_history(self):
        plane = self.plane()
        run = plane.registry.create_run(plane.config(), 'test')
        result = {'code': 'model_call_failed', 'details': {'reason': 'model request total deadline exhausted', 'status': 408, 'error_type': 'OllamaError'}}
        plane.registry.update_run(run, 'failed', result_json=result)
        detail = plane.registry.run_detail(run)
        self.assertEqual(detail['result']['details']['error_code'], 'request_deadline_exhausted')
        with sqlite3.connect(plane.registry.root/'registry.sqlite') as conn:
            self.assertNotIn('error_code', conn.execute('select result_json from runs where run_id=?', (run,)).fetchone()[0])

    def test_http429_backoff_deadline_preserves_cause_for_stream_and_json(self):
        for streaming in (False, True):
            with self.subTest(streaming=streaming):
                client = cc.OllamaClient('https://test-' + str(streaming).lower() + '.invalid/v1', 'test', timeout=600, provider='openai')
                error = cc.OllamaError('rate limited', status=429, retry_after=60)
                endpoint = client.base_url+'/chat/completions'
                def request(*args, **kwargs):
                    if streaming:
                        return list(client._iter_response_lines_url_with_retries(endpoint, {}, max_attempts=5))
                    return client._post_json_url_with_retries(endpoint, {}, max_attempts=5)
                method = '_iter_response_lines_url' if streaming else '_post_json_url'
                with mock.patch.object(client, method, side_effect=error), mock.patch.object(client, '_chat_impl', side_effect=request):
                    with self.assertRaises(cc.OllamaError) as caught:
                        client.chat([{'role': 'user', 'content': 'test'}], request_timeout=.1)
                details = caught.exception.diagnostics()
                self.assertEqual(details['error_code'], 'request_deadline_exhausted')
                self.assertEqual(details['http_status'], 0)
                self.assertEqual(details['last_http_status'], 429)
                self.assertEqual(details['cause_code'], 'model_rate_limited')
                self.assertIsNone(client._request_local().last_retry_error)
                with client._retry_lock:
                    client._endpoint_cooldowns.pop(client._http_retry_key(endpoint), None)

    def test_historical_timeout_retains_transient_rate_limit_cause(self):
        plane = self.plane()
        run = plane.registry.create_run(plane.config(), 'test')
        plane.registry.event(run, 'model_request_retry', {'http_status': 429, 'retry_after_seconds': 60})
        plane.registry.event(run, 'model_transport_error', {'error_type': 'OllamaError'})
        plane.registry.update_run(run, 'failed', result_json={'code': 'model_call_failed', 'details': {'reason': 'model request total deadline exhausted'}})
        result = plane.registry.run_detail(run)
        self.assertEqual(result['result']['details']['last_http_status'], 429)
        self.assertEqual(result['progress']['activity'][-1]['cause_code'], 'model_rate_limited')
