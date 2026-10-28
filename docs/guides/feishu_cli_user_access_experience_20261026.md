---
title: 飞书 CLI 用户身份接入与文档权限排查经验
date: 2026-10-26
status: 指定文档正文读取成功；云空间文件列表待补充用户授权
scope: 本次飞书接入会话的操作经验与实测边界
---

# 飞书 CLI 用户身份接入与文档权限排查经验

日常操作请直接使用 [How-to：用 lark-cli 以用户身份读取飞书云文档](feishu_cli_howto.md)；本文保留接入过程、实测结果和适用边界。

## 1. 结论与适用范围

访问个人飞书云文档时，优先使用官方 `lark-cli` 完成用户登录，并在业务命令中显式指定 `--as user`。用户明确要求以本人身份操作时，使用 `user_access_token`，不能用机器人的 `tenant_access_token` 测试结果代替用户访问结论。

截至本次记录，CLI 已安装、用户登录已完成，指定文档的目录和正文均已实际读取成功。云空间根目录清单查询因缺少用户授权被拦截；已发起补充授权，但尚未完成其登录续接与清单重试，不能宣称文件列表读取成功。

本文是操作经验记录，不是独立 QA 签署，不提升项目任务或硬件验收状态。记录依据为本次会话实际命令输出；后续 CLI 版本、有效权限和文档修订应重新查询。

## 2. 认证成功、用户登录与资源访问应分别判断

| 检查层次 | 本次实际结果 | 可以得出的结论 |
| --- | --- | --- |
| App ID / App Secret 换取应用凭证 | HTTP 200，飞书返回 `code: 0` | 应用凭据有效，认证接口可达 |
| 机器人信息查询 | HTTP 200，机器人名称为「飞书bot」 | 机器人信息接口可调用 |
| 应用身份获取云空间、知识库列表 | 飞书返回 `99991672`，提示缺少应用身份权限 | 这些应用身份接口未获所需权限；不能据此判断用户权限 |
| CLI 用户登录 | 登录成功；联网检查 `identity: user`、`verified: true`、用户凭证 `tokenStatus: valid` | 当时用户登录有效 |
| 用户文档只读 scope 检查 | `docx:document:readonly` 在 `granted` 中 | 用户凭证具备此项 API 权限 |
| 用户身份读取指定 Docx | 目录和正文均返回 `ok: true`、`identity: user` | 该用户当时可以读取该文档 |
| 用户身份获取云空间根目录清单 | CLI 退出码 3，`missing_scope: space:document:retrieve` | 清单查询尚未成功，需要补充相应用户授权 |

每次判断同时核对身份、接口所需 scope 和目标资源的访问结果。能读取一篇文档，不代表能枚举整个云空间；能列目录，也不代表每个文件的正文、附件和嵌入资源都可读取。

## 3. 优先使用官方 CLI 处理 OAuth

官方仓库为 [larksuite/cli](https://github.com/larksuite/cli)。本次通过 GitHub 仓库信息观察到最近推送为 2026-10-23，仓库未归档；这是记录时的状态，不构成持续维护保证。

本次环境为 Linux / WSL、Node.js `v20.20.2`，实际安装的 CLI 版本为 `1.0.98`。

本次安装命令：

```bash
npm install --global --prefix /home/sushaohua/.local @larksuite/cli@latest
lark-cli --version
```

可执行文件位于 `/home/sushaohua/.local/bin/lark-cli`，该目录已在本机 `PATH` 中。官方也提供 `npx @larksuite/cli@latest install` 安装向导；本次实际采用的是上面的 npm 用户目录安装。

已经有应用时复用现有 App ID 和 Secret。通过 `lark-cli config init --help` 确认参数；本次使用了 `--app-id`、`--app-secret-stdin`、`--brand feishu` 和 `--lang zh`，密钥由进程标准输入传入。配置保存到用户目录的 `~/.lark-cli/config.json`。

App Secret、用户访问凭证、刷新凭证和本地认证密钥不写入本经验文档或 Git 仓库。不要把含这些内容的配置文件或完整认证调试输出作为项目证据提交。

## 4. 用户授权采用两步完成

先发起文档只读授权：

```bash
lark-cli auth login --scope docx:document:readonly --no-wait --json
```

命令立即返回 `verification_url`、`device_code` 和 `expires_in`。将原样的授权 URL 展示给用户，并按 CLI 官方指南生成二维码：

```bash
lark-cli auth qrcode '<verification_url>' --output feishu-user-auth.png
```

用户在浏览器或飞书客户端确认后，由执行方续接同一轮授权：

```bash
lark-cli auth login --device-code '<同一轮返回的 device_code>'
lark-cli auth status --json --verify
lark-cli auth check --scope docx:document:readonly --json
```

授权链接应先送达用户，再等待确认并续接；不要在用户尚未看到链接时就阻塞轮询。每个授权流程只使用自己返回的 `device_code`；链接失效后重新发起，并保持原来需要的 scope。临时授权链接、二维码和授权码不保存为长期操作入口。

本次 `expires_in` 为 600 秒。登录成功后，联网验证返回用户「苏韶华Allen」、`identity: user`、`verified: true`，且用户凭证有效。

本次只显式请求了文档只读 scope，但实际用户凭证的 `scope` 中还包含其他已生效权限。不能把“本次只请求某一项权限”写成“整个用户凭证只有这一项权限”；后续以 `auth status` 的实际结果为准。本次业务访问只执行了只读命令。

后台的「用户身份权限」和用户 OAuth 同意授权共同决定可用 API 范围。用户身份授权仍依附于应用注册信息，但资源调用身份是用户；缺少用户 scope 时，应补充用户身份授权，不能切换成 bot 规避。

## 5. 已成功读取的指定文档

目标：[X2D拆机报告——硬件部分](https://xcn2f5o5q8uz.feishu.cn/docx/S7tSdtqMkoiwBcxnfWIcrXScngc)。

首次读取未知结构时，先查目录：

```bash
lark-cli docs +fetch --as user \
  --doc 'https://xcn2f5o5q8uz.feishu.cn/docx/S7tSdtqMkoiwBcxnfWIcrXScngc' \
  --scope outline --max-depth 3
```

再获取正文：

```bash
lark-cli docs +fetch --as user \
  --doc 'https://xcn2f5o5q8uz.feishu.cn/docx/S7tSdtqMkoiwBcxnfWIcrXScngc' \
  --doc-format markdown
```

两次命令均实际返回成功，正文响应的主要字段为：

```json
{
  "ok": true,
  "identity": "user",
  "document_id": "S7tSdtqMkoiwBcxnfWIcrXScngc",
  "revision_id": 1938
}
```

返回的 `content` 字符串长度为 3025，包含拆机 BOM、传感器位置、系统框图和检查点。此长度包括 Markdown / XML 引用标记，不是文档字数统计。

完整 CLI 响应临时保存在本机 `/tmp/feishu_S7tSdtqMkoiwBcxnfWIcrXScngc_read.json`，便于继续处理；`/tmp` 文件不是仓库内的长期证据，也不保证一直保留。

正文中出现了 Excel 文件引用、嵌入 Sheet、图片链接和另一篇文档引用。本次未进一步下载或读取这些资源；正文返回引用不等于已经拿到它们的数据。要分析 BOM 表、传感器表或图片，需要按资源类型继续调用相应读取命令并核对权限。

## 6. 文件列表查询与补充用户权限

调用前先查看当前安装版本的帮助和 schema：

```bash
lark-cli drive files list --help
lark-cli schema drive.files.list
```

本次实际执行的根目录查询为：

```bash
lark-cli drive files list --as user \
  --params '{"folder_token":"","page_size":200}' \
  --format json
```

CLI 在用户权限检查阶段返回：

```json
{
  "ok": false,
  "identity": "user",
  "error": {
    "type": "authorization",
    "subtype": "missing_scope",
    "missing_scopes": ["space:document:retrieve"]
  }
}
```

按实际错误发起对应的用户权限授权：

```bash
lark-cli auth login --scope space:document:retrieve --no-wait --json
```

当前进度停留在此轮授权链接已生成并交给用户。接续时先确认是否已授权及流程是否仍有效，完成相应 device flow 后再重试文件列表。文档正文读取成功不会自动完成这一步。

根目录清单只包含直接子项，不是全云空间递归总量。按本次 schema，根目录不支持分页且不返回快捷方式；读取子文件夹时使用其自己的 `folder_token`，按 `has_more` / `next_page_token` 手动续页。需要递归时再逐层读取子文件夹，不能把第一层数量当作全部文件数量。

## 7. 命令输出和本机权限的常见误判

- **区分 CLI 输出与原始 API 输出。** CLI 成功信封使用 `ok: true` 和退出码 0；不要要求它有原始飞书 API 的顶层 `code: 0`。
- **核对实际身份。** 本次 CLI 配置仍是 `defaultAs: auto`，因此每条文档和列表命令均显式使用 `--as user`，并核对响应 `identity`。
- **先查当前版本帮助。** 远端指南与本机 CLI 可能有差异。本次远端参考称文件夹参数应放入 `--params`，而本机帮助也提供 typed flags；本次采用两者都支持的 `--params` 写法。
- **stdout 和 stderr 分开。** 只解析 stdout 的 JSON；stderr 可能包含进度、凭证刷新或本机警告，不能合并后直接 `json.loads`。
- **文件系统错误不是飞书 scope 错误。** 本次沙箱阻止写入用户目录，出现过本地 DPoP 密钥临时文件只读错误。经工作区外写入授权后重新联网验证成功；不应因此关闭 DPoP、修改默认认证保护或扩大飞书权限。
- **CLI 调用按需请求本机权限。** 安装、保存配置、写入认证密钥发生在用户目录，受管理环境需要相应文件系统批准；这与飞书账号在授权页同意的资源权限是两类操作。

## 8. 后续接续与完成判据

1. 已有明确文档链接时，直接用 `docs +fetch --as user` 验证目标，避免把目录权限当成正文读取的前置条件。
2. 用户仍需文件列表时，完成 `space:document:retrieve` 的有效用户授权，再重试根目录查询。
3. 只有列表命令实际返回成功并取得 `data.files`，才能报告该范围清单读取完成；空清单也必须结合响应范围解释。
4. 新建飞书文档、编辑文档、上传附件等操作不在本次读取验证结果之内，需按用户后续请求执行，不能推定已经成功。

## 9. 官方参考

- [lark-cli 官方仓库与安装说明](https://github.com/larksuite/cli)
- [lark-shared：身份、认证与权限](https://github.com/larksuite/cli/blob/main/skills/lark-shared/SKILL.md)
- [用户授权流程参考](https://github.com/larksuite/cli/blob/main/skills/lark-shared/references/lark-shared-identity-and-permissions.md)
- [指定文档读取参考](https://github.com/larksuite/cli/blob/main/skills/lark-doc/references/lark-doc-fetch.md)
- [Drive 文件列表参考](https://github.com/larksuite/cli/blob/main/skills/lark-drive/references/lark-drive-files-list.md)
- [飞书 OAuth 授权码文档](https://open.feishu.cn/document/authentication-management/access-token/obtain-oauth-code)

远端链接随上游更新；遇到差异时以当前安装版本的 `--help` / `schema`、实际接口响应和飞书官方说明共同判断，不凭旧经验猜测参数或权限。
