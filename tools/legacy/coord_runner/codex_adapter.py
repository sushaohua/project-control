#!/usr/bin/env python3
"""带超时边界与持久化事件日志的只读独立 Codex 审计进程适配器。"""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Optional

from .errors import CoordRunnerError

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_MODEL = "gpt-6-luna"


@dataclass
class CodexReviewResult:
    """独立 Codex 审计会话的结构化返回结果（真实 thread_id、结论、输出文本、Token 消耗及原始事件流）。"""
    session_id: str
    decision: str
    output_text: str
    tokens_used: int
    raw_log: str


@dataclass
class CodexAuditOptions:
    """单次 Codex 只读审计运行的工作目录、产物输出目录与 JSON Schema 约束选项。"""
    workdir: Path
    artifacts_dir: Path
    schema: dict


def audit_schema() -> dict:
    """构造强制约束 Codex 最终输出格式的 JSON Schema 定义。"""
    properties = {
        "task_id": {"type": "string"}, "task_revision": {"type": "integer"},
        "candidate_commit": {"type": "string"}, "role": {"type": "string"},
        "decision": {"type": "string", "enum": ["APPROVED", "REJECTED", "BLOCKED"]},
        "summary": {"type": "string"}, "findings": {"type": "array", "items": {"type": "string"}},
        "accepted_scope": {"type": "string"}, "unexecuted": {"type": "array", "items": {"type": "string"}},
    }
    return {"type": "object", "properties": properties,
            "required": list(properties), "additionalProperties": False}


def parse_final_response(text: str) -> dict:
    """严格解析完整 JSON 响应文档（允许可选的 ```json 代码块包裹），严禁使用关键字模糊匹配。"""
    value = text.strip()
    if value.startswith("```json\n") and value.endswith("```"):
        value = value[len("```json\n"):-3].strip()
    try:
        data = json.loads(value)
    except (ValueError, TypeError) as err:
        raise CoordRunnerError("Codex final response is not a valid structured audit") from err
    if not isinstance(data, dict) or data.get("decision") not in {"APPROVED", "REJECTED", "BLOCKED"}:
        raise CoordRunnerError("Codex audit lacks an exact supported decision")
    return data


class CodexReviewAdapter:
    """启动全新只读 Codex CLI 子进程执行独立审计（严禁降级或回退至其他执行引擎）。"""

    def __init__(self, codex_bin: Optional[Path] = None,
                 default_model: str = DEFAULT_MODEL, timeout_seconds: int = 180):
        """初始化 Codex 审计适配器，绑定二进制路径、默认模型名称与超时秒数。"""
        self.codex_bin = (codex_bin or DEFAULT_CODEX_BIN).resolve()
        self.default_model = default_model
        self.timeout_seconds = timeout_seconds

    def check_availability(self) -> bool:
        """检查本地 Codex CLI 二进制是否存在、可执行且 `--version` 正常响应。"""
        if not self.codex_bin.is_file() or not os.access(self.codex_bin, os.X_OK):
            return False
        try:
            result = subprocess.run([str(self.codex_bin), "--version"],
                                    text=True, capture_output=True, timeout=10)
            return result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False

    def _parse_codex_events(self, stdout: str) -> tuple:
        """从 Codex JSONL 事件流中提取真实 thread_id、累计 Token 用量与最后一条消息文本。"""
        session_id, tokens_used = None, 0
        messages = []
        for line in stdout.splitlines():
            try:
                event = json.loads(line)
            except ValueError:
                continue
            if not isinstance(event, dict):
                continue
            if event.get("type") == "thread.started":
                session_id = event.get("thread_id")
            elif event.get("type") == "item.completed":
                item = event.get("item", {})
                if item.get("type") == "agent_message":
                    messages.append(item.get("text", ""))
            elif event.get("type") == "turn.completed":
                usage = event.get("usage", {})
                tokens_used += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
        return session_id, tokens_used, messages[-1] if messages else ""

    def _command(self, options: CodexAuditOptions) -> list:
        """组装带 `--sandbox read-only` 与 `--output-schema` 的 `codex exec` 命令行参数列表。"""
        return [str(self.codex_bin), "exec", "--skip-git-repo-check",
                "--sandbox", "read-only", "-c", 'approval_policy="never"',
                "-m", self.default_model, "-C", str(options.workdir.resolve()), "--json",
                "--output-schema", str(options.artifacts_dir / "schema.json"),
                "--output-last-message", str(options.artifacts_dir / "final.json"), "-"]

    def _run_process(self, prompt: str, options: CodexAuditOptions) -> None:
        """执行 Codex 子进程并将提示词、JSONL 标准输出与标准错误持久化到审计产物目录。"""
        command = self._command(options)
        (options.artifacts_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        with (options.artifacts_dir / "codex.jsonl").open("w", encoding="utf-8") as stdout:
            with (options.artifacts_dir / "codex.stderr").open("w", encoding="utf-8") as stderr:
                try:
                    result = subprocess.run(command, input=prompt, text=True, stdout=stdout,
                                            stderr=stderr, timeout=self.timeout_seconds)
                except (OSError, subprocess.TimeoutExpired) as err:
                    (options.artifacts_dir / "error.txt").write_text(str(err), encoding="utf-8")
                    raise CoordRunnerError(f"Codex execution blocked; logs: {options.artifacts_dir}") from err
        if result.returncode != 0:
            raise CoordRunnerError(f"Codex execution failed (exit {result.returncode}); logs: {options.artifacts_dir}")

    def execute_audit(self, prompt: str, options: CodexAuditOptions) -> CodexReviewResult:
        """创建全新审计目录、运行只读 Codex 进程并校验返回的真实会话 ID 与结构化结论。"""
        options.artifacts_dir.mkdir(parents=True, exist_ok=False)
        (options.artifacts_dir / "schema.json").write_text(json.dumps(options.schema), encoding="utf-8")
        if not self.codex_bin.is_file() or not os.access(self.codex_bin, os.X_OK):
            raise CoordRunnerError(f"Codex binary unavailable at {self.codex_bin}; logs: {options.artifacts_dir}")
        self._run_process(prompt, options)
        try:
            final = (options.artifacts_dir / "final.json").read_text(encoding="utf-8")
            raw = (options.artifacts_dir / "codex.jsonl").read_text(encoding="utf-8")
            session, tokens, _ = self._parse_codex_events(raw)
            if not session:
                raise CoordRunnerError("Codex output lacked an actual thread_id")
            decision = parse_final_response(final)["decision"]
        except (CoordRunnerError, OSError, ValueError, TypeError) as err:
            raise CoordRunnerError(f"Codex output invalid; logs: {options.artifacts_dir}: {err}") from err
        return CodexReviewResult(session, decision, final, tokens, raw)

    def execute_review(self, prompt: str, workdir: Path,
                       model: Optional[str] = None) -> CodexReviewResult:
        """在临时目录中启动单次独立只读 Codex 审阅并返回 CodexReviewResult。"""
        model_name = model or self.default_model
        adapter = CodexReviewAdapter(self.codex_bin, model_name, self.timeout_seconds)
        root = Path(tempfile.mkdtemp(prefix="codex_review_"))
        return adapter.execute_audit(prompt, CodexAuditOptions(workdir, root / "audit", audit_schema()))
