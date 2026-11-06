```yaml
task_id: TWIN-65
task_revision: 2
candidate_commit: 42a1dc4465b4a848c768283c570a48be63ec1e6b
role: QA
decision: REJECTED
summary: 已核验冻结证据与候选差异。构建成功，但 device_manager 集成回归失败，未满足接受范围要求的全套回归验证。
findings:
- 阻断：冻结日志记录 build/forward 的 2 项测试通过，device_manager 的状态测试与 firmware_updater 测试通过，但
  test_device_manager 在双节点版本同步场景失败：TH 版本状态未达到 ONLINE（test_device_manager.cpp:1438）。验收范围要求
  device_manager 全部单测及必要回归通过，因此该失败不符合接受条款。
- 评审说明：review_bundle.json 的 SHA256 与请求值一致；request.json、server_verdict.json、runtime.log
  及 soc-ap.patch 的 SHA256 与索引记录一致。冻结结果对应候选提交 42a1dc4465b4a848c768283c570a48be63ec1e6b。source_report
  为空，无需核对报告 SHA256。
- 已核查的日志显示五个构建目标成功构建，forward 两项测试通过，device_manager 的状态和固件升级器测试通过。未执行硬件验证，也未将其视为通过。
- 评审说明与最终 JSON 未能分别保存为文件：当前工作区为只读权限。
accepted_scope: 审查范围包括 Rev 2.0.4 协议与 520B 帧容量、/var/update staging 与 128B ATSG 预检、OTA
  安全准入与维护互斥、Stage 1–4 升级编排，以及 forward、device_manager、ui_gateway 回归和 S04/中文注释门禁。物理
  HIL 验证由 TWIN-67 覆盖，不在本任务接受范围内。
unexecuted:
- 因 device_manager 回归失败导致验证命令提前退出，ui_gateway CTest 未执行。
- S04 函数长度/参数数量门禁与中文注释门禁未执行。
actual_session: 01a1af49-8c3a-7952-92db-3988537299ab
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=6d8b9dc8a59366c9e0d0c8126240b1caf69ab321;
  soc-ap=42a1dc4465b4a848c768283c570a48be63ec1e6b; mcu-p3=57674d8b07d6c75a4d20b3fcd52c23df964aa7a7;
  test_harness=19c12bfeeac852670e8bdcb65ce0abcd1de121c1; boot/bootloadermc=4fc171ea61912561949b9a0cfc1da8975e4c39ba;
  boot/bootloaderth=769fccbe52464ad7ceb856c5e89cb0d25abbbf87
server_qa:
  task_id: TWIN-65
  task_revision: 2
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 7e53c82becb0
    id: TWIN-65_run_131535_20261106_051535
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535
    developer_mounts: []
    container_inspect:
      id: 7e53c82becb00d33749bff3e7572d060e3edccfc608c8fd65bef0bea2278912e
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T05:16:09.357825505Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-65_yxfyoku4/evidence/server_lock.json
    sha256: b1ab4ec2e9f55abd58830cfb5ac7b216bd5bdb6bcd122847e6a281ba1fe4c9f7
  checkout_log:
    path: /tmp/qa_TWIN-65_yxfyoku4/evidence/checkout.log
    sha256: f724610b4d900eecef62cf0dce1cba61cd5ff09f05a54e14c631b54276e62a5b
  runtime_log:
    path: /tmp/qa_TWIN-65_yxfyoku4/evidence/runtime.log
    sha256: 20dcb8c82140af3ebfd9d204291a29e2b3f295c5b33da7515c180ad3663330e7
  server_verdict:
    path: /tmp/qa_TWIN-65_yxfyoku4/evidence/server_verdict.json
    sha256: e247c80c5e2bff2727ae64eaea933b7a4c2880a67262d22a7c5cb8328b7eb10a
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: 'rm -rf /tmp/qa_twin65 && mkdir -p /tmp/qa_twin65 && cp -r ../soc-ap
      /tmp/qa_twin65/soc-ap && rm -rf /tmp/qa_twin65/soc-ap/build && ([ -e /tmp/qa_twin65/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin65/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin65/soc-ap/third_party/install))
      && cd /tmp/qa_twin65/soc-ap && bash tools/deploy_twin.sh --build-only && ctest
      --test-dir build/forward --output-on-failure && ctest --test-dir build/device_manager
      --output-on-failure && ctest --test-dir build/ui_gateway --output-on-failure
      && python3 -c ''exec("import re,pathlib\nfiles=[\"services/device_manager/firmware_updater.cpp\",\"services/device_manager/device_manager_state.cpp\",\"services/forward/forward_protocol.cpp\",\"services/forward/forward_uart.cpp\",\"services/forward/forward_service.cpp\",\"services/ui_gateway/ui_gateway_server.cpp\"]\nfor
      f in files:\n lines=pathlib.Path(f).read_text().splitlines(); i=0\n while i<len(lines):\n  s=lines[i].strip()\n  if
      s and not s.startswith((\"//\",\"/*\",\"*\",\"#\")) and \"(\" in s and not s.startswith((\"if\",\"for\",\"while\",\"switch\",\"return\")):\n   j=i\n   while
      \")\" not in s and j+1<len(lines): j+=1; s+=\" \"+lines[j].strip()\n   if s.endswith(\"{\")
      or (j+1<len(lines) and lines[j+1].strip().startswith(\"{\")):\n    m=re.search(r\"([A-Za-z_]\\w*)\\s*\\(([^)]*)\\)\",s)\n    if
      m and m.group(1) not in (\"if\",\"for\",\"while\",\"switch\"):\n     p=[x.strip()
      for x in m.group(2).split(\",\") if x.strip() and x.strip()!=\"void\"]\n     b=s.count(\"{\")-s.count(\"}\");
      k=j\n     if b==0 and k+1<len(lines) and lines[k+1].strip().startswith(\"{\"):
      k+=1; b=lines[k].count(\"{\")-lines[k].count(\"}\")\n     while b>0 and k+1<len(lines):
      k+=1; b+=lines[k].count(\"{\")-lines[k].count(\"}\")\n     assert len(p)<=4
      and (k-i+1)<=50, f\"{f}:{i+1} {m.group(1)} params={len(p)} len={k-i+1}\"\n     i=k+1;
      continue\n  i+=1\nprint(\"[PASS] S04 function length (<=50) and params (<=4)
      verified on all 6 files\")")'' && ! grep -rn "中文说明：模块辅助逻辑与状态说明" contracts/ services/
      tests/ && echo "[PASS] code_documentation_standard.md Chinese comment check
      passed" && rm -rf /tmp/qa_twin65'
    exit_code: '8'
    subpath: soc-ap
    duration: 22.55s
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
      \ have been written to: /tmp/qa_twin65/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin65/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin65/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 66%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin65/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin65/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 83%] Built target test_service_lifecycle\n[ 83%] Built target test_backoff\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin65/soc-ap/build/forward\n\
      [ 12%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 12%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 12%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 29%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 54%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 58%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 75%] Linking CXX static library libforward_service.a\n[ 75%] Built target\
      \ forward_service\n[ 79%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/tests/forward/twin/test_forward_service.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/tests/forward/twin/test_forward_protocol.cpp.o\n\
      [ 87%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [ 91%] Linking CXX executable forward_service_daemon\n[ 95%] Linking CXX executable\
      \ test_forward_protocol\n[ 95%] Built target forward_service_daemon\n[ 95%]\
      \ Built target test_forward_protocol\n[100%] Linking CXX executable test_forward_service\n\
      [100%] Built target test_forward_service\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin65/soc-ap/build/test_forward\n[  5%] Building CXX\
      \ object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n[ \
      \ 5%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 97%] Linking CXX executable test_forward_protocol\n[100%] Linking CXX executable\
      \ test_forward_service\n[100%] Built target test_forward_protocol\n[100%] Built\
      \ target test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin65/soc-ap/build/device_manager\n\
      [  4%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [  8%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
      [ 12%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/firmware_updater.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 24%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 32%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 48%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 56%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin65/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 60%] Linking CXX static library libdevice_manager.a\n[ 60%] Built target device_manager\n\
      [ 64%] Building CXX object CMakeFiles/test_firmware_updater.dir/tmp/qa_twin65/soc-ap/tests/device_manager/twin/test_firmware_updater.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 72%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin65/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_device_manager.dir/tmp/qa_twin65/soc-ap/tests/device_manager/twin/test_device_manager.cpp.o\n\
      [ 80%] Linking CXX executable device_manager_daemon\n[ 84%] Linking CXX executable\
      \ test_firmware_updater\n[ 88%] Linking CXX executable test_device_manager_state\n\
      [ 88%] Built target test_firmware_updater\n[ 92%] Building CXX object CMakeFiles/test_device_manager.dir/tmp/qa_twin65/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 96%] Building CXX object CMakeFiles/test_device_manager.dir/tmp/qa_twin65/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 96%] Built target device_manager_daemon\n[ 96%] Built target test_device_manager_state\n\
      [100%] Linking CXX executable test_device_manager\n[100%] Built target test_device_manager\n\
      [BUILD 4/5] ui_gateway (build/ui_gateway)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin65/soc-ap/build/ui_gateway\n[  7%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n[ 14%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n[ 21%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 28%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n[ 35%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n[ 42%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin65/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 78%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin65/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
      [ 92%] Linking CXX executable ui-gateway\n[100%] Linking CXX executable test_ui_gateway_routes\n\
      [100%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- The CXX compiler identification is\
      \ GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI\
      \ info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n--\
      \ Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Found Python3: /usr/bin/python3.8 (found version \"3.8.10\") found components:\
      \ Interpreter\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n\
      -- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin65/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 66%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin65/soc-ap/build/forward\n    Start 1: test_forward_service\n\
      1/2 Test #1: test_forward_service .............   Passed    1.25 sec\n    Start\
      \ 2: test_forward_protocol\n2/2 Test #2: test_forward_protocol ............\
      \   Passed    0.77 sec\n\n100% tests passed out of 2\n\nTotal Test time (real)\
      \ =   2.01 sec\nTest project /tmp/qa_twin65/soc-ap/build/device_manager\n  \
      \  Start 1: test_device_manager_state\n1/3 Test #1: test_device_manager_state\
      \ ........   Passed    0.23 sec\n    Start 2: test_firmware_updater\n2/3 Test\
      \ #2: test_firmware_updater ............   Passed    0.00 sec\n    Start 3:\
      \ test_device_manager\n3/3 Test #3: test_device_manager ..............***Failed\
      \    7.91 sec\n========================================================================\n\
      TWIN-08 / TWIN-29 Device Manager Verification & Integration Test Suite\n========================================================================\n\
      [RUN ] test_unit_state_init\n[PASS] test_unit_state_init\n[RUN ] test_unit_state_sample_update\n\
      [PASS] test_unit_state_sample_update\n[RUN ] test_unit_state_admission\n[PASS]\
      \ test_unit_state_admission\n[RUN ] test_unit_state_json\n[PASS] test_unit_state_json\n\
      [RUN ] test_unit_temp_conversion_and_json\n[PASS] test_unit_temp_conversion_and_json\n\
      [RUN ] test_unit_fault_sentinel_defense\n[PASS] test_unit_fault_sentinel_defense\n\
      [RUN ] test_unit_offline_sentinel_defense\n[PASS] test_unit_offline_sentinel_defense\n\
      [RUN ] test_unit_grid_proto_build_query\n[PASS] test_unit_grid_proto_build_query\n\
      [RUN ] test_unit_grid_proto_validate_positive_and_negative\n[PASS] test_unit_grid_proto_validate_positive_and_negative\n\
      [RUN ] test_unit_grid_proto_parse_raw\n[PASS] test_unit_grid_proto_parse_raw\n\
      [RUN ] test_unit_state_leveling_grid_and_json\n[PASS] test_unit_state_leveling_grid_and_json\n\
      [RUN ] test_unit_state_grid_defense\n[PASS] test_unit_state_grid_defense\n[RUN\
      \ ] test_unit_version_proto_build_query\n[PASS] test_unit_version_proto_build_query\n\
      [RUN ] test_unit_version_proto_validate_positive_and_negative\n[PASS] test_unit_version_proto_validate_positive_and_negative\n\
      [RUN ] test_unit_version_proto_parse_raw\n[PASS] test_unit_version_proto_parse_raw\n\
      [RUN ] test_unit_state_version_tracking_and_decay\n[PASS] test_unit_state_version_tracking_and_decay\n\
      [RUN ] test_unit_state_get_mcu_version\n[PASS] test_unit_state_get_mcu_version\n\
      [RUN ] test_unit_state_version_json_and_snapshot\n[PASS] test_unit_state_version_json_and_snapshot\n\
      [RUN ] test_unit_state_version_binding_exhaustion\n[PASS] test_unit_state_version_binding_exhaustion\n\
      [RUN ] test_unit_initial_offline_no_fake_online\n[PASS] test_unit_initial_offline_no_fake_online\n\
      [RUN ] test_unit_freshness_timeout_and_offline_sentinel\n[PASS] test_unit_freshness_timeout_and_offline_sentinel\n\
      [RUN ] test_unit_version_freshness_decay_and_system_status\n[PASS] test_unit_version_freshness_decay_and_system_status\n\
      [RUN ] [&]() { return test_rpc_get_snapshot(&env.cli_conn); }\n[PASS] [&]()\
      \ { return test_rpc_get_snapshot(&env.cli_conn); }\n[RUN ] [&]() { return test_dds_sync_and_signal(&env);\
      \ }\n[DEVICE_MGR DEBUG] DDS RX: node=1, temp=62000 millic (62.0 C) -> Snapshot\
      \ GEN=11 (DEGRADED)\n[PASS] [&]() { return test_dds_sync_and_signal(&env); }\n\
      [RUN ] [&]() { return test_rpc_request_sample(&env.cli_conn); }\n[PASS] [&]()\
      \ { return test_rpc_request_sample(&env.cli_conn); }\n[RUN ] [&]() { return\
      \ test_rpc_device_state_and_estop(&env.cli_conn); }\n[PASS] [&]() { return test_rpc_device_state_and_estop(&env.cli_conn);\
      \ }\n[RUN ] [&]() { return test_rpc_get_version_info(&env.cli_conn); }\n[PASS]\
      \ [&]() { return test_rpc_get_version_info(&env.cli_conn); }\n[RUN ] [&]() {\
      \ return test_fwd_link_state_signal_disconnect(&env); }\n[DEVICE_MGR WARN] LinkStateChanged\
      \ disconnected: node=1, reason=SERIAL_HANGUP\n[PASS] [&]() { return test_fwd_link_state_signal_disconnect(&env);\
      \ }\n[RUN ] [&]() { return test_dds_version_sync_dual_nodes(&env); }\n[DEVICE_MGR\
      \ DEBUG] DDS RX: node=2, temp=210000 millic (210.0 C) -> Snapshot GEN=12 (EMERGENCY_STOP_INVOKED)\n\
      \  [FAIL] /tmp/qa_twin65/soc-ap/tests/device_manager/twin/test_device_manager.cpp:1438:\
      \ TH ver status ONLINE\n[FAIL] [&]() { return test_dds_version_sync_dual_nodes(&env);\
      \ }\n========================================================================\n\
      Total: Passed=28, Failed=1\n========================================================================\n\
      \n\n67% tests passed, 1 tests failed out of 3\n\nTotal Test time (real) =  \
      \ 8.15 sec\n\nThe following tests FAILED:\n\t  3 - test_device_manager (Failed)\n\
      \nErrors while running CTest"
  passed: false
  timestamp: '2026-11-06T05:16:34.677912+00:00'
  path: /tmp/qa_TWIN-65_yxfyoku4/evidence/server_qa.json
  sha256: ec4eb2323d3561c3dee1167f4fc928dcab0186675597125bdede1479609d64c0
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-65_yxfyoku4/reviews/1af623b7f9e548fe9c306fdaa51faa48/codex.jsonl
  sha256: e9f9bae7980a16b564f517852a2b401307c22f35757755d793ecad447e66a7ec
reviewed_artifacts:
- path: /tmp/qa_TWIN-65_yxfyoku4/request.json
  sha256: 333e85c4b7cd7a9020e6ebcf849393307d43d6b6a78496f0d232d157fa8ef9f8
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/soc-ap.patch
  sha256: f00a3d8ff137fb8048256ec927a46710b2633a299288a9eced9a60a9a60f13f0
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/boot/bootloadermc.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-65_yxfyoku4/diffs/boot/bootloaderth.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/contracts/twin/telemetry_types.h
  sha256: fef5322c43c7202285da74a7bf51f12652c38cbbee7763f6f14349bab1443048
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_uart.cpp
  sha256: 705bd88c190a6bd5f9a330910cc35ff37c105db7521f8ba0f446b15250d96b4a
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_service.cpp
  sha256: 6f3a0fd9d9699d53b4338e6ee672fd7d0155e96c983cb89eacc4ef18ae75d11f
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_uart.h
  sha256: 8eaf61513b1ccba87bc42202a857d2277fd1d7c7bc46890948d44fba63c31097
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_dbus.cpp
  sha256: 561bc25d9bad1f5e89052a33d4127190d026b2adf34fd25d36dde1383e3bb769
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_service.h
  sha256: 7117000f6c41d30de05b44159b99a0b2beb389202436cac9f712d27f63899667
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_types.h
  sha256: f9dfbaa26d94be752dfe93013a977474e61f013777bcc37071c30e2663cbaeec
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/CMakeLists.txt
  sha256: a75af1f9b8e28ff0e96b322df99597e75d1ff7d947100cf09bdb3f0cff37a33c
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_main.cpp
  sha256: f9150ccc0a9ce435cb972e6b350e5038877da688b28d51c1c62bbca677189ada
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_protocol.h
  sha256: 3a89ff428052a24eefdd4482ea61c47872fcebb567ab8c7d7ac9fbd0cca582e9
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_protocol.cpp
  sha256: 3a43c2f5c71b19c3c12c5cc82a40bda5c32dc1f956e31bead08f342ec43229cb
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/forward/forward_dbus.h
  sha256: d778c1763ae2fd0d0b8d9fd24eeaa28caac335d6e7ddacb322d281cb83ca23be
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_service.h
  sha256: f4c712e4396261f247e07e0cd95c87e4fccf2560ee91ff7531e6b066606b90ab
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_dbus.h
  sha256: a70244fdbf88bd6aa9a9de0733b141c34e06d410404ac8f7e03c93713b28f466
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_service.cpp
  sha256: cca2ceb4b2282f87bb6b2ef0647d04cf8ab179f973927fb223189bca88677997
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/firmware_updater.h
  sha256: bb2a493d2ddbf806917f4295c804f4c4ac4c331929a474280115e5cdc21c3c45
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_state.cpp
  sha256: 4e3dacd9a2d5aa5b4aaf59cf619b4848e20d91b4fed2cc38fc2cab834bcb6ae5
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/firmware_updater.cpp
  sha256: 04980b8ff1233fb7f5e597dd6eb1387515b0e0ccad3c5c16eac50695d92ba3bb
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_dbus.cpp
  sha256: 806f5b60d6f0e0619f16643f6333496aae17092dfa04125e5f77487850da8ade
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/CMakeLists.txt
  sha256: cccd56975d6f89f5194cb335d0d25b7661aacfd1aef3444ba160287df97ebcac
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_main.cpp
  sha256: a4700539daba9b7a787c992bde2cab1cd25c4457c67b5c21f3da1824f12fdef7
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_types.h
  sha256: 8f158e7aedbc4914aed776885424817164784d07534081f391a17f497c92ed32
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/device_manager/device_manager_state.h
  sha256: d3581c554258d0c248b3c90e5c1baa33a3403f87e8f69383b2f971e071dadac6
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  sha256: 11d1b8409fbe5e74e5d06a9d4f82539f6324a2c2646e7e6eae45fdd84974a67d
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_server.h
  sha256: 0cfe589e6600ef64725ceae3890d2bfd7dfe4dcb9c3c6a007ff23c6005306bc7
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_types.h
  sha256: 2afe3e33998e962cd10b60e7204511b85ee4310159292dad25ed41d5d102574f
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_service.h
  sha256: b7fd715e84fbb67be9bc325b589ac03538614f98db31fe3b5c1f4d3a67166e11
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_http.h
  sha256: e1905e9767b3ac54a046f6c293747fa965181de74a3360cf5fe71a949be24148
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_server.cpp
  sha256: 35682527564c2dc492cbae8526e8d6296512df4a5ffd12c7f230fc4fd39845e2
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  sha256: ab7c7c16caf5b09b3f787f1d0538fede8b905797b282f0a45b16283a9eeefe97
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/CMakeLists.txt
  sha256: 0c60befc1b411d748f50297a09e59f8f106eedc939aeb659565b1913ea1cd902
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_service.cpp
  sha256: 564d975f6aefdb293a1927e9debe9038a1c15dc9db5096fa82089785f7f5884e
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_dbus.h
  sha256: 5726b50080058bfbdea96f76370b3cbe7122a780b2507742f3d99b94f0dfb70d
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_http.cpp
  sha256: 5b5e4a1ebf09d4a27de909b6154afe33c50d4b5082149142be6f68a3a3bd775b
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  sha256: 9b7c01de6efdeff528c795f5a68dee3ef7e14fcac8284571bc755e52f5afa3a6
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/services/ui_gateway/ui_gateway_main.cpp
  sha256: 47f20ca69de0b4e599e0d5858235925e317f3f9bf2635366b74ca86e53fb9ce1
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/forward/twin/test_forward_protocol.cpp
  sha256: 0290ae5222206d405526b54130e39f2c0f5f8c6fe6543973b8182e0981ebf101
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/forward/twin/CMakeLists.txt
  sha256: 23dd911c2a3376f910e76b2dcc2897082973e2432dc006181d1714419861bf9f
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/forward/twin/test_forward_service.cpp
  sha256: e4ce8b890b5f5fadaa1afca50b2670e6acf7d9f87665d65daf2c04441599dbf2
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp
  sha256: cdca853cf9590dc1cad6db0ebc0d038393d9a77709cabbe33981784a3c00431e
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/device_manager/twin/test_device_manager.cpp
  sha256: 1cc95942709cac3cf595fd54e098362e76aae6640fae37b0f3c5f6ea09c01e36
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/device_manager/twin/CMakeLists.txt
  sha256: f3c29c80b0433662d8db74a593ad55f0ec220de9b7cf4194b2e476d4803da6db
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/device_manager/twin/test_firmware_updater.cpp
  sha256: f0abf9ef0adc23fd83d8b2925bbe86cde70bc9c22a9dc7f0e556db13dd682493
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  sha256: 9a02c5168834b7a05349f2cce9caf95634699a2e4c8e8e80e5ad4f6e09a9c69f
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/ui_gateway/twin/CMakeLists.txt
  sha256: f1b26e0dcd92b4d7489b3e28515034190015fcb82f052a1c2d9b6dd3fb8317f9
- path: /tmp/qa_sandboxes/TWIN-65_run_131535_20261106_051535/soc-ap/tests/ui_gateway/twin/test_ui_gateway.cpp
  sha256: 825cb421908333ad593a441f64acc3553254fdccf5c92c4c1cd9b901f632ca6c
verification_scope: 审查范围包括 Rev 2.0.4 协议与 520B 帧容量、/var/update staging 与 128B ATSG
  预检、OTA 安全准入与维护互斥、Stage 1–4 升级编排，以及 forward、device_manager、ui_gateway 回归和 S04/中文注释门禁。物理
  HIL 验证由 TWIN-67 覆盖，不在本任务接受范围内。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已核验冻结证据与候选差异。构建成功，但 device_manager 集成回归失败，未满足接受范围要求的全套回归验证。
