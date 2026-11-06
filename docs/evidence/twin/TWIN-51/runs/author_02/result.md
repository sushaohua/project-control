# TWIN-51 (`ISS-20261105-001`) 补充现场核查与复验报告 (`author_02`, `INTEGRATOR`)

## 1. 任务与收件绑定
- **关联任务与问题单**：`TWIN-51` / `ISS-20261105-001` / `DEM-20261105-001`
- **触发收件单**：[`project-control/docs/work_intake/submissions/20261106_soc_ap_backoff_build_failure_followup.md`](file:///home/sushaohua/workspace/ai_soc_project/project-control/docs/work_intake/submissions/20261106_soc_ap_backoff_build_failure_followup.md)
- **执行角色**：`INTEGRATOR` (`07a1f6dc-f47c-45e5-bf00-37ec14e2dfda`, `run_id: author_02`)
- **边界声明**：本轮核查严格限定在当前受管工作区 `/home/sushaohua/workspace/ai_soc_project` 内执行，**零访问外部目录 `/home/sushaohua/testaaa/`**；完整保留 `runs/author_01/` 与 `runs/qa_02/` 历史证据不变。
- **已读规则与来源登记 (`read_sources`)**：
  - `soc-ap/AGENTS.md` + `soc-ap/.agents/rules/repository.md` + `soc-ap/.agents/rules/shared/SOURCE.json` (`source_commit: 17e0887da07ceb3b017623b791b6a6999e837c79`)
  - `project-control/.agents/rules/repository_rule_sources.json`
  - `project-control/.agents/rules/repository_rule_boundaries.md`
  - `project-control/.agents/rules/c_cpp_coding_standard.md`
  - `project-control/.agents/rules/code_documentation_standard.md`
  - `project-control/docs/architecture/soc_ap_build_and_startup_issues_arch_breakdown_20261105.md` (`revision: 4`)
  - `project-control/docs/work_intake/submissions/20261106_soc_ap_backoff_build_failure_followup.md`

---

## 2. 精确行号、版本祖先关系与运行期逻辑核查结论

### 2.1 Git 提交祖先关系与远端服务器同步核实
在 `/home/sushaohua/workspace/ai_soc_project/soc-ap` 执行 `git rev-parse HEAD`、`git ls-remote origin refs/heads/main` 与 `git merge-base --is-ancestor`：
- **修复前基线 (`base_commit`)**：`7c1f35091850b39f4ba3ff9b242043a62f3e5b74`
- **`TWIN-51` 修复提交 (`candidate_commit`)**：`75f8a1a670edabb21c8d3dfc79243e06f73099af`（`fix(runtime): zero-initialize backoff structs in test_backoff.cpp for GCC 15 (TWIN-51)`）
- **当前本地 `HEAD` 与远端 `origin/main`**：`7184edfc796923e2f2c6e3e57ef3a9f791164b51`
- **祖先包含关系**：
  - `git merge-base --is-ancestor 7c1f35091850b39f4ba3ff9b242043a62f3e5b74 75f8a1a670edabb21c8d3dfc79243e06f73099af` ➔ `Exit 0`（是祖先）
  - `git merge-base --is-ancestor 75f8a1a670edabb21c8d3dfc79243e06f73099af 7184edfc796923e2f2c6e3e57ef3a9f791164b51` ➔ `Exit 0`（是祖先，且已推送至远端 `origin/main`）

### 2.2 用户补充报错行号与三个受控版本的精确逐行比对

| 核对位置 | 用户补充日志 (`/home/sushaohua/testaaa/.../soc-ap`) | 修复前旧基线 `7c1f3509...` | `TWIN-51` 修复提交 `75f8a1a6...` | 当前 `soc-ap@main` (`7184edfc...`) |
| :--- | :--- | :--- | :--- | :--- |
| **`test_backoff.cpp` 中 `#include <assert.h>` 行号** | **Line 9** (`In file included from .../test_backoff.cpp:9`) | **Line 9** (`#include <assert.h>`) | Line 11 (`#undef NDEBUG` 在 Line 10) | Line 11 (`#undef NDEBUG` 在 Line 10) |
| **`test_backoff.cpp` 中 `cfg` 声明行号与内容** | **Line 14:22** (`backoff_config_t cfg;`) | **Line 14:22** (`backoff_config_t cfg;`) | Line 21 (`backoff_config_t cfg = {0U, 0U, 0U, 0U, 0U};`) | Line 21 (`backoff_config_t cfg = {0U, 0U, 0U, 0U, 0U};`) |
| **`test_backoff.cpp` 中 `backoff_init(NULL, &cfg)` 行号** | **Line 18:24** (`assert(backoff_init(NULL, &cfg) == ...);`) | **Line 18:24** (`assert(backoff_init(NULL, &cfg) == ...);`) | Line 26 (`assert(backoff_init(NULL, &cfg) == ...);`) | Line 26 (`assert(backoff_init(NULL, &cfg) == ...);`) |
| **`service_lifecycle.h` 中 `backoff_init` 声明行号** | **Line 146:20** (`lifecycle_status_t backoff_init(...)`) | **Line 146:20** (`lifecycle_status_t backoff_init(...)`) | **Line 146:20** (`lifecycle_status_t backoff_init(...)`) | Line 159:20（`19534a9` 新增 `service_lifecycle_init_param_t` 后下移 13 行） |

- **定性结论（旧检出未同步，非受控源码回归或漏改）**：
  1. 用户补充日志中的 4 处精确行号/列号（`test_backoff.cpp:9`、`test_backoff.cpp:14:22`、`test_backoff.cpp:18:24`、`service_lifecycle.h:146:20`）与 `TWIN-51` 修复前的旧提交 `7c1f35091850b39f4ba3ff9b242043a62f3e5b74` **100% 逐行逐列一致**。
  2. 这证明用户外部现场目录 `/home/sushaohua/testaaa/ai_soc_project/soc-ap` 的检出版本停留在 `7c1f35091850b39f4ba3ff9b242043a62f3e5b74`（或更早版本），尚未从远端服务器拉取包含 `TWIN-51` 修复提交 `75f8a1a670edabb21c8d3dfc79243e06f73099af` 的最新 `origin/main` (`7184edfc796923e2f2c6e3e57ef3a9f791164b51`)。
  3. 当前受版本管理的 `soc-ap@main` (`7184edfc796923e2f2c6e3e57ef3a9f791164b51`) 中，`test_backoff.cpp` 的全部 3 个测试函数（`test_backoff_null_guards` Line 20-21、`test_backoff_progression` Line 42/49、`test_backoff_reset` Line 92/99）中的 `st` 与 `cfg` 均已显式零初始化，无任何遗漏或回归，无需二次修改受控源码。

### 2.3 `backoff_init(NULL, &cfg)` 运行期逻辑核实
- 检查 [`soc-ap/runtime/common/service_lifecycle.cpp#L64-L70`](file:///home/sushaohua/workspace/ai_soc_project/soc-ap/runtime/common/service_lifecycle.cpp#L64-L70)：
  ```cpp
  lifecycle_status_t backoff_init(backoff_state_t* state, const backoff_config_t* config)
  {
      if (state == NULL || config == NULL) {
          return LIFECYCLE_ERR_INVALID_ARGUMENT;
      }
      if (config->initial_interval_ms == 0U || config->max_interval_ms < config->initial_interval_ms) {
          return LIFECYCLE_ERR_INVALID_ARGUMENT;
      }
  ```
- **运行期行为确认**：当传入 `backoff_init(NULL, &cfg)` 时，函数入口第一行卫语句 `if (state == NULL || config == NULL)` 立即短路返回 `LIFECYCLE_ERR_INVALID_ARGUMENT`，在运行期**绝不会解引用或读取 `config` (`&cfg`)**。编译器报错纯粹是因为跨编译单元调用时，将未初始化局部变量地址传给 `const backoff_config_t*` 形参触发了 `-Wmaybe-uninitialized` 静态启发式诊断。

---

## 3. 当前 `soc-ap@7184edfc796923e2f2c6e3e57ef3a9f791164b51` 独立复验记录

- **验证范围声明**：本次复验针对 `soc-ap` 的 `runtime/build` 单元测试与监管器组件（`test_backoff`、`test_service_lifecycle`、`test_supervisor_topology` 及 `aisoc_supervisor`），不代表全栈/物理 HIL 全部通过。
- **候选 Commit**：`soc-ap@7184edfc796923e2f2c6e3e57ef3a9f791164b51`
- **实际编译器版本**：`g++ (Ubuntu 9.4.0-1ubuntu1~20.04.2) 9.4.0`
- **复验命令**：
  ```bash
  rm -rf /tmp/twin51_followup_verify && mkdir -p /tmp/twin51_followup_verify && \
  (! grep -En "backoff_(state|config)_t[[:space:]]+(st|cfg)[[:space:]]*;" runtime/build/tests/test_backoff.cpp) && \
  g++ -std=c++17 -O2 -Wall -Wextra -Werror -Wpedantic -Wmaybe-uninitialized -fno-exceptions -fno-rtti \
    -Iruntime/common runtime/build/tests/test_backoff.cpp runtime/common/service_lifecycle.cpp \
    -o /tmp/twin51_followup_verify/test_backoff_strict && \
  /tmp/twin51_followup_verify/test_backoff_strict && \
  cmake -S runtime/build -B /tmp/twin51_followup_verify/build -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE="-O2" && \
  cmake --build /tmp/twin51_followup_verify/build --parallel && \
  ctest --test-dir /tmp/twin51_followup_verify/build --output-on-failure -V && \
  rm -rf /tmp/twin51_followup_verify
  ```
- **实测客观输出（`Exit Code: 0`，零告警）**：
  ```text
  [PASS] No uninitialized st/cfg declarations in test_backoff.cpp
  Running Bounded Backoff Unit Tests...
  PASS: test_backoff_null_guards
  PASS: test_backoff_progression
  PASS: test_backoff_reset
  ALL Bounded Backoff Unit Tests PASSED!
  ...
  1/3 Test #1: test_service_lifecycle ...........   Passed    0.00 sec
  2/3 Test #2: test_backoff .....................   Passed    0.00 sec
  3/3 Test #3: test_supervisor_topology .........   Passed    0.04 sec
  100% tests passed, 0 tests failed out of 3
  ```

---

## 4. 外部现场目录 (`/home/sushaohua/testaaa/ai_soc_project/soc-ap`) 同步更新建议

用户只需在外部克隆目录 `/home/sushaohua/testaaa/ai_soc_project/soc-ap` 中拉取远端 `origin/main` 最新提交（含 `75f8a1a670edabb21c8d3dfc79243e06f73099af` 及后续至 `7184edfc796923e2f2c6e3e57ef3a9f791164b51` 的全部修复）并清理旧构建缓存后重新构建即可消除该阻断：

```bash
cd /home/sushaohua/testaaa/ai_soc_project/soc-ap
git fetch origin main
git checkout main
git pull --ff-only origin main
git rev-parse HEAD   # 应输出 7184edfc796923e2f2c6e3e57ef3a9f791164b51 或更新提交
bash tools/twin_build/build_vmware.sh
```
