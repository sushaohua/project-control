# V2-P03D 独立 QA 审查报告 (`run_20261026_01`)

## 1. 审查元数据

- **Task ID**: `V2-P03D` (`实现独立命令行探针适配器`, Revision `1`)
- **Run ID**: `run_20261026_01`
- **被审角色与会话 (`Executor`)**: `ENG-SIM` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T19:53:41+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/tests/protocol/probe.cpp`:
    - **SHA256**: `7ff67bc4ddba74d3849e04ccfb7c90358de71e3d0d753c9fd064ba83ac8d447a` (`19372` bytes, `502` lines)
- **前置依赖版本绑定核验**:
  - `V2-P03C` (`soc-ap/CMakeLists.txt`): `sha256:1915f23ae45bcb8104cfe776687f84b518ddbc2041dd7bf5f573fc4d095f2a56`
  - `V2-P02C` (`soc-ap/contracts/minimcproto/test-probe.md`): `sha256:0c05ad8ed92a48b0062772042ec8fa1e1ab79d71dfaf2746afa3efb08cd3b7b3`
- **独立审查结论 (`Decision`)**: **`REJECTED`**

---

## 2. 阻断性缺陷清单 (Blocking Defects)

经独立编译复现与对照 `V2-P03D.md`、`test-probe.md` 及 `vectors.json` 全量用例规范审计，发现 `soc-ap/tests/protocol/probe.cpp` 存在以下 **5 项阻断性缺陷**（由于 `probe.cpp` 仅在本票 `V2-P03D` 的 `write_scope` 内，下游 `V2-P03F`～`V2-P05E` 均无权修改 `probe.cpp`，必须在本票修正）：

### `DEF-P03D-01`: `crc` 子命令在 P03 符号桩阶段伪造 `status: ok`（退出码 `0`），且 `--self-check` 未核验桩状态与无参拒绝
- **证据定位**: `soc-ap/tests/protocol/probe.cpp` L125-148 (`handle_crc`), L472-476 (`main`)。
- **实测复现输出**:
  ```text
  $ /tmp/ai_soc_v2_build/V2-P03D/minimc-probe crc --hex 313233343536373839
  status: ok
  crc16_hex: 0x0000
  crc16_dec: 0
  crc16_le_hex: 0000
  (exit_code: 0)
  ```
- **违规依据**:
  1. `V2-P03D.md` `negative_cases` 明确规定：“桩函数的 `not_implemented` 必须原样输出，不伪造 PASS”；`test-probe.md` §4.2 规定 `stub` 组的 `crc, encode, decode, feed` 均须输出 `status: error`、`error_code: not_implemented` 且退出码为 `126`；`vectors.json` 的 `STUB-001`（`operation: "crc"`, `raw_hex: "313233343536373839"`）将在 `V2-P03F` 运行并断言 `not_implemented`。
  2. `V2-P03D.md` `cli` 验证项（`minimc-probe --self-check`）要求：“CLI/错误适配检查通过；符号桩仍为 `not_implemented`，不能作为协议成功”。当前 `--self-check` 仅打印静态帮助文本，未调用底层接口检验错误适配，且无参数调用 `minimc-probe` (`argc < 2`) 返回 `0` 而非 `2` (`USAGE_ERROR`)。
- **修复要求**:
  - 在不内嵌 CRC 算法的前提下检测 `calc_crc16` 是否处于 P03 符号桩阶段：根据 `codec.h` L140 契约，真实 `CRC-16/CCITT-FALSE` 的 `Init=0xFFFF`，因此对 0 字节空切片 `minimc::calc_crc16(minimc::Bytes(nullptr, 0))` 必返回初始值 `0xFFFF`，而 `V2-P03A` 桩函数固定返回 `0`。`handle_crc` 只需检查 `if (minimc::calc_crc16(minimc::Bytes(nullptr, 0)) == 0)`，即可准确识别桩阶段并输出 `status: error\nerror_code: not_implemented`、返回退出码 `126`；进入 `V2-P04A` 真实实现后，空切片返回 `0xFFFF != 0`，同时对真实 CRC 为 `0x0000` 的 16B 帧（`CRC-008`）正常输出 `status: ok\ncrc16_hex: 0x0000`！
  - `argc < 2` 无参调用应打印用法并返回退出码 `2`。
  - `--self-check` 应实际探测 CLI 错误适配并报告当前底层接口状态（例如输出 `self_check: ok` 及各接口状态，同时不能把桩未实现宣称为协议已实现）。

### `DEF-P03D-02`: `crc` 子命令缺失空指针+非零长度测试参数支持（阻断 `V2-P04A` `CRC-009`）
- **证据定位**: `soc-ap/tests/protocol/probe.cpp` L125-148 (`handle_crc`)。
- **问题说明**: `vectors.json` 中 `CRC-009`（对应 `V2-P04A` `negative_cases`：“空指针且长度非0拒绝；不访问边界外字节”）输入为 `"input": { "null_pointer": true, "declared_length": 4 }`，预期输出 `status: error`、`error_code: invalid_argument`。当前 `handle_crc` 仅接受 `--hex`，无法向 `minimc::calc_crc16` 传入 `minimc::Bytes(nullptr, 4)`。
- **修复要求**:
  - 在 `handle_crc` 中支持 `--null-ptr` 与 `--len <declared_length>`（当指定 `--null-ptr` 且 `len > 0` 时，先检测是否处于桩阶段；若非桩阶段，调用 `(void)minimc::calc_crc16(minimc::Bytes(nullptr, len));` 验证底层函数对空指针+非零长度不发生解引用崩溃，随后输出 `status: error\nerror_code: invalid_argument` 并返回 `0`）。

### `DEF-P03D-03`: `encode` 子命令缺失空载荷指针与显式 `payload_len` 参数支持（阻断 `V2-P04B` `ENC-008`）
- **证据定位**: `soc-ap/tests/protocol/probe.cpp` L180, L195-200 (`handle_encode`)。
- **问题说明**: `vectors.json` 中 `ENC-008`（对应 `V2-P04B` `negative_cases`：“空指针/非0长度失败且无越界”）输入为 `header.payload_len = 4`, `null_payload_pointer = true`, `out_capacity = 18`，预期 `encode_frame` 返回 `Status::ERR_INVALID_ARGUMENT`（输出 `status: error`、`error_code: invalid_argument`、`encoded_len: 0`）。当前 `handle_encode` 强制覆写 `header.payload_len = static_cast<uint16_t>(payload_bytes.size())` 且始终传入非空 `payload_bytes.data()`，导致无法构造 `header.payload_len = 4` 且 `payload = minimc::Bytes(nullptr, 4)` 的调用。
- **修复要求**:
  - 在 `handle_encode` 中支持可选参数 `--payload-len <len>` 与 `--null-payload`（当未传 `--null-payload` 时 `--payload-hex` 必填；当传 `--null-payload` 时，`--payload-hex` 可省略，并将 `minimc::Bytes(nullptr, header.payload_len)` 传给 `minimc::encode_frame`）。

### `DEF-P03D-04`: `feed` 子命令输出的 `frames` 列表遗漏 `hop_limit` 与 `route_ctrl` 字段（阻断 `V2-P05C`～`V2-P05E`）
- **证据定位**: `soc-ap/tests/protocol/probe.cpp` L277-286 (`DispatchedRecord`), L377-386, L408-415 (`handle_feed`)。
- **问题说明**: `vectors.json` 中 `SPLD-001`～`SPLD-003`、`TMO-004`、`REC-001`～`REC-004` 的 `expected.frames` 均包含完整的 `hop_limit` 和 `route_ctrl` 字段断言（例如 `SPLD-002` 验证路由帧 `hop_limit: 3, route_ctrl: 4`）。当前 `DispatchedRecord` 及 `handle_feed` 输出的 `frames:` 列表遗漏了 `hop_limit` 和 `route_ctrl`。
- **修复要求**:
  - 在 `DispatchedRecord` 中保存 `hop_limit` 与 `route_ctrl`，并在 `frames:` 列表每项中输出 `hop_limit: <dec>` 与 `route_ctrl: 0x<HEX2>`（置于 `cmd_id` 之后、`seq` 之前）。

### `DEF-P03D-05`: `feed` 子命令 `header_bytes_collected` 计算未扣除 2 字节 SOF 偏移（阻断 `V2-P05A`/`V2-P05B` `SYNC-003` 与 `SHDR-001`）
- **证据定位**: `soc-ap/tests/protocol/probe.cpp` L394 (`handle_feed`)。
- **问题说明**: 根据 `parser.h` L18（`READ_HEADER = 2, ///< Collecting 10 remaining header bytes (offsets 0x02..0x0B)`）及 `vectors.json`，`SYNC-003`（馈送 `5555AA` 进入 `READ_HEADER`）预期 `header_bytes_collected: 0`，`SHDR-001`（馈送 `55AA` + 9 字节头，共 11 字节，`rx_index == 11`）预期 `header_bytes_collected: 9`。当前 `probe.cpp` L394 直接取 `parser.rx_index`，当 `parser.rx_buffer` 存入 `SOF1`、`SOF2`（`rx_index` 为 `2` 和 `11`）时会输出 `2` 和 `11` 而非 `0` 和 `9`。
- **修复要求**:
  - 计算 `header_bytes_collected` 时：当 `parser.state == minimc::ParserState::READ_HEADER` 且 `parser.rx_index >= 2` 时，取 `parser.rx_index - 2`（若 `parser.rx_index < 2` 则取 `parser.rx_index`；非 `READ_HEADER` 状态或已完成帧头时按协议状态输出）。

---

## 3. 独立复现验证日志

独立执行命令：
```bash
git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1 && mkdir -p /tmp/ai_soc_v2_build/V2-P03D && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc soc-ap/tests/protocol/probe.cpp soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/parser.cpp -o /tmp/ai_soc_v2_build/V2-P03D/minimc-probe && /tmp/ai_soc_v2_build/V2-P03D/minimc-probe --self-check && /tmp/ai_soc_v2_build/V2-P03D/minimc-probe crc --hex 313233343536373839 && sha256sum soc-ap/tests/protocol/probe.cpp && wc -c soc-ap/tests/protocol/probe.cpp && python3 project-control/tools/check_task_graph.py --check-artifact V2-P03D && date -Iseconds
```
- **实际输出摘录**:
```text
f508954594b91f2a9daca58dd6087cba3b0b7506
?? tests/protocol/
59d2320663dd7ef4a080272d624f831684935c34
minimc_probe: MiniMCProto v2.0 Test Probe Adapter
protocol_version: 2.0.3
supported_subcommands: crc, encode, decode, feed, poll, reset
status: ok
status: ok
crc16_hex: 0x0000
crc16_dec: 0
crc16_le_hex: 0000
7ff67bc4ddba74d3849e04ccfb7c90358de71e3d0d753c9fd064ba83ac8d447a  soc-ap/tests/protocol/probe.cpp
19372 soc-ap/tests/protocol/probe.cpp
```

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`REJECTED`**
- **被审交付物版本**:
  - `soc-ap/tests/protocol/probe.cpp`: `sha256:7ff67bc4ddba74d3849e04ccfb7c90358de71e3d0d753c9fd064ba83ac8d447a`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T19:53:41+08:00`
