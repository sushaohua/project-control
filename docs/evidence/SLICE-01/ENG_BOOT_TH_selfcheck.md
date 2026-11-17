# SLICE-01 ENG_BOOT_TH 自检与交付回执

## 1. 接单回执与权限基线

| 字段 | 值 |
| :--- | :--- |
| **角色身份 (`role`)** | `ENG_BOOT_TH` |
| **允许写入仓 (`repo`)** | `boot/bootloaderth` |
| **锁定分支 (`branch`)** | `soc_debug`（已核实未写入 `main`） |
| **起始基线 Commit** | `c56ae6fa36d8ca034f4efc8c66c1c46442433748` |
| **候选提交 (`candidate_commit`)** | `1a0351363cf7b9cbc0aa6919b4afc6be61561152`（仅本地原子提交，未执行 `git push`） |
| **消费规则基线 (`project-control`)** | `948fa87a20575a623e38d5cf67ced42f2c7b44c1` |
| **消费规则基线 (`agents`)** | `30ecc6586a861c1543a97804cfe0600bb4778efb` |
| **消费规则文件** | `boot/bootloaderth/AGENTS.md`、`project-control/.agents/rules/code_documentation_standard.md` (`v1.1`) |
| **获批 SSoT 方案** | `project-control/docs/planning/mc_th_upgrade_acceptance_implementationplan_20261117_174500.md` (`v1.1`, `Approved`) |
| **切片与契约指针** | `project-control/slices/SLICE-01.yaml` (`revision: 1`)、`project-control/contracts/minimc_v2_contract.yaml` (`MiniMCProto v2.0`, `revision: 2.0.4`) |

---

## 2. 修改摘要与 Diff Budget 自核

- **修改文件**：`boot/bootloaderth/tools/pack_firmware.py`（共 `1` 个文件，`+35 / -6` 行）
- **允许路径 (`allowed_paths`)**：`["tools/pack_firmware.py"]` — **完全符合**
- **Diff Budget**：`max_files: 1`（实际 `1`），`protected_globs: ["src/**", "inc/**", "ldscripts/**"]`，`max_protected_lines: 0`（受保护目录改动行数为 `0`）— **完全符合**
- **具体变更内容**：
  1. 将 `FW_VERSION_DEFAULT` 由 `0x00010000` 对齐为 `0x01000000`（对应 `v1.0.0.0`），与 `minimc_v2_contract.yaml` 的 `version_code_layout: "major[31:24], minor[23:16], patch[15:8], build[7:0]"`、`printer-soc` 及 `boot/bootloadermc/scripts/pack_firmware.py` 保持一致；保持 `TRAILER_STRUCT_VER = 0x00010000` 不变以对齐 `inc/iap.h`。
  2. 对照 `code_documentation_standard.md` 与 `fast_gate.py`，完善模块 docstring 及 `build_atsg_trailer`、`_write_packed_outputs`、`pack_firmware` 的中文 docstring（补充参数类型、位域说明与返回值语义）及关键校验/封包逻辑中文注释；全部 3 个函数入参均为 `3` 个（`<= 4`），函数体有效代码行数均 `<= 50` 行，文件内无 `[UNVERIFIED]` 标记。
- **旧常量假定排查**：已检索 `boot/bootloaderth/tests/run_tests.sh` 及 `boot/bootloaderth/tests/test_th_boot_ota.c`，均无依赖 `0x00010000` 作为默认 `FW_VERSION_DEFAULT` 的旧断言假设。

---

## 3. 提交后验证输出（均在 `1a0351363cf7b9cbc0aa6919b4afc6be61561152` 后实测）

### 3.1 `boot/bootloaderth/tests/run_tests.sh`（退出码 `0`）

执行命令：`(cd boot/bootloaderth && sh tests/run_tests.sh)`

```text
=== [1/4] Cross-compile TH Bootloader & check 16KB Flash / 48KB SRAM budget (S01/S02) ===
rm -rf build
mkdir -p build
[CC] src/main.c
[CC] src/at32a423_clock.c
[CC] src/at32a423_int.c
[CC] src/flash.c
[CC] src/usart.c
[CC] src/iap.c
[CC] src/tmr.c
[CC] AT32A423_Firmware_Library/libraries/cmsis/cm4/device_support/system_at32a423.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_crm.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_gpio.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_usart.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_flash.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_pwc.c
[CC] AT32A423_Firmware_Library/libraries/drivers/src/at32a423_misc.c
[AS] startup/startup_at32a423.s
[LD] build/bootloaderth.elf
--- Firmware Memory Size Report ---
   text	   data	    bss	    dec	    hex	filename
   9348	     12	   3836	  13196	   338c	build/bootloaderth.elf
bootloaderth.bin size: 9360 bytes (limit: 16384 bytes)
[PASS] S01 linker overflow gate rejected >16KB image with exit code 1
=== [2/4] Check tools/pack_firmware.py 236KB (241,664B) boundary gate (S03) ===
[PASS] S03 pack_firmware.py 236KB boundary checks (241663/241664/241665/245760) passed!
=== [3/4] Run host unit tests for TH Bootloader MiniMCProto v2.0 state machine ===
[PASS] test_th_boot_ota: all TH Bootloader MiniMCProto v2.0 tests passed!
=== [4/4] Verify C function length (<=50 lines) and parameter count (<=4) gate (S04) ===
[PASS] S04 all C functions in boot/bootloaderth satisfy <=50 lines and <=4 parameters!
```

随后执行 `make -C boot/bootloaderth clean` 清理 `build/` 目录，`git -C boot/bootloaderth status --short --untracked-files=all` 输出为空，工作树无未跟踪或构建产物残留。

### 3.2 `fast_gate.py` 与子任务边界检查（退出码 `0`）

执行命令：
`python3 project-control/tools/gates/fast_gate.py --workspace . --files boot/bootloaderth/tools/pack_firmware.py`

```text
FAST_GATE_RC=0
```

另通过 `fast_gate.check_subtask_boundary` 针对 `SLICE-01.yaml` `ENG_BOOT_TH` 子任务（分支 `soc_debug`、`allowed_paths`、`diff_budget` 及静态 AST/反造假扫描）核验通过：`SUBTASK_BOUNDARY_PASS: ENG_BOOT_TH`。

### 3.3 打包产物 128B ATSG Trailer 实测解包校验（退出码 `0`）

在临时目录使用 `boot/bootloaderth/tools/pack_firmware.py` 对 `1024B` 测试净荷打包生成 `firmwareth.bin` (`1152B`)，解包校验尾部 `128B` Trailer：

```text
==================================================
      AT32A423 Firmware Trailer Pack Report       
==================================================
 Input File     : /tmp/tmph7iq7r3i/raw.bin
 Output File    : /tmp/tmph7iq7r3i/firmwareth.bin
 U-Disk Alias   : /tmp/tmph7iq7r3i/fw_th.bin
 Payload Size   : 1024 Bytes (1.00 KB)
 Payload CRC32  : 0x77D1E66D
 Payload SHA256 : 9453541e728864551253584ec3038ece2d328264b0166fe1b9d004f0dd88015f
 Board ID       : 0x42300001 (TH)
 Magic Number   : 0x41545347 ('ATSG')
 Trailer CRC32  : 0x64B63AC0
 Final Size     : 1152 Bytes (Payload + 128B Trailer)
==================================================
[SUCCESS] 固件打包完成，128B 自描述 Trailer 校验一致！

POST_COMMIT_PACK_CHECK: fw_ver=0x01000000 major=1 minor=0 patch=0 build=0 size=1152B
```
