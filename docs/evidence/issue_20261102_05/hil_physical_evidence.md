# ISSUE-20261102-05 现场物理 HIL 联调实测与固件部署存证报告

| 属性 | 内容 |
| :--- | :--- |
| **任务编号** | `TASK-INT-01` (ISSUE-20261102-05) |
| **任务主题** | 锁定四仓组合候选、固件打包、现场物理部署与物理 HIL 联调实测 |
| **执行角色** | `INTEGRATOR` (系统集成工程师) |
| **执行会话 ID** | `4b120074-de2b-46f3-bd39-af85494c3dca` |
| **测试时间** | `2026-11-02 21:00:43.840 ~ 21:00:44.369+08:00` |
| **测试环境** | 宿主: VMware Ubuntu 22.04 LTS (`192.168.77.134`), 用户 `sushaohua`<br>硬件: Twin AT32 物理板卡 (AT32F435 MC + AT32F423 TH), 双 ST-Link V2, CH340 串口 |
| **串口端口** | `/dev/ttyUSB0` (QinHeng Electronics CH340, USB Bus 1-2.1:1.0, 115200 8N1) |
| **整体验收结论** | **100% 验收通过 (PASS)**: 正常链路与否定应答对齐链路双向 Hex 报文、字段切片、CRC16 校验及 AP 宿主报错行为全量闭环 |

---

## 1. 锁定四仓组合候选与制品哈希存证

### 1.1 锁定 Candidate Commit 清单
- `soc-ap`: `427dd6d82caceebb7b4642e78f1dbfa96ff5fc84` (`fix(query): align CMD_RESP_NACK to 0x06 with 3-byte payload per spec Rev 2.0.3`)
- `mcu-p3`: `e051111e68dd61896ed42c0961153b167b8bca41` (`fix(th): align TH MINIMC_CMD_NACK to 0x06 with 3-byte payload per Rev 2.0.3`)
- `test_harness`: `dccf2de1ec680cbf7456c76d70970b0338710e8e` (`test(cascade): align CAS-NEG-008 to 17-byte CMD_NACK (0x06) and add opcode alignment check`)
- `project-control`: `d5b1d46e556cab83eeaf12290dabef5634ca4365` (HEAD)

### 1.2 制品 SHA256 存证哈希列表
| 制品文件 | 字节大小 | SHA256 校验哈希 | 归档路径 |
| :--- | :--- | :--- | :--- |
| `fw_mc.bin` | 371,276 字节 | `ba5f738cdbd04b645a5f60d1cd29c1ff21e2ed9ee47479c711b2dd9ee1c92a4c` | `docs/evidence/issue_20261102_05/binaries/fw_mc.bin` |
| `fw_th.bin` | 71,844 字节 | `0fa6594ba6e77f421acdc1a3cd00365afa95d5d72c567f2d7072031dc5c5db7b` | `docs/evidence/issue_20261102_05/binaries/fw_th.bin` |
| `anchor.bin` | 140 字节 | `c43a60654231a034226c944cf518dbf35268cb88b881cd29f1b93f197852212b` | `docs/evidence/issue_20261102_05/binaries/anchor.bin` |
| `soc-ap` | 58,528 字节 | `a07562ea6681aadb6f74c5893ad9da3c45a0502cc4d138fd777d815e2fd53567` | `docs/evidence/issue_20261102_05/binaries/soc-ap` |

---

## 2. 现场物理硬件部署与探针识别

### 2.1 物理探针与硅片指纹 (基于 `test_harness/hil/tools/device_discovery.py`)
```text
================================================================================
       HIL 物理设备自动发现与指纹对账表 (Device Auto-Discovery)
================================================================================
probe-rs 引擎: /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe
--------------------------------------------------------------------------------
目标角色   | 芯片型号           | Flash    | MSP 栈顶       | 探针标识 (Probe ID)               
--------------------------------------------------------------------------------
[MC  ] | AT32F435VGT7   | 1024 KB  | 0x20060000   | 0483:3748:75003800120000334C41534E
       -> 唯一芯片 UID: 053023904C96C0000D819709
[TH  ] | AT32F423CCT7   | 256 KB   | 0x2000C000   | 0483:3748:                    
       -> 唯一芯片 UID: 053173C58023C000127C0707
================================================================================
```

### 2.2 物理刷入执行记录
1. **TH 从控 (AT32F423CCT7)**:
   - 固件刷入 (`fw_th.bin` @ `0x08004000`):
     ```bash
     /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download --chip AT32F423CCT7 --probe "0483:3748:" --binary-format bin --base-address 0x08004000 --verify fw_th.bin < /dev/null
     ```
     回显: `Finished in 5.40s` (Exit Code: 0, 校验成功)
   - 锚点刷入并软复位 (`anchor.bin` @ `0x0803F800`):
     ```bash
     /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download --chip AT32F423CCT7 --probe "0483:3748:" --binary-format bin --base-address 0x0803F800 --verify --reset anchor.bin < /dev/null
     ```
     回显: `Finished in 0.34s` (Exit Code: 0, 软复位完成)

2. **MC 主控 (AT32F435VGT7)**:
   - 固件刷入并软复位 (`fw_mc.bin` @ `0x08020000`):
     ```bash
     /mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download --chip AT32F435VGT7 --probe "0483:3748:75003800120000334C41534E" --binary-format bin --base-address 0x08020000 --verify --reset fw_mc.bin < /dev/null
     ```
     回显: `Finished in 29.72s` (Exit Code: 0, 校验成功，软复位完成)

---

## 3. 物理串口 (/dev/ttyUSB0) 报文验证与契约对齐

### 3.1 正常链路测试 (既有功能零回归)

| 用例编号 | 测试目标 | 发送 TX 帧 (Hex) | 接收 RX 帧 (Hex) | 往返时延 (RTT) | 判定结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `HIL-POS-01` | AP 单跳查询 MC 固件版本 | `55AA010205010400010000004D68` | `55AA020106020400010010000200020004030201321379A603000000EE6C` | 7.24 ms | **PASS** (返回 0x02 版本报告, Commit 0xA6791332) |
| `HIL-POS-02` | AP 双跳级联查询 TH 固件版本 | `55AA01030501040002000000B218` | `55AA030106020304020010000200020055AA77885AC0566307000000BE18` | 8.38 ms | **PASS** (返回 0x02 版本报告, Commit 0x6356C05A) |
| `HIL-POS-03` | AP 单跳向 MC 发送心跳 PING | `55AA01020503040003000400E803000020F2` | `55AA02010604040003000C00E8030000EE030000100008008B5F` | 7.49 ms | **PASS** (返回 0x04 PONG 响应) |
| `HIL-POS-04` | AP 双跳级联向 TH 发送心跳 PING | `55AA0103050304000400040078563412D8F8` | `55AA03010604030404000C00785634129056341200040000A6E3` | 8.21 ms | **PASS** (返回 0x04 PONG 响应) |

> **客观时间戳记录 (精确对齐 `raw_capture/hil_execution.json` 与 `uart_frames.log`)**:
> - `HIL-POS-01`: TX `2026-11-02 21:00:43.840+08:00` -> RX `2026-11-02 21:00:43.847+08:00` (RTT: 7,241 µs)
> - `HIL-POS-02`: TX `2026-11-02 21:00:43.897+08:00` -> RX `2026-11-02 21:00:43.906+08:00` (RTT: 8,378 µs)
> - `HIL-POS-03`: TX `2026-11-02 21:00:43.956+08:00` -> RX `2026-11-02 21:00:43.963+08:00` (RTT: 7,489 µs)
> - `HIL-POS-04`: TX `2026-11-02 21:00:44.013+08:00` -> RX `2026-11-02 21:00:44.022+08:00` (RTT: 8,213 µs)

---

### 3.2 否定应答契约对齐链路 (核心测试)

#### 【用例 HIL-NEG-01】AP 单跳向 MC 发送未实现命令 (`cmd_id=0x7E`, `seq=42`)
- **TX 时间**: `2026-11-02 21:00:44.072+08:00`
- **RX 时间**: `2026-11-02 21:00:44.078+08:00` (往返时延 RTT: 6,700 µs / 6.70 ms)
- **TX 帧 (14 字节)**: `55 AA 01 02 05 7E 04 00 2A 00 00 00 94 4F`
  - SOF: `55 AA`, SRC: `0x01` (AP), DST: `0x02` (MC), FLAGS: `0x05`, CMD: `0x7E`, HOP: `4`, ROUTE: `0`, SEQ: `0x002A` (42), PLEN: `0`, CRC16: `0x4F94`
- **RX 物理回包 (17 字节)**: `55 AA 02 01 06 06 04 00 2A 00 03 00 04 2A 00 86 19`
- **字段严格逐字节解码比对**:
  ```text
  [0..1]   SOF:          55 AA (合法)
  [2]      SRC_ID:       02 (MC)
  [3]      DST_ID:       01 (AP)
  [4]      FLAGS:        06 (IS_RESPONSE=1, WANTS_ACK=1)
  [5]      CMD_ID:       06 (CMD_NACK，完全对齐 Rev 2.0.3 §5.2，纠正历史 0x00 漂移)
  [6]      HOP_LIMIT:    04
  [7]      ROUTE_CTRL:   00
  [8..9]   SEQ:          2A 00 (42, 准确回显请求序列号)
  [10..11] PAYLOAD_LEN:  03 00 (3 字节，完全对齐 Rev 2.0.3 §5.2，纠正历史 2 字节漂移)
  [12]     error_code:   04 (MINIMC_ERR_UNKNOWN_CMD, 标识未实现命令)
  [13..14] expected_seq: 2A 00 (42, uint16 小端回显)
  [15..16] CRC16:        86 19 -> 0x1986
           (计算值: 0x1986, 物理校验: 100% MATCH)
  ```
- **判定**: **PASS**。

---

#### 【用例 HIL-NEG-02】AP 经 MC 路由向 TH 发送未实现命令 (`cmd_id=0x7E`, `seq=59`)
- **TX 时间**: `2026-11-02 21:00:44.129+08:00`
- **RX 时间**: `2026-11-02 21:00:44.135+08:00` (往返时延 RTT: 6,229 µs / 6.23 ms)
- **TX 帧 (14 字节)**: `55 AA 01 03 05 7E 04 00 3B 00 00 00 A4 C9`
  - SOF: `55 AA`, SRC: `0x01` (AP), DST: `0x03` (TH), FLAGS: `0x05`, CMD: `0x7E`, HOP: `4`, ROUTE: `0`, SEQ: `0x003B` (59), PLEN: `0`, CRC16: `0xC9A4`
- **RX 物理回包 (17 字节)**: `55 AA 03 01 06 06 03 04 3B 00 03 00 04 3B 00 7B 5D`
- **字段严格逐字节解码比对**:
  ```text
  [0..1]   SOF:          55 AA (合法)
  [2]      SRC_ID:       03 (TH)
  [3]      DST_ID:       01 (AP)
  [4]      FLAGS:        06 (IS_RESPONSE=1, WANTS_ACK=1)
  [5]      CMD_ID:       06 (CMD_NACK，完全对齐 Rev 2.0.3 §5.2)
  [6]      HOP_LIMIT:    03 (跳数经 MC 路由递减 1)
  [7]      ROUTE_CTRL:   04 (MC 透明路由状态标头)
  [8..9]   SEQ:          3B 00 (59, 准确回显请求序列号)
  [10..11] PAYLOAD_LEN:  03 00 (3 字节，完全对齐 Rev 2.0.3 §5.2)
  [12]     error_code:   04 (MINIMC_ERR_UNKNOWN_CMD)
  [13..14] expected_seq: 3B 00 (59, uint16 小端回显)
  [15..16] CRC16:        7B 5D -> 0x5D7B
           (计算值: 0x5D7B, 物理校验: 100% MATCH)
  ```
- **判定**: **PASS**。

---

## 4. SoC AP 宿主端 (`soc-ap`) 行为与错误上下文验证

### 4.1 正常查询验证
```bash
$ /home/sushaohua/soc-ap --port /dev/ttyUSB0 --target mc --cmd version --json
{"status":"SUCCESS","exit_code":0,"utc_time_ms":1793624444138,"monotonic_rtt_us":7826,"target":"MC","target_id":2,"cmd":"GET_VERSION","req_seq":0,"resp_seq":0,"version_info":{"proto_ver":"2.0","firmware_ver":"2.0","boot_id":"0x01020304","git_commit":"0xA6791332","capabilities":"0x00000003"}}

$ /home/sushaohua/soc-ap --port /dev/ttyUSB0 --target th --cmd version --json
{"status":"SUCCESS","exit_code":0,"utc_time_ms":1793624444149,"monotonic_rtt_us":8256,"target":"TH","target_id":3,"cmd":"GET_VERSION","req_seq":2,"resp_seq":2,"version_info":{"proto_ver":"2.0","firmware_ver":"2.0","boot_id":"0x8877AA55","git_commit":"0x6356C05A","capabilities":"0x00000007"}}
```
- 结果: 正常解析版本报告，退出码为 0。

### 4.2 NACK 否定应答捕获与结构化报错验证
在物理透明路由注入测试中，宿主程序捕获到板卡返回的真实 `CMD_NACK (0x06)` 报文：

1. **MC NACK 文本格式控制台回显**:
   ```text
   ERROR: Exit code 2 (Received CMD_NACK from target (error_code=0x04, expected_seq=0))
   ```
2. **MC NACK JSON 格式控制台回显**:
   ```json
   {"status":"CORRELATION_ERR","exit_code":2,"utc_time_ms":1793624444243,"target":"MC","cmd":"GET_VERSION","req_seq":0,"error_msg":"Received CMD_NACK from target (error_code=0x04, expected_seq=0)"}
   ```
3. **TH NACK 文本格式控制台回显**:
   ```text
   ERROR: Exit code 2 (Received CMD_NACK from target (error_code=0x04, expected_seq=2))
   ```
4. **TH NACK JSON 格式控制台回显**:
   ```json
   {"status":"CORRELATION_ERR","exit_code":2,"utc_time_ms":1793624444369,"target":"TH","cmd":"GET_VERSION","req_seq":2,"error_msg":"Received CMD_NACK from target (error_code=0x04, expected_seq=2)"}
   ```

- **行为判定**:
  - `soc-ap` 精准提取 3 字节载荷中的 `error_code` (0x04) 与 `expected_seq`；
  - 格式化输出结构化报错日志 `Received CMD_NACK from target (error_code=0x04, expected_seq=...)`；
  - 退出码明确为 `2` (`EXIT_CODE_CORRELATION_ERR`)，优雅退出，零崩溃。

---

## 5. 验收标准与交付物清单达成判定

| TASK-INT-01 验收标准 | 执行情况与物证路径 | 判定 |
| :--- | :--- | :--- |
| **标准 1**: 编译产出锁定 commit 的 `fw_mc.bin` 与 `fw_th.bin` 二进制并归档 | 编译产生 `fw_mc.bin` (SHA256: `ba5f738c...`) 与 `fw_th.bin` (SHA256: `0fa6594b...`)，已归档至 `docs/evidence/issue_20261102_05/binaries/` | **PASS** |
| **标准 2**: probe-rs 真实刷入 Twin 挂载的 AT32 MC 与 TH 物理板卡 | 双探针识别成功，分别刷写基地址 `0x08020000` (MC) 与 `0x08004000`/`0x0803F800` (TH) 并完成硬件软复位，详见 `raw_capture/probe_flash.log` | **PASS** |
| **标准 3**: `/dev/ttyUSB0` 抓包实测正常 `GET_VERSION`/`PING` | 实测 4 项正常用例全部通过，RTT 稳定在 7.24ms ~ 8.38ms，详见 `raw_capture/uart_frames.log` | **PASS** |
| **标准 4**: 注入非法请求触发真实 `NACK(0x06)` 响应闭环 | MC 与 TH 实测物理回发精确 17 字节 `CMD_NACK` 报文，载荷 3 字节，CRC 吻合；AP 宿主解析报错并优雅退出，详见 `raw_capture/uart_frames.log` | **PASS** |

---

## 6. 证据索引

- 二进制制品归档目录: `project-control/docs/evidence/issue_20261102_05/binaries/`
- 固件构建与哈希存证日志: `project-control/docs/evidence/issue_20261102_05/raw_capture/build_firmware.log`
- 探针刷写与复位存证日志: `project-control/docs/evidence/issue_20261102_05/raw_capture/probe_flash.log`
- 双向串口物理报文与字段对账日志: `project-control/docs/evidence/issue_20261102_05/raw_capture/uart_frames.log`
- 原始自动化联调执行数据: `project-control/docs/evidence/issue_20261102_05/raw_capture/hil_execution.json`
