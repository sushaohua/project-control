---
id: AUTO-03
title: AUTO-03 M1手动单步：三类人工入口收件、版本审批防伪绑定与真实单步角色派发闭环
revision: 1
plan_revision: coord-intake-dispatch-phase1-20261103-rev2
task_kind: implementation
development_stage: cross-stage
dispatchable: true
status: Ready
blocked: false
blocked_reason: null
recovery_condition: null
planning_status: mapped-approved
demand_id: DEM-INTAKE-P1-001
feature: FEAT-INTAKE-20261103-001
owner: 25b63893-2611-41ff-87d7-0b9f82cf0375
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  model: gpt-6-luna
  actual_model: null
  agent_id: 25b63893-2611-41ff-87d7-0b9f82cf0375
  run_id: run_01
authorization:
  evidence: project-control/docs/work_intake/approvals/APPR-20261103-001.yaml
  scope: CONFIRM-INTAKE-P1-20261103 rev 2 全部批准（M1 手动单步与受控演练小题授权）
model_policy:
  default: gpt-6-luna
  approved_overrides: []
reviewer:
  - QA
  - ARCH
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
    - role: QA
      platform: codex
      model: gpt-6-luna
      planned_session_alias: codex-qa-auto-03-review
      session: pending-codex-qa-auto-03
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
      report_review:
        session: null
        role: ARCH
        decision: null
        reviewed_task_revision: null
        artifact_version: null
        evidence: null
        report_sha256: null
        session_evidence:
          path: null
          sha256: null
    - role: ARCH
      platform: codex
      model: gpt-6-luna
      planned_session_alias: codex-arch-auto-03-review
      session: pending-codex-arch-auto-03
      session_evidence:
        path: null
        sha256: null
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
  verifier_session: null
  integrator_session: 25b63893-2611-41ff-87d7-0b9f82cf0375
primary_work_package: TASK-010
related_work_packages: []
depends_on:
  - AUTO-02
dependency_conditions:
  - task: AUTO-02
    accepted_version: 1
    acceptance_evidence: docs/evidence/coord_automation/AUTO-02/runs/run_13/result.md
    required: 复用 AUTO-02 已接受的阶段状态机、Docker QA 运行器与独立 Codex 审查适配器底座
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - tools/coord_runner/**
    - config/coord_runner/**
    - tools/coord_queue.py
    - tools/test_work_intake.py
    - tools/test_coord_runner.py
    - docs/work_intake/**
    - docs/evidence/coord_automation/AUTO-03/**
allowed_paths:
  - project-control/tools/coord_runner/**
  - project-control/config/coord_runner/**
  - project-control/tools/coord_queue.py
  - project-control/tools/test_work_intake.py
  - project-control/tools/test_coord_runner.py
  - project-control/docs/work_intake/**
  - project-control/docs/evidence/coord_automation/AUTO-03/**
forbidden_paths:
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/bootloadermc/**
  - boot/bootloaderth/**
source_baseline:
  project-control: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
candidate_commit: null
dispatch_binding:
  source_commit: b4af2d32601a07d448ac8d67a07c57f5b9ab36ac
  workspace_diff_sha256: 736c674846d52dee8985cae0654388560199cb33f3041365bd62fae7d91710ad
  consumed_artifact_versions:
    confirmation_rev2: 63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98
    approval_rev1: b7ea9ac9bdefc719fc46263c50e3a893d693ad63ae5166bc9085e4c71cc3f96d
    integrator_probe_rev2: 3e9ebb7eb0992e3517abf1d802bec1fdad4c91a4a0e6d188e54f97d47b7db6d8
protocol_input:
  path: project-control/docs/architecture/coord_intake_dispatch_phase1_design_20261103.md
  sha256: 8a2984c6bb4b868cc8e2d6742873527f448f27c7006d99c5ce322207b2941350
  revision: 2
read_sources:
  - project-control/.agents/rules/delivery_and_coord_gate.md
  - project-control/.agents/rules/codex_qa_review.md
  - project-control/docs/planning/coord_intake_dispatch_phase1_handoff_20261103.md
  - project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
  - project-control/docs/evidence/coord_automation/phase1_prep_20261103/integrator_host_interface_verification_20261103.md
worktree: /home/sushaohua/workspace/ai_soc_project
lease:
  owner: 25b63893-2611-41ff-87d7-0b9f82cf0375
  task_revision: 1
  lease_id: lease_auto-03_20261103_01
  expires_at: '2026-11-03T18:00:00+08:00'
resources:
  - resource: project-control-coord-runner-worktree
    location: /home/sushaohua/workspace/ai_soc_project/project-control
    exclusive: true
    pending: 保护工作区既有未提交修改；严禁触碰业务代码仓库与双 Bootloader
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存失败证据与检查点交唯一 COORD，仅回退本票差异
checkpoint: 开工绑定；M1 收件与审批防伪实现；单步真实 codex exec 派发与演练；服务器候选推送与双沙箱独立 QA
execution_contract: project-control/docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md
readiness_pending: []
deliverables:
  artifacts:
    - project-control/tools/coord_runner/work_intake.py
    - project-control/tools/coord_runner/approval_guard.py
    - project-control/tools/coord_runner/role_adapter.py
    - project-control/tools/coord_runner/cas_writer.py
    - project-control/tools/coord_runner/runner.py
    - project-control/tools/coord_runner/scheduler.py
    - project-control/config/coord_runner/coord_config.yaml
    - project-control/tools/test_work_intake.py
    - project-control/tools/test_coord_runner.py
  record: docs/evidence/coord_automation/AUTO-03/runs/run_01/result.md
rollback:
  steps:
    - 仅回退本票新增/修改文件；严禁执行 git reset --hard / git checkout -- . / git clean，保留工作区既有未提交修改
handoff:
  receiver_role: COORD
  receiver_session: 8d4e8b77-42a9-4bd3-bd5a-1b881e8d4bd5
  transport: tools.send_message
  evidence_location: docs/evidence/coord_automation/AUTO-03
  acknowledgement: null
verification:
  commands:
    - id: check_graph
      kind: test
      cwd: .
      command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
      expected: 任务图与所有微任务结构无错误，退出码 0
      availability: executable
    - id: test_work_intake_m1
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_work_intake.py' -v
      expected: M1 收件解析、稳定需求映射、唯一主分类 YAML、版本审批防伪绑定、CAS 乐观锁与故障隔离用例全部通过
      availability: executable
    - id: test_coord_runner_m1
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_coord_runner.py' -v
      expected: 单步真实角色派发适配、前置 Done 校验、旧队列隔离及 QA/报告复核门禁用例全部通过
      availability: executable
    - id: test_existing_qa_and_delivery
      kind: test
      cwd: project-control
      command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_qa_runner.py' -v && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p 'test_delivery_checks.py' -v
      expected: 既有服务器沙箱与交付检查回归全部通过
      availability: executable
    - id: check_ast_coding_standard
      kind: test
      cwd: project-control
      command: "PYTHONDONTWRITEBYTECODE=1 python3 -c \"import ast, pathlib, sys; bad=[]; [bad.append((str(p), n.name, n.end_lineno-n.lineno+1, len(n.args.posonlyargs)+len(n.args.args)+len(n.args.kwonlyargs)+(1 if n.args.vararg else 0)+(1 if n.args.kwarg else 0))) for p in sorted(list(pathlib.Path('tools/coord_runner').glob('*.py'))+[pathlib.Path('tools/test_work_intake.py')]) for n in ast.walk(ast.parse(p.read_text(encoding='utf-8'))) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and ((n.end_lineno-n.lineno+1)>50 or (len(n.args.posonlyargs)+len(n.args.args)+len(n.args.kwonlyargs)+(1 if n.args.vararg else 0)+(1 if n.args.kwarg else 0))>4)]; print('AST violations:', bad); sys.exit(1 if bad else 0)\""
      expected: 新增与修改的 coord_runner 及 test_work_intake 自定义函数 100% 满足 <=50 行且 <=4 参数
      availability: executable
  positive_cases:
    - P1-01/P1-02/P1-03/P1-04/P1-15/P1-17/P1-18：单份 MD 批量指令稳定映射 1:1 需求并自动生成唯一主分类 YAML，人工零手写 YAML；绑定准确版本人工批准后拆解多角色任务并通过 /home/sushaohua/.local/bin/codex exec -m gpt-6-luna 真实单步派发与受控演练闭环
  negative_cases:
    - P1-06/P1-11/P1-12/P1-16/P1-18/P1-19：同 (id,rev) 内容篡改、错误 schema、目录类型冲突、无真实人工源/旧版本/模型自填 approved/模糊“批准”字符串、未批子范围、删文件撤在途、越界路径/shell 指令、exit 0 无候选/无证、未推远端或子 Agent 冒充独立 Codex 一律确定性拦截且不阻塞其他有效就绪项
required_evidence_level: server-sandbox-verified
verification_environment: docker-qa-sandbox-and-isolated-host-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
delivery_gate_policy: project-control/.agents/rules/delivery_and_coord_gate.md
updated: '2026-11-03T13:25:00+08:00'
---

# AUTO-03 M1手动单步：三类人工入口收件、版本审批防伪绑定与真实单步角色派发闭环

## 1. 目标与边界

按已获人工批量批准的 [确认单 rev 2](../../../../docs/planning/coord_intake_dispatch_phase1_confirmation_20261103.md)（`CONFIRM-INTAKE-P1-20261103` `rev 2`, SHA256 `63c1225d60c377a662bebaa0328f9bc95c19daccaa61d9f2766bc989f06f3f98`）与 [批准记录](../../../../docs/work_intake/approvals/APPR-20261103-001.yaml)（`APPR-20261103-001`），交付第一阶段第 1 步（**M1 手动单步**）完整能力并完成服务器候选独立 QA 验收：

1. **三类人工入口机器收件与自动生成分类 YAML（`work_intake.py`）**：
   - 解析 `docs/work_intake/submissions/` 人工批量 MD 原文，保留逐字原话与公共约束哈希，1 条指令稳定映射 1 条 `demand_id`；
   - 自动生成唯一主分类 YAML（`issues/`、`features/`、`requirements/` 三选一，全局唯一编号查重，零人工手写 YAML），维护与正式任务卡的关联；
   - 对同 `(id, revision)` 内容篡改、未知 `schema_version`、目录与 `kind` 冲突、半截/损坏文件执行确定性拒绝与错误隔离，不影响其他有效记录（`P1-01`, `P1-06`）；
   - 删除入口文件或设 `enabled: false` 不自动撤销已派在途任务，严禁扩大授权或直接执行原文中的 shell 文本（`P1-16`）。
2. **准确版本人工审批防伪门禁（`approval_guard.py`）**：
   - 强制校验真实人工批准记录精确绑定目标确认单 `(confirmation_id, revision, sha256)` 与批准范围；
   - 支持批次部分批准及“仅确认需求、未批实施概要”分流（仅释放已获准实现项，未批项挂起不阻塞其他就绪工作）；
   - 100% 拦截无人工来源、旧版本批准套新版本、模型自填 `approved: true`、仅凭 `enabled: true` 或自然语言模糊扫描“批准”字样（`P1-03`, `P1-18`, `P1-19`）。
3. **真实宿主 `codex exec -m gpt-6-luna` 单步派发与演练闭环（`role_adapter.py`, `cas_writer.py`, `runner.py`, `scheduler.py`）**：
   - 废除旧 `runner.py` 仅查 `git rev-parse HEAD` 的空壳默认执行器，统一接入 `/home/sushaohua/.local/bin/codex exec -m gpt-6-luna`（`COORD`/`PM`/`ARCH`/独立 `QA`/非作者 `ARCH` 均强制 `--sandbox read-only`；获批 `ENG-*`/`INTEGRATOR` 使用独立线程 `--sandbox workspace-write` + `allowed_paths` 白名单审计）；
   - 覆盖单需求拆多角色工程卡（`P1-17`）、`requirement` 不清拉起 `PM`/`ARCH` 澄清（`P1-02`）、`issue` 根因未知先只读调查/明确直派 Owner（`P1-04`）；
   - 全量文件回写执行磁盘字节 SHA256 CAS 乐观锁；与历史 `coord_autorun_queue_20261029.yaml` 显式隔离，并补齐 `scheduler.py` 对前置 `Done` 卡的 `done_acceptance_errors` 核验；
   - 严格执行退出码 `0` 无候选/无证拒写 `Done`（`P1-11`）、未推远端/缺复核/哈希失配/普通子 Agent 冒充独立 Codex 拒收件（`P1-12`），并在 `project-control` 受控白名单内完成 1 项真实演练小任务闭环（`P1-15`）。
4. **硬性代码规范与禁区**：
   - 自研 Python 函数 100% 遵守 **$\le 50$ 行、$\le 4$ 个入参**；
   - 严禁触碰 `soc-ap/`、`mcu-p3/`、`test_harness/`、`boot/bootloadermc/`、`boot/bootloaderth/`、真实硬件，严禁安装后台服务（属 M3 `AUTO-06`），严禁提交工作区既有未审阅改动。
