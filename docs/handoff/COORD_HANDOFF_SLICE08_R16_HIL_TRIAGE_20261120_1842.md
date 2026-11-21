# AI SoC COORD 会话交接文档：`SLICE-08 (r16)` HIL 缺陷分诊与 `r17` 待批起点

- **交接时间**：`2026-11-20 18:42 +0800`
- **交接前角色**：`COORD`（工作区：`/home/sushaohua/workspace/ai_soc_project`）
- **下一任角色**：`COORD`
- **当前所处阶段**：**`SLICE-08 (r16)` 首轮真机分诊已完成，正停在 `Human Gate #1` 等待用户拍板**（严禁未获用户明确批准前改动任何工程源码或向 `ENG-*` 派单）

---

## 1. 一句话交接摘要

`SLICE-08 revision: 3`（`r16`：`printer-soc@8f26e979`）已通过四阶软件门禁并在 `192.168.1.101` 上机验证了 `r15` 修复（4 守护进程正常自启、`panel_restarts: 0`、DDS 域 `198`、字体与 32bpp 显示零崩溃）；随后的实板交互与串口诊断实证出 **3 项问题（`HIL-DEF-04` 触摸选错 `event1`、`HIL-DEF-05` Klipper 报错弹窗遮罩与按钮/版本 Subject 缺失、`HIL-BLK-01` / `MCU-UART-01` MC `USART2` 失联）**。相关根因、证据链、Diff Budget 与 `r17` 方案对比已写入单一真相源实施方案 **`v1.16`**，当前严格停在 **Human Gate #1** 待用户回答 3 个确认项。

---

## 2. 权威入口文档（接手必读）

1. **实施方案单一真相源（已原地更新至 `v1.16`）**：
   - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（重点阅读 **第 4 节 `## 4.`（第 718–774 行）** 及修订表第 23 行）
2. **垂直切片定义与准出账本**：
   - `project-control/slices/SLICE-08.yaml`（当前 `revision: 3`，对应 `r16`）
   - `project-control/slices/ledger.md`（第 24 行记录 `SLICE-08 r16 SW-Verified`）
3. **`r16` 真机与软件物证目录**：
   - 真机诊断日志与 `/dev/fb0` 截图：`project-control/docs/evidence/SLICE-08/hil_r16/`
   - `r16` 四阶门禁与产出产物（含 `rootfs.ubi`、`aml_upgrade_package.img`、`release-manifest.json`）：`project-control/docs/evidence/SLICE-08/run_20261120_170900_r16/docker_qa/artifacts/`
4. **编排与角色铁律**：
   - 根工作区总纲：`AGENTS.md`（注意：**根仓 Git 命令统一用 `bash tools/workspace_git.sh ...`**）
   - `COORD` / `BOOT` 边界与切片编排：`project-control/.agents/rules/delivery_and_coord_gate.md`、`project-control/.agents/rules/bootloader_role_boundaries.md`、`.agents/skills/slice-batch-orchestrator/SKILL.md`

---

## 3. 各仓库精确基线与当前工作区现场（`2026-11-20 18:42 +0800` 实测）

> 所有业务/固件/测试仓均**完全干净**，仅 `project-control` 与根 `docs/` 有本地文档/物证状态。

| 仓库路径 | 分支 | 当前 `HEAD` | 远端对齐 | 本地工作区状态与注意事项 |
| :--- | :--- | :--- | :--- | :--- |
| `.`（通过 `tools/workspace_git.sh` 管理） | `main` | `bc1ea44` | `origin/main` | 既有 `M docs/README.md` 与 `?? docs/AI_TEAM_WORKFLOW_WHITEPAPER_20261117_165528.md`、`?? docs/HANDOFF_20261117_171334.md`，与本任务无关，保持不动 |
| `project-control` | `main` | `019512ea8e01a16d0339e2ff88c3bcad6cb91f2c` | `origin/main` | 1. `M docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（`v1.16`）<br>2. `?? docs/handoff/COORD_HANDOFF_SLICE08_R16_HIL_TRIAGE_20261120_1842.md`（本交接文档）<br>3. `?? docs/evidence/SLICE-08/hil_r16/`（`r16` 实板取证，**保留**）<br>4. `?? docs/planning/printer_performance_implementationplan_20261120_171756.md`（无关既有文件，**严禁改动**） |
| `printer-soc` | `main` | `8f26e97902849fd6d90162e9136f08dd3a52658d` | `origin/main` | 干净（`r16` `SW-Verified` 基线） |
| `test_harness` | `main` | `fb1409be7ad5586c701df586553d7f5b67bc2b43` | `origin/main` | 干净（`SLICE-08` `--policy integrity-only-hil` 在内） |
| `mcu-p3` | `feat/soc-debug` | `7b623d9a4fff7cf460b53318b71d0b816635b733` | `origin/feat/soc-debug` | 干净（当前在方案 B 下仍冻结，方案 A 需用户明示解冻） |
| `boot/bootloadermc` | `soc_debug` | `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` | `origin/soc_debug` | 干净（**锁 `soc_debug`，禁写 `main`，本批暂不动 Bootloader**） |
| `boot/bootloaderth` | `soc_debug` | `1a0351363cf7b9cbc0aa6919b4afc6be61561152` | `origin/soc_debug` | 干净（**锁 `soc_debug`，禁写 `main`**） |
| `agents` | `main` | `30ecc6586a861c1543a97804cfe0600bb4778efb` | `origin/main` | 干净 |

---

## 4. `r16` 实板硬件现状与已查清的 3 项根因速查

### 4.1 硬件平台瞬时状态（`root@192.168.1.101`）
- 板端已装 `r16` 根文件系统；`S90printer-soc` 相关服务当前处于**停止状态**（`/dev/fb0` 与 `/dev/ttyS1` 空闲）。
- 历史实测状态机：`17:45` 冷上电时 `MC`（`85171363` / `7b623d9a`）与 `TH`（`3292647499` / `7b623d9a`）均在 `921600` 在线；`18:05:40` 下发 `0x1D(1)` 复位 `MC` 后，`18:06` 与 `18:13` 串口探测均超时（`rx` 停留在 `3768`），因此当前 **`MC` 对 `/dev/ttyS1` 处于无应答状态**（如需重测冷上电，须冷断电重启双板）。
- 若需再次获取 `SLICE-05` 归档版本 `7b623d9a` 的双 MCU 打包固件（`fw_mc.bin` `384,240B` / `fw_th.bin` `76,992B`），可直接从受管工作区文件 `project-control/docs/evidence/SLICE-05/hil_raw_hex.log` 中的 `0x21` 线帧负载重组取得（切勿跨越工作区边界访问外部历史会话目录）。

### 4.2 三项缺陷与源码定位速查（勿重复排查）

1. **`HIL-DEF-04` (`BLOCKER`) — 触摸无反应**
   - **现象/日志**：`project-control/docs/evidence/SLICE-08/hil_r16/helix_console_diag.log`（L20–L35）与 `mc_reset_and_ui_diag.log` 实证 `helix-screen` 打开了 `/dev/input/event1`（`ir_keypad1`, `abs=false`），跳过 `/dev/input/event0`（`Goodix Capacitive TouchScreen`，`MT_X=0..719, MT_Y=0..1279`），且板端 `input0..2` 在不同上电周期存在序号漂移风险。
   - **代码**：
     - `printer-soc/services/helixscreen/platform/c308l/live-profile.json:24` 硬编码 `"touch_device": "/dev/input/event1"`；
     - `printer-soc/tools/c308l_services.py:172-177` 与 `printer-soc/boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel:25-27` 仅在目标 `settings.json` 不存在时拷贝配置，导致 `/data/printer-soc/helix/config/settings.json` 长期固化失效路径，绕过 `DisplayBackendFbdev::auto_detect_touch_device()`。
     - 可参照同目录 `printer-soc/services/helixscreen/platform/c308l/demo.py:87-96,122,127` 的 Goodix 识别方式；修复时应把 `"touch_device"` 设回 `""`，并在两个启动脚本/入口前对既有 `settings.json` 做失效/非触摸节点清洗。

2. **`HIL-DEF-05` (`BLOCKER`) — “界面乱（不是下位机离线）”与启动 Subject 警告**
   - **现象/帧图**：`project-control/docs/evidence/SLICE-08/hil_r16/fb0_frame0.png` 与 `fb0_frame0_rot90ccw.png`。内核 `sdk/c308l/platform/kernel/aml-5.15/common_drivers/drivers/framebuffer/osd_fb.c:173-213` 原生支持 32bpp `BGRA/RGBA/BGRX/RGBX`，板端 `fb0`（`32bpp`, `stride=2880`, `720x1280`）显示硬件正常。按 `rotate: 270`（`+90° CCW`）转正的 `fb0_frame0_rot90ccw.png` 主界面本身清晰（`Home` 在左、`Tips` 在右上），但被深色全屏模糊遮罩和黄框弹窗 `"Printer Error"` / `"Klipper has entered an error state..."`（`[Firmware Restart]` / `[Restart Klipper]` / `[Dismiss]`）覆盖，加上触摸失效无法关闭。
   - **代码**：
     - `printer-soc/services/helixscreen/src/printer/printer_network_state.cpp:48` 初始 `klippy_state=KlippyState::SHUTDOWN`；`printer-soc/services/helixscreen/src/application/application.cpp:2022-2027` 在 `snap.mc.is_boot_mode` 设为 `ERROR`、`snap.estop_latched` 设为 `SHUTDOWN`；
     - `printer-soc/services/helixscreen/src/ui/ui_emergency_stop.cpp:270-303` (`EmergencyStopOverlay::klippy_state_observer_`) 据此弹出 `klipper_recovery_dialog.xml` 模糊全屏恢复框；
     - `printer-soc/services/helixscreen/ui_xml/advanced_panel.xml:266-279` 遗漏 `aisoc_mode` 隐藏绑定（仍渲染两个 Klipper 重启按钮）；
     - 启动期因 `AboutSettingsOverlay` 懒初始化，日志出现 `No subject was found with name "aisoc_ap_version"` / `"aisoc_mc_version"` / `"aisoc_th_version"`（`helix_console_diag.log` L440–L442）。
   - **兼容边界**：修改必须受 `#ifdef HELIX_ENABLE_AISOC` 保护，且绝不能篡改 `AC-01..AC-09`、`test_helix_screen_integration.py`、`AISOC_VERSION_FILE` 与下位机真实状态（`MC Bootloader` / `E-Stop Latched` / `DM Offline`）。

3. **`HIL-BLK-01` / `MCU-UART-01` (`MAJOR`) — MC 跨 AP 热重启与 `0x1D(1)` 后串口失联**
   - **日志**：`project-control/docs/evidence/SLICE-08/hil_r16/post_reboot_uart_check.log`（`17:50` AP `reboot` 后 `rx=0, irq 37=0`）、`mc_reset_and_ui_diag.log`（`18:04` 用户仅重启 MC 后 `bootloadermc 0x4FC171EA` 正常回包 `rx 0->3768`；`18:05:40` 下发 `0x1D(1)` 收到 ACK 并执行 `boot_uart_ota.c:936` `NVIC_SystemReset()` 后再无应答）。
   - **代码**：
     - `sdk/c308l/.../c3_c308l_aw419.dts:935-943` 仅在 Linux pinctrl 后拉高 UART 引脚；
     - `mcu-p3/motion-controller-mcu/project/src/wk_usart.c:257` 将 `PA3` (`USART2_RX`) 配为 `GPIO_PULL_NONE`（对照 `bootloadermc` 配 `GPIO_PULL_UP`）；
     - `wk_usart.c:269-270`、`memu_gui.c:450`、`at32f435_437_int.c:354` **从未清 `USART2` `ROERR/FERR/NERR/BFF`**（对照 `boot_uart_ota.c:807` 及 `wk_usart.c:360,411` `USART6`）；AT32F435 上未清 `ROERR` 会锁死 DMA；
     - `eeprom_at24cxx.c:776,804,810` 在 `minimc_proto.c:3225` 切 `921600` 前执行 `200ms+500ms` 延时期间，`USART2` 已开启 `115200` + `IDLE_INT` + 循环 DMA。
   - **本地工具链已核实**：宿主已安装 `/usr/bin/arm-none-eabi-gcc`、`make`、`cmake`、`ninja`；`mcu-p3/motion-controller-mcu/Makefile` 提供 `make pack`（产出 `fw_mc.bin`）及宿主单测入口 `tests/run_tests.sh`。

---

## 5. 当前正在等待用户拍板的 3 个问题（Human Gate #1）

上一轮对话末尾已向用户提出、尚未收到回复的 3 项决策：
1. 是否**批准执行 `S08-HIL-FIX-02`**（`printer-soc` 触摸纠偏、屏蔽 AISoC 下 Klipper 报错弹窗与残留按钮、消除版本 Subject 警告）？
2. MC 串口问题选择：
   - **方案 A（推荐）**：同时**解冻 `mcu-p3`**（仅限 `feat/soc-debug`，暂不动 `boot/bootloadermc`），将 **`S08-MCU-FIX-01`** 纳入 `r17` 由 `ENG-MCU` 修复 `USART2` 并重打 `fw_mc.bin`；
   - **方案 B（保守）**：继续保持 **`mcu-p3@7b623d9` 冻结 0 修改**，仅做 `S08-HIL-FIX-02`，后续 `r17` HIL 时保持“双板与 AP 同步冷断电上电”。
3. 屏幕方向确认：结合 `fb0_frame0_rot90ccw.png`（`Home` 在左、`Tips` 在右上），实物 LCD 上是**正立横向（维持 `rotate: 270`）**，还是**上下倒置 `180°`（须改为 `rotate: 90`）**？

---

## 6. 下一任 Agent 接手执行步骤（Runbook）

1. **接手首轮响应检查**：
   - 若用户新消息**未包含**上述 3 项批复，先保持所有工程仓只读，向用户简明确认这 3 项决策；
   - 若用户已明确批复（`方案 A/B` + `rotate: 270/90`），立即按下列步骤推进：
2. **锁定计划与切片清单（`project-control/` 内）**：
   - 原地更新 `helix_screen_mc_th_integration_implementationplan_20261118_144741.md` 修订表（新增 `v1.17` 实名记录，如 `AI (<具体模型实体>) - COORD`，标注已获 `Human Gate #1` 批准的方案与旋转方向）；
   - 更新 `project-control/slices/SLICE-08.yaml` 至 **`revision: 4`**：
     - `ENG-AP`（`printer-soc@main`）：扩充精确 `allowed_paths` 覆盖 `services/helixscreen/platform/c308l/live-profile.json`、`tools/c308l_services.py`、`boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel`、`services/helixscreen/src/application/application.cpp`、`services/helixscreen/src/ui/ui_emergency_stop.cpp`、`services/helixscreen/src/ui/ui_settings_about.cpp`、`services/helixscreen/ui_xml/advanced_panel.xml`、`services/helixscreen/platform/c308l/tests/test_tools.py`、`services/helixscreen/tests/unit/aisoc/test_aisoc_p0.cpp`（视需要校验 `diff_budget` 是否涉及 stock 上游受保护文件）；
     - 若用户选 **方案 A**：在 `SLICE-08.yaml` 中新增 `ENG-MCU` 子任务（`repo: "mcu-p3"`, `branch: "feat/soc-debug"`），限定 `allowed_paths` 至 `motion-controller-mcu/project/src/wk_usart.c`、`motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c`、`motion-controller-mcu/project/src/at32f435_437_int.c`、`motion-controller-mcu/project/src/minimc_proto.c`、`motion-controller-mcu/project/src/main.c`、`motion-controller-mcu/tests/test_mc_ota_and_relay.c`，并在 `integration_cmd` / `qa_commands` 接入 `tests/run_tests.sh` 及（视 Docker 沙箱工具链支持情况核对）`make pack` 校验；**仍严禁写入 `boot/bootloadermc` 与 `boot/bootloaderth`**。
3. **有界派单与单仓提交**：
   - 使用 `project-control/tools/workflow/run_slice_batch.py`（或按角色边界唤醒 `ENG-AP` / 方案 A 下 `ENG-MCU`）实施改动并自测；严禁 `COORD` 直接改 `printer-soc/` 或 `mcu-p3/` 业务代码；
   - 严控全中文注释/文档字符串、自研函数 $\le 50$ 行 / 入参 $\le 4$ 个、零内存假状态垫片。
4. **四阶软件门禁 -> Human Gate #2 -> `r17` 真机 HIL**：
   - 各仓生成单逻辑 commit 并推齐后，跑通 `fast_gate.py (<3s)` -> `integration_cmd` -> `qa_runner.py` 独立 Docker 只读沙箱构建回归 -> `codex_review.py`（`slice_gate.py`）独立 Codex 双轴冷审（`0 BLOCKER / 0 MINOR`），更新 `ledger.md` 至最新 `SW-Verified`；
   - **停在 `Human Gate #2`** 申请用户批准上板后，才可在 `192.168.1.101` 刷写与复测（遵守零 `probe-rs`/SWD、零加热 `heating_pwm_pct=0`、零电机运动、不动 `/data/boot_backup.img` 与 `/etc/printer-soc/fw_signing_pub.pem` 红线）。
