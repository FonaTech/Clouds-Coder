"""Optional quota scopes and honest scoring for pre-evaluation rejections."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config
from liquid_kernel.control import (
    BASELINE_KERNEL_FILES,
    StructuredPatchValidator,
    LiquidKernelError,
)
from test_agentic_evolution import TaskModel, experiences, judge, wait


class OptionalEvolutionQuotas(unittest.TestCase):
    def plane(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        plane = LiquidKernelControlPlane(Path(temp.name))
        plane._tokens_used, plane._token_limit = 0, 0
        return plane

    def test_unset_zero_and_mode_changes_preserve_optional_limits(self):
        for mode in ["Tuning", "Thinking", "Aggressive"]:
            cfg = normalize_evolution_config({"mode": mode})
            self.assertEqual(cfg["budget"]["max_tokens"], 0)
            self.assertEqual(cfg["budget"]["max_changed_lines"], 0)
            self.assertEqual(cfg["task_benchmark"]["max_task_tokens"], 0)
            changed = normalize_evolution_config(
                {"mode": "Tuning", "budget": {"max_tokens": 0, "max_changed_lines": 0}},
                current=cfg,
            )
            self.assertEqual(changed["budget"]["max_tokens"], 0)
            self.assertEqual(changed["budget"]["timeout_seconds"], 0)
        explicit = normalize_evolution_config(
            {
                "mode": "Thinking",
                "budget": {"max_tokens": 2000000, "max_changed_lines": 1000},
            }
        )
        changed = normalize_evolution_config({"mode": "Tuning"}, current=explicit)
        self.assertEqual(changed["budget"]["max_tokens"], 2000000)
        self.assertEqual(changed["budget"]["max_changed_lines"], 1000)

    def test_unlimited_tracks_tokens_without_exhaustion_or_hidden_reserve(self):
        plane = self.plane()
        for label in ["task", "proposal", "review"]:
            with plane._model_budget_scope(0, label) as state:
                plane._record_model_tokens(
                    "",
                    {
                        "_evolution_usage": {
                            "total_tokens": 300000,
                            "transport_accounted": True,
                        }
                    },
                )
                self.assertEqual(
                    plane._model_allowance("long prompt" * 10000, 16384), 16384
                )
            self.assertEqual(state["used"], 300000)
            self.assertIsNone(state["remaining"])
            self.assertFalse(state["exhausted"])
        self.assertEqual(plane._tokens_used, 900000)
        plane._check_cancel("")

    def test_positive_task_only_total_only_and_nested_limits_are_enforced(self):
        plane = self.plane()
        with self.assertRaises(TimeoutError):
            with plane._model_budget_scope(500):
                plane._record_model_tokens(
                    "",
                    {
                        "_evolution_usage": {
                            "total_tokens": 501,
                            "transport_accounted": True,
                        }
                    },
                )
        plane = self.plane()
        plane._token_limit = 1000
        with self.assertRaises(LiquidKernelError) as caught:
            with plane._model_budget_scope(0):
                plane._record_model_tokens(
                    "",
                    {
                        "_evolution_usage": {
                            "total_tokens": 1001,
                            "transport_accounted": True,
                        }
                    },
                )
        self.assertEqual(caught.exception.code, "run_budget_exhausted")
        plane = self.plane()
        with plane._model_budget_scope(500):
            with plane._model_budget_scope(0):
                self.assertEqual(plane._rollout_token_ceiling, 500)
        self.assertEqual(plane._rollout_token_ceiling, 0)

    def test_transport_honors_task_only_quota_with_unlimited_total(self):
        app = cc.AppContext.__new__(cc.AppContext)
        app.liquid_kernel = self.plane()
        app._liquid_kernel_profile = lambda _: {
            "model": "test",
            "provider": "ollama",
            "base_url": "http://localhost:11434",
        }
        with app.liquid_kernel._model_budget_scope(200):
            with mock.patch.object(cc.OllamaClient, "chat") as chat:
                with self.assertRaisesRegex(
                    TimeoutError, "task_token_budget_exhausted"
                ):
                    app._liquid_kernel_transport_call(
                        "Return JSON", "x" * 4000, "", 1024
                    )
                chat.assert_not_called()

    def test_total_quota_does_not_synthesize_per_task_or_review_caps(self):
        plane = self.plane()
        cfg = normalize_evolution_config(
            {"mode": "Thinking", "budget": {"max_tokens": 2000000}}
        )
        cfg = plane._apply_task_runtime_limits(cfg)
        self.assertEqual(cfg["task_benchmark"]["max_task_tokens"], 0)
        plane.task_runtime_limits = lambda: {"max_rounds": 200, "max_run_tokens": 1000}
        self.assertEqual(
            plane._apply_task_runtime_limits(cfg)["task_benchmark"]["max_task_tokens"],
            0,
        )

    def test_full_pipeline_unlimited_runs_past_old_implicit_preset(self):
        model = TaskModel()

        def billed(*args, **kwargs):
            result = model(*args, **kwargs)
            result["_evolution_usage"] = {
                "total_tokens": 7000,
                "transport_accounted": True,
            }
            return result

        plane = self.plane()
        plane.model_callback = billed
        plane.judge_callback = judge
        plane.experience_provider = lambda *_: experiences(2)
        cfg = plane.apply_startup_config("Thinking", "off")["config"]
        plane.save_config(
            {"budget": {**cfg["budget"], "candidate_limit": 1}}, cfg["revision"]
        )
        detail = wait(plane, plane.trigger()["run_id"])
        self.assertEqual(detail["status"], "awaiting_approval", detail)
        self.assertGreater(detail["result"]["tokens_used"], 120000)
        self.assertTrue(detail["result"]["confirmation"]["passed"])
        self.assertEqual(detail["progress"]["tokens"]["limit"], 0)
        allocations = [
            e["payload"]
            for e in detail["events"]
            if e["kind"] == "task_budget_allocated"
        ]
        self.assertEqual(allocations[0]["per_task_tokens"], 0)
        self.assertEqual(allocations[0]["per_review_tokens"], 0)
        self.assertEqual(detail["progress"]["execution"].get("quota_failures", 0), 0)

    def test_legacy_rejection_exposes_baseline_zero_and_reason_without_judge_score(
        self,
    ):
        plane = self.plane()
        cfg = plane.apply_startup_config("Thinking", "off")["config"]
        run = plane.registry.create_run(cfg, "test")
        root = plane.registry.experience_root / run
        root.mkdir(parents=True, exist_ok=True)
        (root / "incumbent_rollouts.json").write_text(
            json.dumps(
                {
                    "score": 0,
                    "success_rate": 0,
                    "rows": [],
                    "artifacts": {"secret": "never return"},
                }
            )
        )
        plane.registry.update_run(
            run,
            "rejected",
            result_json={
                "evaluations": [
                    {
                        "candidate_index": 1,
                        "code": "patch_too_large",
                        "reason": "candidate exceeds the changed-line budget",
                        "decision": "reject",
                    }
                ]
            },
        )
        detail = plane.registry.run_detail(run)
        summary = detail["score_summary"]
        self.assertEqual(summary["incumbent"]["hard"], 0)
        self.assertEqual(summary["candidate"]["mixed"], 0)
        self.assertFalse(summary["candidate"]["task_execution_measured"])
        self.assertFalse(summary["review_completed"])
        self.assertEqual(summary["evaluations"][0]["code"], "patch_too_large")
        self.assertNotIn("secret", json.dumps(summary))

    def test_default_large_patch_can_run_but_explicit_line_limit_blocks_it(self):
        validator = StructuredPatchValidator()
        cfg = normalize_evolution_config({"mode": "Tuning"})
        proposal = {
            "patch": {
                "files": [
                    {
                        "path": "prompt_policy.py",
                        "operation": "replace_file",
                        "content": BASELINE_KERNEL_FILES["prompt_policy.py"]
                        + "\n"
                        + "# refactoring layout\n" * 500,
                    }
                ]
            }
        }
        _, meta = validator.apply(BASELINE_KERNEL_FILES, proposal, cfg)
        self.assertGreater(meta["changed_lines"], 400)
        cfg["budget"]["max_changed_lines"] = 100
        with self.assertRaises(LiquidKernelError) as caught:
            validator.apply(BASELINE_KERNEL_FILES, proposal, cfg)
        self.assertEqual(caught.exception.code, "patch_too_large")
        self.assertEqual(caught.exception.details["limit"], 100)

    def test_old_automatic_line_limit_is_migrated_without_touching_stored_history(self):
        plane = self.plane()
        old = normalize_evolution_config({"mode": "Tuning"})
        old.pop("quota_policy_version")
        old["budget"].update(max_changed_lines=400, max_tokens=2000000)
        plane.config_path.write_text(json.dumps(old))
        before = plane.config_path.read_bytes()
        self.assertEqual(plane.config()["budget"]["max_changed_lines"], 0)
        self.assertEqual(plane.config()["budget"]["max_tokens"], 2000000)
        self.assertEqual(plane.config_path.read_bytes(), before)
