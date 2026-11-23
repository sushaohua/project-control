# SLICE-09 (`UX-01` / `S09-UX01`)：`r18b` 现状实板触屏走查与五类卡点归因报告

- **任务标识**：`SLICE-09` / `S09-UX01`（刷入新候选前 `SLICE-08 r18b` 现状实板基线取证）
- **执行角色**：`INTEGRATOR`（全业务仓只读 `max_files = 0`）
- **执行时间**：`2026-11-23 09:45 ~ 10:06 +08:00`
- **目标台架**：`root@192.168.1.101`（`C308L-AW419` `Linux 5.15.137 armv7l` + `MC AT32F435` + `TH AT32F423`）
- **依据规范**：[helix_p0_experience_implementationplan_20261121_190357.md](../../planning/helix_p0_experience_implementationplan_20261121_190357.md)（`§1.5`、`§2.4.2 S09-UX01`）与 [SLICE-09.yaml](../../../slices/SLICE-09.yaml)
- **证据目录**：`project-control/docs/evidence/SLICE-09/ux01_r18b_walkthrough/`

---

## 1. 安全红线与基线保护核验总表

| 安全与基线核验项 | 走查前实测值 | 走查后实测值 | 判定 | 原始证据文件 |
| --- | --- | --- | :---: | --- |
| **业务代码零改动 (`max_files=0`)** | 0 改动 | 0 改动（仅写入本走查证据目录） | **PASS** | `UX01_WALKTHROUGH_REPORT.md` |
| **目标温度零加热 & 占空比核验说明** | `GetDeviceState`: `heating=false`（目标温度未设）；物理 PWM 占空比 `[UNVERIFIED]` | `TriggerQuery(1/2)` + `GetDeviceState`: `state="IDLE", heating=false, printing=false`；`UX-01` 为非侵入触屏走查（未停服独占 `/dev/ttyS1` 采集 `0x15` 原始 PWM 字节），`heating_pwm_pct` 物理占空比显式标为 **`[UNVERIFIED]`**（留待实板 HIL 阶段抓 `0x15 heater_duty_percent` 原始帧验证） | **目标温度 `heating=false` PASS / 占空比 `[UNVERIFIED]`** | `01_baseline_registration.log`, `08_post_walkthrough_health_and_safety_audit.log` |
| **零电机运动 & 零 `probe-rs` 调用** | 零运动、`probe_rs_used=false` | 零运动、宿主 `probe_rs_processes=0` | **PASS** | `08_post_walkthrough_health_and_safety_audit.log` |
| **零预置包 & 零真实刷写** | `/run/printer-soc/firmware/` 为空 (`0` 文件)；`MC boot_id=1775181012`、`TH boot_id=1462640722` | `/run/printer-soc/firmware/` 保持为空 (`0` 文件)；双板 `boot_id` 恒为 `1775181012` / `1462640722` | **PASS** | `chk06_scan_and_logs.log`, `08_post_walkthrough_health_and_safety_audit.log` |
| **`/data/boot_backup.img` SHA-256** | `59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86` | `59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86` | **PASS** | `01_baseline_registration.log`, `08_post_walkthrough_health_and_safety_audit.log` |
| **验签公钥只读保护** | `/etc/printer-soc/fw_signing_pub.pem` (`-r--r--r--`, `178 B`) | `/etc/printer-soc/fw_signing_pub.pem` (`-r--r--r--`, `178 B`) | **PASS** | `01_baseline_registration.log`, `08_post_walkthrough_health_and_safety_audit.log` |
| **屏幕背光原值恢复 (`aml-bl`)** | `brightness=204`, `actual_brightness=204` (`80%`, `max=255`) | 拖动实测 `204 -> 104 (41%) -> 204` 后精确恢复 `brightness=204` (`80%`) | **PASS** | `chk02_backlight_adjustment.log`, `chk02_01`~`chk02_03` |
| **持久化语言基线与退回首页** | 只读模板 `"language": "en"`；进场持久化曾被人工切为 `"zh"`（见 §2.2 披露） | 退回英文首页（`08_final_home_restored_en.png`），`settings.json`（及 `/var/lib/helixscreen/settings.json.backup`）保留 `"language": "en"` 且不含 `c308l_default_lang_migrated` | **PASS** | `08_final_home_restored_en.png`, `08_post_walkthrough_health_and_safety_audit.log` |
| **生产守护进程健康无重启** | `phase="running"`, `panel_restarts=0`, PIDs `1199/1200/1201/1216/1226` | `phase="running"`, `panel_restarts=0`, PIDs `1199/1200/1201/1216/1226` 恒定不变 | **PASS** | `01_baseline_registration.log`, `08_post_walkthrough_health_and_safety_audit.log` |

---

## 2. 走查前环境与基线登记（§1.5.1）

### 2.1 实板固件、服务与硬件输入/显示管线登记
1. **AP 候选身份（`/etc/printer-soc/version.json`）**：
   - `product_version`: `"0.1.0-skeleton"`，`candidate_id`: `"0.1.0-skeleton+6f28023f"`，`git_sha`: `"6f28023f"`（对应 `SLICE-08 r18b` 基线 `printer-soc@6f28023f7f1b774d181fc4ba59d3c378f260bfc1`），`profile`: `"c308l-production"`，`build_id`: `"20261121T082130Z"`，`mcu_proto`: `"2.0"`。
2. **MC / TH 在线版本与运行模式（`org.aisoc.DeviceInterface.GetVersionInfo`）**：
   - `MC`: `status="ONLINE"`, `proto_version="2.0"`, `firmware_version="2.0"`, `git_commit="0xA64BFFBF"`, `boot_id=1775181012`, `capability_flags=3`（`Bit31=0`，处于 `App` 模式）。
   - `TH`: `status="ONLINE"`, `proto_version="2.0"`, `firmware_version="2.0"`, `git_commit="0xA64BFFBF"`, `boot_id=1462640722`, `capability_flags=7`（`Bit31=0`，处于 `App` 模式）。
   - 物理串口状态（`org.aisoc.ForwardInterface.GetPortStatus`）：`is_open=true`, `port_path="/dev/ttyS1"`, 走查前 `tx=268502, rx=268502`，走查后 `tx=270623, rx=270623`（100% 零丢包）。
3. **`helix-screen` 运行参数与 `aisoc_mode` 实际值**：
   - 进程：`PID=1226`，命令行 `/usr/share/printer-soc/helixscreen/bin/helix-screen`（无 `--test` 或 Mock 参数，`enable_gateway=false`）。
   - 关键环境变量：`HELIX_DATA_DIR=/usr/share/printer-soc/helixscreen`、`HELIX_CONFIG_DIR=/data/printer-soc/helix/config`、`AISOC_VERSION_FILE=/etc/printer-soc/version.json`、`AISOC_DDS_DOMAIN=198`、`FASTDDS_BUILTIN_TRANSPORTS=SHM`、`DBUS_SESSION_BUS_ADDRESS=unix:path=/tmp/dbus-2BwqLXPZEQ,...`。
   - 物理句柄绑定：`fd 4 -> /dev/fb0`（`720x1280` `BGRA8888`，`stride=2880`，`display.rotate=270` 旋转后逻辑分辨率 `1280x720`）；`fd 5 -> /dev/input/event0`（`Goodix Capacitive TouchScreen`，`ABS_X/ABS_MT_POSITION_X: 0..719`，`ABS_Y/ABS_MT_POSITION_Y: 0..1279`）。
   - **`aisoc_mode` 实际值**：**`1`**（编译启用 `HELIX_ENABLE_AISOC`，由 `xml_registration.cpp:359` 初始化 `s_aisoc_mode_subject = 1`；实机 `About` 页已显示受 `aisoc_mode` 门控的三端版本与本地升级行，且隐藏了非 AISoC 网络/导航项）。
4. **固定扫描目录初始状态（`/run/printer-soc/firmware/`）**：
   - 实测 `ls -la /run/printer-soc/firmware/` 为**系统默认空目录**（仅 `.` 与 `..`，**无任何预置 `fw_mc.bin` 或 `fw_th.bin`**）。
   - 服务运行日志实际落盘路径：板端 `services.json` 配置 `"runtime_dir": "/run/printer-soc"`，真实日志位于 **`/run/printer-soc/forward.log`** 与 **`/run/printer-soc/panel.log`**（实板上 `/var/log/printer-soc` 目录不存在）。

### 2.2 进场现场状态如实披露与双视角取证说明
- **只读默认模板核验**：`/usr/share/printer-soc/helixscreen/config/settings.json` 中 `"language": "en"`，证实 `SLICE-08 r18b` 出厂默认语言确为英文 `"en"`。
- **进场持久化状态发现**：首次只读连接台架未注入任何触控前，抓拍初始帧缓冲 [00_initial_untouched_fb0.png](00_initial_untouched_fb0.png) 并备份 `/data/printer-soc/helix/config/settings.json`（[01b_initial_settings_json_snapshot.json](01b_initial_settings_json_snapshot.json)），发现此前人工在台架现场体验时（对应 `/run/printer-soc/forward.log` 中 `timestamp_unix_ms=6979438` 的历史扫描记录 `task_id="760000001"`），已在触屏上手动将语言切为 `"zh"`、亮度调为 `80% (204)`，且界面停留在左侧第二栏「控制」页。
- **严谨处置流程**：
  1. 先通过真实触屏保全抓拍了 `"zh"` 状态下的首页、一级设置、关于页及 `OtaLocalOverlay` 实况（[02a_pre_zh_home.png](02a_pre_zh_home.png) ~ [02h_pre_zh_ota_bottom.png](02h_pre_zh_ota_bottom.png)），获取中文模式下一级入口缺失、旧“验签”误导文案及局部字库缺字（`订阅真` 渲染为 `□□□`）的第一手真机证据；
  2. 随后通过真实触屏点击 `设置 -> 显示与声音 -> 语言 -> English`（[02j_display_sound_zh.png](02j_display_sound_zh.png) ~ [02l_lang_dropdown_top.png](02l_lang_dropdown_top.png)）切回 `r18b` 出厂默认配置 `"language": "en"` 并点击首页图标回到英文默认基线首页（[03_home_en_baseline.png](03_home_en_baseline.png)）；
  3. 从 `r18b` 默认英文首页出发，严格按 §1.5.2 顺序逐步执行 `CHK-01` ~ `CHK-06` 全量走查，并在结束后退回英文首页，保留 `/data/printer-soc/helix/config/settings.json`（及 `/var/lib/helixscreen/settings.json.backup`）为 `"language": "en"`（不含 `c308l_default_lang_migrated`），供后续阶段 H1 真实检验默认中文一次性迁移逻辑。

---

## 3. 逐步实机走查记录与五类标准归因（`CHK-01` ~ `CHK-06`）

> 本次全部交互均通过 [ux01_touch_fb_tool.py](ux01_touch_fb_tool.py) 按 `270°` 旋转逆映射公式（`raw_x = 719 - ui_y`, `raw_y = ui_x`）向 `/dev/input/event0` 写入真实触摸事件，并从 `/dev/fb0` 实时采集还原为 `1280x720` 正向截图。

### `CHK-01`：三端版本与运行模式查询
- **真实触屏路径**：首页 [03_home_en_baseline.png](03_home_en_baseline.png) → 点击齿轮 `Settings (56, 595)` → 列表上滑 `(640,580)->(640,200)` 露出底部 → 点击 `Help & About (500, 655)`（[chk01_01_help_about_en.png](chk01_01_help_about_en.png)）→ 点击 `About (500, 625)`（首屏 [chk01_02a_about_initial_top_en.png](chk01_02a_about_initial_top_en.png) 仅显示至 `Check for Updates`）→ 列表上滑 `(640,600)->(640,200)` 露出三端版本行（[chk01_02_about_top_en.png](chk01_02_about_top_en.png)、[chk01_03_about_versions_and_ota_row_en.png](chk01_03_about_versions_and_ota_row_en.png)）。
- **前后端版本与运行模式逐项对账**（日志见 [chk01_backend_version_check.log](chk01_backend_version_check.log)）：
  - **AP**：屏幕右侧显示 `0.1.0-skeleton (6f28023f) [c308l-production]` ＝＝ `/etc/printer-soc/version.json`（`product_version="0.1.0-skeleton"`, `git_sha="6f28023f"`, `profile="c308l-production"`），**数据一致**。
  - **MC**：屏幕右侧显示 `2.0 (0xA64BFFBF, boot=1775181012) [App]` ＝＝ `GetVersionInfo.devices.mc`（`firmware_version="2.0"`, `git_commit="0xA64BFFBF"`, `boot_id=1775181012`, `capability_flags=3` 即 `App` 模式），**数据一致**。
  - **TH**：屏幕右侧显示 `2.0 (0xA64BFFBF, boot=1462640722) [App]` ＝＝ `GetVersionInfo.devices.th`（`firmware_version="2.0"`, `git_commit="0xA64BFFBF"`, `boot_id=1462640722`, `capability_flags=7` 即 `App` 模式），**数据一致**。
- **实测异常与五类标准归因**：
  - **`其他异常`**：在 `r18b` 默认 `"language": "en"` 配置下，`CjkFontManager::needs_cjk("en") == false` 未挂载运行时 29 个 `noto_sans_cjk_*.bin` 字库，导致三行中文标签渲染为缺字豆腐块 **`AP □本`**、**`MC □□`**、**`TH □□`**（见 [chk01_03_about_versions_and_ota_row_en.png](chk01_03_about_versions_and_ota_row_en.png)；仅“本”字因内置于语言列表 `"日本語"` 基础编译字体而幸存；对比中文模式 [02f_pre_zh_about_bottom.png](02f_pre_zh_about_bottom.png) 则显示 `AP 版本`、`MC 固件`、`TH 固件`）。

### `CHK-02`：屏幕亮度调节与恢复
- **真实触屏路径**：`Settings` 顶部 → 点击 `Display & Sound (500, 185)` → 列表连续上滑 2 次露出 `DISPLAY -> Brightness` 滑块（初始 `80%`，见 [chk02_01_brightness_before_en.png](chk02_01_brightness_before_en.png)）→ 向左拖动滑块 `(985, 590) -> (550, 590)` 调低至 `41%`（[chk02_02_brightness_lowered_en.png](chk02_02_brightness_lowered_en.png)）→ 向右拖动滑块 `(550, 590) -> (985, 590)` 恢复至 `80%`（[chk02_03_brightness_restored_en.png](chk02_03_brightness_restored_en.png)）。
- **物理背光节点对账**（`/sys/class/backlight/aml-bl/`，日志见 [chk02_backlight_adjustment.log](chk02_backlight_adjustment.log)）：
  - 拖动前：`brightness = 204`，`actual_brightness = 204`，`max_brightness = 255`，`bl_power = 0`（对应 `204 / 255 = 80.0%`）；
  - 拖低后：`brightness = 104`，`actual_brightness = 104`（对应 `104 / 255 = 40.8% ≈ 41%`），物理屏幕背光真实变暗；
  - 恢复后：`brightness = 204`，`actual_brightness = 204`，`settings.json` 中 `"brightness": 80`，**零误差恢复原值**。
- **实测判定与五类标准归因**：**功能正常（PASS，无卡点）**。

### `CHK-03`：有线网络信息查看
- **真实触屏路径**：`Settings` 底部（[chk03_00_back_settings_en.png](chk03_00_back_settings_en.png)）→ 点击 `System (500, 500)`（[chk03_01_system_en.png](chk03_01_system_en.png)）→ 点击 `Network Settings (500, 256)` → 打开网络设置页查看 `Ethernet` 区块（[chk03_02_network_settings_en.png](chk03_02_network_settings_en.png)）。
- **网络配置对账**（日志见 [chk03_ip_addr_eth0.log](chk03_ip_addr_eth0.log)）：
  - 屏幕 `Ethernet` 区块显示：`Connected`、`IP: 192.168.1.101`、`MAC: 02:ad:3d:01:8e:eb`；
  - 板端 `ip addr show eth0` 实测：`inet 192.168.1.101/24`、`link/ether 02:ad:3d:01:8e:eb`（`UP, LOWER_UP`），**IP 与 MAC 100% 精确一致**。
- **实测判定与五类标准归因**：**功能正常（PASS，无卡点）**。

### `CHK-04`：MC/TH 升级入口发现性
- **实机核查过程与精确步数计量**：
  1. **`Settings` 一级菜单全量浏览**：从顶部（[chk04_01_settings_l1_top_en.png](chk04_01_settings_l1_top_en.png) / 中文 [02b_pre_zh_settings_l1.png](02b_pre_zh_settings_l1.png)）滚动到底部（[chk04_02_settings_l1_bottom_en.png](chk04_02_settings_l1_bottom_en.png) / 中文 [02c_pre_zh_settings_l1_bottom.png](02c_pre_zh_settings_l1_bottom.png)），一级菜单仅有 7 个分类：`Display & Sound`、`Printer`、`Printing`、`Hardware & Devices`、`Safety & Notifications`、`System`、`Help & About`。**`Settings` 一级菜单完全没有固件升级入口**（甚至 `Hardware & Devices` 与 `System` 内也无此入口）。
  2. **`aisoc_mode` 门控核实**：`aisoc_mode` 实测为 `1`，未将 `About` 页内的 `row_aisoc_local_ota` 隐藏。
  3. **从首页触达升级页面的精确操作步数**：共需 **4 次点击 + 2 次滚动**（总计 **6 次触屏交互**）：
     - **点击 #1**：首页左侧齿轮 `Settings`；
     - **滚动 #1**：在 `Settings` 一级菜单向上滑动列表（首屏底部仅露出半行 `System`，`Help & About` 完全在视口外！）；
     - **点击 #2**：点击最底部的 `Help & About`；
     - **点击 #3**：点击最底部的 `About`（进入后首屏 [chk01_02a_about_initial_top_en.png](chk01_02a_about_initial_top_en.png) 仅显示 HelixScreen 徽标与原生 `Check for Updates`，看不到 AISoC 区域）；
     - **滚动 #2**：在 `About` 页面向上滑动列表，露出 AISoC 版本与升级入口（[chk04_03_about_scrolled_ota_entry_en.png](chk04_03_about_scrolled_ota_entry_en.png)）；
     - **点击 #4**：点击 `本地固件升级 (MC/TH)` 行打开 `OtaLocalOverlay`。
  4. **视觉可辨识度双重障碍**：
     - 在 `r18b` 默认 `"en"` 下，该入口渲染为 **`本□□□□□ (MC/TH)`**，副标题为 **`□□□□□□□□□□□□ MC/TH □□`**（[chk04_03_about_scrolled_ota_entry_en.png](chk04_03_about_scrolled_ota_entry_en.png)），中文全部变豆腐块；
     - 在 `About` 首屏上方还存在原生 HelixScreen 的 `Check for Updates`（中文为 `检查更新`，见 [02e_pre_zh_about_top.png](02e_pre_zh_about_top.png)），极易让寻找升级的用户误以为那就是固件更新入口；且中文下旧入口副标题写为 `从固定目录扫描、验签并升级 MC/TH 固件`（[02f_pre_zh_about_bottom.png](02f_pre_zh_about_bottom.png)），将当前 `integrity-only-hil` 校验误表述为“验签”。
- **五类标准归因**：
  - **`入口难找`**（主因：`Settings` 一级无入口，深藏于 `Settings -> [滚动] -> Help & About -> About -> [滚动]` 第 3 层子页面折叠区以下，需 4 次点击 + 2 次滚动）；
  - **`其他异常`**（`r18b` 默认 `"en"` 下入口标题与副标题除 `本` 与 `MC/TH` 外全为豆腐块 `□`）；
  - **`反馈不清楚`**（中文副标题误称“验签并升级”，且同页上方紧邻原生 `Check for Updates` 造成混淆）。

### `CHK-05`：打开 OTA 页面与状态可见性
- **真实触屏操作**：在 `About` 页滚动后点击 `(500, 555)` `row_aisoc_local_ota`，成功弹出 `OtaLocalOverlay`，分别采集默认英文态顶部/底部（[chk05_01_ota_overlay_top_en.png](chk05_01_ota_overlay_top_en.png)、[chk05_02_ota_overlay_bottom_en.png](chk05_02_ota_overlay_bottom_en.png)）与中文态顶部/底部（[02g_pre_zh_ota_top.png](02g_pre_zh_ota_top.png)、[02h_pre_zh_ota_bottom.png](02h_pre_zh_ota_bottom.png)）。
- **逐项核对结果**：
  1. **页面可打开性与布局稳定性**：覆层可正常响应点击并滑入打开，无崩溃、无白屏、无控件重叠裁切，排除 `页面打不开`。
  2. **默认英文（`"en"`）配置下字体严重退化**：由于 `CjkFontManager` 在 `"en"` 下卸载/不加载 CJK `.bin` 字库，全页面所有中文标签、状态描述、安全开关与操作按钮**全部变成豆腐块方框 `□`**：
     - 顶栏标题：`本□□□□□ (MC/TH)`；
     - 节点状态行：`TH □□□` -> `fw_th.bin: □□□□□□□□`；`MC □□□` -> `fw_mc.bin: □□□□□□□□`；
     - 安全确认开关：`□□□□□□`（副标题 `□□□□□□□□□□□□□□`，14 个连续方框，完全无法辨认其为安全前置确认开关）；
     - 底部三个操作按钮：`□□□□□□□□`（副标题 `□□ ATSG □ ECDSA-P256 □□□□`）、`□□本□ OTA □□`（副标题 `□□□□ DDS □□□□□□□□□ Bit31=0 □ boot_id`）、`□□□□ (E-Stop)`（见 [chk05_02_ota_overlay_bottom_en.png](chk05_02_ota_overlay_bottom_en.png)）。
  3. **中文（`"zh"`）配置下仍存局部缺字方框**：即便手动将系统语言切为中文加载了 29 个 CJK `.bin` 字库，`开始本地 OTA 升级` 按钮副标题 `订阅真实 DDS 进度并在重启后核验 Bit31=0 与 boot_id` 中的前 3 个汉字（`订`、`阅`、`真`）因未收录进 `.cjk_codepoints.manifest`，在实机屏幕上依然渲染为 **`□□□实 DDS 进度并在重启后核验 Bit31=0 与 boot_id`**（见 [02h_pre_zh_ota_bottom.png](02h_pre_zh_ota_bottom.png)）。
  4. **校验策略误导与包状态文案模糊**：
     - `扫描固定目录固件` 按钮副标题硬编码为 **`核验 ATSG 与 ECDSA-P256 发布签名`**（[02h_pre_zh_ota_bottom.png](02h_pre_zh_ota_bottom.png)），与 `r18b` 候选实际运行的 `integrity-only-hil` 完整性校验策略不符；
     - `TH 固件包` / `MC 固件包` 状态行仅显示 `fw_th.bin: 未扫描或校验未通过` / `fw_mc.bin: 未扫描或校验未通过`（[02g_pre_zh_ota_top.png](02g_pre_zh_ota_top.png)），将“初始未扫描”、“目录无此文件”与“文件校验不通过”混作同一句模糊提示，且页面首屏未告知固定扫描目录的具体路径 `/run/printer-soc/firmware/`（`ui_settings_ota.cpp` 中状态被历史 `FAILED` 覆盖后路径提示消失）。
- **五类标准归因**：
  - **`其他异常`**（默认 `"en"` 全页中文渲染为豆腐块 `□`；`"zh"` 下 `订阅真` 3 字仍缺字显示为 `□□□`）；
  - **`反馈不清楚`**（硬编码误称“核验 ATSG 与 ECDSA-P256 发布签名”；节点包状态未区分未扫描/缺包/校验失败）。

### `CHK-06`：扫描固件与结果反馈
- **真实触屏操作**：确认 `/run/printer-soc/firmware/` 为系统默认空目录（不预置任何包、不触发升级），在 `OtaLocalOverlay` 底部点击 `扫描固定目录固件` 行 `(500, 383)`，抓拍点击后底部视口 [chk06_01_after_scan_bottom_en.png](chk06_01_after_scan_bottom_en.png)，随后列表下滑回顶部抓拍状态区 [chk06_02_after_scan_top_en.png](chk06_02_after_scan_top_en.png)，同步采集目录清单与后台日志 [chk06_scan_and_logs.log](chk06_scan_and_logs.log)。
- **前后端实测表现**：
  1. **后台扫描通路与耗时**：点击后 D-Bus `ForwardInterface.OtaCommand(op=0, mask=3)` 立即送达 `forward_service_daemon`，`/run/printer-soc/forward.log` 新增 `task_id="760000002"`：
     - `event_id=4` (`timestamp_unix_ms=147021619`): `phase="PRECHECK", active=true, target_mask=3`；
     - `event_id=5` (`timestamp_unix_ms=147021619`): `phase="FAILED", active=false, error="PACKAGE_INVALID_OR_CHANGED", mc.valid=false, th.valid=false`。
     后台 `forward.log` 中同一任务从 `PRECHECK` 至 `FAILED` 两个阶段的时间戳差 `< 1 ms`（落在同一毫秒 `147021619`，注：该数值为后台两阶段日志时间差，不含客户端 D-Bus RPC 发起与应答往返时戳），扫描 IPC 与 DDS 状态回传链路本身工作正常。
  2. **界面结果反馈三大卡点**：
     - **卡点 A（默认目录无固件包）**：`r18b` 部署后 `/run/printer-soc/firmware/` 默认为空目录，无配套可扫描的 `fw_mc.bin` / `fw_th.bin`。
     - **卡点 B（底部点击无即时视觉反馈，视口上下割裂）**：`扫描固定目录固件` 按钮位于页面底部第二屏，点击后既无 Toast 提示，底部画面也无任何文字变化（仅行边框聚焦高亮，见 [chk06_01_after_scan_bottom_en.png](chk06_01_after_scan_bottom_en.png)）；用户必须手动滑回最顶部才能看到 `升级状态` 行，极易误以为“点了没反应”。
     - **卡点 C（缺包报错码误导且无下一步操作指引）**：滑回顶部后，总状态显示 **`失败: PACKAGE_INVALID_OR_CHANGED`**（英文态下为 **`□□: PACKAGE_INVALID_OR_CHANGED`**，见 [chk06_02_after_scan_top_en.png](chk06_02_after_scan_top_en.png) 与中文态 [02g_pre_zh_ota_top.png](02g_pre_zh_ota_top.png)），`TH` / `MC` 行仍笼统显示 `fw_th.bin: 未扫描或校验未通过` / `fw_mc.bin: 未扫描或校验未通过`。普通操作者看到 `PACKAGE_INVALID_OR_CHANGED` 会误判为“固件包损坏或被篡改”，既看不出真实原因是**目录为空未找到文件**，也不知道哪块板缺包、更不知道下一步应将 `fw_th.bin` / `fw_mc.bin` 放入 `/run/printer-soc/firmware/` 后重新扫描（且后端 `prepare_images()` 在 `fw_mc.bin` 缺失时还会短路跳过 `fw_th.bin` 扫描）。
- **五类标准归因**：
  - **`缺固件包`**（`/run/printer-soc/firmware/` 系统默认为空，未就位可扫描的 `fw_mc.bin` / `fw_th.bin`）；
  - **`反馈不清楚`**（① 空目录缺包笼统报 `PACKAGE_INVALID_OR_CHANGED` 与 `未扫描或校验未通过`，混淆缺包与损坏；② 点击底部扫描按钮无即时反馈，结果藏在顶部首屏；③ 缺失将固件放入 `/run/printer-soc/firmware/` 后重扫的明确下一步指引）；
  - **`其他异常`**（默认 `"en"` 配置下状态标题与节点描述全部渲染为豆腐块 `□`）。

---

## 4. `UX-01` 五类标准归因汇总矩阵与核心结论

### 4.1 按 §1.5.3 五类硬标准的逐项判定汇总

| 检查项 | 实机完成情况 | `入口难找` | `页面打不开` | `缺固件包` | `反馈不清楚` | `其他异常` | 关联核心证物 |
| :---: | --- | :---: | :---: | :---: | :---: | :---: | --- |
| **`CHK-01` 三端版本与模式** | 三端版本/模式数值与后台 100% 一致 | — | — | — | — | **命中**（`"en"` 下中文标签变豆腐块 `AP □本` / `MC □□` / `TH □□`） | `chk01_03_about_versions_and_ota_row_en.png`, `02f_pre_zh_about_bottom.png`, `chk01_backend_version_check.log` |
| **`CHK-02` 屏幕亮度调节** | 滑块灵敏，`aml-bl` `204->104->204` 真实变化并恢复原值 | — | — | — | — | — | `chk02_01`~`chk02_03`, `chk02_backlight_adjustment.log` |
| **`CHK-03` 有线网络查看** | `eth0` IP `192.168.1.101` 与 MAC `02:ad:3d:01:8e:eb` 100% 一致 | — | — | — | — | — | `chk03_02_network_settings_en.png`, `chk03_ip_addr_eth0.log` |
| **`CHK-04` 升级入口发现性** | `Settings` 一级无入口；需 4 次点击 + 2 次滚动进入 `About` 底部 | **命中** | —（`aisoc_mode=1` 未隐藏） | — | **命中**（旧副标题误写“验签”，上方紧邻 `Check for Updates`） | **命中**（`"en"` 下入口变 `本□□□□□ (MC/TH)`） | `chk04_01`~`chk04_03`, `02b`, `02c`, `02f` |
| **`CHK-05` 打开 OTA 页面** | `OtaLocalOverlay` 正常打开零崩溃，但字体与文案存在显著卡点 | — | —（页面正常打开） | — | **命中**（硬编码误写 ECDSA-P256 签名；包状态未区分未扫描/缺包/损坏） | **命中**（`"en"` 下全页中文变豆腐块；`"zh"` 下 `订阅真` 3 字仍变 `□□□`） | `chk05_01`, `chk05_02`, `02g`, `02h` |
| **`CHK-06` 扫描固件与反馈** | 扫描链路畅通（后台 `PRECHECK->FAILED` 阶段时间差 `<1ms`），但空目录报错语义模糊且无下一步提示 | — | — | **命中**（`/run/printer-soc/firmware/` 默认为空） | **命中**（空目录误报 `PACKAGE_INVALID_OR_CHANGED`，底部点击无即时提示，无放入路径指引） | **命中**（`"en"` 下状态文字全为豆腐块 `□`） | `chk06_01`, `chk06_02`, `chk06_scan_and_logs.log` |

### 4.2 总结性诊断结论（直接印证 `SLICE-09` `UX-02` 修复靶向性）
1. **排除 `页面打不开`**：实板 `aisoc_mode == 1` 正常生效，`OtaLocalOverlay` 页面打开及 `OtaCommand(op=0)` 后台扫描链路均真实畅通、零崩溃。
2. **锁定真实体验阻断的四重叠加根因**：
   - **`入口难找`**：`Settings` 一级菜单缺失升级入口，旧入口深埋于 `Settings -> [下滑] -> Help & About -> About -> [下滑]`，需 4 次点击 + 2 次滚动；
   - **`其他异常`（默认英文配置 CJK 未挂载 + 局部生僻字未入库）**：`r18b` 出厂默认 `"language": "en"` 下不加载 CJK `.bin` 字库，导致 AISoC 专属中文全部变成豆腐块 `□`；即便用户手动切为 `"zh"`，`ota_local_overlay.xml` 中的 `订阅真` 3 字仍因未入 `.bin` 字库而显示为 `□□□`；
   - **`缺固件包`**：`/run/printer-soc/firmware/` 默认为空，缺少随候选交付就位的同源 `fw_mc.bin` / `fw_th.bin`；
   - **`反馈不清楚`**：空目录扫描笼统返回 `PACKAGE_INVALID_OR_CHANGED` 与 `未扫描或校验未通过`（且后端在缺 `fw_mc.bin` 时短路跳过 `fw_th.bin`），底部点击无即时可见提示，既未告知具体缺失文件名与目标目录路径，又将 `integrity-only-hil` 校验硬编码误写为“核验 ATSG 与 ECDSA-P256 发布签名 / 验签”。

---

## 5. 证物清单（相对 `project-control/docs/evidence/SLICE-09/ux01_r18b_walkthrough/`）

- **主报告与辅助采集脚本**：
  - `UX01_WALKTHROUGH_REPORT.md`：本走查报告
  - `ux01_touch_fb_tool.py`：`/dev/input/event0` 270° 坐标逆变换触控注入与 `/dev/fb0` 正向 PNG 采集脚本
- **基线登记与收尾健康/安全审计日志**：
  - `01_baseline_registration.log`：走查前版本、守护进程、D-Bus 快照、背光、网络、空固件目录与备份摘要登记
  - `01b_initial_settings_json_snapshot.json`：进场未触碰前实板持久化 `settings.json` 只读备份快照
  - `chk01_backend_version_check.log`：`CHK-01` 后台 `version.json` / `GetVersionInfo` / `GetSnapshot` 对账日志
  - `chk02_backlight_adjustment.log`：`CHK-02` 背光节点 `204 -> 104 -> 204` 调节前后实测日志
  - `chk03_ip_addr_eth0.log`：`CHK-03` 板端 `ip addr show eth0` 对账日志
  - `chk06_scan_and_logs.log`：`CHK-06` 扫描前后 `ls -la /run/printer-soc/firmware/`、`forward.log`（`task_id=760000002`）与 `panel.log` 原始日志
  - `08_post_walkthrough_health_and_safety_audit.log`：走查后退回首页、`heating=false`、`brightness=204`、`boot_backup.img` SHA-256、`"language": "en"` 基线与零 `probe-rs` 完整审计日志
- **实板 `/dev/fb0` 270° 还原正向截图（`1280x720` PNG，共 29 张）**：
  - 进场实况与切回默认英文基线：`00_initial_untouched_fb0.png`, `02a_pre_zh_home.png` ~ `02l_lang_dropdown_top.png`, `03_home_en_baseline.png`
  - `CHK-01` & `CHK-04`：`chk04_01_settings_l1_top_en.png`, `chk04_02_settings_l1_bottom_en.png`, `chk01_01_help_about_en.png`, `chk01_02a_about_initial_top_en.png`, `chk01_02_about_top_en.png`, `chk01_03_about_versions_and_ota_row_en.png`, `chk04_03_about_scrolled_ota_entry_en.png`
  - `CHK-02`：`chk02_01_brightness_before_en.png`, `chk02_02_brightness_lowered_en.png`, `chk02_03_brightness_restored_en.png`
  - `CHK-03`：`chk03_00_back_settings_en.png`, `chk03_01_system_en.png`, `chk03_02_network_settings_en.png`
  - `CHK-05` & `CHK-06`：`chk05_01_ota_overlay_top_en.png`, `chk05_02_ota_overlay_bottom_en.png`, `chk06_01_after_scan_bottom_en.png`, `chk06_02_after_scan_top_en.png`
  - 收尾恢复首页：`08_final_home_restored_en.png`
