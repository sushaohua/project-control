"""Freeze accepted task commands, repository locks and review inputs."""

import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

import yaml

from .errors import CoordRunnerError


def repository_from_card(card: dict) -> str:
    names = list((card.get("write_scope") or {}).keys())
    code_names = [name for name in names if name != "project-control"]
    if len(code_names) == 1:
        return code_names[0]
    if len(names) == 1:
        return names[0]
    explicit = card.get("candidate_repository")
    if explicit:
        return explicit
    raise CoordRunnerError("Task must identify one candidate repository; cannot infer it from task ID")


def freeze_commands(card: dict) -> list:
    commands = (card.get("verification") or {}).get("commands") or []
    result = []
    for item in commands:
        if not isinstance(item, dict) or not item.get("command") or not item.get("expected"):
            raise CoordRunnerError("QA requires explicit commands and accepted expectations")
        if item.get("availability") not in {"local", "available", "executable"}:
            raise CoordRunnerError("A required QA command is unavailable or still planned")
        kind = item.get("kind", "test")
        subpath = item.get("cwd", ".")
        if kind not in {"build", "test"} or not isinstance(subpath, str):
            raise CoordRunnerError("Invalid QA command kind/cwd")
        if Path(subpath).is_absolute() or ".." in Path(subpath).parts or ":" in subpath:
            raise CoordRunnerError("QA command cwd must be a sandbox-relative path")
        result.append({"kind": kind, "subpath": "" if subpath == "." else subpath,
                       "command": item["command"], "id": item.get("id")})
    if not result or not any(item["kind"] == "test" for item in result):
        raise CoordRunnerError("No accepted non-empty test plan; QA cannot invent commands")
    return result


def freeze_targets(card: dict, candidate: dict, config: dict) -> list:
    locks = dict(card.get("source_baseline") or {})
    locks[candidate["repository"]] = candidate["candidate_commit"]
    result = []
    for name, commit in locks.items():
        repo = (config.get("repositories") or {}).get(name) or {}
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit) or len(set(commit)) <= 1:
            raise CoordRunnerError(f"Invalid server commit for {name}")
        if not repo.get("url") or not repo.get("default_branch"):
            raise CoordRunnerError(f"Missing server URL/ref configuration for {name}")
        result.append({"name": name, "commit": commit, "url": repo["url"], "ref": repo["default_branch"]})
    return result


def create_qa_request(workspace: Path, card: dict, candidate: dict) -> dict:
    task_id = card.get("id", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", task_id):
        raise CoordRunnerError("Invalid task ID")
    if type(candidate["task_revision"]) is not int or candidate["task_revision"] != card.get("revision"):
        raise CoordRunnerError("Task revision changed or is invalid")
    workspace = workspace.resolve()
    config_path = workspace / "project-control/config/qa_runner/default_config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    request = dict(candidate, task_id=task_id, workspace=str(workspace))
    request["commands"] = freeze_commands(card)
    request["targets"] = freeze_targets(card, candidate, config)
    request["contract"] = json.loads(json.dumps(card))
    request["run_dir"] = tempfile.mkdtemp(prefix=f"qa_{task_id}_")
    request["timeout_seconds"] = 180 * len(request["targets"]) + 300 * len(request["commands"]) + 120
    command = [sys.executable, str(workspace / "project-control/tools/qa_runner/qa_runner.py"),
               "--config", str(config_path), "--task", task_id,
               "--revision", str(candidate["task_revision"]),
               "--output-dir", str(Path(request["run_dir"]) / "evidence")]
    for target in request["targets"]:
        command.extend(["--repo-commit", f"{target['name']}={target['commit']}:{target['ref']}"])
    for item in request["commands"]:
        command.extend(["--cmd", f"{item['kind']}:{item['subpath']}:{item['command']}"])
    request["sandbox_command"] = command
    manifest = Path(request["run_dir"]) / "request.json"
    manifest.write_text(json.dumps(request, indent=2, ensure_ascii=False), encoding="utf-8")
    request["request_ref"] = {"path": str(manifest), "sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}
    return request
