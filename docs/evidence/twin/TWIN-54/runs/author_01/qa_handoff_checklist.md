---
task_id: TWIN-54
run_id: author_01
buildno: build-20261105-002
requirement_id: REQ-20261105-001
demand_id: DEM-20261105-005
status: COMPLETED_STEP1_TO_STEP9_HANDOFF_READY
date: '2026-11-05T14:00:00+08:00'
---

# TWIN-54 轻量提测交接清单（`build-20261105-002`，Step 1～Step 9 全部完成）

## 1. 组合版本（`buildno`）与六仓锁定基线

- **组合版本号 (`buildno`)**：`build-20261105-002`
- **锁定源码 Commit**：
  - `soc-ap` (`main`)：`79932746d225bb115010c5545ef3f7499482e137`（含 `TWIN-49`、`7c1f3509`、`TWIN-51`、`TWIN-52`、`TWIN-53` 全部修复）
  - `mcu-p3` (`feat/soc-debug`)：`891a8bb252814c83992a49b01fbe11ba83b92a1f`（含 `TWIN-47` MC、`TWIN-48` TH 及 `TWIN-56` 16-bit `seq` 日志截断与 `s_mc_th_seq=0x0100U` 修复）
  - `test_harness` (`main`)：`d14ed04321c6d4f5ddb35a8801604a8af53b5b60`
  - `project-control` (`main`)：`f4e45fb5cdd1d7c1fee405d9a720f19e200b126f`（含 `AUTO-07` 审阅通过提交）
  - `boot/bootloadermc` (`soc_debug`)：`4fc171ea61912561949b9a0cfc1da8975e4c39ba`（**只读封锁**）
  - `boot/bootloaderth` (`soc_debug`)：`769fccbe52464ad7ceb856c5e89cb0d25abbbf87`（**只读封锁**）

---

## 2. Step 1～Step 9 全步骤执行完成核对表

| 步骤 | 执行内容 | 客观结果与证据摘要 | 状态 |
| :--- | :--- | :--- | :--- |
| **Step 6** | VMware 旧 `/tmp/aisoc_twin_logs` 归档 | 已打包归档至 `192.168.77.134:/home/sushaohua/tmp/aisoc_legacy_archives/aisoc_twin_logs_pre_20261105-001_20261105T041015Z.tar.gz` (`sha256: 33038bdbd16c0d7efcbdce5f7db26b8590a38dd163ba41f0d9d86c10424b633d`) | **DONE** |
| **Step 1** | 宿主机独立检出与 VMware `soc-ap` 强制对齐 | 宿主机与 VMware `/home/sushaohua/tmp/ai_soc_project/soc-ap` 均 100% 对齐锁定 Commit，`git status --porcelain` 为空 | **DONE** |
| **Step 2** | VMware `third_party/build.sh --verify` | D-Bus、Fast CDR、Fast DDS 及 `optional.hpp` 两处 `engaged_` 判空守卫校验全部 `[OK]` | **DONE** |
| **Step 3** | 宿主机 MC/TH 干净交叉编译 (`TWIN-56`) + VMware & Docker `soc-ap` 干净构建与 CTest | MC (`Marlin_AT32.elf`, `fw_mc.bin`) 与 TH (`fw_th.elf`, `fw_th.bin`, `anchor.bin`) 重编通过；VMware (GCC 15.2.0) 与 Docker (`qa-sandbox:20261029`, GCC 9.4.0) 5 大组件构建与 7 项 CTest 100% 通过 | **DONE** |
| **Step 4** | 封存 `build_manifest.yaml` 与 `SHA256SUMS` (`build-20261105-002`) | 已封存 `build_manifest.yaml` 与 `SHA256SUMS`，且 `build/ui_gateway/ui-gateway` 与 `dist/vmware_twin/bin/ui-gateway` SHA-256 完全一致 (`41824294f0354a74315819ba60f46d133dc38c499ef5fe15a36213e9e53e0764`) | **DONE** |
| **Step 5** | 双板 MCU 固件受控烧录与探针校验 | MC (`AT32F435VGT7` `@ 0x08020000`, `29.69s`) 与 TH (`AT32F423CCT7` `@ 0x08004000` `5.74s` + `@ 0x0803F800` `0.34s`) `--verify` 全部一次通过（证据：`step5_flash_verify.log`） | **DONE** |
| **Step 7** | 遗留进程与串口清场（禁止 `hw_sampler.py` 竞争串口） | 停止 VMware 旧四守护进程并清理 `hw_sampler.py`，验证 `/dev/ttyUSB0` 零占用；无损释放 `COM12`/`COM13` 句柄并确认双串口空闲（证据：`step7_cleanup.log`） | **DONE** |
| **Step 8** | Debug 串口双通道捕获先行挂载 + 双板冷启动复位 | 挂载后台常驻只写追加捕获 `dual_dbg_logger.ps1` (`COM12`/`COM13 @ 115200`)，随后执行 `probe-rs.exe reset`，完整捕获双板 Bootloader 与 App 冷启动输出（证据：`step8_preboot_debug.log`） | **DONE** |
| **Step 9** | 受控拉起 VMware 四守护进程并核验 `/proc/<pid>/exe` | 使用 `AISOC_AUTO_BUILD="0"`、`AISOC_MODE="hardware"`、`AISOC_UART_BAUD="921600"` 拉起四守护进程，核对运行中 `/proc/<pid>/exe` 的 SHA-256 与 `build_manifest.yaml` 100% 一致（证据：`step9_daemon_startup.log`） | **DONE** |

---

## 3. Step 5 双板 MCU 固件烧录与 Step 9 运行中进程哈希实测表

### 3.1 已烧录固件制品精确参数表（`build-20261105-002`）

| 目标板卡 | 固件文件 | WSL2 宿主机路径 | Windows 暂存路径 | 字节大小 | SHA-256 摘要 | Flash 烧录基地址 | `--verify` 结果 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MC (`AT32F435VGT7`)** | `fw_mc.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/mc/fw_mc.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_mc.bin` | `383,220` B | `94b495ebe474ac9fcba322156d917f271ef138964e2ca21001ab02eb5a3a0dba` | **`0x08020000`** | **PASSED (`29.69s`)** |
| **TH (`AT32F423CCT7`)** | `fw_th.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/th/fw_th.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\fw_th.bin` | `77,248` B | `9dc9eb8e05eb53a16471541a896210b42f7bae635913f97e950906f0b89fe11d` | **`0x08004000`** | **PASSED (`5.74s`)** |
| **TH (`AT32F423CCT7`)** | `anchor.bin` | `/tmp/aisoc_release_builds/build-20261105-002/artifacts/th/anchor.bin` | `C:\Users\EDY\AppData\Local\Temp\aisoc_build_20261105_001\anchor.bin` | `140` B | `7564309c8fe74ba59a7f836cc877ae9308521a3bc96df3afddc7f6b151440cd7` | **`0x0803F800`** | **PASSED (`0.34s`)** |

### 3.2 Step 9 VMware 运行中四守护进程 `/proc/<pid>/exe` 哈希核对表

| 守护进程 | PID 文件 | 运行中 `/proc/<pid>/exe` 实测 SHA-256 | 与 `build_manifest.yaml` 一致性 |
| :--- | :--- | :--- | :--- |
| `dbus-daemon` | `dbus.pid` | `73d24dd0759d6b3f5a959f73d452b2b29013d1880d04229f434e98b74d00278a` | **100% 匹配** |
| `forward_service_daemon` | `forward.pid` | `c13a44dc21a18064a5dd84cf35fe9d39b44d693c352899fbfafb90b80e67c259` | **100% 匹配** |
| `device_manager_daemon` | `device_manager.pid` | `2a0313efcdef73e578a7498e8c2f9f7d0d83d4ea5918cff0ef9e88ceb4b9cc85` | **100% 匹配** |
| `ui-gateway` | `ui_gateway.pid` | `41824294f0354a74315819ba60f46d133dc38c499ef5fe15a36213e9e53e0764` | **100% 匹配** |
