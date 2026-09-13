import json
import tempfile
import time
import unittest
from pathlib import Path

import Clouds_Coder as cc
from liquid_kernel import (
    LiquidKernelControlPlane,
    LiquidKernelError,
    default_evolution_config,
)


def wait_for_run(plane: LiquidKernelControlPlane, run_id: str, timeout: float = 8.0) -> dict:
    deadline = time.monotonic() + timeout
    active = {"queued", "collecting", "assessing", "proposal_ready", "validating_patch", "benchmarking"}
    detail = plane.registry.run_detail(run_id)
    while (
        (detail["status"] in active or bool(getattr(plane, "active_run_id", "")))
        and time.monotonic() < deadline
    ):
        time.sleep(0.02)
        detail = plane.registry.run_detail(run_id)
    return detail


def improving_model(system: str, prompt: str, profile: str, max_tokens: int) -> dict:
    return {
        "decision": "change",
        "reason": "Preserve tool descriptors without sharing their outer dictionaries.",
        "changelog": "Copy tool descriptor dictionaries before returning them.",
        "case_families": ["tool selection", "safe mutation boundaries"],
        "patch": {
            "files": [
                {
                    "path": "tool_policy.py",
                    "operation": "replace",
                    "old": "return list(tools or [])",
                    "new": "return [dict(tool) for tool in (tools or [])]",
                }
            ]
        },
    }


def improving_judge(payload: dict, profile: str, max_tokens: int) -> dict:
    return {"incumbent": 50, "candidate": 85, "rationale": "Candidate is equally correct and safer."}


class LiquidKernelConfigurationTests(unittest.TestCase):
    def test_default_is_off_with_full_scope_and_two_history_versions(self):
        config = default_evolution_config()
        self.assertEqual(config["mode"], "Off")
        self.assertEqual(config["schedule"], "off")
        self.assertEqual(config["history_access"], "full")
        self.assertEqual(config["history_version_depth"], 2)
        self.assertEqual(config["user_scope"], ["*"])
        self.assertEqual(config["session_scope"], ["*"])

    def test_switching_mode_applies_its_strength_preset(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            config = plane.apply_startup_config("Tuning", "")["config"]
            self.assertEqual(config["schedule"], "weekly")
            self.assertEqual(config["budget"]["candidate_limit"], 1)
            self.assertEqual(config["budget"]["max_changed_lines"], 400)
            config = plane.apply_startup_config("Aggressive", "hourly")["config"]
            self.assertEqual(config["schedule"], "hourly")
            self.assertEqual(config["mutable_surface"], "full_agent_core")
            self.assertEqual(config["budget"]["max_files"], 30)

    def test_off_mode_forbids_manual_and_scheduled_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            for trigger in ("manual", "schedule", "metric"):
                with self.assertRaises(LiquidKernelError) as caught:
                    plane.trigger(trigger)
                self.assertEqual(caught.exception.code, "evolution_disabled")

    def test_startup_schema_and_admin_wiring_are_exposed(self):
        schema = {row["key"]: row for row in cc._admin_config_schema()}
        self.assertEqual(schema["liquid_kernel_mode"]["choices"], ["Off", "Tuning", "Thinking", "Aggressive"])
        self.assertEqual(schema["evolution_schedule"]["factory_default"], "off")
        self.assertEqual(schema["liquid_kernel_startup_policy"]["choices"], ["inherit", "inject"])
        self.assertEqual(schema["liquid_kernel_startup_policy"]["factory_default"], "inherit")
        self.assertIn("--liquid-kernel-mode", schema["liquid_kernel_mode"]["flag"])
        self.assertIn("--liquid-kernel-startup-policy", schema["liquid_kernel_startup_policy"]["flag"])
        self.assertIn("/api/admin/evolution/emergency-off", cc.ADMIN_JS)
        self.assertIn("history=current +", cc.ADMIN_JS)

    def test_missing_liquid_kernel_package_is_restored_from_clouds_coder(self):
        with tempfile.TemporaryDirectory() as temp:
            package_root = Path(temp) / "liquid_kernel"
            status = cc._ensure_embedded_liquid_kernel_package(package_root)
            self.assertTrue(status["ready"])
            self.assertTrue(status["restored"])
            self.assertEqual(status["source"], "embedded")
            self.assertTrue((package_root / "__init__.py").is_file())
            self.assertTrue((package_root / "control.py").is_file())
            self.assertIn("LiquidKernelControlPlane", (package_root / "control.py").read_text(encoding="utf-8"))

    def test_missing_runtime_history_is_initialized_and_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            runtime_root = Path(temp) / "liquid_kernel"
            status = cc.prepare_liquid_kernel_runtime(runtime_root)
            self.assertFalse(status["history_present"])
            self.assertEqual(status["history_action"], "initialized")
            self.assertEqual(status["requested_policy"], "inherit")
            self.assertTrue((runtime_root.parent / cc.LIQUID_KERNEL_BOOTSTRAP_STATE_FILENAME).is_file())


class LiquidKernelArtifactTests(unittest.TestCase):
    def test_baseline_is_a_signed_multi_file_agent_core(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            version = plane.registry.active_version()
            self.assertEqual(
                set(plane.registry.sources(version)),
                {"kernel.py", "tool_policy.py", "prompt_policy.py", "harness.py"},
            )
            self.assertEqual(plane.runtime.load(version).describe()["contract_version"], 1)

    def test_tampering_invalidates_the_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            artifact = plane.registry.artifact(plane.registry.active_version())
            (artifact.path / "tool_policy.py").write_text("def filter_tools(*args, **kwargs): return []\n", encoding="utf-8")
            with self.assertRaises(LiquidKernelError) as caught:
                plane.registry.artifact(artifact.version)
            self.assertEqual(caught.exception.code, "artifact_hash_invalid")

    def test_controlled_modes_cannot_modify_harness_but_aggressive_can(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            sources = plane.registry.sources(plane.registry.active_version())
            proposal = {
                "patch": {
                    "files": [
                        {
                            "path": "harness.py",
                            "operation": "replace",
                            "old": "return {}",
                            "new": "return {\"system_suffix\": \"Prefer verification.\"}",
                        }
                    ]
                }
            }
            tuning = plane.apply_startup_config("Tuning", "off")["config"]
            with self.assertRaises(LiquidKernelError) as caught:
                plane.validator.apply(sources, proposal, tuning)
            self.assertEqual(caught.exception.code, "mutable_surface_violation")
            aggressive = plane.apply_startup_config("Aggressive", "off")["config"]
            candidate, metadata = plane.validator.apply(sources, proposal, aggressive)
            self.assertIn("Prefer verification", candidate["harness.py"])
            self.assertEqual(metadata["paths"], ["harness.py"])

    def test_external_import_and_dunder_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            sources = plane.registry.sources(plane.registry.active_version())
            config = plane.apply_startup_config("Tuning", "off")["config"]
            import_proposal = {
                "patch": {"files": [{"path": "tool_policy.py", "operation": "replace_file", "content": "from subprocess import run\n\ndef filter_tools(tools, *, role='', context=None):\n    return list(tools or [])\n"}]}
            }
            with self.assertRaises(LiquidKernelError) as caught:
                plane.validator.apply(sources, import_proposal, config)
            self.assertEqual(caught.exception.code, "forbidden_import")
            dunder_proposal = {
                "patch": {"files": [{"path": "tool_policy.py", "operation": "replace_file", "content": "def filter_tools(tools, *, role='', context=None):\n    return tools.__class__(tools)\n"}]}
            }
            with self.assertRaises(LiquidKernelError) as caught:
                plane.validator.apply(sources, dunder_proposal, config)
            self.assertEqual(caught.exception.code, "forbidden_attribute")


class LiquidKernelEvolutionTests(unittest.TestCase):
    def test_new_sessions_follow_canary_while_existing_sessions_remain_pinned(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            plane = LiquidKernelControlPlane(root / "control")
            incumbent = plane.registry.active_version()
            files = plane.registry.sources(incumbent)
            files["tool_policy.py"] = files["tool_policy.py"].replace(
                "return list(tools or [])", "return [dict(tool) for tool in (tools or [])]"
            )
            candidate = plane.registry.register_candidate(
                "pin-test", incumbent, files, mode="Tuning", changelog="Candidate", scores={}
            )
            plane.registry.begin_canary(candidate, 100)
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
                kernel_registry=plane.registry,
                kernel_runtime=plane.runtime,
            )
            canary_session = manager.create("Canary")
            plane.registry.abort_canary(reason="test")
            stable_session = manager.create("Stable")
            self.assertEqual(canary_session.kernel_version, candidate)
            self.assertEqual(stable_session.kernel_version, incumbent)
            self.assertEqual(manager.get(canary_session.id).kernel_version, candidate)
            index = crypto.read_json(manager.session_index_path, {})
            self.assertEqual(index["sessions"][canary_session.id]["kernel_version"], candidate)

    def test_injected_embedded_kernel_preserves_previous_versions_for_pinned_sessions(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            incumbent = plane.registry.active_version()
            files = plane.registry.sources(incumbent)
            files["prompt_policy.py"] = files["prompt_policy.py"].replace(
                "return str(prompt or \"\")", "return str(prompt or \"\").rstrip()"
            )
            evolved = plane.registry.register_candidate(
                "pre-inject", incumbent, files, mode="Thinking", changelog="Existing history", scores={}
            )
            plane.registry.begin_canary(evolved, 100)
            plane.registry.promote(evolved)
            injected = plane.inject_embedded_kernel()
            self.assertTrue(injected["injected"])
            self.assertEqual(injected["previous_version"], evolved)
            self.assertNotEqual(injected["version"], evolved)
            self.assertEqual(plane.registry.active_version(), injected["version"])
            self.assertEqual(plane.registry.artifact(evolved).version, evolved)
            self.assertEqual(plane.registry.artifact(incumbent).version, incumbent)
            self.assertEqual(plane.registry.version_detail(injected["version"])["manifest"]["mode"], "embedded")

    def test_tuning_benchmarks_and_enters_canary_automatically(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=improving_model, judge_callback=improving_judge)
            plane.apply_startup_config("Tuning", "off")
            run = plane.trigger("manual")
            detail = wait_for_run(plane, run["run_id"])
            self.assertEqual(detail["status"], "canary")
            self.assertTrue(detail["candidate_version"])
            self.assertEqual(plane.registry.active_state()["canary"]["version"], detail["candidate_version"])
            self.assertEqual(detail["result"]["patch"]["paths"], ["tool_policy.py"])
            self.assertGreater(detail["result"]["candidate"]["mixed"], detail["result"]["incumbent"]["mixed"])

    def test_thinking_requires_approval_before_canary(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=improving_model, judge_callback=improving_judge)
            plane.apply_startup_config("Thinking", "off")
            run = plane.trigger("manual")
            detail = wait_for_run(plane, run["run_id"])
            self.assertEqual(detail["status"], "awaiting_approval")
            self.assertIsNone(plane.registry.active_state()["canary"])
            approved = plane.approve(run["run_id"])
            self.assertEqual(approved["state"]["canary"]["percent"], 5)

    def test_one_generator_failure_does_not_discard_a_later_candidate(self):
        calls = 0

        def flaky_model(system: str, prompt: str, profile: str, max_tokens: int) -> dict:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise LiquidKernelError("provider_bad_request", "first candidate failed upstream")
            return improving_model(system, prompt, profile, max_tokens)

        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=flaky_model, judge_callback=improving_judge)
            plane.apply_startup_config("Thinking", "off")
            detail = wait_for_run(plane, plane.trigger("manual")["run_id"])
            self.assertEqual(detail["status"], "awaiting_approval")
            self.assertEqual(detail["result"]["candidate_index"], 2)
            self.assertEqual(detail["result"]["evaluations"][0]["code"], "provider_bad_request")

    def test_all_candidates_share_the_same_bounded_designed_case_set(self):
        calls = 0
        judged_cases = []

        def case_designing_model(system: str, prompt: str, profile: str, max_tokens: int) -> dict:
            nonlocal calls
            calls += 1
            proposal = improving_model(system, prompt, profile, max_tokens)
            proposal["benchmark_cases"] = [{
                "id": f"designed-{calls}",
                "role": "reviewer",
                "intent": f"exercise recovery path {calls}",
                "constraints": ["preserve tool ordering", "return contract-compatible types"],
                "expected": "complete safely without mutating the input tool list",
            }]
            return proposal

        def recording_judge(payload: dict, profile: str, max_tokens: int) -> dict:
            judged_cases.append(payload["cases"])
            return improving_judge(payload, profile, max_tokens)

        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=case_designing_model, judge_callback=recording_judge)
            plane.apply_startup_config("Thinking", "off")
            detail = wait_for_run(plane, plane.trigger("manual")["run_id"])
            self.assertEqual(detail["status"], "awaiting_approval")
            self.assertEqual(len(judged_cases), 2)
            self.assertEqual(judged_cases[0], judged_cases[1])
            self.assertLessEqual(len(judged_cases[0]), 72)
            self.assertTrue({"designed-1", "designed-2"}.issubset({case["id"] for case in judged_cases[0]}))
            self.assertIsInstance(json.dumps(detail["result"]), str)

    def test_canary_advances_5_25_100_then_promotes(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            incumbent = plane.registry.active_version()
            files = plane.registry.sources(incumbent)
            files["tool_policy.py"] = files["tool_policy.py"].replace(
                "return list(tools or [])", "return [dict(tool) for tool in (tools or [])]"
            )
            candidate = plane.registry.register_candidate(
                "manual-test", incumbent, files, mode="Tuning", changelog="Candidate", scores={"hard": 100, "soft": 80, "mixed": 86}
            )
            plane.registry.begin_canary(candidate, 5)
            policy = {
                "stages": [5, 25, 100],
                "minimum_completed": [1, 1, 1],
                "minimum_hours": [0, 0, 0],
                "success_drop_limit": 0.25,
                "error_increase_limit": 0.25,
                "p95_latency_increase_limit": 1.0,
            }
            plane.registry.observe_session_result(candidate, success=True, duration_seconds=1, canary_policy=policy)
            first = plane.registry.observe_session_result(incumbent, success=True, duration_seconds=1, canary_policy=policy)
            self.assertEqual(first["percent"], 25)
            second = plane.registry.observe_session_result(candidate, success=True, duration_seconds=1, canary_policy=policy)
            self.assertEqual(second["percent"], 100)
            third = plane.registry.observe_session_result(candidate, success=True, duration_seconds=1, canary_policy=policy)
            self.assertEqual(third["action"], "promoted")
            self.assertEqual(plane.registry.active_version(), candidate)

    def test_emergency_off_aborts_canary_and_preserves_incumbent(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), model_callback=improving_model, judge_callback=improving_judge)
            incumbent = plane.registry.active_version()
            plane.apply_startup_config("Tuning", "off")
            detail = wait_for_run(plane, plane.trigger("manual")["run_id"])
            candidate = detail["candidate_version"]
            stopped = plane.emergency_off()
            self.assertEqual(stopped["config"]["mode"], "Off")
            self.assertEqual(plane.registry.active_version(), incumbent)
            self.assertIsNone(plane.registry.active_state()["canary"])
            self.assertEqual(plane.registry.version_detail(candidate)["status"], "rolled_back")

    def test_promoted_version_notice_is_per_device(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            incumbent = plane.registry.active_version()
            files = plane.registry.sources(incumbent)
            files["prompt_policy.py"] = files["prompt_policy.py"].replace(
                "return str(prompt or \"\")", "return str(prompt or \"\").rstrip()"
            )
            candidate = plane.registry.register_candidate(
                "notice-test", incumbent, files, mode="Thinking", changelog="Trim prompt tails.", scores={"hard": 100, "soft": 80, "mixed": 86}
            )
            plane.registry.begin_canary(candidate, 100)
            plane.registry.promote(candidate)
            notice = plane.registry.notice("user-a", "device-a", "webui")
            self.assertEqual(notice["version"], candidate)
            self.assertIn("Trim prompt", notice["changelog"])
            plane.registry.acknowledge_notice("user-a", "device-a", "webui", candidate)
            self.assertIsNone(plane.registry.notice("user-a", "device-a", "webui"))
            self.assertIsNotNone(plane.registry.notice("user-a", "device-b", "webui"))


class LiquidKernelHistoryTests(unittest.TestCase):
    def test_lineage_uses_current_and_exactly_two_parent_versions_by_default(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            parent = plane.registry.active_version()
            chain = [parent]
            for index in range(3):
                files = plane.registry.sources(parent)
                files["prompt_policy.py"] = files["prompt_policy.py"] + f"\nREVISION_{index} = {index}\n"
                parent = plane.registry.register_candidate(
                    f"chain-{index}", parent, files, mode="Thinking", changelog=f"Revision {index}", scores={}
                )
                chain.append(parent)
            self.assertEqual(plane.registry.lineage_versions(chain[-1], 2), [chain[-1], chain[-2], chain[-3]])

    def test_experience_is_separated_by_kernel_version_with_full_default_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            app = cc.AppContext.__new__(cc.AppContext)
            app.codes_root = root / "Codes"
            app.codes_root.mkdir(parents=True)
            app.crypto = cc.CryptoBox(app.codes_root)
            for index, version in enumerate(("kernel-v3", "kernel-v2", "kernel-v1")):
                state_path = app.codes_root / "user-a" / "sessions" / f"session-{index}" / "state.json"
                app.crypto.write_json(
                    state_path,
                    {
                        "title": f"Session {index}",
                        "kernel_version": version,
                        "updated_at": time.time() - index,
                        "messages": [
                            {"role": "user", "content": f"question {index}"},
                            {"role": "assistant", "content": f"answer {index}"},
                        ],
                    },
                )
            config = default_evolution_config()
            config["budget"]["max_tokens"] = 1000
            result = cc.AppContext._liquid_kernel_experience(
                app,
                config,
                "kernel-v3",
                ["kernel-v3", "kernel-v2", "kernel-v1"],
            )
            self.assertTrue(result["full_history_scope"])
            self.assertEqual(result["history_access"], "full")
            self.assertEqual(set(result["history_by_version"]), {"kernel-v3", "kernel-v2", "kernel-v1"})
            self.assertEqual(result["history_by_version"]["kernel-v2"]["record_count"], 1)
            self.assertEqual(result["history_by_version"]["kernel-v1"]["message_count"], 2)


if __name__ == "__main__":
    unittest.main()
