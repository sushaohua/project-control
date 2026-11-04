# TWIN-49 工程交付与作者自检报告 (`author_01`)

## 1. 任务与候选提交信息
- **Task ID**: `TWIN-49`
- **Role**: `ENG-FWD` (Vertical-Slice Engineering Agent Phase 3)
- **Target Repository**: `soc-ap`
- **Branch**: `main`
- **Base Commit**: `c2c5a228c81488bca2178488a4e8a109b0472d72`
- **Candidate Commit**: `cd87958209b050c0ef63e9be814dc8eca34b7d07` (`origin/main`)

## 2. 必读规则与设计输入登记 (`read_sources`)
| 类别 | 路径 | 版本/Revision | SHA-256 / 备注 |
| :--- | :--- | :--- | :--- |
| 仓库规则入口 | `soc-ap/AGENTS.md` | workspace canonical | 已显式读取并核对 |
| 共享规则清单 | `soc-ap/.agents/rules/shared/SOURCE.json` | commit `68c28c1ef59b0d063e70e5e46ca0ef8f96eb6dc1` | 已显式读取并核对 |
| C/C++ 编码门禁 | `project-control/.agents/rules/c_cpp_coding_standard.md` | SHA-256 `acda2ba3e4ab2da98d348f5fa0fc5a86ec2e8f77d0ec52512fb1b6ae1bd5c8dc` | $\le 50$ 行、$\le 4$ 参、零开环定时器、超时显式 ACK 闭环 |
| 中文注释规范 | `project-control/.agents/rules/code_documentation_standard.md` | SHA-256 `49302dc5603e742ba6aa2fa7a20dc6fa1fa6ee358335404b5e941724d8627b67` | 全部新增与修改函数均配备中文 Doxygen 注释 |
| 权威修复方案 | `project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md` | `revision: 3` | SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc` |

## 3. 核心实现改动清单（100% 限制在 `TWIN-49` `allowed_paths` 内）
1. **修复 `forward_uart.cpp` 921600 波特率降级 Bug**：
   - 在 `soc-ap/services/forward/forward_uart.cpp` 的 `get_baud_constant()` 中新增 `case 921600: return B921600;` 与 `case 460800: return B460800;`，并导出 `fwd_uart_get_baud_constant()` 供单测校验。
   - 在 `soc-ap/services/forward/forward_types.h` 中将 `AISOC_FWD_DEFAULT_BAUD` 修正为 `921600U`。
2. **扩充 `forward_service` 协议帧构建与双节点全 ACK 门控闭环**：
   - 在 `soc-ap/contracts/twin/telemetry_types.h` 中对齐 `0x01`~`0x1C` 命令码宏与紧凑线长结构体及编译期 `static_assert` 断言。
   - 在 `soc-ap/services/forward/forward_protocol.{h,cpp}` 中实现 `0x10 (SET_TEMP)`、`0x11 (MOTION_HOME)`、`0x12 (MOTION_MOVE)`、`0x13 (JOB_CONTROL)`、`0x16 (POS_QUERY)`、`0x17 (MOTION_STOP)`、`0x18 (LEVEL_GRID_QUERY, 1B probe_idx=7U)`、`0x19 (SLOT_SELECT / FILAMENT_CONTROL)`、`0x1A (LEVEL_TRIGGER)`、`0x1C (GCODE_EXEC)` 帧构造与响应校验（支持 `0x06 NACK` 识别）。
   - 在 `soc-ap/services/forward/forward_service.{h,cpp}` 与 `forward_dbus.cpp` 中实现双节点（MC `0x02` 与 TH `0x03`）顺序单播全 ACK 门控（Sequential Dual-Unicast All-ACK Gate）与结构化故障上下文（`target_node`, `sequence_id`, `elapsed_ms`, `error_code`），任一节点超时或返回 NACK 立即返回强类型错误码并拒绝伪成功。
3. **打通 `device_manager` D-Bus 方法转发、状态同步与断连/丢 ACK 瞬时暂停**：
   - 在 `soc-ap/services/device_manager/device_manager_dbus.cpp` 与 `device_manager_service.{h,cpp}` 中新增 `SetTemperature`、`MotionHome`、`MotionMove`、`QueryPosition`、`JobControl`、`QueryLevelGrid`、`ControlFilament`、`ExecuteGcode` 8 项 D-Bus 方法并转发至 `org.aisoc.ForwardInterface`。
   - 实现 `device_manager_on_ctrl_failure()`：当底层控制 ACK 超时、返回 NACK 或收到 `LinkStateChanged(disconnected)` 时，若当前处于 `PRINTING` 状态则瞬时挂起为 `PAUSED`。
4. **移除 `ui_gateway` 全部内存 Mock 与开环定时器**：
   - 彻底删除 `soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp` 中的硬编码 `DEFAULT_MESH`、`is_homed = true` 本地赋值、点动假坐标累加（`pos_x_mm += step_mm`）及 `ui_gw_job_tick()` 开环 1000ms 行号自增逻辑；作业进度完全由硬件 `0x13 (JOB_CONTROL)` 真实 ACK 驱动，丢 ACK 瞬时切换为 `PAUSED`。
   - 在 `soc-ap/services/ui_gateway/ui_gateway_server.cpp` 与 `ui_gateway_dbus.{h,cpp}` 中补齐 `/api/v1/temperature/set`、`/api/v1/filament/slots`、`/api/v1/gcode/execute`、`/api/v1/motion/*`、`/api/v1/leveling/*`、`/api/v1/jobs/*`、`/api/v1/emergency/*` 真实 D-Bus 调用：硬件 ACK 成功返回 HTTP `200 OK`，离线返回 HTTP `503 Service Unavailable`，超时或 NACK 返回 HTTP `504 Gateway Timeout`。
5. **修复 `deploy_twin.sh` 与 `third_party/build.sh` 自愈构建与残留清理**：
   - 在 `soc-ap/third_party/build.sh` 中增加 `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`。
   - 在 `soc-ap/tools/deploy_twin.sh` 中增加 `ensure_third_party_built()` 自动构建检查、`purge_previous_deployment()` 进程/PID/过期 `dbus.addr` 清理及洁净 `build/` 目录重建。

## 4. 构建与 CTest 自测结果
在独立副本 `/tmp/qa_twin49/soc-ap` 执行任务卡验收命令：
- `bash tools/deploy_twin.sh --build-only`：5/5 全栈目标（`runtime`, `forward`, `device_manager`, `ui_gateway`, `host CLI`）零错误编译通过。
- `ctest --test-dir build/test_forward --output-on-failure`：`test_forward_service` PASS，`test_forward_protocol` PASS（2/2 Passed）。
- `ctest --test-dir build/test_device_manager --output-on-failure`：`test_device_manager_state` PASS（1/1 Passed）。
- `ctest --test-dir build/test_ui_gateway --output-on-failure`：`test_ui_gateway_routes` PASS（1/1 Passed）。
