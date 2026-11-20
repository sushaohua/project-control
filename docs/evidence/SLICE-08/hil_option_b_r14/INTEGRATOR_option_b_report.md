# SLICE-08 `r14` 实板部署与 Human Gate #2 (Option B) HIL 验证报告

- **执行角色**：`INTEGRATOR`（黑盒系统集成与真机 HIL 席位）
- **目标设备**：`root@192.168.1.101`（C308L/AW419，`eth0` MAC `02:ad:3d:01:8e:eb`）
- **候选制品**：
  - 安装包：[printer-soc-rootfs.tar.gz](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/run_20261120_135830_r14/docker_qa/artifacts/printer-soc-rootfs.tar.gz)（`19288672` B，SHA-256 `cb5f48b51eae5f30dd045c0400131d4244dfc987ae94e2d254d65dbcd665ea50`）
  - 候选清单：[release-manifest.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/run_20261120_135830_r14/docker_qa/artifacts/release-manifest.json)（SHA-256 `a2ec40a3cc740079cfd093224b3ee960de1a7fc8911db3b8f5eec8d6a434a851`）
- **源码改动**：0（严格遵守只写 `project-control/docs/evidence/SLICE-08/hil_option_b_r14/` 红线）

---

## 一、安全红线与不变式核查

| 红线约束 | 实测状态 | 佐证 |
| --- | --- | --- |
| 禁用 `probe-rs` / SWD / JTAG | 严格遵守（未使用） | 全程仅通过 SSH + D-Bus + sysfs |
| 严禁升温/运动指令 | 严格遵守（`heating_pwm_pct=0`，未发 `SetTemperature`/`MotionHome`/`MotionMove`） | [dbus_p0_and_ac04.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/dbus_p0_and_ac04.log) |
| `/data/boot_backup.img` 零改动 | 前/后/终态 SHA-256 完全一致 | `59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86` |
| `/etc/printer-soc/fw_signing_pub.pem` 零改动 | 前/后/终态 SHA-256 一致且为 `0o444` | `391ed9e5993fc86be51c0646693e9a92ad1fb7c2facd05b71f14df08ba75e2d3` |
| 禁止有效签名刷写（Option B） | `AC-03` 保持 `PENDING_BLOCKED`，仅测 `AC-04` 拒签 0 擦写负例 | [option_b_summary.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/option_b_summary.json) |

---

## 二、分步实测结论

### 1. 前置采集、存储硬件核对与批准清理（`PASS`）
- 日志：[pre_flight.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/pre_flight.log)
- **存储芯片与分区事实**（供核对 `board.yaml`）：
  - BusyBox `df` 不支持 `-B1`，已通过 `os.statvfs()` + `df -Pk` 采集；`ubinfo` 未预装，已通过 `/sys/class/ubi/` 与 `dmesg` 完整采集。
  - 芯片：`Macronix SPI NAND (spi0.0)`，总容量 `256 MiB`，block `128 KiB (131072 B)`，page `2048 B`，OOB `64 B`。
  - 8 个 MTD 分区：`mtd0: bl2 (2M)`、`mtd1: tpl (12M)`、`mtd2: logo (2M)`、`mtd3: misc (2M)`、`mtd4: recovery (16M)`、`mtd5: boot (16M)`、`mtd6: system (128M -> ubi0/ubi0_0 rootfs, 980 LEBs, 0 bad PEB)`、`mtd7: data (75M -> ubi1/ubi1_0 data, 556 LEBs, 0 bad PEB)`。
- **串口历史基线**：`/dev/ttyS1` 指向 `/sys/devices/platform/soc/fe000000.apb4/fe080000.serial`（`irq=37`），清理前（uptime `195437.99s`）`irq 37 = 247278`、`meson_uart tx=2315758 rx=214198`。
- **空间与清理**：
  - `/` 空闲（清理前）：`root_free_before_bytes = 61108224`（`avail = 61108224`）
  - `/data` 空闲：清理前 `data_free_before_bytes = 16465920`（`avail = 13189120`）→ 清理 `/data/apps/` 下 8 个已批准旧条目后 `data_free_after_bytes = 55664640`（`avail = 52391936`）。
  - 7 个保留项（`boot_backup.img`, `ev_watch.py`, `flash_erase`, `nandwrite`, `rollback_boot.sh`, `scripts`, `tp_reset.sh`）完好，`/data/boot_backup.img` 校验前后 SHA-256 均为 `59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86`。

### 2. `r14` 同源应用树安装与全量清单核对（`PASS`）
- 日志：[deploy_verify.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/deploy_verify.log)
- 上传至 `/tmp/printer-soc-rootfs.tar.gz` 核验字节（`19288672`）与 SHA-256 无误后，使用板端 Python 3.9 `tarfile` 剥离 `printer-soc-rootfs/` 前缀解压至 `/` 并删除 `/tmp/printer-soc-rootfs.tar.gz`。
- 读取板端 `/usr/share/printer-soc/manifest.json`（自身 SHA-256 `1a9d23241c3e564e09ae6c5aa23d4bc25b7fc7101a48d089be5b5130379b8046`）全量核对：`652/652` 普通文件（字节、SHA-256、八进制权限）+ `12/12` 符号链接（目标路径）总计 `664/664` 条目 **0 误差**。
- 关键权限：`/etc/printer-soc/fw_signing_pub.pem` (`0o444`)、`/etc/printer-soc/version.json` (`0o444`)、`/etc/init.d/S90printer-soc` (`0o755`)、`/usr/share/printer-soc/helixscreen/runtime -> /data/printer-soc/helix`。
- 部署后 `/` 剩余：`root_free_after_bytes = 35561472`（`34728 KiB`）。

### 3. 真冷重启零干预自启验证（`PARTIAL_WITH_DEFECT`）
- 日志：[cold_boot.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/cold_boot.log)
- `sync && reboot` 后，首次 SSH 可连 uptime 为 `23.43s`，再等待 `15s` 至 `58.79s` 只读采集（期间严禁手工 `start`）：
  - **已证实通过**：`rcS -> S90printer-soc` 成功自动拉起 `services.py _run`（848）、`dbus-daemon`（849）、`forward_service_daemon`（850，持有 `/dev/ttyS1` @ `921600` baud，`--allow-offline-start`）、`device_manager_daemon`（865）、`helix-screen`（905，持有 `/dev/fb0`）；确认无 `ui-gateway`、无 `--test`、无 mock；`/data/printer-soc/helix/.cache/helix/{gcode_mod,printer_images}` 实际创建。
  - **实板异常 #1**：`panel_restarts = 1`，首个 `helix-screen`（PID 875）在启动约 5.1s 后打印 `[RTPS_TRANSPORT_SHM Error] Failed init_port fastdds_port7400: Invalid argument` 与 `fastdds_port7411: Invalid argument` 后退出，由 `services.py` 重启为 PID 905。
  - **台架环境异常**：`/dev/ttyS1` 发包正常（`tx:1736`），但 `rx:0` 且 `irq 37: 0`，`forward.log` 持续超时（`error_code=-8`，`OFFLINE_DEGRADED`）。

### 4. D-Bus、安全功能与 `AC-04` 拒签负例、开发态切换（`PARTIAL` / 暴露缺陷）
- 日志：[dbus_p0_and_ac04.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/dbus_p0_and_ac04.log)、[panel_crash_diag.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/panel_crash_diag.log)
1. **`AC-02`（版本与状态）**：
   - AP `/etc/printer-soc/version.json` 读取 `git_sha == "962ce1a6"`；
   - `DeviceInterface.GetVersionInfo`、`RequestImmediateSample("all")`、`GetSnapshot`、`ForwardInterface.GetPortStatus` 均正常响应；`GetPortStatus` 返回 `true, "/dev/ttyS1", tx=234, rx=0`；
   - 因 `/dev/ttyS1` `rx=0`，`ForwardInterface.QueryVersion` 超时，`MC/TH` 状态均为 `OFFLINE`，无法核对 `MC/TH == 7b623d9a` 及 App 模式。
2. **`AC-05`（急停与解除）**：
   - `EmergencyStop byte:1` 返回 D-Bus `rc=0`、业务码 `int32 -8`（因 MCU 离线串口超时），但 DeviceManager 正确触发本地故障锁存，`GetSnapshot` 立即变为 `system_status="EMERGENCY_STOP_INVOKED", device_state="FAULT"`；
   - `EmergencyStop byte:0` 返回 D-Bus `rc=0`、业务码 **`int32 -9`（`AISOC_DEV_ERR_TIMEOUT`）**，DeviceManager 在 MCU 离线态拒绝解除急停锁，维持 `EMERGENCY_STOP_INVOKED / FAULT`。
3. **`AC-06`（背光与 eth0）**：
   - `eth0`：`192.168.1.101/24`，MAC `02:ad:3d:01:8e:eb`；
   - `/sys/class/backlight/aml-bl/brightness`：`204 -> 180`（`brightness=180, actual_brightness=180`）`-> 204` 复原校验通过。
4. **`AC-04` 拒签 0 擦写负例（`PASS_AP_PRECHECK`）**：
   - **`AC-04-UNSIGNED`**（全 0 签名 `fw_mc.bin`，`1421` B）：op=0 (`task_id=4000001`) 与 op=1 (`task_id=4000002`) 均在 `PRECHECK` 立即失败，`"error":"PACKAGE_SIGNATURE_INVALID"`，0 `[OTA_PACKET]`；
   - **`AC-04-BAD-SIGNATURE`**（临时错配 P-256 私钥签名 `fw_mc.bin`，`1421` B）：op=0 (`task_id=4000003`) 与 op=1 (`task_id=4000004`) 均在 `PRECHECK` 立即失败，`"error":"PACKAGE_SIGNATURE_INVALID"`，0 `[OTA_PACKET]`；
   - **`AC-04-WRONG-PACKAGE`**（`board_id=0x42300001` 当 `fw_mc.bin`，`1421` B）：op=0 (`task_id=4000005`) 与 op=1 (`task_id=4000006`) 均在 `PRECHECK` 立即失败，`"error":"PACKAGE_INVALID_OR_CHANGED"`，且该窗口期 `GetPortStatus tx_count`（`456 -> 456`）与 `meson_uart tx`（`6385 -> 6385`）增量为 **0**；
   - 测试后已删除 `/run/printer-soc/firmware/fw_*.bin`，`/etc/printer-soc/fw_signing_pub.pem` 未被修改。（因 MCU 离线，在线 `boot_id` 不变留待台架联机后复核）。
5. **`AC-09-DEV-MODE`（停服、互斥与恢复失败）**：
   - `/etc/init.d/S90printer-soc stop` 与 `/usr/bin/printer-soc dev-mode` 均返回 `0`，`ps` 与 `fuser /dev/ttyS1 /dev/fb0` 为空，`maintenance_inhibit == true`；
   - `/etc/init.d/S90printer-soc start` 正确被 `--respect-inhibit` 拦截（`rc=2`, `MAINTENANCE_INHIBIT_ACTIVE`）；
   - 随后执行显式 `/usr/bin/printer-soc start`（`rc=0`）清除锁并拉起 4 个进程，但 **`helix-screen`（PID 1111/1131/1161/1180/1181/1200）在每次启动约 4.2s 后连环崩溃**（出现 `helix-screen: tpp.c:82: __pthread_tpp_change_priority: Assertion ... failed.`、自身 120s 内 3 次重启熔断 `Crash loop detected`、以及 `exit_code=139` SIGSEGV），最终触发 `services.py` 的 **`PANEL_CRASH_LOOP:139`**，反序退出整个服务栈，当前板端停机在 `"phase": "stopped"`。

---

## 三、缺陷定责与环境阻塞分类（Root-Cause Triage）

1. **`[REJECTED / BLOCKER] HIL-DEF-01`（源码/运行期缺陷，Owner：`ENG-AP`）**
   - `helix-screen` 启动约 `4.2-5.1s` 后触发 FastDDS SHM `open_port_internal: Invalid argument`、`glibc tpp.c:82` 断言及 `SIGSEGV (139)`，暖重启 100% 触发 `PANEL_CRASH_LOOP:139` 导致整栈停机，且 `/dev/shm/fastdds_port7400` 等共享内存文件在异常退出后残留加剧复现。
2. **`[REJECTED / BLOCKER] HIL-DEF-02`（服务编排与集成缺陷，Owner：`ENG-AP`）**
   - [c308l_services.py](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/tools/c308l_services.py) 中 `launch_panel()` 未从 `services.json` 读取 `dds_domain` 注入 `AISOC_DDS_DOMAIN=198`，导致 [aisoc_connection.cpp](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/src/aisoc/aisoc_connection.cpp#L385-L392) 默认绑定 DDS Domain 0（`fastdds_port7400/7411`），与后台服务（Domain 198）失配。
3. **`[BLOCKED / ENVIRONMENT] HIL-BLK-01`（台架物理环境阻塞，Owner：现场台架操作）**
   - `/dev/ttyS1` 重启后 `tx=7785, rx=0, irq 37=0`（历史曾有 `rx=214198, irq 37=247278`），表明 MC/TH 下位机未上电或 `/dev/ttyS1` 物理接线未连通。
4. **`[REJECTED / MINOR] HIL-DEF-03`（配置告警，Owner：`ENG-AP`）**
   - `panel.log` 每次启动均告警 `HELIX_DATA_DIR '/data/printer-soc/helix' has no ui_xml/ directory` 与 `Backup of config/helixscreen.env failed`。

---

## 四、待现场人工确认项与 Pending 边界

1. **待现场人工确认**：
   - LCD 屏幕画面、开机显示与背光调整（`204 -> 180 -> 204`）物理视觉变化；
   - GT911 触屏点击/滑动手感（当前因 `PANEL_CRASH_LOOP:139`，`helix-screen` 已停止，需待上述 BLOCKER 修复或现场重新拉起验证）；
   - 核查 MC/TH 控制板电源及 `/dev/ttyS1` 物理线束，恢复串口应答后补测 `MC/TH == 7b623d9a`、`AC-05` 在线解除、全/半断连拔插及 `AC-04` 在线 `boot_id` 不变复核。
2. **`PENDING / BLOCKED` 项**：
   - `AC-03`（有效签名真刷 OTA）维持 `PENDING_BLOCKED`（遵循 Option B 边界，且缺少发布签名私钥与同源签名 MC/TH 固件包）。

---

## 五、原始物证文件清单

- [pre_flight.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/pre_flight.log) (`23662` B, SHA-256 `2212f945195df51dbf7c1d06487fec7cbffcf96c50fb82e06dd3b9e30dc84a0e`)
- [deploy_verify.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/deploy_verify.log) (`5669` B, SHA-256 `01036dbd979c431612934922baa3d9e9e562f82a43e7cefd4ea65b8ef14f9601`)
- [cold_boot.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/cold_boot.log) (`48053` B, SHA-256 `3ac3009c67f0688eae7206478ede1a8673a4be7538535f4d80b2f51f54c5bc60`)
- [dbus_p0_and_ac04.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/dbus_p0_and_ac04.log) (`39772` B, SHA-256 `6a824bc11b30ec4c9c6b51ef62891dd03147f24be06407cd72ae10b7f314145c`)
- [panel_crash_diag.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/panel_crash_diag.log) (`16123` B, SHA-256 `a2785d63387acfdbbc957075d6929f600e15cff5eba2e4aa156afacd0b02ea97`)
- [option_b_summary.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/option_b_summary.json)
- [INTEGRATOR_option_b_report.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/INTEGRATOR_option_b_report.md)
