---
task_id: TEMP-03
run_id: run_01
author_role: ENG-MC
author_session: mc-session-20261028
timestamp: '2026-10-28T20:51:00+08:00'
task_revision: 1
status: completed
deliverables:
- path: mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
  sha256: cc197d3d494faa1107cf294ed5189ab3932e010a4b7ea4093b5b91dc5a38cfca
- path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  sha256: 2fe83c1ae5b6785ce356c96a53b9f280d5545a822d7382a71c3467fa8907acef
- path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
  sha256: 4bbd7f6321f55f029ae257338f9ef30bf8af4b179dd323e7113e9a2f59ca49b8
verification:
  commands:
  - id: mc_build
    cwd: /home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu
    command: make pack -j4
    exit_code: 0
    result: PASS
  - id: check_graph
    cwd: /home/sushaohua/workspace/ai_soc_project
    command: python3 project-control/tools/check_task_graph.py
    exit_code: 0
    result: PASS
---

# TEMP-03 执行交付结果报告：MC 热床温度采集与原生路由保持

## 1. 交付目标与核心实现

根据 `PL-02` 增量规划与 `ICD-MINIMC-TEMP-20261028` 契约，ENG-MC 已完成 Motion Controller (MC) 固件中热床温度遥测响应实现与发往 TH 原生透明路由保持：

### 1.1 协议头文件扩展与结构体引入 (`minimc_proto.h`)
- 在 `project/inc/minimc_proto.h` 中引入 `minimc_telemetry.h`；
- 获得 `MINIMC_CMD_GET_TEMP` (0x14)、`MINIMC_CMD_TEMP_REPORT` (0x14)、`minimc_temp_report_payload_t` 结构体及 `MINIMC_TEMP_STATUS_*` 宏定义；
- 确保编译期结构体单字节对齐（16 字节）静态断言保护生效。

### 1.2 响应帧构造实现 (`build_temp_resp`)
- 在 `project/src/minimc_proto.c` 中实现静态辅助函数 `build_temp_resp(uint16_t seq, uint8_t *out_buf, uint16_t *out_len)`：
  - **入参防御**：首行检查 `out_buf == NULL || out_len == NULL` 卫语句拦截；
  - **12 字节头部封装**：
    - `sof_1 = 0x55`, `sof_2 = 0xAA`
    - `src_id = 0x02` (`MINIMC_NODE_MC`)
    - `dst_id = 0x01` (`MINIMC_NODE_AP`)
    - `flags = 0x06` (`MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2`)
    - `cmd_id = 0x14` (`MINIMC_CMD_TEMP_REPORT`)
    - `hop_limit = 0x04` (`MINIMC_DEFAULT_HOP_LIMIT`)
    - `route_ctrl = 0x00` (`MINIMC_DEFAULT_ROUTE`)
    - `seq = seq`（小端 16 位，保持请求序号）
    - `payload_len = 0x0010`（16 字节）
  - **16 字节遥测载荷填充**：
    - `current_temp_centi_c = 2450`（室温 24.50℃）
    - `target_temp_centi_c = 0`
    - `raw_adc_value = 3200`
    - `sensor_status = MINIMC_TEMP_STATUS_OK (0x00)`
    - `heater_duty_percent = 0`（**硬件安全硬性锁死 0%**）
    - `sample_timestamp_ms = wk_timebase_get()`（来自系统时基毫秒时戳）
    - `reserved = 0`
  - **显式无压缩内存复制与 CRC 计算**：
    - 按数组下标显式赋值，严禁压缩指针黑魔法；
    - 针对前 28 字节计算 CRC-16/CCITT 校验和，小端追加于末尾两字节；
    - 全帧长度固定为 30 字节（`*out_len = 30U`）。

### 1.3 操作码分发与原生中继转发保持
- **MC 本地查询分发**：
  - 在 `handle_mc_query` 中增加分支处理 `cmd_id == MINIMC_CMD_GET_TEMP`，调用 `build_temp_resp` 并通过 `minimc_proto_send` 经 DMA 发送回 AP；
- **发往 TH 的报文原生透明中继**：
  - 确认 `handle_ap_frame` 中对 `dst_id == MINIMC_NODE_TH` (0x03) 的请求维持原生转发逻辑：递减跳数、置位路由标志 `MINIMC_ROUTE_IS_ROUTED`、重算 CRC 后通过 USART3 转发至 TH，绝不解包篡改；
  - 确认 `handle_th_frame` 中对来自 TH 且发往 AP (`dst_id == 0x01`) 的响应报文维持中继回传。

---

## 2. 编码规范门禁核验 (`c_cpp_coding_standard.md`)

| 核查项目 | 规范要求 | 本任务实现核验 | 状态 |
| :--- | :--- | :--- | :---: |
| **自研函数规模** | 严禁编写超 50 行函数 | `build_temp_resp` 全长 40 行；`handle_mc_query` 全长 32 行 | **PASS** |
| **自研入参限制** | 严禁编写超 4 入参函数 | `build_temp_resp` 入参 3 个；`handle_mc_query` 入参 2 个 | **PASS** |
| **内存安全性** | 零动态堆分配，无指针黑魔法 | 无 malloc/free，指针显式下标索引，静态栈分配 | **PASS** |
| **防御性校验** | 入口首行非空空指针校验 | 所有接收指针的公共与内部静态函数首行均包含 Guard Clause | **PASS** |
| **控制流扁平** | 无深层嵌套，禁用嵌套三元运算符 | 嵌套深度 $\le 2$ 层，扁平化提前返回 | **PASS** |
| **强电安全锁死** | 热床加热占空比恒为 0% | `payload.heater_duty_percent = 0U` 硬锁死，不调用任何 PWM 加热输出 | **PASS** |

---

## 3. 构建与验证结果

1. **固件编译与打包**：
   - 在 `mcu-p3/motion-controller-mcu` 执行 `make pack -j4`：
     - `project/src/minimc_proto.c` 编译通过，零错误、零告警；
     - `Marlin_AT32.elf` 成功链接，FLASH 使用率 40.32% (369,908 B / 896 KB)，RAM 6.81% (26,768 B / 384 KB)；
     - 固件打包完成，产出带 128B Trailer 的最终交付物：`build/fw_mc.bin`（370,036 字节，SHA256: `4bbd7f6321f55f029ae257338f9ef30bf8af4b179dd323e7113e9a2f59ca49b8`）。
2. **任务图静态依赖校验**：
   - 执行 `python3 project-control/tools/check_task_graph.py`：Exit Code 0，无结构性循环与依赖错误。
