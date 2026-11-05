```yaml
task_id: AUTO-07
task_revision: 1
candidate_commit: b5deb3be960e1a68e8b79e76051d845bd91f7af5
role: QA
decision: REJECTED
summary: 已核对锁定候选与冻结证据。指定沙箱检查通过；但源码存在与接受条款冲突的启动信号竞态。工作区为只读，无法将评审说明和最终 JSON 分别落盘，审阅结论载于本对象。
findings:
- 阻断：接受范围要求在途任务、恢复记录与单实例锁保持一致。runner.py 的 run_daemon() 在 acquire_process_lock() 之前注册
  SIGINT/SIGTERM 处理器；若信号在取得锁前到达，_signal_handler() 会直接调用 save_checkpoint()，写入 SQLite
  与检查点文件，却未持有单实例锁。另一运行实例持锁时，这可能覆盖其恢复状态。对应位置：runner.py 的 run_daemon() 与 _signal_handler()。
accepted_scope: CoordRunner restore_from_checkpoint/step 自动收件、幂等账本、TaskLinkUpdate
  的 arch_breakdown revision 与摘要同步、FEAT-20261104-001/002 r4 对齐，以及指定单元/集成检查。主机上的 systemd
  用户服务激活明确排除。bundle SHA256、差异、声明产物、沙箱 verdict 与 runtime log 的摘要均与索引一致；冻结日志记录收件扫描 errors
  为空且 126 项测试通过。
unexecuted: []
actual_session: 01a1a9f2-bddc-7e70-9c17-63f31d335bf9
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=b5deb3be960e1a68e8b79e76051d845bd91f7af5;
  soc-ap=79932746d225bb115010c5545ef3f7499482e137; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: AUTO-07
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: bc3398064d3a
    id: AUTO-07_run_122144_20261105_042144
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144
    developer_mounts: []
    container_inspect:
      id: bc3398064d3aa040a7dcd4dc3de6c94d7cafd134fdac9e51b2f4294ee9b1c914
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-05T04:22:36.658783278Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_AUTO-07_b9afc5rp/evidence/server_lock.json
    sha256: ba462b929215eb89faa40f1613902f2d8995f0e63f9a32876e26a0326cf8bad4
  checkout_log:
    path: /tmp/qa_AUTO-07_b9afc5rp/evidence/checkout.log
    sha256: 8d2bb6183a109a367900166cf4ad75b6d63ee049f9da5176d9d3e3d20c5f5f04
  runtime_log:
    path: /tmp/qa_AUTO-07_b9afc5rp/evidence/runtime.log
    sha256: dd2809a4f8defb6adadfaae503434fd6b5f1e85cc8cc39c6d50c5720ba02cc2d
  server_verdict:
    path: /tmp/qa_AUTO-07_b9afc5rp/evidence/server_verdict.json
    sha256: f96463f95ba8b68e786ab3a1f9a4fc81e4b55080a2716fd4188f8e81914bc60d
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: python3 -m tools.coord_runner --intake-scan && python3 -m unittest tools/test_work_intake.py
      tools/test_coord_runner.py tools/test_coord_recovery.py tools/test_coord_systemd_service.py
      -v
    exit_code: '0'
    subpath: project-control
    duration: 30.75s
    output: "{\n  \"submissions_count\": 5,\n  \"generated_files\": [],\n  \"valid_records\"\
      : [\n    \"FEAT-20261104-001\",\n    \"FEAT-20261104-002\",\n    \"FEAT-INTAKE-20261103-001\"\
      ,\n    \"ISS-20261105-001\",\n    \"ISS-20261105-002\",\n    \"ISS-20261105-003\"\
      ,\n    \"ISS-20261105-004\",\n    \"REQ-20261105-001\"\n  ],\n  \"idempotent_records_count\"\
      : 8,\n  \"errors\": [],\n  \"notices\": [\n    {\n      \"code\": \"IN_FLIGHT_PRESERVED_ON_INTAKE_REMOVAL\"\
      ,\n      \"item_id\": \"['PILOT-REQ-06']\",\n      \"task_ids\": [\n       \
      \ \"MS-22\"\n      ],\n      \"action\": \"preserve_in_flight_notify_coord\"\
      ,\n      \"message\": \"Intake file missing for active task MS-22; in-flight\
      \ work NOT auto-cancelled\"\n    }\n  ]\n}\n\ntest_canonical_workspace_approval_verified\
      \ (tools.test_work_intake.ApprovalGuardAntiForgeryTest) ... ok\ntest_p1_03_and_p1_18_partial_batch_subscope_and_demand_only_split\
      \ (tools.test_work_intake.ApprovalGuardAntiForgeryTest) ... ok\ntest_p1_19_rejects_forged_actor_stale_rev_tampered_hash_and_prose_keywords\
      \ (tools.test_work_intake.ApprovalGuardAntiForgeryTest) ... ok\ntest_cas_rejects_invalid_digest_missing_file_and_duplicate_exclusive\
      \ (tools.test_work_intake.CasWriterTest) ... ok\ntest_read_with_digest_and_write_cas_positive\
      \ (tools.test_work_intake.CasWriterTest) ... ok\ntest_write_cas_rejects_concurrent_edit_and_preserves_user_file\
      \ (tools.test_work_intake.CasWriterTest) ... ok\ntest_committed_m1_live_drill_evidence_verified\
      \ (tools.test_work_intake.RoleAdapterAndGatesTest) ... ok\ntest_coordinate_readonly_resume_and_zero_call_noop\
      \ (tools.test_work_intake.RoleAdapterAndGatesTest) ... ok\ntest_p1_02_p1_04_p1_17_routing_and_multi_role_split\
      \ (tools.test_work_intake.RoleAdapterAndGatesTest) ... ok\ntest_p1_11_p1_12_p1_15_candidate_remote_reconcile_and_codex_reviewer_gates\
      \ (tools.test_work_intake.RoleAdapterAndGatesTest) ... ok\ntest_p1_16_boundary_revert_and_forbidden_repo_block\
      \ (tools.test_work_intake.RoleAdapterAndGatesTest) ... ok\ntest_canonical_workspace_intake_and_disabled_examples\
      \ (tools.test_work_intake.WorkIntakeBatchAndIsolationTest) ... ok\ntest_link_tasks_with_arch_breakdown_updates_revision_and_digest_ledger\
      \ (tools.test_work_intake.WorkIntakeBatchAndIsolationTest)\n验证 TaskLinkUpdate\
      \ 写入 arch_breakdown 时自动递增 revision 并同步更新 .intake_digests.json 账本。 ... ok\ntest_p1_01_batch_md_generates_unique_three_category_yamls_and_links\
      \ (tools.test_work_intake.WorkIntakeBatchAndIsolationTest) ... ok\ntest_p1_06_tampered_same_revision_and_corrupt_records_isolated\
      \ (tools.test_work_intake.WorkIntakeBatchAndIsolationTest) ... ok\ntest_p1_16_disabled_or_deleted_preserves_in_flight_and_blocks_shell_or_forbidden_scope\
      \ (tools.test_work_intake.WorkIntakeBatchAndIsolationTest) ... ok\ntest_checkpoint_corrupt_defense\
      \ (tools.test_coord_runner.CheckpointAndRecoveryTest) ... ok\ntest_checkpoint_roundtrip\
      \ (tools.test_coord_runner.CheckpointAndRecoveryTest) ... ok\ntest_crash_and_restart_recovery_drill\
      \ (tools.test_coord_runner.CheckpointAndRecoveryTest) ... ok\ntest_crash_and_restart_recovery_drill_from_disk_sandbox_qa\
      \ (tools.test_coord_runner.CheckpointAndRecoveryTest) ... ok\ntest_process_level_kill_and_restart_recovery_drill\
      \ (tools.test_coord_runner.CheckpointAndRecoveryTest) ... ok\ntest_codex_auth_failure_blocked\
      \ (tools.test_coord_runner.CodexAndSandboxIsolationGateTest) ... ok\ntest_codex_unavailable_blocked\
      \ (tools.test_coord_runner.CodexAndSandboxIsolationGateTest) ... ok\ntest_docker_container_sandbox_passed\
      \ (tools.test_coord_runner.CodexAndSandboxIsolationGateTest) ... ok\ntest_plain_directory_sandbox_rejected\
      \ (tools.test_coord_runner.CodexAndSandboxIsolationGateTest) ... ok\ntest_daemon_signal_handling\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_default_agent_executor_invokes_role_adapter_with_approval\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_default_agent_executor_rejects_unapproved_or_unpushed_candidate\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_ensure_qa_report_review_preexisting_invalid_review_rejected\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_ensure_qa_report_review_preexisting_valid_review_accepted\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_execute_review_phase_dedicated_reviewer_typeerror_fails_without_fallback\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_execute_review_phase_multi_role\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_execute_review_phase_preexisting_invalid_report_review_rejected\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_execute_review_phase_qa_report_review_rejected\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_execute_review_phase_valid_report_review_approved_to_done\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_invoke_report_reviewer_passes_req_dict\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_missing_executor_fails_closed\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_production_executors_wiring\
      \ (tools.test_coord_runner.ExecutionModesTest) ... ok\ntest_run_once_mode (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_run_tasks_finite_mode (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_runner_resolve_qa_report_missing_entry_path_rejected (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_runner_resolve_qa_report_missing_entry_sha_rejected (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_runner_resolve_qa_report_missing_file_rejected (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_runner_resolve_qa_report_prefill_mismatch_rejected (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_sandbox_qa_restart_recovery_progresses (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_uart_conflict_rolls_back_implementation_lease (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_verify_server_commit_variants (tools.test_coord_runner.ExecutionModesTest)\
      \ ... ok\ntest_exclusive_device_conflict_uart (tools.test_coord_runner.LeaseAndExclusivityTest)\
      \ ... ok\ntest_implementation_concurrency_limit (tools.test_coord_runner.LeaseAndExclusivityTest)\
      \ ... ok\ntest_lease_expiration_and_prune (tools.test_coord_runner.LeaseAndExclusivityTest)\
      \ ... ok\ntest_lease_renewal_and_expired_renewal_fails (tools.test_coord_runner.LeaseAndExclusivityTest)\
      \ ... ok\ntest_release_lease_frees_resource (tools.test_coord_runner.LeaseAndExclusivityTest)\
      \ ... ok\ntest_legacy_queue_and_twin_tasks_explicitly_isolated (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest)\
      \ ... ok\ntest_module_cli_intake_scan_runs_cleanly (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest)\
      \ ... ok\ntest_scheduler_enforces_done_acceptance_errors_on_predecessors (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest)\
      \ ... ok\ntest_step_and_restore_checkpoints_auto_scan_intake_idempotently (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest)\n\
      验证 restore_from_checkpoint 与 step 检查点自动扫描人工收件、生成一次分类 YAML 且连续轮询幂等零空耗。 ... ok\n\
      test_step_isolates_corrupt_submission_without_blocking_valid_intake_or_inflight\
      \ (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest)\n验证单份损坏收件文件在 step\
      \ 检查点被隔离至 errors，不阻断合法提交单收件或在途任务推进。 ... ok\ntest_subagent_platform_and_planned_alias_rejected_in_state_machine\
      \ (tools.test_coord_runner.M1QueueIsolationAndDoneGateTest) ... ok\ntest_python_functions_scale_and_parameters_limits\
      \ (tools.test_coord_runner.MethodologicalInvariantsTest) ... ok\ntest_author_self_review_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_candidate_commit_validation\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_any_review_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_entry_missing_report_sha\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_missing_report_review\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_file_not_found_on_disk\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_file_tampered_or_sha_mismatch\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_review_by_author\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_review_missing_report_path_or_sha\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_review_self_reviewed\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_review_sha_mismatch\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_qa_report_review_unapproved\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_done_rejected_when_required_role_missing\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_evidence_based_remediation_validation\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_fake_done_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_max_corrections_exceeded_escalation\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_developer_mounts_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_failure_triggers_remediation\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_commit_mismatch_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_invalid_sandbox_kind_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_missing_server_qa_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_missing_task_revision_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_string_false_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_qa_verdict_task_revision_mismatch_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_remediation_missing_evidence_rejected\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_review_rejection_triggers_remediation\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_state_machine_invalid_transition\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_state_machine_positive_flow\
      \ (tools.test_coord_runner.StateMachineAndRemediationTest) ... ok\ntest_blocked_task_filtered\
      \ (tools.test_coord_runner.TaskSelectionAndSchedulingTest) ... ok\ntest_bootstrap_prioritized_over_order\
      \ (tools.test_coord_runner.TaskSelectionAndSchedulingTest) ... ok\ntest_completed_tasks_filtered\
      \ (tools.test_coord_runner.TaskSelectionAndSchedulingTest) ... ok\ntest_resource_unavailable_blocked\
      \ (tools.test_coord_runner.TaskSelectionAndSchedulingTest) ... ok\ntest_unmet_dependencies_blocked\
      \ (tools.test_coord_runner.TaskSelectionAndSchedulingTest) ... ok\ntest_all_coord_runner_modules_comply_with_ast_standards\
      \ (tools.test_coord_recovery.ASTScaleAndParameterGateTest) ... ok\ntest_max_parallel_implementation_allows_two_concurrent_tasks\
      \ (tools.test_coord_recovery.DualTaskParallelConcurrencyTest) ... ok\ntest_cas_conflict_detection_p1_13\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_in_flight_revision_conflict_p1_07\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_protect_active_leases_for_running_processes_p1_10\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_reconcile_alive_running_job\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_reconcile_completed_job_from_exit_status\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_reconcile_orphan_killed_process_flags_reconcile_required_p1_09\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_record_revision_conflict_referral_p1_07\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_rescan_idempotence_p1_05\
      \ (tools.test_coord_recovery.FiveSourceReconciliationTest) ... ok\ntest_async_job_launch_creates_pid_and_exit_status\
      \ (tools.test_coord_recovery.JobLauncherAndPidStarttimeTest) ... ok\ntest_get_proc_starttime_matches_proc_stat\
      \ (tools.test_coord_recovery.JobLauncherAndPidStarttimeTest) ... ok\ntest_write_atomic_json_guarantees_file_integrity\
      \ (tools.test_coord_recovery.JobLauncherAndPidStarttimeTest) ... ok\ntest_async_task_advances_while_long_job_running_p1_08\
      \ (tools.test_coord_recovery.M2AsyncOrchestrationAndIdempotenceTest) ... ok\n\
      test_intake_rescan_idempotence_guard_p1_05 (tools.test_coord_recovery.M2AsyncOrchestrationAndIdempotenceTest)\
      \ ... ok\ntest_metadata_and_role_job_persistence (tools.test_coord_recovery.StateStoreAuthoritativeRecoveryTest)\
      \ ... ok\ntest_save_and_restore_coord_state (tools.test_coord_recovery.StateStoreAuthoritativeRecoveryTest)\
      \ ... ok\ntest_single_instance_flock_mutual_exclusion (tools.test_coord_recovery.StateStoreAuthoritativeRecoveryTest)\
      \ ... ok\ntest_sqlite_wal_mode_and_tables_initialized (tools.test_coord_recovery.StateStoreAuthoritativeRecoveryTest)\
      \ ... ok\ntest_systemd_tools_comply_with_ast_standards (tools.test_coord_systemd_service.ASTScaleAndParameterGateTest)\
      \ ... ok\ntest_absent_crontab_reports_clean (tools.test_coord_systemd_service.CrontabIsolationGateTest)\
      \ ... ok\ntest_crontab_command_failure_reports_not_clean (tools.test_coord_systemd_service.CrontabIsolationGateTest)\
      \ ... ok\ntest_forbidden_crontab_entry_detected (tools.test_coord_systemd_service.CrontabIsolationGateTest)\
      \ ... ok\ntest_missing_crontab_executable_reports_clean (tools.test_coord_systemd_service.CrontabIsolationGateTest)\
      \ ... ok\ntest_real_crontab_isolation (tools.test_coord_systemd_service.CrontabIsolationGateTest)\
      \ ... ok\ntest_p1_14_zero_idle_model_consumption_across_consecutive_cycles (tools.test_coord_systemd_service.P1_14_ZeroIdleModelConsumptionAndRecoveryTest)\
      \ ... ok\ntest_service_process_sigterm_stop_and_restart_recovery (tools.test_coord_systemd_service.P1_14_ZeroIdleModelConsumptionAndRecoveryTest)\
      \ ... ok\ntest_check_user_linger_detection (tools.test_coord_systemd_service.ServiceControllerLifecycleTest)\
      \ ... ok\ntest_control_service_actions (tools.test_coord_systemd_service.ServiceControllerLifecycleTest)\
      \ ... ok\ntest_get_service_status_installed_and_missing (tools.test_coord_systemd_service.ServiceControllerLifecycleTest)\
      \ ... ok\ntest_install_and_uninstall_lifecycle (tools.test_coord_systemd_service.ServiceControllerLifecycleTest)\
      \ ... ok\ntest_required_sections_present (tools.test_coord_systemd_service.SystemdUnitFileStructureTest)\
      \ ... ok\ntest_service_exec_and_restart_directives (tools.test_coord_systemd_service.SystemdUnitFileStructureTest)\
      \ ... ok\ntest_working_directory_and_environment (tools.test_coord_systemd_service.SystemdUnitFileStructureTest)\
      \ ... ok\n\n----------------------------------------------------------------------\n\
      Ran 126 tests in 24.788s\n\nOK"
  passed: true
  timestamp: '2026-11-05T04:23:10.033615+00:00'
  path: /tmp/qa_AUTO-07_b9afc5rp/evidence/server_qa.json
  sha256: 7e5bd82db32af5c4973ea57c0d79d2cfc12122912b6f5111cb00f0267311f259
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_AUTO-07_b9afc5rp/reviews/d4f84deabbed41d88bbb985b81947235/codex.jsonl
  sha256: d895f0aca96519ba31b03eede19b9dc1de6b69e6d867b0f3a27ab486f3cfaccb
reviewed_artifacts:
- path: /tmp/qa_AUTO-07_b9afc5rp/request.json
  sha256: 1085add651af3f68eb929cfbae7a6b8e5c43dde0ce379b6b1182ba00a43f7448
- path: /tmp/qa_AUTO-07_b9afc5rp/diffs/project-control.patch
  sha256: 56d4df5e2b50a27cd5bf4a8c82632c160f4d42432b44d89b72d923b8390016c3
- path: /tmp/qa_AUTO-07_b9afc5rp/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_AUTO-07_b9afc5rp/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_AUTO-07_b9afc5rp/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/tools/coord_runner/runner.py
  sha256: 8cf73e3d75f6c646c940bc20bb8752f568bf3cb0a51fb798e64becfb27166fb2
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/tools/coord_runner/work_intake.py
  sha256: f9b4206f2bbda4240c3c1e4bcd6b44a792c5e90d0531a31e0bfcb77196d47680
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/tools/test_coord_runner.py
  sha256: ea81077c76ca4dfd7ab70d1f79a43b419bb3120cc835dd2990cdd13ca6f360f9
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/tools/test_work_intake.py
  sha256: 54711543b89f3bce5294f71440e630f50da2fc6df8c94a661c991b214d3c3972
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/docs/work_intake/features/FEAT-20261104-001.yaml
  sha256: 65127659508f40a46a0e9a1bc018295ccafacb86cda3e1b14be987042ff3eec3
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/docs/work_intake/features/FEAT-20261104-002.yaml
  sha256: bf647d52410a52e41ad6595ede4e16515911ebfc919ba1f05e5d3d732ed124e4
- path: /tmp/qa_sandboxes/AUTO-07_run_122144_20261105_042144/project-control/docs/work_intake/.intake_digests.json
  sha256: 19a49cb3ee98fd0b367992a04db87da61d7b30dcd35d4998871352ddaa1ae46e
verification_scope: CoordRunner restore_from_checkpoint/step 自动收件、幂等账本、TaskLinkUpdate
  的 arch_breakdown revision 与摘要同步、FEAT-20261104-001/002 r4 对齐，以及指定单元/集成检查。主机上的 systemd
  用户服务激活明确排除。bundle SHA256、差异、声明产物、沙箱 verdict 与 runtime log 的摘要均与索引一致；冻结日志记录收件扫描 errors
  为空且 126 项测试通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核对锁定候选与冻结证据。指定沙箱检查通过；但源码存在与接受条款冲突的启动信号竞态。工作区为只读，无法将评审说明和最终 JSON 分别落盘，审阅结论载于本对象。
