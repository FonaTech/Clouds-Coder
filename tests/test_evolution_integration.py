"""Admin -> saved references -> real HTTP transport -> evolution worker."""
import base64
import http.client
import importlib.util
import io
import json
import sqlite3
import tempfile
import threading
import unittest
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from test_agentic_evolution import TaskModel, experiences
from test_liquid_kernel import (
    LiquidKernelControlPlane,
    improving_judge,
    improving_model,
    wait_for_run,
)

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelError
from liquid_kernel.control import valid_judge_score


class ModelService(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.calls.append({'path': self.path, 'body': payload, 'auth': self.headers.get('Authorization')})
        self.server.entered.set()
        self.server.release.wait(10)
        mode = self.server.mode
        judge = 'independent blind evaluator' in json.dumps(payload)
        if mode == 'failure' or (mode == 'judge_failure' and judge):
            self.send_response(401)
            body = b'credential failure: secret-generator secret-judge'
        else:
            if mode == 'agentic':
                content = ({'messages': payload['messages'], 'tools': payload['tools']} if payload.get('tools') and not judge
                           else json.loads(payload['messages'][-1]['content']))
                if judge:
                    result = {'score_a': content['trajectory_a']['score'], 'score_b': content['trajectory_b']['score'],
                              'rationale': 'Actual paired trajectory and artifact outcomes', 'confidence': 1.0}
                else:
                    result = self.server.task_model('', content)
            elif judge:
                content = json.loads(payload['messages'][-1]['content'])
                is_candidate_a = 'dict(tool)' in content['kernel_a']
                result = {'score_a': 85 if is_candidate_a else 50, 'score_b': 50 if is_candidate_a else 85,
                          'rationale': 'Compared independent requests', 'confidence': 0.9}
            elif mode == 'no_change':
                result = {'decision': 'no_change', 'reason': 'No useful change found'}
            elif mode == 'invalid':
                result = {'unexpected': True}
            else:
                result = improving_model('', '', '', 4096)
            message = {'role': 'assistant', 'content': json.dumps(result)}
            if mode == 'native_tools':
                message = {'role': 'assistant', 'content': None, 'tool_calls': [
                    {'id': 'call-native', 'type': 'function', 'function': {'name': 'read_file', 'arguments': '{"path":"input.txt"}'}}]}
            body = json.dumps({'choices': [{'message': message, 'finish_reason': 'tool_calls' if mode == 'native_tools' else 'stop'}]}).encode()
            self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_app(root, model_url):
    app = cc.AppContext.__new__(cc.AppContext)
    app.codes_root = root / 'Codes'
    app.crypto = cc.CryptoBox(app.codes_root)
    app.ide_auth = cc.IDEAuthStore(root / 'ide.sqlite')
    app.ide_password_login_enabled = True
    app.global_profiles = {
        'gen': {'provider': 'openai_compat', 'model': 'wrong-default', 'models': ['selected-model', 'wrong-default'],
                'base_url': model_url + '/generator', 'api_key': 'secret-generator', 'temperature': 0.1},
        'judge': {'provider': 'openai_compat', 'model': 'wrong-default', 'models': ['selected-model', 'wrong-default'],
                  'base_url': model_url + '/judge', 'api_key': 'secret-judge', 'temperature': 0.1},
    }
    app.global_active_profile_id = 'gen'
    app.model = 'wrong-default'
    app.base_url = model_url
    app.verify_admin_token = lambda token: token == 'test-admin'
    attach_plane(app, root / 'evolution')
    return app


def attach_plane(app, root):
    app.liquid_kernel = LiquidKernelControlPlane(
        root, model_callback=app._liquid_kernel_model_call, judge_callback=app._liquid_kernel_judge_call,
        model_resolver=lambda config: app._evolution_models().bind_run(config),
        config_validator=lambda config, **kwargs: app._evolution_models().validate_config(config, **kwargs))
    # These transport fixtures test the retained contract-only backend. New
    # session-task execution is exercised separately with real file tools.
    config = app.liquid_kernel.config()
    config["task_benchmark"]["enabled"] = False
    app.liquid_kernel.config_path.write_text(json.dumps(config))


class EvolutionHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.model_server = ThreadingHTTPServer(('127.0.0.1', 0), ModelService)
        self.model_server.calls = []
        self.model_server.mode = 'change'
        self.model_server.entered = threading.Event()
        self.model_server.release = threading.Event()
        self.model_server.release.set()
        self.model_url = 'http://127.0.0.1:' + str(self.model_server.server_port)
        self.app = make_app(self.root, self.model_url)
        self.server = cc.AgentHTTPServer(('127.0.0.1', 0), cc.Handler, self.app)
        self.threads = [threading.Thread(target=server.serve_forever, daemon=True) for server in (self.model_server, self.server)]
        for thread in self.threads:
            thread.start()

    def tearDown(self):
        self.model_server.release.set()
        if self.app.liquid_kernel.active_run_id:
            self.app.liquid_kernel.cancel(self.app.liquid_kernel.active_run_id)
            wait_for_run(self.app.liquid_kernel, self.app.liquid_kernel.active_run_id)
        for server in (self.server, self.model_server):
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(2)
        self.temp.cleanup()

    def request(self, path, payload=None, *, auth=True, cookie=''):
        conn = http.client.HTTPConnection('127.0.0.1', self.server.server_port, timeout=10)
        headers = {'Content-Type': 'application/json'}
        if auth:
            headers['Authorization'] = 'Bearer test-admin'
        if cookie:
            headers['Cookie'] = 'clouds_ide_session=' + cookie
        try:
            conn.request('POST' if payload is not None else 'GET', '/api/admin/evolution' + path,
                         None if payload is None else json.dumps(payload), headers)
            response = conn.getresponse()
            return response.status, json.loads(response.read())
        finally:
            conn.close()

    def save(self, generator=None, judge=None, cookie=''):
        cfg = self.app.liquid_kernel.config()
        generator = generator or {'source': 'global', 'owner': '', 'profile_id': 'gen', 'model': 'selected-model'}
        judge = judge or {'source': 'global', 'owner': '', 'profile_id': 'judge', 'model': 'selected-model'}
        status, data = self.request('/config', {'revision': cfg['revision'], 'values': {
            'mode': 'Thinking', 'schedule': 'off', 'generator_model_ref': generator, 'judge_model_ref': judge,
        }}, cookie=cookie)
        self.assertEqual(status, 200, data)
        # Keep the integration run small; production presets are unchanged.
        cfg = data['config']
        cfg['budget'].update(candidate_limit=1, max_tokens=4096)
        status, data = self.request('/config', {'revision': cfg['revision'], 'values': cfg}, cookie=cookie)
        self.assertEqual(status, 200, data)
        return data['config']

    def start(self, config):
        status, out = self.request('/runs', {'revision': config['revision']})
        self.assertEqual(status, 202, out)
        return out['run_id']

    def test_worker_native_tool_response_is_not_rejected_as_non_json(self):
        from liquid_kernel.agentic import TOOLS
        self.model_server.mode = 'native_tools'
        result = self.app._liquid_kernel_model_call('Complete the task using real tools.', json.dumps({
            'messages': [{'role': 'user', 'content': 'Read input.txt'}], 'tools': TOOLS}), 'gen', 512)
        self.assertEqual(result['tool_calls'], [{'name': 'read_file', 'arguments': {'path': 'input.txt'}}])
        body = self.model_server.calls[-1]['body']
        self.assertEqual(body['tools'], TOOLS)
        self.assertNotIn('response_format', body)
        self.assertIn('parameters', body['tools'][1]['function'])

    def test_http_selected_models_addresses_credentials_and_judge(self):
        config = self.save()
        run_id = self.start(config)
        detail = wait_for_run(self.app.liquid_kernel, run_id)
        self.assertEqual(detail['status'], 'awaiting_approval', detail)
        calls = self.model_server.calls
        self.assertEqual(len(calls), 2)
        prompt = json.loads(calls[0]['body']['messages'][-1]['content'])
        self.assertNotIn('harness.py', prompt['allowed_patch_files'])
        self.assertTrue(calls[0]['path'].startswith('/generator/'))
        self.assertTrue(calls[1]['path'].startswith('/judge/'))
        self.assertEqual([c['body']['model'] for c in calls], ['selected-model'] * 2)
        self.assertEqual([c['auth'] for c in calls], ['Bearer secret-generator', 'Bearer secret-judge'])
        stages = [e['payload']['stage'] for e in detail['events'] if e['kind'] == 'model_call_completed']
        self.assertEqual(stages, ['generator', 'judge'])
        self.assertNotIn('secret-generator', json.dumps(detail))
        self.assertNotIn('api_key', json.dumps(detail['config']))
        self.assertIsNone(self.app.liquid_kernel.registry.active_state()['canary'])
        self.assertEqual(self.request('/runs/' + run_id + '/cancel', {})[0], 200)
        self.assertEqual(self.app.liquid_kernel.registry.run_detail(run_id)['status'], 'cancelled')

    def test_same_model_same_profile_still_makes_independent_requests(self):
        ref = {'source': 'global', 'owner': '', 'profile_id': 'gen', 'model': 'selected-model'}
        config = self.save(generator=ref, judge=ref)
        detail = wait_for_run(self.app.liquid_kernel, self.start(config))
        self.assertEqual(detail['status'], 'awaiting_approval')
        self.assertEqual(len(self.model_server.calls), 2)
        self.assertNotEqual(self.model_server.calls[0]['body']['messages'], self.model_server.calls[1]['body']['messages'])

    def test_session_tasks_execute_over_real_http_and_judge_actual_trajectories(self):
        self.app.liquid_kernel._run = self.app.liquid_kernel._production_run
        self.model_server.mode = 'agentic'
        self.model_server.task_model = TaskModel()
        self.app.liquid_kernel.experience_provider = lambda *_args: experiences()
        config = self.save()
        status, saved = self.request('/config', {'revision': config['revision'], 'values': {
            'task_benchmark': {'enabled': True, 'max_tasks': 2, 'max_rounds': 8, 'turn_max_tokens': 512},
            'budget': {**config['budget'], 'max_tokens': 240000},
        }})
        self.assertEqual(status, 200, saved)
        detail = wait_for_run(self.app.liquid_kernel, self.start(saved['config']), timeout=15)
        self.assertEqual(detail['status'], 'awaiting_approval', detail)
        self.assertEqual(detail['result']['benchmark_kind'], 'session_agentic')
        self.assertEqual(detail['result']['candidate']['hard'], 100)
        self.assertGreaterEqual(len(self.model_server.calls), 24)
        judge_calls = [call for call in self.model_server.calls if call['path'].startswith('/judge/')]
        self.assertEqual(len(judge_calls), 3)
        judged = json.loads(judge_calls[0]['body']['messages'][-1]['content'])
        self.assertEqual(judged['kernel_a'], '')
        self.assertEqual(judged['kernel_b'], '')
        self.assertIn('artifacts', judged['trajectory_a']['rows'][0])
        self.assertTrue(all(call['body']['model'] == 'selected-model' for call in self.model_server.calls))

    def test_errors_are_failures_and_cancel_never_deploys(self):
        config = self.save()
        for mode in ('failure', 'judge_failure', 'invalid', 'no_change'):
            with self.subTest(mode=mode):
                self.model_server.mode = mode
                detail = wait_for_run(self.app.liquid_kernel, self.start(config))
                self.assertEqual(detail['status'], 'no_change' if mode == 'no_change' else 'failed', detail)
                self.assertNotIn('secret-generator', json.dumps(detail))
                self.assertNotIn('secret-judge', json.dumps(detail))
                self.assertFalse(self.app.liquid_kernel.run_lock.locked())
        self.model_server.mode = 'change'
        self.model_server.entered.clear()
        self.model_server.release.clear()
        run_id = self.start(config)
        self.assertTrue(self.model_server.entered.wait(5))
        self.assertEqual(self.request('/runs', {'revision': config['revision']})[0], 409)
        self.assertEqual(self.request('/runs/' + run_id + '/cancel', {})[0], 200)
        self.model_server.release.set()
        detail = wait_for_run(self.app.liquid_kernel, run_id)
        self.assertEqual(detail['status'], 'cancelled')
        self.assertIsNone(self.app.liquid_kernel.registry.active_state()['canary'])
        self.assertFalse(self.app.liquid_kernel.run_lock.locked())

    def test_catalog_auth_ownership_dedup_and_no_remote_probes(self):
        self.app.global_profiles['duplicate'] = dict(self.app.global_profiles['gen'])
        self.app.global_profiles['different'] = {**self.app.global_profiles['gen'], 'headers': {'X-Tenant': 'other-credential'}}
        owner = cc.user_id_from_ip('127.0.0.1')
        self.app.crypto.write_json(self.app.codes_root / owner / 'user_prefs.json', {'model_profiles': {'mine': self.app.global_profiles['gen']}})
        self.assertEqual(self.request('/models', auth=False)[0], 401)
        with mock.patch.object(cc, '_fetch_provider_models_cached', side_effect=AssertionError('no probes')):
            status, data = self.request('/models')
        self.assertEqual(status, 200)
        self.assertFalse(next(s for s in data['sources'] if s['source'] == 'ide')['available'])
        selected = [o for o in data['options'] if o['model'] == 'selected-model']
        self.assertEqual(len(selected), 4)  # global gen+duplicate, judge, different; Agent mine
        self.assertEqual(len(next(o for o in selected if o['ref']['profile_id'] == 'gen')['aliases']), 2)
        self.assertNotIn('secret-generator', json.dumps(data))
        self.assertNotIn('other-credential', json.dumps(data))
        cfg = self.app.liquid_kernel.config()
        for ref in ({'source': 'ide', 'owner': owner, 'profile_id': 'mine', 'model': 'selected-model'},
                    {'source': 'agent', 'owner': 'other-user', 'profile_id': 'mine', 'model': 'selected-model'}):
            status, out = self.request('/config', {'revision': cfg['revision'], 'values': {'generator_model_ref': ref}})
            self.assertEqual(status, 403, out)

    def test_ide_private_model_survives_logout_and_restart_but_not_disabled_owner(self):
        account = self.app.ide_auth.create_user('evolution-owner', 'ValidPassword-4738!', must_change_password=False)
        owner = account['user_id']
        session = self.app.ide_auth.login('evolution-owner', 'ValidPassword-4738!', '127.0.0.1')
        path = self.app.codes_root / owner / 'user_prefs.json'
        self.app.crypto.write_json(path, {'model_profiles': {'private': self.app.global_profiles['gen']}})
        ref = {'source': 'ide', 'owner': owner, 'profile_id': 'private', 'model': 'selected-model'}
        cfg = self.save(generator=ref, cookie=session['access_token'])
        self.app.ide_auth.revoke_session(session['access_token'])
        attach_plane(self.app, self.root / 'evolution')
        self.model_server.mode = 'no_change'
        detail = wait_for_run(self.app.liquid_kernel, self.start(cfg))
        self.assertEqual(detail['status'], 'no_change')
        self.assertEqual(detail['config']['generator_model_ref']['owner'], owner)
        self.app.ide_auth.set_disabled('evolution-owner', True)
        status, out = self.request('/runs', {'revision': cfg['revision']})
        self.assertEqual((status, out['code']), (409, 'model_owner_disabled'))
        # Emergency Off remains possible with invalidated model references.
        self.assertEqual(self.request('/emergency-off', {})[0], 200)

    def test_revision_legacy_missing_model_and_configuration_changes(self):
        cfg = self.save()
        self.assertEqual(self.request('/runs', {})[1]['code'], 'config_revision_required')
        self.assertEqual(self.request('/runs', {'revision': cfg['revision'] - 1})[1]['code'], 'config_conflict')
        self.assertEqual(self.request('/config', {'revision': cfg['revision'] - 1, 'values': cfg})[1]['code'], 'config_conflict')
        self.app.global_profiles['gen']['api_key'] = 'changed-key'
        self.assertEqual(self.request('/runs', {'revision': cfg['revision']})[1]['code'], 'model_config_changed')
        self.assertFalse(self.app.liquid_kernel.run_lock.locked())
        self.app.global_profiles['gen']['api_key'] = 'secret-generator'
        del self.app.global_profiles['gen']
        self.assertEqual(self.request('/runs', {'revision': cfg['revision']})[1]['code'], 'model_profile_missing')
        with self.assertRaises(LiquidKernelError):
            self.app._liquid_kernel_profile('nonexistent-id')

    def test_background_triggers_fail_closed_and_report_reason(self):
        cfg = self.save()
        plane = self.app.liquid_kernel
        self.app.global_profiles['gen']['models'] = ['wrong-default']
        for trigger in ('manual', 'schedule', 'metric'):
            with self.assertRaises(LiquidKernelError) as caught:
                plane.trigger(trigger)
            self.assertEqual(caught.exception.code, 'model_missing')
            self.assertFalse(plane.run_lock.locked())
        with mock.patch.object(plane, '_schedule_due', return_value=True), mock.patch.object(plane._stop, 'wait', side_effect=[False, True]):
            plane._scheduler_loop()
        self.assertEqual(plane.dashboard()['last_trigger_error']['code'], 'model_missing')
        self.assertEqual(plane.dashboard()['last_trigger_error']['trigger'], 'schedule')
        cfg = plane.config()
        plane.save_config({**cfg, 'mode': 'Off'}, cfg['revision'])
        self.assertEqual(plane.config()['mode'], 'Off')

    def test_private_deleted_configuration_and_legacy_ref_are_strict(self):
        owner = cc.user_id_from_ip('127.0.0.1')
        path = self.app.codes_root / owner / 'user_prefs.json'
        self.app.crypto.write_json(path, {'model_profiles': {'mine': self.app.global_profiles['gen']}})
        ref = {'source': 'agent', 'owner': owner, 'profile_id': 'mine', 'model': 'selected-model'}
        cfg = self.save(generator=ref)
        path.unlink()
        self.assertEqual(self.request('/runs', {'revision': cfg['revision']})[1]['code'], 'model_profile_missing')
        status, out = self.request('/config', {'revision': cfg['revision'], 'values': {'generator_profile': 'missing'}})
        self.assertEqual((status, out['code']), (409, 'model_profile_missing'))
        status, out = self.request('/config', {'revision': cfg['revision'], 'values': {'generator_profile': 'gen::selected-model'}})
        self.assertEqual(status, 200)
        self.assertIsNone(out['config']['generator_model_ref'])
        resolved = self.request('/models')[1]['resolved']['generator']
        self.assertTrue(resolved['available'])
        self.assertEqual(resolved['ref']['model'], 'selected-model')
        cfg = out['config']
        status, out = self.request('/config', {'revision': cfg['revision'], 'values': {'generator_model_ref': {**ref, 'api_key': 'never-copy'}}})
        self.assertEqual((status, out['code']), (400, 'invalid_model_ref'))
        self.assertNotIn('never-copy', self.app.liquid_kernel.config_path.read_text())

    def test_custom_template_cannot_override_selected_model_or_token_limit(self):
        self.app.global_profiles['gen'].update(provider='custom_http', endpoint=self.model_url + '/custom',
            payload_template='{"model":"wrong-literal","max_tokens":99999,"messages":${messages_json}}')
        cfg = self.save()
        self.model_server.mode = 'no_change'
        detail = wait_for_run(self.app.liquid_kernel, self.start(cfg))
        self.assertEqual(detail['status'], 'no_change', detail)
        call = self.model_server.calls[0]
        self.assertEqual(call['body']['model'], 'selected-model')
        self.assertEqual(call['body']['max_tokens'], cfg['task_benchmark']['turn_max_tokens'])


class EvolutionLifecycleTests(unittest.TestCase):
    def test_creation_thread_and_worker_failures_release_lock_and_restart_recovers(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plane = LiquidKernelControlPlane(root, model_callback=improving_model, judge_callback=improving_judge)
            plane.apply_startup_config('Thinking', 'off')
            for target, error in (('create_run', sqlite3.OperationalError('db failed')), ('_event', sqlite3.OperationalError('audit failed'))):
                with mock.patch.object(plane.registry, target, side_effect=error):
                    with self.assertRaises(LiquidKernelError):
                        plane.trigger()
                self.assertFalse(plane.run_lock.locked())
                self.assertEqual(plane.registry.list_runs()['total'], 0)
            with mock.patch('liquid_kernel.control.threading.Thread.start', side_effect=RuntimeError('no thread')):
                with self.assertRaises(LiquidKernelError):
                    plane.trigger()
            self.assertFalse(plane.run_lock.locked())
            self.assertEqual(plane.registry.list_runs()['runs'][0]['status'], 'failed')
            run_id = plane.registry.create_run(plane.config(), 'manual')
            recovered = LiquidKernelControlPlane(root, model_callback=improving_model, judge_callback=improving_judge)
            self.assertEqual(recovered.registry.run_detail(run_id)['status'], 'failed')
            detail = wait_for_run(recovered, recovered.trigger()['run_id'])
            self.assertEqual(detail['status'], 'awaiting_approval')
            self.assertFalse(recovered.run_lock.locked())

    def test_missing_judge_and_invalid_scores_never_become_neutral(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=improving_model)
            plane.apply_startup_config('Thinking', 'off')
            with self.assertRaises(LiquidKernelError):
                plane.trigger()
            self.assertFalse(plane.run_lock.locked())
        for invalid in (None, True, float('nan'), float('inf'), -1, 101, '50'):
            with self.assertRaises(LiquidKernelError):
                valid_judge_score(invalid)
        self.assertEqual(valid_judge_score(0), 0)

    def test_embedded_restore_import_and_upgrade_preserve_runtime(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / 'liquid_kernel'
            package.mkdir()
            (package / 'control.py').write_text('def inject_embedded_kernel(): pass\n')
            (package / '__init__.py').write_text('')
            preserved = {'config.json': b'{"revision":12}', '.artifact_signing_key': b'signing-history', 'registry.sqlite': b'existing-records'}
            for name, content in preserved.items():
                (package / name).write_bytes(content)
            status = cc._ensure_embedded_liquid_kernel_package(package)
            self.assertEqual(status['model_capability_version'], 19)
            self.assertTrue((Path(status['backup_root']) / 'control.py').is_file())
            for name, content in preserved.items():
                self.assertEqual((package / name).read_bytes(), content)
            spec = importlib.util.spec_from_file_location('restored_liquid_kernel', package / '__init__.py', submodule_search_locations=[str(package)])
            module = importlib.util.module_from_spec(spec)
            import sys
            sys.modules[spec.name] = module
            try:
                spec.loader.exec_module(module)
                plane = module.LiquidKernelControlPlane(Path(temp) / 'fresh-runtime', model_callback=improving_model, judge_callback=improving_judge)
                plane.save_config({'task_benchmark': {'enabled': False}}, plane.config()['revision'])
                plane.apply_startup_config('Thinking', 'off')
                detail = wait_for_run(plane, plane.trigger()['run_id'])
                self.assertEqual(detail['status'], 'failed')
                self.assertEqual(detail['result']['code'], 'insufficient_session_tasks')
                self.assertTrue(plane.config()['task_benchmark']['enabled'])
            finally:
                for name in list(sys.modules):
                    if name.startswith('restored_liquid_kernel'):
                        del sys.modules[name]
            archive = zipfile.ZipFile(io.BytesIO(base64.b64decode(cc._EMBEDDED_LIQUID_KERNEL_PACKAGE_B64)))
            for name in ('control.py', 'models.py', '__init__.py'):
                self.assertEqual(archive.read(name), (Path(__file__).resolve().parents[1] / 'liquid_kernel' / name).read_bytes())


if __name__ == '__main__':
    unittest.main()
