---
template_version: '2026-10-27'
review_id: TWIN-06-run-01-independent-qa
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: unverified
model_override_ref: null
planned_session_alias: planned-qa-twin-06
actual_session: 01a18b51-af95-7300-b366-dac8e82b43b6
author_session: null
task_id: TWIN-06
task_revision: 2
reviewed_artifact_version: 'soc-ap=4f08089a6f10049ad65766805d3a20f4f59eea8c; test_harness=0b7497ba43158841eb3c4af7f16e477b9c30c2c5; mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503; requested project-control=b3665c1926685ba0f48866e409ec8ec7a9a13998 (not found); server lock project-control=e07684b12b3763c59b094592c2ba0e6660547c13; origin/main=b3665c10a172a247f4ef303bf7984118319bb97c'
reviewed_artifacts:
  - {path: soc-ap/middleware/dbus/include/aisoc_dbus.h, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 73d8004e9cc391f91e09eb5717526a695ff57f1ba739b2df3f651cf339c16bc1}
  - {path: soc-ap/middleware/dbus/src/aisoc_dbus_internal.h, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 261d7d9b4d512042dac100fbd56e1dc33ac454b64c4b9185b9db547087a48dd0}
  - {path: soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: a83978c549e27f69a599944c0e0b0902a0cd2420875916e19dd0a85b21eac987}
  - {path: soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: c01e907582542f75a463cfa2b26df442b18717d707ab2a39fa371ebc6ab67c1c}
  - {path: soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 669c5884a61a7998a8935501097fe1e7fc908d14bc7d8a45ced766a38602bf2d}
  - {path: soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: f3e2cab25bf1bd79f7e7524ac0e8ef773e3d2947fd294eff5bbc687a60cacf74}
  - {path: soc-ap/middleware/dbus/CMakeLists.txt, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 80cffcdea600067b12140da694f7a90a00bb247fa03b9c64c7599059762e09b8}
  - {path: soc-ap/middleware/dbus/examples/server_example.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 0eec65f5be141911e4e16fb9f8e2a8c84efd328581f2bd21c282325db19b4558}
  - {path: soc-ap/middleware/dbus/examples/client_example.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 30127a238e75ff469ba06b1e7cee04a99c00e0f0bfe86903e9996fc6880d7608}
  - {path: soc-ap/middleware/dbus/README.md, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: ab3229bbc2441a7bb09175c0b91521e6a73079f2d4e51267263766d9eb65da9f}
  - {path: soc-ap/config/dbus/twin/session_twin.conf, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 86e75ad9413fca24c6282356fba7dd206d460efe8fa8daa9025c298540921a96}
  - {path: soc-ap/config/dbus/twin/org.aisoc.conf, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: bc147d05ee8018cf25862766bf52cfbe5f090f75f06b852936cef56c72ac6060}
  - {path: soc-ap/tests/dbus/twin/CMakeLists.txt, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 06ad077ec9e34dac1a496e96aa7e2c39cd68ee4e45c69547e19ab9b1cd61d88c}
  - {path: soc-ap/tests/dbus/twin/test_dbus_ipc.cpp, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: d5014ac4ceb09a2b2068c0c5050443b1fd8ecec93bec49976b9a81d1109a9a97}
  - {path: soc-ap/third_party/dbus/README.md, commit: 4f08089a6f10049ad65766805d3a20f4f59eea8c, sha256: 2898d82324e54110e6c3a95972ee26af794512a03bbf689043e7f961758315f3}
protocol_and_expectations:
  - {source: project-control/.agents/rules/delivery_and_coord_gate.md, version: 1}
  - {source: project-control/.agents/rules/codex_qa_review.md, version: '2026-10-27 update'}
  - {source: project-control/.agents/rules/c_cpp_coding_standard.md, version: 1.0}
  - {source: project-control/.agents/rules/templates/QA审查报告模板.md, version: '2026-10-27'}
  - {source: project-control/.agents/kanban/microtasks/vmware_soc_twin/TWIN-06.md, version: 2}
verification_environment: 'Server QA Docker container 1eaaa0633d60f78885d2d2a50d3e7b9d82220dac04d16097727a144a87fdf68c; image digest sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f; read-only source bind mount.'
verification_scope: 'Read-only source, candidate and server evidence audit; no host-side build or test.'
required_evidence_level: server-sandbox-verified
review_time: '2026-10-30 Asia/Shanghai'
process_audit: failed
result_check: partial
decision: REJECTED
determination: REJECTED
accepted_scope: 'The soc-ap artifacts match the supplied hashes. Server logs record a successful compile and real three-process IPC run for the server lock candidate.'
limitations:
  - 'No hardware or SoC board validation was performed.'
  - 'Actual runtime model and author session were not independently verified.'
unexecuted:
  - 'Permission-denial / unauthorized name ownership case.'
  - 'Host-side reproduction; the recorded server QA run was reviewed without repeating it.'
not_applicable:
  - 'Physical HIL is outside the server-sandbox-verified scope; no HIL pass is inferred.'
issues:
  - id: QA-01
    severity: blocking
    finding: 'The requested project-control SHA does not exist on origin. server_lock names e07684b12b3763c59b094592c2ba0e6660547c13; origin/main resolves to b3665c10a172a247f4ef303bf7984118319bb97c. The candidate set is not accurately bound.'
    evidence: 'git cat-file/fetch for b3665c1926685ba0f48866e409ec8ec7a9a13998 failed (not our ref); git ls-remote origin refs/heads/main and run_01/server_qa/server_lock.json.'
  - id: QA-02
    severity: blocking
    finding: 'Permission denial is not verified. The test daemon loads session_twin.conf, whose default policy allows send_destination="*" and eavesdrop. org.aisoc.conf is not passed to that daemon, and no unauthorized client/name rejection case is present.'
    evidence: 'soc-ap/config/dbus/twin/session_twin.conf; soc-ap/config/dbus/twin/org.aisoc.conf; tests/dbus/twin/test_dbus_ipc.cpp:spawn_daemon/run_client_test_suite.'
  - id: QA-03
    severity: blocking
    finding: 'The task card reviewer session/evidence fields are null; author-session identity is not available, and this QA report has not received the required independent non-author report review.'
    evidence: 'TWIN-06.md reviewer_sessions; run_01/codex_session.jsonl; codex_qa_review.md and delivery_and_coord_gate.md section 3.'
commands:
  - command: 'git -C project-control cat-file/fetch origin <requested SHA>; git -C project-control ls-remote origin refs/heads/main'
    cwd: /home/sushaohua/workspace/ai_soc_project
    tool_version: 'git; exact host version not recorded'
    time: '2026-10-30 Asia/Shanghai'
    exit_code: 'requested SHA fetch failed; ls-remote succeeded'
    output_evidence: 'The requested SHA was not found on origin; remote main was b3665c10a172a247f4ef303bf7984118319bb97c.'
  - command: 'sha256sum all 15 deliverables and server QA evidence files'
    cwd: /home/sushaohua/workspace/ai_soc_project
    time: '2026-10-30 Asia/Shanghai'
    exit_code: '0'
    output_evidence: 'All deliverable hashes matched the supplied manifest; server_lock, checkout.log, runtime.log and server_verdict hashes matched server_qa.json references.'
case_results:
  - case: 'Build and three-process IPC suite'
    expected: 'Build with warnings-as-errors and pass RPC, timeout, error mapping, signals and introspection.'
    observed: 'server_qa.json/runtime.log record exit 0; 7 passed, 0 failed; daemon, server worker and client are separate processes.'
    result: passed-for-recorded-lock
    evidence: 'server_qa.json sha256 8300b175657d0e84c3f9896ab33b98b8258058b9e8c510ecd65af0da904669bf; runtime.log sha256 a00b68d5ef8dddd07c7badd06e7d6ad1dce41867812394c94b76388d978b7211.'
  - case: 'Unauthorized access policy'
    expected: 'A disallowed caller or name owner is rejected under effective policy.'
    observed: 'Not executed; loaded session profile allows arbitrary send destination; system policy was not loaded.'
    result: not-executed
    evidence: 'session_twin.conf; test_dbus_ipc.cpp:710-733.'
required_test_sets: ['Locked-candidate build', 'Three-process RPC/error mapping', 'Timeout', 'Signal broadcast', 'Introspection', 'Permission denial']
executed_test_sets: ['Locked-candidate build', 'Three-process RPC/error mapping', 'Timeout', 'Signal broadcast', 'Introspection']
missing_test_sets: ['Permission denial / unauthorized name ownership']
raw_trace_files: []
supersedes_or_limits: []
handoff:
  receiver_session: null
  evidence_location: project-control/docs/evidence/twin/TWIN-06/runs/run_01/qa_review_report.md
server_qa: {path: project-control/docs/evidence/twin/TWIN-06/runs/run_01/server_qa/server_qa.json, sha256: 8300b175657d0e84c3f9896ab33b98b8258058b9e8c510ecd65af0da904669bf, sandbox_id: TWIN-06_run_133139_20261030_053139, container_id: 1eaaa0633d60f78885d2d2a50d3e7b9d82220dac04d16097727a144a87fdf68c, image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f, server_lock_project_control: e07684b12b3763c59b094592c2ba0e6660547c13}
content_audit:
  fact_sources: {result: passed, basis: 'Checked server lock, checkout/runtime logs and hashes; container evidence supports software sandbox only.'}
  protocol_compatibility: {result: not-applicable, basis: 'No MCU wire-protocol change is part of this SDK delivery.'}
  claim_scope: {result: passed, basis: 'Conclusion is limited to container compilation and IPC; no physical-board claim.'}
  architecture_completeness: {result: failed, basis: 'Permission denial is untested and the project-control candidate binding mismatches.'}
reviewed_qa_report_sha256: null
---

# TWIN-06 独立 QA 审查报告（Run 01）

## 结论

**Decision: REJECTED。** 不能按要求签发 APPROVED：project-control 候选提交不匹配，D-Bus 权限拒绝路径没有实际验收，且独立 Reviewer/报告复核证据尚未完整绑定。

## 候选和哈希核对

SoC、测试仓、MCU 候选分别与 checkout HEAD 和服务器锁定记录一致。用户给出的 project-control SHA `b3665c1926685ba0f48866e409ec8ec7a9a13998` 无法从 origin 获取；远端 `main` 实际为 `b3665c10a172a247f4ef303bf7984118319bb97c`，服务器 `server_lock.json` 则锁定 `e07684b12b3763c59b094592c2ba0e6660547c13`，三者不可互换。

15 个交付文件 SHA-256 均匹配清单。server_qa、server_lock、checkout/runtime log 与 verdict 的哈希引用均匹配。容器 inspect 记录镜像 digest、只读源码挂载和已退出状态。

## 源码与运行证据

源码抽查确认公开指针入口的 guard clause、带 timeout 的同步 RPC、D-Bus 错误回复映射。对交付源文件和测试入口检查函数规模/参数数量，未确认超过 50 行或 4 个参数的自研函数违规；本报告不将作者自检声明当作独立机器证明。用户态 D-Bus 模块不涉及硬件寄存器轮询门禁。

服务器日志记录 `-Wall -Wextra -Werror -fno-exceptions -fno-rtti` 编译退出码 0，测试 7 passed、0 failed。守护进程、服务端 worker、客户端为独立进程。用例覆盖正常 RPC、无效参数错误响应、客户端 deadline 超时、信号广播及 payload、introspection，以及错误名/状态码双向映射。该结果只对 server lock 中的提交集合有效。

权限验收未通过：测试启动 `session_twin.conf`，该 default policy 允许 `send_destination="*"` 和 eavesdrop；`org.aisoc.conf` 未由该测试加载，且没有越权 caller/name ownership 的拒绝用例。通过的 IPC 只能说明宽松 session bus 下通信正常，不能证明权限白名单生效。

## 阻断项与解除条件

1. **QA-01 候选绑定：** 提供可从 origin fetch 的准确 project-control 完整 SHA，并让 server lock/checkout 证据绑定同一准确提交集合。
2. **QA-02 权限负例：** 在预期部署的 bus profile 上实际运行未授权方法调用和名称所有权负例，记录拒绝结果；若 session profile 有意宽松，应明确限定其安全用途，并验证系统 profile。
3. **QA-03 审查来源：** 补齐任务卡 Reviewer session、实际模型和运行记录证据；由非作者独立复核本报告并登记报告 SHA-256。

本决定不否定日志记录的 IPC 正向测试结果；它表示候选绑定及完整任务权限/审查门禁未满足。修复后由 COORD 基于准确候选安排复验，保留本报告历史记录。
