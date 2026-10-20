# MiniMCProto v2.0 采用与独立项目登记

## 用户决定与本地原件

2026-10-20 用户明确“通信采用这个”，指定 `D:\AI_RDdocs\ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md`，并要求复制到当前项目对应目录；独立项目应脱离该知识库直接使用，知识库仅提供参考输入。

本决定更新 [B0 D20](../baseline/B0_方案基线.md)：通信工作以本地 **MiniMCProto v2.0 / Rev 2.0.3** 为依据，旧 D20 原稿、v1.1、v1.2 不再作为当前协议实现依据。选择协议与代码实现、独立评审和硬件验收分别记录，本次没有宣布通信已接通。

| 项目 | 登记 |
| --- | --- |
| 源文件 | 上述用户指定的 Windows 知识库文件；本次只读该文件，不改知识库 |
| 本次复制读取路径 | `/mnt/d/AI_RDdocs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` |
| 项目内协议原件 | [ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md](ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md) |
| 正文身份 | `SPEC-PROTO-20261015-153000`，`Rev 2.0.3 - Active Master Baseline` |
| 字节数 | 55301 |
| SHA256 | `9f8d4f9607cb3e76cc30b9ee2f971b23c3e0d936611188466a71f4aa15f3ce54` |
| 复制结果 | `cp` 后源文件和项目副本 SHA256 相同；正文未经改写 |
| 后续更新 | 本地副本独立版本管理，不自动从知识库刷新；协议变更在本项目登记与评审 |

## 协议与当前工程的关系

本地原稿定义 12 字节头、`L+14` 总帧长、最大 1024 字节载荷、CRC-16/CCITT-FALSE，以及 AP `0x01`、MC `0x02`、SCM/TH `0x03` 的端到端路由。MC 转发时保留业务 seq，递减 hop、置 routed 并重算 CRC。GET_VERSION / VERSION_REPORT、PING / PONG、OTA 等均使用该统一格式，不将旧文本 G-code 或旧升级二进制通道当作 v2.0 实现。

当前物理链路继续使用用户已确认配置：AP `/dev/ttyUSB0` ↔ MC USART2 PA2/PA3，115200 8N1；MC USART6 PA4/PA5 ↔ TH USART1 PB6/PB7，921600 8N1；两段无硬件流控，AP 替代旧屏。协议地址路由不改变实物引脚。工程实际缺口见 [MS-01 源核验](../baseline/ms01_source_inventory_20261020.md)：USART2 仍为 DGUS 处理，两端尚无已验证的 v2.0 栈。

原稿描述 OTA 为其第一阶段重点；本次完成协议接收和采用，不等于已实现 OTA 或安排烧录。当前工程的最小通信与测时任务应据此细化，实际升级实施另按任务/硬件范围执行。

已发现原稿内部一处需要在相应实现前核对：§5.1 / §5.2 将急停载荷规定为 2 字节，§7 V04 却给出 `L=0`、14 字节帧。本次保留原文与问题，不擅改副本或据此实现物理急停。原文“评审问题已闭环”的陈述也不替代当前项目的实际检查结论。

## 项目内阅读入口

原文 Obsidian 回链只保留出处，不要求访问知识库。当前可直接使用：

| 内容 | 项目内位置 |
| --- | --- |
| 用户决定与协议切换 | [B0](../baseline/B0_方案基线.md) |
| 串口目标与证据状态 | [串口登记](../baseline/serial_links.md) |
| 准确代码与制品/构建入口 | [集成清单](../../manifest.yaml)、[工程登记](../baseline/ms01_source_inventory_20261020.md) |
| 当前任务与具体范围 | [主看板](../../.agents/kanban/KANBAN.md)及其本地任务卡 |
| 接口/证据变更规则 | [公共看板与读写协议](../../.agents/rules/04_公共看板与读写协议.md) |
| 离开知识库后的使用方法 | [独立工作区说明](../guides/standalone_workspace.md) |

其他旧回链所指的报告/评审是历史参考，没有在本次选择中变成额外运行依赖；需要新增事实或测试预期时，在本项目内产生并留存准确版本，不回到知识库维护唯一原件。
