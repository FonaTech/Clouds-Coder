# Clouds Coder

Clouds Coder は、CLI 実行面と Web ユーザー面の分離を中核に据えたローカルファーストのコーディングエージェント基盤で、Web UI・Skills Studio・堅牢なストリーミング・長タスク回復制御を備えます。

CLI 級の実行力と Web 級の操作体験を統合して、より滑らかな Vibe Coding 体験を実現しつつ、タイムアウト、出力切断、コンテキスト過負荷、thinking-only ループを抑制する設計です。

## 1. プロジェクトの位置づけ

Clouds Coder の中心目標は次の 1 点です。

- CLI 実行面と Web ユーザー面を分離協調させ、低い導入コストで、可観測かつ追跡可能な Vibe Coding ワークフローを提供すること。

本リポジトリは学習用 agent コードから、実配備可能な standalone ランタイムへ発展し、以下を重視しています。

- CLI/Web 分離協調と低コスト導入
- 長時間タスクの信頼性
- 切断回復と継続生成
- コンテキスト予算制御
- Web UI での実行可観測性
- ツール中心の実行可能ワークフロー

## 1.1 アーキテクチャ継承と再利用の明示

Clouds Coder は以下プロジェクトのカーネル思想を明示的に参照・拡張しています。

- shareAI-lab/learn-claude-code: https://github.com/shareAI-lab/learn-claude-code/tree/main

具体的な継承ポイント（本プロジェクトでの対応）：

- 最小 agent ループ（`LLM -> tool_use -> tool_result -> loop`）
- 計画先行（`TodoWrite`）と複雑タスクのドリフト抑制
- `SKILL.md` によるオンデマンド skill ロード契約
- context compact/recall による長会話対応
- task/background/team/worktree 協調モデル

Clouds Coder での拡張点：

- モノリシックなランタイムカーネル（`Clouds_Coder.py`）：agent loop、ツールルータ、セッション管理、API ハンドラ、SSE、Web UI bridge、Skills Studio を単一プロセス状態域で統合。
- 構造化された切断継続エンジン：強い切断シグナル検出、末尾オーバーラップ走査、括弧/記号ペア補修ヒューリスティック、マルチパス継続、pass/token テレメトリ可視化。
- 回復志向の実行コントローラ：no-tool idle 診断、実行時回復ヒント注入、truncation-rescue の todo/task 自動生成、複雑タスクのループ収束誘導。
- 統一 timeout ガバナンス：グローバル timeout スケジューラに最小下限とラウンド会計を持たせ、モデル active 区間を除外して誤タイムアウトを抑制。
- フェーズ別 live-input 仲裁：write/tool/normal フェーズごとに遅延・重みを分離し、遅れて到着したユーザー入力を長時間実行へ安全に合流。
- コンテキストライフサイクル管理：適応的予算 + 手動ロック（`--ctx_limit`）、アーカイブ連動 compact、対象限定の context recall。
- Provider/Profile オーケストレーション層：Ollama + OpenAI-compatible 設定解析、能力推定（マルチモーダル含む）、media endpoint マッピング、実行時選択とフォールバック。
- ストリーミング信頼性と可観測スタック：SSE ハートビート、書き込み例外耐性、モデル呼び出し進捗イベント、event+snapshot ハイブリッド更新。
- アーティファクト優先ワークスペースモデル：セッションごとの `files/uploads/context_archive/code_preview` 永続化、アップロードのワークスペース反映、段階コードプレビューで再現性を確保。

Skills 再利用について：

- `skills/` は同じ `SKILL.md` プロトコル系を継続利用
- `skills/code-review`、`skills/agent-builder`、`skills/mcp-builder`、`skills/pdf` は再利用可能な基盤 skill
- `skills/generated/*` は Clouds Coder 向けに拡張生成された skill 群
- 実行時ツール契約（`load_skill`、`list_skills`、`write_skill` など）との互換性を維持

## 2. 主な機能

- セッション分離された agent runtime
- 内蔵 Web UI + 外部 Web UI の切替
- Skills Studio（別ポート）で skill のスキャン/編集/生成/アップロード
- Ollama モデル検出とカタログ読み込み
- `LLM.config.json` による OpenAI-compatible プロファイル対応
- 統一 timeout 制御（グローバル超時、モデル active 区間除外）
- 切断回復ループ（継続 pass/token を UI にリアルタイム表示）
- コンテキスト圧縮 + アーカイブ再呼び出し
- no-tool idle 診断と回復ヒント
- Task/Todo/Background/Team/Worktree を一体実装
- SSE ハートビートと書き込み例外処理
- Markdown/HTML/ファイル/コード段階プレビュー
- フロントエンド負荷制御（live/static 凍結、スナップショット制御、仮想リスト）

## 3. アーキテクチャ概要

```text
┌───────────────────────────────────────────────────────────────────────┐
│                            Clouds Coder                              │
├───────────────────────────────────────────────────────────────────────┤
│ 体験・追跡レイヤー                                                    │
│  - マルチプレビュー（Markdown / コード / HTML）                      │
│  - 段階コード履歴バックアップ + 差分/追跡タイムライン                │
│  - 実行進捗カード（thinking/run/truncation/recovery）               │
│  - Skills 可視フロー設計 + SKILL.md 生成/注入                        │
├───────────────────────────────────────────────────────────────────────┤
│ 表示レイヤー                                                          │
│  - Agent Web UI（チャット、ボード、プレビュー、状態）                │
│  - Skills Studio（scan/generate/save/upload skills）                 │
├───────────────────────────────────────────────────────────────────────┤
│ API・ストリームレイヤー                                                │
│  - REST APIs：sessions/config/models/tools/preview/render            │
│  - SSE：/api/sessions/{id}/events（heartbeat + 耐障害）              │
├───────────────────────────────────────────────────────────────────────┤
│ オーケストレーション・制御レイヤー                                     │
│  - AppContext / SessionManager / SessionState                        │
│  - EventHub / TodoManager / TaskManager / WorktreeManager            │
│  - 切断回復 + timeout ガバナンス + 実行回復コントローラ               │
├───────────────────────────────────────────────────────────────────────┤
│ モデル・ツール実行レイヤー                                              │
│  - Ollama/OpenAI-compatible profile オーケストレーション              │
│  - tools: bash/read/write/edit/Todo/skills/context/task/render       │
│  - live-input 仲裁 + 小規模モデル保護                                  │
├───────────────────────────────────────────────────────────────────────┤
│ アーティファクト・永続化レイヤー                                        │
│  - セッションごと files/uploads/context_archive/code_preview          │
│  - conversation/activity/operations/todos/tasks/worktree             │
└───────────────────────────────────────────────────────────────────────┘
```

### 3.1 プログラム相互作用アーキテクチャ図

```text
ユーザー（Browser/Web UI）
        │
        │ REST（message/config/uploads/preview） + SSE（runtime events）
        ▼
ThreadingHTTPServer
  ├─ Handler（Agent APIs）
  └─ SkillsHandler（Skills Studio APIs）
        │
        ▼
SessionManager ──► SessionState（セッション単位状態機械）
        │                    │
        │                    ├─ モデル呼び出し編成（Ollama/OpenAI-compatible）
        │                    ├─ ツール実行（bash/read/write/edit/skills/task）
        │                    └─ 回復制御（truncation/timeout/no-tool idle）
        │
        ├─ EventHub（一時実行イベント）
        └─ アーティファクト保存（files/uploads/code_preview/context_archive）
                │
                ▼
       Preview APIs + Render bridge + 履歴追跡タイムライン
                │
                ▼
        Web UI リアルタイム更新（chat/runtime/preview/skills）
```

### 3.2 タスクロジック図

```text
ユーザー目標
   │
   ▼
意図・コンテキスト受理
   │（アップロード/履歴/コンテキスト予算）
   ▼
計画・分解（Todo/Task/Worktree）
   │
   ▼
Agent Loop
  ├─ Model Call
  │    ├─ 通常出力 ───────────────┐
  │    ├─ ツール要求 ─────► ツール実行├─► 結果追記 -> 次ラウンド
  │    └─ 切断シグナル ───► 継続/回復
  │
  ├─ no-tool idle 検知 -> 診断/回復ヒント
  ├─ timeout 制御（モデル active 区間を除外）
  └─ コンテキスト圧迫 -> compact + recall
   │
   ▼
収束出力とアーティファクト
   │
   ▼
プレビュー/履歴/エクスポート（MD/コード/HTML + 段階バックアップ）
```

## 4. 主要ランタイム構成（実装ベース）

メイン実装：`Clouds_Coder.py`。

- `AppContext`：全体設定・モデルカタログ・サーバ状態
- `SessionManager`：セッション管理
- `SessionState`：セッション単位の実行状態、ツール状態、切断/文脈/進行マーカー
- `EventHub`：SSE/内部イベント配信
- `OllamaClient`：モデル呼び出しアダプタとフォールバック
- `SkillStore`：ローカル/プロバイダ skill 登録・読み込み
- `TodoManager` / `TaskManager` / `BackgroundManager`：計画と非同期処理
- `WorktreeManager`：分離作業ディレクトリ
- `Handler` / `SkillsHandler`：Agent UI/Skills Studio API

## 5. 複雑タスク信頼性設計

### 5.1 切断回復クローズドループ

- live truncation 状態（`text/kind/tool/attempts/tokens`）を追跡
- 切断回復イベントを UI に逐次配信
- 末尾バッファと構造情報から continuation prompt を構築
- 破損末尾を補修してから継続出力をマージ
- 多段継続（`TRUNCATION_CONTINUATION_MAX_PASSES`）
- UI 上は同一 call 内の継続として表示

### 5.2 Timeout スケジューリング

- `--timeout` / `--run_timeout` によるグローバル制御
- 最小 timeout は 600 秒
- モデル active 区間を timeout 計算から除外
- timeout 状態は実行ボードで可視化

### 5.3 ループ/空想抑制

- no-tool idle streak を検知
- 空白/思考のみターンの連続時に診断ヒント注入
- 回復モードへ移行しタスク分解を誘導
- Todo/Task と連携して収束性を向上

### 5.4 コンテキスト予算制御

- `--ctx_limit` による文脈予算上限
- ユーザー明示設定時は手動ロック
- UI に推定 token と残量を表示
- 圧迫時は自動 compact + archive recall

## 6. Web UI とパフォーマンス戦略

- SSE + snapshot polling のハイブリッド更新
- モデル実行中の経過時間表示
- 切断回復パネル（pass/token）
- 大規模会話向け仮想リスト経路
- `live/static` 凍結モードで描画負荷を抑制
- render bridge による構造化可視化フレーム更新
- コードプレビューの stage タイムライン + 全文表示

### 6.1 UX イノベーション（プレビュー・追跡・操作性）

- 統合マルチビュー作業面：同一タスクを Markdown 叙述、HTML 表示、コード段階ビューで横断確認できる。
- リアルタイムコード追跡：write/edit 操作が段階スナップショットと操作ストリームに反映され、変更内容・時刻・実行ステップを追跡可能。
- 履歴バックアップ指向のコードレビュー：段階バックアップ、差分行表示、ホットアンカー定位、純コードコピーによりデバッグと監査を両立。
- 人間中心の実行フィードバック：長時間呼び出し中も会話/実行ボード内で経過時間、切断継続進捗、回復ヒントを可視化。
- Skills 制作注入フローの一体化：Skills Studio は scan -> flow 設計 -> 生成 -> 注入 -> 保存の閉ループを提供し、可視 flow builder を搭載。
- 混在コンテンツ作業の連続性：コード/文書/表/メディアのドラッグアップロード後、即座にワークスペースへ反映し、プレビューと実行経路へ接続。

## 7. Skills システム

2 層構造：

- 実行時ロード層：ローカル skill + provider プロトコル
- Skills Studio 制作層：スキャン、生成、保存、アップロード

本リポジトリの skill 構成：

- 再利用基盤：`skills/code-review`、`skills/agent-builder`、`skills/mcp-builder`、`skills/pdf`
- 拡張生成：`skills/generated/*`
- プロトコル/インデックス：`skills/clawhub/`、`skills/skills_Gen/`

対応プロトコル：

- ローカルファイル型
- HTTP JSON provider manifest 型

## 8. API サマリ

主要エンドポイント群：

- グローバル設定/モデル/ツール/skill：`/api/config`、`/api/models`、`/api/tools`、`/api/skills*`
- セッション管理：`/api/sessions`（CRUD）
- セッション実行：`/api/sessions/{id}`、`/api/sessions/{id}/events`（SSE）
- メッセージ/制御：`/message`、`/interrupt`、`/compact`、`/uploads`
- モデル/言語設定：`/api/sessions/{id}/config/model`、`/config/language`
- プレビュー/描画：`/preview-file/*`、`/preview-code/*`、`/preview-code-stages/*`、`/render-state`、`/render-frame`
- Skills Studio：`/api/skillslab/*`

## 9. クイックスタート

### 9.1 必要環境

- Python 3.10+
- Ollama（ローカルモデル運用向け、推奨）
- 依存インストール：

```bash
pip install -r requirements.txt
```

### 9.2 起動

```bash
python Clouds_Coder.py --host 0.0.0.0 --port 8080
```

デフォルト：

- Agent UI：`http://127.0.0.1:8080`
- Skills Studio：`http://127.0.0.1:8081`（無効化可能）

### 9.3 よく使うオプション

- `--model <name>`：起動モデル
- `--ollama-base-url <url>`：Ollama エンドポイント
- `--timeout <seconds>`：グローバル timeout
- `--ctx_limit <tokens>`：コンテキスト上限（明示設定でロック）
- `--max_rounds <n>`：1 run の最大ラウンド
- `--no_Skills_UI`：Skills Studio 無効化
- `--config <path-or-url>`：外部 LLM 設定
- `--use_external_web_ui` / `--no_external_web_ui`：外部 UI 切替
- `--export_web_ui`：内蔵 UI 資産エクスポート

## 10. リポジトリ構成

リリースパッケージ（静的ファイル）：

```text
.
├── Clouds_Coder.py   # コアランタイム（バックエンド + 内蔵フロント資産）
├── requirements.txt                  # Python 依存
├── .env.example                      # 環境変数テンプレート
├── .gitignore                        # リリース時の隠しファイル除外ルール
├── LLM.config.json                   # メイン LLM 設定テンプレート
├── README.md
├── README-zh.md
├── README-ja.md
├── LICENSE
└── packaging/                        # クロスプラットフォーム包装スクリプト
    ├── README.md
    ├── windows/
    ├── linux/
    └── macos/
```

初回起動後に自動生成される構成：

```text
.
├── skills/                           # 起動時に内蔵 bundle から自動展開
│   ├── code-review/
│   ├── agent-builder/
│   ├── mcp-builder/
│   ├── pdf/
│   └── generated/...
├── js_lib/                           # 実行時に自動取得/検証されるフロントライブラリ
├── Codes/                            # セッション作業領域と実行アーティファクト
│   └── user_*/sessions/*/...
└── web_UI/                           # 任意：外部 WebUI 資産エクスポート時に生成
```

補足：

- `skills/` はプログラム側（`ensure_embedded_skills` + `ensure_runtime_skills`）で自動展開されるため、リリース同梱は必須ではありません。
- `js_lib/` は実行時にダウンロード・検証・キャッシュされるため、クリーンなリリース同梱には必須ではありません。
- macOS の隠しファイル（`.DS_Store`、`__MACOSX`、`._*`）は `.gitignore` で除外し、配布物に含めない運用を推奨します。
- 本リリースは意図的に、実行必須ファイルとパッケージングスクリプト中心の最小構成にしています。

## 11. エンジニアリング特性

- 単一ファイル中核で配備と版管理が容易
- API と UI が密結合し、運用可観測性が高い
- 楽観的再試行より決定的回復を重視
- セッション成果物を永続化し、追跡と再現が容易
- 短いデモではなく長時間タスク実行を重視

## 11.1 アーキテクチャ上の優位性（詳細）

- All-in-one 単一ファイルカーネル（`Clouds_Coder.py`）：agent loop、ツールルータ、セッション状態機械、HTTP API、SSE、Web UI bridge、Skills Studio を同一プロセスに統合し、サービス間オーケストレーション負荷と分散障害点を削減。
- 軽量かつ展開容易：依存は最小限（`requirements.txt`）、単一コマンドで起動可能。さらに PyInstaller/Nuitka の onedir/onefile 配布経路を標準化。
- ネイティブなマルチモーダル対応：プロバイダ能力推定と media endpoint ルーティングをプロファイル解析に内蔵し、画像/音声/動画ワークフローを追加プロキシなしで扱える。
- ローカル + Web モデル広域対応と小規模モデル最適化：Ollama と OpenAI-compatible を併用しつつ、context 予算制御、切断継続、idle 回復、統一 timeout により小モデル運用時の失敗率を抑制。

## 11.2 ネイティブな多言語プログラミング環境切替

- UI 言語切替を標準実装：`zh-CN`、`zh-TW`、`ja`、`en` をグローバル/セッション API 経由で切替可能。
- モデル環境切替を標準実装：Web UI から provider/model プロファイルを動的に切替可能（再起動不要、カタログ検証とフォールバックあり）。
- プログラミング言語コンテキスト切替：コードプレビューが多数の拡張子を自動判別して言語レンダラへ割当て、混在言語リポジトリでも連続した読解・編集が可能。

## 11.3 Cloud CLI Coder：アーキテクチャ価値と実運用上の優位性

- クラウド側 CLI 実行モデル：サーバが隔離セッションワークスペース上で `bash`/`read_file`/`write_file`/`edit_file` を実行し、Web 側で CLI 級プログラミング能力と可観測性を提供。
- 配備・配布が容易：単一コマンド起動と PyInstaller/Nuitka（onedir/onefile）経路により、端末ごとにフル CLI 環境を配る方式より運用負荷を削減。
- サーバ側分離の実装基盤：セッション単位の空間分離（`files/uploads/context_archive/code_preview`）と task/worktree 分離により、1テナント1VM など物理分離運用へ接続しやすい。
- Web + CLI の融合 UX：Web の可視性（状態・タイムライン・プレビュー）と CLI の実行力（Shell・決定的ファイル変更・再現可能アーティファクト）を両立。
- マルチ端末並列の集中管理：1 サービスで複数セッションを並列運用し、モデルカタログ、skills レジストリ、操作ログ、ランタイム制御を集約。
- ローカル/プライベートクラウドでの情報保全：実行と成果物を自主管理環境（ローカル、社内 LAN、私有クラウド）に留められ、第三者 SaaS 実行経路への依存を下げられる。

### 11.3.1 一般的な代替方式との比較

- 純粋な Web Copilot と比較：Clouds Coder は提案表示だけでなく、サーバ側ツール実行と成果物永続化まで提供。
- 純粋なローカル CLI Agent と比較：端末ごとの初期構築コストを下げ、共有可能な可視化コントロールプレーンを追加。
- 重量級マルチサービス型 Agent 基盤と比較：軽量トポロジーを維持しつつ、セッション分離、ストリーミング可観測、長タスク回復を実現。

## 12. 参考

### 12.1 主な参照（指定）

- anomalyco/opencode: https://github.com/anomalyco/opencode/
- openai/codex: https://github.com/openai/codex
- shareAI-lab/learn-claude-code: https://github.com/shareAI-lab/learn-claude-code/tree/main

### 12.1.1 learn-claude-code からの明示的継承

- `agents/s01`~`s12` の agent loop/tool dispatch 学習系を系譜として保持
- Todo/task/worktree/team を概念・インターフェースレベルで継承し standalone runtime に統合
- `SKILL.md` のオンデマンド読み込み手法を再利用し Skills Studio へ拡張

### 12.2 追加推奨参照

- Ollama: https://github.com/ollama/ollama
- OpenAI API docs: https://platform.openai.com/docs
- MDN EventSource (SSE): https://developer.mozilla.org/docs/Web/API/EventSource
- PyInstaller: https://pyinstaller.org/
- Nuitka: https://nuitka.net/

### 12.3 本リポジトリ実装時の参照

- `Clouds_Coder.py`（ランタイム構成、API、フロント連携）
- `packaging/README.md`（配布/パッケージング）
- `requirements.txt`（依存）
- `skills/`（skill プロトコルとロード構造）

## 13. ライセンス

本プロジェクトは MIT License で公開されています。詳細は [LICENSE](./LICENSE)。
