# 跨轮缺陷交接单：`bootloadermc` 只读 `0x01` 误锁 `stay_in_boot` 导致复位无法进 App

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| `v1.0` | `2026-11-21 14:58 +0800` | `AI (Antigravity-CLI) - COORD` | 基于 `SLICE-08` (`hil_r17b`) 真机实测抽离独立跨轮交接单（用户拍板选项 B：先闭环 `SLICE-08`，本项移交下一轮独立处理） | **待下一轮排期审批 (Deferred Handoff)** |

---

## 1. 缺陷标识与责任归属

- **缺陷代号**：`BOOT-MC-STAY-01`
- **唯一责任角色**：`ENG_BOOT_MC`（严禁 `ENG-MCU` 或 `COORD` 跨仓代改，遵循 `project-control/.agents/rules/bootloader_role_boundaries.md`）
- **目标仓库与强制分支红线**：`boot/bootloadermc/` ➔ **严格锁定 `soc_debug` 分支**（**绝对严禁向 `main` 分支提交开发内容**）
- **当前基线 Commit**：`3e01c00c`（现场板端运行标识 `git_commit = 0x4FC171EA`）
- **硬件探针归属（已于 2026-11-21 物理实读确认）**：
  - MC 主控板 (`AT32F435VGT7`, Bootloader 基址 `0x08000000`, 空间 `128 KB`)：
    `--probe "0483:3748:75003800120000334C41534E" --chip AT32F435VGT7`（`PID=0x70083344`, `Flash=1024KB`, `UID=05302390 4c96c000 0d819709`）
  - 证据原件：[09_probers_probe_id.log](../evidence/SLICE-08/hil_r17b/09_probers_probe_id.log)

---

## 2. 复现现象与业务危害

1. **真机必现条件**：当 C308L AP 侧正常开启生产服务（`forward_service_daemon` + `device_manager_daemon` 每 `500ms` 轮询发送只读 `0x01 QueryVersion`）时，一旦 MC 发生任何非升级复位（手动按物理 `RESET` 键、独立看门狗复位、电源瞬态跌落复位或收到 `0x1D(action=1)` 普通软复位），MC 进入 `bootloadermc` 的 `2.0s` 探测窗口。
2. **异常后果**：`bootloadermc` 在 `2.0s` 内必然收到 AP 发来的只读 `0x01` 帧并置位 `s_ota.stay_in_boot = 1U`，导致 `main.c:210` 的 `boot_uart_ota_should_stay_in_boot()` 恒返回 `1U`，2 秒超时自动跳转 App 的机制失效，**MC 被永久锁死在 Bootloader 模式，整机无法自愈恢复业务**。
3. **复现物证**：
   - AP 静默 (`dev-mode`) 时按 `RESET` 键：2 秒后正常跳入 `MC App (0xE5E45EEA)`（[08_manual_reset_to_mc_app_com12.log](../evidence/SLICE-08/hil_r17b/08_manual_reset_to_mc_app_com12.log)）；
   - AP 正常运行时按 `RESET` 键：永久停留在 `bootloadermc (0x4FC171EA)`。

---

## 3. 已物理核实的源码根因

- **精确代码位置**：`boot/bootloadermc/bootloader/src/boot_uart_ota.c` 第 `323–337` 行 `handle_cmd_get_version()`：
  ```c
  static void handle_cmd_get_version(const minimc_frame_hdr_t *p_req)
  {
    ...
    s_ota.stay_in_boot = 1U;  /* <-- 根因：只读版本查询误置驻留标志！ */
    ...
  }
  ```
- **设计本意冲突核对**：同文件第 `953` 行注释明确写明：
  `@brief 查询是否应驻留 Bootloader (收到 UPG2 魔数、0x1D 或 0x20 升级会话)`。
  只读身份探测 `0x01 (MINIMC_CMD_GET_VERSION)` 与 `0x03 (MINIMC_CMD_PING)` 绝不应改变驻留状态；仅以下 4 类条件才应驻留 Bootloader：
  1. SRAM `0x2005FFF0` 检测到 `UPG2` (`0x55504732`) 升级魔数（由 MC App 收到 `0x1D(action=2)` 写入后软复位）；
  2. Bootloader 运行期收到显式 `0x1D(action=2)`（请求驻留 Bootloader）或 `0x20 (CMD_OTA_START)` 升级握手；
  3. U 盘升级会话进行中（`g_upgrade_in_progress` / `g_udisk_connected`）；
  4. `0x08020000` 处不存在合法 App（`is_app_valid(FLASH_APP_ADDR) == 0`）。

---

## 4. 下一轮建议修复边界与验收标准（待下一轮启动时走两阶段审批）

1. **最小代码修改建议**（预计仅改 2 个文件，增删 $\le 30$ 行）：
   - `boot/bootloadermc/bootloader/src/boot_uart_ota.c`：移除 `handle_cmd_get_version()` 中的 `s_ota.stay_in_boot = 1U;`；同时核对 `handle_cmd_system_control()`（`0x1D`），仅当 `action == 2U`（进入/保持 Bootloader）时置 `s_ota.stay_in_boot = 1U`，`action == 1U`（重启回正常模式）不置驻留位。
   - `boot/bootloadermc/tests/test_mc_boot_ota.c`（或对应宿主机单测）：
     - **正例 1**：无 `UPG2` 魔数冷启动，连续注入多帧 `0x01 QueryVersion`，验证正常回复 `0x02`（带 `Bit31=1` Boot 标志）且 `boot_uart_ota_should_stay_in_boot() == 0U`，`2.0s` 到期正常调用 `jump_to_app(0x08020000)`；
     - **正例 2**：带 `UPG2` 魔数启动、或窗口内收到 `0x1D(action=2)` / `0x20`，验证 `boot_uart_ota_should_stay_in_boot() == 1U` 稳定驻留不跳转。
2. **门禁与高风险真机刷写红线**：
   - 先过宿主机单测、交叉编译与四阶软件门禁（独立 Codex 冷审 `0 BLOCKER`）；
   - **真机烧录 Bootloader (`0x08000000`) 必须单独向用户申请 Human Gate #2 物理 SWD 授权**，核对精确文件大小、SHA-256、探针序列号 `0483:3748:75003800120000334C41534E` 与 `--chip AT32F435VGT7` 后方可执行，并在 AP 持续轮询 `0x01` 的在线工况下实测按物理 `RESET` 键 2 秒后自动回到 `MC App` 且恢复 `ONLINE`。
