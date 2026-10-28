# AP–MC–TH 物理台架工程联合调试标准作业程序 (Joint Debug SOP)

> **文档标识**: `SOP-JOINT-DEBUG-20261028`  
> **归档路径**: `project-control/docs/operations/ap_mc_th_joint_debug.md`  
> **状态**: 冻结发布 (Frozen for Execution)  
> **制定角色**: `INTEGRATOR` / 架构与质量评审  
> **生效任务**: `CR-08` 产出，`CR-09` 执行，`CR-10` 独立验收  
> **配套候选清单**: [`project-control/docs/releases/ap_mc_th_readonly_candidate.yaml`](../releases/ap_mc_th_readonly_candidate.yaml)  

---

## 1. 物理环境与安全门禁 (Safety Gates)

### 1.1 硬件连接拓扑
```text
┌─────────────────────────┐          USB 直通          ┌───────────────────────────────────┐
│ VMware Ubuntu (SoC AP)  │ ◄────────────────────────► │ 2 号口 CH340 (/dev/ttyUSB0)       │
│ ./soc-ap                │      115200 8N1 无流控     │ 连接 MC: USART2 (PA2-TX / PA3-RX) │
└─────────────────────────┘                            └─────────────────┬─────────────────┘
                                                                         │
                                                                   USART6 板间级联
                                                                  921600 8N1 无流控
                                                              MC: PA4-TX / PA5-RX
                                                                         │
                                                       ┌─────────────────┴─────────────────┐
                                                       │ TH (Toolhead 工具头从控板)        │
                                                       │ USART1 (PB6-TX / PB7-RX)          │
                                                       └───────────────────────────────────┘
```

### 1.2 强制遵守的六大工程门禁
- **HW-G1 (物理插拔确认)**：AI 仅生成 SOP 指引，台架操作员必须确认连线牢固后方可启动。
- **HW-G2 (烧录基地址强核验)**：
  - **MC 主控 (AT32F435VGT7)**：刷写地址必须为 `0x08020000`（保留 `0x08000000~0x0801FFFF` 的 128KB Bootloader），绝对禁止向 `0x08000000` 盲刷导致变砖！
  - **TH 从控 (AT32F423CCT7)**：刷写地址必须为 `0x08004000`（保留 `0x08000000~0x08003FFF` 的 16KB Bootloader），绝对禁止向 `0x08000000` 盲刷！
- **HW-G3 (异常断电)**：若出现板卡过热、异响或串口无休止报错，立即切断电源。
- **HW-G5 (零虚拟化在环铁律)**：**严禁使用 PTY 伪终端、Mock 或回环软件代替真实物理硬件**。联调验收必须提供真实的串口双向原始 Hex 数据流（Raw Hex TX/RX），若有效响应帧数为 0 必须一票否决！
- **HW-G6 (端到端原生协议一致性)**：MC 必须线速透明中继转发，严禁在 MC 内部解包篡改或伪造 TH 应答。

---

## 2. 联调前准备工作 (Pre-Flight Checks)

### 2.1 候选制品与 SHA-256 核验
台架操作员在执行前，先在宿主机上核验二进制文件的完整性：
```bash
# 1. 核验 AP 二进制
sha256sum soc-ap/build/host/bin/soc-ap
# 预期: 1e0e0263c90c658e8026e1d5a5dd51349b411831575d4be2b7aec42fbd62d6e1

# 2. 核验 MC 固件
sha256sum mcu-p3/motion-controller-mcu/build/fw_mc.bin
# 预期: 74ad2bd0861cebf7f6964ca81f83cf41ac850e8adfa21379073f51e218d78f99

# 3. 核验 TH 固件
sha256sum mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin
# 预期: 5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d
```

### 2.2 硬件探针识别与设备映射
运行设备自发现脚本，确认两支 ST-Link 探针已正确识别且芯片型号对齐：
```bash
python3 test_harness/hil/tools/device_discovery.py
```
*检查点*：输出中 MC 必须对应 `AT32F435VGT7`，TH 必须对应 `AT32F423CCT7`。

---

## 3. 阶段一：物理固件烧录与复位 (Firmware Deployment)

> **注意**：烧录路径统一采用非侵入式 SWD 硬件烧录，避开 U 盘升级路径（CR-07 维持解耦）。

### 3.1 烧录 TH 从控固件 (AT32F423)
```bash
probe-rs download mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin \
  --format bin --base-address 0x08004000 \
  --chip AT32F423CCT7 --probe <TH_PROBE_ID>

probe-rs reset --chip AT32F423CCT7 --probe <TH_PROBE_ID>
```

### 3.2 烧录 MC 主控固件 (AT32F435)
```bash
probe-rs download mcu-p3/motion-controller-mcu/build/fw_mc.bin \
  --format bin --base-address 0x08020000 \
  --chip AT32F435VGT7 --probe <MC_PROBE_ID>

probe-rs reset --chip AT32F435VGT7 --probe <MC_PROBE_ID>
```

---

## 4. 阶段二：单跳 AP ↔ MC 连通性与时延测试 (Single-Hop)

在 VMware Ubuntu 宿主机上，通过物理串口 `/dev/ttyUSB0` 测试与 MC 的直连通信：

### 4.1 MC 固件版本查询 (`GET_VERSION`, `target=mc`)
```bash
./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target mc --cmd version --json
```
- **预期输出**：
  ```json
  {"status":"SUCCESS","exit_code":0,"target":"MC","target_id":2,"cmd":"GET_VERSION","version_info":{"proto_ver":"2.0","firmware_ver":"1.0","git_commit":"0xA6791332"}}
  ```
- **判定标准**：退出码为 `0`，`proto_ver == 2.0`，`monotonic_rtt_us` 通常处于 $500 \sim 3000\,\mu s$ 范围内。

### 4.2 MC 心跳与往返时延度量 (`PING`, `target=mc`)
```bash
./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target mc --cmd ping --json
```
- **预期输出**：
  ```json
  {"status":"SUCCESS","exit_code":0,"target":"MC","target_id":2,"cmd":"PING","ping_info":{"rx_fifo_free_units":8}}
  ```
- **判定标准**：退出码为 `0`，成功测得 RTT 时间戳。

---

## 5. 阶段三：双跳 AP → MC → TH 级联穿透与 RTT 度量 (Two-Hop Cascade)

测试 AP 穿透 MC 原生中继路由、直达 TH 并收到回包的核心链路：

### 5.1 TH 从控版本级联查询 (`GET_VERSION`, `target=th`)
```bash
./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target th --cmd version --json
```
- **预期输出**：
  ```json
  {"status":"SUCCESS","exit_code":0,"target":"TH","target_id":3,"cmd":"GET_VERSION","version_info":{"proto_ver":"2.0","firmware_ver":"1.0","boot_id":"0x8877AA55","git_commit":"0x6356C05A"}}
  ```
- **判定标准**：退出码为 `0`，`target_id == 3`，`boot_id == 0x8877AA55`（证明是真实 TH 自报而非 MC 伪造）。

### 5.2 TH 心跳探活与全链路 RTT 度量 (`PING`, `target=th`)
```bash
./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target th --cmd ping --json
```
- **预期输出**：
  ```json
  {"status":"SUCCESS","exit_code":0,"target":"TH","target_id":3,"cmd":"PING","monotonic_rtt_us":2350}
  ```
- **核心指标记录**：记录 `monotonic_rtt_us`（全链路物理往返时延），重复测试 10 次，计算平均 RTT 与抖动范围。

---

## 6. 阶段四：负例防御与异常故障注入 (Robustness & Fault Injection)

利用基于 probe-rs 的寄存器故障注入工具验证通信自愈能力：

### 6.1 TH 掉线与超时自愈 (CAS-NEG-001)
1. **切断 TH 物理通信**：
   ```bash
   python3 test_harness/hil/tools/probe_fault_injector.py disable --target TH --uart USART1
   ```
2. **AP 发送查询并预期超时**：
   ```bash
   ./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target th --cmd version --timeout-ms 300 --json
   ```
   *预期*：退出码为 `1` (`EXIT_TIMEOUT`)，错误信息提示目标 `0x03` 超时无应答。
3. **恢复 TH 通信并验证自愈**：
   ```bash
   python3 test_harness/hil/tools/probe_fault_injector.py enable --target TH --uart USART1
   ./soc-ap/build/host/bin/soc-ap --port /dev/ttyUSB0 --target th --cmd version --json
   ```
   *预期*：退出码恢复为 `0` (`SUCCESS`)。

---

## 7. 阶段五：数据归档与交付要求

在 CR-09 联合调试完成时，必须将以下原始数据打包归档至 `docs/evidence/cascade_recovery/CR-09/runs/<run-id>/`：
1. **控制台原始输出**（包含 10 次往返时延测量的 Raw JSON）；
2. **串口 Raw Hex 对账数据**（AP TX 帧、MC 中继转发帧、TH 回包帧逐字节十六进制对比）；
3. **硬件探针自发现日志与烧录控制台回显**；
4. **填报完成的联合调试总结报告**。
