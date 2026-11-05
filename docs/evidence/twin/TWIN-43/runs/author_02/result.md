# TWIN-43 作者修正与自检报告 (`author_02`)

- **任务 ID**：`TWIN-43`（`revision: 1`）
- **运行批次 (`run_id`)**：`author_02`
- **任务标题**：AP/VMware `921600` 波特率统一与全栈一键编译及配置化启动脚本
- **执行角色**：`ENG-FWD`
- **执行会话 ID**：`6e214c7d-0965-4b36-805c-41c6f83a87bc`
- **回报目标 (`COORD`)**：`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`
- **目标仓库与分支**：`soc-ap` (`main`)
- **基线提交 (`base_commit`)**：`427dd6d82caceebb7b4642e78f1dbfa96ff5fc84`
- **上一轮候选 (`author_01`)**：`217a76e29c0c99897bf1993514b765cd771adb06`
- **本轮候选提交 (`candidate_commit`)**：`426d604e9ddcfdb3e95e94ecff4f699ae976fc95`（已推送至 `origin/main`）
- **生成时间**：`2026-11-04T12:38:00+08:00`

---

## 一、接单核对与修正依据

| 核对项 | 契约/输入要求 | 实测核对结果 | 状态 |
| :--- | :--- | :--- | :--- |
| 任务卡版本 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-43.md` (`revision: 1`, `run_id: author_02`) | 完全一致 | PASS |
| `ARCH` 权威拆分方案 (`revision: 9`) | `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md`（SHA-256: `13b5a69b92f8369457ed99c0dbea5b5756d6bb2d4b1c7308bcfa33732ab4dad7`） | 完全一致 | PASS |
| `qa_03` 独立 Codex 审查报告 | `project-control/docs/evidence/twin/TWIN-43/runs/qa_03/qa_review_report.md`（会话 `01a1a4bd-7ebf-7a41-8988-76b3635ee14c`，SHA-256: `973d4076df612a5931de753dbcc9f4d568e4e5055219a12d7481b1baa0735210`） | 完全一致 | PASS |
| `protocol_input` 合并实施概要 | `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md`（`revision: 2`，SHA-256: `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec`） | 完全一致 | PASS |
| 写权限范围 (`allowed_paths`) | `git -C soc-ap diff --name-only 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84 426d604e9ddcfdb3e95e94ecff4f699ae976fc95` 100% 落于 `TWIN-43` 允许路径内，历史目录 `author_01/` 与 `qa_01`~`qa_03` 完整保留 | 完全一致 | PASS |

---

## 二、`author_02` 针对 `qa_03` 与 `ARCH` `revision: 9` 的修正内容

1. **彻底移除未消费的配置项 `AISOC_HTTP_BIND`**：
   - 从 `soc-ap/config/runtime/vmware/aisoc_twin.conf` 中移除 `AISOC_HTTP_BIND="0.0.0.0"`，仅保留全部 7 个被脚本真实消费生效的配置键：`AISOC_MODE`、`AISOC_UART_DEVICE`、`AISOC_UART_BAUD`、`AISOC_HTTP_PORT`、`AISOC_WEB_ROOT`、`AISOC_LOG_DIR`、`AISOC_AUTO_BUILD`。
   - 从 `soc-ap/tools/deploy_twin.sh` 中移除 `AISOC_HTTP_BIND` 默认变量，并在 `run_status()` 中固定输出真实监听地址：`echo "  HTTP Listen: 0.0.0.0:${port}"`（与 `ui-gateway` 固定监听 `INADDR_ANY:${port}` 完全一致）。
2. **彻底移除非必需的 `--foreground` (`-f`) 选项**：
   - 从 `soc-ap/tools/deploy_twin.sh` 的头部注释、`DO_FOREGROUND` 变量、`print_usage()`、CLI 参数解析 `case` 及 `ui-gateway` 启动逻辑中移除 `--foreground` / `-f` 分支，使脚本暴露的全部 CLI 选项（`--config`、`--mode`、`--uart`、`--baud`、`--port`、`--build-only`、`--status`、`--stop`、`--help`）在自动化测试中 100% 覆盖执行。

---

## 三、全量自检命令与输出摘要

### 3.1 `build_and_test_fullstack_921600` (`cwd: soc-ap`)
- **执行结果**：`exit_code = 0`
- **关键输出**：
  - 全栈 5 个目标（`build/runtime`, `build/forward`, `build/device_manager`, `build/ui_gateway`, `build/host`）编译 0 错误；
  - `ctest --test-dir build/forward --output-on-failure`：`1/1 Test #1: test_forward_service Passed`；
  - `run_query_cases.py`（14 项 `921600` PTY 级联查询正反例）：`总用例 14, 通过 14, 失败 0`；
  - POSIX PTY 波特率正反例实测：`[PASS] serial_posix baud_to_speed & serial_open positive(921600/460800/115200) and negative(123456) verified`；
  - 宿主 CLI 非法波特率拦截：`[PASS] parse_baud_rate rejected invalid baud 123456`。

### 3.2 `validate_manifest_schema` (`cwd: test_harness`)
- **执行结果**：`exit_code = 0`
- **关键输出**：`Total: 16, Passed: 16, Failed: 0`（`POS-MAN-VMWARE` 与 `POS-MAN-SOC` 均为 `VALID`）。

### 3.3 `verify_deploy_twin_sim_lifecycle` (`cwd: soc-ap`)
- **执行结果**：`exit_code = 0`
- **覆盖验证项**：
  - `--help` 正常输出帮助并以 `0` 退出；
  - `--unknown-flag`、`--mode invalid_mode`、`--mode sim --port 70000`、`--config /tmp/nonexistent_twin.conf`、`--mode hardware --uart /dev/nonexistent_ttyUSB99`、`--mode sim --baud 123456` 均报错并以非 0 退出码拒绝执行；
  - `FORCE_CURL_FAIL=1` 启动后健康探活失败时自动逆序停止全部已启动守护进程并清理全部 PID 与 `runtime.env` 文件：`[PASS] post-launch health-check failure cleaned up all daemons and PID/runtime files`；
  - `--config /tmp/qa_twin43/custom_twin.conf`（`460800` / `0.0.0.0:18082`）启动、`--status`、`--stop` 闭环 PASS；
  - `--config /tmp/qa_twin43/custom_twin.conf --baud 921600 --port 18083` CLI 覆盖优先级验证（`921600` / `0.0.0.0:18083`）PASS；
  - 基于 POSIX PTY 的 `--mode hardware --uart <pty> --baud 921600 --port 18084` 启动、`--status`（匹配 `hardware`、`921600`、`0.0.0.0:18084`）与 `--stop` 闭环 PASS；
  - 连续两轮 `--mode sim --port 18080` 启动、`--status`、`--stop` 恢复闭环 PASS。

> **附：关于 `TWIN-43.md` / `ARCH` `revision: 9` 中 `verify_deploy_twin_sim_lifecycle` 命令的 Shell `&` 优先级提醒（供 `COORD`/`ARCH` 在触发 Docker QA Runner 前同步）**：
> 在 `TWIN-43.md` 第 177 行的单行 `&&` 链中：
> `... && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --stop && python3 -c "import os,pty,time; m,s=pty.openpty(); open(\"/tmp/qa_twin43/pty_path\",\"w\").write(os.ttyname(s)); time.sleep(25)" & PTY_HOLDER_PID=$! && ...`
> 由于 POSIX `sh`/`bash` 中裸 `&` 的语法优先级低于 `&&`（与 `;` 同级），Shell 会将 `&` 之前的**整条前置 `&&` 链**（含 `export PATH`、`cd /tmp/qa_twin43/soc-ap`、`FORCE_CURL_FAIL=1` 等耗时步骤）整体放入后台子 Shell 异步执行，同时立即在当前父 Shell（仍位于只读 `/workspace/soc-ap` 且未等待前置步骤完成）中并行启动 `&` 之后的语句，导致 2 秒后 `/tmp/qa_twin43/pty_path` 尚未生成而报错。
> 建议将上述 `python3 -c "..." & PTY_HOLDER_PID=$! && for _ in $(seq 1 20)...` 与 `(kill "${PTY_HOLDER_PID}" 2>/dev/null || true)` 替换为 Python 内部 `os.fork()` 后台化（不含裸 Shell `&`）：
> ```bash
> python3 -c "import os,pty,time; m,s=pty.openpty(); open(\"/tmp/qa_twin43/pty_path\",\"w\").write(os.ttyname(s)); pid=os.fork(); (open(\"/tmp/qa_twin43/pty_pid\",\"w\").write(str(pid)), os._exit(0)) if pid>0 else time.sleep(25)" && bash tools/deploy_twin.sh --mode hardware --uart "$(cat /tmp/qa_twin43/pty_path)" --baud 921600 --port 18084 && bash tools/deploy_twin.sh --status --port 18084 | grep -E "hardware|921600|0\.0\.0\.0:18084" && bash tools/deploy_twin.sh --stop --port 18084 && (kill "$(cat /tmp/qa_twin43/pty_pid)" 2>/dev/null || true)
> ```
