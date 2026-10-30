"""A rejected experiment is a retained code version, never a baseline alias."""
import tempfile
import unittest
from pathlib import Path
from liquid_kernel import LiquidKernelControlPlane, LiquidKernelError
from liquid_kernel.agentic import KernelWorker
from liquid_kernel.control import LiquidKernelRegistry
from test_agentic_evolution import TaskModel, experiences, judge, wait


class CandidateRetentionTests(unittest.TestCase):
    def plane(self, model=None, reviewer=judge):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        plane = LiquidKernelControlPlane(Path(temp.name), model_callback=model or TaskModel(reject=True),
                                         judge_callback=reviewer, experience_provider=lambda *_: experiences(2))
        cfg = plane.apply_startup_config('Tuning', 'off')['config']
        plane.save_config({'deployment_policy': 'manual', 'budget': {**cfg['budget'], 'candidate_limit': 1}}, cfg['revision'])
        return plane

    def test_no_change_constructs_and_measures_distinct_experiment_even_when_it_loses(self):
        plane = self.plane()
        baseline = plane.registry.active_version()
        detail = wait(plane, plane.trigger()['run_id'], timeout=25)
        self.assertEqual(detail['status'], 'rejected', detail)
        version = detail['candidate_version']
        self.assertTrue(version); self.assertNotEqual(version, baseline)
        saved = plane.registry.version_detail(version)
        self.assertNotEqual(saved['source_hash'], plane.registry.version_detail(baseline)['source_hash'])
        self.assertIn('def before_round', saved['source'])
        self.assertTrue(saved['evaluation']['candidate']['task_execution_measured'])
        self.assertFalse(saved['evaluation']['deployment_eligible'])
        self.assertEqual(saved['status'], 'rejected')
        self.assertIn('recent_tool_exchanges', plane.registry.diff(version)['diff'])
        reopened = LiquidKernelRegistry(plane.registry.root)
        self.assertEqual(reopened.version_detail(version)['evaluation'], saved['evaluation'])
        self.assertEqual(reopened.diff(version), plane.registry.diff(version))
        self.assertEqual(detail['result']['evaluations'][0]['candidate_version'], version)
        self.assertNotIn('same_version', detail['score_summary']['candidate'])
        self.assertEqual(plane.registry.active_version(), baseline)
        for action in [lambda: plane.registry.begin_canary(version, 100), lambda: plane.registry.promote(version),
                       lambda: plane.registry.rollback(version), lambda: plane.approve(detail['run_id'])]:
            with self.assertRaises(LiquidKernelError): action()
        self.assertEqual(plane.registry.active_version(), baseline)

    def test_successful_candidate_keeps_same_registered_id_through_confirmation_and_approval(self):
        plane = self.plane(TaskModel())
        detail = wait(plane, plane.trigger()['run_id'], timeout=25)
        self.assertEqual(detail['status'], 'awaiting_approval', detail)
        retained = plane.registry.list_versions()['versions']
        self.assertEqual(len(retained), 2)
        self.assertTrue(plane.registry.version_detail(detail['candidate_version'])['evaluation']['deployment_eligible'])
        self.assertEqual(detail['candidate_version'], detail['result']['evaluations'][0]['candidate_version'])
        self.assertTrue(detail['result']['confirmation']['passed'])
        plane.approve(detail['run_id'])
        self.assertEqual(plane.registry.active_state()['canary']['version'], detail['candidate_version'])

    def test_multiple_rejected_candidates_all_keep_own_code_and_scores(self):
        plane = self.plane(); cfg = plane.config()
        plane.save_config({'mode': 'Thinking', 'budget': {**cfg['budget'], 'candidate_limit': 2}}, cfg['revision'])
        detail = wait(plane, plane.trigger()['run_id'], timeout=25)
        versions = [row['candidate_version'] for row in detail['result']['evaluations']]
        self.assertEqual(len(set(versions)), 2)
        self.assertEqual(len(plane.registry.list_versions()['versions']), 3)
        for version in versions:
            self.assertTrue(plane.registry.version_detail(version)['evaluation']['candidate']['task_execution_measured'])

    def test_review_failure_preserves_registered_source_and_hard_score(self):
        reviews = 0
        def reviewer(payload, *args):
            nonlocal reviews
            reviews += 1
            if reviews > 1: raise LiquidKernelError('model_call_failed', 'review service down', 502)
            return judge(payload, *args)
        plane = self.plane(TaskModel(), reviewer)
        detail = wait(plane, plane.trigger()['run_id'], timeout=25)
        self.assertEqual(detail['status'], 'failed')
        version = detail['candidate_version']; self.assertTrue(version)
        saved = plane.registry.version_detail(version)
        self.assertEqual(saved['evaluation']['candidate']['hard'], 100)
        self.assertIsNone(saved['evaluation']['candidate'].get('soft'))
        self.assertFalse(saved['evaluation']['deployment_eligible'])
        with self.assertRaises(LiquidKernelError): plane.registry.begin_canary(version)

    def test_invalid_model_patch_after_repairs_falls_back_to_valid_measured_experiment(self):
        base = TaskModel()
        def broken(system, prompt, *args):
            import json
            payload = json.loads(prompt)
            if payload.get('task', '').startswith('Improve the executable'):
                return {'decision': 'change', 'reason': 'Unproven mechanism', 'patch': {'files': [
                    {'path': 'kernel.py', 'operation': 'replace_file', 'content': 'not valid python!'}]}}
            return base(system, payload, *args)
        plane = self.plane(broken)
        detail = wait(plane, plane.trigger()['run_id'], timeout=25)
        self.assertTrue(detail['candidate_version'], detail)
        self.assertEqual(detail['proposal']['candidates'][0]['origin'], 'architecture_exploration')
        self.assertTrue(detail['score_summary']['candidate']['task_execution_measured'])
        self.assertGreaterEqual(len(detail['result']['evaluations'][0]['patch']['validation_repairs']), 3)

    def test_exploration_wraps_evolved_hooks_without_recursion_or_replacing_parent(self):
        plane = self.plane(); source = plane.registry.sources(plane.registry.active_version())
        evidence = {'rows': [{'rounds': 34, 'accounted_tokens': 887360}]}
        for index in range(3):
            proposal = plane._exploration_proposal(source, evidence, index)
            source, _ = plane.validator.apply(source, proposal, plane.config())
            worker = KernelWorker(source)
            try:
                normal = worker.call('before_round', {'context': {'recent_results': []}}, lambda: None)
                failure = worker.call('before_round', {'context': {'recent_results': [{'ok': False}]}}, lambda: None)
                self.assertGreater(failure['recent_tool_exchanges'], normal['recent_tool_exchanges'])
            finally: worker.close()
