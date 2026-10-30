---
id: TWIN-20
title: TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现
revision: 1
plan_revision: vmware-soc-twin-20261029
task_kind: design
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 11604c2e-abcf-42d9-86f0-4978476a35d6
proposed_owner: ENG-UI
executor:
  role: ENG-UI
  agent_id: 11604c2e-abcf-42d9-86f0-4978476a35d6
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
    planned_session_alias: planned-qa-twin-20
    session: a1a21b64-b504-472a-b81c-2d39bb94df74
    session_evidence:
      path: docs/evidence/twin/TWIN-20/runs/run_01/qa_review_report.md
      sha256: 89b2a5228952839ac50b2bf0260ae6fb973f2dfbaa00034e787eb84c30a1fa55
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version:
      run: run_01
      requested_candidates:
        soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63
        project-control: 15f2d4d0158dd2c36cef2b0ebc1d45b0a5261bcc
        test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
        mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
    evidence: docs/evidence/twin/TWIN-20/runs/run_01/qa_review_report.md
    report_sha256: 89b2a5228952839ac50b2bf0260ae6fb973f2dfbaa00034e787eb84c30a1fa55
    report_review:
      session: 08b315ce-9eb5-4aaf-9a3c-1d947d6c3b4a
      role: ARCH
      decision: APPROVED
      reviewed_task_revision: 1
      artifact_version:
        run: run_01
        requested_candidates:
          soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63
          project-control: 15f2d4d0158dd2c36cef2b0ebc1d45b0a5261bcc
          test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
          mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
      evidence: docs/evidence/twin/TWIN-20/runs/run_01/arch_review_report.md
      report_sha256: 28d960a7ffbbae5aba796f7b28d722ad77e5de0dd5a92d6415d99fb843b2a8f6
      session_evidence:
        path: docs/evidence/twin/TWIN-20/runs/run_01/arch_review_report.md
        sha256: 28d960a7ffbbae5aba796f7b28d722ad77e5de0dd5a92d6415d99fb843b2a8f6
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-20
    session: 08b315ce-9eb5-4aaf-9a3c-1d947d6c3b4a
    session_evidence:
      path: docs/evidence/twin/TWIN-20/runs/run_01/arch_review_report.md
      sha256: 28d960a7ffbbae5aba796f7b28d722ad77e5de0dd5a92d6415d99fb843b2a8f6
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version:
      run: run_01
      requested_candidates:
        soc-ap: 19dd461b1959c170963ebd477aa29c36ea841f63
        project-control: 15f2d4d0158dd2c36cef2b0ebc1d45b0a5261bcc
        test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
        mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465
    evidence: docs/evidence/twin/TWIN-20/runs/run_01/arch_review_report.md
    report_sha256: 28d960a7ffbbae5aba796f7b28d722ad77e5de0dd5a92d6415d99fb843b2a8f6
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages: []
depends_on:
- TWIN-02
dependency_conditions:
- task: TWIN-02
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定双环境通信契约、HTTP-SSE接口及料槽schema
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - browser_hmi/first_release/**
  - core/net/mdns/**
  project-control:
  - docs/evidence/twin/TWIN-20/**
allowed_paths:
- soc-ap/browser_hmi/first_release/**
- soc-ap/core/net/mdns/**
- project-control/docs/evidence/twin/TWIN-20/**
source_baseline:
  project-control: a5e4b5e97439cae4a7093d1d0a29c5dc9b3c7819
  soc-ap: 4445c8fedc21bafef5e6c971fcb54cec703f0e71
  mcu-p3: 1246ea9cb441d074ea444f53320f5632fefcd503
  test_harness: 6c61ce6e51cf83d7fb58d319c23cb91bf95786cb
base_commit: 26230b355cfb116ba568c07e997f7f5dc95e86d2
candidate_commit: 19dd461b1959c170963ebd477aa29c36ea841f63
dispatch_binding:
  source_commit: 19dd461b1959c170963ebd477aa29c36ea841f63
  workspace_diff_sha256: 0000000000000000000000000000000000000000000000000000000000000000
  consumed_artifact_versions:
    TWIN-02: 532caecf3a146802969a49e73081400c2b32b25e
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
  sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  revision: 2.0.3
read_sources:
- project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
- project-control/docs/planning/product/first_release_requirements_and_task_decomposition_20261029.md
- project-control/docs/interfaces/vmware_soc_twin_architecture_icd_20261029.md
- project-control/.agents/rules/c_cpp_coding_standard.md
worktree: soc-ap
lease:
  owner: 11604c2e-abcf-42d9-86f0-4978476a35d6
  task_revision: 1
  lease_id: lease-twin-20-run-01
  expires_at: '2026-10-31T20:00:00+08:00'
resources:
- resource: isolated-worktree-and-build-output
  location: null
  exclusive: true
  pending: Ready前按实际会话登记；最多两张实现票并行
budget:
  planned_checkpoint_minutes: 30
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；接口/实现自检；准确候选独立检查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/browser_hmi/first_release/**
  - soc-ap/core/net/mdns/**
  record: docs/evidence/twin/TWIN-20/runs/run_01/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: 0f7c4684-b354-4548-ad9a-2ac9872fb4e2
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-20
  acknowledgement: docs/evidence/twin/TWIN-20/runs/run_01/result.md
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: planned_build_and_acceptance
    cwd: .
    command: Ready前由Owner绑定本票实际构建与正反例运行入口
    expected: 交付HMI料槽调色板映射、基础OOBE新机自检向导、中英多语言与明暗主题、以及mDNS局域网发现支持
    availability: planned-not-runnable
  positive_cases:
  - HMI 展示并允许确认料槽与材料映射；新机向导 (OOBE) 展示服务与固件版本及通信/温度有效性；支持中/英文与深浅主题切换；网关支持 mDNS 局域网自发现与直连
  negative_cases:
  - 未执行或无法检查项严禁伪造通过状态（必须显示“未检查/未知”）；网络断开时清晰提示断开；料槽配置与后端状态不一致时提示校验失败
required_evidence_level: document
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-29T20:30:00+08:00'
---

# TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现

## 范围与交付
交付浏览器 HMI 料槽与耗材调色板映射界面、基础新机向导 (OOBE) 检查流、多语言 (中/英) 资源与深浅主题切换组件、以及网关端 mDNS 局域网设备自发现集成。
支持用户直观交互与局域网便捷连接。

## 正反验收与边界
正例：HMI 展示并允许确认料槽与材料映射；新机向导 (OOBE) 展示服务与固件版本及通信/温度有效性；支持中/英文与深浅主题切换；网关支持 mDNS 局域网自发现与直连。
负例：未执行或无法检查项严禁伪造通过状态（必须显示“未检查/未知”）；网络断开时清晰提示断开；料槽配置与后端状态不一致时提示校验失败。
