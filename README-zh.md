# Clouds Coder

Clouds Coder 是一个以“CLI 执行层与 Web 用户层分离”为核心的本地优先（local-first）编码智能体平台，集成 Web UI、Skills Studio、鲁棒流式回传与复杂任务恢复能力。

它面向真实复杂任务场景，目标是把 CLI 级执行力与 Web 级可视化交互融合成更顺滑的 Vibe Coding 体验，同时解决超时、截断、上下文过载、只思考不执行等问题。

## 1. 项目定位

Clouds Coder 的核心目标：

- 构建 CLI 执行面与 Web 用户面的分离协同环境，让用户以更低门槛获得高质量、可观测、可追溯的 Vibe Coding 体验。

本仓库从学习型 agent 代码演进为可部署的 standalone 运行时，聚焦：

- CLI/Web 分离协同与低门槛上手
- 长任务可靠性
- 截断恢复与续写
- 上下文预算控制
- Web UI 可观测执行状态
- 工具优先的可落地执行链路

## 1.1 架构传承与复用说明

Clouds Coder 明确借鉴并扩展了以下项目的内核思想：

- shareAI-lab/learn-claude-code: https://github.com/shareAI-lab/learn-claude-code/tree/main

具体借鉴点（并在本项目中的映射）：

- 最小 agent 循环（`LLM -> tool_use -> tool_result -> loop`）
- 规划优先（`TodoWrite`）与复杂任务防漂移机制
- `SKILL.md` 按需加载协议
- 上下文压缩与召回（compact/recall）
- task/background/team/worktree 多步骤协同思想

Clouds Coder 在此基础上的扩展：

- 单体内核运行时（`Clouds_Coder.py`）：agent loop、工具路由、会话管理、API Handler、SSE 流、Web UI bridge、Skills Studio 处于同一进程状态域内协作。
- 结构化截断续写引擎：强截断信号检测、尾部重叠扫描、括号/符号配对修复启发式、多 pass 续写与 pass/token 实时遥测。
- 面向恢复的执行控制器：no-tool idle 诊断、运行时恢复提示注入、truncation-rescue 的 todo/task 自动创建，以及复杂任务死循环收敛诱导。
- 统一 timeout 治理：全局 timeout 调度 + 最小下限 + 回合级计账，并排除模型 active 时段，降低“仍在生成却被误超时”的概率。
- 分阶段 live-input 仲裁：针对 write/tool/normal 阶段使用不同延迟与权重策略，把晚到用户指令安全并入长任务执行。
- 上下文生命周期管理：自适应预算与手动锁定（`--ctx_limit`）、归档驱动 compact、按需 context recall，支撑长会话稳定运行。
- Provider/Profile 编排层：Ollama + OpenAI-compatible 配置解析、能力推断（含多模态标记）、media endpoint 映射、运行时选择与回退。
- 流式可靠性与可观测栈：SSE 心跳、写异常容错、模型调用周期进度事件、event+snapshot 混合刷新保障 UI 一致性。
- 工件优先工作区模型：每会话 `files/uploads/context_archive/code_preview` 持久化、上传文件镜像到工作区、阶段化代码预览保障可复现。

Skills 复用说明：

- `skills/` 继续采用同一 `SKILL.md` 协议与 runtime loading 模型
- `skills/code-review`、`skills/agent-builder`、`skills/mcp-builder`、`skills/pdf` 为基础可复用 skills
- `skills/generated/*` 为本项目扩展的场景化 skills（报告、退化恢复、HTML 管线、上传解析等）
- 运行时工具接口与 skill 链路保持兼容（如 `load_skill`、`list_skills`、`write_skill`）

## 2. 核心特性

- 会话隔离的 agent runtime
- 内置 Web UI + 可选外部 Web UI
- Skills Studio（独立端口）用于扫描/编辑/生成/上传 skills
- Ollama 探测与模型目录加载
- 通过 `LLM.config.json` 支持 OpenAI-compatible 多配置
- 统一 timeout 调度（全局超时，模型 active 时段排除）
- 截断恢复循环（续写 pass/token 计数 + UI 实时展示）
- 上下文压缩 + 历史归档召回
- 无工具空转诊断与恢复提示
- Task/Todo/Background/Team/Worktree 一体化机制
- SSE 心跳与写入异常处理
- 预览链路：Markdown/HTML/文件/代码阶段预览
- 前端资源控制：live/static 冻结、快照调度、对话虚拟化

## 3. 架构总览

```text
┌───────────────────────────────────────────────────────────────────────┐
│                            Clouds Coder                              │
├───────────────────────────────────────────────────────────────────────┤
│ 体验与溯源层                                                         │
│  - 多预览中心（Markdown / 代码 / HTML）                              │
│  - 阶段化代码历史备份 + 差异/溯源时间线                              │
│  - 运行进度卡片（thinking/run/truncation/recovery）                 │
│  - Skills 可视化流程构建 + SKILL.md 生成注入                         │
├───────────────────────────────────────────────────────────────────────┤
│ 展示层                                                               │
│  - Agent Web UI（对话、看板、预览、运行状态）                        │
│  - Skills Studio（扫描/生成/保存/上传 skills）                       │
├───────────────────────────────────────────────────────────────────────┤
│ API 与流式层                                                         │
│  - REST APIs：sessions/config/models/tools/preview/render           │
│  - SSE：/api/sessions/{id}/events（心跳 + 容错）                     │
├───────────────────────────────────────────────────────────────────────┤
│ 编排与控制层                                                         │
│  - AppContext / SessionManager / SessionState                        │
│  - EventHub / TodoManager / TaskManager / WorktreeManager            │
│  - 截断恢复 + timeout 治理 + 执行恢复控制器                          │
├───────────────────────────────────────────────────────────────────────┤
│ 模型与工具执行层                                                     │
│  - Ollama/OpenAI-compatible profile 编排                             │
│  - tools: bash/read/write/edit/Todo/skills/context/task/render       │
│  - live-input 仲裁 + 小模型保护策略                                  │
├───────────────────────────────────────────────────────────────────────┤
│ 工件与持久化层                                                       │
│  - 每会话 files/uploads/context_archive/code_preview                 │
│  - conversation/activity/operations/todos/tasks/worktree             │
└───────────────────────────────────────────────────────────────────────┘
```

### 3.1 程序交互架构图

```text
用户（Browser/Web UI）
        │
        │ REST（message/config/uploads/preview） + SSE（runtime events）
        ▼
ThreadingHTTPServer
  ├─ Handler（Agent APIs）
  └─ SkillsHandler（Skills Studio APIs）
        │
        ▼
SessionManager ──► SessionState（会话级运行时状态机）
        │                    │
        │                    ├─ 模型调用编排（Ollama/OpenAI-compatible）
        │                    ├─ 工具执行（bash/read/write/edit/skills/task）
        │                    └─ 恢复控制（truncation/timeout/no-tool idle）
        │
        ├─ EventHub（瞬时运行时事件）
        └─ 工件存储（files/uploads/code_preview/context_archive）
                │
                ▼
       Preview APIs + Render bridge + 历史溯源时间线
                │
                ▼
        Web UI 实时更新（chat/runtime/preview/skills）
```

### 3.2 任务逻辑图

```text
用户目标
   │
   ▼
意图与上下文摄入
   │（上传/历史/上下文预算）
   ▼
规划与分解（Todo/Task/Worktree）
   │
   ▼
Agent Loop
  ├─ Model Call
  │    ├─ 正常输出 ───────────────┐
  │    ├─ 工具调用请求 ─► 执行工具├─► 回填结果 -> 下一轮
  │    └─ 截断信号 ──────► 续写/恢复
  │
  ├─ no-tool idle 检测 -> 诊断与恢复提示
  ├─ timeout 治理（模型 active 时段不计时）
  └─ 上下文压力 -> compact + recall
   │
   ▼
收敛结果与工件
   │
   ▼
预览/历史/导出（MD/代码/HTML + 阶段备份）
```

## 4. 关键运行时组件（来自源码）

主入口：`Clouds_Coder.py`。

- `AppContext`：全局运行时容器（配置、模型目录、服务状态）
- `SessionManager`：会话生命周期管理
- `SessionState`：单会话 agent 状态、工具执行状态、上下文/截断/运行时标记
- `EventHub`：SSE 与内部事件的发布订阅总线
- `OllamaClient`：模型调用适配与回退逻辑
- `SkillStore`：本地/Provider skills 注册与扫描加载
- `TodoManager` / `TaskManager` / `BackgroundManager`：规划与异步执行
- `WorktreeManager`：隔离工作目录管理
- `Handler` / `SkillsHandler`：Agent UI 与 Skills Studio 的 API 入口

## 5. 复杂任务可靠性设计

### 5.1 截断恢复闭环

- 跟踪 live truncation 状态（`text/kind/tool/attempts/tokens`）
- 增量发布截断恢复事件到 UI
- 基于尾部缓冲与结构状态构建 continuation prompt
- 对损坏尾段做修复后再合并续写结果
- 支持多次续写（`TRUNCATION_CONTINUATION_MAX_PASSES`）
- UI 侧按“同一 call 的连续恢复”展示

### 5.2 Timeout 调度

- 每轮 run 采用全局 timeout 调度（`--timeout` / `--run_timeout`）
- 最小 timeout 600 秒
- 模型 active 时段不计入超时预算
- timeout 状态在运行看板可见

### 5.3 防空想/防循环

- 检测 no-tool idle streak
- 连续空白/只思考回合会注入诊断提示
- 进入恢复模式并诱导分解任务执行
- 与 Todo/Task 联动，提升收敛性

### 5.4 上下文预算控制

- `--ctx_limit` 控制上下文预算
- 用户显式设置后触发手动锁定模式
- UI 展示估算 tokens 与剩余预算
- 压力上升时自动 compact + archive recall

## 6. Web UI 与性能策略

- SSE + snapshot 混合刷新
- 模型调用进行中的实时计时与状态条
- 截断恢复实时面板（pass/token）
- 大会话对话虚拟列表路径
- `live/static` 冻结模式降低渲染压力
- render bridge 支持结构化可视化帧推送
- 代码预览支持 stage 时间线 + 全文渲染

### 6.1 UX 创新（预览、溯源、人性化操作）

- 统一多视图预览工作区：同一任务可在 Markdown 叙事、HTML 渲染、代码阶段视图之间无缝切换，无需离开当前会话。
- 实时代码溯源：每次 write/edit 会驱动阶段快照与操作流水更新，用户可追踪“改了什么、何时改、由哪个步骤触发”。
- 面向历史备份的代码审阅体验：阶段化 backup、差异行渲染、热点定位与可复制纯代码导出，兼顾调试与审计。
- 更人性化的运行反馈：长调用期间在会话/运行看板实时展示计时、截断续写进度与恢复提示，而非隐藏在日志里。
- Skills 制作注入流作为一等体验：Skills Studio 提供 scan -> flow 设计 -> 生成 -> 注入 -> 保存闭环，并包含可视化 flow builder。
- 混合内容任务连续性：拖拽上传代码/文档/表格/媒体后，文件会镜像进入工作区并立即接入预览链路与执行链路。

## 7. Skills 系统

两层能力：

- 运行时加载层：本地 skill + provider 协议
- Skills Studio 创作层：扫描、生成、保存、上传

仓库内 skills 组成：

- 基础可复用：`skills/code-review`、`skills/agent-builder`、`skills/mcp-builder`、`skills/pdf`
- 扩展生成：`skills/generated/*`
- 协议与索引资产：`skills/clawhub/`、`skills/skills_Gen/`

协议方向：

- 本地文件协议
- HTTP JSON provider manifest 协议

## 8. API 概览

主要端点组：

- 全局配置/模型/工具/技能：`/api/config`、`/api/models`、`/api/tools`、`/api/skills*`
- 会话生命周期：`/api/sessions`（CRUD）
- 会话运行时：`/api/sessions/{id}`、`/api/sessions/{id}/events`（SSE）
- 控制与消息：`/message`、`/interrupt`、`/compact`、`/uploads`
- 模型与语言配置：`/api/sessions/{id}/config/model`、`/config/language`
- 预览与渲染：`/preview-file/*`、`/preview-code/*`、`/preview-code-stages/*`、`/render-state`、`/render-frame`
- Skills Studio：`/api/skillslab/*`

## 9. 快速开始

### 9.1 环境要求

- Python 3.10+
- Ollama（推荐，用于本地模型）
- 安装依赖：

```bash
pip install -r requirements.txt
```

### 9.2 启动

```bash
python Clouds_Coder.py --host 0.0.0.0 --port 8080
```

默认：

- Agent UI：`http://127.0.0.1:8080`
- Skills Studio：`http://127.0.0.1:8081`（可关闭）

### 9.3 常用参数

- `--model <name>`：启动模型
- `--ollama-base-url <url>`：Ollama 地址
- `--timeout <seconds>`：全局 timeout 调度
- `--ctx_limit <tokens>`：上下文预算（显式设置后锁定）
- `--max_rounds <n>`：单轮最大 agent 回合
- `--no_Skills_UI`：关闭 Skills Studio
- `--config <path-or-url>`：加载外部 LLM 配置
- `--use_external_web_ui` / `--no_external_web_ui`：切换外部 UI
- `--export_web_ui`：导出内置 UI 资源

## 10. 仓库结构

发布包静态结构：

```text
.
├── Clouds_Coder.py   # 核心运行时（后端 + 内嵌前端资源）
├── requirements.txt                  # Python 依赖
├── .env.example                      # 环境变量模板
├── .gitignore                        # 发布时隐藏文件过滤规则
├── LLM.config.json                   # 主 LLM 配置模板
├── README.md
├── README-zh.md
├── README-ja.md
├── LICENSE
└── packaging/                        # 跨平台打包脚本
    ├── README.md
    ├── windows/
    ├── linux/
    └── macos/
```

首次启动后自动生成结构：

```text
.
├── skills/                           # 启动时从内嵌 bundle 自动释放
│   ├── code-review/
│   ├── agent-builder/
│   ├── mcp-builder/
│   ├── pdf/
│   └── generated/...
├── js_lib/                           # 运行时自动下载/校验的前端库缓存
├── Codes/                            # 会话工作区与运行工件
│   └── user_*/sessions/*/...
└── web_UI/                           # 可选；导出外部 WebUI 资源时生成
```

说明：

- `skills/` 由程序自动释放（`ensure_embedded_skills` + `ensure_runtime_skills`），不需要在发布目录手工随包携带。
- `js_lib/` 由运行时自动下载、校验和缓存，干净发布包里可以不存在。
- macOS 隐藏文件（`.DS_Store`、`__MACOSX`、`._*`）通过 `.gitignore` 过滤，发布产物中不应保留。
- 当前发布包有意仅保留运行关键文件与打包脚本。

## 11. 工程特征

- 单文件核心运行时，部署与版本管理简单
- API 与 UI 强耦合可观测，便于在线诊断
- 偏向确定性恢复，而非盲目重试
- 会话级产物可持久化，利于追踪与复现
- 面向长任务稳定执行，不是仅面向短提示

## 11.1 架构优势（深度）

- All-in-one 单文件内核（`Clouds_Coder.py`）：agent loop、工具路由、会话状态机、HTTP API、SSE 流、Web UI bridge、Skills Studio 在同一进程协作，减少跨服务编排与分布式故障点。
- 轻量与易部署：依赖面小（`requirements.txt` 极简），单命令启动，同时支持 PyInstaller/Nuitka 的 onedir/onefile 打包路径，适配本地与分发部署。
- 原生多模态支持：provider 能力推断与 media endpoint 路由在 profile 解析阶段内建，无需额外多模态网关即可对接图像/音频/视频工作流。
- 本地+Web 模型广覆盖并针对小模型优化：同时支持 Ollama 与 OpenAI-compatible 后端；针对小模型增加 context 预算控制、截断续写、空转恢复、统一 timeout 调度等保护机制。

## 11.2 原生多语言编程环境切换

- UI 语言原生切换：支持 `zh-CN`、`zh-TW`、`ja`、`en`，并提供全局与会话级 API 配置入口。
- 模型环境原生切换：可在 Web UI 中按 profile 动态切换 provider/model，无需重启进程，并带模型目录校验与回退。
- 编程语言上下文切换：代码预览可自动识别多种文件后缀并映射渲染语言，适配多语言代码仓库在同一会话中的连续阅读与修改。

## 11.3 Cloud CLI Coder：架构价值与实践优势

- 云端 CLI 执行模型：服务端在隔离会话工作区内执行 `bash`/`read_file`/`write_file`/`edit_file`，用户在 Web 侧获得 CLI 级编程能力与全过程可观测性。
- 易部署与易分发：单命令启动 + PyInstaller/Nuitka（onedir/onefile）打包路径，相比“每台终端都部署完整本地 CLI 栈”更易推广与维护。
- 服务端隔离能力路径：会话级目录隔离（`files/uploads/context_archive/code_preview`）与 task/worktree 隔离，为“一租户一 VM / 主机级物理隔离”提供工程基础。
- Web + CLI 融合体验：既保留 Web 的状态看板/时间线/可视化预览，又保留 CLI 的 Shell 执行、确定性文件修改与工件可复现。
- 多端并行集中管理：单服务可并行管理多会话，统一模型目录、skills 注册表、操作流水与运行时控制面。
- 本地云部署信息安全：代码执行与产物可留在自管环境（本机、内网、私有云），降低对第三方 SaaS 执行路径的依赖。

### 11.3.1 与常见方案对比

- 对比纯 Web Copilot：Clouds Coder 不只是建议层交互，还提供服务端真实工具执行与工件持久化链路。
- 对比纯本地 CLI Agent：Clouds Coder 降低逐端环境配置成本，并增加共享可视化控制平面。
- 对比重型多服务 Agent 平台：Clouds Coder 在保持轻量拓扑的同时，仍提供会话隔离、流式可观测与长任务恢复能力。

## 12. 参考

### 12.1 主要参考（你指定）

- anomalyco/opencode: https://github.com/anomalyco/opencode/
- openai/codex: https://github.com/openai/codex
- shareAI-lab/learn-claude-code: https://github.com/shareAI-lab/learn-claude-code/tree/main

### 12.1.1 与 learn-claude-code 的明确借鉴关系

- 保留 `agents/s01`~`s12` 的 agent loop/tool dispatch 教学链路作为架构来源
- Todo/task/worktree/team 机制在概念与接口层继承，并整合到 standalone web agent
- `SKILL.md` 按需加载方法被复用并扩展到 Skills Studio

### 12.2 建议补充参考

- Ollama: https://github.com/ollama/ollama
- OpenAI API docs: https://platform.openai.com/docs
- MDN EventSource (SSE): https://developer.mozilla.org/docs/Web/API/EventSource
- PyInstaller: https://pyinstaller.org/
- Nuitka: https://nuitka.net/

### 12.3 本仓库实现过程参考

- `Clouds_Coder.py`（运行时架构、API、前端桥接）
- `packaging/README.md`（打包与分发说明）
- `requirements.txt`（依赖面）
- `skills/`（skills 协议与加载结构）

## 13. 许可证

本项目采用 MIT License，见 [LICENSE](./LICENSE)。
