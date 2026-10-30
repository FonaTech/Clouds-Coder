"""Scenario tests for the three reported TodoWrite symptoms.

1. Goals could not be revised in real time.
2. TodoWrite looped without making progress.
3. Duplicate rows appeared that repeated earlier rows.

Every case drives the real dispatcher and merge path
(``_dispatch_todo_update`` -> ``_merge_root_todo_scope`` -> ``TodoManager``)
with a recording model client, so the model-call counts are real.
"""

import unittest

import test_todo_tree_revision_guard as fixtures
from test_todo_llm_budget import recording_client

import Clouds_Coder as cc


def stored(session):
    return session._todo_route_rows("pure_single", role="developer")


class TodoShortIdScenarioTests(unittest.TestCase):
    def session(self, count=3):
        guard = fixtures.TodoTreeRevisionGuardTests("test_status_update_can_add_work_without_replacing_the_roadmap")
        session = guard.bare_session("single")
        session.ollama = recording_client()
        session._dispatch_todo_update({"todos": guard.stages(count)}, role="developer")
        return session

    # Symptom 3: duplicates -------------------------------------------------

    def test_render_shows_stable_short_ids(self):
        session = self.session(3)
        rendered = session.todo.render()
        for sid in ("(t1)", "(t2)", "(t3)"):
            self.assertIn(sid, rendered)
        self.assertEqual([row["short_id"] for row in stored(session)], ["t1", "t2", "t3"])

    def test_echoing_render_output_creates_no_rows_and_no_model_calls(self):
        session = self.session(3)
        echoed = [line for line in session.todo.render().splitlines() if line.strip().startswith("[")]
        session._dispatch_todo_update({"todos": echoed}, role="developer")
        self.assertEqual(len(stored(session)), 3)
        self.assertEqual(session.ollama.impl_calls, [])

    def test_reworded_duplicate_updates_the_existing_row(self):
        session = self.session(1)
        session._dispatch_todo_update(
            {"todos": [{"content": "编写 README 文档", "status": "pending"}]}, role="developer"
        )
        before = len(stored(session))
        session._dispatch_todo_update(
            {"todos": [{"content": "- 编写README文档。", "status": "pending"}]}, role="developer"
        )
        self.assertEqual(len(stored(session)), before)

    def test_distinct_numbered_substeps_never_merge(self):
        session = self.session(1)
        session._dispatch_todo_update(
            {"todos": [
                {"content": "1.1 实现解析器", "status": "pending"},
                {"content": "1.2 实现解析器测试", "status": "pending"},
            ]},
            role="developer",
        )
        session._dispatch_todo_update(
            {"todos": [{"content": "1.3 实现解析器", "status": "pending"}]}, role="developer"
        )
        contents = [row["content"] for row in stored(session)]
        self.assertIn("1.3 实现解析器", contents)
        self.assertIn("1.1 实现解析器", contents)

    def test_worker_reply_checklist_only_syncs_existing_rows(self):
        session = self.session(2)
        target = stored(session)[1]
        result = session._merge_todo_signal_rows(
            [
                {"content": target["content"], "status": "completed"},
                {"content": "一条全新的、从未登记过的任务", "status": "pending"},
            ],
            role="developer",
        )
        rows = stored(session)
        self.assertEqual(len(rows), 2, result)
        self.assertEqual(rows[1]["status"], "completed")

    def test_short_ids_survive_persist_and_load(self):
        session = self.session(3)
        restored = session._normalize_loaded_todo_rows(session._todos_for_persist(), [])
        self.assertEqual([row.get("short_id") for row in restored], ["t1", "t2", "t3"])

    # Symptom 1: real-time revision ------------------------------------------

    def test_update_by_short_id_changes_status_and_text_without_model_calls(self):
        session = self.session(3)
        session._dispatch_todo_update(
            {"todos": [
                {"id": "t1", "status": "completed"},
                {"id": "t2", "content": "阶段2 改写后的目标", "status": "in_progress"},
            ]},
            role="developer",
        )
        rows = stored(session)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["status"], "completed")
        self.assertEqual(rows[1]["content"], "阶段2 改写后的目标")
        self.assertEqual(rows[1]["status"], "in_progress")
        self.assertEqual(session.ollama.impl_calls, [])

    def test_update_by_rt_id_and_by_echoed_tag(self):
        session = self.session(3)
        rows = stored(session)
        session._dispatch_todo_update(
            {"todos": [{"id": rows[2]["subtask_id"], "status": "completed"}]}, role="developer"
        )
        session._dispatch_todo_update({"todos": ["[x] (t2)"]}, role="developer")
        rows = stored(session)
        self.assertEqual([row["status"] for row in rows][1:], ["completed", "completed"])
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(not row.get("external_subtask_id") for row in rows))

    def test_status_update_with_evidence_is_applied_immediately(self):
        session = self.session(2)
        session._dispatch_todo_update(
            {"todos": [{"id": "t1", "status": "completed"}], "evidence": ["tests passed"]},
            role="developer",
        )
        self.assertEqual(stored(session)[0]["status"], "completed")
        self.assertEqual(session.ollama.impl_calls, [])

    # Symptom 2: loops ---------------------------------------------------------

    def test_rejection_names_the_next_step(self):
        session = self.session(3)
        session.ollama = recording_client([{
            "decision": "reject", "confidence": "high", "reason": "coverage not shown",
            "removed_objectives": [], "replacement_mapping": [], "requirement_coverage": [],
            "completion_risk": "high", "evidence": [],
        }])
        result = session._dispatch_todo_update(
            {"todos": [{"content": "只保留一个目标", "status": "in_progress"}],
             "update_mode": "revise_open", "revision_reason": "scope changed"},
            role="developer",
        )
        self.assertIn("rejected", result)
        self.assertIn("Next step", result)
        self.assertIn("(t1)", result)
        self.assertEqual(len(stored(session)), 3)

    def test_repeated_rejections_block_same_request_but_keep_corrections_available(self):
        session = self.session(3)
        reject = {
            "decision": "reject", "confidence": "high", "reason": "coverage not shown",
            "removed_objectives": [], "replacement_mapping": [], "requirement_coverage": [],
            "completion_risk": "high", "evidence": [],
        }
        session.ollama = recording_client([reject, reject, reject])
        payload = {
            "todos": [{"content": "只保留一个目标", "status": "in_progress"}],
            "update_mode": "revise_open", "revision_reason": "scope changed",
        }
        for _ in range(2):
            session._dispatch_todo_update(dict(payload), role="developer")
        third = session._dispatch_todo_update(dict(payload), role="developer")
        self.assertIn("Control[todo_no_progress]", third)
        specs = [
            cc.tool_def("TodoWrite", "todo", {}),
            cc.tool_def("read_file", "read", {"path": {"type": "string"}}),
        ]
        names = [spec["function"]["name"] for spec in session._filter_todo_progress_tools(specs, role="developer")]
        self.assertEqual(names, ["TodoWrite", "read_file"])

    def test_bootstrap_call_is_a_plain_status_update(self):
        session = self.session(1)
        session.todo.items = []
        session.runtime_authoritative_goal = "1. Inspect\n2. Fix\n3. Test"
        call = session._deterministic_bootstrap_todo_call()
        self.assertIsNotNone(call)
        args = call["function"]["arguments"]
        self.assertNotIn("revision_reason", args)
        self.assertEqual(args.get("update_mode"), "status_update")

    def test_role_prompt_lists_ids_for_multi_agent_workers(self):
        session = self.session(2)
        block = session._role_todo_ids_prompt_block("developer")
        self.assertIn("(t1)", block)
        self.assertIn("(t2)", block)


if __name__ == "__main__":
    unittest.main()
