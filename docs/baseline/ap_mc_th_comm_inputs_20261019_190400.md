# AP-MC-TH 通信任务输入资料

**整理日期：** 2026-10-19（北京时间）
**用途：** 为“实现 AP-MC-TH 基本通信并测量通信时间”登记可用输入、证据边界和待决差异。本文是输入整理，不是新协议批准或硬件验收记录。

**持续登记入口：** 后续协议原稿放入[协议资料目录](../specs/README.md)并在本文登记来源；当前串口信息统一维护在[串口链路登记](serial_links.md)。下文串口表保留为本次阅读时的输入快照，不作为另一份持续维护的当前配置。

**2026-10-19 用户确认更新：** AP 接 MC USART2 PA2/PA3、115200 8N1，替代原迪文屏；原屏不再连接此串口。MC USART6 PA4/PA5↔TH USART1 PB6/PB7、921600 8N1；均无硬件流控。MC USART1 是此前的候选假设，不是本轮 AP 入口。USART2 的源码参数匹配，但当前 DGUS 收发/解析仍须在后续固件任务迁移。详见串口登记，不重复要求用户提供这些参数。

## 结论

`/mnt/d/AI_RDdocs` 有值得纳入本任务的协议草案、评审、串口测试计划和硬件拓扑资料。它们不能整体视为现行规范：不同版本互不兼容，且部分文件状态为草案或待批准。当前项目基线 D20 已选原始 `ap_mc_formal_protocol_specification_baseline.md` 作为工作依据，并明确它尚未冻结或通过验收；v1.1 仅作参考，不覆盖 D20。

当前代码能证明 MC 有面向 TH 的 USART6 转发配置，TH 有 USART1 接收实现；不能证明从 VMware AP 发起请求后，MC 会将完整请求交给 TH 并把 TH 应答原路返回。现有普通命令路径是 Marlin/G-code 文本转发；MC 的 `5A A5` 二进制帧属于升级通道，TH 的 `SOH/EOT` 解析代码也不能直接当作已接受的业务协议。

## 当前可用输入

| 主题 | 已有证据 | 可用于本任务的内容 | 限制 |
| --- | --- | --- | --- |
| AP 运行环境 | 项目基线 D25：Ubuntu VMware 经 `ssh vmware` 使用；CH340 直通后报告为 `/dev/ttyUSB0`、115200 8N1 | 可作为主机侧 HIL 入口候选 | USB 串口实际连到哪个 MCU UART、收发线和地线映射仍需确认；这不是未来 SoC 板上的设备名或引脚规范 |
| MC 串口 | `mcu-p3/motion-controller-mcu/project/src/wk_usart.c`：USART1 PA9/PA10、115200、8N1；`project/marlin/configure.h` 选择 USART6，PA4/PA5、921600、8N1、无硬件流控 | 区分主机/调试串口和 MC↔TH 转发串口 | 源码配置不等于当前烧录固件和实物连线已核验 |
| TH 串口 | `mcu-p3/color-engine-mcu/io_toggle/src/bsp/usart.c` 使用 USART1；`io_toggle/inc/usart.h` 设 `BAUDRATE1=921600`；PB6/PB7 配置见驱动源码 | 作为 MC USART6 的目标端候选 | 代码里的 `USART1_LOOPBACK_TEST_ENABLE` 设为 1，但主循环调用目前注释；实际运行模式须以当前固件和实测为准 |
| 现有应用路径 | MC `Marlin_main.c` 对普通命令调用 `forward_uart_send_line(...)`；TH 应用中有 M105/M115 等命令处理 | 可研究“通过 MC 转发只读查询”的复用路径 | 返回路径、命令结束判定及 VMware 至 MC 接口尚未形成已验证的端到端闭环 |
| 测时参考 | `mc_th_usart_baudrate_921600_performance_test_implementationplan_20261014_110800.md` 提议测 RTT、吞吐、丢包、CRC 错误和溢出，样本数 500+ | 可作为测试指标清单参考 | 状态为 Pending Approval；属于计划，不是测试结果或通过标准 |

## 协议资料如何采用

| 文档 | 状态及用途 |
| --- | --- |
| `/mnt/d/AI_RDdocs/ap_mc_formal_protocol_specification_baseline.md` | D20 当前工作依据。描述 AP-MC 二进制帧、PING/PONG 和 SCM 隧道命令；隧道内 TH 业务负载仍未定义。按既有评审修复前不可当作冻结契约。 |
| `/mnt/d/AI_RDdocs/AI_SoC_协作方案/formal_protocol_review_20261009_210204.md` | D20 评审指出遥测长度与字段合计不符、CRC 表/向量错误、状态机及序号/重试规则不完整、隧道负载未定义等 P0 问题；评审没有编译固件或进行 HIL。 |
| `/mnt/d/AI_RDdocs/AI_SoC_协作方案/ap_mc_formal_protocol_v1_1_20261009_223404.md` | 明确标为 reference-only；依 D20 不采用其 16 字节前缀或迁移步骤。 |
| `/mnt/d/AI_RDdocs/ap_mc_formal_protocol_v1_2_specification_and_verification_20261009_093000.md` | 另一套 7 字节头/8 位序号方案，与 D20 帧布局不兼容；未见其被项目基线采纳。 |
| `/mnt/d/AI_RDdocs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md` | 后续多设备路由草案，12 字节头、含源/目的地址，且面向整网 OTA；文件说明尚未编码，不能据此替换 D20。 |
| `/mnt/d/AI_RDdocs/app_test_usart6_th_comm_implementationplan_20261010_151500.md` | Pending Approval 的旧测试计划，使用 115200 并以升级握手探测 TH；与当前源码 921600 和普通只读业务查询目标均有差异。 |
| `/mnt/d/AI_RDdocs/c308l_ap_mc_uart_pinmux_migration_20260921_201240.md` | 产品 AP↔MC 硬件设计资料列出 1.5/3 Mbps、RTS/CTS 等方案；与当前 VMware USB-串口 HIL 接入不同，需分别记录，不能混为同一物理链路。 |

## 测量建议

建议定义一次事务为 AP 发出完整请求，到 AP 收到并校验完整、匹配的 TH 响应。主指标记录端到端 RTT；MC 同时记录收到 AP 请求、发出 TH 请求、收到 TH 响应、发出 AP 响应的时间戳，以区分两段链路与转发开销。用单调时钟计时，并报告样本数、p50/p95/p99/最大值、超时、无效响应和丢包；先采基线，不先杜撰硬性时限。

8N1 串口每字节至少在线路上消耗 10 bit：115200 baud 约 86.8 µs/字节，921600 baud 约 10.85 µs/字节。实际 RTT 还包含请求/响应长度、MC/TH 处理、排队和 VMware/Linux 调度，不应把波特率换算当作完整通信时延。外部计划提出 500+ 次测试和零丢包/错误/溢出的目标，可作为候选验收项，待确认后再纳入正式门槛。

## 建议的首轮闭环与待确认事项

推荐先做一个只读 TH 状态查询，经 MC 转发并原路返回；若当前 TH 的 M105 行为和返回路径可实证，则可用它作为业务事务。此测试应分别记录端到端 RTT 与 MC↔TH 段时延。若目标是验证 D20 二进制协议，则先修复并接受其 P0 契约问题，再定义 AP 请求如何映射到 TH 业务操作；PING/PONG 单测不能替代 TH 端到端查询。

1. **首轮测量的事务：** 采用“TH 只读状态查询（如 M105），经 MC 返回”，还是先测 D20 PING/PONG？建议前者作为业务闭环，PING/PONG 作为传输层单测。
2. **USB 串口接法已确认：** 用户提供 AP `/dev/ttyUSB0` 接 MC USART2（PA2 TX/PA3 RX），115200 8N1、无流控，并明确替代原迪文屏。当前源码的 DGUS 处理尚待迁移；后续核验固件和真实通信，不再询问用户选择 USART1 还是 USART2。
3. **时延验收门槛：** 第一轮是否先只交付分布统计和错误率基线，拿到数据后再定最大 RTT？若已有指定最大时延/样本数，请提供目标。

## 资料边界与整理范围

本次从 `/mnt/d/AI_RDdocs` 的约 687 个可见文件中按协议、串口性能、AP↔MC 硬件和协作评审主题筛选上述材料，并对照当前工作区的 B0 基线、MC/TH 源码及任务卡。外部资料只读；未复制整库、未更改外部文件，也未把草案、计划或代码注释提升为已验收事实。
