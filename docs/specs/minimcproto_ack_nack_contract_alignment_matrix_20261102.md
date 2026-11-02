# MiniMCProto ACK/NACK 契约对齐与最小影响矩阵

> **文档编号**：`SPEC-ALIGN-20261102-01`  
> **关联 Issue**：`ISSUE-20261102-05`  
> **主导角色**：ARCH (系统架构师)  
> **基准规范**：`SPEC-PROTO-20261015-153000` Rev 2.0.3 (SHA256: `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`)  
> **生效范围**：`soc-ap`、`mcu-p3` (MC/TH)、`test_harness`、`project-control`  
> **状态**：**APPROVED / ACTIVE BASELINE**  

---

## 1. 冲突溯源与架构裁决

### 1.1 冲突背景与现象核查
在推进 AP-MC-TH 级联通信与固件一体化联调过程中，发现全系统对于否定应答（NACK）的命令码及载荷定义存在严重分歧与多源漂移：

1. **主通信总规范唯一权威定义**：
   依据 `project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` (Rev 2.0.3) §5.1 与 §5.2：
   - `CMD_ACK = 0x00`：双向确认，固定 **4 字节载荷**（`planner_buf_free` uint8, `rx_fifo_free_units` uint8, `reserved` uint16 LE）；
   - `CMD_NACK = 0x06`：双向否定应答，固定 **3 字节载荷**（`error_code` uint8, `expected_seq` uint16 LE）。
2. **派生级联 ICD 引入笔误**：
   派生文档 `project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md` 第 202 行在定义异常处置时误写为：
   `CMD_NACK（操作码 0x00，载荷长度 0x0002）`。
   该笔误导致 `CMD_ACK` 与 `CMD_NACK` 在派生契约中被赋予了完全相同的操作码 `0x00`，且载荷长度被截断为 2 字节（缺少 `expected_seq` 语义）。
3. **下游三端实现与测试用例发散**：
   由于下游实现阶段以派生 ICD 作为局部输入，导致误差扩散：
   - **`soc-ap`**：`core/host/query.h` 错误定义 `CMD_RESP_NACK = 0x00`，并在 `core/host/query.cpp` 中将接收到的 `0x00` 一律按 NACK 报错拦截；而 `contracts/twin/telemetry_types.h` 却遵照总规范定义了 `MINIMC_CMD_NACK 0x06U`，在 AP 代码库内部形成分裂；
   - **`mcu-p3` MC 固件**：`project/inc/minimc_proto.h` 宏定义 `MINIMC_CMD_NACK 0x00U`，且 `build_nack_resp` 仅生成 2 字节载荷（`err_code` + `0x00` 对齐补位）；
   - **`mcu-p3` TH 固件**：`io_toggle/inc/minimc_proto.h` 宏定义 `MINIMC_CMD_NACK 0x00U`，`build_nack_resp` 同样生成 2 字节载荷；
   - **`test_harness`**：`test_cases/cascade/query_cases.json` 中的用例 `CAS-NEG-008` 注入了 `cmd_id = 0x00` 且载荷为 2 字节的错误报文。

### 1.2 架构裁决结论
核查 Git 提交历史与架构治理记录，确认：
- 不存在任何由架构委员会、协议 Owner 或技术评审会批准的将 `CMD_NACK` 调整为 `0x00` 或修改为 2 字节载荷的正式变更提案；
- 派生 ICD 中的记录系文档起草过程中的笔误；
- 若将 `CMD_NACK` 改为 `0x00`，将与核心流控基元 `CMD_ACK (0x00)` 发生操作码直接碰撞，彻底破坏协议栈对确认与否定应答的基本判别能力。

**架构裁决规则**：
> [!IMPORTANT]
> 1. **权威唯一性**：主总规范 `SPEC-PROTO-20261015-153000` Rev 2.0.3 为全系统协议契约的**唯一权威原件**；
> 2. **禁止逆向篡改**：全系统贯彻绿地架构原则（Greenfield Architecture），严禁以“已有错误实现”反向倒灌篡改主总规范；
> 3. **单向收敛修正**：派生 ICD、三端代码（AP/MC/TH）以及 QA 测试用例必须 100% 纠偏，恢复与总规范严格一致；
> 4. **操作码解耦**：`CMD_ACK` 严格固定为 `0x00`（4 字节载荷）；`CMD_NACK` 严格固定为 `0x06`（3 字节载荷）。

---

## 2. ACK 与 NACK 权威协议契约

### 2.1 基础属性对比表

| 属性项 | 确认应答 (`CMD_ACK`) | 否定应答 (`CMD_NACK`) |
| :--- | :--- | :--- |
| **操作码 (Command ID)** | **`0x00`** | **`0x06`** |
| **传输方向** | 双向 (主 $\leftrightarrow$ 从) | 双向 (主 $\leftrightarrow$ 从) |
| **必须置位 Flags** | `0x06` (`IS_RESPONSE(0x02) \| PROTO_V2(0x04)`) | `0x06` (`IS_RESPONSE(0x02) \| PROTO_V2(0x04)`) |
| **载荷长度 (Payload Length)**| **固定 4 字节** (`0x0004`) | **固定 3 字节** (`0x0003`) |
| **整帧物理总长 (Total Length)**| **18 字节** (12B 帧头 + 4B 载荷 + 2B CRC) | **17 字节** (12B 帧头 + 3B 载荷 + 2B CRC) |
| **帧头 seq 语义** | 严格回显原请求帧的流水号 `seq` | 严格回显原请求帧的流水号 `seq` |
| **核心功能与语义** | 业务确认与信用流控回报 | 业务拒绝、协议异常通告与断点重传同步 |

### 2.2 二进制报文拓扑与逐字节结构

#### 1. CMD_ACK 报文结构 (18 字节)
```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  0x55 (SOF1)  |  0xAA (SOF2)  |    SRC_ID     |    DST_ID     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Flags (0x06) |  CmdID (0x00) |   Hop_Limit   |  Route_Ctrl   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        seq (16-bit LE)        |  payload_len = 0x0004 (16b LE)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|planner_buf_fre|rx_fifo_free_un|      reserved = 0x0000        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       CRC-16 (16-bit LE, 覆盖前 16 字节)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

#### 2. CMD_NACK 报文结构 (17 字节)
```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  0x55 (SOF1)  |  0xAA (SOF2)  |    SRC_ID     |    DST_ID     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Flags (0x06) |  CmdID (0x06) |   Hop_Limit   |  Route_Ctrl   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        seq (16-bit LE)        |  payload_len = 0x0003 (16b LE)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  error_code   |       expected_seq (16-bit Little-Endian)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       CRC-16 (16-bit LE, 覆盖前 15 字节)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 2.3 CMD_NACK 载荷字段定义与 expected_seq 语义
```c
struct __attribute__((packed)) minimc_payload_nack {
    uint8_t  error_code;          // 偏移 0x00: 标准错误码 (uint8)
    uint16_t expected_seq;        // 偏移 0x01: 接收端期望的下一个正确流水号 (uint16_t, Little-Endian)
};
```

#### `expected_seq` 语义及交互机制：
1. **流水号指示**：
   - 在停等（Stop-and-Wait）或滑动窗口通信中，当接收端因“序号超前/乱序”（`MINIMC_ERR_SEQ_OUT_OF_WINDOW`）或“重复过期帧”（`MINIMC_ERR_STALE_EXPIRED`）触发 NACK 时，必须在 `expected_seq` 中回填**本机当前期望接收的下一个流水号**；
   - 发送端在收到 NACK 后，依据该字段判断接收端状态，同步重置发送端滑窗序列并从 `expected_seq` 起始重传；
2. **非序号类错误的处理**：
   - 当因未知操作码（`0x04`）、参数非法拒绝（`0x06`）或设备繁忙（`0x05`）触发 NACK 时，接收端若未推进内部会话序号，`expected_seq` 应回填接收端当前的会话下一期待号（通常为当前请求 `seq + 1` 或保持不变）；
3. **关联校验要求**：
   - 请求端（如 AP）接收到 NACK 时，外层帧头的 `seq` 必须与原请求匹配（保证响应关联正确）；载荷内的 `expected_seq` 作为诊断与状态机对齐参考。

### 2.4 全局标准错误码清单 (Master Error Codes)

| 错误码常量 | 十六进制值 | 说明与语义 | 触发条件 / 场景 |
| :--- | :--- | :--- | :--- |
| `MINIMC_ERR_CRC` | `0x01` | 物理帧校验和错误 | 仅用于本地统计（线路上遇坏 CRC 默认静默丢弃） |
| `MINIMC_ERR_MTU_EXCEEDED` | `0x02` | 载荷长度超限 | `payload_len > 1024` 或超过本节点接收缓冲 |
| `MINIMC_ERR_SEQ_OUT_OF_WINDOW` | `0x03` | 序号超前/越界 (乱序) | 请求流水号脱离接收端有效滑动窗口 |
| `MINIMC_ERR_UNKNOWN_CMD` | `0x04` | 未知/不支持操作码 | 收到节点业务引擎未实现的命令码 |
| `MINIMC_ERR_DEVICE_BUSY` | `0x05` | 接收端繁忙 | 任务队列或硬件资源已满，稍后重试 |
| `MINIMC_ERR_COMMAND_REJECTED` | `0x06` | 参数非法/长度冲突 | 载荷长度与操作码规范不符，或业务参数校验失败 |
| `MINIMC_ERR_ROUTING_CONGESTION` | `0x07` | 路由拥塞丢弃 | 中继网关转发队列饱和丢包 |
| `MINIMC_ERR_STALE_EXPIRED` | `0x08` | 历史重传脱离缓存 | 重传请求已过时，无法从幂等缓存中恢复 |
| `MINIMC_ERR_SEQ_AMBIGUOUS` | `0x09` | 序号处于半周期分界盲区 | 流水号翻转边界模糊 |
| `MINIMC_ERR_HOP_EXCEEDED` | `0x0B` | 跳数耗尽防环 | 中继节点检测到 `hop_limit <= 1` |
| `MINIMC_ERR_ROUTING_FAILED` | `0x0C` | 路由不可达 | 目标节点离线或目标端口未开通 |
| `MINIMC_ERR_OTA_ERASE_FAIL` | `0x10` | Flash 扇区擦除失败 | 固件升级过程中物理 Flash 操作报错 |
| `MINIMC_ERR_OTA_WRITE_FAIL` | `0x11` | Flash 编程写入失败 | 固件分块写入 Flash 失败 |
| `MINIMC_ERR_OTA_CRC_MISMATCH` | `0x12` | 固件全量 CRC32 校验不匹配 | 升级结束全量校验不通过 |
| `MINIMC_ERR_OTA_INVALID_OFFSET`| `0x13` | 固件数据偏移不连续 | 分块数据偏移越界或乱序 |
| `MINIMC_ERR_OTA_IMAGE_OVERSIZE`| `0x14` | 固件尺寸超过分区限制 | 镜像大小超过 Flash 物理分区最大限制 |

---

## 3. 跨仓库代码与资产最小影响矩阵

| 序号 | 目标模块 / 仓库 | 涉及具体文件路径 | 当前存量状态 (偏差) | 纠偏实施细则 (规范基准) | 负责角色 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M1** | **`project-control`** | `docs/interfaces/ap_mc_th_readonly_cascade_icd.md` | 第 202 行定义为操作码 `0x00`、2 字节载荷 | 修正为操作码 `0x06`、载荷长度 `0x0003` (3 字节: `error_code` + `expected_seq`)，补全标准错误码表 | **ARCH** *(已完成)* |
| **M2** | **`soc-ap`** | `core/host/query.h` | `CMD_RESP_NACK = 0x00` | 将枚举值修改为 `CMD_RESP_NACK = 0x06` | **ENG-FWD** |
| **M3** | **`soc-ap`** | `core/host/query.cpp` | `query_validate_frame` 仅检查 `0x00` 并打印固定报错 | 匹配 `frame->header.cmd_id == CMD_RESP_NACK` (`0x06`)；安全提取 3 字节载荷（`error_code` 与 `expected_seq`），并在 `res->error_msg` 中输出结构化错误信息（例如 `"Received CMD_NACK (code=0x%02X, expected_seq=%u)"`） | **ENG-FWD** |
| **M4** | **`soc-ap`** | `contracts/twin/telemetry_types.h` | 已经是 `MINIMC_CMD_NACK 0x06U` | 保持不变，验证其与 `query.h` 完全一致 | **ENG-FWD** |
| **M5** | **`mcu-p3` (MC)** | `motion-controller-mcu/project/inc/minimc_proto.h` | `#define MINIMC_CMD_NACK 0x00U` | 修改为 `#define MINIMC_CMD_NACK 0x06U` | **ENG-MC** |
| **M6** | **`mcu-p3` (MC)** | `motion-controller-mcu/project/src/minimc_proto.c` | `build_nack_resp` 组装 2 字节载荷，总长 16B | 1. 载荷长度填 `out_buf[10] = 0x03U; out_buf[11] = 0x00U;`<br/>2. 填入字段：`out_buf[12] = err_code; out_buf[13] = (uint8_t)(expected_seq & 0xFFU); out_buf[14] = (uint8_t)((expected_seq >> 8U) & 0xFFU);`<br/>3. 计算前 15 字节 CRC-16：`const uint16_t crc = minimc_crc16(out_buf, 15U);`<br/>4. 填入 CRC：`out_buf[15] = crc & 0xFF; out_buf[16] = crc >> 8;`<br/>5. 整帧长度更新为 17 字节：`*out_len = 17U;` | **ENG-MC** |
| **M7** | **`mcu-p3` (TH)** | `color-engine-mcu/io_toggle/inc/minimc_proto.h` | `#define MINIMC_CMD_NACK 0x00U` | 修改为 `#define MINIMC_CMD_NACK 0x06U` | **ENG-TH** |
| **M8** | **`mcu-p3` (TH)** | `color-engine-mcu/io_toggle/src/app/minimc_proto.c` | `build_nack_resp` 组装 2 字节载荷，总长 16B | 1. 载荷长度填 `out_buf[10] = 0x03U; out_buf[11] = 0x00U;`<br/>2. 填入字段：`out_buf[12] = err_code; out_buf[13] = (uint8_t)(expected_seq & 0xFFU); out_buf[14] = (uint8_t)((expected_seq >> 8U) & 0xFFU);`<br/>3. 计算前 15 字节 CRC-16 并填入 `out_buf[15..16]`<br/>4. 返回总长度 17 字节 (`return 17U;`) | **ENG-TH** |
| **M9** | **`test_harness`** | `test_cases/cascade/query_cases.json` | `CAS-NEG-008` 注入 `55AA03010600030402000200040084D6` (cmd=0x00, len=2) | 更新 `CAS-NEG-008` 注入流量为标准 17 字节 NACK 帧：`55AA030106060304020003000402003790`<br/>- 操作码：`0x06`<br/>- 载荷长：`0x0003`<br/>- 载荷内容：`0x04` (UNKNOWN_CMD), `0x0002` (expected_seq)<br/>- CRC16/CCITT-FALSE：`0x9037` (小端 `37 90`)<br/>- 预期行为更新为捕获 `CMD_NACK (0x06)` 携带错误码 `0x04` | **QA** |
| **M10**| **`test_harness`** | `static_checks/cascade/run_query_cases.py` | 运行现有用例集 | 确保在更新 `query_cases.json` 后全量黄金用例与 CRC 校验 100% 通过 | **QA** |

---

## 4. 黄金测试向量对齐参考 (CAS-NEG-008 深度解析)

以 `CAS-NEG-008`（终端从机 TH 回发标准拒绝报文）为例，纠偏前后的物理十六进制帧对比如下：

### 4.1 纠偏前 (错误报文 - 已废止)
```text
十六进制流: 55 AA 03 01 06 00 03 04 02 00 02 00 04 00 84 D6 (共 16 字节)
字段切片:
  [00..01] 55 AA       : SOF
  [02]     03          : SRC = TH
  [03]     01          : DST = AP
  [04]     06          : Flags = IS_RESPONSE | PROTO_V2
  [05]     00          : Cmd ID = 0x00 (错误！与 CMD_ACK 碰撞)
  [06]     03          : Hop Limit = 3
  [07]     04          : Route Ctrl = ROUTE_IS_ROUTED
  [08..09] 02 00       : Seq = 2
  [10..11] 02 00       : Payload Len = 2 (错误！非总规范 3 字节)
  [12..13] 04 00       : Payload = 0x04 (ERR_UNKNOWN_CMD), 0x00 (补位)
  [14..15] 84 D6       : CRC-16 (0xD684, Little-Endian)
```

### 4.2 纠偏后 (权威黄金向量 - 标准 17 字节)
```text
十六进制流: 55 AA 03 01 06 06 03 04 02 00 03 00 04 02 00 37 90 (共 17 字节)
字段切片:
  [00..01] 55 AA       : SOF
  [02]     03          : SRC = TH
  [03]     01          : DST = AP
  [04]     06          : Flags = IS_RESPONSE | PROTO_V2
  [05]     06          : Cmd ID = 0x06 (正确！CMD_NACK)
  [06]     03          : Hop Limit = 3
  [07]     04          : Route Ctrl = ROUTE_IS_ROUTED
  [08..09] 02 00       : Seq = 2 (回显请求流水号)
  [10..11] 03 00       : Payload Len = 3 (严格符合规范)
  [12]     04          : error_code = 0x04 (MINIMC_ERR_UNKNOWN_CMD)
  [13..14] 02 00       : expected_seq = 2 (uint16_t LE)
  [15..16] 37 90       : CRC-16/CCITT-FALSE (0x9037, Little-Endian: 0x37, 0x90)
```
*CRC 计算验证*：
算法 `CRC-16/CCITT-FALSE`（多项式 `0x1021`，初值 `0xFFFF`，结果异或 `0x0000`），对前 15 字节 `55AA03010606030402000300040200` 计算结果为 `0x9037`，低字节 `0x37`、高字节 `0x90`，完全相符。

---

## 5. 唯一权威登记位置及单向防发散检查方法

### 5.1 契约源头权威登记规则
1. **单一事实源 (Single Source of Truth)**：
   - 全系统协议契约的最高且唯一权威文件为：  
     `project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md`
   - 所有派生级联 ICD、模块接口文档及代码实现必须以该文件的特定版本（当前为 Rev 2.0.3）和 SHA256 为不可篡改基准。
2. **派生文档治理**：
   - 派生 ICD 仅允许对总规范中已定义的字段进行场景化约束与裁剪，**严禁重新分配操作码、严禁缩减/扩充总规范已锁定的载荷字段宽度**。
   - 任何涉及协议操作码、载荷布局或状态机流转的调整，必须走正规变更流程，首先在总规范中完成修订并取得系统多方会签，方可向下游同步。

### 5.2 跨仓库单向防发散自动化检查门禁
为彻底杜绝后续因人工笔误或端侧私自实现造成契约漂移，在 `test_harness` 静态检查套件中建立防发散扫描机制：

1. **检查执行位置**：  
   `test_harness/static_checks/minimcproto/check_opcode_alignment.py`
2. **扫描对象与强制断言**：
   - 检查 `soc-ap/core/host/query.h` 与 `soc-ap/contracts/twin/telemetry_types.h`：  
     断言 `CMD_RESP_NACK == 0x06` 且 `MINIMC_CMD_NACK == 0x06U`；
   - 检查 `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h`：  
     断言 `MINIMC_CMD_NACK == 0x06U`；
   - 检查 `mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h`：  
     断言 `MINIMC_CMD_NACK == 0x06U`；
   - 检查 `project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md`：  
     断言 NACK 操作码为 `0x06`，载荷长度为 `0x0003`；
   - 检查 `test_harness/test_cases/cascade/query_cases.json`：  
     断言 `CAS-NEG-008` 的报文中 `cmd_id` 必须为 `0x06`，长度为 `3`，且 CRC16 校验合法。
3. **CI 门禁与提交拦截**：
   - 任何涉及上述文件的 Git Commit 或 PR，必须自动触发上述脚本校验；
   - 任何操作码或长度不一致均被判定为阻断性失败（Exit Code != 0），严禁合入主线分支。
