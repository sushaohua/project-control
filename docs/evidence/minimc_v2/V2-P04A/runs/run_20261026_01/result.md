# 单票实际执行记录: V2-P04A (Run 1)

```yaml
task_id: V2-P04A
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p04a_20261026_01
start_time: "2026-10-26T20:34:00+08:00"
end_time: "2026-10-26T20:36:00+08:00"
start_end_time: "2026-10-26T20:34:00+08:00 ~ 2026-10-26T20:36:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 25d8f99faf338b2d324a9793b33deaa423a57f9e
workspace_diff_sha256: 97e05a4616642bd1997c3f129e483bb72630d52ccdadf864bad60235d1c41c27
input_versions:
  - predecessor_task: V2-P03F
    accepted_version: "sha256:e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P03F/runs/run_20261026_01/arch_review_report.md"
  - test_vectors: "test_harness/test_cases/minimcproto/vectors.json"
    sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "25d8f99faf338b2d324a9793b33deaa423a57f9e"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/core/forward/minimc/codec.cpp (+16, -4 lines)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:34:10+08:00"
    end_time: "2026-10-26T20:34:10+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04A -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:34:28+08:00"
    end_time: "2026-10-26T20:34:29+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/02_configure.log
    actual_case_count: 1
    warning_count: 0
  - id: build
    command: "cmake --build /tmp/ai_soc_v2_build/V2-P04A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:34:32+08:00"
    end_time: "2026-10-26T20:34:32+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: focused_cases
    command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04A/bin/minimc-probe --case-set crc"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T20:34:36+08:00"
    end_time: "2026-10-26T20:34:36+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/04_focused_cases.log
    actual_case_count: 9
    warning_count: 0
  - id: host_regression
    command: "env -C /tmp/ai_soc_v2_build/V2-P04A ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04A
    start_time: "2026-10-26T20:34:40+08:00"
    end_time: "2026-10-26T20:34:40+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/05_host_regression.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_v2_build/V2-P04A -G Ninja -DCMAKE_BUILD_TYPE=Debug"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_v2_build/V2-P04A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P04A/bin/minimc-probe --case-set crc"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "env -C /tmp/ai_soc_v2_build/V2-P04A ctest --output-on-failure -R ^host_runtime_smoke$"
    cwd: /tmp/ai_soc_v2_build/V2-P04A
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/02_configure.log
  - docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/03_build.log
  - docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/04_focused_cases.log
  - docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/05_host_regression.log
candidate_commit: null
candidate_commit_or_diff_sha256: "97e05a4616642bd1997c3f129e483bb72630d52ccdadf864bad60235d1c41c27"
candidate_diff_sha256: "97e05a4616642bd1997c3f129e483bb72630d52ccdadf864bad60235d1c41c27"
artifact_hashes:
  - path: soc-ap/core/forward/minimc/codec.cpp
    size: 1468
    sha256: 7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395
actual_cases:
  - "CRC-001: 标准检查串 '123456789' 计算结果 0x29B1 (通过)"
  - "CRC-002: 空 0-byte 输入返回初始值 0xFFFF (通过)"
  - "CRC-003: Golden 帧 V01 头部及载荷 (12 字节) 计算结果 0x1EF9 (通过)"
  - "CRC-004: Golden 帧 V02 Inbound 头部及载荷 (16 字节) 计算结果 0xB066 (通过)"
  - "CRC-005: Golden 帧 V02 Outbound 头部及载荷 (16 字节) 计算结果 0x3073 (通过)"
  - "CRC-006: Golden 帧 V03 头部及载荷 (23 字节) 计算结果 0xDAA0 (通过)"
  - "CRC-007: Golden 帧 V04 头部及载荷 (12 字节) 计算结果 0xC13D (通过)"
  - "CRC-008: 合法帧 CRC-16 结果为 0x0000 显式比对通过 (通过)"
  - "CRC-009: 空数据指针且长度非0安全拒绝 invalid_argument，不发生空指针解引用 (通过)"
  - "host_runtime_smoke: 宿主冒烟回归测试 1/1 100% 通过"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行针对交付物与 CRC-001~CRC-009 执行记录的独立评审"
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

本微步任务卡 `V2-P04A` 由 `ENG-FWD` (Author) 角色执行，严格遵守 `allowed_paths` 与 `write_scope` 约束：

1. **唯一交付物**: `soc-ap/core/forward/minimc/codec.cpp`
   - 文件大小：`1,468` 字节 (50 行)
   - SHA256：`7cb49c0a6720f40055e9e24eaf9b30a5d8419ddfd6f89982c4d83bbef0218395`
   - Git Diff SHA256: `97e05a4616642bd1997c3f129e483bb72630d52ccdadf864bad60235d1c41c27`
   - 实现内容：
     - 精准实现标准 **CRC-16/CCITT-FALSE** 算法（`Poly=0x1021`, `Init=0xFFFF`, `RefIn=False`, `RefOut=False`, `XorOut=0x0000`）；
     - 防御性空值处理：当 `data.data == nullptr || data.size == 0` 时，安全返回初始值 `0xFFFF`，严禁解引用空指针；
     - 显式类型转换：使用 `static_cast<uint16_t>` 保证零整型提升警告，零未定义行为；
     - 保持桩状态隔离：未修改 `encode_frame` 或 `decode_frame`（保持返回 `Status::ERR_NOT_IMPLEMENTED` 符号桩状态）；
     - 未修改头文件 `codec.h`、`CMakeLists.txt` 或 `test_harness/**` 下任何文件。

2. **验证命令与结果**:
   - `precheck`: 工作区 HEAD `soc-ap: 25d8f99faf338b2d324a9793b33deaa423a57f9e`, `test_harness: 5a2ebe49e26ffb76a55ab74de652142ce9961de7`，干净无杂质（退出码 0）；
   - `configure`: CMake Ninja Debug 配置成功（退出码 0）；
   - `build`: 完整构建成功，生成 `libminimcproto.a`、`bin/soc-ap` 与 `bin/minimc-probe`，`-Wall -Wextra -Wpedantic -Werror` 下 0 告警 0 错误（退出码 0）；
   - `focused_cases`: 运行 `run_codec_cases.py --case-set crc`，全部 9 个用例（`CRC-001`～`CRC-009`）100% 通过（退出码 0）；
   - `host_regression`: `host_runtime_smoke` 回归测试 1/1 100% 通过（退出码 0）。

3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/02_configure.log`
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/03_build.log`
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/04_focused_cases.log`
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/05_host_regression.log`
   - `docs/evidence/minimc_v2/V2-P04A/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**`。
- 未触碰头文件 `codec.h` 或 CMakeLists 文件。
- 回退范围：若本票被退回，仅需通过 `git checkout` 恢复 `soc-ap/core/forward/minimc/codec.cpp` 并清理证据目录，无任何上游污染。
- 提审申请：实现与全套 CRC 用例验证全部通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请将任务卡状态推进至 `Review` 并由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立评审。
