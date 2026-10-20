# 协议接收与独立运行检查证据

本批记录 2026-10-20 用户指定协议副本及项目脱离知识库使用的检查，由当前 AI (Codex) 主对话执行，不是独立 QA/HIL 验收。

| 文件 | 实际内容 |
| --- | --- |
| [workspace_independence.json](workspace_independence.json) | 源文件/项目协议副本字节一致性、SHA256、四仓非文档文件的知识库直接引用检查、实际符号链接目标检查。只读扫描 Git 管理文件，未执行旧文档迁移示例；文档中的出处及知识库历史链接可保留。 |
| [ap_relocated_build.log](ap_relocated_build.log) | 将 AP 的 11 个 Git 管理文件复制到全新临时目录，在最小环境中实际配置、构建、CTest、配置检查的 stdout/stderr、命令、cwd 和退出码。 |
| [ap_relocated_build.json](ap_relocated_build.json) | 对应运行环境、源码 HEAD、输出目录、各命令结果及二进制 SHA256。 |
| [SHA256SUMS](SHA256SUMS) | 本目录其他证据文件哈希；可在本目录执行 `sha256sum -c SHA256SUMS`。 |

未复制知识库、Git 元数据或历史 build 到临时源码目录，未修改/卸载知识库，未重新构建或部署 MCU，也未进行远程/串口操作。检查不宣称已禁止进程访问所有外部文件；它验证静态依赖和 AP 现有骨架的迁移构建、启动及退出。项目内协议是独立版本副本，不自动跟随知识库变化。
