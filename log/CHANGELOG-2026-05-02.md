# CHANGELOG 2026-05-02

## Persistent Wiki RAG + workflow memory + provider resilience + importable split architecture

This update moves Clouds Coder beyond one-shot chunk retrieval: RAG now gains an accumulated Markdown Wiki layer, programming RAG gains scored workflow memory, private vLLM / OpenAI-compatible providers gain long-delay retry governance, and `split_coder.py` can regenerate an importable architecture package for navigating the monolithic runtime.

---

## English

### Headline: Accumulated Wiki RAG, programming workflow memory, and more resilient model/runtime architecture

#### 1. Persistent Wiki RAG layer

- Added `WikiStore`, a durable Markdown wiki compiler for both knowledge libraries and code libraries.
- The wiki is generated under each library root as `wiki/`, with:
  - `sources/`: source-level pages
  - `entities/`: recurring entity / symbol / domain-term pages
  - `concepts/`: community and graph-derived concept pages
  - `synthesis/overview.md`: compact library-wide overview
  - `index.md`: first-hop catalog for retrieval
  - `log.md`: chronological maintenance log
  - `schema.md`: maintenance and query convention file
- Query flow is now wiki-first for accumulated synthesis, then raw chunks for exact evidence and line-level details.
- Knowledge Wiki RAG and Code RAG are separated at the architecture level, so general knowledge synthesis and programming/code retrieval can evolve independently.

#### 2. Programming RAG workflow memory

- Added `WorkflowMemoryStore` for accepted programming workflow patterns captured from completed sessions.
- Sessions are scored from completion signals, code-edit operations, validation/test steps, todo progress, structured planning, and multi-node coordination.
- High-quality workflows are filed as Markdown cards under the code wiki workflow memory and become retrievable with the `workflow` route.
- Code RAG can now retrieve both source-code evidence and proven process patterns, strengthening small-model task handoff, tool-use sequencing, and implementation continuity.

#### 3. Private vLLM / OpenAI-compatible provider resilience

- Model HTTP retry governance now defaults to 5 retries with a 60-second retry interval.
- Transient statuses include `408`, `409`, `425`, `429`, `500`, `502`, `503`, and `504`.
- vLLM / OpenAI-compatible / LM Studio chat endpoints can also retry nginx/upstream-looking transient `404` responses.
- Retry timing follows `Retry-After`, `X-RateLimit-Reset`, and common JSON retry fields when present.
- Endpoint-level cooldowns reduce repeated hammering of the same failing provider/model endpoint.
- Sessions emit visible status during retry waits, while probe mode avoids long retry delays.

#### 4. Runtime output control

- `AGENT_RUN_COMPLETION_SUMMARY` now defaults to `false`.
- Normal chat completion no longer appends an extra synthetic "task completed" assistant summary bubble.
- Operators can re-enable that completion summary explicitly with `AGENT_RUN_COMPLETION_SUMMARY=true`.

#### 5. Importable split architecture output

- `split_coder.py` now generates a `_source_bridge.py` layer that loads the original `Clouds_Coder.py` once and binds routed symbols from it.
- Generated modules remain importable navigation stubs instead of recursively importing each other and recreating circular dependencies.
- Self-check now validates top-level symbol coverage, `py_compile`, stale generated files, package import walk, entry-point help, and cleanup of generated `__pycache__`.
- RAG/Wiki/Workflow symbols are routed into dedicated RAG modules, reducing unclassified architecture drift.

### 2026-05-02 Summary

- Added persistent Markdown Wiki RAG with `index.md`, `log.md`, and `schema.md`
- Added programming workflow memory for accepted high-quality code workflows
- Added private vLLM / OpenAI-compatible retry and cooldown governance
- Disabled extra run-completion summary bubbles by default
- Made `split_coder.py` generate an importable split architecture package

---

## 中文

### 标题：持久化 Wiki RAG、编程工作流记忆、更稳健的模型与运行时架构

#### 1. 持久化 Wiki RAG 层

- 新增 `WikiStore`，为知识库和代码库生成可持久维护的 Markdown Wiki。
- 每个库根目录下会生成 `wiki/`，包含：
  - `sources/`：来源级页面
  - `entities/`：实体、符号、领域术语页面
  - `concepts/`：由社区与图结构导出的概念页
  - `synthesis/overview.md`：全库概览
  - `index.md`：检索第一跳目录
  - `log.md`：按时间追加的维护日志
  - `schema.md`：维护和查询约定
- 检索链路现在优先使用 Wiki 中的累计综合，再回退到 raw chunks 获取精确证据和行级细节。
- 知识 Wiki 图谱 RAG 与编程 Code RAG 在架构上分离，方便分别优化通用知识综合与代码/工程检索。

#### 2. 编程 RAG 工作流记忆

- 新增 `WorkflowMemoryStore`，从完成后的 session 中捕获可复用的高质量编程工作流。
- 系统会根据完成信号、代码修改、验证/测试步骤、todo 推进、结构化规划、多节点协同等因素自动评分。
- 高质量工作流会以 Markdown 卡片形式收录到代码 Wiki 的 workflow memory，并可通过 `workflow` 路由检索。
- Code RAG 不再只检索代码证据，也能检索已经验证过的过程模式，从而强化小模型的任务交接、工具调用顺序和实现连续性。

#### 3. 私有 vLLM / OpenAI-compatible 模型服务韧性

- 模型 HTTP 重试默认提升为 5 次，重试间隔默认 60 秒。
- 临时状态码覆盖 `408`、`409`、`425`、`429`、`500`、`502`、`503`、`504`。
- vLLM / OpenAI-compatible / LM Studio 的 chat endpoint 对 nginx/upstream 风格的临时 `404` 也可进行重试。
- 若服务端返回 `Retry-After`、`X-RateLimit-Reset` 或常见 JSON retry 字段，系统会按服务端节奏等待。
- endpoint 级 cooldown 避免对同一故障 provider/model 端点反复高频请求。
- 会话会在等待重试时显示状态；探测模式不会触发长时间重试。

#### 4. 运行时输出控制

- `AGENT_RUN_COMPLETION_SUMMARY` 默认改为 `false`。
- 正常对话完成后不再额外追加“任务执行完成”的合成 assistant 气泡。
- 如需恢复该摘要行为，可显式设置 `AGENT_RUN_COMPLETION_SUMMARY=true`。

#### 5. 可导入的拆分架构输出

- `split_coder.py` 现在生成 `_source_bridge.py`，由桥接层加载原始 `Clouds_Coder.py`，再把符号绑定到拆分模块中。
- 生成模块作为可导入的架构导航桩存在，不再互相递归 import 导致循环依赖。
- self-check 覆盖顶层符号一致性、`py_compile`、陈旧生成文件、package import walk、entry-point help、`__pycache__` 清理。
- RAG/Wiki/Workflow 相关符号被路由到专门的 RAG 模块，减少未分类架构漂移。

### 2026-05-02 更新摘要

- 新增持久化 Markdown Wiki RAG，包含 `index.md`、`log.md`、`schema.md`
- 新增编程工作流记忆，用于收录高质量代码工作流
- 新增私有 vLLM / OpenAI-compatible 重试与 cooldown 治理
- 默认关闭额外的任务完成摘要气泡
- `split_coder.py` 现在可生成可导入的拆分架构包

---

## 日本語

### 見出し：永続 Wiki RAG、プログラミングワークフローメモリ、より堅牢なモデル/ランタイム構造

#### 1. 永続 Wiki RAG レイヤー

- `WikiStore` を追加し、知識ライブラリとコードライブラリの両方に永続 Markdown Wiki を生成します。
- 各ライブラリルート配下に `wiki/` が生成され、以下を含みます。
  - `sources/`：ソース単位ページ
  - `entities/`：反復出現するエンティティ、シンボル、ドメイン語ページ
  - `concepts/`：コミュニティとグラフ構造から導く概念ページ
  - `synthesis/overview.md`：ライブラリ全体の概要
  - `index.md`：検索の第一ホップとなるカタログ
  - `log.md`：時系列のメンテナンスログ
  - `schema.md`：保守と検索の規約
- 検索は蓄積済みの統合知識として Wiki を優先し、正確な証拠や行レベル詳細が必要な場合に raw chunk へフォールバックします。
- Knowledge Wiki Graph RAG と Programming Code RAG をアーキテクチャ上分離し、一般知識統合とコード/エンジニアリング検索を別々に進化させられます。

#### 2. プログラミング RAG ワークフローメモリ

- `WorkflowMemoryStore` を追加し、完了済み session から再利用可能な高品質プログラミングワークフローを収集します。
- 完了シグナル、コード編集、検証/テスト手順、todo 進捗、構造化計画、複数ノード協調などから自動スコアリングします。
- 高品質ワークフローは Markdown カードとして code wiki workflow memory に保存され、`workflow` ルートで検索できます。
- Code RAG はコード証拠だけでなく、検証済みのプロセスパターンも検索でき、小型モデルのタスク引き継ぎ、ツール順序、実装継続性を強化します。

#### 3. プライベート vLLM / OpenAI-compatible プロバイダ耐性

- モデル HTTP リトライはデフォルトで 5 回、間隔は 60 秒になりました。
- 一時的ステータスとして `408`、`409`、`425`、`429`、`500`、`502`、`503`、`504` を扱います。
- vLLM / OpenAI-compatible / LM Studio の chat endpoint では、nginx/upstream 由来に見える一時的 `404` もリトライ対象にできます。
- `Retry-After`、`X-RateLimit-Reset`、一般的な JSON retry フィールドがある場合はサーバ側の制御に従います。
- endpoint 単位の cooldown により、同じ provider/model endpoint への過剰な再試行を抑えます。
- リトライ待機中は session status に表示され、probe mode では長時間リトライを避けます。

#### 4. ランタイム出力制御

- `AGENT_RUN_COMPLETION_SUMMARY` のデフォルトを `false` に変更しました。
- 通常のチャット完了後に、追加の「タスク完了」assistant サマリーバブルを出さなくなりました。
- 必要な場合は `AGENT_RUN_COMPLETION_SUMMARY=true` で再有効化できます。

#### 5. import 可能な分割アーキテクチャ出力

- `split_coder.py` は `_source_bridge.py` を生成し、元の `Clouds_Coder.py` を一度だけ読み込んで、ルーティング済みシンボルを各分割モジュールへバインドします。
- 生成モジュールは相互再帰 import を行う実装コピーではなく、import 可能なアーキテクチャナビゲーションスタブになります。
- self-check はトップレベルシンボル一致、`py_compile`、古い生成ファイル、package import walk、entry-point help、`__pycache__` クリーンアップを検証します。
- RAG/Wiki/Workflow 関連シンボルは専用 RAG モジュールにルーティングされ、未分類の構造ドリフトを減らします。

### 2026-05-02 要約

- `index.md`、`log.md`、`schema.md` を備えた永続 Markdown Wiki RAG を追加
- 高品質コードワークフローを収集するプログラミングワークフローメモリを追加
- プライベート vLLM / OpenAI-compatible のリトライと cooldown 制御を追加
- 追加のタスク完了サマリーバブルをデフォルト無効化
- `split_coder.py` が import 可能な分割アーキテクチャパッケージを生成可能に
