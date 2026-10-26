# 单票实际执行记录: V2-P05C (Run 1)

```yaml
task_id: V2-P05C
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p05c_20261026_01
start_time: "2026-10-26T21:28:00+08:00"
end_time: "2026-10-26T21:33:00+08:00"
start_end_time: "2026-10-26T21:28:00+08:00 ~ 2026-10-26T21:33:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 79be851016c62e31b041700b4cd200a488a8eade
workspace_diff_sha256: 5ac5d413839263d1c18c61474a5421382967d4a434a41fde7b907bf940833375
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
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/parser.cpp (+46, -3 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:28:11+08:00"
    end_time: "2026-10-26T21:28:11+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05C -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:31:54+08:00"
    end_time: "2026-10-26T21:31:55+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/02_cmake.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P05C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:31:58+08:00"
    end_time: "2026-10-26T21:31:58+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_payload"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:32:01+08:00"
    end_time: "2026-10-26T21:32:02+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/04_stream_payload_cases.log
    actual_case_count: 5
    warning_count: 0
  - id: timeout_antigaming
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set timeout"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:32:08+08:00"
    end_time: "2026-10-26T21:32:09+08:00"
    actual_exit_code: 1
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/05_timeout_antigaming.log
    actual_case_count: 6
    warning_count: 0
  - id: stream_sync_regression
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:32:21+08:00"
    end_time: "2026-10-26T21:32:21+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/06_stream_sync_regression.log
    actual_case_count: 5
    warning_count: 0
  - id: stream_header_regression
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:32:24+08:00"
    end_time: "2026-10-26T21:32:24+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/07_stream_header_regression.log
    actual_case_count: 5
    warning_count: 0
  - id: host_smoke_regression
    command: "(cd /tmp/ai_soc_v2_build/V2-P05C && ctest --output-on-failure -R ^host_runtime_smoke$)"
    cwd: /tmp/ai_soc_v2_build/V2-P05C
    start_time: "2026-10-26T21:32:28+08:00"
    end_time: "2026-10-26T21:32:29+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/08_host_smoke_regression.log
    actual_case_count: 1
    warning_count: 0
  - id: check_task_graph
    command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P05C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:32:43+08:00"
    end_time: "2026-10-26T21:32:43+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/09_check_task_graph.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05C -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P05C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_payload"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set timeout"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 1
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05C/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "(cd /tmp/ai_soc_v2_build/V2-P05C && ctest --output-on-failure -R ^host_runtime_smoke$)"
    cwd: /tmp/ai_soc_v2_build/V2-P05C
    exit_code: 0
  - command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P05C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/02_cmake.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/04_stream_payload_cases.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/05_timeout_antigaming.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/06_stream_sync_regression.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/07_stream_header_regression.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/08_host_smoke_regression.log
  - docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/09_check_task_graph.log
candidate_commit: null
candidate_commit_or_diff_sha256: "5ac5d413839263d1c18c61474a5421382967d4a434a41fde7b907bf940833375"
candidate_diff_sha256: "5ac5d413839263d1c18c61474a5421382967d4a434a41fde7b907bf940833375"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/parser.cpp
    size: 5848
    sha256: 8f6a7037c130f94bffbb849be16953a5c998d11e5e81094b0d9149b348fb3e0c
actual_cases:
  - "SPLD-001: 逐字节接收 V01 (L=0, 14B) 帧，在 CRC 高字节到达时准确分发 1 帧 (通过)"
  - "SPLD-002: 多分段分块流式接收 V02 入站 (18B) 与 V02 出站 (18B) 连续帧，成功分发 2 帧 (通过)"
  - "SPLD-003: 接收最大 1024 字节载荷长帧 (1038B)，完整分发 1 帧且字段无截断 (通过)"
  - "SPLD-004: 仅接收 CRC 低字节时保持在 READ_CRC 状态，不提前分发帧 (通过)"
  - "SPLD-005: 接收错误 CRC 校验和的畸变帧，静默丢弃、递增 err_crc 并安全复位回 WAIT_SOF1 (通过)"
  - "TMO-001~TMO-006: timeout 未实现分组防作弊测试严格拦截退出码 1 (通过)"
  - "SYNC-001~SYNC-005: stream_sync 前置同步测试 5/5 100% 通过 (通过)"
  - "SHDR-001~SHDR-005: stream_header 前置帧头累积与长度门禁测试 5/5 100% 通过 (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过 (通过)"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 SPLD-001~SPLD-005 执行记录的独立评审"
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

本微步任务卡 `V2-P05C` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/parser.cpp`
   - 文件大小：`5,848` 字节 (173 行)
   - SHA256：`8f6a7037c130f94bffbb849be16953a5c998d11e5e81094b0d9149b348fb3e0c`
   - Git Diff SHA256: `5ac5d413839263d1c18c61474a5421382967d4a434a41fde7b907bf940833375`
   - 实现内容：
     - 在 `parser_feed_byte` 中实现 `ParserState::READ_PAYLOAD`：
       - 将载荷字节顺序存入 `parser->rx_buffer[parser->rx_index++] = byte;`，并刷新时间戳 `parser->last_byte_rx_ms = now_ms;`；
       - 当累积载荷到达 `parser->rx_index == parser->expected_len - 2` 时（载荷接收完毕），跃迁至 `parser->state = ParserState::READ_CRC;`；
       - 返回 `Status::OK;`（此时 `*out_frame_ready = false`）。
     - 在 `parser_feed_byte` 中实现 `ParserState::READ_CRC`：
       - **CRC 低字节**（`rx_index == expected_len - 2`）：存入 `rx_buffer`，刷新时间戳，保持在 `READ_CRC` 状态，返回 `Status::OK;`（`*out_frame_ready = false`）；
       - **CRC 高字节**（`rx_index == expected_len - 1`）：存入 `rx_buffer`，刷新时间戳，此时整帧接收齐备；
       - 调用已实现的结构校验与 CRC 校验函数 `decode_frame(Bytes(parser->rx_buffer, parser->expected_len), out_frame)`：
         - 若校验成功（返回 `Status::OK`）：
           - 置位分发标识 `*out_frame_ready = true;`；
           - 递增计数 `parser->dispatched_frames++;`；
         - 若校验失败（CRC 不匹配或格式异常）：
           - 递增错误计数 `parser->err_crc++;`；
           - 置位 `*out_frame_ready = false;`；
         - 无论成功或失败，重置状态机至 `WAIT_SOF1`（`parser->state = ParserState::WAIT_SOF1; parser->rx_index = 0; parser->expected_len = 0;`），保留全部历史诊断统计；
         - 返回 `Status::OK;`（静默丢弃错误帧，符合流式解析容错契约）。
     - 阶段隔离与防作弊：`parser_poll_timeout` 与超时中断先检后刷逻辑保持留桩（留待 V2-P05D 实现）；
     - 未修改头文件 `parser.h`、`codec.*`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: 79be851016c62e31b041700b4cd200a488a8eade`，干净无杂质（退出码 0）；
   - `cmake configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `stream_payload_cases`: 运行 `run_codec_cases.py --case-set stream_payload`，全部 5 个用例（`SPLD-001`～`SPLD-005`）100% 通过（退出码 0）；
   - `timeout_antigaming`: 运行 `run_codec_cases.py --case-set timeout`，被严格拦截并以退出码 1 退出，防作弊核验完全达标；
   - `stream_sync_regression`: 运行 `run_codec_cases.py --case-set stream_sync`，5/5 用例 100% 通过（退出码 0）；
   - `stream_header_regression`: 运行 `run_codec_cases.py --case-set stream_header`，5/5 用例 100% 通过（退出码 0）；
   - `host_smoke_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）；
   - `check_task_graph`: 静态任务依赖图与制品哈希核验 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/02_cmake.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/04_stream_payload_cases.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/05_timeout_antigaming.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/06_stream_sync_regression.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/07_stream_header_regression.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/08_host_smoke_regression.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/09_check_task_graph.log`
   - `docs/evidence/minimc_v2/V2-P05C/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`codec.*`、`parser.h` 或 `project-control/.agents/**`。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/parser.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：载荷累积与 CRC 收尾分发实现、SPLD 定向验证、TMO 防作弊拦截、SYNC / SHDR / 宿主冒烟回归全部验证通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
