# CHANGELOG 2026-05-28

## Role-isolated multi-agent context, stronger tool-reading path, and clearer runtime observability

This update turns multi-agent mode into a practical long-horizon execution strategy for short-context local models: agents now carry separate working contexts, compact independently under the existing tiered compression framework, and expose their live context pressure in the Web UI only when multi-agent mode is actually active.

---

## English

### Headline: Multi-agent context isolation for long-running work on short-context models

#### 1. Role-isolated context budgets

- Multi-agent sessions now track context pressure by active call and role instead of presenting one ambiguous global number.
- Manager, Explorer, Developer, and Reviewer can each keep their own working context shape, so research, implementation, and review traces no longer compete as aggressively inside a single prompt lane.
- Single-agent sessions still use the original single context budget display and do not expose stale inactive agent contexts.

#### 2. Independent tiered compression per agent

- The existing normal/light/medium/heavy compression framework is preserved.
- Multi-agent mode now applies that framework per active role, allowing the tightest agent to compact without flattening every other role's context at the same time.
- This improves long-line task continuity for smaller local models because each role can retain the evidence most relevant to its own job.

#### 3. Long-horizon capability for short-context models

- The architecture intentionally uses role separation as a context-scaling technique: Explorer can keep discovery notes, Developer can keep implementation state, Reviewer can keep validation evidence, and Manager can keep routing state.
- This makes multi-agent mode valuable even when the model itself has limited context, because the runtime can preserve specialized state and only inject the role context needed for the next call.
- The result is better continuity across research → edit → validate → repair loops without requiring a single huge prompt.

#### 4. Context UI semantics

- The top context indicator keeps the original single bar in single mode.
- Once a session enters sync/sequential multi-agent mode, the same slot shows nested role bars sorted by tightest remaining context first.
- The smallest remaining context is displayed as the outer lane, so the most constrained role is visually prominent.
- Role chips appear only for real multi-agent execution, not for L1/L2 single tasks or stale contexts from previous runs.

#### 5. Tool and preview path refinements

- File-reading and long-output behavior was strengthened around flexible access rather than defensive early exit.
- Chat bubble code/diff previews preserve whitespace and indentation, making function structure and patch shape readable in the conversation stream.
- Runtime mode fallback was corrected so completed L1/L2 single tasks do not regress to global sync-mode display after the run resets transient runtime fields.

### 2026-05-28 Summary

- Added role-aware context budget snapshots for active multi-agent calls
- Added per-role independent compression under the existing tiered compact framework
- Kept single-mode context display as the original single global bar
- Added nested multi-agent context bars and localized role-specific context labels
- Fixed stale multi-agent context display after simple single-agent tasks finish
- Improved chat bubble code/diff whitespace preservation

---

## 中文

### 标题：用分角色上下文隔离提升短上下文模型的长线处理能力

#### 1. 分 Agent 上下文预算

- 多 Agent 会话现在按真实调用角色展示上下文压力，不再只给一个含义模糊的全局数值。
- Manager、Explorer、Developer、Reviewer 可以保持各自的工作上下文形态，让调研、实现、审查轨迹不再全部挤进同一条 prompt 通道。
- Single-agent 会话保持原来的单一上下文显示，不暴露历史遗留的未激活 agent context。

#### 2. 分 Agent 独立分层压缩

- 保留现有 normal/light/medium/heavy 分级压缩框架。
- 多 Agent 模式下按活跃角色独立应用压缩，让最紧张的 agent 可以先压缩，而不是把所有角色上下文一起压平。
- 这对短上下文本地模型尤其重要，因为每个角色可以保留与自身职责最相关的证据。

#### 3. 短上下文模型的长线能力放大

- 本次架构把角色拆分明确作为一种 context scaling 技术：Explorer 保留发现和证据，Developer 保留实现状态，Reviewer 保留验证依据，Manager 保留路由与裁决状态。
- 即便模型自身上下文较短，运行时也能通过分角色状态保存，只把下一次调用需要的角色上下文注入模型。
- 因此 research → edit → validate → repair 的长链路不再依赖单次巨大 prompt，连续性更强。

#### 4. 上下文 UI 语义

- Single 模式顶部上下文条保持原有单条进度显示。
- 会话真实进入 sync/sequential 多 Agent 后，同一槽位切换为嵌套角色进度条，并按剩余上下文最紧张优先排序。
- 剩余最少的角色显示在最外层，让最容易耗尽上下文的 agent 在视觉上最突出。
- 角色 chips 只在真实多 Agent 执行时显示，L1/L2 简单 single 任务和历史残留 context 不再唤出多 Agent 展示。

#### 5. 工具读取与预览链路细化

- read file / 长输出路径从“被动防御式截断”转向更灵活的读取能力，减少简单保护导致的提前退出。
- 对话气泡中的代码 / diff 预览保留真实空格与缩进，函数结构和补丁结构可以直接读出来。
- 修复 L1/L2 single 任务结束后 transient runtime 字段清空，UI 又回落到全局 sync 显示的问题。

### 2026-05-28 更新摘要

- 新增按真实多 Agent 调用角色统计的上下文预算快照
- 在现有分层 compact 框架下新增分角色独立压缩
- Single 模式保持原有单一上下文进度条
- 新增嵌套式多 Agent 上下文进度条与多语言角色剩余标签
- 修复简单 single 任务结束后显示历史多 Agent context 的问题
- 改进对话气泡代码 / diff 预览的空格与缩进保真

---

## 日本語

### 見出し：ロール別コンテキスト分離で短コンテキストモデルの長期処理を強化

#### 1. Agent 別コンテキスト予算

- マルチエージェント session は、曖昧な単一グローバル値ではなく、実際の呼び出しロールごとにコンテキスト圧力を表示します。
- Manager、Explorer、Developer、Reviewer はそれぞれの作業コンテキストを保持でき、調査・実装・レビューの痕跡が同じ prompt レーンで過度に競合しにくくなります。
- Single-agent session は従来通り単一コンテキスト表示を維持し、過去の非アクティブ agent context を表示しません。

#### 2. Agent 別の独立階層圧縮

- 既存の normal/light/medium/heavy 圧縮フレームワークを維持します。
- マルチエージェント mode では active role ごとに圧縮を適用し、最も逼迫した agent だけを先に compact できます。
- 各ロールが自分の仕事に最も関係する証拠を保持できるため、短コンテキストのローカルモデルで長い作業を続けやすくなります。

#### 3. 短コンテキストモデル向けの長期処理能力

- ロール分離を context scaling 技術として扱います。Explorer は発見事項、Developer は実装状態、Reviewer は検証根拠、Manager はルーティング状態を保持します。
- モデル自体のコンテキストが短くても、runtime は専用状態を保存し、次の呼び出しに必要なロールコンテキストだけを注入できます。
- research → edit → validate → repair の長いループが、単一の巨大 prompt に依存しにくくなります。

#### 4. コンテキスト UI セマンティクス

- Single mode ではトップのコンテキストバーは従来の単一バーのままです。
- session が実際に sync/sequential マルチエージェント mode に入ると、同じスロットがネストされたロールバーに切り替わり、残りコンテキストが最も少ない順に並びます。
- 最も残りが少ないロールを外側レーンとして表示し、最も制約の強い agent が視覚的に目立つようにしました。
- ロール chips は本物のマルチエージェント実行時だけ表示され、L1/L2 single task や過去 context では表示されません。

#### 5. ツール読み取りとプレビュー経路の改善

- read file / 長出力の経路は、防御的な早期終了よりも柔軟な読み取り能力を重視する方向に強化されました。
- チャットバブル内の code/diff preview は空白とインデントを保持し、関数構造や patch 形状を会話内で確認しやすくなりました。
- L1/L2 single task 終了後に transient runtime field が消え、UI が global sync 表示へ戻る問題を修正しました。

### 2026-05-28 要約

- 実際のマルチエージェント呼び出しロール別のコンテキスト予算 snapshot を追加
- 既存の階層 compact フレームワーク上でロール別独立圧縮を追加
- Single mode は従来の単一コンテキストバーを維持
- ネスト型マルチエージェントコンテキストバーと多言語ロール別残量ラベルを追加
- simple single task 終了後に過去の multi-agent context が表示される問題を修正
- チャットバブル code/diff preview の空白・インデント保持を改善
