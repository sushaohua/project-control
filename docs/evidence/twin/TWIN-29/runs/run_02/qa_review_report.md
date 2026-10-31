---
template_version: '2026-10-27'
review_id: TWIN-29-run02-independent-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
planned_session_alias: planned-qa-twin-29
actual_session: session-qa-twin-29
author_session: session-eng-fwd-twin-29
task_id: TWIN-29
task_revision: 1
run_id: run_02
reviewed_artifact_version: 'soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454; project-control=8b2b685d8232e4b0485740e7fe1268f544fa0528'
reviewed_artifacts:
  - path: soc-ap/services/forward/forward_protocol.h
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/forward/forward_protocol.cpp
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.h
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_state.cpp
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/services/device_manager/device_manager_dbus.cpp
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: soc-ap/tests/device_manager/twin/test_device_manager.cpp
    commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_02/server_qa/server_qa.json
    sha256: efb4a789a8d71246ac585a61a043ffee80c1e155926a6f8dc57156c33d4a307e
    commit: 8b2b685d8232e4b0485740e7fe1268f544fa0528
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
