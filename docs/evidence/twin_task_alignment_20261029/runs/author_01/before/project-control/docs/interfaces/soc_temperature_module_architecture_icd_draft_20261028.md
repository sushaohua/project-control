---
id: ARCH-SOC-TEMP-ICD-20261028
title: SoC 温度遥测多模块架构与通信契约提案
revision: 2
status: draft-pending-independent-review-and-owner-acceptance
author_role: ARCH
date: 2026-10-28
scope: 两阶段应用孪生开发中的双端只读温度切片；独立显示与真实跨进程通信提案
---

# SoC 温度遥测多模块架构与通信契约提案

## 1. 目的、证据与使用条件

本提案为 FORWARD → STATE → 展示客户端设计首个可评审的 SoC 多模块接口，并明确部署、唯一控制路径、资源、故障和分阶段验收。`draft` 表示供相关 Owner 与独立 QA 评审，不替代已登记的 TEMP-01 签署，也不自行冻结协议或改变任务状态。

**revision 2（2026-10-29）变更**：依据用户明确的[VMware→SoC两阶段孪生要求](../planning/vmware_soc_twin_development_plan_20261029.md)，替代revision 1“先同进程CLI、以后拆进程/接UI/IPC”的候选选择。阶段一就需按接受的目标服务边界运行实际模块、进程管理、真实IPC与可见界面；阶段二复用源码、契约及界面并集中适配平台。旧QA/ARCH报告各自只适用于其记录的准确对象、哈希与结论，详见[历史审阅索引](../evidence/soc_temp_arch_20261028/README.md)：QA01审阅的草案哈希为`6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5`并拒绝，QA02审阅的修订草案哈希为`0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae`，ARCH报告分别绑定各自记录的QA报告。历史原件保留，不自动批准本revision。

输入及本次观察的 SHA256（输入含未提交文件，实际消费时重新核对）：

| 输入 | SHA256 / 状态 |
| --- | --- |
| [正式 MiniMCProto Rev 2.0.3](../specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md) | `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54` |
| [PL-01 温度范围](../planning/product/next_increment_scope_pl01.md) | `fc95bd769829d629ebdb12ef1a2df3b3d420bfb8006a18975a20b50741c7ec89`；文档记录用户选择方案 A；签署证据由 COORD 对账 |
| [PL-02 温度设计](../planning/product/next_increment_design_pl02.md) | `75f3512b80a72266aa1bd0f53ee7fe1b523ac4179396f3261a307e85a18bd30a` |
| [TEMP-01 板端遥测 ICD](ap_mc_th_telemetry_icd.md) | `74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d`；已记录 Done/审签，但存在下文冲突 |
| [通信角色边界](../../.agents/rules/06_通信工程师职责与接口边界.md)、[角色定义](../../.agents/rules/02_模块与Agent职责.md)、[重排](../planning/workflow_replan_20261028.md) | 以仓内准确文件为输入，不将岗位视作运行中的会话 |

revision 1编写时TEMP-02、TEMP-04卡记录InProgress；这是日期化观察，不作为当前状态。当前各TEMP卡及真实证据由COORD核对，本提案不编辑其实现或假定实施者已收到发现。温度实际硬件和CR-09～11的组合证据仍须按准确候选对账。已有主机查询、MiniMCProto与串口代码，不据此声称常驻STATE、DDS、D-Bus或真实显示已实现。

## 2. 需要立即协调的协议冲突

以下是源码/文档对照发现，须交 COORD、TEMP-01 作者及 ENG-FWD/MC/TH 和独立 QA 处理；涉及冲突字段的实现与验收不应继续依赖未经澄清的值。保留历史签署，由 COORD 按规则登记影响、消费限制及新候选，不由本文改写 Done。

| 编号 | 已观察到的冲突 | 处理方向与必要接受 |
| --- | --- | --- |
| C1 | 正式协议 §5.1 规定所有 v2 帧必须叠加 `0x04`；TEMP-01 ICD 的请求/响应 flags 分别只写 `0x01`/`0x02`，PL-02 又写 flags=0 | 帧层以正式协议为依据，候选请求 `0x05`、响应 `0x06`；由协议 Owner 和三端复核其他位/路由，重做双向黄金帧及 CRC；未接受前不宣称已修复 |
| C2 | PL-02 使用无符号 `current_temp_c_x10`；TEMP-01 ICD/共享头使用有符号 `current_temp_centi_c` | 不自动选赢家；决定表示法、最小/最大值、非法值、量化和兼容策略，统一头文件、三端、独立向量和文档 |
| C3 | TEMP-01 使用 int16 的 0.01°C 并声称可到 +350°C（35000），超出 int16 最大 32767；`0x7FFF` 又用作故障值 | 选择有足够范围的编码或单位，验证负温、边界、故障哨兵不会碰撞；仅结构尺寸断言不能证明范围正确 |
| C4 | PL-01 一处禁止温度占用 `0x10`，另一处建议使用它；正式协议 `0x10` 为系统控制、`0x40` 为 36 字节单向综合遥测 | `0x10` 不可复用，`0x40` 不可直接当新的查询命令。TEMP-01 提议 `0x14` 作为扩展，须确认命令空间和请求/响应语义、修订与兼容性，由 ARCH/各端及 QA 接受；不把本文写成新分配 |
| C5 | TEMP-01 的 ADC 12 位、开短路阈值、采样时钟和加热关断写作确定事实 | 对照原理图、传感器和两端实现，核量程、阈值、失效极性、启动/复位及失电行为；故障注入与强电输出由硬件负责人确认。不能用上报 duty=0 证明物理输出为零 |
| C6 | PL-01 写 TH RTT ≤10 ms；现有运行资料与 VMware 调度波动不足以证明硬实时边界 | 将其视为待批准目标，先明确测试样本、负载、分位数、测量起止/环境及失败动作，再由相关 Owner 和 QA 决议；不得靠平均值或单次成功作保证 |

板端 MCU 消息语义仅以受影响各方接受后的准确 ICD 为准。本文的 SoC 内部模型独立表达“值/单位/状态”，不能把本文当成 MCU 字节布局。

## 3. 目标范围与部署选择

**本切片按目标结构在VMware阶段运行独立服务及显示**：候选进程为forward-service、device-manager（STATE）、ui-gateway和浏览器HMI；FORWARD独占UART，STATE维护权威快照，UI经网关消费真实状态。具体边界与D-Bus/DDS映射仍需ARCH、FWD、STATE、UI、NET、通信Owner、INTEGRATOR及QA接受，但第一阶段不能用另一套单进程/假数据实现替代已接受的目标结构。

```mermaid
flowchart LR
  subgraph VM[VMware第一阶段 / SoC第二阶段：同构应用]
    UI[独立浏览器显示] <-->|HTTP / SSE| WEB[ui-gateway进程]
    WEB <-->|D-Bus快照及业务方法| STATE[device-manager进程: STATE]
    STATE -->|D-Bus有界采样请求| FWD[forward-service进程: 唯一UART Owner]
    FWD -->|DDS原始遥测| STATE
    STATE -->|DDS权威状态| WEB
  end
  FWD <-->|115200 8N1| MC[MC: 热床采样 / 透明路由]
  MC <-->|921600 8N1| TH[TH: 热端采样]
```

| 单元 | 职责和数据所有权 | 边界 |
| --- | --- | --- |
| FORWARD / ENG-FWD | UART 打开/关闭、帧校验、一次一个在途事务、请求关联、超时及重连；发布每端原始测量结果 | 不生成设备温度、不修改 TH 业务帧；错误独立返回 |
| STATE / ENG-STATE | 两个端点各自状态、最新成功值、新鲜度、故障/链路状态、健康快照 | 不访问 UART；不能将旧值标为新值，也不通过遥测判定硬件安全 |
| UI / ENG-UI | 独立浏览器显示、输入与导航，经ui-gateway展示权威快照及质量 | UI不访问UART；不能造数或将旧缓存标为实时；界面退出不影响后台采集 |
| ui-gateway / ENG-NET，与UI协作 | 浏览器HTTP请求到STATE业务API的映射、真实状态的SSE推送、前端资源提供 | 不成为第二状态权威；阶段一/二使用同一Web/API实现，权限按契约配置 |
| INTEGRATOR | 负责打包、配置、系统服务启动、重启策略与日志目录 | 服务配置/资源由具体候选确认；当前无 systemd 部署实现 |

启动：服务管理器按统一服务清单启动基础IPC、FWD/STATE、UI网关及显示；服务就绪和设备数据健康分开。STATE初始两端UNKNOWN，FWD打开串口失败时DISCONNECTED并有限退避；UI可显示初始化/不可用状态，不等待正常样本才能启动。关闭时停止新请求，调度器在有界期限内终止在途事务并关闭UART。各服务崩溃按统一生命周期重启，按进程代次重建关联；缓存失效后须取得新有效样本才恢复FRESH。UI/网关重启不代替FWD或设备重启。

两阶段保持同一应用源码、服务边界、schema和逻辑依赖；工具链/sysroot、设备名、路径、地址、服务账户及启动适配集中配置。平台输入未明不承诺只换编译器即可成功，目标SoC上独立验证BSP、驱动、实屏与资源/性能。改变拓扑或IPC时须有ADR和兼容/故障测试，不能迁移时悄悄改写业务架构。

## 4. SoC 内部语义契约（候选 v1）

实际 API 名称、编程语言 ABI、生命周期与并发策略进入实现票时由 Owner 明确。下表是可评审的逻辑数据模型，不是新 MCU 协议或已冻结代码接口。

| 字段 | 类型和单位 | 生产者 / 约束 |
| --- | --- | --- |
| `schema_version` | 无符号整数，初始提案 1 | STATE；不兼容变更使用新版本 |
| `source` / `sensor` | `MC/BED` 或 `TH/TOOL` | FORWARD 从匹配的端点和已接受载荷映射；不根据猜测推导 |
| `temperature_millic` | 有符号整数，0.001°C；另有 `has_temperature` | 仅采样有效时存在；转换需溢出检查，非法/故障不能用 0 代替 |
| `sensor_status` | OK、OPEN、SHORT、ADC_TIMEOUT、UNKNOWN | 只有正式硬件契约可证明时映射 OPEN/SHORT；否则 UNKNOWN；不得从断链推断传感器开路 |
| `quality` | UNKNOWN、FRESH、STALE、FAULT | STATE 按后述规则维护，值与来源分开 |
| `raw_adc` | 可选无符号整数；无效时 `has_raw_adc=false` | 原始计数及 ADC 位宽/标定版本仅在端侧证据支持时发布 |
| `source_sample_tick_ms` | 可选端侧 uint32 单调 tick | 来源设备自己的时钟，允许回绕；无 boot epoch 和时钟关联时不能推算绝对采样年龄 |
| `host_received_monotonic_ns` | AP 单调时钟，表示有效帧收齐时刻 | 仅进程本次生命周期内可比较；跨主机/重启不比较 |
| `request_seq` / `generation` | 请求关联号 / AP 进程代次 | seq 仅用于本次在途事务；进程重启、seq回绕须重置关联环境 |
| `last_error` | NONE、LINK_DOWN、TIMEOUT、BAD_FRAME、BAD_RESPONSE、SENSOR_FAULT、INTERNAL | 可区分通信与传感器故障；字段与日志不得制造硬件事实 |

提议语义接口：`RequestSample(source, request_id) → accepted/busy/not_ready`只接受调度，跨进程映射到D-Bus；关联结果由FWD发布真实采样/事务事件，STATE消费后通过DDS发布权威状态；`GetSnapshot() → Snapshot(MC, TH, generation)`供网关经D-Bus补取快照，浏览器经HTTP读取并通过SSE持续更新。实际签名、schema、订阅/服务消失、快照与增量顺序及代次恢复须冻结和测试。进程内回调可作为SDK内部实现，不能代替跨进程验收；唯一调度器串行采样，不能为多个页面重复打开UART或无限排队。

状态转换：初始 UNKNOWN；收到来源/flags/cmd/seq/长度/CRC 均符合已接受协议的有效样本后 FRESH；采样故障 FAULT；通信断开或采样失败显示对应错误并保留最后值及其旧时间（标记 STALE 或 UNKNOWN），超过 `max_age` 为 STALE；只读输出必须同时显示质量，不把旧值当实时值。是否允许显示最后有效值由 UI 标记“上次值”。`max_age` 以 host 单调接收时间计算，仅约束接收后经过时间；未经设备时钟关联，不证明传感器采样本身足够新。周期、响应超时和 max_age 由正式部署配置给定，现阶段未冻结。

TEMP-01 当前编码到内部状态的候选映射如下，仅供修订双方契约时使用：`0x00→OK`、`0x01→OPEN`、`0x02→SHORT`、`0x03→ADC_TIMEOUT`；其他值→`UNKNOWN` 和 `BAD_RESPONSE`，不得显示为有效温度。端侧超时是传感器采样失败，链路 TIMEOUT 是未取得符合事务关联的响应，二者不能互换。传感器故障时温度无效；异常状态与有效值矛盾的帧按 `BAD_RESPONSE` 处理。三端 Owner/QA 须在新 ICD 用精确数值、单位和反例确认该映射。

## 5. DDS 与 D-Bus：阶段一实际IPC的候选契约

显示独立且两阶段进程同构使本切片需要真实跨进程通信；以下是TASK-013/014/015可评审的命名和数据草案，不是现有服务或已批准ABI。使用本图映射时，第一阶段就应冻结并实现相应中间件版本、IDL/XML、QoS、安全权限和主机部署预算；目标预算可单独待核，不把无关未来Topic作为当前前置。

| 方向 | 候选接口 | 权威发布者 / 消费者 | 语义与待决 |
| --- | --- | --- | --- |
| DDS 状态 | `soc.device.temperature.v1`，IDL 类型 `TemperatureSampleV1`；字段对应第4节 | STATE 单一发布者；UI/NET 等订阅 | `source`+`sensor` 标识实例；状态最新值、质量和 host 单调时间；跨主机不得比较单调时间。可靠性、deadline、history/depth、资源上限和晚加入策略均须按目标系统测量及批准 |
| DDS 原始采样 | `soc.raw.temperature.v1`，类型 `RawTemperatureV1` | FORWARD 发布；STATE 消费 | 当前候选布局需此通道，包含事务/样本关联与错误；消息不可冒充DeviceState，schema/QoS和有界资源同上 |
| D-Bus 只读 | 候选 bus `org.project.DeviceState`，object `/org/project/DeviceState`，interface `org.project.DeviceState1`；`GetTemperatureSnapshot()` | STATE 服务；CLI/UI 读取 | 返回版本化、按端点分组的第4节语义；XML签名、错误名、超时和权限待 ARCH/DBUS/STATE 接受；服务消失返回明确不可用，不回填旧值为新值 |
| D-Bus 配置 | 暂无本切片方法 | 不适用 | 配置写入、OTA、启停和加热控制不在当前切片；需要时独立契约及授权 |

DDS 状态不得绕过 STATE 产生第二权威；传输成功不表示设备动作完成。XML 和 IDL 未冻结前不生成生产绑定；下一步按上表形成正式机器可读文件并测试兼容/错误路径。

候选 D-Bus 方法签名草图（未经各方接受，命名及稳定 ABI 待定）：

```xml
<interface name="org.project.DeviceState1">
  <method name="GetTemperatureSnapshot">
    <arg name="schema_version" type="u" direction="out"/>
    <arg name="generation" type="t" direction="out"/>
    <arg name="samples" type="a(yybiyybubutbq)" direction="out"/>
  </method>
</interface>
```

每条 tuple 依次为 `source:u8, sensor:u8, has_temperature:bool, temperature_millic:i32, sensor_status:u8, quality:u8, has_raw_adc:bool, raw_adc:u32, has_source_tick:bool, source_tick_ms:u32, host_received_monotonic_ns:u64, has_request_seq:bool, request_seq:u16`。建议 source `1=MC,2=TH`，sensor `1=BED,2=TOOL`，状态枚举的数值及 `last_error` 扩展、未知枚举行为须在冻结 XML/IDL 前确定。调用超时、权限拒绝、服务消失及格式不兼容分别形成标准错误；具体错误名称、期限、访问策略待接受。`host_received_monotonic_ns` 只在同一主机和 generation 下可比较，不具备跨主机绝对时间含义。

候选 DDS IDL 字段骨架：

```idl
module soc { module device {
  struct TemperatureSampleV1 {
    unsigned long schema_version;
    unsigned long long generation;
    octet source; octet sensor;
    boolean has_temperature; long temperature_millic;
    octet sensor_status; octet quality;
    boolean has_raw_adc; unsigned long raw_adc;
    boolean has_source_tick; unsigned long source_tick_ms;
    unsigned long long host_received_monotonic_ns;
    boolean has_request_seq; unsigned short request_seq;
    unsigned long last_error;
  };
}; };
```

此草图的 `last_error` 尚未并入 D-Bus tuple，两个协议在发布前必须补齐相同语义及固定枚举；不能把草图直接作为生成绑定。DDS 实例键、QoS、兼容和终端编码由 TASK-013 接受。实际 serial wire payload 仍以新板端 ICD 为准。

## 6. 唯一控制路径（未来动作，非当前授权）

```text
UI / LAN / MQTT → NET（认证、授权、格式转换）→ STATE（准入与仲裁）
→ JOB（作业语义与执行状态）→ FORWARD（有界事务）→ MC/TH
```

本地 UI 可直连同一 STATE 业务接口；网络入口须先经 NET。动作请求必须带唯一 `command_id`、来源、授权上下文、期限和幂等规则；所有通道进入同一裁决点。进程内部传输和 DDS/D-Bus 适配层都不得直接调用串口或绕过 STATE。安全停机/急停路径需单独设计和硬件职责确认，不推定一般队列延迟可满足安全要求。

结果分开：`RECEIVED`（入口收到）、`ACCEPTED`（业务准入）、`SENT`（实际发送）、`DEVICE_ACK`（设备协议确认）、`COMPLETED`（依业务和设备证据确认物理动作）、`FAILED/UNKNOWN`。超时或进程重启后若物理结果未知，记录 UNKNOWN 并查询/人工处理，不自动重试非幂等动作。该状态机是待接受的后续控制契约，当前温度只读不实现动作或宣称完成。

## 7. 资源、故障和配置边界

| 项目 | 可实施的初始策略（提案，非实测承诺） | 验证/待确定 |
| --- | --- | --- |
| 在途请求 | 整个 UART 同时最多 1 个；MC、TH 轮询由同一调度器串行 | 确认正式协议/固件接受及超时后旧响应不匹配新请求 |
| 状态缓存 | 两端各 1 份最新状态；变化通知有界，可合并中间状态但不可静默丢故障状态 | 明确锁/队列所有权及慢消费者统计；无无限积压 |
| 排队与背压 | 每端最多 1 个待处理采样意图；重复请求合并或返回 BUSY，不能跨端饿死 | 验证公平、超时和取消；具体周期待配置 |
| 链路故障 | 超时、坏帧、错源/序号与掉线分别记录；坏帧和无关帧不作为本事务成功；重连限速 | 校验同次 read 中多个帧、断开/恢复、重启与序号回绕 |
| 状态与告警 | 超龄标 STALE，故障为 FAULT，重启 UNKNOWN；停止发送不改变已记录的物理事实 | 故障恢复须新成功样本；不以报警代替独立保护 |
| DDS 慢消费者 | 可丢弃过时状态并计数，但故障通知与当前故障状态须可观察 | 单独选 QoS/深度；验证重连/晚加入、资源上限 |
| 内存/CPU/延迟 | 目标硬件、负载、分位数、RSS、队列容量及统计窗口暂未确认 | 先测 VMware 基线，再在目标 SoC 测量；由 Owner/QA 共同确定可执行预算；不能用主机 RTT 推导硬实时 |

暂定工程参数必须集中配置且与 run 记录绑定；上线和 HIL 前经 Owner/QA 接受。定时器采用单调时钟，避免墙钟调整影响超时。模拟异常、软件用例、实际 HIL 分别标记与保存。

## 8. 分阶段任务与验收

不重拆已有 TEMP-01～07；由 COORD 对照影响并安排必要的契约修订或补票。通信工作包 TASK-013 为范围入口、不直接派单。

| 阶段 | Owner / 交付 | 前置和验收 |
| --- | --- | --- |
| A 冲突对账 | ARCH + ENG-FWD/MC/TH；独立 QA；给 COORD 影响清单 | 对 C1～C6 形成准确新版本、黄金帧、传感器依据和消费关系；先复核既有签署可用范围 |
| B SoC 最小契约 | ARCH + FWD/STATE/UI/NET/通信Owner/INTEGRATOR；独立 QA | 确认独立服务/显示、实际IPC、API/schema、生命周期、错误及主机配置；未用的未来通道不阻塞当前切片 |
| C 软件切片 | FWD、STATE、UI/NET、通信Owner，各自实现并有独立 QA | VMware运行真实进程/IPC/管理及界面；验双源成功、故障、错源/seq、多帧、超时、过期、单服务重启、慢消费者和限流；不以离线界面或回调替代 |
| D 组合装配与工程联调 | INTEGRATOR 和各端 Owner | 绑定 AP 和双固件、工具/配置哈希、实际部署身份、授权及候选；按真实硬件分段追踪；故障及加热输出由适当硬件人员核验 |
| E 独立 HIL 与收件 | 独立 Codex QA；QA 产物由非作者 ARCH 复核；COORD 收件 | 真实 UART 正反例、时间戳及 TX/RX 原始 Hex、真实传感器测量与独立基准对照，设备断链/恢复、开路/短路按已接受硬件方法；禁止以 Mock/PTY 替代物理回包，缺证据不通过 |
| F SoC平台迁移 | BSP + INTEGRATOR，各业务/通信/UI Owner，独立QA | 同源代码/契约/界面经目标工具链、驱动和profile部署；上板复验实屏、设备、资源性能和恢复，不能沿用VMware结果声称目标通过 |

温度范围必须包含真实传感器连接方式、测量参考及误差限、异常物理注入授权、PWM全生命周期物理隔离/检测方案；上报零值和单次读数不能证明硬件始终关闭。未确定部分先标待确认，不能编造硬件或精度指标。候选发生修改后绑定新哈希、定向重验；结果与源码恢复锁分别记录。

**阶段门和消费规则：** A/B调查与设计可并行，C消费冲突字段前须有A对应修订ICD/头文件/向量、各端Owner与独立QA的准确版本接受，经COORD收件；C实现IPC/显示前须有B对应进程/通信契约及Owner/QA接受。C各端和服务的代码/构建/独立检查绑定准确commit/diff、制品及报告SHA256，D前由INTEGRATOR/COORD核实；D稳定候选及记录收件后进入E，E通过及报告复核后按VMware阶段范围接受。F消费准确主机候选并需真实SoC/BSP、目标工具链/profile、适用授权和目标用例；不能以目标板缺失阻塞不依赖它的A～E工作。缺前置、冲突或漂移则停止对应消费，保存历史并定向修订/复验，不把旧Done当新版本放行。

**断热与代码硬门：** 按 PL-01 要求，温度增量运行的 MC/TH 固件全生命周期包含启动、复位和异常恢复时，加热 PWM 必须保持 0 且 PID 禁用或旁路。D 前由真实 MC/TH Owner 与硬件负责人共同确认隔离、输出极性、接线和物理监测方案及适用授权；D/E 分别记录部署配置、启动/复位/运行/异常恢复期间实际输出或独立物理隔离证据及其观测范围。无法证明完整生命周期时不签该项通过，不以 duty 字段或单点 0 替代。TH ADC 等适用轮询须有界超时退出并验证超时/恢复；新增自研代码和本次修改按项目 ≤50 行、≤4 参数、裸机零动态堆、指针及寄存器规范审查，遗留/第三方遵守最小修改预算；有问题交作者修复后重审。

## 9. 审阅与待决

1. COORD 通知当前 TEMP-02/04 的真实作者及 TEMP-01 Owner C1～C6，协调停止消费冲突字段并核准确在途改动；未收到回执不宣称已通知或已暂停。
2. ARCH、FWD、STATE、MC、TH、INTEGRATOR 评审接口/职责；QA 独立审查本准确文档，登记会话、模型、候选哈希、结论和报告；HUMAN/真实 MCU Owner 的必要确认不能由 QA 替代。
3. 待确认：传感器硬件/标定、精度与故障阈值；板端字段/版本；采样与陈旧期限；目标部署资源；真正需要的跨进程调用/权限；放行和故障应对方法。
4. 所有现有历史签署及本次工作区未提交内容原样保留。本提案不改变 TEMP 任务状态、源码、固件、设备或服务器。
