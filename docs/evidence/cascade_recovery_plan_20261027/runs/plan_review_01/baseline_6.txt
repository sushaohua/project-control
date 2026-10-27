# MCU 固件、制品与升级链路独立只读缺口审查

- 日期：2026-10-27；审查角色：独立 Codex 审查会话 `/root/independent_cascade_review`。
- 范围：MC/TH 接收发送路径、MiniMCProto 适配、构建打包、现有 TH 升级管理器、Bootloader 制品与 README SOP。
- 源码基线：`mcu-p3` HEAD `a679133204ecbb81ad48694f5372c125db2e749f`。
- 先行读取：根 `AGENTS.md`、`mcu-p3/AGENTS.md`（现存软链接）、`project-control/.agents/rules/codex_qa_review.md`。
- 本报告只记录源码/文档/本地制品事实，不签署 APPROVED，不改工程文件或任务状态，不代表硬件验收。
- 未执行：编译、单测、串口打开、真实回包采集、烧录、复位、Flash 擦写、Bootloader 重建。只在 `/tmp` 写本报告。

## 1. P1：USART2 ISR 内等待同抢占优先级的 USART6，真实完成事件不能在等待期推进

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/at32f435_437_int.c:354`：`USART2_IRQHandler` 直接调用 `gui_rx_callback()`（357）。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c:417`：回调直接在 ISR 内调用 `minimc_proto_process_rx(rx_fifo, usart2_rx_len)`（436）。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:121`：`handle_th_query` 清除完成标志、发送 M115，随后忙等 200000 次，期间不调用接收推进函数。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/at32f435_437_int.c:369`：USART6 IDLE ISR 在 385 行写完成标志。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/at32f435_437_wk_config.c:258`：USART2、USART6 均配置为 `(2,0)`；同抢占优先级不能互相抢占。
- 另一个置位入口是 `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c:427` 的主循环接收轮询；它同样不能在 USART2 ISR 中执行。

**影响与证据边界**

按当前控制流，清零后的 TH 完成标志无法由上述正常入口在等待期置位；本次查询先超时，随后 USART6 才有机会执行。这是源码级执行关系推导，尚未测量硬件时序。Mock 在 send 调用内同步置位，绕过实际 NVIC 行为，不能证明此路径成立。

**建议文件与验收**

- ENG-MC：最小改动 `memu_gui.c`、`at32f435_437_int.c`、`minimc_proto.c/.h`，ISR 只收集或发布已拥有的接收块，路由/会话由主循环事件推进；去掉 ISR 内跨端等待。
- QA：增加真实中断优先级约束审查；工程联调记录 AP 请求进入、TH 回包进入、路由发出三者顺序。独立验收再执行正常、超时、并发请求与恢复。不要只调高 USART6 优先级后继续保留 ISR 业务等待。

## 2. P1：DMA 接收缓冲在消费前重新启用，长度快照与缓冲所有权不闭合

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd/memu_gui.c:424`：先算 USART2 DMA 长度；427～431 把 DMA 重置到同一 `rx_fifo` 并重新启用；436 才解析该缓冲。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/wk_dma.h:49`：USART2 环形 DMA 仅 128 字节；`wk_dma.c:262` 开启 loop mode。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/at32f435_437_int.c:375`：USART6 IDLE 先记长度、重启同一个接收缓冲，再发布完成标志；`wk_usart.c:604` 随后直接读取活动 DMA 缓冲。它没有切换到独立只读快照。

**影响与证据边界**

后续物理字节可在软件尚未消费前覆盖前一块；解析耗时越长，窗口越大。环形 DMA 仅用“容量减剩余计数”得不到已经绕过的圈数，长度为容量整倍数的连续突发尤其容易丢失信息。覆盖是否实际发生、最高可持续速率和现有板负载下概率待实机测量；源码没有保证不会覆盖。

**建议文件与验收**

- ENG-MC：`wk_dma.c/.h`、`at32f435_437_int.c`、`memu_gui.c`、`wk_usart.c` 建立统一接收所有权：双缓冲或环形生产/消费索引，消费期间不重用块；记录 DMA wrap/overrun/drop，切分与重组按协议字节流处理。
- QA：边界覆盖连续 127/128/129 字节、多帧无空闲、帧间仅一个字符空闲、慢消费者、wrap 后恢复；用 canary/接收计数对账验证缓冲生命周期，再做 HIL。测试工具不得用同步内存拷贝掩盖 DMA 竞争。

## 3. P1：当前 MCU 解析器只是局部查询适配，MTU、超时、命令和会话语义未达到正式协议

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h:23` 将 `0x03` 定义为 VERSION_GET；30 行将最大载荷设为 64。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:52` 只验证协议版本、目的地址和载荷上限；97～110 生成固定 4 字节版本载荷；144～168 按 cmd 01/03 触发查询，不验证请求/响应角色、精确命令长度或维护 peer 会话。
- 同文件 14～18 的全局状态、186～272 的 feed 路径没有时间戳、50ms 超时检查或 poll-timeout 入口；半帧可跨任意长空闲继续拼接。
- 正式原件 `/home/sushaohua/workspace/ai_soc_project/project-control/docs/specs/ap_mc_formal_protocol_v2_0_multidevice_routing_draft_20261015.md:62`：L≤1024、最大帧1038字节（72）；308～311：GET_VERSION 01→VERSION_REPORT 02，PING 03→PONG 04；363～390：版本16字节、PONG12字节；235～282：boot_id、seq、重复/过期请求；578、598：50ms 字节间超时及定时轮询。

**影响与证据边界**

64字节上限加128字节 DMA 无法承接协议最大 OTA/stream 帧；一个未结束的短帧会影响下一次请求恢复；CRC 合法并不代表命令或会话有效。当前只读查询尚未扩展到动作业务，因此不能据此宣称已经造成重复动作；应在动作/OTA接入之前补齐。若项目只交付更小子集，必须冻结明确的能力/MTU协商和不支持行为，不能把它称为完整 v2.0 合规。

**建议文件与验收**

- ARCH：接受正式命令、MTU、超时和会话子集，逐条给出落地版本；ENG-MC/TH 在各自协议实现中消费同一份已接受契约，禁止自行复制旧 cmd 定义。
- QA：独立预期验证命令/响应对、精确长度、64/65/1024/1025边界、半帧长空闲后新合法帧、旧seq/未来seq/boot_id变更、响应误当请求；结构解码工具只作为第一层检查。

## 4. P1：升级应答传入容量大于真实栈数组，并且分块 ACK 未匹配当前块号

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c:208`：handshake、send-one-chunk（251）、finish（310）均只有 `ack_payload[8]`。
- 同文件 `th_upg_wait_ack:173` 对上述输出指针固定传 `max_len=32U`。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c:621` 允许 p_len≤max_len，635～637 按 p_len 写入调用者数组。校验和正确的9～32字节响应因此可越过8字节栈数组。
- `th_upgrade_mgr.c:262` 只要求收到 ACK_TH_PUSH_CHUNK，264 行仅检验长度≥5和 `[4]==0`，不比较前4字节块号与 `chunk_idx`；迟到或重复的前一块成功 ACK 可以满足后一块等待。

**影响与证据边界**

容量不一致与块号遗漏由代码直接证实；越界触发输入条件明确，未在本轮执行攻击/故障测试。Bootloader正常ACK可能仅为1或5字节，这不能消除接收边界漏洞。旧ACK导致最终是否失败还受TH最终校验约束，不能未经实测宣称必然刷错成功。

**建议文件与验收**

- ENG-MC：`th_upgrade_mgr.c` 使用携带真实容量的应答结构体/上下文（遵守≤4参），校验每种ACK精确长度、块号、状态和本次升级会话；发送失败立即处理，等待窗口与缓存清理规则明确。
- QA：对8、9、32字节应答做独立内存边界检查，对重复、迟到、错块号、错误cmd和错误长度分别验证不会推进块号；保留现有Bootloader协议的兼容边界，禁止借修复扩大重写历史接口。

## 5. P1：升级预检查只校验标签，文件完整性和分块读取错误没有形成失败闭环

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c:135` 只限制文件总大小；142～150 不检查 f_lseek/f_read 的 FRESULT，读取Trailer后只校验读取长度、magic、board_id。
- 未验证 `struct_ver`、`trailer_crc32`、`payload_len == fsize-128`、payload_len非零/容量上限、SHA256；152 行直接用未经这些检查的 payload_len 计算总块数，随后触发 TH 重启/握手。
- 同文件231～237同样忽略 seek/read 结果，且在短读补 FF 之前，以按声明长度算出的 valid_bytes 读取 s_chunk_buf 计算CRC；后续传输可能消费上次块残留数据；241才填充短读尾部。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/inc/th_upgrade_mgr.h:40` 已定义 struct_ver、sha256、trailer_crc32等字段，检查接口有明确数据来源。

**影响与证据边界**

MC会把只具备正确magic/board标签的损坏元数据称为“Verified”，在未完成本地文件一致性校验前推进重启/握手。TH Bootloader可能另有CRC/SHA/容量检查；因工程内无Bootloader源码，本轮不能判定其擦除前实际拒绝行为，也不能声称已经发生越界擦写。

**建议文件与验收**

- ENG-MC：`th_upgrade_mgr.c/.h` 按分阶段小函数校验元数据版本、CRC、声明/实际长度、Flash分区上限和payload摘要；每次FatFs操作必须检查状态/读取字节数，短读立即停止。读成功后才更新running CRC与块进度。
- QA：独立准备损坏CRC/SHA、错误board、零/超长/不匹配payload_len、读失败/短读/拔盘场景，确认不会发送重启/开始擦除命令；TH端也必须独立审查擦除前边界和失败恢复。禁止以“工具生成的文件通常正确”替代消费者防御。

## 6. P1：运行/升级模式没有覆盖所有入口和共享接收状态，AP 查询可干扰升级

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c:326` 仅在文本 send-line 中静默拒绝 UPGRADE；mode_set（480）只是赋值，无端口租约/原子交接。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:123` 不检查模式，始终清除 USART6共享rx_complete，随后调用可能被静默拒绝的send-line并忙等。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/marlin/marlin_module/th_upgrade_mgr.c:161` 先发 M997 再设置 UPGRADE；214/261/322 调用 send-frame 的返回值被忽略。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/motion-controller-mcu/project/src/wk_usart.c:531` 升级二进制 send-frame 不标记统一tx占用；`mc_th_usart_perf_test:704` 直接强制切换 PERF_TEST。主循环 `main.c:289` 暴露T字符触发入口。
- TH `/home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/src/user/main.c:40`、51～53 经send_quick主动发文本；`src/bsp/usart.c:206` 的send_quick直接使用板间 USART1 DMA。调试心跳80行走USART3，应区别记录，不应误称所有日志都污染业务线。

**影响与证据边界**

升级进行时 AP 的 TH 查询可以清除正在使用的共享接收事件，且文本发送失败并不显式返回调用者；结合第1项 ISR等待会阻塞升级ACK处理。TH重启文字可能出现在新协议链路上，需要定义运行/启动模式与同步恢复，不能默认静默。主循环串行性限制了部分并发路径，具体字节交织须结合ISR和设备时序实测；这里没有断言每次必定发生交织。

**建议文件与验收**

- ARCH：明确NORMAL/UPGRADE/DIAGNOSTIC端口所有权、进入/退出、已在途DMA排空、RX清理、失败返回和模式独占。旧Bootloader的0x5A A5协议作为明确隔离的维护模式，不能被算作MiniMCProto运行协议。
- ENG-MC/TH：`wk_usart.c/.h`、`minimc_proto.c`、`th_upgrade_mgr.c`、`main.c` 与TH `main.c/usart.c`统一受控入口。升级期间AP查询须返回明确busy/不支持且不得清升级接收状态；启动诊断移到独立调试口或封装成正式日志帧。
- QA：升级中插入AP查询/调试T/迟到文本、切换时存在TX DMA、拔盘/超时后再运行，分别验证所有权与恢复；先做工程联调，再交独立验收。

## 7. P2：制品布局、board标签与身份声明需要独立校验，TH锚点扇区未在链接容量中预留

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/tools/pack_firmware.py:85` 生成128字节Trailer，88～89将签名R/S全置0；175～180写 `payload + trailer`，是尾附元数据，不是前置头部，也不是已启用数字签名。
- 同文件139～146可按路径猜board；161～166对缺失版本头使用默认版本/时间；没有校验输入向量表/目标Flash布局/board适配。正常Makefile显式传board可减少误判，但不能证明载荷本身属于该board。
- TH链接脚本 `/home/sushaohua/workspace/ai_soc_project/mcu-p3/color-engine-mcu/io_toggle/libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld:34` 允许从0x08004000起240KiB直到0x08040000；`th_upgrade_mgr.h:21` 同样允许240KiB。
- 现存设计 `/home/sushaohua/workspace/ai_soc_project/mcu-p3/docs/unified_firmware_packaging_tool_implementationplan_20261015_092700.md:16`、59将Sector127锚点放在0x0803F800。若该锚点契约仍有效，App可用长度应止于该地址（238KiB）；当前链接与打包未表达这项保留区。
- MC链接脚本 `motion-controller-mcu/AT32F435xG_FLASH.ld:34` App起点0x08020000、896KiB；TH起点0x08004000。没有证据表明现有起点错误。

**本地制品只读核验结果**

| 本地文件 | 长度 | SHA256 | 首字栈/复位向量 | Trailer |
| --- | --- | --- | --- | --- |
| `motion-controller-mcu/build/fw_mc.bin` | 367924 | `1a0181514a9fb581f06d9a3cfca360a9bb650f8f13b9a876aa8aa95cdce983e7` | 0x20060000 / 0x08043231 | magic41545347、struct10000、board43500001、version010951ff、payload367796 |
| `color-engine-mcu/io_toggle/build/fw_th.bin` | 70096 | `5123839911552018d2cc931ff6d10ee308e1b42c2581480511f7dd31e131f6b0` | 0x2000c000 / 0x08013c49 | magic41545347、struct10000、board42300001、version0100fca7、payload69968 |

两文件尾部CRC与payload SHA均相符，签名R/S均为0。现有TH映像远小于潜在锚点边界，没有证据表明它当前已覆盖锚点。这些结果证明磁盘制品自洽，不证明对应源码构建可复现、板上已部署或TH已接入MiniMCProto。

**建议文件与验收**

- ARCH/MCU Owner：冻结版本化Flash布局及现有Bootloader兼容契约，核实Sector127是否仍保留；再由ENG-TH最小调整链接脚本和上限，不凭文档猜测改Flash分区。
- `tools/pack_firmware.py`、两端Makefile、版本工具与发布清单：发布模式要求显式board、准确版本头、输入ELF/BIN身份、向量表/容量/保留区校验；manifest同时记录原始payload、Trailer、完整发布文件、anchor及Bootloader SHA。称“完整性摘要/CRC校验”或明确启用的签名方案，不把全零签名称为数字验签。
- QA：独立制品检查应验证尾部位置、长度、board、版本、摘要、向量与布局；增加错误board输入、边界尺寸、错误/缺失版本头，避免“可打包”被当成“可安装”。

## 8. P2：升级SOP把文件操作当最终成功，热插拔承诺与现实现冲突；Bootloader闭环条件未齐

**已证实事实与位置**

- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/README.md:91` 承诺运行时热插U盘1秒内启动TH升级；当前 `th_upgrade_mgr.c:505`～516 在开机5秒后空闲且未检测恢复模式时永久停止轮询，受 `th_upgrade_mgr.h:25` 的5000ms常量控制。
- README105～106称更名为.cur即“升级100%成功”。`th_upgrade_mgr.c:324`～338只在旧协议finish ACK成功后更名；336行忽略`th_fs_rename_and_check`返回值，随后返回true；没有执行重启后的TH原生版本/boot_id/能力查询。
- `/home/sushaohua/workspace/ai_soc_project/mcu-p3/bootloader/435/`、`423/`当前仅有ELF/BIN/HEX/MAP，无工程内Bootloader源/链接脚本/构建入口。`project-control/docs/baseline/ms01_source_inventory_20261020.md:42`已有同样登记。因此擦除前验证、容量、锚点、自恢复不能仅依README声称已确认。

**影响与证据边界**

SOP和现行App行为不一致，会使现场误判未启动升级、误把旧.cur文件或finish ACK当成新App生效。Bootloader二进制存在且可计算哈希，不等于当前审查已验证其保护逻辑。不能因此反向断言它没有保护或已经变砖。

**建议文件与验收**

- MCU Owner更新 `mcu-p3/README.md` 的热插窗口/维护模式、版本确认和失败处理；跨仓在 `project-control/docs/...` 建立准确制品/安装记录，避免SOP另建未经检查的“权威成功条件”。
- 冻结Bootloader二进制允许列表和硬件兼容范围；可得时纳入来源/可复现构建；不可得时登记外部依赖，并独立核验已授权的拒绝错误镜像、断电恢复与应用启动行为。
- 升级成功拆成“传输/校验终态→Flash读回/Bootloader凭据→重启→新App版本/boot_id与能力→原生查询恢复”；.cur作为辅助证据。工程联调由实现团队进行，MS-21锁定实际双端组合，MS-17由独立Codex验收。不要用旧文本M115或文件改名替代新协议节点身份。

## 建议纳入父方案的操作顺序

1. ARCH冻结现有正式协议对应的命令、MTU、帧路由、缓冲所有权、ISR/主循环职责、维护协议/运行协议模式、Flash布局与身份验收；先独立审查契约。
2. ENG-MC和ENG-TH分别持有准确授权文件清单与接收输入，按双端依赖并行实施；新增自研函数≤50行、≤4参，存量代码最小修改。第4项栈边界和第5项文件校验单独成微步。
3. INTEGRATOR锁定两端源码/构建配置/Bootloader/发布映像/anchor版本组合；COORD组织真实工程联调，收四向轨迹及超时恢复数据。
4. 独立Codex使用独立预期与准确候选执行MS-17；QA作者工具及报告再由独立Codex复核。历史签署原样保留，新增run表达撤回/受影响范围，不覆盖旧报告或自动推进Done。

## 本轮检查方法和限制

实际只读命令包括：`cat`规则、`rg`/`grep`定位、`nl -ba ... | sed -n ...`精确阅读、`git -C mcu-p3 log/status`、`ls -l`制品清单；另用`python3 -B`标准库读取两份BIN的首8字节、末128字节、SHA256与CRC32，不导入工程模块、不写pycache。上述主要读取与制品检查退出码0。按MCU规则净化PATH后`rg`不可用（退出127），已改用系统`grep`；部分管道因head关闭输出产生Broken pipe，未把此作为验证通过依据。

本报告只读审查不能证明磁盘映像已安装，也不能证明真实串口、复位、擦写、掉电恢复、时延和丢包达标。所有建议的测试均为后续验收项，未在本轮执行。
