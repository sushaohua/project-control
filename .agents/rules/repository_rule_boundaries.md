---
title: PC 全局规则与分仓规则适用边界
date: 2026-11-14
status: current
reviewed_pc_baseline: 1489ab07c8cb408f231cf6f9a3d10ee51e840d35
---

# PC 全局规则与分仓规则适用边界

## 1. 规则三层分离原则

- **Project Control（PC）单源公共规则**：`project-control/.agents/rules/` 定义跨项目职责、任务派发、审批、编码规范、注释规范、服务器候选和独立 QA 门禁，是全局唯一权威原件，**不再向各业务代码仓复制 `shared/` 或 `.repo-rules/` 快照**。
- **`agents` 仓分仓专属规则与技能**：独立仓库 `agents`（工作区位于 `agents/`，主拉取源为内网 GitLab 并双推 GitHub）按 `<repo>/AGENTS.md`、`<repo>/.agents/rules/` 与 `<repo>/.agents/skills/` 存放各业务仓的专属源码、芯片、模块边界与技能。
- **业务代码仓纯净化**：`soc-ap/`、`test_harness/`、`mcu-p3/`、`boot/bootloadermc/`、`boot/bootloaderth/` 内仅保留纯代码、构建与测试；本地和沙箱环境通过 `.gitignore` 忽略的相对软链接（`../agents/<repo>/...` 或 `../../agents/<repo>/...`）挂载分仓入口与规则。
- **服务器与独立 QA 来源绑定**：正式 QA 与沙箱运行不依赖未入 Git 的外部个人路径，而是由 `qa_runner` 按服务端锁定提交同时检出并只读挂载 `project-control@<commit>`（公共规则）与 `agents@<commit>`（分仓规则），由 `qa_runner` 自动衔接沙箱相对软链接。

## 2. 冲突处理与授权

- 发现规则冲突时先确认各规则的来源（`project-control` vs `agents/<repo>`）、版本、目标仓、操作类型和适用环境，分别满足较具体的硬件/源码保护要求与 PC 全局交付门禁；不要以“最后读到的文件”自动覆盖先前有效要求。
- 明确且仍有效的用户指令优先于一般历史流程；超出授权范围或规则间无法协调时暂停相关动作，技术冲突交 ARCH 与对应 Owner 裁定，审批范围冲突交用户/Owner。
- `agents` 仓包含其他外部项目子目录时，本项目 Agent 仅允许读取和修改对应本项目仓库的子目录，严禁越界读写同仓内的其他项目目录。

## 3. 执行环境与硬件规则

- MCU/Boot 本仓规则中的 Windows venv、WSL 防挂起、`probe-rs`、物理串口与预热要求，仅适用于物理台架及获批实机操作；不得误套为 Linux Docker 软件 QA 的容器、端口或探针要求。
- 实机烧录、寄存器操作、复位、故障注入仍遵守本仓 `probe-rs`、芯片型号、探针选择与物理保护规则。软件 QA 通过不代替实机证据。

## 4. 分支、QA 与接续

- 当前 MCU App 使用 `mcu-p3` 的 `feat/soc-debug`；MC/TH Bootloader 各自在独立仓 `soc_debug` 开发；`soc-ap`、`test_harness`、`project-control`、`agents` 使用 `main`。
- 正式 QA 按有效 `qa_policy`（`streamlined-v1` 或 `legacy`）、独立 Codex 会话和服务器锁定候选执行；接单回执与 `read_sources` 须登记实际消费的 `project-control` 与 `agents` 规则提交版本。

## 5. 查阅来源

规则入口及映射关系见同目录 `repository_rule_sources.json`。
