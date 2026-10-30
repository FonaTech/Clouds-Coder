import inspect
import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class SyncRoutingScopeTests(unittest.TestCase):
    def session(self, *, acceptance=False):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.execution_mode = "sync"
        session.runtime_execution_mode = "sync"
        session.runtime_task_type = "engineering"
        session.runtime_assigned_expert = "developer"
        session.active_agent_role = "developer"
        session.reviewer_debug_mode = False
        session.blackboard = {
            "task_epoch": 100.0,
            "focus": {
                "kind": "plan_step",
                "id": "pt:sync:001",
                "index": 0,
                "total": 1,
                "epoch": 10.0,
                "title": "实现模块",
            },
            "project_todos": [{
                "id": "pt:sync:001",
                "key": "bb:proj:pt:sync:001",
                "category": "plan_step",
                "status": "in_progress",
                "plan_step_index": 0,
                "activated_at": 10.0,
                "content": "1. 实现模块",
                "full_content": "1. 实现模块\n1.1 创建模块文件\n验收：运行检查并记录证据",
            }],
            "plan_step_total": 1,
            "task_profile": {
                "execution_mode": "sync",
                "task_type": "engineering",
                "assigned_expert": "developer",
                "participants": ["explorer", "developer", "reviewer"],
            },
        }
        row = {
            "content": "1.1 创建模块文件" if not acceptance else "验收：运行检查并记录证据",
            "status": "in_progress",
            "owner": "developer" if not acceptance else "reviewer",
            "parent_step_id": "pt:sync:001",
        }
        session.todo.update([row])
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_ensure_blackboard_task_profile", lambda self, board=None: self.blackboard["task_profile"])
        bind(session, "_effective_execution_mode", lambda self: "sync")
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        session.agent_bus_messages = []
        session.messages = []
        return session

    def test_old_or_unscoped_handoff_cannot_cross_plan_step(self):
        session = self.session()
        current = session._current_plan_worker_subtask_snapshot(board=session.blackboard, role="")
        old = {
            "from": "developer",
            "to": "reviewer",
            "plan_step_id": "pt:sync:000",
            "plan_step_epoch": 9.0,
            "plan_subtask_id": current["subtask_id"],
        }
        unscoped = {"from": "developer", "to": "reviewer"}

        self.assertFalse(session._route_scope_matches_current_plan(old, session.blackboard, require_scoped=True))
        self.assertFalse(session._route_scope_matches_current_plan(unscoped, session.blackboard, require_scoped=True))

        session.agent_bus_messages = [old, unscoped]
        self.assertIsNone(session._drain_agentbus_fast_route())
        self.assertTrue(all(row.get("_stale_scope") for row in session.agent_bus_messages))

    def test_current_scoped_handoff_is_deliverable(self):
        session = self.session()
        current = session._current_plan_worker_subtask_snapshot(board=session.blackboard, role="")
        session.agent_bus_messages = [{
            "id": "agentmsg:current",
            "ts": cc.now_ts(),
            "from": "developer",
            "to": "reviewer",
            "intent": "review_request",
            "payload": "Review the current implementation.",
            "task_epoch": 100.0,
            "plan_step_id": "pt:sync:001",
            "plan_step_epoch": 10.0,
            "plan_subtask_id": current["subtask_id"],
        }]

        route = session._drain_agentbus_fast_route()

        self.assertIsNotNone(route)
        self.assertEqual(route["env_id"], "agentmsg:current")
        self.assertEqual(route["to"], "reviewer")

    def test_manager_role_choice_is_not_overridden_by_keyword_phase_guess(self):
        session = self.session()
        route = session._enforce_sync_plan_route(
            {"target": "reviewer", "instruction": "Review now."},
            session.blackboard,
        )

        self.assertEqual(route["target"], "reviewer")
        self.assertNotIn("sync-phase-guard", route.get("reason", ""))

    def test_acceptance_does_not_force_a_role_without_explicit_owner(self):
        session = self.session(acceptance=True)
        route = session._enforce_sync_plan_route(
            {"target": "developer", "instruction": "Continue implementation."},
            session.blackboard,
        )

        self.assertEqual(route["target"], "developer")

    def test_scoped_route_requires_matching_task_epoch(self):
        session = self.session()
        current = session._current_plan_worker_subtask_snapshot(board=session.blackboard, role="")
        route = {
            "from": "developer",
            "to": "reviewer",
            "task_epoch": 0.0,
            "plan_step_id": "pt:sync:001",
            "plan_step_epoch": 10.0,
            "plan_subtask_id": current["subtask_id"],
        }
        self.assertFalse(session._route_scope_matches_current_plan(
            route, session.blackboard, require_scoped=True
        ))

    def test_sync_budget_clock_updates_cycles_and_remaining(self):
        session = self.session()
        session.max_agent_rounds = 10
        session.blackboard["task_profile"]["round_budget"] = 6
        session.blackboard["manager_judgement"] = {
            "progress": "in_progress",
            "remaining_rounds": 6,
        }

        session._sync_tick_manager_cycle(session.blackboard, 3)

        self.assertEqual(session.blackboard["manager_cycles"], 3)
        self.assertEqual(session.blackboard["manager_judgement"]["remaining_rounds"], 3)

    def test_sync_budget_clock_keeps_unlimited_as_negative_one(self):
        session = self.session()
        session.max_agent_rounds = 10
        session.blackboard["task_profile"]["round_budget"] = 0
        session.blackboard["manager_judgement"] = {
            "progress": "in_progress",
            "remaining_rounds": 4,
        }

        session._sync_tick_manager_cycle(session.blackboard, 7)

        self.assertEqual(session.blackboard["manager_cycles"], 7)
        self.assertEqual(session.blackboard["manager_judgement"]["remaining_rounds"], -1)

    def test_recovery_reuses_scoped_manager_decision_without_artifact_classification(self):
        session = self.session(acceptance=True)
        session.blackboard.update({
            "status": "CODING",
            "research_notes": [{"content": "earlier research"}],
            "code_artifacts": {"old_step.py": {"content": "pass"}},
            "review_feedback": [],
            "approval": {"approved": False},
            "manager_cycles": 3,
            "manager_summary_attempts": 0,
        })
        session.manager_routes = [{
            "target": "developer",
            "instruction": "Continue the scoped implementation decision.",
            "source": "tool",
            "task_epoch": 100.0,
            "plan_step_id": "pt:sync:001",
        }]
        bind(session, "_latest_user_message_ts", lambda self: 0.0)
        bind(session, "_manager_progress_state", lambda self, board=None: "in_progress")
        bind(session, "_evaluate_finish_gate", lambda self, *args, **kwargs: {"ok": False, "reason": "not-approved"})
        bind(session, "_route_scope_matches_current_plan", lambda self, *args, **kwargs: True)

        route = session._manager_fallback_route()

        self.assertEqual(route["target"], "developer")
        self.assertEqual(route["reason"], "continuity-recovery-last-manager-decision:tool")
        self.assertTrue(route["fallback_recovery"])
        self.assertIn("Continue the scoped implementation decision", route["instruction"])
        self.assertNotEqual(route["target"], "reviewer")

    def test_valid_structured_route_wins_over_conflicting_manager_prose(self):
        session = self.session()
        parsed, diagnostics = session._manager_parse_route_tool_calls([{
            "function": {
                "name": "route_to_next_agent",
                "arguments": '{"target":"reviewer","instruction":"Verify current output."}',
            }
        }])

        self.assertTrue(diagnostics["valid"])
        self.assertEqual(parsed["target"], "reviewer")
        self.assertEqual(parsed["source"], "tool")

    def test_invalid_route_records_reason_and_marks_fallback_recovery(self):
        session = self.session()
        bind(session, "_manager_fallback_route", lambda self: {
            "target": "developer",
            "instruction": "Continue canonical work.",
            "reason": "continuity-recovery-manager-assigned-expert",
            "source": "continuity-recovery",
            "fallback_recovery": True,
        })
        bind(session, "_manager_apply_anti_stall", lambda self, route: route)
        bind(session, "_manager_apply_task_policy", lambda self, route: route)
        bind(session, "_align_route_with_current_plan_step", lambda self, route, board=None: route)
        bind(session, "_enforce_sync_plan_route", lambda self, route, board=None: route)

        route = session._manager_route_from_response(
            "下一步应由 developer 创建脚本。",
            [{"function": {"name": "route_to_next_agent", "arguments": {"target": "unknown"}}}],
        )

        self.assertEqual(route["target"], "developer")
        self.assertTrue(route["fallback_recovery"])
        self.assertIn("invalid-target", route["parse_failure"])
        diagnostics = session.blackboard["manager_route_diagnostics"]
        self.assertEqual(diagnostics[-1]["fallback_target"], "developer")
        self.assertIn("invalid-target", diagnostics[-1]["errors"][0])

    def test_anti_stall_does_not_turn_existing_code_into_implicit_review(self):
        session = self.session()
        session.blackboard["code_artifacts"] = {"module.py": {"content": "pass"}}
        session.blackboard["last_delegate"] = {"target": "explorer", "progress_fp": "same"}
        session.blackboard["persisted_manager_routes"] = []
        session.blackboard["failure_ledger"] = {"repeated_delegations": []}
        session.manager_routes = [{"target": "explorer"}] * 3
        session.stall_severity_score = 0
        bind(session, "_watchdog_state_fingerprint", lambda self, board=None: "same")
        bind(session, "_route_scope_matches_current_plan", lambda self, *args, **kwargs: True)

        route = session._manager_apply_anti_stall({
            "target": "explorer",
            "instruction": "Inspect the unresolved API.",
            "task_type": "general",
            "source": "tool",
        })

        self.assertEqual(route["target"], "explorer")
        self.assertEqual(route["source"], "anti-stall")
        self.assertIn("anti-stall-preserve-manager-role", route["reason"])

    def test_fallback_and_anti_stall_routes_cannot_earn_momentum(self):
        self.assertFalse(cc.SessionState._manager_route_can_earn_momentum({
            "source": "fallback",
            "fallback_recovery": True,
        }))
        self.assertFalse(cc.SessionState._manager_route_can_earn_momentum({"source": "anti-stall"}))
        self.assertTrue(cc.SessionState._manager_route_can_earn_momentum({"source": "tool"}))

    def test_manager_coordination_keeps_high_reasoning_budget(self):
        self.assertEqual(cc.COORDINATION_EFFORT, cc.EFFORT_HIGH)
        tool = self.session()._manager_route_tools()[0]
        description = tool["function"]["description"]
        self.assertIn("scoped evidence", description)
        self.assertIn("Do not infer a role", description)
        prompt_source = inspect.getsource(cc.SessionState._manager_system_prompt)
        self.assertIn("You own routing and phase classification", prompt_source)
        self.assertIn("Do not use a fixed status-to-role", prompt_source)
        self.assertNotIn("missing facts->explorer", prompt_source)
        self.assertNotIn("Route to Developer early", prompt_source)

    def test_sync_policy_keeps_manager_target_outside_stale_participant_list(self):
        policy_source = inspect.getsource(cc.SessionState._manager_apply_task_policy)
        self.assertIn("participants.append(target)", policy_source)
        self.assertNotIn("else:\n                target = participants[0]", policy_source)


if __name__ == "__main__":
    unittest.main()
