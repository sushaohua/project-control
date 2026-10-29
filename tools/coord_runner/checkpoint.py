#!/usr/bin/env python3
"""Checkpoint serialization and crash recovery for COORD runner."""

import datetime
import json
import os
from pathlib import Path
from typing import Optional

from .errors import CheckpointCorruptError
from .models import CoordState


class CheckpointManager:
    """Manages atomic saving, loading, and recovery of COORD state."""

    def __init__(self):
        pass

    def save_checkpoint(self, path: Path, state: CoordState) -> None:
        target_path = Path(path).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        now_str = datetime.datetime.now().astimezone().isoformat()
        state.last_updated = now_str
        payload = json.dumps(state.to_dict(), indent=2, ensure_ascii=False)
        tmp_path = target_path.with_suffix(f".tmp_{os.getpid()}")
        try:
            tmp_path.write_text(payload, encoding="utf-8")
            os.replace(tmp_path, target_path)
        except OSError as err:
            if tmp_path.exists():
                tmp_path.unlink()
            raise CheckpointCorruptError(f"Failed to write checkpoint to {target_path}: {err}")

    def load_checkpoint(self, path: Path) -> CoordState:
        target_path = Path(path).resolve()
        if not target_path.is_file():
            raise FileNotFoundError(f"Checkpoint file does not exist: {target_path}")
        try:
            content = target_path.read_text(encoding="utf-8")
            data = json.loads(content)
        except (OSError, json.JSONDecodeError) as err:
            raise CheckpointCorruptError(f"Checkpoint file {target_path} is corrupt: {err}")
        if not isinstance(data, dict) or "schema_version" not in data:
            raise CheckpointCorruptError(f"Checkpoint file {target_path} missing valid schema")
        return CoordState.from_dict(data)

    def safe_load(self, path: Path) -> Optional[CoordState]:
        target_path = Path(path).resolve()
        if not target_path.is_file():
            return None
        return self.load_checkpoint(target_path)
