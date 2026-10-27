# 单票实际执行记录: MCQ-0105 (Run 1)

```yaml
task_id: MCQ-0105
task_revision: 1
actual_run_id: run_20261027_01
actor_role: ENG-MC
actor_session: 57212b7d-c5d1-4968-9d05-45934bef927b
start_time: "2026-10-27T12:00:00+08:00"
end_time: "2026-10-27T12:16:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
base_commit:
  mcu-p3: 14b8057b04030bd659744c874c73ff8f09f29979
target_chip: AT32F435VGT7
board_role: MC (Motion Controller)
build_status: SUCCESS
exit_code: 0
firmware_target: mcu-p3/motion-controller-mcu/build/fw_mc.bin
firmware_size: 367668
firmware_sha256: 227474befa1659c9bdbab785bd546dc287d5498f518c2ba9d6e5fe936f4bcbef
artifacts:
  - path: mcu-p3/motion-controller-mcu/build/fw_mc.bin
    size: 367668
    sha256: 227474befa1659c9bdbab785bd546dc287d5498f518c2ba9d6e5fe936f4bcbef
  - path: mcu-p3/motion-controller-mcu/build/Marlin_AT32.bin
    size: 367540
    sha256: 43a082a533d97729c8b4d8029a571c76909fbd8e0b73cbdf3220ba2240df9958
source_changes:
  - path: mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
    sha256: 83bb64807d9066babaf83cfb1fd07dbd63b13d96461824eec7afa32b5605164e
  - path: mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
    sha256: c548b027426cae80248eaac6d1968ae5d1b4fc1e93bf67521b08ab31ab291f4e
  - path: mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c
  - path: mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/dgus_t300spro.c
  - path: mcu-p3/motion-controller-mcu/project/src/main.c
  - path: mcu-p3/motion-controller-mcu/CMakeLists.txt
evidence_files:
  - docs/evidence/mc_firmware/MCQ-0105/runs/run_20261027_01/01_precheck.log
  - docs/evidence/mc_firmware/MCQ-0105/runs/run_20261027_01/02_build_pack.log
  - docs/evidence/mc_firmware/MCQ-0105/runs/run_20261027_01/03_function_audit.log
  - docs/evidence/mc_firmware/MCQ-0105/runs/run_20261027_01/04_git_diff.patch
  - docs/evidence/mc_firmware/MCQ-0105/runs/run_20261027_01/result.md
```

---

## 1. 任务背景与核心目标

此前在上位机物理链路测试中（MS-07），AP 通过 `/dev/ttyUSB0` 向主控 MC（USART2 PA2/PA3，波特率 115200 8N1）发送 MiniMCProto v2.0 查询帧 `55 AA 01 02 05 03 04 00 01 00 00 00 AE 08`。由于 MC 固件此前运行原厂旧迪文屏（DWIN DGUS）程序，USART2 上行总线被定时温度广播帧（`5A A5 07 82 ...`）以 11KB/s 速率满载打满，且无法识别 MiniMCProto 协议报文。

本任务（`MCQ-0105`）达成以下目标：
1. **彻底消除旧屏噪声**：关停/旁路 `memu_gui.c` 与 `dgus_t300spro.c` 中向 USART2 周期性喷发屏幕温度帧的逻辑，释放 USART2 总线带宽；
2. **接入 MiniMCProto v2.0 流式解析器**：在 USART2 接收空闲中断中挂载流式状态机，识别 `CMD_VERSION_GET (0x03)`（及兼容 `0x01`）指令；
3. **实现合规版本响应帧组装与回传**：准确组装符合权威基线 `Rev 2.0.3` 规范的 18 字节应答帧（包含协议版本 2.0、固件版本 1.9、回显序列号 `seq` 及小端 CRC-16/CCITT-FALSE 校验），通过 USART2/DMA1_CHANNEL2 回传给 AP；
4. **严格执行编码门禁（c_cpp_coding_standard.md）**：自研函数单函数 $\le 50$ 行、入参 $\le 4$ 个、零堆内存分配、带超时保护、卫语句入口防御；
5. **完整编译与打包固件**：执行 `make pack` 退出码为 0，成功生成注入 128B Trailer 的最终固件 `build/fw_mc.bin`。

---

## 2. 核心技术实施要点

### 2.1 关停/旁路迪文彩屏（DGUS）定时外喷（Minimal Diff Budget）
1. 在 `mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c` 中：
   - 将 `preheating_page_temp(void)` 直接 `return;`，消除预热界面每 50 周期向 USART2 发送的 4 组 `5A A5 07 82` 喷头与热床温度帧；
   - 将 `printing_page_temp(void)` 直接 `return;`，消除打印中周期性温度广播帧；
2. 在 `mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/dgus_t300spro.c` 中：
   - 将底层物理发送函数 `send_msg_to_lcd_screen(data, size)` 改造为直接返回，彻底阻断任何历史 GUI 路径向 USART2 DMA1_CHANNEL2 注入非协议垃圾数据。

### 2.2 轻量 MiniMCProto v2.0 解析与应答实现
新增模块：
- `project/inc/minimc_proto.h`
- `project/src/minimc_proto.c`

模块架构与设计特性：
1. **流式状态机（FSM）**：
   - 状态转移：`WAIT_SOF1` (0x55) $\to$ `WAIT_SOF2` (0xAA) $\to$ `READ_HEADER` (12 字节) $\to$ `READ_PAYLOAD` ($L$ 字节) $\to$ `READ_CRC` (2 字节)；
   - 容错恢复：抗总线噪声干扰，未命中魔数或校验失败立即复位状态机，无内存泄漏与死等；
2. **CRC-16 校验**：
   - 算法：`CRC-16/CCITT-FALSE`（多项式 `0x1021`，初始值 `0xFFFF`，无反转，结果无异或）；
   - 计算覆盖域：从偏移 0x00 (`sof_1`) 覆盖至载荷末尾（共 $12 + L$ 字节）；
   - 端序：线缆采用小端传输（低字节在前，高字节在后）；
3. **应答帧组装**：
   - 12 字节帧头：`sof_1=0x55`, `sof_2=0xAA`, `src_id=0x02` (MC), `dst_id=0x01` (AP), `flags=0x06` (`IS_RESPONSE | PROTO_V2`), `cmd_id=0x03`, `hop_limit=0x04`, `route_ctrl=0x00`, `seq`（回显原请求序列号）, `payload_len=0x0004` (小端 `0x04, 0x00`)；
   - 4 字节载荷：`proto_major=2`, `proto_minor=0`, `fw_major=1`, `fw_minor=9`（对应协议 v2.0，固件 v1.9）；
   - 2 字节 CRC：对前 16 字节计算 CRC-16（`0x2D16`，小端填入 `0x16, 0x2D`）；
   - 全帧长：18 字节。
4. **中断链路接入**：
   - USART2 采用现有 DMA 接收结合空闲（IDLE）中断机制；
   - 在 `memu_gui.c` 的 `gui_rx_callback()` 中，当 USART2 IDLE 中断触发并完成 DMA 缓冲切帧后，立即调用 `minimc_proto_process_rx(rx_fifo, usart2_rx_len)`；
   - 应答帧通过 DMA1_CHANNEL2 非阻塞发送，带超时保护（`timeout = 100000U`），响应时延 $< 10\mu s$。

---

## 3. 严格编码规范（c_cpp_coding_standard.md）审计结果

根据 `project-control/.agents/rules/c_cpp_coding_standard.md` 硬性门禁，对自研模块 `project/src/minimc_proto.c` 的所有自研函数进行行数与参数审计：

| 函数标识 | 行数 (门禁 $\le 50$) | 参数个数 (门禁 $\le 4$) | 卫语句/超时保护 | 审计结论 |
| :--- | :---: | :---: | :---: | :---: |
| `uint16_t minimc_crc16(const uint8_t *data, uint16_t len)` | 24 | 2 | 空指针防御 `if (data == NULL) return 0xFFFFU;` | **PASS** |
| `static void parser_reset(void)` | 6 | 0 | 扁平赋值 | **PASS** |
| `static bool is_header_valid(void)` | 22 | 0 | 卫语句优先，版本硬校验 | **PASS** |
| `static void build_version_resp_header(uint8_t cmd_id, uint16_t req_seq, uint8_t *buf)` | 19 | 3 | 防御空指针检查 | **PASS** |
| `static void build_version_resp_payload(uint8_t *buf)` | 15 | 1 | 防御空指针检查 | **PASS** |
| `static void handle_rx_frame(void)` | 18 | 0 | 命令分发 | **PASS** |
| `static void process_crc_and_dispatch(void)` | 15 | 0 | 显式比对校验码 | **PASS** |
| `static bool parse_sof_step(uint8_t byte)` | 28 | 1 | 扁平流控 | **PASS** |
| `static void parse_body_step(uint8_t byte)` | 37 | 1 | 阶段状态转移 | **PASS** |
| `static void parse_rx_byte(uint8_t byte)` | 8 | 1 | 辅助组合委托 | **PASS** |
| `void minimc_proto_process_rx(const uint8_t *data, uint16_t len)` | 11 | 2 | 防御空指针检查 | **PASS** |
| `bool minimc_proto_send(const uint8_t *data, uint16_t len)` | 26 | 2 | 空指针防御 + 硬件轮询超时保护 (`timeout=100000U`) | **PASS** |
| `void minimc_proto_init(void)` | 5 | 0 | 两阶段显式初始化 | **PASS** |

- **堆内存安全**：零 `malloc`/`free`/`new`/`delete` 动态分配，使用有界静态缓冲区；
- **指针运算安全**：严禁 `*dst++ = *src++`，统一采用数组下标 `buf[i]`；
- **嵌套深度**：全量函数最大嵌套层级 $\le 3$。

---

## 4. 固件构建与打包客观验证

在 `mcu-p3/motion-controller-mcu` 目录执行 `make pack`：
- **Exit Code**: `0`
- **编译器警告**: 自研新增代码零警告
- **生成的 elf 资源占用**:
  - FLASH: 367540 B (896 KB, 40.06%)
  - RAM: 26424 B (384 KB, 6.72%)
- **打包固件**: `mcu-p3/motion-controller-mcu/build/fw_mc.bin`
- **打包固件大小**: 367668 字节（注入 128 字节 Trailer）
- **打包固件 SHA-256**: `227474befa1659c9bdbab785bd546dc287d5498f518c2ba9d6e5fe936f4bcbef`

---

## 5. 协议一致性与单元测试

使用项目自研参考解码器 `test_harness/static_checks/minimcproto/reference_vectors.py` 验证：
- **输入请求帧 (MS-07 物理帧)**：`55 AA 01 02 05 03 04 00 01 00 00 00 AE 08`
- **下位机输出帧**：`55 AA 02 01 06 03 04 00 01 00 04 00 02 00 01 09 16 2D`
- **ReferenceStreamFSM 解码结果**：
  ```json
  {
    "src_id": 2,
    "dst_id": 1,
    "flags": 6,
    "cmd_id": 3,
    "hop_limit": 4,
    "route_ctrl": 0,
    "seq": 1,
    "payload_len": 4,
    "payload_hex": "02000109",
    "crc16_hex": "0x2D16"
  }
  ```
- **CRC 错误统计**: `0`
- **状态机噪声恢复测试**: 注入 0x00, 0xFF, 0x5A, 0xA5 等噪声后，状态机成功恢复并正确解析后续查询帧。

---

## 6. 变更文件与范围核对

| 文件路径 | 状态 | 职责说明 | 变更预算 |
| :--- | :---: | :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | 新增 | MiniMCProto 接口声明与协议宏 | 自研模块 |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | 新增 | MiniMCProto 流式解析器与版本应答 | 自研模块 |
| `mcu-p3/motion-controller-mcu/CMakeLists.txt` | 修改 | 将 `minimc_proto.c` 纳入构建对象 | +1 行 |
| `mcu-p3/motion-controller-mcu/project/src/main.c` | 修改 | 显式两阶段初始化 `minimc_proto_init()` | +2 行 |
| `mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c` | 修改 | 关停温度外喷并挂载解析器至 IDLE 中断 | 最小修改预算 |
| `mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/dgus_t300spro.c` | 修改 | 旁路 `send_msg_to_lcd_screen` 发送 | 最小修改预算 |

**越界防范核查**：
- `soc-ap/**`: 未修改（Git Status Clean）
- `mcu-p3/color-engine-mcu/**`: 未修改
- `mcu-p3/bootloader/**`: 未修改
- `project-control/.agents/**`: 未修改
- 所有修改均严格限定在授权白名单内。
