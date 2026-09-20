# Liquid Agent Kernel

The liquid agent kernel is the versioned policy and harness layer used by Clouds Coder sessions. It is intentionally separated from the immutable control plane that authenticates administrators, stores artifacts, validates candidates, runs evaluations, signs versions, performs Canary rollout, and rolls back regressions.

## Modes

| Mode | Automatic schedule | Mutable surface | Promotion policy |
| --- | --- | --- | --- |
| `Off` | Disabled | None | Runs are rejected |
| `Tuning` | Weekly | Tool and prompt policy plus entrypoint | Starts Canary automatically after passing evaluation |
| `Thinking` | Every three days | Tool and prompt policy plus entrypoint | Requires Admin approval before Canary |
| `Aggressive` | Daily | Complete extracted tool/prompt/harness core | Requires Admin approval before Canary |

Admin may override the schedule. The mode and schedule are available both in the Admin Evolution view and as startup options:

```text
--liquid-kernel-mode Off|Tuning|Thinking|Aggressive
--evolution-schedule off|hourly|daily|every_3_days|weekly
```

The application embeds a compressed copy of this package inside `Clouds_Coder.py`. On startup it uses a complete local package when present and atomically restores the embedded copy when the package is missing or incomplete. The Admin startup setting `liquid_kernel_startup_policy` accepts `inherit` (the default) or `inject`: `inherit` keeps the persisted registry and session-pinned versions, while `inject` adds the embedded kernel as a new promoted version without deleting the existing registry or breaking old sessions.

## Version Boundary

Each immutable artifact contains:

- `kernel.py`: version contract and exported hooks.
- `tool_policy.py`: tool visibility and selection policy.
- `prompt_policy.py`: system-prompt augmentation policy.
- `harness.py`: run, round, and post-tool hooks.
- `manifest.json`: parent, hashes, contract version, mode, and HMAC signature.
- `CHANGELOG.md`: user-visible upgrade log.

Authentication, persistence, evaluation, promotion, audit, signing, and sandbox code never belongs to the mutable artifact. Controlled modes cannot patch `harness.py`; only `Aggressive` may change the full extracted core.

## Evolution Pipeline

1. Select the active kernel and its two parent versions by default.
2. Read the configured user, session, and date scope; the default scope is all users, all sessions, and all dates.
3. Separate experience records by pinned kernel version and redact recognized secrets.
4. Ask the configured generator profile for one or more independently generated candidates, according to the mode budget; a failed model request fails the run and cannot become `no_change`.
5. Require each changed candidate to return a structured patch and optional benchmark cases that exercise the problems it intends to solve.
6. Enforce file, line, token, case, and timeout budgets and reject immutable-boundary violations.
7. Merge sanitized model-designed cases with randomized cases under a fixed capacity, then run every incumbent/candidate comparison against the same case set in separate isolated Python processes.
8. Combine deterministic results at 30% with an independent blind LLM judge at 70%, and retain only the highest-gain passing candidate.
9. Repeat deterministic evaluation once when the candidate regresses by more than 5%; reject after a second regression.
10. Start a `5% → 25% → 100%` Canary. New sessions are assigned by stable hash, while existing sessions remain pinned.
11. Promote only after the 100% stage or roll back automatically when success, error, or latency limits regress.

Every run and state transition is recorded in the SQLite registry with a hash-linked event chain. Promoted artifacts are copied to the backup directory. WebUI and IDE notices are acknowledged independently per user, device, and surface.

## History Policy

`history_version_depth` counts parent versions in addition to the current version. Its default value is `2`. `history_access` defaults to `full`; user and session scopes both default to `*`. Optional start and end dates filter individual message timestamps in the configured timezone. Records remain grouped by their pinned kernel version. Experience metadata is stored in the run registry, while raw redacted records are kept only in the protected per-run manifest and JSONL archive.

## Safety Operations

The Admin `Emergency Off` action atomically changes the mode to `Off`, requests cancellation of an active evolution run, and aborts any current Canary. A candidate cannot be promoted directly: it must reach the 100% Canary stage. Artifact hashes and signatures are checked every time a version is loaded.


## Source-bound models (capability version 2)

`GET /api/admin/evolution/models` requires Admin authentication. Its options combine the global model directory, the current Agent user's encrypted profiles, and the authenticated IDE account's encrypted profiles. IDE ownership comes from the existing verified session cookie or `X-Evolution-IDE-Token`; an IP address never substitutes for IDE authentication. Directory reads use the existing provider cache without starting remote probes.

`generator_model_ref` and `judge_model_ref` contain `source`, `owner`, `profile_id`, `model`, and an HMAC fingerprint of the effective invocation configuration. Credentials remain in their original configuration store. Equivalent configurations are merged within a source; different addresses, credentials, or invocation settings keep separate options. The same model can generate and judge through independent requests. Legacy profile IDs remain supported and empty references explicitly inherit the global default.

Save and start are separate operations. Both Admin requests require a saved `revision`; concurrent updates receive HTTP 409. The editor keeps its own base revision and unsaved values while status polling continues. A run resolves and fixes both concrete models before task creation. Deleted profiles, disabled IDE accounts, changed invocation settings, and unknown model IDs fail explicitly. Restarting or signing out does not revoke an already saved private-model reference; disabling its owning account does.

Runs record `generating` and `judging` phases, sanitized model references, results, and errors. Missing or invalid judge scores fail instead of receiving a neutral score. Interrupted computation records are marked failed after restart, while approval and Canary history remain intact. Database task/event creation is atomic; failed task creation, failed thread startup, cancellation completion, and worker exceptions release the run lock.

Standalone startup checks `EVOLUTION_MODEL_CAPABILITY_VERSION`. An older package is backed up under `.package-backups/` before replacing code files. Existing runtime configuration, registry records, signing keys, artifacts, and version history stay in place. Rebuild both entrypoints' embedded packages with `python tools/sync_liquid_kernel_bundle.py`.

Verification commands are recorded in `docs/evolution_verification.md`. Live acceptance is opt-in through `tools/verify_evolution_real.py`; it uses a temporary runtime, one candidate, at most 4096 generation tokens and 2048 judge tokens, and the manual-approval mode without deployment.
