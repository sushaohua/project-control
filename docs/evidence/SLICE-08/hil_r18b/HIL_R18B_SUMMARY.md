# SLICE-08 (`r18b`) 真机 HIL 收口实测汇总报告

- **执行时间**: `2026-11-21 16:55 ~ 17:13 +0800`
- **目标台架**: `root@192.168.1.101` (`C308L-AW419` + `MC AT32F435` + `TH AT32F423`)
- **安全红线核验**: 全程 `probe_rs_used = false`、`heating_pwm_pct = 0`、零电机运动、`enable_gateway = false`、`/etc/printer-soc/fw_signing_pub.pem` 权限 `0o444`（非软链）、`/data/boot_backup.img` SHA-256 恒为 `59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86`。

## 1. 本轮 `r18b` 目标修复项真机实证结论（100% 闭环）

| 验证项 | 结果 | 原始物证文件 | 关键实测指标 |
| :--- | :---: | :--- | :--- |
| **同源包原子部署与清单校验** | **PASS** | `02_deploy_r18b.log`, `03_ac05_and_ac03_ota.log` | `printer-soc-rootfs.tar.gz` (`76e9348b...`, `git_sha=6f28023f`) 原子覆盖 `/`：`files_ok=652, symlinks_ok=12, total=664/664, errors=0`；`/` 余量 `34.9 MiB` (`68%`)，`/data` 余量 `51.1 MiB` (`13%`) |
| **`AC-03` 双板真实串口 OTA（消除 `HIL-DEF-06`）** | **PASS** | `04b_ac03_ota_th_mc_full.log`, `04c_ac03_forward_and_dm_logs.log` | 按**先 TH（`76,864 B`）后 MC（`384,540 B`）**顺序走完 Stage 1～4，Stage-4 自动跨越 MC `~2.0s` 启动窗直达 **`phase="SUCCEEDED", progress_pct=100, communication_error=0`**；`TH` `boot_id: 3292647499 -> 1462640722` (`0xA64BFFBF`)，`MC` `boot_id: 87314761 -> 1775181012` (`0xA64BFFBF`) |
| **`DM` 维护态自动退出（消除 `HIL-DEF-07`）** | **PASS** | `04_ac03_ota_th_mc.log`, `04b_ac03_ota_th_mc_full.log` | OTA 结束 `maintenance: true -> false` 边沿自动调用 `dev_state_exit_maintenance`，`GetSnapshot` 的 `device_state` 自动恢复为 `"IDLE"`（`generation_id=9`，零 `"UPGRADING_MAINTENANCE"` 残留） |
| **`AC-05-OTA-BUSY` 活跃期互斥** | **PASS** | `04b_ac03_ota_th_mc_full.log` | `FLASH_WRITING` 期间并发 `OtaCommand` 返回 `-5` (`BUSY`)，`EmergencyStop` 返回 `-5` (`BUSY`) |
| **`AC-09-COLD-BOOT` 冷重启零干预自愈（消除 `MCU-UART-01`）** | **PASS** | `05_ac09_cold_boot_recovery.log`, `05b_ac09_cold_boot_verified.log` | 仅对 AP 执行 `sync && reboot`（双 MCU 不断电、零手动按复位、零 `probe-rs`）：重启后 `S90printer-soc` 自动拉起 4 个守护进程与 `helix-screen`（绑定 `/dev/fb0` + Goodix `/dev/input/event0`，`rotate=270`），`/dev/ttyS1` **`tx=213, rx=213`（100% 零丢包）**，`MC` (`0xA64BFFBF`) 与 `TH` (`0xA64BFFBF`) 自动恢复 `"ONLINE"` |
| **`AC-09-DEV-MODE` 排他释放与恢复** | **PASS** | `06_raw_wire_version_and_estop_proof.log` | `printer-soc dev-mode` 后 `uart_owners=[]`, `fb_owners=[]`；`printer-soc start` 后自动恢复运行且双板 `ONLINE` |

## 2. 真机新暴露存量契约偏差（已生成独立交接单）

- **`TH-ESTOP-01`（`AC-05` TH 端 `0x17` 返回 `0B ACK`）**：
  - `MC` 对 `0x17 [0x01/0x00]` 正常执行急停/解除并返回标准 `4B CMD_ACK`；
  - `mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c:666-670` 对 `plen == 1U` 特判返回了 `0B CMD_ACK`（且 L661 未区分 `stop_mode == 0`），导致 `Forward`（要求固定 `4B ACK`）在 `TH` 阶段报 `-8` 超时；
  - 已生成独立交接单：`project-control/docs/planning/th_app_0x17_estop_ack_handoff_20261121_171500.md`。
