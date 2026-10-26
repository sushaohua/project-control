# 微步任务卡 V2-P01A 独立过程审计与结果验收报告 (Independent QA Review Report)

```yaml
review_metadata:
  task_id: V2-P01A
  task_title: 提取帧格式最小契约
  task_revision: 1
  plan_revision: marlin-r2-v2-offline-1
  reviewed_run_id: run_20261026_01
  reviewer_role: QA
  reviewer_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
  executor_role: ARCH
  executor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
  coordinator_session: 9e5411f4-acad-421e-b487-9e68b9483320
  review_timestamp: "2026-10-26T14:53:00+08:00"
  reviewed_artifact:
    path: soc-ap/contracts/minimcproto/v2-minimal.md
    size_bytes: 16034
    total_lines: 242
    sha256: 5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade
  authoritative_protocol_baseline:
    path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    revision: 2.0.3
    sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  reviewed_evidence_files:
    - project-control/docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/result.md
    - project-control/docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/01_precheck.log
    - project-control/docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/02_contract_review.log
  verdict: APPROVED
```

---

## 1. 角色隔离与过程合规性审计 (Process & Role Isolation Audit)

1. **会话三权分立核验**：
   - **编排与派单者 (COORD)**：`9e5411f4-acad-421e-b487-9e68b9483320`
   - **单票执行作者 (ARCH)**：`1c634be7-4be2-4743-af02-dc8ada31bad3`（持有租约 `lease_v2_p01a_20261026_01`，有效期至 `2026-10-26T15:30:00+08:00`）
   - **独立审阅者 (QA)**：`663fcda3-b02b-4d3a-89f6-ffc1ef283810`（本独立子 Agent 会话，与作者及 COORD 物理隔离）
   - **结论**：符合 [minimc_v2_task_execution.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/guides/minimc_v2_task_execution.md)“作者、QA 作者及其 Reviewer 都不能对自己的交付独立签署”的硬性规定。

2. **写入范围与工作区边界核验 (`write_scope` & Git Status)**：
   - 经核查 `01_precheck.log`、`result.md` 与任务卡 [V2-P01A.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/minimc_v2/V2-P01A.md)：
     - 开工前 `soc-ap` HEAD 为 `cf2dff40e8b9d7c94b41d01386f287be45afdb4d`，`test_harness` HEAD 为 `ad0398e20d3645dbfa37bfd0550ded0828d018b2`，工作树干净（与派单绑定 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` 空 diff 一致）；
     - 执行者仅在 `soc-ap` 下新建 `soc-ap/contracts/minimcproto/v2-minimal.md`（16,034 字节，242 行），并在 `project-control/docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/` 下写入本次运行日志与执行记录；
     - 未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**` 等禁止路径。
   - **关于命令交互权限超时的如实记录说明**：
     - 在 `02_contract_review.log` 及本 QA 会话尝试调用非沙箱命令行时，宿主终端交互授权提示（permission prompt）因无人值守等待超时（60s）返回拒绝。
     - 执行者在 `result.md` 中如实将 `contract_review` 记录为 `actual_exit_code: 1` 并保留原始日志，未伪造 `0` 退出码；本 QA 会话直接通过只读文件系统工具完整读取了 [check_task_graph.py](file:///home/sushaohua/workspace/ai_soc_project/project-control/tools/check_task_graph.py) 的 `artifact_check` 逻辑（第 197–217 行：检查 `soc-ap/contracts/minimcproto/v2-minimal.md` 文件存在且非空）以及交付物全文（242 行，16,034 字节 > 0），确认该交付物完全满足 `artifact_check` 的全部断言条件。

---

## 2. 交付物正反判据逐项核对 (Acceptance Criteria Verification)

对照 [V2-P01A.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/minimc_v2/V2-P01A.md) 的 `verification.positive_cases` 与 `verification.negative_cases`，以及权威协议基线 [ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)（Rev 2.0.3），对 [v2-minimal.md](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/minimcproto/v2-minimal.md) 逐项核验如下：

| 序号 | 验收维度 / 判据类型 | 任务卡要求 | 交付物落位章节与内容核验 | 结果 |
| :--- | :--- | :--- | :--- | :--- |
| **P-01** | 正向判据：12 字节帧头逐字节定义 | 逐字节定义 12 字节自然对齐帧头，引用原稿章节 | **§2.1–§2.4 (L24–L96)**：完整定义 3 个 32-bit Word 共 12 字节偏移（`0x00: sof_1=0x55`, `0x01: sof_2=0xAA`, `0x02: src_id`, `0x03: dst_id`, `0x04: flags`, `0x05: cmd_id`, `0x06: hop_limit`, `0x07: route_ctrl`, `0x08..0x09: seq` LE, `0x0A..0x0B: payload_len` LE），载荷起始于 `0x0C`（32-bit 对齐边界），准确引用原稿 §1.1, §1.2, §1.3, §1.4, §2.1, §2.2, §4.1, §5.1, §8。 | **PASS** |
| **P-02** | 正向判据：`L + 14` 总长与 `0..1024` 载荷边界 | 定义 `L+14` 物理帧总长、`0..1024` 载荷边界及越界处置 | **§3 (L99–L110)**：明确给出 $\text{Frame\_Total\_Length} = 12 + L + 2 = L + 14$ 字节；最小空载帧 $L=0$ 为 14 字节，最大合法帧 $L=1024$ 为 1038 字节 (`MINIMC_MAX_FRAME_SIZE`)；候选 $L > 1024$ 判定为 `MINIMC_ERR_MTU_EXCEEDED` 并立即终止接收、复位至 `STATE_WAIT_SOF1`，引用原稿 §1.3。 | **PASS** |
| **P-03** | 正向判据：小端 CRC-16 参数与覆盖域 | 定义小端 CRC-16 算法参数、覆盖域及显式比对规则 | **§4.1–§4.2 (L113–L136)**：准确定义 `CRC-16/CCITT-FALSE`（Poly `0x1021`, Init `0xFFFF`, RefIn `False`, RefOut `False`, XorOut `0x0000`）；覆盖域为偏移 `0x00` 至 $L+11$ 共 $12+L$ 字节；线缆小端序（$L+12$ 为低字节，$L+13$ 为高字节）；强制要求显式比对 `calculated_crc == received_crc`，禁止小端下隐式零残差检验，引用原稿 §3.1, §3.2。 | **PASS** |
| **P-04** | 正向判据：版本/保留位检查与流式错误恢复边界 | 固定帧级错误、版本/保留位检查及错误后恢复边界，逐项引用原稿章节 | **§2.3, §2.4, §5.1, §5.2, §6 (L70–L96, L140–L215)**：<br>1. `Flags` 版本位硬校验 `(flags & 0x0C) != 0x04` 丢弃复位，保留位 `0xE0` 非零非法；<br>2. `Route_Ctrl` 互斥位 `(route_ctrl & 0x03) == 0x03` 判定非法并累加 `err_route_invalid_ctrl`；<br>3. 完整给出 5 状态转移矩阵（`WAIT_SOF1`, `WAIT_SOF2`, `READ_HEADER`, `READ_PAYLOAD`, `READ_CRC`），包含 `WAIT_SOF2` 连续收到 `0x55` 保持同步、`count == 9` 先保存 `header_raw[9] = B` 再判长度、50ms 字符超时“先检后刷”(`state != STATE_WAIT_SOF1 && (now_ms - last_byte_rx_ms) > 50ms`) 铁律及 CRC Guard 顺序；<br>4. 完整追踪 V01、V02 入站、V02 出站、V03 黄金向量，引用原稿 §6, §7。 | **PASS** |
| **N-01** | 反向判据：V04 急停载荷长度冲突保留为 Open Question | 未知或冲突写为 Open Question，不静默裁决 V04 急停长度 | **§1.2 (L20) & §7 OQ-01 (L218–L238)**：明确指出原稿 §5.1 / §5.2.4 定义 `CMD_EMERGENCY_STOP (0x12)` 为固定 2 字节（`uint16_t reason_code`），而原稿 §7 黄金向量 V04 为 `Len=0x0000`（0 字节载荷，14 字节总长）；明确将此冲突保留为 `OQ-01`，不静默裁决，规定物理帧层按通用 $0 \le L \le 1024$ 判定帧结构有效，但严禁将 V04 作为合法业务急停执行样例。 | **PASS** |
| **N-02** | 反向判据：不混淆 50ms 超时与请求级期限，无硬件操作 | 不把 50ms 字节超时当请求级期限，不引入硬件操作 | **§1.2 (L17–L19) & §5.2 (L167–L172)**：明确声明协议层为纯内存/纯数据流操作，禁止调用任何 Linux UART 驱动、GPIO 或硬件外设接口；明确 50ms 仅为流式串口字符间超时（inter-byte timeout），严禁将其作为 RPC 或请求-响应往返（RTT）期限。 | **PASS** |

---

## 3. 执行记录 (`result.md`) 完备性核查与治理建议

1. **必填字段核查**：
   - [result.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/result.md) 包含 `V2-P01A.md` 规定的全部 15 项 `required_record_fields`（`task_id`, `task_revision`, `actor_session`, `start_end_time`, `input_versions`, `worktree_and_diff`, `commands_cwd_exit_codes`, `raw_log_paths`, `candidate_commit_or_diff_sha256`, `actual_cases`, `warnings`, `failures_and_corrections`, `reviewed_version`, `review_decision`, `handoff_ack`）。
2. **下游绑定与收件回填建议（供 COORD 收件关单时使用）**：
   - 建议 COORD 在更新 `V2-P01A.md` 状态（`Review -> Verify/Done`）及回填 `result.md` 的 `reviewed_version` / `independent_review` 字段时，显式写入已核实的交付物 SHA256：
     - `soc-ap/contracts/minimcproto/v2-minimal.md`: `sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade`
   - 下游依赖 `V2-P01A` 的微步任务卡（`V2-P01B`, `V2-P01C`, `V2-P02A`）在派单绑定 `dependency_conditions` 时，应将该 SHA256 与本验收报告路径一并绑定为 `accepted_version` 与 `acceptance_evidence`。

---

## 4. 独立 QA 终审裁决与签署 (Final Verdict & Signature)

- **终审裁决 (Final Verdict)**：**`APPROVED`**
- **签署会话 (Reviewer Session)**：`663fcda3-b02b-4d3a-89f6-ffc1ef283810` (Independent QA Subagent)
- **签署时间 (Signed At)**：`2026-10-26T14:53:00+08:00`
