# TWIN-20 HMI料槽映射、新机检查引导、国际化与局域网发现交付自检报告 (Run 02)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-20` (HMI料槽映射、新机检查引导、国际化与局域网发现) |
| **所属工作包** | `TASK-009` (实现真实通信交互界面与双环境显示) |
| **执行角色** | `ENG-UI` (协力 `ENG-NET`, `ENG-STATE`) |
| **当前轮次** | `run_02` (接入真实双 MCU 固件版本展示、时序衰退状态机联动与零伪造对账) |
| **前置依赖** | `TWIN-02` (Done), `TWIN-29` (Done) |
| **执行状态** | **Completed (真实双 MCU 固件版本呈现、五态防御映射、Sensors 与 OOBE 双端联动、自动化契约测试 7/7 全通)** |

---

## 1. 核心架构与功能实现 (Architecture & Implementation)

依据用户高优先级指令（显示 MC 和 TH 当前真实固件版本，离线/失败/过期时明确提示，可用于升级前后核对版本），`ENG-UI` 在 `run_02` 中重点完成了以下增量功能交付：

### 1.1 主界面 Sensors 标签页真实固件版本展示 (`index.html`, `app.js`)
1. **MC 与 TH 独立卡片呈现**：
   - 在 `#card-th`（工具头卡片）属性列表中新增 `#th-firmware-version` 元素项；
   - 在 `#card-mc`（运动主控热床卡片）属性列表中新增 `#mc-firmware-version` 元素项；
2. **实时数据流解析 (`applyTelemetrySnapshot`)**：
   - 从后端 `/api/v1/temperature/snapshot` 及 SSE `/api/v1/temperature/stream` 中消费由 `TWIN-29` `device_manager` 导出的 `data.devices.mc` 与 `data.devices.th`；
   - 提取 `firmware_version` 与 `git_commit`，以 `v{major}.{minor} ({git_commit})`（如 `v1.0 (0x04231388)`）权威展示真实固件版本；
3. **时序衰退与五态防御状态机映射 (`updateDeviceVersion`)**：
   - **ONLINE (在线)**：展示完整版本号与提交哈希（如 `v1.0 (0x04231388)`），状态徽章绿色“已连接 (在线)”；
   - **STALE (数据已过期)**：展示版本号并附带 `[数据已过期]` 醒目标签，状态徽章黄色“数据已过期”；
   - **OFFLINE (设备离线)**：明确显示“设备离线”，状态徽章红色“设备离线”；
   - **QUERY_FAILED (查询失败)**：明确显示“查询失败”，状态徽章红色“查询失败”；
   - **UNKNOWN (未知/未就绪)**：默认未连接状态显示“未知”，状态徽章黄色“未就绪/未连接/等待接入”；
4. **恪守绝对真实性与零伪造原则**：
   - 严禁任何硬编码、假数据或客户端模拟生成；
   - 设备未连通或未读取成功时绝不显示虚假版本号。

### 1.2 OOBE 开箱向导 Step 3 真实通信与固件自检联动
1. **MC / TH 版本与状态实时绑定**：
   - `#oobe-mc-version` 与 `#oobe-th-version` 实时同步后端真实设备版本；
   - `#oobe-mc-status` 与 `#oobe-th-status` 依据设备当前时序状态（ONLINE/STALE/OFFLINE/QUERY_FAILED/UNKNOWN）动态切换徽章文案与样式（`badge-success`, `badge-warning`, `badge-danger`）；
2. **多语言免刷新即时响应**：
   - 在 `I18N` 字典中新增 `lbl_firmware_ver`, `ver_status_unknown`, `ver_status_offline`, `ver_status_query_failed`, `ver_status_stale` 词条，保持 `zh-CN` 与 `en-US` 100% 对齐；
   - 用户切换语言时，固件版本状态文本与徽章文案毫秒级免刷新同步翻译。

---

## 2. 验证与测试结果 (Verification Results)

### 2.1 本地测试套件全集执行
1. **HMI 自动化契约测试 (`test_hmi_contract.py`)**：
   ```bash
   python3 soc-ap/browser_hmi/first_release/test_hmi_contract.py
   ```
   **测试结果**：7/7 用例全部 PASS（含新增 `test_07_real_dual_mcu_firmware_version_presentation`）。
2. **mDNS Advertiser 纯 C 与 C++17 双标准构建自检**：
   ```bash
   gcc -Wall -Wextra -Werror -pedantic -std=c11 -I soc-ap/core/net/mdns soc-ap/core/net/mdns/mdns_advertiser.c soc-ap/core/net/mdns/test_mdns_advertiser.c -o /tmp/test_mdns && /tmp/test_mdns
   g++ -Wall -Wextra -Werror -pedantic -std=c++17 -fno-exceptions -fno-rtti -I soc-ap/core/net/mdns soc-ap/core/net/mdns/mdns_advertiser.c soc-ap/core/net/mdns/test_mdns_advertiser.c -o /tmp/test_mdns_cxx && /tmp/test_mdns_cxx
   ```
   **测试结果**：C11 与 C++17 各 4/4 项测试全集通过（零编译警告、零堆内存分配）。
3. **静态任务拓扑与门禁检查**：
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
   python3 project-control/tools/delivery_checks.py
   ```
   **检查结果**：exit 0，零结构错误，零门禁阻塞。

---

## 3. 交付物清单与哈希锁定

- `soc-ap/browser_hmi/first_release/index.html`
- `soc-ap/browser_hmi/first_release/app.js`
- `soc-ap/browser_hmi/first_release/test_hmi_contract.py`
- `soc-ap/core/net/mdns/mdns_advertiser.h`
- `soc-ap/core/net/mdns/mdns_advertiser.c`
- `soc-ap/core/net/mdns/test_mdns_advertiser.c`
- `soc-ap/browser_hmi/first_release/slot_schema.json`
- `soc-ap/browser_hmi/first_release/styles.css`
