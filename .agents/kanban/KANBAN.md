---
title: SoC 多 Agent 初始公共看板
date: 2026-09-30
version: 7
status: current-planning
owner: COORD
coord_session: Codex 主对话 /root（2026-10-20 本轮）
tags:
- kanban
- soc
- multi-agent
updated: '2026-10-26 14:55:00'
timezone: 北京时间（UTC+8）
plan_revision: marlin-r2
projection_updated: '2026-10-26 14:55:00'
execution_mode: 主对话委派子Agent；V2-P01A已完成独立QA闭环并Done
active_increment: marlin-r2-v2-offline-1
---

# SoC 多 Agent 公共看板（当前执行版）

2026-10-20 接续材料：[MS-01 当前工程登记](../../docs/baseline/ms01_source_inventory_20261020.md)已保存实际源码版本、构建配置、工具及现有制品证据；MS-01 revision 7 更新只读输入 SHA，正式状态仍为 Backlog，独立评审待安排。AP 本地主机复现 1/1 通过；网络同步与 VMware SSH 受当前环境 socket 限制，尚未验证硬件。用户后续已明确采用[本地 MiniMCProto v2.0 / Rev 2.0.3](../../docs/specs/README.md)，知识库不作为运行依赖。下方任务表保留原状态投影，没有宣称正式派单或验收。

**唯一写入者：COORD。** 当前使用本目录 Markdown 卡和人工交接；任务卡是权威明细，本页只是投影视图。没有部署自动看板服务或认领程序。

本轮计划版本 `marlin-r2`。按 D24/D25，SoC 程序运行于 VMware Ubuntu，USB 直通真实 MC，业务经 MC 到 TH。ENG-MC/ENG-TH 岗位已设立，实际执行者/操作授权按细卡登记；能力报告提示查询与代理缺口，接口就绪后才能采真实成功样例。

## 协调岗位与实际执行者

本轮用户“继续”由当前 Codex 主对话 `/root` 落实编排、维护唯一状态入口并收件，已登记实际 COORD；当前使用人工转交，尚未登记/启动独立检查会话。记录见[本轮协调与交接](../../docs/handoff/COORD_20261020.md)。岗位与实际执行安排仍须逐票区分。

任务表“建议主责”列岗位。实际执行者、独立检查者和收件入口分别在卡的 `owner/executor`、`review_assignments`、`handoff` 中登记；岗位原件见 [[AI_SoC_协作方案/02_模块与Agent职责]]。岗位与实际执行者分开登记；实际情况见任务字段，下表只投影状态。

## 你每天看这六项

任务、负责人、当前阶段、完成证据、卡点、下一步。默认最多两个实现任务并行，独立评审/QA 按资源安排；不要求所有岗位同时运行。

## 当前离线协议增量：25 张实际卡

任务原件：[v2.0 微步索引](microtasks/minimc_v2/README.md)。已按契约/独立预期、接口、符号桩、构建、单函数逻辑、解析分支、独立复验和候选归档拆开；原先 V2-P01～06 只作分组，不再另派。

| 分组 | 实际任务 | 当前状态 | 下一步/使用条件 |
| --- | --- | --- | --- |
| 契约与独立预期 | V2-P01A～P01D | Done (P01A~P01D 全部完成闭环) | 包 1 交付已全部完成独立交叉评审并归档；准予放行包 2 (V2-P02A~C) |
| 接口与测试工具约定 | V2-P02A～P02C | Done (P02A~P02C 全部完成闭环) | 包 2 交付已全部完成独立交叉评审并归档；准予放行包 3 (V2-P03A~F) |
| 桩、构建与探针/运行器 | V2-P03A～P03F | Backlog | 先声明、再桩/编译链接；明确未实现，禁止桩当成功 |
| CRC/编码/解码 | V2-P04A～P04D | Backlog | 每票单一能力，使用实现前固定的独立预期 |
| 流式组帧与恢复 | V2-P05A～P05E | Backlog | 同步、头、载荷CRC、超时、恢复分票 |
| 集成、独立复验、候选 | V2-P06A～P06C | Backlog | 十协议检查＋host smoke，绑定准确候选后交下游 |

每票已有真实仓库/文件范围、正常/异常判据、计划命令、预算检查点、证据位置、失败处理与收件入口。当前没有实际作者/检查签署、输入消费版本或租约，不能把结构完整称为已派单或执行闭环。静态检查只审结构，不会自动放行或启动 Agent。

## 当前小任务（人工投影）

投影时间：2026-10-20 11:26:37（北京时间（UTC+8））。按卡原件刷新状态和直接前置；本轮只落实任务编排与管理工具检查，未执行协议实现或硬件联调。

| 任务 | 建议主责 | 直接前置 | 状态投影 | 明确交付 |
| --- | --- | --- | --- | --- |
| [MS-01 交接真实 MC 工程与硬件环境](milestones/marlin_ms01_20261007_214108.md) | INTEGRATOR | 无内部前置 | Backlog | 登记 MC/TH 私有工程、准确版本/配置/工具链、现有制品与 Windows/WSL、VMware Ubuntu 访问及资源信息。 |
| [MS-02 独立复现 MC 构建与启动记录](milestones/marlin_ms02_20261007_214108.md) | QA | MS-01 | Backlog | 按 MS-01 在隔离输出复现真实 MC 固件构建；在操作授权具备时独立观察台架启动日志。 |
| [MS-03 核查主控查询能力](milestones/marlin_ms03_20261007_214108.md) | ARCH | MS-02 | Backlog | 复核当前 MC 源码/配置的 RX、版本/能力/温度请求与回复路径，登记已用能力、报告差异与缺口。 |
| [MS-04 核查真实 MC 双向串口与实收样例](milestones/marlin_ms04_20261007_214108.md) | ENG-FWD | MS-02, MS-03 | Backlog | 在固件接口可用条件成立后，用独立只读客户端验证 Ubuntu USB 直通 MC 的请求/应答，交出原始 TX/RX。 |
| [MS-05 接受主控最小对接约定](milestones/marlin_ms05_20261007_214108.md) | ARCH | MS-03, MS-04, V2-P01B | Backlog | 接受本轮可消费的 MC 只读接口、设计/实现版本、结束条件、不支持/错误、来源与期限。 |
| [MS-06 准备独立主控验收样例](milestones/marlin_ms06_20261007_214108.md) | QA | MS-05, V2-P01D | Backlog | 在实现前准备绑定真实固件版本的查询/解析/无回复、日志交错与恢复预期。 |
| [MS-18 准备 Ubuntu SoC 主机工程](milestones/marlin_ms18_20261008_083854.md) | INTEGRATOR | MS-01 | Backlog | 提供在 VMware Ubuntu 可构建、启动、正常退出的最小 SoC 工程，已有工程优先复用。 |
| [MS-07 实现主控版本查询](milestones/marlin_ms07_20261007_214108.md) | ENG-FWD | MS-05, MS-06, MS-18, V2-P06C | Backlog | 在 Ubuntu SoC 主机工程中按接受契约发送版本查询并解析完整真实 MC 回复。 |
| [MS-08 实现主控温度查询](milestones/marlin_ms08_20261007_214108.md) | ENG-FWD | MS-07 | Backlog | 沿已接受路径解析真实 MC 温度、目标、单位与有效性，缺字段显示未知。 |
| [MS-09 提供可复现主控故障工具](milestones/marlin_ms09_20261007_214108.md) | ENG-SIM | MS-04, MS-05, MS-06 | Backlog | 提供可关闭的 Python Mock/字节故障工具及真实串口断开场景；两类证据分开。 |
| [MS-10 处理主控断链与查询恢复](milestones/marlin_ms10_20261007_214108.md) | ENG-FWD | MS-08, MS-09, MS-06 | Backlog | 按有界期限处理无回复/断开/恢复，重连后重新发新的只读查询，拒绝盲重放动作。 |
| [MS-20 准备 MC 硬件查询验收候选](milestones/marlin_ms20_20261008_083854.md) | INTEGRATOR | MS-06, MS-10 | Backlog | 装配 Ubuntu SoC 程序、真实 MC 固件身份、契约、样例与故障工具的统一验收候选。 |
| [MS-11 验收 SoC 主机程序到真实 MC 闭环](milestones/marlin_ms11_20261007_214108.md) | QA | MS-06, MS-08, MS-10, MS-20 | Backlog | 对 MS-20 锁定候选独立验收 Ubuntu 程序→FWD→真实 MC→返回，接受 PILOT-REQ-01～03。 |
| [MS-12 交接真实 TH 与既有业务协议](milestones/marlin_ms12_20261007_214108.md) | ARCH | MS-01 | Backlog | 复核 MC/TH 定制源码、USART6 业务接口、来源与一个只读代理用例，登记双向代理缺口。 |
| [MS-13 核查真实板间 USART6 通信条件](milestones/marlin_ms13_20261007_214108.md) | ENG-MC | MS-12, MS-02 | Backlog | 对照原理图、两端配置和可取得的只读轨迹，核对 MC USART6 与 TH USART1 参数、引脚、帧边界与接收处理。 |
| [MS-19 准备真实 TH 独立验收预期](milestones/marlin_ms19_20261008_083854.md) | QA | MS-12, MS-13 | Backlog | 在 MC/TH 代理实现前定义真实从控正常、不支持、单端失联/恢复与旧回复预期。 |
| [MS-14 接通 MC 到 TH 双向业务代理](milestones/marlin_ms14_20261007_214108.md) | ENG-MC | MS-05, MS-12, MS-13, MS-11, MS-19 | Backlog | 按接受的板间业务约定实现 MC 请求转发、TH 回传消费、来源与错误返回；配合 ENG-TH 提供真实只读业务入口。 |
| [MS-15 接入经 MC 返回的 TH 状态](milestones/marlin_ms15_20261007_214108.md) | ENG-FWD | MS-07, MS-14, MS-19 | Backlog | 只经 MC 公开接口解析真实 TH 状态和错误，分别记录 MC 与 TH 有效性。 |
| [MS-16 提供 TH 单端故障场景](milestones/marlin_ms16_20261007_214108.md) | ENG-SIM | MS-14, MS-19 | Backlog | 按 MS-19 提供真实 TH 单端不回复/断开/恢复场景并保留 MC 可观察；离线故障工具单列。 |
| [MS-21 准备真实双端验收候选](milestones/marlin_ms21_20261008_083854.md) | INTEGRATOR | MS-11, MS-15, MS-16, MS-19 | Backlog | 锁定已通过主控基础、真实 TH/MC 代理、FWD 和故障工具，交双端候选。 |
| [MS-17 验收真实双 MCU 查询闭环](milestones/marlin_ms17_20261007_214108.md) | QA | MS-11, MS-15, MS-16, MS-19, MS-21 | Backlog | 独立验收 Ubuntu SoC 程序→MC→TH→MC→返回，覆盖真实双端正常及单端故障恢复。 |
| [MS-22 验收实际团队交接](milestones/marlin_ms22_20261008_083854.md) | QA | MS-02 | Backlog | 检查真实任务派单、交付、独立检查、收件与异常恢复记录。 |


### 后续产品规划

| 任务 | 建议主责 | 直接前置 | 状态投影 | 明确交付 |
| --- | --- | --- | --- | --- |
| [PL-01 确认下一产品增量范围](../../docs/planning/product/product_pl01_20261008_083854.md) | PM | 无内部前置 | Backlog | 下一产品增量的范围选择与验收草案/接受记录；未选项仍 Open |
| [PL-02 设计并拆分下一产品增量](../../docs/planning/product/product_pl02_20261008_083854.md) | ARCH | PL-01 | Backlog | 下一增量的设计、接口影响与待执行细任务图 |

## 三个分别验收的出口

| 出口 | 当前状态（本次投影） | 需要的证据 |
| --- | --- | --- |
| A：SoC→MC | 工程登记/本地 AP 候选已准备；独立接受与 HIL 未完成 | MS-20 候选＋MS-11 独立 MC-only 报告 |
| B：SoC→MC→SCM | 源码配置已登记；业务实现与真实双端验收未完成 | MS-19 预期、MS-21 候选＋MS-17 双端报告 |
| T：实际团队交接 | 本轮 COORD/人工方式已登记；用户另指定独立会话，交接执行待发生 | MS-22 的实际交接、独立检查与异常恢复记录 |
| 实际硬件与打印 | 未执行 | 真实板卡/固件/SDK/接线/物理结果证据，另按任务安排 |

首阶段总目标需要 A、B、T 各自通过；不能把主控、受限模型或文档完成当作整机完成。需求原件见 [[AI_SoC_协作方案/pilot_requirements_20261008_083854]]。

## 原 TASK 工作包

TASK-001～018 已在原卡上修订为工作包，`dispatchable: false`。它们描述长期范围或当前小任务的归属，不作为另一套当前派单计划。主责 MS/PL 卡在工作包 `child_tasks` 中登记；其他覆盖关联在 `related_tasks` 中登记，不重复统计；未拆部分继续待计划，不是开发完成。

通信岗位 TASK-013～018 保留；对应功能开工时拆子任务。原有 DDS/D-Bus 硬前置已从主控查询路线移除，三总线各自验收，不把主控模拟当成它们完成。

## 当前缺项与资源

| 输入/资源 | 状态与影响 |
| --- | --- |
| 工程/VMware 访问、版本和配置 | MCU 环境已有交接资料；准确制品与 SoC 工程入口由 MS-01/02/18 登记 |
| Ubuntu USB 直通与 MC 业务接口 | USART2 为用户已确认的 AP 接口；设备/独占待实测，旧 DGUS 需迁移；USART1 仅按调试通道登记 |
| 定制 SCM 源码及既有 MC→SCM 协议 | 部分资料可取得，充分性待核查；影响阶段 B，不挡独立 MC 查询 |
| MCU/硬件维护者和生产写权限 | 岗位已设立，具体人员、授权及资源占用待登记；影响必要扩展、板级修改和物理验收 |
| SDK/目标板与真实设备 | 当前无真实 SoC 板卡，目标 SDK/BSP/资源验收后续安排；真实 MCU 台架按资源占用登记 |
| 当前开发工作区、制品、验收证据 | 本地四仓及版本已登记；AP 构建/迁移启动通过，协议库未实现，真实联调未执行 |

正式控制仓原件已按 manifest 落在 `project-control/`；当前任务卡是唯一明细，本看板是人工投影。根目录旧 `.agents/` 与外部知识库不写正式状态，不能让多个 worktree 各自改权威状态。

任务状态规则、写权限、事件、异常恢复和证据要求见 [[AI_SoC_协作方案/04_公共看板与读写协议]]。

## 接口前置（不计为已完成任务）

TASK-005 的 MCQ-01～06 为 MC 只读接口建设与验收的待执行结构化微步；现成接口已有等效证据时可复用。MCQ 实际状态在原卡记录，本看板不自动认领/放行。MS-04/07/08 使用能力条件，TH 代理缺口在 MS-12/14 跟踪；报告、图更新或 Backlog 卡存在不代表接口已通过。
