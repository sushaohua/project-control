# TWIN-44 第三轮修正与自检证据报告 (`run_id: author_03`)

## 1. 接单核对回执（`run_id: author_03`）

| 核对项 | 期望值 / 权威契约 | 实测核对结果 | 状态 |
| :--- | :--- | :--- | :--- |
| 任务卡 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-44.md` (`revision: 1`, `run_id: author_03`) | 一致 | PASS |
| 执行角色与会话 | `ENG-MC` (`8ca47c46-1cd8-4f82-955a-9742b6988ded`), `run_id: author_03` | 一致 | PASS |
| 第二轮独立 QA 报告 | `project-control/docs/evidence/twin/TWIN-44/runs/qa_02/` (Codex session `01a1a4ae-918f-74b0-a813-e61683b1cfc3`) | 已精读全部 3 项发现并 100% 闭环 | PASS |
| `ARCH` 权威技术拆分方案 | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 8`, SHA-256: `dfcd39b56ed1a93c58faf9b62ebe2d4adaa4eecb9180d521ba3f97b29294731d`) | 第 `1.3.4` 节裁决 A/B/C 完全对齐 | PASS |
| `protocol_input` | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` (`revision: 2`, SHA-256: `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec`) | 一致 | PASS |
| 修改范围 (`allowed_paths`) | 严格仅限 `mcu-p3/motion-controller-mcu/project/src/{minimc_proto.c,test_twin44_mc_debug.c}`, `inc/minimc_proto.h`, `project-control/docs/evidence/twin/TWIN-44/**` | `git diff e051111e... d2e46955...` 严格只有 3 个文件，恢复 `main.c` 为基线零 diff | PASS |
| 新候选提交 (`candidate_commit`) | `mcu-p3` (`feat/soc-debug`) = `d2e469559081616f6312ecbabf8d6b69a7e92e3a` | 已推送至 `origin/feat/soc-debug` | PASS |

---

## 2. 针对独立 QA (`qa_02`) 三项发现的逐项整改闭环（对照 `ARCH` `revision: 8` 第 1.3.4 节）

### 2.1 裁决 A：保持诚实 MiniMC V2 命令响应语义，严禁伪造未实现命令的假 ACK
1. 在 `minimc_proto.c` 的 `handle_mc_query()` 中，严格只处理基线 `e051111e68dd61896ed42c0961153b167b8bca41` 已真实实现的 5 条命令：
   - `MINIMC_CMD_GET_VERSION (0x01)` $\rightarrow$ `build_version_resp()`
   - `MINIMC_CMD_PING (0x03)` $\rightarrow$ `build_pong_resp()`
   - `MINIMC_CMD_GET_TEMP (0x14)` $\rightarrow$ `build_temp_resp()`
   - `MINIMC_CMD_POS_QUERY (0x16)` $\rightarrow$ `build_pos_resp()`
   - `MINIMC_CMD_LEVEL_GRID_QUERY (0x18)` $\rightarrow$ `build_level_grid_resp()`
2. 对任何未在 `minimc_proto.c` 实现业务执行的命令码（如 `0x10 SET_TEMP`、`0x15`、`0x7E`、`0x99` 等），诚实返回 `build_nack_resp(seq, 0x04U, resp, &resp_len)`，并输出 `[MC-DBG] ... dir=ERR node=MC seq=<seq> cmd=0x<XX> status=BAD_CMD err_code=0x04` 与 `[MC-DBG] ... dir=TX node=MC seq=<seq> cmd=0x06 status=NACK err_code=0x04`，绝不回传伪造的温度或位置 ACK。
3. 在 `minimc_proto.h` / `minimc_proto.c` 提供非侵入式业务状态观测通知接口（均满足 $\le 50$ 行、$\le 4$ 个入参）：
   - `void mc_debug_notify_temp_target(int16_t nozzle_set_ddC, int16_t bed_set_ddC);`（10 行，2 参）
   - `void mc_debug_notify_motion(const char *op, uint8_t axes_mask, uint16_t feed);`（13 行，3 参）
   - `void mc_debug_notify_filament(const char *op, uint8_t slot, uint8_t present_mask, const char *step_state);`（14 行，4 参）
   - `void mc_debug_notify_job(uint8_t job_state_id, uint16_t progress_permille, uint8_t ack_seq);`（10 行，3 参）

### 2.2 裁决 B：恢复 `main.c` 为基线零 diff，将排空与周期状态内聚于 `minimc_proto_poll()`
- 基线 `e051111e68dd61896ed42c0961153b167b8bca41` 的 `main.c` 已在初始化阶段调用 `minimc_proto_init()` 并在 `while(1)` 主循环调用 `minimc_proto_poll()`；
- `minimc_proto_poll()` 内部自包含调用 `mc_debug_log_periodic_state(now_ms)` 与 `mc_debug_poll_drain()`；
- 将 `motion-controller-mcu/project/src/main.c` 恢复至基线 `e051111e68dd61896ed42c0961153b167b8bca41`（零 diff），确保候选变更的每一个生产 `.c` 文件（`minimc_proto.c`）100% 纳入沙箱 `gcc` 编译与测试。

### 2.3 裁决 C：在 `test_twin44_mc_debug.c` 中补齐二进制响应帧校验与三项故障后恢复断言
1. **二进制响应帧（Wire Response）断言**：捕获 `DMA1_CHANNEL2` 发送帧，验证 `0x01`/`0x03`/`0x14`/`0x16`/`0x18` 返回真实响应帧，且未实现命令 `0x10` 返回 `MINIMC_CMD_NACK (0x06)` (`err_code == 0x04`)。
2. **恢复断言 A（环形缓冲满 $\rightarrow$ 排空 $\rightarrow$ 新日志恢复）**：写满 `2048B` 触发 `drop_count == 1` 后，调用 `mc_debug_poll_drain()` 排空，紧接着写入 `"[MC-DBG] RING_RECOVERY_OK\r\n"` 并排空，断言返回 `true`、`drop_count` 保持 `1` 不变且新日志完整出现在串口输出中。
3. **恢复断言 B（`usart2_tx_busy = 1` 发送失败 $\rightarrow$ 恢复空闲 $\rightarrow$ 下一帧查询成功）**：模拟 `usart2_tx_busy = 1` 触发 `minimc_proto_send` 返回 `false` 并记录 `status=TX_ERR err_code=0x06`（无伪 ACK）后，恢复 `usart2_tx_busy = 0` 并发送下一帧 `GET_TEMP (0x14)`，断言成功发出 `TEMP_REPORT` 响应帧且输出 `dir=STATE status=OK` 与 `dir=TX status=ACK`。
4. **恢复断言 C（TH 级联超时 $\rightarrow$ 下一帧级联请求 + TH 应答恢复成功）**：模拟 `seq=31` TH 级联超时（`status=TIMEOUT`）后，紧接着发送 `seq=32` `dest=TH` 请求并注入合法 TH `VERSION_REPORT (0x02)` 应答，断言成功转发回 AP 并输出 `dir=RELAY_RX status=ACK` 与 `dir=TX node=TH status=ACK`。

---

## 3. 交付物与 SHA-256 清单

| 文件路径 | SHA-256 |
| :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | `38a7c4842356d13c3870567ae4fc8284b64e108c2bae8588411fb9e0ccf008e4` |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | `7986230ecaa81e7bfc4d255bbfa9573968ac8bb0f5a55decd86b041320e45d5c` |
| `mcu-p3/motion-controller-mcu/project/src/test_twin44_mc_debug.c` | `fb4a08300a7b6d4239bb1eeaf58c9dbfa1257dedc493e1fb62b43e305dc24188` |

---

## 4. 受控沙箱命令与宿主机交叉编译验证日志

### 4.1 沙箱单元测试验证命令 (`build_and_test_mc_debug_and_921600`)
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
[RUN ] test_ring_buffer_trunc_drop_and_recovery
[PASS] test_ring_buffer_trunc_drop_and_recovery
[RUN ] test_honest_minimc_v2_queries_and_nack
[PASS] test_honest_minimc_v2_queries_and_nack
[RUN ] test_non_intrusive_notify_and_fault_sync
[PASS] test_non_intrusive_notify_and_fault_sync
[RUN ] test_tx_fail_suppresses_ack_and_recovers
[PASS] test_tx_fail_suppresses_ack_and_recovers
[RUN ] test_relay_timeout_crc_err_and_recovery
[PASS] test_relay_timeout_crc_err_and_recovery
------------------------------------------------------------------------
All 6 TWIN-44 test suites (including post-error recovery) PASSED!
========================================================================
```

### 4.2 宿主机 `arm-none-eabi-gcc` 交叉编译 (`make -j4`)
```text
[ 97%] Building C object CMakeFiles/Marlin_AT32.dir/project/src/minimc_proto.c.obj
[ 98%] Linking C executable Marlin_AT32.elf
Memory region         Used Size  Region Size  %age Used
           FLASH:      375852 B       896 KB     40.96%
             RAM:       28864 B       384 KB      7.34%
Generating Marlin_AT32.bin and Marlin_AT32.hex
[100%] Built target Marlin_AT32
```
（验证后已清理 `build/` 目录，确保工作树干净。）

---

## 5. C/C++ 编码规范硬性门禁静态自检表（全部函数 $\le 50$ 行、$\le 4$ 个入参）

- **最大值统计**：`minimc_proto.c` 全部函数最大 47 行、最多 4 入参；`test_twin44_mc_debug.c` 全部函数最大 48 行、最多 4 入参；零动态堆分配（无 `malloc`/`free`）。

| 文件 | 函数名 | 起止行号 | 行数 ($\le 50$) | 入参个数 ($\le 4$) | 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `minimc_proto.c` | `mc_dbg_sync_runtime_state` | 621-631 | 11 | 0 | PASS |
| `minimc_proto.c` | `build_temp_resp` | 633-674 | 42 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_log_tx_err` | 917-925 | 9 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_emit_tx_or_err` | 927-940 | 14 | 3 | PASS |
| `minimc_proto.c` | `mc_dbg_emit_state_and_tx` | 942-955 | 14 | 4 | PASS |
| `minimc_proto.c` | `mc_debug_notify_temp_target` | 974-983 | 10 | 2 | PASS |
| `minimc_proto.c` | `mc_debug_notify_motion` | 985-997 | 13 | 3 | PASS |
| `minimc_proto.c` | `mc_debug_notify_filament` | 999-1012 | 14 | 4 | PASS |
| `minimc_proto.c` | `mc_debug_notify_job` | 1014-1023 | 10 | 3 | PASS |
| `minimc_proto.c` | `handle_mc_core_queries` | 1025-1057 | 33 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_motion_and_level` | 1059-1084 | 26 | 4 | PASS |
| `minimc_proto.c` | `handle_mc_query` | 1086-1111 | 26 | 2 | PASS |
| `minimc_proto.c` | 其余全部 30 个函数 | 32-1353 | 最大 47 | 最多 4 | PASS |
| `test_twin44_mc_debug.c` | 全部 21 个函数 | 29-428 | 最大 48 | 最多 4 | PASS |
