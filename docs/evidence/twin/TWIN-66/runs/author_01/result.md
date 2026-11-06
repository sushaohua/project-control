# TWIN-66 作者交付与自测报告 (`author_01`)

- **任务 ID**: `TWIN-66`
- **执行角色**: `QA / INTEGRATOR` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`)
- **目标仓库与分支**: `test_harness` (`main`)
- **基线 Commit**: `f41d93b753cfd4496f8d5c82fe1c032d1a4d4803`
- **候选 Commit**: `e7f7f574fee7dce8cc78b52772ff32a03b9b345f`

## 1. 规则入口与输入源显式读取登记 (`read_sources`)

- `test_harness/AGENTS.md` + `test_harness/.agents/rules/shared/SOURCE.json` (`source_commit: 6dc6d9e9b7ba9a9db4fb9ac7bc8db87fb65bf6de`)
- `project-control/.agents/rules/repository_rule_sources.json`
- `project-control/.agents/rules/repository_rule_boundaries.md`
- `project-control/.agents/rules/bootloader_role_boundaries.md`
- `project-control/.agents/rules/c_cpp_coding_standard.md`
- `project-control/.agents/rules/code_documentation_standard.md`
- `project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md` (`revision: 2`, `sha256: f41d27c2214cacd1113397f20eb50038a404df94781f4bfdb18239d5d6f246d9`)
- `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` (`Rev 2.0.4`, `sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)
- `project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md` (`revision: 1`, `sha256: c79477a0b9bfa2b18d1451b91b2a6188aa4b50f72bc742a8640aa0a696a1610b`)
- `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` (`revision: 1`, `sha256: 87b0b859e3e7e4cf7e8733ac88d90d1e0fd94f3b3e2117abfea9af3b14d4e6a9`)

## 2. 核心交付物清单

1. **跨五端 Rev 2.0.4 命令码对齐、反向数值唯一性与 520B/534B 容量静态门禁 (`static_checks/minimcproto/check_opcode_alignment.py`)**：
   - 覆盖 `soc-ap`、`mcu-p3(MC)`、`mcu-p3(TH)`、`boot/bootloadermc`、`boot/bootloaderth` 五端真实头文件。
   - 强制校验 `0x1D (CMD_SYSTEM_CONTROL)`、`0x20 (CMD_OTA_START)`、`0x21 (CMD_OTA_DATA)`、`0x22 (CMD_OTA_FINISH)`、`0x23 (CMD_OTA_STATUS)`、`0x15 (CMD_TEMP_REPORT)`、`0x17 (CMD_EMERGENCY_STOP)`、`0x19 (CMD_FILAMENT_CONTROL)` 跨端一致，禁用 `0x05 (ESTOP_ACK)` 及 `0x15 (FILAMENT_CONTROL)` 漂移。
   - 内置反向数值唯一性断言与 4 类负例自检（`0x05` 复辟、`0x15` 错配、`0x1D` 数值碰撞、`< 520B` 载荷上限）。
2. **`G01 ~ G25` 黄金字节向量集与编解码校验 (`static_checks/minimcproto/golden_vectors.json`, `reference_vectors.py`, `run_codec_cases.py`)**：
   - 固化 `G01 ~ G25`（含 `G16a` 144B `0x20 CMD_OTA_START` + 128B `ATSG` Trailer、`G16b~G16e` `64B/512B/37B/1016B` `0x21 CMD_OTA_DATA`、`G16f` `0x22`、`G16g~G16h` `0x23`、`G09~G15` 畸形帧负例、`G17~G25` `0x06 CMD_NACK` 标准错误码）及 `V01 ~ V04` 遥测/急停向量。
3. **五类软件验证矩阵执行器 (`static_checks/minimcproto/run_ota_software_suite.py`)**：
   - 自动执行并输出 `S01 ~ S04`（静态与编译期门禁）、`D01 ~ D08`（编解码黄金向量）、`C01 ~ C09`（跨五端 C 主机单测与契约联动）、`M01 ~ M08`（双 MCU 级联升级、断电保护与 `95%/100%` 阶段隔离）、`N01 ~ N10`（坏 Trailer/错 `board_id`/超限零擦除拒绝、并发锁、中途断流恢复）共 39 项门禁。
4. **OTA 打包/部署工具与 `SEQ-06` 端到端验收测试 (`hil/tools/hil_deploy_via_minimc_ota.py`, `hil/tests/test_mcu_firmware_upgrade.py`, `hil/twin_capture/twin_capture_analyzer.py`, `hil/tools/debug_reconciliation_probe.py`)**：
   - 实现 128B `ATSG` Trailer 打包/校验器、先 `TH (0x03)` 后 `MC (0x02)` 四阶段受控升级客户端，以及 `HIL-CASE-60 ~ HIL-CASE-63` 自检套件。

## 3. 自检命令与客观输出

执行命令：
```bash
cd test_harness && python3 static_checks/minimcproto/check_opcode_alignment.py \
  && python3 static_checks/minimcproto/run_codec_cases.py \
  && python3 static_checks/minimcproto/run_ota_software_suite.py \
  && python3 hil/tests/test_mcu_firmware_upgrade.py --self-test
```

结果摘要（`Exit Code: 0`）：
- `check_opcode_alignment.py`: `[PASS] MiniMCProto v2.0 (Rev 2.0.4) 5-endpoint opcode alignment, reverse uniqueness, >=520B payload capacity, and negative self-tests verified.`
- `run_codec_cases.py`: `[SUMMARY] Golden & Reference Codec Suite: 42 passed, 0 failed.`
- `run_ota_software_suite.py`: `[SUMMARY] OTA Software Suite: 39 passed, 0 failed.` (`S01~S04`, `D01~D08`, `C01~C09`, `M01~M08`, `N01~N10` 全部通过)
- `test_mcu_firmware_upgrade.py --self-test`: `[SUMMARY] SEQ-06 Upgrade Suite: 4/4 passed.` (`HIL-CASE-60 ~ HIL-CASE-63` 全部通过)
