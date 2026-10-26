# 单票实际执行记录: V2-P05A (Run 1)

```yaml
task_id: V2-P05A
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p05a_20261026_01
start_time: "2026-10-26T21:08:00+08:00"
end_time: "2026-10-26T21:11:00+08:00"
start_end_time: "2026-10-26T21:08:00+08:00 ~ 2026-10-26T21:11:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: bc2506049c1c4947b32e8d59055b146ff9e4fac4
workspace_diff_sha256: 38650681ba595e829cace1e10e060006a89a617c41d11e5603fd4d3dbfb656d9
input_versions:
  - predecessor_task: V2-P04D
    accepted_version: "sha256:e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "bc2506049c1c4947b32e8d59055b146ff9e4fac4"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/parser.cpp (+47, -6 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:09:24+08:00"
    end_time: "2026-10-26T21:09:24+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05A -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:09:55+08:00"
    end_time: "2026-10-26T21:09:55+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/02_cmake.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P05A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:10:00+08:00"
    end_time: "2026-10-26T21:10:00+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: stream_sync_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05A/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:10:05+08:00"
    end_time: "2026-10-26T21:10:05+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/04_stream_sync_cases.log
    actual_case_count: 5
    warning_count: 0
  - id: stream_header_antigaming
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05A/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T21:10:11+08:00"
    end_time: "2026-10-26T21:10:11+08:00"
    actual_exit_code: 1
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/05_stream_header_antigaming.log
    actual_case_count: 5
    warning_count: 0
  - id: host_regression
    command: "cd /tmp/ai_soc_v2_build/V2-P05A && ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P05A
    start_time: "2026-10-26T21:10:23+08:00"
    end_time: "2026-10-26T21:10:23+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/06_regression.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P05A -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P05A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05A/bin/minimc-probe --case-set stream_sync"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P05A/bin/minimc-probe --case-set stream_header"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 1
  - command: "cd /tmp/ai_soc_v2_build/V2-P05A && ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P05A
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/02_cmake.log
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/04_stream_sync_cases.log
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/05_stream_header_antigaming.log
  - docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/06_regression.log
candidate_commit: null
candidate_commit_or_diff_sha256: "38650681ba595e829cace1e10e060006a89a617c41d11e5603fd4d3dbfb656d9"
candidate_diff_sha256: "38650681ba595e829cace1e10e060006a89a617c41d11e5603fd4d3dbfb656d9"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/parser.cpp
    size: 3018
    sha256: 573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33
actual_cases:
  - "SYNC-001: 丢弃前置噪声字节 (0x00, 0xFF, 0x12) 保持在 WAIT_SOF1，分发帧数为 0 (通过)"
  - "SYNC-002: 单个 0x55 触发状态机 WAIT_SOF1 -> WAIT_SOF2 转换，不分发帧 (通过)"
  - "SYNC-003: 连续 0x55 0x55 后接 0xAA 维持前导同步并成功进入 READ_HEADER (通过)"
  - "SYNC-004: 0x55 后接非 0xAA/非 0x55 (0x01) 重置状态机回 WAIT_SOF1 (通过)"
  - "SYNC-005: WAIT_SOF2 显式复位 parser_reset 具有幂等性并安全返回 WAIT_SOF1 (通过)"
  - "SHDR-001~SHDR-005: stream_header 未实现分组防作弊测试严格拦截退出码 1，5/5 拒绝通过 (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 SYNC-001~SYNC-005 执行记录的独立评审"
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

本微步任务卡 `V2-P05A` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/parser.cpp`
   - 文件大小：`3,018` 字节 (96 行)
   - SHA256：`573901547d37813fe42dade25459948096886c82baf1866387b065858daf3f33`
   - Git Diff SHA256: `38650681ba595e829cace1e10e060006a89a617c41d11e5603fd4d3dbfb656d9`
   - 实现内容：
     - `parser_init`: 初始化解析器结构体，状态置为 `WAIT_SOF1`，清空全部字段与统计计数；
     - `parser_reset`: 将状态机复位回 `WAIT_SOF1`，清空 `rx_index`、`expected_len`、`last_byte_rx_ms`，严密保留统计计数；
     - `parser_feed_byte`:
       - 入参严格防御：`if (!parser || !out_frame_ready) return Status::ERR_INVALID_ARGUMENT;`
       - 初始化输出：`*out_frame_ready = false; if (out_frame != nullptr) *out_frame = FrameView{};`
       - 处理 `WAIT_SOF1`：
         - `byte == SOF_1 (0x55)`：写入 `rx_buffer[0] = SOF_1`，`rx_index = 1`，转换状态至 `WAIT_SOF2`，记录 `last_byte_rx_ms = now_ms`，返回 `Status::OK`；
         - `byte != SOF_1`：`err_sof++`，记录 `last_byte_rx_ms = now_ms`，保持在 `WAIT_SOF1`，返回 `Status::OK`；
       - 处理 `WAIT_SOF2`：
         - `byte == SOF_2 (0xAA)`：写入 `rx_buffer[1] = SOF_2`，`rx_index = 2`，转换状态至 `READ_HEADER`，记录 `last_byte_rx_ms = now_ms`，返回 `Status::OK`；
         - `byte == SOF_1 (0x55)`：维持同步前导，`rx_buffer[0] = SOF_1`，`rx_index = 1`，保持在 `WAIT_SOF2`，记录 `last_byte_rx_ms = now_ms`，返回 `Status::OK`；
         - 其余无效字节：`err_sof++`，重置状态回 `WAIT_SOF1`，`rx_index = 0`，`expected_len = 0`，记录 `last_byte_rx_ms = now_ms`，返回 `Status::OK`；
       - 阶段隔离与防作弊：在 `READ_HEADER`、`READ_PAYLOAD`、`READ_CRC` 及后续状态严格返回 `Status::ERR_NOT_IMPLEMENTED`；
     - `parser_poll_timeout`: 保持当前符号桩状态（返回 `false`，留待 V2-P05D 实现）；
     - 未修改头文件 `parser.h`、`codec.*`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: bc2506049c1c4947b32e8d59055b146ff9e4fac4`, `test_harness: 5a2ebe49e26ffb76a55ab74de652142ce9961de7`，干净无杂质（退出码 0）；
   - `cmake configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `stream_sync_cases`: 运行 `run_codec_cases.py --case-set stream_sync`，全部 5 个用例（`SYNC-001`～`SYNC-005`）100% 通过（退出码 0）；
   - `stream_header_antigaming`: 运行 `run_codec_cases.py --case-set stream_header`，5/5 用例全部被严格判定为 `not_implemented` 并以退出码 1 退出，防作弊核验完全达标；
   - `host_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/02_cmake.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/04_stream_sync_cases.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/05_stream_header_antigaming.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/06_regression.log`
   - `docs/evidence/minimc_v2/V2-P05A/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`codec.*`、`parser.h` 或 `project-control/.agents/**`。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/parser.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：解析器复位与同步实现、SYNC 定向验证、SHDR 防作弊拦截与冒烟回归全部验证通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
