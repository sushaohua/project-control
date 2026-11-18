# SLICE-02 宿主机 ARM 固件交叉编译、分区预算与双版本包验证报告

- **切片 ID**：`SLICE-02`（`BATCH-OTA-ACCEPTANCE-01`，`DEC-USER-4=A`）
- **验证日期**：`2026-11-18`
- **原始日志物证**：
  - 宿主机 ARM 交叉编译、尺寸/溢出拦截与四仓测试全量原始输出：[host_arm_build_and_tests.log](host_arm_build_and_tests.log)（`sha256: 11daf08080acb635b3cc0ae96ef9118e95559fedc4d5c0307c51ebdddb670322`）
  - 双板全版本（`v1.0/v2.0/v2.1`）ATSG 打包与超限拦截原始输出：[dual_version_pack_verify.log](dual_version_pack_verify.log)（`sha256: 02ea406621c84b3350051f3c1f438aa73de04106b941bab81511ace520b9da42`）
- **受测目标仓锁定基线提交**：
  - `mcu-p3@feat/soc-debug`: `b865222c5e7ec50cbe7d7174b8aa25f93ed16ae0`
  - `boot/bootloadermc@soc_debug`: `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`
  - `boot/bootloaderth@soc_debug`: `1a0351363cf7b9cbc0aa6919b4afc6be61561152`
  - `test_harness@main`: `371a3a3de7e878d4035388ccab70ef4bc84f9046`

---

## 1. 四目标 ARM 交叉编译与宿主单测实测结果（摘自 `host_arm_build_and_tests.log`）

| 目标固件 | 执行命令 | 实测二进制大小与 SHA256 | 分区硬上限 | 门禁与单测结果 |
| :--- | :--- | :--- | :--- | :--- |
| **TH Bootloader** (`boot/bootloaderth`) | `(cd boot/bootloaderth && sh tests/run_tests.sh && make clean)` | `bootloaderth.bin`: **`9,360 B`**<br>`1dc0be2b7c25eea393c04e2490a9c67940bb0e84301f200fa5839adb34ed07ab` | `16,384 B` (`16 KB`) | **PASS**（含 `S01` >16KB 溢出拦截、`S03` 236KB 边界、`test_th_boot_ota`、`S04`） |
| **MC Bootloader** (`boot/bootloadermc`) | `(cd boot/bootloadermc && sh tests/run_tests.sh && make clean)` | `bootloader.bin`: **`37,600 B`**<br>`6da15b4140c9543d666ce537b3f020e9ead323a6e05ef6ba01a22a965316938b` | `131,072 B` (`128 KB`) | **PASS**（含零 `USART6` 符号/引用校验、`pack_firmware.py` 边界、`test_mc_boot_ota`、`S04`） |
| **TH App** (`mcu-p3/color-engine-mcu`) | `make clean all -j4` (`io_toggle/`) + `(cd tests && sh run_tests.sh)` | `fw_th.bin` 净荷: **`76,864 B`**<br>`a3512727423f7c9c5cd8310a43981f71fd92753809213084353f6483e2290128` | `241,664 B` (`236 KB`) | **PASS**（`test_twin45_th_debug` + `test_th_ota_and_bootid` + `236K` LD 零 `M997` + `S04`） |
| **MC App** (`mcu-p3/motion-controller-mcu`) | `cmake -B /tmp/build_mc_arm -G Ninja && cmake --build /tmp/build_mc_arm -j4` + `(cd tests && sh run_tests.sh)` | `Marlin_AT32.bin` 净荷: **`384,348 B`**<br>`4f10f3b1fdbd81b4d7a31a930672c5aeb317845ad1add8b5ab5ee1fa6676ad74` | `917,504 B` (`896 KB`) | **PASS**（FLASH `41.89%`、RAM `44,568 B`、`10` 组 `TWIN-44/47/60` + `test_mc_ota_and_relay` + `S04`） |

---

## 2. 双板全版本 ATSG 打包跨工具对齐实测（摘自 `dual_version_pack_verify.log`）

基于上述真实编译产物 `th_raw.bin` (`76,864 B`) 与 `mc_raw.bin` (`384,348 B`)，分别使用各仓打包脚本与 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 打出 `TH` 与 `MC` 各自的 `v1.0 / v2.0 / v2.1` 测试包并由 `parse_and_verify_atsg_package()` 解包核验：

| 打包产物 | 打包工具与版本参数 | 总字节数 | `fw_version` | 文件 SHA256 (前 16 位) | 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fw_th_v1_0.bin` | `boot/bootloaderth/tools/pack_firmware.py`（默认） | `76,992 B` | `0x01000000` (`v1.0.0.0`) | `e7aa1fe9bebf7ecf...` | **PASS** |
| `fw_th_v2_0.bin` | `mcu-p3/tools/pack_firmware.py -b th -v 0x02000100` | `76,992 B` | `0x02000100` (`v2.0.1.0`) | `4822f98f91452e05...` | **PASS** |
| `fw_th_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board TH --version 2.1` | `76,992 B` | `0x02010000` (`v2.1.0.0`) | `87ec2da010df5fe6...` | **PASS** |
| `fw_mc_v1_0.bin` | `boot/bootloadermc/scripts/pack_firmware.py -b 0x43500001`（默认） | `384,476 B` | `0x01000000` (`v1.0.0.0`) | `2aaef00be80b931e...` | **PASS** |
| `fw_mc_v2_0.bin` | `boot/bootloadermc/scripts/pack_firmware.py -b 0x43500001 -v 0x02000100` | `384,476 B` | `0x02000100` (`v2.0.1.0`) | `7b0562809e8b2b43...` | **PASS** |
| `fw_mc_v2_1.bin` | `hil_deploy_via_minimc_ota.py --board MC --version 2.1` | `384,476 B` | `0x02010000` (`v2.1.0.0`) | `81a27fc3039de502...` | **PASS** |

- **负例超限拦截**：`241,665 B` (>236KB) 输入 `boot/bootloaderth/tools/pack_firmware.py` 与 `917,505 B` (>896KB) 输入 `boot/bootloadermc/scripts/pack_firmware.py` 均返回 `rc=1` 拒绝打包。
- **工作树洁净度核验**：构建产物清理后，`printer-soc`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth`、`test_harness` `git status --short --untracked-files=all` 全部为空。
