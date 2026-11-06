---
title: MiniMCProto v2.0 双 MCU 升级操作与 HIL 固件部署说明书
revision: 2
date: 2026-11-06
author: INTEGRATOR (07a1f6dc-f47c-45e5-bf00-37ec14e2dfda)
status: executable-validated
---

# MiniMCProto v2.0 双 MCU 升级操作与 HIL 固件部署说明书

| 修订 | 日期 | 修订人 | 内容 | 发布状态 |
| --- | --- | --- | --- | --- |
| 1 | 2026-11-05 | AI (Codex)，项目助理 | 固定操作目标、部署政策、步骤和交付验证要求 | 草案；尚未绑定实际升级工具，不可作为当前执行入口 |
| 2 | 2026-11-06 | INTEGRATOR (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`) | 绑定五端锁定基线制品、命令参数、退出码、串口拓扑、恢复 SOP 与 `TWIN-67` (`runs/author_01`) 非实现者实板实操证据 | `executable-validated`（已通过实机全链路验证，作为常规 App 部署唯一权威入口） |

本说明书对齐[统一升级主架构方案（revision 2）](../architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md)与[MiniMCProto v2.0 正式协议规范（Rev 2.0.4）](../specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md)，并已在 `TWIN-67`（`runs/author_01`）中由非实现者角色 `INTEGRATOR` 在物理 HIL 台架上独立完成端到端实操验证。

## 1. 适用范围与固定边界

- 通过 VMware 目标机（`ssh vmware` / `192.168.77.134`）指定目录中的 `ATSG` 签名封装固件包（`fw_th.bin`、`fw_mc.bin`），使用原生 `MiniMCProto v2.0 (Rev 2.0.4)` 协议（`0x1D`、`0x20`、`0x21`、`0x22`、`0x23`）升级真实 `TH` 与 `MC` 应用层固件；完整保留 `MC` 原有 U盘升级入口（`0:/fw_mc.bin` ➔ `FW_MC.CUR`）。
- 后续全部测试及 HIL 台架搭建中的常规 `MC/TH App` 部署，**100% 强制使用本说明书定义的串口升级或 U盘升级流程，严禁使用 `probe-rs`、`OpenOCD`、`ST-Link` 等 SWD/JTAG 调试探针直刷 App 分区**。
- `MC` 自身升级由 `MC Bootloader`（`0x08000000`）执行；`TH` 升级路径为 `AP (0x01) ➔ MC App (0x02 透明级联路由) ➔ TH Bootloader (0x03)`，`MC Bootloader` 绝不承担 `TH` 路由。
- 双板组合升级严格遵循**先 `TH (0x03)` 后 `MC (0x02)`** 顺序；仅当 `MC App` 损坏不可用时，先通过 `MC Bootloader` 串口或 U盘恢复 `MC App`，待 `MC App` 恢复级联路由后再升级 `TH`。
- 分区硬性门禁：`TH Bootloader` 固定 `< 16KB`（实测 `9,360 B < 16,384 B`）；`TH App` 有效净荷 `<= 236KB`（`241,664 B`，实测 `76,896 B`）；`MC Bootloader` 固定 `< 128KB`（实测 `36,892 B < 131,072 B`）；`MC App` 有效净荷 `<= 896KB`（`917,504 B`，实测 `383,272 B`）。
- 本说明书不开放运行期 Bootloader 自升级。双板首次 `D4-A` 受控双 Boot 迁移已记录于 `docs/evidence/twin/TWIN-67/runs/author_01/stepA_boot_migration.log`，后续常规迭代无需触碰 Boot 分区。

## 2. 已验证的实机运行参数、制品清单与拓扑绑定

| 项目 | 已验证的权威参数与绑定值 |
| --- | --- |
| **自动化部署 CLI 入口** | 工作目录：`test_harness`（或 VMware 目标机拷贝目录）<br>命令：`python3 hil/tools/hil_deploy_via_minimc_ota.py --port /dev/ttyUSB0 --baud 921600 --th-pkg <path/to/fw_th.bin> --mc-pkg <path/to/fw_mc.bin> --receipt-out <path/to/hil_deployment_receipt.json>`<br>超时预算：`TH` 全量升级约 `170s~205s`（`64B` 分块，共 `1202` 块），`MC` 全量升级约 `20s~265s`（`512B` 分块，共 `749` 块）；成功退出码为 `0`，任何校验或握手失败返回非零退出码并终止后续部署。 |
| **Web HMI / REST 入口** | 状态轮询：`GET http://127.0.0.1:8080/api/v1/ota/status`（返回 `stage`、`confirm_stage` (`0~4`)、`progress_pct`、`is_maintenance`）<br>升级触发：`POST http://127.0.0.1:8080/api/v1/ota/trigger`（维护期内常规运动/温控/作业接口返回 `HTTP 409/503` 锁定） |
| **文件投放位置与就绪规则** | VMware 目标机（`ssh vmware`）受控暂存目录：`/home/sushaohua/firmware_staging/`（或任务级隔离目录 `/tmp/twin67_hil/`），权限 `0755`。必须先以 `.part` 临时文件名写入并完成 `sha256sum` 校验后，再通过 `mv` 原子重命名为 `fw_th.bin` / `fw_mc.bin`，严禁边复制边触发升级。 |
| **发布包身份（五端锁定基线）** | - **`soc-ap@main`**: `7184edfc796923e2f2c6e3e57ef3a9f791164b51`<br>- **`mcu-p3@feat/soc-debug`**: `3f1cfa66c6d27422cf038936b29aca7e45edb511` (`git_commit_short = 0x3F1CFA66`)<br>- **`test_harness@main`**: `cf81195eca55bcd772ef2daa2fd4aa41634c1492`<br>- **`fw_th.bin`（TH App 升级包）**：总长 `77,024 B`（`76,896 B` 净荷 + `128 B` 尾部 `ATSG` Trailer），`board_id = 0x42300001`，`payload_crc32 = 0xAE3C4CF6`，文件 `SHA256 = fd9d396152e75bc07ac439c0b0084f5a8418084b5f3272f39458e3c353aba83f`<br>- **`fw_mc.bin`（MC App 升级包）**：总长 `383,400 B`（`383,272 B` 净荷 + `128 B` 尾部 `ATSG` Trailer），`board_id = 0x43500001`，`payload_crc32 = 0xE4CC7AD3`，文件 `SHA256 = 5ef7705b5352b491eefdcd1968d63a2e6b80f7ef7f2b9b2ea47faa38aa18daaf` |
| **已部署 Bootloader 身份** | - **`boot/bootloaderth@soc_debug`**: `64b7100d3b0260ad1c24b627986475dcd45ad383`，`bootloaderth.bin`（`9,360 B`，`SHA256 = 9276a0cb895a4909847915076b1691fcfbbf459992e6f70f4a99ccbbe1b748c6`），`0x02` 报告 `git_commit_short = 0x769FCCBE`，`capability_flags = 0xE0080423`（`Bit31=1` Boot 模式，`Bit30=1` ATSG 擦除前准入，`Bit29=1` 首块 512B SRAM 延迟提交，`Bit19=1` 64B 分块，`0x0423`）<br>- **`boot/bootloadermc@soc_debug`**: `faa2ed00dc9b6c8567dd44e875073aab62`，`bootloader.bin`（`36,892 B`，`SHA256 = dfb99ac150b04ec69c30aece7ebaa8a74f15b6696d4cf7557734f25099a403e7`，Build `#129`），`0x02` 报告 `git_commit_short = 0x4FC171EA`，`capability_flags = 0xC0080435`（`Bit31=1` Boot 模式，`Bit30=1` ATSG 擦除前准入，`Bit19=1` 512B 分块，`0x0435`） |
| **设备与物理连接拓扑** | - **VMware HIL 目标机（`ssh vmware` / `192.168.77.134`）**：挂载 USB-UART `/dev/ttyUSB0`（`ch341` `1-2.1:1.0`，`921600 8N1`），直连 `MC (AT32F435VGT7)` 的 `USART2 (PA2/PA3)`<br>- **MC ↔ TH 板间级联总线**：`MC USART6 (PC6/PC7)` ⇄ `TH (AT32F423CCT7) USART1 (PA9/PA10)`，工作于 `921600 8N1`<br>- **宿主机（`192.168.77.113` / Windows 侧）独立只读调试串口**：`COM12 @ 115200 8N1` 采集 `[MC-DBG]`（`MC USART1`），`COM13 @ 115200 8N1` 采集 `[TH-DBG]`（`TH USART2`） |
| **异常恢复入口** | 1. 传输中断/超时：重新发送 `540B` 全零字节流排空残帧后，查询 `0x01 CMD_GET_VERSION` 与 `0x23 CMD_OTA_STATUS`，重新发起 `0x20 CMD_OTA_START` 全量重传。<br>2. `TH` 中断掉电恢复：因 `TH Bootloader` 启用 `N08` 首块 512B SRAM 延迟提交与 `0x0803F800` 有效性锚点，掉电重启后 `TH` 自动驻留 `TH Bootloader`（`Bit31=1`），可直接通过 `AP ➔ MC App ➔ TH Boot` 重刷。<br>3. `MC` 软进入 Boot 或 U盘恢复：在 `MC` 复位后 `1.5s` 窗口内以 `40ms~50ms` 周期发送 `0x1D (action=2)` 捕获串口升级锁，或将 `fw_mc.bin` 放入 FAT32 U盘根目录（`0:/fw_mc.bin`）冷启动自动刷入并重命名为 `FW_MC.CUR`。 |
| **本轮实操证据归档路径** | `project-control/docs/evidence/twin/TWIN-67/runs/author_01/`（含 `result.md`、`hil_deployment_receipt.json`、`stepA_boot_migration.log`、`stepB1_mc_recovery_ota.log`、`stepB2_th_ota_and_n05_n08.log`、`stepB3_e2e_th_then_mc_upgrade.log`、`stepB4_n07_hotunplug.log`、`stepB5_mc_udisk_regression.log`、`mc_debug_raw.log`、`th_debug_raw.log`） |

## 3. 升级前准备（Pre-Flight Checklist）

1. **排他窗口与进程清理**：在 `ssh vmware` 上确认无残留进程争抢 `/dev/ttyUSB0`：
   ```bash
   ssh vmware "pkill -9 -f forward_service_daemon || true; fuser -v /dev/ttyUSB0 || true"
   ```
2. **发布包完整性核验**：在投放目录核对 `fw_th.bin` 与 `fw_mc.bin` 的字节长度、尾部 `128B ATSG Trailer` 及文件 `SHA256`：
   ```bash
   sha256sum fw_th.bin fw_mc.bin
   # 预期输出：
   # fd9d396152e75bc07ac439c0b0084f5a8418084b5f3272f39458e3c353aba83f  fw_th.bin
   # 5ef7705b5352b491eefdcd1968d63a2e6b80f7ef7f2b9b2ea47faa38aa18daaf  fw_mc.bin
   ```
3. **启动独立 Debug 串口监听**：在宿主机启动 `COM12`（`[MC-DBG]`）与 `COM13`（`[TH-DBG]`）只读日志采集（注意 WSL2 调用 Windows 进程必须附加 `timeout ... < /dev/null` 防止 stdin 阻塞）。
4. **安全联锁确认**：确认打印作业处于 `IDLE`、步进电机静止、加热器 PWM 锁死为 `0%`（目标温度 `0°C`）。

## 4. VMware 串口全链路升级标准步骤（先 TH 后 MC）

1. **步骤 1（H01 基线身份核验）**：
   通过 `/dev/ttyUSB0`（`921600 8N1`）向 `MC (0x02)` 与 `TH (0x03)` 发送 `0x01 CMD_GET_VERSION`，确认双板处于 App 模式（`capability_flags Bit31 == 0`），记录升级前 `boot_id` 与 `git_commit_short`。
2. **步骤 2（H02/H03 先升级 TH 节点 `0x03`）**：
   - 发送级联系统控制帧 `0x1D CMD_SYSTEM_CONTROL`（`DST=0x03, hop=3, route=0x04, action=2, delay_ms=20`）请求 `TH` 软复位进入 `TH Bootloader`，并在 `250ms` 后发送 `0x1D (delay_ms=0)` 驻留保持帧；
   - 发送 `0x01 CMD_GET_VERSION`（`DST=0x03`）确认 `TH` 返回 `0x02 CMD_VERSION_REPORT` 且 `capability_flags = 0xE0080423`（`Bit31=1`）；
   - 发送 `144B` 载荷的 `0x20 CMD_OTA_START`（`16B` 标准头 + `128B ATSG Trailer`），通过擦除前预验签门禁并收到 `0x00 CMD_ACK`；
   - 按 `64B` 块大小流式发送 `1202` 帧 `0x21 CMD_OTA_DATA`（总净荷 `76,896 B`），其中第 `0` 块（前 `512 B`）缓存在 `TH` 片内 SRAM（`0x23 CMD_OTA_STATUS` 报告 `state=2/3, cached_chunk0=512`），后续块直接写入 Flash 并回读校验；
   - 发送 `8B` 载荷的 `0x22 CMD_OTA_FINISH`（`fw_crc32=0xAE3C4CF6, action_after_verify=1`），触发 `TH Bootloader` 提交第 `0` 块、写入 `0x0803F800` 锚点、校验全镜像 CRC32 并回复 `0x00 CMD_ACK` 后跳转新 `TH App`；
   - 等待 `1.2s` 后发送 `0x01 CMD_GET_VERSION`（`DST=0x03`），确认 `TH` 已返回新 `TH App`（`Bit31=0`，`boot_id` 刷新为新值，`commit=0x3F1CFA66`）。
3. **步骤 3（H04 再升级 MC 节点 `0x02`）**：
   - 发送直连系统控制帧 `0x1D CMD_SYSTEM_CONTROL`（`DST=0x02, hop=4, route=0x01, action=2, delay_ms=20`）请求 `MC` 软复位进入 `MC Bootloader`，并在 `1.5s` 窗口内每 `50ms` 发送一次 `0x1D (delay_ms=0)` 抢占单写者串口锁；
   - 发送 `0x01 CMD_GET_VERSION`（`DST=0x02`）确认 `MC` 返回 `0x02 CMD_VERSION_REPORT` 且 `capability_flags = 0xC0080435`（`Bit31=1`）；
   - 发送 `144B` 载荷的 `0x20 CMD_OTA_START`（`fw_size_bytes=383272, fw_crc32=0xE4CC7AD3` + `128B ATSG Trailer`），收到 `0x00 CMD_ACK`；
   - 按 `512B` 块大小（在 VMware `ch341` 透传链路上按 `256B` 切片写入以规避 `512B` URB 边界阻塞）流式发送 `749` 帧 `0x21 CMD_OTA_DATA`（总净荷 `383,272 B`），每块均含 `CRC16-CCITT` 内层校验与 Flash 扇区按需擦写回读；
   - 发送 `8B` 载荷的 `0x22 CMD_OTA_FINISH`（`fw_crc32=0xE4CC7AD3, action_after_verify=1`），收到 `0x00 CMD_ACK` 后 `MC Bootloader` 执行 `200ms` USB SE0 物理断连复位并跳转新 `MC App`（`0x08020000`）；
   - 等待 `3.2s` 后发送 `0x01 CMD_GET_VERSION`（`DST=0x02`），确认 `MC` 已返回新 `MC App`（`Bit31=0, commit=0x3F1CFA66, cap=0x00000003`）。
4. **步骤 4（H05 双端业务恢复与回执归档）**：
   - 复核 `TH (0x03)` `0x01 -> 0x02` 与 `MC (0x02)` `0x14 -> 0x15` 温度遥测帧正常响应；
   - 生成结构化升级交接回执 `hil_deployment_receipt.json`，拉起 `soc-ap` 守护进程集群（`device_manager_daemon`、`ui-gateway`、`forward_service_daemon --port /dev/ttyUSB0 --baud 921600`）。

## 5. 保留的 MC U盘升级与恢复规范（`U01 ~ U08`）

1. **文件系统与命名规范**：使用标准 `FAT32`（MBR 分区表）U盘，将含 `128B ATSG Trailer` 的 `MC` 升级包命名为 `fw_mc.bin`（或兼容名 `firmwaremc.bin`）放入根目录 `0:/`。
2. **擦除前预验签门禁（`U02/U03`）**：`MC Bootloader` 挂载 `0:/` 后读取文件末尾 `128B`，严格校验 `magic == 0x41545347 ("ATSG")`、`struct_ver == 1`、`board_id == 0x43500001`、`payload_len <= 917,504 B` 及 `trailer_crc32`。若误放入 `fw_th.bin` 或损坏包，`MC Bootloader` 在擦除 Flash 前立即拒绝并将其重命名为 `.err`。
3. **有效净荷写入与防重复刷写（`U04/U05/U06`）**：校验通过后仅擦写 `0x08020000` 起的 `payload_len` 字节（绝不将末尾 `128B` Trailer 写入 Flash），完成硬件 CRC32 比对后将 `0:/fw_mc.bin` 原子重命名为 `0:/FW_MC.CUR`，卸载 FAT32、执行 `200ms` USB SE0 复位并跳转 `MC App`。后续重启见到 `FW_MC.CUR` 不再重复刷写。
4. **单写者互斥仲裁（`U07`）**：`boot_uart_ota.c` 与 `usbh_user.c` 共享 `boot_ota_acquire_writer()` 单写者锁；当串口 `0x20 CMD_OTA_START` 或 `0x1D` 驻留激活时，U盘通道自动礼让（`[BOOT] UART2 OTA active, deferring USB U-disk upgrade.`），严禁双通道交错擦写。

## 6. 非实现者实板验证记录（`TWIN-67` `runs/author_01`）

| 验收项 | 实测结果 | 关键物理证据摘要 | 证据文件 |
| --- | --- | --- | --- |
| **D4-A 首次双 Boot 受控迁移** | `PASS` | `TH Bootloader` (`9,360 B < 16KB`, `commit=0x769FCCBE`) 与 `MC Bootloader` (`36,892 B < 128KB`, `commit=0x4FC171EA`, Build `#129`) 一次性迁移成功，启动即驻留 Boot 模式响应 `0x01 -> 0x02`。 | `stepA_boot_migration.log` |
| **N05 擦除前预验签零擦除拒绝（MC & TH）** | `PASS` | 向 `MC Boot` 发送错板包 (`0x42300001`) 返回 `0x06 NACK (err=0x06)`、超限包 (`917,505 B`) 返回 `0x06 NACK (err=0x14)`；向 `TH Boot` 发送错板包 (`0x43500001`) 返回 `0x06 NACK (err=0x06)`、超限包 (`241,665 B > 236KB`) 返回 `0x06 NACK (err=0x14)`；`0x23 CMD_OTA_STATUS` 均证实 `bytes_written=0`。 | `stepB1_mc_recovery_ota.log`<br>`stepB2_th_ota_and_n05_n08.log` |
| **N08 TH 首块 512B SRAM 延迟提交与中断复位自恢复** | `PASS` | `TH Boot` 接收前 `512 B`（Chunk 0..7）后 `0x23` 报告 `state=2 (CHUNK0_CACHED_RAM), cached_c0=512, bytes_written=0`；写入至 `offset=1024`（`bytes_written=512`）时在中途不发 `0x1D` 直接触发硬件复位，`1.5s` 后 `TH` 因首块未提交且无 `0x0803F800` 锚点而安全驻留 `TH Boot`（`boot_id: 0x58C2C1B7 -> 0x36FA3B68, cap=0xE0080423, Bit31=1`），随后重传全量 `76,896 B` 成功恢复。 | `stepB2_th_ota_and_n05_n08.log` |
| **H01~H05 & H06 纯串口先 TH 后 MC 全链路升级（零探针介入）** | `PASS` | 双板从运行态 App 出发，全程零 SWD 探针介入：<br>1. `TH (0x03)`：`0x1D` 软入 Boot (`0x9533B519`) ➔ `0x20` ➔ `1202` 块 `0x21` (`76,896 B`) ➔ `0x22` ➔ 新 `TH App` (`boot_id: 0x634EB945 -> 0x8A789505, commit=0x3F1CFA66, cap=0x00000007`)；<br>2. `MC (0x02)`：`0x1D` 软入 Boot (`0xC1E6CD05`) ➔ `0x20` ➔ `749` 块 `0x21` (`383,272 B`) ➔ `0x22` ➔ 新 `MC App` (`boot_id=0xC2587788, commit=0x3F1CFA66, cap=0x00000003`)；<br>3. 升级后双端 `0x01/0x02` 与 `0x14/0x15` 遥测闭环正常，生成 `hil_deployment_receipt.json`。 | `stepB3_e2e_th_then_mc_upgrade.log`<br>`hil_deployment_receipt.json`<br>`mc_debug_raw.log`<br>`th_debug_raw.log` |
| **N07 物理拔线 3s 哨兵衰退、CPU<=2%、HTTP 503 与重连自愈** | `PASS` | 解绑 `/dev/ttyUSB0` (`1-2.1:1.0`) 后，`2.83s`（`<= 3.0s`）内系统状态衰退为 `OFFLINE`、双温区置入哨兵值 `2147483646 (0x7FFFFFFE)`；断连期间守护进程最大 CPU 占用仅 `0.50%`（`<= 2.0%`）；运动/归零/作业/调平接口全部返回 `HTTP 503`；重绑后 `2.05s` 内自动恢复 `ONLINE` 与实时温度 `122.3°C (FRESH)`。 | `stepB4_n07_hotunplug.log` |
| **U01~U08 MC U盘物理回归与单写者共存** | `PASS` | `COM12` 实测 `MC Bootloader` 完成 USB Host 枚举、FAT32 挂载、`FW_MC.CUR (367,924 B)` 防重复刷写识别、串口 OTA 期间 U盘单写者互斥礼让、`200ms` SE0 断连跳转，以及 `MC App` 启动后重新枚举 U盘并执行 `th_upgrade_mgr` 根目录扫描。 | `stepB5_mc_udisk_regression.log` |
