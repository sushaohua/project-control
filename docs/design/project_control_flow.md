# `project-control`（AI SoC V2）全流程真实流转图

本文档严格依据 `/home/sushaohua/workspace/ai_soc_project/project-control` 当前 `HEAD (8dc3a1b)` 的现役规则与工具代码逆向绘制（已排除封存于 `tools/legacy/` 的 V1 废弃状态机），供直观审视其**信息流、控制流、交接跳数与门禁卡点**后再做架构决断。

---

## 一、全景端到端主干流转图（Phase 1 规划 → Phase 2 四阶漏斗 → Phase 3 真机与发布）

```mermaid
flowchart TD
    Start(["用户提出需求或问题"]) --> Triage{"目标明确的小修?"}

    subgraph P1["阶段一 Phase 1：实施方案先行与单一真相源 (SSoT)"]
        Triage -->|"否 (需产品定义)"| SpawnPM["COORD 用 swarm 拉起 PM (指定高级模型)"]
        SpawnPM --> PMWork["PM 编写产品章节 (场景 / 范围 / 完成条件)"]
        PMWork --> CoordRelay["COORD 中转产品澄清与技术可行性往返"]
        CoordRelay --> SpawnArch["COORD 用 swarm 拉起 ARCH (指定高级模型)"]
        Triage -->|"是 (跳过 PM)"| SpawnArch

        SpawnArch --> ArchWork["ARCH 查 graphify 与 contracts 原地合成方案 (.md)"]
        ArchWork --> LockPlan["COORD 锁定方案修订号与 sha256sum"]
        LockPlan --> PreReview["独立 Codex 只读预审 (plan-pre-review 技能)"]
        PreReview --> PreCheck{"预审结果?"}
        PreCheck -->|"存在客观 BLOCKER"| ArchWork
        PreCheck -->|"UNAVAILABLE (超时或启动异常)"| UserDecide["呈报用户决定等待补审或转人工审"]
        PreCheck -->|"0 BLOCKER (附 MINOR 与人工待决项)"| HG1
        UserDecide --> HG1{"Human Gate #1：用户批准方案?"}
    end

    HG1 -->|"打回修改"| ArchWork
    HG1 -->|"批准执行 (生成 slices/SLICE-XX.yaml)"| CruiseStart["COORD 启动 run_slice_batch.py 批次巡航"]

    subgraph P2["阶段二 Phase 2：垂直切片连坐与四阶无状态门禁漏斗"]
        CruiseStart --> IdempCheck{"ledger.md 已登记准出且 input_fingerprint 未变?"}
        IdempCheck -->|"是 (幂等跳过)"| NextSlice{"还有后续切片?"}
        IdempCheck -->|"否"| PreHandoff["git_handoff.py 核验前序远端收据与 covered_checkpoints"]
        PreHandoff -->|"缺件或摘要不符"| BlockedStop(["BLOCKED (退出码 2)：零扣返修，停机保现场"])
        PreHandoff -->|"就绪"| SubtaskParallel["按 subtasks 并发派发各仓工程 Agent (四文件稀疏指针)"]

        SubtaskParallel --> EngCommit["ENG-AP / ENG-PLATFORM / ENG-MCU / ENG_BOOT 各自提交并推送许可分支"]
        EngCommit --> AllocDir["分配唯一证据目录 run_时间戳_UUID (禁复用旧目录)"]

        AllocDir --> G1["第 1 阶 fast_gate.py (<3s 契约 / 分支红线 / 函数规模 / 反造假快检)"]
        G1 -->|"违规 FAILED(1)"| ReworkJudge
        G1 -->|"通过"| G2["第 2 阶 integration_cmd (跨仓合龙与宿主打包自检)"]
        G2 -->|"环境或SSH异常"| BlockedStop
        G2 -->|"断言失败 FAILED(1)"| ReworkJudge
        G2 -->|"通过"| KindBranch{"切片 delivery_kind 类型?"}

        KindBranch -->|"checkpoint (内部检查点)"| SaveCP["写 checkpoint_receipt.json (免容器QA / 免Codex冷审 / 不入账本)"]
        SaveCP --> NextSlice

        KindBranch -->|"deliverable (正式交付点)"| ReuseCheck{"try_reuse_qa 命中同指纹同镜像缓存?"}
        ReuseCheck -->|"命中已验结果"| G4
        ReuseCheck -->|"未命中"| G3["第 3 阶 qa_runner.py (纯SSH核验远端SHA -> 只读Docker全新检出构建回归)"]
        G3 -->|"未推送 / SSH或Docker故障 / 证据冲突"| BlockedStop
        G3 -->|"构建或回归失败 FAILED(1)"| ReworkJudge
        G3 -->|"产出互锁 server_qa + server_verdict + server_lock"| G4

        G4["第 4 阶 codex_review.py (异构 Codex 只读双轴分级冷审 420s)"]
        G4 -->|"CLI缺失 / 超时 / 缺会话ID"| BlockedStop
        G4 -->|"存在 BLOCKER -> REJECTED(1)"| ReworkJudge
        G4 -->|"0 BLOCKER -> APPROVED(0)"| WriteLedger["追加 slices/ledger.md 登记 SW-Verified (MINOR 入技术债表)"]

        ReworkJudge{"已用返修轮次 < 2?"}
        ReworkJudge -->|"是 (消耗 1 轮额度)"| BroadcastFix["向该片全部 subtasks 广播失败原因与当次 file:// 证据返修"]
        BroadcastFix --> AllocDir
        ReworkJudge -->|"否 (满 2 轮熔断)"| MeltdownStop(["FAILED 熔断停机：升级人工介入"])

        WriteLedger --> RemoteReadback["git_handoff.py 推送证据并独立空检出读回验 SHA256 -> 回收临时构建树"]
        RemoteReadback --> HilFlag{"触及底层驱动/Bootloader 或批次末需真机?"}
    end

    HilFlag -->|"否"| NextSlice
    NextSlice -->|"有下一片"| IdempCheck
    NextSlice -->|"批次全部完成"| HilGate

    subgraph P3["阶段三 Phase 3：真机 HIL 穿刺与发布闭环"]
        HilFlag -->|"是 (立即停机请示)"| HilGate{"Human Gate #2：用户授权实板 HIL (Bootloader SWD 单独 #2B)"}
        HilGate --> HilRun["排他台架真机实测 (采集双向 Raw Hex / 时戳 / 实板固件版本读回)"]
        HilRun --> HilAudit["独立 Codex 审计真机物证链 (HW-G5/G6/G7)"]
        HilAudit -->|"假阳性或物证不全"| ReworkJudge
        HilAudit -->|"通过"| LedgerHIL["账本升级为 HIL-Verified"]
        LedgerHIL --> HG3{"Human Gate #3：发布授权 -> 各仓 fetch + rebase 线性发布"}
    end
```

---

## 二、单次需求跨角色真实交互跳数图（Sequence View）

下图按时间轴还原 `project-control` 处理一个含多仓改动切片时的**真实会话往返跳数**（可直观看到哪些跳数是核心防线，哪些跳数产生了通信折返开销）：

```mermaid
sequenceDiagram
    actor User as 用户
    participant Coord as COORD (主会话)
    participant PM as PM (swarm 子会话)
    participant Arch as ARCH (swarm 子会话)
    participant Codex as 独立 Codex CLI (只读)
    participant Engs as 各仓 ENG-* 组 (并发子会话)
    participant Gate as slice_gate + Docker QA (Python)
    participant GitSSH as 内网 GitLab (纯 SSH:2222)

    Note over User,Codex: Phase 1：规划与预审 (约 4~6 跳)
    User->>Coord: 1. 提出需求想法
    Coord->>PM: 2. 拉起 PM 写产品定义章节 (仅传指针)
    PM-->>Coord: 3. @coordinator 返回方案路径与待澄清项
    Coord->>Arch: 4. 拉起 ARCH 查 graphify/契约，同文件合稿技术章节
    Arch-->>Coord: 5. @coordinator 返回完整方案与切片拆分
    Coord->>Codex: 6. 锁 sha256 启动只读方案预审 (plan-pre-review)
    Codex-->>Coord: 7. 返回 BLOCKER / MINOR / 人工待决项 (若有 BLOCKER 回第4步)
    Coord->>User: 8. 呈报方案 + 预审结论，请求 Human Gate #1
    User->>Coord: 9. 批准执行

    Note over Coord,GitSSH: Phase 2：单片巡航执行 (checkpoint 2 跳 / deliverable 4 跳)
    Coord->>Engs: 10. 按仓并发派发 ENG-AP / ENG-MCU 等 (4文件稀疏指针)
    Engs->>GitSSH: 11. 各自修改白名单、本地自测并 git push 候选分支
    Engs-->>Coord: 12. 返回各仓 40 位 candidate_commit
    Coord->>Gate: 13. 调用 slice_gate.py (分配全新 run_ 目录)
    Gate->>Gate: 14. 第1阶 fast_gate (<3s) + 第2阶合龙命令
    alt 切片为 checkpoint (内部检查点)
        Gate-->>Coord: 15a. 写 checkpoint_receipt 直接返回 PASSED (省去 Docker 与 Codex)
    else 切片为 deliverable (正式交付点)
        Gate->>GitSSH: 15b. qa_runner 纯 SSH 克隆远端锁定提交至只读 Docker 容器构建回归
        Gate->>Codex: 16. 传验收条款与证据路径，启动双轴冷审 (420s)
        Codex->>Codex: 17. 自行在工作区执行 ~30 次只读命令核查源码与日志
        Codex-->>Gate: 18. 输出 APPROVED (0 BLOCKER) / REJECTED / BLOCKED
        Gate-->>Coord: 19. 写 verdict.json 与 ledger.md，返回三行摘要与退出码(0/1/2)
    end
    opt 若返回 FAILED(1) 且返修 < 2 轮
        Coord->>Engs: 20. 广播失败原因与证据链接给全部 subtasks 返修 (回第11步)
    end
```

---

## 三、架构拍板参考：`project-control` 实战得失对照表

对照上面的流转图，可以把 `project-control` 的机制清晰拆为**“千锤百炼必须保留的护栏”**和**“造成拖慢与高成本的摩擦点”**两列，方便您逐项拍板：

| 环节 | `project-control` 验证成功的精华（建议保留） | `project-control` 暴露的摩擦点（建议在 `ai-team-mvp` 改进） |
| :--- | :--- | :--- |
| **1. 规划期 (Phase 1)** | 同一份方案原地迭代（禁碎片草稿）；送人类审批前先过一次独立 Codex 预审拦客观漏项；目标明确的小修跳过 PM 直拉 ARCH。 | **PM 传声筒跳数**：新需求固定 `User ↔ COORD ↔ PM ↔ COORD ↔ ARCH` 多轮中转；其实主会话 `COORD` 直接与用户把场景问清，再一次拉起 `ARCH` 出方案更短平快。 |
| **2. 角色与写仓切分** | `COORD` 对业务仓严格只读；双 Bootloader 禁写 `main` 分支硬红线；稀疏四文件指针传参不贴聊天历史。 | **片内按仓拆人 + 巨型切片**：一片塞 5 个功能改 31 个文件（如 `SLICE-09`），且片内拆给 `ENG-AP`/`ENG-MCU`/`ENG_BOOT` 并发盲写，合龙挂了向全员广播返修（磨到 18 轮）。**改为“≤300 行薄片 + 1 个 `Eng` 跨仓贯穿整片”可根治。** |
| **3. 本地工作区隔离** | 根仓 `.gitignore` 忽略子仓，禁止使用 Git submodule；Git 调用剥离父仓环境变量并禁交互提示。 | **无切片级 Worktree**：各 `ENG-*` 直接在共享主目录改代码并被强制先 `git push` 到远端服务器才能跑第 3 阶容器 QA（导致 `P-01` 频繁停下找人要 push 权限）。**改为本地镜像派发隔离 Worktree，全部验完再统一推远端更顺畅。** |
| **4. 门禁漏斗设计** | **`<3s` `fast_gate` 前置反造假** + **`checkpoint / deliverable` 分流** + **三态退出码 (`0/1/2`) `BLOCKED` 零扣返修额度** + **同输入指纹缓存复用 (`try_reuse_qa`)**。 | **Codex 漫游全仓烧 Token**：第 4 阶只传路径和 SHA，让 Codex 自己跑 30+ 次命令读整份长方案与大日志（单轮 50 万+ Token、易超时）。**改为引擎预生成含精确 `git diff` 的精简评审包，可将冷审缩至几万 Token。** |
| **5. 远端同步与交接** | **彻底去除 GitLab HTTP API / Token**，全靠纯 Git/SSH 直连 + `git ls-remote` 读回校验；禁止收据“自指当前仓 Commit SHA”；`0 BLOCKER` 强制放行并将 `MINOR` 记技术债表。 | **临时树散落根目录**：构建中间树曾以 `.slice-08-*.tmp` 散落在控制仓根下占 25 GiB。**统一收口到 `runtime/<req>/` 并在准出后自动回收即可解决。** |
