"""Observed truncated native calls must recover without executing partial code."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError
from liquid_kernel.agentic import AgenticBenchmark, TOOLS, rollout_complete
from liquid_kernel.context import validate_native_arguments
from liquid_kernel.control import BASELINE_KERNEL_FILES
from test_agentic_evolution import TaskModel, experiences, judge, wait
import test_single_no_plan_todo_bootstrap as bootstrap


class NativeOutputRecoveryTests(unittest.TestCase):
    def app(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = LiquidKernelControlPlane(Path(temp.name))
        app._liquid_kernel_profile = lambda _: {'provider': 'ollama', 'base_url': 'http://localhost:11434', 'model': 'test'}
        return app

    def packet(self):
        return json.dumps({'messages': [{'role': 'user', 'content': 'Build and verify a report.'}], 'tools': TOOLS})

    def broken(self, name='bash', large=True, finish='length'):
        source = 'command=echo ok' if not large else '{"command":"' + 'x' * 38000
        return {'content': '', 'thinking': 'Inspect then generate the report.', 'raw': {'done_reason': finish},
                'tool_calls': [{'args_error': 'arguments JSON auto-repaired from invalid/truncated input',
                                'raw_arguments': source[:1200], 'raw_arguments_chars': len(source), 'raw_arguments_full': source,
                                'function': {'name': name, 'arguments': {'command': 'partial'}}}]}

    def test_observed_truncated_write_and_shell_calls_return_one_replan_without_execution(self):
        for name in ['write_file', 'bash']:
            with self.subTest(name=name), mock.patch.object(cc.OllamaClient, 'chat', return_value=self.broken(name)) as chat:
                result = self.app()._liquid_kernel_transport_call('Use native tools.', self.packet(), '', 16384)
                self.assertEqual(chat.call_count, 1)
                self.assertEqual(result['tool_calls'], [])
                self.assertTrue(result['continue'])
                self.assertEqual(result['recovery']['reason'], 'native_tool_output_truncated')
                self.assertFalse(result['recovery']['semantic_repair_attempted'])
                self.assertIn('2000', result['recovery']['message'])
                self.assertGreater(result['_evolution_usage']['total_tokens'], 0)

    def test_oversized_bad_shell_arguments_also_replan_when_finish_reason_says_stop(self):
        with mock.patch.object(cc.OllamaClient, 'chat', return_value=self.broken(finish='stop')) as chat:
            result = self.app()._liquid_kernel_transport_call('Use tools.', self.packet(), '', 16384)
        self.assertEqual(chat.call_count, 1)
        self.assertEqual(result['recovery']['reason'], 'oversized_native_tool_arguments')

    def test_small_native_arguments_use_isolated_source_preserving_semantic_repair(self):
        bad = self.broken(large=False, finish='stop')
        replies = [bad, bad, {'content': '{"command":"echo ok"}', 'raw': {'done_reason': 'stop'}}]
        with mock.patch.object(cc.OllamaClient, 'chat', side_effect=copy.deepcopy(replies)) as chat:
            result = self.app()._liquid_kernel_transport_call('Use tools.', self.packet(), '', 4096)
        self.assertEqual(result['tool_calls'], [{'name': 'bash', 'arguments': {'command': 'echo ok'}}])
        self.assertEqual(chat.call_count, 3)
        self.assertIsNone(chat.call_args.kwargs['tools'])
        self.assertEqual(chat.call_args.kwargs['label'], 'evolution_json_semantic_repair')

    def test_semantic_engine_cannot_invent_a_different_command_or_bypass_missing_fields(self):
        bad = self.broken(large=False, finish='stop')
        with mock.patch.object(cc.OllamaClient, 'chat', side_effect=[bad, bad, {'content': '{"command":"invented operation"}', 'raw': {'done_reason': 'stop'}}]):
            result = self.app()._liquid_kernel_transport_call('Use tools.', self.packet(), '', 4096)
        self.assertEqual(result['tool_calls'], [])
        self.assertTrue(result['recovery']['semantic_repair_attempted'])
        with self.assertRaises(ValueError):
            validate_native_arguments({'function': {'name': 'write_file', 'arguments': {'content': 'partial'}}}, TOOLS)

    def test_full_malformed_arguments_are_archived_without_replacing_the_bounded_preview(self):
        raw = '{"command":"' + 'x' * 38000
        call = cc.OllamaClient('http://localhost', 'test')._normalize_tool_calls([{'function': {'name': 'bash', 'arguments': raw}}])[0]
        self.assertEqual(call['raw_arguments_full'], raw)
        self.assertLess(len(call['raw_arguments']), 1300)
        self.assertEqual(call['raw_arguments_chars'], len(raw))

    def test_ordinary_tasks_block_oversized_malformed_shell_recovery_as_well(self):
        session = bootstrap.SingleNoPlanTodoBootstrapTests().bare_session()
        with mock.patch.object(session, '_continue_truncated_assistant_output') as continuation, mock.patch.object(session, '_chat_with_same_model_retry') as chat:
            ok, args, hint = session._recover_tool_args_from_malformed(name='bash', raw_args='x' * 10000, pinned_selection='test')
        self.assertFalse(ok)
        self.assertEqual(args, {})
        self.assertIn('2000', hint)
        continuation.assert_not_called()
        chat.assert_not_called()

    def test_shared_semantic_tool_repair_must_preserve_short_paths_and_commands(self):
        for value in [{'path': 'invented.txt'}, {'command': 'invented command'}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                cc.validate_semantic_json_repair(json.dumps(value), 'path=original.txt; command=echo ok', preserve_all_values=True)

    def task(self):
        return {'id': 'recover', 'split': 'train', 'fingerprint': 'recover', 'goal': 'Write and verify out.txt',
                'starter_files': {}, 'followups': [], 'checks': [{'kind': 'equals', 'path': 'out.txt', 'value': 'complete'}], 'minimum_tool_calls': 1}

    def config(self):
        return {'max_rounds': 4, 'max_tool_calls': 20, 'task_timeout_seconds': 20, 'turn_max_tokens': 4096}

    def test_agent_recovers_in_original_workspace_after_a_model_output_exception(self):
        count = 0
        def model(system, packet, *args, **kwargs):
            nonlocal count
            count += 1
            if count == 1:
                return {'tool_calls': [{'name': 'write_file', 'arguments': {'path': 'out.txt', 'content': 'complete'}}]}
            if count == 2:
                raise LiquidKernelError('invalid_model_output', 'Observed invalid native call', 422, {'attempts': []})
            self.assertIn('NOT executed', str(packet['messages']))
            return {'tool_calls': [{'name': 'read_file', 'arguments': {'path': 'out.txt'}}, {'name': 'finish_task', 'arguments': {}}]}
        result = AgenticBenchmark(model, lambda: None).run(BASELINE_KERNEL_FILES, [self.task()], self.config())
        row = result['rows'][0]
        self.assertTrue(row['success'])
        self.assertEqual(row['model_output_recoveries'], 1)
        self.assertEqual(row['artifacts']['out.txt'], 'complete')

    def test_persistent_bad_output_is_partial_with_actual_artifact_checks_at_admin_ceiling(self):
        count = 0
        def model(*args, **kwargs):
            nonlocal count
            count += 1
            if count == 1:
                return {'tool_calls': [{'name': 'write_file', 'arguments': {'path': 'out.txt', 'content': 'complete'}}]}
            return {'continue': True, 'tool_calls': [], 'recovery': {'reason': 'native_tool_output_truncated', 'message': 'Not executed; split the output.'}}
        result = AgenticBenchmark(model, lambda: None).run(BASELINE_KERNEL_FILES, [self.task()], self.config())
        row = result['rows'][0]
        self.assertEqual(count, 4)
        self.assertTrue(all(c['ok'] for c in row['checks']))
        self.assertEqual(row['score'], 100)
        self.assertEqual(row['stop_reason'], 'round_limit')
        self.assertFalse(row['success'])
        self.assertFalse(rollout_complete(result))

    def test_auth_failure_still_propagates_after_checkpointing_completed_tasks(self):
        snapshots = []
        benchmark = AgenticBenchmark(lambda *_: None, lambda: None, on_checkpoint=lambda arm, result: snapshots.append(result))
        first = {'task_id': 'first', 'split': 'train', 'score': 50, 'success': False, 'rounds': 4, 'tool_calls': 2, 'stop_reason': 'round_limit', 'error': ''}
        with mock.patch.object(benchmark, 'run_task', side_effect=[first, LiquidKernelError('model_call_failed', 'Authentication rejected', 502)]):
            with self.assertRaises(LiquidKernelError):
                benchmark.run(BASELINE_KERNEL_FILES, [self.task(), {**self.task(), 'id': 'second'}], self.config())
        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0]['completed_tasks'], 1)
        self.assertEqual(snapshots[0]['expected_tasks'], 2)
        self.assertFalse(rollout_complete(snapshots[0]))

    def test_control_plane_retains_actual_partial_baseline_score_if_a_later_task_transport_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            starts = 0
            base = TaskModel()
            def model(system, prompt, *args):
                nonlocal starts
                packet = json.loads(prompt)
                if 'messages' in packet and len(packet['messages']) == 1:
                    starts += 1
                    if starts == 2:
                        raise LiquidKernelError('model_call_failed', 'service unavailable', 502)
                return base(system, packet, *args)
            plane = LiquidKernelControlPlane(Path(directory), model_callback=model, judge_callback=judge, experience_provider=lambda *_: experiences(2))
            plane.apply_startup_config('Tuning', 'off')
            detail = wait(plane, plane.trigger()['run_id'], timeout=20)
            self.assertEqual(detail['status'], 'failed')
            baseline = detail['score_summary']['incumbent']
            self.assertIsNotNone(baseline.get('hard'))
            self.assertEqual(baseline['completed_tasks'], 1)
            self.assertEqual(baseline['score_status'], 'partial')
            self.assertNotIn('soft', baseline)
            saved = json.loads((plane.registry.experience_root / detail['run_id'] / 'incumbent_rollouts.json').read_text())
            self.assertEqual(len(saved['rows']), 1)

    def test_old_failed_run_view_recovers_only_measured_artifact_score_without_rewriting_history(self):
        app = self.app()
        plane = app.liquid_kernel
        cfg = plane.config()
        run_id = plane.registry.create_run(cfg, 'manual')
        plane.registry.event(run_id, 'task_completed', {'arm': 'incumbent', 'task_id': 'first', 'score': 98,
                                                     'task_total': 2, 'success': False, 'stop_reason': 'round_limit'})
        plane.registry.update_run(run_id, 'failed', result_json={'code': 'invalid_model_output'})
        detail = plane.registry.run_detail(run_id)
        self.assertEqual(detail['score_summary']['incumbent']['hard'], 98)
        self.assertEqual(detail['score_summary']['incumbent']['score_status'], 'partial')
        self.assertNotIn('soft', detail['score_summary']['incumbent'])
        self.assertEqual(detail['result'], {'code': 'invalid_model_output'})


if __name__ == '__main__':
    unittest.main()
