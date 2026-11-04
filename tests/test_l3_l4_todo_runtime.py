"""Canonical Todo visibility and Plan-level invariants for L3/L4 sessions."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class CollaborativeTodoRuntimeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="l3-l4-todos-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.session = cc.SessionState(
            "todos", "Todos", root / "sessions", "http://127.0.0.1:9", "test-model",
            root / "skills", cc.CryptoBox(root / "Codes"), root,
            execution_mode="sync", auto_task_level_ceiling=4, defer_initial_persist=True,
        )
        s = self.session
        s.runtime_execution_mode = "sync"
        s.runtime_task_level = 4
        s.runtime_task_type = "engineering"
        s.runtime_task_complexity = "complex"
        s.runtime_assigned_expert = "developer"
        s.runtime_participants = ["explorer", "developer", "reviewer"]
        s.active_agent_role = "developer"
        s.runtime_reclassify_required = False
        s.blackboard = s._new_blackboard("Build and verify a public fixture service")
        s.blackboard["task_profile"].update(
            task_level=4, execution_mode="sync", task_type="engineering", complexity="complex",
            assigned_expert="developer", participants=s.runtime_participants,
        )
        s._emit = mock.Mock()
        s._persist = mock.Mock()
        s.ollama.chat = mock.Mock(return_value={"content": "{}"})

    def test_no_plan_sync_never_drops_peer_todos_when_active_role_changes(self):
        s = self.session
        s.todo.update([
            {"content": "Inspect the input contract", "owner": "explorer", "status": "completed"},
            {"content": "Implement the API", "owner": "developer", "status": "in_progress"},
            {"content": "Independently verify API output", "owner": "reviewer", "status": "pending"},
        ])
        original = s.todo.snapshot()
        for role in ("developer", "reviewer", "explorer", "manager"):
            with self.subTest(role=role):
                s.active_agent_role = role
                s._sync_todos_from_blackboard(reason="role-handoff")
                self.assertEqual(s.todo.snapshot(), original)

    def test_no_plan_sync_does_not_create_a_second_program_generated_roadmap(self):
        s = self.session
        s._sync_todos_from_blackboard(reason="startup")
        self.assertEqual(s.blackboard["project_todos"], [])
        self.assertEqual(s.todo.snapshot(), [])

    def test_no_plan_sync_keeps_open_peer_rows_in_the_finish_gate(self):
        s = self.session
        s.todo.update([
            {"content": "Implement the API", "owner": "developer", "status": "completed"},
            {"content": "Independently verify API", "owner": "reviewer", "status": "in_progress"},
        ])
        s._sync_todos_from_blackboard(reason="developer-finished")
        rows = s._completion_scoped_open_todo_rows(s.blackboard)
        self.assertEqual([(r.get("owner"), r["content"]) for r in rows], [("reviewer", "Independently verify API")])

    def test_approved_plan_does_not_downgrade_semantic_l3_l4_by_low_risk(self):
        for level in (3, 4):
            with self.subTest(level=level):
                self.assertEqual(self.session._plan_risk_target_task_level(level, "low", 0), level)

    def test_plan_approval_risk_adjustment_obeys_admin_automatic_ceiling(self):
        self.session.auto_task_level_ceiling = 3
        self.assertEqual(self.session._plan_risk_target_task_level(3, "high", 0), 3)
        self.assertEqual(self.session._plan_risk_target_task_level(4, "low", 0), 3)
        self.assertEqual(self.session._plan_risk_target_task_level(4, "low", 4), 4)

    def test_user_requirement_change_remains_revision_authority_for_future_steps(self):
        s = self.session
        current = {'id':'current','content':'Implement total','category':'plan_step','status':'in_progress'}
        future = {'id':'future','content':'Verify total','category':'plan_step','status':'pending'}
        s.runtime_plan_approved = True
        s.blackboard['plan'] = {'phase':'executing'}
        s.blackboard['project_todos'] = [current,future]
        s._merge_user_feedback_with_plan('Rename total to gross_total in the output and all remaining checks.')
        adjustment = s.blackboard['user_plan_adjustments'][-1]
        later = adjustment['ts'] + 100
        records = s._plan_worker_revision_evidence_candidates(future,board=s.blackboard,since_ts=later)
        self.assertIn(adjustment['id'],[r['id'] for r in records])
        self.assertFalse(s._plan_subtask_has_accumulated_evidence(future,'Verify gross_total',board=s.blackboard,since_ts=later))

    def test_user_requirement_change_cannot_authorize_an_unrelated_new_plan(self):
        s = self.session
        s.blackboard['user_plan_adjustments'] = [{'id':'user:old','step_id':'old-plan-step',
            'kind':'user_input','tool':'user_request','actor':'user','ok':True,'summary':'Old task requirement','ts':1.0}]
        step = {'id':'new-plan-step','content':'A different task','category':'plan_step','status':'in_progress'}
        s.blackboard['project_todos'] = [step]
        records = s._plan_worker_revision_evidence_candidates(step,board=s.blackboard)
        self.assertNotIn('user:old',[r['id'] for r in records])


    def test_todo_json_uses_admin_output_and_retries_incomplete_final_answer(self):
        s = self.session
        s.max_output_tokens = 48000
        s.ollama.chat = mock.Mock(side_effect=[
            {"content": "", "thinking": '{"passed":true}'},
            {"content": '{"passed":false,"reason":"missing proof"}'},
        ])
        result = s._todo_json_response([{"role": "user", "content": "audit evidence"}], max_tokens=360)
        self.assertIn('false', result['content'])
        self.assertEqual([c.kwargs['max_tokens'] for c in s.ollama.chat.call_args_list], [48000, 48000])
        self.assertNotIn('"passed":true', str(s.ollama.chat.call_args.args))

    def seed_plan(self):
        s = self.session
        s.runtime_plan_approved = True
        s.blackboard['plan'] = {'phase': 'executing', 'steps': ['Implement summary']}
        step = {
            'id': 'pt:revision:001', 'key': 'bb:proj:pt:revision:001',
            'content': 'Implement summary', 'full_content': 'Implement summary\nReturn count and total.',
            'category': 'plan_step', 'status': 'in_progress', 'plan_step_index': 0,
            'activated_at': 10.0,
        }
        s.blackboard['project_todos'] = [step]
        s.blackboard['plan_step_total'] = 1
        return step

    def test_parent_body_only_revision_is_saved_with_same_identity(self):
        s = self.session
        step = self.seed_plan()
        result = s._apply_plan_step_updates([{
            'plan_step_index': 0, 'full_content': 'Implement summary\nReturn count and gross_total.'
        }], board=s.blackboard)
        self.assertIn('accepted', result)
        updated = s.blackboard['project_todos'][0]
        self.assertEqual(updated['id'], step['id'])
        self.assertIn('gross_total', updated['full_content'])
        self.assertIn('gross_total', s.blackboard['plan']['steps'][0])

    def test_genuine_live_input_can_justify_revision_but_is_not_completion_evidence(self):
        s = self.session
        step = self.seed_plan()
        with mock.patch.object(s, '_user_feedback_conflict_score', return_value=0.5):
            s._merge_user_feedback_with_plan('Rename total to gross_total and update acceptance.')
        evidence = s._plan_worker_revision_evidence_candidates(step, board=s.blackboard, since_ts=10.0)
        user_record = next(r for r in evidence if r['tool'] == 'user_request')
        self.assertTrue(user_record['id'].startswith('user:'))
        self.assertFalse(any(r['id'] == user_record['id'] for r in s._plan_step_evidence_records(step['id'], board=s.blackboard)))
        before = [{'content': '验收：summary.json contains total', 'status': 'pending'}]
        after = [{'content': '验收：summary.json contains gross_total', 'status': 'pending'}]
        with mock.patch.object(s, '_semantic_audit_plan_worker_revision', return_value={
            'available': True, 'approved': True, 'reason': 'User changed the output contract',
        }) as audit:
            review = s._review_plan_worker_revision(step, before, after, update_mode='revise_open',
                revision_reason='Apply the authenticated user field rename', revision_evidence=[user_record['id']],
                actor='developer', board=s.blackboard)
        self.assertTrue(review['ok'])
        audit.assert_called_once()
        self.assertNotEqual(audit.call_args.kwargs['before_open'], audit.call_args.kwargs['after_open'])

    def test_todo_operations_persist_as_control_evidence_outside_product_ledger(self):
        s = self.session
        step = self.seed_plan()
        s.todo.update([{'content': '1.1 Read and update Todo', 'status': 'in_progress',
                        'owner': 'developer', 'parent_step_id': step['id']}])
        record = s._record_plan_step_tool_evidence('developer', {
            'name': 'TodoWrite', 'args': {}, 'output': 'Canonical list updated', 'ok': True,
        }, board=s.blackboard)
        self.assertEqual(record['kind'], 'control')
        self.assertIn('unique_ids=True', record['summary'])
        self.assertIn('[in_progress]', record['summary'])
        self.assertEqual(s._plan_step_evidence_records(step['id'], board=s.blackboard), [])
        board = s._ensure_blackboard()
        self.assertEqual(board['plan_control_evidence'][step['id']][0]['id'], record['id'])
        row = s.todo.snapshot()[0]
        _, candidates = s._plan_subtask_semantic_evidence_signature(step, row, board=board)
        self.assertIn(record['id'], [r['id'] for r in candidates])

    def test_status_update_audits_canonical_content_not_ignored_rewording(self):
        s = self.session
        step = self.seed_plan()
        s.todo.update([{'content': '1.1 Read and update Todo', 'status': 'in_progress',
            'owner': 'developer', 'parent_step_id': step['id']}])
        row = s.todo.snapshot()[0]
        with mock.patch.object(s, '_plan_worker_completion_has_evidence', return_value=False) as audit:
            s._merge_plan_worker_todo_items([{'id': row['short_id'], 'content':
                '1.1 Read and update Todo and invent additional obligations',
                'status': 'completed', 'parent_step_id': step['id']}], role='developer')
        self.assertTrue(audit.called)
        self.assertEqual(audit.call_args.args[1]['content'], row['content'])

    def test_available_semantic_review_survives_blackboard_normalization(self):
        s = self.session
        step = self.seed_plan()
        review = {'available': True, 'passed': False, 'evidence_signature': 'unchanged-records',
                  'reason': 'No implementation evidence', 'confidence': 'high'}
        s._record_plan_subtask_semantic_review(step, {'content':'1.1 Implement'}, review,
            subtask_id='pst:revision:row', board=s.blackboard)
        board = s._ensure_blackboard()
        self.assertEqual(board['plan_subtask_semantic_reviews'][step['id']]['pst:revision:row'], review)

    def test_sync_revision_auditor_sees_unchanged_peers_in_actual_commit_graph(self):
        s = self.session
        s.todo.update([
            {'content':'Inspect input', 'owner':'explorer', 'status':'in_progress'},
            {'content':'Implement JSON summary', 'owner':'developer', 'status':'in_progress'},
            {'content':'Verify JSON export', 'owner':'reviewer', 'status':'pending'},
        ])
        before=s.todo.snapshot()
        own=next(row for row in before if row['owner']=='developer')
        with mock.patch.object(s, '_semantic_audit_root_todo_revision', return_value={
            'available':True, 'approved':True, 'reason':'Export is part of the goal',
        }) as audit:
            result=s._dispatch_todo_update({'update_mode':'revise_open',
                'revision_reason':'Cover the explicitly requested export in the existing implementation row',
                'items':[{'id':own['short_id'], 'content':'Implement JSON summary and export', 'status':'in_progress'}]},
                role='developer')
        self.assertIn('accepted', result)
        self.assertEqual({row['owner'] for row in audit.call_args.kwargs['current_rows']},
                         {'explorer','developer','reviewer'})
        self.assertEqual({row['owner'] for row in audit.call_args.kwargs['proposed_rows']},
                         {'explorer','developer','reviewer'})
        after=s.todo.snapshot()
        self.assertEqual(len(after),3)
        self.assertEqual(next(row for row in after if row['owner']=='developer')['short_id'],own['short_id'])
        for role in ('explorer','reviewer'):
            for key in ('short_id','content','status'):
                self.assertEqual(next(row for row in after if row['owner']==role)[key],
                                 next(row for row in before if row['owner']==role)[key])

    def test_script_validation_is_not_cached_as_a_source_file_read(self):
        s = self.session
        (s.files_root/'check.py').write_text('import domain; print(domain.value)', encoding='utf-8')
        (s.files_root/'domain.py').write_text('value = 1', encoding='utf-8')
        self.assertEqual(s._readonly_bash_cache_key('python3 check.py; echo "EXIT=$?"'), '')
        self.assertEqual(s._readonly_bash_cache_key('python3 -c "print(1)"'), '')
        self.assertEqual(s._readonly_bash_cache_key('"C:/Python313/python.exe" check.py'), '')
        (s.files_root/'notes.txt').write_text('cached source', encoding='utf-8')
        self.assertTrue(s._readonly_bash_cache_key('cat notes.txt'))


if __name__ == "__main__":
    unittest.main()
