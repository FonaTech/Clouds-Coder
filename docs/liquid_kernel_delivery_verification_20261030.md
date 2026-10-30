# Liquid Kernel 交付与 CI 修复验证 · 2026-10-30

本次优先处理 GitHub #257 的七项失败与此前的内核导入失败，并完成拆分器归类、三语文档和完整源码交付。用户已修好的工作流不做修改。Docker 启动失败后停止尝试；Linux 原生隔离执行留待用户上传 GitHub 后复验。

## 修复计划与落实

| 问题 | 原因与修复 | 对应验证 |
| --- | --- | --- |
| 收集测试时找不到 `liquid_kernel` | 干净检出不能依赖测试导入顺序；`tests/conftest.py` 先加载公开单文件入口，`pyproject.toml` 配置 pytest 路径 | 无内核目录、无 pytest.ini、无 PYTHONPATH 的两个隔离副本均完成内核优先测试收集 |
| Linux 沙箱测试只显示 `2 != 0` | 测试使用宿主路径和环境，未走运行时虚拟路径与私有临时目录；改用真实运行时接口，保留工作区读写、外部读写阻断和共享目录只读断言 | macOS 原生隔离实测通过；失败时记录后端、stderr、stdout；Linux 仍需 GitHub 复验 |
| 沙箱探测与执行能力不一致 | bubblewrap 探测补齐实际执行使用的 new-session、UTS、IPC 等参数 | 模拟 Linux 探测验证每个必要参数；能力不足不会误报可用，不放开隔离边界 |
| `tools` 导入失败 | 上传的仓库缺少工具目录 | 交付完整 `tools` 包，包括 UTF-8 内嵌包同步工具；GBK 默认环境回归通过 |
| `4.999 != 5.0` | 请求获取门控后按剩余时间发送，精确浮点相等断言错误 | 检查仅发送一次请求，实际 socket timeout 大于零且不超过 5 秒；不放宽产品超时 |
| `/tmp/snap-private-tmp/SKILL.md` 权限异常 | 普通任务的外部技能扫描未保护 `stat`/目录遍历 | 按目录记录警告并继续；四种受限路径下，可读本地与外部技能仍正常加载 |
| shader 元数据测试空列表 | 上传遗漏 `tests/fixtures/skills/shader-dev/SKILL.md` | 补齐夹具；缺失时给出清楚的交付错误，保留真实检索与不加载正文断言 |
| 拆分源码 BOM 解析失败 | 旧拆分器按 UTF-8 保留文件头 BOM | 两份拆分器同步 UTF-8-SIG 读取；中文路径、BOM、独立导入测试通过 |
| 拆分子进程未指定编码 | 旧拆分器依赖平台默认编码 | 捕获边界显式 UTF-8；两份拆分器保持一致 |
| 37 个声明未归类 | 新增运行时状态与私有辅助函数缺少架构所有者 | 拆分器 3.1 共用默认／自动布局规则；当前 1276 条语句、1192 个定义名归入 68 模块，未归类 0；未知声明仍保留诊断 |

主文件修改同时适用于普通任务的技能加载和 IDE 隔离执行，不仅用于自动进化。内嵌 Liquid Kernel 能力版本仍为 19，没有覆盖已进化版本、会话固定版本或历史评分。

## 已完成验证

以下均为本机实际执行，未调用付费模型或发送历史会话。

| 环境／范围 | 结果 | 原始日志 |
| --- | --- | --- |
| Python 3.10.20，干净源码副本全量 pytest | 996 通过、11 跳过、282 子测试通过 | [full310.txt](ci_repair_20261030_logs/full310.txt) |
| Python 3.13.4 / pytest 9.2.0，干净源码副本全量 pytest | 996 通过、11 跳过、282 子测试通过；一条已有弃用警告 | [full313.txt](ci_repair_20261030_logs/full313.txt) |
| 七类 CI 问题的集中回归 | 49 通过、33 子测试通过 | [ci-focused.txt](ci_repair_20261030_logs/ci-focused.txt) |
| Python 3.9.23，新增修复与拆分／技能／并发回归 | 39 通过 | [focused39.txt](ci_repair_20261030_logs/focused39.txt) |
| Python 3.11，新增修复与拆分／技能／并发回归 | 39 通过、30 子测试通过 | [focused311.txt](ci_repair_20261030_logs/focused311.txt) |
| Python 3.12.11，新增修复与拆分／技能／并发回归 | 39 通过、30 子测试通过 | [focused312.txt](ci_repair_20261030_logs/focused312.txt) |
| 拆分全量 self-check | 68 模块、0 未归类，编译、导入、CLI、脱离原文件启动均通过 | [full-split.txt](ci_repair_20261030_logs/full-split.txt) |
| Ruff / Flake8 致命错误检查 | 通过 / 0 | [ruff.txt](ci_repair_20261030_logs/ruff.txt)、[flake8.txt](ci_repair_20261030_logs/flake8.txt) |

11 个跳过项依赖未随干净源码副本携带的旧版历史快照；本次报告的失败项未通过跳过方式规避。Python 3.13 的现有 `re.split` 参数弃用警告不影响运行。

## 安装后复验

已将修复写入用户代码文件夹，并运行公开 `run_split.command`：68 模块、0 未归类、完整 self-check 通过。安装目录 Python 3.10 全量 pytest **1007 通过、301 子测试通过、无跳过**；它额外拥有干净副本未携带的历史快照。详见 [installed-full310.txt](ci_repair_20261030_logs/installed-full310.txt) 和 [installed-split.txt](ci_repair_20261030_logs/installed-split.txt)。

源码分发包与 wheel 构建、`twine check` 通过；源码包确认含新测试引导、技能夹具、tools 和两份拆分器。wheel 在独立目录安装后，Python 3.13 成功加载单文件入口并运行 CLI 帮助。详见 [build-check.txt](ci_repair_20261030_logs/build-check.txt)、[twine-check.txt](ci_repair_20261030_logs/twine-check.txt)、[distribution-check.json](ci_repair_20261030_logs/distribution-check.json) 和 [wheel-cli.txt](ci_repair_20261030_logs/wheel-cli.txt)。

## 上传与复验

修复包采用文件白名单，只包含源码、测试、夹具、工具、三语说明和本次验证材料。**解压后，将内部文件和目录按原路径上传到 GitHub 仓库根目录**；上传 ZIP 文件本身不会替换源码。尤其需要完整上传 `tools/` 和 `tests/fixtures/`。包内不包含 `.github`、API 配置、个人会话、数据库或进化产物。

`Code_Structure` 由更新后的拆分器在用户代码目录重新生成；它是源码派生产物，CI 修复包不携带这一整棵目录。执行 `run_split.command` 可重建并自检。

本次未重启生产服务、触发远程 CI、发布包或部署候选。之前的真实模型与成对进化结果保留在各自原报告中，不作为本次源码的新一轮模型实测。三语 README 与最新日志强调 Liquid Kernel 的任务驱动进化、真实轨迹评分、候选留存、回归与复跑部署门槛，以及能力 19 的执行和反馈可靠性。
