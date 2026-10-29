---
template_version: '2026-10-27'
review_id: AUTO-02-run_10-QA
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
reviewed_artifact_version: "project-control=b7935deef7bf4e1eb5cdadacf5fbc8e25b60bbeb; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_10/result.md
  sha256: 3c6b19666f75aeb012c4ad2ed03f35f8415dab9c62fcf994ce27241a1579545d
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_10/result.md
    sha256: 3c6b19666f75aeb012c4ad2ed03f35f8415dab9c62fcf994ce27241a1579545d
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: 6624e3bf13099f0c59085c72d99262ee9f88920ae87c7e8e26fa846126fc9bc5
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 23d01b6473e6a1672f39b1ce623c5d6cc37574fd2f82850a094e3039c55e202a
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
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_10/server_qa.json
  sha256: 9b4128a57cbf2dbb90bbd0553fca9ab3b351e57871c297a6f788963db06f0086
  container_id: 37c3d915d12553b1c87131840c4ab5fa9c9e03ca687a4a0702ddcd22734e939e
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources:
    result: partial
    basis: 独立 git clone/fetch 与 git ls-remote 确认两个候选服务器 Commit；但本次宿主 Docker daemon 找不到 server_qa.json 所列容器，沙箱运行和 inspect 物证无法独立验证。
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: fail
    basis: 执行记录将该候选表述为真实服务端沙箱通过；仅有可读 JSON/log 不能证明容器、执行环境或测试进程真实运行。
  architecture_completeness:
    result: fail
    basis: QA entry 缺失 report_sha256 时，runner 会从本地报告物理重算并静默补写；此外 runner 将已 APPROVED 的非 QA 代码审查自动伪装成 QA 报告审阅。
---

# AUTO-02 run_10 独立 QA 审查报告

## 审查结论

**REJECTED。** 候选服务器 Commit 与代码文件哈希已核实，目标 run_09 的 state machine 专项 fail-closed 条件及负例测试也存在；但实际执行路径仍绕过“QA entry 必须自行提供 report_sha256”的要求，并把普通 ARCH 代码审查记录直接转写为 QA 报告审阅批准。服务端沙箱证据也无法在本次审查中独立确认。因此本候选不满足 APPROVED 门槛。

## 审查来源与版本核对

- 从记录中的 GitLab URL 分别新 clone/fetch 两个项目并 detached checkout：`project-control=b7935deef7bf4e1eb5cdadacf5fbc8e25b60bbeb`、`test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181`。两仓检出 HEAD 与锁定 SHA 完全相同。
- 宿主机独立执行 `git -C project-control ls-remote origin main`，结果为 `b7935deef7bf4e1eb5cdadacf5fbc8e25b60bbeb refs/heads/main`，退出码 0。
- `result.md` 和 `server_qa.json` 实际 SHA256 分别为 `3c6b19666f75aeb012c4ad2ed03f35f8415dab9c62fcf994ce27241a1579545d` 与 `9b4128a57cbf2dbb90bbd0553fca9ab3b351e57871c297a6f788963db06f0086`，均与提交审查时提供值相同。上述 11 个源码/配置工件在独立 clone 上重算 SHA256，全部与 frontmatter 列值一致。
- 候选的源码读取只来自以上独立 clone；作者工作树中的未提交改动未作为代码基线。run_10 的执行记录和 JSON 属于候选后的证据文件，按给定路径核对哈希与内容。

## run_09 阻断项专项核验

1. **state machine 的 entry 哈希校验：代码条件已修正。** `state_machine.py::_validate_qa_report_review` 先物理读取报告并重算 `real_sha`，随后严格执行 `if not entry_sha or entry_sha != real_sha` 并抛出指定 `GateValidationError`。`test_done_rejected_when_qa_entry_missing_report_sha` 负例也确实存在，断言错误信息包含 entry hash 缺失或不匹配。
2. **端到端调用链仍未闭环。** `runner.py::_resolve_qa_report_ref` 对 `qa_entry.report_sha256` 仅在“有值且错误”时拒绝；缺失/空值时会继续将从文件计算出的 `real_sha` 写回 `qa_entry["report_sha256"]`。随后完成门禁只看到已补写字段。因此上述 state machine 负例绕过 runner，不能证明真实调度路径 fail-closed。QA entry 缺失摘要应在输入边界直接拒绝，而不是由消费方补成有效值。
3. **独立 QA 报告复核是假批准。** `runner.py::_ensure_qa_report_review` 先选择任意已批准的非 QA reviewer（AUTO-02 要求中的 ARCH），然后直接构造 `report_review`，将 `decision` 固定填成 `APPROVED`，并把 ARCH session 复制进去。该 reviewer 的调用只接收 task id、candidate commit 和 role，没有 QA 报告路径或内容；因此它审核的是代码候选，不是 QA 报告。测试 `test_execute_review_phase_multi_role`（约第 776–795 行）还把这个自动生成标记断言为成功，未覆盖实际独立报告复核。此处违反 QA 报告必须由另一未参与写作的会话复核的规则。

## 服务端沙箱证据核验

- 独立 `ls-remote` 成功确认 `project-control/main` SHA 为指定候选。两仓也可从远端 fetch 到锁定提交。
- `server_qa.json`、`server_lock.json`、`checkout.log`、`runtime.log`、`server_verdict.json` 的本地 SHA256 均与 JSON 中引用值一致；日志和 JSON 记录 61 + 20 + 20 + 12 个 Python 测试及 `qa_entrypoint.sh` 两个 suite 均 exit 0，并记录镜像 digest、容器 ID、容器状态和挂载。
- 但本次宿主机执行 `docker inspect 37c3d915d12553b1c87131840c4ab5fa9c9e03ca687a4a0702ddcd22734e939e` 返回 `Error: No such object`。因此不能独立读取运行时容器 inspect，也不能确认报告里的 bind mount、容器状态、镜像 digest 与测试进程之间的真实绑定。文件内部 SHA 一致只能证明这些证据文件未在本次读取期间变化，不能证明其陈述真实。测试结果在本报告中仅记为“证据文件所载结果”，不记作本审查会话重新运行或独立复现。
- 当前 task card 的 QA reviewer 记录虽有 session UUID，但 `session_evidence` 为空；本次材料没有可核验的 Codex session 运行事件/Token 审计绑定。`planned_session_alias` 也不能替代会话证据。无法据此签署会话与容器证据双重独立性。

## AST 规模门禁

对独立 clone 中 `project-control/tools/**/*.py` 的 18 个 Python 文件运行只读 AST 统计：共 293 个函数定义，按函数源码行数及位置参数、关键字参数、可变参数计数，超 50 行或超 4 参的违规数为 **0**。此结果仅说明该目录当前静态规模符合声称门禁，不证明运行时正确性。未对宿主作者工作树运行构建或测试。

## 运行记录审阅与未执行项

- 审阅了 `result.md`、`server_qa.json`、`server_lock.json`、`checkout.log`、`runtime.log`、`server_verdict.json` 与 AUTO-02 revision 1 任务卡及 canonical QA/交付门禁规则。
- 本次宿主审查没有重新运行服务端测试套件；按照独立审查规则，测试必须由沙箱执行。本机 Docker daemon 上目标容器不存在，无法重新读取其 inspect 物证或重放其运行时。
- 已执行：独立 Git clone/fetch/checkout、`git ls-remote`、工件 SHA256 重算、AST 扫描、对指定容器 ID 的 `docker inspect` 查询。`docker inspect` 退出码 1。
- 审查会话的外部 Codex Session UUID、原始运行事件与 token 记录未随任务材料提供；不得用计划别名或任务卡预登记 UUID 代替实证。

## 必要修复与复审条件

1. 在 runner 入口拒绝缺失/空 `qa_entry.report_sha256`，并增加通过 `_execute_review_phase`/完整 runner 路径的负例，证明缺失值不会被消费端补写后放行。
2. 将 QA 报告路径、SHA256、报告内容及审查指令交给一个与作者及 QA 作者不同的真实独立审查会话；只有该会话返回 APPROVED 且身份/运行记录已核验后，才写入 `report_review`。不得复用对代码候选的 ARCH 接受结果。
3. 重新提供可核验服务端 job 与 Docker inspect 原始证据，且容器、镜像 digest、只读候选检出、测试日志和 verdict 对同一锁定候选形成绑定；同时补齐真实 reviewer session 运行证据。产生修复候选后由新的独立 QA 会话重审。

本报告为对上述锁定候选的拒绝决定。不得把 `server_qa.json` 中的 `passed: true` 或当前状态记录提升为 QA 接受。
