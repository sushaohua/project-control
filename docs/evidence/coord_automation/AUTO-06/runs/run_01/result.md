# AUTO-06 run_01 实施与验收结果报告

- **任务编号**: AUTO-06
- **运行轮次**: run_01
- **执行角色**: INTEGRATOR (系统集成工程师)
- **执行时间**: 2026-11-03
- **前置依赖**: AUTO-05 (已在 run_04 取得独立 Docker 沙箱与独立 Codex ARCH 双重 APPROVED 验收，已收件 Done)

---

## 1. 交付物清单与架构落地

按照 `coord_intake_dispatch_phase1_design_20261103.md` (rev 2 §4.2, §4.3, §4.4) 与任务卡要求，完成以下交付物开发：

1. **单实例用户态 systemd 服务文件**:
   - 路径: `project-control/config/coord_runner/ai-soc-coord-runner.service`
   - 特性: 配置 `ExecStart` 指向 `python3 -m tools.coord_runner --daemon --config ...`，`Restart=on-failure`，`RestartSec=5s`，绑定工作目录 `/home/sushaohua/workspace/ai_soc_project`，注入 `PYTHONPATH`、`PYTHONUNBUFFERED` 与 `PYTHONDONTWRITEBYTECODE`。
2. **受控服务生命周期 CLI 管理工具**:
   - 路径: `project-control/tools/coord_runner/service_ctl.py`
   - 特性: 提供 `install`, `uninstall`, `start`, `stop`, `restart`, `status`, `check_linger`, `verify_crontab` 8 项子命令，完整封装 systemctl 与 linger/crontab 检查。
3. **单元与验收自动化测试套件**:
   - 路径: `project-control/tools/test_coord_systemd_service.py`
   - 特性: 覆盖单元文件结构解析、CLI 生命周期模拟、Crontab 隔离门禁、**P1-14 连续 20 轮零空耗强断言**、stop/start/restart 权威恢复校验与 AST 门禁。
4. **服务运维手册**:
   - 路径: `project-control/docs/operations/coord_runner_systemd_service_20261103.md`
   - 特性: 详细记录 `systemd --user` 架构、CLI 操作、Linger 授权机制、WSL2 宿主休眠客观边界与 Crontab 隔离声明。

---

## 2. 关键判据验证

### 2.1 P1-14 零空耗断言实测 (Zero Idle Model Consumption)
在 `test_coord_systemd_service.py` 的 `P1_14_ZeroIdleModelConsumptionAndRecoveryTest` 中：
- 注入探针 Mock Executor 监控所有模型调用；
- 连续执行 10 轮空闲轮询周期（无待处理卡、队列为空）：模型调用次数严格为 0；
- 注入 `BLOCKED` 状态在途任务，执行 5 轮轮询：模型调用次数严格为 0；
- 注入 `COMPLETED` 任务，执行 5 轮轮询：模型调用次数严格为 0；
- 累计 20 轮轮询周期模型调用次数均为 0，完全满足 P1-14 零空耗强约束。

### 2.2 服务停止与重启权威恢复 (Stop/Start/Restart Recovery)
- 验证服务实例停止（模拟 SIGTERM 或 stop 操作）时释放排他 `flock` 并完整固化 SQLite / Checkpoint；
- 新实例启动拉起后，自动从 SQLite / Checkpoint 权威恢复在途任务、状态机状态与租约信息，无断点与数据丢失；
- 排他锁在服务停止后顺利释放，新实例可再次无竞争获取。

### 2.3 Crontab 严格隔离与保护
- 检查当前宿主真实的 `crontab -l`：确认用户既有的 `0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh` 完整保留；
- 确认没有向 crontab 注入任何 `coord_runner` 相关条目；
- 注入毒化测试用例（模拟 crontab 含有 `coord_runner`），门禁测试成功拦截并阻断。

### 2.4 Linger 状态核验
- 宿主机 `/var/lib/systemd/linger/sushaohua` 文件已存在；
- `loginctl show-user sushaohua --property=Linger` 返回 `Linger=yes`；
- `service_ctl.py check_linger` 自动检测结果返回 `linger_enabled: true`。

---

## 3. 测试与门禁执行证据

### 3.1 专用测试套件
```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_systemd_service.py' -v
```
**结果**: 12/12 PASS (Ran 12 tests in 0.296s, OK)

### 3.2 AST 代码规范门禁
通过 `test_systemd_tools_comply_with_ast_standards` 与 `test_all_coord_runner_modules_comply_with_ast_standards`：
- 自研 Python 函数 100% 保持 $\le 50$ 行；
- 自研 Python 函数入参 100% 保持 $\le 4$ 个；
- 违规数量: 0。

### 3.3 全量回归测试
- `test_coord_recovery.py`: 19/19 PASS
- `test_phase1_intake_acceptance.py`: 20/20 PASS
- `check_task_graph.py`: 0 errors

### 3.4 仓库物理隔离
- 仅在 `project-control` 目录内新增/修改文件；
- 严禁触碰 `soc-ap/`, `mcu-p3/`, `test_harness/`, `boot/*`，业务代码仓库变更行数严格为 0。
