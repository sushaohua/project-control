# 单票实际执行记录: V2-P01B (Run 1)

```yaml
task_id: V2-P01B
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p01b_20261026_01
start_time: "2026-10-26T15:19:22+08:00"
end_time: "2026-10-26T15:22:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 5949bcae6ccc3813e025d2702caf7150d6a79f95
workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
input_versions:
  - predecessor_task: V2-P01A
    accepted_version: "sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/qa_review_report.md"
  - protocol_path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    protocol_revision: 2.0.3
    protocol_sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  - repo: soc-ap
    commit: 5949bcae6ccc3813e025d2702caf7150d6a79f95
  - repo: test_harness
    commit: ad0398e20d3645dbfa37bfd0550ded0828d018b2
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/contracts/minimcproto/v2-commands.md (new file, 14491 bytes)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T15:19:22+08:00"
    end_time: "2026-10-26T15:19:39+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/01_precheck.log
    actual_case_count: 4
    warning_count: 0
  - id: contract_review
    command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P01B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T15:20:58+08:00"
    end_time: "2026-10-26T15:21:09+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/02_contract_review.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P01B"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/02_contract_review.log
candidate_commit: null
candidate_commit_or_diff_sha256: "soc-ap/contracts/minimcproto/v2-commands.md"
candidate_diff_sha256: null
artifact_hashes:
  - path: soc-ap/contracts/minimcproto/v2-commands.md
    size: 14491
actual_cases:
  - "逐字段定义 GET_VERSION(0x01, 0B)、VERSION_REPORT(0x02, 16B)、PING(0x03, 4B)、PONG(0x04, 12B) 的端序与字段结构"
  - "确立请求(WANTS_ACK=1, IS_RESPONSE=0)与响应(IS_RESPONSE=1, WANTS_ACK=0)标志位对应关系及 seq 回显语义"
  - "定义帧级物理验证与命令业务级验证两层判定模型（帧级失败静默丢弃复位状态机，命令级失败回送标准 NACK）"
  - "形式化定义 boot_id (Session Epoch) 用于重启隔离检测与上下文重置"
  - "形式化定义 seq 模 65536 停等事务控制、乱序超前丢弃与历史重传幂等回发机制"
  - "负向范围明确排除急停、OTA、切片流、复杂会话运行时及物理硬件时钟"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行内容审查与会签"
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

本微步任务卡 `V2-P01B` 严格按照单一职责规则执行，仅在 `write_scope` 范围内操作：
1. **核心契约文件**: `soc-ap/contracts/minimcproto/v2-commands.md`
   - 逐字段定义 `CMD_GET_VERSION` (`0x01`, 0B)、`CMD_VERSION_REPORT` (`0x02`, 16B)、`CMD_PING` (`0x03`, 4B)、`CMD_PONG` (`0x04`, 12B) 的结构体、Little-Endian 端序与字节偏移表。
   - 确立两层校验模型：第 1 层帧级物理验证（依据 `V2-P01A`，错误静默丢弃复位 FSM），第 2 层命令业务级验证（操作码支持度、载荷长度强校验、保留位断言，错误回发标准 NACK）。
   - 确立 `boot_id` (Session Epoch) 用于跨重启会话重置隔离，确立 `seq` (16-bit 模 65536) 用于单在途停等管理与幂等回显。
   - 负向范围严格排除急停、OTA、切片作业流、复杂重试定时器及物理硬件调用。
2. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/02_contract_review.log`
   - `docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`project-control/.agents/**`。
- 回退范围：若本票被退回，仅需清理 `soc-ap/contracts/minimcproto/v2-commands.md` 与证据目录，无任何上游污染。
- 提审申请：本交付物已完成，现申请转入 `Review` 阶段，交由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）审阅。
