# 单票实际执行记录: V2-P03F (Run 1 / `run_20261026_01`)

```yaml
task_id: V2-P03F
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
lease_id: lease_v2_p03f_20261026_01
start_end_time:
  start_time: "2026-10-26T20:19:04+08:00"
  end_time: "2026-10-26T20:24:00+08:00"
start_time: "2026-10-26T20:19:04+08:00"
end_time: "2026-10-26T20:24:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 59d2320663dd7ef4a080272d624f831684935c34
workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
input_versions:
  - predecessor_task: V2-P01D
    accepted_version: "sha256:a8664e5d461a960feaf4d28fc1e73e2fac5ebf568da202df552b849e2382d67a"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P01D/runs/run_20261026_01/arch_review_report.md"
  - predecessor_task: V2-P02C
    accepted_version: "sha256:0c05ad8ed92a48b0062772042ec8fa1e1ab79d71dfaf2746afa3efb08cd3b7b3"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P02C/runs/run_20261026_01/qa_review_report.md"
  - predecessor_task: V2-P03E
    accepted_version: "sha256:549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P03E/runs/run_20261026_01/qa_review_report.md"
  - vectors_path: test_harness/test_cases/minimcproto/vectors.json
    vectors_sha256: 6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995
  - protocol_path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    protocol_revision: 2.0.3
    protocol_sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  - repo: soc-ap
    commit: 25d8f99faf338b2d324a9793b33deaa423a57f9e
  - repo: test_harness
    commit: 59d2320663dd7ef4a080272d624f831684935c34
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "clean (HEAD 25d8f99faf338b2d324a9793b33deaa423a57f9e)"
  test_harness_diff: "test_harness/static_checks/minimcproto/run_codec_cases.py (new file, 938 lines, 35416 bytes)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/** (evidence logs and result.md)"
commands_cwd_exit_codes:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P03F -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P03F"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - id: runner_self_check
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --self-check"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - id: stub_runner
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P03F/bin/minimc-probe --case-set stub"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - id: host_regression
    command: "env -C /tmp/ai_soc_v2_build/V2-P03F ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P03F
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/02_configure.log
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/04_runner_self_check.log
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/05_stub_runner.log
  - docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/06_host_regression.log
candidate_commit_or_diff_sha256: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf (test_harness/static_checks/minimcproto/run_codec_cases.py)"
artifact_hashes:
  - path: test_harness/static_checks/minimcproto/run_codec_cases.py
    size: 35416
    lines: 938
    sha256: e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf
actual_cases:
  - "通过 --probe 指定 minimc-probe 可执行文件，消费固定样例集 vectors.json，逐 case 报告实际/预期与退出码"
  - "支持 stub 分组（STUB-001~STUB-004，共 4 个用例）及 9 个功能分组（crc, encode, decode_bounds, decode, stream_sync, stream_header, stream_payload, timeout, recovery，共 60 个用例）；--case-set all 仅运行 9 个功能分组，排除 stub"
  - "桩阶段运行 --case-set stub 时，4/4 用例（STUB-001 crc, STUB-002 encode, STUB-003 decode, STUB-004 feed）全部验证 exit_code == 126 且 status == 'error', error_code == 'not_implemented' 通过"
  - "功能分组对未实现后端（exit_code == 126 / error_code == 'not_implemented'）严格判 FAIL，绝不静默跳过或误判 PASS"
  - "运行器 --self-check 验证 7 条自身错误与异常防御路径（SELF-01 探针不存在退出 2、SELF-02 探针不可执行退出 2、SELF-03 未知分组名退出 2、SELF-04 空用例集违反 No Empty Test Pass 退出 2、SELF-05 子进程超时 0.1s 判失败退出 1、SELF-06 功能分组遇到 not_implemented 判失败退出 1、SELF-07 输出字段不匹配判失败退出 1），7/7 全部通过"
  - "既有宿主回归测试 host_runtime_smoke 1/1 通过，尚未实现的业务分组未在此阶段宣称通过"
warnings: []
failures_and_corrections:
  - "首次运行 --self-check 时，构造单用例测试集使用了 base_vectors['cases'][0]（实际为 STUB-001，group='stub'），导致按 group='crc' 筛选时触发空集保护返回退出码 2；随即将筛选改为 [c for c in base_vectors['cases'] if c.get('group') == 'crc'][:1]，重跑 --self-check 7/7 异常路径全部通过（仅 1 次有依据微调，预算上限 2 次内）"
reviewed_version: null
review_decision: null
handoff_ack: null
```

---

## 交付正文与执行报告

### 1. 本票实际修改与交付物

本微步任务卡 `V2-P03F` 由 `QA`（Session ID: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`）执行，严格限制在 `write_scope` 范围内：

1. **单一测试运行器交付物**: `test_harness/static_checks/minimcproto/run_codec_cases.py`
   - **SHA256**: `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf`
   - **大小 / 行数**: `35,416` bytes / `938` lines
   - **核心特性**:
     - **纯 Python 3 标准库实现**：仅使用 `argparse`, `copy`, `json`, `os`, `pathlib`, `struct`, `subprocess`, `sys`, `tempfile`, `typing`，零第三方依赖。
     - **单向预期权威**：严格只读加载 `test_harness/test_cases/minimcproto/vectors.json`，绝不从探针输出反向更新预期。
     - **完备子命令映射与结构化解析**：完整支持 `crc`（含 `--null-ptr --len`）、`encode`（含 `payload_pattern` 展开、`--null-payload`、`--payload-len`、`--buf-size`）、`decode`（含 `frame_pattern` 展开及 `V04` `OQ-01` 命令层冲突元数据核验）、`feed`（含 `byte_by_byte` 等步长模式、`chunks` 离散时间戳模式、`frame_pattern` 展开及 `--reset-after`）、`poll`（`--now-ms`）与 `reset`。
     - **防作弊与非空测试保护 (No Empty Test Pass)**：`--case-set all` 严格只运行 9 个功能分组（60 个用例），不包含 `stub`；若匹配用例数为 `0`、分组名未知、探针不存在或不可执行，立即报错并以退出码 `2` 退出；功能分组若遇到 `exit_code == 126` 或 `error_code: not_implemented`，立即判 `FAIL`（退出码 `1`）。
     - **自检模式 (`--self-check`)**：内置 7 项异常防御自检（`SELF-01`~`SELF-07`），覆盖缺探针、探针无执行权限、未知分组、空用例集、子进程超时、功能组未实现拒绝、输出值不匹配拒绝，实测 `tested_exception_paths_count: 7`，`7/7` 通过。

2. **验证命令与原始日志**:
   - `01_precheck.log`: `soc-ap` HEAD `25d8f99faf338b2d324a9793b33deaa423a57f9e`（干净），`test_harness` HEAD `59d2320663dd7ef4a080272d624f831684935c34`（干净）。
   - `02_configure.log`: CMake Ninja Debug 配置成功（退出码 `0`）。
   - `03_build.log`: 构建 `libminimcproto.a`、`bin/soc-ap`、`bin/minimc-probe` 成功，零警告（退出码 `0`）。
   - `04_runner_self_check.log`: `--self-check` 验证 7 项异常路径全部通过（退出码 `0`）。
   - `05_stub_runner.log`: `--case-set stub` 运行 `STUB-001`~`STUB-004` 共 4 个用例，全部验证 `exit_code == 126` 且 `error_code == "not_implemented"` 通过（退出码 `0`）。
   - `06_host_regression.log`: `host_runtime_smoke` 1/1 通过（退出码 `0`）。

### 2. 边界合规确认

- 未触碰 `soc-ap/**`、`mcu-p3/**`、`test_harness/test_cases/minimcproto/vectors.json` 或 `project-control/.agents/**`。
- 现提交父会话 `COORD` (`9e5411f4-acad-421e-b487-9e68b9483320`)，请指派独立审阅者 `ARCH` (`1c634be7-4be2-4743-af02-dc8ada31bad3`) 进行独立评审。
