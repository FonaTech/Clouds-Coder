"""Routing regressions: semantic decisions, IDE envelopes, and task boundaries."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


def classified(level=1, **changes):
    row = {
        "level": level,
        "judgement": "Classified the requested action rather than its topic.",
        "semantic_confidence": "high",
        "inherit_previous_state": False,
        "requires_todos": level >= 2,
        "requires_plan": level >= 3,
        "plan_change_scope": "preserve",
        "plan_change_evidence": "",
    }
    row.update(changes)
    return {"tool_calls": [{"function": {"name": "classify_task_level", "arguments": row}}]}


class SemanticTaskRoutingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="semantic-routing-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.session = cc.SessionState(
            "routing", "Routing", self.root / "sessions", "http://127.0.0.1:9",
            "test-model", self.root / "skills", cc.CryptoBox(self.root / "codes"), self.root,
            defer_initial_persist=True,
        )
        self.session.execution_mode = "sync"
        self.session.auto_task_level_ceiling = 2
        self.session.l2_todo_policy = "force"
        self.session.user_memory_mode = "off"
        self.session._emit = mock.Mock()
        self.session._blackboard_touch = mock.Mock()
        self.session._persist = mock.Mock()
        self.chat = mock.patch.object(self.session, "_chat_with_same_model_retry", return_value=classified()).start()
        self.addCleanup(mock.patch.stopall)

    def route(self, text, response=None):
        if response is not None:
            self.chat.return_value = response
        self.session.runtime_reclassify_required = True
        return self.session._refresh_runtime_task_policy(
            pinned_selection="test-model", force=True, goal_text=text,
        )

    def seed_previous(self, *, status="CODING", level=4, approved_plan=False):
        s = self.session
        s.auto_task_level_ceiling = 0
        s.runtime_task_level = level
        s.runtime_task_type = "engineering"
        s.runtime_task_complexity = "complex"
        s.runtime_direct_objective = "Implement the previous service."
        s.runtime_execution_mode = "sync" if level >= 4 else "single"
        s.runtime_assigned_expert = "developer"
        s.runtime_participants = ["explorer", "developer", "reviewer"] if level >= 4 else ["developer"]
        s.runtime_round_budget = 24
        s.runtime_requires_todos = True
        s.runtime_goal_reset_pending = True
        s.blackboard = s._new_blackboard("Implement the previous service.")
        s.blackboard.update({
            "status": status,
            "execution_logs": [{"content": "Previous verification output"}],
            "research_notes": [{"content": "Previous research"}],
            "code_artifacts": {"service.py": {"content": "pass"}},
        })
        s.blackboard["task_profile"].update({
            "task_level": level, "task_type": "engineering", "complexity": "complex",
            "execution_mode": s.runtime_execution_mode, "requires_todos": True,
        })
        s.todo.update([{"content": "Finish previous implementation", "status": "in_progress"}])
        if approved_plan:
            s.runtime_plan_approved = True
            s.blackboard["plan"] = {"phase": "executing", "steps": ["Implement service"]}
            s.blackboard["project_todos"] = [{
                "id": "old-step", "content": "Implement service", "category": "plan_step",
                "status": "in_progress", "plan_step_index": 0,
            }]

    def test_completed_l4_development_followup_reclassifies_into_l3_or_l4_plan(self):
        for model_level, expected in ((2, 3), (3, 3), (4, 4)):
            with self.subTest(model_level=model_level):
                self.seed_previous(status="COMPLETED", approved_plan=True)
                self.session.auto_task_level_ceiling = 4
                with mock.patch.object(cc.threading.Thread, "start"):
                    self.session.submit_user_message("为已完成服务增加导出接口和集成测试")
                decision = self.route(self.session.runtime_reclassify_goal,
                    classified(model_level, followup_development=True))
                self.assertEqual(decision['level'], expected)
                self.assertTrue(self.session.runtime_plan_mode_needed)
                self.assertEqual(self.session.runtime_execution_mode, 'sync' if expected == 4 else 'single')
                self.assertFalse(self.session.runtime_plan_approved)
                self.assertEqual(self.session.blackboard['previous_task_context']['task_level'], 4)

    def test_completed_l4_development_followup_still_obeys_admin_ceiling(self):
        self.seed_previous(status="COMPLETED")
        self.session.auto_task_level_ceiling = 2
        decision = self.route("为服务增加接口", classified(2, followup_development=True))
        self.assertEqual(decision['level'], 2)
        self.assertFalse(self.session.runtime_plan_mode_needed)

    def test_fresh_submission_cannot_inherit_ended_work_even_if_model_claims_continuation(self):
        self.seed_previous(status='COMPLETED', approved_plan=True)
        self.session.auto_task_level_ceiling = 4
        with mock.patch.object(cc.threading.Thread, 'start'):
            self.session.submit_user_message('在刚完成的服务基础上增加导出校验脚本')
        self.assertEqual(self.session.runtime_task_level,0)
        self.assertEqual(self.session.blackboard['status'],'INITIALIZING')
        decision = self.route(self.session.runtime_reclassify_goal,
            classified(4,followup_development=True,inherit_previous_state=True,requires_plan=False))
        self.assertFalse(decision['inherit_previous_state'])
        self.assertTrue(self.session.runtime_plan_mode_needed)
        self.assertFalse(self.session.runtime_plan_approved)

    def test_manual_l4_preset_does_not_make_new_task_skip_plan_auto(self):
        self.seed_previous(status='COMPLETED', approved_plan=True)
        s = self.session
        s.user_task_level_override = 4
        s.plan_mode_user_preference = 'auto'
        s.messages = [{'role':'user','content':'实现上一服务','ts':1.0},
                      {'role':'assistant','content':'上一服务已完成','ts':2.0}]
        with mock.patch.object(cc.threading.Thread,'start'):
            s.submit_user_message('为刚完成的服务新增导出校验脚本')
        self.assertFalse(s.runtime_first_task_in_session)
        with mock.patch.object(s,'_manager_decide_plan_mode_needed',return_value={'requires_plan':False}):
            s._refresh_runtime_task_policy(pinned_selection='test-model',force=True,goal_text=s.runtime_reclassify_goal)
        self.assertEqual(s.runtime_task_level,4)
        self.assertTrue(s.runtime_plan_mode_needed)
        self.assertFalse(s.runtime_plan_approved)

    def test_completed_l4_concept_question_remains_l1(self):
        self.seed_previous(status="COMPLETED")
        self.session.auto_task_level_ceiling = 4
        decision = self.route("API是什么意思？", classified(1, followup_development=False))
        self.assertEqual(decision['level'], 1)
        self.assertFalse(self.session.runtime_plan_mode_needed)

    def test_interrupted_unapproved_planning_continues_in_plan_before_execution(self):
        for phase in ('research', 'synthesis'):
            with self.subTest(phase=phase):
                self.seed_previous(status='PLANNING', level=3)
                self.session.runtime_plan_approved = False
                self.session.plan_mode_user_preference = 'auto'
                self.session.blackboard['plan'] = {'phase': phase, 'findings': []}
                self.route('继续')
                self.assertEqual(self.session.runtime_task_level, 3)
                self.assertTrue(self.session.runtime_plan_mode_needed)
                self.assertFalse(self.session.runtime_plan_approved)

    def test_interrupted_planning_still_honors_explicit_plan_off(self):
        self.seed_previous(status='PLANNING', level=3)
        self.session.blackboard['plan'] = {'phase': 'research', 'findings': []}
        self.session.runtime_plan_approved = False
        self.session.plan_mode_user_preference = 'off'
        self.route('继续')
        self.assertFalse(self.session.runtime_plan_mode_needed)

    def test_fast_local_prescreen_cannot_bypass_semantic_router(self):
        with mock.patch.object(cc, "FAST_START_LOCAL_CLASSIFICATION", True):
            decision = self.route("Python是什么？")
        self.assertEqual(self.chat.call_count, 1)
        self.assertEqual(decision["source"], "manager")
        self.assertEqual(self.session.runtime_task_level, 1)
        self.assertEqual(self.session.runtime_task_type, "simple_qa")
        self.assertFalse(self.session._runtime_level_requires_todos())
        self.assertEqual(self.session.runtime_execution_mode, "single")

    def test_topic_keywords_and_greetings_obey_semantic_result(self):
        for text in ("你好", "谢谢", "1+1等于多少？", "API是什么？", "测试是什么意思？", "内核是什么？", "请解释一下什么是函数"):
            with self.subTest(text=text):
                self.session.runtime_task_level = 0
                self.session.blackboard = self.session._new_blackboard("")
                self.session._cached_llm_complexity = self.session._local_classify_task_complexity(text)
                decision = self.route(text)
                self.assertEqual(decision["level"], 1)
                self.assertFalse(decision["requires_todos"])
                self.assertFalse(self.session.runtime_plan_mode_needed)

    def test_actual_ide_entrypoint_and_chat_classify_the_same_user_request(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app.ide_resolve_workspace = mock.Mock(return_value=(self.root, None, {"label": "工作区", "kind": "workspace"}))
        app._ide_session = mock.Mock(return_value=self.session)
        app.submit_user_message = mock.Mock(return_value={"ok": True})
        question = "1+1等于多少？"
        cc.AppContext.ide_agent_task(app, "test-user", "routing", {
            "message": question, "active_path": "src/api.py",
        })
        envelope = app.submit_user_message.call_args.args[2]
        self.assertIn("Active file: src/api.py", envelope)
        self.session.runtime_reclassify_goal = envelope
        decision = self.route(envelope)
        prompt = self.chat.call_args.args[0][0]["content"]
        self.assertIn("User request:\n" + question + "\n", prompt)
        self.assertNotIn("IDE programming request.", prompt)
        self.assertNotIn("Active file: src/api.py", prompt)
        self.assertEqual(decision["level"], 1)
        self.assertEqual(self.session.runtime_reclassify_goal, question)
        self.assertFalse(self.session._single_no_plan_todo_bootstrap_allowed())

    def test_ide_multiline_request_and_attachment_metadata_keep_exact_user_body(self):
        body = "解释下面的代码，不修改文件：\n\nprint('你好')"
        text = "IDE programming request.\nWorkspace root: demo\nWritable path: /tmp/demo\nAttached workspace files (read as needed):\n- api.py\n\n" + body
        self.route(text)
        self.assertIn("User request:\n" + body + "\n", self.chat.call_args.args[0][0]["content"])

    def test_automatic_ceiling_controls_level_mode_todos_and_plan(self):
        for ceiling, expected in ((1, 1), (2, 2), (3, 3), (0, 4)):
            with self.subTest(ceiling=ceiling):
                self.session.runtime_task_level = 0
                self.session.blackboard = self.session._new_blackboard("")
                self.session.auto_task_level_ceiling = ceiling
                row = self.route("实现一个完整服务", classified(4))
                self.assertEqual(row["level"], expected)
                self.assertEqual(self.session.runtime_task_level, expected)
                self.assertEqual(self.session._runtime_level_requires_todos(), expected >= 2)
                self.assertEqual(self.session.runtime_execution_mode, "sync" if expected == 4 else "single")
                self.assertEqual(self.session.runtime_plan_mode_needed, expected >= 3)

    def test_unfinished_task_keeps_level_even_for_an_independent_short_question(self):
        self.seed_previous()
        self.chat.return_value = classified(1)
        decision = self.route("法国的首都是哪里？")
        self.assertEqual(decision["level"], 4)
        self.assertTrue(decision["inherit_previous_state"])
        self.assertEqual(self.session.runtime_task_level, 4)
        self.assertEqual(self.session.runtime_task_type, "engineering")
        self.assertTrue(self.session.todo.has_open_items())

    def test_unfinished_approved_plan_survives_classification(self):
        self.seed_previous(approved_plan=True)
        self.route("这一步该怎么做？")
        self.assertEqual(self.session.runtime_task_level, 4)
        self.assertTrue(self.session.runtime_plan_approved)
        self.assertEqual(self.session.blackboard["plan"]["phase"], "executing")
        self.assertEqual(self.session.blackboard["project_todos"][0]["id"], "old-step")

    def test_unfinished_task_is_resumable_before_any_artifact_exists(self):
        self.seed_previous(status="INITIALIZING")
        for key in ("research_notes", "execution_logs", "review_feedback"):
            self.session.blackboard[key] = []
        self.session.blackboard["code_artifacts"] = {}
        self.session.todo.items = []
        self.assertTrue(self.session._has_resumable_work_state())

    def test_ordinary_submission_reclassifies_after_completion(self):
        self.seed_previous(status="COMPLETED", approved_plan=True)
        self.session.auto_task_level_ceiling = 2
        with mock.patch.object(cc.threading.Thread, "start"):
            self.session.submit_user_message("API是什么？")
        self.route(self.session.runtime_reclassify_goal)
        self.assertEqual(self.session.runtime_task_level, 1)
        self.assertFalse(self.session._runtime_level_requires_todos())
        self.assertFalse(self.session.runtime_plan_approved)

    def test_ordinary_submission_restores_unfinished_level(self):
        self.seed_previous(status="PAUSED", level=3)
        with mock.patch.object(cc.threading.Thread, "start"):
            self.session.submit_user_message("下一步怎么做？")
        self.route(self.session.runtime_reclassify_goal)
        self.assertEqual(self.session.runtime_task_level, 3)
        self.assertEqual(self.session.runtime_execution_mode, "single")

    def test_completed_and_aborted_tasks_cannot_donate_levels_or_plan_locks(self):
        for status in ("COMPLETED", "ABORTED"):
            with self.subTest(status=status):
                self.seed_previous(status=status, approved_plan=True)
                self.session.runtime_task_level_floor = 4
                self.session.runtime_task_level_ceiling = 4
                self.session.runtime_complexity_floor = "complex"
                row = self.route("Python是什么？", classified(1, inherit_previous_state=True))
                self.assertEqual(row["level"], 1)
                self.assertFalse(row["inherit_previous_state"])
                self.assertEqual(self.session.runtime_task_level, 1)
                self.assertEqual(self.session.runtime_task_complexity, "simple")
                self.assertFalse(self.session.runtime_plan_approved)
                self.assertFalse(self.session.runtime_plan_mode_needed)
                self.assertFalse(self.session.todo.has_open_items())
                self.assertEqual(self.session.blackboard["previous_task_context"]["goal"], "Implement the previous service.")

    def test_continuation_phrase_does_not_revive_an_ended_task(self):
        self.seed_previous(status="COMPLETED")
        decision = self.route("继续", classified(2))
        self.assertEqual(self.chat.call_count, 1)
        self.assertEqual(decision["level"], 2)
        self.assertFalse(decision["inherit_previous_state"])

    def test_unfinished_continuation_is_bounded_by_updated_system_ceiling(self):
        self.seed_previous(approved_plan=True)
        self.session.auto_task_level_ceiling = 2
        decision = self.route("继续")
        self.chat.assert_not_called()
        self.assertEqual(decision["level"], 2)
        self.assertEqual(self.session.runtime_task_level, 2)
        self.assertEqual(self.session.runtime_execution_mode, "single")
        self.assertTrue(self.session.runtime_plan_approved)

    def test_cached_policy_cannot_bypass_a_lowered_admin_ceiling(self):
        self.seed_previous()
        self.session.auto_task_level_ceiling = 2
        self.session.runtime_reclassify_required = False
        self.session.runtime_goal_reset_pending = False
        row = self.session._refresh_runtime_task_policy(
            pinned_selection="test-model", goal_text="API是什么？",
        )
        self.assertEqual(row["level"], 2)
        self.assertEqual(self.session.runtime_task_level, 2)
        self.assertEqual(self.session.runtime_execution_mode, "single")

    def test_completion_state_ends_level_inheritance_even_with_stale_status(self):
        self.seed_previous()
        self.session.blackboard["completion"]["state"] = "completed"
        row = self.route("API是什么？")
        self.assertEqual(row["level"], 1)
        self.assertFalse(row["inherit_previous_state"])

    def test_explicit_user_level_still_bypasses_automatic_ceiling(self):
        self.session.auto_task_level_ceiling = 1
        self.session.user_task_level_override = 3
        self.session.plan_mode_user_preference = "off"
        decision = self.route("执行这个任务")
        self.chat.assert_not_called()
        self.assertEqual(decision["level"], 3)
        self.assertEqual(self.session.runtime_task_level, 3)

    def test_invalid_semantic_level_is_repaired_before_execution(self):
        self.chat.side_effect = [classified(99), classified(1)]
        self.route("API是什么？")
        self.assertEqual(self.chat.call_count, 2)
        self.assertEqual(self.session.runtime_task_level, 1)

    def test_non_tool_json_semantic_response_is_accepted(self):
        row = classified()["tool_calls"][0]["function"]["arguments"]
        self.route("API是什么？", {"content": json.dumps(row)})
        self.assertEqual(self.chat.call_count, 1)
        self.assertEqual(self.session.runtime_task_level, 1)

    def test_model_failure_fallback_stays_capped_and_is_reported(self):
        self.chat.side_effect = cc.OllamaError("test provider unavailable")
        row = self.route("API是什么？")
        self.assertEqual(row["level"], 2)
        self.assertTrue(row["source"].startswith("fallback-model-error"))
        self.assertTrue(any("semantic task classification unavailable" in str(call) for call in self.session._emit.call_args_list))

    def test_cancelled_classification_does_not_fall_back_into_execution(self):
        self.chat.side_effect = cc.OllamaError("cancelled")
        self.session.cancel_requested = True
        with self.assertRaises(cc.OllamaError):
            self.route("API是什么？")
        self.assertEqual(self.session.runtime_task_level, 0)

    def test_semantic_classifier_respects_admin_output_budget(self):
        self.session.max_output_tokens = 256
        self.route("API是什么？")
        self.assertEqual(self.chat.call_args.kwargs["max_tokens"], 256)


if __name__ == "__main__":
    unittest.main()
