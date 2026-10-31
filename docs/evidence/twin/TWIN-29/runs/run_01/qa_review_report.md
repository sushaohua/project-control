---
template_version: '2026-10-27'
review_id: TWIN-29-run01-independent-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
planned_session_alias: planned-qa-twin-29
actual_session: session-qa-twin-29
author_session: session-eng-fwd-twin-29
task_id: TWIN-29
task_revision: 1
run_id: run_01
reviewed_artifact_version: 'soc-ap=594ffab12902ac5b38a6f1a6dd869da0942c8dbb; project-control=859c6eaaf93962a04b2464123cde205e67f16ecb'
reviewed_artifacts:
  - path: soc-ap/services/forward/forward_protocol.h
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: soc-ap/services/forward/forward_protocol.cpp
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: soc-ap/services/device_manager/device_manager_state.h
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: soc-ap/services/device_manager/device_manager_state.cpp
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: soc-ap/services/device_manager/device_manager_dbus.cpp
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: soc-ap/tests/device_manager/twin/test_device_manager.cpp
    commit: 594ffab12902ac5b38a6f1a6dd869da0942c8dbb
  - path: project-control/docs/evidence/twin/TWIN-29/runs/run_01/server_qa/server_qa.json
    sha256: f4a8f96313a89840341cdab77661571ff9c317b7cb135ec1c64f40b611b926c3
    commit: 859c6eaaf93962a04b2464123cde205e67f16ecb
decision: REJECTED
recommendation: REJECTED
reviewed_at: '2026-10-31T12:55:00+08:00'
---
# Independent QA Review Report: TWIN-29 (Run 01)

Decision: **REJECTED** (two hard-gate defects, both small). Server QA evidence itself is sound: 22/22 tests pass in isolated container, candidate commits fetched from the server.

## Verified OK
- Scope: diff f259651..594ffab touches only soc-ap services/forward, services/device_manager, tests/device_manager/twin.
- 0x01 query: SOF 55 AA, src=AP, dst=MC/TH, flags=0x05, cmd 0x01, payload_len 0, built via the shared codec encode_frame (CRC16 little-endian, coverage = SOF..payload, same as codec). Matches v2-commands.md §3.1.
- 0x02 response: 30B length, src/dst/cmd/seq/payload_len=16 checks, CRC over bytes 0..27 compared little-endian. 16B payload parse layout matches §3.2.
- 4-state freshness: <5s ONLINE, <15s STALE, else OFFLINE; never-valid -> OFFLINE; QUERY_FAILED preserved. Logic correct.
- No heap, no pointer-increment tricks, null guards first in public functions, all new functions <=50 lines and <=4 params. No hardcoded/mock versions: version data enters only via update_mcu_version; default is UNKNOWN/zeros.

## Findings (blocking)
1. **SOF tolerance (spec deviation)**: fwd_proto_validate_version_response accepts SOF 0x5A 0xA5 in addition to 0x55 0xAA. v2-commands.md requires 0x55 0xAA and silent drop on magic mismatch. Remove the 0x5A/0xA5 branch (and any test relying on it).
2. **Magic numbers (c_cpp_coding_standard hard gate)**: freshness thresholds 5000000000ULL / 15000000000ULL, header literals 0x05U (flags), hop_limit 10U, and 0x5AU/0xA5U in new code should be named constants.

## Non-blocking notes
- validate_version_response does not check flags (IS_RESPONSE) or header version bits; CRC does cover SOF and header.
- find_or_create_version_binding silently evicts slot 0 when the table is full (should return BUSY). Pointer-keyed binding table is a workaround for the unchanged state struct.
- Target/node string parsing ("1"/"2" aliases) is duplicated in three places.
