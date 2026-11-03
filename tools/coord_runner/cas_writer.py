#!/usr/bin/env python3
"""File-level SHA256 Compare-And-Swap (CAS) writer with durable write-intent records."""

from dataclasses import dataclass
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Iterator, Optional, Union

from .errors import CasConflictError

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class FileDigestSnapshot:
    """Immutable byte snapshot and SHA256 digest of a file read from disk."""
    path: Path
    raw_bytes: bytes
    sha256: str

    @property
    def text(self) -> str:
        """Decode raw bytes as strict UTF-8 text."""
        return self.raw_bytes.decode("utf-8")

    def __iter__(self) -> Iterator[object]:
        """Support `(raw_bytes, sha256) = read_with_digest(path)` unpacking."""
        yield self.raw_bytes
        yield self.sha256


@dataclass(frozen=True)
class WriteIntent:
    """Pre-write optimistic concurrency intent bound to exact digests."""
    operation_id: str
    target_path: Path
    expected_sha256: Optional[str]
    planned_sha256: str
    summary: str = ""
    intent_dir: Optional[Path] = None


def _to_bytes(content: Union[str, bytes]) -> bytes:
    if isinstance(content, bytes):
        return content
    if isinstance(content, str):
        return content.encode("utf-8")
    raise TypeError(f"CAS content must be str or bytes, got {type(content).__name__}")


def compute_bytes_sha256(data: Union[str, bytes]) -> str:
    """Compute lowercase 64-hex SHA256 digest for str or bytes."""
    return hashlib.sha256(_to_bytes(data)).hexdigest()


def compute_file_sha256(path: Path) -> str:
    """Compute lowercase 64-hex SHA256 digest from physical file bytes."""
    if path is None:
        raise ValueError("path must not be None")
    target = Path(path)
    if not target.is_file():
        raise FileNotFoundError(f"Cannot hash missing file: {target}")
    return hashlib.sha256(target.read_bytes()).hexdigest()


def _validate_sha256(digest: Optional[str], field_name: str) -> str:
    if not isinstance(digest, str) or not SHA256_RE.match(digest):
        raise CasConflictError(
            f"Invalid {field_name}: expected 64-char lowercase hex SHA256, got {digest!r}",
            {"field": field_name, "value": digest},
        )
    return digest


def read_with_digest(path: Path) -> FileDigestSnapshot:
    """Read physical bytes from disk and return snapshot with exact SHA256."""
    if path is None:
        raise ValueError("path must not be None")
    target = Path(path).resolve()
    if not target.is_file():
        raise FileNotFoundError(f"Target file does not exist: {target}")
    raw = target.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    return FileDigestSnapshot(path=target, raw_bytes=raw, sha256=digest)


def record_write_intent(intent: WriteIntent) -> Optional[Path]:
    """Validate and optionally persist a write intent before mutating target file."""
    if not intent.operation_id or not isinstance(intent.operation_id, str):
        raise CasConflictError("WriteIntent requires non-empty operation_id", {})
    _validate_sha256(intent.planned_sha256, "planned_sha256")
    if intent.expected_sha256 is not None:
        _validate_sha256(intent.expected_sha256, "expected_sha256")
    if intent.intent_dir is None:
        return None
    intent_dir = Path(intent.intent_dir).resolve()
    intent_dir.mkdir(parents=True, exist_ok=True)
    safe_op = re.sub(r"[^A-Za-z0-9_.-]", "_", intent.operation_id)
    out_path = intent_dir / f"{safe_op}.intent.json"
    payload = {
        "operation_id": intent.operation_id,
        "target_path": str(Path(intent.target_path).resolve()),
        "expected_sha256": intent.expected_sha256,
        "planned_sha256": intent.planned_sha256,
        "summary": intent.summary,
        "recorded_at": datetime.datetime.now().astimezone().isoformat(),
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def _verify_intent_binding(
    target: Path,
    expected_sha256: Optional[str],
    planned_sha256: str,
    intent: Optional[WriteIntent],
) -> Optional[str]:
    if intent is None:
        return None
    intent_target = Path(intent.target_path).resolve()
    if intent_target != target:
        raise CasConflictError(
            f"WriteIntent target mismatch: {intent_target} != {target}",
            {"target_path": str(target), "intent_target": str(intent_target)},
        )
    if intent.expected_sha256 != expected_sha256 or intent.planned_sha256 != planned_sha256:
        raise CasConflictError(
            "WriteIntent expected/planned SHA256 does not match write request",
            {
                "target_path": str(target),
                "expected_sha256": expected_sha256,
                "intent_expected_sha256": intent.expected_sha256,
                "planned_sha256": planned_sha256,
                "intent_planned_sha256": intent.planned_sha256,
            },
        )
    saved = record_write_intent(intent)
    return str(saved) if saved else None


def _atomic_replace_bytes(target: Path, raw: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target.with_name(f".{target.name}.cas_tmp_{os.getpid()}")
    fd = os.open(str(tmp_path), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    except OSError:
        os.close(fd)
        if tmp_path.exists():
            tmp_path.unlink()
        raise
    os.close(fd)
    os.replace(str(tmp_path), str(target))


def write_cas(
    path: Path,
    content: Union[str, bytes],
    expected_sha256: str,
    intent: Optional[WriteIntent] = None,
) -> str:
    """Atomically overwrite `path` only if its current on-disk SHA256 equals `expected_sha256`."""
    if path is None:
        raise ValueError("path must not be None")
    _validate_sha256(expected_sha256, "expected_sha256")
    target = Path(path).resolve()
    raw = _to_bytes(content)
    planned_sha = hashlib.sha256(raw).hexdigest()
    intent_ref = _verify_intent_binding(target, expected_sha256, planned_sha, intent)
    if not target.is_file():
        raise CasConflictError(
            f"CAS conflict on {target}: file missing (expected {expected_sha256})",
            {"target_path": str(target), "expected_sha256": expected_sha256,
             "actual_sha256": None, "intent_path": intent_ref},
        )
    actual_sha = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual_sha != expected_sha256:
        raise CasConflictError(
            f"CAS conflict on {target}: expected {expected_sha256}, found {actual_sha}",
            {"target_path": str(target), "expected_sha256": expected_sha256,
             "actual_sha256": actual_sha, "intent_path": intent_ref,
             "operation_id": intent.operation_id if intent else None},
        )
    _atomic_replace_bytes(target, raw)
    return planned_sha


def create_exclusive(
    path: Path,
    content: Union[str, bytes],
    intent: Optional[WriteIntent] = None,
) -> str:
    """Atomically create a brand-new file; fail with CasConflictError if it already exists."""
    if path is None:
        raise ValueError("path must not be None")
    target = Path(path).resolve()
    raw = _to_bytes(content)
    planned_sha = hashlib.sha256(raw).hexdigest()
    intent_ref = _verify_intent_binding(target, None, planned_sha, intent)
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(target), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError as err:
        actual_sha = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
        raise CasConflictError(
            f"Exclusive create conflict on {target}: file already exists (sha256={actual_sha})",
            {"target_path": str(target), "expected_sha256": None,
             "actual_sha256": actual_sha, "intent_path": intent_ref,
             "operation_id": intent.operation_id if intent else None},
        ) from err
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    return planned_sha
