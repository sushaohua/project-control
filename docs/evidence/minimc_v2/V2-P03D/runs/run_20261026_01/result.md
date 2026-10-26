# 单票实际执行记录: V2-P03D (Run 1)

```yaml
task_id: V2-P03D
task_revision: 1
actual_run_id: run_20261026_01
actor_session: 1c634be7-4be2-4743-af02-dc8ada31bad3
lease_id: lease_v2_p03d_20261026_01
start_time: "2026-10-26T19:45:27+08:00"
end_time: "2026-10-26T19:49:15+08:00"
workspace: /home/sushaohua/workspace/ai_soc_project
source_head: f508954594b91f2a9daca58dd6087cba3b0b7506
workspace_diff_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
input_versions:
  - predecessor_task: V2-P03C
    accepted_version: "sha256:1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P03C/runs/run_20261026_01/qa_review_report.md"
  - predecessor_task: V2-P02C
    accepted_version: "sha256:0c05ad8ed92a48b0062772042ec8fa1e1ab79d71dfaf2746afa3efb08cd3b7b3"
    acceptance_evidence: "docs/evidence/minimc_v2/V2-P02C/runs/run_20261026_01/qa_review_report.md"
  - protocol_path: project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md
    protocol_revision: 2.0.3
    protocol_sha256: 9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54
  - repo: soc-ap
    commit: f508954594b91f2a9daca58dd6087cba3b0b7506
  - repo: test_harness
    commit: 59d2320663dd7ef4a080272d624f831684935c34
worktree_and_diff:
  worktree: /home/sushaohua/workspace/ai_soc_project
  soc_ap_diff: "soc-ap/tests/protocol/probe.cpp (new file, 19372 bytes)"
  project_control_diff: "docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/** (evidence logs and result.md)"
commands:
  - id: precheck
    command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T19:45:56+08:00"
    end_time: "2026-10-26T19:45:56+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/01_precheck.log
    actual_case_count: 1
    warning_count: 0
  - id: probe_compile
    command: "mkdir -p /tmp/ai_soc_v2_build/V2-P03D && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc soc-ap/tests/protocol/probe.cpp soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/parser.cpp -o /tmp/ai_soc_v2_build/V2-P03D/minimc-probe"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T19:47:53+08:00"
    end_time: "2026-10-26T19:47:53+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/02_probe_compile.log
    actual_case_count: 1
    warning_count: 0
  - id: cli
    command: "/tmp/ai_soc_v2_build/V2-P03D/minimc-probe --self-check"
    cwd: /home/sushaohua/workspace/ai_soc_project
    start_time: "2026-10-26T19:48:16+08:00"
    end_time: "2026-10-26T19:48:16+08:00"
    actual_exit_code: 0
    stdout_stderr_path: docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/03_cli.log
    actual_case_count: 1
    warning_count: 0
commands_cwd_exit_codes:
  - command: "git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "mkdir -p /tmp/ai_soc_v2_build/V2-P03D && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc soc-ap/tests/protocol/probe.cpp soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/parser.cpp -o /tmp/ai_soc_v2_build/V2-P03D/minimc-probe"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
  - command: "/tmp/ai_soc_v2_build/V2-P03D/minimc-probe --self-check"
    cwd: /home/sushaohua/workspace/ai_soc_project
    exit_code: 0
raw_log_paths:
  - docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/01_precheck.log
  - docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/02_probe_compile.log
  - docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/03_cli.log
candidate_commit: null
candidate_commit_or_diff_sha256: "soc-ap/tests/protocol/probe.cpp"
candidate_diff_sha256: null
artifact_hashes:
  - path: soc-ap/tests/protocol/probe.cpp
    size: 19372
    sha256: 7ff67bc4ddba74d3849e04ccfb7c90358de71e3d0d753c9fd064ba83ac8d447a
actual_cases:
  - "实现零第三方 JSON 依赖的独立命令行测试探针 minimc-probe"
  - "支持 --self-check 与 --help 自检模式，退出码 0"
  - "支持 crc 子命令，接收 --hex 计算并输出 crc16_hex, crc16_dec, crc16_le_hex"
  - "支持 encode 子命令，单向调用 minimc::encode_frame，桩阶段返回 ERR_NOT_IMPLEMENTED 且退出码 126"
  - "支持 decode 子命令，单向调用 minimc::decode_frame，桩阶段返回 ERR_NOT_IMPLEMENTED 且退出码 126"
  - "支持 feed 子命令，支持切片流/等步长时钟驱动 parser_feed_byte，桩阶段返回 ERR_NOT_IMPLEMENTED 且退出码 126"
  - "支持 poll 与 reset 子命令，输出格式化键值对"
  - "探针仅作为单向适配薄层，自身严禁重复实现 CRC 或协议状态机，不伪造 PASS"
warnings: []
failures_and_corrections: []
actual_result: completed
unverified:
  - "需要独立审阅者 QA 进行命令行探针适配器与退出码契约的独立评审"
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

---

## 交付正文与执行报告

### 1. 本票实际修改与交付物

本微步任务卡 `V2-P03D` 由 `ENG-SIM` 角色执行，严格限制在 `write_scope` 范围内：
1. **测试探针交付物**: `soc-ap/tests/protocol/probe.cpp`
   - 文件大小：`19,372` 字节
   - SHA256：`7ff67bc4ddba74d3849e04ccfb7c90358de71e3d0d753c9fd064ba83ac8d447a`
   - 实现内容：
     - **纯标准 C++17 实现**：零第三方外部 JSON 依赖，无任何额外库包引入；
     - **单向适配薄层**：严格仅调用 `codec.h` 与 `parser.h` 接口，原样透传与格式化输出，探针自身严禁重复实现任何协议或算法逻辑；
     - **支持全部 6 大子命令与自检**：
       - `--self-check` / `--help`：输出探针版本与子命令列表，退出码 `0`；
       - `crc --hex <hex_string>`：调用 `calc_crc16` 并格式化输出大端与小端 hex 及十进制；
       - `encode --src ... --dst ... --cmd ... --seq ... --flags ... --hop ... --route ... --payload-hex ... [--buf-size ...]`: 单向驱动 `encode_frame`，桩阶段返回 `not_implemented` 且退出码 `126`；
       - `decode --hex <hex_frame>`: 单向驱动 `decode_frame`，桩阶段返回 `not_implemented` 且退出码 `126`；
       - `feed [--stream-hex ... --timestamps-ms ...] [--start-ms ... --step-ms ...]`: 驱动 `parser_feed_byte`，桩阶段返回 `not_implemented` 且退出码 `126`；
       - `poll --now-ms <t1,t2,...>`: 驱动 `parser_poll_timeout`；
       - `reset`: 驱动 `parser_reset`。
     - **退出码契约**：严格遵循 0（成功/符合预期）、2（参数错误）、126（桩未实现）。
2. **构建与自检验证**:
   - `precheck`: 工作区 HEAD `f508954594b91f2a9daca58dd6087cba3b0b7506`，干净无多余脏改动；
   - `probe_compile`: 使用 `c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror` 联合编译 `probe.cpp`, `codec.cpp`, `parser.cpp` 生成二进制探针 `minimc-probe`，零告警零报错（退出码 0）；
   - `cli`: 运行 `/tmp/ai_soc_v2_build/V2-P03D/minimc-probe --self-check` 输出自检通过（退出码 0）。
3. **执行证据与原始日志**:
   - `docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/01_precheck.log`
   - `docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/02_probe_compile.log`
   - `docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/03_cli.log`
   - `docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/result.md`

### 2. 边界合规确认

- 严禁修改路径：未触碰 `mcu-p3/**`、`test_harness/**` 或 `project-control/.agents/**`。
- 回退范围：若本票被退回，仅需删除 `soc-ap/tests/protocol/probe.cpp` 与证据目录，无任何上游污染。
- 提审申请：编译与自检验证全部通过，现提交 COORD（`9e5411f4-acad-421e-b487-9e68b9483320`），申请更新任务状态为 `Review` 并交由独立审阅者 QA（`663fcda3-b02b-4d3a-89f6-ffc1ef283810`）进行独立评审。
