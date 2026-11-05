```yaml
task_id: TWIN-43
task_revision: 1
candidate_commit: 217a76e29c0c99897bf1993514b765cd771adb06
role: QA
decision: BLOCKED
summary: The pinned bundle hash matches. The frozen evidence supports the full-stack
  build, cascade query cases, manifest schema checks, and a simulated start/status/stop
  lifecycle. It does not cover required baud rejection or missing-UART hardware behavior,
  so acceptance cannot be established.
findings:
- The bundle and referenced diff/evidence hashes match their recorded SHA256 values;
  the checkout log pins the expected candidate commit.
- The frozen run reports successful builds for five targets, 14/14 cascade cases,
  16/16 schema cases, and a sim-mode deployment with HTTP 200 status followed by service
  shutdown and PID cleanup.
- The required negative cases for rejecting an unsupported baud in both the serial
  and host-query paths, and aborting hardware mode when the configured UART is absent,
  were not executed. The available logs do not establish those behaviors.
- No distinct recovery case is evidenced, such as a failed startup followed by a clean
  retry or repeated stop/start lifecycle. Software evidence also cannot establish
  hardware-in-the-loop UART operation.
- source_report is empty, so there is no report or report hash to audit. The candidate
  diff was reviewed against the contract; the broad cascade negatives do not substitute
  for the required baud and hardware-mode negatives.
accepted_scope: Reviewed the TWIN-43 revision 1 contract and pinned soc-ap diff, along
  with the frozen server QA evidence. Supported evidence covers build, cascade query
  and schema checks, and simulated deployment status/stop behavior. Acceptance remains
  unverified for the explicitly required baud and hardware-mode negative behavior
  and recovery coverage.
unexecuted:
- Unsupported baud rejection in serial_open and parse_baud_rate, including refusal
  to open the serial device.
- Hardware-mode startup with a nonexistent AISOC_UART_DEVICE and verification of explicit
  nonzero failure without sim fallback.
- Recovery behavior after startup failure and repeated lifecycle operation.
- Hardware-in-the-loop UART behavior at 921600 baud.
- Independent source_report and source_report SHA256 audit; no source_report was supplied.
actual_session: 01a1a4a1-4133-70f0-950f-f008743914a6
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
    container_id: ab19c621a4a6
    id: TWIN-43_run_113544_20261104_033544
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544
    developer_mounts: []
    container_inspect:
      id: ab19c621a4a654fa785dd0dbf2abacf1cca89ab97b309c0ce0b5ed0a058ab899
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T03:36:06.615382784Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-43_cd0ufejc/evidence/server_lock.json
    sha256: 85750e2942d5f533ebf15678ca9106463eda31a68c7d89d4870b4a2da98fc9b6
  checkout_log:
    path: /tmp/qa_TWIN-43_cd0ufejc/evidence/checkout.log
    sha256: b6d428e46867e20a5917fd6636da7e048313779b161a7fb94f5e9298cddb8e5c
  runtime_log:
    path: /tmp/qa_TWIN-43_cd0ufejc/evidence/runtime.log
    sha256: 221b6fa0cc1eae4f56b52e1a5227769aff7e9629b3029cac3b4b9df916cc3484
  server_verdict:
    path: /tmp/qa_TWIN-43_cd0ufejc/evidence/server_verdict.json
    sha256: 5c8fea4e3e8e696be4f2e1f204ceaa0d630dede87c333c0bc21f1b5b4e10fd11
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin43 && mkdir -p /tmp/qa_twin43/bin && cp -r ../soc-ap
      ../test_harness /tmp/qa_twin43/ && rm -rf /tmp/qa_twin43/soc-ap/build && ([
      -e /tmp/qa_twin43/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin43/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin43/soc-ap/third_party/install)) && cd /tmp/qa_twin43/soc-ap
      && bash tools/deploy_twin.sh --build-only && ctest --test-dir build/forward
      --output-on-failure && python3 ../test_harness/static_checks/cascade/run_query_cases.py
      --test-host build/host/soc-ap --cases ../test_harness/test_cases/cascade/query_cases.json
    exit_code: '0'
    subpath: soc-ap
    duration: 12.55s
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
      [ 41%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
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
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
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
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin43/soc-ap/services/forward/forward_uart.cpp.o\n\
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
      \ object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 12%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n[ 18%]\
      \ Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin43/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
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
      \ CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n[ 25%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n[ 25%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n[ 33%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 50%] Building CXX object\
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
      \ /tmp/qa_twin43/soc-ap/build/host\n[ 11%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin43/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/1 Test #1: test_forward_service .............   Passed    0.50 sec\n\n100%\
      \ tests passed out of 1\n\nTotal Test time (real) =   0.50 sec\n[OK] 黄金用例集静态校验通过:\
      \ ../test_harness/test_cases/cascade/query_cases.json (含 4 正例, 10 负例)\n===========================================================================\n\
      \       执行 AP 宿主程序黑盒 PTY 级联查询测试: build/host/soc-ap\n===========================================================================\n\
      [PASS] CAS-POS-001  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP 直接查询 MC 固件版本 (单跳 GET_VERSION)\n\
      [PASS] CAS-POS-002  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP 经 MC 级联查询 TH 固件版本 (双跳\
      \ GET_VERSION 原生透明路由)\n[PASS] CAS-POS-003  | 退出码: 0 (期望 0) | 耗时: 0.061s | AP\
      \ 向 MC 发送心跳探活与时延测量 (单跳 PING/PONG)\n[PASS] CAS-POS-004  | 退出码: 0 (期望 0) | 耗时:\
      \ 0.061s | AP 经 MC 级联向 TH 发送心跳探活 (双跳 PING/PONG 原生透明路由)\n[PASS] CAS-NEG-001 \
      \ | 退出码: 1 (期望 1) | 耗时: 0.352s | 信道持续静默无响应 (Silence / Timeout)\n[PASS] CAS-NEG-002\
      \  | 退出码: 1 (期望 1) | 耗时: 0.362s | 信道回显原请求报文 (Echo / Reflection Loop)\n[PASS]\
      \ CAS-NEG-003  | 退出码: 1 (期望 1) | 耗时: 0.362s | 响应源节点错位 (Target Mismatch: 查 TH\
      \ 却收到 MC 回包)\n[PASS] CAS-NEG-004  | 退出码: 1 (期望 1) | 耗时: 0.362s | 流水号错位 (Stale\
      \ / Corrupted Sequence Number)\n[PASS] CAS-NEG-005  | 退出码: 2 (期望 2) | 耗时: 0.062s\
      \ | 操作码定义冲突 (Command Opcode Conflict: 收到 0x03 魔数或非法应答)\n[PASS] CAS-NEG-006 \
      \ | 退出码: 2 (期望 2) | 耗时: 0.061s | 载荷长度截断不匹配 (Truncated / Malformed Payload Length)\n\
      [PASS] CAS-NEG-007  | 退出码: 1 (期望 1) | 耗时: 0.362s | 帧尾 CRC-16 损坏 (Corrupted CRC-16)\n\
      [PASS] CAS-NEG-008  | 退出码: 2 (期望 2) | 耗时: 0.061s | 终端从机回发标准拒绝报文 (CMD_NACK with\
      \ Error Code)\n[PASS] CAS-NEG-009  | 退出码: 0 (期望 0) | 耗时: 0.061s | 信道夹杂 DWIN\
      \ 屏幕噪声抗扰 (Inter-packet Noise Resilience)\n[PASS] CAS-NEG-010  | 退出码: 4 (期望 4)\
      \ | 耗时: --s | 命令行非法参数拒绝 (CLI Argument Defense)\n---------------------------------------------------------------------------\n\
      测试汇总: 总用例 14, 通过 14, 失败 0\n==========================================================================="
  - command: python3 static_checks/twin/validate_schemas.py --root ..
    exit_code: '0'
    subpath: test_harness
    duration: 0.13s
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
      && bash tools/deploy_twin.sh --mode sim --port 18080 && bash tools/deploy_twin.sh
      --status --port 18080 && bash tools/deploy_twin.sh --stop --port 18080 && rm
      -rf /tmp/qa_twin43
    exit_code: '0'
    subpath: soc-ap
    duration: 11.24s
    output: "=================================================================\n[BUILD]\
      \ Incrementally building AI-SoC full stack...\n=================================================================\n\
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
      \  [RUNNING] dbus-daemon (PID: 1041)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1046)\n  [RUNNING] device_manager_daemon (PID: 1047)\n  [RUNNING] ui-gateway\
      \ (PID: 1049)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18080/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 1049)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1047)...\n[STOP] Stopping forward_service_daemon (PID: 1046)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1041)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned."
  passed: true
  timestamp: '2026-11-04T03:36:33.216147+00:00'
  path: /tmp/qa_TWIN-43_cd0ufejc/evidence/server_qa.json
  sha256: 94e2f1e441dce401a29fcd10dc92932460357c548e4263464ec1e34de89afc13
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-43_cd0ufejc/reviews/21bf3163b66b4be5b9b641a63e931341/codex.jsonl
  sha256: 3422b68cefa0d9be87287e050328c6288169e5d6ca08125d5f8ed56f25c238f7
reviewed_artifacts:
- path: /tmp/qa_TWIN-43_cd0ufejc/request.json
  sha256: 41993280081dc89a15de8c6ba0d12c3569b703beee9c7f9350ed1bac37b450a7
- path: /tmp/qa_TWIN-43_cd0ufejc/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_cd0ufejc/diffs/soc-ap.patch
  sha256: ff2cae1d54502bfd91875aeca31369d60641429aa4b71cac81d54b59203d3ce4
- path: /tmp/qa_TWIN-43_cd0ufejc/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-43_cd0ufejc/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/core/forward/transport/serial_posix.h
  sha256: 71aad720190d8f641dfdf2627b69a756e55bf7fd0a8d85507c49bf477e8dfb2c
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/core/forward/transport/serial_posix.cpp
  sha256: e335ee98fd5ca67c068424d88bbbd92b316514f08347a66f90ba8c7a3ae1091d
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/core/host/query.h
  sha256: c610fc7880e2d67215ab9431063bcdc50917f657d2353515898d382ecb8e6f3c
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/core/host/query.cpp
  sha256: 8fda9bea0b5cd0166ca62140b1497bb8ccd79a8199ffe91f2b41d987c97dbd14
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/config/runtime/vmware/services_manifest.json
  sha256: 127a44d31bd3a58f64bf865d0a18b700ffb597d0de13cdc6eecfc9d2183bd845
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/config/runtime/common/services_manifest.json
  sha256: 53c2ee8921c4e670bd786e5cefdb226a74e0e453e964d37dd34b785ea92aca38
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/config/runtime/vmware/aisoc_twin.conf
  sha256: 810495667ef758a842fb04c79d86b415d902f1918e0753fe99c87c9fd9dd155c
- path: /tmp/qa_sandboxes/TWIN-43_run_113544_20261104_033544/soc-ap/tools/deploy_twin.sh
  sha256: 8fb3d2d6711504aa0a1dd02a5df036b6a05b863e12f3ac99c41f9d3fd727db63
verification_scope: Reviewed the TWIN-43 revision 1 contract and pinned soc-ap diff,
  along with the frozen server QA evidence. Supported evidence covers build, cascade
  query and schema checks, and simulated deployment status/stop behavior. Acceptance
  remains unverified for the explicitly required baud and hardware-mode negative behavior
  and recovery coverage.
verification_environment: docker-sandbox-and-independent-codex-audit
```

The pinned bundle hash matches. The frozen evidence supports the full-stack build, cascade query cases, manifest schema checks, and a simulated start/status/stop lifecycle. It does not cover required baud rejection or missing-UART hardware behavior, so acceptance cannot be established.
