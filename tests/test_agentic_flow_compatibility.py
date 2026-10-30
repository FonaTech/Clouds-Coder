"""Protocol compatibility and paired full-workflow promotion gates."""

import json
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane
from liquid_kernel.agentic import compare_agentic_flows
from liquid_kernel.models import EvolutionModels, prioritize_model_options


class ThinkingCompatibilityTests(unittest.TestCase):
    def app(self, rounds=5):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = LiquidKernelControlPlane(Path(temp.name))
        original = app.liquid_kernel.config()
        original["task_benchmark"].update(max_rounds=rounds, turn_max_tokens=8192)
        app.liquid_kernel.config = lambda: original
        app._liquid_kernel_profile = lambda _: {
            "provider": "openai_compat",
            "base_url": "http://model.test",
            "model": "hybrid",
            "effort": "",
        }
        return app

    def test_reasoning_only_turns_continue_without_format_repair_and_respect_admin_rounds(
        self,
    ):
        app = self.app(3)
        replies = [
            {
                "content": "",
                "thinking": "Derive the acceptance evidence.",
                "raw": {"done_reason": "length"},
            },
            {
                "content": "",
                "thinking": "Verify both requirements.",
                "raw": {"done_reason": "stop"},
            },
            {"content": '{"ok":true}', "raw": {"done_reason": "stop"}},
        ]
        with mock.patch.object(cc.OllamaClient, "chat", side_effect=replies) as chat:
            result = app._liquid_kernel_transport_call(
                "Return JSON when ready.", "{}", "", 1024
            )
        self.assertTrue(result["ok"])
        self.assertEqual(
            [r.kwargs["max_tokens"] for r in chat.call_args_list], [1024, 2048, 4096]
        )
        self.assertTrue(all(r.kwargs["effort"] == "" for r in chat.call_args_list))
        self.assertIn(
            "Derive the acceptance evidence.", str(chat.call_args_list[1].args)
        )
        self.assertTrue(
            all(r.kwargs["label"] == "evolution_json" for r in chat.call_args_list)
        )
        app = self.app(1)
        with mock.patch.object(
            cc.OllamaClient, "chat", return_value=replies[0]
        ) as chat:
            with self.assertRaises(cc.LiquidKernelError) as caught:
                app._liquid_kernel_transport_call("JSON", "{}", "", 1024)
        self.assertEqual(chat.call_count, 1)
        self.assertEqual(caught.exception.code, "structured_round_budget_exhausted")
        self.assertFalse(caught.exception.details["semantic_repair_attempted"])

    def test_native_worker_reasoning_does_not_force_tool_or_file_write(self):
        from liquid_kernel.context import RECALL_TOOL

        app = self.app()
        prompt = json.dumps(
            {
                "messages": [{"role": "user", "content": "Think then act"}],
                "tools": [RECALL_TOOL],
            }
        )
        with mock.patch.object(
            cc.OllamaClient,
            "chat",
            return_value={"thinking": "Check the evidence first.", "content": ""},
        ):
            result = app._liquid_kernel_transport_call(
                "Use tools when useful.", prompt, "", 1024
            )
        self.assertTrue(result["continue"])
        self.assertEqual(result["tool_calls"], [])
        self.assertEqual(result["reasoning_content"], "Check the evidence first.")

    def test_non_thinking_model_finishes_without_a_continuation(self):
        with mock.patch.object(
            cc.OllamaClient, "chat", return_value={"content": '{"ok":true}'}
        ) as chat:
            result = self.app()._liquid_kernel_transport_call("JSON", "{}", "", 1024)
        self.assertTrue(result["ok"])
        self.assertEqual(chat.call_count, 1)

    def test_auto_does_not_force_reasoning_and_explicit_off_uses_native_switch(self):
        for name in ["deepseek-v4.1-flash", "glm-5.3-flash", "plain-model"]:
            self.assertEqual(
                cc.resolve_reasoning_payload("openai_compat", name, ""), {}
            )
        self.assertEqual(
            cc.resolve_reasoning_payload("openai_compat", "plain-model", "off"), {}
        )
        self.assertEqual(
            cc.resolve_reasoning_payload("openai_compat", "deepseek-v4.1-flash", "off")[
                "payload"
            ],
            {"thinking": {"type": "disabled"}},
        )

    def test_shared_history_preserves_exact_reasoning_for_native_tool_turns(self):
        client = cc.OllamaClient(
            "http://model.test", "hybrid", provider="openai_compat"
        )
        thought = "Evidence trace." * 4000
        source = [
            {
                "role": "assistant",
                "content": "",
                "thinking": thought,
                "tool_calls": [
                    {
                        "id": "x",
                        "type": "function",
                        "function": {"name": "read_file", "arguments": {"path": "a"}},
                    }
                ],
            },
            {"role": "tool", "name": "read_file", "tool_call_id": "x", "content": "ok"},
        ]
        outgoing = client._prepare_request_messages(source, "openai_compat")
        self.assertEqual(outgoing[0]["reasoning_content"], thought)
        self.assertEqual(source[0]["thinking"], thought)
        native = client._prepare_request_messages(source, "ollama")
        self.assertEqual(native[0]["thinking"], thought)
        text = (
            "data: "
            + json.dumps(
                {
                    "choices": [
                        {
                            "delta": {"reasoning_content": thought},
                            "finish_reason": "tool_calls",
                        }
                    ]
                }
            )
            + "\n"
        )
        self.assertEqual(
            client._openai_stream_result_from_lines([text])["thinking"], thought
        )

    def test_parameter_fallback_preserves_output_ceiling_and_unrejected_json_format(
        self,
    ):
        payload = {
            "model": "m",
            "messages": [],
            "max_tokens": 16384,
            "thinking": {"type": "disabled"},
            "response_format": {"type": "json_object"},
        }
        stripped = cc.OllamaClient._compat_payload_after_error(
            payload, ["thinking"], cc.OllamaError("unsupported thinking", status=400)
        )
        self.assertNotIn("thinking", stripped)
        self.assertEqual(stripped["max_tokens"], 16384)
        self.assertEqual(stripped["response_format"], payload["response_format"])
        renamed = cc.OllamaClient._compat_payload_after_error(
            payload, [], cc.OllamaError("unsupported max_tokens", status=400)
        )
        self.assertEqual(renamed["max_completion_tokens"], 16384)
        self.assertNotIn("max_tokens", renamed)
        minimal = cc.OllamaClient._compat_payload_after_error(
            payload, [], cc.OllamaError("InvalidParameter", status=400)
        )
        self.assertEqual(minimal["max_tokens"], 16384)

    def test_stream_finish_reason_is_preserved_even_after_usage_only_event(self):
        client = cc.OllamaClient("http://model.test", "model")
        events = [
            {
                "choices": [
                    {
                        "delta": {"reasoning_content": "still thinking"},
                        "finish_reason": None,
                    }
                ]
            },
            {"choices": [{"delta": {}, "finish_reason": "length"}]},
            {"choices": [], "usage": {"total_tokens": 1024}},
        ]
        result = client._openai_stream_result_from_lines(
            ["data: " + json.dumps(e) + "\n" for e in events]
        )
        self.assertEqual(result["raw"]["done_reason"], "length")
        self.assertEqual(result["thinking"], "still thinking")


class DeadlineTests(unittest.TestCase):
    def test_real_http_trickle_stream_and_backoff_share_total_call_deadline(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                if self.path.startswith("/retry"):
                    self.send_response(503)
                    self.send_header("Retry-After", "60")
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                try:
                    for _ in range(100):
                        self.wfile.write(b"x")
                        self.wfile.flush()
                        time.sleep(0.025)
                except (BrokenPipeError, ConnectionResetError):
                    pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for suffix in ["/stream", "/retry"]:
                client = cc.OllamaClient(
                    f"http://127.0.0.1:{server.server_port}",
                    "plain-model",
                    provider="openai_compat",
                    endpoint=f"http://127.0.0.1:{server.server_port}{suffix}",
                )
                started = time.monotonic()
                with self.assertRaises(cc.OllamaError):
                    client.chat(
                        [{"role": "user", "content": "x"}],
                        max_tokens=128,
                        response_stream=True,
                        request_timeout=0.3,
                    )
                self.assertLess(time.monotonic() - started, 1.1)
                self.assertFalse(getattr(client._request_local(), "deadline", 0))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(2)


class ModelOrderingTests(unittest.TestCase):
    def test_configured_models_precede_discovery_across_all_profiles(self):
        profiles = {
            "p1": {"model": "z", "models": ["z", "a"], "configured_models": ["z"]},
            "p2": {"model": "y", "models": ["y", "b"], "configured_models": ["y"]},
        }
        options = [
            {"profile_id": p, "model": m}
            for p in profiles
            for m in profiles[p]["models"]
        ]
        self.assertEqual(
            [x["model"] for x in prioritize_model_options(options, profiles)],
            ["z", "y", "a", "b"],
        )
        model = EvolutionModels(
            lambda *_: (profiles, "p1"), lambda _: [{"id": "a"}], lambda *_: {}, b"key"
        )
        self.assertEqual(model.model_ids(profiles["p1"]), ["z", "a"])
        before = model.fingerprint(model.effective(profiles["p1"], "z"))
        profiles["p1"]["configured_models"].append("a")
        self.assertEqual(
            before, model.fingerprint(model.effective(profiles["p1"], "z"))
        )

    def test_probe_retains_original_config_provenance(self):
        profile = {"model": "z", "models": ["z"]}
        cc.merge_probed_models_into_profile(profile, [{"id": "a"}])
        self.assertEqual(profile["configured_models"], ["z"])
        self.assertIn("a", profile["models"])


class AgenticFlowComparisonTests(unittest.TestCase):
    def result(self, contract="base", tokens=100, rounds=10, score=100):
        return {
            "score": score,
            "success_rate": 1,
            "rows": [
                {
                    "task_id": key,
                    "task_fingerprint": key,
                    "split": split,
                    "success": True,
                    "score": score,
                    "checks": [{"index": 0, "ok": True}],
                    "flow_contracts": [contract],
                    "accounted_tokens": tokens,
                    "rounds": rounds,
                    "failed_tool_calls": 0,
                }
                for key, split in [("a", "train"), ("b", "holdout")]
            ],
        }

    def test_unchanged_flow_and_subjective_review_cannot_qualify(self):
        self.assertFalse(
            compare_agentic_flows(self.result(), self.result(tokens=20, rounds=2))[
                "eligible"
            ]
        )
        self.assertFalse(
            compare_agentic_flows(self.result(), self.result("candidate"))["eligible"]
        )

    def test_actual_efficiency_gain_requires_quality_and_holdout(self):
        result = compare_agentic_flows(
            self.result(), self.result("candidate", tokens=20, rounds=2)
        )
        self.assertTrue(result["eligible"])
        self.assertGreater(result["holdout_efficiency_delta"], 0)
        bad = self.result("candidate", tokens=20, rounds=2)
        bad["rows"][1]["checks"][0]["ok"] = False
        self.assertFalse(compare_agentic_flows(self.result(), bad)["eligible"])
        bad = self.result("candidate", tokens=20, rounds=2, score=99)
        self.assertFalse(compare_agentic_flows(self.result(), bad)["eligible"])

    def test_mismatched_frozen_tasks_cannot_be_compared(self):
        candidate = self.result("candidate", tokens=20, rounds=2)
        candidate["rows"][0]["task_fingerprint"] = "other"
        self.assertFalse(compare_agentic_flows(self.result(), candidate)["eligible"])
