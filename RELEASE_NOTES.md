# Clouds Coder Release Notes / 发布说明 / リリースノート

Version: `0.1.0`  
Date: `2026-03-05`

## 中文（发布说明）

### 这次发布的定位
Clouds Coder 本次版本聚焦于一个核心方向：

- 建立“CLI 执行层 + Web 用户层”分离协同的 Cloud CLI Coder 体验，让用户在可视化界面中获得 CLI 级执行力与工程可追溯性。

### 核心特典（总览）

- 单文件内核：`Clouds_Coder.py` 承载运行时编排、API、SSE、Web UI bridge、Skills Studio。
- 云端 CLI 编程：服务端工具执行（`bash/read_file/write_file/edit_file`）+ Web 侧实时观测。
- 多模型支持：Ollama + OpenAI-compatible + SiliconFlow + Custom HTTP。
- 小模型优化：上下文预算、截断续写、空转恢复、统一 timeout 治理。
- 多语言切换：`zh-CN/zh-TW/ja/en` 的 UI 与会话语言支持。

### 用户体验创新

- 多预览工作区：同任务支持 Markdown/代码/HTML 三视图预览。
- 实时溯源：代码修改阶段快照、操作流水、差异历史可回看。
- 历史备份体验：stage-based 代码历史与可复制纯代码导出。
- 人性化运行反馈：长任务计时、truncation 续写进度、恢复提示在同一会话面板实时可见。
- Skills 可视化链路：scan -> flow 设计 -> 生成 -> 注入 -> 保存全流程。

### 内核可靠性增强

- 截断恢复闭环：结构化截断检测、尾部修复、多 pass 续写、tokens/pass 可视化。
- 全局 timeout 调度：最小 600s，模型 active 时段排除计时，降低误杀。
- 执行恢复控制器：no-tool idle 诊断与恢复提示自动注入。
- 上下文生命周期管理：`--ctx_limit` 锁定、自适应 compact 与 context recall。

### 发布与部署要点

- 脚本入口统一为：`Clouds_Coder.py`。
- `skills/` 启动时自动释放（`ensure_embedded_skills` + `ensure_runtime_skills`）。
- `js_lib/` 运行时自动下载/校验/缓存（可不随包）。
- 增加发布目录隐藏文件过滤：`.gitignore`（过滤 `.DS_Store`、`__MACOSX`、`._*`）。
- 提供 `pyproject.toml`，支持后续 PyPI 构建发布。

### 兼容性提醒

- 如果你的脚本仍引用 `standalone_web_session_agent.py`，请改为 `Clouds_Coder.py`。
- 打包脚本与 README 中的入口命令已同步更新。

---

## English (Release Notes)

### Release Focus
This release is centered on one architectural direction:

- A separated “CLI execution plane + Web user plane” Cloud CLI Coder workflow, combining CLI-grade execution with Web-grade observability and traceability.

### Core Highlights

- Single-file kernel: `Clouds_Coder.py` now hosts orchestration, APIs, SSE, Web UI bridge, and Skills Studio.
- Cloud-side CLI programming with server tool execution (`bash/read_file/write_file/edit_file`) and live Web feedback.
- Multi-provider support: Ollama, OpenAI-compatible, SiliconFlow, and Custom HTTP.
- Small-model safeguards: context budgeting, truncation continuation, idle recovery, unified timeout governance.
- Native multilingual UX: `zh-CN/zh-TW/ja/en` language switching.

### UX Innovations

- Unified preview workspace for Markdown / Code / HTML.
- Real-time provenance: stage snapshots, operation stream, and diff history.
- History-backup workflow: stage-based code history with copy-safe plain-code export.
- Humanized runtime feedback: elapsed run state, truncation continuation progress, and recovery hints in the same conversation panel.
- Visual Skills pipeline: scan -> flow design -> generate -> inject -> save.

### Reliability & Kernel Upgrades

- Truncation-recovery loop: structural detection, tail repair, multi-pass continuation, live tokens/pass counters.
- Unified timeout scheduler: minimum floor (600s) with model-active-span exclusion.
- Recovery controller: automatic no-tool idle diagnosis and recovery hint injection.
- Context lifecycle management: `--ctx_limit` lock, adaptive compaction, targeted context recall.

### Packaging & Distribution Notes

- Runtime entry script is now `Clouds_Coder.py`.
- `skills/` is auto-extracted at startup (`ensure_embedded_skills` + `ensure_runtime_skills`).
- `js_lib/` is runtime-managed (download/validation/cache), optional in clean package delivery.
- Added hidden-file filtering (`.gitignore`) for macOS artifacts (`.DS_Store`, `__MACOSX`, `._*`).
- Added `pyproject.toml` for future PyPI packaging.

### Compatibility Notice

- If your scripts still reference `standalone_web_session_agent.py`, migrate to `Clouds_Coder.py`.
- Packaging scripts and README command examples are updated accordingly.

---

## 日本語（リリースノート）

### リリースの主眼
本リリースは、次のアーキテクチャ方針を中核にしています。

- 「CLI 実行面 + Web ユーザー面」の分離協調による Cloud CLI Coder 体験。CLI 級実行力と Web 級可観測性/追跡性を統合。

### 主要ハイライト

- 単一ファイルカーネル化：`Clouds_Coder.py` に実行編成、API、SSE、Web UI bridge、Skills Studio を統合。
- サーバ側 CLI 実行（`bash/read_file/write_file/edit_file`）と Web 側リアルタイム可視化。
- マルチプロバイダ対応：Ollama / OpenAI-compatible / SiliconFlow / Custom HTTP。
- 小規模モデル保護：コンテキスト予算、切断継続、idle 回復、統一 timeout 制御。
- 多言語 UI：`zh-CN/zh-TW/ja/en` を標準サポート。

### UX イノベーション

- Markdown / コード / HTML の統合プレビュー。
- リアルタイム追跡：段階スナップショット、操作ストリーム、差分履歴。
- 履歴バックアップ導線：stage ベースのコード履歴と純コードコピー。
- 人間中心の実行フィードバック：長時間実行の経過、切断継続進捗、回復ヒントを同一パネル表示。
- Skills 可視フロー：scan -> flow 設計 -> 生成 -> 注入 -> 保存。

### 信頼性・カーネル強化

- 切断回復ループ：構造検知、末尾補修、マルチパス継続、tokens/pass 可視化。
- 統一 timeout スケジューラ：最小 600 秒、モデル active 区間除外。
- 回復コントローラ：no-tool idle 診断と回復ヒント自動注入。
- コンテキスト管理：`--ctx_limit` ロック、適応 compact、targeted context recall。

### 配布・運用メモ

- 実行エントリは `Clouds_Coder.py` に統一。
- `skills/` は起動時自動展開（`ensure_embedded_skills` + `ensure_runtime_skills`）。
- `js_lib/` は実行時自動取得/検証/キャッシュ（クリーン配布で省略可能）。
- macOS 隠しファイル除外の `.gitignore` を追加（`.DS_Store`、`__MACOSX`、`._*`）。
- PyPI 向けに `pyproject.toml` を追加。

### 互換性注意

- `standalone_web_session_agent.py` を参照する既存スクリプトは `Clouds_Coder.py` へ移行してください。
- パッケージングスクリプトと README の実行例は更新済みです。
