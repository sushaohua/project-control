# soc-ap 编译与启动问题人工提交（2026-11-05）

## 公共约束

- 来源：用户在助理会话中要求确认下列三个可能问题是否存在并修复，随后明确要求放入收件入口，供 COORD 自动取得。三条指令主分类均为“问题 / issue”；编号、分类 YAML、正式任务关联由既有收件流程查重生成。
- 本单是人工要求的整理稿，不是缺陷已复现、修复完成或 QA 通过的证明。用户提供的根因和修复方法作为调查线索；已修复项核实版本及证据后复用，不重复修改。
- 只读观察基线：当前工作区 `soc-ap` 的 `main`，HEAD `7c1f35091850b39f4ba3ff9b242043a62f3e5b74`；管理仓观察 HEAD `491158cd4f183a01517c36fb093821db54a8a6dd`。执行前重新锁定服务器准确候选。
- 用户报告中的 `/home/sushaohua/tmp/ai_soc_project/` 与当前 `/home/sushaohua/workspace/ai_soc_project/` 不同，须核对源码、构建制品及实际加载库的版本，不默认两处相同。
- 由唯一 COORD 查重收件、关联正式任务并更新 Board；INTEGRATOR 汇总编译部署问题，DDS 依赖问题交 ENG-DDS，职责或技术冲突由 ARCH 补充裁定。COORD 不代改业务源码。
- 沿用有效授权及简化 QA，避免无关重构。确认的修复应可从干净服务器检出复现；第三方补丁必须版本化并纳入构建，不能只修改 Git 忽略的安装目录。
- 当前只有一台 VMware 和一套物理台架；本单不授权抢占台架、停止现有任务、烧录、运动或加热。构建与进程生命周期验证安排到明确窗口；本单三项软件修复不默认增加整机 HIL。
- 本次助理仅整理任务并只读核查，未编译、未启动服务、未执行测试，也未修改业务代码。

## 指令 1

【问题】核实并修复 GCC 15 下 test_backoff.cpp 的未初始化警告导致全栈构建阻断（对应用户“问题 2”，根因待查）。

用户报告：全栈编译停在 `build 1/5 runtime`，`runtime/build/tests/test_backoff.cpp` 的局部变量传入防御性断言时触发 `-Werror=maybe-uninitialized`。建议将 `backoff_state_t st;`、`backoff_config_t cfg;` 改为显式零初始化。

当前只读观察：`test_backoff_null_guards()` 中上述两个声明仍未初始化，相关 CMake 目标启用了 `-Werror`；助理未在 GCC 15 下复现告警。实现的空指针卫语句与编译器诊断分别核实，不把告警直接表述成已发生的运行期未初始化读取。

处理要求：记录实际 GCC 版本、完整编译参数和原始错误；确认后在必要位置采用最小初始化修复，保留空指针防御测试及严格告警策略，不以关闭告警或删除断言通过构建。

验收目标：同一 GCC 15 构建条件下消除该阻断，相关 backoff 测试的防御、递增、上限和重置行为保持正确；记录实际执行范围及结果，不把只通过 runtime 目标写成全栈已通过。

## 指令 2

【问题】核实 Fast-CDR optional 复制/移动语义与 Fast-DDS 启动崩溃的关系，并使必要修复可随干净构建复现（对应用户“问题 3”，根因待查）。

用户报告：`forward_service_daemon`、`device_manager_daemon` 启动发生 SIGSEGV / 退出码 139；GDB 栈涉及 `PublicationBuiltinTopicData` 复制构造和 `std::string::_M_construct`。报告将其归因于 Fast-CDR 2.2.5 的 `optional<T>` 在源对象未赋值时仍构造 union 内对象，建议在复制/移动构造中检查 `val.storage_.engaged_`，重编 Fast-CDR、Fast-DDS。用户另报告修补后有 `ALL 6 FAST DDS TEST SUITES PASSED` 输出，此结论须取得原始命令、逐项结果和版本绑定后核实。

当前只读观察：
- 本工作区 `third_party/src/Fast-CDR-2.2.5/include/fastcdr/xcdr/optional.hpp` 与 `third_party/install/include/fastcdr/xcdr/optional.hpp` 已包含所述条件守卫，不能把本地头文件重复描述为仍未修补。
- 仓库 `third_party/archives/Fast-CDR-2.2.5.tar.gz` 内的同名头文件仍无上述守卫，复制/移动构造无条件构造内部对象；压缩包头文件与安装头文件不同。
- `third_party/src/`、`build/`、`install/` 均被 Git 忽略，当前构建脚本从压缩包展开源码，未观察到此修补的版本化应用步骤。须核实本地修补来源及干净重建的实际结果。

处理要求：先核对崩溃现场、编译器/ABI、实际加载的 Fast-CDR/Fast-DDS 库及符号，不仅凭栈顶字符串构造就锁定唯一根因。确认 optional 缺陷后，采用可追溯的最小补丁或已接受的依赖修订方案；保留原始归档来源和校验信息，明确补丁应用位置、幂等性及失败处理。重建受头文件影响的 Fast-CDR、Fast-DDS 和相关 AP 消费者，避免新旧头文件/库/二进制混用。

验收目标：干净检出和重新解包能够自动得到相同修复；覆盖未赋值/已赋值对象的复制、移动及相关生命周期行为；相关 DDS 跨进程通信与两个守护进程的启动健康验证通过。以真实测试条目、退出码及日志证明结果，不将一行汇总文本当作全套测试证明。

## 指令 3

【问题】核实并修复部署调用结束或会话断开后守护进程退出的问题（对应用户“问题 4”，根因待查）。

用户报告：部署脚本退出后四个守护进程同时终止，怀疑未充分隔离 SIGHUP、标准输入和 shell 作业管理；建议统一使用 `nohup`、`< /dev/null` 和 `disown`。

当前只读观察：`tools/deploy_twin.sh` 以 `--nofork` 后台启动 `dbus-daemon`，该启动行没有 `nohup`；forward、device_manager 和 ui-gateway 已使用 `nohup`，但启动行未显式重定向标准输入，脚本没有 `disown`。这些是代码事实，尚不能证明“非交互 shell 正常退出必然杀死全部子进程”。

处理要求：在实际调用方式下区分正常脚本退出、终端/SSH 断开、SIGHUP、父级超时或进程组/cgroup 清理，保存进程树、退出/信号和服务日志。按实际原因选择最小可靠方案；`nohup`、标准输入解绑、作业表处理或已有受控服务管理方式按适用性采用，不把三种 shell 写法机械拼接当作充分修复。不得用忽略错误掩盖服务已启动失败。

验收目标：在约定的部署调用结束和会话断开场景中，四个服务按冻结的生命周期要求存活，D-Bus 和 HTTP/公开健康检查有效；PID/运行记录指向实际进程，显式停止后不遗留占用，重复部署可正确收敛。父级主动销毁整个受控执行环境的场景与普通 shell 退出分开声明，不能声称 nohup/disown 可抵抗所有回收。
