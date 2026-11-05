---
task_id: TWIN-54
run_id: author_01
buildno: build-20261105-001
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
status: AWAITING_STEP5_FLASH_AUTHORIZATION
date: '2026-11-05T12:15:45+08:00'
---

# TWIN-54 轻量提测交接清单（`build-20261105-001`）

## 1. 组合版本（`buildno`）与六仓锁定基线

- **组合版本号 (`buildno`)**：`build-20261105-001`
- **锁定源码 Commit**：
  - `soc-ap` (`main`)：`79932746d225bb115010c5545ef3f7499482e137`（含 `TWIN-49`、`7c1f3509`、`TWIN-51`、`TWIN-52`、`TWIN-53` 全部修复）
  - `mcu-p3` (`feat/soc-debug`)：`016e1236af75f6f19282d6b000f4b1b68bd96cc3`（含 `TWIN-47` MC 与 `TWIN-48` TH 真机固件闭环）
  - `test_harness` (`main`)：`d14ed04321c6d4f5ddb35a8801604a8af53b5b60`
  - `project-control` (`main`)：`1a98934d236bf6ee9d33c92d87e6aa28afd14ea2`（`AUTO-07` 候选：`db20f47cab862b1068f45c08eaa9c25bbcfb316e`）
  - `boot/bootloadermc` (`soc_debug`)：`4fc171ea61912561949b9a0cfc1da8975e4c39ba`（**只读封锁**）
  - `boot/bootloaderth` (`soc_debug`)：`769fccbe52464ad7ceb856c5e89cb0d25abbbf87`（**只读封锁**）

---

## 2. Step 1～Step 4 及 Step 6 执行完成核对表

| 步骤 | 执行内容 | 客观结果与证据摘要 | 状态 |
| :--- | :--- | :--- | :--- |
| **Step 6** | VMware 旧 `/tmp/aisoc_twin_logs` 归档 | 已打包归档至 `192.168.77.134:/home/sushaohua/tmp/aisoc_legacy_archives/aisoc_twin_logs_pre_20261105-001_20261105T041015Z.tar.gz` (`sha256: 33038bdbd16c0d7efcbdce5f7db26b8590a38dd163ba41f0d9d86c10424b633d`) | **DONE** |
| **Step 1** | 宿主机独立检出与 VMware `soc-ap` 强制对齐 | 宿主机 `/tmp/aisoc_release_builds/build-20261105-001/src/{soc-ap,mcu-p3,test_harness}` 与 VMware `/home/sushaohua/tmp/ai_soc_project/soc-ap` 均 100% 对齐锁定 Commit，`git status --porcelain` 为空 | **DONE** |
| **Step 2** | VMware `third_party/build.sh --verify` | D-Bus、Fast CDR、Fast DDS 及 `optional.hpp` 两处 `engaged_` 判空守卫校验全部 `[OK]` | **DONE** |
| **Step 3** | 宿主机 MC/TH 干净交叉编译 + VMware & Docker `soc-ap` 干净构建与 CTest | MC (`Marlin_AT32.elf`, `fw_mc.bin`) 与 TH (`fw_th.elf`, `fw_th.bin`, `anchor.bin`) 编译通过且关键符号在列；VMware (GCC 15.2.0) 与 Docker (`qa-sandbox:20261029`, GCC 9.4.0) 5 大组件构建与 7 项 CTest 100% 通过 | **DONE** |
| **Step 4** | 封存 `build_manifest.yaml` 与 `SHA256SUMS` | 已生成 `build_manifest.yaml` 与 `SHA256SUMS`，且 `build/ui_gateway/ui-gateway` 与 `dist/vmware_twin/bin/ui-gateway` SHA-256 完全一致 (`41824294f0354a74315819ba60f46d133dc38c499ef5fe15a36213e9e53e0764`) | **DONE** |

---

## 3. Step 5 双板 MCU 固件烧录待确认清单（当前已暂停，等待用户烧录授权）

### 3.1 只读探针与芯片身份核验结果（`device_discovery.py`）
- **MC 主控板 (`AT32F435VGT7`)**：在线，`Probe ID = 0483:3748:75003800120000334C41534E`，Flash `1024 KB`，唯一芯片 UID `053023904C96C0000D819709`。
- **TH 工具头板 (`AT32F423CCT7`)**：在线，`Probe ID = 0483:3748:`，Flash `256 KB`，唯一芯片 UID `053173C58023C000127C0707`。

### 3.2 待烧录固件制品精确参数表

| 目标板卡 | 固件文件 | WSL2 宿主机路径 | Windows 暂存路径 | 字节大小 | SHA-256 摘要 | Flash 烧录基地址 | Bootloader 保护区间 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC (`AT32F435VGT7`)** | `fw_mc.bin` | `/tmp/aisoc_release_builds/build-20261105-001/artifacts/mc/fw_mc.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_mc.bin` | `383,284` B | `1e4bf2f50e7e4682444b8e8d35ce05c213427f86c95af5cffaf0081828241241` | **`0x08020000`** | `0x08000000~0x0801FFFF` (128KB 只读不触碰) |
| **TH (`AT32F423CCT7`)** | `fw_th.bin` | `/tmp/aisoc_release_builds/build-20261105-001/artifacts/th/fw_th.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_th.bin` | `77,244` B | `a2d4a50be058b7d06338d14945cb679f70386a94a4230d1254425b2ce5fe9afc` | **`0x08004000`** | `0x08000000~0x08003FFF` (16KB 只读不触碰) |
| **TH (`AT32F423CCT7`)** | `anchor.bin` | `/tmp/aisoc_release_builds/build-20261105-001/artifacts/th/anchor.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\anchor.bin` | `140` B | `094343d5a0450020c58bddd13807c0dc4eb86bb444c70f867463c34032df42ef` | **`0x0803F800`** | 尾部 Anchor 区 (`0x0803F800`) |

### 3.3 待授权执行的精确烧录命令
```bash
# 1. 烧录并校验 MC 应用固件 (AT32F435VGT7 @ 0x08020000)
/mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download \
  --probe "0483:3748:75003800120000334C41534E" --chip AT32F435VGT7 \
  --binary-format bin --base-address 0x08020000 --verify \
  'C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_mc.bin' < /dev/null

# 2. 烧录并校验 TH 应用固件 (AT32F423CCT7 @ 0x08004000) 与 Anchor (@ 0x0803F800)
/mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download \
  --probe "0483:3748:" --chip AT32F423CCT7 \
  --binary-format bin --base-address 0x08004000 --verify \
  'C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_th.bin' < /dev/null
/mnt/c/Users/EDY/tools/probe-rs/probe-rs.exe download \
  --probe "0483:3748:" --chip AT32F423CCT7 \
  --binary-format bin --base-address 0x0803F800 --verify \
  'C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\anchor.bin' < /dev/null
```

---

## 4. 后续 Step 7～Step 9 衔接说明

一旦用户授权执行上述 Step 5 烧录命令，将立即按序执行：
- **Step 7**：终止 VMware 残留 `hw_sampler.py` 与旧守护进程，释放 `/dev/ttyUSB0`、`COM12`、`COM13`；
- **Step 8**：先拉起 Windows `COM12` (`[MC-DBG] 115200`) 与 `COM13` (`[TH-DBG] 115200`) 只追加非阻塞原始日志采集，再执行 `probe-rs.exe reset` 捕获双板冷启动首帧；
- **Step 9**：以 `AISOC_AUTO_BUILD="0"`、`AISOC_MODE="hardware"`、`AISOC_UART_BAUD="921600"` 受控启动 VMware 4 个守护进程，并二次核验 `/proc/<pid>/exe` 的 SHA-256 与本清单封存值 100% 一致，交独立 QA 执行第一阶段全自动批次用例。
