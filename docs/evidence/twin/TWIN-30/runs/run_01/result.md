# TWIN-30 VMware全流程离线打印闭环集成验证与首版收件交付报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-30` (VMware全流程离线打印闭环集成验证与首版收件) |
| **所属工作包** | `TASK-010` (验收首个多 Agent 端到端试点) |
| **执行角色** | `INTEGRATOR` (整机集成与端到端验证工程师) |
| **当前轮次** | `run_01` (全流程首版闭环交付与自检) |
| **代码基线** | `soc-ap: 674e7336f924c2f297c439417a0011adc12427fa` |
| **交付候选** | `soc-ap: 7bb05218c39d6852cac5e8d86db845dbbedd7064` |
| **执行状态** | **Completed (8/8 核心集成套件 100% 通过，无编译警告，严守 C/C++ 编码门禁)** |

---

## 1. 任务背景与集成概述 (Integration & Solution Summary)

根据首版本地正常打印闭环决策（U-D02）与纯逻辑空跑底线（选项 A / U-D03），以及 U-D01 七项首版子范围要求，本项目在 VMware 虚拟化双环境中端到端串联离线作业引擎、流式执行器与权威状态机。

本任务（`TWIN-30`）实现并验证了首版端到端全流程闭环集成测试套件，全面拉通以下软件链条：
1. **未回零防线与 G28 初始化**：初始未回零状态下硬性拦截启动打印（返回 `AISOC_JOB_ERR_NOT_HOMED`）；执行 G28 后微米坐标清零、回零掩码就绪，允许启动；
2. **选项 A 纯逻辑空跑强电锁死拦截**：连续输入 M4/M5/M6/M7 加热指令，加热占空比强制锁死为 0%，安全跳过并正常步进，打印安全审计日志；
3. **CoreXY G0/G1 微米级走线调度与 MC 0x16 报文双向同步**：精确累加微米坐标（`pos_x_um`, `pos_y_um`, `pos_z_um`, `pos_e_um`），并与 MC 固件 `0x16` 20 字节二进制坐标报文实现双向反向同步与状态映射；
4. **多通道混色比例在环调度**：支持 M163/M164 混色比例设置（如 50:50），记录通道权重，并拦截非法权重和超限通道；
5. **在环异常中断与安全挂起**：
   - 走线过程中注入 HMS `0x3001`（断料告警），执行器瞬时安全挂起暂停，进给停止，状态转为 PAUSED，暂停期间走线指令被拦截；
   - 模拟更换耗材并调用 `resume`，状态无缝恢复为 PRINTING，走线继续步进；
   - 走线过程中注入 `M112` 急停信号，瞬时熔断进入 FAULT/ERROR，强电占空比硬清零，后续指令被强力拒绝（`AISOC_JOB_ERR_ESTOP_ACTIVE`）；
   - 执行显式 `clear_estop` 清除急停，恢复常态 IDLE；
6. **128B 原子快照与完成态收敛**：步进至末行，任务状态成功收敛为 COMPLETED，千分比进度达到 1000（100.0%），原子导出 128B 快照并逐字段核验完整性；
7. **双 MCU 固件版本拓扑与状态机联调模拟**：模拟 `devices.mc` 与 `devices.th` 版本帧，验证四态时序衰退状态机（ONLINE / STALE / OFFLINE / QUERY_FAILED）与重连自愈。

---

## 2. 详细技术实现与测试套件结构

### 2.1 集成测试套件结构 (`soc-ap/tests/integration/test_first_release_print_loop.c`)
套件包含 8 个针对性集成测试套件与 `main` 入口：
- `test_homing_guard_and_g28_initialization`：未回零禁止启动与 G28 回零逻辑验证；
- `test_option_a_dry_run_heating_safeguard`：4 条加热指令 0% 强电锁死拦截验证；
- `test_corexy_motion_and_mc_telemetry_sync`：微米走线调度与 MC 0x16 20B 报文双向同步；
- `test_multichannel_color_mixing_ratio`：混色比例设置与合法性边界覆盖；
- `test_in_loop_alarms_and_estop`：HMS 0x3001 断料挂起/恢复与 M112 急停自锁/复位；
- `test_atomic_128b_snapshot_and_completion`：100% 进度收敛与 128B 快照核验；
- `test_dual_mcu_version_simulation`：MC/TH 双固件版本拓扑与 4 态衰退状态机模拟；
- `test_complete_end_to_end_loop`：串联全部特性的端到端完整闭环验证。

### 2.2 编码门禁达标情况
- **函数规模**：最长函数 41 行，全部函数均 $\le 50$ 行；
- **参数个数**：全部函数参数个数均 $\le 4$ 个；
- **指针与内存安全**：零堆内存分配（无 malloc/free/new），禁止指针压缩技巧与二级以上指针；
- **防御性空指针校验**：所有对外与公用函数首行执行 Guard Clause 空指针防御；
- **位运算安全**：显式移位与标准位掩码，无硬编码魔数。

---

## 3. 交付清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/tests/integration/test_first_release_print_loop.c` | 首版全流程闭环集成测试用例 | `b4efbab6bbc5c582fdebe457d63d9ae6feac955d575e796936cc02fa1699204c` |
