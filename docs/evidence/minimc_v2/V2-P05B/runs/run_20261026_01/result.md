# 单票实际执行记录: V2-P05B (Run 1)

```yaml
task_id: V2-P05B
task_revision: 2
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p05b_20261026_01
start_time: "2026-10-26T21:17:00+08:00"
end_time: "2026-10-26T21:20:00+08:00"
start_end_time: "2026-10-26T21:17:00+08:00 ~ 2026-10-26T21:20:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: a3a2d9586402a3f00d8d95902087999478f9244a
workspace_diff_sha256: 44704260e462cb8410d3c5d83355fe6fbd00cca0f9aa7aa90dc3ed11a6e27b8f
input_versions:
  - predecessor_task: V2-P05A
    accepted_version: "sha256:573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "a3a2d9586402a3f00d8d95902087999478f9244a"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/parser.cpp (+36, -2 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:17:40+08:00"
    end_time: "2026-10-26T21:17:40+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05B -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:18:14+08:00"
    end_time: "2026-10-26T21:18:14+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/02_cmake.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P05B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:18:19+08:00"
    end_time: "2026-10-26T21:18:19+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:18:24+08:00"
    end_time: "2026-10-26T21:18:24+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/04_stream_header_cases.log
    actual_case_count: 5
    warning_count: 0
  - id: stream_payload_antigaming
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_payload"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:19:05+08:00"
    end_time: "2026-10-26T21:19:05+08:00"
    actual_exit_code: 1
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/05_stream_payload_antigaming.log
    actual_case_count: 5
    warning_count: 0
  - id: stream_sync_regression
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:19:10+08:00"
    end_time: "2026-10-26T21:19:10+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/06_stream_sync_regression.log
    actual_case_count: 5
    warning_count: 0
  - id: host_smoke_regression
    command: "(cd /tmp/ai_soc_v2_build/V2-P05B && ctest --output-on-failure -R ^host_runtime_smoke$)"
    cwd: /tmp/ai_soc_v2_build/V2-P05B
    start_time: "2026-10-26T21:19:13+08:00"
    end_time: "2026-10-26T21:19:13+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/07_host_smoke_regression.log
    actual_case_count: 1
    warning_count: 0
  - id: check_task_graph
    command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P05B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:19:20+08:00"
    end_time: "2026-10-26T21:19:20+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/08_check_task_graph.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05B -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P05B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_payload"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 1
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05B/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "(cd /tmp/ai_soc_v2_build/V2-P05B && ctest --output-on-failure -R ^host_runtime_smoke$)"
    cwd: /tmp/ai_soc_v2_build/V2-P05B
    exit_code: 0
  - command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P05B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/02_cmake.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/04_stream_header_cases.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/05_stream_payload_antigaming.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/06_stream_sync_regression.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/07_host_smoke_regression.log
  - docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/08_check_task_graph.log
candidate_commit: null
candidate_commit_or_diff_sha256: "44704260e462cb8410d3c5d83355fe6fbd00cca0f9aa7aa90dc3ed11a6e27b8f"
candidate_diff_sha256: "44704260e462cb8410d3c5d83355fe6fbd00cca0f9aa7aa90dc3ed11a6e27b8f"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/parser.cpp
    size: 4226
    sha256: 4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba
actual_cases:
  - "SHDR-001: 逐字节累积 10 字节固定帧头进入 READ_PAYLOAD，状态机保持同步 (通过)"
  - "SHDR-002: 仅接收 9 字节头部数据，解析器保持 READ_HEADER 状态且 header_bytes_collected=7 (通过)"
  - "SHDR-003: 累积 L=0 载荷长度，直接跃迁至 READ_CRC 状态，expected_len 锁定为 14 (通过)"
  - "SHDR-004: 累积 L=1024 边界载荷长度，合法进入 READ_PAYLOAD 状态，expected_len=1038 (通过)"
  - "SHDR-005: 累积超限长度 L=1025，触发 MTU 门禁，递增 err_mtu 并复位回 WAIT_SOF1 (通过)"
  - "SPLD-001~SPLD-005: stream_payload 未实现分组防作弊测试严格拦截退出码 1，5/5 拒绝通过 (通过)"
  - "SYNC-001~SYNC-005: stream_sync 前置流式同步能力回归测试 5/5 100% 通过 (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过 (通过)"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 SHDR-001~SHDR-005 执行记录的独立评审"
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

本微步任务卡 `V2-P05B` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/parser.cpp`
   - 文件大小：`4,226` 字节 (130 行)
   - SHA256：`4839634a52fc5f33bb7c06cb245ffe4b4b9228acfaeae79b9ef87a35c7491aba`
   - Git Diff SHA256: `44704260e462cb8410d3c5d83355fe6fbd00cca0f9aa7aa90dc3ed11a6e27b8f`
   - 实现内容：
     - 在 `parser_feed_byte` 中的 `ParserState::READ_HEADER` 状态分支下：
       - `rx_index < 11` 时：先写入 `rx_buffer[rx_index++] = byte;`，保持状态在 `READ_HEADER`；
       - `rx_index == 11` 时（接收到固定头部的最后一个字节）：
         - 严格先将末字节存入缓冲：`rx_buffer[11] = byte; rx_index = 12;`，杜绝溢出和截断；
         - 小端解析 16-bit 载荷长度：`uint16_t payload_len = static_cast<uint16_t>(rx_buffer[10]) | (static_cast<uint16_t>(rx_buffer[11]) << 8);`；
         - **MTU 门禁检验**：
           - 若 `payload_len > 1024` (超限)：`parser->stat_err_mtu++`，复位状态机 `parser->state = ParserState::WAIT_SOF1; parser->rx_index = 0; parser->expected_len = 0;`；
           - 若 `payload_len == 0` (空载荷)：直接跃迁 `parser->expected_len = 14; parser->state = ParserState::READ_CRC;`；
           - 若 `0 < payload_len <= 1024`：设置目标长度 `parser->expected_len = 14 + payload_len; parser->state = ParserState::READ_PAYLOAD;`；
       - 阶段隔离与防作弊：在 `READ_PAYLOAD` 与 `READ_CRC` 及后续状态严格返回 `Status::ERR_NOT_IMPLEMENTED`；
     - 未修改头文件 `parser.h`、`codec.*`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: a3a2d9586402a3f00d8d95902087999478f9244a`，干净无杂质（退出码 0）；
   - `cmake configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `stream_header_cases`: 运行 `run_codec_cases.py --case-set stream_header`，全部 5 个用例（`SHDR-001`～`SHDR-005`）100% 通过（退出码 0）；
   - `stream_payload_antigaming`: 运行 `run_codec_cases.py --case-set stream_payload`，5/5 用例全部被严格判定为 `not_implemented` 并以退出码 1 退出，防作弊核验完全达标；
   - `stream_sync_regression`: 运行 `run_codec_cases.py --case-set stream_sync`，前置 5 个用例（`SYNC-001`～`SYNC-005`）100% 通过（退出码 0）；
   - `host_smoke_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）；
   - `check_task_graph`: 静态任务依赖图与制品哈希核验 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/02_cmake.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/04_stream_header_cases.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/05_stream_payload_antigaming.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/06_stream_sync_regression.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/07_host_smoke_regression.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/08_check_task_graph.log`
   - `docs/evidence/minimc_v2/V2-P05B/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`codec.*`、`parser.h` 或 `project-control/.agents/**`。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/parser.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：固定帧头累积与长度门禁实现、SHDR 定向验证、SPLD 防作弊拦截、SYNC 与宿主冒烟回归全部验证通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
