# SLICE-02 宿主机 ARM 固件交叉编译、分区预算与双版本包验证报告

- **切片 ID**：`SLICE-02`（`BATCH-OTA-ACCEPTANCE-01`，`DEC-USER-4=A`）
- **验证日期**：`2026-11-17`
- **基线提交**：
  - `mcu-p3@feat/soc-debug`: `b865222c5e7ec50cbe7d7174b8aa25f93ed16ae0`
  - `boot/bootloadermc@soc_debug`: `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`
  - `boot/bootloaderth@soc_debug`: `1a0351363cf7b9cbc0aa6919b4afc6be61561152`（含 `SLICE-01` `tools/pack_firmware.py` 对齐提交）
  - `test_harness@main`: `371a3a3de7e878d4035388ccab70ef4bc84f9046`

---

## 1. 四目标 ARM 交叉编译与宿主单测实测结果

| 目标固件 | 执行命令 | 实测二进制大小 | 分区硬上限 | 门禁与单测结果 |
| :--- | :--- | :--- | :--- | :--- |
| **TH Bootloader** (`boot/bootloaderth`) | `(cd boot/bootloaderth && sh tests/run_tests.sh)` | `bootloaderth.bin`: **`9,360 B`** | `16,384 B` (`16 KB`) | **PASS**（含 `S01` >16KB 溢出拦截、`S03` 236KB 边界、`test_th_boot_ota`、`S04`） |
| **MC Bootloader** (`boot/bootloadermc`) | `(cd boot/bootloadermc && sh tests/run_tests.sh)` | `bootloader.bin`: **`37,600 B`** | `131,072 B` (`128 KB`) | **PASS**（含零 `USART6` 符号/引用校验、`pack_firmware.py` 边界、`test_mc_boot_ota`、`S04`） |
| **TH App** (`mcu-p3/color-engine-mcu`) | `make clean all` (`io_toggle/`) + `(cd tests && sh run_tests.sh)` | `fw_th.bin` 净荷: **`76,864 B`** | `241,664 B` (`236 KB`) | **PASS**（`test_twin45_th_debug` + `test_th_ota_and_bootid` + `236K` LD 零 `M997` + `S04`） |
| **MC App** (`mcu-p3/motion-controller-mcu`) | `cmake -B /tmp/build_mc_arm -G Ninja && cmake --build /tmp/build_mc_arm` + `(cd tests && sh run_tests.sh)` | `Marlin_AT32.bin` 净荷: **`384,348 B`** | `917,504 B` (`896 KB`) | **PASS**（FLASH `41.89%`、RAM `44,568 B`、`10` 组 `TWIN-44/47/60` + `test_mc_ota_and_relay` + `S04`） |

---

## 2. 双版本 ATSG 打包跨工具对齐实测（`version_code = (major<<24)|(minor<<16)|(patch<<8)|build`）

基于上述真实编译产物 `th_raw.bin` (`76,864 B`) 与 `mc_raw.bin` (`384,348 B`)，分别使用各仓打包脚本与 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 打出不同版本测试包并由 `parse_and_verify_atsg_package()` 解包核验：

| 打包产物 | 打包工具与版本参数 | 总字节数 | `fw_version` | 净荷 SHA256 (前 16 位) | 文件 SHA256 (前 16 位) | 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `fw_th_v1_0.bin` | `boot/bootloaderth/tools/pack_firmware.py`（默认） | `76,992 B` | `0x01000000` (`v1.0.0.0`) | `323803db40cf991c...` | `0ba89cf14d0c5f13...` | **PASS** |
| `fw_th_v2_0.bin` | `mcu-p3/tools/pack_firmware.py -b th -v 0x02000100` | `76,992 B` | `0x02000100` (`v2.0.1.0`) | `323803db40cf991c...` | `361c8fd3e141615f...` | **PASS** |
| `fw_th_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board TH --version 2.1` | `76,992 B` | `0x02010000` (`v2.1.0.0`) | `323803db40cf991c...` | `3603d68d16e89bb2...` | **PASS** |
| `fw_mc_v2_0.bin` | `boot/bootloadermc/scripts/pack_firmware.py -b 0x43500001 -v 0x02000100` | `384,476 B` | `0x02000100` (`v2.0.1.0`) | `50e22008ec9d1232...` | `1f8c4e7d7aa6f821...` | **PASS** |
| `fw_mc_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board MC --version 2.1` | `384,476 B` | `0x02010000` (`v2.1.0.0`) | `50e22008ec9d1232...` | `367e08a0d3b218ae...` | **PASS** |

- **负例超限拦截**：`241,665 B` (>236KB) 输入 `boot/bootloaderth/tools/pack_firmware.py` 与 `917,505 B` (>896KB) 输入 `boot/bootloadermc/scripts/pack_firmware.py` 均返回非零退出码拒绝打包（`[PACK-PASS]`）。
- **工作树洁净度核验**：构建产物清理后，`printer-soc`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth`、`test_harness` `git status --short --untracked-files=all` 全部为空。
