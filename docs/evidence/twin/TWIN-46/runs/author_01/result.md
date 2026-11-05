# TWIN-46 作者实现与自检报告 (`run_id: author_01`)

## 1. 任务与角色绑定
- **任务 ID**: `TWIN-46` (`revision: 1`)
- **任务标题**: `TWIN-46 921600全栈配置化启动与MC/TH Debug↔Web UI双向链路对账集成验证`
- **执行角色**: `INTEGRATOR` (Session `71c0aa29-52a3-42ab-b8d5-1cb878087863`, `run_id: author_01`)
- **派单与收件角色**: `COORD` (`ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6`)
- **权威技术输入**:
  - `project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md` (`revision: 11`, SHA-256 `9300ae43010fa5e2e008610a2d108d5407d583410a207a3f7b72b70afccf9814`)
  - `project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md` (`revision: 2`, SHA-256 `c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec`)
- **前置已验收依赖版本**:
  - `TWIN-43` (`soc-ap@426d604e9ddcfdb3e95e94ecff4f699ae976fc95`, `qa_04`)
  - `TWIN-44` (`mcu-p3@f34a4b9d3ce03ec02824e1c54dd4dd3052386156`, `qa_06`)
  - `TWIN-45` (`mcu-p3@29d62ef1bb7cf33e334f7e58aae81717cd26c54f`, `qa_01`)

## 2. 候选提交与写权限核验
- **目标代码仓**: `test_harness` (`main` 分支)
- **基线提交 (`base_commit`)**: `ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414`
- **候选提交 (`candidate_commit`)**: `108158318581df366d133f556343d5367bd30cff`（已推送至 `origin/main`）
- **变更文件清单 (`git -C test_harness diff --name-only ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414..108158318581df366d133f556343d5367bd30cff`)**:
  - `hil/tools/debug_reconciliation_probe.py` (SHA-256: `46e85aa0385046cff33f7e8356ff4931e4bc653695c325810a324b743688d502`)
- **归档矩阵与证据 (`project-control`)**:
  - `project-control/docs/evidence/twin/TWIN-46/runs/author_01/reconciliation_matrix.md` (SHA-256: `c63b9f449019e3826c6934c0b958db08f3666564287d8069d9fda86d4fb0089e`)
  - `project-control/docs/evidence/twin/TWIN-46/runs/author_01/result.md`
- **隔离核验**: `soc-ap`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth` 保持零修改。

## 3. 核心实现与代码规范合规自检
1. **CLI 接口 100% 契约对齐（无未执行冗余分支）**:
   - 仅暴露 `--help` (`-h`)、`--self-test`、`--mc-log`、`--th-log`、`--ap-snapshot`、`--ap-url`、`--matrix-out`，全部 CLI 选项与代码分支在 `TWIN-46.verification.commands` 中 100% 覆盖执行。
2. **五类核心业务双向对账与反例拦截**:
   - 正例完整覆盖：
     1) 温度上报与设定（`bed_ddC`/`bed_set_ddC`、`nozzle_ddC`/`nozzle_set_ddC`、`adc_raw`、`pullup_sel`）；
     2) 归零与运动控制（`axes_mask`、`homed_mask`、`x_mm_x100`/`y_mm_x100`/`z_mm_x100`、`feed`、`motion_state`）；
     3) 5×5 调平网格（`op=GRID_READ`、`probe_idx`、`z_offset_um`、`grid_valid=1`、`status=DONE` 与 25 点 mesh 对账）；
     4) 进退丝与料槽切换（`op=LOAD`、`slot`、`active_slot`、`filament_present_mask`、`step_state=DONE`）；
     5) 打印作业状态机（`job_state`、`progress_permille`、`ack_seq`）。
   - 反例完整拦截：
     - 五类业务状态失配（`ap_mismatch.json`）精确识别失配类别并以退出码 `1` 拒绝；
     - `[MC-DBG]` / `[TH-DBG]` 出现 `dir=ERR` 或 `status=CRC_ERR|TIMEOUT|BAD_FRAME|TX_ERR|BAD_CMD` 时以退出码 `1` 拒绝；
     - `drop>0` 或 `trunc>0` 环形缓冲溢出/截断时以退出码 `1` 拒绝；
   - `OFFLINE` 断连哨兵值（`2147483646` / `32767`）与 `ui-gateway` 控制接口 `POST /api/v1/jobs/start`、`POST /api/v1/motion/home` HTTP `503` 锁定校验，以及故障后恢复为 `ONLINE` 五类对账 `PASS`。
3. **函数规模与入参硬性门禁**:
   - 经 Python AST 静态扫描核验，全部 24 个函数行数均 $\le 48$ 行（严守 $\le 50$ 行上限），入参个数均 $\le 4$ 个，仅依赖 Python 3.8 标准库。

## 4. 本地验证命令执行结果
| 命令 ID | 工作目录 | 退出码 | 结果摘要 |
| :--- | :--- | :--- | :--- |
| `run_debug_reconciliation_probe_selftest` | `test_harness` | `0` | `--help`、`--self-test`（生成 7 个确定性夹具）、`--mc-log`/`--th-log`/`--ap-snapshot` 正例、失配/CRC_ERR/drop>0 反例非 0 退出拦截、`OFFLINE` 哨兵值对账及恢复对账全部 `PASS` |
| `verify_fullstack_deploy_and_reconciliation` | `soc-ap` | `0` | `/tmp/qa_twin46` 可写副本下 `deploy_twin.sh --mode sim --port 18085` 全栈 5 目标编译启动、`--status` 探活、`--ap-url http://127.0.0.1:18085` 实测拉取 HTTP 快照/SSE 流并验证 `POST` 控制接口 HTTP `503` 锁定与五类对账/反例/恢复矩阵生成、`--stop` 优雅停止清理全部 `PASS` |
