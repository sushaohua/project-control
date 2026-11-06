```yaml
task_id: TWIN-63
task_revision: 2
candidate_commit: 77a3651d551e88978654f5bd14688ce2f71876d6
role: QA
decision: BLOCKED
summary: 已核对锁定索引、冻结证据与定向差异；必需的 USB Host 升级及互斥恢复回归执行证据缺失，无法完成验收。
findings:
- 阻断：接受范围要求保留 USB Host U 盘升级、补齐 trailer_crc32 校验，并验证 USB/USART2 单写者互斥及拒绝后通道恢复。冻结日志中的
  test_mc_boot_ota 主机单测隔离了 USB Host 分支；没有 USB 升级成功、trailer 校验失败前零擦除，以及 USB 与串口竞争后恢复的执行证据。源码显示
  USB 路径调用共享 trailer 校验并获取互斥锁，但源码检查不能代替所需回归验证。
accepted_scope: 本次核查 MC Bootloader USART2 MiniMCProto v2.0、本机升级、DST/USART6 隔离、UPG2、USB
  Host 升级保留及 trailer_crc32 校验、USB/USART2 单写者互斥、打包边界、零擦除拒绝、宿主机单测和文档/函数门禁。arm-none-eabi-gcc
  交叉编译及实体 HIL 烧录按已接受范围明确排除。
unexecuted:
- USB Host U 盘升级成功及 trailer_crc32 无效时擦除前拒绝的回归验证。
- USB 与 USART2 实际并发竞争时后到通道被拒绝、随后可恢复升级的集成回归验证。
actual_session: 01a1aed5-f152-7be1-90a8-48358d45fb34
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=5cd627395877b8f5eccd884a83c70e3a5d0cc73a;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1; boot/bootloadermc=77a3651d551e88978654f5bd14688ce2f71876d6;
  boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
server_qa:
  task_id: TWIN-63
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: cbd560dcd430
    id: TWIN-63_run_110942_20261106_030942
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942
    developer_mounts: []
    container_inspect:
      id: cbd560dcd4306cec6db0d7f15ab94b5c11b4a1c656ac2cc37dc6527a838ec643
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T03:10:15.52115872Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-63_3by4pirp/evidence/server_lock.json
    sha256: 7e38477c1f32482aa382f4bb35ba850b0c79a00285f0d4201f90611cce43d390
  checkout_log:
    path: /tmp/qa_TWIN-63_3by4pirp/evidence/checkout.log
    sha256: 332ad227767d537605d0de076253ea29b86de7c79a47d2b0f9d90dfe83289925
  runtime_log:
    path: /tmp/qa_TWIN-63_3by4pirp/evidence/runtime.log
    sha256: 8129eef1dd8439be56de45b00d30ab0b9210ec4d355a831a188402f4e88d122a
  server_verdict:
    path: /tmp/qa_TWIN-63_3by4pirp/evidence/server_verdict.json
    sha256: b45e52254539fd12e8d221c68d08f1cfe8ac89abefa0869d562ef3e8a1fe8edc
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
    duration: 0.41s
    output: "# TWIN-63 Author Verification Report (`author_01`)\n\n- **Task ID**:\
      \ `TWIN-63`\n- **Role**: `ENG_BOOT_MC` (`eng-vertical`)\n- **Repository / Branch**:\
      \ `boot/bootloadermc` / `soc_debug`\n- **Base Commit**: `4fc171ea61912561949b9a0cfc1da8975e4c39ba`\n\
      - **Candidate Commit**: `77a3651d551e88978654f5bd14688ce2f71876d6`\n\n## 1.\
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
      \ packaging complete\n - Input raw binary: /tmp/tmp8z9750d6/mc_ok.bin (917504\
      \ bytes)\n - Target Board ID: 0x43500001 [MC (AT32F435)]\n - Firmware Version:\
      \ 0x01000000\n - SHA-256 Digest: 4438bd37db902e5676b4f257f2d6b2b479bdb88ec501bb3824a96e09f1c4568e\n\
      \ - Output File: /tmp/tmp8z9750d6/fw_mc.bin (917632 bytes)\n==================================================\n\
      ==================================================\n [PACK] Firmware packaging\
      \ complete\n - Input raw binary: /tmp/tmp8z9750d6/th_ok.bin (241664 bytes)\n\
      \ - Target Board ID: 0x42300001 [TH (AT32F423)]\n - Firmware Version: 0x01000000\n\
      \ - SHA-256 Digest: 8aba5e9a7cf5158a11d210bb3edfe208bc67088e6f093e8e32c026629aabf2a6\n\
      \ - Output File: /tmp/tmp8z9750d6/fw_th.bin (241792 bytes)\n==================================================\n\
      [PASS] scripts/pack_firmware.py MC(896KB) & TH(236KB) boundary checks passed!\n\
      === [3/4] Compile & run host unit tests for MC Bootloader MiniMCProto v2.0 OTA\
      \ ===\n[PASS] test_mc_boot_ota: all MC Bootloader MiniMCProto v2.0 tests passed!\n\
      === [4/4] Verify C function length (<=50 lines) and parameter count (<=4) gate\
      \ ===\n[PASS] All checked C functions satisfy <=50 lines and <=4 parameters!\n\
      [DOC-CHECK PASS] app_test/inc/th_upgrade_mgr.h: cjk_lines=24\n[DOC-CHECK PASS]\
      \ bootloader/inc/boot_uart_ota.h: cjk_lines=36\n[DOC-CHECK PASS] bootloader/src/boot_uart_ota.c:\
      \ cjk_lines=36\n[DOC-CHECK PASS] bootloader/src/main.c: cjk_lines=10\n[DOC-CHECK\
      \ PASS] bootloader/src/usbh_user.c: cjk_lines=26\n[DOC-CHECK PASS] scripts/pack_firmware.py:\
      \ cjk_lines=18\n[DOC-CHECK PASS] tests/test_mc_boot_ota.c: cjk_lines=29\n[PASS]\
      \ code_documentation_standard check passed!\n\n[ERROR] Payload size 917505 B\
      \ out of bounds for board 0x43500001 (allowed: 1..917504 B)\n[ERROR] Payload\
      \ size 241665 B out of bounds for board 0x42300001 (allowed: 1..241664 B)"
  passed: true
  timestamp: '2026-11-06T03:10:18.582833+00:00'
  path: /tmp/qa_TWIN-63_3by4pirp/evidence/server_qa.json
  sha256: d00f5defcfc05a4b3d213ee132fe97d415cd8f2f51e7fe6c49ac0dbf27e0d1ae
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-63_3by4pirp/reviews/5d897d69e5bf476f8c0304be48f07e16/codex.jsonl
  sha256: cfb6ae557253c2eda68bd2bb9fc2386b4bfc068e0b5f4578798cce129eb27bfe
reviewed_artifacts:
- path: /tmp/qa_TWIN-63_3by4pirp/request.json
  sha256: a6ed5c20ad46657210bd65282fc31ffbe68d643c4d2449b33f1002875e89db0d
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/boot/bootloadermc.patch
  sha256: 529ae7a4e294668b789dbe2aa761f0cddebb509e863a5eea3c64d444b8674f4b
- path: /tmp/qa_TWIN-63_3by4pirp/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/bsp_eeprom.h
  sha256: 91087c571cc93c1d43a40f0ab86d28181d5db6f518ccd9e862496680722db1a0
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/ffconf.h
  sha256: 923ec63f48173a68a293409cc9fd6c78826ec3686e784ebf6f35e3f393d3b93d
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/at32f435_437_clock.h
  sha256: 5bd4b8d53ca78bb9181868848ddcbe3ccc7a0ba69060068ae7260af6ccac1b33
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/usb_conf.h
  sha256: 45070d470191cf82a88005cfade11de12d81dba1a065da654d527cfa47cd3971
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/bsp_board_pinout.h
  sha256: db74fbd4cd1b06752b49219fbec33d64300a3cbad1ddbaa5449b024371e16b8a
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/firmware_trailer.h
  sha256: eb1cb85080905a1298d6292c4dafc9f99a06f0fb2753d7e096343e157fe13bf6
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/bsp_uart.h
  sha256: 42bb216c7de1727fe3c2136bb6808a4052aa58d3e952136adb62876357947559
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/usbh_user.h
  sha256: 5a26c9ceb338fbf2ead8c738ebee673539559a736fc32c0bf0a92288ef1ed996
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/at32f435_437_int.h
  sha256: 59c8ab8a2d39845685c0d0d3421b5321e53dad74270524f68ef913659827d293
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/at32f435_437_conf.h
  sha256: 52d16fb6d2d2ac3063e6322f4fbf319cd28d4e34e23d336435ed1c2fe3d6ed6c
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/inc/boot_uart_ota.h
  sha256: c41a475d5fd75e996888f6f9b94d8fe3a617f3e701b6eff769f7ccf0b442bc9d
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/usbh_msc_diskio.c
  sha256: 176bcf111e43184c11ae432ad56e529ade777ec450ca76884e4710dbbd054ad0
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/bsp_eeprom.c
  sha256: 036c437ecdbfc8e0befc1d8ddf10e7a66a3b48fc7f746a4d7e678a73079f97dd
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/main.c
  sha256: c2a9b7221fa6d21001ed2fdbefe1fd5b6e04db0f14b93d719ff26d24770332c2
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/at32f435_437_int.c
  sha256: 0fa3c5124221ffed50f9f807239e64df2ce9e48768733fdbc31f43553c1f2b59
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/bsp_uart.c
  sha256: 171599be441d588bc2250cb2786a87b370c1108f4774e758d19173486f3f12eb
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/at32f435_437_clock.c
  sha256: adcb89cec3ac22fde5c093cd07901bbfd19a2e9639926adb3c5cea5f8f345d9b
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/boot_uart_ota.c
  sha256: 679c2ffffdbe5214879f6d25b8ad3cdaa9a3d69bd48507f78abef959828c9206
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/bootloader/src/usbh_user.c
  sha256: 3570e93c5814b1eb85729cd6b9fdd4ec59b57bb338c4070d6066fd5f8b9c0089
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/scripts/pack_firmware.py
  sha256: 4aeb55ad8ded5b1f508fd2624d0cf0d8fb34a2e6f82539688641695d80059e4a
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/app_test/inc/th_upgrade_mgr.h
  sha256: 5b3e28b1bcc3550e5fa251e15c75020aac80ac06818052de7815971664ab64e6
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/tests/run_tests.sh
  sha256: e0cb5005389890c5ce04112f741208bf6adbff29906de2f2c8af303d4cbceb35
- path: /tmp/qa_sandboxes/TWIN-63_run_110942_20261106_030942/boot/bootloadermc/tests/test_mc_boot_ota.c
  sha256: 74db1eb325468f61bd9475cebdbc91ddb726cabfd785676da0e07dc4703f8d6d
verification_scope: 本次核查 MC Bootloader USART2 MiniMCProto v2.0、本机升级、DST/USART6 隔离、UPG2、USB
  Host 升级保留及 trailer_crc32 校验、USB/USART2 单写者互斥、打包边界、零擦除拒绝、宿主机单测和文档/函数门禁。arm-none-eabi-gcc
  交叉编译及实体 HIL 烧录按已接受范围明确排除。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核对锁定索引、冻结证据与定向差异；必需的 USB Host 升级及互斥恢复回归执行证据缺失，无法完成验收。
