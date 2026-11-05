```yaml
task_id: TWIN-43
task_revision: 1
candidate_commit: 217a76e29c0c99897bf1993514b765cd771adb06
role: QA
decision: REJECTED
summary: The bundle SHA256 matches the supplied hash, checkout evidence pins the requested
  candidate, and the frozen test evidence passes. The candidate does not honor the
  configured HTTP bind address during launch, so configuration-driven startup is incomplete.
findings:
- In tools/deploy_twin.sh, AISOC_HTTP_BIND is loaded from configuration and reported
  by --status, but the ui-gateway launch commands pass only --port and --static-dir.
  A configuration requesting a specific bind address therefore cannot control the
  listener and status may report an address the service is not using. The frozen lifecycle
  run used 0.0.0.0, so it does not expose this mismatch; honor the configured bind
  address and cover a non-default bind setting.
accepted_scope: 921600/460800/115200 baud support and invalid-baud rejection; manifest
  schema validation; and background deploy_twin.sh build, configuration loading and
  CLI override, sim startup/status/stop/recovery, hardware missing-UART preflight,
  and health-check-failure cleanup. Physical UART HIL and interactive --foreground
  mode are excluded.
unexecuted:
- Physical hardware UART HIL is not demonstrated by software or PTY evidence and is
  explicitly excluded from this task scope.
- Interactive --foreground exec mode is explicitly excluded.
- A non-default AISOC_HTTP_BIND configuration was not exercised; the launch path currently
  does not pass that setting to ui-gateway.
actual_session: 01a1a4bd-7ebf-7a41-8988-76b3635ee14c
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
    container_id: b6f2ac31c525
    id: TWIN-43_run_120551_20261104_040551
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551
    developer_mounts: []
    container_inspect:
      id: b6f2ac31c525ba230b900cea55a5ca7d395fc31ecbf83592d108478cf793d5a7
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T04:06:15.2880196Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-43_sakxbni4/evidence/server_lock.json
    sha256: 85750e2942d5f533ebf15678ca9106463eda31a68c7d89d4870b4a2da98fc9b6
  checkout_log:
    path: /tmp/qa_TWIN-43_sakxbni4/evidence/checkout.log
    sha256: b6d428e46867e20a5917fd6636da7e048313779b161a7fb94f5e9298cddb8e5c
  runtime_log:
    path: /tmp/qa_TWIN-43_sakxbni4/evidence/runtime.log
    sha256: ccd929ddcc5ab7d9968bd7a3bb24e4b5ec2bb1bfc9e66aacf1f40ef648c41077
  server_verdict:
    path: /tmp/qa_TWIN-43_sakxbni4/evidence/server_verdict.json
    sha256: 6409d64b51d5b235d69a0f070764b96b210bfaf5f297aeb912f5de745390a963
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
    duration: 12.06s
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
      [ 33%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 58%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 66%] Built target test_backoff\n[ 66%] Built target test_service_lifecycle\n\
      [ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin43/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin43/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/forward\n\
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
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
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_uart.cpp.o\n\
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
      \ CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 25%]\
      \ Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 43%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 43%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
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
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 50%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
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
      \ done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been written to:\
      \ /tmp/qa_twin43/soc-ap/build/host\n[ 11%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin43/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/1 Test #1: test_forward_service .............   Passed    0.49 sec\n\n100%\
      \ tests passed out of 1\n\nTotal Test time (real) =   0.49 sec\n[OK] 黄金用例集静态校验通过:\
      \ ../test_harness/test_cases/cascade/query_cases.json (含 4 正例, 10 负例)\n===========================================================================\n\
      \       执行 AP 宿主程序黑盒 PTY 级联查询测试: build/host/soc-ap\n===========================================================================\n\
      [PASS] CAS-POS-001  | 退出码: 0 (期望 0) | 耗时: 0.062s | AP 直接查询 MC 固件版本 (单跳 GET_VERSION)\n\
      [PASS] CAS-POS-002  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP 经 MC 级联查询 TH 固件版本 (双跳\
      \ GET_VERSION 原生透明路由)\n[PASS] CAS-POS-003  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP\
      \ 向 MC 发送心跳探活与时延测量 (单跳 PING/PONG)\n[PASS] CAS-POS-004  | 退出码: 0 (期望 0) | 耗时:\
      \ 0.061s | AP 经 MC 级联向 TH 发送心跳探活 (双跳 PING/PONG 原生透明路由)\n[PASS] CAS-NEG-001 \
      \ | 退出码: 1 (期望 1) | 耗时: 0.304s | 信道持续静默无响应 (Silence / Timeout)\n[PASS] CAS-NEG-002\
      \  | 退出码: 1 (期望 1) | 耗时: 0.362s | 信道回显原请求报文 (Echo / Reflection Loop)\n[PASS]\
      \ CAS-NEG-003  | 退出码: 1 (期望 1) | 耗时: 0.362s | 响应源节点错位 (Target Mismatch: 查 TH\
      \ 却收到 MC 回包)\n[PASS] CAS-NEG-004  | 退出码: 1 (期望 1) | 耗时: 0.362s | 流水号错位 (Stale\
      \ / Corrupted Sequence Number)\n[PASS] CAS-NEG-005  | 退出码: 2 (期望 2) | 耗时: 0.062s\
      \ | 操作码定义冲突 (Command Opcode Conflict: 收到 0x03 魔数或非法应答)\n[PASS] CAS-NEG-006 \
      \ | 退出码: 2 (期望 2) | 耗时: 0.062s | 载荷长度截断不匹配 (Truncated / Malformed Payload Length)\n\
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
      p.write_text(\"#!/usr/bin/env python3\nimport os,sys,urllib.request,urllib.error\nu=[a
      for a in sys.argv[1:] if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\nif
      os.environ.get(\x27FORCE_CURL_FAIL\x27)==\x271\x27:\n sys.stdout.write(\x27503\x27)
      if w else None;sys.exit(0 if w else 22)\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755); pathlib.Path(\"/tmp/qa_twin43/custom_twin.conf\").write_text(\"AISOC_MODE=\\\"sim\\\"\nAISOC_UART_DEVICE=\\\"/dev/null\\\"\nAISOC_UART_BAUD=\\\"460800\\\"\nAISOC_HTTP_BIND=\\\"0.0.0.0\\\"\nAISOC_HTTP_PORT=\\\"18082\\\"\nAISOC_WEB_ROOT=\\\"browser_hmi/first_release\\\"\nAISOC_LOG_DIR=\\\"/tmp/aisoc_custom_logs\\\"\nAISOC_AUTO_BUILD=\\\"0\\\"\n\")"
      && export PATH="/tmp/qa_twin43/bin:$PATH" && ([ -d /tmp/qa_twin43/soc-ap ] ||
      (cp -r ../soc-ap /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build && ([
      -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)))) && cd /tmp/qa_twin43/soc-ap
      && (! bash tools/deploy_twin.sh --config /tmp/nonexistent_twin.conf) && (! bash
      tools/deploy_twin.sh --mode hardware --uart /dev/nonexistent_ttyUSB99 --port
      18080) && (! bash tools/deploy_twin.sh --status --port 18080) && (! bash tools/deploy_twin.sh
      --mode sim --baud 123456 --port 18080) && (! FORCE_CURL_FAIL=1 bash tools/deploy_twin.sh
      --mode sim --port 18080) && (! bash tools/deploy_twin.sh --status --port 18080)
      && [ ! -e /tmp/aisoc_twin_logs/ui_gateway.pid ] && [ ! -e /tmp/aisoc_twin_logs/device_manager.pid
      ] && [ ! -e /tmp/aisoc_twin_logs/forward.pid ] && [ ! -e /tmp/aisoc_twin_logs/dbus.pid
      ] && [ ! -e /tmp/aisoc_twin_logs/runtime.env ] && echo "[PASS] post-launch health-check
      failure cleaned up all daemons and PID/runtime files" && bash tools/deploy_twin.sh
      --config /tmp/qa_twin43/custom_twin.conf && bash tools/deploy_twin.sh --config
      /tmp/qa_twin43/custom_twin.conf --status | grep -E "460800|18082" && bash tools/deploy_twin.sh
      --config /tmp/qa_twin43/custom_twin.conf --stop && bash tools/deploy_twin.sh
      --config /tmp/qa_twin43/custom_twin.conf --baud 921600 --port 18083 && bash
      tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf --status | grep
      -E "921600|18083" && bash tools/deploy_twin.sh --config /tmp/qa_twin43/custom_twin.conf
      --stop && bash tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh
      --status --port 18080 && bash tools/deploy_twin.sh --stop --port 18080 && bash
      tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh --status
      --port 18080 && bash tools/deploy_twin.sh --stop --port 18080 && rm -rf /tmp/qa_twin43
      /tmp/aisoc_custom_logs
    exit_code: '0'
    subpath: soc-ap
    duration: 53.92s
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
      [ 16%] Built target aisoc_runtime_common\n[ 50%] Built target test_service_lifecycle\n\
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
      [STOP] Stopping ui-gateway (PID: 1089)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1087)...\n[STOP] Stopping forward_service_daemon (PID: 1086)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1081)...\n=================================================================\n\
      AI-SoC VMware Twin Full-Stack Status (Mode: hardware)\n  UART Device: /dev/ttyUSB0\
      \ @ 921600 baud\n  HTTP Bind:   0.0.0.0:18080\n=================================================================\n\
      \  [STOPPED] dbus-daemon\n  [STOPPED] forward_service_daemon\n  [STOPPED] device_manager_daemon\n\
      \  [STOPPED] ui-gateway\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state\
      \ -> FAILED (HTTP 000000)\n=================================================================\n\
      [PASS] post-launch health-check failure cleaned up all daemons and PID/runtime\
      \ files\n=================================================================\n\
      AI-SoC VMware Twin Full Stack Deployed Successfully!\n  Mode:        sim\n \
      \ UART:        /dev/null @ 460800 baud\n  HTTP URL:    http://127.0.0.1:18082/\n\
      \  State API:   http://127.0.0.1:18082/api/v1/state\n  Snapshot:    http://127.0.0.1:18082/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_custom_logs\n=================================================================\n\
      \  UART Device: /dev/null @ 460800 baud\n  HTTP Bind:   0.0.0.0:18082\n  [HEALTH\
      \ ] HTTP Probe http://127.0.0.1:18082/api/v1/state -> HTTP 200 OK\n[STOP] Stopping\
      \ ui-gateway (PID: 1292)...\n[STOP] Stopping device_manager_daemon (PID: 1290)...\n\
      [STOP] Stopping forward_service_daemon (PID: 1289)...\n[STOP] Stopping dbus-daemon\
      \ (PID: 1284)...\n[STOP] All AI-SoC VMware Twin services stopped and PID files\
      \ cleaned.\n=================================================================\n\
      AI-SoC VMware Twin Full Stack Deployed Successfully!\n  Mode:        sim\n \
      \ UART:        /dev/null @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18083/\n\
      \  State API:   http://127.0.0.1:18083/api/v1/state\n  Snapshot:    http://127.0.0.1:18083/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_custom_logs\n=================================================================\n\
      \  UART Device: /dev/null @ 921600 baud\n  HTTP Bind:   0.0.0.0:18083\n  [HEALTH\
      \ ] HTTP Probe http://127.0.0.1:18083/api/v1/state -> HTTP 200 OK\n[STOP] Stopping\
      \ ui-gateway (PID: 1481)...\n[STOP] Stopping device_manager_daemon (PID: 1479)...\n\
      [STOP] Stopping forward_service_daemon (PID: 1478)...\n[STOP] Stopping dbus-daemon\
      \ (PID: 1473)...\n[STOP] All AI-SoC VMware Twin services stopped and PID files\
      \ cleaned.\n=================================================================\n\
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
      \  [RUNNING] dbus-daemon (PID: 1807)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1812)\n  [RUNNING] device_manager_daemon (PID: 1813)\n  [RUNNING] ui-gateway\
      \ (PID: 1815)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 1815)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1813)...\n[STOP] Stopping forward_service_daemon (PID: 1812)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1807)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n=================================================================\n\
      [BUILD] Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin43/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 50%] Built target test_service_lifecycle\n\
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
      \  [RUNNING] dbus-daemon (PID: 2140)\n  [RUNNING] forward_service_daemon (PID:\
      \ 2145)\n  [RUNNING] device_manager_daemon (PID: 2146)\n  [RUNNING] ui-gateway\
      \ (PID: 2148)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 2148)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 2146)...\n[STOP] Stopping forward_service_daemon (PID: 2145)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 2140)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n\nERROR: Specified configuration file not\
      \ found: /tmp/nonexistent_twin.conf\nERROR: Hardware mode requires UART device\
      \ '/dev/nonexistent_ttyUSB99', but device node does not exist. Aborting without\
      \ falling back to sim mode.\nERROR: Unsupported baud rate '123456'. Allowed\
      \ values: 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600\nERROR:\
      \ Full-stack deployment failed health check on port 18080."
  passed: true
  timestamp: '2026-11-04T04:07:24.076265+00:00'
  path: /tmp/qa_TWIN-43_sakxbni4/evidence/server_qa.json
  sha256: c72a4013e189e742b8d56e4354f58490b81645a084abdac2e312a672afd925e0
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-43_sakxbni4/reviews/0b4a6e0e7bc54d9197548a0721714735/codex.jsonl
  sha256: b2aa6b77b894a5e6d05f25d20c8dba3b38bc09282f9dbb70e0fc56b59dbd7496
reviewed_artifacts:
- path: /tmp/qa_TWIN-43_sakxbni4/request.json
  sha256: 4bb84a047e9c53e577ec4a348e6da8d6b01d58a8809911208dce15b9dfd0a412
- path: /tmp/qa_TWIN-43_sakxbni4/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_sakxbni4/diffs/soc-ap.patch
  sha256: ff2cae1d54502bfd91875aeca31369d60641429aa4b71cac81d54b59203d3ce4
- path: /tmp/qa_TWIN-43_sakxbni4/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_sakxbni4/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/core/forward/transport/serial_posix.h
  sha256: 71aad720190d8f641dfdf2627b69a756e55bf7fd0a8d85507c49bf477e8dfb2c
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/core/forward/transport/serial_posix.cpp
  sha256: e335ee98fd5ca67c068424d88bbbd92b316514f08347a66f90ba8c7a3ae1091d
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/core/host/query.h
  sha256: c610fc7880e2d67215ab9431063bcdc50917f657d2353515898d382ecb8e6f3c
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/core/host/query.cpp
  sha256: 8fda9bea0b5cd0166ca62140b1497bb8ccd79a8199ffe91f2b41d987c97dbd14
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/config/runtime/vmware/services_manifest.json
  sha256: 127a44d31bd3a58f64bf865d0a18b700ffb597d0de13cdc6eecfc9d2183bd845
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/config/runtime/common/services_manifest.json
  sha256: 53c2ee8921c4e670bd786e5cefdb226a74e0e453e964d37dd34b785ea92aca38
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/config/runtime/vmware/aisoc_twin.conf
  sha256: 810495667ef758a842fb04c79d86b415d902f1918e0753fe99c87c9fd9dd155c
- path: /tmp/qa_sandboxes/TWIN-43_run_120551_20261104_040551/soc-ap/tools/deploy_twin.sh
  sha256: 8fb3d2d6711504aa0a1dd02a5df036b6a05b863e12f3ac99c41f9d3fd727db63
verification_scope: 921600/460800/115200 baud support and invalid-baud rejection;
  manifest schema validation; and background deploy_twin.sh build, configuration loading
  and CLI override, sim startup/status/stop/recovery, hardware missing-UART preflight,
  and health-check-failure cleanup. Physical UART HIL and interactive --foreground
  mode are excluded.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The bundle SHA256 matches the supplied hash, checkout evidence pins the requested candidate, and the frozen test evidence passes. The candidate does not honor the configured HTTP bind address during launch, so configuration-driven startup is incomplete.
