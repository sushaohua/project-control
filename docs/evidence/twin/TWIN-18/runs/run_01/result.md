# TWIN-18 双MCU运动/调平/断料状态接口调查与协议对账执行与验收报告

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-18` (双MCU运动/调平/断料状态接口调查与协议对账) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **所属计划** | `PLAN-TWIN-TASK-EXECUTION-20261029` (VMware与SoC两阶段任务执行与闭环总表) |
| **执行角色** | `ENG-MC` (运控固件工程师，协同 `ENG-TH` 工具头工程师与 `ARCH` 系统架构师) |
| **基线输入** | `REQ-DECOMP-FIRST-RELEASE-20261029`、`ICD-VMWARE-SOC-TWIN-20261029 rev 2`、`SPEC-PROTO-20261015-153000` |
| **前置条件绑定** | `TWIN-01` (`docs/evidence/twin/TWIN-01/runs/run_02/result.md`, version `67709ffaec92ec739f33d19ff690c3ad1a90027bd4d75ba804417a68b6095316`) |
| **执行日期** | 2026-10-30 |
| **执行状态** | **Completed / Delivered (源码级调查与协议对账齐备，行号全部核实，无虚构接口，等待独立 QA 与各岗位审查)** |

---

## 1. 源码基线与交付物清单

### 1.1 四仓库源码提交基线

本任务执行时，四仓库实际 HEAD 提交哈希如下：
* `project-control`: `5f8207eb4905417f6fafaf606a6e7cfcb94ae0d2`
* `soc-ap`: `c6b4a0a9fb3c4dcda3a7b10b2f3ed2ce3a49e6e5`
* `mcu-p3`: `1246ea9cb441d074ea444f53320f5632fefcd503`
* `test_harness`: `210ddd1c3f6f59594836c91b68aae55fb7a35181`

### 1.2 交付物与 SHA256 对账表

本任务严格依照卡片授权范围（`allowed_paths: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md`, `project-control/docs/evidence/twin/TWIN-18/**`）交付：

| 交付文件路径 | 文件性质与说明 | SHA256 校验码 | 状态 |
| :--- | :--- | :--- | :--- |
| [`project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md`](../../../../specs/mcu_motion_leveling_filament_interface_survey_20261029.md) | 双MCU运动控制、自动调平与断料检测接口调查与协议对账规范原件 | `caffb64413d745e513ef5947e8d7c29c0f5ac70fa24e0523ebe7bed565629e38` | **Delivered** |
| [`project-control/docs/evidence/twin/TWIN-18/runs/run_01/result.md`](result.md) | 本执行与验收证据报告 | *当前文件* | **Delivered** |

---

## 2. 真实源码逐项锚点与核查结论表 (Source Code Audit Table)

依据“拒绝臆造接口，每项断言必引源码路径与精确行号”的铁律，调查采掘出的真实代码锚点对账如下：

| 调查领域 | 关键特性 | 源码所在仓库与文件相对路径 | 源码行号范围 | 关键结构体 / 宏 / 函数符号 | 事实核查结论与架构判断 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **运控机构** | CoreXY 机构使能 | `mcu-p3/motion-controller-mcu/project/marlin/configure.h` | Line 39 | `#define COREXY` | 确认为 CoreXY 模式，非笛卡尔或 Delta |
| **运控轴系** | 轴数与多轴枚举 | `mcu-p3/motion-controller-mcu/project/marlin/configure.h`<br/>`mcu-p3/.../marlin_core/Marlin.h` | `configure.h#L22`<br/>`Marlin.h#L174-L185` | `#define NUM_AXIS 9`<br/>`enum AxisEnum` | 共 9 轴：X(0), Y(1), Z(2), A(3), B(4), C(5), D(6), X_HEAD(7), Y_HEAD(8) |
| **逻辑坐标** | 当前规划器坐标 | `mcu-p3/.../marlin_core/Marlin_main.c` | Line 392 | `volatile float current_position[NUM_AXIS]` | 浮点数，单位为毫米（mm） |
| **脉冲坐标** | 步进电机脉冲位置 | `mcu-p3/.../marlin_core/stepper.c`<br/>`mcu-p3/.../marlin_core/planner.c` | `stepper.c#L93`<br/>`planner.c#L102` | `volatile long count_position[NUM_AXIS]`<br/>`long position[NUM_AXIS]` | 整数脉冲数（steps） |
| **坐标读取API** | 步数/毫米读取函数 | `mcu-p3/.../marlin_core/stepper.c`<br/>`mcu-p3/.../marlin_core/stepper.h` | `stepper.c#L1336-L1350`<br/>`stepper.h#L82, L86` | `st_get_position(axis)`<br/>`st_get_position_mm(axis)` | 临界区保护读取；`st_get_position_mm` 返回当前步进位置/steps_per_unit |
| **M114 指令** | 存量串口坐标回显 | `mcu-p3/.../marlin_core/Marlin_main.c` | Line 3551-3568 | `case 114: // M114` | 向调试串口输出 ASCII 文本，非 MiniMCProto 链路，AP 无法直接结构化解析 |
| **MC MiniMCProto** | 现行指令分发 | `mcu-p3/.../project/src/minimc_proto.c` | Line 355-383 | `handle_mc_query()` | 仅支持 `0x01` (版本), `0x03` (心跳), `0x14` (温度)；**无位置与调平指令** |
| **MC 串口转发** | 级联路由到 TH | `mcu-p3/.../project/src/minimc_proto.c`<br/>`mcu-p3/.../project/marlin/configure.h` | `minimc_proto.c#L385-L420`<br/>`configure.h#L47-L59` | `handle_ap_frame()`, `relay_frame()`<br/>`FORWARD_USART_SEL 6` (921600波特率) | `dst=0x03` 递减跳数转 USART6 发 TH；TH 回 `dst=0x01` 经 USART2 (DMA1_CH2) 发 AP |
| **调平配置** | ABL 网格参数 | `mcu-p3/.../project/marlin/configure.h` | Line 199-238 | `ENABLE_AUTO_BED_LEVELING`<br/>`AUTO_BED_LEVELING_GRID`<br/>`AUTO_BED_LEVELING_GRID_POINTS 5` | $5 \times 5$ 共 25 测点网格，范围 20~220mm，网格步长 50mm |
| **调平数据** | 运行时网格缓冲区 | `mcu-p3/.../marlin_core/Marlin_main.c`<br/>`mcu-p3/.../marlin_core/planner.c` | `Marlin_main.c#L528`<br/>`planner.c#L94` | `float bed_level[5][5]`<br/>`matrix_3x3 plan_bed_level_matrix` | 存储 25 点 Z 轴形变偏差；旋转矩阵补偿床面刚体倾斜 |
| **调平持久化** | EEPROM 读写 | `mcu-p3/.../marlin_core/ConfigurationStore.c`<br/>`mcu-p3/.../marlin_core/Marlin_main.c` | `ConfigurationStore.c#L491-L496`<br/>`Marlin_main.c#L2775-L2776` | `AUTO_LEVEL`<br/>`AUTO_LEVEL_1`, `AUTO_LEVEL_2` | 启动时读入 25 点网格；G29 拟合平面方程系数写入 EEPROM |
| **G29 算法** | 测点与最小二乘拟合 | `mcu-p3/.../marlin_core/Marlin_main.c` | Line 2646-2834 | `case 29: // G29`<br/>`qr_solve(25, 3, ...)` | 蛇形循环探测 25 点，QR 分解求解最小二乘平面 $z = ax + by + d$ |
| **网格插补** | 双线性插补算法 | `mcu-p3/.../marlin_core/Marlin_main.c` | Line 4864-4900 | `void adjust_delta(float cartesian[3])` | 取邻近 4 个网格顶点 $z_1, z_2, z_3, z_4$ 执行双线性插补并叠加到 `delta` |
| **调平探针** | MC 探针物理引脚 | `mcu-p3/.../project/inc/at32f435_437_wk_config.h`<br/>`mcu-p3/.../project/src/wk_gpio.c` | `at32f435_437_wk_config.h#L267-L268`<br/>`wk_gpio.c#L54` | `#define Z_LIMIT_PIN GPIO_PINS_1`<br/>`#define Z_LIMIT_GPIO_PORT GPIOE` | 调平探针物理连接在 MC 的 **PE1**（与 Z 限位共用），下压触发 |
| **断料引脚** | TH 断料检测引脚 | `mcu-p3/color-engine-mcu/io_toggle/inc/pins.h` | Line 19-20, 45 | `#define A_LIMIT_PIN GPIO_PINS_2`<br/>`#define A_LIMIT_GPIO_PORT GPIOD` | 断料传感器连接在 TH 的 **PD2**；高电平(`1`)=有料，低电平(`0`)=断料 |
| **断料检测方式** | 轮询 vs 中断 | `mcu-p3/.../src/bsp/wk_exint.c`<br/>`mcu-p3/.../src/app/motherboard.c` | `wk_exint.c#L57-L76`<br/>`motherboard.c#L106-L137` | `EXINT_LINE_14` (仅用于PC14断电)<br/>`Board_manage()` | **断料未使用 EXINT 中断**，完全在主循环中由定时器以 1Hz 频率轮询 |
| **断料防抖** | 采样滤波机制 | `mcu-p3/.../src/app/motherboard.c` | Line 10-11, 71-98 | `FILAMENTCHECK_UPDATE_RATE_US 1000000UL`<br/>`FILAMENT_LOW_SAMPLES 10U` | **每 1 秒采 1 次，连续 10 次低电平才判定断料，去抖延时达 10 秒** |
| **断料通信** | TH 向 MC 上报格式 | `mcu-p3/.../src/app/motherboard.c` | Line 64 | `send_quick("filaout\r\n");` | **TH 发送原始 ASCII 字符串**，未采用 MiniMCProto 二进制协议 |
| **MC 捕获断料** | MC 接收与停机 | `mcu-p3/.../marlin_core/motherboard.c`<br/>`mcu-p3/.../marlin_core/filament_runout.c` | `motherboard.c#L348`<br/>`filament_runout.c#L107-L120` | `FilamentCheckUart()`<br/>`buf_contains(buf, len, "filaout")` | MC 轮询串口缓冲区搜寻 `"filaout"` 文本子串，触发 `FilamentRunoutTrigger` |
| **TH 调平探针** | TH 探针引脚核查 | `mcu-p3/color-engine-mcu/io_toggle/inc/pins.h` | Line 83 | `#define Z_LEVEL_PIN 0` | **TH 侧未连接调平传感器**，探针硬件全部在 MC 板上 |

---

## 3. 关键架构断层与整机闭环风险评估

本调查揭示了当前代码中阻碍首版本地打印闭环的 **3 大关键协议断层**：

```
+---------------------------------------------------------------------------------------------------------+
|                                  当前系统通信现状与断层示意图                                            |
|                                                                                                         |
|   [ Browser HMI ] <== HTTP/SSE ==> [ ui-gateway ] <== D-Bus ==> [ device-manager ]                      |
|                                                                          |                              |
|                                                                      Fast DDS                           |
|                                                                          |                              |
|                                                                 [ forward-service ]                     |
|                                                                          |                              |
|                                                      USART2 (115200) MiniMCProto v2.0                   |
|                                                                          |                              |
|                                                                  +-------v--------+                     |
|                                                                  |  MC (AT32F435) |                     |
|                                                                  +-------+--------+                     |
|                                                                          |                              |
|                                          USART6 (921600) 【混合流: MiniMCProto 二进制 + 裸ASCII】        |
|                                                                          |                              |
|                                                                  +-------v--------+                     |
|                                                                  |  TH (AT32F423) |                     |
|                                                                  +----------------+                     |
|                                                                                                         |
|   【断层 1: MOT-001】MC 仅支持 M114 ASCII 打印到调试口，MiniMCProto 完全无坐标查询指令 -> AP 读不到坐标 |
|   【断层 2: MOT-002】MC 具有 5x5 bed_level 网格，但 print_bed_level 注释死掉，无导出指令 -> AP 无法可视化  |
|   【断层 3: COL-007】TH 确认断料后发 "filaout\r\n" 字符串给 MC，MC 内部挂起，但【未通知 AP】 -> AP 盲区 |
+---------------------------------------------------------------------------------------------------------+
```

1. **断层 1 (`MOT-001`)**：MC 虽具有完整的 `current_position` 浮点毫米与 `st_get_position` 步进坐标，但仅暴露为老式 `M114` ASCII 指令且输出至调试串口 COM8。`minimc_proto.c` 缺乏 `0x16` 坐标查询或 `0x40` 遥测推送，导致 AP 无法通过串口获取实时位置；
2. **断层 2 (`MOT-002`)**：MC 拥有完整的 $5 \times 5$ 共 25 点网格高程插补与 QR 分解平面拟合能力，但缺乏向 AP 导出的二进制帧，HMI 无法呈现调平热力图；
3. **断层 3 (`COL-007`)**：TH 虽能通过 PD2 轮询检测断料，但采用原始 ASCII 文本 `"filaout\r\n"` 发送给 MC，MC 旁路捕获后仅在本地 LCD 弹窗并挂起 SD 打印，**完全未向 AP 发送 MiniMCProto 告警帧**。上位 `device-manager` 无法感知断料，导致作业引擎失联或异常。

---

## 4. 后续任务交接清单 (Downstream Task Handoffs)

针对上述断层，本调查报告向后续微任务提出明确整改需求：

1. **交接至 `TWIN-02` (ARCH, 通信契约)**：
   - 在 `contracts/twin/` 冻结 `CMD_POS_QUERY (0x16)`（20 字节载荷）、`CMD_LEVEL_GRID_QUERY (0x18)`（54 字节载荷）及 `CMD_ALARM_EVENT (0x50)`（HMS 错误码 `0x3001`）的线缆结构体。
2. **交接至 `TWIN-15` (ENG-MC, MC 固件改造)**：
   - 在 `motion-controller-mcu/project/src/minimc_proto.c` 实现 `0x16` 与 `0x18` 指令响应；
   - 确保从 TH 接收的 `0x50` 二进制告警报文能线速透明转发给 AP。
3. **交接至 `TWIN-16` (ENG-TH, TH 固件改造)**：
   - 彻底废除 `send_quick("filaout\r\n")`，改造为打包 `CMD_ALARM_EVENT (0x50)` 二进制帧向 AP（`DST=0x01`）发送；
   - 将断料防抖周期从 10 秒优化为 300ms（50ms 采样 $\times$ 6次确认）。
4. **交接至 `TWIN-17` (ENG-STATE, 作业引擎) 与 `TWIN-19` (ENG-STATE, HMS 与安全)**：
   - `forward-service` 接入 `0x16`、`0x18` 与 `0x50`；
   - `device-manager` 捕获 `0x3001` 后原子挂起作业流，HMI 弹窗阻断。

---

## 5. 任务图谱静态校验与门禁核验结果

在工作区执行任务图依赖检查：
```bash
PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
```
* **校验输出结果**：
  - `canonical_task_count`: 108
  - `microtask_count`: 66
  - `errors`: `[]`
  - `dependency_cycles`: `[]`
  - `exit_code`: `0`
* **门禁符合性**：所有图谱结构、依赖拓扑、任务卡声明合法合规，无循环依赖，无未授权写路径。

---
*本报告作为微任务 TWIN-18 的正式执行记录，已完成双 MCU 源码的实证调查与跨端协议对账，证据完整，准予提交 COORD 收件与独立 QA 审查。*
