#!/usr/bin/env python3
"""OpenAI Codex CLI execution adapter for independent review."""

from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
from typing import Optional

import sys
if __package__:
    from .errors import CoordRunnerError
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from coord_runner.errors import CoordRunnerError

DEFAULT_CODEX_BIN = Path("/home/sushaohua/.local/bin/codex")
DEFAULT_MODEL = "gpt-6-luna"


@dataclass
class CodexReviewResult:
    """Structured result returned by independent Codex review."""
    session_id: str
    decision: str
    output_text: str
    tokens_used: int
    raw_log: str


class CodexReviewAdapter:
    """Executes non-interactive Codex reviews strictly without fallback."""

    def __init__(
        self,
        codex_bin: Optional[Path] = None,
        default_model: str = DEFAULT_MODEL,
    ):
        self.codex_bin = (codex_bin or DEFAULT_CODEX_BIN).resolve()
        self.default_model = default_model

    def check_availability(self) -> bool:
        if not self.codex_bin.is_file() or not os.access(self.codex_bin, os.X_OK):
            return False
        try:
            res = subprocess.run([str(self.codex_bin), "--version"],
                                 text=True, capture_output=True, timeout=10)
            return res.returncode == 0
        except OSError:
            return False

    def _parse_codex_events(self, stdout: str) -> tuple:
        session_id = None
        tokens_used = 0
        texts = []
        for line in stdout.strip().split("\n"):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
                if ev.get("type") == "thread.started":
                    session_id = ev.get("thread_id")
                elif ev.get("type") == "item.completed":
                    item = ev.get("item", {})
                    if item.get("type") == "agent_message":
                        texts.append(item.get("text", ""))
                elif ev.get("type") == "turn.completed":
                    usage = ev.get("usage", {})
                    tokens_used += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
            except json.JSONDecodeError:
                continue
        return session_id, tokens_used, "\n".join(texts).strip()

    def execute_review(
        self,
        prompt: str,
        workdir: Path,
        model: Optional[str] = None,
    ) -> CodexReviewResult:
        if not self.codex_bin.is_file() or not os.access(self.codex_bin, os.X_OK):
            raise CoordRunnerError(f"Codex binary unavailable at {self.codex_bin}")
        used_model = model or self.default_model
        cmd = [
            str(self.codex_bin), "exec", "--skip-git-repo-check",
            "-m", used_model, "-C", str(workdir.resolve()), "--json", prompt,
        ]
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=180)
        if proc.returncode != 0:
            err = proc.stderr.strip() or f"exit code {proc.returncode}"
            raise CoordRunnerError(f"Codex review execution failed: {err}")
        session_id, tokens_used, text = self._parse_codex_events(proc.stdout)
        if not session_id:
            raise CoordRunnerError(f"Codex output lacked valid thread_id: {proc.stdout[:200]}")
        decision = "APPROVED" if "APPROVED" in text else "REJECTED"
        return CodexReviewResult(
            session_id=session_id,
            decision=decision,
            output_text=text,
            tokens_used=tokens_used,
            raw_log=proc.stdout,
        )
