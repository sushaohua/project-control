```yaml
task_id: TWIN-53
task_revision: 1
candidate_commit: f4fb563675be959a8ebbbdda5444cd68cc0b2afa
role: QA
decision: BLOCKED
summary: Bundle、请求及冻结证据哈希与索引一致；候选差异仅涉及授权的两个 soc-ap 路径，源码哈希也与索引声明一致。Runner 记录的回归命令退出码为
  0，日志覆盖四进程存活、fd/0、HTTP、启动崩溃拒绝及 --status 负向检查。仍有验收必需的 SIGHUP 投递和进程回收后置条件未被可靠验证。评审说明与最终
  JSON 无法另行保存：当前工作区为只读。
findings:
- 阻断：测试脚本在部署子进程退出后才向其进程组发送 SIGHUP，并忽略 killpg 失败。候选实现用 setsid 将守护进程移出该进程组，因此测试可能遇到进程组已不存在而未投递任何
  SIGHUP；后续存活检查不能证明四进程经 SIGHUP 后仍存活。这影响已接受的“子会话退出 + SIGHUP 后四进程存活”条款。
- 阻断：测试调用 --stop 并记录其输出，但没有检查四个 PID 对应进程确已退出；启动期崩溃负向场景也没有检查残留进程。--stop 的成功提示由源码无条件输出，不能单独证明回收完成。这影响已接受的
  --stop 收敛和启动失败清理条款。
accepted_scope: 审阅 soc-ap/tools/deploy_twin.sh 与 soc-ap/tools/twin_build/test_deploy_daemon_survival.sh：检查依赖补丁、四守护进程会话隔离与启动探针、存活和
  fd/0、HTTP、状态、停止回收及崩溃负向路径。project-control、mcu-p3、test_harness 本轮无差异。跨编译器 ELF 构建、宿主
  cgroup/容器销毁后的存活以及实体 MCU USB/UART HIL 明确不适用并排除；未将其作为未执行项或声称通过。
unexecuted:
- 在验收回归中确认 SIGHUP 确实投递到目标进程或其原会话，并验证四守护进程存活。
- 在正常 --stop 及启动崩溃清理后验证所有守护进程均已退出，并核对相关 PID 文件清理。
actual_session: 01a1a9a2-b28f-7d13-badc-7ebf445cdc3f
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd;
  soc-ap=f4fb563675be959a8ebbbdda5444cd68cc0b2afa; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-53
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 4892051153a5
    id: TWIN-53_run_105529_20261105_025529
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-53_run_105529_20261105_025529
    developer_mounts: []
    container_inspect:
      id: 4892051153a5bd858fa47aec6d0c1d795f3f7977ea845fb68916c36a6ebd69a4
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-05T02:55:47.079845494Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-53_run_105529_20261105_025529
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-53_ugtz5iqd/evidence/server_lock.json
    sha256: 937f276a6324321c1dd2a1b5e824b08b51ba101f084dcae1e113d21b5f1ae9d4
  checkout_log:
    path: /tmp/qa_TWIN-53_ugtz5iqd/evidence/checkout.log
    sha256: 6f0cb219b7497cb76e12b26b6dc593b847903cb910748146b10e8298f4438c60
  runtime_log:
    path: /tmp/qa_TWIN-53_ugtz5iqd/evidence/runtime.log
    sha256: 6c150a72e43a090c95d3a9bd0d1049729743227554d9713859e070ad04dcad16
  server_verdict:
    path: /tmp/qa_TWIN-53_ugtz5iqd/evidence/server_verdict.json
    sha256: 43785682cb3ff3da9691b103f724582c2fb6aa266f6e6b7ea73f64639b7bbb41
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
    duration: 24.27s
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
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin53/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 66%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin53/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin53/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Built target test_backoff\n[ 83%] Built target test_service_lifecycle\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/forward\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
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
      [  2%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [  5%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/services/forward/forward_uart.cpp.o\n\
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
      [ 44%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin53/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin53/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
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
      [ 97%] Linking CXX executable test_forward_protocol\n[100%] Linking CXX executable\
      \ test_forward_service\n[100%] Built target test_forward_protocol\n[100%] Built\
      \ target test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/device_manager\n\
      [ 11%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 11%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
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
      [ 83%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin53/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 88%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 94%] Linking CXX executable device_manager_daemon\n[100%] Linking CXX executable\
      \ test_device_manager_state\n[100%] Built target device_manager_daemon\n[100%]\
      \ Built target test_device_manager_state\n[BUILD 4/5] ui_gateway (build/ui_gateway)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin53/soc-ap/build/ui_gateway\n\
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n\
      [ 14%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin53/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 78%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin53/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
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
      \ written to: /tmp/qa_twin53/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 66%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 55%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        sim\n  UART:      \
      \  /tmp/aisoc_twin53_dummy_uart @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18093/\n\
      \  State API:   http://127.0.0.1:18093/api/v1/state\n  Snapshot:    http://127.0.0.1:18093/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      \  [OK] dbus.pid (PID=995, State=S, fd/0=/dev/null)\n  [OK] forward.pid (PID=1000,\
      \ State=S, fd/0=/dev/null)\n  [OK] device_manager.pid (PID=1001, State=S, fd/0=/dev/null)\n\
      \  [OK] ui_gateway.pid (PID=1003, State=S, fd/0=/dev/null)\n=================================================================\n\
      AI-SoC VMware Twin Full-Stack Status (Mode: sim)\n  UART Device: /tmp/aisoc_twin53_dummy_uart\
      \ @ 921600 baud\n  HTTP Listen: 0.0.0.0:18093\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 995)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1000)\n  [RUNNING] device_manager_daemon (PID: 1001)\n  [RUNNING] ui-gateway\
      \ (PID: 1003)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18093/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      \  [OK] HTTP /api/v1/state (200) & /api/v1/temperature/snapshot (200)\n  [OK]\
      \ Negative check 1: --status correctly failed after forward_service_daemon crash.\n\
      \  [OK] Negative check 2: deploy_twin.sh rejected startup crash (exit 139) without\
      \ false positive.\n[STOP] All AI-SoC VMware Twin services stopped and PID files\
      \ cleaned.\n=================================================================\n\
      [TWIN-53] ALL Daemon Survival & Crash Detection Tests PASSED!\n================================================================="
  passed: true
  timestamp: '2026-11-05T02:56:14.074139+00:00'
  path: /tmp/qa_TWIN-53_ugtz5iqd/evidence/server_qa.json
  sha256: b4a0dbfaf6a4b42a56e9541243b838bbacfd05b389a9eca00755a1f1c3a34d1f
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-53_ugtz5iqd/reviews/1b7960a3032142e7a90c7086a72d0907/codex.jsonl
  sha256: 36eb561f49f2d2d23c019a20c4486589238e9583ebf83ad1579019ef484cc25f
reviewed_artifacts:
- path: /tmp/qa_TWIN-53_ugtz5iqd/request.json
  sha256: 1f5427eb7d9a762958f9bc8561072ec36e6cc6872c232f7aa3a806a1d27ee296
- path: /tmp/qa_TWIN-53_ugtz5iqd/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-53_ugtz5iqd/diffs/soc-ap.patch
  sha256: 6ceb0b32a45890670001d9b99d614d9a2ad22e4d189e95c946ec16c419e314d5
- path: /tmp/qa_TWIN-53_ugtz5iqd/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-53_ugtz5iqd/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-53_run_105529_20261105_025529/soc-ap/tools/deploy_twin.sh
  sha256: d7f0e1eda459f8c969170059c026bfbda7c15c78a967b662d92656b819647f54
- path: /tmp/qa_sandboxes/TWIN-53_run_105529_20261105_025529/soc-ap/tools/twin_build/test_deploy_daemon_survival.sh
  sha256: 83699e5803f9d452a9060b08a1fe5f2dc7636f2035d7c9ee033b60982aa88006
verification_scope: 审阅 soc-ap/tools/deploy_twin.sh 与 soc-ap/tools/twin_build/test_deploy_daemon_survival.sh：检查依赖补丁、四守护进程会话隔离与启动探针、存活和
  fd/0、HTTP、状态、停止回收及崩溃负向路径。project-control、mcu-p3、test_harness 本轮无差异。跨编译器 ELF 构建、宿主
  cgroup/容器销毁后的存活以及实体 MCU USB/UART HIL 明确不适用并排除；未将其作为未执行项或声称通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

Bundle、请求及冻结证据哈希与索引一致；候选差异仅涉及授权的两个 soc-ap 路径，源码哈希也与索引声明一致。Runner 记录的回归命令退出码为 0，日志覆盖四进程存活、fd/0、HTTP、启动崩溃拒绝及 --status 负向检查。仍有验收必需的 SIGHUP 投递和进程回收后置条件未被可靠验证。评审说明与最终 JSON 无法另行保存：当前工作区为只读。
