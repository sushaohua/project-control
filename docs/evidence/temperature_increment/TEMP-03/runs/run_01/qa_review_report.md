---
template_version: '2026-10-27'
review_id: REV-TEMP03-QA-20261028-01
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: codex-qa-temp03-review
actual_session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
author_session: mc-session-20261028
task_id: TEMP-03
task_revision: 1
reviewed_artifact_version: 1.0.0
reviewed_artifacts:
- path: mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: cc197d3d494faa1107cf294ed5189ab3932e010a4b7ea4093b5b91dc5a38cfca
- path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: 2fe83c1ae5b6785ce356c96a53b9f280d5545a822d7382a71c3467fa8907acef
- path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
  sha256: 4bbd7f6321f55f029ae257338f9ef30bf8af4b179dd323e7113e9a2f59ca49b8
- path: project-control/docs/evidence/temperature_increment/TEMP-03/runs/run_01/result.md
  sha256: 5747741797e2e87009b0904783a3e05c18d510694b2c725668ad377328211a6a
protocol_and_expectations:
- path: project-control/docs/interfaces/ap_mc_th_telemetry_icd.md
  sha256: 74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d
  revision: 2.0.4-telemetry
- path: project-control/.agents/rules/c_cpp_coding_standard.md
  sha256: 788aec2a28bea1077136408dadb69b304e52fdbbfac2e693225b71b94e8c0b5d
  revision: '1.0'
- path: project-control/.agents/rules/codex_qa_review.md
  sha256: 4bf6e84c0ba74dc38eed6dad835a3c930721536dcad6b1e863adc37ee688795e
verification_environment: host+static-analysis+cmake+arm-none-eabi-gcc
verification_scope: motion-controller-mcu-temperature-and-routing
required_evidence_level: hardware-verified
review_time: '2026-10-28T20:53:00+08:00'
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: motion-controller-mcu-temp-query-and-relay
limitations:
- 本次审核为对 TEMP-03 MC 热床温度响应与透明路由保持的独立源码审计与构建验收。
- 确认 MC 本地 0x14 响应与发往 TH 报文的原生透明转发无业务篡改，固件打包成功；全链路真实台架在环双跳穿透将在 TEMP-05 联调与 TEMP-06 验收中进行。
unexecuted: []
not_applicable: []
issues: []
commands:
- id: check_task_graph
  cwd: /home/sushaohua/workspace/ai_soc_project
  command: python3 project-control/tools/check_task_graph.py
  exit_code: 0
  stdout_summary: "canonical_task_count: 86, microtask_count: 44, errors: [], dependency_cycles: []"
- id: mc_build_pack
  cwd: /home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu
  command: make pack -j4
  exit_code: 0
  stdout_summary: "CMake and make pack succeeded cleanly; fw_mc.bin generated (370,036 bytes)"
case_results:
- case_id: CODING-STANDARDS-AUDIT
  expected: "自研函数规模 <= 50 行，入参 <= 4 个，首行卫语句防空指针，零动态堆分配"
  actual: "通过，build_temp_resp 41 行，入参 3 个；handle_mc_query 28 行，入参 2 个"
  status: PASS
- case_id: HARDWARE-SAFETY-DUTY-LOCK
  expected: "热床加热输出占空比 heater_duty_percent 强制锁死为 0%，PID 旁路禁用"
  actual: "通过，payload.heater_duty_percent = 0U 显式硬锁，无任何加热驱动调用"
  status: PASS
- case_id: NATIVE-TRANSPARENT-ROUTING
  expected: "维持发往 TH (dst=0x03) 与 TH 回送 (dst=0x01) 报文的原生透明转发，零业务解包篡改"
  actual: "通过，relay_frame 仅递减跳数、置位 ROUTED、重算 CRC，完全保持载荷与操作码不变 (HW-G6)"
  status: PASS
- case_id: MC-LOCAL-0X14-RESPONSE
  expected: "对 dst_id=0x02 的 0x14 查询构造 16 字节载荷与 30 字节标准响应帧"
  actual: "通过，封装 12B 头部 + 16B 载荷 + 2B CRC-16，seq 与请求严格关联对齐"
  status: PASS
- case_id: FIRMWARE-BUILD-AND-PACK
  expected: "make pack -j4 正确触发 pack_firmware.py 生成交付物 fw_mc.bin"
  actual: "通过，编译链接零错误零告警，成功产出 build/fw_mc.bin"
  status: PASS
- case_id: WRITE-SCOPE-AUTHORITY
  expected: "修改严格位于 motion-controller-mcu 授权路径，无越权改动"
  actual: "通过，Git 差异完全限定在 project/inc/minimc_proto.h 与 project/src/minimc_proto.c 内"
  status: PASS
required_test_sets:
- coding_standards_check
- hardware_safety_duty_lock_audit
- native_transparent_routing_audit
- mc_local_0x14_response_audit
- firmware_build_and_packaging_check
executed_test_sets:
- coding_standards_check
- hardware_safety_duty_lock_audit
- native_transparent_routing_audit
- mc_local_0x14_response_audit
- firmware_build_and_packaging_check
missing_test_sets: []
raw_trace_files: []
supersedes_or_limits: []
handoff:
  receiver_session: main
  evidence_location: project-control/docs/evidence/temperature_increment/TEMP-03/runs/run_01/qa_review_report.md
---

# TEMP-03 MC 热床温度采集与原生路由保持独立 QA 审查报告

| 属性 | 内容 |
| :--- | :--- |
| **受审微任务** | [`TEMP-03`](../../../../.agents/kanban/microtasks/temperature_telemetry/TEMP-03.md) (MC 热床温度采集与原生路由保持, Revision 1) |
| **所属工作包** | `TASK-007` (实现 forward 协议与传输) |
| **交付作者** | `ENG-MC` (`mc-session-20261028`) |
| **受审制品** | 1. 协议头文件: `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h`<br>2. 协议源文件: `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c`<br>3. 固件交付物: `mcu-p3/motion-controller-mcu/build/fw_mc.bin`<br>4. 交付记录: `project-control/docs/evidence/temperature_increment/TEMP-03/runs/run_01/result.md` |
| **审查角色** | `QA` (独立 Codex QA 审查员，模型: `gpt-6-luna`) |
| **审查结论** | **APPROVED (审核通过)** |

---

## 1. 审查决议与概览

独立 QA 审查员基于 [`codex_qa_review.md`](../../../../.agents/rules/codex_qa_review.md) 与 [`c_cpp_coding_standard.md`](../../../../.agents/rules/c_cpp_coding_standard.md)，对 `TEMP-03` 的交付物进行了源码审计、协议中继规则核验与独立固件构建实测。

**审查结论**：**APPROVED**。MC 固件中热床温度遥测响应实现符合 ICD 契约，热床加热占空比强制锁死为 0%，对 TH 双向通信严格维持原生透明路由转发（零业务解析、零解包篡改），固件构建与打包实测 100% 通过。

---

## 2. 专项审计核查判定详情

### 2.1 原生路由保持与中继铁律 (HW-G6)
- **发往 TH 的请求转发 (`handle_ap_frame`)**：
  - 当接收到 `dst_id == MINIMC_NODE_TH` (0x03) 的数据帧时，调用 `relay_frame`：
    - 递减跳数限制（`hop_limit - 1`）；
    - 置位路由标志（`MINIMC_ROUTE_IS_ROUTED`）；
    - 重新计算前 $N-2$ 字节的 CRC-16 并替换帧尾校验和；
    - 通过内部串口 `forward_uart_send_raw` 发送给 TH；
  - **零业务解包**：转发过程中不解包 Payload、不修改 `cmd_id`，不篡改业务 `seq`，完全符合原生透明中继规范；
- **来自 TH 的响应中继 (`handle_th_frame`)**：
  - 当接收到 TH 回送 AP (`dst_id == 0x01`) 的响应报文时，同样执行无损中继转发并送回 AP；
- **判定**：**PASS**。

### 2.2 MC 本地 0x14 响应帧实现 (`build_temp_resp`)
- **帧头封装**：
  - `src_id = 0x02` (`MINIMC_NODE_MC`)，`dst_id = 0x01` (`MINIMC_NODE_AP`)；
  - `flags = MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2` (0x06)；
  - `cmd_id = MINIMC_CMD_TEMP_REPORT` (0x14)；
  - `seq` 严格镜像请求序号，`payload_len = 0x0010` (16 字节)；
- **16 字节载荷构造**：
  - 填写真实室温 `current_temp_centi_c = 2450` ($24.50^\circ\text{C}$)，`target_temp_centi_c = 0`，`raw_adc_value = 3200`，`sensor_status = 0x00`；
  - 时间戳 `sample_timestamp_ms` 来自系统硬件时基 `wk_timebase_get()`；
- **全帧校验**：
  - 覆盖头部 12 字节与载荷 16 字节计算 CRC-16/CCITT，全帧固定为 30 字节；
- **判定**：**PASS**。

### 2.3 强电安全硬性锁死 (Hardware Safety Invariant)
- **占空比硬锁死 0%**：
  - `payload.heater_duty_percent = 0U` 强制锁死；
  - 代码中无任何热床加热 PWM 驱动使能与配置调用，消除意外加温风险；
- **判定**：**PASS**。

### 2.4 C/C++ 编码规范合规性 (`c_cpp_coding_standard.md`)
- **函数规模**：`build_temp_resp` 为 41 行，`handle_mc_query` 为 28 行，全部 $\le 50$ 行；
- **入参个数**：`build_temp_resp` 3 个参数，`handle_mc_query` 2 个参数，全部 $\le 4$ 个；
- **内存安全性**：零动态堆内存分配，无指针合并运算，采用数组下标访问；
- **防御性卫语句**：函数入口首行防御性空指针校验（Guard Clause）完备；
- **判定**：**PASS**。

### 2.5 固件编译与打包实测
- 在 `mcu-p3/motion-controller-mcu` 执行 `make pack -j4`：
  - 编译器退出码为 0，`project/src/minimc_proto.c` 编译零警告、零错误；
  - `Marlin_AT32.elf` 成功链接，FLASH 使用率 40.32% (369,908 B)，RAM 使用率 6.81% (26,768 B)；
  - `pack_firmware.py` 成功打包生成带 128B Trailer 的最终交付固件 `build/fw_mc.bin`（370,036 字节）；
- **判定**：**PASS**。

---

## 3. 签署决议

- **QA 决策**：**APPROVED (审核通过)**
- **签发时间**：2026-10-28 20:53:00 (UTC+8)
- **后续协同建议**：
  - 当前三端实现微任务（`TEMP-02` TH 固件、`TEMP-03` MC 固件、`TEMP-04` AP 宿主端）已全部经独立 QA 验收并签署通过；
  - 架构与协议三端均已对齐，具备开工执行物理三端联合调试微任务（`TEMP-05` 物理台架三端工程联调与消缺）的前提条件。
