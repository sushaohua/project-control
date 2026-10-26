# 单票实际执行记录: V2-P04B (Run 1)

```yaml
task_id: V2-P04B
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p04b_20261026_01
start_time: "2026-10-26T20:42:00+08:00"
end_time: "2026-10-26T20:44:00+08:00"
start_end_time: "2026-10-26T20:42:00+08:00 ~ 2026-10-26T20:44:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: e3215c449421ba0898004012ece1a7d329ea4cf0
workspace_diff_sha256: a133d1432fdca6f8343838de77727e94de7b3d4b60a2bed7644c0786d8b38733
input_versions:
  - predecessor_task: V2-P04A
    accepted_version: "sha256:7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "e3215c449421ba0898004012ece1a7d329ea4cf0"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/codec.cpp (+46, -6 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:42:34+08:00"
    end_time: "2026-10-26T20:42:34+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04B -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:43:16+08:00"
    end_time: "2026-10-26T20:43:17+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/02_configure.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P04B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:43:21+08:00"
    end_time: "2026-10-26T20:43:22+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04B/bin/minimc-probe --case-set encode"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:43:38+08:00"
    end_time: "2026-10-26T20:43:38+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/04_focused_cases.log
    actual_case_count: 8
    warning_count: 0
  - id: host_regression
    command: "env -C /tmp/ai_soc_v2_build/V2-P04B ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04B
    start_time: "2026-10-26T20:43:42+08:00"
    end_time: "2026-10-26T20:43:42+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/05_host_regression.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04B -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P04B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04B/bin/minimc-probe --case-set encode"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "env -C /tmp/ai_soc_v2_build/V2-P04B ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04B
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/02_configure.log
  - docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/04_focused_cases.log
  - docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/05_host_regression.log
candidate_commit: null
candidate_commit_or_diff_sha256: "a133d1432fdca6f8343838de77727e94de7b3d4b60a2bed7644c0786d8b38733"
candidate_diff_sha256: "a133d1432fdca6f8343838de77727e94de7b3d4b60a2bed7644c0786d8b38733"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/codec.cpp
    size: 3063
    sha256: a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7
actual_cases:
  - "ENC-001: 编码 V01 (0B 载荷 CMD_GET_VERSION) 在恰好 14B 容量下成功 (通过)"
  - "ENC-002: 编码 V02 Inbound (4B 载荷 CMD_PING，时间戳小端) (通过)"
  - "ENC-003: 编码 CMD_PONG (12B 载荷，26B 总帧长) (通过)"
  - "ENC-004: 编码 CMD_VERSION_REPORT (16B 载荷，30B 总帧长) (通过)"
  - "ENC-005: 编码最大 1024B 载荷满帧 (总长 1038B，恰好容量 1038) (通过)"
  - "ENC-006: 拒绝 payload_len=1025 (> MTU 1024) 抛出 mtu_exceeded (通过)"
  - "ENC-007: 拒绝输出容量差 1 字节 (容量 13B 对应 14B V01 帧) 抛出 buffer_too_small (通过)"
  - "ENC-008: 拒绝空载荷指针且 payload_len > 0 (payload_len=4) 抛出 invalid_argument (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 ENC-001~ENC-008 执行记录的独立评审"
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

本微步任务卡 `V2-P04B` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/codec.cpp`
   - 文件大小：`3,063` 字节 (90 行)
   - SHA256：`a659515a549b4ffe6e444aa2648e4984288df1fd225fea8356a7cc6a1a1608c7`
   - Git Diff SHA256: `a133d1432fdca6f8343838de77727e94de7b3d4b60a2bed7644c0786d8b38733`
   - 实现内容：
     - 精准实现标准 **有界帧编码 `minimc::encode_frame`** 算法；
     - 入参严密防御：
       - 入口安全初始化 `*out_written = 0`，任何早期错误返回均不泄露旧有效长度；
       - `payload.size > MAX_PAYLOAD_SIZE || header.payload_len > MAX_PAYLOAD_SIZE` 拒绝并返回 `Status::ERR_MTU_EXCEEDED`；
       - `payload.data == nullptr && (payload.size > 0 || header.payload_len > 0)` 拒绝并返回 `Status::ERR_INVALID_ARGUMENT`；
       - `out_buffer.data == nullptr || out_buffer.size < total_frame_size` 拒绝并返回 `Status::ERR_BUFFER_TOO_SMALL`；
     - 内存安全帧头序列化：显式单字节偏移写入（杜绝强转结构体指针导致的未对齐内存访问风险）；
     - 载荷复制：安全拷贝 `payload.size` 字节至偏移 12 处；
     - 校验和计算与尾追加：对 `0 .. 11 + payload.size`（共 `12 + payload.size` 字节）调用已验收的 `calc_crc16`，小端序（LSB在先、MSB在后）追加于帧尾；
     - 成功写入：准确更新 `*out_written = total_frame_size` 并返回 `Status::OK`；
     - 保持桩隔离：未修改 `decode_frame`（保持返回 `Status::ERR_NOT_IMPLEMENTED` 符号桩状态）；
     - 未修改头文件 `codec.h`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: e3215c449421ba0898004012ece1a7d329ea4cf0`, `test_harness: 5a2ebe49e26ffb76a55ab74de652142ce9961de7`，干净无杂质（退出码 0）；
   - `configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `focused_cases`: 运行 `run_codec_cases.py --case-set encode`，全部 8 个用例（`ENC-001`～`ENC-008`）100% 通过（退出码 0）；
   - `host_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/02_configure.log`
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/04_focused_cases.log`
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/05_host_regression.log`
   - `docs/evidence/minimc_v2/V2-P04B/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**`。
- 未触碰头文件 `codec.h` 或 CMakeLists 文件。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/codec.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：实现与全套 ENC 有界编码用例验证全部通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
