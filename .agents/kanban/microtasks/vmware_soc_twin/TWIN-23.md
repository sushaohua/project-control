---
id: TWIN-23
title: TWIN-23 VMware离线G-code作业流式空跑与运控执行器实现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: in-progress
owner: session-eng-state-twin-23
proposed_owner: ENG-STATE
executor:
  role: ENG-STATE
  agent_id: session-eng-state-twin-23
  run_id: run_01
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
    planned_session_alias: planned-qa-twin-23
    session: planned-qa-twin-23
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
    report_review:
      session: planned-arch-twin-23
      role: ARCH
      decision: null
      reviewed_task_revision: null
      artifact_version: null
      evidence: null
      report_sha256: null
      session_evidence: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-23
    session: planned-arch-twin-23
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-011
related_work_packages:
- TASK-002
- TASK-007
- TASK-008
depends_on:
- TWIN-17
- TWIN-18
- TWIN-19
- TWIN-21
- TWIN-22
dependency_conditions:
- task: TWIN-17
  accepted_version: 00c8cbdd86cfde78e7df10082c96cdae98b8f338
  acceptance_evidence: docs/evidence/twin/TWIN-17/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-17离线作业引擎与混色契约
- task: TWIN-18
  accepted_version: 579fd108ee7f12b0daf90d8a1559b61b73c62bf3
  acceptance_evidence: docs/evidence/twin/TWIN-18/runs/run_03/qa_review_report.md
  required: 开工前继承TWIN-18运控/调平/断料底层调查对账规范
- task: TWIN-19
  accepted_version: fa602d359329e5f588b6056a15ca340836f0bc0c
  acceptance_evidence: docs/evidence/twin/TWIN-19/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-19全机HMS 0x3001断料错误码与双级急停熔断逻辑
- task: TWIN-21
  accepted_version: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  acceptance_evidence: docs/evidence/twin/TWIN-21/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-21 MC固件0x16 20B坐标查询响应基线
- task: TWIN-22
  accepted_version: 6bce985fc81e779a1cf63d3eeb1f09c69d806a6c
  acceptance_evidence: docs/evidence/twin/TWIN-22/runs/run_01/qa_review_report.md
  required: 开工前继承TWIN-22 AP温度倍数与故障哨兵防御性治理基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - contracts/twin/job/**
  - tests/job/**
  project-control:
  - docs/evidence/twin/TWIN-23/**
allowed_paths:
- soc-ap/contracts/twin/job/**
- soc-ap/tests/job/**
- project-control/docs/evidence/twin/TWIN-23/**
source_baseline:
  project-control: 8f228399e52df6e50e82c81d33161c9ec42d4a13
  soc-ap: cb70d59e949396f45aec94d33ae23cab75beb282
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: cb70d59e949396f45aec94d33ae23cab75beb282
candidate_commit: null
dispatch_binding:
  source_commit: cb70d59e949396f45aec94d33ae23cab75beb282
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
  sha256: 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease:
  owner: session-eng-state-twin-23
  task_revision: 1
  lease_id: lease-twin-23-run-01
  expires_at: '2026-10-31T22:00:00+08:00'
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；接口/实现自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/contracts/twin/job/job_executor.h
  - soc-ap/contracts/twin/job/job_executor.c
  - soc-ap/tests/job/test_job_executor.c
  record: docs/evidence/twin/TWIN-23/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-23
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: run_job_executor_tests
    cwd: soc-ap
    command: bash -c "gcc -std=c11 -Wall -Wextra -Werror -Icontracts/twin/job -Icore/state/hms -o /tmp/test_job_executor contracts/twin/job/job_engine.c contracts/twin/job/job_executor.c tests/job/test_job_executor.c && /tmp/test_job_executor"
    expected: 作业流式空跑与运控执行器全测试通过
    availability: local
  positive_cases:
  - 接入 job_engine 离线解析引擎，流式读取并解析 G-code 指令流（G0/G1/G28/M163/M164）
  - 严格执行选项 A 强电安全门禁：拦截所有 M104/M109/M140/M190 加热指令，加热占空比硬锁死为 0%，安全空跑走线
  - 驱动 CoreXY 运控步进走线，模拟或对接 MC 0x16 坐标查询反馈，实时维护物理坐标（pos_x_um, pos_y_um, pos_z_um, pos_e_um）
  - 联锁断料检测与急停熔断：捕获 HMS 0x3001 断料错误即时安全暂停；捕获 M112 瞬时急停熔断
  - 输出完整快照：包含作业状态、当前行/总行数、千分比进度、已用时间、实时坐标与混色通道比
  - 严格遵守 C/C++ 硬性门禁：自研函数 <= 50 行，参数 <= 4 个，首行 Guard Clause，零动态堆内存分配
  negative_cases:
  - 严禁向 MC 下发任何非 0% 占空比的加热升温指令
  - 未回零（is_homed == false）时禁止启动打印作业
  - 处于急停状态下严禁接受任何恢复指令
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T15:00:00+08:00'
---

# TWIN-23 VMware离线G-code作业流式空跑与运控执行器实现

## 范围与交付
本任务承接首版本地正常打印闭环目标（U-D02）与第一阶段选项 A 台架底线要求（U-D03），实现上位 AP 的离线作业流式执行器（Job Streaming Executor）：
1. 衔接 `TWIN-17` 的 `job_engine.c` 离线解析引擎与 `TWIN-21` 的 MC 运控坐标系统；
2. 严格执行选项 A（Dry-run 空跑）安全规范：过滤/锁定所有加热指令（M104/M109/M140/M190 占空比恒为 0%），杜绝强电风险；
3. 支持 G0/G1 CoreXY 线性插补走线与 G28 回零联动；
4. 联动 `TWIN-19` 的 HMS 统一错误码（0x3001 断料自动触发安全暂停挂起）与 M112 双级急停即刻熔断；
5. 导出统一作业状态快照供 UI 网关与 Web HMI 订阅呈现；
6. 严格执行自研函数 $\le 50$ 行、参数 $\le 4$ 个、首行卫语句防空指针及绝对零堆内存分配硬性门禁。
