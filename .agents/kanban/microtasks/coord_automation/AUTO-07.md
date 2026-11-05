---
id: AUTO-07
title: AUTO-07 接通CoordRunner启动/恢复与step人工收件检查点并修复分类账本摘要同步
revision: 1
plan_revision: coord-intake-dispatch-phase1-20261105
task_kind: implementation
development_stage: cross-stage
dispatchable: true
status: In-Progress
blocked: false
blocked_reason: null
recovery_condition: null
planning_status: active
demand_id: DEM-20261105-004
issue_id: ISS-20261105-004
confirmation_id: CONFIRM-COORD-INTAKE-20261105
approval_id: APPR-20261105-002
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
  - QA
verifier: null
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions: []
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages: []
depends_on:
  - AUTO-06
dependency_conditions:
  - task: AUTO-06
    accepted_version: e6e4291a9608473cae2604dceb521c930d0c341f
    acceptance_evidence: docs/evidence/coord_automation/AUTO-06/runs/run_03/qa_review_report.md
    required: 继承AUTO-06已验收的CoordRunner单实例锁、SQLite恢复源与WorkIntakeManager收件底座（保留AUTO-06 Done状态与历史证据）
scope_status: mapped
allowed_repositories:
  - project-control
write_scope:
  project-control:
    - tools/coord_runner/runner.py
    - tools/coord_runner/work_intake.py
    - tools/test_coord_runner.py
    - tools/test_work_intake.py
    - docs/work_intake/features/FEAT-20261104-001.yaml
    - docs/work_intake/features/FEAT-20261104-002.yaml
    - docs/work_intake/.intake_digests.json
    - docs/evidence/coord_automation/AUTO-07/**
allowed_paths:
  - project-control/tools/coord_runner/runner.py
  - project-control/tools/coord_runner/work_intake.py
  - project-control/tools/test_coord_runner.py
  - project-control/tools/test_work_intake.py
  - project-control/docs/work_intake/features/FEAT-20261104-001.yaml
  - project-control/docs/work_intake/features/FEAT-20261104-002.yaml
  - project-control/docs/work_intake/.intake_digests.json
  - project-control/docs/evidence/coord_automation/AUTO-07/**
forbidden_paths:
  - soc-ap/**
  - mcu-p3/**
  - test_harness/**
  - boot/bootloadermc/**
  - boot/bootloaderth/**
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-03.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-04.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-05.md
  - project-control/.agents/kanban/microtasks/coord_automation/AUTO-06.md
source_baseline:
  project-control: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
  soc-ap: 79932746d225bb115010c5545ef3f7499482e137
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
branch: main
candidate_commit: null
dispatch_binding:
  source_commit: 77c679616a09d9c82906ff9bdf27fefc6d6c343f
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: a79ebd9d6e77bb39b689366d03c66d7fe84c8b165dddd612369bf8cb88b8bc2e
protocol_input:
  path: project-control/docs/architecture/coord_intake_checkpoint_wiring_arch_breakdown_20261105.md
  sha256: a79ebd9d6e77bb39b689366d03c66d7fe84c8b165dddd612369bf8cb88b8bc2e
  revision: 1
icd_versions:
  - path: project-control/docs/architecture/coord_intake_checkpoint_wiring_arch_breakdown_20261105.md
    version: 1
read_sources:
  - project-control/.agents/rules/repository_rule_sources.json
  - project-control/.agents/rules/repository_rule_boundaries.md
  - project-control/.agents/rules/c_cpp_coding_standard.md
  - project-control/.agents/rules/code_documentation_standard.md
  - project-control/docs/architecture/coord_intake_checkpoint_wiring_arch_breakdown_20261105.md
worktree: project-control
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-auto-07-20261105-01
  expires_at: '2026-11-05T18:00:00+08:00'
resources:
  - resource: coord-runner-test-env
    location: project-control
    exclusive: true
    pending: null
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；restore_from_checkpoint与step检查点接通scan_work_intake；FEAT-20261104-001/002 r4摘要对齐；独立沙箱与Codex QA审阅
execution_contract: project-control/docs/planning/coord_autorun_tasklist_20261029.md
readiness_pending: []
deliverables:
  artifacts:
    - project-control/tools/coord_runner/runner.py
    - project-control/tools/coord_runner/work_intake.py
    - project-control/tools/test_coord_runner.py
    - project-control/tools/test_work_intake.py
    - project-control/docs/work_intake/features/FEAT-20261104-001.yaml
    - project-control/docs/work_intake/features/FEAT-20261104-002.yaml
    - project-control/docs/work_intake/.intake_digests.json
  record: docs/evidence/coord_automation/AUTO-07/runs/author_01/result.md
rollback:
  steps:
    - git -C project-control checkout -- tools/coord_runner/runner.py tools/coord_runner/work_intake.py tools/test_coord_runner.py tools/test_work_intake.py docs/work_intake/features/FEAT-20261104-001.yaml docs/work_intake/features/FEAT-20261104-002.yaml docs/work_intake/.intake_digests.json
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/coord_automation/AUTO-07
  acknowledgement: pending
verification:
  commands:
    - id: test_coord_intake_checkpoint_wiring_and_ledger_consistency
      cwd: project-control
      command: 'python3 -m tools.coord_runner --intake-scan && python3 -m unittest tools/test_work_intake.py tools/test_coord_runner.py tools/test_coord_recovery.py tools/test_coord_systemd_service.py -v'
      expected: coord_runner --intake-scan返回0且errors为空（FEAT-20261104-001@r4与FEAT-20261104-002@r4账本摘要一致）；test_work_intake、test_coord_runner（含step/restore检查点自动收件、重复检查幂等、坏文件隔离、AST函数<=50行且<=4参门禁）、test_coord_recovery与test_coord_systemd_service（含P1-14连续空闲轮询零模型调用）全部100% OK
      availability: available
  positive_cases:
    - CoordRunner在restore_from_checkpoint与step检查点自动调用scan_work_intake，新增Markdown提交单被识别一次并生成分类YAML，重复step不重复建单或调用模型
    - TaskLinkUpdate支持关联arch_breakdown并自动递增revision同步更新.intake_digests.json；FEAT-20261104-001/002升级为revision 4后--intake-scan零错误通过
    - 在途任务(in_flight_tasks)、恢复记录与单实例锁保持一致，收件扫描不绕过ApprovalGuard批准、技术前置或LeaseManager租约
  negative_cases:
    - 单份坏文件（格式损坏或同revision篡改）被隔离在intake.errors中，不阻断其他合法提交单收件，也不破坏在途任务恢复
    - 空闲轮询或未获批准的收件项严禁触发任何大模型调用或未授权派单；严禁将代码测试通过伪造为宿主机后台systemd服务已启用运行
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T11:57:30+08:00'
---

# AUTO-07 接通CoordRunner启动/恢复与step人工收件检查点并修复分类账本摘要同步

## 1. 任务目标与来源
- **关联收件**：[`ISS-20261105-004.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/issues/ISS-20261105-004.yaml) / `DEM-20261105-004`
- **ARCH 方案依据**：[coord_intake_checkpoint_wiring_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/coord_intake_checkpoint_wiring_arch_breakdown_20261105.md) (`revision: 1`, SHA-256 `a79ebd9d6e77bb39b689366d03c66d7fe84c8b165dddd612369bf8cb88b8bc2e`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `CoordRunner.restore_from_checkpoint()` 与 `CoordRunner.step()` 中接通 `scan_work_intake()`，新增提交在检查点被识别一次，重复检查幂等且零模型空耗。
2. 扩展 `TaskLinkUpdate` 支持 `arch_breakdown` 并自动递增 `revision` 同步 `.intake_digests.json`；将 `FEAT-20261104-001/002` 升级为 `revision: 4` 消除 `TAMPERED_SAME_REVISION` 告警。
3. 保留 `AUTO-06` 的 `Done` 和历史证据，明确区分代码检查点验证通过与宿主机后台 systemd 服务当前未启用（不与当前交互式 COORD 会话抢锁）。
