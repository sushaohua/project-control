# SLICE-09 `ENG_BOOT_MC` 自检报告（`S09-BOOT-MC` / `BOOT-MC-STAY-01`）

## 1. 角色身份、分支红线与提交元数据

- **执行角色**：`ENG_BOOT_MC`
- **目标业务仓**：`boot/bootloadermc`（远端：`ssh://git@192.168.77.79:2222/sushaohua/bootloadermc.git`）
- **锁定开发分支**：`soc_debug`（已物理核验 `refs/heads/main` 保持 `01bfda29b82f0576cb255d0b4196aeda1edb8d2e` 零触碰）
- **基线 Commit SHA**：`3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`
- **候选 Commit SHA（本地 `HEAD` 与远端 `origin/soc_debug` 对齐）**：`d2ef9fb6955eba5f7992b743642919e4e712af83`
- **依据方案与契约**：
  - 获批 SSoT 方案：`project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md`（v1.1，§2.1.2、§2.2.1、§2.2.3、§2.4.2 `S09-BOOT-MC`、§2.5.3）
  - 缺陷交接单：`project-control/docs/planning/bootloadermc_0x01_stay_in_boot_handoff_20261121_145800.md`
  - 切片规格：`project-control/slices/SLICE-09.yaml`
  - 协议契约：`project-control/contracts/minimc_v2_contract.yaml`（Rev `2.0.4`，零变更）
- **硬件与探针隔离声明**：本阶段严格遵守软件准出与人工闸门隔离约束，未触碰任何物理硬件，未调用 `probe-rs`（`probe_rs_used = false`）。

---

## 2. 沿用弊端评估、精确改动边界与数据流分解

### 2.1 原有逻辑弊端与影响范围
- **根因定位**：基线 `bootloader/src/boot_uart_ota.c` 的 `handle_cmd_get_version()` 在响应只读 `0x01 (MINIMC_CMD_GET_VERSION)` 时误执行 `s_ota.stay_in_boot = 1U;`。当 AP 守护进程按 `500ms` 周期常规轮询 `0x01` 时，MC 发生任何非升级复位进入 `2.0s` 探测窗口后，`boot_uart_ota_should_stay_in_boot()` 恒返回 `1U`，阻断 `main.c:218` 的 `handle_no_disk_timeout()` 自动跳回 `0x08020000` App。
- **单测漏检原因**：原 `tests/test_mc_boot_ota.c` 的 `test_magic_info_heartbeat_and_dst_filter()` 在无 `UPG2` 冷启动后发送 `0x01`/`0x03` 时未断言 `boot_uart_ota_should_stay_in_boot() == 0U`，且在 `0x1D(action=2)` 置位驻留后才测试 `0x1D(action=1)`，未能独立验证只读轮询与普通重启不置驻留位。

### 2.2 白名单与 Diff Budget 核验（`2 / 2` 文件）

| 序号 | 修改文件路径（相对 `boot/bootloadermc/`） | 白名单核对 | 行数变更 (`git diff --stat`) | 函数规模与入参核验 |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `bootloader/src/boot_uart_ota.c` | 允许 | `+4 / -1` | `handle_cmd_get_version`: 19 行，1 入参 |
| 2 | `tests/test_mc_boot_ota.c` | 允许 | `+119 / -10` | 全部函数 `<= 45` 行（上限 50 行），入参 `<= 4` 个 |

### 2.3 数据流向与状态变化步骤分解
1. **启动初始化（`boot_uart_ota_init`）**：清零静态上下文 `s_ota`（`stay_in_boot = 0U`）并释放单写者锁；仅当 SRAM `0x2005FFF0` 命中 `0x55504732 ("UPG2")` 魔数时清零魔数并置 `s_ota.stay_in_boot = 1U`。
2. **只读探测帧处理（`0x01` / `0x03`）**：
   - `handle_cmd_get_version()` 校验 `payload_len == 0U` 后组装 16B `minimc_payload_version_report_t`（`proto=2.0`、`fw=1.0`、`boot_id`、`MC_FW_GIT_COMMIT_SHORT=0x4FC171EA`、`MC_BOOT_CAPABILITY_FLAGS=0xC0080435`）通过 `USART2` 发送 `0x02` 响应帧，**不修改 `s_ota.stay_in_boot`**；
   - `handle_cmd_ping()` 回显 `echo_token` 与统计计数发送 `0x04` 响应帧，**不修改 `s_ota.stay_in_boot`**。
3. **显式驻留与复位控制（`0x1D` / `0x20`）**：
   - `0x1D(action=1)` 回复 `0x00 CMD_ACK` 并置 `pending_reboot = 1U`，不置 `stay_in_boot`；
   - `0x1D(action=2)` 回复 `0x00 CMD_ACK` 并显式置 `s_ota.stay_in_boot = 1U`；
   - `0x20 (CMD_OTA_START)` 通过单写者互斥、尺寸、板型 `0x43500001` 与 128B `ATSG` `trailer_crc32` 准入并预擦首扇区后，持有 `BOOT_WRITER_UART2` 且置 `s_ota.stay_in_boot = 1U`（准入失败则释放写锁且保持未驻留）。
4. **窗口超时跳转裁决（`main.c` 主循环）**：无升级锁且 `boot_uart_ota_should_stay_in_boot() == 0U` 时，累计满 `2000ms` 且无 U 盘连接即校验 `is_app_valid(0x08020000)` 并安全跳入 MC App。

---

## 3. 黄金回滚镜像与最终候选镜像摘要对照

| 镜像类别 | 对应 Commit SHA (`boot/bootloadermc`) | 归档/产物路径 | 精确字节数 | Flash 预算 (`131072 B`) | ELF 段分布 (`text / data / bss`) | SHA-256 摘要 |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **修改前黄金回滚镜像** | `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` | `project-control/docs/evidence/SLICE-09/candidate_mcu_artifacts/bootloader_3e01c00_rollback.bin` | `37600 B` | PASS (`28.69%`) | `37364 / 184 / 19272` | `1082c318fee4aecb175921290b773137970c7501b21ebd26abf32b887719d9df` |
| **最终候选镜像 (`HEAD`)** | `d2ef9fb6955eba5f7992b743642919e4e712af83` | `boot/bootloadermc/build/bootloader.bin` | `37596 B` | PASS (`28.68%`) | `37360 / 184 / 19272` | `e52289e6505db06b9b60b2b7ea8f2b39b1e58a9d94ce7742ea6c08afc529d3d4` |

---

## 4. 构建、宿主机单测与门禁验证记录

1. **`tests/run_tests.sh` 全套四步门禁**：
   - 命令：`(cd boot/bootloadermc && PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh tests/run_tests.sh)`
   - `[1/4]` ARM 交叉编译（`-Wall -Wextra -Werror`）：`PASS`（`bootloader.bin` = `37596 B <= 131072 B`，ELF 符号表与源码头文件零 `USART6` 引用）。
   - `[2/4]` `scripts/pack_firmware.py` MC(`896KB`) / TH(`236KB`) 正负边界校验：`PASS`。
   - `[3/4]` 宿主机单元测试 `test_mc_boot_ota`（`-Wall -Wextra -Werror -DHOST_UNIT_TEST`）：`PASS`，覆盖：
     - 无 `UPG2` 冷启动连续 4 轮（`500ms` 步进至 `2000ms`）轮询 `0x01` 与 `0x03`，正常回 `0x02 (16B)` / `0x04 (12B)` 且 `boot_uart_ota_should_stay_in_boot() == 0U`，`2.0s` 届满正常调用 `jump_to_app(0x08020000)`；
     - `0x1D(action=1)` 普通重启回 `0x00 CMD_ACK`、触发系统复位且 `boot_uart_ota_should_stay_in_boot() == 0U`；
     - `UPG2` 魔数、`0x1D(action=2)`、合法 `0x20 (CMD_OTA_START)` 三类显式驻留均令 `boot_uart_ota_should_stay_in_boot() == 1U`（且非法错板 `0x20` 拒绝不误锁驻留）；
     - 完整串口 OTA（`0x20 -> 0x21 -> 0x23 -> 0x22` 延迟回写首扇区与跳 App）、50ms 字节间超时恢复、外层 CRC16 NACK、USB Host U 盘升级与单写者并发互斥全量回归通过。
   - `[4/4]` C 函数总行数（`<= 50` 行）与参数个数（`<= 4` 个）静态门禁：`PASS`。
2. **`fast_gate.py` 机械门禁与子任务边界校验**：
   - 命令：`python3 -B project-control/tools/gates/fast_gate.py --workspace /home/sushaohua/workspace/ai_soc_project --files boot/bootloadermc/bootloader/src/boot_uart_ota.c boot/bootloadermc/tests/test_mc_boot_ota.c`
   - 结果：退出码 `0`（含 `SLICE-09.yaml` `ENG_BOOT_MC` `check_subtask_boundary` 分支/路径/预算校验全绿）。
3. **最终 `HEAD` 洁净构建核验**：
   - 推送 `d2ef9fb6955eba5f7992b743642919e4e712af83` 至 `origin/soc_debug` 后再次执行 `make clean all` 生成最新 `boot/bootloadermc/build/bootloader.bin`；
   - `git -C boot/bootloadermc status --porcelain` 输出为空（工作树 100% 洁净）。

---

## 5. 实板验证状态留白说明

- **软件准出前自检状态**：`PASS`（待 `COORD` 合龙执行 `SLICE-09` 四阶正式软件门禁与独立 Codex 冷审）。
- **真机实测状态**：**`待验证 (UNVERIFIED on Hardware - Awaiting Human Gate #2B)`**——按获批方案 §2.5.2，MC Bootloader 实板 SWD 烧录（`0x08000000`）及 AP 在线 `500ms` `0x01` 轮询下的物理复位自愈实测，须在单候选通过四阶软件门禁并获用户单独批准 `Human Gate #2B` 后方可执行。
