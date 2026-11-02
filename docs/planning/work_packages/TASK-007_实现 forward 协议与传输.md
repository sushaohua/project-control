---
title: TASK-007 实现 forward 协议与传输
date: 2026-09-30
id: TASK-007
revision: 8
status: Backlog
blocked: false
owner: null
proposed_owner: ENG-FWD
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: ARCH
verifier: QA
integrator: INTEGRATOR
baseline: B0
scope_status: work-package-only
required_evidence_level: per-child-scope
lease: null
base_commit: null
candidate_commit: null
merged_commit: null
depends_on: []
tags:
- soc
- task
updated: '2026-10-29T13:52:16+08:00'
timezone: 北京时间（UTC+8）
plan_revision: vmware-soc-twin-20261029
task_kind: work_package
dispatchable: false
child_tasks:
- MS-07
- MS-08
- MS-10
- MS-15
- TEMP-02
- TEMP-03
- TEMP-04
- V2-P02A
- V2-P02B
- V2-P03A
- V2-P03B
- V2-P03C
- V2-P03D
- V2-P03E
- V2-P03F
- V2-P04A
- V2-P04B
- V2-P04C
- V2-P04D
- V2-P05A
- V2-P05B
- V2-P0506
- TWIN-07
- TWIN-25
- TWIN-27
- TWIN-29
- TWIN-36
planning_relations:
- MS-05
- MS-06
related_tasks: []
development_stages:
- vmware-twin
- soc-migration
execution_plan: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
historical_acceptance_scope: 原有签署仅适用其原版本；本次规划修订不继承批准
---

# TASK-007 实现 forward 协议与传输（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前增量派单入口是TWIN能力卡，MS原范围保留，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

先建设本地 v2.0 编解码/组帧与离线检查能力，再按已接受的固件接口实现 SoC 主控查询/恢复和从控状态；会话/串口/HIL 独立验收，不以 DDS 为前置。

建议主责 ENG-FWD；所需证据按子卡范围：离线单测、真实 MCU HIL 和目标 SoC 分开。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

[[AI_SoC_协作方案/tasks/marlin_ms07_20261007_214108|MS-07]]、[[AI_SoC_协作方案/tasks/marlin_ms08_20261007_214108|MS-08]]、[[AI_SoC_协作方案/tasks/marlin_ms10_20261007_214108|MS-10]]、[[AI_SoC_协作方案/tasks/marlin_ms15_20261007_214108|MS-15]]

关联但不重复计数：无。

每张小卡只有一个主工作包；工作包不直接派单，也不因几个子任务 Done 就自动完成。

## 规划关联

[[AI_SoC_协作方案/tasks/marlin_ms05_20261007_214108|MS-05]]、[[AI_SoC_协作方案/tasks/marlin_ms06_20261007_214108|MS-06]]

## 验收与交接

工作包完成要有范围覆盖、相关子任务/功能验收和准确集成版本；已有少数小卡 Done 不自动完成工作包。MC-only、MC+SCM、目标构建、真实固件与物理结果分别记录，不能互相代替。尚未拆的功能仍待计划，不称全产品功能已完成。

所有路径映射真实仓库并登记白名单；源码与业务由对应 Owner 实现，QA 独立验证，Integrator 锁版本合入，COORD 唯一写任务状态。生产 MCU 扩展和板级改动另落实维护者/授权，不因本卡存在扩大 SoC 范围。

## 非目标

不自动创建开发 Agent、安装系统依赖、改参考报告、替换运动规划、扩大产品功能或操作未授权硬件。主控查询不以 BSP/UI/三总线完成为默认前置；没有的 Marlin 功能记录缺口，不造 API。

实际进度与证据见子任务；规划关联不作为自动派单的硬前置。具体制度见 [[AI_SoC_协作方案/04_公共看板与读写协议]]，统一执行顺序见 [[AI_SoC_协作方案/03_实施步骤与首个闭环]]。

## 本轮范围与功能关联

SoC FWD 消费真实 MC/TH 接口；MC/TH 设备侧串口/DMA/代理按固件 Owner 微步交付，运行/升级独占。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。

## v2.0 离线增量的实际子任务

2026-10-20 用户要求继续落实任务拆解、闭环与回溯，本工作包接入以下实际微步卡：

[V2-P02A](../../../.agents/kanban/microtasks/minimc_v2/V2-P02A.md)、[V2-P02B](../../../.agents/kanban/microtasks/minimc_v2/V2-P02B.md)、[V2-P03A](../../../.agents/kanban/microtasks/minimc_v2/V2-P03A.md)、[V2-P03B](../../../.agents/kanban/microtasks/minimc_v2/V2-P03B.md)、[V2-P03C](../../../.agents/kanban/microtasks/minimc_v2/V2-P03C.md)、[V2-P03D](../../../.agents/kanban/microtasks/minimc_v2/V2-P03D.md)、[V2-P03E](../../../.agents/kanban/microtasks/minimc_v2/V2-P03E.md)、[V2-P03F](../../../.agents/kanban/microtasks/minimc_v2/V2-P03F.md)、[V2-P04A](../../../.agents/kanban/microtasks/minimc_v2/V2-P04A.md)、[V2-P04B](../../../.agents/kanban/microtasks/minimc_v2/V2-P04B.md)、[V2-P04C](../../../.agents/kanban/microtasks/minimc_v2/V2-P04C.md)、[V2-P04D](../../../.agents/kanban/microtasks/minimc_v2/V2-P04D.md)、[V2-P05A](../../../.agents/kanban/microtasks/minimc_v2/V2-P05A.md)、[V2-P05B](../../../.agents/kanban/microtasks/minimc_v2/V2-P05B.md)、[V2-P05C](../../../.agents/kanban/microtasks/minimc_v2/V2-P05C.md)、[V2-P05D](../../../.agents/kanban/microtasks/minimc_v2/V2-P05D.md)、[V2-P05E](../../../.agents/kanban/microtasks/minimc_v2/V2-P05E.md)、[V2-P06A](../../../.agents/kanban/microtasks/minimc_v2/V2-P06A.md)。

这些卡各有文件边界、直接前置、正反判据、命令、证据根目录和失败处理；实际状态读取卡原件。离线产出不完成本工作包其他范围，也不替代原 MS 硬件/团队验收。完整关系见[微步索引](../../../.agents/kanban/microtasks/minimc_v2/README.md)。


## 2026-10-29 两阶段孪生开发范围更新

TWIN-07将已对账查询能力接入常驻forward-service，独占UART并经真实IPC提供能力；不再把CLI完成当本阶段出口。

依据[执行总表](../vmware_soc_twin_task_execution_20261029.md)和[两阶段方案](../vmware_soc_twin_development_plan_20261029.md)。旧文中的“首轮不等UI/总线”和CLI目标仅指历史MS/CR最小链路，不能作为本轮阶段一出口。工作包仍不可直接派单，历史子票状态不变。

| 新子票 | 责任岗位 | 当前状态 |
| --- | --- | --- |
| [TWIN-07](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-07.md) | ENG-FWD | Backlog，未派单 |
