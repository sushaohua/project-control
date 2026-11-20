# SLICE-08 r14 Option B (`192.168.1.101`) COORD 根因分诊记录

- **日期**：`2026-11-20`
- **分析角色**：`COORD`
- **前置报告**：[INTEGRATOR_option_b_report.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/INTEGRATOR_option_b_report.md)
- **摘要 JSON**：[option_b_summary.json](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/SLICE-08/hil_option_b_r14/option_b_summary.json)

---

## 1. `HIL-DEF-01` (`PANEL_CRASH_LOOP:139` / `tpp.c:82` / `Failed init_port fastdds_port7400`) 完整因果链

通过实板运行 `helix-screen -vvv --log-dest=console -t 8` 与直接读取板端现场转储 `/usr/share/printer-soc/helixscreen/config/crash.txt`，证实 `SIGSEGV (139)`、`tpp.c:82` 断言及 `FastDDS SHM` 报错均源于**同一构建字体层级配置错误**：

1. **直接触发点（`FONT_TIERS := medium` 与 `1280x720` XLARGE 屏幕失配）**：
   - [live-profile.json](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/platform/c308l/live-profile.json#L18-L22) 配置 `"rotate": 270`，C308L `720x1280` 屏有效分辨率为 **`1280x720`**（`min_dim = 720px`），[theme_manager.cpp](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/src/ui/theme_manager.cpp#L1465-L1523) 选择 `XLARGE`（`tier 5`），并在缺失 `_xlarge` 时回退 `_large`。
   - 但 [cross.mk](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/platform/c308l/cross.mk#L26) 固定 `FONT_TIERS := medium`（`HELIX_MAX_FONT_TIER := 3`），未编译链接 `FONTS_LARGE`（`noto_sans_28`、`noto_sans_light_18` 等）与 `FONTS_XLARGE`（`noto_sans_32`、`noto_sans_light_20` 等）。
   - `theme_manager.cpp:1515` 连续跳过 `font_heading` 与 `font_small` 注册（`crash.txt` 记录 `recent_error4:[Theme] Fallback font 'noto_sans_28' for 'font_heading' also not linked — skipping registration` 与 `recent_error3:[Theme] Fallback font 'noto_sans_light_18' for 'font_small' also not linked — skipping registration`）。
2. **中段异常退出与崩溃**：
   - 初始化 UI 约 `+4.06s` 时，`ui_text.cpp:45-48` 查询 `"font_small"` 返回空指针，输出 `[ui_text] FATAL: Font constant 'font_small' not found in globals.xml` 并调用 **`std::exit(EXIT_FAILURE)`**（此时 `AisocConnection` 后台线程 `[1634]` 与 LVGL/FastDDS 静态单例均处于活动态）。
   - `std::exit()` 并发析构全局静态对象期间，线程仍访问已销毁状态，导致 **`SIGSEGV (exit 139)`**（`crash.txt`: `signal:11`, `SEGV_MAPERR`, `fault_addr:0x663666c8`）、glibc `tpp.c:82 (__pthread_tpp_change_priority)` 断言失败，或 FastDDS `open_port_internal` 返回 `Invalid argument` 并遗留 `/dev/shm/fastdds_port7400` 残片。
   - **修复方向**：将 `platform/c308l/cross.mk` 的 `FONT_TIERS` 更新为 `large xlarge`（参照 [fonts.mk](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/mk/fonts.mk#L129-L137) `>=` 规则，会自动包含 `FONTS_MEDIUM + FONTS_LARGE + FONTS_XLARGE`；实测当前 r14 `helixscreen` 安装体积 `27,014,189 B`，远低于 `44 MiB` 预算及 `/` 剩余空间 `35.56 MiB`）。

---

## 2. `HIL-DEF-02`（DDS 域失配、`LD_LIBRARY_PATH`/`DT_RUNPATH` 与 D-Bus 传递）

1. **DDS 域失配**：`c308l_services.py` 中 `launch_panel()` 未从 `services.json` 的 `dds_domain`（`198`）注入 `AISOC_DDS_DOMAIN`，`aisoc_connection.cpp:386` 落回 Domain `0`（`fastdds_port7400`），与 `forward_service_daemon` / `device_manager_daemon`（Domain `198`）隔离。
2. **Domain `198` FastDDS `SHM` 板端实证通过**：在 `192.168.1.101` 上通过 Python `ctypes` 加载 `/usr/lib/printer-soc/libaisoc_dds.so` 并设置 `FASTDDS_BUILTIN_TRANSPORTS=SHM`、Domain `198` 调用 `aisoc_dds_participant_create`，返回 **`rc = 0`**，成功在 `/dev/shm` 建立 `fastdds_port56900/56910/56911` 且销毁后自动清理。
3. **传递动态库路径断裂**：直接执行 `/usr/share/printer-soc/helixscreen/bin/helix-screen --help`（不设 `LD_LIBRARY_PATH`）报 `libfastdds.so.3.6: cannot open shared object file`。原因是 [dependencies.mk](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/platform/c308l/dependencies.mk#L30-L32) 使用 `--enable-new-dtags` 生成非传递的 `DT_RUNPATH`，而 `libaisoc_dds.so` 使用 `-DCMAKE_SKIP_RPATH=ON` 构建。需同时检查 `dependencies.mk`（`--disable-new-dtags` `DT_RPATH` 或在 `/usr/bin/printer-soc-panel` 设置 `LD_LIBRARY_PATH`）以及 `c308l_services.py` 对 `DBUS_SESSION_BUS_ADDRESS` 与 `AISOC_DDS_DOMAIN` 的显式透传。

---

## 3. `HIL-DEF-03`（`HELIX_DATA_DIR` / `HELIX_CONFIG_DIR` 混淆导致根分区被写脏与主题警告）

1. `c308l_services.py`（`launch_panel`）与 [printer-soc-panel](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel#L5) 将 `HELIX_DATA_DIR` 设为 `/data/printer-soc/helix`，且未设置 `HELIX_CONFIG_DIR`。
2. 源码核实：
   - [application.cpp](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/src/application/application.cpp#L1187-L1197) 与 [theme_loader.cpp](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/src/ui/theme_loader.cpp#L424) 将 `HELIX_DATA_DIR` 用作只读资产根（查找 `ui_xml/` 与 `assets/config/themes/defaults/`）。
   - [config.cpp](file:///home/sushaohua/workspace/ai_soc_project/printer-soc/services/helixscreen/src/system/config.cpp#L1648-L1653) 将 `HELIX_CONFIG_DIR` 用作可写运行配置目录；未设置时默认使用相对路径 `config/`（即 `/` 下的 `/usr/share/printer-soc/helixscreen/config/`）。
3. **板端实际后果**：启动即报 `HELIX_DATA_DIR '/data/printer-soc/helix' has no ui_xml/ directory` 与 `[ThemeLoader] Theme 'helixscreen' not found in themes or defaults`，并在 `/` 分区生成/改写了 `/usr/share/printer-soc/helixscreen/config/{settings.json,crash.txt,.crash_restart_count,.helix-screen.lock,telemetry_device.json,telemetry_queue.json}`。
4. **修复方向**：固定 `HELIX_DATA_DIR=/usr/share/printer-soc/helixscreen`，设置 `HELIX_CONFIG_DIR=/data/printer-soc/helix/config`，并在首次启动（目标不存在时）由 `/usr/share/printer-soc/helixscreen/config/settings.json` 播种默认配置到 `/data/printer-soc/helix/config/settings.json`，确保 `rotate=270`、`touch_device=/dev/input/event1`、`wizard_completed=true` 生效且 `/` 不再被运行时写入污染。

---

## 4. `HIL-BLK-01`（`reboot` 后 `/dev/ttyS1` 无响应排查实证）

- **`15:01`（重启前）**：`probe_uart_read_write.py` 于 `/dev/ttyS1` 测得 `MC (0x02)` 与 `TH (0x03)` 在线（`rx=214198`, `irq 37=247278`, `~2ms` 回包）。
- **`15:23`（`reboot` 后）与当前直测排查结果**：
  - 设备树 [c3_c308l_aw419.dts](file:///home/sushaohua/workspace/ai_soc_project/sdk/c308l/platform/kernel/aml-5.15/common_drivers/arch/arm/boot/dts/amlogic/c3_c308l_aw419.dts#L935-L943) 与 [pinctrl-meson-c3.c](file:///home/sushaohua/workspace/ai_soc_project/sdk/c308l/platform/kernel/aml-5.15/common_drivers/drivers/gpio/pinctrl/pinctrl-meson-c3.c#L372-L373) 对照板端 `devmem`：
    - `0xfe00400c = 0x10111111`（bit[31:28]=`1` -> `GPIOX_7` = `uart_e_tx_x`）
    - `0xfe004010 = 0x00001001`（bit[3:0]=`1` -> `GPIOX_8` = `uart_e_rx_x`）
    - `0xfe004100 = 0x000025FF`（`GPIOX_7`/`GPIOX_8` 电平均为空闲高电平 `1`）
    - `0xfe080010 = 0x00002001`、`0xfe080014 = 0x0980000C`（`meson_uart fe080000` 使能、921600 8N1 正常）
  - 独立使用 `probe_uart_read_write.py --port /dev/ttyS1 --node mc --timeout-ms 500 --termios-mode standard` 发送单帧 `0x01`（14B TX 成功写入），仍报 `RESPONSE_TIMEOUT`，且 `/proc/interrupts` `irq 37=0`、`/proc/tty/driver/meson_uart` `rx:0`。
  - 设备树中无 AP GPIO 控制 MC/TH 供电或复位。
  - **结论**：AP 侧引脚复用、波特率、发送物理链路全部正常，需台架侧协助确认 **MC/TH 从板供电是否打开、是否处于 Bootloader/复位保持，或 UART 物理线缆连接状态**。
