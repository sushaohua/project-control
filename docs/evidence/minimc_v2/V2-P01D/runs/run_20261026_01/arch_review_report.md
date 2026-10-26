# 独立架构评审报告: V2-P01D (Review Run 1)

> **任务标识**: `V2-P01D` (Revision 1)  
> **任务标题**: 实现独立样例参考校验器  
> **被审作者会话 (QA)**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`  
> **独立审阅人会话 (ARCH)**: `1c634be7-4be2-4743-af02-dc8ada31bad3`  
> **审阅时间**: 2026-10-26T17:19:30+08:00  
> **被审交付物**: `test_harness/static_checks/minimcproto/reference_vectors.py`  
> **交付物 SHA256**: `a8664e5d461a960feaf4d28fc1e73e2fac5ebf568da202df552b849e2382d67a` (28,503 字节, 668 行)  
> **前置消费依赖**:
> - `test_harness/test_cases/minimcproto/vectors.json` (`sha256:6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995`)
> - `soc-ap/contracts/minimcproto/v2-minimal.md` (`sha256:5fc11e865fde44d780db94487855a7d762092a38362e9be66491b66626ad5ade`)
> - `soc-ap/contracts/minimcproto/v2-commands.md` (`sha256:25345c74b20051266626a1684be7f68f49bb570382969364b39301b7496a05e4`)
> - 协议形式化基线: `SPEC-PROTO-20261015-153000` (Rev 2.0.3, `sha256:9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54`)  
> **审阅结论**: **APPROVED (通过)**

---

## 1. 依赖与实现纯洁度核验 (Implementation Purity Audit)

1. **零第三方依赖**:
   - 脚本完整依赖导入仅包含 Python 3 标准库模块：`argparse`, `copy`, `hashlib`, `json`, `pathlib`, `struct`, `sys`, `typing`。
   - 无任何 `pip` 第三方库、无 `yaml` 或外部工具依赖。
2. **零生产代码与探针污染**:
   - 经全面代码符号与导入审查，脚本内部无任何针对 `soc-ap` 内部 C/C++ 模块、头文件或测试探针编译二进制的导入、链接或外部子进程调用。
   - 算法与流式状态机完全由纯 Python 独立实现，严格满足参考验证器的独立性要求。

---

## 2. 协议形式化逻辑与契约闭环核验 (Protocol Logic Audit)

1. **CRC-16/CCITT-FALSE 算法数学一致性**:
   - 函数 `calc_crc16_ccitt_false` 采用严格逐位计算模型，参数为：
     - 多项式 Poly: `0x1021` ($x^{16} + x^{12} + x^5 + 1$)
     - 初值 Init: `0xFFFF`
     - RefIn: `False` (MSB First)
     - RefOut: `False`
     - XorOut: `0x0000`
   - 与原稿规范 §3.1 / §4 及已验收契约 `v2-minimal.md` 完全一致。测试用例 `CRC-001` (`'123456789'` $\to$ `0x29B1`) 及 `CRC-002` (空输入 $\to$ `0xFFFF`)、`CRC-008` (CRC 零值) 均准确闭环。
2. **两层判定模型与端序解析**:
   - `reference_decode_frame`:
     - 严格遵循 `v2-minimal.md` 契约：$L+14$ 物理长度强校验、MTU $\le 1024$ 限制、`0x55 0xAA` 魔数定界。
     - 严格硬校验协议主版本 `(flags & 0x0C) == 0x04` (`PROTO_VERSION = 0b01`)。
     - 严格校验保留位 `(flags & 0xE0) == 0x00` 及路由互斥 `(route_ctrl & 0x03) != 0x03`。
     - 强制使用小端序解包与 `calculated == received` 显式比对，杜绝 Zero-CRC 歧义。
   - `reference_validate_command`:
     - 严格遵循 `v2-commands.md` 契约：
       - `GET_VERSION` (`0x01`): $L=0$, `WANTS_ACK=1`, `IS_RESPONSE=0`。
       - `VERSION_REPORT` (`0x02`): $L=16$, `IS_RESPONSE=1`, 主次协议版本硬断言 `2.0`。
       - `PING` (`0x03`): $L=4$, `WANTS_ACK=1`。
       - `PONG` (`0x04`): $L=12$, `IS_RESPONSE=1`, 尾部保留位 `reserved == 0`。
3. **OQ-01 开放冲突严格隔离**:
   - 针对黄金向量 `V04`（`CMD_EMERGENCY_STOP`, $L=0$），校验器在帧层解码确立其为结构有效帧（`frame_valid=True`，CRC `0xC13D`），但在命令业务层 `reference_validate_command` 中明确判定为 `False` 并返回 `"OQ-01_emergency_stop_conflict_or_out_of_scope"`。
   - 校验器中强制断言 `gf["command_valid"] is False` 且必须包含 `"OQ-01"` 说明，严禁静默裁决，完全符合任务要求。
4. **流式状态机 (ReferenceStreamFSM) 与超时边界**:
   - 严格映射 5 状态机模型（`WAIT_SOF1`, `WAIT_SOF2`, `READ_HEADER`, `READ_PAYLOAD`, `READ_CRC`）。
   - 字符间 50ms 超时严格执行“先检后刷”（check-before-refresh）铁律，且采用 `(now_ms - last_byte_rx_ms) & 0xFFFFFFFF > 50` 规范处理 `uint32_t` 毫秒时间戳回绕。
   - 满 12B 头末字节先存后判，超 MTU ($L>1024$) 立即递增 `err_mtu` 并复位，前导同步维持 `0x55 0x55 0xAA`，坏 CRC 静默丢弃并累加错误计数。

---

## 3. 独立复现执行与自检核验 (Execution & Self-Check Reproduction)

1. **`--check` 正向全量校验**:
   - 命令: `python3 test_harness/static_checks/minimcproto/reference_vectors.py --vectors test_harness/test_cases/minimcproto/vectors.json --check`
   - 退出码: `0`
   - 结果核查:
     - 黄金帧数量: 5 条（V01, V02_INBOUND, V02_OUTBOUND, V03, V04）全部通过；
     - 测试用例总数: 64 条（`stub`: 4, `crc`: 9, `encode`: 8, `decode_bounds`: 6, `decode`: 12, `stream_sync`: 5, `stream_header`: 5, `stream_payload`: 5, `timeout`: 6, `recovery`: 4）；
     - `errors`: `[]` (无任何错误)。
2. **`--self-check` 内存变异拒绝测试**:
   - 命令: `python3 test_harness/static_checks/minimcproto/reference_vectors.py --vectors test_harness/test_cases/minimcproto/vectors.json --self-check`
   - 退出码: `0` (所有变异均成功触发预期拦截)
   - 覆盖的 8 个内存变异场景核验：
     1. `corrupt_golden_v01_crc`: 篡改黄金帧 V01 CRC，触发 CRC mismatch 拦截；
     2. `corrupt_case_crc_001`: 篡改 CRC-001 预期，触发 CRC mismatch 拦截；
     3. `duplicate_case_id`: 制造重复 case_id，触发唯一性检查拦截；
     4. `empty_functional_group_timeout`: 清空 timeout 分组，触发非空分组拦截；
     5. `tamper_protocol_sha256`: 篡改协议基线 SHA256，触发基线校验拦截；
     6. `violate_v04_oq01_command_valid`: 将 V04 伪造为 `command_valid: True`，触发 OQ-01 规范拦截；
     7. `corrupt_decode_expected_seq`: 篡改 DEC-002 解码预期 seq，触发头部字段比对拦截；
     8. `corrupt_stream_expected_dispatched_frames`: 篡改 REC-004 分发帧数预期，触发流式断言拦截。

---

## 4. 终审结论

`test_harness/static_checks/minimcproto/reference_vectors.py` 具有极高工程规范度，依赖纯净，算法严谨，完整兑现了微步任务卡 `V2-P01D` 的所有交付与质量要求。

- **评审裁决**: **APPROVED (通过)**
- **建议**: 准予微步卡 `V2-P01D` 正式进入 `Done` 状态，放行首个 C11 结构与接口定义任务 `V2-P02A`。
