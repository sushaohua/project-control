# AUTO-06 run_02 实施与返工验收结果报告

- **任务编号**: AUTO-06
- **运行轮次**: run_02 (rework_count: 1/2)
- **执行角色**: INTEGRATOR (系统集成工程师)
- **执行时间**: 2026-11-03
- **前置评审结论**: run_01 由宿主机独立 Codex QA 审签出具 `REJECTED`，提出 2 项客观质量缺陷。本轮针对两项缺陷实施完整返工。

---

## 1. 缺陷修复细节与架构实现

### 1.1 Finding 1 修复：进程级真实服务生命周期与 SIGTERM 优雅停止/重启恢复
- **缺陷表现**: run_01 中单测仅在单线程内手动调用 `release_process_lock()` 并恢复 checkpoint，未测试真实常驻后台服务进程对 SIGTERM（`systemctl stop` / `systemctl restart` 发送的实际信号）的信号拦截与优雅退出。
- **修复方案与实现**:
  - 在 [test_coord_systemd_service.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/test_coord_systemd_service.py) 中实现 `test_service_process_sigterm_stop_and_restart_recovery`；
  - 启动独立的 Python 常驻服务进程 `_run_daemon_worker`（运行 `runner.run_daemon(poll_interval=0.05)`），独占持有内核 `flock` 与在途任务快照；
  - 外部探针进程尝试获取同一文件锁，断言抛出 `ResourceConflictError` 证明锁已被后台服务强占；
  - 向该守护进程发送 `signal.SIGTERM`（真实模拟 `systemctl stop / restart`）；
  - 断言守护进程正常拦截 SIGTERM，将内存与状态落盘至 Checkpoint / SQLite WAL，安全释放内核 flock 并以状态码 0 退出；
  - 随后新实例启动（模拟 systemd 自动拉起重启服务），断言成功重新获取排他锁，并从权威快照完整恢复 `TASK-INFLIGHT`、版本号 `2`、状态 `InProgress` 及历史完成任务 `TASK-PREV`。

### 1.2 Finding 2 修复：Crontab 异常失败不可判定为 clean
- **缺陷表现**: `service_ctl.py:verify_crontab_isolation` 原代码在 `crontab -l` 返回非 0 时一律返回 `crontab_clean: True`，导致权限不足或命令错误时发生门禁穿透。
- **修复方案与实现**:
  - 修改 [service_ctl.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/coord_runner/service_ctl.py#L129-L140)：
    * 当 `rc != 0` 时，仅当输出明确包含 `"no crontab for"`（用户确实未配置任何 crontab）时，才判定为 `crontab_clean: True`；
    * 若为其他退出码或异常报错（如 permission denied, inaccessible, command not found 等），一律判定为 `crontab_clean: False` 并返回包含错误码与标准输出的结构化错误信息；
  - 在 `test_coord_systemd_service.py` 中补充 2 个专用用例：
    * `test_crontab_command_failure_reports_not_clean`: 模拟 crontab 报错退出，验证返回 `crontab_clean: False`；
    * `test_absent_crontab_reports_clean`: 模拟用户无 crontab（"no crontab for sushaohua"），验证返回 `crontab_clean: True`。

---

## 2. 门禁验证与测试证据

### 2.1 专用测试套件全量通过
执行命令：
```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_systemd_service.py' -v
```
**结果**: 14/14 项测试 100% 全部通过 (Ran 14 tests in 0.391s, OK)
- `test_service_process_sigterm_stop_and_restart_recovery`: PASS (实测真实 OS 进程 SIGTERM 停止、flock 释放与重启权威恢复)
- `test_p1_14_zero_idle_model_consumption_across_consecutive_cycles`: PASS (连续 20 轮空闲/阻塞轮询周期模型调用次数严格为 0)
- `test_real_crontab_isolation`: PASS (宿主既有 `sync_md.sh` crontab 完整原封未动)
- `test_forbidden_crontab_entry_detected`: PASS (毒化注入拦截有效)
- `test_crontab_command_failure_reports_not_clean`: PASS (系统异常不可判定为 clean)
- `test_absent_crontab_reports_clean`: PASS (无 crontab 正常通过)
- `test_required_sections_present` / `test_service_exec_and_restart_directives` / `test_working_directory_and_environment`: PASS
- `test_install_and_uninstall_lifecycle` / `test_control_service_actions` / `test_get_service_status_installed_and_missing`: PASS
- `test_check_user_linger_detection`: PASS
- `test_systemd_tools_comply_with_ast_standards`: PASS

### 2.2 AST 代码规范检查
- 自研 Python 函数 100% $\le 50$ 行；
- 自研 Python 函数参数 100% $\le 4$ 个；
- 违规数量: 0。

### 2.3 全量回归验证
- `test_coord_recovery.py`: 19/19 PASS
- `test_phase1_intake_acceptance.py`: 20/20 PASS
- `check_task_graph.py`: 0 errors

### 2.4 仓库边界约束
- 修改与新增文件 100% 局限在 `project-control` 白名单内；
- 业务代码仓库（`soc-ap/`, `mcu-p3/`, `test_harness/`, `boot/*`）修改行数严格为 0。
