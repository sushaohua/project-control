# COORD Runner 用户态 systemd 服务运维与部署手册

**文档版本**: rev 1  
**生效日期**: 2026-11-03  
**适用范围**: Milestone 3 (`AUTO-06`) 定时调度与后台持续推进服务部署  
**责任角色**: INTEGRATOR / DevOps / Operator  

---

## 1. 架构目标与设计原则

根据 `coord_intake_dispatch_phase1_design_20261103.md` (rev 2 §4.2, §4.3) 及确认单条款 `P1-14`：
1. **单实例守护进程**：通过 Linux `systemd --user` 用户级服务单元部署，实现单一守护进程常驻，避免多实例竞态。
2. **权威恢复对齐**：复用外置 SQLite WAL 存储（`~/.local/share/ai_soc_coord_runner/state.sqlite3`）与 `fcntl.flock` 单实例排他锁（`coord_runner.lock`）。
3. **零空耗强门禁 (P1-14)**：在无新输入、无版本变更、无回执、无到期动作的轮询周期内，调度器仅执行轻量级本地文件与 SQLite 扫描，**模型调用次数严格为 0**。
4. **既有环境零破坏**：用户既有 crontab（特别是 `0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh`）完全隔离，严禁以任何方式修改或写入 cron。

---

## 2. 服务配置与单元文件

单元文件位于代码库权威配置路径：
`project-control/config/coord_runner/ai-soc-coord-runner.service`

### 2.1 单元定义
```ini
[Unit]
Description=AI SoC COORD Task Runner Daemon (Single Instance User Service)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/sushaohua/workspace/ai_soc_project
Environment="PYTHONPATH=/home/sushaohua/workspace/ai_soc_project/project-control"
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONDONTWRITEBYTECODE=1"
ExecStart=/usr/bin/python3 -m tools.coord_runner --daemon --config project-control/config/coord_runner/coord_config.yaml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=default.target
```

---

## 3. 部署与运维 CLI 工具 (`service_ctl.py`)

受控运维脚本位于：
`project-control/tools/coord_runner/service_ctl.py`

### 3.1 常用操作指令

| 操作 | CLI 指令 | 等效原生 systemd 指令 |
| :--- | :--- | :--- |
| **安装服务** | `python3 project-control/tools/coord_runner/service_ctl.py install` | 拷贝至 `~/.config/systemd/user/` 并执行 `systemctl --user daemon-reload` |
| **启动服务** | `python3 project-control/tools/coord_runner/service_ctl.py start` | `systemctl --user start ai-soc-coord-runner.service` |
| **停止服务** | `python3 project-control/tools/coord_runner/service_ctl.py stop` | `systemctl --user stop ai-soc-coord-runner.service` |
| **重启服务** | `python3 project-control/tools/coord_runner/service_ctl.py restart` | `systemctl --user restart ai-soc-coord-runner.service` |
| **查看状态** | `python3 project-control/tools/coord_runner/service_ctl.py status` | `systemctl --user status ai-soc-coord-runner.service --no-pager` |
| **卸载服务** | `python3 project-control/tools/coord_runner/service_ctl.py uninstall` | `systemctl --user stop` + `disable` + 删除 unit 文件 + `daemon-reload` |
| **检查 Linger** | `python3 project-control/tools/coord_runner/service_ctl.py check_linger` | 检查 `/var/lib/systemd/linger/sushaohua` 或 `loginctl show-user` |
| **验证 Crontab 隔离** | `python3 project-control/tools/coord_runner/service_ctl.py verify_crontab` | 检查 `crontab -l` 确保无任何 `coord_runner` 污染条目 |

---

## 4. 用户常驻会话 (Linger) 与权限边界

### 4.1 Linger 授权机制
默认情况下，Linux 用户会话在登出（SSH 断开）后，其 `systemd --user` 实例会被系统停止。为了让后台调度服务能够持续运行，必须开启 linger：
```bash
sudo loginctl enable-linger sushaohua
```

### 4.2 Linger 状态核验
- **文件检查**：`/var/lib/systemd/linger/sushaohua` 存在。
- **命令行检查**：`loginctl show-user sushaohua --property=Linger` 输出 `Linger=yes`。
- **当前状态**：宿主机当前已确认启用 linger。

---

## 5. WSL2 宿主休眠客观边界与恢复保证

1. **客观物理边界**：
   - 当前工作空间运行在 Windows WSL2 (Ubuntu Linux) 环境。
   - 当 Windows 宿主机进入睡眠或休眠状态时，WSL2 虚拟内核会被操作系统挂起，CPU 时钟与调度进程暂停。
2. **唤醒后恢复保证**：
   - 宿主机唤醒后，WSL2 内核恢复运行，`systemd --user` 服务自动唤醒。
   - 如果进程因电源管理异常退出，`Restart=on-failure` 及 `RestartSec=5s` 会触发 systemd 自动拉起。
   - 重启时，`runner.py` 启动阶段执行 `restore_from_checkpoint()` 与 `StateStore` 恢复，恢复在途任务、租约状态与队列游标，实现不断点丢失。

---

## 6. Crontab 严格隔离声明

- **绝对零触碰原则**：系统严禁向用户 crontab 注入任何 `coord_runner` 调度指令。
- **既有业务保护**：用户既有的自动化脚本：
  ```cron
  0,30 * * * * /bin/bash /home/sushaohua/scripts/sync_md.sh
  ```
  受到测试套件 `test_coord_systemd_service.py` 中的 `CrontabIsolationGateTest` 严密门禁保护，任何修改或污染均会导致门禁 CI 阻断。

---

## 7. 验收与健康检查

执行自动化验收测试套件：
```bash
cd project-control
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_systemd_service.py' -v
```
预期结果：
- 15 项测试 100% PASS。
- 覆盖 unit 文件格式、CLI 生命周期、crontab 隔离门禁、P1-14 连续 20 轮空闲零模型调用断言、stop/restart 恢复及 AST 代码规范。
