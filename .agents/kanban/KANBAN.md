---
title: SoC 公共看板
version: 8
status: current-planning
owner: COORD
coord_session: Codex 当前主对话 /root（2026-10-28）
updated: '2026-10-28T10:53:59+08:00'
projection_updated: '2026-10-28T10:53:59+08:00'
plan_revision: workflow-replan-20261028
execution_mode: 按卡落实实际会话与授权；未派单不表示运行
---

# 当前任务看板

任务卡是唯一状态明细，本页为 2026-10-28 逐卡 frontmatter 的人工投影。[当前执行分工与重排](../../docs/planning/workflow_replan_20261028.md)规定角色、颗粒度和联调方式；[原快照](../../docs/evidence/workflow_replan_20261028/input_inventory.json)保留调整前 78 张卡及版本。根目录旧 `.agents` 和外部知识库不写正式状态。

## 数量与适用范围

当前 79 张有效卡记录，其中 18 张工作包不直接派发；另有 6 张 superseded V2 历史卡不计入有效数。卡面 Done 不是当前任意候选均可消费；撤回、限制和新增对账要求需与状态一起读。

| 类别 | 数量 | 卡面状态 |
| --- | ---: | --- |
| 工作包 | 18 | Backlog 18 |
| MS里程碑 | 22 | Backlog 21、Done 1 |
| PL规划 | 2 | Backlog 2 |
| V2有效微步 | 20 | Done 20 |
| CR治理/交付 | 15 | Backlog 4、Done 11 |
| MCQ微步 | 2 | Done 2 |

V2 原始 25 张经 6 张归档、1 张收敛票后为 20 张有效卡，全部标记 Done。MCQ-0106 的旧级联候选已撤回；MS-07 的历史 Done 仅保留已裁决范围。CR-02/02Q/02T/03/04/05/06 的当前消费关系须先由 CR-12 逐产物对账，不能用方案 review-02 或 `sha256:verified` 认作各端实现接受。

## 当前派单顺序

CR-12 → CR-08 → CR-09 → CR-10 → CR-11。CR-07 升级专项按部署路径需要或风险可达性决定是否加入硬前置；不因专项存在就机械阻塞无关只读工作，也不能默认旁路安全门禁。所有这些卡当前均 Backlog，等待真实作者、独立检查、准确输入、资源与租约；没有宣称后台执行中。

| 卡片 | 负责岗位 | 本轮结果 |
| --- | --- | --- |
| [CR-12](microtasks/cascade_recovery/CR-12.md) | ARCH＋非作者独立 Codex | 已有产物、接受证据与复用范围集中对账闭环，评定【全量可复用】（Done） |
| [CR-07](microtasks/cascade_recovery/CR-07.md) | ENG-MC；按需 ENG-TH | 升级容量/ACK/文件预检及隔离治理 |
| [CR-08](microtasks/cascade_recovery/CR-08.md) | INTEGRATOR；ARCH/端 Owner/QA | AP/MC/TH 准确候选清单装配与部署 SOP 发布闭环（Done） |
| [CR-09](microtasks/cascade_recovery/CR-09.md) | INTEGRATOR 主持，单一操作者 | 分段及全链路工程联合调试；修复回各端 Owner |
| [CR-10](microtasks/cascade_recovery/CR-10.md) | 独立 Codex QA，非作者复核报告 | 真实 HIL 正常、失联及恢复复验 |
| [CR-11](microtasks/cascade_recovery/CR-11.md) | COORD＋INTEGRATOR | 按原始任务范围接受、列剩余项、交接与版本锁定 |

最多两张实现卡并行，评审按资源安排；不为所有长期角色永久启动 Agent。真实 UART/探针/台架只登记一个实际操作者与占用窗口。[联合调试约定](../../docs/operations/ap_mc_th_joint_debug.md)是计划，未执行动作不计为证据。

## MS 里程碑投影

MS-07/14/15/16/17/21 当前只读级联重叠部分由 CR 恢复序列承接，不重复派发；保留原完整范围、其余前置和未覆盖部分。MS-14 的原非标准 Blocked 状态已规范为 Backlog＋blocked=true。

| 任务 | 状态 | blocked | 消费/派发说明 |
| --- | --- | --- | --- |
| MS-01 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-02 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-03 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-04 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-05 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-06 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-07 | Done | false | 按原卡；Done另核适用限制 |
| MS-08 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-09 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-10 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-11 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-12 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-13 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-14 | Backlog | true | 恢复跟踪，逐范围接受 |
| MS-15 | Backlog | true | 恢复跟踪，逐范围接受 |
| MS-16 | Backlog | true | 恢复跟踪，逐范围接受 |
| MS-17 | Backlog | true | 恢复跟踪，逐范围接受 |
| MS-18 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-19 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-20 | Backlog | false | 按原卡；Done另核适用限制 |
| MS-21 | Backlog | true | 恢复跟踪，逐范围接受 |
| MS-22 | Backlog | false | 按原卡；Done另核适用限制 |

A（MC-only）、B（双 MCU）、T（实际团队交接）分别验收。CR-10 的最小 GET_VERSION/PING 和故障恢复不能自动关闭温度、完整 TH 状态、团队协作及目标 SoC 的未覆盖验收。

## 后续产品规划与工作包

[PL-01](../../docs/planning/product/product_pl01_20261008_083854.md)使用 PM 44 项/SOC 73 项输入，请 HUMAN 选择下一增量；[PL-02](../../docs/planning/product/product_pl02_20261008_083854.md)随后设计拆卡。候选功能不是批准范围，不提前把全部 73 项展开成实现票。

TASK-001～018 仍为不可直接派单的长期工作包，child_tasks 标明唯一主归属，related_tasks 只作关联。当前未执行 CR 的主归属已按契约对账/构建候选/台架/验收重新映射，避免全部挂在模拟工具工作包 TASK-006。

本轮只更新文档/分配并检查结构；历史工程运行与硬件结论以原始证据及当前接受范围为准，主机测试不替代 HIL。独立方案评审结果见[本轮证据](../../docs/evidence/workflow_replan_20261028/)。
