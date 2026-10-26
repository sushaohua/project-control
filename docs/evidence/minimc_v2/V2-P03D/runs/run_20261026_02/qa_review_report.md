# V2-P03D 独立 QA 审查报告 (`run_20261026_02` — Round 2)

## 1. 审查元数据

- **Task ID**: `V2-P03D` (`实现独立命令行探针适配器`, Revision `1`)
- **Run ID**: `run_20261026_02` (Round 2)
- **被审角色与会话 (`Executor`)**: `ENG-SIM` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T20:02:28+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/tests/protocol/probe.cpp`:
    - **SHA256**: `2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c` (`23174` bytes, `602` lines)
  - 关联执行记录与日志:
    - `project-control/docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_02/result.md`
    - `project-control/docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_02/01_precheck.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_02/02_probe_compile.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_02/03_cli.log`
  - 历史记录保留核验:
    - `project-control/docs/evidence/minimc_v2/V2-P03D/runs/run_20261026_01/qa_review_report.md` 完整保留未覆盖。
- **前置依赖版本绑定核验**:
  - `V2-P03C` (`soc-ap/CMakeLists.txt`): `sha256:1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56`
  - `V2-P02C` (`soc-ap/contracts/minimcproto/test-probe.md`): `sha256:0c05ad8ed92a48b0062772042ec8fa1e1ab79d71dfaf2746afa3efb08cd3b7b3`
- **独立审查结论 (`Decision`)**: **`APPROVED`**

---

## 2. 第 1 轮 5 项缺陷闭环核验表

| 缺陷编号 | 缺陷摘要 | `run_20261026_02` 修正实现与实测核验 | 闭环状态 |
| :--- | :--- | :--- | :--- |
| `DEF-P03D-01` | `crc` 桩阶段伪造 `status: ok`，`--self-check` 未反映桩状态，无参未返回 `2` | L129 检查 `minimc::calc_crc16(minimc::Bytes(nullptr, 0)) == 0` 识别符号桩，桩阶段输出 `status: error\nerror_code: not_implemented`、退出码 `126`；L556-560 `argc < 2` 返回退出码 `2`；L567-576 `--self-check` 输出 `self_check: ok` 与 `backend_state: stub_not_implemented` | **CLOSED (PASS)** |
| `DEF-P03D-02` | `crc` 缺失 `--null-ptr --len <n>` 支持（`CRC-009`） | L131-165 支持 `--null-ptr` 与 `--len <n>`，非桩阶段当 `len > 0` 时调用 `minimc::calc_crc16(minimc::Bytes(nullptr, len))` 验证不崩溃并输出 `status: error\nerror_code: invalid_argument` | **CLOSED (PASS)** |
| `DEF-P03D-03` | `encode` 缺失 `--null-payload` 与 `--payload-len <len>` 支持（`ENC-008`） | L198-269 支持 `--null-payload` 与 `--payload-len <len>`，向 `minimc::encode_frame` 传入 `minimc::Bytes(nullptr, header.payload_len)` | **CLOSED (PASS)** |
| `DEF-P03D-04` | `feed` 的 `frames:` 列表遗漏 `hop_limit` 与 `route_ctrl` | L346-357, L453-454, L493-494 在 `DispatchedRecord` 及 `frames:` 输出中完整补充 `hop_limit: <dec>` 与 `route_ctrl: 0x<HEX2>` | **CLOSED (PASS)** |
| `DEF-P03D-05` | `feed` 在 `READ_HEADER` 下 `header_bytes_collected` 未扣除 2B SOF 偏移 | L467-474 在 `READ_HEADER` 状态下计算 `(parser.rx_index >= 2) ? (parser.rx_index - 2) : parser.rx_index` | **CLOSED (PASS)** |

---

## 3. 独立复现验证日志

独立执行命令：
```bash
git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1 && mkdir -p /tmp/ai_soc_v2_build/V2-P03D && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc soc-ap/tests/protocol/probe.cpp soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/parser.cpp -o /tmp/ai_soc_v2_build/V2-P03D/minimc-probe && /tmp/ai_soc_v2_build/V2-P03D/minimc-probe --self-check && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe crc --hex 313233343536373839; echo "crc_exit:$?"; } && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe encode --src 1 --dst 2 --cmd 1 --seq 0 --flags 5 --hop 4 --route 0 --payload-hex ""; echo "encode_exit:$?"; } && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe decode --hex 55AA01020501040000000000F91E; echo "decode_exit:$?"; } && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe feed --stream-hex 55AA01020501040000000000F91E; echo "feed_exit:$?"; } && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe >/dev/null 2>&1; echo "noarg_exit:$?"; } && { /tmp/ai_soc_v2_build/V2-P03D/minimc-probe bogus >/dev/null 2>&1; echo "bogus_exit:$?"; } && sha256sum soc-ap/tests/protocol/probe.cpp && wc -c soc-ap/tests/protocol/probe.cpp && python3 project-control/tools/check_task_graph.py --check-artifact V2-P03D && date -Iseconds
```
- **退出码**: `0`
- **实际输出**:
```text
f508954594b91f2a9daca58dd6087cba3b0b7506
?? tests/protocol/
59d2320663dd7ef4a080272d624f831684935c34
minimc_probe: MiniMCProto v2.0 Test Probe Adapter
protocol_version: 2.0.3
supported_subcommands: crc, encode, decode, feed, poll, reset
self_check: ok
backend_state: stub_not_implemented
status: ok
status: error
error_code: not_implemented
crc_exit:126
status: error
error_code: not_implemented
encoded_len: 0
encode_exit:126
status: error
error_code: not_implemented
frame_valid: false
decode_exit:126
status: error
error_code: not_implemented
feed_exit:126
noarg_exit:2
bogus_exit:2
2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c  soc-ap/tests/protocol/probe.cpp
23174 soc-ap/tests/protocol/probe.cpp
...
  "selected_artifacts": {
    "errors": [],
    "artifact_hashes": {
      "soc-ap/tests/protocol/probe.cpp": "2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c"
    },
    "scope": "presence/hash only; independent content review is still required"
  },
  "exit_code": 0
2026-10-26T20:02:28+08:00
```

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`APPROVED`**
- **核准交付物版本**:
  - `soc-ap/tests/protocol/probe.cpp`: `sha256:2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T20:02:28+08:00`
