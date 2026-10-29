---
template_version: '2026-10-27'
review_id: AUTO-02-run_11-QA
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6
model_override_ref: null
planned_session_alias: planned-qa-auto-02
author_session: 0e0e4b90-2aeb-42d4-abc2-13ed9198e8f0
task_id: AUTO-02
task_revision: 1
decision: REJECTED
reviewed_artifact_version: "project-control=06d1b2d54fdca8a19b345109a3b967910ddb9861; test_harness=210ddd1c3f6f59594836c91b68aae55fb7a35181"
candidate:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_11/result.md
  sha256: 4fa65674298672650a56fab6bc1911d3ee09a9cbb1e68b6abc99f4348629aacb
reviewed_artifacts:
  - path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_11/result.md
    sha256: 4fa65674298672650a56fab6bc1911d3ee09a9cbb1e68b6abc99f4348629aacb
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
    sha256: 07b6f9b051346212829cc4921c6ee490c4fd49eaff8a02754c8e8362518ae33c
  - path: project-control/tools/coord_runner/codex_adapter.py
    sha256: 5e571fbd94cc38486d3b7ba892adf425d7ed0f750384e0e793827e63f948d9a0
  - path: project-control/config/coord_runner/coord_config.yaml
    sha256: 75d43276a3da0fab4640b1f516045bea0d77142638be0d2f47a85a50c86a54f2
  - path: project-control/tools/coord_queue.py
    sha256: cb803af84686e7b98e9e3818b7050cfb99427e1d3b0482e3213f8d98919fe995
server_qa:
  path: project-control/docs/evidence/coord_automation/AUTO-02/runs/run_11/server_qa.json
  sha256: 654cae89eb9bc17449be437e81505669992edfc0f33ceea5c5975557683b6490
  container_id: abcaee7952e4d8aac8d1a878cb41552aa3654de14213f0749753fdf3a8802ed6
  image_digest: sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825
content_audit:
  fact_sources:
    result: passed
    basis: "通过 git -C project-control ls-remote origin main 在线核实完整 SHA 为 06d1b2d54fdca8a19b345109a3b967910ddb9861；宿主机 docker inspect 确认容器 ID、镜像 digest、exited 状态及 /workspace 挂载。"
  protocol_compatibility:
    result: not-applicable
    basis: 本任务为 COORD 调度基础设施，不修改 MiniMCProto 业务协议字段。
  claim_scope:
    result: passed
    basis: 本报告结论仅针对当前调度代码、QA 报告闭环及本次锁定候选的运行证据。
  architecture_completeness:
    result: failed
    basis: "runner.py 的报告复审 TypeError 回退会丢失专属审阅上下文；已有 report_review 字段可绕过本次复审验证。"
---

# AUTO-02 run_11 独立 QA 审查报告

## 审查结论

**决定：REJECTED。** 锁定候选、服务器测试结果、容器物证和指定负例测试均完成核验；但 `runner.py` 的 QA 报告复审路径仍存在可绕过专属 ARCH 复审约束的实现路径，因此不能批准该候选。

本报告记录的平台为 Codex。当前执行环境标识为 GPT-6，无法核实其为任务卡要求的 `gpt-6-luna`；任务卡中预登记的 reviewer session 没有 `session_evidence`，本审查也未取得能将该 session UUID 与当前运行绑定的会话审计记录。因此模型和独立会话来源没有被本报告伪称为已验证。该身份记录缺口不影响下述源码发现及 REJECTED 决定。

## 候选和来源核验

- `project-control` 本地只读快照 HEAD 为 `06d1b2d54fdca8a19b345109a3b967910ddb9861`；`test_harness` HEAD 为 `210ddd1c3f6f59594836c91b68aae55fb7a35181`。
- 执行 `git -C project-control ls-remote origin main`，远端完整 SHA 为 `06d1b2d54fdca8a19b345109a3b967910ddb9861`，与锁定候选一致。
- 对 `result.md`、`server_qa.json` 和 frontmatter 列出的 12 个代码/配置文件执行 SHA256 重算，均与所提供摘要一致。
- `server_lock.json` 将两个仓库分别绑定至对应 `refs/heads/main` 和完整提交 SHA；容器挂载位置是服务端沙箱快照的 `/workspace`，未见 developer mounts。

## 针对 run_10 阻断项的复核

### 1. QA 报告引用必须预填路径和摘要

`runner.py:_resolve_qa_report_ref` 直接读取 `report_path` 与 `report_sha256`。任一缺失或为空时抛出 `CoordRunnerError("QA review entry missing mandatory report_path or report_sha256")`；之后确认物理文件存在，并对磁盘字节重算 SHA256，与预填值不一致则 fail-closed 抛错。实现中未发现自动补写摘要逻辑。

以下指定专项负例存在且在本次 64 项 `test_coord_runner.py` 套件中通过：

- `test_runner_resolve_qa_report_missing_entry_sha_rejected`
- `test_runner_resolve_qa_report_missing_entry_path_rejected`

相邻的物理文件缺失及预填摘要不匹配测试也存在并通过。

### 2. ARCH QA 报告复审专属调用

正常路径会将 `{"role": "ARCH", "report_path": rep_path, "report_sha256": rep_sha, "review_kind": "qa_report"}` 传给审阅执行器，并核验返回的 reviewer/session 不是 QA reviewer 或作者，且 decision 为 `APPROVED` 后才写入 `qa_entry["report_review"]`。拒绝结果调用 `handle_remediation`。指定的拒绝负例 `test_execute_review_phase_qa_report_review_rejected` 在本次套件中通过。

但实现仍有两条绕过/降级路径，构成拒绝项：

1. `runner.py:_invoke_report_reviewer` 在专属字典调用抛出 `TypeError` 时，依次回退为普通 `"ARCH"` 参数或两参数调用。回退调用不包含 `report_path`、`report_sha256` 或 `review_kind`，却可能返回普通代码审查结果并被当作报告复审结果。TypeError 也可能来自执行器内部，而不只是签名不匹配。专属复审必须 fail-closed，不能丢弃上下文后继续。
2. `_ensure_qa_report_review` 遇到已有 truthy `qa_entry["report_review"]` 就直接返回成功，不核验其 reviewer、decision、路径和摘要，也不触发本次专属复审调用。因此预置的旧值/伪造值可绕过独立会话与摘要校验。

当前专项拒绝测试只覆盖专属调用返回 `REJECTED`，没有覆盖执行器对专属调用抛出 `TypeError`，也没有覆盖预置无效 `report_review`。建议修复为：专属调用错误直接失败；任何已有复审记录也必须重新校验 reviewer 独立性、批准状态、报告路径与磁盘摘要绑定，或拒绝预置记录。

### 3. Docker 容器 inspect 物证

源码 `stop_docker_sandbox` 使用 `docker stop -t 2 <container_id>`，没有删除容器。宿主机实际执行 `docker inspect abcaee7952e4`，确认容器存在，完整 ID 为 `abcaee7952e4d8aac8d1a878cb41552aa3654de14213f0749753fdf3a8802ed6`，状态为 `exited`，镜像 ID/digest 为 `sha256:43a2f1c6c95b1df70095eb744d5eadc9225867e0d7a2feda9b41ec3b6d38c825`，挂载目标为 `/workspace`。

`server_qa.json` 的 `container_inspect.state` 是执行时采集的 `running` 状态；这与测试完成后本次宿主机 inspect 的 `exited` 状态属于不同时间点。停止后 inspect 的 ExitCode 为 137；容器仍保留，身份、镜像和挂载均与服务端证据一致。此状态核验通过。

## 实际测试与 AST 扫描

在容器 `abcaee7952e4` 重启后，对挂载的锁定快照执行以下命令。project-control 命令 cwd 为 `/workspace/project-control`，harness 命令 cwd 为 `/workspace/test_harness`：

| 命令 | 结果 |
|---|---|
| `python3 tools/test_coord_runner.py` | exit 0；64 tests，OK |
| `python3 tools/test_qa_runner.py` | exit 0；21 tests，OK |
| `python3 tools/test_delivery_checks.py` | exit 0；20 tests，OK |
| `python3 tools/test_check_task_graph.py` | exit 0；12 tests，OK |
| `./runner/qa_entrypoint.sh --suite all` | exit 0；`cascade_vectors` 与 `hil_unit` 两个 suite 均 PASSED |

合计为 117 个 unittest 加两个 harness suite，即 119 项检查，全部 exit 0。测试执行前后检查的快照 HEAD 与锁定 SHA 一致。未执行构建；该候选没有登记构建结果。

在同一容器内使用 Python `ast` 解析 `/workspace/project-control/tools` 下全部 18 个 Python 文件，扫描 298 个 `FunctionDef`/`AsyncFunctionDef`，以 AST 起止行计函数长度、以位置/普通/仅关键字参数计参数数目。结果为 0 项超过 50 行或 4 个参数。扫描命令 exit 0。此结果只覆盖这 18 个 Python 工具文件，不推断未纳入该目录的代码。

## 必需证据和未覆盖项

- 服务端 `server_qa.json` 声明 `passed: true`，记录 5 组命令全部 exit 0。本次在对应容器快照中重跑后同样全部通过。
- 远端 `project-control/main` 在线核验通过；本轮未另行查询 `test_harness` 远端 ref，使用 server lock 与容器内 checkout SHA 核对其候选版本。
- 没有独立会话审计记录证明当前 reviewer 会话 UUID 与任务卡中预登记 UUID 对应，也无法证明实际模型为任务要求的 gpt-6-luna。
- 未覆盖 `_invoke_report_reviewer` 的 TypeError 回退和预置 `report_review` 绕过路径；源码审查表明两者均可能避开强制专属复审，构成 REJECTED 的实现原因。

## 决定依据

锁定提交、报告摘要、测试套件、AST 限制扫描和 Docker inspect 物证均通过核验；但 run_10 的“ARCH QA 报告复审必须由专属、独立会话调用并绑定准确报告字节”阻断项并未完全闭环。专属上下文可因 `TypeError` 回退而丢失，已有未验证的 `report_review` 又可直接放行。按 fail-closed 要求，**本候选决定为 REJECTED**。修复后应生成新候选并由符合任务规定模型和可核验独立会话来源的 QA 重新审查。
