---
template_version: '2026-10-27'
review_id: arch-review-twin-41-01
review_status: completed
reviewer_role: ARCH
reviewer_roles:
  - ARCH
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-arch-twin-41
actual_session: session-arch-review-41
author_session: session-arch-twin-41
task_id: TWIN-41
task_revision: 1
run_id: arch_01
reviewed_qa_report_sha256: e83ccfe82869ec550acda5e43efc8964fccb4b40a3eb550bf278b694a1cda2e4
reviewed_artifact_version: project-control=001bef072dc5195ab64ef51099b0027ca6e5e413
reviewed_artifacts:
  - path: project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md
    sha256: 8a117ada12634bf342541ec9130bfd100426fb95569758cddb010c5372abe59d
    commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
  - path: project-control/docs/evidence/twin/TWIN-41/runs/author_01/result.md
    sha256: 1eb04bc46aa95e9add582feb902b7e5801a300c72de31d86c3d8449142586192
    commit: 001bef072dc5195ab64ef51099b0027ca6e5e413
  - path: project-control/docs/evidence/twin/TWIN-41/runs/qa_01/qa_review_report.md
    sha256: e83ccfe82869ec550acda5e43efc8964fccb4b40a3eb550bf278b694a1cda2e4
protocol_and_expectations:
  - path: project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
    commit: afd5259
  - path: project-control/.agents/rules/codex_qa_review.md
    commit: afd5259
  - path: project-control/.agents/rules/c_cpp_coding_standard.md
    commit: afd5259
verification_environment: document-review
verification_scope: End-to-end single feature flow closed-loop sequence and protocol mapping architecture matrix (10 features, 5 tiers, 10 sequence diagrams, explicit ACK and sequence ID binding, timeout budgets, 0x7FFFFFFE sentinel temperature, 3s aging decay to OFFLINE, fail-closed 503, and Option A dry-run 0% heating duty lock)
required_evidence_level: document-review
review_time: '2026-11-02T18:00:00+08:00'
process_audit: passed
result_check: passed
decision: APPROVED
accepted_scope: TWIN-41 端到端单功能全流程闭环时序与协议映射权威规范矩阵 (10 大核心功能垂直切片、5 层架构、10 个完整 Mermaid 时序图、显式 ACK 与序列号绑定、超时预算、0x7FFFFFFE 哨兵温、3s 老化降级、Fail-Closed 503 阻断及选项 A 加热锁死)
limitations: []
unexecuted: []
not_applicable: []
issues: []
content_audit:
  fact_sources:
    result: passed
    basis: "10 大核心垂直切片架构梳理基于 MiniMCProto v2.0、状态机设计规范、D-Bus/HTTP 接口定义与雅特力双单片机（AT32F435 MC + AT32F423 TH）硬件特性，事实依据充分。"
  protocol_compatibility:
    result: passed
    basis: "协议字段严格对齐 12 字节 MiniMCProto v2.0 帧头格式（SOF 0x55 0xAA、Flags、Seq、Cmd ID、Len、CRC-16），双向 ACK 与 Sequence ID 对账机制严密。"
  claim_scope:
    result: passed
    basis: "架构规约聚焦于端到端时序与协议映射，职责清晰划分为 5 层，未越权引入非标绕行通路。"
  architecture_completeness:
    result: passed
    basis: "完整覆盖 10 大核心功能的正常流、超时流、断线流与自愈流，铁律硬门禁与 C/C++ 编码门禁 100% 落实。"
---

# TWIN-41 架构拆解阶段端到端单功能全流程闭环梳理与协议映射 独立系统架构师审查报告

## 1. 审查背景与执行身份核查

- **审查任务**: `TWIN-41` (架构拆解阶段端到端单功能全流程闭环梳理与协议映射)
- **审查角色**: `ARCH` (独立系统架构师审查席位)
- **执行平台**: `codex` (`gpt-6-luna`)
- **审查会话**: `session-arch-review-41` (独立会话，未参与作者编写)
- **作者会话**: `session-arch-twin-41` (`run_id: author_01`)
- **审查依据**: `project-control/.agents/rules/codex_qa_review.md` 与系统架构不变量门禁。

本次审查针对候选提交 `001bef072dc5195ab64ef51099b0027ca6e5e413` 交付的核心架构资产：
1. `project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md` (SHA256: `8a117ada12634bf342541ec9130bfd100426fb95569758cddb010c5372abe59d`)
2. `project-control/docs/evidence/twin/TWIN-41/runs/author_01/result.md` (SHA256: `1eb04bc46aa95e9add582feb902b7e5801a300c72de31d86c3d8449142586192`)

---

## 2. 身份、候选与过程核查

| 检查项 | 要核对什么 | 实际结果 | 证据 |
| :--- | :--- | :--- | :--- |
| **输入/范围** | 任务 revision 1，正式契约，前置依赖（TWIN-01, TWIN-08, TWIN-20），写白名单约束 | **通过** | 仅写入 `docs/architecture/` 与 `docs/evidence/twin/TWIN-41/`，符合卡片白名单 |
| **独立性** | 作者与审阅者完全物理隔离，独立 Codex 会话审阅 | **通过** | 作者会话 `session-arch-twin-41` 与审查会话 `session-arch-review-41` 相互独立 |
| **原子步骤** | 架构拆解方法论践行，垂直切片覆盖，铁律硬门禁 | **通过** | 严格按“单功能全流程”切片梳理，彻底根除“开环假跑、静默吞异常、发后即忘” |
| **规范约束** | 函数规模、参数、动态分配、防御性校验 | **通过** | 第 4 节明确约束 $\le 50$ 行、$\le 4$ 参数、零动态堆分配，公开接口首行防御卫语句 |
| **证据真实** | 交付物完整性、哈希校验、无虚假占位 | **通过** | 784 行结构化规约，10 组 Mermaid 时序图，SHA256 校验完全对账 |

---

## 3. 架构内容与 10 大核心功能垂直切片全景核查

审阅确认交付规范 [`end_to_end_feature_flow_closed_loop_matrix.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/end_to_end_feature_flow_closed_loop_matrix.md) 完整构建了 5 层全链路端到端闭环模型：
- **L5 交互层**: Browser Web HMI
- **L4 网关层**: UI Gateway (HTTP REST / SSE)
- **L3 状态层**: Device Manager (State Machine, HMS, Job Engine)
- **L2 转发层**: Forward Service (MiniMCProto v2.0 Framing & Dispatch)
- **L1 硬件层**: Dual MCU Firmware (AT32F435 MC + AT32F423 TH)

### 3.1 10 大核心功能与 Mermaid 时序图核验
文档包含 10 个标准章节，每一章节均包含完整的 Mermaid `sequenceDiagram`，无一遗漏：

1. **功能 1：喷嘴/热床双温遥测与固件心跳 (Nozzle/Bed Telemetry & Firmware Heartbeat)**
   - *时序闭环*: L5 $\to$ L4 $\to$ L3 $\to$ L2 $\to$ L1，双向 1Hz/5Hz 遥测流。
   - *指令与 ACK*: `CMD_TEMP_QUERY (0x14)`、`CMD_PING (0x03)`，硬件回送带原 `seq` 的 `0x14` REPORT / `0x04` PONG。
   - *超时与降级*: 单次 100ms 超时，重试 2 次 (20ms 退避)。3s 无遥测老化衰退至 `OFFLINE`，注入 `0x7FFFFFFE` (`AISOC_TEMP_MILLIC_OFFLINE`) 哨兵温，Web 渲染 `--.- °C`。
2. **功能 2：CoreXY 触控微步 Jog 运控 (Jog Motion)**
   - *时序闭环*: 触控单在途防呆锁定，下发 `CMD_MOTION_MOVE (0x15)` 携带微米坐标增量。
   - *指令与 ACK*: MC 规划器确认 `0x15` ACK 或 `0x16` POS_REPORT 携带绝对微米坐标。
   - *超时与禁令*: 超时 2000ms。**核心禁令：相对位移严禁盲目重发**，防止位移累加引发机械撞击；降级通过 `0x16` 读绝对位置对账。
3. **功能 3：全轴归零 G28 (Homing All / XY)**
   - *时序闭环*: 前端点按归零，网关生成独占序列号下发 `CMD_HOME_AXES (0x17)`。
   - *指令与 ACK*: 限位触碰复触后，MC 上报 `HomedMask=0x07` 确认帧。
   - *超时与防撞*: 标定 30s 超时预算。**核心禁令：归零超时严禁盲重试**，立即撤销 `is_homed` 并锁死绝对运控。
4. **功能 4：5x5 自动调平网格校准 G29 (Mesh Bed Leveling)**
   - *时序闭环*: 下发 `CMD_LEVEL_GRID_QUERY (0x18)` 或触发调平 `0x19`。
   - *载荷对账*: 52 字节载荷（25 个点 `int16_t z_offset_um`），超时预算 120s。
   - *异常降级*: 失败标记网格无效，前端以高对比度热力图警告阻断开工。
5. **功能 5：打印作业流流式下发与执行推进 (Job Execution Pipeline)**
   - *时序闭环*: G-code 块切片下发 `CMD_GCODE_STREAM (0x31)`，基于 Marlin 缓冲区空闲信用流控。
   - *绝对铁律*: **严禁上位机纯本地定时器假自增进度与行号**。作业推进 100% 绑定硬件 ACK；断线瞬时置为 `PAUSED`，进度与行号绝对锁死。
6. **功能 6：4 通道混色配置与权重校验 (4-Channel Filament Slots & Mixing Ratio)**
   - *时序闭环*: 前端配置 4 槽位权重，网关基于 `slot_schema.json` 强校验。
   - *严格不变量*: 权重总和必须绝对等于 `10000`（基点万分比），非法输入直接报 400；下发 `CMD_SET_MIXING_RATIO (0x32)` 至 TH 从控回显 ACK。
7. **功能 7：紧急急停 E-STOP 注入与硬锁存 (Emergency Stop & Reset)**
   - *时序闭环*: 最高优先级广播帧（`FLAGS_IS_PRIORITY = 0x10`），下发 `CMD_EMERGENCY_STOP (0x12)`。
   - *硬件切断*: 50ms 极限超时，3 次高密重发；硬件中断级切断强电，PWM 占空比硬锁死为 0%，必须显式 Clear 方可解锁。
8. **功能 8：全机 HMS 错误码上报与严重度分级 (HMS Error Reporting & Severity)**
   - *时序闭环*: 硬件传感器（如 TH 断料检测）触发 `CMD_ALARM_EVENT (0x50)` 上报 AP，AP 必须回送确认帧。
   - *错误体系*: 16-bit 结构化体系（`0x1000`~`0x5000`），四级严重度分级，断料联动软暂停与全屏处置指引。
9. **功能 9：开箱引导向导 OOBE 硬件状态读取 (OOBE Wizard Hardware Readout)**
   - *时序闭环*: 双 MCU 真实固件版本 `CMD_GET_VERSION (0x01)` 轮询。
   - *唯实铁律*: **真实物理存在性检验，严禁未连接设备虚假显示“合格”或“PASS”**；拔线阻断进入控制台，连线 SSE 免刷新自愈点亮。
10. **功能 10：mDNS 局域网服务发现与直连 (mDNS Service Discovery)**
    - *时序闭环*: C11/C++17 零动态分配 `mdns_advertiser`，RFC 6762 组播 `224.0.0.251:5353` 宣告 `aisoc-printer.local`。
    - *断线降级*: 拔除网线即刻停止组播，重连后自愈刷新 A 记录。

---

## 4. 架构硬性铁律与不可动摇的设计不变量核实

经逐行核查，规范文档对用户与系统架构制定的各项硬性门禁落实如下：

1. **绝对杜绝“发后即忘”（Zero Fire-and-Forget）**：
   - 矩阵中所有下行控制指令均强制置位 `FLAGS_WANTS_ACK (0x01)`，彻底杜绝 `no_reply=TRUE`；
   - 明确下位机必须使用相同的 `Sequence ID` 回显确认，形成完整的闭环事务。
2. **绝对杜绝开环假跑（Strict Realism & Zero Fabricated Progress）**：
   - 明确作业流推进必须 100% 以下位机实际缓冲消费与坐标 ACK 为物理依据；
   - 严禁上位机运行本地虚假自增时钟，异常中断时行号和进度强制冻结。
3. **选项 A 强电安全锁死（Option A 0% Heating Duty Lockout）**：
   - 规范明文规定孪生与空跑验证阶段，加热棒 PWM 占空比硬性锁死为 0%，杜绝强电输出。
4. **结构化异常四元组追溯（Rule 7 Compliance）**：
   - 规定凡超时、丢包或校验报错，必须携带：
     $$\text{Context} = \{\text{target\_node}, \text{sequence\_id}, \text{elapsed\_ms}, \text{error\_code}\}$$
   - 严禁匿名裸日志，统一向上冒泡映射。
5. **热插拔与拔线 3 秒 Fail-Closed 硬隔离**：
   - 串口不可达 3 秒内，状态机必须衰退为 `OFFLINE`，注入 `0x7FFFFFFE` 哨兵温度；
   - Web API 控制接口统一返回 `HTTP 503 Service Unavailable`，UI 按钮置灰禁用。

---

## 5. 审查结论与签署

独立系统架构师审阅确认：`TWIN-41` 交付的端到端单功能全流程闭环时序与协议映射权威规范矩阵，立意高远、结构严谨、细节扎实，100% 覆盖了系统核心业务，100% 贯彻了防开环、防吞异常、防假跑的硬性门禁，具备极高的指导性与工程落地可行性。

- **审查判定**: **APPROVED (通过)**
- **审查人**: 独立系统架构师 (`session-arch-review-41`)
- **签发日期**: `2026-11-02`
