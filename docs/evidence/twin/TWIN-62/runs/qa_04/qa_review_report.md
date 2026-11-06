```yaml
task_id: TWIN-62
task_revision: 4
candidate_commit: 64b7100d3b0260ad1c24b627986475dcd45ad383
role: QA
decision: APPROVED
summary: 锁定候选符合本轮接受条款。已核对冻结证据与源码哈希，并审阅定向差异、范围内正负例和恢复行为；runner 记录的范围内检查通过。
findings:
- 非阻断建议：author_01/result.md 记录的 candidate commit 与锁定提交不同，建议同步报告版本，避免其历史自检记录被误认为本候选证据。
accepted_scope: boot/bootloaderth 定向差异；Docker 中的 236KB 打包边界、MiniMCProto v2.0 最小升级子集宿主机状态机正负例及恢复检查、S04
  函数规模与中文注释门禁。交叉编译及实体 HIL 明确排除在本轮沙箱接受范围外。
unexecuted: []
actual_session: 01a1aecb-f61a-76f3-b694-d99bc58b92a2
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=45c5cdf791ae3d88b76949525ec1b46d25832083;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1; boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba;
  boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
server_qa:
  task_id: TWIN-62
  task_revision: 4
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 21ec62ba03b9
    id: TWIN-62_run_105845_20261106_025845
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845
    developer_mounts: []
    container_inspect:
      id: 21ec62ba03b92728644b3385fc98c3a42b9e77586fd2863aaf258e496df475dc
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T02:59:20.946938626Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-62_gpjmkzav/evidence/server_lock.json
    sha256: 0f0212651157734b6eb760363a5a20ca7af3abb23bc305e89e3736458dc9eb1f
  checkout_log:
    path: /tmp/qa_TWIN-62_gpjmkzav/evidence/checkout.log
    sha256: f9d384c486c3a86ff81ff964b6220ad0ee8f0ed0bf7b1593331b8d253a4e0c0b
  runtime_log:
    path: /tmp/qa_TWIN-62_gpjmkzav/evidence/runtime.log
    sha256: b0641ab5117b8124fbbfdc1fc99d5deacb911f9101500406919dcee822e685f0
  server_verdict:
    path: /tmp/qa_TWIN-62_gpjmkzav/evidence/server_verdict.json
    sha256: 2cbd4d13f2cdedaada1b20ed6fbe831d4a8aa690a44c569ef313f2e1ce2122e3
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
      rm -f /tmp/test_th_boot_ota && sed -n "85,122p" tests/run_tests.sh | sh && python3
      -c "import pathlib, re, sys; files = [\"inc/iap.h\", \"inc/flash.h\", \"inc/usart.h\",
      \"src/iap.c\", \"src/flash.c\", \"src/main.c\", \"src/usart.c\", \"tools/pack_firmware.py\",
      \"tests/test_th_boot_ota.c\"]; cjk = re.compile(r\"[\\u4e00-\\u9fff]\"); [ (txt
      := pathlib.Path(p).read_text(encoding=\"utf-8\"), assert_cjk := sum(1 for l
      in txt.splitlines() if cjk.search(l)) >= 3, print(f\"[DOC-CHECK PASS] {p}: cjk_lines={sum(1
      for l in txt.splitlines() if cjk.search(l))}\"), (sys.exit(1) if not assert_cjk
      else None)) for p in files ]; print(\"[PASS] S04 & code_documentation_standard
      check passed!\")"'
    exit_code: '0'
    subpath: boot/bootloaderth
    duration: 0.33s
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
      \ MiniMCProto v2.0 tests passed!\n[PASS] S04 all C functions in boot/bootloaderth\
      \ satisfy <=50 lines and <=4 parameters!\n[DOC-CHECK PASS] inc/iap.h: cjk_lines=49\n\
      [DOC-CHECK PASS] inc/flash.h: cjk_lines=26\n[DOC-CHECK PASS] inc/usart.h: cjk_lines=22\n\
      [DOC-CHECK PASS] src/iap.c: cjk_lines=38\n[DOC-CHECK PASS] src/flash.c: cjk_lines=32\n\
      [DOC-CHECK PASS] src/main.c: cjk_lines=13\n[DOC-CHECK PASS] src/usart.c: cjk_lines=27\n\
      [DOC-CHECK PASS] tools/pack_firmware.py: cjk_lines=16\n[DOC-CHECK PASS] tests/test_th_boot_ota.c:\
      \ cjk_lines=32\n[PASS] S04 & code_documentation_standard check passed!"
  passed: true
  timestamp: '2026-11-06T02:59:24.042435+00:00'
  path: /tmp/qa_TWIN-62_gpjmkzav/evidence/server_qa.json
  sha256: c9133736a331317aee0b7f2bb1b19e54818127e241ad0508f18474dc7249ef41
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-62_gpjmkzav/reviews/1041be7061ac4cb9b487144b43078102/codex.jsonl
  sha256: acaaa0dbe0ebe3643c2871d423be75275b3cf0b63b75c3a264b0d3d8f5355600
reviewed_artifacts:
- path: /tmp/qa_TWIN-62_gpjmkzav/request.json
  sha256: 949a21e4fa8a3b03a87d64a8eecab0993ce942c69b932e4e97644a1106929f9b
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-62_gpjmkzav/diffs/boot/bootloaderth.patch
  sha256: 8b9f524e4afa0107858d2a28cf134591bf0c7fe4f045ffca7d6681ecf4fee88d
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/inc/iap.h
  sha256: 6ad97d450397bc0e46ca1111cdc16e28953e57e7b5a500510b1e2c44697ec4f6
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/src/iap.c
  sha256: d09851da381d74371fe6e61e6a158f5132bcb7d970158113ce07f8d8d26c196d
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/src/flash.c
  sha256: fee2c0b41d57a3a581b774fd2ce26240fa9e83d0445d7b4137e2a2e3138ece1e
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/src/main.c
  sha256: fe5b74d458afc8afdb75aeb596a3cd36af019f0f43d8d80832b8e2b37f40c7fe
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/tools/pack_firmware.py
  sha256: 8bdbffd30baf2aa7fabfe0802a218ad41c3d9605a93d8124ca84b4833bd5fe65
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/tests/run_tests.sh
  sha256: f8c3e24e547a5e5efcc336e2341470cdcfdcc2a40279e232b9ea95aec7a8f4f0
- path: /tmp/qa_sandboxes/TWIN-62_run_105845_20261106_025845/boot/bootloaderth/tests/test_th_boot_ota.c
  sha256: 5e258a77f0ac4eb4801992fe9865081d48cbd3d2f500ad27b00cfe67ba5c8acf
verification_scope: boot/bootloaderth 定向差异；Docker 中的 236KB 打包边界、MiniMCProto v2.0 最小升级子集宿主机状态机正负例及恢复检查、S04
  函数规模与中文注释门禁。交叉编译及实体 HIL 明确排除在本轮沙箱接受范围外。
verification_environment: docker-sandbox-and-independent-codex-audit
```

锁定候选符合本轮接受条款。已核对冻结证据与源码哈希，并审阅定向差异、范围内正负例和恢复行为；runner 记录的范围内检查通过。
