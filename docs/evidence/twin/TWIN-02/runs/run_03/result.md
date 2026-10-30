# TWIN-02 双环境可执行通信契约与生成规则执行与验收报告 (Run 03 退修整改)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-02` (双环境可执行通信契约与生成规则) |
| **所属工作包** | `TASK-013` (冻结 DDS D-Bus MQTT 通信契约) |
| **执行角色** | `ARCH` (系统架构师) |
| **当前轮次** | `run_03` (针对 run_02 独立 QA 审查意见落实退修) |
| **前序报告** | [`runs/run_02/qa_review_report.md`](../run_02/qa_review_report.md) (REJECTED) |
| **当前候选 Commit** | `soc-ap: 532caec85c4900a0caae4da68367f0f6706e5792` |
| **执行状态** | **Completed / Delivered (退修闭环完成，所有 10 个系统服务强制约束，哈希与服务器候选提交 100% 精确对齐)** |

---

## 1. 逐项整改与差异溯源表 (Finding Resolution Matrix)

| Finding ID | 缺陷根因 | 修复位置与差异 | 新增与修改测试 | 复现命令与实际结果 | 候选 Commit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`TWIN02-QA-01`** (Blocker) | `services_manifest_schema.json` 允许仅提供 4 个活跃服务而省略其余 6 个 deferred 服务（`minItems: 4`）；未强制完整拓扑必须包含全部 10 个服务 | `soc-ap/contracts/twin/services_manifest_schema.json`：<br/>1. `services` 数组改为 `minItems: 10, maxItems: 10, uniqueItems: true`；<br/>2. `allOf` 扩展为 10 项 `contains` 强校验，强制必须同时包含 4 个活跃服务 (`forward-service`, `device-manager`, `ui-gateway`, `browser-hmi`) 与 6 个 deferred 服务 (`job-engine`, `storage-service`, `cloud-gateway`, `camera-service`, `print-guard`, `system-manager`) | 运行 `Draft7Validator` 进行正反例全矩阵验证：<br/>1. 完整 10 服务 (PASS)<br/>2. 仅 4 活跃服务 (REJECT)<br/>3. 缺 1 个 deferred 服务 (REJECT)<br/>4. deferred 服务标 active (REJECT)<br/>5. active 服务标 deferred (REJECT) | Draft7Validator 全矩阵校验 100% 预期通过 | `532caec85c4900a0caae4da68367f0f6706e5792` |
| **`TWIN02-QA-06`** (Blocker-Evidence) | run_02 `result.md` 引用未推送到服务器的本地临时 Commit 哈希 (`f086230...`) 且记录的产物 SHA256 与真实文件不一致，破坏了证据与提交的一致性绑定 | `project-control/docs/evidence/twin/TWIN-02/runs/run_03/result.md`：<br/>将候选 Commit 严格锁定为已推送到 GitLab 远端 `origin/main` 的真实 Commit `532caec85c4900a0caae4da68367f0f6706e5792`，并对所有契约文件执行 `sha256sum` 实测核对，确保表格数据与实际文件 100% 严格一致 | 独立执行 `sha256sum` 并与 `git show <commit>:<path> | sha256sum` 严格比对 | 6 份交付物哈希值实测与远端提交完全一致 | `532caec85c4900a0caae4da68367f0f6706e5792` |

---

## 2. 交付物哈希核对清单

| 交付文件路径 | 类型与描述 | SHA256 校验码 | 对应 soc-ap Commit |
| :--- | :--- | :--- | :--- |
| `soc-ap/contracts/twin/telemetry.idl` | Fast DDS IDL 规范 | `50987edd6419d7c4ac61a18b87f1f7f18638b9595db0c042dae0071d2a81b516` | `532caec85c4900a0caae4da68367f0f6706e5792` |
| `soc-ap/contracts/twin/dbus_interfaces.xml` | D-Bus 接口规范 | `cf1389ffd6d4f580865af6033abdaaf66e3d2d9072dda0ca00785e6bc7ac54ed` | `532caec85c4900a0caae4da68367f0f6706e5792` |
| `soc-ap/contracts/twin/http_sse_schema.json` | Web REST 与 SSE Schema (含数值边界与哨兵) | `603699711f9f558550683cce9507146dabf1b2958a8b7168ad9730f187177406` | `532caec85c4900a0caae4da68367f0f6706e5792` |
| `soc-ap/contracts/twin/telemetry_types.h` | C/C++ 通信头文件 (宏定义消除魔数) | `e485b1183e3bd7cf9c512a7643f70bac8998b364e21cebaf4ae8ab4429601e61` | `532caec85c4900a0caae4da68367f0f6706e5792` |
| `soc-ap/contracts/twin/services_manifest_schema.json` | 服务拓扑 Schema (强制锁定 10 服务及状态) | `e7265d37fa6b518d9c7655ba6118963302fa690b959172c7736e8aeab7b23d34` | `532caec85c4900a0caae4da68367f0f6706e5792` |
| `soc-ap/contracts/twin/README.md` | 契约与生成规范文档 | `09f869547f7e9b1b04b781177d261421cf956b927c2eb3ef3cf4b52ab73f650e` | `532caec85c4900a0caae4da68367f0f6706e5792` |
