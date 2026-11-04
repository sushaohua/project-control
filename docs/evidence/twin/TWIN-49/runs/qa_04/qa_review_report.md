```yaml
task_id: TWIN-49
task_revision: 1
candidate_commit: 333178c66280e785ae1a5c089a6e2a05075cc926
role: QA
decision: APPROVED
summary: 已核验与上一轮 QA 报告及增量补丁的 SHA256。复验聚焦上一候选到本候选的差异，并核查了受影响的全栈构建、三套 CTest 和部署清理证据；未发现已接受条款的阻断项。
findings:
- 非阻断建议：server_verdict.json 的 build_count 为 0，但冻结运行日志记录了五个目标构建成功；建议后续统一该计数与日志口径。
accepted_scope: 按 TWIN-49 revision 1 核查软件及 POSIX PTY 沙箱范围：921600 波特率、0x10..0x1C 命令契约、MC
  后 TH 的双单播全 ACK 闭环、网关 D-Bus 路由及离线/超时/NACK 处理、第三方库自动构建、部署前进程/端口/UART/缓存/日志清理。本轮增量差异涉及遥测载荷与单位、5x5
  网格处理、温度离线映射、部署脚本 UART 自动发现；复验核对了相关回归证据。跨编译器 ELF 构建和实体 MCU USB/UART HIL 属明确排除范围，未声称其通过。
unexecuted: []
actual_session: 01a1a6c4-7035-7213-8292-e56b4df57c47
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-49
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: ad2b9f36344a
    id: TWIN-49_run_213323_20261104_133323
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323
    developer_mounts: []
    container_inspect:
      id: ad2b9f36344a31c8086aa9441abc7c3ce054142408ee7c11ad49f90b18c906d7
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T13:33:45.366468097Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-49_fjmio1cs/evidence/server_lock.json
    sha256: 5ffd458bf6e09fbb187dc40b0320801cd2efc44857dfc1bdac634611ad91e0e5
  checkout_log:
    path: /tmp/qa_TWIN-49_fjmio1cs/evidence/checkout.log
    sha256: bb2f96c5cbef45a070519ff2b9d3860726ed02253e5b3a77e7664b439476e941
  runtime_log:
    path: /tmp/qa_TWIN-49_fjmio1cs/evidence/runtime.log
    sha256: 61ad903d80e44fc172ff284dcb8eb6792403e1b7dc8a877fc4a8e7e110927fb0
  server_verdict:
    path: /tmp/qa_TWIN-49_fjmio1cs/evidence/server_verdict.json
    sha256: b5806bf61541f5f43e6e15fdda9bb69f93aae4ec6d462b6acc9613d10f9ce308
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin49 && mkdir -p /tmp/qa_twin49/bin && python3 -c "import
      pathlib; p=pathlib.Path(\"/tmp/qa_twin49/bin/curl\"); p.write_text(\"#!/usr/bin/env
      python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:]
      if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755)" && export PATH="/tmp/qa_twin49/bin:$PATH" && cp -r ../soc-ap
      /tmp/qa_twin49/ && rm -rf /tmp/qa_twin49/soc-ap/build && ([ -e /tmp/qa_twin49/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin49/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin49/soc-ap/third_party/install))
      && cd /tmp/qa_twin49/soc-ap && bash tools/deploy_twin.sh --build-only && ctest
      --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager
      --output-on-failure && ctest --test-dir build/ui_gateway --output-on-failure
      && mkdir -p dist/vmware_twin/logs dist/vmware_twin/run && echo stale > dist/vmware_twin/logs/stale.log
      && echo cache > dist/vmware_twin/run/stale.cache && touch /tmp/qa_twin49/dummy_uart
      && python3 -c "import socket,time,os; s=socket.socket(); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);
      s.bind((\"127.0.0.1\",18089)); s.listen(1); pid=os.fork(); (open(\"/tmp/qa_twin49/port_holder_pid\",\"w\").write(str(pid))
      if pid>0 else time.sleep(60))" && python3 -c "import time,os; f=open(\"/tmp/qa_twin49/dummy_uart\",\"r+\");
      pid=os.fork(); (open(\"/tmp/qa_twin49/uart_holder_pid\",\"w\").write(str(pid))
      if pid>0 else time.sleep(60))" debug_reconciliation_probe live_pty_ctl && PORT_PID=$(cat
      /tmp/qa_twin49/port_holder_pid) && UART_PID=$(cat /tmp/qa_twin49/uart_holder_pid)
      && grep -q "^State:.*[RS]" "/proc/$PORT_PID/status" && grep -q "^State:.*[RS]"
      "/proc/$UART_PID/status" && bash tools/deploy_twin.sh --mode sim --port 18089
      --uart /tmp/qa_twin49/dummy_uart && ([ ! -d "/proc/$PORT_PID" ] || grep -q "^State:.*Z"
      "/proc/$PORT_PID/status") && ([ ! -d "/proc/$UART_PID" ] || grep -q "^State:.*Z"
      "/proc/$UART_PID/status") && test ! -e dist/vmware_twin/logs/stale.log && test
      ! -e dist/vmware_twin/run/stale.cache && bash tools/deploy_twin.sh --stop --port
      18089 && rm -rf /tmp/qa_twin49
    exit_code: '0'
    subpath: soc-ap
    duration: 24.63s
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
      \ have been written to: /tmp/qa_twin49/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin49/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin49/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 58%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 66%] Built target test_service_lifecycle\n[ 66%] Built target test_backoff\n\
      [ 75%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin49/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin49/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/forward\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 30%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 80%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 90%] Linking CXX static library libforward_service.a\n[ 90%] Built target\
      \ forward_service\n[ 95%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [100%] Linking CXX executable forward_service_daemon\n[100%] Built target forward_service_daemon\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/test_forward\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Linking CXX executable test_forward_service\n[ 94%] Built target test_forward_service\n\
      [ 97%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [100%] Linking CXX executable test_forward_protocol\n[100%] Built target test_forward_protocol\n\
      [BUILD 3/5] device_manager (build/device_manager)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/device_manager\n[  5%] Building CXX\
      \ object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n[ 11%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 16%]\
      \ Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 27%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 38%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 61%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 72%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 77%] Linking CXX static library libdevice_manager.a\n[ 77%] Built target device_manager\n\
      [ 88%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 88%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin49/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 94%] Linking CXX executable device_manager_daemon\n[100%] Linking CXX executable\
      \ test_device_manager_state\n[100%] Built target device_manager_daemon\n[100%]\
      \ Built target test_device_manager_state\n[BUILD 4/5] ui_gateway (build/ui_gateway)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/ui_gateway\n\
      [  7%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n\
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 78%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin49/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
      [ 92%] Linking CXX executable ui-gateway\n[100%] Linking CXX executable test_ui_gateway_routes\n\
      [100%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- The CXX compiler identification is\
      \ GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI\
      \ info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n--\
      \ Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Found Python3: /usr/bin/python3.8 (found version \"3.8.10\") found components:\
      \ Interpreter\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n\
      -- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/host\n[ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin49/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/2 Test #1: test_forward_service .............   Passed    0.71 sec\n    Start\
      \ 2: test_forward_protocol\n2/2 Test #2: test_forward_protocol ............\
      \   Passed    0.25 sec\n\n100% tests passed out of 2\n\nTotal Test time (real)\
      \ =   0.96 sec\nTest project /tmp/qa_twin49/soc-ap/build/device_manager\n  \
      \  Start 1: test_device_manager_state\n1/1 Test #1: test_device_manager_state\
      \ ........   Passed    0.23 sec\n\n100% tests passed out of 1\n\nTotal Test\
      \ time (real) =   0.23 sec\nTest project /tmp/qa_twin49/soc-ap/build/ui_gateway\n\
      \    Start 1: test_ui_gateway_routes\n1/1 Test #1: test_ui_gateway_routes ...........\
      \   Passed    0.06 sec\n\n100% tests passed out of 1\n\nTotal Test time (real)\
      \ =   0.07 sec\n=================================================================\n\
      [BUILD] Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 33%] Built target test_service_lifecycle\n\
      [ 58%] Built target aisoc_supervisor\n[ 83%] Built target test_supervisor_topology\n\
      [100%] Built target test_backoff\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/forward\n[ 90%] Built target forward_service\n\
      [100%] Built target forward_service_daemon\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/test_forward\n\
      [100%] Built target test_forward_protocol\n[100%] Built target test_forward_service\n\
      [BUILD 3/5] device_manager (build/device_manager)...\n-- Configuring done (0.0s)\n\
      -- Generating done (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/device_manager\n\
      [ 77%] Built target device_manager\n[ 88%] Built target test_device_manager_state\n\
      [100%] Built target device_manager_daemon\n[BUILD 4/5] ui_gateway (build/ui_gateway)...\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/ui_gateway\n[ 71%] Built target ui_gateway\n\
      [ 85%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT\
      \ not set)\n-- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build\
      \ files have been written to: /tmp/qa_twin49/soc-ap/build/host\n[ 44%] Built\
      \ target minimcproto\n[ 66%] Built target minimc-probe\n[100%] Built target\
      \ soc-ap\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /tmp/qa_twin49/dummy_uart @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18089/\n\
      \  State API:   http://127.0.0.1:18089/api/v1/state\n  Snapshot:    http://127.0.0.1:18089/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      [STOP] Stopping ui-gateway (PID: 1218)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1216)...\n[STOP] Stopping forward_service_daemon (PID: 1215)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1210)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned."
  passed: true
  timestamp: '2026-11-04T13:34:13.448412+00:00'
  path: /tmp/qa_TWIN-49_fjmio1cs/evidence/server_qa.json
  sha256: 4803dc5e514d9b144c62eea369ea687013ba23ed004e8f8d853f46007ab937cc
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-49_fjmio1cs/reviews/93f9a06c215e46a29a6c8b64d359cfe4/codex.jsonl
  sha256: f8b89f993d4893dac3217a92811e10d713976aaf7fbb039520a22f5a97a2d56b
reviewed_artifacts:
- path: /tmp/qa_TWIN-49_fjmio1cs/request.json
  sha256: b7b7fdcc8a1e6d0507be2dd40c8f13cca250f7e0ac3647665d898b4cb871b45e
- path: /tmp/qa_TWIN-49_fjmio1cs/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_fjmio1cs/diffs/soc-ap.patch
  sha256: 9c97432090edbd60ea789938c504da8940d1c7f9e8b54ed4c4d6a2d15695cc3a
- path: /tmp/qa_TWIN-49_fjmio1cs/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_fjmio1cs/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/contracts/twin/telemetry_types.h
  sha256: 5ee430b244c575ac432938f589d0585c8d57d6b9af2003f5619dfa21c653e43a
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/device_manager/CMakeLists.txt
  sha256: b29c3a752eca559f69b09f03062307a0b621609bc86de7022b77ace986554f38
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/device_manager/device_manager_dbus.cpp
  sha256: c284692a2172d2943469912012720b87214afc90a2c81fa9e5f60444c281dab7
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/device_manager/device_manager_service.cpp
  sha256: 2bb5d7f107c0c582ae3b6e08a16d6e68a8b5e1e316911cdbf0334b608c6e9db7
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/device_manager/device_manager_service.h
  sha256: c135204fc67b9a89ba61e2f361152e43ed93cbb742ec68816f9bd86771195a2c
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/device_manager/device_manager_types.h
  sha256: 2360eaef0286154a33d22a3704646621fe080ac98af2cd3e7aa70d3cdb3a27d7
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_dbus.cpp
  sha256: c868f2001a0c480db3570c4802f00241feede04b3c1db1c4e9a77311f5364bdd
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_protocol.cpp
  sha256: 5dd157ac9b74fb83934e237850c7e5ecc024541d36a152ffcff24277fcdc542c
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_protocol.h
  sha256: 8dcf0ba6e18698c72837ed3710dbe2107dfd9f9554e4b159e3ffbbc20e6f714c
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_service.cpp
  sha256: 43a3d8149ba9d631d34bb565f2bc909e786c2147ee06dbe7b81d61895899124f
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_service.h
  sha256: 692f5d27302ec7eef80c13b5893f9a0ab0ec138d317eda531eb3a9754c9e0a94
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_types.h
  sha256: 50ebf34efabdd2014858c70ccb08dc211f74e302b25a7ccec7f2dab33e22666c
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/forward/forward_uart.cpp
  sha256: 7888314080c6488a247924a48618eb5d3c591578558ce03495cff0a7e2cf6e58
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/CMakeLists.txt
  sha256: c6d07aa7d183cd514d777999835c3859e6b75ec87846f62d690d8fa7a769f1e6
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  sha256: 100cd74dd6c9a2b2870fc770f0e34cbc61b262039fd2524963265a320ec78f92
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/ui_gateway_dbus.h
  sha256: edd6120cda3a8fd0c2a10c0c8170fe0959da396c93b5efc553a1e53d3def8937
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  sha256: a05f1a5d131fb664515543510d88668786a2d4fe4be71e03158e6433dab958fb
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  sha256: 7fdbf9517d429254eec8f84ebf206c30f76a19113d271e78047830c8bfec61af
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/services/ui_gateway/ui_gateway_server.cpp
  sha256: 49895019a2b7f78c60bb0bbe0c7b90f843be504c8ceba22fc21ce6c1d8854469
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
  sha256: d0e15d5ebfbbd183efcb0a1dc37063efccadaf268ef0fe2c4077d2a0f57792e2
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tests/forward/twin/CMakeLists.txt
  sha256: 23dd911c2a3376f910e76b2dcc2897082973e2432dc006181d1714419861bf9f
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tests/forward/twin/test_forward_protocol.cpp
  sha256: ac4680f9796ca979eb49c91cb1b9aee9e0824c940a6caa7adad6daaad4495940
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tests/forward/twin/test_forward_service.cpp
  sha256: 358d87077c73908b703368ecd84f741ddedad0bcafd6d3c8d1fea30b83267a0a
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  sha256: 518622d8af9d5be2dcdf7ba707a5f280e8cdde3e4f3c4784ed4118fba899e35c
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/third_party/build.sh
  sha256: 06ea9dce70a762a7b179c67a7835e01a060783b811da847baf88f6b40c92fd4e
- path: /tmp/qa_sandboxes/TWIN-49_run_213323_20261104_133323/soc-ap/tools/deploy_twin.sh
  sha256: dd32b4c034d0c1e7e9563c63cee532356f9a83a992dfc779a04396058bd48c9a
verification_scope: 按 TWIN-49 revision 1 核查软件及 POSIX PTY 沙箱范围：921600 波特率、0x10..0x1C
  命令契约、MC 后 TH 的双单播全 ACK 闭环、网关 D-Bus 路由及离线/超时/NACK 处理、第三方库自动构建、部署前进程/端口/UART/缓存/日志清理。本轮增量差异涉及遥测载荷与单位、5x5
  网格处理、温度离线映射、部署脚本 UART 自动发现；复验核对了相关回归证据。跨编译器 ELF 构建和实体 MCU USB/UART HIL 属明确排除范围，未声称其通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核验与上一轮 QA 报告及增量补丁的 SHA256。复验聚焦上一候选到本候选的差异，并核查了受影响的全栈构建、三套 CTest 和部署清理证据；未发现已接受条款的阻断项。
