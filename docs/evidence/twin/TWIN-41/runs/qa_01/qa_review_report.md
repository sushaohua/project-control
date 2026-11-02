# 独立 QA 审查报告 (TWIN-41 rev 1)

```yaml
template_version: '2026-10-27'
review_id: qa-review-twin-41-01
review_status: completed
reviewer_role: QA
reviewer_roles:
  - QA
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-41
actual_session: session-qa-twin-41
author_session: session-arch-twin-41
task_id: TWIN-41
task_revision: 1
reviewed_artifact_version: project-control=001bef072dc5195ab64ef51099b0027ca6e5e413
reviewed_artifacts:
  - path: project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md
    sha256: 8a117ada12634bf342541ec9130bfd100426fb95569758cddb010c5372abe59d
  - path: project-control/docs/evidence/twin/TWIN-41/runs/author_01/result.md
    sha256: 1eb04bc46aa95e9add582feb902b7e5801a300c72de31d86c3d8449142586192
protocol_and_expectations:
  - path: project-control/.agents/rules/codex_qa_review.md
    commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
  - path: project-control/.agents/rules/c_cpp_coding_standard.md
    commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
  - path: project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
    commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
verification_environment: local-and-independent-codex
verification_scope: Document review of end-to-end feature flow closed loop matrix across 5 tiers (L5 Web -> L4 UI Gateway -> L3 Device Manager -> L2 Forward -> L1 MCU) for 10 core features, protocol and timing invariants, failure degradation, and self-healing.
required_evidence_level: document-review
review_time: '2026-11-02T10:35:00+08:00'
process_audit: passed
result_check: passed
decision: APPROVED
accepted_scope: TWIN-41 rev 1 架构拆解阶段端到端单功能全流程闭环梳理与协议映射规范文档及自检报告
limitations: []
unexecuted: []
not_applicable: []
issues: []
commands:
  - id: check_task_graph
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    exit_code: 0
  - id: verify_artifact_hashes
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: sha256sum project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md project-control/docs/evidence/twin/TWIN-41/runs/author_01/result.md
    exit_code: 0
case_results:
  - case: CHECKPOINT-1-FEATURE-1-DUAL-TEMP
    expected: Vertical slice across 5 tiers, 100ms timeout, 0x7FFFFFFE sentinel on 3s disconnect, 0% heater duty lock
    actual: L5~L1 flow complete, 0x14 CMD_TEMP_QUERY/REPORT with matching seq, 100ms timeout budget, 3s aging sentinel specified
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-2-JOG-MOTION
    expected: Vertical slice across 5 tiers, Stop-and-Wait, zero blind retry for relative motion, HTTP 503 on offline
    actual: L5~L1 flow complete, 0x15 CMD_MOTION_MOVE, dynamic timeout ~2000ms, zero blind retry strictly mandated, 503 fail-closed specified
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-3-HOMING-G28
    expected: Vertical slice across 5 tiers, 30s timeout, zero blind retry (crash prevention), axis_homed state tracking
    actual: L5~L1 flow complete, 0x17 CMD_HOME_AXES, 30s timeout budget, zero blind retry strictly enforced, is_homed cleared on disconnect
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-4-BED-MESH-G29
    expected: Vertical slice across 5 tiers, 120s timeout, 52-byte payload for 25 points, probe retry policy
    actual: L5~L1 flow complete, 0x19 CMD_TRIGGER_LEVELING and 0x18 CMD_LEVEL_GRID_QUERY, 52B int16_t[25] payload layout, probe 1-retry specified
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-5-JOB-STREAM
    expected: Vertical slice across 5 tiers, zero local fake progress ticking, progress 100% bound to hardware execution ACK
    actual: L5~L1 flow complete, 0x31 STREAM_CHUNK, credit flow control via planner_buf_free, zero local fake ticking strictly enforced, progress locked on disconnect
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-6-MIXING-RATIO
    expected: Vertical slice across 5 tiers, total weight strictly equals 10000 invariant, 400 Bad Request on violation
    actual: L5~L1 flow complete, 0x32 CMD_SET_MIXING_RATIO, slot_schema.json 10000 sum invariant enforced with HTTP 400 rejection
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-7-ESTOP
    expected: Vertical slice across 5 tiers, 0x10 priority flag, 50ms timeout, 3-burst retry, hardware MOS PWM 0% and motor disable
    actual: L5~L1 flow complete, 0x12 CMD_EMERGENCY_STOP with FLAGS_IS_PRIORITY (0x10), 50ms budget, 3-burst retry, hard latching and explicit clear
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-8-HMS-ERRORS
    expected: Vertical slice across 5 tiers, 4 severity levels (INFO/WARNING/ERROR/FATAL), 16-bit error subsystem taxonomy, AP ACK for MCU alarms
    actual: L1~L5 flow complete, 0x50 CMD_ALARM_EVENT from TH, AP sends explicit 0x50 ACK, 4 severity levels and 5 subsystems specified
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-9-OOBE-HARDWARE
    expected: Vertical slice across 5 tiers, strict realism invariant (no fake PASS), dual-MCU version querying
    actual: L5~L1 flow complete, 0x01 CMD_GET_VERSION / 0x02 CMD_VERSION_REPORT, strict realism invariant strictly mandated, next-step blocked if offline
    verdict: PASS
  - case: CHECKPOINT-1-FEATURE-10-MDNS-DISCOVERY
    expected: Vertical slice across 5 tiers, C11/C++17 zero dynamic heap allocation, RFC 6762 timing, network disconnect degradation
    actual: L4~Client flow complete, 224.0.0.251:5353 multicast, PTR/SRV/A/TXT records, zero dynamic heap allocation, disconnect degradation
    verdict: PASS
  - case: CHECKPOINT-2-PROTOCOL-INVARIANTS
    expected: Explicit ACK for every command (zero fire-and-forget), structured error reporting {target_node, sequence_id, elapsed_ms, error_code}
    actual: All commands mandate FLAGS_WANTS_ACK (0x01), all errors use Rule 7 4-tuple structured context, zero naked error logs
    verdict: PASS
  - case: CHECKPOINT-2-FAIL-CLOSED-AND-OPTION-A
    expected: 3s decay to OFFLINE, 0x7FFFFFFE sentinel temperature, HTTP 503 fail-closed, Option A 0% heating duty lock
    actual: Complete fail-closed specification, 0x7FFFFFFE (2147483646) sentinel, UI --.- °C formatting, 503 intercept, Option A 0% heater duty lock verified
    verdict: PASS
content_audit:
  fact_sources:
    result: passed
    basis: Verified against project-control commit 001bef072dc5195ab64ef51099b0027ca6e5e413 and existing protocol baselines
  protocol_compatibility:
    result: passed
    basis: MiniMCProto v2.0 wire layout, Fast DDS topic definitions, and D-Bus interfaces strictly verified
  claim_scope:
    result: passed
    basis: Document-review scope strictly bounded to TWIN-41 architectural specification
  architecture_completeness:
    result: passed
    basis: All 10 core features vertically sliced across 5 tiers with timing, ACK, retry, degradation, and self-healing fully specified
handoff:
  receiver_session: session-coord-autorun
  evidence_location: project-control/docs/evidence/twin/TWIN-41/runs/qa_01/qa_review_report.md
```

## 1. 身份、候选与过程核查

依据 `project-control/.agents/rules/codex_qa_review.md` 规范，本审查由独立 QA 评审员（`session-qa-twin-41`，平台 `codex`，实际模型 `gpt-6-luna`）对微任务 `TWIN-41` rev 1 进行独立文档与契约审计。

| 检查项 | 要核对什么 | 实际结果 | 证据 |
| :--- | :--- | :--- | :--- |
| **输入/范围** | 任务revision、正式契约、前置能力、准确候选、授权路径 | **通过** | `TWIN-41` rev 1，依赖 `TWIN-01`, `TWIN-08`, `TWIN-20` 均已就绪并验收；候选 Commit `001bef072dc5195ab64ef51099b0027ca6e5e413`；写入路径严格限制在 `project-control/docs/architecture/**` 与 `project-control/docs/evidence/twin/TWIN-41/**`。 |
| **独立性** | 作者与各独立检查者分离，QA作者报告另有独立复核 | **通过** | 评审员（`QA`, `session-qa-twin-41`）与作者（`ARCH`, `session-arch-twin-41`）完全分离，独立启动审查席位，只读审查候选快照。 |
| **原子步骤** | 先计划/前检、阶段边界、失败归因/熔断、保留用户改动 | **通过** | 作者自检报告 `author_01/result.md` 记录详实，各步骤边界清晰；架构文档保持独立版本演进，无破坏历史改动。 |
| **代码/构建** | 适用的函数/参数/内存/ISR/DMA及告警门禁，不弱化检查 | **通过** | 架构矩阵在规范级明确约束后续 C/C++ 实施必须满足：函数 $\le 50$ 行、入参 $\le 4$ 个、零运行时堆内存分配、强类型结构化异常与 Guard Clause。 |
| **证据真实** | 命令/cwd/退出码/原始输出/哈希/环境范围一致，未将模拟当HIL | **通过** | 本次审查为 `required_evidence_level: document-review`，执行静态图谱检查（`check_task_graph.py` exit 0）与 SHA256 哈希比对，真实一致。 |

---

## 2. 结果与正常/异常判据核验

本评审员对照任务卡 `TWIN-41.md` 验收条件、`AGENTS.md` 规则 7（通信闭环与硬件真实性强门禁）以及 COORD 审计检查点，对交付文档 `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md`（784 行）进行了逐字逐段的深度审查：

### 2.1 检查点 1：10 大核心垂直切片功能 5 层贯通性（L5 Web -> L4 UI Gateway -> L3 Device Manager -> L2 Forward -> L1 MCU）

| 功能序号与名称 | L5 交互层表现 | L4 网关层契约 | L3 状态与业务层 | L2 转发与编解码层 | L1 MCU 物理层执行 | 判定 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **功能 1：喷嘴/热床双温遥测与固件心跳** | 仪表盘 65.0°C / 210.0°C 渲染，连接状态绿灯指示 | HTTP SSE `/api/v1/temperature/stream`，Snapshot JSON 输出 | D-Bus `TriggerQuery`，新鲜度判定（<3s FRESH，$\ge$3s STALE），`TemperatureSnapshot` | MiniMCProto 12B 头 + 0B 载荷，分配递增 Seq，Stop-and-Wait 单在途模型 | AT32F435 MC / AT32F423 TH ADC 采样，查表线性插值，回发携带原 Seq 的 `0x14` REPORT / `0x04` PONG | **PASS** |
| **功能 2：CoreXY 触控微步 Jog 运控** | 触控点动按钮，点按后即刻添加 pending 态并禁用，防二次连击 | HTTP POST `/api/v1/motion/jog`，参数边界与在线状态防御校验 | D-Bus `MoveAxis`，准入判定（无 ESTOP、无 FAULT），Homing 归零标志保护 | MiniMCProto `0x15` `CMD_MOTION_MOVE`，16B 载荷（`dx_um`, `dy_um`, `dz_um`, `feedrate_mms`） | AT32F435 Marlin CoreXY 运动学解算与梯形加减速走步，回发 `0x15` ACK 或 `0x16` 坐标上报 | **PASS** |
| **功能 3：全轴归零 G28** | 全部/XY 归零按钮，旋转等待动画，归零完成点亮 "Homed" 徽章 | HTTP POST `/api/v1/motion/home`，校验 ALL/XY 参数及在线状态 | D-Bus `HomeAxes`，状态迁移为 HOMING，清空 `homed_mask`，`is_homed=false` | MiniMCProto `0x17` `CMD_HOME_AXES`，4B 载荷（`axes_mask`） | 驱动轴快速触碰限位开关、回退 3mm 慢速二次复触、Z 探针测床建立 (0,0,0) 原点，回发 `0x17` ACK (`homed_mask=0x07`) | **PASS** |
| **功能 4：5x5 自动调平网格校准 G29** | 触发按钮，5x5 拓扑热力图矩阵渲染展示 | HTTP POST `/api/v1/leveling/trigger`，GET `/api/v1/leveling/mesh` | D-Bus `TriggerLeveling`，归零前置依赖校验，调平完成后下发 `0x18` 网格查询 | MiniMCProto `0x19` 触发帧，`0x18` `CMD_LEVEL_GRID_QUERY` 帧 | 探针伸出遍历 25 个物理测点，EEPROM 持久化，回发 52B 载荷（`int16_t z_offset_um[25]`） | **PASS** |
| **功能 5：打印作业流流式下发与执行推进** | HTTP POST `/api/v1/jobs/start`，SSE 流式进度条与剩余时间渲染 | 在线校验（离线阻断 503），任务投递与暂停/恢复接口透传 | 作业引擎驱动，选项 A 强电锁死（`heater_duty=0%`），推进与行号 **100% 绑定硬件物理 ACK** | MiniMCProto `0x31` `STREAM_CHUNK`，结合 PONG `planner_buf_free` 实施滑窗信用流控 | Marlin 规划器缓冲压入与物理走步，回发包含空闲槽位与执行确认的 `0x31` ACK / `0x16` 报告 | **PASS** |
| **功能 6：4 通道混色配置与权重校验** | 4 通道滑块输入，非法输入前端高亮标红阻断 | HTTP POST `/api/v1/filament/slots`，严格执行 `slot_schema.json` 强校验（权重和必须严格等于 10000） | D-Bus `SetFilamentSlots`，更新 `aisoc_mixing_ratio_t` 结构体 | MiniMCProto `0x32` `CMD_SET_MIXING_RATIO`，8B 载荷（4x `uint16_t`） | AT32F423 TH 工具头配置多路挤出比例，回发 `0x32` ACK (`status=OK`) | **PASS** |
| **功能 7：紧急急停 E-STOP 注入与硬锁存** | 全局红色急停按钮，点击即刻弹出不可遮蔽硬锁屏，仅留复位清空 | HTTP POST `/api/v1/emergency/stop`，绕过常规业务队列抢占处理 | 瞬时切入 ESTOP 锁存状态，触发 `AISOC_ESTOP_LEVEL_HARD`，加热与使能全关 | MiniMCProto `0x12` `CMD_EMERGENCY_STOP`，置位 `FLAGS_IS_PRIORITY (0x10)` 广播帧 | MC/TH 硬件中断级响应：MOS PWM 0%、电机 Disable、死循环硬锁止，回发 `0x12` ACK (`Status=ESTOP_LATCHED`) | **PASS** |
| **功能 8：全机 HMS 错误码上报与严重度分级** | 换料指引向导弹出，缺料红色高亮，Toast 故障提示 | SSE 推送 `event: "hms_alarm"`，结构化 JSON 字段 | `hms_manager_raise_alarm` 活跃表管理，4 级严重度评估，联动状态机软暂停/硬急停 | 级联接收 TH 的 `0x50` 告警帧，校验 CRC 并向下位机回送 `0x50` 显式 ACK，抛出 D-Bus 信号 | TH 光电开关 PD2 变高（断料），向 MC 级联发送 `0x50` `CMD_ALARM_EVENT`（8B 载荷：level, subsys, error_code, tick） | **PASS** |
| **功能 9：开箱引导向导 OOBE 硬件状态读取** | `#oobe-modal` 向导页，默认显示“未就绪/等待接入”，未连接严禁虚假显示 PASS | HTTP GET `/api/v1/temperature/snapshot`，返回包含真实固件版本与传感器数据的 JSON | D-Bus `GetSnapshot`，管理双 MCU 握手状态与版本元数据 | MiniMCProto `0x01` `CMD_GET_VERSION` 探测帧，分别寻址 MC (`0x02`) 与 TH (`0x03`) | 双 MCU 返回 `0x02` `CMD_VERSION_REPORT`（24B 载荷：固件版本、boot_id、git_commit） | **PASS** |
| **功能 10：mDNS 局域网服务发现与直连** | 局域网 Tab 页，展示主机名 `aisoc-printer.local`、服务名 `_aisoc._tcp.local` 与一键复制直连 URL | C11/C++17 纯静态零堆分配 `mdns_advertiser` 守护组件，绑定 `224.0.0.251:5353` 组播 | L3 汇总整机真实版本与 IP 地址，注入 mDNS TXT 广播记录 | 属于 AP 网络层守护进程，无下行 MCU 帧；组播下发 PTR/SRV/A/TXT 报文 | 客户端浏览器解析 mDNS 直连访问 L4 Web 8080 端口下发 HMI 静态页面 | **PASS** |

### 2.2 检查点 2：协议不变量与时序硬门禁核查

1. **显式 ACK 与事务闭环门禁（Zero Fire-and-Forget）**：
   - 审查核实：矩阵文档 1.2 节与各功能小节明确禁止无理由 `no_reply=TRUE`；所有下行控制指令帧必须强制置位 `FLAGS_WANTS_ACK (0x01)`；
   - 下位机响应帧必须强制置位 `FLAGS_IS_RESPONSE (0x02)` 且必须回显原请求帧的 `Sequence ID`；
   - 对于双向事件（如 Feature 8 MCU 主动上报 `0x50 CMD_ALARM_EVENT`），明确规定上位机 L2 Forward 必须回发 `0x50 ACK` 确认帧，防止下位机无限重发。**完全合规**。
2. **强类型结构化异常追溯门禁（Rule 7 Compliance）**：
   - 审查核实：文档明确约束所有通信超时、丢包、校验失败或底层报错，必须抛出标准四元组：
     $$\text{Context} = \{\text{target\_node}, \text{sequence\_id}, \text{elapsed\_ms}, \text{error\_code}\}$$
   - 文档第 2.1(e), 2.2(e), 2.3(e), 2.4(e), 2.5(e), 2.6(e), 2.7(e), 2.8(e), 2.9(e), 2.10(e) 节均给出了该功能的精确结构化 JSON 实例与错误码定义（如 `0x1003` 超时、`0x1002` CRC、`0x4001` 归零失败、`0x3001` 断料等），彻底杜绝匿名裸日志。**完全合规**。
3. **打印作业绝对真实推进（Zero Fabricated Progress）**：
   - 审查核实：Feature 5 章节硬性规定“严禁在上位机使用本地纯时间定时器无脑自增打印行号或进度”；
   - 只有收到硬件底层确认帧（`0x31 ACK` 或 `0x16 POS_REPORT`）时，L3 作业引擎才推进当前已执行行号并重算千分比进度；链路丢包或断开时瞬时挂起为 `PAUSED`，行号和进度绝对锁死。**完全合规**。
4. **物理拔线容错与 Fail-Closed 降级**：
   - 审查核实：文档明确标定 3 秒老化衰退机制；拔除 `/dev/ttyUSB0` 或无有效数据超过 3000ms 后：
     * 状态机降级为 `OFFLINE`，数据质量标定为 `QUALITY_FAULT`；
     * 温度注入权威哨兵值 `0x7FFFFFFE` (`2147483646 = AISOC_TEMP_MILLIC_OFFLINE`)；
     * Web HMI 防御性格式化为 `--.- °C`（严格杜绝 `2147483.6 °C` 浮点泄漏）；
     * 加热棒占空比强制清零（0%）；
     * L4 Web 网关针对运控、归零、调平、作业等所有写操作 API 立即返回 `HTTP 503 Service Unavailable` 熔断拦截。**完全合规**。
5. **选项 A 逻辑空跑强电锁死（Option A 0% Heater Duty Lockout）**：
   - 审查核实：文档在 1.2 节、2.1(c) 节及 2.5(a) 节均明确规定：在 VMware 孪生与逻辑空跑验证阶段，加热棒 PWM 占空比硬性锁死为 0%，拦截任何实际加热输出，保障本质物理安全。**完全合规**。
6. **防撞机重试禁令**：
   - 审查核实：针对微步点动（Feature 2）和全轴归零（Feature 3），文档特别发布了 **“严禁盲目重发（Zero Blind Retry）”** 铁律；相对位移运动超时后唯一合法的恢复动作为下发 `0x16` 坐标查询对账，归零超时后强制报警并需人工检修，防止电机二次累加位移引发撞机。**完全合规**。

---

## 3. 问题、限制与结论

### 3.1 发现的问题与处置
- 在审查过程中，未发现违反 `AGENTS.md`、`c_cpp_coding_standard.md` 或通信契约的设计缺陷；
- 文档全面践行了“以单功能切片为维度梳理端到端全流程”的方法论，结构严谨，时序清晰，字段定义完备。

### 3.2 适用范围与局限性声明
- 本次审查为架构拆解阶段的文档规范评审（`required_evidence_level: document-review`）；
- 本报告签署的 `APPROVED` 结论仅针对规范文档本身的完整性、闭环性与协议映射准确性；
- 不代表各节点后续生产源码的构建通过、固件烧录接受或最终物理 HIL 台架验收；各节点的具体实施与组合验证由后续微任务独立闭环。

### 3.3 审查结论与签署
- **最终决定**：**`APPROVED`**
- **任务编号**：`TWIN-41`
- **任务 Revision**：`1`
- **被审阅候选 Commit**：`001bef072dc5195ab64ef51099b0027ca6e5e413`
- **交接目标**：`COORD` (`session-coord-autorun`)，等待 `ARCH` 联合签署后推进状态流转。
