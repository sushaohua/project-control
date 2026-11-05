# TWIN-46 作者实现与自检报告 (`run_id: author_02`)

## 1. 任务与角色绑定
- **任务 ID**: `TWIN-46` (`revision: 1`)
- **任务标题**: `TWIN-46 921600全栈配置化启动与MC/TH Debug↔Web UI双向链路对账集成验证`
- **执行角色**: `INTEGRATOR` (Session `2f8ea5d1-b0c3-46a7-a19f-2ca6b8983802`, `run_id: author_02`)
- **派单与收件角色**: `COORD` (`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`)
- **权威技术输入**:
  - `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 12`, SHA-256 `4ae7e578eb88a9e33ee63a357b3d72b0c0684f59ac1f529a56ca695208d41ae0`)
  - `project-control/docs/evidence/twin/TWIN-46/runs/qa_01/qa_review_report.md` & `final.json` (`qa_01` 4 项审阅发现)
- **前置已验收依赖版本**:
  - `TWIN-43` (`soc-ap@426d604e9ddcfdb3e95e94ecff4f699ae976fc95`, `qa_04`)
  - `TWIN-44` (`mcu-p3@f34a4b9d3ce03ec02824e1c54dd4dd3052386156`, `qa_06`)
  - `TWIN-45` (`mcu-p3@29d62ef1bb7cf33e334f7e58aae81717cd26c54f`, `qa_01`)

## 2. 候选提交与写权限核验
- **目标代码仓**: `test_harness` (`main` 分支)
- **基线提交 (`base_commit`)**: `ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414`
- **候选提交 (`candidate_commit`)**: `91942286e8f686ce044a6aa8fdb11270ff8f5624`（已推送至 `origin/main`）
- **变更文件清单 (`git -C test_harness diff --name-only ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414..91942286e8f686ce044a6aa8fdb11270ff8f5624`)**:
  - `hil/tools/debug_reconciliation_probe.py` (SHA-256: `92d9b665ca82fefd372b63daf8d40666034121e0d7f7328dc1efe25aed3c67fe`)
- **归档矩阵与证据 (`project-control`)**:
  - `project-control/docs/evidence/twin/TWIN-46/runs/author_02/reconciliation_matrix.md` (SHA-256: `68a686da30b9d6d920e6d74005cf8ae5384f0a6a4be8278c84ca9f50a8212550`)
  - `project-control/docs/evidence/twin/TWIN-46/runs/author_02/result.md`
  - 历史记录 `runs/author_01/` 与 `runs/qa_01/` 完整保留零改动。
- **隔离核验**: `soc-ap`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth` 保持零修改。

## 3. 针对 `qa_01` 4 项发现的逐项闭环说明

### 3.1 修复 Finding 1 & Finding 2：`--ap-url` 100% 真实运行态对账 + 921600 POSIX PTY 虚拟下位机驱动全生命周期闭环
1. **彻底移除 `--ap-url` 路径中的硬编码日志与默认快照回退**：
   - `--ap-url` 必须同时显式传入 `--mc-log <path>` 与 `--th-log <path>`（缺失时返回非 0 退出码 `2`），从磁盘读取真实 `[MC-DBG]` / `[TH-DBG]` 日志；
   - 在 `--ap-url` 代码路径中，**零调用** `build_default_mc_ok_log()`、`build_default_th_ok_log()`、`build_default_ap_ok_snapshot()`，并彻底移除了仅针对内存夹具的 `verify_additional_fault_injections()`；
   - `fetch_live_ap_snapshot(ap_url)` 100% 从运行态 `ui-gateway` 拉取：
     - `GET /api/v1/temperature/snapshot`
     - `GET /api/v1/temperature/stream`（解析 SSE `temp_update` 事件并强校验 `sse_json["system_status"] == snap_json["system_status"]` 且 `bed`/`tool` 的 `temperature_millic` 完全相等）
     - `GET /api/v1/jobs/status`
     - `GET /api/v1/leveling/mesh`
   - 当实时 `system_status` 为 `"NORMAL"`/`"ONLINE"` 时，实测调用 `POST /api/v1/filament/slots`（校验 HTTP `200` 且 `"status"=="ok"`, `"code"==0`），并完全由实时 HTTP/SSE 响应组装 `live_ap_snap`，调用 `reconcile_logs_and_snapshot(mc_text, th_text, live_ap_snap)` 对全部五类业务（温度 `temperature_millic`、归零运动坐标与掩码、`5×5` 二维调平网格、进退丝料槽、打印作业状态机及 `ack_seq`）逐项严格对账；
   - 当实时 `system_status` 为 `"OFFLINE"` 时，实测调用 `POST /api/v1/jobs/start` 与 `POST /api/v1/motion/home`，将真实 HTTP 状态码写入 `control_lock_http_status`，调用 `reconcile_logs_and_snapshot()` 进入 `reconcile_offline_snapshot()`。
2. **实现内置 921600 POSIX PTY 虚拟下位机控制器 `live_pty_ctl(action, work_dir, ap_url="")`**：
   - `start-pty`：创建伪终端并 `os.fork()` 后台守护进程监听 `master_fd`，将 `slave_name` 写入 `{work_dir}/pty_path`，按 MiniMCProto v2.0 协议（帧头 `0x55 0xAA`，CRC-16/CCITT-FALSE `poly=0x1021, init=0xFFFF`）实时解析 `forward_service_daemon` 在 `921600` 波特率下发送的 `0x01 GET_VERSION` 与 `0x14 TEMP_QUERY`（`dst=0x02` MC / `dst=0x03` TH），根据 `{work_dir}/pty_mode` 动态回复 `ONLINE` 正常温度帧（`600 ddC` / `2100 ddC`）或 `OFFLINE` 断连帧（`current_temp_deci_c=0x7FFE, status=1 DISCONNECTED`），并持久化最新真实帧 `seq`；
   - `drive-online`：切换 `pty_mode=ONLINE`，触发 `/api/v1/temperature/sample` 直至 `ui-gateway` 进入 `system_status == "NORMAL"` 且控制接口解锁（HTTP `200`），随后依次通过真实 HTTP API 执行 `jobs/start -> pause -> resume -> cancel`、`motion/home`、`motion/jog (X=12.5, Y=25.0, Z=0.4)`、`leveling/trigger`、`filament/slots`，并生成与实时网关状态及真实 PTY `seq` 同步的 `mc_live_ok.log`、`th_live_ok.log` 及反例 `mc_live_mismatch.log`、`mc_live_crc_err.log`、`mc_live_drop.log`；
   - `drive-offline`：切换 `pty_mode=OFFLINE`，触发 `/api/v1/temperature/sample` 直至 `ui-gateway` 衰退为 `system_status == "OFFLINE"`、温度打入哨兵值 `2147483646` 且 `POST /api/v1/jobs/start` 返回 HTTP `503`，生成含 `bed_ddC=32767` / `nozzle_ddC=32767` 的 `mc_live_offline.log` 与 `th_live_offline.log`；
   - `drive-recovery`：切换 `pty_mode=ONLINE`，触发 `/api/v1/temperature/sample` 直至 `ui-gateway` 恢复 `system_status == "NORMAL"`，重新执行五类业务动作并生成 `mc_live_recovery.log` 与 `th_live_recovery.log`；
   - `stop-pty`：安全终止 PTY 守护进程。

### 3.2 修复 Finding 3：离线哨兵值按单位严格区分校验与 HTTP `503` 强门禁
- 在 `reconcile_offline_snapshot(mc_sum, th_sum, ap_data)` 中：
  - `bed.get("temperature_millic") == 2147483646` 且 `tool.get("temperature_millic") == 2147483646`（严禁混用 `32767`）；
  - 若 `bed`/`tool` 中含 `"temp_deci_c"`，必须严格等于 `32767`（严禁混用 `2147483646`）；
  - `[MC-DBG]` 的 `bed_ddC`、`nozzle_ddC` 与 `[TH-DBG]` 的 `nozzle_ddC` 必须全部严格等于 `32767`（绝不放行 `600`/`2100` 等在线温度或 `2147483646`）；
  - `ap_data.get("control_lock_http_status")` 必须显式存在且严格等于 `503`（绝不放行 `504`、`200` 或缺失字段）。
- 在 `--self-test` 中新增 `ap_bad_offline.json`、错误单位哨兵值、HTTP `504`/`200` 以及 `mc_ok.log + ap_offline.json` 反例断言，全部验证拦截生效。

### 3.3 修复 Finding 4：5×5 调平网格二维形状严格校验
- 在 `check_category_leveling(mc_sum, ap_data)` 中，严格校验 `isinstance(grid, list) and len(grid) == 5` 且每一行均为长度为 `5` 的数值列表（排除 `bool`），彻底拒绝 `1×25`、`25×1` 或一维 25 元素畸形网格。
- 在 `--self-test` 中新增 `ap_bad_grid.json`（`[[0.0]*25]` `1×25` 形状）反例断言，验证 `check_category_leveling()` 精确拦截并返回 `passed == False`。

## 4. 代码规范与静态门禁核验
- **函数规模与入参硬性门禁**：经 Python `ast` 静态扫描核验，`test_harness/hil/tools/debug_reconciliation_probe.py` 全部 36 个函数行数均 $\le 46$ 行（严格满足 $\le 50$ 行门禁），入参个数均 $\le 4$ 个，全部具备中文 docstring，仅使用 Python 3.8 标准库。

## 5. 本地验证命令执行结果
| 命令 ID | 工作目录 | 退出码 | 结果摘要 |
| :--- | :--- | :--- | :--- |
| `run_debug_reconciliation_probe_selftest` | `test_harness` | `0` | `--help`、`--self-test`（含正例、5类失配、CRC_ERR、drop>0、离线哨兵正反例、错误单位哨兵/HTTP 504 反例、`1x25` 畸形网格反例）、CLI 文件对账正反例全部 `PASS` |
| `verify_fullstack_deploy_and_reconciliation` | `soc-ap` | `0` | `/tmp/qa_twin46` 可写副本下 `sim` 模式启动探活停止、`921600` POSIX PTY `hardware` 模式在线五类真实对账 PASS、失配/CRC_ERR/drop>0 在线反例非 0 拦截 PASS、在线 `OFFLINE` 故障注入（`2147483646` mdeg / `32767` ddC / HTTP `503`）PASS、故障后恢复 `NORMAL` 在线五类对账 PASS、优雅停止清理全部 `PASS` |
