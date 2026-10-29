---
template_version: '2026-10-27'
review_id: AUTO-02-run_07-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-auto-02
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
decision: REJECTED
reviewed_artifact_version: "project-control=dbc8e65b29b39d44b2616b2eed31aaac7da9fbd0; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_07/result.md
  sha256: 276e17665f5fffc155cd3aea4199be0f726c3b61734597b364769bd5b2e17483
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_07/result.md
    sha256: 276e17665f5fffc155cd3aea4199be0f726c3b61734597b364769bd5b2e17483
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: 6624e3bf13099f0c59085c72d99262ee9f88920ae87c7e8e26fa846126fc9bc5
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 52ff3240a67380756dca9b6d84883f885229fbf0b2cc28487a901abc3122be40
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: e4eba48cd2df15c4bc3767c42d0c03cd87b017899914ad4442bc464f7c0dcd3b
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_07/server_qa.json
  sha256: e31406f3864caa13da51f39df182f48008a2c2f35bf3c2792758553aa01638bc
  container_id: 2cf8d027bc6210bcd45d0725ce4272bbe22bc239197f9cd7af10a5569bede926
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
reviewer_session: null
reviewer_session_evidence: null
reviewer_token_evidence: null
content_audit:
  fact_sources:
    result: passed
    basis: server_lock.json、checkout.log 与 server_qa.json 绑定所列远端 URL/ref/full commit；本地候选 Git 对象的 HEAD 也与锁定 SHA 一致。未对远端服务器作本轮实时查询。
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: passed
    basis: 本报告只对锁定候选代码与随附服务端运行记录作结论；不据此宣称常驻服务已部署。
  architecture_completeness:
    result: failed
    basis: server QA task_revision 缺失时可绕过版本一致性门禁；ARCH 报告复核缺少 QA 报告内容/哈希绑定。
---

# AUTO-02 run_07 独立 QA 审查报告

## 决定

**REJECTED**。候选未满足任务修订号的强制一致性门禁。`state_machine.py` 的 `_validate_server_qa_proof` 读取 `task_revision` 后，仅在该值非 `None` 时比较；若证据缺失此字段，校验会继续通过。任务要求严格验证 `server_qa.get("task_revision") == record.task_revision`，因此当前实现允许缺少修订号的证据通过，是实质性 fail-open。

位置：`project-control/tools/coord_runner/state_machine.py` 中 `_validate_server_qa_proof`（候选提交 `dbc8e65b29b39d44b2616b2eed31aaac7da9fbd0`）。现有测试 `test_qa_verdict_task_revision_mismatch_rejected` 只测了值不匹配（revision 6 vs 1），没有测试字段缺失应拒绝，故测试通过不能排除此缺陷。

## 审查范围与方法

审阅任务卡 revision 1、run_07 作者记录、锁定提交中的 11 个交付文件，以及 `server_lock.json`、`checkout.log`、`server_qa.json`、`server_verdict.json`、`runtime.log`。逐项对照 run_06 阻断项，重点审阅状态机强制门禁、runner 调度逻辑、服务端修订号、记录哈希与测试结果。候选代码以项目仓库 Git 对象中的锁定提交为准；本工作区另外存在未跟踪的 run_07 证据文件和 `test_harness/README.md` 修改，它们未作为候选代码审阅输入。

本轮未在宿主机重跑被审代码测试。构建、检出和测试结果仅按服务端沙箱记录审阅；本地只执行了只读哈希/源码检查和 AST 规模扫描。随附 `checkout.log` 记录从两个远端 URL 按完整 SHA fetch 后 checkout 成功；本报告没有访问服务器进行实时二次查询，也没有独立取得该 QA 服务的签名凭据。

## 逐项核验

### 1. QA 报告的非作者复核

`validate_done_acceptance` 在必需角色包含 QA 时，要求 QA 条目包含 `report_review` 字典、结论为 `APPROVED`，并要求评审身份存在且既不等于 QA 评审身份，也不等于作者身份。静态检查确认此门禁存在。对应测试覆盖了缺字段、拒绝结论、自评和作者自批情形。

`_execute_review_phase` 在当前 AUTO-02 卡片 `[QA, ARCH]` 的角色顺序下先完成 QA，再调用 `_ensure_qa_report_review`；没有合适的非作者评审时会调用 ARCH reviewer，随后填充 `report_review`。当前路径满足“发起非 QA 角色”的调度要求。

但该复核尚未绑定 QA 报告内容：`_invoke_reviewer` 只向通用 reviewer executor 提供 task ID、candidate commit 和 role；`_ensure_qa_report_review` 直接把该 ARCH 结果复制为 QA `report_review`，没有传递 QA 报告路径、哈希或正文供其复核。因此实现无法从记录证明 ARCH 实际审阅的是 QA 报告。此项应在修复时改为对 QA 报告本身执行复核并绑定报告哈希；它不是本次拒绝的唯一依据。

### 2. 纠正必须携带证据

`handle_remediation(record, reason, evidence)` 要求 evidence 为非空字典，且 `path`、`sha256` 非空；否则抛出 `GateValidationError`。QA 失败及 review 非 APPROVED 分支均调用相应 `_extract_*_failure_evidence` 并将结果交给强制入口，源码路径符合要求。

限制：提取器在输入未提供有效引用时会对内存中的 JSON/字符串计算摘要，并使用 `qa_verdict.json`、`review_report.md` 等默认路径标签；它没有在该位置持久化对应文件，也没有验证 path 指向的文件真实存在或 sha256 格式/内容匹配。因此该机制保证了结构非空，但不能单独证明引用对应可读取的原始故障物证。

### 3. 沙箱任务修订号

任务卡、`server_qa.json` 与 `server_verdict.json` 均记录 `task_revision: 1`，与任务卡 revision 1 一致。run_07 沙箱记录的具体证据本身正确。阻断点在验证器对缺字段的容忍：目前只有“存在且不匹配”才拒绝，缺失字段不拒绝，不能视为严格一致性校验，故本项未通过。

### 4. 服务端沙箱与测试记录

随附哈希实测与用户提供值一致：`result.md` 为 `276e17665f5fffc155cd3aea4199be0f726c3b61734597b364769bd5b2e17483`；`server_qa.json` 为 `e31406f3864caa13da51f39df182f48008a2c2f35bf3c2792758553aa01638bc`。server lock 列出 project-control 与 test_harness 的远端 `refs/heads/main` 及指定完整 commit；checkout 日志记录两个完整 SHA 的 fetch/checkout 均 exit 0。容器 ID、镜像 digest、状态及挂载与用户提供的标识相符，记录为无 developer mounts 的独立容器挂载。

`server_qa.json` 记录以下命令全部 exit 0：

- `python3 tools/test_coord_runner.py`：53 tests，OK。
- `python3 tools/test_qa_runner.py`：20 tests，OK。
- `python3 tools/test_delivery_checks.py`：20 tests，OK。
- `python3 tools/test_check_task_graph.py`：12 tests，OK。
- `./runner/qa_entrypoint.sh --suite all`：cascade_vectors、hil_unit 两个子套件均 PASSED。

合计 105 个 unittest 项及 2 个 harness 子套件，共 107 项检查。这里报告的是对沙箱输出记录的核验，不是本轮独立重跑结果；不据此声称完成构建（记录 build_results 为空，build_count 为 0）。

### 5. AST 规模门禁

对锁定候选 `project-control/tools/` 下 18 个 Python 文件执行只读 AST 扫描，统计 282 个同步/异步函数；按函数源码行数不超过 50、参数总数（含位置专用、普通、关键字专用及可变参数）不超过 4 的规则，发现 0 项超限。作者记录声称扫描 20 个 Python 工具文件；本轮独立扫描范围是上述 18 个文件，因此仅对该范围作确认。服务端所运行测试也包含编码规模测试，但其本轮结果依赖上述沙箱记录。

## 必须修复后复审

1. 将 `_validate_server_qa_proof` 改为无条件严格比较证据 `task_revision` 与 `record.task_revision`；缺字段、类型不匹配或值不匹配都应 fail-closed，并增加缺字段负例测试。
2. 让非作者 ARCH 复核明确收到 QA 报告路径及 SHA256（最好也验证报告内容/摘要），不能把通用候选审阅结果直接标成报告复核。
3. 纠正证据需绑定真实可读的物证文件及正确 SHA256，避免为未保存的内存对象生成虚构路径引用。
4. 独立会话运行凭据尚未在本报告绑定：当前登记的计划别名不是会话证据，任务卡 session_evidence 仍为空。正式签署链还需由 COORD 补齐真实 reviewer session UUID、运行审计/Token 凭据及本报告 SHA256；不得用计划别名替代。

完成修复后，原作者应产生新候选与新 run，由独立 Codex 会话按服务端锁定提交重新审查。本报告拒绝的是本次准确候选，不改变任务状态。
