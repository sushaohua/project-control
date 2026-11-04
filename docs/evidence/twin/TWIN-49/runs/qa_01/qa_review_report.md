```yaml
task_id: TWIN-49
task_revision: 1
candidate_commit: cd87958209b050c0ef63e9be814dc8eca34b7d07
role: QA
decision: REJECTED
summary: 已核验冻结索引、请求、差异及相关源码哈希。Runner 记录全栈构建和三组 CTest 通过；但候选未满足部署前清理的明确接受条款。
findings:
- 阻断：接受范围要求部署前清理旧进程、端口/UART 占用、旧缓存和旧日志。候选 deploy_twin.sh 的 purge_previous_deployment
  只停止受管 PID、按指定可执行文件名清理进程，并删除 PID、dbus.addr 和 runtime.env；没有清理占用配置端口或 UART 的其他进程，也没有清理旧日志。相关冻结源码哈希与索引一致。
accepted_scope: 审阅范围为 TWIN-49 接受的软件及 POSIX PTY 验证：921600 波特率、0x10..0x1C 命令与双单播 ACK
  闭环、网关 D-Bus 控制及离线/失败拦截、第三方库自动构建和部署前清理。跨编译器 ELF 构建与实体 MCU USB/UART HIL 属排除项；未声称这些硬件验证通过。
unexecuted:
- 未执行对占用配置端口或 UART 的遗留进程、旧日志清理行为的定向验证。
actual_session: 01a1a672-fa32-7fe3-bb42-3edc253ff4da
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=cd87958209b050c0ef63e9be814dc8eca34b7d07; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=30c21f74e74179994eb475c38cc4afc2c1427a26
server_qa:
  task_id: TWIN-49
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: fcfff7cd35f7
    id: TWIN-49_run_200436_20261104_120436
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436
    developer_mounts: []
    container_inspect:
      id: fcfff7cd35f710b883b07922ea6bb7224273e13ee208c5e8fbaa658cc53ef416
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T12:04:58.975460565Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-49_mcu6ig_k/evidence/server_lock.json
    sha256: 9cda8e51fb9ebeb8589a4d758d640f5a65368ead43474690101d98aaaba9bca8
  checkout_log:
    path: /tmp/qa_TWIN-49_mcu6ig_k/evidence/checkout.log
    sha256: ce9d89e1f0f433e9de1b38d96320fda2df4eb95dac0fb6fe63eb139b946ae8a0
  runtime_log:
    path: /tmp/qa_TWIN-49_mcu6ig_k/evidence/runtime.log
    sha256: 3d456e0d2f42956b4f30f89d12afe8aa34159a8d1723d810d028d8ffbeb1011e
  server_verdict:
    path: /tmp/qa_TWIN-49_mcu6ig_k/evidence/server_verdict.json
    sha256: 18cb897758e03a44c2dcf446bca16219e5ebc18847df5f02ad170184ce3828ee
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin49 && mkdir -p /tmp/qa_twin49 && cp -r ../soc-ap /tmp/qa_twin49/
      && rm -rf /tmp/qa_twin49/soc-ap/build && ([ -e /tmp/qa_twin49/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin49/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin49/soc-ap/third_party/install))
      && cd /tmp/qa_twin49/soc-ap && bash tools/deploy_twin.sh --build-only && ctest
      --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager
      --output-on-failure && ctest --test-dir build/ui_gateway --output-on-failure
      && rm -rf /tmp/qa_twin49
    exit_code: '0'
    subpath: soc-ap
    duration: 12.96s
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
      \ aisoc_runtime_common\n[ 33%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin49/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 58%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 66%] Built target test_backoff\n[ 66%] Built target test_service_lifecycle\n\
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
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
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
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/services/forward/forward_protocol.cpp.o\n\
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
      [ 47%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
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
      [ 89%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin49/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
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
      [ 11%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
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
      [ 83%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
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
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
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
      \ written to: /tmp/qa_twin49/soc-ap/build/host\n[ 11%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
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
      \ =   0.07 sec"
  passed: true
  timestamp: '2026-11-04T12:05:14.816646+00:00'
  path: /tmp/qa_TWIN-49_mcu6ig_k/evidence/server_qa.json
  sha256: 07cf7e1aaa280a0380b7c2d6ba78a59982b614bd2f9722a339f4ce45aed6b4b5
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-49_mcu6ig_k/reviews/600dbc99a387448c8628739bad38aa16/codex.jsonl
  sha256: 2ad690eb4a724b6cf3dc5a1c69880eecf250b71c2a22fb900aaba4753555146b
reviewed_artifacts:
- path: /tmp/qa_TWIN-49_mcu6ig_k/request.json
  sha256: 5079090f93e3e59a516f3c7c8712a9230648d30c4ea0e0334340596b1609d545
- path: /tmp/qa_TWIN-49_mcu6ig_k/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_mcu6ig_k/diffs/soc-ap.patch
  sha256: b57145cbdc5c2b515c202d959f17b8b8200d2d2e85317127cd379d690a606c8f
- path: /tmp/qa_TWIN-49_mcu6ig_k/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-49_mcu6ig_k/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/contracts/twin/telemetry_types.h
  sha256: 941eecff2d0d80c552e904068c46594f2ae528fe68e7c5b44ef0d71e27faa23f
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/device_manager/CMakeLists.txt
  sha256: b29c3a752eca559f69b09f03062307a0b621609bc86de7022b77ace986554f38
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/device_manager/device_manager_dbus.cpp
  sha256: 8fc6eb4bcbd53c6fdf787239c618233319c542859768f5c188a451c3d38e1afa
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/device_manager/device_manager_service.cpp
  sha256: 2bb5d7f107c0c582ae3b6e08a16d6e68a8b5e1e316911cdbf0334b608c6e9db7
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/device_manager/device_manager_service.h
  sha256: c135204fc67b9a89ba61e2f361152e43ed93cbb742ec68816f9bd86771195a2c
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/device_manager/device_manager_types.h
  sha256: 2360eaef0286154a33d22a3704646621fe080ac98af2cd3e7aa70d3cdb3a27d7
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_dbus.cpp
  sha256: 223e9e03fff73ed364964ae582b721448fd284445f0e74a08942187c345d44f3
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_protocol.cpp
  sha256: 047b13d94bf4791a99160a4d4aa026f78218edd26f53487f69ff71f730beb9e7
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_protocol.h
  sha256: 8dcf0ba6e18698c72837ed3710dbe2107dfd9f9554e4b159e3ffbbc20e6f714c
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_service.cpp
  sha256: 43a3d8149ba9d631d34bb565f2bc909e786c2147ee06dbe7b81d61895899124f
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_service.h
  sha256: 692f5d27302ec7eef80c13b5893f9a0ab0ec138d317eda531eb3a9754c9e0a94
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_types.h
  sha256: 50ebf34efabdd2014858c70ccb08dc211f74e302b25a7ccec7f2dab33e22666c
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/forward/forward_uart.cpp
  sha256: 7888314080c6488a247924a48618eb5d3c591578558ce03495cff0a7e2cf6e58
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/CMakeLists.txt
  sha256: c6d07aa7d183cd514d777999835c3859e6b75ec87846f62d690d8fa7a769f1e6
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  sha256: d36719688c41f1141d8f5311fdf6741c2be4ce467ec4800f2d5b9ee73b850be1
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/ui_gateway_dbus.h
  sha256: 200907cb6c4bff7e4f334569ba0efa53fd6e67194cd05d5f4dd7f6d6907e9df0
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  sha256: 0b4028046165323ac97112fd1d275008a01e3cb312c092de1fd4beac1192e8c8
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  sha256: 7fdbf9517d429254eec8f84ebf206c30f76a19113d271e78047830c8bfec61af
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/services/ui_gateway/ui_gateway_server.cpp
  sha256: 49895019a2b7f78c60bb0bbe0c7b90f843be504c8ceba22fc21ce6c1d8854469
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
  sha256: 9a8a751e6837cd96fd2785523fc8a3b26cb5a63dbf4d0e698ef078b952b7b8b9
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/tests/forward/twin/CMakeLists.txt
  sha256: 23dd911c2a3376f910e76b2dcc2897082973e2432dc006181d1714419861bf9f
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/tests/forward/twin/test_forward_protocol.cpp
  sha256: 7a95a4cf7b34bd8551236106df31689e56aa0212fed2a32187c6231e3762b60c
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  sha256: 8bfc20665f9700a31a1915238ef9730fee6336720303f16434bae79ddd8a0b5f
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/third_party/build.sh
  sha256: 06ea9dce70a762a7b179c67a7835e01a060783b811da847baf88f6b40c92fd4e
- path: /tmp/qa_sandboxes/TWIN-49_run_200436_20261104_120436/soc-ap/tools/deploy_twin.sh
  sha256: 763a6bc1d0065d9ff37a1924b84f04cf25ab5f3c1e4af074e38f143d8d37ca5c
verification_scope: 审阅范围为 TWIN-49 接受的软件及 POSIX PTY 验证：921600 波特率、0x10..0x1C 命令与双单播
  ACK 闭环、网关 D-Bus 控制及离线/失败拦截、第三方库自动构建和部署前清理。跨编译器 ELF 构建与实体 MCU USB/UART HIL 属排除项；未声称这些硬件验证通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核验冻结索引、请求、差异及相关源码哈希。Runner 记录全栈构建和三组 CTest 通过；但候选未满足部署前清理的明确接受条款。
