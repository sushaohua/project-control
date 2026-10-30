# TWIN-04 VMware构建配置与同构服务生命周期执行与交付报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-04` (VMware构建配置与同构服务生命周期) |
| **所属工作包** | `TASK-004` (锁定源码和可复现构建) |
| **执行角色** | `INTEGRATOR` (系统集成工程师) |
| **当前轮次** | `run_01` |
| **前置输入依赖** | `TWIN-02` (双环境可执行通信契约与生成规则, accepted in `runs/run_03/result.md`) |
| **基线 Commit** | `soc-ap: 532caecf3a146802969a49e73081400c2b32b25e` |
| **交付候选 Commit** | `soc-ap: 89ac9d54c2994f635be49faa1b88ea2440b083ff` (已推送至远端 `origin/main`) |
| **执行状态** | **Completed / Delivered (100% 门禁通过，测试全绿，已推送到远端仓库)** |

---

## 1. 交付物清单与校验和 (Deliverables & SHA256)

所有产物严格限定在 `TWIN-04` 授权的白名单路径内：

| 交付文件路径 | 类型与描述 | SHA256 校验码 | 对应 soc-ap Commit |
| :--- | :--- | :--- | :--- |
| `soc-ap/cmake/toolchains/vmware.cmake` | VMware x86_64 交叉/本地工具链配置（严格 `-fno-exceptions -fno-rtti`，架构宏与安全防护选项） | `fba14e74e65cf40761d2d638149c51840da2d9546067e78667cdc8f3d93f4a98` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/common/service_lifecycle.h` | 统一同构服务生命周期头文件（统一度量 7 种状态、生命周期操作表、有界退避重试算法、健康评估） | `0c11fe8cae24c5a276c5f499ac269f0509226c53979df7b17fe44a9b243e2977` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/common/service_lifecycle.cpp` | 统一同构服务生命周期实现（零动态堆分配、防御性卫语句、函数 $\le 50$ 行、入参 $\le 4$ 个） | `a37604e611e94a5328d3e8cfd80a2d96f4a149ab6086232c5902e66db3c6d635` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/vmware/supervisor.h` | VMware 服务编排器与进程管理器头文件（管理 4 首切片活跃服务与 6 延后服务） | `779267b37460f3f4d2193b587209c0cc677cf4565219f058ab4b238f05caad30` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/vmware/supervisor.cpp` | VMware 服务编排器实现（拓扑排序启动、逆向拓扑优雅停机、崩溃监听、退避重启调度） | `0ec194813647e69cead8d45cd7c28cf057b4b6487ad23e8ab217f43c54574f08` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/vmware/main.cpp` | VMware Supervisor 命令行入口（支持 `--dry-run`、`--simulation` 等） | `adfe411a69fa035e3e8e72bd8ced1e5d4b4305680b9dc03ab74106425a7a46a0` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/build/CMakeLists.txt` | 独立模块构建与测试配置（生成 `aisoc_runtime_common`、`aisoc_supervisor` 及单元测试套件） | `54af5fbb53b127515f0bfaade74622ab826f06a40e562b41f165cbd28c251b82` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/build/tests/test_service_lifecycle.cpp` | 状态机流转与生命周期钩子单元测试 | `ddc94c4c42208cb51668aa9889a87a5ca36fcca830c1bd46c2b4974fd597a00e` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/build/tests/test_backoff.cpp` | 有界指数退避算法、重试耗尽与重置单元测试 | `e70bde70ea001809a428fda7e846f021fe38f38162d0bf066615c1e7d6cdf3dc` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/runtime/build/tests/test_supervisor_topology.cpp` | 拓扑启动顺序、依赖循环死锁检测、逆向停机测试 | `d241344d188c5d9ea4a07574d272824670a3cc36cdb64c47f81ba20d5f797093` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/config/runtime/common/services_manifest.json` | 跨环境统一服务拓扑清单（10 个服务，严格符合 `services_manifest_schema.json`） | `79c529657d3550c59305b039ed2a0e70ab013e7676e4d944c513fc925a840204` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/config/runtime/vmware/services_manifest.json` | VMware 环境专用服务拓扑清单（严格符合 `services_manifest_schema.json`） | `aface080d154ea97017c207e08ff41f810a4b3115933f6c2ec9e91e35c950af1` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| `soc-ap/tools/twin_build/build_vmware.sh` | VMware 阶段一键构建、校验、测试与打包发布脚本 | `9d38842939b425742b2537998afb1a260fca94cc149956efe131cf96b8fc1c9a` | `89ac9d54c2994f635be49faa1b88ea2440b083ff` |

---

## 2. 契约符合性自检 (Contract Alignment)

### 2.1 JSON Schema 验证实测
使用 Python `jsonschema.Draft7Validator` 对比权威契约原件 `soc-ap/contracts/twin/services_manifest_schema.json`：
- `soc-ap/config/runtime/common/services_manifest.json`：**PASS (0 错误)**
- `soc-ap/config/runtime/vmware/services_manifest.json`：**PASS (0 错误)**
- 强制包含全部 10 个系统服务（4 个 `first_slice_active`，6 个 `deferred`），字段与 IPC 契约 100% 对齐。

### 2.2 服务生命周期与状态定义对齐
- 统一度量 7 种标准状态：`UNINITIALIZED`, `STARTING`, `RUNNING`, `DEGRADED`, `STOPPING`, `STOPPED`, `FAILED`。
- 标准四大接口：`service_init`, `service_start`, `service_health_check`, `service_stop`。
- 守护进程有界指数退避算法：配置包含 `initial_interval_ms`, `max_interval_ms`, `multiplier_num`, `multiplier_den`, `max_retries`，实现防抖、有界退避与重试上限耗尽保护。

### 2.3 拓扑编排顺序验证
4 个活跃切片服务拓扑启动顺序经 Kahn 算法自动解析并由测试严格校验：
1. `forward-service` (无 AP 内部依赖，直通 MCU UART)
2. `device-manager` (依赖 `forward-service`)
3. `ui-gateway` (依赖 `device-manager`, `forward-service`)
4. `browser-hmi` (依赖 `ui-gateway`)
逆向优雅停机顺序：`browser-hmi` $\to$ `ui-gateway` $\to$ `device-manager` $\to$ `forward-service`。

---

## 3. 硬性代码门禁与规范核查 (Coding Standards Compliance)

根据 `project-control/.agents/rules/c_cpp_coding_standard.md` 进行严格自动化筛查：

| 门禁核查项 | 标准规范要求 | 实测结果 | 结论 |
| :--- | :--- | :--- | :--- |
| **函数规模门禁** | 自研函数行数严格 $\le 50$ 行 | 全量自研函数行数最大为 42 行 (`resolve_kahn_topology`) | **PASS (0 超标)** |
| **入参个数门禁** | 自研非结构体函数参数严格 $\le 4$ 个 | 全量函数参数个数最大为 4 个（复杂入参已封装结构体） | **PASS (0 超标)** |
| **动态内存分配** | 嵌入式 C++ 零堆动态分配（严禁 new/delete/malloc/free 及动态 STL） | 扫描源码中 `malloc`, `free`, `new`, `delete`, `std::vector`, `std::string` 等关键字 | **PASS (0 违规，纯静态定长结构)** |
| **防御性空指针校验** | 对外公开函数入口首行强制进行空指针防御校验 (Guard Clause) | 所有公开接口均在第一行检查非空指针，非法立即返回 `LIFECYCLE_ERR_INVALID_ARGUMENT` | **PASS (100% 覆盖)** |
| **编译器选项与异常** | 强制 `-fno-exceptions -fno-rtti`，强类型返回值与错误码 | 工具链与构建文件全量配置 `-fno-exceptions -fno-rtti`，无任何 throw/catch | **PASS** |

---

## 4. 自动化测试与构建证据 (Build & Test Execution Evidence)

执行一键构建脚本 `bash soc-ap/tools/twin_build/build_vmware.sh --clean`：

```text
=================================================================
AISOC VMware Twin Build Pipeline
  Workspace:   /home/sushaohua/workspace/ai_soc_project/soc-ap
  Toolchain:   /home/sushaohua/workspace/ai_soc_project/soc-ap/cmake/toolchains/vmware.cmake
  Build Dir:   /home/sushaohua/workspace/ai_soc_project/soc-ap/build/vmware
  Dist Dir:    /home/sushaohua/workspace/ai_soc_project/soc-ap/dist/vmware_twin
  CMake:       /home/sushaohua/.local/bin/cmake
=================================================================
--> Cleaning build and dist directories...
--> Verifying runtime service manifests against schema...
  [OK] Schema validated: soc-ap/config/runtime/common/services_manifest.json
  [OK] Schema validated: soc-ap/config/runtime/vmware/services_manifest.json
--> Configuring runtime with VMware x86_64 toolchain...
-- [AISOC Toolchain] Configured for VMware x86_64 (Linux, C++17, no-exceptions, no-rtti)
-- The C compiler identification is GNU 9.4.0
-- The CXX compiler identification is GNU 9.4.0
-- Configuring done (1.0s)
-- Generating done (0.0s)
-- Build files have been written to: soc-ap/build/vmware
--> Compiling aisoc_runtime and supervisor binaries...
[100%] Built target test_service_lifecycle
[100%] Built target test_backoff
[100%] Built target test_supervisor_topology
[100%] Built target aisoc_supervisor
--> Running CTest suite...
Test project soc-ap/build/vmware
    Start 1: test_service_lifecycle
1/3 Test #1: test_service_lifecycle ...........   Passed    0.00 sec
    Start 2: test_backoff
2/3 Test #2: test_backoff .....................   Passed    0.00 sec
    Start 3: test_supervisor_topology
3/3 Test #3: test_supervisor_topology .........   Passed    0.00 sec

100% tests passed out of 3

Total Test time (real) =   0.00 sec
--> Running supervisor CLI dry-run verification...
=================================================================
AISOC VMware Twin Services Topology (Total: 10, Active: 4)
=================================================================
[0] forward-service    (Order:  0) State: UNINITIALIZED Active: YES
[1] device-manager     (Order:  1) State: UNINITIALIZED Active: YES
    Dependencies: forward-service
[2] ui-gateway         (Order:  2) State: UNINITIALIZED Active: YES
    Dependencies: device-manager, forward-service
[3] browser-hmi        (Order:  3) State: UNINITIALIZED Active: YES
    Dependencies: ui-gateway
[4] job-engine         (Order:  0) State: UNINITIALIZED Active: NO
    Dependencies: device-manager
[5] storage-service    (Order:  0) State: UNINITIALIZED Active: NO
[6] cloud-gateway      (Order:  0) State: UNINITIALIZED Active: NO
    Dependencies: device-manager
[7] camera-service     (Order:  0) State: UNINITIALIZED Active: NO
[8] print-guard        (Order:  0) State: UNINITIALIZED Active: NO
    Dependencies: camera-service, device-manager
[9] system-manager     (Order:  0) State: UNINITIALIZED Active: NO
-----------------------------------------------------------------
Topological Startup Order (Active Services):
  Step 1: Start forward-service (Role: UART Serial Gateway)
  Step 2: Start device-manager (Role: Device State Machine)
  Step 3: Start ui-gateway (Role: HTTP/SSE Gateway)
  Step 4: Start browser-hmi (Role: Browser Web HMI)
Reverse Topological Shutdown Order:
  Step 1: Stop  browser-hmi
  Step 2: Stop  ui-gateway
  Step 3: Stop  device-manager
  Step 4: Stop  forward-service
=================================================================
Dry run validation complete. Exiting.
--> Running supervisor simulation mode verification...
--> Starting all active services in topological order...
--> All active services successfully started (RUNNING).
--> Performing unified health check on all services...
--> All services reported HEALTH_STATUS_OK.
--> Stopping all services in reverse topological order...
--> All services stopped gracefully (STOPPED).
=================================================================
AISOC VMware Twin Build Pipeline Completed Successfully!
=================================================================
```

---

## 5. 交接与提请审查声明 (Handoff Statement)

本轮次（`run_01`）由系统集成工程师（`INTEGRATOR`）完整实现并交付 `TWIN-04` 所属全部产物。候选代码已合并至 `soc-ap` 仓库 `origin/main`（Commit: `89ac9d54c2994f635be49faa1b88ea2440b083ff`）。本报告与代码已通过前置门禁自检，现提请协调员（`COORD`）安排独立审阅者（`QA`、`ARCH`）开展双盲审查与验证。
