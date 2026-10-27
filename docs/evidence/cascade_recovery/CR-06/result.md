# CR-06 交付与验收记录：TH原生MiniMCProto固件实现与数据流分流

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-06` |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` |
| **执行者 / 角色** | `9e5411f4-acad-421e-b487-9e68b9483320` (COORD) |
| **对应底层规范** | [`ICD-CASCADE-READONLY-20261027`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md) |
| **解决目标** | TH 端原生接入 MiniMCProto v2.0，准确自报真实固件版本与心跳测量，实现二进制业务口与旧文本 G-code 入口的分流隔离 |
| **涉及仓库** | `mcu-p3`（提交 `af279a8c24dde92a0145d767c1c6478cfef05994`，分支 `feat/soc-debug`） |
| **产出固件** | `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` (71176 字节, SHA-256: `5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d`) |
| **验收状态** | **PASS (100% 独立黄金向量验证与固件编译打包闭环)** |

---

## 1. 核心实现与分流隔离内容

### 1.1 原生 MiniMCProto v2.0 协议栈接入 (`minimc_proto.h` / `minimc_proto.c`)
- **编译期结构体布局校验**：
  - `_Static_assert(sizeof(minimc_header_t) == 12)`
  - `_Static_assert(sizeof(minimc_version_report_payload_t) == 16)`
  - `_Static_assert(sizeof(minimc_pong_payload_t) == 12)`
- **版本查询响应 (`GET_VERSION`, cmd_id=0x01)**：
  - TH 本机作为 `src_id=0x03` 生成原生 `CMD_VERSION_REPORT` (0x02)；
  - 携带真实版本元数据：`proto_ver=2.0`、`firmware_ver=1.0`、`boot_id=0x8877AA55`、`git_commit=0x6356C05A`、`capability_flags=7`；
  - 产出帧与独立黄金用例 `CAS-POS-002` 逐字节 100% 吻合：`55AA030106020400020010000200010055AA77885AC05663070000008FE3`。
- **心跳与时延测量响应 (`PING`, cmd_id=0x03)**：
  - TH 本机生成原生 `CMD_PONG` (0x04)；
  - 回显请求方 `t_originate_ms`，并上报真实接收时间戳 `t_receive_ms`、`planner_buf_free=0`、`rx_fifo_free_units=4`；
  - 产出帧与独立黄金用例 `CAS-POS-004` 逐字节 100% 吻合：`55AA03010604040001000C007856341290563412000400000D78`。
- **未知命令防护**：
  - 遇到未知/非法指令回复标准 `CMD_NACK` (0x00)，携带错误码 `0x04`。

### 1.2 二进制业务流与文本 G-code 流透明分流 (`usart.c` / `usart.h`)
- **USART1 DMA 接收无缝解耦**：
  - 由 `minimc_proto_poll()` 流式消费 DMA 环形缓冲区字节；
  - 识别到 `0x55 0xAA` 序列时，进入 MiniMCProto 二进制状态机汇聚帧并校验 CRC，二进制报文绝不流入文本缓冲区；
  - 非二进制字节（ASCII G-code 指令字符）透明推入 `s_text_ring`（512 字节环形缓冲区）；
  - `USART1_has_byte()` 与 `USART1_get_byte()` 改为无阻塞消费 `s_text_ring`，实现原有运动/温控文本 G-code 接收逻辑零侵入、零污染。
- **有界二进制发送与硬件超时保护**：
  - 实现 `usart1_send_raw(const uint8_t *data, uint16_t len)`；
  - 严禁空死等，所有外设与 DMA 状态等待均具备 500,000 次轮询递减超时保护退出机制。

### 1.3 主循环集成与零堆内存分配 (`main.c` / `Makefile`)
- `main.c` 显式两阶段初始化调用 `minimc_proto_init()`，并在 `while(1)` 主循环周期推进 `minimc_proto_poll()`；
- `Makefile` 注册新增 `src/app/minimc_proto.c`，使用原有 GCC 工具链与固件打包流程。

---

## 2. 验收证据与测试记录

### 2.1 独立黄金向量逐字节验证
针对 `test_harness/test_cases/cascade/query_cases.json` 中的全部 TH 原生黄金向量执行独立脚本校验：
- `CAS-POS-002` (GET_VERSION $\to$ VERSION_REPORT): 100% 逐字节匹配 (`True`)；
- `CAS-POS-004` (PING $\to$ PONG): 100% 逐字节匹配 (`True`)。

### 2.2 固件构建与打包
```text
==================================================
 [PACK] 固件打包完成
 - 原始输入文件: build/fw_th.bin (71048 字节)
 - 有效代码净载: 71048 字节
 - 目标板卡架构: 0x42300001 [TH (AT32F423)]
 - 固件版本编号: 0x0100FC27
 - 注入构建时间: 1793105416 (2026-10-27 20:50:16)
 - SHA-256 摘要: 19b70329f16c694174328a56015eeb8f3ff2fc071a80913bc41e6f3a30a3979c
 - 最终输出文件: build/fw_th.bin (71176 字节)
 - Sector 127 锚点: build/anchor.bin (140 字节)
==================================================
```

### 2.3 代码规范与硬性门禁核验
- **函数规模硬性门禁**：所有自研非结构体函数均严格控制在 50 行以内（`build_pong_resp` 46 行，`build_version_resp` 44 行，`parser_step_body` 43 行，`minimc_proto_handle_frame` 41 行，`parser_step_sof` 38 行，其余均 $< 30$ 行）。
- **入参个数硬性门禁**：所有自研函数参数均严格 $\le 4$ 个。
- **内存安全**：零动态堆内存分配（零 malloc/free/new/delete），编译期 `_Static_assert` 结构体布局检查。
- **控制流与接口防御**：只读入参全部加 `const`，公开入口严格第一行空指针防御（Guard Clause），嵌套深度 $\le 3$ 层。
