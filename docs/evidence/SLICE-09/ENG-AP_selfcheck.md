# SLICE-09 ENG-AP 自检报告 (`S09-AP` / `UX-02` + 默认中文 `"zh"` 存量迁移 + R01 / R03 / R04 / R05 全量返修闭环)

- **角色身份**: `ENG-AP`
- **业务仓库与分支**: `printer-soc` (`main`)
- **基线 Commit SHA**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`
- **候选 Commit SHA (本地与 `origin/main` 读回一致)**: `547162dc1525c7476c7713245feb03aca0a8f150`（线性演进：`c25cbfce` ➔ `5100e4a2` ➔ `7dee19eb` ➔ `bc0ff8c7` ➔ `2560f485` ➔ `7d786f9a` ➔ `547162dc`）
- **对照 SSoT 方案**: `project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md` (`v1.5`)
- **对照切片定义**: `project-control/slices/SLICE-09.yaml` (`revision: 4`)

---

## 1. Diff Budget 与写边界核验 (`6f28023f..547162dc` 累计)

- **允许路径 (`allowed_paths`)**: 严格命中白名单内 `24 / 24` 个文件（`max_files: 24`），零新增白名单外文件，零越界触碰兄弟仓（`mcu-p3`、`boot/*`、`test_harness`、`sdk/c308l`、`agents` 均为零改动）。
- **受保护存量预算 (`protected_globs`)**:
  - `services/helixscreen/include/ui_panel_settings.h`: `+2 / -0` 行（`2` 行）
  - `services/helixscreen/src/ui/ui_panel_settings.cpp`: `+12 / -0` 行（`12` 行）
  - `services/helixscreen/src/system/cjk_font_manager.cpp`: `+6 / -0` 行（`6` 行）
  - `tests/device_manager/twin/test_device_manager.cpp`: `+62 / -13` 行（`75` 行）
  - **合计受保护改动**: `95` 行（严格 `<= max_protected_lines: 100`）。
- **工作树洁净度**: 临时构建目录 `.build_s09_r6` 已在提交前彻底删除，`git -C printer-soc status --porcelain` 输出为空。

---

## 2. Codex R05 六项 `BLOCKER` 与一项 `MINOR` (`S09-R05-01` ~ `S09-R05-07`) 根治记录

1. **`S09-R05-01`（`device_manager_state.cpp:1252-1292` 扫描进出 OTA 维护态保留独立非急停故障 `non_estop_fault`）**:
   - `dev_state_enter_maintenance()` 不再清零 `state->non_estop_fault`，防止急停锁存或独立故障期间从面板发起扫描（触发 `maintenance=true`）意外抹除独立故障记忆；
   - `dev_state_exit_maintenance(state, false)` 退出维护态时令 `state->is_fault = state->non_estop_fault || state->estop_latched;`，当 `state->is_fault` 为真时恢复 `device_state = "FAULT"` 并将 `snapshot.system_status_desc` 置为 `(!state->non_estop_fault && state->estop_latched) ? "EMERGENCY_STOP_INVOKED" : "FAULT"`；
   - `test_device_manager.cpp` 新增真实 DDS `AISOC_TOPIC_OTA_STATUS` `maintenance:true` ➔ `maintenance:false` 扫描进出维护态链路验证：在急停锁存期注入 MC 独立故障并经历完整扫描维护进出后，双板 `EmergencyStop(0)` 解除成功仍保持 `FAULT`（`fault=true, estop_latched=false, estop_confirmed=false`），且继续以 `AISOC_DEV_ERR_FAULT (-6)` / `accepted=false` 拒绝 `MotionHome` 与 `RequestImmediateSample`。
2. **`S09-R05-02`（`device_manager_dbus.cpp:285-362` 区分首跳 MC 发送前 `BUSY` 拒绝与第二跳 TH 半程 `BUSY`）**:
   - 核实 `forward_dbus.cpp:114-115` 与 `forward_control.cpp:93/182-193`：`ForwardInterface.EmergencyStop` 先发 `MC (0x02)`、收到 ACK 后隔 `45ms` 再发 `TH (0x03)`，所有发送前 `BUSY` 拒绝（OTA 线程门禁、I/O 队列满或停止）均未进入 `fwd_exchange_drive`，第 2 个回复参数 `detail` 固定含 `"target_node=0x02"` 与 `"sequence_id=0 "`；
   - `forward_emergency_stop_rpc()` 在 `aisoc_dbus_msg_unref(&fwd_reply)` **之前**安全提取 `detail` 字符串（零 UAF），仅当 `fwd_err == AISOC_DEV_ERR_BUSY` 且同时匹配 `"target_node=0x02"` 与 `"sequence_id=0 "` 时置 `*out_pre_send_rejected = true`；`handle_emergency_stop()` 仅在 `reason_code == 1U && pre_send_rejected && !prev_latched` 时回滚本地急停锁，第二跳 `TH (0x03)` 半程 `BUSY` 严格保留 `estop_latched=true, estop_confirmed=false`；
   - `test_device_manager.cpp` 分别实测 `target_node=0x02 sequence_id=0` 发送前拒绝回滚至 `IDLE` 与 `target_node=0x03` 半程 `BUSY` 保持 `estop_latched=true, estop_confirmed=false`。
3. **`S09-R05-03`（`aisoc_connection.cpp:742-750` DDS 订阅句柄为空时照常执行 `check_ota_dds_timeout()`）**:
   - `poll_ota_dds()` 在 `sub == nullptr`（DDS Participant/Subscriber 创建失败或被禁用）提前返回前显式调用 `check_ota_dds_timeout()`，杜绝 D-Bus 受理 `OtaCommand` 置 `active=true` 后因无 DDS 句柄永久卡死在 `BUSY`；
   - `AisocConnectionConfig` 新增测试注入开关 `disable_ota_dds`，`test_aisoc_p0.cpp` 实测覆盖 `sub == nullptr` 路径在超时阈值到达后准时转入 `FAILED` / `OTA_DDS_TIMEOUT`。
4. **`S09-R05-04`（`forward_ota.cpp:198-241` & `aisoc_connection.cpp:896-905` DDS 发布成功后方推进 `published_id` + 超时重扫核对权威状态）**:
   - `forward_ota.cpp:reporter_main()` 移除发布前提前推进 `rt->published_id` 的缺陷：仅在 `aisoc_dds_publish_ota_status() == AISOC_DDS_OK` 时推进 `rt->published_id = target_id`，发布失败时以 `CLOCK_REALTIME` 条件变量有界退避（前 20 次 `50ms`、此后 `250ms`，随 `rt->stopping` 或新 `event_id` 即刻唤醒），待 DDS 恢复后自动补发最新终态（含 `maintenance=false`）；
   - `aisoc_connection.cpp:check_ota_scan_gate()` 在 `!st.active && st.error == "OTA_DDS_TIMEOUT"` 时放行一次性只读扫描重探以核对 `Forward` 权威状态（升级门禁 `check_ota_upgrade_gate` 与状态栏 `evaluate_ota_lock_state` 继续维持维护忙锁）；`test_aisoc_p0.cpp` 双路径验证：若 `Forward` 真实维护仍在途则返回 `-5` 转入 `BACKEND_BUSY` 继续受保护，若 `Forward` 已空闲则受理重扫并恢复 `READY` 与 `DeviceManager` 状态。
5. **`S09-R05-05`（`aisoc_connection.cpp:344-358` 升级 RPC 受理瞬间同步清空双板展示摘要）**:
   - `apply_accepted_ota_rpc()` 不再仅清理未选节点，而是在 `operation=0` 与 `operation=1`（含双板与单板升级）受理成功进入 `PRECHECK` 瞬间统一清空 `next->mc = AisocOtaNodeInfo{}; next->th = AisocOtaNodeInfo{};`（`handle_start_upgrade()` 已在调用 `request_ota(req)` 前提取 `req.mc_sha256` / `req.th_sha256` 传给后端比对），确保首个 DDS 样本到达前覆层展示与 `Forward::prepare_command()` 重置后的 `UNSCANNED` 状态完全一致；
   - `test_aisoc_p0.cpp` 新增双板（`mask=3`）与单板（`mask=1`）`operation=1` 受理窗口断言，核验请求摘要完整送达模拟 `Forward` 的同时本地 `mc/th` 展示状态立即清空且 `is_ota_node_pkg_ready` 为 `false`。
6. **`S09-R05-06`（`ui_settings_ota.cpp:188-241` & `aisoc_connection.cpp:938-949` 按回调样本原值结算一次性扫描反馈 Toast，最新状态同步忙锁）**:
   - `OtaLocalOverlay::on_activate()` 在 `set_ota_callback` 中按值捕获当次 `const AisocOtaStatus& ev` 排入 `helix::ui::queue_update([ev]() { ... sync_from_backend(&ev); })`；
   - 新增纯函数 `consume_ota_scan_feedback(&scan_feedback_pending_, &pending_scan_seq_, fb_ev)`，`sync_from_backend(callback_ev)` 以回调传入的终态样本及其 `client_req_seq` 结算并原位消费一次性扫描结果 Toast，同时始终从 `conn->ota_status()` 与 `conn->snapshot()` 读取最新状态驱动展示文本与外部新任务的 `BUSY` 忙锁；`test_aisoc_p0.cpp` 模拟同 UI 帧到达「本面板扫描 `READY` 样本 + 外部任务 `client_req_seq=0` 在途样本」，验证扫描 `SUCCESS` Toast 不丢失、不重复触发且最新门禁保持 `BUSY`。
7. **`S09-R05-07`（`aisoc_connection.cpp:881-894` 面板 SHA-256 准入校验与 `Forward::valid_hash` 严格对齐 64 位小写十六进制）**:
   - 新增 `is_valid_sha256_hex()` 替代原 `sha256.size() >= 12U` 宽松判断，要求 `sha256.size() == 64U` 且全部字符属于 `[0-9a-f]`（UI 仍仅截取前 12 位展示），彻底消除截短或大写异常摘要先显示“已就绪”再在提交时被后端拒绝的不一致；`test_aisoc_p0.cpp` 补齐 12 位短摘要与 64 位大写摘要负向拦截单测。

---

## 3. 本地实测与门禁验证记录 (R05 返修后全量复测 + ASan 核验)

| 验证项 | 执行命令摘要 | 结果 |
| --- | --- | :---: |
| CJK 字库 100% 字形覆盖门禁 | `python3 -B project-control/docs/evidence/SLICE-09/verify_cjk_glyphs.py printer-soc` | **PASS** (`covered_pool=1826`, 0 缺字) |
| 提交后正式切片门禁 (`fast_gate.py`) | `python3 -B project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-09.yaml` | **PASS** (`24/24` 文件、`95/100` 受保护行、函数均 `<=50` 行/`<=4` 入参、0 违规) |
| 双配置 CMake 构建 + UI `-Werror` 语法核验 | `.build_s09_r6/ps` + `.build_s09_r6/ps_hil` + `g++ -fsyntax-only -Wall -Wextra -Werror ui_settings_ota.cpp` | **PASS** (0 Error, 0 Warning) |
| ASan 内存安全专项验证 (`-fsanitize=address`) | `test_device_manager_asan` (`32/32`) + `test_aisoc_p0_asan` | **PASS** (0 UAF, 0 ASan Error) |
| 双配置 `ctest` 全量单测 | `ctest --test-dir .build_s09_r6/ps` & `ctest --test-dir .build_s09_r6/ps_hil` | **PASS** (`24/24` + `24/24`) |
| `test_device_manager` 连续 10 次稳定性验证 | `ctest --test-dir .build_s09_r6/ps -R "^test_device_manager$" --repeat until-fail:10` | **PASS** (`10/10` 连续全绿) |
| 启动 Fail-Fast 契约测试 | `tests/forward/startup/test_startup_fail_fast.py` | **PASS** |
| 双策略 OTA E2E 全链路测试 | `tests/ota/test_ota_e2e.py` (`signature-required` + `--policy integrity-only-hil`) | **PASS** |
| AISoC 原生连接器与门禁全场景单测 | `timeout 60s ./.build_s09_r6/test_aisoc_p0`（含 `S09-R05-03` ~ `S09-R05-07` 全部新增回归用例） | **PASS** (`[PASS] test_aisoc_p0`) |
| 平台工具、打包与发布集成单测 | `unittest test_tools.py test_product_package.py` (`31` 项) + `test_release_product.py` (`14` 项) | **PASS** |
