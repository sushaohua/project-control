# AP-MC-TH 项目接续入口

本目录现由轻量工作区总仓管理，四个项目仓保留独立历史。当前准确恢复版本见 [workspace.json](workspace.json)，初始化、统一推送和空目录恢复见 [WORKSPACE.md](WORKSPACE.md)。当前机器的总仓 Git 命令使用 `bash tools/workspace_git.sh ...`。

新会话或更换 AI 后，请先读取根目录 `AGENTS.md`，再按本文定位项目资料。文件保存项目上下文；聊天历史不作为唯一交接依据。

## 先读哪些文件

| 内容 | 入口 |
| --- | --- |
| 当前目标及用户决定 | [B0 方案基线](project-control/docs/baseline/B0_方案基线.md) |
| 当前通信协议 v2.0（Rev 2.0.3）与采用记录 | [协议资料目录](project-control/docs/specs/README.md) |
| 当前串口信息及确认状态 | [串口链路登记](project-control/docs/baseline/serial_links.md) |
| 通信资料评审、版本分歧与测时建议 | [AP-MC-TH 通信输入](project-control/docs/baseline/ap_mc_th_comm_inputs_20261019_190400.md) |
| 工程位置及登记版本 | [集成清单](project-control/manifest.yaml) |
| 正式任务及状态 | [主看板](project-control/.agents/kanban/KANBAN.md)与其引用的任务卡 |
| 当前分工、任务粒度与联调安排 | [两阶段任务执行与闭环](project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md) |
| 软硬件交付、实物确认及逐阶段签收 | [AP–MC–TH 软硬件交接规范](project-control/docs/operations/ap_mc_th_software_hardware_handover.md) |
| VMware到SoC两阶段孪生开发、进程与界面要求 | [两阶段应用孪生方案](project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md)与[架构输入确认表](project-control/docs/planning/soc_system_architecture_input_register_20261029.md) |
| 当前源码、工具链和现有制品核验 | [MS-01 当前工程登记](project-control/docs/baseline/ms01_source_inventory_20261020.md) |
| 下一步开发与验收顺序 | [TWIN能力任务与依赖](project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md)（原v2首轮保留历史范围） |
| 首批逐票范围、依赖和验收 | [25 张实际微步卡](project-control/.agents/kanban/microtasks/minimc_v2/README.md)与[执行/证据约定](project-control/docs/guides/minimc_v2_task_execution.md) |
| 给用户指定独立会话的材料 | [独立编排审阅说明](project-control/docs/handoff/MINIMC_V2_PLANNING_REVIEW.md) |
| 任务拆解、闭环和回溯是否就绪 | [2026-10-20 编排核查](project-control/docs/planning/task_orchestration_audit_20261020.md) |
| 最新交接、服务器同步结果及后续步骤 | [两阶段接续](project-control/docs/handoff/HANDOFF_VMWARE_SOC_TWIN_20261029.md)；[历史恢复交接](HANDOFF_20261020.md) |
| 克隆恢复、根目录文件恢复与推送方法 | [总仓恢复与同步](WORKSPACE.md)；[控制仓恢复说明](project-control/docs/guides/workspace_restore.md) |
| 2026-10-26 GitLab 实际发布与恢复结果 | [服务器执行证据](project-control/docs/evidence/20261026_gitlab_publication/README.md) |

## 独立项目边界

`D:\AI_RDdocs\` 仅为知识库；当前协议、决定、任务和运行输入使用项目内文件。脱离知识库后的构建/运行命令及验证范围见[独立工作区使用说明](project-control/docs/guides/standalone_workspace.md)。新参考资料先复制并登记，不自动跟随外部原件变化。

## 当前从哪里继续

当前执行方向为**VMware→SoC两阶段尽量1:1孪生开发**。第一阶段运行真实模块、接受的服务边界、进程管理、实际IPC和浏览器交互，继续连接真实MC/TH；第二阶段复用业务源码、契约、UI资源，经工具链/profile/平台与部署适配后实板验收。现有CLI/级联/温度Done按原候选与范围复用，不能当成新架构已完成。

下一张为ARCH的[TWIN-01](project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-01.md)：整体服务架构与温度C1～C6对账；随后02可执行契约及各Owner实现。16张新卡均Backlog，具体顺序、写边界、独立QA和两阶段收件见[执行总表](project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md)。实际派单需落实作者/检查会话、准确输入、有效租约、worktree和资源。

用户于 2026-10-20 明确采用 MiniMCProto v2.0（Rev 2.0.3），原样副本已保存到[项目协议目录](project-control/docs/specs/README.md)，后续使用本地文件。串口参数已由用户确认：AP `/dev/ttyUSB0`→MC USART2 PA2(TX)/PA3(RX)，115200 8N1；MC USART6 PA4(TX)/PA5(RX)↔TH USART1 PB6(TX)/PB7(RX)，921600 8N1；两段均无硬件流控。AP 替代原迪文屏，原屏不再接 USART2；旧 DGUS 路径的实际迁移状态按当前准确 MC 候选及 CR-12 对账核定，不能把串口初始化等同于协议闭环通过。接线输入以串口登记为准，实际部署和运行证据绑定当次候选。

已有输入不应再次要求用户提供。用户报告、源码配置和硬件实测分别登记；发现分歧向用户提问。资料到位或阅读完成，不代表任务验收通过。

AP/MC/TH 已有后续实现和构建记录；可消费范围与未完成的组合 HIL 以当前任务卡、裁决及对账为准。工程版本以开工时实际 Git HEAD 和工作区差异为准，不能仅采用清单中的历史提交。未部署自动调度服务；岗位名称不表示执行者已启动。

MC 与 TH 共用 `mcu-p3` 仓库，用户指定开发分支为 `origin/feat/soc-debug`；本地对应 `feat/soc-debug`。准确登记及来源状态见[集成清单](project-control/manifest.yaml)，后续 Agent 不应自行改用其他开发分支。

## 新会话的启动指令

```text
先读取 README.md 及其中链接的项目输入和当前任务。
核对实际代码版本，告诉我已完成什么、还有什么未确认、下一步做什么。
已有决定从文件接续，不依赖上一段聊天，也不把未验证项当作已通过。
```
