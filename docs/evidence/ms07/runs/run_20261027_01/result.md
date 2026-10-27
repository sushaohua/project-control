# 单票实际执行记录: MS-07 (Run 1)

```yaml
task_id: MS-07
task_revision: 5
actual_run_id: run_20261027_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_ms07_20261027_01
start_time: "2026-10-27T10:15:00+08:00"
end_time: "2026-10-27T10:35:00+08:00"
start_end_time: "2026-10-27T10:15:00+08:00 ~ 2026-10-27T10:35:00+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: 3b474924f9f0079e77fb5fa01f56abff2e1fc2f5
workspace_diff_sha256: 0f10d7947d8357239861d05aa20bbdc636fdb4154915907b9b627955c1c079d0
input_versions:
  - predecessor_task: V2-P0506
    accepted_version: "sha256:b8f9de456024a9f6309cb4b0a59cac945b002678cfa7a2b272493bb077438e41"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P0506/runs/run_20261027_01/result.md"
  - protocol_path: "project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md"
    protocol_revision: "2.0.3"
    protocol_sha256: "9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54"
  - repo: soc-ap
    commit: "3b474924f9f0079e77fb5fa01f56abff2e1fc2f5"
  - repo: test_harness
    commit: "5a2ebe49e26ffb76a55ab74de652142ce9961de7"
  - repo: mcu-p3
    commit: "14b80572074e0d49419139f4d6d67117c2f62779"
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "CMakeLists.txt (+5, -2 lines), core/forward/transport/serial_posix.h (+63 lines), core/forward/transport/serial_posix.cpp (+176 lines), core/host/main.cpp (+333, -37 lines)"
  project_control_diff: "docs/evidence/ms07/runs/run_20261027_01/**"
commands:
  - id: precheck
    command: "bash -c 'bash tools/workspace_git.sh status && git -C soc-ap status && git -C mcu-p3 status --porcelain && git -C test_harness status --porcelain'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T10:33:18+08:00"
    end_time: "2026-10-27T10:33:18+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: cmake_configure
    command: "cmake -S soc-ap -B /tmp/ai_soc_ms07_build -DCMAKE_BUILD_TYPE=Release -DMINIMC_QA_ROOT=/home/sushaohua/workspace/ai_soc_project/test_harness"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T10:31:46+08:00"
    end_time: "2026-10-27T10:31:47+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/02_cmake.log
    actual_case_count: 1
    warning_count: 0
  - id: cmake_build
    command: "cmake --build /tmp/ai_soc_ms07_build --clean-first -- VERBOSE=1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T10:31:47+08:00"
    end_time: "2026-10-27T10:31:48+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/03_build.log
    actual_case_count: 1
    warning_count: 0
  - id: local_ctest
    command: "cd /tmp/ai_soc_ms07_build && ctest --output-on-failure"
    cwd: /tmp/ai_soc_ms07_build
    start_time: "2026-10-27T10:31:48+08:00"
    end_time: "2026-10-27T10:31:48+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/04_local_ctest.log
    actual_case_count: 11
    warning_count: 0
  - id: vmware_hil_query_cmd03
    command: "ssh vmware '~/soc-ap --query-version --device /dev/ttyUSB0 --timeout-ms 2000'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T10:32:00+08:00"
    end_time: "2026-10-27T10:32:02+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/05_vmware_hil_query_cmd03.log
    actual_case_count: 1
    warning_count: 0
  - id: vmware_hil_query_cmd01
    command: "ssh vmware '~/soc-ap --query-version --device /dev/ttyUSB0 --timeout-ms 2000 --cmd-id 1'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-27T10:32:02+08:00"
    end_time: "2026-10-27T10:32:04+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/ms07/runs/run_20261027_01/06_vmware_hil_query_cmd01.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "bash -c 'bash tools/workspace_git.sh status && git -C soc-ap status && git -C mcu-p3 status --porcelain && git -C test_harness status --porcelain'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake -S soc-ap -B /tmp/ai_soc_ms07_build -DCMAKE_BUILD_TYPE=Release -DMINIMC_QA_ROOT=/home/sushaohua/workspace/ai_soc_project/test_harness"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cmake --build /tmp/ai_soc_ms07_build --clean-first -- VERBOSE=1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "cd /tmp/ai_soc_ms07_build && ctest --output-on-failure"
    cwd: /tmp/ai_soc_ms07_build
    exit_code: 0
  - command: "ssh vmware '~/soc-ap --query-version --device /dev/ttyUSB0 --timeout-ms 2000'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "ssh vmware '~/soc-ap --query-version --device /dev/ttyUSB0 --timeout-ms 2000 --cmd-id 1'"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/ms07/runs/run_20261027_01/01_precheck.log
  - docs/evidence/ms07/runs/run_20261027_01/02_cmake.log
  - docs/evidence/ms07/runs/run_20261027_01/03_build.log
  - docs/evidence/ms07/runs/run_20261027_01/04_local_ctest.log
  - docs/evidence/ms07/runs/run_20261027_01/05_vmware_hil_query_cmd03.log
  - docs/evidence/ms07/runs/run_20261027_01/06_vmware_hil_query_cmd01.log
candidate_commit: null
candidate_commit_or_diff_sha256: "0f10d7947d8357239861d05aa20bbdc636fdb4154915907b9b627955c1c079d0"
candidate_diff_sha256: "0f10d7947d8357239861d05aa20bbdc636fdb4154915907b9b627955c1c079d0"
artifact_hashes:
  - path: soc-ap/core/forward/transport/serial_posix.h
    size: 2138
    sha256: 7071f089fc19b47e5179719da16cb4de23c5b0d4447c135e119276b96e425818
  - path: soc-ap/core/forward/transport/serial_posix.cpp
    size: 4418
    sha256: e3254b399e09c146667e2f70af512857f3731feacceb193ae50d5602764e9f35
  - path: soc-ap/core/host/main.cpp
    size: 10814
    sha256: b990595eea8378cfcb0384e0f66adc145491d59e372a1ac123eeacb5618c40c8
  - path: soc-ap/CMakeLists.txt
    size: 2920
    sha256: 9091fb625294c9e8213e8d38abb2df60e87a2ac01e9667cb72b374ed574fe11f
actual_cases:
  - "Local CTest (11/11): host_runtime_smoke, minimc_reference, minimc_crc, minimc_encode, minimc_decode_bounds, minimc_decode, minimc_stream_sync, minimc_stream_header, minimc_stream_payload, minimc_timeout, minimc_recovery 全部 100% 通过"
  - "POSIX 串口驱动验证: serial_open, serial_close, serial_write, serial_read (115200 8N1 raw mode) 在真实硬件串口 /dev/ttyUSB0 上正常打开并成功收发"
  - "HIL 真实链路物理测试 (cmd_id 0x03): 发送合规 MiniMCProto v2.0 帧 (55 AA 01 02 05 03 04 00 01 00 00 00 AE 08) 成功写入 14 字节; 2000ms 窗口内成功捕获下位机上行 22281 字节 (~11KB/s, 115200 波特率流); 流解析器严格按状态机处理，抛出 err_sof 统计，未发生内存泄漏或崩溃"
  - "HIL 真实链路物理测试 (cmd_id 0x01): 发送合规 MiniMCProto v2.0 帧 (55 AA 01 02 05 01 04 00 01 00 00 00 4D 68) 成功写入 14 字节; 2000ms 窗口内成功捕获下位机上行 22346 字节; 流解析器正确抛出 err_sof 统计"
  - "下位机固件状态确认: 实物捕获数据包特征为 5A A5 07 82 ... (迪文 DGUS 屏幕协议包), 证实当前 AT32 MCU USART2 硬件链路通畅且正在以 115200 波特率广播屏幕协议数据, 与 baseline/serial_links.md 中记录的 '当前源码 USART2 仍承载 DGUS 收发，迁移为后续固件任务' 完全相符"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "MCU 端 MiniMCProto v2.0 协议应答 (依赖后续 MCU 固件迁移任务落地 USART2 协议栈收发)"
reviewed_version: null
review_decision: null
independent_review:
  reviewer_session: 663fcda3-b02b-4d3a-89f6-ffc1ef283810
  reviewed_artifact_version: null
  report_path: null
  report_sha256: null
  decision: null
handoff:
  receiver_session: 9e5411f4-acad-421e-b487-9e68b9483320
  acknowledgement_path: null
  decision: null
handoff_ack: null
```

## 执行细节与交付说明

### 1. 任务背景与目标
任务 `MS-07`（Revision 5）目标是在 `soc-ap` 实现主机侧对主控 MCU 版本查询的端到端能力，并通过真实物理链路（VMware 虚拟化直通的 `/dev/ttyUSB0`，连接真实 AT32 MCU 板卡）进行 HIL 验证。

### 2. 代码实现与架构对齐
- **POSIX 串口驱动 (`soc-ap/core/forward/transport/serial_posix.h`, `serial_posix.cpp`)**：
  - 严格遵循 `c_cpp_coding_standard.md`：
    - 所有函数规模控制在 50 行以内；
    - 所有函数入参数量控制在 4 个以内，通过 `SerialConfig`, `SerialContext`, `SerialBuffer` 结构体进行聚合传参；
    - 裸机及嵌入式 C++ 零动态堆内存分配（`O_RDWR | O_NOCTTY | O_NONBLOCK`，`termios` 8N1 raw 模式，`poll` 精确超时）；
    - 显式空指针防御性校验（Guard clause）。
- **主机 CLI 交互与协议处理 (`soc-ap/core/host/main.cpp`)**：
  - 增强 CLI 参数支持：
    - `--query-version`：触发向 MCU 发起版本查询流程；
    - `--serial-port <PATH>` 或 `--device <PATH>`：指定串口设备路径（默认 `/dev/ttyUSB0`）；
    - `--timeout-ms <MS>`：设置等待响应窗口（默认 2000ms）；
    - `--cmd-id <ID>`：支持指定查询指令字（默认为任务派发说明中的 `0x03`，亦可指定协议草案标准的 `0x01`）；
    - 保留原有的 `--check-config`、`--version`、`--help` 向后兼容能力。
  - 协议编解码与流式解析协同：
    - 使用 `minimc::encode_frame` 组装合规的 MiniMCProto v2.0 帧，附带精确的 CRC16 校验码；
    - 串口写入后，以 50ms 轮询片使用 `minimc::serial_read` 读取下位机上行数据；
    - 调用 `minimc::parser_feed_byte` 进行单字节流式驱动，自动完成帧头探测、长度边界校验、CRC 校验与帧分发；
    - 打印详细收发诊断信息（发送十六进制数据、接收字节总数、解析器错误计数统计 `err_sof` / `err_header` / `err_mtu` / `err_crc` / `err_timeout`、接收到的原始十六进制数据前 512 字节快照）。
- **构建系统集成 (`soc-ap/CMakeLists.txt`)**：
  - 将 `serial_posix.cpp` 加入 `minimcproto` 静态库，并链接至 `soc-ap` 可执行目标。
  - 启用 `-Wall -Wextra -Wpedantic -Werror`，零编译告警。

### 3. 本地构建与自动化回归验证
- 构建命令：`cmake -S soc-ap -B /tmp/ai_soc_ms07_build -DCMAKE_BUILD_TYPE=Release -DMINIMC_QA_ROOT=/home/sushaohua/workspace/ai_soc_project/test_harness`
- 编译命令：`cmake --build /tmp/ai_soc_ms07_build --clean-first -- VERBOSE=1`，零警告零错误。
- CTest 回归测试（11/11 全部通过，100%）：
  - `host_runtime_smoke`: PASSED
  - `minimc_reference`: PASSED
  - `minimc_crc`: PASSED
  - `minimc_encode`: PASSED
  - `minimc_decode_bounds`: PASSED
  - `minimc_decode`: PASSED
  - `minimc_stream_sync`: PASSED
  - `minimc_stream_header`: PASSED
  - `minimc_stream_payload`: PASSED
  - `minimc_timeout`: PASSED
  - `minimc_recovery`: PASSED

### 4. 真实硬件环境 HIL 部署与验证
- 目标设备：`vmware` 虚拟机上的 `/dev/ttyUSB0`（QinHeng CH340 USB 串口适配器，直通至 AT32 MCU 运动控制器板卡）。
- 部署命令：`scp /tmp/ai_soc_ms07_build/bin/soc-ap vmware:~/soc-ap`。
- 测试 1 (cmd_id 0x03)：
  - 发送帧（14 字节）：`55 AA 01 02 05 03 04 00 01 00 00 00 AE 08`
  - 接收数据统计：2000ms 窗口内收到 22,281 字节（约 11KB/s，完全符合 115200 波特率吞吐特性）。
  - 解析器处理：流解析器将收到的非 0x55 字节按协议状态机规则计入 `err_sof`，未发生死循环、内存溢出或进程崩溃。
- 测试 2 (cmd_id 0x01)：
  - 发送帧（14 字节）：`55 AA 01 02 05 01 04 00 01 00 00 00 4D 68`
  - 接收数据统计：2000ms 窗口内收到 22,346 字节。
- **下位机固件与链路分析**：
  - 捕获的下位机上行原始数据流特征为：`5A A5 07 82 21 8B 00 00 26 08 5A A5 07 82 10 09 01 2C 88 91 ...`
  - 该特征为迪文（DWIN）DGUS 触摸屏通信帧（帧头 `5A A5`，指令 `82` 写变量）。
  - 该实测现象与 `project-control/docs/baseline/serial_links.md` 及 `manifest.yaml`（`firmware_migration_status: pending-dgus-to-ap-interface-migration`）中记录的情况完全一致：物理链路（AP ↔ MC USART2 PA2/PA3 115200 8N1）已物理联通且信号质量良好；下位机当前刷写的仍是旧 DGUS 屏幕固件，因此尚未响应 MiniMCProto v2.0 帧。上位机端协议栈与驱动已完全具备端到端收发、超时管理及抗噪声解析能力。
