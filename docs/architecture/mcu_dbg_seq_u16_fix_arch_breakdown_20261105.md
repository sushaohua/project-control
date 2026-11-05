---
id: ARCH-BREAKDOWN-MCU-DBG-SEQ-U16-20261105
title: "MC/TH 串口调试日志 [MC-DBG]/[TH-DBG] 16-bit seq 截断修复与 MC 本地级联号段隔离架构拆解"
revision: 1
status: Approved-By-User
date: "2026-11-05"
author_role: ARCH
author_session: ef428595-f4d6-46a7-9d12-07e1fd215641
target_tasks:
  - TWIN-56
source_baselines:
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
---

# MC/TH 串口调试日志 `[MC-DBG]` / `[TH-DBG]` 16-bit `seq` 截断修复与 MC 本地级联号段隔离架构拆解

## 1. 背景与源码基线

在执行 `TWIN-54` 物理硬件烧录与实机闭环验收前，针对用户提出的“`seq` 在协议中为 16-bit，但在 `[MC-DBG]` 与 `[TH-DBG]` 日志中未见大数值”问题，经 `ARCH` 只读审查确认：
1. **物理串口二进制协议层（MiniMCProto V2）**：`AP` (`soc-ap`)、`MC` (`mcu-p3/motion-controller-mcu`) 与 `TH` (`mcu-p3/color-engine-mcu/io_toggle`) 在 12B 帧头偏移 `byte[8..9]` 上均已完整使用 **16-bit 小端无符号整数 (`uint16_t`)** 进行组帧、转发与响应校验。
2. **调试日志层 8-bit 截断缺陷**：
   - `MC` 端 `minimc_proto.c` 中的 `mc_dbg_meta_t.seq`、`mc_dbg_state_t.ack_seq`、`s_relay_seq` 被定义为 `uint8_t`，且在提取帧序号时仅读取了低字节 `frame[8]`（或 `(uint8_t)(seq & 0xFFU)`），导致超过 `255` 的 16-bit `seq` 在 `[MC-DBG]` 中被模 256 截断；
   - `TH` 端 `usart.c` 中的 `th_dbg_meta_t.seq`、`th_dbg_state_t.last_seq` 被定义为 `uint8_t`，且旁路帧观察器仅读取了低字节 `frame[8]` / `data[8]`，导致超过 `255` 的 16-bit `seq` 在 `[TH-DBG]` 中被模 256 截断。
3. **MC 本地级联序列号起始偏移被重置缺陷**：
   - `MC` 端 `minimc_proto.c#L164` 定义了 `static uint16_t s_mc_th_seq = 0x0100U;`（设计初衷为从 `256 (0x0100)` 起步，以便在日志中一眼区分“AP 下发的请求帧”与“MC 本地 Marlin 队列生成的 0x1C 级联帧”），但在 `minimc_proto_init()` (`#L2303`) 中被误重置为 `s_mc_th_seq = 0U;`。

### 1.1 锁定源码基线

| 仓库 | 当前 HEAD Commit | 说明 |
| :--- | :--- | :--- |
| `mcu-p3` | `016e1236af75f6f19282d6b000f4b1b68bd96cc3` | `TWIN-56` 修改目标仓库（MC 与 TH 调试日志 `uint16_t seq` 修复及宿主自检更新） |
| `test_harness` | `d14ed04321c6d4f5ddb35a8801604a8af53b5b60` | 只读兼容基线（见第 3 节核查结论，无需修改） |

---

## 2. `mcu-p3` 精确修改规范（任务卡 `TWIN-56`）

### 2.1 MC 端（`mcu-p3/motion-controller-mcu`）修改点

1. **[`project/inc/minimc_proto.h`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h#L261)**：
   - 将公开通知接口声明由：
     `void mc_debug_notify_job(uint8_t job_state_id, uint16_t progress_permille, uint8_t ack_seq);`
     更新为：
     `void mc_debug_notify_job(uint8_t job_state_id, uint16_t progress_permille, uint16_t ack_seq);`
   - 注：`minimc_job_resp_t.ack_seq`（`#L190`，二进制协议 8B 载荷内部字段）保持 `uint8_t` 不变，以维持与 `soc-ap/services/forward/forward_protocol.h` 的二进制载荷 ABI 兼容。

2. **[`project/src/minimc_proto.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c)**：
   - **结构体与静态状态升位（`#L119-L164`）**：
     - `mc_dbg_meta_t.seq`（`#L122`）：`uint8_t seq;` $\rightarrow$ `uint16_t seq;`；
     - `mc_dbg_state_t.ack_seq`（`#L138`）：`uint8_t ack_seq;` $\rightarrow$ `uint16_t ack_seq;`；
     - `s_relay_seq`（`#L158`）：`static uint8_t s_relay_seq = 0U;` $\rightarrow$ `static uint16_t s_relay_seq = 0U;`。
   - **日志辅助函数与通知函数形参升位**：
     - `mc_dbg_log_frame_err()`（`#L490-L502`）：从 `hdr[8..9]` 提取完整 16-bit 序号 `const uint16_t seq = (uint16_t)hdr[8] | (uint16_t)((uint16_t)hdr[9] << 8U);` 填入 `meta.seq`；
     - `mc_dbg_log_tx_err()`（`#L959`）：形参 `uint8_t seq_u8` $\rightarrow$ `uint16_t seq`；
     - `mc_dbg_emit_state_and_tx()`（`#L984`）：形参 `uint8_t seq_u8` $\rightarrow$ `uint16_t seq`；
     - `mc_debug_notify_job()`（`#L1056`）：形参 `uint8_t ack_seq` $\rightarrow$ `uint16_t ack_seq`；
     - `mc_apply_gcode_side_effects()`（`#L1595`）：形参 `uint8_t seq_u8` $\rightarrow$ `uint16_t seq`；
     - `sync_th_temp_and_gcode_state()`（`#L1930`）与 `sync_th_filament_resp_state()`（`#L1977`）：形参 `uint8_t seq_u8` $\rightarrow$ `uint16_t seq`。
   - **命令处理与级联收发日志消除 8-bit 截断（`#L1157-L2145`）**：
     - 在 `send_mc_nack()`、`send_pos_query_ack()`、`send_level_grid_ack()`、`trigger_mc_to_th_cascade()`、`handle_mc_set_temp()`、`handle_mc_home()`、`handle_mc_move()`、`handle_mc_job_control()`、`handle_mc_motion_stop()`、`handle_mc_filament()`、`handle_mc_gcode_exec()`、`handle_mc_core_queries()`、`handle_mc_motion_and_level()`、`minimc_proto_send_th_gcode()` 中，将传入 `mc_dbg_meta_t`、`s_dbg_state.ack_seq`、`s_relay_seq` 及调试辅助函数的序列号统一改为完整 16-bit `seq`（仅在 `trigger_mc_to_th_cascade()` `#L1231` 写帧头低字节和 `handle_mc_job_control()` `#L1485` 填 `resp_pay.ack_seq` 时保留 `(uint8_t)(seq & 0xFFU)`）；
     - 在 `handle_th_relay_req()`（`#L1803`）、`handle_ap_frame()`（`#L1839`）、`handle_th_frame()`（`#L2024`, `#L2029`）中，统一使用 `const uint16_t seq = (uint16_t)frame[8] | (uint16_t)((uint16_t)frame[9] << 8U);` 提取完整 16-bit 帧序号用于 `[MC-DBG]` 输出。
   - **恢复 MC 本地级联初始号段（`#L2303`）**：
     - 在 `minimc_proto_init(void)` 中，将 `s_mc_th_seq = 0U;` 修改为 `s_mc_th_seq = 0x0100U;`，使 MC 本地通过 `minimc_proto_send_th_gcode()` 发往 TH 的级联帧从 `257 (0x0101)` 开始递增，与 AP 从 `1` 开始的序列号形成清晰号段区分。

3. **[`project/src/test_twin44_mc_debug.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c)**：
   - 将 `s_test_seq`（`#L52`）、`inject_th_custom_frame()`（`#L195`）与 `inject_th_response_frame()`（`#L221`）中的 `seq` 类型由 `uint8_t` 升位为 `uint16_t`，并写入 `frame[8] = (uint8_t)(seq & 0xFFU); frame[9] = (uint8_t)((seq >> 8U) & 0xFFU);`；
   - 在 `test_twin47_job_filament_level_gcode()`（`#L668-L673`）中：
     - 验证 `minimc_proto_send_th_gcode("M104 S205\r\n", 11U, 1U)` 发送帧的 16-bit `seq` 为 `0x0101U` (`257U`)，且注入 `seq=0x0101U` 的 TH 响应后 `[MC-DBG]` 输出 `dir=RELAY_TX node=TH seq=257 cmd=0x1C status=EXEC` 与 `dir=RELAY_RX node=TH seq=257 cmd=0x1C status=ACK`；
     - 新增对 AP 请求 `seq > 255`（如 `s_test_seq = 300U` $\rightarrow$ `seq=301`）的 `0x13 JOB_CONTROL` 测试断言，验证 `[MC-DBG]` 输出 `seq=301` 与 `ack_seq=301` 无 8-bit 截断。

---

### 2.2 TH 端（`mcu-p3/color-engine-mcu/io_toggle`）修改点

1. **[`src/bsp/usart.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c)**：
   - **结构体升位（`#L59-L79`）**：
     - `th_dbg_meta_t.seq`（`#L62`）：`uint8_t seq;` $\rightarrow$ `uint16_t seq;`；
     - `th_dbg_state_t.last_seq`（`#L76`）：`uint8_t last_seq;` $\rightarrow$ `uint16_t last_seq;`。
   - **旁路帧观察器与发送日志消除 8-bit 截断**：
     - `th_dbg_log_frame_err()`（`#L282-L299`）：使用 `const uint16_t seq = (uint16_t)hdr[8] | (uint16_t)((uint16_t)hdr[9] << 8U);` 填入 `meta.seq`；
     - `th_dbg_handle_valid_rx_frame()`（`#L377-L399`）：使用 `const uint16_t seq = (uint16_t)frame[8] | (uint16_t)((uint16_t)frame[9] << 8U);` 更新 `s_th_dbg_state.last_seq` 与 `rx_meta.seq`；
     - `th_dbg_log_tx_temp_report()`（`#L486`）与 `th_dbg_log_tx_control_resp()`（`#L505`）：形参 `uint8_t seq_u8` $\rightarrow$ `uint16_t seq`；
     - `th_dbg_observe_tx_frame()`（`#L532-L577`）：将 `#L543` 的 `const uint8_t seq_u8 = data[8];` 修改为 `const uint16_t seq = (uint16_t)data[8] | (uint16_t)((uint16_t)data[9] << 8U);` 并传给所有 `[TH-DBG]` `STATE`/`TX`/`ERR` 日志。

2. **[`src/user/test_twin45_th_debug.c`](file:///home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c)**：
   - 将 `inject_minimc_req()`（`#L418-L430`）的第一形参由 `uint8_t seq` 升位为 `uint16_t seq`，写入 `frame[8] = (uint8_t)(seq & 0xFFU); frame[9] = (uint8_t)((seq >> 8U) & 0xFFU);`；
   - 在 `test_twin48_gcode_queue_and_send_quick()`（`#L840-L845`）中，使用 16-bit 序列号 `0x0101U` (`257U`) 注入 `0x1C GCODE_EXEC` 请求，断言 `[TH-DBG]` 输出 `dir=RX node=TH seq=257 cmd=0x1C`、`dir=STATE node=TH seq=257 cmd=0x1C` 与 `dir=TX node=TH seq=257 cmd=0x1C status=ACK exec_status=0`，证明 TH 端 16-bit `seq` > 255 原样输出无截断。

---

## 3. `test_harness` 兼容性只读核查结论

经只读核查 `test_harness`（基线 `d14ed04321c6d4f5ddb35a8801604a8af53b5b60`）：
1. **[`test_harness/hil/tools/debug_reconciliation_probe.py`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/debug_reconciliation_probe.py#L47-L51)**：
   - 正则表达式 `HEADER_RE` 使用 `seq=(?P<seq>\d+)` 匹配任意十进制非负整数，并通过 `parse_int_value()` 解析为 Python `int`，对 `0..65535` 范围内的 16-bit `seq` 与 `ack_seq` 天然 100% 兼容。
2. **[`test_harness/test_cases/twin/twin46_mc_bridge.c`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/twin/twin46_mc_bridge.c) 与 [`twin46_th_bridge.c`](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/twin/twin46_th_bridge.c)**：
   - 两个桥接文件完全通过 921600 原始串口帧驱动 `minimc_proto.c` 与 `usart.c`，未直接调用 `mc_debug_notify_job()`，亦未对 `[MC-DBG]` / `[TH-DBG]` 的 `seq` 做 8-bit 截断假设。
3. **结论**：`test_harness` 无需修改代码，在 `TWIN-56` 验证阶段可直接作为回归测试套件运行。

---

## 4. 任务卡 `TWIN-56` 边界、门禁与验证命令

### 4.1 允许写入路径（`allowed_paths` / `write_scope`）
- 目标仓库：`mcu-p3`（角色：`ENG-MC`）
- 允许修改路径：
  - `motion-controller-mcu/project/inc/minimc_proto.h`
  - `motion-controller-mcu/project/src/minimc_proto.c`
  - `motion-controller-mcu/project/src/test_twin44_mc_debug.c`
  - `color-engine-mcu/io_toggle/src/bsp/usart.c`
  - `color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c`

### 4.2 编码门禁
1. 全部修改或新增的自研 C 函数必须严格满足 **函数体 $\le 50$ 行**、**入参 $\le 4$ 个**、**卫语句空指针校验**、**零动态内存分配**；
2. 全部新增或修改的函数注释/说明性注释必须使用中文；
3. 严禁破坏 MiniMCProto V2 线缆二进制帧格式与 CRC-16 校验逻辑。

### 4.3 验证命令（`verification.commands`）
1. **Docker 沙箱宿主单元测试与共享库桥接回归**：
   ```bash
   gcc -std=c11 -O2 -Wall -Wextra -Werror \
     -I/workspace/mcu-p3/motion-controller-mcu/project/inc \
     /workspace/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c \
     /workspace/mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c \
     -o /tmp/test_twin44_mc_debug && /tmp/test_twin44_mc_debug
   ```
   ```bash
   gcc -std=c11 -O2 -Wall -Wextra -Werror \
     -I/workspace/mcu-p3/color-engine-mcu/io_toggle/inc \
     /workspace/mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c \
     /workspace/mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c \
     /workspace/mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c \
     /workspace/mcu-p3/color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c \
     -o /tmp/test_twin45_th_debug && /tmp/test_twin45_th_debug
   ```
   ```bash
   python3 /workspace/test_harness/hil/tools/debug_reconciliation_probe.py --self-test
   ```
2. **宿主机 ARM 交叉编译（生成待烧录生产固件 `fw_mc.bin` 与 `fw_th.bin`）**：
   - `make -C mcu-p3/motion-controller-mcu/project/MDK_V5 clean all`
   - `make -C mcu-p3/color-engine-mcu/io_toggle/mdk_v5 clean all`
