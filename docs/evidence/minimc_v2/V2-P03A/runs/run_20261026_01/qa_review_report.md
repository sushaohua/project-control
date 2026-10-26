# V2-P03A 独立 QA 审查报告 (`run_20261026_01`)

## 1. 审查元数据

- **Task ID**: `V2-P03A` (`提供编解码符号桩`, Revision `1`)
- **Run ID**: `run_20261026_01`
- **被审角色与会话 (`Executor`)**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T19:27:37+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/core/forward/minimc/codec.cpp`:
    - **SHA256**: `5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3` (`1060` bytes, `39` lines)
  - 关联执行记录与日志:
    - `project-control/docs/evidence/minimc_v2/V2-P03A/runs/run_20261026_01/result.md`
    - `project-control/docs/evidence/minimc_v2/V2-P03A/runs/run_20261026_01/01_precheck.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03A/runs/run_20261026_01/02_compile_stub.log`
    - `project-control/docs/evidence/minimc_v2/V2-P03A/runs/run_20261026_01/03_symbols.log`
- **前置依赖版本绑定核验**:
  - `V2-P02A` (`soc-ap/core/forward/minimc/codec.h`): `sha256:733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75`
  - `MiniMCProto v2.0 Rev 2.0.3`: `sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`
- **独立审查结论 (`Decision`)**: **`APPROVED`**

---

## 2. 审查核查项逐条对账

| 核查项 | 任务卡 `V2-P03A` 判据要求 | `codec.cpp` 实测实现与符号核验 | 结论 |
| :--- | :--- | :--- | :--- |
| 仅定义已冻结的 3 个编解码符号 | 只定义 `codec.h` 中已冻结的 `calc_crc16`、`encode_frame`、`decode_frame` 符号 | `codec.cpp` 仅包含 `#include "codec.h"` 并定义 `minimc::calc_crc16`、`minimc::encode_frame`、`minimc::decode_frame`；`nm -C --defined-only` 确认仅导出上述 3 个全局函数符号（`T`） | **PASS** |
| `calc_crc16` 桩行为 | 返回 `0` 并显式注释为桩阶段行为，不提前实现 CRC 算法 | L5-10 显式注释为 Stage V2-P03 symbol stub（真实实现定于 `V2-P04A`），`(void)data; return 0;` | **PASS** |
| `encode_frame` 桩行为 | 清零输出长度 `*out_written = 0`，严格返回 `Status::ERR_NOT_IMPLEMENTED` | L12-25 检查 `if (out_written != nullptr) { *out_written = 0; }`，并返回 `Status::ERR_NOT_IMPLEMENTED` | **PASS** |
| `decode_frame` 桩行为 | 重置 `*out_frame = {}`，严格返回 `Status::ERR_NOT_IMPLEMENTED` | L27-36 检查 `if (out_frame != nullptr) { *out_frame = {}; }`，并返回 `Status::ERR_NOT_IMPLEMENTED` | **PASS** |
| 负向防作弊红线 | 严禁将空输出或 CRC=0 判定为实现成功；严禁提前实现真实算法或改动接口 | 未改动 `codec.h`（SHA256 保持 `733b589b...`），未提前实现 CRC 或载荷复制，严格返回 `ERR_NOT_IMPLEMENTED` | **PASS** |

---

## 3. 独立复现验证日志

### 3.1 Precheck、Stub 编译、符号表核验与 `check_task_graph.py`

独立执行命令：
```bash
git -C soc-ap rev-parse HEAD && git -C soc-ap status --porcelain=v1 && git -C test_harness rev-parse HEAD && git -C test_harness status --porcelain=v1 && mkdir -p /tmp/ai_soc_v2_build/V2-P03A && c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc -c soc-ap/core/forward/minimc/codec.cpp -o /tmp/ai_soc_v2_build/V2-P03A/codec.o && nm -C --defined-only /tmp/ai_soc_v2_build/V2-P03A/codec.o && sha256sum soc-ap/core/forward/minimc/codec.cpp soc-ap/core/forward/minimc/codec.h && wc -c soc-ap/core/forward/minimc/codec.cpp && python3 project-control/tools/check_task_graph.py --check-artifact V2-P03A && date -Iseconds
```
- **退出码**: `0`
- **实际输出**:
```text
8a8d35a00c70de9faf65d9991491d2f5a41edb16
?? core/forward/minimc/codec.cpp
59d2320663dd7ef4a080272d624f831684935c34
0000000000000000 T minimc::calc_crc16(minimc::Bytes)
000000000000006b T minimc::decode_frame(minimc::Bytes, minimc::FrameView*)
0000000000000020 T minimc::encode_frame(minimc::FrameHeader const&, minimc::Bytes, minimc::MutableBytes, unsigned long*)
0000000000000000 W minimc::Bytes::Bytes()
0000000000000000 W minimc::Bytes::Bytes()
0000000000000000 n minimc::Bytes::Bytes()
5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3  soc-ap/core/forward/minimc/codec.cpp
733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75  soc-ap/core/forward/minimc/codec.h
1060 soc-ap/core/forward/minimc/codec.cpp
...
  "selected_artifacts": {
    "errors": [],
    "artifact_hashes": {
      "soc-ap/core/forward/minimc/codec.cpp": "5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3"
    },
    "scope": "presence/hash only; independent content review is still required"
  },
  "exit_code": 0
2026-10-26T19:27:37+08:00
```

### 3.2 作者执行记录与原始日志核验

- 核验 `project-control/docs/evidence/minimc_v2/V2-P03A/runs/run_20261026_01/result.md`：包含全部 15 项必填字段，记录的 `soc-ap/core/forward/minimc/codec.cpp` 大小（`1060` 字节）与 SHA256（`5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3`）与独立复现结果完全一致。
- 核验 `01_precheck.log`、`02_compile_stub.log` 与 `03_symbols.log`：与独立复现结果完全一致，工作区边界干净，仅修改了本卡 `write_scope` 允许的文件。

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`APPROVED`**
- **核准交付物版本**:
  - `soc-ap/core/forward/minimc/codec.cpp`: `sha256:5a35421cbf2e9d816db3dac7242b6878fa17de9e63a81e25facb4acb0fc3d8d3`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T19:27:37+08:00`
