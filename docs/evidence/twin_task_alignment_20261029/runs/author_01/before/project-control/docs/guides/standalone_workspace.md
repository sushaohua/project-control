# 独立工作区使用说明

## 项目边界

`ai_soc_project/` 是工作区，`project-control/`、`soc-ap/`、`mcu-p3/`、`test_harness/` 为四个独立 Git 仓。当前规则、决定、协议和任务在本地控制仓；代码、构建依赖和测试在各自仓库。`D:\AI_RDdocs\` 仅是知识库，不作为项目根目录、配置目录、构建输入、脚本入口或运行时文件源。

需要参考知识库的新资料时，先将所需文件复制到项目内，记录来源、版本、SHA256 和用途；正常接续使用本地副本。知识库后续修改不会自动改变本项目。旧文档中的迁移命令和 Obsidian 回链属于历史资料，不能作为正常启动步骤或要求 AI 回外部读取的必要输入。

当前通信依据为 [本地 MiniMCProto v2.0 / Rev 2.0.3](../specs/README.md)，用户选择见 [采用记录](../specs/protocol_selection_20261020.md)。本项目保留原稿字节，适用说明单独维护。

## 从工作区直接构建、运行 AP

在安装 CMake ≥3.16、C++17 编译器、Ninja 的 Linux/WSL/VMware Ubuntu 上，从工作区根目录执行：

```bash
cmake -S soc-ap -B soc-ap/build/host -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build soc-ap/build/host
(cd soc-ap/build/host && ctest --output-on-failure)
./soc-ap/build/host/bin/soc-ap --check-config
./soc-ap/build/host/bin/soc-ap --serial-port /dev/ttyUSB0
```

最后一条运行当前 AP 主程序，Ctrl-C 或 SIGTERM 正常退出。当前程序仅报告配置/启动状态，没有打开串口或实现 v2.0 收发，因此能独立启动不代表 AP→MC→TH 通信已经完成。运行细节见 [soc-ap README](../../../soc-ap/README.md)。

MC/TH 是目标板固件，不能作为 Linux 程序直接执行；源码和标准外设库均在 `mcu-p3/`。其 ARM 工具链、开发构建候选命令、现有制品和未验证项见 [工程登记](../baseline/ms01_source_inventory_20261020.md)。真正运行仍需构建和部署到板，知识库无需挂载。Windows 串口/烧录工具及板卡、VMware 访问属于环境资源，分别验证，不能用知识库的存在代替。

## 本次独立性检查

本次检查四仓 Git 管理的非文档文件，未找到对 `AI_RDdocs` 或 `/mnt/d/` 的直接引用；另检查工作区项目文件中的符号链接，未发现指向知识库的链接。旧资料中的来源地址、迁移脚本示例及保留的协议回链不作为构建/运行步骤。

将 `soc-ap` 的 11 个 Git 管理文件复制到新的 `/tmp/soc_ap_standalone_20261020_*` 目录，没有复制知识库、既有 build 或 Git 元数据；在仅含 Linux PATH 和 LANG 的环境中重新配置、构建、运行现有 CTest 及配置检查，均退出 0，`host_runtime_smoke` 1/1 通过。该用例包含真实启动和 SIGTERM 正常退出。证据见 [迁移构建日志](../evidence/20261020_protocol_import/ap_relocated_build.log)及[检查清单](../evidence/20261020_protocol_import/workspace_independence.json)。

这是 AP 现有启动骨架的迁移验证，未卸载/改动 D 盘，也没有重建 MCU、连 VMware 或验证硬件通信。后续新增协议实现仍应在同样不依赖知识库的目录结构内构建和验收。
