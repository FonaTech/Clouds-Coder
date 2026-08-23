import json
import threading
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class SingleNoPlanTodoBootstrapTests(unittest.TestCase):
    def bare_session(self, mode="single"):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.todo = cc.TodoManager("zh-CN")
        session.execution_mode = mode
        session.runtime_execution_mode = mode
        session.runtime_assigned_expert = "developer"
        session.active_agent_role = "developer"
        session.runtime_plan_mode_needed = False
        session.runtime_plan_approved = False
        session.plan_mode_user_preference = "off"
        session.runtime_task_type = "general"
        session.runtime_task_level = 0
        session.user_task_level_override = 0
        session.runtime_requires_todos = None
        session.l2_todo_policy = cc.DEFAULT_L2_TODO_POLICY
        session.blackboard = {}
        session.messages = []
        session.single_no_plan_todo_enabled = True
        session.single_no_plan_todo_prompt = "Custom bootstrap instruction"
        session.single_no_plan_todo_bootstrap_state = "idle"
        session.single_no_plan_todo_bootstrap_attempts = 0
        session.single_no_plan_todo_perception_seen = False
        session.single_no_plan_todo_bootstrap_write_seen = False
        session.events = []
        session.skill_mode = "soft"
        session.web_search_enabled = False
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_emit", lambda self, *args, **
             kwargs: self.events.append((args, kwargs)))
        bind(session, "_persist", lambda self: None)
        return session

    def test_config_supports_top_level_nested_and_prompt_only_forms(self):
        enabled, prompt = cc.extract_single_no_plan_todo_settings(
            {
                "single_no_plan_todo_enabled": True,
                "single_no_plan_todo_prompt": "custom",
            }
        )
        self.assertTrue(enabled)
        self.assertEqual(prompt, "custom")

        enabled, prompt = cc.extract_single_no_plan_todo_settings(
            {"runtime": {"single": {"todo_bootstrap_enabled": True, "todo_bootstrap_prompt": "nested"}}}  # noqa: E501
        )
        self.assertTrue(enabled)
        self.assertEqual(prompt, "nested")

        enabled, prompt = cc.extract_single_no_plan_todo_settings(
            {"single_no_plan_todo_enabled": False,
                "single_no_plan_todo_prompt": "ignored for enablement"}
        )
        self.assertFalse(enabled)
        self.assertEqual(prompt, "ignored for enablement")

        enabled, prompt = cc.extract_single_no_plan_todo_settings(
            {"single_no_plan_todo_enabled": True, "single_no_plan_todo_prompt": ""}
        )
        self.assertTrue(enabled)
        self.assertEqual(prompt, cc.DEFAULT_SINGLE_NO_PLAN_TODO_PROMPT)
        self.assertIn("1-40", prompt)
        self.assertIn("one-for-one", prompt)
        self.assertNotIn("3-7", prompt)

        self.assertEqual(cc.extract_single_no_plan_todo_settings({}), (False, ""))

    def test_l2_todo_policy_normalization_and_config_extraction(self):
        self.assertEqual(cc.DEFAULT_L2_TODO_POLICY, "force")
        self.assertEqual(cc.normalize_l2_todo_policy(None), "force")
        self.assertEqual(cc.normalize_l2_todo_policy("required"), "force")
        self.assertEqual(cc.normalize_l2_todo_policy("llm"), "auto")
        self.assertEqual(cc.normalize_l2_todo_policy("disabled"), "off")
        self.assertEqual(cc.normalize_l2_todo_policy("invalid"), "force")

        self.assertEqual(
            cc.extract_l2_todo_policy_setting({"l2_todo_policy": "auto"}),
            "auto",
        )
        self.assertEqual(
            cc.extract_l2_todo_policy_setting(
                {"runtime": {"l2_todo_policy": "off"}}
            ),
            "off",
        )
        self.assertEqual(
            cc.extract_l2_todo_policy_setting(
                {"task_policy": {"l2_requires_todos": False}}
            ),
            "off",
        )
        self.assertIsNone(cc.extract_l2_todo_policy_setting({}))

    def test_prompt_only_app_context_argument_enables_bootstrap(self):
        with TemporaryDirectory() as root_text:
            root = Path(root_text)
            with patch.object(cc, "probe_ollama_environment", return_value=(False, [], "")):  # noqa: E501
                app = cc.AppContext(
                    root,
                    "http://127.0.0.1:11434",
                    "demo-model",
                    root / "skills",
                    execution_mode="single",
                    single_no_plan_todo_prompt="plan from evidence",
                )
            self.assertTrue(app.single_no_plan_todo_enabled)
            self.assertEqual(app.single_no_plan_todo_prompt, "plan from evidence")

    def test_admin_config_round_trips_bootstrap_prompt_without_empty_integer_args(self):
        raw = {
            "l2_todo_policy": "auto",
            "single_no_plan_todo_enabled": True,
            "single_no_plan_todo_prompt": "Use the read evidence and create the next actions.",  # noqa: E501
            # This reproduces the old Admin form behavior where an optional
            # integer could arrive as an empty string.
            "auto_task_level_ceiling": "",
        }
        clean, errors = cc._admin_coerce_config(raw)
        self.assertFalse(errors)
        self.assertEqual(clean["auto_task_level_ceiling"],
                         cc.DEFAULT_AUTO_TASK_LEVEL_CEILING)
        self.assertEqual(clean["l2_todo_policy"], "auto")
        argv = cc._admin_config_to_argv(raw)
        policy_pos = argv.index("--l2-todo-policy")
        self.assertEqual(argv[policy_pos + 1], "auto")
        self.assertIn("--single-no-plan-todo", argv)
        self.assertIn("--single-no-plan-todo-prompt", argv)
        self.assertIn("Use the read evidence and create the next actions.", argv)
        ceiling_pos = argv.index("--auto_task_level_ceiling")
        self.assertNotEqual(argv[ceiling_pos + 1], "")

    def test_runtime_model_selection_does_not_reference_startup_config_scope(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.active_profile_id = "ollama"
        session.model_profiles = {
            "ollama": {
                "id": "ollama",
                "provider": "ollama",
                "model": "demo-model",
                "base_url": "http://127.0.0.1:11434",
            }
        }
        session.ollama = types.SimpleNamespace(
            model="demo-model", base_url="http://127.0.0.1:11434")
        session.failed_selections = []
        session.auto_task_level_ceiling = 0
        session.updated_at = 0.0
        session.single_no_plan_todo_enabled = True
        session.single_no_plan_todo_prompt = "keep this setting"
        bind(
            session,
            "_sanitize_profile_id",
            lambda self,
            value: str(
                value or "").strip())
        bind(session, "_profile_is_runnable", lambda self, profile: True)
        bind(session, "_apply_active_profile", lambda self: None)
        bind(session, "_ensure_active_profile_capabilities",
             lambda self, force_probe=False: None)
        bind(session, "_persist", lambda self: None)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "model_catalog", lambda self: {
             "selected": self.active_profile_id})

        result = session.set_runtime_selection("ollama::demo-model")
        self.assertEqual(result["selected"], "ollama")
        self.assertTrue(session.single_no_plan_todo_enabled)
        self.assertEqual(session.single_no_plan_todo_prompt, "keep this setting")

    def test_only_single_no_plan_without_existing_plan_or_todos_is_eligible(self):
        session = self.bare_session("single")
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        session.runtime_task_type = "simple_qa"
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session("sync")
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session("single")
        session.runtime_plan_mode_needed = True
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session("single")
        session.plan_mode_user_preference = "on"
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session("single")
        session.todo.update([{"content": "already planned", "status": "in_progress"}])
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

    def test_l2_always_requires_todos_even_when_optional_switch_is_off(self):
        session = self.bare_session("single")
        session.single_no_plan_todo_enabled = False
        session.runtime_task_level = 2
        session.auto_task_level_ceiling = 2
        self.assertTrue(session._runtime_level_requires_todos())
        self.assertTrue(session._single_no_plan_todo_policy_enabled())
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        # The level contract also wins over the old simple_qa exclusion.
        session.runtime_task_type = "simple_qa"
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        # The automatic ceiling is still authoritative: capping at L1 removes
        # the L2 contract, while a manual L2 override deliberately bypasses it.
        session.auto_task_level_ceiling = 1
        self.assertFalse(session._runtime_level_requires_todos())
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())
        session.user_task_level_override = 2
        self.assertTrue(session._runtime_level_requires_todos())
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        # A partially constructed session with no ceiling field must not infer
        # the application's default ceiling and mislabel an explicit L3.
        session = self.bare_session("single")
        session.runtime_task_level = 3
        session.single_no_plan_todo_enabled = False
        self.assertEqual(session._runtime_task_level_for_todo_policy(), 3)
        self.assertFalse(session._todo_contract_prompt_block())

    def test_l2_force_auto_and_off_resolve_without_overriding_other_levels(self):
        session = self.bare_session("single")
        session.runtime_task_level = 2
        session.auto_task_level_ceiling = 2
        session.single_no_plan_todo_enabled = True

        session.l2_todo_policy = "force"
        session.runtime_requires_todos = False
        self.assertTrue(session._runtime_level_requires_todos())
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        session.l2_todo_policy = "off"
        session.runtime_requires_todos = True
        self.assertFalse(session._runtime_level_requires_todos())
        self.assertFalse(session._single_no_plan_todo_policy_enabled())
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())
        self.assertEqual(session._todo_contract_prompt_block(), "")
        self.assertFalse(
            session._single_no_plan_todo_mutation_blocked(
                "write_file", {"path": "x", "content": "y"}
            )
        )

        session.l2_todo_policy = "auto"
        session.runtime_requires_todos = False
        self.assertFalse(session._runtime_level_requires_todos())
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())
        session.runtime_requires_todos = True
        self.assertTrue(session._runtime_level_requires_todos())
        self.assertTrue(session._single_no_plan_todo_bootstrap_allowed())

        session.runtime_requires_todos = None
        session.blackboard = {}
        self.assertTrue(session._runtime_level_requires_todos())

        session.runtime_task_level = 1
        self.assertFalse(session._runtime_level_requires_todos())
        session.runtime_task_level = 3
        session.auto_task_level_ceiling = 0
        session.l2_todo_policy = "off"
        self.assertTrue(session._runtime_level_requires_todos())

    def test_classifier_contract_exposes_semantic_requires_todos(self):
        session = self.bare_session("single")
        spec = session._manager_task_classify_tools()[0]["function"]["parameters"]
        self.assertEqual(spec["properties"]["requires_todos"]["type"], "boolean")
        self.assertIn("requires_todos", spec["required"])

        session.runtime_task_level = 2
        session.auto_task_level_ceiling = 2
        session.l2_todo_policy = "auto"
        self.assertFalse(
            session._normalize_todo_requirement_in_decision(
                {"level": 2, "requires_todos": False},
                allow_context=False,
            )["requires_todos"]
        )
        self.assertTrue(
            session._normalize_todo_requirement_in_decision(
                {"level": 2},
                allow_context=False,
            )["requires_todos"]
        )

    def test_auto_policy_uses_manager_llm_requires_todos_result(self):
        session = self.bare_session("single")
        session.l2_todo_policy = "auto"
        session.auto_task_level_ceiling = 2
        session.runtime_task_level = 0
        session.runtime_round_budget = 0
        session.runtime_participants = []
        session.files_root = Path(".")
        session.skills = types.SimpleNamespace(list_names=lambda: [])
        session._cached_complexity_dimensions = {}
        session.lock = threading.RLock()
        session.user_memory_mode = "off"
        session.user_profile_capsule = ""
        session.user_profile_capsule_meta = {}
        bind(
            session,
            "_format_previous_task_context_for_prompt",
            lambda self, max_chars=1000: "",
        )
        bind(session, "_manager_progress_state", lambda self, board: "initializing")
        bind(session, "_append_live_thinking", lambda self, *args, **kwargs: None)

        calls = []

        def fake_chat(self, *args, **kwargs):
            calls.append(kwargs)
            return {
                "tool_calls": [
                    {
                        "function": {
                            "name": "classify_task_level",
                            "arguments": {
                                "level": 2,
                                "judgement": "self-contained response",
                                "requires_todos": False,
                                "inherit_previous_state": False,
                                "plan_change_scope": "preserve",
                                "plan_change_evidence": "",
                                "requires_plan": False,
                                "semantic_confidence": "high",
                            },
                        }
                    }
                ]
            }

        bind(session, "_chat_with_same_model_retry", fake_chat)
        row = session._manager_classify_task_level(
            "Explain this briefly",
            pinned_selection="demo",
        )
        self.assertEqual(len(calls), 1)
        self.assertFalse(row["requires_todos"])
        self.assertEqual(row["source"], "manager")

    def test_auto_task_level_ceiling_and_manual_override_still_apply(self):
        session = self.bare_session("single")
        session.runtime_task_level = 2
        session.l2_todo_policy = "force"
        session.auto_task_level_ceiling = 1
        self.assertEqual(session._runtime_task_level_for_todo_policy(), 1)
        self.assertFalse(session._runtime_level_requires_todos())

        session.user_task_level_override = 2
        self.assertEqual(session._runtime_task_level_for_todo_policy(), 2)
        self.assertTrue(session._runtime_level_requires_todos())

    def test_todo_payload_prefers_structured_plural_fields_over_stringified_content(
            self):
        session = self.bare_session()
        rows = [
            {
                "content": "Inspect the observed files",
                "status": "in_progress",
                "owner": "developer",
                "parent_step_id": "plan",
            },
            {
                "content": "Implement the next change",
                "status": "pending",
                "owner": "developer",
                "parent_step_id": "build",
            },
        ]
        # This is the provider shape seen in the persisted failure: a valid
        # plural array plus a Python-repr compatibility ``content`` field.
        payload = {"content": repr(rows), "todos": rows}
        parsed = session._todo_payload_items(payload)
        self.assertEqual([row["content"] for row in parsed], [
                         "Inspect the observed files", "Implement the next change"])
        self.assertEqual([row["status"] for row in parsed], ["in_progress", "pending"])

        # The compatibility field also works when it is the only field.
        parsed_repr_only = session._todo_payload_items({"content": repr(rows)})
        self.assertEqual(len(parsed_repr_only), 2)

    def test_l2_todo_pipeline_preserves_eleven_explicit_stages(self):
        session = self.bare_session()
        rows = [
            {
                "content": f"阶段 {index}: 完成对应交付",
                "status": "in_progress" if index == 1 else "pending",
            }
            for index in range(1, 12)
        ]

        parsed = session._todo_payload_items({"todos": rows})
        self.assertEqual(len(parsed), 11)
        self.assertEqual([row["content"] for row in parsed],
                         [row["content"] for row in rows])

        recovered = session._extract_text_items_from_raw_args({"items": rows})
        self.assertEqual(len(recovered), 11)

        structured = "1. 顶层阶段\n" + "\n".join(
            f"1.{index} 阶段 {index}: 完成对应交付" for index in range(1, 12)
        )
        split_rows = cc.split_structured_todo_content(structured)
        self.assertEqual(len(split_rows), 11)
        session.todo.update([{"content": structured, "status": "in_progress"}])
        self.assertEqual(len(session.todo.snapshot()), 11)

    def test_legacy_stringified_loaded_todo_is_recovered_from_same_session_call(self):
        session = self.bare_session()
        rows = [
            {"content": "First observed item", "status": "completed", "owner": "developer"},  # noqa: E501
            {"content": "Second observed item", "status": "in_progress", "owner": "developer"},  # noqa: E501
        ]
        bad_content = repr(rows)[:-4] + "...(truncated)"
        messages = [
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "function": {
                            "name": "TodoWrite",
                            "arguments": json.dumps({"todos": rows}),
                        }
                    }
                ],
            }
        ]
        recovered = session._normalize_loaded_todo_rows(
            [{"content": bad_content, "status": "completed"}],
            messages,
        )
        self.assertEqual([row["content"] for row in recovered], [
                         "First observed item", "Second observed item"])
        self.assertEqual(recovered[1]["status"], "in_progress")
        normal_rows = [{"content": "normal", "status": "pending", "owner": "developer"}]
        self.assertEqual(session._normalize_loaded_todo_rows(
            normal_rows, []), normal_rows)

    def test_frontend_renders_bootstrap_control_as_structured_card(self):
        source = Path(cc.__file__).read_text(encoding="utf-8")
        self.assertIn(
            "'single-no-plan-todo-bootstrap':{labelKey:'event_todo_bootstrap_title'",
            source)
        self.assertIn(
            "const isTodoBootstrap=runtimeHint.name==='single-no-plan-todo-bootstrap'",
            source)
        self.assertIn("event_todo_bootstrap_item_count", source)
        self.assertIn("event_todo_bootstrap_item_count:'1-40 项 · 对齐阶段'", source)

    def test_l2_initial_gate_hides_mutation_tools_and_blocks_stale_calls(self):
        session = self.bare_session("single")
        session.single_no_plan_todo_enabled = False
        session.runtime_task_level = 2
        session.auto_task_level_ceiling = 2
        bind(session, "_available_tools", lambda self: list(cc.TOOLS))

        self.assertTrue(session._single_no_plan_todo_initial_gate_active())
        names = [
            row["function"]["name"]
            for row in session._single_no_plan_todo_perception_tools()
        ]
        self.assertIn("TodoWrite", names)
        self.assertIn("read_file", names)
        self.assertNotIn("write_file", names)
        self.assertNotIn("edit_file", names)
        self.assertNotIn("bash", names)
        self.assertTrue(session._single_no_plan_todo_mutation_blocked(
            "write_file", {"path": "x", "content": "y"}))
        self.assertTrue(session._single_no_plan_todo_mutation_blocked(
            "bash", {"command": "printf x > x"}))

        session.todo.update([{"content": "implement change", "status": "in_progress"}])
        self.assertFalse(session._single_no_plan_todo_initial_gate_active())
        self.assertFalse(session._single_no_plan_todo_mutation_blocked(
            "write_file", {"path": "x", "content": "y"}))

    def test_l2_prompt_states_mandatory_todo_contract(self):
        session = self.bare_session("single")
        session.runtime_task_level = 2
        session.single_no_plan_todo_enabled = False
        session.auto_task_level_ceiling = 2
        prompt = session._todo_contract_prompt_block()
        self.assertIn("MANDATORY L2 TODO CONTRACT", prompt)
        self.assertIn("TodoWrite", prompt)
        self.assertIn("before any mutation", prompt)
        self.assertIn("1-40", prompt)
        self.assertIn("one-for-one", prompt)
        self.assertNotIn("3-7", prompt)

    def test_perception_and_side_effect_classification(self):
        session = self.bare_session()
        self.assertTrue(
            session._single_no_plan_todo_is_perception_result(
                {"name": "read_file", "args": {"path": "index.html"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_perception_result(
                {"name": "bash", "args": {"command": "ls -la"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_perception_result(
                {"name": "check_background", "args": {"mode": "summary"}, "ok": True}
            )
        )
        self.assertFalse(session._single_no_plan_todo_is_perception_result(
            {"name": "bash", "args": {"command": "printf x > generated.txt"}, "ok": True}))  # noqa: E501
        self.assertFalse(
            session._single_no_plan_todo_is_perception_result(
                {"name": "browser_click", "args": {"selector": "#run"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_perception_result(
                {"name": "browser_screenshot", "args": {
                    "url": "http://127.0.0.1:8128"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "mcp__browser__page", "args": {"action": "fill"}, "ok": False}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "mcp__filesystem__write_file",
                    "args": {"path": "out.txt"}, "ok": False}
            )
        )
        self.assertTrue(session._single_no_plan_todo_is_mutation_result(
            {"name": "mcp__service__request", "args": {"method": "POST"}, "ok": True}))
        self.assertFalse(
            session._single_no_plan_todo_is_perception_result(
                {"name": "bash", "args": {
                    "command": "echo $(touch marker)"}, "ok": True}
            )
        )
        self.assertFalse(
            session._single_no_plan_todo_is_perception_result(
                {"name": "bash", "args": {"command": "find . -delete"}, "ok": True}
            )
        )
        self.assertFalse(
            session._single_no_plan_todo_is_perception_result(
                {"name": "bash", "args": {"command": "git branch new-work"}, "ok": True}
            )
        )
        self.assertTrue(session._single_no_plan_todo_is_mutation_result(
            {"name": "bash", "args": {"command": "printf x > generated.txt"}, "ok": False}))  # noqa: E501
        self.assertTrue(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "worktree_run", "args": {"command": "pytest"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "ask_user", "args": {"question": "Need a choice"}, "ok": True}
            )
        )
        self.assertTrue(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "ask_colleague", "args": {"to": "reviewer"}, "ok": False}
            )
        )
        self.assertFalse(
            session._single_no_plan_todo_is_mutation_result(
                {"name": "read_file", "args": {"path": "index.html"}, "ok": True}
            )
        )

    def test_bootstrap_turn_has_custom_prompt_and_only_two_writer_tools(self):
        session = self.bare_session()
        bind(session, "_available_tools", lambda self: list(cc.TOOLS))

        self.assertTrue(session._start_single_no_plan_todo_bootstrap())
        self.assertEqual(session.single_no_plan_todo_bootstrap_state, "waiting")
        self.assertTrue(session.single_no_plan_todo_perception_seen)
        self.assertIn("Custom bootstrap instruction", session.messages[-1]["content"])

        names = [row["function"]["name"]
                 for row in session._single_no_plan_todo_bootstrap_tools()]
        self.assertEqual(names, ["TodoWrite", "TodoWriteRescue"])

    def test_bootstrap_success_and_bounded_failure_are_terminal(self):
        session = self.bare_session()
        self.assertEqual(session._start_single_no_plan_todo_bootstrap(), True)
        self.assertTrue(session._single_no_plan_todo_bootstrap_turn_active())
        session.runtime_execution_mode = "sync"
        self.assertFalse(session._single_no_plan_todo_bootstrap_turn_active())
        session.runtime_execution_mode = "single"
        session.single_no_plan_todo_enabled = False
        self.assertFalse(session._single_no_plan_todo_bootstrap_turn_active())
        session.single_no_plan_todo_enabled = True
        self.assertEqual(
            session._single_no_plan_todo_bootstrap_failure("no tool"), "retry")
        self.assertEqual(session.single_no_plan_todo_bootstrap_state, "waiting")
        self.assertEqual(session.single_no_plan_todo_bootstrap_attempts, 1)
        self.assertEqual(session._single_no_plan_todo_bootstrap_failure(
            "still no tool"), "skip")
        self.assertEqual(session.single_no_plan_todo_bootstrap_state, "skipped")
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session()
        session._start_single_no_plan_todo_bootstrap()
        session.todo.update(
            [
                {"content": "Inspect evidence", "status": "completed"},
                {"content": "Implement next change", "status": "in_progress"},
            ]
        )
        self.assertTrue(session._single_no_plan_todo_has_rows())
        session._single_no_plan_todo_bootstrap_succeeded()
        self.assertEqual(session.single_no_plan_todo_bootstrap_state, "completed")
        self.assertFalse(session._single_no_plan_todo_bootstrap_allowed())

        session = self.bare_session()
        session.runtime_task_level = 2
        session.single_no_plan_todo_enabled = False
        session.auto_task_level_ceiling = 2
        session._start_single_no_plan_todo_bootstrap()
        self.assertEqual(
            session._single_no_plan_todo_bootstrap_failure("no tool"), "retry")
        self.assertEqual(session._single_no_plan_todo_bootstrap_failure(
            "still no tool"), "blocked")
        self.assertEqual(session.single_no_plan_todo_bootstrap_state, "blocked")
        self.assertFalse(session._single_no_plan_todo_bootstrap_turn_active())


if __name__ == "__main__":
    unittest.main()
