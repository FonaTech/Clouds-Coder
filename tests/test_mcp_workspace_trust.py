import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Clouds_Coder as cc


class MCPWorkspaceTrustTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.private = self.root / "private"
        self.config_path = self.workspace / "LLM.config.json"
        self.script_path = self.workspace / "mcp_marker_server.py"
        self.script_path.write_text(
            """import json
import sys
from pathlib import Path

Path(sys.argv[1]).write_text('executed\\n', encoding='utf-8')
for line in sys.stdin:
    message = json.loads(line)
    if 'id' not in message:
        continue
    method = message.get('method')
    if method == 'initialize':
        result = {
            'protocolVersion': '2025-06-18',
            'capabilities': {'tools': {}},
            'serverInfo': {'name': 'test', 'version': '1'},
        }
    elif method == 'tools/list':
        result = {'tools': []}
    else:
        result = {}
    print(
        json.dumps({'jsonrpc': '2.0', 'id': message['id'], 'result': result}),
        flush=True,
    )
""",
            encoding="utf-8",
        )
        self.manager = None

    def tearDown(self):
        if self.manager is not None:
            self.manager.shutdown()
        self.temp.cleanup()

    def write_config(self, marker_name, **extra):
        payload = {
            "provider": "ollama",
            "ollama_url": "http://127.0.0.1:9",
            "mcpServers": {
                "marker": {
                    "command": sys.executable,
                    "args": [str(self.script_path), str(self.workspace / marker_name)],
                    "cwd": str(self.workspace),
                    "env": {"MCP_TEST_MODE": "1"},
                }
            },
        }
        payload.update(extra)
        self.config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

    def make_manager(self, config):
        trust = cc.MCPWorkspaceTrustStore(self.private / "mcp_trust.json")
        self.manager = cc.MCPManager(
            cc.mcp_extract_server_configs(config),
            config_path=self.config_path,
            workspace=self.workspace,
            trust_store=trust,
        )
        self.manager.note_config_loaded()
        return self.manager

    def test_default_trust_store_never_uses_workspace_controlled_path(self):
        with patch.dict(
            os.environ, {"CLOUDS_CODER_PRIVATE_STATE_DIR": str(self.workspace)}
        ):
            path = cc.mcp_default_trust_store_path(self.workspace)

        self.assertFalse(
            path.resolve(strict=False).is_relative_to(self.workspace.resolve())
        )

    def test_workspace_mcp_is_inert_until_exact_command_is_approved(self):
        config = self.write_config("marker-a")
        manager = self.make_manager(config)

        manager.start_async()
        manager.ensure_connected(wait=True, timeout=3)

        self.assertFalse((self.workspace / "marker-a").exists())
        status = manager.status()[0]
        self.assertEqual(status["state"], "approval_required")
        self.assertFalse(status["alive"])
        preview = manager.approval_requests()[0]
        self.assertFalse(preview["approved"])
        self.assertEqual(
            preview["resolved_command"], str(Path(sys.executable).resolve())
        )
        self.assertEqual(preview["env_keys"], ["MCP_TEST_MODE"])
        self.assertEqual(
            preview["referenced_files"][0]["path"], str(self.script_path.resolve())
        )

        result = manager.approve_server(
            "marker",
            expected_config_digest=preview["config_digest"],
            expected_fingerprint=preview["fingerprint"],
        )

        self.assertTrue(result["ok"])
        self.assertTrue((self.workspace / "marker-a").exists())
        self.assertTrue(manager.approval_requests()[0]["approved"])
        self.assertTrue((self.private / "mcp_trust.json").exists())
        self.assertFalse((self.workspace / "mcp_trust.json").exists())

    def test_issue_36_inline_marker_command_never_spawns_without_approval(self):
        marker = self.workspace / "clouds-coder-poc-marker"
        config = {
            "provider": "ollama",
            "mcpServers": {
                "marker": {
                    "command": sys.executable,
                    "args": [
                        "-c",
                        (
                            "from pathlib import Path; "
                            f"Path({str(marker)!r}).write_text('executed\\n')"
                        ),
                    ],
                }
            },
        }
        self.config_path.write_text(json.dumps(config), encoding="utf-8")
        manager = self.make_manager(config)

        manager.start_async()
        manager.ensure_connected(wait=True, timeout=3)

        self.assertFalse(marker.exists())
        self.assertEqual(manager.status()[0]["state"], "approval_required")

    def test_hot_reload_requires_new_approval_when_command_content_changes(self):
        config_a = self.write_config("marker-a")
        manager = self.make_manager(config_a)
        preview_a = manager.approval_requests()[0]
        self.assertTrue(
            manager.approve_server(
                "marker",
                expected_config_digest=preview_a["config_digest"],
                expected_fingerprint=preview_a["fingerprint"],
            )["ok"]
        )
        self.assertTrue((self.workspace / "marker-a").exists())

        config_b = self.write_config("marker-b")
        diff = manager.reload_from_config(config_b)

        self.assertFalse((self.workspace / "marker-b").exists())
        self.assertEqual(diff["approval_required"], ["marker"])
        preview_b = manager.approval_requests()[0]
        self.assertFalse(preview_b["approved"])
        self.assertIn("stale", preview_b["reason"])

        stale = manager.approve_server(
            "marker",
            expected_config_digest=preview_a["config_digest"],
            expected_fingerprint=preview_a["fingerprint"],
        )
        self.assertFalse(stale["ok"])
        self.assertFalse((self.workspace / "marker-b").exists())

        approved = manager.approve_server(
            "marker",
            expected_config_digest=preview_b["config_digest"],
            expected_fingerprint=preview_b["fingerprint"],
        )
        self.assertTrue(approved["ok"])
        self.assertTrue((self.workspace / "marker-b").exists())

    def test_full_config_revision_change_invalidates_running_server(self):
        config = self.write_config("config-marker")
        manager = self.make_manager(config)
        preview = manager.approval_requests()[0]
        self.assertTrue(
            manager.approve_server(
                "marker",
                expected_config_digest=preview["config_digest"],
                expected_fingerprint=preview["fingerprint"],
            )["ok"]
        )
        marker = self.workspace / "config-marker"
        self.assertTrue(marker.exists())
        marker.unlink()

        changed = self.write_config(
            "config-marker", unrelated_provider_setting="changed"
        )
        diff = manager.reload_from_config(changed)

        self.assertFalse(marker.exists())
        self.assertEqual(diff["approval_required"], ["marker"])
        pending = manager.approval_requests()[0]
        self.assertFalse(pending["approved"])
        self.assertIn("config content changed", pending["reason"])

    def test_crash_restart_revalidates_referenced_script_identity(self):
        config = self.write_config("restart-marker")
        manager = self.make_manager(config)
        preview = manager.approval_requests()[0]
        self.assertTrue(
            manager.approve_server(
                "marker",
                expected_config_digest=preview["config_digest"],
                expected_fingerprint=preview["fingerprint"],
            )["ok"]
        )
        marker = self.workspace / "restart-marker"
        self.assertTrue(marker.exists())
        marker.unlink()

        self.script_path.write_text(
            self.script_path.read_text(encoding="utf-8")
            + "\n# changed after approval\n",
            encoding="utf-8",
        )
        restarted = manager.restart_server("marker")

        self.assertFalse(restarted)
        self.assertFalse(marker.exists())
        self.assertEqual(manager.status()[0]["state"], "approval_required")
        self.assertIn("referenced file changed", manager.status()[0]["error"])

    def test_revocation_stops_server_and_blocks_restart(self):
        config = self.write_config("revoke-marker")
        manager = self.make_manager(config)
        preview = manager.approval_requests()[0]
        self.assertTrue(
            manager.approve_server(
                "marker",
                expected_config_digest=preview["config_digest"],
                expected_fingerprint=preview["fingerprint"],
            )["ok"]
        )

        result = manager.revoke_server_approval("marker")

        self.assertTrue(result["ok"])
        self.assertTrue(result["revoked"])
        self.assertFalse(result["approval"]["approved"])
        self.assertEqual(manager.status()[0]["state"], "approval_required")


if __name__ == "__main__":
    unittest.main()
