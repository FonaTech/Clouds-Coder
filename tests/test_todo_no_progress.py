import copy
import types
import unittest
from unittest.mock import patch

import test_todo_tree_revision_guard as fixtures

import Clouds_Coder as cc


class TodoNoProgressTests(unittest.TestCase):
    def session(self, mode="single"):
        return fixtures.TodoTreeRevisionGuardTests().bare_session(mode)

    @staticmethod
    def payload():
        return {"items": [
            {"content": "Inspect the module", "status": "in_progress"},
            {"content": "Implement the requested behavior", "status": "pending"},
            {"content": "Run regression tests", "status": "pending"},
        ]}

    @staticmethod
    def specs():
        return [cc.tool_def(name, name, {}) for name in (
            "TodoWrite", "TodoWriteRescue", "TodoWriteResume", "read_file", "bash",
        )]

    def repeat_until_guarded(self, session):
        payload = self.payload()
        session._dispatch_todo_update(payload, role="developer")
        for _ in range(2):
            result = session._dispatch_todo_update(payload, role="developer")
            self.assertIn("Control[todo_no_progress]", result)
        return payload

    def test_repeated_full_snapshot_without_ids_needs_no_extra_model_calls(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.session(mode)
                payload = self.repeat_until_guarded(session)
                before = copy.deepcopy(session.todo.snapshot())
                with patch.object(session, "_dispatch_todo_update_inner", side_effect=AssertionError("must not audit again")):
                    result = session._dispatch_todo_update(payload, role="developer")
                    rescue = session._todo_write_rescue(payload, role="developer")
                    resume = session._dispatch_todo_update({}, role="developer", resume=True)
                for output in (result, rescue, resume):
                    self.assertIn("Control[todo_no_progress]", output)
                self.assertEqual(session.todo.snapshot(), before)
                self.assertEqual(session.ollama.calls, [])
                self.assertEqual([spec["function"]["name"] for spec in
                                  session._filter_todo_progress_tools(self.specs(), role="developer")],
                                 [spec["function"]["name"] for spec in self.specs()])

    def test_no_change_is_not_reported_as_progress_or_tool_failure(self):
        session = self.session()
        session._dispatch_todo_update(self.payload(), role="developer")
        before = session.todo.snapshot()
        output = session._dispatch_todo_update(self.payload(), role="developer")
        state, reason = session._analyze_todo_result(
            "TodoWrite", output, before_rows=before, after_rows=session.todo.snapshot(),
        )
        self.assertEqual(state, "no_progress")
        self.assertIn("unchanged", reason)
        feedback = session._annotate_tool_control_feedback({"name": "TodoWrite", "output": output, "ok": False})
        self.assertTrue(feedback["control_feedback"])
        self.assertEqual(feedback["control_outcome"], "todo_no_progress")
        state, _ = session._analyze_todo_result(
            "TodoWrite", "CANONICAL SUBTASKS: unchanged", before_rows=before, after_rows=before,
        )
        self.assertEqual(state, "no_progress")

    def test_normal_status_transition_remains_available(self):
        session = self.session()
        payload = self.payload()
        session._dispatch_todo_update(payload, role="developer")
        session._dispatch_todo_update(payload, role="developer")  # One redundant update is harmless.
        payload["items"][0]["status"] = "completed"
        payload["items"][1]["status"] = "in_progress"
        before = session.todo.snapshot()
        output = session._dispatch_todo_update(payload, role="developer")
        self.assertEqual(session._analyze_todo_result(
            "TodoWrite", output, before_rows=before, after_rows=session.todo.snapshot(),
        )[0], "ok")
        self.assertEqual(session._filter_todo_progress_tools(self.specs(), role="developer"), self.specs())
        self.assertEqual(session.ollama.calls, [])

    def test_work_tool_releases_guard_including_external_mcp(self):
        session = self.session()
        payload = self.repeat_until_guarded(session)
        session.mcp = types.SimpleNamespace(call=lambda name, args: "module inspected")
        with patch.object(session, "_observe_step_skill_tool"):
            result = session._dispatch_tool_inner("mcp__test__inspect", {}, role_key="developer")
        self.assertEqual(result, "module inspected")
        self.assertEqual(session._filter_todo_progress_tools(self.specs(), role="developer"), self.specs())
        payload["items"][0]["status"] = "completed"
        payload["items"][1]["status"] = "in_progress"
        output = session._dispatch_todo_update(payload, role="developer")
        self.assertNotIn("todo_no_progress", output)
        self.assertEqual(session.todo.snapshot()[0]["status"], "completed")

    def test_cooldown_is_scoped_to_role_task_and_run(self):
        session = self.session("sync")
        self.repeat_until_guarded(session)
        self.assertEqual(session._filter_todo_progress_tools(self.specs(), role="reviewer"), self.specs())
        session.blackboard["task_epoch"] += 1
        self.assertEqual(session._filter_todo_progress_tools(self.specs(), role="developer"), self.specs())
        session.blackboard["task_epoch"] -= 1
        session.run_generation += 1
        self.assertEqual(session._filter_todo_progress_tools(self.specs(), role="developer"), self.specs())

    def test_plan_snapshot_repetition_preserves_completion_checks(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session, step = fixtures.TodoTreeRevisionGuardTests().plan_session(mode)
                rows = [dict(row) for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]
                # First merge may attach canonical IDs; repeats must then converge.
                for _ in range(4):
                    output = session._dispatch_todo_update({"items": rows}, role="developer")
                self.assertIn("todo_no_progress", output)
                self.assertEqual(session.ollama.calls, [])
                self.assertTrue(session._todowrite_step_counter)
                self.assertTrue(any(row["status"] == "pending" for row in session.todo.snapshot()))

    def test_repeated_completion_without_evidence_is_not_success(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session("single")
        rows = [dict(row) for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]
        rows[0]["status"] = "completed"
        with patch.object(session, "_plan_worker_completion_has_evidence", return_value=False):
            for _ in range(4):
                output = session._dispatch_todo_update({"items": rows}, role="developer")
        self.assertIn("todo_no_progress", output)
        work = [row for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]
        self.assertNotEqual(work[0]["status"], "completed")

    def test_exact_unscoped_plan_child_does_not_need_intent_classification(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session("single")
        child = {"content": "Implement the module", "status": "in_progress", "parent_step_id": step["id"]}
        with patch.object(session, "_active_plan_worker_todo_rows", return_value=[child]):
            result = session._classify_plan_worker_parent_update(
                {**child, "_parent_step_inferred": True}, step,
            )
        self.assertEqual(result, {})
        self.assertEqual(session.ollama.calls, [])

    def test_provider_receives_work_tools_and_cleared_forced_todo_choice(self):
        session = self.session()
        self.repeat_until_guarded(session)
        calls = []
        session.cancel_requested = False
        session.ollama = types.SimpleNamespace(response_stream=False, chat=lambda messages, **kwargs:
                                              calls.append(kwargs) or {"content": "work", "tool_calls": []})
        for name, fn in {
            "_active_runtime_selection": lambda self: "test::model",
            "_inject_runtime_environment_context": lambda self, text: text,
            "_estimate_model_call_prompt_tokens": lambda self, *args, **kwargs: 1,
            "_resolve_effort_for_call": lambda self, **kwargs: "off",
            "_call_interruptible": lambda self, fn, **kwargs: fn(),
            "_record_model_usage": lambda self, *args, **kwargs: None,
        }.items():
            fixtures.bind(session, name, fn)
        session._chat_with_same_model_retry(
            [{"role": "user", "content": "Continue"}], tools=self.specs(), tool_choice="TodoWrite",
            context_label="developer turn", retries=0,
        )
        self.assertEqual(calls[0]["tools"], self.specs())
        self.assertFalse(calls[0].get("tool_choice"))
        self.assertIn("Corrected requests and real status changes", calls[0]["system"])


if __name__ == "__main__":
    unittest.main()
