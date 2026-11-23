# SLICE-09 ENG-AP 自检报告 (`S09-AP` / `UX-02` + 默认中文 `"zh"` 存量迁移 + R01 / R03 / R04 全量返修闭环)

- **角色身份**: `ENG-AP`
- **业务仓库与分支**: `printer-soc` (`main`)
- **基线 Commit SHA**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`
- **候选 Commit SHA (本地与 `origin/main` 读回一致)**: `7d786f9aaa7d009254fa02bd19a63c926bd93f65`（线性演进：`c25cbfce` ➔ `5100e4a2` ➔ `7dee19eb` ➔ `bc0ff8c7` ➔ `2560f485` ➔ `7d786f9a`）
- **对照 SSoT 方案**: `project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md` (`v1.5`)
- **对照切片定义**: `project-control/slices/SLICE-09.yaml` (`revision: 4`)

---

## 1. Diff Budget 与写边界核验 (`6f28023f..7d786f9a` 累计)

- **允许路径 (`allowed_paths`)**: 严格命中白名单内 `24 / 24` 个文件（`max_files: 24`），零新增白名单外文件，零越界触碰兄弟仓（`mcu-p3`、`boot/*`、`test_harness`、`sdk/c308l`、`agents` 均为零改动）。
- **受保护存量预算 (`protected_globs`)**:
  - `services/helixscreen/include/ui_panel_settings.h`: `+2 / -0` 行（`2` 行）
  - `services/helixscreen/src/ui/ui_panel_settings.cpp`: `+12 / -0` 行（`12` 行）
  - `services/helixscreen/src/system/cjk_font_manager.cpp`: `+6 / -0` 行（`6` 行）
  - `tests/device_manager/twin/test_device_manager.cpp`: `+65 / -10` 行（`75` 行）
  - **合计受保护改动**: `95` 行（严格 `<= max_protected_lines: 100`）。
- **工作树洁净度**: 临时构建目录 `.build_s09_r5` 已在提交前彻底删除，`git -C printer-soc status --porcelain` 输出为空。

---

## 2. 核心实现与 Codex R04 五项 AP `BLOCKER` (`S09-R04-01` ~ `S09-R04-05`) 根治记录

1. **`S09-R04-01`（急停解除进入下游转发前即刻撤销 `estop_confirmed`，杜绝半程解除误报双板仍确认急停）**:
   - `device_manager_dbus.cpp` 新增 `unconfirm_emergency_stop()` 并提炼 `forward_emergency_stop_rpc()`：当 `reason_code == 0U` 通过 `in_maint` 与 `control_permission(CLEAR)` 准入、进入下游 `ForwardInterface.EmergencyStop(0)` 前，立即加锁将已锁存态的 `estop_confirmed` 撤销为 `false`（保留 `estop_latched = true`）并递增 `generation_id` 与 `snapshot.generation_id`；`aisoc_connection.cpp:process_pending_estops()` 对 `engage` 与 `!engage` 遇 `FAILED` 均置 `snapshot_.estop_confirmed = false; refresh_requested_ = true;`；
   - `test_device_manager.cpp` 与 `test_aisoc_p0.cpp` 均实测覆盖「从已确认态（`estop_latched=true, estop_confirmed=true`）出发，发起解除（`0`）遇 TH 超时返回 `-8`，`GetSnapshot` 与 `GetDeviceState` 立即降级为 `estop_latched=true, estop_confirmed=false`」。
2. **`S09-R04-02`（以 `non_estop_fault` 持续跟踪非急停独立故障，解除急停后保留锁存期新故障并阻断普通动作）**:
   - `device_manager_types.h` 新增权威字段 `bool non_estop_fault;`（保留 `fault_before_estop` 兼容存量只读测试编译，生产代码零读取）；`device_manager_state.cpp` 在 `dev_state_init_snapshot()` 与 `dev_state_enter_maintenance()` 清零 `is_fault = false; non_estop_fault = false;`，并在温度越界 `out_of_range`、MC 状态 `machine_state >= 5U` 及非 `"EMERGENCY_STOP_INVOKED"` 的 `dev_state_set_fault()` 同步置位 `non_estop_fault = true`；
   - `device_manager_dbus.cpp:clear_emergency_stop_state()` 清零 `estop_latched/estop_confirmed` 后令 `state->is_fault = state->non_estop_fault;`，若 `state->is_fault` 为真则保持 `device_state = "FAULT"` 并将 `"EMERGENCY_STOP_INVOKED"` 归一为 `"FAULT"`；
   - `test_device_manager.cpp` 分别验证无独立故障解除回 `IDLE`，以及锁存期注入 MC `machine_state = 6U` 故障后执行 `EmergencyStop(0)` 返回 `0` 时保持 `system_status="FAULT", device_state="FAULT", fault=true, estop_latched=false, estop_confirmed=false` 且继续以 `AISOC_DEV_ERR_FAULT (-6)` 拦截 `MotionHome` 与 `RequestImmediateSample`。
3. **`S09-R04-03`（重扫/新任务 RPC 受理即刻作废旧包摘要并置 `active=true`，补齐 DDS 失联有界超时 `OTA_DDS_TIMEOUT`）**:
   - `AisocConnectionConfig` 新增 `ota_scan_timeout_ms = 3000U` 与 `ota_active_timeout_ms = 30000U`；`process_pending_ota()` 在 `rc == 0` 受理新任务瞬间立即置 `next.active = true, next.phase = "PRECHECK", next.progress_pct = 0U, next.event_id = 0U, next.client_req_seq = item.req_seq`，并对扫描请求（`operation == 0U`）或未选节点立即重置 `next.mc` / `next.th` 为 `AisocOtaNodeInfo{}`；
   - `ui_settings_ota.cpp:sync_from_backend()` 移除 `event_id == 0U` 跳过刷新的早退分支，受理瞬间即刻刷新为 `PRECHECK` 在途忙锁并清空 `scanned_*_sha256_`；
   - `compute_worker_wait_ms()` 与 `check_ota_dds_timeout()` 在 `ota_status_.active` 超出对应超时阈值无新 DDS 样本时自动发出 `active=false, maintenance=false, phase="FAILED", error="OTA_DDS_TIMEOUT"`（保留当次 `client_req_seq` 触发失败提示后清空跟踪与包摘要），并在 `test_aisoc_p0.cpp` 用短窗口配置完整验证「受理即刻作废阻断升级 ➔ DDS 失联超时退出 ➔ 立即重扫恢复 `READY`」。
4. **`S09-R04-04`（面板任务终态释放 `tracked_task_id_` 同步外部客户端新任务，对齐生产 `UPGRADING_MAINTENANCE` 快照）**:
   - `poll_ota_dds()` 与 `should_accept_ota_sample()` 在本面板任务到达终态（`!parsed.active`）打出当帧 `client_req_seq` 后立即清空 `tracked_task_id_` 与 `tracked_req_seq_`，对后续数值单调递增的外部客户端新 `task_id` 正常接收并置 `client_req_seq = 0U`（驱动全局 `BUSY` 门禁且不误弹本面板扫描 Toast）；
   - `parse_dm_snapshot_json()` 与 `merge_dm_state_json()` 精确识别生产 `DeviceManager` 顶层 `UPGRADING_MAINTENANCE`（兼容 `MAINTENANCE_HOLD` 及 `bed/tool.quality == "MAINTENANCE_HOLD"`），`check_ota_scan_gate`、`check_ota_upgrade_gate` 与 `evaluate_ota_lock_state` 在非 MC 空闲待恢复态下对 `snap.maintenance_locked` 统一返回 `BACKEND_BUSY` / `BUSY`；`test_aisoc_p0.cpp` 同步对齐生产快照格式并实测外部任务 `"7008"` 与纯快照维护锁闭环。
5. **`S09-R04-05`（根除 `test_device_manager.cpp` 中 `aisoc_dbus_msg_unref` 后读取字符串的悬垂指针 UB）**:
   - 修复 `test_rpc_get_snapshot()` 与 `test_sub_rpc_get_device_state()` 中先 `unref` 后读 `snap_json`/`state_json` 的生命周期缺陷，统一在 `aisoc_dbus_msg_unref()` 前复制到自有 `std::string` 后执行断言，并通过 `-fsanitize=address`（ASan）实测验证零 UAF。

---

## 3. 本地实测与门禁验证记录 (R04 返修后全量复测 + ASan 核验)

| 验证项 | 执行命令摘要 | 结果 |
| --- | --- | :---: |
| CJK 字库 100% 字形覆盖门禁 | `python3 -B project-control/docs/evidence/SLICE-09/verify_cjk_glyphs.py printer-soc` | **PASS** (`covered_pool=1826`, 0 缺字) |
| 切片机械门禁 (`fast_gate.py`) | `python3 -B project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-09.yaml` | **PASS** (`24/24` 文件、`95/100` 受保护行、函数均 `<=50` 行/`<=4` 入参、0 违规) |
| 双配置 CMake 构建 + UI `-Werror` 语法核验 | `.build_s09_r5/ps` + `.build_s09_r5/ps_hil` + `g++ -fsyntax-only -Wall -Wextra -Werror ui_settings_ota.cpp` | **PASS** (0 Error, 0 Warning) |
| ASan 内存安全专项验证 (`-fsanitize=address`) | `test_device_manager_asan` (`32/32`) + `test_aisoc_p0_asan` | **PASS** (0 UAF, 0 ASan Error) |
| 双配置 `ctest` 全量单测 | `ctest --test-dir .build_s09_r5/ps` & `ctest --test-dir .build_s09_r5/ps_hil` | **PASS** (`24/24` + `24/24`) |
| `test_device_manager` 连续 10 次稳定性验证 | `ctest --test-dir .build_s09_r5/ps -R "^test_device_manager$" --repeat until-fail:10` | **PASS** (`10/10` 连续全绿) |
| 启动 Fail-Fast 契约测试 | `tests/forward/startup/test_startup_fail_fast.py` | **PASS** |
| 双策略 OTA E2E 全链路测试 | `tests/ota/test_ota_e2e.py` (`signature-required` + `--policy integrity-only-hil`) | **PASS** |
| AISoC 原生连接器与门禁全场景单测 | `timeout 60s ./.build_s09_r5/test_aisoc_p0`（含 `S09-01`~`04` 与 `S09-R04-01`/`03`/`04`） | **PASS** (`[PASS] test_aisoc_p0`) |
| 平台工具、打包与发布集成单测 | `unittest test_tools.py test_product_package.py` (`31` 项) + `test_release_product.py` (`14` 项) | **PASS** |
