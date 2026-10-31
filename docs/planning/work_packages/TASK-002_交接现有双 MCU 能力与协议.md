---
title: "TASK-002 交接现有双 MCU 能力与协议"
date: 2026-09-30
id: TASK-002
revision: 6
status: Backlog
blocked: false
owner: null
proposed_owner: ARCH
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: "现有 MCU Owner"
verifier: QA
integrator: INTEGRATOR
baseline: B0
scope_status: work-package-only
required_evidence_level: source-reviewed
lease: null
base_commit: null
candidate_commit: null
merged_commit: null
depends_on: []
tags: [soc, task]
updated: '2026-10-29T13:52:16+08:00'
timezone: 北京时间（UTC+8）
plan_revision: vmware-soc-twin-20261029
task_kind: work_package
dispatchable: false
child_tasks:
- MS-12
- TWIN-15
- TWIN-16
- TWIN-18
- TWIN-21
- TWIN-24
- TWIN-26
planning_relations: []
related_tasks:
- MS-03
development_stages:
- vmware-twin
- soc-migration
execution_plan: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
historical_acceptance_scope: 原有签署仅适用其原版本；本次规划修订不继承批准
---

# TASK-002 交接现有双 MCU 能力与协议（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前增量派单入口是TWIN能力卡，MS原范围保留，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

核查 MC Marlin、定制 SCM 和既有主从协议；生产维护人待登记，资料不足按具体功能列缺口。

建议主责 ARCH；所需证据 source-reviewed。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

[[AI_SoC_协作方案/tasks/marlin_ms12_20261007_214108|MS-12]]

关联但不重复计数：[[AI_SoC_协作方案/tasks/marlin_ms03_20261007_214108|MS-03]]

每张小卡只有一个主工作包；工作包不直接派单，也不因几个子任务 Done 就自动完成。

## 规划关联

无整体硬前置；各子任务按自身输入。

## 验收与交接

工作包完成要有范围覆盖、相关子任务/功能验收和准确集成版本；已有少数小卡 Done 不自动完成工作包。MC-only、MC+SCM、目标构建、真实固件与物理结果分别记录，不能互相代替。尚未拆的功能仍待计划，不称全产品功能已完成。

所有路径映射真实仓库并登记白名单；源码与业务由对应 Owner 实现，QA 独立验证，Integrator 锁版本合入，COORD 唯一写任务状态。生产 MCU 扩展和板级改动另落实维护者/授权，不因本卡存在扩大 SoC 范围。

## 非目标

不自动创建开发 Agent、安装系统依赖、改参考报告、替换运动规划、扩大产品功能或操作未授权硬件。主控查询不以 BSP/UI/三总线完成为默认前置；没有的 Marlin 功能记录缺口，不造 API。

实际进度与证据见子任务；规划关联不作为自动派单的硬前置。具体制度见 [[AI_SoC_协作方案/04_公共看板与读写协议]]，统一执行顺序见 [[AI_SoC_协作方案/03_实施步骤与首个闭环]]。

## 本轮范围与功能关联

交接真实 MC/TH 源码/配置/固件身份、板间接口和能力差距；已有升级资料不代替运行查询。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。


## 2026-10-29 两阶段孪生开发范围更新

第一阶段继续使用真实MC/TH；TWIN-15/16按C1～C6对账与已接受契约复核，只作必要固件修订。

依据[执行总表](../vmware_soc_twin_task_execution_20261029.md)和[两阶段方案](../vmware_soc_twin_development_plan_20261029.md)。旧文中的“首轮不等UI/总线”和CLI目标仅指历史MS/CR最小链路，不能作为本轮阶段一出口。工作包仍不可直接派单，历史子票状态不变。

| 新子票 | 责任岗位 | 当前状态 |
| --- | --- | --- |
| [TWIN-15](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-15.md) | ENG-MC | Backlog，未派单 |
| [TWIN-16](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-16.md) | ENG-TH | Backlog，未派单 |
