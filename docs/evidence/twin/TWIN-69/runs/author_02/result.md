---
task_id: TWIN-69
task_revision: 2
run_id: author_02
role: INTEGRATOR
agent_id: cc065151-7c24-4606-b449-e03a5e7c2eba
status: Completed
date: 2026-11-07
target_repository: test_harness
branch: main
base_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
previous_candidate_commit: 54231c8d4372998bb91aefc3ec2df5c99169b274
candidate_commit: a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7
cross_repo_baseline:
  project-control: b764378b4d3232d1c7ce77fd4922f520dd31ef51
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
  test_harness: a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
---

# `TWIN-69` (`revision: 2`, `run_id: author_02`) 闭环整改与跨仓联调回执

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
| 9 | `project-control/docs/evidence/twin/TWIN-69/runs/qa_01/qa_review_report.md` | `project-control@b764378b` (`qa_01`) | `1b6f1ac4a6d0f62894ca4bf58f7184f52e85332012d3c75f52f0116898df9fae` | 首轮独立 Codex QA 审阅报告（`01a1b3bd-c81f-78c2-8297-6b47b30e9e87`）；无缺项 |

## 2. 针对 `qa_01` 审阅意见的逐项闭环整改说明

| `qa_01` 审阅意见 | 级别 | `author_02` 整改措施与落点 |
| --- | --- | --- |
| **1. CLI `--th-pkg`/`--mc-pkg` 部署分支未实际使用 `--port` 与 `--baud` 发起串口通信** | **阻断项** | 1. 在 `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` 中使用 Python 标准库（`os`、`termios`、`select`、`time`）实现真实串口/PTY 硬件通信类 **`SerialOtaTarget(port: str, baud: int = 921600, timeout_s: float = 1.2)`** 与 `_configure_serial_port(fd, baud)`（`8N1` raw mode、波特率映射、基于 `select` 的非阻塞发送与 `0x55 0xAA` 12B 帧头定界接收 `exchange_frame()`）；<br>2. 在 `_run_cli_package_upgrade(args)` 中，当传入 `--th-pkg` / `--mc-pkg` 且 `args.port != "virtual"`（非 `--dry-run`）时，**强制实例化 `SerialOtaTarget(args.port, args.baud)`** 打开真实串口或 PTY 设备执行先 TH 后 MC 四阶段升级，并在 `--receipt-out` 生成的 JSON 回执中记录 `"transport": "serial", "port": args.port, "baud": args.baud`；<br>3. 在 `test_harness/hil/tests/test_mcu_firmware_upgrade.py` 的 `HIL-CASE-64` 中新增 `_verify_pty_serial_cli_deploy()` 与 `_pty_bridge_loop()`，使用 `pty.openpty()` 创建真实内核主从伪终端（`/dev/pts/*`），通过 CLI 传入 `--port <slave_path> --baud 921600 --chunk-size 512 --th-pkg <fw_th.bin> --mc-pkg <fw_mc.bin> --receipt-out <receipt.json>`，端到端验证 `SerialOtaTarget` 真实串口文件描述符读写、`76,896 B` TH 固件 `151` 块传输与 JSON 回执落盘 100% 通过。 |
| **2. 非法 `--chunk-size` 预期拒绝日志使用 `[FAIL]` 前缀易与测试失败混淆** | 非阻断建议 | 已将 `main()` 中非法 `--chunk-size`（`<= 0` 或 `> 512`）的拒绝提示前缀统一改为 **`[EXPECTED-REJECT] invalid --chunk-size=...`**。 |

## 3. 交付产物与候选提交绑定

- **`test_harness` 仓库状态**：
  - 分支：`main`
  - `base_commit`：`cf81195eca55bcd772ef2daa2fd4aa41634c1492`
  - `candidate_commit`：**`a43d8540bf3bbfb2d6f3c7a7f3b56a6cc1def1e7`**（已推送至 `origin/main`）

| 交付文件路径 | 修改后 SHA-256 | 变更内容摘要 |
| --- | --- | --- |
| `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` | `a099afaccf61f297f4df2b8c9c0567acfc12d0be3792a7babec1299fff40ed2d` | 实现 `_configure_serial_port()`、`SerialOtaTarget`（`__init__`、`close`、`_read_until_len`、`exchange_frame`）、`_query_node_version()` 复位窗口重试、`_run_cli_package_upgrade()` 真实串口部署入口及 `[EXPECTED-REJECT]` 提示前缀。全部函数严格满足 `<=50` 行、`<=4` 参数、中文 docstring 与行内 `#` 中文注释。 |
| `test_harness/hil/tests/test_mcu_firmware_upgrade.py` | `1a34b08925dada94988baa625f3c9c11b15bf43247df238071eb40e95b255864` | 新增 `_pty_bridge_loop()` 与 `_verify_pty_serial_cli_deploy()`，在 `HIL-CASE-64` 及 `TestMcuFirmwareUpgradeSuite` 中通过真实内核 `pty.openpty()` 验证 CLI `--port /dev/pts/* --baud 921600 --chunk-size 512 --th-pkg ... --mc-pkg ... --receipt-out ...` 完整串口升级闭环。 |
| `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594` | `revision: 5`，对齐默认 `--chunk-size 512`（`76,896 B` TH 固件 `151` 块）与 `0xE0080423` `Bits 16..23=0x08 (Bit19=1) 512B 最大分块` 说明。 |

## 4. 跨仓整体联调与自检验证记录（`mcu-p3@97c1c24` + `test_harness@a43d854`）

| 序号 | 验证命令 | 退出码 | 关键结果摘要 |
| --- | --- | --- | --- |
| 1 | `sh ../mcu-p3/motion-controller-mcu/tests/run_tests.sh` | `0` | 10 项 `TWIN-44/47/60` MC 回归、`test_mc_ota_and_relay`（534B 级联代理 + 防下溢）及 MC `S04` 门禁全部 `PASS`。 |
| 2 | `python3 hil/tools/hil_deploy_via_minimc_ota.py --self-test` | `0` | `[PASS] hil_deploy_via_minimc_ota.py self-test passed: chunk_size=512B, TH(76896B/151 chunks, 1.1->2.1) then MC(1.2->2.3).` |
| 3 | `python3 hil/tests/test_mcu_firmware_upgrade.py --self-test` | `0` | `HIL-CASE-60 ~ HIL-CASE-64` **5/5 passed**（含 `serial PTY(/dev/pts/12@921600) TH=151 chunks/76896B` 真实串口部署验证）。 |
| 4 | `python3 -m unittest discover -s hil/tests -p "test_mcu_firmware_upgrade.py" -v` | `0` | `Ran 5 tests in 0.368s — OK`。 |
| 5 | `python3 static_checks/minimcproto/run_ota_software_suite.py` | `0` | `S01~S04 / D01~D08 / C01~C09 / M01~M08 / N01~N10` 共 **39 passed, 0 failed**（`S04` 函数行数、入参、中文注释与 docstring 门禁 100% 通过）。 |
