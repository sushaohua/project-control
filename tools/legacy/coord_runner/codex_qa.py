"""确定性沙箱测试执行及其客观证据链（容器隔离、仓库锁、命令结果）的严格校验模块。"""

import hashlib
import json
from pathlib import Path
import subprocess

from .errors import CoordRunnerError
from .qa_contract import create_qa_request


def read_qa_ref(ref: dict, run_dir: Path) -> tuple:
    """在当前独立 QA 运行目录边界内读取证据文件并核验其 64 位 SHA256 摘要。"""
    if not isinstance(ref, dict) or not isinstance(ref.get("path"), str) or not ref["path"]:
        raise CoordRunnerError("QA evidence needs a non-empty path")
    expected = ref.get("sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        raise CoordRunnerError("QA evidence needs an exact SHA256")
    path = Path(ref["path"])
    path = (path if path.is_absolute() else run_dir / path).resolve()
    if run_dir.resolve() not in path.parents:
        raise CoordRunnerError("QA evidence must belong to this independent run")
    data = path.read_bytes()
    if not data or hashlib.sha256(data).hexdigest() != expected:
        raise CoordRunnerError(f"QA evidence SHA256 mismatch: {path}")
    return path, data


def validate_checks(proof: dict, request: dict) -> None:
    """将沙箱实际执行的构建/测试命令及其客观退出码与冻结计划及 server_verdict 进行双向绑定校验。"""
    run_dir = Path(request["run_dir"])
    _, raw = read_qa_ref(proof.get("server_verdict"), run_dir)
    verdict = json.loads(raw)
    if any(verdict.get(key) != request[key] for key in ("task_id", "task_revision")):
        raise CoordRunnerError("Server verdict task/revision mismatch")
    actual = proof.get("build_results", []) + proof.get("test_results", [])
    expected = request["commands"]
    if not proof.get("test_results") or len(actual) != len(expected):
        raise CoordRunnerError("Missing executed checks from the frozen plan")
    observed = sorted((item["command"], item["subpath"]) for item in actual)
    planned = sorted((item["command"], item["subpath"]) for item in expected)
    if observed != planned:
        raise CoordRunnerError("Executed commands do not match the frozen plan")
    passed = all(str(item.get("exit_code")) == "0" for item in actual)
    if type(proof.get("passed")) is not bool or proof["passed"] != passed:
        raise CoordRunnerError("Sandbox outcome disagrees with command exit codes")
    if verdict.get("verdict") != ("PASSED" if passed else "FAILED"):
        raise CoordRunnerError("Server verdict disagrees with objective evidence")
    if verdict.get("exit_code") != (0 if passed else 1):
        raise CoordRunnerError("Server verdict exit code mismatch")
    if type(verdict.get("test_count")) is not int or verdict["test_count"] != len(proof["test_results"]):
        raise CoordRunnerError("Server test count mismatch")


def validate_source(proof: dict, request: dict) -> None:
    """核验 server_lock.json 中记录的所有仓库 URL、分支引用与 Commit 哈希均与冻结请求完全一致。"""
    _, raw = read_qa_ref(proof.get("server_lock"), Path(request["run_dir"]))
    repositories = json.loads(raw).get("repositories", [])
    if len(repositories) != len(request["targets"]):
        raise CoordRunnerError("Server repository lock coverage mismatch")
    for target in request["targets"]:
        matching = [repo for repo in repositories if repo.get("name") == target["name"]]
        if len(matching) != 1 or any(matching[0].get(key) != target[key]
                                     for key in ("url", "ref", "commit")):
            raise CoordRunnerError("Server lock does not bind the exact requested target")


def validate_server_proof(ref: dict, request: dict) -> dict:
    """在任何独立模型启动审阅前，先确定性校验 server_qa 证明的容器隔离性、零宿主工作区挂载与日志完整性。"""
    path, data = read_qa_ref(ref, Path(request["run_dir"]))
    proof = json.loads(data)
    if type(proof.get("task_revision")) is not int:
        raise CoordRunnerError("Server proof revision must be an integer")
    if any(proof.get(key) != request[key] for key in ("task_id", "task_revision")):
        raise CoordRunnerError("Server proof task/revision mismatch")
    if proof.get("fresh_checkout") is not True or proof.get("source") != "server-pinned-commits":
        raise CoordRunnerError("QA requires a fresh server-pinned checkout")
    sandbox = proof.get("sandbox") or {}
    inspect = sandbox.get("container_inspect") or {}
    if sandbox.get("kind") != "container" or not sandbox.get("container_id"):
        raise CoordRunnerError("QA requires the actual Docker sandbox")
    if sandbox.get("developer_mounts") != [] or not inspect.get("image_digest") or not inspect.get("id"):
        raise CoordRunnerError("Isolation evidence is missing or unsafe")
    if not inspect["id"].startswith(sandbox["container_id"]):
        raise CoordRunnerError("Container identity mismatch")
    author_root = Path(request["workspace"])
    for mount in inspect.get("mounts", []):
        source = Path(mount.get("Source", "")).resolve()
        if source == author_root or author_root in source.parents or source in author_root.parents:
            raise CoordRunnerError("Sandbox mounts the author workspace")
    for key in ("checkout_log", "runtime_log"):
        read_qa_ref(proof.get(key), Path(request["run_dir"]))
    validate_source(proof, request)
    validate_checks(proof, request)
    proof.update(path=str(path), sha256=ref["sha256"])
    return proof


def execute_sandbox(request: dict) -> dict:
    """由受信任的 Python 运行器直接调用沙箱构建与测试命令（严禁由模型代为启动测试）。"""
    run_dir = Path(request["run_dir"])
    try:
        proc = subprocess.run(request["sandbox_command"], text=True, capture_output=True,
                              cwd=request["workspace"], timeout=request["timeout_seconds"])
    except (OSError, subprocess.TimeoutExpired) as err:
        (run_dir / "sandbox_error.txt").write_text(str(err), encoding="utf-8")
        raise CoordRunnerError(f"Sandbox execution blocked; evidence: {run_dir}: {err}") from err
    (run_dir / "sandbox.stdout").write_text(proc.stdout, encoding="utf-8")
    (run_dir / "sandbox.stderr").write_text(proc.stderr, encoding="utf-8")
    path = run_dir / "evidence/server_qa.json"
    if not path.is_file():
        raise CoordRunnerError(f"Sandbox produced no proof (exit {proc.returncode}); evidence: {run_dir}")
    ref = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    proof = validate_server_proof(ref, request)
    if proc.returncode != (0 if proof["passed"] else 1):
        raise CoordRunnerError(f"Sandbox process and proof disagree; evidence: {run_dir}")
    return {"passed": proof["passed"], "execution_completed": True, "task_id": request["task_id"],
            "task_revision": request["task_revision"], "candidate_commit": request["candidate_commit"],
            "server_qa": proof, "request": request, "summary": "Objective sandbox checks completed"}
