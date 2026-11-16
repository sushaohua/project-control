# printer-soc 专用 AGENTS、rules 与 skills 实施方案

状态：**已按用户批准的 v1.0 完成七文件实施与约定核验，并完成第 12 节本地归档**。用户随后明确要求“推送远端”，按第 13 节对齐并同步既有候选；不新增业务实现，不修改公共规则或原有软链接，不执行业务构建、独立 QA 或 HIL。

## 修订历史

| 版本 | 修订时间（UTC+8） | 修订人 Agent/Author | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-11-16 16:46:19 | AI (Codex) | 根据十席职责、独立代码仓和实际 C++/C 源码，提出沿用五个文件、增加一份规则和一个技能的最小方案；明确输入、边界、语言适用性与验收 | 待用户批准；尚未实施 |
| v1.1 | 2026-11-16 17:12:41 | AI (Codex) | 登记用户对 v1.0 的明确批准，复核三仓基线、五个现有文件与两条软链接，开始七文件有界实施 | 已批准执行；核验完成后原地登记实际结果 |
| v1.2 | 2026-11-16 17:24:10 | AI (Codex) | 完成五文件完善及两文件新增，落实 C++17/C ABI/资源并发与四技能交接；格式、元数据、双入口引用、命令、范围和预算核验通过，登记实际结果 | 本批治理实施完成；不含业务构建、独立 QA/HIL 或 Git 提交 |
| v1.3 | 2026-11-16 17:36:37 | AI (Codex) | 按用户“先提交本轮治理成果”登记 agents 七文件与 PC 方案的本地提交，并授权同步根 workspace.json 中对应两仓提交指针；保持原验收范围 | 本地归档及根锁同步已批准；不含推送、业务准出或额外工程修改 |
| v1.4 | 2026-11-16 17:51:16 | AI (Codex) | 按用户“推送远端”登记明确 URL/分支、依赖候选、agents 双推、fetch/rebase 与冲突停止；远端实查 MCU/双 Boot 已达锁，应用/测试候选仍需同步，根锁最后发布 | 远端同步已批准；不含新业务实现或 SW/HIL 准出 |

## 1. 背景、目标与完成条件

用户要求为 `printer-soc` 制定专用 `AGENTS.md`、rules 和 skills，符合整体架构、角色矩阵及代码独立仓的特点；以 C++ 为主要开发语言，同时纳入适用的 C 语言要求。用户再次明确“先生成方案，批准后，再执行”，本轮不提前启用任何新规则。

本方案的目标是让接手应用仓的 Agent 可以准确回答：本仓负责什么、谁能写哪些路径、哪些语言约束适用、当前能力到哪里、怎样选择真实构建和验收入口，以及何时须交给其他角色。

完成条件：

1. 从 `printer-soc/AGENTS.md` 能找到本仓两份规则、四个按需技能，以及适用的 PC 公共规则；入口简短，细则按需读取。
2. C++17 为现有主要基线；C 源码和 C ABI 边界有明确适用要求，不能把所有 `.h` 当作 C 头文件，也不把应用仓整套改为裸机 C 风格。
3. DM、Forward、Gateway、本地 Helix、文件资产及平台职责清晰，当前实现与目标能力分别描述，不增加重复业务状态或虚构服务。
4. 专属内容只存于 `agents/printer-soc/`；业务仓继续保持独立 Git 和现有软链接，PC 公共规范保持单一真源。
5. 七个目标文件通过格式、引用、命令签名和边界核对；不修改业务源码、SDK、公共门禁或其他仓的活动规则，不签发 SW/HIL 通过。

不在本批范围：实现 Helix 后台、完整文件打印、遥测修复、C/C++ 全库整改、迁移 C 源码、变更编译选项、增加 CI/门禁程序、改动协议、重做十席 RACI、建立新看板或审批阶段。

## 2. 已核实的基线与现状

| 对象 | 本次只读核验结果 |
| --- | --- |
| `printer-soc` | `main`，`d9278c5269af69d1a8b5159653ce68186e59cf1c`，工作树干净 |
| `agents` 本项目范围 | `main`，锁定 `6ca205e7a39384b2be32e244757b9701b23866a8`，本项目七目录无待改动 |
| `project-control` | `main`，`965c15543dc2ff426204d80d00b3f903378cc6ce`，本方案创建前干净 |
| 根工作区 | 当前锁文件已登记 `printer-soc` 与独立 C308L Repo 客户端；本方案不修改根文件或锁 |
| 现有托管入口 | `printer-soc/AGENTS.md → ../agents/printer-soc/AGENTS.md`；`printer-soc/.agents → ../agents/printer-soc/.agents` |
| 现有专属内容 | 入口、`rules/repository.md`、三个 `SKILL.md`，共五个文件、74 行；不是从零新建 |
| 已跟踪语言资产 | 91 个 `.cpp`、9 个 `.c`、59 个 `.h`、2 个 `.hpp`；不含展开的第三方源码 |
| 编译定义 | 根及三服务使用 `LANGUAGES CXX`、C++17；未发现统一的 `C_STANDARD`。不能由这份构建图推断九个 C 文件都被编译或均为生产调用链 |
| 本地 AST | `graphify-out/graph.json` 的 `built_at_commit` 与应用 HEAD 一致；2647 节点、8080 边。已查询下表相关符号与调用边 |

### 2.1 调用链与规则设计的物理依据

以下路径均相对 `printer-soc/`。标为源码核实的关系没有冒称 AST 已提取。

| 接缝 | 真实文件、符号或签名 | 取证与方案影响 |
| --- | --- | --- |
| 生产 Forward 启动 | `services/forward/forward_service.cpp:forward_service_start(forward_service_state_t*)` 调用 `fwd_io_start`、`fwd_uart_open`、`init_dds_entities` | 前两条由源码核实；到 `init_dds_entities()` 的边为 AST `calls/EXTRACTED`。规则要求沿生产链排障，不能只修 CLI |
| 唯一 UART 所有者 | `forward_uart.cpp:fwd_uart_open` 在非 owner 时进入 `fwd_io_control(..., OPEN)`；实际打开交 `fwd_comm_serial_open`；`forward_io.cpp` 维护有界队列及 owner 线程 | 源码核实。UI、DM、诊断工具不得并行抢 UART；DDS domain 不代表物理隔离 |
| DM 与状态通道 | `services/device_manager/device_manager_service.cpp:device_manager_start(device_manager_state_t*) → init_dds_entities()` | AST `calls/EXTRACTED`。结合 `documents/architecture.md` 区分设备准入与 Forward 执行职责 |
| ARM 构建链 | `tools/build_c308l_services.py:main() → unpack()/build_all()/package_runtime()` | 三条均为 AST `calls/EXTRACTED`；源码核实 SDK 外输出、归档/补丁校验及目标依赖前缀 |
| 应用打包 | `tools/package_c308l_product.py:verify_source(source)`、`main()`；CLI 为 `--runtime/--output/[--helix]` | 源码核实。安装树、应用包、入镜与板端运行分别报告；不把打包成功当系统镜像完成 |
| C++ 协议接口 | `core/forward/minimc/codec.h` 定义 `namespace minimc`、`Bytes`、`Status` 与编解码 API；`parser.h` 定义有界接收上下文 | 源码核实。这两个 `.h` 是 C++ 接口，不能套 `extern "C"` 或要求 C 编译器直接包含 |
| C ABI 外观 | `middleware/{dbus,dds}/include/aisoc_{dbus,dds}.h`、`services/forward/forward_service.h` 含 C++ 兼容守卫 | 源码核实。语言链接声明不等于已经证明整套头文件可被任意 C 编译器独立编译，修改接口时仍须实际验收 |
| 语言/中间件边界 | `middleware/dbus/CMakeLists.txt` 明确 `-fno-exceptions/-fno-rtti`；DDS 目标未设置同一组选项，使用第三方 C++ 实体 | 不新增全仓统一禁异常开关；遵守 PC 第 1.4 节限定的第三方适配例外，不能扩张到任意业务代码 |
| 存量接口差异 | `minimc::parser_feed_byte(StreamParser*, uint8_t, uint32_t, FrameView*, bool*) noexcept` 当前为五入参 | 登记事实，本轮不改签名，不擅自认定已获冻结 ABI 豁免。以后涉及该接口时，由相应方案说明兼容与收敛办法；新增自研接口仍执行四入参要求 |

现有九个 C 文件分布于 `contracts/twin/job/`、`core/net/mdns/`、`core/state/hms/` 及相关测试。其存在不证明完整文件打印已实现，旧测试内的内存状态或时间阈值也不能替代生产接口和真实硬件事实。

### 2.2 现有内容需要补齐的地方

- 已有入口及三个技能方向正确，但缺少 C++17、纯 C 接口、资源所有权和各层异常/堆限制的明确适用说明。
- `repository.md` 对 DM/Forward 的介绍较简略，需要对齐应用仓已确认的“控制管理 / 打印执行”双层分工，保留完整打印与 Helix 后台尚未实现的事实。
- 现有技能没有统一明确命令的工作目录；从业务仓目录执行工作区根相对路径会指向错误位置。所有跨仓示例统一标明“在工作区根执行”。
- `sync_contracts.py` 当前无 `--check` 参数，只有指定 `--render-header` 才写生成头；规则中不得因名称猜测 CLI 行为。`fast_gate.py` 对源代码的检查不等于已验证 Markdown 的规则语义。
- 独立候选不能只依赖 Git 忽略的本地资料。当前未检出 `printer-soc/docs` 软链接，本批不创建它；产品设计以跟代码提交的 `documents/` 为依据。

## 3. 参考来源与适配取舍

只参考本项目所属目录：`agents/printer-soc`、`c308l-sdk`、`mcu-p3`、`test_harness`、`bootloadermc`、`bootloaderth` 和历史只读 `soc-ap`；未读取 agents 内其他项目。重点阅读下列正文，其余仅核对文件清单。

| 已读来源 | 借鉴内容 | 本仓适配 |
| --- | --- | --- |
| `agents/mcu-p3/.agents/rules/api_modular_design.md`、`c_cpp_coding_standard.md` | 接口与实现对应、自包含、const、错误返回、明确数据流、规模约束及存量最小修改 | 引用 PC 已集中维护的对应规范；增加应用层语言适用说明，不复制 MCU 规则副本 |
| `agents/c308l-sdk/{AGENTS.md,.agents/rules/repository.md,.agents/skills/sdk-platform-integration/SKILL.md}` | Repo 逐项目 Owner、锁、目标 ABI、隔离构建、安装与设备事实区分 | 明确 ENG-AP 与 ENG-PLATFORM 接缝，避免应用任务取得 SDK 根写权 |
| `agents/test_harness/{AGENTS.md,.agents/rules/repository.md}` | 准确候选、独立预期、证据来源、软件与 HIL 分开 | 应用作者提供自检，不替 INTEGRATOR 或独立 QA 准出，不增加重复签字 |
| `agents/soc-ap/{AGENTS.md,.agents/rules/repository.md}` | 简短入口、公共规则单源、真实通信与最小修改 | 历史只读参考；不带入旧仓名、browser_hmi 或 VMware 构建前提 |
| `agents/bootloadermc/AGENTS.md` | 取证、审批、冲突熔断和硬件授权 | 不移植 Windows venv、探针、Flash/VTOR 和 MCU 时钟规则到 Linux 应用构建 |

采用“完善现有五文件 + 增加一个语言补充规则及一个构建交付技能”。将全部内容继续堆入 `repository.md` 虽少一个入口，但会混合职责与语言细节；按每个服务拆一套规则和技能则会重复。两份规则、四个按需技能足以覆盖当前应用工作，无须新增角色或流程层级。

## 4. 权威关系、独立仓与角色边界

### 4.1 三层来源保持现状

1. **PC 公共规则**：`project-control/.agents/rules/` 继续是公共职责、C/C++ 底线、中文注释、QA 与交付的权威原件。本批不修改或复制它们。
2. **应用事实与产品设计**：`printer-soc/documents/{architecture,status,build_and_deploy,dependency_build_release,external_inputs,platform_integration_design}.md`、真实源码/CMake，以及 `boards/c308l-aw419/` 和依赖锁。规则引用其职责和输入，不另写一份竞争性业务架构。
3. **专属执行指引**：`agents/printer-soc/` 只补充本仓入口、语言适用与工作方法，明确引用上述真源。独立检出/QA 由已有机制同时取得准确 `project-control@commit` 和 `agents@commit` 并挂接，不把个人宿主路径或未跟踪软链接当作版本输入。

`AGENTS.md` 的本地链接继续使用 `.agents/...`，兼顾托管原件和业务仓入口。跨仓路径统一注明相对工作区根；从独立应用检出无法取得必需规则时，报告缺项，不自行复制旧规范或跳出授权工作区寻找。

### 4.2 本仓需要知道的分工

| 角色/关系 | 本仓执行要求 |
| --- | --- |
| PM ↔ ARCH → COORD | 沿既定同一方案、一次批准流程；目标明确的小修按需参与，不要求额外 PM 签字 |
| ENG-AP | 主责本仓 C++/C 应用、服务、中间件适配、安装、诊断和本地 UI 集成；本仓 `main` 或获批切片分支。Helix 本体须有该 SDK Git 项目的基线、产品分支与路径授权 |
| ENG-PLATFORM | 负责具体 SDK 项目的内核/设备树/驱动、基础 ABI、媒体底层、rootfs 和制镜；本仓产品 overlay 不因此取得平台写权 |
| ENG-MCU / ENG_BOOT_MC / ENG_BOOT_TH | 各写自己的固件或 Bootloader 仓；应用排障可只读定位，跨仓修复交对应角色 |
| INTEGRATOR / QA | 分别负责跨仓合龙及正式独立验收。应用作者交付准确候选与自检，不自行升级整片状态或替独立 QA 签署 |

完整十席和 RACI 直接引用 PC `02_模块与Agent职责.md`，不在本仓复制矩阵。本次获批后的治理维护仅限第 5 节七个 `agents/printer-soc` 文件，不因此扩展任何角色的业务仓写权。

### 4.3 模块职责写入 repository.md

- **DM**：设备身份、新鲜度、整机状态、准入、资源与准备编排；打印期间继续协调暂停、恢复、取消和资源调整，不接管 UART 或正文游标。
- **Forward**：唯一 UART 事务/接收所有者；控制层提供协议通路，目标打印层直接读正文并处理执行、背压和干预时机。完整文件流仍待实现，不被已有单行 G-code 替代。
- **Helix / Gateway**：本地面板与外部客户端入口并列。Helix 后台适配仍待实现，不强制经 HTTP/SSE Gateway，不在界面维护第二套设备/作业真相。
- **文件资产 / OTA**：文件领域的进程与 API 尚需具体方案；沿已确认目标职责表达，不创建空壳目录。现有 OTA 通路、FINISH ACK 与新 App 身份确认分别保留，不凭本规则迁移升级器。
- **第三方 / 产品输入**：项目适配源码直接维护；上游原始归档保持不变，补丁与锁按现有流程维护，不能只修改被忽略的解压目录。应用安装树、完整制镜和实际部署分别验收。

## 5. 精确文件清单与 Diff Budget

以下七个活动文件均属于独立 `agents` 仓，路径相对工作区根；表格为 v1.0 批准的目标清单，实际新增和修改结果见第 11 节。

| ID | 动作及文件 | 具体内容 | 完成后行数上限 |
| --- | --- | --- | --- |
| F1 | 修改 `agents/printer-soc/AGENTS.md` | 仓库/分支/输入核对、规则与技能索引、公共来源、写边界、按需验证及交付；保持入口简洁 | 90 |
| F2 | 修改 `agents/printer-soc/.agents/rules/repository.md` | 第 4 节职责和输入、真实状态、UART 排他、候选/独立仓/SDK/第三方边界 | 90 |
| F3 | 新增 `agents/printer-soc/.agents/rules/cpp_c_application.md` | 第 6 节 C++17、C 代码、C ABI、资源与并发补充；只引用公共底线 | 120 |
| F4 | 修改 `agents/printer-soc/.agents/skills/contract-vertical-tdd/SKILL.md` | 已批准任务的生产调用链、契约/边界、C++/C 实现与适量正负验证，引用 F3 | 55 |
| F5 | 修改 `agents/printer-soc/.agents/skills/systematic-link-debugging/SKILL.md` | 从 UI/IPC 到 Forward 和下位协议逐跳取证；正确 CLI、owner/线程/新鲜度/恢复边界 | 55 |
| F6 | 修改 `agents/printer-soc/.agents/skills/hmi-frontend-design/SKILL.md` | Helix C/C++ 主线程适配、本地/外部入口、真实阶段/错误、资源有界与 Mock 限制 | 55 |
| F7 | 新增 `agents/printer-soc/.agents/skills/c308l-app-delivery/SKILL.md` | 锁定 SDK/依赖、选择构建范围、目标交叉构建与安装检查、精确候选交付 | 55 |

活动文件 **最多 7 个，修改 5 个、新增 2 个；最终总计不超过 520 行，新增与删除合计不超过 650 行**。不通过压行或删除必要约束满足预算，优先删去重复叙述。当前方案原件为另一个文档文件，不计入活动规则预算；后续只在此原地修订。

本批不修改根 `AGENTS.md` / `workspace.json`、PC 公共规则及映射 JSON、`agents` 其他子目录、`printer-soc` 的任何 Git 跟踪文件、现有软链接、SDK 或业务契约。现有映射已能发现该目录，无须增加注册表、运行器状态或自动门禁。提交及根锁同步不含在本次实施范围内，按后续用户指示处理。

## 6. C++ 为主、兼顾 C 的专用要求

本节规定 F3 的内容边界；公共规范原文不复制。新增/修改代码继续执行 PC 的函数规模、入参、中文 Doxygen/docstring、防御性校验与最小修改要求，四个技能都引用同一份 F3。

### 6.1 语言与接口

- **C++17 基线**：沿现有 target 使用现代 C++，允许命名空间、强类型枚举、`constexpr`、有界值对象及适用的 RAII；不引入需要 C++20/23 的接口或新标准库前提，不为规范批量改扩展名或重写服务。
- **C 源码边界**：现有 `.c` 保留 C 语义和原有入口。需要新增 C 模块须在对应业务方案说明具体互操作/上游约束及构建目标；本批不宣布全仓已启用某个 C 标准，也不把 C++ 编译 `.c` 当作 C 兼容验证。
- **C ABI 与 C++ 头区分**：跨语言公开 API 沿现有模式使用 C 数据类型、上下文/不透明句柄、错误码及条件 `extern "C"`；不暴露 STL、引用、C++ 类或异常。纯 C++ 头内的 namespace、模板、类和方法不包进 `extern "C"`，不能因后缀为 `.h` 误判语言。
- **既有接口兼容**：不为四入参形式要求擅改公开签名；存量不等于自动获准豁免。遇不合默认规模的接口，先在具体获批任务记录调用者、兼容策略和最小预算，不在本批顺带修复。
- **头文件与类型**：引用 PC 自包含/只声明原则，C 使用适用的 `<stdint.h>/<stdbool.h>` 和 `NULL`，C++ 使用相应头与 `nullptr`；禁止混用语法。整数的范围、符号转换、单位、长度和输出有效性按实际契约说明，不用平台相关 `long` 代替线协议宽度。

### 6.2 资源、错误与生命周期按层适用

| 代码层 | 专用约束 |
| --- | --- |
| 自研协议编解码、解析器、核心通信状态机 | 按 PC 第 3.4 节零动态堆、禁异常/RTTI、有界缓冲；优先沿用已有 `Bytes/MutableBytes`。非拥有视图不得超过接收缓冲生命周期，不能用原始结构体强转或整块 `memcpy` 替代字段/字节序编解码 |
| Linux 第三方中间件适配 | 仅按 PC 第 1.4 节使用必要第三方 C++ API及异常边界，实体有配额、创建失败回滚、销毁释放；异常不穿越 C ABI，不把例外扩展成业务层自由使用无界堆 |
| 其他自研 Linux 服务与工具 | 遵守公共规则及具体方案的资源预算；队列、缓存、日志、并发和依赖有界。不依据“Linux 用户态”自行豁免公共限制；确需例外时在具体方案说明依据和范围 |

RAII 优先管理已获准资源的生命周期，不代表允许新增堆分配。拥有 fd、线程或总线/DDS 实体的对象禁止无意复制；初始化失败能够回滚，显式停止/回收可报告错误，析构不抛异常，不在全局构造期打开 UART 或启动服务。`noexcept` 只用于实现确能兑现的边界，不能用它隐藏第三方异常导致进程退出。

### 6.3 C 共通安全要求与应用并发

- 输入/输出缓冲携带容量、长度及有效期，按签名区分必填与明确可空指针；只读用 const，失败时不交付半有效输出，资源释放使用配对 API。
- 指针运算、控制流、可见性和函数规模引用 PC 规范；C 私有函数/状态限制在编译单元，C++ 使用相应模块私有范围，不用类或 lambda 隐藏无界函数。
- 网络/串口按显式字段和字节序处理，必要时校验 `sizeof/offsetof/static_assert`；不把 C/C++ 内存布局当成线协议，也不重新抄一套命令码。
- 线程、回调、队列与缓冲区明确所有者；回调不得在未知线程直接更新 UI、阻塞执行 UART 或重入业务锁。关闭时先阻止新提交、唤醒等待、停止并 join，再释放被回调引用的对象。
- UART/IPC 请求、排队和响应等待使用真实契约的有界期限，区分单次等待与整笔事务预算；单调时间用于时限。发送成功、协议 ACK 和物理完成分别表达，错误保留 target、关联序号、耗时和错误码。
- 阈值、资源上限及恢复策略引用实际配置和契约；不复制旧测试中的时间常数为产品标准，不自动重放非幂等动作，不由定时器推进真实打印/升级进度。

### 6.4 软硬件契约推演边界

本批只改治理文本，不改变命令码、帧布局、波特率、超时、线程/内存大小、分区或镜像。当前产品 UART 输入由 `board.yaml` 指定 `/dev/ttyS1`、921600、8N1、无流控；规则引用该配置，不建立第二份参数真源。MiniMCProto 继续引用 `project-control/contracts/minimc_v2_contract.yaml` 与真实消费者。

MCU 时钟、中断优先级、Flash/VTOR 不属于本次 Linux 应用规则修改，按对应固件角色与方案处理。C308L 存储、摄像头和资源性能不能由 SDK 默认值推断为实板事实；本轮不进行硬件或资源实测。

## 7. 四个技能的触发、产物与协作

| 技能 | 何时使用 | 必须完成的实际工作/产物 |
| --- | --- | --- |
| `contract-vertical-tdd` | 已批准的 C++/C 应用功能或缺陷修复 | 定位真实生产入口及消费者，先确认可观察的正常/错误预期，沿已有逻辑有界实现；按受影响模块选择测试与构建，交付候选、差异和限制。简单文本修正不强制新建单测 |
| `systematic-link-debugging` | 请求失败、超时、遥测缺失、状态过期或 UI/IPC/UART 行为不一致 | 固定输入、最小复现、逐跳证据、根因与 Owner、配对回归；禁止边猜边改多个仓。UART 诊断与正式 Forward 排他，硬件故障操作须有明确授权 |
| `hmi-frontend-design` | Helix 本地 C/C++ 页面与后台绑定、触控和状态呈现 | 在 UI 主线程消费真实接口，正确呈现 unknown/stale/offline 和请求阶段，处理取消与对象销毁；本地不依赖 Gateway，Mock 始终明确标识，不新建无消费者代理进程 |
| `c308l-app-delivery` | 依赖、交叉构建、安装树、应用包或交付输入变化 | 核对产品/SDK/依赖锁、工具链和 ABI，选择准确工作目录与 profile；检查 ELF、依赖、权限/链接、安装清单和摘要，交付准确候选及实际运行范围。完整制镜交平台，不触发部署或发布 |

四份技能保留 YAML `name/description`，描述中说明何时适用；按需调用，不将四个技能变成每次串行打卡的阶段。共享背景放在规则，技能不重复抄写矩阵和语言规范，也不新增脚本、模板库或外部 skill 运行依赖。

### 7.1 命令的真实签名与工作目录

下列是已从源码核对的入口，供获批后写入技能时选择；本轮不执行这些构建/测试/硬件操作。跨仓命令均在**工作区根**执行；`<任务唯一目录>` 等为示意，实际执行前替换为获批的准确路径。

| 范围 | 入口/参数 | 使用限制 |
| --- | --- | --- |
| 协议只读检查 | `python3 project-control/tools/sync_contracts.py --workspace .` | 当前没有 `--check`；不得无授权带 `--render-header` 写入文件 |
| 适用代码快检 | `python3 project-control/tools/gates/fast_gate.py --workspace . --files <获批修改的准确文件列表>`；切片可另传 `--slice` | 现有全局契约检查及源代码规则按真实结果处理；不能宣称它已经完成技能语义、编译或 HIL 验收 |
| 主机软件 | 根 `CMakeLists.txt` 的 `BUILD_TESTING`、`MINIMC_QA_ROOT`、`CASCADE_QA_ROOT`；完整服务另需 `SOC_AP_BUILD_SERVICES=ON` 及准确宿主依赖前缀 | 默认轻量构建不代表三个生产服务和全部九个 C 文件已编译；外部黄金用例未配置时明确缺项 |
| ARM 应用 | `python3 printer-soc/tools/build_c308l_services.py --sdk sdk/c308l --work artifacts/printer-soc/<任务唯一目录>/c308l-app --jobs 4` | 使用新输出目录，拒绝已使用的展开树；不在 SDK 来源树内输出。`--package-only` 是重打包入口，不能当成新构建证明 |
| 安装树/应用包 | `python3 printer-soc/tools/package_c308l_product.py --runtime <准确运行包目录> --output <全新安装树目录> [--helix <准确Helix包目录>]` | 输入摘要、ARM ELF、依赖、权限/链接分别核对；不等于已进入系统镜像或已在板端运行 |

`host-software`、`c308l-app`、`c308l-system` 是已有验证范围，不宣称为每个脚本通用的 `--profile` 参数。新技能不得把设计中的 `release_product.py`、CI/CD、制品库或缓存晋级当作当前可执行能力。

## 8. 有序实施任务

本批为规则/技能治理，不产生业务工程切片、运行器新状态或空候选；用三个有依赖的任务即可完成。

| ID | 目标文件 | 前置依赖与精确接口边界 | 验收与 Pass Criteria |
| --- | --- | --- | --- |
| APG-01 | F1、F2、F3 | 用户批准本方案；重新核对分支、差异和规则来源。仅治理 Markdown，无新增业务 API；第 2.1 节真实签名只作取证，不修改其声明/实现 | 入口能定位两规则、四技能及公共来源；C++17/C/C ABI/分层资源/职责语义符合第 4、6 节；明确未实现能力，不改变任何代码签名 |
| APG-02 | F4～F7 | APG-01。四份 `name` 分别为现有三个名称及新 `c308l-app-delivery`；只更新技能 Markdown | 触发条件、输入、工作方法和交付清楚；CLI 与当前源码一致；不新增固定审批/服务/门禁；全部引用同一语言规则 |
| APG-03 | 核验七文件并原地更新本方案执行记录 | APG-02；验证不修改业务仓、SDK 或其他规则 | 执行第 9 节，报告真实结果、文件清单及预算。任何失败保留原始日志，不通过删规则或改测试预期使其变绿 |

## 9. 核验、交付与回滚

### 9.1 获批实施后的必要检查

1. **精确范围与空白**：在工作区根运行 `git -C agents status --short --untracked-files=all -- printer-soc`、`git -C agents diff --check -- printer-soc` 和 `git -C agents diff --numstat -- printer-soc`。逐个读取七文件，新增文件也计入行数、空白和格式检查，不能以普通 diff 未显示未跟踪文件为由漏检。
2. **技能及引用**：对四个 `SKILL.md` 用 Python/PyYAML 解析实际 frontmatter，核对 `name/description` 和目录名称；逐条核对本地 Markdown 目标存在。公共路径按工作区根核对，不访问外部网址或个人路径。若使用已有技能校验器，先确认其真实位置/用法；没有工具时用等价结构核对，不编造执行结果。
3. **语言与职责审阅**：按第 1 节五项完成条件及第 6 节适用矩阵，逐条对照公共规范、现有头文件/CMake 和产品架构；命令参数对照第 7.1 节实际脚本。既有不符合默认规范的接口保留问题记录，不通过本批“规范制定”静默批准例外。
4. **无业务改动**：运行 `git -C printer-soc diff --exit-code`、`git -C printer-soc status --short --untracked-files=all` 以及 `bash tools/workspace_git.sh diff --exit-code`；PC 差异只能是本方案原件，`agents` 本项目其他目录无修改。核对两个现有应用软链接仍指向原目标。

这批修改没有编译/协议/运行行为变更，不新增单测、门禁程序，不为了文本验收重建 SDK 或启动服务。结构核验不代表新规则已由自动门禁全部强制执行；后续业务实现仍按真实变更完成构建、正负测试、合龙和独立 QA。

### 9.2 具体后续业务验证要求的写法

技能要求工程任务从实际 CMake target/测试定义选择验证：修改 C/C++ 公开接口时做声明—实现—调用点和编译链接验证；声明 C 兼容的接口按真实依赖分别验证 C/C++ 包含及语言链接；纯 C++ 头只做 C++ 验证。修改目标依赖或 ABI 时重验受影响 ARM 消费者；PTY/Mock、主机测试、ARM 交叉构建、板端运行和 HIL 分别报告，缺项明确说明。

此前其他任务的 QA 暂缓不在本批扩展为全局豁免。文档/技能验证完成仅说明本批内容满足约定，不签发 `SW-Verified` / `HIL-Verified`，不声称完整打印、相机、SDK 恢复或产品发布已验证。

### 9.3 交付与回滚

交付本方案原地执行记录、七文件实际清单/差异、结构与范围核验结果；不另造重复报告体系。本轮及实施阶段均不默认提交、推送或更新根锁，后续按用户明确指示归档。

实施前保存本任务前后差异识别信息。回滚只撤销本任务七文件的修改或新增，保留其他任务改动及本方案历史；不使用整仓 reset/clean，不替换业务软链接，不动 SDK 或业务候选。遇到基线变化先核实影响并更新本方案，实质范围扩张须重新获得用户批准。

## 10. v1.0 规划轮状态

已完成本工作区范围内的源码/AST、公共规范及相关仓规则只读核对，并创建本方案原件。七个活动目标仍未修改；构建、业务单测、门禁、硬件与远端操作均未执行。

本节记录批准前的规划阶段；用户随后已明确批准 v1.0。当前没有需要用户补充的产品问题，不增设第二轮需求流程。

## 11. v1.1 获批执行记录

开始前重新核实 `agents@6ca205e7a39384b2be32e244757b9701b23866a8`、`printer-soc@d9278c5269af69d1a8b5159653ce68186e59cf1c`、`project-control@965c15543dc2ff426204d80d00b3f903378cc6ce` 均仍在 `main`，本项目范围无其他待改动，PC 仅有本方案未跟踪。五个现有活动文件来自该 agents 基线，两个拟新增目标尚不存在；应用两条治理软链接仍指向第 2 节原目标。以该基线及本任务差异识别回滚边界。

APG-01、APG-02、APG-03 均已完成，没有新增脚本、业务切片、流程阶段或审批。两个新文件通过原有业务仓 `.agents` 软链接可读，不需要另建注册表或迁移代码仓。

### 实际文件与预算

| 文件（相对 `agents/printer-soc/`） | 动作 | 实际行数 / 上限 |
| --- | --- | --- |
| `AGENTS.md` | 完善入口、公共来源、角色与四技能索引 | 46 / 90 |
| `.agents/rules/repository.md` | 完善模块职责、产品事实、独立仓与平台边界 | 45 / 90 |
| `.agents/rules/cpp_c_application.md` | 新增 C++17/C/C ABI、内存、错误、生命周期及线程约束 | 49 / 120 |
| `.agents/skills/contract-vertical-tdd/SKILL.md` | 完善真实调用链、按需正负验证与交付 | 22 / 55 |
| `.agents/skills/systematic-link-debugging/SKILL.md` | 完善逐跳取证、Owner、排他与正确 CLI | 24 / 55 |
| `.agents/skills/hmi-frontend-design/SKILL.md` | 完善 UI 主线程、真实阶段与异步对象生命周期 | 17 / 55 |
| `.agents/skills/c308l-app-delivery/SKILL.md` | 新增输入锁定、交叉构建、安装检查与候选交付 | 32 / 55 |

五个原文件修改、两个新文件，合计 **235 / 520 行**。实际 `git diff --numstat -- printer-soc` 加上两个未跟踪新文件的完整行数，共新增 **202**、删除 **41**，增删合计 **243 / 650 行**；未因新文件尚未跟踪漏计预算。

### 实际核验结果

- 七文件逐个读取核对 UTF-8、末尾换行、行尾空白、代码围栏和各文件行数；包含两个新文件，全部通过。
- Python/PyYAML 解析四份实际 frontmatter，核对目录/name 一致、名称格式、description 类型/长度等，全部通过；使用工作区内等价结构核对，没有读取或安装外部技能工具。
- 17 个本地 Markdown 链接分别从 agents 托管路径、printer-soc 软链接路径核对可读；公共规则及六份产品文档引用存在，两条原有软链接目标不变。
- 用 AST 读取四个实际 Python 入口的 `add_argument`，核对协议检查、fast gate、ARM 构建和安装打包参数，确认 `sync_contracts.py` 无 `--check`。没有导入候选脚本或执行构建/硬件命令。
- `git -C agents diff --check -- printer-soc` 退出 0；本项目七目录的状态清单恰为获批的七个目标，其他本项目规则目录无修改。
- `git -C printer-soc diff --exit-code`、`bash tools/workspace_git.sh diff --exit-code` 均退出 0，应用仓状态干净；PC 只有本方案原件，未变更公共规范、映射、契约、业务代码或根锁。

人工对照公共规范和本方案完成条件，已核对 C++ 与 C 头的区别、分层内存/异常适用、存量五入参的未豁免事实、DM/Forward 与本地面板分工，以及当前未实现能力的标注。以上为规则/技能内容及结构核验，不代表自动门禁已经实现全部新约束，亦不签发业务 SW/HIL 准出。

本批未新增业务单测，未重建 SDK、交叉构建或启动服务，未执行正式独立 QA/HIL、部署或远端操作；这些均不在本次治理文本验证范围。按批准范围保留工作树改动，等待后续指示，不自动提交或更新工作区锁。

## 12. v1.3 本轮治理成果本地归档

用户在第 11 节实施完成后，明确要求“先提交本轮治理成果”，沿用此前已说明的顺序：先提交 agents 七个文件及 PC 方案，再同步根工作区版本锁。此为新增明确归档授权，取代第 5/9/11 节关于等待后续提交指示的阶段状态，不扩张业务实现范围。

| 顺序 | 仓库与精确文件 | 归档边界 |
| --- | --- | --- |
| 1 | `agents`：第 5 节七个 `printer-soc` 文件 | 单仓治理逻辑提交；不纳入 agents 内其他项目文件 |
| 2 | `project-control`：本方案原件 | 记录获批范围及实际核验；保持历史失败、业务状态与公共规范原样 |
| 3 | 根工作区：仅 `workspace.json` | 使用 `tools/workspace.py lock` 同步 agents、project-control 两个提交指针；其他仓指针和 SDK 兼容锁不得改变 |

提交前已确认三个原暂存区均为空，七个普通仓分支和 HEAD 与当前根锁一致。精确暂存后检查暂存文件及完整 `git diff --cached --check`，包含此前未跟踪的新文件。每次提交保持 Conventional Commit，失败即保留现场，不修改 hooks 或绕过检查。

子仓提交完成后检查根锁差异只涉及上述两仓，再提交根锁并真实执行 `python3 -B tools/workspace.py verify`，核对七仓及 57 项 SDK 输入一致性。此为版本组合核验，不代替业务构建或独立 QA/HIL；本轮不 fetch、rebase、push、发布或操作硬件。实际各提交 SHA 与最终结果以 Git 历史和本次执行回执为准。

agents 已完成本地提交 `3abd7d260338f363b9b68e29cea23e7a94c23102`（`docs(printer-soc): define C++ application rules and skills`），仅含批准的七个文件，本项目范围工作树干净。暂存差异空白和四份技能元数据核对通过；提交后读取实际 Git 文件内容核对与工作树一致，常规 `git show --numstat` 合计新增 202、删除 41，仍在原预算内。PC 准确版本由包含本方案的提交界定，根锁及最终组合核验结果记入本次执行回执，不为自引用 SHA 制造额外修订提交。

## 13. v1.4 已授权的远端同步

用户明确要求“推送远端”，授权同步本轮治理成果及远端恢复所必需的既有锁定候选。第 12 节的本地归档已完成：agents `3abd7d260338f363b9b68e29cea23e7a94c23102`、PC `7681315d12e4d6891cb7e73ae273e034ecc0cf3a`、根 `7b7a8b8b4c8acb9f25a30a69d79de1623ff478a0`；七仓/57 SDK 版本核验通过，工作树干净。

### 精确目标及远端实查

GitLab 目标地址均为 `ssh://git@192.168.77.113:2222/sushaohua/<项目名>.git`，实际项目名与分支见下表。agents 另按已有 `mirror_urls` 推送 `git@github.com:sushaohua/agents.git` 的 `main`；不创建项目，不调用需要令牌的 GitLab API，不推送 SDK 厂商仓或历史 soc-ap。

| 本地仓 / GitLab 项目名 | 分支 | 推送前 ls-remote 实查 |
| --- | --- | --- |
| `project-control` / `project-control` | `main` | 远端 `82b5643cde7637864982afddbf86239fee7301b1`，需同步治理候选与本记录 |
| `agents` / `agents` | `main` | GitLab `8f7137f62161439563d43e6648acb36d15b7cb47`；GitHub `a2d929594c15eb70099fd627c6bc1c34dbb1cc51`，分别 fetch 核对祖先关系 |
| `printer-soc` / `printer-soc` | `main` | 远端 `9db01b49b2ed6a7b16d423718dab2d746a1274ad`，需上传既有锁定 `d9278c5269af69d1a8b5159653ce68186e59cf1c` |
| `test_harness` / `test_harness` | `main` | 远端 `c5f35334d4d165ef9d245539995d0d2b4bd1ff6c`，需上传既有锁定 `3eef26a98a0e785a35516c910ab971ce208c58b2` |
| `mcu-p3` / `mcu-p3` | `feat/soc-debug` | 远端已为锁定 `b865222c5e7ec50cbe7d7174b8aa25f93ed16ae0`，只核对，不重复修改/推送 |
| `boot/bootloadermc` / `bootloadermc` | `soc_debug` | 远端已为锁定 `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4`，只核对 |
| `boot/bootloaderth` / `bootloaderth` | `soc_debug` | 远端已为锁定 `c56ae6fa36d8ca034f4efc8c66c1c46442433748`，只核对 |
| 根 / `ai-soc-workspace` | `main` | 远端 `b435d68bfc2a87792379614a942865121b006a3d`，在所有引用候选可取得后最后推送 |

预检发现 agents 的 `origin` 实际为已登记的 GitHub 镜像，并非工作区的 GitLab 主目标；因此不能以 origin 名称认定服务端身份。后续使用上述明确 URL 和临时 fetch 结果核对，不改 origin 配置或凭据。最初清点脚本的 origin 必须等于主 URL 断言未成立，随后只读核实了上述真实配置，没有据此绕过工程或 QA 门禁。

### 有序动作与写入预算

1. 仅本方案增加推送授权记录并单独提交；不变更七份已接受的规则技能或既有业务代码。
2. 由 ENG-AP、INTEGRATOR 分别在 printer-soc、test_harness 的准确分支 fetch/rebase；治理仓及根按各自 URL fetch/rebase。agents 核对 GitLab/GitHub 两端均可快进，禁止强推、合并或覆盖冲突。任何变基冲突立即停止保留现场，不自行解决。
3. 对齐后如候选 SHA 改变，记录实际结果；只更新根 `workspace.json` 的受影响仓提交指针，其他字段与 SDK 锁保持原样。实质源码变化不因本次推送授权顺带修改或冒称已验证。
4. 在全部对齐且版本组合核验通过后，顺序推送 printer-soc、test_harness、agents GitLab/GitHub、PC，逐个 `ls-remote` 核对分支 HEAD 与准确本地候选一致；根最后推送并复查。远端拒绝、认证或校验失败立即保留原始日志，报告已完成与未完成目标。

本步工程文件预算为 **0**；允许编辑的版本化文件仅本方案和根 `workspace.json`。Git fetch/rebase/push 限上述分支；应用和测试仓由对应角色执行，不改 hooks、凭据或其他 agents 项目文件，不强推。推送的是开发候选与治理基线，不创建产品 release、tag 或 SW/HIL 准出；此前失败和 QA 暂缓结论保持原样。网络与工具限制按实际错误处理，沙箱网络阻断按工具机制申请所需执行权限。
