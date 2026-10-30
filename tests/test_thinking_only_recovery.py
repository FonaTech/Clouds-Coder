import types
import unittest

import Clouds_Coder as cc


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class ThinkingOnlyRecoveryTests(unittest.TestCase):
    def bare(self, provider="openai_compat"):
        session = cc.SessionState.__new__(cc.SessionState)
        session.messages = [{"role": "user", "content": "Implement the requested feature."}]
        session.max_output_tokens = 8192
        session.cancel_requested = False
        session.ui_language = "en-US"
        session.ollama = types.SimpleNamespace(provider=provider)
        session.runtime_authoritative_goal = "Implement the requested feature."
        bind(session, "_system_prompt", lambda self: "system")
        bind(session, "_single_no_plan_todo_bootstrap_tools", lambda self: [
            cc.tool_def("TodoWrite", "write todos", {"items": {"type": "array"}}),
            cc.tool_def("TodoWriteRescue", "rescue todos", {"items": {"type": "array"}}),
        ])
        return session

    def test_normal_thinking_with_final_content_is_not_empty(self):
        session = self.bare()
        self.assertFalse(session._is_empty_action_turn("final answer", "long reasoning", []))

    def test_recovery_ladder_uses_low_effort_then_forced_todo(self):
        session = self.bare()
        calls = []

        def fake_chat(self, messages, **kwargs):
            calls.append(kwargs)
            if len(calls) == 1:
                return {"content": "", "thinking": "still reasoning", "tool_calls": []}
            return {
                "content": "",
                "thinking": "",
                "tool_calls": [{
                    "id": "todo-1",
                    "type": "function",
                    "function": {"name": "TodoWrite", "arguments": {"items": ["Implement feature"]}},
                }],
            }

        bind(session, "_chat_with_same_model_retry", fake_chat)
        result = session._recover_thinking_only_response(
            {"content": "", "thinking": "original", "tool_calls": []},
            bootstrap=True,
            tools=session._single_no_plan_todo_bootstrap_tools(),
            pinned_selection="",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["stage"], "forced")
        self.assertEqual(calls[0]["think"], True)
        self.assertEqual(calls[0]["effort"], cc.EFFORT_LOW)
        self.assertEqual(calls[1]["think"], False)
        self.assertEqual(calls[1]["tool_choice"], "TodoWrite")

    def test_unknown_provider_does_not_force_tool_choice(self):
        session = self.bare(provider="ollama")
        calls = []

        def fake_chat(self, messages, **kwargs):
            calls.append(kwargs)
            if len(calls) == 1:
                return {"content": "", "thinking": "still reasoning", "tool_calls": []}
            return {
                "content": "",
                "thinking": "",
                "tool_calls": [{
                    "id": "todo-2",
                    "type": "function",
                    "function": {"name": "TodoWrite", "arguments": {"items": ["Implement feature"]}},
                }],
            }

        bind(session, "_chat_with_same_model_retry", fake_chat)
        result = session._recover_thinking_only_response(
            {"content": "", "thinking": "original", "tool_calls": []},
            bootstrap=True,
            tools=session._single_no_plan_todo_bootstrap_tools(),
            pinned_selection="",
        )
        self.assertTrue(result["ok"])
        self.assertNotIn("tool_choice", calls[0])
        self.assertNotIn("tool_choice", calls[1])

    def test_deterministic_todo_preserves_numbered_stages_and_one_active(self):
        session = self.bare()
        session.runtime_authoritative_goal = "1. Inspect the repository\n2. Implement the fix\n3. Run tests"
        call = session._deterministic_bootstrap_todo_call()
        self.assertIsNotNone(call)
        args = call["function"]["arguments"]
        items = args["items"]
        self.assertEqual([row["content"] for row in items], [
            "Inspect the repository", "Implement the fix", "Run tests"
        ])
        self.assertEqual(sum(row.get("status") == "in_progress" for row in items), 1)
        self.assertEqual(args["in_progress_index"], 0)

    def test_non_bootstrap_repair_only_accepts_exposed_structured_tool(self):
        session = self.bare()
        bind(session, "_available_tools", lambda self: [
            cc.tool_def("read_file", "read", {"path": {"type": "string"}}),
        ])
        repaired = session._recover_inline_action_tool_call(
            'The call is ready: {"name":"read_file","arguments":{"path":"README.md"}}'
        )
        self.assertIsNotNone(repaired)
        self.assertEqual(repaired["function"]["name"], "read_file")
        self.assertEqual(repaired["function"]["arguments"]["path"], "README.md")
        self.assertIsNone(session._recover_inline_action_tool_call(
            'Run this: {"name":"write_file","arguments":{"path":"x"}}'
        ))

    def test_intervention_threshold_is_twenty(self):
        self.assertEqual(cc.EMPTY_ACTION_INTERVENTION_THRESHOLD, 20)
        self.assertEqual(cc.EMPTY_ACTION_BOOTSTRAP_THINKING_GRACE_ROUNDS, 10)

    def test_bootstrap_thinking_only_is_not_allowed_to_consume_generic_window(self):
        # The bootstrap writer turn has a stricter contract than ordinary
        # reasoning: a missing Todo call must immediately enter recovery.
        source = __import__("inspect").getsource(cc.SessionState._agent_worker)
        marker = "if empty_action and bootstrap_waiting_for_turn:"
        self.assertIn(marker, source)
        self.assertLess(source.index(marker), source.index("if empty_action:\n", source.index(marker)))
        # Initial bootstrap calls keep the provider's normal reasoning budget;
        # only the bounded recovery ladder disables thinking explicitly.
        self.assertNotIn("effort=EFFORT_OFF if bootstrap_waiting_for_turn", source)

    def test_provider_response_shapes_normalize_to_action_parts(self):
        client = cc.OllamaClient("http://localhost:1", "demo")
        content, calls, thinking = client._extract_openai_message({
            "choices": [{"message": {
                "content": "<think>decide</think>",
                "reasoning_content": "decide",
                "tool_calls": [{"id": "1", "function": {
                    "name": "TodoWrite", "arguments": '{"items":["Ship"]}'
                }}],
            }}]
        })
        self.assertEqual(content, "")
        self.assertEqual(thinking, "decide")
        self.assertEqual(calls[0]["function"]["name"], "TodoWrite")

        content, calls, thinking = client._extract_anthropic_message({
            "content": [
                {"type": "thinking", "thinking": "reason"},
                {"type": "tool_use", "id": "2", "name": "TodoWriteRescue", "input": {"items": ["Verify"]}},
            ]
        })
        self.assertEqual(content, "")
        self.assertEqual(thinking, "reason")
        self.assertEqual(calls[0]["function"]["name"], "TodoWriteRescue")

    def test_ollama_reasoning_models_receive_explicit_think_flag(self):
        client = cc.OllamaClient("http://localhost:1", "qwen3:8b")
        payloads = []

        def fake_post(url, payload):
            if url.endswith("/v1/chat/completions"):
                raise cc.OllamaError("unsupported", status=404)
            payloads.append(dict(payload))
            return {"message": {"content": "done"}}

        client._post_json = fake_post
        client._chat_impl(
            [{"role": "user", "content": "reply"}],
            max_tokens=32,
            think=False,
            effort=cc.EFFORT_OFF,
        )
        self.assertEqual(payloads[-1].get("think"), False)


if __name__ == "__main__":
    unittest.main()
