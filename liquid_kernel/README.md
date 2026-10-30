# Liquid Agent Kernel

The liquid agent kernel is the versioned policy and harness layer used by Clouds Coder sessions. It is intentionally separated from the immutable control plane that authenticates administrators, stores artifacts, validates candidates, runs evaluations, signs versions, performs Canary rollout, and rolls back regressions.

## Modes

| Mode | Automatic schedule | Mutable surface | Promotion policy |
| --- | --- | --- | --- |
| `Off` | Disabled | None | Runs are rejected |
| `Tuning` | Weekly | Entrypoint, tool/prompt/context/recovery modules | Starts Canary automatically after passing evaluation |
| `Thinking` | Every three days | Planning, memory, routing, recovery, verification and state modules | Requires Admin approval before Canary |
| `Aggressive` | Daily | Full extracted core, harness and new core_<name>.py modules | Requires Admin approval before Canary |

Admin may override the schedule and choose `deployment_policy=mode|automatic|manual` independently of edit strength. Automatic means eligible candidates enter the existing 5% → 25% → 100% Canary rollout, with its regression rollback controls. The default `mode` policy preserves the table above. Only the completed real task pathway can deploy automatically; the retained internal contract evaluator is diagnostic and requires manual approval.

Admin may override the schedule. The mode and schedule are available both in the Admin Evolution view and as startup options:

```text
--liquid-kernel-mode Off|Tuning|Thinking|Aggressive
--evolution-schedule off|hourly|daily|every_3_days|weekly
```

The application embeds a compressed copy of this package inside `Clouds_Coder.py`. On startup it diagnoses the framework capability and content, backs up and upgrades an older/incomplete framework, and preserves a compatible newer framework. The Admin startup setting `liquid_kernel_startup_policy` accepts `inherit` (the default) or `inject`: `inherit` keeps the persisted registry and session-pinned versions, while `inject` may initialize the embedded baseline but preserves an evolved active kernel or Canary. An explicit force reset is required to replace an evolved kernel.

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

1. Select the active signed kernel and configured lineage/history scope.
2. Collect redacted human turns, including recent corrections even if the broad history prompt budget is full.
3. Synthesize self-contained multi-turn tasks and freeze a source-session-separated training/holdout split.
4. Execute the incumbent with real model turns and workspace tools; retain private traces, artifacts and assertions.
5. Let the configured generator inspect only training tasks/outcomes and propose code modules within its mode limits.
6. Validate imports, contract, file and line budgets; execute the candidate against the same frozen task bank in fresh workspaces.
7. Reject held-out assertion regressions and failures of the measured-success gate; independently blind-review actual trajectories.
8. Feed measured evaluation summaries into the next bounded candidate attempt and retain the strongest passing candidate.
9. Apply the existing mode's approval policy and `5% → 25% → 100%` Canary with pinned existing sessions.
10. Promote only after the existing Canary gates or roll back on live regressions.

The explicit contract-only backend (`task_benchmark.enabled=false`) retains the earlier randomized hook-contract/source-review evaluation for compatibility. Its result is not represented as a completed long-task benchmark.

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

Standalone startup checks `EVOLUTION_MODEL_CAPABILITY_VERSION`. An older package is backed up under `.package-backups/` before replacing code files. Existing runtime configuration, registry records, signing keys, artifacts, and version history stay in place. Rebuild the main embedded package with `python tools/sync_liquid_kernel_bundle.py`; pass other entrypoint names explicitly when intended. Historical snapshots are preserved by default.

Verification commands are recorded in `docs/evolution_verification.md`. Live acceptance is opt-in through `tools/verify_evolution_real.py`; the verifier requires explicitly selected redacted human session records, runs real tasks through the Admin API, and records real remote model calls. It never substitutes a fabricated candidate or source-review-only judge run for task execution.


## Session-driven architecture evolution (capability 4)

Every non-Off run now executes session-derived tasks. Saved `task_benchmark.enabled=false` is migrated to true; the retired opt-out checkbox is removed. The configured history dates, user/session scopes and version-depth filters remain authoritative. A frozen curriculum is synthesized from human turns in at least two distinct sessions. Starter files are synthetic, self-contained fixtures; historical assistant answers are not seed solutions. Later human corrections are scheduled as additional user turns. This is executable task synthesis, not a claim that historical production sessions have been reproduced exactly.

Each task runs a real bounded model/tool conversation in a fresh temporary workspace. Tools read, write, edit, list files and run commands. Commands require macOS sandbox-exec or Linux bubblewrap, with network denied and no fallback to host execution. Candidate hooks run in a separate process with a per-hook timeout. Worker model references and task definitions are identical across arms. Artifacts, tool results, follow-ups, errors and acceptance assertions are recorded; text claiming success is not acceptance evidence.

Tasks are frozen before proposing code and split by source session. The designer receives training tasks and baseline training trajectories; held-out contents are excluded. Assertions and the scoring implementation are outside all mutable kernel artifacts. Scores use 70% artifact assertions (with a bounded penalty for observed failed actions), 20% independent blind trajectory review and 10% paired workflow efficiency. Every previously passing held-out assertion remains a gate. Promotion additionally requires measured task improvement, nondecreasing full-task success rate, and the mode's minimum mixed-score gain. The public configuration cannot opt out into contract-only/source-review evaluation. That retained internal path is used only by legacy regression fixtures. Insufficient history yields no_change with evaluated=false.

Candidate evaluation feeds the next bounded candidate attempt. A candidate can modify real Python modules, not just prompts: Tuning permits kernel/tool/prompt/context/recovery modules; Thinking additionally permits planning, memory, routing, verification, scheduling, state and serialization; Aggressive permits harness.py and new core_<name>.py modules. before_round can select/reorder tools, retain recent complete tool exchanges while preserving all human/system constraints, and lower the output-token limit. Those policies are interpreted by the same helper in live Agent model calls and in the task runner. Authentication, persistence, evaluation, promotion, audit, signing and sandbox controls remain immutable. This is architecture/code optimization, not neural weight training.

Mode ceilings: Tuning 5 files/400 changed lines/2 tasks; Thinking 12 files/1200 lines/4 tasks; Aggressive 30 files/4000 lines/8 tasks. Every task uses the Admin user Agent max_rounds, max_run_seconds and max_output_tokens values (default 200 rounds / 3000 seconds / 16384 output tokens), independent of evolution strength. Tool-call capacity follows that round limit. The round field is read-only; changing Admin settings takes effect on subsequent runs. Other saved budgets remain bounded by the selected mode. Task calls, source generation and blind review share a run token budget. Provider usage is used where available, with a conservative character estimate otherwise. Cancellation, task/command/hook timeouts and the run deadline are enforced.

The main Clouds_Coder.py embeds this entire package, including agentic.py. Startup diagnoses the package capability and required files. It backs up and atomically replaces only framework files when older or incomplete, rolls back a failed partial upgrade, and preserves a compatible newer framework. Registry data, signing keys, active/canary versions, artifact signatures, user configuration and rollback history are never part of that write set. Contract-1 artifacts keep their original sources and default missing policy fields to identity behavior. An inherited startup inject policy now preserves an evolved kernel; only an explicit force reset may replace it.

Protected run artifacts: experience/<run_id>/task_bank.json, incumbent_rollouts.json, candidate_<n>_rollouts.json, plus existing run/event/version records. The admin form exposes task count and the inherited Admin round limit; existing mode, date/scope, model and scheduling controls still apply. No evolution run is started merely by installing the updated main file.


Capability 4 live-service repairs: Structured generation uses native JSON mode, respects configured reasoning defaults, continues intermediate thinking rounds, and applies bounded format/semantic recovery with explicit truncation diagnostics. Task workers advertise complete native function schemas, send properly paired assistant/tool histories with stable call IDs, and accept actual function-call responses; task design and blind scoring remain JSON objects. Task definitions normalize observed field aliases, verify artifact filename/format consistency, and undergo independent acceptance review before freezing. Line-count requirements are executable assertions. Human bubble logs recover initial requests hidden by compact/file-buffer placeholders; a lone continuation message is insufficient evidence.

Session continuation persists the previous completed-task context and selected fresh evidence in a bounded capsule. Previously observed file excerpts are visible in the next request; small complete source bodies may fulfill repeat reads from cache after fingerprint validation. Changed files invalidate their evidence, and fresh=true bypasses reuse. Todo parsing unwraps only declared Todo argument containers; transport metadata and arbitrary quoted strings cannot become tasks. Known polluted rows are cleaned on load while task prose mentioning tool names is retained.

All configured models can be checked with `tools/verify_model_compatibility_real.py --config <config.json> --report <report.json>`. It enumerates every explicitly configured profile/model combination and runs real JSON, multi-turn native-tool execution, Python artifact assertions, and blind scoring against an explicitly declared public compatibility task. Optional profile filtering supports failure diagnosis. These checks complement, rather than replace, the session-derived long-task verifier. Qualitative judge confidence labels are retained separately from optional numeric confidence; score validation remains strict.


Long-file handling is shared with ordinary user chat: successful write bodies are archived only in the transported view, with paths, hashes and incomplete-preview labels. The actual workspace and saved transcript are unchanged. Matching is local to each assistant/tool exchange, so a reused call ID cannot turn an earlier failed write into a success. Input estimates count this same transported view. Ordinary single/role loops retain malformed-argument original sizes and decline oversized incomplete file writes instead of repairing a truncated prefix into a committed document; retries receive compact-script/chunk guidance.

Task-driven evaluation freezes equal per-task token allocations for incumbent and all candidate arms, leaving 35% of the post-design budget for proposals and scoring. Task budget exhaustion is an observed failed rollout, not a fabricated score or an immediate loss of the entire evolution search. Run-wide limits still apply. Protected full rollout artifacts retain original data; designer/judge views bound repeated long strings and label excerpts with hashes. Source constraints, actual file assertions and held-out gates stay intact.

## Shared full-history context and accounting (capability 5)

`context.py` supplies append-only, digest-addressed full-history archives, complete native call/result groups, context thresholds and nested token accounting. Ordinary IDE/WebUI sessions archive single-agent, role and manager histories before lossy compression, completed-task resets and persistence. `context_recall` searches exact tool arguments and observations by query/path/call ID, with immutable archive IDs, field and line windows. Old overwritten or deleted files remain historical evidence; source fingerprints distinguish current files. Long archived code exposes symbol line hints and a next-window position so clients can retrieve missing middles without repeatedly reading the header. Previously discarded text from older program versions cannot be reconstructed unless it remains in a saved transcript or other existing artifact.

The task runner archives before candidate filtering and bounds the candidate hook input as well as the transported model view. Independent review begins in a fresh context, receives blinded frozen artifacts, and exposes only read-only recall. Large proposal/review packets are archived before excerpting. Review finals require a valid JSON object; format failures receive bounded format and isolated semantic recovery with native JSON mode and no task tools. A failed or ambiguous answer is never interpreted as a score.

Ordinary plan-step quality review uses the same frozen-artifact reader and fresh, read-only context. A host-side minimum inspection gate rejects a final verdict while long artifacts still have no observed omitted-body window. Artifact indexes expose immutable IDs and symbol lines. This prevents a header-only excerpt from being treated as proof that implementation is absent; it does not guarantee that one inspected window proves the entire file correct. Review limits, calls and retries remain inside the ordinary or evolution token ledger.

Admin ordinary-session `max_run_tokens` and `max_task_tokens` default to zero (unlimited) and count input, schemas, output, auxiliary calls, review and retries. Parallel reservations prevent concurrent quota overspending, and settled totals persist. Evolution exposes optional total and per-task token quotas, inherits Admin round/context/output/time limits, and allows explicit compute budgets independently of code-edit strength. Zero or an unset quota is unlimited. No task, proposal or review allowance is synthesized from the total quota; ordinary-session token settings do not silently cap evolution tasks. Limits are ceilings; a task can finish or exhaust its token allowance before the round limit. The historical verifier reports pipeline acceptance separately from baseline task acceptance and measured improvement.

Stable system instructions precede live time and volatile runtime state. Unchanged local sources reuse one bounded in-memory source cache, with size/mtime/ctime/inode checks, content fingerprints and `fresh=true` bypass. Provider-reported cached input tokens are preserved in telemetry and session budgets; absent metrics stay unknown. Cached tokens still consume logical token quotas. Hit rates depend on the model service, prefix, workload and cache lifetime and are not memory-retention guarantees.

Ollama receives the actual configured `num_ctx`, explicit `think:false` when reasoning is off, native JSON format when required, and strict output allowances under quotas. Native streaming preserves whitespace and split inline thinking tags; valid empty-object tool arguments remain valid for zero-argument tools. These transport repairs apply to ordinary user sessions and evolution together. `tools/verify_context_runtime_real.py` tests ordinary encrypted-session continuation, overwritten/deleted historical file recovery, real artifact calculations and independent long-file review using configured cloud or local model profiles.


## Live progress and Admin localization (capability 6)

Evolution reports per-source task design, audit and repair attempts before the task bank freezes. Each execution reports its arm (baseline or numbered candidate), task index/total, current round/Admin limit, tool calls and artifact-check stage. Real model requests expose wait duration, HTTP retry/backoff and a five-second worker heartbeat. A heartbeat means the worker is alive; it does not mean the model or task made progress.

The protected registry adds a run_progress metadata table. Frequent round/tool/wait updates replace a bounded snapshot and retain only the latest 40 activity bubbles, avoiding a full audit event for each heartbeat or tool tick. Coarse milestones retain their hash-chained audit events. Run detail returns the latest 200 events with total/truncation metadata; the existing cursor event API remains available for complete audit retrieval. Counters use actual events, not an estimated overall completion percentage. A token quota may stop execution before the round ceiling. An all-proposal quota failure is explicitly explained as no candidate evaluation, even if the historical run status says no_change.

Admin progress cards and detail bubbles refresh automatically. Task totals, round counts, tool state, model waits/retries, quotas, cache labels, policy hints and configuration fields support Simplified Chinese, Traditional Chinese, English and Japanese. Translated mode/schedule option labels keep explicit immutable protocol values. Dynamic rendered text avoids repeated substring translation of already translated content.

Old runs without detailed telemetry display unavailable values explicitly and may report archive write times; an archive write is not proof of a live worker. tools/inspect_evolution_progress.py reads existing registries in SQLite read-only mode without constructing a control plane, recovering runs, creating schemas, or modifying active kernels. Updating code does not hot-replace a running Python process; restart the program and refresh Admin to use the new UI and telemetry on subsequent runs.

Structured responses additionally normalize complete Python-style literals, trailing commas and closed reasoning wrappers locally; unfinished reasoning, partial nested objects and non-standard values remain invalid. A failed format retry can enter an isolated semantic JSON converter with no tools. The converter sees the requested schema and damaged output as data, maps existing facts/aliases, and must decline missing/truncated evidence. It cannot invent numerical values or rewrite source payloads. The same converter supports ordinary tool-argument recovery and independent review. Oversized incomplete file writes remain unexecuted. All recovery attempts retain cancellation, phase/task/run token quotas, deadlines, full archives and diagnostics; persistent failure remains an explicit failure rather than a successful score. `tools/verify_json_semantic_real.py` exercises configured models on public malformed outputs and explicitly labels injected protocol faults separately from real semantic requests.

Optional offline JS downloads now run in a daemon after services bind, so a 60-second download wait cannot consume the restart supervisor's readiness window. The supervisor allows 180 seconds for required startup, bypasses system proxies for its direct health probe, verifies the exact child PID and restart nonce, and retains a protected `restart_startup.log`. Verified health probes skip potentially blocked optional SQLite diagnostics. Failed required startup still rolls back and records the last probe error. `tools/verify_admin_restart_real.py` starts only an isolated temporary service and tests actual readiness while its optional downloader is deliberately delayed for 70 seconds.


## Shared reasoning compatibility and measured workflow comparison (capability 7)

Auto preserves each provider's configured reasoning behavior. Explicit off uses the native switch for known hybrid DeepSeek/GLM transports; rejection of an optional field removes that field alone. The compatible fallback preserves an output-token ceiling, including when switching max_tokens to max_completion_tokens. Ordinary Web/IDE conversations and evolution use the same client, exact native reasoning history, stream finish reasons and total request deadline. Socket reads, retry requests and backoff share that deadline. SSE byte trickles cannot extend it indefinitely. Display excerpts remain bounded; protocol reasoning is retained for subsequent tool exchanges and full archival.

Thinking-only replies are intermediate rounds. They do not trigger JSON format repair or force a file write. Task, recall and review loops retain the reasoning and continue within Admin rounds, context, token quotas, cancellation and time limits. A structured final result is validated only when submitted. Adaptive continuation output allowances remain within the configured per-turn ceiling. Format/semantic recovery is bounded and reported separately; the error message never claims semantic repair ran when it did not.

The default task-driven evaluator freezes session-derived multi-turn tasks, separates training and holdout sources, and runs incumbent/candidate policies in fresh workspaces with the same worker configuration. Scores combine actual artifact checks (70%), independent blind evidence review (20%) and paired workflow efficiency (10%). Efficiency measures logical tokens, rounds and failed tool calls on successfully completed paired tasks; elapsed latency is reported, not rewarded. Lost passing assertions or task quality regressions block eligibility. A changed effective flow and measured quality/holdout efficiency gain are required; subjective review alone cannot qualify a candidate.

A provisionally qualifying candidate must independently repeat both full arms in fresh workspaces under the same frozen acceptance checks. Non-reproduced gains block candidate registration. Independent replays use the same explicit quota rules as initial runs. A positive user quota can stop tasks earlier than Admin's round ceiling and is reported as a quota failure; zero never creates an implicit fair-share limit. Full flow comparisons and confirmation evidence are retained under the protected run archive and summarized in Admin. This is executable agent-policy optimization; it does not update remote model weights.

Model directories retain explicit config provenance. Configured models are displayed before discovered models from configured APIs in Evolution, Web and IDE. Updating this framework never replaces autonomously evolved kernel artifacts. Contract version remains 1; startup upgrades framework capability/content with backup while preserving compatible newer frameworks and protected state.


## Optional quotas, paired scores and deployment policy (capability 8)

Total evolution tokens, per-task tokens and changed-line limits default to zero (unlimited). Only positive explicitly configured limits apply. Mode changes preserve these choices. Task-only limits work with an unlimited total, and unlimited ledgers still record actual input/output/retry/review usage. Context capacity, per-turn output limits, Admin conversation rounds, tool limits and timeouts remain active. Old preset-only changed-line caps migrate to unlimited in memory; stored run snapshots remain unchanged. Existing positive total quotas are retained until an administrator changes them.

Each run freezes a task bank, executes the current baseline and persists its artifact score before any review or proposal. A fresh blind review supplies the baseline's review and mixed scores even if no valid patch follows. Every valid proposed patch executes the same tasks in clean workspaces, then receives a blinded paired review. The score table shows each candidate beside its paired baseline, including rejected and regressed candidates. Artifact scores survive review failures; missing reviews and incomplete execution stay explicitly unscored or partial. Code validation failures first return their exact diagnostics to the generator for at most two repairs, under the same run quota/deadline. Repaired proposals must pass the unchanged validator before task execution. Persistent code validation rejection has a validity-failure total of zero, with task/review components marked unscored. No-change proposals reuse the identical measured baseline scores. Historical runs can recover saved baseline artifact scores without exposing private rollout files; absent historical review evidence cannot be reconstructed.

Primary eligibility requires completed comparable workflows, no lost passing assertions, no task-quality regression, a measured flow change and positive measured gain. Before deployment both arms repeat independently in fresh workspaces and receive another independent blind review. The repeated candidate must satisfy the same gates and exceed the repeated baseline, including the mode's minimum gain. Equal scores never qualify. Automatic deployment starts Canary only for such candidates. User approval and historical rollback remain available. If the active baseline changes during the run or before manual approval, a new comparison is required. In-flight evaluations keep their frozen model/runtime configuration.

Admin controls, unlimited-quota telemetry, score components, incomplete states, repeat comparisons and deployment choices support Simplified Chinese, Traditional Chinese, Japanese and English. No candidate from release verification is deployed to the user's production registry.

macOS workspace command sandboxes share a narrow parent-metadata traversal rule. This permits `mkdir -p nested/deeper && cd nested/deeper` in ordinary IDE/WebUI tasks and evolution rollouts; it grants metadata only on known ancestor paths and does not grant outside file contents, sibling reads/writes, or parent directory listings. The previous policy incorrectly reported valid workspace subdirectories as not-a-directory.

Repeated premature review finals receive a host-retrieved exact window from the frozen artifact after one reminder. The shared ordinary/evolution reader archives this read-only delivery, provides it to the independent model context, and requires a new verdict. It does not accept or manufacture the previous score. This avoids repeating the same missing-body reminder for hundreds of calls while keeping evidence and quota accounting intact.

## Protected execution defaults and generalization (capability 9)

Candidate kernels cannot override the host's per-call output allowance. Ordinary tasks and evolution use the Admin/runtime allowance, reduced only by the actual remaining quota. The hook context exposes these limits, and omitted policy fields inherit defaults. The original host context_recall descriptor survives policy and tool filtering. Selecting older history retains a bounded progress handoff with exact call identities and archived-evidence retrieval instructions, after the stable user/system prefix. This prevents silent loss of completed work and preserves prefix caching.

Before task execution, candidates are probed in a neutral unrelated task context. New unconditional training-specific schema identifiers in their prompt/policy output cause a repairable task_specific_policy rejection. The probe consults training goals only, never holdout contents. Conditional domain guidance remains possible. This catches a class of schema leakage; it is not a proof of generalization. Generator contracts require mechanism-level hypotheses, current-task schema semantics, preserved working behavior and portable environment recovery. Field names alone never determine types or counter scope.

The real verifier can reuse a fingerprint-checked frozen task bank for a controlled rerun. Both the baseline and newly generated candidate still execute from fresh workspaces with real models and tools, followed by independent review and unchanged deployment gates. Reusing a bank skips only task design, and is explicitly labelled in reports.


## Evaluator validity and transport diagnostics (capability 10)

Command checks are parsed before task-bank freeze. Typed or unambiguous bare Python is wrapped with an explicit interpreter while retaining the exact assertion source and its hash. Legacy banks receive a new fingerprint and evaluator lineage; existing archives are never rewritten. Shell syntax is checked without executing assertions. Invalid evaluator definitions or unavailable isolation are infrastructure failures, not zero agent scores. Historical banks containing unwrapped Python show invalid assessment warnings and cannot authorize manual deployment. Ordinary Bash uses the same detector to return a corrective interpreter hint before executing any source.

Evolution model calls inherit the selected model profile's request timeout, bounded by the remaining task/run deadline, instead of imposing a separate 180-second cap. `OllamaError` remains a backward-compatible internal class for all providers. Public diagnostics distinguish client deadlines, connection timeouts, authentication, rate limits and actual server HTTP status; only the hostname is exposed. These labels support Simplified Chinese, Traditional Chinese, Japanese and English.


## Cross-platform runtime and bootstrap (capability 11)

Admin authentication starts independently of optional form bindings and language loading. Evolution controls are checked against the actual markup, and JSON configuration cloning does not depend on structuredClone. Local authentication connection waits are bounded and retryable.

Without sandbox-exec/bubblewrap, or when the host rejects their startup, agent tools use portable_workspace. This backend interprets a bounded Python AST and simple file commands through explicit capabilities; it never passes user source to eval/exec or an unrestricted host process. It supports json/pathlib/math/csv, simple workspace Python modules, file operations and actual assertions. Unsupported operations return recoverable hints to use file tools or supported Python. It is a limited interpreter, not a general Python environment: network, arbitrary processes, third-party imports, private reflection, symlinks/hardlinks, traversal and protected metadata mutation are unavailable. Assertion/backend limitations are recorded as invalid evaluation definitions rather than zero capability scores. No assertion is bypassed or replaced with success. Native isolation remains preferred. Ordinary remote/hard-mode Bash uses the same confined backend if its process sandbox is unavailable.

UTF-8 is explicit on benchmark/worker pipes and persistence boundaries. Legal surrogate pairs become their Unicode scalar; unpaired code points are preserved with valid JSON escapes in exact archives and visible escapes in file/display text. Normal Unicode archives and model fingerprints retain their original byte contract. Legacy surrogate-pair archives are checked against their original digest without rewriting them.

Default evolution-wide mode time caps have been removed (timeout_seconds=0). Old preset-only caps migrate in memory; explicit custom limits remain enforced. Task duration inherits normal Admin runtime settings and is checked between rounds, while in-flight requests use the normal selected profile timeout. Only an explicit whole-run deadline may preempt a request. Retries and format recovery have no separate hidden 180-second cap.

Transient transport failures use the same outer recovery count as ordinary chat (`MODEL_OUTPUT_RETRY_TIMES`), with a fresh normal profile timeout for each attempt. Authentication, cancellation, emitted partial streams and explicit quota/deadline failures are not blindly retried. Estimated usage for failed requests is accounted conservatively and labeled separately from successful provider usage.

## Isolated encoding and effective flow evidence (capability 12)

Isolated Python processes use -X utf8 in addition to binary protocol streams. Their input is decoded explicitly as UTF-8; policy output is ASCII JSON. PYTHONIOENCODING alone is insufficient under -I, especially on cp936/GBK Windows. Frozen task-bank reads and standalone bundle synchronization also use explicit UTF-8. Windows and hosts without native isolation retain the bounded portable_workspace interpreter; candidate source is never launched through cmd or unrestricted host Python.

Every shared JSON model request normalizes surrogate pairs and escapes unpaired code points in the data before JSON serialization. Escaping only the serialized JSON would allow a remote JSON decoder to reconstruct invalid scalar values and break its tokenizer. Streamed, ordinary, evolution and binary-response JSON requests use this same boundary. Exact archive encoding and existing archive digests remain unchanged.

Flow signature version 3 includes the selected after_tool_results observations that actually become model messages, along with effective system, tool and history policy. During candidate execution a separate frozen-baseline worker receives identical hook inputs. Eligibility uses differences in the effective outputs of that controlled replay, rather than different file bytes from independent model responses. Comment-only edits, discarded extra observations and overrides of protected output limits do not prove an effective architecture change. Earlier diagnostic flow signatures remain readable; mixed evidence versions cannot authorize a new comparison. Changed effective behavior still requires complete real tasks, no regression, higher measured scores and successful independent paired repetition before registration or Canary.

## Proposal schema and indexed evidence (capability 13)

An explicit proposal reason placed at patch.reason is safely promoted to the top level without modifying code. Unambiguous proposal envelopes are unwrapped. Missing/conflicting decisions require at most two model repairs using the normal token ledger, context, request timeout and cancellation. Persistent schema failures preserve baseline scores and reject the unexecuted candidate; they cannot masquerade as no_change. Both proposal paths share this validator.

Large generator/review packets retain their exact original and addressable field bodies. Inline numerical metrics, user requirements and checks remain intact; long trace/hash telemetry receives indexed samples instead of filling every model round. Shared history retrieval supports exact character pagination for minified JSON and preserves search hits under small windows. Ordinary tasks use the same reader. A task that reaches the round ceiling without a final/finish signal retains its artifact results but is incomplete and cannot qualify a deployment.

Capability 14 recovers truncated native tool arguments in the original task loop instead of aborting the evolution run. Incomplete writes and shell commands are never executed; small complete malformed arguments may use isolated, source-preserving semantic repair. Ordinary task guards also cover oversized shell arguments. Each completed task checkpoints its actual artifact score; missing independent review remains unscored. Cancellation, authentication, network and explicit budget failures still propagate.

Capability 15 removes independent 32,000-token ceilings from runtime normalization and model transport, and the separate 16,000-token review ceiling. Admin output settings govern all evolution phases, including reasoning continuations; only explicit request/remaining quotas may lower them. Task-definition audit/repair now permits 30 attempts with matching progress telemetry.

Capability 16 supplies training-only measured cost/quality opportunities to the generator, allows efficiency hypotheses on successful tasks, and gives an initial no_change one bounded opportunity audit. No forced patch or promotion is introduced. Holdout isolation, real paired execution, regression gates and independent confirmation remain mandatory. Unchanged baselines are labeled explicitly, and model prose is preserved rather than translated by substring replacement.

## Architecture experiments and retained candidates (capability 17)

Task-driven search constructs a concrete experimental code variant even when the proposer declines a change: one bounded training-only opportunity audit precedes an explicitly unproven inherited adaptive context-policy experiment. Every variant runs real tasks and independent review; no baseline copy is scored as a candidate. Validated code is registered before rollout, with persistent per-version evidence, partial scores and final rejection/confirmation status. Retention does not grant deployment eligibility. Canary/promotion requires passing paired outcomes and independent confirmation; rollback accepts only previously active versions. Text assertions freeze explicit UTF-8 reads and equivalent single Python heredocs with lineage. Runtime hints describe the active protected interpreter; unsupported shell claims and representation-specific static SVG checks are rejected before task execution.

Capability 18: task-design minimum_tool_calls is a complexity estimate, never a lower bound on efficient execution. Scores require real tool work and delivery of followups, with immutable artifact checks and completed-workflow deployment gates. Scoring protocol 2 prevents comparison with the earlier tool-count floor; affected historical rows are flagged without rewriting their scores.

Capability 19: preflight checks audit portable imports and module members before task freeze. The restricted VM exposes bounded regex operations through fixed isolated workers (no model Python executes in those workers), Pattern/Match operations and chr/ord. Unsupported capabilities enter definition repair, with matching declarations provided to designers and reviewers. Worker regex timeouts prevent catastrophic backtracking from hanging the host.
