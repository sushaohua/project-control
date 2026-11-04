```yaml
task_id: QA-EFFICIENCY-20261104
task_revision: 1
candidate_commit: 567db517a981642f1cb2b052ca2ebd17c755653e
role: QA
decision: REJECTED
summary: 审阅两仓本次差异、相关调度与审阅代码、适用的 §5.4 和中文注释规范。可信证据索引记录两仓候选提交及 137 项相关测试通过。发现一项复验路径可绕过必需的同角色历史报告，违反本轮验收约束。
findings:
- 阻断：review_bundle.py 的 build_reverification_context 在前次运行记录没有当前 role 的报告时，只写入 previous_report_status，仍生成差异并继续调用审阅器；review_prompt
  还允许在没有报告时继续复验。这样复验可能在缺少可核验的同角色前次报告时给出 APPROVED。应将该报告缺失视为证据不足并保持 BLOCKED，不能继续批准。此行为违反
  §5.4 对复验使用既有报告、记录和输入引用的要求，以及本任务“复验携带当前role的可核验旧报告及prev→current diff”的验收约束。发现位置：project-control/tools/coord_runner/review_bundle.py：build_reverification_context、review_prompt。
- 非阻断建议：本次新增 Python 工具模块的文件级 docstring 仍为英文（review_bundle.py 文件开头）；中文注释规范要求新增或修改的说明性注释及
  docstring 使用中文。该说明性文字不影响运行行为，可作为非阻断建议。
accepted_scope: 只读审阅 project-control 候选 567db517a981642f1cb2b052ca2ebd17c755653e（相对基线
  94226a2c655a3cd9fd23f14a5e641a247ed22ad9）和 ai-soc-workspace 候选 5ff859af1fc2658fe1ffaabe06825e763cd506a5（相对基线
  f7af3e1e892378ad17a671fb06f6f7aff8b05cb7）；范围为 QA 效率纠偏规则/模板、Python 审阅证据绑定与复验流程、相关测试，以及
  AGENTS 引用和 workspace.json 对 project-control 的准确 pin。未审阅业务功能、HIL、烧录或服务部署。
unexecuted: []
actual_session: 01a1a560-5ea0-7a20-995e-54694209b32c
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=567db517a981642f1cb2b052ca2ebd17c755653e;
  ai-soc-workspace=5ff859af1fc2658fe1ffaabe06825e763cd506a5
server_qa:
  task_id: QA-EFFICIENCY-20261104
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 8bd99a66b3f3
    id: QA-EFFICIENCY-20261104_run_150344_20261104_070344
    image: qa-sandbox:20261029
    path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344
    developer_mounts: []
    container_inspect:
      id: 8bd99a66b3f389d511cb8b022fdca699a379ddc3010c6955a47b079b98ea7c5b
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T07:03:53.242627616Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_efficiency_20261104/run_01/evidence/server_lock.json
    sha256: 293c019eeffc3c5780bcbba911ba53124dda21e9dec07442c83b25aea9a1b202
  checkout_log:
    path: /tmp/qa_efficiency_20261104/run_01/evidence/checkout.log
    sha256: bcceabd4ad73e3519386314e4f6508fa38b35d971111272b22465ee9927d326a
  runtime_log:
    path: /tmp/qa_efficiency_20261104/run_01/evidence/runtime.log
    sha256: bec4147620a7c88a996553d915af5f333fb0c4abf642ea5b1f8304d52361174c
  server_verdict:
    path: /tmp/qa_efficiency_20261104/run_01/evidence/server_verdict.json
    sha256: a52b8245c88746b2cb72aca0724cfa5dbe642ba6ed08a2ee46520174f5f3b843
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results:
  - command: 'python3 -c ''from pathlib import Path; [compile(Path(p).read_text(),p,''"''"''exec''"''"'')
      for p in [''"''"''tools/coord_runner/review_bundle.py''"''"'',''"''"''tools/coord_runner/runner.py''"''"'',''"''"''tools/test_qa_review_efficiency.py''"''"'']];
      print(''"''"''Python syntax: PASS''"''"'')'''
    exit_code: '0'
    subpath: project-control
    duration: 0.11s
    output: 'Python syntax: PASS'
  test_results:
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_qa_review_efficiency.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 0.39s
    output: 'test_approved_may_include_nonblocking_recommendation (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_current_card_revision_is_checked_before_freeze (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_frozen_manifest_and_declared_run_id_are_bound (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_prior_report_must_match_current_reviewer_role (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_prompt_separates_first_review_and_recheck (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_real_pipeline_blocks_bad_artifact_and_stale_card_before_model (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok

      test_reverification_binds_prior_report_hash_and_candidate_delta (test_qa_review_efficiency.QAReviewEfficiencyTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 7 tests in 0.177s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_qa_pipeline.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 3.10s
    output: 'test_commentary_cannot_corrupt_separate_schema_result (test_qa_pipeline.CodexAdapterProtocolTest)
      ... ok

      test_failed_process_cannot_fallback_or_approve (test_qa_pipeline.CodexAdapterProtocolTest)
      ... ok

      test_fenced_json_is_validated_as_one_document (test_qa_pipeline.CodexAdapterProtocolTest)
      ... ok

      test_non_json_final_cannot_approve_and_logs_survive (test_qa_pipeline.CodexAdapterProtocolTest)
      ... ok

      test_timeout_preserves_partial_events_and_error (test_qa_pipeline.CodexAdapterProtocolTest)
      ... ok

      test_blocked_task_does_not_retry_on_poll (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_daemon_survives_task_audit_error (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_exception_does_not_prevent_other_inflight_task (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_explicit_sandbox_rerun_preserves_previous_evidence (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_failed_objective_checks_are_audited_but_cannot_be_approved (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_finite_mode_returns_when_only_blocked_tasks_remain (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_hil_requirement_cannot_be_approved_by_software_profile (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_internal_typeerror_is_not_reinvoked_with_another_signature (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_invalid_audit_blocks_persists_and_resume_reuses_test_evidence (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_missing_cases_and_wrong_candidate_cannot_be_approved (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_missing_plan_blocks_before_any_model_or_subprocess (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_sandbox_then_independent_readonly_audits_and_bound_reports (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_sandbox_timeout_blocks_without_model_review (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_streamlined_extra_arch_uses_same_completed_sandbox (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_streamlined_qa_authored_tool_gets_one_arch_audit (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_streamlined_resume_uses_completed_facts_and_rejects_tampering (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_streamlined_runs_one_sandbox_and_one_independent_audit (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_tampered_evidence_prevents_resume_from_approving (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok

      test_valid_rejection_returns_to_author_with_report_evidence (test_qa_pipeline.DeterministicQAPipelineTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 24 tests in 2.325s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_coord_runner.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 7.99s
    output: 'test_checkpoint_corrupt_defense (test_coord_runner.CheckpointAndRecoveryTest)
      ... ok

      test_checkpoint_roundtrip (test_coord_runner.CheckpointAndRecoveryTest) ...
      ok

      test_crash_and_restart_recovery_drill (test_coord_runner.CheckpointAndRecoveryTest)
      ... ok

      test_crash_and_restart_recovery_drill_from_disk_sandbox_qa (test_coord_runner.CheckpointAndRecoveryTest)
      ... ok

      test_process_level_kill_and_restart_recovery_drill (test_coord_runner.CheckpointAndRecoveryTest)
      ... ok

      test_codex_auth_failure_blocked (test_coord_runner.CodexAndSandboxIsolationGateTest)
      ... ok

      test_codex_unavailable_blocked (test_coord_runner.CodexAndSandboxIsolationGateTest)
      ... ok

      test_docker_container_sandbox_passed (test_coord_runner.CodexAndSandboxIsolationGateTest)
      ... ok

      test_plain_directory_sandbox_rejected (test_coord_runner.CodexAndSandboxIsolationGateTest)
      ... ok

      test_daemon_signal_handling (test_coord_runner.ExecutionModesTest) ... ok

      test_default_agent_executor_invokes_role_adapter_with_approval (test_coord_runner.ExecutionModesTest)
      ... ok

      test_default_agent_executor_rejects_unapproved_or_unpushed_candidate (test_coord_runner.ExecutionModesTest)
      ... ok

      test_ensure_qa_report_review_preexisting_invalid_review_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_ensure_qa_report_review_preexisting_valid_review_accepted (test_coord_runner.ExecutionModesTest)
      ... ok

      test_execute_review_phase_dedicated_reviewer_typeerror_fails_without_fallback
      (test_coord_runner.ExecutionModesTest) ... ok

      test_execute_review_phase_multi_role (test_coord_runner.ExecutionModesTest)
      ... ok

      test_execute_review_phase_preexisting_invalid_report_review_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_execute_review_phase_qa_report_review_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_execute_review_phase_valid_report_review_approved_to_done (test_coord_runner.ExecutionModesTest)
      ... ok

      test_invoke_report_reviewer_passes_req_dict (test_coord_runner.ExecutionModesTest)
      ... ok

      test_missing_executor_fails_closed (test_coord_runner.ExecutionModesTest) ...
      ok

      test_production_executors_wiring (test_coord_runner.ExecutionModesTest) ...
      ok

      test_run_once_mode (test_coord_runner.ExecutionModesTest) ... ok

      test_run_tasks_finite_mode (test_coord_runner.ExecutionModesTest) ... ok

      test_runner_resolve_qa_report_missing_entry_path_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_runner_resolve_qa_report_missing_entry_sha_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_runner_resolve_qa_report_missing_file_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_runner_resolve_qa_report_prefill_mismatch_rejected (test_coord_runner.ExecutionModesTest)
      ... ok

      test_sandbox_qa_restart_recovery_progresses (test_coord_runner.ExecutionModesTest)
      ... ok

      test_uart_conflict_rolls_back_implementation_lease (test_coord_runner.ExecutionModesTest)
      ... ok

      test_verify_server_commit_variants (test_coord_runner.ExecutionModesTest) ...
      ok

      test_exclusive_device_conflict_uart (test_coord_runner.LeaseAndExclusivityTest)
      ... ok

      test_implementation_concurrency_limit (test_coord_runner.LeaseAndExclusivityTest)
      ... ok

      test_lease_expiration_and_prune (test_coord_runner.LeaseAndExclusivityTest)
      ... ok

      test_lease_renewal_and_expired_renewal_fails (test_coord_runner.LeaseAndExclusivityTest)
      ... ok

      test_release_lease_frees_resource (test_coord_runner.LeaseAndExclusivityTest)
      ... ok

      test_legacy_queue_and_twin_tasks_explicitly_isolated (test_coord_runner.M1QueueIsolationAndDoneGateTest)
      ... ok

      test_module_cli_intake_scan_runs_cleanly (test_coord_runner.M1QueueIsolationAndDoneGateTest)
      ... ok

      test_scheduler_enforces_done_acceptance_errors_on_predecessors (test_coord_runner.M1QueueIsolationAndDoneGateTest)
      ... ok

      test_subagent_platform_and_planned_alias_rejected_in_state_machine (test_coord_runner.M1QueueIsolationAndDoneGateTest)
      ... ok

      test_python_functions_scale_and_parameters_limits (test_coord_runner.MethodologicalInvariantsTest)
      ... ok

      test_author_self_review_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_candidate_commit_validation (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_any_review_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_entry_missing_report_sha (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_missing_report_review (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_file_not_found_on_disk (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_file_tampered_or_sha_mismatch (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_review_by_author (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_review_missing_report_path_or_sha (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_review_self_reviewed (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_review_sha_mismatch (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_qa_report_review_unapproved (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_done_rejected_when_required_role_missing (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_evidence_based_remediation_validation (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_fake_done_rejected (test_coord_runner.StateMachineAndRemediationTest) ...
      ok

      test_max_corrections_exceeded_escalation (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_developer_mounts_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_failure_triggers_remediation (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_commit_mismatch_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_invalid_sandbox_kind_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_missing_server_qa_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_missing_task_revision_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_string_false_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_qa_verdict_task_revision_mismatch_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_remediation_missing_evidence_rejected (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_review_rejection_triggers_remediation (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_state_machine_invalid_transition (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_state_machine_positive_flow (test_coord_runner.StateMachineAndRemediationTest)
      ... ok

      test_blocked_task_filtered (test_coord_runner.TaskSelectionAndSchedulingTest)
      ... ok

      test_bootstrap_prioritized_over_order (test_coord_runner.TaskSelectionAndSchedulingTest)
      ... ok

      test_completed_tasks_filtered (test_coord_runner.TaskSelectionAndSchedulingTest)
      ... ok

      test_resource_unavailable_blocked (test_coord_runner.TaskSelectionAndSchedulingTest)
      ... ok

      test_unmet_dependencies_blocked (test_coord_runner.TaskSelectionAndSchedulingTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 74 tests in 7.828s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_delivery_checks.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 0.28s
    output: 'test_artifact_change_invalidates_old_review (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_complete_recorded_evidence_passes_local_structure_only (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_coord_receipt_cannot_substitute_owner_report (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_current_task_revision_must_match (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_developer_mount_or_worktree_is_not_a_sandbox (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_done_label_cannot_release_unverified_twin_input (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_local_source_or_nonfresh_checkout_is_rejected (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_missing_required_owner_is_rejected (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_new_functions_keep_scale_and_parameter_limits (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_null_dependency_version_is_a_ready_blocker (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_placeholder_server_commit_is_rejected (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_qa_authored_artifact_also_requires_server_sandbox_review (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_qa_report_cannot_self_review (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_report_cannot_approve_a_different_candidate_version (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_report_review_cannot_reuse_qa_sandbox (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_role_alias_without_runtime_record_cannot_close (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_secondary_review_must_bind_exact_qa_report (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_streamlined_accepts_one_primary_review_in_both_gates (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_streamlined_invalid_session_returns_errors_without_crashing (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_streamlined_qa_author_requires_independent_artifact_check (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_streamlined_special_owner_remains_required (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_streamlined_wrong_candidate_and_missing_tests_fail_both_gates (test_delivery_checks.DeliveryChecksTest)
      ... ok

      test_bootstrap_selected_before_business (test_delivery_checks.QueueTest) ...
      ok

      test_duplicate_or_unknown_queue_is_rejected (test_delivery_checks.QueueTest)
      ... ok

      test_existing_assignment_is_reported_before_new_dispatch (test_delivery_checks.QueueTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 25 tests in 0.118s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_review_policy.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 0.23s
    output: 'test_invalid_policy_is_rejected_before_dispatch (test_review_policy.ReviewPolicyTest)
      ... ok

      test_invalid_policy_or_roles_fail_closed (test_review_policy.ReviewPolicyTest)
      ... ok

      test_legacy_is_retained_without_explicit_migration (test_review_policy.ReviewPolicyTest)
      ... ok

      test_new_policy_and_primary_validator_functions_meet_scale_limits (test_review_policy.ReviewPolicyTest)
      ... ok

      test_package_entrypoint_imports_shared_gate_without_tools_path (test_review_policy.ReviewPolicyTest)
      ... ok

      test_qa_authored_tool_defaults_to_one_non_author_arch_check (test_review_policy.ReviewPolicyTest)
      ... ok

      test_streamlined_defaults_to_one_qa_and_retains_explicit_roles (test_review_policy.ReviewPolicyTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 7 tests in 0.072s


      OK'
  - command: 'python3 -c ''from pathlib import Path; import json; d=json.loads(Path(''"''"''ai-soc-workspace/workspace.json''"''"'').read_text());
      assert next(x[''"''"''commit''"''"''] for x in d[''"''"''repositories''"''"'']
      if x[''"''"''path''"''"'']==''"''"''project-control''"''"'')==''"''"''567db517a981642f1cb2b052ca2ebd17c755653e''"''"'';
      assert ''"''"''§5.4''"''"'' in Path(''"''"''ai-soc-workspace/AGENTS.md''"''"'').read_text();
      print(''"''"''Root guidance and exact recovery pin: PASS''"''"'')'''
    exit_code: '0'
    subpath: ''
    duration: 0.11s
    output: 'Root guidance and exact recovery pin: PASS'
  passed: true
  timestamp: '2026-11-04T07:04:08.103107+00:00'
  path: /tmp/qa_efficiency_20261104/run_01/evidence/server_qa.json
  sha256: f74349b1b39c29a773f1d2bab6cff0ffad89b1bf2b3f3c72507ffdd5335e3eea
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_efficiency_20261104/audit_01/codex.jsonl
  sha256: 070968c1b8fde7d970d2532e18a83c39505163075cdcd226b3b7b133db73a44e
reviewed_artifacts:
- path: /tmp/qa_efficiency_20261104/run_01/request.json
  sha256: 3f304616dfc2811bcfd7d632482b1d0e0c174d9636fc7a800dc5ea0586849591
- path: /tmp/qa_efficiency_20261104/run_01/diffs/project-control.patch
  sha256: 630578ff1e9fc849d4e299bd613d69586cc33fd7d811d4efe44cc56425cdf838
- path: /tmp/qa_efficiency_20261104/run_01/diffs/ai-soc-workspace.patch
  sha256: e3733f1bb630c34a0505c5bb4b3f9c0a2a3d8ccb21d722a83b07a33e9541607c
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/.agents/rules/codex_qa_review.md
  sha256: 3b58f127d2fd737e81534c9680b64fa7b53a507b6de76cf710a2bbdb4a4a270a
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/.agents/rules/delivery_and_coord_gate.md
  sha256: 360462bec6222bf44aa8e1800c4d7eb7fc5a34319021c3a098c609985b219c94
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/.agents/rules/templates/QA审查报告模板.md
  sha256: cef58492d356dc3bc8f1bc37e38c3587a9ccb542e11f6c2fcb14aae3fc47e6c9
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/.agents/rules/templates/角色任务提示词.md
  sha256: ef228e2e8437600f05f64226b37355221e2f87cdcd2c38834188f2758e90ea67
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/tools/coord_runner/review_bundle.py
  sha256: 9fc45b37d23cae27465111f14f73d19eb1ded9d41cee2b2b6a81a3242cb6d063
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/tools/coord_runner/runner.py
  sha256: f0ce6e643d78f1d92f02ff7acc9cf15fd28438a0de299175ab9d8738af85b4aa
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/project-control/tools/test_qa_review_efficiency.py
  sha256: b94f0dc6126d7ec061ab0178b5db3ec9195451aee762589b1189fb5a42a0283e
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/ai-soc-workspace/AGENTS.md
  sha256: 713006b920ca7e4cfe4a0022dc9315b60583136d500ad9bea4d86a328f6dc123
- path: /tmp/qa_efficiency_20261104/sandboxes/QA-EFFICIENCY-20261104_run_150344_20261104_070344/ai-soc-workspace/workspace.json
  sha256: 5fa64b855836e8bb142726bde2e60fd77e7b1123a8c5bae469e9ed33844cdddb
verification_scope: 只读审阅 project-control 候选 567db517a981642f1cb2b052ca2ebd17c755653e（相对基线
  94226a2c655a3cd9fd23f14a5e641a247ed22ad9）和 ai-soc-workspace 候选 5ff859af1fc2658fe1ffaabe06825e763cd506a5（相对基线
  f7af3e1e892378ad17a671fb06f6f7aff8b05cb7）；范围为 QA 效率纠偏规则/模板、Python 审阅证据绑定与复验流程、相关测试，以及
  AGENTS 引用和 workspace.json 对 project-control 的准确 pin。未审阅业务功能、HIL、烧录或服务部署。
verification_environment: docker-sandbox-and-independent-codex-audit
```

审阅两仓本次差异、相关调度与审阅代码、适用的 §5.4 和中文注释规范。可信证据索引记录两仓候选提交及 137 项相关测试通过。发现一项复验路径可绕过必需的同角色历史报告，违反本轮验收约束。
