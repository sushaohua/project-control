---
task_id: TEMP-06
run_id: run_01
author_role: QA
author_session: 7f1cda3e-d24d-40ed-92d7-c40afe3a440c
timestamp: '2026-10-29T09:23:00+08:00'
task_revision: 1
status: completed
deliverables:
- path: project-control/docs/evidence/temperature_increment/TEMP-06/runs/run_01/raw_capture/mc_40_samples.json
  sha256: 1b2fc7e9fb2253b307f214cded9bb606651bdd5776943becf59805c693ae02e9
- path: project-control/docs/evidence/temperature_increment/TEMP-06/runs/run_01/raw_capture/th_40_samples.json
  sha256: 65aa675328830ffe60c52cc8ded66bc841bf1c1def4ddc200cbbd6df56e6fe0d
- path: project-control/docs/evidence/temperature_increment/TEMP-06/runs/run_01/raw_capture/fault_injection_test.json
  sha256: cd5dd4f8e64dcf67285bb7e54d7eb089a10c15b819b7d6172d3775f473a196f4
verification:
  commands:
  - id: hil_bench_mc
    cwd: .
    command: python3 project-control/docs/evidence/temperature_increment/TEMP-06/runs/run_01/run_hil_test.py
    exit_code: 0
    result: PASS
  - id: hil_bench_th
    cwd: .
    command: python3 project-control/docs/evidence/temperature_increment/TEMP-06/runs/run_01/run_hil_test.py
    exit_code: 0
    result: PASS
  - id: check_graph
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: python3 project-control/tools/check_task_graph.py
    exit_code: 0
    result: PASS
---

# TEMP-06 独立真实 HIL 验收复验与安全断线测试执行报告 (Run 01)

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **微任务卡** | `TEMP-06` (独立真实 HIL 验收复验与安全断线测试) |
| **所属计划** | `next_increment_design_pl02.md` (增量方案 A：双端温度遥测闭环) |
| **执行角色** | `QA` (独立测试与质量验收, 会话: `7f1cda3e-d24d-40ed-92d7-c40afe3a440c`) |
| **独立复核** | `ARCH` (独立架构复核, 会话: `212d83ba-56f8-4c1b-9b5a-46e87a340671`) |
| **硬件台架** | 双 ST-Link V2 探针 + CH340 物理串口 + 双 AT32 真实板卡 (零虚拟化在环) |
| **测试宿主** | VMware Ubuntu 22.04 LTS (`192.168.77.134`), `/dev/ttyUSB0` |
| **验收结论** | **APPROVED (40 轮双端压测 100% 成功，RTT 抖动严格达标，PWM 占空比恒为 0%，断线与自愈 100% 符合规范)** |

---

## 1. 受测固件与程序基线核验 (Baseline Audit)

测试直接基于 `TEMP-05` 产出的 RC3 候选清单（[`ap_mc_th_temperature_candidate.yaml`](../../../../docs/releases/ap_mc_th_temperature_candidate.yaml)）开展：

- **AP 宿主 CLI 程序 (`soc-ap`)**:
  - SHA-256: `5a1e31eb34ea6b2d36c6cac2abe6c10d0da37daeb5474ce8236a664f95d22776` (42,208 字节)
  - 运行环境: VMware Ubuntu (`/dev/ttyUSB0 @ 115200 8N1`)
- **MC 主控固件 (`fw_mc.bin`)**:
  - SHA-256: `16ea3c9fac94b8facc56ac394f5fc3a2f3ab644877224ded75fe112573352703` (370,036 字节)
  - 芯片: `AT32F435VGT7` (UID: `053023904C96C0000D819709`)
  - 基地址: `0x08020000` (Reset Vector: `0x08043399`)
- **TH 工具头固件 (`fw_th.bin`)**:
  - SHA-256: `d3a1be722c611b567a9a5cd565a9ef2f724bfefdfde8bb2a0bc7573d6113e011` (71,804 字节)
  - 校验锚点: `8098ff2d8ada5caa4992b1c05062be5b62ee73216a04377608622dc8ac219d21` (`0x0803F800`, 140 字节)
  - 芯片: `AT32F423CCT7` (UID: `053173C58023C000127C0707`)
  - 基地址: `0x08004000` (VTOR: `0x08004000`)

---

## 2. 40 轮硬件在环连续压测数据统计 (40-Round Stress Testing)

执行自动化脚本 [`run_hil_test.py`](run_hil_test.py) 进行独立采样与聚合：

### 2.1 MC 单跳热床遥测 (40 轮实测)
- **原始数据记录**: [`raw_capture/mc_40_samples.json`](raw_capture/mc_40_samples.json)
- **实测指标**:
  - 样本总数: 40 次
  - 成功次数: 40 次 (**成功率: 100.0%**)
  - 单跳往返时延（RTT）:
    - 最小值 (Min): `7,246 us` (7.25 ms)
    - 最大值 (Max): `16,093 us` (16.09 ms)
    - 平均值 (Avg): **`7,946.7 us`** (7.95 ms)
  - 热床读数稳定性: 40 轮均为 `24.50℃`（`current_temp_centi_c = 2450`, `raw_adc_value = 3200`, `sensor_status = 0 (OK)`）
  - **强电安全红线 (Hardware Safety Invariant)**:
    - `heater_duty_percent != 0` 违规次数: **0 次**（40 轮 100% 保持为 0%）

### 2.2 TH 双跳喷头遥测 (40 轮穿透实测)
- **原始数据记录**: [`raw_capture/th_40_samples.json`](raw_capture/th_40_samples.json)
- **实测指标**:
  - 样本总数: 40 次
  - 成功次数: 40 次 (**成功率: 100.0%**)
  - 全链路双跳穿透往返时延（RTT）:
    - 最小值 (Min): `8,102 us` (8.10 ms)
    - 最大值 (Max): `9,252 us` (9.25 ms)
    - 平均值 (Avg): **`8,434.9 us`** (8.43 ms)
    - **指标达成**: 40 轮全部处于 `8.10 ~ 9.25 ms` 范围内，**100% 严格满足 RTT ≤ 10ms 红线指标**。
  - 喷头读数真实度: 真实 ADC 采样，读数处于 `121.2℃ ~ 121.6℃`（由于前序联调上电余温逐步向室温冷却降温），无固定假死数据。
  - **强电安全红线 (Hardware Safety Invariant)**:
    - `heater_duty_percent != 0` 违规次数: **0 次**（40 轮 100% 保持为 0%）

---

## 3. 故障注入与安全断线测试 (Fault Injection & Recovery)

使用 [`probe_fault_injector.py`](../../../../test_harness/hil/tools/probe_fault_injector.py) 执行物理寄存器断开与恢复：
- **原始数据记录**: [`raw_capture/fault_injection_test.json`](raw_capture/fault_injection_test.json)

1. **基线正常阶段**:
   - 查询返回正常 (`status: SUCCESS`, RTT `8,562 us`, Temp `121.58℃`)；
2. **故障注入阶段 (切断 TH USART1)**:
   - 寄存器写入: `USART1_CTRL1 = 0x00000000`；
   - AP 发起查询 (`--timeout-ms 300`)：
     ```json
     {"status":"TIMEOUT","exit_code":1,"target":"TH","cmd":"GET_TEMP","error_msg":"Timeout waiting for response from target 0x03 after 300 ms","heater_duty_percent":0}
     ```
   - 判定: AP 精准触发熔断超时，退出码 1，绝不捏造任何脏数据；
3. **自愈恢复阶段 (使能 TH USART1)**:
   - 寄存器写入: `USART1_CTRL1 = 0x0000202C`；
   - AP 立即再次发起查询：
     ```json
     {"status":"SUCCESS","exit_code":0,"monotonic_rtt_us":8411,"target":"TH","temp_info":{"temperature_c":121.27,"sensor_status_str":"OK","heater_duty_percent":0}}
     ```
   - 判定: 瞬时自愈（RTT `8.41 ms`），自愈成功率 100%。

---

## 4. 传感器开路与短路状态码防御审计 (Fault Status Code Audit)

审查 `mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c` 中的故障判定逻辑：
- **开路断线**: ADC 采样值 $> 4075$（`ADC_OPEN_CIRCUIT_THRESHOLD`），状态置为 `MINIMC_TEMP_STATUS_OPEN_CIRCUIT (0x01)`，温度固定上报 `0x7FFF`（`MINIMC_TEMP_FAULT_VALUE_CENTI_C`）；
- **短路故障**: ADC 采样值 $< 20$（`ADC_SHORT_CIRCUIT_THRESHOLD`），状态置为 `MINIMC_TEMP_STATUS_SHORT_CIRCUIT (0x02)`，温度固定上报 `0x7FFF`；
- **采样超时**: ADC 硬件采样轮询超时（`ADC_POLL_TIMEOUT_CYCLES = 10000U` 耗尽），状态置为 `MINIMC_TEMP_STATUS_TIMEOUT (0x03)`，温度固定上报 `0x7FFF`；
- **AP 防御闭环**: AP 收到 `0x7FFF` 自动格式化为 `"FAULT"`，JSON 字段携带强类型错误码，且当检测到 `heater_duty_percent > 0` 时触发 `EXIT_CODE_SAFETY_FAULT (3)` 熔断。

---

## 5. 验收结论

1. 硬件台架零虚拟化、零 PTY，探针指纹与基地址核对 100% 严丝合缝；
2. 40 轮 MC 热床与 40 轮 TH 喷头温度在环遥测压测成功率 100%；
3. 双跳穿透时延平均 `8.43 ms`，100% 满足 $\le 10\text{ ms}$ 指标要求；
4. 加热占空比实测 100% 恒为 0%，无任何加热输出与飞温安全隐患；
5. 硬件断线故障注入与自愈测试 100% 达标。

**HIL 验收结论：APPROVED (通过)**。
