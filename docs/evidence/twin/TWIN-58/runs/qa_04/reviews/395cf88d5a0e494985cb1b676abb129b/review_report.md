```yaml
task_id: TWIN-58
task_revision: 5
candidate_commit: c6692b244e0aa09d04e7051293f9fef3c67535dd
role: QA
decision: BLOCKED
summary: 已校验 bundle、上一轮 QA 报告及本轮定向 diff 的 SHA256。增量证据补足了前后端 G-code 内容负例；AP-3 注释规范符合性仍无法核实。
findings:
- 阻断：验收要求 AP-3 目标范围内代码符合 code_documentation_standard.md。冻结日志中的审计仅统计中文注释行数并检查占位文本，没有提供规范正文或逐项规范检查结果，因而不能确认符合性。该项延续自上一轮未解决的阻断。
- 非阻断建议：冻结 Runner 记录显示全栈构建、1 项 ui_gateway CTest、19 项 Python 契约测试通过；同时记录前端 G-code 校验四例及后端有效扩展名下非法正文返回
  400 的路由用例。
accepted_scope: 复验 TWIN-58 revision 5，聚焦候选 19534a9a4cb393176882fbad046129d55bba51f6
  到 c6692b244e0aa09d04e7051293f9fef3c67535dd 的增量及其受影响验收范围：ISS-20261105-006/007/008/009/010/011/013/017、AP-3
  注释补齐，以及冻结 Runner 所记录的必要 UI 回归。冻结证据显示构建、CTest 和 19 项 Python 测试成功。TWIN-57/TWIN-59
  合并批次改动及物理 HIL 不在本次软件沙箱验收范围内。
unexecuted:
- 核对 AP-3 目标文件是否逐项符合 code_documentation_standard.md；当前证据仅有注释行数及占位文本检查，未能完成规范符合性核验。
actual_session: 01a1ae8f-78a9-7832-b60a-63ddc3fb676d
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=960f079647a00864fe7913836336b2a2ee3d729a;
  soc-ap=c6692b244e0aa09d04e7051293f9fef3c67535dd; mcu-p3=891a8bb252814c83992a49b01fbe11ba83b92a1f;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-58
  task_revision: 5
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: f41a1222ae60
    id: TWIN-58_run_095234_20261106_015234
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234
    developer_mounts: []
    container_inspect:
      id: f41a1222ae6064950cbb6152a18d3cde18c27bee34fcb8d9d63db9c2595e0646
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-06T01:53:06.133520167Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-58_l6ubt9un/evidence/server_lock.json
    sha256: e094a3e350cca0142ac7009a88029eaa619e31d9ff54ee1d82eae63dbc31bf77
  checkout_log:
    path: /tmp/qa_TWIN-58_l6ubt9un/evidence/checkout.log
    sha256: 9edcc224b93ac4f1d25d54a88ed7f27c793da6c418f5b6dcaba5ad8d4fcae414
  runtime_log:
    path: /tmp/qa_TWIN-58_l6ubt9un/evidence/runtime.log
    sha256: 18d6003293096bfca877306e9197b738e85391f77f9601f7e51974f1e8fc4042
  server_verdict:
    path: /tmp/qa_TWIN-58_l6ubt9un/evidence/server_verdict.json
    sha256: 42c0a2b34c8ffae4b8e6a375cc6b48058b4067675947241a684fd23ca36fe66c
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin58 && mkdir -p /tmp/qa_twin58 && cp -r ../soc-ap /tmp/qa_twin58/soc-ap
      && rm -rf /tmp/qa_twin58/soc-ap/build && ([ -e /tmp/qa_twin58/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin58/soc-ap/third_party && ln -s /usr/local /tmp/qa_twin58/soc-ap/third_party/install))
      && cd /tmp/qa_twin58/soc-ap && bash tools/deploy_twin.sh --build-only && ctest
      --test-dir build/ui_gateway --output-on-failure && python3 -m unittest -v browser_hmi/first_release/test_hmi_contract.py
      tests/ui/twin/test_ui_contract.py && python3 -c "import base64; s=base64.b64decode(\"aW1wb3J0IHBhdGhsaWIsIHJlCmpzID0gcGF0aGxpYi5QYXRoKCJicm93c2VyX2htaS9maXJzdF9yZWxlYXNlL2FwcC5qcyIpLnJlYWRfdGV4dChlbmNvZGluZz0idXRmLTgiKQptID0gcmUuc2VhcmNoKHIiKGZ1bmN0aW9uXHMraXNWYWxpZEdjb2RlRmlsZVxzKlwoW14pXSpcKVxzKlx7W1xzXFNdKj9cbiAgICBcfSkiLCBqcykKYXNzZXJ0IG0sICJpc1ZhbGlkR2NvZGVGaWxlIG5vdCBmb3VuZCIKZm5fYm9keSA9IG0uZ3JvdXAoMSkKcHJpbnQoIltGUk9OVEVORC1BVURJVF0gRXh0cmFjdGVkIGlzVmFsaWRHY29kZUZpbGUgZnJvbSBicm93c2VyX2htaS9maXJzdF9yZWxlYXNlL2FwcC5qczoiKQpwcmludChmbl9ib2R5KQpleHRfcmUgPSByZS5jb21waWxlKHIiXC4oZ2NvZGV8Z2NvfG5jKSQiLCByZS5JKQpjbWRfcmUgPSByZS5jb21waWxlKHIiXlxzKltHTVRdXGQrIiwgcmUuSSB8IHJlLk0pCmRlZiBldmFsX2lzX3ZhbGlkX2djb2RlKG5hbWUsIHNpemUsIGNvbnRlbnQpOgogICAgaWYgbm90IG5hbWUgb3Igbm90IGV4dF9yZS5zZWFyY2goc3RyKG5hbWUpLnN0cmlwKCkpOgogICAgICAgIHJldHVybiBGYWxzZQogICAgaWYgbm90IGlzaW5zdGFuY2Uoc2l6ZSwgKGludCwgZmxvYXQpKSBvciBzaXplIDw9IDA6CiAgICAgICAgcmV0dXJuIEZhbHNlCiAgICBpZiBpc2luc3RhbmNlKGNvbnRlbnQsIHN0cik6CiAgICAgICAgaWYgbGVuKGNvbnRlbnQuc3RyaXAoKSkgPT0gMDoKICAgICAgICAgICAgcmV0dXJuIEZhbHNlCiAgICAgICAgbGluZXMgPSBjb250ZW50LnNwbGl0bGluZXMoKQogICAgICAgIGhhc19jbWQgPSBGYWxzZQogICAgICAgIGZvciBpIGluIHJhbmdlKG1pbihsZW4obGluZXMpLCA1MDApKToKICAgICAgICAgICAgc3RyaXBwZWQgPSBsaW5lc1tpXS5zcGxpdCgiOyIpWzBdLnN0cmlwKCkKICAgICAgICAgICAgaWYgc3RyaXBwZWQgYW5kIGNtZF9yZS5tYXRjaChzdHJpcHBlZCk6CiAgICAgICAgICAgICAgICBoYXNfY21kID0gVHJ1ZQogICAgICAgICAgICAgICAgYnJlYWsKICAgICAgICBpZiBub3QgaGFzX2NtZDoKICAgICAgICAgICAgcmV0dXJuIEZhbHNlCiAgICByZXR1cm4gVHJ1ZQoKY2FzZXMgPSBbCiAgICAoImJhZC50eHQiLCAyMSwgIkcyOFxuRzEgWDEwIFkxMCBGMTUwMFxuIiwgRmFsc2UpLAogICAgKCJlbXB0eS5nY29kZSIsIDAsICIiLCBGYWxzZSksCiAgICAoImJhZF9ib2R5Lmdjb2RlIiwgMjksICJOT1RfR0NPREVfQ09OVEVOVFxucmFuZG9tIHRleHQiLCBGYWxzZSksCiAgICAoIm9rLmdjb2RlIiwgMzEsICJHMjhcbk0xMDQgUzIwMFxuRzEgWDEwIFkxMCBGMTUwMFxuIiwgVHJ1ZSksCl0KZm9yIG5hbWUsIHN6LCBib2R5LCBleHBlY3RlZCBpbiBjYXNlczoKICAgIGFjdHVhbCA9IGV2YWxfaXNfdmFsaWRfZ2NvZGUobmFtZSwgc3osIGJvZHkpCiAgICBwcmludChmIltGUk9OVEVORC1DQVNFXSBuYW1lPXtuYW1lfSBzaXplPXtzen0gLT4gYWN0dWFsPXthY3R1YWx9IGV4cGVjdGVkPXtleHBlY3RlZH0iKQogICAgYXNzZXJ0IGFjdHVhbCBpcyBleHBlY3RlZCwgZiJNaXNtYXRjaCBmb3Ige25hbWV9IgpwcmludCgiW1BBU1NdIEZyb250ZW5kIGlzVmFsaWRHY29kZUZpbGUgNC1jYXNlIG5lZ2F0aXZlL3Bvc2l0aXZlIHZlcmlmaWNhdGlvbiBwYXNzZWQiKQoKZmlsZXMgPSBzb3J0ZWQoCiAgICBsaXN0KHBhdGhsaWIuUGF0aCgic2VydmljZXMvdWlfZ2F0ZXdheSIpLmdsb2IoIiouW2NoXSoiKSkKICAgICsgWwogICAgICAgIHBhdGhsaWIuUGF0aCgiYnJvd3Nlcl9obWkvZmlyc3RfcmVsZWFzZS9hcHAuanMiKSwKICAgICAgICBwYXRobGliLlBhdGgoImJyb3dzZXJfaG1pL2ZpcnN0X3JlbGVhc2UvdGVzdF9obWlfY29udHJhY3QucHkiKSwKICAgICAgICBwYXRobGliLlBhdGgoInVpL3R3aW4vYXBwLmpzIiksCiAgICAgICAgcGF0aGxpYi5QYXRoKCJ0b29scy9kZXBsb3lfdHdpbi5zaCIpLAogICAgICAgIHBhdGhsaWIuUGF0aCgidGVzdHMvdWlfZ2F0ZXdheS90d2luL3Rlc3RfdWlfZ2F0ZXdheS5jcHAiKSwKICAgICAgICBwYXRobGliLlBhdGgoInRlc3RzL3VpX2dhdGV3YXkvdHdpbi90ZXN0X3VpX2dhdGV3YXlfcm91dGVzLmNwcCIpLAogICAgICAgIHBhdGhsaWIuUGF0aCgidGVzdHMvdWkvdHdpbi90ZXN0X3VpX2NvbnRyYWN0LnB5IiksCiAgICBdCikKY2prID0gcmUuY29tcGlsZShyIltcdTRlMDAtXHU5ZmZmXSIpCmFzc2VydCBsZW4oZmlsZXMpID49IDE5LCBmIkV4cGVjdGVkID49MTkgZmlsZXMsIGdvdCB7bGVuKGZpbGVzKX0iCmZvciBmIGluIGZpbGVzOgogICAgdHh0ID0gZi5yZWFkX3RleHQoZW5jb2Rpbmc9InV0Zi04IikKICAgIGNqa19saW5lcyA9IHN1bSgxIGZvciBsIGluIHR4dC5zcGxpdGxpbmVzKCkgaWYgY2prLnNlYXJjaChsKSkKICAgIGFzc2VydCAi5Lit5paH6K+05piO77ya5qih5Z2X6L6F5Yqp6YC76L6R5LiO54q25oCB6K+05piOIiBub3QgaW4gdHh0LCBmIlBsYWNlaG9sZGVyIGluIHtmfSIKICAgIGFzc2VydCBjamtfbGluZXMgPj0gMywgZiJJbnN1ZmZpY2llbnQgQ2hpbmVzZSBjb21tZW50cyBpbiB7Zn0iCiAgICBwcmludChmIltET0MtQVVESVQgUEFTU10ge2Z9OiBjamtfY29tbWVudF9saW5lcz17Y2prX2xpbmVzfSIpCnByaW50KGYiW1BBU1NdIEFsbCB7bGVuKGZpbGVzKX0gQmF0Y2ggQVAtMyBmaWxlcyB2ZXJpZmllZCBjb21wbGlhbnQgd2l0aCBjb2RlX2RvY3VtZW50YXRpb25fc3RhbmRhcmQubWQiKQ==\").decode();
      exec(s)" && rm -rf /tmp/qa_twin58
    exit_code: '0'
    subpath: soc-ap
    duration: 11.12s
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
      \ have been written to: /tmp/qa_twin58/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin58/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 25%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin58/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 66%] Linking CXX executable test_backoff\n[ 66%] Linking CXX executable test_service_lifecycle\n\
      [ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin58/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 75%] Built target test_backoff\n[ 75%] Built target test_service_lifecycle\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin58/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin58/soc-ap/build/forward\n\
      [  4%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [  8%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 12%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 29%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 54%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 58%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 75%] Linking CXX static library libforward_service.a\n[ 75%] Built target\
      \ forward_service\n[ 79%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/tests/forward/twin/test_forward_service.cpp.o\n\
      [ 87%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/tests/forward/twin/test_forward_protocol.cpp.o\n\
      [ 91%] Linking CXX executable forward_service_daemon\n[ 95%] Linking CXX executable\
      \ test_forward_protocol\n[ 95%] Built target forward_service_daemon\n[ 95%]\
      \ Built target test_forward_protocol\n[100%] Linking CXX executable test_forward_service\n\
      [100%] Built target test_forward_service\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin58/soc-ap/build/test_forward\n[  7%] Building CXX\
      \ object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 89%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 97%] Linking CXX executable test_forward_protocol\n[100%] Linking CXX executable\
      \ test_forward_service\n[100%] Built target test_forward_protocol\n[100%] Built\
      \ target test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin58/soc-ap/build/device_manager\n\
      [  4%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
      [  9%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 13%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 27%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 54%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 59%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin58/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 63%] Linking CXX static library libdevice_manager.a\n[ 63%] Built target device_manager\n\
      [ 72%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin58/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 72%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/test_device_manager.dir/tmp/qa_twin58/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_device_manager.dir/tmp/qa_twin58/soc-ap/tests/device_manager/twin/test_device_manager.cpp.o\n\
      [ 86%] Linking CXX executable device_manager_daemon\n[ 90%] Building CXX object\
      \ CMakeFiles/test_device_manager.dir/tmp/qa_twin58/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 95%] Linking CXX executable test_device_manager_state\n[ 95%] Built target\
      \ device_manager_daemon\n[ 95%] Built target test_device_manager_state\n[100%]\
      \ Linking CXX executable test_device_manager\n[100%] Built target test_device_manager\n\
      [BUILD 4/5] ui_gateway (build/ui_gateway)...\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler\
      \ ABI info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n\
      -- Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Configuring done (0.1s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin58/soc-ap/build/ui_gateway\n[  7%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n[ 14%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n[ 21%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n[ 28%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n[ 35%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n[ 42%] Building CXX object\
      \ CMakeFiles/ui_gateway.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin58/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 78%] Building CXX object CMakeFiles/ui-gateway.dir/ui_gateway_main.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin58/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
      [ 92%] Linking CXX executable ui-gateway\n[100%] Linking CXX executable test_ui_gateway_routes\n\
      [100%] Built target ui-gateway\n[100%] Built target test_ui_gateway_routes\n\
      [BUILD 5/5] host CLI (build/host)...\n-- The CXX compiler identification is\
      \ GNU 9.4.0\n-- Detecting CXX compiler ABI info\n-- Detecting CXX compiler ABI\
      \ info - done\n-- Check for working CXX compiler: /usr/bin/c++ - skipped\n--\
      \ Detecting CXX compile features\n-- Detecting CXX compile features - done\n\
      -- Found Python3: /usr/bin/python3.8 (found version \"3.8.10\") found components:\
      \ Interpreter\n-- MiniMC QA test suite not enabled (MINIMC_QA_ROOT not set)\n\
      -- Configuring done (0.2s)\n-- Generating done (0.0s)\n-- Build files have been\
      \ written to: /tmp/qa_twin58/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 66%]\
      \ Building CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n\
      [ 77%] Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      Test project /tmp/qa_twin58/soc-ap/build/ui_gateway\n    Start 1: test_ui_gateway_routes\n\
      1/1 Test #1: test_ui_gateway_routes ...........   Passed    0.07 sec\n\n100%\
      \ tests passed out of 1\n\nTotal Test time (real) =   0.07 sec\n[FRONTEND-AUDIT]\
      \ Extracted isValidGcodeFile from browser_hmi/first_release/app.js:\nfunction\
      \ isValidGcodeFile(fileName, fileSize, fileText) {\n        if (!fileName ||\
      \ typeof fileName !== 'string') return false;\n        if (!(/\\.(gcode|gco|nc)$/i.test(fileName.trim())))\
      \ return false;\n        if (typeof fileSize === 'number' && fileSize <= 0)\
      \ return false;\n        if (typeof fileText === 'string') {\n            if\
      \ (fileText.trim().length === 0) return false;\n            if (!(/^\\s*[GMT]\\\
      d+/im.test(fileText))) return false;\n        }\n        return true;\n    }\n\
      [FRONTEND-CASE] name=bad.txt size=21 -> actual=False expected=False\n[FRONTEND-CASE]\
      \ name=empty.gcode size=0 -> actual=False expected=False\n[FRONTEND-CASE] name=bad_body.gcode\
      \ size=29 -> actual=False expected=False\n[FRONTEND-CASE] name=ok.gcode size=31\
      \ -> actual=True expected=True\n[PASS] Frontend isValidGcodeFile 4-case negative/positive\
      \ verification passed\n[DOC-AUDIT PASS] browser_hmi/first_release/app.js: cjk_comment_lines=277\n\
      [DOC-AUDIT PASS] browser_hmi/first_release/test_hmi_contract.py: cjk_comment_lines=35\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_dbus.cpp: cjk_comment_lines=32\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_dbus.h: cjk_comment_lines=59\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_http.cpp: cjk_comment_lines=41\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_http.h: cjk_comment_lines=34\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_job_ctrl.cpp: cjk_comment_lines=22\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_job_ctrl.h: cjk_comment_lines=71\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_main.cpp: cjk_comment_lines=13\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_server.cpp: cjk_comment_lines=157\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_server.h: cjk_comment_lines=32\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_service.cpp: cjk_comment_lines=21\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_service.h: cjk_comment_lines=19\n\
      [DOC-AUDIT PASS] services/ui_gateway/ui_gateway_types.h: cjk_comment_lines=46\n\
      [DOC-AUDIT PASS] tests/ui/twin/test_ui_contract.py: cjk_comment_lines=13\n[DOC-AUDIT\
      \ PASS] tests/ui_gateway/twin/test_ui_gateway.cpp: cjk_comment_lines=60\n[DOC-AUDIT\
      \ PASS] tests/ui_gateway/twin/test_ui_gateway_routes.cpp: cjk_comment_lines=27\n\
      [DOC-AUDIT PASS] tools/deploy_twin.sh: cjk_comment_lines=50\n[DOC-AUDIT PASS]\
      \ ui/twin/app.js: cjk_comment_lines=55\n[PASS] All 19 Batch AP-3 files verified\
      \ compliant with code_documentation_standard.md\n\ntest_01_dom_elements_contract\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验 index.html\
      \ 包含全部必需的 DOM 元素 ID。 ... ok\ntest_02_strict_realism_rule_positive_and_negative\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验严格真实性规则：未接入硬件严禁显示伪造\
      \ PASS 或绿色在线态。 ... ok\ntest_03_color_mixing_10000_weight_invariant (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n\
      校验 TWIN-17 10000 混色权重逻辑与快捷配比预设。 ... ok\ntest_04_i18n_dictionary_parity (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n\
      校验 zh-CN 与 en-US 双语字典键名 100% 对齐。 ... ok\ntest_05_styles_touch_targets_and_themes\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验触控热区 >= 44px\
      \ 及 styles.css 深浅双主题定义。 ... ok\ntest_06_slot_schema_validation (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n\
      校验 slot_schema.json 结构与 10000 权重约束。 ... ok\ntest_07_real_dual_mcu_firmware_version_presentation\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验双 MCU 真实固件版本展示与\
      \ 5 种防御状态映射。 ... ok\ntest_08_e2e_dashboard_and_motion_contract (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n\
      校验 TWIN-33/TWIN-34 打印工作台与运控调平 DOM 契约及 SSE 监听。 ... ok\ntest_09_hardware_offline_banner_and_pills_contract\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验 TWIN-39\
      \ 硬件离线横幅、双状态胶囊、哨兵温度与 503 锁定契约。 ... ok\ntest_10_oobe_finish_and_navigation_persistence_contract\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验 OOBE 向导完成后的标签页跳转、LocalStorage\
      \ 持久化与 Toast 提示。 ... ok\ntest_11_oobe_status_refresh_contract (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n\
      校验 OOBE 在线状态与遥测 DOM 刷新契约。 ... ok\ntest_12_twin58_issues_007_008_009_010_011_013_contract\
      \ (browser_hmi.first_release.test_hmi_contract.TestHMIContract)\n校验 TWIN-58\
      \ (ISS-007/008/009/010/011/013) 保存料槽解耦、模型载入两阶段、G-code 校验与离线去假绿契约。 ... ok\ntest_01_html_dom_elements_contract\
      \ (tests.ui.twin.test_ui_contract.TestUIContract)\n校验 index.html 中存在全部必需的 DOM\
      \ 元素 ID。 ... ok\ntest_02_viewport_and_responsive_meta (tests.ui.twin.test_ui_contract.TestUIContract)\n\
      校验适配触控屏与移动端的 viewport 响应式 meta 标签。 ... ok\ntest_03_real_api_endpoints_binding\
      \ (tests.ui.twin.test_ui_contract.TestUIContract)\n校验 app.js 绑定真实 REST 快照、即时采样\
      \ POST 与 SSE 事件流接口。 ... ok\ntest_04_no_synthetic_or_random_temperatures (tests.ui.twin.test_ui_contract.TestUIContract)\n\
      反向断言：确保前端绝不使用 Math.random 或定时器伪造温度数据。 ... ok\ntest_05_sentinel_fault_and_offline_handling\
      \ (tests.ui.twin.test_ui_contract.TestUIContract)\n校验 app.js 显式处理 0x7FFF 故障哨兵与\
      \ 0x7FFE 离线哨兵。 ... ok\ntest_06_css_touchscreen_responsive_breakpoints (tests.ui.twin.test_ui_contract.TestUIContract)\n\
      校验 800x480 触控屏响应式断点及数据品质徽章样式类。 ... ok\ntest_07_anti_repeat_sample_debounce_lock\
      \ (tests.ui.twin.test_ui_contract.TestUIContract)\n校验即时采样按钮的防抖冷却锁定逻辑。 ... ok\n\
      \n----------------------------------------------------------------------\nRan\
      \ 19 tests in 0.012s\n\nOK"
  passed: true
  timestamp: '2026-11-06T01:53:19.860844+00:00'
  path: /tmp/qa_TWIN-58_l6ubt9un/evidence/server_qa.json
  sha256: 23b3e91935bc1bff7b09db487a82ec9bcacb0009cfebcb6ac63ccf8f31dbe0cc
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-58_l6ubt9un/reviews/395cf88d5a0e494985cb1b676abb129b/codex.jsonl
  sha256: 2e8db5543b86c2234be0b782a4b51d39c6423d7eba528fe4880fb1abc354e42d
reviewed_artifacts:
- path: /tmp/qa_TWIN-58_l6ubt9un/request.json
  sha256: b9ff543169a4511e3be73ae3ecabb6655c1f81890f5fdce0f29881dac57f5ead
- path: /tmp/qa_TWIN-58_l6ubt9un/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-58_l6ubt9un/diffs/soc-ap.patch
  sha256: 2dab474ad7086f4c8918a31e69e8ff10732d83fb1b850858b96ce1f31afbf31c
- path: /tmp/qa_TWIN-58_l6ubt9un/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-58_l6ubt9un/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.cpp
  sha256: 11d1b8409fbe5e74e5d06a9d4f82539f6324a2c2646e7e6eae45fdd84974a67d
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_server.h
  sha256: 5a3e078156dd423585a1fbce5c125b5bc44b0019caf340ed5dadf22b84f1f800
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_types.h
  sha256: 2afe3e33998e962cd10b60e7204511b85ee4310159292dad25ed41d5d102574f
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_service.h
  sha256: b7fd715e84fbb67be9bc325b589ac03538614f98db31fe3b5c1f4d3a67166e11
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_http.h
  sha256: e1905e9767b3ac54a046f6c293747fa965181de74a3360cf5fe71a949be24148
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_server.cpp
  sha256: decfd0f18587dc9e13fd174b17b8fb14eb8c324a1fc00811f3ae79eb8800dcf9
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_job_ctrl.h
  sha256: ab7c7c16caf5b09b3f787f1d0538fede8b905797b282f0a45b16283a9eeefe97
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/CMakeLists.txt
  sha256: 0c60befc1b411d748f50297a09e59f8f106eedc939aeb659565b1913ea1cd902
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_service.cpp
  sha256: 564d975f6aefdb293a1927e9debe9038a1c15dc9db5096fa82089785f7f5884e
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_dbus.h
  sha256: 5726b50080058bfbdea96f76370b3cbe7122a780b2507742f3d99b94f0dfb70d
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_http.cpp
  sha256: 5b5e4a1ebf09d4a27de909b6154afe33c50d4b5082149142be6f68a3a3bd775b
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_dbus.cpp
  sha256: 9b7c01de6efdeff528c795f5a68dee3ef7e14fcac8284571bc755e52f5afa3a6
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/services/ui_gateway/ui_gateway_main.cpp
  sha256: 47f20ca69de0b4e599e0d5858235925e317f3f9bf2635366b74ca86e53fb9ce1
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/browser_hmi/first_release/test_hmi_contract.py
  sha256: 8adfa90da0ac12b551064735f4e81bd230ffa5431a2ca248fe0db11ae51a778f
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/browser_hmi/first_release/app.js
  sha256: 048db7082eab9f0f8751ef692e4205ea1ec77b72859824af49ac819660f02095
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/browser_hmi/first_release/styles.css
  sha256: b750052bcd4ca83602d610c647a0e5fb6e11a78de22947455a95ca7efb91c3a1
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/browser_hmi/first_release/index.html
  sha256: bd241a24e9fb64e0fdd16b0f84def5e6fe4397cdc13f721c605e7a3a02c90131
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/browser_hmi/first_release/slot_schema.json
  sha256: 8089dfea214639782542ea36be2cdeb244704e771c637cad49aebde8ffa88417
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/ui/twin/app.js
  sha256: 13cf845cabf33523b4208441c78b5632a8bd8df71ade025d4cebcf9e369c23b8
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/tools/deploy_twin.sh
  sha256: 5815b9eebf60c1ef3a479eafd46b911d3b966c2cf00fb142ea96bb721b8bfba7
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp
  sha256: 9693e224b9a882c7e9ac9f948aeb987775d44f87785969714354cd034e6fe746
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/tests/ui_gateway/twin/CMakeLists.txt
  sha256: f1b26e0dcd92b4d7489b3e28515034190015fcb82f052a1c2d9b6dd3fb8317f9
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/tests/ui_gateway/twin/test_ui_gateway.cpp
  sha256: 825cb421908333ad593a441f64acc3553254fdccf5c92c4c1cd9b901f632ca6c
- path: /tmp/qa_sandboxes/TWIN-58_run_095234_20261106_015234/soc-ap/tests/ui/twin/test_ui_contract.py
  sha256: 49a03ad0e20ddf5a92b6ffa1b4d4e107341cd4e315d32400c10b8e826190651b
verification_scope: 复验 TWIN-58 revision 5，聚焦候选 19534a9a4cb393176882fbad046129d55bba51f6
  到 c6692b244e0aa09d04e7051293f9fef3c67535dd 的增量及其受影响验收范围：ISS-20261105-006/007/008/009/010/011/013/017、AP-3
  注释补齐，以及冻结 Runner 所记录的必要 UI 回归。冻结证据显示构建、CTest 和 19 项 Python 测试成功。TWIN-57/TWIN-59
  合并批次改动及物理 HIL 不在本次软件沙箱验收范围内。
verification_environment: docker-sandbox-and-independent-codex-audit
```

已校验 bundle、上一轮 QA 报告及本轮定向 diff 的 SHA256。增量证据补足了前后端 G-code 内容负例；AP-3 注释规范符合性仍无法核实。
