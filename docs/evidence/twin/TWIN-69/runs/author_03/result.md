---
task_id: TWIN-69
task_revision: 3
run_id: author_03
role: INTEGRATOR
agent_id: cc065151-7c24-4606-b449-e03a5e7c2eba
status: Completed
date: 2026-11-07
target_repository: test_harness
branch: main
base_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
previous_candidate_commit: a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7
candidate_commit: d5e9faa8b297a6e6069ba588a461e824bc63cfd1
cross_repo_baseline:
  project-control: b764378b4d3232d1c7ce77fd4922f520dd31ef51
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
  test_harness: d5e9faa8b297a6e6069ba588a461e824bc63cfd1
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
---

# `TWIN-69` (`revision: 3`, `run_id: author_03`) 闭环整改与跨仓联调回执

## 1. 规则与任务输入阅读回执 (`read_sources`)

| 序号 | 路径 | 来源仓库 / 版本 | SHA-256 | 适用环境与缺项核对 |
| --- | --- | --- | --- | --- |
| 1 | `project-control/.agents/rules/repository_rule_sources.json` | `project-control@b764378b` | `cb56bda30747360eb6057758f181bc9b031662178d1d9fe9eac6d462c89c9e74` | 宿主机/Docker 软件验证；无缺项 |
| 2 | `project-control/.agents/rules/repository_rule_boundaries.md` | `project-control@b764378b` | `023c5e092e1e056e049406cb089d17eee7efc3f069feee649ec6fb8f9b8fcdca` | 宿主机/Docker 软件验证；无缺项 |
| 3 | `test_harness/AGENTS.md` | `test_harness@cf81195e` | `b0e9dc4f66dee01b8741c3e9f16c26f627c49a57444d56094528d68bc5b0010a` | `test_harness` 仓库级边界；无缺项 |
| 4 | `test_harness/.agents/rules/shared/SOURCE.json` | `test_harness@cf81195e` (PC `17e0887d`) | `1374a577024258269e39b6181ced780662849044df52a57bfb78355640ac018a` | `test_harness` 共享规则快照；无缺项 |
| 5 | `project-control/.agents/rules/code_documentation_standard.md` | `project-control@b764378b` (v1.1) | `975a181cf7a3af82a47b030698a886af0bb420ea380d059f5b9eeaedc35193b9` | 全语言中文注释与 docstring 规范；无缺项 |
| 6 | `project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md` | `project-control@b764378b` (rev 1) | `b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76` | ARCH 权威技术拆解 §3 (`TWIN-69`)；无缺项 |
| 7 | `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` | `project-control@b764378b` (`Rev 2.0.4`) | `ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c` | 协议主规范（`520B` MTU / `512B` 最大分块）；无缺项 |
| 8 | `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `project-control@b764378b` (rev 5) | `138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594` | 双 MCU 升级操作与 HIL 部署说明书（`revision: 5`）；无缺项 |
| 9 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-69.md` | `project-control@b764378b` (rev 2) | `4dc107bd527b0e254eb4ecd796d95fa5efe7bfeac5897099d9d51b18f154ca7d` | 任务卡定义与范围边界；无缺项 |
| 10 | `project-control/docs/evidence/twin/TWIN-69/runs/qa_01/qa_review_report.md` | `project-control@b764378b` (`qa_01`) | `1b6f1ac4a6d0f62894ca4bf58f7184f52e85332012d3c75f52f0116898df9fae` | 首轮独立 Codex QA 审阅报告；无缺项 |
| 11 | `project-control/docs/evidence/twin/TWIN-69/runs/qa_02/qa_review_report.md` | `project-control@b764378b` (`qa_02`) | `6d58a3509f4c74bbe391478d3263316d938234e1fd5ab4d97f5dcc3cb87bb34e` | 二轮独立 Codex QA 审阅报告（`01a1b3c6-dd3e-7f50-ac68-cbe0da85dfa0`）；无缺项 |

## 2. 针对 `qa_02` 审阅意见的逐项闭环整改说明

| `qa_02` 审阅意见 | 级别 | `author_03` 整改措施与落点 |
| --- | --- | --- |
| **1. `_configure_serial_port()` 仅映射 5 个波特率，其他波特率静默回退至 `921600`/`115200` 且回执仍记录用户请求值；PTY 正向证据只覆盖 `921600`** | **阻断项** | 1. 在 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 中新增显式支持白名单 `SUPPORTED_POSIX_BAUDS = (9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000)` 与 `_resolve_posix_baud_constant(baud: int) -> int`，通过白名单校验与 `getattr(termios, f"B{baud}", None)` 精确解析 POSIX 波特率常量，**彻底移除任何默认回退**；若传入不支持或当前平台不存在的波特率（如 `12345` 或 `<= 0`），立即抛出 `ValueError`；<br>2. 在 `main()` CLI 入口处显式调用 `_resolve_posix_baud_constant(args.baud)`，对非法 `--baud` 打印 `[EXPECTED-REJECT] invalid --baud=...` 并以退出码 `2` 拒绝；<br>3. 在 `_configure_serial_port(fd, baud)` 执行 `termios.tcsetattr(fd, termios.TCSANOW, attrs)` 后，立即调用 `verify_attrs = termios.tcgetattr(fd)` 校验 `verify_attrs[4] == b_const and verify_attrs[5] == b_const`，若不一致则抛出 `RuntimeError`，确保回执记录的 `baud` 与内核实际生效波特率严格一致；<br>4. 在 `test_harness/hil/tests/test_mcu_firmware_upgrade.py` 的 `_verify_pty_serial_cli_deploy()` 中，每次测试前先将 `slave_fd` 预设为相异初始波特率（如 `B9600`），分别以 `--baud 921600` 和 `--baud 57600` 执行真实 PTY CLI 升级，并在升级后回读 `termios.tcgetattr(slave_fd)` 断言内核 `ispeed`/`ospeed` 均精确切换为请求速率常量，同时增加 `--baud 12345` 负向拒绝断言（返回码 `2`）。 |
| **2. PTY 测试核对了 TH 的 151 块和字节数及双包升级成功状态，但未断言 MC 的分块数和字节数** | 非阻断建议 | 1. 在 `hil_deploy_via_minimc_ota.py` 的 `_build_upgrade_receipt()` 中完整输出 `th_chunks_sent`、`th_bytes_sent`、`th_final_version`、`mc_chunks_sent`、`mc_bytes_sent`、`mc_final_version`、`total_chunks`、`total_bytes` 及 `final_version`；<br>2. 在 `test_mcu_firmware_upgrade.py` 的 `_verify_pty_serial_cli_deploy()` 中对 `921600` 与 `57600` 两次真实 PTY 升级回执均完整断言：`th_chunks_sent == 151`、`th_bytes_sent == 76896`、`mc_chunks_sent == 4`、`mc_bytes_sent == 2048`、`total_chunks == 155`、`total_bytes == 78944`、`chunk_size == 512`、`final_version == "TH=2.6,MC=2.7"`。 |

## 3. 交付产物与候选提交绑定

- **`test_harness` 仓库状态**：
  - 分支：`main`
  - `base_commit`：`cf81195eca55bcd772ef2daa2fd4aa41634c1492`
  - `previous_candidate_commit`：`a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7`
  - `candidate_commit`：**`d5e9faa8b297a6e6069ba588a461e824bc63cfd1`**（已推送至 `origin/main`）

| 交付文件路径 | 修改后 SHA-256 | 变更内容摘要 |
| --- | --- | --- |
| `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` | `3978eed6964b4dd6a808002adb996f231b9c6f972c50ee2c506b5d80dfd13e0a` | 新增 `SUPPORTED_POSIX_BAUDS`、`_resolve_posix_baud_constant()`（零回退校验）、`_configure_serial_port()` 内核 `tcgetattr` 回读校验、`_build_upgrade_receipt()`（含 TH/MC/汇总全字段）及 `main()` 非法 `--baud` 拒绝出口。全部函数严格满足 `<=50` 行、`<=4` 参数、中文 docstring 与行内 `#` 中文注释。 |
| `test_harness/hil/tests/test_mcu_firmware_upgrade.py` | `85e5b4a9dbaf170175c7cca8f0ca6aa674e0944c20ff5bd6d356ee5c208196d7` | 升级 `_verify_pty_serial_cli_deploy(th_pkg, mc_pkg, baud)` 与 `HIL-CASE-64`，覆盖真实内核 PTY 在 `921600` 与 `57600` 下的 `tcgetattr` 生效校验、TH (`151` 块 / `76896 B`) + MC (`4` 块 / `2048 B`) + 汇总 (`155` 块 / `78944 B`) 全字段回执断言，以及非法 `--baud 12345` 拒绝测试。 |
| `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594` | `revision: 5`，对齐默认 `--chunk-size 512`（`76,896 B` TH 固件 `151` 块）与 `0xE0080423` `Bits 16..23=0x08 (Bit19=1) 512B 最大分块` 说明。 |

## 4. 跨仓整体联调与自检验证记录（`mcu-p3@97c1c24` + `test_harness@d5e9faa`）

| 序号 | 验证命令 | 退出码 | 关键结果摘要 |
| --- | --- | --- | --- |
| 1 | `sh ../mcu-p3/motion-controller-mcu/tests/run_tests.sh` | `0` | 10 项 `TWIN-44/47/60` MC 回归、`test_mc_ota_and_relay`（534B 级联代理 + 防下溢）及 MC `S04` 门禁全部 `PASS`。 |
| 2 | `python3 hil/tools/hil_deploy_via_minimc_ota.py --self-test` | `0` | `[PASS] hil_deploy_via_minimc_ota.py self-test passed: chunk_size=512B, TH(76896B/151 chunks, 1.1->2.1) then MC(1.2->2.3).` |
| 3 | `python3 hil/tests/test_mcu_firmware_upgrade.py --self-test` | `0` | `HIL-CASE-60 ~ HIL-CASE-64` **5/5 passed**（含 `PTY(@921600)`、`PTY(@57600)` 内核 `tcgetattr` 速率生效校验、TH 151块/MC 4块完整回执断言及 `--baud=12345` 拒绝断言）。 |
| 4 | `python3 -m unittest discover -s hil/tests -p "test_mcu_firmware_upgrade.py" -v` | `0` | `Ran 5 tests in 0.552s — OK`。 |
| 5 | `python3 static_checks/minimcproto/run_ota_software_suite.py` | `0` | `S01~S04 / D01~D08 / C01~C09 / M01~M08 / N01~N10` 共 **39 passed, 0 failed**（`S04` 函数行数、入参、中文注释与 docstring 门禁 100% 通过）。 |
