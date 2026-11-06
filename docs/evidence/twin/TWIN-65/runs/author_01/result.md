# TWIN-65 作者实现与主机单元测试自检证据 (`author_01`)

## 1. 任务与基线信息
- **任务编号**：`TWIN-65`
- **执行角色**：`ENG-FWD` / `ENG-STATE` / `ENG-UI` (`eng-vertical`)
- **目标仓库与分支**：`soc-ap` (`main`)
- **源码基线 Commit**：`c6692b244e0aa09d04e7051293f9fef3c67535dd`
- **交付候选 Commit**：`7184edfc796923e2f2c6e3e57ef3a9f791164b51`（修复 `runs/qa_03` 容器高负载下 `test_dds_version_sync_dual_nodes` 版本新鲜度与 D-Bus 广播竞态）

## 2. 规则入口与读取来源登记 (`read_sources`)
- `soc-ap/AGENTS.md` + `soc-ap/.agents/rules/shared/SOURCE.json` (`960f079647a00864fe7913836336b2a2ee3d729a`)
- `project-control/.agents/rules/c_cpp_coding_standard.md`
- `project-control/.agents/rules/code_documentation_standard.md`
- `project-control/docs/architecture/MINIMCPROTO_V2_SPEC.md` (Rev 2.0.4)
- `project-control/docs/architecture/VMWARE_SOC_TWIN_MASTER_PLAN_20261029.md` (Rev 5.1)
- `project-control/docs/plans/TASK_009_SOC_OTA_AND_DUAL_CONFIRMATION_SPEC_20261105.md`

## 3. 核心实现清单 (`allowed_paths` 范围内)
1. **契约对齐 (`contracts/twin/telemetry_types.h`)**：
   - 移除历史 `0x05 MINIMC_CMD_ESTOP_ACK`，全面对齐 Rev 2.0.4 命令码 `0x1D MINIMC_CMD_SYSTEM_CONTROL`（`4B`）、`0x20 MINIMC_CMD_OTA_START`（`144B = 16B header + 128B ATSG Trailer`）、`0x21 MINIMC_CMD_OTA_DATA`（`8B + <=512B`）、`0x22 MINIMC_CMD_OTA_FINISH`（`8B`）、`0x23 MINIMC_CMD_OTA_STATUS`（`8B`）及 `MINIMC_MAX_PAYLOAD_SIZE = 520U`。
   - 定义 128B `minimc_fw_trailer_t`（`magic=0x41545347`、`struct_version=0x00010000`、`board_id`、`version_code`、`payload_len`、`payload_sha256[32]`、`sig_r[32]`、`sig_s[32]`、`reserved[8]`、`trailer_crc32`）及 `static_assert` 布局断言。
2. **协议收发扩展 (`services/forward/forward_protocol.*`, `forward_uart.cpp`, `forward_service.*`)**：
   - 实现 `forward_build_sys_ctrl_req`、`forward_build_ota_start_req`、`forward_build_ota_data_req`、`forward_build_ota_finish_req`、`forward_build_ota_status_req`。
   - 在 `forward_uart_send_ctrl_sync` 与 `forward_service_*` 中实现停等式单帧在途（`in_flight == 1`）RPC，支持 `0x20` 长超时（`5000 ms`）与 `0x21/0x22/0x23` 显式 ACK/NACK 闭环。
3. **升级状态机与四阶段双确认 (`services/device_manager/device_manager_types.h`, `device_manager_state.*`, `firmware_updater.*`)**：
   - `/var/update/incoming` 扫描器：忽略 `.part` 临时文件，探测完整 `.bin` 转入 `PACKAGE_STAGED_PENDING_CONFIRM` 待确认，并拷贝至 `/var/update/staging` 设 `0444` 只读封存。
   - 离线预检：校验 `128B ATSG Trailer`（`magic`、`struct_version`、`trailer_crc32`、`board_id` 与目标节点匹配、`payload_len` Flash 容量上限、`payload_sha256` 全量校验），任一失败零串口副作用拒绝。
   - 四条件安全准入 (`dev_state_check_ota_admission`)：要求作业空闲、运动空闲（`mc_state==0`）、双路温度有效无故障、加热全关（目标 `<=0` 且 PWM `0%`）。
   - `UPGRADING_MAINTENANCE` 维护窗口：升级期间抑制常规 `1.5s STALE / 3.0s OFFLINE` 衰退（温度质量置 `MAINTENANCE_HOLD`，不注入 `2147483646` 哨兵），失败或无法恢复时转入 `OTA_RECOVERY_PENDING`。
   - 串行升级顺序：先 `TH (0x03)` 完全达标（Stage 1~4 全部通过）后，再启动 `MC (0x02)`。
   - 四阶段确认硬隔离：
     - **Stage 1 (`BOOT_MODE_CONFIRMED`)**：发送 `0x1D(action=0x02)` 后轮询 `0x01 -> 0x02` 确认 `capability_flags.bit31 == 1` 且 `boot_id` 刷新。
     - **Stage 2 (`TRANSFER_AND_FLASH_PROGRESS`)**：`0x20 -> 0x21 -> 0x23` 停等传输，核对 `cached_chunk0_bytes` 与 `bytes_written`。
     - **Stage 3 (`IMAGE_VERIFIED_COMMITTED`)**：收到 `0x22 CMD_OTA_FINISH` 的 `0x00 ACK` 时，进度封顶 `95%`、状态文案锁定 `"IMAGE_VERIFIED_COMMITTED"`，严禁提前宣称 `100%` 或 `SUCCEEDED`。
     - **Stage 4 (`NEW_APP_ONLINE_VERIFIED`)**：轮询 `0x01 -> 0x02` 与 `0x14 -> 0x15` 确认 `capability_flags.bit31 == 0`、`boot_id` 再次刷新、`(major<<8|minor) == target_version_code`、`git_commit_short` 匹配且鲜活温度恢复后，方才置为 `100% SUCCEEDED`。
4. **网关控制锁与 OTA 路由 (`services/ui_gateway/ui_gateway_server.*`)**：
   - `UPGRADING_MAINTENANCE` 期间所有常规控制路由（`/api/v1/control/*`, `/api/v1/temperature/target`, `/api/v1/motion/*`, `/api/v1/job/*`, `/api/v1/filament/*`, `/api/v1/gcode`）返回 `HTTP 409 Conflict`（`CONFLICT_UPGRADING_MAINTENANCE`），仅急停保持抢占优先。
   - 新增 `GET /api/v1/ota/status` 与 `POST /api/v1/ota/trigger` 路由。

## 4. 构建与测试验证结果
在独立临时目录 `/tmp/qa_twin65` 执行完整构建与单元测试：
```text
[BUILD] All 5 full-stack targets built successfully.
Test project /tmp/qa_twin65/soc-ap/build/forward
1/2 Test #1: test_forward_service .............   Passed    0.88 sec
2/2 Test #2: test_forward_protocol ............   Passed    0.76 sec
100% tests passed out of 2

Test project /tmp/qa_twin65/soc-ap/build/device_manager
1/3 Test #1: test_device_manager_state ........   Passed    0.23 sec
2/3 Test #2: test_firmware_updater ............   Passed    0.00 sec
3/3 Test #3: test_device_manager ..............   Passed    1.33 sec
100% tests passed out of 3

Test project /tmp/qa_twin65/soc-ap/build/ui_gateway
1/1 Test #1: test_ui_gateway_routes ...........   Passed    0.07 sec
100% tests passed out of 1
```
- **S04 静态门禁检查**：全部自研非结构体函数严格 `<= 50` 行、`<= 4` 入参，公开函数首行 Guard Clause 完整，新增/修改注释及 docstring 100% 中文，0 违规。
