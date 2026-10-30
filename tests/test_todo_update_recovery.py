"""Regressions for identity loss, correction lockout and stale Todo focus."""
import copy
import unittest
from unittest.mock import patch

import Clouds_Coder as cc
import test_todo_tree_revision_guard as fixtures


class TodoUpdateRecoveryTests(unittest.TestCase):
    def root_session(self, mode="single", count=3):
        guard = fixtures.TodoTreeRevisionGuardTests()
        session = guard.bare_session(mode)
        session._dispatch_todo_update({"todos": guard.stages(count)}, role="developer")
        return session

    @staticmethod
    def children(session, step):
        return [row for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]

    def test_plan_id_only_updates_support_all_displayed_ids_and_aliases(self):
        for mode in ("single", "sync"):
            for field in ("id", "short_id", "todo_id", "subtask_id", "mapping", "tag", "canonical"):
                with self.subTest(mode=mode, field=field):
                    session, step = fixtures.TodoTreeRevisionGuardTests().plan_session(mode)
                    # Seed canonical ids using the real dispatcher.
                    session._dispatch_todo_update({"resume": True}, role="developer")
                    child = self.children(session, step)[1]
                    if field == "mapping":
                        payload = {"updates": {child["short_id"]: {"status": "in_progress"}}}
                    elif field == "tag":
                        payload = {"todos": [f"[>] ({child['short_id']})"]}
                    else:
                        key = "id" if field == "canonical" else field
                        value = child["subtask_id"] if field == "canonical" else child["short_id"]
                        payload = {"todos": [{key: value, "status": "in_progress"}]}
                    result = session._dispatch_todo_update(payload, role="developer")
                    rows = self.children(session, step)
                    self.assertEqual(len(rows), 3, result)
                    self.assertEqual(rows[1]["status"], "in_progress", result)
                    self.assertEqual(rows[0]["status"], "pending", result)
                    self.assertEqual(rows[1]["subtask_id"], child["subtask_id"])
                    self.assertEqual(rows[1]["content"], child["content"])
                    self.assertEqual(session.ollama.calls, [])

    def test_root_canonical_id_survives_multiple_content_edits_and_restore(self):
        session = self.root_session()
        original = session.todo.snapshot()[1]
        for title in ("替换为当前实现目标", "补充最新接口约束"):
            session._dispatch_todo_update({"todos": [{"id": original["short_id"], "content": title}]}, role="developer")
            row = session.todo.snapshot()[1]
            self.assertEqual(row["subtask_id"], original["subtask_id"])
            self.assertEqual(row["short_id"], original["short_id"])
        restored = session._normalize_loaded_todo_rows(session._todos_for_persist(), [])
        session.todo.update(restored)
        result = session._dispatch_todo_update({"todos": [{"id": original["subtask_id"], "status": "completed"}]}, role="developer")
        self.assertEqual(session.todo.snapshot()[1]["status"], "completed", result)
        self.assertEqual(len(session.todo.snapshot()), 3)

    def test_root_status_only_display_tag_preserves_content(self):
        session = self.root_session()
        target = session.todo.snapshot()[1]
        result = session._dispatch_todo_update({"todos": [f"[x] ({target['short_id']})"]}, role="developer")
        row = session.todo.snapshot()[1]
        self.assertEqual(row["status"], "completed", result)
        self.assertEqual(row["content"], target["content"])

    def test_unknown_explicit_reference_never_appends_or_partially_commits(self):
        for plan in (False, True):
            for ref in ("t999", "rt:missing", "pst:missing:123"):
                with self.subTest(plan=plan, ref=ref):
                    if plan:
                        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
                        target = self.children(session, step)[0]
                    else:
                        session = self.root_session()
                        target = session.todo.snapshot()[0]
                    before = copy.deepcopy(session.todo.snapshot())
                    result = session._dispatch_todo_update({"todos": [
                        {"id": target["short_id"], "status": "pending"},
                        {"id": ref, "content": "不应被追加的修改", "status": "in_progress"},
                    ]}, role="developer")
                    self.assertIn("Error:", result)
                    self.assertEqual(session.todo.snapshot(), before)

    def test_render_echo_does_not_copy_display_suffix_into_task_content(self):
        for plan in (False, True):
            with self.subTest(plan=plan):
                if plan:
                    session, _step = fixtures.TodoTreeRevisionGuardTests().plan_session()
                    session._dispatch_todo_update({"resume": True}, role="developer")
                else:
                    session = self.root_session()
                before = [row["content"] for row in session.todo.snapshot()]
                lines = [line for line in session.todo.render().splitlines() if line.startswith("[")]
                if plan:
                    lines = lines[1:]  # System roadmap row is not a worker edit.
                result = session._dispatch_todo_update({"todos": lines}, role="developer")
                self.assertEqual([row["content"] for row in session.todo.snapshot()], before, result)

    def test_root_focus_moves_to_explicit_target_without_resending_old_row(self):
        session = self.root_session()
        target = session.todo.snapshot()[2]
        result = session._dispatch_todo_update({"todos": [{"id": target["short_id"], "status": "in_progress"}]}, role="developer")
        rows = session.todo.snapshot()
        self.assertEqual([row["status"] for row in rows], ["pending", "pending", "in_progress"], result)

    def test_long_rendered_working_row_drops_suffix_before_truncation(self):
        session = self.root_session()
        target = session.todo.snapshot()[0]
        title = "检查长任务的接口约束和兼容性条件" * 25
        session._dispatch_todo_update({"todos": [{"id": target["short_id"], "content": title}]}, role="developer")
        before = session.todo.snapshot()[0]["content"]
        line = session.todo.render().splitlines()[0]
        result = session._dispatch_todo_update({"todos": [line]}, role="developer")
        self.assertEqual(session.todo.snapshot()[0]["content"], before, result)

    def test_automatic_next_task_has_working_display_text(self):
        session = self.root_session()
        target = session.todo.snapshot()[0]
        session._dispatch_todo_update({"todos": [{"id": target["short_id"], "status": "completed"}]}, role="developer")
        row = session.todo.snapshot()[1]
        self.assertEqual(row["status"], "in_progress")
        self.assertEqual(row["activeForm"], session.todo._default_active_form("in_progress", row["content"], owner=row["owner"]))

    def test_corrected_payload_stays_available_after_two_noops(self):
        session = self.root_session()
        target = session.todo.snapshot()[0]
        payload = {"todos": [{"id": target["short_id"], "status": "in_progress"}]}
        for _ in range(3):
            session._dispatch_todo_update(payload, role="developer")
        specs = [cc.tool_def(name, name, {}) for name in ("TodoWrite", "TodoWriteRescue", "read_file")]
        self.assertEqual(session._filter_todo_progress_tools(specs, role="developer"), specs)
        result = session._dispatch_todo_update({"todos": [{"id": target["short_id"], "status": "completed"}]}, role="developer")
        self.assertEqual(session.todo.snapshot()[0]["status"], "completed", result)

    def test_rejected_revision_allows_correction_without_forcing_obsolete_work(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
        target = self.children(session, step)[0]
        payload = {"todos": [{"id": target["short_id"], "content": "1.1 调整接口检查范围", "status": "in_progress"}]}
        for _ in range(2):
            result = session._dispatch_todo_update(payload, role="developer")
        self.assertNotIn("do not resubmit this revision", result)
        self.assertIn("revise_open", result)
        fixed = self.children(session, step)
        fixed[0]["content"] = payload["todos"][0]["content"]
        with patch.object(session, "_review_plan_worker_revision", return_value={"ok": True, "structural": True}):
            result = session._dispatch_todo_update({"todos": fixed, "update_mode": "revise_open",
                "revision_reason": "接口检查发现范围需要调整", "revision_evidence": ["ev:scope"]}, role="developer")
        self.assertIn("调整接口检查范围", self.children(session, step)[0]["content"], result)

    def test_single_prompt_contains_complete_long_list(self):
        session = self.root_session(count=40)
        with patch.object(session, "_agent_loop_todo_alignment", return_value={"todo_total": 40}):
            prompt = session._single_agent_todo_alignment_prompt_block("developer")
        for row in session.todo.snapshot():
            self.assertIn(f"({row['short_id']})", prompt)
            self.assertIn(row["content"], prompt)
        self.assertIn("</single-todo-alignment-state>", prompt)

    def test_plan_canonical_output_displays_committed_short_ids(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
        result = session._dispatch_todo_update({"resume": True}, role="developer")
        canonical = result.split("CANONICAL SUBTASKS", 1)[1]
        for row in self.children(session, step):
            self.assertIn(f"({row['short_id']})", canonical)
            self.assertIn(row["subtask_id"], canonical)

    def test_plan_canonical_lines_round_trip_without_changing_content(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
        result = session._dispatch_todo_update({"resume": True}, role="developer")
        before = self.children(session, step)
        lines = [line.strip() for line in result.split("CANONICAL SUBTASKS", 1)[1].splitlines()
                 if line.strip().startswith("[")]
        result = session._dispatch_todo_update({"todos": lines}, role="developer")
        self.assertEqual([row["content"] for row in self.children(session, step)],
                         [row["content"] for row in before], result)

    def test_same_discovery_can_support_successive_audited_refinements(self):
        approve = {"approved": True, "confidence": "high", "reason": "The discovery supports this refinement.",
                   "unsupported_changes": []}
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session, step = fixtures.TodoTreeRevisionGuardTests().plan_session(mode, [approve, approve])
                session.blackboard["plan_step_evidence"] = {step["id"]: [{
                    "id": "ev:scope-discovery", "step_id": step["id"], "kind": "runtime", "tool": "read_file",
                    "ok": True, "summary": "接口检查发现必须同时记录跨模块约束与兼容性条件", "ts": 20.0,
                }]}
                for title in ("1.1 检查现有接口并记录跨模块约束", "1.1 检查现有接口并记录跨模块约束与兼容性条件"):
                    rows = self.children(session, step)
                    rows[0]["content"] = title
                    result = session._dispatch_todo_update({"todos": rows, "update_mode": "revise_open",
                        "revision_reason": "已发现的接口约束要求进一步调整检查内容", "revision_evidence": ["ev:scope-discovery"]},
                        role="developer")
                    self.assertIn("ROLLING SUBPLAN REVISION: accepted", result)
                    self.assertEqual(len(self.children(session, step)), 3)
                self.assertEqual(len(session.ollama.calls), 2)

    def test_plan_id_only_completion_keeps_evidence_gate(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
        target = self.children(session, step)[0]
        with patch.object(session, "_plan_worker_completion_has_evidence", return_value=False):
            result = session._dispatch_todo_update({"todos": [{"id": target["short_id"], "status": "completed"}]},
                                                   role="developer")
        self.assertNotEqual(self.children(session, step)[0]["status"], "completed", result)
        self.assertEqual(len(self.children(session, step)), 3)

    def test_invalid_id_prevents_even_an_accompanying_parent_edit(self):
        session, step = fixtures.TodoTreeRevisionGuardTests().plan_session()
        before = copy.deepcopy(session.blackboard)
        result = session._dispatch_todo_update({"todos": [{"id": "t999", "content": "修改后的工作"}],
            "plan_updates": [{"step_id": step["id"], "content": "修改母步骤内容"}]}, role="developer")
        self.assertIn("Error:", result)
        self.assertEqual(session.blackboard, before)


if __name__ == "__main__":
    unittest.main()
