---
id: TWIN-62
title: TWIN-62 TH Bootloader 16KB预算内MiniMCProto v2.0最小升级子集与236KB对齐
revision: 4
plan_revision: vmware-soc-twin-20261106
task_kind: implementation
development_stage: vmware-twin
dispatchable: true
status: Review
blocked: false
planning_status: active
owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
proposed_owner: ENG_BOOT_TH
executor:
  role: ENG_BOOT_TH
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
accepted_scope: "Docker QA sandbox (gcc + python3) verification of TH Bootloader MiniMCProto v2.0 minimal 7-command upgrade subset (0x01/0x02, 0x03/0x04, 0x1D, 0x20 144B pre-erase ATSG trailer check, 0x21 520B max payload with Chunk 0 RAM cache, 0x23, 0x22 Anchor+Chunk0 commit), 236KB (241,664B) net App bound in pack_firmware.py & iap.h (S03), C function <=50 lines / <=4 params & Chinese comment check (S04), and host unit tests in boot/bootloaderth/tests/test_th_boot_ota.c. Cross-compiler arm-none-eabi-gcc ELF/bin build (9,360B <= 16,384B verified on host in author_01/result.md) and physical HIL flashing (covered by D4-A & TWIN-67) are not applicable in qa-sandbox:20261029; all in-scope checks are executed in server_qa so unexecuted is empty when those checks pass."
review_assignments:
  reviewer_sessions:
  - role: QA
    platform: codex
    model: gpt-6-luna
    planned_session_alias: planned-qa-twin-62
    session: null
    decision: PENDING
    evidence: docs/evidence/twin/TWIN-62/runs/qa_04/qa_review_report.md
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
- boot/bootloaderth
- project-control
write_scope:
  boot/bootloaderth:
  - inc/iap.h
  - inc/flash.h
  - inc/usart.h
  - src/iap.c
  - src/flash.c
  - src/main.c
  - src/usart.c
  - tools/pack_firmware.py
  - Makefile
  - tests/**
  project-control:
  - docs/evidence/twin/TWIN-62/**
allowed_paths:
- boot/bootloaderth/inc/iap.h
- boot/bootloaderth/inc/flash.h
- boot/bootloaderth/inc/usart.h
- boot/bootloaderth/src/iap.c
- boot/bootloaderth/src/flash.c
- boot/bootloaderth/src/main.c
- boot/bootloaderth/src/usart.c
- boot/bootloaderth/tools/pack_firmware.py
- boot/bootloaderth/Makefile
- boot/bootloaderth/tests/**
- project-control/docs/evidence/twin/TWIN-62/**
forbidden_paths:
- soc-ap/**
- mcu-p3/**
- boot/bootloadermc/**
- test_harness/**
- boot/bootloaderth/.repo-rules/**
- boot/bootloaderth/ldscripts/AT32A423xC_FLASH.ld
source_baseline:
  project-control: 45c5cdf791ae3d88b76949525ec1b46d25832083
  soc-ap: c6692b244e0aa09d04e7051293f9fef3c67535dd
  mcu-p3: 57674d8b07d6c75a4d20b3fcd52c23df964aa7a7
  test_harness: 19c12bfeeac852670e8bdcb65ce0abcd1de121c1
  boot/bootloadermc: 4fc171ea61912561949b9a0cfc1da8975e4c39ba
  boot/bootloaderth: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
base_commit: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
branch: soc_debug
candidate_commit: 64b7100d3b0260ad1c24b627986475dcd45ad383
dispatch_binding:
  source_commit: 769fccbe52464ad7ceb856c5e89cb0d25abbbf87
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
worktree: boot/bootloaderth
lease:
  owner: 07a1f6dc-f47c-45e5-bf00-37ec14e2dfda
  task_revision: 4
  lease_id: lease-twin-62-20261106-01
  expires_at: '2026-11-07T22:00:00+08:00'
resources:
- resource: boot-bootloaderth-worktree
  location: boot/bootloaderth
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
  - boot/bootloaderth/inc/iap.h
  - boot/bootloaderth/src/iap.c
  - boot/bootloaderth/src/flash.c
  - boot/bootloaderth/src/main.c
  - boot/bootloaderth/tools/pack_firmware.py
  - boot/bootloaderth/tests/**
  record: docs/evidence/twin/TWIN-62/runs/author_01/result.md
rollback:
  steps:
  - git -C boot/bootloaderth checkout -- .
handoff:
  receiver_role: COORD
  receiver_session: ff2fb105-fd84-4ecb-b1e6-8f8eb00badc6
  transport: docs
  evidence_location: docs/evidence/twin/TWIN-62
  acknowledgement: accepted
verification:
  commands:
  - id: build_and_test_twin-62
    cwd: boot/bootloaderth
    command: 'cat ../../project-control/docs/evidence/twin/TWIN-62/runs/author_01/result.md && python3 -c "import subprocess, sys, tempfile, os; tmpd = tempfile.mkdtemp(); [ (open(os.path.join(tmpd, f\"in_{sz}.bin\"), \"wb\").write(b\"\\x5A\" * sz), res := subprocess.run([sys.executable, \"tools/pack_firmware.py\", os.path.join(tmpd, f\"in_{sz}.bin\"), os.path.join(tmpd, f\"out_{sz}.bin\")], capture_output=True, text=True), assert_ok := (res.returncode == 0 and os.path.getsize(os.path.join(tmpd, f\"out_{sz}.bin\")) == sz + 128) if ok else (res.returncode != 0), (sys.exit(1) if not assert_ok else None)) for sz, ok in [(241663, True), (241664, True), (241665, False), (245760, False)] ]; print(\"[PASS] S03 pack_firmware.py 236KB boundary checks (241663/241664/241665/245760) passed!\")" && gcc -std=c11 -O2 -Wall -Wextra -Werror -DIAP_HOST_TEST -DDEBUG_LOG_ENABLE=0 -Iinc src/iap.c src/flash.c tests/test_th_boot_ota.c -o /tmp/test_th_boot_ota && /tmp/test_th_boot_ota && rm -f /tmp/test_th_boot_ota && sed -n "85,122p" tests/run_tests.sh | sh && python3 -c "import pathlib, re, sys; files = [\"inc/iap.h\", \"inc/flash.h\", \"inc/usart.h\", \"src/iap.c\", \"src/flash.c\", \"src/main.c\", \"src/usart.c\", \"tools/pack_firmware.py\", \"tests/test_th_boot_ota.c\"]; cjk = re.compile(r\"[\\u4e00-\\u9fff]\"); [ (txt := pathlib.Path(p).read_text(encoding=\"utf-8\"), assert_cjk := sum(1 for l in txt.splitlines() if cjk.search(l)) >= 3, print(f\"[DOC-CHECK PASS] {p}: cjk_lines={sum(1 for l in txt.splitlines() if cjk.search(l))}\"), (sys.exit(1) if not assert_cjk else None)) for p in files ]; print(\"[PASS] S04 & code_documentation_standard check passed!\")"'
    expected: "Docker QA沙箱内pack_firmware.py 236KB边界门禁(S03)、test_th_boot_ota MiniMCProto v2.0 7命令状态机与负例单测、函数规模/入参及中文注释门禁(S04) 100%通过。（accepted_scope说明：qa-sandbox:20261029镜像不含arm-none-eabi-gcc交叉编译器，宿主机交叉编译9360B <= 16384B及S01链接器溢出验证已在author_01/result.md核验，实体HIL烧录在TWIN-67核验，均排除在本Docker沙箱范围外）"
    availability: available
  positive_cases:
  - 移除5A A5私有帧，实现USART1 921600 MiniMCProto v2.0最小7命令升级子集、首块RAM缓存、Anchor两阶段提交与236KB上限（Docker沙箱执行gcc宿主机状态机单测与pack_firmware.py边界门禁；arm-none-eabi-gcc交叉编译9360B<=16384B与实体HIL排除在qa-sandbox:20261029外）
  negative_cases:
  - 0x20错board_id、坏trailer_crc32或payload_len > 241664B时回NACK且零Flash擦除；无有效Anchor且首字为有效栈顶时拒跳App驻留Boot
required_evidence_level: server-sandbox-and-independent-review
verification_environment: docker-qa-sandbox-and-isolated-codex
qa_review_policy: project-control/.agents/rules/codex_qa_review.md
updated: '2026-11-06T09:55:00+08:00'
---

# TWIN-62 TH Bootloader 16KB预算内MiniMCProto v2.0最小升级子集与236KB对齐

## 1. 权威架构与协议契约依据
- **主架构方案（`revision: 2`）**：[project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/architecture/minimc_v2_unified_mcu_upgrade_architecture_20261105.md) (`sha256: b2b6d047500180c9f4d67d72c94794cbe5080caa52901ba262aa089bc1543223`)
- **协议主规范（`Rev 2.0.4`）**：[project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_4_unified_ota_20261106.md) (`sha256: ec874cab3f8f98fec6412b2da2b4f1fa52bfd8a33601da21e908b0ffaeb0522c`)

## 2. 验收标准 (`acceptance_criteria`)
1. 移除5A A5私有帧，实现USART1 921600 MiniMCProto v2.0最小7命令升级子集、首块RAM缓存、Anchor两阶段提交与236KB上限，Flash总占用 <= 16,384 Bytes
2. 0x20错board_id、坏trailer_crc32或payload_len > 241664B时回NACK且零Flash擦除；无有效Anchor且首字为有效栈顶时拒跳App驻留Boot
3. 全部新增/修改自研函数 100% 满足单函数 <= 50 行、入参 <= 4 个、零动态堆分配，且具备符合 `code_documentation_standard.md` 的中文说明注释。
