# SLICE-09 ENG-AP 自检报告 (`S09-AP` / `UX-02` + 默认中文 `"zh"` 与存量一次性迁移)

- **角色身份**: `ENG-AP`
- **业务仓库与分支**: `printer-soc` (`main`)
- **基线 Commit SHA**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`
- **候选 Commit SHA (本地与 `origin/main` 读回一致)**: `5100e4a23c3c28512517fb07a64c80aed2e5b2d6`（含首提 `c25cbfce350605ec8ab9212558335e1758260352` 与 `1280x720` 滚动视口扫描即时 Toast 补强 `5100e4a23c3c28512517fb07a64c80aed2e5b2d6`）
- **对照 SSoT 方案**: `project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md` (`v1.1`)
- **对照切片定义**: `project-control/slices/SLICE-09.yaml`

---

## 1. Diff Budget 与写边界核验

- **允许路径 (`allowed_paths`)**: 严格命中白名单内 `20 / 20` 个文件，零越界触碰其他文件或兄弟仓（`mcu-p3`、`boot/*`、`test_harness`、`sdk/c308l`、`agents` 均为零改动）。
- **受保护存量预算 (`protected_globs`)**:
  - `services/helixscreen/include/ui_panel_settings.h`: `+2 / -0` 行
  - `services/helixscreen/src/ui/ui_panel_settings.cpp`: `+12 / -0` 行
  - `services/helixscreen/src/system/cjk_font_manager.cpp`: `+6 / -0` 行
  - **合计受保护改动**: `20` 行（严格 `<= max_protected_lines: 45`）。
- **工作树洁净度**: 临时构建目录 `.build_s09_ps` 与 `.build_s09_ps_hil` 已在提交前彻底删除，未访问或写入 `/tmp` 构建目录，`git -C printer-soc status --porcelain` 输出为空。

---

## 2. 核心实现要点核对

1. **默认中文 `"zh"` 与存量 `/data` 一次性迁移**:
   - `services/helixscreen/platform/c308l/live-profile.json`: `settings.language` 设为 `"zh"` 并新增 `"c308l_default_lang_migrated": 1`。
   - `tools/c308l_services.py` 与 `boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel`:
     - 首次从只读 `config/settings.json` 播种时同步写入 `.helix-fresh-install`，对齐 `Config::init()` 防止残留旧备份回灌；
     - 新增 `migrate_default_language_once()` 与 `sync_panel_backup_language()`，当只读默认配置声明 `"language": "zh"` 且持久化 `settings.json`（及 `$HOME/.helixscreen/settings.json.backup`）未含 `"c308l_default_lang_migrated"` 时，若原语言为空或 `"en"` 则一次性迁移为 `"zh"` 并落盘 `"c308l_default_lang_migrated": 1`；用户后续手动改回 `"en"` 后重启忠实保留用户选择；
     - `printer-soc-panel` 外层改为 `if [ -f "$HELIX_CONFIG_DIR/settings.json" ]` 解耦 `sys_input` 存在性，仅在 `sys_input` 目录存在时执行 `touch_device` 清洗，100% 兼容存量单测夹具。
   - 更新 `test_tools.py` 并扩展 `test_product_package.py` 正反单测（首启标记、存量 `"en"` 含滚动备份一次性迁 `"zh"`、手动切回 `"en"` 二次启动保持 `"en"`）。
2. **CJK 字库保底、`Settings` 一级入口与双入口单例复用**:
   - `cjk_font_manager.cpp`: 在 `#ifdef HELIX_ENABLE_AISOC` 下令 `CjkFontManager::needs_cjk()` 返回 `true`，保证默认中文及用户手动切回英文时均保持挂载 CJK 后备字库，零豆腐块。
   - `settings_panel.xml` + `ui_panel_settings.h/.cpp`: 在 `row_system` 与 `row_help` 之间新增受 `aisoc_mode` 门控的一级入口 `本地固件升级 (MC/TH)`，回调 `on_settings_local_ota_clicked` 同步在 `init_subjects()` 与 `register_settings_panel_callbacks()` 注册（满足 `[L013]`），调用 `helix::settings::get_ota_local_overlay().show(...)` 与 `About` 页 100% 复用同一单例。
   - `about_settings_overlay.xml` 与 `ota_local_overlay.xml`: 修正静态副标题文案，消除硬编码“ECDSA-P256 发布签名 / 验签”误导及未收录字符。
3. **Forward 单节点 `scan_state`/`scan_error`/`policy` 补齐与非短路扫描**:
   - `ota_internal.h`、`ota_image.cpp`、`forward_ota.cpp`: 增补定长静态数组 `scan_state[2][24]`、`scan_error[2][32]`（零动态分配），输出顶层 `"policy"`（`"integrity-only-hil"` / `"signature-required"`）及 `mc`/`th` 子节点 `"scan_state"`（`UNSCANNED` / `READY` / `MISSING` / `INVALID` / `SIGNATURE_INVALID`）与 `"scan_error"`；`prepare_images()` 在 `operation == 0U` 扫描时完整遍历所选节点不短路，确保单缺 `fw_mc.bin` 时 `fw_th.bin` 仍完成校验并暴露有效 `sha256`。
   - `aisoc_connection.h/.cpp`、`ui_settings_ota.h/.cpp`: 解析 `policy`、`scan_state`、`scan_error`，扩充文本缓冲区（`192B` / `160B`），严格按方案 §2.2.2 字库已验证文案呈现五态与明确下一步指引，支持取消缺失节点后单板升级已就绪节点；针对 `1280x720` 下滚至底部点击「扫描固定目录固件」时顶部状态行不在当前视口的场景，新增 `scan_feedback_pending_`（`on_deactivate()` / `handle_start_upgrade()` 清零，且跳过 `event_id == 0` 的 RPC 初始残影），在收到真实扫描终态（`READY` / `FAILED` 或 RPC 错误）时直接复用已 100% 字库核验的 `phase_str` 弹出即时 `SUCCESS` / `WARNING` Toast（`2800ms`）。
   - 扩展 `test_aisoc_p0.cpp` 与 `test_ota_e2e.py`（新增 `missing_mc_only` 非短路扫描与单板 TH 升级闭环、`policy` 与 `scan_state` 断言）。

---

## 3. 本地实测与门禁验证记录

| 验证项 | 执行命令摘要 | 结果 |
| --- | --- | :---: |
| CJK 字库 100% 字形覆盖门禁 | `python3 -B project-control/docs/evidence/SLICE-09/verify_cjk_glyphs.py printer-soc` | **PASS** (`covered_pool=1826`, 0 缺字) |
| 秒级机械门禁 (`fast_gate.py`) | `fast_gate.py --workspace ... --files <17个非受保护文件>` + `check_subtask_boundary(ENG-AP)` | **PASS** (`20/20` 文件, 受保护 `20/45` 行, 0 违规) |
| 双配置 CMake 构建 + `test_aisoc_p0` | `.build_s09_ps` (严签) + `.build_s09_ps_hil` (`AISOC_OTA_INTEGRITY_ONLY_HIL=ON`) + `g++ -Werror` | **PASS** (0 Error, 0 Warning) |
| ARMv7 交叉语法与类型检查 | `arm-none-linux-gnueabihf-g++ -std=c++17 -Wall -Wextra -Werror -fsyntax-only` (含开关 `HELIX_ENABLE_AISOC`) | **PASS** (4 个 Helix C++ 文件全通过) |
| 双配置 `ctest` 全量单测 | `ctest --test-dir .build_s09_ps` & `ctest --test-dir .build_s09_ps_hil` | **PASS** (`24/24` + `24/24`) |
| Forward 启动快速失败测试 | `python3 -B tests/forward/startup/test_startup_fail_fast.py ...` | **PASS** |
| 双策略 OTA E2E (含单缺包新例) | `test_ota_e2e.py` (`signature-required` + `--policy integrity-only-hil`) | **PASS** (双策略含 `missing_mc_only` 全绿) |
| AISoC 原生连接器 P0 单测 | `./.build_s09_ps/test_aisoc_p0` | **PASS** (`[PASS] test_aisoc_p0`) |
| 平台工具、打包与发布集成单测 | `unittest test_tools.py test_product_package.py` (`30` 项) + `test_release_product.py` (`14` 项) + `test_helix_screen_integration.py --self-test` (`11` 项) | **PASS** |

---

## 4. 汇报分级范围声明

- **已验证范围 (`host-software` + ARMv7 编译与打包单测)**: 宿主机双配置全量单测/E2E、字库覆盖校验、配置一次性迁移正反用例已实测通过。
- **待后续阶段验证 (`c308l-system` 容器沙箱制镜与实板 `HIL`)**: 整包 Docker QA 只读沙箱系统制镜由 `COORD` 统一触发四阶门禁执行；实板 `r18b -> SLICE-09` 持久化 `/data` 语言迁移与触屏双板 OTA 升级留待人工闸门 `Human Gate #2A` 批准后在真机验证。
