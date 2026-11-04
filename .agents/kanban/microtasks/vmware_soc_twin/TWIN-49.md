---
id: TWIN-49
title: TWIN-49 AP全栈去Mock穿透、921600波特率修复、双单播控制闭环与deploy_twin.sh加固
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 7812a1f6-5006-4971-a954-802f855cf20a
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: 7812a1f6-5006-4971-a954-802f855cf20a
  run_id: author_04
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-002
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "Software and POSIX PTY sandbox verification of soc-ap forward_uart.cpp B921600 fix, unified opcodes (0x10..0x1C with 0x15 TEMP_REPORT, 0x17 MOTION_STOP, 0x18 1B probe_idx=7, 0x19 unified slot/filament), sequential dual-unicast (MC 0x02 then TH 0x03 all-ACK gate), complete removal of ui_gateway_job_ctrl.cpp in-memory mocks/DEFAULT_MESH/open-loop timer, and deploy_twin.sh + third_party/build.sh automatic third-party build and pre-deploy purge. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable in qa-sandbox:20261029: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-49
    session: 01a1a6c4-7035-7213-8292-e56b4df57c47
    reviewer_session: 01a1a6c4-7035-7213-8292-e56b4df57c47
    commit_sha: 333178c66280e785ae1a5c089a6e2a05075cc926
    session_evidence:
      path: project-control/docs/evidence/twin/TWIN-49/runs/qa_04/codex_events.jsonl
      sha256: f8b89f993d4893dac3217a92811e10d713976aaf7fbb039520a22f5a97a2d56b
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
    report_path: docs/evidence/twin/TWIN-49/runs/qa_04/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-49/runs/qa_04/qa_review_report.md
    report_sha256: 5a5a8476fdaa16e3108f688c7685c58c79de459e57d07cec15d8eb62acdbbd5f
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
related_work_packages:
- TASK-008
- TASK-009
- TASK-010
depends_on:
- TWIN-43
- TWIN-47
- TWIN-48
dependency_conditions:
- task: TWIN-43
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-43/runs/qa_04/qa_review_report.md
  required: 继承TWIN-43 soc-ap 921600配置与deploy_twin.sh脚本基线
- task: TWIN-47
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=d86041814689b2f353d6fe0b372d31689b826a98; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-47/runs/qa_03/qa_review_report.md
  required: 绑定TWIN-47 MC端MiniMCProto V2控制命令与载荷契约
- task: TWIN-48
  accepted_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79; soc-ap=c2c5a228c81488bca2178488a4e8a109b0472d72; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3; test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
  acceptance_evidence: docs/evidence/twin/TWIN-48/runs/qa_01/qa_review_report.md
  required: 绑定TWIN-48 TH端MiniMCProto V2级联控制与0x1C载荷契约
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - contracts/twin/telemetry_types.h
  - services/forward/forward_types.h
  - services/forward/forward_uart.cpp
  - services/forward/forward_protocol.h
  - services/forward/forward_protocol.cpp
  - services/forward/forward_service.h
  - services/forward/forward_service.cpp
  - services/forward/forward_dbus.cpp
  - services/device_manager/device_manager_types.h
  - services/device_manager/device_manager_state.h
  - services/device_manager/device_manager_state.cpp
  - services/device_manager/device_manager_service.h
  - services/device_manager/device_manager_service.cpp
  - services/device_manager/device_manager_dbus.cpp
  - services/ui_gateway/ui_gateway_dbus.h
  - services/ui_gateway/ui_gateway_dbus.cpp
  - services/ui_gateway/ui_gateway_job_ctrl.h
  - services/ui_gateway/ui_gateway_job_ctrl.cpp
  - services/ui_gateway/ui_gateway_server.cpp
  - tools/deploy_twin.sh
  - third_party/build.sh
  - services/forward/CMakeLists.txt
  - services/device_manager/CMakeLists.txt
  - services/ui_gateway/CMakeLists.txt
  - tests/forward/twin/CMakeLists.txt
  - tests/forward/twin/test_forward_protocol.cpp
  - tests/forward/twin/test_forward_service.cpp
  - tests/device_manager/twin/test_device_manager_state.cpp
  - tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  project-control:
  - docs/evidence/twin/TWIN-49/**
allowed_paths:
- soc-ap/contracts/twin/telemetry_types.h
- soc-ap/services/forward/forward_types.h
- soc-ap/services/forward/forward_uart.cpp
- soc-ap/services/forward/forward_protocol.h
- soc-ap/services/forward/forward_protocol.cpp
- soc-ap/services/forward/forward_service.h
- soc-ap/services/forward/forward_service.cpp
- soc-ap/services/forward/forward_dbus.cpp
- soc-ap/services/device_manager/device_manager_types.h
- soc-ap/services/device_manager/device_manager_state.h
- soc-ap/services/device_manager/device_manager_state.cpp
- soc-ap/services/device_manager/device_manager_service.h
- soc-ap/services/device_manager/device_manager_service.cpp
- soc-ap/services/device_manager/device_manager_dbus.cpp
- soc-ap/services/ui_gateway/ui_gateway_dbus.h
- soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
- soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
- soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
- soc-ap/services/ui_gateway/ui_gateway_server.cpp
- soc-ap/tools/deploy_twin.sh
- soc-ap/third_party/build.sh
- soc-ap/services/forward/CMakeLists.txt
- soc-ap/services/device_manager/CMakeLists.txt
- soc-ap/services/ui_gateway/CMakeLists.txt
- soc-ap/tests/forward/twin/CMakeLists.txt
- soc-ap/tests/forward/twin/test_forward_protocol.cpp
- soc-ap/tests/forward/twin/test_forward_service.cpp
- soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
- soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
- project-control/docs/evidence/twin/TWIN-49/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
source_baseline:
  project-control: 17e0887da07ceb3b017623b791b6a6999e837c79
  soc-ap: c2c5a228c81488bca2178488a4e8a109b0472d72
  mcu-p3: 016e1236af75f6f19282d6b000f4b1b68bd96cc3
  test_harness: 30c21f74e74179994eb475c38cc4afc2c1427a26
base_commit: c2c5a228c81488bca2178488a4e8a109b0472d72
branch: main
candidate_commit: 333178c66280e785ae1a5c089a6e2a05075cc926
dispatch_binding:
  source_commit: c2c5a228c81488bca2178488a4e8a109b0472d72
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
- soc-ap/AGENTS.md
- soc-ap/.agents/rules/shared/SOURCE.json
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md
worktree: soc-ap
lease:
  owner: 7812a1f6-5006-4971-a954-802f855cf20a
  task_revision: 1
  lease_id: lease-twin-49-20261104-01
  expires_at: '2026-11-04T21:00:00+08:00'
resources:
- resource: forward-build-env
  location: soc-ap
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；CTest与deploy_twin.sh自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/contracts/twin/telemetry_types.h
  - soc-ap/services/device_manager/CMakeLists.txt
  - soc-ap/services/device_manager/device_manager_dbus.cpp
  - soc-ap/services/device_manager/device_manager_service.cpp
  - soc-ap/services/device_manager/device_manager_service.h
  - soc-ap/services/device_manager/device_manager_types.h
  - soc-ap/services/forward/forward_dbus.cpp
  - soc-ap/services/forward/forward_protocol.cpp
  - soc-ap/services/forward/forward_protocol.h
  - soc-ap/services/forward/forward_service.cpp
  - soc-ap/services/forward/forward_service.h
  - soc-ap/services/forward/forward_types.h
  - soc-ap/services/forward/forward_uart.cpp
  - soc-ap/services/ui_gateway/CMakeLists.txt
  - soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  - soc-ap/services/ui_gateway/ui_gateway_dbus.h
  - soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  - soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  - soc-ap/services/ui_gateway/ui_gateway_server.cpp
  - soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
  - soc-ap/tests/forward/twin/CMakeLists.txt
  - soc-ap/tests/forward/twin/test_forward_protocol.cpp
  - soc-ap/tests/forward/twin/test_forward_service.cpp
  - soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  - soc-ap/third_party/build.sh
  - soc-ap/tools/deploy_twin.sh
  record: docs/evidence/twin/TWIN-49/runs/author_04/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- contracts/ services/ tests/ tools/ third_party/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-49
  acknowledgement: received-author_04-333178c66280e785ae1a5c089a6e2a05075cc926
verification:
  commands:
  - id: build_and_test_soc_ap_e2e_control
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin49 && mkdir -p /tmp/qa_twin49/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin49/bin/curl\"); p.write_text(\"#!/usr/bin/env python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status)) if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\"); p.chmod(0o755)" && export PATH="/tmp/qa_twin49/bin:$PATH" && cp -r ../soc-ap /tmp/qa_twin49/ && rm -rf /tmp/qa_twin49/soc-ap/build && ([ -e /tmp/qa_twin49/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin49/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin49/soc-ap/third_party/install)) && cd /tmp/qa_twin49/soc-ap && bash tools/deploy_twin.sh --build-only && ctest --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager --output-on-failure && ctest --test-dir build/ui_gateway --output-on-failure && mkdir -p dist/vmware_twin/logs dist/vmware_twin/run && echo stale > dist/vmware_twin/logs/stale.log && echo cache > dist/vmware_twin/run/stale.cache && touch /tmp/qa_twin49/dummy_uart && python3 -c "import socket,time,os; s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind((\"127.0.0.1\",18089)); s.listen(1); pid=os.fork(); (open(\"/tmp/qa_twin49/port_holder_pid\",\"w\").write(str(pid)) if pid>0 else time.sleep(60))" && python3 -c "import time,os; f=open(\"/tmp/qa_twin49/dummy_uart\",\"r+\"); pid=os.fork(); (open(\"/tmp/qa_twin49/uart_holder_pid\",\"w\").write(str(pid)) if pid>0 else time.sleep(60))" debug_reconciliation_probe live_pty_ctl && PORT_PID=$(cat /tmp/qa_twin49/port_holder_pid) && UART_PID=$(cat /tmp/qa_twin49/uart_holder_pid) && grep -q "^State:.*[RS]" "/proc/$PORT_PID/status" && grep -q "^State:.*[RS]" "/proc/$UART_PID/status" && bash tools/deploy_twin.sh --mode sim --port 18089 --uart /tmp/qa_twin49/dummy_uart && ([ ! -d "/proc/$PORT_PID" ] || grep -q "^State:.*Z" "/proc/$PORT_PID/status") && ([ ! -d "/proc/$UART_PID" ] || grep -q "^State:.*Z" "/proc/$UART_PID/status") && test ! -e dist/vmware_twin/logs/stale.log && test ! -e dist/vmware_twin/run/stale.cache && bash tools/deploy_twin.sh --stop --port 18089 && rm -rf /tmp/qa_twin49'
    expected: 容器/tmp可写副本下deploy_twin.sh自动检测third_party并完成全栈编译，forward/device_manager/ui_gateway三套CTest单测（含B921600映射、0x10..0x1C组解帧、双单播全ACK闭环、去Mock网关路由与超时/离线503/504拦截）100% PASS，且deploy_twin.sh部署前自动清理占用配置端口/UART的遗留进程、旧缓存与旧日志验证通过
    availability: available
  positive_cases:
  - forward_uart.cpp正确支持B921600/B460800且默认921600；forward_protocol与forward_service支持0x10..0x1C全控制命令及先MC(0x02)后TH(0x03)串行双单播全ACK闭环
  - ui_gateway_job_ctrl.cpp与ui_gateway_server.cpp彻底移除本地内存假回零、DEFAULT_MESH假网格及1000ms开环进度定时器，全部控制路由经D-Bus穿透至forward_service
  - deploy_twin.sh与third_party/build.sh支持自动构建第三方库及部署前彻底清理旧进程、旧端口/串口占用、旧缓存与旧日志
  negative_cases:
  - 当MCU离线或任一节点(MC或TH)超时/返回NACK时，控制接口拒绝伪造成功状态，立即返回HTTP 503/504并在打印态挂起为PAUSED
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T17:45:00+08:00'
---

# TWIN-49 AP全栈去Mock穿透、921600波特率修复、双单播控制闭环与deploy_twin.sh加固

## 1. 任务目标与来源
- **ARCH 方案依据**：[end_to_end_physical_link_remediation_plan_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/planning/end_to_end_physical_link_remediation_plan_20261104.md) (`revision: 3`, SHA-256 `21dd6cc16b9eb7d643662b6fba681e6360f4dcd98cdece55439c6f759c5b22cc`)
- **执行模式**：单工程 Agent（`7812a1f6-5006-4971-a954-802f855cf20a`）顺序垂直贯穿阶段 3/4。

## 2. 验收标准 (`acceptance_criteria`)
1. 修复 `forward_uart.cpp` `B921600` 降级 Bug；统一 `0x10`~`0x1C` 协议帧；实现先 `MC (0x02)` 后 `TH (0x03)` 的双单播全 ACK 闭环。
2. 彻底删除 `ui_gateway_job_ctrl.cpp` 本地内存假回零、`DEFAULT_MESH` 与 `1000ms` 开环定时器，打通 `ui_gateway ➔ device_manager ➔ forward_service` D-Bus 控制全链路。
3. 修复 `deploy_twin.sh` 与 `third_party/build.sh`，实现第三方库自动构建与重部署前全量清场。
