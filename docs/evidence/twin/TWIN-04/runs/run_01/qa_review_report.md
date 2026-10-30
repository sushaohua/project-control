---
template_version: '2026-10-27'
review_id: TWIN-04-QA-run_01-audit
review_status: completed
reviewer_role: QA
reviewer_roles: [QA]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-qa-twin-04
actual_session: 01a18ab5-b1e8-7751-8ad8-b7ce15218e37
author_session: f7948bdf-1bcf-0963-c62c-f75e52643ea6
task_id: TWIN-04
task_revision: 2
reviewed_artifact_version: "soc-ap=89ac9d54c2994f635be49faa1b88ea2440b083ff; project-control=80ffa386f3ff682b0913763109d63c865b0d9808"
reviewed_artifacts:
  - {path: soc-ap/cmake/toolchains/vmware.cmake, sha256: fba14e74e65cf40761d2d638149c51840da2d9546067e78667cdc8f3d93f4a98}
  - {path: soc-ap/runtime/common/service_lifecycle.h, sha256: 0c11fe8cae24c5a276c5f499ac269f0509226c53979df7b17fe44a9b243e2977}
  - {path: soc-ap/runtime/common/service_lifecycle.cpp, sha256: a37604e611e94a5328d3e8cfd80a2d96f4a149ab6086232c5902e66db3c6d635}
  - {path: soc-ap/runtime/vmware/supervisor.h, sha256: 779267b37460f3f4d2193b587209c0cc677cf4565219f058ab4b238f05caad30}
  - {path: soc-ap/runtime/vmware/supervisor.cpp, sha256: 0ec194813647e69cead8d45cd7c28cf057b4b6487ad23e8ab217f43c54574f08}
  - {path: soc-ap/runtime/vmware/main.cpp, sha256: adfe411a69fa035e3e8e72bd8ced1e5d4b4305680b9dc03ab74106425a7a46a0}
  - {path: soc-ap/runtime/build/CMakeLists.txt, sha256: 54af5fbb53b127515f0bfaade74622ab826f06a40e562b41f165cbd28c251b82}
  - {path: soc-ap/runtime/build/tests/test_service_lifecycle.cpp, sha256: ddc94c4c42208cb51668aa9889a87a5ca36fcca830c1bd46c2b4974fd597a00e}
  - {path: soc-ap/runtime/build/tests/test_backoff.cpp, sha256: e70bde70ea001809a428fda7e846f021fe38f38162d0bf066615c1e7d6cdf3dc}
  - {path: soc-ap/runtime/build/tests/test_supervisor_topology.cpp, sha256: d241344d188c5d9ea4a07574d272824670a3cc36cdb64c47f81ba20d5f797093}
  - {path: soc-ap/config/runtime/common/services_manifest.json, sha256: 79c529657d3550c59305b039ed2a0e70ab013e7676e4d944c513fc925a840204}
  - {path: soc-ap/config/runtime/vmware/services_manifest.json, sha256: aface080d154ea97017c207e08ff41f810a4b3115933f6c2ec9e91e35c950af1}
  - {path: soc-ap/tools/twin_build/build_vmware.sh, sha256: 9d38842939b425742b2537998afb1a260fca94cc149956efe131cf96b8fc1c9a}
  - {path: project-control/docs/evidence/twin/TWIN-04/runs/run_01/result.md, sha256: d0ba69275fae5756b14038bdbb73d8fa94b45ba3e26670c5ea30ab0db14579b7}
server_qa:
  path: project-control/docs/evidence/twin/TWIN-04/runs/run_01/server_qa/server_qa.json
  sha256: 91bce746f3b9284ee1d2cb6c2eac1c518a154954334f93c76d33ce463c68c7e0
content_audit:
  fact_sources:
    result: passed
    basis: "server_lock、checkout.log及本地只读核对确认候选提交；列出的交付文件SHA256均与指定值一致。"
  protocol_compatibility:
    result: passed
    basis: "服务清单保留10项服务定义，4项首片服务的DDS、D-Bus及HTTP/SSE配置与依赖关系可见；本次未将清单存在等同于运行实现。"
  claim_scope:
    result: failed
    basis: "任务验收还要求真实VM服务启动、就绪、健康、退避、权限及日志限制可复现；交付运行路径实际固定为模拟模式，未覆盖这些行为。"
  architecture_completeness:
    result: failed
    basis: "拓扑有4项active和6项deferred并可按Kahn算法排序，但VMware supervisor未消费manifest中的服务二进制路径、IPC及就绪契约，无法证明实际服务拓扑运行完整。"
decision: REJECTED
review_time: '2026-10-30'
verification_scope: "TWIN-04 revision 2 指定候选的源码、清单、构建配置、作者结果文档及服务器QA记录；软件静态审查。"
required_evidence_level: software-verified
process_audit: "候选提交、文件哈希及服务器锁定记录通过核对；服务器QA日志不包含本票构建或运行测试。actual_session仍待绑定。"
result_check: "静态代码检查与既有作者证据对照完成；未在本次审查中重新构建或执行测试。"
accepted_scope: "服务状态机、退避计算及4项active服务的拓扑排序实现可读；不接受为真实VM服务生命周期通过。"
limitations:
  - "服务器QA的server_verdict记录build_count=0、test_count=1；实际执行项是check_task_graph.py，结果仅表示规划结构检查成功。"
  - "作者result.md包含构建、CTest和模拟运行文本，但服务器运行日志未包含该构建/测试命令、输出或退出码；本次未独立重跑。"
  - "本报告actual_session为null，待COORD绑定实际会话标识。"
unexecuted:
  - "VMware真实进程启动/exec失败处理、就绪信号、运行健康、权限和日志上限验证。"
  - "服务崩溃、重启风暴、设备缺失、IPC未就绪、日志满及异常退出负例。"
  - "本地独立构建及CTest复跑。"
not_applicable:
  - item: "真实MC/TH HIL与SoC实板验证"
    reason: "TWIN-04要求software-verified；该结论不覆盖硬件验收。"
issues:
  - id: "TWIN-04-QA-01"
    severity: blocker
    finding: "supervisor运行入口并未进入真实VM运行模式。main.cpp始终以simulation_mode=true初始化supervisor；默认服务注册仅填名称、角色及依赖，没有消费manifest的binary_path。"
    evidence: "soc-ap/runtime/vmware/main.cpp：supervisor_init(&supervisor, true)；soc-ap/runtime/vmware/supervisor.cpp：默认注册函数未从manifest载入服务定义。"
    impact: "当前命令路径只展示拓扑或模拟生命周期，无法复现任务卡要求的真实服务启动、权限、健康和故障恢复。"
  - id: "TWIN-04-QA-02"
    severity: blocker
    finding: "即使切换到非模拟模式，start_service_entry在可执行文件不存在时仍回退到service_lifecycle_start；fork成功后也立即转为RUNNING，未核实exec成功或服务就绪。健康检查缺省路径返回OK。"
    evidence: "soc-ap/runtime/vmware/supervisor.cpp：start_service_entry及service_lifecycle_health_check调用路径。"
    impact: "设备/服务缺失或子进程未成功执行可能被报告为启动成功、RUNNING或健康，不能满足正负例判据。"
  - id: "TWIN-04-QA-03"
    severity: major
    finding: "服务器QA记录没有验证交付实现：build_count为0，唯一test_result为check_task_graph.py。"
    evidence: "server_qa/server_verdict.json、runtime.log；测试输出明确标为静态规划验证。"
    impact: "作者文档中的构建和模拟测试结果未得到本轮服务器沙箱的独立运行证据支持。"
commands:
  - command: "读取TWIN-04任务卡、QA规则、交付审查模板、候选源码、服务清单、作者结果及server_qa证据；对15项指定文件执行sha256sum；核对四个仓库HEAD。"
    cwd: "/home/sushaohua/workspace/ai_soc_project"
    exit_code: 0
    result: "所列文件SHA256及四个候选提交均匹配。未执行构建或测试。"
case_results:
  - case: "SHA256与提交绑定"
    expected: "所列候选文件哈希及仓库提交与审查输入一致。"
    observed: "本地只读核对全部匹配；server_lock与checkout.log记载服务器按指定提交检出。"
    verdict: "通过"
  - case: "7种生命周期状态与转移"
    expected: "状态转换受约束，非法转换返回错误。"
    observed: "源码定义UNINITIALIZED、STARTING、RUNNING、DEGRADED、STOPPING、STOPPED、FAILED及对应转换；同状态转换被允许。"
    verdict: "代码检查通过；未独立运行测试"
  - case: "有界指数退避"
    expected: "按配置倍率递增并受max_interval_ms限制，达到max_retries后停止重试。"
    observed: "backoff_next_delay实现乘法、上限截断和重试次数耗尽；有效配置下符合预期。配置校验未拒绝multiplier_num=0等可能导致零延迟的配置。"
    verdict: "部分通过；配置边界需补充防御"
  - case: "Kahn拓扑启动与逆序停止"
    expected: "4项active服务按依赖顺序启动并逆序停止，检测环依赖。"
    observed: "拓扑算法实现Kahn排序及环检测；源码与作者测试定义预期顺序forward-service、device-manager、ui-gateway、browser-hmi。停止顺序由逆序索引实现。"
    verdict: "代码检查通过；实际supervisor运行仍为模拟入口"
  - case: "编译选项"
    expected: "VMware工具链和运行构建使用-fno-exceptions、-fno-rtti及严格告警选项。"
    observed: "toolchain及runtime/build/CMakeLists.txt均设置所需选项。"
    verdict: "通过；本次未重新编译"
  - case: "函数规模与参数数目"
    expected: "自研非结构体函数不超过50行、4个参数。"
    observed: "本次检查的生命周期与supervisor实现采用小函数拆分；作者结果文档报告最大42行、最多4参。未在本轮运行独立自动计数器。"
    verdict: "静态抽查未发现超限；作者数值未独立复算"
required_test_sets:
  - "真实VM启动、停止、就绪、健康、权限与日志限制"
  - "基础IPC未就绪、设备缺失、服务崩溃、重启风暴、日志满、异常退出"
executed_test_sets:
  - "服务器执行：check_task_graph.py；用于任务图静态检查，不是TWIN-04实现测试。"
missing_test_sets:
  - "TWIN-04真实VM正例及所列故障负例"
raw_trace_files: []
supersedes_or_limits:
  - "本报告只对TWIN-04 revision 2的指定候选作出判断；不改变其他仓库或任务的既有结论。"
handoff:
  receiver_session: null
  evidence_location: "project-control/docs/evidence/twin/TWIN-04/runs/run_01/"
---

# TWIN-04 revision 2 独立 QA 审查报告

## 1. 身份、候选与过程核查

| 检查项 | 实际结果 | 证据 |
| --- | --- | --- |
| 输入/范围 | **通过（候选核对）**。任务卡 revision 2、指定提交和交付路径已核对；所列文件SHA256均匹配。任务卡当前记录仍显示 `planned-not-dispatched`，作者及Reviewer的实际session字段未绑定。 | TWIN-04任务卡；server_lock.json、checkout.log；本地只读 `git rev-parse` 与 `sha256sum` 核对。 |
| 独立性 | **待绑定**。本审查按独立QA执行，作者session为 `f7948bdf-1bcf-0963-c62c-f75e52643ea6`；本报告的 `actual_session` 仍为null，须由COORD绑定真实会话标识后完成签署记录。 | 用户提供的作者session；任务卡Reviewer登记及本报告YAML。 |
| 原子步骤 | **通过（证据读取）**。本次只读核对服务器锁定、检出记录、运行记录及源码；没有改动候选或运行会写入候选目录的命令。 | server_qa证据；本报告命令记录。 |
| 代码/构建 | **部分通过**。生命周期状态、拓扑、编译选项和作者报告的函数规模/参数门禁已静态核对。任务要求的真实VM正负例未执行；服务器QA没有构建。 | 指定源码、result.md、server_verdict.json与runtime.log。 |
| 证据真实 | **部分通过**。服务器记录绑定四个候选提交，容器为只读挂载且无开发者挂载；但其唯一执行项是任务图检查，不能支持VM构建或运行验收。作者结果文档中的构建与测试输出未在服务器运行日志中复现。 | server_qa.json、server_lock.json、checkout.log、runtime.log、server_verdict.json及result.md。 |

## 2. 结果与正常/异常判据

- **生命周期状态：**代码定义七种标准状态，并通过 `service_lifecycle_can_transition` 限制跨状态转换；服务启动、健康状态更新、停止及失败处理均有相应接口。单元测试列在交付中，但本轮没有重跑。
- **有界指数退避：**实现以当前延迟乘以配置倍率、按最大延迟截断，并在重试数达到上限时返回耗尽。配置入口没有拒绝 `multiplier_num=0` 等可产生零延迟重试的参数组合，因此该算法仅对有效配置证明有界递增。
- **拓扑编排：**4项active服务与6项deferred服务已登记；active依赖图通过Kahn算法排序，并以逆序索引停止。测试源码包含环依赖检测和预期顺序检查。运行入口当前固定使用模拟模式，故该结果只证明拓扑/模拟生命周期，不证明真实进程编排。
- **编译选项：**VMware工具链及运行构建目标包含 `-fno-exceptions -fno-rtti`，并启用严格警告选项。本轮没有重新编译确认实际编译器命令。
- **函数与参数门禁：**源码采取静态结构和辅助函数拆分；未发现显著超出50行或4参数限制的实现。作者结果报告给出的最大函数42行、最大参数4个，本轮未另行运行自动计数复核。
- **VM运行和故障正反例：**没有有效运行证据。`main.cpp`将supervisor固定初始化为模拟模式；默认服务注册不读取manifest的二进制路径。非模拟分支在二进制缺失时仍回退为生命周期模拟，fork成功后即标记启动，缺少exec成功与就绪确认；缺省健康检查可直接返回OK。因此设备缺失、IPC未就绪、启动失败和进程未就绪均不能按任务契约可靠判定。
- **测试执行证据：**服务器隔离记录的 `build_count=0`、`test_count=1`；执行项是 `check_task_graph.py`，且输出说明仅为规划静态检查。作者结果文档记载了VMware构建、CTest和模拟运行，但本轮未在服务器日志中找到对应命令与结果，故不视为独立运行证明。

## 3. 问题、限制与结论

存在两项阻塞实现缺口：supervisor当前实际运行入口仅提供模拟生命周期；非模拟路径也可能在二进制缺失或exec/就绪失败时报告成功。另有证据缺口：服务器QA未构建或运行TWIN-04实现，任务卡登记中的计划状态、作者/Reviewer实际会话及租约信息也未在本次核验材料中绑定。

拓扑、生命周期状态建模、基本退避和编译选项有源码实现；这些局部结果不能满足任务卡要求的真实VM启动、就绪、健康及异常恢复可复现。**最终决定：`REJECTED`。** 修复运行模式和服务就绪/健康判断，并补齐准确候选上的独立构建及正反例执行证据后，需对新候选重新审查。