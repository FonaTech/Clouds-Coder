import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class PlanTodoProgressionTests(unittest.TestCase):
    def bare_session(self, mode="sync"):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.runtime_execution_mode = mode
        session.execution_mode = mode
        session.runtime_assigned_expert = "developer"
        session.active_agent_role = "developer"
        session.runtime_plan_approved = True
        session.runtime_plan_mode_needed = False
        session.runtime_reclassify_required = False
        session.blackboard = {}
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "_inject_runtime_environment_context", lambda self, text: text)
        return session

    def test_visual_acceptance_without_browser_requests_semantic_review(self):
        acceptance = (
            "验收：在浏览器打开页面，画面可见、canvas 已渲染且控制台无报错；"
            "证据：截图与 runtime 输出。"
        )
        expected = "runtime/test/build/browser execution evidence"
        shell_record = {
            "kind": "runtime",
            "tool": "bash",
            "ok": True,
            "exit_code": 0,
            "command": "grep WebGLRenderer index.html",
            "summary": "WebGLRenderer found",
        }
        browser_record = {
            "kind": "runtime",
            "tool": "chrome",
            "ok": True,
            "exit_code": None,
            "command": "open http://127.0.0.1:8123",
            "summary": "status 200; screenshot page.png; canvas webgl rendered visible; image/png",  # noqa: E501
        }

        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                missing = session._evaluate_acceptance_evidence_records(
                    [shell_record], expected, acceptance_text=acceptance
                )
                passed = session._evaluate_acceptance_evidence_records(
                    [shell_record, browser_record], expected, acceptance_text=acceptance
                )

                self.assertFalse(missing["passed"])
                self.assertEqual(
                    missing["reason"], "visual-runtime-needs-semantic-review"
                )
                self.assertTrue(missing["semantic_review_required"])
                self.assertTrue(passed["passed"])
                self.assertEqual(passed["matched_records"], [browser_record])

    def test_plan_single_prompt_requires_evidence_backed_batch_todo_sync(self):
        session = self.bare_session("single")
        step_id = "pt:test:todo-sync"
        session.blackboard = {
            "project_todos": [
                {
                    "id": step_id,
                    "key": "bb:proj:" + step_id,
                    "content": "计算石墨烯透过率并绘图",
                    "full_content": "计算石墨烯透过率并绘图",
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
            ],
            "plan_step_total": 1,
        }
        session.todo.update(
            [
                {
                    "content": "检查 Python/numpy/matplotlib 环境可用性",
                    "status": "completed",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
                {
                    "content": "验证 Kubo 公式与透过率数值",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
                {
                    "content": "编写正式绘图脚本",
                    "status": "pending",
                    "owner": "developer",
                    "parent_step_id": step_id,
                },
            ]
        )

        prompt = session._plan_todo_discipline_prompt(role="developer")

        self.assertIn("Current in_progress subtask: 验证 Kubo 公式与透过率数值", prompt)
        self.assertIn("1 completed, 1 pending", prompt)
        self.assertIn("update_mode='status_update'", prompt)
        self.assertIn("update them together in one call", prompt)
        self.assertIn("do not close ordinary work rows by themselves", prompt)
        self.assertNotIn("phase_bias=", prompt)
        self.assertNotIn("next_action=", prompt)

    def test_decorated_validation_heading_rebinds_stale_todo_evidence(self):
        session = self.bare_session()
        step = {"id": "pt:test:000", "activated_at": 10.0}
        old_row = {"content": "1.2 创建 index.html", "parent_step_id": step["id"]}
        target_row = {
            "content": "1.3 初始化场景 scene、相机 camera、WebGLRenderer 与 Fog",
            "parent_step_id": step["id"],
        }
        old_id = session._stable_plan_worker_subtask_id(step["id"], old_row)
        target_id = session._stable_plan_worker_subtask_id(step["id"], target_row)
        session.blackboard = {
            "plan_step_evidence": {
                step["id"]: [
                    {
                        "id": "ev:cross-row",
                        "step_id": step["id"],
                        "subtask_id": old_id,
                        "subtask_content": old_row["content"],
                        "kind": "runtime",
                        "tool": "bash",
                        "ok": True,
                        "exit_code": 0,
                        "ts": 20.0,
                        "command": "grep index.html",
                        "summary": (
                            "=== 1.2+1.3 内容断言 === new THREE.Scene "
                            "new THREE.PerspectiveCamera new THREE.WebGLRenderer new THREE.Fog OK"),  # noqa: E501
                    }]}}

        records = session._plan_subtask_evidence_records(
            step,
            target_row["content"],
            board=session.blackboard,
            subtask_id=target_id,
            since_ts=10.0,
        )

        self.assertEqual([record["id"] for record in records], ["ev:cross-row"])

    def test_status_update_commits_supported_rows_and_keeps_acceptance_open(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                step_id = "pt:test:000"
                step = {
                    "id": step_id,
                    "key": "bb:proj:" + step_id,
                    "content": "1. 初始化场景",
                    "full_content": (
                        "1. 初始化场景\n1.1 创建目录\n1.2 创建 index.html\n"
                        "1.3 初始化 WebGLRenderer\n"
                        "验收：在浏览器打开页面，画面可见且控制台无报错"
                    ),
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                session.blackboard = {
                    "project_todos": [step],
                    "plan_step_total": 1,
                    "plan_subtask_evidence_bindings": {},
                }
                bind(
                    session,
                    "_sync_plan_worker_todos_to_blackboard",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_update_plan_file_step_status",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_plan_worker_completion_has_evidence",
                    lambda self, plan_step, row, **kwargs: (
                        not self._is_plan_step_acceptance_subtask(
                            row.get("content", "")
                        )
                    ),
                )
                bind(
                    session,
                    "_plan_worker_completion_evidence_records",
                    lambda self, plan_step, row, **kwargs: [
                        {
                            "id": "ev:"
                            + self._stable_plan_worker_subtask_id(plan_step["id"], row),
                            "step_id": plan_step["id"],
                            "kind": "runtime",
                            "tool": "bash",
                            "ok": True,
                            "exit_code": 0,
                            "summary": "verified",
                            "ts": 20.0,
                        }
                    ],
                )
                rows = [{"key": step["key"],
                         "content": step["content"],
                         "status": "in_progress",
                         },
                        {"content": "1.1 创建目录",
                         "status": "completed",
                         "owner": "developer",
                         "parent_step_id": step_id,
                         "subtask_id": f"pst:{step_id}:a",
                         "created_at": 10.0,
                         },
                        {"content": "1.2 创建 index.html",
                         "status": "in_progress",
                         "owner": "developer",
                         "parent_step_id": step_id,
                         "subtask_id": f"pst:{step_id}:b",
                         "created_at": 10.0,
                         },
                        {"content": "1.3 初始化 WebGLRenderer",
                         "status": "pending",
                         "owner": "reviewer",
                         "parent_step_id": step_id,
                         "subtask_id": f"pst:{step_id}:c",
                         "created_at": 10.0,
                         },
                        {"content": "验收：在浏览器打开页面，画面可见且控制台无报错；证据：screenshot/canvas runtime evidence",  # noqa: E501
                         "status": "pending",
                         "owner": "reviewer",
                         "parent_step_id": step_id,
                         "subtask_id": f"pst:{step_id}:acceptance",
                         "created_at": 10.0,
                         },
                        ]
                session.todo.update(rows)
                incoming = [
                    {
                        "content": row["content"],
                        "status": "completed",
                        "owner": "reviewer",
                        "parent_step_id": step_id,
                        "subtask_id": row.get("subtask_id", ""),
                    }
                    for row in rows[1:]
                ]

                result = session._dispatch_todo_update(
                    {
                        "todos": incoming,
                        # Older providers still send a cursor. It must not
                        # override the explicit statuses in this snapshot.
                        "in_progress_index": 2,
                        "update_mode": "status_update",
                    },
                    role="reviewer",
                )
                stored = [
                    row for row in session.todo.snapshot() if row.get("parent_step_id")
                ]

                self.assertEqual(
                    [row["status"] for row in stored[:-1]], ["completed"] * 3
                )
                self.assertEqual(stored[-1]["status"], "in_progress")
                if mode == "single":
                    self.assertEqual(stored[1]["owner"], "reviewer")
                    self.assertEqual(stored[2]["owner"], "reviewer")
                else:
                    self.assertEqual(stored[1]["owner"], "developer")
                    self.assertEqual(stored[2]["owner"], "reviewer")
                self.assertIn("STATUS EVIDENCE AUDIT", result)

    def test_explicit_batch_status_snapshot_is_not_overridden_by_cursor(self):
        """A legacy cursor must not turn a batch snapshot back into one active row."""
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                items = [
                    {"content": "1.1 first", "status": "completed"},
                    {"content": "1.2 second", "status": "completed"},
                    {"content": "1.3 current", "status": "pending"},
                ]
                result = session._apply_todo_payload_in_progress_index(
                    items,
                    {"in_progress_index": 2},
                )

                self.assertEqual(
                    [row["status"] for row in result],
                    ["completed", "completed", "pending"],
                )

    def test_legacy_cursor_still_selects_pending_row_without_explicit_status(self):
        session = self.bare_session("sync")
        result = session._apply_todo_payload_in_progress_index(
            ["first", "second", "third"],
            {"in_progress_index": 1},
        )

        self.assertEqual(
            [row["status"] for row in result],
            ["pending", "in_progress", "pending"],
        )

    def test_stale_todowrite_is_discarded_after_active_step_changes(self):
        session = self.bare_session("sync")
        session.run_generation = 7
        step_one = {
            "id": "pt:test:001",
            "key": "bb:proj:pt:test:001",
            "content": "1. 第一阶段",
            "full_content": "1. 第一阶段\n1.1 当前工作\n验收：运行检查并记录证据",
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
            "activated_at": 10.0,
        }
        step_two = {
            "id": "pt:test:002",
            "key": "bb:proj:pt:test:002",
            "content": "2. 第二阶段",
            "full_content": "2. 第二阶段\n2.1 后续工作\n验收：运行检查并记录证据",
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 1,
            "activated_at": 20.0,
        }
        session.blackboard = {
            "task_epoch": 11.0,
            "status": "CODING",
            "approval": {"approved": False},
            "completion": {"state": "working"},
            "project_todos": [step_one, step_two],
            "plan_step_total": 2,
        }
        session.todo.update(
            [
                {
                    "content": "1.1 当前工作",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_one["id"],
                }
            ]
        )
        transaction = session._capture_todo_write_transaction(
            session.blackboard,
            active_step_id=step_one["id"],
        )
        # This is the state transition that happened while the old TodoWrite
        # thread was still doing its slow audit.
        step_one["status"] = "completed"
        session.blackboard["plan_step_cursor"] = 1
        session.blackboard["project_todos"] = [step_one, step_two]

        before = session.todo.snapshot()
        result = session._merge_plan_worker_todo_items(
            [
                {
                    "content": "1.1 当前工作",
                    "status": "completed",
                    "owner": "developer",
                    "parent_step_id": step_one["id"],
                }
            ],
            role="developer",
            transaction=transaction,
        )

        self.assertIn("stale_todo_transaction", result)
        self.assertEqual(session.todo.snapshot(), before)

    def test_stale_todowrite_cannot_reopen_completed_run(self):
        session = self.bare_session("sync")
        session.run_generation = 3
        step = {
            "id": "pt:test:001",
            "key": "bb:proj:pt:test:001",
            "content": "1. 已完成步骤",
            "full_content": "1. 已完成步骤\n1.1 工作\n验收：运行检查并记录证据",
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
            "activated_at": 10.0,
        }
        session.blackboard = {
            "task_epoch": 11.0,
            "status": "CODING",
            "approval": {"approved": False},
            "completion": {"state": "working"},
            "project_todos": [step],
            "plan_step_total": 1,
        }
        transaction = session._capture_todo_write_transaction(
            session.blackboard,
            active_step_id=step["id"],
        )
        session.blackboard["status"] = "COMPLETED"
        session.blackboard["approval"] = {"approved": True}
        session.blackboard["completion"] = {"state": "completed"}
        before = session.todo.snapshot()

        result = session._merge_plan_worker_todo_items(
            [
                {
                    "content": "1.1 工作",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step["id"],
                }
            ],
            role="developer",
            transaction=transaction,
        )

        self.assertIn("stale_todo_transaction", result)
        self.assertEqual(session.todo.snapshot(), before)

    def test_sync_worker_does_not_dispatch_after_terminal_state(self):
        session = self.bare_session("sync")
        session.blackboard = {
            "status": "COMPLETED",
            "approval": {"approved": True},
            "completion": {"state": "completed"},
            "project_todos": [],
        }
        events = []
        bind(
            session,
            "_emit",
            lambda self, *args, **kwargs: events.append((args, kwargs)),
        )

        session._multi_agent_sync_blackboard_worker(pinned_selection="")

        self.assertFalse(
            any(args and args[0] == "manager_delegate" for args, _ in events)
        )
        self.assertTrue(
            any(
                "already finished" in str(args[1] if len(args) > 1 else "")
                for args, _ in events
            )
        )

    def test_provisional_approval_is_not_treated_as_terminal_sync_completion(self):
        session = self.bare_session("sync")
        self.assertFalse(
            session._blackboard_is_terminal_completion(
                {
                    "status": "COMPLETED",
                    "approval": {"approved": True},
                    "completion": {"state": "blocked"},
                }
            )
        )

    def test_single_finish_gate_counts_developer_owned_todos(self):
        session = self.bare_session("single")
        session.runtime_plan_approved = False
        session.blackboard = {
            "status": "CODING",
            "project_todos": [],
            "task_profile": {
                "task_type": "engineering",
                "execution_mode": "single",
                "assigned_expert": "developer",
            },
            "completion": {"state": "working"},
        }
        session.todo.update(
            [
                {
                    "content": "阶段8 城市管理与 UI",
                    "status": "in_progress",
                    "owner": "developer",
                },
                {
                    "content": "阶段9 存档与读档",
                    "status": "pending",
                    "owner": "developer",
                },
            ]
        )
        bind(
            session,
            "_can_auto_finish_from_approval",
            lambda self, *args, **kwargs: (True, "ok"),
        )
        bind(session, "_manager_has_error_log", lambda self, *args, **kwargs: False)

        rows = session._completion_scoped_open_todo_rows(session.blackboard)
        gate = session._evaluate_finish_gate(session.blackboard)

        self.assertEqual(len(rows), 2)
        self.assertFalse(gate["ok"])
        self.assertEqual(gate["reason"], "worker-todo-pending:2")

    def test_run_summary_is_not_generated_for_unfinished_run_boundary(self):
        session = self.bare_session("single")
        session.cancel_requested = False
        session.runtime_plan_approved = False
        session.runtime_plan_proposal = {}
        session.messages = []
        session.blackboard = {
            "status": "PAUSED",
            "project_todos": [],
            "completion": {"state": "blocked"},
        }

        session._generate_run_completion_summary()

        self.assertEqual(session.messages, [])

    def test_sync_review_gate_routes_validation_to_developer(self):
        session = self.bare_session("sync")
        route = session._finish_gate_route_for_reason(
            "sync-review-missing",
            {
                "status": "CODING",
                "task_profile": {"assigned_expert": "developer"},
                "project_todos": [],
            },
        )

        self.assertEqual(route["target"], "developer")
        self.assertIn("validation", route["instruction"].lower())

    def test_reviewer_role_policy_error_is_not_a_product_blocker(self):
        session = self.bare_session("sync")
        self.assertFalse(
            session._execution_log_entry_is_blocking_error(
                {
                    "actor": "reviewer",
                    "tool": "bash",
                    "content": (
                        "tool_error bash: Error: shell mutation is not allowed for read-only agent role 'reviewer'"  # noqa: E501
                    ),
                }
            )
        )

    def test_blackboard_sync_nests_workers_below_parent_in_roadmap_order(self):
        session = self.bare_session("sync")
        parents = [
            {"key": "bb:proj:pt:000", "content": "1. 已完成", "status": "completed"},
            {
                "key": "bb:proj:pt:001",
                "content": "2. 当前步骤",
                "status": "in_progress",
            },
            {"key": "bb:proj:pt:002", "content": "3. 后续步骤", "status": "pending"},
        ]
        workers = [
            {
                "content": "2.1 当前子任务",
                "status": "in_progress",
                "owner": "developer",
                "parent_step_id": "pt:001",
            }
        ]
        session.todo.update(parents + workers)
        session.blackboard = {"plan": {"phase": ""}, "project_todos": []}
        bind(session, "_todo_route_kind", lambda self, board=None: "plan_sync")
        bind(session, "_init_project_todos", lambda self, board: None)
        bind(session, "_update_project_todo_status", lambda self, board: None)
        bind(
            session,
            "_todo_project_rows_from_blackboard",
            lambda self, board: list(parents),
        )
        bind(
            session,
            "_todo_route_rows",
            lambda self, route_kind, rows=None, role="", board=None: list(workers),
        )
        bind(session, "_filter_plan_fragment_todo_rows", lambda self, rows: list(rows))

        session._sync_todos_from_blackboard(reason="dummy", board=session.blackboard)

        self.assertEqual(
            [row["content"] for row in session.todo.snapshot()],
            ["1. 已完成", "2. 当前步骤", "2.1 当前子任务", "3. 后续步骤"],
        )

    def test_manager_route_is_anchored_to_global_current_subtask(self):
        session = self.bare_session("sync")
        step = {
            "id": "pt:test:000",
            "content": "1. 初始化场景",
            "full_content": "1. 初始化场景\n1.1 创建目录\n1.2 创建 index.html",
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
        }
        session.blackboard = {"project_todos": [step], "plan_step_total": 2}
        bind(
            session,
            "_current_plan_worker_subtask_snapshot",
            lambda self, board=None, role="": {
                "step_id": step["id"],
                "subtask_id": "pst:test:current",
                "subtask_content": "1.2 创建 index.html",
            },
        )
        bind(
            session,
            "_route_focus_fields",
            lambda self, board=None: {
                "focus_kind": "plan_step",
                "focus_id": step["id"],
            },
        )
        bind(
            session,
            "_plan_subtask_route_fields",
            lambda self, board=None, role="": {
                "plan_subtask_id": "pst:test:current",
                "plan_subtask_content": "1.2 创建 index.html",
            },
        )

        route = session._align_route_with_current_plan_step(
            {"target": "developer", "instruction": "Step 2: build future mountains"},
            session.blackboard,
        )

        self.assertIn("Canonical current subtask", route["instruction"])
        self.assertIn("1.2 创建 index.html", route["instruction"])
        self.assertNotIn("future mountains", route["instruction"])

    def test_generic_evidence_shape_is_not_an_artifact_assertion(self):
        session = self.bare_session()
        text = "Acceptance: run browser runtime and record screenshot/canvas evidence"
        self.assertEqual(session._extract_plan_step_referenced_paths(text, limit=8), [])
        self.assertEqual(session._acceptance_assertion_terms(text), [])
        self.assertTrue(session._acceptance_requires_browser_evidence(text))

    def test_semantic_acceptance_can_resolve_visual_tool_shape_ambiguity(self):
        session = self.bare_session("sync")
        step = {
            "id": "pt:visual:000",
            "content": "1. 浏览器场景",
            "full_content": "1. 浏览器场景\n验收：浏览器画面可见且 canvas 正常渲染",
            "activated_at": 10.0,
        }
        acceptance = {
            "content": "验收：浏览器画面可见且 canvas 正常渲染",
            "parent_step_id": step["id"],
            "created_at": 10.0,
        }
        session.blackboard = {"plan_step_evidence": {}}
        trusted = session._record_trusted_plan_step_acceptance_event(
            step,
            acceptance,
            evidence="semantic audit says pass",
            actor="reviewer",
            source="semantic_verified",
        )

        self.assertTrue(trusted)
        self.assertEqual(
            [
                row["id"]
                for row in session._trusted_plan_step_acceptance_records(
                    step, acceptance, board=session.blackboard, since_ts=10.0
                )
            ],
            [trusted["id"]],
        )

        browser = {
            "id": "ev:browser",
            "step_id": step["id"],
            "subtask_id": session._stable_plan_worker_subtask_id(
                step["id"],
                acceptance),
            "subtask_content": acceptance["content"],
            "kind": "runtime",
            "tool": "chrome",
            "ok": True,
            "exit_code": None,
            "command": "open http://127.0.0.1:8123",
            "summary": "status 200; screenshot page.png; canvas webgl rendered visible; image/png",  # noqa: E501
            "ts": trusted["ts"] + 0.01,
        }
        session.blackboard["plan_step_evidence"][step["id"]].append(browser)
        self.assertEqual(
            [
                row["id"]
                for row in session._trusted_plan_step_acceptance_records(
                    step, acceptance, board=session.blackboard, since_ts=10.0
                )
            ],
            [trusted["id"]],
        )

    def test_hardcoded_subtask_match_failure_uses_cached_llm_evidence_audit(self):
        class FakeOllama:
            def __init__(self):
                self.calls = 0

            def chat(self, *args, **kwargs):
                self.calls += 1
                return {
                    "content": (
                        '{"decision":"pass","passed":true,"confidence":"high",'
                        '"reason":"equivalent generated module satisfies the requested entry",'  # noqa: E501
                        '"evidence":"ev:equivalent created and syntax checked",'
                        '"evidence_ids":["ev:equivalent"]}')}

        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                session.ollama = FakeOllama()
                session.messages = []
                session.runtime_direct_objective = ""
                step_id = "pt:semantic:000"
                step = {
                    "id": step_id,
                    "content": "1. 初始化模块",
                    "full_content": "1. 初始化模块\n1.1 创建 src/expected-entry.js",
                    "activated_at": 10.0,
                }
                row = {
                    "content": "1.1 创建 src/expected-entry.js",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                subtask_id = session._stable_plan_worker_subtask_id(step_id, row)
                session.blackboard = {
                    "plan_step_evidence": {
                        step_id: [
                            {
                                "id": "ev:equivalent",
                                "step_id": step_id,
                                "subtask_id": "pst:old-binding",
                                "subtask_content": "create an equivalent generated entry",  # noqa: E501
                                "kind": "file",
                                "tool": "write_file",
                                "ok": True,
                                "exit_code": None,
                                "path": "src/generated-entry.js",
                                "summary": "generated entry module created; syntax check passed",  # noqa: E501
                                "ts": 20.0,
                            }]}}

                self.assertFalse(
                    session._plan_subtask_has_accumulated_evidence(
                        step,
                        row["content"],
                        board=session.blackboard,
                        subtask_id=subtask_id,
                        since_ts=10.0,
                    )
                )
                self.assertTrue(
                    session._plan_worker_completion_has_evidence(
                        step,
                        row,
                        board=session.blackboard,
                        subtask_id=subtask_id,
                        since_ts=10.0,
                    )
                )
                self.assertTrue(
                    session._plan_worker_completion_has_evidence(
                        step,
                        row,
                        board=session.blackboard,
                        subtask_id=subtask_id,
                        since_ts=10.0,
                    )
                )
                self.assertEqual(session.ollama.calls, 1)
                self.assertEqual(
                    [
                        record["id"]
                        for record in session._plan_worker_completion_evidence_records(
                            step,
                            row,
                            board=session.blackboard,
                            subtask_id=subtask_id,
                            since_ts=10.0,
                        )
                    ],
                    ["ev:equivalent"],
                )

    def test_llm_subtask_audit_does_not_pass_without_real_evidence(self):
        session = self.bare_session("sync")
        step = {"id": "pt:none:000", "content": "1. 初始化", "activated_at": 10.0}
        row = {"content": "1.1 创建 src/main.js", "created_at": 10.0}
        session.blackboard = {"plan_step_evidence": {step["id"]: []}}

        self.assertFalse(
            session._plan_worker_completion_has_evidence(
                step,
                row,
                board=session.blackboard,
                since_ts=10.0,
            )
        )

    def test_llm_subtask_audit_cannot_turn_failed_record_into_completion(self):
        class OveroptimisticOllama:
            def chat(self, *args, **kwargs):
                return {
                    "content": (
                        '{"decision":"pass","passed":true,"confidence":"high",'
                        '"reason":"claimed pass","evidence":"failed record",'
                        '"evidence_ids":["ev:failed"]}'
                    )
                }

        session = self.bare_session("single")
        session.ollama = OveroptimisticOllama()
        step = {"id": "pt:failed:000", "content": "1. 初始化", "activated_at": 10.0}
        row = {"content": "1.1 验证 src/main.js", "created_at": 10.0}
        session.blackboard = {
            "plan_step_evidence": {
                step["id"]: [
                    {
                        "id": "ev:failed",
                        "step_id": step["id"],
                        "kind": "runtime",
                        "tool": "bash",
                        "ok": False,
                        "exit_code": 1,
                        "command": "node --check src/main.js",
                        "summary": "SyntaxError",
                        "ts": 20.0,
                    }
                ]
            }
        }

        self.assertFalse(
            session._plan_worker_completion_has_evidence(
                step,
                row,
                board=session.blackboard,
                since_ts=10.0,
            )
        )

    def test_sync_role_policy_failure_does_not_override_decisive_browser_pass(self):
        acceptance = "验收：浏览器打开 index.html 可见 canvas 场景且控制台无报错"
        browser_pass = {
            "id": "ev:browser-pass",
            "kind": "runtime",
            "tool": "bash",
            "ok": True,
            "exit_code": 0,
            "command": "chrome --headless http://127.0.0.1:8765/index.html",
            "summary": "CHROME_EXIT=0 canvas width=756 height=469 ERROR_COUNT=0 ACCEPTANCE=PASS",  # noqa: E501
            "ts": 20.0,
        }
        role_policy_failure = {
            "id": "ev:role-policy",
            "kind": "runtime",
            "tool": "bash",
            "ok": False,
            "exit_code": -1,
            "command": "chrome --headless index.html > probe.txt",
            "summary": (
                "Error: shell mutation is not allowed for read-only agent role 'reviewer'. "  # noqa: E501
                "Use read/search/validation commands only."),
            "ts": 21.0,
        }

        session = self.bare_session("sync")
        result = session._evaluate_acceptance_evidence_records(
            [browser_pass, role_policy_failure],
            "runtime/test/build/browser execution evidence",
            acceptance_text=acceptance,
        )

        self.assertTrue(result["passed"])
        self.assertEqual(
            [row["id"] for row in result["matched_records"]], ["ev:browser-pass"]
        )

    def test_unrelated_failed_probe_does_not_override_decisive_browser_pass(self):
        acceptance = "验收：浏览器打开 index.html 可见 canvas 场景且控制台无报错"
        browser_pass = {
            "id": "ev:browser-pass",
            "kind": "runtime",
            "tool": "bash",
            "ok": True,
            "exit_code": 0,
            "command": "chrome --headless http://127.0.0.1:8765/index.html",
            "summary": "CHROME_EXIT=0 canvas visible ERROR_COUNT=0 ACCEPTANCE=PASS",
            "ts": 20.0,
        }
        unrelated_probe = {
            "id": "ev:probe-failed",
            "kind": "runtime",
            "tool": "bash",
            "ok": False,
            "exit_code": 1,
            "command": "node orbitcontrols_probe.js",
            "summary": "ReferenceError: EventDispatcher is not defined",
            "ts": 21.0,
        }

        session = self.bare_session("sync")
        result = session._evaluate_acceptance_evidence_records(
            [browser_pass, unrelated_probe],
            "runtime/test/build/browser execution evidence",
            acceptance_text=acceptance,
        )

        self.assertTrue(result["passed"])

    def test_later_real_acceptance_failure_still_overrides_prior_pass(self):
        acceptance = "验收：浏览器打开 index.html 可见 canvas 场景且控制台无报错"
        records = [
            {
                "id": "ev:pass",
                "kind": "runtime",
                "tool": "bash",
                "ok": True,
                "exit_code": 0,
                "command": "chrome --headless http://127.0.0.1:8765/index.html",
                "summary": "canvas visible ERROR_COUNT=0 ACCEPTANCE=PASS",
                "ts": 20.0,
            },
            {
                "id": "ev:real-fail",
                "kind": "runtime",
                "tool": "bash",
                "ok": False,
                "exit_code": 1,
                "command": "python browser_acceptance_test.py index.html",
                "summary": "ACCEPTANCE=FAIL canvas missing; ERROR_COUNT=1",
                "ts": 21.0,
            },
        ]

        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                result = session._evaluate_acceptance_evidence_records(
                    records,
                    "runtime/test/build/browser execution evidence",
                    acceptance_text=acceptance,
                )
                self.assertFalse(result["passed"])
                self.assertEqual(result["reason"], "latest-runtime-check-failed")

    def test_acceptance_todowrite_uses_one_cached_semantic_audit(self):
        class FakeOllama:
            def __init__(self):
                self.calls = 0

            def chat(self, *args, **kwargs):
                self.calls += 1
                return {
                    "content": (
                        '{"decision":"pass","passed":true,"confidence":"high",'
                        '"reason":"runtime metrics prove the requested state transition",'  # noqa: E501
                        '"missing":[],"next_actions":[],"evidence":'
                        '["STATE_CHANGE_COUNT=11","RUNTIME_ERROR_COUNT=0"]}')}

        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                session.ollama = FakeOllama()
                session.messages = []
                session.runtime_direct_objective = ""
                step_id = f"pt:{mode}:acceptance"
                step = {
                    "id": step_id,
                    "key": "bb:proj:" + step_id,
                    "content": "1. Runtime feature",
                    "full_content": (
                        "1. Runtime feature\n1.1 implement feature\n"
                        "验收：在浏览器中目标组件呈现预期状态变化；运行时编译无错误"
                    ),
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                work = {
                    "content": "1.1 implement feature",
                    "status": "completed",
                    "owner": "developer",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                    "completed_at": 18.0,
                }
                acceptance_row = {
                    "content": "验收：在浏览器中目标组件呈现预期状态变化；运行时编译无错误",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                    "started_at": 19.0,
                }
                session.blackboard = {
                    "project_todos": [step],
                    "plan_step_total": 1,
                    "plan_step_evidence": {
                        step_id: [
                            {
                                "id": "ev:ink-runtime",
                                "step_id": step_id,
                                "kind": "runtime",
                                "tool": "bash",
                                "ok": True,
                                "exit_code": 0,
                                "command": "python verify_runtime_behavior.py",
                                "summary": (
                                    "STATE_CHANGE_COUNT=11 RUNTIME_ERROR_COUNT=0"
                                ),
                                "ts": 20.0,
                            }
                        ],
                    },
                    "plan_subtask_evidence_bindings": {},
                }
                session.todo.update(
                    [
                        {
                            "key": step["key"],
                            "content": step["content"],
                            "status": "in_progress",
                        },
                        work,
                        acceptance_row,
                    ]
                )
                bind(
                    session,
                    "_sync_plan_worker_todos_to_blackboard",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_update_plan_file_step_status",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_advance_completed_acceptance_after_todo_commit",
                    lambda self, *args, **kwargs: False,
                )
                incoming = [
                    {**work, "status": "completed"},
                    {**acceptance_row, "status": "completed"},
                ]

                session._merge_plan_worker_todo_items(
                    incoming,
                    role="developer",
                    update_mode="status_update",
                )
                first = [
                    row
                    for row in session.todo.snapshot()
                    if row.get("parent_step_id") == step_id
                    and session._is_plan_step_acceptance_subtask(row.get("content", ""))
                ][-1]
                self.assertEqual(first["status"], "completed")
                self.assertTrue(
                    session._trusted_plan_step_acceptance_records(
                        step,
                        first,
                        board=session.blackboard,
                        since_ts=10.0,
                    )
                )
                self.assertEqual(session.ollama.calls, 1)

                session._plan_worker_completion_has_evidence(
                    step,
                    first,
                    board=session.blackboard,
                    since_ts=10.0,
                )
                self.assertEqual(session.ollama.calls, 1)

    def test_semantic_verify_keeps_acceptance_open(self):
        class VerifyOllama:
            def chat(self, *args, **kwargs):
                return {
                    "content": (
                        '{"decision":"verify","passed":false,"confidence":"high",'
                        '"reason":"one direct observation is still missing",'
                        '"missing":["runtime behavior"],"next_actions":["run focused check"],'  # noqa: E501
                        '"evidence":[]}')}

        session = self.bare_session("single")
        session.ollama = VerifyOllama()
        session.messages = []
        session.runtime_direct_objective = ""
        step_id = "pt:verify:acceptance"
        step = {
            "id": step_id,
            "content": "1. Runtime behavior",
            "full_content": "1. Runtime behavior\n1.1 build\n验收：runtime behavior is visible",  # noqa: E501
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
            "activated_at": 10.0,
        }
        work = {
            "content": "1.1 build",
            "status": "completed",
            "owner": "developer",
            "parent_step_id": step_id,
        }
        acceptance_row = {
            "content": "验收：在浏览器确认 runtime behavior is visible",
            "status": "in_progress",
            "owner": "developer",
            "parent_step_id": step_id,
        }
        step["full_content"] = (
            "1. Runtime behavior\n1.1 build\n验收：在浏览器确认 runtime behavior is visible"
        )
        session.todo.update([work, acceptance_row])
        session.blackboard = {
            "project_todos": [step],
            "plan_step_evidence": {
                step_id: [
                    {
                        "id": "ev:candidate",
                        "step_id": step_id,
                        "kind": "runtime",
                        "tool": "bash",
                        "ok": True,
                        "exit_code": 0,
                        "command": "node --check main.js",
                        "summary": "syntax ok",
                        "ts": 20.0,
                    }
                ]
            },
        }

        self.assertFalse(
            session._plan_worker_completion_has_evidence(
                step,
                acceptance_row,
                board=session.blackboard,
                since_ts=10.0,
            )
        )
        self.assertFalse(
            session._trusted_plan_step_acceptance_records(
                step,
                acceptance_row,
                board=session.blackboard,
                since_ts=10.0,
            )
        )

    def test_acceptance_todo_commit_advances_once_from_committed_gate(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                session.messages = []
                session.agent_messages = []
                session.manager_context = []
                session.contexts = {}
                session.runtime_direct_objective = ""
                step_id = f"pt:{mode}:atomic"
                step = {
                    "id": step_id,
                    "key": "bb:proj:" + step_id,
                    "content": "1. Build runtime",
                    "full_content": "1. Build runtime\n1.1 build\n验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS",  # noqa: E501
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                work = {
                    "content": "1.1 build",
                    "status": "completed",
                    "owner": "developer",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                acceptance_row = {
                    "content": "验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                session.blackboard = {
                    "project_todos": [step],
                    "plan_step_total": 1,
                    "plan_step_evidence": {
                        step_id: [
                            {
                                "id": "ev:acceptance-pass",
                                "step_id": step_id,
                                "kind": "runtime",
                                "tool": "bash",
                                "ok": True,
                                "exit_code": 0,
                                "command": "python acceptance_test.py",
                                "summary": "ACCEPTANCE=PASS exit_code=0",
                                "ts": 20.0,
                            }
                        ]
                    },
                    "plan_subtask_evidence_bindings": {},
                }
                session.todo.update(
                    [
                        {
                            "key": step["key"],
                            "content": step["content"],
                            "status": "in_progress",
                        },
                        work,
                        acceptance_row,
                    ]
                )
                bind(
                    session,
                    "_sync_plan_worker_todos_to_blackboard",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_update_plan_file_step_status",
                    lambda self, *args, **kwargs: None,
                )
                advances = []
                bind(
                    session,
                    "_advance_plan_step",
                    lambda self, evidence="", actor="developer": (
                        advances.append((evidence, actor)) or True
                    ),
                )

                session._merge_plan_worker_todo_items(
                    [
                        {**work, "status": "completed"},
                        {**acceptance_row, "status": "completed"},
                    ],
                    role="developer",
                    update_mode="status_update",
                )

                stored = [
                    row
                    for row in session.todo.snapshot()
                    if row.get("parent_step_id") == step_id
                    and session._is_plan_step_acceptance_subtask(row.get("content", ""))
                ][-1]
                self.assertEqual(stored["status"], "completed")
                self.assertEqual(len(advances), 1)

    def test_acceptance_no_progress_limits_are_ten_cycles(self):
        self.assertEqual(cc.ACCEPTANCE_GATE_STALL_THRESHOLD, 10)
        self.assertEqual(cc.ACCEPTANCE_GATE_HARD_CEILING, 10)
        self.assertEqual(cc.ACCEPTANCE_GATE_TOTAL_ROUND_CEILING, 10)

    def test_unbound_step_local_acceptance_evidence_is_used(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                step_id = f"pt:{mode}:unbound"
                step = {
                    "id": step_id,
                    "content": "1. Runtime feature",
                    "full_content": (
                        "1. Runtime feature\n1.1 build feature\n"
                        "验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS"
                    ),
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                acceptance = {
                    "content": "验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                session.blackboard = {
                    "project_todos": [step],
                    "plan_step_evidence": {
                        step_id: [
                            {
                                "id": "ev:unbound-pass",
                                "step_id": step_id,
                                # Older/third-party tools may omit subtask_id while the
                                # runtime still records the event under this exact step.
                                "kind": "runtime",
                                "tool": "bash",
                                "ok": True,
                                "exit_code": 0,
                                "command": "python acceptance_test.py",
                                "summary": "ACCEPTANCE=PASS exit_code=0",
                                "ts": 20.0,
                            }
                        ]
                    },
                }

                records = session._matching_acceptance_evidence_records(
                    step,
                    acceptance,
                    board=session.blackboard,
                )

                self.assertEqual(
                    [record["id"] for record in records], ["ev:unbound-pass"]
                )

    def test_unbound_step_local_evidence_completes_incomplete_acceptance_binding(self):
        """A stale/incomplete acceptance binding must not hide a step-local pass."""
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                step_id = f"pt:{mode}:bound-fallback"
                step = {
                    "id": step_id,
                    "content": "1. Runtime feature",
                    "full_content": (
                        "1. Runtime feature\n1.1 build feature\n"
                        "验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS"
                    ),
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                acceptance = {
                    "content": "验收：运行 acceptance_test.py 返回 ACCEPTANCE=PASS",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                acceptance_id = session._stable_plan_worker_subtask_id(
                    step_id, acceptance
                )
                session.blackboard = {
                    "project_todos": [step],
                    "plan_step_evidence": {
                        step_id: [
                            {
                                "id": "ev:bound-incomplete",
                                "step_id": step_id,
                                "subtask_id": acceptance_id,
                                "kind": "runtime",
                                "tool": "bash",
                                "ok": True,
                                "exit_code": 0,
                                "command": "node unrelated_probe.js",
                                "summary": "probe completed; acceptance result not reported",  # noqa: E501
                                "ts": 20.0,
                            },
                            {
                                "id": "ev:unbound-pass-fallback",
                                "step_id": step_id,
                                # Deliberately omit subtask_id: this is the shape
                                # emitted by older/third-party tool integrations.
                                "kind": "runtime",
                                "tool": "bash",
                                "ok": True,
                                "exit_code": 0,
                                "command": "python acceptance_test.py",
                                "summary": "ACCEPTANCE=PASS exit_code=0",
                                "ts": 21.0,
                            },
                        ]
                    },
                }

                records = session._matching_acceptance_evidence_records(
                    step,
                    acceptance,
                    board=session.blackboard,
                )

                record_ids = [record["id"] for record in records]
                self.assertIn("ev:unbound-pass-fallback", record_ids)
                # Aggregate matching may retain the earlier bound observation
                # as supporting context; the decisive unbound pass must still
                # be present and able to close the contract.
                self.assertEqual(record_ids[-1], "ev:unbound-pass-fallback")

    def test_plan_parent_bare_ordinal_resolves_without_weakening_step_isolation(self):
        session = self.bare_session("single")
        first = {
            "id": "pt:epoch:000",
            "content": "1. First step",
            "category": "plan_step",
            "status": "in_progress",
            "plan_step_index": 0,
        }
        second = {
            "id": "pt:epoch:001",
            "content": "2. Second step",
            "category": "plan_step",
            "status": "pending",
            "plan_step_index": 1,
        }
        session.blackboard = {"project_todos": [first, second]}

        self.assertEqual(
            session._canonical_plan_worker_parent_id("1", board=session.blackboard),
            first["id"],
        )
        self.assertEqual(
            session._canonical_plan_worker_parent_id("#1", board=session.blackboard),
            first["id"],
        )
        self.assertEqual(
            session._canonical_plan_worker_parent_id("2", board=session.blackboard),
            second["id"],
        )

    def test_todowrite_bare_current_parent_commits_but_future_parent_is_rejected(self):
        for mode in ("single", "sync"):
            with self.subTest(mode=mode):
                session = self.bare_session(mode)
                step_id = f"pt:{mode}:000"
                next_step_id = f"pt:{mode}:001"
                step = {
                    "id": step_id,
                    "key": "bb:proj:" + step_id,
                    "content": "1. Build entry",
                    "full_content": "1. Build entry\n1.1 create entry",
                    "category": "plan_step",
                    "status": "in_progress",
                    "plan_step_index": 0,
                    "activated_at": 10.0,
                }
                next_step = {
                    "id": next_step_id,
                    "key": "bb:proj:" + next_step_id,
                    "content": "2. Future work",
                    "category": "plan_step",
                    "status": "pending",
                    "plan_step_index": 1,
                }
                worker = {
                    "content": "1.1 create entry",
                    "status": "in_progress",
                    "owner": "developer",
                    "parent_step_id": step_id,
                    "created_at": 10.0,
                }
                session.blackboard = {
                    "project_todos": [step, next_step],
                    "plan_step_total": 2,
                    "plan_subtask_evidence_bindings": {},
                }
                session.todo.update(
                    [
                        {
                            "key": step["key"],
                            "content": step["content"],
                            "status": "in_progress",
                        },
                        worker,
                        {
                            "key": next_step["key"],
                            "content": next_step["content"],
                            "status": "pending",
                        },
                    ]
                )
                bind(
                    session,
                    "_sync_plan_worker_todos_to_blackboard",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_update_plan_file_step_status",
                    lambda self, *args, **kwargs: None,
                )
                bind(
                    session,
                    "_advance_completed_acceptance_after_todo_commit",
                    lambda self, *args, **kwargs: False,
                )
                bind(
                    session,
                    "_plan_worker_completion_has_evidence",
                    lambda self, *args, **kwargs: True,
                )
                bind(
                    session,
                    "_plan_worker_completion_evidence_records",
                    lambda self, plan_step, row, **kwargs: [
                        {
                            "id": "ev:entry",
                            "step_id": plan_step["id"],
                            "kind": "file",
                            "tool": "write_file",
                            "ok": True,
                            "summary": "entry created",
                            "ts": 20.0,
                        }
                    ],
                )

                accepted = session._dispatch_todo_update(
                    {
                        "todos": [
                            {
                                "content": worker["content"],
                                "status": "completed",
                                "parent_step_id": "1",
                            }
                        ]
                    },
                    role="developer",
                )
                stored = [
                    row
                    for row in session.todo.snapshot()
                    if row.get("parent_step_id") == step_id
                    and row.get("content") == worker["content"]
                ]
                self.assertEqual(stored[-1]["status"], "completed")
                self.assertNotIn("rejected a cross-step", accepted)

                # The WebUI deliberately keeps roadmap parents in ``todos``
                # and exposes only the active parent's children in ``tasks``.
                # A committed TodoWrite must therefore be visible immediately
                # in the task panel snapshot without flattening both layers.
                session.tasks = types.SimpleNamespace(list_objects=lambda: [])
                session.runtime_plan_proposal = {}
                ui_todos, ui_tasks, scope = session._ui_todo_task_scope_snapshot(
                    session.blackboard
                )
                self.assertEqual(
                    [row["plan_step_id"] for row in ui_todos],
                    [step_id, next_step_id],
                )
                self.assertEqual(scope["parent_step_id"], step_id)
                visible_worker = [
                    row for row in ui_tasks if row.get("subject") == worker["content"]
                ]
                self.assertEqual(visible_worker[-1]["status"], "completed")

                before = session.todo.snapshot()
                rejected = session._dispatch_todo_update(
                    {
                        "todos": [
                            {
                                "content": "2.1 future change",
                                "status": "in_progress",
                                "parent_step_id": "2",
                            }
                        ]
                    },
                    role="developer",
                )
                self.assertIn("rejected a cross-step", rejected)
                self.assertEqual(session.todo.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
