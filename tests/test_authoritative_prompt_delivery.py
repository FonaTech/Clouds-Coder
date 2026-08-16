import threading
import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


def long_goal():
    return ("完整任务段落：必须保留所有约束和步骤。\n" * 700) + "TAIL_ACCEPTANCE_MARKER_9F72"


class AuthoritativePromptDeliveryTests(unittest.TestCase):
    def bare_session(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.runtime_authoritative_goal = long_goal()
        session.runtime_reclassify_goal = ""
        session.messages = []
        session.blackboard = {}
        return session

    def test_all_execution_topologies_receive_complete_goal_at_model_boundary(self):
        session = self.bare_session()
        captured = []
        session.cancel_requested = False
        session.ollama = types.SimpleNamespace(
            response_stream=False,
            chat=lambda messages, **kwargs: captured.append(messages) or {
                "content": "ok",
                "tool_calls": [],
            },
        )
        bind(session, "_active_runtime_selection", lambda self: "test::model")
        bind(session, "_inject_runtime_environment_context", lambda self, text: text)
        bind(session, "_estimate_model_call_prompt_tokens", lambda self, *args, **kwargs: 1)
        bind(session, "_resolve_effort_for_call", lambda self, **kwargs: "off")
        bind(session, "_call_interruptible", lambda self, fn, **kwargs: fn())
        bind(session, "_record_model_usage", lambda self, *args, **kwargs: None)

        labels = (
            "agent turn",                 # single / plan+single execution
            "manager turn",               # sync and plan+sync coordinator
            "developer turn",             # sync worker
            "reviewer turn",              # sync worker
            "plan-mode explorer round 1", # plan research
            "plan-mode synthesis",        # plan synthesis
            "subagent",                   # delegated worker
        )
        for label in labels:
            session._chat_with_same_model_retry(
                [{"role": "user", "content": "short derived prompt"}],
                context_label=label,
                retries=0,
            )

        self.assertEqual(len(captured), len(labels))
        for rows in captured:
            rendered = "\n".join(session._model_message_text(row) for row in rows)
            self.assertIn("TAIL_ACCEPTANCE_MARKER_9F72", rendered)
            self.assertIn(session.runtime_authoritative_goal, rendered)

    def test_full_goal_already_in_context_is_not_duplicated(self):
        session = self.bare_session()
        rows = session._messages_with_authoritative_user_goal(
            [{"role": "user", "content": f"Task:\n{session.runtime_authoritative_goal}"}],
            context_label="plan-mode synthesis",
        )
        rendered = "\n".join(session._model_message_text(row) for row in rows)
        self.assertEqual(rendered.count("TAIL_ACCEPTANCE_MARKER_9F72"), 1)

    def test_plan_choice_preserves_original_authoritative_goal(self):
        session = self.bare_session()
        original = session.runtime_authoritative_goal

        session._apply_authoritative_user_submission("A", preserve=True)

        self.assertEqual(session.runtime_authoritative_goal, original)
        self.assertTrue(session.runtime_authoritative_goal.endswith("TAIL_ACCEPTANCE_MARKER_9F72"))

    def test_old_session_recovers_full_message_from_truncated_blackboard_prefix(self):
        session = self.bare_session()
        goal = session.runtime_authoritative_goal
        session.runtime_authoritative_goal = ""
        session.messages = [{"role": "user", "content": goal}]
        session.blackboard = {"original_goal": goal[:4000]}

        recovered = session._authoritative_user_goal_for_model()

        self.assertEqual(recovered, goal)
        self.assertTrue(recovered.endswith("TAIL_ACCEPTANCE_MARKER_9F72"))

    def test_plan_research_prompt_uses_full_authoritative_goal(self):
        session = self.bare_session()
        session.ui_language = "zh-CN"
        session.files_root = "/workspace"
        bind(session, "_ensure_blackboard", lambda self: {"loaded_skills": {}})

        prompt = session._plan_mode_research_prompt()

        self.assertIn(session.runtime_authoritative_goal, prompt)
        self.assertTrue(prompt.index("TAIL_ACCEPTANCE_MARKER_9F72") > 10_000)

    def test_multi_agent_seed_keeps_full_goal_for_explorer_and_manager(self):
        session = self.bare_session()
        session.agent_messages = []
        session.manager_context = []
        session.contexts = {role: [] for role in cc.AGENT_ROLES}
        session.blackboard = {"original_goal": ""}
        appended = []
        bind(session, "_is_multi_agent_mode", lambda self: True)
        bind(session, "_mark_multi_agent_context_hud_active", lambda self, **kwargs: None)
        bind(session, "_agent_language_policy_note", lambda self: "")
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_blackboard_reset_for_goal", lambda self, goal, **kwargs: self.blackboard.update(original_goal=goal))
        bind(session, "_mark_runtime_goal_reset_handled", lambda self, **kwargs: None)
        bind(session, "_format_previous_task_context_for_prompt", lambda self, **kwargs: "")
        bind(session, "_apply_agent_language_policy", lambda self, text, **kwargs: text)
        bind(session, "_agent_context", lambda self, role: [row for row in appended if row.get("agent_role") == role])

        def append_message(self, role, message, **kwargs):
            row = dict(message)
            row["agent_role"] = role
            appended.append(row)
            return row

        bind(session, "_append_agent_context_message", append_message)

        session._seed_multi_agent_contexts_if_needed("truncated fallback")

        explorer_text = "\n".join(
            session._model_message_text(row)
            for row in appended
            if row.get("agent_role") == "explorer"
        )
        manager_text = "\n".join(session._model_message_text(row) for row in session.manager_context)
        self.assertIn(session.runtime_authoritative_goal, explorer_text)
        self.assertIn(session.runtime_authoritative_goal, manager_text)

    def test_long_running_and_deferred_inputs_are_not_trimmed(self):
        session = self.bare_session()
        session.lock = threading.RLock()
        session.live_input_queue_lock = threading.Lock()
        session.deferred_start_worker_lock = threading.Lock()
        session.pending_user_inputs = []
        session.deferred_start_inputs = []
        session.deferred_start_seq = 0
        session.deferred_start_worker_started = True
        session.live_input_seq = 0
        session.agent_round_index = 0
        session.run_generation = 1
        session.current_phase = "thinking"
        session.current_tool_name = ""
        session.updated_at = 0.0
        bind(session, "_persist", lambda self: None)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        text = long_goal()

        running = session._enqueue_running_user_input(text)
        deferred = session._enqueue_deferred_start_input(text)

        self.assertEqual(running["content"], text)
        self.assertEqual(deferred["content"], text)
        self.assertTrue(running["content"].endswith("TAIL_ACCEPTANCE_MARKER_9F72"))
        self.assertTrue(deferred["content"].endswith("TAIL_ACCEPTANCE_MARKER_9F72"))

    def test_authoritative_marker_survives_tier3_compaction_and_offload(self):
        session = self.bare_session()
        wrapped = (
            f"{cc.AUTHORITATIVE_USER_GOAL_OPEN}\n"
            f"{session.runtime_authoritative_goal}\n"
            f"{cc.AUTHORITATIVE_USER_GOAL_CLOSE}"
        )
        session.manager_context = [{"role": "user", "content": wrapped}]
        session.runtime_plan_proposal = {}
        bind(
            session,
            "_offload_to_file_buffer",
            lambda self, *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not offload authority")),
        )

        session._compact_role_context("manager", 3)

        self.assertEqual(session.manager_context[0]["content"], wrapped)
        self.assertIn("TAIL_ACCEPTANCE_MARKER_9F72", session.manager_context[0]["content"])


if __name__ == "__main__":
    unittest.main()
