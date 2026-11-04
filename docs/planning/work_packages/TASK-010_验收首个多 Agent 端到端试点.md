---
title: TASK-010 验收首个多 Agent 端到端试点
date: 2026-09-30
id: TASK-010
revision: 11
status: Backlog
blocked: false
owner: null
proposed_owner: QA
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: ARCH
verifier: QA
integrator: INTEGRATOR
baseline: B0
scope_status: work-package-only
required_evidence_level: hardware-and-collaboration-verified
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
- MS-06
- MS-11
- MS-17
- MS-19
- MS-22
- CR-10
- CR-11
- TEMP-06
- TEMP-07
- TWIN-03
- TWIN-12
- TWIN-14
- AUTO-02
- AUTO-03
- AUTO-04
- AUTO-05
- AUTO-06
- TWIN-30
- TWIN-35
- TWIN-40
- TWIN-42
- TWIN-46
- TWIN-50
planning_relations:
- MS-06
- MS-08
- MS-10
related_tasks:
- MS-20
- MS-21
development_stages:
- vmware-twin
- soc-migration
execution_plan: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
historical_acceptance_scope: 原有签署仅适用其原版本；本次规划修订不继承批准
---

# TASK-010 验收首个多 Agent 端到端试点（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前增量派单入口是TWIN能力卡，MS原范围保留，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

MS-06/19 提前交独立预期，MS-11/17 分别验收 MC-only 与 MC+SCM，MS-22 验收实际团队交接。首阶段总出口需要三份对应证据，不把 UI、STATE、三总线绑定主控验收。

建议主责 QA；所需证据分别为真实 MCU 查询与实际协作验收。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

[[AI_SoC_协作方案/tasks/marlin_ms06_20261007_214108|MS-06]]、[[AI_SoC_协作方案/tasks/marlin_ms11_20261007_214108|MS-11]]、[[AI_SoC_协作方案/tasks/marlin_ms17_20261007_214108|MS-17]]、[[AI_SoC_协作方案/tasks/marlin_ms19_20261008_083854|MS-19]]、[[AI_SoC_协作方案/tasks/marlin_ms22_20261008_083854|MS-22]]

关联但不重复计数：[[AI_SoC_协作方案/tasks/marlin_ms20_20261008_083854|MS-20]]、[[AI_SoC_协作方案/tasks/marlin_ms21_20261008_083854|MS-21]]

每张小卡只有一个主工作包；工作包不直接派单，也不因几个子任务 Done 就自动完成。

## 规划关联

[[AI_SoC_协作方案/tasks/marlin_ms06_20261007_214108|MS-06]]、[[AI_SoC_协作方案/tasks/marlin_ms08_20261007_214108|MS-08]]、[[AI_SoC_协作方案/tasks/marlin_ms10_20261007_214108|MS-10]]

## 验收与交接

工作包完成要有范围覆盖、相关子任务/功能验收和准确集成版本；已有少数小卡 Done 不自动完成工作包。MC-only、MC+SCM、目标构建、真实固件与物理结果分别记录，不能互相代替。尚未拆的功能仍待计划，不称全产品功能已完成。

所有路径映射真实仓库并登记白名单；源码与业务由对应 Owner 实现，QA 独立验证，Integrator 锁版本合入，COORD 唯一写任务状态。生产 MCU 扩展和板级改动另落实维护者/授权，不因本卡存在扩大 SoC 范围。

## 非目标

不自动创建开发 Agent、安装系统依赖、改参考报告、替换运动规划、扩大产品功能或操作未授权硬件。主控查询不以 BSP/UI/三总线完成为默认前置；没有的 Marlin 功能记录缺口，不造 API。

实际进度与证据见子任务；规划关联不作为自动派单的硬前置。具体制度见 [[AI_SoC_协作方案/04_公共看板与读写协议]]，统一执行顺序见 [[AI_SoC_协作方案/03_实施步骤与首个闭环]]。

## 当前真实台架验收范围

MS-11/17 必须有 Ubuntu 宿主程序＋真实 MC/TH 候选、原始报文与故障恢复记录；MS-22 需实际任务全生命周期/异常交接及独立检查。Mock、文档结构校验和工作包存在不能代替任何出口通过。目标 SoC 与物理打印另按产品阶段验证。

## v2.0 离线增量的实际子任务

2026-10-20 用户要求继续落实任务拆解、闭环与回溯，本工作包接入以下实际微步卡：

历史关联：[V2-P06B（已替代归档）](../../../.agents/kanban/microtasks/minimc_v2/superseded/V2-P06B.md)。当前离线复验/归档由 [V2-P0506](../../../.agents/kanban/microtasks/minimc_v2/V2-P0506.md) 承接；本工作包只保留范围关联。

这些卡各有文件边界、直接前置、正反判据、命令、证据根目录和失败处理；实际状态读取卡原件。离线产出不完成本工作包其他范围，也不替代原 MS 硬件/团队验收。完整关系见[微步索引](../../../.agents/kanban/microtasks/minimc_v2/README.md)。


## 2026-10-29 两阶段孪生开发范围更新

TWIN-03交独立预期，TWIN-12验VM真实应用加MC/TH，TWIN-14验SoC实板；QA作者产物由非作者ARCH复核。MS-22团队演练单列，不自动核销。

依据[执行总表](../vmware_soc_twin_task_execution_20261029.md)和[两阶段方案](../vmware_soc_twin_development_plan_20261029.md)。旧文中的“首轮不等UI/总线”和CLI目标仅指历史MS/CR最小链路，不能作为本轮阶段一出口。工作包仍不可直接派单，历史子票状态不变。

| 新子票 | 责任岗位 | 当前状态 |
| --- | --- | --- |
| [TWIN-03](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-03.md) | QA | Backlog，未派单 |
| [TWIN-12](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-12.md) | QA | Backlog，未派单 |
| [TWIN-14](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-14.md) | QA | Backlog，未派单 |


## 2026-10-29 连续调度准备

新增主归属AUTO-02，由INTEGRATOR实现并经独立服务器沙箱QA与非作者报告复核后收件。详见[总控执行清单](../coord_autorun_tasklist_20261029.md)。现有子票状态/签署保留，不代表运行器已经部署。
