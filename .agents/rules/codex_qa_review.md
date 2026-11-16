---
title: V2 独立异构 Codex 双轴分级冷审与 HIL 物证审计规则
status: current-rule
owner: COORD
effective_date: 2026-10-26
updated: '2026-11-14'
plan_revision: v2-two-axis-graded-codex
---

# 独立 QA 统一使用异构 Codex 双轴分级冷审

## C308L 候选与覆盖范围

独立 QA 的输入包含 `printer-soc`、必要 SDK 项目/产品锁、PC、agents 和测试资产的准确候选；三种构建 profile 单独报告实际覆盖。正式 QA 由准确锁恢复 SDK，或消费完整来源可核验的受控只读 SDK 制品；禁止直接挂载开发者 SDK。ARM ELF 的交叉编译不能当成 x86 容器执行成功，系统镜像生成不能当成目标板启动成功。

HIL 按被验证能力取证：真实入口可以是 Helix、IPC 或 API；UART 取板级描述，当前 C308L 为 `/dev/ttyS1`。身份查询不要求虚构运动证据；相机、存储、运动及 OTA 分别取相应物理事实。缺少环境不消耗作者代码返修轮次，未推送候选不能冒充服务端正式 QA 通过。

本规则定义 V2 垂直切片（`SLICE-XX`）的正式独立 QA 审阅标准，由 `project-control/tools/gates/codex_review.py` 与 `slice_gate.py` 机械执行。历史已完成报告保留原签署与原结论不改写。

## 1. 独立会话与物理隔离红线

1. **异构独立只读会话**：正式代码与物证审查必须通过本机 `/home/sushaohua/.local/bin/codex` 启动全新独立会话（默认模型 `gpt-6-luna`，强制参数 `--sandbox read-only -c approval_policy="never" --json --output-schema`），从 JSONL 事件流提取真实 `thread.started` 会话 UUID 与真实 Token 消耗。禁止使用同源 `invoke_subagent` 普通子 Agent 冒充独立 Codex QA，禁止记录或提交任何 API 密钥/凭据。
2. **前置机械过滤原则**：只有当切片已通过 `fast_gate.py`（`<3s` 机械规范/契约/反假状态检查）及跨仓合龙、且具备客观构建测试证据（`qa_runner.py` 产出的 `server_qa.json`）后，才允许调用 Codex，杜绝用高成本冷审挑低级格式问题。
3. **执行层与审计层解耦**：Docker 构建测试由 `qa_runner.py` 执行，真机 HIL 由受控台架脚本或 `INTEGRATOR` 执行并固化原始物证；Codex 审阅席位严禁依赖直连宿主机 USB 硬件，专注对锁定 Commit、Diff、契约真源与物证哈希链进行防伪审计。

## 2. 双轴审查维度与三级判定标准（`BLOCKER / MINOR / NIT`）

单轮 Codex 审查同时覆盖以下两个正交审计轴，并对每条发现标注精确严重度：

- **轴 1：Spec 覆盖与全链路防伪真实性（`spec_realism`）**
  - 核对实现是否完整闭环切片声明的 `Consumes / Produces` 与正负验收判据；
  - 严查内存假状态、开环本地定时器推进进度、篡改报文字节的测试桥（Shim）、`ctypes` 后门伪日志、中继私自降级转译 G-code 或 0 调用悬空函数。
- **轴 2：嵌入式安全、通信闭环与 Diff Budget（`embedded_safety`）**
  - 核查动态堆分配、指针越界/多重指针、无超时死循环轮询、指令下发无 ACK 超时冒泡、错误日志缺 `{target_node, seq_id, elapsed_ms, error_code}`、未验签擦除 Flash 及超出获批 **Diff Budget** 的无关重构。

### 严重度分级与放行刚性约束

| 级别 | 判定标准 | 门禁动作（由 `codex_review.py` 强制校验） |
| :--- | :--- | :--- |
| **`BLOCKER`** | 违反契约/验收条款、功能未闭环、存在假状态/Mock 作弊、内存/硬件/Flash 安全缺陷、通信无超时闭环或越界改动 | **一票否决（`decision = REJECTED`）**；退回原 `ENG-*` 保活会话定向修复（上限 2 轮，超限熔断） |
| **`MINOR`** | 局部可维护性改进、非热路径冗余、不影响契约与安全的边界注释优化 | **不阻断放行（`0 BLOCKER` 即 `APPROVED`）**；自动摘录写入 `slices/ledger.md` 技术债表后续收敛 |
| **`NIT`** | 纯命名风格或排版偏好 | 仅记录参考，不阻断、不计入返修轮次 |
| **环境缺口** | 沙箱物证缺失、哈希不匹配或远端不可达导致无法核验 | 判定 **`BLOCKED`**，交 `COORD` 排查环境，不计入作者代码返修轮次 |

## 3. 真机 HIL 物证链审计底线（HW-G5 / HW-G6 / HW-G7）

针对升级 `HIL-Verified` 的批次里程碑审计，Codex 必须逐节点核验：
1. **真实固件身份链（HW-G7）**：各受测节点（AP / MC / TH / Bootloader）的 40 位源码 Commit、构建制品 SHA256、烧录/OTA 记录与现场协议读回版本自洽（禁止仅凭硬编码常量判通过）。
2. **原始双向报文对账（HW-G5/G6）**：具备 板级描述指定的真实 UART（当前 `/dev/ttyS1`） 真实波特率、毫秒级时间戳及逐帧 `Raw Hex TX / RX` 对账记录；有效协议关联回包数为 0 或以 PTY/Mock 替身采证的一律判 `REJECTED`。
