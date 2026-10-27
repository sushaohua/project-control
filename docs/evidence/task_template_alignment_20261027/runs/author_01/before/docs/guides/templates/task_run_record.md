# 单票实际执行记录模板

此模板只供真实 run 时复制到卡内证据目录；模板不是已执行结果。未发生的命令、签署或回执填“未执行/待检查”，不填写示例 PASS。

```yaml
task_id: null
task_revision: null
actual_run_id: null
actor_session: null
lease_id: null
start_time: null
end_time: null
workspace: null
input_versions: []
source_head: null
workspace_diff_sha256: null
commands:
  - command: null
    cwd: null
    start_time: null
    end_time: null
    actual_exit_code: null
    stdout_stderr_path: null
    actual_case_count: null
    warning_count: null
candidate_commit: null
candidate_diff_sha256: null
artifact_hashes: []
failures_and_corrections: []
actual_result: not-executed
unverified: []
independent_review:
  platform: codex
  policy: project-control/.agents/rules/codex_qa_review.md
  planned_session_alias: null
  reviewer_session: null # 实际落实的会话入口，不填未启动的计划名
  cli_session_id: null # 通过 CLI 审核时记录真实 ID
  reviewed_artifact_version: null
  report_path: null
  report_sha256: null
  decision: null
handoff:
  receiver_session: null
  acknowledgement_path: null
  decision: null
```

正文按需补：本票实际修改、输入与前置为何可用、正常/异常预期与观察、失败根因和逐次更正、保留的用户差异、回退范围、交付版本与下游使用限制。
