---
task_id: TWIN-69
task_revision: 1
run_id: author_01
role: INTEGRATOR
agent_id: cc065151-7c24-4606-b449-e03a5e7c2eba
status: Completed
date: 2026-11-07
target_repository: test_harness
branch: main
base_commit: cf81195eca55bcd772ef2daa2fd4aa41634c1492
candidate_commit: 54231c8d4372998bb91aefc3ec2df5c99169b274
cross_repo_baseline:
  project-control: 33de1d299452a09d90f7e1f568d740903429cb83
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
  test_harness: 54231c8d4372998bb91aefc3ec2df5c99169b274
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
---

# `TWIN-69` (`revision: 1`, `run_id: author_01`) 执行与跨仓联调回执

## 1. 规则与任务输入阅读回执 (`read_sources`)

| 序号 | 路径 | 来源仓库 / 版本 | SHA-256 | 适用环境与缺项核对 |
| --- | --- | --- | --- | --- |
| 1 | `project-control/.agents/rules/repository_rule_sources.json` | `project-control@33de1d29` | `cb56bda30747360eb6057758f181bc9b031662178d1d9fe9eac6d462c89c9e74` | 宿主机/Docker 软件验证；无缺项 |
| 2 | `project-control/.agents/rules/repository_rule_boundaries.md` | `project-control@33de1d29` | `023c5e092e1e056e049406cb089d17eee7efc3f069feee649ec6fb8f9b8fcdca` | 宿主机/Docker 软件验证；无缺项 |
| 3 | `test_harness/AGENTS.md` | `test_harness@cf81195e` | `b0e9dc4f66dee01b8741c3e9f16c26f627c49a57444d56094528d68bc5b0010a` | `test_harness` 仓库级边界；无缺项 |
| 4 | `test_harness/.agents/rules/shared/SOURCE.json` | `test_harness@cf81195e` (PC `17e0887d`) | `1374a577024258269e39b6181ced780662849044df52a57bfb78355640ac018a` | `test_harness` 共享规则快照；无缺项 |
| 5 | `project-control/.agents/rules/code_documentation_standard.md` | `project-control@33de1d29` (v1.1) | `975a181cf7a3af82a47b030698a886af0bb420ea380d059f5b9eeaedc35193b9` | 全语言中文注释与 docstring 规范；无缺项 |
| 6 | `project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md` | `project-control@33de1d29` (rev 1) | `b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76` | ARCH 权威技术拆解 §3 (`TWIN-69`)；无缺项 |
| 7 | `project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md` | `project-control@33de1d29` (`Rev 2.0.4`) | `ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c` | 协议主规范（`520B` MTU / `512B` 最大分块）；无缺项 |
| 8 | `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `project-control@33de1d29` (rev 4 -> rev 5) | `6be279c98f96972925a5da39b2d88cb1ffecafe3cedd69d957779933afe7fb56` (修改前) | 双 MCU 升级操作与 HIL 部署说明书；无缺项 |
| 9 | `project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-69.md` | `project-control@33de1d29` (rev 1) | `067c79805b77e3089e7b7f475492cbef0d151f2318746999a578863dba4dda7e` | `TWIN-69` 正式任务卡契约；无缺项 |

## 2. 交付产物与候选提交绑定

- **`test_harness` 仓库状态**：
  - 分支：`main`
  - `base_commit`：`cf81195eca55bcd772ef2daa2fd4aa41634c1492`
  - `candidate_commit`：`54231c8d4372998bb91aefc3ec2df5c99169b274`（已推送至 `origin/main`）

| 交付文件路径 | 修改后 SHA-256 | 变更内容摘要 |
| --- | --- | --- |
| `test_harness/hil/tools/hil_deploy_via_minimc_ota.py` | `fcc8045fb231e3dfbd4847a11b4a236d3376e6284b2d5b3aaaae0965657a780d` | 1. 导出协议常量 `TH_BOOT_CAPABILITY = 0xE0080423`、`MC_BOOT_CAPABILITY = 0xC0080435`、`DEFAULT_OTA_CHUNK_SIZE = 512`、`MAX_OTA_CHUNK_SIZE = 512`、`MIN_OTA_CHUNK_SIZE = 64`、`TH_BOOT_CAPABILITY_MAX_CHUNK = 512`、`MC_BOOT_CAPABILITY_MAX_CHUNK = 512`；<br>2. 在 `_stage2_start_and_stream()` 与 `run_single_node_four_stage_upgrade()` / `run_ordered_th_then_mc_upgrade()` 中固化默认 `chunk_size = 512`，入口拦截非法 `chunk_size`（`<=0` 或 `>512`），支持首块 512B 填满时（`off==0` 或小分块累加满 `512B`）核验 `0x23` `chunk0_cached_observed`；<br>3. 在 `_build_cli_parser()` / `main()` 中完整支持 `--chunk-size`（默认 `512`）、`--port`、`--baud`、`--th-pkg`、`--mc-pkg`、`--receipt-out`，非法 `--chunk-size` 返回退出码 `2`；<br>4. 在 `run_builtin_selftest()` 中验证能力位 `512B` 解码及 `76,896 B` TH 净荷精确切分 `151` 块（`150 × 512B + 96B`）完成 Stage 1~4 闭环。 |
| `test_harness/hil/tests/test_mcu_firmware_upgrade.py` | `c18a3e05f200c9b73ea067614768966282d2ff349ec4f07216cc4bb6127186cb` | 导入 `DEFAULT_OTA_CHUNK_SIZE`、`MAX_OTA_CHUNK_SIZE`、`TH_BOOT_CAPABILITY_MAX_CHUNK`、`MC_BOOT_CAPABILITY_MAX_CHUNK`；新增 `HIL-CASE-64`（`verify_case64_default_512b_chunk_and_76896b_th_stream`）与 `TestMcuFirmwareUpgradeSuite(unittest.TestCase)`，覆盖 `512B` 常量/能力位解码、`76,896 B` TH 固件 `151` 块流式发送及非法 `chunk_size`（`0` 与 `513`）API/CLI 确定性拒绝。 |
| `project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md` | `138619495b389ff290a9dc97fb9c4b4391c4cbadf1a74f3b9fff103d50bf0594` | 升级至 `revision: 5`，增补修订表第 5 行；修正第 38 行 `TH Bootloader` `capability_flags = 0xE0080423` 位域说明为 `Bits 16..23=0x08 (Bit19=1) 512B 最大分块`；更新第 34 行与第 67 行默认分块参数为 `512B`（`--chunk-size 512`，`76,896 B` 共 `151` 块：`150 × 512B + 1 × 96B`，典型耗时 `15s~30s`），并在第 6 节保留 `TWIN-67` 64B (`1202` 块) 压力兼容实测记录。 |

## 3. 跨仓整体联调与自检验证记录（`TWIN-68` `mcu-p3@97c1c24` + `TWIN-69` `test_harness@54231c8`）

遵照串行联调门禁要求，基于 `mcu-p3@97c1c2422e98357e72cc822d2b5293b9e0c2abc6`（`TWIN-68` 已落盘提交）与 `test_harness@54231c8d4372998bb91aefc3ec2df5c99169b274`（`TWIN-69` 候选提交）执行全部 5 项跨仓整体联调命令：

| 序号 | 验证命令 | 退出码 | 关键结果摘要 |
| --- | --- | --- | --- |
| 1 | `sh /home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/tests/run_tests.sh` | `0` | `[1/3]` 10 项 `TWIN-44/47/60` MC 回归单测全部 `PASS`；`[2/3]` `test_mc_ota_and_relay`（含 `TWIN-64` 534B 级联代理 + `TWIN-68` `check_th_relay_timeout` 防下溢与回绕单测）`PASS`；`[3/3]` MC 零 `M997/5AA5` 残留与 `S04` 门禁（函数 `<=50` 行、入参 `<=4` 个、中文注释）`PASS`。 |
| 2 | `python3 /home/sushaohua/workspace/ai_soc_project/test_harness/static_checks/minimcproto/run_ota_software_suite.py` | `0` | 跨 5 端（`soc-ap@7184edf`、`mcu-p3@97c1c24`、`bootloadermc@faa2ed0`、`bootloaderth@64b7100`、`test_harness@54231c8`）全套 `S01~S04`、`D01~D08`、`C01~C09`、`M01~M08`、`N01~N10` 共 **39 passed, 0 failed**（含 `S04` 全部 8 个 Python 脚本函数 `<=50` 行、入参 `<=4` 个、中文 docstring 与行内 `#` 注释校验）。 |
| 3 | `python3 /home/sushaohua/workspace/ai_soc_project/test_harness/hil/tools/hil_deploy_via_minimc_ota.py --self-test` | `0` | `[PASS] hil_deploy_via_minimc_ota.py self-test passed: chunk_size=512B, TH(76896B/151 chunks, 1.1->2.1) then MC(1.2->2.3).` |
| 4 | `python3 /home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests/test_mcu_firmware_upgrade.py --self-test` | `0` | `HIL-CASE-60 ~ HIL-CASE-64` 共 **5/5 passed**（含 `DEFAULT_OTA_CHUNK_SIZE=512`、`0xE0080423/0xC0080435 -> 512B`、`76,896B = 151 chunks` 及非法 `chunk_size` `0`/`513` 确定性拦截）。 |
| 5 | `python3 -m unittest discover -s /home/sushaohua/workspace/ai_soc_project/test_harness/hil/tests -p "test_mcu_firmware_upgrade.py" -v` | `0` | `Ran 5 tests in 0.178s — OK`。 |
