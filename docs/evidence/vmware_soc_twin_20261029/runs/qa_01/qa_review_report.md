---
review_id: REV-VMWARE-SOC-TWIN-20261029-QA01
reviewer_role: QA
platform: codex
actual_session: 01a1861b-bc97-7052-bbfd-668cb2d90db0
actual_model: "Codex / GPT-6; exact runtime model alias not exposed in visible session metadata"
required_default_model: gpt-6-luna
task_id: PLAN-VMWARE-SOC-TWIN-20261029
reviewed_artifact_version: author_01 candidate manifest
reviewed_artifact: project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/candidate_manifest.json
reviewed_artifact_sha256: a5a354473c906862ff151f350587c10c5cebc9bea155cf650494896d0cc5eadf
review_scope: six listed documents, available before snapshots, and related historical document-review scope; document-only
decision: REJECTED
review_time_utc: 2026-10-29T05:25:33Z
---

# VMware → SoC 两阶段孪生开发文档独立 QA 报告

## 结论

**REJECTED**。六份候选文档整体准确记录用户确认的两阶段方向，清楚要求 VMware 阶段运行实际功能模块、独立进程、进程管理、真实 IPC 和可见交互，并要求第二阶段复用同一业务源码、契约和界面资源。B0 输入、硬件在环界限及尚未冻结的目标平台细节也基本一致且有范围说明。

阻断项是 revision 2 对历史报告范围的概括不准确：它把 revision 1 的 QA/ARCH 报告统称为只适用于 SHA256 0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae，但历史 QA01 实际审查的是另一份候选 6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5，并给出 REJECTED。QA02 才审查 0c7b4... 并给出 APPROVED；后续 ARCH 报告复核的是 QA02 报告及其目标绑定。应逐份区分报告版本、目标文档哈希与结论，避免把 QA01 错绑到 0c7b4...。

本结论只评审文档内容及其版本/历史范围说明，不改变任何任务状态，不代表 Owner 接受、软件实现、构建、HIL 或目标 SoC 验收通过。

## 审查会话与模型可见性

- 本次 Codex 线程 ID：01a1861b-bc97-7052-bbfd-668cb2d90db0，从 Codex TUI 的 list_threads 结果确认；不同于来源线程 01a1817c-49dd-7003-89ca-6502c10bc8bb。
- 可见运行身份为 Codex / GPT-6。TUI 线程元数据及当前工具接口没有暴露精确模型别名；规则要求的默认值为 gpt-6-luna。本报告如实记录不可见，不推断实际运行模型，也未声称存在模型覆盖批准。
- 本次没有构建、测试、源码操作或硬件操作。

## 候选文件哈希核对

以下六个当前文件均与 author_01 的 candidate_manifest.json 记录值及本次 sha256sum 实算值匹配：

| 候选文件 | SHA256 | 结果 |
| --- | --- | --- |
| project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md | 1d1c9d26d6126dd7771afdfcd9a7a5f862b8bbcd245cd60b366b64bc36db5b31 | 匹配；新文件，无 before 快照 |
| project-control/docs/baseline/B0_方案基线.md | 2e8e3a7e5e8e86317733dcb3c7d79c34c5b225b2820f9ccd59d7c124b7f79965 | 匹配 |
| project-control/docs/planning/soc_system_architecture_input_register_20261029.md | 4c5c6ea97bbb3cb3b1a16e931d2dc18f32667a3517e6da8bae19478473f987cc | 匹配 |
| project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md | cd68ba84fbf47d0196fd81ae2e96e6fa3bb5f52915d34ded4910948e4a745172 | 匹配 |
| project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md | 2661e57b10fcae304eca19bce4cd3af7daf21ba2cdf19663ce931d161aedfb4d | 匹配 |
| README.md | 8c2d91d5d4ca48b4bd1a360ffc6591a229b89fe20e095c2e1ee802808e2cde42 | 匹配 |

## Before 快照核对

五份现有 before 快照均存在，其 SHA256 与 before_manifest.json 匹配：

| 快照 | SHA256 | 结果 |
| --- | --- | --- |
| before/project-control/docs/baseline/B0_方案基线.md | 46a3f87a514312ea27160ceaf407aeae5fc318126d93ef4ba42ea04526ce9b34 | 匹配 |
| before/project-control/docs/planning/soc_system_architecture_input_register_20261029.md | 57151d51062307188daf47e65932aef49972c7da4ab73db5d7e99885a49cd25a | 匹配 |
| before/project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md | 0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719048e4a5e751ae | 匹配 |
| before/project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md | f64733879e00cdb4d3632c4419325b31f1d677787305967b4a46cb19440ee576 | 匹配 |
| before/README.md | a0db8f72c752dbdac9763fee475aa64bcde152afa972bc7b60f77f75cc0b40f0 | 匹配 |

新建的两阶段方案没有对应 before 文件，符合其在本轮新增的状态。逐份 diff 显示：输入登记新增 P00 并更新 P03/U01 与局部架构状态；B0 增加 D28；README 增加方案入口；选型/HMI 文件明确离线原型只用于布局讨论；温度架构 ICD 从同进程 CLI/后续 IPC 方向改为阶段一的独立服务和实际 IPC 提案。

## 内容审查

### 用户两阶段要求与旧方案替代

- 两阶段方案第 1、2、4、6 节明确 VMware 上尽量同构地运行真实模块、独立进程、生命周期管理、IPC 和界面；第二阶段复用同一业务源码、契约与 UI 资源，适配工具链、平台和部署。文中将“只改编译器和启动脚本”作为目标而非保证，并另列 ABI、驱动、显示/触控、资源和性能复验，未把未验证迁移能力当成事实。
- 两阶段方案第 4 节明确进程内回调、一次性 CLI 查询和前端造数不得替代阶段一进程/IPC/管理/显示；既有 AP 查询 CLI 只可作为诊断或库复用线索。输入表、温度 ICD revision 2、选型/HMI 文件也均说明旧同进程 CLI 方案已被替代。
- 离线 HTML 原型明确使用浏览器模拟数据、不接 AP/MC/TH、无 D-Bus/DDS/UART，且不能作为阶段一交付或 HIL 证据。其演示刷新率、过期时间和曲线未冒充生产参数。

### B0 输入、HIL 与未冻结项

- 输入表 P00/P03/U01 与 B0 D28 对齐；B0 D24/D25 仍要求真实 MC/TH 台架、真实 USB 直通串口及真实 HIL。方案允许的测试替身限于缺少对应 SoC 外设的独立软件分支，须标识来源、使用相同契约，且不能签署 MC/TH 或目标板硬件验收。VMware 阶段仍要求真实 MC/TH 结果驱动界面；目标 SoC 板卡另行实测。
- 目标板/CPU/ABI/RAM、Linux/BSP/sysroot/工具链、启动管理器/账户/路径、实屏和交互部署位置、功能首版范围、频率/过期预算、权限/所有权、控制路由、故障恢复和资源性能等仍被明确标记为待确认。D-Bus、DDS、Fast DDS 与生成器版本是候选，不是已部署或已冻结选择。
- 温度架构文件继续标明 draft，不替代 TEMP-01 签署或冻结板端协议；C1–C6 冲突、Owner 接受、物理温度/断热证据、目标平台性能及 IPC schema/QoS 均保留了前置与验收边界。

### 历史签署范围（阻断）

核对到的历史记录如下：

| 记录 | 报告 SHA256 | 实际目标文档 SHA256 | 结论/范围 |
| --- | --- | --- | --- |
| soc_temp_arch_20261028/runs/qa_01/qa_review_report.md | e7edcb750d589bc21b8a822f4ab5dca94254c8ba8abad375931e4e775c9a0820 | 6753599ef5d8282cf876649359873c2daf0f40fbcc01c379a0aa7a2e5e250bf5 | REJECTED，较早的 revision 1 候选 |
| soc_temp_arch_20261028/runs/qa_02/qa_review_report.md | ea9f75328a018d6081fb5deac7bfb5e75a794d583e71efc22dd6dbc982ec19e5 | 0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae | APPROVED，仅供 Owner 评审的 revision 1 候选 |
| soc_temp_arch_20261028/runs/report_arch_01/qa_report_arch_review.md | f7f6e8d2d226bd78d36f62d469fc09b58888921d2182c368d8bd63c562000bc8 | 对 QA02 报告复核；其报告指向目标 0c7b4... | REJECTED，限于 QA02 报告及其独立性/登记复核 |
| soc_temp_arch_20261028/runs/report_arch_02/qa_report_arch_review.md | 9d14f720931ff947210c6c102868ae5a74f4d6a59dad5e50af744ced379300cb | 对 QA02 报告复核；其报告指向目标 0c7b4... | APPROVED，限于更正后的 QA02 报告复核 |

因此，ICD revision 2 第 17 行“旧 revision 1 的 QA/ARCH 报告仅适用于原哈希 0c7b…”的概括不准确：QA01 的报告目标是 675359…，不是 0c7b…。应拆分说明 QA01 的 REJECTED 版本、QA02 对 0c7b… 的 APPROVED 范围，以及 ARCH 报告所复核的 QA02 报告哈希和其所指目标。当前 revision 2 哈希 cd68ba… 没有被这些历史报告批准；候选文字“不自动批准本 revision”这一点正确。

另有一个候选范围之外的历史索引 project-control/docs/evidence/soc_temp_arch_20261028/README.md 仍写“当前 SHA256 0c7b…”。该值对应历史 revision 1，不是现行 revision 2 的 cd68ba…；未修改该索引，但建议后续将它标为截至历史运行时的 reviewed hash，避免“当前”造成误读。

## 执行记录、命令与限制

工作目录均为 /home/sushaohua/workspace/ai_soc_project。

以下为主要 shell 检查的实际命令及退出码；相对路径均以本节所列工作目录为基准：

~~~sh
cat AGENTS.md                                                # 0
cat project-control/.agents/rules/codex_qa_review.md        # 0
cat project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/candidate_manifest.json && cat project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before_manifest.json && cat project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/document_checks.json && cat project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/README.md # 0
find project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before -type f -printf '%P %s bytes\n' # 0
sha256sum project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md project-control/docs/baseline/B0_方案基线.md project-control/docs/planning/soc_system_architecture_input_register_20261029.md project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md README.md # 0
sha256sum project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/baseline/B0_方案基线.md project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/planning/soc_system_architecture_input_register_20261029.md project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/README.md # 0
sha256sum project-control/docs/evidence/soc_temp_arch_20261028/runs/qa_01/qa_review_report.md project-control/docs/evidence/soc_temp_arch_20261028/runs/qa_02/qa_review_report.md project-control/docs/evidence/soc_temp_arch_20261028/runs/report_arch_01/qa_report_arch_review.md project-control/docs/evidence/soc_temp_arch_20261028/runs/report_arch_02/qa_report_arch_review.md # 0
sed -n '1,22p' project-control/docs/evidence/soc_temp_arch_20261028/README.md # 0
~~~

对 before 文件的比较命令为 diff -u，五个文件各自退出码均为 1（存在正文差异，不是执行错误）；两阶段方案是新文件，没有 before 对照：

~~~sh
diff -u project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/planning/soc_system_architecture_input_register_20261029.md project-control/docs/planning/soc_system_architecture_input_register_20261029.md
diff -u project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md
diff -u project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md
diff -u project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/project-control/docs/baseline/B0_方案基线.md project-control/docs/baseline/B0_方案基线.md
diff -u project-control/docs/evidence/vmware_soc_twin_20261029/runs/author_01/before/README.md README.md
~~~

正文定位另外使用 nl -ba、sed -n、rg -n 读取方案、输入表、B0、温度 ICD、IPC/HMI 文档、TEMP-01 卡及历史报告；各命令退出码为 0。Codex TUI list_threads 返回本次线程 ID。git -C project-control status --short --branch 为只读环境核对，退出码 0.

主要定位命令的完整参数如下；均在同一工作目录执行，退出码为 0：

~~~sh
rg -n -i '同进程|进程内|单进程|CLI|离线|替代|VMware|IPC|GUI|HMI|HIL|硬件|未冻结|待确认|冻结|sign|签署|accepted|APPROVED|REJECTED|输入|Input' project-control/docs/planning/vmware_soc_twin_development_plan_20261029.md project-control/docs/baseline/B0_方案基线.md project-control/docs/planning/soc_system_architecture_input_register_20261029.md project-control/docs/interfaces/soc_temperature_module_architecture_icd_draft_20261028.md project-control/docs/planning/soc_ipc_selection_and_hmi_prototype_20261029.md README.md
rg -l '0c7b4ed64d7c388f3bc4075266e9bb80d05ec8243dff1d0719047ae4e5a751ae|soc_temperature_module_architecture_icd_draft_20261028' project-control/docs/evidence project-control/.agents | sort
find project-control/docs/evidence -type f \( -iname '*temp*' -o -iname '*temperature*' \) -printf '%p %s bytes\n' | sort | head -200
rg -n 'actual_session:|actual_model:|reviewed_artifact_sha256:|decision:|reviewed_target_sha256:' project-control/docs/evidence/soc_temp_arch_20261028/runs/qa_01/qa_review_report.md project-control/docs/evidence/soc_temp_arch_20261028/runs/qa_02/qa_review_report.md project-control/docs/evidence/soc_temp_arch_20261028/runs/report_arch_02/qa_report_arch_review.md
nl -ba project-control/.agents/kanban/microtasks/temperature_telemetry/TEMP-01.md | sed -n '1,180p'
sed -n '1,22p' project-control/docs/evidence/soc_temp_arch_20261028/README.md
~~~

未进行构建、测试、源码修改、任务卡修改或硬件操作。session/model 信息由 Codex TUI list_threads 与可见运行上下文记录；精确模型子型号不可见。

## 修订要求

1. 将 revision 1 历史报告按准确目标哈希与结论分别登记，尤其区分 QA01 的 675359… / REJECTED 与 QA02 的 0c7b… / APPROVED。
2. 在报告范围中区分架构文档被审目标哈希和 ARCH 报告实际审查的 QA02 报告哈希；不把历史 QA02/ARCH 结论推广到 revision 2 (cd68ba…)。
3. 对候选范围外历史索引 README 的“当前 SHA”由其维护方另行决定是否标注为历史 reviewed hash。
4. 修订后按 canonical 流程产生新候选哈希并重新独立审查；本报告不代替复审或改写历史状态。
