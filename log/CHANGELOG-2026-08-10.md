# CHANGELOG 2026-08-10

## Full architecture review: current runtime vs the 2026-06-22 baseline

This review compares the current `Clouds_Coder.py` with the local `Clouds_Coder_3.54_0.py` baseline and the official GitHub release `v2026.06.22` (`Clouds Coder 2026.06.22-Stable`, published 2026-06-22). The official release asset was downloaded in ranged blocks and verified against GitHub's declared SHA-256. The local baseline has the same 822 top-level AST statements and 88,346 source lines as the official asset; its only byte-level difference is an extra `nonlocal event_name` in the SSE parser closure, so the local file is treated as a release-equivalent packaging variant for the structural comparison.

### Audit evidence

| Metric | 2026-06-22 baseline | Current `Clouds_Coder.py` | Delta |
| --- | ---: | ---: | ---: |
| File size | 4,723,922 bytes (local baseline) | 5,541,692 bytes | +817,770 bytes |
| Source lines | 88,346 | 103,114 | +14,768 |
| Top-level AST statements | 822 | 874 | +52 |
| Top-level assignments | 467 | 492 | +25 |
| Top-level functions | 239 | 262 | +23 |
| Top-level classes | 41 | 45 | +4 |
| Built-in tools | 49 | 50 | +1 |
| CLI `add_argument` option strings | 106 | 112 | +6 |
| API route string inventory | 66 | 81 | +15 |

Official asset evidence:

- Release: <https://github.com/FonaTech/Clouds-Coder/releases/tag/v2026.06.22>
- Asset: `Clouds_Coder.py`, 4,723,910 bytes
- Official SHA-256: `1cf04bc125e0c48fc5f400afb7f6469b9ebbad1226a7b2a1f2bd4a83ff9afeab`
- Local `Clouds_Coder_3.54_0.py` SHA-256: `df36bedb92e6bc9c668c5586939ea667ddf5e7bcb457ed383d31bc201972963b`
- Both baseline files parse successfully and have identical top-level statement/line counts. The 12-byte local size difference is the source-level `nonlocal event_name` variation described above, not a hidden feature delta.

## English

### Headline: a governed admin plane, an immutable App Store runtime, measurable model operations, and evidence-bound execution

#### 1. Admin authentication and configuration became a first-class control plane

- Added `AdminAuthStore` and `AdminAuthError` with SQLite-backed credentials, password hashing, short-lived revocable browser sessions, token exchange, setup/login/logout, and bounded login rate limiting.
- Added `/admin` plus `/api/admin/auth/{status,setup,login,token-login,session,logout}`. Passwords and raw tokens are not stored in telemetry or application records.
- Added a typed startup configuration schema with coercion, range/choice validation, effective-port conflict checks, default/initial reset, export/import, and supervised restart preflight. A failed restart terminates the replacement process and rolls back to the last known-good configuration.
- Global skill mutation, IDE writes, RAG writes, Code RAG writes, MCP write actions, and other administrative mutations now pass authenticated-admin and same-origin/trusted-client checks.

#### 2. App Store and application runtime isolation

- Added `ApplicationRegistry` and the `clouds-coder-app-store-v1` contract.
- Users can create, edit, delete, launch, and submit personal applications assembled from up to eight Skills. Shared applications move through immutable submitted revisions and administrator review/publication lifecycle states.
- Application launches use immutable, integrity-checked Skill snapshots. Resource files are bounded (128 files / 64 MB), oversized resources are externalized safely, and hard application mode cannot fall back to mutable global Skills. Snapshot paths are protected from IDE and shell mutation.
- Added `/api/apps/personal`, `/api/apps/shared`, `/api/apps/skills`, `/api/apps/` and `/api/admin/apps` routes, including approve/reject and publish/unpublish lifecycle actions.

#### 3. Low-contention telemetry and admin metrics

- Added `TelemetryStore` backed by `telemetry.sqlite`, with indexes for time, user, model, tool, kind, and application.
- `OllamaClient` now emits bounded model-operation telemetry (provider/model, operation status, duration, token usage when available, and error class). Prompts, tool arguments, secrets, and raw responses are deliberately excluded.
- Added `/api/admin/metrics` with time-window and user-hash filters, percentile/bucket summaries, model/tool breakdowns, and failure counts. This is an observability surface, not a benchmark claim; no external performance benchmark was inferred from source inspection.

#### 4. Todo and plan completion reliability was substantially tightened

- Added `TodoWriteResume` so a worker can reconcile an existing Todo graph without restating or duplicating work.
- Added configurable L2 Todo policy (`force`, `auto`, `off`) and an optional single/no-plan bootstrap (`--single-no-plan-todo`, `--single-no-plan-todo-prompt`, `--no-single-no-plan-todo`). The bootstrap is bounded and restores normal tools after success or a recorded failure.
- Added transaction snapshots and stale-write rejection, canonical numbering/deduplication for plan workers, foreign-step filtering, revision identity checks, evidence binding, semantic completion review, acceptance-contract checks, browser/runtime evidence handling, and atomic step advancement.
- These paths bind completion to tool evidence, artifacts, exit status, and acceptance terms instead of trusting a model's “done” text alone. A passing claim without the required evidence remains unresolved.

#### 5. HTTP, encoding, and workspace safety hardening

- Added safe UTF-8 byte/text helpers and bounded JSON request-body readers that close unread bodies, preventing malformed payloads and connection reuse issues from leaking into handlers.
- Added trusted client-IP extraction, same-origin write checks, bearer-token parsing, consistent admin error responses, and role-aware shell mutation guards.
- IDE hard-snapshot/application-snapshot paths are explicitly read-only; global Skills and immutable application resources cannot be changed through an unprivileged route.

#### 6. Port and service topology is now explicit

- The default auxiliary layout is agent `P`, Skills `P+1`, RAG `P+2`, Code `P+3`, MCP `P+4`, IDE `P+5`.
- Admin validation only counts services enabled in the submitted configuration, so a disabled service cannot reserve or conflict with another service's port.

#### 7. Source splitter now reflects the real architecture

- The current split is source-complete: `Code_Structure/.split_manifest.json` records all 874/874 top-level statements, 820 source-defined names, 53 real source modules, and zero unclassified statements.
- The generated package contains actual source fragments in `admin/`, `app/`, `agent/`, `config/`, `ide/`, `llm/`, `mcp/`, `rag/`, `server/`, `session/`, `skills/`, `utils/`, and `web/`. It does not import, read, or depend on the original monolith through a bridge module.
- `Code_Structure/_runtime.py` only preserves original top-level initialization order and shared globals required by the legacy dependency graph. The source modules remain navigable and independently syntax-checked.
- Validation completed: 69 generated Python files compile; package import works without importing the original `Clouds_Coder.py`; `python -m Code_Structure --help` works; launcher help works on the root scripts.

### Review notes and remaining boundaries

- No top-level definition was removed. The largest changed surface is `SessionState` (856 → 1,023 methods), followed by `AppContext` (158 → 173), `Handler` (17 → 24), and `OllamaClient` (54 → 61).
- The release baseline and current file are both single-file runtimes; the split package is a navigation/import artifact and does not replace the supported `python Clouds_Coder.py` entry point.
- Source review confirms policy and guard paths, but it does not substitute for deployment-specific penetration testing, provider latency benchmarks, or a full browser regression suite.

## 中文

### 标题：管理控制面、不可变应用商店、可量化模型遥测，以及绑定证据的执行收敛

本次审查以本地 `Clouds_Coder_3.54_0.py` 和官方 GitHub `v2026.06.22` 发布资产为基线。官方资产已分块下载并通过声明的 SHA-256 校验；本地基线与官方文件拥有相同的 822 个顶层 AST 语句和 88,346 行，仅在 SSE 闭包中多出一处 `nonlocal event_name`，因此按发布等价变体进行结构对比。

#### 1. 管理员认证与配置成为一等控制面

- 新增 `AdminAuthStore` / `AdminAuthError`：SQLite 凭据、密码哈希、短期可撤销浏览器会话、Token 换取、首次设置/登录/退出和有界登录限流。
- 新增 `/admin` 与 `/api/admin/auth/{status,setup,login,token-login,session,logout}`；密码和原始 Token 不写入遥测或应用记录。
- 新增带类型的启动配置 schema：类型转换、范围/枚举校验、有效端口冲突检测、默认/初始重置、导入导出、重启预检。重启失败会终止替代进程并回滚到上一个可用配置。
- 全局 Skill、IDE、RAG、Code RAG、MCP 等写操作现在经过管理员认证与同源/可信客户端校验。

#### 2. 应用商店与运行时隔离

- 新增 `ApplicationRegistry` 和 `clouds-coder-app-store-v1` 合约。
- 用户可从最多 8 个 Skills 组合、编辑、删除、启动个人应用，并提交共享审核；共享应用通过不可变提交版本和管理员审核/发布生命周期。
- 启动时使用完整性校验的不可变 Skill 快照；资源上限为 128 个文件 / 64 MB，过大资源安全外置；硬应用模式不能回退到可变的全局 Skills；IDE 与 shell 不能修改快照路径。
- 新增 `/api/apps/personal`、`/api/apps/shared`、`/api/apps/skills`、`/api/apps/` 与 `/api/admin/apps`，包含审核和上下架操作。

#### 3. 低争用遥测与管理员指标

- 新增 SQLite `telemetry.sqlite` 与 `TelemetryStore`，按时间、用户、模型、工具、类型和应用建立索引。
- `OllamaClient` 记录受限模型操作遥测（provider/model、状态、耗时、可用时的 token 用量和错误类别），刻意不记录 prompt、工具参数、密钥或原始响应。
- 新增 `/api/admin/metrics`，支持时间窗与用户哈希筛选、分位数/桶统计、模型/工具拆分和失败计数。它是可观测接口，不代表未经实测的性能基准。

#### 4. Todo/Plan 完成可靠性

- 新增 `TodoWriteResume`，允许 worker 对已有 Todo 图做规范化对齐，避免重复描述和重复编号。
- 新增 L2 Todo 策略 `force/auto/off` 及可选 single/no-plan bootstrap；相关 CLI 为 `--l2-todo-policy`、`--single-no-plan-todo`、`--single-no-plan-todo-prompt`、`--no-single-no-plan-todo`。bootstrap 有界重试，成功或失败记录后恢复正常工具。
- 新增事务快照与过期写入拒绝、plan worker 规范编号/去重、跨步骤过滤、修订身份校验、证据绑定、语义完成复核、验收合约检查、浏览器/运行时证据和原子推进。
- 完成状态绑定工具证据、工件、退出码和验收条件，不再只信任模型的“已完成”文字。

#### 5. HTTP、编码与工作区安全

- 新增安全 UTF-8 与有界 JSON body 读取，未读 body 会主动关闭，降低畸形请求和连接复用问题。
- 新增可信客户端 IP、同源写保护、Bearer Token 解析、统一管理员错误和按角色的 shell 变更防护。
- IDE 硬快照/应用快照路径只读；未授权路由不能修改全局 Skills 或不可变应用资源。

#### 6. 端口拓扑与拆分架构

- 默认端口为 agent `P`、Skills `P+1`、RAG `P+2`、Code `P+3`、MCP `P+4`、IDE `P+5`；配置校验只统计实际启用的服务。
- `Code_Structure/.split_manifest.json` 证明当前拆分覆盖 874/874 个顶层语句、820 个源码定义名称、53 个真实源码模块、0 个未分类语句。模块内保存真实源码片段；`_runtime.py` 只负责按原始顺序初始化，不读取或导入原始单文件。

### 审查边界

没有发现顶层定义被删除；最大改动面是 `SessionState`（856 → 1,023 个方法），其次为 `AppContext`（158 → 173）、`Handler`（17 → 24）和 `OllamaClient`（54 → 61）。源码审查确认了策略与防护路径，但不替代部署级渗透测试、Provider 延迟基准或完整浏览器回归测试。

## 日本語

### 見出し：管理プレーン、イミュータブルな App Store、モデル操作テレメトリ、証拠に結び付いた実行収束

本レビューはローカル `Clouds_Coder_3.54_0.py` と公式 GitHub `v2026.06.22` リリースを基準にした。公式アセットは分割範囲で取得して宣言 SHA-256 を検証済みで、ローカル基準版は公式版と同じ 822 トップレベル AST 文・88,346 行を持つ。差分は SSE クロージャの `nonlocal event_name` 1 箇所だけなので、リリース相当のローカル変体として比較した。

#### 1. 管理者認証・設定

- `AdminAuthStore` / `AdminAuthError`、SQLite 資格情報、パスワードハッシュ、短期で失効可能なブラウザセッション、Token 交換、初期設定、ログイン/ログアウト、試行回数制限を追加。
- `/admin` と `/api/admin/auth/...`、型付き設定 schema、範囲/列挙/実効ポート検証、初期/既定値リセット、エクスポート/インポート、監視付き再起動を追加。再起動失敗時は既知の正常設定へロールバックする。
- Skills、IDE、RAG、Code RAG、MCP の管理書き込みは管理者認証と same-origin / trusted-client 検査を通過する必要がある。

#### 2. App Store と実行分離

- `ApplicationRegistry` と `clouds-coder-app-store-v1` 契約を追加。最大 8 Skills の個人アプリ、審査可能な共有アプリ、不可変リビジョン、公開/非公開ライフサイクルを提供する。
- 起動時は整合性検証済みの Skill スナップショットを使い、128 ファイル / 64 MB の資源上限、外部化、ハードアプリモードのグローバル Skill フォールバック禁止、スナップショット書き込み禁止を適用する。
- `/api/apps/personal`、`/api/apps/shared`、`/api/apps/skills`、`/api/apps/`、`/api/admin/apps` を追加。

#### 3. テレメトリと計画信頼性

- `TelemetryStore`（`telemetry.sqlite`）と `/api/admin/metrics` を追加。モデル/ツール操作の状態、所要時間、利用可能な token 数、エラー分類を低競合で集計し、prompt・引数・秘密・生レスポンスは保存しない。
- `TodoWriteResume`、L2 Todo ポリシー（`force/auto/off`）、single/no-plan bootstrap、トランザクション世代、古い書き込みの破棄、worker の正規採番/重複排除、証拠バインディング、意味的完了審査、受入条件、原子的なステップ進行を追加。
- 完了は「完了」と書かれたモデル文ではなく、ツール証拠・成果物・終了コード・受入条件で判定する。

#### 4. 分割ツールと検証

- `Code_Structure/.split_manifest.json` は 874/874 文、820 ソース定義名、53 実ソースモジュール、未分類 0 を記録する。各モジュールに実際のソース片があり、`_runtime.py` は初期化順序と共有グローバルだけを維持し、元モノリスを読み込まない。
- 69 個の生成 Python ファイルが compile 済みで、元ファイルなしの package import、`python -m Code_Structure --help`、各ランチャーの help が通過した。

### レビュー境界

トップレベル定義の削除はない。最大の変更面は `SessionState`（856 → 1,023 メソッド）、次に `AppContext`（158 → 173）、`Handler`（17 → 24）、`OllamaClient`（54 → 61）。ソースレビューは実装されたポリシー/ガードを確認するが、配備環境の侵入試験、Provider ベンチマーク、完全なブラウザ回帰試験を代替しない。
