# TWIN-49 工程交付与作者复验报告 (`author_02`)

## 1. 任务与候选提交信息
- **Task ID**: `TWIN-49`
- **Role**: `ENG-FWD` (Vertical-Slice Engineering Agent Phase 3)
- **Target Repository**: `soc-ap`
- **Branch**: `main`
- **Base Commit**: `c2c5a228c81488bca2178488a4e8a109b0472d72`
- **Previous Candidate (`author_01`)**: `cd87958209b050c0ef63e9be814dc8eca34b7d07`
- **Current Candidate (`author_02`)**: `9b457be31b05a6cf8bbe7b0a1dc08f21f6d8a116` (`origin/main`)

## 2. 必读规则与设计输入登记 (`read_sources`)
| 类别 | 路径 | 版本/Revision | SHA-256 / 备注 |
| :--- | :--- | :--- | :--- |
| 仓库规则入口 | `soc-ap/AGENTS.md` | workspace canonical | 已显式读取并核对 |
| 共享规则清单 | `soc-ap/.agents/rules/shared/SOURCE.json` | commit `68c28c1ef59b0d063e70e5e46ca0ef8f96eb6dc1` | 已显式读取并核对 |
| C/C++ 编码门禁 | `project-control/.agents/rules/c_cpp_coding_standard.md` | SHA-256 `acda2ba3e4ab2da98d348f5fa0fc5a86ec2e8f77d0ec52512fb1b6ae1bd5c8dc` | $\le 50$ 行、$\le 4$ 参、零开环定时器、超时显式 ACK 闭环 |
| 中文注释规范 | `project-control/.agents/rules/code_documentation_standard.md` | SHA-256 `49302dc5603e742ba6aa2fa7a20dc6fa1fa6ee358335404b5e941724d8627b67` | 全部新增与修改函数均配备中文说明注释 |
| 权威修复方案 | `project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md` | `revision: 3` | SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc` |

## 3. `qa_01` 唯一阻断项修复说明 (`soc-ap/tools/deploy_twin.sh`)
- **阻断项原文**：
  - `阻断：接受范围要求部署前清理旧进程、端口/UART 占用、旧缓存和旧日志。候选 deploy_twin.sh 的 purge_previous_deployment 只停止受管 PID、按指定可执行文件名清理进程，并删除 PID、dbus.addr 和 runtime.env；没有清理占用配置端口或 UART 的其他进程，也没有清理旧日志。`
- **精确修复内容**（[deploy_twin.sh](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/tools/deploy_twin.sh)，SHA-256: `7cf18b1e5e98f3853c308f455e693e833a80554cb222262f695a3e0ca28d0228`）：
  1. 新增 `kill_port_and_uart_holders()` 函数：通过 `python3` 扫描 `/proc/net/tcp`、`/proc/net/tcp6` 及 `/proc/[0-9]*/fd/*`，定位并终止占用配置端口 `${AISOC_HTTP_PORT}` 或配置串口 `${AISOC_UART_DEVICE}` 的遗留进程（排除自身 `$$` 与父进程 `$PPID`，并保护包含 `debug_reconciliation_probe` / `live_pty_ctl` 的虚拟 PTY 桥接进程）；同时兼容 `fuser -k "${target_port}/tcp"`。
  2. 清理串口锁文件：删除 `/var/lock/LCK..$(basename "${AISOC_UART_DEVICE}")`、`/tmp/LCK..$(basename "${AISOC_UART_DEVICE}")`、`dist/vmware_twin/run/*.lock` 与 `${AISOC_LOG_DIR}/*.lock`。
  3. 清理旧日志文件：删除 `dist/vmware_twin/logs/*.log`、`dist/vmware_twin/run/*.log` 与 `${AISOC_LOG_DIR}/*.log`。
  4. 清理旧缓存与 IPC 残留：删除 `dist/vmware_twin/run/*.cache`、`dist/vmware_twin/run/cache`、`dist/vmware_twin/cache`、`${AISOC_LOG_DIR}/*.cache`、`${AISOC_LOG_DIR}/cache`、`/tmp/aisoc_cache_*`、`/dev/shm/aisoc_*` 以及各目录下的 `*.pid`、`dbus.addr`、`runtime.env`。

## 4. 全栈编译、CTest 单测与 `deploy_twin.sh` 清场定向验证结果
在 `/tmp/qa_twin49/soc-ap` 隔离副本下执行完整验证：
1. `bash tools/deploy_twin.sh --build-only`：5 大目标全栈构建成功。
2. `ctest --test-dir build/forward --output-on-failure`：`2/2 Passed` (`test_forward_service`, `test_forward_protocol`)。
3. `ctest --test-dir build/device_manager --output-on-failure`：`1/1 Passed` (`test_device_manager_state`)。
4. `ctest --test-dir build/ui_gateway --output-on-failure`：`1/1 Passed` (`test_ui_gateway_routes`)。
5. 定向清场验证：
   - 预置 `dist/vmware_twin/logs/stale.log`、`/tmp/aisoc_twin_logs/stale.log`、`dist/vmware_twin/run/stale.cache`、`/tmp/aisoc_twin_logs/stale.cache`、`/tmp/LCK..qa_twin49_dummy_uart`；
   - 启动占用 `127.0.0.1:18089` 的后台 Socket 监听进程 (`PORT_PID`) 与持有 `/tmp/qa_twin49_dummy_uart` 文件描述符的后台进程 (`UART_PID`)；
   - 执行 `bash tools/deploy_twin.sh --mode sim --port 18089 --uart /tmp/qa_twin49_dummy_uart`；
   - 验证 `PORT_PID` 与 `UART_PID` 均被自动终止，`stale.log`、`stale.cache`、`LCK..qa_twin49_dummy_uart` 均被清除，新 `ui-gateway` 在 `18089` 端口正常响应 `HTTP 200`；
   - 执行 `bash tools/deploy_twin.sh --stop --port 18089 --uart /tmp/qa_twin49_dummy_uart` 正常停止全部守护进程。
