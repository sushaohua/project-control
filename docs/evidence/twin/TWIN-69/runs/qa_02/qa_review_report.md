```yaml
task_id: TWIN-69
task_revision: 2
candidate_commit: a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7
role: QA
decision: REJECTED
summary: 上一轮同角色 QA 报告及本轮定向差异的哈希均匹配。新增串口传输与 PTY 证据修复了上一轮指出的虚拟靶机阻断；但本轮源码仍可能静默使用与 --baud
  不同的实际波特率，未满足接受范围中的串口参数要求。
findings:
- 阻断：接受范围要求 CLI 的 --baud 参数用于真实 POSIX 串口传输。[hil_deploy_via_minimc_ota.py](/tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104/test_harness/hil/tools/hil_deploy_via_minimc_ota.py:420)
  只为 9600、115200、230400、460800、921600 配置波特率；其他值会静默回退到 921600（若平台没有 B921600 常量，则再回退到
  B115200），而 [CLI 参数定义](/tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104/test_harness/hil/tools/hil_deploy_via_minimc_ota.py:712)
  接受任意整数，回执仍记录用户请求值。因而例如 --baud 57600 会以其他速率通信并给出不准确回执。冻结 PTY 正向证据只覆盖 921600，不能验证其他参数值被实际应用。
- 非阻断建议：PTY 测试核对了 TH 的 151 块和字节数及双包升级成功状态，但没有断言 MC 的分块数和字节数；可补充相应回执断言。
- 非阻断建议：当前工作区为只读，无法将评审说明与最终 JSON 分别写入文件；本响应提供最终 JSON。
accepted_scope: 已核对 task revision 2 的接受范围、上一轮 QA 报告（SHA256 匹配）、上一候选至本候选的定向差异（SHA256
  匹配）、本轮 request/evidence 索引与 runtime/verdict 哈希，以及声明源码和手册哈希。范围内检查涵盖 CLI 串口部署、默认 512B
  与 76,896B/151 块正向证据、非法分块拒绝、能力位和 revision 5 手册、要求的软件回归及恢复相关 CASE-63 证据。已校验的 server
  证据报告命令通过，PTY 验证覆盖 921600。物理 HIL 硬件执行不在接受范围内，未声称通过。source_report 为空。
unexecuted: []
actual_session: 01a1b3c6-dd3e-7f50-ac68-cbe0da85dfa0
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=b764378b4d3232d1c7ce77fd4922f520dd31ef51;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=97c1c2422e98357e72cc822d2b5293b9e0c2abc6;
  test_harness=a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-69
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 32a391cfc661
    id: TWIN-69_run_101104_20261107_021104
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104
    developer_mounts: []
    container_inspect:
      id: 32a391cfc6610830c7e1eedf88ae32b40287abe8b5068774bfea67aa182a3208
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-07T02:11:43.918797322Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-69_ew7xy2c1/evidence/server_lock.json
    sha256: dbb83e2e40b918c057f80dff829dbce6d2e371e660d5ac7463cc5017b8062f28
  checkout_log:
    path: /tmp/qa_TWIN-69_ew7xy2c1/evidence/checkout.log
    sha256: 5954027e185cd2a2d4be2e4e95b946e6b080fcedff6642d8d7122181dd1e5a7a
  runtime_log:
    path: /tmp/qa_TWIN-69_ew7xy2c1/evidence/runtime.log
    sha256: 5f00910498ec3324f20f0b213f4d8f4d3a370d040c3e98819e5dba56bea39a15
  server_verdict:
    path: /tmp/qa_TWIN-69_ew7xy2c1/evidence/server_verdict.json
    sha256: 02e3e4d22ccc2ff464deb2b7ae059ff4b44a33d8c1add7f54e663f132cd421d6
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: 'sh ../mcu-p3/motion-controller-mcu/tests/run_tests.sh && python3 hil/tools/hil_deploy_via_minimc_ota.py
      --self-test && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test &&
      python3 -m unittest discover -s hil/tests -p "test_mcu_firmware_upgrade.py"
      -v && python3 static_checks/minimcproto/run_ota_software_suite.py && grep -q
      "revision: 5" ../project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
      && grep -q "Bits 16..23=0x08 (Bit19=1)" ../project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md'
    exit_code: '0'
    subpath: test_harness
    duration: 9.57s
    output: "=== [1/3] Run TWIN-44/47/60 MC regression suite (test_twin44_mc_debug.c)\
      \ ===\n========================================================================\n\
      TWIN-44 & TWIN-47 MC USART2 921600, Control Cmds & 0x1C Verification\n========================================================================\n\
      [RUN ] test_usart2_921600_reconfig\n[PASS] test_usart2_921600_reconfig\n[RUN\
      \ ] test_ring_buffer_trunc_drop_and_recovery\n[PASS] test_ring_buffer_trunc_drop_and_recovery\n\
      [RUN ] test_honest_minimc_v2_queries_and_nack\n[PASS] test_honest_minimc_v2_queries_and_nack\n\
      [RUN ] test_non_intrusive_notify_and_fault_sync\n[PASS] test_non_intrusive_notify_and_fault_sync\n\
      [RUN ] test_tx_fail_suppresses_ack_and_recovers\n[PASS] test_tx_fail_suppresses_ack_and_recovers\n\
      [RUN ] test_relay_timeout_crc_err_and_recovery\n[PASS] test_relay_timeout_crc_err_and_recovery\n\
      [RUN ] test_th_relay_correlation_and_nack\n[PASS] test_th_relay_correlation_and_nack\n\
      [RUN ] test_twin47_temp_home_move_stop\n[PASS] test_twin47_temp_home_move_stop\n\
      [RUN ] test_twin47_job_filament_level_gcode\n[PASS] test_twin47_job_filament_level_gcode\n\
      [RUN ] test_twin60_adc_range_filament_nack_and_boot_id\n[PASS] test_twin60_adc_range_filament_nack_and_boot_id\n\
      ------------------------------------------------------------------------\nAll\
      \ 10 TWIN-44/TWIN-47/TWIN-60 test suites PASSED!\n========================================================================\n\
      === [2/3] Run TWIN-64 MC OTA, 0x1D magic (0x2005FFF0), 534B proxy & th_upgrade_mgr\
      \ suite ===\n[PASS] test_mc_ota_and_relay: all TWIN-64/TWIN-68 MC App OTA, 534B\
      \ relay & underflow tests passed!\n=== [3/3] Verify MC zero M997/5AA5 residue\
      \ & S04 function/comment gates ===\n[PASS] MC S04 function length (<=50), params\
      \ (<=4) and Chinese comments verified!\n[PASS] hil_deploy_via_minimc_ota.py\
      \ self-test passed: chunk_size=512B, TH(76896B/151 chunks, 1.1->2.1) then MC(1.2->2.3).\n\
      === SEQ-06 MCU Firmware Upgrade Verification Suite (HIL-CASE-60~64) ===\n  [PASS]\
      \ HIL-CASE-60 (TH Cascaded 4-Stage Upgrade): TH v1.1->v2.5 boot_id=0x2000b001->0x2010b002->0x2111b007\n\
      \  [PASS] HIL-CASE-61 (Ordered TH->MC Dual Upgrade): Ordered TH(v1.1->v2.1)\
      \ -> MC(v1.2->v2.4) upgrade verified\n  [PASS] HIL-CASE-62 (Zero-Erase Gate\
      \ & Interlocks): Zero-erase gate verified for wrong board_id and TH(236KB)/MC(896KB)\
      \ oversize\n  [PASS] HIL-CASE-63 (Interruption & 95%/100% Gate): Mid-stream\
      \ 0x08004000 protection, power-cycle retry recovery & Stage 3 (95%) cap verified\n\
      \  [PASS] HIL-CASE-64 (512B Default Chunk & 76896B 151-Chunk Stream): DEFAULT_OTA_CHUNK_SIZE=512,\
      \ 0xE0080423/0xC0080435->512B, serial PTY(/dev/pts/0@921600) TH=151 chunks/76896B\
      \ & invalid chunk_size rejected\n\n[SUMMARY] SEQ-06 Upgrade Suite: 5/5 passed.\n\
      === MiniMCProto v2.0 (Rev 2.0.4) OTA Software Verification Suite ===\n\n---\
      \ 1. Static & Compile-Time Gates (S01~S04) ---\n  [PASS] S01: 5-endpoint Rev\
      \ 2.0.4 opcode table & reverse numeric uniqueness\n  [PASS] S02: Zero 0x05/0x15\
      \ legacy drift & >=520B payload / >=534B frame capacity\n  [PASS] S03: TH Bootloader\
      \ 16KB (0x08000000..0x08003FFF) Flash budget & 0B .bss growth\n  [PASS] S04:\
      \ Function <=50 lines, <=4 params, Chinese docstrings & inline '#' comments\
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
      \n[SUMMARY] OTA Software Suite: 39 passed, 0 failed.\n\n[EXPECTED-REJECT] invalid\
      \ --chunk-size=0 (must be 1..512)\n[EXPECTED-REJECT] invalid --chunk-size=513\
      \ (must be 1..512)\ntest_case60_th_cascaded_upgrade (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n\
      执行 HIL-CASE-60 TH 级联四阶段升级单测断言。 ... ok\ntest_case61_ordered_th_then_mc_upgrade\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-61 先\
      \ TH 后 MC 顺序四阶段升级单测断言。 ... ok\ntest_case62_pre_erase_and_busy_interlocks (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n\
      执行 HIL-CASE-62 擦除前零擦除门禁与忙状态互锁单测断言。 ... ok\ntest_case63_interruption_and_stage4_isolation\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-63 中途掉电首块保护重传与\
      \ Stage 3/4 隔离单测断言。 ... ok\ntest_case64_default_512b_chunk_and_76896b_th_stream\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-64 默认\
      \ 512B 分块、76,896B TH 151 块流式升级与非法分块拒绝断言。 ... [EXPECTED-REJECT] invalid --chunk-size=0\
      \ (must be 1..512)\n[EXPECTED-REJECT] invalid --chunk-size=513 (must be 1..512)\n\
      ok\n\n----------------------------------------------------------------------\n\
      Ran 5 tests in 0.366s\n\nOK"
  passed: true
  timestamp: '2026-11-07T02:11:56.096536+00:00'
  path: /tmp/qa_TWIN-69_ew7xy2c1/evidence/server_qa.json
  sha256: 5b4608647bfd34ba2a4b7d9a43ca8eabefacbfaf7b4f6607bcef4ec2b26f750e
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-69_ew7xy2c1/reviews/cc0f9c8d44e84255ae2a87a4e6181bda/codex.jsonl
  sha256: ce6414590005693a58325b89c064a3f147a944702788698fc69b64d29c2f8f19
reviewed_artifacts:
- path: /tmp/qa_TWIN-69_ew7xy2c1/request.json
  sha256: 84d93decdcbaef41e9405242110c8731403ab7978a09ad8887c9c530cdb1a328
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/test_harness.patch
  sha256: 461c5597412442efc51a223b3ba691764ba725b54be2e666393e18d0e19c5224
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_ew7xy2c1/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: a099afaccf61f297f4df2b8c9c0567acfc12d0be3792a7babec1299fff40ed2d
- path: /tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: 1a34b08925dada94988baa625f3c9c11b15bf43247df238071eb40e95b255864
- path: /tmp/qa_sandboxes/TWIN-69_run_101104_20261107_021104/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  sha256: 138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594
verification_scope: 已核对 task revision 2 的接受范围、上一轮 QA 报告（SHA256 匹配）、上一候选至本候选的定向差异（SHA256
  匹配）、本轮 request/evidence 索引与 runtime/verdict 哈希，以及声明源码和手册哈希。范围内检查涵盖 CLI 串口部署、默认 512B
  与 76,896B/151 块正向证据、非法分块拒绝、能力位和 revision 5 手册、要求的软件回归及恢复相关 CASE-63 证据。已校验的 server
  证据报告命令通过，PTY 验证覆盖 921600。物理 HIL 硬件执行不在接受范围内，未声称通过。source_report 为空。
verification_environment: docker-sandbox-and-independent-codex-audit
```

上一轮同角色 QA 报告及本轮定向差异的哈希均匹配。新增串口传输与 PTY 证据修复了上一轮指出的虚拟靶机阻断；但本轮源码仍可能静默使用与 --baud 不同的实际波特率，未满足接受范围中的串口参数要求。
