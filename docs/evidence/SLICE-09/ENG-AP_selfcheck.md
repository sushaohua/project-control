# SLICE-09 ENG-AP 自检报告 (`S09-AP` / `UX-02` + 默认中文 `"zh"` 与存量一次性迁移 + R01 返修闭环)

- **角色身份**: `ENG-AP`
- **业务仓库与分支**: `printer-soc` (`main`)
- **基线 Commit SHA**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`
- **候选 Commit SHA (本地与 `origin/main` 读回一致)**: `bc0ff8c785ff11b470a4bec6bc46c4aec461da9c`（线性演进：`c25cbfce` ➔ `5100e4a2` ➔ `7dee19eb` ➔ `bc0ff8c7`）
- **对照 SSoT 方案**: `project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md` (`v1.3`)
- **对照切片定义**: `project-control/slices/SLICE-09.yaml` (`revision: 2`)

---

## 1. Diff Budget 与写边界核验 (`6f28023f..bc0ff8c7` 累计)

- **允许路径 (`allowed_paths`)**: 严格命中白名单内 `21 / 21` 个文件，零新增白名单外文件，零越界触碰兄弟仓（`mcu-p3`、`boot/*`、`test_harness`、`sdk/c308l`、`agents` 均为零改动）。
- **受保护存量预算 (`protected_globs`)**:
  - `services/helixscreen/include/ui_panel_settings.h`: `+2 / -0` 行
  - `services/helixscreen/src/ui/ui_panel_settings.cpp`: `+12 / -0` 行
  - `services/helixscreen/src/system/cjk_font_manager.cpp`: `+6 / -0` 行
  - `tests/device_manager/twin/test_device_manager.cpp`: `+2 / -1` 行（共 `3` 行）
  - **合计受保护改动**: `23` 行（严格 `<= max_protected_lines: 50`）。
- **工作树洁净度**: 临时构建目录 `.build_s09_r2` 与 `.build_s09_dm_fix` 均已在提交前彻底删除，`git -C printer-soc status --porcelain` 输出为空。

---

## 2. 核心实现与 Codex R01 四项 `BLOCKER` (`S09-01` ~ `S09-04`) 闭环记录

1. **`S09-01`（区分 `active` 运行忙锁与 `!active && maintenance` MC 待恢复态）**:
   - 在 `aisoc_connection.h/.cpp` 提取单一真源准入函数 `check_ota_scan_gate()` 与 `check_ota_upgrade_gate()` 并由 `ui_settings_ota.cpp` 与 `test_aisoc_p0.cpp` 共用：
     - `handle_scan()` 仅在 `st.active == true` 时弹 `BUSY` 阻断，`!st.active && st.maintenance` 允许扫描恢复包；
     - `handle_start_upgrade()` 在 `!st.active && (st.maintenance || snap.mc.is_boot_mode || st.error == "RESTORE_MC_BEFORE_TH")` 时，若 `mask != 1U`（勾选 TH 或双板）立即弹 `"状态: MC 处于待恢复模式，请取消选择 TH 仅升级 MC"` 阻断，若 `mask == 1U`（仅选 MC）放行单板串口恢复；
     - `sync_from_backend()` 与 `format_ota_phase()` 将 `busy` 收敛为 `st.active` / `last_rpc_code == -5` / `BACKEND_BUSY`，待恢复态清晰展示 `"状态: MC 处于待恢复模式，请取消选择 TH 仅升级 MC"`。
2. **`S09-02`（以权威设备快照驱动 `estop_latched`，消除外部解除后急停提示残留）**:
   - `aisoc_connection.cpp:parse_dm_snapshot_json()` 根据 `GetSnapshot()` 的权威 `system_status` 实时同步 `out_snap->estop_latched = (sys_st == "EMERGENCY_STOP_INVOKED")`，DM 断连时重置为 `false`；
   - `ui_settings_ota.cpp:sync_from_backend()` 状态栏改为判断 `else if (snap.estop_latched)`，不再被历史 `last_estop_outcome == CONFIRMED` 锁死；
   - `test_aisoc_p0.cpp` 新增真实独立 D-Bus 客户端外部调用 `EmergencyStop(byte:0)` 解除急停后 `snapshot().estop_latched == false` 的闭环断言。
3. **`S09-03`（重扫断连或被拒时作废旧 `READY` 摘要、禁止误弹校验通过 Toast）**:
   - `aisoc_connection.cpp:process_pending_ota()` 在 `rc != 0` 时清零 `active`/`reboot_verified`，当 `req.operation == 0U` 重扫失败时立即置 `next.phase = "FAILED"` 并清空 `next.mc` / `next.th` 包摘要，区分 `-5` (`BACKEND_BUSY`)、断连/服务未在线 (`RPC_DISCONNECTED`) 与指令拒绝 (`OTA_COMMAND_REJECTED`)；`poll_ota_dds()` 在收到新 DDS 事件时清零 `parsed.last_rpc_code = 0`；
   - `ui_settings_ota.cpp:format_ota_phase()` 在最顶部优先拦截 `st.last_rpc_code < 0`，`sync_from_backend()` 仅在 `st.last_rpc_code == 0 && !st.active && st.phase == "READY"` 时弹 `SUCCESS` Toast；
   - `test_aisoc_p0.cpp` 新增前次扫描 `READY` 后关闭模拟 Forward 服务重扫（`RPC_DISCONNECTED`）及返回 `-2`（`OTA_COMMAND_REJECTED`）清除 `mc/th.valid` 与 `sha256` 的正反单测。
4. **`S09-04`（全量覆盖 `/var/lib/helixscreen` 首选滚动备份与 `$HOME/.helixscreen` 回退备份一次性语言迁移）**:
   - `tools/c308l_services.py` 与 `printer-soc-panel` 统一遍历首选状态目录（`HELIX_STATE_DIR`、`/var/lib/helixscreen`）与回退目录（`$HOME/.helixscreen`）下的 `settings.json.backup` 与 `helixconfig.json.backup` 共 4 类备份候选：未含 `c308l_default_lang_migrated` 时一次性将 `"en"`/空迁移为 `"zh"` 并落盘标记，已含标记的手动 `"en"` 严格保留不变；
   - `test_product_package.py` 新增 `test_primary_var_lib_backup_migration_and_manual_en_preserved` 覆盖 `c308l_services.py` 与 `printer-soc-panel` 首选备份目录正反迁移断言。

---

## 3. 本地实测与门禁验证记录 (R01 返修后全量复测)

| 验证项 | 执行命令摘要 | 结果 |
| --- | --- | :---: |
| CJK 字库 100% 字形覆盖门禁 | `python3 -B project-control/docs/evidence/SLICE-09/verify_cjk_glyphs.py printer-soc` | **PASS** (`covered_pool=1826`, 0 缺字) |
| 秒级机械门禁 (`fast_gate.py`) | `fast_gate.py --workspace ... --files <17个非受保护文件>` + 累计 `20/20` 文件与 `20/45` 受保护行核验 | **PASS** (函数均 `<=50` 行、`<=4` 入参、0 违规) |
| 双配置 CMake 构建 + ARMv7 `-Werror` | `.build_s09_r2/ps` + `.build_s09_r2/ps_hil` + `arm-none-linux-gnueabihf-g++ -Wall -Wextra -Werror` | **PASS** (0 Error, 0 Warning) |
| 双配置 `ctest` 全量单测 | `ctest --test-dir .build_s09_r2/ps` & `ctest --test-dir .build_s09_r2/ps_hil` | **PASS** (`24/24` + `24/24`) |
| 双策略 OTA E2E (含单缺包新例) | `test_ota_e2e.py` (`signature-required` + `--policy integrity-only-hil`) | **PASS** |
| AISoC 原生连接器与门禁单测 | `./.build_s09_r2/test_aisoc_p0`（含 `S09-01`~`S09-03` 新用例） | **PASS** (`[PASS] test_aisoc_p0`) |
| 平台工具、打包与发布集成单测 | `unittest test_tools.py test_product_package.py` (`31` 项，含 `S09-04` `/var/lib/helixscreen` 新例) + `test_release_product.py` (`14` 项) | **PASS** |
| `test_device_manager` 初始离线版本竞态修复 (`v1.3`) | 将 `test_rpc_get_version_info` 移至 `test_rpc_get_snapshot` 之后、耗时用例之前（零削弱断言），在 `.build_s09_dm_fix` 连续运行 20 次 `ctest -R "^test_device_manager$"` + `fast_gate.py --slice project-control/slices/SLICE-09.yaml` | **PASS** (`20/20` 连续全绿，0 失败) |
