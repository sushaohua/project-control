# TWIN-62 Author Self-Check Result (`author_01`)

- **Task ID**: `TWIN-62`
- **Role**: `ENG_BOOT_TH` (`eng-vertical`)
- **Repository & Branch**: `boot/bootloaderth` (`soc_debug`)
- **Base Commit**: `769fccbe52464ad7ceb856c5e89cb0d25abbbf87`
- **Candidate Commit**: `9b40f8fb7c4bb6008126e94653f615039bad4d64`

## 1. Read Sources Registered (`read_sources`)
- `boot/bootloaderth/.repo-rules/AGENTS.md`
- `boot/bootloaderth/.repo-rules/SOURCE.json` (`commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)
- `boot/bootloaderth/AGENTS.md`
- `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`revision: 2`, `sha256: b30cf87bcda5b7f7e49fd34d0df5bd2a29d21631ffbd7171331a49e13d1757c6`)
- `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` (`Rev 2.0.4`, `sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)
- `project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md` (`revision: 1`, `sha256: c79477a0b9bfa2b18d1451b91b2a6188aa4b50f72bc742a8640aa0a696a1610b`)
- `project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md` (`revision: 2`, `sha256: f41d27c2214cacd1113397f20eb50038a404df94781f4bfdb18239d5d6f246d9`)
- `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` (`revision: 1`, `sha256: 87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9`)

## 2. Summary of Changes
1. **MiniMCProto v2.0 Minimal 7-Command Subset (`inc/iap.h`, `src/iap.c`, `src/main.c`)**:
   - Removed legacy `0x5A 0xA5` frame header, `CMD_TH_HELLO (0x10)` ~ `ACK_TH_FINISH (0x93)` macros, and 8-bit additive checksum.
   - Implemented `DST == 0x03` MiniMCProto v2.0 7-command state machine (`0x01/0x02` with `capability_flags=0xE0080423U` & dynamic `boot_id`, `0x03/0x04`, `0x1D`, `0x20 [144B]`, `0x21 [520B max]`, `0x23 [8B]`, `0x22 [8B]`, plus `0x00 CMD_ACK [4B]` / `0x06 CMD_NACK [3B]`).
   - Enforced pre-erase `144B` (`16B` header + `128B` ATSG Trailer) admission in `0x20 CMD_OTA_START` (`241,665B` oversize rejected with `NACK 0x14` and `0` Flash erase; wrong board/CRC rejected with `NACK 0x06` and `0` Flash erase).
   - Preserved Chunk 0 (`offset < 512`) SRAM caching (`ota_state = 2`, `cached_chunk0_bytes = 512`, `bytes_written = 0`) and two-phase commit in `0x22 CMD_OTA_FINISH` (Sector 127 Anchor `0x0803F800` written first, then Chunk 0 at `0x08004000`).
2. **Anchor Integrity Gate & 236KB Alignment (`inc/flash.h`, `src/flash.c`, `tools/pack_firmware.py`)**:
   - Fixed `bsp_flash_app_integrity_check()` / `flash_verify_app_integrity()` so missing Anchor at `0x0803F800` returns `false` and stays in Bootloader.
   - Aligned `MAX_PAYLOAD_SIZE = 236 * 1024` (`241,664B`) in `tools/pack_firmware.py` and `inc/iap.h`.
3. **16KB Flash / 48KB SRAM Budget (`S01/S02/S03/S04`)**:
   - `build/bootloaderth.bin` is **`9,360` bytes** (`57.13%` of `16,384B`, free margin `+7,024B`); `.data + .bss + ._user_heap_stack` ends at `0x20000F04`, well below `0x20008000` magic region.
   - Added `tests/test_th_boot_ota.c` and `tests/run_tests.sh`.

## 3. Verification Output
```text
text=9348, data=12, bss=3836, dec=13196, hex=338c (build/bootloaderth.elf)
bootloaderth.bin size: 9360 bytes (limit: 16384 bytes)
[PASS] S01 linker overflow gate rejected >16KB image with exit code 1
[PASS] S03 pack_firmware.py 236KB boundary checks (241663/241664/241665/245760) passed!
[PASS] test_th_boot_ota: all TH Bootloader MiniMCProto v2.0 tests passed!
[PASS] S04 all C functions in boot/bootloaderth satisfy <=50 lines and <=4 parameters!
```
