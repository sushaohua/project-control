# 全流程 Git 服务端交接实施方案

## 修订历史

| 版本 | 修订时间（UTC+8） | 修订人 Agent/Author | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| v0.1 | 2026-11-20 09:39:36 | AI (Codex) | 定义远端交接、可独立复核的发布候选和构建清理边界 | 由 v0.2 接续评审 |
| v0.2 | 2026-11-20 10:25:34 | AI (Codex) | 记录 Helix P0 只交付最终候选，提出未来批次按交付点准出、同输入续跑和制品一次深检 | 用户于 2026-11-20 批准实施 |
| v0.3 | 2026-11-20 11:27:20 | AI (Codex) | 记录解阻事项 2、3 授权，补充目录流转及受管共享目录备选 | 事项 2、3 已同意，制品长期存放方案待选定 |
| v0.4 | 2026-11-20 12:49:20 | AI (Codex) | 按当前单机条件定义隔离取件和 GitLab 读回验证的范围 | 事项 2、3 授权沿用，跨机存储方案待验证 |

## 1. 产品目标与范围

用户已明确所有阶段的交接物必须由 Git 服务器维护，接手方不依赖上一环的机器、会话、容器或工作目录。SDK 的持久交接只保留 `sdk/c308l` 的 Git 提交快照，制镜副本和编译中间树在本轮结束后清理。优化目标是在证据可信的条件下节省 token、计算和存储。用户已确认 Helix P0 只有最终交付价值，06、07 的功能在 08 最终候选上一并验收。

本方案建议以内网 GitLab 为统一接收端。源文件、规则、方案、切片、收据、原始验证日志和账本用 Git 提交管理。确需交付的镜像或固件用同项目 Git LFS 管理，独立 QA/HIL 用到的容器镜像用 GitLab 项目 OCI Registry 按 manifest digest 管理。交接记录本身始终来自 Git 提交。LFS 和 Registry 是拟采用的 GitLab 能力，启用、访问、配额和保留状态待实测。`agents` 继续按工作区清单同步 GitHub 镜像。

- “正式交接”涵盖 PM/ARCH → COORD → ENG/INTEGRATOR → QA → 独立 Codex → HIL → 发布，以及阻塞返修、跨人和跨机器继续。撤回或失败同样要能交接实际状态和原始记录。
- “快照”是根入口仓版本、各业务仓完整提交、厂商 manifest 源及提交、产品锁出处和 SHA-256、SDK 每个 `(name, path, commit)`。当前 56 个项目由现有锁表达，锁文件是项目清单的唯一权威来源。记录可引用该锁，无需另存 SDK 的文件系统副本。
- 接收方只需任务 ID、远端 ref 和完整 SHA、受管工具及服务账号。新空环境重取该版本，验证证据摘要后可以继续同一个候选。消息和会话仅作通知，可附 Git 定位符。
- 物理台架、探针、审批人和签名私钥仍由原责任方管理。交接保存台架配置和操作记录、审批记录、签名制品和公钥来源。Human Gate #2（实板）及 #3（发布）仍独立生效。
- 范围包含新交接及仍在途的候选。已结项的方案、证据和签署原件保留。历史材料若成为现行输入，须先补齐可恢复定位并核对原始字节；缺失时记为缺口。

完成条件为两个独立工作区之间能按阶段恢复同一个任务。发布侧在原 SDK 制镜副本和构建树已清理后，从服务器取得同一候选，核对交付字节、独立软件深检结论及 HIL 结果。只有服务端可读回的交接才能驱动下一阶段或更新正式准出状态。

### 1.1 未来批次的准出规则

每份新方案先列出下一团队实际要接收并独立使用的候选，给每个切片明确交接目的，再按需安排准出。没有独立消费方和完成条件的中间切片，默认作为开发检查点。审批、写边界和硬件操作前的安全门槛沿用现行规则。

| 切片用途 | 完成时执行 | 交给下一环 | 正式状态 |
| --- | --- | --- | --- |
| 内部开发检查点 | 对改动做本地快检和针对性正负测试，缺陷尽早返回；开发者自测次数按需 | Git 上准确的代码提交、测试命令、原始必要证据及待办。接手者可继续编译、联调，正式验收覆盖项登记到交付点 | 检查点就绪，不进入 `SW-Verified` / `HIL-Verified` 账本 |
| 独立交付点 | 对同一冻结候选做正式软件门禁，兑现它本身和所覆盖检查点的验收承诺。若实际用途要求实板或发布，再进入相应授权与验收 | 已验证源码/SDK 锁、独立裁决、最终制品与所需交接证据 | 按实际覆盖登记 `SW-Verified` 或 `HIL-Verified` |

单一整机版本通常只有一个交付点。如果同一批次的驱动 SDK 要先交另一团队集成，之后整机再对外发布，这两个候选分别有明确接收方和验收条件，可以各有一次正式准出。触及底层串口、Bootloader 或其他实板红线时，物理操作前仍须命中相应安全门禁和人工授权，内部检查点身份不授予相关权限。

针对新切片，拟以 `delivery_kind: checkpoint | deliverable` 和交付点的 `covered_checkpoints` 引用在已批准方案中声明角色、基线与验收项。旧切片缺字段时走现有正式门禁。检查点未完成、历史证据与候选不符或交付点漏掉前序验收项时，编排停止。已经登记的 Helix 06/07 `SW-Verified` 属历史事实，方案仅调整当前剩余工作及未来正式准出安排。

## 2. 当前环境与端到端真实符号调用链

2026-11-20 使用无交互 SSH 执行 `git ls-remote --exit-code`，根入口仓、七个普通子仓的登记分支及 C308L 厂商 manifest 的 `master` 均返回远端 HEAD。`project-control/main` 返回 `33c66117c5d7ceec7098b27c8c5bb98ab679731f`，厂商 manifest 返回 `eb5d0d5179a03b25ceb56ac4a41c6bd87b7e06ac`。这项取证核实了读取入口。逐项目锁定提交的远端长期可达性和无缓存完整恢复留给首个实施项验证。

当前 `git lfs version` 无法执行，Docker 26.1.3 的 CLI 可用。GitLab LFS/OCI 地址、ACL、对象保留、对象是否能独立读回、Runner 的读凭据和 QA 镜像能否从空宿主启动均为 `[UNVERIFIED]`。`project-control` 本地仍有 SLICE-08 r02–r12 的未跟踪证据目录，根仓也有现行文档的本地修改或未跟踪项。已验证的远端可达性不替代这些文件的逐件迁入审查。

`printer-soc/graphify-out/graph.json` 对应 `d9278c5269af69d1a8b5159653ce68186e59cf1c`，缺少 `release_product` 节点。本表用当次工作树的 Python AST 直接提取调用边，并对照 YAML、配置和日志核实实际入口。

| 环节 | 真实调用边与入口 | 现状断点 |
| --- | --- | --- |
| 根仓恢复与 SDK | `workspace:tools/workspace.py:restore` → `load_sdk_spec` / `restore_sdk` → `workspace:tools/sdk_workspace.py:_write_revision_overlay` / `verify_sdk`（EXTRACTED） | 现有流程可按应用提交中的产品锁逐项目恢复。`publish` 只发布登记的普通仓，SDK 项目的长久引用须由各项目 Owner 维护。 |
| COORD 派单与准出 | `project-control:tools/workflow/run_slice_batch.py:_adjudicate_verdict_file` → `_qa_ok` / `as_uri`，`project-control:tools/gates/slice_gate.py:_write_gate_verdict` → `_collect_evidence_uris`（EXTRACTED） | Gate 返回本地 `file://`。`_run_codex_stage` 把当前工作区传给审阅，并在本地成功后直接追加账本。 |
| 重复验证与失败续跑 | `project-control:tools/gates/slice_gate.py:execute_slice_funnel` → `run_fast_gate` / `_run_shell_step` / `_run_docker_qa` / `_run_codex_stage`（EXTRACTED） | 06/07 的合龙命令再做一次快检并单独查契约，单轮共查三次。07 两次正式运行输入指纹相同，先前 Docker 已通过，Codex 异常仍触发整轮重跑。 |
| Docker QA | `project-control:tools/qa_runner/qa_runner.py:prepare_profile_inputs` → `_stage_profile_workspace` / `load_sdk_spec` / `restore_sdk` / `verify_sdk`，`write_evidence_bundle` → `archive_system_artifacts`（EXTRACTED） | 候选已有服务端精确检出入口。当前合成根工作区配置，未检出准确的根入口仓，发布工具会将缺根仓身份记为待补输入。归档条目含本地绝对路径，[`.gitignore`](../../.gitignore) 忽略归档下的镜像和包。`default_config.yaml` 中 `host-software` 使用本机标签、`c308l-app` 镜像 ID 为空、`c308l-system` 引用现有镜像 ID。Runner 停止容器后没有实际清理目录的路径。 |
| SLICE-07 本机构建 | `docs/evidence/SLICE-07/host_c308l_arm_build_and_pack.log` 记录从主 `sdk/c308l/` 构建、SDK 锁、产物摘要和 PASS | 原始日志已入 Git，8.6 GiB 的临时树未收尾。 |
| SLICE-08 制镜及复核 | `printer-soc:tools/release_product.py:build_image` → `prepare_sdk_copy` / `read_image_state` / `validate_image_pair` / `post_strip_map`，`release_manifest` → `verify_candidate` → `read_image_state` / `post_strip_map`（EXTRACTED） | 下一阶段会回读原制镜 SDK、产品展开树和 fakeroot 元数据。该本地试跑止于 `system-image` 校验失败，留下约 16.5 GiB。当前代码不满足清理后独立晋级。 |
| HIL 与发布 | `test_harness:hil/tests/test_helix_screen_integration.py:verify` → `check_artifacts` / `check_preflight` / `check_cases` / `check_promotion`（EXTRACTED） | HIL 在清单旁核验实际文件并绑定候选摘要。保持验收入口，让交接恢复器把 GitLab 制品恢复到该布局。 |

SDK 产品锁与平台 Owner 继续以 `printer-soc/boards/c308l-aw419/sdk/manifest.lock.xml`、`project-control/contracts/c308l_platform_contract.yaml` 为准。此次治理改造不改变 MiniMCProto 命令码、帧布局、波特率、ACK 超时、中断、RAM、Flash 分区或 VTOR。系统镜像校验继续使用现有 UBI 容量和对齐限制、AML 包内 `system.PARTITION` 等价校验、ELF 和公钥 `0444` 判据。

## 3. 服务端交接协议

### 3.1 对象归属与保留

| 对象 | 权威位置与引用 | 本机生命周期 |
| --- | --- | --- |
| 需求、方案、切片、回执、运维指引、规则与审批记录 | `project-control` 对应 Git 路径。根仓及 `agents` 各维护自身职责内容。用 `repo/ref + commit + repo-relative path` 指定版本 | 工作草稿可写，交接以已提交、已推送且已读回的版本为准 |
| 业务候选与 SDK 源输入 | `workspace.json` 登记的 Git 远端及分支、SDK manifest 与产品锁。被引用版本须能由接收方服务账号从可长期保留的 ref 取到 | 一个正常开发 SDK 检出可按锁恢复。独立 QA 或制镜临时 SDK 按 run 回收 |
| 机械门禁、合龙、独立 QA、Codex、HIL 原始物证 | `project-control/docs/evidence/<任务>/<run>/` 按阶段保存经准入的数据。每个文件记录相对路径、字节数和 SHA-256 | 日志/裁决进入 Git；超出 Git 文本预算但必须保留的原始物证使用明确的 LFS 路径。主机绝对路径可以存在于原始日志正文，不能作为接收输入 |
| 需要下游消费的最终制品 | `project-control` 同项目 Git LFS，范围按候选 manifest 和阶段白名单，包括实际使用的 `.tar.gz`、`.ubi`、`.img`、签名固件及 HIL 必需的大件 | 按需下载并验证对象内容。目标文件选择来自现有发布清单，不归档整个输出目录 |
| QA/HIL 容器环境 | Git 中跟踪配方和已接受镜像记录，GitLab OCI Registry 保留镜像清单及层。记录 `name@sha256:<manifest digest>`、目标架构和预期 image config ID | 在隔离接收环境按 digest 拉取后运行。缓存可复用但不作为取得方式的前提 |

编译对象、生成树、重复检出的 SDK、CMake/Ninja 缓存、未裁剪 ELF、`.debug` 和未被验收清单消费的中间包随本轮回收。源码凭据、Runner 凭据、私钥不进入 Git、LFS、镜像层或原始发布记录。必须长期保留的受限原始物证，仅在具备访问隔离的已批准 GitLab 位置归档。若无合适位置，该笔交接保持阻塞。

### 3.2 单一收据接口与交接时序

新增 `project-control/contracts/git_handoff.schema.json`，作为交接记录的机器契约。新工具沿用现有工作区清单和各阶段原有收据，禁止在新记录里复制业务验收逻辑。

- **交接定位符**。使用 JSON `{"repo":"project-control","ref":"refs/heads/main","commit":"<完整 SHA>","path":"<收据仓内路径>","sha256":"<收据字节摘要>"}`。`ref` 必须允许且长久可取。CLI 的 `--receipt` 接收这个 JSON 字符串，结构与收据内的前序定位符相同。当前收据所在提交 SHA 由接收定位符在提交后提供，避免自引用。
- **收据字段**。`schema_version`、任务/切片 ID、`revision`、`run_id`、阶段、真实结果、前序收据定位符、`input_fingerprint`、输入 ref/commit、锁/镜像身份、证据和制品相对路径/长度/SHA-256、可查验的审批或裁决定位符。远端 URL 从已受信的工作区登记或 GitLab 管理位置解析，拒绝绝对路径、`file://`、路径越界、软链接逃逸和未登记远端。
- **发布次序**。发起方先把候选源提交和必要 GitLab 对象发布到获批的 refs，再提交对应交接收据；从接收侧身份独立拉取指定 ref，确认提交可达、读取实际文件和 LFS 字节并验摘要。发布前先固定包含对应源码锁的根入口仓提交，QA 从真实根仓检出消费 `workspace.json`。候选运行所用的 `project-control` 提交与后来追加证据和账本的 `project-control` 提交分别锁定。COORD 收到已读回回执后才在新会话派单、准出或复用记录，正式账本变更也须推送读回。部分发布失败时保留原阶段，按同一 run/摘要幂等重试；同标识不同内容必须发新收据，冲突原样报告。

| 交接面 | 下游接受的最少输入 | 当次门槛 |
| --- | --- | --- |
| PM/ARCH → COORD | 合一方案、已批准修订、契约和切片 refs | 方案版本和审批可在远端重读，COORD 的派单指针带该提交 |
| COORD → ENG/INTEGRATOR → QA | 同一候选向量、各席自检原件、检查点完成记录、交付覆盖清单、SDK 锁和 QA 镜像 digest | 内部检查点按 Git 证据交接，到独立交付点才执行完整 QA。各分仓候选在许可 ref 可达，缺项返回 `BLOCKED`。Bootloader 只接受 `soc_debug`，MCU 保持登记分支，SDK 按 Owner 管理 |
| QA → 独立 Codex → 账本 | 同一候选的原始日志、`server_lock.json`、`server_verdict.json`、`server_qa.json`、候选实物及独立裁决 | Codex 用新检出和已读回的 QA 收据。裁决及原始流已远端可读后，方可登记和交接 `SW-Verified` |
| 软件候选 → HIL → 发布 | 最终候选清单和制品、独立深检结果、固件与台架前置身份、原始物证、审批、HIL 裁决及候选摘要 | HIL 核对受测实物 SHA 与软件候选。发布核对实际字节、独立软件裁决、HIL 收据和审批对同一候选的绑定。ACL 和 Human Gate #2/#3 分别生效 |
| 失败/阻塞 → 返修/接班 | 阶段输入、原始失败日志、退出码、已完成步骤和可重跑入口 | GitLab 暂不可用或必要证据缺失时暂停。阶段输入和原始证据可独立验证时，从第一个未完成阶段继续。修复改变输入时重建受影响的验证证据 |

### 3.3 发布接缝比选与清理时点

现行做法让 `system-image`、`verify` 和 `release-manifest` 回读同一制镜树，重做镜像配对和入镜映射检查。可选做法是远端保留 `sdk-image` 以复用这些入口，代价是每个制镜候选增加近 8 GiB 的持久依赖。采用一次独立深检、按原始字节晋级的路线。制镜阶段保留构建所需的输入检查，独立 QA 在软件准出前对冻结的最终 UBI、AML 包和产品归档做一次完整镜像深检，随后留用原件和已绑定的深检结论。

深检按锁取 SDK packer/strip，从最终 AML 包实测提取 `system.PARTITION`，与最终 UBI 对比。从该 UBI 提取 UBIFS，再核对产品归档、实际入镜内容、权限、ELF 剥离、链接及 `FILE_FILTER` 判据，08 必须为 `Y`。厂商 `rootfs.mk` 使用 `mkfs.ubifs`/`ubinize`，须先证明只读提取器保留核验所需的权限和链接语义，当前能力 `[UNVERIFIED]`。工具纳入已接受 QA 镜像。软件裁决归档深检命令和版本、原始结果、输入身份及制品摘要。受信读写权限和独立审阅负责守住一次深检的可信度。HIL 核对实物身份并增加物理证据，晋级核对制品摘要、软件/HIL 审签及授权。字节或适用输入发生变化，拒绝原候选晋级并按影响重新取证。

生命周期为“产出 → 同 run 完成自检和收据 → 服务端读回 → 回收”。成功时在结束最后一个依赖临时树的生产步骤、确认应归档内容已读回后，回收仅属于本 run 的目录与容器。故障时立即停机并保全原始证据，符合现有 Fail-Fast。GitLab 不可用时该 run 没有完成交接，临时现场只作为发布重试输入。失败收据成功归档后，结束该 run 并回收临时树。只删除有 run 所有权、位于专用根、未被活动锁持有的路径；清理失败记录剩余路径并重试回收。禁止按模糊目录前缀清理工作树或 Git 对象库。

### 3.4 资源节约与 Helix 首个验证样例

- **计算**。一轮内统一由快检阶段执行一次相同契约校验。交付点按目标环境运行所需验证，合并同一环境、同一用例的重复执行。Codex 启动等纯环境故障后，复用同一候选已通过的 Docker QA，前提是分仓提交、SDK 锁、测试命令、运行器与执行镜像摘要、必要环境和 GitLab 原始证据相符。继续执行使用新尝试 ID 并引用原通过的证据，旧记录保留。候选或输入变化影响哪些验收，就从最早受影响的阶段重新执行。
- **Token**。派单和冷审默认传入任务目标、白名单、验收项、候选差异摘要和 Git 指针。机器校验先报告缺项、错参数等确定性问题，审阅者按证据路径取用原始上下文。检查点无需独立 Codex 冷审。完整审阅仍覆盖正式交付候选的全部必需判据。
- **存储**。必要原始证据保留一份，通过路径和摘要引用。完整候选制品按内容标识归档一次，账本和审签引用同一原件；日志正文和结构化摘要避免重复嵌入同一大段输出。构建中间树、重复工作区和调试产物按 §3.3 回收。
- **Helix**。08 最终候选上执行 06 的自启/版本/全及半断连恢复、07 的 OTA 签名正负例/升级互斥/重启身份，以及 08 的制镜、`FILE_FILTER=Y`、入镜闭合和候选链。现有 08 Docker 命令主要覆盖制镜与释放流程自测，补齐 06/07 的宿主业务回归后才可采用一次统一准出。按同一冻结输入运行宿主业务回归和 ARM/C308L 制镜各自所需的任务，统一收集证据供一次软件冷审。最终保留一条完整软件准出、一次真机实测与独立终审、一次发版确认。
- **验收计量**。统计同一候选正式门禁/冷审次数、各阶段耗时、原始记录已有的审阅 token 用量、归档字节与本机清理前后字节。Helix 预期每个未变化的最终候选只走一轮正式软件准出，同一镜像只做一次完整深检。不给已有历史 06/07 生成替代认证，也不为了统计重跑历史构建。

## 4. 实施顺序、路径与 Diff Budget

获批后由 COORD 登记一条纵向切片 `project-control/slices/SLICE-GIT-HANDOFF-01.yaml`，下表为该切片顺序。表中新增接口与命令为实施设计。预算按新增/改动文件上限和新增行估计上限约束；新增代码和注释执行现有规则。各阶段凡有其他业务修改需求，回到本方案更新边界后批准。

| ID / 责任 | 精确路径与预算 | 输入输出、依赖及 Pass Criteria |
| --- | --- | --- |
| GH-01 服务端能力与空工作区恢复 / COORD、GitLab 管理员 | `project-control/slices/SLICE-GIT-HANDOFF-01.yaml`，`project-control/config/qa_runner/default_config.yaml`，`project-control/tools/qa_runner/Dockerfile.toolchain`，`project-control/tools/qa_runner/Dockerfile.c308l-system`。最多 4 个文件、120 新增行。最多建立本切片受控验证 ref；GitLab 权限/保留及实际试写按管理员授权执行 | 用已登记候选在工作区内全新目录执行 `git clone`、`python3 -B tools/workspace.py restore`、`python3 -B tools/workspace.py verify`，比对 SDK 的 56 个路径和提交。证明 LFS 样本可以由接收账号在空缓存下载真实内容，验证 Registry 三类镜像 digest、架构和 config ID 并运行 smoke，明确 Dockerfile 额外 `repo`/Linaro 构建上下文的 GitLab 来源。验证保护与保留的持久 ref。任何不可取得的输入阻塞对应环节并记录具体差距。 |
| GH-02 远端收据与阶段互锁 / project-control 工具责任方、COORD | `project-control/contracts/git_handoff.schema.json`，`project-control/tools/workflow/git_handoff.py`，`project-control/tools/workflow/run_slice_batch.py`，`project-control/tools/gates/slice_gate.py`，`project-control/tools/test_v2_gates.py`，`project-control/slices/TEMPLATE_SLICE.yaml`，`project-control/.agents/rules/delivery_and_coord_gate.md`，根 `docs/WORKSPACE.md`。最多 8 个文件、520 新增行 | 依赖 GH-01 的远端可达性。拟提供 `prepare_handoff(stage_dir: Path, metadata: dict, receipt_path: Path) -> dict` 和 `verify_handoff(receipt_ref: str, expected: dict, download_dir: Path) -> dict`。服务端验证命令为 `python3 -B project-control/tools/workflow/git_handoff.py verify --receipt <定位符> --stage <阶段> --out <空目录>`。`run_batch_cruise(cfg: dict) -> dict` 按声明运行内部检查点或交付点，消费已读回收据并按阶段续跑。以 `execute_slice_funnel(workspace, slice_path, out_dir, fast_only=False)` 为门禁接缝，复用现有快检、裁决、提示、指纹与账本入口。`python3 -B -m unittest discover -s project-control/tools -p test_v2_gates.py -v` 验证单交付、多交付和续跑正负例。接手方可删除本机证据目录后继续。私有本机路径、失效 ref、不可达 commit、错候选、缺前序检查点和只传本地 verdict 的情况应阻塞，账本不能提前变绿。 |
| GH-03 Docker QA 归档与按 run 清理 / project-control Runner 责任方、COORD | `project-control/tools/qa_runner/qa_runner.py`，`project-control/tools/test_qa_runner.py`，`project-control/.gitignore`，`project-control/.gitattributes`。最多 4 个文件、240 新增行。属性和忽略规则按制品白名单调整 | 依赖 GH-01/02。沿用 `write_evidence_bundle(output_dir, run_result, lock_data, logs)` 与 `archive_system_artifacts(sandbox_dir, output_dir, task_id)`，拟将可交接字段规范为相对路径及摘要。通过现有远端检出入口取得精确根 commit，根仓身份及锁在容器里可验证。`python3 -B -m unittest discover -s project-control/tools -p test_qa_runner.py -v` 加无缓存实跑。模拟或受控触发对象缺失、上传中断、下载摘要错误及清理竞争，确认未准出、可重试、活动 run 不受影响。通过后确认无同 run 的容器、SDK 副本及编译树。 |
| GH-04 同候选 HIL/发布复核与 Helix 统一准出 / COORD、ENG-AP、INTEGRATOR、独立 QA | `printer-soc/tools/release_product.py`，`printer-soc/tests/integration/test_release_product.py`，`project-control/slices/SLICE-GIT-HANDOFF-01.yaml`（复用 GH-01 文件），`project-control/slices/SLICE-08.yaml`（在途切片新修订）。最多 4 个文件、380 新增行。06/07 切片定义及 `test_harness/hil/tests/test_helix_screen_integration.py` 零差异 | 依赖 GH-01/02/03 和提取器实物验证。拟保留 `verify_candidate(args, plan)` 执行一次独立深检，`release_manifest(args, plan)` 消费 `--handoff <定位符>`，复用证据与字节校验入口。`python3 -B -m unittest discover -s printer-soc/tests/integration -p test_release_product.py -v` 和 `python3 -B test_harness/hil/tests/test_helix_screen_integration.py --self-test` 验证入口。08 全量验收在同一冻结候选上覆盖 `ctest`、`test_startup_fail_fast.py`、`test_aisoc_p0`、`test_ota_e2e.py`、工具与打包回归、C308L 制镜及最终镜像深检。错 AML、坏 UBI 和错入镜权限在软件准出前阻断。换机且无原 SDK 制镜树时，晋级仍核对原候选实物、软件和 HIL 裁决。错候选 HIL、缺 LFS 字节或未达 06/07 覆盖项均拒绝。真机和发布只在既有独立授权后验收。 |
| GH-05 在途切换和磁盘回收 / COORD | 当前方案原件和 `project-control/docs/evidence/SLICE-GIT-HANDOFF-01/` 本次实证；无业务修改。仅对下面清单逐路径回收 | 依赖相应历史记录的读回证明及回收授权。先审查新交接用得到的 SLICE-08 原始失败日志及构建输入锁；归档原件并独立拉取校验。核验 SLICE-07 已归档日志。执行精确路径回收后，`du -x -B1 -s .`、`python3 -B tools/workspace.py verify` 及服务端同候选恢复通过。 |

保护路径 `sdk/c308l/**`、`mcu-p3/**`、`boot/**`、`test_harness/**`、业务协议契约、历史方案/验收记录全部保持零源码差异。GitLab 对象接入的授权须覆盖具体存储及 ref；审批本方案后仍须按当前项目规定办理真实远端写入、实板和发布授权。

GH-05 首次纳入的两个本地路径为 `project-control/.slice-07-build.5BvVlh.tmp/` 与 `artifacts/slice-08-release.g9zrBD/`，合计约 25 GiB。SLICE-08 本地制镜已经失败，原始 `stages.log`、`system-image.log`、`build-plan.json` 等按实际归档需要核对；镜像或包如属于另一个仍在途且经确认的候选，先按其自身 run 归档读回，禁止跨候选混用。`artifacts/c308l-assessment/`、旧离线包、额外 worktree 和其他历史目录由各自责任范围另行核对，GH-05 不枚举删除它们。

## 5. 验收、故障与回滚

1. **跨机正例**。用两套新目录和独立权限试验，A 产出、提交、发布，B 只取得 Git 定位符，在独立目录和空 Docker 缓存中按准确锁拉取并续跑。逐阶段比对源提交、收据、镜像 digest 与对象内容，检查 QA/Codex/HIL/发布都在同一候选上。无 HIL 或发布授权时该阶段保持待验。只允许以真实原始物证升级状态。
2. **断链负例**。分别移走本机树、指向未推送提交、提交 LFS pointer 但缺对象、指向错版本或被删除的 OCI digest、提供篡改 UBI 或权限错误、串换 run 和 HIL 收据。只有本机树缺失且所有服务端对象齐全时可继续，其余均按真实原因阻塞，且不新增正式绿账。
3. **回收正负例**。成功读回后验证临时目录与容器消失，历史正式制品仍可恢复，SDK 主检出与各仓提交可验证。上传失败保全原始现场；补传且读回后回收，重试幂等。对正在运行的目录、受管工作树及带越界链接的目录拒绝回收。
4. **切换与回滚**。在新流程通过恢复演练前，不将已结项证据重标为新流程凭证。线上异常时冻结新的正式交接和准出，保留已发布的收据与引用，通过单仓线性 `git revert` 回退代码和配置。旧工具可用于局部复现，正式交接仍以可从服务端读回为界。已清理的临时树可以按锁复建；既有发布候选必须从服务端读回原字节。
5. **未来批次正负例**。演练“两个内部检查点、一个独立交付点”和“两个候选各自被独立消费”两种配置，分别只有一次和两次正式软件准出。复现 Codex 中断，确认同输入复用 QA。改变测试命令、镜像或候选后复用应被拒绝。检查点缺失或交付点覆盖漏项时，后续准出应被阻断。

## 6. 本轮审批与 COORD 交接

用户在 2026-11-20 会话回复“批准方案，实施把。”，通过 v0.2 的 Human Gate #1。审批录入时间为 2026-11-20 10:45:30（UTC+8）。执行范围以第 4 节的文件白名单、预算、阶段依赖和回收清单为准。

交由 COORD 启动 `SLICE-GIT-HANDOFF-01`，先执行 GH-01 干净恢复和服务端能力核验，再按依赖推进 GH-02 至 GH-05。获批的方案和现有 Helix/公共规则为指针来源。若环境缺少工作流原语，按现有规则委派对应责任方并如实记录执行方式。未通过 GitLab 服务端验证的交接保持阻塞。本次实施审批沿用第 4 节关于远端写入、实板和正式发布的授权边界。

## 7. 制品用目录流转与本轮解阻

同一台机器上的构建、安装包验收和制品校验可以直接在 run 的目录中交接。多台机器也可以通过受管共享目录传文件，接收方按候选清单核对大小和 SHA-256。内容一致性取决于已冻结且有独立 QA 裁决的清单，以及接收端对实际字节的核对。GitLab 保存制品原件的理由，是让另一台机器可以在原构建机退出、原工作目录清理后仍取到同一份制品，并符合已批准的 GitLab 交接要求。

| 用途 | 建议路径 | 成功条件 |
| --- | --- | --- |
| 同一运行或同一台机器临时传递 | 使用当前候选独立的本地目录。原件按清单冻结，可直接在目录中验证 | 交接双方使用同一候选 SHA 和制品摘要。该目录的生命周期由当前 run 管理 |
| 当前已批准的正式交接 | 代码、清单、SDK 锁和证据在 Git。实际需要给 HIL 或发布使用的最终制品只归档一次，可在获批的 GitLab 存储读回。中间产物按回收约定处置 | 另一机器脱离原工作区后仍能从 GitLab 取回同一候选。使用 v0.2 选定的 LFS/OCI 时，先验证各自的服务地址、权限及读回 |
| 可选的长期共享目录 | GitLab 保存候选清单、完整提交、文件大小、SHA-256、受管存储标识和相对路径。批准后由内网共享目录唯一保管最终文件，按候选摘要或内容摘要落盘 | 第二台机器使用独立账号，在原构建目录不可访问时能读取、核对和恢复原件。固定目录须具备责任人、生产端单次发布、消费端只读、保留与备份恢复。待确认这是对“正式交接物由 Git 服务器维护”的范围调整 |

共享目录备选只改变最终制品的储存地点。GitLab 上的源码、SDK 锁、QA/HIL 原始证据与裁决、正式账本照原方案管理。无论采用哪种方式，镜像深检一次，后续核对同一候选的实际字节、裁决和授权。普通个人目录可用于本机调试。涉及正式跨机取件时，按获批的存储选项验证其独立可达性。

### 7.1 用户已同意的解阻动作

1. **事项 2。** 由 ENG-AP 在 `printer-soc/.gitignore` 只增加 `/AGENTS.md` 与 `/.agents` 两条根级规则。回归时确认合法恢复软链接正常、真实源码改动仍阻塞。独立 QA 在既有 `project-control/tools/qa_runner/Dockerfile.c308l-system` 白名单内验证只读 UBIFS 提取器，用实际 UBI 证明文件权限、软链接语义与负例判据。实测通过后再解锁 GH-04 对提取器的依赖。
2. **事项 3。** 先核对 `project-control` 和根仓本任务提交，以及需归档的 SLICE-08 原始失败日志，按明确清单推送并从独立检出读回核对。现存其他任务的工作树改动单独保留。已归档证据、仍需要的候选原件和 GH-05 路径范围核对通过后，回收 §4 列明的两处目录并记录实际字节。

事项 1 的 `external_url`、Registry、客户端安装及推镜像属于另一组环境动作。本轮先按已同意的 2、3 开展可独立验证的部分。正式跨机交接在持久存储选定且实测通过后准出。如果采用共享目录备选，由 COORD 带回实际服务、责任人、可恢复性实测及最小改动清单，按方案变更批准后接入正式流程。

### 7.2 只有一台机器时的验证安排

用户确认当前没有第二台测试机器。COORD 报告任务环境内没有已提供的受管共享目录信息。事项 2 和事项 3 中的远端提交与证据读回可以在当前机器完成，沿用原授权。

1. **GitLab 读回。** 使用同机独立的空检出，直接从 GitLab 拉已推送的许可 ref，重新核对准确提交、必要日志和 SHA-256，防止误读原工作区缓存。此结果记录为服务端读回。历史失败目录如只承担失败复盘，完成必要日志与输入锁的独立读回并核对当前候选依赖后，可按已批准 GH-05 范围清理。
2. **制品流转。** 把测试用候选的清单和最终制品置于工作区内专用目录。启动消费容器时只读挂载该目录，检查挂载配置和归档摘要。构建输出树、开发工作区、Docker socket 均不可见。用原件通过和缺件或摘要错误拒绝的配对测试，记录为“单机隔离取件”。Docker 镜像导入可在有既存导出包及隔离镜像存储时附测，核对导出包摘要和实际加载的 image ID。该项与事项 2、3 独立执行。
3. **报告边界。** 单机结果能证明流程脱离原构建目录，GitLab 读回能证明本次从服务器取得相同字节。异机连通性、独立机器凭据以及共享目录保留和备份恢复留待服务实际具备时验证。对于暂时采用单机流程的工作，正式制品若仍需后续消费，须先确认其原件留在已接受的保存位置再清理构建目录。
