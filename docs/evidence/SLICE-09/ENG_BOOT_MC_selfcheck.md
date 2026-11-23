# SLICE-09 `ENG_BOOT_MC` 自检报告（`S09-BOOT-MC` / `BOOT-MC-STAY-01` + `S09-06` 收口）

## 1. 角色身份、分支红线与提交元数据

- **执行角色**：`ENG_BOOT_MC`
- **目标业务仓**：`boot/bootloadermc`（远端：`ssh://git@192.168.77.79:2222/sushaohua/bootloadermc.git`）
- **锁定开发分支**：`soc_debug`（已物理核验本地与远端 `refs/heads/main` 恒保持 `01bfda29b82f0576cb255d0b4196aeda1edb8d2e` 零触碰）
- **基线 Commit SHA**：`3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`
- **前序候选 Commit SHA (`r03`)**：`d2ef9fb6955eba5f7992b743642919e4e712af83`
- **最终候选 Commit SHA（本地 `HEAD` 与远端 `origin/soc_debug` 对齐）**：`157b5317bc8fd90e93f684f949d37e98428ea193`
- **依据方案、切片与返修单**：
  - 获批 SSoT 方案：`project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md`（`v1.4`，§2.1.2、§2.2.1、§2.2.3、§2.3.2、§2.4.2 `S09-BOOT-MC`、§2.5.3）
  - 缺陷交接单：`project-control/docs/planning/bootloadermc_0x01_stay_in_boot_handoff_20261121_145800.md`
  - 冷审返修单：`project-control/docs/evidence/SLICE-09/run_20261123_r03/codex/final.json`（闭环 `S09-06`）
  - 切片规格：`project-control/slices/SLICE-09.yaml`（`revision: 3`）
  - 协议契约：`project-control/contracts/minimc_v2_contract.yaml`（Rev `2.0.4`，零变更）
- **硬件与探针隔离声明**：本阶段严格遵守软件准出与人工闸门隔离约束，未触碰任何物理硬件，未调用 `probe-rs`（`probe_rs_used = false`）。

---

## 2. 沿用弊端评估、精确改动边界与数据流分解

### 2.1 原有逻辑弊端与 `r03` 冷审 `S09-06` 根因
- **`BOOT-MC-STAY-01` 根因**：基线 `bootloader/src/boot_uart_ota.c` 的 `handle_cmd_get_version()` 在响应只读 `0x01 (MINIMC_CMD_GET_VERSION)` 时误置 `s_ota.stay_in_boot = 1U;`，与 AP 守护进程 `500ms` 常规版本轮询碰撞，导致非升级复位进入 `2.0s` 探测窗口后永久锁死在 Bootloader。
- **`S09-06` 单测与生产阈值脱节根因**：`r03` 候选在 `bootloader/src/main.c:218` 硬编码 `probe_ticks >= 2000U && !g_udisk_connected`，而宿主机单测 `tests/test_mc_boot_ota.c` 最后直接由测试代码自行调用 `jump_to_app()`，未经过生产超时判定函数且未校验窗口届满前（如 `1999ms`）保持不跳。
- **根治措施**：在 `boot_uart_ota.h/.c` 统一定义 `#define BOOT_PROBE_WINDOW_MS (2000U)` 并提炼纯判定函数 `boot_uart_ota_should_jump_after_window(probe_ticks, udisk_connected, upgrade_in_progress)`；`bootloader/src/main.c` 主循环直接调用该生产函数驱动 `handle_no_disk_timeout(probe_ticks)`，宿主机单测 `tests/test_mc_boot_ota.c` 按同构毫秒步进直接调用同一生产函数验证窗口届满前保持、满 `2000ms` 自动跳 App 及各类显式驻留/忙条件越窗保持驻留。

### 2.2 白名单与 Diff Budget 核验（相对基线 `3e01c00`，累计 `4 / 4` 文件）

| 序号 | 修改文件路径（相对 `boot/bootloadermc/`） | 白名单核对 | 累计行数变更 (`git diff --numstat 3e01c00..HEAD`) | 函数规模与入参核验 |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `bootloader/inc/boot_uart_ota.h` | 允许 | `+13 / -0` | 定义 `BOOT_PROBE_WINDOW_MS (2000U)` 与 3 入参公开声明 |
| 2 | `bootloader/src/boot_uart_ota.c` | 允许 | `+24 / -1` | `handle_cmd_get_version` (19 行/1 入参)、`boot_uart_ota_should_jump_after_window` (16 行/3 入参) |
| 3 | `bootloader/src/main.c` | 允许 | `+18 / -8` | `main` 总长 38 行（含空行与注释，`<= 50` 行）、0 入参 |
| 4 | `tests/test_mc_boot_ota.c` | 允许 | `+190 / -10` | 全部测试与辅助函数 `<= 45` 行（上限 50 行）、入参 `<= 4` 个 |

### 2.3 数据流向与状态变化步骤分解
1. **启动初始化（`boot_uart_ota_init`）**：清零静态上下文 `s_ota`（`stay_in_boot = 0U`）并释放单写者锁；仅当 SRAM `0x2005FFF0` 命中 `0x55504732 ("UPG2")` 魔数时清零魔数并置 `s_ota.stay_in_boot = 1U`。
2. **只读探测帧处理（`0x01` / `0x03`）**：
   - `handle_cmd_get_version()` 校验 `payload_len == 0U` 后组装 16B `minimc_payload_version_report_t`（`proto=2.0`、`fw=1.0`、`boot_id`、`MC_FW_GIT_COMMIT_SHORT=0x4FC171EA`、`MC_BOOT_CAPABILITY_FLAGS=0xC0080435`）通过 `USART2` 发送 `0x02` 响应帧，**不修改 `s_ota.stay_in_boot`**；
   - `handle_cmd_ping()` 回显 `echo_token` 与统计计数发送 `0x04` 响应帧，**不修改 `s_ota.stay_in_boot`**。
3. **显式驻留与复位控制（`0x1D` / `0x20`）**：
   - `0x1D(action=1)` 回复 `0x00 CMD_ACK` 并置 `pending_reboot = 1U`，不置 `stay_in_boot`；
   - `0x1D(action=2)` 回复 `0x00 CMD_ACK` 并显式置 `s_ota.stay_in_boot = 1U`；
   - `0x20 (CMD_OTA_START)` 通过单写者互斥、尺寸、板型 `0x43500001` 与 128B `ATSG` `trailer_crc32` 准入并预擦首扇区后，持有 `BOOT_WRITER_UART2` 且置 `s_ota.stay_in_boot = 1U`（准入失败则释放写锁且保持未驻留）。
4. **统一生产窗口超时跳转裁决（`main.c` ➔ `boot_uart_ota_should_jump_after_window`）**：主循环仅在 `g_upgrade_in_progress == 0U && boot_uart_ota_should_stay_in_boot() == 0U` 时累加 `probe_ticks`，每毫秒调用 `boot_uart_ota_should_jump_after_window(probe_ticks, g_udisk_connected, g_upgrade_in_progress)`；仅当无升级进行中、无串口驻留请求、无 U 盘连接且 `probe_ticks >= BOOT_PROBE_WINDOW_MS (2000U)` 时返回 `1U`，驱动 `handle_no_disk_timeout(probe_ticks)` 校验 `is_app_valid(0x08020000)` 并安全跳入 MC App。

---

## 3. 黄金回滚镜像与最终候选镜像摘要对照

| 镜像类别 | 对应 Commit SHA (`boot/bootloadermc`) | 归档/产物路径 | 精确字节数 | Flash 预算 (`131072 B`) | ELF 段分布 (`text / data / bss / dec`) | SHA-256 摘要 |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **修改前黄金回滚镜像** | `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` | `project-control/docs/evidence/SLICE-09/candidate_mcu_artifacts/bootloader_3e01c00_rollback.bin` | `37600 B` | PASS (`28.69%`) | `37364 / 184 / 19272 / 56820` | `1082c318fee4aecb175921290b773137970c7501b21ebd26abf32b887719d9df` |
| **最终候选镜像 (`HEAD`)** | `157b5317bc8fd90e93f684f949d37e98428ea193` | `boot/bootloadermc/build/bootloader.bin` | `37628 B` | PASS (`28.71%`) | `37392 / 184 / 19272 / 56848` | `0e9ace3fc6dc8ffc557cd0225dd36a78b776066b2a05803e7539c64e24804874` |

---

## 4. 构建、宿主机单测与门禁验证记录

1. **`tests/run_tests.sh` 全套四步门禁**：
   - 命令：`(cd boot/bootloadermc && PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh tests/run_tests.sh)`
   - `[1/4]` ARM 交叉编译（`-Wall -Wextra -Werror`）：`PASS`（`bootloader.bin` = `37628 B <= 131072 B`，ELF 符号表与源码头文件零 `USART6` 引用）。
   - `[2/4]` `scripts/pack_firmware.py` MC(`896KB`) / TH(`236KB`) 正负边界校验：`PASS`。
   - `[3/4]` 宿主机单元测试 `test_mc_boot_ota`（`-Wall -Wextra -Werror -DHOST_UNIT_TEST`）及 `SLICE-09.yaml` 第 88 行容器同款单文件编译命令验证：`PASS`，直接调用生产 `boot_uart_ota_should_jump_after_window()` 覆盖：
     - 窗口届满前保持不跳：`0ms`、`500ms`、`1000ms`、`1500ms` 及 `1999ms`（伴随连续 4 轮 `0x01`/`0x03` 只读轮询）均返回 `0U` 且 `s_jump_count == 0U`；
     - 窗口届满自动跳转：推进最后 `1ms` 达 `2000ms`（`BOOT_PROBE_WINDOW_MS`）时生产判定返回 `1U` 并驱动 `jump_to_app(0x08020000)`；
     - 普通软复位不驻留：`0x1D(action=1)` 回复 `0x00 CMD_ACK`、触发系统复位且 `boot_uart_ota_should_stay_in_boot() == 0U`；
     - 显式驻留与忙保护越窗保持：`UPG2` 魔数、`0x1D(action=2)`、合法 `0x20 (CMD_OTA_START)`、`udisk_connected == 1U`、`upgrade_in_progress == 1U` 在 `2000ms` 与 `5000ms` 均返回 `0U` 继续驻留（且非法错板 `0x20` 拒绝不误锁驻留）；
     - 完整串口 OTA（`0x20 -> 0x21 -> 0x23 -> 0x22` 延迟回写首扇区与跳 App）、50ms 字节间超时恢复、外层 CRC16 NACK、USB Host U 盘升级与单写者并发互斥全量回归通过。
   - `[4/4]` C 函数总行数（`<= 50` 行）与参数个数（`<= 4` 个）静态门禁：`PASS`。
2. **`fast_gate.py` 机械门禁与子任务边界校验**：
   - 命令：`python3 -B project-control/tools/gates/fast_gate.py --workspace /home/sushaohua/workspace/ai_soc_project --files boot/bootloadermc/bootloader/inc/boot_uart_ota.h boot/bootloadermc/bootloader/src/boot_uart_ota.c boot/bootloadermc/bootloader/src/main.c boot/bootloadermc/tests/test_mc_boot_ota.c`
   - 结果：退出码 `0`；`SLICE-09.yaml`（`revision: 3`）中 `ENG_BOOT_MC` `check_subtask_boundary` 分支/路径/预算/静态检查 `SUBTASK_BOUNDARY_PASS`。
3. **线性推送与最终 `HEAD` 洁净构建核验**：
   - 执行 `git fetch origin soc_debug && git rebase origin/soc_debug && git push origin soc_debug` 将 `157b5317bc8fd90e93f684f949d37e98428ea193` 线性推送至远端，核验 `git ls-remote origin refs/heads/soc_debug refs/heads/main` 一致且 `main` 未变动；
   - 推送完成后执行 `make clean all` 生成与最新 `HEAD` 匹配的 `build/bootloader.bin`、`build/bootloader.elf`、`build/bootloader.map`；
   - `git -C boot/bootloadermc status --porcelain` 输出为空（工作树 100% 洁净）。

---

## 5. 实板验证状态留白说明

- **软件准出前自检状态**：`PASS`（待 `COORD` 更新归档制品摘要并合龙执行 `SLICE-09 r04` 四阶正式软件门禁与独立 Codex 冷审）。
- **真机实测状态**：**`待验证 (UNVERIFIED on Hardware - Awaiting Human Gate #2B)`**——按获批方案 §2.5.2，MC Bootloader 实板 SWD 烧录（`0x08000000`）及 AP 在线 `500ms` `0x01` 轮询下的物理复位自愈实测，须在单候选通过四阶软件门禁并获用户单独批准 `Human Gate #2B` 后方可执行。
