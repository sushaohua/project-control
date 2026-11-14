---
id: TWIN-46
title: TWIN-46 921600全栈配置化启动与MC/TH Debug↔Web UI双向链路对账集成验证
revision: 1
plan_revision: vmware-soc-twin-20261104
task_kind: integration
development_stage: vmware-twin
dispatchable: true
status: Backlog
blocked: false
planning_status: planned
owner: null
proposed_owner: INTEGRATOR
executor:
  role: INTEGRATOR
  agent_id: null
  run_id: null
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
feature_id: FEAT-20261104-001
confirmation_id: CONFIRM-DEBUG-BAUD-20261104
approval_id: APPR-20261104-001
accepted_scope: "Software, sim-mode lifecycle, and 921600 PTY virtual-MCU hardware-mode full-stack integration verification of debug_reconciliation_probe.py across the 5 telemetry/control categories (temperature, motion/homing, 5x5 bed-leveling grid, filament/slot, job state), unit-specific offline sentinel (2147483646 mdeg / 32767 ddC) and strict HTTP 503 lock checks, live negative fault injection and live recovery loop against the running ui-gateway, and deploy_twin.sh lifecycle. Cross-compiler ELF build and physical MCU USB/UART HIL are not applicable: qa-sandbox:20261029 provides host GCC/Python only and no physical MCU hardware; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-46
    session: pending-codex-qa-twin-46
    session_evidence: null
    decision: PENDING
    reviewed_task_revision: 1
    artifact_version: null
    evidence: null
    report_sha256: null
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-010
related_work_packages:
- TASK-002
- TASK-007
- TASK-009
depends_on:
- TWIN-43
- TWIN-44
- TWIN-45
- TWIN-50
dependency_conditions:
- task: TWIN-43
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-43/runs/qa_04/qa_review_report.md
  required: 消费TWIN-43 AP/VMware 921600串口支持与deploy_twin.sh全栈一键编译及配置化启动脚本
- task: TWIN-44
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=f34a4b9d3ce03ec02824e1c54dd4dd3052386156; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-44/runs/qa_06/qa_review_report.md
  required: 消费TWIN-44 MC固件USART2 921600与USART1非阻塞[MC-DBG]日志固件产物
- task: TWIN-45
  accepted_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f; soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f; test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  acceptance_evidence: docs/evidence/twin/TWIN-45/runs/qa_01/qa_review_report.md
  required: 消费TWIN-45 TH固件USART3非阻塞[TH-DBG]日志固件产物
- task: TWIN-50
  accepted_version: pending
  acceptance_evidence: docs/evidence/twin/TWIN-50/runs/qa_01/qa_review_report.md
  required: 消费TWIN-50全链路去Mock与真实端到端闭环修复基线
scope_status: mapped
allowed_repositories:
- test_harness
- project-control
write_scope:
  test_harness:
  - hil/tools/debug_reconciliation_probe.py
  - static_checks/twin/**
  - test_cases/twin/**
  project-control:
  - docs/evidence/twin/TWIN-46/**
allowed_paths:
- test_harness/hil/tools/debug_reconciliation_probe.py
- test_harness/static_checks/twin/**
- test_harness/test_cases/twin/**
- project-control/docs/evidence/twin/TWIN-46/**
forbidden_paths:
- mcu-p3/**
- boot/**
- soc-ap/**
source_baseline:
  project-control: 42b031efff970b01ee8cc8e5dd087387cdf9288f
  soc-ap: 426d604e9ddcfdb3e95e94ecff4f699ae976fc95
  mcu-p3: 29d62ef1bb7cf33e334f7e58aae81717cd26c54f
  test_harness: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
base_commit: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
branch: main
candidate_commit: 91942286e8f686ce044a6aa8fdb11270ff8f5624
dispatch_binding:
  source_commit: ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    arch_breakdown: 30a4d3a26878cdf1527f9a59524a93157f0e11dae4776c40342dadfb871745cb
    merged_summary: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
protocol_input:
  path: project-control/docs/planning/debug_and_921600_merged_implementation_summary_20261104.md
  sha256: c469fcd058b8607f454d661a69c07bf8a483e5763d9d231a574d71ee14cd69ec
  revision: 2
icd_versions:
- path: project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
  version: 14
read_sources:
- project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md
- project-control/docs/planning/mc_th_debug_mode_requirement_confirmation_20261103.md
- project-control/docs/planning/vmware_mc_921600_requirement_confirmation_20261103.md
- soc-ap/tools/deploy_twin.sh
- soc-ap/config/runtime/vmware/services_manifest.json
worktree: test_harness
lease: null
resources:
- resource: integrator-twin-env
  location: test_harness
  exclusive: true
  pending: null
budget:
  planned_checkpoint_minutes: 60
  max_evidence_based_corrections: 2
  on_limit: 保存证据交COORD
checkpoint: 开工前绑定；对账工具自检与全栈集成验证；独立沙箱与QA审查；收件
execution_contract: project-control/docs/planning/vmware_soc_twin_task_execution_20261029.md
readiness_pending:
- TWIN-50
deliverables:
  artifacts:
  - test_harness/hil/tools/debug_reconciliation_probe.py
  - test_harness/test_cases/twin/twin46_mc_bridge.c
  - test_harness/test_cases/twin/twin46_th_bridge.c
  record: docs/evidence/twin/TWIN-46/runs/author_03/result.md
rollback:
  steps:
  - git -C test_harness checkout -- hil/tools/ static_checks/twin/ test_cases/twin/
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-46
  acknowledgement: received-author_02-91942286e8f686ce044a6aa8fdb11270ff8f5624
verification:
  commands:
  - id: run_debug_reconciliation_probe_selftest
    cwd: test_harness
    command: python3 hil/tools/debug_reconciliation_probe.py --help >/dev/null && python3 hil/tools/debug_reconciliation_probe.py --self-test --matrix-out /tmp/qa_twin46_fixtures/selftest_matrix.md && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json --matrix-out /tmp/qa_twin46_fixtures/cli_ok_matrix.md && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_mismatch.json) && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_crc_err.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json) && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_drop.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json) && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_bad_grid.json) && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_offline.json) && (! python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_offline.log --th-log /tmp/qa_twin46_fixtures/th_offline.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_bad_offline.json) && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_offline.log --th-log /tmp/qa_twin46_fixtures/th_offline.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_offline.json --matrix-out /tmp/qa_twin46_fixtures/cli_offline_matrix.md && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json --matrix-out /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && test -s /tmp/qa_twin46_fixtures/selftest_matrix.md && test -s /tmp/qa_twin46_fixtures/cli_ok_matrix.md && test -s /tmp/qa_twin46_fixtures/cli_offline_matrix.md && test -s /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && rm -rf /tmp/qa_twin46_fixtures
    expected: --help、--self-test及--mc-log/--th-log/--ap-snapshot/--matrix-out CLI全路径校验（覆盖温度、归零/运动、二维5x5调平网格、进退丝/料槽、打印作业状态五类正向对账，数值失配/CRC_ERR/drop>0/1x25畸形网格/错误单位离线哨兵或非503状态码非0退出拦截，按单位严格校验OFFLINE哨兵值2147483646 mdeg与32767 ddC及HTTP 503控制锁对账，以及故障后恢复对账）并导出非空reconciliation_matrix.md全部PASS
    availability: available
  - id: verify_fullstack_deploy_and_reconciliation
    cwd: soc-ap
    command: 'rm -rf /tmp/qa_twin46 && mkdir -p /tmp/qa_twin46/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin46/bin/curl\"); p.write_text(\"#!/usr/bin/env python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status)) if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\"); p.chmod(0o755)" && export PATH="/tmp/qa_twin46/bin:$PATH" && cp -r ../soc-ap ../mcu-p3 ../test_harness /tmp/qa_twin46/ && rm -rf /tmp/qa_twin46/soc-ap/build && ([ -e /tmp/qa_twin46/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin46/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin46/soc-ap/third_party/install)) && cd /tmp/qa_twin46/soc-ap && bash tools/deploy_twin.sh --mode sim --port 18085 && bash tools/deploy_twin.sh --status --port 18085 && bash tools/deploy_twin.sh --stop --port 18085 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"start-pty\", \"/tmp/qa_twin46\"))" && bash tools/deploy_twin.sh --mode hardware --uart "$(cat /tmp/qa_twin46/pty_path)" --baud 921600 --port 18085 && bash tools/deploy_twin.sh --status --port 18085 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-online\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log --matrix-out /tmp/qa_twin46/live_ok_matrix.md && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-mismatch\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"restore-mismatch\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-crc-err\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-drop\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-offline\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log --matrix-out /tmp/qa_twin46/live_offline_matrix.md && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-recovery\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live.log --th-log /tmp/qa_twin46/th_live.log --matrix-out /tmp/qa_twin46/reconciliation_matrix.md && test -s /tmp/qa_twin46/live_ok_matrix.md && test -s /tmp/qa_twin46/live_offline_matrix.md && test -s /tmp/qa_twin46/reconciliation_matrix.md && bash tools/deploy_twin.sh --stop --port 18085 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"stop-pty\", \"/tmp/qa_twin46\"))" && rm -rf /tmp/qa_twin46'
    expected: 容器/tmp可写副本下一键编译并验证deploy_twin.sh sim模式启停后，编译mcu-p3真实MC/TH固件模块(libmc_fw.so/libth_fw.so)挂载至921600 POSIX PTY启动全栈服务进入真实NORMAL/ONLINE态，debug_reconciliation_probe.py --ap-url配合C固件实时排空的mc_live.log/th_live.log与ui-gateway实时HTTP/SSE响应完成在线五类业务正例对账、在线运行态网关失配/坏CRC帧/环形缓冲满溢(drop>0)注入非0退出拦截、在线传感器故障注入驱动网关进入OFFLINE(2147483646 mdeg与32767 ddC哨兵及HTTP 503控制锁)对账及在线恢复ONLINE后的五类业务对账闭环并生成reconciliation_matrix.md全部PASS，停止后无残留进程
    availability: available
  positive_cases:
  - debug_reconciliation_probe.py同步解析真实[MC-DBG]与[TH-DBG]结构化串口日志流及AP HTTP/SSE状态快照（支持--self-test、--mc-log/--th-log/--ap-snapshot离线对账及--ap-url配合--mc-log/--th-log在线拉取运行中ui-gateway实时快照与SSE流，不伪造日志或回退默认快照），自动生成五类核心业务（温度、归零/移动、二维5x5调平网格、进退丝/料槽、打印作业状态）双向对账报告(--matrix-out)
  - 全栈一键启动脚本deploy_twin.sh在921600默认配置下完成编译、sim模式启停探活，并通过921600 POSIX PTY连接运行态全栈完成在线五类正向对账、在线故障注入、在线恢复与优雅停止闭环
  negative_cases:
  - 当[MC-DBG]/[TH-DBG]日志中的五类业务状态与AP/UI状态快照不一致、调平网格非严格5x5二维列表（如1x25畸形网格）、或出现未预期的CRC_ERR/TIMEOUT/BAD_FRAME/TX_ERR或drop>0/trunc>0时，debug_reconciliation_probe.py在离线与--ap-url在线模式下均返回非0退出码并定位失配项；恢复一致快照与正常日志流后重新对账返回0
  - 当处于业务串口断连/离线状态（system_status=OFFLINE）时，debug_reconciliation_probe.py按单位严格校验AP温度哨兵值（2147483646毫摄氏度）与MCU日志/deci-C温度哨兵值（32767十分之一摄氏度）及ui-gateway控制接口严格HTTP 503锁定响应（拒绝错误单位哨兵值及504/200状态码），并在运行态网关恢复ONLINE后在线对账恢复通过
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-04T14:58:00+08:00'
---

# TWIN-46 921600全栈配置化启动与MC/TH Debug↔Web UI双向链路对账集成验证

## 1. 任务目标与来源
- **ARCH 拆分依据**：[debug_reconciliation_and_921600_arch_breakdown_20261104.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/debug_reconciliation_and_921600_arch_breakdown_20261104.md) (`revision: 14`, SHA-256 `30a4d3a26878cdf1527f9a59524a93157f0e11dae4776c40342dadfb871745cb`, ARCH Session `1de28c06-e3d8-4a7a-88b5-0ae5069a2c94`)
- **需求与批准绑定**：`FEAT-20261104-001`, `FEAT-20261104-002` / `CONFIRM-DEBUG-BAUD-20261104` (`rev 2`) / `APPR-20261104-001` (`rev 1`)

## 2. 验收标准 (`acceptance_criteria`)
1. 在 `test_harness/hil/tools/debug_reconciliation_probe.py` 实现非侵入式双路结构化 Debug 日志（`[MC-DBG]` + `[TH-DBG]`）与 AP `ui-gateway` HTTP/SSE 接口（`/api/v1/temperature/snapshot`、`/api/v1/temperature/stream`、`/api/v1/jobs/status`、`/api/v1/leveling/mesh`、`/api/v1/filament/slots`）的自动化双向对账采集与比对工具，100% 覆盖 `--help`、`--self-test`、`--mc-log`、`--th-log`、`--ap-snapshot`、`--ap-url`、`--matrix-out` 全部 CLI 选项与代码分支；`--ap-url` 必须显式配合 `--mc-log` 与 `--th-log` 读取真实日志文件并 100% 从运行态 `ui-gateway` 拉取实时状态，严禁伪造日志或回退默认快照。
2. 完成五类核心业务功能（温度上报与设定、归零/运动控制、严格二维 `5×5` 调平网格、进退丝/料槽切换、打印作业状态机）的正向双向对账、反例拦截（数值失配、`1×25` 等畸形网格、`CRC_ERR`/`TIMEOUT`/`BAD_FRAME`/`TX_ERR`、`drop>0`/`trunc>0` 非 0 退出码）、`OFFLINE` 断连按单位严格哨兵值（AP `temperature_millic == 2147483646`、MCU 日志与 `temp_deci_c == 32767`，拒绝单位互换）与严格 HTTP `503` 控制锁定校验（拒绝 `504`/`200`）、以及故障恢复后的再次对账闭环，并生成非空 `reconciliation_matrix.md` 报告。
3. 在受控 Docker 沙箱（`qa-sandbox:20261029`）中验证 `soc-ap/tools/deploy_twin.sh` 全栈一键编译、`sim` 模式启停探活、以及基于 `921600` POSIX PTY 虚拟下位机的全栈在线正向五类对账、在线反例拦截、在线 `OFFLINE` 故障注入与 HTTP `503` 锁定对账、在线恢复 `ONLINE` 后的五类对账与优雅停止闭环（注：交叉编译器 ELF 构建与物理板卡 USB/UART 拔线 HIL 在本纯软件沙箱集成任务中为 `not applicable`，详见 `accepted_scope`）。
