```yaml
task_id: TWIN-61
task_revision: 2
candidate_commit: 20bfa16e7381a40e895aac2ca587b56b7d4ff31d
role: QA
decision: REJECTED
summary: 复验已核对上一轮 QA 报告（SHA256 匹配）：上一候选因 unittest 导入路径错误而 BLOCKED。本轮路径已修正，冻结命令通过；但新增的
  290 帧门禁仍未满足主测试计划要求的逐帧双向序列及应答核验。
findings:
- 阻断：主测试计划 §4.2 要求 290 帧均有匹配 ACK/业务响应，且 TH 日志中的 seq=256..290 完整保真。本候选的 test_290_frame_burst_stress.py
  仅要求 MC RX 序列完整、TH RX 序列非空；未验证 TH 序列完整性或逐帧匹配应答（参见脚本约第 175–221 行）。因此日志缺少多数 TH 帧或应答仍可能通过，未符合
  290 帧验收条款。
accepted_scope: 复核 test_harness 从上一候选 9f3918a2f9fc79a683ce218436b005e593a7109b 到本候选的两个定向脚本差异；核对全量
  HIL 主测试计划、290 帧及 5 类复合序列脚本，以及 project-control/tools/** Batch PC-1 中文注释范围。冻结索引中的正向、负向、恢复和指定回归命令结果均已核查。实体硬件台架执行与
  live workspace intake scan 按任务合同排除，不视为已通过。
unexecuted: []
actual_session: 01a1ae7d-bf67-77f1-8b0b-1bf1105652f9
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=c1d2c461aa65e6497c295843a2735d0d02ee2e2d;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=20bfa16e7381a40e895aac2ca587b56b7d4ff31d
server_qa:
  task_id: TWIN-61
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 4ed2f483a3aa
    id: TWIN-61_run_093330_20261106_013330
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330
    developer_mounts: []
    container_inspect:
      id: 4ed2f483a3aaae08bc5b94a91bf367b305500cbb58afb8cb4a3cc6fe5de6675f
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T01:33:49.753616793Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-61_wou9ay1o/evidence/server_lock.json
    sha256: 1b83c5e5666e4e7c5063dce88d269c03d318e79b601b4b5efc64d08edad4cacc
  checkout_log:
    path: /tmp/qa_TWIN-61_wou9ay1o/evidence/checkout.log
    sha256: 56e5bcf340f3c08edc7750b5bb6058c0811a4737e03dccde384696271c62a1ad
  runtime_log:
    path: /tmp/qa_TWIN-61_wou9ay1o/evidence/runtime.log
    sha256: 86563e1b40d74e9f161633eda8daf50318fbd1b79ed064025c0692f5571a48d9
  server_verdict:
    path: /tmp/qa_TWIN-61_wou9ay1o/evidence/server_verdict.json
    sha256: 8af5bf2c765ee283d7425f9935dcb7608083c8ed5311db899edf2556e0d610d3
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
    duration: 6.10s
    output: '[PASS] debug_reconciliation_probe.py self-test suite passed (11 fixtures
      generated).

      [PASS] code_documentation_standard.md check passed


      ............................................................................................................................

      ----------------------------------------------------------------------

      Ran 124 tests in 4.601s


      OK

      test_evaluate_burst_debug_logs_positive_290_frames (__main__.Test290FrameBurstStress)

      验证正例：290 帧完整收发、seq=256..290 原样输出、零 CRC_ERR/BAD_FRAME/drop/trunc 时判定通过。 ... ok

      test_evaluate_burst_debug_logs_rejects_8bit_wrap_and_adc_pollution (__main__.Test290FrameBurstStress)

      验证反例：当发生 8-bit 序列号回绕、裸 `adc SS_ADC_BUSY` 污染、TIMEOUT 或长行 `...` 截断时严格拦截。 ... ok

      test_generate_290_burst_plan_covers_16bit_seq_boundary (__main__.Test290FrameBurstStress)

      验证 290 帧突发计划完整覆盖 seq=1..290，且每帧 CRC16 与 16位小端序列号编码准确。 ... ok

      test_run_live_http_burst_end_to_end_with_mock_server (__main__.Test290FrameBurstStress)

      验证 `run_live_http_burst` 端到端驱动 290 帧 HTTP 序列并调用 `evaluate_burst_debug_logs`
      校验通过。 ... ok


      ----------------------------------------------------------------------

      Ran 4 tests in 0.617s


      OK

      test_run_live_composite_sequences_end_to_end_with_mock_server (__main__.TestCompositeLifecycleSequences)

      验证 `run_live_composite_sequences` 通过本地 Mock HTTP Server 端到端驱动 SEQ-01..SEQ-05
      闭环通过。 ... ok

      test_seq01_oobe_bootid_adc_and_bed_range_gate (__main__.TestCompositeLifecycleSequences)

      验证 SEQ-01：动态 boot_id 变化、raw_adc 映射及 300°C 热床超量程故障降级。 ... ok

      test_seq02_motion_homing_leveling_jog_and_no_trunc (__main__.TestCompositeLifecycleSequences)

      验证 SEQ-02：归零 -> 调平 -> 点动 -> 204B 坐标查询零截断闭环。 ... ok

      test_seq03_filament_save_decoupling_and_400_validation (__main__.TestCompositeLifecycleSequences)

      验证 SEQ-03：保存配置固定 action=0/target=0，非法权重/槽位/动作返回 400。 ... ok

      test_seq04_gcode_upload_and_two_stage_job_start (__main__.TestCompositeLifecycleSequences)

      验证 SEQ-04：非法 G-code 上传返回 400，一键载入仅暂存不进入 PRINTING。 ... ok

      test_seq05_offline_3s_sentinel_and_404_framing (__main__.TestCompositeLifecycleSequences)

      验证 SEQ-05：断链 >=3.0s 打入 2147483646 离线哨兵，未知路由 404 Content-Length 完整。 ... ok


      ----------------------------------------------------------------------

      Ran 6 tests in 0.509s


      OK'
  passed: true
  timestamp: '2026-11-06T01:33:58.546550+00:00'
  path: /tmp/qa_TWIN-61_wou9ay1o/evidence/server_qa.json
  sha256: 49157783b538ffdf5a00cad98e7996e0a674dad4aa85009ac6de9229df15c29e
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-61_wou9ay1o/reviews/0e5299e9b25840e29beb8a4dceb3e73f/codex.jsonl
  sha256: a3bffed7ef088522608a287c0c2f917b925630e53d6aa334f2f8a9f2d0ceb840
reviewed_artifacts:
- path: /tmp/qa_TWIN-61_wou9ay1o/request.json
  sha256: e9ac42de23eea38e5e760ae990374642d59cf3fff672cdf3c606c803867c2f9e
- path: /tmp/qa_TWIN-61_wou9ay1o/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_wou9ay1o/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_wou9ay1o/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-61_wou9ay1o/diffs/test_harness.patch
  sha256: ce9fff51dc1ac3eafbbfb11f07d85f0be3d76fc349ed9c18b4675a32870610e6
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/.gitkeep
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tools/probe_fault_injector.py
  sha256: 9e521512a762a930c9dc2553bc6ac311ce9fddf5283f59b4a675e9505f4b499e
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tools/device_discovery.py
  sha256: dd6b353b104d26d44d5f655039d51e874d4a99021861db019548f73bb05863cd
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tools/debug_reconciliation_probe.py
  sha256: b062d2dfd411e128eba7dd44f7ec54a390db908adc749700a572b3f25d2fb68d
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tools/generate_twin35_evidence_logs.py
  sha256: 85659fa939917265f7b2759c29b2245eb243811dbed1535e5032e87f601bd3cd
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_composite_lifecycle_sequences.py
  sha256: bef16bd14c6ce258506771f8ea1100387851a829126b991830e25c432e4601c6
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_probe_tools.py
  sha256: 94b9b438ac69026b2fc73ce8ade21b0b0b3f7ca0d425fed87996514c5527047c
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_290_frame_burst_stress.py
  sha256: c0259740e302df96b3a12e3328fc443efbf47a90e225a16fcea4b873c58249e7
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_qa_e2e_hotunplug.py
  sha256: 1a4a26fae45dd83cc2c399f6de8d2c1f5682384b8022a2f9e3754500409de19a
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_qa_e2e_oobe_browser.py
  sha256: e7920cba3c569a602c3c2a74d0b9f188816718ce531855eb38b6f7b990ad70d2
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_qa_e2e_features_browser.py
  sha256: f5dd3c60d36123a86ca5aa5f446cc4e7d9f0f12195f3c3b5b87f6f4a87a39908
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/tests/test_qa_e2e_workbench_browser.py
  sha256: 7a1bf4248e20ac9a6002e306913b791ab4d58ea7afc34cd26b077e65e2dcb940
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/twin_capture/test_twin_capture.py
  sha256: 6c8d4d7f6b3f8147f2a0df127b486b2de4d100940bf5ef126b601d5029b82884
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/twin_capture/twin_capture_analyzer.py
  sha256: b662df9145ffdb2fdd0428425d48f2f6361de4f9aa8136c60c68cea46af28073
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/test_harness/hil/guides/probe_rs_hardware_fault_injection.md
  sha256: de74a7ea5888e60526b2b2a936283e71134cf737eaf6fb4163050e7efe8a6a2b
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/docs/planning/hil_full_acceptance_master_plan_20261105.md
  sha256: 743a773fa8c50c6815f207264c06f91c020a422e87dc3512017f412de4fbe3ac
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_qa_pipeline.py
  sha256: 979ab926d79c2ea163381f3103fc16d4585be17c832ba82dc2ead9ec08bf7299
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_coord_recovery.py
  sha256: b3ddb0ef050bb57d119cf0687db4185bcdff7d5eea745826d66fbd854ce6870b
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_review_policy.py
  sha256: a0635dcd088f166edb54a6efcd3b62996fc1cba14357ea1451d2d6fb055d802f
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_coord_runner.py
  sha256: 09e1c183a937141024b005a14874e33ef01e8d66bfe44146ef527cf007f132a4
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/push_to_server.sh
  sha256: f754bb07a28f17eae2666052c2439143ffdffa91cc3519384d65933c2fb33db4
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_qa_runner.py
  sha256: 6a489f0f2ff5855758c878f7ecb47f38c21b7fd3569dd2ed4ac334484b3ab849
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_work_intake.py
  sha256: c4792d4be989858a22f92d6901bba8e4a1973936c2273ca30ac9c53f05e5b709
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_qa_review_efficiency.py
  sha256: 231cf1e7f1da116ee6147beef102bd77a8e83f8ce61c05d07e30e2f90a180bad
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/delivery_checks.py
  sha256: 9d4ff0da07c332505070ee7d761971a0ede6a36e29b55d446e67242b6c539554
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_queue.py
  sha256: dbcb7f2f32b78c295d1d6d30180de0fd4ee98a8921c9d93ef41941c2c0a7d869
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_check_task_graph.py
  sha256: d5c0c2c1b0928743e8d89eef7b53979f0fa9c42749ffb643408d33c196525863
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_coord_systemd_service.py
  sha256: dfcbe0416cabb5da17fcaabe7b945fa84589698cf5b95bbd51b69f8812cb0b11
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_delivery_checks.py
  sha256: 649d60a424660993162cae79480ff7f530bfa50cb20a4ae632c812d600fff38b
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/check_task_graph.py
  sha256: 1018663741bdd7769bbaf780926f42021762bac24b400226c4e80f01d9faa964
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/test_phase1_intake_acceptance.py
  sha256: 5f78df8e1c363033930d6fad5e524aafe13c9aa5f7b29ed35ac57e8662bbb969
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/m2_drill.py
  sha256: 88e24f9a512ccfd60db16df80918381d0f522bc9d1dbb4c59cb11333a16b7711
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/models.py
  sha256: 38e9be75b8202c93de932fc6f1a0c28e29e85441d557630d8f41c92b7afc05b4
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/job_launcher.py
  sha256: a4c070fb1cf3463665397506b7ed47e4823008425c41cd94046de85e913b9e40
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/runner.py
  sha256: 2e2e1231b2039924a51ac0811ead8ce3efc684a61132f847770ff2280ae4125c
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/role_adapter.py
  sha256: d6d35f7d0cbd233417240fbe4ef42520236292c9868290604d8b917bfaa6928d
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/approval_guard.py
  sha256: 71ced2ab76594a254b904f8bfe126f0f5bb9ffef05f859d92de90a1859b5a42b
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/scheduler.py
  sha256: 853db45936542ac47f69f96bbc9ee205ed73867276c9be56cd6f6f9591cfb9f5
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/state_machine.py
  sha256: 74682ec0c1b4a1ff9121f6a4ac48c89521f8e320126e09c0504afdc27a8dba0b
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/work_intake.py
  sha256: 362a476fc35be051e829eed1766bdb00f4514917a45d127c3a20224020323519
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/lease_manager.py
  sha256: 46fb1c03599703d0a9ddbaf5a1a4332ba877d18de3884c1847c60a36163a75b4
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/m1_drill.py
  sha256: cb23cec7db948d8451bd9611f777644d0897e183d3c5da029dec1fd20637d9c0
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/__init__.py
  sha256: f59717dab174ec1c397bd60ad84a79038c59b9f482f72a5cfeff9a4517d3f0c0
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/reconciler.py
  sha256: 5fdbe017b3e1f2b1a2434c85ba21fb031a739b4d3997423b5568f6b63f0f3cb6
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/state_store.py
  sha256: 3a32881f7a7c6bb7737e01479340df2c6151a71f13fb25682c0cffb98b9e9c08
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/README.md
  sha256: ef38aee45e4495a8b78144db7c977053d7fa826968c1c89d3ef774c8a76a8bc5
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/codex_qa.py
  sha256: bd910bef855982c13b0d611b8d5a02d20c96fb9402dae14a65009dbb513a5658
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/errors.py
  sha256: dd022c5530e5e0d4f96282c56c86e6379cf4656d1bfb9fa459df8a5696573de2
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/checkpoint.py
  sha256: fd86711395210ed29ba7c157dd4413d9837bae420488304929ebbe47caa9e5f4
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/review_policy.py
  sha256: 2eea1498dcae66b09f9fa029750c65a4cfe9f349576e625a106c681159d33823
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/service_ctl.py
  sha256: b65764da86fbc254884600f2c330026638c4b52007436ae2b4f3d7cb4f69db1e
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/qa_contract.py
  sha256: 473e181166ff865f5fb97d36855972b9cf9a28b1ea8f39d768c3c0493a1c94f5
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/codex_adapter.py
  sha256: 5ded83b0c896c30d6f84a5ce884ecd6741e0c5c736d37c2d55c5487bbf44801a
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/cas_writer.py
  sha256: b975e69bb8876fa11038cf72671be8e1f4679f542849ff198d2cd15964f41f0e
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/__main__.py
  sha256: 7c7c832634f9676b6e512bb0beb3ee6d579f56fbc5ce04167dec4a6c225db7b0
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/coord_runner/review_bundle.py
  sha256: 90d3f8cb137f01a67f1d1c65d30832510c930f79812c24fc5ab216989e257e70
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/qa_runner/__init__.py
  sha256: 759d854b4ca8189fd5a430e7dffc324f660ee868d11b0209d32471b1cc9ba30f
- path: /tmp/qa_sandboxes/TWIN-61_run_093330_20261106_013330/project-control/tools/qa_runner/qa_runner.py
  sha256: d4ea75c06a1d4d0105e27dd9d2167ebf139a7c2188d9957a1e771efad9af09f5
verification_scope: 复核 test_harness 从上一候选 9f3918a2f9fc79a683ce218436b005e593a7109b
  到本候选的两个定向脚本差异；核对全量 HIL 主测试计划、290 帧及 5 类复合序列脚本，以及 project-control/tools/** Batch
  PC-1 中文注释范围。冻结索引中的正向、负向、恢复和指定回归命令结果均已核查。实体硬件台架执行与 live workspace intake scan 按任务合同排除，不视为已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验已核对上一轮 QA 报告（SHA256 匹配）：上一候选因 unittest 导入路径错误而 BLOCKED。本轮路径已修正，冻结命令通过；但新增的 290 帧门禁仍未满足主测试计划要求的逐帧双向序列及应答核验。
