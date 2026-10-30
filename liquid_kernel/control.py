from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import hmac
import importlib.util
import json
import math
import os
import random
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .agentic import (
    AgenticBenchmark,
    SCORING_PROTOCOL_VERSION,
    KernelWorker,
    build_task_bank,
    canonicalize_task_bank,
    compare_agentic_flows,
    rollout_complete,
    task_config,
    trajectory_model_view,
    training_opportunity_evidence,
)
from .context import EvaluationDefinitionError, normalize_executable_command, json_text, utf8_bytes, utf8_text, subprocess_environment

EVOLUTION_MODES = ("Off", "Tuning", "Thinking", "Aggressive")
CONTROL_SCHEMA_VERSION = 1
EVOLUTION_MODEL_CAPABILITY_VERSION = 19
KERNEL_CONTRACT_VERSION = 1
BASELINE_KERNEL_SOURCE = '''from __future__ import annotations

KERNEL_CONTRACT_VERSION = 1
KERNEL_NAME = "Clouds Coder Baseline"

from .harness import after_tool_results, before_round, before_run
from .prompt_policy import augment_prompt
from .tool_policy import filter_tools


def describe():
    return {
        "name": KERNEL_NAME,
        "contract_version": KERNEL_CONTRACT_VERSION,
        "capabilities": ["tools", "prompt-policy", "harness-hooks"],
    }
'''

BASELINE_TOOL_POLICY_SOURCE = '''from __future__ import annotations


def filter_tools(tools, *, role="", context=None):
    return list(tools or [])
'''

BASELINE_PROMPT_POLICY_SOURCE = '''from __future__ import annotations


def augment_prompt(prompt, *, role="", context=None):
    return str(prompt or "")
'''

BASELINE_HARNESS_SOURCE = '''from __future__ import annotations


def before_run(context=None):
    return {}


def before_round(context=None):
    return {}


def after_tool_results(results, *, context=None):
    return list(results or [])
'''

BASELINE_KERNEL_FILES = {
    "kernel.py": BASELINE_KERNEL_SOURCE,
    "tool_policy.py": BASELINE_TOOL_POLICY_SOURCE,
    "prompt_policy.py": BASELINE_PROMPT_POLICY_SOURCE,
    "harness.py": BASELINE_HARNESS_SOURCE,
}

TUNING_KERNEL_FILES = frozenset({"kernel.py", "tool_policy.py", "prompt_policy.py", "context_policy.py", "recovery.py"})
CONTROLLED_KERNEL_FILES = frozenset({*TUNING_KERNEL_FILES, "planning.py", "memory.py", "tool_router.py",
                                    "verification.py", "scheduler.py", "state.py", "serialization.py"})
FULL_AGENT_CORE_FILES = frozenset({*CONTROLLED_KERNEL_FILES, "harness.py"})
IMMUTABLE_CONTROL_COMPONENTS = (
    "authentication",
    "persistence",
    "evaluation",
    "promotion",
    "audit",
    "signing",
    "sandbox",
)


class LiquidKernelError(RuntimeError):
    def __init__(self, code: str, message: str, status: int = 400, details: dict | None = None):
        super().__init__(message)
        self.code = str(code or "liquid_kernel_error")
        self.status = int(status or 400)
        self.details = dict(details or {})


def _now() -> float:
    return time.time()


def _json(value: Any) -> str:
    return json_text(value, sort_keys=True, separators=(",", ":"), default=str)


def normalize_proposal_output(value):
    """Repair unambiguous envelope placement, never infer a decision or patch."""
    result = copy.deepcopy(value)
    changes = []
    for _ in range(4):
        if not isinstance(result, dict) or any(key in result for key in ('decision', 'patch')):
            break
        envelopes = [(key, result[key]) for key in ('proposal', 'result', 'data', 'output') if isinstance(result.get(key), dict)]
        if len(envelopes) != 1:
            break
        key, result = envelopes[0]
        changes.append('unwrap:' + key)
    if not isinstance(result, dict):
        raise LiquidKernelError('invalid_proposal_schema', 'Proposal must contain an explicit decision and reason', 422)
    patch = result.get('patch') if isinstance(result.get('patch'), dict) else {}
    for key in ('decision', 'reason', 'changelog'):
        outer, nested = result.get(key), patch.get(key)
        if key == 'decision' and outer and nested and outer != nested:
            raise LiquidKernelError('invalid_proposal_schema', 'Proposal decisions conflict', 422, {'field':key})
        if not outer and isinstance(nested, str) and nested.strip():
            result[key] = nested
            changes.append('patch.' + key + '->' + key)
    if not isinstance(result.get('decision'), str) or result['decision'] not in {'change', 'no_change'} or not isinstance(result.get('reason'), str) or not result['reason'].strip():
        raise LiquidKernelError('invalid_proposal_schema', 'Proposal must contain an explicit decision and reason', 422,
                                {'required_fields':['decision','reason'], 'received_keys':sorted(result)})
    if result['decision'] == 'no_change' and patch.get('files'):
        raise LiquidKernelError('invalid_proposal_schema', 'No-change proposal contains an executable patch', 422)
    if changes:
        result['_proposal_normalization'] = changes
    return result


def _read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def _atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(json_text(payload, indent=2, sort_keys=True), encoding="utf-8")
    try:
        os.chmod(temp, 0o600)
    except Exception:
        pass
    os.replace(temp, path)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _normalize_kernel_files(value: object) -> dict[str, str]:
    if isinstance(value, str):
        return {"kernel.py": utf8_text(value)}
    if not isinstance(value, dict):
        raise LiquidKernelError("invalid_kernel_bundle", "kernel artifact must be source text or a file map")
    files: dict[str, str] = {}
    for raw_path, raw_source in value.items():
        path = str(raw_path or "").strip().replace("\\", "/")
        if not path or path.startswith("/") or ".." in Path(path).parts or "/" in path:
            raise LiquidKernelError("invalid_kernel_path", "kernel artifact contains an invalid file path")
        files[path] = utf8_text(raw_source or "")
    if "kernel.py" not in files:
        raise LiquidKernelError("kernel_contract_missing", "kernel artifact is missing kernel.py")
    return files


def _kernel_file_hashes(files: dict[str, str]) -> dict[str, str]:
    return {path: _sha256_bytes(utf8_bytes(source)) for path, source in sorted(files.items())}


def _kernel_bundle_hash(files: dict[str, str]) -> str:
    return _sha256_bytes(utf8_bytes(_json(_kernel_file_hashes(files))))


def _kernel_bundle_text(files: dict[str, str]) -> str:
    return "\n\n".join(f"# === {path} ===\n{source}" for path, source in sorted(files.items()))


def _safe_zone(value: object) -> str:
    raw = str(value or "Asia/Shanghai").strip() or "Asia/Shanghai"
    try:
        ZoneInfo(raw)
        return raw
    except Exception:
        return "Asia/Shanghai"


MODE_PRESETS: dict[str, dict] = {
    "Off": {
        "schedule": "off",
        "cooldown_hours": 0,
        "candidate_limit": 0,
        "max_files": 0,
        "max_changed_lines": 0,
        "max_cases": 0,
        "max_tokens": 0,
        "timeout_seconds": 0,
        "mutable_surface": "none",
        "auto_promote": False,
        "minimum_gain": 0.0,
    },
    "Tuning": {
        "schedule": "weekly",
        "cooldown_hours": 72,
        "candidate_limit": 1,
        "max_files": 5,
        "max_changed_lines": 0,
        "max_cases": 36,
        "max_tokens": 0,
        "timeout_seconds": 0,
        "mutable_surface": "controlled",
        "auto_promote": True,
        "minimum_gain": 1.5,
    },
    "Thinking": {
        "schedule": "every_3_days",
        "cooldown_hours": 48,
        "candidate_limit": 2,
        "max_files": 12,
        "max_changed_lines": 0,
        "max_cases": 72,
        "max_tokens": 0,
        "timeout_seconds": 0,
        "mutable_surface": "controlled",
        "auto_promote": False,
        "minimum_gain": 3.0,
    },
    "Aggressive": {
        "schedule": "daily",
        "cooldown_hours": 24,
        "candidate_limit": 3,
        "max_files": 30,
        "max_changed_lines": 0,
        "max_cases": 120,
        "max_tokens": 0,
        "timeout_seconds": 0,
        "mutable_surface": "full_agent_core",
        "auto_promote": False,
        "minimum_gain": 5.0,
    },
}


HARD_BUDGET_LIMITS = {
    "candidate_limit": 3,
    "max_files": 30,
    "max_changed_lines": 100_000_000,
    "max_cases": 160,
    "max_tokens": 10_000_000,
    "timeout_seconds": 21_600,
}


def normalize_model_ref(value: object) -> dict | None:
    if value is None or value == "":
        return None
    if not isinstance(value, dict) or set(value) - {"source", "owner", "profile_id", "model", "fingerprint"}:
        raise LiquidKernelError("invalid_model_ref", "model reference must contain only source, owner, profile_id, model and fingerprint")
    ref = {key: str(value.get(key, "") or "").strip() for key in ("source", "owner", "profile_id", "model")}
    if ref["source"] not in {"global", "agent", "ide"} or not ref["profile_id"] or not ref["model"]:
        raise LiquidKernelError("invalid_model_ref", "select a configured model and its source")
    if (ref["source"] == "global" and ref["owner"]) or (ref["source"] != "global" and not ref["owner"]):
        raise LiquidKernelError("invalid_model_ref", "model ownership is invalid")
    if value.get("fingerprint"):
        ref["fingerprint"] = str(value["fingerprint"])
    return ref


def valid_judge_score(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
        raise LiquidKernelError("invalid_judge_output", "judge must return numeric scores between 0 and 100")
    return float(value)


def default_evolution_config() -> dict:
    preset = dict(MODE_PRESETS["Off"])
    return {
        "revision": 1,
        "quota_policy_version": 2,
        "timeout_policy_version": 1,
        "mode": "Off",
        "schedule": preset.pop("schedule"),
        "timezone": "Asia/Shanghai",
        "event_triggers": True,
        "event_error_rate_threshold": 0.12,
        "event_retry_rate_threshold": 0.18,
        "cooldown_hours": preset.pop("cooldown_hours"),
        "history_version_depth": 2,
        "history_access": "full",
        "history_start_date": "",
        "history_end_date": "",
        "user_scope": ["*"],
        "session_scope": ["*"],
        "generator_profile": "",
        "judge_profile": "",
        "generator_model_ref": None,
        "judge_model_ref": None,
        "budget": {
            key: preset[key]
            for key in ("candidate_limit", "max_files", "max_changed_lines", "max_cases", "max_tokens", "timeout_seconds")
        },
        "mutable_surface": preset["mutable_surface"],
        "auto_promote": preset["auto_promote"],
        "deployment_policy": "mode",
        "minimum_gain": preset["minimum_gain"],
        "task_benchmark": task_config("Off"),
        "hard_score_weight": 0.70,
        "soft_score_weight": 0.20,
        "efficiency_score_weight": 0.10,
        "hard_regression_limit": 0.05,
        "canary": {
            "stages": [5, 25, 100],
            "minimum_completed": [20, 50, 0],
            "minimum_hours": [24, 48, 0],
            "success_drop_limit": 0.05,
            "error_increase_limit": 0.05,
            "p95_latency_increase_limit": 0.20,
        },
    }


def normalize_evolution_config(raw: object, *, current: dict | None = None) -> dict:
    raw_values = dict(raw) if isinstance(raw, dict) else {}
    source = dict(current or default_evolution_config())
    source.update(raw_values)
    mode = str(source.get("mode", "Off") or "Off").strip().title()
    if mode not in EVOLUTION_MODES:
        raise LiquidKernelError("invalid_mode", "mode must be Off, Tuning, Thinking, or Aggressive")
    preset = MODE_PRESETS[mode]
    previous_mode = str((current or {}).get("mode", "Off") or "Off").strip().title()
    mode_changed = bool(current) and mode != previous_mode
    out = default_evolution_config()
    out.update({key: value for key, value in source.items() if key in out})
    out["mode"] = mode
    out["timezone"] = _safe_zone(out.get("timezone"))
    submitted_schedule = str(raw_values.get("schedule", "") or "").strip().lower()
    current_schedule = str((current or {}).get("schedule", "") or "").strip().lower()
    schedule_source = (
        preset["schedule"]
        if mode_changed and (not submitted_schedule or submitted_schedule == current_schedule)
        else out.get("schedule")
    )
    out["schedule"] = str(schedule_source or preset["schedule"]).strip().lower()
    if out["schedule"] not in {"off", "hourly", "daily", "every_3_days", "weekly"}:
        raise LiquidKernelError("invalid_schedule", "schedule must be off, hourly, daily, every_3_days, or weekly")
    if mode == "Off":
        out["schedule"] = "off"
    out["event_triggers"] = bool(out.get("event_triggers", True))
    out["event_error_rate_threshold"] = max(0.01, min(1.0, float(out.get("event_error_rate_threshold", 0.12) or 0.12)))
    out["event_retry_rate_threshold"] = max(0.01, min(1.0, float(out.get("event_retry_rate_threshold", 0.18) or 0.18)))
    cooldown_source = preset["cooldown_hours"] if mode_changed else out.get("cooldown_hours")
    out["cooldown_hours"] = max(0, min(24 * 30, int(cooldown_source or 0)))
    out["history_version_depth"] = max(0, min(12, int(out.get("history_version_depth", 2) or 0)))
    out["history_access"] = str(out.get("history_access", "full") or "full").strip().lower()
    if out["history_access"] not in {"full", "metadata"}:
        raise LiquidKernelError("invalid_history_access", "history_access must be full or metadata")
    out["history_start_date"] = str(out.get("history_start_date", "") or "").strip()
    out["history_end_date"] = str(out.get("history_end_date", "") or "").strip()
    for key in ("user_scope", "session_scope"):
        values = out.get(key, ["*"])
        if not isinstance(values, list):
            values = [values]
        out[key] = [str(item).strip() for item in values if str(item).strip()][:500] or ["*"]
    out["generator_profile"] = str(out.get("generator_profile", "") or "").strip()
    out["judge_profile"] = str(out.get("judge_profile", "") or "").strip()
    for role in ("generator", "judge"):
        if f"{role}_profile" in raw_values and f"{role}_model_ref" not in raw_values:
            out[f"{role}_model_ref"] = None
        out[f"{role}_model_ref"] = normalize_model_ref(out.get(f"{role}_model_ref"))
    supplied_budget = out.get("budget", {}) if isinstance(out.get("budget"), dict) else {}
    if not current and "budget" not in raw_values:
        supplied_budget = {}
    if mode_changed:
        # Strength controls code edits. Compute limits are explicit choices;
        # zero must survive a mode switch as the unlimited sentinel.
        submitted = raw_values.get("budget", {})
        supplied_budget = {key: submitted[key] for key in ("max_tokens", "timeout_seconds", "max_changed_lines")
                           if isinstance(submitted, dict) and key in submitted}
        for key in ("max_tokens", "max_changed_lines", "timeout_seconds"):
            if key not in supplied_budget:
                supplied_budget[key] = (current or {}).get("budget", {}).get(key, 0)
    budget: dict[str, int] = {}
    for key, hard_limit in HARD_BUDGET_LIMITS.items():
        default_value = int(preset[key])
        requested = int(supplied_budget.get(key, default_value) or 0)
        ceiling = int(hard_limit) if key in {"max_tokens", "timeout_seconds", "max_changed_lines"} and mode != "Off" else min(int(hard_limit), default_value)
        budget[key] = max(0, min(ceiling, requested))
    out["budget"] = budget
    out["quota_policy_version"] = 2
    prior_task = source.get("task_benchmark", {})
    task_source = raw_values.get("task_benchmark", {"enabled": prior_task.get("enabled", True), "max_task_tokens": prior_task.get("max_task_tokens", 0)} if mode_changed else prior_task)
    out["task_benchmark"] = task_config(mode, task_source)
    out["mutable_surface"] = str(preset["mutable_surface"])
    policy = str(out.get("deployment_policy", "mode") or "mode")
    if policy not in {"mode", "automatic", "manual"}:
        raise LiquidKernelError("invalid_deployment_policy", "deployment_policy must be mode, automatic or manual")
    out["deployment_policy"] = policy
    out["auto_promote"] = mode != "Off" and (policy == "automatic" or (policy == "mode" and bool(preset["auto_promote"])))
    minimum_gain_source = preset["minimum_gain"] if mode_changed else out.get("minimum_gain")
    out["minimum_gain"] = max(float(preset["minimum_gain"]), float(minimum_gain_source or 0.0))
    out["hard_score_weight"] = 0.70
    out["soft_score_weight"] = 0.20
    out["efficiency_score_weight"] = 0.10
    out["hard_regression_limit"] = 0.05
    canary = out.get("canary", {}) if isinstance(out.get("canary"), dict) else {}
    out["canary"] = {
        "stages": [5, 25, 100],
        "minimum_completed": [20, 50, 0],
        "minimum_hours": [24, 48, 0],
        "success_drop_limit": max(0.01, min(0.25, float(canary.get("success_drop_limit", 0.05) or 0.05))),
        "error_increase_limit": max(0.01, min(0.25, float(canary.get("error_increase_limit", 0.05) or 0.05))),
        "p95_latency_increase_limit": max(0.05, min(1.0, float(canary.get("p95_latency_increase_limit", 0.20) or 0.20))),
    }
    out["revision"] = max(1, int(out.get("revision", 1) or 1))
    return out


@dataclass(frozen=True)
class KernelArtifact:
    version: str
    parent_version: str
    path: Path
    source_hash: str
    status: str


class _ClosingSQLiteConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            return super().__exit__(exc_type, exc_value, exc_traceback)
        finally:
            self.close()


_PROGRESS_TRANSIENT = frozenset({'task_round_started', 'task_round_completed', 'task_tool_started', 'task_tool_completed', 'model_request_wait', 'model_request_retry', 'model_http_attempt_started', 'model_phase_round_started', 'token_usage'})
_PROGRESS_FIELDS = frozenset({'task_id', 'task_index', 'task_total', 'round', 'round_limit', 'tool_calls', 'tool_name', 'tool_index', 'arm', 'split', 'attempt', 'max_attempts', 'operation', 'candidate_index', 'candidate_total', 'stage', 'model', 'request_id', 'timeout_seconds', 'elapsed_seconds', 'retry_after_seconds', 'http_status', 'error_type', 'error_code', 'provider', 'endpoint_host', 'status_origin', 'last_http_status', 'cause_code', 'success', 'score', 'used', 'limit', 'train', 'holdout', 'per_task_tokens', 'paired_rollouts', 'reserve_percent', 'scope', 'remaining', 'exhausted', 'stop_reason', 'required_input_tokens'})
_TERMINAL_RUNS = frozenset({'no_change', 'rejected', 'failed', 'cancelled', 'promoted', 'rolled_back', 'awaiting_approval'})


def _progress_update(state, kind, payload, now, config=None):
    """Reduce metadata only; no prompts, source bodies or reasoning enter bubbles."""
    config = config or {}
    state = dict(state or {})
    state.setdefault('schema_version', 1)
    state.setdefault('design', {'completed': 0, 'total': int(config.get('task_benchmark', {}).get('max_tasks', 0))})
    state.setdefault('execution', {'completed': 0, 'arm_completed': 0, 'total': 0, 'round': 0, 'tool_calls': 0,
                                    'round_limit': int(config.get('task_benchmark', {}).get('max_rounds', 0))})
    state.setdefault('model', {'started': 0, 'completed': 0, 'failed': 0, 'state': 'idle'})
    state.setdefault('tokens', {'used': 0, 'limit': int(config.get('budget', {}).get('max_tokens', 0))})
    safe = {key: value for key, value in payload.items() if key in _PROGRESS_FIELDS and isinstance(value, (str, int, float, bool, type(None)))}
    for key in ('thinking_chars', 'content_chars', 'output_limit', 'finish_reason', 'recovery_mode', 'retry_budget'):
        if isinstance(payload.get(key), (str, int, float, bool)):
            safe[key] = payload[key]
    if payload.get('reason') in {'native_tool_output_truncated', 'oversized_native_tool_arguments', 'native_tool_output_unusable'}:
        safe['reason'] = payload['reason']
    state['heartbeat_at'] = now
    if kind == 'model_request_wait':
        if state['model'].get('request_id') == safe.get('request_id') and state['model'].get('state') in {'waiting', 'retrying'}:
            state['model']['elapsed_seconds'] = safe.get('elapsed_seconds', 0)
        return state
    state['last_activity_at'] = now
    state['last_kind'] = kind
    design, execution, model = state['design'], state['execution'], state['model']
    if kind == 'queued':
        state['stage'] = 'queued'
    elif kind == 'collecting':
        state['stage'] = 'collecting'
    elif kind.startswith('task_design'):
        state['stage'] = safe.get('operation', 'task_design')
        design.update({key: safe[key] for key in ('task_index', 'task_total', 'attempt', 'max_attempts', 'operation') if key in safe})
        if 'task_total' in safe:
            design['total'] = safe['task_total']
        if kind == 'task_design_completed':
            design['completed'] = max(int(design.get('completed', 0)), int(safe.get('task_index', 0)))
    elif kind == 'task_bank_frozen':
        design['completed'] = design['total'] = int(payload.get('train', 0)) + int(payload.get('holdout', 0))
        state['stage'] = 'task_bank_frozen'
    elif kind == 'task_budget_allocated':
        execution['planned_rollouts'] = safe.get('paired_rollouts', 0)
        state['tokens']['per_task_limit'] = safe.get('per_task_tokens', 0)
    elif kind == 'task_started':
        state['stage'] = 'task_execution'
        if execution.get('arm') != safe.get('arm'):
            execution['arm_completed'] = 0
        execution.update(safe)
        execution.update(round=0, tool_calls=0, tool_name='', action='starting')
    elif kind in {'task_round_started', 'task_round_completed', 'task_tool_started', 'task_tool_completed', 'task_checks_started'}:
        state['stage'] = 'task_checks' if kind == 'task_checks_started' else 'task_execution'
        execution.update(safe)
        execution['action'] = kind
    elif kind == 'task_completed':
        execution.update(safe)
        execution['completed'] = int(execution.get('completed', 0)) + 1
        execution['arm_completed'] = int(execution.get('arm_completed', 0)) + 1
        execution['action'] = kind
        if safe.get('stop_reason') == 'quota_exhausted':
            execution['quota_failures'] = int(execution.get('quota_failures', 0)) + 1
    elif kind == 'model_call_started':
        state['stage'] = 'baseline_review' if safe.get('stage') == 'baseline_judge' else 'judging' if safe.get('stage') == 'judge' else 'generating'
        state.update({key: safe[key] for key in ('candidate_index', 'candidate_total') if key in safe})
    elif kind == 'model_request_started':
        model.update(safe)
        model.update(state='waiting', started=int(model.get('started', 0)) + 1, started_at=now, elapsed_seconds=0, attempt=1)
    elif kind in {'model_request_retry','model_transport_recovery'}:
        model.update(safe)
        model['state'] = 'retrying'
    elif kind in {'model_phase_round_started', 'model_reasoning_continued', 'model_http_attempt_started'}:
        model.update(safe)
        model['state'] = 'waiting'
        if kind == 'model_http_attempt_started':
            model['retry_after_seconds'] = 0
    elif kind in {'model_request_completed', 'model_request_failed'}:
        if model.get('request_id') == safe.get('request_id'):
            model.update(safe)
            model['state'] = 'failed' if kind.endswith('failed') else 'completed'
            model['finished_at'] = now
        key = 'failed' if kind.endswith('failed') else 'completed'
        model[key] = int(model.get(key, 0)) + 1
    elif kind == 'token_usage':
        state['tokens'].update(safe)
    elif kind == 'model_budget_consumed':
        state['last_budget'] = {key: payload[key] for key in ('scope', 'limit', 'used', 'remaining', 'exhausted') if key in payload}
    elif kind in _TERMINAL_RUNS:
        state['stage'] = kind
        evaluations = payload.get('evaluations', [])
        if evaluations and all(row.get('code') == 'proposal_budget_exhausted' for row in evaluations):
            state['summary'] = {'code': 'proposal_budget_exhausted', 'affected_candidates': len(evaluations)}
    if kind != 'token_usage':
        state['activity'] = (state.get('activity', []) + [{'kind': kind, 'at': now, **safe}])[-40:]
    return state


def _progress_outcome(state, result):
    evaluations = result.get('evaluations', []) if isinstance(result, dict) else []
    if evaluations and all(row.get('code') == 'proposal_budget_exhausted' for row in evaluations):
        state['summary'] = {'code': 'proposal_budget_exhausted', 'affected_candidates': len(evaluations)}
    return state


def _legacy_progress(root, run, events):
    """Read old checkpoints without modifying the registry or loading user text."""
    state = {}
    for event in events:
        payload = event.get('payload', {})
        if event['kind'] == 'task_completed':
            payload = {**payload, 'round': payload.get('round', payload.get('rounds', 0))}
            if 'budget_exhausted' in str(payload.get('error', '')):
                payload = {**payload, 'stop_reason': 'quota_exhausted'}
        state = _progress_update(state, event['kind'], payload, event['created_at'], run.get('config', {}))
    state['legacy'] = True
    state['detailed_telemetry_available'] = False
    archives = list((Path(root) / 'experience' / run['run_id'] / 'model_calls').glob('*/full_history.jsonl'))
    if archives:
        # Stat only: archives may contain private requests. A file is not a
        # proof of model completion or a network heartbeat.
        state['legacy_archive_count'] = len(archives)
        state['legacy_archive_activity_at'] = max(path.stat().st_mtime for path in archives)
    return state


def read_evolution_progress(root, run_id):
    """Read-only diagnostics for existing processes; never starts a control plane."""
    root = Path(root)
    with contextlib.closing(sqlite3.connect(f'file:{(root / "registry.sqlite").resolve()}?mode=ro', uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute('SELECT run_id,status,config_json,result_json,created_at,updated_at,completed_at,error FROM runs WHERE run_id=?', (run_id,)).fetchone()
        if row is None:
            raise LiquidKernelError('run_not_found', 'evolution run not found', 404)
        run = dict(row)
        run['config'] = json.loads(run.pop('config_json'))
        result = json.loads(run.pop('result_json'))
        events = [dict(item) for item in conn.execute('SELECT kind,payload_json,created_at FROM run_events WHERE run_id=? ORDER BY event_id DESC LIMIT 200', (run_id,))][::-1]
        for event in events:
            event['payload'] = json.loads(event.pop('payload_json'))
        try:
            stored = conn.execute('SELECT state_json FROM run_progress WHERE run_id=?', (run_id,)).fetchone()
        except sqlite3.OperationalError:
            stored = None
    run['progress'] = json.loads(stored[0]) if stored else _legacy_progress(root, run, events)
    _progress_outcome(run['progress'], result)
    if run['status'] in _TERMINAL_RUNS:
        run['progress']['stage'] = run['status']
    run['server_time'] = _now()
    run.pop('config')
    return run


class LiquidKernelRegistry:
    SQLITE_CONNECTIONS_CLOSE_ON_EXIT = True

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.root, 0o700)
        except Exception:
            pass
        self.artifacts_root = self.root / "artifacts"
        self.candidates_root = self.root / "candidates"
        self.experience_root = self.root / "experience"
        self.backups_root = self.root / "backups"
        for path in (self.artifacts_root, self.candidates_root, self.experience_root, self.backups_root):
            path.mkdir(parents=True, exist_ok=True)
            try:
                os.chmod(path, 0o700)
            except Exception:
                pass
        self.db_path = self.root / "registry.sqlite"
        self.active_path = self.root / "active.json"
        self.signing_key_path = self.root / ".artifact_signing_key"
        self.lock = threading.RLock()
        self.signing_key = self._load_signing_key()
        self._init_db()
        self.bootstrap_baseline()

    def _load_signing_key(self) -> bytes:
        if self.signing_key_path.exists():
            try:
                return bytes.fromhex(self.signing_key_path.read_text(encoding="utf-8").strip())
            except Exception:
                pass
        key = os.urandom(32)
        self.signing_key_path.write_text(key.hex(), encoding="utf-8")
        try:
            os.chmod(self.signing_key_path, 0o600)
        except Exception:
            pass
        return key

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30, factory=_ClosingSQLiteConnection)
        try:
            conn.row_factory = sqlite3.Row
        except BaseException:
            conn.close()
            raise
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS schema_meta(version INTEGER NOT NULL);
                INSERT INTO schema_meta(version) SELECT 0 WHERE NOT EXISTS(SELECT 1 FROM schema_meta);
                CREATE TABLE IF NOT EXISTS versions(
                    version TEXT PRIMARY KEY,parent_version TEXT NOT NULL,status TEXT NOT NULL,
                    source_hash TEXT NOT NULL,manifest_json TEXT NOT NULL,changelog TEXT NOT NULL,
                    hard_score REAL NOT NULL DEFAULT 0,soft_score REAL NOT NULL DEFAULT 0,
                    mixed_score REAL NOT NULL DEFAULT 0,created_at REAL NOT NULL,promoted_at REAL NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS runs(
                    run_id TEXT PRIMARY KEY,mode TEXT NOT NULL,status TEXT NOT NULL,trigger_kind TEXT NOT NULL,
                    incumbent_version TEXT NOT NULL,candidate_version TEXT NOT NULL DEFAULT '',
                    config_json TEXT NOT NULL,experience_json TEXT NOT NULL DEFAULT '{}',proposal_json TEXT NOT NULL DEFAULT '{}',
                    result_json TEXT NOT NULL DEFAULT '{}',error TEXT NOT NULL DEFAULT '',created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,completed_at REAL NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS run_events(
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,run_id TEXT NOT NULL,kind TEXT NOT NULL,
                    payload_json TEXT NOT NULL,previous_hash TEXT NOT NULL,event_hash TEXT NOT NULL,created_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS candidate_evaluations(
                    version TEXT PRIMARY KEY,run_id TEXT NOT NULL,evaluation_json TEXT NOT NULL,updated_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS run_progress(run_id TEXT PRIMARY KEY,state_json TEXT NOT NULL,updated_at REAL NOT NULL);
                CREATE INDEX IF NOT EXISTS run_events_run_id ON run_events(run_id,event_id);
                CREATE TABLE IF NOT EXISTS deployments(
                    deployment_id TEXT PRIMARY KEY,version TEXT NOT NULL,previous_version TEXT NOT NULL,
                    status TEXT NOT NULL,stage_percent INTEGER NOT NULL,metrics_json TEXT NOT NULL,
                    created_at REAL NOT NULL,updated_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS notice_ack(
                    user_id TEXT NOT NULL,device_id TEXT NOT NULL,surface TEXT NOT NULL,version TEXT NOT NULL,
                    acknowledged_at REAL NOT NULL,PRIMARY KEY(user_id,device_id,surface,version)
                );
                UPDATE schema_meta SET version=1;
                """
            )

    def _sign(self, manifest: dict) -> str:
        return hmac.new(self.signing_key, utf8_bytes(_json(manifest)), hashlib.sha256).hexdigest()

    def _manifest(
        self,
        version: str,
        parent: str,
        source_hash: str,
        *,
        mode: str,
        source: str,
        files: dict[str, str] | None = None,
    ) -> dict:
        base = {
            "schema_version": 1,
            "contract_version": KERNEL_CONTRACT_VERSION,
            "version": version,
            "parent_version": parent,
            "source_hash": source_hash,
            "mode": mode,
            "source": source,
            "created_at": _now(),
        }
        if files:
            base["files"] = _kernel_file_hashes(files)
        base["signature"] = self._sign(base)
        return base

    def bootstrap_baseline(self) -> str:
        with self.lock, self._connect() as conn:
            existing = conn.execute("SELECT version FROM versions ORDER BY created_at LIMIT 1").fetchone()
            if existing:
                if not self.active_path.exists():
                    _atomic_json(self.active_path, {"version": str(existing[0]), "canary": None})
                return str(existing[0])
            files = dict(BASELINE_KERNEL_FILES)
            source_hash = _kernel_bundle_hash(files)
            version = f"kernel-0001-baseline-{source_hash[:8]}"
            target = self.artifacts_root / version
            target.mkdir(parents=True, exist_ok=False)
            for path, source in files.items():
                (target / path).write_text(utf8_text(source), encoding="utf-8")
            manifest = self._manifest(
                version,
                "",
                source_hash,
                mode="baseline",
                source="bootstrap",
                files=files,
            )
            _atomic_json(target / "manifest.json", manifest)
            (target / "CHANGELOG.md").write_text("# Baseline\n\nInitial extracted liquid-kernel compatibility layer.\n", encoding="utf-8")
            conn.execute(
                "INSERT INTO versions(version,parent_version,status,source_hash,manifest_json,changelog,created_at,promoted_at) VALUES(?,?,?,?,?,?,?,?)",
                (version, "", "active", source_hash, _json(manifest), "Initial extracted liquid-kernel compatibility layer.", _now(), _now()),
            )
            _atomic_json(self.active_path, {"version": version, "canary": None})
            return version

    def active_state(self) -> dict:
        state = _read_json(self.active_path, {})
        version = str(state.get("version", "") or "")
        if not version:
            version = self.bootstrap_baseline()
        return {"version": version, "canary": state.get("canary") if isinstance(state.get("canary"), dict) else None}

    def active_version(self) -> str:
        return str(self.active_state()["version"])

    def lineage_versions(self, version: str = "", history_depth: int = 2) -> list[str]:
        current = str(version or self.active_version())
        depth = max(0, min(12, int(history_depth or 0)))
        versions: list[str] = []
        with self._connect() as conn:
            while current and len(versions) < depth + 1:
                versions.append(current)
                row = conn.execute("SELECT parent_version FROM versions WHERE version=?", (current,)).fetchone()
                current = str(row[0] if row else "")
        return versions

    def choose_version(self, user_id: str, session_id: str) -> str:
        state = self.active_state()
        canary = state.get("canary")
        if not isinstance(canary, dict):
            return str(state["version"])
        candidate = str(canary.get("version", "") or "")
        percent = max(0, min(100, int(canary.get("percent", 0) or 0)))
        if not candidate or percent <= 0:
            return str(state["version"])
        bucket = int(hashlib.sha256(utf8_bytes(f"{user_id}|{session_id}|{candidate}")).hexdigest()[:8], 16) % 100
        return candidate if bucket < percent else str(state["version"])

    def artifact(self, version: str) -> KernelArtifact:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM versions WHERE version=?", (str(version),)).fetchone()
        if not row:
            raise LiquidKernelError("version_not_found", "kernel version not found", 404)
        path = self.artifacts_root / str(row["version"])
        manifest = _read_json(path / "manifest.json", {})
        signature = str(manifest.pop("signature", "") or "")
        if not signature or not hmac.compare_digest(signature, self._sign(manifest)):
            raise LiquidKernelError("artifact_signature_invalid", "kernel artifact signature is invalid", 409)
        manifest["signature"] = signature
        manifest_files = manifest.get("files") if isinstance(manifest.get("files"), dict) else {}
        if manifest_files:
            files: dict[str, str] = {}
            for relative_path, expected_hash in manifest_files.items():
                relative = str(relative_path or "")
                file_path = path / relative
                if not relative or not file_path.is_file():
                    raise LiquidKernelError("artifact_hash_invalid", "kernel artifact file is missing", 409)
                source = file_path.read_text(encoding="utf-8")
                if _sha256_bytes(utf8_bytes(source)) != str(expected_hash or ""):
                    raise LiquidKernelError("artifact_hash_invalid", "kernel artifact file hash is invalid", 409)
                files[relative] = source
            if _kernel_bundle_hash(files) != str(row["source_hash"]):
                raise LiquidKernelError("artifact_hash_invalid", "kernel artifact bundle hash is invalid", 409)
        else:
            kernel_path = path / "kernel.py"
            if _sha256_bytes(kernel_path.read_bytes()) != str(row["source_hash"]):
                raise LiquidKernelError("artifact_hash_invalid", "kernel artifact source hash is invalid", 409)
        return KernelArtifact(str(row["version"]), str(row["parent_version"]), path, str(row["source_hash"]), str(row["status"]))

    def list_versions(self, limit: int = 100, offset: int = 0) -> dict:
        with self._connect() as conn:
            total = int(conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0])
            rows = [dict(row) for row in conn.execute(
                "SELECT version,parent_version,status,source_hash,changelog,hard_score,soft_score,mixed_score,created_at,promoted_at FROM versions ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (max(1, min(500, int(limit))), max(0, int(offset))),
            ).fetchall()]
        for row in rows:
            with self._connect() as conn:
                saved = conn.execute('SELECT run_id,evaluation_json FROM candidate_evaluations WHERE version=?', (row['version'],)).fetchone()
            if saved:
                evaluation = json.loads(saved['evaluation_json'])
                row.update(run_id=saved['run_id'], deployment_eligible=evaluation.get('deployment_eligible', False),
                           score_status=(evaluation.get('candidate') or {}).get('score_status', 'pending_evaluation'))
                for key in ('hard', 'soft', 'mixed'):
                    row[key + '_score'] = (evaluation.get('candidate') or {}).get(key)
        return {"versions": rows, "total": total, "active": self.active_state()}

    def version_detail(self, version: str) -> dict:
        self.artifact(version)
        with self._connect() as conn:
            row = dict(conn.execute("SELECT * FROM versions WHERE version=?", (version,)).fetchone())
            deployments = [dict(item) for item in conn.execute(
                "SELECT * FROM deployments WHERE version=? ORDER BY created_at DESC", (version,)
            ).fetchall()]
        row["manifest"] = json.loads(row.pop("manifest_json", "{}") or "{}")
        row["deployments"] = deployments
        row["sources"] = self.sources(version)
        row["source"] = row["sources"]["kernel.py"]
        with self._connect() as conn:
            saved = conn.execute('SELECT run_id,evaluation_json FROM candidate_evaluations WHERE version=?', (version,)).fetchone()
        if saved:
            row['run_id'] = saved['run_id']
            row['evaluation'] = json.loads(saved['evaluation_json'])
        return row

    def source(self, version: str) -> str:
        return self.sources(version)["kernel.py"]

    def sources(self, version: str) -> dict[str, str]:
        artifact = self.artifact(version)
        manifest = _read_json(artifact.path / "manifest.json", {})
        manifest_files = manifest.get("files") if isinstance(manifest.get("files"), dict) else {}
        paths = sorted(str(path) for path in manifest_files) if manifest_files else ["kernel.py"]
        return {path: (artifact.path / path).read_text(encoding="utf-8") for path in paths}

    def diff(self, version: str) -> dict:
        import difflib

        detail = self.version_detail(version)
        parent = str(detail.get("parent_version", "") or "")
        before_files = self.sources(parent) if parent else {}
        after_files = detail.get("sources", {}) if isinstance(detail.get("sources"), dict) else {}
        chunks: list[str] = []
        for path in sorted(set(before_files) | set(after_files)):
            before = str(before_files.get(path, "") or "").splitlines()
            after = str(after_files.get(path, "") or "").splitlines()
            chunks.extend(difflib.unified_diff(
                before,
                after,
                fromfile=f"{parent or '/dev/null'}/{path}",
                tofile=f"{version}/{path}",
                lineterm="",
            ))
        return {
            "version": version,
            "parent_version": parent,
            "diff": "\n".join(chunks),
        }

    def register_candidate(self, run_id: str, parent: str, source: str | dict[str, str], *, mode: str, changelog: str, scores: dict, evaluation: dict | None = None) -> str:
        files = _normalize_kernel_files(source)
        digest = _kernel_bundle_hash(files)
        with self._connect() as conn:
            sequence = int(conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0]) + 1
        version = f"kernel-{sequence:04d}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{digest[:8]}"
        staging = self.candidates_root / run_id / version
        staging.mkdir(parents=True, exist_ok=False)
        for path, file_source in files.items():
            (staging / path).write_text(utf8_text(file_source), encoding="utf-8")
        manifest = self._manifest(
            version,
            parent,
            digest,
            mode=mode,
            source=f"evolution:{run_id}",
            files=files,
        )
        _atomic_json(staging / "manifest.json", manifest)
        (staging / "CHANGELOG.md").write_text(utf8_text(changelog or "Candidate kernel update."), encoding="utf-8")
        target = self.artifacts_root / version
        os.replace(staging, target)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO versions(version,parent_version,status,source_hash,manifest_json,changelog,hard_score,soft_score,mixed_score,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (version, parent, "candidate", digest, _json(manifest), str(changelog or ""), float(scores.get("hard", 0)), float(scores.get("soft", 0)), float(scores.get("mixed", 0)), _now()),
            )
        if evaluation is not None:
            self.record_candidate_evaluation(version, evaluation, run_id=run_id)
        return version

    def record_candidate_evaluation(self, version, evaluation, *, run_id=''):
        if not version:
            return
        with self._connect() as conn:
            previous = conn.execute('SELECT run_id,evaluation_json FROM candidate_evaluations WHERE version=?', (version,)).fetchone()
            prior = json.loads(previous['evaluation_json']) if previous else {}
            record = {**prior, **evaluation}
            # This flag is computed by protected control code, never a model.
            flow = record.get('flow_comparison') or {}
            confirmation = record.get('confirmation') or {}
            eligible = (record.get('decision') == 'promote' and flow.get('eligible') is True
                        and confirmation.get('completed') is True and confirmation.get('passed') is True
                        and float(record.get('gain', 0)) > 0)
            record['deployment_eligible'] = bool(eligible)
            state = 'candidate' if eligible else 'rejected' if record.get('decision') in {'reject', 'rejected'} else 'evaluating'
            scores = record.get('candidate') or {}
            conn.execute('INSERT OR REPLACE INTO candidate_evaluations VALUES(?,?,?,?)',
                         (version, run_id or (previous['run_id'] if previous else ''), _json(record), _now()))
            conn.execute('UPDATE versions SET status=?,hard_score=?,soft_score=?,mixed_score=? WHERE version=? AND promoted_at=0 AND status NOT IN (\'canary\',\'active\')',
                         (state, float(scores.get('hard') or 0), float(scores.get('soft') or 0), float(scores.get('mixed') or 0), version))

    def _require_candidate_eligible(self, version):
        with self._connect() as conn:
            row = conn.execute('SELECT evaluation_json,run_id FROM candidate_evaluations WHERE version=?', (version,)).fetchone()
        if row:
            with self._connect() as conn:
                run = conn.execute('SELECT status FROM runs WHERE run_id=?', (row['run_id'],)).fetchone()
            if json.loads(row['evaluation_json']).get('deployment_eligible') is True and run and run['status'] not in {'failed', 'cancelled', 'rejected'}:
                return
            raise LiquidKernelError('candidate_not_eligible', 'Retained candidate has not passed real evaluation and independent confirmation', 409)

    def begin_canary(self, version: str, percent: int = 5) -> dict:
        self._require_candidate_eligible(version)
        artifact = self.artifact(version)
        active = self.active_state()
        existing_canary = active.get("canary") if isinstance(active.get("canary"), dict) else None
        if existing_canary and str(existing_canary.get("version", "") or "") != artifact.version:
            raise LiquidKernelError("canary_in_progress", "another kernel version is already in Canary", 409)
        current = str(active.get("version", "") or self.active_version())
        if artifact.version == current:
            return self.active_state()
        deployment_id = "deploy_" + uuid.uuid4().hex
        now = _now()
        state = {"version": current, "canary": {"version": artifact.version, "percent": int(percent), "deployment_id": deployment_id, "started_at": now}}
        _atomic_json(self.active_path, state)
        with self._connect() as conn:
            conn.execute("UPDATE versions SET status='canary' WHERE version=?", (artifact.version,))
            conn.execute(
                "INSERT INTO deployments(deployment_id,version,previous_version,status,stage_percent,metrics_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
                (deployment_id, artifact.version, current, "canary", int(percent), "{}", now, now),
            )
        return state

    def abort_canary(self, *, reason: str = "") -> dict:
        state = self.active_state()
        incumbent = str(state.get("version", "") or "")
        canary = state.get("canary") if isinstance(state.get("canary"), dict) else None
        if not canary:
            return {"ok": True, "aborted": False, "version": incumbent}
        candidate = str(canary.get("version", "") or "")
        deployment_id = str(canary.get("deployment_id", "") or "")
        now = _now()
        _atomic_json(
            self.active_path,
            {
                "version": incumbent,
                "canary": None,
                "rollback": {"from": candidate, "to": incumbent, "reason": str(reason or "canary aborted"), "at": now},
            },
        )
        with self._connect() as conn:
            if candidate:
                conn.execute("UPDATE versions SET status='rolled_back' WHERE version=? AND status='canary'", (candidate,))
                conn.execute(
                    "UPDATE runs SET status='rolled_back',error=?,updated_at=?,completed_at=? WHERE candidate_version=? AND status='canary'",
                    (str(reason or "canary aborted"), now, now, candidate),
                )
            if deployment_id:
                conn.execute(
                    "UPDATE deployments SET status='rolled_back',updated_at=? WHERE deployment_id=?",
                    (now, deployment_id),
                )
        return {
            "ok": True,
            "aborted": True,
            "version": incumbent,
            "rolled_back_from": candidate,
            "reason": str(reason or "canary aborted"),
            "at": now,
        }

    def promote(self, version: str) -> dict:
        self._require_candidate_eligible(version)
        artifact = self.artifact(version)
        state = self.active_state()
        canary = state.get("canary") if isinstance(state.get("canary"), dict) else None
        if not canary or str(canary.get("version", "") or "") != artifact.version or int(canary.get("percent", 0) or 0) < 100:
            raise LiquidKernelError("canary_incomplete", "kernel must complete the 100% Canary stage before promotion", 409)
        previous = self.active_version()
        now = _now()
        _atomic_json(self.active_path, {"version": artifact.version, "canary": None})
        with self._connect() as conn:
            conn.execute("UPDATE versions SET status='archived' WHERE status='active' AND version<>?", (artifact.version,))
            conn.execute("UPDATE versions SET status='active',promoted_at=? WHERE version=?", (now, artifact.version))
            conn.execute("UPDATE deployments SET status='promoted',stage_percent=100,updated_at=? WHERE version=? AND status='canary'", (now, artifact.version))
            conn.execute(
                "UPDATE runs SET status='promoted',updated_at=?,completed_at=? WHERE candidate_version=? AND status='canary'",
                (now, now, artifact.version),
            )
        backup = self.backups_root / artifact.version
        if not backup.exists():
            shutil.copytree(artifact.path, backup)
        return {"ok": True, "version": artifact.version, "previous_version": previous, "promoted_at": now}

    def rollback(self, target_version: str = "", *, reason: str = "") -> dict:
        state = self.active_state()
        current = str(state["version"])
        if target_version:
            with self._connect() as conn:
                prior = conn.execute('SELECT promoted_at FROM versions WHERE version=?', (target_version,)).fetchone()
            if not prior or not prior['promoted_at']:
                raise LiquidKernelError('rollback_unavailable', 'Rollback requires a previously active kernel version', 409)
        if isinstance(state.get("canary"), dict):
            if not target_version or str(target_version) == current:
                return self.abort_canary(reason=reason or "manual Canary rollback")
            self.abort_canary(reason=reason or "manual Canary rollback before version rollback")
        if not target_version:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT parent_version FROM versions WHERE version=?", (current,)
                ).fetchone()
            target_version = str(row[0] if row else "")
        if not target_version:
            raise LiquidKernelError("rollback_unavailable", "the active kernel has no parent version", 409)
        artifact = self.artifact(target_version)
        now = _now()
        _atomic_json(self.active_path, {"version": artifact.version, "canary": None, "rollback": {"from": current, "reason": reason, "at": now}})
        with self._connect() as conn:
            conn.execute("UPDATE versions SET status='rolled_back' WHERE version=?", (current,))
            conn.execute("UPDATE versions SET status='active',promoted_at=? WHERE version=?", (now, artifact.version))
            conn.execute("UPDATE deployments SET status='rolled_back',updated_at=? WHERE status='canary' OR version=?", (now, current))
        return {"ok": True, "version": artifact.version, "rolled_back_from": current, "reason": reason, "at": now}

    @staticmethod
    def _p95(values: list[float]) -> float:
        if not values:
            return 0.0
        ordered = sorted(max(0.0, float(value)) for value in values)
        index = min(len(ordered) - 1, max(0, int((len(ordered) * 0.95) - 1)))
        return float(ordered[index])

    def observe_session_result(
        self,
        version: str,
        *,
        success: bool,
        duration_seconds: float,
        error: bool = False,
        canary_policy: dict | None = None,
    ) -> dict:
        state = self.active_state()
        canary = state.get("canary")
        if not isinstance(canary, dict):
            return {"ok": True, "observed": False}
        candidate = str(canary.get("version", "") or "")
        incumbent = str(state.get("version", "") or "")
        version = str(version or incumbent)
        if version not in {candidate, incumbent}:
            return {"ok": True, "observed": False}
        deployment_id = str(canary.get("deployment_id", "") or "")
        with self.lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM deployments WHERE deployment_id=?", (deployment_id,)).fetchone()
            if not row or str(row["status"]) != "canary":
                return {"ok": True, "observed": False}
            metrics = json.loads(str(row["metrics_json"] or "{}"))
            bucket = metrics.setdefault(version, {"completed": 0, "success": 0, "errors": 0, "durations": []})
            bucket["completed"] = int(bucket.get("completed", 0) or 0) + 1
            bucket["success"] = int(bucket.get("success", 0) or 0) + int(bool(success))
            bucket["errors"] = int(bucket.get("errors", 0) or 0) + int(bool(error))
            durations = [float(item) for item in bucket.get("durations", []) if isinstance(item, (int, float))][-499:]
            durations.append(max(0.0, float(duration_seconds or 0.0)))
            bucket["durations"] = durations
            now = _now()
            conn.execute("UPDATE deployments SET metrics_json=?,updated_at=? WHERE deployment_id=?", (_json(metrics), now, deployment_id))
        candidate_metrics = metrics.get(candidate, {})
        incumbent_metrics = metrics.get(incumbent, {})
        candidate_count = int(candidate_metrics.get("completed", 0) or 0)
        incumbent_count = int(incumbent_metrics.get("completed", 0) or 0)
        if candidate_count <= 0 or incumbent_count <= 0:
            return {"ok": True, "observed": True, "metrics": metrics}
        candidate_success = float(candidate_metrics.get("success", 0) or 0) / candidate_count
        incumbent_success = float(incumbent_metrics.get("success", 0) or 0) / incumbent_count
        candidate_errors = float(candidate_metrics.get("errors", 0) or 0) / candidate_count
        incumbent_errors = float(incumbent_metrics.get("errors", 0) or 0) / incumbent_count
        candidate_p95 = self._p95(candidate_metrics.get("durations", []))
        incumbent_p95 = self._p95(incumbent_metrics.get("durations", []))
        policy = canary_policy if isinstance(canary_policy, dict) else default_evolution_config()["canary"]
        regression = candidate_count >= 5 and incumbent_count >= 5 and (
            candidate_success < incumbent_success - float(policy.get("success_drop_limit", 0.05) or 0.05)
            or candidate_errors > incumbent_errors + float(policy.get("error_increase_limit", 0.05) or 0.05)
            or (
                incumbent_p95 > 0
                and candidate_p95 > incumbent_p95 * (1.0 + float(policy.get("p95_latency_increase_limit", 0.20) or 0.20))
            )
        )
        comparison = {
            "candidate_success": candidate_success,
            "incumbent_success": incumbent_success,
            "candidate_error_rate": candidate_errors,
            "incumbent_error_rate": incumbent_errors,
            "candidate_p95_seconds": candidate_p95,
            "incumbent_p95_seconds": incumbent_p95,
        }
        if regression:
            rollback = self.abort_canary(reason="automatic canary regression threshold")
            return {"ok": True, "observed": True, "action": "rolled_back", "comparison": comparison, "rollback": rollback}
        stage = int(canary.get("percent", 5) or 5)
        stages = [int(item) for item in policy.get("stages", [5, 25, 100]) if int(item) in {5, 25, 100}]
        stages = stages or [5, 25, 100]
        stage_index = stages.index(stage) if stage in stages else 0
        minimum_completed = [max(0, int(item)) for item in policy.get("minimum_completed", [20, 50, 0])]
        minimum_hours = [max(0, int(item)) for item in policy.get("minimum_hours", [24, 48, 0])]
        required_count = minimum_completed[stage_index] if stage_index < len(minimum_completed) else 0
        required_hours = minimum_hours[stage_index] if stage_index < len(minimum_hours) else 0
        elapsed_hours = max(0.0, (_now() - float(canary.get("started_at", 0) or 0)) / 3600.0)
        if candidate_count >= required_count and elapsed_hours >= required_hours:
            if stage_index >= len(stages) - 1:
                promoted = self.promote(candidate)
                return {"ok": True, "observed": True, "action": "promoted", "comparison": comparison, "promotion": promoted}
            next_stage = stages[stage_index + 1]
            canary["percent"] = next_stage
            canary["started_at"] = _now()
            _atomic_json(self.active_path, {"version": incumbent, "canary": canary})
            with self._connect() as conn:
                conn.execute("UPDATE deployments SET stage_percent=?,updated_at=? WHERE deployment_id=?", (next_stage, _now(), deployment_id))
            return {"ok": True, "observed": True, "action": "advanced", "percent": next_stage, "comparison": comparison}
        return {"ok": True, "observed": True, "action": "continue", "comparison": comparison, "metrics": metrics}

    def notice(self, user_id: str, device_id: str, surface: str) -> dict | None:
        version = self.active_version()
        with self._connect() as conn:
            acknowledged = conn.execute(
                "SELECT 1 FROM notice_ack WHERE user_id=? AND device_id=? AND surface=? AND version=?",
                (str(user_id), str(device_id), str(surface), version),
            ).fetchone()
            row = conn.execute("SELECT version,parent_version,changelog,mixed_score,promoted_at FROM versions WHERE version=?", (version,)).fetchone()
        if acknowledged or not row or not str(row["parent_version"] or "") or float(row["promoted_at"] or 0) <= 0:
            return None
        state = self.active_state()
        return {
            "version": version,
            "changelog": str(row["changelog"] or ""),
            "score": float(row["mixed_score"] or 0),
            "promoted_at": float(row["promoted_at"] or 0),
            "canary": state.get("canary"),
            "rollback": state.get("rollback") if isinstance(state.get("rollback"), dict) else None,
        }

    def acknowledge_notice(self, user_id: str, device_id: str, surface: str, version: str) -> dict:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO notice_ack(user_id,device_id,surface,version,acknowledged_at) VALUES(?,?,?,?,?)",
                (str(user_id), str(device_id), str(surface), str(version), _now()),
            )
        return {"ok": True, "version": str(version)}

    def create_run(self, config: dict, trigger_kind: str) -> str:
        run_id = "evo_" + uuid.uuid4().hex
        now = _now()
        incumbent = self.active_version()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO runs(run_id,mode,status,trigger_kind,incumbent_version,config_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
                (run_id, config["mode"], "queued", str(trigger_kind), incumbent, _json(config), now, now),
            )
            self._event(conn, run_id, "queued", {"mode": config["mode"], "incumbent_version": incumbent, "trigger": trigger_kind})
        return run_id

    def update_run(self, run_id: str, status: str, **fields: Any) -> None:
        allowed = {"candidate_version", "experience_json", "proposal_json", "result_json", "error", "completed_at"}
        assignments = ["status=?", "updated_at=?"]
        values: list[Any] = [str(status), _now()]
        for key, value in fields.items():
            if key not in allowed:
                continue
            assignments.append(f"{key}=?")
            values.append(_json(value) if key.endswith("_json") and not isinstance(value, str) else value)
        values.append(run_id)
        with self._connect() as conn:
            conn.execute(f"UPDATE runs SET {','.join(assignments)} WHERE run_id=?", values)

    def event(self, run_id: str, kind: str, payload: dict) -> None:
        with self.lock, self._connect() as conn:
            if kind in _PROGRESS_TRANSIENT:
                self._save_progress(conn, run_id, kind, payload)
            else:
                self._event(conn, run_id, kind, payload)

    def _save_progress(self, conn, run_id, kind, payload):
        run = conn.execute("SELECT config_json FROM runs WHERE run_id=?", (run_id,)).fetchone()
        if not run:
            return
        row = conn.execute("SELECT state_json FROM run_progress WHERE run_id=?", (run_id,)).fetchone()
        now = _now()
        state = _progress_update(json.loads(row[0]) if row else {}, kind, payload, now, json.loads(run[0]))
        state['detailed_telemetry_available'] = True
        conn.execute("INSERT OR REPLACE INTO run_progress(run_id,state_json,updated_at) VALUES(?,?,?)", (run_id, _json(state), now))
        if kind != 'model_request_wait':
            conn.execute("UPDATE runs SET updated_at=? WHERE run_id=?", (now, run_id))

    def _event(self, conn, run_id: str, kind: str, payload: dict) -> None:
        now = _now()
        self._save_progress(conn, run_id, kind, payload)
        previous = conn.execute("SELECT event_hash FROM run_events ORDER BY event_id DESC LIMIT 1").fetchone()
        previous_hash = str(previous[0] if previous else "")
        material = _json({"run_id": run_id, "kind": kind, "payload": payload, "previous_hash": previous_hash, "created_at": now})
        event_hash = hashlib.sha256(utf8_bytes(material)).hexdigest()
        conn.execute(
            "INSERT INTO run_events(run_id,kind,payload_json,previous_hash,event_hash,created_at) VALUES(?,?,?,?,?,?)",
            (run_id, kind, _json(payload), previous_hash, event_hash, now),
        )

    def events_since(self, after_event_id: int = 0, limit: int = 200) -> dict:
        with self._connect() as conn:
            rows = [dict(row) for row in conn.execute(
                "SELECT event_id,run_id,kind,payload_json,previous_hash,event_hash,created_at FROM run_events WHERE event_id>? ORDER BY event_id LIMIT ?",
                (max(0, int(after_event_id or 0)), max(1, min(1000, int(limit or 200)))),
            ).fetchall()]
        for row in rows:
            row["payload"] = json.loads(row.pop("payload_json", "{}") or "{}")
        return {"events": rows, "last_event_id": int(rows[-1]["event_id"] if rows else after_event_id or 0)}

    def run_detail(self, run_id: str, event_limit: int = 200) -> dict:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
            if not row:
                raise LiquidKernelError("run_not_found", "evolution run not found", 404)
            events = [dict(item) for item in conn.execute(
                "SELECT event_id,kind,payload_json,event_hash,created_at FROM run_events WHERE run_id=? ORDER BY event_id DESC LIMIT ?", (run_id, max(1, min(1000, int(event_limit))))
            ).fetchall()]
        out = dict(row)
        for key in ("config_json", "experience_json", "proposal_json", "result_json"):
            out[key[:-5]] = json.loads(out.pop(key, "{}") or "{}")
        for event in events:
            event["payload"] = json.loads(event.pop("payload_json", "{}") or "{}")
        out["events"] = list(reversed(events))
        with self._connect() as conn:
            stored = conn.execute("SELECT state_json FROM run_progress WHERE run_id=?", (run_id,)).fetchone()
            total = conn.execute("SELECT COUNT(*) FROM run_events WHERE run_id=?", (run_id,)).fetchone()[0]
        out['progress'] = json.loads(stored[0]) if stored else _legacy_progress(self.root, out, out['events'])
        _progress_outcome(out['progress'], out.get('result', {}))
        out['events_total'] = total
        out['events_truncated'] = total > len(events)
        if out['status'] in _TERMINAL_RUNS:
            out['progress']['stage'] = out['status']
        result = out.get('result') or {}
        failure = result.get('details') or {}
        if result.get('code') == 'model_call_failed' and failure.get('reason') == 'model request total deadline exhausted':
            # Diagnose historical generic-client errors without rewriting history.
            failure.update(error_code='request_deadline_exhausted', status_origin='client', http_status=0)
            for item in out['progress'].get('activity', []):
                if item.get('kind') in {'model_transport_error', 'model_request_failed'}:
                    item.update(error_code='request_deadline_exhausted', status_origin='client', http_status=0)
            out['progress'].get('model', {}).update(error_code='request_deadline_exhausted')
            retry = next((item for item in reversed(out['progress'].get('activity', [])) if item.get('kind') == 'model_request_retry' and item.get('http_status')), {})
            if retry:
                failure.update(last_http_status=retry['http_status'], cause_code='model_rate_limited' if retry['http_status'] == 429 else 'model_http_error')
                for item in out['progress'].get('activity', []):
                    if item.get('kind') in {'model_transport_error', 'model_request_failed'}:
                        item.update(last_http_status=failure['last_http_status'], cause_code=failure['cause_code'])
        baseline = result.get('incumbent') or {}
        if 'hard' not in baseline:
            path = (self.experience_root / str(run_id) / 'incumbent_rollouts.json').resolve()
            if path.is_relative_to(self.experience_root.resolve()) and path.is_file() and path.stat().st_size <= 16_000_000:
                stat = path.stat()
                cache_key = (str(path), stat.st_mtime_ns, stat.st_size)
                cache = getattr(self, '_score_summary_cache', {})
                if cache_key not in cache:
                    archived = _read_json(path, {})
                    cache[cache_key] = {key: archived[key] for key in ('score', 'success_rate') if key in archived}
                    if len(cache) > 64:
                        cache.pop(next(iter(cache)))
                    self._score_summary_cache = cache
                saved = cache[cache_key]
                if 'score' in saved:
                    baseline = {'hard': saved['score'], 'success_rate': saved.get('success_rate')}
        if 'hard' not in baseline:
            # Older interrupted runs persisted completed task events before
            # they persisted the arm. Recover only those measured scores in
            # the read-only view; no review/composite score can be inferred.
            with self._connect() as conn:
                completed = conn.execute("SELECT payload_json FROM run_events WHERE run_id=? AND kind='task_completed' ORDER BY event_id", (run_id,)).fetchall()
            measured = {}
            for record in completed:
                item = json.loads(record[0])
                score = item.get('score')
                if item.get('arm') == 'incumbent' and isinstance(score, (int, float)) and not isinstance(score, bool) and math.isfinite(score) and 0 <= score <= 100:
                    measured[item['task_id']] = item
            if measured:
                baseline = {'hard': sum(item['score'] for item in measured.values()) / len(measured),
                            'completed_tasks': len(measured), 'expected_tasks': max(item.get('task_total', len(measured)) for item in measured.values()),
                            'score_status': 'partial', 'task_execution_measured': True, 'score_source': 'completed_task_events'}
        evaluations = result.get('evaluations') or []
        validation_codes = {'mutable_surface_violation', 'patch_too_large', 'kernel_contract_missing', 'empty_patch',
                            'forbidden_import', 'forbidden_name', 'forbidden_scope', 'forbidden_decorator',
                            'forbidden_attribute', 'forbidden_call', 'patch_context_missing', 'invalid_patch_syntax',
                            'duplicate_patch_file', 'invalid_patch_operation', 'task_specific_policy'}
        views = []
        for item in evaluations:
            view = {key: item.get(key) for key in ('candidate_index', 'candidate_version', 'decision', 'code', 'reason', 'flow_comparison', 'confirmation', 'opportunity_audit')}
            view['incumbent'] = item.get('incumbent') or baseline
            view['candidate'] = item.get('candidate') or {}
            if not view['candidate'] and item.get('code') in validation_codes:
                view['candidate'] = {'hard': None, 'soft': None, 'mixed': 0.0, 'validation': 0,
                                     'score_status': 'validation_failed', 'task_execution_measured': False}
            views.append(view)
        evaluated = next((item for item in reversed(views) if item['candidate']), {})
        candidate = result.get('candidate') or evaluated.get('candidate') or {}
        out['score_summary'] = {'incumbent': baseline, 'candidate': candidate,
                                'review_completed': candidate.get('soft') is not None,
                                'evaluations': views}
        valid = result.get('code') != 'invalid_evaluation_definition'
        bank_path = (self.experience_root / str(run_id) / 'task_bank.json').resolve()
        if bank_path.is_relative_to(self.experience_root.resolve()) and bank_path.is_file():
            stat = bank_path.stat()
            cache_key = (str(bank_path), stat.st_mtime_ns, stat.st_size)
            cache = getattr(self, '_evaluator_definition_cache', {})
            if cache_key not in cache:
                bank_valid = stat.st_size <= 16_000_000
                bank = {}
                try:
                    bank = _read_json(bank_path, {}) if bank_valid else {}
                    for task in bank.get('tasks', []):
                        for check in task.get('checks', []):
                            if check.get('kind') == 'command':
                                normalized = normalize_executable_command(check.get('command', ''), check.get('language', ''), validate_shell=True)
                                bank_valid &= normalized['command'] == check.get('command')
                except (ValueError, OSError, subprocess.SubprocessError):
                    bank_valid = False
                cache[cache_key] = {'valid': bool(bank_valid), 'minimum_calls': {task.get('id'): task.get('minimum_tool_calls', 0) for task in bank.get('tasks', [])}}
                if len(cache) > 64:
                    cache.pop(next(iter(cache)))
                self._evaluator_definition_cache = cache
            valid &= cache[cache_key]['valid']
            if result.get('scoring_protocol_version', 1) < SCORING_PROTOCOL_VERSION:
                legacy_rows = [row for evaluation in evaluations for row in evaluation.get('task_results', [])]
                biased = [row['task_id'] for row in legacy_rows if row.get('score') == 0 and not row.get('error')
                          and 0 < row.get('tool_calls', 0) < cache[cache_key]['minimum_calls'].get(row.get('task_id'), 0)
                          and row.get('checks') and all(check.get('ok') for check in row['checks'])]
                if biased:
                    valid = False
                    out['score_summary']['scoring_issue'] = {'code': 'legacy_tool_count_floor', 'task_ids': sorted(set(biased)),
                        'reason': 'A task-design tool-call estimate incorrectly zeroed otherwise passing artifacts; fresh paired evaluation required'}
        out['score_summary']['evaluation_valid'] = bool(valid)
        if not valid:
            out['score_summary']['warning_code'] = 'invalid_evaluation_definition'
        out["server_time"] = _now()
        return out

    def list_runs(self, limit: int = 100, offset: int = 0) -> dict:
        with self._connect() as conn:
            total = int(conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0])
            rows = [dict(row) for row in conn.execute(
                "SELECT run_id,mode,status,trigger_kind,incumbent_version,candidate_version,error,created_at,updated_at,completed_at FROM runs ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (max(1, min(500, int(limit))), max(0, int(offset))),
            ).fetchall()]
        return {"runs": rows, "total": total}


class LiquidKernelRuntime:
    def __init__(self, registry: LiquidKernelRegistry):
        self.registry = registry
        self.lock = threading.RLock()
        self.modules: dict[str, Any] = {}
        self.module_order: deque[str] = deque()
        self.module_limit = 8

    def load(self, version: str = "") -> Any:
        target_version = str(version or self.registry.active_version())
        with self.lock:
            if target_version in self.modules:
                return self.modules[target_version]
            artifact = self.registry.artifact(target_version)
            module_name = "clouds_liquid_kernel_" + re_safe(target_version)
            spec = importlib.util.spec_from_file_location(
                module_name,
                artifact.path / "kernel.py",
                submodule_search_locations=[str(artifact.path)],
            )
            if spec is None or spec.loader is None:
                raise LiquidKernelError("kernel_load_failed", "unable to load kernel module", 500)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            try:
                spec.loader.exec_module(module)
            except Exception:
                sys.modules.pop(module_name, None)
                raise
            if int(getattr(module, "KERNEL_CONTRACT_VERSION", 0) or 0) != KERNEL_CONTRACT_VERSION:
                sys.modules.pop(module_name, None)
                raise LiquidKernelError("kernel_contract_mismatch", "kernel contract version is incompatible", 409)
            self.modules[target_version] = module
            self.module_order.append(target_version)
            while len(self.module_order) > self.module_limit:
                stale_version = self.module_order.popleft()
                if stale_version == target_version:
                    continue
                stale_module = self.modules.pop(stale_version, None)
                stale_name = str(getattr(stale_module, "__name__", "") or "")
                if stale_name:
                    for loaded_name in [name for name in sys.modules if name == stale_name or name.startswith(stale_name + ".")]:
                        sys.modules.pop(loaded_name, None)
            return module

    def filter_tools(self, tools: list[dict], *, version: str = "", role: str = "", context: dict | None = None) -> list[dict]:
        module = self.load(version)
        callback = getattr(module, "filter_tools", None)
        result = callback(list(tools or []), role=role, context=dict(context or {})) if callable(callback) else list(tools or [])
        return result if isinstance(result, list) else list(tools or [])

    def augment_prompt(self, prompt: str, *, version: str = "", role: str = "", context: dict | None = None) -> str:
        module = self.load(version)
        callback = getattr(module, "augment_prompt", None)
        result = callback(str(prompt or ""), role=role, context=dict(context or {})) if callable(callback) else str(prompt or "")
        return str(result or prompt or "")

    def hook(self, name: str, *, version: str = "", default: Any = None, **kwargs: Any) -> Any:
        module = self.load(version)
        callback = getattr(module, str(name), None)
        return callback(**kwargs) if callable(callback) else default


def re_safe(value: object) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in str(value or ""))


class StructuredPatchValidator:
    FORBIDDEN_NAMES = {
        "eval", "exec", "compile", "__import__", "open", "breakpoint", "globals", "locals",
        "subprocess", "socket", "ctypes", "multiprocessing", "urllib", "requests", "shutil", "pathlib",
        "getattr", "setattr", "delattr", "vars", "dir", "type", "object", "help", "input", "breakpoint",
    }

    @staticmethod
    def allowed_files(config: dict) -> frozenset[str]:
        mode = str(config.get("mode", ""))
        return FULL_AGENT_CORE_FILES if mode == "Aggressive" else TUNING_KERNEL_FILES if mode == "Tuning" else CONTROLLED_KERNEL_FILES

    @staticmethod
    def _changed_lines(before: str, after: str) -> int:
        import difflib

        total = 0
        for tag, left_start, left_end, right_start, right_end in difflib.SequenceMatcher(
            a=before.splitlines(), b=after.splitlines()
        ).get_opcodes():
            if tag != "equal":
                total += max(left_end - left_start, right_end - right_start)
        return total

    def _validate_ast(self, path: str, source: str, allowed_files: frozenset[str]) -> None:
        try:
            tree = ast.parse(source, filename=path)
        except SyntaxError as exc:
            raise LiquidKernelError("invalid_patch_syntax", "candidate contains invalid Python syntax",
                                    details={"path": path, "line": exc.lineno, "reason": exc.msg}) from exc
        allowed_modules = {Path(name).stem for name in allowed_files}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                raise LiquidKernelError("forbidden_import", "candidate imports an external runtime module")
            if isinstance(node, ast.ImportFrom):
                module_name = str(node.module or "")
                if module_name == "__future__" and int(node.level or 0) == 0:
                    continue
                if int(node.level or 0) != 1 or module_name not in allowed_modules:
                    raise LiquidKernelError("forbidden_import", "candidate imports outside the liquid agent core")
            if isinstance(node, (ast.Global, ast.Nonlocal)):
                raise LiquidKernelError("forbidden_scope", "candidate may not mutate external or nonlocal scope")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.decorator_list:
                raise LiquidKernelError("forbidden_decorator", "candidate functions may not use decorators")
            if isinstance(node, ast.Attribute) and str(node.attr or "").startswith("__"):
                raise LiquidKernelError("forbidden_attribute", "candidate may not access dunder attributes")
            if isinstance(node, ast.Name) and (node.id.startswith("__") or node.id in self.FORBIDDEN_NAMES):
                raise LiquidKernelError("forbidden_name", "candidate may not reference runtime escape capabilities")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_NAMES:
                raise LiquidKernelError("forbidden_call", f"candidate calls forbidden function {node.func.id}")

    def apply(self, source: str | dict[str, str], proposal: dict, config: dict) -> tuple[dict[str, str], dict]:
        patch = proposal.get("patch") if isinstance(proposal.get("patch"), dict) else {}
        files = patch.get("files") if isinstance(patch.get("files"), list) else []
        if not files:
            raise LiquidKernelError("empty_patch", "candidate proposal did not contain a structured patch")
        budget = config["budget"]
        if len(files) > int(budget["max_files"]):
            raise LiquidKernelError("patch_too_large", "candidate changes too many files")
        current = _normalize_kernel_files(source)
        allowed_files = self.allowed_files(config)
        touched: set[str] = set()
        changed_lines = 0
        for item in files:
            path = str(item.get("path", "") if isinstance(item, dict) else "").strip().replace("\\", "/")
            custom_core = (config.get("mode") == "Aggressive" and path.startswith("core_")
                           and path.endswith(".py") and path[5:-3].replace("_", "").isalnum()
                           and "/" not in path and "\\" not in path)
            if not isinstance(item, dict) or (path not in allowed_files and not custom_core):
                raise LiquidKernelError("mutable_surface_violation", "candidate attempted to modify a file outside this mode: " + path,
                                        details={"path": path, "allowed_files": sorted(allowed_files)})
            if path in touched:
                raise LiquidKernelError("duplicate_patch_file", "candidate contains multiple operations for one file")
            touched.add(path)
            operation = str(item.get("operation", "replace") or "replace")
            before = str(current.get(path, "") or "")
            if operation == "replace_file":
                updated = str(item.get("content", "") or "")
            elif operation == "replace":
                old = str(item.get("old", "") or "")
                new = str(item.get("new", "") or "")
                if not old or old not in before:
                    raise LiquidKernelError("patch_context_missing", "structured patch context was not found")
                updated = before.replace(old, new, 1)
            else:
                raise LiquidKernelError("invalid_patch_operation", "unsupported structured patch operation")
            changed_lines += self._changed_lines(before, updated)
            current[path] = updated
        if int(budget["max_changed_lines"]) > 0 and changed_lines > int(budget["max_changed_lines"]):
            raise LiquidKernelError("patch_too_large", "candidate exceeds the explicitly configured changed-line limit",
                                    details={"changed_lines": changed_lines, "limit": int(budget["max_changed_lines"]), "scope": "changed_lines"})
        unexpected = sorted(path for path in set(current) - FULL_AGENT_CORE_FILES
                            if not (path.startswith("core_") and path.endswith(".py") and path[5:-3].replace("_", "").isalnum()))
        if unexpected:
            raise LiquidKernelError("mutable_surface_violation", "kernel bundle contains unsupported files", details={"files": unexpected})
        for path, file_source in current.items():
            self._validate_ast(path, file_source, frozenset(current))
        contract = KernelBenchmark.run_bundle(
            current,
            [{"id": "contract", "role": "developer", "intent": "verify liquid kernel contract", "nonce": 1}],
            timeout_seconds=max(1.0, min(10.0, float(budget.get("timeout_seconds", 10) or 10))),
        )
        if not bool(contract.get("ok", False)):
            raise LiquidKernelError(
                "kernel_contract_missing",
                "candidate failed the isolated liquid-kernel contract check",
                details={"result": contract},
            )
        return current, {
            "changed_lines": changed_lines,
            "files": len(touched),
            "paths": sorted(touched),
            "mutable_surface": str(config.get("mutable_surface", "none")),
        }

    def check_generalization(self, source, candidate, training_tasks, config):
        """Probe unconditional training-schema leakage without consulting holdout data."""
        text = _json([{key: task.get(key) for key in ('goal', 'followups')} for task in training_tasks])
        reserved = {'read_file', 'write_file', 'edit_file', 'list_files', 'finish_task', 'context_recall',
                    'before_round', 'before_run', 'after_tool_results', 'filter_tools', 'augment_prompt',
                    'max_output_tokens', 'context_token_limit', 'tool_calls', 'tool_call_id', 'recent_results'}
        terms = {word for word in re.findall(r'\b[A-Za-z][A-Za-z0-9_]{7,}\b', text) if '_' in word and word not in reserved}
        if not terms:
            return {'contrastive_probe': 'no_specific_schema_terms', 'checked_terms': 0}
        context = {'goal': 'Inspect a source file and repair a failing test. Follow its actual schema; no domain-specific field names are prescribed.',
                   'messages': [], 'recent_results': [], 'round': 3, 'execution_mode': 'single',
                   'max_output_tokens': config['task_benchmark']['turn_max_tokens']}
        rendered = []
        for files in (source, candidate):
            worker = KernelWorker(files)
            try:
                policy = worker.call('before_round', {'context': context}, lambda: None)
                prompt = worker.call('augment_prompt', {'prompt': 'Inspect the source and repair the failing test.', 'role': 'developer', 'context': context}, lambda: None)
                rendered.append(_json({'policy': policy, 'prompt': prompt}))
            finally:
                worker.close()
        leaked = sorted(term for term in terms if term in rendered[1] and term not in rendered[0])
        if leaked:
            raise LiquidKernelError('task_specific_policy', 'Candidate applies training-only schema names to an unrelated task',
                                    details={'training_terms': leaked, 'probe': 'unrelated_task_context', 'holdout_accessed': False})
        return {'contrastive_probe': 'passed', 'checked_terms': len(terms), 'holdout_accessed': False}


def safe_builtins() -> dict:
    return {
        "bool": bool, "dict": dict, "enumerate": enumerate, "float": float, "int": int,
        "isinstance": isinstance, "len": len, "list": list, "max": max, "min": min,
        "range": range, "set": set, "sorted": sorted, "str": str, "sum": sum, "tuple": tuple,
        "zip": zip, "Exception": Exception, "ValueError": ValueError, "object": object,
        "__build_class__": __build_class__, "__name__": "liquid_candidate",
    }


class KernelBenchmark:
    def __init__(self, runtime: LiquidKernelRuntime):
        self.runtime = runtime

    @staticmethod
    def run_bundle(files: str | dict[str, str], cases: list[dict], timeout_seconds: float = 15.0) -> dict:
        payload = {"files": _normalize_kernel_files(files), "cases": list(cases or [])}
        runner = r'''
import importlib.util
import json
import pathlib
import sys
import tempfile

payload = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
with tempfile.TemporaryDirectory(prefix="liquid-kernel-benchmark-") as temp:
    root = pathlib.Path(temp)
    for relative, source in dict(payload.get("files") or {}).items():
        (root / relative).write_text(str(source or ""), encoding="utf-8", errors="backslashreplace")
    name = "isolated_liquid_kernel"
    spec = importlib.util.spec_from_file_location(name, root / "kernel.py", submodule_search_locations=[str(root)])
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to construct candidate package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    required = ["filter_tools", "augment_prompt", "before_run", "before_round", "after_tool_results"]
    missing = [hook for hook in required if not callable(getattr(module, hook, None))]
    if int(getattr(module, "KERNEL_CONTRACT_VERSION", 0) or 0) != 1:
        missing.append("KERNEL_CONTRACT_VERSION=1")
    rows = []
    passed = 0
    for case in list(payload.get("cases") or []):
        tools = [
            {"type": "function", "function": {"name": "read_file"}},
            {"type": "function", "function": {"name": "bash"}},
            {"type": "function", "function": {"name": "write_file"}},
        ]
        try:
            before_run = module.before_run(context=case)
            before_round = module.before_round(context=case)
            filtered = module.filter_tools(tools, role=str(case.get("role") or ""), context=case)
            prompt = module.augment_prompt("BASE PROMPT", role=str(case.get("role") or ""), context=case)
            after = module.after_tool_results([{"ok": True, "name": "read_file"}], context=case)
            ok = (
                not missing
                and isinstance(before_run, dict)
                and isinstance(before_round, dict)
                and isinstance(filtered, list)
                and isinstance(prompt, str)
                and bool(prompt)
                and isinstance(after, list)
            )
            rows.append({"id": str(case.get("id") or ""), "ok": bool(ok)})
            passed += int(bool(ok))
        except Exception as exc:
            rows.append({"id": str(case.get("id") or ""), "ok": False, "error": str(exc)[:240]})
    total = max(1, len(list(payload.get("cases") or [])))
    print(json.dumps({"ok": not missing and passed == len(list(payload.get("cases") or [])), "score": 100.0 * passed / total, "missing": missing, "rows": rows}))
'''
        try:
            completed = subprocess.run(
                [sys.executable, "-X", "utf8", "-I", "-S", "-c", runner],
                input=_json(payload),
                text=True,
                encoding="utf-8", errors="backslashreplace",
                capture_output=True,
                timeout=max(0.5, float(timeout_seconds or 15.0)),
                env=subprocess_environment(),
            )
        except subprocess.TimeoutExpired:
            return {"ok": False, "score": 0.0, "error": "isolated benchmark timed out", "rows": []}
        if completed.returncode != 0:
            return {
                "ok": False,
                "score": 0.0,
                "error": (completed.stderr or completed.stdout or "isolated benchmark failed")[-2000:],
                "rows": [],
            }
        result = json.loads(completed.stdout.strip() or "{}")
        return result if isinstance(result, dict) else {"ok": False, "score": 0.0, "rows": []}

    @staticmethod
    def random_cases(count: int, seed: int) -> list[dict]:
        rng = random.Random(seed)
        roles = ("developer", "reviewer", "explorer", "manager")
        intents = (
            "inspect a large repository safely", "repair a failing test", "summarize evidence before editing",
            "avoid repeating a tool call", "preserve user constraints", "finish only after verification",
            "handle an unavailable tool", "continue a multi-step task", "recover from malformed model output",
        )
        return [
            {"id": f"case-{idx + 1}", "role": rng.choice(roles), "intent": rng.choice(intents), "nonce": rng.getrandbits(32)}
            for idx in range(max(8, int(count)))
        ]

    def deterministic(
        self,
        incumbent_source: str | dict[str, str],
        candidate_source: str | dict[str, str],
        cases: list[dict],
    ) -> dict:
        scores: dict[str, float] = {}
        details: dict[str, list] = {}
        for label, source in (("incumbent", incumbent_source), ("candidate", candidate_source)):
            result = self.run_bundle(source, cases)
            scores[label] = max(0.0, min(100.0, float(result.get("score", 0.0) or 0.0)))
            details[label] = list(result.get("rows", []) or [])
        return {"scores": scores, "details": details, "case_count": len(cases)}


class LiquidKernelControlPlane:
    def __init__(
        self,
        root: Path,
        *,
        experience_provider: Callable[[dict, str, list[str]], dict] | None = None,
        model_callback: Callable[[str, str, str, int], dict] | None = None,
        judge_callback: Callable[[dict, str, int], dict] | None = None,
        model_resolver: Callable[[dict], dict] | None = None,
        config_validator: Callable[..., dict] | None = None,
        task_runtime_limits: Callable[[], dict] | None = None,
    ):
        self.root = Path(root).resolve()
        self.registry = LiquidKernelRegistry(self.root)
        self.runtime = LiquidKernelRuntime(self.registry)
        self.validator = StructuredPatchValidator()
        self.benchmark = KernelBenchmark(self.runtime)
        self.config_path = self.root / "config.json"
        self.config_lock = threading.RLock()
        self.run_lock = threading.Lock()
        self.active_run_id = ""
        self.cancelled: set[str] = set()
        self.observations: deque[dict] = deque(maxlen=200)
        self.experience_provider = experience_provider
        self.model_callback = model_callback
        self.judge_callback = judge_callback
        self.model_resolver = model_resolver
        self.config_validator = config_validator
        self.task_runtime_limits = task_runtime_limits
        self.last_trigger_error = None
        self._stop = threading.Event()
        self._scheduler_thread: threading.Thread | None = None
        if not self.config_path.exists():
            _atomic_json(self.config_path, default_evolution_config())
        # Computation threads cannot survive a process restart. Approval and
        # Canary records remain governed by their existing deployment rules.
        self._recover_interrupted_runs()

    def _recover_interrupted_runs(self):
        with self.registry._connect() as conn:
            conn.execute("UPDATE runs SET status='failed',error=?,completed_at=?,updated_at=? WHERE status IN ('queued','collecting','assessing','generating','proposal_ready','validating_patch','benchmarking','judging')",
                         ("Evolution computation interrupted before completion (process restart or worker failure)", _now(), _now()))

    def config(self) -> dict:
        with self.config_lock:
            stored = _read_json(self.config_path, {})
            if int(stored.get('quota_policy_version', 0) or 0) < 2:
                # Previous Admin had no editable line-limit field; its values
                # were imposed by mode presets, not an explicit user setting.
                stored = {**stored, 'budget': {**stored.get('budget', {}), 'max_changed_lines': 0}}
            if int(stored.get('timeout_policy_version',0) or 0)<1:
                legacy_timeout={'Off':0,'Tuning':3600,'Thinking':7200,'Aggressive':14400}.get(stored.get('mode'),0)
                if stored.get('budget',{}).get('timeout_seconds')==legacy_timeout:
                    stored={**stored,'budget':{**stored.get('budget',{}),'timeout_seconds':0}}
            return self._apply_task_runtime_limits(normalize_evolution_config(stored))

    def _apply_task_runtime_limits(self, config: dict) -> dict:
        if self.task_runtime_limits is not None:
            runtime = self.task_runtime_limits()
            rounds = max(1, min(8000, int(runtime["max_rounds"])))
            config["task_benchmark"].update(
                max_rounds=rounds, max_tool_calls=rounds * 8,
                task_timeout_seconds=max(1, int(runtime.get("max_run_seconds", 3000))),
                round_limit_source="admin.max_rounds",
            )
            if runtime.get("max_output_tokens"):
                config["task_benchmark"]["turn_max_tokens"] = max(128, int(runtime["max_output_tokens"]))
            if runtime.get("context_token_limit"):
                config["task_benchmark"]["context_token_limit"] = max(4096, int(runtime["context_token_limit"]))
                config["task_benchmark"]["context_limit_source"] = "admin.ctx_limit"
            # Evolution owns its optional cumulative quotas. Ordinary-session
            # token settings must not turn its explicit zero into a hidden cap.
        return config

    def save_config(self, values: object, expected_revision: int = 0, *, context=None) -> dict:
        with self.config_lock:
            current = self.config()
            if expected_revision and int(current.get("revision", 0)) != int(expected_revision):
                raise LiquidKernelError("config_conflict", "evolution config changed; reload before saving", 409)
            clean = normalize_evolution_config(values, current=current)
            if self.config_validator:
                clean = self.config_validator(clean, context=context, current=current)
            clean = self._apply_task_runtime_limits(clean)
            clean["revision"] = int(current.get("revision", 0)) + 1
            _atomic_json(self.config_path, clean)
            if clean["mode"] == "Off":
                if self.active_run_id:
                    self.cancelled.add(self.active_run_id)
                    self.registry.event(self.active_run_id, "cancel_requested", {"reason": "evolution mode set to Off"})
                self.registry.abort_canary(reason="evolution mode set to Off")
        return {"ok": True, "config": clean}

    def apply_startup_config(self, mode: str = "", schedule: str = "") -> dict:
        current = self.config()
        values = dict(current)
        normalized_mode = str(mode or "").strip().title()
        normalized_schedule = str(schedule or "").strip().lower()
        if normalized_mode:
            if normalized_mode not in EVOLUTION_MODES:
                raise LiquidKernelError("invalid_mode", "mode must be Off, Tuning, Thinking, or Aggressive")
            values["mode"] = normalized_mode
            if not normalized_schedule:
                values["schedule"] = str(MODE_PRESETS[normalized_mode]["schedule"])
        if normalized_schedule:
            values["schedule"] = normalized_schedule
        if not normalized_mode and not normalized_schedule:
            return {"ok": True, "config": current, "changed": False}
        saved = self.save_config(values, expected_revision=int(current.get("revision", 0) or 0))
        saved["changed"] = True
        return saved

    def start_scheduler(self) -> None:
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            return
        self._stop.clear()
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, name="liquid-kernel-evolution", daemon=True)
        self._scheduler_thread.start()

    def stop_scheduler(self) -> None:
        self._stop.set()
        if self.active_run_id:
            self.cancelled.add(self.active_run_id)

    def _schedule_due(self, config: dict, last_created: float) -> bool:
        if config["mode"] == "Off" or config["schedule"] == "off":
            return False
        interval = {
            "hourly": 3600,
            "daily": 86400,
            "weekly": 7 * 86400,
            "every_3_days": 3 * 86400,
        }.get(str(config["schedule"]), 0)
        if interval <= 0:
            return False
        return _now() - float(last_created or 0) >= max(interval, int(config["cooldown_hours"]) * 3600)

    def _scheduler_loop(self) -> None:
        while not self._stop.wait(30):
            try:
                config = self.config()
                runs = self.registry.list_runs(limit=1).get("runs", [])
                last_created = float(runs[0].get("created_at", 0) or 0) if runs else 0.0
                if self._schedule_due(config, last_created) and not self.active_run_id:
                    self.trigger("schedule")
            except LiquidKernelError as exc:
                self.last_trigger_error = {"code": exc.code, "error": str(exc), "trigger": "schedule", "at": _now()}
            except Exception:
                self.last_trigger_error = {"code": "scheduler_failed", "error": "Evolution scheduler could not start a run", "at": _now()}
                continue

    def trigger(self, trigger_kind: str = "manual", expected_revision: int = 0) -> dict:
        with self.config_lock:
            config = self.config()
            if expected_revision and expected_revision != config["revision"]:
                raise LiquidKernelError("config_conflict", "evolution config changed; reload and save before starting", 409)
            if config["mode"] == "Off":
                raise LiquidKernelError("evolution_disabled", "liquid-kernel evolution is Off", 409)
            if not self.run_lock.acquire(blocking=False):
                raise LiquidKernelError("run_in_progress", "an evolution run is already active", 409)
            run_id = ""
            try:
                if not callable(self.model_callback) or not callable(self.judge_callback):
                    raise LiquidKernelError("model_unavailable", "generator and judge must both be configured", 409)
                if self.model_resolver:
                    config = self.model_resolver(config)
                run_id = self.registry.create_run(config, trigger_kind)
                self.active_run_id = run_id
                threading.Thread(target=self._run, args=(run_id, config), daemon=True, name=f"evolution-{run_id[:12]}").start()
                self.last_trigger_error = None
            except BaseException as exc:
                self.active_run_id = ""
                self.run_lock.release()
                if run_id:
                    try:
                        self.registry.update_run(run_id, "failed", error="Evolution worker could not start", completed_at=_now())
                    except (OSError, sqlite3.Error):
                        pass  # Recovered on the next idle dashboard read/restart.

                if isinstance(exc, LiquidKernelError):
                    raise
                raise LiquidKernelError("run_start_failed", "Evolution worker could not start; retry after checking storage and worker availability", 503) from exc
            return {"ok": True, "run_id": run_id, "status": "queued", "revision": config["revision"],
                    "models": {role: config.get(f"{role}_model_ref") for role in ("generator", "judge")}}

    def inject_embedded_kernel(self, reason: str = "administrator selected embedded kernel", *, force: bool = False) -> dict:
        """Install the bundled kernel without deleting version or session history."""
        incumbent = self.registry.active_version()
        state = self.registry.active_state()
        detail = self.registry.version_detail(incumbent)
        if not force and (detail.get("parent_version") or state.get("canary")):
            return {"ok": True, "injected": False, "protected_evolved_kernel": True,
                    "version": incumbent, "previous_version": incumbent,
                    "reason": "Startup framework upgrade preserves the evolved kernel and active canary. Explicit force is required to replace it."}
        embedded_source = dict(BASELINE_KERNEL_FILES)
        if _kernel_bundle_hash(self.registry.sources(incumbent)) == _kernel_bundle_hash(embedded_source):
            return {
                "ok": True,
                "injected": False,
                "version": incumbent,
                "previous_version": incumbent,
                "reason": "embedded kernel is already active",
            }
        run_id = self.registry.create_run(self.config(), "admin_inject")
        self.registry.update_run(run_id, "injecting")
        self.registry.event(run_id, "injecting", {"previous_version": incumbent, "reason": str(reason or "")})
        try:
            version = self.registry.register_candidate(
                run_id,
                incumbent,
                embedded_source,
                mode="embedded",
                changelog="Administrator injected the embedded Liquid Agent Kernel.",
                scores={"hard": 100.0, "soft": 100.0, "mixed": 100.0},
            )
            self.registry.begin_canary(version, 100)
            promoted = self.registry.promote(version)
            result = {
                "ok": True,
                "injected": True,
                "version": version,
                "previous_version": incumbent,
                "reason": str(reason or ""),
                "promoted": promoted,
            }
            self.registry.update_run(
                run_id,
                "promoted",
                candidate_version=version,
                result_json=result,
                completed_at=_now(),
            )
            self.registry.event(run_id, "injected", result)
            return result
        except Exception as exc:
            self.registry.update_run(run_id, "failed", error=str(exc), completed_at=_now())
            self.registry.event(run_id, "failed", {"error": str(exc)})
            raise

    def cancel(self, run_id: str) -> dict:
        with self.config_lock:
            detail = self.registry.run_detail(str(run_id))
            status = str(detail.get("status", "") or "")
            if status == "canary":
                rollback = self.registry.abort_canary(reason="evolution run cancelled by administrator")
                self.registry.update_run(str(run_id), "cancelled", completed_at=_now())
                self.registry.event(str(run_id), "cancelled", {"rollback": rollback})
                return {"ok": True, "run_id": str(run_id), "cancel_requested": False, "rollback": rollback}
            if status in {"rejected", "failed", "cancelled", "no_change", "promoted", "rolled_back"}:
                raise LiquidKernelError("invalid_run_state", "run is already complete", 409)
            if status == "awaiting_approval":
                self.registry.update_run(str(run_id), "cancelled", completed_at=_now())
                self.registry.event(str(run_id), "cancelled", {})
                return {"ok": True, "run_id": str(run_id), "cancel_requested": False}
            self.cancelled.add(str(run_id))
            self.registry.event(str(run_id), "cancel_requested", {})
            return {"ok": True, "run_id": str(run_id), "cancel_requested": True}

    def _check_cancel(self, run_id: str) -> None:
        if run_id in self.cancelled:
            raise LiquidKernelError("run_cancelled", "evolution run was cancelled", 409)
        if getattr(self, "_token_budget_exhausted", False):
            raise LiquidKernelError("run_budget_exhausted", "Evolution model-token budget exhausted.", 409)
        if getattr(self, "_active_deadline", 0) and time.monotonic() > self._active_deadline:
            raise LiquidKernelError("run_budget_exhausted", "Evolution wall-clock budget exhausted.", 409)

    def _model_allowance(self, prompt: str, requested: int) -> int:
        total_limit = getattr(self, "_token_limit", 0)
        local_ceiling = getattr(self, "_rollout_token_ceiling", 0)
        if not total_limit and not local_ceiling:
            return requested
        # The host callback accounts for the actual transported native history.
        # Raw rollout JSON may include archived write bodies no longer sent.
        used = getattr(self, "_tokens_used", 0)
        remaining = total_limit - used if total_limit else requested
        if total_limit and not local_ceiling:
            remaining -= max(1, len(prompt) // 4)
        if local_ceiling:
            local_remaining = local_ceiling - used
            if local_remaining < 128:
                raise TimeoutError("task_token_budget_exhausted: reserved per-task model budget exhausted")
            remaining = min(remaining, local_remaining)
        if remaining < 128:
            self._token_budget_exhausted = True
            raise LiquidKernelError("run_budget_exhausted", "Evolution model-token budget exhausted.", 409)
        return min(requested, remaining)

    @contextlib.contextmanager
    def _model_budget_scope(self, limit, label="task"):
        previous = getattr(self, "_rollout_token_ceiling", 0)
        previous_label = getattr(self, "_model_budget_label", "")
        started = self._tokens_used
        limit = max(0, int(limit or 0))
        ceilings = [value for value in (previous, started + limit if limit else 0) if value]
        self._rollout_token_ceiling = min(ceilings) if ceilings else 0
        self._model_budget_label = label
        state = {"scope": label, "limit": int(limit), "used": 0, "exhausted": False}
        try:
            yield state
        except TimeoutError as exc:
            state["exhausted"] = "budget" in str(exc)
            raise
        finally:
            state["used"] = self._tokens_used - started
            state["remaining"] = max(0, limit - state["used"]) if limit else None
            state["exhausted"] = state["exhausted"] or bool(limit and state["used"] >= limit)
            self._rollout_token_ceiling = previous
            self._model_budget_label = previous_label
            if self.active_run_id:
                self.registry.event(self.active_run_id, "model_budget_consumed", state)

    def _record_model_tokens(self, prompt: str, result: dict) -> None:
        usage = result.pop("_evolution_usage", {})
        reported = usage.get("total_tokens", 0) if isinstance(usage, dict) else 0
        estimate = max(1, (len(prompt) + len(_json(result))) // 4)
        self._tokens_used = getattr(self, "_tokens_used", 0) + (max(1, int(reported or 0)) if isinstance(usage, dict) and usage.get("transport_accounted") else max(estimate, int(reported or 0)))
        total_limit = getattr(self, "_token_limit", 0)
        if self.active_run_id:
            self.registry.event(self.active_run_id, 'token_usage', {'used': self._tokens_used, 'limit': total_limit})
        if total_limit and self._tokens_used > total_limit:
            self._token_budget_exhausted = True
            raise LiquidKernelError("run_budget_exhausted", "Evolution model-token budget exhausted.", 409)
        if getattr(self, "_rollout_token_ceiling", 0) and self._tokens_used > self._rollout_token_ceiling:
            raise TimeoutError("task_token_budget_exhausted: observed task model usage exceeded its reserved budget")

    @contextlib.contextmanager
    def observe_model_request(self, model, *, timeout_seconds=0, label="", provider='', endpoint_host=''):
        run_id = self.active_run_id
        request_id = uuid.uuid4().hex
        if not run_id:
            yield request_id
            return
        started = time.monotonic()
        payload = {'request_id': request_id, 'model': str(model), 'timeout_seconds': timeout_seconds, 'operation': label,
                   'provider': str(provider), 'endpoint_host': str(endpoint_host)}
        self.registry.event(run_id, 'model_request_started', payload)
        stop = threading.Event()
        def heartbeat():
            while not stop.wait(5):
                self.registry.event(run_id, 'model_request_wait', {'request_id': request_id, 'elapsed_seconds': round(time.monotonic() - started, 1)})
        thread = threading.Thread(target=heartbeat, name='evolution-model-heartbeat', daemon=True)
        thread.start()
        try:
            yield request_id
        except BaseException as exc:
            diagnostic = exc.diagnostics() if callable(getattr(exc, 'diagnostics', None)) else {}
            self.registry.event(run_id, 'model_request_failed', {**payload, 'elapsed_seconds': round(time.monotonic() - started, 1), 'error_type': type(exc).__name__, 'error_code': str(getattr(exc, 'code', '')), **diagnostic})
            raise
        else:
            self.registry.event(run_id, 'model_request_completed', {**payload, 'elapsed_seconds': round(time.monotonic() - started, 1)})
        finally:
            stop.set()
            thread.join(timeout=.2)

    def note_model_retry(self, request_id, info):
        if self.active_run_id:
            info = info if isinstance(info, dict) else {}
            self.registry.event(self.active_run_id, 'model_http_attempt_started' if info.get('phase') == 'request' else 'model_request_retry', {
                'request_id': request_id, 'attempt': info.get('attempt', info.get('retry', 0)),
                'retry_budget': info.get('retry_budget', 0),
                'http_status': info.get('status', 0), **({'error_code': 'model_rate_limited'} if info.get('status') == 429 else {}), 'retry_after_seconds': info.get('delay', info.get('sleep_seconds', info.get('wait_seconds', 0)))})

    def _call_model(self, system: str, prompt: str, profile: str, max_tokens: int) -> dict:
        if not callable(self.model_callback):
            raise LiquidKernelError("model_unavailable", "Evolution model callback is not configured.")
        allowance = self._model_allowance(system + prompt, max_tokens)
        result = self.model_callback(system, prompt, profile, allowance)
        if not isinstance(result, dict):
            raise LiquidKernelError("invalid_model_output", "evolution model did not return a JSON object")
        self._record_model_tokens(system + prompt, result)
        return result

    def _call_proposal_model(self, system, payload, profile, max_tokens):
        original = json.loads(payload) if isinstance(payload, str) else payload
        request = original
        attempts = []
        for attempt in range(3):
            self._check_cancel(self.active_run_id)
            result = self._call_model(system, _json(request), profile, max_tokens)
            try:
                return normalize_proposal_output(result)
            except LiquidKernelError as exc:
                attempts.append({'attempt':attempt+1,'code':exc.code,'reason':str(exc),'details':exc.details})
                if attempt == 2:
                    raise LiquidKernelError('invalid_proposal_schema', 'Proposal schema remains invalid after bounded repair', 422,
                                            {'attempts':attempts}) from exc
                if self.active_run_id:
                    self.registry.event(self.active_run_id, 'model_json_recovery', {
                        'attempt':attempt+1,'reason':'invalid_proposal_schema','stage':'generator','recovery_mode':'schema'})
                request = {'task':'Repair the proposal JSON schema without inventing evidence or changing deployment/acceptance rules.',
                           'original_request':original,
                           'previous_output':{key:value for key,value in result.items() if key!='_evolution_usage'},
                           'validation_errors':attempts,
                           'required_contract':{'decision':'change|no_change','reason':'nonempty top-level string',
                                                'patch':'For change, retain the full proposed files under patch.files. Never infer a missing decision.'}}

    def _experience(self, config: dict, incumbent: str) -> dict:
        versions = self.registry.lineage_versions(incumbent, int(config["history_version_depth"]))
        if callable(self.experience_provider):
            result = self.experience_provider(config, incumbent, versions)
            if isinstance(result, dict):
                return result
        return {"versions": versions, "records": [], "record_count": 0, "note": "No experience provider configured."}

    @staticmethod
    def _experience_audit_view(experience: dict) -> dict:
        audit = {key: value for key, value in dict(experience or {}).items() if key not in {"records", "history_by_version", "task_source_records"}}
        grouped = experience.get("history_by_version", {}) if isinstance(experience.get("history_by_version"), dict) else {}
        audit["history_by_version"] = {
            str(version): {
                key: value
                for key, value in dict(payload or {}).items()
                if key != "records"
            }
            for version, payload in grouped.items()
            if isinstance(payload, dict)
        }
        audit["raw_records_persisted_in_protected_manifest"] = any(
            bool(payload.get("records"))
            for payload in grouped.values()
            if isinstance(payload, dict)
        )
        return audit

    def _soft_score(
        self,
        incumbent_source: str | dict[str, str],
        candidate_source: str | dict[str, str],
        cases: list[dict],
        config: dict,
        observations: dict | None = None,
    ) -> dict:
        incumbent_files = _normalize_kernel_files(incumbent_source)
        candidate_files = _normalize_kernel_files(candidate_source)
        if callable(self.judge_callback):
            payload = {
                "incumbent_source": _kernel_bundle_text(incumbent_files) if observations is None else "",
                "candidate_source": _kernel_bundle_text(candidate_files) if observations is None else "",
                "incumbent_files": incumbent_files if observations is None else {},
                "candidate_files": candidate_files if observations is None else {},
                "cases": cases,
                "observations": observations,
            }
            tokens = self._model_allowance("" if observations is not None else _json(payload), int(config['task_benchmark']['turn_max_tokens']))
            result = self.judge_callback(
                payload,
                config.get("judge_model_ref") or str(config.get("judge_profile", "")),
                tokens,
            )
            if isinstance(result, dict):
                self._record_model_tokens(_json(payload), result)
                a = valid_judge_score(result.get("incumbent"))
                b = valid_judge_score(result.get("candidate"))
                return {"incumbent": a, "candidate": b, "details": result}
            raise LiquidKernelError("invalid_judge_output", "Judge did not return scores")
        raise LiquidKernelError("judge_unavailable", "Judge callback is not configured")

    @staticmethod
    def _benchmark_cases(proposals: list[dict], max_cases: int, seed: int) -> list[dict]:
        limit = max(8, int(max_cases or 8))
        base_count = min(limit, max(8, limit // 2))
        cases = KernelBenchmark.random_cases(base_count, seed)
        seen = {
            _json({key: value for key, value in case.items() if key not in {"id", "nonce"}})
            for case in cases
        }

        def clipped(value: object, length: int) -> str:
            return str(value or "").strip()[:length]

        for proposal in proposals:
            proposed = proposal.get("benchmark_cases") if isinstance(proposal.get("benchmark_cases"), list) else []
            for raw_case in proposed:
                if len(cases) >= limit:
                    break
                if not isinstance(raw_case, dict):
                    continue
                intent = clipped(raw_case.get("intent"), 600)
                if not intent:
                    continue
                constraints = raw_case.get("constraints") if isinstance(raw_case.get("constraints"), list) else []
                normalized_constraints = []
                for item in constraints[:8]:
                    value = clipped(item, 240)
                    if value:
                        normalized_constraints.append(value)
                case = {
                    "id": clipped(raw_case.get("id"), 80) or f"designed-{len(cases) + 1}",
                    "role": clipped(raw_case.get("role"), 80) or "developer",
                    "intent": intent,
                    "constraints": normalized_constraints,
                    "expected": clipped(raw_case.get("expected"), 600),
                }
                fingerprint = _json({key: value for key, value in case.items() if key != "id"})
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                case["nonce"] = int(hashlib.sha256(utf8_bytes(fingerprint)).hexdigest()[:8], 16)
                cases.append(case)
        return cases

    def _evaluate_candidate(
        self,
        run_id: str,
        source: dict[str, str],
        proposal: dict,
        config: dict,
        cases: list[dict],
        seed: int,
    ) -> tuple[dict[str, str], dict, dict]:
        self._check_cancel(run_id)
        candidate_source, patch_meta = self.validator.apply(source, proposal, config)
        self.registry.update_run(run_id, "benchmarking")
        hard = self.benchmark.deterministic(source, candidate_source, cases)
        incumbent_hard = float(hard["scores"]["incumbent"])
        candidate_hard = float(hard["scores"]["candidate"])
        regression_limit = incumbent_hard * (1.0 - float(config["hard_regression_limit"]))
        retried = False
        if candidate_hard < regression_limit:
            retried = True
            retry_cases = self.benchmark.random_cases(int(config["budget"]["max_cases"]), seed + 1)
            hard = self.benchmark.deterministic(source, candidate_source, retry_cases)
            incumbent_hard = float(hard["scores"]["incumbent"])
            candidate_hard = float(hard["scores"]["candidate"])
            if candidate_hard < incumbent_hard * 0.95:
                return candidate_source, {
                    "decision": "reject",
                    "reason": "deterministic score regressed by more than 5% twice",
                    "hard": hard,
                    "hard_retried": True,
                    "patch": patch_meta,
                }, {"hard": candidate_hard, "soft": 0.0, "mixed": 0.0}
        self._check_cancel(run_id)
        self.registry.update_run(run_id, "judging")
        self.registry.event(run_id, "model_call_started", {"stage": "judge", "model": config.get("judge_model_ref")})
        try:
            soft = self._soft_score(source, candidate_source, cases, config)
        except LiquidKernelError as exc:
            raise LiquidKernelError("judge_call_failed", str(exc), exc.status, {"cause": exc.code}) from exc
        self._check_cancel(run_id)
        self.registry.event(run_id, "model_call_completed", {"stage": "judge", "model": config.get("judge_model_ref"), "scores": soft})
        incumbent_mixed = incumbent_hard * 0.30 + float(soft["incumbent"]) * 0.70
        candidate_mixed = candidate_hard * 0.30 + float(soft["candidate"]) * 0.70
        gain = candidate_mixed - incumbent_mixed
        scores = {"hard": candidate_hard, "soft": float(soft["candidate"]), "mixed": candidate_mixed}
        return candidate_source, {
            "decision": "promote" if gain >= float(config["minimum_gain"]) else "reject",
            "incumbent": {"hard": incumbent_hard, "soft": soft["incumbent"], "mixed": incumbent_mixed},
            "candidate": scores,
            "gain": gain,
            "minimum_gain": float(config["minimum_gain"]),
            "hard_retried": retried,
            "random_seed": seed,
            "case_count": len(cases),
            "patch": patch_meta,
            "soft_details": soft.get("details", {}),
        }, scores

    def _exploration_proposal(self, source, evidence, index):
        """Construct an explicitly unproven context-policy trial, never a baseline clone."""
        training = evidence.get('rows', [])
        rounds = max([int(row.get('rounds', 0)) for row in training] or [0])
        # Keep more exact recent exchanges during recovery. Older exchanges
        # remain in the protected archive with host-enforced progress handoff.
        keep = (6 if rounds > 12 else 8) + 2 * (index % 3)
        tag = _kernel_bundle_hash(source)[:12] + '_' + str(index)
        parent = 'exploration_parent_' + tag
        suffix = ('\n\n' + parent + ' = before_round\n'
                  'def before_round(context=None):\n'
                  '    context = context or {}\n'
                  '    policy = dict(' + parent + '(context=context) or {})\n'
                  '    failures = any(row.get("ok") is False for row in context.get("recent_results", []) if isinstance(row, dict))\n'
                  '    policy["recent_tool_exchanges"] = ' + str(keep + 6) + ' if failures else ' + str(keep) + '\n'
                  '    return policy\n')
        return {'decision': 'change',
                'reason': 'Test an inherited adaptive recent-observation window against measured training round/token costs. Keep more exchanges during recovery; exact evidence and user goals remain protected. This is an experiment, not a proven improvement.',
                'changelog': 'Experimental adaptive context selection; deployment requires real paired and independent confirmation.',
                'origin': 'architecture_exploration',
                'hypothesis': {'mechanism': 'adaptive_recent_tool_exchanges', 'recent_exchanges': keep,
                               'recovery_exchanges': keep + 6, 'training_evidence': evidence, 'verified_gain': False},
                'patch': {'files': [{'path': 'kernel.py', 'operation': 'replace_file', 'content': source['kernel.py'] + suffix}]}}

    def _run_task_driven(self, run_id: str, config: dict, incumbent: str, source: dict, experience: dict) -> None:
        self._active_deadline = getattr(self,"_active_deadline",0) or (time.monotonic()+config["budget"]["timeout_seconds"] if config["budget"]["timeout_seconds"] else 0)
        self._token_limit = max(0, config["budget"]["max_tokens"])
        self._tokens_used = 0
        self._token_budget_exhausted = False
        seed = random.SystemRandom().randint(1, 2**31 - 1)
        profile = config.get("generator_model_ref") or config.get("generator_profile", "")
        output_root = self.registry.experience_root / run_id

        def task_model(system, prompt, tokens=None, *, deadline=None):
            self._check_cancel(run_id)
            self._call_deadline = deadline or 0
            try:
                return self._call_model(system, _json(prompt), profile, tokens or config['task_benchmark']['turn_max_tokens'])
            finally:
                self._call_deadline = 0

        self.registry.event(run_id, "task_design_started", {"stage": "task_designer"})
        try:
            bank = build_task_bank(experience, config, task_model, seed, progress=lambda kind, payload: self.registry.event(run_id, kind, payload))
        except ValueError as exc:
            raise LiquidKernelError("invalid_task_design", str(exc), 422) from exc
        self._check_cancel(run_id)
        if not bank["tasks"]:
            result = {"decision": "failed", "code": "insufficient_session_tasks", "reason": bank["reason"],
                      "benchmark_kind": "session_agentic", "evaluated": False}
            self.registry.update_run(run_id, "failed", error=bank["reason"], result_json=result, completed_at=_now())
            self.registry.event(run_id, "failed", result)
            return
        bank = canonicalize_task_bank(bank)
        frozen_hash = bank["fingerprint"]
        _atomic_json(output_root / "task_bank.json", bank)
        self.registry.event(run_id, "task_bank_frozen", {"fingerprint": frozen_hash, "train": bank["train_count"],
                                                         "holdout": bank["holdout_count"], "source_split": True})
        # Only a positive, explicitly configured task quota limits a rollout.
        # Total quota is shared as-is; no fair-share or proposal/review slice is
        # synthesized from it. Zero never means a tiny fallback allowance.
        rollout_count = len(bank["tasks"]) * (1 + 3 * max(1, config["budget"]["candidate_limit"]))
        task_tokens = max(0, int(config["task_benchmark"].get("max_task_tokens", 0) or 0))
        config["task_benchmark"]["token_budget"] = task_tokens
        phase_tokens = 0
        self.registry.event(run_id, "task_budget_allocated", {"per_task_tokens": task_tokens, "paired_rollouts": rollout_count,
                                                             "reserved_tokens": 0, "per_proposal_tokens": 0,
                                                             "per_review_tokens": 0, "total_limit": self._token_limit,
                                                             "reserve_percent": 0, "round_limit": config["task_benchmark"]["max_rounds"]})

        @contextlib.contextmanager
        def task_budget_scope():
            with self._model_budget_scope(task_tokens, "task") as state:
                yield state

        candidate_versions = {}

        def save_task_checkpoint(arm, snapshot):
            _atomic_json(output_root / (arm + '_rollouts.json'), snapshot)
            if arm == 'incumbent':
                current = self.registry.run_detail(run_id).get('result', {})
                summary = {'hard': snapshot['score'], 'success_rate': snapshot['success_rate'],
                           'completed_tasks': snapshot['completed_tasks'], 'expected_tasks': snapshot['expected_tasks'],
                           'score_status': 'partial', 'task_execution_measured': True}
                self.registry.update_run(run_id, 'benchmarking', result_json={**current, 'incumbent': summary})
            elif arm in candidate_versions:
                version = candidate_versions[arm]
                summary = {'hard': snapshot['score'], 'success_rate': snapshot['success_rate'],
                           'completed_tasks': snapshot['completed_tasks'], 'expected_tasks': snapshot['expected_tasks'],
                           'score_status': 'partial', 'task_execution_measured': True}
                self.registry.record_candidate_evaluation(version, {'candidate': summary})
                current = self.registry.run_detail(run_id).get('result', {})
                self.registry.update_run(run_id, 'benchmarking', result_json={**current, 'candidate': summary})

        benchmark = AgenticBenchmark(task_model, lambda: self._check_cancel(run_id),
                                     lambda kind, payload: self.registry.event(run_id, kind, payload), task_budget_scope,
                                     archive_root=output_root / "full_history", reference_files=source, on_checkpoint=save_task_checkpoint)
        self.registry.update_run(run_id, "benchmarking")
        baseline = benchmark.run(source, bank["tasks"], config["task_benchmark"], "incumbent")
        _atomic_json(output_root / "incumbent_rollouts.json", baseline)
        baseline_summary = {"hard": baseline["score"], "success_rate": baseline["success_rate"], "completed_tasks": len(baseline["rows"])}
        self.registry.update_run(run_id, "benchmarking", result_json={"incumbent": baseline_summary})
        self.registry.update_run(run_id, "judging")
        self.registry.event(run_id, "model_call_started", {"stage": "baseline_judge", "kind": "frozen_baseline_outcomes"})
        baseline_review = self._soft_score(source, source, bank["tasks"], config,
                                          observations={"incumbent": baseline, "candidate": baseline})
        baseline_soft = (baseline_review["incumbent"] + baseline_review["candidate"]) / 2
        baseline_summary.update(soft=baseline_soft, mixed=baseline["score"] * .7 + baseline_soft * .2 + 5,
                                score_status="completed" if rollout_complete(baseline) else "partial", task_execution_measured=True)
        self.registry.update_run(run_id, "judging", result_json={"incumbent": baseline_summary})
        self.registry.event(run_id, "baseline_scored", {"score": baseline_summary["mixed"]})
        self._check_cancel(run_id)
        training_tasks = [task for task in bank["tasks"] if task["split"] == "train"]
        baseline_training = [trajectory_model_view(row) for row in baseline["rows"] if row["split"] == "train"]
        optimization_evidence = training_opportunity_evidence(baseline)
        evaluations = []
        proposals = []
        accepted = []
        previous_training_rollouts = []
        count = max(1, config["budget"]["candidate_limit"])
        for index in range(count):
            self._check_cancel(run_id)
            self.registry.update_run(run_id, "generating")
            prompt = {
                "task": "Improve the executable agent architecture using measured quality and efficiency on user-derived long tasks, including successful tasks. Construct one concrete experimental architecture variant as a structured code patch. The experiment may underperform; evaluation, not the proposer, decides whether to deploy.",
                "candidate_index": index + 1, "mode": config["mode"], "kernel_files": source,
                "allowed_patch_files": sorted(self.validator.allowed_files(config)),
                "new_modules": "Aggressive additionally permits core_<name>.py modules; other modes use only the allowed names.",
                "budget": config["budget"], "task_execution_limits": config["task_benchmark"], "training_tasks": training_tasks, "baseline_training_rollouts": baseline_training,
                "previous_training_rollouts": previous_training_rollouts,
                "optimization_evidence": optimization_evidence,
                "previous_evaluations": [{key: row[key] for key in ("candidate_index", "decision", "code", "details", "reason", "gain", "measured_task_gain", "patch") if key in row}
                                         for row in evaluations],
                "execution_policy_contract": {
                    "kernel_entrypoint": "kernel.py MUST preserve KERNEL_CONTRACT_VERSION = 1 and export all five callable hooks: filter_tools, augment_prompt, before_run, before_round, after_tool_results. Preserve unchanged hooks by importing/re-exporting them from the original artifact modules.",
                    "before_round": "context contains messages, recent_results, goal, round, max_output_tokens and context_token_limit. Supported effective fields are allowed_tools, tool_order, recent_tool_exchanges and system_suffix; arbitrary messages/history/max_output_tokens replacements are not applied. Return only supported fields that need a measured change. Omit allowed_tools/recent_tool_exchanges to inherit host defaults. Output allowance is controlled exclusively by Admin/runtime/quota, never by candidate max_output_tokens. Host recall is always protected. History selection retains a protected progress handoff plus exact archived evidence.",
                    "python_constraints": "Inputs are JSON dict/list data: use .get() and normal indexing. Dynamic reflection (getattr/setattr/vars/dir/type), external imports, decorators and dunder access are unavailable.",
                    "available_builtins": sorted(key for key in safe_builtins() if not key.startswith("__") and key not in self.validator.FORBIDDEN_NAMES),
                    "modules": "Implement algorithms in Python: planning, context/evidence selection, recovery, routing, verification and state. Re-export hooks through kernel.py. Only relative imports within this artifact and __future__ annotations are allowed. No standard-library imports, including threading/hashlib/json/re, are allowed; use plain Python builtins and artifact modules. In controlled modes never edit harness.py; import and re-export a hook from an allowed new module through kernel.py instead.",
                    "other_hooks": "before_run(context)->dict; filter_tools(tools,role,context)->list; augment_prompt(prompt,role,context)->str; after_tool_results(results,context)->list. Each result is {name, ok, output}; output may be a nested object containing content/exit_code, not just a string. Preserve pairing by tool name and archived exact evidence.",
                    "immutable": list(IMMUTABLE_CONTROL_COMPONENTS),
                },
                "rules": ["Do not access or infer held-out task contents. Do not weaken acceptance checks or safety controls.",
                          "Optimize actual task behavior, not just prompt wording or contract-test scores.",
                          "Propose one bounded mechanism-level hypothesis supported by observed correctness, quality, token/round costs, context/memory, routing or recovery evidence. Passing every check or having zero failed tools is not by itself a reason for no_change. Preserve working behavior. A hypothesis is not a claimed improvement until the real paired evaluation verifies it.",
                          "Do not stop because the baseline succeeds. Select a bounded mechanism-level experiment from the optimization axes, state its falsifiable hypothesis and uncertainty, and submit real executable changes. Never copy the baseline or make comment/name-only changes; avoid speculative global rewrites.",
                          "Never encode training filenames, JSON keys, expected values or metric definitions as universal instructions. Derive schema and counter semantics from the current task. Plural field names can legally be counts; names alone never determine types.",
                          "Test recovery across unrelated contexts. A sandbox or missing-command error is an environment constraint: use portable Python operations, not smaller output limits or blanket history deletion.",
                          "All arms use fresh workspaces, the same frozen tasks, and the same worker model configuration."],
                "output_schema": {"decision": "change", "reason": "measured evidence and a testable experimental mechanism; benefits remain unverified until evaluation", "changelog": "change summary",
                                  "patch": {"files": [{"path": "allowed module", "operation": "replace|replace_file", "old": "text", "new": "text", "content": "module source"}]}},
            }
            self.registry.event(run_id, "model_call_started", {"stage": "generator", "candidate_index": index + 1, "candidate_total": count})
            try:
                with self._model_budget_scope(phase_tokens, "proposal"):
                    proposal = self._call_proposal_model("You evolve agent code from measured task outcomes. Return strict JSON. Evaluator and deployment controls are immutable.",
                                          prompt, profile, config["task_benchmark"]["turn_max_tokens"])
                    if proposal['decision'] == 'no_change':
                        initial = proposal
                        self.registry.event(run_id, 'opportunity_audit_started', {'candidate_index': index + 1})
                        try:
                            proposal = self._call_proposal_model(
                                "Audit a no-change decision against actual training costs and quality. A successful task can still support a bounded mechanism-level efficiency trial. Return the same strict proposal JSON; never invent benefits or bypass real evaluation.",
                                {**prompt, 'proposal_phase': 'opportunity_audit', 'previous_proposal': initial,
                                 'audit_instruction': 'Reconsider the initial no_change using every optimization axis and the exact training evidence. A failure-only explanation is insufficient. Propose a small testable general mechanism when supported; otherwise select one conservative architecture exploration and label its benefit unproven. Do not access holdout contents.'},
                                profile, config['task_benchmark']['turn_max_tokens'])
                            proposal['opportunity_audit'] = {'status': 'completed', 'initial_decision': 'no_change', 'final_decision': proposal['decision']}
                            self.registry.event(run_id, 'opportunity_audit_completed', {'candidate_index': index + 1, 'decision': proposal['decision']})
                        except LiquidKernelError as exc:
                            if exc.code not in {'invalid_proposal_schema', 'invalid_model_output', 'structured_round_budget_exhausted'}:
                                raise
                            proposal = initial
                            proposal['opportunity_audit'] = {'status': 'failed', 'code': exc.code}
                            self.registry.event(run_id, 'opportunity_audit_failed', {'candidate_index': index + 1, 'code': exc.code})
            except TimeoutError as exc:
                evaluations.append({"candidate_index": index + 1, "decision": "reject", "code": "proposal_budget_exhausted", "reason": str(exc)})
                continue
            except LiquidKernelError as exc:
                if exc.code not in {'invalid_proposal_schema', 'invalid_model_output', 'structured_round_budget_exhausted'}:
                    raise
                proposal = self._exploration_proposal(source, optimization_evidence, index)
                proposal['generation_diagnostic'] = {'code': exc.code, 'reason': str(exc), 'details': exc.details}
                self.registry.event(run_id, 'architecture_exploration_started', {'candidate_index': index + 1, 'reason': exc.code})
            if proposal["decision"] == "no_change":
                prior = proposal
                proposal = self._exploration_proposal(source, optimization_evidence, index)
                proposal['opportunity_audit'] = prior.get('opportunity_audit')
                proposal['declined_proposal'] = prior
                self.registry.event(run_id, 'architecture_exploration_started', {'candidate_index': index + 1, 'mechanism': proposal['hypothesis']['mechanism']})
            proposals.append(proposal)
            self.registry.update_run(run_id, "proposal_ready", proposal_json={"candidates": proposals})
            self.registry.event(run_id, "model_call_completed", {"stage": "generator", "decision": proposal["decision"]})
            phase, partial_candidate, candidate_version = "proposal", {}, ""
            try:
                self.registry.update_run(run_id, "validating_patch")
                repairs = []
                repairable = {"kernel_contract_missing", "forbidden_import", "forbidden_name", "forbidden_scope",
                              "forbidden_decorator", "forbidden_attribute", "forbidden_call", "patch_context_missing",
                              "empty_patch", "mutable_surface_violation", "patch_too_large", "invalid_patch_syntax",
                              "duplicate_patch_file", "invalid_patch_operation", "task_specific_policy"}
                for repair_index in range(3):
                    self._check_cancel(run_id)
                    try:
                        candidate, patch_meta = self.validator.apply(source, proposal, config)
                        patch_meta["generalization"] = self.validator.check_generalization(source, candidate, training_tasks, config)
                        break
                    except LiquidKernelError as invalid:
                        if invalid.code not in repairable:
                            raise
                        repairs.append({"code": invalid.code, "reason": str(invalid), "details": invalid.details})
                        if repair_index == 2:
                            failed = proposal
                            proposal = self._exploration_proposal(source, optimization_evidence, index)
                            proposal['failed_model_proposal'] = failed
                            proposal['opportunity_audit'] = failed.get('opportunity_audit')
                            candidate, patch_meta = self.validator.apply(source, proposal, config)
                            patch_meta['generalization'] = self.validator.check_generalization(source, candidate, training_tasks, config)
                            proposals[-1] = proposal
                            self.registry.update_run(run_id, 'validating_patch', proposal_json={'candidates': proposals})
                            self.registry.event(run_id, 'architecture_exploration_started', {'candidate_index': index + 1, 'reason': 'model_patch_validation_exhausted'})
                            break
                        self.registry.event(run_id, "candidate_patch_repair_started", {"candidate_index": index + 1, "attempt": repair_index + 1, "code": invalid.code})
                        self.registry.event(run_id, "model_call_started", {"stage": "generator", "candidate_index": index + 1, "attempt": repair_index + 1})
                        repaired = self._call_proposal_model("Repair the proposed agent code using the exact validator diagnostics. Return the complete strict JSON patch against the ORIGINAL kernel_files. Preserve all safety and acceptance rules.",
                                              {**prompt, "previous_proposal": proposal, "validation_errors": repairs},
                                              profile, config["task_benchmark"]["turn_max_tokens"])
                        if repaired.get("decision") != "change" or not str(repaired.get("reason", "")).strip():
                            raise invalid
                        if proposal.get("opportunity_audit"):
                            repaired["opportunity_audit"] = proposal["opportunity_audit"]
                        proposal = repaired
                        proposals[-1] = proposal
                        self.registry.update_run(run_id, "validating_patch", proposal_json={"candidates": proposals})
                patch_meta["validation_repairs"] = repairs
                if _kernel_bundle_hash(candidate) == _kernel_bundle_hash(source):
                    raise LiquidKernelError('empty_patch', 'Candidate must contain actual executable changes')
                candidate_version = self.registry.register_candidate(
                    run_id, incumbent, candidate, mode=config['mode'],
                    changelog=proposal.get('changelog', proposal['reason']), scores={},
                    evaluation={'candidate_index': index + 1, 'decision': 'pending_evaluation', 'candidate': {},
                                'incumbent': dict(baseline_summary), 'patch': patch_meta, 'proposal': proposal})
                candidate_versions[f'candidate_{index + 1}'] = candidate_version
                self.registry.update_run(run_id, 'benchmarking', candidate_version=candidate_version)
                self.registry.event(run_id, 'candidate_registered', {'candidate_index': index + 1, 'candidate_version': candidate_version})
                self._check_cancel(run_id)
                phase = "task"
                self.registry.update_run(run_id, "benchmarking")
                observed = benchmark.run(candidate, bank["tasks"], config["task_benchmark"], f"candidate_{index + 1}")
                previous_training_rollouts = [trajectory_model_view(row) for row in observed["rows"] if row["split"] == "train"]
                _atomic_json(output_root / f"candidate_{index + 1}_rollouts.json", observed)
                # Persist measured artifacts before a reviewer/network failure can
                # interrupt the pair. Missing reviews remain explicitly unscored.
                checkpoint = {"candidate_index": index + 1, "candidate_version": candidate_version, "decision": "pending_review", "incumbent": dict(baseline_summary),
                              "candidate": {"hard": observed["score"], "success_rate": observed["success_rate"],
                                            "score_status": "pending_review", "task_execution_measured": True}}
                partial_candidate = checkpoint["candidate"]
                self.registry.record_candidate_evaluation(candidate_version, checkpoint)
                self.registry.update_run(run_id, "judging", result_json={"incumbent": baseline_summary,
                                         "evaluations": [*evaluations, checkpoint], "tokens_used": self._tokens_used})
                if _json(bank["tasks"]) != _json(json.loads((output_root / "task_bank.json").read_text(encoding="utf-8"))["tasks"]):
                    raise LiquidKernelError("task_bank_changed", "Frozen task bank changed during evaluation", 409)
                self._check_cancel(run_id)
                # Every incumbent-passing holdout assertion remains a gate;
                # a high style score cannot compensate for losing working behavior.
                regressed = []
                baseline_by_id = {row["task_id"]: row for row in baseline["rows"]}
                for row in observed["rows"]:
                    prior = baseline_by_id[row["task_id"]]
                    current_checks = {check["index"]: bool(check["ok"]) for check in row["checks"]}
                    lost_assertion = any(check["ok"] and not current_checks.get(check["index"], False)
                                         for check in prior["checks"])
                    if row["split"] == "holdout" and (lost_assertion or row["score"] < prior["score"] or (prior["success"] and not row["success"])):
                        regressed.append(row["task_id"])
                self.registry.update_run(run_id, "judging")
                phase = "review"
                self.registry.event(run_id, "model_call_started", {"stage": "judge", "kind": "observed_agentic_outcomes"})
                with self._model_budget_scope(phase_tokens, "review"):
                    soft = self._soft_score(source, candidate, bank["tasks"], config,
                                            observations={"incumbent": baseline, "candidate": observed})
                self.registry.event(run_id, "model_call_completed", {"stage": "judge", "scores": {key: soft[key] for key in ("incumbent", "candidate")}})
                flow = compare_agentic_flows(baseline, observed)
                incumbent_mixed = baseline["score"] * .7 + soft["incumbent"] * .2 + 5
                candidate_mixed = observed["score"] * .7 + soft["candidate"] * .2 + 5 + flow['efficiency_delta'] * .05
                gain = candidate_mixed - incumbent_mixed
                # No measured task improvement => no autonomous promotion.
                measured_gain = flow['measured_gain']
                decision = "promote" if flow['eligible'] and gain > 0 and gain >= config["minimum_gain"] else "reject"
                confirmation = {'required': True, 'completed': False, 'passed': False}
                if decision == 'promote':
                    self.registry.event(run_id, 'flow_confirmation_started', {'candidate_index': index + 1, 'task_total': len(bank['tasks'])})
                    repeated_base = benchmark.run(source, bank['tasks'], config['task_benchmark'], 'incumbent_confirmation')
                    repeated_candidate = benchmark.run(candidate, bank['tasks'], config['task_benchmark'], f'candidate_{index + 1}_confirmation')
                    _atomic_json(output_root / f'confirmation_{index + 1}.json', {'incumbent': repeated_base, 'candidate': repeated_candidate})
                    confirmed = compare_agentic_flows(repeated_base, repeated_candidate)
                    repeat_review = self._soft_score(source, candidate, bank['tasks'], config,
                                                     observations={'incumbent': repeated_base, 'candidate': repeated_candidate})
                    repeat_base_score = repeated_base['score'] * .7 + repeat_review['incumbent'] * .2 + 5
                    repeat_candidate_score = repeated_candidate['score'] * .7 + repeat_review['candidate'] * .2 + 5 + confirmed['efficiency_delta'] * .05
                    repeat_gain = repeat_candidate_score - repeat_base_score
                    confirmation = {'required': True, 'completed': True,
                                    'passed': confirmed['eligible'] and confirmed['measured_gain'] >= config['minimum_gain'] and repeat_gain > 0 and repeat_gain >= config['minimum_gain'],
                                    'comparison': confirmed, 'gain': repeat_gain,
                                    'incumbent': {'hard': repeated_base['score'], 'soft': repeat_review['incumbent'], 'mixed': repeat_base_score},
                                    'candidate': {'hard': repeated_candidate['score'], 'soft': repeat_review['candidate'], 'mixed': repeat_candidate_score}}

                    if not confirmation['passed']:
                        decision = 'reject'
                    self.registry.event(run_id, 'flow_confirmation_completed', {'candidate_index': index + 1, 'success': confirmation['passed']})
                result = {"candidate_index": index + 1, "candidate_version": candidate_version, "decision": decision, "gain": gain, "measured_task_gain": measured_gain,
                          "opportunity_audit": proposal.get('opportunity_audit'),
                          "benchmark_kind": "session_agentic", "scoring_protocol_version": SCORING_PROTOCOL_VERSION, "task_bank_fingerprint": frozen_hash,
                          "flow_comparison": flow, "confirmation": confirmation,
                          "train_count": bank["train_count"], "holdout_count": bank["holdout_count"],
                          "incumbent": {"hard": baseline["score"], "soft": soft["incumbent"], "mixed": incumbent_mixed, "score_status": "completed" if rollout_complete(baseline) else "partial", "task_execution_measured": True},
                          "candidate": {"hard": observed["score"], "soft": soft["candidate"], "mixed": candidate_mixed, "score_status": "completed" if rollout_complete(observed) else "partial", "task_execution_measured": True},
                          "patch": patch_meta, "soft_details": soft.get("details", {}),
                          "task_results": [{"task_id": row["task_id"], "split": row["split"], "score": row["score"],
                                            "success": row["success"], "rounds": row["rounds"], "tool_calls": row["tool_calls"],
                                            "checks": row["checks"], "error": row["error"]} for row in observed["rows"]],
                          "reason": "Full agentic workflow quality/efficiency gain passed independent paired confirmation" if decision == "promote" else "Independent paired confirmation failed" if confirmation.get("completed") and not confirmation.get("passed") else "Real task or held-out acceptance regressed" if regressed else "No reproducible agentic workflow improvement"}
                self.registry.record_candidate_evaluation(candidate_version, result)
                evaluations.append(result)
                if decision == "promote":
                    accepted.append((candidate, proposal, result))
            except TimeoutError as exc:
                evaluations.append({"candidate_index": index + 1, "decision": "reject", "code": phase + "_budget_exhausted", "reason": str(exc),
                                    "incumbent": dict(baseline_summary), "candidate": partial_candidate})
            except LiquidKernelError as exc:
                if exc.code not in {"mutable_surface_violation", "patch_too_large", "kernel_contract_missing", "empty_patch",
                                    "forbidden_import", "forbidden_name", "forbidden_scope", "forbidden_decorator", "forbidden_attribute", "forbidden_call", "patch_context_missing", "invalid_patch_syntax", "duplicate_patch_file", "invalid_patch_operation", "task_specific_policy"}:
                    raise
                evaluations.append({"candidate_index": index + 1, "decision": "reject", "code": exc.code, "reason": str(exc),
                                    "details": exc.details,
                                    "incumbent": dict(baseline_summary),
                                    "candidate": {"hard": None, "soft": None, "mixed": 0.0, "validation": 0, "score_status": "validation_failed", "task_execution_measured": False}})
            if candidate_version:
                evaluations[-1]['candidate_version'] = candidate_version
                self.registry.record_candidate_evaluation(candidate_version, evaluations[-1])
            self.registry.update_run(run_id, "judging", result_json={"incumbent": baseline_summary, "evaluations": evaluations, "tokens_used": self._tokens_used})
            self.registry.event(run_id, "candidate_evaluated", {"candidate_index": index + 1, "decision": evaluations[-1]["decision"]})
        if not accepted:
            changed = any(proposal["decision"] == "change" for proposal in proposals) or any(row.get('decision')=='reject' for row in evaluations)
            status = "rejected" if changed else "no_change"
            result = {"decision": status, "benchmark_kind": "session_agentic", "scoring_protocol_version": SCORING_PROTOCOL_VERSION, "task_bank_fingerprint": frozen_hash,
                      "evaluations": evaluations, "incumbent": evaluations[-1].get("incumbent", baseline_summary) if evaluations else baseline_summary, "tokens_used": self._tokens_used, "case_count": len(bank["tasks"])}
            self.registry.update_run(run_id, status, result_json=result, completed_at=_now())
            self.registry.event(run_id, status, {"benchmark_kind": "session_agentic"})
            return
        candidate, proposal, result = max(accepted, key=lambda item: item[2]["gain"])
        result = {**result, "evaluations": evaluations, "tokens_used": self._tokens_used, "candidate_count": len(proposals)}
        with self.config_lock:
            self._check_cancel(run_id)
            if self.registry.active_version() != incumbent:
                raise LiquidKernelError("baseline_changed", "Active baseline changed during evaluation; rerun against the new baseline before deployment", 409)
            version = result["candidate_version"]
            result["candidate_version"] = version
            status = "canary" if config["auto_promote"] else "awaiting_approval"
            if config["auto_promote"]:
                self.registry.begin_canary(version, 5)
            self.registry.update_run(run_id, status, candidate_version=version, result_json=result, completed_at=_now())
            self.registry.event(run_id, status, {"candidate_version": version, "gain": result["gain"], "benchmark_kind": "session_agentic"})

    def _run(self, run_id: str, config: dict) -> None:
        self._active_run_config = config
        try:
            self._active_deadline = (time.monotonic()+config["budget"]["timeout_seconds"]) if config["budget"]["timeout_seconds"] and config.get("task_benchmark",{}).get("enabled",True) else 0
            incumbent = self.registry.active_version()
            source = self.registry.sources(incumbent)
            self.registry.update_run(run_id, "collecting")
            self.registry.event(run_id, "collecting", {"versions": int(config["history_version_depth"]) + 1})
            experience_config = {**config, "_run_id": run_id}
            experience = self._experience(experience_config, incumbent)
            _atomic_json(self.registry.experience_root / run_id / "manifest.json", experience)
            self.registry.update_run(run_id, "assessing", experience_json=self._experience_audit_view(experience))
            self._check_cancel(run_id)
            if config.get("task_benchmark", {}).get("enabled", True):
                self._run_task_driven(run_id, config, incumbent, source, experience)
                return
            system = (
                "You are the Liquid Agent Kernel evolution designer. Assess whether the incumbent should change. "
                "Return strict JSON. Never alter authentication, persistence, evaluator, promotion, audit, sandbox, or signing controls."
            )
            seed = random.SystemRandom().randint(1, 2**31 - 1)
            candidate_limit = max(1, int(config["budget"].get("candidate_limit", 1) or 1))
            generator_tokens = config["task_benchmark"]["turn_max_tokens"]
            prompt_cases = self.benchmark.random_cases(
                min(max(8, int(config["budget"]["max_cases"]) // 2), int(config["budget"]["max_cases"])),
                seed,
            )
            proposals: list[dict] = []
            evaluations: list[dict] = []
            accepted: list[tuple[dict[str, str], dict, dict, dict]] = []
            for candidate_index in range(candidate_limit):
                self._check_cancel(run_id)
                prompt = _json({
                    "task": "Assess the complete incumbent kernel and historical experience. Return no_change or a structured patch proposal.",
                    "candidate_index": candidate_index + 1,
                    "candidate_limit": candidate_limit,
                    "previous_candidate_summaries": [
                        {"decision": row.get("decision"), "reason": row.get("reason"), "changelog": row.get("changelog")}
                        for row in proposals
                    ],
                    "mode": config["mode"],
                    "mutable_surface": config["mutable_surface"],
                    "allowed_patch_files": sorted(self.validator.allowed_files(config)),
                    "kernel_files": source,
                    "experience": experience,
                    "benchmark_cases": prompt_cases,
                    "immutable_control_components": list(IMMUTABLE_CONTROL_COMPONENTS),
                    "output_schema": {
                        "decision": "no_change|change",
                        "reason": "string",
                        "changelog": "markdown",
                        "case_families": ["string"],
                        "benchmark_cases": [{
                            "id": "short stable identifier",
                            "role": "agent role",
                            "intent": "task or failure mode to exercise",
                            "constraints": ["observable requirement"],
                            "expected": "expected safe behavior",
                        }],
                        "patch": {
                            "files": [{
                                "path": "|".join(sorted(self.validator.allowed_files(config))),
                                "operation": "replace|replace_file",
                                "old": "string",
                                "new": "string",
                                "content": "string",
                            }]
                        },
                    },
                })
                self.registry.update_run(run_id, "generating")
                self.registry.event(run_id, "model_call_started", {"stage": "generator", "candidate_index": candidate_index + 1, "model": config.get("generator_model_ref")})
                proposal = self._call_proposal_model(
                    system, prompt,
                    config.get("generator_model_ref") or str(config.get("generator_profile", "")),
                    generator_tokens,
                )
                self._check_cancel(run_id)
                if proposal.get("decision") not in {"change", "no_change"} or not str(proposal.get("reason", "")).strip():
                    raise LiquidKernelError("invalid_model_output", "Evolution model must return change or no_change with a reason")
                self.registry.event(run_id, "model_call_completed", {"stage": "generator", "model": config.get("generator_model_ref"), "decision": proposal["decision"]})
                proposals.append(proposal)
                self.registry.update_run(run_id, "proposal_ready", proposal_json={"candidates": proposals})
                self.registry.event(run_id, "proposal_ready", {
                    "candidate_index": candidate_index + 1,
                    "decision": proposal.get("decision", ""),
                })

            cases = self._benchmark_cases(proposals, int(config["budget"]["max_cases"]), seed)
            for candidate_index, proposal in enumerate(proposals):
                self._check_cancel(run_id)
                decision = str(proposal.get("decision", "no_change"))
                if decision == "error":
                    continue
                if decision != "change":
                    evaluations.append({"candidate_index": candidate_index + 1, "decision": "no_change", "reason": str(proposal.get("reason", ""))})
                    continue
                try:
                    self.registry.update_run(run_id, "validating_patch")
                    candidate_source, result, scores = self._evaluate_candidate(
                        run_id, source, proposal, config, cases, seed
                    )
                    result["candidate_index"] = candidate_index + 1
                    evaluations.append(dict(result))
                    self.registry.event(run_id, "candidate_evaluated", {
                        "candidate_index": candidate_index + 1,
                        "decision": result.get("decision", ""),
                        "gain": result.get("gain", 0),
                        "patch": result.get("patch", {}),
                    })
                    if result["decision"] == "promote":
                        accepted.append((candidate_source, proposal, result, scores))
                except LiquidKernelError as exc:
                    if exc.code in {"run_cancelled", "judge_call_failed", "model_call_failed", "invalid_model_output", "invalid_judge_output", "judge_unavailable", "model_profile_missing", "model_config_changed", "model_owner_disabled", "model_missing"}:
                        raise
                    rejected = {
                        "candidate_index": candidate_index + 1,
                        "decision": "reject",
                        "reason": str(exc),
                        "code": exc.code,
                        "details": exc.details,
                    }
                    evaluations.append(rejected)
                    self.registry.event(run_id, "candidate_rejected", rejected)
            if not accepted:
                changed = any(str(proposal.get("decision", "")) == "change" for proposal in proposals)
                generation_failed = any(str(proposal.get("decision", "")) == "error" for proposal in proposals)
                status = "failed" if generation_failed else "rejected" if changed else "no_change"
                result = {
                    "decision": status,
                    "reason": (
                        "No candidate exceeded the promotion threshold."
                        if changed
                        else "Candidate generation failed."
                        if generation_failed
                        else "No beneficial change identified."
                    ),
                    "candidate_count": candidate_limit,
                    "evaluations": evaluations,
                    "random_seed": seed,
                    "case_count": len(cases),
                }
                with self.config_lock:
                    self._check_cancel(run_id)
                    self.registry.update_run(run_id, status, result_json=result, completed_at=_now())
                    self.registry.event(run_id, status, {"candidate_count": candidate_limit, "reason": result["reason"]})
                return
            candidate_source, proposal, result, scores = max(
                accepted,
                key=lambda item: float(item[2].get("gain", float("-inf")) or float("-inf")),
            )
            result["candidate_count"] = candidate_limit
            result["evaluations"] = evaluations
            with self.config_lock:
                self._check_cancel(run_id)
                version = self.registry.register_candidate(
                    run_id, incumbent, candidate_source, mode=config["mode"],
                    changelog=str(proposal.get("changelog", "") or proposal.get("reason", "Candidate kernel update.")), scores=scores,
                )
                result["candidate_version"] = version
                # The retained internal contract evaluator is diagnostic only.
                # Automatic deployment requires the real paired task pathway.
                status = "awaiting_approval"
                result["automatic_deployment_eligible"] = False
                # Complete the control-plane deployment before publishing the
                # terminal run state. Observers use the run status as a readiness
                # signal; publishing ``canary`` first can let them tear down a
                # temporary registry while this thread is still opening SQLite.
                self.registry.update_run(run_id, status, candidate_version=version, result_json=result, completed_at=_now())
                self.registry.event(run_id, status, {"candidate_version": version, "gain": result.get("gain", 0)})
        except (LiquidKernelError, EvaluationDefinitionError) as exc:
            status = "cancelled" if exc.code == "run_cancelled" or run_id in self.cancelled else "failed"
            self.registry.update_run(run_id, status, error=str(exc), result_json={**self.registry.run_detail(run_id).get("result", {}), "code": exc.code, "details": exc.details}, completed_at=_now())
            self.registry.event(run_id, status, {"code": exc.code, "error": str(exc)})
        except Exception as exc:
            status = "cancelled" if run_id in self.cancelled else "failed"
            error = "Evolution computation failed (" + type(exc).__name__ + ")"
            self.registry.update_run(run_id, status, error=error, result_json={**self.registry.run_detail(run_id).get("result", {}), "code": "run_failed"}, completed_at=_now())
            self.registry.event(run_id, status, {"error": error})
        finally:
            detail = self.registry.run_detail(run_id)
            if detail['status'] in {'failed', 'cancelled'}:
                with self.registry._connect() as conn:
                    retained = conn.execute('SELECT version,evaluation_json FROM candidate_evaluations WHERE run_id=?', (run_id,)).fetchall()
                for row in retained:
                    saved = json.loads(row['evaluation_json'])
                    if saved.get('decision') in {'pending_evaluation', 'pending_review'}:
                        self.registry.record_candidate_evaluation(row['version'], {'decision': 'reject', 'code': detail.get('result', {}).get('code'), 'reason': detail.get('error')})
            self._active_run_config = None
            self._active_deadline = 0
            self._rollout_token_ceiling = 0
            self._token_limit = 0
            self._token_budget_exhausted = False
            self.cancelled.discard(run_id)
            self.active_run_id = ""
            try:
                self.run_lock.release()
            except Exception:
                pass

    def approve(self, run_id: str) -> dict:
        with self.config_lock:
            if self.config()["mode"] == "Off":
                raise LiquidKernelError("evolution_disabled", "liquid-kernel evolution is Off", 409)
            detail = self.registry.run_detail(run_id)
            if detail["status"] != "awaiting_approval":
                raise LiquidKernelError("invalid_run_state", "run is not awaiting approval", 409)
            if detail.get('score_summary', {}).get('evaluation_valid') is False:
                raise LiquidKernelError('invalid_evaluation_definition', 'Invalid evaluation evidence cannot authorize deployment', 409)
            if detail.get("incumbent_version") != self.registry.active_version():
                raise LiquidKernelError("baseline_changed", "Active baseline changed during evaluation; rerun against the new baseline before deployment", 409)
            version = str(detail.get("candidate_version", "") or "")
            state = self.registry.begin_canary(version, 5)
            self.registry.update_run(run_id, "canary")
            self.registry.event(run_id, "approved", {"candidate_version": version, "canary_percent": 5})
            return {"ok": True, "run_id": run_id, "state": state}

    def reject(self, run_id: str, reason: str = "") -> dict:
        with self.config_lock:
            detail = self.registry.run_detail(run_id)
            if detail["status"] not in {"awaiting_approval", "canary"}:
                raise LiquidKernelError("invalid_run_state", "run cannot be rejected in its current state", 409)
            rollback = None
            if detail["status"] == "canary":
                rollback = self.registry.abort_canary(reason=str(reason or "Rejected by administrator."))
            self.registry.update_run(run_id, "rejected", error=str(reason or "Rejected by administrator."), completed_at=_now())
            self.registry.event(run_id, "admin_rejected", {"reason": str(reason or ""), "rollback": rollback})
            return {"ok": True, "run_id": run_id, "status": "rejected", "rollback": rollback}

    def observe_session_result(
        self,
        version: str,
        *,
        success: bool,
        duration_seconds: float,
        error: bool = False,
        retry: bool = False,
    ) -> dict:
        config = self.config()
        observed = self.registry.observe_session_result(
            version,
            success=success,
            duration_seconds=duration_seconds,
            error=error,
            canary_policy=config.get("canary", {}),
        )
        self.observations.append({"ts": _now(), "error": bool(error), "retry": bool(retry)})
        if observed.get("observed") or config["mode"] == "Off" or not bool(config.get("event_triggers", True)):
            return observed
        recent = [row for row in self.observations if _now() - float(row.get("ts", 0) or 0) <= 3600]
        if len(recent) < 20 or self.active_run_id:
            return observed
        error_rate = sum(int(bool(row.get("error"))) for row in recent) / len(recent)
        retry_rate = sum(int(bool(row.get("retry"))) for row in recent) / len(recent)
        runs = self.registry.list_runs(limit=1).get("runs", [])
        last_created = float(runs[0].get("created_at", 0) or 0) if runs else 0.0
        cooldown_ready = _now() - last_created >= int(config.get("cooldown_hours", 0) or 0) * 3600
        if cooldown_ready and (
            error_rate >= float(config.get("event_error_rate_threshold", 0.12) or 0.12)
            or retry_rate >= float(config.get("event_retry_rate_threshold", 0.18) or 0.18)
        ):
            try:
                trigger = self.trigger("metric")
                observed["evolution_trigger"] = trigger
            except LiquidKernelError as exc:
                self.last_trigger_error = {"code": exc.code, "error": str(exc), "trigger": "metric", "at": _now()}
        return observed

    def emergency_off(self) -> dict:
        current = self.config()
        saved = self.save_config({**current, "mode": "Off", "schedule": "off"}, expected_revision=int(current.get("revision", 0) or 0))
        rollback = self.registry.abort_canary(reason="administrator emergency stop")
        return {
            "ok": True,
            "config": saved["config"],
            "cancelled_run_id": str(self.active_run_id or ""),
            "rollback": rollback,
        }

    def dashboard(self) -> dict:
        with self.config_lock:
            if not self.run_lock.locked():
                self._recover_interrupted_runs()
        runs = self.registry.list_runs(limit=50)
        latest_id = runs['runs'][0]['run_id'] if runs['runs'] else ''
        latest_progress = self.registry.run_detail(self.active_run_id or latest_id).get('progress') if (self.active_run_id or latest_id) else None
        return {
            "ok": True,
            "config": self.config(),
            "active": self.registry.active_state(),
            "active_run_id": self.active_run_id,
            "active_progress": latest_progress if self.active_run_id else None,
            "latest_progress": latest_progress,
            "last_trigger_error": self.last_trigger_error,
            "runs": runs,
            "versions": self.registry.list_versions(limit=100),
            "events": self.registry.events_since(0, limit=200),
            "immutable_control_components": list(IMMUTABLE_CONTROL_COMPONENTS),
        }
