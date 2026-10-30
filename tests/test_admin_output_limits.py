"""Admin controls output ceilings; task definitions have 30 bounded attempts."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError, normalize_evolution_config
from liquid_kernel.agentic import TASK_DEFINITION_ATTEMPTS, build_task_bank, task_config
from test_agentic_evolution import TaskModel, experiences


class AdminOutputLimitsTests(unittest.TestCase):
    def app(self, limit=98304):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = LiquidKernelControlPlane(Path(directory.name), task_runtime_limits=lambda: {'max_rounds': 200, 'max_output_tokens': limit})
        app._liquid_kernel_profile = lambda _: {'provider': 'ollama', 'model': 'test', 'base_url': 'http://localhost:11434'}
        return app

    def test_normalization_runtime_and_save_preserve_large_admin_output_limits(self):
        for limit in [32768, 65536, 98304, 131072]:
            with self.subTest(limit=limit):
                self.assertEqual(task_config('Tuning', {'turn_max_tokens': limit})['turn_max_tokens'], limit)
                plane = self.app(limit).liquid_kernel
                self.assertEqual(plane.config()['task_benchmark']['turn_max_tokens'], limit)
                saved = plane.save_config({'mode': 'Tuning'}, plane.config()['revision'])['config']
                self.assertEqual(saved['task_benchmark']['turn_max_tokens'], limit)

    def test_transport_sends_exact_admin_limit_above_32000_and_never_exceeds_it(self):
        app = self.app(98304)
        for requested, expected in [(98304, 98304), (131072, 98304), (65536, 65536), (0, 98304)]:
            with self.subTest(requested=requested), mock.patch.object(cc.OllamaClient, 'chat', return_value={'content': '{"ok":true}'}) as chat:
                self.assertTrue(app._liquid_kernel_transport_call('Return JSON.', '{}', '', requested)['ok'])
                self.assertEqual(chat.call_args.kwargs['max_tokens'], expected)

    def test_reasoning_continuation_uses_admin_ceiling_without_32000_cap(self):
        app = self.app(98304)
        replies = [{'thinking': 'Derive the result.', 'content': '', 'raw': {'done_reason': 'length'}}, {'content': '{"ok":true}'}]
        with mock.patch.object(cc.OllamaClient, 'chat', side_effect=replies) as chat:
            result = app._liquid_kernel_transport_call('JSON.', '{}', '', 40000)
        self.assertTrue(result['ok'])
        self.assertEqual([call.kwargs['max_tokens'] for call in chat.call_args_list], [40000, 80000])

    def test_independent_review_uses_admin_limit_and_explicit_quota_still_applies(self):
        app = self.app(65536)
        plane = app.liquid_kernel
        cfg = plane.config()
        seen = []
        def judge(payload, profile, tokens):
            seen.append(tokens)
            return {'incumbent': 90, 'candidate': 91}
        plane.judge_callback = judge
        plane._soft_score('def a(): pass', 'def a(): pass', [], cfg)
        self.assertEqual(seen, [65536])
        plane._tokens_used = 0
        plane._token_limit = 20000
        plane._soft_score('def a(): pass', 'def a(): pass', [], cfg)
        self.assertLessEqual(seen[-1], 20000)

    def bank(self, model, progress=None):
        cfg = normalize_evolution_config({'mode': 'Tuning'})
        return build_task_bank(experiences(2), cfg, model, 42, progress=progress)

    def test_task_definition_audit_can_repair_beyond_old_fifth_attempt(self):
        base = TaskModel()
        events = []
        audits = 0
        def model(system, packet):
            nonlocal audits
            if packet.get('task', '').startswith('Audit task and acceptance'):
                audits += 1
                return {'valid': audits >= 6, 'issues': ['Fix explicit filenames'] if audits < 6 else []}
            return base(system, packet)
        bank = self.bank(model, lambda kind, payload: events.append((kind, copy.deepcopy(payload))))
        self.assertEqual(len(bank['tasks']), 2)
        completed = [payload for kind, payload in events if kind == 'task_design_completed']
        self.assertEqual(completed[0]['attempt'], 6)
        self.assertTrue(all(payload['max_attempts'] == 30 for _, payload in events))

    def test_persistent_definition_failure_stops_at_exactly_30_without_freezing_invalid_task(self):
        base = TaskModel()
        audits = 0
        def model(system, packet):
            nonlocal audits
            if packet.get('task', '').startswith('Audit task and acceptance'):
                audits += 1
                return {'valid': False, 'issues': ['Contradictory assertions']}
            return base(system, packet)
        with self.assertRaises(ValueError):
            self.bank(model)
        self.assertEqual(TASK_DEFINITION_ATTEMPTS, 30)
        self.assertEqual(audits, 30)

    def test_unusable_initial_definition_can_regenerate_from_original_source(self):
        base = TaskModel()
        failed = False
        recovered_source = False
        def model(system, packet):
            nonlocal failed, recovered_source
            if not failed:
                failed = True
                raise LiquidKernelError('invalid_model_output', 'Observed malformed definition', 422)
            if packet.get('operation') == 'repair_task_definition':
                recovered_source = bool(packet.get('source', {}).get('user_turns'))
            return base(system, packet)
        bank = self.bank(model)
        self.assertTrue(recovered_source)
        self.assertEqual(len(bank['tasks']), 2)

    def test_definition_repair_does_not_swallow_cancellation_auth_or_global_budget(self):
        for code in ['run_cancelled', 'model_call_failed', 'run_budget_exhausted']:
            with self.subTest(code=code), self.assertRaises(LiquidKernelError) as caught:
                self.bank(lambda *_: (_ for _ in ()).throw(LiquidKernelError(code, code)))
            self.assertEqual(caught.exception.code, code)


if __name__ == '__main__':
    unittest.main()
