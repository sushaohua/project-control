```yaml
task_id: TWIN-63
task_revision: 3
candidate_commit: faa2ed00dc9b6c8567dd44e875028f65073aab62
role: QA
decision: APPROVED
summary: 复验通过。上一轮 QA 报告（SHA256 3549b72411ccd5932c5c85dc7bcba1db809ccae08e36eacd9932250f9cff7b3d）因
  USB Host 及互斥恢复回归证据缺失而 BLOCKED。本轮增量加入 USB Host 成功、坏 trailer_crc32 擦除前拒绝、USB/UART2
  双向互斥和锁释放后恢复用例；冻结 Runner 证据显示测试命令退出码为 0，服务端 verdict 为 PASSED。
findings:
- 本轮定向差异 SHA256 与索引一致；坏 trailer_crc32 用例断言擦除计数为零，USB/UART2 双向竞争及释放后重试恢复用例均由冻结测试执行通过。
- 已核对冻结 runtime.log、server_verdict.json、request.json 与上一轮报告的 SHA256；Runner 记录 test_count=1、exit_code=0、build_count=0。
- 未将硬件验证视为通过；本结论仅覆盖接受的 Docker QA 沙箱与宿主机单测范围。
accepted_scope: MC Bootloader USART2 MiniMCProto v2.0 本机升级、DST=0x02 与 USART6 隔离、UPG2、USB
  Host U 盘升级及 trailer_crc32 校验、USB/UART2 单写者互斥和竞争后恢复、错误 board_id/坏 trailer_crc32/超边界时零擦除拒绝、MC/TH
  打包边界、宿主机单测、C 函数规模/参数及中文注释门禁。arm-none-eabi-gcc 交叉编译和实体 HIL 烧录按接受范围排除。
unexecuted: []
actual_session: 01a1aee0-ca6e-7171-9879-a685189d67c9
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=2a86f91735f6865626b0794b726d90e1f2247d68;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1; boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62;
  boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
server_qa:
  task_id: TWIN-63
  task_revision: 3
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 7bc161ad87d0
    id: TWIN-63_run_112122_20261106_032122
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122
    developer_mounts: []
    container_inspect:
      id: 7bc161ad87d0b73011d095e75c79b24d1b2b000598601c6b7d44732ef6a32ec4
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T03:22:06.399254445Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-63_f3qib5qt/evidence/server_lock.json
    sha256: e509b0c419988ed5ed5d3352743d078201da38ad530a26ac98528945e70b4b81
  checkout_log:
    path: /tmp/qa_TWIN-63_f3qib5qt/evidence/checkout.log
    sha256: 82b2296d24ec059513b604033b9bf71fe26adc30b9544f4d38798ce9f4f20335
  runtime_log:
    path: /tmp/qa_TWIN-63_f3qib5qt/evidence/runtime.log
    sha256: 96a8f2d0c6dbac889ca7cc73ff8dfacead9384d76e0377c5138f14d7092cd503
  server_verdict:
    path: /tmp/qa_TWIN-63_f3qib5qt/evidence/server_verdict.json
    sha256: 0b1b03b4abef0a6577cb7e6cf16591a3ebebb112805b6e7ec2f9c6d16bdf2b24
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: 'cat ../../project-control/docs/evidence/twin/TWIN-63/runs/author_01/result.md
      && ! grep -rn "USART6" bootloader/src/ bootloader/inc/ && echo "[PASS] Zero
      USART6 coupling in MC Bootloader source/headers!" && rm -rf /tmp/qa_twin63 &&
      cp -r . /tmp/qa_twin63 && cd /tmp/qa_twin63 && mkdir -p build && sed -n "20,99p"
      tests/run_tests.sh | sh && python3 -c "import pathlib, re, sys; files = [\"app_test/inc/th_upgrade_mgr.h\",
      \"bootloader/inc/boot_uart_ota.h\", \"bootloader/src/boot_uart_ota.c\", \"bootloader/src/main.c\",
      \"bootloader/src/usbh_user.c\", \"scripts/pack_firmware.py\", \"tests/test_mc_boot_ota.c\"];
      cjk = re.compile(r\"[\\u4e00-\\u9fff]\"); [ (txt := pathlib.Path(p).read_text(encoding=\"utf-8\"),
      assert_cjk := sum(1 for l in txt.splitlines() if cjk.search(l)) >= 3, print(f\"[DOC-CHECK
      PASS] {p}: cjk_lines={sum(1 for l in txt.splitlines() if cjk.search(l))}\"),
      (sys.exit(1) if not assert_cjk else None)) for p in files ]; print(\"[PASS]
      code_documentation_standard check passed!\")" && rm -rf /tmp/qa_twin63'
    exit_code: '0'
    subpath: boot/bootloadermc
    duration: 0.49s
    output: "# TWIN-63 Author Verification Report (`author_01`)\n\n- **Task ID**:\
      \ `TWIN-63`\n- **Role**: `ENG_BOOT_MC` (`eng-vertical`)\n- **Repository / Branch**:\
      \ `boot/bootloadermc` / `soc_debug`\n- **Base Commit**: `4fc171ea61912561949b9a0cfc1da8975e4c39ba`\n\
      - **Candidate Commit**: `faa2ed00dc9b6c8567dd44e875028f65073aab62`\n\n## 1.\
      \ Rule Entry & Read Sources Registration\n- `boot/bootloadermc/.repo-rules/AGENTS.md`\n\
      - `boot/bootloadermc/.repo-rules/SOURCE.json` (`source_commit`: `fa1c2dd52a699757ab2e8f81bfefba914dd4d23c`)\n\
      - `boot/bootloadermc/AGENTS.md`\n- `project-control/.agents/rules/bootloader_role_boundaries.md`\
      \ (`version`: `1.0`)\n- `project-control/.agents/rules/c_cpp_coding_standard.md`\
      \ (`version`: `1.2`)\n- `project-control/.agents/rules/code_documentation_standard.md`\
      \ (`version`: `1.0`)\n- `project-control/docs/planning/minimc_v2_unified_mcu_upgrade_proposal_20261105.md`\
      \ (`revision`: `3`)\n- `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-63.md`\
      \ (`revision`: `2`)\n\n## 2. Summary of Changes\n1. **MiniMCProto v2.0 (Rev\
      \ 2.0.4) 7-Command Subset (`bootloader/inc/boot_uart_ota.h`, `bootloader/src/boot_uart_ota.c`)**:\n\
      \   - Implemented `USART2` (`PA2 TX / PA3 RX @ 921600 8N1`, `GPIO_MUX_7`, `1024B`\
      \ ISR ring buffer) and `DST == 0x02 (MINIMC_NODE_MC)` 7-command OTA state machine\
      \ (`0x01/0x02` with `capability_flags = 0xC0080435U` & dynamic `boot_id`, `0x03/0x04`,\
      \ `0x1D`, `0x20` 144B pre-erase ATSG admission, `0x21` 520B max payload with\
      \ 2KB sector erase on boundary + readback verify + retransmit idempotency, `0x23`\
      \ 8B status, `0x22` 8B full-image IEEE CRC32 verify + jump).\n   - Strictly\
      \ filtered out `DST == 0x03 (MINIMC_NODE_TH)` frames (zero `USART6` coupling).\n\
      \   - Implemented `UPG2` (`0x55504732UL` at `0x2005FFF0UL`) stay-in-boot magic\
      \ word detection and clearing.\n2. **USB Host vs `USART2` Single-Writer Mutex\
      \ & Shared 128B Trailer Gate (`bootloader/src/usbh_user.c`, `bootloader/src/main.c`)**:\n\
      \   - Unified USB Host `verify_firmware_trailer()` and `USART2` `0x20 CMD_OTA_START`\
      \ on `boot_verify_trailer_struct(&trailer, BOARD_ID_MC_AT32F435, MC_MAX_APP_SIZE)`\
      \ (checking `magic`, `struct_ver == 0x00010000U`, `board_id == 0x43500001U`,\
      \ `0 < payload_len <= 917,504B`, and `trailer_crc32` over first 124B).\n   -\
      \ Implemented `boot_ota_acquire_writer()` / `boot_ota_release_writer()` single-writer\
      \ lock between USB Host (`BOOT_WRITER_USB`) and `USART2` (`BOOT_WRITER_UART2`).\n\
      \   - Added `boot_uart_ota_deinit()` to `deinit_bootloader_peripherals()` in\
      \ `jump_to_app()`.\n3. **236KB TH / 896KB MC Boundary Alignment (`app_test/inc/th_upgrade_mgr.h`,\
      \ `scripts/pack_firmware.py`)**:\n   - Updated `TH_FLASH_MAX_APP_SIZE` to `236U\
      \ * 1024U` (`241,664B`) and enforced net payload bounds (`MC <= 917,504B`, `TH\
      \ <= 241,664B`) in `scripts/pack_firmware.py`.\n\n## 3. Verification Results\n\
      - Command: `rm -rf /tmp/qa_twin63 && cp -r . /tmp/qa_twin63 && cd /tmp/qa_twin63\
      \ && sh tests/run_tests.sh && rm -rf /tmp/qa_twin63`\n- Result: **PASS (Exit\
      \ Code 0)**\n  - `build/bootloader.bin` = `36,612` bytes (`27.93%` of `131,072B`\
      \ 128KB budget), zero `USART6` coupling.\n  - `scripts/pack_firmware.py` boundary\
      \ checks (`917,504B` pass, `917,505B` fail; `241,664B` pass, `241,665B` fail):\
      \ **PASS**.\n  - Host unit test `test_mc_boot_ota`: **PASS**.\n  - C function\
      \ length (`<= 50` lines) and parameter count (`<= 4` params) gate: **PASS**.\n\
      [PASS] Zero USART6 coupling in MC Bootloader source/headers!\n=== [2/4] Verify\
      \ scripts/pack_firmware.py MC (896KB=917,504B) & TH (236KB=241,664B) boundary\
      \ gate ===\n==================================================\n [PACK] Firmware\
      \ packaging complete\n - Input raw binary: /tmp/tmpm95lpr24/mc_ok.bin (917504\
      \ bytes)\n - Target Board ID: 0x43500001 [MC (AT32F435)]\n - Firmware Version:\
      \ 0x01000000\n - SHA-256 Digest: 4438bd37db902e5676b4f257f2d6b2b479bdb88ec501bb3824a96e09f1c4568e\n\
      \ - Output File: /tmp/tmpm95lpr24/fw_mc.bin (917632 bytes)\n==================================================\n\
      ==================================================\n [PACK] Firmware packaging\
      \ complete\n - Input raw binary: /tmp/tmpm95lpr24/th_ok.bin (241664 bytes)\n\
      \ - Target Board ID: 0x42300001 [TH (AT32F423)]\n - Firmware Version: 0x01000000\n\
      \ - SHA-256 Digest: 8aba5e9a7cf5158a11d210bb3edfe208bc67088e6f093e8e32c026629aabf2a6\n\
      \ - Output File: /tmp/tmpm95lpr24/fw_th.bin (241792 bytes)\n==================================================\n\
      [PASS] scripts/pack_firmware.py MC(896KB) & TH(236KB) boundary checks passed!\n\
      === [3/4] Compile & run host unit tests for MC Bootloader MiniMCProto v2.0 OTA\
      \ ===\nFAT32 File System initialized.\nSearching for upgrade package (fw_mc.bin)...\n\
      Found: firmwaremc.bin, Size: 1152 bytes, Target: 0x08020000\nStarting firmware\
      \ flash programming...\n[PRE-VERIFY] REJECTED: Trailer check failed (rc=-6,\
      \ magic=0x41545347, board=0x43500001)\n[SECURITY GATE] Pre-verification FAILED.\
      \ Flash erase ABORTED!\nUpgrade failed!\n[BOOT] FS Check PASSED: 0:/firmwaremc.bin\
      \ -> 0:/firmwaremc.err verified (Size=1152 B).\nFAT32 File System initialized.\n\
      Searching for upgrade package (fw_mc.bin)...\nFound: firmwaremc.bin, Size: 1152\
      \ bytes, Target: 0x08020000\nStarting firmware flash programming...\n[PRE-VERIFY]\
      \ PASS: MC Firmware verified. Payload: 1024 B, Ver: 0x01020300\nErasing 1 sectors\
      \ (2KB each) from 0x08020000...\nWriting image to Flash (1024 B)...\nCRC32 Check\
      \ OK: 0x7C87C1A0\nUpgrade firmwaremc.bin successful!\n[BOOT] FS Check PASSED:\
      \ 0:/firmwaremc.bin -> 0:/firmwaremc.cur verified (Size=1152 B).\nJumping to\
      \ Application at 0x08020000...\nFAT32 File System initialized.\nSearching for\
      \ upgrade package (fw_mc.bin)...\n[BOOT] UART2 OTA active, deferring USB U-disk\
      \ upgrade.\nFAT32 File System initialized.\nSearching for upgrade package (fw_mc.bin)...\n\
      Found: firmwaremc.bin, Size: 1152 bytes, Target: 0x08020000\nStarting firmware\
      \ flash programming...\n[PRE-VERIFY] PASS: MC Firmware verified. Payload: 1024\
      \ B, Ver: 0x01020300\nErasing 1 sectors (2KB each) from 0x08020000...\nWriting\
      \ image to Flash (1024 B)...\nCRC32 Check OK: 0x7C87C1A0\nUpgrade firmwaremc.bin\
      \ successful!\n[BOOT] FS Check PASSED: 0:/firmwaremc.bin -> 0:/firmwaremc.cur\
      \ verified (Size=1152 B).\nJumping to Application at 0x08020000...\n[PASS] test_mc_boot_ota:\
      \ all MC Bootloader MiniMCProto v2.0 & USB Host tests passed!\n=== [4/4] Verify\
      \ C function length (<=50 lines) and parameter count (<=4) gate ===\n[PASS]\
      \ All checked C functions satisfy <=50 lines and <=4 parameters!\n[DOC-CHECK\
      \ PASS] app_test/inc/th_upgrade_mgr.h: cjk_lines=24\n[DOC-CHECK PASS] bootloader/inc/boot_uart_ota.h:\
      \ cjk_lines=36\n[DOC-CHECK PASS] bootloader/src/boot_uart_ota.c: cjk_lines=36\n\
      [DOC-CHECK PASS] bootloader/src/main.c: cjk_lines=10\n[DOC-CHECK PASS] bootloader/src/usbh_user.c:\
      \ cjk_lines=20\n[DOC-CHECK PASS] scripts/pack_firmware.py: cjk_lines=18\n[DOC-CHECK\
      \ PASS] tests/test_mc_boot_ota.c: cjk_lines=41\n[PASS] code_documentation_standard\
      \ check passed!\n\n[ERROR] Payload size 917505 B out of bounds for board 0x43500001\
      \ (allowed: 1..917504 B)\n[ERROR] Payload size 241665 B out of bounds for board\
      \ 0x42300001 (allowed: 1..241664 B)"
  passed: true
  timestamp: '2026-11-06T03:22:09.586485+00:00'
  path: /tmp/qa_TWIN-63_f3qib5qt/evidence/server_qa.json
  sha256: 0821003692b7da706995444e8875dd526d62f4e543fa7940b60d94129b06f1c2
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-63_f3qib5qt/reviews/c5c14d1d16694cf5aff28d2985eaef6d/codex.jsonl
  sha256: db5f8f984439e8beb7ad51d62fc504f96d4ec6115931439e91edcc66e2096a4b
reviewed_artifacts:
- path: /tmp/qa_TWIN-63_f3qib5qt/request.json
  sha256: 3166a156d83c33b334597830dca23d9e60126aedc8029c0deb3e9e45869f892b
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/boot/bootloadermc.patch
  sha256: 9d68cd9deda83c4d9f399ff3bc0494cdd2608a5f9b67703c0876166e05247820
- path: /tmp/qa_TWIN-63_f3qib5qt/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/bsp_eeprom.h
  sha256: 91087c571cc93c1d43a40f0ab86d28181d5db6f518ccd9e862496680722db1a0
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/ffconf.h
  sha256: 923ec63f48173a68a293409cc9fd6c78826ec3686e784ebf6f35e3f393d3b93d
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/at32f435_437_clock.h
  sha256: 5bd4b8d53ca78bb9181868848ddcbe3ccc7a0ba69060068ae7260af6ccac1b33
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/usb_conf.h
  sha256: 45070d470191cf82a88005cfade11de12d81dba1a065da654d527cfa47cd3971
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/bsp_board_pinout.h
  sha256: db74fbd4cd1b06752b49219fbec33d64300a3cbad1ddbaa5449b024371e16b8a
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/firmware_trailer.h
  sha256: eb1cb85080905a1298d6292c4dafc9f99a06f0fb2753d7e096343e157fe13bf6
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/bsp_uart.h
  sha256: 42bb216c7de1727fe3c2136bb6808a4052aa58d3e952136adb62876357947559
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/usbh_user.h
  sha256: 5a26c9ceb338fbf2ead8c738ebee673539559a736fc32c0bf0a92288ef1ed996
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/at32f435_437_int.h
  sha256: 59c8ab8a2d39845685c0d0d3421b5321e53dad74270524f68ef913659827d293
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/at32f435_437_conf.h
  sha256: 52d16fb6d2d2ac3063e6322f4fbf319cd28d4e34e23d336435ed1c2fe3d6ed6c
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/inc/boot_uart_ota.h
  sha256: c41a475d5fd75e996888f6f9b94d8fe3a617f3e701b6eff769f7ccf0b442bc9d
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/usbh_msc_diskio.c
  sha256: 176bcf111e43184c11ae432ad56e529ade777ec450ca76884e4710dbbd054ad0
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/bsp_eeprom.c
  sha256: 036c437ecdbfc8e0befc1d8ddf10e7a66a3b48fc7f746a4d7e678a73079f97dd
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/main.c
  sha256: c2a9b7221fa6d21001ed2fdbefe1fd5b6e04db0f14b93d719ff26d24770332c2
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/at32f435_437_int.c
  sha256: 0fa3c5124221ffed50f9f807239e64df2ce9e48768733fdbc31f43553c1f2b59
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/bsp_uart.c
  sha256: 171599be441d588bc2250cb2786a87b370c1108f4774e758d19173486f3f12eb
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/at32f435_437_clock.c
  sha256: adcb89cec3ac22fde5c093cd07901bbfd19a2e9639926adb3c5cea5f8f345d9b
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/boot_uart_ota.c
  sha256: 679c2ffffdbe5214879f6d25b8ad3cdaa9a3d69bd48507f78abef959828c9206
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/bootloader/src/usbh_user.c
  sha256: 3a2955a3dd79651ddb3e72ce98e4d12f5ecf9246d4df75665760b62b3e2e15bd
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/scripts/pack_firmware.py
  sha256: 4aeb55ad8ded5b1f508fd2624d0cf0d8fb34a2e6f82539688641695d80059e4a
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/app_test/inc/th_upgrade_mgr.h
  sha256: 5b3e28b1bcc3550e5fa251e15c75020aac80ac06818052de7815971664ab64e6
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/tests/run_tests.sh
  sha256: 820146f216a390451219d7e0815e37ba89a6aa47eb236fe552510fa2e8b4e4d3
- path: /tmp/qa_sandboxes/TWIN-63_run_112122_20261106_032122/boot/bootloadermc/tests/test_mc_boot_ota.c
  sha256: a87ecc2d27dc5f0a36b44bb29f933987c712a44d04db47d340fb1a9842a88870
verification_scope: MC Bootloader USART2 MiniMCProto v2.0 本机升级、DST=0x02 与 USART6 隔离、UPG2、USB
  Host U 盘升级及 trailer_crc32 校验、USB/UART2 单写者互斥和竞争后恢复、错误 board_id/坏 trailer_crc32/超边界时零擦除拒绝、MC/TH
  打包边界、宿主机单测、C 函数规模/参数及中文注释门禁。arm-none-eabi-gcc 交叉编译和实体 HIL 烧录按接受范围排除。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验通过。上一轮 QA 报告（SHA256 3549b72411ccd5932c5c85dc7bcba1db809ccae08e36eacd9932250f9cff7b3d）因 USB Host 及互斥恢复回归证据缺失而 BLOCKED。本轮增量加入 USB Host 成功、坏 trailer_crc32 擦除前拒绝、USB/UART2 双向互斥和锁释放后恢复用例；冻结 Runner 证据显示测试命令退出码为 0，服务端 verdict 为 PASSED。
