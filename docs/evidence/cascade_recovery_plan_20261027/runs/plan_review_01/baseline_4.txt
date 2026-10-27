# AP / Host / QA 相邻漏洞独立只读审计（2026-10-27）

本报告由独立审阅任务 `/root/independent_host_review` 执行。范围为 soc-ap 主机程序、串口传输、CTest 和 test_harness 参考运行器。未修改业务源码、正式任务状态或工程文件；实验源码、构建和新证据位于 `/tmp`。导入 Python 运行器自动产生的本次 `run_codec_cases.cpython-38.pyc` 已移除，预存 `reference_vectors.cpython-38.pyc` 未动。未连接、烧写或测试物理板卡；所有新增运行均为 host 软件负例，不能作为 HIL 或物理通过证据。

审查版本：soc-ap commit `8d6c446cd3b0bac57054723ba7da9cd797ab4131`；main.cpp SHA256 `879a2efdffb4b1a0a6cf47e6cf65501e6fc6f065d23a20cc44f59a52d30d1d74`。parser.cpp SHA256 `4b882ecaf454b564d93ce57b50bbba624b62d45902aa0cf85a937e6b1da4cc1b`；codec.cpp SHA256 `e943c3b6c991063a6a887b954ce9eef95dd2485ddf5901c9763052f97414b040`。

## 1. 命令语义和响应关联缺失（高；已复现＋源码事实）

`soc-ap/core/host/main.cpp:28` 默认 cmd=0x03，`:144` 固定 L=0；而 `soc-ap/contracts/minimcproto/v2-commands.md:67-91` 规定 GET_VERSION=0x01/L0、VERSION_REPORT=0x02/L16，`:120-153` 规定 PING=0x03/L4、PONG=0x04/L12。默认请求既不是版本查询，也不是合法业务 PING。

`main.cpp:237-240` 仅以 parser ready 终止接收，`:278-279` 直接报告 SUCCESS。`core/forward/minimc/parser.cpp:154-160` 的 ready 只代表 decode_frame 通过帧级校验。没有校验响应 src=目标、dst=AP、IS_RESPONSE、WANTS_ACK、预期 cmd、seq 关联和命令固定载荷。`main.cpp:171-176` 把任意 >=4B 载荷前四字节打印为固件版本。

复用此前 `/tmp/independent_host_review_20261027.py` 已运行的8例，不重复运行：silence（0字节/0帧）exit0；原样回显AP请求、错来源(srcTH)、错目的(dstTH)、未知cmd7F、非响应flags04、错seq400、4B短VERSION_REPORT，后7例全部 SUCCESS/exit0。回显例的 src=AP/dst=MC/L0，仍称 MCU response，是最直接的误判反例。

拟修改：`soc-ap/core/host/main.cpp`（或其拆出的命令/事务模块）、共享命令常量/解码接口；新增 host 查询负例到 `soc-ap/tests/host/` 和独立 QA 用例到 `test_harness/`。判据必须为预期命令级匹配，而不是CRC成功；NACK、其他事务响应和请求回显不得成功。

## 2. 超时/断链错误最终都返回0（高；已复现＋源码事实）

`main.cpp:271` 把 serial_read=false 与暂无数据合并忽略，`:283` 无条件return0，`:308-310` 不消费 poll返回值和received，最终return0。`serial_posix.cpp:156-157` 对HUP/ERR/NVAL明确返回false，但调用者未上报。

扩展实验 peer_hangup：PTY读到AP TX后关闭master，host仍等待约80ms，输出0字节/0帧后exit0，无读失败/断链诊断。此前静默例与本轮非法超时例也均exit0。源码推导：持续HUP时poll可能立即返回，调用者在总超时前热循环；本次没有测量CPU占用，不把热循环CPU量当作已测事实。

拟修改：`core/host/main.cpp`、`core/forward/transport/serial_posix.h/.cpp`；区分超时、IO错误、协议不匹配和成功，向main传播非零状态，记录端点/错误原因；read故障独立负例纳入host测试。

## 3. serial_write缺少截止时间/进展约束（高；已复现＋源码事实）

`serial_posix.cpp:112-125` 无deadline；EAGAIN/EWOULDBLOCK/EINTR直接continue；write返回0时既不前进也不退出。主机查询timeout在发完包之后才用于读窗口（`main.cpp:299-308`），不能约束写循环。

隔离实验使用真实POSIX PTY，不读取master，把slave输出队列写满，确认 `FILL_RESULT=-1 ERRNO=11`；随后调用生产serial_write，300ms内未返回，被外部Python看门狗SIGKILL（returncode=-9）。另以链接器 `--wrap=write` 注入持续返回0，同样300ms不返回后被kill。前者实测真实OS EAGAIN路径，后者是明确标注的syscall fault injection，不声称真实驱动自然返回0，也不把300ms观察本身当作数学无限证明；无退出路径来自源码。

证据：`/tmp/cascade_transport_gap_probe.cpp`、`/tmp/cascade_host_gap_probes.py`、`/tmp/cascade_host_gap_probes_20261027.log`。拟修改：transport头/实现（显式写deadline，POLLOUT等待，处理zero progress，保持部分写统计），host总事务deadline和传输独立故障用例；遵守每函数<=50行/<=4参，使用配置结构体而非新增过多参数。

## 4. 配置输入被静默改写（中；已复现＋源码事实）

`serial_posix.cpp:11-26` 仅支持9600到230400中的枚举值，其他一律退回B115200；`:71-80` 仍open成功。直接API实验请求921600，tcgetattr确认实际输出速度B115200，函数exit0。当前AP CLI固定115200，因此这主要是transport通用API的漏洞，不能夸大为现有CLI已发921600。

`main.cpp:78-94` 使用atoi/strtoul无endptr/errno/范围检查，uint8窄化。实测 timeout=garbage→0、-1→-1，都先发包再立即exit0；cmd=garbage→00、3junk→03、0x103→03、-1→FF；dst=0x102→02；均未报参数错误。未实测atoi超int范围，不能推定其具体结果。

拟修改：`core/host/main.cpp` 严格数值解析与支持值白名单；`serial_posix.h/.cpp` 不支持baud返回错误，不允许静默fallback；host/API参数边界测试。非法输入必须在打开设备/发包之前失败。

## 5. 日志不能完成原始逐帧物理对账（高验收影响；已复现＋源码事实）

`main.cpp:200-213` capture固定512B并静默丢弃后续数据；`:195-196` raw仅在失败诊断打印；`:278-281` 成功分支只打印解码摘要，不打印raw RX、cap或完整计数。TX打印在`:153`，成功RX摘要在`:163-169`，均无墙钟毫秒时间戳。`:216-222` steady-clock毫秒仅供parser使用，没有输出，不能充当事件取证时间。

本轮注入600B噪声，total_bytes_received=600但RX Raw Captured Data仅512B，未标注截断/丢88B。此前7个成功误报的输出也无raw RX。512B小于协议最大帧1038B（parser.h:38-42），即使单个最大帧也不能由该capture完整保留。

拟修改：`core/host/main.cpp`/独立证据记录模块、HIL采集脚本；成功和失败均记录毫秒墙钟时间＋单调时钟RTT、原始双向字节/逐帧事件、事务关联、串口设置、构建/固件hash；有界存储须显式overflow计数/截断标记，缺失关键原始应答的run不得通过。不能要求只扩大数组而继续静默丢证据。

## 6. FrameView返回借用的生命周期风险（中；源码事实＋推导风险）

`main.cpp:252` parser为poll_and_parse局部变量，`codec.cpp:152` payload借用输入buffer，parser.h:78-81明确生命周期约束。非空payload在poll_and_parse返回后指向已退栈内存。当前`:279`打印发生在返回前，execute_query_version在`:308`后不解引用payload，故没有证据说当前打印发生use-after-return。

拟修改：`core/host/main.cpp` 所有权/消费接口；在parser活着时完成严格验证并复制所需值，或让parser由调用方拥有；不能把借用FrameView向外暴露却暗示稳定持有。无需无关重写通用parser；应补生命周期说明和真实消费路径测试。

## 7. 默认CTest只有smoke仍100%绿色（中；已复现＋源码事实）

`soc-ap/CMakeLists.txt:38-44` 总有host_runtime_smoke，协议QA被MINIMC_QA_ROOT条件包住，`:82-83` 未配置只STATUS提示。`tests/host/smoke.sh:16-47` 只检查help/version/config与daemon启停，未执行query-version。

既有隔离构建未配置QA_ROOT；本次 `ctest --output-on-failure` 实跑1/1 host_runtime_smoke通过，输出100%，exit0，原始记录 `/tmp/independent_host_review_20261027_build/Testing/Temporary/LastTest.log`。这证明绿色不能说明协议、query或HIL通过，不说明CTest工具有错。此前配置输出明确 `MiniMC QA test suite not enabled`。

拟修改：`CMakeLists.txt`、host查询测试、CI/任务验收命令。允许开发smoke配置，但验收profile须强制QA_ROOT与明确测试组/数量，区分smoke/codec/host事务/HIL证据等级；不能只以ctest总exit0收件。

## 8. 参考运行器的command_valid是Python推算，不验证生产命令处理（高覆盖缺口；源码事实＋已复现）

`test_harness/static_checks/minimcproto/run_codec_cases.py:244-260` 读取probe输出的cmd/length后，用自身Python字典推算command_valid；`:418-424` 将该推算值与fixture比较。`soc-ap/tests/protocol/probe.cpp:308-337` 只调用decode_frame并打印帧级字段，没有生产command_valid判定；CMakeLists.txt:76-79把运行器连到minimc-probe而不是soc-ap查询行为。

独立调用evaluate_command_layer_on_decoded：frame_valid=true、cmd02、L16，但flags04（非response）、dstTH、seq999、载荷全0（proto0.0），仍返回 `(True, None)`。当前expected中有command_valid元数据的case仅DEC-001/002/003/005/006。长度检查本身是有用的fixture/帧语义元数据检查，但不能被记作生产命令验证、事务匹配或HIL通过；运行器没有覆盖flags/seq/版本字段语义更不说明生产实现具备这些检查。

拟修改：`test_harness/static_checks/minimcproto/run_codec_cases.py` 将fixture派生元数据与生产返回判据分别命名；正式命令校验测试必须实际调用受测生产validator/host事务接口，再与独立预期比较；新增flags/长度/保留字节/proto/请求应答关联负例，现有codec测试仍保留帧级定位。不要在参考代码里“补上逻辑”后宣称生产实现已修。

## 可复核执行记录

以下命令均实际执行；路径含真实根目录。首次8例结果复用，没有重复执行。

| cwd | 命令 | 退出码/结果 |
| --- | --- | --- |
| `/home/sushaohua/workspace/ai_soc_project/soc-ap` | `cmake -S . -B /tmp/independent_host_review_20261027_build -G Ninja -DCMAKE_BUILD_TYPE=Release` | 0，GNU9.4.0，QA_ROOT未配置 |
| 同上 | `cmake --build /tmp/independent_host_review_20261027_build` | 0 |
| 同上 | `python3 /tmp/independent_host_review_20261027.py` | 0；8例，各child exit0，7例误报SUCCESS |
| `/tmp/independent_host_review_20261027_build` | `ctest --output-on-failure` | 0；仅1/1 smoke |
| `/home/sushaohua/workspace/ai_soc_project/soc-ap` | `c++ -std=c++17 -Wall -Wextra -Werror -I core/forward/transport /tmp/cascade_transport_gap_probe.cpp core/forward/transport/serial_posix.cpp -Wl,--wrap=write -o /tmp/cascade_transport_gap_probe` | 0 |
| 同上 | `python3 /tmp/cascade_host_gap_probes.py` | 0；baud child0；eagain/zero由300ms看门狗kill，child=-9；其余9个host子例exit0 |

运行器微实验在cwd `/home/sushaohua/workspace/ai_soc_project/test_harness` 执行 `python3 - <<'PY' ... PY`，用importlib.util导入`static_checks/minimcproto/run_codec_cases.py`，直接传入本报告第8组列出的dict；exit0，stdout如第8组。它不是生产程序测试，也没有修改fixture。只读定位和hash/status命令均exit0；首次错误的contracts根目录搜索、任务通配符搜索exit2，以及移除本次pyc后尝试rmdir因预存reference pyc保留而exit1，均不作验证通过依据。

## 既有证据索引与限制

- 首次8例脚本：`/tmp/independent_host_review_20261027.py`（原始stdout在独立审阅工具事件中，未另存日志文件）。
- 新增完整输出：`/tmp/cascade_host_gap_probes_20261027.log`；脚本：`/tmp/cascade_host_gap_probes.py`；串口小工具源码：`/tmp/cascade_transport_gap_probe.cpp`。
- 原始CTest输出：`/tmp/independent_host_review_20261027_build/Testing/Temporary/LastTest.log`。
- 历史物理日志（本次只读，未独立复测物理真实性）：`project-control/docs/evidence/ms07/runs/run_20261027_01/05_vmware_hil_query_cmd03.log`、`06_vmware_hil_query_cmd01.log`、`qa_review_report.md`；`run_20261027_02/hil_physical_evidence.log`、`result.md`。
- 历史run01 QA报告L92-102已明确看到物理0帧，却L114签APPROVED；复盘文档L30的“未核验真实Raw Hex”应改为“看到了零有效回包但未执行否决”。run02日志L13-25为cmd03/L0请求与cmd03/L4应答，即便物理来源成立，也不满足正式版本命令布局。
- 本报告没有新的APPROVED签署，没有改正式结论/状态。建议按以上8组形成工程修复卡和独立QA负例卡；真正版本/TH闭环仍须真实双端原生协议与物理证据验证。
