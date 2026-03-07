# CHANGELOG 2026-03-07

Trilingual merged release notes: English / 中文 / 日本語.

## English

### Priority-Ordered Updates

1. Core architecture and multi-agent system (highest priority)
- Introduced execution mode constants: `EXECUTION_MODE_SINGLE`, `EXECUTION_MODE_SEQUENTIAL`, `EXECUTION_MODE_SYNC`.
- Added role enums: `AGENT_ROLES = ("explorer", "developer", "reviewer")`, and `AGENT_BUBBLE_ROLES` (including `manager`).
- Added task-level strategy matrix: `TASK_LEVEL_POLICIES` (`L1` to `L5`).
- Added blackboard statuses: `BLACKBOARD_STATUSES` = `INITIALIZING`, `RESEARCHING`, `CODING`, `TESTING`, `REVIEWING`, `COMPLETED`, `PAUSED`.

2. Circuit breaker and anti-drift hardening
- Added `CircuitBreakerTriggered` for hard execution cut-off.
- Added hard thresholds: `HARD_BREAK_TOOL_ERROR_THRESHOLD = 3`, `HARD_BREAK_RECOVERY_ROUND_THRESHOLD = 3`, `FUSED_FAULT_BREAK_THRESHOLD = 3`.

3. Thinking output recovery for deep reasoning models
- Added `EmptyActionError` to catch thought-only turns without executable actions.
- Added wake-up guardrail: `EMPTY_ACTION_WAKEUP_RETRY_LIMIT = 2` with `<thinking-empty-recovery>` runtime prefix.
- Enhanced `split_thinking_content` with lenient `<think>` parsing and unclosed-tag fallback.

4. Memory-bounded diff rendering and hotspot preservation
- Added `_compress_rows_keep_hotspot` to preserve modified regions while compressing untouched context.
- Added dynamic `buffer_cap` in `make_numbered_diff` and `build_code_preview_rows`.

5. Todo ownership and arbiter governance
- Todo entries now support `owner` and `key`.
- Added bulk controls: `complete_active()`, `complete_all_open()`, `clear_all()`.
- Added arbiter guardrail: `ARBITER_VALID_PLANNING_STREAK_LIMIT = 4`.

6. Runtime dependencies and miscellaneous control-plane updates
- Added imports: `deque`, `selectors`, `signal`, `shlex`.
- Extended `RUNTIME_CONTROL_HINT_PREFIXES` with `<arbiter-continue>` and `<fault-prefill>`.

### 2026-03-07 Architecture Innovations
- Monolithic same-frequency multi-agent collaboration via a shared blackboard.
- Industrial circuit-breaker safety model for bounded convergence.
- OOM-safe hotspot rendering for giant diff workloads.
- Adaptive thinking wake-up for empty-action recovery.

---

## 中文

### 按优先级排序的更新内容

1. 核心架构与多智能体系统（最高优先级）
- 新增执行模式常量：`EXECUTION_MODE_SINGLE`、`EXECUTION_MODE_SEQUENTIAL`、`EXECUTION_MODE_SYNC`。
- 新增角色定义：`AGENT_ROLES = ("explorer", "developer", "reviewer")`，以及包含 `manager` 的 `AGENT_BUBBLE_ROLES`。
- 新增任务分级策略矩阵：`TASK_LEVEL_POLICIES`（`L1` 到 `L5`）。
- 新增黑板状态：`BLACKBOARD_STATUSES` = `INITIALIZING`、`RESEARCHING`、`CODING`、`TESTING`、`REVIEWING`、`COMPLETED`、`PAUSED`。

2. 断路器与防漂移硬化
- 新增 `CircuitBreakerTriggered` 异常用于硬性熔断。
- 新增硬阈值：`HARD_BREAK_TOOL_ERROR_THRESHOLD = 3`、`HARD_BREAK_RECOVERY_ROUND_THRESHOLD = 3`、`FUSED_FAULT_BREAK_THRESHOLD = 3`。

3. 深度推理模型的思考输出恢复
- 新增 `EmptyActionError`，捕捉“只思考不执行”的空转。
- 新增唤醒阈值：`EMPTY_ACTION_WAKEUP_RETRY_LIMIT = 2` 与 `<thinking-empty-recovery>` 运行时前缀。
- 强化 `split_thinking_content`，支持宽容 `<think>` 解析和未闭合标签兜底。

4. 内存有界差异渲染与热点保留
- 新增 `_compress_rows_keep_hotspot`，保留修改热点并压缩未改动上下文。
- 在 `make_numbered_diff` 与 `build_code_preview_rows` 中新增动态 `buffer_cap`。

5. Todo 归属与仲裁治理
- Todo 项新增 `owner` 与 `key` 字段。
- 新增批量控制：`complete_active()`、`complete_all_open()`、`clear_all()`。
- 新增仲裁约束：`ARBITER_VALID_PLANNING_STREAK_LIMIT = 4`。

6. 运行时依赖与控制平面杂项
- 新增导入：`deque`、`selectors`、`signal`、`shlex`。
- 扩展 `RUNTIME_CONTROL_HINT_PREFIXES`：`<arbiter-continue>`、`<fault-prefill>`。

### 2026-03-07 架构创新点
- 基于共享黑板的单体化同频多智能体协作。
- 工业级熔断保护，确保有边界的收敛执行。
- OOM 安全的热点渲染，支撑大规模差异展示。
- 自适应思考唤醒，修复空动作漂移。

---

## 日本語

### 優先度順の更新内容

1. コアアーキテクチャとマルチエージェント（最優先）
- 実行モード定数を追加：`EXECUTION_MODE_SINGLE`、`EXECUTION_MODE_SEQUENTIAL`、`EXECUTION_MODE_SYNC`。
- 役割定義を追加：`AGENT_ROLES = ("explorer", "developer", "reviewer")` と `manager` を含む `AGENT_BUBBLE_ROLES`。
- タスクレベル戦略 `TASK_LEVEL_POLICIES`（`L1`〜`L5`）を追加。
- Blackboard 状態 `BLACKBOARD_STATUSES` を追加：`INITIALIZING`、`RESEARCHING`、`CODING`、`TESTING`、`REVIEWING`、`COMPLETED`、`PAUSED`。

2. サーキットブレーカとドリフト抑制強化
- `CircuitBreakerTriggered` を追加し、不可逆失敗でハード停止可能に。
- 閾値を追加：`HARD_BREAK_TOOL_ERROR_THRESHOLD = 3`、`HARD_BREAK_RECOVERY_ROUND_THRESHOLD = 3`、`FUSED_FAULT_BREAK_THRESHOLD = 3`。

3. 深い推論モデル向け思考出力リカバリ
- 実行アクション不在を検知する `EmptyActionError` を追加。
- ウェイクアップ制御：`EMPTY_ACTION_WAKEUP_RETRY_LIMIT = 2` と `<thinking-empty-recovery>`。
- `split_thinking_content` を寛容化し、未閉じ `<think>` タグをフォールバック処理。

4. メモリ有界差分描画とホットスポット保持
- 変更領域保持圧縮 `_compress_rows_keep_hotspot` を追加。
- `make_numbered_diff` と `build_code_preview_rows` に動的 `buffer_cap` を追加。

5. Todo 所有権と仲裁ガバナンス
- Todo に `owner` と `key` を追加。
- 一括制御 API：`complete_active()`、`complete_all_open()`、`clear_all()`。
- 仲裁制約 `ARBITER_VALID_PLANNING_STREAK_LIMIT = 4` を追加。

6. ランタイム依存と制御プレーン雑項
- 追加 import：`deque`、`selectors`、`signal`、`shlex`。
- `RUNTIME_CONTROL_HINT_PREFIXES` を拡張：`<arbiter-continue>`、`<fault-prefill>`。

### 2026-03-07 アーキテクチャ革新点
- 共有 Blackboard によるモノリシック同周波数マルチエージェント協調。
- 収束境界を保証する産業グレードのサーキットブレーカ。
- 大規模差分でも耐える OOM 安全ホットスポット描画。
- 空アクションを回収する適応型思考ウェイクアップ。
