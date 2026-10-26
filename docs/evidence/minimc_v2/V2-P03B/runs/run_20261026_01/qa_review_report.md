# V2-P03B 独立 QA 审查报告 (`run_20261026_01`)

## 1. 审查元数据

- **Task ID**: `V2-P03B` (`提供解析器符号桩`, Revision `1`)
- **Run ID**: `run_20261026_01`
- **被审角色与会话 (`Executor`)**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T19:34:03+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/core/forward/minimc/parser.cpp`:
    - **SHA256**: `16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4` (`1499` bytes, `56` lines)
  - 关联执行记录与日志:
    - `project-control/docs/evidence/minimc_v2/V2-P03B/runs/run_20261026_01/result.md`
    - `project-control/docs/evidence/minimc_v2/V2-P03B/runs/run_20261026_01/01_precheck.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03B/runs/run_20261026_01/02_compile_stub.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03B/runs/run_20261026_01/03_symbols.log`
- **前置依赖版本绑定核验**:
  - `V2-P02B` (`soc-ap/core/forward/minimc/parser.h`): `sha256:a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe`
  - `V2-P03A` (`soc-ap/core/forward/minimc/codec.cpp`): `sha256:5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3`
  - `MiniMCProto v2.0 Rev 2.0.3`: `sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`
- **独立审查结论 (`Decision`)**: **`APPROVED`**

---

## 2. 审查核查项逐条对账

| 核查项 | 任务卡 `V2-P03B` 判据要求 | `parser.cpp` 实测实现与符号核验 | 结论 |
| :--- | :--- | :--- | :--- |
| 仅定义已冻结的 4 个解析器符号 | 只定义 `parser.h` 中已冻结的 `parser_init`、`parser_reset`、`parser_feed_byte`、`parser_poll_timeout` 符号 | `parser.cpp` 仅包含 `#include "parser.h"` 并在 `namespace minimc` 下定义上述 4 个函数；`nm -C --defined-only` 确认仅导出该 4 个全局函数符号（`T`） | **PASS** |
| `parser_init` 行为 | 空指针保护，零堆内存分配，初始化解析器及清零计数器 | L5-10 `if (!parser) return; *parser = StreamParser{};`，零堆分配 | **PASS** |
| `parser_reset` 行为 | 空指针保护，重置 `state=WAIT_SOF1` 及游标，严格保留 6 项诊断计数器 | L12-22 重置 `state`、`rx_index`、`expected_len`、`last_byte_rx_ms`，保留 `err_sof`、`err_header`、`err_mtu`、`err_crc`、`err_timeout`、`dispatched_frames` | **PASS** |
| `parser_feed_byte` 桩行为 | 空指针检查返回 `ERR_INVALID_ARGUMENT`；置位 `*out_frame_ready = false`、重置 `*out_frame = FrameView{}`；返回 `Status::ERR_NOT_IMPLEMENTED` | L24-44 检查 `if (!parser \|\| !out_frame_ready) return Status::ERR_INVALID_ARGUMENT;`，置 `*out_frame_ready = false;` 与 `*out_frame = FrameView{};`，返回 `Status::ERR_NOT_IMPLEMENTED` | **PASS** |
| `parser_poll_timeout` 桩行为 | 桩阶段严格返回 `false` | L46-53 显式注释为 Stage V2-P03 symbol stub（真实超时逻辑定于 `V2-P05D`），返回 `false` | **PASS** |
| 负向防作弊红线 | 不加入同步、载荷处理或超时算法；不修改 `parser.h`/`codec.h`；无堆分配 | `parser.h` (`a4397848...`)、`codec.h` (`733b589b...`)、`codec.cpp` (`5a35421c...`) SHA256 均未变化；未提前加入任何流式状态机或超时逻辑 | **PASS** |

---

## 3. 独立复现验证日志

### 3.1 Precheck、Stub 编译、符号表核验与 `check_task_graph.py`

独立执行命令：
```bash
git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1 && mkdir -p /tmp/ai_soc_v2_build/V2-P03B && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc -c soc-ap/core/forward/minimc/parser.cpp -o /tmp/ai_soc_v2_build/V2-P03B/parser.o && nm -C --defined-only /tmp/ai_soc_v2_build/V2-P03B/parser.o && sha256sum soc-ap/core/forward/minimc/parser.cpp soc-ap/core/forward/minimc/parser.h soc-ap/core/forward/minimc/codec.h soc-ap/core/forward/minimc/codec.cpp && wc -c soc-ap/core/forward/minimc/parser.cpp && python3 project-control/tools/check_task_graph.py --check-artifact V2-P03B && date -Iseconds
```
- **退出码**: `0`
- **实际输出**:
```text
e0896cb1b05031fddfddef88015ab004598343a2
?? core/forward/minimc/parser.cpp
59d2320663dd7ef4a080272d624f831684935c34
0000000000000000 T minimc::parser_init(minimc::StreamParser*)
0000000000000032 T minimc::parser_reset(minimc::StreamParser*)
0000000000000081 T minimc::parser_feed_byte(minimc::StreamParser*, unsigned char, unsigned int, minimc::FrameView*, bool*)
0000000000000174 T minimc::parser_poll_timeout(minimc::StreamParser*, unsigned int)
0000000000000000 W minimc::Bytes::Bytes()
0000000000000000 W minimc::Bytes::Bytes()
0000000000000000 n minimc::Bytes::Bytes()
16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4  soc-ap/core/forward/minimc/parser.cpp
a4397848a1c65b5a1e183b7a9e95283fb6908c4180b46701161de14b86575cbe  soc-ap/core/forward/minimc/parser.h
733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75  soc-ap/core/forward/minimc/codec.h
5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3  soc-ap/core/forward/minimc/codec.cpp
1499 soc-ap/core/forward/minimc/parser.cpp
...
  "selected_artifacts": {
    "errors": [],
    "artifact_hashes": {
      "soc-ap/core/forward/minimc/parser.cpp": "16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4"
    },
    "scope": "presence/hash only; independent content review is still required"
  },
  "exit_code": 0
2026-10-26T19:34:03+08:00
```

### 3.2 作者执行记录与原始日志核验

- 核验 `project-control/docs/evidence/minimc_v2/V2-P03B/runs/run_20261026_01/result.md`：包含全部 15 项必填字段，记录的 `soc-ap/core/forward/minimc/parser.cpp` 大小（`1499` 字节）与 SHA256（`16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4`）与独立复现结果完全一致。
- 核验 `01_precheck.log`、`02_compile_stub.log` 与 `03_symbols.log`：与独立复现结果完全一致，工作区边界干净，仅修改了本卡 `write_scope` 允许的文件。

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`APPROVED`**
- **核准交付物版本**:
  - `soc-ap/core/forward/minimc/parser.cpp`: `sha256:16a73b1105c78c85ca243f5a4b05d7f28875b4f29c39cb10b726c62ed2dda8d4`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T19:34:03+08:00`
