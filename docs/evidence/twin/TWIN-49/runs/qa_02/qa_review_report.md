```yaml
task_id: TWIN-49
task_revision: 1
candidate_commit: 9b457be31b05a6cf8bbe7b0a1dc08f21f6d8a116
role: QA
decision: REJECTED
summary: 复验已核对 QA 上轮报告及哈希：上一候选 cd87958209b050c0ef63e9be814dc8eca34b7d07 因部署前未清理配置端口/UART
  占用和旧日志被拒绝。本候选增量 diff 为 deploy_twin.sh 清理逻辑整改；冻结 Runner 记录全栈构建、三组 CTest 和部署清理命令均通过，但源码仍明确排除一类
  UART 占用进程，未满足已接受的彻底清理条款。
findings:
- 阻断：接受条款要求部署前清理配置 UART 的遗留占用进程，但 tools/deploy_twin.sh 在第 234、248 行对命令行包含 `debug_reconciliation_probe`
  或 `live_pty_ctl` 的进程跳过 UART 文件句柄匹配与终止。Runner 的清理检查仅使用普通 Python 进程同时持有测试端口和 UART
  文件，未覆盖这两个被排除的进程名，因此该场景仍未满足要求。部署前端口/UART/缓存/日志清理是接受范围内的明确要求。
accepted_scope: 本轮依据 QA 上轮报告（SHA256 20ba15b2ac36ef92b2c57cb1fd7fb77ee39fbfb3a7523ecfed3af98ccee582af）和本候选增量差异复验。范围包括
  B921600/B460800 与默认波特率、0x10..0x1C 协议和双单播全 ACK 闭环、网关 D-Bus 路由及离线/超时/NACK 负向行为、第三方库自动构建、部署前清理，以及受影响改动的必要回归。已核对本轮冻结
  Runner 报告的全栈构建、三组 CTest、部署清理链路均以 0 退出。跨编译器 ELF 构建和实体 MCU USB/UART HIL 属排除项；未声称这些硬件验证通过。
unexecuted: []
actual_session: 01a1a681-d2d8-74e0-ba3c-b74d1d327146
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=9b457be31b05a6cf8bbe7b0a1dc08f21f6d8a116; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-49
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 78f52002c791
    id: TWIN-49_run_202035_20261104_122035
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035
    developer_mounts: []
    container_inspect:
      id: 78f52002c791a975ce2e8c11403657d4a4d7a1a5e504c8813cfd562d73b590b8
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T12:21:00.047017473Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-49_pyikclgo/evidence/server_lock.json
    sha256: d4b21f328362e261c5ff1eed635c0f8b84e3df99cc553dd819ed2633c971e818
  checkout_log:
    path: /tmp/qa_TWIN-49_pyikclgo/evidence/checkout.log
    sha256: 7d2ce3c959d099892a1344339b241f71d81df736ed924b09efb46f2bbf21eb75
  runtime_log:
    path: /tmp/qa_TWIN-49_pyikclgo/evidence/runtime.log
    sha256: 0bd1cfe8cad034b0053e3ac1dcfa82212c50bb946a60208593f5a45d58de8ad7
  server_verdict:
    path: /tmp/qa_TWIN-49_pyikclgo/evidence/server_verdict.json
    sha256: 29a14611141a65e8a3ba74551fb9373e43afcc7a757d0ed694133fa979cd2428
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
      s.bind((\"127.0.0.1\",18089)); s.listen(1); f=open(\"/tmp/qa_twin49/dummy_uart\",\"r+\");
      pid=os.fork(); (open(\"/tmp/qa_twin49/holder_pid\",\"w\").write(str(pid)) if
      pid>0 else time.sleep(60))" && HOLDER_PID=$(cat /tmp/qa_twin49/holder_pid) &&
      grep -q "^State:.*[RS]" "/proc/$HOLDER_PID/status" && bash tools/deploy_twin.sh
      --mode sim --port 18089 --uart /tmp/qa_twin49/dummy_uart && ([ ! -d "/proc/$HOLDER_PID"
      ] || grep -q "^State:.*Z" "/proc/$HOLDER_PID/status") && test ! -e dist/vmware_twin/logs/stale.log
      && test ! -e dist/vmware_twin/run/stale.cache && bash tools/deploy_twin.sh --stop
      --port 18089 && rm -rf /tmp/qa_twin49
    exit_code: '0'
    subpath: soc-ap
    duration: 25.05s
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
      \ aisoc_runtime_common\n[ 33%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin49/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 58%] Linking CXX executable test_service_lifecycle\n[ 66%] Linking CXX executable\
      \ test_backoff\n[ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin49/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin49/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Built target test_service_lifecycle\n[ 83%] Built target test_backoff\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/forward\n\
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
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
      [  5%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [  5%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 97%] Linking CXX executable test_forward_protocol\n[100%] Linking CXX executable\
      \ test_forward_service\n[100%] Built target test_forward_protocol\n[100%] Built\
      \ target test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/device_manager\n\
      [  5%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
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
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n\
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin49/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [ 92%] Linking CXX executable ui-gateway\n[100%] Linking CXX executable test_ui_gateway_routes\n\
      [100%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- The CXX compiler identification is\
      \ GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI\
      \ info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n--\
      \ Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Found Python3: /usr/bin/python3.8 (found version \"3.8.10\") found components:\
      \ Interpreter\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n\
      -- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/host\n[ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin49/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/2 Test #1: test_forward_service .............   Passed    0.70 sec\n    Start\
      \ 2: test_forward_protocol\n2/2 Test #2: test_forward_protocol ............\
      \   Passed    0.25 sec\n\n100% tests passed out of 2\n\nTotal Test time (real)\
      \ =   0.95 sec\nTest project /tmp/qa_twin49/soc-ap/build/device_manager\n  \
      \  Start 1: test_device_manager_state\n1/1 Test #1: test_device_manager_state\
      \ ........   Passed    0.23 sec\n\n100% tests passed out of 1\n\nTotal Test\
      \ time (real) =   0.23 sec\nTest project /tmp/qa_twin49/soc-ap/build/ui_gateway\n\
      \    Start 1: test_ui_gateway_routes\n1/1 Test #1: test_ui_gateway_routes ...........\
      \   Passed    0.06 sec\n\n100% tests passed out of 1\n\nTotal Test time (real)\
      \ =   0.07 sec\n=================================================================\n\
      [BUILD] Incrementally building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/runtime\n\
      [ 16%] Built target aisoc_runtime_common\n[ 66%] Built target test_service_lifecycle\n\
      [ 66%] Built target test_backoff\n[ 75%] Built target aisoc_supervisor\n[100%]\
      \ Built target test_supervisor_topology\n[BUILD 2/5] forward (build/forward\
      \ & build/test_forward)...\n-- Configuring done (0.0s)\n-- Generating done (0.0s)\n\
      -- Build files have been written to: /tmp/qa_twin49/soc-ap/build/forward\n[\
      \ 90%] Built target forward_service\n[100%] Built target forward_service_daemon\n\
      -- Configuring done (0.0s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin49/soc-ap/build/test_forward\n[ 97%] Built target\
      \ test_forward_protocol\n[100%] Built target test_forward_service\n[BUILD 3/5]\
      \ device_manager (build/device_manager)...\n-- Configuring done (0.0s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin49/soc-ap/build/device_manager\n\
      [ 77%] Built target device_manager\n[100%] Built target test_device_manager_state\n\
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
      [STOP] Stopping ui-gateway (PID: 1214)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1212)...\n[STOP] Stopping forward_service_daemon (PID: 1211)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1206)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned."
  passed: true
  timestamp: '2026-11-04T12:21:27.851163+00:00'
  path: /tmp/qa_TWIN-49_pyikclgo/evidence/server_qa.json
  sha256: c78caab716adbc7f47be029d8e9b8b68409a0d4b7f4192cd038cf3b81fedb422
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-49_pyikclgo/reviews/e017254427a64b70845988a798c4fd65/codex.jsonl
  sha256: 1bb8de1d9dbb2481c3f2764e7e744adbc5802d0d2907f10126bcf0348d901691
reviewed_artifacts:
- path: /tmp/qa_TWIN-49_pyikclgo/request.json
  sha256: 00c71852100e967a15f7db4ae9f680a7b825d2f97b252cceff421c93b8f0aa1b
- path: /tmp/qa_TWIN-49_pyikclgo/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_pyikclgo/diffs/soc-ap.patch
  sha256: 5c08854add5cc6a4df202ecc17a68662b8f7a6f47d3f6db5abb2c5c0697f155b
- path: /tmp/qa_TWIN-49_pyikclgo/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_pyikclgo/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/contracts/twin/telemetry_types.h
  sha256: 941eecff2d0d80c552e904068c46594f2ae528fe68e7c5b44ef0d71e27faa23f
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/device_manager/CMakeLists.txt
  sha256: b29c3a752eca559f69b09f03062307a0b621609bc86de7022b77ace986554f38
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/device_manager/device_manager_dbus.cpp
  sha256: 8fc6eb4bcbd53c6fdf787239c618233319c542859768f5c188a451c3d38e1afa
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/device_manager/device_manager_service.cpp
  sha256: 2bb5d7f107c0c582ae3b6e08a16d6e68a8b5e1e316911cdbf0334b608c6e9db7
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/device_manager/device_manager_service.h
  sha256: c135204fc67b9a89ba61e2f361152e43ed93cbb742ec68816f9bd86771195a2c
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/device_manager/device_manager_types.h
  sha256: 2360eaef0286154a33d22a3704646621fe080ac98af2cd3e7aa70d3cdb3a27d7
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_dbus.cpp
  sha256: 223e9e03fff73ed364964ae582b721448fd284445f0e74a08942187c345d44f3
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_protocol.cpp
  sha256: 047b13d94bf4791a99160a4d4aa026f78218edd26f53487f69ff71f730beb9e7
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_protocol.h
  sha256: 8dcf0ba6e18698c72837ed3710dbe2107dfd9f9554e4b159e3ffbbc20e6f714c
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_service.cpp
  sha256: 43a3d8149ba9d631d34bb565f2bc909e786c2147ee06dbe7b81d61895899124f
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_service.h
  sha256: 692f5d27302ec7eef80c13b5893f9a0ab0ec138d317eda531eb3a9754c9e0a94
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_types.h
  sha256: 50ebf34efabdd2014858c70ccb08dc211f74e302b25a7ccec7f2dab33e22666c
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/forward/forward_uart.cpp
  sha256: 7888314080c6488a247924a48618eb5d3c591578558ce03495cff0a7e2cf6e58
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/CMakeLists.txt
  sha256: c6d07aa7d183cd514d777999835c3859e6b75ec87846f62d690d8fa7a769f1e6
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  sha256: d36719688c41f1141d8f5311fdf6741c2be4ce467ec4800f2d5b9ee73b850be1
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/ui_gateway_dbus.h
  sha256: 200907cb6c4bff7e4f334569ba0efa53fd6e67194cd05d5f4dd7f6d6907e9df0
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  sha256: 0b4028046165323ac97112fd1d275008a01e3cb312c092de1fd4beac1192e8c8
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  sha256: 7fdbf9517d429254eec8f84ebf206c30f76a19113d271e78047830c8bfec61af
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/services/ui_gateway/ui_gateway_server.cpp
  sha256: 49895019a2b7f78c60bb0bbe0c7b90f843be504c8ceba22fc21ce6c1d8854469
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
  sha256: 9a8a751e6837cd96fd2785523fc8a3b26cb5a63dbf4d0e698ef078b952b7b8b9
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/tests/forward/twin/CMakeLists.txt
  sha256: 23dd911c2a3376f910e76b2dcc2897082973e2432dc006181d1714419861bf9f
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/tests/forward/twin/test_forward_protocol.cpp
  sha256: 7a95a4cf7b34bd8551236106df31689e56aa0212fed2a32187c6231e3762b60c
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  sha256: 8bfc20665f9700a31a1915238ef9730fee6336720303f16434bae79ddd8a0b5f
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/third_party/build.sh
  sha256: 06ea9dce70a762a7b179c67a7835e01a060783b811da847baf88f6b40c92fd4e
- path: /tmp/qa_sandboxes/TWIN-49_run_202035_20261104_122035/soc-ap/tools/deploy_twin.sh
  sha256: 7cf18b1e5e98f3853c308f455e693e833a80554cb222262f695a3e0ca28d0228
verification_scope: 本轮依据 QA 上轮报告（SHA256 20ba15b2ac36ef92b2c57cb1fd7fb77ee39fbfb3a7523ecfed3af98ccee582af）和本候选增量差异复验。范围包括
  B921600/B460800 与默认波特率、0x10..0x1C 协议和双单播全 ACK 闭环、网关 D-Bus 路由及离线/超时/NACK 负向行为、第三方库自动构建、部署前清理，以及受影响改动的必要回归。已核对本轮冻结
  Runner 报告的全栈构建、三组 CTest、部署清理链路均以 0 退出。跨编译器 ELF 构建和实体 MCU USB/UART HIL 属排除项；未声称这些硬件验证通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验已核对 QA 上轮报告及哈希：上一候选 cd87958209b050c0ef63e9be814dc8eca34b7d07 因部署前未清理配置端口/UART 占用和旧日志被拒绝。本候选增量 diff 为 deploy_twin.sh 清理逻辑整改；冻结 Runner 记录全栈构建、三组 CTest 和部署清理命令均通过，但源码仍明确排除一类 UART 占用进程，未满足已接受的彻底清理条款。
