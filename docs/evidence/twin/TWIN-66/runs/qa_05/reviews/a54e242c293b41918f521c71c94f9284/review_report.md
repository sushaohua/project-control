```yaml
task_id: TWIN-66
task_revision: 5
candidate_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
role: ARCH
decision: APPROVED
summary: 复验已核对同角色上一轮 ARCH 报告快照（SHA256 2772384147071d32a987960c000c72d6eb7720e0c72461605077a39d86a32334）及本轮整改差异（SHA256
  732c5daffc29d021a199d0368b48a4bb6d07a0d5e28d038abbc4bf6cdeaefe43）。差异将 SoC 单测工作目录设为源码根目录；冻结证据显示
  C08 通过，完整验收命令链退出码为 0。
findings: []
accepted_scope: 核查 test_harness 从上一候选 fb f6e1157a4e729b2ca2da9ecda3fc488409f839 到本候选的增量差异，并核验五端
  opcode/520B 容量门禁、G01–G25 黄金向量、S01–S04、D01–D08、C01–C09、M01–M08、N01–N10 及 MCU 升级自测。冻结日志记录上述范围通过；候选文件哈希与已校验证据索引一致。物理
  HIL 硬件执行不在接受范围内，也未视为已验证。
unexecuted: []
actual_session: 01a1af92-9089-7f22-9df8-c462b8604009
reviewer_role: ARCH
reviewer_roles:
- ARCH
reviewed_artifact_version: project-control=ae168003454eb18acbf5d867c15c52042cc87f4c;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511;
  test_harness=cf81195eca55bcd772ef2daa2fd4aa41634c1492; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-66
  task_revision: 5
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 9c6f14e0e050
    id: TWIN-66_run_143417_20261106_063417
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417
    developer_mounts: []
    container_inspect:
      id: 9c6f14e0e0503a48a66e1e6433ad17ff99dd30c464d1adbaff3de6e6816b2f43
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T06:34:48.911366903Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-66_bo5iw0uk/evidence/server_lock.json
    sha256: 362ace7b573c66094f866a821762ca531b0384cae816b0614375fcda135781bc
  checkout_log:
    path: /tmp/qa_TWIN-66_bo5iw0uk/evidence/checkout.log
    sha256: b619b2b4ab32b41e8895eec4ed4c84d9968112847e94f0f40282f420142c3bfe
  runtime_log:
    path: /tmp/qa_TWIN-66_bo5iw0uk/evidence/runtime.log
    sha256: c3ef2e1d3fafe42207248362cf9f2f58a087a9b139e219eaba66492d2a56dad3
  server_verdict:
    path: /tmp/qa_TWIN-66_bo5iw0uk/evidence/server_verdict.json
    sha256: 082e3b8e64af4ee7540bf37f10b0457b616d6f91d2cc695aac3b2233a182e518
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
    duration: 9.93s
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
      \  [PASS] S04: Function <=50 lines, <=4 params, Chinese docstrings & inline\
      \ '#' comments verified\n\n--- 2. Codec & Golden Byte Vectors (D01~D08) ---\n\
      \  [PASS] G01: status=OK len=14B\n  [PASS] G02: status=OK len=14B\n  [PASS]\
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
      \ & retry recovery\n  [PASS] M05: TH power-loss after Chunk 0 -> stays in Boot\
      \ & full retry recovery\n  [PASS] M06: TH power-loss after Chunk 1 -> Anchor/Chunk0\
      \ protected & retry recovery\n  [PASS] M07: 0x23 CMD_OTA_ABORT & MC 5000ms proxy\
      \ timeout clean recovery\n  [PASS] M08: Stage 3 (95% cap on 0x22 ACK) vs Stage\
      \ 4 (100% after new App 0x02) isolation\n\n--- 5. Negative & Fault-Injection\
      \ Interception (N01~N10) ---\n  [PASS] N01: Bad ATSG magic (0x41545348) rejected\
      \ with NACK 0x06 & 0 erases\n  [PASS] N02: Board ID mismatch (MC pkg to TH)\
      \ rejected with NACK 0x06 & 0 erases\n  [PASS] N03: Tampered trailer_crc32 rejected\
      \ with NACK 0x06 & 0 erases\n  [PASS] N04: Oversize image (TH 241,665B & MC\
      \ 917,505B) rejected with NACK 0x14 & 0 erases\n  [PASS] N05: Invalid Cortex-M4\
      \ vector table (SP/PC Thumb bit0) rejected\n  [PASS] N06: Out-of-order 0x21\
      \ chunk offset rejected with NACK 0x13\n  [PASS] N07: Corrupted 0x22 Finish\
      \ fw_crc32 rejected with NACK 0x12 & stays in Boot\n  [PASS] N08: Upgrade request\
      \ during PRINTING/HEATING/WRITER_LOCK rejected (NACK 0x05)\n  [PASS] N09: Forged\
      \ legacy 0x05 opcode & unexpected response intercepted & rejected\n  [PASS]\
      \ N10: Post-Finish App boot failure stays at 95% and transitions to ERROR/ROLLBACK\n\
      \n[SUMMARY] OTA Software Suite: 39 passed, 0 failed.\n=== SEQ-06 MCU Firmware\
      \ Upgrade Verification Suite (HIL-CASE-60~63) ===\n  [PASS] HIL-CASE-60 (TH\
      \ Cascaded 4-Stage Upgrade): TH v1.1->v2.5 boot_id=0x2000b001->0x2010b002->0x2111b007\n\
      \  [PASS] HIL-CASE-61 (Ordered TH->MC Dual Upgrade): Ordered TH(v1.1->v2.1)\
      \ -> MC(v1.2->v2.4) upgrade verified\n  [PASS] HIL-CASE-62 (Zero-Erase Gate\
      \ & Interlocks): Zero-erase gate verified for wrong board_id and TH(236KB)/MC(896KB)\
      \ oversize\n  [PASS] HIL-CASE-63 (Interruption & 95%/100% Gate): Mid-stream\
      \ 0x08004000 protection, power-cycle retry recovery & Stage 3 (95%) cap verified\n\
      \n[SUMMARY] SEQ-06 Upgrade Suite: 4/4 passed."
  passed: true
  timestamp: '2026-11-06T06:35:01.719671+00:00'
  path: /tmp/qa_TWIN-66_bo5iw0uk/evidence/server_qa.json
  sha256: 4819bb723f64ee97d13eff79530b943881e89d9d9ac74a12feeac5e8fc6b2517
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-66_bo5iw0uk/reviews/a54e242c293b41918f521c71c94f9284/codex.jsonl
  sha256: 04c28864451ff2d743ef218de26052a972dcf2550ef83357fd6c09263cd75246
reviewed_artifacts:
- path: /tmp/qa_TWIN-66_bo5iw0uk/request.json
  sha256: 428a872eea028a9e411a2b8f4e0773ce2d971a3fd021d1d0f43a475acfa4fb39
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/test_harness.patch
  sha256: c82b5f933221168d115326d457d2235683c94c60dbaf947e65f1389e51c790d8
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_bo5iw0uk/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/static_checks/minimcproto/check_opcode_alignment.py
  sha256: 7a7358db859a5c078d3a0fad3cf63ed99a2c03d63c80532d5c837af8dbdaae78
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/static_checks/minimcproto/run_ota_software_suite.py
  sha256: f07b9678bb7621cd75e962384d2acb97b5bf7e1a60133ee3a6439abe4087abc0
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/static_checks/minimcproto/reference_vectors.py
  sha256: e1fa1941f23e2ca15b55ebbcb8c7c4650c5cf5713e636ed6319b2dd267353203
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/static_checks/minimcproto/run_codec_cases.py
  sha256: 4d2db3e59f6c6c4278429440006e2998628080cb2b8cb58fb7d56a6c1944d29a
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/static_checks/minimcproto/golden_vectors.json
  sha256: 022153520cbe91afa64f4af8b2889d5840fdb6bb86f06d9d462172e34af90039
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: dffa21cfeb94f6705fb8b18a2430c03c360f2e49a549cb60389209af5d3868da
- path: /tmp/qa_sandboxes/TWIN-66_run_143417_20261106_063417/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: c28ac5c58dd344d92438a9bf6b7fc7c16cce41a60aa91e01afef9d599e372f77
verification_scope: 核查 test_harness 从上一候选 fb f6e1157a4e729b2ca2da9ecda3fc488409f839
  到本候选的增量差异，并核验五端 opcode/520B 容量门禁、G01–G25 黄金向量、S01–S04、D01–D08、C01–C09、M01–M08、N01–N10
  及 MCU 升级自测。冻结日志记录上述范围通过；候选文件哈希与已校验证据索引一致。物理 HIL 硬件执行不在接受范围内，也未视为已验证。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验已核对同角色上一轮 ARCH 报告快照（SHA256 2772384147071d32a987960c000c72d6eb7720e0c72461605077a39d86a32334）及本轮整改差异（SHA256 732c5daffc29d021a199d0368b48a4bb6d07a0d5e28d038abbc4bf6cdeaefe43）。差异将 SoC 单测工作目录设为源码根目录；冻结证据显示 C08 通过，完整验收命令链退出码为 0。
