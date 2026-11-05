# TWIN-44 MC 固件 USART2 921600 升级与 USART1 非阻塞 `[MC-DBG]` 结构化日志输出交付自检报告 (author_01)

| 字段 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-44` (`revision: 1`, `qa_policy: streamlined-v1`) |
| **所属工作包** | `TASK-002` (关联 `TASK-007`, `TASK-010`) |
| **执行角色 / 会话** | `ENG-MC` (`8ca47c46-1cd8-4f82-955a-9742b6988ded`) |
| **当前轮次** | `author_01` |
| **目标代码仓库与分支** | `mcu-p3` (`feat/soc-debug`) |
| **基线 Commit (`base_commit`)** | `e051111e68dd61896ed42c0961153b167b8bca41` |
| **候选 Commit (`candidate_commit`)** | `a03aa9d9a371c4af985ee18e7c5a5c82c1b1c9e9` |
| **执行状态** | **Completed (交叉编译 0 错误、静态编码门禁 100% 通过、单元测试与回归测试 100% 通过)** |

---

## 1. 接单核对回执 (`dispatch_binding` & 前置输入校验)

接单前已逐项核对任务卡 `TWIN-44.md` (`revision: 1`) 与权威输入产物，确认无技术冲突或输入缺失：

| 核对项 | 路径 / 标识 | 期望版本 / SHA-256 | 实测结果 | 结论 |
| :--- | :--- | :--- | :--- | :--- |
| **ARCH 拆分方案** | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` | `revision: 2`, `fe72f550cc32d28dbba0a00d364373b8b2687c1c4c007a6e5f03732e94a99697` (ARCH `433026bf-a1ff-4863-8f3e-7a5f43b016ff`) | 完全一致 | PASS |
| **合并实施概要 (`protocol_input`)** | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` | `revision: 2`, `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec` | 完全一致 | PASS |
| **Debug 需求确认单** | `project-control/docs/planning/mc_th_debug_mode_requirement_confirmation_20261103.md` | `36ae2a6f8bc6ed13e6e89443fcca62fe882c841f2a65619ad735216d9cbacebe` | 已核对 | PASS |
| **921600 需求确认单** | `project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md` | `3911e18cf6ca949369d9449659c3fa842af57e025cd718de327a7c57b6ee0a37` | 已核对 | PASS |
| **源码基线 (`mcu-p3`)** | `feat/soc-debug` `HEAD` | `e051111e68dd61896ed42c0961153b167b8bca41` | 完全一致 | PASS |
| **前置依赖 (`depends_on`)** | `TWIN-24`, `TWIN-30` | `status: Done`, `blocked: false` | 均已闭环 Done | PASS |
| **写范围白名单 (`allowed_paths`)** | `minimc_proto.h`, `minimc_proto.c`, `main.c`, `docs/evidence/twin/TWIN-44/**` | 严禁触碰 `wk_usart.{c,h}`, `color-engine-mcu/**`, `marlin/**`, `soc-ap/**`, `boot/**` | 严格遵守 | PASS |

---

## 2. 交付产物与 SHA-256 清单

| 文件路径 | 变更说明 | SHA-256 |
| :--- | :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | 定义 `AP_USART_BAUDRATE (921600U)`、`MC_DEBUG_MODE_ENABLE (1)`、2048B 环形缓冲与 192B 单行上限常量、操作码及非阻塞 Debug 接口声明 | `b8c65d5fa792b2817203f5bf40e8aead1cacc11b54023849ac55584cf776cc60` |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | 在 `minimc_proto_init()` 安全重配 `USART2` 为 `921600U`；实现 `s_mc_dbg_ring[2048]` 非阻塞环形缓冲、`mc_debug_write()`、`mc_debug_poll_drain()`、`drop`/`trunc` 计数及全链路 `[MC-DBG]` 结构化日志 | `3c4ac16695afbe6737f79d2c1f25e41af5fb300472db633b267df5c98ef0d860` |
| `mcu-p3/motion-controller-mcu/project/src/main.c` | 模块化拆分主函数（满足 $\le 50$ 行门禁），将启动标识与心跳替换为非阻塞 `mc_debug_write()`，主循环接入 `mc_debug_poll_drain()` | `43287dd3437e722061be9516e8bc116061a52c4f555206daa76b0551fee83f55` |
| `project-control/docs/evidence/twin/TWIN-44/runs/author_01/test_twin44_mc_debug.c` | `TWIN-44` 独立正反例单元测试套件（覆盖 `921600` 重配、环形缓冲溢出/截断、五类业务字段、TH 级联超时与 CRC 错误） | `97b1892e71af3f473a1fcd23ffb30132f32aa1f130da4cf512dc23b49e737102` |

---

## 3. 核心实现要点

1. **`USART2` (`PA2`/`PA3`, AP↔MC 业务串口) 波特率升级至 `921600U`**：
   - 在 `minimc_proto.h` 定义 `#ifndef AP_USART_BAUDRATE` / `#define AP_USART_BAUDRATE 921600U`。
   - 在 `minimc_proto_init(void)`（于 `main.c` 中紧随 `wk_usart2_init()` 与 `wk_dma1_channel6_init()` 调用）中按标准外设安全时序执行：
     `usart_enable(USART2, FALSE)` $\rightarrow$ `usart_init(USART2, AP_USART_BAUDRATE, USART_DATA_8BITS, USART_STOP_1_BIT)` $\rightarrow$ `usart_enable(USART2, TRUE)`，保持 `PA2`/`PA3` GPIO 复用、`DMA1_CH2` TX、`DMA1_CH6` RX 及 `IDLE` 中断不变，零改动 `wk_usart.{c,h}`。
   - 保持 `USART6` (`PA4`/`PA5`, MC↔TH 级联 `921600`) 与 `USART1` (`PA9`/`PA10`, MC Debug `115200`) 波特率不变。
2. **`USART1` (`115200`) 非阻塞静态环形缓冲与定额排空**：
   - 定义 `static uint8_t s_mc_dbg_ring[2048]`（零动态内存分配）。
   - `mc_debug_write(const char *buf, uint16_t len)`：单条超过 `192` 字节时截断为 `192` 字节（以 `...\r\n` 结尾）并递增 `s_mc_dbg_trunc_count`；当环形缓冲剩余空间不足整条写入时立即丢弃并递增 `s_mc_dbg_drop_count`，绝不等待串口发送标志。
   - `mc_debug_poll_drain(void)`：每次调用最多非阻塞向 `USART1` 写入 `64` 字节；仅当 `usart_flag_get(USART1, USART_TDBE_FLAG) != RESET` 时写入 1 字节，未就绪立即返回。
3. **`[MC-DBG]` 结构化日志覆盖**：
   - 统一格式：`[MC-DBG] ts=<ms> dir=<RX|TX|RELAY_TX|RELAY_RX|STATE|ERR> node=<AP|MC|TH> seq=<u8> cmd=0x<hex> status=<OK|ACK|NACK|TIMEOUT|CRC_ERR|EXEC> <kv_pairs...> drop=<u32> trunc=<u32>\r\n`
   - 完整覆盖 `dir=RX`、`dir=TX`、`dir=RELAY_TX`、`dir=RELAY_RX`、`dir=STATE`（含 $\ge 500\text{ ms}$ 即 $\le 2\text{ Hz}$ 周期限频状态摘要）、`dir=ERR`（`CRC_ERR`、`BAD_FRAME`、`TIMEOUT`）以及温度、归零/运动、调平网格、进退丝/料槽、打印作业状态机五类核心业务字段。

---

## 4. 编译验证与自动化测试日志

### 4.1 MC 固件 CMake 交叉编译验证 (`build_mc_firmware`)

执行命令：
```bash
cd mcu-p3/motion-controller-mcu && cmake -B build -DCMAKE_BUILD_TYPE=Debug && cmake --build build -j4
```
关键输出：
```text
[ 98%] Building C object CMakeFiles/Marlin_AT32.dir/project/src/minimc_proto.c.obj
[100%] Linking C executable Marlin_AT32.elf
Memory region         Used Size  Region Size  %age Used
           FLASH:      375868 B       896 KB     40.97%
             RAM:       28864 B       384 KB      7.34%
Generating Marlin_AT32.bin and Marlin_AT32.hex
[100%] Built target Marlin_AT32
```
（注：编译验证完成后已清理 `mcu-p3/motion-controller-mcu/build/` 目录，未向 Git 提交任何构建产物。）

### 4.2 严格编译门禁 (`-Wall -Wextra -Wpedantic -Werror` & C++17 Header Check) 与契约对齐门禁

- `arm-none-eabi-gcc ... -Wall -Wextra -Wpedantic -Werror -std=gnu11 -c project/src/minimc_proto.c`：Exit Code `0`（0 警告、0 错误）。
- `g++ -std=c++17 -Wall -Wextra -Werror -I project/inc -fsyntax-only -x c++ -c project/inc/minimc_proto.h`：Exit Code `0`。
- `python3 test_harness/static_checks/minimcproto/check_opcode_alignment.py --strict`：`[PASS] 全端契约完全对齐：CMD_NACK (0x06) 与载荷长度规范全量吻合！`（Exit Code `0`）。

### 4.3 `TWIN-44` 独立单元测试与 `TWIN-24` 回归测试

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
[RUN ] test_relay_and_negative_error_cases
[PASS] test_relay_and_negative_error_cases
------------------------------------------------------------------------
All 4 TWIN-44 test suites PASSED!
========================================================================
```
同时运行 `TWIN-24` 6 项回归测试套件（`test_twin24_level_grid.c`）：`All 6 test suites PASSED!`。

---

## 5. 函数规模（$\le 50$ 行）与入参个数（$\le 4$ 个）静态自检表

| 所属文件 | 函数名称 | 起始-结束行 | 总跨度行数 (`<=50`) | 有效代码行 | 入参个数 (`<=4`) | 门禁结果 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `minimc_proto.c` | `mc_dbg_ring_free_space` | 125-137 | 13 | 13 | 0 | PASS |
| `minimc_proto.c` | `mc_dbg_ring_push_bytes` | 139-150 | 12 | 12 | 2 | PASS |
| `minimc_proto.c` | `mc_debug_set_enabled` | 152-155 | 4 | 4 | 1 | PASS |
| `minimc_proto.c` | `mc_debug_is_enabled` | 157-160 | 4 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_get_drop_count` | 162-165 | 4 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_get_trunc_count` | 167-170 | 4 | 4 | 0 | PASS |
| `minimc_proto.c` | `mc_debug_write` | 172-194 | 23 | 23 | 2 | PASS |
| `minimc_proto.c` | `mc_debug_poll_drain` | 196-210 | 15 | 15 | 0 | PASS |
| `minimc_proto.c` | `mc_dbg_emit` | 212-240 | 29 | 29 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_node_name` | 242-253 | 12 | 12 | 1 | PASS |
| `minimc_proto.c` | `mc_dbg_motion_state_str` | 255-270 | 16 | 16 | 1 | PASS |
| `minimc_proto.c` | `mc_dbg_job_state_str` | 272-303 | 32 | 32 | 1 | PASS |
| `minimc_proto.c` | `minimc_crc16` | 305-328 | 24 | 24 | 2 | PASS |
| `minimc_proto.c` | `ring_init` | 330-338 | 9 | 9 | 1 | PASS |
| `minimc_proto.c` | `ring_push` | 340-356 | 17 | 17 | 3 | PASS |
| `minimc_proto.c` | `ring_pop` | 358-367 | 10 | 9 | 2 | PASS |
| `minimc_proto.c` | `parser_init` | 369-378 | 10 | 10 | 1 | PASS |
| `minimc_proto.c` | `parser_reset` | 380-389 | 10 | 10 | 1 | PASS |
| `minimc_proto.c` | `parser_check_header` | 391-410 | 20 | 20 | 1 | PASS |
| `minimc_proto.c` | `parser_step_sof` | 412-439 | 28 | 28 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_log_frame_err` | 441-457 | 17 | 17 | 3 | PASS |
| `minimc_proto.c` | `parser_step` | 459-505 | 47 | 45 | 3 | PASS |
| `minimc_proto.c` | `build_version_resp` | 507-545 | 39 | 38 | 3 | PASS |
| `minimc_proto.c` | `build_pong_resp` | 547-588 | 42 | 41 | 4 | PASS |
| `minimc_proto.c` | `build_nack_resp` | 590-615 | 26 | 25 | 4 | PASS |
| `minimc_proto.c` | `build_temp_resp` | 617-655 | 39 | 36 | 3 | PASS |
| `minimc_proto.c` | `pos_mm_to_um` | 657-665 | 9 | 9 | 1 | PASS |
| `minimc_proto.c` | `level_mm_to_um` | 667-688 | 22 | 22 | 1 | PASS |
| `minimc_proto.c` | `query_homed_mask` | 690-706 | 17 | 17 | 0 | PASS |
| `minimc_proto.c` | `query_motion_state` | 708-719 | 12 | 12 | 0 | PASS |
| `minimc_proto.c` | `build_pos_resp` | 721-759 | 39 | 36 | 3 | PASS |
| `minimc_proto.c` | `build_level_grid_resp` | 761-801 | 41 | 39 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_format_temp_kv` | 803-818 | 16 | 16 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_format_motion_kv` | 820-843 | 24 | 24 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_format_level_kv` | 845-862 | 18 | 18 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_format_filament_kv` | 864-879 | 16 | 16 | 4 | PASS |
| `minimc_proto.c` | `mc_dbg_format_job_kv` | 881-895 | 15 | 15 | 2 | PASS |
| `minimc_proto.c` | `mc_dbg_emit_state_and_tx` | 897-903 | 7 | 7 | 3 | PASS |
| `minimc_proto.c` | `relay_frame` | 905-920 | 16 | 16 | 3 | PASS |
| `minimc_proto.c` | `handle_mc_core_queries` | 922-960 | 39 | 38 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_motion_and_level` | 962-998 | 37 | 36 | 3 | PASS |
| `minimc_proto.c` | `handle_mc_filament_and_job` | 1000-1032 | 33 | 32 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_query` | 1034-1064 | 31 | 30 | 2 | PASS |
| `minimc_proto.c` | `handle_ap_frame` | 1066-1102 | 37 | 36 | 2 | PASS |
| `minimc_proto.c` | `handle_th_frame` | 1104-1135 | 32 | 30 | 2 | PASS |
| `minimc_proto.c` | `check_th_relay_timeout` | 1137-1155 | 19 | 19 | 1 | PASS |
| `minimc_proto.c` | `mc_debug_log_periodic_state` | 1157-1178 | 22 | 20 | 1 | PASS |
| `minimc_proto.c` | `drain_ap_rx` | 1180-1195 | 16 | 16 | 0 | PASS |
| `minimc_proto.c` | `drain_th_rx` | 1197-1214 | 18 | 18 | 0 | PASS |
| `minimc_proto.c` | `minimc_proto_poll` | 1216-1224 | 9 | 9 | 0 | PASS |
| `minimc_proto.c` | `minimc_proto_push_ap_rx` | 1226-1233 | 8 | 8 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_process_rx` | 1235-1242 | 8 | 8 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_send` | 1244-1269 | 26 | 26 | 2 | PASS |
| `minimc_proto.c` | `minimc_proto_init` | 1271-1290 | 20 | 17 | 0 | PASS |
| `main.c` | `para_reset` | 108-111 | 4 | 4 | 1 | PASS |
| `main.c` | `main_init_clocks_and_dma` | 113-140 | 28 | 24 | 0 | PASS |
| `main.c` | `main_init_usarts_and_periph` | 142-172 | 31 | 27 | 0 | PASS |
| `main.c` | `main_init_marlin_modules` | 174-194 | 21 | 20 | 0 | PASS |
| `main.c` | `main_poll_debug_and_perf` | 196-217 | 22 | 20 | 0 | PASS |
| `main.c` | `main_loop_step` | 219-242 | 24 | 22 | 0 | PASS |
| `main.c` | `main` | 250-260 | 11 | 10 | 0 | PASS |
