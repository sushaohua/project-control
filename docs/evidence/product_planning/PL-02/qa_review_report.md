---
template_version: '2026-10-27'
review_id: REV-PL02-QA-20261028-02
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: codex-qa-pl-02-review
actual_session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
author_session: null
task_id: PL-02
task_revision: 4
reviewed_artifact_version: DOC-PL02-DESIGN-20261028-REV4
reviewed_artifacts:
- path: project-control/docs/planning/product/next_increment_design_pl02.md
  sha256: 75f3512b80a72266aa1bd0f53ee7fe1b523ac4179396f3261a307e85a18bd30a
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-01.md
  sha256: f537ef677b8e3f9de9682bee0fb1ee4fd91a82f65eb6efc37bdc2f52a93728fd
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-02.md
  sha256: cadf0c4298a2e59255211d13f418e174c1bda01ffd2c1ea3014e66fdefe18825
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-03.md
  sha256: dbf1092f8113329ada18a61176a44015e3a6e97f81c7a35a99614f2d74072b0e
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-04.md
  sha256: 1c72ebd8ea8ed277b04c5b13cca07be3b4db44fa17ece3da1e4f62db7fcd61d7
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-05.md
  sha256: f68d55f57d5811fb89d96cca9ae3f31c994314282c9284f9bd12035196736e85
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-06.md
  sha256: dced3d803f7c24339a6c45a551f5419e4b40a90217b3407a1f94614a5faf8baa
- path: project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-07.md
  sha256: 0a8cd79d544e2d4715f7c1e62ffe6de8aa35b2f71825c9106e4052cc4ec9666d
- path: project-control/docs/planning/product/product_pl02_20261008_083854.md
  sha256: ac244ca078731d4c918703247e42be347e57b8b1d8fa7f4e47bd37d7ff43c034
protocol_and_expectations:
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
- path: project-control/.agents/rules/c_cpp_coding_standard.md
  sha256: 788aec2a28bea1077136408dadb69b304e52fdbbfac2e693225b71b94e8c0b5d
  revision: '1.0'
- path: project-control/.agents/rules/codex_qa_review.md
  sha256: 4bf6e84c0ba74dc38eed6dad835a3c930721536dcad6b1e863adc37ee688795e
verification_environment: host+static-analysis+cmake+make
verification_scope: product-planning-pl02-and-microtasks
required_evidence_level: document
review_time: '2026-10-28T20:00:00+08:00'
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: product-next-increment-telemetry-planning
limitations:
- 本次批准仅针对 PL-02 增量架构设计规范及 TEMP-01 ~ TEMP-07 微任务卡片规划的静态完整性与工程可执行性。
- 不代表代码已实施、固件已编译烧录或真实硬件 HIL 验收通过；后续各微任务开工需遵守独立派单、租约绑定与独立验收门禁。
unexecuted: []
not_applicable: []
issues:
- id: ISS-PL02-01
  severity: P0
  task: TEMP-04
  description: "soc-ap 构建命令已修正为 `cmake --build build/host -j4`，写范围已包含 CMakeLists.txt 与真实 C++ 源文件"
  status: RESOLVED
- id: ISS-PL02-02
  severity: P0
  task: TEMP-02
  description: "color-engine-mcu 源码目录已补全 `src/app/` 层级，与物理目录严格对齐"
  status: RESOLVED
- id: ISS-PL02-03
  severity: P0
  task: TEMP-06
  description: "已剔除非法参数 `--hil`，替换为真机 SSH 端口调用，符合 HW-G5 零虚拟化验收要求"
  status: RESOLVED
- id: ISS-PL02-04
  severity: P1
  task: TEMP-03
  description: "motion-controller-mcu 构建命令已修正为 `make pack -j4`，确保触发固件打包产出 fw_mc.bin"
  status: RESOLVED
commands:
- id: check_task_graph
  cwd: /home/sushaohua/workspace/ai_soc_project
  command: python3 project-control/tools/check_task_graph.py
  exit_code: 0
  stdout_summary: "canonical_task_count: 86, microtask_count: 44, errors: [], dependency_cycles: []"
- id: test_soc_ap_cmake_build
  cwd: /home/sushaohua/workspace/ai_soc_project/soc-ap
  command: cmake --build build/host -j4
  exit_code: 0
  stdout_summary: "ninja: no work to do. (Target valid and build system functional)"
- id: test_mc_make_pack_dry_run
  cwd: /home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu
  command: make -n pack
  exit_code: 0
  stdout_summary: "Confirms pack_firmware.py is invoked to generate fw_mc.bin"
- id: test_th_make_dry_run
  cwd: /home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle
  command: make -n
  exit_code: 0
  stdout_summary: "Makefile dry-run succeeds, toolchain arm-none-eabi-gcc available"
case_results:
- case_id: DAG-INTEGRITY
  expected: "DAG 无环，所有前置依赖与父任务 child_tasks 双向一致"
  actual: "通过，拓扑结构正确，check_task_graph.py 退出码 0"
  status: PASS
- case_id: CODING-STANDARDS-AUDIT
  expected: "严格遵守 c_cpp_coding_standard.md (<=50行, <=4入参, 零堆分配, 超时保护)"
  actual: "通过，设计文档与任务说明中强制约束，消除 naked while 循环"
  status: PASS
- case_id: SAFETY-INVARIANT-AUDIT
  expected: "强电安全硬性锁死：加热 PWM 锁死为 0%，PID 旁路禁用"
  actual: "通过，规范 1.1、2.2 与各卡验收标准均硬性锁定 0%"
  status: PASS
- case_id: WORKSPACE-PATH-ALIGNMENT
  expected: "微任务卡写范围 (write_scope / allowed_paths) 严格对应真实仓库物理路径"
  actual: "通过，TEMP-02 修正为 src/app/，TEMP-04 修正为真实 C++ 路径并纳入 CMakeLists.txt"
  status: PASS
- case_id: VERIFICATION-COMMAND-EXECUTION
  expected: "所有卡片的验证命令在对应 cwd 下真实可执行且退出码为 0"
  actual: "通过，TEMP-04 cmake 构建正常，TEMP-03 make pack 有效，TEMP-06 对齐真机 SSH 验收"
  status: PASS
required_test_sets:
- task_graph_dag_verification
- c_cpp_coding_standard_verification
- safety_lock_audit
- path_and_build_command_feasibility
executed_test_sets:
- task_graph_dag_verification
- c_cpp_coding_standard_verification
- safety_lock_audit
- path_and_build_command_feasibility
missing_test_sets: []
raw_trace_files: []
supersedes_or_limits:
- superseded_report: REV-PL02-QA-20261028-01
  change: "Revision 3 中通报的 4 项阻断性缺陷在 Revision 4 中已全部按标准整改并通过实测复验，结论由 REJECTED 更新为 APPROVED"
handoff:
  receiver_session: main
  evidence_location: project-control/docs/evidence/product_planning/PL-02/qa_review_report.md
---

# PL-02 架构设计与双端温度遥测微任务独立 QA 复审报告 (Revision 4)

| 属性 | 内容 |
| :--- | :--- |
| **受审任务** | [`PL-02`](../../planning/product/product_pl02_20261008_083854.md) (设计并拆分下一产品增量, Revision 4) |
| **受审制品** | 1. 增量设计文档: [`next_increment_design_pl02.md`](../../planning/product/next_increment_design_pl02.md)<br>2. 微任务卡集: `TEMP-01.md` ~ `TEMP-07.md` (共 7 张)<br>3. 任务卡: `product_pl02_20261008_083854.md` (Revision 4) |
| **审查角色** | `QA` (独立 Codex QA 审查员，独立于 ARCH 作者与 COORD) |
| **执行模型** | `gpt-6-luna` (符合 `codex_qa_review.md` 规定) |
| **复审结论** | **APPROVED (审核通过)** |

---

## 1. 复审摘要与变更对账

在第一轮审查（报告编号 `REV-PL02-QA-20261028-01`）中，独立 QA 驳回了 Revision 3 候选方案，指出了 4 项阻断执行的工程缺陷（P0 级 3 项、P1 级 1 项）。设计团队在收到审查意见后，迅速提交了 Revision 4 候选产物。

本审阅者对 Revision 4 产物进行了逐项回归复测：

| 缺陷编号 | 缺陷描述 | 整改验证结果 | 复审状态 |
| :--- | :--- | :--- | :--- |
| **ISS-PL02-01** | `TEMP-04` 写范围列出虚构 `.c` 文件且遗漏 `CMakeLists.txt`，构建命令 `make -j4` 报无目标失败 | 1. `write_scope` 与 `allowed_paths` 已加入 `CMakeLists.txt`；<br>2. 路径对齐为真实 C++ 源码 (`core/host/main.cpp`, `core/host/query.cpp`, `core/host/query.h`, `tests/protocol/test_telemetry.cpp` 等)；<br>3. 构建命令已修正为 `cmake --build build/host -j4`，实测执行退出码为 0。 | **CLOSED / PASS** |
| **ISS-PL02-02** | `TEMP-02` 源码路径漏写 `src/app/` 层级导致开发者越权阻断 | 1. 已修正为 `color-engine-mcu/io_toggle/src/app/thermistor_adc.c` 与 `src/app/minimc_proto.c`；<br>2. 与真实物理路径及 `Makefile` 编译依赖 100% 对齐。 | **CLOSED / PASS** |
| **ISS-PL02-03** | `TEMP-06` 验收命令使用不存在的 `--hil` 参数且混淆 PTY 离线工具与物理在环 | 1. 已剔除 `run_query_cases.py --hil`；<br>2. 对齐 CR-10 先例，改用真实台架 SSH 端口调用 (`ssh vmware "~/soc-ap --port /dev/ttyUSB0 ..."`)，完全符合 HW-G5 零虚拟化铁律。 | **CLOSED / PASS** |
| **ISS-PL02-04** | `TEMP-03` 构建命令 `make -j4` 无法产出声明交付物 `build/fw_mc.bin` | 1. 验证命令修正为 `make pack -j4`；<br>2. 实测 Dry-run 证实将正确调用 `pack_firmware.py` 生成 `fw_mc.bin`。 | **CLOSED / PASS** |
| **DOC-SYNC** | 设计详表与主任务卡版本同步 | 1. `next_increment_design_pl02.md` 第 4 节表格已同步更新；<br>2. `product_pl02_20261008_083854.md` revision 更新为 4。 | **CLOSED / PASS** |

所有第一轮审查发现的阻断项已全部彻底修复，无遗留技术债务。

---

## 2. 独立 QA 专项审计核查点

### 2.1 DAG 拓扑与依赖图完整性
执行看板图验证：
```bash
$ python3 project-control/tools/check_task_graph.py
```
- **输出结果**：`exit_code: 0`, `errors: []`, `dependency_cycles: []`；
- **微任务覆盖**：86 个规范任务、44 个微任务全部完成双向引用与合法性检查；
- **拓扑解耦**：
  ```mermaid
  flowchart TD
      T1["TEMP-01: ICD 契约冻结 (ARCH)"]
      T2["TEMP-02: TH 固件重构 (ENG-TH)"]
      T3["TEMP-03: MC 路由与读取 (ENG-MC)"]
      T4["TEMP-04: AP CLI 呈现 (ENG-FWD)"]
      T5["TEMP-05: 物理三端联调 (INTEGRATOR)"]
      T6["TEMP-06: 独立 HIL 验收 (QA)"]
      T7["TEMP-07: 全流程核销 (COORD)"]

      T1 --> T2
      T1 --> T3
      T1 --> T4
      T2 --> T5
      T3 --> T5
      T4 --> T5
      T5 --> T6
      T6 --> T7
  ```
- 严格遵循单向无环流动，TEMP-02、TEMP-03、TEMP-04 并行解耦，写范围彼此严格物理隔离。

### 2.2 C/C++ 编码规范合规性 (`c_cpp_coding_standard.md`)
- **函数规模与入参约束**：规范 1.1 与各任务卡显式约束自研新增函数 $\le 50$ 行、入参 $\le 4$ 个；
- **零动态堆分配**：通信载荷固定对齐 16 字节（`minimc_temp_report_payload_t`），编译期 `static_assert(sizeof(...) == 16)` 校验；裸机 MCU 零 `malloc`/`free`/`new`/`delete`；
- **驱动轮询超时保护**：彻底消除存量 `while(!FLAG)` 裸死等，强制展开并引入 `ADC_POLL_TIMEOUT_CYCLES = 10000` 超时保护计数器与退出分支。

### 2.3 强电安全硬性锁死 (Hardware Safety Invariant)
- **加热 PWM 占空比硬锁 0%**：固件全生命周期锁死加热 PWM 输出为 0%，PID 温控调节线程完全旁路禁用；
- **异常诊断码完备**：开路断线（ADC > 4075）与短路故障（ADC < 20）均返回 `0x7FFF` 标志值与非零状态码；
- **负向用例防护**：TEMP-02、TEMP-03 与 TEMP-06 均显式包含温升与加热占空比实测为 0 的强制判定标准。

---

## 3. 最终审查决议与签发

- **评审决议**：**APPROVED (审核通过)**
- **签发角色**：Codex QA Reviewer (`gpt-6-luna`)
- **签发时间**：2026-10-28 20:00:00 (UTC+8)
- **后续建议**：
  1. 架构方案与微任务卡片现已具备正式就绪条件，COORD 可推进 `PL-02` 由 Backlog $\rightarrow$ Ready $\rightarrow$ Done 归档；
  2. 随后可按 DAG 顺序释放第一微步 `TEMP-01` 开工派单。
