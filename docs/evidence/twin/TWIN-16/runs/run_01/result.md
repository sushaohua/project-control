# TWIN-16 TH 温度契约复核与必要修订交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-16` (TH 温度契约复核与必要修订) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **执行角色** | `ENG-TH` (从控/工具头固件工程师) |
| **当前轮次** | `run_01` (契约复核、0.1℃ 分辨率对账、强电安全锁死与独立沙箱闭环) |
| **前置依赖** | `TWIN-02` (`532caecf3a146802969a49e73081400c2b32b25e`), `TWIN-03` (`0b7497ba43158841eb3c4af7f16e477b9c30c2c5`), `TEMP-02` (`1.0.0`) |
| **候选 Commit** | `mcu-p3: d756a13b3c2a1c47186a07311b2c24fa43431465` (`feat/soc-debug`), `project-control: 565429b7fa9953f9b824fbb2d8b34944aef1c9f9` |
| **作者会话 ID** | `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5` |
| **执行状态** | **Completed (TH 0x14 温度响应实现、0.1℃ 分辨率对账、强电安全硬性锁死 100% 验证通过)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据 `ICD-VMWARE-SOC-TWIN-20261029`、`telemetry_types.h` 及系统契约 C1～C6 决议，`ENG-TH` 对从控工具头固件进行了精确复核与必要修订：
1. **温度分辨率与量程对账 (C2 & C3)**：
   - 彻底将原有草案的 `0.01℃` (`centi_c`) 修正为法定契约的 **`0.1℃` (`deci_c`)** 分辨率，结构体字段命名为 `current_temp_deci_c` 与 `target_temp_deci_c`；
   - NTC 查表 `s_ntc_table` 全部数值映射为 `0.1℃`（如 210℃ 编码为 `2100`，25℃ 编码为 `250`），消除 `int16_t` 溢出风险；
   - 哨兵对齐：`0x7FFF` (`MINIMC_TEMP_SENTINEL_FAULT`) 表示开路/短路故障，`0x7FFE` (`MINIMC_TEMP_SENTINEL_OFFLINE`) 表示超时离线；
2. **协议 Flags 与命令码规范 (C1 & C4)**：
   - 响应帧 Flags 严格置为 `0x06` (`MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2`)；
   - 命令码严格分配为 `0x14` (`MINIMC_CMD_TEMP_REPORT`)，源节点标识置为 `MINIMC_NODE_TH` (`0x03`)；
3. **强电安全硬性锁死 (C5)**：
   - `thermistor_safety_lock()` 强制锁死 `target_temperature[0] = 0`、`soft_pwm[0] = 0`、`TMR3` 通道占空比置 0，遥测报文 `heater_duty_percent = 0U`，本增量硬性禁止任何加热输出；
4. **单调时间戳与本地硬件保护**：
   - `sample_timestamp_ms` 接入本地单调时钟 `get_tick_count()`，开路（ADC > 4075）与短路（ADC < 20）阈值实施就地拦截并标记。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `mcu-p3/color-engine-mcu/io_toggle/inc/minimc_proto.h` | 协议头文件，节点标识定义 | `69dfd606b668881abc9e85e233d39d1d9d9d4bd824ac9d1d836cd50edec71e04` |
| `mcu-p3/color-engine-mcu/io_toggle/inc/minimc_telemetry.h` | 16字节紧凑遥测 Payload 与哨兵定义 | `add9c7a729a028c52b82b983546c95afe9a3f709ffcb96cc029ab5caf2af93c3` |
| `mcu-p3/color-engine-mcu/io_toggle/inc/thermistor_adc.h` | ADC 采集与安全锁接口声明 | `263074c78c8cef12cdaaf5198a167458562976606da3a96953367b170ced4e8d` |
| `mcu-p3/color-engine-mcu/io_toggle/src/app/thermistor_adc.c` | ADC 采样、超时防护、查表插值与强电安全锁实现 | `ff385cdec3ccb642949d77dd2f6ad769364f250df177f81d2e679699e10cfe3c` |
| `mcu-p3/color-engine-mcu/io_toggle/src/app/minimc_proto.c` | 0x14 响应帧构造与协议分发实现 | `4a289bb0b63fb13faa1dcb62696427faa3b4648b43f9fb017adfc747b5c78b67` |
| `mcu-p3/color-engine-mcu/io_toggle/build/fw_th.bin` | AT32F423 TH 目标板固件构建产物 (71,804 字节) | `df02647e585e2081d5ebd87680c0ecf1dab795768018c01b063a797425fe1e25` |

---

## 3. 编码硬门禁符合性声明 (Coding Standards Compliance)

1. **函数规模硬性门禁**：所有自研新增与修改函数（`adc_hw_init` 27行、`adc_calibrate_with_timeout` 23行、`thermistor_safety_lock` 7行、`thermistor_adcConfig` 6行、`adc_read_single_raw` 20行、`adc_single_conversion_get` 19行、`sample_adc_average` 21行、`ntc_adc_to_deci_c` 26行、`thermistor_adc_get_telemetry` 44行、`build_temp_resp` 49行）**严格控制在 $\le 50$ 行以内**，经自动化脚本扫描 100% 通过；
2. **函数入参限制**：所有函数入参个数均 $\le 4$ 个；
3. **指针与内存安全**：零动态堆内存分配（无 malloc/free），指针解引用与取地址独立成行，无压缩指针运算，无多重指针；
4. **防御性校验**：所有公开函数入口首行均执行 Guard Clause 防御性空指针检查；
5. **硬件轮询安全**：所有 ADC 转换与校准等待均包含带 `ADC_POLL_TIMEOUT_CYCLES` 的超时计数器退出机制，严禁死循环。

---

## 4. 验证与独立沙箱证据 (Verification & Sandbox Evidence)

- **宿主机固件构建**：`cd mcu-p3/color-engine-mcu/io_toggle && make pack` 成功生成带 128B Trailer 及 140B Sector 127 锚点的固件 `build/fw_th.bin`；
- **独立 Docker 容器沙箱 QA 验证**：
  - 沙箱 ID: `TWIN-16_run_175010_20261030_095010` (Container: `63269389ae22`)
  - 镜像 Digest: `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`
  - 验证命令 1 (`minimc_telemetry.h` 语法与 Static Assert 检查): PASS (Exit 0)
  - 验证命令 2 (`check_layout.c` 二进制布局、偏移、哨兵与转换测试): PASS (Exit 0)
  - 验证命令 3 (`check_task_graph.py` 静态任务图检查): PASS (Exit 0)
  - 产物记录：`project-control/docs/evidence/twin/TWIN-16/runs/run_01/server_qa/` (`server_qa.json` sha256: `bffbaf7fc5ec1f95d9a7afe4c3f29b8a9eec8c8ce998ea77657c4372c5162023`)。
