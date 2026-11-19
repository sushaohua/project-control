# SLICE-06 ENG-AP 自检证据报告 (`printer-soc`)

- **角色**：`ENG-AP`
- **唯一目标仓与分支**：`printer-soc` / `main`
- **Candidate Commit**：`c2467833eaf40c0a2dccf9ffd4171280e1e35f45`（含主实现 `9875c9f6`、沙箱路径修复 `a94419ea` 与 S6-002/DEC-SCREEN-05 测试补齐 `c2467833eaf40c0a2dccf9ffd4171280e1e35f45`，已推送至 `origin/main`）
- **基线提交**：`888d389c`

### r02 Codex S6-002 与 DEC-SCREEN-05 一致性测试补齐
- 定向修复与补齐（仅改动 `printer-soc` 内 2 个测试文件）：
  1. `tests/forward/startup/test_startup_fail_fast.py`：确认 `start_dbus_monitor(dependencies, address, sig_log, resources)` 参数完整并实测 8/8 场景全过；核实 `offline_allow_mc_timeout` 与 `offline_allow_th_timeout` 均在拉起 `forward_service_daemon --allow-offline-start` 前启动 `dbus-monitor` 捕获 `LinkStateChanged(false, "STARTUP_PROBE_FAILED")`，随后拉起真实 `device_manager_daemon` 且**严禁手动调用 `ForwardInterface.QueryVersion`**：`offline_allow_mc_timeout` 挂断旧 PTY1 确认 `GetPortStatus` 变为 `false` 与 MC 离线后原子切换至健康 PTY2，纯等 DM 500ms 轮询经 `allow_open=true` 重开串口（`GetPortStatus` `false -> true`）、自动刷新 `DM.GetVersionInfo()` 双端 `ONLINE` 并捕获 `LinkStateChanged(1/2, true, "OK")`；`offline_allow_th_timeout` 纯等 DM 500ms 轮询识别 MC 在线/TH 离线，清零 `model.fault = ''` 后纯等 DM 500ms 轮询自动恢复 TH 在线与 `LinkStateChanged(2, true, "OK")`。
  2. `tests/packaging/test_product_package.py`：新增 `ProductPackageTest.test_dec_screen_05_three_way_pruning_consistency` 及拆分辅助函数（全部满足中文 docstring、`<=50` 行、`<=4` 入参），直接校验真实 `services/helixscreen/` 三方一致性：
     - **编译配置层**：`platform/c308l/cross.mk` 设为 `ENABLE_AISOC := yes`、`ENABLE_MOCKS := no`、`ENABLE_REMOTE_CONTROL := no`、`ENABLE_DEV_PANELS := no` 且不含 `-static`；`platform/c308l/build_env.py` `make_command` 强制 `ENABLE_AISOC=yes`、`ENABLE_MOCKS=no`、`ENABLE_REMOTE_CONTROL=no`；`Makefile` 在非 `ENABLE_MOCKS=yes` 时剔除 `moonraker_api_mock.cpp`，在 `ENABLE_AISOC=yes` 时启用 `-DHELIX_ENABLE_AISOC`。
     - **页面与 XML 注册层**：`scan_xml_registrations` 解析 `src/xml_registration.cpp`（支持单/多行 `register_xml` 与 `#ifdef/#ifndef/#if/#elif/#else/#endif` 栈），核实 `PRUNED_XML_PREFIXES`/`PRUNED_XML_EXACT` 命中的 37 处注册全部处于 `#ifndef HELIX_ENABLE_AISOC` 保护内（0 处未保护注册）；核实 `ui_xml/navigation_bar.xml` 的 `nav_btn_filament` 与 `nav_btn_advanced` 均绑定 `aisoc_mode` 隐藏非 P0 入口。
     - **C308L 打包清单层**：调用 `platform/c308l/package.py:should_include_asset()` 与 `copy_assets()` 遍历真实 `ui_xml/` 与 `assets/`，断言被裁 XML、`demo.py`、`demo_gcodes`、`assets/test_gcodes` 与非通用机型图均被剔除，5 个核心 P0 XML（`about_settings_overlay.xml`、`network_settings_overlay.xml`、`navigation_bar.xml`、`home_panel.xml`、`settings_panel.xml`）均保留；断言 `platform/c308l/live-profile.json` 运行配置字段（剔除中文 `purpose` 说明字段）不含 `--test` 与 `mock_demo`。
- r02 终版 `c2467833eaf40c0a2dccf9ffd4171280e1e35f45` 实测汇总（已清理 `/tmp/s6_fix_build`，`printer-soc` 洁净无残留）：
  - `python3 project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-06.yaml`：PASS (0)
  - `python3 project-control/tools/sync_contracts.py --workspace .`：PASS (0)
  - `ctest --test-dir /tmp/s6_fix_build --output-on-failure`：PASS (`24/24`, `43.01 sec`)
  - `python3 printer-soc/tests/forward/startup/test_startup_fail_fast.py printer-soc /tmp/s6_fix_build/bin printer-soc/third_party/install`：PASS (`8/8`)
  - `python3 -m unittest discover -s printer-soc/tests/packaging -p "test_*.py" -v`：PASS (`9/9`, `0.537s`)
  - `python3 -m unittest discover -s printer-soc/services/helixscreen/platform/c308l/tests -p "test_*.py" -v`：PASS (`16/16`, `0.038s`)
  - `(cd printer-soc && python3 -m unittest services/helixscreen/platform/c308l/tests/test_tools.py tests/packaging/test_product_package.py -v)`：PASS (`22/22`, `0.463s`)
  - `make -C printer-soc/services/helixscreen test-aisoc`：PASS (`[PASS] test_aisoc_p0`)

### r01 Docker QA 门禁失败修复补充
- 查阅 `docker_qa/runtime.log`：23/23 CTest 通过后，`tests/forward/startup/test_startup_fail_fast.py` 因 CMake `CMAKE_RUNTIME_OUTPUT_DIRECTORY` 将二进制生成于 `/output/build_ps/bin/` 而沙箱调用传入 `/output/build_ps/services/forward` 报 `FileNotFoundError`。
- 定向修复：
  1. `tests/forward/startup/test_startup_fail_fast.py` 新增 `resolve_binaries_dir`，当传入目录缺失 `forward_service_daemon` 时回退解析 `binaries.parent.parent / 'bin'`；
  2. `services/helixscreen/tests/unit/aisoc/test_aisoc_p0.cpp` 新增 `apply_dbus_lib_env`，为自定义前缀 `dbus-daemon` 子进程注入同前缀 `lib` 到 `LD_LIBRARY_PATH`，消除与系统旧版 `libdbus-1.so.3` 的符号冲突。
- 本地按 `SLICE-06.yaml` 全套 `qa_commands` 与 `integration_cmd` 等价复跑全部通过（24/24 CTest、8/8 `test_startup_fail_fast.py`、21/21 Python 单测、`[PASS] test_aisoc_p0`、`fast_gate.py` 0 报错）。
- **依据文档**：
  - 获批 SSoT：`project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`
  - 切片定义：`project-control/slices/SLICE-06.yaml`
  - 机器契约：`project-control/contracts/minimc_v2_contract.yaml`

---

## 1. Diff Budget 与路径白名单核验

- **改动文件总数**：`36 / 36`（含 `30` 个修改文件与 `6` 个新增文件，全部命中 `allowed_paths`）。
- **受保护存量变更预算**：`585 / 600` 行以内（已由 `fast_gate.py` 校验通过，含 `services/helixscreen/{Makefile,mk/**,include/**,src/application/**,src/ui/**,src/xml_registration.cpp}`）。
- **工作区洁净度**：`printer-soc` 提交后工作区零额外临时/构建残留；C308L 与宿主机临时构建目录（`/tmp/c308l_verify`、`/tmp/c308l_final_ctest`）已全部清理。

---

## 2. 核心改动摘要

1. **Forward 离线自愈启动与非写刷只读 `QueryVersion` 穿透 (`services/forward/`)**
   - `forward_main.cpp`、`forward_types.h`：新增 `--allow-offline-start`，无该参数时严格保持原生 `exit=2/3` fail-fast 契约；启用后全断连或 MC 在线/TH 离线半断连均降级存活并触发 `LinkStateChanged(false, "STARTUP_PROBE_FAILED")`，随后由 DM 500ms 轮询经 `allow_open=true` 自动重开串口自愈。
   - `forward_ota.h`、`forward_ota_guard.cpp`、`forward_exchange.cpp`、`forward_service.cpp`：当无实际 OTA 写刷活动（`!rt->active && rt->recovery_pending`）时，仅放行只读 `0x01 MINIMC_CMD_GET_VERSION` 事务识别 MC `Bit31=1` Boot 身份；写控制/G-code 仍严格拦截返回 `-5 (AISOC_FWD_ERR_BUSY)`；读回 MC `Bit31=0` App 后自动解除非活动期 `recovery_pending` 并发布 `"IDLE"`。
   - `contracts/twin/dbus_interfaces.xml`：与 `ForwardInterface`（14 方法 + `LinkStateChanged` 信号）及 `DeviceInterface`（13 方法 + 3 信号）保持一一对应。
2. **HelixScreen 进程内原生 `AisocConnection` 与 P0 UI 适配 (`services/helixscreen/`)**
   - 新增 `include/aisoc/aisoc_connection.h`、`src/aisoc/{aisoc_json.h,aisoc_json.cpp,aisoc_connection.cpp}`，进程内直连本地 D-Bus（DM `GetVersionInfo`/`GetSnapshot`/`GetDeviceState` + Boot/维护态下只读 `Forward.QueryVersion` 补充）并读取同源只读 `/etc/printer-soc/version.json`，严格零 `ui_gateway`、零 `--test`、零 `mock_demo`。
   - `Application::init_aisoc()` 通过 `helix::ui::queue_update` 安全刷新主线程 `PrinterState` 与 About 三端（AP + MC + TH 及 App/Boot 模式）视图；`EmergencyStopOverlay` 严格区分 `-5 -> "后台已锁定 (BUSY)"` 与 `0 -> "设备已确认急停"`；`NetworkSettingsOverlay` 仅隐藏 Wi-Fi 卡片及右栏列表而保留 `eth0` IP/MAC 展示；`navigation_bar.xml`、`xml_registration.cpp`、`platform/c308l/package.py` 按 `DEC-SCREEN-05` 协同裁掉无用面板/XML/演示固件/多机型图与 `demo.py`。
   - 新增 `tests/unit/aisoc/test_aisoc_p0.cpp` 与 `mk/tests.mk` 目标 `test-aisoc`，基于真实 `dbus-daemon` 闭环验证全在线、半断连、畸形 JSON、MC Boot 检测/恢复、DM 断链清理与急停结果区分。
3. **C308L 受控动态链接与统一生产监督 (`tools/`、`platform/c308l/`、`boards/c308l-aw419/`)**
   - `tools/build_c308l_services.py`（已拆分 `<=50` 行函数）：编译并导出 `aisoc_dbus.h`、`aisoc_dds.h`、`contracts/twin/*.h`、`libaisoc_dbus.a` 与 `libaisoc_dds.so`。
   - `platform/c308l/{cross.mk,dependencies.mk,build.py,build_env.py,package.py,live-profile.json}`：移除 `-static`，改用 `-Wl,-Bstatic -lz -latomic -Wl,-Bdynamic` 静态链接 `libz.a`/`libatomic.a` 并动态链接 `libc`/`libstdc++`/`libaisoc_dds.so`/`libdbus-1.so.3`，嵌入相对 `RUNPATH=$ORIGIN/../../../../lib/printer-soc:$ORIGIN/../lib`（零绝对 RPATH），开启 `ENABLE_AISOC=yes`、`ENABLE_MOCKS=no`、`ENABLE_REMOTE_CONTROL=no`。
   - `config/runtime/c308l/services.json`、`tools/c308l_services.py`、`boards/c308l-aw419/rootfs-overlay/{etc/init.d/S90printer-soc,usr/bin/printer-soc-panel}`、`tools/package_c308l_product.py`（已拆分 `<=50` 行函数）：默认 `enable_gateway=false`、`allow_offline_start=true`、生成只读 `/etc/printer-soc/version.json`、非阻塞 `start`（`<=4.5s`）、逆序 `stop`、`status`、`dev-mode`（写入 `maintenance_inhibit` 且校验串口/帧缓冲零占用）、包体校验 `<= 44 MiB` 与 `boot_mode=production` / `panel=native_aisoc`。

---

## 3. 提交后实测验证结果（均在 `9875c9f6` 终版代码后真实运行）

| 验证项 | 命令 | 结果 | 关键观测数据 |
| :--- | :--- | :--- | :--- |
| Fast-Gate 机械门禁 | `python3 project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-06.yaml` | PASS (0) | 36/36 文件、受保护预算内、AST/C 门禁 0 报错 |
| 契约同步校验 | `python3 project-control/tools/sync_contracts.py --workspace .` | PASS (0) | 协议与 D-Bus XML 零漂移 |
| 宿主机全量 CTest | `cmake -S printer-soc -B /tmp/c308l_final_ctest -DSOC_AP_BUILD_SERVICES=ON -DTHIRDPARTY_INSTALL_DIR=... && cmake --build ... && ctest --output-on-failure` | PASS (24/24) | 24/24 tests passed (`39.07 sec`) |
| Forward 启动与 Boot 恢复测试 | `python3 printer-soc/tests/forward/startup/test_startup_fail_fast.py printer-soc /tmp/c308l_final_ctest/bin printer-soc/third_party/install` | PASS (8/8) | `open_failure`, `mc_timeout`, `th_timeout`, `normal`, `mc_boot`, `offline_allow_open_failure`, `offline_allow_mc_timeout`, `offline_allow_th_timeout` 全通过 |
| Native `AisocConnection` P0 集成测试 | `make -C printer-soc/services/helixscreen test-aisoc` | PASS | `[PASS] test_aisoc_p0` |
| C308L 构建工具单元测试 | `python3 -m unittest discover -s printer-soc/services/helixscreen/platform/c308l/tests -p "test_*.py" -v` | PASS (16/16) | `Ran 16 tests ... OK` |
| 产品打包与服务监督单元测试 | `python3 -m unittest discover -s printer-soc/tests/packaging -p "test_*.py" -v` | PASS (8/8) | `Ran 8 tests ... OK` |
| C308L 全链交叉构建、动态打包与 ELF 核验 | `build_c308l_services.py` + `build_helixscreen_c308l.py` + `package_helixscreen_c308l.py` + `package_c308l_product.py` + `readelf -d` | PASS | `helix-screen` stripped `11,662,292 B`；`product.tar.gz` `18,508,712 B`（`~17.65 MiB <= 44 MiB`）；`RUNPATH=[$ORIGIN/../../../../lib/printer-soc:$ORIGIN/../lib]`；`NEEDED` 仅含 `libdl.so.2`/`libpthread.so.0`/`libaisoc_dds.so`/`libdbus-1.so.3`/`libstdc++.so.6`/`libm.so.6`/`libgcc_s.so.1`/`libc.so.6`/`ld-linux-armhf.so.3`（零绝对 RPATH、零缺失依赖） |
