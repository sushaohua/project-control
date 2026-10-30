# TWIN-18 双MCU运动/调平/断料状态接口调查与协议对账执行与验收报告 (Run 02 退修整改)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-18` (双MCU运动/调平/断料状态接口调查与协议对账) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **执行角色** | `ENG-MC` (协同 `ENG-TH` 与 `ARCH`) |
| **当前轮次** | `run_02` (针对 run_01 独立 QA 审查意见落实退修) |
| **前序报告** | [`runs/run_01/qa_review_report.md`](../run_01/qa_review_report.md) (REJECTED) |
| **当前规范原件** | `project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md` |
| **执行状态** | **Completed / Delivered (退修闭环完成，协议矩阵与报文定义 100% 对齐)** |

---

## 1. 逐项整改与差异溯源表 (Finding Resolution Matrix)

| Finding ID | 缺陷根因 | 修复位置与差异 | 新增与修改测试 | 复现命令与实际结果 |
| :--- | :--- | :--- | :--- | :--- |
| **`TWIN18-QA-01`** (Blocker) | §5 对账总矩阵与 §6 详细报文定义存在多处不一致：<br/>1. `MOT-001` 出现了歧义的“0x40 或 0x16”；<br/>2. `MOT-002` 载荷在表格中写 52 字节，在 §6.2 结构体中写 54 字节；<br/>3. `COL-007` 末尾字段在表格写 `param=0`，在 §6.3 写 `timestamp_tick_ms` | `project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md`：<br/>1. 彻底锁定 `MOT-001` 为 **`CMD_POS_QUERY = 0x16`**，载荷 20 字节；<br/>2. 彻底对齐 `MOT-002` 为 **`CMD_LEVEL_GRID_QUERY = 0x18`**，载荷严格锁定为 **52 字节** (`uint8_t grid_points_x`, `uint8_t grid_points_y`, `int16_t z_offset_um[25]`)，去除结构体中未被使用的冗余字段，使静态断言 `sizeof == 52`，帧长锁定为 66 字节；<br/>3. 彻底对齐 `COL-007` 字段定义为 `uint8_t alarm_level`, `uint8_t subsystem_id`, `uint16_t error_code`, `uint32_t timestamp_tick_ms` (共 8 字节) | 审查对账矩阵与结构体定义，对齐所有字段宽度与含义 | 文本与静态结构体 100% 对齐 |

---

## 2. 交付物 SHA256 校验码

| 交付文件路径 | 类型与描述 | SHA256 校验码 |
| :--- | :--- | :--- |
| [`project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md`](../../../../specs/mcu_motion_leveling_filament_interface_survey_20261029.md) | 双MCU运动/调平/断料调查与协议对账规范 (rev 2) | `596b4e84252fd71332865663a31187d40e5826ab345712bec34d40eca1f2f4ea` |
