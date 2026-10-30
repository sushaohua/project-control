# TWIN-03 独立黄金预期与两阶段故障验收用例交付与自检报告 (Run 02 - 针对ARCH审查整改闭环)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-03` (独立黄金预期与两阶段故障验收用例) |
| **所属工作包** | `TASK-010` (验收首个多 Agent 端到端试点) |
| **执行角色** | `QA` (独立测试工程师) |
| **复核角色** | `ARCH` (系统架构师，待独立会话复核) |
| **当前轮次** | `run_02` (针对 Run 01 ARCH 审查意见的定向整改闭环) |
| **前置依赖** | `TWIN-02` (accepted version: `soc-ap: 532caecf3a146802969a49e73081400c2b32b25e`) |
| **前置证据** | `docs/evidence/twin/TWIN-02/runs/run_03/result.md` |
| **候选 Commit** | `test_harness: 0b7497ba43158841eb3c4af7f16e477b9c30c2c5` (已推送到远端 `origin/main`) |
| **执行状态** | **Completed / Delivered (定向整改 100% 达成，测试全绿，已推送到远端仓库)** |

---

## 1. 针对 Run 01 ARCH 审查发现的整改闭环落实 (Discrepancy Remediation)

针对独立 ARCH 审查会话 `01a18ab7-e3e0-7673-918e-aad60f325354` 出具的审查意见，本次 Run 02 实施了全量闭环整改：

| 发现项编号 | 严重度 | 原始审查意见 | Run 02 修复方案与代码落地 | 对应物证与测试 |
| :--- | :--- | :--- | :--- | :--- |
| **`ARCH-01`** | **Blocker** | `server_qa.json` 仅记录 1 项测试（任务图检查），未在隔离容器内实际运行黄金用例、模式验证、布局对账或捕获测试。 | 沙箱运行器 `qa_runner.py` 绑定命令 `python3 static_checks/twin/validate_schemas.py && python3 static_checks/twin/run_twin_cases.py && python3 static_checks/twin/reconcile_layout.py && python3 hil/twin_capture/test_twin_capture.py`，在只读沙箱内留存完整测试输出。 | 沙箱 `runtime.log` 完整记录全量测试执行与 PASS 输出。 |
| **`ARCH-02`** | **Major** | `run_twin_cases.py` 负例检查仅对 `NEG-TEL-006` 和 `007` 断言失败；`NEG-TEL-008` 及时间戳、代次、重复序号和零回包用例仅计数，不判定预期行为。 | 完善 `verify_telemetry_negatives`：<br>1. 对 `NEG-TEL-001` 断言时间戳递减与错误码 `TIMESTAMP_REGRESSION_DETECTED`；<br>2. 对 `NEG-TEL-002` 断言代次倒退与错误码 `STALE_GENERATION_ID`；<br>3. 对 `NEG-TEL-003` 断言重复序列号错误；<br>4. 对 `NEG-TEL-004/005` 断言上下限越界错误码；<br>5. 对 `NEG-TEL-008` 等注入帧断言 `verify_wire_frame_hex` 必须返回失败；<br>6. 对 `NEG-TEL-009` 断言失联 15s 产生 `QUALITY_FAULT` 与通信丢失告警。 | `run_twin_cases.py` 7 套测试用例 100% 通过。 |
| **`ARCH-03`** | **Major** | D-Bus 检查仅要求 `expected_error_name` 存在，不核对错误码或准入结果；SSE 检查缺少状态与拓扑流转语义校验。 | 完善 `verify_dbus_cases`：<br>1. 校验 `expected_error_name` 必须符合 `org.aisoc.Error.*` 命名规范；<br>2. 对所有失败用例，校验必须具有显式拒绝或错误标识（`error_code < 0` 或 `accepted == False` 或 `cleared == False` 或 `expected_status` 非空）；<br>3. 对所有成功用例，校验 `error_code == 0` 且未被拒绝；<br>4. 信号用例严格校验 `emitted_args` 字典有效性。 | `run_twin_cases.py` 中 27 项 D-Bus 黄金用例全量对账通过。 |
| **`ARCH-04`** | **Major** | 遥测哨兵检查未与黄金字段逐项对账；热床温度路径未验证 `deci_c` 到 `millic` 的换算。 | 1. 在 `verify_nozzle_and_bed` 中为全部 4 路热床用例补齐 `wire_temp_deci_c * 100 == temperature_millic` 及 `temperature_millic / 1000.0 == temperature_c` 的双向精准对账断言。<br>2. 在 `verify_sentinels_and_freshness` 中补齐 `expected_dds_millic` 哨兵值与 `expected_sensor_status_dds` 的严格断言。 | `run_twin_cases.py` 全量通过。 |
| **`ARCH-05`** | **Minor** | CRC16 验证缺少独立已知校验向量，`check_layout.c` 仅断言非零。 | 1. 在 `check_layout.c` 的 `test_crc_calculation` 中引入标准已知测试向量 `"123456789"`，严格断言计算结果等于 `0x29B1U`。<br>2. 在 `run_twin_cases.py` 中新增 `CRC16-KNOWN-VECTORS` 独立验证套件，严格断言 `"123456789"` 映射 `0x29B1` 且空缓冲为 `0xFFFF`。<br>3. 在 `test_twin_capture.py` 中新增相同断言。 | `check_layout.c` 与 Python 单测均严格核验 0x29B1。 |
| **`ARCH-06`** | **Minor** | 捕获分析器超出 15ms 的 jitter violation 不会令 CLI 失败；双环境对账缺少 `src_id` 与 `dst_id` 对齐。 | 1. `twin_capture_analyzer.py` 的 `main()` 入口中若检测到 `violations > 0`，退出码强制返回 1，形成 CLI 级硬门禁失败拦截。<br>2. `align_dual_traces` 中补齐 `src_id` 与 `dst_id` 的双端严格匹配。 | `test_twin_capture.py` 8 项测试全部通过。 |

---

## 2. 交付物物证清单与最新 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 | 对应 Commit |
| :--- | :--- | :--- | :--- |
| `test_harness/test_cases/twin/golden_telemetry_cases.json` | 遥测黄金向量（Fast DDS 100ms周期、4路喷嘴、热床/机箱、哨兵与负例） | `bb0b37641b452bb340bc217e809102d7be362a659ab5f7895e38d9b11cbf2945` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/test_cases/twin/golden_dbus_cases.json` | D-Bus 统一控制准入与错误码黄金预期集 | `15703beb77b0cb362395d9de3bd87542863e346d087e937a78c284258cec22fe` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/test_cases/twin/golden_sse_cases.json` | HTTP REST 与 SSE 实时事件流黄金预期集 | `2c8032df9362e3378d41be50e26d0e9b3cde4d94a1383fb93ccbc214280e6799` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/static_checks/twin/validate_schemas.py` | Draft7Validator 自动化正反例矩阵验证脚本 | `55b0a21c72340d5fc5c0b13866fb90dfe24124c988b63df5fcd2b484e9ae3d35` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/static_checks/twin/fallback_validator.py` | 纯 Python JSON Schema Draft-07 离线轻量验证器（无第三方依赖） | `c741dfccabaa84afef299d3bd374a0791c3f8efebd52f22ba513ce11a77f45a6` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/static_checks/twin/check_layout.c` | C/C++ 内存布局、偏移量、已知 CRC-16 (0x29B1) 校验程序 | `98f8e97f89adebee2444f637d5e1b5d219abce23f48b3b50760eada1b0fa7f3f` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/static_checks/twin/reconcile_layout.py` | C/C++ 结构体与 Fast DDS IDL 静态与二进制对账脚本 | `e34d19dd9128f743efe64dc84b569cd10c025ba6b83af40456c34d1b72dc51dd` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/static_checks/twin/run_twin_cases.py` | 独立黄金预期、负例断言与 CRC-16 已知向量综合测试运行器 | `41b03fbe9f93c1a9e6de71aff98c688ca60fc34312f0d2edcc4844170c1879a4` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/hil/twin_capture/twin_capture_analyzer.py` | 虚拟/物理帧捕获、抖动门禁与端到端对账工具（抖动违例 CLI 返回 1） | `b662df9145ffdb2fdd0428425d48f2f6361de4f9aa8136c60c68cea46af28073` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |
| `test_harness/hil/twin_capture/test_twin_capture.py` | 捕获分析器单测（含已知 CRC-16 向量与 AST 门禁核验） | `6c8d4d7f6b3f8147f2a0df127b486b2de4d100940bf5ef126b601d5029b82884` | `0b7497ba43158841eb3c4af7f16e477b9c30c2c5` |

---

## 3. 门禁规范符合性自检 (Coding Standard Compliance)

依据《代码编写规范与硬性门禁》（`c_cpp_coding_standard.md`）：
- **函数行数与参数门禁**：通过 Python AST 语法树全自动静态校验，所有自研新增/修改非结构体函数行数均 $\le 50$ 行，入参个数 $\le 4$ 个。
- **纯栈内存模型**：`check_layout.c` 保持 100% 零动态堆内存分配（禁用 malloc/free），采用 C11 `_Static_assert` 进行编译期对齐与偏移量核验。
- **已知黄金校验和**：已将独立国际标准向量 `"123456789"` $\to$ `0x29B1` 贯穿嵌入 C 语言布局测试、Python 综合运行器与捕获分析器单测中。
