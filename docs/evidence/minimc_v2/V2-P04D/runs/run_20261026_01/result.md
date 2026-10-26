# 单票实际执行记录: V2-P04D (Run 1)

```yaml
task_id: V2-P04D
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p04d_20261026_01
start_time: "2026-10-26T20:58:00+08:00"
end_time: "2026-10-26T21:00:00+08:00"
start_end_time: "2026-10-26T20:58:00+08:00 ~ 2026-10-26T21:00:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 219597a3a85570515f21b13656979b31487da02a
workspace_diff_sha256: 2422842ad7140536aa673912bb2bac7f4c2f26b1f5e0fbeb199d087545b3ad67
input_versions:
  - predecessor_task: V2-P04C
    accepted_version: "sha256:84312fea95497444b58a3792139325e88e71465c6a2f7fcdf90cc1aac5fa2be7"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P04C/runs/run_20261026_01/qa_review_report.md"
  - test_runner: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "219597a3a85570515f21b13656979b31487da02a"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/codec.cpp (+56, -3 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:58:40+08:00"
    end_time: "2026-10-26T20:58:40+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04D -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:59:11+08:00"
    end_time: "2026-10-26T20:59:12+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/02_configure.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P04D"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:59:19+08:00"
    end_time: "2026-10-26T20:59:19+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04D/bin/minimc-probe --case-set decode"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:59:23+08:00"
    end_time: "2026-10-26T20:59:23+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/04_focused_cases.log
    actual_case_count: 12
    warning_count: 0
  - id: host_regression
    command: "env -C /tmp/ai_soc_v2_build/V2-P04D ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04D
    start_time: "2026-10-26T20:59:28+08:00"
    end_time: "2026-10-26T20:59:29+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/05_host_regression.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04D -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P04D"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04D/bin/minimc-probe --case-set decode"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "env -C /tmp/ai_soc_v2_build/V2-P04D ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04D
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/02_configure.log
  - docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/04_focused_cases.log
  - docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/05_host_regression.log
candidate_commit: null
candidate_commit_or_diff_sha256: "2422842ad7140536aa673912bb2bac7f4c2f26b1f5e0fbeb199d087545b3ad67"
candidate_diff_sha256: "2422842ad7140536aa673912bb2bac7f4c2f26b1f5e0fbeb199d087545b3ad67"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/codec.cpp
    size: 6019
    sha256: e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040
actual_cases:
  - "DEC-001: 解码 Golden 帧 V01 (14B CMD_GET_VERSION) (通过)"
  - "DEC-002: 解码 Golden 帧 V02 Inbound (18B CMD_PING) (通过)"
  - "DEC-003: 解码 Golden 帧 V02 Outbound (18B 路由后 CMD_PING, hop=3, route_ctrl=0x04) (通过)"
  - "DEC-004: 解码 Golden 帧 V03 (25B CMD_STREAM_CHUNK) (通过)"
  - "DEC-005: 解码 Golden 帧 V04 作为结构有效 14B 帧 (业务层冲突隔离) (通过)"
  - "DEC-006: 解码合法帧 CRC-16 为 0x0000 显式比对通过 (通过)"
  - "DEC-007: 解码最大 1024B 载荷满帧 (总长 1038B) (通过)"
  - "DEC-008: 拒绝错误 SOF 魔数 (0x55 0xAB) 返回 bad_sof (通过)"
  - "DEC-009: 拒绝损坏的 CRC-16 (尾字节翻转) 返回 crc_mismatch (通过)"
  - "DEC-010: 拒绝非法协议版本号 (flags=0x01, proto!=0b01) 返回 bad_version (通过)"
  - "DEC-011: 拒绝非零保留标志位 (flags=0x25, reserved!=0) 返回 bad_flags_reserved (通过)"
  - "DEC-012: 拒绝互斥路由控制位组合 ((route_ctrl & 0x03) == 0x03) 返回 bad_route_ctrl (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 DEC-001~DEC-012 执行记录的独立评审"
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

本微步任务卡 `V2-P04D` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/codec.cpp`
   - 文件大小：`6,019` 字节 (162 行)
   - SHA256：`e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040`
   - Git Diff SHA256: `2422842ad7140536aa673912bb2bac7f4c2f26b1f5e0fbeb199d087545b3ad67`
   - 实现内容：
     - 在 `minimc::decode_frame` 中完整实现第二阶段头部格式校验、CRC-16 校验与各字段安全提取；
     - 完整保留 Stage 1 边界防御（`< 14` 返回 `ERR_FRAME_TOO_SHORT`，`> 1024` 返回 `ERR_MTU_EXCEEDED`，`!= 14 + declared_payload_len` 返回 `ERR_LENGTH_MISMATCH`）；
     - 显式单字节偏移校验（杜绝结构体强转与未对齐内存访问）：
       a) SOF 校验：`frame_bytes.data[0] != 0x55 || frame_bytes.data[1] != 0xAA` 返回 `Status::ERR_BAD_SOF`；
       b) 协议版本校验：`(flags & FLAGS_PROTO_VERSION_MASK) != FLAGS_PROTO_VERSION_V2` 返回 `Status::ERR_BAD_VERSION`；
       c) 标志保留位校验：`(flags & FLAGS_RESERVED_MASK) != 0` 返回 `Status::ERR_BAD_FLAGS_RESERVED`；
       d) 路由控制校验：`((route_ctrl & 0x03) == 0x03) || ((route_ctrl & ROUTE_RESERVED_MASK) != 0)` 返回 `Status::ERR_BAD_ROUTE_CTRL`；
       e) CRC-16 校验：计算 `calc_crc16(Bytes(frame_bytes.data, 12 + declared_payload_len))`，对比尾部 2 字节小端序线缆 CRC，不匹配返回 `Status::ERR_CRC_MISMATCH`；
       f) 字段提取填充：校验全部通过后，若 `out_frame != nullptr`，显式读取并填充 `out_frame->header` 各字段、`out_frame->payload` 与 `out_frame->crc`；
       g) 返回 `Status::OK`。
     - 严格保持已实现的 `calc_crc16` 与 `encode_frame` 逻辑不变；
     - 未修改头文件 `codec.h`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: 219597a3a85570515f21b13656979b31487da02a`, `test_harness: 5a2ebe49e26ffb76a55ab74de652142ce9961de7`，干净无杂质（退出码 0）；
   - `configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `focused_cases`: 运行 `run_codec_cases.py --case-set decode`，全部 12 个用例（`DEC-001`～`DEC-012`）100% 通过（退出码 0）；
   - 回归核验：`crc` (9/9)、`encode` (8/8) 与 `decode_bounds` (6/6) 持续 100% 保持通过；
   - `host_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/02_configure.log`
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/04_focused_cases.log`
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/05_host_regression.log`
   - `docs/evidence/minimc_v2/V2-P04D/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**`。
- 未触碰头文件 `codec.h` 或 CMakeLists 文件。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/codec.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：实现与全套 DEC 完整帧校验用例验证全部通过（增量阶段 V2-P04 核心业务逻辑全面收敛），现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立审查。
