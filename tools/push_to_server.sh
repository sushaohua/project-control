#!/usr/bin/env bash
set -euo pipefail

# Use the project-control copy or an exported copy in the workspace root.
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
if [[ $# -gt 0 ]]; then
    workspace_root=$(cd -- "$1" && pwd)
elif [[ -f "$script_dir/project-control/manifest.yaml" ]]; then
    workspace_root=$script_dir
else
    workspace_root=$(cd -- "$script_dir/../.." && pwd)
fi

# Prefer the entry repository's token-authenticated, five-repository publisher.
if [[ -f "$workspace_root/workspace.json" && -f "$workspace_root/tools/workspace.py" ]]; then
    exec python3 "$workspace_root/tools/workspace.py" --workspace "$workspace_root" publish
fi

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
