# SLICE-02 宿主机 ARM 固件交叉编译、分区预算与双版本包验证报告

- **切片 ID**：`SLICE-02`（`BATCH-OTA-ACCEPTANCE-01`，`DEC-USER-4=A`）
- **验证日期**：`2026-11-18`
- **原始日志物证**：
  - 宿主机 ARM 交叉编译、尺寸/溢出拦截与四仓测试全量原始输出：[host_arm_build_and_tests.log](host_arm_build_and_tests.log)（`sha256: 6e7ba81ea7cf7e7e48338c28b89df69a04c45988a4783a0eb5950bf817b04cff`）
  - 双版本 ATSG 打包跨工具一致与超限拦截原始输出：[dual_version_pack_verify.log](dual_version_pack_verify.log)（`sha256: b862466fda9f8cd63e140266a2e85c8ba73681e4dc946ab2aa412a60118f961e`）
- **基线提交**：
  - `mcu-p3@feat/soc-debug`: `b865222c5e7ec50cbe7d7174b8aa25f93ed16ae0`
  - `boot/bootloadermc@soc_debug`: `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`
  - `boot/bootloaderth@soc_debug`: `1a0351363cf7b9cbc0aa6919b4afc6be61561152`
  - `test_harness@main`: `371a3a3de7e878d4035388ccab70ef4bc84f9046`

---

## 1. 四目标 ARM 交叉编译与宿主单测实测结果（摘自 `host_arm_build_and_tests.log`）

| 目标固件 | 执行命令 | 实测二进制大小与 SHA256 | 分区硬上限 | 门禁与单测结果 |
| :--- | :--- | :--- | :--- | :--- |
| **TH Bootloader** (`boot/bootloaderth`) | `(cd boot/bootloaderth && sh tests/run_tests.sh && make clean)` | `bootloaderth.bin`: **`9,360 B`**<br>`d4a0ad563ba8f5e945040b5eaa6f522189f369b04413f0b6cd166266f577c5bc` | `16,384 B` (`16 KB`) | **PASS**（含 `S01` >16KB 溢出拦截、`S03` 236KB 边界、`test_th_boot_ota`、`S04`） |
| **MC Bootloader** (`boot/bootloadermc`) | `(cd boot/bootloadermc && sh tests/run_tests.sh && make clean)` | `bootloader.bin`: **`37,600 B`**<br>`eb45713fb055ac229d96cdaff0f9383a9499830a71b999f5b639ad86de08c84a` | `131,072 B` (`128 KB`) | **PASS**（含零 `USART6` 符号/引用校验、`pack_firmware.py` 边界、`test_mc_boot_ota`、`S04`） |
| **TH App** (`mcu-p3/color-engine-mcu`) | `make clean all -j4` (`io_toggle/`) + `(cd tests && sh run_tests.sh)` | `fw_th.bin` 净荷: **`76,864 B`**<br>`2e2ffb8efbaf9903d636cfa2d17bff197d031c01ffe111c9b9ee74976e070d54` | `241,664 B` (`236 KB`) | **PASS**（`test_twin45_th_debug` + `test_th_ota_and_bootid` + `236K` LD 零 `M997` + `S04`） |
| **MC App** (`mcu-p3/motion-controller-mcu`) | `cmake -B /tmp/build_mc_arm -G Ninja && cmake --build /tmp/build_mc_arm -j4` + `(cd tests && sh run_tests.sh)` | `Marlin_AT32.bin` 净荷: **`384,348 B`**<br>`1030ad7f92da3e4de389d42106b2d6c29c1e98a5299242c64193a190a0246fbc` | `917,504 B` (`896 KB`) | **PASS**（FLASH `41.89%`、RAM `44,568 B`、`10` 组 `TWIN-44/47/60` + `test_mc_ota_and_relay` + `S04`） |

---

## 2. 双版本 ATSG 打包跨工具对齐实测（摘自 `dual_version_pack_verify.log`）

基于上述真实编译产物 `th_raw.bin` (`76,864 B`) 与 `mc_raw.bin` (`384,348 B`)，分别使用各仓打包脚本与 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 打出不同版本测试包并由 `parse_and_verify_atsg_package()` 解包核验：

| 打包产物 | 打包工具与版本参数 | 总字节数 | `fw_version` | 文件 SHA256 (前 16 位) | 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fw_th_v1_0.bin` | `boot/bootloaderth/tools/pack_firmware.py`（默认） | `76,992 B` | `0x01000000` (`v1.0.0.0`) | `681d64a8d1c1e146...` | **PASS** |
| `fw_th_v2_0.bin` | `mcu-p3/tools/pack_firmware.py -b th -v 0x02000100` | `76,992 B` | `0x02000100` (`v2.0.1.0`) | `61224dab0bf5e281...` | **PASS** |
| `fw_th_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board TH --version 2.1` | `76,992 B` | `0x02010000` (`v2.1.0.0`) | `f5680cc004b900ad...` | **PASS** |
| `fw_mc_v2_0.bin` | `boot/bootloadermc/scripts/pack_firmware.py -b 0x43500001 -v 0x02000100` | `384,476 B` | `0x02000100` (`v2.0.1.0`) | `6faf62d97f83f512...` | **PASS** |
| `fw_mc_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board MC --version 2.1` | `384,476 B` | `0x02010000` (`v2.1.0.0`) | `a0f30562599786b1...` | **PASS** |

- **负例超限拦截**：`241,665 B` (>236KB) 输入 `boot/bootloaderth/tools/pack_firmware.py` 与 `917,505 B` (>896KB) 输入 `boot/bootloadermc/scripts/pack_firmware.py` 均返回 `rc=1` 拒绝打包。
- **工作树洁净度核验**：构建产物清理后，`printer-soc`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth`、`test_harness` `git status --short --untracked-files=all` 全部为空。
