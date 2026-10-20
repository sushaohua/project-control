---
title: "TASK-006 协调真实 MCU 台架和异常夹具"
date: 2026-09-30
id: TASK-006
revision: 6
status: Backlog
blocked: false
owner: null
proposed_owner: INTEGRATOR
reviewer: "ARCH＋现有 MCU Owner"
verifier: QA
integrator: INTEGRATOR
baseline: B0
scope_status: work-package-only
required_evidence_level: host-tool-and-hardware-verified
lease: null
base_commit: null
candidate_commit: null
merged_commit: null
depends_on: []
tags: [soc, task]
updated: '2026-10-13 12:19:12'
timezone: 北京时间（UTC+8）
plan_revision: marlin-r2
task_kind: work_package
dispatchable: false
child_tasks:
- MS-04
- MS-09
- MS-13
- MS-14
- MS-16
planning_relations: []
related_tasks:
- MS-19
---

# TASK-006 协调真实 MCU 台架与异常夹具（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前可派单入口是 MS 小卡，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

协调真实 MCU 台架接入和隔离资源；ENG-MC/ENG-TH 维护固件，ENG-FWD 核查请求/应答，ENG-SIM 只维护 Mock/故障工具。

长期协调归 INTEGRATOR，各子卡执行岗位按原件登记；Mock 工具与真实台架查询分别留证据，已有模拟器路线由 D24 覆盖。

## 已拆小任务

[[AI_SoC_协作方案/tasks/marlin_ms04_20261007_214108|MS-04]]、[[AI_SoC_协作方案/tasks/marlin_ms09_20261007_214108|MS-09]]、[[AI_SoC_协作方案/tasks/marlin_ms13_20261007_214108|MS-13]]、[[AI_SoC_协作方案/tasks/marlin_ms14_20261007_214108|MS-14]]、[[AI_SoC_协作方案/tasks/marlin_ms16_20261007_214108|MS-16]]

关联但不重复计数：[[AI_SoC_协作方案/tasks/marlin_ms19_20261008_083854|MS-19]]

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

协调真实 MCU 台架接入和隔离资源；ENG-MC/ENG-TH 维护固件，ENG-FWD 核查请求/应答，ENG-SIM 只维护 Mock/故障工具。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。
