import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

import Clouds_Coder as cc


class _StudioApp:
    def __init__(self, root: Path):
        self.workspace = root
        self.skills_root = root / "skills"
        self.skills_root.mkdir()
        self.skills_port = 0
        self.agent_port = 0
        self.ui_style = "neo"
        self.show_upload_list = False
        self.web_ui_dir = root / "webui"
        self.skills_studio = cc.SkillsStudioStore(
            root / "admin" / "skills_studio.sqlite",
            root / "admin" / "skills_studio",
            self.skills_root,
        )

    def manager_for_user(self, user_id):
        class Manager:
            def model_catalog(self, force_probe=False):
                return {}

        return Manager()

    def ide_monaco_worker_path(self):
        return None

    def rag_js_lib_asset_path(self, path):
        return None

    def web_ui_skills_index_html(self):
        return "legacy"

    def web_ui_skills_style_css(self):
        return ""

    def web_ui_skills_js(self):
        return ""

    def web_ui_status(self):
        return {}


class SkillsStudioStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = cc.SkillsStudioStore(
            self.root / "skills_studio.sqlite",
            self.root / "state",
            self.root / "skills",
        )
        self.first = self.store.bootstrap("192.168.1.5")

    def tearDown(self):
        self.temp.cleanup()

    def test_same_ip_creates_distinct_devices_and_private_projects(self):
        second = self.store.bootstrap("192.168.1.5")
        self.assertNotEqual(self.first["device_id"], second["device_id"])
        project = self.store.create_project(
            self.first["device_id"], {"title": "Review Reports"}
        )
        self.assertEqual(self.store.list_projects(second["device_id"]), [])
        with self.assertRaises(cc.SkillsStudioError):
            self.store.get_project(second["device_id"], project["id"])

    def test_revision_guard_path_safety_and_symlink_block(self):
        project = self.store.create_project(
            self.first["device_id"], {"title": "Safe Skill"}
        )
        with self.assertRaisesRegex(cc.SkillsStudioError, "traversal"):
            self.store.write_file(
                self.first["device_id"],
                project["id"],
                "../escape",
                b"x",
                expected_revision=0,
            )
        current = self.store.get_project(self.first["device_id"], project["id"])[
            "revision"
        ]
        self.store.write_file(
            self.first["device_id"],
            project["id"],
            "references/a.md",
            b"a",
            expected_revision=current,
        )
        with self.assertRaises(cc.SkillsStudioError) as caught:
            self.store.write_file(
                self.first["device_id"],
                project["id"],
                "references/b.md",
                b"b",
                expected_revision=current,
            )
        self.assertEqual(caught.exception.code, "revision_conflict")
        project_row = None
        with self.store._connect() as db:
            project_row = self.store._row_project(
                db, project["id"], self.first["device_id"]
            )
            root = Path(project_row["root_path"])
        (root / "link").symlink_to(self.root)
        with self.assertRaises(cc.SkillsStudioError) as caught:
            self.store.write_file(
                self.first["device_id"],
                project["id"],
                "link/escape",
                b"x",
                expected_revision=current + 1,
            )
        self.assertEqual(caught.exception.code, "symlink_blocked")

    def test_frozen_submission_is_immutable_and_publish_is_atomic(self):
        project = self.store.create_project(
            self.first["device_id"], {"title": "Build Reports"}
        )
        submission = self.store.submit(self.first["device_id"], project["id"])
        frozen_before = self.store.submission_snapshot(submission["id"])["snapshot"]
        revision = self.store.get_project(self.first["device_id"], project["id"])[
            "revision"
        ]
        self.store.write_file(
            self.first["device_id"],
            project["id"],
            "references/later.md",
            b"later",
            expected_revision=revision,
        )
        frozen_after = self.store.submission_snapshot(submission["id"])["snapshot"]
        self.assertEqual(frozen_before, frozen_after)
        out = self.store.review_submission(submission["id"], "approve", "ship")
        self.assertEqual(out["status"], "published")
        self.assertTrue((self.root / "skills" / "build-reports" / "SKILL.md").is_file())
        self.store.review_submission(submission["id"], "unpublish")
        self.assertFalse((self.root / "skills" / "build-reports").exists())
        self.store.review_submission(submission["id"], "republish")
        self.assertTrue((self.root / "skills" / "build-reports" / "SKILL.md").is_file())

    def test_script_requires_hard_isolation_result(self):
        project = self.store.create_project(
            self.first["device_id"], {"title": "Run Script"}
        )
        revision = self.store.get_project(self.first["device_id"], project["id"])[
            "revision"
        ]
        self.store.write_file(
            self.first["device_id"],
            project["id"],
            "scripts/run.py",
            b"print('ok')\n",
            expected_revision=revision,
        )
        submission = self.store.submit(self.first["device_id"], project["id"])
        with self.assertRaises(cc.SkillsStudioError) as caught:
            self.store.review_submission(submission["id"], "approve")
        self.assertEqual(caught.exception.code, "isolation_required")

    def test_clouds_coder_sidecar_merges_without_polluting_frontmatter(self):
        skill = self.root / "sidecar-skills" / "demo"
        (skill / "agents").mkdir(parents=True)
        (
            skill /
            "SKILL.md").write_text(
            "---\nname: demo\ndescription: Use this demo skill for testing sidecar metadata safely.\n---\n\n# Demo\n",  # noqa: E501
            encoding="utf-8",
        )
        (skill / "agents" / "clouds-coder.yaml").write_text(
            "triggers:\n  - sidecar trigger\nprotocol: custom\n", encoding="utf-8"
        )
        loaded = cc.SkillStore(self.root / "sidecar-skills")
        demo = next(row for row in loaded.list_metadata() if row.get("name") == "demo")
        self.assertIn("sidecar trigger", demo["triggers"])


class SkillsStudioHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = _StudioApp(Path(self.temp.name))
        self.server = cc.AgentHTTPServer(("127.0.0.1", 0), cc.SkillsHandler, self.app)
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
        data = json.dumps(body).encode() if body is not None else None
        hdrs = dict(headers or {})
        if data is not None:
            hdrs["Content-Type"] = "application/json"
            hdrs["Content-Length"] = str(len(data))
        conn.request(method, path, body=data, headers=hdrs)
        response = conn.getresponse()
        payload = json.loads(response.read().decode())
        cookies = response.getheaders()
        conn.close()
        return response.status, payload, cookies

    def test_bootstrap_cookie_csrf_and_origin_checks(self):
        status, boot, headers = self.request("GET", "/api/skillslab/v2/bootstrap")
        self.assertEqual(status, 200)
        cookie_values = [
            value.split(";", 1)[0]
            for key, value in headers
            if key.lower() == "set-cookie"
        ]
        cookie = "; ".join(cookie_values)
        status, _, _ = self.request(
            "POST",
            "/api/skillslab/v2/projects",
            {"title": "Denied"},
            {"Cookie": cookie},
        )
        self.assertEqual(status, 403)
        common = {"Cookie": cookie, "X-CSRF-Token": boot["csrf_token"]}
        status, _, _ = self.request(
            "POST",
            "/api/skillslab/v2/projects",
            {"title": "Denied"},
            {**common, "Origin": "https://evil.example"},
        )
        self.assertEqual(status, 403)
        status, project, _ = self.request(
            "POST",
            "/api/skillslab/v2/projects",
            {"title": "Allowed"},
            {
                **common,
                "Origin": f"http://127.0.0.1:{self.port}",
                "Host": f"127.0.0.1:{self.port}",
            },
        )
        self.assertEqual(status, 201)
        self.assertEqual(project["slug"], "allowed")


if __name__ == "__main__":
    unittest.main()
