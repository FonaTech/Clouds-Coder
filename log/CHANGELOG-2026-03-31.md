# CHANGELOG 2026-03-31

## UX polish + richer file preview + dependency alignment

This update focuses on usability and source-install completeness: richer document/table/media preview coverage, timeout consistency improvements, and a refreshed `requirements.txt` that matches the current file-loading pipeline.

---

## English

### Headline: Better preview coverage, smoother UX, and source-install dependency sync

#### 1. Richer file preview coverage

- Expanded the source-install dependency set so local environments can load and preview uploaded files more reliably.
- The current preview / parsing stack now aligns with the runtime behavior for:
  - PDF: `pdfminer.six` + `PyMuPDF`
  - CSV / TSV: built-in csv parsing, plus `pandas` workflows used by analysis skills
  - Excel: `openpyxl` (`.xlsx/.xlsm`) and `xlrd` (`.xls`)
  - Word: `python-docx`
  - PowerPoint: `python-pptx`
  - Image normalization / asset handling: `Pillow`
- Browser-side preview coverage continues to include image, audio, and video files directly, while unsupported or partially supported formats still fall back to parsed markdown/text previews instead of failing hard.

#### 2. User-experience improvements

- Preview documentation now explicitly reflects support for PDF, Office files, tables, code, HTML/Markdown, and media.
- Source-install instructions now clearly explain that `pip install -r requirements.txt` is the recommended path when users need full upload parsing and rich file preview behavior.
- The model wait / wake timeout path was synchronized with the global runtime timeout so long model wake-ups no longer stop early on a stale fixed 35s / 40s limit.

#### 3. Documentation / packaging alignment

- Added a root `requirements.txt` to match the current runtime capabilities exposed by `Clouds_Coder.py`.
- Updated the top-level README to point to this 2026-03-31 changelog as the latest architecture / UX update.
- Reworded the dependency positioning in README: PyPI install remains the lightweight base runtime, while source install enables the fuller preview/parser stack.

### 2026-03-31 Summary

- Added an explicit source-install `requirements.txt`
- Synced README install guidance with the real preview/parser dependency set
- Documented broader file preview support and recent UX improvements
- Recorded global-timeout synchronization for the model wait chain

---

## 中文

### 标题：文件预览增强、交互体验优化、源码安装依赖补齐

#### 1. 文件预览能力增强

- 补齐了源码安装所需依赖，使本地环境在上传/载入文件时更容易获得完整预览能力。
- 当前预览/解析链路已与运行时能力对齐，覆盖：
  - PDF：`pdfminer.six` + `PyMuPDF`
  - CSV / TSV：内置 `csv` 解析，同时兼容分析链路中的 `pandas`
  - Excel：`openpyxl`（`.xlsx/.xlsm`）与 `xlrd`（`.xls`）
  - Word：`python-docx`
  - PowerPoint：`python-pptx`
  - 图片归一化 / 资源处理：`Pillow`
- 浏览器端仍可直接预览图片、音频、视频；对不完全支持的格式，后端继续保留 markdown / 文本 fallback，而不是直接失败。

#### 2. 用户体验优化

- README 中的预览说明已明确写出 PDF、Office、表格、代码、HTML/Markdown、媒体文件等覆盖范围。
- 源码安装说明现在明确建议：如果需要完整的上传解析与富预览能力，应使用 `pip install -r requirements.txt`。
- 模型 wait / wake 链路的超时已同步到全局 runtime timeout，不再被旧的 35s / 40s 硬编码提前截断。

#### 3. 文档与依赖对齐

- 新增根目录 `requirements.txt`，与 `Clouds_Coder.py` 当前实际能力保持一致。
- 更新顶层 README，把最新变更入口切换到本次 `2026-03-31` changelog。
- README 中对依赖策略的表述已调整：PyPI 安装仍是轻量基础运行时，源码安装则启用更完整的文件预览/解析依赖栈。

### 2026-03-31 更新摘要

- 新增源码安装用 `requirements.txt`
- README 安装说明与当前预览/解析依赖完成对齐
- 补充了更多文件预览与 UX 优化说明
- 记录模型 wait 链路与全局超时的同步修复

---

## 日本語

### 見出し：ファイルプレビュー強化、UX 改善、ソース導入依存の整合

#### 1. ファイルプレビュー対応の強化

- ソース導入時の依存関係を補強し、アップロードファイルの読み込みとプレビューがより安定しました。
- 現在のプレビュー / 解析スタックは以下の形式に対応します。
  - PDF: `pdfminer.six` + `PyMuPDF`
  - CSV / TSV: 組み込み `csv`、分析系では `pandas`
  - Excel: `openpyxl`（`.xlsx/.xlsm`）と `xlrd`（`.xls`）
  - Word: `python-docx`
  - PowerPoint: `python-pptx`
  - 画像アセット処理: `Pillow`
- 画像・音声・動画は引き続きブラウザ側で直接プレビューでき、未対応または部分対応フォーマットは markdown / text fallback に自動で退避します。

#### 2. UX 改善

- README のプレビュー説明を更新し、PDF・Office・表形式・コード・HTML/Markdown・メディア対応を明記しました。
- フル機能のファイル解析とリッチプレビューが必要な場合、`pip install -r requirements.txt` を使うべきことをソース導入手順に明記しました。
- モデルの wait / wake タイムアウトはグローバル runtime timeout に同期され、古い固定 35s / 40s 制限で途中終了しなくなりました。

#### 3. ドキュメント / 依存の整合

- ルートに `requirements.txt` を追加し、`Clouds_Coder.py` の現行機能と一致させました。
- トップ README の最新更新リンクを本 `2026-03-31` changelog に更新しました。
- README の依存方針も更新し、PyPI 導入は軽量ベース、ソース導入はより完全なプレビュー / 解析スタックを有効化する形に整理しました。

### 2026-03-31 要約

- ソース導入向け `requirements.txt` を追加
- README の導入説明を実際の依存関係に合わせて更新
- より広いファイルプレビュー対応と UX 改善を記録
- モデル wait チェーンのグローバルタイムアウト同期を記録
