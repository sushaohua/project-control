---
title: 物理 HIL 台架隔离环境搭建与单仓独立开发（mcu-p3 / soc-ap）快速验证指南
revision: 2
date: 2026-11-07
author: COORD (ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6)
status: active
---

# 物理 HIL 台架隔离环境搭建与单仓独立开发（`mcu-p3` / `soc-ap`）快速验证指南

本指南支持开发者在宿主机**任意路径**下**单独检出并开发 `mcu-p3`**（无需在宿主机拉取 `soc-ap`），或**单独检出并开发 `soc-ap`**（无需在宿主机拉取 `mcu-p3`）。
物理台架所需的配对运行环境统一收敛在 **VMware 虚拟机（`192.168.77.134`）的 `~/hil_bench/` 隔离目录**中，自动从 Git 服务器（`192.168.77.113:2222`）拉取构建，与宿主机开发路径完全解耦。

---

## 0. 物理台架拓扑与单仓解耦原则

### 0.1 拓扑结构（宿主机任意单仓开发 ⇄ VMware 隔离台架）

```text
+-----------------------------------------------------------------------------------+
| 宿主机 (WSL2 / Linux @ 192.168.77.113) —— 支持任意目录单仓独立开发                 |
|  - 场景 1 (只改固件):  /<任意路径>/mcu-p3/   (宿主机无需拉取 soc-ap / test_harness)|
|  - 场景 2 (只改上位机): /<任意路径>/soc-ap/   (宿主机无需拉取 mcu-p3 / test_harness)|
|  - Git 服务器:         ssh://git@192.168.77.113:2222/sushaohua/*.git              |
|  - 独立 Debug 串口 (Windows 侧只读监听):                                           |
|      * COM12 @ 115200 8N1  <--- [MC-DBG] (MC USART1 独立调试输出)                 |
|      * COM13 @ 115200 8N1  <--- [TH-DBG] (TH USART2 独立调试输出)                 |
+-----------------------------------------+-----------------------------------------+
                                          | SSH / SCP / RSYNC (ssh vmware / 192.168.77.134)
                                          v
+-----------------------------------------------------------------------------------+
| VMware 虚拟机 (Ubuntu 24.04 @ 192.168.77.134)                                     |
|  - 隔离台架根目录: /home/sushaohua/hil_bench/ (自动从 Git 服务器拉取维护)          |
|      ├── soc-ap/            (台架上位机服务运行副本，监听 http://127.0.0.1:8080)  |
|      ├── test_harness/      (台架串口 OTA 升级与协议帧直发工具副本)               |
|      └── firmware_staging/  (存放待刷写的 fw_th.bin / fw_mc.bin 及升级回执)       |
|  - 物理业务串口:   /dev/ttyUSB0 (921600 8N1)                                      |
+-----------------------------------------+-----------------------------------------+
                                          | UART (PA2/PA3, 921600 8N1)
                                          v
                         +--------------------------------+
                         | MC 运动控制板 (Node 0x02)       |
                         | AT32F435VGT7 (Boot + Marlin)   |
                         +----------------+---------------+
                                          | 板间级联 UART (USART6 <-> USART1, 921600 8N1)
                                          v
                         +--------------------------------+
                         | TH 工具头板 (Node 0x03)         |
                         | AT32F423CCT7 (Boot + TH App)   |
                         +--------------------------------+
```

### 0.2 三条核心隔离与防踩坑原则

1. **宿主机任意路径单仓开发**：
   - `mcu-p3` 仓内自带打包工具（`tools/pack_firmware.py`、`tools/version_tool.py`）和宿主机单测脚本，可在任意路径独立编译打包出 `fw_th.bin` 和 `fw_mc.bin`。
   - `soc-ap` 仓内自带 `third_party/` 与一键编译部署脚本（`tools/deploy_twin.sh`），可在任意路径独立开发。
2. **串口分时独占（关键）**：VMware 上的 `/dev/ttyUSB0` 同一时刻只能被一个进程打开：
   - **平时跑业务**：由 VMware 上 `~/hil_bench/soc-ap` 的 `forward_service_daemon` 独占打开 `/dev/ttyUSB0`。
   - **串口刷固件**：目前 `soc-ap` 的 `/api/v1/ota/trigger` 仅为状态门禁桩（未接通底层 D-Bus 串口发包），真实串口升级必须调用 `~/hil_bench/test_harness/hil/tools/hil_deploy_via_minimc_ota.py`。因此升级时遵循 **“先停 `soc-ap` ➔ 跑升级脚本刷包 ➔ 重新启动 `soc-ap`”**（第 2 节已封装为单条命令）。
3. **禁止调试探针直刷 App**：日常更新 MC/TH 应用固件，一律走 `/dev/ttyUSB0` 串口升级（或 MC U盘升级），不使用 `probe-rs` / `ST-Link` 直刷 App 分区。

---

## 1. 一次性初始化 VMware 隔离台架（`~/hil_bench`）与 Debug 串口

### 1.1 在 VMware 上一键搭建 `~/hil_bench`（从 Git 服务器自动拉取编译）

无论你在宿主机哪个目录工作，首次使用台架（或需要彻底重置台架环境）时，执行以下一条命令即可在 VMware 上从 Git 服务器拉取最新 `soc-ap` 与 `test_harness` 并完成编译：

```bash
ssh vmware 'set -e
mkdir -p ~/hil_bench/firmware_staging
cd ~/hil_bench
if [ ! -d soc-ap/.git ]; then
    git clone ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git
else
    git -C soc-ap fetch origin && git -C soc-ap checkout main && git -C soc-ap reset --hard origin/main
fi
if [ ! -d test_harness/.git ]; then
    git clone ssh://git@192.168.77.113:2222/sushaohua/test_harness.git
else
    git -C test_harness fetch origin && git -C test_harness checkout main && git -C test_harness reset --hard origin/main
fi
bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --build-only
'
```

### 1.2 在宿主机开启 MC / TH 独立 Debug 串口监听（按需在任意目录执行）

当需要观察 MC（`COM12`）或 TH（`COM13`）内部调试打印时，在宿主机另开终端运行（注意保留末尾 `< /dev/null` 防止 WSL2 调用 `powershell.exe` 阻塞）：

```bash
# 采集 15 秒 MC 独立 Debug 串口 (COM12 @ 115200) 与 TH 独立 Debug 串口 (COM13 @ 115200)
timeout 20s powershell.exe -NoProfile -NonInteractive -Command '
  $p12 = New-Object System.IO.Ports.SerialPort("COM12", 115200, "None", 8, "One");
  $p13 = New-Object System.IO.Ports.SerialPort("COM13", 115200, "None", 8, "One");
  $p12.ReadTimeout = 200; $p13.ReadTimeout = 200;
  $p12.Open(); $p13.Open();
  $sw = [Diagnostics.Stopwatch]::StartNew();
  while ($sw.Elapsed.TotalSeconds -lt 15) {
    try { $l = $p12.ReadExisting(); if ($l) { Write-Host -NoNewline "[MC] $l" } } catch {}
    try { $r = $p13.ReadExisting(); if ($r) { Write-Host -NoNewline "[TH] $r" } } catch {}
    Start-Sleep -Milliseconds 50
  }
  $p12.Close(); $p13.Close()
' < /dev/null
```

---

## 2. 场景一：单独开发 `mcu-p3` 工程时的部署与验证

> **前提**：你可以在宿主机**任意目录**下单独克隆或打开 `mcu-p3` 工程（无需在宿主机安装或拉取 `soc-ap`）：
> ```bash
> # 若尚未克隆，可在任意目录单独拉取 mcu-p3：
> git clone -b feat/soc-debug ssh://git@192.168.77.113:2222/sushaohua/mcu-p3.git
> cd mcu-p3
> ```
> 以下所有宿主机命令均假设你当前位于你的 **`mcu-p3` 根目录**下。

### 步骤 1：在 `mcu-p3` 根目录编译打包并传到 VMware 台架暂存区

- **若修改了 TH 固件（`color-engine-mcu`）**：
  ```bash
  # 1. (可选) 跑 TH 宿主机单测自检
  sh color-engine-mcu/tests/run_tests.sh

  # 2. 编译 TH 固件并自动追加 128B ATSG 签名尾块 -> 生成 color-engine-mcu/io_toggle/build/fw_th.bin
  make -C color-engine-mcu/io_toggle pack && \
  scp color-engine-mcu/io_toggle/build/fw_th.bin vmware:~/hil_bench/firmware_staging/fw_th.bin.part && \
  ssh vmware "mv ~/hil_bench/firmware_staging/fw_th.bin.part ~/hil_bench/firmware_staging/fw_th.bin"
  ```

- **若修改了 MC 固件（`motion-controller-mcu`）**：
  ```bash
  # 1. (可选) 跑 MC 宿主机单测自检
  sh motion-controller-mcu/tests/run_tests.sh

  # 2. 编译 MC 固件并自动追加 128B ATSG 签名尾块 -> 生成 motion-controller-mcu/build/fw_mc.bin
  make -C motion-controller-mcu pack && \
  scp motion-controller-mcu/build/fw_mc.bin vmware:~/hil_bench/firmware_staging/fw_mc.bin.part && \
  ssh vmware "mv ~/hil_bench/firmware_staging/fw_mc.bin.part ~/hil_bench/firmware_staging/fw_mc.bin"
  ```

### 步骤 2：確保 VMware 台架上的 `soc-ap` 服务为服务器最新稳定版

如果你希望自动从 Git 服务器拉取最新稳定版 `soc-ap` 并编译（避免 VMware 上残留其他人改过的 `soc-ap`），执行：

```bash
ssh vmware 'set -e
cd ~/hil_bench
git -C soc-ap fetch origin && git -C soc-ap checkout main && git -C soc-ap reset --hard origin/main
git -C test_harness fetch origin && git -C test_harness checkout main && git -C test_harness reset --hard origin/main
bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --build-only
'
```
*(注：如果 VMware 上的 `soc-ap` 已经是最新干净版，日常连续改测 `mcu-p3` 时可跳过此步以节省编译时间。)*

### 步骤 3：一键串口升级（自动停 `soc-ap` ➔ 512B 分块刷写 ➔ 自动重拉起 `soc-ap`）

根据你本次改的是 TH、MC 还是两块板都改了，**三选一**执行：

- **选项 3A：只升级 TH（约 15~25 秒，151 个 512B 分块，经 MC App 级联路由）**
  ```bash
  ssh vmware 'set -e
  bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --stop
  python3 ~/hil_bench/test_harness/hil/tools/hil_deploy_via_minimc_ota.py \
    --port /dev/ttyUSB0 --baud 921600 --chunk-size 512 \
    --th-pkg ~/hil_bench/firmware_staging/fw_th.bin \
    --receipt-out ~/hil_bench/firmware_staging/last_ota_receipt.json
  cat ~/hil_bench/firmware_staging/last_ota_receipt.json
  AISOC_AUTO_BUILD=0 bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB0 --baud 921600 --port 8080
  '
  ```

- **选项 3B：只升级 MC（约 20~60 秒，749 个 512B 分块，直连 MC Bootloader）**
  ```bash
  ssh vmware 'set -e
  bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --stop
  python3 ~/hil_bench/test_harness/hil/tools/hil_deploy_via_minimc_ota.py \
    --port /dev/ttyUSB0 --baud 921600 --chunk-size 512 \
    --mc-pkg ~/hil_bench/firmware_staging/fw_mc.bin \
    --receipt-out ~/hil_bench/firmware_staging/last_ota_receipt.json
  cat ~/hil_bench/firmware_staging/last_ota_receipt.json
  AISOC_AUTO_BUILD=0 bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB0 --baud 921600 --port 8080
  '
  ```

- **选项 3C：双板同时升级（严格遵循先 TH 后 MC 顺序）**
  ```bash
  ssh vmware 'set -e
  bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --stop
  python3 ~/hil_bench/test_harness/hil/tools/hil_deploy_via_minimc_ota.py \
    --port /dev/ttyUSB0 --baud 921600 --chunk-size 512 \
    --th-pkg ~/hil_bench/firmware_staging/fw_th.bin \
    --mc-pkg ~/hil_bench/firmware_staging/fw_mc.bin \
    --receipt-out ~/hil_bench/firmware_staging/last_ota_receipt.json
  cat ~/hil_bench/firmware_staging/last_ota_receipt.json
  AISOC_AUTO_BUILD=0 bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB0 --baud 921600 --port 8080
  '
  ```

### 步骤 4：调用命令验证 MC 和 TH 的功能

升级完成且 `soc-ap` 自动拉起后，可通过以下两种方式验证：

#### 方式 A：通过 VMware 上 `soc-ap` 的 HTTP 接口验证（适合验证已接入 `soc-ap` 的功能）

在宿主机直接用 `curl http://192.168.77.134:8080/...`（或在 `ssh vmware` 内用 `127.0.0.1:8080`）：

| 验证目标 | 对应底层协议帧与目标节点 | 宿主机一行验证命令 |
| :--- | :--- | :--- |
| **1. 查双板在线、版本与温度快照** | `0x01->0x02` & `0x14->0x15` (`MC` + `TH`) | `curl -s http://192.168.77.134:8080/api/v1/state \| python3 -m json.tool` |
| **2. 触发双板即时温度采样** | `0x14 -> 0x15` (`MC 0x02` + `TH 0x03`) | `curl -s -X POST http://192.168.77.134:8080/api/v1/temperature/sample` |
| **3. 验证 MC 热床设温 (`0°C` 安全验证)** | `0x10 CMD_SET_TEMP` ➔ **MC (`0x02`)** | `curl -s -X POST http://192.168.77.134:8080/api/v1/temperature/set -H "Content-Type: application/json" -d '{"bed_c":0,"nozzle_c":0}'` |
| **4. 验证 TH 喷头设温 (`0°C` 级联验证)** | `0x10 CMD_SET_TEMP` ➔ **TH (`0x03`)** | `curl -s -X POST http://192.168.77.134:8080/api/v1/temperature/set -H "Content-Type: application/json" -d '{"nozzle_c":0,"bed_c":0}'` |
| **5. 验证 TH 多色换料槽位控制** | `0x19 CMD_FILAMENT_CTRL` ➔ **TH (`0x03`)** | `curl -s -X POST http://192.168.77.134:8080/api/v1/filament/slots -H "Content-Type: application/json" -d '{"slot_id":1,"action":"SELECT"}'` |
| **6. 验证 MC 运动归零 / 点动** | `0x11` / `0x12` ➔ **MC (`0x02`)** | `curl -s -X POST http://192.168.77.134:8080/api/v1/motion/jog -H "Content-Type: application/json" -d '{"axis":"X","distance_mm":0.0,"feedrate":1500}'` |
| **7. 验证 MC/TH G-code 透传执行** | `0x1C CMD_GCODE_EXECUTE` ➔ **MC/TH** | `curl -s -X POST http://192.168.77.134:8080/api/v1/gcode/execute -H "Content-Type: application/json" -d '{"gcode":"M114"}'` |
| **8. 验证急停触发与解除** | `0x17 CMD_EMERGENCY_STOP` ➔ **MC (`0x02`)** | `curl -s -X POST http://192.168.77.134:8080/api/v1/emergency/stop` （解除用 `/api/v1/emergency/clear`） |

#### 方式 B：一行命令直发任意 `MiniMCProto v2.0` 原始帧（适合验证 `soc-ap` 尚未封装的新指令）

若你在 `mcu-p3` 新增了 `soc-ap` 尚未支持的 `cmd_id` 或载荷字段，执行以下命令停掉 `soc-ap` 并直接向 MC (`dst=0x02`) 或 TH (`dst=0x03`) 发送自定义帧：

```bash
ssh vmware '
bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --stop >/dev/null
python3 - << "PY"
import sys
sys.path.insert(0, "/home/sushaohua/hil_bench/test_harness/hil/tools")
import hil_deploy_via_minimc_ota as ota

with ota.SerialOtaTarget("/dev/ttyUSB0", 921600) as ser:
    # 可将 cmd_id=0x01, payload=b"" 替换为你新增的指令码与二进制载荷
    for name, dst in [("MC (0x02)", 0x02), ("TH (0x03)", 0x03)]:
        req = ota.build_frame(dst=dst, seq=1, cmd_id=0x01, payload=b"")
        resp = ser.exchange_frame(req)
        print(f"[{name}] rsp_cmd=0x{resp.cmd_id:02X}, payload_len={len(resp.payload)}, hex={resp.payload.hex()}")
PY
'
```

---

## 3. 场景二：单独开发 `soc-ap` 工程时的环境检查与闭环自测

> **前提**：你可以在宿主机**任意目录**下单独克隆或打开 `soc-ap` 工程（无需在宿主机拉取 `mcu-p3`）：
> ```bash
> # 若尚未克隆，可在任意目录单独拉取 soc-ap：
> git clone ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git
> cd soc-ap
> ```
> 以下所有宿主机命令均假设你当前位于你的 **`soc-ap` 根目录**下。

### 步骤 1：台架下位机健康预检（3 秒确认真实 MC 和 TH 均在线且处于 App 模式）

在把你的 `soc-ap` 改动部署到台架之前，先运行这条预检命令，确认物理台架上的 **MC (`0x02`)** 和 **TH (`0x03`)** 均正常在线并能回包：

```bash
ssh vmware '
bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --stop >/dev/null 2>&1 || true
python3 - << "PY"
import sys
sys.path.insert(0, "/home/sushaohua/hil_bench/test_harness/hil/tools")
import hil_deploy_via_minimc_ota as ota

with ota.SerialOtaTarget("/dev/ttyUSB0", 921600) as ser:
    for name, dst in [("MC", 0x02), ("TH", 0x03)]:
        resp = ser.exchange_frame(ota.build_frame(dst=dst, seq=1, cmd_id=0x01, payload=b""))
        ver = ota.parse_version_report(resp)
        in_boot = bool(ver.capability_flags & 0x80000000)
        assert not in_boot, f"{name} 当前停留在 Bootloader 模式 (cap=0x{ver.capability_flags:08X})，请先执行 2.3 节恢复 App 固件！"
        print(f"[PRECHECK PASS] {name}(0x{dst:02X}) ONLINE in APP mode: v{ver.fw_major}.{ver.fw_minor}, commit=0x{ver.git_commit_short:08X}, boot_id=0x{ver.boot_id:08X}")
PY
'
```
- **判定标准**：输出两行 `[PRECHECK PASS] MC(0x02) ONLINE...` 和 `[PRECHECK PASS] TH(0x03) ONLINE...`，代表下位机硬件与串口链路 100% 正常，可放心测试 `soc-ap`。

### 步骤 2：将当前目录下的 `soc-ap` 部署到 VMware 并启动

在你的宿主机 **`soc-ap` 根目录**下，根据需要二选一执行：

- **方式 A（本地修改未提交代码，直接从当前 `soc-ap` 目录同步到 VMware 编译启动）**：
  ```bash
  rsync -av --delete \
    --exclude='.git/' --exclude='build/' --exclude='dist/' --exclude='third_party/build/' --exclude='third_party/install/' \
    ./ vmware:~/hil_bench/soc-ap/ && \
  ssh vmware "bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB0 --baud 921600 --port 8080"
  ```

- **方式 B（已 `git push` 到 Git 服务器，让 VMware 直接从服务器拉取指定分支/提交编译启动）**：
  ```bash
  # 默认拉取 origin/main；若为特定分支可将 main 替换为你的分支名
  ssh vmware 'cd ~/hil_bench/soc-ap && \
    git fetch origin && git checkout main && git reset --hard origin/main && \
    bash tools/deploy_twin.sh --mode hardware --uart /dev/ttyUSB0 --baud 921600 --port 8080'
  ```

### 步骤 3：端到端收发自测（验证 `soc-ap` 发出的命令 MC 和 TH 都能真实返回）

`deploy_twin.sh` 启动成功后，运行以下一条自测命令，一次性验证 **4 个守护进程存活 + MC/TH 均在线 + 发往 MC 和 TH 的控制命令均收到真实硬件 ACK 返回**：

```bash
ssh vmware 'set -e
echo "=== [1/4] 检查 4 大守护进程与 HTTP 探针状态 ==="
bash ~/hil_bench/soc-ap/tools/deploy_twin.sh --status

echo "=== [2/4] 触发双节点 (MC+TH) 即时温度采样并核对在线状态 ==="
curl -s -X POST http://127.0.0.1:8080/api/v1/temperature/sample && echo ""
sleep 0.5
curl -s http://127.0.0.1:8080/api/v1/state | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(\"System State:\", d.get(\"system_status_desc\"), \"| gen_id:\", d.get(\"generation_id\"))
print(\"MC Status:   \", d.get(\"mcu_versions\", {}).get(\"mc\"))
print(\"TH Status:   \", d.get(\"mcu_versions\", {}).get(\"th\"))
"

echo "=== [3/4] 验证发往 MC(0x02) 与 TH(0x03) 的双端设温指令真实 ACK 闭环 ==="
curl -s -X POST http://127.0.0.1:8080/api/v1/temperature/set \
  -H "Content-Type: application/json" -d "{\"bed_c\":0,\"nozzle_c\":0}" && echo ""

echo "=== [4/4] 验证发往 TH(0x03) 的换料槽位控制指令真实 ACK 闭环 ==="
curl -s -X POST http://127.0.0.1:8080/api/v1/filament/slots \
  -H "Content-Type: application/json" -d "{\"slot_id\":1,\"action\":\"SELECT\"}" && echo ""
'
```

### 步骤 4：故障定位与日志查看速查

如果在自测 `soc-ap` 时发现接口报错或超时，直接查看 VMware 上 `/tmp/aisoc_twin_logs/` 的分层日志：

```bash
# 查看串口收发与超时上下文 (target_node, sequence_id, elapsed_ms, error_code)
ssh vmware "tail -n 50 /tmp/aisoc_twin_logs/forward_service.log"

# 查看设备状态机、DDS 温度快照更新与 D-Bus 准入日志
ssh vmware "tail -n 50 /tmp/aisoc_twin_logs/device_manager.log"

# 查看 HTTP/SSE 网关请求处理日志
ssh vmware "tail -n 50 /tmp/aisoc_twin_logs/ui_gateway.log"
```
