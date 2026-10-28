---
title: How-to：用 lark-cli 以用户身份读取飞书云文档
date: 2026-10-26
cli_version: 1.0.98
scope: Linux / WSL 下的用户登录、文档读取、文件列表与权限排查
---

# How-to：用 lark-cli 以用户身份读取飞书云文档

本机已安装 CLI 并完成用户登录，日常使用从第 1 节开始。新机器按第 5 节安装配置。所有业务命令显式使用 `--as user`。

本指南按本机 `lark-cli 1.0.98` 的帮助、schema 和实际读取结果编写。指定文档正文已读取成功；云空间文件列表仍待补充用户授权后重试。历史过程和权限差异见[接入经验](feishu_cli_user_access_experience_20261026.md)。

## 1. 日常起手：检查登录，读取文档

检查本机版本与用户凭证：

```bash
lark-cli --version
lark-cli auth status --json --verify
```

重点查看 `identities.user.verified` 是否为 `true`、`identities.user.tokenStatus` 是否为 `valid`，并确认 `identities.user.userName` 是准备使用的账号。尚未登录或凭证失效时，按第 4 节重新授权。

把下面变量替换成要读取的文档链接。这里给出的链接在本次接入中已实际读通：

```bash
FEISHU_DOC_URL='https://xcn2f5o5q8uz.feishu.cn/docx/S7tSdtqMkoiwBcxnfWIcrXScngc'
```

先查看目录：

```bash
lark-cli docs +fetch --as user --doc "$FEISHU_DOC_URL" \
  --scope outline --max-depth 3
```

读取整篇正文：

```bash
lark-cli docs +fetch --as user --doc "$FEISHU_DOC_URL" \
  --doc-format markdown
```

成功时，CLI 返回 `ok: true`、`identity: user`，正文位于 `data.document.content`，版本位于 `data.document.revision_id`。`--doc-format markdown` 控制正文格式，外层输出仍是 JSON。

## 2. 只读需要的内容，或保存到本地

按关键词读取：

```bash
lark-cli docs +fetch --as user --doc "$FEISHU_DOC_URL" \
  --scope keyword --keyword '传感器|RFID' --doc-format markdown
```

按章节读取：先从目录响应拿到对应标题的 `id`，替换下面占位符：

```bash
lark-cli docs +fetch --as user --doc "$FEISHU_DOC_URL" \
  --scope section --start-block-id '<目录中的标题 id>' \
  --doc-format markdown
```

保存完整 JSON 响应：

```bash
lark-cli docs +fetch --as user --doc "$FEISHU_DOC_URL" \
  --doc-format markdown > /tmp/feishu-document.json
```

先确认上一条命令退出码为 0，再提取正文保存为 Markdown：

```bash
python3 - <<'PY'
import json
from pathlib import Path

response = json.loads(Path('/tmp/feishu-document.json').read_text(encoding='utf-8'))
if response.get('ok') is not True:
    raise SystemExit('读取未成功，请查看 CLI 的错误输出。')
content = response['data']['document']['content']
target = Path('/tmp/feishu-document.md')
target.write_text(content, encoding='utf-8')
print(f'已保存：{target}')
PY
```

示例输出放在 `/tmp`；需要长期保存时换成自己的资料目录。正文中的图片、附件、嵌入 Sheet 和关联文档可能只返回引用，需要按资源类型另行读取；这份 Markdown 不等于包含所有附件的离线备份。

## 3. 查询云空间根目录或文件夹

文档正文和文件列表是不同权限。先检查本次清单查询所需的用户授权：

```bash
lark-cli auth check --scope space:document:retrieve --json
```

如果返回缺少权限，按第 4 节补充 `space:document:retrieve`，完成授权后再执行查询。

读取根目录直属文件与文件夹：

```bash
lark-cli drive files list --as user \
  --params '{"folder_token":"","page_size":200}' --format json
```

读取指定文件夹：把返回项中 `type: folder` 的 `token`，或文件夹链接 `/drive/folder/` 后的 token，填入下面占位符：

```bash
lark-cli drive files list --as user \
  --params '{"folder_token":"<文件夹 token>","page_size":200}' \
  --format json
```

结果在 `data.files` 中，每项通常包含 `name`、`type`、`token`、`url` 等字段。

普通文件夹若返回 `has_more: true`，把 `next_page_token` 原样填入下一次请求：

```bash
lark-cli drive files list --as user \
  --params '{"folder_token":"<同一文件夹 token>","page_size":200,"page_token":"<next_page_token>"}' \
  --format json
```

根目录按本版本 schema 不支持分页且不返回快捷方式；根目录清单只是第一层。需要子文件夹内容时继续使用各自的 token 查询，不能把第一层数量当作全云空间文件总数。

## 4. 登录与补充用户授权

### 自己在终端操作

只需读指定文档时，先申请文档只读权限：

```bash
lark-cli auth login --scope docx:document:readonly
```

需要补充文件列表权限时：

```bash
lark-cli auth login --scope space:document:retrieve
```

打开命令输出的授权链接，用目标飞书账号确认，保持终端命令运行，等待登录成功。然后重新执行第 1 节的联网状态检查，以及之前失败的业务命令。

在应用后台「权限管理 → 用户身份权限」中也必须启用所需 scope，并按后台提示使配置生效。后台已启用和用户 OAuth 已同意是两个步骤。若 CLI 提示其他缺失 scope，以该次实际错误为准补充对应用户权限。

始终显式指定所需 `--scope`；本机版本不带范围的登录或使用 `--recommend` 会请求更广范围。多次登录可能累积历史授权，申请只读 scope 不会自动撤销已有写权限。

### 让 Codex 帮你操作

执行方先发起不阻塞的授权流程：

```bash
lark-cli auth login --scope space:document:retrieve --no-wait --json
```

执行方把 `verification_url` 原样发给用户，并生成、展示二维码：

```bash
lark-cli auth qrcode '<verification_url>' --output feishu-user-auth.png
```

用户确认后回复“已授权”，执行方再续接同一轮返回的 `device_code`：

```bash
lark-cli auth login --device-code '<同一轮 device_code>'
lark-cli auth status --json --verify
```

链接有效期以本次 `expires_in` 为准，失效后重新发起。不要复用旧经验文档或旧对话中的临时授权链接；不要把另一轮的 device code 混进当前流程。

可以直接向 Codex 下达：

> 用 lark-cli 的用户身份读取这篇文档：<文档链接>。先列目录，再概括正文。

> 用 lark-cli 的用户身份读取我的云空间根目录文件列表；缺少权限时发起对应的用户授权。

## 5. 新机器首次安装与配置

前提是安装 Node.js / npm；本次环境使用 Node.js 20。Linux / WSL 可安装到自己的用户目录：

```bash
npm install --global --prefix "$HOME/.local" @larksuite/cli@latest
export PATH="$HOME/.local/bin:$PATH"
lark-cli --version
```

`export` 只影响当前终端；需要后续终端也可使用时，将同一行加入自己的 shell 配置。官方另一种安装方式是 `npx @larksuite/cli@latest install`。

使用已有应用时执行交互式配置，在提示中选择复用现有应用，并输入 App ID / App Secret：

```bash
lark-cli config init
```

自动化配置先查看 `lark-cli config init --help`，通过 `--app-secret-stdin` 从标准输入传递 Secret。本次本机保存路径是 `~/.lark-cli/config.json`；认证密钥位于用户数据目录。不要把凭据配置加入项目 Git 仓库。

配置完成后按第 4 节登录。CLI 使用 device flow，无需沿用手动 OAuth 的本机回调地址、复制 `code` 和自行兑换 Token 流程。

## 6. 常见问题速查

| 现象 | 处理方式 |
| --- | --- |
| `lark-cli: command not found` | 检查用户安装目录是否在 `PATH`；本机也可直接调用 `/home/sushaohua/.local/bin/lark-cli` |
| `missing_scope`，并提示 `space:document:retrieve` | 按第 4 节补充文件列表的用户授权，再重试 |
| 能读文档但不能列文件 | 分别补充 API 权限；指定文档读取不依赖先列根目录 |
| 已有 scope，但返回目标资源无权限 | 确认登录账号及文档本身对该用户的分享权限；核对链接和 token，按实际错误处理 |
| 用户凭证失效或授权链接过期 | 重新发起相应用户登录；每轮使用新的链接及对应 device code |
| 输出身份是 `bot` | 业务命令加 `--as user`，并确认已完成用户登录 |
| `read-only file system`，路径在用户配置或密钥目录 | 这是本机文件系统限制；在受管理环境申请相应目录写入权限，不要改成申请更多飞书权限 |
| 脚本解析 JSON 失败 | stdout 与 stderr 分开；不要将进度或错误输出合并进 JSON。确认 CLI 命令先执行成功 |
| 正文有 Sheet、图片或附件引用 | 通过相应资源命令继续读取，不能把引用当成已获得资源内容 |

查当前版本的参数与内置操作说明：

```bash
lark-cli docs +fetch --help
lark-cli drive files list --help
lark-cli schema drive.files.list
lark-cli skills read lark-shared
lark-cli skills read lark-doc/references/lark-doc-fetch.md
```

内置 Skills 随当前 CLI 构建，遇到在线文档和本机参数差异时，先核对本机帮助。新增操作只有实际执行成功后才能记录为通过；本 How-to 中尚未实测的示例不作为验收证据。

官方入口：[lark-cli 仓库](https://github.com/larksuite/cli)。本项目实测记录：[飞书接入经验](feishu_cli_user_access_experience_20261026.md)。
