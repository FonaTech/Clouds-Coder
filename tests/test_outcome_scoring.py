"""A faster real solution must not be zeroed by a generated action-count guess."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.agentic import AgenticBenchmark, compare_agentic_flows, digest
from liquid_kernel.control import BASELINE_KERNEL_FILES


class OutcomeScoringTests(unittest.TestCase):
    def task(self):
        return {'id': 'efficient-real-work', 'split': 'holdout', 'fingerprint': 'frozen',
                'goal': 'Write result.txt then follow the revision.', 'starter_files': {},
                'followups': [{'after_round': 2, 'content': 'Change result.txt to revised.'}],
                'checks': [{'kind': 'file_exists', 'path': 'result.txt'},
                           {'kind': 'equals', 'path': 'result.txt', 'value': 'revised'}], 'minimum_tool_calls': 7}

    def run_task(self, model, task=None, rounds=8):
        return AgenticBenchmark(model, lambda: None).run(BASELINE_KERNEL_FILES, [task or self.task()],
                {'max_rounds': rounds, 'max_tool_calls': 30, 'task_timeout_seconds': 30, 'turn_max_tokens': 16384})

    def test_two_real_file_actions_complete_revision_below_seven_action_estimate(self):
        calls = 0
        def model(*args, **kwargs):
            nonlocal calls
            calls += 1
            return {'tool_calls': [{'name': 'write_file', 'arguments': {'path': 'result.txt', 'content': 'initial' if calls == 1 else 'revised'}}],
                    **({'final': 'Revised and complete.'} if calls == 2 else {})}
        observed = self.run_task(model)
        row = observed['rows'][0]
        self.assertEqual(row['tool_calls'], 2)
        self.assertEqual(row['score'], 100)
        self.assertTrue(row['success'])
        self.assertTrue(row['executed_work'])
        self.assertEqual(row['followups_delivered'], 1)
        self.assertEqual(row['scoring_protocol_version'], 2)
        self.assertEqual(row['minimum_tool_calls_estimate'], 7)
        self.assertTrue(all(check['ok'] for check in row['checks']))

    def test_passing_starter_files_without_real_work_are_not_success(self):
        task = self.task(); task['starter_files'] = {'result.txt': 'revised'}
        observed = self.run_task(lambda *args, **kwargs: {'final': 'I claim it is done.'}, task)
        row = observed['rows'][0]
        self.assertFalse(row['executed_work'])
        self.assertFalse(row['success'])
        self.assertEqual(row['score'], 0)

    def test_unprocessed_followup_cannot_pass_even_if_artifact_matches(self):
        response = {'tool_calls': [{'name': 'write_file', 'arguments': {'path': 'result.txt', 'content': 'revised'}}], 'final': 'Done.'}
        observed = self.run_task(lambda *args, **kwargs: response, rounds=1)
        self.assertFalse(observed['rows'][0]['success'])
        self.assertEqual(observed['rows'][0]['followups_delivered'], 0)
        self.assertEqual(observed['rows'][0]['score'], 0)

    def test_mixed_scoring_protocols_cannot_authorize_deployment(self):
        row = {'task_id': 'one', 'task_fingerprint': 'same', 'split': 'holdout', 'score': 100, 'success': True,
               'checks': [], 'flow_contracts': ['a'], 'rounds': 10, 'error': '', 'scoring_protocol_version': 1}
        base = {'score': 100, 'success_rate': 1, 'rows': [row]}
        candidate = copy.deepcopy(base); candidate['rows'][0].update(scoring_protocol_version=2, flow_contracts=['b'], rounds=3)
        comparison = compare_agentic_flows(base, candidate)
        self.assertFalse(comparison['comparable'])
        self.assertFalse(comparison['eligible'])

    def test_historical_floor_bias_is_flagged_without_rewriting_scores(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            run = plane.registry.create_run(plane.config(), 'test')
            path = plane.registry.experience_root/run/'task_bank.json'; path.parent.mkdir(parents=True)
            task = self.task(); task['fingerprint'] = digest(task)
            path.write_text(json.dumps({'tasks': [task]}), encoding='utf-8')
            result = {'incumbent': {'hard': 100}, 'evaluations': [{'candidate': {'hard': 0}, 'task_results': [
                {'task_id': task['id'], 'score': 0, 'tool_calls': 6, 'error': '',
                 'checks': [{'ok': True}, {'ok': True}]}]}]}
            plane.registry.update_run(run, 'rejected', result_json=result)
            detail = plane.registry.run_detail(run)
            self.assertFalse(detail['score_summary']['evaluation_valid'])
            self.assertEqual(detail['score_summary']['scoring_issue']['code'], 'legacy_tool_count_floor')
            self.assertEqual(detail['result'], result)
            self.assertEqual(plane.registry.run_detail(run)['result'], result)
