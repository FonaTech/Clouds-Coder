"""Deployment decisions require completed paired evidence, with reversible approval."""

import json
import tempfile
import unittest
from pathlib import Path

from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config
from liquid_kernel.agentic import compare_agentic_flows
from liquid_kernel.control import LiquidKernelError
from test_agentic_evolution import TaskModel, experiences, judge, wait


class PairDeploymentPolicyTests(unittest.TestCase):
    def plane(self, policy="manual", model=None, reviewer=None):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        plane = LiquidKernelControlPlane(
            Path(temp.name),
            model_callback=model or TaskModel(),
            judge_callback=reviewer or judge,
            experience_provider=lambda *_: experiences(2),
        )
        cfg = plane.apply_startup_config("Thinking", "off")["config"]
        plane.save_config(
            {
                "deployment_policy": policy,
                "budget": {**cfg["budget"], "candidate_limit": 1},
            },
            cfg["revision"],
        )
        return plane

    def test_policy_is_independent_of_edit_strength(self):
        for mode in ("Tuning", "Thinking", "Aggressive", "Off"):
            automatic = normalize_evolution_config(
                {"mode": mode, "deployment_policy": "automatic"}
            )
            manual = normalize_evolution_config(
                {"mode": mode, "deployment_policy": "manual"}
            )
            self.assertEqual(automatic["auto_promote"], mode != "Off")
            self.assertFalse(manual["auto_promote"])
            self.assertEqual(automatic["mutable_surface"], manual["mutable_surface"])

    def test_automatic_candidate_has_complete_better_primary_and_repeat_scores(self):
        plane = self.plane("automatic")
        incumbent = plane.registry.active_version()
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "canary", detail)
        result = detail["result"]
        self.assertGreater(result["candidate"]["mixed"], result["incumbent"]["mixed"])
        self.assertTrue(result["flow_comparison"]["complete"])
        self.assertTrue(result["confirmation"]["passed"])
        self.assertGreater(
            result["confirmation"]["candidate"]["mixed"],
            result["confirmation"]["incumbent"]["mixed"],
        )
        self.assertEqual(plane.registry.active_version(), incumbent)
        self.assertEqual(plane.registry.active_state()["canary"]["percent"], 5)
        plane.reject(detail["run_id"], "End isolated deployment test")
        self.assertIsNone(plane.registry.active_state()["canary"])
        self.assertEqual(plane.registry.active_version(), incumbent)

    def test_manual_approval_and_historical_rollback(self):
        plane = self.plane()
        incumbent = plane.registry.active_version()
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "awaiting_approval", detail)
        self.assertIsNone(plane.registry.active_state()["canary"])
        approved = plane.approve(detail["run_id"])
        self.assertEqual(
            approved["state"]["canary"]["version"], detail["candidate_version"]
        )
        plane.registry.rollback(incumbent, reason="Isolated historical rollback")
        self.assertIsNone(plane.registry.active_state()["canary"])
        self.assertEqual(plane.registry.active_version(), incumbent)

    def test_no_change_runs_distinct_experiment_with_actual_scores_and_no_deployment(self):
        plane = self.plane("automatic", model=TaskModel(reject=True))
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "rejected", detail)
        score = detail["score_summary"]
        self.assertEqual(score["incumbent"]["mixed"], score["candidate"]["mixed"])
        self.assertNotIn("same_version", score["candidate"])
        self.assertTrue(detail["candidate_version"])
        self.assertTrue(score["candidate"]["task_execution_measured"])
        self.assertIsNone(plane.registry.active_state()["canary"])

    def test_manual_approval_after_baseline_switch_requires_new_comparison(self):
        plane = self.plane()
        detail = wait(plane, plane.trigger()["run_id"])
        original = plane.registry.active_version()
        files = plane.registry.sources(original)
        files["kernel.py"] += "\n# Another historical version\n"
        other = plane.registry.register_candidate(
            "external",
            original,
            files,
            mode="Thinking",
            changelog="Other version",
            scores={},
        )
        plane.registry.begin_canary(other, 100)
        plane.registry.promote(other)
        with self.assertRaises(LiquidKernelError) as caught:
            plane.approve(detail["run_id"])
        self.assertEqual(caught.exception.code, "baseline_changed")
        self.assertIsNone(plane.registry.active_state()["canary"])

    def test_baseline_switch_during_confirmation_blocks_automatic_deployment(self):
        count = 0

        def reviewer(payload, *args):
            nonlocal count
            count += 1
            if count == 3:
                previous = plane.registry.active_version()
                files = plane.registry.sources(previous)
                files["kernel.py"] += "\n# Concurrent approved historical version\n"
                other = plane.registry.register_candidate(
                    "external",
                    previous,
                    files,
                    mode="Thinking",
                    changelog="Concurrent rollback target",
                    scores={},
                )
                plane.registry.begin_canary(other, 100)
                plane.registry.promote(other)
            return judge(payload, *args)

        plane = self.plane("automatic", reviewer=reviewer)
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "failed", detail)
        self.assertEqual(detail["result"]["code"], "baseline_changed")
        self.assertTrue(detail["score_summary"]["candidate"]["task_execution_measured"])
        self.assertIsNone(plane.registry.active_state()["canary"])

    def test_review_failure_preserves_measured_scores(self):
        for failing_call in (1, 2):
            with self.subTest(failing_call=failing_call):
                calls = 0

                def reviewer(payload, *args):
                    nonlocal calls
                    calls += 1
                    if calls == failing_call:
                        raise LiquidKernelError(
                            "invalid_judge_output", "No complete review"
                        )
                    return judge(payload, *args)

                plane = self.plane(reviewer=reviewer)
                detail = wait(plane, plane.trigger()["run_id"])
                self.assertEqual(detail["status"], "failed", detail)
                self.assertIsNotNone(detail["score_summary"]["incumbent"]["hard"])
                if failing_call == 2:
                    self.assertIsNotNone(detail["score_summary"]["candidate"]["hard"])
                    self.assertIsNone(detail["score_summary"]["candidate"].get("mixed"))
                self.assertIsNone(plane.registry.active_state()["canary"])

    def test_incomplete_or_equal_pair_cannot_be_eligible(self):
        row = {
            "task_id": "one",
            "task_fingerprint": "frozen",
            "split": "holdout",
            "score": 100,
            "success": True,
            "checks": [],
            "flow_contracts": ["a"],
            "rounds": 5,
            "error": "",
        }
        base = {"score": 100, "success_rate": 1, "rows": [row]}
        other = {**base, "rows": [{**row, "flow_contracts": ["b"]}]}
        self.assertFalse(compare_agentic_flows(base, other)["eligible"])
        other["rows"][0].update(rounds=1, stop_reason="round_limit")
        self.assertFalse(compare_agentic_flows(base, other)["complete"])
        self.assertFalse(compare_agentic_flows(base, other)["eligible"])

    def test_invalid_generated_contract_is_repaired_before_real_task_execution(self):
        model = TaskModel()
        proposals = []

        def generate(system, prompt, *args, **kwargs):
            payload = json.loads(prompt)
            result = model(system, prompt, *args, **kwargs)
            if payload.get("task", "").startswith("Improve the executable"):
                proposals.append(payload)
                if len(proposals) == 1:
                    for file in result["patch"]["files"]:
                        if file["path"] == "kernel.py":
                            file["content"] = file["content"].replace(
                                "KERNEL_CONTRACT_VERSION = 1", ""
                            )
            return result

        plane = self.plane(model=generate)
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "awaiting_approval", detail)
        self.assertEqual(len(proposals), 2)
        self.assertEqual(
            proposals[-1]["validation_errors"][0]["code"], "kernel_contract_missing"
        )
        self.assertIn(
            "KERNEL_CONTRACT_VERSION=1",
            proposals[-1]["validation_errors"][0]["details"]["result"]["missing"],
        )
        self.assertEqual(len(detail["result"]["patch"]["validation_repairs"]), 1)
