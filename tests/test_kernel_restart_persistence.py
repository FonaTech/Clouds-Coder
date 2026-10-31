"""Startup must inherit live policy and preserve durable Canary progress."""
import copy
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.request import ProxyHandler, Request, build_opener

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError
from test_evolution_integration import make_app


def register_canary(plane, percent=5):
    """A signed imported-version fixture; this never deploys a user artifact."""
    incumbent = plane.registry.active_version()
    files = plane.registry.sources(incumbent)
    files['kernel.py'] += '\n# Isolated restart fixture\n'
    candidate = plane.registry.register_candidate(
        'restart-fixture', incumbent, files, mode='Thinking', changelog='Restart fixture', scores={},
    )
    plane.registry.begin_canary(candidate, percent)
    return incumbent, candidate


class KernelRestartPolicyTests(unittest.TestCase):
    def app(self, root):
        app = make_app(root, 'http://127.0.0.1:9')
        app.admin_config_lock = threading.RLock()
        app.admin_config_path = root/'startup_config.json'
        app.admin_active_config = cc._admin_factory_config()
        app.admin_initial_config = cc._admin_factory_config()
        app.liquid_kernel_bootstrap = {}
        app.telemetry = types.SimpleNamespace(boot_id='test-boot')
        app.admin_restart_error_path = root/'restart_error.json'
        return app

    def save_policy(self, app):
        refs = {role+'_model_ref': {
            'source': 'global', 'owner': '', 'profile_id': pid, 'model': 'selected-model',
        } for role, pid in [('generator', 'gen'), ('judge', 'judge')]}
        return app.save_evolution_config({'mode': 'Thinking', 'schedule': 'daily', **refs})['config']

    def reopen(self, app, root):
        app.liquid_kernel = LiquidKernelControlPlane(
            root/'evolution', model_callback=app._liquid_kernel_model_call,
            judge_callback=app._liquid_kernel_judge_call,
            model_resolver=lambda config: app._evolution_models().bind_run(config),
            config_validator=lambda config, **kwargs: app._evolution_models().validate_config(config, **kwargs),
        )
        return app.liquid_kernel

    def test_repeated_same_mode_preserves_custom_schedule_revision_and_bindings(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = self.app(root)
            saved = self.save_policy(app)
            plane = self.reopen(app, root)
            before = plane.config_path.read_bytes()
            app.global_profiles['gen']['api_key'] = 'changed-test-credential'
            result = plane.apply_startup_config('Thinking')
            self.assertFalse(result['changed'])
            self.assertEqual(result['config'], saved)
            self.assertEqual(plane.config_path.read_bytes(), before)
            self.assertEqual(plane.config()['schedule'], 'daily')

    def test_stale_off_defaults_and_changed_binding_do_not_cancel_canary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = self.app(root)
            saved = self.save_policy(app)
            register_canary(app.liquid_kernel, 25)
            state = app.liquid_kernel.registry.active_state()
            before = app.liquid_kernel.config_path.read_bytes()
            app.global_profiles['gen']['api_key'] = 'changed-test-credential'
            plane = self.reopen(app, root)
            # A preserved newer compatible framework may not expose the new
            # diagnostic attribute; the host must still inherit its policy.
            del plane.had_saved_config
            inherited = app.restore_liquid_kernel_startup('Off', 'off')
            self.assertEqual(inherited['config'], saved)
            self.assertFalse(inherited['changed'])
            attempted = app.restore_liquid_kernel_startup('Aggressive', explicit_mode=True)
            self.assertEqual(attempted['warning']['code'], 'model_config_changed')
            self.assertEqual(attempted['config'], saved)
            self.assertEqual(plane.config_path.read_bytes(), before)
            self.assertEqual(plane.registry.active_state(), state)
            with self.assertRaises(LiquidKernelError) as caught:
                plane.trigger()
            self.assertEqual(caught.exception.code, 'model_config_changed')
            self.assertFalse(plane.run_lock.locked())
            self.assertEqual(plane.dashboard()['last_trigger_error']['trigger'], 'startup')
            refreshed = copy.deepcopy(saved)
            for role in ('generator', 'judge'):
                refreshed[role+'_model_ref'].pop('fingerprint', None)
            updated = app.save_evolution_config(refreshed, saved['revision'])['config']
            self.assertIsNone(plane.last_trigger_error)
            self.assertNotEqual(updated['generator_model_ref']['fingerprint'], saved['generator_model_ref']['fingerprint'])
            app._evolution_models().bind_run(updated)
            stopped = app.restore_liquid_kernel_startup('Off', explicit_mode=True)
            self.assertEqual(stopped['config']['mode'], 'Off')
            self.assertIsNone(plane.registry.active_state()['canary'])

    def test_live_policy_updates_restart_mirrors_without_clobbering_other_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = self.app(root)
            payload = {
                'version': 1, 'draft': {**cc._admin_factory_config(), 'port': 8123},
                'defaults': {**cc._admin_factory_config(), 'port': 8124},
            }
            app.admin_config_path.write_text(json.dumps(payload), encoding='utf-8')
            saved = self.save_policy(app)
            mirrored = json.loads(app.admin_config_path.read_text(encoding='utf-8'))
            for name in ('draft', 'defaults'):
                self.assertEqual(mirrored[name]['liquid_kernel_mode'], 'Thinking')
                self.assertEqual(mirrored[name]['evolution_schedule'], 'daily')
                self.assertEqual(mirrored[name]['port'], payload[name]['port'])
            self.assertEqual(app.admin_active_config['liquid_kernel_mode'], 'Thinking')
            self.reopen(app, root)
            app.configure_admin_runtime(cc._admin_factory_config())
            self.assertEqual(app.admin_active_config['liquid_kernel_mode'], saved['mode'])
            self.assertEqual(app.liquid_kernel.config(), saved)

    def test_restart_serialization_does_not_turn_policy_defaults_into_explicit_flags(self):
        config = {**cc._admin_factory_config(), 'liquid_kernel_mode': 'Off', 'evolution_schedule': 'off'}
        argv = cc._admin_config_to_argv(config)
        self.assertNotIn('--liquid-kernel-mode', argv)
        self.assertNotIn('--evolution-schedule', argv)
        defaults = cc._admin_argparse_defaults(config)
        self.assertNotIn('liquid_kernel_mode', defaults)
        self.assertNotIn('evolution_schedule', defaults)

    def test_admin_restart_carries_only_deliberately_changed_policy_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fallback = {**cc._admin_factory_config(), 'liquid_kernel_mode': 'Thinking', 'evolution_schedule': 'daily'}
            for requested, expected in [(fallback, {}), ({**fallback, 'liquid_kernel_mode': 'Off'}, {'liquid_kernel_mode': 'Off'})]:
                with self.subTest(expected=expected):
                    process = types.SimpleNamespace(pid=123456, poll=lambda: None)
                    response = mock.MagicMock()
                    response.__enter__.return_value.read.return_value = json.dumps({
                        'restart_verified': True, 'boot_id': 'new-boot', 'pid': process.pid,
                    }).encode('utf-8')
                    opener = mock.Mock()
                    opener.open.return_value = response
                    with mock.patch.object(cc.subprocess, 'Popen', return_value=process) as launch, mock.patch('urllib.request.build_opener', return_value=opener):
                        self.assertTrue(cc._admin_supervised_restart(
                            requested, fallback, restart_nonce='nonce', restart_from_boot_id='old-boot',
                            error_path=root/'restart.json', timeout_seconds=5,
                        ))
                    environment = launch.call_args.kwargs['env']
                    self.assertEqual(json.loads(environment['CLOUDS_CODER_EVOLUTION_STARTUP_OVERRIDES']), expected)

    def test_canary_metrics_timer_stage_and_promotion_survive_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = self.app(root)
            self.save_policy(app)
            with mock.patch('liquid_kernel.control._now', return_value=1000):
                incumbent, candidate = register_canary(app.liquid_kernel)
            with mock.patch('liquid_kernel.control._now', return_value=1000+25*3600):
                for _ in range(20):
                    app.liquid_kernel.observe_session_result(incumbent, success=True, duration_seconds=1)
                    app.liquid_kernel.observe_session_result(candidate, success=True, duration_seconds=1)
            state = copy.deepcopy(app.liquid_kernel.registry.active_state())
            self.assertEqual(state['canary']['percent'], 25)
            with app.liquid_kernel.registry._connect() as conn:
                metrics = conn.execute('SELECT metrics_json FROM deployments').fetchone()[0]
            plane = self.reopen(app, root)
            app.global_profiles['gen']['api_key'] = 'changed-test-credential'
            app.restore_liquid_kernel_startup('Off', 'off')
            self.assertEqual(plane.registry.active_state(), state)
            with plane.registry._connect() as conn:
                self.assertEqual(conn.execute('SELECT metrics_json FROM deployments').fetchone()[0], metrics)
            with mock.patch('liquid_kernel.control._now', return_value=1000+74*3600):
                for _ in range(30):
                    plane.observe_session_result(incumbent, success=True, duration_seconds=1)
                    plane.observe_session_result(candidate, success=True, duration_seconds=1)
                self.assertEqual(plane.registry.active_state()['canary']['percent'], 100)
                final = plane.observe_session_result(candidate, success=True, duration_seconds=1)
            self.assertEqual(final['action'], 'promoted')
            self.assertEqual(plane.registry.active_version(), candidate)
            self.assertIsNone(plane.registry.active_state()['canary'])

    def test_scheduler_resumes_canary_using_stored_metrics_without_new_tasks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            app = self.app(root)
            self.save_policy(app)
            with mock.patch('liquid_kernel.control._now', return_value=1000):
                incumbent, candidate = register_canary(app.liquid_kernel)
                for _ in range(50):
                    app.liquid_kernel.observe_session_result(incumbent, success=True, duration_seconds=1)
                    app.liquid_kernel.observe_session_result(candidate, success=True, duration_seconds=1)
            self.assertEqual(app.liquid_kernel.registry.active_state()['canary']['percent'], 5)
            with app.liquid_kernel.registry._connect() as conn:
                metrics = conn.execute('SELECT metrics_json FROM deployments').fetchone()[0]
            app.global_profiles['gen']['api_key'] = 'changed-test-credential'
            for now, expected in [(1000+25*3600, 25), (1000+74*3600, 100), (1000+74*3600, None)]:
                with self.subTest(stage=expected):
                    plane = self.reopen(app, root)
                    app.restore_liquid_kernel_startup('Off', 'off')
                    with (
                        mock.patch('liquid_kernel.control._now', return_value=now),
                        mock.patch.object(plane._stop, 'wait', side_effect=[False, True]),
                        mock.patch.object(plane, 'trigger', side_effect=AssertionError('Canary must not request a model')),
                    ):
                        plane._scheduler_loop()
                    self.assertIsNone(plane.last_trigger_error)
                    state = plane.registry.active_state()
                    if expected is None:
                        self.assertIsNone(state['canary'])
                        self.assertEqual(state['version'], candidate)
                    else:
                        self.assertEqual(state['canary']['percent'], expected)
                    with plane.registry._connect() as conn:
                        row = conn.execute('SELECT metrics_json,stage_percent,status FROM deployments').fetchone()
                        self.assertEqual(row[0], metrics)
                        self.assertEqual(row[1], expected or 100)
                        self.assertEqual(row[2], 'canary' if expected else 'promoted')


class KernelRealProcessRestartTests(unittest.TestCase):
    def test_three_real_startups_with_stale_binding_keep_health_policy_and_canary(self):
        with tempfile.TemporaryDirectory(prefix='kernel-restart-中文-') as directory:
            workspace = Path(directory).resolve()
            source = workspace/'Clouds_Coder.py'
            shutil.copy2(Path(cc.__file__), source)
            runtime = workspace/cc.ADMIN_STATE_DIRNAME/'liquid_kernel'
            seed = LiquidKernelControlPlane(runtime)
            ref = {'source': 'global', 'owner': '', 'profile_id': 'ollama', 'model': 'demo-model', 'fingerprint': 'stale-binding'}
            seed.save_config({'mode': 'Thinking', 'schedule': 'off', 'generator_model_ref': ref, 'judge_model_ref': ref})
            register_canary(seed, 25)
            before = seed.config_path.read_bytes()
            active = seed.registry.active_state()
            (workspace/'LLM.config.json').write_text(json.dumps({'provider': 'ollama', 'model': 'demo-model', 'base_url': 'http://127.0.0.1:9'}), encoding='utf-8')
            startup = workspace/cc.ADMIN_STATE_DIRNAME/cc.ADMIN_CONFIG_FILENAME
            startup.write_text(json.dumps({'defaults': {**cc._admin_factory_config(), 'liquid_kernel_mode': 'Off', 'evolution_schedule': 'off'}}), encoding='utf-8')
            opener = build_opener(ProxyHandler({}))
            boot_ids = []
            for index, flags in enumerate([[], ['--liquid-kernel-mode', 'Thinking'], ['--liquid-kernel-mode', 'Aggressive']]):
                with self.subTest(startup=index):
                    with socket.socket() as listener:
                        listener.bind(('127.0.0.1', 0))
                        port = listener.getsockname()[1]
                    config = {**cc._admin_factory_config(), 'host': '127.0.0.1', 'port': port,
                              'skills_ui_enabled': False, 'rag_admin_enabled': False, 'code_admin_enabled': False,
                              'mcp_service_enabled': False, 'collaboration_enabled': False, 'ide_enabled': False,
                              'download_js_lib': 'disabled', 'web_search_enabled': 'disabled',
                              'ollama_base_url': 'http://127.0.0.1:9', 'model': 'demo-model'}
                    env = {**os.environ, 'AGENT_WORKDIR': str(workspace), 'CLOUDS_CODER_HOME': str(workspace/'home'),
                           'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1',
                           'CLOUDS_CODER_RESTART_NONCE': 'restart-test', 'CLOUDS_CODER_RESTART_FROM_BOOT_ID': 'prior-boot'}
                    for key in ['CLOUDS_CODER_SKIP_ADMIN_DEFAULTS', 'CLOUDS_CODER_EVOLUTION_STARTUP_OVERRIDES']:
                        env.pop(key, None)
                    log = workspace/f'boot-{index}.log'
                    with log.open('wb') as output:
                        process = subprocess.Popen([sys.executable, str(source), *cc._admin_config_to_argv(config), *flags],
                                                   cwd=workspace, env=env, stdout=output, stderr=subprocess.STDOUT)
                        try:
                            deadline = time.monotonic()+60
                            health = None
                            while time.monotonic() < deadline and process.poll() is None:
                                try:
                                    with opener.open(f'http://127.0.0.1:{port}/api/health?restart_nonce=restart-test&restart_from=prior-boot', timeout=1) as response:
                                        health = json.loads(response.read())
                                    break
                                except OSError:
                                    time.sleep(0.1)
                            self.assertIsNotNone(health, log.read_text(encoding='utf-8', errors='replace'))
                            self.assertTrue(health['restart_verified'])
                            self.assertEqual(health['pid'], process.pid)
                            boot_ids.append(health['boot_id'])
                            self.assertEqual(seed.config_path.read_bytes(), before)
                            self.assertEqual(seed.registry.active_state(), active)
                            token = (workspace/cc.ADMIN_STATE_DIRNAME/'admin.token').read_text(encoding='utf-8').strip()
                            request = Request(f'http://127.0.0.1:{port}/api/admin/evolution/runs',
                                              data=json.dumps({'revision': seed.config()['revision']}).encode('utf-8'),
                                              headers={'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'})
                            with self.assertRaises(HTTPError) as blocked:
                                opener.open(request, timeout=5)
                            self.assertEqual(blocked.exception.code, 409)
                            self.assertEqual(json.loads(blocked.exception.read())['code'], 'model_config_changed')
                        finally:
                            process.terminate()
                            try:
                                process.wait(timeout=10)
                            except subprocess.TimeoutExpired:
                                process.kill()
                                process.wait(timeout=5)
                    if index == 2:
                        self.assertIn('startup warning', log.read_text(encoding='utf-8'))
            self.assertEqual(len(set(boot_ids)), 3)
