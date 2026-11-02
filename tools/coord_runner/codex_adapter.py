#!/usr/bin/env python3
"""Read-only independent Codex audits with bounded execution and durable logs."""

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
    session_id: str
    decision: str
    output_text: str
    tokens_used: int
    raw_log: str


@dataclass
class CodexAuditOptions:
    workdir: Path
    artifacts_dir: Path
    schema: dict


def audit_schema() -> dict:
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
    """Accept only an entire JSON document (optionally fenced), never keyword search."""
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
    """Launch a new read-only Codex process; never downgrade to another engine."""

    def __init__(self, codex_bin: Optional[Path] = None,
                 default_model: str = DEFAULT_MODEL, timeout_seconds: int = 180):
        self.codex_bin = (codex_bin or DEFAULT_CODEX_BIN).resolve()
        self.default_model = default_model
        self.timeout_seconds = timeout_seconds

    def check_availability(self) -> bool:
        if not self.codex_bin.is_file() or not os.access(self.codex_bin, os.X_OK):
            return False
        try:
            result = subprocess.run([str(self.codex_bin), "--version"],
                                    text=True, capture_output=True, timeout=10)
            return result.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            return False

    def _parse_codex_events(self, stdout: str) -> tuple:
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
        return [str(self.codex_bin), "exec", "--skip-git-repo-check",
                "--sandbox", "read-only", "-c", 'approval_policy="never"',
                "-m", self.default_model, "-C", str(options.workdir.resolve()), "--json",
                "--output-schema", str(options.artifacts_dir / "schema.json"),
                "--output-last-message", str(options.artifacts_dir / "final.json"), "-"]

    def _run_process(self, prompt: str, options: CodexAuditOptions) -> None:
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
        model_name = model or self.default_model
        adapter = CodexReviewAdapter(self.codex_bin, model_name, self.timeout_seconds)
        root = Path(tempfile.mkdtemp(prefix="codex_review_"))
        return adapter.execute_audit(prompt, CodexAuditOptions(workdir, root / "audit", audit_schema()))
