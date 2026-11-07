---
id: TWIN-68
title: TWIN-68 MC级联代理check_th_relay_timeout无符号时基下溢修复与回绕单测闭环
revision: 1
plan_revision: vmware-soc-twin-20261107
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: true
blocker_reason: "qa_runner.py 在调用 GitLab REST API v4 (http://192.168.77.113/api/v4/projects/sushaohua%2Fproject-control/repository/commits/...) 核验服务端锁定提交时返回 HTTP 401: {\"error\":\"invalid_token\",\"error_description\":\"Token is expired. You can either do re-authorization or token refresh.\"}（当前 ~/.bashrc 中的 GITLAB_TOKEN 已于 2026-11-07 过期；证据保存在 docs/evidence/twin/TWIN-68/runs/qa_01/sandbox.stderr）。"
unblock_condition: "请 Owner 在 GitLab (192.168.77.113) 刷新或重新签发具有 read_api/api 权限的 GITLAB_TOKEN 并更新环境变量（或 ~/.bashrc），随后 COORD 另建 qa_02 运行受控 Docker 沙箱与独立 Codex 只读审阅。"
planning_status: active
owner: 1e94997f-e120-4f43-b840-bceec750dc20
proposed_owner: ENG-MC
executor:
  role: ENG-MC
  agent_id: 1e94997f-e120-4f43-b840-bceec750dc20
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-003
feature_id: FEAT-20261106-001
demand_id: DEM-20261106-001
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (gcc + python3) verification of MC App check_th_relay_timeout and minimc_proto_poll timestamp sampling order fix & 32-bit half-space unsigned underflow guard (elapsed < 0x80000000UL), host unit test test_th_relay_timeout_underflow_and_wraparound in test_mc_ota_and_relay.c (verifying +1ms tick advance on TH relay TX without false TIMEOUT/BAD_FRAME 0x07, 32-bit counter wraparound across 0xFFFFFFFFU->0x00000000U, and normal timeout), full mcu-p3 motion-controller-mcu/tests/run_tests.sh regression suite, and S04 function length (<=50 lines), params (<=4) & Chinese comment checks. Cross-compiler arm-none-eabi-gcc ELF/bin build and physical HIL hardware execution are out of scope for qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-68-01
    session: null
    reviewer_session: null
    decision: PENDING
    commit_sha: null
    reviewed_task_revision: null
    artifact_version: null
    report_path: null
    evidence: null
    report_sha256: null
    session_evidence: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-64
- TWIN-67
dependency_conditions:
- task: TWIN-64
  accepted_version: project-control=6d8b9dc8a59366c9e0d0c8126240b1caf69ab321; soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1;
    boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba; boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
  acceptance_evidence: docs/evidence/twin/TWIN-64/runs/qa_04/qa_review_report.md
  required: 继承TWIN-64 mcu-p3 MC级联代理基线
- task: TWIN-67
  accepted_version: project-control=d9ed9b699067410f89c8119404f9895ec3fdb6f2; soc-ap=7184edfc796923e2f2c6e3e57ef3a9f791164b51;
    mcu-p3=3f1cfa66c6d27422cf038936b29aca7e45edb511; test_harness=cf81195eca55bcd772ef2daa2fd4aa41634c1492;
    boot/bootloadermc=faa2ed00dc9b6c8567dd44e875028f65073aab62; boot/bootloaderth=64b7100d3b0260ad1c24b627986475dcd45ad383
  acceptance_evidence: docs/evidence/twin/TWIN-67/runs/qa_03/qa_review_report.md
  required: 继承TWIN-67物理HIL级联实测日志与基线
scope_status: mapped
allowed_repositories:
- mcu-p3
- project-control
write_scope:
  mcu-p3:
  - motion-controller-mcu/project/src/minimc_proto.c
  - motion-controller-mcu/tests/test_mc_ota_and_relay.c
  project-control:
  - docs/evidence/twin/TWIN-68/**
allowed_paths:
- mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
- mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c
- project-control/docs/evidence/twin/TWIN-68/**
forbidden_paths:
- soc-ap/**
- boot/**
- test_harness/**
- mcu-p3/color-engine-mcu/**
- mcu-p3/.repo-rules/**
source_baseline:
  project-control: b764378b4d3232d1c7ce77fd4922f520dd31ef51
  soc-ap: 7184edfc796923e2f2c6e3e57ef3a9f791164b51
  mcu-p3: 3f1cfa66c6d27422cf038936b29aca7e45edb511
  test_harness: cf81195eca55bcd772ef2daa2fd4aa41634c1492
  boot/bootloadermc: faa2ed00dc9b6c8567dd44e875028f65073aab62
  boot/bootloaderth: 64b7100d3b0260ad1c24b627986475dcd45ad383
base_commit: 3f1cfa66c6d27422cf038936b29aca7e45edb511
branch: feat/soc-debug
candidate_commit: 97c1c2422e98357e72cc822d2b5293b9e0c2abc6
dispatch_binding:
  source_commit: 3f1cfa66c6d27422cf038936b29aca7e45edb511
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76
    protocol_v2_0_4: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
  revision: Rev 2.0.4
icd_versions:
- path: project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md
  version: 1
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  version: Rev 2.0.4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- mcu-p3/.repo-rules/AGENTS.md
- mcu-p3/.repo-rules/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
worktree: mcu-p3
lease:
  owner: 1e94997f-e120-4f43-b840-bceec750dc20
  task_revision: 1
  lease_id: lease-twin-68-20261107-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: mcu-p3-worktree
  location: mcu-p3
  exclusive: false
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；自检单测与注释规范检查；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - mcu-p3/motion-controller-mcu/project/src/minimc_proto.c
  - mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c
  record: docs/evidence/twin/TWIN-68/runs/author_01/result.md
rollback:
  steps:
  - git -C mcu-p3 checkout -- motion-controller-mcu/project/src/minimc_proto.c motion-controller-mcu/tests/test_mc_ota_and_relay.c
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-68
  acknowledgement: received-author_01-97c1c2422e98357e72cc822d2b5293b9e0c2abc6
verification:
  commands:
  - id: verify_mc_relay_timeout_underflow_and_wraparound
    cwd: mcu-p3
    command: sh motion-controller-mcu/tests/run_tests.sh
    expected: 全套MC回归套件、test_mc_ota_and_relay（含+1ms跨tick下溢不误超时、32位计数器回绕与正常超时测试）及S04函数行数(<=50)/入参(<=4)/中文注释检查100% PASS
    availability: available
  positive_cases:
  - minimc_proto_poll在drain_ap_rx与drain_th_rx之后采样now_ms，且check_th_relay_timeout具备32位模半空间防下溢保护（elapsed < 0x80000000UL）
  - test_th_relay_timeout_underflow_and_wraparound验证同轮发送期间SysTick推进+1ms不误触发TIMEOUT或0x07 BAD_FRAME，且跨0xFFFFFFFFU->0x00000000U回绕正常判定
  negative_cases:
  - 当now_ms < s_relay_start_ms发生负向差值下溢（如0xFFFFFFFFU）时严禁误清s_relay_pending或误退代理模式；真实流逝>=s_relay_timeout_ms时准时触发TIMEOUT
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-07T09:18:00+08:00'
---

# TWIN-68 MC级联代理check_th_relay_timeout无符号时基下溢修复与回绕单测闭环

## 1. 权威架构与协议契约依据
- **关联收件**：[`FEAT-20261106-001.yaml`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/features/FEAT-20261106-001.yaml) / `DEM-20261106-001`
- **专项架构拆解方案（`revision: 1`）**：[project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_relay_underflow_and_512b_chunk_arch_breakdown_20261107.md) (`sha256: b3c295be841195e34598f7f1eec91e6f02457ca9df0374e0147fe60be5344a76`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` 中修正 `minimc_proto_poll()` 的 `now_ms` 采样时序至 `drain_ap_rx()` / `drain_th_rx()` 之后，并在 `check_th_relay_timeout()` 中对 `proxy_elapsed` 与 `elapsed` 增加 32 位模半空间防下溢保护（`< 0x80000000UL`），根除跨毫秒发送导致的 `elapsed_ms=4294967295` 伪超时与 `BAD_FRAME 0x07`。
2. 在 `mcu-p3/motion-controller-mcu/tests/test_mc_ota_and_relay.c` 中新增 `test_th_relay_timeout_underflow_and_wraparound()`，验证同轮发送期间 `+1ms` 跨 tick 下溢不误超时、32 位计数器回绕以及正常超时释放。
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
