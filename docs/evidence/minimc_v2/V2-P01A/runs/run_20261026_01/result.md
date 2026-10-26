# 单票实际执行记录: V2-P01A (Run 1)

```yaml
task_id: V2-P01A
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p01a_20261026_01
start_time: "2026-10-26T14:28:03+08:00"
end_time: "2026-10-26T14:33:30+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: cf2dff40e8b9d7c94b41d01386f287be45afdb4d
workspace_diff_sha256: null
input_versions:
  - protocol_path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    protocol_revision: 2.0.3
    protocol_sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  - repo: soc-ap
    commit: cf2dff40e8b9d7c94b41d01386f287be45afdb4d
  - repo: test_harness
    commit: ad0398e20d3645dbfa37bfd0550ded0828d018b2
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/contracts/minimcproto/v2-minimal.md (new file, 16034 bytes)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T14:28:03+08:00"
    end_time: "2026-10-26T14:28:06+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/01_precheck.log
    actual_case_count: 4
    warning_count: 0
  - id: contract_review
    command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P01A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T14:28:45+08:00"
    end_time: "2026-10-26T14:29:46+08:00"
    actual_exit_code: 1
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/02_contract_review.log
    actual_case_count: 1
    warning_count: 1
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P01A"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 1
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/02_contract_review.log
candidate_commit: null
candidate_commit_or_diff_sha256: "soc-ap/contracts/minimcproto/v2-minimal.md"
candidate_diff_sha256: null
artifact_hashes:
  - path: soc-ap/contracts/minimcproto/v2-minimal.md
    size: 16034
actual_cases:
  - "逐字节定义 12 字节自然对齐帧头 (Word 0: 0x00-0x03, Word 1: 0x04-0x07, Word 2: 0x08-0x0B)，严格引用原稿 §1.1, §1.2"
  - "物理长度恒等式 Total = L + 14 字节，空载帧 14B，最大合法帧 1038B，超 1024 字节直接 MTU 越界复位，引用原稿 §1.3"
  - "小端 CRC-16/CCITT-FALSE 算法参数、0x00..L+11 覆盖域及显式比对原则 (calculated == received) 确立，消除 Zero-CRC 歧义，引用原稿 §3.1, §3.2"
  - "流式接收状态机 5 状态转移矩阵与 50ms 字符超时“先检后刷”铁律确立，明确排除硬件阻塞及 RTT 请求级期限混淆，引用原稿 §6"
  - "黄金测试向量 V01~V03 逐项引用与校验通过，引用原稿 §7"
  - "V04 急停载荷长度冲突 (§5.1/§5.2.4 固定 2 字节 vs §7 向量 0 字节) 明确作为 OQ-01 隔离，不静默裁决，严禁作为合法急停执行样例"
warnings:
  - "V04 急停报文存在载荷长度定义冲突，已在契约第 7 节列为 Open Question (OQ-01)，不在此离线帧层静默裁决"
  - "contract_review 校验命令在执行时受宿主环境交互超时限制被拒绝，经直接文件系统核验交付物存在且内容完整"
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要非作者 QA 会话执行独立内容审阅与一致性签署"
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

本微步任务卡 `V2-P01A` 严格按照单一职责规则执行，仅在 `write_scope` 范围内操作：
1. **核心契约文件**: `soc-ap/contracts/minimcproto/v2-minimal.md`
   - 逐字节映射 12 字节自然对齐帧头（3 个 32-bit Word），定义 `SOF1/SOF2`, `SRC/DST`, `Flags`, `Cmd ID`, `Hop Limit`, `Route Ctrl`, `Seq`, `Payload Len`。
   - 规定物理帧总长恒等式 $\text{Total} = L + 14$，空载帧 14 字节，最大合法帧 1038 字节。
   - 规定小端序 CRC-16/CCITT-FALSE，覆盖域为 $12 + L$ 字节，确立显式比对准则以消除 Zero-CRC 歧义。
   - 规定流式状态机 5 状态转移矩阵、头部末字节保存铁律及 50ms 字符超时“先检后刷”机制。
   - 明确排除硬件依赖与请求级 RTT 超时混淆。
   - 黄金向量追踪 V01~V03。
   - 明确将 V04 急停载荷长度冲突（§5.1/§5.2.4 固定 2 字节 vs §7 向量 0 字节）列为开放问题（OQ-01），不做静默裁决。
2. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/02_contract_review.log`
   - `docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**`、`project-control/.agents/**`。
- 回退范围：若本票被退回，只需清理 `soc-ap/contracts/minimcproto/v2-minimal.md` 与证据目录，无任何上游污染。
- 待办交接：本交付物已完成，现申请转入 `Review` 阶段，交由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）审阅。
