---
id: TWIN-63
title: TWIN-63 MC Bootloader原生USART2 MiniMCProto v2.0本机升级与U盘完整能力共存
revision: 2
plan_revision: vmware-soc-twin-20261106
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: ENG_BOOT_MC
executor:
  role: ENG_BOOT_MC
  agent_id: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  run_id: author_01
qa_policy: streamlined-v1
reviewer:
- QA
verifier: null
integrator: INTEGRATOR
requirement_id: REQ-20261105-003
demand_id: DEM-20261105-006
confirmation_id: CONFIRM-MINIMC-V2-UNIFIED-UPGRADE-20261106
approval_id: APPR-20261106-001
accepted_scope: "Docker QA sandbox (gcc + python3) verification of MC Bootloader native USART2 MiniMCProto v2.0 local upgrade state machine (DST=0x02, no TH routing, zero USART6 coupling), full USB Host flash drive upgrade preservation with trailer_crc32 verification fix, single-writer mutex between USB and USART2, USART2 deinit before jump_to_app, scripts/pack_firmware.py MC(896KB=917,504B) & TH(236KB=241,664B) boundary checks, host unit tests in tests/test_mc_boot_ota.c, and C function <=50 lines / <=4 params & Chinese comment check (S04). Cross-compiler arm-none-eabi-gcc ELF/bin build (36,612B <= 131,072B verified on host in author_01/result.md) and physical HIL flashing (covered by D4-A & TWIN-67) are not applicable in qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-63
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-63/runs/qa_02/qa_review_report.md
  verifier_session: null
  integrator_session: null
primary_work_package: TASK-009
related_work_packages:
- TASK-007
- TASK-012
depends_on:
- TWIN-60
dependency_conditions:
- task: TWIN-60
  accepted_version: project-control=960f079647a00864fe7913836336b2a2ee3d729a; soc-ap=79932746d225bb115010c5545ef3f7499482e137;
    mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7; test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
  acceptance_evidence: docs/evidence/twin/TWIN-60/runs/qa_02/qa_review_report.md
  required: 继承TWIN-60锁定基线
scope_status: mapped
allowed_repositories:
- boot/bootloadermc
- project-control
write_scope:
  boot/bootloadermc:
  - bootloader/inc/**
  - bootloader/src/**
  - scripts/pack_firmware.py
  - app_test/inc/th_upgrade_mgr.h
  - bootloader/CMakeLists.txt
  - Makefile
  - tests/**
  project-control:
  - docs/evidence/twin/TWIN-63/**
allowed_paths:
- boot/bootloadermc/bootloader/inc/**
- boot/bootloadermc/bootloader/src/**
- boot/bootloadermc/scripts/pack_firmware.py
- boot/bootloadermc/app_test/inc/th_upgrade_mgr.h
- boot/bootloadermc/bootloader/CMakeLists.txt
- boot/bootloadermc/Makefile
- boot/bootloadermc/tests/**
- project-control/docs/evidence/twin/TWIN-63/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/bootloaderth/**
- test_harness/**
- boot/bootloadermc/.repo-rules/**
source_baseline:
  project-control: 5cd627395877b8f5eccd884a83c70e3a5d0cc73a
  soc-ap: c6692b244e0aa09d04e7051293f9fef3c67535dd
  mcu-p3: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
  test_harness: 19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  boot/bootloadermc: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  boot/bootloaderth: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
base_commit: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
branch: soc_debug
candidate_commit: 77a3651d551e88978654f5bd14688ce2f71876d6
dispatch_binding:
  source_commit: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  consumed_artifact_versions:
    master_upgrade_architecture: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223
    protocol_v2_0_4: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
protocol_input:
  path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c
  revision: Rev 2.0.4
icd_versions:
- path: project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
  version: 2
- path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
  version: Rev 2.0.4
read_sources:
- project-control/.agents/rules/repository_rule_sources.json
- project-control/.agents/rules/repository_rule_boundaries.md
- project-control/.agents/rules/bootloader_role_boundaries.md
- project-control/.agents/rules/c_cpp_coding_standard.md
- project-control/.agents/rules/code_documentation_standard.md
- project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md
- project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md
- project-control/docs/planning/minimc_v2_upgrade_engineering_inputs_20261105.md
- project-control/docs/planning/minimc_v2_upgrade_qa_planning_input_20261105.md
- project-control/docs/guides/minimc_v2_mcu_upgrade_and_hil_deployment_manual_20261105.md
worktree: boot/bootloadermc
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 2
  lease_id: lease-twin-63-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: boot-bootloadermc-worktree
  location: boot/bootloadermc
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
  - boot/bootloadermc/bootloader/inc/**
  - boot/bootloadermc/bootloader/src/**
  - boot/bootloadermc/scripts/pack_firmware.py
  - boot/bootloadermc/app_test/inc/th_upgrade_mgr.h
  - boot/bootloadermc/tests/**
  record: docs/evidence/twin/TWIN-63/runs/author_01/result.md
rollback:
  steps:
  - git -C boot/bootloadermc checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-63
  acknowledgement: accepted
verification:
  commands:
  - id: build_and_test_twin-63
    cwd: boot/bootloadermc
    command: 'cat ../../project-control/docs/evidence/twin/TWIN-63/runs/author_01/result.md && ! grep -rn "USART6" bootloader/src/ bootloader/inc/ && echo "[PASS] Zero USART6 coupling in MC Bootloader source/headers!" && rm -rf /tmp/qa_twin63 && cp -r . /tmp/qa_twin63 && cd /tmp/qa_twin63 && mkdir -p build && sed -n "20,99p" tests/run_tests.sh | sh && python3 -c "import pathlib, re, sys; files = [\"app_test/inc/th_upgrade_mgr.h\", \"bootloader/inc/boot_uart_ota.h\", \"bootloader/src/boot_uart_ota.c\", \"bootloader/src/main.c\", \"bootloader/src/usbh_user.c\", \"scripts/pack_firmware.py\", \"tests/test_mc_boot_ota.c\"]; cjk = re.compile(r\"[\\u4e00-\\u9fff]\"); [ (txt := pathlib.Path(p).read_text(encoding=\"utf-8\"), assert_cjk := sum(1 for l in txt.splitlines() if cjk.search(l)) >= 3, print(f\"[DOC-CHECK PASS] {p}: cjk_lines={sum(1 for l in txt.splitlines() if cjk.search(l))}\"), (sys.exit(1) if not assert_cjk else None)) for p in files ]; print(\"[PASS] code_documentation_standard check passed!\")" && rm -rf /tmp/qa_twin63'
    expected: "Docker QA沙箱内MC零USART6耦合检查、scripts/pack_firmware.py MC(896KB)/TH(236KB)边界门禁、test_mc_boot_ota MiniMCProto v2.0与U盘/串口互斥单测、函数规模/入参及中文注释门禁(S04) 100%通过。（accepted_scope说明：qa-sandbox:20261029镜像不含arm-none-eabi-gcc交叉编译器，宿主机交叉编译36612B <= 131072B已在author_01/result.md核验，实体HIL烧录在TWIN-67核验，均排除在本Docker沙箱范围外）"
    availability: available
  positive_cases:
  - 100%保留USB Host U盘升级并补齐trailer_crc32校验；新增USART2 921600 DST=0x02 MiniMCProto v2.0本机升级、UPG2驻留魔数、U盘/串口单一写入互斥锁与跳转前USART2复位（Docker沙箱执行gcc宿主机单测与pack_firmware.py边界门禁；arm-none-eabi-gcc交叉编译36612B<=131072B与实体HIL排除在qa-sandbox:20261029外）
  negative_cases:
  - 严禁MC Boot初始化USART6或转发DST=0x03帧；0x20错board_id、坏trailer_crc32或超917504B时零Flash擦除拒绝；U盘与串口并发触发时互斥拒绝后到通道
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-63 MC Bootloader原生USART2 MiniMCProto v2.0本机升级与U盘完整能力共存

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 100%保留USB Host U盘升级并补齐trailer_crc32校验；新增USART2 921600 DST=0x02 MiniMCProto v2.0本机升级、UPG2驻留魔数、U盘/串口单一写入互斥锁与跳转前USART2复位
2. 严禁MC Boot初始化USART6或转发DST=0x03帧；0x20错board_id、坏trailer_crc32或超917504B时零Flash擦除拒绝；U盘与串口并发触发时互斥拒绝后到通道
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
