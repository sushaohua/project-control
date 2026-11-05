```yaml
task_id: TWIN-53
task_revision: 1
candidate_commit: 87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a
role: QA
decision: APPROVED
summary: 已完成锁定候选的只读独立审阅；证据索引、范围、定向差异及 Runner 原始记录相符，接受条款均有覆盖，未发现阻断项。
findings:
- 非阻断建议：deploy_twin.sh 在找不到 setsid 时会静默退回 nohup；该分支不能保证独立 session。当前 Runner 记录的验收环境会话隔离检查通过。
accepted_scope: 已审阅 soc-ap/tools/deploy_twin.sh 与 soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
  的定向差异，以及 Runner 对应原始证据。索引及证据哈希、提交绑定、允许改动路径均核对一致。记录覆盖四进程存活与非僵尸状态、独立会话和 SIGHUP 后存活、fd/0
  指向 /dev/null、--status 与 HTTP 200、单进程故障检测、启动期崩溃拒绝误报和清理、--stop 回收。排除范围：交叉编译 ELF、宿主
  cgroup/容器 teardown 存活验证及实体 MCU USB/UART HIL；未声称这些硬件或环境验证通过。source_report 为空，无需报告哈希核对。
unexecuted: []
actual_session: 01a1a9ae-e883-7270-8cdd-358b3b47aed9
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd;
  soc-ap=87c3bd31b1adc9f17fcc75aa5d7ea26beb44e59a; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-53
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 15a59ef01344
    id: TWIN-53_run_110856_20261105_030856
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-53_run_110856_20261105_030856
    developer_mounts: []
    container_inspect:
      id: 15a59ef013445deaab238fb3f074bdc24f1815b01b3c8a7966ea2509409d5460
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-05T03:09:17.361702765Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-53_run_110856_20261105_030856
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-53_sxew_tmh/evidence/server_lock.json
    sha256: 642eb5195bcd3da8fefba41caa578a1338eae5a59f3dbf81645c7d19dc5c139c
  checkout_log:
    path: /tmp/qa_TWIN-53_sxew_tmh/evidence/checkout.log
    sha256: 225d1a4adb07d5dec2ac0ed0f01c8a45559b5ae2e0bf1af5e19868e80b8b9737
  runtime_log:
    path: /tmp/qa_TWIN-53_sxew_tmh/evidence/runtime.log
    sha256: 9fbc6e5d273ba80da456323c77b7b6d08afa7183a3efdbde74781095bdffa20e
  server_verdict:
    path: /tmp/qa_TWIN-53_sxew_tmh/evidence/server_verdict.json
    sha256: cf786023bb7d336469e27c503b8d9be33c17759deb42616b10321071973b2c27
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin53 && mkdir -p /tmp/qa_twin53/bin && python3 -c "import
      pathlib; p=pathlib.Path(\"/tmp/qa_twin53/bin/curl\"); p.write_text(\"#!/usr/bin/env
      python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:]
      if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755)" && export PATH="/tmp/qa_twin53/bin:$PATH" && cp -r ../soc-ap
      /tmp/qa_twin53/soc-ap && ([ -e /tmp/qa_twin53/soc-ap/third_party/install ] ||
      (mkdir -p /tmp/qa_twin53/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin53/soc-ap/third_party/install))
      && cd /tmp/qa_twin53/soc-ap && bash tools/twin_build/test_deploy_daemon_survival.sh
      && rm -rf /tmp/qa_twin53
    exit_code: '0'
    subpath: soc-ap
    duration: 14.34s
    output: "=================================================================\n[TWIN-53]\
      \ Running deploy_twin.sh Daemon Survival & SIGHUP Tests...\n=================================================================\n\
      =================================================================\n[BUILD] Incrementally\
      \ building AI-SoC full stack...\n=================================================================\n\
      [BUILD 1/5] runtime (build/runtime)...\n-- The C compiler identification is\
      \ GNU 9.4.0\n-- The CXX compiler identification is GNU 9.4.0\n-- Detecting C\
      \ compiler ABI info\n-- Detecting C compiler ABI info - done\n-- Check for working\
      \ C compiler: /usr/bin/cc - skipped\n-- Detecting C compile features\n-- Detecting\
      \ C compile features - done\n-- Detecting CXX compiler ABI info\n-- Detecting\
      \ CXX compiler ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++\
      \ - skipped\n-- Detecting CXX compile features\n-- Detecting CXX compile features\
      \ - done\n-- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files\
      \ have been written to: /tmp/qa_twin53/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin53/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin53/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 58%] Linking CXX executable test_service_lifecycle\n[ 66%] Linking CXX executable\
      \ test_backoff\n[ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin53/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin53/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Built target test_service_lifecycle\n[ 83%] Built target test_backoff\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/forward\n\
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 30%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 80%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 90%] Linking CXX static library libforward_service.a\n[ 90%] Built target\
      \ forward_service\n[ 95%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [100%] Linking CXX executable forward_service_daemon\n[100%] Built target forward_service_daemon\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/test_forward\n\
      [  2%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 97%] Linking CXX executable test_forward_protocol\n[ 97%] Built target test_forward_protocol\n\
      [100%] Linking CXX executable test_forward_service\n[100%] Built target test_forward_service\n\
      [BUILD 3/5] device_manager (build/device_manager)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin53/soc-ap/build/device_manager\n[ 11%] Building CXX\
      \ object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n[ 11%] Building\
      \ CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n[ 16%]\
      \ Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 27%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 38%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 61%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 72%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 77%] Linking CXX static library libdevice_manager.a\n[ 77%] Built target device_manager\n\
      [ 83%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 88%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin53/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 94%] Linking CXX executable device_manager_daemon\n[100%] Linking CXX executable\
      \ test_device_manager_state\n[100%] Built target device_manager_daemon\n[100%]\
      \ Built target test_device_manager_state\n[BUILD 4/5] ui_gateway (build/ui_gateway)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/ui_gateway\n\
      [  7%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n\
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 78%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin53/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
      [ 92%] Linking CXX executable ui-gateway\n[100%] Linking CXX executable test_ui_gateway_routes\n\
      [100%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- The CXX compiler identification is\
      \ GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI\
      \ info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n--\
      \ Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Found Python3: /usr/bin/python3.8 (found version \"3.8.10\") found components:\
      \ Interpreter\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n\
      -- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin53/soc-ap/build/host\n[ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 66%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 66%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /tmp/aisoc_twin53_dummy_uart @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18093/\n\
      \  State API:   http://127.0.0.1:18093/api/v1/state\n  Snapshot:    http://127.0.0.1:18093/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      \  [OK] dbus.pid (PID=997, State=S, fd/0=/dev/null)\n  [OK] forward.pid (PID=1002,\
      \ State=S, fd/0=/dev/null)\n  [OK] device_manager.pid (PID=1003, State=S, fd/0=/dev/null)\n\
      \  [OK] ui_gateway.pid (PID=1005, State=S, fd/0=/dev/null)\n  [OK] SIGHUP delivered\
      \ to all 4 daemons and caller session; all 4 survived.\n=================================================================\n\
      AI-SoC VMware Twin Full-Stack Status (Mode: sim)\n  UART Device: /tmp/aisoc_twin53_dummy_uart\
      \ @ 921600 baud\n  HTTP Listen: 0.0.0.0:18093\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 997)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1002)\n  [RUNNING] device_manager_daemon (PID: 1003)\n  [RUNNING] ui-gateway\
      \ (PID: 1005)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18093/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      \  [OK] HTTP /api/v1/state (200) & /api/v1/temperature/snapshot (200)\n  [OK]\
      \ Negative check 1: --status correctly failed after forward_service_daemon crash.\n\
      \  [OK] Negative check 2: deploy_twin.sh rejected startup crash (exit 139) without\
      \ false positive.\n  [OK] Negative check 2 cleanup verified: all daemons terminated\
      \ and PID files removed.\n[STOP] Stopping ui-gateway (PID: 1406)...\n[STOP]\
      \ Stopping device_manager_daemon (PID: 1404)...\n[STOP] Stopping forward_service_daemon\
      \ (PID: 1403)...\n[STOP] Stopping dbus-daemon (PID: 1398)...\n[STOP] All AI-SoC\
      \ VMware Twin services stopped and PID files cleaned.\n  [OK] --stop verified:\
      \ all 4 daemon PIDs terminated and all PID files removed.\n=================================================================\n\
      [TWIN-53] ALL Daemon Survival & Crash Detection Tests PASSED!\n================================================================="
  passed: true
  timestamp: '2026-11-05T03:09:34.358728+00:00'
  path: /tmp/qa_TWIN-53_sxew_tmh/evidence/server_qa.json
  sha256: 4495d7f3374725f92968cfb8cf30de3b5d7cdab74fc57e73987c84e744cd237b
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-53_sxew_tmh/reviews/00b76e896ca24c7cb4818ec120cfd697/codex.jsonl
  sha256: 4c6bf166ca1781b694039dde1aabf655fcfd13e6fbfbaa22f21d67acbef91629
reviewed_artifacts:
- path: /tmp/qa_TWIN-53_sxew_tmh/request.json
  sha256: fd27f9ea98320b2be8dc1367b0571f35adc5ec0422d8dff32a458afea3e7d92d
- path: /tmp/qa_TWIN-53_sxew_tmh/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-53_sxew_tmh/diffs/soc-ap.patch
  sha256: 8b49e12e5e27b2fd594e05af03c135881699511d43b36af2d9831a4f0b14c698
- path: /tmp/qa_TWIN-53_sxew_tmh/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-53_sxew_tmh/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-53_run_110856_20261105_030856/soc-ap/tools/deploy_twin.sh
  sha256: cc087d098a8614439de7963591f545ac666e6da60161199c706de1a16860315e
- path: /tmp/qa_sandboxes/TWIN-53_run_110856_20261105_030856/soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
  sha256: eb54fdd3b46082dc1c61b8546acdc2a5dfdd88fbf4ff7eacd40226ed8d07ff57
verification_scope: 已审阅 soc-ap/tools/deploy_twin.sh 与 soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
  的定向差异，以及 Runner 对应原始证据。索引及证据哈希、提交绑定、允许改动路径均核对一致。记录覆盖四进程存活与非僵尸状态、独立会话和 SIGHUP 后存活、fd/0
  指向 /dev/null、--status 与 HTTP 200、单进程故障检测、启动期崩溃拒绝误报和清理、--stop 回收。排除范围：交叉编译 ELF、宿主
  cgroup/容器 teardown 存活验证及实体 MCU USB/UART HIL；未声称这些硬件或环境验证通过。source_report 为空，无需报告哈希核对。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已完成锁定候选的只读独立审阅；证据索引、范围、定向差异及 Runner 原始记录相符，接受条款均有覆盖，未发现阻断项。
