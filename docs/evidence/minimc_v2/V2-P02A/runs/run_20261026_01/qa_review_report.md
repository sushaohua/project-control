# V2-P02A 独立 QA 审查报告 (`run_20261026_01`)

## 1. 审查元数据

- **Task ID**: `V2-P02A` (`定义无堆分配编解码接口`, Revision `1`)
- **Run ID**: `run_20261026_01`
- **被审角色与会话 (`Executor`)**: `ENG-FWD` (`1c634be7-4be2-4743-af02-dc8ada31bad3`)
- **独立审查角色与会话 (`Reviewer`)**: `QA` (`663fcda3-b02b-4d3a-89f6-ffc1ef283810`)
- **审查策略依据**: `project-control/.agents/rules/codex_qa_review.md`
- **审查时间**: `2026-10-26T18:35:00+08:00`
- **被审交付物及版本哈希**:
  - `soc-ap/core/forward/minimc/codec.h`:
    - **SHA256**: `733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75` (`6682` bytes, `207` lines)
  - 关联执行记录与日志:
    - `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/result.md`
    - `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/01_precheck.log`
    - `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/02_header_check.log`
- **前置依赖版本绑定核验**:
  - `V2-P01A` (`soc-ap/contracts/minimcproto/v2-minimal.md`): `sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade`
  - `V2-P01B` (`soc-ap/contracts/minimcproto/v2-commands.md`): `sha256:25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4`
  - `V2-P01D` (`test_harness/static_checks/minimcproto/reference_vectors.py`): `sha256:a8664e5d461a960feaf4d28fc1e73e2fac5ebf568da202df552b849e2382d67a`
  - `MiniMCProto v2.0 Rev 2.0.3`: `sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`
- **独立审查结论 (`Decision`)**: **`APPROVED`**

---

## 2. 审查核查项逐条对账

### 2.1 依赖与零堆分配核查 (Zero-Heap & Self-Containment)

| 核查项 | 规范要求 | `codec.h` 实测实现 | 结论 |
| :--- | :--- | :--- | :--- |
| 头文件保护 | `#pragma once` / Include Guard | L1-3, L206 同时具备 `#pragma once` 与 `SOC_AP_CORE_FORWARD_MINIMC_CODEC_H` 保护宏 | **PASS** |
| 标准库依赖最小化与自包含 | 仅包含必需的基础定长整数与大小头文件，无额外依赖 | L5-6 仅包含 `#include <cstddef>` 与 `#include <cstdint>` | **PASS** |
| 零动态堆内存分配 | 零 `malloc/free`、零 `new/delete`、无 `std::vector`/`std::string` 等动态容器 | 全文仅含 POD/trivial 值类型、指针+长度非持有切片与 `noexcept` 函数声明，零堆分配 | **PASS** |

### 2.2 接口规范与正反判据核验

| 核查项 | 任务卡 `V2-P02A` 与前置契约要求 | `codec.h` 实测定义与契约 | 结论 |
| :--- | :--- | :--- | :--- |
| 协议常量与掩码定义 | `SOF=0x55/0xAA`, `HEADER_SIZE=12`, `CRC_SIZE=2`, `MIN_FRAME_SIZE=14`, `MAX_PAYLOAD_SIZE=1024`, `MAX_FRAME_SIZE=1038`, `INTER_BYTE_TIMEOUT_MS=50`，以及 `Flags` / `Route_Ctrl` 掩码 | L15-38 完整定义为 `inline constexpr` 常量，与 `v2-minimal.md` §1.2/§1.3/§2.2 逐位一致 | **PASS** |
| 非持有内存切片 (`Bytes` / `MutableBytes`) | 指针+大小非持有设计，明确输入别名生命周期 | L46-66 定义 `Bytes { const uint8_t* data; size_t size; }` 与 `MutableBytes { uint8_t* data; size_t size; }` 及 `as_bytes()`，显式声明底层缓冲区生命周期必须长于视图 | **PASS** |
| 状态码 (`Status`) | 完备涵盖成功、参数/容量错误、帧长/MTU错误、头字段/CRC错误及未实现桩状态 (`ERR_NOT_IMPLEMENTED`) | L72-105 定义 `enum class Status : int32_t`，含 `OK = 0`、`ERR_INVALID_ARGUMENT = 1`、`ERR_BUFFER_TOO_SMALL = 2`、`ERR_FRAME_TOO_SHORT = 3`、`ERR_MTU_EXCEEDED = 4`、`ERR_LENGTH_MISMATCH = 5`、`ERR_BAD_SOF = 6`、`ERR_BAD_VERSION = 7`、`ERR_BAD_FLAGS_RESERVED = 8`、`ERR_BAD_ROUTE_CTRL = 9`、`ERR_CRC_MISMATCH = 10`、`ERR_INVALID_FRAME = 11`、`ERR_NOT_IMPLEMENTED = 12` 及 `status_to_string()` | **PASS** |
| 帧头与借用帧视图 (`FrameHeader` / `FrameView`) | 12 字节帧头字段 (`sof_1`, `sof_2`, `src_id`, `dst_id`, `flags`, `cmd_id`, `hop_limit`, `route_ctrl`, `seq`, `payload_len`)；`FrameView` 为借用视图 | L113-133 定义 12 字节自然对齐 `FrameHeader` 与 `FrameView { FrameHeader header{}; Bytes payload{}; uint16_t crc = 0; }`，明确 `payload` 直接借用自输入 `frame_bytes` 缓冲区 | **PASS** |
| `calc_crc16` 声明与 `0x0000` 合法性 | `CRC-16/CCITT-FALSE` 签名，明确 `0x0000` 为合法 CRC 值，不得当作失败 | L139-144 声明 `uint16_t calc_crc16(Bytes data) noexcept;`，注释契约明确规定返回值 `0x0000` 是有效校验和、严禁视作错误 | **PASS** |
| `encode_frame` 声明与防假成功契约 | 明确输出容量不足返回 `ERR_BUFFER_TOO_SMALL`、超 MTU 返回 `ERR_MTU_EXCEEDED`、失败时清零 `out_written` | L146-165 声明 `Status encode_frame(const FrameHeader& header, Bytes payload, MutableBytes out_buffer, size_t* out_written) noexcept;`，明确规定失败时 `*out_written = 0`，杜绝假成功 | **PASS** |
| `decode_frame` 声明与内存安全契约 | 禁止将未对齐字节流直接强转为 packed 结构体指针解引用；失败时重置 `out_frame` | L167-191 声明 `Status decode_frame(Bytes frame_bytes, FrameView* out_frame) noexcept;`，Memory Safety Rule 明确禁止直接将字节流强转为 packed 结构体指针解引用，要求按字节偏移提取字段 | **PASS** |

---

## 3. 独立验证命令与结果记录

### 3.1 交付物哈希与任务图工具独立校验

执行命令：
```bash
python3 project-control/tools/check_task_graph.py --check-artifact V2-P02A
```
- **退出码**: `0`
- **关键输出摘录**:
```json
  "selected_artifacts": {
    "errors": [],
    "artifact_hashes": {
      "soc-ap/core/forward/minimc/codec.h": "733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75"
    },
    "scope": "presence/hash only; independent content review is still required"
  },
  "exit_code": 0
```

### 3.2 执行记录与原始日志核验

- 核验 `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/01_precheck.log`：
  - `soc-ap` 基线 HEAD 为 `849135ee69500e7e96ee75eed73c245e1ac94851`，`test_harness` 基线 HEAD 为 `59d2320663dd7ef4a080272d624f831684935c34`，退出码 `0`。
- 核验 `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/02_header_check.log`：
  - 命令 `c++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I soc-ap/core/forward/minimc -x c++ -fsyntax-only -include codec.h /dev/null` 退出码 `0`，零警告。
- 核验 `project-control/docs/evidence/minimc_v2/V2-P02A/runs/run_20261026_01/result.md`：
  - 包含全部 15 项必填执行记录字段，记录的文件大小（`6682` 字节）与 SHA256（`733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75`）与磁盘文件完全一致。
  - *注：本独立审查会话在尝试并发运行无沙箱 shell 的 `git` 与 `c++` 命令时触发了宿主环境权限拦截（Permission prompt denied），按系统安全规则不绕过权限拦截，通过 `check_task_graph.py --check-artifact V2-P02A`（退出码 `0`）、源码逐行静态审计以及作者原始日志交叉验证完成了全部核查项确认。*

---

## 4. 最终独立审查结论与签署

- **审查结论 (`Decision`)**: **`APPROVED`**
- **核准交付物版本**:
  - `soc-ap/core/forward/minimc/codec.h`: `sha256:733b589bf4ddb08c6108ffdc039acaab4992425bf1393a3dd94ae19f91fc0e75`
- **独立审查签名**:
  - Reviewer Role: `QA`
  - Reviewer Session: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`
  - Timestamp: `2026-10-26T18:35:00+08:00`
