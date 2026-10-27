# 单票实际执行记录: V2-P0506 (Run 1)

```yaml
task_id: V2-P0506
task_revision: 1
actual_run_id: run_20261027_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p0506_20261027_01
start_time: "2026-10-27T09:45:00+08:00"
end_time: "2026-10-27T09:51:00+08:00"
start_end_time: "2026-10-27T09:45:00+08:00 ~ 2026-10-27T09:51:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 79be851016c62e31b041700b4cd200a488a8eade
workspace_diff_sha256: b8f9de456024a9f6309cb4b0a59cac945b002678cfa7a2b272493bb077438e41
input_versions:
  - predecessor_task: V2-P05B
    accepted_version: "sha256:4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "79be851016c62e31b041700b4cd200a488a8eade"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
  - repo: project-control
    commit: "92ca46d485bfaa8065fdabc994c75a88dcad16bd"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "CMakeLists.txt (+42 lines), core/forward/minimc/parser.cpp (+263, -75 lines)"
  project_control_diff: "docs/releases/minimc_v2_offline_candidate.yaml, docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/**"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:48:32+08:00"
    end_time: "2026-10-27T09:48:32+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P0506 -G Ninja -DCMAKE_BUILD_TYPE=Debug -DMINIMC_QA_ROOT=\"$PWD/test_harness\""
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:49:57+08:00"
    end_time: "2026-10-27T09:49:57+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/02_cmake.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P0506"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:50:02+08:00"
    end_time: "2026-10-27T09:50:02+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_recovery_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506/bin/minimc-probe --case-set recovery"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:50:07+08:00"
    end_time: "2026-10-27T09:50:07+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/04_focused_recovery_cases.log
    actual_case_count: 4
    warning_count: 0
  - id: registered_tests
    command: "cd /tmp/ai_soc_v2_build/V2-P0506 && ctest -N"
    cwd: /tmp/ai_soc_v2_build/V2-P0506
    start_time: "2026-10-27T09:50:11+08:00"
    end_time: "2026-10-27T09:50:11+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/05_registered_tests.log
    actual_case_count: 11
    warning_count: 0
  - id: ctest_all
    command: "cd /tmp/ai_soc_v2_build/V2-P0506 && ctest --output-on-failure"
    cwd: /tmp/ai_soc_v2_build/V2-P0506
    start_time: "2026-10-27T09:50:16+08:00"
    end_time: "2026-10-27T09:50:16+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/06_ctest_all.log
    actual_case_count: 11
    warning_count: 0
  - id: run_all_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506/bin/minimc-probe --case-set all"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:50:20+08:00"
    end_time: "2026-10-27T09:50:20+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/07_run_all_cases.log
    actual_case_count: 60
    warning_count: 0
  - id: check_task_graph
    command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P0506"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T09:50:37+08:00"
    end_time: "2026-10-27T09:50:38+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/08_check_task_graph.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P0506 -G Ninja -DCMAKE_BUILD_TYPE=Debug -DMINIMC_QA_ROOT=\"$PWD/test_harness\""
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P0506"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506/bin/minimc-probe --case-set recovery"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cd /tmp/ai_soc_v2_build/V2-P0506 && ctest -N"
    cwd: /tmp/ai_soc_v2_build/V2-P0506
    exit_code: 0
  - command: "cd /tmp/ai_soc_v2_build/V2-P0506 && ctest --output-on-failure"
    cwd: /tmp/ai_soc_v2_build/V2-P0506
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P0506/bin/minimc-probe --case-set all"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P0506"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/02_cmake.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/03_build.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/04_focused_recovery_cases.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/05_registered_tests.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/06_ctest_all.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/07_run_all_cases.log
  - docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/08_check_task_graph.log
candidate_commit: null
candidate_commit_or_diff_sha256: "b8f9de456024a9f6309cb4b0a59cac945b002678cfa7a2b272493bb077438e41"
candidate_diff_sha256: "b8f9de456024a9f6309cb4b0a59cac945b002678cfa7a2b272493bb077438e41"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/parser.cpp
    size: 7382
    sha256: 4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b
  - path: soc-ap/CMakeLists.txt
    size: 2516
    sha256: acf7197951385bdc93d09b2b3a9928cf4d62675e4b3aba74d492cfaef6daaeac
  - path: project-control/docs/releases/minimc_v2_offline_candidate.yaml
    size: 1913
    sha256: e5728fccdc5983c5761b481661d1fc72f6e4a879d40d7f142f1e4da5eca461ab
actual_cases:
  - "REC-001: 遭遇坏CRC帧立即自愈丢弃并顺利分发后继合法V01帧 (通过)"
  - "REC-002: 遭遇L=1025超MTU帧头立即自愈丢弃并顺利分发后继合法V02入站帧 (通过)"
  - "REC-003: 遭遇非v2.0错误协议版本帧静默丢弃并顺利分发后继合法V01帧 (通过)"
  - "REC-004: 复合数据流(有效V01->前导噪声->坏CRC->帧截断+60ms超时->有效V03)完全自愈分发 (通过)"
  - "CTest targets (11/11): host_runtime_smoke, minimc_reference, minimc_crc, minimc_encode, minimc_decode_bounds, minimc_decode, minimc_stream_sync, minimc_stream_header, minimc_stream_payload, minimc_timeout, minimc_recovery 全部 100% 通过"
  - "All functional cases (60/60): crc(9), encode(8), decode_bounds(6), decode(12), stream_sync(5), stream_header(5), stream_payload(5), timeout(6), recovery(4) 全部通过退出码 0"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 CTest/全量60用例执行记录的独立评审"
reviewed_version: null
review_decision: null
independent_review:
  reviewer_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
  reviewed_artifact_version: null
  report_path: null
  report_sha256: null
  decision: null
handoff:
  receiver_session: 9e5411f4-acad-421e-b487-9e68b9483320
  acknowledgement_path: null
  decision: null
handoff_ack: null
```

---

## 交付正文与执行报告

### 1. 本票实际修改与交付物

本合并微步任务卡 `V2-P0506`（合并原包 5 剩余逻辑与包 6 离线集成及归档）由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **交付物 1**: `soc-ap/core/forward/minimc/parser.cpp`
   - SHA256: `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b`
   - 大小: `7,382` 字节 (238 行)
   - 编码规范合规：
     - **函数规模硬性门禁**：所有自研函数均拆解为单一职责子函数，每一个函数严格控制在 50 行以内（最大函数 48 行）；
     - **入参个数硬性门禁**：所有内部静态辅助函数入参均严格控制在 4 个以内（超参封装为 `DispatchSink*`）；
     - **内存安全与指针显式化**：零动态堆内存分配（无 `new`, `malloc`），严禁压缩指针运算，数组下标显式递增；
     - **超时判定先检后刷铁律**：`parser_feed_byte` 入口第一行执行 Guard 校验，随后在状态非 `WAIT_SOF1` 时执行 `(now_ms - last_byte_rx_ms) > 50` 判定，超时则递增 `err_timeout` 并复位至 `WAIT_SOF1`，随后以新状态处理当前字节；
     - **定时轮询**：`parser_poll_timeout` 对处于非空闲状态的解析器执行 50ms 超时复位，空闲状态幂等返回 `false`；
     - **自愈恢复能力**：无论遇到 CRC 错误、超限 MTU、非法协议版本或字节流截断，解析器均能递增相应诊断计数并安全重置回 `WAIT_SOF1`，顺利接收并分发后续合法帧。

2. **交付物 2**: `soc-ap/CMakeLists.txt`
   - SHA256: `acf7197951385bdc93d09b2b3a9928cf4d62675e4b3aba74d492cfaef6daaeac`
   - 大小: `2,516` 字节 (78 行)
   - 遵从 `soc-ap/contracts/minimcproto/test-probe.md` 规则：
     - 支持通过 `-DMINIMC_QA_ROOT=<path>` 引入独立 QA 测试套件；
     - 缺失测试脚本或样例时执行 `message(FATAL_ERROR ...)` 防御报错；
     - 注册 1 个既有 Smoke: `host_runtime_smoke`；
     - 注册 1 个静态黄金参考测试: `minimc_reference`；
     - 分别注册 9 个真实功能组测试目标: `minimc_crc`, `minimc_encode`, `minimc_decode_bounds`, `minimc_decode`, `minimc_stream_sync`, `minimc_stream_header`, `minimc_stream_payload`, `minimc_timeout`, `minimc_recovery`；
     - CTest `-N` 总数精确为 11 项。

3. **交付物 3**: `project-control/docs/releases/minimc_v2_offline_candidate.yaml`
   - SHA256: `e5728fccdc5983c5761b481661d1fc72f6e4a879d40d7f142f1e4da5eca461ab`
   - 包含完整的离线版本元数据：`candidate_id`, `scope`, `repositories`, `protocol` (校验 sha256: `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`), `verification`, `limitations`, `handoff`。

### 2. 验证与回归结果汇总

- **focused_recovery_cases (REC-001 ~ REC-004)**: 4/4 100% 全部通过（退出码 0）。
- **registered_tests (ctest -N)**: 11/11 目标全部精确注册（1 个 host smoke + 10 个 minimc_*）。
- **ctest_all (ctest --output-on-failure)**: 11/11 目标全部 100% 运行通过（0 错误 0 告警，退出码 0）。
- **run_all_cases (全量 9 组功能用例)**: 60/60 全部 100% 通过（0 失败 0 错误，退出码 0）。
- **check_task_graph**: 静态依赖图、代码行数/入参门禁、候选清单元数据核验全部通过（0 错误，退出码 0）。

### 3. 执行证据与原始日志

- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/01_precheck.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/02_cmake.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/03_build.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261026_01/04_focused_recovery_cases.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/05_registered_tests.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/06_ctest_all.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/07_run_all_cases.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/08_check_task_graph.log`
- `docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/result.md`

### 4. 边界合规与提审申请

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`codec.*`、`parser.h` 或 `project-control/.agents/**`。
- 本票执行完毕，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡推进至 `Review` 并指派独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查与签署。
