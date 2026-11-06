```yaml
task_id: TWIN-62
task_revision: 2
candidate_commit: 9b40f8fb7c4bb6008126e94653f615039bad4d64
role: QA
decision: BLOCKED
summary: 已核对 bundle、任务范围、冻结运行证据和定向差异。服务器记录的命令通过，但验收要求的负向证据未完整覆盖，暂不能确认全部范围。
findings:
- 阻断：接受范围要求 0x20 的坏 trailer_crc32 请求返回 NACK 且不擦除 Flash。测试 test_ota_start_negative_zero_erase
  覆盖超限和错 board_id，但未构造坏 trailer_crc32 请求，因此此项必需负向证据缺失。源码中的 iap_trailer_validate 检查不能替代该验收证据。
- 冻结证据索引、server_verdict.json、runtime.log 与定向差异的 SHA256 均与索引相符；运行记录为 PASSED、exit_code
  0。author_01/result.md 的内容随冻结命令输出可核对。source_report 为空，无需核验 source_report SHA256。
- 差异涉及范围内文件；boot/bootloadermc、soc-ap、mcu-p3、test_harness 和 project-control 均无差异。未发现接受范围之外的改动。
- 非阻断建议：为 OTA_START 坏 trailer CRC 增加零擦除断言，并在失败会话后验证状态机及后续请求恢复。
accepted_scope: 审查 TWIN-62 revision 2 的 MiniMCProto v2.0 TH Bootloader 接受范围：7 命令最小升级子集、Chunk
  0 RAM 缓存、Anchor 两阶段提交、236KB 上限、pack_firmware.py 边界检查、宿主机状态机单测及函数规模/中文注释门禁。arm-none-eabi-gcc
  交叉编译与 16KB 链接器验证由 author_01/result.md 记录且明确排除在本 Docker QA 沙箱范围外；实体 HIL 烧录由 TWIN-67
  覆盖且排除在本范围外，未将其描述为本轮验证通过。
unexecuted:
- 接受范围内的坏 trailer_crc32 负向用例及零 Flash 擦除结果缺少可核验证据。
actual_session: 01a1aeba-0471-76f1-a63a-46001d2ac41e
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=45c5cdf791ae3d88b76949525ec1b46d25832083;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1; boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba;
  boot/bootloaderth=9b40f8fb7c4bb6008126e94653f615039bad4d64
server_qa:
  task_id: TWIN-62
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 558bd12b6b09
    id: TWIN-62_run_103910_20261106_023910
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910
    developer_mounts: []
    container_inspect:
      id: 558bd12b6b094e7316e81bc817fea92812dc8f3d570745d20cb08d7014db8d28
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T02:39:45.101993965Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-62_sgr60z_9/evidence/server_lock.json
    sha256: 4772d06e5beba5ab635b5133a49d573cbac7c16867bb8882dca661ff6fa52b51
  checkout_log:
    path: /tmp/qa_TWIN-62_sgr60z_9/evidence/checkout.log
    sha256: 50a7160ab7897afce0ee007aa74e39ec6dabc1ff3fe899ffa424c8e044d48055
  runtime_log:
    path: /tmp/qa_TWIN-62_sgr60z_9/evidence/runtime.log
    sha256: 655e8cb2b9d96f612f064e51ce0f4c7fe7138320a721d4a3cf89da5cfbb79432
  server_verdict:
    path: /tmp/qa_TWIN-62_sgr60z_9/evidence/server_verdict.json
    sha256: 7ec2b1ff250568b7d7caff8eacd7418c3e6734c4d0c3c8622f422b6de091d2aa
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: 'cat ../../project-control/docs/evidence/twin/TWIN-62/runs/author_01/result.md
      && python3 -c "import subprocess, sys, tempfile, os; tmpd = tempfile.mkdtemp();
      [ (open(os.path.join(tmpd, f\"in_{sz}.bin\"), \"wb\").write(b\"\\x5A\" * sz),
      res := subprocess.run([sys.executable, \"tools/pack_firmware.py\", os.path.join(tmpd,
      f\"in_{sz}.bin\"), os.path.join(tmpd, f\"out_{sz}.bin\")], capture_output=True,
      text=True), assert_ok := (res.returncode == 0 and os.path.getsize(os.path.join(tmpd,
      f\"out_{sz}.bin\")) == sz + 128) if ok else (res.returncode != 0), (sys.exit(1)
      if not assert_ok else None)) for sz, ok in [(241663, True), (241664, True),
      (241665, False), (245760, False)] ]; print(\"[PASS] S03 pack_firmware.py 236KB
      boundary checks (241663/241664/241665/245760) passed!\")" && gcc -std=c11 -O2
      -Wall -Wextra -Werror -DIAP_HOST_TEST -DDEBUG_LOG_ENABLE=0 -Iinc src/iap.c src/flash.c
      tests/test_th_boot_ota.c -o /tmp/test_th_boot_ota && /tmp/test_th_boot_ota &&
      rm -f /tmp/test_th_boot_ota && python3 -c "import pathlib, re, sys; files =
      [\"inc/iap.h\", \"inc/flash.h\", \"inc/usart.h\", \"src/iap.c\", \"src/flash.c\",
      \"src/main.c\", \"src/usart.c\", \"tools/pack_firmware.py\", \"tests/test_th_boot_ota.c\"];
      cjk = re.compile(r\"[\\u4e00-\\u9fff]\"); [ (txt := pathlib.Path(p).read_text(encoding=\"utf-8\"),
      assert_cjk := sum(1 for l in txt.splitlines() if cjk.search(l)) >= 3, print(f\"[DOC-CHECK
      PASS] {p}: cjk_lines={sum(1 for l in txt.splitlines() if cjk.search(l))}\"),
      (sys.exit(1) if not assert_cjk else None)) for p in files ]; print(\"[PASS]
      S04 & code_documentation_standard check passed!\")"'
    exit_code: '0'
    subpath: boot/bootloaderth
    duration: 0.43s
    output: "# TWIN-62 Author Self-Check Result (`author_01`)\n\n- **Task ID**: `TWIN-62`\n\
      - **Role**: `ENG_BOOT_TH` (`eng-vertical`)\n- **Repository & Branch**: `boot/bootloaderth`\
      \ (`soc_debug`)\n- **Base Commit**: `769fccbe52464ad7ceb856c5e89cb0d25abbbf87`\n\
      - **Candidate Commit**: `9b40f8fb7c4bb6008126e94653f615039bad4d64`\n\n## 1.\
      \ Read Sources Registered (`read_sources`)\n- `boot/bootloaderth/.repo-rules/AGENTS.md`\n\
      - `boot/bootloaderth/.repo-rules/SOURCE.json` (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)\n\
      - `boot/bootloaderth/AGENTS.md`\n- `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md`\
      \ (`revision: 2`, `sha256: b30cf87bcda5b7f7e49fd34d0df5bd2a29d21631ffbd7171331a49e13d1757c6`)\n\
      - `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md`\
      \ (`Rev 2.0.4`, `sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)\n\
      - `project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md`\
      \ (`revision: 1`, `sha256: c79477a0b9bfa2b18d1451b91b2a6188aa4b50f72bc742a8640aa0a696a1610b`)\n\
      - `project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md`\
      \ (`revision: 2`, `sha256: f41d27c2214cacd1113397f20eb50038a404df94781f4bfdb18239d5d6f246d9`)\n\
      - `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`\
      \ (`revision: 1`, `sha256: 87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9`)\n\
      \n## 2. Summary of Changes\n1. **MiniMCProto v2.0 Minimal 7-Command Subset (`inc/iap.h`,\
      \ `src/iap.c`, `src/main.c`)**:\n   - Removed legacy `0x5A 0xA5` frame header,\
      \ `CMD_TH_HELLO (0x10)` ~ `ACK_TH_FINISH (0x93)` macros, and 8-bit additive\
      \ checksum.\n   - Implemented `DST == 0x03` MiniMCProto v2.0 7-command state\
      \ machine (`0x01/0x02` with `capability_flags=0xE0080423U` & dynamic `boot_id`,\
      \ `0x03/0x04`, `0x1D`, `0x20 [144B]`, `0x21 [520B max]`, `0x23 [8B]`, `0x22\
      \ [8B]`, plus `0x00 CMD_ACK [4B]` / `0x06 CMD_NACK [3B]`).\n   - Enforced pre-erase\
      \ `144B` (`16B` header + `128B` ATSG Trailer) admission in `0x20 CMD_OTA_START`\
      \ (`241,665B` oversize rejected with `NACK 0x14` and `0` Flash erase; wrong\
      \ board/CRC rejected with `NACK 0x06` and `0` Flash erase).\n   - Preserved\
      \ Chunk 0 (`offset < 512`) SRAM caching (`ota_state = 2`, `cached_chunk0_bytes\
      \ = 512`, `bytes_written = 0`) and two-phase commit in `0x22 CMD_OTA_FINISH`\
      \ (Sector 127 Anchor `0x0803F800` written first, then Chunk 0 at `0x08004000`).\n\
      2. **Anchor Integrity Gate & 236KB Alignment (`inc/flash.h`, `src/flash.c`,\
      \ `tools/pack_firmware.py`)**:\n   - Fixed `bsp_flash_app_integrity_check()`\
      \ / `flash_verify_app_integrity()` so missing Anchor at `0x0803F800` returns\
      \ `false` and stays in Bootloader.\n   - Aligned `MAX_PAYLOAD_SIZE = 236 * 1024`\
      \ (`241,664B`) in `tools/pack_firmware.py` and `inc/iap.h`.\n3. **16KB Flash\
      \ / 48KB SRAM Budget (`S01/S02/S03/S04`)**:\n   - `build/bootloaderth.bin` is\
      \ **`9,360` bytes** (`57.13%` of `16,384B`, free margin `+7,024B`); `.data +\
      \ .bss + ._user_heap_stack` ends at `0x20000F04`, well below `0x20008000` magic\
      \ region.\n   - Added `tests/test_th_boot_ota.c` and `tests/run_tests.sh`.\n\
      \n## 3. Verification Output\n```text\ntext=9348, data=12, bss=3836, dec=13196,\
      \ hex=338c (build/bootloaderth.elf)\nbootloaderth.bin size: 9360 bytes (limit:\
      \ 16384 bytes)\n[PASS] S01 linker overflow gate rejected >16KB image with exit\
      \ code 1\n[PASS] S03 pack_firmware.py 236KB boundary checks (241663/241664/241665/245760)\
      \ passed!\n[PASS] test_th_boot_ota: all TH Bootloader MiniMCProto v2.0 tests\
      \ passed!\n[PASS] S04 all C functions in boot/bootloaderth satisfy <=50 lines\
      \ and <=4 parameters!\n```\n[PASS] S03 pack_firmware.py 236KB boundary checks\
      \ (241663/241664/241665/245760) passed!\n[PASS] test_th_boot_ota: all TH Bootloader\
      \ MiniMCProto v2.0 tests passed!\n[DOC-CHECK PASS] inc/iap.h: cjk_lines=49\n\
      [DOC-CHECK PASS] inc/flash.h: cjk_lines=26\n[DOC-CHECK PASS] inc/usart.h: cjk_lines=22\n\
      [DOC-CHECK PASS] src/iap.c: cjk_lines=38\n[DOC-CHECK PASS] src/flash.c: cjk_lines=32\n\
      [DOC-CHECK PASS] src/main.c: cjk_lines=13\n[DOC-CHECK PASS] src/usart.c: cjk_lines=27\n\
      [DOC-CHECK PASS] tools/pack_firmware.py: cjk_lines=16\n[DOC-CHECK PASS] tests/test_th_boot_ota.c:\
      \ cjk_lines=31\n[PASS] S04 & code_documentation_standard check passed!"
  passed: true
  timestamp: '2026-11-06T02:39:48.260218+00:00'
  path: /tmp/qa_TWIN-62_sgr60z_9/evidence/server_qa.json
  sha256: 387cd8cdab847d6949a5198af5ecb36faa2ee7da4443480d974a36e73d798449
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-62_sgr60z_9/reviews/9556071bfa664dccbf63e5526fed7c26/codex.jsonl
  sha256: 44ac8fd9b5c1b15297cf846544d87c8f4a5373a18567460e0767093741e8c9d2
reviewed_artifacts:
- path: /tmp/qa_TWIN-62_sgr60z_9/request.json
  sha256: 1cc13ec308861e4afab712ef8c9a27186f447b43c2b1aa8de84ea66566a4508e
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_sgr60z_9/diffs/boot/bootloaderth.patch
  sha256: 514289e15251131b9346563913544a99355a95ef4f10e56a6509a0720c8250cb
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/inc/iap.h
  sha256: 6ad97d450397bc0e46ca1111cdc16e28953e57e7b5a500510b1e2c44697ec4f6
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/src/iap.c
  sha256: d09851da381d74371fe6e61e6a158f5132bcb7d970158113ce07f8d8d26c196d
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/src/flash.c
  sha256: fee2c0b41d57a3a581b774fd2ce26240fa9e83d0445d7b4137e2a2e3138ece1e
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/src/main.c
  sha256: fe5b74d458afc8afdb75aeb596a3cd36af019f0f43d8d80832b8e2b37f40c7fe
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/tools/pack_firmware.py
  sha256: 8bdbffd30baf2aa7fabfe0802a218ad41c3d9605a93d8124ca84b4833bd5fe65
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/tests/run_tests.sh
  sha256: f8c3e24e547a5e5efcc336e2341470cdcfdcc2a40279e232b9ea95aec7a8f4f0
- path: /tmp/qa_sandboxes/TWIN-62_run_103910_20261106_023910/boot/bootloaderth/tests/test_th_boot_ota.c
  sha256: 21a8172d8ae14964f12eaf6d95ecca9b82998e14adfb5069c1308f4e98e0c0d3
verification_scope: 审查 TWIN-62 revision 2 的 MiniMCProto v2.0 TH Bootloader 接受范围：7
  命令最小升级子集、Chunk 0 RAM 缓存、Anchor 两阶段提交、236KB 上限、pack_firmware.py 边界检查、宿主机状态机单测及函数规模/中文注释门禁。arm-none-eabi-gcc
  交叉编译与 16KB 链接器验证由 author_01/result.md 记录且明确排除在本 Docker QA 沙箱范围外；实体 HIL 烧录由 TWIN-67
  覆盖且排除在本范围外，未将其描述为本轮验证通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核对 bundle、任务范围、冻结运行证据和定向差异。服务器记录的命令通过，但验收要求的负向证据未完整覆盖，暂不能确认全部范围。
