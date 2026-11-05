---
title: SoC公共看板
version: 29
status: current-planning
owner: COORD
updated: '2026-11-05T11:13:30+08:00'
plan_revision: vmware-soc-twin-20261029
execution_mode: 任务状态只以原卡为准；计划岗位和别名不表示运行
---

# 当前任务看板

当前接续为[VMware→SoC两阶段孪生任务](../../docs/planning/vmware_soc_twin_task_execution_20261029.md)。共111张有效卡，18张工作包不直接派发；另6张superseded V2历史卡不计入。旧卡状态/阻塞保持，历史签署只适用原版本。根目录旧`.agents`不作正式状态源。

| 类别 | 数量 | 实际状态投影 |
| --- | ---: | --- |
| AUTO | 4 | Done 4 (AUTO-03, AUTO-04, AUTO-05, AUTO-06) |
| CR | 15 | Backlog 1、Done 14 |
| MCQ | 2 | Done 2 |
| MS | 22 | Backlog 20、Done 1、Verify 1 |
| PL | 2 | Done 2 |
| TASK | 18 | Backlog 18 |
| TEMP | 7 | Done 7 |
| TWIN | 30 | Backlog 4、Done 26（含人为冻结3） |
| V2 | 20 | Done 20 |

## 当前顺序与责任

前置任务[TWIN-01](microtasks/vmware_soc_twin/TWIN-01.md)至[TWIN-12](microtasks/vmware_soc_twin/TWIN-12.md)、[TWIN-17](microtasks/vmware_soc_twin/TWIN-17.md)至[TWIN-25](microtasks/vmware_soc_twin/TWIN-25.md)、[TWIN-29](microtasks/vmware_soc_twin/TWIN-29.md)及[TWIN-30](microtasks/vmware_soc_twin/TWIN-30.md)卡面均为Done；其中TWIN-26已按用户指令执行人为冻结（blocked: true），TWIN-13/TWIN-14亦按不具备SoC迁移条件指令执行人为冻结（blocked: true），其接受范围以各卡绑定候选和证据为准，TWIN-01仍须遵循[交付门禁](../rules/delivery_and_coord_gate.md)登记的疑点和消费限制。
- [TWIN-30](microtasks/vmware_soc_twin/TWIN-30.md)（VMware全流程离线打印闭环集成验证与首版收件）：【已闭环 Done】承接首版本地正常打印闭环目标（U-D02）与纯逻辑空跑底线（选项 A / U-D03），完成全流程闭环集成测试套件开发与端到端在环串联：验证未回零硬拦截与 G28 归零、选项 A 4条加热指令 0% 强电锁死安全推进、CoreXY G0/G1 微米走线与 MC 0x16 20B 报文反向同步、多通道混色调度、HMS 0x3001 断料瞬时安全挂起与恢复、M112 急停瞬时熔断与自锁复位、128B 权威快照原子导出与 100% 收敛态、双 MCU 固件版本 4 态衰退模拟；C11/C++17 8/8 集成套件 100% 通过，两组独立沙箱（QA / ARCH）全绿验证，独立 Codex QA 与 ARCH 双重 APPROVED 收件；
- [TWIN-23](microtasks/vmware_soc_twin/TWIN-23.md)（VMware离线G-code作业流式空跑与运控执行器实现）：【已闭环 Done】承接首版本地正常打印闭环目标（U-D02）与选项 A 台架底线要求（U-D03），已完成离线 G-code 流式读取、选项 A 强电 0% 过滤、CoreXY 走线调度、HMS 0x3001 断料联锁与 M112 急停熔断；C11/C++17 8/8 单测与 6/6 回归测试 100% 通过，两组独立沙箱（QA / ARCH）全绿通过，独立 Codex QA 与 ARCH 双重 APPROVED 收件；
- [TWIN-21](microtasks/vmware_soc_twin/TWIN-21.md)（MC固件0x16坐标查询与运动指令响应）：已完成0x16 20B微米整型对账、栈溢出根除与强电0%锁死，服务器沙箱100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-22](microtasks/vmware_soc_twin/TWIN-22.md)（AP端温控倍数换算与故障哨兵防御性治理）：已完成deci_c至milli_c统一换算（解决TWIN-12 245.0℃ vs 24.5℃冲突）、故障哨兵输出null与降级，服务器沙箱11项单测100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-24](microtasks/vmware_soc_twin/TWIN-24.md)（MC固件5×5调平网格导出0x18响应实现）：落实U-D04裁决，基于固件存量5×5双线性网格导出52B载荷，缓冲区扩至128B，双独立Docker沙箱100%通过，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-25](microtasks/vmware_soc_twin/TWIN-25.md)（AP端0x18调平网格解析与设备状态拓扑呈现）：承接TWIN-24下位机网格数据，提供D-Bus/HTTP-SSE/Web HMI拓扑状态呈现，双独立Docker沙箱16项单测全通，独立Codex QA与ARCH复核APPROVED收件；
- [TWIN-13](microtasks/vmware_soc_twin/TWIN-13.md)（SoC平台迁移与实板候选交接）：因不具备SoC迁移条件，涉及平台迁移部分按用户指令【人为冻结】（blocked: true），首版打印闭环改为在VMware孪生环境上验证；
- [TWIN-14](microtasks/vmware_soc_twin/TWIN-14.md)（SoC实屏实板独立验收与阶段二收件）：按用户指令【人为冻结】（blocked: true），首版验收基于VMware环境完成；
- [TWIN-26](microtasks/vmware_soc_twin/TWIN-26.md)（双MCU固件升级通道与Bootloader IAP协议复用对账）：已按用户指令【人为冻结】（blocked: true）。虽双独立Docker沙箱6大测试全通、独立Codex QA与ENG-MC完成复核，但遵照人工指示严格保持冻结状态，严禁下游自动消费；
- [TWIN-27](microtasks/vmware_soc_twin/TWIN-27.md)（AP端VMware指定目录固件扫描与安全准入服务实现）：因前置TWIN-26被人为冻结，本任务保持Backlog且标记blocked: true，不派发、不推进；
- [TWIN-28](microtasks/vmware_soc_twin/TWIN-28.md)（端到端真实双MCU固件升级在环联调与验收）：保持Backlog且标记blocked: true，待上游解冻后按流程推进；
- [TWIN-29](microtasks/vmware_soc_twin/TWIN-29.md)（AP端双MCU真实固件版本查询链路与时序衰退状态机实现）：落实用户高优先级固件版本展示指令，实现0x01/0x02版本帧组帧与解析、device_manager双端版本拓扑与FRESH/STALE/OFFLINE/FAILED四态时序衰退，服务器沙箱23/23测试全通，独立Codex QA与ARCH复核APPROVED收件；

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
12. **TWIN-20（HMI料槽映射、新机检查引导、国际化与局域网发现，含真实双MCU固件版本呈现）**：已完成4通道供料耗材调色板映射与TWIN-17 10000基准混色联动、OOBE 5步新机开箱向导、中英双语动态免刷新切换与深浅高对比度主题切换、纯C轻量级mDNS局域网服务广播器（_aisoc._tcp.local:8080）；在Revision 2中全面落实用户高优先级指令，主界面Sensors卡片与OOBE Step 3接入真实双MCU（MC与TH）固件版本（v{major}.{minor} 0x{git_commit}），支持ONLINE/STALE/OFFLINE/QUERY_FAILED/UNKNOWN五态时序防御映射，绝对零假数据/零硬编码伪造，在独立Docker沙箱中完成100%构建与自动化契约测试（7/7用例全通），取得独立Codex QA与ARCH双审签APPROVED闭环。
13. **2026-11-05收件（`ISS-20261105-001`～`003` / `DEM-20261105-001`～`003`）**：【已全部闭环 Done】由ARCH完成只读根因调查与架构任务拆解（`soc_ap_build_and_startup_issues_arch_breakdown_20261105.md`，`revision: 4`），[TWIN-51](microtasks/vmware_soc_twin/TWIN-51.md)（`INTEGRATOR`：修复`test_backoff.cpp`在GCC 15下的`-Werror=maybe-uninitialized`编译阻断，独立Codex QA `01a1a999-e8d7-7cb3-ad5e-61e0dd08e72c` `APPROVED`）、[TWIN-52](microtasks/vmware_soc_twin/TWIN-52.md)（`ENG-DDS`：Fast-CDR 2.2.5 `optional`未初始化拷贝崩溃补丁固化与`third_party/build.sh`可重现构建，独立Codex QA `01a1a9ad-5a37-7bb3-9835-4ed9ce0a308b` `APPROVED`）、[TWIN-53](microtasks/vmware_soc_twin/TWIN-53.md)（`INTEGRATOR`：加固`deploy_twin.sh`后台守护进程会话隔离、`SIGHUP`免疫与四进程存活探针，独立Codex QA `01a1a9ae-e883-7270-8cdd-358b3b47aed9` `APPROVED`）全部在服务器独立Docker沙箱与独立Codex QA审查下通过并同步至VMware实机环境。

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
