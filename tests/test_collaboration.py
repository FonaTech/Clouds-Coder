import http.client
import json
import os
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc

CollaborationError = cc.CollaborationError
CollaborationStore = cc.CollaborationStore
apply_text_operation = cc.apply_text_operation
transform_text_operation = cc.transform_text_operation


class CollaborationStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = CollaborationStore(
            self.root / "state" / "collaboration.sqlite",
            self.root / "Codes",
            self.root / "state" / "collaboration",
        )
        self.password = "Valid-project-pass-123!"
        self.project = self.store.create_project(
            "Project Alpha", self.password, timezone_name="Asia/Shanghai")

    def tearDown(self):
        self.temp.cleanup()

    def admit(self, nickname="Alice", secret="a" * 40, ip="192.168.1.20"):
        return self.store.request_admission(
            self.project["name"],
            self.password,
            secret,
            nickname,
            device_label=nickname + " laptop",
            client_ip=ip,
        )

    def approve_and_login(self, nickname="Alice", secret="a" * 40, ip="192.168.1.20"):
        pending = self.admit(nickname, secret, ip)
        self.store.approve_device(self.project["project_id"], pending["device_id"])
        logged_in = self.admit(nickname, secret, ip)
        principal = self.store.authenticate(
            logged_in["access_token"],
            csrf_token=logged_in["csrf_token"],
            require_csrf=True,
            client_ip=ip,
        )
        return pending, logged_in, principal

    def test_password_is_hashed_and_never_persisted_as_plaintext(self):
        raw = (self.root / "state" / "collaboration.sqlite").read_bytes()
        self.assertNotIn(self.password.encode("utf-8"), raw)
        with self.store._connect() as conn:
            row = conn.execute(
                "SELECT password_algorithm,password_iterations,password_hash,password_salt FROM projects WHERE project_id=?",  # noqa: E501
                (self.project["project_id"],),
            ).fetchone()
        self.assertEqual(row["password_algorithm"], "pbkdf2_hmac_sha256")
        self.assertEqual(row["password_iterations"], 600_000)
        self.assertNotEqual(row["password_hash"], self.password)

    def test_missing_initialized_database_fails_closed(self):
        self.store.db_path.unlink()

        self.assertEqual(
            self.store.storage_health(),
            {"available": False, "code": "collaboration_store_unavailable"},
        )
        self.assertFalse(self.store.db_path.exists())
        with self.assertRaises(sqlite3.OperationalError):
            self.store.list_projects()

    def test_same_ip_different_devices_keep_distinct_identities(self):
        first = self.admit("Alice", "a" * 40, "192.168.1.40")
        second = self.admit("Bob", "b" * 40, "192.168.1.40")
        self.assertNotEqual(first["device_id"], second["device_id"])
        members = self.store.list_members(self.project["project_id"])["members"]
        self.assertEqual({row["nickname"] for row in members}, {"Alice", "Bob"})
        self.assertEqual({row["last_ip"] for row in members}, {"192.168.1.40"})

    def test_document_version_returns_immutable_text_history(self):
        _, _, principal = self.approve_and_login()
        self.store.write_file(principal, "index.html", b"<h1>one</h1>\n", 0)
        self.store.write_file(principal, "index.html", b"<h1>two</h1>\n", 1)

        first = self.store.document_version(
            principal.project_id, "index.html", 1
        )
        latest = self.store.document_version(principal.project_id, "index.html")

        self.assertEqual(first["content"], "<h1>one</h1>\n")
        self.assertEqual(first["revision"], 1)
        self.assertEqual(latest["content"], "<h1>two</h1>\n")
        self.assertEqual(latest["revision"], 2)

    def test_embedded_ide_history_uses_collaboration_revisions(self):
        _, _, principal = self.approve_and_login()
        self.store.write_file(principal, "main.py", b"value = 1\n", 0)
        self.store.write_file(principal, "main.py", b"value = 2\n", 1)
        app = cc.AppContext.__new__(cc.AppContext)
        app.collaboration = self.store
        app._collaboration_principal_for_ide_user = lambda user_id: principal

        stages = app.ide_code_preview_stages(
            "collab:test", "session-a", root_id="session", rel="main.py"
        )
        first = app.ide_code_preview_payload(
            "collab:test",
            "session-a",
            root_id="session",
            rel="main.py",
            stage_id="collab:1",
        )

        self.assertEqual([row["id"]
                         for row in stages["stages"]], ["collab:1", "collab:2"])
        self.assertEqual(stages["latest_id"], "collab:2")
        self.assertEqual(first["full_text"], "value = 1\n")
        self.assertEqual(first["stage"]["index"], 1)

    def test_presence_stays_online_for_ten_minutes_after_activity(self):
        _, _, principal = self.approve_and_login()
        with mock.patch.object(cc, "_now", return_value=1_000.0):
            self.store.update_presence(principal, document_path="", cursor={})
        with mock.patch.object(cc, "_now", return_value=1_599.0):
            snapshot = self.store.snapshot(principal)
        self.assertEqual(
            [row["member_id"] for row in snapshot["presence"]],
            [principal.member_id],
        )

        with mock.patch.object(cc, "_now", return_value=1_601.0):
            snapshot = self.store.snapshot(principal)
        self.assertEqual(snapshot["presence"], [])

    def test_embedded_ide_starts_and_repeats_collaboration_presence_heartbeat(self):
        self.assertIn("function startCollaborationPresenceHeartbeat()", cc.IDE_JS)
        self.assertIn(
            "postCollaborationPresence().catch(()=>{});"
            "S.collaborationPresenceHeartbeat=setInterval(",
            cc.IDE_JS,
        )
        self.assertIn("),60000)", cc.IDE_JS)
        self.assertIn(
            "connectCollaborationEvents();startCollaborationPresenceHeartbeat()",
            cc.IDE_JS,
        )

    def test_embedded_ide_actively_notifies_collaboration_conflicts(self):
        self.assertIn("function showCollaborationConflictNotice(", cc.IDE_JS)
        self.assertIn("showCollaborationConflictNotice(active)", cc.IDE_JS)
        self.assertIn("Shared workspace conflict:", cc.IDE_JS)
        self.assertIn("Review Conflicts", cc.IDE_JS)
        self.assertIn("function openCollaborationConflictReview(", cc.IDE_JS)
        self.assertIn("/review`", cc.IDE_JS)
        self.assertIn("/resolve`", cc.IDE_JS)
        self.assertIn("/candidates/${qs(candidateId)}`", cc.IDE_JS)

    def test_blocked_device_cannot_reenter_and_old_session_is_revoked(self):
        pending, logged_in, principal = self.approve_and_login()
        self.store.set_member_access(
            self.project["project_id"], principal.member_id, "block")
        with self.assertRaises(CollaborationError) as blocked_session:
            self.store.authenticate(logged_in["access_token"])
        self.assertEqual(blocked_session.exception.code, "session_expired")
        with self.assertRaises(CollaborationError) as blocked_login:
            self.admit()
        self.assertEqual(blocked_login.exception.code, "device_blocked")

    def test_password_rotation_revokes_sessions_but_keeps_approved_device(self):
        pending, logged_in, principal = self.approve_and_login()
        new_password = "New-project-pass-456!"
        rotated = self.store.rotate_password(self.project["project_id"], new_password)
        self.assertEqual(rotated["password_version"], 2)
        with self.assertRaises(CollaborationError):
            self.store.authenticate(logged_in["access_token"])
        with self.assertRaises(CollaborationError):
            self.store.request_admission(
                self.project["name"], self.password, "a" * 40, "Alice")
        resumed = self.store.request_admission(
            self.project["name"],
            new_password,
            "a" * 40,
            "Alice",
            client_ip="192.168.1.20")
        self.assertEqual(resumed["status"], "approved")
        self.assertEqual(resumed["member"]["member_id"], principal.member_id)

    def test_path_traversal_and_symlink_escape_are_rejected(self):
        project_id = self.project["project_id"]
        for value in ("../secret", "/etc/passwd", "a/../../secret", "a//b"):
            with self.subTest(value=value), self.assertRaises(CollaborationError):
                self.store.resolve_path(project_id, value)
        workspace = self.store.project_workspace(project_id)
        outside = self.root / "outside"
        outside.mkdir()
        link = workspace / "linked"
        try:
            link.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symbolic links are unavailable")
        with self.assertRaises(CollaborationError) as escaped:
            self.store.resolve_path(project_id, "linked/file.txt")
        self.assertEqual(escaped.exception.code, "symlink_forbidden")

    def test_concurrent_ot_insertions_are_transformed_deterministically(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        pending_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        self.store.approve_device(self.project["project_id"], pending_b["device_id"])
        login_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        bob = self.store.authenticate(login_b["access_token"])
        self.store.write_file(alice, "notes.txt", b"abc", 0)
        first = self.store.submit_operation(
            alice,
            "notes.txt",
            1,
            [{"retain": 1}, {"insert": "X"}, {"retain": 2}],
            client_operation_id="alice-op-0001",
        )
        second = self.store.submit_operation(
            bob,
            "notes.txt",
            1,
            [{"retain": 1}, {"insert": "Y"}, {"retain": 2}],
            client_operation_id="bob-op-00001",
        )
        current = self.store.read_document(self.project["project_id"], "notes.txt")
        self.assertEqual(first["revision"], 2)
        self.assertEqual(second["revision"], 3)
        self.assertEqual(current["content"], "aXYbc")

    def test_stale_whole_file_write_creates_immutable_candidates_and_freezes(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "shared.txt", b"base", 0)
        self.store.write_file(alice, "shared.txt", b"current", 1)
        with self.assertRaises(CollaborationError) as conflict:
            self.store.write_file(alice, "shared.txt", b"stale", 1)
        self.assertEqual(conflict.exception.code, "revision_conflict")
        pending_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        self.store.approve_device(self.project["project_id"], pending_b["device_id"])
        login_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        bob = self.store.authenticate(login_b["access_token"])
        with self.assertRaises(CollaborationError):
            self.store.write_file(bob, "shared.txt", b"another stale branch", 1)
        cases = self.store.list_conflicts(self.project["project_id"], status="open")
        self.assertEqual(len(cases), 1)
        self.assertEqual([row["branch_label"]
                         for row in cases[0]["candidates"]], ["A", "B", "C"])
        with self.assertRaises(CollaborationError) as frozen:
            self.store.write_file(alice, "shared.txt", b"next", 2)
        self.assertEqual(frozen.exception.code, "document_frozen")

    def test_external_write_is_persisted_as_conflict_before_409(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "external.txt", b"database", 0)
        path = self.store.project_workspace(self.project["project_id"]) / "external.txt"
        path.write_text("outside", encoding="utf-8")
        with self.assertRaises(CollaborationError) as conflict:
            self.store.read_document(self.project["project_id"], "external.txt")
        self.assertEqual(conflict.exception.code, "external_write_conflict")
        cases = self.store.list_conflicts(self.project["project_id"], status="open")
        self.assertEqual(len(cases), 1)
        with self.store._connect() as conn:
            frozen = conn.execute(
                "SELECT frozen FROM documents WHERE project_id=? AND path='external.txt'",  # noqa: E501
                (self.project["project_id"],
                 )).fetchone()[0]
        self.assertEqual(frozen, 1)

    def test_external_watcher_ignores_transient_truncate_then_restore(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "transient.txt", b"complete", 0)
        path = self.store.project_workspace(
            self.project["project_id"]) / "transient.txt"

        path.write_bytes(b"")
        with mock.patch.object(cc, "_now", return_value=100.0):
            first = self.store.scan_external_writes()
        with mock.patch.object(cc, "_now", return_value=100.4):
            second = self.store.scan_external_writes()
        path.write_bytes(b"complete")
        with mock.patch.object(cc, "_now", return_value=100.5):
            restored = self.store.scan_external_writes()

        self.assertEqual(first["count"], 0)
        self.assertEqual(second["count"], 0)
        self.assertEqual(restored["count"], 0)
        self.assertEqual(self.store.list_conflicts(
            self.project["project_id"], status="open"), [])

    def test_external_watcher_confirms_stable_real_write(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "stable-external.txt", b"database", 0)
        path = self.store.project_workspace(
            self.project["project_id"]) / "stable-external.txt"
        path.write_bytes(b"outside")

        with mock.patch.object(cc, "_now", return_value=200.0):
            first = self.store.scan_external_writes()
        with mock.patch.object(cc, "_now", return_value=201.0):
            confirmed = self.store.scan_external_writes()

        self.assertEqual(first["count"], 0)
        self.assertEqual(confirmed["count"], 1)
        conflict = self.store.list_conflicts(
            self.project["project_id"], status="open")[0]
        self.assertEqual(conflict["reason"], "external_write")

    def test_process_same_content_retry_is_idempotent_not_conflict(self):
        _, _, alice = self.approve_and_login()
        written = self.store.write_file(alice, "same.txt", b"same content", 0)

        retried = self.store.adopt_process_write(alice, "same.txt", b"same content", 0)

        self.assertTrue(retried["ok"])
        self.assertTrue(retried["idempotent"])
        self.assertEqual(retried["revision"], written["revision"])
        self.assertEqual(self.store.list_conflicts(
            self.project["project_id"], status="open"), [])

    def test_process_delete_is_committed_without_empty_conflict_branch(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "remove-me.txt", b"temporary", 0)
        coordinator = cc.CollaborationWriteCoordinator(
            self.store,
            alice.project_id,
            alice.member_id,
            alice.device_id,
        )
        path = self.store.project_workspace(
            self.project["project_id"]) / "remove-me.txt"

        with coordinator.mutation_lease():
            before = coordinator.begin_process()
            path.unlink()
            changes = coordinator.finish_process(before)

        deleted = next(row for row in changes if row.get("path") == "remove-me.txt")
        self.assertTrue(deleted["ok"])
        self.assertEqual(deleted["action"], "delete")
        self.assertEqual(self.store.list_conflicts(
            self.project["project_id"], status="open"), [])
        with self.store._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM documents WHERE project_id=? AND path='remove-me.txt'",
                (self.project["project_id"],),
            ).fetchone()
        self.assertIsNone(row)

    def test_admin_emergency_abort_restores_baseline_and_unfreezes_document(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "abort.txt", b"base", 0)
        self.store.write_file(alice, "abort.txt", b"current", 1)
        with self.assertRaises(CollaborationError):
            self.store.write_file(alice, "abort.txt", b"stale", 1)
        conflict = self.store.list_conflicts(
            self.project["project_id"], status="open")[0]

        result = self.store.emergency_abort_conflict(
            self.project["project_id"], conflict["conflict_id"], actor_id="admin-test"
        )

        self.assertEqual(result["status"], "aborted")
        self.assertEqual(
            self.store.project_workspace(self.project["project_id"]).joinpath(
                "abort.txt").read_bytes(),
            b"current",
        )
        with self.store._connect() as conn:
            document = conn.execute(
                "SELECT frozen FROM documents WHERE project_id=? AND path='abort.txt'",
                (self.project["project_id"],),
            ).fetchone()
            audit = conn.execute(
                "SELECT action,actor_id FROM audit_events WHERE target_id=? ORDER BY created_at DESC LIMIT 1",  # noqa: E501
                (conflict["conflict_id"],),
            ).fetchone()
        self.assertEqual(document["frozen"], 0)
        self.assertEqual((audit["action"], audit["actor_id"]),
                         ("conflict.emergency_abort", "admin-test"))

    def test_unassigned_conflict_review_roles_are_claimed_by_distinct_members(self):
        _, _, alice = self.approve_and_login()
        pending_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        self.store.approve_device(self.project["project_id"], pending_b["device_id"])
        login_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        bob = self.store.authenticate(login_b["access_token"])
        self.store.write_file(alice, "external-review.txt", b"database", 0)
        path = self.store.project_workspace(
            self.project["project_id"]) / "external-review.txt"
        path.write_text("outside", encoding="utf-8")
        with self.assertRaises(CollaborationError):
            self.store.read_document(self.project["project_id"], "external-review.txt")
        conflict = self.store.list_conflicts(
            self.project["project_id"], status="open")[0]
        candidate_id = conflict["candidates"][0]["candidate_id"]

        first = self.store.submit_conflict_review(
            alice,
            conflict["conflict_id"],
            role="primary",
            candidate_id=candidate_id,
            risk="baseline is known",
            reason="keep the database baseline",
        )
        self.assertEqual(first["status"], "reviewing")
        claimed = self.store.list_conflicts(self.project["project_id"])[0]
        self.assertEqual(claimed["primary_reviewer"], alice.member_id)
        with self.assertRaises(CollaborationError) as duplicate:
            self.store.submit_conflict_review(
                alice,
                conflict["conflict_id"],
                role="secondary",
                candidate_id=candidate_id,
                risk="same reviewer",
                reason="must not be accepted",
            )
        self.assertEqual(duplicate.exception.code, "reviewer_separation_required")

        second = self.store.submit_conflict_review(
            bob,
            conflict["conflict_id"],
            role="secondary",
            candidate_id=candidate_id,
            risk="external edit will be discarded",
            reason="the baseline is authoritative",
        )
        self.assertEqual(second["status"], "ready")
        reviewed = self.store.list_conflicts(self.project["project_id"])[0]
        self.assertEqual(reviewed["secondary_reviewer"], bob.member_id)
        self.assertEqual(len(reviewed["reviews"]), 2)

    def test_recovery_restores_missing_file_from_committed_document(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "recover.txt", b"durable", 0)
        path = self.store.project_workspace(self.project["project_id"]) / "recover.txt"
        path.unlink()
        report = self.store.recover_files()
        self.assertIn(f"{self.project['project_id']}:recover.txt", report["repaired"])
        self.assertEqual(path.read_bytes(), b"durable")

    def test_ide_style_rename_and_delete_keep_document_state_consistent(self):
        _, _, alice = self.approve_and_login()
        self.store.write_file(alice, "folder/original.txt", b"shared", 0)
        renamed = self.store.rename_path(alice, "folder", "renamed")
        self.assertEqual(renamed["document_count"], 1)
        current = self.store.read_document(
            self.project["project_id"], "renamed/original.txt")
        self.assertEqual(current["content"], "shared")
        with self.assertRaises(CollaborationError):
            self.store.read_document(self.project["project_id"], "folder/original.txt")
        deleted = self.store.delete_path(alice, "renamed", recursive=True)
        self.assertEqual(deleted["document_count"], 1)
        with self.assertRaises(CollaborationError):
            self.store.read_document(self.project["project_id"], "renamed/original.txt")

    def test_audit_chain_detects_tampering(self):
        self.admit()
        self.assertTrue(self.store.verify_audit_chain()["ok"])
        with self.store._connect() as conn:
            conn.execute(
                "UPDATE audit_events SET action='tampered' WHERE audit_id=(SELECT MAX(audit_id) FROM audit_events)")  # noqa: E501
        self.assertFalse(self.store.verify_audit_chain()["ok"])

    def test_blackboard_non_owner_change_requires_owner_proposal_resolution(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        pending_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        self.store.approve_device(self.project["project_id"], pending_b["device_id"])
        login_b = self.admit("Bob", "b" * 40, "192.168.1.21")
        bob = self.store.authenticate(login_b["access_token"])
        created = self.store.upsert_blackboard_item(
            alice, {"title": "Owner task", "status": "pending"})
        proposed = self.store.upsert_blackboard_item(
            bob,
            {"item_id": created["item_id"], "title": "Owner task",
                "status": "completed", "result_summary": "done"},
        )
        self.assertTrue(proposed["proposal"])
        result = self.store.resolve_blackboard_proposal(
            alice, proposed["proposal_id"], accept=True)
        self.assertEqual(result["status"], "accepted")
        item = next(row for row in self.store.blackboard(
            self.project["project_id"]) if row["item_id"] == created["item_id"])
        self.assertEqual(item["status"], "completed")

    def test_agent_tasks_merge_atomically_with_one_active_worker_coordinator(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        barrier = threading.Barrier(6)
        results = []
        errors = []

        def begin(index):
            try:
                barrier.wait()
                results.append(
                    self.store.begin_agent_task(
                        alice,
                        agent_id=f"agent:session-{index}",
                        session_id=f"session-{index}",
                        task_text="Implement the shared login repair and verify it.",
                    )
                )
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=begin, args=(index,)) for index in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 6)
        self.assertEqual(len({row["item_id"] for row in results}), 1)
        self.assertEqual(sum(row["role"] == "coordinator" for row in results), 1)
        self.assertEqual(sum(not row["merged"] for row in results), 1)

        item = self.store.blackboard(self.project["project_id"])[0]
        self.assertEqual(item["origin"], "agent_bridge")
        self.assertEqual(len(item["participants"]), 6)
        coordinator = next(
            row for row in item["participants"] if row["role"] == "coordinator")
        self.assertEqual(coordinator["agent_id"], item["coordinator_agent_id"])
        self.assertIn("Execute", coordinator["assignment"])
        self.assertIn("divide", coordinator["assignment"])

    def test_ide_agent_tasks_match_real_objective_not_generic_envelope_title(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        cfd = self.store.begin_agent_task(
            alice,
            agent_id="agent:cfd",
            session_id="cfd",
            task_text=(
                "IDE programming request.\n"
                "Workspace root: Shared workspace (session)\n"
                "Writable path: /Users/Alice/private/workspace\n\n"
                "完成一个 CFD 流体力学仿真软件。"
            ),
        )
        fem = self.store.begin_agent_task(
            alice,
            agent_id="agent:fem",
            session_id="fem",
            task_text=(
                "IDE programming request.\n"
                "Workspace root: Shared workspace (session)\n"
                "Writable path: /Users/Alice/private/workspace\n\n"
                "完成一个固体力学 FEM 仿真软件。"
            ),
        )
        same_cfd = self.store.begin_agent_task(
            alice,
            agent_id="agent:cfd-review",
            session_id="cfd-review",
            task_text=(
                "IDE programming request.\n"
                "Workspace root: another label (session)\n"
                "Writable path: /home/alice/other-workspace\n\n"
                "完成一个 CFD 流体力学仿真软件。"
            ),
        )

        self.assertNotEqual(cfd["item_id"], fem["item_id"])
        self.assertEqual(cfd["item_id"], same_cfd["item_id"])
        self.assertFalse(fem["merged"])
        self.assertTrue(same_cfd["merged"])
        titles = {row["title"]
                  for row in self.store.blackboard(self.project["project_id"])}
        self.assertIn("完成一个 CFD 流体力学仿真软件。", titles)
        self.assertIn("完成一个固体力学 FEM 仿真软件。", titles)
        self.assertNotIn("IDE programming request.", titles)

    def test_coordinator_delegates_plan_while_contributors_only_publish_own_evidence(
            self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        first = self.store.begin_agent_task(
            alice,
            agent_id="agent:first",
            session_id="first",
            task_text="Repair collaboration task routing.",
        )
        second = self.store.begin_agent_task(
            alice,
            agent_id="agent:second",
            session_id="second",
            task_text="Repair collaboration task routing.",
        )
        self.assertEqual(first["role"], "coordinator")
        self.assertEqual(second["role"], "contributor")

        rejected = self.store.record_agent_blackboard_update(
            alice,
            agent_id="agent:second",
            session_id="second",
            section="plan_steps",
            content="1. Replace the complete plan",
        )
        self.assertTrue(rejected["rejected"])
        self.assertEqual(rejected["reason"], "coordinator_only")
        accepted = self.store.record_agent_blackboard_update(
            alice,
            agent_id="agent:first",
            session_id="first",
            section="plan_steps",
            content="1. Inspect routing and implement the backend\n2. Verify the IDE event bridge",  # noqa: E501
        )
        self.assertTrue(accepted["recorded"])
        item = self.store.blackboard(self.project["project_id"])[0]
        assignments = {row["agent_id"]: row["assignment"]
                       for row in item["participants"]}
        self.assertIn("Inspect routing and implement the backend",
                      assignments["agent:first"])
        self.assertIn("Verify the IDE event bridge", assignments["agent:second"])
        self.assertIn("integrate participant results", assignments["agent:first"])
        self.assertEqual(
            item["coordination_plan"], [
                "Inspect routing and implement the backend", "Verify the IDE event bridge"], )  # noqa: E501

        own_clue = self.store.record_agent_blackboard_update(
            alice,
            agent_id="agent:second",
            session_id="second",
            section="research_notes",
            content="The event route is missing a refresh trigger.",
        )
        self.assertTrue(own_clue["recorded"])
        item = self.store.blackboard(self.project["project_id"])[0]
        clue = next(row for row in item["evidence"]
                    if row["summary"].startswith("The event route"))
        self.assertEqual(clue["agent_id"], "agent:second")

    def test_agent_bridge_redacts_private_prompt_credentials_and_host_paths(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        started = self.store.begin_agent_task(
            alice,
            agent_id="agent:safe",
            session_id="safe",
            task_text=(
                "Fix authentication. api_key=super-secret-value password=hunter2 "
                "and inspect /Users/Alice/private/project.py"
            ),
        )
        self.store.record_agent_task_evidence(
            alice,
            agent_id="agent:safe",
            session_id="safe",
            kind="clue",
            summary="Bearer abcdefghijklmnop was found in /Users/Alice/private/config.json",  # noqa: E501
        )
        private = self.store.record_agent_blackboard_update(
            alice,
            agent_id="agent:safe",
            session_id="safe",
            section="conversation_history",
            content="Private conversation must-not-be-public",
        )
        self.assertTrue(private["skipped"])
        self.assertEqual(private["reason"], "private_section")
        self.store.finish_agent_task(
            alice,
            agent_id="agent:safe",
            session_id="safe",
            status="completed",
            result_summary="Completed without publishing password=hunter2 or sk-secretcredential123456789.",  # noqa: E501
        )
        public_payload = json.dumps(self.store.blackboard(
            self.project["project_id"]), ensure_ascii=False)
        self.assertNotIn("super-secret-value", public_payload)
        self.assertNotIn("hunter2", public_payload)
        self.assertNotIn("abcdefghijklmnop", public_payload)
        self.assertNotIn("/Users/Alice", public_payload)
        self.assertNotIn("sk-secretcredential123456789", public_payload)
        self.assertNotIn("must-not-be-public", public_payload)
        self.assertIn("[redacted]", public_payload)
        self.assertEqual(started["role"], "coordinator")

    def test_merged_task_waits_for_all_agents_and_preserves_each_result(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        first = self.store.begin_agent_task(
            alice,
            agent_id="agent:first",
            session_id="first",
            task_text="Implement and review one shared change.",
        )
        self.store.begin_agent_task(
            alice,
            agent_id="agent:second",
            session_id="second",
            task_text="Implement and review one shared change.",
        )
        first_done = self.store.finish_agent_task(
            alice,
            agent_id="agent:first",
            session_id="first",
            status="completed",
            result_summary="Backend change completed.",
        )
        self.assertEqual(first_done["status"], "in_progress")
        second_blocked = self.store.finish_agent_task(
            alice,
            agent_id="agent:second",
            session_id="second",
            status="blocked",
            result_summary="Review found an unresolved constraint.",
        )
        self.assertEqual(second_blocked["status"], "blocked")
        item = next(row for row in self.store.blackboard(
            self.project["project_id"]) if row["item_id"] == first["item_id"])
        self.assertEqual(item["status"], "blocked")
        self.assertIn("Backend change completed", item["result_summary"])
        self.assertIn("unresolved constraint", item["result_summary"])

    def test_finishing_agent_closes_its_active_file_intents(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        self.store.begin_agent_task(
            alice,
            agent_id="agent:writer",
            session_id="writer",
            task_text="Implement one shared change.",
        )
        self.store.update_agent(
            alice,
            agent_id="agent:writer",
            session_id="writer",
            status="running",
        )
        self.store.declare_intent(
            alice,
            "index.html",
            agent_id="agent:writer",
            intent="edit_file",
        )

        finished = self.store.finish_agent_task(
            alice,
            agent_id="agent:writer",
            session_id="writer",
            status="completed",
            result_summary="Change and validation completed.",
        )

        self.assertEqual(finished["closed_intents"], 1)
        with self.store._connect() as conn:
            status = conn.execute(
                "SELECT status FROM file_intents WHERE agent_id='agent:writer'"
            ).fetchone()[0]
        self.assertEqual(status, "closed")

    def test_startup_recovery_closes_abandoned_agent_runtime(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        started = self.store.begin_agent_task(
            alice,
            agent_id="agent:abandoned",
            session_id="abandoned",
            task_text="Implement an interrupted shared change.",
        )
        self.store.update_agent(
            alice,
            agent_id="agent:abandoned",
            session_id="abandoned",
            status="running",
        )
        self.store.declare_intent(
            alice,
            "stale.js",
            agent_id="agent:abandoned",
            intent="write_file",
        )

        recovered = CollaborationStore(
            self.root / "state" / "collaboration.sqlite",
            self.root / "Codes",
            self.root / "state" / "collaboration",
        )
        with recovered._connect() as conn:
            agent_status = conn.execute(
                "SELECT status FROM agents WHERE agent_id='agent:abandoned'"
            ).fetchone()[0]
            intent_status = conn.execute(
                "SELECT status FROM file_intents WHERE agent_id='agent:abandoned'"
            ).fetchone()[0]
            assignment_status = conn.execute(
                "SELECT status FROM blackboard_agent_assignments WHERE item_id=? AND agent_id='agent:abandoned'",  # noqa: E501
                (started["item_id"],),
            ).fetchone()[0]
        self.assertEqual(agent_status, "idle")
        self.assertEqual(intent_status, "closed")
        self.assertEqual(assignment_status, "blocked")

    def test_project_purge_removes_agent_bridge_children_before_blackboard_items(self):
        _, _, alice = self.approve_and_login("Alice", "a" * 40)
        started = self.store.begin_agent_task(
            alice,
            agent_id="agent:purge",
            session_id="purge",
            task_text="Create public evidence before project purge.",
        )
        self.store.record_agent_task_evidence(
            alice,
            agent_id="agent:purge",
            session_id="purge",
            kind="clue",
            summary="This evidence must be removed before its parent item.",
        )
        self.store.quarantine_project(self.project["project_id"], self.project["name"])
        result = self.store.purge_project(self.project["project_id"], force=True)
        self.assertTrue(result["purged"])
        with self.store._connect() as conn:
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM blackboard_agent_assignments WHERE item_id=?",
                    (started["item_id"],
                     )).fetchone()[0],
                0,
            )
            self.assertEqual(
                conn.execute(
                    "SELECT COUNT(*) FROM blackboard_agent_evidence WHERE item_id=?",
                    (started["item_id"],
                     )).fetchone()[0],
                0,
            )

    def test_proxy_lease_expires_at_project_day_boundary(self):
        _, _, alice = self.approve_and_login()
        lease = self.store.grant_lease(
            alice,
            relative="lease.txt",
            agent_ids=["agent-a", "agent-b"],
            expires_at=0,
        )
        self.assertGreater(lease["expires_at"], __import__("time").time())
        self.assertLessEqual(lease["expires_at"] - __import__("time").time(), 24 * 3600)
        self.assertTrue(self.store.validate_lease(
            self.project["project_id"], "lease.txt", ["agent-b", "agent-a"]))


class OperationalTransformTests(unittest.TestCase):
    def test_transform_delete_against_insert(self):
        incoming = [{"retain": 1}, {"delete": 1}, {"retain": 1}]
        applied = [{"retain": 1}, {"insert": "X"}, {"retain": 2}]
        transformed = transform_text_operation(incoming, applied)
        self.assertEqual(apply_text_operation("aXbc", transformed), "aXc")


class TrustedClientIPTests(unittest.TestCase):
    class Handler:
        def __init__(self, peer, forwarded=""):
            self.client_address = (peer, 1234)
            self.headers = {"X-Forwarded-For": forwarded}

    def test_forged_forwarded_for_is_ignored_without_proxy_trust(self):
        handler = self.Handler("192.168.1.50", "127.0.0.1")
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLOUDS_CODER_TRUST_PROXY", None)
            self.assertEqual(cc.trusted_client_ip(handler), "192.168.1.50")

    def test_trusted_proxy_chain_returns_real_lan_client_not_loopback(self):
        handler = self.Handler("127.0.0.1", "192.168.1.50, 127.0.0.1")
        with mock.patch.dict(
            os.environ,
            {"CLOUDS_CODER_TRUST_PROXY": "true",
                "CLOUDS_CODER_TRUSTED_PROXIES": "127.0.0.1/32"},
        ):
            self.assertEqual(cc.trusted_client_ip(handler), "192.168.1.50")


class CollaborationAccessLogTests(unittest.TestCase):
    def make_handler(self, path):
        handler = object.__new__(cc.CollaborationHandler)
        handler.path = path
        handler.client_address = ("192.168.1.20", 45678)
        return handler

    def test_successful_high_frequency_requests_are_silent_by_default(self):
        paths = (
            "/api/ide/v2/terminals/term_123/output?offset=170",
            "/api/ide/v2/sessions/sess_123/agent-state",
            "/api/ide/v2/sessions/sess_123/events",
            "/api/collab/v1/events?after=42",
            "/api/collab/v1/presence",
            "/api/collab/v1/snapshot",
            "/api/collab/v1/agents/sessions/sess_123",
            "/api/collab/v1/documents/src%2Fapp.py/operations",
        )
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLOUDS_CODER_COLLAB_ACCESS_LOG", None)
            with mock.patch("builtins.print") as output:
                for path in paths:
                    self.make_handler(path).log_message(
                        '"%s" %s %s', "GET / HTTP/1.1", "200", "-")
        output.assert_not_called()

    def test_stale_terminal_not_found_poll_is_silent(self):
        handler = self.make_handler(
            "/api/ide/v2/terminals/term_stale/output?offset=170")
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLOUDS_CODER_COLLAB_ACCESS_LOG", None)
            with mock.patch("builtins.print") as output:
                handler.log_message(
                    '"%s" %s %s',
                    "GET /api/ide/v2/terminals/term_stale/output?offset=170 HTTP/1.1",
                    "404",
                    "-",
                )
        output.assert_not_called()

    def test_errors_remain_visible_while_successful_conflict_requests_are_silent(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLOUDS_CODER_COLLAB_ACCESS_LOG", None)
            with mock.patch("builtins.print") as output:
                self.make_handler("/api/ide/v2/terminals/term_123/output").log_message(
                    '"%s" %s %s', "GET /api/ide/v2/terminals/term_123/output HTTP/1.1", "401", "-")  # noqa: E501
                self.make_handler("/api/collab/v1/conflicts/case_123/resolve").log_message(  # noqa: E501
                    '"%s" %s %s', "POST /api/collab/v1/conflicts/case_123/resolve HTTP/1.1", "200", "-")  # noqa: E501
        output.assert_called_once()

    def test_diagnostic_switch_restores_polling_logs(self):
        handler = self.make_handler("/api/ide/v2/sessions/sess_123/agent-state")
        with mock.patch.dict(os.environ, {"CLOUDS_CODER_COLLAB_ACCESS_LOG": "1"}):
            with mock.patch("builtins.print") as output:
                handler.log_message(
                    '"%s" %s %s',
                    "GET /api/ide/v2/sessions/sess_123/agent-state HTTP/1.1",
                    "200",
                    "-")
        output.assert_called_once()


class CollaborationConfigTests(unittest.TestCase):
    def test_collaboration_is_lan_ready_by_default(self):
        config = cc._admin_factory_config()
        self.assertTrue(config["collaboration_enabled"])
        self.assertEqual(config["collab_host"], "0.0.0.0")
        self.assertTrue(config["collab_allow_insecure_http"])

    def test_non_loopback_requires_https_gate(self):
        config = cc._admin_factory_config()
        config.update({
            "collaboration_enabled": True,
            "host": "0.0.0.0",
            "collab_host": "0.0.0.0",
            "collab_allow_insecure_http": False,
        })
        _, errors = cc._admin_coerce_config(config)
        self.assertTrue(any(row["key"] == "collaboration_enabled" for row in errors))
        config["collab_allow_insecure_http"] = True
        _, errors = cc._admin_coerce_config(config)
        self.assertFalse(any(row["key"] == "collaboration_enabled" for row in errors))

    def test_admin_one_click_lan_profile_derives_safe_defaults(self):
        app = object.__new__(cc.AppContext)
        draft = cc._admin_factory_config()
        draft.update({
            "port": 8128,
            "collaboration_enabled": False,
            "collab_host": "127.0.0.1",
            "collab_port": 9999,
            "collab_allow_insecure_http": False,
            "model": "keep-this-model",
        })
        captured = {}
        app.admin_config_payload = lambda: {"draft": dict(draft)}

        def save(values, *, expected_revision=""):
            captured.update(values)
            captured["expected_revision"] = expected_revision
            return {"ok": True, "draft": values}

        app.save_admin_config = save
        result = cc.AppContext.save_lan_collaboration_config(
            app, True, expected_revision="rev-1")
        self.assertTrue(result["ok"])
        self.assertTrue(captured["collaboration_enabled"])
        self.assertEqual(captured["collab_host"], "0.0.0.0")
        self.assertEqual(captured["collab_port"], 8135)
        self.assertTrue(captured["collab_allow_insecure_http"])
        self.assertEqual(captured["model"], "keep-this-model")
        self.assertEqual(captured["expected_revision"], "rev-1")

        captured.clear()
        cc.AppContext.save_lan_collaboration_config(
            app, False, expected_revision="rev-2")
        self.assertFalse(captured["collaboration_enabled"])
        self.assertEqual(captured["model"], "keep-this-model")

    def test_admin_can_compare_and_sync_active_cli_config_to_restart_draft(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config_path = root / "LLM.config.json"
            config_path.write_text("{}", encoding="utf-8")
            app = object.__new__(cc.AppContext)
            app.admin_config_lock = threading.RLock()
            app.admin_config_path = root / "startup_config.json"
            app.admin_restart_error_path = root / "restart_error.json"
            app.admin_initial_config = cc._admin_factory_config()
            app.admin_active_config = dict(app.admin_initial_config)
            app.admin_active_config.update({
                "port": 9128,
                "config": str(config_path),
                "model": "active-cli-model",
            })
            app.telemetry = type("Telemetry", (), {"boot_id": "boot-test"})()
            stale = dict(app.admin_initial_config)
            stale.update({"port": 8128, "config": "", "model": "stale-draft-model"})
            cc._write_json_file(
                app.admin_config_path,
                {"version": 1, "draft": stale,
                    "defaults": app.admin_initial_config, "updated_at": 1},
            )

            before = cc.AppContext.admin_config_payload(app)
            self.assertTrue(before["restart_required"])
            self.assertEqual(before["draft"]["config"], "")
            self.assertEqual(before["active"]["config"], str(config_path))
            self.assertEqual(before["effective_ports"]["agent"], 8128)
            self.assertEqual(before["active_effective_ports"]["agent"], 9128)

            synced = cc.AppContext.sync_admin_config_from_active(
                app, expected_revision=before["revision"]
            )
            after = cc.AppContext.admin_config_payload(app)
            self.assertTrue(synced["ok"])
            self.assertFalse(after["restart_required"])
            self.assertEqual(after["draft"]["config"], str(config_path))
            self.assertEqual(after["draft"]["model"], "active-cli-model")

    def test_admin_conflict_and_active_config_controls_have_complete_routes(self):
        self.assertIn('id="syncActiveConfigBtn"', cc.ADMIN_INDEX_HTML)
        self.assertIn('id="collabConflictList"', cc.ADMIN_INDEX_HTML)
        self.assertIn("'/api/admin/config/sync-active'", cc.ADMIN_JS)
        self.assertIn("api(root+'/conflicts')", cc.ADMIN_JS)
        self.assertIn(
            "+'/conflicts/'+encodeURIComponent(conflict.conflict_id)+'/abort'",
            cc.ADMIN_JS)
        source = Path(cc.__file__).read_text(encoding="utf-8")
        self.assertIn('if path == "/api/admin/config/sync-active":', source)
        self.assertIn('m_collab_conflicts = re.match(', source)
        self.assertIn('m_collab_abort = re.match(', source)

    def test_session_state_keeps_private_state_with_controlled_shared_files_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shared = (root / "Codes" / "collaboration" /
                      str(__import__("uuid").uuid4()) / "workspace").resolve()
            shared.mkdir(parents=True)
            private = root / "private-sessions"
            manager = cc.SessionManager(
                private,
                "collab:test",
                "http://127.0.0.1:11434",
                "test-model",
                root / "skills",
                root / "js_lib",
                cc.CryptoBox(root / "crypto"),
                shared,
                workspace_root=shared,
                collaboration_context={"project_id": "project", "member_id": "member"},
            )
            first = manager.create("one")
            second = manager.create("two")
            self.assertEqual(first.files_root, shared)
            self.assertEqual(second.files_root, shared)
            self.assertTrue(first.state_path.is_relative_to(private))
            self.assertTrue(first.long_output_dir.is_relative_to(first.root))
            self.assertFalse(first.state_path.is_relative_to(shared))

    def test_session_submission_starts_public_task_before_agent_worker(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = cc.SessionManager(
                root / "sessions",
                "collab:project:member",
                "http://127.0.0.1:11434",
                "test-model",
                root / "skills",
                root / "js_lib",
                cc.CryptoBox(root / "crypto"),
                root,
            )
            session = manager.create("bridge")
            calls = []

            class Bridge:
                def begin_task(self, session_id, task_text):
                    calls.append((session_id, task_text))
                    return {
                        "role": "coordinator",
                        "participant_count": 1,
                        "merged": False}

            session.collaboration_write_coordinator = Bridge()
            session._agent_worker = lambda: None
            result = session.submit_user_message("Repair the shared event bridge.")
            self.assertTrue(result["running"])
            self.assertEqual(calls, [(session.id, "Repair the shared event bridge.")])
            for _ in range(4):
                worker = getattr(session, "_persist_scheduler_thread", None)
                if worker is None:
                    break
                worker.join(timeout=2)

    def test_collaboration_run_outcome_uses_structured_public_evidence_only(self):
        class Session:
            blackboard = {"status": "COMPLETED", "completion": {"state": "completed"}}
            cancel_requested = False
            pending_user_question = None
            run_started_at = 100.0
            messages = [{"role": "user", "content": "api_key=private-user-secret"}]
            operations = [{"ts": 101.0,
                           "type": "file_patch",
                           "data": {"path": "src/app.py",
                                    "diff": "password=hunter2"},
                           },
                          {"ts": 102.0,
                           "type": "command",
                           "data": {"command": "pytest -q --token private-command-secret",  # noqa: E501
                                    "exit_code": 0},
                           },
                          ]

        status, summary = cc.AppContext._collaboration_run_outcome(Session())
        self.assertEqual(status, "completed")
        self.assertIn("src/app.py", summary)
        self.assertIn("1 passed", summary)
        self.assertNotIn("private-user-secret", summary)
        self.assertNotIn("hunter2", summary)
        self.assertNotIn("private-command-secret", summary)

    def test_collaboration_runtime_uses_current_ip_user_llm_profiles(self):
        class SourceManager:
            lock = threading.RLock()
            user_model_profiles = {
                "shared-openai": {
                    "id": "shared-openai",
                    "provider": "openai_compat",
                    "label": "LAN API",
                    "model": "shared-model",
                    "base_url": "http://192.168.1.10:9000/v1",
                    "api_key": "server-side-secret",
                }
            }
            user_active_profile_id = "shared-openai"
            read_context_policy = cc.DEFAULT_READ_CONTEXT_POLICY
            tool_memory_policy = cc.DEFAULT_TOOL_MEMORY_POLICY
            auto_task_level_ceiling = cc.DEFAULT_AUTO_TASK_LEVEL_CEILING
            l2_todo_policy = cc.DEFAULT_L2_TODO_POLICY
            single_no_plan_todo_enabled = False
            single_no_plan_todo_prompt = ""
            web_search_enabled = True
            user_language = cc.DEFAULT_UI_LANGUAGE

        app = object.__new__(cc.AppContext)
        app.force_global_llm_config_for_users = False
        captured = {}

        def manager_for_user(user_id):
            captured["user_id"] = user_id
            return SourceManager()

        app.manager_for_user = manager_for_user
        source = cc.AppContext._collaboration_runtime_source(app, "192.168.1.20")
        self.assertEqual(captured["user_id"], cc.user_id_from_ip("192.168.1.20"))
        self.assertEqual(source["source_kind"], "current_ip_user")
        self.assertEqual(source["config"]["profiles"][0]
                         ["base_url"], "http://192.168.1.10:9000/v1")
        self.assertEqual(source["config"]["profiles"][0]
                         ["api_key"], "server-side-secret")

        app.force_global_llm_config_for_users = True
        source = cc.AppContext._collaboration_runtime_source(app, "192.168.1.20")
        self.assertEqual(source["source_kind"], "admin_global")

    def test_private_collaboration_llm_config_persists_and_restores_shared_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manager = cc.SessionManager(
                root / "sessions",
                "collab:project:member",
                "http://127.0.0.1:9",
                "old-model",
                root / "skills",
                root / "js_lib",
                cc.CryptoBox(root / "crypto"),
                root,
                default_llm_config={
                    "provider": "ollama",
                    "ollama_url": "http://127.0.0.1:9",
                    "ollama_model": "old-model",
                },
            )
            session = manager.create("Private model")
            app = cc.AppContext.__new__(cc.AppContext)
            app.manager_for_user = lambda _user_id: manager
            private_config = {
                "provider": "openai_compat",
                "openai_url": "http://127.0.0.1:9/v1",
                "openai_model": "private-model",
                "openai_key": "private-server-secret",
            }
            result = cc.AppContext.ide_apply_llm_config(
                app,
                manager.user_id,
                session.id,
                private_config,
                client_ip="192.168.1.20",
            )
            self.assertTrue(manager.collaboration_llm_independent)
            self.assertEqual(result["source"], "collaboration_private")
            self.assertEqual(result["active_profile"]["model"], "private-model")
            self.assertNotIn("private-server-secret", json.dumps(result))

            reloaded = cc.SessionManager(
                root / "sessions",
                manager.user_id,
                "http://127.0.0.1:9",
                "old-model",
                root / "skills",
                root / "js_lib",
                cc.CryptoBox(root / "crypto"),
                root,
            )
            self.assertTrue(reloaded.collaboration_llm_independent)
            self.assertEqual(reloaded.collaboration_llm_source_kind,
                             "collaboration_private")
            self.assertEqual(reloaded._active_profile()["model"], "private-model")

            shared_config = {
                "provider": "openai_compat",
                "openai_url": "http://127.0.0.1:9/v1",
                "openai_model": "shared-model",
                "openai_key": "shared-server-secret",
            }
            app.manager_for_user = lambda _user_id: reloaded
            app._collaboration_runtime_source = lambda _client_ip: {
                "config": shared_config,
                "revision": app._llm_config_revision(shared_config),
                "source_kind": "current_ip_user",
                "source_user_id": cc.user_id_from_ip("192.168.1.20"),
                "language": cc.DEFAULT_UI_LANGUAGE,
            }
            restored = cc.AppContext.ide_use_shared_llm_config(
                app,
                reloaded.user_id,
                client_ip="192.168.1.20",
                session_id=session.id,
            )
            self.assertFalse(reloaded.collaboration_llm_independent)
            self.assertEqual(reloaded._active_profile()["model"], "shared-model")
            self.assertEqual(restored["source"], "current_ip_user")
            self.assertNotIn("shared-server-secret", json.dumps(restored))

    def test_independent_collaboration_manager_ignores_automatic_source_sync(self):
        principal = cc.CollaborationPrincipal(
            project_id="project",
            member_id="member",
            device_id="device",
            session_digest="digest",
            csrf_token="csrf",
            nickname="Member",
            expires_at=cc.now_ts() + 3600,
        )
        manager = mock.Mock()
        manager.collaboration_llm_independent = True
        app = cc.AppContext.__new__(cc.AppContext)
        app._lock = threading.RLock()
        app._session_mgrs = {"collab:project:member": manager}
        app._collaboration_runtime_source = mock.Mock(return_value={"revision": "new"})
        with mock.patch.object(cc.AppContext, "_sync_collaboration_runtime_source") as sync:  # noqa: E501
            resolved = cc.AppContext.manager_for_collaboration(
                app, principal, client_ip="192.168.1.20"
            )
        self.assertIs(resolved, manager)
        sync.assert_not_called()

    def test_admin_global_config_broadcast_skips_private_collaboration_manager(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app.base_url = "http://127.0.0.1:9"
        app.model = "old-model"
        app._lock = threading.RLock()
        manager = mock.Mock()
        manager.collaboration_llm_independent = True
        manager.sessions = {}
        app._session_mgrs = {"collab:project:member": manager}
        app._sync_global_ollama_defaults = lambda _active: None
        app.web_search_setting_locked = False
        app.user_memory_setting_locked = False
        config = {
            "provider": "openai_compat",
            "openai_url": "http://127.0.0.1:9/v1",
            "openai_model": "admin-global",
            "openai_key": "admin-server-secret",
        }
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(
            cc, "LLM_CONFIG_PATH", Path(temp) / "LLM.config.json"
        ):
            result = cc.AppContext.apply_global_llm_config(app, config, source="test")
        self.assertEqual(result["live_users_updated"], 0)
        manager.reset_to_llm_config.assert_not_called()

    def test_startup_config_reapplies_when_existing_user_revision_matches_but_model_drifted(  # noqa: E501
            self):
        app = cc.AppContext.__new__(cc.AppContext)
        config = {
            "provider": "glm",
            "glm_url": "https://example.invalid/v1",
            "glm_model": "admin-model",
            "glm_key": "server-secret",
        }
        revision = app._llm_config_revision(config)
        app.default_llm_config = config
        app.global_llm_config_revision = revision
        app.global_llm_config_source = "startup-config"
        app.force_global_llm_config_for_users = True
        manager = mock.Mock()
        manager.global_llm_config_revision = revision
        manager.user_model_profiles = {
            "ollama": {"provider": "ollama", "model": "qwen2.5-coder:7b"}
        }
        applied = cc.AppContext._apply_forced_global_llm_config(
            app, manager, "user_192.168.1.6"
        )
        self.assertTrue(applied)
        manager.reset_to_llm_config.assert_called_once_with(
            config, source="startup-config"
        )
        self.assertTrue(manager.force_global_defaults_on_load)

        private = mock.Mock()
        private.collaboration_llm_independent = True
        self.assertFalse(
            cc.AppContext._apply_forced_global_llm_config(
                app, private, "collab:project:member"
            )
        )
        private.reset_to_llm_config.assert_not_called()

    def test_ordinary_ide_llm_config_and_model_selection_update_ip_main_user(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            crypto = cc.CryptoBox(root / "crypto")

            def create_manager(user_id):
                return cc.SessionManager(
                    root / user_id / "sessions",
                    user_id,
                    "http://127.0.0.1:9",
                    "old-model",
                    root / "skills",
                    root / "js_lib",
                    crypto,
                    root,
                    default_llm_config={
                        "provider": "ollama",
                        "ollama_url": "http://127.0.0.1:9",
                        "ollama_model": "old-model",
                    },
                )

            client_ip = "192.168.1.55"
            source_id = cc.user_id_from_ip(client_ip)
            source = create_manager(source_id)
            ide_manager = create_manager("ide_device_remote")
            session = ide_manager.create("Remote IDE")
            managers = {source_id: source, ide_manager.user_id: ide_manager}
            app = cc.AppContext.__new__(cc.AppContext)
            app.force_global_llm_config_for_users = False
            app.manager_for_user = lambda user_id: managers[user_id]
            config = {
                "provider": "openai_compat",
                "openai_url": "http://127.0.0.1:9/v1",
                "openai_model": "shared-from-ide",
                "openai_key": "main-user-server-secret",
            }
            result = cc.AppContext.ide_apply_llm_config(
                app,
                ide_manager.user_id,
                session.id,
                config,
                client_ip=client_ip,
            )
            self.assertEqual(source._active_profile()["model"], "shared-from-ide")
            self.assertEqual(ide_manager._active_profile()["model"], "shared-from-ide")
            self.assertEqual(result["scope"], "main_web_ui_user")
            self.assertNotIn("main-user-server-secret", json.dumps(result))

            selection = f"{source.user_active_profile_id}::selected-in-ide"
            cc.AppContext.ide_set_agent_model(
                app,
                ide_manager.user_id,
                session.id,
                selection,
                client_ip=client_ip,
            )
            self.assertEqual(source._active_profile()["model"], "selected-in-ide")
            self.assertEqual(ide_manager._active_profile()["model"], "selected-in-ide")

            with self.assertRaises(ValueError):
                cc.AppContext.ide_apply_llm_config(
                    app,
                    ide_manager.user_id,
                    session.id,
                    {"unrelated": True},
                    client_ip=client_ip,
                )


class CollaborationWatcherTests(unittest.TestCase):
    def test_watcher_backs_off_and_recovers(self):
        waits = []
        logs = []

        class StopEvent:
            def wait(self, delay):
                waits.append(delay)
                return len(waits) >= 4

        class Store:
            def __init__(self):
                self.scans = 0
                self.reaps = 0

            def scan_external_writes(self):
                self.scans += 1
                if self.scans <= 2:
                    raise sqlite3.OperationalError("storage unavailable")

            def reap_stale_agents(self):
                self.reaps += 1

        app = type("App", (), {})()
        app.collaboration = Store()

        cc.collaboration_file_watcher_loop(
            app,
            StopEvent(),
            normal_interval=1.0,
            max_backoff=30.0,
            log=logs.append,
        )

        self.assertEqual(waits, [1.0, 2.0, 4.0, 1.0])
        self.assertEqual(app.collaboration.scans, 3)
        self.assertEqual(app.collaboration_watcher_health["status"], "healthy")
        self.assertEqual(app.collaboration_watcher_health["consecutive_failures"], 0)
        self.assertEqual(len([line for line in logs if "degraded" in line]), 2)
        self.assertEqual(len([line for line in logs if "recovered" in line]), 1)


class CollaborationHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.store = CollaborationStore(
            root / "state" / "collaboration.sqlite",
            root / "Codes",
            root / "state" / "collaboration",
        )
        self.project = self.store.create_project(
            "HTTP Project", "Http-project-pass-123!")

        class App:
            collaboration = self.store
            collaboration_insecure_http = False

            class Applications:
                @staticmethod
                def list_shared():
                    return [{"id": "shared-app", "name": "Shared App"}]

            applications = Applications()

            @staticmethod
            def web_ui_ide_index_html():
                return cc.IDE_INDEX_HTML

            @staticmethod
            def web_ui_ide_style_css():
                return cc.IDE_CSS

            @staticmethod
            def web_ui_ide_js():
                return cc.IDE_JS

            @staticmethod
            def manager_for_collaboration(_principal, *, client_ip=""):
                return object()

            @staticmethod
            def collaboration_resource_manifest(_user_id):
                return {
                    "llm": {
                        "source": "current_ip_user",
                        "profile_count": 2,
                        "server_side_credentials": True},
                    "skills": {
                        "enabled": True,
                        "count": 1,
                        "read_only": True},
                    "shared_apps": {
                        "enabled": True,
                        "count": 1,
                        "read_only": True},
                    "libraries": {
                        "knowledge": {
                            "enabled": True,
                            "agent_access": True,
                            "stats": {
                                "document_count": 3}},
                        "code": {
                            "enabled": True,
                            "agent_access": True,
                            "stats": {
                                "file_count": 4}},
                    },
                    "api_paths": {
                        "skills": "/api/skills",
                        "shared_apps": "/api/apps/shared"},
                    "services": {
                        "main": {
                            "enabled": True,
                            "port": 8128}},
                }

            @staticmethod
            def skills_catalog():
                return [{"id": "skill-one", "name": "Skill One"}]

            @staticmethod
            def skill_providers_catalog():
                return []

            @staticmethod
            def skill_protocols_catalog():
                return []

            @staticmethod
            def skill_protocol_examples():
                return []

            @staticmethod
            def ide_is_loopback_address(value):
                return cc.AppContext.ide_is_loopback_address(value)

            @staticmethod
            def ide_request_capabilities(account, *, client_ip, direct_loopback):
                return cc.AppContext.ide_request_capabilities(
                    App, account, client_ip=client_ip, direct_loopback=direct_loopback
                )

            @staticmethod
            def ide_config(user_id, client_ip=""):
                return {
                    "ok": True,
                    "app": "clouds-coder-collaboration-ide",
                    "user_id": user_id,
                    "sessions": [],
                    "mounts": [],
                    "collaboration_mode": True,
                }

            @staticmethod
            def ide_monaco_worker_path():
                return None

            @staticmethod
            def rag_js_lib_asset_path(_path):
                return None

        self.server = cc.AgentHTTPServer(
            ("127.0.0.1", 0), cc.CollaborationHandler, App())
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        payload = json.dumps(body).encode("utf-8") if body is not None else None
        request_headers = {"Origin": f"http://127.0.0.1:{self.port}", **(headers or {})}
        if payload is not None:
            request_headers["Content-Type"] = "application/json"
        conn.request(method, path, body=payload, headers=request_headers)
        response = conn.getresponse()
        raw = response.read()
        result = json.loads(raw.decode("utf-8")) if raw else {}
        response_headers = dict(response.getheaders())
        conn.close()
        return response.status, result, response_headers

    def test_database_failure_returns_structured_503(self):
        device_key = "database-failure-device-" + "x" * 32
        status, pending, _ = self.request(
            "POST",
            "/api/collab/v1/admission",
            {
                "project": self.project["name"],
                "password": "Http-project-pass-123!",
                "device_key": device_key,
                "nickname": "Storage Test",
            },
        )
        self.assertEqual(status, 202)
        self.store.approve_device(self.project["project_id"], pending["device_id"])
        status, _, headers = self.request(
            "POST",
            "/api/collab/v1/admission",
            {
                "project": self.project["name"],
                "password": "Http-project-pass-123!",
                "device_key": device_key,
                "nickname": "Storage Test",
            },
        )
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        with mock.patch.object(
            self.store,
            "_connect",
            side_effect=sqlite3.OperationalError("storage unavailable"),
        ):
            status, payload, _ = self.request(
                "GET",
                "/api/collab/v1/status",
                headers={"Cookie": cookie},
            )

        self.assertEqual(status, 503)
        self.assertEqual(payload["code"], "collaboration_store_unavailable")
        self.assertNotIn("storage unavailable", payload["error"])

    def test_health_reports_missing_collaboration_database(self):
        self.store.db_path.unlink()

        status, payload, _ = self.request("GET", "/api/health")

        self.assertEqual(status, 503)
        self.assertFalse(payload["ok"])
        self.assertEqual(
            payload["storage"]["code"],
            "collaboration_store_unavailable",
        )

    def test_cookie_and_csrf_domains_are_independent_and_enforced(self):
        device_key = "http-device-key-" + "x" * 32
        status, pending, _ = self.request(
            "POST",
            "/api/collab/v1/admission",
            {
                "project": self.project["name"],
                "password": "Http-project-pass-123!",
                "device_key": device_key,
                "nickname": "Browser User",
            },
        )
        self.assertEqual(status, 202)
        self.store.approve_device(self.project["project_id"], pending["device_id"])
        status, login, headers = self.request(
            "POST",
            "/api/collab/v1/admission",
            {
                "project": self.project["name"],
                "password": "Http-project-pass-123!",
                "device_key": device_key,
                "nickname": "Browser User",
            },
        )
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        self.assertTrue(cookie.startswith("clouds_collab_session="))
        self.assertNotIn("clouds_ide_session", headers["Set-Cookie"])
        status, _, _ = self.request(
            "POST", "/api/collab/v1/presence", {"cursor": {}}, {"Cookie": cookie}
        )
        self.assertEqual(status, 403)
        status, presence, _ = self.request(
            "POST",
            "/api/collab/v1/presence",
            {"cursor": {}},
            {"Cookie": cookie, "X-CSRF-Token": login["csrf_token"]},
        )
        self.assertEqual(status, 200)
        self.assertTrue(presence["ok"])
        status, me, _ = self.request(
            "GET", "/api/collab/v1/status", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertTrue(me["authenticated"])
        self.assertEqual(me["snapshot"]["project"]["project_id"],
                         self.project["project_id"])

    def test_collaboration_port_serves_the_ide_shell_and_collaboration_identity(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/")
        response = conn.getresponse()
        html = response.read().decode("utf-8")
        conn.close()
        self.assertEqual(response.status, 200)
        self.assertIn('id="ideShell"', html)
        self.assertIn('data-side-view="collaboration"', html)
        self.assertIn('id="collaborationResources"', html)
        self.assertNotIn('id="workspace" class="workspace-shell"', html)

        device_key = "ide-device-key-" + "z" * 32
        status, pending, _ = self.request("POST", "/api/collab/v1/admission", {
            "project": self.project["name"],
            "password": "Http-project-pass-123!",
            "device_key": device_key,
            "nickname": "IDE Member",
        })
        self.assertEqual(status, 202)
        self.store.approve_device(self.project["project_id"], pending["device_id"])
        status, login, headers = self.request("POST", "/api/collab/v1/admission", {
            "project": self.project["name"],
            "password": "Http-project-pass-123!",
            "device_key": device_key,
            "nickname": "IDE Member",
        })
        self.assertEqual(status, 200)
        cookie = headers["Set-Cookie"].split(";", 1)[0]
        status, me, _ = self.request(
            "GET", "/api/ide/v2/auth/me", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertTrue(me["account"]["collaboration_mode"])
        self.assertEqual(me["account"]["project_id"], self.project["project_id"])
        status, config, _ = self.request(
            "GET", "/api/ide/config", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertTrue(config["collaboration_mode"])
        self.assertEqual(config["mounts"], [])

        status, resources, _ = self.request(
            "GET", "/api/collab/v1/resources", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertEqual(resources["llm"]["source"], "current_ip_user")
        self.assertTrue(resources["llm"]["server_side_credentials"])
        self.assertEqual(resources["skills"]["count"], 1)
        self.assertEqual(resources["libraries"]["code"]["stats"]["file_count"], 4)
        self.assertEqual(resources["services"]["main"]["url"], "http://127.0.0.1:8128")
        self.assertNotIn("api_key", json.dumps(resources))

        status, skills, _ = self.request(
            "GET", "/api/skills", headers={"Cookie": cookie})
        self.assertEqual(status, 200)
        self.assertEqual(skills[0]["id"], "skill-one")

        status, denied, _ = self.request(
            "POST",
            "/api/ide/v2/resources/skills",
            {"path": "global-change", "content": "not allowed"},
            {"Cookie": cookie, "X-CSRF-Token": login["csrf_token"]},
        )
        self.assertEqual(status, 403)
        self.assertEqual(denied["code"], "admin_required")

        status, _, _ = self.request(
            "GET", "/api/ide/v2/auth/me", headers={"Cookie": "clouds_ide_session=forged"}  # noqa: E501
        )
        self.assertEqual(status, 401)


if __name__ == "__main__":
    unittest.main()
