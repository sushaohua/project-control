#!/usr/bin/env python3
"""COORD 运行器状态快照（Checkpoint）的原子落盘序列化与崩溃恢复管理模块。"""

import datetime
import json
import os
from pathlib import Path
from typing import Optional

from .errors import CheckpointCorruptError
from .models import CoordState


class CheckpointManager:
    """管理 COORD 全局状态快照的原子保存、加载校验与崩溃安全恢复。"""

    def __init__(self):
        """初始化 Checkpoint 管理器实例。"""
        pass

    def save_checkpoint(self, path: Path, state: CoordState) -> None:
        """通过 PID 后缀临时文件加 os.replace 原子重命名机制保存 CoordState 快照。"""
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
        """加载并校验指定路径的 Checkpoint JSON 文件，损坏或缺少 schema_version 时抛出异常。"""
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
        """当 Checkpoint 文件存在时加载并返回状态快照，文件不存在时安全返回 None。"""
        target_path = Path(path).resolve()
        if not target_path.is_file():
            return None
        return self.load_checkpoint(target_path)
