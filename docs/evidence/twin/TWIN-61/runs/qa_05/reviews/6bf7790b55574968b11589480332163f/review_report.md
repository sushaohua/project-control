```yaml
task_id: TWIN-61
task_revision: 5
candidate_commit: ef657531b845557b6f1d0cc64786b783635446ab
role: QA
decision: BLOCKED
summary: 复验已核对本轮候选、证据索引和上一轮 QA 报告；定向变更及指定回归证据可核实。SEQ-05 新增的 3000ms 恢复时限缺少超时负例证据，无法确认该验收条件。
findings:
- 阻断：本轮新增 SEQ-05 恢复时限（T_recover ≤ 3000ms），但冻结自测只覆盖即时恢复成功；没有恢复超过 3000ms 时应判失败的负例，也没有恰好
  3000ms 边界断言。现有端到端测试虽检查 SEQ-05 通过，却未断言报告中的 recover_ms。缺少的证据关联验收主计划 T_recover=3000ms
  及接受范围所要求的超时负例；因此该项必需证据尚不能核实。
- 非阻断建议：默认断链和重连命令仍以 `|| true` 忽略失败状态，建议后续保留命令失败信息，便于诊断台架操作问题。
accepted_scope: 复验同角色上一轮 QA 报告（task_revision 4，candidate c33ae18e25806b63010f2c7aba03e3ac9a5c3f28；SHA256
  与索引一致）及整改上下文，聚焦其到本候选的 test_harness 定向增量，并核对受影响的混色权重与 SEQ-05 恢复逻辑、290 帧及复合序列脚本、冻结的指定回归证据，以及验收主计划和
  Batch PC-1 范围。覆盖软件与模拟器证据；实体硬件台架验证和 live workspace intake scan 按既有任务合同排除，不声称已通过。
unexecuted:
- SEQ-05 重连超过 3000ms 时应失败的冻结负向自测，以及 3000ms 恢复边界断言。
actual_session: 01a1aeb3-ccbc-7962-8bac-a63d17a7a9fc
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=c1d2c461aa65e6497c295843a2735d0d02ee2e2d;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=ef657531b845557b6f1d0cc64786b783635446ab
server_qa:
  task_id: TWIN-61
  task_revision: 5
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 0c07ac7542f0
    id: TWIN-61_run_103220_20261106_023220
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220
    developer_mounts: []
    container_inspect:
      id: 0c07ac7542f06fea8edb639fc14e1e265c7806eaed7ea7d17314fa410fe3eff7
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T02:32:50.952221626Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-61_nrruyghb/evidence/server_lock.json
    sha256: 9c22289d241e4af03da8d7871080fa027f33502a4229df888e2890e158abdb12
  checkout_log:
    path: /tmp/qa_TWIN-61_nrruyghb/evidence/checkout.log
    sha256: 3c3105e1c3f3df77095d60e9dc9cfc5fa540109e2f4728e2c5aa865681812f71
  runtime_log:
    path: /tmp/qa_TWIN-61_nrruyghb/evidence/runtime.log
    sha256: 5aca9aff11940b95bd1bbf2461822da39cd4481c46b87c5dce1d74bc14613e21
  server_verdict:
    path: /tmp/qa_TWIN-61_nrruyghb/evidence/server_verdict.json
    sha256: ac591e481374498d7bf991c24cd55e0aeaafe647f96722b96fd979d9383c6602
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: (cd ../project-control/tools && python3 -m unittest test_check_task_graph.py
      test_delivery_checks.py test_qa_runner.py test_qa_pipeline.py test_review_policy.py
      test_coord_recovery.py test_coord_systemd_service.py) && python3 hil/tools/debug_reconciliation_probe.py
      --self-test && python3 hil/tests/test_290_frame_burst_stress.py --self-test
      && python3 hil/tests/test_composite_lifecycle_sequences.py --self-test && !
      grep -rn "中文说明：模块辅助逻辑与状态说明" hil/ ../project-control/tools/ && echo "[PASS] code_documentation_standard.md
      check passed"
    exit_code: '0'
    subpath: test_harness
    duration: 7.03s
    output: "[PASS] debug_reconciliation_probe.py self-test suite passed (11 fixtures\
      \ generated).\n{\n  \"live_mode\": \"serial\",\n  \"serial_burst\": {\n    \"\
      expected_total_frames\": 290,\n    \"observed_mc_unique_rx_seqs\": 290,\n  \
      \  \"observed_mc_unique_tx_ack_seqs\": 290,\n    \"observed_th_unique_rx_seqs\"\
      : 145,\n    \"observed_th_unique_tx_seqs\": 145,\n    \"max_seq_observed\":\
      \ 290,\n    \"missing_seqs_count\": 0,\n    \"missing_mc_tx_ack_seqs\": [],\n\
      \    \"missing_th_rx_seqs\": [],\n    \"missing_th_tx_seqs\": [],\n    \"missing_mc_relay_rx_seqs\"\
      : [],\n    \"missing_high_seqs_256_plus\": [],\n    \"missing_th_high_seqs_256_plus\"\
      : [],\n    \"bare_adc_busy_detected\": false,\n    \"crc_err_count\": 0,\n \
      \   \"bad_frame_count\": 0,\n    \"timeout_count\": 0,\n    \"ellipsis_trunc_line_count\"\
      : 0,\n    \"mc_drop_delta\": 0,\n    \"mc_trunc_delta\": 0,\n    \"th_drop_delta\"\
      : 0,\n    \"th_trunc_delta\": 0,\n    \"passed\": true,\n    \"serial_ack_ok\"\
      : 290,\n    \"serial_error_count\": 0\n  },\n  \"passed\": true\n}\n[PASS] code_documentation_standard.md\
      \ check passed\n\n............................................................................................................................\n\
      ----------------------------------------------------------------------\nRan\
      \ 124 tests in 5.361s\n\nOK\ntest_cli_live_serial_mode_over_real_pty (__main__.Test290FrameBurstStress)\n\
      验证 `main(--live --live-mode serial --serial-dev <pty>)` 通过真实 PTY 串口描述符收发 290\
      \ 帧二进制包并通过对账。 ... ok\ntest_evaluate_burst_debug_logs_positive_290_frames (__main__.Test290FrameBurstStress)\n\
      验证正例：290 帧双向完整收发、TH 序列 100% 匹配、零错误/截断时判定通过。 ... ok\ntest_evaluate_burst_debug_logs_rejects_8bit_wrap_and_adc_pollution\
      \ (__main__.Test290FrameBurstStress)\n验证反例：当发生 8-bit 序列号回绕、裸 `adc SS_ADC_BUSY`\
      \ 污染或长行 `...` 截断时严格拦截。 ... ok\ntest_evaluate_burst_debug_logs_rejects_missing_th_or_tx_ack\
      \ (__main__.Test290FrameBurstStress)\n验证反例：缺失单帧 TH 高位序列（如 seq=289）或缺失单帧 TX ACK\
      \ 应答时必须判定失败。 ... ok\ntest_generate_290_burst_plan_covers_16bit_seq_boundary\
      \ (__main__.Test290FrameBurstStress)\n验证 290 帧突发计划完整覆盖 seq=1..290，且每帧 CRC16\
      \ 与 16位小端序列号编码准确。 ... ok\ntest_run_live_http_burst_end_to_end_with_mock_server\
      \ (__main__.Test290FrameBurstStress)\n验证 `run_live_http_burst` 无伪造 Header 驱动\
      \ 290 步 HTTP 请求并经底层串口总线闭环对账通过。 ... ok\n\n----------------------------------------------------------------------\n\
      Ran 6 tests in 0.707s\n\nOK\ntest_run_live_composite_sequences_end_to_end_with_stateful_sim\
      \ (__main__.TestCompositeLifecycleSequences)\n验证 `run_live_composite_sequences`\
      \ 配合步进时钟与断链/重连钩子完整跑通 SEQ-01..SEQ-05。 ... ok\ntest_seq01_oobe_bootid_adc_and_bed_range_gate\
      \ (__main__.TestCompositeLifecycleSequences)\n验证 SEQ-01：动态 boot_id 变化、raw_adc\
      \ 映射及 300°C 热床超量程故障降级。 ... ok\ntest_seq02_motion_and_temperature_bounds (__main__.TestCompositeLifecycleSequences)\n\
      验证 SEQ-02：归零 -> 调平 -> 点动 -> 204B 坐标查询零截断，以及喷头/热床设温边界。 ... ok\ntest_seq03_filament_save_decoupling_and_400_validation\
      \ (__main__.TestCompositeLifecycleSequences)\n验证 SEQ-03：合法槽位/动作/混色权重 10000 返回\
      \ 200，越界 slot_id=4、action=3、权重和 100/9000 返回 400。 ... ok\ntest_seq04_gcode_upload_and_two_stage_job_start\
      \ (__main__.TestCompositeLifecycleSequences)\n验证 SEQ-04：三类独立非法 G-code 上传返回 400，合法上传暂存保持\
      \ IDLE，显式启动才进入 PRINTING。 ... ok\ntest_seq05_offline_3s_sentinel_and_404_framing\
      \ (__main__.TestCompositeLifecycleSequences)\n验证 SEQ-05：断链 >=3.0s 打入 2147483646\
      \ 离线哨兵、小于 3.0s 被拒绝，且 404 帧完整。 ... ok\n\n----------------------------------------------------------------------\n\
      Ran 6 tests in 0.536s\n\nOK"
  passed: true
  timestamp: '2026-11-06T02:33:00.705331+00:00'
  path: /tmp/qa_TWIN-61_nrruyghb/evidence/server_qa.json
  sha256: 2cf04476f62ffa66f426119ad2908f956d85973e84fd8bf991240330da360389
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-61_nrruyghb/reviews/6bf7790b55574968b11589480332163f/codex.jsonl
  sha256: 61564552a7ddf2d29743b5e5c0a9c93f2f3429b3bc8b10968b10ba3c278dc54e
reviewed_artifacts:
- path: /tmp/qa_TWIN-61_nrruyghb/request.json
  sha256: 4b6cbc54fc766c0bcfa1a0c9acaa41d094f5911c931c07cf9f8dbc58a57aef24
- path: /tmp/qa_TWIN-61_nrruyghb/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_nrruyghb/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_nrruyghb/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_nrruyghb/diffs/test_harness.patch
  sha256: 5d71e7bc99e40222241cc0a1abc816fc48d21864202e02e19cc231632f9e967a
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/.gitkeep
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tools/probe_fault_injector.py
  sha256: 9e521512a762a930c9dc2553bc6ac311ce9fddf5283f59b4a675e9505f4b499e
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tools/device_discovery.py
  sha256: dd6b353b104d26d44d5f655039d51e874d4a99021861db019548f73bb05863cd
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tools/debug_reconciliation_probe.py
  sha256: b062d2dfd411e128eba7dd44f7ec54a390db908adc749700a572b3f25d2fb68d
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tools/generate_twin35_evidence_logs.py
  sha256: 85659fa939917265f7b2759c29b2245eb243811dbed1535e5032e87f601bd3cd
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_composite_lifecycle_sequences.py
  sha256: 7418a2350d79d538cc8a887639c6adefcce999741483b68bc69fd35dce0bef68
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_probe_tools.py
  sha256: 94b9b438ac69026b2fc73ce8ade21b0b0b3f7ca0d425fed87996514c5527047c
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_290_frame_burst_stress.py
  sha256: d27aa29b9c14fc61b49a119eec3da62b25aec91ee2c5a36aa5d89b5681b3667a
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_qa_e2e_hotunplug.py
  sha256: 1a4a26fae45dd83cc2c399f6de8d2c1f5682384b8022a2f9e3754500409de19a
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_qa_e2e_oobe_browser.py
  sha256: e7920cba3c569a602c3c2a74d0b9f188816718ce531855eb38b6f7b990ad70d2
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_qa_e2e_features_browser.py
  sha256: f5dd3c60d36123a86ca5aa5f446cc4e7d9f0f12195f3c3b5b87f6f4a87a39908
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/tests/test_qa_e2e_workbench_browser.py
  sha256: 7a1bf4248e20ac9a6002e306913b791ab4d58ea7afc34cd26b077e65e2dcb940
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/twin_capture/test_twin_capture.py
  sha256: 6c8d4d7f6b3f8147f2a0df127b486b2de4d100940bf5ef126b601d5029b82884
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/twin_capture/twin_capture_analyzer.py
  sha256: b662df9145ffdb2fdd0428425d48f2f6361de4f9aa8136c60c68cea46af28073
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/test_harness/hil/guides/probe_rs_hardware_fault_injection.md
  sha256: de74a7ea5888e60526b2b2a936283e71134cf737eaf6fb4163050e7efe8a6a2b
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md
  sha256: 743a773fa8c50c6815f207264c06f91c020a422e87dc3512017f412de4fbe3ac
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_qa_pipeline.py
  sha256: 979ab926d79c2ea163381f3103fc16d4585be17c832ba82dc2ead9ec08bf7299
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_coord_recovery.py
  sha256: b3ddb0ef050bb57d119cf0687db4185bcdff7d5eea745826d66fbd854ce6870b
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_review_policy.py
  sha256: a0635dcd088f166edb54a6efcd3b62996fc1cba14357ea1451d2d6fb055d802f
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_coord_runner.py
  sha256: 09e1c183a937141024b005a14874e33ef01e8d66bfe44146ef527cf007f132a4
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/push_to_server.sh
  sha256: f754bb07a28f17eae2666052c2439143ffdffa91cc3519384d65933c2fb33db4
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_qa_runner.py
  sha256: 6a489f0f2ff5855758c878f7ecb47f38c21b7fd3569dd2ed4ac334484b3ab849
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_work_intake.py
  sha256: c4792d4be989858a22f92d6901bba8e4a1973936c2273ca30ac9c53f05e5b709
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_qa_review_efficiency.py
  sha256: 231cf1e7f1da116ee6147beef102bd77a8e83f8ce61c05d07e30e2f90a180bad
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/delivery_checks.py
  sha256: 9d4ff0da07c332505070ee7d761971a0ede6a36e29b55d446e67242b6c539554
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_queue.py
  sha256: dbcb7f2f32b78c295d1d6d30180de0fd4ee98a8921c9d93ef41941c2c0a7d869
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_check_task_graph.py
  sha256: d5c0c2c1b0928743e8d89eef7b53979f0fa9c42749ffb643408d33c196525863
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_coord_systemd_service.py
  sha256: dfcbe0416cabb5da17fcaabe7b945fa84589698cf5b95bbd51b69f8812cb0b11
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_delivery_checks.py
  sha256: 649d60a424660993162cae79480ff7f530bfa50cb20a4ae632c812d600fff38b
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/check_task_graph.py
  sha256: 1018663741bdd7769bbaf780926f42021762bac24b400226c4e80f01d9faa964
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/test_phase1_intake_acceptance.py
  sha256: 5f78df8e1c363033930d6fad5e524aafe13c9aa5f7b29ed35ac57e8662bbb969
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/m2_drill.py
  sha256: 88e24f9a512ccfd60db16df80918381d0f522bc9d1dbb4c59cb11333a16b7711
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/models.py
  sha256: 38e9be75b8202c93de932fc6f1a0c28e29e85441d557630d8f41c92b7afc05b4
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/job_launcher.py
  sha256: a4c070fb1cf3463665397506b7ed47e4823008425c41cd94046de85e913b9e40
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/runner.py
  sha256: 2e2e1231b2039924a51ac0811ead8ce3efc684a61132f847770ff2280ae4125c
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/role_adapter.py
  sha256: d6d35f7d0cbd233417240fbe4ef42520236292c9868290604d8b917bfaa6928d
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/approval_guard.py
  sha256: 71ced2ab76594a254b904f8bfe126f0f5bb9ffef05f859d92de90a1859b5a42b
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/scheduler.py
  sha256: 853db45936542ac47f69f96bbc9ee205ed73867276c9be56cd6f6f9591cfb9f5
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/state_machine.py
  sha256: 74682ec0c1b4a1ff9121f6a4ac48c89521f8e320126e09c0504afdc27a8dba0b
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/work_intake.py
  sha256: 362a476fc35be051e829eed1766bdb00f4514917a45d127c3a20224020323519
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/lease_manager.py
  sha256: 46fb1c03599703d0a9ddbaf5a1a4332ba877d18de3884c1847c60a36163a75b4
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/m1_drill.py
  sha256: cb23cec7db948d8451bd9611f777644d0897e183d3c5da029dec1fd20637d9c0
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/__init__.py
  sha256: f59717dab174ec1c397bd60ad84a79038c59b9f482f72a5cfeff9a4517d3f0c0
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/reconciler.py
  sha256: 5fdbe017b3e1f2b1a2434c85ba21fb031a739b4d3997423b5568f6b63f0f3cb6
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/state_store.py
  sha256: 3a32881f7a7c6bb7737e01479340df2c6151a71f13fb25682c0cffb98b9e9c08
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/README.md
  sha256: ef38aee45e4495a8b78144db7c977053d7fa826968c1c89d3ef774c8a76a8bc5
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/codex_qa.py
  sha256: bd910bef855982c13b0d611b8d5a02d20c96fb9402dae14a65009dbb513a5658
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/errors.py
  sha256: dd022c5530e5e0d4f96282c56c86e6379cf4656d1bfb9fa459df8a5696573de2
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/checkpoint.py
  sha256: fd86711395210ed29ba7c157dd4413d9837bae420488304929ebbe47caa9e5f4
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/review_policy.py
  sha256: 2eea1498dcae66b09f9fa029750c65a4cfe9f349576e625a106c681159d33823
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/service_ctl.py
  sha256: b65764da86fbc254884600f2c330026638c4b52007436ae2b4f3d7cb4f69db1e
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/qa_contract.py
  sha256: 473e181166ff865f5fb97d36855972b9cf9a28b1ea8f39d768c3c0493a1c94f5
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/codex_adapter.py
  sha256: 5ded83b0c896c30d6f84a5ce884ecd6741e0c5c736d37c2d55c5487bbf44801a
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/cas_writer.py
  sha256: b975e69bb8876fa11038cf72671be8e1f4679f542849ff198d2cd15964f41f0e
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/__main__.py
  sha256: 7c7c832634f9676b6e512bb0beb3ee6d579f56fbc5ce04167dec4a6c225db7b0
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/coord_runner/review_bundle.py
  sha256: 90d3f8cb137f01a67f1d1c65d30832510c930f79812c24fc5ab216989e257e70
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/qa_runner/__init__.py
  sha256: 759d854b4ca8189fd5a430e7dffc324f660ee868d11b0209d32471b1cc9ba30f
- path: /tmp/qa_sandboxes/TWIN-61_run_103220_20261106_023220/project-control/tools/qa_runner/qa_runner.py
  sha256: d4ea75c06a1d4d0105e27dd9d2167ebf139a7c2188d9957a1e771efad9af09f5
verification_scope: 复验同角色上一轮 QA 报告（task_revision 4，candidate c33ae18e25806b63010f2c7aba03e3ac9a5c3f28；SHA256
  与索引一致）及整改上下文，聚焦其到本候选的 test_harness 定向增量，并核对受影响的混色权重与 SEQ-05 恢复逻辑、290 帧及复合序列脚本、冻结的指定回归证据，以及验收主计划和
  Batch PC-1 范围。覆盖软件与模拟器证据；实体硬件台架验证和 live workspace intake scan 按既有任务合同排除，不声称已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验已核对本轮候选、证据索引和上一轮 QA 报告；定向变更及指定回归证据可核实。SEQ-05 新增的 3000ms 恢复时限缺少超时负例证据，无法确认该验收条件。
