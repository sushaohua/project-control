# SLICE-03 物理 HIL 集成验证报告 (`C308L /dev/ttyS1 @ 921600`)

- **执行角色**：`INTEGRATOR`（严格零业务仓改动 `diff_budget: max_files=0`）
- **验证时间**：`2026-11-18T10:08:40+08:00`（目标板 C308L 无电池 RTC，系统日志时间戳为开机单调时钟 `1970-01-01 01:02:38.687 ~ 01:05:46.798`）
- **物理台架**：`root@192.168.1.101`（C308L `armv7l Linux 5.15.137`）`/dev/ttyS1 @ 921600 8N1`，直连真实 MC (`0x02`) 并级联真实 TH (`0x03`)
- **安全门禁**：全程 **未使用** `probe-rs` / OpenOCD / SWD / JTAG（`probe_rs_used: false`）；Option A 加热 PWM 全程锁死 `0%`（`heating_pwm_pct: 0`）
- **总体结论**：**FAILED (`passed: false`)** — `B1`、`B3_TH`、`B2_TH`、`B3_MC`、`B2_MC` 及双端新固件业务恢复均 **100% 实测通过**（双板均成功从 `0x97C1C242` 升级至 `mcu-p3@b865222c` `0xB865222C`，共 `902` 个 `512B` 分块 `0` 重传）；但真机黑盒穿刺在 **`B4_TH`** 与 **`B4_MC`** 暴露出 **2 项真实固件缺陷（`HIL-FINDING-01`、`HIL-FINDING-02`）**，按防伪真实性铁律如实记为未全绿。

---

## 1. 固件包身份与物证索引

| 制品 / 物证 | 尺寸 | 净荷 / 分块 | 期望版本 (`fw_version`) | 文件 SHA256 / 物证路径 |
| :--- | :--- | :--- | :--- | :--- |
| `fw_th_v2_0.bin` | `76,992 B` | `76,864 B` (`151` 块, `CRC32=0x67530BF9`) | `0x02000100` (`v2.0`) | `4822f98f91452e059211cb55fe725991edc068dd8661424fb53c65d22e1ccb47` |
| `fw_mc_v2_0.bin` | `384,476 B` | `384,348 B` (`751` 块, `CRC32=0xC7A65C3F`) | `0x02000100` (`v2.0`) | `7b0562809e8b2b4383971fe5507e4d0487fe1ff2202984996c7995bf0f677632` |
| 双向原始 Hex 日志 | `1,952` 行 | `965` TX / `960` 有效 RX / `5` 复位轮询超时 | — | [hil_raw_hex.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-03/hil_raw_hex.log) (`sha256: 571025ec6e6aba426211d1f87e78f8f4dece3f848c8ebf8ea59055ac5495b2db`) |
| 结构化部署回执 | — | — | — | [hil_deployment_receipt.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-03/hil_deployment_receipt.json) |

---

## 2. 升级前后双板身份与 `boot_id` 跃迁表

| 节点 | 阶段 | 运行模式 (`Bit31`) | `fw` | `commit` | `boot_id` | `capability_flags` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TH (`0x03`)** | `B1` 升级前 App | `App (0)` | `2.0` | `0x97C1C242` | `0xC441D04B` | `0x00000007` |
| **TH (`0x03`)** | `B3_TH` Bootloader | `Boot (1)` | `1.0` | `0x769FCCBE` | `0x60DA4806` | `0xE0080423` |
| **TH (`0x03`)** | `B3_TH` 软复位回原 App | `App (0)` | `2.0` | `0x97C1C242` | `0x4A74CC81` | `0x00000007` |
| **TH (`0x03`)** | `B4_TH` 进 Boot / 中途复位驻留 Boot | `Boot (1)` | `1.0` | `0x769FCCBE` | `0xBD4B3B68` ➔ `0x1B7CB519` | `0xE0080423` |
| **TH (`0x03`)** | `B2_TH` 升级后新 App（`B2_MC` 后复查） | `App (0)` | `2.0` | `0xB865222C` | `0xC7076DA8` | `0x00000007` |
| **MC (`0x02`)** | `B1` 升级前 App | `App (0)` | `2.0` | `0x97C1C242` | `0xE8A86172` | `0x00000003` |
| **MC (`0x02`)** | `B3_MC` Bootloader | `Boot (1)` | `1.0` | `0x4FC171EA` | `0xC1E6CD05` | `0xC0080435` |
| **MC (`0x02`)** | `B3_MC` 软复位回原 App | `App (0)` | `2.0` | `0x97C1C242` | `0x8B139E59` | `0x00000003` |
| **MC (`0x02`)** | `B4_MC` 进 Boot / 中途复位驻留 Boot | `Boot (1)` | `1.0` | `0x4FC171EA` | `0xC1E6CD05` ➔ **`0xC1E6CD05` (未刷新)** | `0xC0080435` |
| **MC (`0x02`)** | `B2_MC` 升级后新 App | `App (0)` | `2.0` | `0xB865222C` | `0x02789779` | `0x00000003` |

---

## 3. `B1 ~ B4` 逐项真机实测结果明细

| 用例段 | 结论 | 关键观测事实与原始帧证据摘要 |
| :--- | :--- | :--- |
| **`B1`（基线与禁探针）** | **PASS** | MC (`0xE8A86172`) 与 TH (`0xC441D04B`) 均返回 `fw=2.0`, `commit=0x97C1C242`, `Bit31=0`；`0x14->0x15` 测得 MC `target=0, duty=0%`（裸板无热敏电阻 `current=32767, adc=4092, sensor_status=1`）、TH `target=0, duty=0%`（`current=1222 / 122.2°C, adc=2048, sensor_status=0`）。 |
| **`B3_TH`（TH 零擦除拒错）** | **PASS** | `0x1D(2)` 进 TH Boot (`0x769FCCBE`, `0xE0080423`, `boot_id=0x60DA4806`)；错板 `0x20` (`board_id=0x43500001`) 回 `NACK 0x06` 且 `0x23` `bytes_written=0`；超限 `0x20` (`241,665 B`) 回 `NACK 0x14` 且 `0x23` `bytes_written=0`；`0x1D(1)` 等 `1.5s` 后 `0x01` 确认原 TH App (`0x97C1C242`, `Bit31=0`, `boot_id=0x4A74CC81`) 完好。 |
| **`B4_TH`（TH 取消拒收与断链驻留）** | **FAIL (`HIL-FINDING-01`)** | 合法 `0x20` + Chunk 0 (`512B`) 后 `0x23` 报告 `ota_state=2, cached_chunk0_bytes=512, bytes_written=0`；随后在活跃代理期内立即发 `0x24` (`seq=18`)，**MC App (`src=0x02`) 直接拦截并返回 `0x06 NACK (err=0x05 DEVICE_BUSY)`**（见下节根因）；对比诊断待 MC `5s` 代理超时后重发 `0x24` (`seq=19`) 才到达 TH Bootloader 并返回 `src=0x03 NACK (err=0x04)`；`4B 0x23` (`seq=20`) 返回 `src=0x03 NACK (err=0x06)`；`0x1D(1)` 中途复位后 TH 安全驻留 Bootloader (`Bit31=1`, `boot_id=0x1B7CB519` 刷新, `bytes_written=0`)。 |
| **`B2_TH`（TH 全量升级）** | **PASS** | 从驻留 TH Bootloader 完整发送 `0x20 -> 0x21 (151 块, 512B, 0 重传) -> 0x22` 刷入 `76,864 B` 净荷（耗时 ~8.7s），`0x22` 前 `0x23` 报告 `bytes_written=76352, cached_chunk0_bytes=512`；`0x22` 后 `0x01` 确认新 TH App (`Bit31=0`, `fw=2.0`, `commit=0xB865222C`, `boot_id=0xC7076DA8`)，`0x14->0x15` 正常 (`duty=0%`)。 |
| **`B3_MC`（MC 零擦除拒错）** | **PASS** | `0x1D(2)` 进 MC Boot (`0x4FC171EA`, `0xC0080435`, `boot_id=0xC1E6CD05`)；错板 `0x20` (`board_id=0x42300001`) 回 `NACK 0x06` 且 `0x23` `bytes_written=0`；超限 `0x20` (`917,505 B`) 回 `NACK 0x14` 且 `0x23` `bytes_written=0`；`0x1D(1)` 软复位经 Bootloader 探盘及 Marlin 启动（第 4 次轮询 ~5.57s）确认原 MC App (`0x97C1C242`, `Bit31=0`, `boot_id=0x8B139E59`) 完好。 |
| **`B4_MC`（MC 取消拒收与断链驻留）** | **FAIL (`HIL-FINDING-02`)** | 合法 `0x20`（擦 Sector 0）+ Chunk 0 (`512B`) 后 `0x23` 报告 `ota_state=2, cached_chunk0_bytes=512, bytes_written=512`；`0x24` 返回 `NACK 0x04`；`4B 0x23` 返回 `NACK 0x06`；`0x1D(1)` 中途复位后 MC 安全驻留 Bootloader (`Bit31=1`, `0x23 bytes_written=0`)，**但 `boot_id` 仍为 `0xC1E6CD05`，与复位前及 `B3_MC` 完全一致未刷新**（见下节根因）。 |
| **`B2_MC` & 双端业务恢复** | **PASS** | 从驻留 MC Bootloader 完整发送 `0x20 -> 0x21 (751 块, 512B, 0 重传) -> 0x22` 刷入 `384,348 B` 净荷（耗时 ~38.3s），`0x22` 前 `0x23` 报告 `bytes_written=384348, cached_chunk0_bytes=512`；`0x22` 后轮询确认 MC 新 App 上线 (`Bit31=0`, `fw=2.0`, `commit=0xB865222C`, `boot_id=0x02789779`)，级联 TH 保持在线 (`Bit31=0`, `fw=2.0`, `commit=0xB865222C`, `boot_id=0xC7076DA8`)，双端 `0x14->0x15` 遥测响应正常且加热 `0%`。 |

---

## 4. 真机 HIL 发现的真实固件缺陷根因分诊

### `HIL-FINDING-01`（`B4_TH`）：MC App 在 TH 升级代理态拦截 `0x24` 回 `NACK 0x05`
- **现象与原始帧**：`[B4_TH_ABORT_0x24]` 在 `B4_TH_CHUNK0`/`0x23` 之后立即下发 `TX 55aa010305240304120000000355`（`dst=0x03`, `cmd=0x24`），收到 `RX 55aa02010606040012000300051200aa68`（**`src=0x02 MC`**, `cmd=0x06 NACK`, `err=0x05 DEVICE_BUSY`），未按 `SLICE-03` B4 预期到达 TH Bootloader 返回 `NACK 0x04`。待 MC `MC_TH_PROXY_TIMEOUT_MS (5000ms)` 自动退出代理态后发 `0x24`（`seq=19`），TH Bootloader 确实返回 `src=0x03 NACK 0x04`（`55aa030106060304130003000413006f2f`）。
- **源码根因**：`mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:2487-2494,2596-2600` 的 `is_ota_or_maint_cmd()` 仅放行 `0x01, 0x03, 0x17, 0x1D` 及 `0x20..0x23`（`MINIMC_CMD_OTA_START..MINIMC_CMD_OTA_STATUS`），遗漏 `0x24`（`MINIMC_CMD_OTA_ABORT`），导致 `s_th_proxy_active=true` 期间 MC App 在转发前拦截并回 `MINIMC_ERR_DEVICE_BUSY (0x05)`。`mcu-p3@b865222c` 中亦存在同样逻辑。

### `HIL-FINDING-02`（`B4_MC`）：MC Bootloader 跨软复位 `boot_id` 未刷新
- **现象与原始帧**：MC Bootloader (`commit=0x4FC171EA`) 在 `B3_MC`（`seq=182`）、`B4_MC` 复位前（`seq=193`）与 `B4_MC` `0x1D(1)` 软复位后（`seq=200`）三次返回完全相同的 `boot_id=0xC1E6CD05`（`55aa020106020400c80010000200010005cde6c1...`）。
- **源码根因**：`boot/bootloadermc/bootloader/src/boot_uart_ota.c:52,206-223` 中 `s_boot_salt` 为 `.bss` 静态变量（每次 `NVIC_SystemReset()` 后被清零再加一次固定 `0x9E3779B9UL`），`uid0..uid2` 为芯片固定 UID，而 `CRM->ctrlsts` 的 `SWRESETF` 位在连续软复位间未被清除且保持相同值，且未混入 `.noinit` 递增种子或 SysTick/ADC 熵源，导致连续 Bootloader→Bootloader 软复位无法区分新旧 Boot 会话。

---

## 5. `[UNVERIFIED]` 未连接物理外设与待补测边界声明

以下硬件与入口在当前台架物理不存在或未接入，严格诚实标注为 **`[UNVERIFIED]`**（未执行、未伪造）：
1. **`[UNVERIFIED] B5_UDISK_MANUAL_PLUG_HW_G1`**：C308L `/dev/ttyS1` 现场无物理 FAT32 U 盘插拔与人工供电开关条件，MC U 盘升级（`0:/fw_mc.bin -> FW_MC.CUR / .err`）、防重刷及 U 盘/串口单写者物理互斥未在真机实测。
2. **`[UNVERIFIED] COM12_COM13_DEBUG_UART`**：原 VMware (`192.168.77.134`) 离线，本台架未接出 MC USART1 (`[MC-DBG]`) 与 TH USART3 (`[TH-DBG]`) 独立调试串口，板端文本日志未采集。
3. **`[UNVERIFIED] PRINTER_SOC_REST_ON_C308L`**：本次使用 C308L 上的 `hil_deploy_via_minimc_ota.py` 编解码与 termios 直驱 `/dev/ttyS1` 完成黑盒 MCU/Bootloader OTA 穿刺；`printer-soc` 守护进程集群（REST / D-Bus / `forward_ota` / DDS）当前未在 `192.168.1.101` 运行，C308L 实板 REST 入口尚未部署实测。
