---
name: two-axis-qa-audit
description: "AI SoC V2 独立异构 QA 双轴分级冷审技能：面向 Codex 只读审阅席位，围绕『Spec覆盖与防伪真实性』及『嵌入式安全与Diff预算』双轴输出 BLOCKER / MINOR / NIT 分级裁决。"
---

# 独立 QA 双轴分级冷审规范 (`two-axis-qa-audit`)

本技能定义 `QA`（独立只读 Codex 会话，`gpt-6-luna`）对垂直切片候选的双轴审查标准。行长、参数个数与契约宏对齐已由前置 `fast_gate.py` 机械拦截，审阅者聚焦深层语义与系统风险。

## 双轴独立审计清单

### 轴 1：Spec 覆盖与全链路防伪真实性 (`spec_realism`)
1. **端到端契约闭环**：核对各子仓改动是否真正接通切片声明的 `Consumes / Produces`，正例与异常/超时负例是否成对覆盖。
2. **零造假一票否决**：
   - 严查网关/状态层硬编码假状态（如固定 `is_homed = true`、本地定时器空跑推进进度）；
   - 严查联调桥或测试夹具篡改协议帧字节（Shim）或用 `ctypes` 后门注入假固件日志；
   - 严查中继节点私自解包转译旧文本协议（G-code）、伪造下游 ACK 或生产代码 0 调用悬空函数。

### 轴 2：嵌入式安全、通信闭环与 Diff Budget (`embedded_safety`)
1. **资源与内存安全**：裸机与核心协议层零动态堆分配（禁 `malloc/new/std::vector`）、指针深度 $\le 2$、入口空指针守卫完备。
2. **超时与故障溯源**：硬件轮询必带超时退出；上位机凡发指令必等显式 ACK，超时与 CRC 错误日志必带 `{target_node, seq_id, elapsed_ms, error_code}`。
3. **Flash 与最小修改预算**：Bootloader 擦除 Flash 前必先完成 128B ATSG Trailer 完整性校验；存量代码（如 Marlin）改动严格控制在获批 `diff_budget` 内。

## 三级判定铁律（`BLOCKER / MINOR / NIT`）
- **`BLOCKER`**：仅限违反验收条款、功能断链、假状态/Mock 作弊、安全/死锁风险或越界修改 $\rightarrow$ 必须判 `REJECTED`。
- **`MINOR` / `NIT`**：非阻断可维护性或注释优化 $\rightarrow$ `0 BLOCKER` 时必须判 `APPROVED`，由 `slice_gate.py` 自动记入 `slices/ledger.md` 技术债表，严禁因 `MINOR/NIT` 卡死批次巡航。

## 目标平台审阅范围

核对host-software/c308l-app/c308l-system的准确覆盖、SDK产品锁与PC/agents候选。ARM ABI、加载器和递归库依赖、安装树权限与来源、镜像内容均按实际交付核验。SDK从锁恢复或来自受控只读制品，禁止挂载开发者SDK。源码和平台配置只读审阅，不直接操作硬件；软件批准不能升级为HIL。
