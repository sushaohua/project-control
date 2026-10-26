# 微步任务卡 V2-P01B 独立过程审计与结果验收报告 (Independent QA Review Report)

```yaml
review_metadata:
  task_id: V2-P01B
  task_title: 提取版本与心跳命令契约
  task_revision: 1
  plan_revision: marlin-r2-v2-offline-1
  reviewed_run_id: run_20261026_01
  reviewer_role: QA
  reviewer_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
  executor_role: ARCH
  executor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
  coordinator_session: 9e5411f4-acad-421e-b487-9e68b9483320
  review_timestamp: "2026-10-26T15:28:30+08:00"
  reviewed_artifact:
    path: soc-ap/contracts/minimcproto/v2-commands.md
    size_bytes: 14491
    total_lines: 244
    sha256: 25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4
  consumed_predecessor:
    task_id: V2-P01A
    accepted_version: sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade
    acceptance_evidence: docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/qa_review_report.md
  authoritative_protocol_baseline:
    path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    revision: 2.0.3
    sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  reviewed_evidence_files:
    - path: project-control/docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/result.md
      sha256: 81de729feaec1164314fba2cd3ec32edd97cd2f3012519d2ba6b965be698c524
    - path: project-control/docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/01_precheck.log
      sha256: 6d8d04bc2edf10357645ffd94e0c46984c022871df7419e8f152d47962463b24
    - path: project-control/docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/02_contract_review.log
      sha256: dbaeea33f76aab1c8d227ebb1ac79f5d2e9984d16a6bcc5a6ac41fbaec2cb3c5
  verdict: APPROVED
```

---

## 1. 角色隔离、前置绑定与工作区边界审计 (Process & Scope Audit)

1. **三权分立与租约核验 (`PASS`)**：
   - **编排者 (COORD)**：`9e5411f4-acad-421e-b487-9e68b9483320`
   - **执行作者 (ARCH)**：`1c634be7-4be2-4743-af02-dc8ada31bad3`（租约 `lease_v2_p01b_20261026_01`，有效期至 `2026-10-26T16:30:00+08:00`）
   - **独立审阅者 (QA)**：`663fcda3-b02b-4d3a-89f6-ffc1ef283810`（本独立子 Agent 会话，与作者及 COORD 完全隔离）

2. **前置依赖版本绑定核验 (`PASS`)**：
   - [V2-P01B.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/minimc_v2/V2-P01B.md) 与 [result.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/result.md) 均准确绑定已通过独立 QA 验收的前置 `V2-P01A` 交付物版本 `sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade` 及验收报告 `docs/evidence/minimc_v2/V2-P01A/runs/run_20261026_01/qa_review_report.md`。

3. **独立验证命令与工作区边界核验 (`PASS`)**：
   - 本 QA 会话独立执行 `python3 project-control/tools/check_task_graph.py --workspace . --check-artifact V2-P01B`：
     - 退出码：`0`
     - `errors`: `[]`
     - `artifact_hashes`: `{"soc-ap/contracts/minimcproto/v2-commands.md": "25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4"}`
   - 独立检查四仓 `git status --porcelain=v1` 与 `HEAD`：
     - `soc-ap`: HEAD 为 `5949bcae6ccc3813e025d2702caf7150d6a79f95`（与任务卡 `base_commit` / `dispatch_binding.source_commit` 一致），工作区仅新增 `?? contracts/minimcproto/v2-commands.md`；
     - `mcu-p3`: HEAD 为 `14b8057b04030bd659744c874c73ff8f09f29979`，工作区干净（无任何修改）；
     - `test_harness`: HEAD 为 `ad0398e20d3645dbfa37bfd0550ded0828d018b2`，工作区干净（无任何修改）；
     - `project-control`: HEAD 为 `70dbb6f44a2fd830b1cbf19f26de9792867a063b`，仅包含任务卡派单状态更新与 `docs/evidence/minimc_v2/V2-P01B/` 证据目录。
   - **结论**：开发严格限制在 `write_scope` 允许范围内，无任何越界修改。

---

## 2. 正反验收判据逐项核对 (Acceptance Criteria Verification)

对照 [V2-P01B.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/.agents/kanban/microtasks/minimc_v2/V2-P01B.md) 与权威基线 [ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md)（Rev 2.0.3），对交付物 [v2-commands.md](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/contracts/minimcproto/v2-commands.md) 逐项审计如下：

| 序号 | 验收维度 / 判据类型 | 任务卡与规范要求 | 交付物落位章节与内容核验 | 结果 |
| :--- | :--- | :--- | :--- | :--- |
| **P-01** | 正向判据：4 条核心命令的字段、端序与响应关系 | `GET_VERSION` 0B、`VERSION_REPORT` 16B、`PING` 4B、`PONG` 12B 的字段/端序/响应关系明确 | **§3.1–§3.4 (L63–L177) & §5 (L210–L244)**：<br>1. `CMD_GET_VERSION (0x01)`：AP$\to$从机，`flags=0x05 (WANTS_ACK\|VER_2_0)`，`payload_len=0`（总长 14B），预期应答 `CMD_VERSION_REPORT (0x02)`，并追踪 V01 黄金向量；<br>2. `CMD_VERSION_REPORT (0x02)`：从机$\to$AP，`flags=0x06 (IS_RESPONSE\|VER_2_0)`，`seq` 严格回显原请求 `seq`，固定 16B 小端紧凑结构体（`proto_ver_major=2`, `proto_ver_minor=0`, `firmware_major`, `firmware_minor`, `boot_id` u32 LE, `git_commit_short` u32 LE, `capability_flags` u32 LE，总长 30B）；<br>3. `CMD_PING (0x03)`：双向请求，`flags=0x05`，固定 4B 小端载荷（`t_originate_ms` u32 LE，总长 18B），预期应答 `CMD_PONG (0x04)`，并追踪 V02 入站黄金向量；<br>4. `CMD_PONG (0x04)`：双向响应，`flags=0x06`，`seq` 回显原请求 `seq`，固定 12B 小端紧凑结构体（`t_originate_ms` u32 LE, `t_receive_ms` u32 LE, `planner_buf_free` u8, `rx_fifo_free_units` u8, `reserved` u16 LE 置 0 且接收断言 0，总长 26B）。完全对齐原稿 §5.1, §5.2.2, §5.2.3, §7。 | **PASS** |
| **P-02** | 正向判据：两层判定模型（帧级 vs 命令级） | 明确帧结构有效与业务命令有效分别判定 | **§2 & §2.1 (L25–L60)**：<br>• 第 1 层（帧级物理验证，依据 `V2-P01A`）：检验 SOF、总长 `L+14`、MTU `0..1024`、主版本位 `(flags & 0x0C) == 0x04`、头部保留位 `(flags & 0xE0) == 0`、小端 CRC-16 显式比对；**失败时静默丢弃并复位 FSM，严禁回送任何应答**；<br>• 第 2 层（命令业务级验证）：在帧级通过后检验 `cmd_id` 支持性、载荷长度严格匹配固定规约、请求/响应标志位语义、响应 `seq` 回显一致性及载荷 `reserved == 0`；**对非法请求帧回发标准 `CMD_NACK`（`MINIMC_ERR_UNKNOWN_CMD=0x04` 或 `MINIMC_ERR_COMMAND_REJECTED=0x06`）**。 | **PASS** |
| **P-03** | 正向判据：`boot_id` 与 `seq` 用途规约 | 列出 `boot_id` 和 `seq` 用途 | **§4.1–§4.2 (L180–L207)**：<br>• `boot_id` (`Session Epoch`)：节点冷启动/复位生成的 32-bit 标识，通过 `GET_VERSION`/`VERSION_REPORT` 同步；若与已记录 `session_epoch` 不一致则判定对端重启，立即清空未决请求与缓存并重置会话序列号（对齐原稿 §4.1.1）；<br>• `seq` (`Sequence Number`)：可靠请求按 16-bit 模 65536 单调自增消耗 `tx_seq`，遵循单在途停等 (`In-Flight Limit = 1`)；响应帧原样回显 `req.seq` 不消耗计数；接收端使用 `(uint16_t)(seq_recv - seq_expected)` 区分有序新帧 (`0`)、超前乱序 (`1..32767` $\to$ `0x03`)、半周期歧义 (`32768` $\to$ `0x09`) 与历史重传 (`32769..65535` $\to$ 缓存重发或 `0x08`)（对齐原稿 §4.1.2–§4.1.5）。 | **PASS** |
| **N-01** | 反向判据：排除急停/OTA/运动等非目标命令 | 急停/OTA/运动命令不列入本增量已实现能力 | **§1.2 (L18–L19)**：明确声明 `CMD_EMERGENCY_STOP`、`CMD_OTA_*`、`CMD_STREAM_CHUNK`、`CMD_TELEMETRY_REPORT`、`CMD_ALARM_EVENT` 等高级业务指令不属于本卡范围，不实现、不伪造支持。 | **PASS** |
| **N-02** | 反向判据：排除复杂会话运行时与硬件时钟依赖 | 会话重试、重启隔离等未实现内容明确留到后续，不伪造设备支持；无硬件依赖 | **§1.2 (L20–L22)**：明确将会话重试定时器、指数退避、重启隔离在途事务清空与路由转发表状态机留待后续票，本契约仅约束静态字段布局与数据契约；明确时间戳为离线逻辑参数，禁止调用硬件 RTC 或物理外设。 | **PASS** |

---

## 3. 执行记录 (`result.md`) 与下游交接核查

1. [result.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/result.md) 包含 `V2-P01B.md` 要求的全部 15 项必填字段，命令日志路径、退出码（`precheck: 0`, `contract_review: 0`）与原始日志文件完全一致。
2. 建议 COORD 在完成 `V2-P01B` 收件与状态更新（`Review -> Verify/Done`）时，将以下已核验版本信息绑定至 `V2-P01B.md`、`result.md` 及下游依赖卡（`V2-P01C`, `V2-P01D`, `V2-P02B`）：
   - `reviewed_artifact_version`: `sha256:25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4`
   - `acceptance_evidence`: `docs/evidence/minimc_v2/V2-P01B/runs/run_20261026_01/qa_review_report.md`
   - `review_decision`: `APPROVED`

---

## 4. 独立 QA 终审裁决与签署 (Final Verdict & Signature)

- **终审裁决 (Final Verdict)**：**`APPROVED`**
- **签署会话 (Reviewer Session)**：`663fcda3-b02b-4d3a-89f6-ffc1ef283810` (Independent QA Subagent)
- **签署时间 (Signed At)**：`2026-10-26T15:28:30+08:00`
