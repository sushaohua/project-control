# 单票实际执行记录: V2-P01C (Run 1)

```yaml
task_id: V2-P01C
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
lease_id: lease_v2_p01c_20261026_01
start_end_time:
  start_time: "2026-10-26T15:31:20+08:00"
  end_time: "2026-10-26T15:48:30+08:00"
start_time: "2026-10-26T15:31:20+08:00"
end_time: "2026-10-26T15:48:30+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: ad0398e20d3645dbfa37bfd0550ded0828d018b2
workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
input_versions:
  - predecessor_task: V2-P01A
    accepted_version: "sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/qa_review_report.md"
  - predecessor_task: V2-P01B
    accepted_version: "sha256:25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/qa_review_report.md"
  - protocol_path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    protocol_revision: 2.0.3
    protocol_sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  - repo: soc-ap
    commit: 849135ee69500e7e96ee75eed73c245e1ac94851
  - repo: test_harness
    commit: ad0398e20d3645dbfa37bfd0550ded0828d018b2
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  test_harness_diff: "test_harness/test_cases/minimcproto/vectors.json (new file, 48365 bytes, sha256:6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995)"
  soc_ap_diff: "clean (no modifications)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T15:32:20+08:00"
    end_time: "2026-10-26T15:32:41+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/01_precheck.log
    actual_case_count: 4
    warning_count: 0
  - id: fixtures
    command: "python3 -m json.tool test_harness/test_cases/minimcproto/vectors.json > /dev/null"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T15:47:29+08:00"
    end_time: "2026-10-26T15:48:14+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/02_fixtures.log
    actual_case_count: 58
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 -m json.tool test_harness/test_cases/minimcproto/vectors.json > /dev/null"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/02_fixtures.log
candidate_commit: null
candidate_commit_or_diff_sha256: "sha256:6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
candidate_diff_sha256: "6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995"
artifact_hashes:
  - path: test_harness/test_cases/minimcproto/vectors.json
    size: 48365
    sha256: 6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995
actual_cases:
  - "golden_frames: 完整保留 V01(14B, CRC 0x1EF9)、V02_INBOUND(18B, CRC 0xB066)、V02_OUTBOUND(18B, CRC 0x3073)、V03(25B, CRC 0xDAA0)、V04(14B, CRC 0xC13D，显式标记 frame_valid=true / command_valid=false / OQ-01 载荷长度冲突)"
  - "stub (4 cases: STUB-001..004): 覆盖桩阶段 crc/encode/decode/feed 显式返回 not_implemented 断言"
  - "crc (9 cases: CRC-001..009): 覆盖 '123456789'(0x29B1)、空输入(0xFFFF)、五条原稿黄金帧、CRC=0x0000 合法输入及空指针非零长度拒绝"
  - "encode (8 cases: ENC-001..008): 覆盖 V01(0B)、V02(4B PING)、PONG(12B)、VERSION_REPORT(16B)、最大 1024B 载荷帧，以及 L=1025 超 MTU、输出缓冲少 1B、空载荷指针非零长度拒绝"
  - "decode_bounds (6 cases: DBND-001..006): 覆盖 0B、11B、13B 过短输入、L=1025 超 MTU、实际字节数与 L+14 不符（截断与超长）"
  - "decode (12 cases: DEC-001..012): 覆盖 V01~V04（V04 仅结构有效）、CRC=0x0000 帧、1024B 最大载荷帧，以及坏 SOF、坏 CRC、错版本(flags=0x01)、非零保留位(flags=0x25)、非法互斥路由控制(route_ctrl=0x03)"
  - "stream_sync (5 cases: SYNC-001..005): 覆盖噪声丢弃、单 0x55 进入 WAIT_SOF2、连续 0x55 0x55 0xAA 前导同步、非 AA 复位及 reset 幂等"
  - "stream_header (5 cases: SHDR-001..005): 覆盖 11B 未满头不读 L、12B 头 L=0 转 READ_CRC、L=4/L=1024 转 READ_PAYLOAD、L=1025 触发 err_mtu 立即复位 WAIT_SOF1"
  - "stream_payload (5 cases: SPLD-001..005): 覆盖 V01 逐字节送入、V02 入站+出站分片粘连双帧、1024B 最大帧流式送入、CRC 高字节未到不分发、坏 CRC 静默丢弃复位"
  - "timeout (6 cases: TMO-001..006): 覆盖 49ms/50ms 不超时、51ms 超时复位、超时后当前 0x55 作为新 SOF1（先检后刷）、uint32_t 回绕以及空闲态轮询不重复累加"
  - "recovery (4 cases: REC-001..004): 覆盖坏 CRC、L=1025 超 MTU、错版本、噪声+重复 SOF+截断超时后紧接合法帧完整恢复且仅输出合法帧"
warnings:
  - "V04 急停向量 (Len=0x0000) 在 golden_frames 与 DEC-005 中均显式标记为 frame_valid=true, command_valid=false (OQ-01)，禁止作为合法急停业务执行样例"
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要非作者独立审阅者 ARCH (1c634be7-4be2-4743-af02-dc8ada31bad3) 对 vectors.json 执行独立评审与签署"
  - "独立参考校验器脚本将在下游 V2-P01D 实现并执行数学复核"
reviewed_version: null
review_decision: null
independent_review:
  reviewer_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
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

本微步任务卡 `V2-P01C` 由独立 QA 会话（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）作为作者执行，严格限制在 `write_scope` 内：
1. **独立测试向量文件**: [vectors.json](file:///home/sushaohua/workspace/ai_soc_project/test_harness/test_cases/minimcproto/vectors.json)
   - 文件大小：`48,365` 字节
   - 文件 SHA256：`6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995`
   - 包含顶层 `schema_version` (`minimcproto-vectors-v2.0.3-r1`)、`protocol_sha256` (`9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`) 及前置已验收契约 `V2-P01A`、`V2-P01B` 的精确哈希引用。
   - 完整保留 5 条原稿黄金向量（`V01`, `V02_INBOUND`, `V02_OUTBOUND`, `V03`, `V04`）及独立复算的小端 `CRC-16/CCITT-FALSE` 值，其中 `V04` 明确标注为物理帧结构有效（`frame_valid: true`）、业务命令载荷长度冲突（`command_valid: false`, `OQ-01`）。
   - 提供 `stub` 辅助组（4 条）与 9 个正式功能分组（`crc` 9 条、`encode` 8 条、`decode_bounds` 6 条、`decode` 12 条、`stream_sync` 5 条、`stream_header` 5 条、`stream_payload` 5 条、`timeout` 6 条、`recovery` 4 条），合计 **54 条用例 + 5 条黄金基准向量**，每条均具备唯一 `case_id`、`raw_hex`、固定输入与不依赖生产实现的明确预期。
2. **执行证据与原始日志**:
   - [01_precheck.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/01_precheck.log)
   - [02_fixtures.log](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/02_fixtures.log)
   - [result.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/result.md)

### 2. 边界合规与回退说明

- 未触碰 `soc-ap/**`、`mcu-p3/**` 或 `project-control/.agents/**` 正式任务卡状态。
- 如需回退本票改动，仅需移除 `test_harness/test_cases/minimcproto/vectors.json` 与 `project-control/docs/evidence/minimc_v2/V2-P01C/runs/run_20261026_01/`。
- 现将 `V2-P01C` (`run_20261026_01`) 交付物提交给 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请转入 `Review` 阶段由独立审阅者 ARCH（`1c634be7-4be2-4743-af02-dc8ada31bad3`）执行独立评审。
