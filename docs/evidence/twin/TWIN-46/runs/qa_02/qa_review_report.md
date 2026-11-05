```yaml
task_id: TWIN-46
task_revision: 1
candidate_commit: 91942286e8f686ce044a6aa8fdb11270ff8f5624
role: QA
decision: REJECTED
summary: 'The pinned bundle hash matches. The recorded host tests cover positive,
  negative, offline, and recovery paths, but the live PTY integration does not reconcile
  captured MCU/TH debug streams with the gateway: it synthesizes the log files independently
  of the PTY responses and gateway state.'
findings:
- In diffs/test_harness.patch, the PTY responder handles only version and temperature
  requests. write_live_online_logs() and drive_gateway_offline() separately construct
  [MC-DBG]/[TH-DBG] text from hard-coded values; the probe then compares those generated
  files with live HTTP responses. The five-category live positive checks and live
  fault/recovery checks therefore do not establish the contracted debug-to-UI data
  path from runtime telemetry.
- The recorded negative live cases alter synthesized log files while the gateway remains
  in its normal online state; this does not demonstrate live fault injection into
  the PTY/MC/TH-to-gateway path. The recovery check likewise generates a new synthetic
  log set.
accepted_scope: The frozen evidence records CLI/self-test positive and negative checks,
  offline sentinel and HTTP 503 checks, simulated deployment lifecycle, and a 921600
  POSIX PTY virtual-MCU full-stack run. Cross-compiler ELF builds and physical MCU
  USB/UART HIL are excluded by the contract; software evidence does not establish
  physical HIL.
unexecuted: []
actual_session: 01a1a552-8988-7c72-bd13-6e3c7486f6e1
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=426d604e9ddcfdb3e95e94ecff4f699ae976fc95; mcu-p3=29d62ef1bb7cf33e334f7e58aae81717cd26c54f;
  test_harness=91942286e8f686ce044a6aa8fdb11270ff8f5624
server_qa:
  task_id: TWIN-46
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: abdaf5296ea8
    id: TWIN-46_run_144908_20261104_064908
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-46_run_144908_20261104_064908
    developer_mounts: []
    container_inspect:
      id: abdaf5296ea8a68be6d5d72d6df841de95c4510e6fba0292b1710488c6bb180d
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T06:49:33.947026973Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-46_run_144908_20261104_064908
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-46_n4_g79lu/evidence/server_lock.json
    sha256: 148b7fefca222c70fee476614638823cb31ac7b8b5a3e3ea0836c6e9dd355b68
  checkout_log:
    path: /tmp/qa_TWIN-46_n4_g79lu/evidence/checkout.log
    sha256: d8ed87ad485c566062d8adf78823507b809150633bb4826b9a533f7cda180a27
  runtime_log:
    path: /tmp/qa_TWIN-46_n4_g79lu/evidence/runtime.log
    sha256: 0087bf4d39cdbbb3f466c5f8904f5367183d82cec4eafc339c3c6a18d24287c0
  server_verdict:
    path: /tmp/qa_TWIN-46_n4_g79lu/evidence/server_verdict.json
    sha256: 39a5880d2c672537c3fd13d6411002ad566888e0ee8c3dc12c5d458b35e80558
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
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json) && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_bad_grid.json) && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_ok.log --th-log /tmp/qa_twin46_fixtures/th_ok.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_offline.json) && (! python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_offline.log --th-log /tmp/qa_twin46_fixtures/th_offline.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_bad_offline.json) && python3 hil/tools/debug_reconciliation_probe.py
      --mc-log /tmp/qa_twin46_fixtures/mc_offline.log --th-log /tmp/qa_twin46_fixtures/th_offline.log
      --ap-snapshot /tmp/qa_twin46_fixtures/ap_offline.json --matrix-out /tmp/qa_twin46_fixtures/cli_offline_matrix.md
      && python3 hil/tools/debug_reconciliation_probe.py --mc-log /tmp/qa_twin46_fixtures/mc_ok.log
      --th-log /tmp/qa_twin46_fixtures/th_ok.log --ap-snapshot /tmp/qa_twin46_fixtures/ap_ok.json
      --matrix-out /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && test -s /tmp/qa_twin46_fixtures/selftest_matrix.md
      && test -s /tmp/qa_twin46_fixtures/cli_ok_matrix.md && test -s /tmp/qa_twin46_fixtures/cli_offline_matrix.md
      && test -s /tmp/qa_twin46_fixtures/cli_recovery_matrix.md && rm -rf /tmp/qa_twin46_fixtures
    exit_code: '0'
    subpath: test_harness
    duration: 0.52s
    output: '[PASS] debug_reconciliation_probe.py self-test suite passed (11 fixtures
      generated).

      [PASS] Reconciliation succeeded (online-5-category).

      [PASS] Reconciliation succeeded (offline-sentinel).

      [PASS] Reconciliation succeeded (online-5-category).


      [RECONCILE FAIL] 1. Temperature Reporting & Setpoint: Temperature/ADC mismatch
      between MCU logs and AP snapshot

      [RECONCILE FAIL] 2. Homing & Motion Control: Motion coordinates or homed_mask
      mismatch

      [RECONCILE FAIL] 3. 5x5 Bed Leveling Grid: 5x5 leveling mesh shape or probe
      z_offset_um mismatch

      [RECONCILE FAIL] 4. Filament Feed/Retract & Slot Select: Filament slot/mask/step_state
      mismatch

      [RECONCILE FAIL] 5. Print Job State Machine: Job state or progress_permille
      mismatch

      [RECONCILE FAIL] MC-DBG seq=7 cmd=0x14 status=CRC_ERR err=0x01

      [RECONCILE FAIL] Ring buffer overflow/truncation detected: mc_drop=3, mc_trunc=1,
      th_drop=0, th_trunc=0

      [RECONCILE FAIL] 3. 5x5 Bed Leveling Grid: 5x5 leveling mesh shape or probe
      z_offset_um mismatch

      [RECONCILE FAIL] OFFLINE unit-sentinel or HTTP 503 lock mismatch: bed_mc=2147483646,
      tool_mc=2147483646, mc_bed_ddC=600, lock=503

      [RECONCILE FAIL] OFFLINE unit-sentinel or HTTP 503 lock mismatch: bed_mc=32767,
      tool_mc=2147483646, mc_bed_ddC=32767, lock=504'
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
      --status --port 18085 && bash tools/deploy_twin.sh --stop --port 18085 && python3
      -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe
      as p; sys.exit(p.live_pty_ctl(\"start-pty\", \"/tmp/qa_twin46\"))" && bash tools/deploy_twin.sh
      --mode hardware --uart "$(cat /tmp/qa_twin46/pty_path)" --baud 921600 --port
      18085 && bash tools/deploy_twin.sh --status --port 18085 && python3 -c "import
      sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe
      as p; sys.exit(p.live_pty_ctl(\"drive-online\", \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))"
      && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url
      http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_ok.log --th-log /tmp/qa_twin46/th_live_ok.log
      --matrix-out /tmp/qa_twin46/live_ok_matrix.md && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_mismatch.log
      --th-log /tmp/qa_twin46/th_live_ok.log) && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_crc_err.log
      --th-log /tmp/qa_twin46/th_live_ok.log) && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_drop.log --th-log
      /tmp/qa_twin46/th_live_ok.log) && python3 -c "import sys; sys.path.insert(0,
      \"../test_harness/hil/tools\"); import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-offline\",
      \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_ok.log --th-log
      /tmp/qa_twin46/th_live_ok.log) && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_offline.log
      --th-log /tmp/qa_twin46/th_live_offline.log --matrix-out /tmp/qa_twin46/live_offline_matrix.md
      && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-recovery\",
      \"/tmp/qa_twin46\", \"http://127.0.0.1:18085\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18085 --mc-log /tmp/qa_twin46/mc_live_recovery.log
      --th-log /tmp/qa_twin46/th_live_recovery.log --matrix-out /tmp/qa_twin46/reconciliation_matrix.md
      && test -s /tmp/qa_twin46/live_ok_matrix.md && test -s /tmp/qa_twin46/live_offline_matrix.md
      && test -s /tmp/qa_twin46/reconciliation_matrix.md && bash tools/deploy_twin.sh
      --stop --port 18085 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"stop-pty\",
      \"/tmp/qa_twin46\"))" && rm -rf /tmp/qa_twin46
    exit_code: '0'
    subpath: soc-ap
    duration: 34.22s
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
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin46/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 58%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 66%] Built target test_backoff\n[ 66%] Built target test_service_lifecycle\n\
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
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
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
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/services/forward/forward_protocol.cpp.o\n\
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
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin46/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
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
      \ object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n[ 18%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n[ 18%]\
      \ Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 43%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
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
      \ CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n[ 50%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 58%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin46/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
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
      \ /tmp/qa_twin46/soc-ap/build/host\n[ 11%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 88%]\
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
      \  [RUNNING] dbus-daemon (PID: 862)\n  [RUNNING] forward_service_daemon (PID:\
      \ 867)\n  [RUNNING] device_manager_daemon (PID: 868)\n  [RUNNING] ui-gateway\
      \ (PID: 870)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18085/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 870)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 868)...\n[STOP] Stopping forward_service_daemon (PID: 867)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 862)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n=================================================================\n\
      [BUILD] Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin46/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 33%] Built target test_service_lifecycle\n\
      [ 50%] Built target test_backoff\n[ 75%] Built target aisoc_supervisor\n[100%]\
      \ Built target test_supervisor_topology\n[BUILD 2/5] forward (build/forward\
      \ & build/test_forward)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin46/soc-ap/build/forward\n[\
      \ 90%] Built target forward_service\n[100%] Built target forward_service_daemon\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin46/soc-ap/build/test_forward\n[100%] Built target\
      \ test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin46/soc-ap/build/device_manager\n[ 87%] Built target\
      \ device_manager\n[100%] Built target device_manager_daemon\n[BUILD 4/5] ui_gateway\
      \ (build/ui_gateway)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin46/soc-ap/build/ui_gateway\n\
      [ 83%] Built target ui_gateway\n[100%] Built target ui-gateway\n[BUILD 5/5]\
      \ host CLI (build/host)...\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT\
      \ not set)\n-- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build\
      \ files have been written to: /tmp/qa_twin46/soc-ap/build/host\n[ 44%] Built\
      \ target minimcproto\n[ 66%] Built target minimc-probe\n[100%] Built target\
      \ soc-ap\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        hardware\n  UART: \
      \       /dev/pts/0 @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18085/\n \
      \ State API:   http://127.0.0.1:18085/api/v1/state\n  Snapshot:    http://127.0.0.1:18085/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full-Stack Status (Mode: hardware)\n  UART Device: /dev/pts/0 @ 921600\
      \ baud\n  HTTP Listen: 0.0.0.0:18085\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 1198)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1203)\n  [RUNNING] device_manager_daemon (PID: 1204)\n  [RUNNING] ui-gateway\
      \ (PID: 1206)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18085/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [PASS] Live AP gateway (http://127.0.0.1:18085) reconciliation succeeded (online-5-category).\n\
      [PASS] Live AP gateway (http://127.0.0.1:18085) reconciliation succeeded (offline-sentinel).\n\
      [PASS] Live AP gateway (http://127.0.0.1:18085) reconciliation succeeded (online-5-category).\n\
      [STOP] Stopping ui-gateway (PID: 1206)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1204)...\n[STOP] Stopping forward_service_daemon (PID: 1203)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1198)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n\n[RECONCILE FAIL] 1. Temperature Reporting\
      \ & Setpoint: Temperature/ADC mismatch between MCU logs and AP snapshot\n[RECONCILE\
      \ FAIL] 2. Homing & Motion Control: Motion coordinates or homed_mask mismatch\n\
      [RECONCILE FAIL] 3. 5x5 Bed Leveling Grid: 5x5 leveling mesh shape or probe\
      \ z_offset_um mismatch\n[RECONCILE FAIL] 4. Filament Feed/Retract & Slot Select:\
      \ Filament slot/mask/step_state mismatch\n[RECONCILE FAIL] 5. Print Job State\
      \ Machine: Job state or progress_permille mismatch\n[RECONCILE FAIL] MC-DBG\
      \ seq=9 cmd=0x14 status=CRC_ERR err=0x01\n[RECONCILE FAIL] Ring buffer overflow/truncation\
      \ detected: mc_drop=3, mc_trunc=1, th_drop=0, th_trunc=0\n[RECONCILE FAIL] OFFLINE\
      \ unit-sentinel or HTTP 503 lock mismatch: bed_mc=2147483646, tool_mc=2147483646,\
      \ mc_bed_ddC=600, lock=503"
  passed: true
  timestamp: '2026-11-04T06:50:11.506231+00:00'
  path: /tmp/qa_TWIN-46_n4_g79lu/evidence/server_qa.json
  sha256: e8d46e446a5bb1167698126bcdf18448c4ab62b9702a4aec0a7beae719803d4f
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-46_n4_g79lu/reviews/59b6817308134d84859e0477a4b6eb2c/codex.jsonl
  sha256: 62992ccae130225c14afab911fd44ba72756690a971359311836df1598bb77df
reviewed_artifacts:
- path: /tmp/qa_TWIN-46_n4_g79lu/request.json
  sha256: acfa62ee01509ce713aaf589e50a8b48901b4ab063f80f64b93922d8dfe02134
- path: /tmp/qa_TWIN-46_n4_g79lu/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_n4_g79lu/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_n4_g79lu/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-46_n4_g79lu/diffs/test_harness.patch
  sha256: 06c5ff7093193161b20fbcedb7b07d6e89f25ad406bbf5e99038a125d5ff7850
- path: /tmp/qa_sandboxes/TWIN-46_run_144908_20261104_064908/test_harness/hil/tools/debug_reconciliation_probe.py
  sha256: 92d9b665ca82fefd372b63daf8d40666034121e0d7f7328dc1efe25aed3c67fe
verification_scope: The frozen evidence records CLI/self-test positive and negative
  checks, offline sentinel and HTTP 503 checks, simulated deployment lifecycle, and
  a 921600 POSIX PTY virtual-MCU full-stack run. Cross-compiler ELF builds and physical
  MCU USB/UART HIL are excluded by the contract; software evidence does not establish
  physical HIL.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The pinned bundle hash matches. The recorded host tests cover positive, negative, offline, and recovery paths, but the live PTY integration does not reconcile captured MCU/TH debug streams with the gateway: it synthesizes the log files independently of the PTY responses and gateway state.
