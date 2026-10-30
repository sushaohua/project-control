---
title: SoC公共看板
version: 10
status: current-planning
owner: COORD
updated: '2026-10-30T12:26:00+08:00'
plan_revision: vmware-soc-twin-20261029
execution_mode: 任务状态只以原卡为准；计划岗位和别名不表示运行
---

# 当前任务看板

当前接续为[VMware→SoC两阶段孪生任务](../../docs/planning/vmware_soc_twin_task_execution_20261029.md)。共106张有效卡，18张工作包不直接派发；另6张superseded V2历史卡不计入。旧卡状态/阻塞保持，历史签署只适用原版本。根目录旧`.agents`不作正式状态源。

| 类别 | 数量 | 实际状态投影 |
| --- | ---: | --- |
| CR | 15 | Backlog 1、Done 14 |
| MCQ | 2 | Done 2 |
| MS | 22 | Backlog 20、Done 1、Verify 1 |
| PL | 2 | Done 2 |
| TASK | 18 | Backlog 18 |
| TEMP | 7 | Done 7 |
| TWIN | 20 | Backlog 13、Done 7 |
| V2 | 20 | Done 20 |

## 当前顺序与责任

前置任务[TWIN-01](microtasks/vmware_soc_twin/TWIN-01.md)、[TWIN-02](microtasks/vmware_soc_twin/TWIN-02.md)、[TWIN-18](microtasks/vmware_soc_twin/TWIN-18.md)、[TWIN-03](microtasks/vmware_soc_twin/TWIN-03.md)、[TWIN-04](microtasks/vmware_soc_twin/TWIN-04.md)、[TWIN-05](microtasks/vmware_soc_twin/TWIN-05.md)及[TWIN-06](microtasks/vmware_soc_twin/TWIN-06.md)卡面均为Done；其接受范围以各卡绑定候选和证据为准，TWIN-01仍须遵循[交付门禁](../rules/delivery_and_coord_gate.md)登记的疑点和消费限制。后续涉及[TWIN-07](microtasks/vmware_soc_twin/TWIN-07.md)、[TWIN-08](microtasks/vmware_soc_twin/TWIN-08.md)、[TWIN-15](microtasks/vmware_soc_twin/TWIN-15.md)、[TWIN-16](microtasks/vmware_soc_twin/TWIN-16.md)和[TWIN-17](microtasks/vmware_soc_twin/TWIN-17.md)，实际就绪与派单由COORD按任务卡和前置证据核定。

2026-10-30工作区记录中，TWIN-05（Fast DDS SDK与有界QoS）与TWIN-06（D-Bus SDK与权限超时）Run 03经过定向整改，已在双独立Docker沙箱完成100%通过测试，并分别取得独立的真实Codex QA与ARCH双审签APPROVED，经COORD核实全部闭环推进至Done。释放下游任务[TWIN-07](microtasks/vmware_soc_twin/TWIN-07.md)（FORWARD常驻服务）与[TWIN-08](microtasks/vmware_soc_twin/TWIN-08.md)（STATE权威快照）。

最多两张实现卡并行；实际会话、前置接受、写白名单、隔离输出、租约与资源待Ready前落实。台架/串口/探针只登记一名实际操作者，CLI不能与常驻FWD抢UART。QA独立Codex、QA作者产物由非作者ARCH复核；COORD按准确候选收件，不因结构exit0自动推进。

## 既有范围与保留项

CR-12→08→09→10→11及TEMP-01～07卡面Done保留原只读级联/温度CLI候选范围，不代表新服务拓扑/IPC/显示/SoC已完成。温度C1～C6须由TWIN-01逐项对账，旧签署不自动接受新契约。CR-00为Done、CR-07仍为Backlog；升级按所选部署路径判定，不无条件占住新主线。V2有效20张Done，MCQ-0106撤回/限制和MS-07受限Done继续按原裁决读取。

| MS任务 | 状态 | blocked | 关联TWIN能力（非全部核销） |
| --- | --- | --- | --- |
| MS-01 | Backlog | false | TWIN-01, TWIN-04 |
| MS-02 | Backlog | false | TWIN-04 |
| MS-03 | Backlog | false | TWIN-01, TWIN-15 |
| MS-04 | Backlog | false | TWIN-11, TWIN-12 |
| MS-05 | Backlog | false | TWIN-01, TWIN-02 |
| MS-06 | Backlog | false | TWIN-03 |
| MS-07 | Done | false | TWIN-07 |
| MS-08 | Backlog | false | TWIN-07, TWIN-15 |
| MS-09 | Backlog | false | TWIN-03, TWIN-12 |
| MS-10 | Backlog | false | TWIN-07, TWIN-12 |
| MS-11 | Backlog | false | TWIN-11, TWIN-12 |
| MS-12 | Backlog | false | TWIN-01, TWIN-16 |
| MS-13 | Backlog | false | TWIN-11, TWIN-12 |
| MS-14 | Backlog | true | TWIN-15, TWIN-16 |
| MS-15 | Backlog | true | TWIN-07, TWIN-08 |
| MS-16 | Backlog | true | TWIN-03, TWIN-12 |
| MS-17 | Backlog | true | TWIN-12 |
| MS-18 | Backlog | false | TWIN-04 |
| MS-19 | Backlog | false | TWIN-03 |
| MS-20 | Backlog | false | TWIN-11 |
| MS-21 | Backlog | true | TWIN-11 |
| MS-22 | Verify | false |  |

MS-22保持Verify，实际团队交接/异常演练单列；原MS未覆盖温度/TH完整状态/产品范围不自动关闭。PM产品全量目录、JOB/混色/AI/MQTT等按后续批准增量，不把局部完成称整机100%。

18个工作包已更新两阶段范围及TWIN主归属；所有原卡逐项处理见[执行总表第6节](../../docs/planning/vmware_soc_twin_task_execution_20261029.md)。本轮只更新文档和任务发现前缀，检查/审阅见[证据](../../docs/evidence/twin_task_alignment_20261029/README.md)，不表示开发/部署/HIL已执行。
