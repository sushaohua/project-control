---
id: TWIN-35
title: TWIN-35 VMware宿主机端到端Web界面操作打印闭环综合验收
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: completed
owner: 6f94fd50-14cc-4b73-8837-03d6b03d5707
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: 6f94fd50-14cc-4b73-8837-03d6b03d5707
  run_id: run_02
reviewer:
- ARCH
- QA
verifier: 00c153ce-1d55-49b4-a3aa-7df50e168c29
integrator: INTEGRATOR
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: session-qa-hil-twin-35
    session: 01a19ac9-79d4-7642-9947-2922a15c13f7
    session_evidence: docs/evidence/twin/TWIN-35/runs/run_02/sessions/codex_session_01a19ac6-cb27-7e10-9be9-555256c71011.jsonl
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0
    evidence: docs/evidence/twin/TWIN-35/runs/run_02/qa_review_report.md
    report_sha256: 770c1a64650930716da6472f07ec56efad96b0effce5eacdc9f8d6d828929fb2
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: session-arch-review-35
    session: 245429ef-cba5-4ff3-8c9f-a473a4f79fc1
    session_evidence: docs/evidence/twin/TWIN-35/runs/arch_01/arch_review_report.md
    decision: APPROVED
    reviewed_task_revision: 2
    artifact_version: soc-ap=12a3f9a84c21a5ce70ef264bee041249c60240a0
    evidence: docs/evidence/twin/TWIN-35/runs/arch_01/arch_review_report.md
    report_sha256: 95bf7ee910b32e0c76b5d89ecee5bf15ebabfb43df6ccaaf4bf636e0ed4905de
  verifier_session: 00c153ce-1d55-49b4-a3aa-7df50e168c29
  integrator_session: 6f94fd50-14cc-4b73-8837-03d6b03d5707
primary_work_package: TASK-010
related_work_packages:
- TASK-009
- TASK-011
depends_on:
- TWIN-30
dependency_conditions:
- task: TWIN-30
  accepted_version: project-control=3347b2c5898d9ba943a5ba0c9a7ea2b7b25203b5
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30 Web HMI全流程基线与版本展示UI
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - tests/integration/**
  project-control:
  - docs/evidence/twin/TWIN-35/**
allowed_paths:
- soc-ap/tests/integration/**
- project-control/docs/evidence/twin/TWIN-35/**
source_baseline:
  project-control: 4960ec3c77aafb2e6b9c00fc7f6fda1f0f4aad27
  soc-ap: 8581872d76d52f939a6e0042a3ab1a138b5cd363
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 3a10e16beae43e51fc9673925179471e43f66114
base_commit: 8581872d76d52f939a6e0042a3ab1a138b5cd363
candidate_commit: null
dispatch_binding:
  source_commit: 8581872d76d52f939a6e0042a3ab1a138b5cd363
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    TWIN-41: 69212b70073f42ad87f3b19e1464c0386d090d14
    TWIN-42: 69212b70073f42ad87f3b19e1464c0386d090d14
protocol_input:
  path: project-control/docs/planning/ui_ux_end_to_end_interaction_design_20261031.md
  sha256: bde64b69b88556659cee48c87d2e648ad51d60a76b88250cc8f317102ff5e7f2
  revision: 1
read_sources:
- project-control/docs/planning/product/first_release_scope_decision_20261029.md
- soc-ap/tests/integration/test_first_release_print_loop.c
- project-control/.agents/rules/e2e_issue_verification_flow.md
worktree: soc-ap
lease:
  owner: session-integrator-twin-35
  task_revision: 2
  lease_id: lease-twin-35-run-02
  expires_at: '2026-11-03T18:00:00+08:00'
resources:
- resource: vmware-cluster-8080
  location: 192.168.77.134:8080
  exclusive: true
  pending: []
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；端到端集成测试自检；双独立沙箱检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
trigger_contracts:
- feature_id: FEAT-HMI-004-OOBE
  trigger_owner: ENG-FWD (aisoc_forward_service / aisoc_device_manager)
  trigger_event: 开机检测到USB连接或Web端进入向导触发CMD_GET_VERSION
  contract_ref: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  call_chain:
  - Web UI (app.js)
  - UI Gateway (/api/v1/temperature/snapshot)
  - D-Bus (org.aisoc.Device)
  - Forward Service (CMD_GET_VERSION 0x01)
  - MiniMCProto (MC/TH 0x02/0x03)
  completion_signal: 返回CMD_VERSION_REPORT，devices.mc/th更新为ONLINE且valid=true
  deadline_and_failure: 3000ms超时，超时保留UNKNOWN并记录Issue
  retry_cancel_reconnect: 拔线后3s衰退至OFFLINE，重连后自愈重读
  not_applicable_reason: null
- feature_id: FEAT-MOT-001-JOG
  trigger_owner: ENG-STATE / ENG-FWD
  trigger_event: 用户点击轴控罗盘Jog按钮
  contract_ref: soc-ap/contracts/minimcproto/v2-commands.md
  call_chain:
  - Web UI (/api/v1/motion/jog)
  - UI Gateway
  - D-Bus (MotionService)
  - Forward Service (G0/G1)
  - MC (ACK)
  completion_signal: MC回传ACK且坐标刷新
  deadline_and_failure: 5000ms超时，超时返回HTTP 504并Toast报错
  retry_cancel_reconnect: 幂等点动，防止连续狂点堆积
  not_applicable_reason: null
normal_e2e_acceptance:
  plan_ref: project-control/docs/planning/e2e_normal_flow_acceptance_plan_20261102.md
  coverage_matrix: project-control/docs/planning/e2e_normal_flow_acceptance_plan_20261102.md#用例覆盖矩阵
  required_gates:
  - software
  - real-hil
  issue_refs:
  - ISSUE-20261102-01
deliverables:
  artifacts:
  - soc-ap/tests/integration/test_web_print_loop.py
  record: docs/evidence/twin/TWIN-35/runs/run_02/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-35
  acknowledgement: null
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误
    availability: local
  positive_cases:
  - 在 VMware 环境通过 Web 页面完整闭环执行一次本地打印（选模型->G28回零->流式空跑->监视->完成）
  - 验证网页端开始/暂停/继续/取消按钮与后台状态机同步
  - 验证网页端红色 E-STOP 紧急急停按钮即时熔断
  - 验证 5x5 调平热力图与手动轴控响应
  - 验证新机向导 OOBE 正常连接探测、有效数据显示与工作台导航持久化
  - 严格保持 Option A 强电 0% 锁死安全基线
  negative_cases:
  - 任何升温命令严禁输出到物理发热元件
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-02T12:00:00+08:00'
---

# TWIN-35 VMware宿主机端到端Web界面操作打印闭环综合验收 (Revision 2)

## 任务目标
由 INTEGRATOR 联合 QA，在 VMware 真实运行环境（`192.168.77.134:8080`）完成“当前功能正常流程优先”的端到端 Web 界面操作打印闭环综合验收与 Issue 闭环。
