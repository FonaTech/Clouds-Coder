import http.client
import json
import shlex
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

import Clouds_Coder as cc


def wait_for_status(manager, process_id, terminal=True, timeout=5.0):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        last = manager.get_process(process_id)
        active = last["status"] in manager.ACTIVE_STATUSES
        if active != terminal:
            return last
        time.sleep(0.03)
    raise AssertionError(f"process {process_id} did not reach expected state: {last}")


class UserProcessManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manager = cc.UserProcessManager()
        self.background = cc.BackgroundManager(
            self.root,
            process_manager=self.manager,
            owner_user_id="user-alpha",
            session_id="session-alpha",
            session_title="Alpha session",
        )

    def tearDown(self):
        self.background.stop_all()
        self.temp.cleanup()

    def _sleep_command(self, seconds=30):
        return f"{shlex.quote(sys.executable)} -c " + shlex.quote(
            f"import time; time.sleep({seconds})"
        )

    def test_background_run_is_registered_completes_and_redacts_secrets(self):
        message = self.background.run(
            "API_KEY=topsecret printf 'token=output-secret'", timeout=5
        )
        process_id = message.split()[2]
        row = wait_for_status(self.manager, process_id)

        self.assertEqual(row["status"], "completed")
        self.assertEqual(row["exit_code"], 0)
        self.assertEqual(row["session_id"], "session-alpha")
        self.assertNotIn("topsecret", row["command"])
        detail = self.manager.get_process(process_id, owner_user_id="user-alpha")
        self.assertNotIn("output-secret", detail["output_tail"])
        self.assertNotIn(str(self.root), json.dumps(detail))

    def test_running_process_can_be_stopped_and_process_group_is_reaped(self):
        message = self.background.run(self._sleep_command(), timeout=60)
        process_id = message.split()[2]
        deadline = time.time() + 3
        while time.time() < deadline:
            row = self.manager.get_process(process_id)
            if row["status"] == "running":
                break
            time.sleep(0.02)
        else:
            self.fail("background process never reached running state")

        stopped = self.manager.stop_process(
            process_id,
            owner_user_id="user-alpha",
            actor="user:test",
            reason="test stop",
        )
        self.assertTrue(stopped["ok"])
        row = wait_for_status(self.manager, process_id)
        self.assertEqual(row["status"], "terminated")
        self.assertEqual(row["termination_actor"], "user:test")
        self.assertEqual(row["termination_reason"], "test stop")

    def test_adopted_async_process_uses_same_registry(self):
        process = subprocess.Popen(
            [sys.executable, "-c", "print('adopted')"],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            start_new_session=(sys.platform != "win32"),
        )
        process_id = self.background.adopt_process(
            process,
            "python adopted-job",
            cwd=self.root,
            idle_timeout_seconds=10,
            hard_timeout_seconds=10,
        )
        row = wait_for_status(self.manager, process_id)
        self.assertEqual(row["source"], "bash_async_handoff")
        self.assertEqual(row["status"], "completed")
        self.assertIn("adopted", self.manager.get_process(process_id)["output_tail"])

    def test_owner_isolation_hides_foreign_processes_and_rejects_stop(self):
        self.manager.register(
            process_id="bg_foreign",
            task_id="bg_foreign",
            owner_user_id="user-beta",
            session_id="session-beta",
            session_title="Beta",
            command="sleep 1",
            cwd=self.root,
            source="background_run",
            started_at=time.time(),
            status="running",
            terminator=lambda: None,
        )
        own = self.manager.list_processes(owner_user_id="user-alpha")
        self.assertEqual(own["processes"], [])
        with self.assertRaises(cc.ProcessManagerError) as missing:
            self.manager.get_process("bg_foreign", owner_user_id="user-alpha")
        self.assertEqual(missing.exception.status, 404)
        with self.assertRaises(cc.ProcessManagerError):
            self.manager.stop_process(
                "bg_foreign", owner_user_id="user-alpha", actor="user:test"
            )

    def test_bulk_stop_requires_scope_and_honors_user_filter(self):
        stopped = []
        for index, owner in enumerate(("user-alpha", "user-alpha", "user-beta")):
            key = f"bg_{index}"
            self.manager.register(
                process_id=key,
                task_id=key,
                owner_user_id=owner,
                session_id=f"session-{owner}",
                session_title=owner,
                command="long task",
                cwd=self.root,
                source="background_run",
                started_at=time.time(),
                status="running",
                terminator=lambda value=key: stopped.append(value),
            )
        with self.assertRaises(cc.ProcessManagerError) as unscoped:
            self.manager.bulk_stop(actor="admin")
        self.assertEqual(unscoped.exception.code, "bulk_filter_required")

        user_hash = cc.UserProcessManager._user_hash("user-alpha")
        result = self.manager.bulk_stop(actor="admin", user_hash=user_hash)
        self.assertEqual(result["matched"], 2)
        self.assertEqual(set(stopped), {"bg_0", "bg_1"})


class _ProcessHTTPApp:
    def __init__(self, manager):
        self.process_manager = manager
        self.admin_token = "cc_admin_" + "p" * 40

    def verify_admin_token(self, token):
        return "token" if str(token or "") == self.admin_token else ""

    def manager_for_user(self, user_id):
        return object()


class ProcessManagerHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manager = cc.UserProcessManager()
        self.user_id = cc.user_id_from_ip("127.0.0.1")
        self.background = cc.BackgroundManager(
            self.root,
            process_manager=self.manager,
            owner_user_id=self.user_id,
            session_id="session-http",
            session_title="HTTP session",
        )
        self.app = _ProcessHTTPApp(self.manager)
        self.server = cc.AgentHTTPServer(("127.0.0.1", 0), cc.Handler, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.background.stop_all()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method, path, body=None, headers=None):
        port = self.server.server_address[1]
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        request_headers = dict(headers or {})
        request_headers.setdefault("Origin", f"http://127.0.0.1:{port}")
        payload = None
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        conn.request(method, path, body=payload, headers=request_headers)
        response = conn.getresponse()
        raw = response.read()
        conn.close()
        return response.status, json.loads(raw.decode("utf-8")) if raw else {}

    def test_user_routes_are_owner_scoped_and_admin_routes_require_auth(self):
        own_id = self.background.run(
            f"{shlex.quote(sys.executable)} -c "
            + shlex.quote("import time; time.sleep(30)"),
            timeout=60,
        ).split()[2]
        self.manager.register(
            process_id="bg_other",
            task_id="bg_other",
            owner_user_id="another-user",
            session_id="other-session",
            session_title="Other",
            command="foreign command",
            cwd=self.root,
            source="background_run",
            started_at=time.time(),
            status="running",
            terminator=lambda: None,
        )
        deadline = time.time() + 3
        while time.time() < deadline:
            if self.manager.get_process(own_id)["status"] == "running":
                break
            time.sleep(0.02)

        status, own = self.request("GET", "/api/processes")
        self.assertEqual(status, 200)
        self.assertEqual([row["id"] for row in own["processes"]], [own_id])
        status, hidden = self.request("GET", "/api/processes/bg_other")
        self.assertEqual(status, 404)
        self.assertEqual(hidden["code"], "process_not_found")

        status, _ = self.request("GET", "/api/admin/processes")
        self.assertEqual(status, 401)
        admin_header = {"Authorization": "Bearer " + self.app.admin_token}
        status, all_rows = self.request(
            "GET", "/api/admin/processes", headers=admin_header
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            {row["id"] for row in all_rows["processes"]}, {own_id, "bg_other"}
        )

        status, denied = self.request(
            "POST", "/api/processes/bg_other/stop", {"reason": "not mine"}
        )
        self.assertEqual(status, 404)
        self.assertEqual(denied["code"], "process_not_found")
        status, stopped = self.request(
            "POST", f"/api/processes/{own_id}/stop", {"reason": "done"}
        )
        self.assertEqual(status, 200)
        self.assertTrue(stopped["ok"])

    def test_admin_bulk_stop_requires_explicit_confirmation(self):
        headers = {"Authorization": "Bearer " + self.app.admin_token}
        status, denied = self.request(
            "POST",
            "/api/admin/processes/bulk-stop",
            {"ids": ["bg_missing"]},
            headers,
        )
        self.assertEqual(status, 400)
        self.assertEqual(denied["code"], "confirmation_required")


class ProcessManagerEmbeddedUITests(unittest.TestCase):
    def test_main_and_admin_pages_include_process_management(self):
        self.assertIn('id="userProcesses"', cc.INDEX_HTML)
        self.assertIn("/api/processes?limit=100", cc.APP_JS)
        self.assertIn('data-view="processes"', cc.ADMIN_INDEX_HTML)
        self.assertIn("/api/admin/processes/bulk-stop", cc.ADMIN_JS)


class ProcessManagerAgentToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.manager = cc.UserProcessManager()
        self.current = cc.BackgroundManager(
            self.root / "current",
            process_manager=self.manager,
            owner_user_id="user-alpha",
            session_id="session-current",
            session_title="Current",
        )
        self.other = cc.BackgroundManager(
            self.root / "other",
            process_manager=self.manager,
            owner_user_id="user-alpha",
            session_id="session-other",
            session_title="Other",
        )
        self.foreign = cc.BackgroundManager(
            self.root / "foreign",
            process_manager=self.manager,
            owner_user_id="user-beta",
            session_id="session-foreign",
            session_title="Foreign",
        )
        self.session = cc.SessionState.__new__(cc.SessionState)
        self.session.id = "session-current"
        self.session.owner_user_id = "user-alpha"
        self.session.bg = self.current

    def tearDown(self):
        self.current.stop_all()
        self.other.stop_all()
        self.foreign.stop_all()
        self.temp.cleanup()

    @staticmethod
    def _sleep_command(seconds=30):
        return f"{shlex.quote(sys.executable)} -c " + shlex.quote(
            f"import time; time.sleep({seconds})"
        )

    def _start(self, background):
        process_id = background.run(self._sleep_command(), timeout=60).split()[2]
        deadline = time.time() + 3
        while time.time() < deadline:
            if self.manager.get_process(process_id)["status"] == "running":
                return process_id
            time.sleep(0.02)
        self.fail(f"process {process_id} did not reach running state")

    def test_agent_tools_are_owner_scoped_across_sessions_and_stop_exact_id(self):
        current_id = self._start(self.current)
        other_id = self._start(self.other)
        foreign_id = self._start(self.foreign)

        payload = json.loads(
            self.session._dispatch_tool_inner(
                "list_background_processes", {}, "developer"
            )
        )
        rows = {row["id"]: row for row in payload["processes"]}
        self.assertEqual(set(rows), {current_id, other_id})
        self.assertEqual(rows[current_id]["session_scope"], "current_session")
        self.assertEqual(rows[other_id]["session_scope"], "other_session")
        self.assertNotIn("user_hash", json.dumps(payload))
        self.assertNotIn(foreign_id, json.dumps(payload))

        detail = json.loads(
            self.session._dispatch_tool_inner(
                "list_background_processes", {"process_id": other_id}, "developer"
            )
        )
        self.assertEqual(detail["process"]["id"], other_id)
        self.assertIn("output_tail", detail["process"])

        denied = self.session._dispatch_tool_inner(
            "stop_background_process",
            {"process_id": foreign_id, "reason": "must remain hidden"},
            "developer",
        )
        self.assertIn("process_not_found", denied)
        stopped = json.loads(
            self.session._dispatch_tool_inner(
                "stop_background_process",
                {"process_id": other_id, "reason": "agent cleanup"},
                "developer",
            )
        )
        self.assertTrue(stopped["ok"])
        row = wait_for_status(self.manager, other_id)
        self.assertEqual(row["status"], "terminated")
        self.assertEqual(row["termination_actor"], "agent:developer")
        self.assertEqual(row["termination_reason"], "agent cleanup")

        prompt = self.session._background_processes_prompt_block()
        self.assertIn("current-authenticated-user scope", prompt)
        self.assertIn(current_id, prompt)
        self.assertNotIn(foreign_id, prompt)

    def test_agent_tool_contracts_and_empty_registry(self):
        list_spec = cc.TOOL_SPEC_BY_NAME["list_background_processes"]["function"]
        stop_spec = cc.TOOL_SPEC_BY_NAME["stop_background_process"]["function"]
        self.assertNotIn("user_id", list_spec["parameters"]["properties"])
        self.assertNotIn("user_id", stop_spec["parameters"]["properties"])
        self.assertEqual(stop_spec["parameters"]["required"], ["process_id"])
        self.assertIn("list_background_processes", cc.PLAN_MODE_RESEARCH_TOOL_ALLOWLIST)
        self.assertNotIn(
            "stop_background_process", cc.PLAN_MODE_RESEARCH_TOOL_ALLOWLIST
        )
        self.assertIn("list_background_processes", cc.AGENT_TOOL_ALLOWLIST["explorer"])
        self.assertNotIn("stop_background_process", cc.AGENT_TOOL_ALLOWLIST["explorer"])
        self.assertIn("stop_background_process", cc.AGENT_TOOL_ALLOWLIST["developer"])
        self.assertIn("list_background_processes", cc.CONVERSATION_VISIBLE_TOOL_EVENTS)
        self.assertIn("stop_background_process", cc.CONVERSATION_VISIBLE_TOOL_EVENTS)

        empty = json.loads(
            self.session._dispatch_tool_inner(
                "list_background_processes", {}, "developer"
            )
        )
        self.assertEqual(empty["processes"], [])
        self.assertEqual(empty["total"], 0)
        missing = self.session._dispatch_tool_inner(
            "stop_background_process", {}, "developer"
        )
        self.assertIn("process_id_required", missing)


if __name__ == "__main__":
    unittest.main()
