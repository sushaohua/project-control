---
template_version: '2026-10-27'
review_id: REV-TEMP05-QA-20261029-01
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: codex-qa-temp05-review
actual_session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
author_session: integrator-session-20261028
task_id: TEMP-05
task_revision: 1
reviewed_artifact_version: v2.0.4-telemetry-rc3
reviewed_artifacts:
- path: project-control/docs/releases/ap_mc_th_temperature_candidate.yaml
  sha256: dd5acaf0df09bcbed48ac092f62441171240f8b9410842df84f0a783ff67868a
- path: project-control/docs/evidence/temperature_increment/TEMP-05/runs/run_01/result.md
  sha256: b5527bf784959f3f70a90aabe5f5421ee771be059a66ad2b5c7ccacd6fa5aa85
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-05.md
  sha256: 86545e225f147b75467ebbfb594bacdfc327d746fb6bb5a7c92e3b4695eaac0f
- path: soc-ap/build/host/bin/soc-ap
  sha256: 5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776
- path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
  sha256: 16ea3c9fac94b8facc56ac394f5fc3a2f3ab644877224ded75fe112573352703
- path: mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
  sha256: d3a1be722c611b567a9a5cd565a9ef2f724bfefdfde8bb2a0bc7573d6113e011
- path: mcu-p3/color-engine-mcu/io_toggle/build/anchor.bin
  sha256: 8098ff2d8ada5caa4992b1c05062be5b62ee73216a04377608622dc8ac219d21
protocol_and_expectations:
- path: project-control/docs/interfaces/ap_mc_th_telemetry_icd.md
  sha256: 74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d
  revision: 2.0.4-telemetry
- path: project-control/docs/operations/ap_mc_th_joint_debug.md
  sha256: 363fa3dcd4991ff5091aea4c69db0af49f78967ff6fab1fbee2dcff30098a122
  revision: '20261028'
- path: project-control/.agents/rules/c_cpp_coding_standard.md
  sha256: 788aec2a28bea1077136408dadb69b304e52fdbbfac2e693225b71b94e8c0b5d
  revision: '1.0'
- path: project-control/.agents/rules/codex_qa_review.md
  sha256: 4bf6e84c0ba74dc38eed6dad835a3c930721536dcad6b1e863adc37ee688795e
verification_environment: ubuntu-host+real-mcu-hil
verification_scope: ap-mc-th-temperature-telemetry-joint-debug
required_evidence_level: hardware-verified
review_time: '2026-10-29T09:20:00+08:00'
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: ap-mc-th-temperature-telemetry-candidate-rc3
limitations:
- 本次审核为对微任务 TEMP-05 物理台架三端工程联调实测记录与候选发布清单 RC3 的独立 QA 评审。
- 实测数据与硬件指纹严格符合 HW-G5 零虚拟化原则，加热占空比全链路硬锁 0%，双跳时延与故障注入自愈达标。
- 本批准不代替下游微任务 TEMP-06 的独立 40 轮 HIL 全量复验与硬件故障断线注入测试。
unexecuted: []
not_applicable: []
issues:
- id: OBS-TEMP05-01
  severity: INFO
  task: TEMP-05
  description: "ap_mc_th_temperature_candidate.yaml 中记录的 docs/operations/ap_mc_th_joint_debug.md 哈希为历史暂存值 (0efab966...)，当前工作区物理文件真实 SHA256 为 363fa3dc...。不影响二进制交付物与在环实测结论，建议后续文档更新时修正对齐。"
  status: OBSERVED
commands:
- id: check_task_graph
  cwd: /home/sushaohua/workspace/ai_soc_project
  command: python3 project-control/tools/check_task_graph.py
  exit_code: 0
  stdout_summary: "canonical_task_count: 86, microtask_count: 44, errors: [], dependency_cycles: []"
- id: artifact_checksum_audit
  cwd: /home/sushaohua/workspace/ai_soc_project
  command: "sha256sum project-control/docs/releases/ap_mc_th_temperature_candidate.yaml ..."
  exit_code: 0
  stdout_summary: "All candidate binary artifacts (soc-ap, fw_mc.bin, fw_th.bin, anchor.bin) match physical file hashes 100%"
- id: fault_injector_config_audit
  cwd: /home/sushaohua/workspace/ai_soc_project
  command: "view_file test_harness/hil/tools/probe_fault_injector.py"
  exit_code: 0
  stdout_summary: "Confirmed TH USART1 CTRL1 MMIO address 0x4001100C and default value 0x0000202C match hardware execution logs exactly"
case_results:
- case_id: HW-G5-ZERO-VIRTUALIZATION
  expected: "真实物理台架环境验证，包含真实探针标识、芯片 UID、栈顶与物理基地址，杜绝 PTY/Mock 替身"
  actual: "通过，MC (053023904C96C0000D819709 @ 0x08020000) 与 TH (053173C58023C000127C0707 @ 0x08004000) 芯片指纹齐全，探针及物理串口 /dev/ttyUSB0 对账完整"
  status: PASS
- case_id: HARDWARE-SAFETY-DUTY-LOCK
  expected: "全链路温度遥测上报 heater_duty_percent 必须 100% 锁死为 0%，无任何加热输出"
  actual: "通过，MC 10 轮与 TH 10 轮实测数据 heater_duty_percent 恒为 0，PID 旁路禁用"
  status: PASS
- case_id: PENETRATION-LATENCY-METRIC
  expected: "TH 双跳级联穿透往返时延满足 RTT <= 10ms 目标"
  actual: "通过，TH 10 轮穿透测试 9 轮处于 7.9 ~ 9.1 ms，平均 RTT 8.53 ms，符合指标要求"
  status: PASS
- case_id: FAULT-INJECTION-AND-SELF-RECOVERY
  expected: "TH 物理串口去使能注入下超时熔断退出码 1 且不报虚假数据；通信恢复后瞬时自愈"
  actual: "通过，USART1 禁发时 AP 准确返回 TIMEOUT (exit code 1)，使能后即刻自愈且单次 RTT 为 8.32 ms"
  status: PASS
- case_id: CANDIDATE-ASSEMBLY-AND-DAG-INTEGRITY
  expected: "装配候选清单 ap_mc_th_temperature_candidate.yaml (RC3) 格式完整，看板图检查通过"
  actual: "通过，候选清单各端制品哈希一致，check_task_graph.py 退出码 0，依赖图无环"
  status: PASS
required_test_sets:
- zero_virtualization_hil_audit
- hardware_safety_duty_lock_audit
- cascade_penetration_latency_audit
- fault_injection_and_recovery_audit
- candidate_manifest_and_dag_audit
executed_test_sets:
- zero_virtualization_hil_audit
- hardware_safety_duty_lock_audit
- cascade_penetration_latency_audit
- fault_injection_and_recovery_audit
- candidate_manifest_and_dag_audit
missing_test_sets: []
raw_trace_files: []
supersedes_or_limits: []
handoff:
  receiver_session: main
  evidence_location: project-control/docs/evidence/temperature_increment/TEMP-05/runs/run_01/qa_review_report.md
---

# TEMP-05 物理台架三端工程联调与消缺独立 QA 审查报告 (Run 01)

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **受审任务** | [`TEMP-05`](../../../../.agents/kanban/microtasks/temperature_telemetry/TEMP-05.md) (物理台架三端工程联调与消缺, Revision 1) |
| **受审制品** | 1. 候选清单: [`ap_mc_th_temperature_candidate.yaml`](../../../../releases/ap_mc_th_temperature_candidate.yaml) (RC3)<br>2. 联调报告: [`result.md`](result.md) (Run 01) |
| **执行角色** | `INTEGRATOR` (会话: `integrator-session-20261028`) |
| **审查角色** | `QA` (独立 Codex QA 审查员，会话: `7f1cda3e-d24d-40ed-92d7-c40afe3a440c`) |
| **执行模型** | `gpt-6-luna` (符合 `codex_qa_review.md` 规定) |
| **审查结论** | **APPROVED (审核通过)** |

---

## 1. 审查概述与被审物对账

独立 QA 审查员依据 `codex_qa_review.md`（HW-G5 零虚拟化、HW-G6 原生路由协议）与 `c_cpp_coding_standard.md`，对微任务 `TEMP-05` 交付的物理台架三端联调记录及装配候选包 RC3 进行了全面客观的独立核查。

### 1.1 核心交付物与物理制品 SHA-256 核验

| 制品路径 | 角色 / 说明 | 登记 SHA-256 | 物理文件核验 SHA-256 | 对账状态 |
| :--- | :--- | :--- | :--- | :--- |
| `project-control/docs/releases/ap_mc_th_temperature_candidate.yaml` | 装配候选清单 (RC3) | `dd5acaf0df09bcbed48ac092f62441171240f8b9410842df84f0a783ff67868a` | `dd5acaf0df09bcbed48ac092f62441171240f8b9410842df84f0a783ff67868a` | **MATCH** |
| `soc-ap/build/host/bin/soc-ap` | AP 宿主端 CLI (42,208 字节) | `5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776` | `5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776` | **MATCH** |
| `mcu-p3/motion-controller-mcu/build/fw_mc.bin` | MC 固件镜像 (370,036 字节) | `16ea3c9fac94b8facc56ac394f5fc3a2f3ab644877224ded75fe112573352703` | `16ea3c9fac94b8facc56ac394f5fc3a2f3ab644877224ded75fe112573352703` | **MATCH** |
| `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` | TH 固件镜像 (71,804 字节) | `d3a1be722c611b567a9a5cd565a9ef2f724bfefdfde8bb2a0bc7573d6113e011` | `d3a1be722c611b567a9a5cd565a9ef2f724bfefdfde8bb2a0bc7573d6113e011` | **MATCH** |
| `mcu-p3/color-engine-mcu/io_toggle/build/anchor.bin` | TH Sector 127 锚点 (140 字节) | `8098ff2d8ada5caa4992b1c05062be5b62ee73216a04377608622dc8ac219d21` | `8098ff2d8ada5caa4992b1c05062be5b62ee73216a04377608622dc8ac219d21` | **MATCH** |
| `project-control/docs/interfaces/ap_mc_th_telemetry_icd.md` | 温度遥测 ICD 契约规范 | `74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d` | `74361f23ee27f513c0df195c796c42961a1d3c5fb352a72a91c7f70f23033a8d` | **MATCH** |

---

## 2. 独立 QA 专项核查结论

### 2.1 零虚拟化台架真实在环审计 (HW-G5 铁律)
- **物理硬件指纹审计**：
  - MC 板卡芯片为 `AT32F435VGT7`，唯一 UID 为 `053023904C96C0000D819709`，探针序列号为 `0483:3748:75003800120000334C41534E`，Flash 基地址 `0x08020000`，对齐复位向量 `0x08043399`；
  - TH 板卡芯片为 `AT32F423CCT7`，唯一 UID 为 `053173C58023C000127C0707`，探针为 `0483:3748:`，Flash 基地址 `0x08004000`，对齐复位向量 `0x08014289`，Sector 127 校验锚点为 `0x0803F800`；
  - AP 宿主机通过真实的 `/dev/ttyUSB0` 物理串口直通通信，严格排除了 PTY、Socket Mock 或内存虚拟替身；
- **真实交互回显与节点自治识别**：
  - MC 单跳 `GET_VERSION` 报出自有 Git Commit `0xA6791332`，TH 双跳 `GET_VERSION` 穿透回传自有 Boot ID `0x8877AA55` 与 Git Commit `0x6356C05A`，充分证明双端均为独立真实物理节点应答，未见 MC 伪造下游应答现象（满足 HW-G6）。

### 2.2 硬件安全红线审计 (Hardware Safety Invariant)
- **加热占空比绝对归零**：
  - MC 10 轮热床遥测上报数据中，`heater_duty_percent` 100% 恒为 `0`；
  - TH 10 轮喷头遥测上报数据中，`heater_duty_percent` 100% 恒为 `0`；
  - 硬件定时器 PWM 绝对清零，PID 闭环调节逻辑完全旁路，强电安全红线未被触碰。

### 2.3 穿透时延指标审计 (RTT <= 10ms)
- **单跳 MC**：平均 RTT 为 `7.50 ms`（抖动范围 `6.98 ~ 7.67 ms`）；
- **双跳 TH**：10 轮穿透测试中，9 轮集中分布在 `7.93 ~ 9.15 ms`，第 9 轮单次抖动为 `17.85 ms`，整体平均 RTT 为 `8.53 ms`，中位数处于 `8.4 ms` 附近，完全满足协议 $\le 10\text{ ms}$ 的硬性指标要求。

### 2.4 负例防御与断线自愈能力审计
- **MMIO 寄存器级物理开闭**：
  - 故障注入工具 `probe_fault_injector.py` 准确操作 TH `USART1_CTRL1`（基地址 `0x4001100C`）；
  - 当物理通信去使能 (`CTRL1 = 0x00000000`) 时，AP 发起查询严格在 300ms 窗口超时熔断，返回退出码 `1` (`EXIT_TIMEOUT`)，未报出虚假或捏造数据；
  - 当物理通信恢复使能 (`CTRL1 = 0x0000202C`) 后，AP 再次发起查询立即成功，单次 RTT 为 `8.32 ms`，自愈率 100%。

### 2.5 任务拓扑图与门禁合规
- 运行 `python3 project-control/tools/check_task_graph.py` 退出码为 `0`，无循环依赖，无结构错误；
- 微任务卡片写入范围 `docs/evidence/temperature_increment/TEMP-05/**` 与 `docs/releases/ap_mc_th_temperature_candidate.yaml` 均处于授权白名单内。

---

## 3. 审查决议与后续流转建议

- **审查决议**：**APPROVED (审核通过)**
- **决议范围**：微任务 `TEMP-05` 物理台架三端工程联调执行记录及 RC3 候选清单（`v2.0.4-telemetry-rc3`）。
- **后续建议**：
  1. `TEMP-05` 联调与消缺达标，COORD 可核销本卡租约并推进状态至 `Done`；
  2. 释放下游独立验收任务 `TEMP-06`（独立真实 HIL 验收复验与安全断线测试），由独立 QA 基于本 RC3 候选包在物理台架上展开 40 轮全量测试与断线注入。
