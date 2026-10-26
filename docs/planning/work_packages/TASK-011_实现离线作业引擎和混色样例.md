---
title: "TASK-011 实现离线作业引擎和混色样例"
date: 2026-09-30
id: TASK-011
revision: 6
status: Backlog
blocked: false
owner: null
proposed_owner: ENG-JOB
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: "ARCH"
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
tags: [soc, task]
updated: '2026-10-13 12:24:23'
timezone: 北京时间（UTC+8）
plan_revision: marlin-r2
task_kind: work_package
dispatchable: false
child_tasks: []
planning_relations:
- MS-11
- TASK-005
related_tasks: []
---

# TASK-011 实现离线作业引擎和混色样例（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前可派单入口是 MS 小卡，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

先短 G-code 作业与进度/暂停/取消语义，再按 SCM 的真实宏/单位/生效边界验证混色；文件不可变，结果未知不盲续打。

建议主责 ENG-JOB；所需证据按子卡范围：离线单测、真实 MCU HIL 和目标 SoC 分开。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

尚未拆出主责小卡；对应功能实现前先设计和拆卡。

关联但不重复计数：无。

每张小卡只有一个主工作包；工作包不直接派单，也不因几个子任务 Done 就自动完成。

## 规划关联

[[AI_SoC_协作方案/tasks/marlin_ms11_20261007_214108|MS-11]]、[[AI_SoC_协作方案/tasks/TASK-005_冻结第一版控制和 AP-MCU 契约|TASK-005]]

## 验收与交接

工作包完成要有范围覆盖、相关子任务/功能验收和准确集成版本；已有少数小卡 Done 不自动完成工作包。MC-only、MC+SCM、目标构建、真实固件与物理结果分别记录，不能互相代替。尚未拆的功能仍待计划，不称全产品功能已完成。

所有路径映射真实仓库并登记白名单；源码与业务由对应 Owner 实现，QA 独立验证，Integrator 锁版本合入，COORD 唯一写任务状态。生产 MCU 扩展和板级改动另落实维护者/授权，不因本卡存在扩大 SoC 范围。

## 非目标

不自动创建开发 Agent、安装系统依赖、改参考报告、替换运动规划、扩大产品功能或操作未授权硬件。主控查询不以 BSP/UI/三总线完成为默认前置；没有的 Marlin 功能记录缺口，不造 API。

实际进度与证据见子任务；规划关联不作为自动派单的硬前置。具体制度见 [[AI_SoC_协作方案/04_公共看板与读写协议]]，统一执行顺序见 [[AI_SoC_协作方案/03_实施步骤与首个闭环]]。

## 本轮范围与功能关联

PL-01 先选择作业模式和真实切片样本，PL-02 明确流控/位点/暂停取消/四通道语义及 GAP 前置后拆作业实现。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。
