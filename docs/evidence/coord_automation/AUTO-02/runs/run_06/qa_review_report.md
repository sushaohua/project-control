---
template_version: '2026-10-27'
review_id: AUTO-02-run_06-QA
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
reviewer_token_evidence: null
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
decision: REJECTED
reviewed_artifact_version: "project-control=a6e1cd246b8ab00d23a283928918c73034b35be8; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_06/result.md
  sha256: d8b523198d4b0fd394d0b48650d6f6e9987b04513232cf089fa526138af3a4c8
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_06/result.md
    sha256: d8b523198d4b0fd394d0b48650d6f6e9987b04513232cf089fa526138af3a4c8
  - path: project-control/tools/coord_runner/__init__.py
    sha256: c1806f909a8c9c891c17c9f9a2824851a7a70d289ab087502794bff5796de7fa
  - path: project-control/tools/coord_runner/models.py
    sha256: e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 5a8e8397a5057dd60bfba0291fe60c3d9baef0acb9b8cdc62b4774283fb0c3ae
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: 8f64a0a26377d1455c313677f0c4e78a0f1ca3a60b754fcfd3ee37f167e2fe24
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_06/server_qa.json
  sha256: a3d2aa9ab2742b9521c3a90886092012527448ad5daaf9df323f2cf1a116596a
  container_id: e95f05fd0232a205304b5b63491d0f68c8b0d2a72f548d474ee79bc7d5bf11de
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources:
    result: passed
    basis: 候选 SHA 与 server_lock.json、checkout.log 一致；本地 project-control 与 test_harness HEAD 也分别等于锁定 SHA。
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: failed
    basis: 报告声称 QA 报告复核门禁和有证据纠正门禁已强制实现，但代码允许缺少 report_review 和纠正证据。
  architecture_completeness:
    result: failed
    basis: QA报告复核强制条件未实现；server_qa.json 的 task_revision=6 与受审任务卡 revision=1 不一致。
---

# AUTO-02 独立 QA 审查报告（run_06）

## 决定

**REJECTED。** 本候选的服务器沙箱记录报告五个测试命令均 exit 0，且我确认候选版本及交付文件摘要与记录一致；但代码没有落实任务声称的 QA 报告复核必需门禁和“有证据纠正”要求。另外，沙箱证据的任务修订号与受审任务卡不一致，且当前交互未提供可核验的独立审查会话 UUID/token 凭证。上述问题阻止正式接受该候选。

## 审查范围与方法

- 依据：AUTO-02 revision 1、`codex_qa_review.md`、`delivery_and_coord_gate.md`、run_06 作者记录、锁定提交清单、checkout/runtime/server verdict 证据。
- 候选绑定：`project-control=a6e1cd246b8ab00d23a283928918c73034b35be8`、`test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181`。`server_lock.json` 和 `checkout.log` 记录相同 ref 与完整提交；当前两个仓库 HEAD 也分别与该锁定值相同。
- 对作者记录、`server_qa.json`、`runtime.log` 和 12 个交付文件逐项核对 SHA256，均与本报告 frontmatter 中给出的摘要一致。
- 只读审查了调度器、租约、状态机、检查点、审阅循环、配置及相关测试断言。未在宿主机运行候选测试；测试结果引用独立容器 runtime 记录。
- AST 扫描覆盖 `project-control/tools/coord_runner`、`project-control/tools` 和 `test_harness/runner` 下共 20 个 Python 文件，包含类方法和嵌套函数；按函数定义跨度（起止行，含装饰器前行不计）与参数（包括 `self`、可变参数）核查，发现 **0 个超过 50 行或 4 参数的函数**。

## 服务端沙箱与测试记录

`server_qa.json` 的 SHA256 为 `a3d2aa9ab2742b9521c3a90886092012527448ad5daaf9df323f2cf1a116596a`。其中记录 fresh checkout、无 developer mounts；容器 Inspect ID 为 `e95f05fd0232a205304b5b63491d0f68c8b0d2a72f548d474ee79bc7d5bf11de`，镜像 digest 为 `sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825`，挂载仅为沙箱 `/tmp/qa_sandboxes/AUTO-02_run_172423_20261029_092423` 到容器 `/workspace` 的读写 bind。runtime.log 与 JSON 中的容器 ID、digest 及运行输出一致。

| 沙箱命令 | 记录结果 |
| --- | --- |
| `python3 tools/test_coord_runner.py` | exit 0；48 tests，OK |
| `python3 tools/test_qa_runner.py` | exit 0；20 tests，OK |
| `python3 tools/test_delivery_checks.py` | exit 0；20 tests，OK |
| `python3 tools/test_check_task_graph.py` | exit 0；12 tests，OK |
| `./runner/qa_entrypoint.sh --suite all` | exit 0；`cascade_vectors`、`hil_unit` 两套均 PASSED |

按作者记录口径为 102 项检查（前四组 100 项 unittest 加最后 2 个 suite），这五条命令的 stdout/退出码在 `server_qa.json` 与 `runtime.log` 中可对照。该结果证明这些被记录的测试通过，不代表未覆盖的门禁正确，也不抵消下述代码缺陷。

## 发现

### 阻断项 1：QA 报告复核不是必需条件

`project-control/tools/coord_runner/state_machine.py:146-149` 只在 QA 条目的 `report_review` 字段**存在**时核验其结论；字段缺失时不会拒绝。`runner.py:148-168` 的审阅循环记录普通角色审阅结果后即可转入 `DONE`，并未要求针对 QA 报告的另一非作者复核。因而只要 QA reviewer 本身 APPROVED，缺少 `report_review` 的卡仍能通过 `validate_done_acceptance`。这与任务记录所称“QA 角色复核报告具备 APPROVED”以及规则要求的非作者复核不符。

### 阻断项 2：纠正不要求证据

`state_machine.py:66-83` 将 `evidence` 声明为可选；只有调用方主动传入时才检查 path/SHA256。QA 失败和 reviewer 拒绝路径在 `state_machine.py:94-105`、`114-130` 调用 `handle_remediation` 时都没有传证据。因此最多两次计数及第三次升级存在，但“有证据纠正”没有被实现为强制条件，不能接受作者关于该门禁已落实的声明。

### 阻断项 3：沙箱证据任务修订号不匹配

受审卡 `AUTO-02.md` 的 `revision` 为 1，作者记录也写 revision 1；但 `server_qa.json` 和 `server_verdict.json` 均标记 `task_revision: 6`。尽管锁定候选 SHA、日志哈希和容器证据相互一致，这个字段冲突使服务端 QA 记录无法按规范绑定到当前任务修订，须由 COORD/作者澄清并重新生成一致证据，不能由审查者推断为笔误。

### 阻断项 4：独立审查席位凭证缺失

任务卡登记的 QA session UUID 为 `3118e0b6-e82d-4f88-8b22-512cd6451293`，但 `session_evidence` 为空；当前审查交互未提供可验证的会话启动/执行审计记录或 token 凭证。计划别名及用户指定模型不能替代规则要求的真实独立会话绑定。报告按用户提供的 `gpt-6-luna` 标注模型元数据；此交互本身无法独立证明实际 runtime model/session 与上述登记 UUID 一致。

## 已通过的检查点与边界

- 服务器锁定提交和检出日志一致，且与当前本地 checkout 的 HEAD 相同；交付文件摘要和作者记录摘要吻合。
- 运行记录中的 48/20/20/12 个 Python 测试及两套 harness 检查均为 exit 0。
- AST 扫描未发现超 50 行或超 4 参数的函数。
- 静态审查确认代码包含最大 2 张实现卡并行配置、UART 等排他资源租约、7 阶段状态枚举/转移、临时文件加 `os.replace` 检查点写入，以及子进程 `SIGKILL` 后父进程恢复检查点的测试。
- 上述机制的存在或测试通过不等同于无缺陷：报告复核和纠正证据的实际强制性仍未满足。此审查不验证真实硬件、常驻部署、外部 Agent 服务或独立会话凭证。

## 复审要求

修复报告复核必须字段及其身份/候选绑定；使纠正计数入口拒绝缺少可核验 path 与 SHA256 的纠正；重新生成 task revision 与卡片一致的服务端锁定/QA证据；并补齐独立 Codex 会话的真实会话和 token 执行证据。以上修复应形成新候选或新 run，再由独立会话按准确服务器提交复审。本报告不推进任务状态。
