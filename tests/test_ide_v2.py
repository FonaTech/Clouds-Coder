import base64
import http.client
import inspect
import io
import json
import os
import sqlite3
import tempfile
import threading
import time
import types
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


class OfflineJSAssetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "js_lib"
        self.root.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_incomplete_package_is_not_treated_as_complete(self):
        entry = {
            "id": "sample",
            "filename": "main.js",
            "relative_path": "sample/dist/main.js",
            "package_urls": ["https://example.invalid/sample.tgz"],
            "package_install_dir": "sample",
            "package_required_paths": ["package.json", "dist/main.js"],
        }
        partial = self.root / "sample" / "dist"
        partial.mkdir(parents=True)
        (partial / "unrelated.js").write_text("partial", encoding="utf-8")
        ok, source, error, _ = cc._ensure_offline_js_package(
            self.root, entry, allow_download=False
        )
        self.assertFalse(ok)
        self.assertEqual(source, "download-disabled")
        self.assertIn("incomplete", error)

    def test_package_glob_minimum_is_enforced(self):
        package = self.root / "sample"
        (package / "dist" / "fonts").mkdir(parents=True)
        (package / "package.json").write_text("{}", encoding="utf-8")
        for index in range(2):
            (package / "dist" / "fonts" / f"font-{index}.woff2").write_bytes(b"font")
        self.assertFalse(
            cc._package_install_ready(
                package,
                ["package.json"],
                [("dist/fonts/*.woff2", 3)],
            )
        )
        (package / "dist" / "fonts" / "font-2.woff2").write_bytes(b"font")
        self.assertTrue(
            cc._package_install_ready(
                package,
                ["package.json"],
                [("dist/fonts/*.woff2", 3)],
            )
        )

    def test_existing_asset_and_disabled_download_never_use_http(self):
        existing = self.root / "monaco" / "min" / "vs" / "loader.js"
        existing.parent.mkdir(parents=True)
        existing.write_text("window.require = {};", encoding="utf-8")
        with mock.patch.object(cc, "_download_http_bytes") as download:
            resolved, reason = cc.ensure_offline_js_asset(
                self.root, "monaco/min/vs/loader.js", allow_download=False
            )
            self.assertEqual(resolved, existing.resolve())
            self.assertEqual(reason, "existing")
            missing, reason = cc.ensure_offline_js_asset(
                self.root, "codicons/dist/codicon.css", allow_download=False
            )
        self.assertIsNone(missing)
        self.assertEqual(reason, "download-disabled")
        download.assert_not_called()

    def test_connection_deadline_still_indexes_every_catalog_entry(self):
        catalog = [
            {
                "id": "one",
                "filename": "one.js",
                "urls": ["https://example.invalid/one.js"],
            },
            {
                "id": "two",
                "filename": "two.js",
                "urls": ["https://example.invalid/two.js"],
            },
        ]
        with (
            mock.patch.object(cc, "OFFLINE_JS_LIB_CATALOG", catalog),
            mock.patch.object(cc, "_download_http_bytes") as download,
        ):
            summary = cc.ensure_offline_js_libs(
                Path(self.tmp.name), no_connection_deadline=-1
            )
        self.assertEqual(summary["catalog_total"], 2)
        self.assertEqual(len([row for row in summary["libs"] if row.get("catalog")]), 2)
        self.assertEqual(summary["missing"], 2)
        download.assert_not_called()

    def test_session_html_localization_honors_disabled_downloads(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.js_lib_root = self.root
        session.js_lib_download_enabled = False
        with mock.patch.object(cc, "_download_http_bytes") as download:
            resolved, reason = session._resolve_offline_js_asset_for_url(
                "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"
            )
        self.assertIsNone(resolved)
        self.assertEqual(reason, "download-disabled")
        download.assert_not_called()

    def test_source_bundle_honors_disabled_downloads(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app.workspace = Path(self.tmp.name)
        app.skills_root = Path(self.tmp.name) / "skills"
        app.skills_root.mkdir()
        app.js_lib_root = self.root
        app.js_lib_download_enabled = False
        with (
            mock.patch.object(cc, "ensure_runtime_skills"),
            mock.patch.object(cc, "ensure_offline_js_libs") as ensure_all,
        ):
            bundle = app.source_bundle()
        self.assertGreater(len(bundle), 1000)
        ensure_all.assert_not_called()

    def test_chat_submission_uses_short_upload_handoff_and_keeps_post_path(self):
        self.assertIn("const CHAT_UPLOAD_HANDOFF_WAIT_MS=250;", cc.APP_JS)
        self.assertIn("waitForPendingUploads(handoffWait)", cc.APP_JS)
        self.assertNotIn("waitForPendingUploads(10000)", cc.APP_JS)
        self.assertIn(
            '"chat_upload_frontend_wait_ms": int(CHAT_UPLOAD_FRONTEND_WAIT_MS)',
            inspect.getsource(cc.Handler.do_GET),
        )

    def test_session_manager_does_not_probe_ollama_during_construction(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            crypto = cc.CryptoBox(root / "codes")
            with mock.patch.object(
                cc,
                "probe_ollama_environment",
                side_effect=AssertionError("probe must be lazy"),
            ):
                manager = cc.SessionManager(
                    root / "sessions",
                    "user-a",
                    "http://127.0.0.1:11434",
                    "demo-model",
                    root / "skills",
                    root / "js_lib",
                    crypto,
                    root,
                    False,
                    {},
                    "zh-CN",
                    cc.DEFAULT_CONTEXT_TOKEN_LIMIT,
                    False,
                    cc.MAX_AGENT_ROUNDS,
                    cc.MAX_RUN_SECONDS,
                    cc.DEFAULT_SHELL_COMMAND_TIMEOUT_SECONDS,
                    cc.DEFAULT_AUTO_TASK_LEVEL_CEILING,
                    cc.DEFAULT_L2_TODO_POLICY,
                    False,
                    True,
                    "",
                    cc.ARBITER_DEFAULT_TIMEOUT_SECONDS,
                    cc.ARBITER_DEFAULT_MAX_TOKENS,
                    cc.ARBITER_DEFAULT_TEMPERATURE,
                    cc.EXECUTION_MODE_SYNC,
                    cc.AGENT_MAX_OUTPUT_TOKENS,
                )
            self.assertFalse(manager.ollama_env_available)


class IDESandboxBackendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.files = Path(self.tmp.name) / "files"
        (self.files / "nested").mkdir(parents=True)
        self.session = cc.SessionState.__new__(cc.SessionState)
        self.session.files_root = self.files
        self.session._remote_runtime_read_roots = lambda: []

    def tearDown(self):
        self.tmp.cleanup()

    def test_bubblewrap_prefix_mounts_only_workspace_writable(self):
        backend = {
            "available": True,
            "name": "bubblewrap",
            "processes": True,
            "terminal": True,
            "debug": True,
        }
        with (
            mock.patch.object(cc, "_detect_ide_sandbox_backend", return_value=backend),
            mock.patch.object(
                cc.shutil,
                "which",
                side_effect=lambda name: "/usr/bin/bwrap" if name == "bwrap" else None,
            ),
        ):
            prefix = self.session._workspace_sandbox_shell_prefix(self.files / "nested")
            command = self.session._sandbox_virtualize_command(
                f"cat {self.files / 'nested' / 'input.txt'}", self.files / "nested"
            )
        self.assertIn("--bind", prefix)
        self.assertIn(str(self.files.resolve()), prefix)
        self.assertIn("/workspace", prefix)
        self.assertIn("/workspace/nested/input.txt", command)
        self.assertNotIn(str(self.files.resolve()), command)

    def test_container_prefix_is_readonly_and_disables_terminal_debug(self):
        backend = {
            "available": True,
            "name": "docker",
            "processes": True,
            "terminal": False,
            "debug": False,
            "image": "clouds-coder-sandbox:latest",
        }
        with (
            mock.patch.object(cc, "_detect_ide_sandbox_backend", return_value=backend),
            mock.patch.object(cc.shutil, "which", return_value="/usr/bin/docker"),
        ):
            prefix = self.session._workspace_sandbox_shell_prefix(self.files / "nested")
            terminal_prefix = self.session._workspace_sandbox_shell_prefix(
                self.files, feature="terminal"
            )
        self.assertIn("--read-only", prefix)
        self.assertIn("ALL", prefix)
        self.assertIn("no-new-privileges", prefix)
        self.assertIn("/workspace/nested", prefix)
        self.assertEqual(terminal_prefix, [])

    def test_capabilities_follow_backend_feature_support(self):
        app = cc.AppContext.__new__(cc.AppContext)
        backend = {
            "available": True,
            "name": "docker",
            "processes": True,
            "terminal": False,
            "debug": False,
            "image": "local-image",
            "reason": "container limitations",
        }
        with mock.patch.object(
            cc.AppContext, "_ide_remote_sandbox_backend", return_value=backend
        ):
            capabilities = app.ide_request_capabilities(
                {"role": "user"}, client_ip="192.168.1.22", direct_loopback=False
            )
        self.assertTrue(capabilities["processes"])
        self.assertFalse(capabilities["terminal"])
        self.assertFalse(capabilities["debug"])
        self.assertEqual(capabilities["sandbox_backend"], "docker")

    def test_linux_and_windows_backend_detection(self):
        ready = types.SimpleNamespace(returncode=0)
        with (
            mock.patch.dict(os.environ, {"CLOUDS_CODER_SANDBOX_BACKEND": "bwrap"}),
            mock.patch.object(cc.os, "name", "posix"),
            mock.patch.object(cc.sys, "platform", "linux"),
            mock.patch.object(cc.shutil, "which", return_value="/usr/bin/bwrap"),
            mock.patch.object(cc.subprocess, "run", return_value=ready),
        ):
            linux = cc._detect_ide_sandbox_backend(force=True)
        self.assertEqual(linux["name"], "bubblewrap")
        self.assertTrue(linux["terminal"])

        with (
            mock.patch.dict(
                os.environ,
                {
                    "CLOUDS_CODER_SANDBOX_BACKEND": "docker",
                    "CLOUDS_CODER_SANDBOX_IMAGE": "local-sandbox:test",
                },
            ),
            mock.patch.object(cc.os, "name", "nt"),
            mock.patch.object(cc.sys, "platform", "win32"),
            mock.patch.object(cc.shutil, "which", return_value="C:/docker.exe"),
            mock.patch.object(cc.subprocess, "run", return_value=ready),
        ):
            windows = cc._detect_ide_sandbox_backend(force=True)
        self.assertEqual(windows["name"], "docker")
        self.assertTrue(windows["processes"])
        self.assertFalse(windows["terminal"])
        self.assertFalse(windows["debug"])

    def test_windows_auto_uses_builtin_job_sandbox_without_container(self):
        with (
            mock.patch.dict(
                os.environ,
                {"CLOUDS_CODER_SANDBOX_BACKEND": "auto"},
            ),
            mock.patch.object(cc.os, "name", "nt"),
            mock.patch.object(cc.sys, "platform", "win32"),
            mock.patch.object(
                cc, "_windows_builtin_sandbox_probe", return_value=(True, "ready")
            ),
            mock.patch.object(cc.shutil, "which", return_value=None),
        ):
            backend = cc._detect_ide_sandbox_backend(force=True)
        self.assertEqual(backend["name"], "windows-job")
        self.assertTrue(backend["available"])
        self.assertTrue(backend["processes"])
        self.assertTrue(backend["terminal"])
        self.assertTrue(backend["debug"])

    def test_windows_job_prefix_is_internal_marker(self):
        backend = {
            "available": True,
            "name": "windows-job",
            "processes": True,
            "terminal": True,
            "debug": True,
        }
        with mock.patch.object(cc, "_detect_ide_sandbox_backend", return_value=backend):
            prefix = self.session._workspace_sandbox_shell_prefix(self.files)
            terminal = self.session._workspace_sandbox_shell_prefix(
                self.files, feature="terminal"
            )
        self.assertTrue(cc._is_windows_job_sandbox_prefix(prefix))
        self.assertTrue(cc._is_windows_job_sandbox_prefix(terminal))

    def test_ide_contains_embedded_icon_fallback(self):
        self.assertIn('<body class="icons-fallback">', cc.IDE_INDEX_HTML)
        self.assertIn(".icons-fallback .codicon::before", cc.IDE_CSS)
        self.assertIn("function initIconFallback()", cc.IDE_JS)


class IDEAuthStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = cc.IDEAuthStore(Path(self.tmp.name) / "ide_auth.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def test_first_admin_binds_legacy_loopback_identity(self):
        legacy = cc.user_id_from_ip("127.0.0.1")
        result = self.store.setup_admin(
            "local-admin", "Strong-Passphrase-42!", legacy_user_id=legacy
        )
        self.assertEqual(result["account"]["role"], "admin")
        self.assertEqual(result["account"]["user_id"], legacy)
        self.assertTrue(self.store.configured())
        self.assertIsNotNone(self.store.verify_session(result["access_token"]))
        with self.assertRaises(cc.IDEAuthError) as caught:
            self.store.setup_admin(
                "second-admin",
                "Another-Passphrase-42!",
                legacy_user_id="ide_second_admin",
            )
        self.assertEqual(caught.exception.code, "setup_already_completed")

    def test_change_password_revokes_sessions_without_leaking_verification_session(
        self,
    ):
        setup = self.store.setup_admin(
            "local-admin",
            "Strong-Passphrase-42!",
            legacy_user_id=cc.user_id_from_ip("127.0.0.1"),
        )
        account = setup["account"]
        self.store.change_password(
            account, "Strong-Passphrase-42!", "Replacement-Passphrase-73!"
        )
        self.assertIsNone(self.store.verify_session(setup["access_token"]))
        with sqlite3.connect(str(self.store.path)) as conn:
            active = conn.execute(
                "SELECT COUNT(*) FROM ide_sessions WHERE revoked_at=0"
            ).fetchone()[0]
        self.assertEqual(active, 0)
        logged_in = self.store.login(
            "local-admin", "Replacement-Passphrase-73!", "127.0.0.1"
        )
        self.assertIsNotNone(self.store.verify_session(logged_in["access_token"]))

    def test_user_disable_revokes_session(self):
        self.store.setup_admin(
            "local-admin",
            "Strong-Passphrase-42!",
            legacy_user_id=cc.user_id_from_ip("127.0.0.1"),
        )
        account = self.store.create_user("developer-one", "Developer-Passphrase-93!")
        session = self.store.login(
            "developer-one", "Developer-Passphrase-93!", "192.168.1.22"
        )
        self.assertEqual(session["account"]["user_id"], account["user_id"])
        self.store.set_disabled("developer-one", True)
        self.assertIsNone(self.store.verify_session(session["access_token"]))

    def test_local_session_is_passwordless_and_device_ip_change_rebinds_automatically(
        self,
    ):
        local = self.store.local_session(legacy_user_id=cc.user_id_from_ip("127.0.0.1"))
        self.assertEqual(local["account"]["username"], "local-admin")
        self.assertIsNotNone(
            self.store.verify_session(local["access_token"], "127.0.0.1")
        )

        device_key = "cc_device_" + "A" * 43
        approved = self.store.register_device(
            device_key,
            label="Test browser",
            fingerprint="test-fingerprint",
            client_ip="192.168.1.22",
        )
        self.assertFalse(approved.get("pending", False))
        self.assertEqual(approved["device"]["status"], "approved")
        self.assertEqual(approved["account"]["role"], "user")
        self.assertIsNotNone(
            self.store.verify_session(approved["access_token"], "192.168.1.22")
        )
        self.assertIsNone(
            self.store.verify_session(approved["access_token"], "192.168.1.23")
        )
        moved = self.store.register_device(
            device_key,
            label="Test browser",
            fingerprint="test-fingerprint",
            client_ip="192.168.1.23",
        )
        self.assertFalse(moved.get("pending", False))
        self.assertEqual(moved["device"]["status"], "approved")
        self.assertEqual(moved["account"]["user_id"], approved["account"]["user_id"])
        self.assertIsNone(
            self.store.verify_session(approved["access_token"], "192.168.1.22")
        )
        self.assertIsNotNone(
            self.store.verify_session(moved["access_token"], "192.168.1.23")
        )

        self.store.revoke_device(moved["device"]["pairing_id"])
        with self.assertRaises(cc.IDEAuthError) as caught:
            self.store.register_device(
                device_key,
                label="Test browser",
                fingerprint="test-fingerprint",
                client_ip="192.168.1.23",
            )
        self.assertEqual(caught.exception.code, "device_revoked")

    def test_local_admin_can_set_password_when_optional_login_is_enabled(self):
        local = self.store.local_session(legacy_user_id=cc.user_id_from_ip("127.0.0.1"))
        self.store.reset_password("local-admin", "Known-Passphrase-73!")
        self.assertIsNone(self.store.verify_session(local["access_token"], "127.0.0.1"))
        logged_in = self.store.login("local-admin", "Known-Passphrase-73!", "127.0.0.1")
        self.assertIsNotNone(
            self.store.verify_session(logged_in["access_token"], "127.0.0.1")
        )


class IDECapabilityTests(unittest.TestCase):
    def test_loopback_mounts_and_remote_process_sandbox_capabilities(self):
        app = cc.AppContext.__new__(cc.AppContext)
        local = app.ide_request_capabilities(
            {"role": "user"}, client_ip="127.0.0.1", direct_loopback=True
        )
        self.assertTrue(local["mounts"])
        self.assertTrue(local["processes"])
        terminal_supported = bool(
            (cc._pty is not None and os.name == "posix") or os.name == "nt"
        )
        self.assertEqual(local["terminal"], terminal_supported)
        lan = app.ide_request_capabilities(
            {"role": "admin"}, client_ip="192.168.1.22", direct_loopback=False
        )
        self.assertFalse(lan["mounts"])
        self.assertEqual(
            lan["terminal"], bool(lan["hard_isolation"] and terminal_supported)
        )
        if not lan["hard_isolation"]:
            with self.assertRaises(cc.IDECapabilityError):
                app.ide_require_capability(lan, "terminal")


class IDEWorkspaceServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.files = self.root / "files"
        self.files.mkdir()
        self.app = cc.AppContext.__new__(cc.AppContext)
        self.app.ide_state_lock = threading.RLock()
        self.app.ide_terminal_lock = threading.RLock()
        self.app.ide_terminals = {}
        self.app.ide_extensions_root = self.root / "extensions"
        self.app.ide_extensions_root.mkdir()
        self.app.ide_resolve_workspace = lambda user_id, session_id, root_id, rel="": (
            self.files,
            cc.safe_path(cc.normalize_rel_preview_path(rel) or ".", self.files),
            {"id": "session", "kind": "session"},
        )
        self.app._ide_reject_hard_snapshot_mutation = lambda *args: None
        self.app._ide_emit_workspace_change = lambda *args, **kwargs: None
        self.app.user_root = lambda user_id: self.root / str(user_id)

    def tearDown(self):
        self.tmp.cleanup()

    def test_terminal_output_base64_preserves_split_utf8_bytes(self):
        raw = "山海绘卷".encode()
        split = 2
        terminal = {
            "user_id": "account-a",
            "output": bytearray(raw[:split]),
            "output_start": 0,
            "output_end": split,
            "closed": False,
            "returncode": None,
            "last_activity": 0.0,
            "lock": threading.RLock(),
        }
        self.app.ide_terminals["term-a"] = terminal

        first = self.app.ide_terminal_output("account-a", "term-a", 0)
        with terminal["lock"]:
            terminal["output"].extend(raw[split:])
            terminal["output_end"] = len(raw)
            terminal["closed"] = True
            terminal["returncode"] = 0
        second = self.app.ide_terminal_output(
            "account-a", "term-a", first["next_offset"]
        )

        joined = base64.b64decode(first["data_b64"]) + base64.b64decode(
            second["data_b64"]
        )
        self.assertEqual(joined.decode("utf-8"), "山海绘卷")
        self.assertEqual(second["encoding"], "utf-8")

    def test_revision_aware_atomic_write_rejects_stale_editor(self):
        target = self.files / "main.py"
        target.write_text("value = 1\n", encoding="utf-8")
        opened = self.app.ide_read_file("account-a", "session-a", rel="main.py")
        target.write_text("value = 2\n", encoding="utf-8")
        with self.assertRaises(cc.IDEFileConflict) as caught:
            self.app.ide_write_file(
                "account-a",
                "session-a",
                {
                    "path": "main.py",
                    "content": "value = 3\n",
                    "expected_revision": opened["revision"],
                },
            )
        self.assertEqual(caught.exception.code, "file_conflict")
        self.assertEqual(target.read_text(encoding="utf-8"), "value = 2\n")

    def test_quick_open_file_list_is_recursive_bounded_and_skips_generated_dirs(self):
        (self.files / "src" / "nested").mkdir(parents=True)
        (self.files / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
        (self.files / "src" / "nested" / "页面.html").write_text(
            "<h1>ok</h1>\n", encoding="utf-8"
        )
        (self.files / "node_modules" / "package").mkdir(parents=True)
        (self.files / "node_modules" / "package" / "ignored.js").write_text(
            "ignored\n", encoding="utf-8"
        )

        listed = self.app.ide_workspace_files(
            "account-a", "session-a", root_id="session", max_files=10
        )
        paths = [row["path"] for row in listed["files"]]
        self.assertEqual(paths, ["src/main.py", "src/nested/页面.html"])
        self.assertFalse(listed["truncated"])

        bounded = self.app.ide_workspace_files(
            "account-a", "session-a", root_id="session", max_files=1
        )
        self.assertEqual(bounded["count"], 1)
        self.assertTrue(bounded["truncated"])

        snapshot = self.app._ide_prompt_workspace_snapshot(
            self.files, max_entries=20, max_chars=4000
        )
        snapshot_paths = [row["path"] for row in snapshot["entries"]]
        self.assertEqual(snapshot["awareness"], "always_on")
        self.assertIn("src/main.py", snapshot_paths)
        self.assertIn("src/nested/页面.html", snapshot_paths)
        self.assertIn("node_modules", snapshot_paths)
        self.assertNotIn("node_modules/package/ignored.js", snapshot_paths)
        self.assertGreaterEqual(snapshot["skipped_directories"], 1)

    def test_prompt_enhancement_uses_active_model_without_submitting_task(self):
        (self.files / "notes.md").write_text("context\n", encoding="utf-8")

        class FakeRuntime:
            model = "test-model"
            provider = "ollama"
            base_url = "http://127.0.0.1:11434"

        class FakeSession:
            ui_language = "zh-CN"
            active_profile_id = "local"
            model_profiles = {
                "local": {
                    "provider": "ollama",
                    "model": "test-model",
                    "base_url": "http://127.0.0.1:11434",
                    "request_timeout": 30,
                }
            }
            ollama = FakeRuntime()
            lock = threading.RLock()
            telemetry_callback = None

            def snapshot_safe(self, **_kwargs):
                return {
                    "conversation_feed": [
                        {
                            "role": "user",
                            "text": "IDE programming request.\n\nEarlier context",
                        }
                    ]
                }

        session = FakeSession()
        self.app._ide_session = lambda user_id, session_id: session
        self.app.submit_user_message = mock.Mock(
            side_effect=AssertionError("must not submit")
        )
        model_payload = {
            "intent_summary": "修复并验证目标功能",
            "deliverables": ["代码修改", "测试证据"],
            "constraints": ["不扩大范围"],
            "assumptions": [],
            "acceptance_criteria": ["测试通过"],
            "execution_steps": [
                {
                    "title": "定位",
                    "action": "检查目标实现与现有测试。",
                    "depends_on": [],
                    "completion_check": "已确认修改点。",
                },
                {
                    "title": "实现",
                    "action": "完成目标功能修改。",
                    "depends_on": ["定位"],
                    "completion_check": "实现符合约束。",
                },
                {
                    "title": "验证",
                    "action": "运行相关测试并核对结果。",
                    "depends_on": ["实现"],
                    "completion_check": "测试通过。",
                },
            ],
            "selected_skills": [],
            "clarifications": [
                {
                    "question": "是否需要保持兼容？",
                    "default_answer": "默认保持现有公开接口兼容。",
                }
            ],
            "enhanced_prompt": "## 目标\n修复目标功能并完成验证。",
        }
        with (
            mock.patch.object(
                self.app,
                "_ide_prompt_skill_catalog",
                side_effect=AssertionError(
                    "skills catalog must stay lazy when awareness is off"
                ),
            ) as skills_catalog,
            mock.patch.object(
                cc.OllamaClient,
                "chat",
                return_value={"content": json.dumps(model_payload, ensure_ascii=False)},
            ) as chat,
        ):
            out = self.app.ide_enhance_agent_prompt(
                "account-a",
                "session-a",
                {
                    "root_id": "session",
                    "active_path": "main.py",
                    "attachments": ["notes.md"],
                    "message": "请修复目标功能",
                },
            )
        self.assertEqual(out["source"], "model")
        self.assertEqual(out["model"], "test-model")
        self.assertIn("修复目标功能并完成验证", out["enhanced_prompt"])
        self.assertIn("请修复目标功能", out["enhanced_prompt"])
        self.assertIn("默认保持现有公开接口兼容", out["enhanced_prompt"])
        self.assertEqual(out["open_questions"], ["是否需要保持兼容？"])
        self.assertEqual(out["clarifications"], model_payload["clarifications"])
        self.assertEqual(out["acceptance_criteria"], ["测试通过"])
        self.assertEqual(len(out["execution_steps"]), 3)
        self.assertEqual(out["workspace_context"]["awareness"], "always_on")
        self.assertFalse(out["skills_awareness"])
        self.app.submit_user_message.assert_not_called()
        skills_catalog.assert_not_called()
        kwargs = chat.call_args.kwargs
        self.assertFalse(kwargs["think"])
        self.assertFalse(kwargs["response_stream"])
        self.assertEqual(kwargs["temperature"], 0.15)
        self.assertEqual(kwargs["max_tokens"], 3600)
        prompt = chat.call_args.args[0][0]["content"]
        self.assertIn('"directory_snapshot"', prompt)
        self.assertIn('"skills_awareness"', prompt)

    def test_prompt_enhancement_selects_valid_skills_and_refines_with_full_instructions(
        self,
    ):
        (self.files / "src").mkdir()
        (self.files / "src" / "app.js").write_text(
            "console.log('ok')\n", encoding="utf-8"
        )

        class FakeRuntime:
            model = "test-model"
            provider = "ollama"
            base_url = "http://127.0.0.1:11434"

        class FakeSession:
            ui_language = "en"
            active_profile_id = "local"
            model_profiles = {
                "local": {
                    "provider": "ollama",
                    "model": "test-model",
                    "base_url": "http://127.0.0.1:11434",
                }
            }
            ollama = FakeRuntime()
            lock = threading.RLock()
            telemetry_callback = None

            def snapshot_safe(self, **_kwargs):
                return {"conversation_feed": []}

        class FakeSkillStore:
            def _resolve_name(self, name):
                return (
                    ("frontend", None)
                    if name in {"frontend", "Frontend"}
                    else (None, "unknown")
                )

            def load(self, name):
                self.loaded = name
                return (
                    "<skill>Inspect existing components, then implement and run "
                    "browser validation.</skill>"
                )

        store = FakeSkillStore()
        catalog = [
            {
                "id": "frontend",
                "name": "Frontend",
                "description": "Build and validate browser interfaces.",
                "provider": "local",
                "triggers": ["frontend"],
                "entrypoints": [],
            }
        ]
        first = {
            "intent_summary": "Implement the requested interface safely.",
            "deliverables": ["Updated interface"],
            "constraints": [],
            "assumptions": [],
            "acceptance_criteria": ["Browser flow passes"],
            "clarifications": [],
            "execution_steps": [
                {
                    "title": "Inspect",
                    "action": "Inspect src/app.js.",
                    "depends_on": [],
                    "completion_check": "Current behavior is known.",
                }
            ],
            "selected_skills": [
                {
                    "id": "frontend",
                    "rationale": "The task changes a browser interface.",
                },
                {"id": "invented-skill", "rationale": "This id is not real."},
            ],
            "enhanced_prompt": "## Goal\nImplement the interface.",
        }
        refined = {
            "execution_steps": [
                {
                    "title": "Inspect",
                    "action": "Inspect src/app.js and its tests.",
                    "depends_on": [],
                    "completion_check": "Current behavior is known.",
                },
                {
                    "title": "Implement",
                    "action": "Implement one bounded UI increment.",
                    "depends_on": ["Inspect"],
                    "completion_check": "The increment works.",
                },
                {
                    "title": "Verify",
                    "action": "Run browser validation.",
                    "depends_on": ["Implement"],
                    "completion_check": "The browser flow passes.",
                },
            ],
            "final_prompt": (
                "## Goal\nImplement the interface in three verified stages."
            ),
        }
        self.app._ide_session = lambda user_id, session_id: FakeSession()
        self.app._ide_prompt_skill_catalog = lambda: (store, catalog, False)
        with mock.patch.object(
            cc.OllamaClient,
            "chat",
            side_effect=[
                {"content": json.dumps(first)},
                {"content": json.dumps(refined)},
            ],
        ) as chat:
            out = self.app.ide_enhance_agent_prompt(
                "account-a",
                "session-a",
                {
                    "message": "Improve the frontend",
                    "budget": "medium",
                    "skills_awareness": True,
                },
            )
        self.assertEqual(chat.call_count, 2)
        self.assertEqual(store.loaded, "frontend")
        self.assertEqual([row["id"] for row in out["selected_skills"]], ["frontend"])
        self.assertNotIn("invented-skill", out["enhanced_prompt"])
        self.assertIn("`frontend`", out["enhanced_prompt"])
        self.assertEqual(len(out["execution_steps"]), 3)
        first_prompt = chat.call_args_list[0].args[0][0]["content"]
        second_prompt = chat.call_args_list[1].args[0][0]["content"]
        self.assertIn("src/app.js", first_prompt)
        self.assertIn("Build and validate browser interfaces", first_prompt)
        self.assertIn("Inspect existing components", second_prompt)

    def test_prompt_enhancement_uses_budget_aware_template_when_model_is_unavailable(
        self,
    ):
        class FakeRuntime:
            model = "offline-model"
            provider = "ollama"
            base_url = "http://127.0.0.1:11434"

        class FakeSession:
            ui_language = "zh-CN"
            active_profile_id = "local"
            model_profiles = {
                "local": {
                    "provider": "ollama",
                    "model": "offline-model",
                    "base_url": "http://127.0.0.1:11434",
                }
            }
            ollama = FakeRuntime()
            lock = threading.RLock()
            telemetry_callback = None

            def snapshot_safe(self, **_kwargs):
                return {"conversation_feed": []}

        self.app._ide_session = lambda user_id, session_id: FakeSession()
        with mock.patch.object(
            cc.OllamaClient, "chat", side_effect=RuntimeError("offline")
        ):
            out = self.app.ide_enhance_agent_prompt(
                "account-a",
                "session-a",
                {"message": "实现导出按钮", "budget": "high"},
            )
        self.assertEqual(out["source"], "fallback")
        self.assertEqual(out["fallback_reason"], "model_error")
        self.assertEqual(out["budget"], "high")
        self.assertIn("任务目标", out["enhanced_prompt"])
        self.assertIn("实现导出按钮", out["enhanced_prompt"])
        self.assertIn("工作区目录（始终感知）", out["enhanced_prompt"])
        self.assertEqual(len(out["execution_steps"]), 3)
        self.assertIn("offline", out["warning"])

    def test_prompt_enhancement_preserves_unbounded_original_input(self):
        class FakeRuntime:
            model = "test-model"
            provider = "ollama"
            base_url = "http://127.0.0.1:11434"

        class FakeSession:
            ui_language = "zh-CN"
            active_profile_id = "local"
            model_profiles = {
                "local": {
                    "provider": "ollama",
                    "model": "test-model",
                    "base_url": "http://127.0.0.1:11434",
                }
            }
            ollama = FakeRuntime()
            lock = threading.RLock()
            telemetry_callback = None

            def snapshot_safe(self, **_kwargs):
                return {"conversation_feed": []}

        original = "开始-" + ("完整输入内容" * 12000) + "-结束"
        model_payload = {
            "intent_summary": "完整保留并处理用户输入。",
            "deliverables": [],
            "constraints": [],
            "assumptions": [],
            "acceptance_criteria": [],
            "clarifications": [],
            "execution_steps": [
                {
                    "title": "执行",
                    "action": "处理完整请求。",
                    "depends_on": [],
                    "completion_check": "请求已完整处理。",
                }
            ],
            "selected_skills": [],
            "enhanced_prompt": "## 目标\n处理完整请求。",
        }
        self.app._ide_session = lambda user_id, session_id: FakeSession()
        with mock.patch.object(
            cc.OllamaClient,
            "chat",
            return_value={"content": json.dumps(model_payload, ensure_ascii=False)},
        ) as chat:
            out = self.app.ide_enhance_agent_prompt(
                "account-a",
                "session-a",
                {"message": original, "budget": "low"},
            )
        sent = chat.call_args.args[0][0]["content"]
        self.assertIn(original, sent)
        self.assertEqual(out["original_prompt"], original)
        self.assertIn(original, out["enhanced_prompt"])
        self.assertEqual(len(out["execution_steps"]), 1)

    def test_prompt_enhancement_parser_accepts_complete_flexible_formats(self):
        nested = self.app._ide_parse_prompt_enhancement_response(
            json.dumps(
                {
                    "result": {
                        "interpreted_intent": "Repair the parser.",
                        "outputs": ["Parser update"],
                        "steps": ["Inspect", "Implement", "Verify"],
                        "final_prompt": "## Goal\nRepair the parser.",
                    }
                }
            )
        )
        self.assertEqual(nested["intent_summary"], "Repair the parser.")
        self.assertEqual(nested["deliverables"], ["Parser update"])
        self.assertEqual(nested["execution_steps"], ["Inspect", "Implement", "Verify"])
        self.assertIn("Repair the parser", nested["enhanced_prompt"])

        markdown = self.app._ide_parse_prompt_enhancement_response(
            "# INTERPRETED INTENT\nHandle the request safely.\n\n"
            "## Deliverables\n- Updated parser\n- Regression tests\n\n"
            "## Execution Steps\n1. Inspect formats\n2. Implement tolerance\n\n"
            "## Final Agent Prompt\nImplement and verify the parser update."
        )
        self.assertEqual(markdown["_format"], "markdown")
        self.assertEqual(markdown["intent_summary"], "Handle the request safely.")
        self.assertEqual(
            markdown["deliverables"], ["Updated parser", "Regression tests"]
        )
        self.assertEqual(
            markdown["execution_steps"], ["Inspect formats", "Implement tolerance"]
        )
        self.assertEqual(
            markdown["enhanced_prompt"], "Implement and verify the parser update."
        )

    def test_prompt_enhancement_parser_rejects_incomplete_json(self):
        malformed = '{"intent_summary":"ok","enhanced_prompt":"unterminated"'
        prefixed = "Here is the requested JSON:\n" + malformed
        fenced = "```json\n" + malformed + "\n```"
        incomplete_array = (
            'Here is the requested JSON:\n[{"enhanced_prompt":"complete inner object"}'
        )
        self.assertEqual(self.app._ide_parse_prompt_enhancement_response(malformed), {})
        self.assertEqual(self.app._ide_parse_prompt_enhancement_response(prefixed), {})
        self.assertEqual(self.app._ide_parse_prompt_enhancement_response(fenced), {})
        self.assertEqual(
            self.app._ide_parse_prompt_enhancement_response(incomplete_array), {}
        )

    def test_prompt_enhancement_preference_is_persisted(self):
        saved = self.app.ide_save_workbench_state(
            "account-a",
            {
                "state": {
                    "active_session_id": "session-a",
                    "prompt_enhance_persistent": True,
                    "prompt_enhance_enabled": True,
                    "prompt_enhance_skills_awareness": True,
                    "prompt_enhance_budget": "high",
                }
            },
        )
        self.assertTrue(saved["state"]["prompt_enhance_persistent"])
        self.assertTrue(saved["state"]["prompt_enhance_enabled"])
        self.assertTrue(saved["state"]["prompt_enhance_skills_awareness"])
        self.assertEqual(saved["state"]["prompt_enhance_budget"], "high")
        loaded = self.app.ide_get_workbench_state("account-a")
        self.assertTrue(loaded["state"]["prompt_enhance_persistent"])
        self.assertTrue(loaded["state"]["prompt_enhance_enabled"])
        self.assertTrue(loaded["state"]["prompt_enhance_skills_awareness"])
        self.assertEqual(loaded["state"]["prompt_enhance_budget"], "high")

        one_shot = self.app.ide_save_workbench_state(
            "account-a",
            {
                "state": {
                    "prompt_enhance_persistent": False,
                    "prompt_enhance_enabled": True,
                    "prompt_enhance_budget": "xhigh",
                }
            },
        )
        self.assertFalse(one_shot["state"]["prompt_enhance_persistent"])
        self.assertFalse(one_shot["state"]["prompt_enhance_enabled"])
        self.assertEqual(one_shot["state"]["prompt_enhance_budget"], "xhigh")

        invalid = self.app.ide_save_workbench_state(
            "account-a", {"state": {"prompt_enhance_budget": "unbounded"}}
        )
        self.assertEqual(invalid["state"]["prompt_enhance_budget"], "medium")

    def test_prompt_enhancement_fallback_matches_all_supported_ui_languages(self):
        markers = {
            "zh-CN": "任务目标",
            "zh-TW": "任務目標",
            "ja": "タスク目標",
            "en": "Task Goal",
        }
        for language, marker in markers.items():
            with self.subTest(language=language):
                out = self.app._ide_prompt_enhancement_fallback(
                    "Keep literal/path.py unchanged",
                    language=language,
                    active_path="literal/path.py",
                )
                self.assertIn(marker, out["enhanced_prompt"])
                self.assertIn("Keep literal/path.py unchanged", out["enhanced_prompt"])
                self.assertTrue(out["acceptance_criteria"])

        variants = {
            budget: self.app._ide_prompt_enhancement_fallback(
                "Implement the feature", language="en", budget=budget
            )
            for budget in ("low", "medium", "high", "xhigh")
        }
        self.assertLess(
            len(variants["low"]["enhanced_prompt"]),
            len(variants["medium"]["enhanced_prompt"]),
        )
        self.assertLess(
            len(variants["medium"]["enhanced_prompt"]),
            len(variants["high"]["enhanced_prompt"]),
        )
        self.assertLess(
            len(variants["high"]["enhanced_prompt"]),
            len(variants["xhigh"]["enhanced_prompt"]),
        )
        self.assertEqual(
            [
                len(variants[budget]["execution_steps"])
                for budget in ("low", "medium", "high", "xhigh")
            ],
            [3, 3, 3, 3],
        )
        profiles = [
            cc.IDE_PROMPT_ENHANCEMENT_BUDGETS[budget]
            for budget in ("low", "medium", "high", "xhigh")
        ]
        self.assertEqual(
            [row["max_tokens"] for row in profiles], [1800, 3600, 6000, 8200]
        )
        self.assertEqual([row["max_skills"] for row in profiles], [1, 3, 5, 8])
        self.assertTrue(
            all("complex" in row["step_guidance"].lower() for row in profiles)
        )
        self.assertIn(
            "materially viable",
            cc.IDE_PROMPT_ENHANCEMENT_BUDGETS["high"]["solution_diversity"],
        )
        self.assertIn(
            "rollback", cc.IDE_PROMPT_ENHANCEMENT_BUDGETS["xhigh"]["planning_depth"]
        )

    def test_ide_preview_html_reuses_workspace_safe_artifact_renderers(self):
        target = self.files / "results.csv"
        target.write_text("planet,distance\nEarth,1\nMars,1.52\n", encoding="utf-8")

        class PreviewSession:
            def _preview_csv_html(self, fp):
                return f"<html><body>{fp.name}</body></html>"

        self.app._ide_session = lambda user_id, session_id: PreviewSession()
        rendered = self.app.ide_preview_html(
            "account-a", "session-a", rel="results.csv"
        )
        self.assertIn("results.csv", rendered)
        with self.assertRaises(FileNotFoundError):
            self.app.ide_preview_html("account-a", "session-a", rel="missing.csv")

    def test_large_previewable_artifact_opens_readonly_without_loading_content(self):
        target = self.files / "large.pdf"
        target.write_bytes(b"%PDF-1.4\n" + b"0" * 32)
        original_limit = cc.IDE_FILE_MAX_BYTES
        try:
            cc.IDE_FILE_MAX_BYTES = 16
            opened = self.app.ide_read_file("account-a", "session-a", rel="large.pdf")
        finally:
            cc.IDE_FILE_MAX_BYTES = original_limit
        self.assertTrue(opened["readonly"])
        self.assertEqual(opened["encoding"], "base64")
        self.assertEqual(opened["content_b64"], "")
        self.assertEqual(opened["file"]["preview_kind"], "pdf")

    def test_large_text_and_markdown_use_bounded_server_previews(self):
        preview_session = cc.SessionState.__new__(cc.SessionState)
        self.app._ide_session = lambda user_id, session_id: preview_session
        text_target = self.files / "large.txt"
        text_target.write_text(
            "# DFT Hamiltonian\n\n$$ \\hat H = -\\frac12\\sum_i \\nabla_i^2 $$\n\n"
            + ("payload\n" * 500_000),
            encoding="utf-8",
        )
        markdown_target = self.files / "complex.md"
        markdown_target.write_text(
            "# Report\n\n<script>alert('unsafe')</script>\n\n"
            + "| A | B |\n|---|---|\n| 1 | 2 |\n" * 200_000,
            encoding="utf-8",
        )
        original_limit = cc.IDE_TEXT_PREVIEW_MAX_BYTES
        try:
            cc.IDE_TEXT_PREVIEW_MAX_BYTES = 256 * 1024
            text_opened = self.app.ide_read_file(
                "account-a", "session-a", rel="large.txt"
            )
            markdown_opened = self.app.ide_read_file(
                "account-a", "session-a", rel="complex.md"
            )
            text_preview = self.app.ide_preview_html(
                "account-a", "session-a", rel="large.txt"
            )
            markdown_preview = self.app.ide_preview_html(
                "account-a", "session-a", rel="complex.md"
            )
        finally:
            cc.IDE_TEXT_PREVIEW_MAX_BYTES = original_limit
        self.assertTrue(text_opened["readonly"])
        self.assertTrue(markdown_opened["readonly"])
        self.assertTrue(text_opened["content_omitted"])
        self.assertIn("showing the first", text_preview)
        self.assertIn("<h1", text_preview)
        self.assertIn("$$", text_preview)
        self.assertIn("<h1", markdown_preview)
        for preview in (text_preview, markdown_preview):
            self.assertNotIn("<script>alert", preview.lower())
            self.assertIn("/assets/js_lib/katex/dist/katex.min.css", preview)
            self.assertIn("/assets/js_lib/katex/dist/katex.min.js", preview)
            self.assertIn(
                "/assets/js_lib/katex/dist/contrib/auto-render.min.js", preview
            )
            self.assertIn("renderMathInElement", preview)
            self.assertNotIn("https://", preview)

    def test_markdown_preview_renders_structured_blocks_and_local_enhancers(self):
        preview_session = cc.SessionState.__new__(cc.SessionState)
        self.app._ide_session = lambda user_id, session_id: preview_session
        target = self.files / "structured.md"
        target.write_text(
            "---\n"
            "title: Structured report\n"
            "tags:\n"
            "  - markdown\n"
            "  - preview\n"
            "---\n"
            "# Overview\n\n"
            "- [x] completed\n- [ ] pending\n\n"
            "> A quoted finding\n\n"
            "| Name | Value |\n| --- | --- |\n| Alpha | 1 |\n\n"
            "Inline formula $x^2$ and block formula:\n\n"
            "$$\\sum_i x_i$$\n\n"
            "```mermaid\n"
            "graph TD\n"
            "  A[Input] --> B[Output]\n"
            "```\n",
            encoding="utf-8",
        )
        preview = self.app.ide_preview_html(
            "account-a", "session-a", rel="structured.md"
        )
        for marker in (
            "Document metadata",
            "pv-task-checkbox",
            "<blockquote>",
            "<table",
            "language-mermaid",
            "/assets/js_lib/marked.min.js",
            "/assets/js_lib/mermaid.min.js",
            "/assets/js_lib/katex/dist/katex.min.js",
            "pv-markdown-source",
        ):
            self.assertIn(marker, preview)
        self.assertNotIn("https://", preview)

    def test_markdown_fallback_keeps_common_structure_readable(self):
        rendered = cc._preview_markdown_fallback_html(
            "# Heading\n\n- [x] done\n- [ ] todo\n\n"
            "> quote\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n"
            '```json\n{"ok": true}\n```'
        )
        self.assertIn("<h1>Heading</h1>", rendered)
        self.assertIn("pv-task-checkbox", rendered)
        self.assertIn("<blockquote>", rendered)
        self.assertIn("<table", rendered)
        self.assertIn("language-json", rendered)
        self.assertNotIn("<script", rendered.lower())

    def test_image_preview_streams_original_or_safe_thumbnail_without_base64_json(self):
        from PIL import Image

        target = self.files / "large.png"
        Image.new("RGB", (5000, 3000), (20, 120, 220)).save(target, format="PNG")
        opened = self.app.ide_read_file("account-a", "session-a", rel="large.png")
        data, content_type = self.app.ide_image_preview(
            "account-a", "session-a", rel="large.png"
        )
        self.assertTrue(opened["readonly"])
        self.assertTrue(opened["content_omitted"])
        self.assertIn(content_type.split(";", 1)[0], {"image/png", "image/jpeg"})
        self.assertGreater(len(data), 100)

    def test_xlsx_preview_has_archive_and_table_budgets(self):
        import openpyxl

        preview_session = cc.SessionState.__new__(cc.SessionState)
        self.app._ide_session = lambda user_id, session_id: preview_session
        target = self.files / "large.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Data"
        for row in range(1, 260):
            ws.append([f"cell-{row}-{col}" for col in range(1, 55)])
        wb.save(target)
        wb.close()
        opened = self.app.ide_read_file("account-a", "session-a", rel="large.xlsx")
        preview = self.app.ide_preview_html("account-a", "session-a", rel="large.xlsx")
        self.assertTrue(opened["readonly"])
        self.assertTrue(opened["content_omitted"])
        self.assertIn("Data", preview)
        self.assertIn("truncated", preview)

    def test_workspace_path_escape_and_symlink_escape_are_rejected(self):
        with self.assertRaises(ValueError):
            self.app.ide_resolve_workspace(
                "account-a", "session-a", "session", "../outside.txt"
            )
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = self.files / "link.txt"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaises(ValueError):
            self.app.ide_resolve_workspace(
                "account-a", "session-a", "session", "link.txt"
            )

    def test_workspace_archive_preserves_tree_and_empty_dirs_but_skips_symlinks(self):
        (self.files / "project" / "empty").mkdir(parents=True)
        (self.files / "project" / "src").mkdir()
        (self.files / "project" / "src" / "main.py").write_text(
            "print('ok')\n", encoding="utf-8"
        )
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = self.files / "project" / "outside-link.txt"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")

        archive = self.app.ide_workspace_archive(
            "account-a", "session-a", root_id="session", rel="project"
        )
        archive_path = Path(archive["path"])
        try:
            with zipfile.ZipFile(archive_path) as bundle:
                names = set(bundle.namelist())
                self.assertIn("project/", names)
                self.assertIn("project/empty/", names)
                self.assertIn("project/src/main.py", names)
                self.assertNotIn("project/outside-link.txt", names)
                self.assertEqual(bundle.read("project/src/main.py"), b"print('ok')\n")
        finally:
            archive_path.unlink(missing_ok=True)

    def test_workspace_copy_and_move_preserve_tree_and_avoid_overwrite(self):
        (self.files / "project" / "empty").mkdir(parents=True)
        (self.files / "project" / "src").mkdir()
        (self.files / "project" / "src" / "main.py").write_text(
            "print('ok')\n", encoding="utf-8"
        )
        (self.files / "destination").mkdir()

        copied = self.app.ide_copy_workspace_entry(
            "account-a",
            "session-a",
            {
                "root_id": "session",
                "source_path": "project",
                "destination_dir": "",
                "operation": "copy",
            },
        )
        self.assertEqual(copied["destination_path"], "project copy")
        self.assertTrue((self.files / "project copy" / "empty").is_dir())
        self.assertEqual(
            (self.files / "project copy" / "src" / "main.py").read_text(
                encoding="utf-8"
            ),
            "print('ok')\n",
        )
        copied_again = self.app.ide_copy_workspace_entry(
            "account-a",
            "session-a",
            {
                "source_path": "project",
                "destination_dir": "",
                "operation": "copy",
            },
        )
        self.assertEqual(copied_again["destination_path"], "project copy 2")

        moved = self.app.ide_copy_workspace_entry(
            "account-a",
            "session-a",
            {
                "source_path": "project\\src\\main.py",
                "destination_dir": "destination",
                "operation": "move",
            },
        )
        self.assertEqual(moved["destination_path"], "destination/main.py")
        self.assertFalse((self.files / "project" / "src" / "main.py").exists())
        self.assertTrue((self.files / "destination" / "main.py").is_file())

        noop = self.app.ide_copy_workspace_entry(
            "account-a",
            "session-a",
            {
                "source_path": "destination/main.py",
                "destination_dir": "destination",
                "operation": "move",
            },
        )
        self.assertTrue(noop["noop"])
        with self.assertRaisesRegex(ValueError, "into itself"):
            self.app.ide_copy_workspace_entry(
                "account-a",
                "session-a",
                {
                    "source_path": "project",
                    "destination_dir": "project/empty",
                    "operation": "copy",
                },
            )

    def test_workspace_copy_rejects_symbolic_links(self):
        source = self.files / "source"
        source.mkdir()
        target = source / "target.txt"
        target.write_text("safe", encoding="utf-8")
        link = source / "link.txt"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(ValueError, "symbolic links"):
            self.app.ide_copy_workspace_entry(
                "account-a",
                "session-a",
                {
                    "source_path": "source",
                    "destination_dir": "",
                    "operation": "copy",
                },
            )

    def test_directory_upload_preserves_empty_directories_and_rejects_escape(self):
        out = self.app.ide_upload(
            "account-a",
            "session-a",
            {
                "root_id": "session",
                "dest": "imports",
                "directories": ["sample", "sample/empty"],
                "items": [
                    {
                        "path": "sample/readme.txt",
                        "content_b64": cc.base64.b64encode(
                            "目录内容".encode()
                        ).decode(),
                    }
                ],
            },
        )
        self.assertEqual(out["count"], 1)
        self.assertEqual(out["directory_count"], 2)
        self.assertTrue((self.files / "imports" / "sample" / "empty").is_dir())
        self.assertEqual(
            (self.files / "imports" / "sample" / "readme.txt").read_text(
                encoding="utf-8"
            ),
            "目录内容",
        )
        with self.assertRaises(ValueError):
            self.app.ide_upload(
                "account-a",
                "session-a",
                {"dest": "", "directories": ["../escaped"], "items": []},
            )
        self.assertFalse((self.root / "escaped").exists())

    def test_chunked_upload_is_idempotent_atomic_and_normalizes_windows_paths(self):
        target = self.files / "imports" / "样例" / "子目录" / "数据.txt"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"old-content")
        raw = "跨平台目录内容".encode()
        first, second = raw[:9], raw[9:]
        base = {
            "root_id": "session",
            "dest": "imports",
            "path": "样例\\子目录\\数据.txt",
            "upload_id": "up_0123456789abcdef0123456789abcdef",
            "size": len(raw),
        }
        first_payload = {
            **base,
            "offset": 0,
            "chunk_b64": cc.base64.b64encode(first).decode("ascii"),
            "action": "append",
        }
        out = self.app.ide_upload_chunk("account-a", "session-a", first_payload)
        self.assertEqual(out["received"], len(first))
        self.assertEqual(target.read_bytes(), b"old-content")
        retry = self.app.ide_upload_chunk("account-a", "session-a", first_payload)
        self.assertEqual(retry["received"], len(first))
        completed = self.app.ide_upload_chunk(
            "account-a",
            "session-a",
            {
                **base,
                "offset": len(first),
                "chunk_b64": cc.base64.b64encode(second).decode("ascii"),
                "action": "complete",
            },
        )
        self.assertTrue(completed["complete"])
        self.assertEqual(target.read_bytes(), raw)
        self.assertEqual(completed["file"]["path"], "imports/样例/子目录/数据.txt")

    def test_chunked_upload_abort_removes_partial_file(self):
        payload = {
            "root_id": "session",
            "path": "partial.bin",
            "upload_id": "up_abcdef0123456789abcdef0123456789",
            "size": 6,
            "offset": 0,
            "chunk_b64": cc.base64.b64encode(b"abc").decode("ascii"),
            "action": "append",
        }
        self.app.ide_upload_chunk("account-a", "session-a", payload)
        self.app.ide_upload_chunk(
            "account-a", "session-a", {**payload, "action": "abort", "chunk_b64": ""}
        )
        self.assertFalse((self.files / "partial.bin").exists())
        self.assertFalse(list(self.files.glob(".clouds-upload-*.part")))

    def test_multi_chunk_binary_upload_round_trips_through_zip(self):
        raw = bytes(range(256)) * 5000
        upload_id = "up_00112233445566778899aabbccddeeff"
        chunk_size = 512 * 1024
        for offset in range(0, len(raw), chunk_size):
            chunk = raw[offset : offset + chunk_size]
            complete = offset + len(chunk) == len(raw)
            out = self.app.ide_upload_chunk(
                "account-a",
                "session-a",
                {
                    "root_id": "session",
                    "dest": "跨平台",
                    "path": "二进制\\payload.bin",
                    "upload_id": upload_id,
                    "size": len(raw),
                    "offset": offset,
                    "chunk_b64": cc.base64.b64encode(chunk).decode("ascii"),
                    "action": "complete" if complete else "append",
                },
            )
        self.assertTrue(out["complete"])
        self.assertEqual(
            (self.files / "跨平台" / "二进制" / "payload.bin").read_bytes(), raw
        )
        archive = self.app.ide_workspace_archive(
            "account-a", "session-a", root_id="session", rel="跨平台"
        )
        archive_path = Path(archive["path"])
        try:
            with zipfile.ZipFile(archive_path) as bundle:
                self.assertEqual(bundle.read("跨平台/二进制/payload.bin"), raw)
        finally:
            archive_path.unlink(missing_ok=True)

    def test_agent_task_accepts_only_existing_workspace_attachments(self):
        attachment = self.files / ".clouds_coder" / "attachments" / "brief.txt"
        attachment.parent.mkdir(parents=True)
        attachment.write_text("solar system requirements", encoding="utf-8")
        submitted = []

        class FakeSession:
            pass

        self.app._ide_session = lambda user_id, session_id: FakeSession()
        self.app.submit_user_message = lambda user_id, session_id, message: (
            submitted.append(message) or {"ok": True}
        )
        out = self.app.ide_agent_task(
            "account-a",
            "session-a",
            {
                "root_id": "session",
                "message": "Build the model",
                "attachments": [".clouds_coder/attachments/brief.txt"],
            },
        )
        self.assertTrue(out["ok"])
        self.assertIn("Attached workspace files", submitted[0])
        self.assertIn(".clouds_coder/attachments/brief.txt", submitted[0])
        with self.assertRaises(FileNotFoundError):
            self.app.ide_agent_task(
                "account-a",
                "session-a",
                {"message": "Build", "attachments": ["missing.txt"]},
            )

    def _vsix(self, entries):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            for name, data in entries:
                archive.writestr(name, data)
        return output.getvalue()

    def test_vsix_zip_slip_is_rejected(self):
        manifest = json.dumps(
            {"publisher": "sample", "name": "safe", "version": "1.0.0"}
        )
        data = self._vsix(
            [
                ("extension/package.json", manifest),
                ("extension/../../escaped.txt", "bad"),
            ]
        )
        with self.assertRaises(ValueError):
            self.app._ide_safe_extract_vsix(data, self.root / "install")
        self.assertFalse((self.root / "escaped.txt").exists())

    def test_declarative_vsix_manifest_is_exposed_without_host_apis(self):
        manifest = json.dumps(
            {
                "publisher": "sample",
                "name": "theme",
                "version": "1.0.0",
                "browser": "dist/extension.js",
                "contributes": {
                    "commands": [{"command": "sample.hello", "title": "Hello"}]
                },
            }
        )
        data = self._vsix(
            [
                ("extension/package.json", manifest),
                ("extension/dist/extension.js", "self.onmessage=()=>{}"),
            ]
        )
        public = self.app._ide_safe_extract_vsix(data, self.root / "install")
        self.assertEqual(public["id"], "sample.theme")
        self.assertTrue(public["worker_supported"])
        self.assertIn("commands", public["contributes"])
        self.assertNotIn("scripts", public)

    def test_packaged_ide_assets_fallback_from_an_isolated_workspace(self):
        workspace_assets = self.root / "workspace-js"
        packaged_root = self.root / "package"
        packaged_assets = packaged_root / "js_lib"
        loader = packaged_assets / "monaco" / "min" / "vs" / "loader.js"
        worker = (
            packaged_assets
            / "monaco"
            / "min"
            / "vs"
            / "assets"
            / "editor.worker-test.js"
        )
        loader.parent.mkdir(parents=True)
        worker.parent.mkdir(parents=True)
        loader.write_text("loader", encoding="utf-8")
        worker.write_text("worker", encoding="utf-8")
        workspace_assets.mkdir()
        self.app.js_lib_root = workspace_assets

        with mock.patch.object(cc, "SCRIPT_DIR", packaged_root):
            self.assertEqual(
                self.app.rag_js_lib_asset_path("monaco/min/vs/loader.js"),
                loader.resolve(),
            )
            self.assertEqual(self.app.ide_monaco_worker_path(), worker.resolve())

    @unittest.skipUnless(
        cc.AppContext._ide_remote_sandbox_supported(), "macOS sandbox-exec required"
    )
    def test_remote_workspace_sandbox_blocks_outside_read_and_write(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = self.files
        (self.files / "inside.txt").write_text("inside", encoding="utf-8")
        outside = self.root / "outside.txt"
        outside.write_text("outside", encoding="utf-8")
        prefix = session._workspace_sandbox_shell_prefix()
        allowed = cc.subprocess.run(
            [*prefix, "/bin/sh", "-c", "cat inside.txt && echo changed > made.txt"],
            cwd=self.files,
            capture_output=True,
            text=True,
        )
        self.assertEqual(allowed.returncode, 0)
        self.assertEqual(
            (self.files / "made.txt").read_text(encoding="utf-8").strip(), "changed"
        )
        blocked_read = cc.subprocess.run(
            [
                *prefix,
                "/bin/sh",
                "-c",
                f"cat {cc.shlex.quote(str(Path.home() / '.zshrc'))}",
            ],
            cwd=self.files,
            capture_output=True,
            text=True,
        )
        blocked_sibling_read = cc.subprocess.run(
            [*prefix, "/bin/sh", "-c", f"cat {cc.shlex.quote(str(outside))}"],
            cwd=self.files,
            capture_output=True,
            text=True,
        )
        blocked_write = cc.subprocess.run(
            [
                *prefix,
                "/bin/sh",
                "-c",
                "echo escaped > /private/tmp/clouds-coder-sandbox-test",
            ],
            cwd=self.files,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(blocked_read.returncode, 0)
        self.assertNotEqual(blocked_sibling_read.returncode, 0)
        self.assertNotEqual(blocked_write.returncode, 0)
        self.assertFalse(Path("/private/tmp/clouds-coder-sandbox-test").exists())

    def test_remote_process_environment_uses_workspace_private_temp(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = self.files
        session.ide_remote_sandbox_required = True
        env = session._shell_process_env()
        expected = str(self.files / ".clouds_coder" / "tmp")
        virtual = cc._detect_ide_sandbox_backend().get("name") in {
            "bubblewrap",
            "docker",
            "podman",
        }
        self.assertEqual(env["HOME"], "/workspace" if virtual else str(self.files))
        self.assertEqual(env["TMPDIR"], "/tmp" if virtual else expected)
        self.assertEqual(env["TMP"], "/tmp" if virtual else expected)
        self.assertEqual(env["TEMP"], "/tmp" if virtual else expected)
        self.assertTrue(Path(expected).is_dir())
        allowed_roots = [self.files.resolve(), *session._remote_runtime_read_roots()]
        for entry in env["PATH"].split(os.pathsep):
            resolved = Path(entry).resolve()
            if resolved == Path("/Users") or resolved.is_relative_to(Path("/Users")):
                self.assertTrue(
                    any(
                        resolved == root or resolved.is_relative_to(root)
                        for root in allowed_roots
                    )
                )

    def test_remote_agent_file_tools_reject_external_virtual_roots(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = self.files
        session.ide_remote_sandbox_required = True
        session.skill_mode = "dynamic"

        for path in (
            "/skills/private/SKILL.md",
            "/js_lib/monaco/min/vs/loader.js",
            "file_buffer/long-output.txt",
            "[file_buffer:long-output]",
        ):
            with self.subTest(path=path):
                result = session._dispatch_tool_inner(
                    "read_file", {"path": path}, "developer"
                )
                self.assertIn("limited to the isolated session workspace", result)

        write_result = session._dispatch_tool_inner(
            "write_file",
            {"path": "/js_lib/escaped.js", "content": "escaped"},
            "developer",
        )
        edit_result = session._dispatch_tool_inner(
            "edit_file",
            {
                "path": "file_buffer/long-output.txt",
                "old_text": "old",
                "new_text": "new",
            },
            "developer",
        )
        self.assertIn("limited to the isolated session workspace", write_result)
        self.assertIn("limited to the isolated session workspace", edit_result)

    def test_remote_agent_file_scope_allows_workspace_paths_only(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = self.files
        session.ide_remote_sandbox_required = True

        self.assertEqual(
            session._remote_agent_file_scope_error("src/main.py", "read"), ""
        )
        self.assertEqual(
            session._remote_agent_file_scope_error("/workspace/src/main.py", "write"),
            "",
        )
        escaped = session._remote_agent_file_scope_error("../outside.txt", "read")
        self.assertIn("path escapes workspace", escaped)


class IDEHTTPAuthTests(unittest.TestCase):
    class FakeApp:
        def __init__(self, root):
            self.ide_auth = cc.IDEAuthStore(root / "auth.sqlite")
            self.saved = None

        ide_is_loopback_address = staticmethod(cc.AppContext.ide_is_loopback_address)
        ide_require_capability = staticmethod(cc.AppContext.ide_require_capability)

        def ide_request_capabilities(self, account, *, client_ip, direct_loopback):
            return cc.AppContext.ide_request_capabilities(
                self, account, client_ip=client_ip, direct_loopback=direct_loopback
            )

        def ide_auth_status(self, *, local_setup_allowed):
            return {
                "setup_required": not self.ide_auth.configured(),
                "local_setup_allowed": local_setup_allowed,
                "local_auto_login": False,
                "password_login_enabled": True,
            }

        def setup_ide_admin(self, username, password, *, local_setup_allowed):
            if not local_setup_allowed:
                raise cc.IDEAuthError("setup_local_only", "local only", 403)
            return self.ide_auth.setup_admin(
                username, password, legacy_user_id=cc.user_id_from_ip("127.0.0.1")
            )

        def login_ide(self, username, password, client_ip):
            return self.ide_auth.login(username, password, client_ip)

        def register_ide_device(self, payload, *, client_ip):
            return self.ide_auth.register_device(
                payload.get("device_key"),
                label=payload.get("label", "Web browser"),
                fingerprint=payload.get("fingerprint", ""),
                client_ip=client_ip,
            )

        def ide_get_workbench_state(self, user_id):
            return {"ok": True, "state": {}}

        def ide_save_workbench_state(self, user_id, payload):
            self.saved = (user_id, payload)
            return {"ok": True, "state": payload.get("state", {})}

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = self.FakeApp(Path(self.tmp.name))
        self.server = cc.AgentHTTPServer(("127.0.0.1", 0), cc.IdeHandler, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        payload = json.dumps(body).encode() if body is not None else None
        request_headers = {"Host": f"127.0.0.1:{self.port}"}
        request_headers.update(headers or {})
        if payload is not None:
            request_headers["Content-Type"] = "application/json"
        conn.request(method, path, body=payload, headers=request_headers)
        response = conn.getresponse()
        raw = response.read()
        result = json.loads(raw.decode() or "{}")
        response_headers = dict(response.getheaders())
        conn.close()
        return response.status, response_headers, result

    def test_cookie_session_and_csrf_protect_state_writes(self):
        status, headers, setup = self.request(
            "POST",
            "/api/ide/v2/auth/setup",
            {"username": "local-admin", "password": "Strong-Passphrase-42!"},
            {"Origin": f"http://127.0.0.1:{self.port}"},
        )
        self.assertEqual(status, 201)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        csrf = setup["csrf_token"]
        status, _, me = self.request(
            "GET", "/api/ide/v2/auth/me", headers={"Cookie": cookie}
        )
        self.assertEqual(status, 200)
        self.assertEqual(me["account"]["username"], "local-admin")
        status, _, error = self.request(
            "POST",
            "/api/ide/v2/workbench/state",
            {"state": {"active_view": "search"}},
            {"Cookie": cookie, "Origin": f"http://127.0.0.1:{self.port}"},
        )
        self.assertEqual(status, 403)
        self.assertEqual(error["code"], "csrf_required")
        status, _, saved = self.request(
            "POST",
            "/api/ide/v2/workbench/state",
            {"state": {"active_view": "search"}},
            {
                "Cookie": cookie,
                "Origin": f"http://127.0.0.1:{self.port}",
                "X-CSRF-Token": csrf,
            },
        )
        self.assertEqual(status, 200)
        self.assertEqual(saved["state"]["active_view"], "search")
        self.assertEqual(self.app.saved[0], setup["account"]["user_id"])

    def test_plain_http_lan_device_session_is_allowed_and_ip_bound(self):
        previous = os.environ.get("CLOUDS_CODER_TRUST_PROXY")
        os.environ["CLOUDS_CODER_TRUST_PROXY"] = "1"
        try:
            device_key = "cc_device_" + "B" * 43
            status, headers, authenticated = self.request(
                "POST",
                "/api/ide/v2/auth/device",
                {
                    "device_key": device_key,
                    "label": "LAN browser",
                    "fingerprint": "test",
                },
                headers={
                    "Host": f"192.168.1.20:{self.port}",
                    "Origin": f"http://192.168.1.20:{self.port}",
                    "X-Forwarded-For": "192.168.1.55",
                },
            )
            cookie = headers["Set-Cookie"].split(";", 1)[0]
            self.assertEqual(status, 200)
            self.assertEqual(authenticated["account"]["role"], "user")
            self.assertFalse(authenticated["capabilities"]["mounts"])
            status, _, me = self.request(
                "GET",
                "/api/ide/v2/auth/me",
                headers={
                    "Host": f"192.168.1.20:{self.port}",
                    "Cookie": cookie,
                    "X-Forwarded-For": "192.168.1.55",
                },
            )
            self.assertEqual(status, 200)
            self.assertEqual(
                me["account"]["user_id"], authenticated["account"]["user_id"]
            )
            status, _, error = self.request(
                "GET",
                "/api/ide/v2/auth/me",
                headers={
                    "Host": f"192.168.1.20:{self.port}",
                    "Cookie": cookie,
                    "X-Forwarded-For": "192.168.1.56",
                },
            )
            self.assertEqual(status, 401)
            self.assertEqual(error["code"], "authentication_required")
        finally:
            if previous is None:
                os.environ.pop("CLOUDS_CODER_TRUST_PROXY", None)
            else:
                os.environ["CLOUDS_CODER_TRUST_PROXY"] = previous


class IDEWorkbenchSourceTests(unittest.TestCase):
    def test_bash_read_loop_intervention_allows_ten_identical_reads(self):
        self.assertEqual(cc.BASH_READ_LOOP_THRESHOLD, 10)

    def test_terminal_renderer_has_incremental_utf8_and_dependency_free_ansi_fallback(
        self,
    ):
        self.assertIn("data_b64", inspect.getsource(cc.AppContext.ide_terminal_output))
        self.assertIn("new TextDecoder", cc.IDE_JS)
        self.assertIn(
            "function stripTerminalControlChunk(text,state,final=false)", cc.IDE_JS
        )
        self.assertIn("appendTerminalPlainText(E('terminalFallback'),plain)", cc.IDE_JS)
        self.assertNotIn("host.textContent+=out.data", cc.IDE_JS)

        node = cc.shutil.which("node")
        if not node:
            self.skipTest("Node.js is unavailable for the frontend parser check")
        start = cc.IDE_JS.index("function stripTerminalControlChunk")
        end = cc.IDE_JS.index("\nfunction appendTerminalPlainText", start)
        parser = cc.IDE_JS[start:end]
        script = (
            parser
            + r"""
const state={pending:''};
const chunks=['\x1b[31','m红\x1b]0;标题','\x07色\x1b[0m'];
const output=chunks.map((chunk,index)=>stripTerminalControlChunk(
chunk,state,index===chunks.length-1)).join('');
process.stdout.write(JSON.stringify({output,pending:state.pending}));
"""
        )
        completed = cc.subprocess.run(
            [node, "-e", script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        parsed = json.loads(completed.stdout)
        self.assertEqual(parsed, {"output": "红色", "pending": ""})

    def test_python_debug_uses_stdlib_pdb_when_debugpy_is_missing(self):
        self.assertIn("error.code==='debugpy_unavailable'", cc.IDE_JS)
        self.assertIn("python} -m pdb", cc.IDE_JS)
        self.assertIn("Using the built-in Python pdb compatibility debugger", cc.IDE_JS)
        with mock.patch.object(cc.importlib.util, "find_spec", return_value=None):
            tool = next(
                row
                for row in cc.AppContext.__new__(cc.AppContext).ide_toolchains()
                if row["name"] == "python-debug"
            )
        self.assertFalse(tool["available"])
        self.assertIn("pdb compatibility debugger", tool["install_hint"])

    def test_recovery_hard_break_allows_ten_debug_rounds(self):
        self.assertEqual(cc.HARD_BREAK_RECOVERY_ROUND_THRESHOLD, 10)
        source = inspect.getsource(cc.SessionState._agent_worker)
        self.assertIn(
            "recovery_retry_rounds >= HARD_BREAK_RECOVERY_ROUND_THRESHOLD",
            source,
        )
        self.assertIn("recovery instructions repeated without progress", source)

    def test_hidden_panel_state_survives_panel_tab_restoration(self):
        source = cc.IDE_JS
        restore_start = source.index("async function restoreWorkbenchState()")
        restore_end = source.index("async function runSearch()", restore_start)
        restore = source[restore_start:restore_end]

        self.assertIn("const panelVisible=state.panel_visible!==false", restore)
        self.assertIn("showPanel(S.panel);S.panelVisible=panelVisible", restore)
        self.assertIn("classList.toggle('panel-hidden',!panelVisible)", restore)
        self.assertNotIn("if(!S.panelVisible)togglePanel()", restore)

    def test_agent_polling_and_thinking_exclusion_are_present(self):
        self.assertIn("/agent-state", cc.IDE_JS)
        self.assertIn("scheduleAgentPoll", cc.IDE_JS)
        self.assertIn("refreshAgentEditedFile", cc.IDE_JS)
        self.assertNotIn(
            '"live_thinking"', inspect.getsource(cc.AppContext.ide_agent_state)
        )

    def test_public_model_text_is_kept_when_the_same_turn_calls_tools(self):
        source = Path(cc.__file__).read_text(encoding="utf-8")
        self.assertGreaterEqual(
            source.count("if text.strip() or (thinking_text and not tool_calls):"), 2
        )
        self.assertNotIn(
            "if (text.strip() or thinking_text) and not tool_calls:", source
        )

    def test_tool_rounds_keep_real_approach_but_disable_synthetic_progress(self):
        source = Path(cc.__file__).read_text(encoding="utf-8")
        self.assertFalse(cc.PUBLIC_TOOL_PROGRESS_SUMMARY_ENABLED)
        self.assertGreaterEqual(
            source.count("_public_tool_progress_summary(tool_calls"), 2
        )
        self.assertIn("function agentApproach(text,role='Agent')", cc.IDE_JS)
        self.assertIn("function renderAgentPlanCard(tools,role='Agent')", cc.IDE_JS)
        self.assertIn("function isSyntheticPublicProgress(text)", cc.IDE_JS)
        self.assertIn("progress&&!isSyntheticPublicProgress(progress)", cc.IDE_JS)
        self.assertIn("S.agentPlanCards.get(signature)", cc.IDE_JS)
        self.assertIn("Planned ×${count}", cc.IDE_JS)
        self.assertIn(
            "if(type==='approach'){agentApproach(text,role);continue}", cc.IDE_JS
        )
        self.assertNotIn("String(S.agentState?.live_thinking", cc.IDE_JS)

    def test_public_tool_progress_summary_is_disabled_without_touching_tool_calls(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.ui_language = "zh-CN"
        session.last_public_progress_signature = ""
        session.last_public_progress_ts = 0.0
        session.todo = cc.TodoManager("zh-CN")
        session.todo.update(
            [
                {"content": "提取 PDF 文本并梳理论文结构", "status": "in_progress"},
                {"content": "编写 HTML 报告", "status": "pending"},
            ]
        )
        summary = session._public_tool_progress_summary(
            [
                {
                    "function": {
                        "name": "bash",
                        "arguments": {"command": "pdftotext input.pdf output.txt"},
                    }
                }
            ]
        )
        self.assertEqual(summary, "")
        self.assertEqual(session._public_progress_prompt_instruction(), "")
        self.assertEqual(session.last_public_progress_signature, "")
        self.assertEqual(
            session._public_tool_progress_summary(
                [
                    {
                        "function": {
                            "name": "bash",
                            "arguments": {"command": "pdftotext input.pdf output.txt"},
                        }
                    }
                ]
            ),
            "",
        )
        self.assertEqual(
            session._public_tool_progress_summary(
                [
                    {
                        "function": {
                            "name": "read_file",
                            "arguments": {"path": "input.txt"},
                        }
                    }
                ]
            ),
            "",
        )
        self.assertTrue(
            cc.is_synthetic_public_progress(
                "正在推进「提取 PDF 文本」；本轮将运行命令以提取或验证证据，"
                "结果将用于确定下一步。"
            )
        )
        self.assertFalse(
            cc.is_synthetic_public_progress("模型自主输出的真实阶段说明。")
        )

        client = cc.OllamaClient("http://127.0.0.1:11434", "test")
        prepared = client._prepare_request_messages(
            [
                {
                    "role": "assistant",
                    "content": (
                        "正在推进「提取 PDF 文本」；本轮将运行命令以提取或验证证据，"
                        "结果将用于确定下一步。"
                    ),
                    "tool_calls": [
                        {
                            "id": "call-1",
                            "type": "function",
                            "function": {
                                "name": "bash",
                                "arguments": {"command": "pwd"},
                            },
                        }
                    ],
                },
                {"role": "assistant", "content": "模型自主输出的真实阶段说明。"},
            ],
            "ollama",
        )
        self.assertEqual(prepared[0]["content"], "")
        self.assertEqual(prepared[0]["tool_calls"][0]["function"]["name"], "bash")
        self.assertEqual(prepared[1]["content"], "模型自主输出的真实阶段说明。")

    def test_four_languages_keep_independent_preferences_while_progress_fallback_is_off(
        self,
    ):
        expected = {
            "zh-CN": "zh-cn-concise-milestones",
            "zh-TW": "zh-tw-concise-milestones",
            "ja": "ja-polite-milestones",
            "en": "en-concise-milestones",
        }
        for language, preference_id in expected.items():
            with self.subTest(language=language):
                payload = cc.agent_language_preference_payload(language)
                self.assertEqual(payload["language"], language)
                self.assertEqual(payload["id"], preference_id)
                self.assertEqual(payload["public_progress_mode"], "off")
                session = cc.SessionState.__new__(cc.SessionState)
                session.ui_language = language
                session.last_public_progress_signature = ""
                session.last_public_progress_ts = 0.0
                session.todo = cc.TodoManager(language)
                summary = session._public_tool_progress_summary(
                    [
                        {
                            "function": {
                                "name": "bash",
                                "arguments": {"command": "run-tests"},
                            }
                        }
                    ]
                )
                self.assertEqual(summary, "")

    def test_program_ide_layout_panels_previews_and_new_task_are_wired(self):
        self.assertIn(
            'side-view[data-side-view="explorer"]{grid-template-rows:35px auto '
            "auto 22px minmax(0,1fr)}",
            cc.IDE_CSS,
        )
        self.assertIn(".editor-group>.editor-host{grid-row:4}", cc.IDE_CSS)
        self.assertIn('id="artifactPreview0"', cc.IDE_INDEX_HTML)
        self.assertIn('title="New Task"', cc.IDE_INDEX_HTML)
        self.assertIn("refreshWorkspaceSnapshot", cc.IDE_JS)
        self.assertIn("function artifactUrl(file,kind='raw')", cc.IDE_JS)
        self.assertIn(
            'r"^/api/ide/sessions/([^/]+)/workspace/raw$"',
            inspect.getsource(cc.IdeHandler.do_GET),
        )
        self.assertIn(
            'r"^/api/ide/sessions/([^/]+)/workspace/preview$"',
            inspect.getsource(cc.IdeHandler.do_GET),
        )
        self.assertIn("E('newAgentChatBtn').onclick=()=>createSession()", cc.IDE_JS)
        self.assertIn("async function debugActiveFile()", cc.IDE_JS)
        self.assertNotIn("Binary files cannot be edited in the text editor.", cc.IDE_JS)

    def test_empty_editor_actions_open_files_and_commands(self):
        self.assertIn('data-command="file.open">Open File', cc.IDE_INDEX_HTML)
        self.assertIn(
            'data-command="workbench.action.quickOpen">Go to File', cc.IDE_INDEX_HTML
        )
        self.assertIn(
            'data-command="workbench.action.showCommands">Command Palette',
            cc.IDE_INDEX_HTML,
        )
        self.assertIn(".empty-actions [data-command]", cc.IDE_JS)
        self.assertIn("button.dataset.command", cc.IDE_JS)
        self.assertIn("beginFileUpload(activeDir(),true)", cc.IDE_JS)
        self.assertIn("openAfter&&firstPath?openFile(firstPath)", cc.IDE_JS)
        self.assertIn("async function loadQuickFiles()", cc.IDE_JS)
        self.assertIn("workspace/files?root_id=", cc.IDE_JS)
        self.assertIn(
            "S.paletteMode=value.startsWith('>')?'commands':'files'", cc.IDE_JS
        )
        self.assertIn("if(row.kind==='file')openFile", cc.IDE_JS)
        self.assertIn('/workspace/files$"', inspect.getsource(cc.IdeHandler.do_GET))

    def test_prompt_enhancement_review_flow_is_fully_wired(self):
        self.assertIn('id="promptEnhanceBtn"', cc.IDE_INDEX_HTML)
        self.assertIn("codicon-lightbulb", cc.IDE_INDEX_HTML)
        self.assertIn('aria-pressed="false"', cc.IDE_INDEX_HTML)
        for element_id in (
            "promptEnhanceOverlay",
            "promptEnhanceLoading",
            "promptEnhanceAnalysis",
            "promptEnhanceIntent",
            "promptEnhanceDetails",
            "promptUseOriginal",
            "promptRegenerate",
            "promptEnhanceEditor",
            "promptUseEnhanced",
        ):
            self.assertIn(f'id="{element_id}"', cc.IDE_INDEX_HTML)
        self.assertNotIn('id="promptEnhanceEdit"', cc.IDE_INDEX_HTML)
        self.assertIn("Final Agent Prompt", cc.IDE_INDEX_HTML)
        self.assertIn("agent-enhance-button.is-active", cc.IDE_CSS)
        self.assertIn("prompt-enhance-analysis", cc.IDE_CSS)
        self.assertIn("function togglePromptEnhancement()", cc.IDE_JS)
        self.assertIn("async function requestPromptEnhancement", cc.IDE_JS)
        self.assertIn("async function usePromptReview(original=false)", cc.IDE_JS)
        self.assertIn("usePromptReview(true)", cc.IDE_JS)
        self.assertIn("regeneratePromptReview()", cc.IDE_JS)
        self.assertIn("editor.readOnly=false", cc.IDE_JS)
        self.assertIn("promptClarificationGroup(result.clarifications)", cc.IDE_JS)
        self.assertIn("new AbortController()", cc.IDE_JS)
        self.assertIn("signal:controller?.signal", cc.IDE_JS)
        self.assertIn(
            "E('promptEnhanceOverlay').classList.remove('is-hidden')", cc.IDE_JS
        )
        self.assertIn("promptEnhancePersistent:false", cc.IDE_JS)
        self.assertIn("prompt_enhance_persistent:S.promptEnhancePersistent", cc.IDE_JS)
        self.assertIn(
            "prompt_enhance_enabled:S.promptEnhancePersistent&&S.promptEnhanceEnabled",
            cc.IDE_JS,
        )
        self.assertIn(
            "S.promptEnhancePersistent=state.prompt_enhance_persistent===true",
            cc.IDE_JS,
        )
        self.assertIn(
            "S.promptEnhanceEnabled=S.promptEnhancePersistent&&"
            "state.prompt_enhance_enabled===true",
            cc.IDE_JS,
        )
        self.assertIn("promptEnhanceBudget:'medium'", cc.IDE_JS)
        self.assertIn("prompt_enhance_budget:S.promptEnhanceBudget", cc.IDE_JS)
        self.assertIn("promptEnhanceSkillsAware:false", cc.IDE_JS)
        self.assertIn(
            "prompt_enhance_skills_awareness:S.promptEnhanceSkillsAware", cc.IDE_JS
        )
        self.assertIn("skills_awareness:!!draft.skills_aware", cc.IDE_JS)
        self.assertIn("function setPromptEnhanceSkillsAware(enabled)", cc.IDE_JS)
        self.assertIn("Workspace awareness", cc.IDE_JS)
        self.assertIn("function promptExecutionGroup(rows)", cc.IDE_JS)
        self.assertIn("function promptSkillGroup(rows)", cc.IDE_JS)
        self.assertIn("function bindPromptEnhanceButton()", cc.IDE_JS)
        self.assertIn("showPromptEnhanceBudgetMenu(button)", cc.IDE_JS)
        self.assertIn("function setPromptEnhancePersistent(enabled)", cc.IDE_JS)
        self.assertIn("Remember across tasks and reloads", cc.IDE_JS)
        self.assertIn("draft.enhance_requested&&!S.promptEnhancePersistent", cc.IDE_JS)
        self.assertIn("enhance_requested:S.promptEnhanceEnabled", cc.IDE_JS)
        self.assertIn("prompt-budget-persistent", cc.IDE_CSS)
        self.assertIn("prompt-persistent-switch", cc.IDE_CSS)
        self.assertIn("['low','medium','high','xhigh']", cc.IDE_JS)
        self.assertIn("budget:S.promptEnhanceBudget", cc.IDE_JS)
        self.assertIn("/prompt-enhance", cc.IDE_JS)
        post_source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn('/prompt-enhance$"', post_source)
        self.assertIn("ide_enhance_agent_prompt", post_source)
        backend_source = inspect.getsource(cc.AppContext.ide_enhance_agent_prompt)
        self.assertIn("Do not reveal chain-of-thought", backend_source)
        self.assertIn("The original request remains authoritative", backend_source)
        self.assertIn("default_answer", backend_source)
        self.assertIn("planning_depth", backend_source)
        self.assertIn("solution_diversity", backend_source)
        self.assertIn("scope_breadth", backend_source)
        self.assertIn('max_tokens=int(budget_spec["max_tokens"])', backend_source)
        self.assertIn("client.timeout = None", backend_source)
        self.assertIn("_ide_prompt_enhancement_fallback(", backend_source)
        self.assertIn("Local template", cc.IDE_JS)

    def test_session_switches_discard_stale_async_results(self):
        self.assertIn("sessionSwitchSeq:0", cc.IDE_JS)
        self.assertIn("function sessionRequestCurrent(session,seq=null)", cc.IDE_JS)
        self.assertIn("const seq=++S.sessionSwitchSeq", cc.IDE_JS)
        self.assertIn("if(seq!==S.sessionSwitchSeq)return false", cc.IDE_JS)
        self.assertIn(
            "const session=S.activeSession,switchSeq=S.sessionSwitchSeq", cc.IDE_JS
        )
        self.assertIn("switchSeq!==S.sessionSwitchSeq", cc.IDE_JS)
        self.assertIn("workspaceRefreshSeq", cc.IDE_JS)
        self.assertIn("const sid=S.activeSession,seq=S.sessionSwitchSeq", cc.IDE_JS)
        self.assertIn(
            "if(S.agentPollBusy){S.agentPollRequested=true;return}", cc.IDE_JS
        )

    def test_text_markdown_image_and_excel_preview_paths_are_wired(self):
        self.assertEqual(cc.preview_kind_for_path("notes.txt"), "markdown")
        self.assertEqual(cc.preview_kind_for_path("report.mdx"), "markdown")
        self.assertEqual(cc.preview_kind_for_path("plot.png"), "image")
        self.assertEqual(cc.preview_kind_for_path("data.xlsx"), "excel")
        self.assertIn("'image-preview'", cc.IDE_JS)
        self.assertIn("'markdown','text'].includes(kind)", cc.IDE_JS)
        self.assertIn("media.onerror=()=>showArtifactPreviewError", cc.IDE_JS)
        self.assertIn("frame.src=artifactUrl(file,'preview')", cc.IDE_JS)
        self.assertIn(
            ".artifact-stage img{display:block;width:100%;height:100%", cc.IDE_CSS
        )
        self.assertIn(".artifact-preview-error", cc.IDE_CSS)

    def test_program_agent_todo_model_attachment_and_diff_controls_are_wired(self):
        self.assertIn('id="agentTodoPanel"', cc.IDE_INDEX_HTML)
        self.assertIn('id="agentModelBtn"', cc.IDE_INDEX_HTML)
        self.assertIn('id="agentAttachmentInput"', cc.IDE_INDEX_HTML)
        self.assertIn("uploadAgentAttachments", cc.IDE_JS)
        self.assertIn("showAgentModelMenu", cc.IDE_JS)
        self.assertIn("renderFilePatchCard", cc.IDE_JS)
        self.assertIn("data-agent-open-file", cc.IDE_JS)
        self.assertIn("context_left_percent", cc.IDE_JS)

    def test_program_agent_stop_live_input_and_file_paste_are_wired(self):
        self.assertIn('id="stopAgentBtn"', cc.IDE_INDEX_HTML)
        self.assertIn('id="agentDropHint"', cc.IDE_INDEX_HTML)
        self.assertIn("async function stopAgent()", cc.IDE_JS)
        self.assertIn("/agent/interrupt", cc.IDE_JS)
        self.assertIn("function agentClipboardFiles(event)", cc.IDE_JS)
        self.assertIn("agentComposer.addEventListener('drop'", cc.IDE_JS)
        self.assertIn("agentPrompt.addEventListener('paste'", cc.IDE_JS)
        self.assertNotIn("E('agentPrompt').disabled=S.agentSubmitting", cc.IDE_JS)
        self.assertNotIn("input.disabled=true", cc.IDE_JS)
        self.assertIn("input.value=''", cc.IDE_JS)
        self.assertIn("input.value=input.value.trim()?", cc.IDE_JS)
        self.assertIn(".agent-stop-button", cc.IDE_CSS)
        self.assertIn(".agent-drop-hint", cc.IDE_CSS)

    def test_program_agent_ask_user_options_and_free_text_are_wired(self):
        self.assertIn('id="agentAskUser"', cc.IDE_INDEX_HTML)
        self.assertIn("function renderAgentAskUser(state)", cc.IDE_JS)
        self.assertIn("async function answerAgentQuestion(answer)", cc.IDE_JS)
        self.assertIn("/ask-user/answer", cc.IDE_JS)
        self.assertIn("pending.allow_free_text===false", cc.IDE_JS)
        self.assertIn("if(pending)return answerAgentQuestion(message)", cc.IDE_JS)
        self.assertIn("Awaiting input", cc.IDE_JS)
        self.assertIn(".agent-ask-user-option", cc.IDE_CSS)

    def test_agent_cards_structure_controls_roles_commands_and_file_diffs(self):
        self.assertIn("function parseAgentControl(text)", cc.IDE_JS)
        self.assertIn("function renderCompactCard(data)", cc.IDE_JS)
        self.assertIn("function agentRoleKey(role='')", cc.IDE_JS)
        self.assertIn("agent-role-manager", cc.IDE_CSS)
        self.assertIn("agent-role-reviewer", cc.IDE_CSS)
        self.assertIn("Changed files:", cc.IDE_JS)
        self.assertIn("Working directory:", cc.IDE_JS)
        self.assertIn("data.diff_numbered||data.diff", cc.IDE_JS)
        self.assertIn("line-mark", cc.IDE_JS)
        self.assertNotIn(
            "fileTool&&!/error|failed|malformed/i.test(resultText)", cc.IDE_JS
        )

    def test_agent_tool_events_render_directly_from_sse_and_merge_shell_cards(self):
        self.assertIn("function renderAgentOperationOnce(op)", cc.IDE_JS)
        self.assertIn("renderAgentOperationOnce({id:String(event?.id||'')", cc.IDE_JS)
        self.assertIn(
            "['tool_start','tool_result','file_patch','command','compact',"
            "'error'].includes(type)",
            cc.IDE_JS,
        )
        self.assertIn("data.tool_call_id", cc.IDE_JS)
        self.assertIn("existing?.dataset.commandComplete==='true'", cc.IDE_JS)
        self.assertIn("S.agentRendered.add(key)", cc.IDE_JS)
        self.assertNotIn(
            "lower==='bash'||lower==='worktree_run')return null", cc.IDE_JS
        )

    def test_agent_poll_deadline_is_not_postponed_by_continuous_sse(self):
        self.assertIn("agentPollDue:0", cc.IDE_JS)
        self.assertIn("if(S.agentPoll&&S.agentPollDue<=due)return", cc.IDE_JS)
        self.assertIn("const wait=Math.max(40,Number(delay)||0)", cc.IDE_JS)
        self.assertIn(
            "clearTimeout(S.agentPoll);S.agentPoll=null;S.agentPollDue=0", cc.IDE_JS
        )

    def test_final_agent_text_uses_sanitized_markdown_and_deduplicates_role_prefix(
        self,
    ):
        self.assertIn("/assets/js_lib/marked.min.js", cc.IDE_INDEX_HTML)
        self.assertIn("function renderAgentMarkdown(text)", cc.IDE_JS)
        self.assertIn("sanitizePreviewHtml(html)", cc.IDE_JS)
        self.assertIn("function stripAgentRolePrefix(text,role='')", cc.IDE_JS)
        self.assertIn("body.className='agent-markdown'", cc.IDE_JS)
        self.assertIn(
            ".agent-markdown h1,.agent-markdown h2,.agent-markdown h3", cc.IDE_CSS
        )

    def test_agent_sidebar_pins_todo_and_composer_around_scrolling_history(self):
        self.assertIn("height:100%;min-height:0;border-right:0", cc.IDE_CSS)
        self.assertIn(
            'grid-template-areas:"agent-header" "agent-context" "agent-todo" '
            '"agent-messages" "agent-composer"',
            cc.IDE_CSS,
        )
        self.assertIn(
            ".secondary-sidebar>.agent-messages{grid-area:agent-messages}", cc.IDE_CSS
        )
        self.assertIn(
            ".secondary-sidebar>.agent-composer{grid-area:agent-composer}", cc.IDE_CSS
        )
        self.assertIn(
            ".agent-messages{min-height:0;overflow:auto;overscroll-behavior:contain",
            cc.IDE_CSS,
        )
        self.assertIn(
            ".agent-composer{min-height:0;max-height:min(420px,52vh);overflow:auto",
            cc.IDE_CSS,
        )
        self.assertIn("resize:none", cc.IDE_CSS)

    def test_run_has_non_pty_fallback_and_utf8_platform_selection(self):
        self.assertIn(
            "if(S.panel==='terminal'&&S.capabilities.terminal){await "
            "newTerminal(file.dir||'.')",
            cc.IDE_JS,
        )
        self.assertIn("/terminal/run", cc.IDE_JS)
        self.assertIn("S.config?.platform", cc.IDE_JS)
        handler_source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn(
            'ide_require_capability(context["capabilities"], "processes")',
            handler_source,
        )

    def test_all_history_mode_only_shows_modified_line_numbers(self):
        self.assertIn("renderIndicators:false", cc.IDE_JS)
        self.assertNotIn("renderIndicators:true", cc.IDE_JS)
        self.assertIn("renderGutterMenu:false", cc.IDE_JS)
        self.assertIn("renderMarginRevertIcon:false", cc.IDE_JS)
        self.assertIn("compactMode:true", cc.IDE_JS)
        self.assertIn("lineDecorationsWidth:8", cc.IDE_JS)
        self.assertIn(
            "S.codeHistoryMode==='all'||S.codeHistoryMode==='changes'", cc.IDE_JS
        )
        self.assertIn(".history-diff-host .inline-deleted-margin-view-zone", cc.IDE_CSS)
        self.assertIn(
            "diff.getOriginalEditor().updateOptions({lineNumbers:'off'",
            cc.IDE_JS,
        )
        self.assertIn(
            "diff.getModifiedEditor().updateOptions({lineNumbers:'on',"
            "lineNumbersMinChars:5,lineDecorationsWidth:24})",
            cc.IDE_JS,
        )
        self.assertIn("lineNumbersMinChars:5,lineDecorationsWidth:8", cc.IDE_JS)
        self.assertIn("function protectDeletedReviewZones(host)", cc.IDE_JS)
        self.assertIn("'selectstart','dragstart','contextmenu','copy'", cc.IDE_JS)
        self.assertIn("protectDeletedReviewZones(E(`diffEditor${group}`))", cc.IDE_JS)
        self.assertIn(
            ".history-diff-host .monaco-editor .line-delete-selectable", cc.IDE_CSS
        )
        self.assertIn("user-select:none!important", cc.IDE_CSS)
        self.assertIn("pointer-events:none!important", cc.IDE_CSS)
        self.assertIn(
            "const model=S.models.get(file.key);return model?model.getValue():"
            "file.content",
            cc.IDE_JS,
        )
        self.assertIn("const commonEditorOptions=", cc.IDE_JS)
        self.assertIn("function captureHistoryView(group,file)", cc.IDE_JS)
        self.assertIn("source.getModel()!==targetModel", cc.IDE_JS)
        self.assertIn("function restoreHistoryView(group,state)", cc.IDE_JS)
        self.assertIn(
            "anchorOffset:source.getTopForLineNumber(anchorLine)-source.getScrollTop()",
            cc.IDE_JS,
        )
        self.assertIn(
            "target.getTopForLineNumber(anchorLine)-Number(state.anchorOffset||0)",
            cc.IDE_JS,
        )
        self.assertIn("onDidUpdateDiff", cc.IDE_JS)
        self.assertIn("S.monaco.ScrollType?.Immediate??1", cc.IDE_JS)
        self.assertNotIn("S.monaco.ScrollType.Immediate", cc.IDE_JS)

    def test_ide_assets_use_content_revision_urls(self):
        app = cc.AppContext.__new__(cc.AppContext)
        html = app.web_ui_ide_index_html()
        self.assertRegex(html, r'href="/assets/ide\.css\?v=[0-9a-f]{12}"')
        self.assertRegex(html, r'src="/assets/ide\.js\?v=[0-9a-f]{12}"')

    def test_session_switch_resets_agent_history_and_editor_split_state(self):
        self.assertIn("function resetAgentSessionUI(sessionId='')", cc.IDE_JS)
        self.assertIn("E('agentMessages').innerHTML=''", cc.IDE_JS)
        self.assertIn("function syncEditorGroupLayout()", cc.IDE_JS)
        self.assertIn("if(!split)S.activeGroup=0", cc.IDE_JS)
        self.assertIn("setEditorModel(1,null);setEditorModel(0,null)", cc.IDE_JS)
        self.assertIn(
            "if(session!==S.activeSession||switchSeq!==S.sessionSwitchSeq)return null",
            cc.IDE_JS,
        )

    def test_sse_connection_loads_selected_session_history_once(self):
        self.assertIn(
            "S.agentEventsConnected=true;S.agentPollRequested=true;"
            "scheduleAgentPoll(0)",
            cc.IDE_JS,
        )
        self.assertIn(
            "if(S.agentPollRequested||!current())scheduleAgentPoll(0)",
            cc.IDE_JS,
        )


class IDEAutoTitleTests(unittest.TestCase):
    @staticmethod
    def make_session(title="Program 12:34", model_title="宝可梦精灵球绘制"):
        session = cc.SessionState.__new__(cc.SessionState)
        session.id = "sess_auto_title"
        session.title = title
        session.title_origin = (
            "default"
            if session._is_default_session_title(title)
            else ("auto" if session._is_low_quality_auto_title(title) else "legacy")
        )
        session.last_auto_title_source = ""
        session.last_auto_title_ts = 0.0
        session.cancel_requested = False
        session.lock = threading.RLock()
        session.ui_language = "zh-CN"
        session.messages = [
            {
                "role": "user",
                "content": (
                    "IDE programming request.\n"
                    "Workspace root: Demo (session)\n"
                    "Writable path: /tmp/demo\n"
                    "Active file: plot.py\n\n"
                    "制作一个宝可梦精灵球的图片，用matplot设计制作显示"
                ),
            }
        ]
        session.todo = types.SimpleNamespace(snapshot=lambda: [])
        session.tasks = types.SimpleNamespace(list_objects=lambda: [])
        prompts = []

        class FakeModel:
            def chat(self, messages, **_kwargs):
                prompts.append(messages[0]["content"])
                return {"content": model_title}

        session.ollama = FakeModel()
        session._inject_runtime_environment_context = lambda text="": text
        session._persist = mock.Mock()
        session._emit = mock.Mock()
        return session, prompts

    def test_program_ide_task_envelope_is_removed_before_title_generation(self):
        session, prompts = self.make_session()
        self.assertEqual(
            session._latest_user_goal_text(),
            "制作一个宝可梦精灵球的图片，用matplot设计制作显示",
        )
        self.assertTrue(session._maybe_auto_rename_session_title("test"))
        self.assertEqual(session.title, "宝可梦精灵球绘制")
        self.assertEqual(session.title_origin, "auto")
        self.assertEqual(session.last_auto_title_source, "model")
        self.assertIn("制作一个宝可梦精灵球", prompts[0])
        self.assertNotIn("Workspace root:", prompts[0])

    def test_generic_model_title_falls_back_to_concrete_user_task(self):
        session, _ = self.make_session(model_title="IDE编程请求处理")
        self.assertTrue(session._maybe_auto_rename_session_title("test"))
        self.assertEqual(session.title, "制作一个宝可梦精灵球的图片")
        self.assertEqual(session.last_auto_title_source, "fallback")
        self.assertFalse(session._is_low_quality_auto_title(session.title))

    def test_continuation_message_does_not_replace_title_goal(self):
        session, _ = self.make_session(model_title="继续")
        session.messages.append(
            {"role": "user", "content": "我现在无法操作，请你检查发生了什么"}
        )
        session.messages.append({"role": "user", "content": "继续"})
        self.assertEqual(session._latest_user_goal_text(), "继续")
        self.assertEqual(
            session._best_session_title_goal_text(),
            "制作一个宝可梦精灵球的图片，用matplot设计制作显示",
        )
        self.assertTrue(session._maybe_auto_rename_session_title("test"))
        self.assertEqual(session.title, "制作一个宝可梦精灵球的图片")
        self.assertEqual(session.last_auto_title_source, "fallback")

    def test_legacy_default_and_bad_auto_titles_are_replaceable(self):
        session, _ = self.make_session(title="IDE编程会话 / IDE编程会话")
        self.assertEqual(session.title_origin, "default")
        self.assertTrue(session._maybe_auto_rename_session_title("test"))

        bad, _ = self.make_session(title="编程任务进行中")
        self.assertEqual(bad.title_origin, "auto")
        self.assertTrue(bad._maybe_auto_rename_session_title("test"))
        self.assertEqual(bad.title, "宝可梦精灵球绘制")

    def test_windows_localized_program_titles_are_replaceable_defaults(self):
        for title in (
            "Program 10:30 AM",
            "Program 上午10:30",
            "Program １０：３０",
            "Program \u200e10:30 PM",
        ):
            with self.subTest(title=title):
                session, _ = self.make_session(title=title)
                self.assertEqual(session.title_origin, "default")
                self.assertTrue(session._maybe_auto_rename_session_title("test"))
                self.assertEqual(session.title, "宝可梦精灵球绘制")

    def test_manual_title_is_never_overwritten(self):
        session, _ = self.make_session(title="Program 12:34")
        session.title_origin = "manual"
        self.assertFalse(session._maybe_auto_rename_session_title("test"))
        self.assertEqual(session.title, "Program 12:34")
        session.ollama.chat = mock.Mock(
            side_effect=AssertionError("model should not be called")
        )
        self.assertFalse(session._maybe_auto_rename_session_title("test"))

    def test_load_migration_repairs_only_replaceable_legacy_titles(self):
        session, _ = self.make_session(title="IDE编程请求初始化")
        self.assertTrue(session._migrate_legacy_auto_title_on_load())
        self.assertEqual(session.title, "制作一个宝可梦精灵球的图片")
        self.assertEqual(session.title_origin, "auto")
        self.assertEqual(session.last_auto_title_source, "migration")

        manual, _ = self.make_session(title="IDE编程请求初始化")
        manual.title_origin = "manual"
        self.assertFalse(manual._migrate_legacy_auto_title_on_load())
        self.assertEqual(manual.title, "IDE编程请求初始化")

    def test_manager_rename_marks_title_as_manual(self):
        manager = cc.SessionManager.__new__(cc.SessionManager)
        manager.lock = threading.RLock()
        manager.session_index = {}
        session = types.SimpleNamespace(
            id="sess_manual",
            title="Program 10:00",
            title_origin="default",
            last_auto_title_source="model",
            updated_at=0.0,
            _persist=mock.Mock(),
        )
        manager._load_session_locked = lambda _session_id: session
        manager._session_message_count = lambda _session: 0
        manager.rename("sess_manual", "我的太阳系模型")
        self.assertEqual(session.title, "我的太阳系模型")
        self.assertEqual(session.title_origin, "manual")
        self.assertEqual(session.last_auto_title_source, "")


class IDEAgentStateTests(unittest.TestCase):
    def test_interrupt_agent_cancels_only_matching_queued_rows(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app._lock = threading.RLock()
        app._task_queue = cc.deque(
            [
                {
                    "id": 11,
                    "user_id": "user-a",
                    "session_id": "session-a",
                    "content": "one",
                },
                {
                    "id": 12,
                    "user_id": "user-b",
                    "session_id": "session-b",
                    "content": "two",
                },
            ]
        )
        session = types.SimpleNamespace(
            running=True,
            interrupted=0,
            visible=[],
        )
        session.interrupt = lambda: setattr(
            session, "interrupted", session.interrupted + 1
        )
        session.update_scheduler_visible_message = lambda queue_id, **state: (
            session.visible.append((queue_id, state))
        )
        app._ide_session = lambda user_id, session_id: session
        refreshed = []
        app._refresh_scheduler_visible_positions = lambda: refreshed.append(True)

        out = app.ide_interrupt_agent("user-a", "session-a")

        self.assertTrue(out["cancel_requested"])
        self.assertEqual(out["cancelled_queued"], 1)
        self.assertEqual(session.interrupted, 1)
        self.assertEqual(session.visible, [(11, {"status": "cancelled"})])
        self.assertEqual([row["id"] for row in app._task_queue], [12])
        self.assertEqual(refreshed, [True])

    def test_session_interrupt_does_not_wait_for_a_busy_session_lock(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.lock = threading.RLock()
        session.cancel_requested = False
        session.current_phase = "tool:bash"
        session.current_tool_name = "bash"
        session._running_bash_proc = None
        session._emit = mock.Mock()
        session._persist = mock.Mock()
        acquired = threading.Event()

        def hold_lock():
            with session.lock:
                acquired.set()
                time.sleep(0.3)

        holder = threading.Thread(target=hold_lock)
        holder.start()
        self.assertTrue(acquired.wait(1))
        started = time.monotonic()
        session.interrupt()
        elapsed = time.monotonic() - started
        holder.join(1)

        self.assertTrue(session.cancel_requested)
        self.assertLess(elapsed, 0.2)
        session._emit.assert_not_called()
        session._persist.assert_not_called()

    def test_interrupt_agent_http_route_is_wired(self):
        source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn('/agent/interrupt$"', source)
        self.assertIn("ide_interrupt_agent", source)

    def test_program_ide_manual_compact_requires_idle_session(self):
        app = cc.AppContext.__new__(cc.AppContext)

        class FakeSession:
            running = False
            compacted = 0

            def manual_compact(self):
                self.compacted += 1

            def snapshot_safe(self, **_kwargs):
                return {
                    "context_tokens_estimate": 1200,
                    "context_left_tokens": 8800,
                    "context_left_percent": 88.0,
                }

        session = FakeSession()
        app._ide_session = lambda user_id, session_id: session
        out = app.ide_compact_agent("user-a", "session-a")
        self.assertTrue(out["ok"])
        self.assertEqual(session.compacted, 1)
        self.assertEqual(out["context_left_tokens"], 8800)
        session.running = True
        with self.assertRaises(ValueError):
            app.ide_compact_agent("user-a", "session-a")
        self.assertEqual(session.compacted, 1)

    def test_workspace_transfer_and_compact_ui_routes_are_wired(self):
        get_source = inspect.getsource(cc.IdeHandler.do_GET)
        post_source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn('/workspace/archive$"', get_source)
        self.assertIn("ide_workspace_archive", get_source)
        self.assertIn('/workspace/upload-chunk$"', post_source)
        self.assertIn("ide_upload_chunk", post_source)
        self.assertIn('/compact$"', post_source)
        self.assertIn("ide_compact_agent", post_source)
        self.assertIn('id="workspaceSectionLabel"', cc.IDE_INDEX_HTML)
        self.assertIn('id="downloadWorkspaceBtn"', cc.IDE_INDEX_HTML)
        self.assertIn("showWorkspaceMenu", cc.IDE_JS)
        self.assertIn("downloadWorkspaceBtn').onclick", cc.IDE_JS)
        self.assertIn("Download Folder as ZIP", cc.IDE_JS)
        self.assertIn("Download File", cc.IDE_JS)
        self.assertIn("scanDirectoryHandle", cc.IDE_JS)
        self.assertIn("showDirectoryPicker", cc.IDE_JS)
        self.assertIn("directories", cc.IDE_JS)
        self.assertIn("uploadFileStream", cc.IDE_JS)
        self.assertIn("chunkSize=512*1024", cc.IDE_JS)
        self.assertIn("workspace/upload-chunk", cc.IDE_JS)
        self.assertIn("compactAgentContext", cc.IDE_JS)
        self.assertIn("agent-model-compact", cc.IDE_CSS)
        self.assertIn("min-width:52px!important", cc.IDE_CSS)
        self.assertIn("compact.textContent='Compact'", cc.IDE_JS)
        self.assertIn("context_effective_token_limit", cc.IDE_JS)

    def test_workspace_drag_drop_clipboard_and_context_actions_are_wired(self):
        post_source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn('/workspace/copy$"', post_source)
        self.assertIn("ide_copy_workspace_entry", post_source)
        self.assertIn(
            'id="tree" class="tree" role="tree" tabindex="0"', cc.IDE_INDEX_HTML
        )
        self.assertIn('id="workspaceSectionLabel"', cc.IDE_INDEX_HTML)
        self.assertIn('tabindex="0" role="button"', cc.IDE_INDEX_HTML)

        for marker in (
            "workspaceClipboard:null",
            "explorerSelection:null",
            "scanDroppedDataTransfer",
            "getAsFileSystemHandle",
            "webkitGetAsEntry",
            "bindWorkspaceDropZone(tree)",
            "bindWorkspaceDropZone(workspaceLabel,{rootOnly:true})",
            "copyExplorerEntry",
            "pasteWorkspaceClipboard",
            "explorerHasKeyboardFocus",
            "addCommand('explorer.copy'",
            "addCommand('explorer.cut'",
            "addCommand('explorer.paste'",
            "addCommand('explorer.rename'",
            "addCommand('explorer.delete'",
            "Paste into Parent",
            "Upload Files Here",
            "Upload Folder Here",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, cc.IDE_JS)

        self.assertIn(
            "S.workspaceClipboard=null;S.explorerSelection=null;"
            "clearWorkspaceDropState()",
            cc.IDE_JS,
        )
        self.assertIn("event.key==='Delete'||event.key==='Backspace'", cc.IDE_JS)
        self.assertIn(".tree-row.is-drop-target", cc.IDE_CSS)
        self.assertIn(".tree-row.is-cut", cc.IDE_CSS)

    def test_program_session_creation_uses_server_default_title(self):
        self.assertIn(
            "api('/api/ide/sessions',{method:'POST',body:'{}'})",
            cc.IDE_JS,
        )
        self.assertNotIn("Program ${new Date().toLocaleTimeString", cc.IDE_JS)

    def test_agent_state_exposes_sanitized_pending_user_question(self):
        app = cc.AppContext.__new__(cc.AppContext)

        class FakeSession:
            operations = []
            lock = threading.RLock()

            def snapshot_safe(self, **_kwargs):
                return {
                    "running": False,
                    "pending_user_question": {
                        "id": "ask-42",
                        "question": "Choose a renderer",
                        "options": ["Canvas", "WebGL"],
                        "allow_free_text": False,
                        "role": "planner",
                        "ts": 12.5,
                        "private": "hidden",
                    },
                    "conversation_feed": [],
                    "todos": [],
                    "tasks": [],
                }

        app._ide_session = lambda user_id, session_id: FakeSession()
        state = app.ide_agent_state("user-a", "session-a")
        self.assertEqual(
            state["pending_user_question"],
            {
                "id": "ask-42",
                "question": "Choose a renderer",
                "options": ["Canvas", "WebGL"],
                "allow_free_text": False,
                "role": "planner",
                "ts": 12.5,
            },
        )

    def test_answer_agent_question_rejects_stale_or_invalid_answers(
        self,
    ):
        app = cc.AppContext.__new__(cc.AppContext)
        session = types.SimpleNamespace(
            pending_user_question={
                "id": "ask-current",
                "question": "Choose one",
                "options": ["A", "B"],
                "allow_free_text": False,
            }
        )
        app._ide_session = lambda user_id, session_id: session
        submitted = []
        app.submit_user_message = lambda user_id, session_id, content: (
            submitted.append(content) or {"ok": True}
        )

        out = app.ide_answer_agent_question(
            "user-a", "session-a", {"question_id": "ask-current", "answer": "B"}
        )
        self.assertEqual(submitted, ["B"])
        self.assertEqual(out["answer"], "B")
        with self.assertRaisesRegex(ValueError, "stale"):
            app.ide_answer_agent_question(
                "user-a", "session-a", {"question_id": "ask-old", "answer": "A"}
            )
        with self.assertRaisesRegex(ValueError, "stale"):
            app.ide_answer_agent_question("user-a", "session-a", {"answer": "A"})
        with self.assertRaisesRegex(ValueError, "available options"):
            app.ide_answer_agent_question(
                "user-a", "session-a", {"question_id": "ask-current", "answer": "C"}
            )

    def test_ask_user_answer_http_route_is_wired(self):
        source = inspect.getsource(cc.IdeHandler.do_POST)
        self.assertIn('/ask-user/answer$"', source)
        self.assertIn("ide_answer_agent_question", source)

    def test_ide_public_operation_data_is_shared_by_state_and_sse(self):
        public = cc.ide_public_operation_data(
            {
                "name": "bash",
                "tool_call_id": "call-42",
                "agent_role": "developer",
                "command": "python verify.py",
                "cwd": "/workspace/session",
                "output": "验证通过",
                "exit_code": 0,
                "duration_ms": 42,
                "changed_files": ["verify.py"],
                "secret": "do-not-publish",
            }
        )
        self.assertEqual(public["tool_call_id"], "call-42")
        self.assertEqual(public["command"], "python verify.py")
        self.assertEqual(public["output"], "验证通过")
        self.assertEqual(public["exit_code"], 0)
        self.assertEqual(public["changed_files"], ["verify.py"])
        self.assertNotIn("secret", public)
        stream_source = inspect.getsource(cc.IdeHandler._stream_ide_events)
        state_source = inspect.getsource(cc.AppContext.ide_agent_state)
        self.assertIn('"id": str(event.get("id", "")', stream_source)
        self.assertIn('"ts": float(event.get("ts", 0.0)', stream_source)
        self.assertIn("ide_public_operation_data(data)", stream_source)
        self.assertIn("ide_public_operation_data(data)", state_source)

    def test_ide_sse_stream_emits_complete_live_command_operation(self):
        class FakeHub:
            def __init__(self):
                self.queue = __import__("queue").Queue()
                self.queue.put(
                    {
                        "id": "evt-command-1",
                        "seq": 17,
                        "ts": 123.5,
                        "type": "command",
                        "data": {
                            "name": "bash",
                            "tool_call_id": "call-17",
                            "agent_role": "developer",
                            "command": "printf 验证通过",
                            "cwd": "/workspace/session",
                            "output": "验证通过",
                            "exit_code": 0,
                            "duration_ms": 9,
                            "changed_files": [],
                            "secret": "do-not-publish",
                        },
                    }
                )

            def subscribe(self):
                return self.queue

            def unsubscribe(self, _queue):
                return None

        class FakeSession:
            id = "sess-live"
            event_seq = 16
            files_root = Path(tempfile.mkdtemp())
            events = FakeHub()

        class FakeHandler:
            def __init__(self):
                self.payloads = []

            def send_response(self, _status):
                return None

            def send_header(self, _key, _value):
                return None

            def end_headers(self):
                return None

            def _sse_write(self, payload):
                self.payloads.append(payload)
                return len(self.payloads) < 2

        handler = FakeHandler()
        cc.IdeHandler._stream_ide_events(handler, FakeSession())
        raw = b"".join(handler.payloads).decode("utf-8")
        event_lines = [
            line[6:] for line in raw.splitlines() if line.startswith("data: ")
        ]
        event = json.loads(event_lines[-1])
        self.assertEqual(event["id"], "evt-command-1")
        self.assertEqual(event["seq"], 17)
        self.assertEqual(event["type"], "command")
        self.assertEqual(event["data"]["tool_call_id"], "call-17")
        self.assertEqual(event["data"]["command"], "printf 验证通过")
        self.assertEqual(event["data"]["output"], "验证通过")
        self.assertEqual(event["data"]["exit_code"], 0)
        self.assertNotIn("secret", event["data"])

    def test_shell_command_event_keeps_tool_call_id_for_live_card_replacement(self):
        source = inspect.getsource(cc.SessionState._dispatch_tool_inner)
        self.assertIn('"tool_call_id": trim(str(tool_call_id or ""), 240)', source)

    def test_agent_state_filters_thinking_and_preserves_public_evidence(self):
        app = cc.AppContext.__new__(cc.AppContext)

        class FakeSession:
            def snapshot_safe(self, **_kwargs):
                return {
                    "running": True,
                    "agent_phase": "agent:developer:tool:write_file",
                    "agent_active_role": "developer",
                    "agent_active_tool": "write_file",
                    "event_seq": 8,
                    "message_count": 3,
                    "live_thinking": "private reasoning",
                    "live_response_text": "Editing the model.",
                    "model": "coder-model",
                    "provider": "test-provider",
                    "context_tokens_estimate": 1200,
                    "context_left_tokens": 6800,
                    "context_left_percent": 85.0,
                    "context_effective_token_limit": 8000,
                    "conversation_feed": [
                        {
                            "role": "assistant",
                            "agent_role": "developer",
                            "type": "message",
                            "text": "Implementing the model.",
                            "thinking": "private reasoning",
                            "ts": 1,
                        },
                        {
                            "role": "system",
                            "type": "file_patch",
                            "text": "[file_patch] solar.py",
                            "data": {"path": "solar.py", "diff": "secretly large diff"},
                            "ts": 2,
                        },
                        {
                            "role": "assistant",
                            "agent_role": "developer",
                            "type": "tool_calls",
                            "text": (
                                "正在推进「提取 PDF 文本」；本轮将运行命令"
                                "以提取或验证证据，结果将用于确定下一步。"
                            ),
                            "data": {
                                "tools": ["bash"],
                                "public_progress": (
                                    "正在推进「提取 PDF 文本」；本轮将运行命令"
                                    "以提取或验证证据，结果将用于确定下一步。"
                                ),
                            },
                            "ts": 2.5,
                        },
                    ],
                    "operations": [
                        {
                            "id": "evt-1",
                            "seq": 8,
                            "ts": 2,
                            "type": "tool_result",
                            "data": {
                                "name": "write_file",
                                "tool_call_id": "call-1",
                                "path": "solar.py",
                                "result": "ok",
                                "thinking": "private",
                            },
                        },
                        {
                            "id": "evt-2",
                            "seq": 9,
                            "ts": 3,
                            "type": "file_patch",
                            "data": {
                                "path": "solar.py",
                                "session_rel_path": "solar.py",
                                "change_type": "modify",
                                "added": 2,
                                "deleted": 1,
                                "diff_numbered": "@@ -1 +1,2 @@\n-old\n+new",
                                "code_stage": {"id": "stage-1", "private": "hidden"},
                            },
                        },
                        {
                            "id": "evt-3",
                            "seq": 10,
                            "ts": 4,
                            "type": "compact",
                            "data": {
                                "reason": "auto",
                                "tier": 2,
                                "context_used_before": 7000,
                                "context_used_after": 4000,
                                "context_used_reduction": 3000,
                                "effective": True,
                            },
                        },
                    ],
                    "todos": [{"content": "Build model", "status": "in_progress"}],
                    "tasks": [],
                }

        app._ide_session = lambda user_id, session_id: FakeSession()
        state = app.ide_agent_state("user-a", "session-a")
        serialized = json.dumps(state)
        self.assertNotIn("private reasoning", serialized)
        self.assertNotIn("live_thinking", state)
        self.assertEqual(state["feed"][0]["agent_role"], "developer")
        self.assertEqual(state["operations"][0]["data"]["name"], "write_file")
        self.assertEqual(state["operations"][0]["data"]["path"], "solar.py")
        self.assertEqual(state["operations"][0]["data"]["tool_call_id"], "call-1")
        self.assertEqual(state["model"], "coder-model")
        self.assertEqual(state["context_left_tokens"], 6800)
        self.assertEqual(
            state["operations"][1]["data"]["diff_numbered"], "@@ -1 +1,2 @@\n-old\n+new"
        )
        self.assertNotIn("private", state["operations"][1]["data"]["code_stage"])
        self.assertEqual(state["operations"][2]["type"], "compact")
        self.assertEqual(state["operations"][2]["data"]["context_used_reduction"], 3000)
        progress_row = next(row for row in state["feed"] if row["type"] == "tool_calls")
        self.assertEqual(progress_row["data"]["tools"], ["bash"])
        self.assertEqual(progress_row["text"], "")
        self.assertNotIn("public_progress", progress_row["data"])

    def test_agent_state_keeps_persisted_operation_history(self):
        source = inspect.getsource(cc.AppContext.ide_agent_state)
        self.assertIn("sess.operations[-500:]", source)
        self.assertIn('"operations": operations[-500:]', source)

    def test_tool_event_context_exposes_only_safe_execution_summary(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = Path("/workspace/session")
        session._tool_result_local = threading.local()
        data = session._tool_event_context(
            "bash",
            {"command": "python verify.py", "secret": "do-not-publish"},
            {"exit_code": 0, "duration_ms": 42, "changed_files": ["verify.py"]},
        )
        self.assertEqual(data["command"], "python verify.py")
        self.assertEqual(data["cwd"], "/workspace/session")
        self.assertEqual(data["exit_code"], 0)
        self.assertEqual(data["changed_files"], ["verify.py"])
        self.assertNotIn("secret", data)

    def test_shell_environment_forces_utf8_for_local_and_remote_processes(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.files_root = Path(tempfile.mkdtemp())
        session.ide_remote_sandbox_required = False
        local = session._shell_process_env()
        self.assertEqual(local["PYTHONIOENCODING"], "utf-8")
        self.assertEqual(local["PYTHONUTF8"], "1")
        if os.name != "nt":
            self.assertIn("UTF-8", local["LC_ALL"])
        completed = cc.subprocess.run(
            [cc.sys.executable, "-c", "print('山海绘卷')"],
            env=local,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        self.assertEqual(completed.stdout.strip(), "山海绘卷")

    def test_shutdown_interrupt_cancels_and_kills_running_bash_without_session_lock(
        self,
    ):
        app = cc.AppContext.__new__(cc.AppContext)
        app._lock = threading.RLock()
        process = mock.Mock()
        process.pid = 4242
        process.poll.return_value = None
        session = types.SimpleNamespace(
            running=True, cancel_requested=False, _running_bash_proc=process
        )
        manager = types.SimpleNamespace(lock=threading.RLock(), sessions={"s": session})
        app._session_mgrs = {"u": manager}
        with (
            mock.patch.object(cc.os, "killpg") as killpg,
            mock.patch.object(cc.os, "getpgid", return_value=4242),
        ):
            report = app.interrupt_all_sessions_for_shutdown()
        self.assertTrue(session.cancel_requested)
        self.assertEqual(report["running"], 1)
        self.assertEqual(report["bash_terminated"], 1)
        if os.name == "posix":
            killpg.assert_called_once_with(4242, cc.signal.SIGKILL)


class IDERegressionFixTests(unittest.TestCase):
    def test_markdown_preview_removes_only_document_wide_indent(self):
        source = (
            "    # 标题\n\n    正文段落\n    第二行\n\n    ```python\n    "
            "print('ok')\n    ```"
        )
        normalized = cc.normalize_markdown_preview_text(source)
        self.assertTrue(normalized.startswith("# 标题"))
        self.assertIn("\n正文段落\n第二行", normalized)
        self.assertIn("```python\nprint('ok')", normalized)
        mixed = "# 标题\n    ```python\n    print('ok')\n    ```"
        self.assertEqual(cc.normalize_markdown_preview_text(mixed), mixed)

    def test_structured_ask_user_options_survive_state_and_answer_validation(self):
        app = cc.AppContext.__new__(cc.AppContext)
        pending = {
            "id": "ask-structured",
            "question": "Choose a renderer",
            "options": [
                {"label": "Canvas", "value": "canvas", "description": "2D fallback"},
                {"label": "WebGL", "value": "webgl"},
            ],
            "allow_free_text": False,
            "role": "planner",
        }

        class FakeSession:
            operations = []
            lock = threading.RLock()
            pending_user_question = pending

            def snapshot_safe(self, **_kwargs):
                return {
                    "running": False,
                    "pending_user_question": pending,
                    "conversation_feed": [],
                    "todos": [],
                    "tasks": [],
                }

        session = FakeSession()
        app._ide_session = lambda _user_id, _session_id: session
        state = app.ide_agent_state("user-a", "session-a")
        self.assertEqual(
            state["pending_user_question"]["options"][0]["value"], "canvas"
        )
        submitted = []
        app.submit_user_message = lambda _u, _s, content: (
            submitted.append(content) or {"ok": True}
        )
        out = app.ide_answer_agent_question(
            "user-a", "session-a", {"question_id": "ask-structured", "answer": "webgl"}
        )
        self.assertEqual(submitted, ["webgl"])
        self.assertEqual(out["answer"], "webgl")
        with self.assertRaisesRegex(ValueError, "available options"):
            app.ide_answer_agent_question(
                "user-a",
                "session-a",
                {"question_id": "ask-structured", "answer": "WebGL"},
            )

    def test_session_list_does_not_lock_or_rescan_loaded_history(self):
        manager = cc.SessionManager.__new__(cc.SessionManager)
        manager.lock = threading.RLock()
        manager.user_language = "zh-CN"
        manager.session_index = {
            f"s-{i}": {
                "id": f"s-{i}",
                "title": f"Old {i}",
                "updated_at": float(i),
                "message_count": i,
            }
            for i in range(2500)
        }

        class ExplodingLock:
            def acquire(self, *_args, **_kwargs):
                raise AssertionError("session list must not lock every loaded session")

        manager.sessions = {
            "s-2499": types.SimpleNamespace(
                id="s-2499",
                title="Current",
                running=False,
                updated_at=2500.0,
                lock=ExplodingLock(),
            )
        }
        page = manager.list(limit=20)
        self.assertEqual(len(page["sessions"]), 20)
        self.assertEqual(page["sessions"][0]["id"], "s-2499")
        self.assertEqual(page["sessions"][0]["message_count"], 2499)

    def test_code_preview_index_recovers_from_persisted_file_patch_operations(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = cc.SessionState.__new__(cc.SessionState)
            session.root = root
            session.code_preview_dir = root / "code_preview"
            session.code_preview_dir.mkdir()
            session.code_preview_index = {}
            session.operations = [
                {
                    "type": "file_patch",
                    "ts": 12.0,
                    "data": {
                        "path": "main.py",
                        "added": 1,
                        "deleted": 1,
                        "code_stage": {
                            "id": "stage_old",
                            "ts": 12.0,
                            "change_type": "modified",
                        },
                    },
                }
            ]
            bucket = session._code_preview_bucket_dir("main.py")
            (bucket / "stage_old.before.txt").write_text(
                "print('old')\n", encoding="utf-8"
            )
            (bucket / "stage_old.after.txt").write_text(
                "print('new')\n", encoding="utf-8"
            )
            session._recover_code_preview_index_from_operations()
            self.assertEqual(
                session.code_preview_index["main.py"][0]["id"], "stage_old"
            )
            self.assertEqual(session.code_preview_index["main.py"][0]["added"], 1)

    def test_windows_low_integrity_access_denied_is_cached_as_optional_degradation(
        self,
    ):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            key = os.path.normcase(str(root.resolve()))
            cc._WINDOWS_LOW_INTEGRITY_ROOTS.discard(key)
            cc._WINDOWS_LOW_INTEGRITY_FAILED_ROOTS.discard(key)
            try:
                with mock.patch.object(
                    cc,
                    "_windows_set_low_integrity_label",
                    side_effect=PermissionError(5, "Access is denied"),
                ) as label:
                    self.assertFalse(cc._windows_prepare_low_integrity_workspace(root))
                    self.assertFalse(cc._windows_prepare_low_integrity_workspace(root))
                label.assert_called_once()
                self.assertIn(key, cc._WINDOWS_LOW_INTEGRITY_FAILED_ROOTS)
            finally:
                cc._WINDOWS_LOW_INTEGRITY_FAILED_ROOTS.discard(key)


if __name__ == "__main__":
    unittest.main()
