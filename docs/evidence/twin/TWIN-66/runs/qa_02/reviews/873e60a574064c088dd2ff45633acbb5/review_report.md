```yaml
task_id: TWIN-66
task_revision: 2
candidate_commit: 3e3fb659e9bb3e54222ded1169a70fc331681c48
role: QA
decision: BLOCKED
summary: 复验确认增量差异将上一轮指出的硬编码通过改为实际检查；冻结证据中 M04、N08–N10 通过，但 C05–C08 编译失败，且失败原因不足以判断是候选问题还是验证环境问题。命令链因此未执行最后的升级自检，当前证据不足以批准或确认源码不符合条款。
findings:
- 复验上下文：上一轮 QA 报告 reverification/previous_qa_review.md（SHA256 6de5d13da7ba090860395a47da67eeb417961c79862d3c454124be366a5fc32f）因
  C05–C08、M04、N08–N10 硬编码通过而 REJECTED。本轮差异 SHA256 与索引相符；差异显示这些检查现已实际执行，本轮结论独立于上一轮。
- 阻断：接受条款要求 C01–C09 单模块契约和主机测试通过。冻结 runtime.log 显示 C05、C06、C07、C08 的 CMake 构建失败，OTA
  套件结果为 35 passed、4 failed。日志仅保留截断的编译错误详情，无法核实失败根因，故无法判断为源码不符合还是验证环境导致，也不能确认这些条款通过。
- 阻断：接受的验证命令以 && 串联；OTA 套件退出码为 1，故末尾的 hil/tests/test_mcu_firmware_upgrade.py --self-test
  未执行。该项属于接受范围内必需证据。
- 已核实本轮其他相关证据：冻结日志显示 G01–G25/codec 套件 42 passed、0 failed，OTA 套件内可见 M04、N08–N10 及 S/D
  类检查通过。未将未执行的物理 HIL 硬件验证视为通过；该项按范围排除。
accepted_scope: 按 TWIN-66 revision 2 已校验索引审阅 5 端 opcode/520B 容量静态门禁、G01–G25 固定字节黄金向量、OTA
  软件套件 S01–S04/D01–D08/C01–C09/M01–M08/N01–N10、部署/升级工具及升级自检。复验聚焦上一候选 e7f7f574fee7dce8cc78b52772ff32a03b9b345f
  到本候选的 test_harness 增量差异，并检查受影响检查及必要回归证据。物理 HIL 硬件执行属于 TWIN-67，明确排除。
unexecuted:
- C05–C08 真实构建/测试未通过，编译失败根因无法从冻结日志核实；这些接受范围内条款尚无可确认的通过证据。
- hil/tests/test_mcu_firmware_upgrade.py --self-test 因前序 OTA 软件套件失败、&& 命令链提前终止而未执行。
actual_session: 01a1af81-8530-74b2-89f3-ed9940ec8401
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=d817294ac45357e718acb0b2908088492110b4f1;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511;
  test_harness=3e3fb659e9bb3e54222ded1169a70fc331681c48; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-66
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: e62421c62869
    id: TWIN-66_run_141707_20261106_061707
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707
    developer_mounts: []
    container_inspect:
      id: e62421c62869438e8739dfc5af95d77a56f90e357166e38d4927b590cb20bb55
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T06:17:37.645372611Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-66_z_11r0sb/evidence/server_lock.json
    sha256: 503fdf1f1cbe5513929e4b1ee08e641fc4f77982e113c27868c221baf55a1949
  checkout_log:
    path: /tmp/qa_TWIN-66_z_11r0sb/evidence/checkout.log
    sha256: bc5ca7c6e81e653c23c6084d9f72af25917981690ea4bb92bd8883a74a12b944
  runtime_log:
    path: /tmp/qa_TWIN-66_z_11r0sb/evidence/runtime.log
    sha256: a731617bb61d573bfbfda9c58c57f7229218a19e59bc4836661ae95743f73339
  server_verdict:
    path: /tmp/qa_TWIN-66_z_11r0sb/evidence/server_verdict.json
    sha256: b0daf2d00317a17b6cc4a19a3e113a7c92337dc6f8d76c3a02d270d36a8f206a
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: python3 static_checks/minimcproto/check_opcode_alignment.py && python3
      static_checks/minimcproto/run_codec_cases.py && python3 static_checks/minimcproto/run_ota_software_suite.py
      && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test
    exit_code: '1'
    subpath: test_harness
    duration: 2.06s
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
      \ safe shutdown, UPGD magic & 0x19 filament\n  [PASS] C09: ATSG 128B Trailer\
      \ packer & verifier cross-tool parity (OK)\n\n--- 4. End-to-End Virtual Dual-MCU\
      \ Integration (M01~M08) ---\n  [PASS] M01: TH(0x03) 4-stage cascaded upgrade\
      \ & boot_id transition\n  [PASS] M02: MC(0x02) 4-stage direct upgrade & boot_id\
      \ transition\n  [PASS] M03: Strict TH-first then MC-second dual-MCU sequential\
      \ closed loop\n  [PASS] M04: 0x21 chunk CRC16 corruption NACK(0x12) & retry\
      \ recovery\n  [PASS] M05: TH power-loss after Chunk 0 -> stays in Boot & full\
      \ retry recovery\n  [PASS] M06: TH power-loss after Chunk 1 -> Anchor/Chunk0\
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
      \  [FAIL] C05: soc-ap forward UART_MODE_OTA_ROUTE (534B frame, 3000ms erase\
      \ timeout) failed: CMake build failed for test_forward_protocol: In file included\
      \ from /workspace/soc-ap/services/forward/forward_types.h:15,\n            \
      \     from /workspace/soc-\n  [FAIL] C06: soc-ap device_manager 0x02 version\
      \ cache & PRINTING/HOMING upgrade lock failed: CMake build failed for test_firmware_updater:\
      \ In file included from /workspace/soc-ap/services/device_manager/device_manager_types.h:19,\n\
      \                 from /\n  [FAIL] C07: soc-ap firmware_updater 4-stage state\
      \ machine & TH->MC order lock failed: CMake build failed for test_firmware_updater:\
      \ In file included from /workspace/soc-ap/services/device_manager/device_manager_types.h:19,\n\
      \                 from /\n  [FAIL] C08: soc-ap ui_gateway /api/v1/firmware/upload|start|status\
      \ (400/409/502) failed: CMake build failed for test_ui_gateway_routes: In file\
      \ included from /workspace/soc-ap/services/ui_gateway/ui_gateway_dbus.h:11,\n\
      \                 from /workspac\n\n[SUMMARY] OTA Software Suite: 35 passed,\
      \ 4 failed."
  passed: false
  timestamp: '2026-11-06T06:17:42.672285+00:00'
  path: /tmp/qa_TWIN-66_z_11r0sb/evidence/server_qa.json
  sha256: 629c08e98afab6bde0ee5d115f5300415de3015b853b4e6e92d42c96ff658090
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-66_z_11r0sb/reviews/873e60a574064c088dd2ff45633acbb5/codex.jsonl
  sha256: 94e948453dc454ee35d78ef4b2f58deb46b2eaded24b7cadd1088fbec3ad3111
reviewed_artifacts:
- path: /tmp/qa_TWIN-66_z_11r0sb/request.json
  sha256: 31e21e024d717ab2bdcc39f524c497b0e53ad268e556ae6bc7cf23c86bfaae8e
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/test_harness.patch
  sha256: 595e5d7c182941cadf98e17169ce3765937ed426bde0b2df7f7d3edd108f3a1c
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_z_11r0sb/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/static_checks/minimcproto/check_opcode_alignment.py
  sha256: 7a7358db859a5c078d3a0fad3cf63ed99a2c03d63c80532d5c837af8dbdaae78
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/static_checks/minimcproto/run_ota_software_suite.py
  sha256: 0f160c8875b6d48c23d75955d7ce185753ff4779afd72be594573c5a2230d773
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/static_checks/minimcproto/reference_vectors.py
  sha256: e1fa1941f23e2ca15b55ebbcb8c7c4650c5cf5713e636ed6319b2dd267353203
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/static_checks/minimcproto/run_codec_cases.py
  sha256: 4d2db3e59f6c6c4278429440006e2998628080cb2b8cb58fb7d56a6c1944d29a
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/static_checks/minimcproto/golden_vectors.json
  sha256: 022153520cbe91afa64f4af8b2889d5840fdb6bb86f06d9d462172e34af90039
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: dffa21cfeb94f6705fb8b18a2430c03c360f2e49a549cb60389209af5d3868da
- path: /tmp/qa_sandboxes/TWIN-66_run_141707_20261106_061707/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: c28ac5c58dd344d92438a9bf6b7fc7c16cce41a60aa91e01afef9d599e372f77
verification_scope: 按 TWIN-66 revision 2 已校验索引审阅 5 端 opcode/520B 容量静态门禁、G01–G25 固定字节黄金向量、OTA
  软件套件 S01–S04/D01–D08/C01–C09/M01–M08/N01–N10、部署/升级工具及升级自检。复验聚焦上一候选 e7f7f574fee7dce8cc78b52772ff32a03b9b345f
  到本候选的 test_harness 增量差异，并检查受影响检查及必要回归证据。物理 HIL 硬件执行属于 TWIN-67，明确排除。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验确认增量差异将上一轮指出的硬编码通过改为实际检查；冻结证据中 M04、N08–N10 通过，但 C05–C08 编译失败，且失败原因不足以判断是候选问题还是验证环境问题。命令链因此未执行最后的升级自检，当前证据不足以批准或确认源码不符合条款。
