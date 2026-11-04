# TWIN-49 (`author_04`, `ENG-FWD`) 跨仓载荷精确对齐与动态串口探测交付报告

## 1. 任务与规则溯源 (`read_sources`)

- **任务卡**：[TWIN-49.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-49.md) (`run_id: author_04`)
- **规则入口与版本登记**：
  - [repository_rule_sources.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_sources.json)
  - [repository_rule_boundaries.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/repository_rule_boundaries.md)
  - [AGENTS.md](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/AGENTS.md)
  - [SOURCE.json](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/.agents/rules/shared/SOURCE.json) (`shared_rule_bundle_version: 2026-10-30-repo-rule-dist-v1`)
  - [c_cpp_coding_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/c_cpp_coding_standard.md)
  - [code_documentation_standard.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/rules/code_documentation_standard.md)
  - [end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **仓库与候选提交**：
  - 仓库：`soc-ap` (`main`)
  - 候选 Commit：`333178c66280e785ae1a5c089a6e2a05075cc926`

## 2. 本轮精确对齐修改清单（6 项）

1. **`0x16 (POS_REPORT)` 20B 响应结构体与 `um` 单位对齐**：
   - 在 [telemetry_types.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h) 将 `MINIMC_POS_RESP_SIZE` 对齐为 `20U`，并将 `minimc_pos_resp_t` 对齐为 `{pos_x_um, pos_y_um, pos_z_um, pos_e_um, mc_state, homed_mask, reserved}`（与 `mcu-p3` 20B `minimc_pos_payload_t` 逐字节一致）。
   - 在 [forward_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_dbus.cpp) 与 [device_manager_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_dbus.cpp) 中统一以 `um` 为单位传递坐标，去除多余的 `* 10` 二次缩放，并将 `handle_motion_home` 默认速度对齐为 `1500 mm/min`。
2. **`0x12 (MOTION_MOVE)` 16B 请求结构体字段顺序与 `um` 单位对齐**：
   - 在 [telemetry_types.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/twin/telemetry_types.h) 将 `minimc_move_req_t` 字段顺序对齐为 `{axes_mask, is_relative, feedrate_mm_min, x_um, y_um, z_um}`（与整改方案 §2.2.2 及 `mcu-p3` `minimc_move_req_t` 100% 一致）。
   - 在 [device_manager_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_dbus.cpp) 与 [forward_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_dbus.cpp) 中直接传递 `dist_um` (`um`) 与 `1500 mm/min` 进给率，并按非零轴位移自动生成 `axes_mask`。
3. **`0x13 (JOB_CONTROL)` 取消动作码对齐 (`0=CANCEL/IDLE`)**：
   - 在 [ui_gateway_job_ctrl.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp) 的 `ui_gw_job_cancel()` 中将 D-Bus 动作码从 `4U`（在方案 §2.2.3 中为 `QUERY`）对齐为 `0U`（`CANCEL/IDLE`）。
4. **`0x18 (LEVEL_GRID_REPORT)` `5×5` 网格全链路对齐**：
   - 在 [forward_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_dbus.cpp)、[device_manager_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/device_manager/device_manager_dbus.cpp)、[ui_gateway_dbus.h](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/ui_gateway/ui_gateway_dbus.h)、[ui_gateway_dbus.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp) 及 [ui_gateway_job_ctrl.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp) 中将调平网格从 `3×3`（9 点）升级为完整 `5×5`（25 点），并在 `/api/v1/leveling/mesh` JSON 中同步输出 `"grid_valid":true,"probe_idx":7,"z_offset_um":...`。
5. **`0x7FFF` 传感器断路离线哨兵 (`2147483646`) 对齐**：
   - 在 [forward_protocol.cpp](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/services/forward/forward_protocol.cpp) 的 `fwd_proto_parse_raw_temp` 中，当收到 `wire.current_temp_deci_c == 0x7FFF` 且 `wire.sensor_status != MINIMC_WIRE_STATUS_OK` 时映射为 `AISOC_TEMP_MILLIC_OFFLINE` (`2147483646`)，驱动 `device_manager` 与 `ui-gateway` 准确进入 `"OFFLINE"` 与 HTTP `503` 锁定态。
6. **`deploy_twin.sh` 动态 `/dev/ttyUSB*` 探测容错**：
   - 在 [deploy_twin.sh](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/tools/deploy_twin.sh) 的 `hardware` 模式下，当未通过 `--uart` 显式强制指定路径且默认 `AISOC_UART_DEVICE`（如 `/dev/ttyUSB0`）不存在时，自动扫描 `/dev/ttyUSB*`（如 `/dev/ttyUSB1`）并切换，解决 VMware USB 串口号漂移问题。

## 3. 自检与跨仓垂直联调验证结果

- `build_and_test_soc_ap_e2e_control`：5 个全栈构建目标、`test_forward_service`、`test_forward_protocol`、`test_device_manager_state`、`test_ui_gateway_routes` 及 `deploy_twin.sh` 端口/UART 清理验证全部 `0` 退出通过。
- 配合 `TWIN-50` 零旁路 921600 PTY 端到端联调（`verify_vertical_slice_e2e_pty_no_bypass`）：在线五类业务对账、离线哨兵 `2147483646/32767` + HTTP 503 锁定、重连恢复对账全部 `PASS`。
