---
task_id: TWIN-54
run_id: author_01
buildno: build-20261105-002
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
status: READY_FOR_STEP5_FLASH_AFTER_TWIN56_QA
date: '2026-11-05T13:06:00+08:00'
---

# TWIN-54 轻量提测交接清单（`build-20261105-002`，含 `TWIN-56` 修复）

## 1. 组合版本（`buildno`）与六仓锁定基线

- **组合版本号 (`buildno`)**：`build-20261105-002`
- **锁定源码 Commit**：
  - `soc-ap` (`main`)：`79932746d225bb115010c5545ef3f7499482e137`（含 `TWIN-49`、`7c1f3509`、`TWIN-51`、`TWIN-52`、`TWIN-53` 全部修复）
  - `mcu-p3` (`feat/soc-debug`)：`75f69aa374f543008c706634088d2b4bd10cf97c`（含 `TWIN-47` MC、`TWIN-48` TH 及 `TWIN-56` 16-bit `seq` 日志截断与 `s_mc_th_seq=0x0100U` 修复）
  - `test_harness` (`main`)：`d14ed04321c6d4f5ddb35a8801604a8af53b5b60`
  - `project-control` (`main`)：`f4e45fb5cdd1d7c1fee405d9a720f19e200b126f`（含 `AUTO-07` 审阅通过提交）
  - `boot/bootloadermc` (`soc_debug`)：`4fc171ea61912561949b9a0cfc1da8975e4c39ba`（**只读封锁**）
  - `boot/bootloaderth` (`soc_debug`)：`769fccbe52464ad7ceb856c5e89cb0d25abbbf87`（**只读封锁**）

---

## 2. Step 1～Step 4 及 Step 6 执行完成核对表

| 步骤 | 执行内容 | 客观结果与证据摘要 | 状态 |
| :--- | :--- | :--- | :--- |
| **Step 6** | VMware 旧 `/tmp/aisoc_twin_logs` 归档 | 已打包归档至 `192.168.77.134:/home/sushaohua/tmp/aisoc_legacy_archives/aisoc_twin_logs_pre_20261105-001_20261105T041015Z.tar.gz` (`sha256: 33038bdbd16c0d7efcbdce5f7db26b8590a38dd163ba41f0d9d86c10424b633d`) | **DONE** |
| **Step 1** | 宿主机独立检出与 VMware `soc-ap` 强制对齐 | 宿主机与 VMware `/home/sushaohua/tmp/ai_soc_project/soc-ap` 均 100% 对齐锁定 Commit，`git status --porcelain` 为空 | **DONE** |
| **Step 2** | VMware `third_party/build.sh --verify` | D-Bus、Fast CDR、Fast DDS 及 `optional.hpp` 两处 `engaged_` 判空守卫校验全部 `[OK]` | **DONE** |
| **Step 3** | 宿主机 MC/TH 干净交叉编译 (`TWIN-56`) + VMware & Docker `soc-ap` 干净构建与 CTest | MC (`Marlin_AT32.elf`, `fw_mc.bin`) 与 TH (`fw_th.elf`, `fw_th.bin`, `anchor.bin`) 在 `75f69aa374f543008c706634088d2b4bd10cf97c` 下重编通过；VMware (GCC 15.2.0) 与 Docker (`qa-sandbox:20261029`, GCC 9.4.0) 5 大组件构建与 7 项 CTest 100% 通过 | **DONE** |
| **Step 4** | 封存 `build_manifest.yaml` 与 `SHA256SUMS` (`build-20261105-002`) | 已更新 `build_manifest.yaml` 与 `SHA256SUMS`，且 `build/ui_gateway/ui-gateway` 与 `dist/vmware_twin/bin/ui-gateway` SHA-256 完全一致 (`41824294f0354a74315819ba60f46d133dc38c499ef5fe15a36213e9e53e0764`) | **DONE** |

---

## 3. Step 5 双板 MCU 固件烧录清单（用户已授权 A2，待 `TWIN-56` QA 收口后立即烧录）

### 3.1 只读探针与芯片身份核验结果（`device_discovery.py`）
- **MC 主控板 (`AT32F435VGT7`)**：在线，`Probe ID = 0483:3748:75003800120000334C41534E`，Flash `1024 KB`，唯一芯片 UID `053023904C96C0000D819709`。
- **TH 工具头板 (`AT32F423CCT7`)**：在线，`Probe ID = 0483:3748:`，Flash `256 KB`，唯一芯片 UID `053173C58023C000127C0707`。

### 3.2 待烧录固件制品精确参数表（`build-20261105-002`）

| 目标板卡 | 固件文件 | WSL2 宿主机路径 | Windows 暂存路径 | 字节大小 | SHA-256 摘要 | Flash 烧录基地址 | Bootloader 保护区间 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC (`AT32F435VGT7`)** | `fw_mc.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/mc/fw_mc.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_mc.bin` | `383,220` B | `94b495ebe474ac9fcba322156d917f271ef138964e2ca21001ab02eb5a3a0dba` | **`0x08020000`** | `0x08000000~0x0801FFFF` (128KB 只读不触碰) |
| **TH (`AT32F423CCT7`)** | `fw_th.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/th/fw_th.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_th.bin` | `77,248` B | `9dc9eb8e05eb53a16471541a896210b42f7bae635913f97e950906f0b89fe11d` | **`0x08004000`** | `0x08000000~0x08003FFF` (16KB 只读不触碰) |
| **TH (`AT32F423CCT7`)** | `anchor.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/th/anchor.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\anchor.bin` | `140` B | `7564309c8fe74ba59a7f836cc877ae9308521a3bc96df3afddc7f6b151440cd7` | **`0x0803F800`** | 尾部 Anchor 区 (`0x0803F800`) |

### 3.3 精确烧录命令
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
