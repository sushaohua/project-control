---
template_version: '2026-10-27'
task_id: AUTO-02
task_revision: 1
reviewer_role: QA
reviewer_platform: codex
reviewer_model: gpt-6-luna
decision: REJECTED
reviewed_artifact_version: 657b7da25d01febcb8c272e68ada8a2b3bdda4250caa19e1edf9f92799649370
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_01/result.md
  sha256: 657b7da25d01febcb8c272e68ada8a2b3bdda4250caa19e1edf9f92799649370
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_01/result.md
    sha256: 657b7da25d01febcb8c272e68ada8a2b3bdda4250caa19e1edf9f92799649370
  - path: project-control/tools/coord_runner/__init__.py
    sha256: 66693b1f4cbb0cf7d9041b584ebd4791e84def091ae9e68ac03646f4f92d73b6
  - path: project-control/tools/coord_runner/models.py
    sha256: e2db6126d84ef12a007f83a89ddd472e5569e0ca7ba28b0f20a09d5f4a18ce78
  - path: project-control/tools/coord_runner/errors.py
    sha256: 1407cc0ddd7dc5a954dc024f2be1e2689274a0735bef37d8e8effd22ccef07e3
  - path: project-control/tools/coord_runner/lease_manager.py
    sha256: e65e24a97af415303c7193e6c0c1d0264aac7aa9e90c43f4e0a657676680a96d
  - path: project-control/tools/coord_runner/state_machine.py
    sha256: 3c591694b703b42fd230cc779f73c82c19c6f25e51f2bbed25304a6f09c8ac45
  - path: project-control/tools/coord_runner/checkpoint.py
    sha256: 5e38f357b573570a27cd718e296b694c8cb6671bacd5a67a834ff796b5f56ed6
  - path: project-control/tools/coord_runner/scheduler.py
    sha256: c015900d4ee81e421da333aec2b0e49d0066158c9dffa3f1c23037083095e884
  - path: project-control/tools/coord_runner/runner.py
    sha256: b8569038fbf6b7bfe5078e67bdb812274e45cfe5d06147128586a1072d2f9f24
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_01/server_qa/server_qa.json
  sha256: 8e20db5d947dd29aef34106f2520c94048d14fbc0a423c395cd6191df310d0de
content_audit:
  fact_sources:
    result: passed
    basis: '服务端沙箱工作树 HEAD 与锁定的 project-control、test_harness commits 一致；checkout.log 记录了从配置的远端 fetch 与 checkout。当前审查会话再次 ls-remote 时因 socket Operation not permitted 失败，未能独立确认 refs/heads/main 的当前指向。'
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: failed
    basis: 执行记录及既有 QA 草稿将默认模拟回调描述为真实 Agent/QA/Review 执行，并将状态序列化往返称为崩溃恢复演练；代码与独立行为核验不支持这些表述。
  architecture_completeness:
    result: failed
    basis: 缺省路径可合成通过并推进 Done，SandboxQA checkpoint 无法恢复推进，QA verdict 缺少类型与候选/作业绑定校验，且设备锁冲突会泄漏实现租约。
---

# AUTO-02 独立 QA 审查报告

## 1. 决定

**决定：REJECTED。** 四组 Python 单元测试及 `qa_entrypoint.sh --suite all` 均通过；但通过的测试未覆盖以下关键安全与恢复路径，且部分测试直接依赖默认模拟行为。它们不能支持本票所要求的真实 Agent 调度、可信服务端 QA 门禁及崩溃恢复结论。

本报告审查任务卡 `AUTO-02` revision 1、INTEGRATOR 执行记录、锁定候选源码和所列服务端沙箱证据。候选执行记录 SHA256 与交付值一致。提交锁定为 `project-control=dfea09b83702da96f9c269c64ba7ad9547e0710f`、`test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181`。

## 2. 服务器候选与沙箱证据核对

`server_qa.json` 的 SHA256 为 `8e20db5d947dd29aef34106f2520c94048d14fbc0a423c395cd6191df310d0de`，与提交值相符。所指沙箱 `/tmp/qa_sandboxes/AUTO-02_run_160235_20261029_080235` 中，两个仓库 HEAD 分别为上述锁定 commit。沙箱各受审源码、配置和队列文件的 SHA256 均与本报告 frontmatter 所列值相符。`checkout.log` 记录了从配置的远端 fetch 锁定 commit 并 checkout；对应 checkout、runtime、server verdict sidecar 的摘要也与 `server_qa.json` 中记录一致。

我在该沙箱目录中实际重新执行五组命令，结果如下：

| 沙箱仓库 / 命令 | 结果 |
| --- | --- |
| `project-control`: `python3 tools/test_coord_runner.py` | exit 0，26 tests，OK |
| `project-control`: `python3 tools/test_qa_runner.py` | exit 0，20 tests，OK |
| `project-control`: `python3 tools/test_delivery_checks.py` | exit 0，20 tests，OK |
| `project-control`: `python3 tools/test_check_task_graph.py` | exit 0，12 tests，OK |
| `test_harness`: `./runner/qa_entrypoint.sh --suite all` | exit 0，`cascade_vectors` 与 `hil_unit` 均显示 PASSED |

本任务没有构建命令，构建验证不适用。测试通过事实不消除下文的行为缺陷。

隔离证据边界：记录给出了 `kind: remote-runner`、沙箱 ID、路径和空 `developer_mounts`，checkout 日志也与实际 HEAD 对得上；但记录没有提供 runner/job 的可验证服务端身份、隔离镜像或快照摘要、账号、网络策略和资源限制。该 JSON 与摘要只能证明其内容与本地文件相符，不能独立证明可信 QA 服务的身份或运行隔离。另，用户给出的 project-control ref 为 `refs/heads/main`，`server_lock.json` 中写的是 `refs/heads/dfea09b83702da96f9c269c64ba7ad9547e0710f`；当前审查环境执行 `git ls-remote` 时因 `socket: Operation not permitted` 无法重查远端分支当前指向。故报告仅确认沙箱检出的 commit 与锁定 SHA 相符，不宣称独立复核了 main 当前 ref。

按 canonical QA 规则，正式 QA 会话本身也应在隔离环境中运行。本次工具会话的工作目录是项目工作区；任务卡登记的 reviewer session ID 与本次运行事件之间没有可核验的启动/隔离绑定材料。因此本报告不声称本次 Codex 会话本身已在所述远端沙箱内运行；实际五组复跑均是在该沙箱工作树中执行的。

## 3. 源码与验收点审查

### 3.1 已实现并由测试支持的部分

- `CoordScheduler` 按 bootstrap 与 order 生成候选，检查依赖、已完成卡和资源可用性。
- `LeaseManager` 对单个实例中的 implementation lease 限制最大并发数为 2；UART 排他冲突在常规单锁路径可阻止第二个租约。配置文件相应设置为 2。
- 状态机允许七个主要阶段 `Backlog → Ready → InProgress → CandidatePushed → SandboxQA → Review → Done`，并拒绝非法迁移。
- `max_evidence_based_corrections=2` 时，计数达到 2 后再次处理退修会切到 `Escalated` 并抛出 `RemediationLimitExceededError`。
- checkpoint 使用临时文件和 `os.replace` 完成原子替换式写入。

这些属于局部实现能力，不足以证明端到端调度和恢复验收已完成。

### 3.2 阻断通过的问题

1. **默认路径伪造候选、QA 和审查结果（P0）**：`runner.py` 的 `_execute_agent_phase` 在没有 `agent_executor` 时取卡片 SHA 或硬编码 SHA；`_execute_qa_phase` 在没有 `qa_executor` 时返回 `passed: True`；`_execute_review_phase` 在没有 `review_executor` 时合成一个 reviewer session 和 `APPROVED`。因此 runner 未连接真实 Agent、AUTO-01 服务端 QA 或独立审查，也能推进完成。独立行为复核中，未配置任何 executor 的 `run_tasks(1)` 返回完成数 1 并将 `T1` 放入 `completed_tasks`。现有 `test_run_tasks_finite_mode` 正是在无 executor 的情况下断言完成。这违反“虚假 Done、同作者自批、服务端 QA 失败不得错误放行”的验收条件。

2. **QA verdict 可被错误类型绕过，且未绑定具体服务器证据（P0）**：`validate_qa_verdict` 使用 `bool(qa_verdict.get("passed", False))`。Python 中非空字符串 `"false"` 会转换为真；独立调用实际返回 `True`。此外，verdict 未强制包含 exit code、服务端 job 身份、任务 revision、沙箱 ID、候选 commit 或原始证据摘要。仅给出 `passed` 或任意非空字符串即可满足 QA 阶段，无法证明批准的是该候选的服务端结果。

3. **重启后 `SandboxQA` 状态无法继续（P1）**：`process_task` 只处理 `InProgress`、`CandidatePushed`、`Review` 和 `Done`，没有处理恢复出来的 `SandboxQA`。在 `SandboxQA` 状态调用 `process_task` 后状态仍为 `SandboxQA`，QA executor 不会再次运行，任务会在后续循环持续滞留。现有 `test_crash_and_restart_recovery_drill` 只保存一个内存态 `InProgress` 记录并由新对象读回字段；没有杀死/重启进程，也没有验证 `SandboxQA`、Review、失败退修、lease 过期或任务续跑。因此不能称为已验证崩溃恢复演练。

4. **排他资源获取失败会泄漏 implementation lease（P1）**：`_acquire_task_leases` 先取得 implementation lease，再逐项获取设备租约；若 UART 已被占用，后续获取抛出 `ResourceConflictError`，已取得的 implementation lease 没有回滚。独立复核建立 UART 冲突后调用 `dispatch_task`，冲突返回时仍残留 1 个 active implementation lease，可能错误耗尽两张实现卡并发额度。

5. **“有证据纠正”只检查自由文本原因（P1）**：`handle_remediation` 接收 reason 字符串并增加计数，没有证据对象、证据路径/摘要、候选版本或 verdict 绑定校验。当前逻辑能限制次数，但无法证明每次纠正基于证据，和任务卡及执行记录所称“最多 2 次有证据纠正”不等价。

6. **声称支持的命令行入口不存在（P1）**：`runner.py` 定义类方法 `run_once`、`run_tasks` 和 `run_daemon`，但文件没有 `main`、`__main__` 入口或 argparse 参数注册。因此报告所述 `--once`、`--max-tasks N` CLI 模式不能由候选代码直接调用；当前是库方法，不是已交付 CLI。

7. **Done/审查绑定不足**：`validate_done_acceptance` 只要求 review assignments 非空且每项 decision 等于 `APPROVED`；它不核对 reviewer 会话与准确候选 SHA、任务 revision、报告摘要的绑定。`validate_review_verdict` 的自审检查只比较会话字符串。默认审查 executor 又可伪造 reviewer ID，所以此处不能支撑执行记录中对真实独立审查/虚假 Done 的完整拦截声明。

### 3.3 函数规模 AST 扫描

我对沙箱锁定源码中的 9 个 Python 文件（`coord_runner/*.py`、`coord_queue.py`、`test_coord_runner.py`）重新解析 AST，共扫描 58 个函数/方法定义。按 AST 源码跨度计（包含空行和注释，属于偏保守计数），最大为 31 行，位于 `runner.py:step`；显式参数数排除方法接收者 `self`/`cls` 后最大为 3 个，位于 `coord_queue.py:next_action`。本次扫描结果为 **0 个超过 50 行或超过 4 个参数的函数**。

作者测试中的 AST 检查也通过；但其实现将 `self` 计入参数、未计入 varargs/kwargs，且只检查常规 args 与 kwonlyargs。本报告独立扫描把 varargs/kwargs 纳入参数计算，并排除了常规方法接收者。两种口径下均未发现门禁违规。

## 4. 修复后重审要求

请原作者在新候选中至少完成以下事项后重新提交审查：

- 未配置真实 executor/服务时 fail closed，禁止合成 commit、QA 通过或审查批准；实现并绑定真实 Agent 启动/等待与 AUTO-01 服务器判定。
- 对 QA 结果实施严格 schema/type 校验，并校验 job、沙箱、任务 revision 和候选 commit 一致性；异常类型或字段缺失必须拒绝。
- 补齐全部可恢复状态的恢复逻辑，演练实际进程退出与重启，验证任务续跑、退修计数及租约恢复。
- 让多资源租约获取具备失败回滚/原子语义；为退修证据保存并验证可追溯的证据引用。
- 交付真实可调用的 CLI（若仍在本票范围）并移除或准确限定作者执行记录中的不实能力表述。
- 提供可核验的 server runner/job 与沙箱隔离属性记录；正式独立 QA 会话应绑定实际启动/运行事件与隔离环境。

修复后必须产生新的准确候选和 QA run；本报告拒绝的是当前锁定候选，不替代 COORD 对状态的处理。
