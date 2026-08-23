import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

import Clouds_Coder as cc


class _RagAuthApp:
    def __init__(self, root: Path):
        self.admin_auth = cc.AdminAuthStore(root / "admin_auth.sqlite")
        self.admin_token = "cc_admin_" + "a" * 40
        self.rag_rebuild_count = 0
        self.code_rebuild_count = 0

    def verify_admin_token(self, token):
        candidate = str(token or "").strip()
        if candidate == self.admin_token:
            return "token"
        return "session" if self.admin_auth.verify_session(candidate) else ""

    def admin_auth_status(self, *, local_setup_allowed):
        configured = self.admin_auth.configured()
        return {
            "setup_required": not configured,
            "password_login_enabled": configured,
            "token_login_enabled": True,
            "local_setup_allowed": bool(not configured and local_setup_allowed),
            "setup_local_only": True,
            "session_ttl_seconds": cc.ADMIN_AUTH_SESSION_TTL_SECONDS,
        }

    def setup_admin(
        self, username, password, *, local_setup_allowed, bootstrap_token=""
    ):
        if self.admin_auth.configured():
            raise cc.AdminAuthError(
                "setup_already_completed", "already configured", 409
            )
        if (
            not local_setup_allowed
            and self.verify_admin_token(bootstrap_token) != "token"
        ):
            raise cc.AdminAuthError("setup_local_only", "local setup required", 403)
        return self.admin_auth.setup(username, password)

    def login_admin(self, username, password, client_ip):
        if not self.admin_auth.configured():
            raise cc.AdminAuthError("setup_required", "setup required", 409)
        return self.admin_auth.login(username, password, client_ip)

    def exchange_admin_token(self, token):
        if self.verify_admin_token(token) != "token":
            raise cc.AdminAuthError("invalid_token", "invalid token", 401)
        return self.admin_auth.issue_session(username_key="__token__", auth_version=0)

    def logout_admin(self, token):
        self.admin_auth.revoke_session(token)

    def rag_rebuild(self):
        self.rag_rebuild_count += 1
        return {"ok": True, "kind": "rag"}

    def code_rebuild(self):
        self.code_rebuild_count += 1
        return {"ok": True, "kind": "code"}

    @staticmethod
    def web_ui_rag_admin_index_html():
        return cc.RAG_ADMIN_INDEX_HTML

    @staticmethod
    def web_ui_rag_admin_style_css():
        return cc.RAG_ADMIN_CSS

    @staticmethod
    def web_ui_rag_admin_js():
        return cc.RAG_ADMIN_JS

    @staticmethod
    def web_ui_code_admin_index_html():
        return cc.CODE_ADMIN_INDEX_HTML

    @staticmethod
    def web_ui_code_admin_style_css():
        return cc.CODE_ADMIN_CSS

    @staticmethod
    def web_ui_code_admin_js():
        return cc.CODE_ADMIN_JS


class RagAdminAuthenticationHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = _RagAuthApp(Path(self.temp.name))
        self.servers = {}
        self.threads = []
        for name, handler in (
            ("rag", cc.RagAdminHandler),
            ("code", cc.CodeAdminHandler),
        ):
            server = cc.AgentHTTPServer(("127.0.0.1", 0), handler, self.app)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.servers[name] = server
            self.threads.append(thread)

    def tearDown(self):
        for server in self.servers.values():
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, service, method, path, body=None, headers=None, *, origin=True):
        server = self.servers[service]
        port = server.server_address[1]
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        payload = None
        request_headers = dict(headers or {})
        if origin:
            request_headers.setdefault("Origin", f"http://127.0.0.1:{port}")
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        conn.request(method, path, body=payload, headers=request_headers)
        response = conn.getresponse()
        raw = response.read()
        response_headers = dict(response.getheaders())
        conn.close()
        if response_headers.get("Content-Type", "").startswith("application/json"):
            data = json.loads(raw.decode("utf-8")) if raw else {}
        else:
            data = raw.decode("utf-8")
        return response.status, data, response_headers

    def test_both_pages_include_complete_auth_ui_without_prompt_token_login(self):
        for service, script_path in (
            ("rag", "/assets/rag-admin.js"),
            ("code", "/assets/code-admin.js"),
        ):
            status, html, _ = self.request(service, "GET", "/")
            self.assertEqual(status, 200)
            self.assertIn('id="authOverlay"', html)
            self.assertIn('id="passwordLoginForm"', html)
            self.assertIn('id="setupForm"', html)
            self.assertIn('id="readOnlyBtn"', html)
            status, script, _ = self.request(service, "GET", script_path)
            self.assertEqual(status, 200)
            self.assertNotIn(
                "prompt('Admin token required for library changes')", script
            )
            self.assertIn("/api/admin/auth/token-login", script)
            self.assertIn("bootstrapAuth()", script)

    def test_setup_login_shared_session_logout_and_write_enforcement(self):
        status, auth_status, _ = self.request("rag", "GET", "/api/admin/auth/status")
        self.assertEqual(status, 200)
        self.assertTrue(auth_status["setup_required"])
        self.assertTrue(auth_status["local_setup_allowed"])

        status, denied, _ = self.request("rag", "POST", "/api/rag/rebuild", {})
        self.assertEqual(status, 401)
        self.assertEqual(denied["code"], "unauthorized")

        credentials = {"username": "library-admin", "password": "Strong-Admin-123!"}
        status, setup, _ = self.request(
            "rag", "POST", "/api/admin/auth/setup", credentials
        )
        self.assertEqual(status, 201)
        session = setup["access_token"]
        self.assertTrue(session.startswith("cc_session_"))

        auth_header = {"Authorization": "Bearer " + session}
        status, state, _ = self.request(
            "code", "GET", "/api/admin/auth/session", headers=auth_header
        )
        self.assertEqual(status, 200)
        self.assertEqual(state["auth_kind"], "session")

        status, rebuilt, _ = self.request(
            "code", "POST", "/api/code/rebuild", {}, auth_header
        )
        self.assertEqual(status, 200)
        self.assertEqual(rebuilt["kind"], "code")
        self.assertEqual(self.app.code_rebuild_count, 1)

        status, _, _ = self.request(
            "rag", "POST", "/api/admin/auth/logout", {}, auth_header
        )
        self.assertEqual(status, 200)
        status, _, _ = self.request(
            "code", "GET", "/api/admin/auth/session", headers=auth_header
        )
        self.assertEqual(status, 401)

        status, login, _ = self.request(
            "code", "POST", "/api/admin/auth/login", credentials
        )
        self.assertEqual(status, 200)
        self.assertTrue(login["access_token"].startswith("cc_session_"))

    def test_token_exchange_cross_origin_and_content_type_controls(self):
        token_header = {"Authorization": "Bearer " + self.app.admin_token}
        status, exchanged, _ = self.request(
            "rag", "POST", "/api/admin/auth/token-login", {}, token_header
        )
        self.assertEqual(status, 200)
        self.assertTrue(exchanged["access_token"].startswith("cc_session_"))

        port = self.servers["code"].server_address[1]
        status, rejected, _ = self.request(
            "code",
            "POST",
            "/api/admin/auth/token-login",
            {},
            {**token_header, "Origin": "http://malicious.example"},
        )
        self.assertEqual(status, 403)
        self.assertEqual(rejected["code"], "cross_origin")

        status, invalid, _ = self.request(
            "code",
            "POST",
            "/api/admin/auth/token-login",
            headers={
                **token_header,
                "Origin": f"http://127.0.0.1:{port}",
                "Content-Type": "text/plain",
                "Content-Length": "0",
            },
        )
        self.assertEqual(status, 415)
        self.assertEqual(invalid["code"], "invalid_content_type")


if __name__ == "__main__":
    unittest.main()
