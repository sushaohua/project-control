```yaml
task_id: TWIN-69
task_revision: 1
candidate_commit: 54231c8d4372998bb91aefc3ec2df5c99169b274
role: QA
decision: REJECTED
summary: 冻结证据哈希匹配，范围内软件正向、负向及回归检查均有通过记录；但定向差异显示 CLI 部署入口没有按接受范围中的参数执行串口部署。
findings:
- 阻断：接受范围要求 CLI 支持 --port、--baud、--th-pkg、--mc-pkg、--receipt-out 部署参数。当前实现虽解析这些参数，但
  th-pkg/mc-pkg 分支创建 VirtualDualMcuOtaTarget 并在虚拟靶机上运行；--port 和 --baud 未用于串口通信。因此手册给出的串口部署命令无法完成实际硬件部署。
- 非阻断建议：非法 chunk size 的预期拒绝信息使用 `[FAIL]` 前缀，容易与真实测试失败混淆；可考虑改为更明确的预期拒绝提示。
- 评审说明与最终 JSON 未能分别保存为文件：当前工作区为只读，无法创建评审产物。
accepted_scope: 按已校验索引审阅 TWIN-69 revision 1 及候选提交；核对部署工具和升级测试差异、revision 5 手册内容、能力位说明、默认
  512B/151 块正向证据、非法 chunk size 负向证据及所要求的软件回归。source_report 为空。物理 HIL 硬件执行明确排除在本轮范围之外，未将其表述为已通过。
unexecuted: []
actual_session: 01a1b3bd-c81f-78c2-8297-6b47b30e9e87
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=b764378b4d3232d1c7ce77fd4922f520dd31ef51;
  soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51; mcu-p3=97c1c2422e98357e72cc822d2b5293b9e0c2abc6;
  test_harness=54231c8d4372998bb91aefc3ec2df5c99169b274; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-69
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 4e4f2cdd5a30
    id: TWIN-69_run_100010_20261107_020010
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-69_run_100010_20261107_020010
    developer_mounts: []
    container_inspect:
      id: 4e4f2cdd5a30163a8366276b7b2c63c2153a8df5863323d5925346d4c40f85f2
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-07T02:01:49.285858868Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-69_run_100010_20261107_020010
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-69_xdoffwnh/evidence/server_lock.json
    sha256: 0f03acc2fe44e28592a9ff4e06fe0bdf9aacbf6a16c010d84027dba200ba8b35
  checkout_log:
    path: /tmp/qa_TWIN-69_xdoffwnh/evidence/checkout.log
    sha256: 8b5cade674efa6e97a2473f0c5fe7f2cca648b603dcd4531c70e8bd627dc0521
  runtime_log:
    path: /tmp/qa_TWIN-69_xdoffwnh/evidence/runtime.log
    sha256: a7a2335ee103517e5c5b7e668a1794e2171b6c1935c5ecc2ab9a2934f3d7ae08
  server_verdict:
    path: /tmp/qa_TWIN-69_xdoffwnh/evidence/server_verdict.json
    sha256: b301273e767983b094cf98260fb4dfe779ea2cfeadeb45dc8c0d0491dce5ffd3
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
    duration: 9.09s
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
      \ 0xE0080423/0xC0080435->512B, 76896B=151 chunks & invalid chunk_size rejected\n\
      \n[SUMMARY] SEQ-06 Upgrade Suite: 5/5 passed.\n=== MiniMCProto v2.0 (Rev 2.0.4)\
      \ OTA Software Verification Suite ===\n\n--- 1. Static & Compile-Time Gates\
      \ (S01~S04) ---\n  [PASS] S01: 5-endpoint Rev 2.0.4 opcode table & reverse numeric\
      \ uniqueness\n  [PASS] S02: Zero 0x05/0x15 legacy drift & >=520B payload / >=534B\
      \ frame capacity\n  [PASS] S03: TH Bootloader 16KB (0x08000000..0x08003FFF)\
      \ Flash budget & 0B .bss growth\n  [PASS] S04: Function <=50 lines, <=4 params,\
      \ Chinese docstrings & inline '#' comments verified\n\n--- 2. Codec & Golden\
      \ Byte Vectors (D01~D08) ---\n  [PASS] G01: status=OK len=14B\n  [PASS] G02:\
      \ status=OK len=14B\n  [PASS] G03: status=OK len=26B\n  [PASS] G04: status=OK\
      \ len=30B\n  [PASS] G05: status=OK len=18B\n  [PASS] G06: status=OK len=18B\n\
      \  [PASS] G07: status=OK len=15B\n  [PASS] G08: status=OK len=18B\n  [PASS]\
      \ G09: status=ERR_FRAME_TOO_SHORT len=10B\n  [PASS] G10: status=ERR_BAD_SOF\
      \ len=14B\n  [PASS] G11: status=ERR_BAD_VERSION len=14B\n  [PASS] G12: status=ERR_BAD_FLAGS_RESERVED\
      \ len=14B\n  [PASS] G13: status=ERR_BAD_ROUTE_CTRL len=14B\n  [PASS] G14: status=ERR_MTU_EXCEEDED\
      \ len=1039B\n  [PASS] G15: status=ERR_CRC_MISMATCH len=14B\n  [PASS] G16: status=OK\
      \ len=158B\n  [PASS] G16a: status=OK len=158B\n  [PASS] G16b: status=OK len=86B\n\
      \  [PASS] G16c: status=OK len=534B\n  [PASS] G16d: status=OK len=59B\n  [PASS]\
      \ G16e: status=OK len=1038B\n  [PASS] G16f: status=OK len=22B\n  [PASS] G16g:\
      \ status=OK len=22B\n  [PASS] G16h: status=OK len=18B\n  [PASS] G17: status=OK\
      \ len=17B\n  [PASS] G18: status=OK len=17B\n  [PASS] G19: status=OK len=17B\n\
      \  [PASS] G20: status=OK len=17B\n  [PASS] G21: status=OK len=17B\n  [PASS]\
      \ G22: status=OK len=17B\n  [PASS] G23: status=OK len=17B\n  [PASS] G24: status=OK\
      \ len=17B\n  [PASS] G25: status=OK len=17B\n  [PASS] V01_MC_BED_NORMAL_60C:\
      \ status=OK len=30B\n  [PASS] V02_TH_NOZZLE_ROUTED_215C: status=OK len=30B\n\
      \  [PASS] V03_TH_SENSOR_OPEN_FAULT_SENTINEL: status=OK len=30B\n  [PASS] V04_AP_PRIORITY_ESTOP_CMD:\
      \ status=OK len=15B\n  [PASS] D01: G01~G04 Ping/Pong/GetVersion/VersionReport(16B)\
      \ round-trip\n  [PASS] D02: G05~G06 0x1D CMD_SYSTEM_CONTROL(4B) & 0x00 CMD_ACK(4B)\n\
      \  [PASS] D03: G07~G08 0x17 CMD_EMERGENCY_STOP(1B) & priority 0x00 CMD_ACK\n\
      \  [PASS] D04: G09~G15 Framing negative rejection (SHORT/SOF/VER/FLAGS/ROUTE/MTU/CRC)\n\
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
      \n[SUMMARY] OTA Software Suite: 39 passed, 0 failed.\n\n[FAIL] invalid --chunk-size=0\
      \ (must be 1..512)\n[FAIL] invalid --chunk-size=513 (must be 1..512)\ntest_case60_th_cascaded_upgrade\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-60 TH\
      \ 级联四阶段升级单测断言。 ... ok\ntest_case61_ordered_th_then_mc_upgrade (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n\
      执行 HIL-CASE-61 先 TH 后 MC 顺序四阶段升级单测断言。 ... ok\ntest_case62_pre_erase_and_busy_interlocks\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-62 擦除前零擦除门禁与忙状态互锁单测断言。\
      \ ... ok\ntest_case63_interruption_and_stage4_isolation (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n\
      执行 HIL-CASE-63 中途掉电首块保护重传与 Stage 3/4 隔离单测断言。 ... ok\ntest_case64_default_512b_chunk_and_76896b_th_stream\
      \ (test_mcu_firmware_upgrade.TestMcuFirmwareUpgradeSuite)\n执行 HIL-CASE-64 默认\
      \ 512B 分块、76,896B TH 151 块流式升级与非法分块拒绝断言。 ... [FAIL] invalid --chunk-size=0 (must\
      \ be 1..512)\n[FAIL] invalid --chunk-size=513 (must be 1..512)\nok\n\n----------------------------------------------------------------------\n\
      Ran 5 tests in 0.177s\n\nOK"
  passed: true
  timestamp: '2026-11-07T02:02:00.962925+00:00'
  path: /tmp/qa_TWIN-69_xdoffwnh/evidence/server_qa.json
  sha256: 29c7727bd1156e2f20aa5a2c84eabf2688a11cc7e9e61cc1104aa671e36a0337
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-69_xdoffwnh/reviews/2b1ec339459e48debc10f0e1d18d8aac/codex.jsonl
  sha256: 10dc321482844f75974a391e5d3ec16fbc8a2ec628e9e97c5f9904e2a04faabe
reviewed_artifacts:
- path: /tmp/qa_TWIN-69_xdoffwnh/request.json
  sha256: bde07739199842c534ff6829406f7b8a57403fa7c6157280d0348aca53b2f598
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/test_harness.patch
  sha256: ee929751ee47ef39658cd43fe8ded852d5313cb161827b704b05c4bb272b3cfa
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-69_xdoffwnh/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-69_run_100010_20261107_020010/test_harness/hil/tools/hil_deploy_via_minimc_ota.py
  sha256: fcc8045fb231e3dfbd4847a11b4a236d3376e6284b2d5b3aaaae0965657a780d
- path: /tmp/qa_sandboxes/TWIN-69_run_100010_20261107_020010/test_harness/hil/tests/test_mcu_firmware_upgrade.py
  sha256: c18a3e05f200c9b73ea067614768966282d2ff349ec4f07216cc4bb6127186cb
- path: /tmp/qa_sandboxes/TWIN-69_run_100010_20261107_020010/project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
  sha256: 138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594
verification_scope: 按已校验索引审阅 TWIN-69 revision 1 及候选提交；核对部署工具和升级测试差异、revision 5 手册内容、能力位说明、默认
  512B/151 块正向证据、非法 chunk size 负向证据及所要求的软件回归。source_report 为空。物理 HIL 硬件执行明确排除在本轮范围之外，未将其表述为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

冻结证据哈希匹配，范围内软件正向、负向及回归检查均有通过记录；但定向差异显示 CLI 部署入口没有按接受范围中的参数执行串口部署。
