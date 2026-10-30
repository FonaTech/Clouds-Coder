"""Success does not close architecture search; improvements still need proof."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError
from liquid_kernel.agentic import training_opportunity_evidence
from test_agentic_evolution import TaskModel, experiences, judge, wait


class OptimizationOpportunityTests(unittest.TestCase):
    def plane(self, model):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        plane = LiquidKernelControlPlane(Path(directory.name), model_callback=model, judge_callback=judge,
                                         experience_provider=lambda *_: experiences(2))
        plane.apply_startup_config('Tuning', 'off')
        return plane

    def test_successful_training_costs_and_repeat_observations_are_measured_without_holdout(self):
        read = {'name': 'read_file', 'ok': True, 'arguments': {'path': 'data.txt'}, 'output': {'content': 'same'}}
        original = {'rows': [{'task_id': 'train', 'split': 'train', 'score': 100, 'success': True,
                             'rounds': 34, 'tool_calls': 34, 'accounted_tokens': 887360, 'failed_tool_calls': 0,
                             'checks': [{'ok': True}], 'trace': [read, copy.deepcopy(read)], 'context': {'compactions': 2}},
                            {'task_id': 'PRIVATE_HOLDOUT', 'split': 'holdout', 'accounted_tokens': 13944548, 'trace': []}]}
        before = copy.deepcopy(original)
        evidence = training_opportunity_evidence(original)
        self.assertEqual(original, before)
        self.assertEqual(len(evidence['rows']), 1)
        row = evidence['rows'][0]
        self.assertEqual((row['rounds'], row['accounted_tokens'], row['identical_read_observations']), (34, 887360, 1))
        self.assertNotIn('PRIVATE_HOLDOUT', json.dumps(evidence))
        self.assertNotIn('cache_hit_ratio', row)

    def test_no_change_is_audited_once_with_training_only_evidence_and_normal_accounting(self):
        base = TaskModel()
        seen = []
        plane = None
        def model(system, prompt, *args):
            payload = json.loads(prompt)
            if payload.get('task', '').startswith('Improve the executable'):
                seen.append((payload, plane._model_budget_label, plane._tokens_used))
                return {'decision': 'no_change', 'reason': 'No supported general mechanism after considering cost and quality.'}
            return base(system, payload, *args)
        plane = self.plane(model)
        detail = wait(plane, plane.trigger()['run_id'])
        self.assertEqual(detail['status'], 'rejected')
        self.assertEqual(len(seen), 2)
        self.assertEqual(seen[1][0]['proposal_phase'], 'opportunity_audit')
        self.assertEqual([scope for _, scope, _ in seen], ['proposal', 'proposal'])
        self.assertGreater(seen[1][2], seen[0][2])
        bank = json.loads((plane.registry.experience_root / detail['run_id'] / 'task_bank.json').read_text())
        heldout = {row['id'] for row in bank['tasks'] if row['split'] == 'holdout'}
        for payload, _, _ in seen:
            self.assertTrue(all(row['split'] == 'train' for row in payload['optimization_evidence']['rows']))
            self.assertTrue(heldout.isdisjoint(row['task_id'] for row in payload['optimization_evidence']['rows']))
            self.assertIn('including successful tasks', payload['task'])
            self.assertNotIn('concrete observed failure', payload['output_schema']['reason'])
        self.assertTrue(detail['candidate_version'])
        self.assertNotIn('same_version', detail['score_summary']['candidate'])
        self.assertEqual(detail['proposal']['candidates'][0]['origin'], 'architecture_exploration')
        self.assertEqual(detail['result']['evaluations'][0]['opportunity_audit']['status'], 'completed')

    def test_opportunity_audit_can_propose_real_code_which_must_run_before_acceptance(self):
        base = TaskModel()
        proposals = 0
        def model(system, prompt, *args):
            nonlocal proposals
            payload = json.loads(prompt)
            if payload.get('task', '').startswith('Improve the executable'):
                proposals += 1
                if proposals == 1:
                    return {'decision': 'no_change', 'reason': 'Initial conservative decision.'}
            return base(system, payload, *args)
        plane = self.plane(model)
        detail = wait(plane, plane.trigger()['run_id'], timeout=20)
        self.assertEqual(proposals, 2)
        evaluation = detail['result']['evaluations'][0]
        self.assertTrue(evaluation['candidate']['task_execution_measured'], detail)
        self.assertEqual(evaluation['opportunity_audit']['final_decision'], 'change')
        self.assertIn('flow_comparison', evaluation)
        self.assertTrue((plane.registry.experience_root / detail['run_id'] / 'candidate_1_rollouts.json').is_file())

    def test_bad_audit_output_retains_valid_initial_no_change_with_explicit_warning(self):
        base = TaskModel()
        count = 0
        def model(system, prompt, *args):
            nonlocal count
            payload = json.loads(prompt)
            if payload.get('task', '').startswith('Improve the executable'):
                count += 1
                if count == 1:
                    return {'decision': 'no_change', 'reason': 'Initial valid no-change decision.'}
                raise LiquidKernelError('invalid_model_output', 'Malformed opportunity audit', 422)
            return base(system, payload, *args)
        plane = self.plane(model)
        detail = wait(plane, plane.trigger()['run_id'])
        self.assertEqual(detail['status'], 'rejected')
        audit = detail['score_summary']['evaluations'][0]['opportunity_audit']
        self.assertEqual(audit, {'status': 'failed', 'code': 'invalid_model_output'})
        self.assertTrue(detail['candidate_version'])
        self.assertTrue(any(row['kind'] == 'opportunity_audit_failed' for row in detail['events']))

    def test_opportunity_audit_cannot_swallow_cancellation_or_transport_failure(self):
        for code, status in [('run_cancelled', 'cancelled'), ('model_call_failed', 'failed')]:
            with self.subTest(code=code):
                base = TaskModel()
                def model(system, prompt, *args):
                    payload = json.loads(prompt)
                    if payload.get('proposal_phase') == 'opportunity_audit':
                        raise LiquidKernelError(code, code)
                    if payload.get('task', '').startswith('Improve the executable'):
                        return {'decision': 'no_change', 'reason': 'Initial decision.'}
                    return base(system, payload, *args)
                plane = self.plane(model)
                detail = wait(plane, plane.trigger()['run_id'])
                self.assertEqual(detail['status'], status)
                self.assertIn('hard', detail['score_summary']['incumbent'])


if __name__ == '__main__':
    unittest.main()
