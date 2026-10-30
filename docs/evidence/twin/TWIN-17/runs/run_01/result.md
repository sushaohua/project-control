# TWIN-17 本地离线作业引擎与基础混色执行规划交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-17` (本地离线作业引擎与基础混色执行规划) |
| **所属工作包** | `TASK-011` (实现离线作业引擎和混色样例) |
| **执行角色** | `ENG-STATE` (协力 `JOB`) |
| **当前轮次** | `run_01` (G-code 流式解析契约、作业生命周期状态机与双通道混色实现) |
| **前置依赖** | `TWIN-02` (Done) |
| **执行状态** | **Completed (契约定义、状态机实现及正反用例 100% 验证通过)** |

---

## 1. 核心架构与功能实现 (Architecture & Implementation)

依据 `PM:FEAT-COL-001`（混色首版）与 `TASK-011` 规划，完成了本地离线作业引擎与混色执行规范交付：
1. **统一作业生命周期状态模型 (`job_types.h`, `job_engine.h`)**：
   - 状态转移定义：`IDLE` $\to$ `PRINTING` $\rightleftharpoons$ `PAUSED` $\to$ `COMPLETED` / `CANCELED` / `ERROR`；
   - 挂起原因显式分类：`USER_REQUEST`, `FILAMENT_RUNOUT` (对接 HMS 0x3001), `TEMP_ABNORMAL`, `DOOR_OPEN`；
   - 绝对零动态堆内存分配：采用静态固定结构体 `aisoc_job_engine_t` 与千分比单调进度计算；
   - 尺寸与对齐严格静态断言：所有核心契约结构体具备 `sizeof` 与 `_Alignof` / `alignof` 编译期校验。
2. **基础多通道混色权重分配规范 (COL-001)**：
   - 支持最多 4 通道供料系统，基准权重总和恒定为 `10000` (100.00% 精度，0.01% 分辨率)；
   - 入参强校验：通道数必须为 $1 \sim 4$，权重累加和非 10000 立即拦截拒绝 (`AISOC_JOB_ERR_INVALID_MIXING_RATIO`)；
   - 支持单材料（100% 通道0）与多材料（如双通道 50%-50%）混色。
3. **G-code 离线流式逐行解析器 (`job_engine.c`)**：
   - 解析支持 `G0`, `G1` (X/Y/Z/E 坐标以微米 um 存储，进给速率 mm/min)；
   - 支持调温指令 `M104`, `M109`, `M140`, `M190` 以及混色指令 `M163`, `M164`；
   - 遇到急停 `M112` 立即瞬时熔断并中断当前所有作业；
   - 行内注释（`;`）与空白行安全旁路，畸形指令即时防御拒绝 (`AISOC_JOB_ERR_MALFORMED_GCODE`)。
4. **硬性编码规范合规**：
   - 所有自研函数长度 $\le 35$ 行（严控于 $\le 50$ 行硬门禁）；
   - 函数入参 $\le 3$ 个（严控于 $\le 4$ 个硬门禁）；
   - 指针解引用与取地址操作独立成行，公共函数首行防御性空指针校验（Guard Clause）；
   - 编译严格通过 C11 与 C++17 (`-fno-exceptions -fno-rtti`) 全严苛标志 (`-Wall -Wextra -Werror -pedantic`)，零警告。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/contracts/twin/job/job_types.h` | 结构体与常量定义（静态断言校验尺寸与对齐） | `f3699b37f79f49ed607168d75da9e6dc2875c7d1aa97198abf9fee671aa3c2ad` |
| `soc-ap/contracts/twin/job/job_engine.h` | 作业引擎对外 API 声明 | `38b373c60c339a677d90ace725f87d66b112894f0dc1694b991db85acfc9e075` |
| `soc-ap/contracts/twin/job/job_engine.c` | 状态机与 G-code 解析核心实现 | `d23efa2c4253c6a1abe75ddf1d9b85c6a52167b4c0583f1e86f328f12626679c` |
| `soc-ap/contracts/twin/job/job_contract.json` | JSON Schema 形式化接口约束定义 (Draft-7) | `a0c796ea25891e606199f32345992975735b96ff176a38c7b9cbb0dfa0ea5852` |
| `soc-ap/contracts/twin/job/test_job_engine.c` | 正反用例完备单元测试套件 | `6ad0907b4add51a69cafce83db7f7492c927be4c277e0adf26fd19998cc09d88` |

---

## 3. 正反用例与验证实测结果

### 3.1 C11 编译与测试日志

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -I soc-ap/contracts/twin/job soc-ap/contracts/twin/job/job_engine.c soc-ap/contracts/twin/job/test_job_engine.c -o /tmp/test_job_engine && /tmp/test_job_engine
```

实测输出：
```
=== Starting TWIN-17 Job Engine Acceptance Tests ===
[PASS] test_initialization_and_homing_guard (未回零禁止启动验证通过)
[PASS] test_pause_resume_cancel (断料挂起/恢复/主动取消验证通过)
[PASS] test_color_mixing_validation (50-50混色成功、非10000非法混色拒绝验证通过)
[PASS] test_gcode_streaming_parser (G1坐标/挤出微米转换、注释过滤、畸形拒绝验证通过)
[PASS] test_estop_interruption (急停瞬时熔断、急停期间指令拒绝、复位验证通过)
[PASS] test_progress_completion (行号推进与100.0%完成状态转换验证通过)
=== ALL TWIN-17 TESTS PASSED SUCCESSFULLY (6/6 Suites) ===
```

### 3.2 C++17 (-fno-exceptions -fno-rtti) 编译与测试日志

```bash
g++ -Wall -Wextra -Werror -pedantic -std=c++17 -fno-exceptions -fno-rtti -I soc-ap/contracts/twin/job soc-ap/contracts/twin/job/job_engine.c soc-ap/contracts/twin/job/test_job_engine.c -o /tmp/test_job_engine_cxx && /tmp/test_job_engine_cxx
```

实测输出：
```
=== Starting TWIN-17 Job Engine Acceptance Tests ===
[PASS] test_initialization_and_homing_guard (未回零禁止启动验证通过)
[PASS] test_pause_resume_cancel (断料挂起/恢复/主动取消验证通过)
[PASS] test_color_mixing_validation (50-50混色成功、非10000非法混色拒绝验证通过)
[PASS] test_gcode_streaming_parser (G1坐标/挤出微米转换、注释过滤、畸形拒绝验证通过)
[PASS] test_estop_interruption (急停瞬时熔断、急停期间指令拒绝、复位验证通过)
[PASS] test_progress_completion (行号推进与100.0%完成状态转换验证通过)
=== ALL TWIN-17 TESTS PASSED SUCCESSFULLY (6/6 Suites) ===
```

### 3.3 形式化 JSON Schema 校验

```bash
python3 -c "import json, jsonschema; jsonschema.Draft7Validator.check_schema(json.load(open('soc-ap/contracts/twin/job/job_contract.json')))"
```
校验结果：Draft-7 Schema 语法与约束 100% 合规。
