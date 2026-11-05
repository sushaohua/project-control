---
id: TWIN-53
title: TWIN-53 加固deploy_twin.sh后台守护进程会话隔离、SIGHUP免疫与四进程存活探针
revision: 1
plan_revision: vmware-soc-twin-20261105
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_02
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
issue_id: ISS-20261105-003
demand_id: DEM-20261105-003
confirmation_id: CONFIRM-SOC-AP-ISSUES-20261105
approval_id: APPR-20261105-001
accepted_scope: "Software and POSIX process-session sandbox verification of soc-ap/tools/deploy_twin.sh (ensure_third_party_built optional.hpp engaged-guard check, launch_detached_daemon via setsid+nohup+</dev/null+disown for all 4 daemons, and check_all_daemons_alive readiness/anti-false-positive gate) and soc-ap/tools/twin_build/test_deploy_daemon_survival.sh (sub-session exit + SIGHUP 4-daemon survival, fd/0 -> /dev/null verification, --status/--stop convergence, and negative early-crash/single-daemon-kill detection). Cross-compiler ELF build, host cgroup/container teardown survival, and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-53
    session: 01a1a9ae-e883-7270-8cdd-358b3b47aed9
    reviewer_session: 01a1a9ae-e883-7270-8cdd-358b3b47aed9
    commit_sha: 87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-53/runs/qa_02/codex_events.jsonl
      sha256: 4c6bf166ca1781b694039dde1aabf655fcfd13e6fbfbaa22f21d67acbef91629
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd; soc-ap=87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-53/runs/qa_02/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-53/runs/qa_02/qa_review_report.md
    report_sha256: 8737161b6c6a3eaa3414972a79350e3f6fc8312ae08323343e69857cbcbecd0d
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-004
- TASK-007
depends_on:
- TWIN-49
- TWIN-51
- TWIN-52
dependency_conditions:
- task: TWIN-49
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-49/runs/qa_04/qa_review_report.md
  required: 继承TWIN-49 deploy_twin.sh一键编译与清场基线
- task: TWIN-51
  accepted_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd; soc-ap=75f8a1a670edabb21c8d3dfc79243e06f73099af; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-51/runs/qa_02/qa_review_report.md
  required: 继承TWIN-51 test_backoff.cpp GCC 15编译修复
- task: TWIN-52
  accepted_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd; soc-ap=ad2538ae7f4834cac98be97e08b055f80eb81cfc; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-52/runs/qa_03/qa_review_report.md
  required: 继承TWIN-52 Fast-CDR optional补丁与DDS守护进程防SIGSEGV修复
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - tools/deploy_twin.sh
  - tools/twin_build/test_deploy_daemon_survival.sh
  project-control:
  - docs/evidence/twin/TWIN-53/**
allowed_paths:
- soc-ap/tools/deploy_twin.sh
- soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
- project-control/docs/evidence/twin/TWIN-53/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
- soc-ap/tests/**
- soc-ap/services/**
- soc-ap/middleware/**
source_baseline:
  project-control: 491158cd4f183a01517c36fb093821db54a8a6dd
  soc-ap: ad2538ae7f4834cac98be97e08b055f80eb81cfc
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
base_commit: ad2538ae7f4834cac98be97e08b055f80eb81cfc
branch: main
candidate_commit: 87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a
dispatch_binding:
  source_commit: ad2538ae7f4834cac98be97e08b055f80eb81cfc
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 2c3bba7cb6037cb8f89a6231008eafaa8bd4b8fcf90e81a7560742bafb8b200c
protocol_input:
  path: project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
  sha256: 2c3bba7cb6037cb8f89a6231008eafaa8bd4b8fcf90e81a7560742bafb8b200c
  revision: 4
icd_versions:
- path: project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
  version: 4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- soc-ap/AGENTS.md
- soc-ap/.agents/rules/shared/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md
worktree: soc-ap
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-53-20261105-01
  expires_at: '2026-11-05T16:00:00+08:00'
resources:
- resource: integrator-deploy-env
  location: soc-ap
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；会话退出与SIGHUP四进程存活回归自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/tools/deploy_twin.sh
  - soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
  record: docs/evidence/twin/TWIN-53/runs/author_02/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- tools/deploy_twin.sh tools/twin_build/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-53
  acknowledgement: received-author_02-87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a
verification:
  commands:
  - id: test_deploy_twin_session_disconnect_and_four_daemon_survival
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin53 && mkdir -p /tmp/qa_twin53/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin53/bin/curl\"); p.write_text(\"#!/usr/bin/env python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status)) if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\"); p.chmod(0o755)" && export PATH="/tmp/qa_twin53/bin:$PATH" && cp -r ../soc-ap /tmp/qa_twin53/soc-ap && ([ -e /tmp/qa_twin53/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin53/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin53/soc-ap/third_party/install)) && cd /tmp/qa_twin53/soc-ap && bash tools/twin_build/test_deploy_daemon_survival.sh && rm -rf /tmp/qa_twin53'
    expected: 子Shell与独立会话执行deploy_twin.sh退出并收到SIGHUP后，dbus-daemon、forward_service_daemon、device_manager_daemon、ui-gateway四个守护进程100%存活（非Z态）、fd/0均重定向至/dev/null、--status返回0、HTTP接口正常响应200，且任一守护进程异常退出时--status与就绪探针准确返回非0并清理
    availability: available
  positive_cases:
  - deploy_twin.sh通过setsid+nohup+</dev/null+disown启动全部4个守护进程，调用Shell退出及SIGHUP广播后4个守护进程全部持续存活
  - 就绪探针同时校验HTTP 200与全部4个守护进程PID存活，--status返回0且--stop干净回收全部进程
  negative_cases:
  - 若任一后台守护进程（如forward_service_daemon或device_manager_daemon）在启动期崩溃退出，deploy_twin.sh拒绝因静态/api/v1/state文件误报成功，立即返回非0并清理残留进程
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-05T10:31:00+08:00'
---

# TWIN-53 加固deploy_twin.sh后台守护进程会话隔离、SIGHUP免疫与四进程存活探针

## 1. 任务目标与来源
- **关联收件**：[`ISS-20261105-003.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/issues/ISS-20261105-003.yaml) / `DEM-20261105-003`
- **ARCH 方案依据**：[soc_ap_build_and_startup_issues_arch_breakdown_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md) (`revision: 1`, SHA-256 `04be47f7ca02f7a98e4f249e8313309d32c9642a07574c011cb2161014ac5b36`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `soc-ap/tools/deploy_twin.sh` 中统一通过 `launch_detached_daemon()`（`setsid nohup ... < /dev/null` + `disown`）启动 `dbus-daemon`、`forward_service_daemon`、`device_manager_daemon`、`ui-gateway` 四个核心守护进程，并在就绪轮询中强制校验全部 4 个进程 PID 存活。
2. 新增 `soc-ap/tools/twin_build/test_deploy_daemon_survival.sh` 验证子会话退出与 `SIGHUP` 广播后 4 个守护进程存活及反向故障拦截。
