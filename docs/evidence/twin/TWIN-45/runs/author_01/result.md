# TWIN-45 TH 固件 USART3 非阻塞 `[TH-DBG]` 全操作结构化日志输出交付自检报告 (author_01)

| 字段 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-45` (`revision: 1`, `qa_policy: streamlined-v1`) |
| **所属工作包** | `TASK-002` (关联 `TASK-007`, `TASK-010`) |
| **执行角色 / 会话** | `ENG-TH` (`d5309433-d257-4397-b0b5-ef72e5d66d55`) |
| **当前轮次** | `author_01` |
| **目标代码仓库与分支** | `mcu-p3` (`feat/soc-debug`) |
| **任务卡登记基线 (`base_commit`)** | `e051111e68dd61896ed42c0961153b167b8bca41` (派单时分支基线 `a03aa9d9a371c4af985ee18e7c5a5c82c1b1c9e9`) |
| **候选 Commit (`candidate_commit`)** | `8b9afc7041cc7baee7310e51458ba921178ad1ba` |
| **执行状态** | **Completed (交叉编译 0 错误、静态编码门禁 100% 通过、单元测试与回归验证 100% 通过)** |

---

## 1. 接单核对回执 (`dispatch_binding` & 前置输入校验)

接单前已逐项核对任务卡 `TWIN-45.md` (`revision: 1`) 与权威输入产物，确认无技术冲突或输入缺失：

| 核对项 | 路径 / 标识 | 期望版本 / SHA-256 | 实测结果 | 结论 |
| :--- | :--- | :--- | :--- | :--- |
| **任务卡 (`TWIN-45.md`)** | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-45.md` | `revision: 1`, `7f2ac10f7b4a4bd263cf47e964423b1c2e5a157c62b47571b0a4849728a71e90` | 完全一致 | PASS |
| **ARCH 权威拆分方案** | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` | `revision: 4`, `6a51f088734b0a625276340b418925172b0046df11a483d49111e19546d24813` (ARCH `433026bf-a1ff-4863-8f3e-7a5f43b016ff`) | 完全一致 | PASS |
| **合并实施概要 (`protocol_input`)** | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` | `revision: 2`, `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec` | 完全一致 | PASS |
| **Debug 需求确认单** | `project-control/docs/planning/mc_th_debug_mode_requirement_confirmation_20261103.md` | `revision: 1`, `36ae2a6f8bc6ed13e6e89443fcca62fe882c841f2a65619ad735216d9cbacebe` | 完全一致 | PASS |
| **源码基线 (`mcu-p3`)** | `feat/soc-debug` `HEAD` | `a03aa9d9a371c4af985ee18e7c5a5c82c1b1c9e9` (`color-engine-mcu/` 与 `e051111e68dd61896ed42c0961153b167b8bca41` 零差异) | 完全一致 | PASS |
| **前置依赖 (`depends_on`)** | `TWIN-30` | `status: Done`, `blocked: false` | 已闭环 Done | PASS |
| **写范围白名单 (`allowed_paths`)** | `color-engine-mcu/io_toggle/src/bsp/usart.c`, `inc/usart.h`, `src/user/main.c`, `docs/evidence/twin/TWIN-45/**` | 严禁触碰 `src/app/minimc_proto.c`, `inc/minimc_proto.h`, `src/app/thermistor_adc.{c,h}`, `motion-controller-mcu/**`, `soc-ap/**`, `test_harness/**`, `boot/**` | 严格遵守 | PASS |

---

## 2. 交付产物与 SHA-256 清单

| 文件路径 | 变更说明 | SHA-256 |
| :--- | :--- | :--- |
| `mcu-p3/color-engine-mcu/io_toggle/inc/usart.h` | 定义 `TH_DEBUG_MODE_ENABLE (1)`、`TH_DBG_LINE_MAX_LEN (192U)`、`TH_DBG_STATE_INTERVAL_MS (500U)`，声明 `th_debug_set_enabled()`、`th_debug_is_enabled()`、`th_debug_write()`、`USART3_get_tx_drop_count()`、`USART3_get_tx_trunc_count()`、`th_debug_log_periodic_state()`，增加 C++ `extern "C"` 守卫 | `e75ad3ca99f760f4ddda607b4c1ba6df1c9edecb70d30539ef8f75ed522d43a1` |
| `mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c` | 保持 `USART1` (`921600`) 与 `USART3` (`115200` `DMA1_CH5` 非阻塞环形缓冲) 不变；在 `usart1_rx_pop_raw_byte()` 与 `usart1_send_raw()` 实现非阻塞 `[TH-DBG]` 日志观察器（覆盖 `dir=RX\|TX\|STATE\|ERR`），完善 `drop`/`trunc` 计数与周期状态输出，全部函数满足 $\le 50$ 行与 $\le 4$ 入参门禁 | `406f25e1b0c8f541b0befddb18a2e80b5112b210581aeeb9f3b1a0dad2045a5f` |
| `mcu-p3/color-engine-mcu/io_toggle/src/user/main.c` | 模块化拆分主函数（满足 $\le 50$ 行门禁），在主循环接入 `th_debug_log_periodic_state(current_tick)` 与 `USART3_forward_service()` | `ddffa6bfb36503a40cb7f8d577ec187ed3e0fb89a132f42e691ca83b8681f2dc` |
| `project-control/docs/evidence/twin/TWIN-45/runs/author_01/test_twin45_th_debug.c` | `TWIN-45` 主机端独立正反例单元测试套件（覆盖 `USART1` `921600` / `USART3` `115200` 初始化、`dir=RX\|TX\|STATE\|ERR` 日志、$\le 2\text{ Hz}$ 限频、`CRC_ERR`/`BAD_FRAME` 与 DMA 恢复、环形缓冲满 `drop`/`trunc` 非阻塞压测） | `400dfb29930f72eb39116aefc321607886ba5ee6f56da65a539114122b43fe00` |

---

## 3. 核心实现要点

1. **保持 TH 串口波特率与非阻塞 DMA 架构不变**：
   - `USART1` (`PB6`/`PB7`，TH↔MC 板间级联链路，`DMA1_CH4` TX / `DMA1_CH2` RX) 保持 `BAUDRATE1 = 921600` 8N1 不变。
   - `USART3` (`PC4`/`PC5`，宿主机 `COM6` TH Debug 串口，`DMA1_CH5` TX 非阻塞 2048B 环形缓冲 `USART3_write()`) 保持 `BAUDRATE2 = 115200` 8N1 不变。
2. **`[TH-DBG]` 全操作结构化日志（零侵入 `minimc_proto.c`）**：
   - 统一单行格式：
     `[TH-DBG] ts=<ms> dir=<RX|TX|STATE|ERR> node=<MC|TH> seq=<u8> cmd=0x<hex> status=<OK|ACK|NACK|CRC_ERR|EXEC> <kv_pairs...> drop=<u32> trunc=<u32>\r\n`
   - **级联请求接收 (`dir=RX`)**：在 `usart1_rx_pop_raw_byte()` 中挂载轻量级帧观察器 `th_dbg_observe_rx_byte()`，识别 MiniMC V2 帧头 (`0x55 0xAA`)、帧长、目标节点、`seq`、`cmd`、载荷参数（如 `nozzle_set`、`op=LOAD|UNLOAD|SELECT`、`slot`）与 CRC-16 校验。
   - **级联响应发送 (`dir=TX`)**：在 `usart1_send_raw()` 中挂载 `th_dbg_observe_tx_frame()`，解析发往 MC 的响应帧（`0x02` 版本、`0x04` Pong、`0x14` 温度上报 `nozzle_ddC`/`adc_raw`/`pullup_sel`/`fault`、`0x06` NACK）并输出对应 `dir=STATE` 与 `dir=TX status=ACK|NACK`。
   - **周期性与状态变更摘要 (`dir=STATE`)**：`th_debug_log_periodic_state(now_ms)` 严格按 `TH_DBG_STATE_INTERVAL_MS = 500U`（$\le 2\text{ Hz}$）限频，只读查询 `thermistor_adc_get_telemetry()` 与断料/进退丝状态，输出温度 (`nozzle_ddC=<i16> adc_raw=<u16> pullup_sel=<u8> fault=<u8>`) 与进退丝/料槽 (`op=<LOAD|UNLOAD|SELECT> slot=<u8> active_slot=<u8> filament_present_mask=0x<hex> step_state=<IDLE|FEEDING|RETRACTING|DONE|ERR>`) 状态行。
   - **异常与流控隔离 (`dir=ERR` & `drop`/`trunc`)**：遇到 CRC 校验失败或非法帧长时输出 `dir=ERR ... status=CRC_ERR|BAD_FRAME` 并复位观察器状态机，不影响 `USART1` 级联 DMA 恢复；单行超 `192B` 自动截断并以 `...\r\n` 结尾同时递增 `usart3_tx_trunc_count`；当 `USART3` 2048B 环形缓冲剩余空间不足时立即丢弃并递增 `usart3_tx_drop_count`，绝不阻塞 `USART1` 级联收发。

---

## 4. 编译验证与自动化测试日志

### 4.1 TH 固件交叉编译验证 (`build_th_firmware`)

执行命令：
```bash
cd mcu-p3/color-engine-mcu/io_toggle && make -j4 && make all -j4
```
关键输出：
```text
[VERSION][DEV] 生成 16bit 时间特征码: 0x1547 (V2.0.1-1547 1104)
[VERSION] 生成头文件: build/version_autogen.h
[CC] src/user/main.c
[CC] src/bsp/usart.c
[LD] build/fw_th.elf
--- Firmware Memory Size Report ---
   text	   data	    bss	    dec	    hex	filename
  73068	    844	  17924	  91836	  166bc	build/fw_th.elf
```
（注：验证 `build/fw_th.elf` / `.bin` / `.hex` 生成成功后已执行 `make clean` 清理 `build/` 目录，确保 Git 工作树干净。）

### 4.2 严格编译门禁 (`-Wall -Wextra -Wpedantic -Werror` & C++17 Header Check) 与契约对齐门禁

- `arm-none-eabi-gcc ... -Wall -Wextra -Wpedantic -Werror -std=gnu11 -c src/bsp/usart.c`：Exit Code `0`（0 警告、0 错误）。
- `arm-none-eabi-g++ ... -std=c++17 -Wall -Wextra -Werror -fsyntax-only -x c++ -c inc/usart.h`：Exit Code `0`。
- `python3 test_harness/static_checks/minimcproto/check_opcode_alignment.py --strict`：`[PASS] 全端契约完全对齐：CMD_NACK (0x06) 与载荷长度规范全量吻合！`（Exit Code `0`）。

### 4.3 `TWIN-45` 主机端独立正反例单元测试 (`test_twin45_th_debug.c`)

```text
========================================================================
TWIN-45 TH USART1 921600 Cascade & USART3 Non-Blocking [TH-DBG] Suite
========================================================================
[RUN ] test_usart1_921600_and_usart3_115200_init
[PASS] test_usart1_921600_and_usart3_115200_init
[RUN ] test_cascade_rx_and_tx_logging
[PASS] test_cascade_rx_and_tx_logging
[RUN ] test_periodic_state_rate_limit_2hz
[PASS] test_periodic_state_rate_limit_2hz
[RUN ] test_negative_crc_err_bad_frame_and_dma_recovery
[PASS] test_negative_crc_err_bad_frame_and_dma_recovery
[RUN ] test_negative_usart3_ring_full_drop_and_trunc_nonblocking
[PASS] test_negative_usart3_ring_full_drop_and_trunc_nonblocking
------------------------------------------------------------------------
All 5 TWIN-45 test suites PASSED!
========================================================================
```

---

## 5. 函数规模（$\le 50$ 行）与入参个数（$\le 4$ 个）静态自检表

| 所属文件 | 函数名称 | 起始-结束行 | 总跨度行数 (`<=50`) | 有效代码行 | 入参个数 (`<=4`) | 门禁结果 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `usart.c` | `th_dbg_rx_reset` | 118-123 | 6 | 6 | 0 | PASS |
| `usart.c` | `th_dbg_node_name` | 125-132 | 8 | 8 | 1 | PASS |
| `usart.c` | `th_debug_set_enabled` | 134-137 | 4 | 4 | 1 | PASS |
| `usart.c` | `th_debug_is_enabled` | 139-142 | 4 | 4 | 0 | PASS |
| `usart.c` | `USART3_get_tx_drop_count` | 144-147 | 4 | 4 | 0 | PASS |
| `usart.c` | `USART3_get_tx_trunc_count` | 149-152 | 4 | 4 | 0 | PASS |
| `usart.c` | `usart3_tx_free_space` | 154-163 | 10 | 10 | 0 | PASS |
| `usart.c` | `th_debug_write` | 165-187 | 23 | 23 | 2 | PASS |
| `usart.c` | `th_dbg_emit` | 189-217 | 29 | 29 | 2 | PASS |
| `usart.c` | `th_dbg_format_temp_kv` | 219-233 | 15 | 15 | 2 | PASS |
| `usart.c` | `th_dbg_format_filament_kv` | 235-250 | 16 | 16 | 2 | PASS |
| `usart.c` | `th_dbg_log_frame_err` | 252-268 | 17 | 17 | 3 | PASS |
| `usart.c` | `th_dbg_update_rx_filament_state` | 270-278 | 9 | 9 | 3 | PASS |
| `usart.c` | `th_dbg_handle_valid_rx_frame` | 280-324 | 45 | 42 | 2 | PASS |
| `usart.c` | `th_dbg_rx_step_sof` | 326-353 | 28 | 28 | 1 | PASS |
| `usart.c` | `th_dbg_finish_rx_crc` | 355-370 | 16 | 16 | 0 | PASS |
| `usart.c` | `th_dbg_observe_rx_byte` | 372-409 | 38 | 37 | 1 | PASS |
| `usart.c` | `th_dbg_log_tx_temp_report` | 411-422 | 12 | 12 | 3 | PASS |
| `usart.c` | `th_dbg_observe_tx_frame` | 424-471 | 48 | 47 | 2 | PASS |
| `usart.c` | `th_debug_log_periodic_state` | 473-507 | 35 | 32 | 1 | PASS |
| `usart.c` | `USART1_dma_rx_index_update` | 509-516 | 8 | 8 | 0 | PASS |
| `usart.c` | `USART1_dma_rx_init` | 518-546 | 29 | 25 | 0 | PASS |
| `usart.c` | `USART1_dma_tx_init` | 548-572 | 25 | 21 | 0 | PASS |
| `usart.c` | `MY_USART1_Init` | 574-602 | 29 | 24 | 0 | PASS |
| `usart.c` | `usart1_wait_tdc_with_timeout` | 604-611 | 8 | 8 | 0 | PASS |
| `usart.c` | `usart1_dma_transmit_blocking` | 613-636 | 24 | 22 | 2 | PASS |
| `usart.c` | `send_quick` | 638-650 | 13 | 13 | 1 | PASS |
| `usart.c` | `usart1_push_text_byte` | 652-664 | 13 | 13 | 1 | PASS |
| `usart.c` | `usart1_rx_pop_raw_byte` | 666-686 | 21 | 20 | 1 | PASS |
| `usart.c` | `usart1_send_raw` | 688-697 | 10 | 10 | 2 | PASS |
| `usart.c` | `USART1_has_byte` | 699-703 | 5 | 5 | 0 | PASS |
| `usart.c` | `USART1_get_byte` | 705-722 | 18 | 17 | 1 | PASS |
| `usart.c` | `USART1_dma_free` | 724-729 | 6 | 6 | 0 | PASS |
| `usart.c` | `reset_dma_usart1` | 731-741 | 11 | 11 | 0 | PASS |
| `usart.c` | `USART1_send_string` | 743-750 | 8 | 8 | 1 | PASS |
| `usart.c` | `USART1_loopback_test` | 752-761 | 10 | 10 | 0 | PASS |
| `usart.c` | `MX_USART1_UART_Init` | 763-766 | 4 | 4 | 0 | PASS |
| `usart.c` | `USART1GetDataToUsart3` | 768-776 | 9 | 9 | 0 | PASS |
| `usart.c` | `USART1_diagnose_report` | 778-791 | 14 | 13 | 0 | PASS |
| `usart.c` | `USART1_get_dma_overflow_count` | 793-796 | 4 | 4 | 0 | PASS |
| `usart.c` | `usart1_flow_control_check` | 798-814 | 17 | 16 | 0 | PASS |
| `usart.c` | `usart1_snapshot_rx_ring` | 816-841 | 26 | 26 | 1 | PASS |
| `usart.c` | `usart1_check_response` | 843-868 | 26 | 26 | 1 | PASS |
| `usart.c` | `usart1_send_xon` | 870-879 | 10 | 10 | 0 | PASS |
| `usart.c` | `usart1_send_xoff` | 881-890 | 10 | 10 | 0 | PASS |
| `usart.c` | `usart1_check_frame_complete` | 892-915 | 24 | 24 | 0 | PASS |
| `usart.c` | `usart1_extract_frame_payload` | 917-930 | 14 | 14 | 4 | PASS |
| `usart.c` | `usart1_parse_frame` | 932-965 | 34 | 34 | 2 | PASS |
| `usart.c` | `USART3_dma_rx_index_update` | 967-974 | 8 | 8 | 0 | PASS |
| `usart.c` | `USART3_dma_rx_init` | 976-1003 | 28 | 24 | 0 | PASS |
| `usart.c` | `USART3_dma_tx_init` | 1005-1032 | 28 | 23 | 0 | PASS |
| `usart.c` | `MY_USART3_Init` | 1034-1072 | 39 | 33 | 0 | PASS |
| `usart.c` | `usart3_dma_tx_kick` | 1074-1097 | 24 | 23 | 0 | PASS |
| `usart.c` | `usart3_ring_push_bytes` | 1099-1116 | 18 | 17 | 2 | PASS |
| `usart.c` | `USART3_write` | 1118-1138 | 21 | 21 | 2 | PASS |
| `usart.c` | `USART3_send_byte` | 1140-1143 | 4 | 4 | 1 | PASS |
| `usart.c` | `USART3_flush` | 1145-1158 | 14 | 14 | 0 | PASS |
| `usart.c` | `USART3_dma_tx_isr_handler` | 1160-1179 | 20 | 18 | 0 | PASS |
| `usart.c` | `USART3_has_byte` | 1181-1185 | 5 | 5 | 0 | PASS |
| `usart.c` | `USART3_get_byte` | 1187-1204 | 18 | 17 | 1 | PASS |
| `usart.c` | `USART3_dma_free` | 1206-1211 | 6 | 6 | 0 | PASS |
| `usart.c` | `reset_dma_usart3` | 1213-1219 | 7 | 7 | 0 | PASS |
| `usart.c` | `USART3_send_string` | 1221-1228 | 8 | 8 | 1 | PASS |
| `usart.c` | `USART3_get_line` | 1230-1264 | 35 | 35 | 2 | PASS |
| `usart.c` | `USART3_receive_line_and_forward` | 1266-1279 | 14 | 14 | 2 | PASS |
| `usart.c` | `USART3_forward_service` | 1281-1289 | 9 | 9 | 0 | PASS |
| `usart.c` | `USART3_forward_command` | 1291-1300 | 10 | 10 | 2 | PASS |
| `usart.c` | `USART3_get_forward_drop_count` | 1302-1305 | 4 | 4 | 0 | PASS |
| `main.c` | `main_init_peripherals` | 24-49 | 26 | 22 | 0 | PASS |
| `main.c` | `main_log_startup_banner` | 51-66 | 16 | 15 | 0 | PASS |
| `main.c` | `main_poll_periodic_tasks` | 68-85 | 18 | 16 | 1 | PASS |
| `main.c` | `main` | 87-99 | 13 | 12 | 0 | PASS |
