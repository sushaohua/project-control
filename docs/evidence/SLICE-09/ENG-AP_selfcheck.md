# SLICE-09 ENG-AP 自检报告 (`S09-AP` / `UX-02` + 默认中文 `"zh"` 存量迁移 + R01 & R03 返修闭环)

- **角色身份**: `ENG-AP`
- **业务仓库与分支**: `printer-soc` (`main`)
- **基线 Commit SHA**: `6f28023f7f1b774d181fc4ba59d3c378f260bfc1`
- **候选 Commit SHA (本地与 `origin/main` 读回一致)**: `2560f4858889c63d6a1d673f2b429ed78e755b07`（线性演进：`c25cbfce` ➔ `5100e4a2` ➔ `7dee19eb` ➔ `bc0ff8c7` ➔ `2560f485`）
- **对照 SSoT 方案**: `project-control/docs/planning/helix_p0_experience_implementationplan_20261121_190357.md` (`v1.4`)
- **对照切片定义**: `project-control/slices/SLICE-09.yaml` (`revision: 3`)

---

## 1. Diff Budget 与写边界核验 (`6f28023f..2560f485` 累计)

- **允许路径 (`allowed_paths`)**: 严格命中白名单内 `24 / 24` 个文件（`max_files: 24`），零新增白名单外文件，零越界触碰兄弟仓（`mcu-p3`、`boot/*`、`test_harness`、`sdk/c308l`、`agents` 均为零改动）。
- **受保护存量预算 (`protected_globs`)**:
  - `services/helixscreen/include/ui_panel_settings.h`: `+2 / -0` 行（`2` 行）
  - `services/helixscreen/src/ui/ui_panel_settings.cpp`: `+12 / -0` 行（`12` 行）
  - `services/helixscreen/src/system/cjk_font_manager.cpp`: `+6 / -0` 行（`6` 行）
  - `tests/device_manager/twin/test_device_manager.cpp`: `+34 / -5` 行（`39` 行）
  - **合计受保护改动**: `59` 行（严格 `<= max_protected_lines: 60`）。
- **工作树洁净度**: 临时构建目录 `.build_s09_r4` 已在提交前彻底删除，`git -C printer-soc status --porcelain` 输出为空。

---

## 2. 核心实现与 Codex R01 / R03 `BLOCKER` 全量闭环记录

### 2.1 R03 五项 `BLOCKER` (`S09-01` ~ `S09-05`) 根治闭环
1. **`S09-01`（分离急停本地锁存 `estop_latched` 与双板全链路确认 `estop_confirmed`，彻底解耦 `system_status` 字符串）**:
   - `device_manager_types.h` 新增 `bool estop_confirmed;`；`device_manager_state.cpp` 初始化清零并在 `GetSnapshot()` 与 `GetDeviceState()` 输出权威 `"estop_latched":true|false,"estop_confirmed":true|false`；
   - `device_manager_dbus.cpp` 中 `latch_emergency_stop()` 置 `estop_latched=true, estop_confirmed=false` 并递增 `generation_id`；`handle_emergency_stop()` 仅当 `reason_code == 1U && fwd_err == 0` 时调用 `confirm_emergency_stop()` 置 `estop_confirmed=true`（下游超时/失败保持 `estop_latched=true, estop_confirmed=false`），`reason_code == 0U && fwd_err == 0` 时调用 `clear_emergency_stop_state()` 同时清零两者（解除失败不误清本地锁）；维护模式 `is_maintenance || ota_recovery_pending` 期间及首次未锁存撞上 `-5 (AISOC_DEV_ERR_BUSY)` 时直接拒绝/回滚，绝不残留假急停锁；
   - `aisoc_connection.h/.cpp` 与 `ui_settings_ota.cpp` 改为从权威布尔字段解析（DM 断连时清零），彻底摆脱被 MC 故障覆盖为 `"FAULT"` 的 `system_status` 字符串；UI 仅在 `snap.estop_confirmed` 为真时显示 `"状态: 设备已确认急停"`，在 `snap.estop_latched && !snap.estop_confirmed` 时显示 `"状态: 本地急停已锁存（板卡未全部应答）"`；
   - `test_device_manager.cpp` 与 `test_aisoc_p0.cpp` 完整覆盖双板 ACK 确认、TH 超时仅本地锁存、锁存期 MC 故障上报不丢锁、外部 `EmergencyStop(0)` 解除及解除失败保留锁场景。
2. **`S09-02`（重扫请求单调序号 `req_seq` 与新 `task_id` 严格绑定，杜绝旧 `READY` 快照抢跑误弹成功 Toast）**:
   - `AisocConnection::request_ota()` 返回单调递增 `uint64_t req_seq`；`process_pending_ota()` 与 `poll_ota_dds()` 严格隔离旧刷新与残留 DDS 快照——仅当本次请求 RPC 失败直接写入 `client_req_seq = req_seq`，或本次请求分配的**新 `tracked_task_id_`** 对应 DDS 快照到达时才令 `ota_status_.client_req_seq = req_seq`；
   - `OtaLocalOverlay` 通过 `pending_scan_seq_` 与共享判定函数 `evaluate_ota_scan_feedback()` 严格匹配 `st.client_req_seq == pending_scan_seq_` 后才消费 `scan_feedback_pending_`；
   - `test_aisoc_p0.cpp` 实测覆盖「排队在前的旧 `READY` 快照回调与残留旧 `task_id` DDS 快照先于本次 `-2` 重扫拒绝到达，不误弹成功且如实触发本次失败提示」。
3. **`S09-03`（`UNSCANNED` 节点同步清空旧镜像元数据，UI 与门禁三重校验 `READY + valid + sha256`）**:
   - `forward_ota.cpp:prepare_command()` 在重置 `scan_state[index] = "UNSCANNED"` 时（含 `operation == 0U` 全量重扫及升级任务未选节点 `(target_mask & (1U << index)) == 0U`），同步清空 `rt->image[index].valid = false; size = 0U; crc = 0U; version = 0U; sha256[0] = '\0';`，`ota_image.cpp` 在任意读取/验签/摘要失败路径同步调用 `reset_image_meta()`；
   - `aisoc_connection.cpp`（`is_ota_node_pkg_ready()` / `check_ota_upgrade_gate()`）与 `ui_settings_ota.cpp`（`format_ota_pkg`、`format_ota_phase`、`scanned_*_sha256_`）统一要求 `info.scan_state == "READY" && info.valid && info.sha256.size() >= 12U`；
   - `tests/ota/test_ota_e2e.py` 在双策略下新增 `unscanned_th_after_both_scan`（双包扫描 `READY` ➔ 移走 `fw_th.bin` 并发起仅 MC 升级 ➔ TH 终态快照保持 `UNSCANNED + valid=false + sha256="" + size=0`）。
4. **`S09-04`（移除历史粘滞 `last_estop_outcome == BACKEND_BUSY`，OTA 完成后实时恢复就绪）**:
   - `evaluate_ota_lock_state()` 与 `ui_settings_ota.cpp:sync_from_backend()` 的 `BUSY` 判定仅看实时锁 `st.active || st.last_rpc_code == -5 || snap.maintenance_locked`（保留 `application.cpp:2034` 全局 `estop_callback` 不覆盖）；
   - `test_aisoc_p0.cpp` 与 `test_ota_e2e.py`（`_wait_dm_ready_after_busy_estop`）分别在连接器单测与真实双守护进程全链路下验证「升级中点击急停返回 `-5 BUSY` ➔ OTA 完成释放锁 ➔ 状态实时恢复就绪且不残留急停锁」。
5. **`S09-05`（启动 `dev_thread` 前设定 1.5s 后台身份探测静默窗口，100% 确定性验证初始离线契约）**:
   - `test_device_manager.cpp:setup_dev_test_env()` 先初始化 `setup_test_dds_and_dbus_cli(env)`，并在启动 `dev_thread` 前设定 `env->dev_state.next_identity_probe_ns = now_ns + 1500000000ULL`（核实 `dev_thread` 启动入口不覆盖该字段）；在 `test_rpc_get_version_info()` 零削弱验证初始 `OFFLINE + valid:false`，并在 `test_rpc_identity_fields()` 持互斥锁归零 `next_identity_probe_ns = 0U` 验证真实探测与在线缓存吊销。
6. **单测生命周期加固**: `test_aisoc_p0.cpp` 新增 `ScopedCallbackReset` RAII 守卫自动注销栈捕获回调，消除跨子用例悬垂互斥锁死锁隐患。

### 2.2 R01 四项历史 `BLOCKER` 回归保持
- `active` 运行忙锁与 `!active && maintenance` MC 待恢复态精确分流、单缺包提示及 `/var/lib/helixscreen` + `$HOME/.helixscreen` 滚动备份一次性中文迁移均在本次回归中 100% 保持通过。

---

## 3. 本地实测与门禁验证记录 (R03 返修后全量复测)

| 验证项 | 执行命令摘要 | 结果 |
| --- | --- | :---: |
| CJK 字库 100% 字形覆盖门禁 | `python3 -B project-control/docs/evidence/SLICE-09/verify_cjk_glyphs.py printer-soc` | **PASS** (`covered_pool=1826`, 0 缺字) |
| 秒级机械门禁 (`fast_gate.py`) | `fast_gate.py --workspace . --slice project-control/slices/SLICE-09.yaml` + `--files <20个非受保护文件>` | **PASS** (`24/24` 文件、`59/60` 受保护行、函数均 `<=50` 行/`<=4` 入参、0 违规) |
| 双配置 CMake 构建 + UI `-Werror` 语法核验 | `.build_s09_r4/ps` + `.build_s09_r4/ps_hil` + `g++ -fsyntax-only -Wall -Wextra -Werror ui_settings_ota.cpp` | **PASS** (0 Error, 0 Warning) |
| 双配置 `ctest` 全量单测 | `ctest --test-dir .build_s09_r4/ps` & `ctest --test-dir .build_s09_r4/ps_hil` | **PASS** (`24/24` + `24/24`) |
| `test_device_manager` 连续稳定性验证 | `ctest --test-dir .build_s09_r4/ps -R "^test_device_manager$" --repeat until-fail:10` | **PASS** (`10/10` 连续全绿) |
| 启动 Fail-Fast 契约测试 | `python3 -B tests/startup/test_startup_fail_fast.py --build-dir .build_s09_r4/ps` | **PASS** |
| 双策略 OTA E2E (含 `S09-03` & `S09-04` 新例) | `test_ota_e2e.py` (`signature-required` + `--policy integrity-only-hil`) | **PASS** |
| AISoC 原生连接器与门禁单测 | `timeout 60s ./.build_s09_r4/test_aisoc_p0`（含 `S09-01`~`S09-04` 全场景） | **PASS** (`[PASS] test_aisoc_p0`) |
| 平台工具、打包与发布集成单测 | `unittest test_tools.py test_product_package.py` (`31` 项) + `test_release_product.py` (`14` 项) | **PASS** |
