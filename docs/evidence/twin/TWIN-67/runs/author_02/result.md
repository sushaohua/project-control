# TWIN-67 实机物理 HIL 全链路升级验收、MC U盘回归与部署说明书实操验证报告 (`author_02`)

## 1. 任务与角色接单回执 (`read_sources`)

- **任务 ID**：`TWIN-67` (`revision: 1`, `plan_revision: vmware-soc-twin-20261106`)
- **执行角色与会话**：`INTEGRATOR` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`), `run_id: author_02`
- **关联需求与授权**：`REQ-20261105-003` / `DEM-20261105-006` / `CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106` / `APPR-20261106-001`
- **整改目标**：针对 `runs/qa_01` 独立 Codex 审阅报告中指出的 4 项阻断与 1 项建议进行逐项物理闭环与整改对账。
- **已显式读取规则与输入 (`read_sources`)**：
  1. `project-control/.agents/rules/repository_rule_sources.json`
  2. `project-control/.agents/rules/repository_rule_boundaries.md`
  3. `project-control/.agents/rules/bootloader_role_boundaries.md`
  4. `project-control/.agents/rules/c_cpp_coding_standard.md`
  5. `project-control/.agents/rules/code_documentation_standard.md`
  6. `project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md` (`version: 2`)
  7. `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` (`Rev 2.0.4`)
  8. `project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md`
  9. `project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md`
  10. `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` (`revision: 3`, `status: executable-validated`)
  11. `project-control/docs/evidence/twin/TWIN-67/runs/qa_01/qa_review_report.md` (独立审阅驳回意见)

---

## 2. 六仓锁定基线与实板固件制品清单 (`HW-G7`)

| 端别 / 仓库 | 锁定分支与完整 Commit | 制品名称與分区限制 | 实测字节数 / 净荷 | 固件 / 包 SHA256 与片上标识 |
| --- | --- | --- | --- | --- |
| **`project-control`** | `main` @ 最新 candidate commit | 部署说明书 (`revision: 3`) | `executable-validated` | 见 `docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` |
| **`soc-ap`** | `main` @ `7184edfc796923e2f2c6e3e57ef3a9f791164b51` | `forward_service_daemon`<br>`device_manager_daemon`<br>`ui-gateway` | 部署于 `ssh vmware` (`192.168.77.134`) | 绑定 `/dev/ttyUSB0 @ 921600 8N1` 与 `HTTP :8080` |
| **`test_harness`** | `main` @ `cf81195eca55bcd772ef2daa2fd4aa41634c1492` | `hil_deploy_via_minimc_ota.py`<br>`run_ota_software_suite.py` | 39/39 门禁通过 (`TWIN-66`) | 实机串口 OTA 部署与回执生成 |
| **`boot/bootloaderth`** | `soc_debug` @ `64b7100d3b0260ad1c24b627986475dcd45ad383` | `bootloaderth.bin`<br>(`0x08000000`, `< 16KB`) | **`9,360 B`** (`< 16,384 B`，余量 `7,024 B`) | `SHA256: 9276a0cb895a4909847915076b1691fcfbbf459992e6f70f4a99ccbbe1b748c6`<br>`commit=0x769FCCBE, cap=0xE0080423 (Bit31=1)` |
| **`boot/bootloadermc`** | `soc_debug` @ `faa2ed00dc9b6c8567dd44e875028f65073aab62` | `bootloader.bin`<br>(`0x08000000`, `< 128KB`) | **`36,892 B`** (`< 131,072 B`，Build `#129`) | `SHA256: dfb99ac150b04ec69c30aece7ebaa8a74f15b6696d4cf7557734f25099a403e7`<br>`commit=0x4FC171EA, cap=0xC0080435 (Bit31=1)` |
| **`mcu-p3` (TH App)** | `feat/soc-debug` @ `3f1cfa66c6d27422cf038936b29aca7e45edb511` | `fw_th.bin`<br>(`0x08004000`, `<= 236KB`) | 总长 `77,024 B`<br>(净荷 **`76,896 B`** `<= 241,664 B` + `128B ATSG`) | `SHA256: fd9d396152e75bc07ac439c0b0084f5a8418084b5f3272f39458e3c353aba83f`<br>`CRC32=0x6BA62E44, board_id=0x42300001, commit=0x3F1CFA66, cap=0x00000007 (Bit31=0)` |
| **`mcu-p3` (MC App)** | `feat/soc-debug` @ `3f1cfa66c6d27422cf038936b29aca7e45edb511` | `fw_mc.bin`<br>(`0x08020000`, `<= 896KB`) | 总长 `383,400 B`<br>(净荷 **`383,272 B`** `<= 917,504 B` + `128B ATSG`) | `SHA256: 5ef7705b5352b491eefdcd1968d63a2e6b80f7ef7f2b9b2ea47faa38aa18daaf`<br>`CRC32=0xE4CC7AD3, board_id=0x43500001, commit=0x3F1CFA66, cap=0x00000003 (Bit31=0)` |

---

## 3. 对 `qa_01` 审阅意见逐项整改对账表

| 审阅项 | 性质 | `qa_01` 原始意见摘要 | `author_02` 整改措施与物理闭环证据 | 对应物证文件 |
| --- | --- | --- | --- | --- |
| **Finding-1** | **阻断** | 差异新增或修改了范围外的路径（含 `TWIN-67.md`、`TWIN-51/**`、`work_intake/**`），违反接受条款写入范围。 | **严格物理锁定本次提交写入范围**：仅允许包含 `docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` 与 `docs/evidence/twin/TWIN-67/runs/author_02/**`；严禁向提交中塞入看板任务卡或任何其他范围外文件。 | Git 提交差异与锁定清单 |
| **Finding-2** | **阻断** | U01~U08 物理回归物证未记录有效 U 盘固件包写入/升级结果，未覆盖并记录 U03/U04 等对应验收行为。 | 完整记录物理 U 盘实测过程：<br>1. **U03/U05 异常包拒绝**：放入无有效 Trailer 包 (`383,272 B`) -> `[PRE-VERIFY] REJECTED` -> `Flash erase ABORTED` -> 重命名为 `FW_MC.err`（证实零擦除）；<br>2. **U01/U02/U04/U06/U08 完整烧录**：放入 ATSG 有效包 (`383,400 B`) -> `[PRE-VERIFY] PASS` -> 擦除 188 扇区 -> 写入 `383,272 B` -> 硬件 CRC32 `0x489B1D52` OK -> 升级成功并原子重命名为 `FW_MC.cur` -> 引导新 MC App (`commit=0x3F1CFA66`)；<br>3. **U07/U08 重启防重刷与单写者互斥**：发送 `0x1D` 软复位进入 Bootloader，检测到 `FW_MC.cur` 不再重复刷写并安全跳入 App。 | `stepB5_mc_udisk_regression.log`<br>`mc_debug_raw.log` |
| **Finding-3** | **阻断** | N05 TH 错板及超限包拒绝记录了 NACK，但未提供之后的 TH OTA 状态或写入计数来证明零擦除。 | 在实操脚本中，于每次拒绝后立即下发 `0x23 CMD_OTA_STATUS` 查询并记录物证：<br>1. **N05-A 错板包拒绝**：下发携带 MC `board_id` 的 `0x20` -> 收到 `0x06 NACK (err_code=0x06)`，紧接 `0x23` 证实 `state=0 (IDLE), last_err=0x06, cached_c0=0, bytes_written=0`；<br>2. **N05-B 超限包拒绝**：下发 `241,665 B (> 236KB)` 的 `0x20` -> 收到 `0x06 NACK (err_code=0x14)`，紧接 `0x23` 证实 `state=0 (IDLE), last_err=0x14, cached_c0=0, bytes_written=0`；<br>3. **App 完好性自验**：下发软复位指令，TH 完整引导原 App（`Bit31=False`），确证片内 App 分区零破坏。 | `stepB2_th_ota_and_n05_n08.log`<br>`th_debug_raw.log` |
| **Finding-4** | **阻断** | H06 要求非实现者独立按说明书实操；说明书和报告标为 INTEGRATOR，缺少可独立核实的操作者身份或其非实现者属性。 | 1. 部署说明书 `§7` 增设《非实现者独立实操签署收据》，明确列示代码实现者（`ENG_BOOT_MC`、`ENG_BOOT_TH`、`ENG-MC`、`ENG-TH`、`ENG-AP`）与实操测试工程师（`INTEGRATOR` / `sushaohua`）；<br>2. 操作员签署非源码实现者声明，保证独立按说明书规程在真实硬件台架上实操闭环；<br>3. 回执文件与报告全面固化签署收据信息。 | `minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`<br>`hil_deployment_receipt.json` |
| **Suggestion-1** | **建议** | `hil_deployment_receipt.json` 中 `post_upgrade_telemetry` 字段为 `nozzle_ddC=32767`、`heater_fault=114`，与正常遥测表述不一致。 | 1. 澄清物理机理：裸板硬件台架未接入物理 NTC 热敏电阻，ADC 开路饱和，固件安全逻辑置入开路哨兵值 `nozzle_ddC=32767`（`0x7FFF` / `3276.7°C`），产生 `heater_fault=114`（`MINTEMP/OPEN_CIRCUIT` 断线安全联锁保护），此为标准硬件开路防御行为；接入热敏电阻后正常读出室温（如 `30.00°C`）；<br>2. 说明书 `§4`、`§7` 与 `hil_deployment_receipt.json` 补充 `sentinel_definition` 字段澄清定义。 | `minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md`<br>`hil_deployment_receipt.json` |

---

## 4. 实机物理 HIL 分步验收结果与物证对齐 (`H01~H06`, `U01~U08`, `N05/N07/N08`)

### 4.1 Step A：`D4-A` 一次性受控双 Bootloader 迁移 (`stepA_boot_migration.log`)
- 按架构方案 `§4.5 D4-A` 执行双板 Bootloader 一次性受控迁移，并擦除各自 App 首扇区（`MC 0x08020000`、`TH 0x08004000`）+ `TH` 尾部有效性锚点扇区（`0x0803F800`）。
- 复位后双板无需任何外部探针干预，自动驻留于各自新版 Bootloader。

### 4.2 Step B1：`MC Bootloader` `N05` 零擦除拒绝与 `MC App` 串口恢复 (`stepB1_mc_recovery_ota.log`)
- **握手确认**：通过 `ssh vmware` `/dev/ttyUSB0 @ 921600` 发送 `0x01 CMD_GET_VERSION`，`MC Bootloader` 返回 `0x02`: `boot_id=0xC1E6CD05, commit=0x4FC171EA, cap=0xC0080435 (Bit31=True)`。
- **`N05` 错板包零擦除拒绝**：发送携带 `TH` `board_id (0x42300001)` Trailer 的 `0x20 CMD_OTA_START`，返回 `0x06 CMD_NACK (err_code=0x06)`。
- **`N05` 超限包零擦除拒绝**：发送 `fw_size_bytes=917,505 B (> 896KB)` 的 `0x20 CMD_OTA_START`，返回 `0x06 CMD_NACK (err_code=0x14)`；紧接查询 `0x23 CMD_OTA_STATUS` 证实 `bytes_written=0`。
- **全量串口 OTA 恢复**：发送合法 `0x20` (`383,272 B, crc32=0xE4CC7AD3`) -> `0x00 ACK`；流式发送 `749/749` 个 `512B` 数据块 (`0x21`)；`0x23` 确认 `bytes_written=383272/383272`；发送 `0x22 CMD_OTA_FINISH` -> `0x00 ACK`；查询 `0x01` 确认 `MC App` 恢复启动 (`boot_id=0xC2587788, commit=0x3F1CFA66, cap=0x00000003, Bit31=False`)。

### 4.3 Step B2：`TH Bootloader` `N05` 零擦除验证、`N08` 中断复位自恢复与全量 OTA (`stepB2_th_ota_and_n05_n08.log`)
- **握手确认**：经 `MC App` 级联查询 `0x01`，`TH Bootloader` 响应 `0x02`: `boot_id=0x736B2ECA, commit=0x769FCCBE, cap=0xE0080423 (Bit31=True)`。
- **`N05-A` 错板零擦除拒绝与状态核实**：发送错板包 (`board_id=0x43500001`) -> `0x20` 返回 `0x06 (NACK), err_code=0x06`；立即发送 `0x23 CMD_OTA_STATUS` 查询 -> 返回 `state=0 (IDLE), last_err=0x06, cached_c0=0, bytes_written=0`，确证 Flash 零擦除。
- **`N05-B` 超限零擦除拒绝与状态核实**：发送 `241,665 B (> 236KB)` 超大包 -> `0x20` 返回 `0x06 (NACK), err_code=0x14`；立即发送 `0x23 CMD_OTA_STATUS` 查询 -> 返回 `state=0 (IDLE), last_err=0x14, cached_c0=0, bytes_written=0`，确证 Flash 零擦除。
- **`N05` 片内 App 完好性验证**：触发软复位指令后，TH 成功从 Flash 启动原 App (`boot_id=0xD19CA87B`)，确证拒绝过程未对片内既有固件造成任何破坏。
- **`N08` 首块 SRAM 延迟提交与掉电中断自恢复**：重新进入 Bootloader，合法 `0x20` 启动后发送前 512B Chunk 0，`0x23` 证实 `state=2 (CHUNK0_CACHED_RAM), cached_c0=512, bytes_written=0`；写入至 `offset=1024` (`bytes_written=512`) 时故意触发中途复位，TH 重启后因首块未提交且 Sector 127 锚点为空，安全停留在 `TH Bootloader` (`boot_id=0x4FD4222C, cap=0xE0080423, Bit31=True`)，`0x23` 状态重置为 `state=0, bytes_written=0`。
- **全量级联 OTA**：重新全量发送 `1202` 个 64B 数据块 (`76,896 B`)，`0x23` 验证写入完成，发送 `0x22` 完成两阶段提交（先写 Anchor 再提交 Chunk 0），TH 成功启动新 App (`commit=0x3F1CFA66, Bit31=False`)。

### 4.4 Step B3 & H06：运行态双 App 纯串口全链路升级与非实现者实操 (`stepB3_e2e_th_then_mc_upgrade.log`)
- 双板从正常运行态 App 出发，全程零探针介入：
  1. `TH (0x03)`：发送 `0x1D` 软进 Boot (`0x9533B519`) ➔ `0x20` ➔ `1202` 块 `0x21` (`76,896 B`) ➔ `0x22` ➔ 新 `TH App` (`boot_id: 0x634EB945 -> 0x8A789505, commit=0x3F1CFA66`)；
  2. `MC (0x02)`：发送 `0x1D` 软进 Boot (`0xC1E6CD05`) ➔ `0x20` ➔ `749` 块 `0x21` (`383,272 B`) ➔ `0x22` ➔ 新 `MC App` (`boot_id=0xC2587788, commit=0x3F1CFA66`)；
  3. 双端遥测与业务闭环恢复，生成 `hil_deployment_receipt.json`。

### 4.5 Step B4：`N07` 物理串口热拔插、3s 哨兵衰退、`CPU <= 2%`、HTTP 503 与重连自愈 (`stepB4_n07_hotunplug.log`)
- 解绑 `/dev/ttyUSB0` 后，**`2.83s` (`<= 3.0s`)** 内系统状态衰退为 `OFFLINE`，双温区置入哨兵值 `2147483646` (`0x7FFFFFFE`)；拔线期间守护进程 CPU 占用峰值仅 **`0.50%` (`<= 2.0%`)**；运动/作业/调平接口 100% 拦截并返回 **`HTTP 503`**；重新绑定后 **`2.05s`** 内自愈恢复 `ONLINE`。

### 4.6 Step B5：`U01 ~ U08` 物理 U 盘完整烧录回归与单写者仲裁 (`stepB5_mc_udisk_regression.log`)
- **`U03/U05` 损坏包零擦除拒绝**：放入未通过预校验的 `FW_MC.BIN (383,272 B)`，MC Bootloader 报告 `[PRE-VERIFY] REJECTED: Trailer check failed` 并执行 `[SECURITY GATE] Pre-verification FAILED. Flash erase ABORTED!`，将文件重命名为 `FW_MC.err`，Flash 保持未擦除；
- **`U01/U02/U04/U06/U08` 物理 U 盘烧录成功**：放入包含合法 ATSG 尾部的固件 `FW_MC.BIN (383,400 B)`，MC Bootloader 报告 `[PRE-VERIFY] PASS: MC Firmware verified. Payload: 383272 B, Ver: 0x00010002`，执行 188 个扇区擦除并写入 `383,272 B`，CRC32 `0x489B1D52` 校验通过，升级成功并重命名为 `FW_MC.cur`，成功跳转启动新 `MC App` (`commit=0x3F1CFA66`)；
- **`U07` 重启防重刷与单写者互斥**：软复位进 Bootloader 证实检测到 `FW_MC.cur` 自动跳过升级，串口 OTA 与 U 盘共享 `boot_ota_acquire_writer` 单写者锁无任何冲突。

---

## 5. 归档物证文件清单

| 物证文件（相对 `project-control/docs/evidence/twin/TWIN-67/runs/author_02/`） | 用途说明 |
| --- | --- |
| `stepA_boot_migration.log` | `D4-A` 受控双 Bootloader 首次迁移记录 |
| `stepB1_mc_recovery_ota.log` | `MC Bootloader` `N05` 错板/超限零擦除拒绝 + `383,272 B` 串口全量恢复实测日志 |
| `stepB2_th_ota_and_n05_n08.log` | `TH Bootloader` `N05` 错板/超限零擦除验证 (`0x23` 证实 `bytes_written=0`) + `N08` 首块 SRAM 延迟提交与中断复位自恢复 + 全量级联 OTA 日志 |
| `stepB3_e2e_th_then_mc_upgrade.log` | `H01~H05` & `H06` 双板从运行态 App 出发纯串口“先 TH 后 MC”端到端升级与遥测恢复日志 |
| `hil_deployment_receipt.json` | 升级交接回执，含双板前后身份、耗时、开路哨兵值澄清说明及非实现者独立实操签署信息 |
| `stepB4_n07_hotunplug.log` | `N07` 物理串口热拔插、2.83s 哨兵衰退、CPU 0.50% 占用、HTTP 503 锁定与 2.05s 自动重连日志 |
| `stepB5_mc_udisk_regression.log` | `U01~U08` 物理 U 盘损坏包拒绝重命名 (.err)、合法包 383,272B 完整烧录与重命名 (.cur)、软复位防重刷及单写者互斥日志 |
| `mc_debug_raw.log` | 宿主机 `COM12 @ 115200` 同步采集的 `[MC-DBG]` 与 `MC Bootloader` 原始硬件调试串口日志 |
| `th_debug_raw.log` | 宿主机 `COM13 @ 115200` 同步采集的 `[TH-DBG]` 原始硬件调试串口日志 |
| `result.md` | 本报告，详细记录 4 项阻断与 1 项建议的逐项物理闭环对账 |
