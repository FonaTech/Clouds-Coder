"""Progress persistence and localization; real model acceptance runs separately."""
import json
import sqlite3
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.control import read_evolution_progress, normalize_evolution_config
from test_agentic_evolution import TaskModel, experiences
from liquid_kernel.agentic import build_task_bank


class EvolutionProgressTests(unittest.TestCase):
    def plane(self, root):
        plane = LiquidKernelControlPlane(root)
        config = plane.config()
        config['task_benchmark']['max_tasks'] = 8
        config['task_benchmark']['max_rounds'] = 200
        run = plane.registry.create_run(config, 'progress_test')
        plane.active_run_id = run
        return plane, run

    def test_latest_round_and_tool_are_persisted_without_growing_event_log(self):
        with tempfile.TemporaryDirectory() as temp:
            plane, run = self.plane(Path(temp))
            registry = plane.registry
            registry.event(run, 'task_design_generating', {'task_index': 8, 'task_total': 8, 'operation': 'task_design', 'attempt': 1})
            registry.event(run, 'task_bank_frozen', {'train': 6, 'holdout': 2})
            registry.event(run, 'task_started', {'task_id': 't2', 'task_index': 2, 'task_total': 8, 'arm': 'candidate_2', 'round_limit': 200})
            for index in range(1, 201):
                registry.event(run, 'task_round_started', {'task_id': 't2', 'round': index, 'tool_calls': index - 1})
                registry.event(run, 'task_tool_started', {'tool_name': 'bash', 'tool_calls': index})
            detail = registry.run_detail(run)
            x = detail['progress']['execution']
            self.assertEqual((x['round'], x['round_limit'], x['tool_calls'], x['task_index']), (200, 200, 200, 2))
            self.assertEqual(x['tool_name'], 'bash')
            self.assertEqual(detail['progress']['design']['completed'], 8)
            self.assertLessEqual(len(detail['progress']['activity']), 40)
            self.assertEqual(detail['events_total'], 4)
            self.assertEqual(read_evolution_progress(Path(temp), run)['progress']['execution'], x)

    def test_heartbeat_is_not_task_progress_and_retry_drops_sensitive_payloads(self):
        with tempfile.TemporaryDirectory() as temp:
            plane, run = self.plane(Path(temp))
            with plane.observe_model_request('local-test', timeout_seconds=180) as request:
                before = plane.registry.run_detail(run)['progress']
                time.sleep(.01)
                plane.registry.event(run, 'model_request_wait', {'request_id': request, 'elapsed_seconds': 10})
                pulse = plane.registry.run_detail(run)['progress']
                self.assertEqual(before['last_activity_at'], pulse['last_activity_at'])
                self.assertGreater(pulse['heartbeat_at'], before['heartbeat_at'])
                plane.note_model_retry(request, {'attempt': 2, 'status': 429, 'delay': 12,
                                                'url': 'private-address', 'reason': 'private-secret'})
                progress = plane.registry.run_detail(run)['progress']
                self.assertEqual(progress['model']['state'], 'retrying')
                self.assertEqual(progress['model']['retry_after_seconds'], 12)
                self.assertNotIn('private-', json.dumps(progress))
            model = plane.registry.run_detail(run)['progress']['model']
            self.assertEqual((model['started'], model['completed'], model['failed']), (1, 1, 0))

    def test_read_only_legacy_diagnostic_does_not_recover_or_cancel_active_run(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plane, run = self.plane(root)
            plane.registry.update_run(run, 'assessing')
            with sqlite3.connect(root/'registry.sqlite') as conn:
                conn.execute('DROP TABLE run_progress')
            archive = root/'experience'/run/'model_calls'/'request'/'full_history.jsonl'
            archive.parent.mkdir(parents=True)
            archive.write_text('private old request text')
            before = {name: (root/name).read_bytes() for name in ('active.json', '.artifact_signing_key')}
            result = read_evolution_progress(root, run)
            self.assertEqual(result['status'], 'assessing')
            self.assertTrue(result['progress']['legacy'])
            self.assertEqual(result['progress']['legacy_archive_count'], 1)
            self.assertNotIn('private old request', json.dumps(result))
            self.assertEqual(before, {name: (root/name).read_bytes() for name in before})
            with sqlite3.connect(root/'registry.sqlite') as conn:
                self.assertIsNone(conn.execute("SELECT name FROM sqlite_master WHERE name='run_progress'").fetchone())

    def test_design_progress_reports_task_and_audit_repair_without_source_text(self):
        with tempfile.TemporaryDirectory() as temp:
            plane, _ = self.plane(Path(temp))
            config = normalize_evolution_config({'mode': 'Thinking'})
            config['task_benchmark']['max_tasks'] = 2
            model = TaskModel()
            progress = []
            bank = build_task_bank(experiences(), config, model, 42, lambda kind, payload: progress.append((kind, payload)))
            self.assertEqual(len(bank['tasks']), 2)
            self.assertEqual([p['task_index'] for kind, p in progress if kind == 'task_design_completed'], [1, 2])
            self.assertEqual([p['task_total'] for kind, p in progress if kind == 'task_design_auditing'], [2, 2])
            self.assertNotIn('用户', json.dumps(progress, ensure_ascii=False))

    def test_no_change_budget_failures_are_explained_as_unevaluated_candidates(self):
        with tempfile.TemporaryDirectory() as temp:
            plane, run = self.plane(Path(temp))
            plane.registry.event(run, 'no_change', {'evaluations': [
                {'candidate_index': i, 'code': 'proposal_budget_exhausted'} for i in range(1, 4)]})
            state = plane.registry.run_detail(run)['progress']
            self.assertEqual(state['summary'], {'code': 'proposal_budget_exhausted', 'affected_candidates': 3})
            plane.registry.update_run(run, 'no_change', result_json={'evaluations': [{'code': 'proposal_budget_exhausted'}]})
            self.assertEqual(read_evolution_progress(Path(temp), run)['progress']['summary']['affected_candidates'], 1)

    def test_run_detail_event_page_is_bounded_and_reports_omitted_events(self):
        with tempfile.TemporaryDirectory() as temp:
            plane, run = self.plane(Path(temp))
            for number in range(7):
                plane.registry.event(run, 'checkpoint', {'attempt': number})
            detail = plane.registry.run_detail(run, event_limit=3)
            self.assertEqual(detail['events_total'], 8)
            self.assertTrue(detail['events_truncated'])
            self.assertEqual([e['payload']['attempt'] for e in detail['events']], [4, 5, 6])


class EvolutionProgressI18nTests(unittest.TestCase):
    def test_every_new_label_has_explicit_four_language_entries(self):
        prefix = cc.ADMIN_JS.split('const ADMIN_TEXT_SOURCE', 1)[0]
        script = "global.sessionStorage={getItem:()=>''};global.document={getElementById:()=>null};\n" + prefix
        script += '\nconsole.log(JSON.stringify(ADMIN_EVOLUTION_I18N_ROWS));'
        rows = json.loads(subprocess.run(['node', '-e', script], check=True, text=True, capture_output=True).stdout)
        self.assertGreaterEqual(len(rows), 90)
        for row in rows:
            self.assertEqual(len(row), 5)
            self.assertTrue(all(str(value).strip() for value in row))
        expected = {'Evaluation progress', 'Task definitions', 'Conversation rounds', 'Socket timeout',
                    '本次迭代总 Token 配额', '输入缓存命中', 'Run token quota (0 = unlimited)',
                    'Plan-step token quota (0 = unlimited)'}
        self.assertTrue(expected <= {row[0] for row in rows})
        self.assertIn('renderEvolutionRunDetail(detail)', cc.ADMIN_JS)
        self.assertIn("A.evolutionRunId=''", cc.ADMIN_JS)


if __name__ == '__main__':
    unittest.main()
