```yaml
task_id: TWIN-52
task_revision: 1
candidate_commit: 68b926e4376185a4979869a4787b90c8623a9164
role: QA
decision: REJECTED
summary: 候选未满足负向恢复验收：触发安装头文件守卫缺失后，build.sh fastcdr 未能修复安装结果，后续 verify 仍失败。
findings:
- 阻断：验收要求安装头文件缺少守卫时拒绝放行并重新打补丁构建，且构建及复核通过。冻结运行记录显示源码目录的 optional.hpp 已有两处守卫，但安装步骤将安装目录中的头文件报告为“Up-to-date”；随后
  verify 仍因缺少守卫而失败（runtime.log，SHA256 已核验）。这证明候选在该验收场景下未完成恢复；命令在运行 CTest 前退出。
accepted_scope: 审阅 Fast-CDR 补丁与 third_party/build.sh 的补丁应用、安装校验和负向恢复，以及 optional 回归和
  DDS CTest。跨编译器 ELF 构建及实体 MCU USB/UART HIL 属于排除项，不作为未执行项目。bundle、request、server verdict、runtime
  log 和 soc-ap 定向差异的 SHA256 均与索引一致；source_report 为空。
unexecuted:
- 必需的 test_fastcdr_optional 与 test_dds_pubsub CTest 未执行完成：冻结命令在 build.sh fastcdr 后的安装校验处失败并提前退出。
actual_session: 01a1a9a0-7d66-7293-82d2-78299bce71b7
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd;
  soc-ap=68b926e4376185a4979869a4787b90c8623a9164; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-52
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: a58547ec2caf
    id: TWIN-52_run_105321_20261105_025321
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321
    developer_mounts: []
    container_inspect:
      id: a58547ec2caff3849a625ec63e1f10b90a9f644a341b09874c5952d29847ee4a
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-05T02:53:44.966969847Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-52_ji8dy6lb/evidence/server_lock.json
    sha256: ad62f7d5dd2c6e8d98d81511ce8558dbf1595d4d6a45598360ad4ed996f3a0dd
  checkout_log:
    path: /tmp/qa_TWIN-52_ji8dy6lb/evidence/checkout.log
    sha256: 894b455615df2a82b1c2dd894e597f99377036ea910aa14f2bb86f76f22dbe87
  runtime_log:
    path: /tmp/qa_TWIN-52_ji8dy6lb/evidence/runtime.log
    sha256: 43380bcbfd433692eccfed0d4e33325c0accc7306b6c245941aff52bf94aa3f1
  server_verdict:
    path: /tmp/qa_TWIN-52_ji8dy6lb/evidence/server_verdict.json
    sha256: 532c33d93a93feb58e221e68a319aedac766ee2317c36222776d2aeec0905633
  tool_versions:
    git: git version 2.25.1
    python: Python 3.8.10
  build_results: []
  test_results:
  - command: rm -rf /tmp/qa_twin52 && mkdir -p /tmp/qa_twin52/raw && tar -xzf third_party/archives/Fast-CDR-2.2.5.tar.gz
      -C /tmp/qa_twin52/raw && test "$(grep -c "if (val.storage_.engaged_)" /tmp/qa_twin52/raw/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp
      || true)" -eq 0 && cp -r ../soc-ap /tmp/qa_twin52/soc-ap && ([ -e /tmp/qa_twin52/soc-ap/third_party/install
      ] || (mkdir -p /tmp/qa_twin52/soc-ap/third_party && cp -a /usr/local /tmp/qa_twin52/soc-ap/third_party/install))
      && cp /tmp/qa_twin52/raw/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp
      && rm -rf /tmp/qa_twin52/soc-ap/third_party/src/Fast-CDR-2.2.5 && (! bash /tmp/qa_twin52/soc-ap/third_party/build.sh
      --verify) && mkdir -p /tmp/qa_twin52/soc-ap/third_party/src/foonathan_memory-0.7-3
      /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/asio/asio/include
      /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/tinyxml2 /tmp/qa_twin52/soc-ap/third_party/src/dbus-1.16.2
      && touch /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/asio/asio/include/asio.hpp
      /tmp/qa_twin52/soc-ap/third_party/src/Fast-DDS-3.6.2/thirdparty/tinyxml2/tinyxml2.cpp
      && bash /tmp/qa_twin52/soc-ap/third_party/build.sh fastcdr && bash /tmp/qa_twin52/soc-ap/third_party/build.sh
      --verify && bash /tmp/qa_twin52/soc-ap/third_party/build.sh && test "$(grep
      -c "if (val.storage_.engaged_)" /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp)"
      -eq 2 && cmake -S /tmp/qa_twin52/soc-ap/middleware/dds/tests -B /tmp/qa_twin52/build_opt_test
      && cmake --build /tmp/qa_twin52/build_opt_test --parallel && LD_LIBRARY_PATH="/tmp/qa_twin52/soc-ap/third_party/install/lib:${LD_LIBRARY_PATH:-}"
      ctest --test-dir /tmp/qa_twin52/build_opt_test --output-on-failure && cmake
      -S /tmp/qa_twin52/soc-ap/tests/dds/twin -B /tmp/qa_twin52/build_dds_twin &&
      cmake --build /tmp/qa_twin52/build_dds_twin --parallel && LD_LIBRARY_PATH="/tmp/qa_twin52/soc-ap/third_party/install/lib:${LD_LIBRARY_PATH:-}"
      ctest --test-dir /tmp/qa_twin52/build_dds_twin --output-on-failure && rm -rf
      /tmp/qa_twin52
    exit_code: '1'
    subpath: soc-ap
    duration: 1.56s
    output: "==================================================\nBuild & Installation\
      \ Verification:\n==================================================\n  [OK]\
      \ D-Bus library: /tmp/qa_twin52/soc-ap/third_party/install/lib/libdbus-1.so\n\
      \  [OK] D-Bus daemon:  /tmp/qa_twin52/soc-ap/third_party/install/bin/dbus-daemon\n\
      \  [OK] Fast CDR:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so\n\
      \  [OK] Fast DDS:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastdds.so\n\
      --> Unpacking Fast-CDR-2.2.5...\n--> Applying Fast-CDR optional.hpp engaged\
      \ guard patch...\npatching file include/fastcdr/xcdr/optional.hpp\n  [OK] Fast-CDR\
      \ optional.hpp patched and verified (2 engaged guards).\n==================================================\n\
      Building Fast-CDR (2.2.5)...\n==================================================\n\
      -- Setting build type to 'Release' as none was specified.\n-- Tests not compiled\
      \ by default\n-- The CXX compiler identification is GNU 9.4.0\n-- Detecting\
      \ CXX compiler ABI info\n-- Detecting CXX compiler ABI info - done\n-- Check\
      \ for working CXX compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile\
      \ features\n-- Detecting CXX compile features - done\n-- Configuring Fast CDR\n\
      -- Version: 2.2.5\n-- Performing Test SUPPORTS_NOTFOUND\n-- Performing Test\
      \ SUPPORTS_NOTFOUND - Success\n-- Enforced cxx_std_11 CMake feature\n-- Looking\
      \ for C++ include sys/types.h\n-- Looking for C++ include sys/types.h - found\n\
      -- Looking for C++ include stdint.h\n-- Looking for C++ include stdint.h - found\n\
      -- Looking for C++ include stddef.h\n-- Looking for C++ include stddef.h - found\n\
      -- Check size of long double\n-- Check size of long double - done\n-- Check\
      \ size of __float128\n-- Check size of __float128 - done\n-- The C compiler\
      \ identification is GNU 9.4.0\n-- Detecting C compiler ABI info\n-- Detecting\
      \ C compiler ABI info - done\n-- Check for working C compiler: /usr/bin/cc -\
      \ skipped\n-- Detecting C compile features\n-- Detecting C compile features\
      \ - done\n-- Configuring done (0.4s)\n-- Generating done (0.0s)\n-- Build files\
      \ have been written to: /tmp/qa_twin52/soc-ap/third_party/build/Fast-CDR\n[\
      \ 10%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/CdrSizeCalculator.cpp.o\n\
      [ 20%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/FastCdr.cpp.o\n[ 40%]\
      \ Building CXX object src/cpp/CMakeFiles/fastcdr.dir/FastBuffer.cpp.o\n[ 40%]\
      \ Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/BadParamException.cpp.o\n\
      [ 50%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/BadOptionalAccessException.cpp.o\n\
      [ 60%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/Exception.cpp.o\n\
      [ 70%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/Cdr.cpp.o\n[ 80%]\
      \ Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/LockedExternalAccessException.cpp.o\n\
      [ 90%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/NotEnoughMemoryException.cpp.o\n\
      [100%] Linking CXX shared library libfastcdr.so\n[100%] Built target fastcdr\n\
      -- Install configuration: \"Release\"\n-- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/FastBuffer.h\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/cdr\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/cdr/fixed_size_string.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/config\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/config/doxygen_modules.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/Cdr.h\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions/BadParamException.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions/Exception.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions/BadOptionalAccessException.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions/LockedExternalAccessException.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/exceptions/NotEnoughMemoryException.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/fastcdr_dll.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/FastCdr.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/eProsima_auto_link.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/CdrEncoding.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/CdrSizeCalculator.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/external.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/MemberId.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/detail\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/detail/optional.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/detail\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/detail/container_recursive_inspector.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/config.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so.2.2.5\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so.2\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/cmake/fastcdr/fastcdr-shared-targets.cmake\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/cmake/fastcdr/fastcdr-shared-targets-release.cmake\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/cmake/fastcdr/fastcdr-config.cmake\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/cmake/fastcdr/fastcdr-config-version.cmake\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/share/fastcdr/LICENSE\n\
      ==================================================\nBuild & Installation Verification:\n\
      ==================================================\n  [OK] D-Bus library: /tmp/qa_twin52/soc-ap/third_party/install/lib/libdbus-1.so\n\
      \  [OK] D-Bus daemon:  /tmp/qa_twin52/soc-ap/third_party/install/bin/dbus-daemon\n\
      \  [OK] Fast CDR:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so\n\
      \  [OK] Fast DDS:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastdds.so\n\
      \n  [FAIL] Fast CDR optional.hpp missing engaged guard in /tmp/qa_twin52/soc-ap/third_party/install!\n\
      \  [FAIL] Fast CDR optional.hpp missing engaged guard in /tmp/qa_twin52/soc-ap/third_party/install!"
  passed: false
  timestamp: '2026-11-05T02:53:49.303866+00:00'
  path: /tmp/qa_TWIN-52_ji8dy6lb/evidence/server_qa.json
  sha256: c60560429d1e5549c3d1df0e8d28b705a25fb5b383cd5f0d836f0d8378ab11d6
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-52_ji8dy6lb/reviews/7e99c549e8e14602a001d8cd822d8ad6/codex.jsonl
  sha256: dce18b189a4dc1ca02da23536ecd54cc586a8fdbf479cae5699943720a793341
reviewed_artifacts:
- path: /tmp/qa_TWIN-52_ji8dy6lb/request.json
  sha256: 37c9c5efa6f178566fbd104495a454a561898f79510308468489f8017ebe1761
- path: /tmp/qa_TWIN-52_ji8dy6lb/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-52_ji8dy6lb/diffs/soc-ap.patch
  sha256: 2247b6f8d631e04ef4ffb3aae4234e9dedebae6a5d71576ea3a6d78efab6d26b
- path: /tmp/qa_TWIN-52_ji8dy6lb/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-52_ji8dy6lb/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321/soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch
  sha256: d6f9957923de6f5fd403fff7f99a6308823c5e12f6a698698e54c1b83e901cc6
- path: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321/soc-ap/third_party/build.sh
  sha256: 7da8a8870f9defc26bbf24e11fd49a6e95ae5b2c9f84bc70a123ca899165411b
- path: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321/soc-ap/middleware/dds/tests/CMakeLists.txt
  sha256: 50a29cdd95840be9742e08da4fa386935a22ee40b3c306cb01e6906cc6b4a0c4
- path: /tmp/qa_sandboxes/TWIN-52_run_105321_20261105_025321/soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp
  sha256: a3f686178762eb1779c1623bde20c667d00465c98cdbac135c796ceb78d1e160
verification_scope: 审阅 Fast-CDR 补丁与 third_party/build.sh 的补丁应用、安装校验和负向恢复，以及 optional
  回归和 DDS CTest。跨编译器 ELF 构建及实体 MCU USB/UART HIL 属于排除项，不作为未执行项目。bundle、request、server
  verdict、runtime log 和 soc-ap 定向差异的 SHA256 均与索引一致；source_report 为空。
verification_environment: docker-sandbox-and-independent-codex-audit
```

候选未满足负向恢复验收：触发安装头文件守卫缺失后，build.sh fastcdr 未能修复安装结果，后续 verify 仍失败。
