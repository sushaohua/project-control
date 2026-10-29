---
template_version: '2026-10-27'
review_id: AUTO-02-run_09-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-auto-02
reviewer_session: null
reviewer_session_evidence: null
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
decision: REJECTED
reviewed_artifact_version: "project-control=38939d638992b22fa73ec9ff1272e8b01d0551e4; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_09/result.md
  sha256: fa4e808962cd2ec002358f58a848b1cf3831acc945428a8ce7dc7fc3f5a1d084
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_09/result.md
    sha256: fa4e808962cd2ec002358f58a848b1cf3831acc945428a8ce7dc7fc3f5a1d084
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: 6624e3bf13099f0c59085c72d99262ee9f88920ae87c7e8e26fa846126fc9bc5
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 8830882234ad95cf38c969212a526355dacc87a1bfe8b3faddbbae62d05090d6
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: 3b3d15f7b70a2aea5f1d04823af42d87802c3f19920f6f9c549a80a47b64bda5
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_09/server_qa.json
  sha256: 94d10f6c8a0fa643fffc90000c7d3dc3e53e09dfac570ed94dce6f4cf0d2c8d2
  container_id: 57fc83eb0a078d7f38eca7de4cd78390afd0dd50e1d20ec2cc2f87be52e13557
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources:
    result: failed
    basis: 本地 Git 对象中的候选提交和指定源码摘要与锁定值一致；但对记录的 GitLab SSH 服务器执行只读 ls-remote 时因当前环境 socket 网络权限被拒绝，未能独立确认服务器 ref/commit。
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: passed
    basis: 结论区分源码审阅、server_qa.json 所记载的沙箱结果与未能独立复核的远端服务器事实，不将日志记录表述为本次实测。
  architecture_completeness:
    result: failed
    basis: state_machine.py 仅在 QA entry 的 report_sha256 为真值时校验与磁盘字节重算值相等；缺失或空值会通过，未满足任务要求的强制绑定。
---

# AUTO-02 独立 QA 审查报告（run_09）

## 审查范围与方法

按 project-control/.agents/rules/codex_qa_review.md 与 project-control/.agents/rules/delivery_and_coord_gate.md 检查任务卡、作者执行记录、锁定候选代码、server_qa.json 及其引用的运行记录。审查以两个指定完整提交的本地 Git 对象内容为代码快照；对 project-control 十二项指定文件逐一读取提交对象并重算 SHA256，均与本报告绑定值一致。作者工作树有未提交修改，因此未将工作树内容作为源码基线。

尝试对记录中的 GitLab SSH 地址执行只读 git ls-remote，但该环境返回 socket: Operation not permitted，未能现场查询远端 ref。当前执行上下文也没有提供本次 Reviewer 的 Session UUID、会话启动/运行审计记录或 token 使用凭证；任务卡里已登记的会话 UUID 对应的 session_evidence 仍为空。因此本报告不把 server_qa.json 的自述等同于本次观察到的服务器或容器事实。

未在宿主机运行受测测试套件，也未把作者工作树用于执行验证。审阅包含锁定提交源代码检查、指定负例名称和断言检查、Python AST 静态扫描，以及对服务端证据文件内部摘要的核对。

## run_08 专项整改核验

runner.py:_resolve_qa_report_ref 已移除基于 QA entry JSON 序列化内容生成报告哈希的路径。函数要求 full_p.is_file()，从磁盘读取字节计算 SHA256；若预填 report_sha256 为真值且与重算摘要不符，则抛出 CoordRunnerError。该部分符合本次专项要求。

state_machine.py:_validate_qa_report_review 会校验被复核报告的物理文件存在，读取文件字节重算摘要，并严格要求 report_review.report_sha256 与重算值相同。问题在 QA entry 自身的摘要比较：代码使用 if entry_sha and entry_sha != real_sha。当 entry.report_sha256 缺失或为空字符串时，检查被跳过，Done 门禁仍可能接受。这与本次明确要求的 report_review.get("report_sha256") 和 entry.get("report_sha256") 对磁盘重算值进行强制一致性核验不符。建议要求 entry 摘要存在且为有效字符串，并无条件与 real_sha 相等。

以下四项专项测试在候选测试代码中均存在：

- test_done_rejected_when_qa_report_file_not_found_on_disk
- test_done_rejected_when_qa_report_file_tampered_or_sha_mismatch
- test_runner_resolve_qa_report_missing_file_rejected
- test_runner_resolve_qa_report_prefill_mismatch_rejected

现有状态机专项负例覆盖物理文件缺失和已提供但错误的摘要；没有覆盖 entry.report_sha256 缺失或空值时必须拒绝，故未发现上述门禁缺口。

## 沙箱测试证据核对

server_qa.json 的实际 SHA256 为 94d10f6c8a0fa643fffc90000c7d3dc3e53e09dfac570ed94dce6f4cf0d2c8d2，与提供值一致。其内嵌的容器 ID、镜像 digest 与 runtime.log 所录 Inspect 文本一致；server_lock.json 的两个仓库 URL/ref/commit 与本次审查目标一致。四个被引用文件的摘要（lock、checkout、runtime、verdict）均与磁盘文件重算值一致。

服务端记录声称以下五个命令均 exit 0：

| 记录的套件 | 记录结果 |
| --- | --- |
| tools/test_coord_runner.py | 60 tests，OK |
| tools/test_qa_runner.py | 20 tests，OK |
| tools/test_delivery_checks.py | 20 tests，OK |
| tools/test_check_task_graph.py | 12 tests，OK |
| runner/qa_entrypoint.sh --suite all | cascade_vectors、hil_unit 两套件 PASSED |

合计为 112 个 unittest 项和 2 个入口套件，即记录的 114 项检查通过。该计数及 exit code 是对已哈希证据内容的核读；因远端和实际容器无法在本次环境查询，不将其表述为本次独立执行或现场观测。

## AST 扫描

对 project-control=38939d638992b22fa73ec9ff1272e8b01d0551e4 中 tools/coord_runner/ 与 tools/coord_queue.py 的 Python 源文件进行 AST 扫描：10 个文件、79 个函数；按函数定义起止行统计函数体跨度，并按参数列表计数（方法的 self/cls 不计），超过 50 行或超过 4 个参数的函数为 0。该结果只覆盖上述 Python 自研实现文件，不构成对仓库内其他语言或第三方代码的判定。

## 阻断项与决定

**决定：REJECTED。** 当前候选不能按任务卡专项要求接受，原因如下：

1. **功能门禁缺口：** state_machine.py 对 entry.report_sha256 的比较仅在该值为真值时发生；缺失/空摘要未被拒绝。补充拒绝缺失/空摘要的逻辑和专项测试后，需针对新候选复审。
2. **服务器来源未独立确认：** 当前审查环境对远端 SSH 查询报 Operation not permitted。在服务器/ref 与代码快照不能独立核对时，按服务器基线门禁不得签署通过。需提供可从服务器重新 fetch/查询的只读审查环境及完整 commit 对账记录。
3. **Reviewer 会话证据缺失：** 本次可用材料未包含本审查会话的真实 Session UUID 与运行审计记录，任务卡相应 session_evidence 为空。正式收件前需补齐可核验的独立会话来源证据，并由非作者复核本 QA 报告及其最终 SHA256。

报告拒绝不否认 server_qa.json 所记录的测试结果；它表示源码存在明确验收差距，且服务器/会话独立性证据尚未达到规则要求。
