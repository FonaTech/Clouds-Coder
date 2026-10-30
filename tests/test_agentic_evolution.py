"""Actual multi-round rollouts against a deterministic model service substitute."""
import copy
import json
import shlex
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

import Clouds_Coder as cc
from liquid_kernel import LiquidKernelControlPlane, normalize_evolution_config
from liquid_kernel.agentic import (
    AgenticBenchmark,
    KernelWorker,
    TaskWorkspace,
    apply_execution_policy,
    build_task_bank,
    source_sessions,
)
from liquid_kernel.control import BASELINE_KERNEL_FILES, LiquidKernelError


def experiences(count=3):
    return {"history_by_version": {"v1": {"records": [
        {"user_id": "user-a", "session_id": f"s{index}", "title": "数据处理工具",
         "messages": [{"role": "user", "content": f"读取输入、实现数据处理并输出报告，任务 {index}"},
                      {"role": "assistant", "content": "Historical solution must never seed the test workspace"},
                      {"role": "user", "content": "处理中需要接受调整后的输出格式"}]}
        for index in range(count)
    ]}}}


class TaskModel:
    def __init__(self, reject=False):
        self.calls = []
        self.reject = reject

    def __call__(self, system, prompt, profile=None, max_tokens=4096, **kwargs):
        payload = json.loads(prompt) if isinstance(prompt, str) else prompt
        self.calls.append(copy.deepcopy(payload))
        if "source" in payload:
            return {"goal": "读取 input.txt，生成 result.txt 和 summary.txt，并处理后续用户修订。",
                    "starter_files": {"input.txt": "initial input"}, "family": "data-processing",
                    "followups": [{"after_round": 3, "content": "最终输出改为 revised output"}],
                    "checks": [{"kind": "contains", "path": "result.txt", "value": "revised output"},
                               {"kind": "equals", "path": "summary.txt", "value": "verified"}],
                    "rubric": ["Follow the revised user request and verify actual files."], "minimum_tool_calls": 3}
        if payload.get("task", "").startswith("Improve the executable"):
            if self.reject:
                return {"decision": "no_change", "reason": "No supported improvement"}
            return {"decision": "change", "reason": "Baseline ignored later steering after an avoidable failed read.",
                    "changelog": "Move file inspection ahead of other actions using a recovery module.",
                    "patch": {"files": [
                        {"path": "kernel.py", "operation": "replace_file", "content": BASELINE_KERNEL_FILES["kernel.py"] +
                         '\nfrom .recovery import before_round\n'},
                        {"path": "recovery.py", "operation": "replace_file", "content":
                         'def before_round(context=None):\n    return {"tool_order": ["read_file", "write_file", "finish_task"]}\n'},
                    ]}}
        if payload.get("task", "").startswith("Audit task and acceptance"):
            return {"valid": True, "issues": []}
        messages = payload["messages"]
        round_index = 1 + sum(row["role"] == "assistant" for row in messages)
        preferred_read = payload["tools"][0]["function"]["name"] == "read_file"
        if round_index == 1:
            return {"tool_calls": [{"name": "read_file", "arguments": {"path": "input.txt" if preferred_read else "missing.txt"}}]}
        if round_index == 2:
            return {"tool_calls": [{"name": "write_file", "arguments": {"path": "result.txt", "content": "initial output"}}]}
        if round_index == 3:
            return {"tool_calls": [{"name": "write_file", "arguments": {"path": "result.txt", "content": "revised output" if preferred_read else "initial output"}}]}
        if round_index == 4:
            return {"tool_calls": [{"name": "write_file", "arguments": {"path": "summary.txt", "content": "verified"}}]}
        return {"tool_calls": [{"name": "finish_task", "arguments": {}}], "final": "Done after verification."}


def judge(payload, *_args):
    assert payload["incumbent_source"] == payload["candidate_source"] == ""
    observed = payload["observations"]
    return {"incumbent": observed["incumbent"]["score"], "candidate": observed["candidate"]["score"],
            "rationale": "Compared observed files, assertions, corrections, and tool failures."}


def wait(plane, run_id, timeout=12):
    deadline = time.monotonic() + timeout
    while plane.active_run_id and time.monotonic() < deadline:
        time.sleep(.02)
    assert not plane.active_run_id, "run did not finish"
    return plane.registry.run_detail(run_id)


class AgenticEvolutionTests(unittest.TestCase):
    def test_task_bank_uses_human_requests_and_separates_source_sessions(self):
        model = TaskModel()
        config = normalize_evolution_config({"mode": "Thinking"})
        bank = build_task_bank(experiences(), config, lambda system, prompt: model(system, prompt), 42)
        self.assertEqual(len(bank["tasks"]), 3)
        self.assertEqual(bank["holdout_count"], 1)
        self.assertEqual(len({row["source_id"] for row in bank["tasks"]}), 3)
        self.assertNotIn("Historical solution", json.dumps(model.calls))
        self.assertTrue(all(row["followups"] and len(row["checks"]) == 2 for row in bank["tasks"]))

    def test_same_session_across_versions_never_crosses_splits(self):
        experience = experiences(2)
        experience["history_by_version"]["v2"] = copy.deepcopy(experience["history_by_version"]["v1"])
        self.assertEqual(len(source_sessions(experience, 20)), 2)

    def test_recent_source_and_last_user_correction_survive_history_prompt_truncation(self):
        experience = experiences(2)
        latest = {"user_id": "user-a", "session_id": "newest", "title": "New preference", "updated_at": 100,
                  "messages": [{"role": "user", "content": f"request {i}"} for i in range(30)]}
        experience["task_source_records"] = [latest]
        sources = source_sessions(experience, 2)
        self.assertEqual(sources[0]["title"], "New preference")
        self.assertIn("request 29", sources[0]["user_turns"])
        self.assertIn("request 0", sources[0]["user_turns"])

    def test_transport_failure_during_rollout_fails_the_run(self):
        with tempfile.TemporaryDirectory() as temp:
            model = TaskModel()

            def fail_worker(system, prompt, profile, tokens):
                payload = json.loads(prompt)
                if "messages" in payload:
                    raise LiquidKernelError("model_call_failed", "worker service unavailable", 502)
                return model(system, payload, profile, tokens)

            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(), model_callback=fail_worker, judge_callback=judge)
            plane.apply_startup_config("Thinking", "off")
            detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "failed")
            self.assertEqual(detail["result"]["code"], "model_call_failed")

    def test_metadata_only_or_single_session_cannot_claim_measured_improvement(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(1),
                                             model_callback=TaskModel(), judge_callback=judge)
            plane.apply_startup_config("Thinking", "off")
            detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "failed")
            self.assertFalse(detail["result"]["evaluated"])
            self.assertEqual(detail["result"]["code"], "insufficient_session_tasks")

    def test_real_tools_followups_artifacts_and_blind_scores_drive_code_evolution(self):
        with tempfile.TemporaryDirectory() as temp:
            model = TaskModel()
            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(),
                                             model_callback=model, judge_callback=judge)
            cfg = plane.apply_startup_config("Thinking", "off")["config"]
            plane.save_config({"budget": {**cfg["budget"], "candidate_limit": 1}}, cfg["revision"])
            incumbent = plane.registry.active_version()
            detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "awaiting_approval", detail)
            result = detail["result"]
            self.assertGreater(result["measured_task_gain"], 0)
            self.assertTrue(result["confirmation"]["completed"])
            self.assertTrue(result["confirmation"]["passed"])
            self.assertEqual(result["candidate"]["hard"], 100)
            self.assertIn("recovery.py", result["patch"]["paths"])
            self.assertEqual(plane.registry.active_version(), incumbent)
            run_root = plane.registry.experience_root / detail["run_id"]
            bank = json.loads((run_root / "task_bank.json").read_text())
            observed = json.loads((run_root / "candidate_1_rollouts.json").read_text())
            self.assertTrue(all(row["success"] and row["rounds"] == 5 for row in observed["rows"]))
            self.assertTrue(all(row["artifacts"]["result.txt"] == "revised output" for row in observed["rows"]))
            design = next(row for row in model.calls if row.get("task", "").startswith("Improve the executable"))
            holdout_ids = {row["id"] for row in bank["tasks"] if row["split"] == "holdout"}
            self.assertTrue(holdout_ids.isdisjoint({row["id"] for row in design["training_tasks"]}))
            self.assertTrue(all(row["split"] == "train" for row in design["baseline_training_rollouts"]))
            candidate = plane.registry.sources(detail["candidate_version"])
            context = {"messages": [{"role": "user", "content": "A real live user"}]}
            self.assertEqual(plane.runtime.hook("before_round", version=detail["candidate_version"], context=context)["tool_order"][0], "read_file")
            self.assertIn("recovery.py", candidate)

    def test_independent_full_workflow_confirmation_failure_blocks_registration(self):
        original = AgenticBenchmark.run
        def confirmed_run(benchmark, files, tasks, config, arm="kernel"):
            result = original(benchmark, files, tasks, config, arm)
            if arm == 'candidate_1_confirmation':
                result['score'], result['success_rate'] = 0, 0
                for row in result['rows']:
                    row['success'], row['score'] = False, 0
            return result
        with tempfile.TemporaryDirectory() as temp:
            plane=LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_: experiences(2),
                                           model_callback=TaskModel(), judge_callback=judge)
            cfg=plane.apply_startup_config('Thinking','off')['config']
            plane.save_config({'budget':{**cfg['budget'],'candidate_limit':1,'max_tokens':240000}},cfg['revision'])
            incumbent=plane.registry.active_version()
            with mock.patch.object(AgenticBenchmark,'run',new=confirmed_run):
                detail=wait(plane,plane.trigger()['run_id'])
            self.assertEqual(detail['status'],'rejected')
            self.assertEqual(plane.registry.active_version(),incumbent)
            evaluation=detail['result']['evaluations'][0]
            self.assertTrue(evaluation['confirmation']['completed'])
            self.assertFalse(evaluation['confirmation']['passed'])
            self.assertEqual(evaluation['decision'],'reject')

    def test_holdout_regression_cannot_be_bought_with_a_high_model_score(self):
        with tempfile.TemporaryDirectory() as temp:
            model = TaskModel()
            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(),
                                             model_callback=model, judge_callback=lambda *_args: {"incumbent": 0, "candidate": 100})
            cfg = plane.apply_startup_config("Thinking", "off")["config"]
            plane.save_config({"budget": {**cfg["budget"], "candidate_limit": 1}}, cfg["revision"])
            original = AgenticBenchmark.run
            invocation = 0

            def with_regression(benchmark, *args):
                nonlocal invocation
                invocation += 1
                value = original(benchmark, *args)
                if invocation == 2:
                    for row in value["rows"]:
                        if row["split"] == "holdout":
                            row["score"] = 0
                            row["success"] = False
                return value

            with mock.patch.object(AgenticBenchmark, "run", with_regression):
                detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "rejected", detail)
            self.assertIn("held-out", detail["result"]["evaluations"][0]["reason"])

    def test_strength_caps_cannot_be_bypassed_by_custom_budget(self):
        for mode, expected in (("Tuning", (5, 99999, 2)), ("Thinking", (12, 99999, 4)), ("Aggressive", (30, 99999, 8))):
            cfg = normalize_evolution_config({"mode": mode, "budget": {"max_files": 999, "max_changed_lines": 99999},
                                              "task_benchmark": {"max_tasks": 999, "max_rounds": 999}})
            self.assertEqual((cfg["budget"]["max_files"], cfg["budget"]["max_changed_lines"], cfg["task_benchmark"]["max_tasks"]), expected)
            self.assertEqual(cfg["task_benchmark"]["max_rounds"], 999)

    def test_new_core_module_and_architecture_import_follow_mode_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp))
            cfg = normalize_evolution_config({"mode": "Aggressive"})
            proposal = {"patch": {"files": [{"path": "core_planner.py", "operation": "replace_file", "content": "def next_state(state):\n    return dict(state)\n"}]}}
            candidate, _meta = plane.validator.apply(BASELINE_KERNEL_FILES, proposal, cfg)
            self.assertIn("core_planner.py", candidate)
            with self.assertRaises(LiquidKernelError):
                plane.validator.apply(BASELINE_KERNEL_FILES, proposal, normalize_evolution_config({"mode": "Thinking"}))

    def test_model_token_budget_stops_run_without_promoting(self):
        with tempfile.TemporaryDirectory() as temp:
            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(), model_callback=TaskModel(), judge_callback=judge)
            cfg = plane.apply_startup_config("Thinking", "off")["config"]
            plane.save_config({"budget": {**cfg["budget"], "max_tokens": 128}}, cfg["revision"])
            detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "failed")
            self.assertEqual(detail["result"]["code"], "run_budget_exhausted")
            self.assertFalse(plane.registry.active_state().get("canary"))

    def test_live_context_policy_preserves_human_constraints_and_tool_pairs(self):
        messages = [{"role": "user", "content": "Original goal"}, {"role": "assistant", "content": "old"},
                    {"role": "tool", "content": "old evidence"}, {"role": "user", "content": "New constraint"},
                    {"role": "assistant", "content": "current"}, {"role": "tool", "content": "current evidence"}]
        selected, _tools, tokens = apply_execution_policy(messages, [], 2000, {"recent_tool_exchanges": 1, "max_output_tokens": 512})
        self.assertEqual([row["content"] for row in selected if not row.get("content", "").startswith("<kernel-history-handoff>")], ["Original goal", "New constraint", "current", "current evidence"])
        self.assertIn('old evidence', next(row['content'] for row in selected if row.get('content', '').startswith('<kernel-history-handoff>')))
        self.assertIn('context_recall', next(row['content'] for row in selected if row.get('content', '').startswith('<kernel-history-handoff>')))
        self.assertEqual(tokens, 2000)

    def test_policy_worker_timeout_and_workspace_path_boundaries(self):
        files = dict(BASELINE_KERNEL_FILES)
        files["harness.py"] = files["harness.py"].replace("def before_round(context=None):\n    return {}", "def before_round(context=None):\n    while True:\n        pass")
        worker = KernelWorker(files)
        try:
            with self.assertRaises(TimeoutError):
                worker.call("before_round", {"context": {}}, lambda: None)
        finally:
            worker.close()
        with tempfile.TemporaryDirectory() as temp:
            workspace = TaskWorkspace(temp, lambda: None)
            with self.assertRaises(ValueError):
                workspace.tool("write_file", {"path": "../outside.txt", "content": "bad"})

    @unittest.skipUnless((sys.platform == "darwin" and shutil.which("sandbox-exec")) or shutil.which("bwrap"), "OS command sandbox unavailable")
    def test_real_command_executes_checks_but_cannot_read_or_write_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent / "workspace"
            root.mkdir()
            secret = parent / "outside-secret.txt"
            secret.write_text("private")
            workspace = TaskWorkspace(root, lambda: None)
            inside = 'from pathlib import Path; Path("result.txt").write_text("checked"); assert Path("result.txt").read_text()=="checked"'
            result = workspace.command('python3 -c ' + shlex.quote(inside))
            self.assertEqual(result["exit_code"], 0, result)
            nested = workspace.command('mkdir -p nested/deeper && cd nested/deeper && printf checked > result.txt && cat result.txt')
            self.assertEqual(nested["exit_code"], 0, nested)
            self.assertEqual((root / 'nested/deeper/result.txt').read_text(), 'checked')
            for code in (f'open({str(secret)!r}).read()', f'open({str(secret)!r}, "w").write("changed")'):
                denied = workspace.command('python3 -c ' + shlex.quote(code))
                self.assertNotEqual(denied["exit_code"], 0, denied)
            if sys.platform == "darwin":
                listing = workspace.command('ls ' + shlex.quote(str(parent)))
                self.assertNotEqual(listing["exit_code"], 0, listing)
            self.assertEqual(secret.read_text(), "private")

    def test_cancellation_during_model_turn_cannot_turn_into_a_zero_score_success(self):
        with tempfile.TemporaryDirectory() as temp:
            model = TaskModel()
            plane = None

            def cancel_during_turn(system, prompt, profile, tokens):
                payload = json.loads(prompt)
                if "messages" in payload:
                    plane.cancelled.add(plane.active_run_id)
                return model(system, payload, profile, tokens)

            plane = LiquidKernelControlPlane(Path(temp), experience_provider=lambda *_args: experiences(),
                                             model_callback=cancel_during_turn, judge_callback=judge)
            plane.apply_startup_config("Thinking", "off")
            detail = wait(plane, plane.trigger()["run_id"])
            self.assertEqual(detail["status"], "cancelled", detail)
            self.assertIsNone(plane.registry.active_state().get("canary"))

    def test_startup_framework_upgrade_preserves_signed_evolved_kernel(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "liquid_kernel"
            root.mkdir()
            (root / "control.py").write_text("EVOLUTION_MODEL_CAPABILITY_VERSION = 2\n")
            plane = LiquidKernelControlPlane(root)
            incumbent = plane.registry.active_version()
            files = dict(BASELINE_KERNEL_FILES)
            files["prompt_policy.py"] += "\n# evolved implementation\n"
            evolved = plane.registry.register_candidate("test", incumbent, files, mode="Thinking", changelog="evolved", scores={})
            plane.registry.begin_canary(evolved, 100)
            plane.registry.promote(evolved)
            state_paths = [root / "active.json", root / "registry.sqlite", root / ".artifact_signing_key", root / "config.json"]
            before = {str(path): path.read_bytes() for path in state_paths}
            status = cc._ensure_embedded_liquid_kernel_package(root)
            self.assertEqual(status["model_capability_version"], 19)
            self.assertEqual(status["diagnosis"], "upgraded")
            self.assertEqual({str(path): path.read_bytes() for path in state_paths}, before)
            restarted = LiquidKernelControlPlane(root)
            self.assertEqual(restarted.registry.active_version(), evolved)
            self.assertIn("evolved implementation", restarted.registry.sources(evolved)["prompt_policy.py"])
            self.assertFalse(restarted.inject_embedded_kernel()["injected"])
            self.assertEqual(restarted.registry.active_version(), evolved)
            self.assertTrue(cc._ensure_embedded_liquid_kernel_package(root)["ready"])

    def test_newer_compatible_framework_is_not_downgraded(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cc._ensure_embedded_liquid_kernel_package(root)
            path = root / "control.py"
            path.write_text(path.read_text().replace("EVOLUTION_MODEL_CAPABILITY_VERSION = 19", "EVOLUTION_MODEL_CAPABILITY_VERSION = 20"))
            before = path.read_bytes()
            status = cc._ensure_embedded_liquid_kernel_package(root)
            self.assertEqual(status["diagnosis"], "compatible_newer_framework_preserved")
            self.assertEqual(path.read_bytes(), before)

    def test_corrupt_framework_version_is_repaired_without_touching_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "control.py").write_bytes(b"\xff\x00invalid")
            artifact = root / "artifacts" / "evolved" / "kernel.py"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# evolved artifact")
            status = cc._ensure_embedded_liquid_kernel_package(root)
            self.assertEqual(status["diagnosis"], "upgraded")
            self.assertEqual(status["model_capability_version"], 19)
            self.assertEqual(artifact.read_text(), "# evolved artifact")

    def test_partial_framework_upgrade_failure_rolls_back_without_touching_state(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            old = {"__init__.py": b"# previous package", "control.py": b"EVOLUTION_MODEL_CAPABILITY_VERSION = 2\n",
                   "models.py": b"# previous model adapter", "config.json": b'{"revision": 7}',
                   "active.json": b'{"version":"evolved"}', ".artifact_signing_key": b"key"}
            for name, data in old.items():
                (root / name).write_bytes(data)
            replace = cc.os.replace
            failed = False

            def fail_once(source, target):
                nonlocal failed
                if Path(target) == root / "models.py" and not failed:
                    failed = True
                    raise OSError("simulated upgrade interruption")
                return replace(source, target)

            with mock.patch.object(cc.os, "replace", fail_once):
                with self.assertRaisesRegex(RuntimeError, "rolled back"):
                    cc._ensure_embedded_liquid_kernel_package(root)
            self.assertEqual({name: (root / name).read_bytes() for name in old}, old)
            self.assertFalse((root / ".framework-upgrade.lock").exists())
            self.assertFalse((root / "agentic.py").exists())

    def test_stale_startup_lock_recovers_without_replacing_evolved_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".framework-upgrade.lock").write_text(json.dumps({"pid": 99999999, "created_at": 0}))
            (root / "active.json").write_text('{"version":"keep-this-evolved-version"}')
            status = cc._ensure_embedded_liquid_kernel_package(root)
            self.assertTrue(status["restored"])
            self.assertIn("keep-this-evolved-version", (root / "active.json").read_text())
            self.assertFalse((root / ".framework-upgrade.lock").exists())


if __name__ == "__main__":
    unittest.main()
