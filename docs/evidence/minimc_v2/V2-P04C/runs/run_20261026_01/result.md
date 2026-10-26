# 单票实际执行记录: V2-P04C (Run 1)

```yaml
task_id: V2-P04C
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p04c_20261026_01
start_time: "2026-10-26T20:50:00+08:00"
end_time: "2026-10-26T20:52:00+08:00"
start_end_time: "2026-10-26T20:50:00+08:00 ~ 2026-10-26T20:52:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 830ef5a7a230deb720f26a144f921b2c96bebe18
workspace_diff_sha256: baad915063b64d720f501139e9e77fda984bcc341240efba740c8135648ad98d
input_versions:
  - predecessor_task: V2-P04B
    accepted_version: "sha256:a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "830ef5a7a230deb720f26a144f921b2c96bebe18"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/codec.cpp (+22, -3 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:50:40+08:00"
    end_time: "2026-10-26T20:50:40+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04C -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:50:59+08:00"
    end_time: "2026-10-26T20:51:00+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/02_configure.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P04C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:51:07+08:00"
    end_time: "2026-10-26T20:51:08+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04C/bin/minimc-probe --case-set decode_bounds"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:51:12+08:00"
    end_time: "2026-10-26T20:51:12+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/04_focused_cases.log
    actual_case_count: 6
    warning_count: 0
  - id: host_regression
    command: "env -C /tmp/ai_soc_v2_build/V2-P04C ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04C
    start_time: "2026-10-26T20:51:16+08:00"
    end_time: "2026-10-26T20:51:16+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/05_host_regression.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04C -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P04C"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04C/bin/minimc-probe --case-set decode_bounds"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "env -C /tmp/ai_soc_v2_build/V2-P04C ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04C
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/02_configure.log
  - docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/04_focused_cases.log
  - docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/05_host_regression.log
candidate_commit: null
candidate_commit_or_diff_sha256: "baad915063b64d720f501139e9e77fda984bcc341240efba740c8135648ad98d"
candidate_diff_sha256: "baad915063b64d720f501139e9e77fda984bcc341240efba740c8135648ad98d"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/codec.cpp
    size: 3752
    sha256: 84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7
actual_cases:
  - "DBND-001: 0 字节空输入 (< 14B 最小帧长) 安全拒绝，返回 frame_too_short (通过)"
  - "DBND-002: 11 字节残缺帧头 (< 14B 最小帧长) 安全拒绝，返回 frame_too_short (通过)"
  - "DBND-003: 13 字节截断帧 (缺失 CRC 高字节) 安全拒绝，返回 frame_too_short (通过)"
  - "DBND-004: 声明 L=1025 (> MTU 1024) 且在访问载荷或 CRC 前安全拒绝，返回 mtu_exceeded (通过)"
  - "DBND-005: 截断帧 (声明 L=4 应为 18 字节，实际仅 17 字节) 拒绝，返回 length_mismatch (通过)"
  - "DBND-006: 超长缓冲区 (声明 L=0 应为 14 字节，实际 15 字节) 拒绝，返回 length_mismatch (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 DBND-001~DBND-006 执行记录的独立评审"
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

本微步任务卡 `V2-P04C` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/codec.cpp`
   - 文件大小：`3,752` 字节 (109 行)
   - SHA256：`84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7`
   - Git Diff SHA256: `baad915063b64d720f501139e9e77fda984bcc341240efba740c8135648ad98d`
   - 实现内容：
     - 在 `minimc::decode_frame` 中实现第一阶段的长度与边界校验防御逻辑；
     - 入口防御：若 `out_frame != nullptr`，先将其重置为空状态 `*out_frame = {}`；
     - 最小帧长校验：若 `frame_bytes.data == nullptr || frame_bytes.size < MIN_FRAME_SIZE` (14 字节)，安全返回 `Status::ERR_FRAME_TOO_SHORT`；
     - 声明载荷长度提取：通过显式字节偏移读取 `frame_bytes.data[10]` 与 `frame_bytes.data[11]` 组合为小端 uint16（禁止强转结构体指针，杜绝未对齐内存访问）；
     - MTU 门禁校验：若 `declared_payload_len > MAX_PAYLOAD_SIZE` (1024 字节)，安全返回 `Status::ERR_MTU_EXCEEDED`；
     - 帧总长度匹配校验：计算理论期望帧长 `HEADER_SIZE + declared_payload_len + CRC_SIZE`（即 `14 + declared_payload_len`）。若实际 `frame_bytes.size != expected_frame_size`，安全返回 `Status::ERR_LENGTH_MISMATCH`；
     - 阶段边界（防提前越界实现）：对于通过上述长度/边界校验的候选帧，由于完整头部格式与 CRC 校验属于下张微步卡 `V2-P04D` 的范围，本阶段严格返回 `Status::ERR_NOT_IMPLEMENTED`，绝不提前伪造返回 OK；
     - 严格保持已实现的 `calc_crc16` 与 `encode_frame` 逻辑不变；
     - 未修改头文件 `codec.h`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: 830ef5a7a230deb720f26a144f921b2c96bebe18`, `test_harness: 5a2ebe49e26ffb76a55ab74de652142ce9961de7`，干净无杂质（退出码 0）；
   - `configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `focused_cases`: 运行 `run_codec_cases.py --case-set decode_bounds`，全部 6 个用例（`DBND-001`～`DBND-006`）100% 通过（退出码 0）；
   - 回归核验：`crc` (9/9) 与 `encode` (8/8) 持续 100% 通过；
   - `host_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/02_configure.log`
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/04_focused_cases.log`
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/05_host_regression.log`
   - `docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**`。
- 未触碰头文件 `codec.h` 或 CMakeLists 文件。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/codec.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：实现与全套 DBND 边界防御用例验证全部通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
