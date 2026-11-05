---
id: TWIN-43
title: TWIN-43 AP/VMware 921600 波特率统一与全栈一键编译及配置化启动脚本
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Done
blocked: false
planning_status: closed
owner: 6e214c7d-0965-4b36-805c-41c6f83a87bc
proposed_owner: ENG-FWD
executor:
  role: ENG-FWD
  agent_id: 6e214c7d-0965-4b36-805c-41c6f83a87bc
  run_id: author_02
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-002
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "Software and POSIX PTY sandbox verification of 921600/460800/115200 baud support, invalid-baud rejection, manifest schema validation, and deploy_twin.sh full CLI/config lifecycle (--build-only, --config non-default loading and CLI override precedence, --mode sim and PTY-backed --mode hardware launch, missing-UART preflight, post-launch health-check failure cleanup, and recovery). Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-43
    session: 01a1a4ed-70d6-7862-965c-efc1a463e061
    reviewer_session: 01a1a4ed-70d6-7862-965c-efc1a463e061
    commit_sha: 426d604e9ddcfdb3e95e94ecff4f699ae976fc95
    session_evidence:
      path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-43/runs/qa_04/codex_events.jsonl
      sha256: 9221b211805bcaddbac70620312c0fde27a7b66209512edc5a4120c5dc258ddc
    decision: APPROVED
    reviewed_task_revision: 1
    artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
    report_path: /home/sushaohua/workspace/ai_soc_project/project-control/docs/evidence/twin/TWIN-43/runs/qa_04/qa_review_report.md
    evidence: docs/evidence/twin/TWIN-43/runs/qa_04/qa_review_report.md
    report_sha256: 54dd84f11ef242dd674f43d573e29fb80512c3022fa88dfc2c22194f7b883895
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-007
related_work_packages:
- TASK-004
- TASK-010
depends_on:
- TWIN-04
- TWIN-09
- TWIN-30
dependency_conditions:
- task: TWIN-04
  accepted_version: soc-ap=8f05b7396bb11fb011b0279c6a38f26a194507be; project-control=6b3556fb52002833ce57bc28ca236630bd8e9073
  acceptance_evidence: docs/evidence/twin/TWIN-04/runs/run_01/qa_review_report.md
  required: 继承TWIN-04 VMware运行时构建与services_manifest.json配置基线
- task: TWIN-09
  accepted_version: soc-ap=d214ded82447502944a41d2b27194245b0f96b19; project-control=754b188b312ac79e2873ea97075b8a2a74937ecc
  acceptance_evidence: docs/evidence/twin/TWIN-09/runs/run_01/qa_review_report.md
  required: 继承TWIN-09 ui_gateway与VMware运行时配置基线
- task: TWIN-30
  accepted_version: soc-ap=7bb05218c39d6852cac5e8d86db845dbbedd7064; project-control=f7d18c48774a8787f0dfa1d1cbe9dddea9309a40
  acceptance_evidence: docs/evidence/twin/TWIN-30/runs/run_01/qa_review_report.md
  required: 继承TWIN-30 VMware全流程闭环与串口通信基线
scope_status: mapped
allowed_repositories:
- soc-ap
- project-control
write_scope:
  soc-ap:
  - core/forward/transport/serial_posix.h
  - core/forward/transport/serial_posix.cpp
  - core/host/main.cpp
  - core/host/query.h
  - core/host/query.cpp
  - config/runtime/vmware/**
  - config/runtime/common/**
  - dist/vmware_twin/config/services_manifest.json
  - tools/deploy_twin.sh
  project-control:
  - docs/evidence/twin/TWIN-43/**
allowed_paths:
- soc-ap/core/forward/transport/serial_posix.h
- soc-ap/core/forward/transport/serial_posix.cpp
- soc-ap/core/host/main.cpp
- soc-ap/core/host/query.h
- soc-ap/core/host/query.cpp
- soc-ap/config/runtime/vmware/**
- soc-ap/config/runtime/common/**
- soc-ap/dist/vmware_twin/config/services_manifest.json
- soc-ap/tools/deploy_twin.sh
- project-control/docs/evidence/twin/TWIN-43/**
forbidden_paths:
- mcu-p3/**
- test_harness/**
- boot/**
- soc-ap/contracts/**
- soc-ap/services/**
- soc-ap/tests/**
- soc-ap/browser_hmi/**
source_baseline:
  project-control: 42b031efff970b01ee8cc8e5dd087387cdf9288f
  soc-ap: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  mcu-p3: e051111e68dd61896ed42c0961153b167b8bca41
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
branch: main
candidate_commit: 426d604e9ddcfdb3e95e94ecff4f699ae976fc95
dispatch_binding:
  source_commit: 427dd6d82caceebb7b4642e78f1dbfa96ff5fc84
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 9e66c080771a98ed2e87043c369841dcea0140f0270ae1ebab0d811c613cf5b3
    merged_summary: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
protocol_input:
  path: project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md
  sha256: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
  revision: 2
icd_versions:
- path: soc-ap/contracts/twin/services_manifest_schema.json
  version: 1.0.0
- path: project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
  version: 10
read_sources:
- project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
- project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md
- soc-ap/contracts/twin/services_manifest_schema.json
- soc-ap/core/forward/transport/serial_posix.h
- soc-ap/core/forward/transport/serial_posix.cpp
- soc-ap/services/forward/forward_main.cpp
- soc-ap/tools/deploy_twin.sh
worktree: soc-ap
lease:
  owner: 6e214c7d-0965-4b36-805c-41c6f83a87bc
  task_revision: 1
  lease_id: lease-twin-43-20261104-01
  expires_at: '2026-11-04T15:00:00+08:00'
resources:
- resource: forward-build-env
  location: soc-ap
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；组件自检；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending: []
deliverables:
  artifacts:
  - soc-ap/core/forward/transport/serial_posix.h
  - soc-ap/core/forward/transport/serial_posix.cpp
  - soc-ap/core/host/query.h
  - soc-ap/core/host/query.cpp
  - soc-ap/config/runtime/vmware/services_manifest.json
  - soc-ap/config/runtime/common/services_manifest.json
  - soc-ap/config/runtime/vmware/aisoc_twin.conf
  - soc-ap/tools/deploy_twin.sh
  record: docs/evidence/twin/TWIN-43/runs/author_02/result.md
rollback:
  steps:
  - git -C soc-ap checkout -- core/forward/transport/serial_posix.h core/forward/transport/serial_posix.cpp core/host/ config/runtime/ dist/vmware_twin/config/ tools/deploy_twin.sh
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-43
  acknowledgement: received-author_02-426d604e9ddcfdb3e95e94ecff4f699ae976fc95
verification:
  commands:
  - id: build_and_test_fullstack_921600
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin43 && mkdir -p /tmp/qa_twin43/bin && cp -r ../soc-ap ../test_harness /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build && ([ -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)) && cd /tmp/qa_twin43/soc-ap && bash tools/deploy_twin.sh --build-only && ctest --test-dir build/forward --output-on-failure && python3 ../test_harness/static_checks/cascade/run_query_cases.py --test-host build/host/soc-ap --cases ../test_harness/test_cases/cascade/query_cases.json && python3 -c "import pathlib; pathlib.Path(\"/tmp/test_serial_baud.cpp\").write_text(\"#include <cassert>\n#include <cstdio>\n#include <cstdlib>\n#include <fcntl.h>\n#include <unistd.h>\n#include \\\"serial_posix.h\\\"\n#include \\\"query.h\\\"\nint main() {\n  minimc::SerialConfig dflt;\n  assert(dflt.baud_rate == 921600U);\n  minimc::QueryOptions qdflt;\n  assert(qdflt.baud_rate == 921600U);\n  int mfd = posix_openpt(O_RDWR | O_NOCTTY);\n  assert(mfd >= 0 && grantpt(mfd) == 0 && unlockpt(mfd) == 0);\n  const char* pts = ptsname(mfd);\n  assert(pts != nullptr);\n  minimc::SerialContext ctx;\n  minimc::SerialConfig bad{pts, 123456U};\n  assert(!minimc::serial_open(&bad, &ctx) && !ctx.is_open && ctx.fd == -1);\n  const uint32_t bauds[] = {921600U, 460800U, 115200U};\n  for (uint32_t b : bauds) {\n    minimc::SerialConfig ok{pts, b};\n    assert(minimc::serial_open(&ok, &ctx) && ctx.is_open && ctx.fd >= 0);\n    minimc::serial_close(&ctx);\n    assert(!ctx.is_open && ctx.fd == -1);\n  }\n  close(mfd);\n  printf(\\\"[PASS] serial_posix baud_to_speed & serial_open positive(921600/460800/115200) and negative(123456) verified\\\\n\\\");\n  return 0;\n}\n\")" && g++ -std=c++17 -O2 -Wall -Wextra -Werror -I core/forward/transport -I core/forward/minimc -I core/host core/forward/transport/serial_posix.cpp /tmp/test_serial_baud.cpp -o /tmp/test_serial_baud && /tmp/test_serial_baud && (! ./build/host/soc-ap --port /dev/null --baud 123456 --target mc --cmd version) && echo "[PASS] parse_baud_rate rejected invalid baud 123456"'
    expected: 容器/tmp可写副本下全栈5目标编译0错误，CTest与14项cascade_query_cases（921600 PTY闭环）全部PASS，PTY实测serial_open支持921600/460800/115200并拒绝123456（fd==-1），soc-ap CLI拒绝--baud 123456
    availability: available
  - id: validate_manifest_schema
    cwd: test_harness
    command: python3 static_checks/twin/validate_schemas.py --root ..
    expected: services_manifest.json (921600) Schema校验PASS，退出码0
    availability: available
  - id: verify_deploy_twin_sim_lifecycle
    cwd: soc-ap
    command: 'mkdir -p /tmp/qa_twin43/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin43/bin/curl\"); p.write_text(\"#!/usr/bin/env python3\nimport os,sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\nif os.environ.get(\x27FORCE_CURL_FAIL\x27)==\x271\x27:\n sys.stdout.write(\x27503\x27) if w else None;sys.exit(0 if w else 22)\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status)) if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\"); p.chmod(0o755); pathlib.Path(\"/tmp/qa_twin43/custom_twin.conf\").write_text(\"AISOC_MODE=\\\"sim\\\"\nAISOC_UART_DEVICE=\\\"/dev/null\\\"\nAISOC_UART_BAUD=\\\"460800\\\"\nAISOC_HTTP_PORT=\\\"18082\\\"\nAISOC_WEB_ROOT=\\\"browser_hmi/first_release\\\"\nAISOC_LOG_DIR=\\\"/tmp/aisoc_custom_logs\\\"\nAISOC_AUTO_BUILD=\\\"0\\\"\n\")" && export PATH="/tmp/qa_twin43/bin:$PATH" && ([ -d /tmp/qa_twin43/soc-ap ] || (cp -r ../soc-ap /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build && ([ -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)))) && cd /tmp/qa_twin43/soc-ap && bash tools/deploy_twin.sh --help >/dev/null && (! bash tools/deploy_twin.sh --unknown-flag) && (! bash tools/deploy_twin.sh --mode invalid_mode) && (! bash tools/deploy_twin.sh --mode sim --port 70000) && (! bash tools/deploy_twin.sh --config /tmp/nonexistent_twin.conf) && (! bash tools/deploy_twin.sh --mode hardware --uart /dev/nonexistent_ttyUSB99 --port 18080) && (! bash tools/deploy_twin.sh --status --port 18080) && (! bash tools/deploy_twin.sh --mode sim --baud 123456 --port 18080) && (! FORCE_CURL_FAIL=1 bash tools/deploy_twin.sh --mode sim --port 18080) && (! bash tools/deploy_twin.sh --status --port 18080) && [ ! -e /tmp/aisoc_twin_logs/ui_gateway.pid ] && [ ! -e /tmp/aisoc_twin_logs/device_manager.pid ] && [ ! -e /tmp/aisoc_twin_logs/forward.pid ] && [ ! -e /tmp/aisoc_twin_logs/dbus.pid ] && [ ! -e /tmp/aisoc_twin_logs/runtime.env ] && echo "[PASS] post-launch health-check failure cleaned up all daemons and PID/runtime files" && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --status | grep -E "460800|0\.0\.0\.0:18082" && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --stop && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --baud 921600 --port 18083 && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --status | grep -E "921600|0\.0\.0\.0:18083" && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --stop && python3 -c "import os,pty,time; m,s=pty.openpty(); open(\"/tmp/qa_twin43/pty_path\",\"w\").write(os.ttyname(s)); pid=os.fork(); (open(\"/tmp/qa_twin43/pty_pid\",\"w\").write(str(pid)), os._exit(0)) if pid>0 else time.sleep(25)" && bash tools/deploy_twin.sh --mode hardware --uart "$(cat /tmp/qa_twin43/pty_path)" --baud 921600 --port 18084 && bash tools/deploy_twin.sh --status --port 18084 | grep -E "hardware|921600|0\.0\.0\.0:18084" && bash tools/deploy_twin.sh --stop --port 18084 && (kill "$(cat /tmp/qa_twin43/pty_pid)" 2>/dev/null || true) && bash tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh --status --port 18080 && bash tools/deploy_twin.sh --stop --port 18080 && bash tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh --status --port 18080 && bash tools/deploy_twin.sh --stop --port 18080 && rm -rf /tmp/qa_twin43 /tmp/aisoc_custom_logs'
    expected: --help及全部7项配置键/CLI选项100%覆盖；未知选项、非法mode/port/baud、缺失配置文件、hardware缺失串口设备及FORCE_CURL_FAIL=1启动后探活失败均以非0退出并彻底清理全部守护进程与PID/runtime.env文件；--config非默认参数(460800/18082)、CLI覆盖(921600/18083)、PTY支撑的--mode hardware(921600/18084)及连续两轮sim启停恢复闭环全部PASS
    availability: available
  positive_cases:
  - 在POSIX PTY上实测serial_posix.cpp中baud_to_speed与serial_open支持921600(B921600)、460800(B460800)与115200(B115200)
  - SerialConfig与QueryOptions默认波特率统一为921600，services_manifest.json中ap_mc_uart.baud_rate统一为921600并通过validate_schemas.py校验
  - deploy_twin.sh读取默认config/runtime/vmware/aisoc_twin.conf（全部7个配置键100%被消费，无冗余未生效配置键）与自定义--config配置文件(460800/18082)，CLI参数(--baud 921600 --port 18083)优先级高于配置文件，支持--build-only、--mode sim、基于PTY的--mode hardware、--status、--stop、--help及重复启停恢复生命周期
  negative_cases:
  - 传入非法波特率（123456）时serial_open立即返回false并拒绝打开串口（fd==-1且is_open==false），soc-ap CLI、deploy_twin.sh传入--baud 123456、非法--mode、非法--port、未知CLI选项或不存在的--config文件时均报错并以非0退出码拒绝执行
  - hardware模式下当指定AISOC_UART_DEVICE（/dev/nonexistent_ttyUSB99）不存在时以非0退出码终止且不降级启动sim进程；当守护进程启动后健康探活失败（FORCE_CURL_FAIL=1）时自动逆序停止全部已启动守护进程并清理全部PID/runtime.env文件，随后重新启动可正常恢复
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T10:40:00+08:00'
---

# TWIN-43 AP/VMware 921600 波特率统一与全栈一键编译及配置化启动脚本

## 1. 任务目标与来源
- **ARCH 拆分依据**：[debug_reconciliation_and_921600_arch_breakdown_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md) (`revision: 10`, SHA-256 `9e66c080771a98ed2e87043c369841dcea0140f0270ae1ebab0d811c613cf5b3`, ARCH Session `433026bf-a1ff-4863-8f3e-7a5f43b016ff`)
- **需求与批准绑定**：`FEAT-20261104-002` / `CONFIRM-DEBUG-BAUD-20261104` (`rev 2`) / `APPR-20261104-001` (`rev 1`)

## 2. 验收标准 (`acceptance_criteria`)
1. `soc-ap/core/forward/transport/serial_posix.h` (`SerialConfig::baud_rate = 921600`) 与 `serial_posix.cpp` (`baud_to_speed`) 支持 `460800` (`B460800`) 与 `921600` (`B921600`)，并保留 `115200` 等既有波特率兼容。
2. `soc-ap/core/host/query.h`、`soc-ap/core/host/query.cpp`、`soc-ap/core/host/main.cpp` 默认波特率统一为 `921600` 并放开 `parse_baud_rate` 对 `921600`/`460800` 的支持；`config/runtime/{vmware,common}/services_manifest.json` 与 `dist/vmware_twin/config/services_manifest.json` 中 `ap_mc_uart.baud_rate` 统一为 `921600` 并通过 `validate_schemas.py`。
3. 新增 `soc-ap/config/runtime/vmware/aisoc_twin.conf` 并升级 `soc-ap/tools/deploy_twin.sh`，实现全栈增量编译（`--build-only`）与配置驱动一键启动/状态查询/停止（`--mode sim|hardware`、`--config`、`--status`、`--stop`）。
4. 所有新增/修改 C/C++ 函数严格满足 $\le 50$ 行、$\le 4$ 个入参门禁。
