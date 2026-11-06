# TWIN-67 实机物理 HIL 全链路升级验收、MC U盘回归与部署说明书实操验证报告 (`author_01`)

## 1. 任务与角色接单回执 (`read_sources`)

- **任务 ID**：`TWIN-67` (`revision: 1`, `plan_revision: vmware-soc-twin-20261106`)
- **执行角色与会话**：`INTEGRATOR` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`), `run_id: author_01`
- **关联需求与授权**：`REQ-20261105-003` / `DEM-20261105-006` / `CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106` / `APPR-20261106-001`
- **已显式读取规则与输入 (`read_sources`)**：
  1. `project-control/.agents/rules/repository_rule_sources.json`
  2. `project-control/.agents/rules/repository_rule_boundaries.md`
  3. `project-control/.agents/rules/bootloader_role_boundaries.md`
  4. `project-control/.agents/rules/c_cpp_coding_standard.md`
  5. `project-control/.agents/rules/code_documentation_standard.md`
  6. `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`version: 2`, `sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
  7. `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` (`Rev 2.0.4`, `sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)
  8. `project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md`
  9. `project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md`
  10. `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` (升级至 `revision: 2`, `status: executable-validated`)

---

## 2. 六仓锁定基线与实板交叉编译固件制品对账表 (`HW-G7`)

| 端别 / 仓库 | 锁定分支与完整 Commit | 制品名称與分区限制 | 实测字节数 / 净荷 | 固件 / 包 SHA256 与片上标识 |
| --- | --- | --- | --- | --- |
| **`project-control`** | `main` @ `5e8def0aed1a66e4583b5d3e5aed89b86f5a13db` | 部署说明书 (`revision: 2`) | `executable-validated` | 见 `docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` |
| **`soc-ap`** | `main` @ `7184edfc796923e2f2c6e3e57ef3a9f791164b51` | `forward_service_daemon`<br>`device_manager_daemon`<br>`ui-gateway` | 部署于 `ssh vmware` (`192.168.77.134`) | 绑定 `/dev/ttyUSB0 @ 921600 8N1` 与 `HTTP :8080` |
| **`test_harness`** | `main` @ `cf81195eca55bcd772ef2daa2fd4aa41634c1492` | `hil_deploy_via_minimc_ota.py`<br>`run_ota_software_suite.py` | 39/39 门禁通过 (`TWIN-66`) | 实机串口 OTA 部署与回执生成 |
| **`boot/bootloaderth`** | `soc_debug` @ `64b7100d3b0260ad1c24b627986475dcd45ad383` | `bootloaderth.bin`<br>(`0x08000000`, `< 16KB`) | **`9,360 B`** (`< 16,384 B`，余量 `7,024 B`) | `SHA256: 9276a0cb895a4909847915076b1691fcfbbf459992e6f70f4a99ccbbe1b748c6`<br>`commit=0x769FCCBE, cap=0xE0080423 (Bit31=1)` |
| **`boot/bootloadermc`** | `soc_debug` @ `faa2ed00dc9b6c8567dd44e875028f65073aab62` | `bootloader.bin`<br>(`0x08000000`, `< 128KB`) | **`36,892 B`** (`< 131,072 B`，Build `#129`) | `SHA256: dfb99ac150b04ec69c30aece7ebaa8a74f15b6696d4cf7557734f25099a403e7`<br>`commit=0x4FC171EA, cap=0xC0080435 (Bit31=1)` |
| **`mcu-p3` (TH App)** | `feat/soc-debug` @ `3f1cfa66c6d27422cf038936b29aca7e45edb511` | `fw_th.bin`<br>(`0x08004000`, `<= 236KB`) | 总长 `77,024 B`<br>(净荷 **`76,896 B`** `<= 241,664 B` + `128B ATSG`) | `SHA256: fd9d396152e75bc07ac439c0b0084f5a8418084b5f3272f39458e3c353aba83f`<br>`CRC32=0xAE3C4CF6, board_id=0x42300001, commit=0x3F1CFA66, cap=0x00000007 (Bit31=0)` |
| **`mcu-p3` (MC App)** | `feat/soc-debug` @ `3f1cfa66c6d27422cf038936b29aca7e45edb511` | `fw_mc.bin`<br>(`0x08020000`, `<= 896KB`) | 总长 `383,400 B`<br>(净荷 **`383,272 B`** `<= 917,504 B` + `128B ATSG`) | `SHA256: 5ef7705b5352b491eefdcd1968d63a2e6b80f7ef7f2b9b2ea47faa38aa18daaf`<br>`CRC32=0xE4CC7AD3, board_id=0x43500001, commit=0x3F1CFA66, cap=0x00000003 (Bit31=0)` |

---

## 3. 实机物理 HIL 分步验收结果与四方物证对齐 (`H01~H06`, `U01~U08`, `N05/N07/N08`)

### 3.1 Step A：`D4-A` 一次性受控双 Bootloader 迁移 (`stepA_boot_migration.log`)
- 按架构方案 `§4.5 D4-A` 执行双板 Bootloader 一次性受控迁移，并擦除各自 App 首扇区（`MC 0x08020000`、`TH 0x08004000`）+ `TH` 尾部有效性锚点扇区（`0x0803F800`）。
- 复位后双板无需任何外部探针干预，自动驻留于各自新版 Bootloader。

### 3.2 Step B1：`MC Bootloader` `N05` 擦除前零擦除拒绝与 `MC App` 串口全量恢复 (`stepB1_mc_recovery_ota.log`)
- **握手确认**：通过 `ssh vmware` `/dev/ttyUSB0 @ 921600` 发送 `0x01 CMD_GET_VERSION`，`MC Bootloader` 返回 `0x02`: `boot_id=0xC1E6CD05, commit=0x4FC171EA, cap=0xC0080435 (Bit31=True)` (`raw=55aa020106020400010010000200010005cde6c1ea71c14f350408c04d87`)。
- **`N05` 错板包零擦除拒绝**：发送携带 `TH` `board_id (0x42300001)` Trailer 的 `0x20 CMD_OTA_START`，`MC Bootloader` 立即返回 `0x06 CMD_NACK (err_code=0x06, seq=2)` (`raw=55aa02010606040002000300060200f205`)。
- **`N05` 超限包零擦除拒绝**：发送 `fw_size_bytes=917,505 B (> 896KB)` 的 `0x20 CMD_OTA_START`，`MC Bootloader` 立即返回 `0x06 CMD_NACK (err_code=0x14, seq=3)` (`raw=55aa02010606040003000300140300a1a3`)；紧接查询 `0x23 CMD_OTA_STATUS` 证实 `bytes_written=0`，Flash 零擦除。
- **全量串口 OTA 恢复**：发送合法 `0x20` (`383,272 B, crc32=0xE4CC7AD3`) -> `0x00 ACK`；流式发送 `749/749` 个 `512B` 数据块 (`0x21`) 耗时 `19.98s`；`0x23` 确认 `bytes_written=383272/383272`；发送 `0x22 CMD_OTA_FINISH` -> `0x00 ACK`；`2.5s` 后查询 `0x01` 确认 `MC App` 已启动 (`boot_id=0xC2587788, commit=0x3F1CFA66, cap=0x00000003, Bit31=False`)。

### 3.3 Step B2：`TH Bootloader` `N05` 擦除前拒绝、`N08` 首块 SRAM 延迟提交中断自恢复与级联 OTA (`stepB2_th_ota_and_n05_n08.log`)
- **级联握手确认**：经 `MC App` 透明级联路由 (`DST=0x03, hop=3, route=0x04`) 查询 `0x01`，`TH Bootloader` 返回 `0x02`: `boot_id=0x58C2C1B7, commit=0x769FCCBE, cap=0xE0080423 (Bit31=True)`。
- **`N05` 错板与 `241,665 B (> 236KB)` 超限零擦除拒绝**：
  - 发送 `MC` `board_id` 包至 `TH Bootloader` -> 返回 `0x06 NACK (err_code=0x06, seq=3)` (`raw=55aa030106060304030003000603000775`)；
  - 发送 `241,665 B (> 241,664 B / 236KB)` 包至 `TH Bootloader` -> 返回 `0x06 NACK (err_code=0x14, seq=4)` (`raw=55aa03010606030404000300140400d7d8`)。
- **`N08` 首块 512B SRAM 延迟提交与中途复位自恢复**：
  - 发送合法 `0x20` (`76,896 B, crc32=0xAE3C4CF6`) -> `0x00 ACK`；
  - 发送前 `512 B` (`offset 0..512`) 后查询 `0x23 CMD_OTA_STATUS`，返回 `state=2 (CHUNK0_CACHED_RAM), cached_c0=512, bytes_written=0` (`raw=55aa0301062303040f000800020000020000000032b9`)，证明首块仅缓存于 SRAM、Flash `0x08004000` 尚未写入；
  - 继续写入至 `offset=1024` (`state=3, cached_c0=512, bytes_written=512`) 后，**不发送任何 `0x1D` 驻留指令，直接对 `TH` 施加硬件复位模拟中途掉电中断**；
  - 等待 `1.5s`（超过 Boot 启动探测窗口）后直接查询 `0x01`，`TH` 因首块未提交且 `0x0803F800` 无有效锚点，自动拒绝跳转残缺镜像并安全驻留 `TH Bootloader`（`boot_id` 刷新为 `0x36FA3B68`, `cap=0xE0080423, Bit31=True`），`0x23` 重置为 `state=0 (IDLE), bytes_written=0`；
  - 随后重新发起 `0x20` + `1202` 块 `0x21` (`76,896 B`) + `0x22`，`TH` 成功跳转进入 `TH App` (`boot_id=0x634EB945, commit=0x3F1CFA66, cap=0x00000007, Bit31=False`)。

### 3.4 Step B3 & H06：运行态双 App 纯串口“先 TH 后 MC”全链路升级与非实现者实操验证 (`stepB3_e2e_th_then_mc_upgrade.log`, `hil_deployment_receipt.json`)
- **全程零调试探针介入**，从双板正常运行态 App (`MC boot_id=0xC2587788`, `TH boot_id=0x634EB945`) 出发：
  1. **`H01/H02/H03` 先升级 `TH (0x03)`**：发送 `0x1D (JumpToBootloader)` 软进入 `TH Bootloader` (`boot_id=0x9533B519, cap=0xE0080423, Bit31=True`) ➔ `0x20` ➔ `1202/1202` 块 `0x21` (`76,896 B`) ➔ `0x22` ➔ 新 `TH App` 启动并验证通过 (`boot_id: 0x634EB945 -> 0x8A789505, commit=0x3F1CFA66, cap=0x00000007, Bit31=False`, 耗时 `201.01s`)。
  2. **`H04` 再升级 `MC (0x02)`**：确认 `TH` 新 App 生效后，向 `MC` 发送 `0x1D (JumpToBootloader)` 软进入 `MC Bootloader` (`boot_id=0xC1E6CD05, commit=0x4FC171EA, cap=0xC0080435, Bit31=True`) ➔ `0x20` ➔ `749/749` 块 `0x21` (`383,272 B`) ➔ `0x22` ➔ 新 `MC App` 启动并验证通过 (`boot_id=0xC2587788, commit=0x3F1CFA66, cap=0x00000003, Bit31=False`)。
  3. **`H05` 双端业务恢复与回执生成**：复核 `TH` `0x01 -> 0x02` (`boot_id=0x8A789505`) 与 `MC` `0x14 -> 0x15` 遥测闭环正常，生成 `hil_deployment_receipt.json`。

### 3.5 Step B4：`N07` 物理串口热拔插、3 秒内哨兵衰退、`CPU <= 2%`、HTTP 503 门禁与自动重连自愈 (`stepB4_n07_hotunplug.log`)
- 在 `ssh vmware` 上拉起锁定版 `soc-ap@7184edfc` 三大守护进程 (`device_manager_daemon`, `ui-gateway`, `forward_service_daemon --port /dev/ttyUSB0 --baud 921600`)：
  - **在线基线**：`forward_service_daemon` 完成 MC/TH 双节点 `0x01 -> 0x02` 握手 (`commit=0x3F1CFA66`)，`GET /api/v1/temperature/snapshot` 返回 `TH=ONLINE`, `tool_temp=121.2°C (FRESH)`，`GET /api/v1/ota/status` 返回 `stage=IDLE, is_maintenance=false`。
  - **物理拔线 (`unbind 1-2.1:1.0`)**：**`2.83s` (`<= 3.0s`)** 内系统状态衰退为 `OFFLINE`，`bed_millic` 与 `tool_millic` 均置为哨兵值 **`2147483646` (`0x7FFFFFFE`)**，`MC=OFFLINE, TH=OFFLINE`。
  - **CPU 占用门禁 (`<= 2.0%`)**：拔线期间连续 4 次采样守护进程 CPU 占用为 `[0.3%, 0.3%, 0.5%, 0.5%]`，峰值 **`0.50% <= 2.0%`**。
  - **HTTP 503 Fail-Closed 门禁**：拔线期间请求 `POST /api/v1/motion/jog`、`/api/v1/motion/home`、`/api/v1/jobs/start`、`/api/v1/leveling/trigger` 100% 拦截并返回 **`HTTP 503`** (`Hardware offline`)。
  - **物理重连 (`bind 1-2.1:1.0`)**：**`2.05s` (`<= 3.0s`)** 内自动重连恢复 `TH=ONLINE` 与实时温度 `122.3°C (FRESH)`。

### 3.6 Step B5：`U01 ~ U08` MC U盘物理回归与单写者仲裁验证 (`stepB5_mc_udisk_regression.log`, `mc_debug_raw.log`)
- 物理 U盘插在 `MC` 主板 USB Host 接口上，通过 `COM12` 实测确认：
  - **`U01/U02/U06`**：`MC Bootloader` 启动后执行 `Probing for U-disk / UART2 OTA (2.0s timeout window)... -> USB Device Attached. -> USB Device Enumeration Done. -> FAT32 File System initialized. -> Searching for upgrade package (fw_mc.bin)... -> No valid upgrade package (fw_mc.bin) found on U-disk.`，对盘内已重命名的 `FW_MC.CUR (367,924 Bytes)` 严格防重复擦写；
  - **`U05/U08`**：`MC Bootloader` 执行 `200ms` USB SE0 物理断连复位并跳转 `0x08020000` 后，`MC App` 重新完成 `[MC_APP] USB Device Attached. -> USB Device Enumeration Completed. -> USB Mass Storage Application Ready. -> [MC_APP][UPG] FatFs mounted successfully.`，列出根目录 `FW_MC.CUR` 并执行 `[MC_APP][UPG] Cannot find fw_th.bin or FW_TH.BIN` 扫描；
  - **`U07`**：在 U盘挂载在线状态下，串口 `0x1D` 与 `0x20 CMD_OTA_START` 通过 `boot_ota_acquire_writer(BOOT_WRITER_UART2)` 独占单写者锁，无任何双通道冲突。

---

## 4. 归档物证文件与 SHA256 清单

| 物证文件（相对 `project-control/docs/evidence/twin/TWIN-67/runs/author_01/`） | 用途说明 |
| --- | --- |
| `stepA_boot_migration.log` | `D4-A` 受控双 Bootloader (`bootloaderth.bin` 9,360B + `bootloader.bin` 36,892B) 首次迁移记录 |
| `stepB1_mc_recovery_ota.log` | `MC Bootloader` `N05` 错板/超限零擦除拒绝 + `383,272 B` 串口全量恢复实测日志 |
| `stepB2_th_ota_and_n05_n08.log` | `TH Bootloader` `N05` 错板/`241,665 B` 超限拒绝 + `N08` 首块 SRAM 延迟提交与中途复位自恢复 + `76,896 B` 级联升级日志 |
| `stepB3_e2e_th_then_mc_upgrade.log` | `H01~H05` & `H06` 双板从运行态 App 出发纯串口“先 TH 后 MC”端到端升级与遥测恢复日志（零探针介入） |
| `hil_deployment_receipt.json` | 升级前后双板 `boot_id`、`git_commit`、`capability_mask`、耗时与遥测快照结构化回执 |
| `stepB4_n07_hotunplug.log` | `N07` 物理串口热拔插、`2.83s` 哨兵衰退、`CPU 0.50% <= 2%`、HTTP 503 锁定与 `2.05s` 自动恢复日志 |
| `stepB5_mc_udisk_regression.log` | `U01~U08` `MC Bootloader` 与 `MC App` U盘枚举、FAT32 挂载、`FW_MC.CUR` 防重、SE0 交接与 `th_upgrade_mgr` 扫描日志 |
| `mc_debug_raw.log` | 宿主机 `COM12 @ 115200` 同步采集的 `[MC-DBG]` 与 `MC Bootloader` 原始硬件调试串口日志 |
| `th_debug_raw.log` | 宿主机 `COM13 @ 115200` 同步采集的 `[TH-DBG]` 原始硬件调试串口日志 |
