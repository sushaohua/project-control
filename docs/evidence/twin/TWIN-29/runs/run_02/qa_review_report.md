---
template_version: '2026-10-27'
review_id: TWIN-29-run02-independent-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-29
actual_session: session-qa-twin-29
author_session: session-eng-fwd-twin-29
task_id: TWIN-29
task_revision: 1
run_id: run_02
reviewed_artifact_version: 'soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528'
reviewed_artifacts:
  - path: soc-ap/services/forward/forward_protocol.h
    sha256: 188de250ecbd4a06a44ebcf8909c956cd2878cda16dd3128610718919684ede2
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/forward/forward_protocol.cpp
    sha256: 07abba5cd85a849f2385ef8a8ace4ac6876abde61cacbb926ab95ec15c9a5e96
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.h
    sha256: 0d569c52160f032fd7f78592b36c45f77b439b94146c2c8970bace58a07aba76
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.cpp
    sha256: 77b8cabfa23c26543efe5f787d9757a381c26aa9c3c01cbda246a85c0c9ce942
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_dbus.cpp
    sha256: c501a72527ac23abda9e4f26b0f3eac0c7faaee46731242c3d4ae4cac776964b
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/tests/device_manager/twin/test_device_manager.cpp
    sha256: 8d1875896acdeca1d1f2c40d7ae77c78587c0b4d1131e847fe30581f9762d54b
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/result.md
    sha256: bc53cfbe86ef0b9a7c25998702eecd34c9101a0789ab715a04c9ff5f2bfe3499
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/server_qa/server_qa.json
    sha256: efb4a789a8d71246ac585a61a043ffee80c1e155926a6f8dc57156c33d4a307e
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
server_qa:
  path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/server_qa/server_qa.json
  sha256: efb4a789a8d71246ac585a61a043ffee80c1e155926a6f8dc57156c33d4a307e
content_audit:
  fact_sources:
    result: passed
    basis: "基于 soc-ap Git 候选 86f5e17ead0971ca1a1eb20c07ca345924e24454 与 MiniMCProto v2.0 规格事实来源，双 MCU 版本查询、上报解析、时序衰退及 D-Bus 接口实现均严格溯源。"
  protocol_compatibility:
    result: passed
    basis: "严格遵循 MiniMCProto v2.0 规范，消除了 0x5A/0xA5 非标 SOF 容差分支，强制仅接受 0x55 0xAA；强制 IS_RESPONSE (0x02) 标志校验；超时常数与宏定义完全遵循协议规约。"
  claim_scope:
    result: passed
    basis: "修改范围严格限定于 soc-ap/services/forward/**、soc-ap/services/device_manager/** 及 soc-ap/tests/device_manager/twin/**，无越权修改。"
  architecture_completeness:
    result: passed
    basis: "完整实现 4 态衰退状态机（ONLINE/STALE/OFFLINE/QUERY_FAILED）、拓扑绑定满额防护（非覆盖淘汰）、严守 C/C++ 编码门禁（函数<=50行，参数<=4，防御空指针首行校验，无堆分配）。"
decision: APPROVED
recommendation: APPROVED
reviewed_at: '2026-10-31T14:35:00+08:00'
---
# Independent QA Review Report: TWIN-29 (Run 02)

Decision: **APPROVED**. Candidate soc-ap 86f5e17, project-control 8b2b685. Server QA: 23/23 passed (runtime.log), server_qa.json sha256 efb4a789a8d71246ac585a61a043ffee80c1e155926a6f8dc57156c33d4a307e verified.

## Run_01 defects
- SOF tolerance: 0x5A/0xA5 branch removed; only 0x55 0xAA accepted. Resolved.
- Magic numbers: named constants AISOC_DEV_VER_ONLINE/STALE_TIMEOUT_NS, MINIMC_DEFAULT_HOP_LIMIT, MINIMC_REQ_FLAGS_V2. Resolved.
- IS_RESPONSE: validate now requires the flag. Resolved.
- Binding overflow: slot-0 eviction removed for both grid and version tables; full table returns nullptr (callers return BUSY for version). Resolved. New dev_state_reset_bindings() added for test isolation.
- Alias parsing: unified in resolve_mcu_version_slot. Resolved.

## Standard compliance
New/changed functions <=50 lines, <=4 params, null guards first, no heap, no pointer-increment tricks. Write scope limited to soc-ap services/forward, services/device_manager, tests.

## Non-blocking notes
- Alias parsing in forward_protocol.cpp build_version_query_frame still has its own target string check (different layer).
- Header version bits are still not validated in the response check; CRC covers SOF and header.
