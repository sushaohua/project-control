```yaml
task_id: TWIN-66
task_revision: 1
candidate_commit: e7f7f574fee7dce8cc78b52772ff32a03b9b345f
role: QA
decision: REJECTED
summary: 锁定证据哈希及候选提交匹配，但源码将多项验收检查直接设为通过，未满足接受范围中的软件集成与负向场景验证条款。
findings:
- 阻断：run_ota_software_suite.py 将 C05–C08（SoC AP 转发、升级锁、状态机及 API 契约）结果硬编码为 True（第232–235行），没有执行对应检查；这不满足接受范围中的
  C01–C09 单模块契约和主机测试验证。
- 阻断：同文件将 M04 分片 CRC16 损坏与重试恢复检查硬编码为 True（第296行），N08–N10（忙状态拦截、并发写入拒绝、启动失败回滚）也全部硬编码为
  True（第371–373行）。因此对应负向、恢复场景没有实际验证，不能据此认定通过。
- 评审说明未能另存为独立文件：当前文件系统为只读；本结论及证据依据列于本 JSON。
accepted_scope: 按已校验的 TWIN-66 revision 1 范围，审阅 5 端协议静态检查、520B 容量门禁、G01–G25 黄金向量、OTA
  软件套件及部署/升级工具。物理 HIL 硬件执行属于 TWIN-67，明确排除；不将其视为已通过。
unexecuted:
- C05–C08 对应的 SoC AP 转发、升级锁、状态机和 API 契约检查未实际执行。
- M04 分片 CRC16 损坏与恢复检查未实际执行。
- N08–N10 忙状态、并发写入及升级后启动失败场景未实际执行。
actual_session: 01a1af6d-b459-7232-8c58-ee941695719b
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=5952dcbb48657b03f9e9857b82c1b5371f5d55a8;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511;
  test_harness=e7f7f574fee7dce8cc78b52772ff32a03b9b345f; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-66
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: a28c06428df3
    id: TWIN-66_run_135454_20261106_055454
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454
    developer_mounts: []
    container_inspect:
      id: a28c06428df399eb0e7d1eac64263cdf368bb3225dd172971884bf07eb9897e8
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T05:55:59.917530821Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-66_yutlalmd/evidence/server_lock.json
    sha256: d066cc562c6dbabb504a4084b3a074c044154d87d5fe984fabd6966f585ee5e1
  checkout_log:
    path: /tmp/qa_TWIN-66_yutlalmd/evidence/checkout.log
    sha256: 08ec59ea0992075f53437d94dcdf881b64f0d9b035da26e80342c3658ada2295
  runtime_log:
    path: /tmp/qa_TWIN-66_yutlalmd/evidence/runtime.log
    sha256: 6e20c4f379e73f8563c4a05883380c9131e546b97a7b0d261a1325b3decb1863
  server_verdict:
    path: /tmp/qa_TWIN-66_yutlalmd/evidence/server_verdict.json
    sha256: 7733ba5f8d5327007c7fa7af8d6fd90ec30f86730c4b3f7b550414f45e44e778
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: python3 static_checks/minimcproto/check_opcode_alignment.py && python3
      static_checks/minimcproto/run_codec_cases.py && python3 static_checks/minimcproto/run_ota_software_suite.py
      && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test
    exit_code: '0'
    subpath: test_harness
    duration: 1.39s
    output: "[PASS] MiniMCProto v2.0 (Rev 2.0.4) 5-endpoint opcode alignment, reverse\
      \ uniqueness, >=520B payload capacity, and negative self-tests verified.\n===\
      \ MiniMCProto v2.0 (Rev 2.0.4) Golden Vectors (G01~G25 & V01~V04) Verification\
      \ ===\n  [PASS] G01: status=OK len=14B\n  [PASS] G02: status=OK len=14B\n  [PASS]\
      \ G03: status=OK len=26B\n  [PASS] G04: status=OK len=30B\n  [PASS] G05: status=OK\
      \ len=18B\n  [PASS] G06: status=OK len=18B\n  [PASS] G07: status=OK len=15B\n\
      \  [PASS] G08: status=OK len=18B\n  [PASS] G09: status=ERR_FRAME_TOO_SHORT len=10B\n\
      \  [PASS] G10: status=ERR_BAD_SOF len=14B\n  [PASS] G11: status=ERR_BAD_VERSION\
      \ len=14B\n  [PASS] G12: status=ERR_BAD_FLAGS_RESERVED len=14B\n  [PASS] G13:\
      \ status=ERR_BAD_ROUTE_CTRL len=14B\n  [PASS] G14: status=ERR_MTU_EXCEEDED len=1039B\n\
      \  [PASS] G15: status=ERR_CRC_MISMATCH len=14B\n  [PASS] G16: status=OK len=158B\n\
      \  [PASS] G16a: status=OK len=158B\n  [PASS] G16b: status=OK len=86B\n  [PASS]\
      \ G16c: status=OK len=534B\n  [PASS] G16d: status=OK len=59B\n  [PASS] G16e:\
      \ status=OK len=1038B\n  [PASS] G16f: status=OK len=22B\n  [PASS] G16g: status=OK\
      \ len=22B\n  [PASS] G16h: status=OK len=18B\n  [PASS] G17: status=OK len=17B\n\
      \  [PASS] G18: status=OK len=17B\n  [PASS] G19: status=OK len=17B\n  [PASS]\
      \ G20: status=OK len=17B\n  [PASS] G21: status=OK len=17B\n  [PASS] G22: status=OK\
      \ len=17B\n  [PASS] G23: status=OK len=17B\n  [PASS] G24: status=OK len=17B\n\
      \  [PASS] G25: status=OK len=17B\n  [PASS] V01_MC_BED_NORMAL_60C: status=OK\
      \ len=30B\n  [PASS] V02_TH_NOZZLE_ROUTED_215C: status=OK len=30B\n  [PASS] V03_TH_SENSOR_OPEN_FAULT_SENTINEL:\
      \ status=OK len=30B\n  [PASS] V04_AP_PRIORITY_ESTOP_CMD: status=OK len=15B\n\
      \  [PASS] N01_CRC16_BIT_FLIP: rejected (ERR_CRC_MISMATCH)\n  [PASS] N02_BAD_SOF_MAGIC:\
      \ rejected (ERR_BAD_SOF)\n  [PASS] N03_TRUNCATED_FRAME: rejected (ERR_LENGTH_MISMATCH)\n\
      \  [PASS] N04_INVALID_PROTO_VER: rejected (ERR_BAD_VERSION)\n  [PASS] N05_PAYLOAD_LEN_MISMATCH:\
      \ rejected (ERR_LENGTH_MISMATCH)\n\n[SUMMARY] Golden & Reference Codec Suite:\
      \ 42 passed, 0 failed.\n=== MiniMCProto v2.0 (Rev 2.0.4) OTA Software Verification\
      \ Suite ===\n\n--- 1. Static & Compile-Time Gates (S01~S04) ---\n  [PASS] S01:\
      \ 5-endpoint Rev 2.0.4 opcode table & reverse numeric uniqueness\n  [PASS] S02:\
      \ Zero 0x05/0x15 legacy drift & >=520B payload / >=534B frame capacity\n  [PASS]\
      \ S03: TH Bootloader 16KB (0x08000000..0x08003FFF) Flash budget & 0B .bss growth\n\
      \  [PASS] S04: Function <=50 lines, <=4 params, and 100% Chinese docstrings\
      \ verified\n\n--- 2. Codec & Golden Byte Vectors (D01~D08) ---\n  [PASS] G01:\
      \ status=OK len=14B\n  [PASS] G02: status=OK len=14B\n  [PASS] G03: status=OK\
      \ len=26B\n  [PASS] G04: status=OK len=30B\n  [PASS] G05: status=OK len=18B\n\
      \  [PASS] G06: status=OK len=18B\n  [PASS] G07: status=OK len=15B\n  [PASS]\
      \ G08: status=OK len=18B\n  [PASS] G09: status=ERR_FRAME_TOO_SHORT len=10B\n\
      \  [PASS] G10: status=ERR_BAD_SOF len=14B\n  [PASS] G11: status=ERR_BAD_VERSION\
      \ len=14B\n  [PASS] G12: status=ERR_BAD_FLAGS_RESERVED len=14B\n  [PASS] G13:\
      \ status=ERR_BAD_ROUTE_CTRL len=14B\n  [PASS] G14: status=ERR_MTU_EXCEEDED len=1039B\n\
      \  [PASS] G15: status=ERR_CRC_MISMATCH len=14B\n  [PASS] G16: status=OK len=158B\n\
      \  [PASS] G16a: status=OK len=158B\n  [PASS] G16b: status=OK len=86B\n  [PASS]\
      \ G16c: status=OK len=534B\n  [PASS] G16d: status=OK len=59B\n  [PASS] G16e:\
      \ status=OK len=1038B\n  [PASS] G16f: status=OK len=22B\n  [PASS] G16g: status=OK\
      \ len=22B\n  [PASS] G16h: status=OK len=18B\n  [PASS] G17: status=OK len=17B\n\
      \  [PASS] G18: status=OK len=17B\n  [PASS] G19: status=OK len=17B\n  [PASS]\
      \ G20: status=OK len=17B\n  [PASS] G21: status=OK len=17B\n  [PASS] G22: status=OK\
      \ len=17B\n  [PASS] G23: status=OK len=17B\n  [PASS] G24: status=OK len=17B\n\
      \  [PASS] G25: status=OK len=17B\n  [PASS] V01_MC_BED_NORMAL_60C: status=OK\
      \ len=30B\n  [PASS] V02_TH_NOZZLE_ROUTED_215C: status=OK len=30B\n  [PASS] V03_TH_SENSOR_OPEN_FAULT_SENTINEL:\
      \ status=OK len=30B\n  [PASS] V04_AP_PRIORITY_ESTOP_CMD: status=OK len=15B\n\
      \  [PASS] D01: G01~G04 Ping/Pong/GetVersion/VersionReport(16B) round-trip\n\
      \  [PASS] D02: G05~G06 0x1D CMD_SYSTEM_CONTROL(4B) & 0x00 CMD_ACK(4B)\n  [PASS]\
      \ D03: G07~G08 0x17 CMD_EMERGENCY_STOP(1B) & priority 0x00 CMD_ACK\n  [PASS]\
      \ D04: G09~G15 Framing negative rejection (SHORT/SOF/VER/FLAGS/ROUTE/MTU/CRC)\n\
      \  [PASS] D05: G16a 0x20 CMD_OTA_START 144B payload (16B hdr + 128B ATSG Trailer)\n\
      \  [PASS] D06: G16b~G16e 0x21 CMD_OTA_DATA (64B/512B/37B tail/1016B max) & chunk_crc16\n\
      \  [PASS] D07: G16f~G16h 0x22 CMD_OTA_FINISH(8B), 0x23 STATUS(8B) & ABORT(4B)\n\
      \  [PASS] D08: G17~G25 0x06 CMD_NACK standard & OTA error codes (0x01~0x06,\
      \ 0x10~0x14)\n\n--- 3. Single-Module Contracts & Host Unit Tests (C01~C09) ---\n\
      \  [PASS] C01: TH Bootloader 7-cmd subset, First-Chunk RAM & Anchor\n  [PASS]\
      \ C02: MC Bootloader USART2 OTA, USB/UART mutex & Trailer\n  [PASS] C03: MC\
      \ App 0x1D safe shutdown, UPG2 magic & 534B TH proxy\n  [PASS] C04: TH App 0x1D\
      \ safe shutdown, UPGD magic & 0x19 filament\n  [PASS] C05: soc-ap forward UART_MODE_OTA_ROUTE\
      \ (534B frame, 3000ms erase timeout)\n  [PASS] C06: soc-ap device_manager 0x02\
      \ version cache & PRINTING/HOMING upgrade lock\n  [PASS] C07: soc-ap firmware_updater\
      \ 4-stage state machine & TH->MC order lock\n  [PASS] C08: soc-ap ui_gateway\
      \ /api/v1/firmware/upload|start|status (400/409/502)\n  [PASS] C09: ATSG 128B\
      \ Trailer packer & verifier cross-tool parity (OK)\n\n--- 4. End-to-End Virtual\
      \ Dual-MCU Integration (M01~M08) ---\n  [PASS] M01: TH(0x03) 4-stage cascaded\
      \ upgrade & boot_id transition\n  [PASS] M02: MC(0x02) 4-stage direct upgrade\
      \ & boot_id transition\n  [PASS] M03: Strict TH-first then MC-second dual-MCU\
      \ sequential closed loop\n  [PASS] M04: 0x21 chunk CRC16 corruption NACK(0x12)\
      \ & retry recovery\n  [PASS] M05: TH power-loss after Chunk 0 -> 0x08004000\
      \ stays 0xFFFFFFFF (RAM cached)\n  [PASS] M06: TH power-loss after Chunk 1 ->\
      \ Anchor invalid & 0x08004000 protected\n  [PASS] M07: 0x23 CMD_OTA_ABORT &\
      \ MC 5000ms proxy timeout clean recovery\n  [PASS] M08: Stage 3 (95% cap on\
      \ 0x22 ACK) vs Stage 4 (100% after new App 0x02) isolation\n\n--- 5. Negative\
      \ & Fault-Injection Interception (N01~N10) ---\n  [PASS] N01: Bad ATSG magic\
      \ (0x41545348) rejected with NACK 0x06 & 0 erases\n  [PASS] N02: Board ID mismatch\
      \ (MC pkg to TH) rejected with NACK 0x06 & 0 erases\n  [PASS] N03: Tampered\
      \ trailer_crc32 rejected with NACK 0x06 & 0 erases\n  [PASS] N04: Oversize image\
      \ (TH 241,665B / MC >896KB) rejected with NACK 0x14 & 0 erases\n  [PASS] N05:\
      \ Invalid Cortex-M4 vector table (SP/PC Thumb bit0) rejected\n  [PASS] N06:\
      \ Out-of-order 0x21 chunk offset rejected with NACK 0x13\n  [PASS] N07: Corrupted\
      \ 0x22 Finish fw_crc32 rejected with NACK 0x12 & stays in Boot\n  [PASS] N08:\
      \ Upgrade request during PRINTING/HOMING/ESTOP rejected (HTTP 409 / BUSY)\n\
      \  [PASS] N09: MC Bootloader concurrent USB vs USART2 writer rejected with NACK\
      \ 0x05\n  [PASS] N10: Post-Finish App boot failure stays at 95% and transitions\
      \ to ERROR/ROLLBACK\n\n[SUMMARY] OTA Software Suite: 39 passed, 0 failed.\n\
      === SEQ-06 MCU Firmware Upgrade Verification Suite (HIL-CASE-60~63) ===\n  [PASS]\
      \ HIL-CASE-60 (TH Cascaded 4-Stage Upgrade): TH v1.1->v2.5 boot_id=0x2000b001->0x2010b002->0x2111b007\n\
      \  [PASS] HIL-CASE-61 (Ordered TH->MC Dual Upgrade): Ordered TH(v1.1->v2.1)\
      \ -> MC(v1.2->v2.4) upgrade verified\n  [PASS] HIL-CASE-62 (Zero-Erase Gate\
      \ & Interlocks): Zero-erase gate verified for wrong board_id and TH(236KB)/MC(896KB)\
      \ oversize\n  [PASS] HIL-CASE-63 (Interruption & 95%/100% Gate): Mid-stream\
      \ 0x08004000 protection, retry recovery & Stage 3 (95%) cap verified\n\n[SUMMARY]\
      \ SEQ-06 Upgrade Suite: 4/4 passed."
  passed: true
  timestamp: '2026-11-06T05:56:04.135126+00:00'
  path: /tmp/qa_TWIN-66_yutlalmd/evidence/server_qa.json
  sha256: cab3a3f5aca5bcade5265efa62362f5e3069379bca2c7e1702d6b817d42a889c
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-66_yutlalmd/reviews/77d3815e86874a968f34e6ef3ac3e298/codex.jsonl
  sha256: 7a8fc0d5d14b96b281f40a5aaf0b27a49273c9b92690684046d15a1409fe01ea
reviewed_artifacts:
- path: /tmp/qa_TWIN-66_yutlalmd/request.json
  sha256: 22d524a809c647df12e94ef34b46e5dd391e072527e0622bda5bd3f96f391d99
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/test_harness.patch
  sha256: 417133875632ae7727d7cd46c0de1b61c00f072d55b8aad5c2221fab9150162d
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_yutlalmd/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/static_checks/minimcproto/check_opcode_alignment.py
  sha256: 9f2e1da5c52d87122875ed3c7117dd9521a4ab9c33770765fb097463ffdfa78f
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/static_checks/minimcproto/run_ota_software_suite.py
  sha256: 2c8fa66e3a11662a1dce14bf5cf7c8b8ab34236e1a3aa940a323914fe436474e
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/static_checks/minimcproto/reference_vectors.py
  sha256: 91ee8fef5f193e7768a62209d0f7ab349c77d0e87cba3971c82cfe2dad4a0c1f
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/static_checks/minimcproto/run_codec_cases.py
  sha256: 1a3f9b558f26bb96a8b4da316e46638984358c477a825c01cc10a80dc3360719
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/static_checks/minimcproto/golden_vectors.json
  sha256: 022153520cbe91afa64f4af8b2889d5840fdb6bb86f06d9d462172e34af90039
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: 17d76ee360a217ebb368bb9ece85bcb874a251557f95388ae32bb5892a27cc1c
- path: /tmp/qa_sandboxes/TWIN-66_run_135454_20261106_055454/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: 8bc108f52a1c8f4e6bd2be6bd9f780b3a932101c2ade1568bccf626cd9268afc
verification_scope: 按已校验的 TWIN-66 revision 1 范围，审阅 5 端协议静态检查、520B 容量门禁、G01–G25 黄金向量、OTA
  软件套件及部署/升级工具。物理 HIL 硬件执行属于 TWIN-67，明确排除；不将其视为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

锁定证据哈希及候选提交匹配，但源码将多项验收检查直接设为通过，未满足接受范围中的软件集成与负向场景验证条款。
