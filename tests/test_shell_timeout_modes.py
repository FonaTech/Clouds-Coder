import tempfile
import time
import unittest
from pathlib import Path

import Clouds_Coder as cc


class ShellTimeoutModeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        sessions = base / "sessions"
        skills = base / "skills"
        sessions.mkdir()
        skills.mkdir()
        self.session = cc.SessionState(
            "shell-test",
            "shell-test",
            sessions,
            "http://127.0.0.1:11434",
            "unused",
            skills,
            cc.CryptoBox(base / "crypto"),
            base,
        )

    def tearDown(self):
        try:
            self.session.bg.stop_all()
        finally:
            self.tmp.cleanup()

    def test_config_aliases_and_admin_schema(self):
        raw = {
            "runtime": {
                "bash_timeout_mode": "idle",
                "bash_async_after": 42,
            }
        }
        self.assertEqual(cc.extract_shell_timeout_mode_setting(raw), "auto")
        self.assertEqual(cc.extract_shell_async_handoff_setting(raw), 42)
        schema = {row["key"]: row for row in cc._admin_config_schema()}
        self.assertEqual(
            schema["shell_timeout_mode"]["choices"], ["fixed", "auto", "async"]
        )
        self.assertEqual(schema["shell_async_handoff_seconds"]["factory_default"], 600)

    def test_fixed_uses_total_elapsed_time(self):
        self.session.shell_timeout_mode = "fixed"
        meta = self.session._run_shell_meta(
            "python3 -u -c 'import time; [print(i, flush=True) or time.sleep(.4) for i in range(5)]'",  # noqa: E501
            self.session.files_root,
            1,
        )
        self.assertEqual(meta["exit_code"], -1)
        self.assertIn("mode=fixed", meta["error"])
        self.assertLess(meta["duration_ms"], 1800)

    def test_auto_resets_timeout_on_output_and_stops_after_silence(self):
        self.session.shell_timeout_mode = "auto"
        active = self.session._run_shell_meta(
            "python3 -u -c 'import time; [print(i, flush=True) or time.sleep(.4) for i in range(5)]'",  # noqa: E501
            self.session.files_root,
            1,
        )
        self.assertEqual(active["exit_code"], 0)
        self.assertEqual(active["error"], "")
        self.session.cancel_requested = False
        idle = self.session._run_shell_meta(
            "python3 -u -c 'import time; print(\"ready\", flush=True); time.sleep(2)'",
            self.session.files_root,
            1,
        )
        self.assertEqual(idle["exit_code"], -1)
        self.assertIn("mode=auto", idle["error"])

    def test_async_handoff_keeps_the_same_process_and_streams_output(self):
        self.session.shell_timeout_mode = "async"
        self.session._shell_async_handoff_seconds = lambda: 1
        marker = self.session.files_root / "launch-count.txt"
        command = (
            'python3 -u -c "import os,time,pathlib; '
            "p=pathlib.Path('launch-count.txt'); "
            "p.write_text((p.read_text() if p.exists() else '')+'x'); "
            '[(print(i, flush=True), time.sleep(.4)) for i in range(7)]"'
        )
        started = time.time()
        meta = self.session._run_shell_meta(command, self.session.files_root, 2)
        self.assertTrue(meta.get("handed_off"))
        self.assertLess(time.time() - started, 2.0)
        task_id = str(meta.get("background_task_id", ""))
        self.assertTrue(task_id.startswith("bg_"))
        first = next(
            row for row in self.session.bg.list_objects() if row["id"] == task_id
        )
        self.assertEqual(first["status"], "running")
        self.assertGreater(first["pid"], 0)
        deadline = time.time() + 5
        final = first
        while time.time() < deadline:
            final = next(
                row for row in self.session.bg.list_objects() if row["id"] == task_id
            )
            if final["status"] != "running":
                break
            time.sleep(0.1)
        self.assertEqual(final["status"], "completed")
        self.assertEqual(final["exit_code"], 0)
        self.assertIn("6", final["output_tail"])
        self.assertTrue(final["full_output_path"])
        self.assertEqual(marker.read_text(encoding="utf-8"), "x")

    def test_shell_failure_guidance_is_event_driven_and_clears_on_exit_zero(self):
        self.assertEqual(self.session._shell_failure_guidance_prompt_block(), "")
        self.assertNotIn(
            "TEMPORARY SHELL RECOVERY GUIDANCE",
            self.session._agent_role_system_prompt("developer"),
        )
        self.assertNotIn(
            "TEMPORARY SHELL RECOVERY GUIDANCE",
            self.session._system_prompt(),
        )

        self.session._set_tool_result_meta(
            exit_code=1,
            shell_exit_code=1,
            error="command failed",
        )
        failed = self.session._build_tool_result_item(
            "bash",
            {"command": "false"},
            "Error: command failed",
        )
        self.assertFalse(failed["ok"])
        guidance = self.session._shell_failure_guidance_prompt_block()
        self.assertIn("TEMPORARY SHELL RECOVERY GUIDANCE", guidance)
        self.assertIn("observed_exit_code=1", guidance)
        self.assertIn("nohup", guidance)
        self.assertIn(
            "TEMPORARY SHELL RECOVERY GUIDANCE",
            self.session._agent_role_system_prompt("developer"),
        )
        self.assertIn(
            "TEMPORARY SHELL RECOVERY GUIDANCE",
            self.session._system_prompt(),
        )
        self.assertNotIn(
            "TEMPORARY SHELL RECOVERY GUIDANCE",
            self.session._helper_system_prompt("helper"),
        )

        self.session._set_tool_result_meta(exit_code=0, shell_exit_code=0)
        succeeded = self.session._build_tool_result_item(
            "bash",
            {"command": "printf ok"},
            "ok",
        )
        self.assertTrue(succeeded["ok"])
        self.assertEqual(self.session._shell_failure_guidance_prompt_block(), "")

    def test_truncated_shell_output_arms_guidance_even_on_exit_zero(self):
        self.session._set_tool_result_meta(
            exit_code=0,
            shell_exit_code=0,
            model_truncated=True,
        )
        result = self.session._build_tool_result_item(
            "bash",
            {"command": "python3 noisy.py"},
            "completed",
        )
        self.assertTrue(result["ok"])
        guidance = self.session._shell_failure_guidance_prompt_block()
        self.assertIn("output truncated", guidance)
        self.assertIn("observed_exit_code=0", guidance)


if __name__ == "__main__":
    unittest.main()
