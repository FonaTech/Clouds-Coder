# CHANGELOG 2026-06-22

## RAG reinforcement, real MCP client, personalized long-term memory, and graph visualization

This update concentrates on retrieval quality and knowledge plumbing. The RAG engine moved from TF-IDF cosine to BM25 with symbol-exact boosting, gained cross-lingual recall without any embedding model, learned to ingest book-length documents safely, and exposed a self-ingestion tool the agent can use to remember good references. Alongside it, Clouds Coder gained a genuine Model Context Protocol (MCP) client, a redesigned long-term user-memory path that is uniform across modes yet genuinely personalized, and a fully animated 2D/3D knowledge graph with adaptive labels.

---

## English

### Headline: Lexical-only RAG that actually recalls, plus real MCP and personalized memory

#### 1. RAG retrieval moved to BM25 + symbol-exact boost (lexical-only)

- The lexical core of `TFGraphIDFIndex` / `CodeGraphIndex` changed from TF-IDF **cosine** (which length-penalizes and saturates poorly) to **BM25** (`RAG_BM25_K1=1.5`, `RAG_BM25_B=0.6`). Postings now store raw term frequency; length normalization lives in the BM25 denominator.
- Score normalization is **pool-independent saturation** `raw/(raw+RAG_BM25_SATURATION=4.0)`, deliberately **not** min-max. Min-max would force the best candidate in an all-weak pool to 1.0 and break the no-evidence / minimum-synthesis thresholds; saturation preserves absolute relevance so a weak pool stays weak.
- Added a **symbol-exact boost**: when a query token equals a chunk's symbol exactly it gets a strong, idf-independent boost (`0.5·(0.85+0.15·rarity)`); a partial part-match is dampened. Exact identifier queries are high-precision intent, so they now reliably surface the defining chunk.
- Final score (no dense path): `lexical × 0.80 + graph_bonus + symbol_boost`, applied identically to the knowledge RAG and the code RAG.

#### 2. Chunking that preserves structure

- The Python code chunker now **recurses (depth ≤ 4)** into nested functions, closures, decorated helpers, and inner classes, with hierarchical names like `outer.inner` and `Class.method`. Each chunk persists its `symbol` / `symbol_kind` so the symbol boost can see them (these were previously dropped).
- A new boundary-safe splitter (`_rag_boundary_split`) backs each oversized-block cut to the nearest paragraph / sentence / newline / whitespace boundary, with boundary-aligned overlap, replacing the old mid-character slicing.

#### 3. Cross-lingual knowledge retrieval — no embedding model

- Query in Chinese and hit English content (and vice versa) over plain BM25. Two layers cooperate: a curated synonym table (~4000 CN/EN/acronym groups) expanded at both index- and query-time, and a new query-time translation bridge (`_augment_query_cross_lingual`) for arbitrary / out-of-vocabulary terms.
- The bridge detects a single-script query (CJK xor Latin), translates it best-effort via the session model, and appends the translation so a single bilingual query string flows through the existing tokenizer and BM25 in one pass. Cached per normalized query, gated on length, and skips already-bilingual or echo translations. Scope is the knowledge RAG only — code retrieval stays literal. Opt out per request with `cross_lingual=false`.

#### 4. `rag_remember` — agent self-ingestion tool

- The agent can persist a good reference or a distilled finding directly into the knowledge library: `rag_remember(text, title?, tags?, category?, source?)`. It reuses the same dedup/import path as the admin text-import (sha256-deduped, no extra LLM call) with a provenance header.
- Because it writes only to the RAG library and never to user files, it is allowed for the explorer and reviewer roles and in plan-mode research, alongside `write_to_blackboard`.

#### 5. Book-length ingestion, made safe

- `RAG_MAX_CHUNKS_PER_DOC` was raised from 500 to **20000**, and a single `RAG_MAX_DOCUMENT_CHARS` cap (default 12M, env `AGENT_RAG_MAX_DOCUMENT_CHARS`, clamped 150k–40M) now replaces the scattered per-extractor truncation limits across PDF / docx / csv / pptx / xls parsing and the upload re-read path.
- Safety is structural: parsing runs in a spawned subprocess with a hard timeout and terminate/kill, so a huge or slow parse cannot hang the app, and the chunk cap bounds even a pathological multi-million-character input. The `pdftotext` subprocess timeout was aligned to the same parse-timeout budget.

#### 6. Versioned index snapshots

- Snapshots carry a `bm25-v1` format tag plus the new `chunk_lengths` / `avg_chunk_len` fields. On a format mismatch, `restore()` declines and the index rebuilds transparently from the persisted `documents.json` / `chunks.json` source of truth — no data loss, no manual migration.

#### 7. Animated 2D/3D knowledge graph with adaptive labels

- The 2D RAG graph gained node expand / collapse / scale animation: focusing a node now eases the layout morph (newly revealed neighbors expand outward from the clicked node) instead of switching instantly.
- The same expand/collapse + scale animation was ported to the 3D (Three.js) view, which renders on demand and drives a continuous animation frame until the morph settles.
- The 3D view gained labels for the first time, formatted to match the 2D labels exactly (same font, truncation, and dark-on-light styling). Labels keep a constant on-screen height regardless of depth.
- 3D labels are **density-culled in screen space every frame**: each label anchor is projected to screen pixels, off-screen and behind-camera labels are hidden, and remaining labels are greedily placed by importance (selected > hovered > hub > community > score) so a label shows only if its screen box does not overlap an already-placed, more-important one. Dense regions show only the important labels, and the visible set recomputes live as the camera orbits and zooms.
- Both the knowledge-RAG and code-RAG admin pages get all of this automatically (the code-RAG page is generated from the knowledge-RAG page with only endpoint/string swaps).

#### 8. Real MCP (Model Context Protocol) client

- Added a genuine stdio JSON-RPC 2.0 MCP driver (`MCPServerProcess`, `MCPManager`): it spawns each configured server as a child process and speaks the `initialize → notifications/initialized → tools/list → tools/call` handshake over stdin/stdout, with id-correlated pending futures fed by a per-process reader thread.
- Config is read from `LLM.config.json` in both the Claude/Codex dialect (`mcpServers` / `mcp_servers` with `{command, args, env}`) and the OpenCode dialect (`mcp` with `{type:"local", command:[argv], environment:{}}`); remote/sse/http transports are recorded but skipped with a notice (stdio only).
- MCP tools appear as `mcp__<server>__<tool>` and behave exactly like built-in tools across every mode and role (single-agent, manager, explorer, developer, reviewer, plan-mode), bypassing the per-role allowlist and routed ahead of any builtin so they cannot be shadowed.
- MCP is mounted as a **global, app-level service** on `--port + 4` (e.g. 8084 at the default 8080), independent of the IDE UI, with health monitoring, auto-restart of crashed servers, and hot-reload when the on-disk config changes. The service is reachable over a small HTTP surface (`/mcp/health`, `/mcp/tools`, `/mcp/status`, `/mcp/reload`, `/mcp/restart`, `/mcp/call`).
- The `mcp-builder` skill was rewritten to teach the real wire protocol and both config dialects, and is now released as inline source rather than from the embedded bundle.

#### 9. Port scheme made consistent

- Every auxiliary service now follows `--port` incrementally: agent = P, skills = P+1, rag = P+2, code = P+3, mcp = P+4, ide = P+5. The IDE moved off its old fixed port (which collided with mcp at the default 8080 and silently disabled the MCP service), and both the IDE and MCP conflict checks now count only services that actually started, so a disabled service can never block another from binding.

#### 10. Long-term user memory: uniform yet personalized

- The per-turn hot path (`_user_profile_capsule_prompt_block`) is now byte-identical across the `weak` and `on` modes (same injection budget), empty when `off`, and injects at most once per user message. Memory mode governs how rich the capsule is at build time, never how heavy each turn is — so performance is uniform across off / weak / on.
- Personalization is genuinely model-driven, not a hardcoded keyword/regex gate. In `on` mode a best-effort post-session distillation reads the recent conversation and proposes durable preferences as structured items (confidence ranked above the regex capture but never treated as certain). This runs off the hot path in the existing background session-finished step, so it adds no per-turn cost.
- The capsule's closing instruction is the only relevance gate — the model decides when a remembered preference applies, and explicit current instructions, manual level, manual plan, and explicit tool choices always override it.

#### 11. Multi-agent todo numbering unified

- Multi-agent worker todos are now a strict extension of the single-agent standard: one renumbering authority assigns sequential `N.M` numbers by display position (not by author), a single-seed invariant prevents two paths from both creating a step's subtasks, and a read-before-write canonical echo shows the reconciled list back in the tool result so workers reuse existing numbers instead of restating work as free text.

#### 12. Chat-page preview: open HTML in a real browser

- The chat-page webpage preview gained **Copy Link** and **Open in Browser** buttons. Because the in-pane iframe is cramped and distorts rendered pages, these open the identical content full-window in the default browser. The buttons are shown for HTML previews only — other file kinds (code, images, text) preview fine in-pane and keep just the download button.

#### 13. Source splitter updated

- `split_coder.py` now classifies every top-level symbol: a new `mcp/` package (`mcp/driver.py`) houses the MCP driver classes, helpers, and constants, and the display / JSON / reasoning helpers were routed to their natural utility modules. The split self-check passes with zero unclassified symbols.

### 2026-06-22 Summary

Retrieval is the theme: BM25 plus symbol-exact boosting and structure-preserving chunking make lexical-only recall reliable, cross-lingual querying works without an embedding model, books ingest safely, and the agent can remember good references on its own. Around that, a real MCP client makes external tools first-class everywhere, long-term memory became uniform in cost yet personalized in substance, and the knowledge graph is now fully animated with adaptive, density-culled labels in both 2D and 3D.

---

## 中文

### 标题：真正能召回的纯词法 RAG，加上真实 MCP 与个性化长期记忆

#### 1. RAG 检索改为 BM25 + 符号精确加权（纯词法）

- `TFGraphIDFIndex` / `CodeGraphIndex` 的词法核心从 TF-IDF **余弦**（会惩罚长文本、饱和特性差）改为 **BM25**（`RAG_BM25_K1=1.5`、`RAG_BM25_B=0.6`）。倒排表现在存储原始词频，长度归一化交给 BM25 的分母处理。
- 分数归一化采用**与候选池无关的饱和函数** `raw/(raw+RAG_BM25_SATURATION=4.0)`，刻意**不用** min-max。min-max 会把全弱候选池里的最佳项强行拉到 1.0，破坏「无证据 / 最低综合分」阈值；饱和函数保留绝对相关性，弱池仍判为弱。
- 新增**符号精确加权**：当查询词与某个分块的符号完全相等时给予强力、与 idf 无关的加权（`0.5·(0.85+0.15·rarity)`）；部分匹配则衰减。精确标识符查询是高精度意图，现在能稳定召回定义所在的分块。
- 最终分数（无稠密路径）：`lexical × 0.80 + graph_bonus + symbol_boost`，知识 RAG 与代码 RAG 完全一致。

#### 2. 保留结构的切分

- Python 代码切分器现在**递归（深度 ≤ 4）**进入嵌套函数、闭包、被装饰的辅助函数和内部类，使用 `outer.inner`、`Class.method` 这样的层级名称。每个分块都会持久化 `symbol` / `symbol_kind`（此前被丢弃），符号加权才能看到它们。
- 新增边界安全切分（`_rag_boundary_split`）：超长块的每个切点都回退到最近的段落 / 句子 / 换行 / 空白边界，并按边界对齐重叠，取代旧的「字符中间硬切」。

#### 3. 跨语言知识检索 —— 无需嵌入模型

- 用中文查询命中英文内容（反之亦然），全程基于普通 BM25。两层协同：一张精心整理的同义词表（约 4000 组中/英/缩写）在索引期与查询期都做扩展；以及针对任意 / 词表外词汇的查询期翻译桥 `_augment_query_cross_lingual`。
- 翻译桥检测单一文种的查询（中日韩与拉丁互斥），用会话模型尽力翻译，并把译文追加进去，使一条双语查询串在一次处理中走完既有分词器与 BM25。结果按归一化查询缓存，按长度门控，跳过本已双语或翻译回声的情形。**仅作用于知识 RAG**——代码检索保持字面。可按请求用 `cross_lingual=false` 关闭。

#### 4. `rag_remember` —— 智能体自我入库工具

- 智能体可以把一份好的参考资料或提炼出的结论直接写入知识库：`rag_remember(text, title?, tags?, category?, source?)`。它复用与管理端文本导入相同的去重 / 导入路径（sha256 去重、无额外 LLM 调用），并带溯源头信息。
- 因为它只写知识库、绝不写用户文件，所以与 `write_to_blackboard` 一样，对 explorer / reviewer 角色和 plan 模式调研都开放。

#### 5. 书籍级导入，且安全

- `RAG_MAX_CHUNKS_PER_DOC` 从 500 提升到 **20000**，并用统一的 `RAG_MAX_DOCUMENT_CHARS` 上限（默认 12M，环境变量 `AGENT_RAG_MAX_DOCUMENT_CHARS`，限定 150k–40M）取代散落在 PDF / docx / csv / pptx / xls 解析与上传重读路径中的各处截断。
- 安全性是结构性的：解析在独立子进程中运行，带硬超时与 terminate/kill，因此超大或缓慢的解析无法卡死应用；分块上限也能约束极端的数百万字符输入。`pdftotext` 子进程超时已与同一解析超时预算对齐。

#### 6. 带版本的索引快照

- 快照带 `bm25-v1` 格式标记以及新的 `chunk_lengths` / `avg_chunk_len` 字段。格式不匹配时 `restore()` 拒绝恢复，索引会从持久化的 `documents.json` / `chunks.json` 真源透明重建——无数据丢失、无需手工迁移。

#### 7. 带动画的 2D/3D 知识图谱与自适应标签

- 2D RAG 图谱新增节点展开 / 收起 / 缩放动画：聚焦某节点时布局会平滑过渡（新出现的邻居从被点击节点向外展开），不再瞬间切换。
- 同样的展开/收起 + 缩放动画移植到了 3D（Three.js）视图；该视图按需渲染，会驱动一段连续动画帧直到过渡收敛。
- 3D 视图首次加入标签，格式与 2D 完全一致（相同字体、截断与深色字浅底样式）。无论深度如何，标签都保持恒定的屏幕高度。
- 3D 标签**每帧在屏幕空间做密度剔除**：把每个标签锚点投影到屏幕像素，隐藏屏外与相机背面的标签，其余按重要度贪心摆放（选中 > 悬停 > 枢纽 > 社区 > 分数）——只有当一个标签的屏幕框不与已摆放的更重要标签重叠时才显示。稠密区域只显示重要标签，可见集合会随相机环绕与缩放实时重算。
- 知识 RAG 与代码 RAG 管理页都自动获得以上能力（代码 RAG 页由知识 RAG 页仅替换端点/文案生成）。

#### 8. 真实的 MCP（模型上下文协议）客户端

- 新增真正的 stdio JSON-RPC 2.0 MCP 驱动（`MCPServerProcess`、`MCPManager`）：把每个配置的服务器作为子进程拉起，通过 stdin/stdout 走 `initialize → notifications/initialized → tools/list → tools/call` 握手，由每进程一个读取线程喂入 id 关联的待决 future。
- 配置从 `LLM.config.json` 读取，兼容 Claude/Codex 方言（`mcpServers` / `mcp_servers`，`{command, args, env}`）与 OpenCode 方言（`mcp`，`{type:"local", command:[argv], environment:{}}`）；remote/sse/http 传输会记录但带提示跳过（仅 stdio）。
- MCP 工具以 `mcp__<server>__<tool>` 形式出现，在所有模式与角色（单智能体、manager、explorer、developer、reviewer、plan 模式）下与内置工具行为完全一致，绕过按角色的白名单，并排在所有内置工具之前路由，因此不会被遮蔽。
- MCP 作为**全局的应用级服务**挂载在 `--port + 4`（默认 8080 下即 8084），与 IDE UI 无关，带健康监控、崩溃服务器自动重启、磁盘配置变更热重载。该服务通过一组小型 HTTP 接口可达（`/mcp/health`、`/mcp/tools`、`/mcp/status`、`/mcp/reload`、`/mcp/restart`、`/mcp/call`）。
- `mcp-builder` 技能已重写，讲解真实的线缆协议与两种配置方言，并改为内联源码发布，不再来自嵌入包。

#### 9. 端口方案统一

- 所有辅助服务现在都随 `--port` 递增：agent = P、skills = P+1、rag = P+2、code = P+3、mcp = P+4、ide = P+5。IDE 从旧的固定端口（在默认 8080 下与 mcp 冲突并静默禁用了 MCP 服务）迁出；IDE 与 MCP 的冲突检查现在只统计真正启动的服务，因此被禁用的服务永远不会阻塞其它服务绑定。

#### 10. 长期用户记忆：均一而个性化

- 每轮的热路径（`_user_profile_capsule_prompt_block`）在 `weak` 与 `on` 模式下逐字节相同（相同注入预算），`off` 时为空，且每条用户消息最多注入一次。记忆模式只决定胶囊在构建期的丰富度，绝不决定每轮的开销——因此 off / weak / on 的性能是均一的。
- 个性化是真正由模型驱动的，而非硬编码的关键词/正则门控。在 `on` 模式下，一次尽力而为的会话后蒸馏读取近期对话，把持久偏好提炼为结构化条目（置信度排在正则捕获之上，但绝不视为确定）。它在既有的后台「会话结束」步骤中运行，处于热路径之外，因此不增加每轮成本。
- 胶囊的收尾指令是唯一的相关性门控——由模型判断某条记忆偏好何时适用；显式的当前指令、手动等级、手动计划与显式工具选择始终覆盖它。

#### 11. 多智能体待办编号统一

- 多智能体的 worker 待办现在是单智能体标准的严格扩展：单一编号权威按显示位置（而非作者）分配连续的 `N.M` 编号；单次播种不变式防止两条路径同时创建某步的子任务；写前读的规范回显会把对齐后的清单回写到工具结果里，使 worker 复用既有编号，而不是用自由文本重述工作。

#### 12. 对话页预览：用真实浏览器打开 HTML

- 对话页的网页预览新增**复制链接**与**浏览器打开**两个按钮。由于内嵌 iframe 空间局促、会让渲染页面变形，这两个按钮会在默认浏览器中以整窗口打开相同内容。这两个按钮仅对 HTML 预览显示——其它文件类型（代码、图片、文本）在窗格内预览正常，保留下载按钮即可。

#### 13. 源码拆分器更新

- `split_coder.py` 现在能为每个顶层符号分类：新增 `mcp/` 包（`mcp/driver.py`）容纳 MCP 驱动的类、辅助函数与常量，display / JSON / reasoning 辅助函数也归入各自天然的工具模块。拆分自检通过，零未分类符号。

### 2026-06-22 更新摘要

主题是检索：BM25 加符号精确加权、再加上保留结构的切分，让纯词法召回变得可靠；跨语言查询无需嵌入模型即可工作；书籍可安全导入；智能体能自行记住好的参考。围绕这些，真实的 MCP 客户端让外部工具在各处都成为一等公民，长期记忆做到开销均一而内容个性化，知识图谱在 2D 与 3D 中都实现了带自适应密度剔除标签的完整动画。

---

## 日本語

### 見出し：本当に再現できる語彙のみ RAG、そして本物の MCP と個別化された長期記憶

#### 1. RAG 検索を BM25 + シンボル完全一致ブーストへ（語彙のみ）

- `TFGraphIDFIndex` / `CodeGraphIndex` の語彙コアを、TF-IDF **コサイン**（長文を不利にし飽和特性が悪い）から **BM25**（`RAG_BM25_K1=1.5`、`RAG_BM25_B=0.6`）に変更。転置リストは生の出現頻度を保持し、長さ正規化は BM25 の分母が担う。
- スコア正規化は**候補プールに依存しない飽和**関数 `raw/(raw+RAG_BM25_SATURATION=4.0)` を採用し、min-max は意図的に**使わない**。min-max は全弱プールでも最良候補を 1.0 に押し上げ「証拠なし / 最低統合スコア」しきい値を壊すが、飽和は絶対的な関連度を保つため弱いプールは弱いままになる。
- **シンボル完全一致ブースト**を追加：クエリ語がチャンクのシンボルと完全一致すると idf 非依存の強いブースト（`0.5·(0.85+0.15·rarity)`）を与え、部分一致は減衰させる。完全な識別子クエリは高精度な意図なので、定義チャンクを安定して再現できる。
- 最終スコア（密ベクトル経路なし）：`lexical × 0.80 + graph_bonus + symbol_boost`。ナレッジ RAG とコード RAG で完全に同一。

#### 2. 構造を保つチャンク化

- Python コードチャンカーが、ネストした関数・クロージャ・デコレートされた補助関数・内部クラスへ**再帰（深さ ≤ 4）**し、`outer.inner`・`Class.method` のような階層名を付ける。各チャンクは `symbol` / `symbol_kind` を保持し（以前は破棄されていた）、シンボルブーストから参照できる。
- 新しい境界安全分割（`_rag_boundary_split`）が、過大ブロックの各切断点を最寄りの段落 / 文 / 改行 / 空白の境界へ戻し、境界に揃えたオーバーラップを付ける。従来の文字途中での切断を置き換えた。

#### 3. 言語横断のナレッジ検索 —— 埋め込みモデル不要

- 中国語で検索して英語コンテンツに当てる（逆も）。すべて通常の BM25 上で動く。二層が協調：整備した類義語表（中/英/略語 約 4000 グループ）をインデックス時とクエリ時の両方で拡張し、任意 / 語彙外の語にはクエリ時翻訳ブリッジ `_augment_query_cross_lingual` を使う。
- ブリッジは単一文字種のクエリ（CJK と Latin の排他）を検出し、セッションモデルでベストエフォート翻訳して追記。これで一本のバイリンガルクエリ文字列が既存のトークナイザと BM25 を一度で通る。正規化クエリ単位でキャッシュし、長さでゲートし、既にバイリンガル / 翻訳エコーはスキップ。**対象はナレッジ RAG のみ**——コード検索はリテラルのまま。リクエスト単位で `cross_lingual=false` により無効化可能。

#### 4. `rag_remember` —— エージェント自己取り込みツール

- エージェントが良い参考資料や蒸留した知見を直接ナレッジライブラリへ書き込める：`rag_remember(text, title?, tags?, category?, source?)`。管理画面のテキスト取り込みと同じ重複排除 / 取り込み経路（sha256 重複排除・追加の LLM 呼び出しなし）を再利用し、来歴ヘッダを付ける。
- ナレッジライブラリにのみ書き込み、ユーザーファイルには決して書かないため、`write_to_blackboard` と同様に explorer / reviewer ロールおよび plan モードの調査でも許可される。

#### 5. 書籍級の取り込みを安全に

- `RAG_MAX_CHUNKS_PER_DOC` を 500 から **20000** に引き上げ、統一の `RAG_MAX_DOCUMENT_CHARS` 上限（既定 12M、環境変数 `AGENT_RAG_MAX_DOCUMENT_CHARS`、150k–40M にクランプ）が、PDF / docx / csv / pptx / xls 解析やアップロード再読込に散在していた切り捨てを置き換えた。
- 安全性は構造的：解析は生成サブプロセスでハードタイムアウト + terminate/kill 付きで実行されるため、巨大・低速な解析でもアプリを固められず、チャンク上限は数百万文字の病的入力さえ抑える。`pdftotext` サブプロセスのタイムアウトも同じ解析タイムアウト予算に揃えた。

#### 6. バージョン付きインデックススナップショット

- スナップショットは `bm25-v1` 形式タグと新フィールド `chunk_lengths` / `avg_chunk_len` を持つ。形式不一致時には `restore()` が復元を拒否し、永続化された `documents.json` / `chunks.json` という真の出所からインデックスを透過的に再構築する——データ損失も手動移行もなし。

#### 7. アニメーション付き 2D/3D ナレッジグラフと適応ラベル

- 2D RAG グラフにノードの展開 / 折りたたみ / 拡縮アニメーションを追加：ノードにフォーカスするとレイアウトが滑らかに変形し（新たに現れた隣接ノードがクリックしたノードから外へ展開）、瞬時切り替えではなくなった。
- 同じ展開/折りたたみ + 拡縮アニメーションを 3D（Three.js）ビューへ移植。オンデマンド描画のため、変形が収束するまで連続フレームを駆動する。
- 3D ビューに初めてラベルを追加し、2D と完全に同じ書式（同じフォント・切り詰め・濃色文字/淡色背景）にした。奥行きに関わらずラベルは一定の画面上高さを保つ。
- 3D ラベルは**毎フレーム、画面空間で密度カリング**される：各アンカーを画面ピクセルへ投影し、画面外とカメラ背面のラベルを隠し、残りを重要度で貪欲配置（選択 > ホバー > ハブ > コミュニティ > スコア）——その画面ボックスが既配置のより重要なラベルと重ならない場合のみ表示。密集領域では重要ラベルだけが出て、可視集合はカメラの旋回とズームに応じてリアルタイムに再計算される。
- ナレッジ RAG とコード RAG の管理ページは、これらすべてを自動的に得る（コード RAG ページはナレッジ RAG ページからエンドポイント/文言の置換のみで生成）。

#### 8. 本物の MCP（Model Context Protocol）クライアント

- 本物の stdio JSON-RPC 2.0 MCP ドライバ（`MCPServerProcess`、`MCPManager`）を追加：設定された各サーバーを子プロセスとして起動し、stdin/stdout 越しに `initialize → notifications/initialized → tools/list → tools/call` のハンドシェイクを話す。id 対応の保留 future はプロセスごとの読み取りスレッドが供給する。
- 設定は `LLM.config.json` から読み、Claude/Codex 方言（`mcpServers` / `mcp_servers`、`{command, args, env}`）と OpenCode 方言（`mcp`、`{type:"local", command:[argv], environment:{}}`）の両方に対応。remote/sse/http トランスポートは記録するが通知付きでスキップ（stdio のみ）。
- MCP ツールは `mcp__<server>__<tool>` として現れ、あらゆるモードとロール（単一エージェント、manager、explorer、developer、reviewer、plan モード）で組み込みツールと完全に同じ挙動を取る。ロール別許可リストを迂回し、いかなる組み込みよりも先にルーティングされるため隠れることがない。
- MCP は **グローバルなアプリレベルサービス**として `--port + 4`（既定 8080 なら 8084）にマウントされ、IDE UI とは独立で、ヘルス監視・クラッシュサーバーの自動再起動・ディスク設定変更時のホットリロードを備える。小さな HTTP 面（`/mcp/health`、`/mcp/tools`、`/mcp/status`、`/mcp/reload`、`/mcp/restart`、`/mcp/call`）で到達できる。
- `mcp-builder` スキルは実際のワイヤープロトコルと両方の設定方言を教えるよう書き直し、埋め込みバンドルからではなくインラインソースとして提供するようにした。

#### 9. ポート方式の一貫化

- 補助サービスはすべて `--port` に従って増分する：agent = P、skills = P+1、rag = P+2、code = P+3、mcp = P+4、ide = P+5。IDE は旧来の固定ポート（既定 8080 で mcp と衝突し MCP サービスを黙って無効化していた）から移動し、IDE と MCP の衝突チェックは実際に起動したサービスのみを数えるようになったため、無効なサービスが他のバインドを阻むことはない。

#### 10. 長期ユーザー記憶：均一でありながら個別化

- 毎ターンのホットパス（`_user_profile_capsule_prompt_block`）は `weak` と `on` モードでバイト単位まで同一（同じ注入バジェット）、`off` では空、ユーザーメッセージごとに最大一度だけ注入する。記憶モードはカプセルの構築時の豊かさを左右するだけで、各ターンの重さは左右しない——よって off / weak / on で性能は均一。
- 個別化はハードコードのキーワード/正規表現ゲートではなく、真にモデル駆動。`on` モードではベストエフォートのセッション後蒸留が直近の会話を読み、持続的な好みを構造化項目として提案する（信頼度は正規表現キャプチャより上位だが確定とは扱わない）。既存のバックグラウンド「セッション終了」ステップで実行され、ホットパス外なのでターン毎コストを増やさない。
- カプセルの結びの指示が唯一の関連性ゲート——記憶した好みがいつ適用されるかはモデルが判断し、明示的な現在の指示・手動レベル・手動プラン・明示的なツール選択が常に優先する。

#### 11. マルチエージェントの ToDo 採番を統一

- マルチエージェントの worker ToDo は単一エージェント標準の厳密な拡張になった：単一の採番権威が表示位置（作者ではなく）で連番 `N.M` を割り当て、単一シード不変条件が二経路による同一ステップのサブタスク二重生成を防ぎ、書き込み前読み取りの正準エコーが調整済みリストをツール結果へ書き戻すので、worker は作業を自由文で言い直さず既存番号を再利用する。

#### 12. チャットページのプレビュー：HTML を本物のブラウザで開く

- チャットページのウェブプレビューに **リンクをコピー** と **ブラウザで開く** ボタンを追加。ペイン内 iframe は窮屈でレンダリングを歪めるため、これらは同一コンテンツを既定ブラウザの全ウィンドウで開く。ボタンは HTML プレビューでのみ表示——他のファイル種別（コード・画像・テキスト）はペイン内で問題なくプレビューでき、ダウンロードボタンだけを残す。

#### 13. ソース分割ツールを更新

- `split_coder.py` はすべてのトップレベルシンボルを分類するようになった：新しい `mcp/` パッケージ（`mcp/driver.py`）が MCP ドライバのクラス・補助関数・定数を収め、display / JSON / reasoning 補助関数はそれぞれ自然なユーティリティモジュールへ振り分けた。分割のセルフチェックは未分類シンボル 0 で通過する。

### 2026-06-22 要約

テーマは検索：BM25 とシンボル完全一致ブースト、そして構造を保つチャンク化により語彙のみの再現が信頼でき、言語横断クエリは埋め込みモデルなしで動き、書籍も安全に取り込め、エージェントは良い参考を自ら記憶できる。その周囲で、本物の MCP クライアントが外部ツールをどこでも一級市民にし、長期記憶はコスト均一でありながら中身は個別化され、ナレッジグラフは 2D・3D の両方で適応的・密度カリング付きラベルとともに完全にアニメーション化された。
