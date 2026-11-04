# TWIN-50 (`author_01`, `INTEGRATOR`) 测试夹具去旁路净化与 921600 垂直端到端 PTY 联调交付报告

## 1. 任务与规则溯源 (`read_sources`)

- **任务卡**：[TWIN-50.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-50.md) (`run_id: author_01`)
- **规则入口与版本登记**：
  - [repository_rule_sources.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_sources.json)
  - [repository_rule_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_boundaries.md)
  - [AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/test_harness/AGENTS.md)
  - [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/test_harness/.agents/rules/shared/SOURCE.json) (`source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)
  - [c_cpp_coding_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/c_cpp_coding_standard.md)
  - [code_documentation_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/code_documentation_standard.md)
  - [end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **三仓版本对齐与候选提交**：
  - `mcu-p3`: `016e1236af75f6f19282d6b000f4b1b68bd96cc3` (`TWIN-47`/`TWIN-48`)
  - `soc-ap`: `333178c66280e785ae1a5c089a6e2a05075cc926` (`TWIN-49`)
  - `test_harness`: `2812f60f5250d777d38a55537d9d5018cb603692` (`TWIN-50`, branch `main`)

## 2. 核心净化与垂直集成改动清单

1. **[twin46_mc_bridge.c](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/twin/twin46_mc_bridge.c)**：
   - **彻底删除 `normalize_ap_temp_wire_frame()`**：`mc_bridge_feed_ap_rx()` 直接将 AP 下发的原始串口字节逐字节送入 `minimc_usart2_rx_isr_byte(data[i])`，严禁篡改任何命令字或重算 CRC。
   - **彻底删除全部 `mc_bridge_notify_*` 与 `mc_bridge_set_motion` 旁路函数**：所有 `[MC-DBG]` 日志（温度 `0x10`/`0x14`/`0x15`、归零与运动 `0x11`/`0x12`/`0x16`/`0x17`、5x5 调平网格 `0x18`/`0x1A`、进退丝/选槽 `0x19`、作业控制 `0x13`、G-code `0x1C`）100% 由真实二进制串口协议帧经 `minimc_proto_poll()` 驱动产生。
   - 提供宿主端 Marlin 强符号桥接（`Extruder_One`、`Platform`、`Heater_set_target_temperature`、`enquecommand`、`enquecommand_P`、`quickStop`）。
2. **[twin46_th_bridge.c](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/twin/twin46_th_bridge.c)**：
   - **彻底删除 `th_bridge_notify_filament_op()`** 与初始化预埋 `th_debug_notify_filament()` 调用，`[TH-DBG]` 日志 100% 由 MC `USART6` 级联转发帧经 `minimc_proto_poll()` 产生。
3. **[debug_reconciliation_probe.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/debug_reconciliation_probe.py)**：
   - **彻底删除 `sync_online_categories` 等所有 `ctypes` `notify` 旁路调用**。
   - `drive_gateway_online_actions()` 100% 通过向运行中的 `ui-gateway` 发起真实 HTTP 请求（`/api/v1/temperature/set`、`/api/v1/temperature/sample`、`/api/v1/gcode/execute`、`/api/v1/jobs/{start,pause,resume,cancel}`、`/api/v1/motion/{home,jog}`、`/api/v1/leveling/trigger`、`/api/v1/filament/slots`），经 D-Bus 与 921600 PTY 串口帧驱动 C 固件完成五类业务闭环。
   - 新增 `resolve_vmware_usb_uart()` 动态探测 `/dev/ttyUSB*`（支持 `/dev/ttyUSB1` 自动漂移回退）。
   - 在 `start_pty_daemon()` 中于 `fork()` 前关闭父进程无需持有的 `slave_fd`，配合 `deploy_twin.sh` 端口/UART 清理机制安全共存。
4. **[check_opcode_alignment.py](file:///home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/check_opcode_alignment.py)**：
   - 对齐 `soc-ap/contracts/twin/telemetry_types.h`、`mcu-p3` MC `minimc_proto.h` 与 TH `minimc_proto.h` 的全部 17 个 MiniMCProto V2 命令码（`0x00`~`0x1C`）。

## 3. 验证命令与实测结果

1. **`verify_opcode_alignment_and_probe_selftest`**：
   - 17/17 跨仓命令码静态对齐检查 `PASS`；
   - `debug_reconciliation_probe.py --self-test` 11 组夹具自检 `PASS`；
   - `! grep -rn "normalize_ap_temp_wire_frame|mc_bridge_notify_|th_bridge_notify_"` 确认零旁路残留。
2. **`verify_vertical_slice_e2e_pty_no_bypass`**：
   - `start-pty` 编译 `libmc_fw.so`/`libth_fw.so` 并启动 921600 PTY；
   - `deploy_twin.sh --mode hardware --baud 921600` 启动完整 AP 服务栈并通过 `--status` 健康检查；
   - `drive-online` + 在线五类业务对账：`[PASS] Live AP gateway reconciliation succeeded (online-5-category)`；
   - `drive-offline` + 断连哨兵 (`2147483646`/`32767`) 与 HTTP `503` 锁定对账：`[PASS] Live AP gateway reconciliation succeeded (offline-sentinel)`；
   - `drive-recovery` + 恢复后在线五类业务对账：`[PASS] Live AP gateway reconciliation succeeded (online-5-category)`。
