---
title: "TASK-001 收敛 FDM 产品需求和验收"
date: 2026-09-30
id: TASK-001
revision: 7
status: Backlog
blocked: false
owner: null
proposed_owner: PM
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: "ARCH"
verifier: QA
integrator: INTEGRATOR
baseline: B0
scope_status: work-package-only
required_evidence_level: document
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
- PL-01
planning_relations: []
related_tasks:
- PL-02
development_stages:
- vmware-twin
- soc-migration
execution_plan: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
historical_acceptance_scope: 原有签署仅适用其原版本；本次规划修订不继承批准
---

# TASK-001 收敛 FDM 产品需求和验收（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前增量派单入口是TWIN能力卡，MS原范围保留，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

逐项收敛当前与后续产品行为、范围和验收。查询试点原件见 [[AI_SoC_协作方案/pilot_requirements_20261008_083854]]；全产品候选项见 [[AI_SoC_协作方案/product_feature_catalog_baseline]]，由 PL-01 收敛下一增量，不以全部产品需求完备挡住查询调查。

建议主责 PM；所需证据 document。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

[[AI_SoC_协作方案/tasks/product_pl01_20261008_083854|PL-01]]

关联但不重复计数：[[AI_SoC_协作方案/tasks/product_pl02_20261008_083854|PL-02]]

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

产品候选以 [SOC 维护原件](../product/product_feature_catalog_baseline.md) 为准，PM 44 项目标显式映射（[PM 产品目标目录](../product/full_color_3d_printer_feature_catalog_baseline.md)）；当前输入版本及 SHA256 见 PL-01/PL-02。逐项范围/阈值由 PL-01 接受。目录更新不自动改变批准范围或本工作包状态。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。


## 2026-10-29 两阶段孪生开发范围更新

保留已批准温度只读切片；PM补首版Must/Should/Later/Out，不把产品目录全量功能展开为本轮实现。

依据[执行总表](../vmware_soc_twin_task_execution_20261029.md)和[两阶段方案](../vmware_soc_twin_development_plan_20261029.md)。旧文中的“首轮不等UI/总线”和CLI目标仅指历史MS/CR最小链路，不能作为本轮阶段一出口。工作包仍不可直接派单，历史子票状态不变。

