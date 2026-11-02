# 独立 QA 审查报告：VMware→SoC 两阶段任务候选

```yaml
review_id: twin_task_alignment_20261029_qa_01
review_status: completed
reviewer_role: QA
platform: codex
requested_model: gpt-6-luna
actual_model: unknown # 本会话界面未暴露精确运行模型别名
planned_session_alias: null
actual_thread_id: 01a1861b-bc97-7052-bbfd-668cb2d90db0
author_thread_id: 01a1817c-49dd-7003-89ca-6502c10bc8bb
task_id: null # 本次审查是候选批次，不是正式任务卡
task_revision: candidate_manifest_v2
reviewed_artifact_version: candidate_manifest.json SHA256 9ffb1ff23a29e50f10d6e1634949e2a448a48c2962d988b9aa5404f8b71f3f25
review_time: 2026-10-29T06:04:21Z
verification_environment: isolated workspace; read-only review and authorized local tool checks
verification_scope: planning documents, task cards, task discovery/checker change and isolated regression
required_evidence_level: document/source-reviewed
process_audit: pass
result_check: pass
decision: APPROVED
accepted_scope: exact candidate manifest above; planning/task documents and small task-discovery tool change only
```

## 审查对象与范围

按本轮 QA 请求审查了 `runs/author_01/candidate_manifest.json` 所列 89 个候选文件。其 SHA256 为 `9ffb1ff23a29e50f10d6e1634949e2a448a48c2962d988b9aa5404f8b71f3f25`；`candidate_manifest_v2.json` 与当前 manifest 字节相同。候选清单中 89 个路径均存在且哈希匹配，复核时再次逐项重算一致。逐文件期望与实测 SHA256 见 [`reviewed_file_hashes.json`](reviewed_file_hashes.json)，该清单自身 SHA256 为 `adc5475b436fc41989228ad931e25a71f4440ff967823d36bf32561f5975a94b`。

阅读范围包括：两阶段执行总表和开发方案、16 张 TWIN 卡、18 个工作包、旧卡接续与看板、规则/任务模板/QA 规则、系统架构输入登记、温度模块 ICD、D-Bus/DDS 与 HMI 提案、软硬件交接和 HMI/SoC/QA README，以及 `check_task_graph.py` 与对应测试差异。旧版独立审查没有被沿用；本报告只适用于上述准确候选哈希。

## 结论

**APPROVED — 仅限规划文件、任务组织和小型任务发现工具更新。** 未发现需要拒绝本候选的规划/结构/工具回归问题。

两阶段边界表达一致：阶段一在 VMware 跑真实业务模块、目标进程边界与管理、实际 D-Bus/DDS/HTTP-SSE 通道和可见浏览器界面，并继续使用真实 MC/TH；阶段二复用相同业务源码、契约和 UI 资源，再按真实 SoC/BSP/显示输入做构建与部署适配并在实板验收。未知 SoC/BSP/sysroot/显示和目标资源预算只阻断相应阶段二事项，没有被用作 VMware 无关工作的前置条件。离线界面、PTY/Mock、真实 MC/TH HIL、SoC 实板证据分账，模拟结果不能替代物理接受。

16 张卡的能力链覆盖架构与 C1–C6 温度冲突对账、可执行契约、独立预期、VM 构建与进程生命周期、DDS/D-Bus、FORWARD/STATE、HTTP/SSE 网关、浏览器界面、VM 整链交接与独立验收、SoC 迁移与实板验收，以及 MC/TH 必要契约复核。MC 与 TH 有各自的责任岗位、任务路径和受限固件范围。所有新 TWIN 卡仍为 Backlog；实际 owner、会话、租约和交付验收为空，没有伪造派单或接受。

18 个工作包均有两阶段范围更新。86 张旧卡的输入状态和 blocked 值未变化；46 张原 Done 卡字节保持不变。40 张变更中的既有卡均提高 revision；本次复核未发现签署被绑定到新 revision 的情况。例：MS-22 当前 revision 3，其历史 ARCH 记录仍明确绑定 revision 2，状态保持 Verify。

## 独立检查结果

| 检查 | 结果 | 证据 |
| --- | --- | --- |
| 当前候选及 89 文件哈希 | 通过：缺失 0、哈希不匹配 0；最终复核仍与 `reviewed_file_hashes.json` 一致 | [`integrity_check.log`](integrity_check.log)、[`final_integrity.log`](final_integrity.log) |
| 旧卡与覆盖表 | 通过：输入 86 张；状态/blocked 漂移 0；Done 字节漂移 0；覆盖表 102 张（46 Done、55 Backlog、1 Verify）；16 张 TWIN 均 Backlog、blocked=false，实际 owner/executor/session/decision/lease/acceptance 均未填 | [`integrity_check.log`](integrity_check.log)、[`revision_scope_check.log`](revision_scope_check.log)、[`twin_session_check.log`](twin_session_check.log) |
| 任务图 | 通过：102 张正式任务、60 张 microtask；errors=[]、依赖环 0；85 个共享写路径对全部有依赖顺序 | [`task_graph.log`](task_graph.log)、[`revision_scope_check.log`](revision_scope_check.log) |
| TWIN-01 Ready 反例 | 预期未就绪：exit 2；未登记的实际作者/检查者、worktree、输入绑定、租约/检查点、收件方及 CR-11 接受证据仍阻止开工 | [`ready_negative.log`](ready_negative.log) |
| 执行总表相对 Markdown 链接 | 通过：检查 106 个本地链接，损坏 0 | [`planning_links.log`](planning_links.log) |
| 当前工具回归 | 通过：12 项，exit 0；包含 TWIN-01 不绕过 microtask 结构/Ready 门禁的负例 | [`tool_tests.log`](tool_tests.log) |
| 基线工具回归 | 按预期 exit 1：11 项中只有旧自审断言失败，断言期待通用文字，实际诊断包含 `author (agent-author)` | [`baseline_tool_tests.log`](baseline_tool_tests.log) |

工具差异复核：`check_task_graph.py` 只在 `is_microtask()` 的识别前缀中加入 `TWIN-`。新增测试创建不完整 TWIN 卡，并断言 `write_scope` 错误和 readiness blocker；自审测试断言从宽泛文本改为与现有诊断一致的带作者标识文本。实现中的自审安全门未在本轮改变，该测试修改没有放松失败条件。

## 实际命令与证据

命令 cwd 均为 `/home/sushaohua/workspace/ai_soc_project`。Python 工具版本为 `Python 3.8.10`。各命令在 2026-10-29 UTC 本次审查窗口运行；日志没有记录每个进程的秒级起始时间，故不推算填入。

| 命令 | 退出码 | 原始日志 SHA256 |
| --- | ---: | --- |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/tools -p test_check_task_graph.py -v` | 0 | `c73e6da3795e5834f61ed8c9aef142bec25b964ab6e6edd1440549ddec920d05` (`tool_tests.log`) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s project-control/docs/evidence/twin_task_alignment_20261029/runs/author_01/before/project-control/tools -p test_check_task_graph.py -v` | 1，符合记录的旧断言失配 | `70e261ecf8f33f0546bdd1cda525850e63b0f2dbce5bd7c101d856e4cf422505` (`baseline_tool_tests.log`) |
| `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .` | 0 | `41c9a0bb1f737175548c8c3ae046c3f7029d3c5dcfa3055d110f0d5c44a8cb61` (`task_graph.log`) |
| `PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace . --check-ready TWIN-01` | 2，符合未就绪预期 | `735ebe530d96cc7c136380a00adb644538e1c603450d3bb3546b50b25a9ea870` (`ready_negative.log`) |
| `python3` inline 相对链接检查执行总表 | 0 | `14419c03e0a72205940490dacf837ebb8f30b07d2da79c0ed8fad8534271103d` (`planning_links.log`) |
| `python3` inline 清单/状态/字节/覆盖检查 | 0 | `6f49d679a550c989fa7dcbed510811d855e5304ac5e3aece58cc5ff2d4e9ca40` (`integrity_check.log`) |
| `python3` inline revision/签署/共享写顺序检查 | 0 | `7a6a131494e180e87cb78c4afe65046b168fe97931887a963c1e038df9d5f4b5` (`revision_scope_check.log`) |
| `python3` inline TWIN 实际会话/租约/接受字段检查 | 0 | `8397ad26a90a83a691dcda69b26dc0a0f7f24b7203df216db41e434cb97a5dd6` (`twin_session_check.log`) |
| `python3` inline最终哈希复核 | 0 | `6c2a6334776d4cb144ef73a326f407c442fad87474059d9e849f2cd1a55ca85f` (`final_integrity.log`) |

## 限制与未执行项

- 本报告不代表服务实现、编译、VMware 运行、真实 MC/TH HIL、SoC 交叉构建、实板/实屏、性能或物理安全验收通过；这些事项未执行。
- 由于本轮明确禁止网络访问，未重新核验 D-Bus、Fast DDS 和 Fast DDS-Gen 的外部版本/支持周期；选型文档中的外部技术版本声明不属于本次独立验证结果。
- 实际模型别名在本运行界面不可见，故记录为 `unknown`；`gpt-6-luna` 是请求模型，不被当作实际模型。
- QA 报告及 QA 工具产物仍需按仓库规则由未参与写作的 ARCH 独立复核。此待复核不改变本报告对作者候选规划/工具差异的独立决定，也不更新正式任务状态。

## 收件

接收岗位：COORD（待登记实际会话与收件回执）。本报告哈希不在本文件自引用，单独保存在 [`qa_review_report.sha256`](qa_review_report.sha256)。所有检查日志和哈希证据位于本目录。
