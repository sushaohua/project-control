# CR-11 全流程验收、交接与版本锁文件同步执行记录 (Run 01)

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-11` (全流程验收、交接与版本锁文件同步) |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` / `workflow-replan-20261028` |
| **执行角色** | `COORD` ＋ `INTEGRATOR` |
| **独立审阅会话** | `codex-cr-11-qa` (Model: `gpt-6-luna`, Role: `QA`) |
| **复核审阅会话** | `codex-cr-11-arch` (Model: `gpt-6-luna`, Role: `ARCH`) |
| **前置任务闭环** | `CR-12` (Done), `CR-08` (Done), `CR-09` (Done), `CR-10` (Done) |
| **交付目标** | 1. 逐票接受证据与原 MS 里程碑范围对账<br>2. 五仓真实 Commit 与制品 SHA-256 最终锁定<br>3. 权威交接文档 [`HANDOFF_20261028.md`](../../../../docs/handoff/HANDOFF_20261028.md) 发布<br>4. 任务状态更新与图结构完整性自检 |
| **验收结论** | **APPROVED (级联纠偏恢复流水线全量闭环，版本锁文件已同步锁定，具备开启下一增量条件)** |

---

## 1. 级联恢复全链路流水线（CR-12 $\to$ CR-08 $\to$ CR-09 $\to$ CR-10）执行对账

| 阶段 / 任务 | 交付物与核心成果 | 签署角色与结论 | 证据位置 |
| :--- | :--- | :--- | :--- |
| **CR-12 (集中对账)** | 产出复用矩阵 `reuse_matrix.md`，确立 AP、MC、TH、测试向量与探针工具全量可复用基线 | ARCH / QA: **APPROVED** | [`docs/evidence/cascade_recovery/CR-12/result.md`](../CR-12/result.md) |
| **CR-08 (候选装配与SOP)** | 冻结 `ap_mc_th_readonly_candidate.yaml` 与五阶段实物联调 SOP，选定 SWD 安全烧录路径 | INTEGRATOR / ARCH / QA: **APPROVED** | [`docs/evidence/cascade_recovery/CR-08/result.md`](../CR-08/result.md) |
| **CR-09 (工程联调与消缺)** | 排除 ModemManager 竞争、TH 扇区 127 锚点缺失、MC DMA 标志丢失、Marlin 存量吞帧冲突等现场缺陷；完成真机双跳穿透 | INTEGRATOR: **DONE** | [`docs/evidence/cascade_recovery/CR-09/result.md`](../CR-09/result.md) |
| **CR-10 (独立真实 HIL 复验)** | 40 轮无间断实物压测（0.0% 丢包），正向 CAS-POS-001~004 与负向 CAS-NEG-001/010 全通；严格满足 HW-G1~HW-G6 零虚拟化铁律 | QA / ARCH: **APPROVED** | [`docs/evidence/cascade_recovery/CR-10/result.md`](../CR-10/result.md) |

---

## 2. 原始 MS 里程碑范围继承与剩余未覆盖项矩阵 (MS Scope Reconciliation)

根据 `workflow_replan_20261028.md` 规定，CR-10 的最小 GET_VERSION/PING 和故障恢复**不能自动关闭温度、完整 TH 状态、团队协作及目标 SoC 的未覆盖验收**。以下明确区分已接受范围与剩余项：

| 里程碑 | 原设计完整范围 | CR 恢复流水线已接受范围 | 剩余未覆盖范围 (待后续增量排期) |
| :--- | :--- | :--- | :--- |
| **MS-07** | 双 MCU 最小级联与通信回显 | **已接受**: 物理 UART 链路通畅、原生双向透明路由、GET_VERSION 与 PING 命令双跳闭环 | 温度流回显、喷头传感器数据解析、高级运控指令透传 |
| **MS-14** | 双 MCU 原型构建与初步联调 | **已接受**: AP ↔ MC ↔ TH 双跳硬件在环连通、基础通信稳定、时延抖动满足运控裕量 | 运动控制插补联动、挤出机同步步进驱动 |
| **MS-15** | 工具头与运控双向状态同步 | **已接受**: 心跳探活 PING/PONG、队列状态回传 (`rx_fifo_free_units`) | 细粒度加热棒 PWM 状态、霍尔断料检测事件上报 |
| **MS-16** | 异常故障注入与鲁棒性验证 | **已接受**: TH 单端硬件级切断 (CAS-NEG-001)、超时保护 (300ms) 及秒级自愈恢复 | 线路高噪声误码恢复、掉电临界保护、固件非法篡改拦截 |
| **MS-17** | 双 MCU 固件 OTA 安全升级与校验 | **未接受**: 本轮采用 SWD 探针规避升级风险 (CR-07 已解耦) | 升级管理器容量治理、ACK 关联校验、固件签名预检 (待 CR-07) |
| **MS-21** | 完整物理在环 FDM 系统端到端验收 | **已接受**: 只读级联基础通信底座 | 完整打印作业执行、三总线与业务映射、UI 与云端控制闭环 |

---

## 3. 五仓最终恢复提交与制品指纹锁定 (Repository Commit & Artifact Lock)

### 3.1 各独立 Git 仓库提交锁定
1. **`ai-soc-workspace` (顶层入口仓)**:
   - Branch: `main`
   - Commit: `95ea9d2` (`chore: update locked commit for project-control after CR-10`)
   - Remote: `ssh://git@192.168.77.113:2222/sushaohua/ai-soc-workspace.git`
2. **`project-control`**:
   - Branch: `main`
   - Commit: `16bb5b5` (`docs(cr-10): complete independent real HIL verification and record acceptance`)
   - Remote: `ssh://git@192.168.77.113:2222/sushaohua/project-control.git`
3. **`soc-ap`**:
   - Branch: `main`
   - Commit: `4445c8fedc21bafef5e6c971fcb54cec703f0e71`
   - Remote: `ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git`
4. **`mcu-p3`**:
   - Branch: `feat/soc-debug`
   - Commit: `1246ea9cb441d074ea444f53320f5632fefcd503`
   - Remote: `ssh://git@192.168.77.113:2222/sushaohua/mcu-p3.git`
5. **`test_harness`**:
   - Branch: `main`
   - Commit: `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb`
   - Remote: `ssh://git@192.168.77.113:2222/sushaohua/test_harness.git`

### 3.2 交付物与可执行二进制制品 SHA-256 (锁定对应 RC2 候选清单)
- `soc-ap/build/host/bin/soc-ap`: `1e0e0263c90c658e8026e1d5a5dd51349b411831575d4be2b7aec42fbd62d6e1` (41,720 字节)
- `mcu-p3/motion-controller-mcu/build/fw_mc.bin`: `8cddff04aab41506fa2d87e3f352549b068c0c13d3e5ba4cd937b741ea0118d0` (369,724 字节，含 128B Trailer)
- `mcu-p3/motion-controller-mcu/build/Marlin_AT32.bin`: `ff30795e8746a8344ecae4020640a63e43d1388b588cbcca449c2b680fb5963a` (369,596 字节代码载荷)
- `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin`: `5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d` (71,176 字节)
- `mcu-p3/color-engine-mcu/io_toggle/build/anchor.bin`: `660d9e6f341c8207a4caac8903f4666a4d67e55107dc4300cf4bd9411ead2352` (140 字节，Sector 127 签名锚点)
- `test_harness/test_cases/cascade/query_cases.json`: `64d1377ae46bff3795eab51d4829b4a50fd8a99b668f0c853046ddc0d878fcd2`

---

## 4. 任务状态与图结构校验

1. 执行结构校验:
   `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace . --check-done CR-11`
   - 结果: 79 张规范任务卡解析成功，0 错误，0 循环依赖，exit_code = 0。
2. 同步更新看板 `KANBAN.md`，CR 恢复系列全部 5 张核心卡（CR-12, CR-08, CR-09, CR-10, CR-11）全部置为 `Done`。
