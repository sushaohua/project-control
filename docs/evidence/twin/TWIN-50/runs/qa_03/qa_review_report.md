```yaml
task_id: TWIN-50
task_revision: 1
candidate_commit: d14ed04321c6d4f5ddb35a8801604a8af53b5b60
role: QA
decision: APPROVED
summary: 复验通过。本轮修复了上一候选的数值失配负向拦截问题；锁定证据覆盖接受范围内的静态、自检及完整 PTY 正向、负向、离线和恢复流程。
findings:
- 复验上下文：同角色上一轮 QA 报告 SHA256 与快照一致（968a2aeda26e8b4fc8fbaf974e4d1e85519036a8122e97f32586aa55ee9c57ee）。上一候选因数值失配仍报告成功且命令链中止而被拒绝。本轮增量
  diff SHA256 与索引一致（01efa0f85732a6314a35ff9ca087acd79535ac6880be093876a6f1cbbff194b6），修改范围仅为探针的失配注入和恢复控制。
- 本轮冻结运行证据显示在线五类对账通过；失配被探针报为坐标/归位掩码不匹配，CRC 错误和环形缓冲丢包（mc_drop=3）均产生拦截失败信号。串联命令以退出码
  0 完成，随后离线哨兵对账、恢复后的在线对账及服务清理均有证据。
- 静态证据显示旁路残留检查、17 个 MiniMCProto V2 命令码对齐和探针 11 项自检通过。候选源码 SHA256 与已校验索引中声明的工件哈希一致。review_bundle、运行日志和服务器
  verdict 哈希均与索引提供值一致；source_report 为空。
- 非阻断建议：失配注入与恢复分支可检查 sync_online 控制命令的返回值，避免控制步骤失败时仅凭 HTTP 状态返回成功。该建议不影响本轮冻结证据支持的结论。
accepted_scope: 复核 TWIN-50 revision 1 的锁定候选及接受范围：测试夹具移除旁路、17 个命令码静态对齐、探针自检，以及 921600
  PTY 全栈五类业务正向对账、数值失配/坏 CRC/环形缓冲丢包负向拦截、OFFLINE 单位哨兵和 HTTP 503 锁定、ONLINE 恢复对账及部署/PTY
  生命周期。排除交叉编译器 ELF 构建与物理 MCU SWD/USB/UART HIL；本次未声称这些硬件验证通过。
unexecuted: []
actual_session: 01a1a6f3-2867-7ce0-9e0d-6ddcd2830e13
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=17e0887da07ceb3b017623b791b6a6999e837c79;
  soc-ap=333178c66280e785ae1a5c089a6e2a05075cc926; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-50
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 5f7edef7b12f
    id: TWIN-50_run_222422_20261104_142422
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422
    developer_mounts: []
    container_inspect:
      id: 5f7edef7b12fe75b07af2bd1f5e3ab0b3cf396a39c85781b63413e6e2e7dd9fc
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-04T14:24:46.100451133Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-50_16d6hfoh/evidence/server_lock.json
    sha256: 0c1597f7ceef623770102e518a536a7cb7c0f4c83733664f66f5a36654b6ba6b
  checkout_log:
    path: /tmp/qa_TWIN-50_16d6hfoh/evidence/checkout.log
    sha256: 0e3c970d438ae357583dd43ea4d6a68e30382705d6e24673eab8a69552c9f513
  runtime_log:
    path: /tmp/qa_TWIN-50_16d6hfoh/evidence/runtime.log
    sha256: fd637f035203fde655b8a69e8633c4d9635f7b2c06a6bff145ee34bd428a1885
  server_verdict:
    path: /tmp/qa_TWIN-50_16d6hfoh/evidence/server_verdict.json
    sha256: d81b3963654ba5a1e59efd150d441cec988d8c1dd03076e8557f3934d12af4a9
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: (! grep -rnE "normalize_ap_temp_wire_frame|mc_bridge_notify_|th_bridge_notify_"
      test_cases/twin/ hil/tools/debug_reconciliation_probe.py) && python3 static_checks/minimcproto/check_opcode_alignment.py
      && python3 hil/tools/debug_reconciliation_probe.py --help >/dev/null && python3
      hil/tools/debug_reconciliation_probe.py --self-test --matrix-out /tmp/qa_twin50_selftest.md
      && test -s /tmp/qa_twin50_selftest.md && rm -f /tmp/qa_twin50_selftest.md
    exit_code: '0'
    subpath: test_harness
    duration: 0.22s
    output: "=== MiniMCProto V2 Cross-Repo Opcode Alignment Gate ===\n  [OK]   0x00\
      \ (ACK              ) aligned across soc-ap / MC / TH\n  [OK]   0x01 (GET_VERSION\
      \      ) aligned across soc-ap / MC / TH\n  [OK]   0x02 (VERSION_REPORT   )\
      \ aligned across soc-ap / MC / TH\n  [OK]   0x03 (PING             ) aligned\
      \ across soc-ap / MC / TH\n  [OK]   0x04 (PONG             ) aligned across\
      \ soc-ap / MC / TH\n  [OK]   0x06 (NACK             ) aligned across soc-ap\
      \ / MC / TH\n  [OK]   0x10 (SET_TEMP         ) aligned across soc-ap / MC /\
      \ TH\n  [OK]   0x11 (MOTION_HOME      ) aligned across soc-ap / MC / TH\n  [OK]\
      \   0x12 (MOTION_MOVE      ) aligned across soc-ap / MC / TH\n  [OK]   0x13\
      \ (JOB_CONTROL      ) aligned across soc-ap / MC / TH\n  [OK]   0x15 (TEMP_REPORT\
      \      ) aligned across soc-ap / MC / TH\n  [OK]   0x16 (POS_QUERY        )\
      \ aligned across soc-ap / MC / TH\n  [OK]   0x17 (MOTION_STOP      ) aligned\
      \ across soc-ap / MC / TH\n  [OK]   0x18 (LEVEL_GRID_QUERY ) aligned across\
      \ soc-ap / MC / TH\n  [OK]   0x19 (SLOT_SELECT      ) aligned across soc-ap\
      \ / MC / TH\n  [OK]   0x1A (LEVEL_TRIGGER    ) aligned across soc-ap / MC /\
      \ TH\n  [OK]   0x1C (GCODE_EXEC       ) aligned across soc-ap / MC / TH\n\n\
      [PASSED] All 17 MiniMCProto V2 opcodes are 100% aligned.\n[PASS] debug_reconciliation_probe.py\
      \ self-test suite passed (11 fixtures generated)."
  - command: rm -rf /tmp/qa_twin50 && mkdir -p /tmp/qa_twin50/bin && python3 -c "import
      pathlib; p=pathlib.Path(\"/tmp/qa_twin50/bin/curl\"); p.write_text(\"#!/usr/bin/env
      python3\nimport sys,urllib.request,urllib.error\nu=[a for a in sys.argv[1:]
      if a.startswith(\x27http\x27)][-1]\nw=\x27-w\x27 in sys.argv\ntry:\n r=urllib.request.urlopen(u,timeout=2);b=r.read();sys.stdout.write(str(r.status))
      if w else sys.stdout.buffer.write(b)\nexcept urllib.error.HTTPError as e:\n
      sys.stdout.write(str(e.code)) if w else None;sys.exit(0 if w else 22)\nexcept
      Exception:\n sys.stdout.write(\x27000\x27) if w else None;sys.exit(7)\n\");
      p.chmod(0o755)" && export PATH="/tmp/qa_twin50/bin:$PATH" && cp -r ../soc-ap
      ../mcu-p3 ../test_harness /tmp/qa_twin50/ && rm -rf /tmp/qa_twin50/soc-ap/build
      && ([ -e /tmp/qa_twin50/soc-ap/third_party/install ] || (mkdir -p /tmp/qa_twin50/soc-ap/third_party
      && ln -s /usr/local /tmp/qa_twin50/soc-ap/third_party/install)) && cd /tmp/qa_twin50/soc-ap
      && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"start-pty\",
      \"/tmp/qa_twin50\"))" && bash tools/deploy_twin.sh --mode hardware --uart "$(cat
      /tmp/qa_twin50/pty_path)" --baud 921600 --port 18086 && bash tools/deploy_twin.sh
      --status --port 18086 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-online\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log
      /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/live_ok_matrix.md &&
      python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\"); import
      debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-mismatch\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log
      /tmp/qa_twin50/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"restore-mismatch\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 -c "import sys;
      sys.path.insert(0, \"../test_harness/hil/tools\"); import debug_reconciliation_probe
      as p; sys.exit(p.live_pty_ctl(\"inject-crc-err\", \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))"
      && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py --ap-url
      http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log /tmp/qa_twin50/th_live.log)
      && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"inject-drop\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && (! python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log
      /tmp/qa_twin50/th_live.log) && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-offline\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log
      /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/live_offline_matrix.md
      && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"drive-recovery\",
      \"/tmp/qa_twin50\", \"http://127.0.0.1:18086\"))" && python3 ../test_harness/hil/tools/debug_reconciliation_probe.py
      --ap-url http://127.0.0.1:18086 --mc-log /tmp/qa_twin50/mc_live.log --th-log
      /tmp/qa_twin50/th_live.log --matrix-out /tmp/qa_twin50/reconciliation_matrix.md
      && test -s /tmp/qa_twin50/live_ok_matrix.md && test -s /tmp/qa_twin50/live_offline_matrix.md
      && test -s /tmp/qa_twin50/reconciliation_matrix.md && bash tools/deploy_twin.sh
      --stop --port 18086 && python3 -c "import sys; sys.path.insert(0, \"../test_harness/hil/tools\");
      import debug_reconciliation_probe as p; sys.exit(p.live_pty_ctl(\"stop-pty\",
      \"/tmp/qa_twin50\"))" && rm -rf /tmp/qa_twin50
    exit_code: '0'
    subpath: soc-ap
    duration: 26.27s
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
      \ have been written to: /tmp/qa_twin50/soc-ap/build/runtime\n[  8%] Building\
      \ CXX object CMakeFiles/aisoc_runtime_common.dir/tmp/qa_twin50/soc-ap/runtime/common/service_lifecycle.cpp.o\n\
      [ 16%] Linking CXX static library libaisoc_runtime_common.a\n[ 16%] Built target\
      \ aisoc_runtime_common\n[ 41%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin50/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/test_backoff.dir/tests/test_backoff.cpp.o\n\
      [ 41%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tests/test_supervisor_topology.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_service_lifecycle.dir/tests/test_service_lifecycle.cpp.o\n\
      [ 58%] Linking CXX executable test_service_lifecycle\n[ 66%] Linking CXX executable\
      \ test_backoff\n[ 66%] Built target test_service_lifecycle\n[ 66%] Built target\
      \ test_backoff\n[ 75%] Building CXX object CMakeFiles/test_supervisor_topology.dir/tmp/qa_twin50/soc-ap/runtime/vmware/supervisor.cpp.o\n\
      [ 83%] Building CXX object CMakeFiles/aisoc_supervisor.dir/tmp/qa_twin50/soc-ap/runtime/vmware/main.cpp.o\n\
      [ 91%] Linking CXX executable aisoc_supervisor\n[100%] Linking CXX executable\
      \ test_supervisor_topology\n[100%] Built target aisoc_supervisor\n[100%] Built\
      \ target test_supervisor_topology\n[BUILD 2/5] forward (build/forward & build/test_forward)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin50/soc-ap/build/forward\n\
      [  5%] Building CXX object CMakeFiles/forward_service.dir/forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/forward_service.dir/forward_uart.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_dbus.cpp.o\n\
      [ 20%] Building CXX object CMakeFiles/forward_service.dir/forward_service.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 30%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 40%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 45%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 70%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 80%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 85%] Building CXX object CMakeFiles/forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 90%] Linking CXX static library libforward_service.a\n[ 90%] Built target\
      \ forward_service\n[ 95%] Building CXX object CMakeFiles/forward_service_daemon.dir/forward_main.cpp.o\n\
      [100%] Linking CXX executable forward_service_daemon\n[100%] Built target forward_service_daemon\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin50/soc-ap/build/test_forward\n\
      [  2%] Building CXX object CMakeFiles/test_forward_service.dir/test_forward_service.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [  7%] Building CXX object CMakeFiles/test_forward_protocol.dir/test_forward_protocol.cpp.o\n\
      [ 10%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/services/forward/forward_protocol.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 15%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/services/forward/forward_uart.cpp.o\n\
      [ 18%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 23%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/services/forward/forward_dbus.cpp.o\n\
      [ 26%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 31%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/services/forward/forward_service.cpp.o\n\
      [ 34%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 36%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 39%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 47%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/codec.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 52%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/minimc/parser.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/core/forward/transport/serial_posix.cpp.o\n\
      [ 60%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 63%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 65%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 68%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 73%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 76%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 78%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 81%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 84%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 86%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_protocol.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 92%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 94%] Building CXX object CMakeFiles/test_forward_service.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 97%] Linking CXX executable test_forward_protocol\n[100%] Linking CXX executable\
      \ test_forward_service\n[100%] Built target test_forward_protocol\n[100%] Built\
      \ target test_forward_service\n[BUILD 3/5] device_manager (build/device_manager)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin50/soc-ap/build/device_manager\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/device_manager_state.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/device_manager_service.cpp.o\n\
      [ 16%] Building CXX object CMakeFiles/device_manager.dir/device_manager_dbus.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 27%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 38%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 44%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 55%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 61%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 66%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 72%] Building CXX object CMakeFiles/device_manager.dir/tmp/qa_twin50/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 77%] Linking CXX static library libdevice_manager.a\n[ 77%] Built target device_manager\n\
      [ 88%] Building CXX object CMakeFiles/device_manager_daemon.dir/device_manager_main.cpp.o\n\
      [ 88%] Building CXX object CMakeFiles/test_device_manager_state.dir/tmp/qa_twin50/soc-ap/tests/device_manager/twin/test_device_manager_state.cpp.o\n\
      [ 94%] Linking CXX executable device_manager_daemon\n[100%] Linking CXX executable\
      \ test_device_manager_state\n[100%] Built target device_manager_daemon\n[100%]\
      \ Built target test_device_manager_state\n[BUILD 4/5] ui_gateway (build/ui_gateway)...\n\
      -- The CXX compiler identification is GNU 9.4.0\n-- Detecting CXX compiler ABI\
      \ info\n-- Detecting CXX compiler ABI info - done\n-- Check for working CXX\
      \ compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n-- Detecting\
      \ CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating done\
      \ (0.0s)\n-- Build files have been written to: /tmp/qa_twin50/soc-ap/build/ui_gateway\n\
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_service.cpp.o\n\
      [ 21%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_dbus.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_http.cpp.o\n\
      [ 28%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_server.cpp.o\n\
      [ 35%] Building CXX object CMakeFiles/ui_gateway.dir/ui_gateway_job_ctrl.cpp.o\n\
      [ 42%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_msg.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_core.cpp.o\n\
      [ 57%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_client.cpp.o\n\
      [ 64%] Building CXX object CMakeFiles/ui_gateway.dir/tmp/qa_twin50/soc-ap/middleware/dbus/src/aisoc_dbus_server.cpp.o\n\
      [ 71%] Linking CXX static library libui_gateway.a\n[ 71%] Built target ui_gateway\n\
      [ 85%] Building CXX object CMakeFiles/test_ui_gateway_routes.dir/tmp/qa_twin50/soc-ap/tests/ui_gateway/twin/test_ui_gateway_routes.cpp.o\n\
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
      \ written to: /tmp/qa_twin50/soc-ap/build/host\n[ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/parser.cpp.o\n\
      [ 22%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/minimc/codec.cpp.o\n\
      [ 33%] Building CXX object CMakeFiles/minimcproto.dir/core/forward/transport/serial_posix.cpp.o\n\
      [ 44%] Linking CXX static library libminimcproto.a\n[ 44%] Built target minimcproto\n\
      [ 55%] Building CXX object CMakeFiles/soc-ap.dir/core/host/main.cpp.o\n[ 77%]\
      \ Building CXX object CMakeFiles/soc-ap.dir/core/host/query.cpp.o\n[ 77%] Building\
      \ CXX object CMakeFiles/minimc-probe.dir/tests/protocol/probe.cpp.o\n[ 88%]\
      \ Linking CXX executable bin/soc-ap\n[ 88%] Built target soc-ap\n[100%] Linking\
      \ CXX executable bin/minimc-probe\n[100%] Built target minimc-probe\n=================================================================\n\
      [BUILD] All 5 full-stack targets built successfully.\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full Stack Deployed Successfully!\n  Mode:        hardware\n  UART: \
      \       /dev/pts/0 @ 921600 baud\n  HTTP URL:    http://127.0.0.1:18086/\n \
      \ State API:   http://127.0.0.1:18086/api/v1/state\n  Snapshot:    http://127.0.0.1:18086/api/v1/temperature/snapshot\n\
      \  Logs & PIDs: /tmp/aisoc_twin_logs\n=================================================================\n\
      =================================================================\nAI-SoC VMware\
      \ Twin Full-Stack Status (Mode: hardware)\n  UART Device: /dev/pts/0 @ 921600\
      \ baud\n  HTTP Listen: 0.0.0.0:18086\n=================================================================\n\
      \  [RUNNING] dbus-daemon (PID: 1016)\n  [RUNNING] forward_service_daemon (PID:\
      \ 1021)\n  [RUNNING] device_manager_daemon (PID: 1022)\n  [RUNNING] ui-gateway\
      \ (PID: 1024)\n  [HEALTH ] HTTP Probe http://127.0.0.1:18086/api/v1/state ->\
      \ HTTP 200 OK\n=================================================================\n\
      [PASS] Live AP gateway (http://127.0.0.1:18086) reconciliation succeeded (online-5-category).\n\
      [PASS] Live AP gateway (http://127.0.0.1:18086) reconciliation succeeded (offline-sentinel).\n\
      [PASS] Live AP gateway (http://127.0.0.1:18086) reconciliation succeeded (online-5-category).\n\
      [STOP] Stopping ui-gateway (PID: 1024)...\n[STOP] Stopping device_manager_daemon\
      \ (PID: 1022)...\n[STOP] Stopping forward_service_daemon (PID: 1021)...\n[STOP]\
      \ Stopping dbus-daemon (PID: 1016)...\n[STOP] All AI-SoC VMware Twin services\
      \ stopped and PID files cleaned.\n\n[RECONCILE FAIL] 2. Homing & Motion Control:\
      \ Motion coordinates or homed_mask mismatch\n[RECONCILE FAIL] MC-DBG seq=9 cmd=0x14\
      \ status=CRC_ERR err=0x01\n[RECONCILE FAIL] MC-DBG seq=9 cmd=0x14 status=CRC_ERR\
      \ err=0x01\n[RECONCILE FAIL] Ring buffer overflow/truncation detected: mc_drop=3,\
      \ mc_trunc=0, th_drop=0, th_trunc=0"
  passed: true
  timestamp: '2026-11-04T14:25:15.278604+00:00'
  path: /tmp/qa_TWIN-50_16d6hfoh/evidence/server_qa.json
  sha256: 0ad9adfe379746d1093350b5e5ddb60c67f69ae63617d3c28b7ebc772d3d85eb
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-50_16d6hfoh/reviews/485b27e0cb0347d589754f27c0db68d0/codex.jsonl
  sha256: 7e0200814954f381f706e489c8d01089655363b65e7c2575a2cd4a1969b4a241
reviewed_artifacts:
- path: /tmp/qa_TWIN-50_16d6hfoh/request.json
  sha256: b03645bc72d375443b12edc057f9c2da0b443fb2f802686b5a2e13733965ef33
- path: /tmp/qa_TWIN-50_16d6hfoh/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-50_16d6hfoh/diffs/soc-ap.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-50_16d6hfoh/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-50_16d6hfoh/diffs/test_harness.patch
  sha256: a4ff7436c1681a6dc352302b1cd43e1bb8402cd76731ef57568ff93244528fd7
- path: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422/test_harness/hil/tools/debug_reconciliation_probe.py
  sha256: b062d2dfd411e128eba7dd44f7ec54a390db908adc749700a572b3f25d2fb68d
- path: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422/test_harness/test_cases/twin/twin46_mc_bridge.c
  sha256: c579f785506f8dc3378efefd5147e1f1464729282b20cd5eb66e2a21ffd61c6f
- path: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422/test_harness/test_cases/twin/twin46_th_bridge.c
  sha256: 6be80801bbcfc17e142fe48479cb6aaed985724f9370acf4769a439fb02390a4
- path: /tmp/qa_sandboxes/TWIN-50_run_222422_20261104_142422/test_harness/static_checks/minimcproto/check_opcode_alignment.py
  sha256: bcc098de7793d08c79f391be82f55a1d3b099b9984f8db08952722ad8b1253e9
verification_scope: 复核 TWIN-50 revision 1 的锁定候选及接受范围：测试夹具移除旁路、17 个命令码静态对齐、探针自检，以及
  921600 PTY 全栈五类业务正向对账、数值失配/坏 CRC/环形缓冲丢包负向拦截、OFFLINE 单位哨兵和 HTTP 503 锁定、ONLINE 恢复对账及部署/PTY
  生命周期。排除交叉编译器 ELF 构建与物理 MCU SWD/USB/UART HIL；本次未声称这些硬件验证通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

复验通过。本轮修复了上一候选的数值失配负向拦截问题；锁定证据覆盖接受范围内的静态、自检及完整 PTY 正向、负向、离线和恢复流程。
