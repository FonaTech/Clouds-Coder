# CHANGELOG 2026-06-05

## Plan continuity, live user steering, Web search, and Web service observability

This update focuses on making long-running Clouds Coder sessions behave like one continuous task system instead of a sequence of loosely connected model turns. The core change is architectural: plan state, todo state, blackboard memory, live user input, tool evidence, Web search, and Web UI rendering now participate in one tighter runtime loop.

---

## English

### Headline: Continuity-first runtime control for plan, multi-agent, and Web sessions

#### 1. Plan resume repair became structural and event-driven

- Added a conservative plan-resume repair path around `_repair_plan_resume_state`, `_detect_plan_resume_state_issue`, and `_maybe_prompt_plan_resume_repair`.
- The runtime now detects real structural conflicts such as missing plan rows, multiple active plan steps, missing active worker subtasks, or missing worker subtask state.
- Repair is surfaced as an LLM-visible structural prompt when the state is actually inconsistent, instead of silently rebuilding the plan tree on every loop.
- Final-subtask and finish gates were separated so completion is not blocked simply because the last subtask has just ended.

#### 2. Safer plan-step advancement evidence

- Plan infrastructure reads, including `.clouds_coder/plan.md` and internal skills-cache reads, no longer count as execution or validation evidence for the current plan step.
- `_worker_step_has_evidence` and `_tool_results_have_validation_evidence` now reject infrastructure-only reads through `_is_plan_infrastructure_read_result`.
- `_phase_gate` now blocks step advancement when the approved plan step has extractable expected subtasks but those subtasks are missing or incomplete.
- This prevents accidental jumps from step 1 to step 2 after merely reading the plan file.

#### 3. Session continuation and live user input are better connected

- `submit_user_message()` now distinguishes a plan choice, a continuation message, a new task, and a live adjustment during an active run.
- Approved plan state is preserved during continuation instead of being reset as a fresh blackboard.
- Runtime live user additions now enter a locked live-input queue with best-effort delivery, so late feedback is not forced to wait for the previous run to finish.
- The frontend no longer treats live-input queue responses as ordinary deferred scheduler tasks.

#### 4. Blackboard-centered cooperation for single and multi-agent modes

- Blackboard state is used more aggressively as the shared task source of truth across Manager, Explorer, Developer, and Reviewer.
- Multi-agent cooperation is tied to the current plan focus instead of letting each role advance a private task.
- Single-agent execution uses the same continuity model at a smaller scale: the active goal, task memory, tool evidence, and todo state still point to the same task line.
- Manager coordination snapshots now carry practical state, including active focus, worker todo progress, recent artifacts, execution evidence, and files already touched for that focus.

#### 5. Tool context, Web search, and user memory integration

- The dynamic tool-context path was expanded so recent tool use can inform later model calls without re-reading the same files or re-running the same commands unnecessarily.
- `agent_web_search` is integrated as a real runtime tool with enable/disable controls, tool feedback events, HTTP fetching, page/evidence tracking, and persistent search indexing.
- Useful search hits and evidence are recorded into a local search index so future searches can reuse successful source patterns.
- User-level long-term memory was added with per-user isolation, summary-only storage, profile capsules, `off/weak/on` influence levels, and clear/export/config API support.

#### 6. Web UI rendering and structured bubbles

- Chat bubble parsing was expanded for plan handoffs, verification markers, todo focus messages, live user adjustments, finish-blocked messages, and Web search events.
- Scroll anchoring now keeps the current viewport stable unless the user is already attached to the bottom.
- Large-session rendering was tuned to reduce flicker, forced reflow, timer-driven scroll jumps, and bottom-position vibration.
- Multi-agent context bars remain session-aware and only replace the single context bar after multi-agent mode is actually active.

#### 7. Runtime configuration and validation

- Automatic L1-L5 classification now has a default automatic ceiling of L2, while manual level and manual plan-mode choices remain authoritative.
- Web search can be controlled through `--enable-web-search` and `--disable-web-search`.
- User preference memory can be controlled through startup/config modes (`off`, `weak`, `on`), with `weak` as the practical default.
- The main runtime and the 2.30 compatibility file were kept in sync.

### 2026-06-05 Summary

- Added event-driven plan resume repair prompts
- Fixed plan-step jumps caused by infrastructure-only reads
- Improved session continuation and live user feedback injection
- Strengthened blackboard cooperation across single/multi-agent and plan/non-plan execution
- Added local agent Web search indexing and feedback visibility
- Added per-user summary memory with configurable influence
- Improved structured bubbles and scroll/render stability
- Validated `Clouds_Coder.py`, `Clouds_Coder_2.30.py`, runtime JavaScript extraction, and split architecture self-check

---

## 中文

### 标题：面向连续任务的 Plan / 多 Agent / Web 会话运行时治理

#### 1. Plan 接续修复改为结构化、按事件触发

- 新增围绕 `_repair_plan_resume_state`、`_detect_plan_resume_state_issue`、`_maybe_prompt_plan_resume_repair` 的保守 plan resume 修复链路。
- 运行时会识别真实结构矛盾，例如 plan rows 缺失、多个 active plan step、缺失 active worker subtask、worker subtask 状态缺失等。
- 修复不再是每轮隐式重建任务树，而是在状态确实矛盾时向 LLM 注入可见的结构化修复提示。
- 最后一个 subtask 完成与 finish gate 被拆开处理，避免“所有子任务完成了，却因为仍在子任务状态而无法 finish”的循环。

#### 2. Plan Step 推进证据更严格

- `.clouds_coder/plan.md` 和内部 skills cache 读取不再被当作当前 plan step 的执行或验收证据。
- `_worker_step_has_evidence` 与 `_tool_results_have_validation_evidence` 通过 `_is_plan_infrastructure_read_result` 排除纯基础设施读取。
- 当当前 plan step 可以解析出应有的 subtasks，但 worker subtasks 缺失或未完成时，`_phase_gate` 会阻止 step 自动推进。
- 这修复了“只读了 plan 文件就从 step 1 跳到 step 2”的误推进问题。

#### 3. Session 接续与实时用户输入衔接更顺畅

- `submit_user_message()` 现在区分 plan 选择、接续消息、新任务，以及运行中的实时用户调整。
- 已批准的 plan state 在接续任务时会保留，而不是被当成新黑板重置。
- 运行中的用户追加输入会进入带锁的 live-input queue，并以 best-effort 方式尽快注入当前任务链路。
- 前端不再把 live-input queue 的响应误当成普通 scheduler 延迟任务。

#### 4. Blackboard 成为 single / multi-agent 的共同任务事实源

- Blackboard 状态被更积极地用于 Manager、Explorer、Developer、Reviewer 之间同步当前任务。
- 多 Agent 合作围绕当前 plan focus 展开，而不是各角色推进自己的私有任务。
- Single-agent 也复用同一套连续性模型：active goal、task memory、tool evidence、todo state 指向同一条任务主线。
- Manager coordination snapshot 会携带当前 focus、worker todo 进度、近期 artifacts、执行证据、已读/已改文件等可操作上下文。

#### 5. Tool Context、Web Search 与用户记忆接入

- 动态 tool context 能让近期工具调用影响后续模型决策，降低重复 read_file、重复 bash、重复检索的概率。
- `agent_web_search` 已作为真实 runtime tool 集成，支持启用/关闭、工具反馈事件、HTTP 抓取、页面/证据追踪与本地搜索索引。
- 命中有效信息的网页与证据会写入本地索引，后续检索可以复用成功来源和信息类型。
- 新增用户级长期记忆：按 user_id 隔离、只保存摘要、profile capsule 注入、`off/weak/on` 影响档位，并支持清空/导出/配置接口。

#### 6. Web UI 渲染与结构化气泡

- 对话气泡结构化解析覆盖 plan handoff、verification marker、todo focus、live user adjustment、finish-blocked、Web search 事件等场景。
- 滚动锚定逻辑改为：只有用户贴底时才自动跟随底部，否则保持当前 viewport 坐标稳定。
- 大会话渲染减少闪屏、强制 reflow、计时器触发的滚动跳动，以及底部细微振动。
- 多 Agent 上下文进度条按 session 状态持久化，只有真实进入多 Agent 后才替换 single context bar。

#### 7. 运行配置与验证

- 自动 L1-L5 分类默认上限改为 L2；用户手动指定复杂度与手动指定 plan mode 仍然优先。
- Web search 支持通过 `--enable-web-search` 与 `--disable-web-search` 控制。
- 用户偏好记忆支持 `off`、`weak`、`on` 三档启动/配置模式，默认 `weak`。
- 主版本 `Clouds_Coder.py` 与兼容版本 `Clouds_Coder_2.30.py` 已同步。

### 2026-06-05 更新摘要

- 新增按事件触发的 plan resume repair 提示
- 修复基础设施读取导致 plan step 误推进的问题
- 改进 session 接续与运行中用户反馈注入
- 强化 single/multi-agent、plan/non-plan 下的 blackboard 协作连续性
- 新增本地 agent Web search 索引与工具反馈可见性
- 新增可配置影响强度的用户级摘要记忆
- 改进结构化气泡与滚动/渲染稳定性
- 已验证 `Clouds_Coder.py`、`Clouds_Coder_2.30.py`、运行时 JS 提取与 split architecture self-check

---

## 日本語

### 見出し：Plan / マルチエージェント / Web セッションを連続タスクとして扱う runtime 制御

#### 1. Plan resume repair を構造検出・イベント駆動に変更

- `_repair_plan_resume_state`、`_detect_plan_resume_state_issue`、`_maybe_prompt_plan_resume_repair` を中心に保守的な plan resume 修復経路を追加しました。
- plan rows の欠落、複数 active plan step、active worker subtask の欠落、worker subtask 状態の欠落など、実際の構造矛盾を検出します。
- 毎ループで隠れて task tree を再構築するのではなく、矛盾があるときだけ LLM へ構造化された修復プロンプトを提示します。
- 最終 subtask 完了と finish gate を分離し、全 subtask が終わった後に finish が不自然にブロックされる循環を減らしました。

#### 2. Plan step 進行証拠を厳格化

- `.clouds_coder/plan.md` や内部 skills cache の読み取りは、現在の plan step の実行・検証証拠として扱わなくなりました。
- `_worker_step_has_evidence` と `_tool_results_have_validation_evidence` は `_is_plan_infrastructure_read_result` により infrastructure-only read を除外します。
- 現在の plan step から期待 subtask を抽出できるのに worker subtasks が欠落または未完了の場合、`_phase_gate` は step 自動進行をブロックします。
- plan file を読んだだけで step 1 から step 2 へ進む誤進行を防ぎます。

#### 3. Session 継続と live user input の接続を改善

- `submit_user_message()` は plan 選択、継続メッセージ、新規タスク、実行中の live adjustment を区別します。
- 承認済み plan state は継続時に保持され、fresh blackboard として不必要に reset されません。
- 実行中に追加されたユーザー入力は lock 付き live-input queue に入り、best-effort で現在のタスクへ注入されます。
- フロントエンドは live-input queue の応答を通常の遅延 scheduler task と誤認しなくなりました。

#### 4. Blackboard を single / multi-agent 共通の task source of truth に

- Blackboard 状態を Manager、Explorer、Developer、Reviewer の同期基盤としてより積極的に利用します。
- Multi-agent 協調は現在の plan focus を中心に動き、各 role が private task を勝手に進める状態を避けます。
- Single-agent でも active goal、task memory、tool evidence、todo state が同じタスク線を指す連続性モデルを使います。
- Manager coordination snapshot には focus、worker todo 進捗、最近の artifacts、実行証拠、既に触れたファイルなどの実用的な文脈が入ります。

#### 5. Tool context、Web search、ユーザーメモリの統合

- 動的 tool context により、直近の tool 利用が後続 model call に反映され、同じ read_file / bash / search の不要な繰り返しを減らします。
- `agent_web_search` を runtime tool として統合し、有効/無効制御、tool feedback event、HTTP fetching、page/evidence tracking、永続 search index に対応しました。
- 有用な検索 hit と evidence はローカル index に記録され、後続検索で成功した source pattern を再利用できます。
- user_id ごとの長期メモリを追加し、summary-only 保存、profile capsule、`off/weak/on` influence level、clear/export/config API を提供します。

#### 6. Web UI rendering と structured bubbles

- plan handoff、verification marker、todo focus、live user adjustment、finish-blocked、Web search events などの bubble 構造化解析を拡張しました。
- スクロール anchoring は、ユーザーが底部にいる場合だけ bottom-follow し、それ以外は現在 viewport を維持します。
- 大きな session での flicker、forced reflow、timer による scroll jump、bottom vibration を減らしました。
- Multi-agent context bar は session-aware になり、実際に multi-agent が有効になった後だけ single context bar を置き換えます。

#### 7. Runtime configuration と検証

- 自動 L1-L5 分類の既定上限を L2 にし、手動 level 指定と手動 plan-mode 指定は引き続き最優先です。
- Web search は `--enable-web-search` と `--disable-web-search` で制御できます。
- User preference memory は `off`、`weak`、`on` の startup/config mode を持ち、既定は `weak` です。
- メイン runtime と 2.30 互換ファイルを同期しました。

### 2026-06-05 要約

- イベント駆動 plan resume repair prompt を追加
- infrastructure-only read による plan step 誤進行を修正
- session 継続と実行中 user feedback injection を改善
- single/multi-agent、plan/non-plan をまたぐ blackboard 協調連続性を強化
- local agent Web search index と tool feedback visibility を追加
- 設定可能な user-level summary memory を追加
- structured bubbles と scroll/render stability を改善
- `Clouds_Coder.py`、`Clouds_Coder_2.30.py`、runtime JS extraction、split architecture self-check を検証
