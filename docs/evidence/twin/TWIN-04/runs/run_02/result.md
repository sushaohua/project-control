# TWIN-04 VMware构建配置与同构服务生命周期执行与交付报告 (Run 02 - 针对QA审查整改闭环)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-04` (VMware构建配置与同构服务生命周期) |
| **所属工作包** | `TASK-004` (锁定源码和可复现构建) |
| **执行角色** | `INTEGRATOR` (系统集成工程师) |
| **当前轮次** | `run_02` (针对 Run 01 QA 审查发现的定向整改闭环) |
| **前置输入依赖** | `TWIN-02` (双环境可执行通信契约与生成规则, accepted in `runs/run_03/result.md`) |
| **基线 Commit** | `soc-ap: 89ac9d54c2994f635be49faa1b88ea2440b083ff` |
| **交付候选 Commit** | `soc-ap: 6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` (已推送至远端 `origin/main`) |
| **执行状态** | **Completed / Delivered (定向整改 100% 达成，测试全绿，已推送到远端仓库)** |

---

## 1. 针对 Run 01 QA 审查发现的整改闭环落实 (Discrepancy Remediation)

针对独立 QA 审查会话 `01a18ab5-b1e8-7751-8ad8-b7ce15218e37` 出具的审查意见，本次 Run 02 实施了深度整改：

| 发现项编号 | 严重度 | 原始审查意见 | Run 02 修复方案与代码落地 | 对应物证与测试 |
| :--- | :--- | :--- | :--- | :--- |
| **`TWIN-04-QA-01`** | **Blocker** | `supervisor` 运行入口未进入真实 VM 运行模式，`main.cpp` 始终以 `simulation_mode=true` 硬编码初始化，默认服务注册未消费 manifest 的 `binary_path`。 | 1. 在 `supervisor.cpp` 中为全部 10 项服务显式注入与 `services_manifest.json` 100% 对齐的 `/opt/aisoc/bin/...` 二进制路径。<br>2. 在 `main.cpp` 中将 `supervisor_init` 改为按 `do_simulation` 显式传参；无参数运行时进入真实进程探测路径，当目标二进制不存在时退出码为 1 并打印失败告警，杜绝硬编码模拟。 | `test_manifest_binary_binding` 单元测试通过；`aisoc_supervisor` 无参运行实测退出码为 1。 |
| **`TWIN-04-QA-02`** | **Blocker** | 在非模拟模式下，当二进制不存在时静默回退到模拟模式；`fork()` 后立即标记为 `RUNNING` 未核实 `exec()` 是否成功，健康检查缺省返回 OK。 | 1. 废除回退逻辑：若目标二进制不可执行，`spawn_real_process` 立即转入 `SERVICE_STATE_FAILED` 并返回错误。<br>2. 引入 `pipe(pipefd)` 带 `FD_CLOEXEC` 管道机制，若子进程 `execv()` 失败则写入错误码并退出，父进程读到错误立即标记 `SERVICE_STATE_FAILED`；仅当管道读到 EOF (exec成功) 时才转入 `RUNNING`。<br>3. 在 `supervisor_health_check_all` 中通过 `kill(pid, 0)` 实时感知子进程存活状态，若进程死亡立即转入 `SERVICE_STATE_FAILED`。 | 新增 `test_real_mode_missing_binary_rejection` 与 `test_real_mode_valid_binary_spawn` 单元测试，100% 通过。 |
| **`TWIN-04-QA-03`** | **Major** | 服务器沙箱物证仅执行了 `check_task_graph.py`，`build_count=0`，未覆盖实际编译与测试。 | 沙箱运行器 `qa_runner.py` 绑定命令 `bash tools/twin_build/build_vmware.sh --clean --build-dir /tmp/build_vmware --dist-dir /tmp/dist_vmware`，在只读沙箱内完整记录 C++ 编译与 CTest 全量通过日志。 | 沙箱 `runtime.log` 完整记录 CMake/CTest。 |

---

## 2. 交付物清单与最新 SHA256 校验码

| 交付文件路径 | 类型与描述 | SHA256 校验码 | 对应 Commit |
| :--- | :--- | :--- | :--- |
| `soc-ap/cmake/toolchains/vmware.cmake` | VMware x86_64 交叉/本地工具链配置（严格 `-fno-exceptions -fno-rtti`，架构宏与安全防护选项） | `fba14e74e65cf40761d2d638149c51840da2d9546067e78667cdc8f3d93f4a98` | `42ca2b7712225c718b0e5f4b62f9bee3ae29ce39` |
| `soc-ap/runtime/common/service_lifecycle.h` | 统一同构服务生命周期头文件 | `0c11fe8cae24c5a276c5f499ac269f0509226c53979df7b17fe44a9b243e2977` | `42ca2b7712225c718b0e5f4b62f9bee3ae29ce39` |
| `soc-ap/runtime/common/service_lifecycle.cpp` | 统一同构服务生命周期实现 | `a37604e611e94a5328d3e8cfd80a2d96f4a149ab6086232c5902e66db3c6d635` | `42ca2b7712225c718b0e5f4b62f9bee3ae29ce39` |
| `soc-ap/runtime/vmware/supervisor.h` | VMware 服务编排器与进程管理器头文件 | `779267b37460f3f4d2193b587209c0cc677cf4565219f058ab4b238f05caad30` | `42ca2b7712225c718b0e5f4b62f9bee3ae29ce39` |
| `soc-ap/runtime/vmware/supervisor.cpp` | VMware 服务编排器实现（支持真实 fork/exec 管道探测、无回退失败捕获、kill(pid,0)与waitpid(WNOHANG)健康巡检） | `45084a25d6f831ba33b197da85b4bd2966837ff582fb869536285357f8eff1ec` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/runtime/vmware/main.cpp` | VMware Supervisor 命令行入口（支持真实模式、`--dry-run`、`--simulation` 显式分支） | `64bb9e132a8119e05be74a0a8deb7f7b3ce54d6403fc3444c3f0a5c98ce0bffd` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/runtime/build/CMakeLists.txt` | 模块构建与测试配置 | `54af5fbb53b127515f0bfaade74622ab826f06a40e562b41f165cbd28c251b82` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/runtime/build/tests/test_service_lifecycle.cpp` | 状态机流转与生命周期钩子单元测试 | `ddc94c4c42208cb51668aa9889a87a5ca36fcca830c1bd46c2b4974fd597a00e` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/runtime/build/tests/test_backoff.cpp` | 有界指数退避算法、重试耗尽与重置单元测试 | `e70bde70ea001809a428fda7e846f021fe38f38162d0bf066615c1e7d6cdf3dc` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/runtime/build/tests/test_supervisor_topology.cpp` | 拓扑启动顺序、环死锁检测、逆向停机、manifest二进制1:1精确绑定与真实进程探测测试 | `f14a8e10ba0d5d1af082746344e9ed87289ae17c7d1574337efff0515587b15b` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/config/runtime/common/services_manifest.json` | 跨环境统一服务拓扑清单 | `79c529657d3550c59305b039ed2a0e70ab013e7676e4d944c513fc925a840204` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/config/runtime/vmware/services_manifest.json` | VMware 环境专用服务拓扑清单 | `aface080d154ea97017c207e08ff41f810a4b3115933f6c2ec9e91e35c950af1` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |
| `soc-ap/tools/twin_build/build_vmware.sh` | VMware 阶段一键构建、校验、测试与打包发布脚本（生产级纯真实模式 systemd 单元） | `0c820bb0d2077507253b5c420571470c69164c2748dde555c60eed062d9695d5` | `6a63b7879795beed0f9e1e8dc3e52c935fe2a54f` |

---

## 3. 门禁规范符合性自检 (Coding Standard Compliance)

依据《代码编写规范与硬性门禁》（`c_cpp_coding_standard.md`）：
- **函数行数**：所有自研新增/修改非结构体函数均严格控制在 50 行以内（最大函数 `spawn_real_process` 为 48 行）。
- **函数参数**：所有自研新增/修改非结构体函数入参严禁超 4 个（`set_entry_binary` 为 2 参，`spawn_real_process` 为 1 参）。
- **内存安全**：零动态堆内存分配（严格禁止 `malloc`/`free`/`new`/`delete`），统一使用静态结构体容器与栈上局部缓冲。
- **卫语句与防御**：所有函数入口首行强制进行非空指针校验。
- **编译器防护**：`-fno-exceptions -fno-rtti`，`-Wall -Wextra -Werror` 全绿通过。
