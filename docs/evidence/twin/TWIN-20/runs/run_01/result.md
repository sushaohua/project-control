# TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-20` (HMI料槽映射、新机检查引导、国际化与局域网发现) |
| **所属工作包** | `TASK-009` (实现真实通信交互界面与双环境显示) |
| **执行角色** | `ENG-UI` (协力 `ENG-NET`, `ENG-STATE`) |
| **当前轮次** | `run_01` (料槽与调色板映射、OOBE真实向导、免刷新双语/主题、网关mDNS发现首轮交付) |
| **前置依赖** | `TWIN-02` (Done) |
| **执行状态** | **Completed (4通道料槽映射、10000混色校验、OOBE零伪造检测、中英免刷新/深浅主题、C轻量mDNS广播器及正反例全通)** |

---

## 1. 核心架构与功能实现 (Architecture & Implementation)

依据 `PM:FEAT-HMI-003`（料槽调色板映射）、`PM:FEAT-HMI-004`（新机检查向导）、`PM:FEAT-HMI-005`（多语言与主题）与 `PM:FEAT-NET-001`（局域网 mDNS 自发现）需求规范，`ENG-UI` 完成了以下核心功能交付：

### 1.1 HMI 料槽与耗材调色板映射 (`soc-ap/browser_hmi/first_release/`)
1. **4 通道供料系统完整覆盖 (Slot 1 ~ Slot 4)**：
   - 支持主流 3D 打印材料类型选择（`PLA`, `PETG`, `ABS`, `TPU`, `PC`, `PA-CF`）；
   - 支持原生拾色器与 HEX 颜色文本输入（带格式校验正则 `^#[0-9A-Fa-f]{6}$`），并配套高频常用预设调色板（红/蓝/绿/黄/橙/白/黑）；
   - 耗材余量估算：滑动条与数值联动（0%~100%），可视化进度条与克数估算；
2. **联动 TWIN-17 10000 混色基准权重校验 (COL-001)**：
   - 严格遵循 `total_mixing_weight == 10000` (100.00% 精度，0.01% 分辨率) 核心契约；
   - 提供快捷配比预设：单槽100% (`single-1`, `single-2`)、双槽50:50 (`dual-50`)、四槽均分25% (`quad-25`)；
   - 实时求和与偏差提示：若权重和不等于 10000，保存按钮强制置灰禁用，并明确显示偏差绝对值；
3. **后端契约一致性与持久化 (`slot_schema.json`)**：
   - 提供 JSON Schema 严苛校验契约；
   - REST 接口 `POST /api/v1/filament/slots` 提交，具备网络异常时的本地平稳回退。

### 1.2 新机检查引导向导 (OOBE - Out of Box Experience)
1. **5 步引导全交互流程**：
   - **Step 1: 欢迎 (Welcome)**：整机介绍与真实性规范公示；
   - **Step 2: 语言与主题 (Preferences)**：支持中英免刷新即时切换；
   - **Step 3: 固件与通信自检 (Firmware & Comm)**：检测 MC (AT32F435) 与 TH (AT32F423) UART 链路连通性及版本；
   - **Step 4: 传感器检测 (Sensors Check)**：喷头 NTC 温度有效性、热床 NTC 温度有效性、4 通道光电断料检测开关状态；
   - **Step 5: 就绪完成 (Completion)**：配置总览与保存，进入控制台；
2. **严格遵循真实性规则 (Realism Invariant - 零伪造硬防线)**：
   - 针对未检测/离线/无硬件连接项，**严禁全绿伪造成功**；
   - 在未接入真实硬件或处于脱机状态下，通信链路与传感器状态明确标示为警告色徽章**“未就绪/未连接/等待接入”**与**“未检查/离线”**；
   - 前端代码绝对零 `Math.random()` 假数据伪造。

### 1.3 国际化与双主题切换 (i18n & Themes)
1. **中英双语无刷新即时切换 (zh-CN & en-US)**：
   - 建立拥有 99 组键值对的完整中英字典对照表；
   - 页面文本、料槽属性、OOBE 向导、HMS 错误指引均实现全量覆盖；
2. **深浅双色高对比度主题 (Dark & Light)**：
   - 基于 CSS 自定义属性变量实现原生无缝瞬时切换；
3. **800x480 触摸屏人体工学优化**：
   - 所有触控操作热区尺寸严格满足 `min-height: 44px; min-width: 44px;`；
   - CSS 媒体查询针对小于等于 820px 的横屏触摸设备优化栅格折行与防误触间距。

### 1.4 网关端 mDNS 局域网服务发现 (`soc-ap/core/net/mdns/`)
1. **轻量级纯 C 组播广播器 (`mdns_advertiser.c`, `mdns_advertiser.h`)**：
   - 向标准组播地址 `224.0.0.251:5353` 发送 `_aisoc._tcp.local` 服务广播；
   - 严格组装 DNS 头部（ID=0, Flags=0x8400 权威响应, ANCOUNT=4）及 PTR、SRV、TXT、A 4 类标准资源记录；
   - SRV 记录绑定目标主机名 `aisoc-printer.local` 与 Web 端口（如 8080）；
   - TXT 记录包含 `version=2.0`、`model=twin` 核心元数据；
   - A 记录绑定设备 IPv4 地址（如 `192.168.1.100`）；
2. **C/C++ 编码规范与硬门禁 100% 达标**：
   - **零动态堆内存分配**：所有报文组装全部在定长 1460 字节静态缓冲区内完成，严禁 `malloc`/`new`；
   - **函数规模硬门禁**：所有自研函数均 $\le 34$ 行（远严于 $\le 50$ 行红线）；
   - **入参个数硬门禁**：所有函数入参 $\le 4$ 个；
   - **指针与内存安全**：公共入口首行全部设立 Guard Clause 防御性空指针校验，指针运算显式分步拆行，无魔数；
   - **双编译器严苛编译**：通过 `gcc -std=c11` 与 `g++ -std=c++17` (`-fno-exceptions -fno-rtti`) 全严苛标志 (`-Wall -Wextra -Werror -pedantic`) 编译，零警告零错误。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/browser_hmi/first_release/index.html` | 响应式 800x480 HMI 主界面结构与 OOBE 向导 DOM | `7b9548cb53f3b82f554296f736ed0a972f19de5e62103c14eeab1a1148357e39` |
| `soc-ap/browser_hmi/first_release/styles.css` | 深浅高对比度主题、44px 触控尺寸及 800x480 媒体查询 | `ee9f69c672b749335b7ecbc74b092e82d1c7df05fb70667ac8af548cdf3af2dc` |
| `soc-ap/browser_hmi/first_release/app.js` | 原生 JS 业务逻辑（料槽校验、OOBE向导、i18n、mDNS直连） | `0c737b1f069eedfbebe8ec6b683c5baa4543816a7fc22b3dec7fd2664217a20c` |
| `soc-ap/browser_hmi/first_release/slot_schema.json` | 4 通道供料料槽与 10000 混色权重 JSON 规范 Schema | `8089dfea214639782542ea36be2cdeb244704e771c637cad49aebde8ffa88417` |
| `soc-ap/browser_hmi/first_release/test_hmi_contract.py` | HMI DOM契约、10000权重、真实性、i18n及样式自动化测试 | `d23053e0ede2aad0f66531d97129f46fc441e0b1538c8851f6cb72ccb8e6718a` |
| `soc-ap/core/net/mdns/mdns_advertiser.h` | mDNS 广播器核心数据结构、状态码与 API 声明 | `e09c1d14aab0176817cda902fc256bcbba8c6d6942a86c7281868f444c4d659f` |
| `soc-ap/core/net/mdns/mdns_advertiser.c` | 纯 C 语言轻量级 mDNS 组播报文构造与广播实现 | `efafc5b0200556bbb2162718aa48825e2e83ebde7e12a8b13424cb4ce28d68f7` |
| `soc-ap/core/net/mdns/test_mdns_advertiser.c` | mDNS 报文构造、Wire格式、正反例单元测试集 | `d9f9888d5c9c7d85820101a8978d3089e7de6141b9484f85de9afeabe168b887` |

---

## 3. 正反用例与验证实测结果

### 3.1 mDNS Advertiser C11 与 C++17 单元测试输出
```
=== Starting TWIN-20 mDNS Advertiser Unit Tests (gcc -std=c11) ===
[PASS] test_initialization_positive
[PASS] test_initialization_negative (Guard Clause & boundary validation)
[PASS] test_packet_building_and_wire_format (DNS Header & PTR/SRV/TXT/A wire layout)
[PASS] test_socket_lifecycle (Socket open, multicast send, and graceful close)
=== ALL TWIN-20 mDNS ADVERTISER TESTS PASSED (4/4 Suites) ===

=== Starting TWIN-20 mDNS Advertiser Unit Tests (g++ -std=c++17 -fno-exceptions -fno-rtti) ===
[PASS] test_initialization_positive
[PASS] test_initialization_negative (Guard Clause & boundary validation)
[PASS] test_packet_building_and_wire_format (DNS Header & PTR/SRV/TXT/A wire layout)
[PASS] test_socket_lifecycle (Socket open, multicast send, and graceful close)
=== ALL TWIN-20 mDNS ADVERTISER TESTS PASSED (4/4 Suites) ===
```

### 3.2 HMI Contract 自动化测试输出
```
test_01_dom_elements_contract (__main__.TestHMIContract)
Verify presence of all mandatory DOM element IDs. ... ok
test_02_strict_realism_rule_positive_and_negative (__main__.TestHMIContract)
Verify strict realism rule: unlinked hardware MUST NOT show fake PASS/green status. ... ok
test_03_color_mixing_10000_weight_invariant (__main__.TestHMIContract)
Verify TWIN-17 10000 mixing weight logic and presets. ... ok
test_04_i18n_dictionary_parity (__main__.TestHMIContract)
Verify 100% key parity between zh-CN and en-US dictionaries. ... ok
test_05_styles_touch_targets_and_themes (__main__.TestHMIContract)
Verify touch targets >= 44px and dual themes in styles.css. ... ok
test_06_slot_schema_validation (__main__.TestHMIContract)
Verify slot_schema.json structure and constraints. ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.004s

OK
```

---

## 4. 门禁合规性审查表 (Hard Invariant Compliance Checklist)

| 门禁核查项 | 标准规范要求 | 实际交付达成情况 | 结论 |
| :--- | :--- | :--- | :--- |
| **自研函数行数** | 严禁编写超 50 行非结构体自研函数 | `mdns_advertiser.c` 最大函数为 34 行，平均 15 行 | **PASS** |
| **自研函数入参** | 严禁编写超 4 个入参自研函数 | 全部函数入参 $\le 4$ 个，多参统一封装结构体指针 | **PASS** |
| **零动态堆分配** | 严禁 `malloc`/`free`/`new`/`delete` | 零堆内存分配，全静态固定缓存 `packet_buffer[1460]` | **PASS** |
| **防御性校验** | 公开函数首行空指针校验 (Guard Clause) | `mdns_advertiser_init` 等公共 API 第一行非空防御 | **PASS** |
| **真实性门禁** | 严禁伪造通过状态（必须显示未检查/未知） | OOBE 向导未连接硬件项 100% 显式标注“未就绪/未连接” | **PASS** |
| **触控人体工学** | 800x480 触摸屏按键热区 $\ge 44\text{px}$ | `--touch-min-size: 44px`，全部交互按键满足约束 | **PASS** |
| **双编译器严选** | C11 与 C++17 无异常无 RTTI 零警告通过 | `-std=c11` 与 `-std=c++17` 带 `-Wall -Wextra -Werror -pedantic` 零报警 | **PASS** |
| **国际化与主题** | 中英双语动态免刷新、深浅高对比度主题 | 99 组词条全覆盖对齐，CSS 变量无刷新瞬时切换 | **PASS** |
