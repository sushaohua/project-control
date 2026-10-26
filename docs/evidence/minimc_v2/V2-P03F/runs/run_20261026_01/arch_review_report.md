# 独立架构评审报告: V2-P03F (Review Run 1)

> **任务标识**: `V2-P03F` (Revision 1)  
> **任务标题**: 实现独立预期比较运行器  
> **被审作者会话 (QA)**: `663fcda3-b02b-4d3a-89f6-ffc1ef283810`  
> **独立审阅人会话 (ARCH)**: `1c634be7-4be2-4743-af02-dc8ada31bad3`  
> **审阅规范**: `project-control/.agents/rules/codex_qa_review.md`  
> **审阅时间**: 2026-10-26T20:27:30+08:00  
> **被审交付物**: `test_harness/static_checks/minimcproto/run_codec_cases.py`  
> **交付物 SHA256**: `e1384164c92078fe8dc71017d5128c0b0e610deb527f53d182efa6c5257f9cdf` (35,416 字节, 939 行)  
> **前置消费依赖**:
> - `test_harness/test_cases/minimcproto/vectors.json` (`sha256:6d46bd05a4133e678611abe2ab1cb88db190c394f23151900009c0c077c8d995`)
> - `test_harness/static_checks/minimcproto/reference_vectors.py` (`sha256:a8664e5d461a960feaf4d28fc1e73e2fac5ebf568da202df552b849e2382d67a`)
> - `soc-ap/contracts/minimcproto/test-probe.md` (`sha256:0c05ad8ed92a48b0062772042ec8fa1e1ab79d71dfaf2746afa3efb08cd3b7b3`)
> - `soc-ap/CMakeLists.txt` (`sha256:549df0a78f0baab9d6c3331c73cb590c3dd73a81d476c5b4aec7b8dfbb6053d8`)
> - `soc-ap/tests/protocol/probe.cpp` (`sha256:2ebee129e4c1d35fa394d74d8b5daf66e4480cb5b4671c89055af29be554b42c`)
> **审阅结论**: **APPROVED (通过)**

---

## 1. 依赖与实现纯洁度核验 (Implementation Purity Audit)

1. **零第三方依赖**:
   - 脚本完整导入仅包含 Python 3 标准库模块：`argparse`, `copy`, `json`, `os`, `pathlib`, `struct`, `subprocess`, `sys`, `tempfile`, `typing`。
   - 严禁且无任何 `pip` 第三方库、无 `yaml` 或外部工具依赖。
2. **单向预期权威 (Unidirectional Expectation Authority)**:
   - 运行器严格只读加载 `vectors.json` 作为唯一测试真理源；
   - 绝对不从探针 stdout 反向更新、推导或宽容覆盖预期值；
   - 探针交互完全基于标准子进程 `subprocess.Popen`，使用只读文本流通讯。

---

## 2. 探针适配与契约对齐核验 (Probe Contract Alignment)

1. **子命令完整映射**:
   - `crc`: 支持标准 `--hex`，并支持 V2-P04A 所需的 `--null-ptr` 与 `--len` 边界输入；
   - `encode`: 完整解包 header 各字段，支持 `payload_pattern` 展开、`--null-payload`、`--payload-len` 以及 `--buf-size`，精准对接 `ENC-001`～`ENC-008`；
   - `decode`: 支持十六进制帧与 `frame_pattern` 展开，并内置命令层验证与 `V04` `OQ-01` 冲突元数据比对；
   - `feed`: 完整支持 Mode A（逗号切片流与离散时间戳、`--reset-after`）与 Mode B（`byte_by_byte` 步长驱动与毫秒时钟）；
   - `poll`: 完整支持 `--now-ms` 时间戳列表驱动；
   - `reset`: 完整支持独立显式复位子命令。
2. **探针输出解析容错度与严格性**:
   - 解析函数 `parse_probe_stdout` 正确处理顶层键值对（`status`, `error_code`, `crc16_hex`, `encoded_len`, `raw_hex`, `frame_valid` 等）；
   - 正确处理嵌套段落 `frames:` 列表，完整保留并比对包含 `src_id`, `dst_id`, `flags`, `cmd_id`, `hop_limit`, `route_ctrl`, `seq`, `payload_len`, `payload_hex`, `crc16_hex` 的各帧字段；
   - 正确处理 `counters:` 段落，比对 6 大错误与分发计数器（`err_sof`, `err_header`, `err_mtu`, `err_crc`, `err_timeout`, `dispatched_frames`）。

---

## 3. 防作弊与红线规范核验 (Anti-Gaming & Invariants Audit)

1. **非空测试通过原则 (No Empty Test Pass)**:
   - 若匹配用例数为 0，运行器抛出 `No Empty Test Pass violation` 并以退出码 `2` 失败退出，绝不误判 PASS。
2. **桩用例严格隔离 (Stub Isolation)**:
   - `--case-set all` 仅调度 9 个正式功能分组（共 60 个用例），严格剔除 `stub` 分组；
   - `--case-set stub` 仅执行 `STUB-001`～`STUB-004`，断言退出码 `126` 与 `error_code: not_implemented`；
   - 在功能分组测试中，若底层后端返回退出码 `126` 或 `not_implemented`，运行器强制判定用例 `FAIL`（退出码 `1`），绝对杜绝未实现状态静默跳过或伪造 PASS。

---

## 4. 独立复现执行与自检核验 (Independent Verification Reproduction)

1. **运行器自检 (`--self-check`)**:
   - 执行命令: `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --self-check`
   - 退出码: `0`
   - 结果: 7/7 异常与边界防御路径全部通过：
     - `SELF-01`: 探针文件不存在拒绝 (退出码 2) -> `passed`
     - `SELF-02`: 探针不可执行拒绝 (退出码 2) -> `passed`
     - `SELF-03`: 未知用例分组拒绝 (退出码 2) -> `passed`
     - `SELF-04`: 空测试集 No Empty Test Pass 拦截 (退出码 2) -> `passed`
     - `SELF-05`: 子进程超时 0.1s 拦截 (退出码 1) -> `passed`
     - `SELF-06`: 功能分组遇到 not_implemented 严格判定失败 (退出码 1) -> `passed`
     - `SELF-07`: 探针输出字段值不匹配严格判定失败 (退出码 1) -> `passed`
2. **桩测试集实测 (`--case-set stub`)**:
   - 执行命令: `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P03F/bin/minimc-probe --case-set stub`
   - 退出码: `0`
   - 结果: 4/4 用例全部通过，准确核验了 `STUB-001` (crc), `STUB-002` (encode), `STUB-003` (decode), `STUB-004` (feed) 的符号桩 `exit_code == 126` 及 `not_implemented` 行为。
3. **真实功能分组防御实测**:
   - 针对当前符号桩执行 `crc` 功能分组：
     - 执行命令: `python3 test_harness/static_checks/minimcproto/run_codec_cases.py --vectors test_harness/test_cases/minimcproto/vectors.json --probe /tmp/ai_soc_v2_build/V2-P03F/bin/minimc-probe --case-set crc`
     - 退出码: `1`
     - 结果: 0/9 通过，9/9 失败，全部准确拦截 `unimplemented backend rejected on functional group 'crc'`，无任何伪造通过。
4. **宿主 Regression 测试**:
   - 执行命令: `env -C /tmp/ai_soc_v2_build/V2-P03F ctest --output-on-failure -R ^host_runtime_smoke$`
   - 退出码: `0` (1/1 测试通过，100% 通过)。

---

## 5. 终审结论

`test_harness/static_checks/minimcproto/run_codec_cases.py` 设计严密，代码质量优异，完全符合任务卡 `V2-P03F`、测试探针契约 `test-probe.md` 与独立 QA 审查规范。

- **评审裁决**: **APPROVED (通过)**
- **建议**: 准予微步卡 `V2-P03F` 正式通过，完成增量组 `V2-P03`（骨架与桩实现）的最后闭环，放行下一步真实功能实现 `V2-P04A`。
