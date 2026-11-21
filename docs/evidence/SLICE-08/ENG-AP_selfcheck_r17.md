# SLICE-08 (r17) ENG-AP 自检报告 (`S08-HIL-FIX-02`)

- **角色 / 仓库 / 分支**: `ENG-AP` / `printer-soc` / `main`
- **基线提交**: `8f26e979`
- **候选提交 (`candidate_commit`)**: `2db747cbec027a8ae4a53966a9dd73a3829c83d5`（已完成 `fetch origin main && rebase origin/main && push origin main`，线性历史且工作树干净）
- **依据文档**:
  - `project-control/docs/planning/helix_screen_mc_th_integration_implementationplan_20261118_144741.md`（§4.1–§4.4）
  - `project-control/slices/SLICE-08.yaml`（`revision: 4`, `ENG-AP` subtask）
  - `project-control/contracts/c308l_platform_contract.yaml`

## 1. 修改文件与 Diff Budget 核对

共计修改 **8 个文件**（预算上限 `max_files <= 9`），受保护存量路径（`*services/helixscreen/src/application/**` 与 `*services/helixscreen/src/ui/**`）增删合计 **16 行**（预算上限 `<= 120` 行）：

| 序号 | 文件路径（`printer-soc/` 内） | 增 / 删行数 | 修复内容摘要 |
| :---: | :--- | :---: | :--- |
| 1 | `services/helixscreen/platform/c308l/live-profile.json` | `+1 / -1` | 第 24 行 `input.touch_device` 由 `"/dev/input/event1"` 改为空串 `""`，维持 `display.rotate: 270` 及其他字段不变 |
| 2 | `tools/c308l_services.py` | `+71 / -5` | 新增 `is_touch_event_device(dev_path, sys_input)` 与 `prepare_panel_settings(assets, panel_config, sys_input=None)`（全中文 docstring/注释，<=50 行、<=4 入参）；`launch_panel()` 改为调用 `prepare_panel_settings(assets, panel_config)` |
| 3 | `boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel` | `+32 / -0` | 在 `exec` 前新增基于 `sys_input="$prefix/sys/class/input"` 的 `python3 -B -c` 清洗逻辑：验证 `EV_ABS`（bit 3）与非零 `capabilities/abs`，失效或非触摸节点（如 `ir_keypad1`）原子重置为 `""`（`0o644`）并保留其余配置键 |
| 4 | `services/helixscreen/src/ui/ui_emergency_stop.cpp` | `+11 / -0` | 受 `#ifdef HELIX_ENABLE_AISOC` 保护，在 `show_recovery_dialog()` 与 `show_recovery_for(RecoveryReason reason)` 入口记录 debug 日志后直接 `return;` 屏蔽 `klipper_recovery_dialog`；保留非 AISoC 路径及真实 D-Bus `EmergencyStop` |
| 5 | `services/helixscreen/src/application/application.cpp` | `+5 / -0` | 在 `Application::init_aisoc()` 调用 `m_aisoc->start()` 前调用 `about_overlay.init_subjects()` 与 `about_overlay.register_callbacks()`（核实已含 `#include "ui_settings_about.h"`）；保持第 2020–2031 行真实状态映射完全不变 |
| 6 | `services/helixscreen/ui_xml/advanced_panel.xml` | `+2 / -0` | 为 `advanced_restart_klipper_btn` 与 `advanced_firmware_restart_btn` 各增加 `<bind_flag_if_eq subject="aisoc_mode" flag="hidden" ref_value="1"/>` |
| 7 | `services/helixscreen/platform/c308l/tests/test_tools.py` | `+8 / -1` | 校验 `live-profile.json` 中 `input.touch_device == ''` 且 `display.rotate == 270`、`wizard_completed == True` |
| 8 | `tests/packaging/test_product_package.py` | `+92 / -0` | 新增全中文 docstring 测试覆盖 `c308l_services.prepare_panel_settings`/`launch_panel` 与 `printer-soc-panel` 对 `ir_keypad1`、`event9`、Goodix `event0` 的清洗/保留逻辑，以及 `advanced_panel.xml`、`ui_emergency_stop.cpp`、`application.cpp` 3 项防回归守卫 |

## 2. 提交后真实执行命令与验证结果

以下全部校验均在提交 `2db747cbec027a8ae4a53966a9dd73a3829c83d5` 并推送至 `origin/main` 之后实测执行：

1. **工具与打包单元测试**：
   - 命令：`python3 -B -m unittest printer-soc/services/helixscreen/platform/c308l/tests/test_tools.py printer-soc/tests/packaging/test_product_package.py -v`
   - 退出码：`0`
   - 摘要：`Ran 28 tests in 0.608s` — `OK`（包含新增的 `test_c308l_services_sanitizes_touch_device`、`test_panel_wrapper_sanitizes_touch_device`、`test_s08_hil_fix_02_ui_and_aisoc_guards` 与 `test_c308l_font_tiers_rpath_and_budget`）。

2. **发布校验集成测试**：
   - 命令：`python3 -B -m unittest discover -s printer-soc/tests/integration -p test_release_product.py -v`
   - 退出码：`0`
   - 摘要：`Ran 14 tests in 2.264s` — `OK`。

3. **Fast-Gate 机械门禁与切片边界校验**：
   - 命令：`python3 project-control/tools/gates/fast_gate.py --workspace . --files printer-soc/tools/c308l_services.py printer-soc/services/helixscreen/platform/c308l/tests/test_tools.py printer-soc/tests/packaging/test_product_package.py`
   - 退出码：`0`（零输出报错）。
   - 子任务边界校验（调用 `fast_gate.check_subtask_boundary` 检查 `SLICE-08.yaml` `ENG-AP` 子任务）：`SUBTASK_BOUNDARY_ERRS: []`，退出码 `0`。

4. **Git 线性历史与工作树状态确认**：
   - `git -C printer-soc rev-parse HEAD origin/main`：`2db747cbec027a8ae4a53966a9dd73a3829c83d5`（本地与远端一致）。
   - `git -C printer-soc status --short`：无输出（工作树干净）。

## 3. 范围与未执行项声明

- 本阶段在宿主机完成全部 Python 单测、集成测试、XML/Shell/AST/Diff Budget 校验与 C++ 防回归守卫校验；
- C308L ARM `helix-screen` 交叉编译、全量 `qa_commands` 与 UBIFS/AML 打包构建将在后续 `COORD` / `qa_runner.py` 独立只读 Docker 沙箱及 `Human Gate #2` 批准后的真机 HIL 验收中实测验证；
- 严守边界：未修改 `mcu-p3/`、`boot/`、`test_harness/`、`sdk/`、`agents/` 或根仓文件。
