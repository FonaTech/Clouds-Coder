# CHANGELOG 2026-10-30 · Liquid Kernel

## English · Task-driven evolution and reliable execution

Liquid Kernel now combines a task-driven evolution loop with capability-19 execution and feedback defenses. The optimization target is the Agent's complete problem-solving flow: planning, tool routing, context use, memory access, recovery, and verification. Edit strength determines which code modules may change. The framework improvements below make that loop more executable and its comparisons more dependable.

### Evolution with observable outcomes

The existing loop derives multi-turn tasks from the configured session scope and executes real model/tool trajectories in isolated workspaces. Baseline and candidate run the same frozen task bank. Produced artifacts, independent review, completion, and execution cost contribute to comparison; holdout tasks and independent paired confirmation check whether a gain persists.

Candidates remain independent, inspectable versions even when they are worse. Code, diffs, parent versions, scores, traces, and rejection reasons are retained. Automatic deployment accepts only a completed real evaluation with no regression, successful independent confirmation, and a score strictly above the baseline. Eligible versions still pass the configured Canary process. A failed confirmation rejects deployment while preserving the experiment.

### Capability 19: a stronger execution and feedback foundation

- **Portable execution:** bounded `re`, Pattern/Match operations, and `chr`/`ord` extend the constrained interpreter on systems without a native sandbox. Regex work has time/data limits; file access remains workspace-bound.
- **Evaluator reliability:** task design and execution share capability declarations. AST checks reject unsupported imports, module members, and constructs during definition repair, before they can distort task scores. Frozen assertions and historical scores are preserved.
- **Shared runtime resilience:** common model transport handles unlimited requests without `float(None)`. Structured recovery distinguishes intermediate thinking, truncated output, and a valid final body. Explicit UTF-8 boundaries support multilingual inputs. The IDE enhancement compatibility fixes are one consumer of these shared runtime improvements.

### Delivering the same kernel in every form

`Clouds_Coder.py` embeds the released kernel sources, and startup preserves existing evolved artifacts, session pins, and rollback history. Splitter **3.1** assigns **1276 statements and 1192 defined names** to **68 source modules**, reducing unclassified declarations from **37 to 0**. Concurrency gates, evidence retrieval, context state, cancellation state, Todo parsing, JSON recovery, and toolchains now have explicit owners. Default and auto-layout share these rules; genuinely unknown declarations stay visible and a regression check covers the current monolith.

Clean-checkout CI now initializes the public single-file entrypoint before importing kernel tests. `pyproject.toml` carries pytest paths, and the source update includes `tools` and the skill fixture. Permission-denied external skill folders no longer abort ordinary tasks; sandbox readiness checks all namespace features used by execution. The user's separately repaired workflows are preserved.

The earlier paired evaluation proves the comparison and rejection path; it does not establish that every candidate improves. Capability-19 regressions, portable execution, embedded/split delivery, and real shared-runtime model calls have separate evidence. See [kernel architecture](../liquid_kernel/README.md), [paired-run evidence](../docs/candidate_retention_verification_20261028.md), and [current delivery/CI verification](../docs/liquid_kernel_delivery_verification_20261030.md).

## 中文 · 任务驱动进化与执行可靠性

Liquid Kernel 将现有任务驱动进化闭环与能力版本 19 的执行、反馈防御结合起来。优化对象是 Agent 完成目标的整条链路：规划、工具路由、上下文使用、记忆访问、恢复和验证。修改强度控制可变更的代码模块。本次进步集中在让闭环能实际运行、比较结果更可信、已验证的内核能一致交付。

### 用可观察结果推动进化

现有闭环从配置范围内的会话提取多轮任务，在隔离工作区执行真实模型与工具轨迹。基线与候选运行同一批冻结任务，结合产物、独立审核、完成情况与执行成本进行比较，并通过 holdout 任务和独立成对复跑检验收益能否保持。

候选即使退步，也作为独立、可检查的版本留存，保留代码、差异、父版本、评分、轨迹和拒绝原因。自动部署只接受完成真实评测、无回归、独立复跑通过，且评分严格高于基线的候选；符合条件的版本仍按配置进入 Canary。复跑失败会拒绝部署，同时保留这次实验。

### 能力 19：增强执行与反馈基础

- **跨平台执行：** 受限解释器新增有资源边界的 `re`、Pattern/Match 与 `chr`/`ord`，让没有原生沙箱的环境也能完成更多常见操作。正则执行受时间与数据限制，文件访问限定在工作区。
- **评测器可靠性：** 任务设计与执行共用能力声明，AST 检查在定义修复阶段识别不支持的导入、模块成员和语法，减少错误验收对任务分数的干扰。冻结断言与历史分数保持原样。
- **共享运行时韧性：** 公共模型传输修复不限时请求的 `float(None)`，结构化恢复区分中间思考、截断输出和有效最终正文，显式 UTF-8 边界支持多语言输入。IDE 增强器的兼容修复是这些公共改进的一个使用入口。

### 将同一个内核交付到不同运行形式

`Clouds_Coder.py` 内嵌发布的内核源码，启动保留已有进化产物、会话固定版本和回退历史。拆分器 **3.1** 将 **1276 条语句、1192 个定义名**归入 **68 个源码模块**，未归类声明从 **37 降到 0**。并发门控、证据检索、上下文状态、取消状态、Todo 解析、JSON 恢复与工具链现在都有明确归属。默认和自动布局共用这些规则；真正未知的声明仍可见，当前主文件的归类完整性已有回归检查。

干净检出的 CI 会先初始化单文件入口，再导入内核测试；`pyproject.toml` 同步 pytest 路径，源码更新包含 `tools` 与技能夹具。外部技能目录无权限不再中止普通任务，沙箱探测覆盖实际使用的全部命名空间。用户单独修好的工作流保持原样。

前阶段的成对实测验证了比较、留存与拒绝路径，不代表每个候选都会进步。能力 19 的回归、可移植执行、内嵌／拆分交付和公共运行时真实模型调用分别留有证据。详见[内核架构](../liquid_kernel/README.md)、[成对运行记录](../docs/candidate_retention_verification_20261028.md)和[本次交付／CI 验证](../docs/liquid_kernel_delivery_verification_20261030.md)。

## 日本語 · タスク駆動の進化と実行の信頼性

Liquid Kernel は既存のタスク駆動の進化ループと、能力バージョン 19 の実行・フィードバック保護を組み合わせます。最適化の対象は、計画、ツール選択、コンテキスト利用、記憶検索、回復、検証を含む Agent の問題解決全体です。変更強度が編集可能なコード範囲を決定します。本更新はループの実行性、比較の信頼性、検証済みカーネルの一貫した配布を改善します。

### 観測可能な結果に基づく進化

既存ループは設定されたセッション範囲から複数ターンのタスクを作り、隔離した作業領域で実モデルとツールの軌跡を実行します。ベースラインと候補は同じ凍結タスク群を使います。成果物、独立レビュー、完了状況、実行コストを比較し、holdout タスクと独立した対再実行で改善の再現性を確認します。

悪化した候補も独立した検査可能なバージョンとして保持し、コード、差分、親バージョン、得点、軌跡、却下理由を残します。自動配置には、実評価の完了、回帰なし、独立再実行の成功、ベースラインを厳密に上回る得点が必要です。適格なバージョンは設定済み Canary を通過します。確認に失敗した場合は配置を拒否し、実験自体は保持します。

### 能力 19：実行とフィードバックの基盤を強化

- **移植可能な実行：** 制限付き実行器に、資源制限付きの `re`、Pattern/Match、`chr`/`ord` を追加しました。ネイティブサンドボックスのない環境でも一般的な操作を増やし、正規表現の時間・データ量と作業領域内のファイル境界を維持します。
- **評価器の信頼性：** タスク設計と実行が能力定義を共有します。未対応の import、メンバー、構文を定義修復段階の AST 検査で検出し、不適切な検証による得点への影響を減らします。凍結した検証条件と履歴の得点は保持します。
- **共有ランタイムの回復力：** 共通通信の時間制限なし要求で起きる `float(None)` を修正しました。構造化回復は中間思考、切り詰め、完全な最終本文を区別し、UTF-8 境界で多言語入力を支えます。IDE 強化機能は、この共通修正を利用する箇所の一つです。

### 同じカーネルを異なる実行形態へ配布

`Clouds_Coder.py` はリリース対象のカーネルソースを内蔵し、起動時に既存の進化成果物、セッション固定版、ロールバック履歴を保持します。分割ツール **3.1** は **1276 文、1192 定義名**を **68 ソースモジュール**へ割り当て、未分類を **37 から 0** に減らしました。並列ゲート、証拠検索、コンテキスト状態、取消状態、Todo 解析、JSON 回復、ツールチェーンに所有モジュールを定義しました。標準・自動レイアウトは規則を共有し、未知の宣言は表示し続けます。現在の単一ファイルには分類の回帰検査があります。

新規チェックアウトの CI は、カーネルテストの import 前に単一ファイル入口を初期化します。`pyproject.toml` に pytest のパスを設定し、`tools` とスキルのテストデータも配布します。外部スキルのアクセス拒否で通常タスクが中断せず、サンドボックス検出は実行時の全名前空間を確認します。利用者が修復したワークフローは変更しません。

前段階の対実測は比較・保持・却下の経路を確認したもので、すべての候補の改善を示すものではありません。能力 19 の回帰、移植可能な実行、内蔵・分割配布、共有通信の実モデル呼び出しには個別の証拠があります。[カーネル構成](../liquid_kernel/README.md)、[対実行記録](../docs/candidate_retention_verification_20261028.md)、[今回の配布・CI 検証](../docs/liquid_kernel_delivery_verification_20261030.md)を参照してください。
