# TWIN-02 双环境可执行通信契约与生成规则执行与验收报告 (Run 02 退修整改)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-02` (双环境可执行通信契约与生成规则) |
| **所属工作包** | `TASK-013` (冻结 DDS D-Bus MQTT 通信契约) |
| **执行角色** | `ARCH` (系统架构师) |
| **当前轮次** | `run_02` (针对 run_01 独立 QA 审查意见落实退修) |
| **前序报告** | [`runs/run_01/qa_review_report.md`](../run_01/qa_review_report.md) (REJECTED) |
| **当前候选 Commit** | `soc-ap: f086230df3952d876f9917fdaad8ea6cb4b49f9a` |
| **执行状态** | **Completed / Delivered (退修闭环完成，静态断言与契约 Schema 全量通过)** |

---

## 1. 逐项整改与差异溯源表 (Finding Resolution Matrix)

| Finding ID | 缺陷根因 | 修复位置与差异 | 新增与修改测试 | 复现命令与实际结果 | 候选 Commit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`TWIN02-QA-01`** (Blocker) | `services_manifest_schema.json` 缺少对首切片 4 个服务同时存在且必须为 `first_slice_active` 的强约束，未严格限制其余 6 个服务必须为 `deferred` | `soc-ap/contracts/twin/services_manifest_schema.json`：<br/>1. `services` 数组增加 `contains` 强校验，强制必须包含 `forward-service`, `device-manager`, `ui-gateway`, `browser-hmi` 4 个服务；<br/>2. `ServiceDescriptor` 增加 `allOf`/`if-then`，严格锁定前 4 者为 `first_slice_active`，其余 6 者为 `deferred` | 运行 `jsonschema.Draft7Validator.check_schema` 校验合法性，并验证非首切片标 active 时的拒收负例 | `python3 -m json.tool` exit 0；Draft7 校验通过 | `f086230` |
| **`TWIN02-QA-02`** (Blocker) | `http_sse_schema.json` 中 `temperature_millic` 仅标为 integer，未对物理有效范围及高位哨兵做约束 | `soc-ap/contracts/twin/http_sse_schema.json`：<br/>`temperature_millic` 增加 `oneOf` 约束：<br/>- 分支 1：物理测量范围 `minimum: -40000, maximum: 500000` (对应 -40.000°C ~ +500.000°C)；<br/>- 分支 2：`enum: [2147483647, 2147483646]` (对应故障哨兵 0x7FFFFFFF 与离线哨兵 0x7FFFFFFE) | 验证合法温度与哨兵数值通过，越界数值与非法哨兵被拦截 | `python3 -m json.tool` exit 0；Draft7 校验通过 | `f086230` |
| **`TWIN02-QA-03`** (Major) | `telemetry_types.h` 中 CRC 计算使用未命名的裸数值常量 (`0xFFFFU`, `0x1021U`, `0x8000U`, `8`)，触犯编码规范魔数禁令 | `soc-ap/contracts/twin/telemetry_types.h`：<br/>显式定义 `MINIMC_CRC16_CCITT_INIT (0xFFFFU)`、`MINIMC_CRC16_CCITT_POLYNOMIAL (0x1021U)`、`MINIMC_CRC16_CCITT_MSB_MASK (0x8000U)`、`MINIMC_BITS_PER_BYTE (8U)`，彻底消除计算过程中的魔数 | 执行 `g++ -std=c++17 -Wall -Wextra -Werror` 与 `gcc -std=c11` 编译语法检查 | exit code 0，零警告零报错 | `f086230` |

---

## 2. 交付物哈希核对清单

| 交付文件路径 | 类型与描述 | SHA256 校验码 |
| :--- | :--- | :--- |
| `soc-ap/contracts/twin/telemetry.idl` | Fast DDS IDL 规范 | `50987edd6419d7c4ac61a18b87f1f7f18638b9595db0c042dae0071d2a81b516` |
| `soc-ap/contracts/twin/dbus_interfaces.xml` | D-Bus 接口规范 | `cf1389ffd6d4f580865af6033abdaaf66e3d2d9072dda0ca00785e6bc7ac54ed` |
| `soc-ap/contracts/twin/http_sse_schema.json` | Web REST 与 SSE Schema (已加数值边界与哨兵约束) | `6114eb38e05d0458df81c81044e1c5f617ce71bb769f37c356ef2eb24ee94589` |
| `soc-ap/contracts/twin/telemetry_types.h` | C/C++ 通信头文件 (已清除 CRC 魔数) | `c379df44b419b67da67db445100742f9b14bfe3201460d3d5f573d84a7e8e503` |
| `soc-ap/contracts/twin/services_manifest_schema.json` | 服务拓扑 Schema (已锁定 4 真实进程与 6 deferred) | `86ca1c9a63bfa4b4657dcbb2887373f1d82ea124508aa43e4981df2f6fa72379` |
| `soc-ap/contracts/twin/README.md` | 契约与生成规范文档 | `09f869547f7e9b1b04b781177d261421cf956b927c2eb3ef3cf4b52ab73f650e` |
