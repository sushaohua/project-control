---
template_version: '2026-10-27'
review_id: AUTO-02-run_08-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: unverified
model_override_ref: null
planned_session_alias: planned-qa-auto-02
reviewer_session: null
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
decision: REJECTED
reviewed_artifact_version: "project-control=45b7b6c323520cd4773b22901a0dce05fc693708; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_08/result.md
  sha256: bf9274047149adb491a16602fc25219250f6e1994803e3859e3aa5eed03ee74d
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_08/result.md
    sha256: bf9274047149adb491a16602fc25219250f6e1994803e3859e3aa5eed03ee74d
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: 6624e3bf13099f0c59085c72d99262ee9f88920ae87c7e8e26fa846126fc9bc5
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 3506ad6d09e5a5463250d26b2dcd4ab7713d8d042f419edd58747a80c95d6005
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: 3f24725eeac632e8424c85a86c6089ff210032b9abaf298b9d3e10a7f1e912c4
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_08/server_qa.json
  sha256: fb4d4c82d21598526980dae16e00296d792d68b3cb6358dc5c05e11d156c580a
  container_id: 08c1ac7a7465ad2d6fcd859ffc433626df71969320dae9d98df9633c8fa58889
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources:
    result: passed
    basis: 本地 Git 对象确认两个锁定 Commit 存在且分别为 main；server_lock、checkout.log 与候选 SHA 一致，服务端运行证据哈希匹配。
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: passed
    basis: 审查结论限定于所核对的调度门禁、退修物证、服务端测试记录及函数规模扫描。
  architecture_completeness:
    result: failed
    basis: QA 报告物理路径及其真实 SHA256 未被强制核实，见正文阻断项 QA-01。
---

# AUTO-02 run_08 独立 QA 审查报告

## 审查范围与方法

审查对象为任务卡 `AUTO-02` revision 1、执行记录 `run_08/result.md`、指定的 `project-control` 与 `test_harness` 候选 Commit，以及 `server_qa.json`、`server_lock.json`、`checkout.log`、`runtime.log` 和 `server_verdict.json`。核对了候选 Commit、受审源码 SHA256、服务端证据中的锁定版本/容器信息/测试结果，并针对 run_07 的三个阻断项逐项检查实现和指定负例测试。没有在宿主机运行受审代码或重跑测试；测试结论仅依据服务端沙箱归档日志。

本运行环境未提供可独立核验的审查会话 UUID、模型运行记录或 token 审计。任务卡虽登记 QA session UUID，但 `session_evidence` 为空，不能证明该 UUID 对应本次会话；因此 frontmatter 将 `reviewer_session` 留空，并将 `actual_model` 记为 `unverified`。这不影响以下代码核查，但不构成“独立会话凭证已核实”的声明。

## 版本与服务端证据核对

- 本地 Git 对象确认 `project-control` HEAD 为 `45b7b6c323520cd4773b22901a0dce05fc693708`，`test_harness` HEAD 为 `210ddd1c3f6f59594836c91b68aae55fb7a35181`；二者均显示 `HEAD -> main, origin/main`。`server_lock.json` 和 `checkout.log` 记录了相同 Commit 的 fetch/checkout。
- `result.md` SHA256 为 `bf9274047149adb491a16602fc25219250f6e1994803e3859e3aa5eed03ee74d`；`server_qa.json` SHA256 为 `fb4d4c82d21598526980dae16e00296d792d68b3cb6358dc5c05e11d156c580a`，均与输入值一致。
- `server_qa.json` 内的容器完整 ID、镜像 digest、running 状态及挂载信息与 `runtime.log` 的 Inspect 记录相符；无 developer mounts。锁定文件、checkout、runtime 和 verdict 的归档 SHA256 与 `server_qa.json` 引用一致。
- 服务端记录五组命令全部 exit 0：`test_coord_runner.py` 56 项、`test_qa_runner.py` 20 项、`test_delivery_checks.py` 20 项、`test_check_task_graph.py` 12 项，以及 `qa_entrypoint.sh --suite all` 中 cascade_vectors 与 hil_unit 两套。前四组共 108 个单元测试，入口脚本另有 2 套件检查，记录总数 110；这里只确认日志声明，不将其表述为本会话重新执行。

## run_07 阻断项专项审查

### 1. task_revision 缺失与不匹配拒绝

`state_machine.py:_validate_server_qa_proof` 对 `qa_rev is None` 或 `qa_rev != record.task_revision` 均抛出 `GateValidationError`，缺失和不匹配都 fail-closed。`test_coord_runner.py` 中 `test_qa_verdict_missing_task_revision_rejected` 与 `test_qa_verdict_task_revision_mismatch_rejected` 分别覆盖这两个负例。该项实现与测试覆盖符合要求。

### 2. QA 报告物理路径和 SHA256 强绑定 — 未通过

`runner.py:_resolve_qa_report_ref` 仅在 `report_sha256` 缺失时尝试读取 `workspace_root / report_path`。如果目标文件不存在，它会改用 `json.dumps(qa_entry)` 的 SHA256；如果条目预先带有 `report_sha256`，则完全不读取文件并直接接受该值。默认路径由 `task_revision` 拼成 `run_01`，不能定位本次 `run_08` 报告。

`_ensure_qa_report_review` 随后把该路径和 SHA 放入 `report_review`，但 `state_machine.py:_validate_qa_report_review` 只要求两个字段为非空字符串，并在 QA 条目也提供 SHA 时比较字符串相等；它不验证路径指向存在的文件，也不重新计算文件哈希。因此，任意路径与自报 SHA 可以满足这项门禁，未形成对 QA 报告物理字节的绑定。若已有 `report_review`，`_ensure_qa_report_review` 也直接跳过解析，由上述字段校验承担全部检查。

指定的 `test_done_rejected_when_qa_report_review_missing_report_path_or_sha` 和 `test_done_rejected_when_qa_report_review_sha_mismatch` 覆盖字段缺失和字段间不一致，但不覆盖报告文件不存在、磁盘内容哈希不符、预填 SHA 未重算或错误默认路径。因此，虽然字段负例通过，run_07 阻断项 2 并未实质闭环。这是拒绝本候选的阻断问题。

### 3. 退修物证优先读取真实磁盘文件

`state_machine.py:_find_or_create_evidence` 按候选顺序读取存在的物理文件并基于实际字节计算 SHA256；找不到时会将原始内容写入 `/tmp/<fallback_name>` 后返回对应真实路径及内容哈希。这满足“先查物理文件，后写入真实文件”的基本顺序。边界上，`_extract_qa_failure_evidence` 和 `_extract_review_failure_evidence` 会优先返回 verdict 内已有的 `evidence` 字典，不验证其中路径所指文件是否存在或哈希是否对应；因此传入已有 evidence 时不保证是本函数读出的物理文件。该边界应由后续修正考虑，但本次主要阻断仍为 QA 报告 SHA 未绑定物理内容。

## AST 函数规模扫描

对候选 `project-control/tools` 下 18 个 Python 文件进行只读 AST 扫描，共检查 287 个函数定义（方法参数计数排除 `self`/`cls`；函数长度按 AST 起止行计）。发现超过 50 行或超过 4 个显式参数的函数：0。作者记录声称扫描 20 个 Python 工具文件；当前指定源码树在 `project-control/tools` 中实际找到 18 个 `.py` 文件，因此文件数口径有差异，但扫描到的 18 个文件未触发门禁违规。

## 决定

**REJECTED。** 服务器沙箱测试记录、候选版本绑定、task_revision 严格拒绝和 AST 扫描结果均有支持；但 QA 报告审查哈希没有被强制绑定到实际存在的报告文件字节，恰好是 run_07 阻断项 2 的核心要求。故不能批准当前候选。作者应要求报告路径真实存在、每次从磁盘读取并重新计算 SHA256，拒绝缺失文件及预填哈希与文件内容不符的情况，并补充对应负例后产生新候选及新审查 run。另须补齐可核验的独立 QA 会话/模型运行证据，才能把正式审查席位信息登记为已验证。
