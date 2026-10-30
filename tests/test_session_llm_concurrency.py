import inspect
import json
import os
import tempfile
import threading
import time
import types
import unittest
from io import BytesIO
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

import Clouds_Coder as cc


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")
        self.headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self.body


def http_error(url, status=503, text="upstream unavailable"):
    return HTTPError(url, status, "error", {}, BytesIO(text.encode("utf-8")))


OK_BODY = {"choices": [{"message": {"content": "ok"}}]}


class BlockingTransport:
    """Stand-in for ``urlopen`` that holds each request until released."""

    def __init__(self):
        self.release = threading.Event()
        self.lock = threading.Lock()
        self.entered = []
        self.timeouts = []

    def __call__(self, req, timeout=None):
        with self.lock:
            self.entered.append(threading.current_thread().name)
            self.timeouts.append(timeout)
        if not self.release.wait(10):
            raise TimeoutError("test transport was never released")
        return FakeResponse(OK_BODY)

    def wait_entered(self, count, timeout=5.0):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self.lock:
                if len(self.entered) >= count:
                    return True
            time.sleep(0.01)
        return False


def wait_until(predicate, timeout=5.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.01)
    return False


def gated_client(limit=2, provider="openai_compat", base_url="http://model.test"):
    client = cc.OllamaClient(base_url, "demo-model", provider=provider)
    gate = cc.SessionLLMGate(limit)
    client.request_gate = gate
    return client, gate


def start_chat(client, results, key, **kwargs):
    def run():
        try:
            results[key] = client.chat([{"role": "user", "content": key}], **kwargs)
        except BaseException as exc:  # noqa: BLE001 - surfaced to the test
            results[key] = exc

    thread = threading.Thread(target=run, name=key, daemon=True)
    thread.start()
    return thread


def message_text(req):
    payload = json.loads(req.data.decode("utf-8"))
    return str(payload["messages"][-1]["content"])


class SessionLLMGateTests(unittest.TestCase):
    def setUp(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def tearDown(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def test_limit_two_with_three_threads_queues_the_third(self):
        client, gate = gated_client(limit=2)
        transport = BlockingTransport()
        results = {}
        with mock.patch.object(cc, "urlopen", side_effect=transport):
            threads = [start_chat(client, results, f"t{i}") for i in range(3)]
            try:
                self.assertTrue(transport.wait_entered(2))
                self.assertTrue(wait_until(lambda: gate.snapshot()["queued"] == 1))
                time.sleep(0.15)
                snap = gate.snapshot()
                self.assertEqual(len(transport.entered), 2)
                self.assertEqual(snap["in_flight"], 2)
                self.assertEqual(snap["queued_waits"], 1)
            finally:
                transport.release.set()
                for thread in threads:
                    thread.join(5)
        self.assertEqual(len(transport.entered), 3)
        self.assertTrue(all(results[key]["content"] == "ok" for key in ("t0", "t1", "t2")))
        final = gate.snapshot()
        self.assertEqual(final["peak"], 2)
        self.assertEqual(final["total"], 3)
        self.assertEqual(final["in_flight"], 0)
        self.assertEqual(final["queued"], 0)

    def test_auxiliary_is_skipped_without_blocking_when_full(self):
        client, gate = gated_client(limit=2)
        transport = BlockingTransport()
        results = {}
        with mock.patch.object(cc, "urlopen", side_effect=transport):
            holder = start_chat(client, results, "main")
            try:
                self.assertTrue(transport.wait_entered(1))
                started = time.monotonic()
                # limit 2 leaves max(0, limit-1) = 1 auxiliary slot ...
                aux_one = start_chat(client, results, "aux1", auxiliary=True)
                self.assertTrue(transport.wait_entered(2))
                # ... so a second auxiliary request is refused immediately.
                with self.assertRaises(cc.LLMGateBusy):
                    client.chat([{"role": "user", "content": "aux2"}], auxiliary=True)
                self.assertLess(time.monotonic() - started, 2.0)
                self.assertEqual(gate.snapshot()["skipped_busy"], 1)
                self.assertEqual(len(transport.entered), 2)
            finally:
                transport.release.set()
                holder.join(5)
                aux_one.join(5)
        self.assertEqual(results["aux1"]["content"], "ok")

    def test_auxiliary_with_limit_one_runs_only_when_idle(self):
        gate = cc.SessionLLMGate(1)
        ticket = gate.acquire(priority="main")
        with self.assertRaises(cc.LLMGateBusy):
            gate.acquire(auxiliary=True)
        gate.release(ticket)
        aux = gate.acquire(auxiliary=True)
        self.assertTrue(aux)
        gate.release(aux)
        self.assertEqual(gate.snapshot()["skipped_busy"], 1)

    def test_cancel_check_exits_the_wait(self):
        client, gate = gated_client(limit=1)
        transport = BlockingTransport()
        results = {}
        cancel = threading.Event()
        with mock.patch.object(cc, "urlopen", side_effect=transport):
            holder = start_chat(client, results, "holder")
            try:
                self.assertTrue(transport.wait_entered(1))
                waiter = start_chat(client, results, "waiter", cancel_check=cancel.is_set)
                self.assertTrue(wait_until(lambda: gate.snapshot()["queued"] == 1))
                cancel.set()
                waiter.join(2)
                self.assertFalse(waiter.is_alive())
                self.assertIsInstance(results["waiter"], cc.OllamaError)
                self.assertEqual(getattr(results["waiter"], "status", None), 499)
                self.assertIn("interrupted by user", str(results["waiter"]))
                self.assertEqual(gate.snapshot()["queued"], 0)
                self.assertEqual(len(transport.entered), 1)
            finally:
                transport.release.set()
                holder.join(5)
        self.assertEqual(gate.snapshot()["in_flight"], 0)

    def test_set_limit_two_to_one_takes_effect(self):
        gate = cc.SessionLLMGate(2)
        first = gate.acquire(priority="main")
        second = gate.acquire(priority="main")
        self.assertEqual(gate.set_limit(1), 1)
        self.assertEqual(gate.snapshot()["limit"], 1)
        gate.release(first)
        got = {}
        waiter = threading.Thread(target=lambda: got.setdefault("ticket", gate.acquire(priority="main")), daemon=True)
        waiter.start()
        self.assertTrue(wait_until(lambda: gate.snapshot()["queued"] == 1))
        time.sleep(0.3)
        # One request is still in flight and the new limit is 1, so it waits.
        self.assertNotIn("ticket", got)
        gate.release(second)
        waiter.join(2)
        self.assertIn("ticket", got)
        gate.release(got["ticket"])
        # Growing the limit back wakes nobody incorrectly and is clamped.
        self.assertEqual(gate.set_limit(99), cc.SESSION_LLM_CONCURRENCY_MAX)

    def test_main_beats_app_when_both_wait(self):
        gate = cc.SessionLLMGate(1)
        holder = gate.acquire(priority="main")
        order = []
        lock = threading.Lock()

        def worker(priority):
            ticket = gate.acquire(priority=priority, label=priority)
            with lock:
                order.append(priority)
            time.sleep(0.05)
            gate.release(ticket)

        app_thread = threading.Thread(target=worker, args=("app",), daemon=True)
        app_thread.start()
        self.assertTrue(wait_until(lambda: gate.snapshot()["queued"] == 1))
        main_thread = threading.Thread(target=worker, args=("main",), daemon=True)
        main_thread.start()
        self.assertTrue(wait_until(lambda: gate.snapshot()["queued"] == 2))
        gate.release(holder)
        app_thread.join(5)
        main_thread.join(5)
        # The app request queued first, but main is served first.
        self.assertEqual(order, ["main", "app"])
        self.assertEqual(gate.snapshot()["queued_waits"], 2)

    def test_stale_generation_entries_do_not_count_and_orphan_cap_blocks_auxiliary(self):
        gate = cc.SessionLLMGate(2, generation=0)
        stale = [gate.acquire(priority="main"), gate.acquire(priority="main")]
        self.assertEqual(gate.snapshot()["in_flight"], 2)
        gate.set_generation(1)
        snap = gate.snapshot()
        self.assertEqual(snap["in_flight"], 0)
        self.assertEqual(snap["orphaned_in_flight"], 2)
        self.assertEqual(snap["orphaned"], 2)
        self.assertTrue(all(row["orphaned"] for row in snap["requests"]))
        # Orphans from run 0 no longer use run 1's slots: blocking requests
        # are admitted immediately even though two old requests are running.
        current = gate.acquire(priority="main")
        self.assertEqual(gate.snapshot()["in_flight"], 1)
        # orphaned (2) >= limit (2): auxiliary requests are refused even
        # though a slot is still free for them.
        with self.assertRaises(cc.LLMGateBusy):
            gate.acquire(auxiliary=True)
        self.assertEqual(gate.snapshot()["skipped_busy"], 1)
        for ticket in stale:
            gate.release(ticket)
        aux = gate.acquire(auxiliary=True)
        self.assertTrue(aux)
        gate.release(aux)
        gate.release(current)
        final = gate.snapshot()
        self.assertEqual(final["in_flight_total"], 0)
        self.assertEqual(final["peak"], 2)

    def test_abandoned_requests_keep_their_slot_until_released(self):
        gate = cc.SessionLLMGate(1)
        ticket = gate.acquire(priority="main", label="arbiter")
        self.assertEqual(gate.mark_abandoned(threading.get_ident()), 1)
        snap = gate.snapshot()
        self.assertEqual(snap["abandoned"], 1)
        self.assertEqual(snap["in_flight"], 1)
        self.assertTrue(snap["requests"][0]["abandoned"])
        with self.assertRaises(cc.LLMGateBusy):
            gate.acquire(auxiliary=True)
        gate.release(ticket)
        self.assertEqual(gate.snapshot()["in_flight_total"], 0)

    def test_on_change_runs_outside_the_gate_lock(self):
        seen = []
        gate = cc.SessionLLMGate(2)

        def on_change(snapshot):
            # Re-entering the gate would deadlock if the lock were held.
            seen.append((snapshot["in_flight"], gate.snapshot()["limit"]))

        gate.on_change = on_change
        ticket = gate.acquire(priority="main")
        gate.release(ticket)
        self.assertEqual(seen, [(1, 2), (0, 2)])


class AuxiliaryCooldownTests(unittest.TestCase):
    def setUp(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def tearDown(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def test_openai_compat_auxiliary_failure_does_not_retry_or_write_cooldown(self):
        client, gate = gated_client(limit=2)

        def failing_urlopen(req, timeout=None):
            raise http_error(req.full_url)

        with mock.patch.object(cc, "urlopen", side_effect=failing_urlopen) as opened, \
                mock.patch.object(client, "_wait_with_cancel") as waited:
            with self.assertRaises(cc.OllamaError) as raised:
                client.chat([{"role": "user", "content": "aux"}], auxiliary=True)
        self.assertEqual(getattr(raised.exception, "status", None), 503)
        self.assertEqual(opened.call_count, 1)
        waited.assert_not_called()
        self.assertEqual(cc.OllamaClient._endpoint_cooldowns, {})
        # The failed request released its slot.
        self.assertEqual(gate.snapshot()["in_flight_total"], 0)

    def test_openai_compat_main_failure_still_writes_cooldown(self):
        # Positive control: the same failure on a main call keeps the
        # existing retry/cooldown behaviour.
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        responses = [http_error("http://model.test/v1/chat/completions"), FakeResponse(OK_BODY)]

        def fake_urlopen(req, timeout=None):
            item = responses.pop(0)
            if isinstance(item, BaseException):
                raise item
            return item

        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen), \
                mock.patch.object(client, "_wait_with_cancel") as waited:
            result = client.chat([{"role": "user", "content": "main"}])
        self.assertEqual(result["content"], "ok")
        self.assertTrue(waited.called)
        key = client._http_retry_key("http://model.test/v1/chat/completions")
        self.assertIn(key, cc.OllamaClient._endpoint_cooldowns)

    def test_ollama_fallback_path_auxiliary_failure_does_not_retry_or_write_cooldown(self):
        client = cc.OllamaClient("http://ollama.test:11434", "qwen3:8b", provider="ollama")
        opened = []

        def fake_urlopen(req, timeout=None):
            opened.append(req.full_url)
            raise http_error(req.full_url)

        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen), \
                mock.patch.object(client, "_wait_with_cancel") as waited:
            with self.assertRaises(cc.OllamaError):
                client.chat([{"role": "user", "content": "aux"}], auxiliary=True)
        # One attempt on /v1, then exactly one on the native /api/chat fallback.
        self.assertEqual(
            opened,
            ["http://ollama.test:11434/v1/chat/completions", "http://ollama.test:11434/api/chat"],
        )
        waited.assert_not_called()
        self.assertEqual(cc.OllamaClient._endpoint_cooldowns, {})

    def test_active_cooldown_skips_auxiliary_before_acquire_for_both_providers(self):
        # Keys come from the URLs the request paths really use; for Ollama the
        # cooldown is set on the native /api/chat fallback URL, which shares
        # the host-level key with /v1/chat/completions.
        cases = (
            ("openai_compat", "http://model.test", "http://model.test/v1/chat/completions"),
            ("ollama", "http://ollama.test:11434", "http://ollama.test:11434/api/chat"),
        )
        for provider, base, cooled_url in cases:
            with self.subTest(provider=provider):
                cc.OllamaClient._endpoint_cooldowns.clear()
                client, gate = gated_client(limit=2, provider=provider, base_url=base)
                key = client._http_retry_key(cooled_url)
                cc.OllamaClient._endpoint_cooldowns[key] = {"until": time.time() + 120.0}
                before = dict(cc.OllamaClient._endpoint_cooldowns)
                with mock.patch.object(cc, "urlopen") as opened, \
                        mock.patch.object(client, "_wait_with_cancel") as waited:
                    started = time.monotonic()
                    with self.assertRaises(cc.LLMGateBusy):
                        client.chat([{"role": "user", "content": "aux"}], auxiliary=True)
                    self.assertLess(time.monotonic() - started, 1.0)
                opened.assert_not_called()
                waited.assert_not_called()
                self.assertEqual(cc.OllamaClient._endpoint_cooldowns, before)
                snap = gate.snapshot()
                self.assertEqual(snap["skipped_busy"], 1)
                self.assertEqual(snap["total"], 0)

    def test_cooldown_set_after_precheck_is_not_waited_by_auxiliary(self):
        # The retry helper is the second guard: an auxiliary call that reaches
        # it while a cooldown is active raises LLMGateBusy instead of waiting.
        client = cc.OllamaClient("http://ollama.test:11434", "qwen3:8b", provider="ollama")
        url = "http://ollama.test:11434/api/chat"
        cc.OllamaClient._endpoint_cooldowns[client._http_retry_key(url)] = {"until": time.time() + 120.0}
        local = client._request_local()
        local.auxiliary = True
        try:
            with mock.patch.object(cc, "urlopen") as opened, \
                    mock.patch.object(client, "_wait_with_cancel") as waited:
                with self.assertRaises(cc.LLMGateBusy):
                    client._post_json("/api/chat", {"model": "qwen3:8b"}, max_attempts=0)
                with self.assertRaises(cc.LLMGateBusy):
                    list(client._iter_response_lines_url_with_retries(url, {"model": "qwen3:8b"}, max_attempts=0))
            opened.assert_not_called()
            waited.assert_not_called()
        finally:
            local.auxiliary = False

    def test_main_ollama_stream_and_fallback_keep_default_retry_budget(self):
        client = cc.OllamaClient("http://ollama.test:11434", "qwen3:8b", provider="ollama")
        seen = []

        def fake_post_json(path, payload, **kwargs):
            seen.append((path, kwargs))
            if path.endswith("/v1/chat/completions"):
                raise cc.OllamaError("unsupported", status=404)
            return {"message": {"content": "done"}}

        client._post_json = fake_post_json
        result = client.chat([{"role": "user", "content": "main"}])
        self.assertEqual(result["content"], "done")
        # Main calls keep the historical call shape (no max_attempts override).
        self.assertEqual(seen, [("/v1/chat/completions", {}), ("/api/chat", {})])
        seen.clear()
        client.chat([{"role": "user", "content": "aux"}], auxiliary=True)
        self.assertEqual(seen, [("/v1/chat/completions", {"max_attempts": 0}), ("/api/chat", {"max_attempts": 0})])

    def test_native_ollama_stream_receives_retry_budget(self):
        client = cc.OllamaClient("http://ollama.test:11434", "qwen3:8b", provider="ollama")
        captured = []

        def fake_lines(url, payload, headers=None, *, max_attempts=None, cancel_check=None, on_retry=None):
            captured.append((url, max_attempts))
            yield json.dumps({"message": {"content": "streamed"}, "done": True})

        client._iter_response_lines_url_with_retries = fake_lines
        result = client.chat([{"role": "user", "content": "aux"}], stream_thinking=True, auxiliary=True)
        self.assertEqual(result["content"], "streamed")
        client.chat([{"role": "user", "content": "main"}], stream_thinking=True)
        self.assertEqual(
            captured,
            [("http://ollama.test:11434/api/chat", 0), ("http://ollama.test:11434/api/chat", None)],
        )


class RequestTimeoutOverrideTests(unittest.TestCase):
    def setUp(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def tearDown(self):
        cc.OllamaClient._endpoint_cooldowns.clear()

    def test_per_call_timeout_reaches_urlopen_and_main_keeps_client_timeout(self):
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        self.assertGreaterEqual(client.timeout, cc.MIN_TIMEOUT_SECONDS)
        seen = []

        def fake_urlopen(req, timeout=None):
            seen.append((message_text(req), round(timeout, 3)))
            return FakeResponse(OK_BODY)

        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen):
            client.chat([{"role": "user", "content": "aux"}], auxiliary=True, request_timeout=6)
            client.chat([{"role": "user", "content": "main"}])
            client.chat([{"role": "user", "content": "short-main"}], request_timeout=15)
            client.chat([{"role": "user", "content": "main-again"}])
        self.assertEqual(
            seen,
            [
                ("aux", 6.0),
                ("main", client.timeout),
                ("short-main", 15.0),
                ("main-again", client.timeout),
            ],
        )
        self.assertEqual(round(client._effective_request_timeout(), 3), client.timeout)

    def test_override_is_thread_local(self):
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        inside = threading.Event()
        leave = threading.Event()
        seen = {}

        def fake_urlopen(req, timeout=None):
            name = message_text(req)
            seen[name] = round(timeout, 3)
            if name == "aux":
                inside.set()
                leave.wait(5)
            return FakeResponse(OK_BODY)

        with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen):
            results = {}
            aux = start_chat(client, results, "aux", auxiliary=True, request_timeout=3)
            try:
                self.assertTrue(inside.wait(5))
                # While the auxiliary request holds its 3s override on its own
                # thread, a main call on this thread still uses self.timeout.
                client.chat([{"role": "user", "content": "main"}])
            finally:
                leave.set()
                aux.join(5)
        self.assertEqual(seen["aux"], 3.0)
        self.assertEqual(seen["main"], client.timeout)

    def test_invalid_request_timeout_is_ignored(self):
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        for value in (0, -5, "soon", float("nan"), True):
            with self.subTest(value=value):
                self.assertIsNone(client._normalize_request_timeout_override(value))
        self.assertEqual(client._normalize_request_timeout_override(10**9), float(cc.MAX_TIMEOUT_SECONDS))


class TodoBudgetScopeTests(unittest.TestCase):
    def client(self):
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        client.calls = 0

        def fake_impl(messages, **kwargs):
            client.calls += 1
            return {"content": "ok", "thinking": "", "tool_calls": []}

        client._chat_impl = fake_impl
        return client

    def test_sixth_call_inside_scope_raises_and_outside_is_unlimited(self):
        client = self.client()
        with cc.todo_llm_budget_scope() as state:
            for _ in range(5):
                client.chat([{"role": "user", "content": "review"}])
            with self.assertRaises(cc.TodoLLMBudgetExhausted) as raised:
                client.chat([{"role": "user", "content": "review"}])
            self.assertIsInstance(raised.exception, cc.LLMGateBusy)
            self.assertEqual(state["used"], 5)
            self.assertEqual(state["denied"], 1)
        self.assertEqual(client.calls, 5)
        for _ in range(12):
            client.chat([{"role": "user", "content": "free"}])
        self.assertEqual(client.calls, 17)

    def test_nested_scopes_share_the_outer_counter_and_probes_are_free(self):
        client = self.client()
        with cc.todo_llm_budget_scope(limit=2) as outer:
            client.chat([{"role": "user", "content": "a"}])
            with cc.todo_llm_budget_scope(limit=50) as inner:
                self.assertIs(inner, outer)
                client.chat([{"role": "user", "content": "b"}])
                client.chat([{"role": "user", "content": "probe"}], probe_mode=True)
                with self.assertRaises(cc.TodoLLMBudgetExhausted):
                    client.chat([{"role": "user", "content": "c"}])
            self.assertEqual(outer["used"], 2)
        self.assertEqual(client.calls, 3)

    def test_budget_scope_is_thread_local(self):
        client = self.client()
        other = {}
        with cc.todo_llm_budget_scope(limit=1):
            client.chat([{"role": "user", "content": "inside"}])

            def run_other_thread():
                try:
                    for _ in range(3):
                        client.chat([{"role": "user", "content": "other thread"}])
                    other["ok"] = True
                except Exception as exc:
                    other["error"] = exc

            worker = threading.Thread(target=run_other_thread, daemon=True)
            worker.start()
            worker.join(5)
        self.assertEqual(other, {"ok": True})

    def test_exhausted_budget_sends_no_request_and_takes_no_slot(self):
        client, gate = gated_client(limit=2)
        with mock.patch.object(cc, "urlopen", side_effect=lambda req, timeout=None: FakeResponse(OK_BODY)) as opened:
            with cc.todo_llm_budget_scope(limit=1):
                client.chat([{"role": "user", "content": "first"}])
                with self.assertRaises(cc.TodoLLMBudgetExhausted):
                    client.chat([{"role": "user", "content": "second"}])
        self.assertEqual(opened.call_count, 1)
        snap = gate.snapshot()
        self.assertEqual(snap["total"], 1)
        self.assertEqual(snap["in_flight_total"], 0)


class SessionGateWiringTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "skills").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def make_session(self, sid="gate-session", **kwargs):
        return cc.SessionState(
            sid,
            sid,
            self.base / "sessions",
            "http://127.0.0.1:9",
            "demo-model",
            self.base / "skills",
            cc.CryptoBox(self.base / "crypto"),
            self.base,
            **kwargs,
        )

    def test_session_creates_one_gate_and_attaches_it_to_all_clients(self):
        session = self.make_session(session_llm_concurrency=3)
        try:
            gate = session.llm_gate
            self.assertIsInstance(gate, cc.SessionLLMGate)
            self.assertEqual(gate.limit, 3)
            self.assertIs(session.ollama.request_gate, gate)
            self.assertIs(session._build_arbiter_client().request_gate, gate)
            self.assertIs(session._build_auto_title_client().request_gate, gate)
            # Re-applying the active profile keeps the same gate attached.
            session._apply_active_profile()
            self.assertIs(session.ollama.request_gate, gate)
            self.assertIs(session._ensure_llm_gate(), gate)
        finally:
            session.bg.stop_all()

    def test_default_concurrency_and_clamping(self):
        session = self.make_session()
        try:
            self.assertEqual(session.session_llm_concurrency, cc.DEFAULT_SESSION_LLM_CONCURRENCY)
            self.assertEqual(session.set_session_llm_concurrency(0), 1)
            self.assertEqual(session.llm_gate.limit, 1)
            self.assertEqual(session.set_session_llm_concurrency("40"), 16)
            self.assertEqual(session.llm_gate.limit, 16)
        finally:
            session.bg.stop_all()

    def make_manager(self, **kwargs):
        return cc.SessionManager(
            self.base / "codes" / "user-a" / "sessions",
            "user-a",
            "http://127.0.0.1:9",
            "demo-model",
            self.base / "skills",
            self.base / "js_lib",
            cc.CryptoBox(self.base / "codes"),
            self.base,
            **kwargs,
        )

    def test_new_built_session_gets_gate_lazily_and_ignores_fake_clients(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ollama = types.SimpleNamespace(provider="openai_compat")
        session.run_generation = 4
        gate = session._ensure_llm_gate()
        self.assertIsInstance(gate, cc.SessionLLMGate)
        self.assertEqual(gate.limit, cc.DEFAULT_SESSION_LLM_CONCURRENCY)
        self.assertEqual(gate.generation, 4)
        self.assertIs(session._ensure_llm_gate(), gate)
        # Test doubles are left untouched.
        self.assertFalse(hasattr(session.ollama, "request_gate"))
        session.active_agent_role = "developer"
        ticket = gate.acquire(priority="main", label="main")
        self.assertEqual(gate.snapshot()["requests"][0]["role"], "developer")
        gate.release(ticket)

    def test_concurrency_round_trips_through_persisted_session_state(self):
        session = self.make_session("persist-session", session_llm_concurrency=5)
        try:
            session._persist()
        finally:
            session.bg.stop_all()
        restored = self.make_session("persist-session")
        try:
            self.assertEqual(restored.session_llm_concurrency, 5)
            self.assertEqual(restored.llm_gate.limit, 5)
            self.assertIs(restored.ollama.request_gate, restored.llm_gate)
        finally:
            restored.bg.stop_all()

    def test_run_generation_increment_orphans_previous_run_requests(self):
        manager = self.make_manager()
        session = manager.create("generation")
        try:
            gate = session.llm_gate
            start_generation = int(session.run_generation)
            self.assertEqual(gate.generation, start_generation)
            stale = gate.acquire(priority="main", label="previous-run")
            session._agent_worker = lambda: None
            result = session.submit_user_message("Start a new run.")
            self.assertTrue(result["running"])
            self.assertEqual(session.run_generation, start_generation + 1)
            snap = gate.snapshot()
            self.assertEqual(snap["generation"], session.run_generation)
            self.assertEqual(snap["in_flight"], 0)
            self.assertEqual(snap["orphaned_in_flight"], 1)
            gate.release(stale)
        finally:
            for _ in range(4):
                worker = getattr(session, "_persist_scheduler_thread", None)
                if worker is None:
                    break
                worker.join(timeout=2)
            session.bg.stop_all()

    def test_manager_propagates_and_defaults_resize_existing_gates(self):
        manager = self.make_manager(session_llm_concurrency=3)
        session = manager.create("propagation")
        try:
            self.assertEqual(manager.session_llm_concurrency, 3)
            self.assertEqual(session.session_llm_concurrency, 3)
            gate = session.llm_gate
            self.assertEqual(gate.limit, 3)
            manager.session_llm_concurrency = 1
            manager._apply_user_defaults_to_session(session, persist=False)
            self.assertIs(session.llm_gate, gate)
            self.assertEqual(gate.limit, 1)
            self.assertEqual(session.session_llm_concurrency, 1)
            manager._persist_user_prefs()
            self.assertEqual(self.make_manager().session_llm_concurrency, 1)
        finally:
            session.bg.stop_all()

    def test_live_admin_update_resizes_running_session_gates(self):
        manager = self.make_manager(session_llm_concurrency=2)
        session = manager.create("admin-live")
        app = cc.AppContext.__new__(cc.AppContext)
        app.base_url = "http://127.0.0.1:9"
        app.model = "demo-model"
        app._lock = threading.RLock()
        app._session_mgrs = {"user-a": manager}
        app._sync_global_ollama_defaults = lambda _active: None
        app.web_search_setting_locked = False
        app.user_memory_setting_locked = False
        config = {
            "provider": "openai_compat",
            "openai_url": "http://127.0.0.1:9/v1",
            "openai_model": "admin-model",
            "openai_key": "admin-secret",
            "runtime": {"session_llm_concurrency": 4},
        }
        try:
            gate = session.llm_gate
            with mock.patch.object(cc, "LLM_CONFIG_PATH", self.base / "LLM.config.json"), \
                    mock.patch.object(cc, "probe_and_merge_model_profiles", return_value=False), \
                    mock.patch.object(cc, "list_ollama_models_cached", return_value=[]):
                result = cc.AppContext.apply_global_llm_config(app, config, source="test")
            self.assertTrue(result["ok"], result)
            self.assertEqual(app.session_llm_concurrency, 4)
            self.assertEqual(manager.session_llm_concurrency, 4)
            self.assertEqual(session.session_llm_concurrency, 4)
            self.assertIs(session.llm_gate, gate)
            self.assertEqual(gate.limit, 4)
        finally:
            session.bg.stop_all()


class SessionLLMConcurrencyConfigTests(unittest.TestCase):
    def test_normalize_clamps_and_defaults(self):
        self.assertEqual(cc.SESSION_LLM_CONCURRENCY_FACTORY_DEFAULT, 2)
        # A list, not a dict: True and 1 would collide as dict keys.
        cases = [
            (None, cc.DEFAULT_SESSION_LLM_CONCURRENCY),
            ("", cc.DEFAULT_SESSION_LLM_CONCURRENCY),
            ("abc", cc.DEFAULT_SESSION_LLM_CONCURRENCY),
            (True, cc.DEFAULT_SESSION_LLM_CONCURRENCY),
            (0, 1),
            (-3, 1),
            (1, 1),
            ("3", 3),
            ("4.7", 4),
            (16, 16),
            (17, 16),
            (999, 16),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                self.assertEqual(cc.normalize_session_llm_concurrency(raw), expected)
        self.assertEqual(cc.normalize_session_llm_concurrency(None, default=7), 7)
        self.assertEqual(cc.normalize_session_llm_concurrency("bad", default=99), 16)

    def test_extract_reads_both_keys_top_level_and_sections(self):
        self.assertIsNone(cc.extract_session_llm_concurrency_setting({}))
        self.assertIsNone(cc.extract_session_llm_concurrency_setting("not a dict"))
        self.assertEqual(cc.extract_session_llm_concurrency_setting({"session_llm_concurrency": 3}), 3)
        self.assertEqual(cc.extract_session_llm_concurrency_setting({"llm_concurrency_per_session": "5"}), 5)
        self.assertEqual(cc.extract_session_llm_concurrency_setting({"runtime": {"session_llm_concurrency": 40}}), 16)
        self.assertEqual(cc.extract_session_llm_concurrency_setting({"limits": {"llm_concurrency_per_session": 0}}), 1)
        # Top-level keys win over sections, matching auto_task_level_ceiling.
        self.assertEqual(
            cc.extract_session_llm_concurrency_setting(
                {"session_llm_concurrency": 2, "runtime": {"session_llm_concurrency": 9}}
            ),
            2,
        )

    def test_env_default_is_read_and_clamped(self):
        for raw, expected in (("", 2), ("4", 4), ("0", 1), ("99", 16), ("junk", 2)):
            with self.subTest(raw=raw), mock.patch.dict(os.environ, {"AGENT_SESSION_LLM_CONCURRENCY": raw}):
                self.assertEqual(cc._session_llm_concurrency_env_default(), expected)

    def test_admin_schema_row_sits_next_to_auto_ceiling_and_round_trips(self):
        schema = cc._admin_config_schema()
        keys = [row["key"] for row in schema]
        row = schema[keys.index("session_llm_concurrency")]
        self.assertEqual(keys.index("session_llm_concurrency"), keys.index("auto_task_level_ceiling") + 1)
        self.assertEqual(row["group"], "runtime")
        self.assertEqual(row["label"], "In-session model request concurrency")
        self.assertEqual(row["type"], "integer")
        self.assertEqual(row["flag"], "--session-llm-concurrency")
        self.assertEqual((row["minimum"], row["maximum"]), (1, 16))
        self.assertEqual(row["factory_default"], cc.DEFAULT_SESSION_LLM_CONCURRENCY)
        self.assertIn("'In-session model request concurrency','会话内模型请求并发数'", cc.ADMIN_JS)

        clean, errors = cc._admin_coerce_config({"session_llm_concurrency": "4"})
        self.assertFalse(errors)
        self.assertEqual(clean["session_llm_concurrency"], 4)
        argv = cc._admin_config_to_argv({"session_llm_concurrency": 4})
        self.assertEqual(argv[argv.index("--session-llm-concurrency") + 1], "4")
        # An emptied admin field falls back to the default instead of "".
        argv = cc._admin_config_to_argv({"session_llm_concurrency": ""})
        self.assertEqual(
            argv[argv.index("--session-llm-concurrency") + 1],
            str(cc.DEFAULT_SESSION_LLM_CONCURRENCY),
        )
        _clean, errors = cc._admin_coerce_config({"session_llm_concurrency": 17})
        self.assertEqual([row["key"] for row in errors], ["session_llm_concurrency"])

    def test_startup_resolution_order_is_external_then_webui_then_cli(self):
        source = inspect.getsource(cc.main)
        default_pos = source.index("resolved_session_llm_concurrency = DEFAULT_SESSION_LLM_CONCURRENCY")
        external_pos = source.index("extract_session_llm_concurrency_setting(external_config)")
        web_pos = source.index("extract_session_llm_concurrency_setting(web_ui_config)")
        cli_pos = source.index('getattr(args, "session_llm_concurrency", None)')
        app_pos = source.index("session_llm_concurrency=resolved_session_llm_concurrency")
        self.assertLess(default_pos, external_pos)
        self.assertLess(external_pos, web_pos)
        self.assertLess(web_pos, cli_pos)
        self.assertLess(cli_pos, app_pos)
        self.assertIn('"--session-llm-concurrency"', source)
        self.assertIn('dest="session_llm_concurrency"', source)


def bind(instance, name, function):
    setattr(instance, name, types.MethodType(function, instance))


class BusyChat:
    """``chat`` stand-in that skips like a full session gate."""

    def __init__(self):
        self.calls = []

    def chat(self, messages, **kwargs):
        self.calls.append(dict(kwargs))
        raise cc.LLMGateBusy("in-session model slot busy (limit 1); auxiliary request skipped")


def step_skill_session(root):
    import test_step_skill_runtime as step_tests

    for name, description in (
        ("research", "Scientific literature and evidence synthesis"),
        ("briefing", "Design polished presentation decks"),
    ):
        step_tests.selection_tests._write_skill(root, name, f"name: {name}\ndescription: {description}")
    session = step_tests.selection_tests.SkillSelectionTests()._runtime_session(cc.SkillStore(root), mode="single", plan=True)
    session.max_agent_rounds = 20
    session.runtime_authoritative_goal = "Produce a research result"
    session.blackboard["original_goal"] = session.runtime_authoritative_goal
    session.blackboard["task_epoch"] = 100.0
    session._ensure_blackboard = types.MethodType(cc.SessionState._ensure_blackboard, session)
    session._blackboard_touch = types.MethodType(cc.SessionState._blackboard_touch, session)
    session._step_skill_restore_pending = False
    return session, step_tests


class AuxiliaryBusySkipTests(unittest.TestCase):
    def test_step_skill_busy_skip_restores_focus_and_requeues(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        session, step_tests = step_skill_session(Path(tmp.name))
        step_tests.set_step(session, 1, "Analyze the scientific literature")
        busy = BusyChat()
        session.ollama = busy
        state_before = session._normalize_step_skill_state(session.blackboard.get("step_skill_state"))

        result = session._maybe_recheck_step_skills(trigger="run-start")

        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "llm_gate_busy")
        call = busy.calls[0]
        self.assertTrue(call["auxiliary"])
        self.assertEqual(call["label"], "step_skill_eval")
        self.assertEqual(call["request_timeout"], cc.SKILL_RUNTIME_EVALUATION_TIMEOUT_SECONDS + 2.0)
        state = session._normalize_step_skill_state(session.blackboard["step_skill_state"])
        # The skipped evaluation left no trace of having evaluated the focus.
        self.assertEqual(state["focus_signature"], state_before["focus_signature"])
        self.assertEqual(state["last_evaluation_at"], state_before["last_evaluation_at"])
        self.assertNotEqual(state["evaluation_status"], "unavailable")
        self.assertIn("run-start", state["pending_triggers"])
        events = [row["event"] for row in session.blackboard.get("skill_runtime_events", [])]
        self.assertNotIn("step_skill_evaluation_failed", events)
        self.assertIn("skill_recheck_requested", events)
        self.assertNotIn("evaluation unavailable", session._loaded_skills_prompt_hint())

        # The next round evaluates for real once a slot is free.
        session.ollama = step_tests.ScriptedEvaluator(
            lambda payload: step_tests.evaluation(payload, load=["local:research"])
        )
        result = session._maybe_recheck_step_skills(trigger="single-round")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(len(session.ollama.calls), 1)
        self.assertEqual(step_tests.active(session), {"local:research"})

    def make_session(self, base, **kwargs):
        (base / "skills").mkdir(exist_ok=True)
        return cc.SessionState(
            "busy-session",
            "busy-session",
            base / "sessions",
            "http://model.test",
            "demo-model",
            base / "skills",
            cc.CryptoBox(base / "crypto"),
            base,
            **kwargs,
        )

    def test_arbiter_skips_when_gate_is_busy_and_aligns_socket_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            session = self.make_session(Path(tmp), session_llm_concurrency=1)
            try:
                session.arbiter_enabled = True
                session.arbiter_timeout_seconds = 3.0
                session.ollama.provider = "openai_compat"
                cc.OllamaClient._endpoint_cooldowns.clear()
                text = "I will now write the report file and run the verification script. " * 2
                gate = session.llm_gate
                ticket = gate.acquire(priority="main", label="main")
                try:
                    with mock.patch.object(cc, "urlopen") as transport:
                        decision = session._call_arbiter_llm(text, force=True)
                    transport.assert_not_called()
                finally:
                    gate.release(ticket)
                self.assertEqual(decision["status"], "ARBITER_SKIPPED")
                self.assertEqual(gate.snapshot()["skipped_busy"], 1)

                seen = []

                def fake_urlopen(req, timeout=None):
                    seen.append(round(timeout, 3))
                    return FakeResponse({"choices": [{"message": {"content": '{"status":"VALID_PLANNING","reasoning":"r"}'}}]})

                with mock.patch.object(cc, "urlopen", side_effect=fake_urlopen):
                    decision = session._call_arbiter_llm(text, force=True)
                self.assertEqual(decision["status"], "VALID_PLANNING")
                self.assertEqual(len(seen), 1)
                self.assertGreater(seen[0], 0.0)
                self.assertLessEqual(seen[0], 5.0)
                self.assertEqual(cc.OllamaClient._endpoint_cooldowns, {})
            finally:
                session.bg.stop_all()
                cc.OllamaClient._endpoint_cooldowns.clear()

    def subtask_review_session(self):
        import test_plan_todo_progression as plan_tests

        session = plan_tests.PlanTodoProgressionTests().bare_session("single")
        session.messages = []
        session.runtime_direct_objective = ""
        step_id = "pt:busy:000"
        step = {"id": step_id, "content": "1. 初始化模块", "full_content": "1. 初始化模块\n1.1 创建 src/expected-entry.js", "activated_at": 10.0}
        row = {"content": "1.1 创建 src/expected-entry.js", "parent_step_id": step_id, "created_at": 10.0}
        session.blackboard = {"plan_step_evidence": {step_id: [{
            "id": "ev:equivalent", "step_id": step_id, "subtask_id": "pst:old-binding",
            "subtask_content": "create an equivalent generated entry", "kind": "file", "tool": "write_file",
            "ok": True, "exit_code": None, "path": "src/generated-entry.js",
            "summary": "generated entry module created; syntax check passed", "ts": 20.0,
        }]}}
        return session, step, row, session._stable_plan_worker_subtask_id(step_id, row)

    def test_subtask_review_busy_skip_is_not_cached(self):
        session, step, row, subtask_id = self.subtask_review_session()
        session.ollama = BusyChat()
        review = session._llm_review_plan_subtask_completion(step, row, board=session.blackboard, subtask_id=subtask_id, since_ts=10.0)
        self.assertFalse(review["available"])
        self.assertTrue(review.get("skipped"))
        self.assertNotIn("plan_subtask_semantic_reviews", session.blackboard)

        verdict = {"content": (
            '{"decision":"pass","passed":true,"confidence":"high","reason":"equivalent module",'
            '"evidence":"ev:equivalent created and syntax checked","evidence_ids":["ev:equivalent"]}'
        )}
        session.ollama = types.SimpleNamespace(chat=mock.Mock(return_value=verdict))
        kwargs = {"board": session.blackboard, "subtask_id": subtask_id, "since_ts": 10.0}
        self.assertTrue(session._plan_worker_completion_has_evidence(step, row, **kwargs))
        self.assertTrue(session._plan_worker_completion_has_evidence(step, row, **kwargs))
        # One real verdict, then served from the cache.
        self.assertEqual(session.ollama.chat.call_count, 1)

    def test_subtask_review_cache_only_reuses_available_verdicts(self):
        session, step, row, subtask_id = self.subtask_review_session()
        session.ollama = types.SimpleNamespace(chat=mock.Mock(side_effect=RuntimeError("provider offline")))
        kwargs = {"board": session.blackboard, "subtask_id": subtask_id, "since_ts": 10.0}
        review = session._llm_review_plan_subtask_completion(step, row, **kwargs)
        self.assertFalse(review["available"])
        # The unavailable review is still recorded for diagnostics ...
        self.assertIn("plan_subtask_semantic_reviews", session.blackboard)
        cached, _candidates = session._cached_plan_subtask_semantic_review(step, row, **kwargs)
        # ... but never served from the cache.
        self.assertEqual(cached, {})
        session._llm_review_plan_subtask_completion(step, row, **kwargs)
        self.assertEqual(session.ollama.chat.call_count, 2)

    def test_enrichment_busy_skip_keeps_prior_status(self):
        import test_context_memory_recall as recall_tests

        session = recall_tests.ContextMemoryRecallTests().bare_session()
        session.lock = threading.RLock()
        body = "\n".join(["# Intro"] + [f"fact line {idx}" for idx in range(230)])
        source = session.files_root / "busy.md"
        source.write_text(body, encoding="utf-8")
        session.ollama = BusyChat()
        # A segment read marks the observation and starts enrichment itself.
        out = session._run_read("busy.md", mode="segment", segment_id="s0001")
        session._semantic_enrichment_worker.join(5)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(len(session.ollama.calls), 1)
        self.assertTrue(session.ollama.calls[0]["auxiliary"])
        # Skipped, not failed: no retry delay, and the next read tries again.
        self.assertEqual(memory["semantic_status"], "")
        self.assertEqual(memory["semantic_retry_at"], 0.0)
        self.assertTrue(memory["semantic_refresh_due"])
        self.assertEqual(memory["semantic_attempts"], 0)
        self.assertTrue(any(card.get("text") for card in memory["cards"]))
        session.ollama = mock.Mock()
        session.ollama.chat = mock.Mock(return_value={"content": '{"summary":"meaning","key_points":["p1"]}'})
        session._mark_long_content_read("busy.md", source, body.splitlines(), {"mode": "segment", "segment_id": "s0001"}, out)
        session._semantic_enrichment_worker.join(5)
        self.assertEqual(session.ollama.chat.call_count, 1)
        memory = next(iter(session.long_content_memory.values()))
        self.assertEqual(memory["semantic_status"], "ready")
        self.assertEqual(memory["semantic_attempts"], 1)


class AcceptanceVerifyHintTests(unittest.TestCase):
    def make_session(self, chat):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "en"
        session.todo = cc.TodoManager("en")
        session.messages = []
        session.plan_mode_user_preference = "auto"
        session.runtime_execution_mode = "single"
        session.execution_mode = "single"
        self.step = {"id": "pt:verify:000", "category": "plan_step", "status": "in_progress", "content": "1. Build the app"}
        session.blackboard = {"project_todos": [self.step], "step_files": {}, "execution_logs": []}
        session.todo.update([
            {"content": "1.1 create src/app.js", "status": "completed", "owner": "developer", "parent_step_id": self.step["id"]},
            {"content": "1.2 write the readme", "status": "in_progress", "owner": "developer", "parent_step_id": self.step["id"]},
        ])
        session.ollama = types.SimpleNamespace(chat=chat)
        bind(session, "_ensure_blackboard", lambda self: self.blackboard)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "_inject_runtime_environment_context", lambda self, text: text)
        bind(session, "_build_plan_guidance_notice_data", lambda self, text, summary="": {"summary": summary})
        bind(session, "_active_plan_worker_todo_rows", lambda self, step_id, role="": [
            dict(row) for row in self.todo.snapshot() if row.get("parent_step_id") == step_id
        ])
        return session

    def rework_hints(self, session):
        return [row for row in session.messages if "<step-rework>" in str(row.get("content", ""))]

    def test_verifier_reads_content_and_tags_auxiliary_call(self):
        chat = mock.Mock(return_value={"content": '{"all_passed": false, "rework_items": ["src/app.js was never written"]}'})
        session = self.make_session(chat)
        rows = [row for row in session.todo.snapshot() if row["status"] == "completed"]
        verdict = session._llm_verify_subtask_acceptance(self.step, rows, session.blackboard)
        self.assertEqual(verdict, {"available": True, "all_passed": False, "rework_items": ["src/app.js was never written"]})
        kwargs = chat.call_args.kwargs
        self.assertTrue(kwargs["auxiliary"])
        self.assertEqual(kwargs["label"], "acceptance_verify")
        self.assertEqual(kwargs["request_timeout"], cc.ACCEPTANCE_VERIFY_TIMEOUT_SECONDS)
        # Older clients that answer under "text" still parse.
        chat.return_value = {"text": 'verdict: {"all_passed": true, "rework_items": []}'}
        self.assertTrue(session._llm_verify_subtask_acceptance(self.step, rows, session.blackboard)["all_passed"])
        chat.side_effect = cc.LLMGateBusy("busy")
        self.assertFalse(session._llm_verify_subtask_acceptance(self.step, rows, session.blackboard)["available"])

    def test_rework_is_hinted_once_per_evidence_signature_without_status_changes(self):
        chat = mock.Mock(return_value={"content": '{"all_passed": false, "rework_items": ["src/app.js was never written"]}'})
        session = self.make_session(chat)
        before = [(row["content"], row["status"]) for row in session.todo.snapshot()]

        session._inject_rework_if_needed(self.step, {})
        hints = self.rework_hints(session)
        self.assertEqual(len(hints), 1)
        self.assertIn("src/app.js was never written", hints[0]["content"])
        self.assertIn("rework_completed", hints[0]["content"])
        self.assertEqual([(row["content"], row["status"]) for row in session.todo.snapshot()], before)
        self.assertEqual(chat.call_count, 1)

        # Same evidence: no second hint and no second model call, even after
        # the 30s rate-limit window.
        setattr(session, f"_rework_injected_{self.step['id']}", 0.0)
        session._inject_rework_if_needed(self.step, {})
        self.assertEqual(len(self.rework_hints(session)), 1)
        self.assertEqual(chat.call_count, 1)

        # Inside the rate-limit window (a check just ran) the model is not
        # called even when the evidence changed.
        setattr(session, f"_rework_injected_{self.step['id']}", cc.now_ts())
        session.blackboard["execution_logs"].append({"content": "node build.js -> ok"})
        session._inject_rework_if_needed(self.step, {})
        self.assertEqual(chat.call_count, 1)

        # New evidence after the window: one new check and one new hint.
        setattr(session, f"_rework_injected_{self.step['id']}", 0.0)
        chat.return_value = {"content": '{"all_passed": false, "rework_items": ["build output does not include src/app.js"]}'}
        session._inject_rework_if_needed(self.step, {})
        self.assertEqual(chat.call_count, 2)
        hints = self.rework_hints(session)
        self.assertEqual(len(hints), 2)
        self.assertIn("build output does not include src/app.js", hints[-1]["content"])
        self.assertEqual([(row["content"], row["status"]) for row in session.todo.snapshot()], before)

    def test_skipped_verifier_neither_hints_nor_consumes_the_signature(self):
        chat = mock.Mock(side_effect=cc.LLMGateBusy("busy"))
        session = self.make_session(chat)
        session._inject_rework_if_needed(self.step, {})
        self.assertEqual(self.rework_hints(session), [])
        chat.side_effect = None
        chat.return_value = {"content": '{"all_passed": false, "rework_items": ["missing file"]}'}
        setattr(session, f"_rework_injected_{self.step['id']}", 0.0)
        session._inject_rework_if_needed(self.step, {})
        self.assertEqual(len(self.rework_hints(session)), 1)


class SubagentCancelTests(unittest.TestCase):
    def make_session(self, round_delay=0.0):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "en"
        session.active_agent_role = ""
        self.rounds = []
        self.round_kwargs = []

        def fake_retry(self_, msgs, **kwargs):
            self.rounds.append(threading.current_thread().name)
            self.round_kwargs.append(dict(kwargs))
            if round_delay:
                time.sleep(round_delay)
            index = len(self.rounds)
            return {"content": f"round {index}", "tool_calls": [
                {"id": f"call-{index}", "function": {"name": "noop", "arguments": {}}}
            ]}

        bind(session, "_chat_with_same_model_retry", fake_retry)
        bind(session, "_loaded_skills_context_block", lambda self, **kwargs: "")
        bind(session, "_active_runtime_selection", lambda self: "demo")
        bind(session, "_missing_required_args", lambda self, name, args: [])
        bind(session, "_tool_result_context_content", lambda self, name, args, out: str(out))
        return session

    def test_cancel_token_stops_subagent_before_next_round(self):
        session = self.make_session()
        cancel = threading.Event()
        original = session._chat_with_same_model_retry

        def cancelling_retry(self_, msgs, **kwargs):
            response = original(msgs, **kwargs)
            if len(self.rounds) == 2:
                cancel.set()
            return response

        bind(session, "_chat_with_same_model_retry", cancelling_retry)
        out = session.run_subagent("explore", cancel_event=cancel)
        self.assertEqual(len(self.rounds), 2)
        self.assertEqual(out, "round 2")
        self.assertEqual(self.round_kwargs[0]["priority"], "subagent")
        self.assertEqual(self.round_kwargs[0]["label"], "subagent")

    def test_teammate_worker_uses_teammate_priority(self):
        session = self.make_session()
        seen = []
        bind(session, "run_subagent", lambda self, prompt, agent_type="Explore", **kwargs: seen.append(kwargs) or "done")
        session.teammates = {}
        session.lock = threading.RLock()
        session.bus = types.SimpleNamespace(send=lambda *args, **kwargs: None)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "_persist", lambda self: None)
        session._spawn_teammate("ana", "researcher", "look around")
        self.assertTrue(wait_until(lambda: session.teammates["ana"]["status"] == "idle"))
        self.assertEqual(seen, [{"priority": "teammate"}])

    def test_task_tool_timeout_cancels_subagent_on_next_round(self):
        session = self.make_session(round_delay=0.15)
        bind(session, "_flow_context", lambda self, role="", tool_call_id="": {"tool_start_evidence_id": "ev"})
        bind(session, "_sanitize_agent_role", lambda self, role: str(role or "").strip().lower())
        bind(session, "_guard_role_shell_mutation", lambda self, role, name, args: "")
        bind(session, "_trace_tool_result", lambda self, name, args, out, role="": out)
        bind(session, "_maybe_record_tool_memory_after_result", lambda self, *args, **kwargs: None)
        bind(session, "_record_tool_telemetry", lambda self, *args, **kwargs: None)
        bind(session, "_emit", lambda self, *args, **kwargs: None)
        bind(session, "_dispatch_tool_inner", lambda self, name, args, role_key="", tool_call_id="": self.run_subagent(
            args["prompt"], args.get("agent_type", "Explore")
        ))
        with mock.patch.dict(cc._TOOL_TIMEOUT_MAP, {"task": 0.2}):
            out = session._dispatch_tool("task", {"prompt": "explore the repo"}, "", "call-task")
        # The timeout result text is unchanged.
        self.assertEqual(
            out,
            "Error: tool 'task' timed out after 0.2 seconds. The operation may still be running in the background.",
        )
        self.assertEqual(session.tool_orphan_threads, 1)
        self.assertEqual(session.tool_orphan_threads_total, 1)
        # The round in flight when the timeout hit finishes; no further round starts.
        self.assertTrue(wait_until(lambda: session.tool_orphan_threads == 0, timeout=3.0))
        self.assertEqual(len(self.rounds), 2)
        time.sleep(0.4)
        self.assertEqual(len(self.rounds), 2)
        self.assertTrue(all(name.startswith("tool-task") for name in self.rounds))

    def test_fast_tool_does_not_count_as_orphan(self):
        session = self.make_session()
        bind(session, "_flow_context", lambda self, role="", tool_call_id="": {"tool_start_evidence_id": "ev"})
        bind(session, "_sanitize_agent_role", lambda self, role: str(role or "").strip().lower())
        bind(session, "_guard_role_shell_mutation", lambda self, role, name, args: "")
        bind(session, "_trace_tool_result", lambda self, name, args, out, role="": out)
        bind(session, "_maybe_record_tool_memory_after_result", lambda self, *args, **kwargs: None)
        bind(session, "_record_tool_telemetry", lambda self, *args, **kwargs: None)
        seen = []
        bind(session, "_dispatch_tool_inner", lambda self, name, args, role_key="", tool_call_id="": seen.append(
            self._current_tool_cancel_event()
        ) or "listed")
        self.assertEqual(session._dispatch_tool("list_skills", {}, "", "call-1"), "listed")
        self.assertIsInstance(seen[0], threading.Event)
        self.assertFalse(seen[0].is_set())
        self.assertEqual(int(getattr(session, "tool_orphan_threads", 0) or 0), 0)
        # Outside a timed tool there is no cancel flag.
        self.assertIsNone(session._current_tool_cancel_event())


class LLMConcurrencyMonitoringTests(unittest.TestCase):
    """A8: snapshot field, coalesced transient push and telemetry names."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        (self.base / "skills").mkdir()
        # Class-level table shared by every client; keep tests independent.
        cc.OllamaClient._endpoint_cooldowns.clear()

    def tearDown(self):
        cc.OllamaClient._endpoint_cooldowns.clear()
        self.tmp.cleanup()

    def make_session(self, sid="monitor-session", **kwargs):
        session = cc.SessionState(
            sid,
            sid,
            self.base / "sessions",
            "http://127.0.0.1:9",
            "demo-model",
            self.base / "skills",
            cc.CryptoBox(self.base / "crypto"),
            self.base,
            **kwargs,
        )
        self.addCleanup(session.bg.stop_all)
        return session

    def wait_quiet(self, session, timeout=5.0):
        """Wait until no coalesced push is pending or being sent."""
        return wait_until(lambda: session._llm_concurrency_push_timer is None, timeout=timeout)

    def test_full_snapshot_reports_live_gate_state_and_tool_orphans(self):
        session = self.make_session(session_llm_concurrency=3)
        gate = session.llm_gate
        session.active_agent_role = "developer"
        ticket = gate.acquire(priority="main", label="main")
        session.tool_orphan_threads = 2
        session.tool_orphan_threads_total = 5
        try:
            snap = session.snapshot()
        finally:
            gate.release(ticket)
        conc = snap["llm_concurrency"]
        self.assertEqual(conc["limit"], 3)
        self.assertEqual(conc["in_flight"], 1)
        self.assertEqual(conc["peak"], 1)
        self.assertEqual(conc["queued"], 0)
        self.assertEqual(conc["tool_orphan_threads"], 2)
        self.assertEqual(conc["tool_orphan_threads_total"], 5)
        self.assertEqual(len(conc["requests"]), 1)
        row = conc["requests"][0]
        self.assertEqual(
            set(row), {"id", "priority", "label", "role", "elapsed_seconds", "abandoned", "orphaned"}
        )
        self.assertEqual(row["label"], "main")
        self.assertEqual(row["role"], "developer")
        self.assertEqual(row["priority"], "main")
        self.assertFalse(row["abandoned"])
        self.assertGreaterEqual(row["elapsed_seconds"], 0.0)
        # Released: the next snapshot is live, not a stale copy.
        self.assertEqual(session.snapshot()["llm_concurrency"]["in_flight"], 0)

    def test_snapshot_request_rows_are_capped_at_sixteen(self):
        session = self.make_session(session_llm_concurrency=16)
        gate = session.llm_gate
        tickets = [gate.acquire(priority="main", label=f"call-{index}") for index in range(18)]
        try:
            conc = session.snapshot(lite=True)["llm_concurrency"]
            self.assertEqual(conc["in_flight"], 18)
            self.assertEqual(len(conc["requests"]), cc.SESSION_LLM_GATE_SNAPSHOT_MAX_REQUESTS)
            self.assertEqual(conc["requests"][0]["label"], "call-0")
        finally:
            for ticket in tickets:
                gate.release(ticket)

    def test_lite_cache_hit_returns_live_gate_state(self):
        session = self.make_session()
        gate = session.llm_gate
        self.assertTrue(self.wait_quiet(session))
        # A pushed llm_concurrency event takes the next session event_seq,
        # which is already part of the lite cache key, so a push causes one
        # cache miss by design.  Turn pushes off to test the cache-hit path.
        session._llm_concurrency_push_ready = False
        first = session.snapshot(lite=True)
        self.assertEqual(first["llm_concurrency"]["in_flight"], 0)
        ticket = gate.acquire(priority="main", label="main")
        try:
            # Gate state is not part of the lite cache key, so this is a
            # cache hit: the expensive projection must not run again.
            session._ui_message_is_countable = mock.Mock(
                side_effect=AssertionError("lite cache hit must not rebuild the projection")
            )
            with mock.patch.object(
                cc, "_apply_lite_snapshot_bounds",
                side_effect=AssertionError("lite cache hit must not rebuild the projection"),
            ):
                second = session.snapshot(lite=True)
            self.assertEqual(second["snapshot_revision"], first["snapshot_revision"])
            self.assertEqual(second["llm_concurrency"]["in_flight"], 1)
            self.assertEqual(second["llm_concurrency"]["requests"][0]["label"], "main")
            # The cached projection itself is not mutated by the patch.
            self.assertEqual(session._snapshot_cache_lite["llm_concurrency"]["in_flight"], 0)
        finally:
            gate.release(ticket)
        with mock.patch.object(
            cc, "_apply_lite_snapshot_bounds",
            side_effect=AssertionError("lite cache hit must not rebuild the projection"),
        ):
            third = session.snapshot(lite=True)
        self.assertEqual(third["llm_concurrency"]["in_flight"], 0)
        self.assertEqual(third["llm_concurrency"]["total"], 1)

    def test_degraded_snapshot_reports_live_gate_state(self):
        session = self.make_session()
        gate = session.llm_gate
        # Cached branch: an older lite projection exists.
        session.snapshot(lite=True)
        ticket = gate.acquire(priority="main", label="main")
        try:
            cached_view = session.degraded_snapshot("session lock busy")
            self.assertTrue(cached_view["degraded"])
            self.assertEqual(cached_view["llm_concurrency"]["in_flight"], 1)
            # Minimal branch: no cached projection at all.
            session._snapshot_cache_lite = {}
            session._snapshot_cache_full = {}
            bare_view = session.degraded_snapshot("session lock busy")
            self.assertTrue(bare_view["degraded"])
            self.assertEqual(bare_view["llm_concurrency"]["in_flight"], 1)
        finally:
            gate.release(ticket)

    def test_snapshot_safe_falls_back_to_live_degraded_view_when_lock_is_busy(self):
        session = self.make_session()
        gate = session.llm_gate
        session.snapshot_safe(lite=True)
        holder_ready = threading.Event()
        release_holder = threading.Event()

        def hold_lock():
            with session.lock:
                holder_ready.set()
                release_holder.wait(5)

        holder = threading.Thread(target=hold_lock, daemon=True)
        holder.start()
        self.assertTrue(holder_ready.wait(5))
        ticket = gate.acquire(priority="main", label="main")
        try:
            snap = session.snapshot_safe(lite=True, lock_timeout=0.05)
            self.assertTrue(snap["degraded"])
            self.assertEqual(snap["llm_concurrency"]["in_flight"], 1)
        finally:
            gate.release(ticket)
            release_holder.set()
            holder.join(5)

    def test_bare_session_snapshot_helper_is_empty_without_gate(self):
        session = cc.SessionState.__new__(cc.SessionState)
        self.assertEqual(session._llm_concurrency_snapshot(), {})
        # Pushes are off for half-built sessions; nothing is scheduled.
        session._on_llm_gate_change({})
        self.assertIsNone(getattr(session, "_llm_concurrency_push_timer", None))

    def test_gate_changes_are_coalesced_into_one_transient_push_per_second(self):
        session = self.make_session()
        gate = session.llm_gate
        self.assertTrue(self.wait_quiet(session))
        published = []
        operations_before = len(session.operations)
        activity_before = len(session.activity)
        session.running = True
        session.run_last_heartbeat = 123.0
        original_publish = session.events.publish

        def capture(event):
            published.append(dict(event))
            return original_publish(event)

        with mock.patch.object(session.events, "publish", side_effect=capture):
            started = time.monotonic()
            for index in range(10):
                ticket = gate.acquire(priority="main", label=f"burst-{index}")
                gate.release(ticket)
            gate.set_limit(3)
            burst_done = time.monotonic()
            self.assertTrue(wait_until(lambda: len(published) >= 1, timeout=3.0))
            self.assertTrue(self.wait_quiet(session))
            settled = time.monotonic()
        session.running = False
        events = [row for row in published if row.get("type") == "llm_concurrency"]
        self.assertEqual(len(events), len(published))
        self.assertTrue(1 <= len(events) <= 2, events)
        # The final state is never lost: the last push reflects every change.
        last = events[-1]["data"]
        self.assertEqual(last["limit"], 3)
        self.assertEqual(last["total"], 10)
        self.assertEqual(last["in_flight"], 0)
        self.assertEqual(events[-1]["session_id"], session.id)
        if len(events) == 2:
            # A trailing push waits out the interval after the first one.
            self.assertGreaterEqual(settled - started, cc.SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS * 0.9)
        self.assertLess(burst_done - started, 1.0)
        # Transient only: the 500-row operations log and activity are untouched,
        # and a background push does not refresh the run heartbeat.
        self.assertEqual(len(session.operations), operations_before)
        self.assertEqual(len(session.activity), activity_before)
        self.assertEqual(session.run_last_heartbeat, 123.0)

    def test_consecutive_pushes_are_at_least_one_interval_apart(self):
        session = self.make_session()
        gate = session.llm_gate
        self.assertTrue(self.wait_quiet(session))
        pushes = []
        original_publish = session.events.publish

        def capture(event):
            if event.get("type") == "llm_concurrency":
                pushes.append((time.monotonic(), dict(event.get("data") or {})))
            return original_publish(event)

        with mock.patch.object(session.events, "publish", side_effect=capture):
            gate.release(gate.acquire(priority="main", label="first"))
            self.assertTrue(wait_until(lambda: len(pushes) >= 1, timeout=3.0))
            self.assertTrue(self.wait_quiet(session))
            after_first_burst = len(pushes)
            gate.release(gate.acquire(priority="main", label="second"))
            self.assertTrue(wait_until(lambda: len(pushes) > after_first_burst, timeout=3.0))
            self.assertTrue(self.wait_quiet(session))
        # acquire and release each change the gate, so one burst yields one
        # push, or one push plus one trailing push, depending on thread timing.
        self.assertGreaterEqual(len(pushes), 2)
        stamps = [stamp for stamp, _data in pushes]
        for earlier, later in zip(stamps, stamps[1:]):
            self.assertGreaterEqual(
                later - earlier, cc.SESSION_LLM_CONCURRENCY_PUSH_INTERVAL_SECONDS * 0.9
            )
        # The newest state always arrives.
        self.assertEqual(pushes[-1][1]["total"], 2)
        self.assertEqual(pushes[-1][1]["in_flight"], 0)

    def test_push_runs_off_the_changing_thread_and_outside_the_gate_lock(self):
        session = self.make_session()
        gate = session.llm_gate
        self.assertTrue(self.wait_quiet(session))
        seen = []
        original_publish = session.events.publish

        def capture(event):
            # Probe from the publishing thread: a blocking acquire with a
            # timeout only fails if this thread itself still held the gate
            # lock (it is non-reentrant).
            acquired = gate._cond.acquire(timeout=1.0)
            if acquired:
                gate._cond.release()
            seen.append((threading.get_ident(), acquired))
            return original_publish(event)

        with mock.patch.object(session.events, "publish", side_effect=capture):
            # The gate itself publishes nothing on the changing thread.
            gate.release(gate.acquire(priority="main", label="main"))
            self.assertNotIn(threading.get_ident(), [ident for ident, _ok in seen])
            self.assertTrue(wait_until(lambda: len(seen) >= 1, timeout=3.0))
            self.assertTrue(self.wait_quiet(session))
        self.assertTrue(seen)
        self.assertTrue(all(ok for _ident, ok in seen))
        self.assertTrue(all(ident != threading.get_ident() for ident, _ok in seen))

    def test_restore_records_gate_changes_without_pushing(self):
        # A restored run_generation moves the gate inside _load_if_exists.
        # Pushing from there would publish half-restored state, so the change
        # is only recorded until the constructor finishes.
        original = self.make_session("restore-session")
        original.run_generation = 7
        original._persist()
        original.bg.stop_all()
        published = []
        original_publish = cc.EventHub.publish

        def capture(hub, event):
            if isinstance(event, dict) and event.get("type") == "llm_concurrency":
                published.append(dict(event))
            return original_publish(hub, event)

        with mock.patch.object(cc.EventHub, "publish", capture):
            restored = self.make_session("restore-session")
            self.assertEqual(restored.llm_gate.generation, 7)
            time.sleep(0.2)
            self.assertEqual(published, [])
            self.assertIsNone(restored._llm_concurrency_push_timer)
            self.assertTrue(restored._llm_concurrency_push_ready)
            # Once constructed, gate changes are pushed again.
            restored.llm_gate.release(restored.llm_gate.acquire(priority="main", label="main"))
            self.assertTrue(wait_until(lambda: len(published) >= 1, timeout=3.0))
            self.assertTrue(self.wait_quiet(restored))
        self.assertEqual(published[-1]["data"]["generation"], 7)
        self.assertEqual(published[-1]["data"]["total"], 1)

    def telemetry_client(self, telemetry_name="chat"):
        records = []
        client = cc.OllamaClient("http://model.test", "demo-model", provider="openai_compat")
        client.set_telemetry(lambda kind, **fields: records.append((kind, fields)), name=telemetry_name)
        client.request_gate = cc.SessionLLMGate(2)
        return client, records

    def test_telemetry_name_uses_label_and_keeps_fallbacks(self):
        client, records = self.telemetry_client()
        with mock.patch.object(cc, "urlopen", return_value=FakeResponse(OK_BODY)):
            client.chat([{"role": "user", "content": "x"}], label="main")
            client.chat([{"role": "user", "content": "x"}], auxiliary=True, label="semantic_enrichment")
            client.chat([{"role": "user", "content": "x"}])
            client.chat([{"role": "user", "content": "x"}], probe_mode=True, label="main")
        names = [fields["name"] for kind, fields in records if kind == "llm_call"]
        self.assertEqual(names, ["main", "semantic_enrichment", "chat", "capability_probe"])
        self.assertTrue(all(fields["status"] == "success" for _kind, fields in records))
        # Derived clients keep their own name when the caller sets no label.
        arbiter, arbiter_records = self.telemetry_client("arbiter")
        with mock.patch.object(cc, "urlopen", return_value=FakeResponse(OK_BODY)):
            arbiter.chat([{"role": "user", "content": "x"}])
        self.assertEqual(arbiter_records[0][1]["name"], "arbiter")

    def test_failed_labeled_call_is_recorded_under_its_label(self):
        client, records = self.telemetry_client()

        def failing_urlopen(req, timeout=None):
            raise http_error(req.full_url, status=400, text="bad request")

        with mock.patch.object(cc, "urlopen", side_effect=failing_urlopen):
            with self.assertRaises(cc.OllamaError):
                client.chat([{"role": "user", "content": "x"}], auxiliary=True, label="arbiter")
        self.assertEqual([(kind, fields["name"], fields["status"]) for kind, fields in records],
                         [("llm_call", "arbiter", "error")])

    def test_main_loop_calls_are_named_main_in_telemetry(self):
        session = self.make_session()
        records = []
        session.set_telemetry_callback(lambda kind, **fields: records.append((kind, fields)))
        bind(session, "_call_interruptible", lambda self, fn, **kwargs: fn())
        with mock.patch.object(session.ollama, "_iter_response_lines_url_with_retries", side_effect=lambda *_args, **_kwargs: iter([
            json.dumps({"message": {"content": "ok"}, "done": True, "done_reason": "stop"})
        ])):
            session._chat_with_same_model_retry(
                [{"role": "user", "content": "hello"}], context_label="agent turn", retries=0
            )
            session._chat_with_same_model_retry(
                [{"role": "user", "content": "hello"}], context_label="subagent", retries=0,
                priority="subagent", label="subagent",
            )
        llm = [fields for kind, fields in records if kind == "llm_call"]
        self.assertEqual([fields["name"] for fields in llm], ["main", "subagent"])
        self.assertTrue(all(fields["session_id"] == session.id for fields in llm))

    def test_dashboard_counts_every_llm_call_and_breaks_down_by_source(self):
        store = cc.TelemetryStore(self.base / "telemetry" / "telemetry.sqlite")
        for name, status in (
            ("main", "success"), ("main", "success"), ("semantic_enrichment", "timeout"),
            ("chat", "success"), ("capability_probe", "error"),
        ):
            store.record("llm_call", name=name, status=status, duration_ms=10.0, provider="openai_compat", model="m")
        store.record("tool_call", name="read_file", status="success", duration_ms=1.0)
        app = types.SimpleNamespace(_lock=threading.RLock(), _session_mgrs={})
        board = store.dashboard(app, since_hours=1.0)
        self.assertEqual(board["summary"]["llm_calls"], 5)
        self.assertEqual(board["summary"]["llm_success"], 3)
        self.assertEqual(board["summary"]["llm_failures"], 2)
        self.assertEqual(board["events"]["llm_call"]["count"], 5)
        self.assertEqual(sum(row["calls"] for row in board["models"]), 5)
        sources = {row["name"]: row["calls"] for row in board["llm_sources"]}
        self.assertEqual(sources, {"main": 2, "semantic_enrichment": 1, "chat": 1, "capability_probe": 1})
        self.assertEqual(sum(sources.values()), board["summary"]["llm_calls"])
        # Tool rows are not mixed into the llm source breakdown.
        self.assertEqual([row["name"] for row in board["tools"]], ["read_file"])

    def test_library_admin_session_rows_carry_live_concurrency(self):
        session = self.make_session("rag-row")
        gate = session.llm_gate
        ticket = gate.acquire(priority="app", label="rag_evaluate")
        try:
            row = cc.AppContext._session_row_llm_concurrency(session)
        finally:
            gate.release(ticket)
        self.assertEqual(row["in_flight"], 1)
        self.assertEqual(row["requests"][0]["label"], "rag_evaluate")
        self.assertEqual(cc.AppContext._session_row_llm_concurrency(types.SimpleNamespace()), {})


class LLMConcurrencyWebUITests(unittest.TestCase):
    """Run the new WebUI helpers in Node with a stubbed DOM."""

    NODE = "/Users/Fona/.nvm-arm64/versions/node/v24.13.0/bin/node"

    def node_binary(self):
        for candidate in (self.NODE, cc.shutil.which("node")):
            if candidate and os.path.exists(candidate):
                return candidate
        self.skipTest("Node.js is unavailable for the WebUI check")

    @staticmethod
    def js_line_function(source, name):
        start = source.index(f"function {name}(")
        return source[start:source.index("\n", start)]

    @staticmethod
    def js_block_function(source, name):
        start = source.index(f"function {name}(")
        return source[start:source.index("\n}\n", start) + 2]

    def run_node(self, script):
        completed = cc.subprocess.run(
            [self.node_binary(), "-e", script], capture_output=True, text=True, timeout=60
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_app_indicator_renders_snapshot_and_live_event(self):
        app = cc.APP_JS
        view = self.js_line_function(app, "_llmConcurrencyView")
        render = self.js_line_function(app, "renderLlmConcurrencyStat")
        on_event = self.js_block_function(app, "onRuntimeEvent")
        script = (
            "const I={stat_llm_concurrency:'模型并发',stat_llm_peak:'峰值',stat_llm_queued:'排队',"
            "stat_llm_orphaned:'孤儿',stat_llm_abandoned:'已放弃',stat_llm_no_requests:'none'};"
            "function t(k){return I[k]||k}"
            "const el={hidden:true,textContent:'',attrs:{},classList:{s:new Set(),toggle(c,on){on?this.s.add(c):this.s.delete(c)}},"
            "getAttribute(k){return this.attrs[k]??null},setAttribute(k,v){this.attrs[k]=String(v)},removeAttribute(k){delete this.attrs[k]}};"
            "function E(id){return id==='llmConcurrencyStat'?el:null}"
            "function setTextIfChanged(e,txt){if(e.textContent===txt)return false;e.textContent=txt;return true}"
            "const S={activeId:'s1',snap:{id:'s1'}};"
            "function _deltaConsumeSeq(){return{stale:false,gap:false}}"
            "function _renderBridgeEnqueue(){}"
            "function _deltaApplyRuntimeEvent(){return{handled:false,needsSnapshot:true}}\n"
            + view + "\n" + render + "\n" + on_event + "\n"
            "const out={};renderLlmConcurrencyStat();out.hiddenWithoutData=el.hidden;"
            "S.snap.llm_concurrency={limit:2,in_flight:1,peak:2,queued:0,requests:[{label:'main',role:'developer',elapsed_seconds:4.2}]};"
            "renderLlmConcurrencyStat();out.fromSnapshot=el.textContent;"
            "out.ret=onRuntimeEvent({type:'llm_concurrency',session_id:'s1',seq:3,data:{limit:2,in_flight:2,peak:3,queued:1,"
            "orphaned_in_flight:1,requests:[{label:'main',role:'developer',elapsed_seconds:12.4},"
            "{label:'semantic_enrichment',role:'',elapsed_seconds:3.6,abandoned:true,orphaned:true}]}});"
            "out.live=el.textContent;out.title=el.attrs.title;out.busy=el.classList.s.has('busy');"
            "onRuntimeEvent({type:'llm_concurrency',session_id:'other',seq:4,data:{limit:9,in_flight:0,peak:0,queued:0}});"
            "out.afterOtherSession=el.textContent;"
            "process.stdout.write(JSON.stringify(out));"
        )
        out = self.run_node(script)
        self.assertTrue(out["hiddenWithoutData"])
        self.assertEqual(out["fromSnapshot"], "模型并发 1/2 · 峰值 2 · 排队 0")
        self.assertEqual(out["ret"], {"handled": True, "needsSnapshot": False})
        self.assertEqual(out["live"], "模型并发 2/2 · 峰值 3 · 排队 1 · 孤儿 1")
        self.assertEqual(
            out["title"], "main · developer · 12s\nsemantic_enrichment · 4s (已放弃, 孤儿)"
        )
        self.assertTrue(out["busy"])
        self.assertEqual(out["afterOtherSession"], out["live"])

    def test_app_i18n_has_indicator_labels_in_every_language(self):
        start = cc.APP_JS.index("const I18N={")
        end = cc.APP_JS.index("\n};", start)
        packs = cc.APP_JS[start:end]
        for key in ("stat_llm_concurrency", "stat_llm_peak", "stat_llm_queued",
                    "stat_llm_orphaned", "stat_llm_abandoned", "stat_llm_no_requests"):
            self.assertEqual(packs.count(f"{key}:"), 4, key)
        self.assertIn("stat_llm_concurrency:'模型并发'", packs)
        self.assertIn("stat_llm_concurrency:'模型並行'", packs)
        self.assertIn("stat_llm_concurrency:'モデル並列'", packs)
        self.assertIn("stat_llm_concurrency:'Model concurrency'", packs)

    def test_library_admin_card_reads_selected_session_row(self):
        for source in (cc.RAG_ADMIN_JS, cc.CODE_ADMIN_JS):
            card = self.js_block_function(source, "sessionLlmConcurrencyCard")
            script = (
                "const S={config:{default_session_id:'a',sessions:[{id:'a',title:'Demo',llm_concurrency:{limit:2,"
                "in_flight:1,peak:2,queued:0,requests:[{label:'main',role:'developer',elapsed_seconds:4.2},"
                "{label:'arbiter',role:'',elapsed_seconds:1.0,abandoned:true}]}},{id:'b',title:'Idle',llm_concurrency:{}}]}};"
                "let picked='';function selectedSession(){return picked}\n"
                + card + "\n"
                "const out={a:sessionLlmConcurrencyCard()};picked='b';out.b=sessionLlmConcurrencyCard();"
                "process.stdout.write(JSON.stringify(out));"
            )
            out = self.run_node(script)
            self.assertEqual(out["a"]["value"], "1/2")
            self.assertEqual(out["a"]["meta"], "peak 2 · queued 0 · Demo")
            self.assertEqual(out["a"]["tip"], "main · developer · 4s\narbiter · 1s (abandoned)")
            self.assertIsNone(out["b"])


if __name__ == "__main__":
    unittest.main()
