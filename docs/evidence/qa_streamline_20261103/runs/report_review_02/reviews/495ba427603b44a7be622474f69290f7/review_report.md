```yaml
task_id: QA-SIMPLIFY-20261103
task_revision: 1
candidate_commit: cec9b34f8284f7b2580a7d219536d32b7b1ee849
role: ARCH
decision: APPROVED
summary: The bundle SHA256 matches 428c5ca1f8e4a01564950a9dc554f7bc6dc8bed060480a25de8af69c6f778178.
  The primary QA report SHA256 independently recomputes to 6b0a1568b8819f60cd99f3a20aa72626a9a39d9517905f29239b2b0edc27a297.
  Its findings and scope are consistent with the pinned candidate and separate frozen
  sandbox evidence.
findings: []
accepted_scope: Bounded QA policy, runner, closure, and template simplification with
  legacy behavior retained until explicit migration; no scheduler rewrite. The pinned
  candidate and its diff match the report. Separate sandbox evidence binds the candidate
  commit and records all eight required suites passing (196 tests), plus the root
  recovery pin, AGENTS, and source hash check. Positive, negative, and recovery coverage
  is present. HIL, MCU builds, and live scheduler deployment are excluded for this
  policy-tool change.
unexecuted: []
actual_session: 01a1a1c1-8534-7dc1-9a21-612aa61b85d6
reviewer_role: ARCH
reviewer_roles:
- ARCH
reviewed_artifact_version: project-control=cec9b34f8284f7b2580a7d219536d32b7b1ee849;
  soc-ap=427dd6d82caceebb7b4642e78f1dbfa96ff5fc84; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414; ai-soc-workspace=e5b7ec6d80259976b8a38e4164b5596311fed15f
server_qa:
  task_id: QA-SIMPLIFY-20261103
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: d5e9523472d7
    id: QA-SIMPLIFY-20261103_run_220816_20261103_140816
    image: qa-sandbox:20261029
    path: /tmp/qa_streamline_trusted_q0uazgt5/sandboxes/QA-SIMPLIFY-20261103_run_220816_20261103_140816
    developer_mounts: []
    container_inspect:
      id: d5e9523472d7bc417100a6b56f4d1704c2f68fbf0da6b4e1ac45b1b91aefb822
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-03T14:08:37.224970403Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_streamline_trusted_q0uazgt5/sandboxes/QA-SIMPLIFY-20261103_run_220816_20261103_140816
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/evidence/server_lock.json
    sha256: 99af8b52d9090a62129c32e89d810bb7885c49b4b64f32578518f08708021afd
  checkout_log:
    path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/evidence/checkout.log
    sha256: 1729eaad3b82f1d410cb3b19714b4b3db04deb663f4bb23e90919e949d10f6de
  runtime_log:
    path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/evidence/runtime.log
    sha256: abf8ba2e53834a234192b4ee86051249c153ac945c94fa3c8ef1babe8a43c0fe
  server_verdict:
    path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/evidence/server_verdict.json
    sha256: 84c2fed31f11d9c0dc84517e196508e6f836c4e0f333289d6ab7093d849204b6
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
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

      Ran 7 tests in 0.069s


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

      Ran 25 tests in 0.117s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_qa_pipeline.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 2.34s
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

      Ran 24 tests in 2.163s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_coord_runner.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 15.77s
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

      Ran 74 tests in 15.600s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_check_task_graph.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 0.19s
    output: 'test_check_task_graph_scale_and_params (test_check_task_graph.TestCodingStandards)
      ... ok

      test_candidate_descriptor_rejects_bogus_commits (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 10: 候选清单中填入全 0/全 1 等伪造 commit 必须报错 ... ok

      test_done_acceptance_rejects_rejected_decision (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 8: 独立评审结论为 REJECTED 必须拒绝 Done 验收 ... ok

      test_done_acceptance_rejects_self_review (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 7: 作者兼独立评审者必须拒绝 Done 验收 ... ok

      test_done_acceptance_rejects_uncompleted_predecessor (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 9: 前置任务非 Done 时，本任务不能被接受为 Done ... ok

      test_duplicate_task_id_rejected (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 2: 重复 Task ID 必须非零退出并报告错误 ... ok

      test_glob_write_scope_overlap_detected (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 3: glob 路径包含（如 ** 与具体文件）无依赖顺序时必须被拦截 ... ok

      test_readiness_blocker_on_blocked_task (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 4: 带有 blocked=true 的任务必须阻止推进到 Ready/InProgress ... ok

      test_readiness_blocker_on_bogus_commit (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 6: dispatch_binding 中填入 bogus commit 时必须拦截 ... ok

      test_readiness_blocker_on_expired_lease (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 5: 租约过期的任务必须生成 blocker ... ok

      test_twin_cards_use_full_microtask_gates (test_check_task_graph.TestTaskGraphNegativeCases)

      新任务族不得绕过结构、依赖和Ready门禁。 ... ok

      test_unquoted_colon_yaml_causes_error (test_check_task_graph.TestTaskGraphNegativeCases)

      反例 1: YAML 含未引用冒号导致解析异常，工具必须报错并定位 ... ok


      ----------------------------------------------------------------------

      Ran 12 tests in 0.010s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_coord_recovery.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 2.55s
    output: 'test_all_coord_runner_modules_comply_with_ast_standards (test_coord_recovery.ASTScaleAndParameterGateTest)
      ... ok

      test_max_parallel_implementation_allows_two_concurrent_tasks (test_coord_recovery.DualTaskParallelConcurrencyTest)
      ... ok

      test_cas_conflict_detection_p1_13 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_in_flight_revision_conflict_p1_07 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_protect_active_leases_for_running_processes_p1_10 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_reconcile_alive_running_job (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_reconcile_completed_job_from_exit_status (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_reconcile_orphan_killed_process_flags_reconcile_required_p1_09 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_record_revision_conflict_referral_p1_07 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_rescan_idempotence_p1_05 (test_coord_recovery.FiveSourceReconciliationTest)
      ... ok

      test_async_job_launch_creates_pid_and_exit_status (test_coord_recovery.JobLauncherAndPidStarttimeTest)
      ... ok

      test_get_proc_starttime_matches_proc_stat (test_coord_recovery.JobLauncherAndPidStarttimeTest)
      ... ok

      test_write_atomic_json_guarantees_file_integrity (test_coord_recovery.JobLauncherAndPidStarttimeTest)
      ... ok

      test_async_task_advances_while_long_job_running_p1_08 (test_coord_recovery.M2AsyncOrchestrationAndIdempotenceTest)
      ... ok

      test_intake_rescan_idempotence_guard_p1_05 (test_coord_recovery.M2AsyncOrchestrationAndIdempotenceTest)
      ... ok

      test_metadata_and_role_job_persistence (test_coord_recovery.StateStoreAuthoritativeRecoveryTest)
      ... ok

      test_save_and_restore_coord_state (test_coord_recovery.StateStoreAuthoritativeRecoveryTest)
      ... ok

      test_single_instance_flock_mutual_exclusion (test_coord_recovery.StateStoreAuthoritativeRecoveryTest)
      ... ok

      test_sqlite_wal_mode_and_tables_initialized (test_coord_recovery.StateStoreAuthoritativeRecoveryTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 19 tests in 1.727s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_phase1_intake_acceptance.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 1.61s
    output: 'test_all_acceptance_functions_comply_with_ast_limits (test_phase1_intake_acceptance.TestAcceptanceSuiteInvariants)
      ... ok

      test_p1_03_approved_feature_scope_dispatches_while_unapproved_blocked (test_phase1_intake_acceptance.TestPhase1ApprovalAndAntiForgery)
      ... ok

      test_p1_18_partial_batch_approval_and_demand_only_confirmation (test_phase1_intake_acceptance.TestPhase1ApprovalAndAntiForgery)
      ... ok

      test_p1_19_anti_forgery_rejects_bogus_actors_stale_rev_and_fuzzy_prose (test_phase1_intake_acceptance.TestPhase1ApprovalAndAntiForgery)
      ... ok

      test_p1_05_intake_rescan_and_renotify_idempotence (test_phase1_intake_acceptance.TestPhase1AsyncOrchestrationAndIdempotence)
      ... ok

      test_p1_07_higher_revision_in_flight_conflict_delegation (test_phase1_intake_acceptance.TestPhase1AsyncOrchestrationAndIdempotence)
      ... ok

      test_p1_08_async_long_running_job_allows_second_task_advancement (test_phase1_intake_acceptance.TestPhase1AsyncOrchestrationAndIdempotence)
      ... ok

      test_p1_20_reordered_input_reuses_approvals_while_substantive_bump_requires_fresh
      (test_phase1_intake_acceptance.TestPhase1AsyncOrchestrationAndIdempotence) ...
      ok

      test_p1_11_exit_code_zero_without_evidence_or_qa_rejection_blocked (test_phase1_intake_acceptance.TestPhase1ExecutionGatesAndLiveDrill)
      ... ok

      test_p1_12_unpushed_candidate_and_fake_qa_subagent_rejected (test_phase1_intake_acceptance.TestPhase1ExecutionGatesAndLiveDrill)
      ... ok

      test_p1_15_live_drill_end_to_end_verification (test_phase1_intake_acceptance.TestPhase1ExecutionGatesAndLiveDrill)
      ... ok

      test_p1_01_batch_markdown_generates_unique_yamls_and_preserves_contracts (test_phase1_intake_acceptance.TestPhase1IntakeAndSecurity)
      ... ok

      test_p1_06_tampered_content_and_schema_version_isolated_from_valid_items (test_phase1_intake_acceptance.TestPhase1IntakeAndSecurity)
      ... ok

      test_p1_16_delete_or_disable_preserves_in_flight_and_blocks_shell_and_escape
      (test_phase1_intake_acceptance.TestPhase1IntakeAndSecurity) ... ok

      test_p1_09_timeout_and_crash_reconciliation_via_dispatch_key (test_phase1_intake_acceptance.TestPhase1ReconciliationAndConcurrency)
      ... ok

      test_p1_10_single_instance_flock_and_active_lease_protection (test_phase1_intake_acceptance.TestPhase1ReconciliationAndConcurrency)
      ... ok

      test_p1_13_cas_optimistic_concurrency_blocks_user_overwrite (test_phase1_intake_acceptance.TestPhase1ReconciliationAndConcurrency)
      ... ok

      test_p1_02_ambiguous_requirement_triggers_pm_arch_clarification (test_phase1_intake_acceptance.TestPhase1TriageAndMultiRole)
      ... ok

      test_p1_04_issue_root_cause_triage_routing_to_owner (test_phase1_intake_acceptance.TestPhase1TriageAndMultiRole)
      ... ok

      test_p1_17_single_demand_multi_role_split_preserves_demand_id (test_phase1_intake_acceptance.TestPhase1TriageAndMultiRole)
      ... ok


      ----------------------------------------------------------------------

      Ran 20 tests in 1.428s


      OK'
  - command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools -p test_coord_systemd_service.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 0.61s
    output: 'test_systemd_tools_comply_with_ast_standards (test_coord_systemd_service.ASTScaleAndParameterGateTest)
      ... ok

      test_absent_crontab_reports_clean (test_coord_systemd_service.CrontabIsolationGateTest)
      ... ok

      test_crontab_command_failure_reports_not_clean (test_coord_systemd_service.CrontabIsolationGateTest)
      ... ok

      test_forbidden_crontab_entry_detected (test_coord_systemd_service.CrontabIsolationGateTest)
      ... ok

      test_missing_crontab_executable_reports_clean (test_coord_systemd_service.CrontabIsolationGateTest)
      ... ok

      test_real_crontab_isolation (test_coord_systemd_service.CrontabIsolationGateTest)
      ... ok

      test_p1_14_zero_idle_model_consumption_across_consecutive_cycles (test_coord_systemd_service.P1_14_ZeroIdleModelConsumptionAndRecoveryTest)
      ... ok

      test_service_process_sigterm_stop_and_restart_recovery (test_coord_systemd_service.P1_14_ZeroIdleModelConsumptionAndRecoveryTest)
      ... ok

      test_check_user_linger_detection (test_coord_systemd_service.ServiceControllerLifecycleTest)
      ... ok

      test_control_service_actions (test_coord_systemd_service.ServiceControllerLifecycleTest)
      ... ok

      test_get_service_status_installed_and_missing (test_coord_systemd_service.ServiceControllerLifecycleTest)
      ... ok

      test_install_and_uninstall_lifecycle (test_coord_systemd_service.ServiceControllerLifecycleTest)
      ... ok

      test_required_sections_present (test_coord_systemd_service.SystemdUnitFileStructureTest)
      ... ok

      test_service_exec_and_restart_directives (test_coord_systemd_service.SystemdUnitFileStructureTest)
      ... ok

      test_working_directory_and_environment (test_coord_systemd_service.SystemdUnitFileStructureTest)
      ... ok


      ----------------------------------------------------------------------

      Ran 15 tests in 0.384s


      OK'
  - command: 'PYTHONDONTWRITEBYTECODE=1 python3 -c ''from pathlib import Path; import
      hashlib,json; r=Path(''"''"''ai-soc-workspace''"''"''); c=Path(''"''"''project-control''"''"'');
      d=json.loads((r/''"''"''workspace.json''"''"'').read_text()); assert next(x[''"''"''commit''"''"'']
      for x in d[''"''"''repositories''"''"''] if x[''"''"''path''"''"'']==''"''"''project-control''"''"'')==''"''"''cec9b34f8284f7b2580a7d219536d32b7b1ee849''"''"'';
      assert (r/''"''"''AGENTS.md''"''"'').read_bytes()==(c/''"''"''docs/evidence/qa_streamline_20261103/docs/run_01/AGENTS.md.candidate''"''"'').read_bytes();
      m=json.loads((c/''"''"''docs/evidence/qa_streamline_20261103/author/run_01/source_manifest.json''"''"'').read_text());
      assert all(hashlib.sha256((c/x[''"''"''path''"''"'']).read_bytes()).hexdigest()==x[''"''"''sha256''"''"'']
      for x in m[''"''"''files''"''"'']); print(''"''"''Root AGENTS, published recovery
      pin, and 9-file source manifest: PASS''"''"'')'''
    exit_code: '0'
    subpath: ''
    duration: 0.11s
    output: 'Root AGENTS, published recovery pin, and 9-file source manifest: PASS'
  passed: true
  timestamp: '2026-11-03T14:09:03.537002+00:00'
  path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/evidence/server_qa.json
  sha256: 1583e35473b5d43540c25ffdb1aa610c596bcd49242177149a683f1f4c097a6a
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/reviews/495ba427603b44a7be622474f69290f7/codex.jsonl
  sha256: 0691826130d976bbea0961853dcf2726f42dca54fa1389eb380fa15bc672d16b
reviewed_artifacts:
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/request.json
  sha256: 6102434f06bfcea86598ca9c265d58a984295d7c5e5b9006c8fc0ab2b833efb9
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/diffs/project-control.patch
  sha256: fa0742860b3408b73232e784a3dc4a50550204ed5ca0b3ff00fe167ba3bba108
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_streamline_trusted_q0uazgt5/runs/report_review_02/diffs/ai-soc-workspace.patch
  sha256: 9d2ea26c18f805a4d02caab86d15b8be56c8ac079157ed695d25c95511510efc
verification_scope: Bounded QA policy, runner, closure, and template simplification
  with legacy behavior retained until explicit migration; no scheduler rewrite. The
  pinned candidate and its diff match the report. Separate sandbox evidence binds
  the candidate commit and records all eight required suites passing (196 tests),
  plus the root recovery pin, AGENTS, and source hash check. Positive, negative, and
  recovery coverage is present. HIL, MCU builds, and live scheduler deployment are
  excluded for this policy-tool change.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The bundle SHA256 matches 428c5ca1f8e4a01564950a9dc554f7bc6dc8bed060480a25de8af69c6f778178. The primary QA report SHA256 independently recomputes to 6b0a1568b8819f60cd99f3a20aa72626a9a39d9517905f29239b2b0edc27a297. Its findings and scope are consistent with the pinned candidate and separate frozen sandbox evidence.
