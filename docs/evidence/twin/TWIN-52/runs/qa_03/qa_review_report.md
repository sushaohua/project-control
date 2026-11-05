```yaml
task_id: TWIN-52
task_revision: 1
candidate_commit: ad2538ae7f4834cac98be97e08b055f80eb81cfc
role: QA
decision: APPROVED
summary: 锁定候选符合已接受的软件范围。已核对 bundle、request、verdict、runtime log、定向 diff 及四个候选产物的 SHA256；冻结证据记录负向校验拒绝、补丁应用与安装、正向校验及两套
  CTest 全部通过。
findings:
- runtime.log 记录未打补丁的安装头文件被 --verify 拒绝，并显示 [FAIL] missing engaged guard；随后记录补丁应用、两处守卫校验通过、test_fastcdr_optional
  与 test_dds_pubsub 均通过。
- 定向差异只涉及接受范围内的四个路径，候选产物哈希与索引声明一致。源码中的构建、安装和 verify 路径与验收条款相符。
- 非阻断建议：当前 verify_install 通过匹配守卫文本数量确认补丁状态；未来可考虑校验更具体的构造函数上下文。
- 审阅说明与最终 JSON 未另存为文件：当前工作区权限为只读。
accepted_scope: 审阅 TWIN-52 revision 1 的软件及 C++17 沙箱范围：Fast-CDR 2.2.5 optional engaged-guard
  补丁、build.sh 的应用/校验行为、未激活与已激活 optional 拷贝/移动覆盖、Fast-DDS participant/publisher/subscriber
  与 pub/sub 回归证据。接受范围明确排除交叉编译 ELF 构建及实体 MCU USB/UART HIL；本审阅不声称这些硬件验证已通过。
unexecuted: []
actual_session: 01a1a9ad-5a37-7bb3-9835-4ed9ce0a308b
reviewer_role: QA
reviewer_roles:
- QA
reviewed_artifact_version: project-control=491158cd4f183a01517c36fb093821db54a8a6dd;
  soc-ap=ad2538ae7f4834cac98be97e08b055f80eb81cfc; mcu-p3=016e1236af75f6f19282d6b000f4b1b68bd96cc3;
  test_harness=d14ed04321c6d4f5ddb35a8801604a8af53b5b60
server_qa:
  task_id: TWIN-52
  task_revision: 1
  source: server-pinned-commits
  fresh_checkout: true
  sandbox:
    kind: container
    container_id: 2c2e24e6bacd
    id: TWIN-52_run_110719_20261105_030719
    image: qa-sandbox:20261029
    path: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719
    developer_mounts: []
    container_inspect:
      id: 2c2e24e6bacd5c5203cb6107cb6c5354a76499d122cc7d0610d9e953c8b3ec9e
      image: qa-sandbox:20261029
      image_digest: sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f
      created: '2026-11-05T03:07:42.954292179Z'
      state: exited
      mounts:
      - Type: bind
        Source: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719
        Destination: /workspace
        Mode: ro
        RW: false
        Propagation: rprivate
  server_lock:
    path: /tmp/qa_TWIN-52_d29xbpdj/evidence/server_lock.json
    sha256: bb85e32d9e9a72257dacbc583de8218b01b7929b43769d2e8440962c484a70ee
  checkout_log:
    path: /tmp/qa_TWIN-52_d29xbpdj/evidence/checkout.log
    sha256: 1e64e27cab14bda798755925429528d896ee8b509080e2a2860f25cc9d0dbddb
  runtime_log:
    path: /tmp/qa_TWIN-52_d29xbpdj/evidence/runtime.log
    sha256: e5f6df543397965a996f11fcbd5207a772d07dec2750a5813118c0f4b712dffb
  server_verdict:
    path: /tmp/qa_TWIN-52_d29xbpdj/evidence/server_verdict.json
    sha256: 26b2687e33822f1f73982b04ed2b31f7e792e62145a89e3f0a801fbd4e3c2658
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
    exit_code: '0'
    subpath: soc-ap
    duration: 6.62s
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
      \ 20%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/Cdr.cpp.o\n[ 20%]\
      \ Building CXX object src/cpp/CMakeFiles/fastcdr.dir/CdrSizeCalculator.cpp.o\n\
      [ 30%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/FastBuffer.cpp.o\n\
      [ 40%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/FastCdr.cpp.o\n[ 50%]\
      \ Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/BadOptionalAccessException.cpp.o\n\
      [ 60%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/NotEnoughMemoryException.cpp.o\n\
      [ 80%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/BadParamException.cpp.o\n\
      [ 80%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/LockedExternalAccessException.cpp.o\n\
      [ 90%] Building CXX object src/cpp/CMakeFiles/fastcdr.dir/exceptions/Exception.cpp.o\n\
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
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/MemberId.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/detail\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/detail/optional.hpp\n\
      -- Up-to-date: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/detail\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/detail/container_recursive_inspector.hpp\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/config.h\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so.2.2.5\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so.2\n\
      -- Installing: /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so\n\
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
      \  [OK] Fast CDR optional.hpp engaged guard verified: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp\n\
      All requested third_party components verified in /tmp/qa_twin52/soc-ap/third_party/install.\n\
      \  [OK] Fast-CDR optional.hpp patch already applied: /tmp/qa_twin52/soc-ap/third_party/src/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp\n\
      ==================================================\nBuild & Installation Verification:\n\
      ==================================================\n  [OK] D-Bus library: /tmp/qa_twin52/soc-ap/third_party/install/lib/libdbus-1.so\n\
      \  [OK] D-Bus daemon:  /tmp/qa_twin52/soc-ap/third_party/install/bin/dbus-daemon\n\
      \  [OK] Fast CDR:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastcdr.so\n\
      \  [OK] Fast DDS:      /tmp/qa_twin52/soc-ap/third_party/install/lib/libfastdds.so\n\
      \  [OK] Fast CDR optional.hpp engaged guard verified: /tmp/qa_twin52/soc-ap/third_party/install/include/fastcdr/xcdr/optional.hpp\n\
      All requested third_party components verified in /tmp/qa_twin52/soc-ap/third_party/install.\n\
      -- The C compiler identification is GNU 9.4.0\n-- The CXX compiler identification\
      \ is GNU 9.4.0\n-- Detecting C compiler ABI info\n-- Detecting C compiler ABI\
      \ info - done\n-- Check for working C compiler: /usr/bin/cc - skipped\n-- Detecting\
      \ C compile features\n-- Detecting C compile features - done\n-- Detecting CXX\
      \ compiler ABI info\n-- Detecting CXX compiler ABI info - done\n-- Check for\
      \ working CXX compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n\
      -- Detecting CXX compile features - done\n-- Configuring done (0.1s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin52/build_opt_test\n\
      [ 12%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/test_fastcdr_optional.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 37%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [ 87%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 87%] Building CXX object CMakeFiles/test_fastcdr_optional.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [100%] Linking CXX executable test_fastcdr_optional\n[100%] Built target test_fastcdr_optional\n\
      Test project /tmp/qa_twin52/build_opt_test\n    Start 1: test_fastcdr_optional\n\
      1/1 Test #1: test_fastcdr_optional ............   Passed    0.11 sec\n\n100%\
      \ tests passed out of 1\n\nTotal Test time (real) =   0.11 sec\n-- The C compiler\
      \ identification is GNU 9.4.0\n-- The CXX compiler identification is GNU 9.4.0\n\
      -- Detecting C compiler ABI info\n-- Detecting C compiler ABI info - done\n\
      -- Check for working C compiler: /usr/bin/cc - skipped\n-- Detecting C compile\
      \ features\n-- Detecting C compile features - done\n-- Detecting CXX compiler\
      \ ABI info\n-- Detecting CXX compiler ABI info - done\n-- Check for working\
      \ CXX compiler: /usr/bin/c++ - skipped\n-- Detecting CXX compile features\n\
      -- Detecting CXX compile features - done\n-- Configuring done (0.2s)\n-- Generating\
      \ done (0.0s)\n-- Build files have been written to: /tmp/qa_twin52/build_dds_twin\n\
      [ 25%] Building CXX object CMakeFiles/test_dds_pubsub.dir/test_dds_pubsub.cpp.o\n\
      [ 25%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_types.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_common.cpp.o\n\
      [ 50%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_participant.cpp.o\n\
      [ 62%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_sub.cpp.o\n\
      [ 75%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds.cpp.o\n\
      [ 87%] Building CXX object CMakeFiles/test_dds_pubsub.dir/tmp/qa_twin52/soc-ap/middleware/dds/src/aisoc_dds_pub.cpp.o\n\
      [100%] Linking CXX executable test_dds_pubsub\n[100%] Built target test_dds_pubsub\n\
      Test project /tmp/qa_twin52/build_dds_twin\n    Start 1: test_dds_pubsub\n1/1\
      \ Test #1: test_dds_pubsub ..................   Passed    1.29 sec\n\n100% tests\
      \ passed out of 1\n\nTotal Test time (real) =   1.29 sec\n\n  [FAIL] Fast CDR\
      \ optional.hpp missing engaged guard in /tmp/qa_twin52/soc-ap/third_party/install!"
  passed: true
  timestamp: '2026-11-05T03:07:52.235772+00:00'
  path: /tmp/qa_TWIN-52_d29xbpdj/evidence/server_qa.json
  sha256: 46e2bb978f29de635366cddc903cc7c9469fdb4c8f9af5793380c92ab0a8d857
platform: codex
model: gpt-6-luna
session_evidence:
  path: /tmp/qa_TWIN-52_d29xbpdj/reviews/63f60c03ee7349abbdb65264c00411c8/codex.jsonl
  sha256: 77241ff8bf7e688ed54cfe3055f6fb34a530544b0d16eca6bae7f8b8bc0cbee6
reviewed_artifacts:
- path: /tmp/qa_TWIN-52_d29xbpdj/request.json
  sha256: d8f5e610a9509ac3a752cfadc00663cf1377fc2f1310abe87dd2060e7e01437e
- path: /tmp/qa_TWIN-52_d29xbpdj/diffs/project-control.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-52_d29xbpdj/diffs/soc-ap.patch
  sha256: 62b8e7e0278c98114d0cfb0784d3de1557a7245c1c1f625512ee041bacca75c7
- path: /tmp/qa_TWIN-52_d29xbpdj/diffs/mcu-p3.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_TWIN-52_d29xbpdj/diffs/test_harness.patch
  sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- path: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719/soc-ap/third_party/patches/Fast-CDR-2.2.5-optional-engaged-guard.patch
  sha256: d6f9957923de6f5fd403fff7f99a6308823c5e12f6a698698e54c1b83e901cc6
- path: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719/soc-ap/third_party/build.sh
  sha256: dda80b418bbd99fab4c6d6b7eac91310096b291c3de4710d6a5db71021c18844
- path: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719/soc-ap/middleware/dds/tests/CMakeLists.txt
  sha256: 50a29cdd95840be9742e08da4fa386935a22ee40b3c306cb01e6906cc6b4a0c4
- path: /tmp/qa_sandboxes/TWIN-52_run_110719_20261105_030719/soc-ap/middleware/dds/tests/test_fastcdr_optional.cpp
  sha256: a3f686178762eb1779c1623bde20c667d00465c98cdbac135c796ceb78d1e160
verification_scope: 审阅 TWIN-52 revision 1 的软件及 C++17 沙箱范围：Fast-CDR 2.2.5 optional
  engaged-guard 补丁、build.sh 的应用/校验行为、未激活与已激活 optional 拷贝/移动覆盖、Fast-DDS participant/publisher/subscriber
  与 pub/sub 回归证据。接受范围明确排除交叉编译 ELF 构建及实体 MCU USB/UART HIL；本审阅不声称这些硬件验证已通过。
verification_environment: docker-sandbox-and-independent-codex-audit
```

锁定候选符合已接受的软件范围。已核对 bundle、request、verdict、runtime log、定向 diff 及四个候选产物的 SHA256；冻结证据记录负向校验拒绝、补丁应用与安装、正向校验及两套 CTest 全部通过。
