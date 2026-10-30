# TWIN-18 双MCU运动/调平/断料状态接口调查与协议对账执行与验收报告 (Run 03 退修整改)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-18` (双MCU运动/调平/断料状态接口调查与协议对账) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **执行角色** | `ENG-MC` (协同 `ENG-TH` 与 `ARCH`) |
| **当前轮次** | `run_03` (针对 run_02 独立 QA 审查意见落实退修) |
| **前序报告** | [`runs/run_02/qa_review_report.md`](../run_02/qa_review_report.md) (REJECTED) |
| **当前规范原件** | `project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md` |
| **当前候选 Commit** | `project-control: 1c38984827bd5b7f3f185193808bd61725f08f23` |
| **执行状态** | **Completed / Delivered (退修闭环完成，只读快照容器沙箱与真实分支元数据全量对齐)** |

---

## 1. 逐项整改与差异溯源表 (Finding Resolution Matrix)

| Finding ID | 缺陷根因 | 修复位置与差异 | 新增与修改测试 | 复现命令与实际结果 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`TWIN18-QA-02`** (Blocker) | `server_lock.json` 中的 `ref` 写成了非广告分支 `refs/heads/<commit_sha>`，破坏了服务器元数据真实性 | `project-control/tools/qa_runner/qa_runner.py`：<br/>升级 `build_server_lock_data`，自动将远程候选分支绑定为真实存在的 `refs/heads/main`（或 target 指定 ref），彻底杜绝虚假 ref 产生 | 运行 `qa_runner.py` 并检查输出的 `server_lock.json` | 所有四仓 ref 均为可由 `git ls-remote` 解析的真实 `refs/heads/main` |
| **`TWIN18-QA-05`** (Blocker) | QA 容器将 `/workspace` 挂载为 `RW=true`，不符合 delivery_and_coord_gate.md §3/§3.1 的只读候选快照隔离门禁 | `project-control/tools/qa_runner/qa_runner.py`：<br/>调整工作流为宿主机先完成隔离目录 checkout，随后以 `-v ...:/workspace:ro` 启动 Docker 容器，实现 100% 只读源码快照 | 执行 `docker inspect` 检查 mount 信息 | `Mode: "ro"`, `RW: false`，完全符合只读候选要求 |
| **`协议字段一致性说明`** | 审阅请求中出现的简写与文档原文存在细微标识差异 | 规范文档中统一并固定使用源码级标识符：<br/>- `grid_points_x` (1 字节)<br/>- `grid_points_y` (1 字节)<br/>- `z_offset_um[25]` (50 字节)<br/>总载荷严格锁定为 52 字节，与 §5、§6.2 保持 100% 逐字一致 | 静态断言与对账矩阵审查 | 52 字节与 25 点网格完全一致 |

---

## 2. 交付物 SHA256 校验码

| 交付文件路径 | 类型与描述 | SHA256 校验码 |
| :--- | :--- | :--- |
| [`project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md`](../../../../specs/mcu_motion_leveling_filament_interface_survey_20261029.md) | 双MCU运动/调平/断料调查与协议对账规范 (rev 2) | `596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea` |
