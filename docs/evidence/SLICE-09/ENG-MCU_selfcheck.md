# SLICE-09 ENG-MCU 自检报告 (`S09-MCU` / `TH-ESTOP-01`)

## 1. 交付概要与版本锚点

- **责任角色**：`ENG-MCU`
- **业务仓库**：`mcu-p3`
- **锁定分支**：`feat/soc-debug`
- **基线提交 (`SLICE-08 r18b`)**：`a64bffbf1a0c5cbc2fe96b516320980426978b`
- **候选提交 (`candidate_commit`)**：`112842cb42146e466f7001ede30096bd0125c385`（8 位短提交：`112842cb` / `0x112842CB`，已线性 `rebase` 并推送至 `origin/feat/soc-debug`）
- **远端同步与工作区洁净度**：`git -C mcu-p3 rev-parse HEAD == git -C mcu-p3 rev-parse origin/feat/soc-debug`，且在最终 `make clean && make pack` 后 `git -C mcu-p3 status --porcelain` 输出为空。

---

## 2. 修改文件清单与 Diff Budget 核验（3 / 3 白名单内）

严格限制在 `project-control/slices/SLICE-09.yaml` 为 `ENG-MCU` 划定的 3 个 `allowed_paths` 文件内（`max_files: 3`，总计 `3 files changed, 144 insertions(+), 17 deletions(-)`）：

1. `color-engine-mcu/io_toggle/src/app/minimc_proto.c`：
   - 修复 `handle_th_motion_stop()`（共 35 行，3 个入参，全中文注释，零嵌套三目，单条 `if` 条件逻辑运算符最多 1 个 $\le 2$ 个）：
     - `plen > 1U`：单播且置 `MINIMC_FLAG_WANTS_ACK` 时返回 `build_nack_resp(src_id, seq, 0x02U, out_buf)`，广播或免应答返回 `0U`；
     - `plen == 1U && frame[MINIMC_HEADER_SIZE] > 1U`：单播且置 `MINIMC_FLAG_WANTS_ACK` 时返回 `build_nack_resp(src_id, seq, 0x03U, out_buf)`，广播或免应答返回 `0U`；
     - 仅当 `(plen == 0U) || (frame[MINIMC_HEADER_SIZE] == 1U)` 时执行 `quickStop()`、`thermistor_set_target_deci_c(0)`、`load_filament_Flag = 0` 及 `(void)th_control_enqueue_gcode("M112", 4U, true)`；当 `plen == 1U && frame[MINIMC_HEADER_SIZE] == 0U`（解除急停）时不执行关断、不清零目标温度、不入队 `"M112"`；
     - 移除原 `plen == 1U` 返回 `0B` 载荷的旧分支，对单播 `WANTS_ACK` 请求（含无参、`0x01` 锁存、`0x00` 解除）统一调用 `build_ack_resp(src_id, seq, out_buf)` 返回标准 `18B`（`4B CMD_ACK`）响应帧；广播（`dst_id == MINIMC_NODE_BROADCAST`）或未置 `MINIMC_FLAG_WANTS_ACK` 返回 `0U`。
2. `color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c`：
   - 更新 `test_twin48_filament_and_stop()` 第 1054 行附近 `0x17 [0x01]` 响应长度断言由 `14U` 升级为 `18U`（`4B CMD_ACK`），并校验载荷末 2 字节保留位为 `0x0000`。
3. `color-engine-mcu/tests/test_th_ota_and_bootid.c`：
   - 新增辅助注入函数 `send_th_estop_frame()` 与两组正负配对测试 `test_th_estop_0x17_latch_and_release()`、`test_th_estop_0x17_nack_and_bcast()`，完整覆盖：
     - `0x17 [0x01]` 单播锁存：`18B` 帧（`4B CMD_ACK`，`reserved=0x0000`，CRC16 合法）+ `quickStop()` 调用 + 清零目标温度 + 清零 `load_filament_Flag` + 入队 `"M112"`；
     - `0x17 [0x00]` 单播解除：`18B` 帧（`4B CMD_ACK`，`reserved=0x0000`，CRC16 合法）+ 零 `quickStop()` 调用 + 保持目标温度与电机标志不变 + 零 `"M112"` 入队；
     - `0x17 [0x02]` 非法模式：单播返回 `17B` `NACK 0x03` 且无急停副作用，广播返回 `0U`；
     - `plen > 1`（`plen=2`）：单播返回 `17B` `NACK 0x02`，广播返回 `0U`；
     - 广播 `dst_id=0xFF`（`[0x01]` / `[0x00]`）及单播未置 `MINIMC_FLAG_WANTS_ACK`：均返回 `0U` 无应答。

---

## 3. 本地单测与静态门禁执行结果

1. **TH 回归与静态门禁套件**：
   - 命令：`(cd mcu-p3/color-engine-mcu/tests && sh run_tests.sh)`
   - 结果：`PASS`（`test_twin45_th_debug` 10 项全绿、`test_th_ota_and_bootid` TWIN-64 + TH-ESTOP-01 全绿、`AT32F423xC_FLASH.ld` 236K + 零 `M997` 残留 + 函数行数 $\le 50$ / 入参 $\le 4$ / 禁嵌套三目 / 单 `if` 逻辑运算符 $\le 2$ 校验全绿）。
2. **MC 回归与静态门禁套件**：
   - 命令：`(cd mcu-p3/motion-controller-mcu/tests && sh run_tests.sh)`
   - 结果：`PASS`（`test_twin44_mc_debug` 10 项全绿、`test_mc_ota_and_relay` 全绿、MC S04 门禁校验全绿）。
3. **跨仓秒级机械门禁 (`fast_gate.py`)**：
   - 命令：`python3 -B project-control/tools/gates/fast_gate.py --workspace /home/sushaohua/workspace/ai_soc_project --files mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c mcu-p3/color-engine-mcu/tests/test_th_ota_and_bootid.c`
   - 结果：`PASS`（退出码 `0`，同时在干净 `HEAD` 上通过 `SLICE-09.yaml` `ENG-MCU` `check_subtask_boundary` 核验）。

---

## 4. 最终干净 `HEAD` (`112842cb`) 交叉编译与打包固件清单

在推送完成且工作区干净的最终 `HEAD` (`112842cb42146e466f7001ede30096bd0125c385`) 上，依次执行 `(cd mcu-p3/motion-controller-mcu && make clean && make pack)` 与 `(cd mcu-p3/color-engine-mcu/io_toggle && make clean && make pack)`，经 `arm-none-eabi-objdump` 与 `ATSG` 128B Trailer 核实双包均嵌入短提交 `0x112842CB`：

| 固件包 | 精确文件路径 | 总字节数（净载 + 128B Trailer） | 完整文件 SHA-256 | 净载 Payload SHA-256 | Board ID / 版本号 / Trailer CRC32 | 嵌入短提交 |
| --- | --- | :---: | --- | --- | --- | :---: |
| **`fw_mc.bin`** | `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/build/fw_mc.bin` | `384668` (`384540 + 128`) | `320966b15cf2fb414a17cb90b4291023bb993e4922777eeace96a35056644915` | `31ea1f558446294937d0c0ca40d9f32c0a44fbef5d707a1cfd9387284faa2336` | `0x43500001` / `0x02003CB1` / `0xEE063E0F` | `0x112842CB` (`@0x080492b4`) |
| **`fw_th.bin`** | `/home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` | `76968` (`76840 + 128`) | `904ceee06e31729b98fe774b3845d1dc1b540622c44d6d0db3a3fa85a0aa7624` | `c9f3f5a5b02ac5bec68659f9266af71407ba8af5080dd811add9ddd1d1beecb2` | `0x42300001` / `0x02006F93` / `0x6C9B4F69` | `0x112842CB` (`@0x0800c264`) |
