#!/usr/bin/env bash
# @file push_to_server.sh
# @brief 多仓库同步推送与远端 HEAD 一致性校验脚本。
# @details 优先调用顶层工作区带令牌认证的五仓发布工具；降级模式下按固定分支顺序推送并核对远端 SHA。
set -euo pipefail

# 优先使用 project-control 仓内副本或导出到工作区根目录的副本定位工作区根路径
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ $# -gt 0 ]]; then
    workspace_root=$(cd -- "$1" && pwd)
elif [[ -f "$script_dir/project-control/manifest.yaml" ]]; then
    workspace_root=$script_dir
else
    workspace_root=$(cd -- "$script_dir/../.." && pwd)
fi

# 优先调用入口仓库的带 Token 认证多仓库发布器
if [[ -f "$workspace_root/workspace.json" && -f "$workspace_root/tools/workspace.py" ]]; then
    exec python3 "$workspace_root/tools/workspace.py" --workspace "$workspace_root" publish
fi

# 降级模式：遍历四个核心子仓库，检查当前分支与工作区洁净度后推送并核对远端引用
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes -o ConnectTimeout=10}"
failed=0
for entry in soc-ap:main project-control:main mcu-p3:feat/soc-debug test_harness:main; do
    repo=${entry%%:*}
    branch=${entry#*:}
    path="$workspace_root/$repo"
    if [[ $(git -C "$path" branch --show-current) != "$branch" ]]; then
        printf 'SKIP %s: expected checked-out branch %s\n' "$repo" "$branch" >&2
        failed=1
        continue
    fi
    if [[ -n $(git -C "$path" status --porcelain) ]]; then
        printf 'SKIP %s: commit or review local changes first\n' "$repo" >&2
        failed=1
        continue
    fi
    if git -C "$path" push origin "HEAD:refs/heads/$branch"; then
        if remote_line=$(git -C "$path" ls-remote --heads origin "refs/heads/$branch"); then
            read -r remote_sha remote_ref <<< "$remote_line"
            local_sha=$(git -C "$path" rev-parse HEAD)
            if [[ "$remote_sha" == "$local_sha" ]]; then
                printf 'VERIFIED %s %s %s\n' "$repo" "$branch" "$local_sha"
                continue
            fi
        fi
        printf 'UNVERIFIED %s: remote tip did not match local HEAD\n' "$repo" >&2
    else
        printf 'PENDING %s: push failed\n' "$repo" >&2
    fi
    failed=1
done
exit "$failed"
