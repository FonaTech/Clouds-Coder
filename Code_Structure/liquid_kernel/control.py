from __future__ import annotations

import ast
import hashlib
import hmac
import importlib.util
import json
import math
import os
import random
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from zoneinfo import ZoneInfo


EVOLUTION_MODES = ("Off", "Tuning", "Thinking", "Aggressive")
CONTROL_SCHEMA_VERSION = 1
EVOLUTION_MODEL_CAPABILITY_VERSION = 2
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

CONTROLLED_KERNEL_FILES = frozenset({"kernel.py", "tool_policy.py", "prompt_policy.py"})
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
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def _read_json(path: Path, fallback: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def _atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    try:
        os.chmod(temp, 0o600)
    except Exception:
        pass
    os.replace(temp, path)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _normalize_kernel_files(value: object) -> dict[str, str]:
    if isinstance(value, str):
        return {"kernel.py": value}
    if not isinstance(value, dict):
        raise LiquidKernelError("invalid_kernel_bundle", "kernel artifact must be source text or a file map")
    files: dict[str, str] = {}
    for raw_path, raw_source in value.items():
        path = str(raw_path or "").strip().replace("\\", "/")
        if not path or path.startswith("/") or ".." in Path(path).parts or "/" in path:
            raise LiquidKernelError("invalid_kernel_path", "kernel artifact contains an invalid file path")
        files[path] = str(raw_source or "")
    if "kernel.py" not in files:
        raise LiquidKernelError("kernel_contract_missing", "kernel artifact is missing kernel.py")
    return files


def _kernel_file_hashes(files: dict[str, str]) -> dict[str, str]:
    return {path: _sha256_bytes(source.encode("utf-8")) for path, source in sorted(files.items())}


def _kernel_bundle_hash(files: dict[str, str]) -> str:
    return _sha256_bytes(_json(_kernel_file_hashes(files)).encode("utf-8"))


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
        "max_changed_lines": 400,
        "max_cases": 36,
        "max_tokens": 48_000,
        "timeout_seconds": 3600,
        "mutable_surface": "controlled",
        "auto_promote": True,
        "minimum_gain": 1.5,
    },
    "Thinking": {
        "schedule": "every_3_days",
        "cooldown_hours": 48,
        "candidate_limit": 2,
        "max_files": 12,
        "max_changed_lines": 1200,
        "max_cases": 72,
        "max_tokens": 120_000,
        "timeout_seconds": 7200,
        "mutable_surface": "controlled",
        "auto_promote": False,
        "minimum_gain": 3.0,
    },
    "Aggressive": {
        "schedule": "daily",
        "cooldown_hours": 24,
        "candidate_limit": 3,
        "max_files": 30,
        "max_changed_lines": 4000,
        "max_cases": 120,
        "max_tokens": 240_000,
        "timeout_seconds": 14_400,
        "mutable_surface": "full_agent_core",
        "auto_promote": False,
        "minimum_gain": 5.0,
    },
}


HARD_BUDGET_LIMITS = {
    "candidate_limit": 3,
    "max_files": 30,
    "max_changed_lines": 4000,
    "max_cases": 160,
    "max_tokens": 300_000,
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
        "minimum_gain": preset["minimum_gain"],
        "hard_score_weight": 0.30,
        "soft_score_weight": 0.70,
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
    supplied_budget = (
        {}
        if mode_changed
        else out.get("budget", {}) if isinstance(out.get("budget"), dict) else {}
    )
    budget: dict[str, int] = {}
    for key, hard_limit in HARD_BUDGET_LIMITS.items():
        default_value = int(preset[key])
        requested = int(supplied_budget.get(key, default_value) or 0)
        budget[key] = max(0, min(int(hard_limit), requested))
    out["budget"] = budget
    out["mutable_surface"] = str(preset["mutable_surface"])
    out["auto_promote"] = bool(preset["auto_promote"])
    minimum_gain_source = preset["minimum_gain"] if mode_changed else out.get("minimum_gain")
    out["minimum_gain"] = max(float(preset["minimum_gain"]), float(minimum_gain_source or 0.0))
    out["hard_score_weight"] = 0.30
    out["soft_score_weight"] = 0.70
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
        return hmac.new(self.signing_key, _json(manifest).encode("utf-8"), hashlib.sha256).hexdigest()

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
                (target / path).write_text(source, encoding="utf-8")
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
        bucket = int(hashlib.sha256(f"{user_id}|{session_id}|{candidate}".encode("utf-8")).hexdigest()[:8], 16) % 100
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
                if _sha256_bytes(source.encode("utf-8")) != str(expected_hash or ""):
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

    def register_candidate(self, run_id: str, parent: str, source: str | dict[str, str], *, mode: str, changelog: str, scores: dict) -> str:
        files = _normalize_kernel_files(source)
        digest = _kernel_bundle_hash(files)
        with self._connect() as conn:
            sequence = int(conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0]) + 1
        version = f"kernel-{sequence:04d}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{digest[:8]}"
        staging = self.candidates_root / run_id / version
        staging.mkdir(parents=True, exist_ok=False)
        for path, file_source in files.items():
            (staging / path).write_text(file_source, encoding="utf-8")
        manifest = self._manifest(
            version,
            parent,
            digest,
            mode=mode,
            source=f"evolution:{run_id}",
            files=files,
        )
        _atomic_json(staging / "manifest.json", manifest)
        (staging / "CHANGELOG.md").write_text(str(changelog or "Candidate kernel update."), encoding="utf-8")
        target = self.artifacts_root / version
        os.replace(staging, target)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO versions(version,parent_version,status,source_hash,manifest_json,changelog,hard_score,soft_score,mixed_score,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (version, parent, "candidate", digest, _json(manifest), str(changelog or ""), float(scores.get("hard", 0)), float(scores.get("soft", 0)), float(scores.get("mixed", 0)), _now()),
            )
        return version

    def begin_canary(self, version: str, percent: int = 5) -> dict:
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
        with self._connect() as conn:
            self._event(conn, run_id, kind, payload)

    def _event(self, conn, run_id: str, kind: str, payload: dict) -> None:
        now = _now()
        previous = conn.execute("SELECT event_hash FROM run_events ORDER BY event_id DESC LIMIT 1").fetchone()
        previous_hash = str(previous[0] if previous else "")
        material = _json({"run_id": run_id, "kind": kind, "payload": payload, "previous_hash": previous_hash, "created_at": now})
        event_hash = hashlib.sha256(material.encode("utf-8")).hexdigest()
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

    def run_detail(self, run_id: str) -> dict:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM runs WHERE run_id=?", (run_id,)).fetchone()
            if not row:
                raise LiquidKernelError("run_not_found", "evolution run not found", 404)
            events = [dict(item) for item in conn.execute(
                "SELECT event_id,kind,payload_json,event_hash,created_at FROM run_events WHERE run_id=? ORDER BY event_id", (run_id,)
            ).fetchall()]
        out = dict(row)
        for key in ("config_json", "experience_json", "proposal_json", "result_json"):
            out[key[:-5]] = json.loads(out.pop(key, "{}") or "{}")
        for event in events:
            event["payload"] = json.loads(event.pop("payload_json", "{}") or "{}")
        out["events"] = events
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
    }

    @staticmethod
    def allowed_files(config: dict) -> frozenset[str]:
        return FULL_AGENT_CORE_FILES if str(config.get("mode", "")) == "Aggressive" else CONTROLLED_KERNEL_FILES

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
        tree = ast.parse(source, filename=path)
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
            if not isinstance(item, dict) or path not in allowed_files:
                raise LiquidKernelError("mutable_surface_violation", "candidate attempted to modify an immutable file")
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
        if changed_lines > int(budget["max_changed_lines"]):
            raise LiquidKernelError("patch_too_large", "candidate exceeds the changed-line budget")
        unexpected = sorted(set(current) - FULL_AGENT_CORE_FILES)
        if unexpected:
            raise LiquidKernelError("mutable_surface_violation", "kernel bundle contains unsupported files", details={"files": unexpected})
        for path, file_source in current.items():
            self._validate_ast(path, file_source, FULL_AGENT_CORE_FILES)
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

payload = json.loads(sys.stdin.read() or "{}")
with tempfile.TemporaryDirectory(prefix="liquid-kernel-benchmark-") as temp:
    root = pathlib.Path(temp)
    for relative, source in dict(payload.get("files") or {}).items():
        (root / relative).write_text(str(source or ""), encoding="utf-8")
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
                [sys.executable, "-I", "-S", "-c", runner],
                input=_json(payload),
                text=True,
                capture_output=True,
                timeout=max(0.5, float(timeout_seconds or 15.0)),
                env={"PYTHONIOENCODING": "utf-8", "PYTHONNOUSERSITE": "1"},
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
            return normalize_evolution_config(_read_json(self.config_path, {}))

    def save_config(self, values: object, expected_revision: int = 0, *, context=None) -> dict:
        with self.config_lock:
            current = self.config()
            if expected_revision and int(current.get("revision", 0)) != int(expected_revision):
                raise LiquidKernelError("config_conflict", "evolution config changed; reload before saving", 409)
            clean = normalize_evolution_config(values, current=current)
            if self.config_validator:
                clean = self.config_validator(clean, context=context, current=current)
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

    def inject_embedded_kernel(self, reason: str = "administrator selected embedded kernel") -> dict:
        """Install the bundled kernel without deleting version or session history."""
        incumbent = self.registry.active_version()
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

    def _call_model(self, system: str, prompt: str, profile: str, max_tokens: int) -> dict:
        if not callable(self.model_callback):
            raise LiquidKernelError("model_unavailable", "Evolution model callback is not configured.")
        result = self.model_callback(system, prompt, profile, max_tokens)
        if not isinstance(result, dict):
            raise LiquidKernelError("invalid_model_output", "evolution model did not return a JSON object")
        return result

    def _experience(self, config: dict, incumbent: str) -> dict:
        versions = self.registry.lineage_versions(incumbent, int(config["history_version_depth"]))
        if callable(self.experience_provider):
            result = self.experience_provider(config, incumbent, versions)
            if isinstance(result, dict):
                return result
        return {"versions": versions, "records": [], "record_count": 0, "note": "No experience provider configured."}

    @staticmethod
    def _experience_audit_view(experience: dict) -> dict:
        audit = {key: value for key, value in dict(experience or {}).items() if key not in {"records", "history_by_version"}}
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
    ) -> dict:
        incumbent_files = _normalize_kernel_files(incumbent_source)
        candidate_files = _normalize_kernel_files(candidate_source)
        if callable(self.judge_callback):
            result = self.judge_callback(
                {
                    "incumbent_source": _kernel_bundle_text(incumbent_files),
                    "candidate_source": _kernel_bundle_text(candidate_files),
                    "incumbent_files": incumbent_files,
                    "candidate_files": candidate_files,
                    "cases": cases,
                },
                config.get("judge_model_ref") or str(config.get("judge_profile", "")),
                min(16_000, int(config["budget"]["max_tokens"]), int(config.get("_judge_token_limit", 16_000))),
            )
            if isinstance(result, dict):
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
                case["nonce"] = int(hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:8], 16)
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

    def _run(self, run_id: str, config: dict) -> None:
        try:
            incumbent = self.registry.active_version()
            source = self.registry.sources(incumbent)
            self.registry.update_run(run_id, "collecting")
            self.registry.event(run_id, "collecting", {"versions": int(config["history_version_depth"]) + 1})
            experience_config = {**config, "_run_id": run_id}
            experience = self._experience(experience_config, incumbent)
            _atomic_json(self.registry.experience_root / run_id / "manifest.json", experience)
            self.registry.update_run(run_id, "assessing", experience_json=self._experience_audit_view(experience))
            self._check_cancel(run_id)
            system = (
                "You are the Liquid Agent Kernel evolution designer. Assess whether the incumbent should change. "
                "Return strict JSON. Never alter authentication, persistence, evaluator, promotion, audit, sandbox, or signing controls."
            )
            seed = random.SystemRandom().randint(1, 2**31 - 1)
            candidate_limit = max(1, int(config["budget"].get("candidate_limit", 1) or 1))
            generator_tokens = max(512, int(config["budget"]["max_tokens"]) // candidate_limit)
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
                proposal = self._call_model(
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
                status = "canary" if bool(config["auto_promote"]) else "awaiting_approval"
                # Complete the control-plane deployment before publishing the
                # terminal run state. Observers use the run status as a readiness
                # signal; publishing ``canary`` first can let them tear down a
                # temporary registry while this thread is still opening SQLite.
                if bool(config["auto_promote"]):
                    self.registry.begin_canary(version, 5)
                self.registry.update_run(run_id, status, candidate_version=version, result_json=result, completed_at=_now())
                self.registry.event(run_id, status, {"candidate_version": version, "gain": result.get("gain", 0)})
        except LiquidKernelError as exc:
            status = "cancelled" if exc.code == "run_cancelled" or run_id in self.cancelled else "failed"
            self.registry.update_run(run_id, status, error=str(exc), result_json={"code": exc.code, "details": exc.details}, completed_at=_now())
            self.registry.event(run_id, status, {"code": exc.code, "error": str(exc)})
        except Exception as exc:
            status = "cancelled" if run_id in self.cancelled else "failed"
            error = "Evolution computation failed (" + type(exc).__name__ + ")"
            self.registry.update_run(run_id, status, error=error, result_json={"code": "run_failed"}, completed_at=_now())
            self.registry.event(run_id, status, {"error": error})
        finally:
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
        return {
            "ok": True,
            "config": self.config(),
            "active": self.registry.active_state(),
            "active_run_id": self.active_run_id,
            "last_trigger_error": self.last_trigger_error,
            "runs": self.registry.list_runs(limit=50),
            "versions": self.registry.list_versions(limit=100),
            "events": self.registry.events_since(0, limit=200),
            "immutable_control_components": list(IMMUTABLE_CONTROL_COMPONENTS),
        }
