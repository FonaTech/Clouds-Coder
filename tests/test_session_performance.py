import tempfile
import threading
import types
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc


def make_manager(root: Path, user_id: str = "user-a") -> cc.SessionManager:
    crypto = cc.CryptoBox(root / "codes")
    return cc.SessionManager(
        root / "codes" / user_id / "sessions",
        user_id,
        "http://127.0.0.1:11434",
        "demo-model",
        root / "skills",
        root / "js_lib",
        crypto,
        root,
    )


class CryptoBoxPerformanceTests(unittest.TestCase):
    def test_v2_round_trip_and_v1_backward_compatibility(self):
        with tempfile.TemporaryDirectory() as temp:
            crypto = cc.CryptoBox(Path(temp) / "codes")
            text = "Clouds Coder 加密兼容 " * 200

            encrypted = crypto.encrypt_text(text)
            envelope = cc.json.loads(encrypted)
            if cc._AESGCM is not None:
                self.assertEqual(envelope["v"], 2)
            self.assertEqual(crypto.decrypt_text(encrypted), text)

            legacy = crypto._encrypt_text_v1(text)
            self.assertEqual(cc.json.loads(legacy)["v"], 1)
            self.assertEqual(crypto.decrypt_text(legacy), text)

    @unittest.skipIf(cc._AESGCM is None, "cryptography AES-GCM unavailable")
    def test_v2_tampering_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            crypto = cc.CryptoBox(Path(temp) / "codes")
            envelope = cc.json.loads(crypto.encrypt_text("integrity"))
            ciphertext = bytearray(cc.base64.b64decode(envelope["c"]))
            ciphertext[-1] ^= 1
            envelope["c"] = cc.base64.b64encode(bytes(ciphertext)).decode("ascii")

            with self.assertRaisesRegex(ValueError, "integrity"):
                crypto.decrypt_text(cc.json_dumps(envelope))

    def test_legacy_multimegabyte_decryption_is_chunk_accelerated(self):
        with tempfile.TemporaryDirectory() as temp:
            crypto = cc.CryptoBox(Path(temp) / "codes")
            text = "0123456789abcdef" * 131_072
            legacy = crypto._encrypt_text_v1(text)

            started = cc.time.monotonic()
            restored = crypto.decrypt_text(legacy)
            elapsed = cc.time.monotonic() - started

            self.assertEqual(restored, text)
            self.assertLess(elapsed, 2.5)


class SessionCatalogPerformanceTests(unittest.TestCase):
    def test_cached_catalog_pages_do_not_rewalk_ten_thousand_rows(self):
        manager = cc.SessionManager.__new__(cc.SessionManager)
        manager.lock = threading.RLock()
        manager.user_language = "en"
        manager.sessions = {}
        manager.catalog_revision = 17
        manager.session_index = {
            f"session-{index}": {
                "id": f"session-{index}",
                "title": f"Session {index}",
                "updated_at": float(index),
                "message_count": index,
            }
            for index in range(10_000)
        }
        first = manager.list(limit=120)
        self.assertEqual(len(first["sessions"]), 120)
        self.assertEqual(first["total"], 10_000)
        self.assertTrue(first["has_more"])
        self.assertEqual(first["catalog_revision"], 17)

        class NoValues(dict):
            def values(self):
                raise AssertionError("cached page must not rewalk the full session index")

        manager.session_index = NoValues(manager.session_index)
        second = manager.list(limit=120, offset=120)
        self.assertEqual(len(second["sessions"]), 120)
        self.assertEqual(second["offset"], 120)

    def test_persisted_catalog_avoids_per_session_meta_reads_on_restart(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index_path = root / "codes" / "user-a" / "session_index.json"
            crypto = cc.CryptoBox(root / "codes")
            crypto.write_json(
                index_path,
                {
                    "version": 1,
                    "catalog_revision": 9,
                    "sessions": {
                        f"session-{index}": {
                            "id": f"session-{index}",
                            "title": f"Session {index}",
                            "updated_at": float(index),
                            "message_count": index,
                        }
                        for index in range(500)
                    },
                },
            )
            with mock.patch.object(
                cc.SessionManager,
                "_session_summary_from_disk",
                side_effect=AssertionError("persisted catalog should be authoritative"),
            ):
                manager = make_manager(root)
            page = manager.list(limit=80)
            self.assertEqual(page["catalog_revision"], 9)
            self.assertEqual(len(page["sessions"]), 80)
            self.assertEqual(page["total"], 500)

    def test_structural_catalog_changes_are_durable_before_return(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = make_manager(root)
            session = manager.create("Immediate")
            payload = manager.crypto.read_json(manager.session_index_path, {})
            self.assertIn(session.id, payload.get("sessions", {}))

            manager.rename(session.id, "Renamed")
            payload = manager.crypto.read_json(manager.session_index_path, {})
            self.assertEqual(payload["sessions"][session.id]["title"], "Renamed")

            self.assertTrue(manager.delete(session.id))
            payload = manager.crypto.read_json(manager.session_index_path, {})
            self.assertNotIn(session.id, payload.get("sessions", {}))

    def test_session_creation_persists_explicit_title_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            manager = make_manager(Path(temp))
            web = manager.create("Web Session", title_origin="default")
            ide_manual = manager.create("IDE Workspace", title_origin="manual")
            application = manager.create("Image Studio", title_origin="application")

            self.assertEqual(web.title_origin, "default")
            self.assertEqual(ide_manual.title_origin, "manual")
            self.assertEqual(application.title_origin, "application")
            payload = manager.crypto.read_json(manager.session_index_path, {})
            self.assertEqual(payload["sessions"][web.id]["title_origin"], "default")
            self.assertEqual(payload["sessions"][ide_manual.id]["title_origin"], "manual")
            self.assertEqual(payload["sessions"][application.id]["title_origin"], "application")

    def test_large_catalog_structural_changes_use_replayable_incremental_journal(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            crypto = cc.CryptoBox(root / "codes")
            index_path = root / "codes" / "user-a" / "session_index.json"
            crypto.write_json(
                index_path,
                {
                    "version": 1,
                    "catalog_revision": 10_000,
                    "sessions": {
                        f"session-{index}": {
                            "id": f"session-{index}",
                            "title": f"Session {index}",
                            "updated_at": float(index),
                            "message_count": index,
                        }
                        for index in range(10_000)
                    },
                },
            )
            manager = make_manager(root)
            with mock.patch.object(
                manager,
                "_session_index_payload_locked",
                side_effect=AssertionError("large structural changes must not rebuild the full index"),
            ):
                session = manager.create("Journal Create")
                manager.rename(session.id, "Journal Rename")

            restarted = make_manager(root)
            self.assertEqual(restarted.session_index[session.id]["title"], "Journal Rename")

            with mock.patch.object(
                manager,
                "_session_index_payload_locked",
                side_effect=AssertionError("large delete must remain O(1)"),
            ):
                self.assertTrue(manager.delete(session.id))
            restarted_after_delete = make_manager(root)
            self.assertNotIn(session.id, restarted_after_delete.session_index)

    def test_summary_update_keeps_first_page_bounded_after_cache_warmup(self):
        manager = cc.SessionManager.__new__(cc.SessionManager)
        manager.lock = threading.RLock()
        manager.user_language = "en"
        manager.sessions = {}
        manager.catalog_revision = 17
        manager._session_catalog_cache_revision = -1
        manager._session_catalog_cache = []
        manager._session_catalog_recent = {}
        manager._session_catalog_deleted_ids = set()
        manager._session_catalog_rebuild_pending = False
        manager.session_index = {
            f"session-{index}": {
                "id": f"session-{index}",
                "title": f"Session {index}",
                "updated_at": float(index),
                "message_count": index,
            }
            for index in range(10_000)
        }
        manager.list(limit=120)

        class NoValues(dict):
            def values(self):
                raise AssertionError("hot first page must not rewalk the full index")

        manager.session_index = NoValues(manager.session_index)
        manager.session_index["session-1"] = {
            **manager.session_index["session-1"],
            "updated_at": 20_000.0,
            "running": True,
        }
        manager._session_catalog_changed_locked("session-1")
        page = manager.list(limit=120)
        self.assertEqual(page["sessions"][0]["id"], "session-1")
        self.assertTrue(page["sessions"][0]["running"])


class LargeSessionSnapshotTests(unittest.TestCase):
    def test_legacy_state_load_keeps_only_bounded_runtime_windows(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills_root = root / "skills"
            skill_dir = skills_root / "demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo\ndescription: demo\n---\n# Demo\n",
                encoding="utf-8",
            )
            crypto = cc.CryptoBox(root / "codes")
            shared_skills = cc.SkillStore(skills_root)
            session_root = root / "codes" / "user-a" / "sessions"
            session_dir = session_root / "legacy"
            session_dir.mkdir(parents=True)
            crypto.write_json(
                session_dir / "state.json",
                {
                    "id": "legacy",
                    "messages": [
                        {"role": "user", "content": f"message-{index}", "ts": float(index)}
                        for index in range(2_000)
                    ],
                    "activity": [{"type": "status", "ts": float(index)} for index in range(700)],
                    "operations": [{"type": "status", "seq": index, "ts": float(index), "data": {}} for index in range(900)],
                    "uploads": [{"id": f"upload-{index}"} for index in range(140)],
                    "event_seq": 2_000,
                },
            )
            crypto.write_json(
                session_dir / "meta.json",
                {"id": "legacy", "title": "Legacy", "message_count": 20_000},
            )

            session = cc.SessionState(
                "legacy",
                "Legacy",
                session_root,
                "http://127.0.0.1:11434",
                "demo-model",
                skills_root,
                crypto,
                root,
                skills_snapshot=shared_skills,
                defer_initial_persist=True,
            )

            self.assertEqual(len(session.messages), cc.SESSION_RUNTIME_MESSAGE_WINDOW)
            self.assertEqual(len(session.activity), cc.SESSION_RUNTIME_ACTIVITY_WINDOW)
            self.assertEqual(len(session.operations), cc.SESSION_RUNTIME_OPERATION_WINDOW)
            self.assertEqual(len(session.uploads), cc.SESSION_RUNTIME_UPLOAD_WINDOW)
            self.assertEqual(session.ui_message_count, 20_000)

    def test_repeated_lite_snapshot_reuses_migrated_bounded_projection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = cc.SessionState(
                "session-large",
                "Large",
                root / "sessions",
                "http://127.0.0.1:11434",
                "demo-model",
                root / "skills",
                cc.CryptoBox(root / "codes"),
                root,
            )
            session.messages = [
                {
                    "role": "user" if index % 2 == 0 else "tool",
                    "content": f"message {index}",
                    "ts": float(index),
                }
                for index in range(20_000)
            ]
            session.operations = [
                {
                    "id": f"operation-{index}",
                    "seq": index + 1,
                    "ts": float(index),
                    "type": "status",
                    "data": {"summary": f"operation {index}"},
                }
                for index in range(2_000)
            ]
            session._ui_runtime_state_ready = False
            first = session.snapshot(lite=True)
            self.assertEqual(first["message_count"], 10_000)
            self.assertLessEqual(len(first["messages"]), 120)
            self.assertLessEqual(len(first["conversation_feed"]), 160)
            self.assertLessEqual(len(first["operations"]), 60)

            session._ui_message_is_countable = mock.Mock(
                side_effect=AssertionError("unchanged lite snapshot must not rescan messages")
            )
            second = session.snapshot(lite=True)
            self.assertEqual(second["snapshot_revision"], first["snapshot_revision"])
            session._ui_message_is_countable.assert_not_called()

    def test_lite_snapshot_cache_tracks_unemitted_transient_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = cc.SessionState(
                "session-transient",
                "Transient",
                root / "sessions",
                "http://127.0.0.1:11434",
                "demo-model",
                root / "skills",
                cc.CryptoBox(root / "codes"),
                root,
            )
            session.running = True
            first = session.snapshot(lite=True)
            self.assertEqual(first["live_thinking"], "")

            session.live_thinking_text = "new thought"
            second = session.snapshot(lite=True)
            self.assertEqual(second["live_thinking"], "new thought")

            session.scheduler_starting = True
            third = session.snapshot(lite=True)
            self.assertTrue(third["scheduler_starting"])

    def test_lite_snapshot_has_a_hard_serialized_byte_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            session = cc.SessionState(
                "session-byte-budget",
                "Large payload",
                root / "sessions",
                "http://127.0.0.1:11434",
                "demo-model",
                root / "skills",
                cc.CryptoBox(root / "codes"),
                root,
            )
            session.messages = [
                {
                    "id": f"message-{index}",
                    "seq": index + 1,
                    "role": "assistant" if index % 2 else "user",
                    "content": f"message-{index}:" + "x" * 24_000,
                    "thinking": "y" * 12_000,
                    "data": {"details": "z" * 20_000, "nested": [{"body": "q" * 8_000}] * 12},
                    "ts": float(index),
                }
                for index in range(140)
            ]
            session.operations = [
                {
                    "id": f"operation-{index}",
                    "seq": 1_000 + index,
                    "type": "command",
                    "ts": float(index),
                    "data": {"command": "echo test", "output": "o" * 30_000},
                }
                for index in range(80)
            ]
            session._ui_runtime_state_ready = False

            snapshot = session.snapshot(lite=True)
            encoded_size = len(cc.json_dumps(snapshot).encode("utf-8"))

            self.assertLessEqual(encoded_size, cc.LITE_SNAPSHOT_MAX_BYTES)
            self.assertEqual(snapshot["message_count"], 140)
            self.assertTrue(snapshot["ui_windows"]["conversation_feed"]["truncated"])
            self.assertTrue(any(row.get("ui_truncated") for row in snapshot["conversation_feed"]))


class IDEIncrementalStateTests(unittest.TestCase):
    def setUp(self):
        self.app = cc.AppContext.__new__(cc.AppContext)
        self.session = types.SimpleNamespace(
            title="Cursor",
            title_origin="manual",
            lock=threading.RLock(),
            operations=[
                {
                    "id": "operation-101",
                    "seq": 101,
                    "ts": 101.0,
                    "type": "status",
                    "data": {"summary": "one"},
                },
                {
                    "id": "operation-102",
                    "seq": 102,
                    "ts": 102.0,
                    "type": "status",
                    "data": {"summary": "two"},
                },
            ],
        )
        self.session.snapshot_safe = lambda **_kwargs: {
            "running": False,
            "scheduler_starting": True,
            "event_seq": 102,
            "snapshot_revision": 102,
            "feed_revision": 102,
            "operation_revision": 102,
            "conversation_feed": [
                {"id": "feed-101", "seq": 101, "role": "user", "type": "message", "text": "one", "ts": 101.0},
                {"id": "feed-102", "seq": 102, "role": "assistant", "type": "message", "text": "two", "ts": 102.0},
            ],
            "operations": self.session.operations,
            "todos": [],
            "tasks": [],
        }
        self.app._ide_session = lambda _user_id, _session_id: self.session

    def test_incremental_cursor_no_change_and_expiration(self):
        initial = self.app.ide_agent_state("user-a", "session-a")
        self.assertEqual([row["seq"] for row in initial["feed"]], [101, 102])
        self.assertFalse(initial["incremental"])
        self.assertTrue(initial["scheduler_starting"])

        delta = self.app.ide_agent_state(
            "user-a",
            "session-a",
            after_feed_seq=101,
            after_operation_seq=101,
            known_snapshot_revision=101,
        )
        self.assertEqual([row["seq"] for row in delta["feed"]], [102])
        self.assertEqual([row["seq"] for row in delta["operations"]], [102])
        self.assertTrue(delta["incremental"])

        unchanged = self.app.ide_agent_state(
            "user-a",
            "session-a",
            after_feed_seq=102,
            after_operation_seq=102,
            known_snapshot_revision=102,
        )
        self.assertEqual(unchanged["feed"], [])
        self.assertEqual(unchanged["operations"], [])

        expired = self.app.ide_agent_state(
            "user-a",
            "session-a",
            after_feed_seq=1,
            after_operation_seq=1,
            known_snapshot_revision=1,
        )
        self.assertTrue(expired["reset_required"])
        self.assertEqual(expired["feed"], [])

    def test_agent_state_byte_budget_pages_large_incremental_operations(self):
        operations = [
            {
                "id": f"operation-{index}",
                "seq": index,
                "ts": float(index),
                "type": "command",
                "data": {"command": "echo", "output": "x" * 20_000},
            }
            for index in range(1, 501)
        ]
        session = types.SimpleNamespace(
            title="Large IDE",
            title_origin="manual",
            lock=threading.RLock(),
            operations=operations,
        )
        session.snapshot_safe = lambda **_kwargs: {
            "running": False,
            "scheduler_starting": False,
            "event_seq": 500,
            "snapshot_revision": 500,
            "feed_revision": 500,
            "operation_revision": 500,
            "conversation_feed": [],
            "operations": operations[-60:],
            "agent_contexts": [],
            "todos": [],
            "tasks": [],
        }
        app = cc.AppContext.__new__(cc.AppContext)
        app._ide_session = lambda _user_id, _session_id: session

        state = app.ide_agent_state(
            "user-a",
            "session-a",
            after_operation_seq=0,
            known_snapshot_revision=1,
        )

        self.assertLessEqual(len(cc.json_dumps(state).encode("utf-8")), cc.IDE_AGENT_STATE_MAX_BYTES)
        self.assertTrue(state["incremental_has_more"])
        self.assertLess(state["operation_cursor"], 500)
        self.assertGreater(len(state["operations"]), 0)


class SubmissionAndLanguagePerformanceTests(unittest.TestCase):
    def test_kimi_invalid_parameter_retries_with_minimal_openai_payload(self):
        client = cc.OllamaClient(
            "https://ark.cn-beijing.volces.com",
            "kimi-k3",
            provider="kimi",
            endpoint="https://ark.cn-beijing.volces.com/api/plan/v1",
        )
        invalid = cc.OllamaError(
            'HTTP 400: {"error":{"code":"InvalidParameter","message":"A parameter specified in the request is not valid","param":"","type":"BadRequest"}}',
            status=400,
            body='{"error":{"code":"InvalidParameter","param":""}}',
        )
        success = {"choices": [{"message": {"content": "ok"}}]}
        client._post_json_url_with_retries = mock.Mock(side_effect=[invalid, success])
        tools = [{"type": "function", "function": {"name": "demo", "parameters": {"type": "object"}}}]

        result = client._chat_openai_compat(
            [{"role": "user", "content": "hello"}],
            tools=tools,
            tool_choice="demo",
            max_tokens=1234,
            temperature=0.7,
            reasoning={"payload": {"thinking": {"type": "enabled"}}, "strip_keys": ["thinking"]},
        )

        self.assertEqual(result["content"], "ok")
        retry_payload = client._post_json_url_with_retries.call_args_list[1].args[1]
        self.assertEqual(retry_payload["model"], "kimi-k3")
        self.assertEqual(retry_payload["tools"], tools)
        self.assertFalse(retry_payload["stream"])
        for key in ("temperature", "max_tokens", "tool_choice", "thinking"):
            self.assertNotIn(key, retry_payload)

    def test_shared_skill_snapshot_and_new_session_use_one_initial_state_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill_dir = root / "skills" / "demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: demo\ndescription: demo\n---\n# Demo\n",
                encoding="utf-8",
            )
            shared_skills = cc.SkillStore(root / "skills")
            crypto = cc.CryptoBox(root / "codes")
            manager = cc.SessionManager(
                root / "codes" / "user-a" / "sessions",
                "user-a",
                "http://127.0.0.1:11434",
                "demo-model",
                root / "skills",
                root / "js_lib",
                crypto,
                root,
                skills_snapshot=shared_skills,
            )
            with mock.patch.object(
                cc.SkillStore,
                "reload",
                side_effect=AssertionError("new session must reuse the shared parsed catalog"),
            ), mock.patch.object(
                cc.SessionState,
                "_persist",
                autospec=True,
            ) as persist:
                session = manager.create("Fast")

            self.assertEqual(len(session.skills.skills), len(shared_skills.skills))
            self.assertEqual(persist.call_count, 1)

    def test_default_capability_lookup_does_not_probe_kimi(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shared_skills = cc.SkillStore(root / "skills")
            crypto = cc.CryptoBox(root / "codes")
            session = cc.SessionState(
                "session-a",
                "Session A",
                root / "codes" / "user-a" / "sessions",
                "https://ark.cn-beijing.volces.com/api/plan/v1",
                "kimi-k3",
                root / "skills",
                crypto,
                root,
                default_llm_config={
                    "provider": "kimi",
                    "kimi_url": "https://ark.cn-beijing.volces.com/api/plan/v1",
                    "kimi_model": "kimi-k3",
                },
                skills_snapshot=shared_skills,
                defer_initial_persist=True,
            )
            session.multimodal_capability_cache = {}
            session.ollama.probe_multimodal_capabilities = mock.Mock(
                return_value=cc.default_multimodal_capabilities()
            )
            session.ollama.probe_cache_entry = mock.Mock(return_value={})

            session._ensure_active_profile_capabilities(force_probe=False)
            session.ollama.probe_multimodal_capabilities.assert_not_called()
            session._ensure_active_profile_capabilities(force_probe=True)
            session.ollama.probe_multimodal_capabilities.assert_called_once_with(force=True)

    def test_fast_accept_only_schedules_delayed_state_persistence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = make_manager(root)
            session = manager.create("Fast ACK")
            session.deferred_start_worker_started = True
            session._persist = mock.Mock()
            session._schedule_persist = mock.Mock()
            session._schedule_persist_delayed = mock.Mock()

            response = session.accept_user_message("hello")

            self.assertTrue(response["accepted"])
            self.assertTrue(response["deferred_start"])
            self.assertTrue(session.scheduler_starting)
            session._persist.assert_not_called()
            session._schedule_persist.assert_not_called()
            session._schedule_persist_delayed.assert_called_once_with(0.75)

    def test_default_language_update_does_not_touch_loaded_sessions(self):
        manager = cc.SessionManager.__new__(cc.SessionManager)
        manager.lock = threading.RLock()
        manager.user_language = "zh-CN"
        manager.sessions = {
            "session-a": types.SimpleNamespace(
                _set_ui_language=mock.Mock(side_effect=AssertionError("must not relabel session")),
                _persist=mock.Mock(side_effect=AssertionError("must not persist session")),
            )
        }
        manager._persist_user_prefs = mock.Mock()
        out = manager.set_user_language("en")
        self.assertEqual(out["language"], "en")
        manager._persist_user_prefs.assert_called_once_with()

    def test_app_submission_uses_fast_accept_path(self):
        app = cc.AppContext.__new__(cc.AppContext)
        session = types.SimpleNamespace(
            app_binding={},
            running=False,
            accept_user_message=mock.Mock(
                return_value={"ok": True, "accepted": True, "queued": True, "running": False}
            ),
            submit_user_message=mock.Mock(side_effect=AssertionError("slow submit path must run in background")),
        )
        manager = types.SimpleNamespace(
            get=lambda _session_id: session,
            prepare_user_intent_for_session=mock.Mock(
                side_effect=AssertionError("intent preparation must not block HTTP ACK")
            ),
        )
        app.manager_for_user = lambda _user_id: manager
        app.scheduler_limits_enabled = lambda: False
        app.telemetry = types.SimpleNamespace(record=lambda *_args, **_kwargs: None)
        app._publish_collaboration_agent_state = lambda *_args, **_kwargs: None
        out = app.submit_user_message("user-a", "session-a", "hello")
        self.assertTrue(out["accepted"])
        session.accept_user_message.assert_called_once_with("hello")

    def test_session_creation_does_not_hold_app_global_lock_during_manager_create(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app._lock = threading.RLock()
        app.telemetry = types.SimpleNamespace(record=lambda *_args, **_kwargs: None)
        app._session_creation_quota_status_locked = lambda *_args, **_kwargs: {
            "enabled": False,
            "remaining": None,
            "window_key": "2026-09-11",
        }
        app._load_session_daily_limit_state_locked = lambda *_args, **_kwargs: {
            "window_key": "2026-09-11",
            "used": 0,
        }
        app._save_session_daily_limit_state_locked = mock.Mock()

        class Manager:
            def create(self, _title):
                self.lock_was_owned = bool(app._lock._is_owned())
                return types.SimpleNamespace(id="session-a")

        manager = Manager()
        app.manager_for_user = lambda _user_id: manager
        session, _status = app.create_session_for_user("user-a", "Fast")
        self.assertEqual(session.id, "session-a")
        self.assertFalse(manager.lock_was_owned)

    def test_scheduler_running_counts_do_not_scan_loaded_sessions(self):
        app = cc.AppContext.__new__(cc.AppContext)
        session = types.SimpleNamespace(id="session-a", running=True, scheduler_starting=False)

        class NoValues(dict):
            def values(self):
                raise AssertionError("running counts must use the active set")

        manager = types.SimpleNamespace(sessions=NoValues({"session-a": session}))
        app._session_mgrs = {"user-a": manager}
        app._scheduler_active_sessions = {("user-a", "session-a")}
        app._scheduler_active_initialized = True
        total, per_user = app._running_counts_locked()
        self.assertEqual(total, 1)
        self.assertEqual(per_user, {"user-a": 1})

    def test_recent_submission_dedupe_survives_worker_pop(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.id = "session-a"
        session.running = False
        session.scheduler_starting = False
        session.deferred_start_worker_lock = threading.Lock()
        session.deferred_start_inputs = []
        session.deferred_start_recent_submissions = []
        session.deferred_start_seq = 0
        session.deferred_start_worker_started = True
        session.snapshot_revision = 0
        session.event_seq = 0
        session.updated_at = 0.0
        session._snapshot_cache_lite_key = None
        session._schedule_persist = mock.Mock()

        first = session.accept_user_message("same message")
        with session.deferred_start_worker_lock:
            session.deferred_start_inputs.pop(0)
        second = session.accept_user_message("same message")

        self.assertFalse(first.get("duplicate", False))
        self.assertTrue(second["duplicate"])
        self.assertEqual(second["queue_id"], first["queue_id"])
        self.assertEqual(session.deferred_start_inputs, [])

    def test_deferred_worker_keeps_starting_state_through_prepare(self):
        session = cc.SessionState.__new__(cc.SessionState)
        session.id = "session-a"
        session.lock = threading.RLock()
        session.running = False
        session.scheduler_starting = True
        session.deferred_start_worker_lock = threading.Lock()
        session.deferred_start_inputs = [
            {"id": 1, "content": "hello", "queued_at": cc.now_ts(), "reason": "accepted"}
        ]
        session.deferred_start_worker_started = True
        session.snapshot_revision = 1
        session.event_seq = 1
        session.updated_at = cc.now_ts()
        session._snapshot_cache_lite_key = None
        session._persist = mock.Mock()
        session._schedule_persist = mock.Mock()
        session._emit = mock.Mock()
        observed = []

        def prepare(_session, _text):
            observed.append(session.scheduler_starting)

        def submit(_text):
            observed.append(session.scheduler_starting)
            session.running = True
            return {"ok": True, "running": True}

        session.deferred_start_prepare_callback = prepare
        session.submit_user_message = submit
        session._deferred_start_worker_loop()

        self.assertEqual(observed, [True, True])
        self.assertTrue(session.running)
        self.assertFalse(session.scheduler_starting)
        self.assertFalse(session.deferred_start_worker_started)

    def test_scheduler_submission_ack_is_fast_and_deduplicated(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app._lock = threading.RLock()
        app._task_queue = cc.deque()
        app._task_queue_seq = 0
        app._task_submission_recent = cc.deque(maxlen=cc.SCHEDULER_SUBMISSION_DEDUPE_MAX)
        app.max_user = 1
        app.max_user_sessions = 1
        app.telemetry = types.SimpleNamespace(record=mock.Mock())

        session = cc.SessionState.__new__(cc.SessionState)
        session.id = "session-a"
        session.app_binding = {}
        session.running = False
        session.scheduler_starting = False
        session.collaboration_write_coordinator = None
        session.update_scheduler_visible_message = mock.Mock()
        session._emit = mock.Mock()

        prepare_started = threading.Event()
        release_prepare = threading.Event()
        submit_finished = threading.Event()

        def prepare(_session, _text):
            prepare_started.set()
            release_prepare.wait(2)

        def submit(_text):
            session.running = True
            submit_finished.set()
            return {"ok": True, "queued": False, "running": True}

        session.submit_user_message = submit
        manager = types.SimpleNamespace(
            lock=threading.RLock(),
            sessions={session.id: session},
            get=lambda _session_id: session,
            prepare_user_intent_for_session=prepare,
        )
        app._session_mgrs = {"user-a": manager}
        app.manager_for_user = lambda _user_id: manager

        started = cc.time.monotonic()
        first = app.submit_user_message("user-a", session.id, "slow preparation")
        elapsed = cc.time.monotonic() - started
        duplicate = app.submit_user_message("user-a", session.id, "slow preparation")

        self.assertLess(elapsed, 0.2)
        self.assertTrue(first["scheduler_started"])
        self.assertTrue(first["queued"])
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(duplicate["queue_id"], first["queue_id"])
        self.assertTrue(prepare_started.wait(1))
        self.assertFalse(submit_finished.is_set())

        release_prepare.set()
        self.assertTrue(submit_finished.wait(1))

    def test_frontend_contracts_are_bounded_and_incremental(self):
        self.assertIn("const SESSION_BOOT_LIMIT=120;", cc.APP_JS)
        self.assertNotIn("scheduleLoadRemainingSessions", cc.APP_JS)
        self.assertIn("sessionSearch", cc.APP_JS)
        self.assertIn("after_feed_seq=${S.agentFeedSeq}", cc.IDE_JS)
        self.assertIn("known_snapshot_revision=${S.agentSnapshotRevision}", cc.IDE_JS)
        self.assertIn("AGENT_RENDERED_KEY_LIMIT=720", cc.IDE_JS)
        self.assertIn("scheduleAgentEventFrame", cc.IDE_JS)
        self.assertIn("ideSessionSearch", cc.IDE_INDEX_HTML)
        self.assertIn("S.sessionById.set(sid,next)", cc.APP_JS)
        self.assertIn("S.sessionById.set(sid,row)", cc.APP_JS)
        self.assertIn("submissionBySession:new Map()", cc.APP_JS)
        self.assertIn("S.snap?.scheduler_starting?t('starting')", cc.APP_JS)
        self.assertIn("_submissionStateFromAck(sessionId,out)", cc.APP_JS)
        self.assertIn("initialSnapshot:_initialSessionSnapshot(row)", cc.APP_JS)
        self.assertIn("message_count:Math.max(0,Number(src.message_count||0))", cc.APP_JS)
        self.assertNotIn("scheduleSnapshot({forceFull:true,delayMs:0,allowWhenFrozen:true})},520", cc.APP_JS)
        self.assertIn("SUBMISSION_STATE_MAX=48", cc.APP_JS)
        self.assertIn("starting=!!state.scheduler_starting", cc.IDE_JS)
        self.assertIn("agentSubmissionStatus:'',agentSubmissionPendingUntil:0", cc.IDE_JS)
        self.assertNotIn("if(!busy&&!awaiting&&S.agentSubmitting)S.agentSubmitting=false", cc.IDE_JS)
        self.assertIn("S.agentSubmissionStatus='starting'", cc.IDE_JS)
        self.assertIn("await switchSession(out.id,true,{roots:out.roots})", cc.IDE_JS)
        self.assertIn("scheduleAgentPoll(0);scheduleSessionWorkspaceBootstrap", cc.IDE_JS)
        self.assertIn("function applyImmediateSessionRoots", cc.IDE_JS)
        self.assertIn("out?.incremental_has_more?0", cc.IDE_JS)
        self.assertIn("FAST_START_DEFER_CAPABILITY_PROBE", Path(cc.__file__).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
