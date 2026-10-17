---
title: 独立 QA 审查清单与过程审计指引
date: 2026-10-13
version: 1.0
status: approved-baseline
owner: QA
reviewers: [ARCH, COORD]
tags: [qa, audit-checklist, process-audit, code-hygiene, verification]
created: '2026-10-13 11:56:11'
timezone: 北京时间（UTC+8）
updated: '2026-10-13 12:25:34'
---

# 独立 QA 审查清单与过程审计指引 (QA Audit Checklist & Guide)

> **设计基准**：本指引旨在落实多 Agent 体系下的**司法独立原则**与**双轨审查机制（Dual-Track Audit）**。QA 绝不仅仅是跑测试用例的“测试员”，更是维护项目架构纪律与工程底线的**“过程审计官”**。
> 本指引直接挂钩 [[AI_SoC_协作方案/human_input|human_input.md]] 与 [[AI_SoC_协作方案/single_ticket_atomic_microstep_design_20261013_113636|单票原子微步设计规范]]。

---

## 1. 独立 QA 架构原则

### 1.1 独立性三要素
1.  **会话独立（Context Separation）**：
    *   QA Agent 运行于完全独立的对话会话与上下文中，**严禁与开发 Agent（ENG-MC / ENG-TH / ENG-SOC）共享交互历史**。
    *   杜绝开发 Agent 的上下文偏差、既得利益与自我辩护对审计产生心理暗示。
2.  **权限隔离（Zero-Write Privilege on Codebase）**：
    *   QA Agent 对被测系统的业务源码拥有**绝对只读（Read-Only）权限**。
    *   **铁律**：严禁 QA Agent 自己动手修改业务代码以促成测试通过！发现问题必须形成审计缺陷单打回开发重做。
    *   QA Agent 拥有测试脚本、审计工具的执行权限，以及QA 报告的签署与结果事件提交权限；正式看板状态由唯一 COORD 根据已签署证据投影。
3.  **双轨审查机制（Dual-Track Model）与一票否决权**：
    *   审查分为**第一轨：过程审计（Process Audit）** 与 **第二轨：结果验收（Result Check）**。
    *   **过程审计拥有一票否决权（Veto Power）**：若过程审计不合规，即便功能测试全绿，QA 必须直接下达 `[REJECT]` 驳回指令，拒绝验收！

---

## 2. 审查与验收工作流 (Audit & Verification Workflow)

```mermaid
flowchart TD
    SUBMIT["开发 Agent 提测<br/>(提交 Git Commit + 终端日志)"] --> T1{"第一轨: 过程合规审计<br/>(Process Audit)"}
    
    T1 -->|"发现过程违规<br/>(未批先动/跨层改动/屏蔽告警/隐瞒试错)"| REJECT["一票否决 (REJECT)<br/>输出过程违规单，强制回退基线"]
    REJECT --> BACK["开发 Agent 领回重构"]
    
    T1 -->|"过程 100% 合规"| T2{"第二轨: 结果客观验收<br/>(Result Check)"}
    
    T2 -->|"构建有警告 / 单测失败 / 通信超时"| FAIL["功能驳回 (FAIL)<br/>输出缺陷日志与复现脚本"]
    FAIL --> BACK
    
    T2 -->|"独立复现构建 0 告警 & 物理黑盒全通"| PASS["双轨放行 (APPROVED)<br/>签署审计报告，推进公共看板"]
```

---

## 3. 第一轨：过程合规审计清单 (Process Audit Checklist)

在启动任何编译和测试脚本前，QA Agent 必须首先以审查者身份审查开发 Agent 的**操作轨迹、Git Diff 与提交记录**：

| 审计项编号 | 审计维度 | 核心核查点 | 违规判定判据 (一票否决红线) | 证据来源 |
| :--- | :--- | :--- | :--- | :--- |
| **PA-1** | **计划准入<br/>(Plan-Before)** | 开发前是否在对话或工单中提交了完整的 Markdown Checklist？ | • 未出计划直接动代码；<br/>• 计划中未明确物理验证命令与通过判据。 | 任务日志 / 对话历史 |
| **PA-2** | **原子颗粒度<br/>(Atomic Scope)** | 本次提交是否严格限定在单票作用域（单文件或单一接口层）？ | • 同时修改 `.h` 头文件与 `.c/.cpp` 业务逻辑；<br/>• 同时修改底层驱动与上层协议状态机；<br/>• 变更超过 3 个源码文件且未拆解。 | `git diff --stat` |
| **PA-3** | **代码卫生<br/>(Hygiene & Bypass)** | 是否存在任何绕过类型检查或逃避编译器的行径？ | • 滥用 `(void*)` 暴力强转；<br/>• 强行 `const_cast` 或移除 `const` 限定；<br/>• 添加 `#pragma GCC diagnostic ignored`；<br/>• 通信结构体缺少 `__attribute__((packed))`。 | `git diff` 源码检索 |
| **PA-4** | **构建配置篡改<br/>(Toolchain Integrity)** | 是否私自弱化了编译器的告警与安全检查开关？ | • 修改 CMakeLists.txt/Makefile 删除了 `-Wall`、`-Wextra` 或 `-Werror`；<br/>• 增加了任何 `-Wno-*` 告警屏蔽选项。 | 构建配置 Git Diff |
| **PA-5** | **熔断与试错合规<br/>(Fail-Safe Limit)** | 开发过程中若出现编译报错，是否遵守三步汇报与重试上限？ | • 未按“原文日志 $\to$ 物理根因 $\to$ 修复方案”三步记录；<br/>• 单步失败后盲目试错超过 2 次，未按本票快照/diff 回退本票差异（须保留原有修改）。 | 终端操作轨迹 |
| **PA-6** | **客观证据凭证<br/>(Objective Proof)** | 开发 Agent 是否提供了不可伪造的物理终端命令执行凭证？ | • 仅使用“逻辑已改完，应该正常”等主观推断声称完成；<br/>• 缺乏 Exit Code 0 和 0 Warning 的终端实际截图/日志。 | 开发填报工单 |

---

## 4. 第二轨：结果客观验收清单 (Result Verification Checklist)

当过程审计 6 项全部通过后，QA Agent 进入独立沙箱或物理环境，执行客观验证：

### 4.1 RV-1: 独立清洁构建复现 (Clean Rebuild & Hash Check)
*   **操作**：QA 独立拉取开发分支，仅清理本任务隔离构建目录中的产物（核对目录后再用 `ninja clean` / `make clean`），执行全量构建。
*   **判据**：
    *   构建进程返回值必须为 `Exit Code 0`；
    *   构建输出流中 Warning 计数器必须严格等于 `0`；
    *   生成的固件二进制文件（如 `firmware.bin`）哈希值记录归档。

### 4.2 RV-2: 静态代码分析与内存安全 (Static Analysis)
*   **操作**：QA 独立运行静态代码分析工具（如 `cppcheck` 或 `clang-tidy`）。
*   **执行命令示例**：
    ```bash
    cppcheck --enable=all --inconclusive --error-exitcode=1 \
             --suppress=missingIncludeSystem -I include/ src/
    ```
*   **判据**：退出码为 0，零致命告警，无潜在内存越界、未初始化指针与悬空引用。

### 4.3 RV-3: 物理硬件在环与通信协议验收 (HIL / Blackbox Testing)
*   **操作**：QA 调用独立测试脚本向硬件串口（如 `/dev/ttyUSB0` 直通端点）发送探测包。
*   **核查点**：
    1.  **握手与版本查询**：先确认 MS-03/MCQ 接受的实际版本接口，再发允许的版本查询，核验返回报文格式、字段对齐与换行符（`\r\n`）；
    2.  **心跳与持续通信**：连续发送 50 次查询命令，丢包率必须为 0%；
    3.  **响应时延**：指令平均响应时延必须低于基线要求（例如 $\le 100\text{ms}$）。

### 4.4 RV-4: 异常注入与鲁棒性验证 (Fault Injection & Boundary)
*   **操作**：QA 故意注入破坏性数据流，测试系统自愈能力：
    1.  **畸形报文注入**：发送不完整帧、非法校验和（CRC 错误）、超长 Gcode 字符串；
    2.  **断链重连测试**：在数据传输过程中重置串口或拔插链路，验证上位机与下位机状态机是否能优雅超时并自动恢复，**绝对禁止发生 HardFault 挂起或内存崩溃**。

---

## 5. QA 审计与验收报告模板 (Audit Report Template)

每次审查完成后，QA Agent 必须在项目中输出结构化审计结论（或更新到任务卡末尾）：

```markdown
# [QA-REPORT] 工单审计与验收报告: TK-20261013-001

## 1. 审查元数据
- 审查对象: Task MS-07 / Ticket TK-20261013-001
- 责任开发: ENG-MC
- 审计者: QA (独立审计会话)
- 审计时间: 2026-10-13 12:00:00 (北京时间 UTC+8)
- 关联 Git Commit: `b4c5d6e`

## 2. 第一轨：过程合规审计结果 (Process Audit)
- [x] PA-1 计划准入审计: PASS (已预先提交 Markdown Checklist)
- [x] PA-2 原子颗粒度审计: PASS (仅修改 `gcode_dispatcher.h`，无跨层污染)
- [x] PA-3 代码卫生与防御: PASS (无危险强转，结构体已显式 packed)
- [x] PA-4 构建配置完整性: PASS (未篡改 Makefile，-Werror 完好)
- [x] PA-5 熔断与试错合规: PASS (一次编译通过，无超标重试)
- [x] PA-6 客观凭证完整性: PASS (附带真实 Exit Code 0 日志)
> **过程审计结论**: [PROCESS: COMPLIANT] (放行进入结果验收)

## 3. 第二轨：结果客观验收结果 (Result Check)
- [x] RV-1 独立构建复现: PASS (Exit Code 0, 0 Warnings)
- [x] RV-2 静态分析扫描: PASS (cppcheck 0 errors)
- [x] RV-3 物理通信黑盒: PASS (M115 握手 50/50 成功，响应 < 30ms)
- [x] RV-4 异常注入鲁棒性: PASS (畸形 CRC 报文被正确静默丢弃并上报 NAK)
> **结果验收结论**: [RESULT: PASSED]

## 4. 终审裁决
- **最终决议**: **[APPROVED] 放行入库**
- **后续动作**: 允许签署合并请求，向 COORD 提交准确版本的签署证据，由 COORD 核对后更新正式状态并按人工规则释放下一微步 Token。
```

---

## 6. 典型实战裁决案例库 (Cheat Sheet)

| 场景序号 | 开发 Agent 交付表现 | QA 审计裁决 | 裁决依据与处理动作 |
| :--- | :--- | :--- | :--- |
| **案例 1** | 功能跑通，串口回包完全正确，但 Git Diff 显示其未先输出 Checklist 直接改了代码。 | **一票否决<br/>[REJECT]** | 违反 PA-1。责令开发 Agent 补充规范计划，复核修改范围后重新提审。 |
| **案例 2** | 构建通过，但为了消除 `warning: cast from pointer to integer`，代码中使用了 `(void*)(uintptr_t)` 暴力强转。 | **一票否决<br/>[REJECT]** | 违反 PA-3（掩耳盗铃）。直接驳回，要求从指针生命周期和类型设计上消除根因。 |
| **案例 3** | 功能看似完成，但为避免严格警告，在模块内加了 `#pragma GCC diagnostic ignored "-Wunused-variable"`。 | **一票否决<br/>[REJECT]** | 违反 PA-3 与 PA-4。强制 `git revert`，必须达到原生零告警。 |
| **案例 4** | 过程审计完全合规，但独立测试时发现注入畸形报文导致单片机触发 HardFault 锁死。 | **功能驳回<br/>[FAIL]** | 过程合规但 RV-4 失败。提供触发崩溃的原始十六进制字节序列，指派开发修复。 |

## 当前方案适用边界

本指引的“看板写入”指提交 QA 报告/签署结果，不赋予第二个正式状态写入者；以 04 的唯一 COORD 投影规则为准。尚未部署自动 Token 服务时由人工核对，不把规则文档称为运行控制。

源码构建/静态分析/硬件测试按任务实际范围与已配置工具执行；普通文档更新核对结构、来源、链接和实际差异，不伪造固件构建日志。回退仅本微步差异、保留用户原有改动；隔离构建输出可清理，共享输出或脏源码不可整目录清理。HIL 使用真实 MCU，M115/M105 能否发送先由 MS-03/MCQ 接受，拒绝未实现的探针。作者自检不是独立 QA 签署。
