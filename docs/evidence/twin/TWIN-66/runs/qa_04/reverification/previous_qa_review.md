```yaml
task_id: TWIN-66
task_revision: 3
candidate_commit: e01f63b1d0a695c5117a50f190762aa7e1fc16f9
role: ARCH
decision: REJECTED
summary: 复验已核对同角色上一轮 ARCH 报告（SHA256 04c154ba315ed1bf4a998a93399c9d9f005ce1f63150f8c2b17825b0daf296c8）和本轮增量差异（SHA256
  231ebe770550c6d67e7e209fe4b04c5c8cda152a625c6293ae2b17a8cb07f81c）。上一轮因 C05–C08 失败及自测未执行而
  BLOCKED；本轮定向修复后，冻结验证仍因 C05–C08 失败退出，故未满足 revision 3 的全通过验收。bundle、server verdict、runtime
  log 及所列候选源码工件哈希均与索引一致。
findings:
- 阻断：接受范围要求 OTA 软件套件 S01–S04、D01–D08、C01–C09、M01–M08、N01–N10 全部通过。冻结日志显示 C05–C08 均失败，测试进程以
  rc=127 退出，报告 D-Bus 无法打开 `/home/sushaohua/workspace/ai_soc_project/soc-ap/third_party/install`
  下的路径；因此四项契约未通过，且本轮新增的 `_prepare_writable_soc_ap` 改动没有使这些检查在锁定沙箱中成功。
- 阻断：接受范围要求完整执行 `verify_twin-66`。串联命令在 `run_ota_software_suite.py` 退出 1 后停止，`hil/tests/test_mcu_firmware_upgrade.py
  --self-test` 未执行，缺少必要回归证据。
- 冻结证据记录静态门禁、42 项黄金与参考 codec 向量、D 类、C01–C04/C09、M01–M08 与 N01–N10 通过；这些结果不抵消 C05–C08
  失败或缺失的自测。
accepted_scope: 按 TWIN-66 revision 3 核查 5 端静态门禁、G01–G25 黄金向量、S01–S04/D01–D08/C01–C09/M01–M08/N01–N10
  软件套件、部署工具及 MCU 固件升级自测。复验聚焦上一候选 3e3fb659e9bb3e54222ded1169a70fc331681c48 到本候选的增量改动，并核对受影响的
  C05–C08 和必要回归证据。物理 HIL 硬件执行在本任务范围之外，不视为已验证。
unexecuted:
- hil/tests/test_mcu_firmware_upgrade.py --self-test：完整串联命令在 OTA 软件套件失败后提前终止。
actual_session: 01a1af88-1387-71c3-9ab9-433859d22752
reviewer_role: ARCH
reviewer_roles:
- ARCH
reviewed_artifact_version: project-control=ae198228401c0b021f5e14e05731ec660400e5aa;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511;
  test_harness=e01f63b1d0a695c5117a50f190762aa7e1fc16f9; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-66
  task_revision: 3
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: b2749249ab82
    id: TWIN-66_run_142209_20261106_062209
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209
    developer_mounts: []
    container_inspect:
      id: b2749249ab82528c05ec3fa2fb84b394213f6baf286adb6c6439409c90a715b0
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T06:22:34.177062264Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-66_6onm543b/evidence/server_lock.json
    sha256: 4ff3e3be82f8569f2589823a23d6d387d917783a44bec6c11fe79694edeb80e7
  checkout_log:
    path: /tmp/qa_TWIN-66_6onm543b/evidence/checkout.log
    sha256: 9482f251541d508fb236cb889bf70426c4df265ebb2a9085375e0f3789d816a5
  runtime_log:
    path: /tmp/qa_TWIN-66_6onm543b/evidence/runtime.log
    sha256: da2e34ba1b7f82da3987eb2213fbd0174823c2e7d7d4fd11dec1aad1b691fef1
  server_verdict:
    path: /tmp/qa_TWIN-66_6onm543b/evidence/server_verdict.json
    sha256: 320048e7822aa72abd027721b012db5b660b68a6aac7a14e368afef6f9058fc3
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
    duration: 8.47s
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
      \ timeout) failed: test_forward_protocol failed (rc=127): dbus[208]: Failed\
      \ to start message bus: Failed to open \"/home/sushaohua/workspace/ai_soc_project/soc-ap/third_party/insta\n\
      \  [FAIL] C06: soc-ap device_manager 0x02 version cache & PRINTING/HOMING upgrade\
      \ lock failed: test_firmware_updater failed (rc=127): dbus[346]: Failed to start\
      \ message bus: Failed to open \"/home/sushaohua/workspace/ai_soc_project/soc-ap/third_party/insta\n\
      \  [FAIL] C07: soc-ap firmware_updater 4-stage state machine & TH->MC order\
      \ lock failed: test_firmware_updater failed (rc=127): dbus[346]: Failed to start\
      \ message bus: Failed to open \"/home/sushaohua/workspace/ai_soc_project/soc-ap/third_party/insta\n\
      \  [FAIL] C08: soc-ap ui_gateway /api/v1/firmware/upload|start|status (400/409/502)\
      \ failed: test_ui_gateway_routes failed (rc=127): dbus[459]: Failed to start\
      \ message bus: Failed to open \"/home/sushaohua/workspace/ai_soc_project/soc-ap/third_party/inst\n\
      \n[SUMMARY] OTA Software Suite: 35 passed, 4 failed."
  passed: false
  timestamp: '2026-11-06T06:22:45.424657+00:00'
  path: /tmp/qa_TWIN-66_6onm543b/evidence/server_qa.json
  sha256: a240757780e9dc852e7a143ace39f74db5575c963935bc99541fb460efa63225
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-66_6onm543b/reviews/c662c4d520b04955a9dfb0e5cf749175/codex.jsonl
  sha256: d20576fe88142074cea0cb948015354bd440679611eca871fa2d38e51a3b5807
reviewed_artifacts:
- path: /tmp/qa_TWIN-66_6onm543b/request.json
  sha256: e72f997ced2fae048814b461f43672b8b5f211aa4892faae96361ae86c6714b3
- path: /tmp/qa_TWIN-66_6onm543b/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_6onm543b/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_6onm543b/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_6onm543b/diffs/test_harness.patch
  sha256: 4555ce1747c1c0a778288f6a4e23e6169944a742d1c34e5d126b4cde146a4646
- path: /tmp/qa_TWIN-66_6onm543b/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-66_6onm543b/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/static_checks/minimcproto/check_opcode_alignment.py
  sha256: 7a7358db859a5c078d3a0fad3cf63ed99a2c03d63c80532d5c837af8dbdaae78
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/static_checks/minimcproto/run_ota_software_suite.py
  sha256: a530e4ed2959c385a5916f765438ce02719dcc86b4b8ad61675c9b60d4cc6e92
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/static_checks/minimcproto/reference_vectors.py
  sha256: e1fa1941f23e2ca15b55ebbcb8c7c4650c5cf5713e636ed6319b2dd267353203
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/static_checks/minimcproto/run_codec_cases.py
  sha256: 4d2db3e59f6c6c4278429440006e2998628080cb2b8cb58fb7d56a6c1944d29a
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/static_checks/minimcproto/golden_vectors.json
  sha256: 022153520cbe91afa64f4af8b2889d5840fdb6bb86f06d9d462172e34af90039
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: dffa21cfeb94f6705fb8b18a2430c03c360f2e49a549cb60389209af5d3868da
- path: /tmp/qa_sandboxes/TWIN-66_run_142209_20261106_062209/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: c28ac5c58dd344d92438a9bf6b7fc7c16cce41a60aa91e01afef9d599e372f77
verification_scope: 按 TWIN-66 revision 3 核查 5 端静态门禁、G01–G25 黄金向量、S01–S04/D01–D08/C01–C09/M01–M08/N01–N10
  软件套件、部署工具及 MCU 固件升级自测。复验聚焦上一候选 3e3fb659e9bb3e54222ded1169a70fc331681c48 到本候选的增量改动，并核对受影响的
  C05–C08 和必要回归证据。物理 HIL 硬件执行在本任务范围之外，不视为已验证。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验已核对同角色上一轮 ARCH 报告（SHA256 04c154ba315ed1bf4a998a93399c9d9f005ce1f63150f8c2b17825b0daf296c8）和本轮增量差异（SHA256 231ebe770550c6d67e7e209fe4b04c5c8cda152a625c6293ae2b17a8cb07f81c）。上一轮因 C05–C08 失败及自测未执行而 BLOCKED；本轮定向修复后，冻结验证仍因 C05–C08 失败退出，故未满足 revision 3 的全通过验收。bundle、server verdict、runtime log 及所列候选源码工件哈希均与索引一致。
