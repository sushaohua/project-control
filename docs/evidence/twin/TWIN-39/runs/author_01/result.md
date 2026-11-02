# TWIN-39 Author Self-Check Result

- **Task**: TWIN-39 (`browser_hmi` 硬件离线阻断视觉与双状态指示器)
- **Role**: ENG-UI
- **Commit**: `soc-ap: 456aa72adb0def34dca448e9dafcdef4e7ab9d52`
- **Result**: PASS

## 1. Verification Summary
- **Header 双状态指示灯 (Header Dual Pills)**：
  - 保留网关服务指示灯 `#conn-pill`（表示与 Web 服务的 HTTP/SSE 状态）。
  - 新增底层物理硬件指示灯 `#hw-conn-pill`，内含状态圆点 `#hw-status-dot` 与状态文本 `#hw-conn-status`。
  - 支持在线 (`online`, 绿灯)、离线 (`offline`, 红灯) 与未知 (`unknown`, 灰灯) 三态切换。
- **顶部离线安全横幅 (Offline Banner)**：
  - 在主界面顶部（导航栏上方）增加 `#hw-offline-banner`，默认 `display: none`。
  - 物理硬件断开时即时显示："⚠️ 硬件连接已断开，运控与加热已锁定，请检查物理连线后重试"。
  - 支持中英文 i18n 免刷新动态切换 (`hw_offline_banner_msg`)。
- **哨兵温度防御性解析与格式化**：
  - 在 `app.js` 的 `extractTemperatureC` 中正确识别 `2147483646` (`0x7FFFFFFE`, `AISOC_TEMP_MILLIC_OFFLINE`) 与 `null`，格式化为 `--.- °C`，彻底杜绝 `2147483.6 °C` 浮点泄漏。
  - 正确识别 `2147483647` (`0x7FFFFFFF`, `AISOC_TEMP_MILLIC_FAULT`) 并展示为 `FAULT`。
- **离线交互安全阻断 (Fail-Closed UI Locking)**：
  - 当硬件离线 (`hwOnline === false`) 时，自动禁用并灰化轴控点动罗盘 (`.btn-jog`)、全部归零 (`#btn-home-all`)、XY 归零 (`#btn-home-xy`)、重新调平 (`#btn-trigger-leveling`) 以及作业控制按钮 (`#btn-job-start`, `#btn-job-resume`)。
  - 当硬件遥测恢复在线时，自动解除禁用，恢复触控交互。
- **友好拦截 HTTP 503 / 504 错误**：
  - 在 `sendPostRequest` 与 `fetchApi` 中拦截 HTTP 503 / 504 响应，解析后端错误消息（如 `"Hardware offline: cannot start job"`）。
  - 通过非阻塞式 `#toast-container` 友好提示告警，并联动触发硬件离线锁，防止未捕获 Promise rejection 或静默吞错。
- **样式与触控规范 (styles.css)**：
  - 保证 `#hw-conn-pill`、`#hw-offline-banner` 与 `.hmi-toast` 在深色/浅色模式下均高对比显眼。
  - 所有按钮与点击目标均满足 `--touch-min-size: 44px` 触控工效规范。

## 2. Test Execution Evidence
- 自动化契约测试套件 `python3 soc-ap/browser_hmi/first_release/test_hmi_contract.py`：
  - `test_01_dom_elements_contract` PASS
  - `test_02_strict_realism_rule_positive_and_negative` PASS
  - `test_03_color_mixing_10000_weight_invariant` PASS
  - `test_04_i18n_dictionary_parity` PASS (100% 中英文对齐)
  - `test_05_styles_touch_targets_and_themes` PASS
  - `test_06_slot_schema_validation` PASS
  - `test_07_real_dual_mcu_firmware_version_presentation` PASS
  - `test_08_e2e_dashboard_and_motion_contract` PASS
  - `test_09_hardware_offline_banner_and_pills_contract` PASS (TWIN-39 新增全量契约测试)
  - **总计: 9/9 测试通过 (100% OK)**
- Node.js 无头 DOM 运行时模拟断言：
  - 哨兵温度解析 (`null`, `2147483646`, `2147483647`, `0x7FFE`, `0x7FFF`) 全部断言通过。
  - 硬件离线判定与按钮禁用 (`.btn-jog`, `btn-home-all`, `btn-trigger-leveling`, `btn-job-start`) 及上线自动解禁全部断言通过。
- C++ 后端 `test_ui_gateway` 测试：
  - 14/14 测试用例全部通过，与前端 503 阻断契约无缝闭环。
