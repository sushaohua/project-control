# SLICE-01 INTEGRATOR 自检与交付回执

## 1. 接单回执与权限基线

| 字段 | 值 |
| :--- | :--- |
| **角色身份 (`role`)** | `INTEGRATOR` |
| **允许写入仓 (`repo`)** | `test_harness` |
| **锁定分支 (`branch`)** | `main`（未写入任何其他业务仓及 `project-control/` 规则/契约/切片/账本） |
| **起始基线 Commit** | `3eef26a98a0e785a35516c910ab971ce208c58b2` |
| **候选提交 (`candidate_commit`)** | `371a3a3de7e878d4035388ccab70ef4bc84f9046`（仅本地原子提交，未执行 `git push`） |
| **消费规则基线 (`project-control`)** | `948fa87a20575a623e38d5cf67ced42f2c7b44c1` |
| **消费规则基线 (`agents`)** | `30ecc6586a861c1543a97804cfe0600bb4778efb` |
| **消费规则文件** | `test_harness/AGENTS.md`、`test_harness/.agents/rules/repository.md`、`project-control/.agents/rules/code_documentation_standard.md` (`v1.1`)、`project-control/.agents/rules/c_cpp_coding_standard.md` (`v1.0`)、`project-control/.agents/rules/delivery_and_coord_gate.md` (`rev 8`)、`project-control/.agents/rules/codex_qa_review.md` |
| **获批 SSoT 方案** | `project-control/docs/planning/mc_th_upgrade_acceptance_implementationplan_20261117_174500.md` (`v1.1`, `Approved`) |
| **切片与契约指针** | `project-control/slices/SLICE-01.yaml` (`revision: 1`)、`project-control/contracts/minimc_v2_contract.yaml` (`MiniMCProto v2.0`, `revision: 2.0.4`) |

---

## 2. 修改摘要与 Diff Budget 自核

- **修改文件（4 个，`+295 / -108` 行）**：
  1. `static_checks/minimcproto/check_opcode_alignment.py`
  2. `static_checks/minimcproto/run_ota_software_suite.py`
  3. `hil/tools/hil_deploy_via_minimc_ota.py`
  4. `hil/tests/test_mcu_firmware_upgrade.py`
- **允许路径 (`allowed_paths`)**：严格限定上述 4 个路径，未新增或改动任何越界文件 — **完全符合**
- **Diff Budget**：`max_files: 4`（实际 `4`），`protected_globs: []`，`max_protected_lines: 0` — **完全符合**
- **具体变更内容**：
  1. **`static_checks/minimcproto/check_opcode_alignment.py`**：
     - 将已封存的 `"soc-ap"` 端点路径替换为 `"printer-soc"`（`printer-soc/contracts/twin/telemetry_types.h`, `printer-soc/core/forward/minimc/codec.h`）；
     - 依据 `minimc_v2_contract.yaml` 为 `mcu-p3(MC)` 与 `mcu-p3(TH)` 补齐共享头文件 `mcu-p3/common/protocol/minimc_proto_defs.h`，并在 `ALLOWED_EXTRA_MACROS` 登记 `MINIMC_CMD_OTA_ABORT = 0x24`（与 `minimc_v2_contract.yaml` 一致）。
  2. **`hil/tools/hil_deploy_via_minimc_ota.py`**：
     - 新增 `encode_version_code()` 与 `CMD_OTA_ABORT = 0x24`，将 `--pack-in/--pack-out` 的 `--version` 打包编码、`_handle_ota_start` `pending_ver` 解码及 Stage 4 (`run_single_node_four_stage_upgrade`) 版本比对统一为 `(major << 24) | (minor << 16) | (patch << 8) | build`，兼容 `2.1`、`2.1.3.4` 与 `0x02010000` 等形式；
     - 移除 `VirtualDualMcuOtaTarget` 中虚构的 `0x23` 4B 主动取消分支，对齐真实 MC/TH Bootloader 语义：`0x24` 返回 `NACK 0x04` (`ERR_UNKNOWN_CMD`)，带载荷 `0x23` 返回 `NACK 0x06` (`ERR_COMMAND_REJECTED`) 且不清空 `ota_state`。
  3. **`hil/tests/test_mcu_firmware_upgrade.py`**：
     - 将 `HIL-CASE-60 ~ HIL-CASE-64` 测试固件包的 `version_code` 全部对齐至 `(major << 24) | (minor << 16) | (patch << 8) | build` 布局；
     - 新增 `HIL-CASE-65` (`verify_case65_no_abort_and_version_encoding` 与 `_verify_node_no_abort_and_reflash`)：实测 `encode_version_code` 与 CLI `--version 0x02010304` 打包、TH 与 MC 双端传输中收到 `0x24 -> NACK 0x04` 与 `4B 0x23 -> NACK 0x06`、中断复位后安全驻留 Bootloader (`Bit31=1`) 并可重刷恢复至 App (`Bit31=0`)。
  4. **`static_checks/minimcproto/run_ota_software_suite.py`**：
     - 在 `_build_app_c_test_jobs` 为 `C03`/`C04` 补齐 `-Imcu-p3/common/protocol` 头路径；
     - 将 `C05 ~ C08` 全部迁移至 `printer-soc`：在 `/tmp` 临时构建目录使用顶层 `cmake -DSOC_AP_BUILD_SERVICES=ON -DTHIRDPARTY_INSTALL_DIR=/usr/local`（工作区 `third_party/install` 不存在时自动解析 `/usr/local`，兼容 `qa-sandbox:20261029` `:ro` 挂载），并通过 CTest 真实执行 `test_forward_protocol`、`forward_ota_progress`、`test_firmware_updater`、`test_ui_gateway_routes` 及 `ota_forward_gateway_pty` (`tests/ota/test_ota_e2e.py` 12 条 PTY E2E 用例)，断言均基于实读 `printer-soc` 源码与真实输出；
     - 在 `C09` 使用 `0x02010500` 验证 `hil_deploy_via_minimc_ota` 与 `boot/bootloadermc/scripts/pack_firmware.py`、`boot/bootloaderth/tools/pack_firmware.py` 的 128B ATSG Trailer 逐字节一致性；
     - 清除 `M07` 假阳性断言，新增 `_exercise_no_abort_recovery` / `_verify_m07_no_abort_and_recovery` 对 TH 与 MC 双端实测 `0x24 -> NACK 0x04`、`4B 0x23 -> NACK 0x06`、中断复位驻留 Bootloader (`Bit31=1`) 及重刷恢复。

---

## 3. 提交后验证原始输出（均在 `371a3a3de7e878d4035388ccab70ef4bc84f9046` 后实测）

### 3.1 `check_opcode_alignment.py`（退出码 `0`）

执行命令：`python3 test_harness/static_checks/minimcproto/check_opcode_alignment.py`

```text
[PASS] MiniMCProto v2.0 (Rev 2.0.4) 5-endpoint opcode alignment, reverse uniqueness, >=520B payload capacity, and negative self-tests verified.
RC_ALIGN=0
```

### 3.2 `qa-sandbox:20261029` 只读挂载容器内 `run_ota_software_suite.py`（退出码 `0`）

执行命令：`docker run --rm -v "$(pwd)":/workspace:ro -w /workspace qa-sandbox:20261029 python3 test_harness/static_checks/minimcproto/run_ota_software_suite.py`

```text
=== MiniMCProto v2.0 (Rev 2.0.4) OTA Software Verification Suite ===

--- 1. Static & Compile-Time Gates (S01~S04) ---
  [PASS] S01: 5-endpoint Rev 2.0.4 opcode table & reverse numeric uniqueness
  [PASS] S02: Zero 0x05/0x15 legacy drift & >=520B payload / >=534B frame capacity
  [PASS] S03: TH Bootloader 16KB (0x08000000..0x08003FFF) Flash budget & 0B .bss growth
  [PASS] S04: Function <=50 lines, <=4 params, Chinese docstrings & inline '#' comments verified

--- 2. Codec & Golden Byte Vectors (D01~D08) ---
  [PASS] G01: status=OK len=14B
  [PASS] G02: status=OK len=14B
  [PASS] G03: status=OK len=26B
  [PASS] G04: status=OK len=30B
  [PASS] G05: status=OK len=18B
  [PASS] G06: status=OK len=18B
  [PASS] G07: status=OK len=15B
  [PASS] G08: status=OK len=18B
  [PASS] G09: status=ERR_FRAME_TOO_SHORT len=10B
  [PASS] G10: status=ERR_BAD_SOF len=14B
  [PASS] G11: status=ERR_BAD_VERSION len=14B
  [PASS] G12: status=ERR_BAD_FLAGS_RESERVED len=14B
  [PASS] G13: status=ERR_BAD_ROUTE_CTRL len=14B
  [PASS] G14: status=ERR_MTU_EXCEEDED len=1039B
  [PASS] G15: status=ERR_CRC_MISMATCH len=14B
  [PASS] G16: status=OK len=158B
  [PASS] G16a: status=OK len=158B
  [PASS] G16b: status=OK len=86B
  [PASS] G16c: status=OK len=534B
  [PASS] G16d: status=OK len=59B
  [PASS] G16e: status=OK len=1038B
  [PASS] G16f: status=OK len=22B
  [PASS] G16g: status=OK len=22B
  [PASS] G16h: status=OK len=18B
  [PASS] G17: status=OK len=17B
  [PASS] G18: status=OK len=17B
  [PASS] G19: status=OK len=17B
  [PASS] G20: status=OK len=17B
  [PASS] G21: status=OK len=17B
  [PASS] G22: status=OK len=17B
  [PASS] G23: status=OK len=17B
  [PASS] G24: status=OK len=17B
  [PASS] G25: status=OK len=17B
  [PASS] V01_MC_BED_NORMAL_60C: status=OK len=30B
  [PASS] V02_TH_NOZZLE_ROUTED_215C: status=OK len=30B
  [PASS] V03_TH_SENSOR_OPEN_FAULT_SENTINEL: status=OK len=30B
  [PASS] V04_AP_PRIORITY_ESTOP_CMD: status=OK len=15B
  [PASS] D01: G01~G04 Ping/Pong/GetVersion/VersionReport(16B) round-trip
  [PASS] D02: G05~G06 0x1D CMD_SYSTEM_CONTROL(4B) & 0x00 CMD_ACK(4B)
  [PASS] D03: G07~G08 0x17 CMD_EMERGENCY_STOP(1B) & priority 0x00 CMD_ACK
  [PASS] D04: G09~G15 Framing negative rejection (SHORT/SOF/VER/FLAGS/ROUTE/MTU/CRC)
  [PASS] D05: G16a 0x20 CMD_OTA_START 144B payload (16B hdr + 128B ATSG Trailer)
  [PASS] D06: G16b~G16e 0x21 CMD_OTA_DATA (64B/512B/37B tail/1016B max) & chunk_crc16
  [PASS] D07: G16f~G16h 0x22 CMD_OTA_FINISH(8B) & 0x23 STATUS(8B/4B framing)
  [PASS] D08: G17~G25 0x06 CMD_NACK standard & OTA error codes (0x01~0x06, 0x10~0x14)

--- 3. Single-Module Contracts & Host Unit Tests (C01~C09) ---
  [PASS] C01: TH Bootloader 7-cmd subset, First-Chunk RAM & Anchor
  [PASS] C02: MC Bootloader USART2 OTA, USB/UART mutex & Trailer
  [PASS] C03: MC App 0x1D safe shutdown, UPG2 magic & 534B TH proxy
  [PASS] C04: TH App 0x1D safe shutdown, UPGD magic & 0x19 filament
  [PASS] C05: printer-soc forward 534B OTA frames, progress & 5000/6000/8000ms timeouts
  [PASS] C06: printer-soc device_manager ATSG precheck & maintenance decay suppression
  [PASS] C07: printer-soc firmware_updater TH->MC order lock & Stage 4 hard isolation
  [PASS] C08: printer-soc ui_gateway 409/OTA routes & ota_forward_gateway_pty E2E (12 cases)
  [PASS] C09: ATSG 128B Trailer & version_code cross-tool parity (OK/OK, mc_parity=True, th_parity=True)

--- 4. End-to-End Virtual Dual-MCU Integration (M01~M08) ---
  [PASS] M01: TH(0x03) 4-stage cascaded upgrade & boot_id transition
  [PASS] M02: MC(0x02) 4-stage direct upgrade & boot_id transition
  [PASS] M03: Strict TH-first then MC-second dual-MCU sequential closed loop
  [PASS] M04: 0x21 chunk CRC16 corruption NACK(0x12) & retry recovery
  [PASS] M05: TH power-loss after Chunk 0 -> stays in Boot & full retry recovery
  [PASS] M06: TH power-loss after Chunk 1 -> Anchor/Chunk0 protected & retry recovery
  [PASS] M07: Unsupported 0x24(NACK 0x04) & 4B 0x23(NACK 0x06), Boot(Bit31=1) & reflash recovery
  [PASS] M08: Stage 3 (95% cap on 0x22 ACK) vs Stage 4 (100% after new App 0x02) isolation

--- 5. Negative & Fault-Injection Interception (N01~N10) ---
  [PASS] N01: Bad ATSG magic (0x41545348) rejected with NACK 0x06 & 0 erases
  [PASS] N02: Board ID mismatch (MC pkg to TH) rejected with NACK 0x06 & 0 erases
  [PASS] N03: Tampered trailer_crc32 rejected with NACK 0x06 & 0 erases
  [PASS] N04: Oversize image (TH 241,665B & MC 917,505B) rejected with NACK 0x14 & 0 erases
  [PASS] N05: Invalid Cortex-M4 vector table (SP/PC Thumb bit0) rejected
  [PASS] N06: Out-of-order 0x21 chunk offset rejected with NACK 0x13
  [PASS] N07: Corrupted 0x22 Finish fw_crc32 rejected with NACK 0x12 & stays in Boot
  [PASS] N08: Upgrade request during PRINTING/HEATING/WRITER_LOCK rejected (NACK 0x05)
  [PASS] N09: Forged legacy 0x05 opcode & unexpected response intercepted & rejected
  [PASS] N10: Post-Finish App boot failure stays at 95% and transitions to ERROR/ROLLBACK

[SUMMARY] OTA Software Suite: 39 passed, 0 failed.
```

### 3.3 `test_mcu_firmware_upgrade.py` 与 `hil_deploy_via_minimc_ota.py --self-test`（退出码 `0`）

执行命令：
- `python3 -m unittest discover -s test_harness/hil/tests -p "test_mcu_firmware_upgrade.py"`
- `python3 test_harness/hil/tools/hil_deploy_via_minimc_ota.py --self-test`

```text
....[EXPECTED-REJECT] invalid --chunk-size=0 (must be 1..512)
[EXPECTED-REJECT] invalid --chunk-size=513 (must be 1..512)
[EXPECTED-REJECT] invalid --baud=12345: unsupported baud=12345 (allowed: (9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000))
.[PASS] Packed 1024B -> 1152B (TH, v2.1, 0x02010304)
.
----------------------------------------------------------------------
Ran 6 tests in 0.570s

OK
RC_UNIT=0
[PASS] hil_deploy_via_minimc_ota.py self-test passed: chunk_size=512B, TH(76896B/151 chunks, 1.1->2.1) then MC(1.2->2.3).
RC_SELFTEST=0
```

### 3.4 `fast_gate.py` 静态与切片边界门禁（退出码 `0`）

执行命令：
- `python3 project-control/tools/gates/fast_gate.py --workspace . --files test_harness/static_checks/minimcproto/check_opcode_alignment.py test_harness/static_checks/minimcproto/run_ota_software_suite.py test_harness/hil/tools/hil_deploy_via_minimc_ota.py test_harness/hil/tests/test_mcu_firmware_upgrade.py`
- `python3 project-control/tools/gates/fast_gate.py --workspace . --slice project-control/slices/SLICE-01.yaml`

```text
RC_FAST_FILES=0
RC_FAST_SLICE=0
```
