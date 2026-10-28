---
template_version: '2026-10-27'
review_id: handover-document-qa-01
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: null
actual_session: /root/handover_document_qa
author_session: /root
task_id: DOC-CASCADE-HANDOVER-20261028
task_revision: 1.0
reviewed_artifact_version: "handover SHA256 47b9773385f5a5271b66572029501d8850a0e396cabb3ea07beb49db8008da50; README SHA256 a0db8f72c752dbdac9763fee475aa64bcde152afa972bc7b60f77f75cc0b40f0"
reviewed_artifacts:
  - path: project-control/docs/operations/ap_mc_th_software_hardware_handover.md
    sha256: 47b9773385f5a5271b66572029501d8850a0e396cabb3ea07beb49db8008da50
  - path: README.md
    sha256: a0db8f72c752dbdac9763fee475aa64bcde152afa972bc7b60f77f75cc0b40f0
protocol_and_expectations:
  - project-control/docs/planning/workflow_replan_20261028.md
  - project-control/docs/baseline/serial_links.md
  - project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md
  - project-control/.agents/rules/codex_qa_review.md
  - project-control/.agents/rules/02_模块与Agent职责.md
  - project-control/.agents/rules/c_cpp_coding_standard.md
verification_environment: read-only Markdown review in /home/sushaohua/workspace/ai_soc_project
verification_scope: handover document and root README entry; no business/source mutation
required_evidence_level: documentation-review
review_time: 2026-10-28 Asia/Shanghai
process_audit: completed
result_check: completed
decision: REJECTED
accepted_scope: null
limitations:
  - Documentation review only; not CR-08 execution, deployment acceptance, or firmware/HIL acceptance.
  - Existing CR-08 SOP/result were checked as mutable references and were not treated as frozen acceptance evidence.
unexecuted:
  - Build and firmware tests
  - Physical deployment, serial communication, and HIL
not_applicable:
  - hardware operation: not authorized or required for document-scope review
issues:
  - "H-01: Section 4's introductory text correctly assigns post-deployment initialization and TX/RX evidence to phases C/D, but the AP↔MC and MC↔TH rows still say '待确认：本次初始化、接线及收发'. This leaves a conflicting reading that phase B requires post-deployment initialization/communication, creating a circular release prerequisite. Clarify both rows as pre-deployment wiring/static-configuration checks and point initialization/TX/RX to C/D."
commands:
  - command: "cat AGENTS.md && cat project-control/.agents/rules/codex_qa_review.md"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
    output: "Read-only terminal output; canonical policy and workspace rules were reviewed."
  - command: "sha256sum project-control/docs/operations/ap_mc_th_software_hardware_handover.md README.md project-control/docs/planning/workflow_replan_20261028.md project-control/docs/baseline/serial_links.md project-control/docs/interfaces/ap_mc_th_readonly_cascade_icd.md project-control/.agents/rules/codex_qa_review.md project-control/.agents/rules/02_模块与Agent职责.md project-control/.agents/rules/c_cpp_coding_standard.md project-control/docs/evidence/cascade_recovery/CR-08/result.md project-control/docs/operations/ap_mc_th_joint_debug.md"
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool: sha256sum
    exit_code: 0
    stdout: project-control/docs/evidence/handover_document_20261028/runs/qa_01/command_01_sha256.stdout.log
    stdout_sha256: c19ecf0c905246bb8236b4163954f769eff38b9b0d1689239dfac09eb163c18d
  - command: "Read line-numbered excerpts from workflow, serial registration, handover stage/table wording and CR-08 result using nl/sed."
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool: nl, sed
    exit_code: 0
    stdout: project-control/docs/evidence/handover_document_20261028/runs/qa_01/command_02_scope_review.stdout.log
    stdout_sha256: 430aa9cc0a061012739775dae1906d2149d47d8a0589b2f9f5e779fafc7405e2
case_results: []
required_test_sets: []
executed_test_sets: []
missing_test_sets: []
raw_trace_files: []
supersedes_or_limits:
  - "This review applies only to the two exact document hashes above. A corrected revision requires a new review run."
handoff:
  receiver_session: COORD / root
  evidence_location: project-control/docs/evidence/handover_document_20261028/runs/qa_01/
---

# 独立审查报告：AP–MC–TH 软硬件交接文档

## 1. 身份、候选与过程核查

审阅者为独立 Codex 会话 `/root/handover_document_qa`，实际模型 `gpt-6-luna`；作者会话 `/root`。审阅对象为交接规范修订 1.0 与 README 新增入口，精确 SHA256 见元数据。按只读范围检查了权威重排、串口登记、ICD、独立 QA 规则、HW-G1～4 职责/权限、编码门禁，并对照 CR-08 记录和联合调试 SOP 的当前内容。

三项建议在主体设计中均可执行：首轮限定只读 GET_VERSION/PING；函数级拆解保留为能力卡内检查点并受 ≤50 行/≤4 参数门禁；真实 HIL 要求双向原始帧和 TH 来源证明，明确拒绝 PTY/Mock 代替物理响应。分阶段顺序与重排一致（CR-12→08→09→10→11），SOP/候选即使标为 frozen 仍要求准确版本接受。已登记串口参数照用，未登记的适配器型号、接头、供电/电平、板号等保持待确认。权限边界未授予 AI 烧录或硬件操作；HW-G1～4及独立性保留。

发现 H-01：§4 总述说明部署前只确认实物身份、接线、电平、映射和静态配置，部署后初始化/收发留给 C/D；但 AP↔MC、MC↔TH 两行仍把“本次初始化、接线及收发”列为待确认。表格可能被解释为阶段 B 必须完成部署后收发，形成循环放行条件。请改成部署前接线/静态配置，部署后初始化与收发引用阶段 C/D。因该歧义直接影响用户要求避免的循环放行，本准确版本 REJECTED。

## 2. 结果、正常/异常判据

文档没有宣称当前部署/HIL已经发生；阶段 E要求独立真实 HIL 和同候选签署，且正常查询有效关联响应为零即失败。TH 身份不得仅靠固定 boot_id/短 git 字段证明；缺少中段观测时要求说明缺口并交 ARCH/QA 判断。故障用例需预先接受，失联/超时按正式预期判断，USART 静默不冒充掉电。这些要求符合 HW-G5/G6 与 QA 规则。

CR-08 当前结果记录仍宣称 APPROVED/直接解锁 CR-09，现有 SOP 含未替换探针占位符及示例固定响应/RTT；本交接文档要求按准确版本重核、补全命令/预期，并明确 frozen 标签本身不构成接受证据。因此本审阅未把两者作为可执行或已接受输入，也未替其变更状态。

## 3. 未执行项与决定

未运行构建、固件测试、串口、部署或硬件 HIL；均不属于文档范围，也未授权。执行命令、cwd、退出码和哈希输出见 `command_01_sha256.stdout.log`、`command_02_scope_review.stdout.log`。报告只针对上述文档 SHA256，不批准固件、CR-08、CR-09 或实际硬件。

**决定：REJECTED（限交接文档修订 1.0 与当前 README 版本）**。修复 H-01 后请对新哈希开启独立复核 run；不修改任务状态。
