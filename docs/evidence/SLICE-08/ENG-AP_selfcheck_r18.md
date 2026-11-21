# SLICE-08 (r18 / r18b) ENG-AP 自检报告 (`S08-R18-AP` + Round 1 竞态加固)

- **角色 / 仓库 / 分支**: `ENG-AP` / `printer-soc` / `main`
- **基线提交**: `c9a1541ed8a54b83ec26799153754fa710b5e57b`
- **首轮提交 (`r18`)**: `5066bbb91a7fe37d3ff6005fe5e0854c6ba18b3d`
- **Round 1 最终候选提交 (`r18b`)**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`（已完成 `fetch && rebase && push`，线性历史且工作树干净）
- **依据文档**:
  - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（§5 `HIL-DEF-06`、`HIL-DEF-07`）
  - `project-control/slices/SLICE-08.yaml`（`revision: 5`）

## 1. 修改文件与 Diff Budget 核对

本轮增量修改 **5 个文件**（`SLICE-08` 切片累计修改 `13` 个文件 `<= max_files: 13`）：
1. `services/forward/modules/ota/ota_transfer.cpp`（`+55 / -10`）：`OTA_ENTER_BOOT_WAIT_US = 450000U`；保持 Stage-2 `wait_mode(rt, true, out)` 首错锁存（严格保留 `boot_timeout` `count((3,1))==4`）；为 Stage-4 `wait_mode(rt, false, out)` 新增静态辅助函数 `probe_version_once` 与 `wait_app_ready`（最多 `8` 次有界重询覆盖 MC `~2.0s` 启动期，遇非超时错误或耗尽 `8` 次锁存 `communication_error`）。
2. `services/device_manager/device_manager_service.cpp`（`+41 / -2`）：`receive_maintenance()` 检测 `is_maintenance` 跳变，分别调用 `dev_state_enter_maintenance(state)` / `dev_state_exit_maintenance(state, false)` 并通过 `publish_maintenance_transition()` 广播最新快照与状态变更信号，消除 `"UPGRADING_MAINTENANCE"` 残留。
3. `tests/ota/test_ota_e2e.py`（`+9 / -1`）：新增 `delayed_app_boot` 用例覆盖双签名策略（模拟 `0x22` 后前 3 次 `0x01` 超时、第 4 次上线仍 `SUCCEEDED 100%`）。
4. `tests/device_manager/twin/test_device_manager.cpp`（`+99 / -0`）：新增 `test_unit_maintenance_enter_and_exit_state` 与 `test_dds_maintenance_enter_and_exit_recovery`。
5. `tests/integration/test_active_status.cpp`（`+2 / -0`，Round 1 返修）：在 `start_services()` 补齐 `aisoc_dds_publisher_wait_for_matched(env->forward.status_runtime.publisher, 1U, 1500U)`，消除 `VOLATILE` QoS 单边匹配下立即向 PTY 注入单次 `0x40` 帧的容器高负载丢包竞态。

## 2. 提交后验证结果
- 双配置 `ctest`（默认与 `-DAISOC_OTA_INTEGRITY_ONLY_HIL=ON`）：**24/24 Passed**；`active_status_pipeline` 连续 20 次防抖复测（`--repeat until-fail:20`）`12.20s` 全绿。
- `test_ota_e2e.py`（默认与 `--policy integrity-only-hil`）：**18/18 Passed**（含 `delayed_app_boot` 与 `boot_timeout`）。
- `fast_gate.py --slice project-control/slices/SLICE-08.yaml`：退出码 `0`。
