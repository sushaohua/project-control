---
template_version: '2026-10-27'
review_id: TWIN-03-ARCH-run_01-audit
review_status: completed
reviewer_role: ARCH
reviewer_roles: [ARCH]
platform: codex
requested_model: gpt-6-luna
actual_model: gpt-6-luna
model_override_ref: null
planned_session_alias: planned-arch-twin-03
actual_session: 01a18ab7-e3e0-7673-918e-aad60f325354
author_session: 80ffa386-f3ff-682b-0913-763109d63c86
task_id: TWIN-03
task_revision: 1
reviewed_artifact_version: "test_harness=27532d3bc1237e6f7324edcadee14fc95169fc49; project-control=80ffa386f3ff682b0913763109d63c865b0d9808"
reviewed_artifacts:
  - {path: test_harness/test_cases/twin/golden_telemetry_cases.json, sha256: bb0b37641b452bb340bc217e809102d7be362a659ab5f7895e38d9b11cbf2945}
  - {path: test_harness/test_cases/twin/golden_dbus_cases.json, sha256: 15703beb77b0cb362395d9de3bd87542863e346d087e937a78c284258cec22fe}
  - {path: test_harness/test_cases/twin/golden_sse_cases.json, sha256: 2c8032df9362e3378d41be50e26d0e9b3cde4d94a1383fb93ccbc214280e6799}
  - {path: test_harness/static_checks/twin/validate_schemas.py, sha256: 135f4f64aa66da4644fdb595abae12112864577841e03b407583c011f3a7d0b3}
  - {path: test_harness/static_checks/twin/check_layout.c, sha256: adc10afc409628e5f08bd201255965813239e40417f3764692e0992e01a4387b}
  - {path: test_harness/static_checks/twin/reconcile_layout.py, sha256: e34d19dd9128f743efe64dc84b569cd10c025ba6b83af40456c34d1b72dc51dd}
  - {path: test_harness/static_checks/twin/run_twin_cases.py, sha256: 4c7b2846413c73e58668dd8721693d00ce88169a014513e913ae245e3873d61b}
  - {path: test_harness/hil/twin_capture/twin_capture_analyzer.py, sha256: 085755b419525d3cb9f042b6e21d1f16437b5213b76d333d6f687ca7e326bcf9}
  - {path: test_harness/hil/twin_capture/test_twin_capture.py, sha256: a1bfbf7023e4cf911108e2ef799dc846f63edf27060a42724d15e10cca904496}
  - {path: project-control/docs/evidence/twin/TWIN-03/runs/run_01/result.md, sha256: fbb713817c0f4a58dca43f776cd6db3088193e634520a5857615ead8eda0f63b}
server_qa:
  path: project-control/docs/evidence/twin/TWIN-03/runs/run_01/server_qa/server_qa.json
  sha256: 1a1ac357a959852f415b419b79b20497d420f69f4c862a9ae0a7366ba2960560
protocol_and_expectations:
  - "TWIN-02 accepted version: soc-ap commit 532caecf3a146802969a49e73081400c2b32b25e; acceptance evidence: project-control/docs/evidence/twin/TWIN-02/runs/run_03/result.md"
  - "TWIN-03 card revision 1; required negative cases include timestamp/generation ordering, slow consumer, reconnect duplication, service disappearance, noise, and zero valid normal replies."
verification_environment: "只读工作区内容审阅；未在独立 ARCH 沙箱执行被审源码或自动化测试"
verification_scope: "核对交付文件哈希、静态审阅黄金用例/检查器/捕获分析器及对照任务卡和TWIN-02输入；不构成远端服务器、隔离容器或HIL真实性认证"
required_evidence_level: software-verified
review_time: "2026-10-30 Asia/Shanghai"
process_audit: failed
result_check: failed
decision: REJECTED
accepted_scope: "仅确认当前工作区所列11项文件的SHA-256与用户提供值一致；不接受其测试通过、完整契约覆盖或两阶段验收能力主张"
limitations:
  - "当前会话实际标识为null，尚待登记绑定；本报告未提供独立ARCH会话运行记录。"
  - "只读工作区中存在与清单一致的候选内容和server_qa记录，但无法独立查询远端服务器、重新fetch候选或认证容器inspect/runner真实性。"
  - "未在独立沙箱运行交付脚本、单元测试、构建或硬件测试。"
unexecuted:
  - "独立容器中的候选检出、脚本运行与原始日志复核。"
  - "Fast DDS IDL、D-Bus XML、HTTP/SSE schema对全部黄金向量的独立实测对账。"
  - "物理HIL双向原始帧采集、设备/固件绑定及真实采样抖动验收。"
not_applicable:
  - "嵌入式固件构建、MC/TH实板烧录：本票交付为测试资产，且required_evidence_level为software-verified；不据此判为通过。"
issues:
  - "ARCH-01：server_qa仅记录1项测试（任务图检查），build_results为空；没有证据表明运行了本票黄金用例、Draft7Validator矩阵、布局对账或捕获单元测试。作者报告中的测试通过声明因此未获服务器沙箱证据支持。"
  - "ARCH-02：run_twin_cases.py的负例检查只对NEG-TEL-006和NEG-TEL-007要求帧校验失败；NEG-TEL-008协议版本错误及其余时间戳、代次、重复序号和零有效回包用例只计数，不判定预期行为。"
  - "ARCH-03：D-Bus检查仅要求每个方法用例有expected_error_name、每个信号用例有emitted_args；不核对期望错误码、准入结果、字段内容或实际契约。SSE/REST检查只做部分schema验证，不核对HTTP状态码、拓扑变化语义；未知event_type或空用例也可能不产生失败。"
  - "ARCH-04：遥测哨兵检查验证帧完整性，却没有把帧内温度、状态和黄金字段逐项对账；床温路径也未验证deci_c到millic的换算。当前检查器可能在黄金内容与实际帧/状态不一致时仍报告通过。"
  - "ARCH-05：CRC16验证缺少独立已知校验向量。check_layout.c仅断言CRC非零；Python捕获单测也仅断言结果为正整数。黄金帧与检查器共用同一算法，不能单独证明CCITT-FALSE实现及线上字节序正确。"
  - "ARCH-06：捕获分析器保留CRC无效帧并可将其纳入时序/序列对账；按序号映射会折叠重复帧，对账仅比较温度和状态，不检查代次、缺帧双向统计或关联身份；超出15ms的jitter violation不会令CLI失败。"
  - "ARCH-07：交付样例没有覆盖任务卡要求的慢消费者、重连重复、服务消失等故障判据；README式分账及工具支持两种帧输入不等于已建立两阶段故障接受用例或实板验收证据。"
  - "ARCH-08：任务卡TWIN-03仍登记Backlog、planning_status=planned-not-dispatched，作者、候选和review会话字段为空；需COORD核实卡片与候选/交付报告之间的正式绑定和状态收件。"
commands:
  - command: "sha256sum [本报告列出的11个交付/证据文件]"
    cwd: "/home/sushaohua/workspace/ai_soc_project"
    tool_version: "sha256sum（版本未记录）"
    time: "2026-10-30"
    exit_code: 0
    stdout_stderr: "本会话工具输出；未归档为独立运行日志"
    stdout_stderr_sha256: null
  - command: "只读查看模板、QA规则、交付/服务端记录、任务卡及交付源码"
    cwd: "/home/sushaohua/workspace/ai_soc_project"
    tool_version: "Codex工具会话；实际会话标识待绑定"
    time: "2026-10-30"
    exit_code: 0
    stdout_stderr: "本会话工具输出；未归档为独立运行日志"
    stdout_stderr_sha256: null
case_results:
  - case_id: "sha256-manifest"
    independent_expectation: "用户清单中列出的11个交付文件哈希"
    trigger_input: "只读计算当前工作区对应文件SHA-256"
    expected: "逐项与清单一致"
    observed: "11项均一致"
    verdict: "通过（仅文件字节哈希核对）"
    evidence: "本会话sha256sum工具输出，未归档"
  - case_id: "server-sandbox-acceptance"
    independent_expectation: "独立沙箱执行本票验收脚本并留存实际日志"
    trigger_input: "server_qa.json及其引用的候选/runner证据"
    expected: "锁定候选上执行本票测试，日志与候选可核验一致"
    observed: "server_qa记录build_count=0、test_count=1；所见测试为check_task_graph；未见本票脚本执行记录"
    verdict: "失败"
    evidence: "server_qa.json、runtime.log、server_verdict.json（本地读取；真实性未独立认证）"
required_test_sets:
  - "golden telemetry正反例及CRC16独立校验"
  - "D-Bus黄金用例的错误码、准入和信号语义断言"
  - "REST/SSE schema及状态/拓扑语义断言"
  - "C/C++布局与IDL字段对账"
  - "捕获分析器帧校验、抖动和双环境对账单元测试"
  - "任务卡指定的时间戳/代次乱序、慢消费者、重连重复、服务消失、噪声及零有效正常回包负例"
executed_test_sets: []
missing_test_sets:
  - "以上必需测试组均未见本次server_qa运行证据；作者result.md中的自检记录不替代独立沙箱记录。"
raw_trace_files: []
supersedes_or_limits:
  - "本报告只审查TWIN-03 revision 1所列交付；不评价MC/TH固件、SoC实板实现或物理HIL通过。"
handoff:
  receiver_session: null
  evidence_location: "project-control/docs/evidence/twin/TWIN-03/runs/run_01（本报告由用户请求直接输出，尚未写入该目录）"
content_audit:
  fact_sources:
    result: failed
    basis: "文件哈希与清单相符；但远端提交、独立容器及服务端判定的真实性未在本会话独立认证，server_qa只记录任务图检查。"
  protocol_compatibility:
    result: failed
    basis: "检查器对CRC16缺少独立已知向量；遥测/D-Bus/SSE检查存在只计数或部分验证路径，不能据此确认所有黄金向量严格符合TWIN-02冻结契约。"
  claim_scope:
    result: failed
    basis: "作者报告宣称100%验收，但服务器记录未运行本票验收套件；任务卡指定的慢消费者、重连重复和服务消失等负例亦未覆盖。"
  architecture_completeness:
    result: failed
    basis: "捕获对账不拒绝CRC无效帧、不对jitter超限给出失败退出；现有资产不足以证明两阶段故障接受覆盖完整。"
---

# TWIN-03 ARCH 独立复核报告

## 1. 身份、候选与过程核查

复核对象为TWIN-03 revision 1，候选清单为 `soc-ap=89ac9d54c2994f635be49faa1b88ea2440b083ff`、`test_harness=27532d3bc1237e6f7324edcadee14fc95169fc49`、`project-control=80ffa386f3ff682b0913763109d63c865b0d9808`、`mcu-p3=1246ea9cb441d074ea444f53320f5632fefcd503`。本次只读计算的11项交付及报告哈希均与用户提供值一致。

本地 `server_qa.json` 声明候选锁定、容器和只读挂载，并附有server lock、runtime log及verdict的路径和哈希。但本会话无法独立查询服务器或认证这些记录；更关键的是，记录中的 `build_count` 为0、`test_count` 为1，唯一可见运行项是任务图静态检查。没有本票黄金测试和捕获测试在该容器内执行的证据。因此作者报告中的“100%验收”不能作为已由独立QA沙箱验证的结果。

任务卡仍为Backlog及`planned-not-dispatched`，作者、候选和ARCH实际会话字段为空。报告按要求保留`actual_session: 01a18ab7-e3e0-7673-918e-aad60f325354

## 2. 结果与架构/契约一致性核查

静态审阅确认交付包含遥测、D-Bus、SSE黄金JSON，Draft7Validator脚本，C/C++布局检查，IDL对账脚本、黄金用例运行器及帧捕获分析器。若干编码门禁从源码可见：新增C函数使用静态辅助函数，所见函数规模与参数量符合`≤50行、≤4参`；`check_layout.c`使用栈变量，未见动态堆分配；头文件有结构体大小及字段偏移断言。

这些源码特征不能抵消检查语义与运行证据缺口：

- **负例实际覆盖不足**：`verify_telemetry_negatives()` 对大多数负例只返回列表长度；协议版本不匹配用例没有断言拒绝。D-Bus脚本主要检查期望字段是否存在，SSE/REST脚本做部分schema验证，但没有校验状态码与业务预期，也没有完整断言黄金字段。
- **遥测值没有完整对账**：帧校验成功不等于JSON预期字段正确。哨兵用例未逐项比较帧载荷、wire状态、DDS状态与期望质量；床温路径没有像喷嘴路径一样验证温度单位换算。
- **CRC16证据不独立**：C检查只断言CRC非零，Python单测也未使用已知标准结果。黄金帧与检查器使用同一算法，未提供独立向量来证明CCITT-FALSE结果及线上字节序。
- **100ms抖动判据不是接受门禁**：分析器会报告超过15ms的间隔数量，但不会据此返回失败退出；它也可能把CRC无效帧纳入时序计算。双迹对账按序号映射，未充分处置重复序号、代次及双向丢帧。
- **Draft7Validator矩阵没有本次独立运行记录**：脚本包含部分正反例，但作者报告记录不能替代server_qa中的沙箱执行日志；现有负例也未证明所有相关约束均有针对性覆盖。
- **两阶段故障接受未闭环**：卡片要求慢消费者、重连重复、服务消失等负例，交付中未见对应黄金接受判据。捕获工具能读取虚拟与物理帧，不代表已完成物理HIL或提供实板双向证据。

## 3. 问题、限制与结论

本次拒绝基于可定位的验收缺陷：独立沙箱未运行本票测试，若干检查器仅核对字段存在或数据格式而不核验契约语义，CRC测试缺少独立已知结果，捕获分析器也未将关键故障条件作为失败判据。任务卡声明的部分负例覆盖缺失。以上问题限制了这些资产作为后续实现任务“权威黄金裁决基准”的可信度。

**决定：REJECTED。** 当前哈希匹配只证明所见文件字节与清单相符，不构成测试通过、远端候选认证或实板验证。整改后需锁定新候选，由独立沙箱运行全部适用检查并留存原始日志；ARCH报告再绑定真实会话标识及其运行证据。