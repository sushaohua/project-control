# 工作区恢复与服务器同步

工作区根目录不是 Git 仓库。代码及管理资料分别保存在四个仓库；根目录入口文件的导出快照保存在本仓 `workspace-root/`，避免只推子仓导致入口丢失。根目录 `.agents/` 是旧副本，正式状态读取本仓 `.agents/`。

## 从服务器恢复

在空工作区中执行以下命令（已有目录时先核对，避免重复检出）：

```bash
git clone --branch main ssh://git@192.168.77.113:2222/sushaohua/project-control.git project-control
git clone --branch main ssh://git@192.168.77.113:2222/sushaohua/soc-ap.git soc-ap
git clone --branch feat/soc-debug ssh://git@192.168.77.113:2222/sushaohua/mcu-p3.git mcu-p3
git clone --branch main ssh://git@192.168.77.113:2222/sushaohua/test_harness.git test_harness
cp -n project-control/workspace-root/README.md.snapshot README.md
cp -n project-control/workspace-root/AGENTS.md.snapshot AGENTS.md
```

`cp -n` 保留已存在的根目录文件。随后读取本仓最新交接 `docs/handoff/HANDOFF_20261020.md`；需要根目录导航及历史交接副本时：

```bash
cp -n project-control/docs/handoff/HANDOFF_20261019.md HANDOFF_20261019.md
cp -n project-control/workspace-root/HANDOFF_20261020.md.snapshot HANDOFF_20261020.md
```

快照仅用于恢复或导出，不作为第二份持续编辑的根目录原件。根目录文件更新后，发布时刷新快照。

恢复后依次读取本地[协议目录](../specs/README.md)和[独立工作区运行说明](standalone_workspace.md)。无需克隆或挂载知识库；历史迁移文档中的知识库命令不是恢复/启动步骤。

## 推送与验证

在允许连接服务器的终端，从工作区执行：

```bash
bash project-control/tools/push_to_server.sh
```

脚本检查分支及工作区状态，普通推送四个指定分支，再用 `ls-remote` 核对服务器 SHA；不强制覆盖远端历史。服务器拒绝非快进推送时，先核对远端新增提交及冲突，再继续。输出 `VERIFIED` 才算完成对应仓库的远端核对。

根目录 `artifacts/server_sync_20261019/` 保留昨日 Git bundle、版本清单与校验和；不包含 2026-10-20 后续本地检查点中的新增资料。bundle 含当批分支所需历史，可搬到可联网环境后检出；不能将旧包当作今天全部工作或已同步服务器。本次推送失败证据见 `docs/evidence/20261020/push_attempt.log`。工作区有修改时脚本会跳过对应仓库，应先审阅并提交准确候选，再推送。
