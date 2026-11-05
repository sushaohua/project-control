---
title: TASK-005 冻结第一版控制和 AP-MCU 契约
date: 2026-09-30
id: TASK-005
revision: 9
status: Backlog
blocked: false
owner: null
proposed_owner: ARCH
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
reviewer: ENG-FWD＋现有 MCU Owner
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
tags:
- soc
- task
updated: '2026-10-29T13:52:16+08:00'
timezone: 北京时间（UTC+8）
plan_revision: vmware-soc-twin-20261029
task_kind: work_package
dispatchable: false
child_tasks:
- CR-12
- MS-03
- MS-05
- PL-02
- TEMP-01
- V2-P01A
- V2-P01B
- V2-P01C
- V2-P01D
- V2-P02C
- MCQ-0105
- TWIN-01
- TWIN-41
- TWIN-52
planning_relations: []
related_tasks:
- MS-12
development_stages:
- vmware-twin
- soc-migration
execution_plan: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
historical_acceptance_scope: 原有签署仅适用其原版本；本次规划修订不继承批准
---

# TASK-005 冻结第一版控制和 AP-MCU 契约（工作包）

**不直接派单。** 本卡原位修订并保留稳定 ID/文件名，用于描述领域范围和子任务归属；当前增量派单入口是TWIN能力卡，MS原范围保留，不是另一套 TASK 执行顺序。任务状态仅见字段与证据，不在此重复实时结论。

## 目标与范围

通信格式已由 B0 D20 选择本地 MiniMCProto v2.0 / Rev 2.0.3；先提取离线最小契约和独立预期，再结合实际固件核对可用能力。后续会话、控制与升级分别拆卡，不把旧文本/升级通道当成 v2.0 已实现。

建议主责 ARCH；所需证据 document。实际执行条件在子任务登记。读取当前 B0、角色边界和相关已接受约定；分析报告只参考。

本工作包中的建议主责、Reviewer/Verifier/Integrator 表示长期岗位或待落实维护职责，不是已运行的 Agent；“现有 MCU Owner”也不能证明当前已有人接手。只有派出的子任务登记实际执行者、独立检查者和接收入口，定义见 [[AI_SoC_协作方案/02_模块与Agent职责]]。

## 已拆小任务

[[AI_SoC_协作方案/tasks/marlin_ms03_20261007_214108|MS-03]]、[[AI_SoC_协作方案/tasks/marlin_ms05_20261007_214108|MS-05]]、[[AI_SoC_协作方案/tasks/product_pl02_20261008_083854|PL-02]]

关联但不重复计数：[[AI_SoC_协作方案/tasks/marlin_ms12_20261007_214108|MS-12]]

每张小卡只有一个主工作包；工作包不直接派单，也不因几个子任务 Done 就自动完成。

## 规划关联

无整体硬前置；各子任务按自身输入。

## 验收与交接

工作包完成要有范围覆盖、相关子任务/功能验收和准确集成版本；已有少数小卡 Done 不自动完成工作包。MC-only、MC+SCM、目标构建、真实固件与物理结果分别记录，不能互相代替。尚未拆的功能仍待计划，不称全产品功能已完成。

所有路径映射真实仓库并登记白名单；源码与业务由对应 Owner 实现，QA 独立验证，Integrator 锁版本合入，COORD 唯一写任务状态。生产 MCU 扩展和板级改动另落实维护者/授权，不因本卡存在扩大 SoC 范围。

## 非目标

不自动创建开发 Agent、安装系统依赖、改参考报告、替换运动规划、扩大产品功能或操作未授权硬件。主控查询不以 BSP/UI/三总线完成为默认前置；没有的 Marlin 功能记录缺口，不造 API。

实际进度与证据见子任务；规划关联不作为自动派单的硬前置。具体制度见 [[AI_SoC_协作方案/04_公共看板与读写协议]]，统一执行顺序见 [[AI_SoC_协作方案/03_实施步骤与首个闭环]]。

## MC 只读接口前置微步（MCQ）

以下为本工作包内的结构化待执行微步记录，整体 status 保持 Backlog，不直接派发整包；每步在实际执行前落实角色、文件白名单、验收命令与准确输入。已有固件满足时由 MS-03 记录等效证据，不重复修改。接口变化和实现变化分步，构建清单变化单列，失败保留用户已有修改并只回退本步差异。

| 微步 ID | 阶段/建议岗位 | 前置 | 明确产物与判据 | 当前状态 |
| --- | --- | --- | --- | --- |
| MCQ-01 | 设计／ARCH＋ENG-MC | MS-03 来源结论 | 消费 V2-P01B 的离线设计及 MS-03 来源结论，形成固件只读身份/能力/温度、结束/错误/期限的建设接受稿；v2.0 选择已由 B0 记录，不再等待旧协议选择 | Backlog |
| MCQ-02 | 接口／ENG-MC | MCQ-01 | 仅本轮所需头文件声明；引用构建与类型/布局检查通过，实际命令开工前登记 | Backlog |
| MCQ-03 | 符号／ENG-MC | MCQ-02 | 实现文件最小可链接符号；未实现返回明确不可用，不返回假成功 | Backlog |
| MCQ-04 | 构建接入／INTEGRATOR＋ENG-MC | MCQ-03 | 单独接入现行构建目标/include/source 清单；准确固件构建返回 0、告警核查 | Backlog |
| MCQ-05 | 逻辑／ENG-MC | MCQ-04 | 将 RX、请求分发、身份与温度回复、日志分流各拆单函数微步；有界缓冲，来源不混成 fromsd，真实行为符合接受稿 | Backlog |
| MCQ-06 | 独立验证／QA | MCQ-05 | 真实台架请求/回复、未知命令、半包、多包、超时/断连与恢复原始字节；固件/配置/制品/端点/日志可追溯 | Backlog |

MCQ-06 或等效现成接口证据是 MS-04 采集成功样例的使用条件。MS-03 只调查并交允许探测/缺口；MCQ 不反过来依赖 MS-04/05，避免先要真实样例才能开始补接口的循环。MCQ-01 接受的是固件建设输入，MS-05 结合 MS-04 实收接受本轮 FWD 消费约定，两者用途分开。

GAP-02 轴边界、GAP-03 时间单位、GAP-04 断电 ISR 进入相应固件修复微步；真实运动/加热/续打前独立验收，不能仅凭查询通过开放动作。最新源码未在本轮重新读取，报告结论需复核。

## 本轮范围与功能关联

保留 MCQ 结构化前置；设计稿、实际固件和可消费契约版本分别记录。

对应产品项以 PM:/SOC: 限定 ID 追踪到 REQ/ADR/ICD、细卡和实际验收；本工作包不直接派单，不因报告或文档修订改 Done。必要 MCU 扩展由已设立 ENG-MC/ENG-TH 按准确任务授权实施。

## v2.0 离线增量的实际子任务

2026-10-20 用户要求继续落实任务拆解、闭环与回溯，本工作包接入以下实际微步卡：

[V2-P01A](../../../.agents/kanban/microtasks/minimc_v2/V2-P01A.md)、[V2-P01B](../../../.agents/kanban/microtasks/minimc_v2/V2-P01B.md)、[V2-P01C](../../../.agents/kanban/microtasks/minimc_v2/V2-P01C.md)、[V2-P01D](../../../.agents/kanban/microtasks/minimc_v2/V2-P01D.md)、[V2-P02C](../../../.agents/kanban/microtasks/minimc_v2/V2-P02C.md)。

这些卡各有文件边界、直接前置、正反判据、命令、证据根目录和失败处理；实际状态读取卡原件。离线产出不完成本工作包其他范围，也不替代原 MS 硬件/团队验收。完整关系见[微步索引](../../../.agents/kanban/microtasks/minimc_v2/README.md)。


## 2026-10-29 两阶段孪生开发范围更新

TWIN-01冻结全局服务/部署/唯一控制路径和模块实现状态，逐项处理温度冲突；TWIN-02形成可执行契约，旧签署不自动接受新版本。

依据[执行总表](../vmware_soc_twin_task_execution_20261029.md)和[两阶段方案](../vmware_soc_twin_development_plan_20261029.md)。旧文中的“首轮不等UI/总线”和CLI目标仅指历史MS/CR最小链路，不能作为本轮阶段一出口。工作包仍不可直接派单，历史子票状态不变。

| 新子票 | 责任岗位 | 当前状态 |
| --- | --- | --- |
| [TWIN-01](../../../.agents/kanban/microtasks/vmware_soc_twin/TWIN-01.md) | ARCH | Backlog，未派单 |
