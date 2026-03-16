# CHANGELOG 2026-03-17

Trilingual merged release notes: English / 中文 / 日本語.

## English

### Priority-Ordered Updates

1. Single-mode agent leak fix (critical)
- Fixed `_manager_apply_task_policy()`: when `executor_mode_flag=True`, the target-not-in-participants branch (`L16241-16248`) could append extra agents, overriding the Single-mode `participants = [assigned_expert]` constraint set at `L16226-16227`.
- Added a hard post-guard: after all participant/target resolution, if `mode == EXECUTION_MODE_SINGLE`, force `participants = [assigned_expert]` and redirect any non-expert target back to the assigned expert.
- Effect: Single-mode tasks are now guaranteed to use exactly one agent regardless of executor_mode_flag or LLM routing decisions.

2. Conclusive-reply termination signal fix (critical)
- Root cause: when an agent (e.g. developer) replied with a conclusive answer like "task complete", the Manager ignored it because (a) the conclusive-reply check in `_manager_fallback_route()` only ran on the fallback path, not the tool-parsed routing path; (b) `_manager_apply_task_policy()` had no conclusive-reply detection; (c) blackboard `approval.approved` was never set by text-based completion signals.
- Fix 1 — Policy-layer interception: added conclusive-reply detection in `_manager_apply_task_policy()` before the `can_finish_from_approval` gate. When any agent's latest text is conclusive, no open todo items remain, and no error log exists, the target is forced to `finish`.
- Fix 2 — Sync-loop interception: added post-turn conclusive-reply detection in `_multi_agent_sync_blackboard_worker()`. After each agent turn completes, if the agent gave a conclusive reply with no open tasks and no errors, the loop breaks immediately with auto-approval.
- Fix 3 — General endpoint detection in fallback: extended `_detect_endpoint_intent` from `simple_qa`-only to all task types in `_manager_fallback_route()`, so developer conclusive replies in research/engineering/general tasks also trigger fallback finish.
- Effect: four-layer defense (fallback → general-endpoint → policy → sync-loop) ensures conclusive replies are never ignored.

### 2026-03-16 Bug Fix Summary
- Eliminated Single-mode multi-agent leak caused by executor_mode_flag overriding participant constraints.
- Eliminated infinite delegation loops where Manager kept dispatching agents after a conclusive reply, by adding termination detection at four independent checkpoints.
- Both fixes include safety guards: conclusive-reply finish is suppressed when error logs exist or open todo items remain.

---

## 中文

### 按优先级排序的更新内容

1. Single 模式 Agent 泄漏修复（严重）
- 修复 `_manager_apply_task_policy()`：当 `executor_mode_flag=True` 时，target 不在 participants 的分支（`L16241-16248`）会 append 额外 Agent，覆盖了 `L16226-16227` 设置的 `participants = [assigned_expert]` 约束。
- 新增硬约束后置守卫：在所有 participant/target 解析完成后，若 `mode == EXECUTION_MODE_SINGLE`，强制重置 `participants = [assigned_expert]`，并将非 expert 的 target 重定向回 assigned_expert。
- 效果：Single 模式任务无论 executor_mode_flag 或 LLM 路由决策如何，都保证只使用一个 Agent。

2. 结论性回复终止信号修复（严重）
- 根因：当 Agent（如 developer）回复"任务完成"等结论性文本时，Manager 忽略该信号，原因是：(a) `_manager_fallback_route()` 中的结论检测仅在 fallback 路径触发，LLM 工具路由路径完全绕过；(b) `_manager_apply_task_policy()` 没有任何结论检测逻辑；(c) 文本形式的完成信号不会设置 blackboard `approval.approved`。
- 修复 1 — Policy 层拦截：在 `_manager_apply_task_policy()` 的 `can_finish_from_approval` 检查之前，新增结论性回复检测。当任意 Agent 最新文本为结论性回复、无待办事项、无错误日志时，强制 target 为 `finish`。
- 修复 2 — Sync 循环拦截：在 `_multi_agent_sync_blackboard_worker()` 每个 Agent turn 完成后，新增结论性回复检测。满足条件时立即 break 并自动 approve。
- 修复 3 — Fallback 通用 endpoint 检测：将 `_detect_endpoint_intent` 从仅限 `simple_qa` 扩展到所有任务类型，使 research/engineering/general 类型的 developer 结论性回复也能触发 fallback finish。
- 效果：四层防御（fallback → 通用 endpoint → policy → sync 循环）确保结论性回复不会被忽略。

### 2026-03-16 修复总结
- 消除了 executor_mode_flag 覆盖 participant 约束导致的 Single 模式多 Agent 泄漏。
- 消除了 Agent 给出结论性回复后 Manager 仍反复委派的死循环，通过在四个独立检查点添加终止检测。
- 两项修复均包含安全守卫：存在错误日志或待办事项时，结论检测不会触发 finish（避免误杀）。

---

## 日本語

### 優先度順の更新内容

1. Single モード Agent リーク修正（重大）
- `_manager_apply_task_policy()` ��修正：`executor_mode_flag=True` の場合、target が participants に含まれない分岐（`L16241-16248`）が追加 Agent を append し、`L16226-16227` で設定した `participants = [assigned_expert]` 制約を上書きしていた。
- ハードガードを追加：全 participant/target 解決後、`mode == EXECUTION_MODE_SINGLE` であれば `participants = [assigned_expert]` を強制リセットし、expert 以外の target を assigned_expert にリダイレクト。
- 効果：executor_mode_flag や LLM ルーティング結果に関わらず、Single モードタスクは必ず 1 Agent のみで実行。

2. 結論的応答の終了シグナル修正（重大）
- 根本原因：Agent（例: developer）が「タスク完了」等の結論的応答を返しても Manager が無視していた。理由：(a) `_manager_fallback_route()` の結論検出は fallback パスでのみ実行され、ツール解析ルーティングパスでは完全にバイパス；(b) `_manager_apply_task_policy()` に結論検出ロジックが皆無；(c) テキストベースの完了シグナルでは blackboard `approval.approved` が設定されない。
- 修正 1 — Policy 層インターセプト：`_manager_apply_task_policy()` の `can_finish_from_approval` チェック前に結論的応答検出を追加。Agent の最新テキストが結論的で、未完了タスクなし、エラーログなしの場合、target を `finish` に強制。
- 修正 2 — Sync ループインターセプト：`_multi_agent_sync_blackboard_worker()` で各 Agent ターン完了後に結論的応答検出を追加。条件を満たせば即座に break し自動承認。
- 修正 3 — Fallback 汎用 endpoint 検出：`_detect_endpoint_intent` を `simple_qa` 限定から全タスクタイプに拡張し、research/engineering/general タイプの developer 結論的応答でも fallback finish をトリガー。
- 効果：4 層防御（fallback → 汎用 endpoint → policy → sync ループ）により結論的応答の見落としを排除。

### 2026-03-16 修正サマリー
- executor_mode_flag が participant 制約を上書きすることで発生していた Single モードの複数 Agent リークを解消。
- Agent が結論的応答を返した後も Manager が繰り返し委任する無限ループを、4 つの独立チェックポイントでの終了検出により解消。
- 両修正にはセーフガードを含む：エラーログまたは未完了タスクが存在する場合、結論検出は finish をトリガーしない（誤終了防止）。
