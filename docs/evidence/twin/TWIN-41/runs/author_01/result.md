# TWIN-41 架构拆解阶段端到端单功能全流程闭环梳理与协议映射自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-41` (架构拆解阶段端到端单功能全流程闭环梳理与协议映射) |
| **所属工作包** | `TASK-010` (架构权威规范与多模块集成闭环基准) |
| **执行角色** | `ARCH` (系统架构师) |
| **协同角色** | `ENG-MC`, `ENG-TH`, `ENG-FWD`, `ENG-STATE`, `ENG-UI`, `INTEGRATOR` |
| **交付成果** | `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md` |
| **自检结论** | **100% PASS (10 大垂直切片功能全覆盖，7 大架构维度无死角穿透，铁律硬门禁 100% 合规)** |

---

## 1. 任务背景与核心架构目标

在多模块复杂分布式嵌入式系统（SoC + 双MCU + 浏览器HMI）开发过程中，经常出现因架构拆解粗放、缺乏单功能端到端纵向贯通而引发的系统级通病：
1. **各模块自说自话**：上位机基于本地时钟假自增进度与假走线，下位机执行失步或中断无法同步反馈；
2. **“发后即忘”开环失控**：指令下发缺乏显式硬件 ACK 事务回溯，肆意滥用 `no_reply=TRUE`；
3. **异常吞没与隐蔽截断**：底层掉线、丢包或报错以裸错误码或假成功掩盖，缺乏全局可追溯的结构化上下文。

针对上述痛点，本任务严格践行用户提出的核心方法论——**“在多模块系统集成的时候，得一个功能一个功能的梳理全流程。架构拆解的时候也得考虑”**，编制了系统级端到端单功能全流程闭环时序与协议映射权威规范矩阵。

---

## 2. 交付成果内容与 10 大核心功能覆盖核验

本次编制的规范文档位于 `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md`（共 784 行，结构化 Markdown）。全面覆盖了整机系统首版运行所必需的 10 大核心垂直切片功能：

1. **功能 1：喷嘴/热床双温遥测与固件心跳 (Nozzle/Bed Telemetry & Firmware Heartbeat)**
   - 梳理 L5 $\leftrightarrow$ L4 $\leftrightarrow$ L3 $\leftrightarrow$ L2 $\leftrightarrow$ L1 完整 1Hz/5Hz 周期性双温轮询与探活流；
   - 规范 `CMD_TEMP_QUERY (0x14)`、`CMD_PING (0x03)` 与上行响应帧 `0x14`、`0x04`；
   - 约束 100ms 超时与 2 次退避重试，3s 老化衰退及 `0x7FFFFFFE` 哨兵温度打入机制。
2. **功能 2：CoreXY 触控微步 Jog 运控 (Jog Motion)**
   - 梳理前后端交互与点动防呆（单在途请求禁用机制）；
   - 规范 `CMD_MOTION_MOVE (0x15)` 载荷微米坐标结构及与 MC Marlin CoreXY 规划器的匹配；
   - 确立 **“相对位移严禁盲目重发”** 核心禁令，规范通过 `0x16` 坐标查询对账的故障恢复路径。
3. **功能 3：全轴归零 G28 (Homing All / XY)**
   - 梳理限位触碰、慢速复触与绝对坐标系原点建立过程；
   - 规范 `CMD_HOME_AXES (0x17)` 与 20 字节 `minimc_pos_report_payload_t` 响应；
   - 标定 30 秒超时预算，确立归零失败严禁盲重试的防撞机硬隔离。
4. **功能 4：5x5 自动调平网格校准 G29 (Mesh Bed Leveling)**
   - 梳理 25 个物理测点探测时序与 `CMD_LEVEL_GRID_QUERY (0x18)` 交互；
   - 规范 52 字节网格载荷（`int16_t z_offset_um[25]`）在线缆传输中的端序与换算度量；
   - 标定 120 秒超时预算与探针重试逻辑。
5. **功能 5：打印作业流流式下发与执行推进 (Job Execution Pipeline)**
   - 梳理 G-code 流式下发、Marlin 规划器缓冲信用流控与逐行确认推进；
   - 严格杜绝本地开环定时器假自增，作业推进与行号自增 100% 绑定硬件物理 ACK；
   - 规范链路中断瞬时切换 `PAUSED`、行号与进度绝对锁死的 Fail-Closed 机制。
6. **功能 6：4 通道混色配置与权重校验 (4-Channel Filament Slots & Mixing Ratio)**
   - 梳理前端色盘配置、网关 `slot_schema.json` 强校验与下位机配置同步；
   - 严格执行 **“总权重必须绝对等于 10000”** 不变量，非法权重直接报 400 阻断；
   - 规范下行 `CMD_SET_MIXING_RATIO (0x32)` 及从控执行确认。
7. **功能 7：紧急急停 E-STOP 注入与硬锁存 (Emergency Stop & Reset)**
   - 梳理最高优先级广播时序（`FLAGS_IS_PRIORITY = 0x10`）；
   - 规范硬件中断级强电切断（加热 MOS PWM 0%、电机驱动 Disable）；
   - 规范 50ms 极限超时、3 次密集重发与必须显式 Clear 复位的硬锁存安全机制。
8. **功能 8：全机 HMS 错误码上报与严重度分级 (HMS Error Reporting & Severity)**
   - 梳理工具头断料开关（PD2）到 AP 的 `CMD_ALARM_EVENT (0x50)` 上报及 AP 回显 ACK 闭环；
   - 规范 16-bit 错误码体系（`0x1000`~`0x5000`）及四级严重度（INFO/WARNING/ERROR/FATAL）；
   - 规范断料 `0x3001` 联动软暂停与全屏指引。
9. **功能 9：开箱引导向导 OOBE 硬件状态读取 (OOBE Wizard Hardware Readout)**
   - 梳理新机握手与双 MCU 真实固件版本（`CMD_GET_VERSION = 0x01`）探测流；
   - 严格执行 **“物理真实性不变量（Strict Realism Invariant）”**，未连接设备严禁虚假显示“合格”或“PASS”；
   - 规范离线时“下一步”禁用与连线后 SSE 免刷新自愈点亮。
10. **功能 10：mDNS 局域网服务发现与直连 (mDNS Service Discovery)**
    - 梳理 C11/C++17 纯静态零堆分配 `mdns_advertiser` 广播守护流；
    - 规范组播 `224.0.0.251:5353`、PTR/SRV/A/TXT 报文布局与 RFC 6762 抖动响应；
    - 规范网络拔线断开停止宣告与重连自愈。

---

## 3. 7 大架构维度贯通深度核验

针对上述 10 大功能，文档对每个功能均按标准章节逐一落地了以下 7 个维度的详尽规约：

| 维度编号 | 维度定义 | 规范落实情况与技术细节 |
| :--- | :--- | :--- |
| **a** | **端到端分层时序图** | 针对全部 10 个功能分别绘制了清晰完整的 Mermaid `sequenceDiagram`，垂直涵盖 L5 Web HMI $\to$ L4 UI Gateway $\to$ L3 Device Manager $\to$ L2 Forward $\to$ L1 MCU (MC/TH)。 |
| **b** | **下行协议帧与 Sequence ID 规则** | 详尽规约了 MiniMCProto 12 字节帧头字段、命令字编码、载荷大小、端序及 16-bit 模 65536 单调自增与 Stop-and-Wait 单在途事务模型。 |
| **c** | **物理硬件/MCU 执行与显式 ACK** | 明确定义了下位机物理动作（ADC采样、电机脉冲、探针触发、MOS关断）及上行响应帧结构，强调响应帧必须回显请求 `seq`。 |
| **d** | **超时预算与重试策略** | 为每个功能明确标定了具体超时数值（如 Query 100ms, Jog 2000ms, Homing 30000ms, Leveling 120s, E-Stop 50ms 等），并对相对位移与归零下达了严禁盲重试的指令。 |
| **e** | **结构化报错抛出链条 (Rule 7)** | 100% 落实 Rule 7 门禁，所有异常必须携带四元组 `{target_node, sequence_id, elapsed_ms, error_code}`，杜绝匿名裸日志，标明逐层透传至前端 Toast 的完整路径。 |
| **f** | **Fail-Closed 降级与阻断** | 详尽规约了物理断线 3s 内的状态机衰退、哨兵温度 `0x7FFFFFFE` 注入、UI 格式化 `--.- °C` 阻断、HTTP 503 拦截、作业行号/进度绝对冻结。 |
| **g** | **自愈与状态对齐机制** | 规约了重连后版本重新握手、Session Epoch 检验、坐标对齐、断点行号恢复与界面免刷新自动解禁机制。 |

---

## 4. 架构铁律与工程门禁符合性声明

1. **零开环与杜绝 `no_reply=TRUE`**：经全文档规约核查，10 大功能下行控制指令 100% 要求 `FLAGS_WANTS_ACK = 0x01` 并配对上行响应帧，彻底杜绝无应答“发后即忘”；
2. **零开环假跑进度**：打印作业推进严格以硬件 ACK 为物理准绳，链路中断时行号与进度绝对锁死，杜绝虚假自增；
3. **选项 A 强电锁死**：加热棒占空比在空跑阶段硬性锁死为 0%，拦截任何实际加热输出；
4. **C/C++ 编码规范合规**：所有新增协议结构体均定义为自然对齐或 packed 结构并带编译期静态断言，无动态堆内存分配，无多重指针黑魔法。

---

## 5. 交付资产清单与哈希校验

| 交付文件 | 文件类型 | 行数 | SHA-256 校验和 |
| :--- | :--- | :--- | :--- |
| `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md` | 架构矩阵权威规范 | 784 | `8a117ada12634bf342541ec9130bfd100426fb95569758cddb010c5372abe59d` |
| `project-control/docs/evidence/twin/TWIN-41/runs/author_01/result.md` | 自检与交付总结报告 | 本文件 | *(见 Git 提交审计)* |

---

## 6. 结项声明

经 `ARCH` 角色严谨编制与全维度核验，微任务 `TWIN-41` 已全面达成所有设计目标，形成了统领整机集成的权威架构矩阵规范，正式提交版本控制并移交 QA 审计。
