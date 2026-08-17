import json
import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class FakeOllama:
    def __init__(self, responses=None):
        self.responses = list(responses or [])
        self.calls = []

    def chat(self, messages, **kwargs):
        self.calls.append({"messages": messages, "kwargs": kwargs})
        response = (
            self.responses.pop(0)
            if self.responses
            else {
                "decision": "reject",
                "confidence": "high",
                "reason": "The proposal has not demonstrated complete requirement coverage.",
                "removed_objectives": [],
                "replacement_mapping": [],
                "requirement_coverage": [],
                "completion_risk": "high",
                "evidence": [],
            }
        )
        if isinstance(response, str):
            return {"content": response}
        return {"content": json.dumps(response, ensure_ascii=False)}


class TodoTreeRevisionGuardTests(unittest.TestCase):
    def bare_session(self, mode="single", responses=None):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.runtime_execution_mode = mode
        session.execution_mode = mode
        session.runtime_assigned_expert = "developer"
        session.active_agent_role = "developer"
        session.runtime_plan_approved = False
        session.runtime_plan_mode_needed = False
        session.runtime_reclassify_required = False
        session.runtime_authoritative_goal = (
            "Build all ten ordered stages of the offline city game, including terrain, roads, "
            "zoning, buildings, utilities, traffic, management, save/load, and final acceptance."
        )
        session.run_generation = 1
        session.messages = []
        session.blackboard = {
            "original_goal": session.runtime_authoritative_goal,
            "task_epoch": 100.0,
            "project_todos": [],
            "todo_tree_baseline": [],
            "todo_tree_revisions": [],
        }
        session.ollama = FakeOllama(responses)
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "_inject_runtime_environment_context", lambda self, text: text)
        return session

    def plan_session(self, mode="single", responses=None):
        session = self.bare_session(mode, responses)
        session.runtime_plan_approved = True
        step_id = "pt:test:todo-guard"
        step = {
            "id": step_id,
            "key": f"bb:proj:{step_id}",
            "content": "实现完整城市系统",
            "full_content": (
                "实现完整城市系统\n"
                "1.1 检查现有接口\n"
                "1.2 实现核心模块\n"
                "验收：运行集成测试并记录通过证据"
            ),
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
            "activated_at": 10.0,
        }
        session.blackboard.update(
            {
                "project_todos": [step],
                "plan_step_total": 1,
                "plan_worker_todos": {},
                "plan_subtask_evidence_bindings": {},
                "plan_step_evidence": {},
                "plan_todo_revisions": [],
            }
        )
        session.todo.update(
            [
                {
                    "key": step["key"],
                    "content": step["content"],
                    "status": "in_progress",
                },
                {
                    "content": "1.1 检查现有接口",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
                {
                    "content": "1.2 实现核心模块",
                    "status": "pending",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
                {
                    "content": "验收：运行集成测试并记录通过证据",
                    "status": "pending",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
            ]
        )
        bind(
            session,
            "_sync_plan_worker_todos_to_blackboard",
            lambda self, *args, **kwargs: True,
        )
        bind(
            session, "_update_plan_file_step_status", lambda self, *args, **kwargs: None
        )
        bind(
            session,
            "_advance_completed_acceptance_after_todo_commit",
            lambda self, *args, **kwargs: False,
        )
        return session, step

    @staticmethod
    def stages(count=10):
        return [
            {
                "content": f"阶段{index} 详细目标 {index}：实现模块 {index} 并完成对应集成验收",
                "status": "in_progress" if index == 1 else "pending",
                "owner": "developer",
                "parent_step_id": f"stage{index}",
            }
            for index in range(1, count + 1)
        ]

    def test_partial_status_snapshots_never_shorten_single_or_sync_tree(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                session._dispatch_todo_update(
                    {"todos": self.stages()}, role="developer"
                )

                partial = [
                    {
                        "content": "阶段1 架构设计与项目骨架",
                        "status": "completed",
                        "owner": "developer",
                        "parent_step_id": "stage1",
                    },
                    {
                        "content": "阶段2 3D 渲染核心",
                        "status": "completed",
                        "owner": "developer",
                        "parent_step_id": "stage2",
                    },
                    {
                        "content": "阶段3 地形系统",
                        "status": "in_progress",
                        "owner": "developer",
                        "parent_step_id": "stage3",
                    },
                ]
                session._dispatch_todo_update({"todos": partial}, role="developer")

                stored = session._todo_route_rows(
                    session._todo_route_kind(role="developer"),
                    role="developer",
                )
                self.assertEqual(len(stored), 10)
                self.assertEqual(
                    [row["status"] for row in stored],
                    ["completed", "completed", "in_progress"] + ["pending"] * 7,
                )
                self.assertIn("详细目标 1", stored[0]["content"])
                self.assertIn("详细目标 2", stored[1]["content"])
                self.assertEqual(len(session.ollama.calls), 0)

    def test_rescue_uses_same_merge_only_guard(self):
        session = self.bare_session("single")
        session._dispatch_todo_update({"todos": self.stages(6)}, role="developer")
        session._todo_write_rescue(
            {
                "todos": [
                    {
                        "content": "阶段1",
                        "status": "completed",
                        "parent_step_id": "stage1",
                    },
                    {
                        "content": "阶段2",
                        "status": "in_progress",
                        "parent_step_id": "stage2",
                    },
                ]
            },
            role="developer",
        )

        stored = session._todo_route_rows("pure_single", role="developer")
        self.assertEqual(len(stored), 6)
        self.assertEqual(
            [row["status"] for row in stored[:3]],
            ["completed", "in_progress", "pending"],
        )
        self.assertEqual(len(session.ollama.calls), 0)

    def test_resume_alias_preserves_omitted_root_rows(self):
        session = self.bare_session("single")
        session._dispatch_todo_update({"todos": self.stages(5)}, role="developer")

        session._dispatch_todo_update(
            {
                "todos": [
                    {
                        "content": "阶段1",
                        "status": "completed",
                        "parent_step_id": "stage1",
                    },
                    {
                        "content": "阶段2",
                        "status": "in_progress",
                        "parent_step_id": "stage2",
                    },
                ]
            },
            role="developer",
            resume=True,
        )

        stored = session._todo_route_rows("pure_single", role="developer")
        self.assertEqual(len(stored), 5)
        self.assertEqual(
            [row["status"] for row in stored],
            ["completed", "in_progress"] + ["pending"] * 3,
        )
        self.assertEqual(len(session.ollama.calls), 0)

    def test_status_update_can_add_work_without_replacing_the_roadmap(self):
        session = self.bare_session("single")
        session._dispatch_todo_update({"todos": self.stages(4)}, role="developer")

        session._dispatch_todo_update(
            {
                "todos": [
                    {
                        "content": "补充跨模块回归测试",
                        "status": "pending",
                        "parent_step_id": "extra-regression",
                    }
                ],
                "update_mode": "status_update",
            },
            role="developer",
        )

        stored = session._todo_route_rows("pure_single", role="developer")
        self.assertEqual(len(stored), 5)
        self.assertEqual(
            [row["content"] for row in stored[:4]],
            [row["content"] for row in self.stages(4)],
        )
        self.assertEqual(stored[-1]["content"], "补充跨模块回归测试")
        self.assertEqual(len(session.ollama.calls), 0)

    def test_stale_todo_transaction_cannot_overwrite_a_newer_tree(self):
        session = self.bare_session("single")
        session._dispatch_todo_update({"todos": self.stages(3)}, role="developer")
        transaction = session._capture_todo_write_transaction(session.blackboard)
        current = session.todo.snapshot()
        session.todo.update(
            current
            + [
                {
                    "content": "并发新增的任务",
                    "status": "pending",
                    "owner": "developer",
                    "subtask_id": "rt:concurrent",
                }
            ]
        )

        result = session._merge_flat_todo_items(
            [{"content": "阶段1", "status": "completed", "parent_step_id": "stage1"}],
            role="developer",
            transaction=transaction,
        )

        self.assertIn("stale_todo_transaction", result)
        self.assertEqual(
            len(session._todo_route_rows("pure_single", role="developer")), 4
        )
        self.assertEqual(session.todo.snapshot()[-1]["content"], "并发新增的任务")

    def test_explicit_replan_is_rejected_by_llm_and_preserves_tree(self):
        rejection = {
            "decision": "reject",
            "confidence": "high",
            "reason": "Stages three and four still carry uncovered acceptance requirements.",
            "removed_objectives": ["阶段3", "阶段4"],
            "replacement_mapping": [],
            "requirement_coverage": ["Stages one and two remain covered"],
            "completion_risk": "high",
            "evidence": ["No completion evidence exists for stages three and four"],
        }
        session = self.bare_session("single", [rejection])
        session._dispatch_todo_update({"todos": self.stages(4)}, role="developer")

        result = session._dispatch_todo_update(
            {
                "todos": self.stages(2),
                "update_mode": "revise_open",
                "revision_reason": "Use a shorter execution tree after the latest implementation findings.",
                "revision_evidence": [
                    "Only stages one and two have observable results"
                ],
            },
            role="developer",
        )

        self.assertIn("revision rejected", result.lower())
        self.assertEqual(
            len(session._todo_route_rows("pure_single", role="developer")), 4
        )
        self.assertEqual(
            session.blackboard["todo_tree_revisions"][-1]["status"], "rejected"
        )
        self.assertIn(
            "uncovered acceptance requirements",
            session.blackboard["todo_tree_revisions"][-1]["review_reason"],
        )

    def test_llm_semantic_decision_is_authoritative_without_local_risk_thresholds(self):
        approval = {
            "decision": "approve",
            "confidence": "medium",
            "reason": "The merged objective explicitly retains every implementation and acceptance obligation.",
            "removed_objectives": ["stage two", "stage three", "stage four"],
            "replacement_mapping": [
                {
                    "removed": "stages two through four",
                    "replacement": "combined implementation and acceptance objective",
                    "reason": "The replacement preserves all three scopes and their checks.",
                }
            ],
            "requirement_coverage": [
                "rendering, terrain, and roads -> combined implementation and acceptance objective"
            ],
            "completion_risk": "medium",
            "evidence": ["The replacement text carries the full obligations"],
        }
        session = self.bare_session("single", [approval])
        session._dispatch_todo_update({"todos": self.stages(4)}, role="developer")
        proposal = [
            {
                "content": "阶段1 详细目标 1：实现模块 1 并完成对应集成验收",
                "status": "completed",
                "parent_step_id": "stage1",
            },
            {
                "content": "合并阶段2至4：完整实现渲染、地形、道路并逐项完成原有集成验收",
                "status": "in_progress",
                "parent_step_id": "stage2-4",
            },
        ]

        result = session._dispatch_todo_update(
            {
                "todos": proposal,
                "update_mode": "revise_open",
                "revision_reason": "Current module boundaries require one integrated implementation transaction.",
                "revision_evidence": [
                    "The modules now share one verified integration boundary"
                ],
            },
            role="developer",
        )

        self.assertIn("accepted after independent LLM", result)
        stored = session._todo_route_rows("pure_single", role="developer")
        self.assertEqual(len(stored), 2)
        self.assertEqual(
            session.blackboard["todo_tree_revisions"][-1]["status"], "accepted"
        )
        self.assertEqual(
            session.blackboard["todo_tree_revisions"][-1]["completion_risk"], "medium"
        )

    def test_invalid_review_json_fails_closed(self):
        session = self.bare_session("single", ["not-json"])
        session._dispatch_todo_update({"todos": self.stages(3)}, role="developer")
        result = session._dispatch_todo_update(
            {
                "todos": self.stages(1),
                "update_mode": "revise_open",
                "revision_reason": "Replace the remaining objectives based on a new execution shape.",
            },
            role="developer",
        )

        self.assertIn("invalid structured JSON", result)
        self.assertEqual(
            len(session._todo_route_rows("pure_single", role="developer")), 3
        )
        self.assertEqual(
            session.blackboard["todo_tree_revisions"][-1]["status"], "rejected"
        )

    def test_plan_status_update_preserves_omitted_subtasks_in_single_and_sync(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session, step = self.plan_session(mode)
                session._dispatch_todo_update(
                    {
                        "todos": [
                            {
                                "content": "1.1 检查现有接口",
                                "status": "in_progress",
                                "parent_step_id": step["id"],
                            }
                        ],
                        "update_mode": "status_update",
                    },
                    role="developer",
                )

                stored = [
                    row
                    for row in session.todo.snapshot()
                    if row.get("parent_step_id") == step["id"]
                ]
                self.assertEqual(len(stored), 3)
                self.assertEqual(
                    [row["content"] for row in stored[:2]],
                    ["1.1 检查现有接口", "1.2 实现核心模块"],
                )
                self.assertTrue(
                    stored[2]["content"].startswith("验收：运行集成测试并记录通过证据")
                )
                self.assertEqual(len(session.ollama.calls), 0)

    def test_plan_structural_revision_always_uses_llm_semantic_review(self):
        response = {
            "approved": True,
            "confidence": "low",
            "reason": "The expanded current subtask preserves the parent step and its acceptance obligation.",
            "unsupported_changes": [],
        }
        session, step = self.plan_session("single", [response])
        session.blackboard["plan_step_evidence"] = {
            step["id"]: [
                {
                    "id": "ev:plan-revision",
                    "step_id": step["id"],
                    "subtask_id": session._stable_plan_worker_subtask_id(
                        step["id"],
                        {"content": "1.1 检查现有接口"},
                    ),
                    "subtask_content": "1.1 检查现有接口",
                    "kind": "runtime",
                    "tool": "read_file",
                    "ok": True,
                    "summary": "接口检查发现还需记录跨模块约束",
                    "ts": 20.0,
                }
            ]
        }

        result = session._dispatch_todo_update(
            {
                "todos": [
                    {
                        "content": "1.1 检查现有接口并记录跨模块约束",
                        "status": "in_progress",
                        "parent_step_id": step["id"],
                    },
                    {
                        "content": "1.2 实现核心模块",
                        "status": "pending",
                        "parent_step_id": step["id"],
                    },
                    {
                        "content": "验收：运行集成测试并记录通过证据",
                        "status": "pending",
                        "parent_step_id": step["id"],
                    },
                ],
                "update_mode": "revise_open",
                "revision_reason": "接口检查证明当前子任务需要包含跨模块约束记录。",
                "revision_evidence": ["ev:plan-revision"],
            },
            role="developer",
        )

        self.assertIn("ROLLING SUBPLAN REVISION: accepted", result)
        self.assertEqual(len(session.ollama.calls), 1)
        self.assertEqual(
            session.blackboard["plan_todo_revisions"][-1]["status"], "accepted"
        )


if __name__ == "__main__":
    unittest.main()
