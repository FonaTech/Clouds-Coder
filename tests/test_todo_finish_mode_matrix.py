"""Todo initialization and finish invariants shared by all ordinary modes."""
import unittest
from unittest import mock

import test_l3_l4_todo_runtime as fixtures


class TodoFinishModeMatrixTests(unittest.TestCase):
    @staticmethod
    def preparation():
        return {'goal': 'Implement and verify the supplied service',
                'state': 'The test supplies a known empty workspace and explicit service requirements',
                'skills': 'No specialized skill is required for the supplied service fixture',
                'basis': 'user_context', 'ready': True, 'missing': []}

    def session(self, mode, *, plan=False):
        fixture = fixtures.CollaborativeTodoRuntimeTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        s = fixture.session
        s.runtime_task_level = 3 if mode == 'single' else 4
        s.runtime_execution_mode = mode
        s.execution_mode = mode
        s.runtime_plan_approved = plan
        s.runtime_plan_mode_needed = False
        s.plan_mode_user_preference = 'auto' if plan else 'off'
        s.blackboard['task_profile'].update(task_level=s.runtime_task_level, execution_mode=mode)
        if plan:
            s.blackboard['plan'] = {'phase':'executing','steps':['Implement and verify service']}
            s.blackboard['project_todos'] = [{'id':'step','content':'Implement and verify service',
                'full_content':'Implement and verify service','category':'plan_step','status':'in_progress','plan_step_index':0}]
        return s

    def test_required_no_plan_todo_precedes_mutation_in_single_and_multi(self):
        for mode in ('single', 'sync'):
            with self.subTest(mode=mode):
                s = self.session(mode)
                s.running = True
                self.assertTrue(s._required_no_plan_todo_initialization_needed())
                blocked = s._dispatch_tool('write_file', {'path':'output.txt','content':'result'}, agent_role='developer')
                self.assertIn('todo_initialization_required', blocked)
                self.assertFalse((s.files_root/'output.txt').exists())
                s._dispatch_tool('TodoWrite', {'todos':[{'content':'Implement and verify the service','status':'in_progress'}], 'preparation': self.preparation()}, agent_role='developer')
                identities = [r['short_id'] for r in s.todo.snapshot()]
                self.assertTrue(identities)
                self.assertFalse(s._required_no_plan_todo_initialization_needed())
                s._dispatch_tool('write_file', {'path':'output.txt','content':'result'}, agent_role='developer')
                self.assertEqual((s.files_root/'output.txt').read_text(encoding='utf-8'), 'result')
                self.assertEqual(identities, [r['short_id'] for r in s.todo.snapshot()])

    def test_missing_required_todo_blocks_finish_and_routes_to_real_initialization(self):
        for mode in ('single', 'sync'):
            with self.subTest(mode=mode):
                s = self.session(mode)
                gate = s._evaluate_finish_gate()
                self.assertFalse(gate['ok'])
                self.assertEqual(gate['reason'], 'required-todo-missing')
                self.assertIn('TodoWrite', gate['route']['instruction'])
                self.assertTrue(gate['route']['is_mandatory'])

    def test_multi_worker_initializes_own_tracking_without_replacing_peer_rows(self):
        s = self.session('sync')
        s.running = True
        s.todo.update([{'content':'Inspect input','owner':'explorer','status':'in_progress'}])
        peer_id = s.todo.snapshot()[0]['short_id']
        self.assertFalse(s._required_no_plan_todo_initialization_needed('explorer'))
        self.assertTrue(s._required_no_plan_todo_initialization_needed('developer'))
        self.assertIn('todo_initialization_required',s._dispatch_tool('write_file',{'path':'output.txt','content':'result'},agent_role='developer'))
        s._dispatch_tool('TodoWrite',{'todos':[{'content':'Implement and verify service','status':'in_progress'}], 'preparation': self.preparation()},agent_role='developer')
        self.assertFalse(s._required_no_plan_todo_initialization_needed('developer'))
        self.assertEqual(len(s.todo.snapshot()),2)
        self.assertEqual(next(r for r in s.todo.snapshot() if r['owner']=='explorer')['short_id'],peer_id)

    def test_unapproved_plan_cannot_finish_in_any_planning_phase(self):
        for mode in ('single', 'sync'):
            for phase in ('research', 'synthesis', 'awaiting_choice'):
                with self.subTest(mode=mode, phase=phase):
                    s = self.session(mode)
                    s.blackboard['plan'] = {'phase':phase}
                    with mock.patch.object(s, '_can_auto_finish_from_approval', return_value=(True, 'ok')):
                        gate = s._evaluate_finish_gate()
                    self.assertFalse(gate['ok'])
                    self.assertEqual(gate['reason'], 'plan-approval-pending')

    def test_multi_finish_includes_unowned_legacy_rows(self):
        s = self.session('sync')
        s.todo.update([{'content':'Legacy work still pending','status':'pending'}])
        with mock.patch.object(s, '_can_auto_finish_from_approval', return_value=(True, 'ok')):
            gate = s._evaluate_finish_gate()
        self.assertFalse(gate['ok'])
        self.assertEqual(gate['reason'], 'worker-todo-pending:1')

    def test_no_plan_unfinished_peer_is_routed_to_its_actual_owner(self):
        s = self.session('sync')
        s.todo.update([{'content':'Implementation verified','owner':'developer','status':'completed'},
                       {'content':'Independent review not finished','owner':'reviewer','status':'in_progress'}])
        with mock.patch.object(s, '_can_auto_finish_from_approval', return_value=(True,'ok')):
            gate = s._evaluate_finish_gate()
        self.assertFalse(gate['ok'])
        self.assertEqual(gate['route']['target'],'reviewer')
        self.assertIn(s.todo.snapshot()[1]['short_id'],gate['route']['instruction'])

    def test_completed_plan_parents_do_not_hide_unfinished_current_plan_children(self):
        for mode in ('single', 'sync'):
            with self.subTest(mode=mode):
                s = self.session(mode, plan=True)
                s.blackboard['project_todos'][0]['status'] = 'completed'
                s.todo.update([{'content':'Unfinished verification','parent_step_id':'step',
                               'owner':'reviewer','status':'in_progress'}])
                with mock.patch.object(s, '_can_auto_finish_from_approval', return_value=(True, 'ok')):
                    gate = s._evaluate_finish_gate()
                self.assertFalse(gate['ok'])
                self.assertEqual(gate['reason'], 'worker-todo-pending:1')

    def test_finish_requests_never_finalize_open_work_in_four_modes(self):
        for mode in ('single', 'sync'):
            for plan in (False, True):
                with self.subTest(mode=mode, plan=plan):
                    s = self.session(mode, plan=plan)
                    row = {'content':'Work remains','status':'in_progress','owner':'developer'}
                    if plan:
                        row['parent_step_id'] = 'step'
                    s.todo.update([row])
                    result = s._resolve_finish_request('developer', source='single-tool:finish_task' if mode=='single' else 'multi-agent-finish-tool')
                    self.assertFalse(result['stop'])
                    self.assertNotEqual(s.blackboard['completion']['state'], 'completed')
                    self.assertTrue(any(r['status']!='completed' for r in s.todo.snapshot()))

    def test_real_finalizer_is_idempotent_after_all_work_is_ready_in_four_modes(self):
        for mode in ('single', 'sync'):
            for plan in (False, True):
                with self.subTest(mode=mode, plan=plan):
                    s = self.session(mode, plan=plan)
                    row = {'content':'Verified work','status':'completed','owner':'developer'}
                    if plan:
                        s.blackboard['project_todos'][0]['status'] = 'completed'
                        row['parent_step_id'] = 'step'
                    s.todo.update([row])
                    with mock.patch.object(s, '_manager_feedback_passed_from_blackboard', return_value=True), \
                         mock.patch.object(s, '_auto_summary_on_finish', return_value='Observed validation passed'):
                        first = s._resolve_finish_request('developer', source='finish-tool', summary='Verified delivery')
                        second = s._resolve_finish_request('developer', source='finish-tool', summary='Verified delivery')
                    self.assertTrue(first['stop'])
                    self.assertTrue(first['finalized'])
                    self.assertTrue(second['stop'])
                    self.assertFalse(second['finalized'])
                    self.assertEqual(s.blackboard['completion']['state'], 'completed')
                    self.assertEqual(len([m for m in s.messages if m.get('type')=='completion_summary']), 1)

    def test_l1_simple_question_keeps_direct_finish_and_has_no_todo_bootstrap(self):
        s = self.session('single')
        s.runtime_task_level = 1
        s.runtime_task_type = 'simple_qa'
        s.blackboard['task_profile'].update(task_level=1, task_type='simple_qa')
        self.assertEqual(s._todo_contract_prompt_block(), '')
        self.assertFalse(s._required_no_plan_todo_initialization_needed())
        self.assertTrue(s._evaluate_finish_gate()['ok'])

    def test_unrelated_read_does_not_clear_failed_test_before_finish(self):
        s = self.session('single')
        s.blackboard['execution_logs'] = [
            {'actor':'developer','content':'bash python -m unittest\nFAILED (failures=1)\nexit_code=1','ts':1.0},
            {'actor':'developer','content':'bash ls -la\nreport.py tests\nexit_code=0','ts':2.0},
        ]
        self.assertTrue(s._manager_has_error_log())
        s.blackboard['execution_logs'].append({'actor':'developer',
            'content':'bash python -m unittest\nRan 2 tests\nOK\nexit_code=0','ts':3.0})
        self.assertFalse(s._manager_has_error_log())

    def test_corrected_source_read_can_resolve_its_own_read_error(self):
        s = self.session('single')
        s.blackboard['execution_logs'] = [
            {'actor':'developer','content':'bash cat wrong.txt\nError: No such file\nexit_code=1','ts':1.0},
            {'actor':'developer','content':'bash cat report.py\ncontent observed\nexit_code=0','ts':2.0},
        ]
        self.assertFalse(s._manager_has_error_log())
