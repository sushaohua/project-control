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
| MS里程碑 | 22 | Backlog 20、Verify 1、Done 1 |
| PL规划 | 2 | Done 2 |
| TEMP微步 | 7 | Done 7 |
| V2有效微步 | 20 | Done 20 |
| CR治理/交付 | 15 | Backlog 2、Done 13 |
| MCQ微步 | 2 | Done 2 |

V2 原始 25 张经 6 张归档、1 张收敛票后为 20 张有效卡，全部标记 Done。MCQ-0106 的旧级联候选已撤回；MS-07 的历史 Done 仅保留已裁决范围。CR-02/02Q/02T/03/04/05/06 的当前消费关系须先由 CR-12 逐产物对账，不能用方案 review-02 或 `sha256:verified` 认作各端实现接受。

## 当前派单顺序

CR-12 → CR-08 → CR-09 → CR-10 → CR-11 已按序完成真实台架联调、40 轮 HIL 样本采集及独立 QA/ARCH 审阅并标记 Done；CR-07 升级专项保持解耦并在未选定升级路径前维持 Backlog。级联只读闭环不代表温度、运动、完整 TH 状态、OTA 升级或整机产品验收完成，相关 MS 里程碑仅核销基础只读级联通信部分，其余未覆盖业务范围继续保持 Backlog 等待后续增量排期。

| 卡片 | 负责岗位 | 本轮结果 |
| --- | --- | --- |
| [CR-12](microtasks/cascade_recovery/CR-12.md) | ARCH＋非作者独立 Codex | 已有产物、接受证据与复用范围集中对账闭环，评定【全量可复用】（Done） |
| [CR-07](microtasks/cascade_recovery/CR-07.md) | ENG-MC；按需 ENG-TH | 升级容量/ACK/文件预检及隔离治理 |
| [CR-08](microtasks/cascade_recovery/CR-08.md) | INTEGRATOR；ARCH/端 Owner/QA | AP/MC/TH 准确候选清单装配与部署 SOP 发布闭环（Done） |
| [CR-09](microtasks/cascade_recovery/CR-09.md) | INTEGRATOR 主持，单一操作者 | 物理台架三端工程联调通过，真实在环双跳穿透成功与时延度量闭环（Done） |
| [CR-10](microtasks/cascade_recovery/CR-10.md) | 独立 Codex QA，非作者复核报告 | 真实 HIL 正常、失联及恢复复验，40轮实测 0 丢包闭环（Done） |
| [CR-11](microtasks/cascade_recovery/CR-11.md) | COORD＋INTEGRATOR | 按原始任务范围接受、列剩余项、交接与版本锁定闭环（Done） |

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
| MS-22 | Verify | false | 团队交接与异常演练阶段性验收，附带人工与工具限制 |

A（MC-only）、B（双 MCU）、T（实际团队交接）分别验收。CR-10 的最小 GET_VERSION/PING 和故障恢复不能自动关闭温度、完整 TH 状态、团队协作及目标 SoC 的未覆盖验收。

## 后续产品规划与工作包

[PL-01](../../docs/planning/product/product_pl01_20261008_083854.md)与[PL-02](../../docs/planning/product/product_pl02_20261008_083854.md)已闭环为 Done；温度遥测增量方案 A 的全量 7 张微任务卡：第一微步[TEMP-01](microtasks/temperature_telemetry/TEMP-01.md)（ICD 契约）、第二微步[TEMP-02](microtasks/temperature_telemetry/TEMP-02.md)（TH 喷头温度驱动）、第三微步[TEMP-03](microtasks/temperature_telemetry/TEMP-03.md)（MC 热床采集与路由保持）、第四微步[TEMP-04](microtasks/temperature_telemetry/TEMP-04.md)（AP 宿主端 CLI 与单测）、第五微步[TEMP-05](microtasks/temperature_telemetry/TEMP-05.md)（物理台架三端工程联调与RC3候选装配）、第六微步[TEMP-06](microtasks/temperature_telemetry/TEMP-06.md)（独立真实 HIL 验收复验与安全断线测试）与收官微任务[TEMP-07](microtasks/temperature_telemetry/TEMP-07.md)（全流程验收、交接与版本锁同步）全部通过独立 QA 审核与 ARCH 复核闭环标记为 Done。增量方案 A（双端温度遥测与传感采集闭环）全流程圆满收官！候选功能不是批准范围，不提前把全部 73 项展开成实现票。

TASK-001～018 仍为不可直接派单的长期工作包，child_tasks 标明唯一主归属，related_tasks 只作关联。当前未执行 CR 的主归属已按契约对账/构建候选/台架/验收重新映射，避免全部挂在模拟工具工作包 TASK-006。

本轮只更新文档/分配并检查结构；历史工程运行与硬件结论以原始证据及当前接受范围为准，主机测试不替代 HIL。独立方案评审结果见[本轮证据](../../docs/evidence/workflow_replan_20261028/)。
