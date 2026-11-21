# 独立交接单：TH App (`color-engine-mcu`) `0x17` 急停命令 `0B ACK` 契约偏差与解除语义修复 (`TH-ESTOP-01`)

## 修订历史

| 版本 | 修订时间 | 修订人 | 变更摘要 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| `v1.0` | `2026-11-21 17:15 +0800` | `AI (Antigravity-CLI) - COORD` | 基于 `SLICE-08 (r18b)` 真机 HIL 实测定位 `TH App` 对 `0x17` (`plen=1`) 返回 `0B ACK` 导致 `Forward` 报 `-8` 超时及 `stop_mode=0` 误入队 `M112` 的精确源码根因，生成下一轮修复交接单 | 待下一轮（建议并入 `SLICE-09` P1 控制接入）审批排期 |

---

## 1. 现象与实板证据锚点

- **触发场景**：在 `192.168.1.101`（`printer-soc@6f28023f`、`MC@0xA64BFFBF`、`TH@0x7B623D9A / 0xA64BFFBF`）执行 `AC-05` 调用 D-Bus `org.aisoc.DeviceInterface.EmergencyStop(byte:1)`。
- **实测表现**：
  - `MC`（节点 `0x02`）正常执行 `quickStop()`、置 `is_paused=1U` 并在 `~66ms` 内返回标准 `4B CMD_ACK`（随后的 `0x17 [0x00]` 亦正常将 `MC` `is_paused` 清回 `0U`）；
  - `TH`（节点 `0x03`）在 `200ms` 窗口届满时报 `[FWD QUERY] target_node=3 sequence_id=15 elapsed_ms=200 error_code=-8`（见 [03_ac05_and_ac03_ota.log](../evidence/SLICE-08/hil_r18b/03_ac05_and_ac03_ota.log) 与 `forward.log`）。
  - 宿主机 `test_ota_e2e.py` 未提前暴露该问题，是因为 Python 孪生模拟器对双节点 `0x17` 均按契约返回了 `4B CMD_ACK`。

---

## 2. 经物理核实的源码根因（100% 锁定）

对比 `Forward` 控制表、`MC App` 与 `TH App` 三端实码：

1. **AP `Forward` 契约要求（`printer-soc/services/forward/forward_control.cpp:27,179-191`）**：
   - `COMMANDS[]` 登记 `{0x17U, 0x00U, 1U, 4U, false}`：固定发送 `1B` 请求载荷（`reason_code / stop_mode`：`1=急停锁存`，`0=解除锁存`），且严格校验响应命令为 `0x00 (CMD_ACK)`、**响应载荷长度固定为 `4B`（`minimc_ack_payload_t`）**；
   - `forward_service_emergency_stop()` 先单播 `0x02 (MC)`，收到 `4B ACK` 后延时 `45ms` 再单播 `0x03 (TH)`。
2. **MC App 正确实现（`mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:2099-2136`）**：
   - `handle_mc_motion_stop()` 根据 `frame[MINIMC_HEADER_SIZE] == 1U` 区分急停置位（`is_paused = 1U`）与解除（`is_paused = 0U`），并统一调用 `send_mc_ack_frame(MINIMC_CMD_ACK, seq, &ack_pay, sizeof(ack_pay))` 返回 **`4B CMD_ACK`**。
3. **TH App 存在两处偏差（`mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c:642-672`）**：
   - **偏差 A（`0B ACK` 导致 `-8` 超时）**：第 666–670 行写有旧兼容分支：
     ```c
     if (plen == 1U)
     {
         init_th_resp_hdr(out_buf, src_id, MINIMC_CMD_ACK, seq);
         return finalize_th_resp_frame(out_buf, 0U);
     }
     return build_ack_resp(src_id, seq, out_buf);
     ```
     当收到标准 `1B` 载荷请求时返回了 **`0B` 载荷的 `CMD_ACK`**，被 `Forward` 的 `min_resp_len=4, max_resp_len=4` 校验过滤丢弃，最终表现为 `200ms` `SERIAL_TIMEOUT (-8)`。
   - **偏差 B（`stop_mode == 0` 解除时误动作）**：第 658–661 行未区分 `plen == 1U && frame[MINIMC_HEADER_SIZE] == 0U`（解除急停），在解除请求时仍无条件执行 `quickStop()`、清零目标温度并调用 `th_control_enqueue_gcode("M112", 4U, true)`。

---

## 3. 下一轮最小修复建议与验收标准

- **责任角色 / 仓库 / 分支**：`ENG-MCU` / `mcu-p3`（锁定分支 `feat/soc-debug`）
- **预计 Diff Budget**：2 个文件（`color-engine-mcu/io_toggle/src/app/minimc_proto.c`、`color-engine-mcu/tests/` 对应协议单测），增删 $\le 30$ 行：
  1. 删除 `handle_th_motion_stop()` 第 666–670 行的 `0U` 空载荷特判，对 `plen <= 1U` 的非广播 `WANTS_ACK` 请求统一调用 `build_ack_resp(src_id, seq, out_buf)` 返回标准 **`4B CMD_ACK`**（与 `MC`、`Forward`、`test_helix_screen_integration.py:265` 对齐）；
  2. 当 `plen == 1U && frame[MINIMC_HEADER_SIZE] == 0U` 时按“解除急停锁存”处理（恢复允许控制态，不重复入队 `"M112"` 或清零温度；仅在 `plen == 0U || frame[MINIMC_HEADER_SIZE] == 1U` 时执行急停关断与 `"M112"`）。
- **验收判据 (`Pass Criteria`)**：
  1. `color-engine-mcu` 宿主机单测覆盖 `0x17 [0x01]` 与 `0x17 [0x00]` 均返回 `18B` 帧（含 `4B` `CMD_ACK` 载荷且末 2 字节为 `0x0000`），且 `0x00` 不触发 `"M112"`；
  2. 真机串口 OTA 更新 `fw_th.bin` 后，调用 `org.aisoc.DeviceInterface.EmergencyStop(byte:1)` 与 `EmergencyStop(byte:0)` 均返回 `int32 0`，`GetSnapshot` 状态完成 `IDLE -> EMERGENCY_STOP -> IDLE` 闭环。
