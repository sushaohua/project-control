# TWIN-53 作者自检报告 (`author_02`, `INTEGRATOR`)

## 1. 任务与基线绑定
- **任务 ID**：`TWIN-53`（对应 `ISS-20261105-003` / `DEM-20261105-003`）
- **执行角色**：`INTEGRATOR` (`7812a1f6-5006-4971-a954-802f855cf20a`, `run_id: author_02`)
- **架构方案依据**：`project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md` §2.3 & §3.4 (`revision: 3`, SHA-256: `a232e1ab0dbbf8f9eb188efbec5a486ff251400ee970d0b2446d5eab63efb1c4`)
- **已读规则与来源登记 (`read_sources`)**：
  - `soc-ap/AGENTS.md` + `soc-ap/.agents/rules/repository.md` + `soc-ap/.agents/rules/shared/SOURCE.json` (`source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)
  - `project-control/.agents/rules/repository_rule_sources.json`
  - `project-control/.agents/rules/repository_rule_boundaries.md`
  - `project-control/.agents/rules/c_cpp_coding_standard.md`
  - `project-control/.agents/rules/code_documentation_standard.md`
  - `project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md`
  - `project-control/docs/evidence/twin/TWIN-53/runs/qa_01/qa_review_report.md`
- **源码基线与候选提交**：
  - `base_commit` (`soc-ap`): `ad2538ae7f4834cac98be97e08b055f80eb81cfc`
  - `candidate_commit` (`soc-ap`): `87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a` (`main` HEAD: `79932746d225bb115010c5545ef3f7499482e137`)
- **修改与新增文件列表（严格符合 `allowed_paths`）**：
  - `soc-ap/tools/deploy_twin.sh`
  - `soc-ap/tools/twin_build/test_deploy_daemon_survival.sh`

## 2. `author_02` 返工修复内容摘要
针对 `qa_01`（独立 Codex 审阅会话 `01a1a9a2-b28f-7d13-badc-7ebf445cdc3f`）指出的两项测试断言不充分问题，在 `soc-ap/tools/twin_build/test_deploy_daemon_survival.sh` 与 `soc-ap/tools/deploy_twin.sh` 中完成如下加固：
1. **真实 `SIGHUP` 投递与 `setsid` 会话脱离双重断言（`launch_in_subshell_and_sighup` & `verify_sighup_and_session_isolation`）**：
   - 在启动子会话部署完成后写入就绪标志并保持子会话存活（`exec sleep 30`），向存活的调用方子会话进程组真实发送 `os.killpg(proc.pid, signal.SIGHUP)`（不忽略异常），使其因 `SIGHUP` 退出；
   - 对 4 个守护进程 PID 逐一校验其 `/proc/<pid>/stat` 的 `PGID`/`SID` 与子会话 `PGID` 不同（证明 `setsid` 会话脱离生效），校验 `/proc/<pid>/status` 的 `SigIgn`/`SigCgt` SIGHUP 免疫位，并直接向全部 4 个守护进程 PID 发送 `kill -HUP "${pid}"`（不加 `|| true`），等待 `500ms` 后再次验证 4 个进程全部存活（`State=S/R`，`fd/0 -> /dev/null`）。
2. **启动崩溃清理与 `--stop` 进程/PID 文件回收后置条件显式断言（`verify_pids_terminated_and_files_removed` & `verify_stop_reclaims_all_daemons`）**：
   - 在启动期崩溃负向测试（Negative check 2，`deploy_twin.sh` 返回非 0）之后，显式校验全部 4 个守护进程 PID 已终止且 4 个 `.pid` 文件已被清理（`! -e`）；
   - 在测试末尾重新启动 4 个守护进程并执行 `deploy_twin.sh --stop`，显式对记录的 4 个守护进程 PID 逐一校验进程已终止（`! kill -0` 或 `Z` 态）且 4 个 `.pid` 文件均不存在（`! -e`）。

## 3. 自检命令与客观输出
```text
=================================================================
[TWIN-53] Running deploy_twin.sh Daemon Survival & SIGHUP Tests...
=================================================================
  [OK] dbus.pid (PID=3795946, State=S, fd/0=/dev/null)
  [OK] forward.pid (PID=3795951, State=S, fd/0=/dev/null)
  [OK] device_manager.pid (PID=3795952, State=S, fd/0=/dev/null)
  [OK] ui_gateway.pid (PID=3795954, State=S, fd/0=/dev/null)
  [OK] SIGHUP delivered to all 4 daemons and caller session; all 4 survived.
  [RUNNING] dbus-daemon (PID: 3795946)
  [RUNNING] forward_service_daemon (PID: 3795951)
  [RUNNING] device_manager_daemon (PID: 3795952)
  [RUNNING] ui-gateway (PID: 3795954)
  [HEALTH ] HTTP Probe http://127.0.0.1:18093/api/v1/state -> HTTP 200 OK
  [OK] HTTP /api/v1/state (200) & /api/v1/temperature/snapshot (200)
  [OK] Negative check 1: --status correctly failed after forward_service_daemon crash.
  [OK] Negative check 2: deploy_twin.sh rejected startup crash (exit 139) without false positive.
  [OK] Negative check 2 cleanup verified: all daemons terminated and PID files removed.
[STOP] Stopping ui-gateway (PID: 3796364)...
[STOP] Stopping device_manager_daemon (PID: 3796362)...
[STOP] Stopping forward_service_daemon (PID: 3796361)...
[STOP] Stopping dbus-daemon (PID: 3796356)...
[STOP] All AI-SoC VMware Twin services stopped and PID files cleaned.
  [OK] --stop verified: all 4 daemon PIDs terminated and all PID files removed.
=================================================================
[TWIN-53] ALL Daemon Survival & Crash Detection Tests PASSED!
=================================================================
```
