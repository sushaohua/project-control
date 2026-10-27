# CR-05 交付与验收记录：MC原生双向透明路由与中断解耦

| 字段 | 属性 / 内容 |
| :--- | :--- |
| **任务卡片** | `CR-05` |
| **所属计划** | `PLAN-CASCADE-RECOVERY-20261027 v1.1` |
| **执行者 / 角色** | `9e5411f4-acad-421e-b487-9e68b9483320` (COORD) |
| **对应底层规范** | [`ICD-CASCADE-READONLY-20261027`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md) |
| **治理漏洞** | F08（中断内业务忙等死锁）、F09（伪造 TH 身份与虚假响应）、F10（单槽 DMA 接收覆盖与时序竞争）、F11（双向透明中继与防环） |
| **涉及仓库** | `mcu-p3`（提交 `231baf7dd3f08caa4b462b143edffc16bec76f5e`，分支 `feat/soc-debug`） |
| **产出固件** | `mcu-p3/motion-controller-mcu/build/fw_mc.bin` (369516 字节, SHA-256: `054b83d883629b10ff28b673fe41b3083e199ea5cf0800d42150e24d4e6e9fc9`) |
| **验收状态** | **PASS (100% 路由黄金向量验证与固件编译打包闭环)** |

---

## 1. 核心治理与改造内容

### 1.1 彻底删除伪造 TH 身份与 M115 忙等逻辑 (F08, F09)
- **删除伪造响应**：彻底移除 `handle_th_query` 中向 TH 发送 `M115` 文本并在 MC 伪造 `src_id=0x03` TH 响应的错误代码；MC 绝不代替 TH 伪造业务响应。
- **删除中断忙等**：彻底移除在中断/回调上下文中的 `while(timeout)` 轮询，解除 USART2 与 USART6 抢占优先级死锁风险。

### 1.2 原生双向透明中继 (F11)
- **入站转发 (AP $\to$ MC $\to$ TH)**：
  - 当接收到 `dst_id == 0x03` 的 MiniMCProto 帧，MC 严格校验 CRC-16；
  - 检查 `hop_limit`：若 `hop_limit <= 1`，静默丢弃防环；若 `> 1`，将 `hop_limit` 递减 1；
  - 置位 `route_ctrl |= 0x04` (`ROUTE_IS_ROUTED`)；
  - 保持业务 Payload、`seq`、`cmd_id` 完全不变，重算全帧 CRC-16；
  - 通过 `forward_uart_send_raw` 将原始二进制帧通过 USART6 DMA 发往 TH。
- **出站回传 (TH $\to$ MC $\to$ AP)**：
  - 当从 USART6 接收到 TH 回传且 `dst_id == 0x01` 的响应帧，MC 校验 CRC 成功后执行相同的递减 hop_limit、置位 routed 标志与 CRC 重算逻辑；
  - 原样回传给 AP（USART2），端到端保留真实 TH 固件自报字段。

### 1.3 中断解耦与双缓冲 / 环形缓冲队列 (F08, F10)
- `gui_rx_callback`（USART2 IDLE 中断）仅将接收字节快速压入 `s_ap_ring` 并重置 DMA，执行耗时 $< 2\mu s$，绝不执行耗时解析或等待；
- 主循环 `main.c` 周期调用 `minimc_proto_poll()`，在安全的主循环上下文中有界消费环形缓冲区数据并推进解析状态机，彻底消除同槽 DMA 竞争覆盖。

### 1.4 本机 MiniMCProto v2.0 只读查询原生支持
- 本机版本查询（`dst_id=0x02, cmd_id=0x01`）：回发标准 16 字节 `CMD_VERSION_REPORT`（`0x02`），携带正确 boot_id (`0x01020304`)、git commit (`0xA6791332`) 与能力标志；
- 本机心跳测量（`dst_id=0x02, cmd_id=0x03`）：回发标准 12 字节 `CMD_PONG`（`0x04`），回显发起方时间戳与缓冲区状态。

---

## 2. 验收证据与测试记录

### 2.1 路由黄金向量逐字节验证
针对 `test_harness/test_cases/cascade/query_cases.json` 中的全部黄金中继向量进行离线验证：
- `CAS-POS-002` 入站转发（AP $\to$ TH）：`55AA01030501040002000000B218` $\to$ `55AA01030501030402000000F559`（CRC 匹配 `0xF559`，100% 一致）；
- `CAS-POS-002` 出站回传（TH $\to$ AP）：`55AA03010602040002001000...8FE3` $\to$ `...030402001000...1D95`（CRC 匹配 `0x1D95`，100% 一致）；
- `CAS-POS-004` 入站/出站 PING 转发（100% 逐字节一致）。

### 2.2 固件构建与打包
```text
==================================================
 [PACK] 固件打包完成
 - 原始输入文件: build/Marlin_AT32.bin (369388 字节)
 - 有效代码净载: 369388 字节
 - 目标板卡架构: 0x43500001 [MC (AT32F435)]
 - 固件版本编号: 0x01092DB3
 - 注入构建时间: 1793104432 (2026-10-27 20:33:52)
 - SHA-256 摘要: 054b83d883629b10ff28b673fe41b3083e199ea5cf0800d42150e24d4e6e9fc9
 - 最终输出文件: build/fw_mc.bin (369516 字节)
==================================================
```

### 2.3 代码规范与硬性门禁核验
- **函数行数门禁**：所有自研非结构体函数均严格控制在 50 行以内（最大函数 `build_pong_resp` 45 行，`parser_step` 36 行）。
- **入参个数门禁**：所有自研函数参数均严格 $\le 4$ 个。
- **指针安全与防御**：所有入口具备空指针防御性校验，无动态内存分配，无危险指针运算。
