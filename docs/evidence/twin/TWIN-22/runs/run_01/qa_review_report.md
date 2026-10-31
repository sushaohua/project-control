---
template_version: '2026-10-27'
review_id: TWIN-22-run01-independent-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-22
actual_session: session-qa-twin-22
author_session: session-eng-fwd-twin-22
task_id: TWIN-22
task_revision: 1
run_id: run_01
reviewed_artifact_version: 'soc-ap=6850cc553d405b5e7e511ff181d985fdee8e221f; mcu-p3=abbc3ae240972f5a60d751c6204c8b73f1f464bf; project-control=c6a1a21f5711be18cabf85c037d4e30b8bc67cba; test_harness=0b7497ba43158841eb3c4af7f16e477b9c30c2c5'
reviewed_artifacts:
  - path: soc-ap/services/forward/forward_protocol.cpp
    sha256: 5bccbfb4d95ee025628f3299705341a6a60ff30d3b1932e1adabfa2dc009e415
    commit: 6850cc553d405b5e7e511ff181d985fdee8e221f
  - path: soc-ap/services/device_manager/device_manager_state.cpp
    sha256: 678892d4da5a81fa7bf03fd2781d184885f33cc25d89d545f1298299b12e965b
    commit: 6850cc553d405b5e7e511ff181d985fdee8e221f
  - path: soc-ap/tests/device_manager/twin/test_device_manager.cpp
    sha256: b2be13ba63431f9935878b72e1cbdcf389dd56b95c934b69e5c4b08e1acc7bfc
    commit: 6850cc553d405b5e7e511ff181d985fdee8e221f
  - path: project-control/docs/evidence/twin/TWIN-22/runs/run_01/result.md
    sha256: a27f25e27e39f079844b6f4512bb773fe32ede1d14ffd20c3095c475ee9ce753
    commit: c6a1a21f5711be18cabf85c037d4e30b8bc67cba
  - path: project-control/docs/evidence/twin/TWIN-22/runs/run_01/server_qa/server_lock.json
    sha256: 3f985c6d6f7e02c97c737388c9192e75123e28bb3ac781210eed72cde7512c5a
    commit: c6a1a21f5711be18cabf85c037d4e30b8bc67cba
  - path: project-control/docs/evidence/twin/TWIN-22/runs/run_01/server_qa/server_qa.json
    sha256: c51da108e77161032267749bd48e2c491d4fa899d000d47b174b7083c2e9cfae
    commit: c6a1a21f5711be18cabf85c037d4e30b8bc67cba
  - path: project-control/docs/evidence/twin/TWIN-22/runs/run_01/server_qa/server_verdict.json
    sha256: f7c3ddcbda46fde5ddb2032e91c6e23a1d3ab719b3b02547f39c6bcc2c4fcf29
    commit: c6a1a21f5711be18cabf85c037d4e30b8bc67cba
server_qa:
  path: project-control/docs/evidence/twin/TWIN-22/runs/run_01/server_qa/server_qa.json
  sha256: c51da108e77161032267749bd48e2c491d4fa899d000d47b174b7083c2e9cfae
content_audit:
  fact_sources:
    result: passed
    basis: "Verified candidate commit fetched from Git server into isolated Docker container (image qa-sandbox:20261029). Build and test execution cleanly exited 0."
  protocol_compatibility:
    result: passed
    basis: "MiniMCProto 0x14 temperature telemetry deci-Celsius to milli-Celsius (245 deci-C -> 24500 milli-C -> 24.5 C) protocol scale aligned. 0x7FFF (FAULT) and 0x7FFE (OFFLINE) correctly intercepted."
  claim_scope:
    result: passed
    basis: "Edits strictly confined to soc-ap/services/forward, soc-ap/services/device_manager, soc-ap/tests/device_manager/twin, and project-control/docs/evidence/twin/TWIN-22."
  architecture_completeness:
    result: passed
    basis: "Root cause of TWIN-12 245.0 C vs 24.5 C conflict resolved. Toolhead 2147483.6 C and spurious FRESH/OK bug eradicated by formatting fault/offline sentinels as JSON null and setting quality to FAULT/STALE."
protocol_and_expectations:
  - 'TWIN-22 revision 1 review request; first_release_print_closed_loop_and_twin12_investigation.md.'
  - 'delivery_and_coord_gate.md §2, §3.1, §5.1, §5.2; codex_qa_review.md; c_cpp_coding_standard.md.'
verification_environment: 'Container sandbox qa-sandbox:20261029 with read-only source mount from Git server pinned commits; independent host-side review of exported server_qa evidence.'
verification_scope: 'AP Forward protocol temperature unit scaling, Device Manager sentinel formatting/quality assessment, 11/11 automated integration tests.'
required_evidence_level: software-verified
review_time: '2026-10-31 02:48 UTC'
process_audit: completed
result_check: completed
decision: APPROVED
accepted_scope: 'TWIN-22 revision 1 remediation of temperature scaling and sentinel defect in soc-ap at commit 6850cc553d405b5e7e511ff181d985fdee8e221f is APPROVED for software-verified scope.'
limitations:
  - 'Remediation validated at software and mock/DDS level. Full HIL verification against physical MCU boards will take place in integrated milestone test runs.'
unexecuted:
  - 'Physical serial HIL streaming with real hardware (covered in integrated stage).'
not_applicable:
  - item: 'Hardware heating test'
    reason: 'Strong electric heating locked to 0% duty cycle.'
issues: []
commands:
  - command: "cmake -B /tmp/build_devmgr -S tests/device_manager/twin -DCMAKE_CXX_FLAGS='-I/usr/local/include/dbus-1.0 -I/usr/local/lib/dbus-1.0/include' && cmake --build /tmp/build_devmgr"
    cwd: '/workspace/soc-ap'
    tool_version: 'cmake 3.28.3, g++ 9.4.0'
    time: '2026-10-31 02:46 UTC'
    exit_code: 0
    output: 'Built target test_device_manager'
  - command: '/tmp/build_devmgr/test_device_manager'
    cwd: '/workspace/soc-ap'
    tool_version: 'g++ test binary'
    time: '2026-10-31 02:46 UTC'
    exit_code: 0
    output: 'Total: Passed=11, Failed=0'
  - command: 'PYTHONDONTWRITEBYTECODE=1 python3 tools/check_task_graph.py --workspace ..'
    cwd: '/workspace/project-control'
    tool_version: 'Python 3.8.10'
    time: '2026-10-31 02:46 UTC'
    exit_code: 0
    output: 'canonical_task_count: 110, microtask_count: 68, errors: []'
---

# TWIN-22 独立 QA 审查报告

## 1. 审查背景与结论

依据 `project-control/.agents/rules/codex_qa_review.md` 及 `delivery_and_coord_gate.md`，独立 QA 席位（`session-qa-twin-22`, `model: gpt-6-luna`）对微任务 `TWIN-22`（AP 温度单位缩放与哨兵异常修复）进行了全方位独立代码审计与容器沙箱物证核验。

**QA 审查裁决**：**`APPROVED`（审核通过）**。

---

## 2. 核心缺陷根因核验与修复项

1. **TWIN-12 热床 245.0℃ 异常对账解决**：
   - 彻底移除了原 `forward_protocol.cpp` 中存在严重缺陷的启发式单位猜测逻辑（`> 1000 * 10` 则盲目乘 100）；
   - 统一使用 `telemetry_deci_to_millic` 转换函数，确保 MCU 上报的 `245`（0.1℃ 单精度整型）准确转换为 `24500`（milli-Celsius），使 AP 快照与 JSON 导出准确对应为 `24.5℃`。

2. **工具头 2147483.6℃ 哨兵泄露与虚假 OK/FRESH 根除**：
   - 固件在传感器掉线/故障时填入哨兵 `0x7FFF` / `0x7FFE`，在转换前被 `fwd_proto_parse_raw_temp()` 精确拦截；
   - `device_manager_state.cpp` 中新增 `format_temp_c_val()`，针对 `0x7FFFFFFF` / `0x7FFFFFFE` 哨兵直接向 JSON 输出 `null`，彻底杜绝 `2147483.6` 荒谬浮点值外溢；
   - `eval_sample_quality()` 严格将哨兵数据降级为 `FAULT` 或 `STALE`，系统运行状态同步降级为 `DEGRADED`，绝不再标记为 `OK` 或 `FRESH`。

3. **编码硬门禁符合性 (`c_cpp_coding_standard.md`)**：
   - 所有自研及修改函数（`fwd_proto_parse_raw_temp`、`eval_sample_quality`、`format_temp_c_val`、`update_system_status_desc`）严格控制在 30 行以内（$\le 50$ 行），入参 $\le 3$ 个（$\le 4$ 个）；
   - 首行均包含防御性空指针判断，无动态堆分配，无多重指针。

4. **自动化单测与回归闭环**：
   - `test_device_manager.cpp` 包含 11 个测试套件，全面覆盖 24.5℃ 正例缩放、0x7FFF 故障拦截、0x7FFE 离线拦截、DDS 状态降级与 D-Bus RPC 远程快照获取，11 项单测全部 PASS。

---

## 3. 容器沙箱物证对账

- **Container Image**: `qa-sandbox:20261029`
- **Candidate Commit**: `soc-ap: 6850cc553d405b5e7e511ff181d985fdee8e221f`
- **Server Lock SHA256**: `3f985c6d6f7e02c97c737388c9192e75123e28bb3ac781210eed72cde7512c5a`
- **Server QA SHA256**: `c51da108e77161032267749bd48e2c491d4fa899d000d47b174b7083c2e9cfae`
- **Verdict**: Build exit 0, test exit 0 (Passed=11, Failed=0). All regression suites passed.
