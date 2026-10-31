---
template_version: '2026-10-27'
review_id: TWIN-20-QA-run_02-review
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-20-run02
actual_session: session-qa-twin-20
author_session: session-eng-ui-twin-20
task_id: TWIN-20
task_revision: 2
reviewed_artifact_version:
  run: run_02
  requested_candidates:
    soc-ap: cb70d59e949396f45aec94d33ae23cab75beb282
    project-control: f0fe3948482adb71e5366006850fdb9dd36282bc
    test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
    mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
reviewed_artifacts:
  - {path: soc-ap/browser_hmi/first_release/index.html, sha256: 6a24faf2e0117a9fec14d0bb0f6636cfe2946daffeb1ce1e39fc6ed9d992b487}
  - {path: soc-ap/browser_hmi/first_release/styles.css, sha256: ee9f69c672b749335b7ecbc74b092e82d1c7df05fb70667ac8af548cdf3af2dc}
  - {path: soc-ap/browser_hmi/first_release/app.js, sha256: 7a84520bea0d9f6a305d0990d171e8b19aa6d7bbce6da0bfc4dafd6689ce0bc3}
  - {path: soc-ap/browser_hmi/first_release/slot_schema.json, sha256: 8089dfea214639782542ea36be2cdeb244704e771c637cad49aebde8ffa88417}
  - {path: soc-ap/browser_hmi/first_release/test_hmi_contract.py, sha256: 3653641de36b569d1f928ceb4b3886d4ba36c8c8259f8655a75dd703bf45ddcb}
  - {path: soc-ap/core/net/mdns/mdns_advertiser.h, sha256: e09c1d14aab0176817cda902fc256bcbba8c6d6942a86c7281868f444c4d659f}
  - {path: soc-ap/core/net/mdns/mdns_advertiser.c, sha256: efafc5b0200556bbb2162718aa48825e2e83ebde7e12a8b13424cb4ce28d68f7}
  - {path: soc-ap/core/net/mdns/test_mdns_advertiser.c, sha256: d9f9888d5c9c7d85820101a8978d3089e7de6141b9484f85de9afeabe168b887}
  - {path: project-control/docs/evidence/twin/TWIN-20/runs/run_02/result.md, sha256: 91b3dcac1e2fa6faed698a0011b85818073a2ab43be384859fc22414b056b233}
server_qa:
  path: project-control/docs/evidence/twin/TWIN-20/runs/run_02/server_qa/server_qa.json
  sha256: 4dc55022157ede5084dea36581388fc5edad3bfd5ae97381ad2186b6d9e8523c
content_audit:
  fact_sources:
    result: passed
    basis: "基于 soc-ap 候选提交 cb70d59e949396f45aec94d33ae23cab75beb282 与 project-control 候选 f0fe3948482adb71e5366006850fdb9dd36282bc，在独立 Docker 沙箱中检出并验证。双 MCU 固件版本展示与状态拓扑消费严格溯源自 TWIN-29 规范。"
  protocol_compatibility:
    result: passed
    basis: "前端解析与映射逻辑完全兼容 TWIN-29 REST /api/v1/temperature/snapshot 与 SSE /api/v1/temperature/stream 导出的 devices.mc 与 devices.th 字段，准确提取 firmware_version 与 git_commit 并进行防御性映射。"
  claim_scope:
    result: passed
    basis: "修改范围严格限定于 TWIN-20 授权的 soc-ap/browser_hmi/first_release/** 与 docs/evidence/twin/TWIN-20/** 路径，未越权修改其他文件。"
  architecture_completeness:
    result: passed
    basis: "完整实现了 Sensors 标签页下 MC/TH 双端独立版本展示及 OOBE Step 3 固件通信自检联动；五态时序衰退状态机（ONLINE/STALE/OFFLINE/QUERY_FAILED/UNKNOWN）防御性映射完整，绝无假数据/硬编码/客户端伪造通过。"
decision: APPROVED
recommendation: APPROVED
reviewed_at: '2026-10-31T14:48:00+08:00'
---

# Independent QA Review Report: TWIN-20 (Run 02)

Decision: **APPROVED**. Candidate soc-ap `cb70d59e949396f45aec94d33ae23cab75beb282`, project-control `f0fe3948482adb71e5366006850fdb9dd36282bc`.
Server QA: 4/4 suites pass (Docker Sandbox container `4dc55022...`), 7/7 contract tests pass, mDNS C11 and C++17 unit tests 4/4 pass.

## Key Verifications
1. Real Dual MCU Firmware Version Display: Sensors tab `#th-firmware-version` and `#mc-firmware-version` successfully parse `devices.th` and `devices.mc`, rendering `v{major}.{minor} ({git_commit})`.
2. Defensive 5-State Mapping: ONLINE, STALE, OFFLINE, QUERY_FAILED, and UNKNOWN mapped without hardcoding.
3. OOBE Step 3: Badges and version subtitles update dynamically according to telemetry freshness.
4. i18n Dictionary Parity: All new keys strictly synchronized between zh-CN and en-US with 100% key parity.
