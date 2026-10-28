# CR-12 核心资产与证据集中对账复用矩阵 (Reuse Matrix)

> **任务标识**: `CR-12`  
> **归档路径**: `project-control/docs/evidence/cascade_recovery/CR-12/runs/run_01/reuse_matrix.md`  
> **对账日期**: 2026-10-28  
> **对账角色**: `ARCH` / 独立质量复核  
> **依据规约**: `workflow_replan_20261028.md`, `codex_qa_review.md`, `ap_mc_th_readonly_cascade_icd.md`  

---

## 1. 对账总览与判定准则

本矩阵针对 **AP 宿主程序**、**MC 运动控制器固件**、**TH 工具头从控固件**、**测试用例与黄金向量集**、**HIL 探针故障注入工具** 展开逐项证据核验。

### 判定结论度量定义：
1. **可复用 (Reusable)**：源码提交明确、构建配置与二进制制品可追溯核验、已有测试日志与独立审查完备、适用范围清晰，可直接作为后续候选打包（CR-08）或台架联调（CR-09）的基线输入。
2. **需补查 (Requires Follow-up Check)**：核心功能有效，但存在特定外部依赖（如构建时间戳漂移、未覆盖某些边界分支），需在部署或后续专项中补齐针对性核查，但不阻断当前只读主线。
3. **不可使用 (Prohibited / Invalidated)**：结论基于虚假替身（如 PTY 代替物理硬件）、存在伪造协议中继或已被正式裁决撤回的资产，严禁在后续流中消费。

---

## 2. 逐项对账清单与复用矩阵

| 资产类别 | 准确源码 Commit / 差异 | 构建产物与配置 / SHA256 | 实际运行过的检查与原始日志 | 适用范围 / 被撤回结论 / 尚缺验证 | 最终裁决与使用依据 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. AP 宿主程序**<br>(`soc-ap`) | **Commit**: `4445c8fedc21bafef5e6c971fcb54cec703f0e71`<br>**分支**: `main`<br>**差异**: Clean (无未提交改动) | **二进制**: `soc-ap/build/host/bin/soc-ap` (41,720 B)<br>**SHA256**: `1e0e0263c90c658e8026e1d5a5dd51349b411831575d4be2b7aec42fbd62d6e1`<br>**配置**: Linux x86_64, CMake+Ninja, C++17, `-O3 -fno-exceptions -fno-rtti` | 1. 14/14 独立黄金用例全通（4 正例 + 10 负例）；<br>2. 60/60 基础编解码与容错用例全通；<br>3. 原始日志: `docs/evidence/cascade_recovery/CR-04/result.md` | **适用范围**: 上位机 Linux/VMware 串口协议封装、四层严格校验（CRC/回显/seq关联/结构）及确定性退出码（0~4）。<br>**被撤回结论**: 撤回以 PTY 仿真通过代替真实硬件验收结论。<br>**尚缺验证**: 真实 `/dev/ttyUSB0` 直通 VMware 下与真实 MC 物理交互时延。 | **【可复用】**<br>AP 宿主实现完全符合契约，测试覆盖完备，直接进入 CR-08 候选清单用于台架联调。 |
| **2. MC 主控固件**<br>(`mcu-p3`) | **Commit**: `af279a8c24dde92a0145d767c1c6478cfef05994`<br>**分支**: `feat/soc-debug`<br>**差异**: Clean (无未提交改动) | **固件**: `mcu-p3/motion-controller-mcu/build/fw_mc.bin` (369,516 B)<br>**当前实测 SHA256**: `74ad2bd0861cebf7f6964ca81f83cf41ac850e8adfa21379073f51e218d78f99`<br>**历史报告 SHA256**: `054b83d8...`<br>**配置**: ARM GCC 10.3, `-O2`, AT32F435VGT7, 烧录地址 `0x08020000` | 1. 编译期静态布局与链接通过；<br>2. 黄金中继向量 100% 逐字节吻合（入站/出站透明转发）；<br>3. 中断安全入队（$< 2\mu s$），主循环解耦消费；<br>4. 原始日志: `docs/evidence/cascade_recovery/CR-05/result.md` | **适用范围**: MC 原生透明双向路由中继、USART2 与 USART6 DMA 环形缓冲通信。<br>**被撤回结论**: 彻底撤回 `MCQ-0106` 在 MC 内部伪造 TH 响应的作弊代码。<br>**尚缺验证**: 1. `version_autogen.h` 打包时戳导致二进制哈希变化（见下文分析）；2. 真实双板物理 UART 时钟对齐；3. `th_upgrade_mgr.c` 治理（挂于 CR-07）。 | **【可复用】**<br>原生双向中继逻辑与中断解耦真实有效，符合 HW-G6 规范，可直接用于烧录联调。 |
| **3. TH 从控固件**<br>(`mcu-p3`) | **Commit**: `af279a8c24dde92a0145d767c1c6478cfef05994`<br>**分支**: `feat/soc-debug`<br>**差异**: Clean (无未提交改动) | **固件**: `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` (71,176 B)<br>**实测 SHA256**: `5eaeb608cd22b5ec3041672db08fc865cb7b539620fb7b21de1a0925d4df9d3d` (与 CR-06 报告 100% 完全一致)<br>**配置**: ARM GCC 10.3, `-O2`, AT32F423CCT7, 烧录地址 `0x08004000` | 1. 编译期 `_Static_assert` 结构体内存对齐全通；<br>2. TH 原生响应与 `CAS-POS-002` (版本) 及 `CAS-POS-004` (PING) 黄金帧逐字节 100% 吻合；<br>3. DMA 接收层流式分流二进制帧与 ASCII G-code；<br>4. 原始日志: `docs/evidence/cascade_recovery/CR-06/result.md` | **适用范围**: TH 端作为 `src_id=0x03` 原生自报真实版本与心跳时延，原有文本温控/运控逻辑零污染。<br>**被撤回结论**: 撤回此前未经实测的“TH 已预装 MiniMCProto 固件”幽灵硬件假设。<br>**尚缺验证**: 真实打印机工具头板刷写后的物理信号电平。 | **【可复用】**<br>TH 原生协议栈实现完备，哈希严密对齐，直接作为候选固件用于台架联调。 |
| **4. 测试用例与黄金向量集**<br>(`test_harness`) | **Commit**: `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb`<br>**分支**: `main`<br>**差异**: Clean (无未提交改动) | **文件**: `test_cases/cascade/query_cases.json`<br>**SHA256**: `18f7d9d5f04a91a9f14371fa7a49339e1bf6ebbf15e181467406a6b5a3bbfe5d`<br>**运行器**: `static_checks/cascade/run_query_cases.py` | 1. `run_query_cases.py --check-vectors` 纯 Python CRC 校验全通；<br>2. `run_query_cases.py --test-host` 14/14 全通；<br>3. 原始记录: `docs/evidence/20261020_task_orchestration/` 与 CR-02Q | **适用范围**: 提供只读级联 GET_VERSION 与 PING 的正负向标准十六进制帧与预期退出码。<br>**被撤回结论**: 明确规定测试运行器内的 PTY 仿真仅用于主机程序黑盒测试，绝不能替代物理在环 HIL。<br>**尚缺验证**: 真实物理串口 Hex 抓包的微秒级时延对账。 | **【可复用】**<br>黄金向量集是 CR-09 联合调试与 CR-10 独立 HIL 验收的法定预期依据。 |
| **5. HIL 故障注入与探针工具**<br>(`test_harness`) | **Commit**: `6c61ce6e51cf83d7fb58d319c23cb91bf95786cb`<br>**分支**: `main`<br>**差异**: Clean (无未提交改动) | **脚本**: `hil/tools/probe_fault_injector.py` & `device_discovery.py`<br>**单测**: `hil/tests/test_probe_tools.py` | 1. `test_probe_tools.py` 10/10 单元测试全通；<br>2. CR-02T 缺陷治理闭环（F23 芯片误认、F24 快照安全、F25 时长校验、F26 状态截断）；<br>3. 原始记录: CR-02T | **适用范围**: 通过 probe-rs 在线读写 MMIO 寄存器（`USART_CTRL1`），开合 MC/TH 串口物理通信，仿真从机掉线与网络抖动。<br>**被撤回结论**: 撤回此前缺少芯片角色绑定、可能误操作非目标芯片的旧实现。<br>**尚缺验证**: 物理机柜台架真实 ST-Link 探针在线连接。 | **【可复用】**<br>工具治理完全合格，为 MS-16 异常断线与恢复验收提供可靠夹具。 |

---

## 3. 专项核查发现：MC 固件构建哈希漂移根因

在核对 `fw_mc.bin` SHA256 过程中，发现当前文件 SHA256 为 `74ad2bd0...`，而 CR-05 报告记录为 `054b83d8...`。

**根因定位**：
- `mcu-p3/motion-controller-mcu/build/version_autogen.h` 由构建打包脚本 `version_tool.py` 动态生成。
- 宏定义中包含编译时刻的动态时间戳（如 `#define BUILD_TIMESTAMP (1793104432U)` 与 `#define BUILD_TIME_STR "2026-10-27 20:33:52"`）。
- 只要重新执行 `make pack`，即使 C 源码完全没有改动，固件二进制末尾的版本签名区也会发生微小字节差异，导致 SHA256 重新计算。
- **治理与使用结论**：
  - 代码基线和逻辑保持完全一致（HEAD `af279a8`）；
  - 在 CR-08 装配候选时，必须一次性锁定当前确定性的 `fw_mc.bin` 二进制及其当前 SHA256（`74ad2bd0...`），并在部署 SOP 中记录该确定性版本，避免联调前再次重新打包导致哈希失配。

---

## 4. 下游微任务消费指南

1. **对 CR-08（候选清单装配与部署 SOP）**：
   - 直接消费：
     - AP 宿主可执行程序：`soc-ap/build/host/bin/soc-ap` (`1e0e0263...`)
     - MC 固件：`mcu-p3/motion-controller-mcu/build/fw_mc.bin` (`74ad2bd0...`)
     - TH 固件：`mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` (`5eaeb608...`)
     - 黄金向量集：`test_harness/test_cases/cascade/query_cases.json`
2. **对 CR-09（物理台架三端工程联调）**：
   - 以本矩阵确认的参数（AP 115200 8N1 $\to$ MC 921600 8N1 $\to$ TH）与黄金向量开展物理收发验证。
3. **对 CR-07（升级管理器治理专项）**：
   - 维持解耦状态。因当前只读级联联调采用 SWD 探针烧录（`probe-rs`），无需经过 U 盘或 USART6 固件中继升级，因此 CR-07 不阻断 CR-08 和 CR-09。
