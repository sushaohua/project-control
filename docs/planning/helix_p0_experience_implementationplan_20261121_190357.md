# Helix P0 体验补齐与两项遗留缺陷合并交付实施方案（UX-01 / UX-02 / TH-ESTOP-01 / BOOT-MC-STAY-01）

## 修订历史

| 版本 | 修订时间（北京时间） | 修订人 | 变更摘要 | 审批状态 |
| --- | --- | --- | --- | --- |
| `v0.1` | `2026-11-21 19:03:57` | `AI (Codex)` | 核对 r18b 已有交互和包内容，定义 DES-UI 职责及真机体验验收 | 待用户审批 |
| `v0.2` | `2026-11-21 19:18:00` | `AI (Antigravity-CLI / PM / gemini-4-neon-high)` | 按用户确认将 `UX-01`、`UX-02`、`TH-ESTOP-01`、`BOOT-MC-STAY-01` 四项合并为下一轮统一交付；完成第 1 部分产品目标、用户流程、DES-UI 入口与状态文案规范、`UX-01` 走查清单与四项可观察验收条件，预留第 2 部分交 ARCH 原地合成技术设计 | 待 ARCH 技术核对后交用户审批 |
| `v1.0` | `2026-11-21 19:27:00` | `AI (Antigravity-CLI / ARCH / gemini-4-carbon-high)` | 完成源码与 `graphify` AST 物理取证，逐项消解 `OI-01`~`OI-05`；原地合成第 2 部分（`§2.1`~`§2.5`：影响仓库与精确文件白名单、跨仓调用链与协议/字库/分区契约推演、`Design-It-Twice` 接缝比选与分仓 `Diff Budget`、`SLICE-09` 切片规格、四阶门禁、单台架顺序 HIL 与四项分报/回滚预案） | 待用户审批 (Human Gate #1) |
| `v1.1` | `2026-11-23 09:16:00` | `AI (Antigravity-CLI / ARCH / gemini-4-carbon-high)` | 合入用户批准 `v1.0` 时追加的小修需求“把 Helix 默认语言改成中文 (`"zh"`)”：物理核实语言键值真值（`"zh"`）、`ui_xml/translations/zh.xml` 全量汉字 100% 字库覆盖及中英文菜单映射；设计 `/data/printer-soc/helix` 存量 `r18b` 配置一次性默认中文迁移机制（忠实保留用户后续手动切回英文的选择）；同步更新第 1/2 部分导航描述、`printer-soc@main` 文件白名单（`15` ➔ `20` 文件）、`Diff Budget`、`S09-AP` 契约与验收判据 | **已批准执行**（`2026-11-23 09:22` 用户“嗯，批准。”；常规上板过 `Human Gate #2A`，MC Bootloader SWD 写刷单独过 `Human Gate #2B`） |
| `v1.2` | `2026-11-23 10:23:31` | `AI (Codex / PM)`、`AI (Codex / ARCH)` | 按用户要求新增第五项 `S09-RES`。以 `r18b` 对比 SLICE-09 候选，明确 AP 运行采样、MC/TH 静态容量核算与证据验收。 | **已批准执行**（`2026-11-23 13:01` 用户“全部批准。”） |
| `v1.3` | `2026-11-23 12:56:00` | `AI (Antigravity-CLI / ARCH / gemini-4-carbon-high)` | 针对容器沙箱双套 `ctest` 复现的 `test_device_manager.cpp:1427` `500ms` 身份轮询时序竞态，将 `tests/device_manager/twin/test_device_manager.cpp` 纳入 `printer-soc@main` 白名单（`20` ➔ `21` 文件，`protected_globs` 新增该文件、`max_protected_lines` `45` ➔ `50`），在 `main()` 中将纯只读初始状态检查 `test_rpc_get_version_info` 提前至 `test_rpc_get_snapshot` 之后执行（零断言削弱）；100% 原样保留 `v1.2` 与 `§1.8`、`§2.6` 内容 | **已批准执行**（`2026-11-23 13:01` 用户“全部批准。”） |
| `v1.4` | `2026-11-23 14:02:00` | `AI (Antigravity-CLI / ARCH / gemini-4-carbon-high)` | 针对 `SLICE-09 r03` 独立 Codex 冷审检出的 6 项 `BLOCKER`（`S09-01`~`S09-06`）与 2 项证据 `MINOR`（`S09-07`~`S09-08`）原地合入一次性根治设计：分离 `DeviceManager` 本地急停保护锁 `estop_latched` 与双板 `4B ACK` 确认态 `estop_confirmed`；重扫 Toast 绑定单调 `client_req_seq` 与 `task_id`；`Forward` `prepare_command()` 同步清理重扫/未选节点旧 `valid` 与 `sha256`；移除 `last_estop_outcome==BACKEND_BUSY` 陈旧锁残留；`test_device_manager.cpp` 夹具确定性留出首 `1.5s` 初始未探测窗口；`bootloadermc` 提炼生产 `2000ms` 超时跳转判定函数并纳入宿主单测；同步扩增白名单（`printer-soc` `21` ➔ `24` 文件、`bootloadermc` `2` ➔ `4` 文件）与 `Diff Budget`（`ENG-AP` 受保护上限 `50` ➔ `60` 行） | **已批准执行**（`2026-11-23 14:53` 用户“批准执行。”） |

> `v1.0` ~ `v1.4` 已全部获用户批准执行；本轮合并交付包含 `UX-01`、`UX-02`（含默认中文 `"zh"` 与存量迁移）、`TH-ESTOP-01`、`BOOT-MC-STAY-01` 及第五项 `S09-RES` 资源评估。

---

## 第 1 部分：产品目标、交互规范与验收定义（PM / DES-UI）

### 1.1 背景、功能基线与合并交付目标

1. **来源与问题定义**：
   - 在 `SLICE-08 (r18b)` 完成双板串口 OTA 与冷重启自愈的 `HIL-Verified` 闭环后（见 [HIL_R18B_SUMMARY.md](../evidence/SLICE-08/hil_r18b/HIL_R18B_SUMMARY.md)），用户现场体验反馈：**板端触屏找不到 MC/TH 固件升级入口**，且升级过程中的缺包/校验反馈不够直观，旧文案还将当前校验策略误表述为“验签通过”。
   - 同时，`SLICE-08` 实板验收阶段留存两项已锁定源码根因的延后缺陷交接单：
     - `TH-ESTOP-01`：[th_app_0x17_estop_ack_handoff_20261121_171500.md](th_app_0x17_estop_ack_handoff_20261121_171500.md)（TH App 对 `0x17` 急停命令返回 `0B ACK` 导致 AP 报超时，且 `stop_mode=0` 解除时误再次触发急停）；
     - `BOOT-MC-STAY-01`：[bootloadermc_0x01_stay_in_boot_handoff_20261121_145800.md](bootloadermc_0x01_stay_in_boot_handoff_20261121_145800.md)（MC Bootloader 收到 AP 只读 `0x01` 版本查询后误置 `stay_in_boot=1`，导致常规复位后永久滞留 Bootloader、无法自愈回 App）。
2. **已确认功能基线（冻结不变，历史证据保留）**：
   - 基线：`SLICE-08 r18b` `HIL-Verified` 候选（`printer-soc@6f28023f`、`mcu-p3@a64bffbf`、`boot/bootloadermc@3e01c00`、`boot/bootloaderth@1a03513`）。
   - `SLICE-08` 的既有结项状态与验收证据按原版本完整保留，不覆盖或重写。
3. **本轮合并交付目标（用户已确认，含 `2026-11-23` 追加默认中文要求）**：
   - 将 **`UX-01`、`UX-02`（含 Helix 默认语言改为中文 `"zh"` 及存量配置一次性迁移）、`TH-ESTOP-01`、`BOOT-MC-STAY-01`** 四项合并为下一轮统一交付，形成**一个最终候选**完成正式软件准出，并在单台架按顺序完成真机验收；原定 P1 运动/打印控制功能继续单独排期。
   - **产品效果**：板端触屏开机/升级后默认展示全中文界面（同时尊重用户后续手动语言切换），操作者能够从「设置 (`Settings`)」一级菜单直接找到 MC/TH 固件升级并清晰看到缺包/在线/校验/进度/完成结果；急停锁存与解除在双板侧真实闭环；MC 在 AP 持续轮询下发生非升级复位后能自动回到 App 恢复在线。

---

### 1.2 需求范围、优先级与边界

> 以下优先级与四项合并范围均为**用户已确认决定**；细化交互文案与走查字段为 **PM / DES-UI 提议**（供 ARCH 核对可行性后随整份方案一并请用户批准）。

| 项编号 | 优先级 | 责任角色与仓边界（摘要） | 产品目标与核心交付内容 | 备注 / 门禁红线 |
| --- | :---: | --- | --- | --- |
| **`UX-01`** | **P0（首步取证）** | `DES-UI` 定走查清单；`INTEGRATOR` 真机执行（零业务代码修改） | 基于现有 `r18b` 英文默认基线候选，从板端真实首页出发走查版本查询、亮度、有线网络与 MC/TH 固件升级（走到找入口、打开页面、扫描固件、查看结果），如实定位并归因体验卡点。 | 必须先于 `UX-02` 实板部署执行，保留 `r18b` 英文现状证据。 |
| **`UX-02`** | **P0（体验补齐）** | `DES-UI` 定入口与状态文案；`ENG-AP` 实施 `printer-soc` Helix UI 与配置迁移；交付配套可扫描固件 | **将 Helix 默认语言设为中文（`"zh"`），并对存量 `/data` `r18b` 默认英文配置执行一次性升级迁移（保留用户后续手动切换语言的选择）**；在「设置 (`Settings`)」一级增加「本地固件升级 (MC/TH)」入口，保留「关于 (`About`)」页原入口，两处复用同一 OTA 页面；分别清晰呈现 MC、TH 固件包状态；缺包、离线或校验失败时给出明确下一步提示；修正将当前完整性校验误写为“验签通过”的文案；最终候选配套可扫描的 `fw_mc.bin` / `fw_th.bin`。 | 严格复用真实后端 OTA RPC 与状态，严禁前端伪造进度或包状态，严禁每次重启强行覆盖用户手动语言选择。 |
| **`TH-ESTOP-01`** | **P0（安全闭环）** | `ENG-MCU` 实施 `mcu-p3@feat/soc-debug` | 修复 TH App 对 `0x17` 急停锁存与解除的协议响应与语义：锁存（`1`）和解除（`0`）均返回标准 `4B CMD_ACK`，解除时不重新触发急停/清温/入队 `M112`；实现 AP 下发后 MC、TH 双板真实应答与整机状态 `IDLE -> EMERGENCY_STOP -> IDLE` 闭环。 | 需通过宿主机单测 + 真实串口 OTA 刷入 `fw_th.bin` 后真机复验。 |
| **`BOOT-MC-STAY-01`** | **P0（自愈修复）** | `ENG_BOOT_MC` 实施 `boot/bootloadermc@soc_debug`（**严禁写 `main`**） | 修复 MC Bootloader 收到只读 `0x01` 版本查询后误置驻留标志的问题：普通 `0x01` 正常应答且 `2.0s` 等待窗口结束后自动跳转 App；同时回归 `UPG2` 魔数、`0x1D(action=2)`、`0x20` 等显式驻留及正常 OTA 恢复路径。 | **Bootloader 实板写刷（SWD 烧录 `0x08000000`）必须单独向用户报批**；未获批前仅完成软件准出并明确标注实板项待验证。 |

#### 包含范围（In Scope）
- `r18b` 真机首页起步的体验现状走查与卡点归因报告（`UX-01`，保持 `r18b` 英文现状取证）。
- Helix 默认语言切为中文（`"language": "zh"`）、存量 `/data/printer-soc/helix/config/settings.json` 一次性默认中文升级迁移（不覆盖用户后续手动切回英文的选择）、触屏「设置 (`Settings`)」一级新增升级入口、「关于 (`About`)」页入口保留、双入口复用同一 OTA 页面、MC/TH 各自包状态与可操作下一步提示、校验策略如实文案修正、以及与最终候选版本匹配的固定目录可扫描固件准备（`UX-02`）。
- `TH App` `0x17` 急停锁存/解除 `4B ACK` 与解除语义修复及双板真机急停闭环验证（`TH-ESTOP-01`）。
- `bootloadermc` 只读 `0x01` 不置驻留位修复、显式驻留与正常 OTA 回归测试，以及单独报批获准后的真机刷写与复位自愈验证（`BOOT-MC-STAY-01`）。

#### 明确排除范围（Out of Scope）
- **原定 P1 打印与运动控制功能**（继续单独排期，不混入本轮）。
- 新增网络在线下载 OTA、U 盘文件管理器浏览选包或变更固定扫描目录策略（继续沿用固定目录 `/run/printer-soc/firmware/`）。
- 修改协议命令码、帧布局、MCU Flash 分区布局、签名体系/公钥发布策略、Bootloader `bootloaderth`、Linux SDK/内核驱动或新增常驻后台服务。
- 涉及加热或电机实际通电运动的操作（继续严守零加热 PWM=0、零电机运动安全红线）。

---

### 1.3 端到端用户流程与异常表现

#### 1.3.1 正常主流程

1. **只读核验与基础设置流程（`UX-01` `r18b` 英文基线体验路径）**：
   - 操作者从 `r18b` 真机首页进入齿轮 `Settings`（英文基线；部署新候选后对应中文菜单为 `设置`）：
     - **版本查询**：进入 `Help & About`（`帮助与关于`）→ `About`（`关于`），下滑可见 AP 版本、MC 固件版本/运行模式、TH 固件版本/运行模式。
     - **屏幕亮度**：进入 `Display & Sound`（`显示与声音`），拖动 `Brightness`（`亮度`）滑块，物理背光随拖动真实变化，操作后可恢复原亮度。
     - **有线网络**：进入 `System`（`系统`）→ `Network Settings`（`网络设置`）→ `Ethernet`（`以太网`），可见 `eth0` 的 IP 与 MAC 地址。
2. **默认中文与本地固件升级全流程（`UX-02` 目标体验路径）**：
   - **默认中文与手动切换保持**：全新部署或从 `r18b` 升级启动后，Helix 默认加载中文界面（`"language": "zh"`，顶栏与一级分类显示 `设置`、`显示与声音`、`打印机`、`正在打印`、`硬件与设备`、`安全与通知`、`系统`、`帮助与关于`）；若用户在 `设置 (Settings)` → `显示与声音 (Display & Sound)` → `语言 (Language)` 中手动切回 `English ("en")`，后续服务重启或整机断电重启仍保留用户所选语言。
   - **入口可达**：操作者从首页进入齿轮「`设置 (Settings)`」，**在一级菜单直接看到并点击「`本地固件升级 (MC/TH)`」**（2 步直达）；也可从 `设置 (Settings)` → `帮助与关于 (Help & About)` → `关于 (About)` 原入口进入，两处打开完全一致的 OTA 页面。
   - **进入与扫描**：打开页面后查看当前连接/锁定状态与 MC、TH 各自固件包状态；点击「扫描固定目录固件」，后台扫描固定目录 `/run/printer-soc/firmware/` 并返回真实校验结果，分别展示 `fw_th.bin`、`fw_mc.bin` 的就绪状态（文件名、大小、短摘要及与当前校验策略一致的通过提示）。
   - **目标勾选、安全确认与执行**：勾选目标节点（双选时后台按既定顺序先 TH 后 MC）、按需勾选「允许同版本重刷」、勾选「安全前置确认（无打印、无加热、运动静止）」，点击「开始本地 OTA 升级」。
   - **进度监控与完成后复查**：界面实时呈现后台真实阶段、百分比进度条与锁定提示；完成后明确提示重启回 App 与核验结果；操作者切回「`关于 (About)`」页复查 MC、TH 固件版本与运行模式（`App`），并与同一次后台 OTA 事务日志及双板 `boot_id` 对账一致。
3. **急停锁存与解除流程（`TH-ESTOP-01`）**：
   - 设备处于 `IDLE` 在线状态时，AP 下发急停锁存（`EmergencyStop(1)`）→ MC 与 TH 均返回 `4B ACK` → 整机状态切换为 `EMERGENCY_STOP`（急停已锁存）；
   - 确认安全后下发解除急停（`EmergencyStop(0)`）→ MC 与 TH 均返回 `4B ACK` 且 TH 不再错误触发 `M112` → 整机状态恢复为 `IDLE`。
4. **MC 非升级复位自愈流程（`BOOT-MC-STAY-01`）**：
   - AP 生产守护进程持续以 `500ms` 周期轮询只读 `0x01` 版本查询；
   - MC 发生非升级复位（如按物理 `RESET` 键或普通软复位）进入 Bootloader `2.0s` 窗口；
   - `bootloadermc` 正常应答 `0x01`（带 Boot 标志）但不锁定驻留；`2.0s` 窗口期满后自动跳转回 `MC App`，AP 端自动恢复 `MC ONLINE` 且状态正常。

#### 1.3.2 关键异常、负例与恢复表现

| 异常/负例场景 | 预期可观察系统与界面表现 | 恢复 / 下一步动作 |
| --- | --- | --- |
| **固定目录缺包（双包均缺或仅缺 MC/TH 其一）** | 扫描结束后，对应缺失节点行明确提示「未找到 `fw_mc.bin`（或 `fw_th.bin`）」，不得笼统显示“未扫描”；另一就绪节点仍真实显示其包信息。点击开始升级若勾选了缺包节点，阻止发起并提示具体缺包节点与目录路径。 | 按提示将对应固件包放入 `/run/printer-soc/firmware/` 后点击「重新扫描」，或仅勾选已就绪节点进行单板升级。 |
| **固件包校验失败（魔数/头/长度/完整性或签名不通过）** | 对应节点行明确标示「校验失败」及后台返回原因摘要，严禁显示为“已通过”或“验签通过”；阻止勾选该失效包发起升级。 | 提示用户核对并替换有效固件包后重新扫描。 |
| **AP 后端连接未就绪或 MC/TH 节点离线** | 界面明确区分「本地服务未连接」与「MC/TH 节点离线」，不无限 Loading、不静默失败；点击扫描或升级给出明确错误与排查指引。 | 提示检查串口/后台服务连接并等待节点恢复 `ONLINE` 后重试。 |
| **未勾选节点或未完成安全前置确认** | 点击「开始本地 OTA 升级」时本地阻断发起，明确指出缺少项（目标节点或安全确认开关）。 | 补全勾选后即可直接发起，无需退回重进。 |
| **升级进行中并发点击升级或触发急停** | 状态栏清晰区分「后台已锁定（`BUSY`）」与「设备已确认急停」；并发请求被安全拒绝，不破坏在途 OTA 事务。 | 等待当前 OTA 结束释放锁后再执行后续操作。 |
| **显式请求进入 Bootloader（`UPG2` / `0x1D(action=2)` / `0x20`）** | `bootloadermc` 必须继续可靠驻留，不因 `BOOT-MC-STAY-01` 修复而提前跳 App，确保正常串口 OTA 与异常恢复路径不受影响。 | 正常完成串口 OTA 或收到重启指令后返回 App。 |

---

### 1.4 DES-UI 交互入口与状态文案规范（`UX-02`）

本节依据 [07_UI交互设计师职责与交付规范.md](../../.agents/rules/07_UI交互设计师职责与交付规范.md) 编制，由 `ENG-AP` 严格落地（底层字段映射与实现边界交 `ARCH` 在第 2 部分确认）。

#### 1.4.1 信息架构与双入口复用规范

1. **主入口（新增，`设置 (Settings)` 一级直达）**：
   - **位置**：`设置 (Settings)` 主列表（`settings_panel.xml`）一级菜单内新增操作行，置于 `系统 (System)` 与 `帮助与关于 (Help & About)` 之间，**仅在 `aisoc_mode == 1` 时可见**，不影响非 AISoC 模式布局。
   - **主标题**：统一采用半角括号 `本地固件升级 (MC/TH)`（与既有 `about_settings_overlay.xml` 保持一致且经 CJK 字库 100% 覆盖核实）。
   - **副标题**：`从固定目录扫描、校验并升级 MC/TH 固件`。
   - **图标与热区**：沿用 `download` 图标及 `setting_action_row` 标准行高（满足最小触控热区 $\ge 48\times 48\text{ px}$），从首页至升级页严格满足 **2 次点击直达**（首页齿轮 → `本地固件升级 (MC/TH)`）。
2. **次入口（保留，`关于 (About)` 页原入口同步文案）**：
   - 保留 `设置 (Settings)` → `帮助与关于 (Help & About)` → `关于 (About)` 中的 `row_aisoc_local_ota` 行；
   - **同步修正副标题**：将原 `从固定目录扫描、验签并升级 MC/TH 固件` 改为 `从固定目录扫描、校验并升级 MC/TH 固件`。
3. **页面与状态单一复用原则**：
   - 两处入口必须调用同一 `OtaLocalOverlay` 页面实例与同一套后台状态订阅/RPC，严禁复制第二套 UI 或本地维护独立假状态。

#### 1.4.2 校验策略文案纠偏（硬性修正项）

现有 `r18b` 文案将当前 `integrity-only-hil` 候选的完整性校验误写成“验签通过”，会导致操作者误判安全策略。**必须全页统一修正如下**（若未来启用真实公钥验签，应由后端显式返回校验模式再展示对应文案，前端不得硬编码谎称“已通过 ECDSA-P256 验签”）：

| 界面位置（当前源码锚点） | 现有误导文案（`r18b`） | `UX-02` 目标标准文案 |
| --- | --- | --- |
| `about_settings_overlay.xml:158` | `从固定目录扫描、验签并升级 MC/TH 固件` | `从固定目录扫描、校验并升级 MC/TH 固件` |
| `ota_local_overlay.xml:34`（扫描按钮副标题） | `核验 ATSG 与 ECDSA-P256 发布签名` | `扫描 /run/printer-soc/firmware/ 并校验包完整性与策略` |
| `ui_settings_ota.cpp:43`（`READY` 阶段提示） | `固定目录包已通过 ATSG 与 ECDSA-P256 验签，等待安全确认` | `固件包校验通过，请核对目标并勾选安全确认后开始升级` |
| `ui_settings_ota.cpp:181`（未扫描/缺包拦阻 Toast） | `请先扫描固定目录并通过验签` | `请先扫描固件并确认已勾选节点固件包校验通过` |

#### 1.4.3 OTA 页面五态展示与明确下一步提示矩阵

页面须清晰分别呈现 **`TH 固件包`** 与 **`MC 固件包`** 各自状态，并在每一种非就绪/异常态给出**可执行的下一步操作提示**：

| 维度 / 场景 | 页面展示位置 | 标准展示文案规范 | 明确下一步提示（不可缺失） |
| --- | --- | --- | --- |
| **初始未扫描** | `升级状态` / `TH 固件包` / `MC 固件包` | 状态：`等待扫描本地固件`；TH/MC 行分别显示：`fw_th.bin：未扫描` / `fw_mc.bin：未扫描` | 引导：`请点击“扫描本地固件”检查 /run/printer-soc/firmware/` |
| **扫描中 / 升级中（Loading）** | `升级状态` + 进度条 + `并发与急停` | 真实反映后端阶段与 `0%~100%` 进度（如 `阶段: FLASH_WRITING (62%)`）；锁状态显示 `状态: 后台已锁定 (BUSY)` | 明确提示：`升级进行中请勿断电，等待自动重启与回 App 核验`（防重复点击） |
| **单板或双板包就绪（Ready）** | `TH 固件包` / `MC 固件包` / `升级状态` | 就绪节点显示：`已就绪 · <文件名> (<大小>B, sha:<前12位>)`；总状态：`固件包校验通过，等待安全确认` | 引导：`勾选需升级节点与安全确认后，点击“开始本地 OTA 升级”` |
| **缺包（无文件 / 单缺其一）** | 对应缺失节点行 + `升级状态` / Toast | 缺失节点行：`缺失 · 未找到 fw_mc.bin`（或 `fw_th.bin`）；总状态如双缺则提示 `固定目录未找到可升级固件包` | 引导：`请将 fw_mc.bin / fw_th.bin 放入 /run/printer-soc/firmware/ 后重新扫描`（单缺时补充提示：`或取消勾选缺失节点仅升级已就绪板`） |
| **校验失败（格式/头/摘要/策略失败）** | 对应节点行 + `升级状态` | 节点行：`校验失败 · <具体原因摘要>`；总状态：`固件包校验未通过（<原因>）` | 引导：`请核对并替换有效固件包后重新扫描` |
| **节点离线 / 服务未连接（Offline）** | `并发与急停` / `升级状态` / Toast | 明确显示 `本地服务未连接` 或 `目标节点离线（MC/TH 离线状态）` | 引导：`请检查后台服务与板卡通信连接，待节点恢复 ONLINE 后重试` |
| **升级失败（Error）** | `升级状态` + Toast | `升级失败：<后端错误码/原因>` | 引导：`请核对设备在线状态与故障原因后重新扫描重试` |
| **升级提交待核验 / 完成（Success）** | `升级状态` + 进度条 | 核验中：`传输已提交，等待重启回 App 并核验版本与 boot_id...`；核验完成：`100% 升级完成，双板已回 App 且核验通过` | 引导：`可前往“关于”页复查 MC/TH 最新版本号与运行模式` |

#### 1.4.4 DES-UI 交付 6 项自检与用户操作闭环约束核对

- **有反馈且等待有界**：扫描、升级、急停点击均有即时 UI/Toast/状态栏反馈；禁止无限 Loading 或无响应点击。
- **真实性与防假状态**：所有包摘要、在线态、进度百分比与回 App 核验结果严格来自后端真实回报，禁止前端定时器假进度或静态“全绿”。
- **防重复与恢复闭环**：`BUSY`/在途态拒绝重复触发副作用；失败、缺包或取消后页面保持可重新扫描与恢复，不卡死在异常态。
- **触控与字体适配**：沿用 Helix 标准 `setting_action_row` / `setting_info_row` / `setting_toggle_row` 组件与深/浅色主题 Token，满足 $\ge 48\times 48\text{ px}$ 触控热区，并在 270° 旋转屏分辨率下确认中文文案无截断与乱码。

---

### 1.5 `UX-01`｜`r18b` 现状实机走查清单规范（`DES-UI` 定单，`INTEGRATOR` 执行）

本清单用于**先取 `r18b` 现状证据**（零业务代码修改），`INTEGRATOR` 必须从真机真实首页（触屏视角）逐步操作，禁止跳过导航或用后台 RPC 冒充界面可达性。

#### 1.5.1 走查前环境登记（必填）
- 记录板端实跑候选信息：`printer-soc` Git SHA / rootfs 摘要、MC/TH 当前版本与 `boot_id`、`helix-screen` 运行参数与 `aisoc_mode` 实际值、`/run/printer-soc/firmware/` 初始文件清单（区分“系统默认无包”还是“已预置包”）。

#### 1.5.2 逐步实机走查项

| 序号 | 检查项 | 首页起步操作路径（按 `r18b` 源码现状） | 预期核对点 | 必采证物 |
| :---: | --- | --- | --- | --- |
| **`CHK-01`** | **三端版本与运行模式查询** | 首页 → 齿轮 `Settings` → `Help & About` → `About` → 向下滚动 | 核对屏幕是否清晰显示 `AP 版本`、`MC 固件`、`TH 固件` 及其 `App/Boot` 运行模式，且与后台实测版本一致。 | 实拍/截屏 + 对应后台版本查询日志 |
| **`CHK-02`** | **屏幕亮度调节与恢复** | `Settings` → `Display & Sound` → 拖动亮度滑块 → 恢复原值 | 核对滑块可操作、物理背光亮度随拖动真实变化，恢复后保持原值。 | 调节前后观测记录/照片 + 背光节点数值核对 |
| **`CHK-03`** | **有线网络信息查看** | `Settings` → `System` → `Network Settings` → `Ethernet` | 核对屏幕显示的 `eth0` IP 地址、MAC 地址与板端实际网络配置一致。 | 实拍/截屏 + `ip addr` 核对日志 |
| **`CHK-04`** | **MC/TH 升级入口发现性** | ① 停留在 `Settings` 一级浏览全部菜单项；② 再按 `Settings` → `Help & About` → `About` 下滑寻找 `本地固件升级 (MC/TH)` | 记录 `Settings` 一级是否存在入口、需几步点击与几次滚动才能找到旧入口、`aisoc_mode` 是否导致入口被隐藏。 | `Settings` 一级图 + `About` 页图 + 操作步数记录 |
| **`CHK-05`** | **打开 OTA 页面与状态可见性** | 在 `About` 页点击 `本地固件升级 (MC/TH)` | 核对页面能否正常打开、无崩溃/白屏/裁切、中文显示是否正常、初始文案是否存在误导或不清楚处。 | OTA 页面初始画面实拍/截屏 |
| **`CHK-06`** | **扫描固件与结果反馈** | 在 OTA 页面点击 `扫描固定目录固件`（在 `r18b` 当前实板目录状态下执行，**不发起实际写刷**） | 核对扫描是否有响应、返回耗时、MC/TH 包状态与总状态文案展示内容，如实判定用户能否看懂当前缺包/失败原因及下一步该做什么。 | 点击后画面实拍/截屏 + 对应目录 `ls` 与后台扫描日志 |

#### 1.5.3 卡点归因硬标准（每项如实打标，禁止笼统写“不通过”）
每处发现的问题必须归入以下标准分类之一（可多选并注明精确页面与截屏编号）：
1. **`入口难找`**：功能存在但藏于多层菜单/深层滚动，或一级设置不可见；
2. **`页面打不开`**：入口缺失/被条件隐藏、点击无响应、崩溃或无法弹出覆层；
3. **`缺固件包`**：页面和扫描通路正常，但 `/run/printer-soc/firmware/` 未随候选就位 `fw_mc.bin` / `fw_th.bin`；
4. **`反馈不清楚`**：扫描/错误/状态文案模糊、未区分缺包与校验失败、未提示下一步操作、或文案将完整性校验误写为“验签通过”；
5. **`其他异常`**：字体乱码、布局遮挡、状态与后台真实数据不符等（附原始日志）。

---

### 1.6 可观察完成条件与交付总则

#### 1.6.1 执行与验收总则（用户已确认）
1. **并行与顺序编排**：`UX-01` 优先取得 `r18b` 现状结论；交互细化与分仓软件开发（`ENG-AP`、`ENG-MCU`、`ENG_BOOT_MC`）可并行推进。
2. **单候选正式软件准出**：所有代码修改合龙至**一个最终候选**，按项目四阶门禁完成正式软件准出（含独立沙箱构建回归与独立异构 Codex 双轴冷审 `0 BLOCKER`），并生成与该候选精确匹配的可扫描 `fw_mc.bin` / `fw_th.bin`。
3. **单台架顺序实机验收**：在唯一真机台架上按顺序执行各实机验证项；严守安全红线（零加热、零运动、只读验签公钥不动、备份不篡改）。
4. **Bootloader 写刷单独报批闸门**：涉及 SWD 写刷 `boot/bootloadermc` 至 `0x08000000` 前，必须单独呈报精确镜像 SHA-256、文件大小、探针 ID 与芯片型号，获用户明确批准后方可执行。
5. **四项分报与客观留白**：结项汇报按 `UX-01`、`UX-02`、`TH-ESTOP-01`、`BOOT-MC-STAY-01` 四项分别列出判定结论、最终候选各仓 Commit SHA 与原始证据路径；**任何缺少真实实板实测的条目必须保留“待验证”状态，绝不借软件自测或模拟替代真机通过**。
6. **正式交接可追溯**：最终交接须提供 Git 服务端可读回的各仓正式提交（线性历史）及对应交付收据。

#### 1.6.2 四项可观察完成条件（`Pass Criteria`）

| 验收项 | 前置条件 | 操作步骤 | 可观察通过判据（正例 + 必测负例） |
| --- | --- | --- | --- |
| **`UX-01` 现状走查** | 台架运行 `r18b` 英文默认基线候选（无业务代码改动） | `INTEGRATOR` 按 §1.5 从真实首页（英文基线）走完 `CHK-01`~`CHK-06` | 产出完整现状走查记录与截图/日志证物；对版本、亮度、网络、升级入口、打开页面、扫描及反馈逐项判定，并按标准 5 类卡点归因如实定性。 |
| **`UX-02` 体验补齐（默认中文迁移 + 负例：缺包/不可用反馈）** | 台架部署最终候选（含存量 `/data` `r18b` 持久化配置），固定目录 `/run/printer-soc/firmware/` 处于缺包状态（测试双缺与单缺其一） | ① 观察部署重启后面板默认语言，并验证手动切换语言再重启后的保持行为；② 从首页 → `设置 (Settings)` 一级点击「`本地固件升级 (MC/TH)`」→ 点击扫描 → 尝试勾选缺包节点发起升级 | ① **存量 `r18b` 板升级后界面自动默认显示中文（`"zh"`，如 `设置`、`显示与声音`、`系统`、`帮助与关于`）且零缺字；在 `显示与声音` → `语言` 手动切为 `English` 并重启服务后仍忠实保持 `English`（不强制覆写），切回 `中文` 恢复全中文界面**；② `设置 (Settings)` 一级直接可见入口并打开页面（`关于 (About)` 入口同样可用且复用同一页）；③ MC/TH 各自状态明确标出缺失文件并给出明确下一步提示，不出现“验签通过”误导文案；④ 尝试升级缺包节点被明确阻断并提示原因。 |
| **`UX-02` 体验补齐（正例：真实触屏全链路双板升级）** | 台架部署最终候选（默认中文界面），固定目录就位与该候选匹配且校验通过的 `fw_th.bin` 与 `fw_mc.bin` | 从板端真实触屏进入升级页 → 扫描确认双包就绪 → 勾选 TH+MC 与安全确认 → 发起升级 → 观察进度直至完成 → 切回 `关于 (About)` 页复查版本与模式 | ① 扫描后分别清晰展示 MC、TH 固件包信息与策略一致的通过文案；② 升级全过程呈现真实后台进度与锁定态，不卡死；③ 完成后屏幕呈现明确完成与回 App 核验提示；④ `关于 (About)` 页可核对最新 MC/TH 版本与 `App` 模式；⑤ 触屏操作记录与**同一次后台 OTA 事务日志、双板固件版本、升级前后 `boot_id` 变化**四方严格对账一致。 |
| **`TH-ESTOP-01` TH 急停与解除** | 最终候选已通过 `fw_th.bin` 串口 OTA 刷新到真机 TH 板，整机处于 `IDLE` 在线态 | 通过 AP 依次下发急停锁存（`EmergencyStop(1)`）与解除急停（`EmergencyStop(0)`），并检查宿主机协议单测 | ① 宿主机单测覆盖 `0x17 [0x01]` 与 `0x17 [0x00]` 均返回标准 `4B ACK`，且 `0x00` 不触发 `M112`；② 真机 AP 下发锁存与解除均返回成功（零 `-8` 超时），原始通信/后台日志证明 MC、TH 均返回真实 `4B ACK`；③ `GetSnapshot` 设备状态真实走完 `IDLE -> EMERGENCY_STOP -> IDLE` 闭环，解除后未重新锁存急停。 |
| **`BOOT-MC-STAY-01` MC Bootloader 驻留修复** | 最终候选 `bootloadermc` 已通过宿主机单测、交叉编译与软件四阶门禁；**且已获用户单独实板 SWD 烧录批准** | ① 宿主机单测回归普通 `0x01` 轮询跳转 + 显式驻留（`UPG2`/`0x1D(action=2)`/`0x20`）；② 获批刷写实板后，在 AP 持续轮询 `0x01` 工况下触发 MC 非升级复位；③ 回归一次正常 OTA/显式驻留恢复路径 | ① 宿主机正负用例全部通过；② 真机 AP 持续轮询 `0x01` 下，MC 复位后正常应答 `0x01` 且约 `2.0s` 等待窗口结束后自动跳回 `MC App` 并恢复 `ONLINE`；③ 显式驻留与正常串口 OTA 恢复路径无退化。*（若用户暂不批准实板 SWD 烧录，本项软件部分标 `SW-Verified`，实板部分明确保留“待验证”。）* |

---

### 1.7 约束、假设与待决项（交 `ARCH` 核实与人工审批）

1. **已确认事实与硬约束（无需重问用户）**：
   - 四项（`UX-01`、`UX-02`、`TH-ESTOP-01`、`BOOT-MC-STAY-01`）合并下一轮单候选统一交付；原定 P1 继续单独排期。
   - 沿用固定目录 `/run/printer-soc/firmware/` 与既有 `OtaLocalOverlay` 页面复用原则。
   - 双 Bootloader 严禁写 `main`（`bootloadermc` 锁定 `soc_debug`），实板 SWD 刷写必须单独报批。
2. **交 `ARCH` 在第 2 部分物理核实的待定技术项（`open_items`）**：
   - **OI-01（包状态与错误粒度）**：核实 `AisocOtaNodeInfo` / `AisocOtaStatus` 及后端扫描 RPC（`Forward` / `DeviceManager` / `aisoc_connection`）当前返回的字段与错误码，是否足以在前端无歧义区分**「未扫描」「缺文件（`fw_mc.bin`/`fw_th.bin` 不存在）」「校验失败（具体原因）」「节点离线 / 后端未连接」**；若现有只读字段不足，评估是否需在 `printer-soc` 后端或适配层做最小契约内补齐，并纳入精准文件白名单与 Diff Budget。
   - **OI-02（校验策略文案来源）**：核实后端是否上报当前构建/运行的校验模式（如 `integrity-only-hil` vs 正式签名校验），以决定前端采用“策略中性准确文案（校验通过）”还是动态展示后端下发的校验模式。
   - **OI-03（触屏中文字体与布局验证）**：核实板端 `helix-screen` 内置中文字库对新增文案字符（含全角括号/斜杠如 `本地固件升级（MC／TH）` vs 半角 `本地固件升级 (MC/TH)`）的覆盖情况，避免出现缺字方框。
   - **OI-04（最终候选配套可扫描固件产出与部署方式）**：明确单候选合龙后，如何由受控构建链路产出与该候选匹配、经校验可扫描的 `fw_mc.bin` / `fw_th.bin`（含 `TH-ESTOP-01` 修复），并在 `UX-02` 实机验收前按“先缺包负例、后置包正例”顺序就位。
   - **OI-05（真机实测顺序与依赖耦合）**：明确单台架上 `UX-01`（`r18b` 现状）→（若获批）`BOOT-MC-STAY-01` SWD 刷写与复位验证 → `UX-02` 缺包负例 → `UX-02` 触屏双板 OTA（同步刷入含 `TH-ESTOP-01` 修复的 `fw_th.bin`）→ `TH-ESTOP-01` 真机急停/解除闭环的精确执行次序，确保同一事务对账与最少重复刷写。
3. **需用户审批的闸门项**：
   - **审批闸门 1（本方案总体审批）**：待 `ARCH` 补齐第 2 部分技术设计与切片后，呈报用户一次性审批本合并实施方案。
   - **审批闸门 2（Bootloader 实板写刷独立审批）**：待 `BOOT-MC-STAY-01` 通过软件四阶门禁产出精确二进制摘要后，单独申请物理 SWD 烧录许可。

---

### 1.8 `S09-RES`｜资源评估（`v1.2` 增量，已批准）

用户要求为 SLICE-09 增加资源评估。建议以 `SLICE-08 r18b` 为基线评估本轮最终候选，给出资源占用、可比差值和已知容量余量，作为第五项交付结果。AP 覆盖整机和 Helix、Forward 等生产服务的 CPU、内存，以及系统、数据和固件暂存所用存储。MC、TH 覆盖 App 和配套 Bootloader 的 Flash、静态 RAM 及栈预留。

AP 运行数据复用同一台架的实板验收窗口，覆盖正常空闲和 `UX-02` 的双板 OTA。基线优先采用版本和工况可核对的现有记录。候选 OTA 采样与原验收共用一次升级事务。MC、TH 的静态评估使用对应版本的正式构建产物。通信吞吐、协议延迟和 CRC16 仍由[通信性能测试方案](printer_performance_implementationplan_20261120_171756.md)单独评审。

**完成条件**为提交一份可追溯的资源表及原始证据，逐项给出版本、工况、取数来源、绝对值和可比差值，按已有的分区或链接上限计算余量。发现超限时标出对应版本、资源和上限。缺少同工况基线、有效采样或实际栈峰值时，明确标出缺项及其对结论的影响。AP 实板数据沿用 §2.5.2 的授权边界和单台架顺序。

---

## 第 2 部分：技术架构、调用链、分仓白名单与切片规划（ARCH）

### 2.1 影响仓库、锁定分支与精确文件清单（经 AST / 源码物理核实）

#### 2.1.1 受管仓库基线与本轮读写边界总表

| 仓库路径 (`workspace.json`) | 锁定分支 | 基线 Commit (`SLICE-08 r18b`) | 本轮权限属性 | 唯一责任角色 | 说明与分支红线 |
| --- | --- | --- | :---: | --- | --- |
| `printer-soc` | `main` | `6f28023f7f1b774d181fc4ba59d3c378f260bfc1` | **读写（限白名单 24 文件）** | `ENG-AP` | 落地 `UX-02` 及 `r03` 冷审 `S09-01`~`S09-05` 根治：默认中文与存量迁移、双入口、单节点当次扫描一致性、重扫请求序号绑定、急停本地锁存与双板确认分离、实时忙锁释放及 `test_device_manager` 确定性初始窗口 |
| `mcu-p3` | `feat/soc-debug` | `a64bffbf1a0c5cbc2fe96b51632098042697878b` | **读写（限白名单 3 文件）** | `ENG-MCU` | 落地 `TH-ESTOP-01`：TH App `0x17` 锁存/解除统一回 `4B ACK`、消除解除误动作与双单测套件对齐 |
| `boot/bootloadermc` | `soc_debug` | `3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` | **读写（限白名单 4 文件）** | `ENG_BOOT_MC` | 落地 `BOOT-MC-STAY-01` 及 `S09-06`：移除 `0x01` 误置 `stay_in_boot`，提炼 `main.c` 生产 `2000ms` 超时跳转判定纳入宿主单测；**严格锁定 `soc_debug`，绝对严禁写入 `main`** |
| `boot/bootloaderth` | `soc_debug` | `1a0351363cf7b9cbc0aa6919b4afc6be61561152` | **只读输入** | — | 本轮零改动；作为同源版本身份与 OTA 协议不变锚点 |
| `test_harness` | `main` | `fb1409be7ad5586c701df586553d7f5b67bc2b43` | **只读输入** | `INTEGRATOR`（执行） | 复用既有 `test_helix_screen_integration.py` 与 `check_platform_inputs.py`，零夹具篡改 |
| `sdk/c308l` | 清单锁 `ea8f4eec...` | `manifest_commit=eb5d0d51...` | **只读输入** | — | 遵循 `c308l_platform_contract.yaml`，零平台/内核/驱动修改 |
| `project-control` | `main` | `36ee0f4b19c0ff6c357547f0f13380a22f4a3246` | **治理归档** | `COORD` | 获批后登记 `slices/SLICE-09.yaml`、维护 `slices/ledger.md` 与 `docs/evidence/SLICE-09/`；`contracts/minimc_v2_contract.yaml` 零变更 |

#### 2.1.2 三仓精确修改文件清单（白名单外零触碰）

1. **`printer-soc@main`（`ENG-AP`，共 24 个文件）**：
   - **默认中文语言配置、存量 `/data` 一次性迁移与打包单测（5 个）**：
     - `services/helixscreen/platform/c308l/live-profile.json`：将 `settings.language` 由 `"en"` 改为 **`"zh"`**，并写入 `"c308l_default_lang_migrated": 1`（由 `package.py:write_config()` 合并入只读包内 `config/settings.json`）。
     - `tools/c308l_services.py`：扩展 `prepare_panel_settings()`（拆分为 `<=50` 行、`<=4` 入参、全中文 docstring 的小辅助函数）：① 首次从 `assets/config/settings.json` 播种时同步创建 `panel_config/.helix-fresh-install`（对齐 `Config::init()` `config.cpp:1834-1844` 防旧备份回灌）；② 当 `assets/config/settings.json` 声明 `"language": "zh"` 且持久化 `settings.json`（及 `/var/lib/helixscreen` 与 `$HOME/.helixscreen` 滚动备份）尚未含 `"c308l_default_lang_migrated"` 时，若原 `language` 为 `"en"` 或空则一次性迁移为 `"zh"` 并写入 `"c308l_default_lang_migrated": 1`；此后用户在界面手动切回 `"en"` 时，`Config::save()` 原样保留 JSON 中的 `"c308l_default_lang_migrated": 1`，后续重启绝不覆盖用户手动选择。
     - `boards/c308l-aw419/rootfs-overlay/usr/bin/printer-soc-panel`：镜像同步上述首启 `.helix-fresh-install` 标记与一次性默认中文迁移逻辑（外层改为 `if [ -f "$HELIX_CONFIG_DIR/settings.json" ]` 解耦 `sys_input` 存在性，内部仅在 `default_settings.language == "zh"` 时触发一次性迁移、仅在 `sys_input` 目录存在时执行 `touch_device` 清洗，100% 兼容存量极简夹具）。
     - `services/helixscreen/platform/c308l/tests/test_tools.py`：同步更新 `live-profile.json` 语言断言为 `live['settings']['language'] == 'zh'` 及 `c308l_default_lang_migrated == 1`。
     - `tests/packaging/test_product_package.py`：保留存量播种测试不退化，新增 `prepare_panel_settings()` 与 `printer-soc-panel` 对 `r18b` 遗留 `"language": "en"`（含滚动备份）首次升级自动切为 `"zh"`、以及用户手动改回 `"en"` 后重启忠实保留 `"en"` 的正反单测。
   - **UI 布局 XML（3 个）**：
     - `services/helixscreen/ui_xml/settings_panel.xml`：在 `group_settings` 内 `row_system`（`系统`）与 `row_help`（`帮助与关于`）之间新增受 `aisoc_mode` 门控的 `container_settings_aisoc_ota` / `row_settings_local_ota`（主标题 `本地固件升级 (MC/TH)`，副标题 `从固定目录扫描、校验并升级 MC/TH 固件`，`description_min_bp="0"`，回调 `on_settings_local_ota_clicked`）。
     - `services/helixscreen/ui_xml/about_settings_overlay.xml`：保留 `row_aisoc_local_ota` 次入口，将第 158 行副标题由 `从固定目录扫描、验签并升级 MC/TH 固件` 修正为 `从固定目录扫描、校验并升级 MC/TH 固件`。
     - `services/helixscreen/ui_xml/ota_local_overlay.xml`：将第 34 行扫描副标题修正为 `扫描 /run/printer-soc/firmware/ 并校验固件包完整性`，将第 37 行升级副标题修正为 `接收后台 OTA 进度并在重启后核验 App 模式与 boot_id`（消除硬编码签名表述与未烘入字库的 `真/订/阅` 字符）。
   - **Helix UI 与 CJK 字库管理（5 个）**：
     - `services/helixscreen/include/ui_panel_settings.h`：声明静态回调 `static void on_settings_local_ota_clicked(lv_event_t* e);`。
     - `services/helixscreen/src/ui/ui_panel_settings.cpp`：注册 `on_settings_local_ota_clicked`（同步写入 `SettingsPanel::init_subjects()` 与 `register_settings_panel_callbacks()` 以满足 `[L013]` XML 解析前置约束），回调内调用 `helix::settings::get_ota_local_overlay().show(get_global_settings_panel().parent_screen_);`，与 `关于 (About)` 入口 100% 复用同一单例。
     - `services/helixscreen/src/system/cjk_font_manager.cpp`：在 `#ifdef HELIX_ENABLE_AISOC` 下令 `CjkFontManager::needs_cjk()` 返回 `true`——默认 `"zh"` 下原生加载 CJK 字库，且即使用户在 `显示与声音` → `语言` 手动切回英文 `"en"`，AISoC 专属中文行（`AP 版本`、`本地固件升级 (MC/TH)` 与 `OtaLocalOverlay`）仍保持挂载 29 个 `assets/fonts/cjk/noto_sans_cjk_*.bin` 而不卸载退化为豆腐块。
     - `services/helixscreen/include/ui_settings_ota.h`：将 `phase_buf_` 扩至 `192` 字节，`mc_pkg_buf_`、`th_pkg_buf_`、`lock_estop_buf_` 扩至 `160` 字节，并新增 `uint64_t pending_scan_seq_ = 0U;` 绑定当次扫描请求序号（`S09-02`）。
     - `services/helixscreen/src/ui/ui_settings_ota.cpp`：基于后端真实 `scan_state`、`scan_error`、`policy` 及 `AisocSnapshot` 实现五态展示与下一步提示，并闭环 `S09-01`~`S09-04`：① 仅当 `snap.estop_confirmed` 为真显示 `状态: 设备已确认急停`，`snap.estop_latched && !snap.estop_confirmed` 显示 `状态: 本地急停已锁存（板卡未全部应答）`；② 重扫 Toast 严格校验 `st.client_req_seq == pending_scan_seq_`，杜绝旧 `READY` 快照抢先消费等待标志；③ `format_ota_pkg` 与 `scanned_*_sha256_` 同时要求 `scan_state == "READY" && valid && sha256.size() >= 12U`；④ `busy` 仅读取实时锁（`st.active || st.last_rpc_code == -5 || snap.maintenance_locked`），移除 `last_estop_outcome == BACKEND_BUSY` 陈旧残留（急停遇 `-5` 继续由 `application.cpp:2034` 全局 `estop_callback` 弹即时提示，不覆盖全局回调）。
   - **Helix 原生连接器与单测（3 个）**：
     - `services/helixscreen/include/aisoc/aisoc_connection.h`：`AisocOtaNodeInfo` 含 `scan_state`/`scan_error`；`AisocOtaStatus` 含 `policy` 与 `uint64_t client_req_seq = 0U`；`AisocSnapshot` 新增 `bool estop_confirmed = false`；`request_ota()` 返回本次分配的单调递增 `uint64_t` 请求序号（并声明可单测复用的纯判定辅助接口）。
     - `services/helixscreen/src/aisoc/aisoc_connection.cpp`：`parse_dm_snapshot_json()`（及状态轮询）从权威布尔字段解析 `estop_latched` 与 `estop_confirmed`；`request_ota()` 分配单调递增 `req_seq` 入队并在工作线程出队/绑定 `task_id` 时同步至 `ota_status_.client_req_seq`；`check_ota_upgrade_gate()` 对所选节点同时强制 `scan_state == "READY" && valid && sha256.size() >= 12U`。
     - `services/helixscreen/tests/unit/aisoc/test_aisoc_p0.cpp`：覆盖 `policy`、`scan_state`、双板急停确认 vs 单板超时仅本地锁存 vs 锁存期故障上报不丢锁及外部解除（`S09-01`）、旧 `READY` 回调先于本次拒绝到达不吞失败提示（`S09-02`）、`UNSCANNED` 节点不误判就绪（`S09-03`）、以及 `BUSY -> OTA 完成 -> 恢复就绪` 锁自动释放（`S09-04`）。
   - **Forward OTA 扫描状态/策略与当次镜像一致性及 E2E 测试（4 个）**：
     - `services/forward/modules/ota/ota_internal.h`：`fwd_ota_runtime` 含定长静态字段 `char scan_state[2][24]` 与 `char scan_error[2][32]`（零动态分配）。
     - `services/forward/modules/ota/ota_image.cpp`：`ota_load_image()` 精确写入单节点 `scan_state`（`"READY"` / `"MISSING"` / `"INVALID"` / `"SIGNATURE_INVALID"`）与 `scan_error`。
     - `services/forward/forward_ota.cpp`：`build_snapshot()` 输出顶层 `"policy"` 及 `mc`/`th` 的 `"scan_state"`、`"scan_error"`；`prepare_images()` 在 `operation == 0U` 时完整遍历 `rt->mask` 全部节点；**`prepare_command()` 在重置 `scan_state[index] = "UNSCANNED"` 时，对扫描任务（`operation == 0U`）或升级任务未选节点（`(request->target_mask & (1U << index)) == 0U`）同步清空 `rt->image[index].valid = false; size = 0U; version = 0U; sha256[0] = '\0'; warning[0] = '\0';`（`S09-03`）**。
     - `tests/ota/test_ota_e2e.py`：覆盖单节点缺包扫描、`policy` 字段断言，以及**「双包扫描 `READY` ➔ 移走 `fw_th.bin` 并发起仅 MC 任务 ➔ TH 终态快照保持 `UNSCANNED + valid=false + sha256=""`」**（`S09-03`）。
   - **DeviceManager 急停锁存/双板确认权威分离与 Twin 确定性夹具（4 个）**：
     - `services/device_manager/device_manager_types.h`：经源码物理核实 `device_manager_state_t` 定义于该头文件第 `78–118` 行（`device_manager_state.h` 仅含函数原型且签名不变，保持零改动），紧邻第 `94` 行 `bool estop_latched;` 新增 `bool estop_confirmed;`（标识本次急停锁存已获 MC+TH 双板 `4B ACK` 确认，`S09-01`）。
     - `services/device_manager/device_manager_state.cpp`：`dev_state_init_snapshot()` 显式清零 `estop_latched = false; estop_confirmed = false;`；`dev_state_get_snapshot_json()`（`GetSnapshot`）与 `dev_state_get_summary_json()`（`GetDeviceState`）直接输出布尔字段 `"estop_latched":true|false,"estop_confirmed":true|false`，与易被后续 `dev_state_set_fault()` 覆写的 `system_status` 字符串彻底解耦（`S09-01`）。
     - `services/device_manager/device_manager_dbus.cpp`：`latch_emergency_stop()` 置 `estop_latched = true, estop_confirmed = false`；`handle_emergency_stop()` 仅当 `reason_code == 1U && fwd_err == 0` 时加锁置 `estop_confirmed = true` 并递增 `generation_id`（下游超时/失败时保持 `estop_latched == true && estop_confirmed == false`）；`clear_emergency_stop_state()` 同时清零 `estop_latched` 与 `estop_confirmed`（`S09-01`）。
     - `tests/device_manager/twin/test_device_manager.cpp`：① 在 `setup_dev_test_env()` 中先完成 `setup_test_dds_and_dbus_cli(env)` 并在启动 `dev_thread` 前将 `env->dev_state.next_identity_probe_ns` 设为 `get_host_monotonic_ns() + 1500000000ULL`，确定性留出首 `1.5s` 初始未探测窗口供 `test_rpc_get_version_info` 100% 稳定验证初始 `OFFLINE + valid:false`，随后在 `test_rpc_identity_fields` 显式归零 `next_identity_probe_ns` 触发真实探测验证不伪造身份（`S09-05`）；② 新增急停双板 `4B ACK` 确认（`estop_latched=true, estop_confirmed=true`）、下游单板超时仅本地锁存（`estop_latched=true, estop_confirmed=false`）、锁存期间 MC 故障上报覆盖 `system_status="FAULT"` 仍保持急停锁、以及外部 `EmergencyStop(0)` 解除清零用例（`S09-01`）。
2. **`mcu-p3@feat/soc-debug`（`ENG-MCU`，共 3 个文件）**：
   - `color-engine-mcu/io_toggle/src/app/minimc_proto.c`：修复 `handle_th_motion_stop()`（第 642–672 行）。
   - `color-engine-mcu/io_toggle/src/user/test_twin45_th_debug.c`：同步修正 `test_twin48_filament_and_stop()` 第 1054 行旧 `0B ACK` 长度断言（`14U` ➔ `18U` 并校验 `4B CMD_ACK` 载荷尾两字节为 `0x0000`）。
   - `color-engine-mcu/tests/test_th_ota_and_bootid.c`：新增 `0x17 [0x01]` 急停锁存与 `0x17 [0x00]` 急停解除正负配对测试（验证 `18B` 帧 / `4B CMD_ACK`、锁存清温并入队 `M112`、解除不清温且不入队 `M112`、非法 `stop_mode > 1` 回 `NACK 0x03`）。
3. **`boot/bootloadermc@soc_debug`（`ENG_BOOT_MC`，共 4 个文件）**：
   - `bootloader/inc/boot_uart_ota.h`：定义统一探测窗口常量 `#define BOOT_PROBE_WINDOW_MS (2000U)`，声明共用纯判定函数 `uint8_t boot_uart_ota_should_jump_after_window(uint32_t probe_ticks, uint8_t udisk_connected, uint8_t upgrade_in_progress);`（`S09-06`）。
   - `bootloader/src/boot_uart_ota.c`：移除 `handle_cmd_get_version()` 第 327 行 `s_ota.stay_in_boot = 1U;`；实现 `boot_uart_ota_should_jump_after_window()`（仅当 `!upgrade_in_progress && boot_uart_ota_should_stay_in_boot() == 0U && !udisk_connected && probe_ticks >= BOOT_PROBE_WINDOW_MS` 时返回 `1U`，否则返回 `0U`）。
   - `bootloader/src/main.c`：第 `210–220` 行主循环直接调用 `boot_uart_ota_should_jump_after_window(probe_ticks, g_udisk_connected, g_upgrade_in_progress)` 驱动 `handle_no_disk_timeout(probe_ticks)`，消除生产代码与单测阈值脱节（`S09-06`）。
   - `tests/test_mc_boot_ota.c`：直接调用 `boot_uart_ota_should_jump_after_window()` 覆盖 `1999ms` 窗口未届满保持不跳、连续 `0x01`/`0x03` 轮询满 `2000ms` 触发跳转、以及 `UPG2` / `0x1D(action=2)` / `0x20` / `udisk_connected=1` / `upgrade_in_progress=1` 超过 `2000ms` 继续驻留及 `0x1D(action=1)` 重启不驻留的完整配对单测（`S09-06`）。

---

### 2.2 跨仓调用链与软硬件协议契约推演（含 `OI-01`~`OI-05` 物理核实结论）

#### 2.2.1 《端到端真实符号调用链与现状断点核实表》（经 `graphify` AST 与源码取证）

| 业务链路 | 真实符号调用链（`仓:文件路径:函数/符号` + 调用边） | 现状断点 / 根因定位（`SLICE-08 r18b`） |
| --- | --- | --- |
| **`UX-02` 入口导航、默认中文迁移与字库渲染** | ① 旧深层路径：`printer-soc:ui_xml/settings_panel.xml:row_help` ➔ `SettingsPanel::on_help_clicked()` ➔ `settings_help_overlay.xml` ➔ `about_settings_overlay.xml:row_aisoc_local_ota` ➔ `ui_settings_about.cpp:on_about_local_ota_clicked()` `[EXTRACTED]` ➔ `OtaLocalOverlay::show()`。<br>② 配置与语言加载链：`c308l_services.py:prepare_panel_settings()` / `printer-soc-panel` ➔ `config.cpp:Config::init()`（含 `$HOME/.helixscreen/settings.json.backup` 滚动备份恢复）➔ `application.cpp:1848` `helix::ui::ensure_translation_loaded(lang)`（加载 `ui_xml/translations/zh.xml`）➔ `CjkFontManager::on_language_changed(lang)`。 | ① `settings_panel.xml` 一级无升级入口，需 4 次点击 + 滚动方可触达；<br>② `live-profile.json:9` 原设 `"language": "en"`，且实板 `/data/printer-soc/helix/config/settings.json`（及 `.helixscreen/settings.json.backup`）已持久化 `r18b` 的 `"language": "en"`，仅改只读模板不会迁移存量板配置；<br>③ `ota_local_overlay.xml:37`（`真/订/阅`）与 `ui_settings_ota.cpp:176`（`勾`）不在 `.cjk_codepoints.manifest`（1239 字）内，且用户若手动切回 `"en"` 时 `needs_cjk("en")==false` 会卸载 CJK 字库导致 AISoC 中文变豆腐块。 |
| **`UX-02` 固定目录扫描与策略上报** | `ui_settings_ota.cpp:OtaLocalOverlay::handle_scan()` ➔ `AisocConnection::request_ota(op=0, mask=3)` ➔ D-Bus `ForwardInterface.OtaCommand` ➔ `forward_ota.cpp:fwd_ota_dbus_command()` `[EXTRACTED]` ➔ `fwd_ota_command()` `[EXTRACTED]` ➔ `worker_main()` ➔ `execute_task()` ➔ `prepare_images()` ➔ `ota_image.cpp:ota_load_image()` ➔ DDS `state/ota_status` ➔ `AisocConnection::poll_ota_dds()` ➔ `OtaLocalOverlay::sync_from_backend()`。 | ① `forward_ota.cpp:89-99` 在 `operation==0` 扫描时若 `index=0 (fw_mc.bin)` 不存在立即 `return false`，短路跳过 `index=1 (fw_th.bin)` 扫描；<br>② `ota_load_image()` 未区分 `ENOENT` 缺包与包校验失败，也未在 JSON 中输出编译期 `policy`，前端第 43 行硬编码显示“已通过 ECDSA-P256 验签”。 |
| **`TH-ESTOP-01` 双板急停锁存与解除** | `DeviceInterface.EmergencyStop(reason_code)` ➔ `device_manager_dbus.cpp:handle_emergency_stop()` ➔ `latch_emergency_stop()` / `ForwardInterface.EmergencyStop` ➔ `forward_control.cpp:forward_service_emergency_stop()`（先单播 `0x02 MC` 4B ACK，延时 `45ms` 再单播 `0x03 TH` 要求固定 `4B CMD_ACK`）➔ MC 级联转发 ➔ `mcu-p3:color-engine-mcu/io_toggle/src/app/minimc_proto.c:minimc_proto_poll()` ➔ `dispatch_th_command()` `[EXTRACTED]` ➔ `handle_th_motion_stop()` `[EXTRACTED]`。 | ① `minimc_proto.c:666-670` 对 `plen == 1U` 特判调用 `finalize_th_resp_frame(out_buf, 0U)` 返回 `14B`（`0B` 载荷 ACK），被 `Forward` `min_resp_len=4` 丢弃致 `200ms` 超时（`-8`）；<br>② 第 658–661 行未区分 `frame[12] == 0U`（解除），解除时仍执行 `quickStop()`、清零目标温度并入队 `"M112"`；<br>③ `test_twin45_th_debug.c:1054` 存量断言仍写死 `14U`。 |
| **`BOOT-MC-STAY-01` MC 复位窗口与 `0x01` 轮询** | `boot/bootloadermc:bootloader/src/main.c:main()` ➔ `boot_uart_ota_init()`（检测 `0x2005FFF0 == UPG2`）➔ 主循环 `boot_uart_ota_poll()` ➔ `feed_frame_byte()` ➔ `dispatch_valid_frame()` `[EXTRACTED]` ➔ `handle_cmd_get_version()` `[EXTRACTED]` ➔ `main.c:210` `boot_uart_ota_should_stay_in_boot()` 控制 `2000ms` `handle_no_disk_timeout()` ➔ `jump_to_app(0x08020000)`。 | `boot_uart_ota.c:327` 在处理只读 `0x01 CMD_GET_VERSION` 时执行 `s_ota.stay_in_boot = 1U;`，与 AP 守护进程每 `500ms` 常规版本轮询碰撞，导致任何非升级复位进入 `2.0s` 探测窗后 `boot_uart_ota_should_stay_in_boot()` 恒为 `1U`，永久锁死在 Bootloader。 |

#### 2.2.2 PM 待决项 `OI-01` ~ `OI-05` 逐项消解结论

1. **`OI-01`（包状态与错误粒度）已消解**：
   - 核查确认现有 `state/ota_status` 仅含布尔 `valid` 与顶层 `error`，无法区分「初始未扫描」「单文件缺失」「包头/CRC/SHA 损坏」「签名失败」，且 `prepare_images()` 在 `fw_mc.bin` 缺失时会短路跳过 `fw_th.bin`。
   - **消解方案**：在 `Forward` 内部为 `mc`/`th` 子对象增补只读定长字段 `"scan_state"` 与 `"scan_error"`，并在 `operation == 0U` 时完整扫描请求掩码内的全部节点；前端结合 `AisocSnapshot` 的 `dm_connected` 与 `mc.online`/`th.online` 实现零歧义五态与下一步指引，无需 UI 越权直接访问 `/run/printer-soc/firmware/`。
2. **`OI-02`（校验策略文案来源）已消解**：
   - 核查确认 `ota_image.cpp:59` 通过编译宏 `AISOC_OTA_INTEGRITY_ONLY_HIL` 切换策略，但 `forward_ota.cpp:build_snapshot()` 未向 DDS 暴露该策略。
   - **消解方案**：在 `build_snapshot()` 顶层 JSON 增补只读字段 `"policy"`（`"integrity-only-hil"` 或 `"signature-required"`）。Helix `OtaLocalOverlay` 在 `READY` 态按后端真实上报的 `policy` 动态展示 `固件包完整性校验通过...`（`integrity-only-hil`）或 `固件包签名与完整性校验通过...`（`signature-required`），静态按钮描述统一采用策略中性的准确表述（“校验包完整性”），彻底根除谎称“已通过 ECDSA-P256 验签”。
3. **`OI-03`（默认中文 `"zh"` 语言码真值、存量 `/data` 一次性迁移与全量 `zh` 字形覆盖）已消解**：
   - **语言代码真值与中文菜单映射（物理核实）**：
     - 核实 `system_settings_manager.cpp:47`（`LANGUAGE_CODES[] = {"en", "de", "fr", "es", "ru", "pt", "it", "zh", "ja"}`，下拉项第 7 项显示 `"中文"`）、`config.cpp:2880`（`/language`）与 `translation_loader.cpp:44`（加载 `ui_xml/translations/<lang>.xml`）：中文精确配置键值为 **`"language": "zh"`**（非 `"zh_CN"`），且 `ui_xml/translations/zh.xml`（`227,258 B`）已随 `package.py:42-46` 完整打入 C308L 生产包。
     - 切为 `"zh"` 后，`translations/zh.yml` 标准菜单映射精确为：`SETTINGS` ➔ `设置`、`Display & Sound` ➔ `显示与声音`（`Brightness` ➔ `亮度`、`Language` ➔ `语言`）、`System` ➔ `系统` ➔ `Network Settings` ➔ `网络设置` ➔ `Ethernet` ➔ `以太网`、`Help & About` ➔ `帮助与关于` ➔ `About` ➔ `关于`；AISoC 专属中文标签未配置英文 `label_tag`，在 `"zh"` 与 `"en"` 下均原样展示中文。
   - **存量 `/data` 持久化配置一次性迁移机制（兼容 `Config::init` 滚动备份与用户手动切换）**：
     - 实板 `192.168.1.101` 的 `/data/printer-soc/helix/config/settings.json` 与 `$HOME/.helixscreen/settings.json.backup`（`app_constants.h:208`）已留存 `r18b` 的 `"language": "en"` 且 `config_version > 0`。
     - 在 `live-profile.json` 设 `"language": "zh"` 与 `"c308l_default_lang_migrated": 1`；`c308l_services.py:prepare_panel_settings()` 与 `printer-soc-panel` 首次播种时落盘 `.helix-fresh-install`（对齐 `config.cpp:1836`），并对已存在且未含 `"c308l_default_lang_migrated"` 的 `settings.json` 及 `.helixscreen/settings.json.backup`（仅当 `assets/config/settings.json` 默认语言为 `"zh"` 时触发）执行一次性 `"en"/空 -> "zh"` 迁移并写入 `"c308l_default_lang_migrated": 1`。当用户后续在 UI 手动切回 `"en"` 时，`Config::save()` 持久化整個 `nlohmann::json data` 对象从而保留 `"c308l_default_lang_migrated": 1`，下次重启不再覆盖用户选择；同时 `cjk_font_manager.cpp` 在 `#ifdef HELIX_ENABLE_AISOC` 下保持 `needs_cjk() == true`，确保用户切回 `"en"` 时 AISoC 中文项依然零豆腐块。
   - **全量 `zh.xml` 与新增文案 CJK 字形覆盖率（物理逐码位核实）**：
     - 宿主机与 QA 容器均无 `lv_font_conv` 及 `.otf` 源字体，不重生成字库。逐字节解析全部 29 个 `assets/fonts/cjk/noto_sans_cjk_*.bin` 的 `cmap` 表并与 `noto_sans_*.c` 求并集核对：
       1) `ui_xml/translations/zh.xml` 全量 `886` 个非 ASCII 码位中，**全部中文汉字与中文标点 100% 覆盖（`885/886`，汉字缺字数 = `0`）**；唯一未收录符号为 9 国语言共有的多喷头耗材提示箭头 `→`（`U+2192`，位于 `zh.yml:2692` `'Tool {} → Slot {}'`，不在 C308L 单喷头及本轮页面范围内）。
       2) 半角 `(MC/TH)` 与全角 `（MC／TH）` 均在字库内，**全仓统一采用半角括号标题 `本地固件升级 (MC/TH)`**；同时避开 `.bin` 未收录的 `勾/双/往/策/真/订/阅` 7 字，锁定下表 **100% 字库已覆盖（实测缺字数 = `0`）** 的标准文案，并在门禁脚本中加入自动字形覆盖断言：

   | 界面位置 / 状态槽 | 经字库 `cmap` 100% 物理核验的精确落地文案（零缺字） |
   | --- | --- |
   | `settings_panel.xml` 新增行 & `about_settings_overlay.xml:157` | 主标题：`本地固件升级 (MC/TH)`；副标题：`从固定目录扫描、校验并升级 MC/TH 固件` |
   | `ota_local_overlay.xml:34,37` 按钮副标题 | 扫描：`扫描 /run/printer-soc/firmware/ 并校验固件包完整性`<br>开始升级：`接收后台 OTA 进度并在重启后核验 App 模式与 boot_id` |
   | 初始未扫描（`UNSCANNED`） | 升级状态：`等待扫描本地固件（请点击“扫描固定目录固件”检查 /run/printer-soc/firmware/）`<br>TH/MC 包行：`fw_th.bin: 未扫描（点击下方扫描）` / `fw_mc.bin: 未扫描（点击下方扫描）` |
   | 节点包就绪（`READY`） | 包行：`已就绪 · <file> (<size>B, sha:<前12位>..)`<br>升级状态（`integrity-only-hil`）：`固件包完整性校验通过，请确认目标与安全开关后开始升级`<br>升级状态（`signature-required`）：`固件包签名与完整性校验通过，请确认目标与安全开关后开始升级` |
   | 节点缺包（`MISSING`） | 缺失节点行：`缺失 · 未找到 <fw_mc.bin|fw_th.bin>（请放入 /run/printer-soc/firmware/ 后重扫，或取消选择该板）`<br>总状态（全缺）：`固定目录未找到可升级固件包，请放入 fw_th.bin / fw_mc.bin 后重新扫描` |
   | 校验失败（`INVALID` / `SIGNATURE_INVALID`） | 节点行：`校验失败 · 包完整性或板型不匹配（请替换有效包后重扫）` 或 `校验失败 · 发布签名校验未通过（请替换有效签名包后重扫）`<br>总状态：`固件包校验未通过，请核对节点提示并替换有效包后重新扫描` |
   | 离线 / 未连接 / 忙锁 / 急停 | `状态: 本地服务未连接（请检查后台服务后重试）` / `状态: 节点离线（请检查板卡连接待恢复 ONLINE 后重试）` / `状态: 后台已锁定 (BUSY)` / `状态: 本地急停已锁存（板卡未全部应答）` / `状态: 设备已确认急停` |
   | 按钮本地拦阻 Toast | 缺选择或未开安全确认：`请选择升级节点并开启安全前置确认`<br>所选节点未扫描或未就绪：`请先扫描固件并确认所选节点固件包校验通过` |
   | 升级中 / 待核验 / 完成 / 失败 | 升级中：`升级进行中请勿断电：阶段 <phase> (<pct>%)`<br>待核验：`传输已提交，等待重启回 App(Bit31=0) 并核验版本与 boot_id...`<br>完成：`100% 升级完成，已回 App 且核验通过（可切回“关于”页复查版本）`<br>失败：`升级失败: <error>（请核对设备在线状态与故障原因后重扫重试）` |

4. **`OI-04`（最终候选配套可扫描固件产出与部署方式）已消解**：
   - 本轮统一合并切片定为 **`SLICE-09`**（原延后 P1 运动/打印控制切片顺延为 **`SLICE-10+`**，保持 `SLICE-01`~`SLICE-08` 历史账本与证据零改动）。
   - 单候选合龙时，宿主机 `integration_cmd` 基于 `mcu-p3@feat/soc-debug` 最终提交执行 `motion-controller-mcu` 与 `color-engine-mcu/io_toggle` 的 `make clean && make pack`（自动注入 8 位 `HEAD` 短提交并由 `mcu-p3/tools/pack_firmware.py` 生成带 `ATSG` 头、`CRC32` 与 `SHA-256` 的 `fw_mc.bin` / `fw_th.bin`），连同 `boot/bootloadermc` 交叉编译产物 `bootloader.bin` 一并校验摘要后归档至 `project-control/docs/evidence/SLICE-09/candidate_mcu_artifacts/artifacts_manifest.json`。由于 `qa_runner.py` 的只读容器 `sha256:94adbc...` 内仅装有宿主机 `gcc/g++` 与 C308L Linux 交叉链（无裸机 `arm-none-eabi-gcc`），容器内执行 `printer-soc` C308L 全量构建制镜（`--hil-ota-integrity-only`）及 `mcu-p3`、`bootloadermc` 全部宿主机 `gcc` 单测套件，宿主机合龙门禁强制核验 `artifacts_manifest.json` 绑定的 `MCU_P3_COMMIT` 与 `BOOT_MC_COMMIT` 严格等于各自 `HEAD` 40 位 SHA。
   - 实机部署时，`printer-soc-rootfs.tar.gz` 默认保持 `/run/printer-soc/firmware/` 为空，天然支撑先做 `UX-02` 缺包负例，再通过 `scp` 置入上述同源 `fw_th.bin` + `fw_mc.bin` 执行触屏升级正例。
5. **`OI-05`（单台架实测顺序与解耦编排）已消解**：
   - 按 **`UX-01`（刷前 `r18b` 现状）➔ `Human Gate #2A` 部署候选 AP rootfs ➔ `UX-02` 缺包负例（双缺+单缺）➔ `UX-02` 置入同源包真实触屏双板 OTA（同步将含 `TH-ESTOP-01` 的 `fw_th.bin` 刷入 TH 板并完成同一事务四方对账）➔ `TH-ESTOP-01` 真机急停锁存/解除闭环 ➔ 独立 `Human Gate #2B` 获批后执行 `BOOT-MC-STAY-01` SWD 烧录 `0x08000000` 与 `0x01` 轮询下复位自愈及 OTA 回归** 顺序执行。该次序保证：① 零重复刷写；② 即使 `Human Gate #2B` 暂缓批准，前三项仍可独立取得完整真机实证，`BOOT-MC-STAY-01` 实板项诚实保留“待验证”。

#### 2.2.3 软硬件与跨仓协议契约推演

- **MiniMCProto v2 协议帧与单一契约源**：`project-control/contracts/minimc_v2_contract.yaml` 保持零变更。
  - `0x17 (CMD_EMERGENCY_STOP)`：AP `Forward` 固定发送 `1B` 载荷（`1=急停锁存`，`0=解除锁存`），先单播 `0x02 (MC)`、间隔 `45ms` 再单播 `0x03 (TH)`，每跳超时预算 `200ms`（921600 bps 下 `15B` 请求 + `18B` 响应物理传输仅约 `0.36ms`）。`TH App` 修复后对 `plen <= 1U` 的单播 `WANTS_ACK` 帧统一返回 `18B`（`12B` 头 + `4B minimc_ack_payload_t [queue_free, rx_free_units, 0x00, 0x00]` + `2B CRC16`），广播帧（`dst_id=0xFF`）继续静默不回 ACK。
  - **DeviceManager 快照与摘要字段精确映射**：物理核实 `device_manager_types.h:94`、`device_manager_dbus.cpp:207-282` 与 `device_manager_state.cpp:704-744`，`GetSnapshot()` 与 `GetDeviceState()` 同时输出权威布尔字段 `"estop_latched"` 与 `"estop_confirmed"`（解耦易被后续传感器/板卡故障改写为 `"FAULT"` 的 `system_status` 字符串）：锁存前 `{"device_state":"IDLE","system_status":"ONLINE","estop_latched":false,"estop_confirmed":false}` ➔ `EmergencyStop(1)` 经 MC+TH 双板 `4B ACK` 确认后 `{"device_state":"FAULT","system_status":"EMERGENCY_STOP_INVOKED","estop_latched":true,"estop_confirmed":true}`（若下游单板超时则保持 `"estop_latched":true,"estop_confirmed":false`，UI 如实提示“本地急停已锁存（板卡未全部应答）”，绝不谎报设备已确认）➔ `EmergencyStop(0)` 双板 `4B ACK` 成功后恢复 `{"device_state":"IDLE","system_status":"ONLINE","estop_latched":false,"estop_confirmed":false}`。
- **Flash 分区、VTOR、SRAM 魔数与中断/超时预算**：
  - `bootloadermc`（`AT32F435VGT7`）：Bootloader 位于 `0x08000000`（上限 `128 KB = 131,072 B`），App 位于 `0x08020000`（上限 `896 KB = 917,504 B`），跳转前执行 `200ms` USB SE0 断开、`__disable_irq()`、复位 `USART1/USART2/DMA1/OTGFS1/SysTick`、清空 `NVIC->ICER/ICPR` 并设置 `SCB->VTOR = 0x08020000`。移除 `handle_cmd_get_version()` 中的 `s_ota.stay_in_boot = 1U` 后，仅当检测到 `0x2005FFF0 == 0x55504732 ("UPG2")`、收到 `0x1D(action=2)`、收到合法 `0x20 (CMD_OTA_START)` 持锁、或插入 U 盘升级时才驻留 Bootloader；常规复位下即使 `500ms` 收到 AP `0x01` 查询，仍正常回复 `0x02 (capability_flags=0xC0080435, Bit31=1)` 并在 `2000ms` 窗口届满后自动跳入 `MC App`。
  - **零动态内存与静态缓冲预算**：`TH App` 与 `bootloadermc` 全程零 `malloc/free`；`Forward` `ota_internal.h` 仅在单实例静态结构 `fwd_ota_runtime` 增加 `2*(24+32) = 112 B` 定长字符数组，序列化后的 `state/ota_status` JSON 峰值约 `670 B`，严格低于 `aisoc_ota_status_t::json` `1024 B` 上限。

---

### 2.3 `Design-It-Twice` 接缝比选与最小修改预算（分仓 `Diff Budget`）

#### 2.3.1 接缝比选：`UX-02` 单节点缺包/校验状态与策略感知边界

- **备选方案 A（纯 Helix 前端解析现有字段 + 前端直接 `stat()` 固件目录）**：
  - 保持 `Forward` 不变，由 `OtaLocalOverlay` 自行调用 POSIX `stat("/run/printer-soc/firmware/fw_*.bin")` 推断缺包，再结合旧 `valid`/`error` 拼接提示。
  - **缺陷（否决）**：① 破坏 `forward_ota.cpp` 单一目录所有者边界，引入 UI 观测与后端实际读取之间的 TOCTOU 竞态；② 无法修复 `prepare_images()` 在 `fw_mc.bin` 缺失时短路跳过 `fw_th.bin` 扫描的真实后端缺陷（导致单存 `fw_th.bin` 时前端也拿不到 `th.sha256`、无法单板升级 TH）；③ 无法感知后端真实编译的验签策略。
- **选定方案 B（`Forward` `ota_image/forward_ota` 增补只读 `scan_state`/`scan_error`/`policy` + Helix 纯视图呈现）**：
  - `Forward` 仍是唯一触碰 `/run/printer-soc/firmware/` 的深模块：扫描任务（`operation==0`）独立完成所选双节点文件打开与头/摘要/签名核验，逐节点输出窄状态码 `scan_state`、`scan_error` 与顶层 `policy`，已就绪节点保留有效 `sha256` 供单板勾选升级；Helix `AisocConnection` 与 `OtaLocalOverlay` 仅做只读解析与文案映射。
  - **优势（采纳）**：零假状态、零跨进程文件竞态、一次性打通“单缺一包仍可展示并单升另一板”的产品闭环，且向后完全兼容既有 `state/ota_status` 字段与 `test_ota_e2e.py`。

#### 2.3.2 分仓最小修改预算（`Diff Budget` 硬门禁）

| 责任角色 | 目标仓库与分支 | `max_files` | 受保护存量 `protected_globs` | `max_protected_lines` | 预计净改动规模与编码门禁约束 |
| --- | --- | :---: | --- | :---: | --- |
| `INTEGRATOR`（`UX-01`） | 全业务仓只读 | **`0`** | — | `0` | 仅向 `project-control/docs/evidence/SLICE-09/ux01_r18b_walkthrough/` 归档走查证物 |
| `ENG-AP`（`UX-02` + `S09-01`~`S09-05`） | `printer-soc@main` | **`24`** | `["*services/helixscreen/include/ui_panel_settings.h", "*services/helixscreen/src/ui/ui_panel_settings.cpp", "*services/helixscreen/src/system/cjk_font_manager.cpp", "*tests/device_manager/twin/test_device_manager.cpp"]` | **`60`** | 受保护存量改动约 `38` 行；新增的 `device_manager_types.h`、`device_manager_state.cpp`、`device_manager_dbus.cpp` 已实测原生通过 `fast_gate.py`，其余自研/配置/脚本/单测文件强制全中文注释/docstring、函数 $\le 50$ 行、入参 $\le 4$ 个 |
| `ENG-MCU`（`TH-ESTOP-01`） | `mcu-p3@feat/soc-debug` | **`3`** | `[]`（全量接受静态门禁扫描） | `0` | 3 文件合计改动约 `45` 行；须同时满足 `fast_gate.py` 与 `color-engine-mcu/tests/run_tests.sh`（禁嵌套三目、单 `if` 逻辑运算符 $\le 2$ 个、函数 $\le 50$ 行、入参 $\le 4$ 个） |
| `ENG_BOOT_MC`（`BOOT-MC-STAY-01` + `S09-06`） | `boot/bootloadermc@soc_debug` | **`4`** | `[]`（`boot_uart_ota.h`、`main.c` 等 4 文件均原生通过 `fast_gate.py`） | `0` | 4 文件合计改动约 `65` 行；严格锁定 `soc_debug` 分支（禁写 `main`），满足 `<=128KB` Flash 预算、零 `USART6` 耦合及函数 $\le 50$ 行 / 入参 $\le 4$ 个 |

---

### 2.4 有序切片规划（切片映射与 `SLICE-09` 完整可执行规格）

#### 2.4.1 切片编号映射与并行拓扑

- **历史基线冻结**：`SLICE-01` ~ `SLICE-08` 已结项账本与证据原样保留。
- **本轮切片定义**：新建 **`SLICE-09`**（批次 `BATCH-HELIX-P0-02`，`profile: "c308l-system"`，`depends_on: ["SLICE-08"]`，`requires_hil_immediately: true`）作为四项合并的**唯一正式交付候选**；原路线图中待排期的 P1 运动/打印控制接入顺延为 **`SLICE-10+`**。
- **并行与汇合关系**：
  - **并行流 1（实板基线取证 `S09-UX01`）**：`INTEGRATOR` 在刷入新候选前率先在 `r18b` 实板上完成 §1.5 走查取证（零代码修改）；
  - **并行流 2（三仓并发开发 `S09-AP` / `S09-MCU` / `S09-BOOT-MC`）**：`ENG-AP`、`ENG-MCU`、`ENG_BOOT_MC` 互无源码编译依赖，按契约并行编码、本地自检并线性提交推送至各自受控分支；
  - **单候选汇合门禁**：三仓候选 Commit 齐备后，统一进入 `SLICE-09` 四阶门禁产出唯一 `SW-Verified` 候选与配套同源 `fw_mc.bin` / `fw_th.bin` / `bootloader.bin`，再转入单台架顺序实机验收。

#### 2.4.2 子任务精确接口签名、实现契约与验收命令

1. **`S09-UX01`｜`r18b` 现状走查取证与证据措辞收敛（`INTEGRATOR` / `COORD`，全业务仓只读 `max_files=0`）**：
   - **输入（Consumes）**：台架在跑 `SLICE-08 r18b` 候选（`printer-soc@6f28023f`）及 §1.5 走查表（`CHK-01`~`CHK-06`）。
   - **产出（Produces）**：`project-control/docs/evidence/SLICE-09/ux01_r18b_walkthrough/UX01_WALKTHROUGH_REPORT.md` 及对应照片/截屏、背光节点读数、`ip addr`、`/run/printer-soc/firmware/` `ls` 与 `panel.log`/`forward.log`，逐项按 5 类标准定性卡点；同步闭环冷审两项证据 `MINOR`：**`S09-08`** 将 `UX01_WALKTHROUGH_REPORT.md` 中 `CHK-06` 时间差严格限定表述为后台同一 `task` 的 `PRECHECK` 至 `FAILED` 阶段日志时间戳差（`<1ms`），不混同为客户端 RPC 往返耗时；**`S09-07`** 在最终候选固化后同步 `resource_assessment/RESOURCE_ASSESSMENT_REPORT.md` 的 AP 候选 Commit SHA 与候选列标题。
2. **`S09-AP`｜默认中文与存量迁移、升级双入口、扫描当次一致性、请求序号绑定及急停双布尔分离（`ENG-AP`，`printer-soc@main`）**：
   - **精确接口与结构变更（Produces / Consumes）**：
     - `live-profile.json` / `c308l_services.py` / `printer-soc-panel`：
       - `live-profile.json`：`settings.language = "zh"`，`settings.c308l_default_lang_migrated = 1`；
       - `def migrate_default_language_once(data: dict, default_lang: str) -> bool:` 与 `def sync_panel_backup_language(panel_config: Path, default_lang: str) -> None:`（均含中文 docstring、`<=50` 行、`<=4` 入参），由 `prepare_panel_settings(assets: Path, panel_config: Path, sys_input: Path = None) -> None` 调用；首次播种 `settings.json` 时写入 `panel_config / ".helix-fresh-install"`；`printer-soc-panel` 保持等价一次性迁移语义，并在 `test_tools.py`、`test_product_package.py` 增补正反单测。
     - `device_manager_types.h` / `device_manager_state.cpp` / `device_manager_dbus.cpp`（`S09-01`）：
       - `device_manager_state_t` 新增 `bool estop_confirmed;`；`dev_state_init_snapshot()` 清零 `estop_latched` 与 `estop_confirmed`；`latch_emergency_stop()` 置 `estop_latched = true, estop_confirmed = false`；`handle_emergency_stop()` 仅当 `reason_code == 1U && fwd_err == 0` 时置 `estop_confirmed = true` 并递增 `generation_id`；`clear_emergency_stop_state()` 同时清零两者；`dev_state_get_snapshot_json()` 与 `dev_state_get_summary_json()` 输出 `"estop_latched":true|false,"estop_confirmed":true|false`。
     - `ota_internal.h` / `ota_image.cpp` / `forward_ota.cpp`（含 `S09-03`）：
       - `bool ota_load_image(fwd_ota_runtime* rt, uint8_t index);`（保持原签名，内部更新 `rt->scan_state[index]` 与 `rt->scan_error[index]`；`prepare_command()` 初始置 `"UNSCANNED"` / `""`，并对 `operation == 0U` 扫描任务或 `operation == 1U` 未选节点同步清空 `rt->image[index].valid = false; size = 0U; version = 0U; sha256[0] = '\0'; warning[0] = '\0';`；`prepare_images()` 在 `rt->operation == 0U` 时遍历完 `0..1` 中匹配 `rt->mask` 的全部节点后再汇总终态）。
       - `state/ota_status` JSON 新增向后兼容键：顶层 `"policy":"integrity-only-hil"|"signature-required"`，以及 `mc`/`th` 内 `"scan_state"`、`"scan_error"`。
     - `aisoc_connection.h/.cpp`（含 `S09-01`~`S09-03`）：
       - `AisocSnapshot` 增 `bool estop_confirmed = false;` 并从权威布尔键解析；`AisocOtaNodeInfo` 含 `scan_state`/`scan_error`；`AisocOtaStatus` 含 `policy` 与 `uint64_t client_req_seq = 0U;`；`uint64_t AisocConnection::request_ota(const AisocOtaRequest& req)` 返回单调递增 `req_seq` 并在工作线程执行及绑定 `task_id` 期间透传至 `AisocOtaStatus::client_req_seq`；`check_ota_upgrade_gate()` 对所选节点同时要求 `scan_state == "READY" && valid && sha256.size() >= 12U`。
     - `ui_panel_settings.h/.cpp` & `settings_panel.xml`：
       - `static void SettingsPanel::on_settings_local_ota_clicked(lv_event_t* e);` ➔ 调用 `helix::settings::get_ota_local_overlay().show(get_global_settings_panel().parent_screen_);`。
     - `cjk_font_manager.cpp`：
       - `bool CjkFontManager::needs_cjk(const std::string& lang)`：在 `#ifdef HELIX_ENABLE_AISOC` 下返回 `true`（默认 `"zh"` 原生启用，且防止用户手动切回 `"en"` 时卸载 CJK fallback 字库；非 AISoC 构建保持 `lang == "zh" || lang == "ja"`）。
     - `ui_settings_ota.h/.cpp`（含 `S09-01`~`S09-04`）：
       - `static std::string format_ota_pkg(const char* label, const helix::aisoc::AisocOtaNodeInfo& info);`（同时要求 `info.scan_state == "READY" && info.valid && info.sha256.size() >= 12U`）
       - `static std::string format_ota_phase(const helix::aisoc::AisocOtaStatus& st);`
       - `pending_scan_seq_` 严格匹配 `st.client_req_seq` 后方消费 `scan_feedback_pending_` 弹出扫描结果 Toast；`busy` 仅读取 `st.active || st.last_rpc_code == -5 || snap.maintenance_locked`（不读 `last_estop_outcome == BACKEND_BUSY`，保留 `application.cpp:2034` 全局一次性急停 Toast）；区分 `snap.estop_confirmed`（`状态: 设备已确认急停`）与 `snap.estop_latched && !snap.estop_confirmed`（`状态: 本地急停已锁存（板卡未全部应答）`）。
     - `tests/device_manager/twin/test_device_manager.cpp`（`S09-01` & `S09-05`）：
       - `setup_dev_test_env()` 先初始化测试客户端并在启动 `dev_thread` 前设定 `next_identity_probe_ns = now + 1500000000ULL`，确定性暴露初始 `OFFLINE + valid:false` 状态供 `test_rpc_get_version_info` 断言，随后在 `test_rpc_identity_fields` 显式归零 `next_identity_probe_ns` 触发真实探测；同步覆盖急停双板确认、单板超时仅本地锁存、锁存期故障上报不丢锁与外部解除。
   - **本地自检命令**：CMake 构建 `build_ps` 与 `build_ps_hil` ➔ 运行双套 `ctest`、`test_ota_e2e.py`（双策略含移走未选包新用例）、`test_aisoc_p0`（含 `S09-01`~`S09-04` 新用例）、`test_tools.py`、`test_product_package.py` 及 AISoC XML/C++ 中文字符 `.bin` 字形 100% 覆盖检查。
3. **`S09-MCU`｜TH App `0x17` 锁存/解除 `4B ACK` 与解除语义修复（`ENG-MCU`，`mcu-p3@feat/soc-debug`）**：
   - **精确接口与行为契约**：
     - `static uint16_t handle_th_motion_stop(const uint8_t *frame, uint16_t plen, uint8_t *out_buf);`（保持原签名，`<=50` 行，`<=4` 入参，单 `if` 逻辑操作符 `<=2` 个）：
       1) `plen > 1U`：单播且 `WANTS_ACK` 返回 `build_nack_resp(src_id, seq, 0x02U, out_buf)`，否则返回 `0U`；
       2) `plen == 1U && frame[MINIMC_HEADER_SIZE] > 1U`：单播且 `WANTS_ACK` 返回 `build_nack_resp(src_id, seq, 0x03U, out_buf)`，否则返回 `0U`；
       3) 仅当 `(plen == 0U) || (frame[MINIMC_HEADER_SIZE] == 1U)`（急停锁存/无参急停）时执行 `quickStop()`、`thermistor_set_target_deci_c(0)`、`load_filament_Flag = 0` 及 `(void)th_control_enqueue_gcode("M112", 4U, true)`；当 `plen == 1U && frame[MINIMC_HEADER_SIZE] == 0U`（解除急停）时**不执行**上述关断与 `"M112"` 入队；
       4) 若为广播（`dst_id == MINIMC_NODE_BROADCAST`）或未置 `MINIMC_FLAG_WANTS_ACK` 返回 `0U`；其余单播请求**统一调用 `build_ack_resp(src_id, seq, out_buf)` 返回标准 `18B`（`4B CMD_ACK`）响应帧**。
   - **本地自检命令**：`(cd mcu-p3/color-engine-mcu/tests && sh run_tests.sh) && (cd mcu-p3/motion-controller-mcu/tests && sh run_tests.sh)`，并执行双目录 `make clean && make pack` 验证 ARM 交叉编译零警告/零错误。
4. **`S09-BOOT-MC`｜MC Bootloader 只读 `0x01` 不置驻留位与生产 `2000ms` 窗口判定覆盖（`ENG_BOOT_MC`，`boot/bootloadermc@soc_debug`）**：
   - **精确接口与行为契约**：
     - `static void handle_cmd_get_version(const minimc_frame_hdr_t *p_req);`（`bootloader/src/boot_uart_ota.c:320`）：删除 `s_ota.stay_in_boot = 1U;`，其余 `16B 0x02 CMD_VERSION_REPORT` 字段（`proto=2.0`, `fw=1.0`, `boot_id`, `MC_FW_GIT_COMMIT_SHORT`, `MC_BOOT_CAPABILITY_FLAGS=0xC0080435`）完全不变；
     - `uint8_t boot_uart_ota_should_stay_in_boot(void);`：仅在 `UPG2` 魔数命中、收到 `0x1D(action=2)`、或 `0x20` 串口升级会话激活（`s_ota.stay_in_boot != 0U || s_active_writer == BOOT_WRITER_UART2`）时返回 `1U`；
     - `uint8_t boot_uart_ota_should_jump_after_window(uint32_t probe_ticks, uint8_t udisk_connected, uint8_t upgrade_in_progress);`（`boot_uart_ota.h/.c`，`<=50` 行、`3` 入参）：基于 `BOOT_PROBE_WINDOW_MS (2000U)` 返回 `(upgrade_in_progress == 0U && boot_uart_ota_should_stay_in_boot() == 0U && udisk_connected == 0U && probe_ticks >= BOOT_PROBE_WINDOW_MS) ? 1U : 0U`，由 `bootloader/src/main.c` 主循环直接调用，并在 `tests/test_mc_boot_ota.c` 覆盖窗口届满前（`1999ms`）、`0x01/0x03` 轮询届满（`2000ms`）自动跳转、以及显式驻留/U盘连接/升级中越窗保持驻留（`S09-06`）。
   - **本地自检命令**：`(cd boot/bootloadermc && PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin sh tests/run_tests.sh)`（一次跑通交叉编译 `<=128KB`、零 `USART6`、`pack_firmware.py` 边界、`test_mc_boot_ota` 新旧用例及函数规模门禁）。

---

### 2.5 四阶软件门禁、单台架顺序实机验收编排与回滚预案

#### 2.5.1 单一最终候选四阶软件门禁漏斗（`slice_gate.py --slice project-control/slices/SLICE-09.yaml`）

1. **第 1 阶 `fast_gate.py`（`<3s` 机械门禁）**：
   - 校验 `minimc_v2_contract.yaml` 与 `c308l_platform_contract.yaml` 同步零漂移；
   - 强校验 `printer-soc@main`（$\le 24$ 文件，受保护改动 $\le 60$ 行）、`mcu-p3@feat/soc-debug`（$\le 3$ 文件）、`boot/bootloadermc@soc_debug`（$\le 4$ 文件，严禁 `main` 分支）路径白名单、全中文注释/docstring、自研函数 $\le 50$ 行 / $\le 4$ 入参、零未核实占位标记与零改字节垫片。
2. **第 2 阶 `integration_cmd`（宿主机跨仓全量合龙 + 同源固件包构建固化）**：
   - 运行 `printer-soc` 打包/工具单测（含 `live-profile.json` 默认 `"zh"` 与存量配置一次性迁移单测）+ **AISoC XML/C++ 字符串相对 `noto_sans_cjk_*.bin` + `noto_sans_*.c` 100% 字形覆盖校验脚本**；
   - 运行 `test_harness/hil/tests/test_helix_screen_integration.py --self-test`；
   - 运行 `mcu-p3` 双板单测（`motion-controller-mcu/tests/run_tests.sh` + `color-engine-mcu/tests/run_tests.sh`）及 `boot/bootloadermc` 全套构建与单测（`PATH=... sh tests/run_tests.sh`）；
   - 执行宿主机 ARM 交叉编译与 `ATSG` 打包产出与当前 `mcu-p3` `HEAD`、`boot/bootloadermc` `HEAD` 精确绑定的 `fw_mc.bin`、`fw_th.bin`、`bootloader.bin`，调用 `validate_atsg_base(..., check_crc=True)` 核验双包结构与板型（`0x43500001` / `0x42300001`），将制品与含 40 位 Commit SHA + SHA-256 的 `artifacts_manifest.json` 固化至 `project-control/docs/evidence/SLICE-09/candidate_mcu_artifacts/`（清理或忽略临时构建物，保持 Git 工作树 100% 洁净）。
3. **第 3 阶 `qa_runner.py`（只读 Docker 沙箱 `c308l-system` 全新远端检出构建回归）**：
   - 从 GitLab 服务端全新克隆锁定 Commit（`printer-soc`、`mcu-p3`、`boot/bootloadermc`、`boot/bootloaderth`、`test_harness`、`project-control`、`agents` 及 `sdk/c308l`）；
   - 执行 `printer-soc` 双模式构建（默认严签 + `AISOC_OTA_INTEGRITY_ONLY_HIL=ON`）、`test_aisoc_p0`、`release_product.py`（`plan --hil-ota-integrity-only` ➔ `build` ➔ `package` ➔ `system-image` ➔ `verify`，`FILE_FILTER=Y`、公钥 `0o444`、UBIFS 解包对账）、`ctest`、`test_startup_fail_fast.py`、`test_ota_e2e.py`（双策略含单缺包扫描新用例）、字形覆盖断言；
   - 在同一隔离容器内用 `gcc` 编译运行 `mcu-p3`（`test_twin44_mc_debug`、`test_mc_ota_and_relay`、`test_twin45_th_debug`、`test_th_ota_and_bootid`）与 `boot/bootloadermc`（`test_mc_boot_ota`）全部宿主机单测套件。
4. **第 4 阶 `codex_review.py`（独立异构 Codex 双轴冷审）**：
   - 围绕「Spec 覆盖与防伪真实性」及「嵌入式安全与 Diff 预算」双轴独立冷审，达成 `APPROVED (0 BLOCKER)` 后自动写入 `slices/ledger.md`（`SLICE-09 | SW-Verified`）并停机申请实板闸门。

#### 2.5.2 单台架顺序实机验收流程与双人工闸门（`root@192.168.1.101`）

> **全程安全底线**：加热占空比 `heating_pwm_pct == 0`（零设温、零加热）、零电机通电运动、`/etc/printer-soc/fw_signing_pub.pem` 保持 `0o444`、`/data/boot_backup.img` SHA-256（`59951adabc9f633332168ec2fa48443cf8cb385c6da9746f5795893c754b8c86`）前后恒定不变。

1. **阶段 H0（刷机前，与编码并行）：执行 `UX-01` `r18b` 现状走查**：
   - 确认台架仍为 `SLICE-08 r18b`（`git_sha=6f28023f`），从真实首页逐步完成 `CHK-01`~`CHK-06`（不执行写刷），归档实拍与 5 类卡点归因报告。
2. **人工闸门 `Human Gate #2A`（常规 AP 部署与串口 OTA / 急停验收授权）** ➔ 获批后执行 **阶段 H1~H3（全程 `probe_rs_used = false`）**：
   - **阶段 H1（部署最终候选 AP rootfs + 默认中文一次性迁移核验 + `UX-02` 缺包负例触屏验证）**：
     - 备份核验空间余量后将 `SLICE-09` 候选 `printer-soc-rootfs.tar.gz` 原子部署至 `/` 并重启服务，核验 `/etc/printer-soc/version.json` 匹配新 `printer-soc` SHA；核验存量 `/data/printer-soc/helix/config/settings.json` 已一次性由 `"en"` 迁移为 `"language": "zh"`（带 `c308l_default_lang_migrated: 1`），面板默认呈现全中文界面（`设置`、`显示与声音`、`系统`、`帮助与关于`）且零缺字方框；在 `显示与声音` → `语言` 手动切为 `English` 并执行 `printer-soc restart` 核验仍保持 `English`（且 AISoC 中文行无豆腐块），随后切回 `中文` 继续后续验收；
     - **负例 A（双缺）**：确认 `/run/printer-soc/firmware/` 为空，从首页 → `设置 (Settings)` 一级点击 `本地固件升级 (MC/TH)`（并从 `帮助与关于` → `关于 (About)` 页验证双入口打开同一页面）→ 点击扫描 → 核验双行均显示 `缺失 · 未找到 ...` 与放入目录指引，无“验签通过”字样，点击开始升级被明确阻断；
     - **负例 B（单缺）**：仅置入同源 `fw_th.bin` → 重新扫描 → 核验 `TH` 行显示 `已就绪 · fw_th.bin (...)`、`MC` 行仍显示 `缺失 · 未找到 fw_mc.bin`，双选点击开始升级被阻断。
   - **阶段 H2（`UX-02` 正例：置入同源双包，真实触屏发起双板串口 OTA 全流程与四方对账）**：
     - 将 `candidate_mcu_artifacts/` 下同源 `fw_mc.bin` 一并置入 `/run/printer-soc/firmware/` → 触屏点击扫描确认 `TH`、`MC` 双包就绪且提示为“固件包完整性校验通过” → 开启 `TH`、`MC`、`允许同版本重刷`、`安全前置确认` → 触屏点击 `开始本地 OTA 升级`；
     - 观测触屏实时阶段/百分比进度条与 `BUSY` 锁定提示直至显示 `100% 升级完成，已回 App 且核验通过`；切回触屏 `关于 (About)` 页复查 `MC`、`TH` 新版本/短提交与 `[App]` 模式；
     - 核对四方物证严格一致：① 触屏前后实拍；② `forward.log` 同一次 `task_id`（先 `TH` 后 `MC` 完成 Stage 1~4）；③ 双板在线 `git_commit` 均跃迁为 `mcu-p3` 最终候选 8 位短提交（含 `TH-ESTOP-01` 修复）；④ 双板升级前后 `boot_id` 均发生非零跃迁。
   - **阶段 H3（`TH-ESTOP-01` 真机急停锁存与解除闭环验证）**：
     - 在整机 `IDLE` 在线态下依次下发 `EmergencyStop(byte:1)` 与 `EmergencyStop(byte:0)`（同步验证触屏急停按钮反馈），采集串口双向帧、`forward.log` 与 `GetSnapshot`：
     - 核验 `MC(0x02)` 与 `TH(0x03)` 对锁存（`0x01`）和解除（`0x00`）均在 `200ms` 内返回标准 `18B`（`4B CMD_ACK`）且返回码均为 `0`（零 `-8` 超时），解除后 TH 未重入急停，`GetSnapshot` 完整走完 `IDLE/ONLINE -> FAULT/EMERGENCY_STOP_INVOKED -> IDLE/ONLINE` 闭环。
3. **独立高风险报批闸门 `Human Gate #2B`（`BOOT-MC-STAY-01` 实板 SWD 烧录 `0x08000000` 专项审批）**：
   - 执行前向用户单独呈报：`boot/bootloadermc@soc_debug` 40 位 Commit SHA、`bootloader.bin` 精确字节数与 SHA-256、探针 `--probe "0483:3748:75003800120000334C41534E"`、`--chip AT32F435VGT7`、目标首址 `0x08000000` 及回滚包摘要。
   - **获批后执行阶段 H4**：
     1) AP 切入 `printer-soc dev-mode` 释放 `/dev/ttyS1`，调用 `probe-rs download` 烧录 `bootloader.bin` 至 `0x08000000` 并复位；
     2) AP 执行 `printer-soc start` 恢复生产 `500ms` `0x01` 轮询；触发 MC 非升级复位，采集日志证明 MC 在 `2.0s` 窗口内正常应答 `0x01 -> 0x02 (Bit31=1)` 但不锁定驻留，`~2.0s` 后自动跳回 `MC App` 并恢复 `MC ONLINE`；
     3) 再触发一次 MC 串口重刷，验证显式驻留（`0x1D(action=2)` / `0x20`）与完整串口 OTA 恢复路径零退化。
   - **未获批 / 缺测诚实留白规则**：若用户暂缓批准 `Human Gate #2B`，立即跳过阶段 H4，将该项实板状态如实登记为 **`待验证 (Pending HIL - Awaiting Human Gate #2B)`**，绝不阻塞前三项实证归档，也绝不将整体验收虚标为全项实板通过。

#### 2.5.3 四项分报交付模板与故障回滚预案

- **四项分报标准结构（结项必须逐行如实填写，附 Git 服务端可读回 40 位 SHA 与收据路径）**：

  | 交付项 | 软件准出状态 | 真机实测状态 | 候选仓库与远端可读回 40 位 Commit SHA | 核心物证与收据路径（相对 `project-control/docs/evidence/SLICE-09/`） |
  | --- | :---: | :---: | --- | --- |
  | **`UX-01`（`r18b` 现状走查）** | `N/A（零改码）` | `PASS / 待验证` | 基线 `printer-soc@6f28023f...` | `ux01_r18b_walkthrough/UX01_WALKTHROUGH_REPORT.md` + 实拍/日志 |
  | **`UX-02`（升级双入口与五态体验）** | `SW-Verified` | `HIL-Verified / 待验证` | `printer-soc@<40-sha>`, `mcu-p3@<40-sha>` | `hil/ux02_missing_pkg_neg.log`, `hil/ux02_touch_dual_ota.log` + 触屏实拍 + `release-manifest.json` |
  | **`TH-ESTOP-01`（TH `0x17` 急停与解除）** | `SW-Verified` | `HIL-Verified / 待验证` | `mcu-p3@<40-sha>` | `run_*/docker_qa/runtime.log`, `hil/th_estop_0x17_cycle.log` |
  | **`BOOT-MC-STAY-01`（MC `0x01` 不驻留修复）** | `SW-Verified` | `HIL-Verified / 待验证（视 Gate #2B）` | `boot/bootloadermc@<40-sha>` (`soc_debug`) | `run_*/integration.log`, `hil/boot_mc_reset_selfheal.log`（若未刷实板则留空标待验证） |

- **分级安全回滚预案**：
  1. **AP 侧回滚（`printer-soc`）**：若新候选 rootfs 在实板上出现界面异常或服务回退，立即将已通过 `HIL-Verified` 的 `SLICE-08 r18b` `printer-soc-rootfs.tar.gz`（`76e9348b...`，`git_sha=6f28023f`）重新原子解压覆盖 `/` 并重启 `S90printer-soc`，1 分钟内无损恢复 `r18b` 基线。
  2. **MC / TH App 侧回滚（`mcu-p3`）**：保留 `SLICE-08` 已验证的 `fw_mc_r18.bin` 与 `fw_th_r18.bin` 原件；若新 App 出现异常，将其拷入 `/run/printer-soc/firmware/` 开启 `allow_reflash=true` 通过串口 OTA 直接回刷至 `mcu-p3@a64bffbf`（即使单板滞留 Bootloader，Bootloader 的 `0x20` 串口升级恢复路径仍可直接接收回刷）。
  3. **MC Bootloader 侧回滚（`boot/bootloadermc`，仅限 `Human Gate #2B` 执行后触发）**：烧录新 `bootloader.bin` 前，预先基于基线 `boot/bootloadermc@3e01c00ce4dfb5e9e749e79c3cfbc076e3680bf4` 编译留存黄金回滚镜像 `bootloader_3e01c00.bin` 并记录 SHA-256；一旦阶段 H4 出现启动或跳转异常，立即在同一 ST-Link 探针（`0483:3748:75003800120000334C41534E`）上执行 `probe-rs download --chip AT32F435VGT7 --binary-format bin --base-address 0x08000000 bootloader_3e01c00.bin` 恢复 `3e01c00` 原貌。

### 2.6 `S09-RES`｜资源评估取证（`v1.2` 增量，已批准）

`INTEGRATOR` 负责收集，AP、MC、TH 和 Bootloader 对应 Owner 复核测量口径。输入为 SLICE‑08 `r18b` 和 SLICE‑09 同一最终候选的完整 Git SHA、制品 SHA‑256 及构建配置。方案的 `v1.1` 审查基线可从 `project-control@8c455bf` 取回，当前 `r01` 四项门禁按该版本核对。评估复用只读采样与现有构建制品。新增固件埋点可量出 MCU 执行时间或实际栈峰值，但会改变待测固件及观测开销，留待单独评估。业务仓 Diff Budget 为 `max_files=0`、`max_protected_lines=0`。

| 端点 | 经源码、图谱核对的入口 | 取数来源与口径 |
| --- | --- | --- |
| AP | `printer-soc/tools/c308l_services.py:main() → query_status()`，`launch() → identity()` 经源码核实。图谱未抽取这些 Python 边。 | 采样前后执行 `printer-soc status`，根据 `controller`、`children` 的 PID、`start_ticks`、可执行文件及存活状态核对身份。由 `cat /proc/uptime /proc/stat /proc/meminfo` 与 `cat /proc/<pid>/stat /proc/<pid>/status` 采集样本。系统 CPU 以总 tick 增量扣除 idle 和 iowait 后的占比表示，服务 CPU 以 `utime+stime` 增量占整机总 tick 增量的百分比表示，总 tick 不重复加 guest。内存报各服务 `VmRSS` 观测峰值和整机 `MemAvailable` 观测最低值，单位 KiB。进程代次变化时分段，RSS 保留各进程独立值。 |
| AP 存储 | `printer-soc/tools/release_product.py` 生成发布清单，既有 Docker QA 归档 rootfs 包。 | `df -k / /data /run/printer-soc/firmware` 配合 `/proc/self/mountinfo` 逐挂载报使用量和可用量（KiB），固件包暂存目录在同一挂载时共用容量。用 `stat -c %s` 与 `sha256sum` 记录 rootfs 包和同源固件包字节数及身份，压缩包大小单列。 |
| MC App | `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c:drain_ap_rx() → handle_ap_frame() → handle_th_relay_req() → relay_frame()` 为图谱 `EXTRACTED` 边，已对照源码。 | `motion-controller-mcu/Makefile` 的 `make pack` 产出 `build/Marlin_AT32.elf`、`build/template.map`，链接规则见 `motion-controller-mcu/AT32F435xG_FLASH.ld`，Flash 上限 896 KiB。 |
| TH App | `mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c:dispatch_th_command() → handle_th_motion_stop()` 为图谱 `EXTRACTED` 边，已对照源码。 | `color-engine-mcu/io_toggle/Makefile` 的 `make pack` 对应 `build/fw_th.elf`、`build/fw_th.map`，链接规则见该目录 `libraries/cmsis/cm4/device_support/startup/gcc/linker/AT32F423xC_FLASH.ld`，Flash 上限 236 KiB，`RAM`、`BOOT_IPC` 与 `RAM_STACK` 独立核算。 |
| MC Bootloader | `boot/bootloadermc/bootloader/src/main.c:main() → handle_no_disk_timeout() → jump_to_app()` 为图谱 `EXTRACTED` 边，已对照源码。 | 复用 `tests/run_tests.sh` 的 `make all` 产物 `build/bootloader.elf`、`build/bootloader.map` 和 `build/bootloader.bin`。链接规则见 `cmake/linker/at32f435_bootloader.ld`，Flash 上限 128 KiB。 |
| TH Bootloader | `boot/bootloaderth/src/main.c:main() → boot_check_and_wait_handshake()` 为图谱 `EXTRACTED` 边，已对照源码。 | 复用锁定提交 `Makefile` 的 `make all` 产物 `build/bootloaderth.elf`、`build/bootloaderth.map` 和 `build/bootloaderth.bin`。链接规则见 `ldscripts/AT32A423xC_FLASH.ld`，Flash 上限 16 KiB。基线与候选若是同一锁定构建，则共用一份静态证据。 |

- **采样顺序**：优先采用已有且工况可匹配的 `r18b` 记录。台架仍运行 `r18b` 且已有采样授权时，在部署前补采空闲窗口。AP 在 H1 的候选稳定空闲和 H2 的现有双板 OTA 事务中以约 1 Hz 采样，空闲建议持续 60 秒。用主机日志时间和板端 `/proc/uptime` 对齐窗口，以 `task_id` 与 `forward.log` 对齐 OTA 阶段。记录日志和跟踪开关、启用服务、采样覆盖时段与板上版本。复用原验收操作，采样结束即退出。
- **MCU 只读核算**：在锁定制品上执行 `arm-none-eabi-size -A <ELF>`、`arm-none-eabi-objdump -h <ELF>`、`arm-none-eabi-readelf -lW <ELF>`，与 map 的 `Memory Configuration`、段表及 `_Min_Stack_Size` 对账。按分区首址至最高有效 Flash LMA 末址计算占用跨度（含 `.data` 的 Flash 装载映像与可烧录间隙），以实际链接/布局上限减去占用得出余量。App 经 `validate_atsg_base(..., check_crc=True)` 解析 `fw_mc.bin` / `fw_th.bin`，用净载核对 ELF 的 Flash 映像，ATSG 包总字节单列。各 RAM bank 按 VMA 分别统计静态区、对齐和编译期预留，独立注明 `_Min_Stack_Size`、堆预留及 `BOOT_IPC`，避免重复扣除。运行时 MCU CPU 和实际栈峰值在没有可核实观测时记为未测。缺少原制品时先比对锁定提交、工具链、配置及重建产物，重建差异和未能建立的关联如实记录。
- **交付与验收**：原始采样、ELF 段/链接映射摘录、制品身份及资源表统一归档于 `project-control/docs/evidence/SLICE-09/resource_assessment/`。表中逐项记录基线、候选、单位、工况、差值、既定容量余量和证据来源。准出复核时，PID 换代、制品身份不符、工况不匹配或样本缺失均标出相应缺测或不可比项，越分区或 RAM bank 上限列明实际值、上限及超额；不把缺测记为通过。没有既定阈值的观测项仅记数值和样本覆盖。若采样干扰 HIL，暂停采样并保留已有证据，恢复按 §2.5.3 执行。台架采样沿用 §2.5.2 的授权与顺序，无额外部署、刷写或压测步骤。

