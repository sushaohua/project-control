# TWIN-49 工程交付与作者复验报告 (`author_03`)

## 1. 任务与候选提交信息
- **Task ID**: `TWIN-49`
- **Role**: `ENG-FWD` (Vertical-Slice Engineering Agent Phase 3)
- **Target Repository**: `soc-ap`
- **Branch**: `main`
- **Base Commit**: `c2c5a228c81488bca2178488a4e8a109b0472d72`
- **Previous Candidate (`author_02`)**: `9b457be31b05a6cf8bbe7b0a1dc08f21f6d8a116`
- **Current Candidate (`author_03`)**: `7848e839de13d1005c0e59c589f07a87e0e930be` (`origin/main`)

## 2. 必读规则与设计输入登记 (`read_sources`)
| 类别 | 路径 | 版本/Revision | SHA-256 / 备注 |
| :--- | :--- | :--- | :--- |
| 仓库规则入口 | `soc-ap/AGENTS.md` | workspace canonical | 已显式读取并核对 |
| 共享规则清单 | `soc-ap/.agents/rules/shared/SOURCE.json` | commit `68c28c1ef59b0d063e70e5e46ca0ef8f96eb6dc1` | 已显式读取并核对 |
| C/C++ 编码门禁 | `project-control/.agents/rules/c_cpp_coding_standard.md` | SHA-256 `acda2ba3e4ab2da98d348f5fa0fc5a86ec2e8f77d0ec52512fb1b6ae1bd5c8dc` | $\le 50$ 行、$\le 4$ 参、零开环定时器、超时显式 ACK 闭环 |
| 中文注释规范 | `project-control/.agents/rules/code_documentation_standard.md` | SHA-256 `49302dc5603e742ba6aa2fa7a20dc6fa1fa6ee358335404b5e941724d8627b67` | 全部新增与修改函数均配备中文说明注释 |
| 权威修复方案 | `project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md` | `revision: 3` | SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc` |

## 3. `qa_02` 唯一阻断项修复说明 (`soc-ap/tools/deploy_twin.sh`)
- **阻断项原文**：
  - `接受条款要求部署前清理配置 UART 的遗留占用进程，但 tools/deploy_twin.sh 在第 234、248 行对命令行包含 debug_reconciliation_probe 或 live_pty_ctl 的进程跳过 UART 文件句柄匹配与终止。`
- **精确修复内容**（[deploy_twin.sh](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/tools/deploy_twin.sh)，SHA-256: `901563a4ada96ea564cc295f66cb532dd56519b375c280a4d0f8b26a55d25c1d`）：
  - 在 `kill_port_and_uart_holders()` 中彻底移除 `cmdline` 读取与 `protected_pty` 豁免分支，将 `if uart_targets and not protected_pty:` 改为 `if uart_targets:`，对任何非自身/非父进程（`exclude_pids` 之外）持有配置端口或 UART 设备句柄的遗留进程一律无差别终止。

## 4. 全栈编译、CTest 单测与无豁免清场验证结果
在 `/tmp/qa_twin49/soc-ap` 隔离副本下执行完整验证：
1. `bash tools/deploy_twin.sh --build-only`：5 大目标全栈构建成功。
2. `ctest --test-dir build/forward --output-on-failure`：`2/2 Passed`。
3. `ctest --test-dir build/device_manager --output-on-failure`：`1/1 Passed`。
4. `ctest --test-dir build/ui_gateway --output-on-failure`：`1/1 Passed`。
5. 无豁免清场验证：
   - 预置 `dist/vmware_twin/logs/stale.log`、`/tmp/aisoc_twin_logs/stale.log`、`dist/vmware_twin/run/stale.cache`、`/tmp/aisoc_twin_logs/stale.cache`、`/tmp/LCK..qa_twin49_dummy_uart`；
   - 启动占用 `127.0.0.1:18089` 的后台监听进程 (`PORT_PID`) 与**命令行显式携带 `debug_reconciliation_probe live_pty_ctl` 参数**且持有 `/tmp/qa_twin49_dummy_uart` 句柄的后台进程 (`UART_PID`)；
   - 执行 `bash tools/deploy_twin.sh --mode sim --port 18089 --uart /tmp/qa_twin49_dummy_uart`；
   - 验证 `PORT_PID` 与携带 `debug_reconciliation_probe live_pty_ctl` 的 `UART_PID` 均被自动终止，旧日志、旧缓存及锁文件全部清除，新 `ui-gateway` 在 `18089` 端口正常响应 `HTTP 200`；
   - 执行 `bash tools/deploy_twin.sh --stop --port 18089 --uart /tmp/qa_twin49_dummy_uart` 正常停止全部守护进程。
