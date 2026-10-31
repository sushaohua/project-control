---
id: TWIN-30
title: TWIN-30 VMware全流程离线打印闭环集成验证与首版收件
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: session-integrator-twin-30
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: session-integrator-twin-30
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
    planned_session_alias: planned-qa-twin-30
    session: session-qa-twin-30
    session_evidence:
      path: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
      sha256: 0e999e80be64c45e46ec172d35d1953477d0f52bcfd8c345e50a8db583beba29
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
    evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
    report_sha256: 0e999e80be64c45e46ec172d35d1953477d0f52bcfd8c345e50a8db583beba29
    report_review:
      session: session-arch-twin-30
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 1
      artifact_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
      evidence: docs/evidence/twin/TWIN-30/runs/run_01/arch_review_report.md
      report_sha256: 108f13dfc0d5474b2ce4b3e14a47bac4aff803cfd8b7dffcf8328ea9c9f86e94
      session_evidence:
        path: docs/evidence/twin/TWIN-30/runs/run_01/arch_review_report.md
        sha256: 108f13dfc0d5474b2ce4b3e14a47bac4aff803cfd8b7dffcf8328ea9c9f86e94
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-30
    session: session-arch-twin-30
    session_evidence:
      path: docs/evidence/twin/TWIN-30/runs/run_01/arch_review_report.md
      sha256: 108f13dfc0d5474b2ce4b3e14a47bac4aff803cfd8b7dffcf8328ea9c9f86e94
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
    evidence: docs/evidence/twin/TWIN-30/runs/run_01/arch_review_report.md
    report_sha256: 108f13dfc0d5474b2ce4b3e14a47bac4aff803cfd8b7dffcf8328ea9c9f86e94
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-008
- TASK-009
- TASK-011
depends_on:
- TWIN-20
- TWIN-23
- TWIN-25
- TWIN-29
dependency_conditions:
- task: TWIN-20
  accepted_version: soc-ap=cb70d59e949396f45aec94d33ae23cab75beb282; project-control=f0fe3948482adb71e5366006850fdb9dd36282bc
  acceptance_evidence: docs/evidence/twin/TWIN-20/runs/run_02/qa_review_report.md
  required: 继承TWIN-20 Web HMI界面、料槽映射、OOBE与版本展示UI
- task: TWIN-23
  accepted_version: soc-ap=674e7336f924c2f297c439417a0011adc12427fa; project-control=e097299f1483d5192f3319996fa3008901f27613
  acceptance_evidence: docs/evidence/twin/TWIN-23/runs/run_01/qa_review_report.md
  required: 继承TWIN-23离线作业流式执行器与选项A强电0%硬锁死保护
- task: TWIN-25
  accepted_version: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  acceptance_evidence: docs/evidence/twin/TWIN-25/runs/run_01/qa_review_report.md
  required: 继承TWIN-25 AP端0x18调平网格拓扑解析与呈现基线
- task: TWIN-29
  accepted_version: soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454
  acceptance_evidence: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
  required: 继承TWIN-29双MCU版本查询链路与devices.mc/th四态衰退时序状态机
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - tests/integration/**
  project-control:
  - docs/evidence/twin/TWIN-30/**
allowed_paths:
- soc-ap/tests/integration/**
- project-control/docs/evidence/twin/TWIN-30/**
source_baseline:
  project-control: 362e4751f7bbdb85117f34c2ae77ec4bc268fdfb
  soc-ap: 674e7336f924c2f297c439417a0011adc12427fa
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 674e7336f924c2f297c439417a0011adc12427fa
candidate_commit: 7bb05218c39d6852cac5e8d86db845dbbedd7064
dispatch_binding:
  source_commit: 674e7336f924c2f297c439417a0011adc12427fa
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions: {}
protocol_input:
  path: project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md
  sha256: 596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/planning/product/product_feature_task_traceability_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease:
  owner: session-integrator-twin-30
  task_revision: 1
  lease_id: lease-twin-30-run-01
  expires_at: '2026-10-31T23:30:00+08:00'
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；端到端集成测试自检；准确候选独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/tests/integration/test_first_release_print_loop.c
  record: docs/evidence/twin/TWIN-30/runs/<actual-run>/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-autorun
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-30
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: run_integration_tests
    cwd: soc-ap
    command: bash -c "gcc -std=c11 -Wall -Wextra -Werror -Icontracts/twin/job -Icore/state/hms -Iservices/device_manager -Iservices/forward -o /tmp/test_first_release_print_loop contracts/twin/job/job_engine.c contracts/twin/job/job_executor.c tests/integration/test_first_release_print_loop.c && /tmp/test_first_release_print_loop"
    expected: 首版全流程闭环集成测试全部通过
    availability: local
  positive_cases:
  - 端到端串联离线作业引擎、流式执行器与权威状态机，验证首版本地打印完整闭环
  - 严格执行选项 A 强电安全门禁：所有加热指令占空比硬锁死为 0%，拦截并安全推进
  - 验证 G28 软件回零防护校验（未回零禁止启动，执行 G28 后允许启动）
  - 验证 CoreXY 微米走线调度与 MC 0x16 20B 坐标报文实时反向同步
  - 验证多通道混色比例设置（M163/M164 50:50 等）与料槽映射
  - 验证 HMS 0x3001 全机断料告警瞬时触发任务挂起暂停、停进给与恢复
  - 验证 M112 急停瞬时熔断、指令硬拒绝与显式清除急停复位
  - 验证 128B 权威快照原子导出，包含行号推进、千分比进度与完成态切换
  - 严格遵守 C/C++ 编码门禁：自研函数 <= 50 行，入参 <= 4 个，首行 Guard Clause，零堆分配
  negative_cases:
  - 严禁向 MC 下发任何非 0% 占空比的加热升温指令
  - 未回零状态下启动打印必须返回错误码被硬性拒绝
  - 急停熔断生效期间一切走线与步进指令必须被拒
---
# TWIN-30 VMware全流程离线打印闭环集成验证与首版收件

## 任务目标
承接首版本地正常打印闭环目标（U-D02）与纯逻辑空跑底线要求（选项 A / U-D03），基于 VMware 虚拟化双环境，对齐 U-D01 七项首版子范围与全机状态：
1. 验证 Web HMI 界面全流程（OOBE 新机向导、5×5 网格热力、料槽调色板映射、固件版本状态展示）；
2. 验证离线 G-code 作业流式调度、CoreXY 微米走线与 MC 0x16 20B 坐标报文反向同步；
3. 严格落实选项 A 强电 0% 锁死拦截（M4/M5/M6/M7 零占空比安全推进）；
4. 验证在环故障联锁：HMS 0x3001 断料瞬时暂停/停进给/恢复走线；M112 急停瞬时熔断/指令拒绝与清除复位；
5. 产出首版端到端全流程闭环集成测试用例 `test_first_release_print_loop.c` 并通过服务器双独立沙箱检验。
