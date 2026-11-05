```yaml
task_id: TWIN-46
task_revision: 1
candidate_commit: 108158318581df366d133f556343d5367bd30cff
role: QA
decision: REJECTED
summary: The pinned bundle and recorded sandbox run are valid, and fixture-based positive,
  negative, offline, and recovery checks pass. The live sim path does not perform
  the required five-category reconciliation against live AP state, and offline validation
  accepts invalid sentinel/status combinations.
findings:
- The live `--ap-url` path fabricates MC/TH logs with `build_default_mc_ok_log()`
  and `build_default_th_ok_log()`. Its five-category positive report uses a default
  AP snapshot for temperature and filament, while only job and mesh data come from
  live endpoints; the live snapshot is OFFLINE. Thus the passing live run does not
  establish five-category reconciliation against live sim state or real debug streams.
- The required live full-stack negative and recovery loop is not exercised. `verify_additional_fault_injections()`
  and the post-fault report use in-memory golden fixtures; they do not inject faults
  into, or verify recovery from, the live gateway path.
- '`reconcile_offline_snapshot()` accepts either sentinel value for each temperature
  field and permits HTTP 504, although the contract specifies unit-specific sentinel
  values (2147483646 millidegrees and 32767 deci-degrees) and HTTP 503. Invalid offline
  responses can therefore pass this check.'
- The 5x5 leveling check only requires 25 flattened points; it can accept a malformed
  grid shape such as one row containing 25 values. The contract requires a 5x5 grid.
accepted_scope: Reviewed the exact TWIN-46 revision 1 contract, pinned test_harness
  diff, bundle hash, checkout and server evidence, and the recorded fixture and sim-mode
  test outputs. Software and sim-mode integration are in scope. Physical MCU USB/UART
  HIL and cross-compiler ELF builds are excluded as specified; this review makes no
  claim about unexecuted HIL.
unexecuted:
- Full-stack sim positive reconciliation of all five categories using live AP state
  and corresponding debug-log inputs.
- Full-stack live mismatch, CRC/drop, OFFLINE-lock, and recovery checks against the
  running gateway.
- Negative checks proving unit-specific offline sentinel enforcement, rejection of
  non-503 lock responses, and rejection of malformed leveling grid shapes.
actual_session: 01a1a51c-ab4d-7622-beac-81fd6d929260
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f;
  test_harness=108158318581df366d133f556343d5367bd30cff
server_qa:
  task_id: TWIN-46
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 491292a665e4
    id: TWIN-46_run_134143_20261104_054143
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-46_run_134143_20261104_054143
    developer_mounts: []
    container_inspect:
      id: 491292a665e41b5565fbde601189bc2ba3986ac147ebe43b0047d3433af461cd
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T05:42:05.24238016Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-46_run_134143_20261104_054143
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-46_uyk2ih_1/evidence/server_lock.json
    sha256: 950141a014712591da25d3c4d0d6a5916f7044db6247e7d5ab5a058ed0676449
  checkout_log:
    path: /tmp/qa_TWIN-46_uyk2ih_1/evidence/checkout.log
    sha256: f3505f30e615858347dc091f37dc866f86bb84197fe5ac2b47de4c65e6a12d1f
  runtime_log:
    path: /tmp/qa_TWIN-46_uyk2ih_1/evidence/runtime.log
    sha256: 96c1a49ddeb0fab6dd7e3b89b615fb17f3fb75e482664f05531155927a5d94e3
  server_verdict:
    path: /tmp/qa_TWIN-46_uyk2ih_1/evidence/server_verdict.json
    sha256: 745e4ea83038a24e7a5db375f296aa006be0b9e246ed74dd98a57865d899604b
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: python3 hil/tools/debug_reconciliation_probe.py --help >/dev/null &&
      python3 hil/tools/debug_reconciliation_probe.py --self-test --matrix-out /tmp/qa_twin46_fixtures/selftest_matrix.md
      && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log
      --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json
      --matrix-out /tmp/qa_twin46_fixtures/cli_ok_matrix.md && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_mismatch.json) && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_crc_err.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json) && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_drop.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json) && python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_offline.json --matrix-out /tmp/qa_twin46_fixtures/cli_offline_matrix.md
      && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log
      --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json
      --matrix-out /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && test -s /tmp/qa_twin46_fixtures/selftest_matrix.md
      && test -s /tmp/qa_twin46_fixtures/cli_ok_matrix.md && test -s /tmp/qa_twin46_fixtures/cli_offline_matrix.md
      && test -s /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && rm -rf /tmp/qa_twin46_fixtures
    exit_code: '0'
    subpath: test_harness
    duration: 0.40s
    output: '[PASS] debug_reconciliation_probe.py self-test suite passed (7 fixtures
      generated).

      [PASS] Reconciliation succeeded (online-5-category).

      [PASS] Reconciliation succeeded (offline-sentinel).

      [PASS] Reconciliation succeeded (online-5-category).


      [RECONCILE FAIL] 1. Temperature Reporting & Setpoint: Temperature/ADC mismatch
      between MCU logs and AP snapshot

      [RECONCILE FAIL] 2. Homing & Motion Control: Motion coordinates or homed_mask
      mismatch

      [RECONCILE FAIL] 3. 5x5 Bed Leveling Grid: 5x5 leveling mesh or probe z_offset_um
      mismatch

      [RECONCILE FAIL] 4. Filament Feed/Retract & Slot Select: Filament slot/mask/step_state
      mismatch

      [RECONCILE FAIL] 5. Print Job State Machine: Job state or progress_permille
      mismatch

      [RECONCILE FAIL] MC-DBG seq=7 cmd=0x14 status=CRC_ERR err=0x01

      [RECONCILE FAIL] Ring buffer overflow/truncation detected: mc_drop=3, mc_trunc=1,
      th_drop=0, th_trunc=0'
  - command: rm -rf /tmp/qa_twin46 && mkdir -p /tmp/qa_twin46/bin && python3 -c "import
      pathlib; p=pathlib.Path(\"/tmp/qa_twin46/bin/curl\"); p.write_text(\"#!/usr/bin/env
      python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:]
      if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755)" && export PATH="/tmp/qa_twin46/bin:$PATH" && cp -r ../soc-ap
      ../test_harness /tmp/qa_twin46/ && rm -rf /tmp/qa_twin46/soc-ap/build && ([
      -e /tmp/qa_twin46/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin46/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin46/soc-ap/third_party/install)) && cd /tmp/qa_twin46/soc-ap
      && bash tools/deploy_twin.sh --mode sim --port 18085 && bash tools/deploy_twin.sh
      --status --port 18085 && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --matrix-out /tmp/qa_twin46/reconciliation_matrix.md
      && test -s /tmp/qa_twin46/reconciliation_matrix.md && bash tools/deploy_twin.sh
      --stop --port 18085 && rm -rf /tmp/qa_twin46
    exit_code: '0'
    subpath: soc-ap
    duration: 20.57s
    output: "=================================================================\n[BUILD]\
      \ Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- The C compiler identification is\
      \ GNU 9.4.0\n-- The CXX compiler identification is GNU 9.4.0\n-- Detecting C\
      \ compiler ABI info\n-- Detecting C compiler ABI info - done\n-- Check for working\
      \ C compiler: /usr/bin/cc - skipped\n-- Detecting C compile features\n-- Detecting\
      \ C compile features - done\n-- Detecting CXX compiler ABI info\n-- Detecting\
      \ CXX compiler ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++\
      \ - skipped\n-- Detecting CXX compile features\n-- Detecting CXX compile features\
      \ - done\n-- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files\
      \ have been written to: /tmp/qa_twin46/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin46/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 41%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin46/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 58%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 66%] Built target test_service_lifecycle\n[ 66%] Built target test_backoff\n\
      [ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin46/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin46/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin46/soc-ap/build/forward\n\
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 30%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 80%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 90%] Linking CXX static library libforward_service.a\n[ 90%] Built target\
      \ forward_service\n[ 95%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [100%] Linking CXX executable forward_service_daemon\n[100%] Built target forward_service_daemon\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin46/soc-ap/build/test_forward\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [100%] Linking CXX executable test_forward_service\n[100%] Built target test_forward_service\n\
      [BUILD 3/5] device_manager (build/device_manager)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin46/soc-ap/build/device_manager\n[  6%] Building CXX\
      \ object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n[ 12%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 18%]\
      \ Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 43%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 56%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 87%] Linking CXX static library libdevice_manager.a\n[ 87%] Built target device_manager\n\
      [ 93%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [100%] Linking CXX executable device_manager_daemon\n[100%] Built target device_manager_daemon\n\
      [BUILD 4/5] ui_gateway (build/ui_gateway)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin46/soc-ap/build/ui_gateway\n[  8%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n[ 16%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n[ 25%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n[ 33%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 50%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 58%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 83%] Linking CXX static library libui_gateway.a\n[ 83%] Built target ui_gateway\n\
      [ 91%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [100%] Linking CXX executable ui-gateway\n[100%] Built target ui-gateway\n[BUILD\
      \ 5/5] host CLI (build/host)...\n-- The CXX compiler identification is GNU 9.4.0\n\
      -- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI info - done\n\
      -- Check for working CXX compiler: /usr/bin/c++ - skipped\n-- Detecting CXX\
      \ compile features\n-- Detecting CXX compile features - done\n-- Found Python3:\
      \ /usr/bin/python3.8 (found version \"3.8.10\") found components: Interpreter\n\
      -- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n-- Configuring\
      \ done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been written to:\
      \ /tmp/qa_twin46/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 11%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 66%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /dev/ttyUSB0 @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18085/\n  State\
      \ API:   http://127.0.0.1:18085/api/v1/state\n  Snapshot:    http://127.0.0.1:18085/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full-Stack Status (Mode: sim)\n  UART Device: /dev/ttyUSB0 @ 921600 baud\n\
      \  HTTP Listen: 0.0.0.0:18085\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 856)\n  [RUNNING] forward_service_daemon (PID:\
      \ 861)\n  [RUNNING] device_manager_daemon (PID: 862)\n  [RUNNING] ui-gateway\
      \ (PID: 864)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18085/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [PASS] Live AP gateway (http://127.0.0.1:18085) HTTP/SSE & 5-category reconciliation\
      \ verified.\n[STOP] Stopping ui-gateway (PID: 864)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 862)...\n[STOP] Stopping forward_service_daemon (PID: 861)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 856)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned."
  passed: true
  timestamp: '2026-11-04T05:42:28.956248+00:00'
  path: /tmp/qa_TWIN-46_uyk2ih_1/evidence/server_qa.json
  sha256: 198f197055884795b676978322cfd68a61be85746a2b69818aff00c5ca6e2c7b
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-46_uyk2ih_1/reviews/6b529edd014540c6bc6b51db716a46c2/codex.jsonl
  sha256: 0371dc899ba5a87cea46f7923d94cfa9885fd92c9bad5feab06909004e152557
reviewed_artifacts:
- path: /tmp/qa_TWIN-46_uyk2ih_1/request.json
  sha256: 17687ce44fa5d4c2d57fdcb6c5ec0e87228a5a55fb7fae9145054e005cc3ee5c
- path: /tmp/qa_TWIN-46_uyk2ih_1/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_uyk2ih_1/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_uyk2ih_1/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_uyk2ih_1/diffs/test_harness.patch
  sha256: e659d88ff61a00182a670fa8ab6e7c696276d55977b820a56e012b69632e6c0d
- path: /tmp/qa_sandboxes/TWIN-46_run_134143_20261104_054143/test_harness/hil/tools/debug_reconciliation_probe.py
  sha256: 46e85aa0385046cff33f7e8356ff4931e4bc653695c325810a324b743688d502
verification_scope: Reviewed the exact TWIN-46 revision 1 contract, pinned test_harness
  diff, bundle hash, checkout and server evidence, and the recorded fixture and sim-mode
  test outputs. Software and sim-mode integration are in scope. Physical MCU USB/UART
  HIL and cross-compiler ELF builds are excluded as specified; this review makes no
  claim about unexecuted HIL.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The pinned bundle and recorded sandbox run are valid, and fixture-based positive, negative, offline, and recovery checks pass. The live sim path does not perform the required five-category reconciliation against live AP state, and offline validation accepts invalid sentinel/status combinations.
