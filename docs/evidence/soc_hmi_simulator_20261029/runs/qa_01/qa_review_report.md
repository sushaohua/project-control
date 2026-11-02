---
template_version: '2026-10-27'
review_id: soc_hmi_simulator_20261029-qa_01
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: '精确部署模型标签未向审阅上下文公开；上下文仅标识为 GPT-6 系列'
model_override_ref: null
planned_session_alias: null
actual_session: '不可见；未将来源会话ID误记为本审阅会话'
author_session: null
task_id: 'soc_hmi_simulator_20261029（本轮委托；无任务revision提供）'
task_revision: null
reviewed_artifact_version: 'README/index.html/app.js/style.css 与选型提案，按下列 SHA256 锁定'
reviewed_artifacts:
  - path: artifacts/soc_hmi_simulator_20261029/README.md
    sha256: 166eb96ba4170cc0da47a6207ecc645ff932d8b5347235c58b7b5e7a4d135889
  - path: artifacts/soc_hmi_simulator_20261029/index.html
    sha256: 750009b048d90e35b2924f6be137bd5f78bf37b26d86bd9a1e3cb89386422188
  - path: artifacts/soc_hmi_simulator_20261029/app.js
    sha256: 5deb862f4b50fe25820e8191db4869fabe1a35c8b00a60ba0a9575b3efcf72fb
  - path: artifacts/soc_hmi_simulator_20261029/style.css
    sha256: a5d67877921b7d0009a5e0eb77f279a3532220cac444e8d1fd0f909342f59e79
  - path: project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md
    sha256: f64733879e00cdb4d3632c4419325b31f1d677787305967b4a46cb19440ee576
protocol_and_expectations:
  - '委托限定：只审阅离线HMI模拟原型与相关提案；不审计固件或HIL。'
  - '独立规则：project-control/.agents/rules/codex_qa_review.md；模板版本2026-10-27。'
verification_environment: 'workspace /home/sushaohua/workspace/ai_soc_project；Node.js v20.20.2；无可用浏览器可执行文件及 Playwright/Puppeteer/jsdom。'
verification_scope: '静态检查、app.js Node语法解析、五类状态机语义与缓存边界；选型提案只复核所引官方来源与条件限制。'
required_evidence_level: '离线软件行为检查；不属于HIL，不宣称视觉验收。'
review_time: '2026-10-29 03:05 UTC'
process_audit: '未完全满足：运行结果可重现，但平台未公开实际会话标识及精确模型标签，无法满足规则的会话/模型签署登记。'
result_check: 'Node状态机检查通过；选型来源存在官方资料冲突；浏览器视觉未检查。'
decision: REJECTED
accepted_scope: '仅评估原型中的模拟数据边界、状态质量语义、断链/重启恢复逻辑、离线静态边界及相关提案引用的官方来源。'
limitations:
  - '没有真实浏览器或浏览器自动化环境，CSS响应式布局、画布绘图、焦点/屏幕阅读器表现未视觉验证。'
  - 'Node检查直接加载app.js导出的状态函数，不运行完整DOM事件循环，也不证明浏览器兼容性。'
  - '未进行网络抓包、硬件、串口、加热、运动、部署、性能或安全验证；提案明确不是生产版本冻结。'
  - '当前会话上下文不提供可定位的本审阅会话ID及精确模型标签；按规则不推断或编造。'
unexecuted:
  - '真实浏览器打开和人工视觉检查。'
  - '发行版/BSP包、目标sysroot/工具链、交叉编译及SoC实机验证。'
not_applicable:
  - item: '固件构建、串口、HIL及物理加热/运动检查'
    reason: '受审物是明确离线的屏幕原型；委托明确限定仅报告原型，不存在硬件验收声明。'
issues:
  - id: QA-PROC-01
    severity: blocker
    detail: 'canonical QA policy要求登记实际Codex会话和模型；该会话只暴露泛化GPT-6标签，实际session ID与精确模型不可见。独立性可以按本委托上下文确认，但签署身份记录不完整。'
  - id: QA-REF-01
    severity: major
    detail: 'Fast DDS支持周期官方来源存在不一致。提案引用的RELEASE_SUPPORT.md称3.6.x为LTS、3.6.2标准支持到2028-03且EOL到2031-05；官方3.6.2依赖/兼容页列3.6.x、标准支持与EOL均为2027-04，且未标为LTS。正式冻结前需要注明并解决来源冲突。'
commands:
  - command: 'node --check artifacts/soc_hmi_simulator_20261029/app.js'
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'Node.js v20.20.2'
    time_utc: '2026-10-29T03:05:53Z'
    exit_code: 0
    result: '语法解析通过。完整命令记录见verification_commands.log。'
    stdout_stderr: 'project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/verification_commands.log'
    stdout_stderr_sha256: 7ddff484162c60b2ddcd6c3cd061bc76a8e558c7fc667493fab1a8f57db990ac
  - command: 'node project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/node_state_checks.js'
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'Node.js v20.20.2'
    time_utc: '2026-10-29T03:05:53Z'
    exit_code: 0
    stdout_stderr: 'project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/verification_commands.log'
    stdout_stderr_sha256: 7ddff484162c60b2ddcd6c3cd061bc76a8e558c7fc667493fab1a8f57db990ac
    scenario_output_log: 'project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/node_state_checks.log'
    scenario_output_log_sha256: bad783ca9b80347c91dc9dcb67dd023a3483ee9e6f0c498241650231065dea7c
    script_sha256: 023a4222542963f061c5ff17f300095e272e634e218580da5fd51a0f0c30dd26
  - command: "rg -n -i 'fetch\\(|XMLHttpRequest|WebSocket|EventSource|https?://|navigator\\.serial|serialport|writeFile|heater|motor|gpio' artifacts/soc_hmi_simulator_20261029"
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'ripgrep; exact version not recorded'
    time_utc: '2026-10-29T03:05:53Z'
    exit_code: 1
    result: '无匹配项；rg exit 1 表示文本未命中。HTML只加载同目录style.css和app.js。'
    stdout_stderr: 'project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/verification_commands.log'
    stdout_stderr_sha256: 7ddff484162c60b2ddcd6c3cd061bc76a8e558c7fc667493fab1a8f57db990ac
  - command: "node -e module availability check for playwright, puppeteer, jsdom"
    cwd: '/home/sushaohua/workspace/ai_soc_project'
    tool_version: 'Node.js v20.20.2'
    time_utc: '2026-10-29T03:05:53Z'
    exit_code: 0
    result: '三个模块均 unavailable；chromium/chromium-browser/google-chrome/firefox 均未找到。'
    stdout_stderr: 'project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/verification_commands.log'
    stdout_stderr_sha256: 7ddff484162c60b2ddcd6c3cd061bc76a8e558c7fc667493fab1a8f57db990ac
case_results:
  - case: '初始状态与正常新样本'
    expected: '未收样本显示UNKNOWN/无数值；有效模拟样本后变为FRESH。'
    observed: 'UNKNOWN -> FRESH。'
    result: PASS
  - case: 'TH过期'
    expected: '保留旧值并标记STALE；MC仍可单独为FRESH。'
    observed: 'TH为STALE且仍有旧值，MC保持FRESH。'
    result: PASS
  - case: '传感器FAULT'
    expected: '质量为FAULT、温度值无效/空值，并显示错误级健康状态。'
    observed: 'FAULT、null、error。'
    result: PASS
  - case: '链路断开及恢复'
    expected: '断链时保留旧值并标STALE；恢复按钮后旧快照继续陈旧，收到新有效样本后才FRESH。'
    observed: '保持旧值为STALE；新样本到达后变FRESH。'
    result: PASS
  - case: 'AP模拟重启'
    expected: '代次递增、快照和趋势清空、短暂UNKNOWN，等待后新样本恢复。'
    observed: '代次增至2、双端值清空、history清空；1.5秒边界后样本到达并恢复FRESH。'
    result: PASS
  - case: '状态/缓存有界及非法场景'
    expected: 'history最多60条，events最多6条，未知场景不改变状态。'
    observed: '三个断言均成立。'
    result: PASS
required_test_sets:
  - '模拟状态值和恢复语义。'
  - '离线/无硬件控制边界静态检查。'
  - '选型来源和条件限制核验。'
executed_test_sets:
  - 'Node状态状态机断言：6组，通过。'
  - 'JS语法检查：通过。'
  - '静态网络/硬件API扫描：无命中。'
  - 'D-Bus、Fast DDS及Fast DDS-Gen官方页面核对。'
missing_test_sets:
  - '浏览器实际显示和交互视觉核验。'
raw_trace_files: []
supersedes_or_limits:
  - '本报告只覆盖2026-10-29这一组原型文件与关联选型提案，不替代产品架构接受、SoC兼容性验证或HIL。'
handoff:
  receiver_session: null
  evidence_location: project-control/docs/evidence/soc_hmi_simulator_20261029/runs/qa_01/
---

# 独立 QA 审查报告：SoC HMI 离线模拟原型

## 结论

**REJECTED（本次原型包审查）**。Node离线状态检查和静态隔离检查通过，未发现状态机错误：`UNKNOWN/FRESH/STALE/FAULT`、断链恢复、重启清快照、等待新样本，以及历史/事件缓存上限均符合原型说明。结论拒绝来自两项待解决事项：本会话没有可核验的实际会话ID/精确模型标签，无法完成canonical policy要求的签署身份登记；相关选型提案的Fast DDS官方支持周期页面数据互相冲突。拒绝不表示原型状态逻辑测试失败。

## 范围和候选

只读审查四个原型文件和关联选型提案，版本由本报告YAML中的SHA256唯一标识。遵循 `AGENTS.md` 与 canonical `project-control/.agents/rules/codex_qa_review.md`。仅在指定run目录新增Node检查脚本、原始输出和本报告；未修改受审代码、提案、任务卡或硬件。

## 检查结果

| 检查 | 结果 | 证据/说明 |
| --- | --- | --- |
| 模拟标识和本地数据边界 | 通过（静态） | HTML明确标识离线模拟、未接AP/MC/TH；只引用本地CSS/JS。静态扫描未命中网络、串口、硬件控制相关API/词项。 |
| UNKNOWN/FRESH/STALE/FAULT | 通过（Node） | 初态无值为UNKNOWN；正常样本为FRESH；过期保留旧值为STALE；FAULT返回null且健康级别error。 |
| 断链与恢复 | 通过（Node） | 断链保留旧值并STALE；切回正常时在新有效样本前仍STALE。 |
| 模拟重启 | 通过（Node） | 清空双端快照及趋势、代次+1、初始UNKNOWN；达到1.5秒后本地新样本使状态恢复。该等待是演示参数。 |
| 状态/缓存有界 | 通过（Node） | trend最多60点，events最多6条；非法scenario被忽略。 |
| JS实际执行 | 通过（Node） | Node v20.20.2对app.js作语法解析，并在VM中执行导出的实际状态函数。完整DOM和浏览器事件循环未运行。 |
| 浏览器视觉 | 未执行 | 本环境无Chromium/Chrome/Firefox，也无Playwright/Puppeteer/jsdom；布局、画布、焦点和辅助技术表现未验证。 |
| 选型来源 | 有条件、存在冲突 | D-Bus稳定线/发行版包建议与1.16.2发行记录、Fast DDS-Gen配套关系可由官方资料支持。Fast DDS支持周期有官方页面冲突，见下。 |

Node用例期望、观察结果及可重复命令见 `node_state_checks.js` 和 `node_state_checks.log`。六组断言均退出码0。未将Node结果描述为浏览器验证、硬件验证或产品安全证据。

## 官方来源核对

- D-Bus官方说明页称1.16.x为稳定线并建议优先使用发行版包；官方发行目录列有1.16.2。该提案也正确保留了发行版/BSP与target sysroot前置条件。[D-Bus官方说明](https://wiki.freedesktop.org/www/Software/dbus/)，[官方发行目录](https://dbus.freedesktop.org/releases/dbus/)
- D-Bus API指南支持采用GDBus、QtDBus等较高层绑定，并指出一般服务应避免直接使用低层libdbus。[D-Bus API设计指南](https://dbus.freedesktop.org/doc/dbus-api-design.html)
- eProsima Fast DDS-Gen兼容表将Fast DDS 3.6配套到Fast DDS-Gen 4.3.x，并列v4.3.0；提案所述生成器配套关系有官方来源支持。[Fast DDS-Gen支持/兼容表](https://github.com/eProsima/Fast-DDS-Gen/blob/master/RELEASE_SUPPORT.md)
- 支持周期数据冲突：提案引用的Fast DDS `RELEASE_SUPPORT.md`列3.6.x (LTS)、v3.6.2、标准支持至2028-03、EOL至2031-05；官方3.6.2依赖/兼容页则列3.6.x的标准支持与EOL均为2027-04，且该表没有把3.6标为LTS。该兼容页同时确认3.6.x最低CMake 3.28。两处需在正式冻结前由维护方澄清，并在提案中加上明确版本/核对日期或冲突说明。[Fast DDS RELEASE_SUPPORT.md](https://github.com/eProsima/Fast-DDS/blob/master/RELEASE_SUPPORT.md)，[Fast DDS 3.6.2依赖与兼容性](https://fast-dds.docs.eprosima.com/en/stable/notes/versions.html)

以上是官方来源一致性核查，不是对D-Bus/Fast DDS部署的批准。目标SoC、sysroot、编译工具链和实际性能尚未验证；提案已有此限制说明。

## 签署身份、限制与未执行项

Canonical policy要求登记真实Codex session和实际model。受审上下文只显示泛化的“GPT-6”系列说明，未暴露精确模型标签或本次审阅会话ID；`source_thread_id`指向委托来源，不可冒记成审阅session。默认要求模型为`gpt-6-luna`，本报告不能核实是否满足。该元数据缺口阻止本次签署为APPROVED。

视觉检查未执行，因为浏览器运行时不可用。真实浏览器检查若后续补做，应在新独立run中保留截图/环境及报告；本次Node逻辑结论仅限状态函数。

