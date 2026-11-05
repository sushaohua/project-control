---
id: TWIN-50
title: TWIN-50 测试夹具去旁路净化、全栈921600垂直端到端PTY预检与真机HIL终验
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: integration
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
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "Software, static opcode alignment (check_opcode_alignment.py), and 921600 PTY virtual-MCU hardware-mode full-stack vertical-slice integration verification of debug_reconciliation_probe.py after completely removing twin46_mc_bridge.c normalize_ap_temp_wire_frame and ctypes notify bypasses, driving 100% via ui-gateway HTTP control APIs across the 5 business categories (temperature, motion/homing/stop, 5x5 bed-leveling grid, filament/slot, job/G-code), unit-specific offline sentinel (2147483646 mdeg / 32767 ddC) and strict HTTP 503 lock checks, live negative fault injection and live recovery loop against the running ui-gateway, and deploy_twin.sh lifecycle. Cross-compiler ELF build and physical MCU SWD/USB/UART HIL are not applicable in qa-sandbox:20261029: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-50
    session: 01a1a6f3-2867-7ce0-9e0d-6ddcd2830e13
    reviewer_session: 01a1a6f3-2867-7ce0-9e0d-6ddcd2830e13
    commit_sha: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-50/runs/qa_03/codex_events.jsonl
      sha256: 7e0200814954f381f706e489c8d01089655363b65e7c2575a2cd4a1969b4a241
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-50/runs/qa_03/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-50/runs/qa_03/qa_review_report.md
    report_sha256: b41de0120d053704eb2924d2cf39924fca3c0f92e1030a3f34e4e5d9095fd791
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-002
- TASK-007
- TASK-009
depends_on:
- TWIN-47
- TWIN-48
- TWIN-49
dependency_conditions:
- task: TWIN-47
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
  required: 消费TWIN-47 MC控制命令闭环与真机交叉编译固件
- task: TWIN-48
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-48/runs/qa_01/qa_review_report.md
  required: 消费TWIN-48 TH级联控制闭环与真机交叉编译固件
- task: TWIN-49
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-49/runs/qa_04/qa_review_report.md
  required: 消费TWIN-49 AP去Mock全链路控制与deploy_twin.sh脚本
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - hil/tools/debug_reconciliation_probe.py
  - test_cases/twin/twin46_mc_bridge.c
  - test_cases/twin/twin46_th_bridge.c
  - static_checks/minimcproto/check_opcode_alignment.py
  project-control:
  - docs/evidence/twin/TWIN-50/**
  - docs/evidence/hil/**
allowed_paths:
- test_harness/hil/tools/debug_reconciliation_probe.py
- test_harness/test_cases/twin/twin46_mc_bridge.c
- test_harness/test_cases/twin/twin46_th_bridge.c
- test_harness/static_checks/minimcproto/check_opcode_alignment.py
- project-control/docs/evidence/twin/TWIN-50/**
- project-control/docs/evidence/hil/**
forbidden_paths:
- mcu-p3/**
- soc-ap/**
- boot/**
source_baseline:
  project-control: 17e0887da07ceb3b017623b791b6a6999e837c79
  soc-ap: 333178c66280e785ae1a5c089a6e2a05075cc926
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: 30c21f74e74179994eb475c38cc4afc2c1427a26
base_commit: 30c21f74e74179994eb475c38cc4afc2c1427a26
branch: main
candidate_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
dispatch_binding:
  source_commit: 30c21f74e74179994eb475c38cc4afc2c1427a26
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    remediation_plan: 21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc
protocol_input:
  path: project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
  sha256: 21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc
  revision: 3
icd_versions:
- path: project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
  version: 3
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- test_harness/AGENTS.md
- test_harness/.agents/rules/shared/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
worktree: test_harness
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-50-20261104-01
  expires_at: '2026-11-04T21:00:00+08:00'
resources:
- resource: integrator-twin-env
  location: test_harness
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；去旁路PTY垂直回归；真机SWD烧录与4路串口HIL终验；独立QA审计；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - test_harness/hil/tools/debug_reconciliation_probe.py
  - test_harness/test_cases/twin/twin46_mc_bridge.c
  - test_harness/test_cases/twin/twin46_th_bridge.c
  - test_harness/static_checks/minimcproto/check_opcode_alignment.py
  record: docs/evidence/twin/TWIN-50/runs/author_02/result.md
rollback:
  steps:
  - git -C test_harness checkout -- hil/tools/ test_cases/twin/ static_checks/minimcproto/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-50
  acknowledgement: received-author_02-d14ed04321c6d4f5ddb35a8801604a8af53b5b60
verification:
  commands:
  - id: verify_opcode_alignment_and_probe_selftest
    cwd: test_harness
    command: (! grep -rnE "normalize_ap_temp_wire_frame|mc_bridge_notify_|th_bridge_notify_" test_cases/twin/ hil/tools/debug_reconciliation_probe.py) && python3 static_checks/minimcproto/check_opcode_alignment.py && python3 hil/tools/debug_reconciliation_probe.py --help >/dev/null && python3 hil/tools/debug_reconciliation_probe.py --self-test --matrix-out /tmp/qa_twin50_selftest.md && test -s /tmp/qa_twin50_selftest.md && rm -f /tmp/qa_twin50_selftest.md
    expected: 零旁路残留检查PASS，跨仓17个命令码静态对齐检查PASS，debug_reconciliation_probe.py自检PASS
    availability: available
  - id: verify_vertical_slice_e2e_pty_no_bypass
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin50 && mkdir -p /tmp/qa_twin50/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin50/bin/curl\"); p.write_text(\"#!/usr/bin/env python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status)) if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\"); p.chmod(0o755)" && export PATH="/tmp/qa_twin50/bin:$PATH" && cp -r ../soc-ap ../mcu-p3 ../test_harness /tmp/qa_twin50/ && rm -rf /tmp/qa_twin50/soc-ap/build && ([ -e /tmp/qa_twin50/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin50/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin50/soc-ap/third_party/install)) && cd /tmp/qa_twin50/soc-ap && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"start-pty\", \"/tmp/qa_twin50\"))" && bash tools/deploy_twin.sh --mode hardware --uart "$(cat /tmp/qa_twin50/pty_path)" --baud 921600 --port 18086 && bash tools/deploy_twin.sh --status --port 18086 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-online\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/live_ok_matrix.md && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-mismatch\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"restore-mismatch\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-crc-err\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-drop\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-offline\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/live_offline_matrix.md && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-recovery\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/reconciliation_matrix.md && test -s /tmp/qa_twin50/live_ok_matrix.md && test -s /tmp/qa_twin50/live_offline_matrix.md && test -s /tmp/qa_twin50/reconciliation_matrix.md && bash tools/deploy_twin.sh --stop --port 18086 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"stop-pty\", \"/tmp/qa_twin50\"))" && rm -rf /tmp/qa_twin50'
    expected: 彻底删除normalize_ap_temp_wire_frame与ctypes旁路notify后，100%由HTTP控制API触发D-Bus与921600串口帧驱动C固件完成五类业务正向对账、运行态数值失配/坏CRC帧/环形缓冲丢包(drop>0)注入非0退出拦截、断连OFFLINE哨兵(2147483646/32767)与HTTP 503锁定、重连恢复对账全部PASS
    availability: available
  positive_cases:
  - 彻底删除twin46_mc_bridge.c中的normalize_ap_temp_wire_frame帧篡改与debug_reconciliation_probe.py中的ctypes旁路notify调用，100%通过ui-gateway HTTP API驱动921600串口协议帧产生[MC-DBG]与[TH-DBG]日志完成五类业务双向对账
  - check_opcode_alignment.py静态核验soc-ap与mcu-p3(MC/TH)全量17个MiniMCProto V2命令码100%对齐，deploy_twin.sh在921600 POSIX PTY下完成在线五类对账、故障注入、离线哨兵与恢复闭环（注：交叉编译器ELF构建与物理MCU USB/UART/SWD HIL在qa-sandbox:20261029纯软件容器中为not applicable，见accepted_scope）
  negative_cases:
  - 运行态注入数值失配(inject-mismatch)、CRC错误(inject-crc-err)、环形缓冲丢包(inject-drop)时，debug_reconciliation_probe.py返回非0退出码拦截
  - 运行态串口/传感器断连进入OFFLINE时，按单位严格校验2147483646 mdeg与32767 ddC哨兵值及HTTP 503控制锁定，恢复ONLINE后重新对账返回0
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T17:45:00+08:00'
---

# TWIN-50 测试夹具去旁路净化、全栈921600垂直端到端PTY预检与真机HIL终验

## 1. 任务目标与来源
- **ARCH 方案依据**：[end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **执行模式**：单工程 Agent（`7812a1f6-5006-4971-a954-802f855cf20a`）顺序垂直贯穿阶段 4/4。

## 2. 验收标准 (`acceptance_criteria`)
1. 删除 `twin46_mc_bridge.c:normalize_ap_temp_wire_frame()` 与 `debug_reconciliation_probe.py` 旁路 `ctypes` `notify` 调用，100% 依靠 HTTP 控制接口 ➔ D-Bus ➔ 921600 串口帧驱动 C 固件完成五类业务闭环对账、运行态负向故障注入拦截（数值失配、CRC错误、环形缓冲丢包）、离线哨兵（`2147483646`/`32767` + HTTP 503 锁定）及重连恢复对账。
2. 在受控 Docker 沙箱（`qa-sandbox:20261029`）中完成跨仓 17 个命令码静态对齐检查与 921600 POSIX PTY 零旁路全栈闭环验证（注：交叉编译器 ELF 构建与物理板卡 SWD/USB/UART HIL 在 `qa-sandbox:20261029` 纯软件沙箱中为 `not applicable`，详见 `accepted_scope`）。
