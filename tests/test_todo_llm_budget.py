"""TodoWrite model-call budget, deterministic fallback and status_update mode.

The model client is a real ``OllamaClient`` with only ``_chat_impl`` (or
``urlopen``) patched, so every count below is taken at the ``chat()`` layer
where the per-TodoWrite budget is enforced.
"""

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import test_todo_tree_revision_guard as fixtures

import Clouds_Coder as cc

AMBIGUOUS = {"intent": "ambiguous", "confidence": "low", "reason": "insufficient evidence"}


def recording_client(responses=None):
    """Real OllamaClient whose transport is replaced by a scripted _chat_impl.

    ``responses`` is consumed in order; an Exception instance is raised, any
    other value is returned as the message content (dicts as JSON).  Without
    a scripted response the classifier-style AMBIGUOUS answer is returned.
    """
    client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
    client.impl_calls = []
    script = list(responses or [])

    def fake_impl(messages, **kwargs):
        client.impl_calls.append({
            "messages": messages,
            "kwargs": kwargs,
            "timeout": round(client._effective_request_timeout(), 3),
        })
        response = script.pop(0) if script else AMBIGUOUS
        if isinstance(response, BaseException):
            raise response
        if not isinstance(response, str):
            response = json.dumps(response, ensure_ascii=False)
        return {"content": response, "thinking": "", "tool_calls": []}

    client._chat_impl = fake_impl
    return client


def count_chat_calls(client):
    """Wrap client.chat to count every call, including budget-denied ones."""
    attempts = {"calls": 0, "denied": 0, "labels": []}
    original = client.chat

    def counted(messages, **kwargs):
        attempts["calls"] += 1
        attempts["labels"].append(kwargs.get("label", ""))
        try:
            return original(messages, **kwargs)
        except cc.TodoLLMBudgetExhausted:
            attempts["denied"] += 1
            raise

    client.chat = counted
    return attempts


def reworded(count):
    return [
        {
            "content": f"第{index}阶段：改写后的目标说明 {index}，补充交付物与验收口径",
            "status": "in_progress" if index == 1 else "pending",
        }
        for index in range(1, count + 1)
    ]


def stored_rows(session):
    return session._todo_route_rows("pure_single", role="developer")


class TodoLLMBudgetTests(unittest.TestCase):
    def setUp(self):
        cc.OllamaClient._endpoint_cooldowns.clear()
        self.fixtures = fixtures.TodoTreeRevisionGuardTests()

    def tearDown(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def seeded_session(self, count):
        session = self.fixtures.bare_session("single")
        session._dispatch_todo_update({"todos": self.fixtures.stages(count)}, role="developer")
        return session

    def test_twelve_reworded_rows_make_at_most_five_model_calls(self):
        session = self.seeded_session(12)
        client = recording_client()
        session.ollama = client
        attempts = count_chat_calls(client)

        result = session._dispatch_todo_update({"todos": reworded(12)}, role="developer")

        # Every reworded id-less row asks the intent classifier, but only
        # five requests reach the transport; the other seven are refused by
        # the budget at the chat() layer and treated as ambiguous.
        self.assertEqual(attempts["calls"], 12)
        self.assertEqual(len(client.impl_calls), 5)
        self.assertEqual(attempts["denied"], 7)
        self.assertEqual(set(attempts["labels"]), {"todo_intent"})
        self.assertTrue(all(call["timeout"] == cc.TODO_LLM_TIMEOUT_SECONDS for call in client.impl_calls))
        self.assertTrue(all(call["kwargs"].get("no_http_retry") for call in client.impl_calls))
        self.assertFalse(str(result).startswith("Error:"))
        # status_update never shortens the tree, and says it kept the rows.
        stored = stored_rows(session)
        self.assertGreaterEqual(len(stored), 12)
        self.assertTrue(all(row["content"] in [r["content"] for r in stored] for row in self.fixtures.stages(12)))
        self.assertIn("omitted row(s) were preserved", result)
        # The scope ends with the TodoWrite: later calls are not limited.
        self.assertFalse(cc.todo_llm_budget_active())
        for _ in range(7):
            client.chat([{"role": "user", "content": "after TodoWrite"}])
        self.assertEqual(len(client.impl_calls), 12)

    def test_budget_and_timeout_restore_after_the_todowrite(self):
        session = self.seeded_session(3)
        client = recording_client()
        session.ollama = client
        session._dispatch_todo_update({"todos": reworded(3)}, role="developer")
        self.assertEqual({call["timeout"] for call in client.impl_calls}, {cc.TODO_LLM_TIMEOUT_SECONDS})
        client.chat([{"role": "user", "content": "main loop"}])
        # Outside the scope the client timeout and normal retries apply.
        self.assertEqual(client.impl_calls[-1]["timeout"], client.timeout)
        self.assertNotIn("no_http_retry", client.impl_calls[-1]["kwargs"])

    def test_worker_text_sync_never_adds_rows_or_calls_the_model(self):
        # Reworded checklist prose in a worker reply is not a request to add
        # work: unmatched rows are dropped before the merge, so no classifier
        # call is made and the tree does not grow.
        session = self.seeded_session(12)
        client = recording_client()
        session.ollama = client
        fixtures.bind(session, "_sync_todos_from_blackboard", lambda self, *args, **kwargs: None)
        fixtures.bind(session, "_blackboard_touch", lambda self, *args, **kwargs: None)
        before = len(session.todo.snapshot())
        text = "\n".join(
            f"[ ] 第{index}阶段：改写后的目标说明 {index}，补充交付物与验收口径" for index in range(1, 13)
        )

        session._blackboard_update_from_worker_step(
            "developer",
            {"status": "tools", "text": text, "tool_results": []},
        )

        self.assertEqual(len(client.impl_calls), 0)
        self.assertEqual(len(session.todo.snapshot()), before)
        self.assertFalse(cc.todo_llm_budget_active())

    def test_status_update_with_evidence_does_not_audit(self):
        session = self.seeded_session(4)
        client = recording_client()
        session.ollama = client
        payload = {
            "todos": [
                {
                    "content": self.fixtures.stages(4)[0]["content"],
                    "status": "completed",
                    "parent_step_id": "stage1",
                },
                {
                    "content": self.fixtures.stages(4)[1]["content"],
                    "status": "in_progress",
                    "parent_step_id": "stage2",
                },
            ],
            "revision_reason": "Stage one passed its integration check.",
            "revision_evidence": ["bash: pytest tests/stage1 -q -> 12 passed"],
        }

        result = session._dispatch_todo_update(payload, role="developer")

        # Before this change a reason/evidence silently upgraded the call to
        # revise_open and ran the LLM audit.  Now it is a plain status merge.
        self.assertEqual(client.impl_calls, [])
        self.assertEqual(session.blackboard["todo_tree_revisions"], [])
        self.assertNotIn("TODO TREE REVISION", result)
        stored = stored_rows(session)
        self.assertEqual(len(stored), 4)
        self.assertEqual(
            [row["status"] for row in stored],
            ["completed", "in_progress", "pending", "pending"],
        )
        # The evidence is recorded on the rows it reports on, nowhere else.
        self.assertEqual(stored[0]["evidence"], "bash: pytest tests/stage1 -q -> 12 passed")
        self.assertEqual(stored[1]["evidence"], "bash: pytest tests/stage1 -q -> 12 passed")
        self.assertNotIn("evidence", stored[2])
        self.assertIn("2 omitted row(s) were preserved", result)

        # A later note never overwrites a completed row's evidence.
        session._dispatch_todo_update(
            {
                "todos": [
                    {**payload["todos"][0], "status": "pending"},
                    {**payload["todos"][1], "status": "completed"},
                ],
                "revision_evidence": ["bash: pytest tests/stage2 -q -> 9 passed"],
            },
            role="developer",
        )
        stored = stored_rows(session)
        self.assertEqual(stored[0]["status"], "completed")
        self.assertEqual(stored[0]["evidence"], "bash: pytest tests/stage1 -q -> 12 passed")
        self.assertEqual(stored[1]["evidence"], "bash: pytest tests/stage2 -q -> 9 passed")
        self.assertEqual(client.impl_calls, [])

    def test_plan_status_update_with_evidence_does_not_audit(self):
        session, step = self.fixtures.plan_session("single")
        client = recording_client()
        session.ollama = client

        result = session._dispatch_todo_update(
            {
                "todos": [
                    {
                        "content": "1.1 检查现有接口",
                        "status": "in_progress",
                        "parent_step_id": step["id"],
                    }
                ],
                "revision_reason": "Interface inspection is still running.",
                "revision_evidence": ["read_file: src/api.py"],
            },
            role="developer",
        )

        self.assertEqual(client.impl_calls, [])
        self.assertEqual(session.blackboard["plan_todo_revisions"], [])
        self.assertNotIn("preserve_current_subplan", result)
        self.assertNotIn("ROLLING SUBPLAN REVISION", result)
        work = [row for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]
        self.assertEqual(len(work), 3)
        self.assertEqual(work[0]["evidence"], "read_file: src/api.py")
        self.assertNotIn("evidence", work[1])

    def safe_root_revision(self):
        # Keeps every current row (same text, so same identity) and adds one.
        rows = [dict(row) for row in self.fixtures.stages(3)]
        rows.append({
            "content": "补充跨模块回归测试并记录通过证据",
            "status": "pending",
            "parent_step_id": "extra-regression",
        })
        return {
            "todos": rows,
            "update_mode": "revise_open",
            "revision_reason": "A cross-module regression check is required by the latest findings.",
        }

    @staticmethod
    def lossy_root_revision(fixture):
        return {
            "todos": fixture.stages(1),
            "update_mode": "revise_open",
            "revision_reason": "Replace the remaining objectives based on a new execution shape.",
        }

    def test_budget_skipped_root_audit_approves_a_safe_revision(self):
        session = self.seeded_session(3)
        client = recording_client()
        session.ollama = client
        # An outer scope that is already used up: the TodoWrite's own scope
        # reuses it, so the audit is refused by the budget.
        with cc.todo_llm_budget_scope(limit=0):
            result = session._dispatch_todo_update(self.safe_root_revision(), role="developer")

        self.assertEqual(client.impl_calls, [])
        self.assertIn("deterministic fallback rule", result)
        self.assertEqual(len(stored_rows(session)), 4)
        audit = session.blackboard["todo_tree_revisions"][-1]
        self.assertEqual(audit["status"], "accepted")
        self.assertIn("semantic review skipped (budget)", audit["review_reason"])

    def test_budget_skipped_root_audit_rejects_unmapped_removal(self):
        session = self.seeded_session(3)
        client = recording_client()
        session.ollama = client
        with cc.todo_llm_budget_scope(limit=0):
            result = session._dispatch_todo_update(self.lossy_root_revision(self.fixtures), role="developer")

        self.assertEqual(client.impl_calls, [])
        self.assertIn("revision rejected", result.lower())
        self.assertEqual(len(stored_rows(session)), 3)
        audit = session.blackboard["todo_tree_revisions"][-1]
        self.assertEqual(audit["status"], "rejected")
        self.assertIn("deterministic fallback rejected", audit["review_reason"])
        self.assertIn("(2) removed open rows need a counterpart", audit["review_reason"])
        self.assertIn("阶段2", audit["review_reason"])
        self.assertIn("阶段3", audit["review_reason"])

    def test_timed_out_root_audit_uses_the_rule_over_the_real_transport(self):
        session = self.seeded_session(3)
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        session.ollama = client
        seen = []

        def timed_out(req, timeout=None):
            seen.append(round(timeout, 3))
            raise TimeoutError("timed out")

        started = time.monotonic()
        with mock.patch.object(cc, "urlopen", side_effect=timed_out):
            rejected = session._dispatch_todo_update(self.lossy_root_revision(self.fixtures), role="developer")
            approved = session._dispatch_todo_update(self.safe_root_revision(), role="developer")

        # One request per audit at the short TodoWrite socket timeout: no
        # HTTP retry, no retry delay and no shared endpoint cooldown.
        self.assertEqual(seen, [cc.TODO_LLM_TIMEOUT_SECONDS] * 2)
        self.assertLess(time.monotonic() - started, 5.0)
        self.assertEqual(cc.OllamaClient._endpoint_cooldowns, {})
        self.assertIn("revision rejected", rejected.lower())
        self.assertIn("deterministic fallback rule", approved)
        revisions = session.blackboard["todo_tree_revisions"]
        self.assertEqual([row["status"] for row in revisions[-2:]], ["rejected", "accepted"])
        self.assertIn("semantic review skipped (timeout)", revisions[-2]["review_reason"])
        self.assertEqual(len(stored_rows(session)), 4)

    def test_fallback_rule_rejects_a_downgraded_completed_row(self):
        session = self.seeded_session(2)
        session._dispatch_todo_update(
            {"todos": [{**self.fixtures.stages(2)[0], "status": "completed"}]},
            role="developer",
        )
        session.ollama = recording_client()
        with cc.todo_llm_budget_scope(limit=0):
            result = session._dispatch_todo_update(
                {
                    "todos": [
                        {**self.fixtures.stages(2)[0], "status": "in_progress"},
                        self.fixtures.stages(2)[1],
                    ],
                    "update_mode": "rework_completed",
                    "revision_reason": "Reopen stage one after the regression report.",
                },
                role="developer",
            )

        self.assertIn("revision rejected", result.lower())
        audit = session.blackboard["todo_tree_revisions"][-1]
        self.assertEqual(audit["status"], "rejected")
        self.assertIn("(1) completed rows must not be removed or downgraded", audit["review_reason"])
        self.assertEqual(stored_rows(session)[0]["status"], "completed")

    def test_invalid_review_json_still_fails_closed(self):
        # Invalid JSON is not a skip: even a revision the deterministic rule
        # would approve stays rejected.
        session = self.seeded_session(3)
        session.ollama = recording_client(["not-json"])
        result = session._dispatch_todo_update(self.safe_root_revision(), role="developer")

        self.assertIn("invalid structured JSON", result)
        self.assertEqual(len(stored_rows(session)), 3)
        audit = session.blackboard["todo_tree_revisions"][-1]
        self.assertEqual(audit["status"], "rejected")
        self.assertNotIn("deterministic fallback", audit["review_reason"])

    def test_provider_error_is_not_a_skip(self):
        session = self.seeded_session(3)
        session.ollama = recording_client([RuntimeError("provider offline")])
        result = session._dispatch_todo_update(self.safe_root_revision(), role="developer")

        self.assertIn("revision rejected", result.lower())
        self.assertIn("semantic review unavailable", result)
        self.assertEqual(len(stored_rows(session)), 3)

    def test_explicit_model_rejection_stays_authoritative(self):
        rejection = {
            "decision": "reject",
            "confidence": "high",
            "reason": "The added regression row duplicates stage three's acceptance.",
            "removed_objectives": [],
            "replacement_mapping": [],
            "requirement_coverage": [],
            "completion_risk": "medium",
            "evidence": [],
        }
        session = self.seeded_session(3)
        session.ollama = recording_client([rejection])
        result = session._dispatch_todo_update(self.safe_root_revision(), role="developer")

        self.assertIn("duplicates stage three", result)
        self.assertEqual(len(stored_rows(session)), 3)
        self.assertNotIn("deterministic fallback", session.blackboard["todo_tree_revisions"][-1]["review_reason"])

    def plan_revision_session(self):
        session, step = self.fixtures.plan_session("single")
        session.blackboard["plan_step_evidence"] = {
            step["id"]: [
                {
                    "id": "ev:plan-revision",
                    "step_id": step["id"],
                    "subtask_id": session._stable_plan_worker_subtask_id(
                        step["id"], {"content": "1.1 检查现有接口"},
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
        return session, step

    def plan_revision(self, step, rows):
        return {
            "todos": [{**row, "parent_step_id": step["id"]} for row in rows],
            "update_mode": "revise_open",
            "revision_reason": "接口检查证明当前子任务需要包含跨模块约束记录。",
            "revision_evidence": ["ev:plan-revision"],
        }

    def test_budget_skipped_plan_audit_approves_a_safe_revision(self):
        session, step = self.plan_revision_session()
        session.ollama = recording_client()
        rows = [
            {"content": "1.1 检查现有接口", "status": "in_progress"},
            {"content": "1.2 实现核心模块", "status": "pending"},
            {"content": "1.3 记录跨模块约束", "status": "pending"},
            {"content": "验收：运行集成测试并记录通过证据", "status": "pending"},
        ]
        with cc.todo_llm_budget_scope(limit=0):
            result = session._dispatch_todo_update(self.plan_revision(step, rows), role="developer")

        self.assertIn("ROLLING SUBPLAN REVISION: accepted by the deterministic fallback rule", result)
        self.assertEqual(session.ollama.impl_calls, [])
        work = [row["content"] for row in session.todo.snapshot() if row.get("parent_step_id") == step["id"]]
        self.assertIn("1.3 记录跨模块约束", work)
        revision = session.blackboard["plan_todo_revisions"][-1]
        self.assertEqual(revision["status"], "accepted")
        self.assertIn("deterministic fallback approved", revision["reason"])

    def test_budget_skipped_plan_audit_rejects_unmapped_removal(self):
        session, step = self.plan_revision_session()
        session.ollama = recording_client()
        before = session.todo.snapshot()
        rows = [
            {"content": "1.1 检查现有接口并记录跨模块约束", "status": "in_progress"},
            {"content": "验收：运行集成测试并记录通过证据", "status": "pending"},
        ]
        with cc.todo_llm_budget_scope(limit=0):
            result = session._dispatch_todo_update(self.plan_revision(step, rows), role="developer")

        self.assertIn("Rolling subplan revision rejected", result)
        self.assertIn("(2) removed open rows need a counterpart", result)
        self.assertIn("1.2 实现核心模块", result)
        self.assertEqual(session.todo.snapshot(), before)
        self.assertEqual(session.blackboard["plan_todo_revisions"][-1]["status"], "rejected")

    def test_indirect_todowrite_helpers_fall_back_when_the_budget_is_used(self):
        session, step = self.fixtures.plan_session("single")
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        session.root = Path(temporary.name)
        session.context_token_upper_bound = 128000
        session.runtime_direct_objective = ""
        session.ollama = recording_client()
        with cc.todo_llm_budget_scope(limit=0) as budget:
            acceptance = session._llm_plan_step_acceptance_subtask(step, ["1.1 检查现有接口"])
            subtasks = session._llm_plan_step_subtasks(step)
            quality = session._llm_review_plan_step_quality(step, {}, session.blackboard)
            judge = session._acceptance_semantic_judge(step, {}, session.blackboard, {})
            contract = session._ensure_plan_step_acceptance_subtask(
                step, ["1.1 检查现有接口", "1.2 实现核心模块"], allow_llm=True,
            )
        # Each helper reached chat(), was refused, and used its own fallback.
        self.assertEqual(budget["denied"], 4)
        self.assertEqual(session.ollama.impl_calls, [])
        self.assertEqual(acceptance, "")
        self.assertEqual(subtasks, [])
        self.assertFalse(quality["available"])
        self.assertFalse(judge["passed"])
        self.assertTrue(session._is_plan_step_acceptance_subtask(contract[-1]))

    def test_skipped_classifiers_and_reviews_are_marked(self):
        session, step = self.fixtures.plan_session("single")
        session.ollama = recording_client()
        with cc.todo_llm_budget_scope(limit=0):
            intent = session._classify_root_todo_intent(
                {"content": "完全改写过的目标"},
                [{"content": "原目标", "status": "pending", "subtask_id": "rt:a"}],
                board=session.blackboard,
            )
            parent = session._classify_plan_worker_parent_update(
                {"content": "实现完整城市系统并记录约束", "_parent_step_inferred": True},
                step,
                board=session.blackboard,
            )
            plan_review = session._semantic_audit_plan_step_updates(
                [], [], ["pt:000"], reason="merge two steps", board=session.blackboard,
            )
        for result in (intent, parent):
            self.assertEqual(result["intent"], "ambiguous")
            self.assertTrue(result["skipped"])
            self.assertEqual(result["skip_reason"], "budget")
        # Multi-step plan edits have no deterministic rule: still fail-closed.
        self.assertFalse(plan_review["available"])
        self.assertFalse(plan_review["approved"])
        self.assertTrue(plan_review["skipped"])
        self.assertIn("budget", plan_review["reason"])

    def test_skip_reason_classification(self):
        self.assertEqual(cc.todo_llm_skip_reason(cc.TodoLLMBudgetExhausted("used")), "budget")
        self.assertEqual(cc.todo_llm_skip_reason(cc.LLMGateBusy("slot busy")), "busy")
        self.assertEqual(cc.todo_llm_skip_reason(TimeoutError("timed out")), "timeout")
        self.assertEqual(cc.todo_llm_skip_reason(cc.OllamaError("HTTP 504: gateway", status=504)), "timeout")
        try:
            try:
                raise TimeoutError("read")
            except TimeoutError as inner:
                raise cc.OllamaError("Connection error: read") from inner
        except cc.OllamaError as wrapped:
            self.assertEqual(cc.todo_llm_skip_reason(wrapped), "timeout")
        self.assertEqual(cc.todo_llm_skip_reason(RuntimeError("provider offline")), "")
        self.assertEqual(cc.todo_llm_skip_reason(ValueError("bad json")), "")

    def test_endpoint_cooldown_skips_instead_of_waiting(self):
        client = recording_client()
        key = client._http_retry_key(client._chat_request_url())
        cc.OllamaClient._endpoint_cooldowns[key] = {"until": time.time() + 120.0}
        started = time.monotonic()
        with cc.todo_llm_budget_scope():
            with self.assertRaises(cc.LLMGateBusy):
                client.chat([{"role": "user", "content": "review"}])
        self.assertLess(time.monotonic() - started, 2.0)
        self.assertEqual(client.impl_calls, [])


if __name__ == "__main__":
    unittest.main()
