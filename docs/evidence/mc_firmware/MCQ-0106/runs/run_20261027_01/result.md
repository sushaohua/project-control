# 单票实际执行记录: MCQ-0106 (Run 1)

```yaml
task_id: MCQ-0106
task_revision: 1
actual_run_id: run_20261027_01
actor_role: ENG-MC
actor_session: 57212b7d-c5d1-4968-9d05-45934bef927b
start_time: "2026-10-27T13:50:00+08:00"
end_time: "2026-10-27T13:58:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
base_commit:
  mcu-p3: 23e8d5c8052f9a76d4981766627aa5aa1c7ee07c
candidate_commit:
  mcu-p3: a679133204ecbb81ad48694f5372c125db2e749f
target_chip: AT32F435VGT7
board_role: MC (Motion Controller)
build_status: SUCCESS
exit_code: 0
firmware_target: mcu-p3/motion-controller-mcu/build/fw_mc.bin
firmware_size: 367924
firmware_sha256: c11067d9e3fcc082ffff701a7041aeafcc81dfdfb2a18e32be6ccf6dd2d7eab5
artifacts:
  - path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
    size: 367924
    sha256: c11067d9e3fcc082ffff701a7041aeafcc81dfdfb2a18e32be6ccf6dd2d7eab5
  - path: mcu-p3/motion-controller-mcu/build/Marlin_AT32.bin
    size: 367796
    sha256: 44e130bae7b7e34d5c66ae761b59faeb0ddfdad75b9f19fd0f7fe877ba7a5b09
source_changes:
  - path: mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
    sha256: 235436443000f8d33d1dd7b6082a2907a1c4d7d4c3aaf3d32730623e43fb03f2
  - path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
    sha256: b1b6c99b1d8008ba4da70b5c88a90cb9a230361a0bf10adba772a489c7e8e4bd
evidence_files:
  - docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/01_precheck.log
  - docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/02_build_pack.log
  - docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/03_function_audit.log
  - docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/04_git_diff.patch
  - docs/evidence/mc_firmware/MCQ-0106/runs/run_20261027_01/result.md
```

---

## 1. 任务背景与核心目标

在前序微任务 `MCQ-0105` 中，MC 主控（AT32F435VGT7）已成功接入 MiniMCProto v2.0，消除了迪文屏 11KB/s 垃圾噪声，并实现了对自身版本（MC 1.9）的闭环响应（实测 RTT 6.14ms）。

本任务（`MCQ-0106`）目标为打通 AP $\to$ MC $\to$ TH $\to$ MC $\to$ AP 的板间双向业务代理通路：
1. **定义节点地址**：在 `project/inc/minimc_proto.h` 增加 `MINIMC_NODE_TH 0x03U`；
2. **目的地址分发**：在 `minimc_proto.c` 的 `handle_rx_frame()` 中，检查帧头目标地址 `dst_id`：
   - 若 `dst_id == MINIMC_NODE_MC (0x02)` 或广播 `0xFF`：保持原有 MC 自身响应不变；
   - 若 `dst_id == MINIMC_NODE_TH (0x03)`：识别为面向从控 TH 的指令，触发板间转发；
3. **USART6 下发探测与超时等待**：
   - 调用 `forward_uart_send_line("M115", 4U)` 向 USART6（921600 8N1）发送 G-code 版本探测；
   - 轮询等待 TH 回复（检查 `forward_uart_dma.forward_uart_rx_complete`，强制设置 200,000 次循环硬件超时保护计数器，严禁死等）；
4. **MiniMCProto 响应帧封装与回传**：
   - 收到 TH 回传后，格式化合规 MiniMCProto 应答帧：`src_id=0x03` (TH), `dst_id=0x01` (AP), `flags=0x06`, `payload_len=4`, `payload=[0x02, 0x00, 0x01, 0x00]`（TH 协议 2.0，固件 1.0），计算 CRC-16/CCITT-FALSE，通过 USART2（`minimc_proto_send`）回发 AP；
   - 超时未收到 TH 回复时，静默丢弃，严禁伪造成功响应；
5. **编码门禁与固件构建**：
   - 100% 遵从 `c_cpp_coding_standard.md`；
   - `make -C mcu-p3/motion-controller-mcu pack` 退出码 0，成功生成 `build/fw_mc.bin`。

---

## 2. 核心技术实施要点

### 2.1 节点定义与报头合法性扩充
- 在 `project/inc/minimc_proto.h` 中增加宏定义：
  ```c
  #define MINIMC_NODE_TH 0x03U
  ```
- 在 `project/src/minimc_proto.c` 的 `is_header_valid()` 中，扩充合法目的地址校验：
  ```c
  const bool is_valid_dst = (dst_id == MINIMC_NODE_MC) ||
                            (dst_id == MINIMC_NODE_TH) ||
                            (dst_id == 0xFFU);
  ```

### 2.2 MC 与 TH 差异化应答封装
- 将帧头与载荷构造拆解为两个辅助函数：
  - `build_version_resp_header(src_id, cmd_id, req_seq, buf)`：入参显式指定 `src_id`（MC 为 `0x02`，TH 为 `0x03`），回显请求 `cmd_id` 与 `req_seq`；
  - `build_version_resp_payload(fw_minor, buf)`：入参显式指定固件次版本（MC 为 9 即 1.9，TH 为 0 即 1.0），末尾填充小端 CRC-16；
- 保持单一职责，入参均 $\le 4$ 个，函数规模 $\le 20$ 行。

### 2.3 TH 代理转发状态机与硬件保护
- 封装 `handle_th_query(cmd_id, req_seq)`：
  1. 清除旧完成标志：`forward_uart_dma.forward_uart_rx_complete = 0U;`
  2. 触发 USART6 DMA 发送：`forward_uart_send_line("M115", 4U);`
  3. 带超时保护等待 TH 回传（USART6 IDLE 中断置位 `rx_complete`）：
     ```c
     uint32_t timeout = 200000U;
     while ((forward_uart_dma.forward_uart_rx_complete == 0U) && (timeout > 0U))
     {
         timeout--;
     }
     if (forward_uart_dma.forward_uart_rx_complete == 0U)
     {
         return; /* 超时退出，严禁伪造应答 */
     }
     ```
  4. 组装 18 字节响应帧并发送：`minimc_proto_send(resp_buf, 18U);`
  5. 复位接收完成标志位：`forward_uart_dma.forward_uart_rx_complete = 0U;`

---

## 3. 编码规范（c_cpp_coding_standard.md）审计结果

对自研模块 `project/src/minimc_proto.c` 的 15 个函数进行全面审计：

| 函数标识 | 行数 (门禁 $\le 50$) | 参数个数 (门禁 $\le 4$) | 卫语句 / 防御 | 结论 |
| :--- | :---: | :---: | :---: | :---: |
| `uint16_t minimc_crc16(const uint8_t *data, uint16_t len)` | 24 | 2 | 空指针防御 `if (data == NULL) return 0xFFFFU;` | **PASS** |
| `static void parser_reset(void)` | 6 | 0 | 扁平赋值 | **PASS** |
| `static bool is_header_valid(void)` | 24 | 0 | 目的地址/版本硬校验 | **PASS** |
| `static void build_version_resp_header(uint8_t src_id, uint8_t cmd_id, uint16_t req_seq, uint8_t *buf)` | 19 | 4 | 防御空指针检查 | **PASS** |
| `static void build_version_resp_payload(uint8_t fw_minor, uint8_t *buf)` | 15 | 2 | 防御空指针检查 | **PASS** |
| `static void handle_mc_query(uint8_t cmd_id, uint16_t req_seq)` | 7 | 2 | 模块委托调用 | **PASS** |
| `static void handle_th_query(uint8_t cmd_id, uint16_t req_seq)` | 22 | 2 | 硬件轮询超时保护 (`timeout=200000U`) | **PASS** |
| `static void handle_rx_frame(void)` | 25 | 0 | 目的地址路由分发 | **PASS** |
| `static void process_crc_and_dispatch(void)` | 15 | 0 | 显式校验比对 | **PASS** |
| `static bool parse_sof_step(uint8_t byte)` | 28 | 1 | 扁平控制流 | **PASS** |
| `static void parse_body_step(uint8_t byte)` | 37 | 1 | 阶段状态转移 | **PASS** |
| `static void parse_rx_byte(uint8_t byte)` | 8 | 1 | 辅助组合委托 | **PASS** |
| `void minimc_proto_process_rx(const uint8_t *data, uint16_t len)` | 11 | 2 | 防御空指针检查 | **PASS** |
| `bool minimc_proto_send(const uint8_t *data, uint16_t len)` | 26 | 2 | 硬件发送超时保护 (`timeout=100000U`) | **PASS** |
| `void minimc_proto_init(void)` | 5 | 0 | 两阶段初始化 | **PASS** |

- **最大函数行数**: 37 行（远低于 50 行门禁）
- **最大函数参数**: 4 个（满足 $\le 4$ 门禁）
- **动态内存分配**: 零 `malloc`/`free`
- **指针运算**: 数组下标显式递增，严禁 `*dst++`
- **嵌套深度**: 最大深度 $\le 3$ 层

---

## 4. 固件构建与打包客观验证

在 `mcu-p3/motion-controller-mcu` 执行 `make pack`：
- **Exit Code**: `0`
- **编译告警**: 新增模块零告警
- **ELF 存储占用**:
  - FLASH: 367796 B (896 KB, 40.09%)
  - RAM: 26424 B (384 KB, 6.72%)
- **打包固件**: `mcu-p3/motion-controller-mcu/build/fw_mc.bin`
- **固件大小**: 367924 字节
- **固件 SHA-256**: `c11067d9e3fcc082ffff701a7041aeafcc81dfdfb2a18e32be6ccf6dd2d7eab5`
- **mcu-p3 Commit Hash**: `a679133204ecbb81ad48694f5372c125db2e749f`

---

## 5. 协议一致性与单元测试

使用项目参考解码器（`reference_vectors.py`）验证：
1. **MC 查询响应**:
   - Query: `55 AA 01 02 05 03 04 00 01 00 00 00 AE 08`
   - Resp:  `55 AA 02 01 06 03 04 00 01 00 04 00 02 00 01 09 16 2D`
   - 解码结果: `src_id=0x02`, `dst_id=0x01`, `fw_ver=1.9`, CRC `0x2D16` 匹配。
2. **TH 查询响应**:
   - Query: `55 AA 01 03 05 03 04 00 01 00 00 00 8D E3`
   - Resp:  `55 AA 03 01 06 03 04 00 01 00 04 00 02 00 01 00 5E C7`
   - 解码结果: `src_id=0x03`, `dst_id=0x01`, `fw_ver=1.0`, CRC `0xC75E` 匹配。
3. **TH 超时保护**:
   - 当 TH 未响应时，MC 超时退出，未发送任何伪造报文。
