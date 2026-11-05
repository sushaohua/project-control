```yaml
task_id: TWIN-43
task_revision: 1
candidate_commit: 217a76e29c0c99897bf1993514b765cd771adb06
role: QA
decision: BLOCKED
summary: Pinned bundle and frozen test evidence hashes match. The recorded checks
  cover baud-rate behavior, manifest schema validation, invalid hardware startup,
  and repeated sim start/status/stop. Required evidence is missing for config-file
  loading and recovery after a deployment startup failure, so the accepted scope is
  not fully verified.
findings:
- The bundle SHA256 matches 8da5d76c5b1a54f0243ce90e46c420be49e4acfd39a3ad2bf029939a06a6fe95;
  the recorded server evidence matches 84186550616d89dfead433fa4424b3c34f209996f3b7bae9216b75d86955a54c.
  Checkout evidence pins soc-ap to the requested candidate commit.
- Recorded positive and negative coverage includes PTY opens at 921600/460800/115200,
  rejection of 123456, CLI invalid-baud rejection, schema validation, missing-hardware-device
  rejection, and two successful sim lifecycle cycles.
- The contract requires verifying that deploy_twin.sh reads aisoc_twin.conf and supports
  --config. The lifecycle command uses default settings and CLI overrides, but does
  not supply a distinct config file or verify config-derived values and precedence.
- The contract claims recovery after startup failure. The evidence exercises failed
  preflight and ordinary stop/restart, but does not force a failure after daemons
  launch (such as a failed health check) and verify cleanup. The --foreground path
  also uses exec after launching background services, so its failure cleanup is not
  demonstrated.
accepted_scope: 'Software and PTY verification of the pinned TWIN-43 candidate: baud
  defaults and supported rates, invalid-baud rejection, manifest schema checks, hardware
  missing-device rejection, and repeated sim lifecycle. Physical hardware HIL is explicitly
  outside this contract’s acceptance scope and is not established by software tests.'
unexecuted:
- Exercise --config with non-default values and confirm the loaded settings plus CLI
  override precedence.
- Force a post-launch startup or health-check failure and verify all started processes
  and PID/runtime files are cleaned up; include the foreground failure path if it
  is within the intended acceptance scope.
- Physical hardware HIL remains unexecuted and is outside the accepted software/PTY
  scope.
actual_session: 01a1a4ac-9ead-7903-8ac4-1144225c6d64
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=42b031efff970b01ee8cc8e5dd087387cdf9288f;
  soc-ap=217a76e29c0c99897bf1993514b765cd771adb06; mcu-p3=e051111e68dd61896ed42c0961153b167b8bca41;
  test_harness=ccf1476a0b98cb55ca9ee7bd49d73ca5d4704414
server_qa:
  task_id: TWIN-43
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 4ef7bbcdceeb
    id: TWIN-43_run_114751_20261104_034751
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751
    developer_mounts: []
    container_inspect:
      id: 4ef7bbcdceeb0dce7273b635abaff8153c255f20d5e05a25fd1130b4e3475b1d
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T03:48:20.38424077Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-43_eibefh_c/evidence/server_lock.json
    sha256: 85750e2942d5f533ebf15678ca9106463eda31a68c7d89d4870b4a2da98fc9b6
  checkout_log:
    path: /tmp/qa_TWIN-43_eibefh_c/evidence/checkout.log
    sha256: b6d428e46867e20a5917fd6636da7e048313779b161a7fb94f5e9298cddb8e5c
  runtime_log:
    path: /tmp/qa_TWIN-43_eibefh_c/evidence/runtime.log
    sha256: 6fa932bf8e573cae944ae7961edcb5ca5648d0245423b97bb90baaae667ac1a9
  server_verdict:
    path: /tmp/qa_TWIN-43_eibefh_c/evidence/server_verdict.json
    sha256: e58a715bac0cd5490479112a387c60fcf5e1dce635ed54ecd1c072717bec6805
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: 'rm -rf /tmp/qa_twin43 && mkdir -p /tmp/qa_twin43/bin && cp -r ../soc-ap
      ../test_harness /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build && ([
      -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)) && cd /tmp/qa_twin43/soc-ap
      && bash tools/deploy_twin.sh --build-only && ctest --test-dir build/forward
      --output-on-failure && python3 ../test_harness/static_checks/cascade/run_query_cases.py
      --test-host build/host/soc-ap --cases ../test_harness/test_cases/cascade/query_cases.json
      && python3 -c "import pathlib; pathlib.Path(\"/tmp/test_serial_baud.cpp\").write_text(\"#include
      <cassert>\n#include <cstdio>\n#include <cstdlib>\n#include <fcntl.h>\n#include
      <unistd.h>\n#include \\\"serial_posix.h\\\"\n#include \\\"query.h\\\"\nint main()
      {\n  minimc::SerialConfig dflt;\n  assert(dflt.baud_rate == 921600U);\n  minimc::QueryOptions
      qdflt;\n  assert(qdflt.baud_rate == 921600U);\n  int mfd = posix_openpt(O_RDWR
      | O_NOCTTY);\n  assert(mfd >= 0 && grantpt(mfd) == 0 && unlockpt(mfd) == 0);\n  const
      char* pts = ptsname(mfd);\n  assert(pts != nullptr);\n  minimc::SerialContext
      ctx;\n  minimc::SerialConfig bad{pts, 123456U};\n  assert(!minimc::serial_open(&bad,
      &ctx) && !ctx.is_open && ctx.fd == -1);\n  const uint32_t bauds[] = {921600U,
      460800U, 115200U};\n  for (uint32_t b : bauds) {\n    minimc::SerialConfig ok{pts,
      b};\n    assert(minimc::serial_open(&ok, &ctx) && ctx.is_open && ctx.fd >= 0);\n    minimc::serial_close(&ctx);\n    assert(!ctx.is_open
      && ctx.fd == -1);\n  }\n  close(mfd);\n  printf(\\\"[PASS] serial_posix baud_to_speed
      & serial_open positive(921600/460800/115200) and negative(123456) verified\\\\n\\\");\n  return
      0;\n}\n\")" && g++ -std=c++17 -O2 -Wall -Wextra -Werror -I core/forward/transport
      -I core/forward/minimc -I core/host core/forward/transport/serial_posix.cpp
      /tmp/test_serial_baud.cpp -o /tmp/test_serial_baud && /tmp/test_serial_baud
      && (! ./build/host/soc-ap --port /dev/null --baud 123456 --target mc --cmd version)
      && echo "[PASS] parse_baud_rate rejected invalid baud 123456"'
    exit_code: '0'
    subpath: soc-ap
    duration: 11.95s
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
      \ have been written to: /tmp/qa_twin43/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin43/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin43/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 58%] Linking CXX executable test_service_lifecycle\n[ 66%] Linking CXX executable\
      \ test_backoff\n[ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin43/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin43/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Built target test_backoff\n[ 83%] Built target test_service_lifecycle\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/forward\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 30%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 80%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 90%] Linking CXX static library libforward_service.a\n[ 90%] Built target\
      \ forward_service\n[ 95%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [100%] Linking CXX executable forward_service_daemon\n[100%] Built target forward_service_daemon\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/test_forward\n\
      [  5%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [100%] Linking CXX executable test_forward_service\n[100%] Built target test_forward_service\n\
      [BUILD 3/5] device_manager (build/device_manager)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/device_manager\n[  6%] Building CXX\
      \ object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n[ 12%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 18%]\
      \ Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 43%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 56%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 87%] Linking CXX static library libdevice_manager.a\n[ 87%] Built target device_manager\n\
      [ 93%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [100%] Linking CXX executable device_manager_daemon\n[100%] Built target device_manager_daemon\n\
      [BUILD 4/5] ui_gateway (build/ui_gateway)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/ui_gateway\n[  8%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n[ 16%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n[ 25%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n[ 33%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 41%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n[ 50%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 58%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
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
      \ /tmp/qa_twin43/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 66%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin43/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/1 Test #1: test_forward_service .............   Passed    0.49 sec\n\n100%\
      \ tests passed out of 1\n\nTotal Test time (real) =   0.49 sec\n[OK] 黄金用例集静态校验通过:\
      \ ../test_harness/test_cases/cascade/query_cases.json (含 4 正例, 10 负例)\n===========================================================================\n\
      \       执行 AP 宿主程序黑盒 PTY 级联查询测试: build/host/soc-ap\n===========================================================================\n\
      [PASS] CAS-POS-001  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP 直接查询 MC 固件版本 (单跳 GET_VERSION)\n\
      [PASS] CAS-POS-002  | 退出码: 0 (期望 0) | 耗时: 0.062s | AP 经 MC 级联查询 TH 固件版本 (双跳\
      \ GET_VERSION 原生透明路由)\n[PASS] CAS-POS-003  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP\
      \ 向 MC 发送心跳探活与时延测量 (单跳 PING/PONG)\n[PASS] CAS-POS-004  | 退出码: 0 (期望 0) | 耗时:\
      \ 0.061s | AP 经 MC 级联向 TH 发送心跳探活 (双跳 PING/PONG 原生透明路由)\n[PASS] CAS-NEG-001 \
      \ | 退出码: 1 (期望 1) | 耗时: 0.352s | 信道持续静默无响应 (Silence / Timeout)\n[PASS] CAS-NEG-002\
      \  | 退出码: 1 (期望 1) | 耗时: 0.362s | 信道回显原请求报文 (Echo / Reflection Loop)\n[PASS]\
      \ CAS-NEG-003  | 退出码: 1 (期望 1) | 耗时: 0.363s | 响应源节点错位 (Target Mismatch: 查 TH\
      \ 却收到 MC 回包)\n[PASS] CAS-NEG-004  | 退出码: 1 (期望 1) | 耗时: 0.362s | 流水号错位 (Stale\
      \ / Corrupted Sequence Number)\n[PASS] CAS-NEG-005  | 退出码: 2 (期望 2) | 耗时: 0.062s\
      \ | 操作码定义冲突 (Command Opcode Conflict: 收到 0x03 魔数或非法应答)\n[PASS] CAS-NEG-006 \
      \ | 退出码: 2 (期望 2) | 耗时: 0.061s | 载荷长度截断不匹配 (Truncated / Malformed Payload Length)\n\
      [PASS] CAS-NEG-007  | 退出码: 1 (期望 1) | 耗时: 0.362s | 帧尾 CRC-16 损坏 (Corrupted CRC-16)\n\
      [PASS] CAS-NEG-008  | 退出码: 2 (期望 2) | 耗时: 0.061s | 终端从机回发标准拒绝报文 (CMD_NACK with\
      \ Error Code)\n[PASS] CAS-NEG-009  | 退出码: 0 (期望 0) | 耗时: 0.062s | 信道夹杂 DWIN\
      \ 屏幕噪声抗扰 (Inter-packet Noise Resilience)\n[PASS] CAS-NEG-010  | 退出码: 4 (期望 4)\
      \ | 耗时: --s | 命令行非法参数拒绝 (CLI Argument Defense)\n---------------------------------------------------------------------------\n\
      测试汇总: 总用例 14, 通过 14, 失败 0\n===========================================================================\n\
      [PASS] serial_posix baud_to_speed & serial_open positive(921600/460800/115200)\
      \ and negative(123456) verified\nUsage: ./build/host/soc-ap [--serial-port PATH\
      \ | --port PATH | --device PATH]\n       ./build/host/soc-ap --target <mc|th>\
      \ --cmd <version|ping> [--port PATH] [--timeout-ms MS] [--baud 921600] [--seq\
      \ N] [--json]\n       ./build/host/soc-ap --query-version [--timeout-ms MS]\n\
      \       ./build/host/soc-ap --check-config\n       ./build/host/soc-ap --help\
      \ | --version\n[PASS] parse_baud_rate rejected invalid baud 123456"
  - command: python3 static_checks/twin/validate_schemas.py --root ..
    exit_code: '0'
    subpath: test_harness
    duration: 0.10s
    output: '========================================================================

      TWIN-03 Schema Draft7Validator Matrix Results

      ========================================================================

      [PASS] POS-MAN-VMWARE                   : VALID

      [PASS] POS-MAN-SOC                      : VALID

      [PASS] NEG-MAN-ONLY-4-ACTIVE            : Array missing required element at
      /services

      [PASS] NEG-MAN-MISSING-SYSTEM-MGR       : Array missing required element at
      /services

      [PASS] NEG-MAN-ACTIVE-MARKED-DEFERRED   : Value deferred != const first_slice_active
      at /services/0/slice_status

      [PASS] NEG-MAN-GENERATION-ZERO          : 0 < min 1 at /generation_id

      [PASS] NEG-MAN-BAD-REVISION-TAG         : ''bad_revision'' mismatch pattern
      ^[0-9]{8}_rev[0-9]+$ at /manifest_revision

      [PASS] POS-HTTP-SNAPSHOT-VALID          : VALID

      [PASS] POS-HTTP-SNAPSHOT-FAULT          : VALID

      [PASS] NEG-HTTP-TEMP-TOO-HIGH           : 500.1 > max 500.0 at /tool/temperature_c

      [PASS] NEG-HTTP-TEMP-TOO-LOW            : -40.1 < min -40.0 at /bed/temperature_c

      [PASS] NEG-HTTP-INVALID-SENTINEL        : Expected 1 valid in oneOf, got 0 at
      /tool/temperature_millic

      [PASS] NEG-HTTP-ADC-OVERFLOW            : 4096 > max 4095 at /bed/raw_adc

      [PASS] NEG-HTTP-EXTRA-PROPERTY          : Property ''extra_field'' not allowed
      at /extra_field

      [PASS] POS-SSE-TEMP-UPDATE              : VALID

      [PASS] NEG-SSE-INVALID-QUALITY-ENUM     : Value INVALID_QUALITY not in [''FRESH'',
      ''STALE'', ''FAULT'', ''UNKNOWN''] at /bed_q

      ------------------------------------------------------------------------

      Total: 16, Passed: 16, Failed: 0'
  - command: mkdir -p /tmp/qa_twin43/bin && python3 -c "import pathlib; p=pathlib.Path(\"/tmp/qa_twin43/bin/curl\");
      p.write_text(\"#!/usr/bin/env python3\nimport sys,urllib.request,urllib.error\nu=[a
      for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n
      r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755)" && export PATH="/tmp/qa_twin43/bin:$PATH" && ([ -d /tmp/qa_twin43/soc-ap
      ] || (cp -r ../soc-ap /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build
      && ([ -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)))) && cd /tmp/qa_twin43/soc-ap
      && (! bash tools/deploy_twin.sh --mode hardware --uart /dev/nonexistent_ttyUSB99
      --port 18080) && (! bash tools/deploy_twin.sh --status --port 18080) && (! bash
      tools/deploy_twin.sh --mode sim --baud 123456 --port 18080) && bash tools/deploy_twin.sh
      --mode sim --port 18080 && bash tools/deploy_twin.sh --status --port 18080 &&
      bash tools/deploy_twin.sh --stop --port 18080 && bash tools/deploy_twin.sh --mode
      sim --port 18080 && bash tools/deploy_twin.sh --status --port 18080 && bash
      tools/deploy_twin.sh --stop --port 18080 && rm -rf /tmp/qa_twin43
    exit_code: '0'
    subpath: soc-ap
    duration: 22.97s
    output: "=================================================================\nAI-SoC\
      \ VMware Twin Full-Stack Status (Mode: hardware)\n  UART Device: /dev/ttyUSB0\
      \ @ 921600 baud\n  HTTP Bind:   0.0.0.0:18080\n=================================================================\n\
      \  [STOPPED] dbus-daemon\n  [STOPPED] forward_service_daemon\n  [STOPPED] device_manager_daemon\n\
      \  [STOPPED] ui-gateway\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state\
      \ -> FAILED (HTTP 000000)\n=================================================================\n\
      =================================================================\n[BUILD] Incrementally\
      \ building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 33%] Built target test_service_lifecycle\n\
      [ 50%] Built target test_backoff\n[ 75%] Built target aisoc_supervisor\n[100%]\
      \ Built target test_supervisor_topology\n[BUILD 2/5] forward (build/forward\
      \ & build/test_forward)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin43/soc-ap/build/forward\n[\
      \ 90%] Built target forward_service\n[100%] Built target forward_service_daemon\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/test_forward\n[100%] Built target\
      \ test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/device_manager\n[ 87%] Built target\
      \ device_manager\n[100%] Built target device_manager_daemon\n[BUILD 4/5] ui_gateway\
      \ (build/ui_gateway)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin43/soc-ap/build/ui_gateway\n\
      [ 83%] Built target ui_gateway\n[100%] Built target ui-gateway\n[BUILD 5/5]\
      \ host CLI (build/host)...\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT\
      \ not set)\n-- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build\
      \ files have been written to: /tmp/qa_twin43/soc-ap/build/host\n[ 44%] Built\
      \ target minimcproto\n[ 66%] Built target minimc-probe\n[100%] Built target\
      \ soc-ap\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /dev/ttyUSB0 @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18080/\n  State\
      \ API:   http://127.0.0.1:18080/api/v1/state\n  Snapshot:    http://127.0.0.1:18080/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full-Stack Status (Mode: sim)\n  UART Device: /dev/ttyUSB0 @ 921600 baud\n\
      \  HTTP Bind:   0.0.0.0:18080\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 1075)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1080)\n  [RUNNING] device_manager_daemon (PID: 1081)\n  [RUNNING] ui-gateway\
      \ (PID: 1083)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 1083)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1081)...\n[STOP] Stopping forward_service_daemon (PID: 1080)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1075)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n=================================================================\n\
      [BUILD] Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 33%] Built target test_backoff\n\
      [ 50%] Built target test_service_lifecycle\n[ 75%] Built target aisoc_supervisor\n\
      [100%] Built target test_supervisor_topology\n[BUILD 2/5] forward (build/forward\
      \ & build/test_forward)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin43/soc-ap/build/forward\n[\
      \ 90%] Built target forward_service\n[100%] Built target forward_service_daemon\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/test_forward\n[100%] Built target\
      \ test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin43/soc-ap/build/device_manager\n[ 87%] Built target\
      \ device_manager\n[100%] Built target device_manager_daemon\n[BUILD 4/5] ui_gateway\
      \ (build/ui_gateway)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin43/soc-ap/build/ui_gateway\n\
      [ 83%] Built target ui_gateway\n[100%] Built target ui-gateway\n[BUILD 5/5]\
      \ host CLI (build/host)...\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT\
      \ not set)\n-- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build\
      \ files have been written to: /tmp/qa_twin43/soc-ap/build/host\n[ 44%] Built\
      \ target minimcproto\n[ 66%] Built target minimc-probe\n[100%] Built target\
      \ soc-ap\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /dev/ttyUSB0 @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18080/\n  State\
      \ API:   http://127.0.0.1:18080/api/v1/state\n  Snapshot:    http://127.0.0.1:18080/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full-Stack Status (Mode: sim)\n  UART Device: /dev/ttyUSB0 @ 921600 baud\n\
      \  HTTP Bind:   0.0.0.0:18080\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 1408)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1413)\n  [RUNNING] device_manager_daemon (PID: 1414)\n  [RUNNING] ui-gateway\
      \ (PID: 1416)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 1416)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1414)...\n[STOP] Stopping forward_service_daemon (PID: 1413)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1408)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n\nERROR: Hardware mode requires UART device\
      \ '/dev/nonexistent_ttyUSB99', but device node does not exist. Aborting without\
      \ falling back to sim mode.\nERROR: Unsupported baud rate '123456'. Allowed\
      \ values: 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600"
  passed: true
  timestamp: '2026-11-04T03:48:58.098661+00:00'
  path: /tmp/qa_TWIN-43_eibefh_c/evidence/server_qa.json
  sha256: 84186550616d89dfead433fa4424b3c34f209996f3b7bae9216b75d86955a54c
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-43_eibefh_c/reviews/fbc5d7be42c84e3093f2b51d0db06b19/codex.jsonl
  sha256: c05e77ba33ba61e8d24c1ed093f007424768636bb4373d8348920f4969651d1f
reviewed_artifacts:
- path: /tmp/qa_TWIN-43_eibefh_c/request.json
  sha256: a2ac5dece37ac12bd0db4cf341ff861b698ee24a0f93019a42895c7e15054253
- path: /tmp/qa_TWIN-43_eibefh_c/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_eibefh_c/diffs/soc-ap.patch
  sha256: ff2cae1d54502bfd91875aeca31369d60641429aa4b71cac81d54b59203d3ce4
- path: /tmp/qa_TWIN-43_eibefh_c/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_eibefh_c/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/core/forward/transport/serial_posix.h
  sha256: 71aad720190d8f641dfdf2627b69a756e55bf7fd0a8d85507c49bf477e8dfb2c
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/core/forward/transport/serial_posix.cpp
  sha256: e335ee98fd5ca67c068424d88bbbd92b316514f08347a66f90ba8c7a3ae1091d
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/core/host/query.h
  sha256: c610fc7880e2d67215ab9431063bcdc50917f657d2353515898d382ecb8e6f3c
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/core/host/query.cpp
  sha256: 8fda9bea0b5cd0166ca62140b1497bb8ccd79a8199ffe91f2b41d987c97dbd14
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/config/runtime/vmware/services_manifest.json
  sha256: 127a44d31bd3a58f64bf865d0a18b700ffb597d0de13cdc6eecfc9d2183bd845
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/config/runtime/common/services_manifest.json
  sha256: 53c2ee8921c4e670bd786e5cefdb226a74e0e453e964d37dd34b785ea92aca38
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/config/runtime/vmware/aisoc_twin.conf
  sha256: 810495667ef758a842fb04c79d86b415d902f1918e0753fe99c87c9fd9dd155c
- path: /tmp/qa_sandboxes/TWIN-43_run_114751_20261104_034751/soc-ap/tools/deploy_twin.sh
  sha256: 8fb3d2d6711504aa0a1dd02a5df036b6a05b863e12f3ac99c41f9d3fd727db63
verification_scope: 'Software and PTY verification of the pinned TWIN-43 candidate:
  baud defaults and supported rates, invalid-baud rejection, manifest schema checks,
  hardware missing-device rejection, and repeated sim lifecycle. Physical hardware
  HIL is explicitly outside this contract’s acceptance scope and is not established
  by software tests.'
verification_environment: docker-sandbox-and-independent-codex-audit
```

Pinned bundle and frozen test evidence hashes match. The recorded checks cover baud-rate behavior, manifest schema validation, invalid hardware startup, and repeated sim start/status/stop. Required evidence is missing for config-file loading and recovery after a deployment startup failure, so the accepted scope is not fully verified.
