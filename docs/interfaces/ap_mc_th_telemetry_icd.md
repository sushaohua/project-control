# MiniMCProto v2.0 双端温度遥测接口控制文件 (ICD)

- **协议名称**：MiniMCProto v2.0 Telemetry Extension
- **版本号**：v2.0.4-telemetry
- **文档编号**：ICD-MINIMC-TEMP-20261028
- **责任角色**：ARCH
- **基线规范**：[`ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md`](../specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)
- **代码规范基线**：[`c_cpp_coding_standard.md`](../../.agents/rules/c_cpp_coding_standard.md)

---

## 1. 概述与设计原则

本规范定义了 SoC AP、MC（运动控制器）与 TH（工具头控制器）之间进行温度遥测查询与响应的物理帧格式、载荷结构与状态码规范。

### 1.1 核心设计约束
1. **操作码安全避让**：MiniMCProto v2.0 主规范已分配 `0x10` 为 `CMD_SYSTEM_CONTROL`，本增量正式分配并冻结操作码：
   $$\text{MINIMC\_CMD\_GET\_TEMP} = 0\text{x}14$$
   $$\text{MINIMC\_CMD\_TEMP\_REPORT} = 0\text{x}14$$（携带 `MINIMC_FLAG_IS_RESPONSE` 标志）。
2. **分层寻址原则**：严禁创建冗余操作码（如禁止定义 `CMD_GET_TEMP_MC` 与 `CMD_GET_TEMP_TH`）。所有端统一使用操作码 `0x14`，通过 MiniMC 帧头的目标节点 ID（`dst_id`）实现寻址：
   - `dst_id = 0x02`（`MINIMC_NODE_MC`）：查询热床温度；
   - `dst_id = 0x03`（`MINIMC_NODE_TH`）：查询喷头温度。
3. **强电安全硬性锁死原则 (Hardware Safety Invariant)**：
   - 本增量为**纯遥测只读增量**；
   - 固件生命周期内，加热输出 PWM 占空比硬锁死为 `0%`（`heater_duty_percent = 0`）；
   - Marlin 与 TH 内部 PID 温控循环完全旁路或禁用，严禁向加热棒或热床输出驱动功率。
4. **确定性内存与对齐**：
   - 载荷结构体采用显式单字节对齐 `#pragma pack(push, 1)`；
   - 严格禁止隐式编译器填充字节；
   - 必须在 C/C++ 编译期通过 `_Static_assert` / `static_assert` 校验载荷尺寸恒等于 16 字节。

---

## 2. 帧格式与交互时序

MiniMCProto v2.0 基础物理帧格式如下（全长 $12 + \text{len} + 2$ 字节）：
```
+---------+---------+--------+--------+-------+--------+-----------+------------+----------+--------------+------------------+----------+
| SOF1    | SOF2    | SRC_ID | DST_ID | FLAGS | CMD_ID | HOP_LIMIT | ROUTE_CTRL | SEQ (16) | PL_LEN (16)  | PAYLOAD (PL_LEN) | CRC (16) |
| (0x55)  | (0xAA)  | (1B)   | (1B)   | (1B)  | (1B)   | (1B)      | (1B)       | (小端)   | (小端)       | (可变)           | (CRC-16) |
+---------+---------+--------+--------+-------+--------+-----------+------------+----------+--------------+------------------+----------+
```

### 2.1 查询请求帧 (Query Frame)

| 字段 | 期望取值 | 说明 |
| :--- | :--- | :--- |
| `sof_1` / `sof_2` | `0x55`, `0xAA` | 帧起始引导符 |
| `src_id` | `0x01` (`MINIMC_NODE_AP`) | 发送端节点 ID (AP) |
| `dst_id` | `0x02` 或 `0x03` | 目标节点 ID (MC 或 TH) |
| `flags` | `0x01` (`MINIMC_FLAG_WANTS_ACK`) | 要求对方确认应答 |
| `cmd_id` | `0x14` (`MINIMC_CMD_GET_TEMP`) | 温度遥测操作码 |
| `hop_limit` | `0x04` | 默认中继跳数限制 |
| `route_ctrl` | `0x00` | 初始路由控制字 |
| `seq` | 自增序号（16位） | 请求序列号 |
| `payload_len` | `0x0000` (0 字节) | 请求帧无载荷 |
| `crc` | CRC-16/CCITT | 覆盖头部 12 字节的校验和 |

### 2.2 响应应答帧 (Response Frame)

| 字段 | 期望取值 | 说明 |
| :--- | :--- | :--- |
| `sof_1` / `sof_2` | `0x55`, `0xAA` | 帧起始引导符 |
| `src_id` | `0x02` 或 `0x03` | 响应端节点 ID (MC 或 TH) |
| `dst_id` | `0x01` (`MINIMC_NODE_AP`) | 目标节点 ID (AP) |
| `flags` | `0x02` (`MINIMC_FLAG_IS_RESPONSE`) | 响应帧标志 |
| `cmd_id` | `0x14` (`MINIMC_CMD_TEMP_REPORT`) | 温度遥测操作码 |
| `hop_limit` | `hop_limit - 1` | 经 MC 中继时递减 |
| `route_ctrl` | `0x04` (`MINIMC_ROUTE_IS_ROUTED`) | 经 MC 中继时置位路由标志 |
| `seq` | 匹配请求序号 | 保持与请求帧一致的序列号 |
| `payload_len` | `0x0010` (16 字节) | 载荷长度固定为 16 字节 |
| `payload` | 见第 3 节定义 | 16 字节结构体数据 |
| `crc` | CRC-16/CCITT | 覆盖头部 12 字节与 16 字节载荷的校验和 |

---

## 3. 遥测载荷数据结构 (`minimc_temp_report_payload_t`)

```c
#pragma pack(push, 1)
typedef struct {
    int16_t  current_temp_centi_c; /* 当前温度 (0.01℃)，范围 -4000 ~ +35000；故障时置 0x7FFF */
    int16_t  target_temp_centi_c;  /* 目标设定温度 (0.01℃)，只读模式固定填 0 */
    uint16_t raw_adc_value;        /* 原始 ADC 采样值 (0-4095)，故障时置 4095 或 0 */
    uint8_t  sensor_status;        /* 传感器运行状态码 (见 3.2 节) */
    uint8_t  heater_duty_percent;  /* 加热输出占空比 (0-100)，本增量必须恒等于 0 */
    uint32_t sample_timestamp_ms;  /* 采样单调时间戳 (ms)，来自 MCU systick */
    uint32_t reserved;             /* 保留字段，固定填 0 */
} minimc_temp_report_payload_t;
#pragma pack(pop)
```

### 3.1 字段语义详表

| 偏移 | 字段名 | 类型 | 字节数 | 取值范围 / 单位 | 语义说明 |
| :---: | :--- | :--- | :---: | :--- | :--- |
| `0x00` | `current_temp_centi_c` | `int16_t` | 2 | $-4000 \sim +35000$ ($0.01^\circ\text{C}$)<br>异常值：`0x7FFF` | 摄氏度乘以 100。例如 $25.30^\circ\text{C}$ 编码为 `2530` ($0\text{x}09E2$)；传感器异常时置为 `0x7FFF`。 |
| `0x02` | `target_temp_centi_c` | `int16_t` | 2 | $0$ ($0.01^\circ\text{C}$) | 只读增量固定填 `0`。 |
| `0x04` | `raw_adc_value` | `uint16_t` | 2 | $0 \sim 4095$ | 12 位 ADC 原始转换值，供遥测端排查阻值漂移与噪声。 |
| `0x06` | `sensor_status` | `uint8_t` | 1 | 枚举值 `0x00 ~ 0x03` | 传感器硬件健康度状态码。 |
| `0x07` | `heater_duty_percent`| `uint8_t` | 1 | **强制恒为 `0`** | 加热器输出占空比百分比。若非 0 即判定为安全故障。 |
| `0x08` | `sample_timestamp_ms`| `uint32_t` | 4 | $0 \sim 2^{32}-1$ (ms) | 单片机端采样瞬间的单调毫秒时间戳。 |
| `0x0C` | `reserved` | `uint32_t` | 4 | **固定为 `0`** | 32 位字节对齐与远期扩展保留。 |
| **总计**| - | - | **16** | - | **精确等于 16 字节** |

### 3.2 传感器状态码 (`sensor_status`)

- `MINIMC_TEMP_STATUS_OK = 0x00`：传感器正常，温度有效；
- `MINIMC_TEMP_STATUS_OPEN_CIRCUIT = 0x01`：热敏电阻开路或拔出（ADC $> 4075$），温度置为 `0x7FFF`；
- `MINIMC_TEMP_STATUS_SHORT_CIRCUIT = 0x02`：热敏电阻对地或电源短路（ADC $< 20$），温度置为 `0x7FFF`；
- `MINIMC_TEMP_STATUS_TIMEOUT = 0x03`：ADC 转换超时，未获得有效采样，温度置为 `0x7FFF`。

---

## 4. 各端处理逻辑与路由规范

### 4.1 SoC AP 宿主端
- 发送查询：根据 CLI 参数 `--target mc` 或 `--target th` 构造请求帧（`dst_id = 0x02` 或 `0x03`）；
- 解析接收：
  - 校验 `payload_len == 16`；
  - 校验 `sensor_status`：若为 `0x00`，输出温度浮点数（`current_temp_centi_c / 100.0`）；若非 `0x00`，输出告警提示并标记状态码；
  - 校验 `heater_duty_percent == 0`：若大于 0，立即触发安全告警；
  - 支持 `--json` 格式化输出。

### 4.2 MC 运动控制端
- 收到 `dst_id == 0x02`（本机）：
  - 读取 Marlin 热床温度，填充 16 字节载荷，回送响应帧至 AP（`dst_id = 0x01`）；
- 收到 `dst_id == 0x03`（TH 目标）：
  - 维持原生透明转发，通过内部串口转发至 TH，**严禁对发往 TH 的报文进行解包篡改**；
- 收到来自 TH 发往 AP（`dst_id == 0x01`）的响应报文：
  - 透明中继转发回 AP，置位 `MINIMC_ROUTE_IS_ROUTED`，递减 `hop_limit`。

### 4.3 TH 工具头端
- 收到 `dst_id == 0x03`：
  - 触发一次带超时计数器保护的 ADC 采样；
  - 执行 NTC 查表转换为摄氏度；
  - 检查开路/短路判定阈值；
  - 构造 16 字节载荷，发回报文至 AP（`dst_id = 0x01`，经 MC 中继）。
- 加热输出 PWM 强制保持输出为 0。

---

## 5. 编译期与运行时校验约定

所有使用本协议头文件 [`minimc_telemetry.h`](minimc_telemetry.h) 的工程，必须通过以下断言确保结构体布局不发生编译期漂移：
```c
#ifdef __cplusplus
static_assert(sizeof(minimc_temp_report_payload_t) == 16, "minimc_temp_report_payload_t must be 16 bytes");
#else
_Static_assert(sizeof(minimc_temp_report_payload_t) == 16, "minimc_temp_report_payload_t must be 16 bytes");
#endif
```
