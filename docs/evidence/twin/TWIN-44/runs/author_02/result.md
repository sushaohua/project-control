# TWIN-44 第二轮修正与自检证据报告 (`run_id: author_02`)

## 1. 接单核对回执（`run_id: author_02`）

| 核对项 | 期望值 / 权威契约 | 实测核对结果 | 状态 |
| :--- | :--- | :--- | :--- |
| 任务卡 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-44.md` (`revision: 1`, SHA-256: `8da574e4410f9f3d5e117d56a11fc6f0697aa971289d9461ef1008d882944565`) | 一致 | PASS |
| 执行角色与会话 | `ENG-MC` (`8ca47c46-1cd8-4f82-955a-9742b6988ded`), `run_id: author_02` | 一致 | PASS |
| 首轮独立 QA 报告 | `project-control/docs/evidence/twin/TWIN-44/runs/qa_01/` (Codex session `01a1a48a-3fb2-7ca0-b715-eac8b6d6e7d1`) | 已精读全部 3 项发现并逐一闭环 | PASS |
| `ARCH` 权威技术拆分方案 | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 6`, SHA-256: `a1a6e9d0a35ad504720d63c6276584646cc14c2fea7597985280c350dc1ddc2b`) | 第 `1.3.1` / `1.3.2` 节技术裁决完全对齐 | PASS |
| `protocol_input` | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` (`revision: 2`, SHA-256: `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec`) | 一致 | PASS |
| 修改范围 (`allowed_paths`) | 仅限 `mcu-p3/motion-controller-mcu/project/src/{minimc_proto.c,main.c,test_twin44_mc_debug.c}`, `inc/minimc_proto.h`, `project-control/docs/evidence/twin/TWIN-44/**` | 零越界，未触碰 `wk_usart.{c,h}`、`color-engine-mcu/**`、`marlin/**` | PASS |
| 新候选提交 (`candidate_commit`) | `mcu-p3` (`feat/soc-debug`) = `84072c726fd99c4c54369247a36a6d4f14ebc4a6` | 已推送至 `origin/feat/soc-debug`（相对 `e051111e68dd61896ed42c0961153b167b8bca41` 仅含 4 个白名单文件） | PASS |

---

## 2. 针对独立 QA (`qa_01`) 三项发现的逐项整改闭环（对照 `ARCH` `revision: 6` 第 1.3.1 / 1.3.2 节）

### 2.1 整改项 1：状态与温度实时动态同步，消除静态常量失真
1. **引入 `thermistor.h` 并实现 `static void mc_dbg_sync_runtime_state(void)`（11 行，0 入参）**：
   - 实时读取 Marlin 全局采样变量 `current_temperature_ex1` 与 `current_temperature_bed`；
   - 当任一通道为 `BAD_TEMPERATURE` (`1024`) 或 `< -200` 时，置 `s_dbg_state.heater_fault = 1U`，并将故障通道温度打入哨兵值 `MINIMC_TEMP_SENTINEL_FAULT` (`32767` / `0x7FFF`)；正常时置 `s_dbg_state.heater_fault = 0U`，并将 `raw * 10` (`0.1°C`) 实时同步至 `s_dbg_state.nozzle_ddC` 与 `s_dbg_state.bed_ddC`；
   - 在 `build_temp_resp()`、`mc_dbg_format_temp_kv()`、`mc_dbg_emit_state_and_tx()` 及 `mc_debug_log_periodic_state()` 中调用 `mc_dbg_sync_runtime_state()`，并在 `build_temp_resp()` 中绑定真实 `target_temp_deci_c = s_dbg_state.bed_set_ddC` 与 `sensor_status = (s_dbg_state.heater_fault != 0U) ? MINIMC_TEMP_STATUS_DISCONNECTED : MINIMC_TEMP_STATUS_OK`。
2. **各命令处理分支从请求载荷动态解析业务状态**：
   - `MINIMC_CMD_SET_TEMP` (`0x10`)：从载荷动态更新 `nozzle_set_ddC` 与 `bed_set_ddC`；
   - `MINIMC_CMD_MOTION_HOME` (`0x11`) / `MOVE` (`0x12`) / `STOP` (`0x17`)：通过 `mc_dbg_update_motion_req()` 动态更新 `axes_mask`（`STOP` 置 `0`）与 `feed`（`STOP` 置 `0`），坐标 `x/y/z_mm_x100`、`homed_mask`、`motion_state` 实时从 `current_position[]`、`axis_known_position[]`、`movesplanned()`、`is_paused` 读取；
   - `MINIMC_CMD_LEVEL_GRID_QUERY` (`0x18`)：支持从载荷读取 `probe_idx` 并实时读取 `bed_level[gx][gy]`；
   - `MINIMC_CMD_FILAMENT_CONTROL` (`0x15`) / `SLOT_SELECT` (`0x19`)：动态解析 `slot`、`op` (`SELECT`/`LOAD`/`UNLOAD`) 与 `filament_present_mask`；
   - `MINIMC_CMD_JOB_CONTROL` (`0x13`)：动态解析 `job_state_id` 与 16 位千分比进度 `progress_permille` (`frame[13..14]`)，且当 `is_paused != 0U` 时实时反映 `job_state=PAUSED`。

### 2.2 整改项 2：强制校验 `minimc_proto_send()` 与 `forward_uart_send_raw()` 返回值，杜绝伪阳性 ACK
1. 新增 `mc_dbg_log_tx_err()`（9 行，3 参）与 `mc_dbg_emit_tx_or_err()`（14 行，3 参），并升级 `mc_dbg_emit_state_and_tx()`（14 行，4 参）：
   - 在 `minimc_proto.c` 全部响应发送路径（`GET_VERSION`、`PING`、`GET_TEMP`/`SET_TEMP`、`POS_QUERY`/`MOTION_*`、`LEVEL_GRID_QUERY`、`FILAMENT_CONTROL`/`SLOT_SELECT`、`JOB_CONTROL`、`NACK` 及 `handle_th_frame` 级联回传）均捕获 `const bool tx_ok = minimc_proto_send(...)`；
   - 仅当 `tx_ok == true` 时才更新 `s_dbg_state.ack_seq = seq_u8` 并输出 `dir=STATE` 与 `dir=TX status=ACK|NACK`；
   - 当 `tx_ok == false`（如 `USART2` DMA 忙超时）时，抑制 `dir=STATE` 与 `dir=TX status=ACK`，并输出 `[MC-DBG] ... dir=ERR node=MC seq=<seq> cmd=0x<XX> status=TX_ERR err_code=0x06`。
2. 在 `handle_ap_frame()` 向 TH 转发级联帧时：
   - 先调用 `forward_uart_send_raw(relay_buf, len)` 并校验返回值；
   - 若返回 `false`（发送失败），立即复位 `s_relay_pending = false`，抑制 `dir=RELAY_TX` 并输出 `[MC-DBG] ... dir=ERR node=TH seq=<seq> cmd=0x<XX> status=TX_ERR err_code=0x06`。

### 2.3 整改项 3：沙箱可写路径适配与单元测试随仓提交
- 将包含 6 大测试套件的 `mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c` 随 `mcu-p3` 仓库提交，适配只读挂载 `/workspace` 的 `qa-sandbox:20261029` 容器在 `/tmp/test_twin44` 编译运行。

---

## 3. 交付物与 SHA-256 清单

| 文件路径 | SHA-256 |
| :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | `d6e28139d10132e78fa83e55d7fe7208707ac080730f0b42dde36f9e8b77735e` |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | `78a3a75f6cbeb46bd100d8f89a6b234762f10b41b58bbc29f560491082d49d1a` |
| `mcu-p3/motion-controller-mcu/project/src/main.c` | `43287dd3437e722061be9516e8bc116061a52c4f555206daa76b0551fee83f55` |
| `mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c` | `54c3808fdf091a17f2556f43e3518c58075c6fe1d370f13d718b08cff016f6fd` |

---

## 4. 受控沙箱命令与宿主机交叉编译验证日志

### 4.1 沙箱单元测试验证命令 (`verify_mc_debug_and_921600_unit`)
执行命令：
```bash
gcc -std=c11 -O2 -Wall -Wextra -no-pie -fno-pie -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER -I project/inc -I project/delay -I project/marlin -I project/marlin/marlin_core -I project/marlin/marlin_module -I libraries/drivers/inc -I libraries/cmsis/cm4/core_support -I libraries/cmsis/cm4/device_support project/src/minimc_proto.c project/src/test_twin44_mc_debug.c -o /tmp/test_twin44 && /tmp/test_twin44 && rm -f /tmp/test_twin44
```
实测输出：
```text
========================================================================
TWIN-44 MC USART2 921600 & USART1 Non-Blocking [MC-DBG] Verification
========================================================================
[RUN ] test_usart2_921600_reconfig
[PASS] test_usart2_921600_reconfig
[RUN ] test_ring_buffer_trunc_and_drop
[PASS] test_ring_buffer_trunc_and_drop
[RUN ] test_mc_dbg_all_five_categories_and_dirs
[PASS] test_mc_dbg_all_five_categories_and_dirs
[RUN ] test_runtime_temp_fault_and_pause_sync
[PASS] test_runtime_temp_fault_and_pause_sync
[RUN ] test_tx_fail_suppresses_false_ack
[PASS] test_tx_fail_suppresses_false_ack
[RUN ] test_relay_and_negative_error_cases
[PASS] test_relay_and_negative_error_cases
------------------------------------------------------------------------
All 6 TWIN-44 test suites PASSED!
========================================================================
```

### 4.2 宿主机 `arm-none-eabi-gcc` 交叉编译 (`make -j4`)
```text
[ 97%] Building C object CMakeFiles/Marlin_AT32.dir/project/src/minimc_proto.c.obj
[ 98%] Linking C executable Marlin_AT32.elf
Memory region         Used Size  Region Size  %age Used
           FLASH:      376924 B       896 KB     41.08%
             RAM:       28864 B       384 KB      7.34%
Generating Marlin_AT32.bin and Marlin_AT32.hex
[100%] Built target Marlin_AT32
```
（验证后已清理 `build/` 目录，确保工作树干净。）

---

## 5. C/C++ 编码规范硬性门禁静态自检表（全部函数 $\le 50$ 行、$\le 4$ 个入参）

- **最大值统计**：`minimc_proto.c` 共 37 个函数（最大 48 行，最多 4 入参）；`main.c` 共 7 个函数（最大 31 行，最多 1 入参）；`test_twin44_mc_debug.c` 共 20 个函数（最大 38 行，最多 4 入参）。
- **内存与指针安全**：零动态内存分配（0 处 `malloc`/`free`/`new`/`delete`），公开函数首行均具备空指针卫语句校验，零压缩指针算术。

| 文件 | 函数名 | 起止行号 | 行数 ($\le 50$) | 入参个数 ($\le 4$) | 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `minimc_proto.c` | `mc_dbg_ring_free_space` | 129-141 | 13 | 0 | PASS |
| `minimc_proto.c` | `mc_dbg_ring_push_bytes` | 143-154 | 12 | 2 | PASS |
| `minimc_proto.c` | `mc_debug_set_enabled` | 156-159 | 4 | 1 | PASS |
| `minimc_proto.c` | `mc_debug_is_enabled` | 161-164 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_get_drop_count` | 166-169 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_get_trunc_count` | 171-174 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_write` | 176-198 | 23 | 2 | PASS |
| `minimc_proto.c` | `mc_debug_poll_drain` | 200-214 | 15 | 0 | PASS |
| `minimc_proto.c` | `mc_dbg_emit` | 216-244 | 29 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_node_name` | 246-257 | 12 | 1 | PASS |
| `minimc_proto.c` | `mc_dbg_motion_state_str` | 259-274 | 16 | 1 | PASS |
| `minimc_proto.c` | `mc_dbg_job_state_str` | 276-307 | 32 | 1 | PASS |
| `minimc_proto.c` | `minimc_crc16` | 309-332 | 24 | 2 | PASS |
| `minimc_proto.c` | `ring_init` | 334-342 | 9 | 1 | PASS |
| `minimc_proto.c` | `ring_push` | 344-360 | 17 | 3 | PASS |
| `minimc_proto.c` | `ring_pop` | 362-371 | 10 | 2 | PASS |
| `minimc_proto.c` | `parser_init` | 373-382 | 10 | 1 | PASS |
| `minimc_proto.c` | `parser_reset` | 384-393 | 10 | 1 | PASS |
| `minimc_proto.c` | `parser_check_header` | 395-414 | 20 | 1 | PASS |
| `minimc_proto.c` | `parser_step_sof` | 416-443 | 28 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_log_frame_err` | 445-461 | 17 | 3 | PASS |
| `minimc_proto.c` | `parser_step` | 463-509 | 47 | 3 | PASS |
| `minimc_proto.c` | `build_version_resp` | 511-549 | 39 | 3 | PASS |
| `minimc_proto.c` | `build_pong_resp` | 551-592 | 42 | 4 | PASS |
| `minimc_proto.c` | `build_nack_resp` | 594-619 | 26 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_sync_runtime_state` | 621-631 | 11 | 0 | PASS |
| `minimc_proto.c` | `build_temp_resp` | 633-674 | 42 | 3 | PASS |
| `minimc_proto.c` | `pos_mm_to_um` | 676-684 | 9 | 1 | PASS |
| `minimc_proto.c` | `level_mm_to_um` | 686-707 | 22 | 1 | PASS |
| `minimc_proto.c` | `query_homed_mask` | 709-725 | 17 | 0 | PASS |
| `minimc_proto.c` | `query_motion_state` | 727-738 | 12 | 0 | PASS |
| `minimc_proto.c` | `build_pos_resp` | 740-778 | 39 | 3 | PASS |
| `minimc_proto.c` | `build_level_grid_resp` | 780-820 | 41 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_format_temp_kv` | 822-838 | 17 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_format_motion_kv` | 840-863 | 24 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_format_level_kv` | 865-882 | 18 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_format_filament_kv` | 884-899 | 16 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_format_job_kv` | 901-915 | 15 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_log_tx_err` | 917-925 | 9 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_emit_tx_or_err` | 927-940 | 14 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_emit_state_and_tx` | 942-955 | 14 | 4 | PASS |
| `minimc_proto.c` | `relay_frame` | 957-972 | 16 | 3 | PASS |
| `minimc_proto.c` | `handle_mc_core_queries` | 974-1017 | 44 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_update_motion_req` | 1019-1040 | 22 | 2 | PASS |
| `minimc_proto.c` | `handle_mc_motion_and_level` | 1042-1078 | 37 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_filament_and_job` | 1080-1127 | 48 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_query` | 1129-1158 | 30 | 2 | PASS |
| `minimc_proto.c` | `handle_ap_frame` | 1160-1201 | 42 | 2 | PASS |
| `minimc_proto.c` | `handle_th_frame` | 1203-1234 | 32 | 2 | PASS |
| `minimc_proto.c` | `check_th_relay_timeout` | 1236-1254 | 19 | 1 | PASS |
| `minimc_proto.c` | `mc_debug_log_periodic_state` | 1256-1278 | 23 | 1 | PASS |
| `minimc_proto.c` | `drain_ap_rx` | 1280-1295 | 16 | 0 | PASS |
| `minimc_proto.c` | `drain_th_rx` | 1297-1314 | 18 | 0 | PASS |
| `minimc_proto.c` | `minimc_proto_poll` | 1316-1324 | 9 | 0 | PASS |
| `minimc_proto.c` | `minimc_proto_push_ap_rx` | 1326-1333 | 8 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_process_rx` | 1335-1342 | 8 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_send` | 1344-1369 | 26 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_init` | 1371-1400 | 30 | 0 | PASS |
| `main.c` | `para_reset` | 108-111 | 4 | 1 | PASS |
| `main.c` | `main_init_clocks_and_dma` | 113-140 | 28 | 0 | PASS |
| `main.c` | `main_init_usarts_and_periph` | 142-172 | 31 | 0 | PASS |
| `main.c` | `main_init_marlin_modules` | 174-194 | 21 | 0 | PASS |
| `main.c` | `main_poll_debug_and_perf` | 196-217 | 22 | 0 | PASS |
| `main.c` | `main_loop_step` | 219-242 | 24 | 0 | PASS |
| `main.c` | `main` | 250-260 | 11 | 0 | PASS |
| `test_twin44_mc_debug.c` | 全部 20 个函数 | 29-364 | 最大 38 | 最多 4 | PASS |
