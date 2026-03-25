# CHANGELOG 2026-03-20

## 🔥 Plan Mode 架构 & 内核全面升级

本次更新是自项目启动以来最大规模的架构级改动，涵盖 7 大模块、60+ 个修改点。核心主题：**Plan Mode 统一架构**、**分层上下文压缩**、**通用错误处理**、**Reviewer Debug Mode**。

---

## English

### Headline: Plan Mode & Core Architecture Overhaul

#### 1. Plan Mode — Unified Architecture (Critical)

**UI Toggle**: New `Plan: Auto/On/Off` button in the toolbar. Users can now force plan mode on (even for L1 tasks) or off (skip planning for L5 tasks).

**Single + Sync Support**: Plan mode now works identically in both `single` and `sync` execution modes.
- Single mode: `_single_agent_plan_step_check()` auto-advances plan steps based on tool results and phase detection.
- Sync mode: Manager delegates per-step with `advance_plan_step=true`.
- Both modes share the same plan step tracking, todo sync, and progress display.

**Plan Step Protection (6-layer defense)**:
- `_mark_all_done_silently()` preserves plan_step todos — arbiter can't batch-complete them.
- `_can_auto_finish_from_approval()` blocks finish when plan steps are pending.
- Arbiter snapshot includes plan progress ("Only 2/7 steps completed — do NOT classify as TASK_COMPLETED").
- `_manager_progress_state()` never returns "done" with pending plan steps.
- `_project_todo_hint_for_manager()` warns "DO NOT finish until all N steps completed".
- `_manager_fallback_route()` redirects to developer instead of finishing when plan steps remain.

**Planner Bubble UI**: Orange-red themed (`#e8533f`) chat bubble with full agent badge structure, matching explorer/developer/reviewer styling.

#### 2. Tiered Context Compression + File Buffer (Critical)

**Problem**: `_auto_compact` only compressed `self.messages`, never touching `agent_messages` (800 msgs), `manager_context` (400), or per-role `contexts` (400 each). After compact, agent contexts caused immediate re-wall.

**Solution**: 4-tier progressive compression system:
- Tier 0 (>40% left): Normal operation
- Tier 1 (20-40%): Aggressive microcompact, reduced keep_recent
- Tier 2 (10-20%): Compact agent contexts, file buffer offload
- Tier 3 (<10%): Deep compact everything, 600-char content limit

**File Buffer**: Large content (>2000 chars) offloaded to `file_buffer/` directory, replaced with compact references in context. Auto-pruned at 500 files.

**Range Extension**: `ctx_left` range expanded from [18000, 100000] to [4000, 1,000,000] — supports both tiny and 1M-token contexts.

**State Handoff**: `_build_state_handoff()` ensures goal, progress, active agent, round info, and code artifacts survive compaction losslessly.

#### 3. Universal Error Architecture (High)

**Unified `errors` list** with `category` field replaces compilation-only detection. 6 error categories: `test > lint > compilation > build_package > deploy_infra > runtime`.

- `_detect_error_category()`: Command keyword matching
- `_extract_error_lines()`: Pattern-based error line extraction
- `_process_tool_result_errors()`: Unified tool result processing (replaces inline detection in both multi-agent and single-agent paths)
- `compilation_errors` maintained as backward-compatible view via `_sync_compilation_errors_compat()`

**Reviewer DEBUG METHODOLOGY** generalized: covers runtime tracebacks, test assertions, lint violations — not just compiler errors.

#### 4. Reviewer Debug Mode (High)

**Problem**: When compilation/test errors occurred, system entered infinite loop — Manager routed to Explorer (read-only), Explorer asked Developer, Developer read files but didn't fix.

**Solution**: Reviewer Debug Mode — when errors detected, reviewer gets `write_file`/`edit_file` access:
- `_activate_reviewer_debug_mode()`: Triggered when `_manager_has_error_log()` is true
- Reviewer system prompt switches to debug methodology with full tool access
- Manager capability note dynamically reflects debug mode
- Auto-deactivates when errors resolve or after 6 rounds (falls back to developer)
- Explorer stall detection: 3 consecutive identical delegations → forced switch to developer

#### 5. Complexity Inheritance & Real-time Input Merge (Medium)

**Complexity Inheritance**: When user responds to plan proposals or L5 confirmations, system no longer re-classifies and loses the previous complexity level.
- `_is_plan_choice_response()`: Detects plan choice responses → skips reclassification
- `_user_mentions_complexity()`: Only changes level when user explicitly mentions complexity keywords
- Previous level inherited when user doesn't mention complexity

**Real-time User Input Merge**: Live user inputs during execution now trigger `_merge_user_feedback_with_plan()` — injects plan-aware merge note into manager context so the plan direction can be adjusted mid-flight.

**Restart Intent Fusion**: `_fuse_restart_intent()` merges user/plan/context intents on restart with priority: user > plan > context. Pure continuation phrases ("继续", "continue") inherit plan intent fully.

#### 6. Task Phase Independence (Medium)

**Problem**: Manager was overly procedural — analysis phases used implementation patterns, wasting debug time.

**Solution**: Phase-aware delegation:
- `_plan_step_phase_hint()`: Infers phase (research/design/implement/test/review/deploy) from step content
- `_infer_current_phase_from_blackboard()`: Determines current phase from active plan step or blackboard state
- `TASK_PHASE_ROUTING`: Maps phases to preferred agents (research→explorer, implement→developer, etc.)
- Manager system prompt includes `PHASE INDEPENDENCE` instruction: "Each phase has its own expertise. Do NOT carry over implementation patterns from previous phases."

#### 7. TodoWrite Isolation & Multimodal Support (Medium)

**TodoWrite Isolation**: When plan_step todos exist, worker `TodoWrite` items are tagged with `owner` to prevent overwriting plan steps during `_sync_todos_from_blackboard()`.

**Multimodal Native Support**: `_run_read()` now detects image/audio/video files by extension:
- If model supports the media type → base64 encode and inject as native multimodal input via `_pending_media_inputs`
- `_recent_multimodal_inputs()` merges pending media from read_file with upload media
- If model doesn't support → returns metadata with guidance to use bash tools

---

## 中文

### 标题：Plan Mode 架构 & 内核全面升级

#### 1. Plan Mode — 统一架构（重要）

**UI 开关**：工具栏新增 `Plan: Auto/On/Off` 按钮。用户可强制开启（L1 也走 plan）或关闭（L5 跳过规划）。

**Single + Sync 双模式支持**：Plan mode 在 single 和 sync 执行模式下行为一致。
- Single 模式：`_single_agent_plan_step_check()` 根据工具结果和阶段检测自动推进 plan steps。
- Sync 模式：Manager 通过 `advance_plan_step=true` 逐步委派。
- 两种模式共享相同的 plan step 追踪、todo 同步和进度显示。

**Plan Step 保护（6 层防线）**：
- `_mark_all_done_silently()` 保护 plan_step todos — arbiter 无法批量完成。
- `_can_auto_finish_from_approval()` 在 plan steps 未完成时阻止 finish。
- Arbiter snapshot 注入 plan 进度（"仅完成 2/7 步 — 不要判定为 TASK_COMPLETED"）。
- `_manager_progress_state()` 有 pending plan steps 时永不返回 "done"。
- `_project_todo_hint_for_manager()` 警告 "所有 N 步完成前不要 finish"。
- `_manager_fallback_route()` plan steps 未完成时重定向到 developer 而非 finish。

**Planner 气泡 UI**：橙红色主题（`#e8533f`），完整 agent badge 结构，与 explorer/developer/reviewer 风格统一。

#### 2. 分层上下文压缩 + 文件缓冲（重要）

**问题**：`_auto_compact` 只压缩 `self.messages`，完全不碰 `agent_messages`（800条）、`manager_context`（400条）、per-role `contexts`（各400条）。compact 后 agent 上下文导致立即再次撞墙。

**方案**：4 级渐进压缩：
- Tier 0（>40% 剩余）：正常运行
- Tier 1（20-40%）：激进 microcompact
- Tier 2（10-20%）：压缩 agent 上下文，文件缓冲卸载
- Tier 3（<10%）：深度压缩，600 字符内容限制

**文件缓冲**：大内容（>2000字符）卸载到 `file_buffer/` 目录，上下文中只留引用。

**范围扩展**：ctx_left 范围从 [18000, 100000] 扩展到 [4000, 1,000,000]。

**状态衔接**：`_build_state_handoff()` 确保目标、进度、活跃 agent、代码产物在 compact 后无损传递。

#### 3. 通用错误架构（高）

**统一 `errors` 列表** + `category` 字段，替代仅编译错误检测。6 个错误类别：`test > lint > compilation > build_package > deploy_infra > runtime`。

- `_process_tool_result_errors()`：统一工具结果错误处理
- `compilation_errors` 作为向后兼容视图通过 `_sync_compilation_errors_compat()` 同步
- Reviewer DEBUG METHODOLOGY 泛化：覆盖运行时 traceback、测试断言、lint 违规

#### 4. Reviewer Debug Mode（高）

**问题**：编译/测试错误时系统进入死循环 — Manager 路由到 Explorer（只读）→ Explorer 请求 Developer → Developer 只读不修。

**方案**：Reviewer Debug Mode — 检测到错误时 reviewer 获得写权限：
- 触发条件：`_manager_has_error_log()` 为 true
- Reviewer 系统提示切换为 debug 方法论 + 完整工具访问
- 错误解决后自动退出，或 6 轮后降级到 developer
- Explorer 停滞检测：连续 3 次相同委派 → 强制切换到 developer

#### 5. 复杂度继承 & 实时输入合并（中）

**复杂度继承**：用户回复 plan 方案时不再重新分类丢失复杂度。
- `_is_plan_choice_response()`：检测 plan 选择回复 → 跳过重分类
- `_user_mentions_complexity()`：仅在用户明确提到复杂度关键词时改变 level

**实时用户输入合并**：执行中的 live input 触发 `_merge_user_feedback_with_plan()` — 向 manager 注入 plan-aware 合并提示。

**Restart 意图融合**：`_fuse_restart_intent()` 按 user > plan > context 优先级融合意图。

#### 6. 任务阶段独立性（中）

**问题**：Manager 过度程序化 — 分析阶段使用实现模式，浪费 debug 时间。

**方案**：阶段感知委派：
- `_plan_step_phase_hint()`：从步骤内容推断阶段（research/design/implement/test/review/deploy）
- `TASK_PHASE_ROUTING`：阶段到 agent 的映射
- Manager 系统提示包含 `PHASE INDEPENDENCE` 指令

#### 7. TodoWrite 隔离 & 多模态支持（中）

**TodoWrite 隔离**：plan_step 存在时，worker TodoWrite 的 items 自动标记 owner，不覆盖 plan steps。

**多模态原生支持**：`_run_read()` 检测图片/音频/视频文件，模型支持时 base64 编码并作为原生多模态输入注入。

---

## 日本語

### タイトル：Plan Mode アーキテクチャ & コア全面アップグレード

#### 1. Plan Mode — 統一アーキテクチャ（重大）

**UI トグル**：ツール���ーに `Plan: Auto/On/Off` ボタンを追加。ユーザーが Plan Mode を強制 ON/OFF 可能。

**Single + Sync 両モード対応**：Plan Mode が single/sync 両実行モードで同一動作。
- Single モード：`_single_agent_plan_step_check()` がツール結果とフェーズ検出に基づき plan step を自動推進。
- Sync モード：Manager が `advance_plan_step=true` でステップごとに委任。

**Plan Step 保護（6 層防御）**：
- `_mark_all_done_silently()` が plan_step todos を保護 — arbiter による一括完了を防止。
- `_can_auto_finish_from_approval()` が未完了 plan steps 存在時に finish をブロック。
- Arbiter snapshot に plan 進捗を注入。
- `_manager_progress_state()` が未完了 plan steps 存在時に "done" を返さない。
- `_manager_fallback_route()` が plan steps 未完了時に developer へリダイレクト。

**Planner バブル UI**：オレンジレッドテーマ（`#e8533f`）、完全な agent badge 構造。

#### 2. 階層型コンテキスト圧縮 + ファイルバッファ（重大）

4 段階の漸進的圧縮システム（Tier 0-3）。`agent_messages`/`manager_context`/`contexts` を compact 時に同期圧縮。ctx_left 範囲を [4000, 1,000,000] に拡張。ファイルバッファで大容量コンテンツをディスクにオフロード。

#### 3. 汎用エラーアーキテクチャ（高）

統一 `errors` リスト + `category` フィールド。6 カテゴリ：test/lint/compilation/build_package/deploy_infra/runtime。`_process_tool_result_errors()` で統一処理。

#### 4. Reviewer Debug Mode（高）

エラー検出時に reviewer が `write_file`/`edit_file` アクセスを取得。独立した冷静なバグ修正プロセス。エラー解決後に自動無効化、または 6 ラウンド後に developer にフォールバック。Explorer スタル検出：3 回連続同一委任で強制切替。

#### 5. 複雑度継承 & リアルタイム入力マージ（中）

Plan 提案への返答時に再分類をスキップし複雑度を継承。実行中のユーザー入力を plan 方向と統合。リスタート時の意図融��（user > plan > context 優先度）。

#### 6. タスクフェーズ独立性（中）

フェーズ認識委任：research/design/implement/test/review/deploy。各フェーズが独自の専門性を持ち、前フェーズの実装パターンを引き継がない。

#### 7. TodoWrite 分離 & マルチモーダルサポート（中）

plan_step 存在時に worker TodoWrite を分離。`_run_read()` が画像/音声/動画ファイルを検出し、モデルがサポートする場合はネイティブマルチモーダル入力として注入。

### 2026-03-20 修正サマリー
- Plan Mode を統一アーキテクチャに昇格：UI トグル、Single/Sync 両対応、6 層 plan step 保護
- 4 段階コンテキスト圧縮 + ファイルバッファで compact 後の再壁衝突を解消
- 6 カテゴリ統一エラー検出で compilation 以外のエラーも自動追跡
- Reviewer Debug Mode で「Explorer 読むだけ→Developer 直さない」無限ループを解消
- 複雑度継承・リアルタイム入力マージ・リスタート意図融合で対話の連続性を確保
- フェーズ認識委任で Manager の過度なプログラム化を防止
- マルチモーダルネイティブサポートで画像/音声/動画ファイルの直接分析が可能に
