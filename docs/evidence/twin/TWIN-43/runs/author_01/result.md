# TWIN-43 作者自检与接单核对报告 (`author_01`)

- **任务 ID**：`TWIN-43`（`revision: 1`）
- **任务标题**：AP/VMware `921600` 波特率统一与全栈一键编译及配置化启动脚本
- **执行角色**：`ENG-FWD`
- **执行会话 ID**：`6e214c7d-0965-4b36-805c-41c6f83a87bc`
- **回报目标 (`COORD`)**：`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`
- **目标仓库与分支**：`soc-ap` (`main`)
- **基线提交 (`base_commit`)**：`427dd6d82caceebb7b4642e78f1dbfa96ff5fc84`
- **候选提交 (`candidate_commit`)**：`217a76e29c0c999897bf1993514b765cd771adb06` -> 实测精确 SHA：`217a76e29c0c99897bf1993514b765cd771adb06`（已推送至 `origin/main`）
- **生成时间**：`2026-11-04T10:58:00+08:00`

---

## 一、接单前置核对回执

| 核对项 | 期望值 / 契约要求 | 实测核对结果 | 状态 |
| :--- | :--- | :--- | :--- |
| 任务卡版本 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-43.md` (`revision: 1`) | `revision: 1` | PASS |
| `ARCH` 权威拆分方案 | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 2`, SHA-256: `fe72f550cc32d28dbba0a00d364373b8b2687c1c4c007a6e5f03732e94a99697`, 作者会话 `433026bf-a1ff-4863-8f3e-7a5f43b016ff`) | 完全一致 | PASS |
| `protocol_input` 合并实施概要 | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` (`revision: 2`, SHA-256: `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec`) | 完全一致 | PASS |
| 需求确认单 | `project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md` (`revision: 1`, SHA-256: `3911e18cf6ca949369d9449659c3fa842af57e025cd718de327a7c57b6ee0a37`) | 完全一致 | PASS |
| `source_baseline` (`soc-ap`) | `427dd6d82caceebb7b4642e78f1dbfa96ff5fc84` (`main`) | 开工前 `HEAD` 精确匹配 `427dd6d82caceebb7b4642e78f1dbfa96ff5fc84` | PASS |
| 前置依赖 (`depends_on`) | `TWIN-04` (`Done`), `TWIN-30` (`Done`) | 已闭环验收通过 | PASS |
| 写权限范围 (`allowed_paths`) | 仅限 `soc-ap/core/forward/transport/serial_posix.{h,cpp}`、`soc-ap/core/host/{main.cpp,query.h,query.cpp}`、`soc-ap/config/runtime/{vmware,common}/**`、`soc-ap/dist/vmware_twin/config/services_manifest.json`、`soc-ap/tools/deploy_twin.sh`、`project-control/docs/evidence/twin/TWIN-43/**` | `git -C soc-ap show --name-only` 100% 落于白名单内，零越界修改 | PASS |

> **附：关于 `TWIN-43.md` `verification.commands` 脚本参数名的核对提醒（供 `COORD` 在启动 Docker QA Runner 前同步）**：
> 1. `test_harness/static_checks/cascade/run_query_cases.py` 实际接收宿主二进制的参数名为 `--test-host build/host/soc-ap`（而非 `--binary build/host/soc-ap`）。
> 2. `test_harness/static_checks/twin/validate_schemas.py` 实际接收工作区根目录的参数名为 `--root ..`（而非 `--soc-ap-root ../soc-ap`）。
> 由于 `test_harness/**` 属于 `TWIN-43` 的 `forbidden_paths`，本轮严格未触碰 `test_harness/**`；建议 `COORD` 在触发受控 Docker QA 沙箱前将 `TWIN-43.md` 中这两处 CLI 选项名修正为真实脚本支持的 `--test-host` 与 `--root ..`。

---

## 二、修改文件与交付物清单

`soc-ap` 候选提交 `217a76e29c0c99897bf1993514b765cd771adb06` 变更文件：
1. `soc-ap/core/forward/transport/serial_posix.h`：`SerialConfig::baud_rate` 默认值更新为 `921600`。
2. `soc-ap/core/forward/transport/serial_posix.cpp`：`baud_to_speed()` 新增 `460800` (`B460800`) 与 `921600` (`B921600`) 映射，保留 `9600`..`230400` 既有支持，非法波特率返回 `false`；`serial_open()` 默认初始化 `speed = B921600`。
3. `soc-ap/core/host/query.h`：`QueryOptions::baud_rate` 默认值更新为 `921600`。
4. `soc-ap/core/host/query.cpp`：新增 `is_supported_baud_rate()` 辅助函数，`parse_baud_rate()` 支持 `{9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600}`，拒绝非法波特率。
5. `soc-ap/core/host/main.cpp`：`print_usage()` 首行增加空指针卫语句，并将帮助信息更新为 `[--baud 921600]`。
6. `soc-ap/config/runtime/vmware/services_manifest.json`：`forward-service` 串口 `baud_rate` 更新为 `921600`。
7. `soc-ap/config/runtime/common/services_manifest.json`：`forward-service` 串口 `baud_rate` 更新为 `921600`。
8. `soc-ap/dist/vmware_twin/config/services_manifest.json`：`forward-service` 串口 `baud_rate` 更新为 `921600`。
9. `soc-ap/config/runtime/vmware/aisoc_twin.conf`：新增默认运行配置文件（`AISOC_MODE="hardware"`, `AISOC_UART_DEVICE="/dev/ttyUSB0"`, `AISOC_UART_BAUD="921600"`, `AISOC_HTTP_BIND="0.0.0.0"`, `AISOC_HTTP_PORT="8080"`, `AISOC_WEB_ROOT="browser_hmi/first_release"`, `AISOC_LOG_DIR="/tmp/aisoc_twin_logs"`, `AISOC_AUTO_BUILD="1"`）。
10. `soc-ap/tools/deploy_twin.sh`：升级为全栈一键增量编译（`build/runtime`, `build/forward`, `build/device_manager`, `build/ui_gateway`, `build/host`）与配置驱动生命周期管理脚本（支持 `--config`, `--mode sim|hardware`, `--uart`, `--baud`, `--port`, `--build-only`, `--status`, `--stop`）。

---

## 三、C/C++ 编码规范硬性门禁核查结果

对照 `project-control/.agents/rules/c_cpp_coding_standard.md` 对所有修改文件内的函数逐一执行静态门禁核查：

| 源文件 | 函数名 | 行号范围 | 总行数（含空行） | 非空有效行数 ($\le 50$) | 入参个数 ($\le 4$) | 首行空指针卫语句 | 结论 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `serial_posix.cpp` | `baud_to_speed` | L11-L47 | 37 | 37 | 2 | `if (speed == nullptr)` | PASS |
| `serial_posix.cpp` | `configure_termios` | L49-L78 | 30 | 24 | 2 | `if (fd < 0)` | PASS |
| `serial_posix.cpp` | `serial_open` | L80-L105 | 26 | 24 | 2 | `if (config == nullptr \|\| ...)` | PASS |
| `serial_posix.cpp` | `serial_close` | L107-L116 | 10 | 10 | 1 | `if (ctx == nullptr)` | PASS |
| `serial_posix.cpp` | `wait_for_writable` | L118-L135 | 18 | 17 | 2 | `if (fd < 0)` | PASS |
| `serial_posix.cpp` | `serial_write` | L137-L179 | 43 | 41 | 4 | `if (bytes_written != nullptr) ...` | PASS |
| `serial_posix.cpp` | `serial_read` | L181-L225 | 45 | 42 | 4 | `if (bytes_read != nullptr) ...` | PASS |
| `main.cpp` | `print_usage` | L19-L28 | 10 | 10 | 1 | `if (executable == nullptr)` | PASS |
| `main.cpp` | `run_host_daemon` | L30-L46 | 17 | 14 | 1 | `if (opts == nullptr)` | PASS |
| `main.cpp` | `run_query_mode` | L48-L73 | 26 | 25 | 1 | `if (opts == nullptr)` | PASS |
| `query.cpp` | `is_supported_baud_rate` | L63-L77 | 15 | 15 | 1 | 值入参 | PASS |
| `query.cpp` | `parse_baud_rate` | L79-L95 | 17 | 17 | 2 | `if (str == nullptr \|\| out_baud == nullptr ...)` | PASS |
| `query.cpp` | `parse_param_with_value` | L138-L184 | 47 | 47 | 4 | `if (arg == nullptr \|\| ...)` | PASS |
| `query.cpp` | `parse_single_option` | L186-L213 | 28 | 28 | 4 | `if (arg == nullptr \|\| ...)` | PASS |
| `query.cpp` | `parse_query_arguments` | L215-L242 | 28 | 28 | 3 | `if (argv == nullptr \|\| opts == nullptr)` | PASS |

---

## 四、自检验证命令与原始输出

### 4.1 全栈增量编译、`forward` 单元测试与 `921600` PTY 级联黑盒回归

执行命令（`cwd: soc-ap`）：
```bash
bash tools/deploy_twin.sh --build-only && ctest --test-dir build/forward --output-on-failure && python3 ../test_harness/static_checks/cascade/run_query_cases.py --test-host build/host/soc-ap --cases ../test_harness/test_cases/cascade/query_cases.json
```

关键输出：
```text
[BUILD 1/5] runtime (build/runtime)...
[100%] Built target aisoc_supervisor
[100%] Built target test_supervisor_topology
[BUILD 2/5] forward (build/forward & build/test_forward)...
[100%] Built target forward_service_daemon
[100%] Built target test_forward_service
[BUILD 3/5] device_manager (build/device_manager)...
[100%] Built target device_manager_daemon
[BUILD 4/5] ui_gateway (build/ui_gateway)...
[100%] Built target ui-gateway
[BUILD 5/5] host CLI (build/host)...
[100%] Built target soc-ap
=================================================================
[BUILD] All 5 full-stack targets built successfully.
=================================================================
Test project /home/sushaohua/workspace/ai_soc_project/soc-ap/build/forward
    Start 1: test_forward_service
1/1 Test #1: test_forward_service .............   Passed    0.49 sec

100% tests passed out of 1
[OK] 黄金用例集静态校验通过: ../test_harness/test_cases/cascade/query_cases.json (含 4 正例, 10 负例)
===========================================================================
       执行 AP 宿主程序黑盒 PTY 级联查询测试: build/host/soc-ap
===========================================================================
[PASS] CAS-POS-001 .. CAS-POS-004 (4/4)
[PASS] CAS-NEG-001 .. CAS-NEG-010 (10/10)
---------------------------------------------------------------------------
测试汇总: 总用例 14, 通过 14, 失败 0
```

### 4.2 `services_manifest.json` (`921600`) Schema 校验

执行命令（`cwd: test_harness`）：
```bash
python3 static_checks/twin/validate_schemas.py --root ..
```
及三份实体 `services_manifest.json` 针对 `services_manifest_schema.json` 的 Draft-07 校验：
```text
TWIN-03 Schema Draft7Validator Matrix Results: Total: 16, Passed: 16, Failed: 0
[PASS] soc-ap/config/runtime/vmware/services_manifest.json: schema=VALID, baud_rate=921600
[PASS] soc-ap/config/runtime/common/services_manifest.json: schema=VALID, baud_rate=921600
[PASS] soc-ap/dist/vmware_twin/config/services_manifest.json: schema=VALID, baud_rate=921600
```

### 4.3 `deploy_twin.sh` `sim` 模式全栈启动、`--status` 探活与 `--stop` 生命周期验证

执行命令（`cwd: soc-ap`）：
```bash
bash tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh --status && bash tools/deploy_twin.sh --stop
```

原始输出：
```text
=================================================================
AI-SoC VMware Twin Full Stack Deployed Successfully!
  Mode:        sim
  UART:        /dev/ttyUSB0 @ 921600 baud
  HTTP URL:    http://127.0.0.1:18080/
  State API:   http://127.0.0.1:18080/api/v1/state
  Snapshot:    http://127.0.0.1:18080/api/v1/temperature/snapshot
  Logs & PIDs: /tmp/aisoc_twin_logs
=================================================================
=================================================================
AI-SoC VMware Twin Full-Stack Status (Mode: sim)
  UART Device: /dev/ttyUSB0 @ 921600 baud
  HTTP Bind:   0.0.0.0:18080
=================================================================
  [RUNNING] dbus-daemon (PID: 2863623)
  [RUNNING] forward_service_daemon (PID: 2863628)
  [RUNNING] device_manager_daemon (PID: 2863629)
  [RUNNING] ui-gateway (PID: 2863631)
  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state -> HTTP 200 OK
=================================================================
[STOP] Stopping ui-gateway (PID: 2863631)...
[STOP] Stopping device_manager_daemon (PID: 2863629)...
[STOP] Stopping forward_service_daemon (PID: 2863628)...
[STOP] Stopping dbus-daemon (PID: 2863623)...
[STOP] All AI-SoC VMware Twin services stopped and PID files cleaned.
```

### 4.4 负例自检（非法波特率拦截 + `hardware` 模式缺失串口设备拒绝静默降级）

1. **非法波特率 `123456` 拦截**：
   - 命令：`soc-ap/build/host/soc-ap --port /dev/null --target mc --cmd version --baud 123456`
   - 结果：立即返回 `EXIT_CODE_USAGE_ERROR` (`exit_code = 4`)。
2. **`hardware` 模式缺失串口设备拒绝启动**：
   - 命令：`bash soc-ap/tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB_NONEXISTENT_99`
   - 输出：`ERROR: Hardware mode requires UART device '/dev/ttyUSB_NONEXISTENT_99', but device node does not exist. Aborting without falling back to sim mode.`
   - 结果：返回非 0 退出码 (`exit_code = 3`)，未启动任何守护进程、未静默降级为 `sim`。
