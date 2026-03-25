# CHANGELOG 2026-03-25

## 🔥 Skills 生态系统兼容 & 双库 RAG 架构 & 多因素上下文压缩

本次更新覆盖 4 大主题、18 个修改点：Skills 生态兼容性全面扩展（兼容 5 大生态系统）、双库 RAG 知识架构落地（Code RAG + Data RAG）、两大内置 Skills 重写（research-orchestrator-pro / scientific-reasoning-lab）、多因素优先级上下文压缩升级，以及 5 项关键修复。

---

## English

### Headline: Universal Skills Ecosystem + Dual RAG Architecture + Core Reliability Fixes

#### 1. Universal Skills Ecosystem Compatibility (Critical)

**5-ecosystem compatibility**: Clouds Coder now loads and executes skills from any of the five major skill ecosystems without any per-provider adapters:
- `awesome-claude-skills`
- `Minimax-skills`
- `skills-main`
- `kimi-agent-internals`
- `academic-pptx-skill-main`

**Root cause of previous failures**: The Execution Guide injection (lines 11094–11131) forced `read_file` calls on virtual skill paths that don't exist in the filesystem, causing the model to loop indefinitely trying to read non-existent files instead of following the skill's SKILL.md instructions.

**Fixes and simplifications**:
- **Removed Execution Guide injection** entirely — the model now follows SKILL.md instructions directly without interference
- **Removed Chain Tracking system** (7 methods including `_skill_chain_completion_blocker`, `_record_skill_chain_entry`) — eliminated over-engineered interception that silently blocked skill execution
- **Simplified `_broadcast_loaded_skill` blackboard writes** from 16 fields → 6 fields (name, path, description, loaded_at, trigger_context, source)
- **Simplified `_loaded_skills_prompt_hint`** from ~350 tokens → ~120 tokens: compact in-context hint that tells the model which skills are loaded without cluttering its context budget
- **LLM-driven autonomous discovery**: discovery prompt simplified (max 3 skills per scan, 30 catalog entries, `max_tokens=120`) so the model makes its own judgment about what skill fits the task type — no keyword-based forced triggers
- **Multi-skill loading with conflict detection**: multiple skills can be loaded simultaneously; loading a skill that directly conflicts with an already-loaded skill is blocked
- **Sync-mode Manager TodoWrite capability**: Manager in sync mode now has access to `TodoWrite` for coordinating plan steps with skill execution

**New: `_preload_skills_from_plan_steps`** — scans plan step text for skill name mentions and proactively preloads them before execution begins, reducing skill-load latency mid-execution.

**Shell path auto-quoting** (`_rewrite_shell_virtual_paths`): paths containing spaces are now automatically wrapped in double quotes before shell dispatch, fixing execution failures on macOS paths with spaces.

**Plan expansion**:
- Plan steps limit raised from 10 → 20 steps
- Per-step character limit raised from 400 → 600 characters
- Anti-hallucination constraint added to plan synthesis: "Only reference scripts and files that ACTUALLY EXIST in the session filesystem"

#### 2. Dual RAG Architecture — Code RAG + Data RAG (High)

**Architecture**: Two independent ingestion and retrieval engines, both built on TF_G_IDF_RAG:
- `RAGIngestionService` (Data RAG): handles documents, PDFs, structured data files — general knowledge base
- `CodeIngestionService` (Code RAG): handles source code files with code-aware tokenization — code-specific knowledge base

**Unified retrieval**: `query_knowledge_library(query, top_k)` searches both libraries in parallel and returns a merged ranked result, so the model always queries one interface regardless of content type.

**RAG guide injection**: Both `research-orchestrator-pro` and `scientific-reasoning-lab` now include a full retrieval guide documenting the `query_knowledge_library` interface, parameter meanings, response format, and best-practice query patterns. The model can leverage the knowledge base directly from within a loaded skill.

#### 3. Built-in Skills Overhaul: research-orchestrator-pro & scientific-reasoning-lab (High)

**`research-orchestrator-pro` rewritten as cooperative decision hub**:
- Previous version: conflicted with output skills (e.g., ppt) by trying to run its own analysis workflow in parallel, causing the model to synthesize hallucinated scripts
- New design: acts as an analysis decision hub that focuses exclusively on evidence synthesis and task structuring; when loaded alongside an output skill (e.g., ppt, report-writer), it defers all output formatting to that skill
- Includes full RAG retrieval guide for background knowledge augmentation
- Anti-hallucination posture: "Do NOT generate file/script names that don't exist"

**`scientific-reasoning-lab` rewritten as 5-step self-iterating reasoning engine**:
- Phase 1: Problem decomposition — defines variables, constraints, assumptions
- Phase 2: Formal reasoning chain — step-by-step derivation with mathematical rigor (now embedded as sub-engine of research-orchestrator-pro Phase 2)
- Phase 3: Self-verification — checks logical consistency, unit/dimension coherence, numerical ranges
- Phase 4: Critical evaluation — identifies gaps, uncertainty bounds, and edge cases
- Phase 5: Integration — synthesizes findings into structured conclusions with explicit confidence levels
- Includes full RAG retrieval guide for referencing prior knowledge during reasoning

#### 4. Multi-Factor Priority Context Compression (High)

**Problem**: Previous `_auto_compact` discarded messages chronologically (oldest first), which could drop task-critical information (current plan step, recent errors, active skills) while retaining low-value content from early in a session.

**New `_classify_message_priority` — 10-factor scoring (0–10)**:
- Recency: 0–3 points (newest messages score highest)
- Role weight: system=3, user=2, assistant=2, tool=1
- Task progress markers (`TodoWrite`, `plan_step`, `finish_task`): +2
- Error / critical information (`Error:`, exception traces): +2
- Current goal relevance: +1
- Skill-related content (`<loaded-skill>`, `skill loaded`): +1
- `compact-resume` note: forced to 10 (always preserved)

**New `_priority_compress_messages` — priority-based three-tier compression**:
- High priority (score ≥ 7): kept intact
- Medium priority (score 4–6): content truncated to 500-character summary
- Low priority (score 0–3): collapsed to a one-liner or dropped if over token budget
- Output is re-sorted by original message index to maintain conversation order

**`_build_state_handoff` enhanced** with four new structured fields:
- `PLAN_PROGRESS`: completed/total plan steps
- `CURRENT_STEP`: text of the active plan step
- `ACTIVE_SKILLS`: list of currently loaded skills
- `RECENT_TOOLS`: summary of last 5 tool calls

**`_auto_compact` integration**: priority compression runs first; original chronological `pop(0)` is preserved as a safety fallback if priority compression doesn't reduce tokens far enough.

#### 5. Anti-stall Mechanism Optimization (Medium)

**Problem**: `_manager_apply_anti_stall` triggered "CHANGE YOUR APPROACH" after only 2 consecutive delegations to the same target, interrupting agents that were legitimately making incremental progress across multiple turns.

**Changes**:
- Threshold raised from 2 → 3 consecutive same-target delegations before triggering
- Instruction softened from the blunt "CHANGE YOUR APPROACH" to a collaborative guidance message:
  > "You have been working on this for multiple rounds without visible progress. Consider: 1) Use ask_colleague to request help from another agent. 2) Try a completely different tool or approach. 3) If the subtask is complete, call finish_current_task with what you have so far."

#### 6. Critical Bug Fixes (High)

**Fix 1 — `CodeIngestionService._flush_lock` (AttributeError)**
- Symptom: `AttributeError: 'CodeIngestionService' object has no attribute '_flush_lock'` when uploading code files to the Code Library
- Root cause: `CodeIngestionService.__init__` completely overrides parent `RAGIngestionService.__init__` without calling `super().__init__()`, so `_flush_lock = threading.Lock()` (initialized in the parent) was never created
- Fix: added `self._flush_lock = threading.Lock()` at the end of `CodeIngestionService.__init__`

**Fix 2 — Frontend `setTaskLevel()` complexity selector resets**
- Symptom: selecting a task complexity level (e.g., L4) works momentarily then reverts to "Auto" after the next message
- Root cause: `setTaskLevel()` called `updateLevelBtn(lvl)` to update the UI button but never called `scheduleSnapshot()`, so the next SSE snapshot refresh overwrote the button state with stale server data
- Fix: added `scheduleSnapshot({forceFull:false, delayMs:80, allowWhenFrozen:true})` after `updateLevelBtn(lvl)`, matching the pattern already used by `applyModel()`

**Fix 3 — `_sync_todos_from_blackboard` drops worker TodoWrite items**
- Symptom: in sync mode, items written by `TodoWrite` from developer/explorer/reviewer agents only persist for one round, then disappear on the next blackboard sync
- Root cause: items with `owner ∈ {developer, explorer, reviewer}` were being filtered out from `non_system_rows` (as non-system items) but were not included in `system_rows` either — so they were silently lost on every sync cycle
- Fix: worker items are now collected into a separate `worker_rows` list and merged with priority (placed between system rows and non-system rows), protected from sync overwrites

**Fix 4 — Anti-stall threshold and instruction (see item 5 above)**

**Fix 5 — Multi-factor context compression (see item 4 above)**

### 2026-03-25 Summary
- Skills ecosystem now compatible with all 5 major skill providers; Execution Guide and Chain Tracking removed to let the model follow skills naturally
- Dual RAG architecture (Code RAG + Data RAG) with unified `query_knowledge_library` retrieval interface and injected retrieval guides in built-in skills
- `research-orchestrator-pro` redesigned as a non-interfering analysis hub; `scientific-reasoning-lab` rebuilt as a 5-phase self-iterating reasoning engine
- Context compression upgraded from chronological-only to 10-factor priority scoring, preserving task-critical information over session noise
- Anti-stall threshold raised (2→3) and instruction softened to collaborative guidance
- Five critical fixes: `_flush_lock` AttributeError, task-level selector UI revert, worker todo preservation, and the two above

---

## 中文

### 标题：Skills 生态系统兼容 & 双库 RAG 架构 & 内核可靠性修复

#### 1. Skills 生态系统全面兼容（重要）

**5 大生态系统兼容**：Clouds Coder 现在可原生加载并执行来自以下五大生态系统的 skills，无需任何 per-provider 适配器：
- `awesome-claude-skills`
- `Minimax-skills`
- `skills-main`
- `kimi-agent-internals`
- `academic-pptx-skill-main`

**此前失败的根因**：Execution Guide 注入（行 11094–11131）强制对虚拟 skill 路径发起 `read_file` 调用，但这些路径在文件系统中根本不存在，导致模型陷入循环，无法按 SKILL.md 指令正常执行。

**修复与简化**：
- **完全移除 Execution Guide 注入** — 模型现在直接遵循 SKILL.md 指令，不再受干扰
- **移除 Chain Tracking 系统**（7 个方法，包括 `_skill_chain_completion_blocker`、`_record_skill_chain_entry` 等）— 消除了过度工程化的链路拦截，曾静默阻断 skill 执行
- **简化 `_broadcast_loaded_skill` 黑板写入**：16 字段 → 6 字段（name/path/description/loaded_at/trigger_context/source）
- **简化 `_loaded_skills_prompt_hint`**：约 350 tokens → 约 120 tokens，在不浪费上下文预算的前提下向模型告知已加载的 skills
- **LLM 自主发现**：发现 prompt 精简（每次最多 3 个 skill，30 个目录条目，`max_tokens=120`），模型根据任务类型自主判断调用哪个 skill，而非关键词强触发
- **多 skill 加载 + 冲突检测**：允许同时加载多个 skills；加载与已加载 skill 直接冲突的 skill 时自动阻止
- **Sync 模式 Manager TodoWrite 能力**：Manager 现在可在 sync 模式下使用 `TodoWrite` 协调 plan steps 与 skill 执行

**新增 `_preload_skills_from_plan_steps`**：扫描 plan steps 文本中的 skill 名称，在执行开始前提前预加载，减少执行中途 skill 加载的延迟。

**Shell 路径自动引号**（`_rewrite_shell_virtual_paths`）：含空格的路径在 shell 分发前自动加双引号，修复 macOS 含空格路径的执行失败问题。

**Plan 扩展**：
- Plan steps 上限从 10 → 20 步
- 单步字符限制从 400 → 600 字符
- Plan 合成新增反幻觉约束："Only reference scripts and files that ACTUALLY EXIST in the session filesystem"

#### 2. 双库 RAG 架构 — Code RAG + Data RAG（高）

**架构**：两个独立的摄取与检索引擎，均基于 TF_G_IDF_RAG：
- `RAGIngestionService`（Data RAG）：处理文档、PDF、结构化数据文件 — 通用知识库
- `CodeIngestionService`（Code RAG）：处理源代码文件，使用代码感知分词 — 代码专用知识库

**统一检索**：`query_knowledge_library(query, top_k)` 并行检索两个库并返回合并排序的结果，模型使用单一接口检索任意内容类型。

**RAG 指南注入**：`research-orchestrator-pro` 和 `scientific-reasoning-lab` 均内置完整的 RAG 检索指南，记录 `query_knowledge_library` 接口说明、参数含义、响应格式和最佳实践查询模式。模型可在 skill 内直接利用知识库。

#### 3. 内置 Skills 重写：research-orchestrator-pro & scientific-reasoning-lab（高）

**`research-orchestrator-pro` 重写为协作型决策中枢**：
- 旧版问题：与输出型 skills（如 ppt）冲突，尝试并行运行自己的分析流程，导致模型合成幻想出的脚本
- 新设计：专注于证据综合与任务结构化的分析决策中枢；与输出型 skill 同时加载时，将所有输出格式化工作交给该 skill
- 内置完整 RAG 检索指南，用于补充背景知识
- 反幻觉姿态："Do NOT generate file/script names that don't exist"

**`scientific-reasoning-lab` 重写为 5 步自迭代推理引擎**：
- Phase 1：问题分解 — 定义变量、约束、假设
- Phase 2：形式化推理链 — 逐步推导，数学严谨性（嵌入为 research-orchestrator-pro Phase 2 的子引擎）
- Phase 3：自我验证 — 检查逻辑一致性、单位/量纲一致性、数值范围
- Phase 4：批判性评估 — 识别缺口、不确定性边界和边缘情况
- Phase 5：整合 — 将发现综合为带显式置信度的结构化结论
- 内置完整 RAG 检索指南，用于推理过程中参考已有知识

#### 4. 多因素优先级上下文压缩（高）

**问题**：旧版 `_auto_compact` 按时间顺序（最旧的先丢弃）裁剪消息，可能丢弃任务关键信息（当前 plan step、近期错误、活跃 skills），同时保留会话初期的低价值内容。

**新增 `_classify_message_priority` — 10 因素评分（0-10）**：
- 时间近因性：0–3 分（越新越高）
- 角色权重：system=3、user=2、assistant=2、tool=1
- 任务进度标记（`TodoWrite`、`plan_step`、`finish_task`）：+2
- 错误/关键信息（`Error:`、异常 traceback）：+2
- 当前目标相关性：+1
- Skill 相关内容（`<loaded-skill>`、`skill loaded`）：+1
- `compact-resume` 注释：强制设为 10（始终保留）

**新增 `_priority_compress_messages` — 优先级三级压缩**：
- 高优先级（分数 ≥ 7）：完整保留
- 中优先级（分数 4–6）：内容压缩至 500 字符摘要
- 低优先级（分数 0–3）：折叠为单行或在超出 token 预算时丢弃
- 输出按原始消息索引重新排序，保持对话顺序

**`_build_state_handoff` 增强**，新增四个结构化字段：
- `PLAN_PROGRESS`：已完成/总计 plan steps
- `CURRENT_STEP`：当前活跃 plan step 的文本
- `ACTIVE_SKILLS`：当前已加载的 skills 列表
- `RECENT_TOOLS`：最近 5 次工具调用摘要

**`_auto_compact` 整合**：优先级压缩优先执行；原有的时序 `pop(0)` 作为保底 fallback 保留。

#### 5. Anti-stall 机制优化（中）

**问题**：`_manager_apply_anti_stall` 在连续 2 次委派给相同 target 后就触发 "CHANGE YOUR APPROACH"，打断了正在合理分步推进的 agent。

**变更**：
- 阈值从 2 → 3 次连续相同 target 才触发
- 指令从强制性的 "CHANGE YOUR APPROACH" 改为协作性引导：
  > "You have been working on this for multiple rounds without visible progress. Consider: 1) Use ask_colleague to request help from another agent. 2) Try a completely different tool or approach. 3) If the subtask is complete, call finish_current_task with what you have so far."

#### 6. 关键 Bug 修复（高）

**修复 1 — `CodeIngestionService._flush_lock`（AttributeError）**
- 症状：向代码库上传代码文件时触发 `AttributeError: 'CodeIngestionService' object has no attribute '_flush_lock'`
- 根因：`CodeIngestionService.__init__` 完全重写了父类 `RAGIngestionService.__init__` 但未调用 `super().__init__()`，导致父类初始化的 `_flush_lock = threading.Lock()` 从未创建
- 修复：在 `CodeIngestionService.__init__` 末尾添加 `self._flush_lock = threading.Lock()`

**修复 2 — 前端 `setTaskLevel()` 复杂度选择器回弹**
- 症状：选择任务复杂度（如 L4）后，下一条消息发送后 UI 自动回弹到 "Auto"
- 根因：`setTaskLevel()` 调用 `updateLevelBtn(lvl)` 更新了 UI 按钮，但未调用 `scheduleSnapshot()`，导致下一次 SSE 快照刷新用服务端旧数据覆盖按钮状态
- 修复：在 `updateLevelBtn(lvl)` 后添加 `scheduleSnapshot({forceFull:false, delayMs:80, allowWhenFrozen:true})`，与 `applyModel()` 已有的模式保持一致

**修复 3 — `_sync_todos_from_blackboard` 丢失 Worker TodoWrite 条目**
- 症状：sync 模式下，developer/explorer/reviewer agent 通过 `TodoWrite` 写入的条目仅在当前轮次有效，下一次黑板同步后消失
- 根因：`owner ∈ {developer, explorer, reviewer}` 的条目在同步时被从 `non_system_rows` 中过滤出去（作为非系统条目），但又没有被加入 `system_rows`，导致每个同步周期都静默丢弃这些条目
- 修复：worker items 现在单独收集到 `worker_rows` 列表，合并时优先保留（位于 system rows 与 non-system rows 之间），不再被同步覆盖

**修复 4 — Anti-stall 阈值与指令（见第 5 项）**

**修复 5 — 多因素上下文压缩（见第 4 项）**

### 2026-03-25 修复总结
- Skills 生态系统现在兼容全部 5 大主流 skill 提供商；移除 Execution Guide 和 Chain Tracking，让模型自然遵循 skills
- 双库 RAG 架构（Code RAG + Data RAG）落地，统一检索接口 `query_knowledge_library`，RAG 检索指南注入到内置 skills
- `research-orchestrator-pro` 重设计为非干扰性分析中枢；`scientific-reasoning-lab` 重构为 5 阶段自迭代推理引擎
- 上下文压缩从纯时序裁剪升级为 10 因素优先级评分，优先保留任务关键信息
- Anti-stall 阈值提升（2→3）并软化为协作性引导
- 五项关键修复：`_flush_lock` AttributeError、任务级别选择器 UI 回弹、worker todo 保护，以及上述两项

---

## 日本語

### タイトル：Skills エコシステム互換 & デュアル RAG アーキテクチャ & コア信頼性修正

#### 1. Skills エコシステム全面対応（重大）

**5 エコシステム対応**：Clouds Coder は以下 5 つの主要 skills エコシステムから skills を読み込み、per-provider アダプターなしで実行可能：
- `awesome-claude-skills`
- `Minimax-skills`
- `skills-main`
- `kimi-agent-internals`
- `academic-pptx-skill-main`

**以前の失敗の根本原因**：Execution Guide インジェクション（行 11094–11131）がファイルシステムに存在しない仮想 skill パスに `read_file` を強制し、モデルが SKILL.md 指示に従う代わりに無限ループに陥っていた。

**修正と簡素化**：
- **Execution Guide インジェクションを完全削除** — モデルが干渉なしに SKILL.md 指示に直接従う
- **Chain Tracking システム削除**（7 メソッド：`_skill_chain_completion_blocker`、`_record_skill_chain_entry` 等） — skill 実行をサイレントにブロックしていた過剰エンジニアリングの排除
- **`_broadcast_loaded_skill` ブラックボード書き込み簡素化**：16 フィールド → 6 フィールド
- **`_loaded_skills_prompt_hint` 簡素化**：約 350 tokens → 約 120 tokens
- **LLM 自律発見**：発見 prompt を精简（最大 3 skills、30 カタログエントリ、`max_tokens=120`）、モデルがタスクタイプに応じて自律的に skill を判断
- **マルチ skill ロード + コンフリクト検出**：複数 skills の同時ロード可能；直接競合する skill のロードはブロック
- **Sync モード Manager の TodoWrite 能力**：Manager が sync モードで `TodoWrite` を使用可能

**新機能 `_preload_skills_from_plan_steps`**：plan step テキストの skill 名前を事前スキャンして先行プリロード。

**Shell パス自動クォート**（`_rewrite_shell_virtual_paths`）：スペースを含むパスを自動でダブルクォートで囲み、macOS のパス実行失敗を修正。

**Plan 拡張**：
- Plan steps 上限 10 → 20 ステップ
- 1 ステップ文字数 400 → 600 文字
- Plan 合成に反幻覚制約を追加

#### 2. デュアル RAG アーキテクチャ — Code RAG + Data RAG（高）

**アーキテクチャ**：TF_G_IDF_RAG 上に構築された 2 つの独立した取り込み・検索エンジン：
- `RAGIngestionService`（Data RAG）：ドキュメント、PDF、構造化データファイル — 汎用知識ベース
- `CodeIngestionService`（Code RAG）：コードファイル専用、コード認識トークナイザー

**統一検索**：`query_knowledge_library(query, top_k)` が両ライブラリを並列検索し、マージされたランク付き結果を返す。

**RAG ガイド注入**：`research-orchestrator-pro` と `scientific-reasoning-lab` 両方に、`query_knowledge_library` インターフェース、パラメータ、レスポンス形式、ベストプラクティスクエリパターンを説明する完全な RAG 検索ガイドを内蔵。

#### 3. 内蔵 Skills 全面リライト：research-orchestrator-pro & scientific-reasoning-lab（高）

**`research-orchestrator-pro` を協調型決定ハブとしてリライト**：
- 旧問題：出力型 skills（ppt 等）と競合し、自身の分析ワークフローを並行実行しようとして幻覚スクリプトを生成させていた
- 新設計：証拠統合とタスク構造化に特化した分析決定ハブ；出力型 skill と同時ロード時は出力フォーマットをその skill に委任
- 完全な RAG 検索ガイドを内蔵
- 反幻覚スタンス："Do NOT generate file/script names that don't exist"

**`scientific-reasoning-lab` を 5 ステップ自己反復推論エンジンとしてリライト**：
- Phase 1：問題分解 — 変数・制約・仮定の定義
- Phase 2：形式的推論チェーン — 数学的厳密性を持つステップバイステップの導出（research-orchestrator-pro Phase 2 のサブエンジンとして統合）
- Phase 3：自己検証 — 論理的一貫性、単位/次元整合性、数値範囲の確認
- Phase 4：批判的評価 — ギャップ、不確実性の境界、エッジケースの特定
- Phase 5：統合 — 明示的な信頼度レベルを持つ構造化された結論へ統合
- 完全な RAG 検索ガイドを内蔵

#### 4. 多因子優先度コンテキスト圧縮（高）

**問題**：以前の `_auto_compact` は時系列順（古いものから）でメッセージを削除し、重要なタスク情報（現在の plan step、最近のエラー、アクティブ skills）を失う可能性があった。

**新 `_classify_message_priority` — 10 因子スコアリング（0–10）**：
- 時間的近接性：0–3 点（最新メッセージが最高スコア）
- 役割の重み：system=3、user=2、assistant=2、tool=1
- タスク進捗マーカー（`TodoWrite`、`plan_step`、`finish_task`）：+2
- エラー/重要情報（`Error:`、例外トレース）：+2
- 現在の目標との関連性：+1
- Skill 関連コンテンツ：+1
- `compact-resume` ノート：強制的に 10（常に保持）

**新 `_priority_compress_messages` — 優先度ベース 3 段階圧縮**：
- 高優先度（スコア ≥ 7）：そのまま保持
- 中優先度（スコア 4–6）：500 文字サマリーに圧縮
- 低優先度（スコア 0–3）：1 行サマリーに折り畳むか削除

**`_build_state_handoff` 強化**：PLAN_PROGRESS、CURRENT_STEP、ACTIVE_SKILLS、RECENT_TOOLS フィールドを追加。

**`_auto_compact` 統合**：優先度圧縮を先行実行；元の時系列 `pop(0)` はセーフティフォールバックとして保持。

#### 5. Anti-stall メカニズム最適化（中）

**変更**：
- 閾値を 2 → 3 回連続同一ターゲット委任に引き上げ
- "CHANGE YOUR APPROACH" を協調的ガイダンスメッセージに軟化

#### 6. 重大バグ修正（高）

**修正 1 — `CodeIngestionService._flush_lock`（AttributeError）**
- 原因：`CodeIngestionService.__init__` が親クラス `RAGIngestionService.__init__` を完全に上書きし `super().__init__()` を呼ばないため、親で初期化される `_flush_lock` が存在しない
- 修正：`CodeIngestionService.__init__` の末尾に `self._flush_lock = threading.Lock()` を追加

**修正 2 — フロントエンド `setTaskLevel()` 複雑度セレクターリセット**
- 原因：`setTaskLevel()` が `updateLevelBtn(lvl)` を呼ぶが `scheduleSnapshot()` を呼ばないため、次の SSE スナップショット更新で UI が古いサーバーデータで上書きされる
- 修正：`updateLevelBtn(lvl)` の後に `scheduleSnapshot({forceFull:false, delayMs:80, allowWhenFrozen:true})` を追加

**修正 3 — `_sync_todos_from_blackboard` が Worker TodoWrite アイテムを消失**
- 原因：`owner ∈ {developer, explorer, reviewer}` のアイテムが `non_system_rows` からフィルタリングされるが `system_rows` にも追加されず、毎回のブラックボード同期でサイレントに消失
- 修正：worker items を独立した `worker_rows` リストに収集して優先的にマージ

**修正 4 — Anti-stall 閾値と指示（第 5 項参照）**

**修正 5 — 多因子コンテキスト圧縮（第 4 項参照）**

### 2026-03-25 修正サマリー
- Skills エコシステムが主要 5 プロバイダー全てに対応；Execution Guide と Chain Tracking を削除してモデルが skills を自然にフォロー
- デュアル RAG アーキテクチャ（Code RAG + Data RAG）、統一検索インターフェース `query_knowledge_library`、内蔵 skills への RAG 検索ガイド注入
- `research-orchestrator-pro` を非干渉の分析ハブとして再設計；`scientific-reasoning-lab` を 5 フェーズ自己反復推論エンジンとしてリビルド
- コンテキスト圧縮を時系列のみから 10 因子優先度スコアリングに高度化し、タスク重要情報を保持
- Anti-stall 閾値引き上げ（2→3）と協調的ガイダンスへの軟化
- 5 つの重大修正：`_flush_lock` AttributeError、タスクレベルセレクター UI リバート、worker todo 保護、および上記 2 項
