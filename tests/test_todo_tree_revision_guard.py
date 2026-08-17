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
                "reason": (
                    "The proposal has not demonstrated complete requirement coverage."
                ),
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
            "Build all ten ordered stages of the offline city game, including "
            "terrain, roads, zoning, buildings, utilities, traffic, management, "
            "save/load, and final acceptance."
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

    def test_explicit_replan_is_rejected_by_llm_and_preserves_tree(self):
        rejection = {
            "decision": "reject",
            "confidence": "high",
            "reason": (
                "Stages three and four still carry uncovered acceptance requirements."
            ),
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
                "revision_reason": (
                    "Use a shorter execution tree after the latest implementation "
                    "findings."
                ),
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
            "reason": (
                "The merged objective explicitly retains every implementation and "
                "acceptance obligation."
            ),
            "removed_objectives": ["stage two", "stage three", "stage four"],
            "replacement_mapping": [
                {
                    "removed": "stages two through four",
                    "replacement": "combined implementation and acceptance objective",
                    "reason": (
                        "The replacement preserves all three scopes and their checks."
                    ),
                }
            ],
            "requirement_coverage": [
                "rendering, terrain, and roads -> combined implementation and "
                "acceptance objective"
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
                "revision_reason": (
                    "Current module boundaries require one integrated implementation "
                    "transaction."
                ),
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
            session.blackboard["todo_tree_revisions"][-1]["completion_risk"],
            "medium",
        )

    def test_invalid_review_json_fails_closed(self):
        session = self.bare_session("single", ["not-json"])
        session._dispatch_todo_update({"todos": self.stages(3)}, role="developer")
        result = session._dispatch_todo_update(
            {
                "todos": self.stages(1),
                "update_mode": "revise_open",
                "revision_reason": (
                    "Replace the remaining objectives based on a new execution shape."
                ),
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


if __name__ == "__main__":
    unittest.main()
