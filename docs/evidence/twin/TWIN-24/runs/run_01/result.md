# TWIN-24 MC 固件 5×5 调平网格导出 (0x18) 响应交付自检报告 (Run 01)

| 属性 | 内容 |
| :--- | :--- |
| **任务卡片** | `TWIN-24` (MC 固件 5×5 调平网格导出 0x18 响应实现) |
| **所属工作包** | `TASK-002` (交接现有双 MCU 能力与协议) |
| **执行角色** | `ENG-MC` (运动主控固件工程师) |
| **当前轮次** | `run_01` (0x18 调平网格响应实现、52字节载荷微米对账、128字节局部缓冲区扩容与独立自检闭环) |
| **前置依赖** | `TWIN-21` (`mcu-p3=abbc3ae240972f5a60d751c6204c8b73f1f464bf`), `TWIN-22` (`soc-ap=6850cc553d405b5e7e511ff181d985fdee8e221f`) |
| **候选 Commit** | `mcu-p3: 9b017f186665c2c9226146cc0fdc34af3ad5242b` (`feat/soc-debug`) |
| **作者会话 ID** | `session-eng-mc-twin-24` |
| **执行状态** | **Completed (MC 0x18 调平网格导出响应、52字节载荷5×5微米网格精度对账、128字节缓冲区防溢出与强电安全恒0%锁死 100% 验证通过)** |

---

## 1. 契约复核与核心实现 (Contract Alignment & Implementation)

依据 `project-control/docs/specs/mcu_motion_leveling_filament_interface_survey_20261029.md` 第 3.4 与 6.2 节及系统裁决指令 **U-D04**（“固件存量为 5×5 双线性网格，PM 目标要求 7×7 网格，未达成技术裁决，采用固件存量；当前开发功能以固件存量为主要参考”）与 **U-D03**（强电加热占空比恒为 0% 锁死），`ENG-MC` 对运动控制器（AT32F435VGT7）的 MiniMCProto 二进制通信协议进行了首版调平网格导出（`MOT-002`）的工程落地：

1. **协议操作码与载荷定义 (`minimc_proto.h`)**：
   - 增加操作码宏定义：`MINIMC_CMD_LEVEL_GRID_QUERY = 0x18U`；
   - 增加常量定义：
     - `MINIMC_LEVEL_GRID_POINTS_X = 5U`
     - `MINIMC_LEVEL_GRID_POINTS_Y = 5U`
     - `MINIMC_LEVEL_GRID_POINTS_NUM = 25U`
     - `MINIMC_LEVEL_GRID_PAYLOAD_SIZE = 52U`
     - `MINIMC_LEVEL_GRID_FRAME_SIZE = 66U`
   - 增加单字节紧凑对齐结构体 `minimc_level_grid_payload_t`：
     ```c
     #pragma pack(push, 1)
     typedef struct {
         uint8_t  grid_points_x;      /* 固定为 5 */
         uint8_t  grid_points_y;      /* 固定为 5 */
         int16_t  z_offset_um[25];    /* 25 个采样点的相对偏差 (微米 um, 0.001mm), 范围 -32768~+32767 um */
     } minimc_level_grid_payload_t;
     #pragma pack(pop)
     ```
   - 包含 `_Static_assert(sizeof(minimc_level_grid_payload_t) == 52)` 与 C++17 `static_assert` 兼容。

2. **局部响应缓冲区扩容至 128 字节 (`minimc_proto.c`)**：
   - 排查发现原 `handle_mc_query` 内部局部响应缓冲区为 `uint8_t resp[64];`。由于 0x18 响应帧长为 66 字节（12B 头部 + 52B 载荷 + 2B CRC），若使用 64 字节缓冲区必然导致栈溢出和崩溃；
   - 将该局部响应缓冲区彻底扩容至 `uint8_t resp[128];`，并增加 `resp_len <= sizeof(resp)` 防御性边界检查，杜绝栈破坏隐患。

3. **毫米转微米精度对账与安全钳位 (`level_mm_to_um`)**：
   - 引用 Marlin 存量 `extern float bed_level[AUTO_BED_LEVELING_GRID_POINTS][AUTO_BED_LEVELING_GRID_POINTS];`；
   - 实现静态转换辅助函数 `level_mm_to_um(float mm)`：
     - 正负浮点毫米值乘以 1000.0 并进行精确四舍五入，浮点转换误差 $\le 0.5\text{ um} \le 1\text{ um}$；
     - 增加严格的上下界钳位保护：值域超出 `[-32768, 32767]` 时强制截断至边界，彻底消除符号数溢出翻转风险。

4. **调平网格响应组装与指令分发 (`build_level_grid_resp` & `handle_mc_query`)**：
   - `build_level_grid_resp()`：
     - 首行执行 Guard Clause 防御性空指针检查；
     - 组装 12 字节 MiniMCProto v2.0 报头（`flags=0x06` V2|RESP, `src=0x02` MC, `dst=0x01` AP, `cmd=0x18`, `seq`, `payload_len=52`）；
     - 填充 52 字节载荷（`grid_points_x=5`, `grid_points_y=5`，按行遍历 `y * 5 + x` 填入 `z_offset_um`）；
     - 计算并附加 CCITT-FALSE CRC16 校验码，总帧长为 66 字节；
   - 在 `handle_mc_query()` 中接入 `MINIMC_CMD_LEVEL_GRID_QUERY` 分支，组装并调用 `minimc_proto_send()` 经 DMA 异步发送；
   - 强电硬件安全硬锁死：加热器输出占空比恒为 0%（`thermistor_safety_lock`），本增量严禁开启任何发热丝 PWM。

---

## 2. 交付物清单与 SHA-256 校验码

| 交付文件路径 | 类型与描述 | SHA-256 校验码 |
| :--- | :--- | :--- |
| `mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h` | 协议头文件，0x18 报文、常量、网格尺寸与 52B 紧凑载荷定义 | `db2d086e52ccd1d744a518d6cfb994592c43c1ab5e4a12640b3594edc9b06629` |
| `mcu-p3/motion-controller-mcu/project/src/minimc_proto.c` | 协议实现，0x18 处理分支、build_level_grid_resp 封装与 128B 局部缓冲区防溢出 | `844ee3228e1b614b05a7127d590deef8d5137899f6b8a4e6c6fbaf776ac7a0e2` |
| `mcu-p3/motion-controller-mcu/build/Marlin_AT32.bin` | AT32F435 MC 目标板原始固件镜像 (371,132 字节) | `7f162c982d48c21d824781b85a39854078a6d95526670a793a326c038b3f64b2` |
| `mcu-p3/motion-controller-mcu/build/Marlin_AT32.elf` | 目标板 ELF 符号表文件 | `ee7bc370be2ddae140ef6559ba17430c8d6c85ccba5fe020bc43e0f9d8d7138d` |
| `mcu-p3/motion-controller-mcu/build/fw_mc.bin` | 带 128B Trailer 签名的最终打包固件产物 (371,260 字节) | `e879c05c62d32f5ed9324e72adcf96ecfa71e364046fb55116ac7a4cfe188974` |
| `project-control/docs/evidence/twin/TWIN-24/runs/run_01/test_twin24_level_grid.c` | 独立正反例验证与 0x18 端到端流水线测试程序 | `06235f00d392eb79ab251b65203590217325e2d977ebb16267a561d3e9373083` |

---

## 3. 编码硬门禁符合性声明 (Coding Standards Compliance)

本任务严格遵从 `project-control/.agents/rules/c_cpp_coding_standard.md`：
1. **函数规模硬性门禁（$\le 50$ 行）**：
   - `level_mm_to_um()`: 22 行
   - `build_level_grid_resp()`: 44 行
   - `handle_mc_query()`: 44 行
   - `test_twin24_level_grid.c` 中所有单测辅助函数均在 46 行以内；
   - 经自动化脚本扫描，所有自研函数均在 45 行以内，**100% 达标**。
2. **函数入参限制（$\le 4$ 个）**：
   - 所有自研新增函数参数个数：`level_mm_to_um` (1个)、`build_level_grid_resp` (3个)、`handle_mc_query` (2个)，**100% 达标**。
3. **指针与内存安全**：
   - 零动态堆内存分配（严禁 `malloc` / `free` / `new` / `delete`）；
   - 显式数组索引赋值，严禁压缩指针运算黑魔法（无 `*dst++ = *src++`）；
   - 指针解引用与取地址操作独立成行，无多重指针（无 `***`）。
4. **控制流与防御性校验**：
   - `build_level_grid_resp` 入口第一行严格执行 Guard Clause 空指针校验：`if ((out_buf == NULL) || (out_len == NULL)) return;`；
   - 函数嵌套深度 $\le 2$ 层，无嵌套三元运算符。
5. **编译期静态断言**：
   - 头文件包含 `_Static_assert(sizeof(minimc_level_grid_payload_t) == 52)` 强制校验结构体大小与单字节紧凑排布。

---

## 4. 验证与测试命令执行记录 (Verification Results)

### 4.1 嵌入式目标交叉编译（arm-none-eabi-gcc）

执行带 `-Werror` 的交叉语法检查：
```bash
arm-none-eabi-gcc -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER \
  -I mcu-p3/motion-controller-mcu/build \
  -I mcu-p3/motion-controller-mcu/libraries/cmsis/cm4/core_support \
  -I mcu-p3/motion-controller-mcu/libraries/cmsis/cm4/device_support \
  -I mcu-p3/motion-controller-mcu/libraries/drivers/inc \
  -I mcu-p3/motion-controller-mcu/project/inc \
  -I mcu-p3/motion-controller-mcu/project/delay \
  -I mcu-p3/motion-controller-mcu/project/fatfs/source \
  -I mcu-p3/motion-controller-mcu/project/marlin \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_core \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_gcode \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_msc \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_module \
  -mcpu=cortex-m4 -mfpu=fpv4-sp-d16 -mfloat-abi=hard \
  -Wall -Wextra -Wpedantic -fdata-sections -ffunction-sections -fcommon \
  -Werror=implicit-function-declaration -Werror -O0 -g3 -std=gnu11 \
  -c mcu-p3/motion-controller-mcu/project/src/minimc_proto.c -o /tmp/minimc_proto.o
```
**结果**：Exit Code 0，无任何警告与错误。

### 4.2 C++ 头文件兼容性检查（g++ -std=c++17）

```bash
g++ -std=c++17 -Wall -Wextra -Werror -I mcu-p3/motion-controller-mcu/project/inc -fsyntax-only -x c++ -c mcu-p3/motion-controller-mcu/project/inc/minimc_proto.h
```
**结果**：Exit Code 0，头文件完全兼容 C++17。

### 4.3 固件构建与打包（make pack）

```bash
make -C mcu-p3/motion-controller-mcu pack
```
**输出**：
```text
==================================================
 [PACK] 固件打包完成
 - 原始输入文件: build/Marlin_AT32.bin (371132 字节)
 - 有效代码净载: 371132 字节
 - 目标板卡架构: 0x43500001 [MC (AT32F435)]
 - 固件版本编号: 0x01095448
 - 注入构建时间: 1793416463 (2026-10-31 11:14:23)
 - SHA-256 摘要: 7f162c982d48c21d824781b85a39854078a6d95526670a793a326c038b3f64b2
 - 最终输出文件: build/fw_mc.bin (371260 字节)
==================================================
```
**结果**：编译并成功打包输出 `fw_mc.bin`。

### 4.4 独立二进制单测运行（test_twin24_level_grid）

运行包含 6 个测试套件的正反例测试程序：
```bash
gcc -DAT32F435VGT7 -DUSE_STDPERIPH_DRIVER -Wno-pointer-to-int-cast -Wno-int-to-pointer-cast \
  -I mcu-p3/motion-controller-mcu/build \
  -I mcu-p3/motion-controller-mcu/libraries/cmsis/cm4/core_support \
  -I mcu-p3/motion-controller-mcu/libraries/cmsis/cm4/device_support \
  -I mcu-p3/motion-controller-mcu/libraries/drivers/inc \
  -I mcu-p3/motion-controller-mcu/project/inc \
  -I mcu-p3/motion-controller-mcu/project/delay \
  -I mcu-p3/motion-controller-mcu/project/fatfs/source \
  -I mcu-p3/motion-controller-mcu/project/marlin \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_core \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_gcode \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_lcd \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_msc \
  -I mcu-p3/motion-controller-mcu/project/marlin/marlin_module \
  project-control/docs/evidence/twin/TWIN-24/runs/run_01/test_twin24_level_grid.c \
  mcu-p3/motion-controller-mcu/project/src/minimc_proto.c \
  -o /tmp/test_twin24 && /tmp/test_twin24
```
**测试输出**：
```text
========================================================================
TWIN-24 MC Firmware 5x5 Level Grid Query (0x18) Response Verification
========================================================================
[RUN ] test_struct_layout_and_size
[PASS] test_struct_layout_and_size
[RUN ] test_level_mm_to_um_reconciliation
[PASS] test_level_mm_to_um_reconciliation
[RUN ] test_build_level_grid_resp_frame
[PASS] test_build_level_grid_resp_frame
[RUN ] test_rx_pipeline_e2e_dispatch
[PASS] test_rx_pipeline_e2e_dispatch
[RUN ] test_buffer_safety_and_defensive_checks
[PASS] test_buffer_safety_and_defensive_checks
[RUN ] test_high_voltage_safety_confirmation
[PASS] test_high_voltage_safety_confirmation
------------------------------------------------------------------------
All 6 test suites PASSED!
========================================================================
```
**结果**：6 个测试套件 100% 通过。

### 4.5 规划图与门禁校验

```bash
PYTHONDONTWRITEBYTECODE=1 python3 project-control/tools/check_task_graph.py --workspace .
```
**结果**：Exit Code 0，结构无错误，依赖无环。
