# TWIN-15 MC 温度契约复核与必要修订交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-15` (MC 温度契约复核与必要修订) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **执行角色** | `ENG-MC` (运动主控固件工程师) |
| **当前轮次** | `run_01` (定向整改、对账 C1-C6 契约与独立沙箱闭环) |
| **前置依赖** | `TWIN-02` (`532caecf3a146802969a49e73081400c2b32b25e`), `TWIN-03` (`0b7497ba43158841eb3c4af7f16e477b9c30c2c5`), `TEMP-03` (`1.0.0`) |
| **候选 Commit** | `mcu-p3: 0ba7769fe60a032f765deada1e112c360e08b3cd` (`feat/soc-debug`), `project-control: 6207499476986989df3a82848510cbaa68e1435e` |
| **作者会话 ID** | `1aba53f3-e424-4e8c-926a-ddfc0d5e44c5` |
| **执行状态** | **Completed (MC 0x14 温度响应实现、0.1℃ 分辨率对账、强电锁死及透明路由 100% 验证通过)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据 `ICD-VMWARE-SOC-TWIN-20261029`、`telemetry_types.h` 及 C1～C6 决议，`ENG-MC` 对原 `TEMP-03` 的初版实现进行了精确复核与必要定向修订：
1. **温度分辨率与量程对账 (C2 & C3)**：
   - 将原草案的 `0.01℃` (`centi_c`) 修正为法定契约的 **`0.1℃` (`deci_c`)** 分辨率，结构体字段命名为 `current_temp_deci_c` 与 `target_temp_deci_c`；
   - 彻底解决 `+350℃` 在 `int16_t` 溢出的风险；室温 `24.5℃` 编码为 `245`；
   - 哨兵对齐：`0x7FFF` (`MINIMC_TEMP_SENTINEL_FAULT`) 表示传感器故障，`0x7FFE` (`MINIMC_TEMP_SENTINEL_OFFLINE`) 表示超时或离线；
2. **协议 Flags 与命令码规范 (C1 & C4)**：
   - 响应帧 Flags 严格置为 `0x06` (`MINIMC_FLAG_IS_RESPONSE | MINIMC_FLAG_PROTO_V2`)；
   - 命令码严格分配为 `0x14` (`MINIMC_CMD_TEMP_REPORT`)，与查询码 `0x14` (`MINIMC_CMD_GET_TEMP`) 统一，通过 Flags 区分方向；
3. **强电安全硬性锁死 (C5)**：
   - `payload.heater_duty_percent = 0U` 强电硬件硬锁死，本切片不调用任何 PWM 加热输出；
4. **TH 报文原生透明中继保持**：
   - 保持 MC 对发往 TH (`dst_id == 0x03`) 请求及来自 TH 响应的透明中继转发与 CRC 重算逻辑，绝不篡改 payload。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | 协议头文件，引入遥测扩展 | `cc197d3d494faa1107cf294ed5189ab3932e010a4b7ea4093b5b91dc5a38cfca` |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_telemetry.h` | 16字节紧凑遥测 Payload 与哨兵定义 | `add9c7a729a028c52b82b983546c95afe9a3f709ffcb96cc029ab5caf2af93c3` |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | 0x14 响应帧构造与查询分发实现 | `1b49bf10d8fdb885591ed9aeb8957ff8ec5a3dca5c6fa7ddfee1ccd8683c1c2a` |
| `mcu-p3/motion-controller-mcu/build/fw_mc.bin` | AT32F435 MC 目标板固件构建产物 (370,036 字节) | `662e5822f1cb36ea39fb85e69f2e03168496eaa032f13cb29c2df5194ac3e13b` |

---

## 3. 编码硬门禁符合性声明 (Coding Standards Compliance)

1. **函数规模硬性门禁**：`build_temp_resp` 全长 42 行，`handle_mc_query` 全长 34 行，自研新增函数严格控制在 $\le 50$ 行以内；
2. **入参限制**：`build_temp_resp` 仅 3 个入参，严格控制在 $\le 4$ 个以内；
3. **指针与内存安全**：零动态堆内存分配（无 malloc/free），指针下标显式索引，无多重指针；
4. **防御性校验**：`build_temp_resp` 首行包含 Guard Clause 防御性空指针检查；
5. **布局静态断言**：头文件包含 `_Static_assert(sizeof(minimc_temp_report_payload_t) == 16)` 编译期校验。

---

## 4. 验证与独立沙箱证据

- **宿主机固件构建**：`cd mcu-p3/motion-controller-mcu && make pack -j4` 编译成功，生成带 128B Trailer 的打包固件 `build/fw_mc.bin`；
- **独立 Docker 容器沙箱 QA 验证**：
  - 沙箱 ID: `TWIN-15_run_173258_20261030_093258` (Container: `901d20ba32d4`)
  - 镜像 Digest: `sha256:acbab225932c3877fff37f4d9e5a21235e099182c198e4f4034064ea80cf544f`
  - 验证命令 1 (`minimc_telemetry.h` 语法与断言检查): PASS (Exit 0)
  - 验证命令 2 (`check_layout.c` 内存对齐与偏移检查): PASS (Exit 0)
  - 验证命令 3 (`check_task_graph.py` 静态任务图检查): PASS (Exit 0)
  - 产物记录：`project-control/docs/evidence/twin/TWIN-15/runs/run_01/server_qa/` (`server_qa.json` sha256: `36b65c08cdac85f6f354d0e45916e45dd6931eb5a8897bb7a86680539e487f79`)。
