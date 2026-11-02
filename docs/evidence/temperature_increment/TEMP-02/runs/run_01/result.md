---
task_id: TEMP-02
run_id: run_01
author_role: ENG-TH
author_session: th-session-20261028
timestamp: '2026-10-28T20:34:00+08:00'
task_revision: 1
status: completed
deliverables:
- path: mcu-p3/color-engine-mcu/io_toggle/inc/thermistor_adc.h
  sha256: 263074c78c8cef12cdaaf5198a167458562976606da3a96953367b170ced4e8d
- path: mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c
  sha256: 434a51b794a0570886bb01c5e6ceca323d5496b6f14dcd79c394051c6144afda
- path: mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c
  sha256: 9fa1d91e26d869ba113fc755f1ab882fe19fdca53e12caa98720d4bf8a02428a
- path: mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
  sha256: 16e145e19649e1294e68f15da449405da744680cd1fcc4929d4aa5763a5e446c
verification:
  commands:
  - id: th_clean_pack
    cwd: /home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle
    command: make clean && make pack
    exit_code: 0
    result: PASS
  - id: check_graph
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    exit_code: 0
    result: PASS
---

# TEMP-02 执行交付结果报告：TH 喷头温度驱动重构与应答实现

## 1. 交付目标与核心实现

根据 `PL-02` 增量规划与 `ICD-MINIMC-TEMP-20261028` 契约，ENG-TH 已完成 Toolhead (TH) 固件中温度驱动与 MiniMCProto v2.0 协议应答的重构开发：

### 1.1 ADC 驱动死等消除与超时保护 (`thermistor_adc.c` / `thermistor_adc.h`)
- **死等彻底消除**：重构原有存量代码中裸 `while(!FLAG);` 无界轮询，全部展开并绑定递减超时保护计数器 `ADC_POLL_TIMEOUT_CYCLES = 10000U`；
- **异常故障判定与状态码**：
  - 开路断线：当 12-bit ADC 读数 $> 4075$ 时，置位 `MINIMC_TEMP_STATUS_OPEN_CIRCUIT (0x01)`，上报故障温度 `0x7FFF`，`raw_adc_value = 4095`；
  - 短路故障：当 12-bit ADC 读数 $< 20$ 时，置位 `MINIMC_TEMP_STATUS_SHORT_CIRCUIT (0x02)`，上报故障温度 `0x7FFF`，`raw_adc_value = 0`；
  - 采样超时：当 ADC 轮询超时退出时，置位 `MINIMC_TEMP_STATUS_TIMEOUT (0x03)`，上报故障温度 `0x7FFF`，`raw_adc_value = 0`；
- **NTC 100K B3950 线性查表与插值**：
  - 基于 26 级校准点表，覆盖 $-25^\circ\text{C} \sim +320^\circ\text{C}$，全整数分段线性插值计算出 $0.01^\circ\text{C}$ 精度温度（如 $25.00^\circ\text{C}$ 编码为 `2500`）；
- **强电安全硬性锁死 (Hardware Safety Invariant)**：
  - 采样与初始化入口强制重置 `target_temperature[0] = 0`、`soft_pwm[0] = 0`，并强制调用 `tmr_channel_value_set(TMR3, TMR_SELECT_CHANNEL_2, 0U)` 确保加热输出绝对为 0；
  - 载荷中 `heater_duty_percent` 强制置 `0%`，`target_temp_centi_c` 强制置 `0`，PID 温控旁路禁用。

### 1.2 MiniMCProto 0x14 温度查询与响应 (`minimc_proto.c`)
- **操作码解包与寻址**：
  - 识别 `MINIMC_CMD_GET_TEMP (0x14)`，当 `dst_id == 0x03` (`MINIMC_NODE_TH`) 且无 `MINIMC_FLAG_IS_RESPONSE` 时触发温度遥测采样；
- **固定 16 字节载荷构造**：
  - 构造 `minimc_temp_report_payload_t` 载荷，严格满足 16 字节紧凑单字节对齐（通过 `_Static_assert` 编译期校验）；
  - 填充单调毫秒时间戳 `sample_timestamp_ms`（来自 `get_tick_count()`）；
- **响应帧汇聚与回送**：
  - 发送至 AP（`dst_id = 0x01`），`flags = MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2 (0x06)`；
  - 回显原请求 `seq`，`hop_limit = 0x04`，`payload_len = 0x0010`，并追加标准 CRC-16/CCITT 校验和（全帧共 30 字节），经 USART1 中继给 MC。

---

## 2. 编码规范门禁核验 (`c_cpp_coding_standard.md`)

| 核查项目 | 规范要求 | 本任务实现核验 | 状态 |
| :--- | :--- | :--- | :---: |
| **自研函数规模** | 严禁编写超 50 行函数 | `thermistor_adc.c` 中 9 个函数最大 40 行；`minimc_proto.c` 中新增/修改函数最大 45 行 | **PASS** |
| **自研入参限制** | 严禁编写超 4 入参函数 | 全部新增函数入参 $\le 3$ 个（`build_temp_resp` 3 个，其余 $\le 2$ 个） | **PASS** |
| **内存安全性** | 零动态堆分配，无指针黑魔法 | 无 malloc/free/new/delete，指针显式下标访问，编译期静态断言 | **PASS** |
| **防御性校验** | 入口首行非空空指针校验 | 所有接收指针的公共与静态辅助函数首行均包含 Guard Clause | **PASS** |
| **硬件死等消除** | 禁止无防护轮询，强制超时保护 | 所有硬件标志等待均显式展开大括号并带递减计数器退出 | **PASS** |
| **强电安全锁死** | 加热输出占空比硬锁死 0% | 固件生命周期内 `heater_duty_percent = 0`，PWM 输出通道强制复位为 0 | **PASS** |

---

## 3. 构建与验证结果

1. **固件编译与打包**：
   - 在 `mcu-p3/color-engine-mcu/io_toggle` 执行 `make clean && make pack`：
     - `src/app/thermistor_adc.c`：编译零警告、零错误；
     - `src/app/minimc_proto.c`：编译零警告、零错误；
     - 成功产出最终打包固件：`build/fw_th.bin`（71,804 字节，含 128B Trailer 与 140B Anchor，SHA256: `16e145e19649e1294e68f15da449405da744680cd1fcc4929d4aa5763a5e446c`）；
2. **任务图静态门禁**：
   - 执行 `check_task_graph.py --workspace .`：返回 Exit Code 0，无结构性循环与依赖错误。
