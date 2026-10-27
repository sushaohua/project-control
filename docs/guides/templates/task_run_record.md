# 单票实际执行记录模板

模板版本：2026-10-27。与[任务卡](../../../.agents/rules/templates/任务卡模板.md)、[派单提示](../../../.agents/rules/templates/角色任务提示词.md)、[QA报告](../../../.agents/rules/templates/QA审查报告模板.md)配套。只在真实run复制到本票授权证据目录；模板和计划命令不是运行结果，空值不能改成示例PASS。

```yaml
template_version: '2026-10-27'
task_id: null
task_revision: null
actual_run_id: null
actor_role: null
actor_session: null
lease_id: null
start_time: null # UTC或明确时区；不得猜秒数
end_time: null
workspace: null
branch: null
input_versions: [] # 每项来源/生产票、准确版本、用途、接受报告/哈希
source_head: null
workspace_diff_sha256: null
version_bundle: null # 路径及SHA256，包含实际输入/候选组合
verification_environment: null
verification_scope: null
required_evidence_level: null
commands: [] # 每项结构见下面 command_fields；写实际执行过的命令
case_results: [] # 每例结构见下面 case_result_fields
required_test_sets: []
executed_test_sets: []
missing_test_sets: []
candidate_commit: null
candidate_diff_sha256: null
artifact_hashes: [] # 每项 path/sha256/type；区分ELF/raw BIN/pack BIN/报告
hardware: null # HIL才填：端点、串口参数、probe/UID、实际部署/启动身份与证据
raw_trace_files: [] # 每项路径/SHA256/时戳来源/方向/丢失或截断数
failures_and_corrections: []
actual_result: not-executed # not-executed / passed / failed；不是任务Done或QA决定
unverified: []
not_applicable: [] # 环节、理由和接受依据；不适用不填PASS
independent_reviews: [] # 每项角色、实际会话、同一候选/revision、报告路径/SHA256/决定
handoff:
  receiver_session: null
  acknowledgement_path: null
  acceptance_record: null # COORD另行接受记录；收件回执不代替签署
```

```yaml
command_fields:
  command: null
  cwd: null
  start_time: null
  end_time: null
  tool_versions: []
  actual_exit_code: null
  stdout_stderr_path: null
  stdout_stderr_sha256: null
  actual_case_count: null
  warning_count: null
case_result_fields:
  case_id: null
  scenario: null # normal / fault-injection / document-check等实际范围
  expectation_source_version: null
  input_or_trigger: null
  expected: null # 包含正常响应或预期无响应/错误、时间期限与退出码
  observed: null
  matched_response_count: null # 文档/非通信检查不适用时说明
  result: not-executed # not-executed / passed / failed / not-applicable
  evidence: null
  evidence_sha256: null
```

`*_fields`是数组元素的结构说明，不把空对象当已运行命令/用例。先固定独立预期，再写实际观察。负例的预期exit非零或零响应可以正确，但必须比较预期与实际；正常查询零有效关联响应必须失败。单纯exit0、CRC正确或测试进程未崩溃不构成业务成功。

正文写明实际修改、前置能力为何可用、失败原文→根因→逐次更正、未执行项、用户既有差异、回退范围和下游使用限制。必跑组缺失、case=0或关键原始日志截断时不得宣称对应验收通过。

HIL记录真实端点和部署身份，原始TX/RX带UTC毫秒及单调时钟/测量点；RTT记录样本、成功/失败/超时及分布。PTY/Mock/假探针结果只能归host-software；命令写入成功、文件改名不等于物理恢复或新App生效。

本记录只承载执行事实；所有必需独立检查分别填写`independent_reviews`。新记录使用数组，避免一个结论覆盖多岗位；已有历史`independent_review`原件保留，修订时注明字段迁移，不能补造过去的签署。报告自身SHA256在文件写完后保存到任务卡/交接清单，避免自引用。
