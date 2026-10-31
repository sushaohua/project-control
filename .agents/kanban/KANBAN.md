---
title: SoC公共看板
version: 20
status: current-planning
owner: COORD
updated: '2026-10-31T11:38:00+08:00'
plan_revision: vmware-soc-twin-20261029
execution_mode: 任务状态只以原卡为准；计划岗位和别名不表示运行
---

# 当前任务看板

当前接续为[VMware→SoC两阶段孪生任务](../../docs/planning/vmware_soc_twin_task_execution_20261029.md)。共109张有效卡，18张工作包不直接派发；另6张superseded V2历史卡不计入。旧卡状态/阻塞保持，历史签署只适用原版本。根目录旧`.agents`不作正式状态源。

| 类别 | 数量 | 实际状态投影 |
| --- | ---: | --- |
| CR | 15 | Backlog 1、Done 14 |
| MCQ | 2 | Done 2 |
| MS | 22 | Backlog 20、Done 1、Verify 1 |
| PL | 2 | Done 2 |
| TASK | 18 | Backlog 18 |
| TEMP | 7 | Done 7 |
| TWIN | 27 | Backlog 4、InProgress 2、Done 21 |
| V2 | 20 | Done 20 |

## 当前顺序与责任

前置任务[TWIN-01](microtasks/vmware_soc_twin/TWIN-01.md)至[TWIN-12](microtasks/vmware_soc_twin/TWIN-12.md)、[TWIN-17](microtasks/vmware_soc_twin/TWIN-17.md)至[TWIN-22](microtasks/vmware_soc_twin/TWIN-22.md)及[TWIN-24](microtasks/vmware_soc_twin/TWIN-24.md)卡面均为Done；其接受范围以各卡绑定候选和证据为准，TWIN-01仍须遵循[交付门禁](../rules/delivery_and_coord_gate.md)登记的疑点和消费限制。
- [TWIN-21](microtasks/vmware_soc_twin/TWIN-21.md)（MC固件0x16坐标查询与运动指令响应）：已完成0x16 20B微米整型对账、栈溢出根除与强电0%锁死，服务器沙箱100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-22](microtasks/vmware_soc_twin/TWIN-22.md)（AP端温控倍数换算与故障哨兵防御性治理）：已完成deci_c至milli_c统一换算（解决TWIN-12 245.0℃ vs 24.5℃冲突）、故障哨兵输出null与降级，服务器沙箱11项单测100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-24](microtasks/vmware_soc_twin/TWIN-24.md)（MC固件5×5调平网格导出0x18响应实现）：落实U-D04裁决，基于固件存量5×5双线性网格导出52B载荷，缓冲区扩至128B，双独立Docker沙箱100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-25](microtasks/vmware_soc_twin/TWIN-25.md)（AP端0x18调平网格解析与设备状态拓扑呈现）：承接TWIN-24下位机网格数据，提供D-Bus/HTTP-SSE/Web HMI拓扑状态呈现，已派发ENG-FWD会话session-eng-fwd-twin-25执行；
- [TWIN-26](microtasks/vmware_soc_twin/TWIN-26.md)（双MCU固件升级通道与Bootloader IAP协议复用对账）：落实U-D05首版固件升级裁决，恪守避免修改Bootloader原则，TH复用存量921600 IAP时序，MC评估探针与透传通道，已派发ARCH会话session-arch-twin-26执行；
- [TWIN-27](microtasks/vmware_soc_twin/TWIN-27.md)（AP端VMware指定目录固件扫描与安全准入服务实现）：在soc-ap实现/var/update/目录扫描、128B Trailer验签与device-manager前置安全联锁，规划就绪Backlog；
- [TWIN-28](microtasks/vmware_soc_twin/TWIN-28.md)（端到端真实双MCU固件升级在环联调与验收）：在真实物理MC/TH台架上实测刷写，0x01/0x02前后版本核验，规划就绪Backlog。

2026-10-30工作区记录中：
1. **TWIN-07（FORWARD常驻服务与唯一UART通路）**：已完成常驻进程守护、MiniMCProto v2.0双向编解码与CRC校验、PTY串口仿真、DDS `telemetry/raw_temp`低延迟发布与D-Bus RPC控制服务，在独立Docker沙箱中通过100%验证，取得独立Codex QA与ARCH审签APPROVED闭环；
2. **TWIN-08（STATE权威快照与统一请求准入）**：已完成单一权威温度状态模型与世代单调递增管理、3s/10s新鲜度退化评估、50ms防抖统一请求准入仲裁、急停熔断、DDS与D-Bus异步广播联动，在独立Docker沙箱中通过100%验证，取得独立Codex QA与ARCH审签APPROVED闭环；
3. **TWIN-15（MC温度契约复核与必要修订）**：已完成MC固件0x14查询响应实现、0.1℃ (`deci_c`) 分辨率对账消除溢出、强电安全硬性锁死为0%及TH报文原生透明中继保持，在独立Docker沙箱（`TWIN-15_run_173258`）中完成100%验证，生成AT32F435固件并取得独立Codex QA与ARCH审签APPROVED闭环；
4. **TWIN-09（UI网关真实HTTP与SSE通信）**：已完成独立守护进程、非阻塞POSIX Socket与poll()事件循环、HTTP REST快照/准入采样代理、SSE实时长连接多客户端广播、D-Bus点对点解耦交互及全自研函数≤50行硬门禁，在独立Docker容器沙箱（`TWIN-09_run_174259`）中完成100%验证（8/8用例全通），取得独立Codex QA与ARCH审签APPROVED闭环；
5. **TWIN-16（TH温度契约复核与必要修订）**：已完成TH固件0x14查询响应实现、0.1℃ (`deci_c`) 分辨率全面对账、NTC查表映射修正、开短路故障哨兵（0x7FFF）以及thermistor_safety_lock强电硬件硬锁死，在独立Docker沙箱（`TWIN-16_run_175010`）中完成100%验证，生成AT32F423打包固件并取得独立Codex QA与ARCH审签APPROVED闭环；
6. **TWIN-10（浏览器交互屏幕接入真实业务接口）**：已完成纯原生零外部依赖的前端交互HMI、实时SSE事件流长连接接入、REST快照加载与防抖准入采样控制、严防死守零伪造模拟数据、0x7FFF/0x7FFE显式哨兵映射及800x480触摸屏优化，在独立Docker容器沙箱（`TWIN-10_run_175524`）中完成100%验证（7/7用例全通），取得独立Codex QA与ARCH审签APPROVED闭环；
7. **TWIN-11（VMware整链联调与候选交接）**：已完成全链路发布元数据定义（vmware_twin_candidate.yaml锁定微服务/Web/固件制品精准Commit与SHA256）、编排启动联调SOP手册（vmware_twin_joint_debug.md覆盖多进程拉起、D-Bus/DDS/HTTP验证及四类故障自愈），在独立Docker容器沙箱（`TWIN-11_run_175931`）中完成100%验证，取得独立Codex QA与ARCH审签APPROVED闭环；
8. **TWIN-12（VMware应用孪生与真实MCU独立验收）**：已完成真实硬件在环（HIL）双开发板串口贯通实测（MC 7.51ms, TH 8.49ms <= 10ms，加热占空比恒为0%）、全栈微服务（FORWARD/STATE/UI Gateway）在VMware Ubuntu宿主常驻部署与优雅生命周期守护、D-Bus与Fast DDS跨进程低时延协同、HTTP REST与即时采样单调世代号递增（3->5），修复fastcdr未激活union内存拷贝跨环境ABI漏洞，在独立Docker容器沙箱（`TWIN-12_run_190452`）中完成100%验证，取得独立Codex QA与ARCH双审签APPROVED闭环；
9. **TWIN-17（本地离线作业引擎与基础混色执行规划）**：已完成离线作业流式解析引擎、开始/暂停/恢复/取消状态机完整实现、4通道供料混色权重规范契约（0~10000基准，0.01%分辨率，FEAT-COL-001）、M112瞬时熔断急停、纯静态配置与绝对零动态堆内存分配，自研函数全部≤35行，在独立Docker沙箱（`TWIN-17_run_202502`）中完成C11/C++17双严苛编译器构建验证与6/6单元测试全通，取得独立Codex QA与ARCH双审签APPROVED闭环；
10. **TWIN-18（双MCU运动/调平/断料状态接口调查与协议对账）**：已采掘完成MC (AT32F435) 与TH (AT32F423) 底层运控与传感接口规范（SPEC-MCU-MOTION-LEVELING-FILAMENT-20261029.md，涵盖CoreXY 9轴架构、`st_get_position` API、5×5双线性调平网格与7×7产品差距以及断料检测去抖机制），严格分离纯软件开发与实机台架验收，取得独立Codex QA与ARCH双审签APPROVED闭环；
11. **TWIN-19（全机HMS错误码体系、双级急停联动与安全快照导出）**：已完成全机HMS 24类分级错误码体系（0x1000 COMM, 0x2000 THERMAL, 0x3000 MMU含0x3001断料, 0x4000 MOTION, 0x5000 SAFETY）、双级急停联动管理与安全互锁（Level 1软急停保温停进给，Level 2硬急停断开强电并强制人工特权复位）、一键脱敏诊断导出工具（export_diag_pack.py）及敏感凭据100%正则脱敏，自研函数全部≤39行，在独立Docker沙箱（`TWIN-19_run_202545`）中完成7/7单元测试与反向泄露断言测试全通，取得独立Codex QA与ARCH双审签APPROVED闭环；
12. **TWIN-20（HMI料槽映射、新机检查引导、国际化与局域网发现）**：已完成4通道供料耗材调色板映射与TWIN-17 10000基准混色联动、OOBE 5步新机开箱向导（硬件脱机状态真实性防伪，绝无全绿假通过）、中英双语动态免刷新切换与深浅高对比度主题切换（800x480触摸屏优化，按钮min-size>=44px）、纯C轻量级mDNS局域网服务广播器（_aisoc._tcp.local:8080，零堆内存分配，自研函数≤36行），在独立Docker沙箱（`TWIN-20_run_210206`）中完成C11/C++17双严苛编译器构建验证与4/4测试全通，HMI契约测试6/6全通，取得独立Codex QA与ARCH双审签APPROVED闭环。

当前释放下游就绪任务，COORD将按依赖接续调度推进。最多两张实现卡并行；实际会话、前置接受、写白名单、隔离输出、租约与资源待Ready前落实。台架/串口/探针只登记一名实际操作者，CLI不能与常驻FWD抢UART。QA独立Codex、QA作者产物由非作者ARCH复核；COORD按准确候选收件，不因结构exit0自动推进。

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
