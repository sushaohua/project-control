---
id: TWIN-20
title: TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现（含真实双MCU固件版本呈现）
revision: 2
plan_revision: vmware-soc-twin-20261029
task_kind: design
development_stage: vmware-twin
dispatchable: true
status: InProgress
blocked: false
planning_status: planned
owner: session-eng-ui-twin-20
proposed_owner: ENG-UI
executor:
  role: ENG-UI
  agent_id: session-eng-ui-twin-20
  run_id: run_02
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
    planned_session_alias: planned-qa-twin-20-run02
    session: session-qa-twin-20
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  - role: ARCH
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-arch-twin-20-run02
    session: session-arch-twin-20
    session_evidence: null
    decision: null
    reviewed_task_revision: null
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages: []
depends_on:
- TWIN-02
- TWIN-29
dependency_conditions:
- task: TWIN-02
  accepted_version: 532caecf3a146802969a49e73081400c2b32b25e
  acceptance_evidence: docs/evidence/twin/TWIN-02/runs/run_03/result.md
  required: 开工前绑定双环境通信契约、HTTP-SSE接口及料槽schema
- task: TWIN-29
  accepted_version: soc-ap=86f5e17ead0971ca1a1eb20c07ca345924e24454
  acceptance_evidence: docs/evidence/twin/TWIN-29/runs/run_02/qa_review_report.md
  required: 继承TWIN-29双MCU版本查询链路与devices.mc/devices.th拓扑遥测
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
  project-control: 9e3e558e6587c4f420e5015b60098df68903c72b
  soc-ap: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  mcu-p3: 04231388c842c1ce3e5b71675d0dc118a65edf2e
  test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5
base_commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
candidate_commit: cb70d59e949396f45aec94d33ae23cab75beb282
dispatch_binding:
  source_commit: 86f5e17ead0971ca1a1eb20c07ca345924e24454
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    TWIN-02: 532caecf3a146802969a49e73081400c2b32b25e
    TWIN-29: 86f5e17ead0971ca1a1eb20c07ca345924e24454
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
  owner: session-eng-ui-twin-20
  task_revision: 2
  lease_id: lease-twin-20-run-02
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
  record: docs/evidence/twin/TWIN-20/runs/run_02/result.md
rollback:
  steps:
  - 仅回退本票候选；保存失败证据和原状态；硬件恢复须按实际SOP及授权执行
handoff:
  receiver_role: COORD
  receiver_session: session-coord-main
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-20
  acknowledgement: docs/evidence/twin/TWIN-20/runs/run_02/result.md
verification:
  commands:
  - id: check_graph
    cwd: .
    command: PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
    expected: 结构无错误；不等于任务/运行/硬件接受
    availability: local
  - id: test_hmi_contract
    cwd: .
    command: python3 soc-ap/browser_hmi/first_release/test_hmi_contract.py
    expected: exit 0, HMI契约及真实版本展示断言全通
    availability: host-toolchain
  - id: test_mdns_c11
    cwd: .
    command: gcc -Wall -Wextra -Werror -pedantic -std=c11 -I soc-ap/core/net/mdns soc-ap/core/net/mdns/mdns_advertiser.c soc-ap/core/net/mdns/test_mdns_advertiser.c -o /tmp/test_mdns && /tmp/test_mdns
    expected: exit 0, mDNS 4/4测试通过
    availability: host-toolchain
  - id: test_mdns_cxx17
    cwd: .
    command: g++ -Wall -Wextra -Werror -pedantic -std=c++17 -fno-exceptions -fno-rtti -I soc-ap/core/net/mdns soc-ap/core/net/mdns/mdns_advertiser.c soc-ap/core/net/mdns/test_mdns_advertiser.c -o /tmp/test_mdns_cxx && /tmp/test_mdns_cxx
    expected: exit 0, mDNS C++17 4/4测试通过
    availability: host-toolchain
  positive_cases:
  - HMI 展示料槽与材料映射；新机向导 (OOBE) Step 3 展示真实双 MCU 固件版本号与通信自检状态；主界面 Sensors 标签页下分别展示真实 MC 与 TH 固件版本号；支持中/英文与深浅主题切换；网关支持 mDNS 局域网自发现与直连
  negative_cases:
  - 设备离线 (OFFLINE)、查询失败 (QUERY_FAILED)、采样超时/过期 (STALE) 或未连接 (UNKNOWN) 时，严格按防御状态机显示对应未知/离线/查询失败/过期提示，绝不以硬编码、假数据或伪造版本显示
required_evidence_level: software-verified
verification_environment: isolated-host-or-document
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-10-31T14:36:00+08:00'
---

# TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现（含真实双MCU固件版本呈现）

## 范围与交付
1. 交付浏览器 HMI 料槽与耗材调色板映射界面、基础新机向导 (OOBE) 检查流、多语言 (中/英) 资源与深浅主题切换组件、以及网关端 mDNS 局域网设备自发现集成。
2. 依据用户高优先级指令，接入后端真实双 MCU (MC 与 TH) 固件版本与状态拓扑（消费 TWIN-29 提供的 `devices.mc` 与 `devices.th`），在主界面 Sensors 卡片及 OOBE Step 3 中分别展示真实固件版本号（`v{major}.{minor} (0x{git_commit})`）。
3. 严格遵循真实性防御原则：在设备离线、查询失败、数据过期或未就绪时，界面分别明确指示“未知”、“离线”、“查询失败”、“数据已过期”，严禁以硬编码、假数据或伪造响应展示。版本信息须可用于后续核对固件升级前后的实际版本。

## 正反验收与边界
正例：HMI 展示并允许确认料槽与材料映射；新机向导 (OOBE) 展示真实双 MCU 固件版本与通信/温度自检状态；Sensors 标签页分别呈现真实 MC/TH 固件版本；支持中/英文与深浅主题切换；网关支持 mDNS 局域网自发现与直连。
负例：未执行、无法检查或断开项严禁伪造通过状态（必须显示“未知/离线/查询失败/过期”）；网络断开时清晰提示断开；料槽配置与后端状态不一致时提示校验失败。
