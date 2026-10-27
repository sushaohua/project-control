# 新增 HIL 发现/注入工具只读补审

审查对象：`test_harness` commit `1d0861f199b92f9eac7c2103dfe80b207dbe4838`（2026-10-27T16:24:52+08:00）；`hil/tools/device_discovery.py`、`hil/tools/probe_fault_injector.py` 及 `hil/guides/probe_rs_hardware_fault_injection.md`。

范围限制：未运行这两个脚本入口，未调用 probe-rs、subprocess 或任何物理设备。只读源码、Git元数据，并将函数经 AST 挑选后编译到隔离命名空间；全部硬件 I/O、时间等待替换为假函数。因此下述反例只证明软件控制流/失败处理漏洞，不能作为硬件验收、真实波形、时序或芯片寄存器事实的证据。未改工程文件及上一份报告。

软件反例：`/tmp/cascade_new_hil_tools_repro_20261027.py`；原始输出：`/tmp/cascade_new_hil_tools_repro_20261027.out`。不导入原模块、不执行CLI入口，所提取函数的硬件依赖均由假函数提供。

## 1. 角色识别不能唯一绑定授权板卡，扫描/手工入口均可能选错目标（已证实，P0）

- `device_discovery.py:125–156` 先尝试两个芯片配置，单凭 Flash 容量 **或** 固件向量表MSP识别角色；读取 UID 后不与已登记板卡身份比较，亦不拒绝容量/MSP互相矛盾、UID缺失/重复。MSP来自被测固件内容，不是独立硅片型号证明。
- `device_discovery.py:172–177` 遍历所有枚举探针，同角色后项静默覆盖前项；没有 session/台架/任务授权探针清单或唯一性检查。`discover_all()` 每次对系统所有匹配probe读取指纹，而非只接触已登记台架。
- `probe_fault_injector.py:79–90` 的 `manual_probe` 直接返回用户给的probe加角色预设chip，完全绕过目标身份核对；后续寄存器操作无需UID确认。
- 软件反例：Fake读取 `Flash=256KB、MSP=0x20060000`，`inspect_probe` 输出 `role=MC`；两个匹配MC探针时 `target_mapping.MC` 静默选 `probe-B`；`resolve_target_probe('FAKE','TH','probe-MC')` 返回 `('probe-MC','AT32F423CCT7')`，没有任何硬件检查。
- 修改文件/操作：两个工具新增结构化 target context，绑定任务/run、明确允许的probe列表、probe序列号、芯片识别、96-bit UID、固件/板卡角色；冲突/无唯一匹配必须失败，容量/MSP仅作辅助线索；手工probe只绕过自动枚举，不能绕过身份校验。默认只枚举、不连接未知设备；显式限定授权范围后读取。指南39–58行“唯一锁定”的说法应随实现更正。

## 2. 快照失败仍写零，缓存未绑定设备，恢复可能写错原值或默认整字（已证实，P0）

- `probe_fault_injector.py:53–76` 缓存只有 `/tmp/hil_fault_cache/{role}_{uart}_ctrl1.json`，内容无probe、UID、地址、芯片、固件、run/lease；无独占/原子写入、无过期判定。缓存缺失、JSON错误或读取异常被吞掉后使用硬编码 `default_val`。
- `probe_fault_injector.py:153–158` 快照读取失败或为0，不保存快照但仍写 `0x00000000`；为0也是合法原状态，随后enable可能错误开启原本关闭接口。`165–176` 把缓存/默认值整字写回；`188–203` reset-all完全不使用原快照而写默认整字。这会覆盖控制寄存器内除目标使能位外的其他配置，且“恢复原寄存器”不成立。
- 软件反例：Fake `probe_memory_word=None` 模拟初始快照失败，`disable_uart` 仍调用写函数，记录 `write_after_failed_snapshot=[0]`。
- 修改文件/操作：`probe_fault_injector.py` 改成受控事务：同一已验证target context锁内读取精确原值，读取失败绝不写入；包括原值0的全部状态都持久化；快照键包含UID+地址+run，原子写入并保护并发；恢复核对同一UID、固件/配置版本及事务状态，恢复原值后读回精确核对。没有可信快照就报错交人工恢复，不默认整字写“正常值”；reset-all改为只恢复本run实际修改的接口，并显式列范围。指南75–82、134–137、184–185行同步修订。

## 3. glitch无finally，异常后可长期断链；设备重发现和CLI耗时使“指定毫秒”无精度保证（已证实，P0/P1）

- `probe_fault_injector.py:179–185` 为 disable → sleep → enable，没有try/finally；`--duration-ms`（235行）接受任意int，负值会在已disable之后触发sleep异常；KeyboardInterrupt、sleep异常和中间状态读失败也无恢复保证。
- disable/get-status（146–162行）写零后还有一次独立probe读取；sleep之后enable再次 `resolve_target_probe`（165–167行）。自动模式再次扫描所有探针、读取多组指纹后才写回，同一次glitch前后可绑定不同板。一次probe命令超时上限5秒，发现阶段又有多个命令，工具无法把真实断开窗口限定为`duration_ms`。
- 软件反例：提取glitch函数，以fake disable记录 `disabled`、fake sleep抛ValueError、fake enable记录 `restored`，最终事件只有 `['disabled']`，恢复未调用。没有运行真实sleep或硬件操作。
- 修改文件/操作：`probe_fault_injector.py` 在任何写入前校验duration范围；一次resolve并固定UID/probe贯穿读/写/恢复；已持久化快照后，在try/finally内恢复并显式上报恢复失败，保留可定位恢复事务。用monotonic时间记录确认disable写入/读回与restore写入/读回的边界，输出请求窗口、实测控制窗口、误差及各命令耗时；需要严格物理窗口时用可验证硬件夹具/持续调试会话另行验收。
- 指南26–29行“物理级纳秒/毫秒控制”、130–131行“切断300毫秒后恢复”不能作为已达到精度的结论；只能描述请求保持时间。真实通信断开/恢复时刻还需物理TX/RX或其他独立测量，Python调用耗时不等于物理时序。此次没有实测精度，也未查证probe连接是否暂停CPU，不应追加“绝对非侵入”的实测结论。

## 4. reset-all吞写失败仍宣称全部成功，其他命令亦未验证实际读回值/物理通信（已证实，P0）

- `probe_fault_injector.py:201–203` 丢弃 `write_memory_word` 返回bool，无读回且无失败汇总；未在线目标195–196行跳过仍最后打印“所有接口已重置”。`main():280–281` 不处理返回结果，普通非零写命令经run_cmd返回而非抛异常时，CLI可正常结束为0。此处必须区分：超时异常会传播，但**写命令返回非零**被明确吞掉。
- `disable_uart/enable_uart` 虽核对写CLI返回值（158–160、172–174行），之后 `get_uart_status` 只返回当前值，不与请求写值比较；`main():267–275` 无条件输出“已成功切断/开通物理通信”。寄存器读回不一致也可被宣称成功；即便读回一致，仍只是注入控制成功，不能据此宣布物理协议恢复。
- `device_discovery.py:101–109` 读取解析不核对返回地址、元素数量/宽度。fake成功输出 `deadbeef: 00000100`，请求另一地址、count=3，仍返回单元素 `[256]`；该值可继续被当成角色/UID输入。`list_raw_probes():69–71` 也将枚举命令失败转空列表，非target模式可正常输出空结果，掩盖探针调用失败与确无设备的差别。
- 软件反例：Fake发现只有TH在线，所有write返回False。`reset_all_uarts` 正常返回None，输出仍含“TH USART1 -> 恢复使能”和“所有接口已重置为正常使能状态”。这是软件返回/日志反例，未执行真实CLI。
- 修改文件/操作：两个工具让读取命令验证returncode、stderr、完整地址/数量/宽度；区分无设备、身份不明、命令失败。所有写操作读回核对请求目标位/原值；reset-all聚合每个目标结果，任何必需目标缺失、写失败或读回不一致返回明确非零，保留原始命令/退出码/时间及实际作用范围。CLI成功措辞限于已证实的寄存器操作；物理链路恢复由独立端到端TX/RX判据决定。指南范例165–173行仍为TODO，不能作为有效自动验收。

## 修复与验证边界

修复涉及上述两个工具、指南、`test_harness/README.md` 的使用/能力说明，以及新增隔离软件负例与实际HIL验收记录。软件负例至少覆盖冲突/重复身份、手工probe身份不匹配、初读失败/原值0、缓存跨UID/run、负时长/KeyboardInterrupt、写非零/超时/读回不一致、目标缺失、全量恢复部分失败。修复之后另由未参与工具编写的独立Codex会话审核；硬件恢复、时序、运行中CPU状态和端到端协议行为必须另做授权真实测量，不能用本报告fake测试签发硬件通过。

AST另记录函数规模/参数事实（不单独判定Python违规）：`device_discovery.py:84` 的probe_memory_word 6参；`probe_fault_injector.py:93` write_memory_word 5参、179行glitch_uart 5参、206行main共76行。根AGENTS.md对“所有代码”提出函数规模要求，但canonical规则名为C/C++，Python适用范围及计数口径需在任务标准中显式统一，不能把C++标准自动外推为已判Python违规；在上述target/transaction上下文和分阶段修复中可一并考虑拆分。
