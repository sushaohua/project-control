# TWIN-23 离线作业流式空跑与运控执行器交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-23` (离线作业流式空跑与运控执行器) |
| **所属工作包** | `TASK-011` (实现离线作业引擎和混色样例) |
| **执行角色** | `ENG-STATE / ENG-JOB` (离线作业流与运控状态工程师) |
| **当前轮次** | `run_01` (全功能首轮交付与自检闭环) |
| **代码基线** | `soc-ap: cb70d59e949396f45aec94d33ae23cab75beb282` |
| **交付候选** | `soc-ap: 674e7336f924c2f297c439417a0011adc12427fa` |
| **执行状态** | **Completed (8/8 单元测试与 6/6 回归测试 100% 通过，无编译警告，严守 C/C++ 编码门禁)** |

---

## 1. 任务背景与方案概述 (Problem & Solution Summary)

根据首版打印闭环决策（U-D02）与双 MCU 真实探针/运控现状对账（TWIN-18），首版本地打印在 VMware 虚拟化双环境上进行端到端闭环验证。为确保绝对电气安全：
1. **严格贯彻选项 A (Option A) 纯逻辑空跑基线**：上位机强电加热占空比硬锁死为 0%，拦截一切加热指令（M4/M5/M6/M7），彻底杜绝虚机与台架空跑期间的起火或烧毁风险；
2. **继承 TWIN-17 离线作业引擎并扩展执行器**：实现流式 Gcode 逐行解析与状态推进、G28 回零前置门禁、行号跟踪与千分比进度导出；
3. **对接 TWIN-21 运控坐标契约**：运控流式走线（G0/G1）解析为微米级坐标推进，严格对齐 MC 固件 `0x16` 响应的 20 字节二进制坐标报文格式（`pos_x_um`, `pos_y_um`, `pos_z_um`, `feedrate_mm_s`, `status_flags`）；
4. **集成 TWIN-19 全机 HMS 0x3001 告警**：断料告警瞬时触发任务安全挂起暂停，进给停止，等待上层干预恢复；
5. **集成急停熔断与自锁保护**：接收 M112 指令或急停信号时瞬时熔断，处于急停状态期间硬性拒绝一切走线与加热指令，必须显式调用清除急停后方可复位；
6. **规范化 128B 权威快照导出**：支持向状态管理器及上层遥测总线原子导出 128 字节二进制状态快照。

---

## 2. 详细技术改造与实现细节 (Implementation Details)

### 2.1 执行器核心契约 (`soc-ap/contracts/twin/job/job_executor.h`)
- 定义 `aisoc_job_executor_state_t` 结构体，总长 128 字节，包含 `base_engine`（TWIN-17 引擎）、四轴微米坐标、进给速度、选项 A 空跑锁、HMS 告警标志、G28 回零就绪标志及混色百分比；
- 公开 13 项标准执行器接口：
  - `aisoc_job_executor_init`：显式两阶段初始化，绑定空跑安全锁；
  - `aisoc_job_executor_start`：任务启动（强制校验 G28 回零就绪卫语句）；
  - `aisoc_job_executor_feed_line`：逐行流式解析与指令分发；
  - `aisoc_job_executor_pause` / `aisoc_job_executor_resume` / `aisoc_job_executor_cancel`：暂停、恢复与取消；
  - `aisoc_job_executor_trigger_estop` / `aisoc_job_executor_clear_estop`：急停熔断与自锁恢复；
  - `aisoc_job_executor_inject_hms`：HMS 0x3001 断料及其他故障注入并联动安全挂起；
  - `aisoc_job_executor_set_homed`：回零状态同步；
  - `aisoc_job_executor_set_mixing_ratio`：混色比设置（校验 0~10000 范围）；
  - `aisoc_job_executor_sync_mc_position`：反向同步下位机 MC 0x16 20 字节二进制坐标报文；
  - `aisoc_job_executor_export_snapshot`：导出 128 字节固定尺寸快照。

### 2.2 执行器逻辑与硬性门禁保障 (`soc-ap/contracts/twin/job/job_executor.c`)
- **选项 A 空跑加热拦截 (`handle_heating_cmd`)**：当 `is_dry_run_locked` 为真时，拦截 M4/M5/M6/M7 指令，强制将加热占空比与目标温度重置为 0，打印安全提示并安全步进进度；
- **微米级坐标更新 (`handle_linear_move`)**：解析 G0/G1 坐标，计算微米差值并累加进给轴 `pos_e_um`；
- **回零保护 (`handle_homing_cmd`)**：解析 G28 指令，重置三轴微米坐标为 0 并置 `g28_homed = true`；
- **编码规范约束**：全文件共 19 个函数，每个函数行数均 $\le 36$ 行（硬性门禁 $\le 50$ 行）；参数个数均 $\le 2$ 个（硬性门禁 $\le 4$ 个）；所有对外函数首行均为防御性空指针校验（Guard Clause）；零动态堆内存分配。

### 2.3 单元与集成测试套件 (`soc-ap/tests/job/test_job_executor.c`)
- `test_init_and_null_guards`：空指针校验与初始化门禁 100% 覆盖；
- `test_homing_guard_and_g28`：未回零禁止启动与 G28 回零逻辑覆盖；
- `test_option_a_dry_run_heating_interception`：选项 A 加热指令拦截与占空比 0 锁定覆盖；
- `test_motion_streaming_coordinates`：G0/G1 微米坐标与 TWIN-21 20B 报文对齐覆盖；
- `test_filament_runout_hms_3001`：HMS 0x3001 断料安全暂停/停进给/恢复走线覆盖；
- `test_m112_and_estop_interlock`：M112 急停熔断与自锁覆盖；
- `test_snapshot_export_and_progress`：128B 快照导出与进度千分比覆盖；
- `test_sync_pos_and_telemetry`：MC 0x16 报文反向同步覆盖。

---

## 3. 交付清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/contracts/twin/job/job_executor.h` | 执行器公开接口与 128B 状态结构体 | `963c91f54ca173e0d8c38fa2c205e3090d6755a2e7326decce782ddf549953ab` |
| `soc-ap/contracts/twin/job/job_executor.c` | 执行器流式走线、选项 A 加热锁与 HMS 联动实现 | `9fb9cdb455a93c90ccc2cbe7614cb267b5deb0ac93f7ff05217e7d9548996d9b` |
| `soc-ap/tests/job/test_job_executor.c` | 8 组针对性单元测试套件 | `0d21d4495e66c2571c7da798e12d3210369e3223c4267a6bc33204d899915e7e` |
