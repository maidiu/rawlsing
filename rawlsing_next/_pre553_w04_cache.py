"""W04 governed persistent accelerator policy and atomic cache primitives.

The accelerator is disposable derived material.  The canonical C11 release is
owned by :mod:`rawlsing_next.pre553_parquet_carrier`; this module never creates a
second canonical store or a query engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Mapping

POLICY_ENV = "RAWLSING_C11_ACCELERATOR_POLICY"
LEGACY_ENV = "RAWLSING_C11_ACCELERATOR_DIR"
POLICY_SCHEMA = "PYAT_C11_ACCELERATOR_POLICY@1"
CACHE_SCHEMA = "PRE553_I02_EVENT_ACCELERATOR@2"
CACHE_METADATA_KEY = b"rawlsing.c11.event_accelerator"
CACHE_ENVELOPE_KEY = b"rawlsing.c11.event_accelerator.envelope"
CACHE_GLOB = "c11-events-*.parquet"
AUTHORIZED_SOURCE_PERMISSIONS = frozenset({
    "NONRESPONDENT_SOURCEFREE",
    "NONRESPONDENT_SOURCEFREE_ONLY",
})
_EVENT_CACHE_PREFIX = "c11-events-"


class AcceleratorPolicyError(ValueError):
    """The host policy/root is absent, unauthorized, malformed or unsafe."""


@dataclass(frozen=True)
class AcceleratorPolicy:
    root: Path
    max_bytes: int
    max_files: int
    max_age_seconds: int
    source_permission: str
    authorization_id: str
    policy_digest: str
    trusted_root_id: str


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def _private_dir(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    return (
        stat.S_ISDIR(info.st_mode)
        and not stat.S_ISLNK(info.st_mode)
        and info.st_uid == os.getuid()
        and info.st_mode & 0o077 == 0
    )


def _private_regular(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    return (
        stat.S_ISREG(info.st_mode)
        and not stat.S_ISLNK(info.st_mode)
        and info.st_uid == os.getuid()
        and info.st_mode & 0o022 == 0
    )


def _positive_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise AcceleratorPolicyError(f"retention_budget.{name} must be a positive integer")
    return value


def _policy_from_mapping(data: Mapping[str, Any], *, source: str) -> AcceleratorPolicy:
    if data.get("schema") != POLICY_SCHEMA or data.get("enabled") is not True:
        raise AcceleratorPolicyError("accelerator policy schema/enabled is invalid")
    root_value = data.get("root")
    if not isinstance(root_value, str) or not Path(root_value).is_absolute():
        raise AcceleratorPolicyError("accelerator policy root must be an absolute path")
    root = Path(root_value)
    if not _private_dir(root):
        raise AcceleratorPolicyError("accelerator policy root is absent or not a private owned directory")
    permission = data.get("source_permission")
    if permission not in AUTHORIZED_SOURCE_PERMISSIONS:
        raise AcceleratorPolicyError("accelerator policy source_permission is not a nonrespondent sourcefree grant")
    authorization = data.get("authorization_id")
    if not isinstance(authorization, str) or not authorization.strip():
        raise AcceleratorPolicyError("accelerator policy authorization_id is required")
    budget = data.get("retention_budget")
    if not isinstance(budget, Mapping):
        raise AcceleratorPolicyError("accelerator policy retention_budget is required")
    max_bytes = _positive_int(budget.get("max_bytes"), "max_bytes")
    max_files = _positive_int(budget.get("max_files"), "max_files")
    max_age_seconds = _positive_int(budget.get("max_age_seconds"), "max_age_seconds")
    digest = _sha(_canonical_json(dict(data)).encode("utf-8"))
    trusted_root = _sha(_canonical_json({
        "policy": digest,
        "root": str(root.resolve()),
        "source": source,
        "source_permission": permission,
        "authorization_id": authorization.strip(),
    }).encode("utf-8"))
    return AcceleratorPolicy(
        root=root.resolve(),
        max_bytes=max_bytes,
        max_files=max_files,
        max_age_seconds=max_age_seconds,
        source_permission=str(permission),
        authorization_id=authorization.strip(),
        policy_digest=digest,
        trusted_root_id=trusted_root,
    )


def _load_policy_file(path: Path) -> AcceleratorPolicy:
    if not _private_regular(path):
        raise AcceleratorPolicyError("accelerator policy file is absent or not an owned private file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AcceleratorPolicyError("accelerator policy file is unreadable or invalid JSON") from exc
    if not isinstance(data, Mapping):
        raise AcceleratorPolicyError("accelerator policy root must be an object")
    return _policy_from_mapping(data, source="policy_file")


def _legacy_test_policy() -> AcceleratorPolicy | None:
    """Explicit sourcefree pytest temp-root fallback; never a deployment grant.

    Existing focused tests configure ``RAWLSING_C11_ACCELERATOR_DIR``.  That
    path remains supported only while pytest is executing and only below the
    platform temporary root, so production/default callers cannot obtain a
    writable cache merely by setting an environment variable.
    """
    if not os.environ.get("PYTEST_CURRENT_TEST"):
        return None
    configured = os.environ.get(LEGACY_ENV, "").strip()
    if not configured:
        return None
    root = Path(configured)
    if not root.is_absolute():
        return None
    temp_root = Path(tempfile.gettempdir()).resolve()
    try:
        root.resolve().relative_to(temp_root)
    except ValueError:
        return None
    if not root.exists():
        try:
            root.mkdir(mode=0o700, parents=True, exist_ok=False)
        except OSError:
            return None
    if not _private_dir(root):
        return None
    data = {
        "schema": POLICY_SCHEMA,
        "enabled": True,
        "root": str(root.resolve()),
        "source_permission": "NONRESPONDENT_SOURCEFREE",
        "authorization_id": "PYTEST_TEMP_ROOT_EXPLICIT",
        "retention_budget": {
            "max_bytes": 268_435_456,
            "max_files": 16,
            "max_age_seconds": 86_400,
        },
    }
    return _policy_from_mapping(data, source="pytest_temp_root")


def load_policy() -> AcceleratorPolicy | None:
    """Resolve an operative policy or safely return ``None``.

    A configured policy is authoritative: invalid/unauthorized policy never
    falls back to the legacy directory variable.  No root is created here except
    the explicit pytest-only temp fallback.
    """
    configured = os.environ.get(POLICY_ENV, "").strip()
    if configured:
        try:
            return _load_policy_file(Path(configured))
        except (OSError, AcceleratorPolicyError):
            return None
    return _legacy_test_policy()


def cache_file(policy: AcceleratorPolicy, key: str) -> Path:
    if not isinstance(key, str) or len(key) != 64 or any(ch not in "0123456789abcdef" for ch in key):
        raise AcceleratorPolicyError("cache key must be lowercase sha256 hex")
    return policy.root / f"{_EVENT_CACHE_PREFIX}{key[0]}.parquet"


def _owned_cache_file(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    return (
        stat.S_ISREG(info.st_mode)
        and not stat.S_ISLNK(info.st_mode)
        and info.st_uid == os.getuid()
        and info.st_mode & 0o022 == 0
    )


def prune(policy: AcceleratorPolicy, *, keep: Path | None = None, now: float | None = None) -> None:
    """Apply the policy retention budget to disposable cache files only."""
    import time

    current = time.time() if now is None else now
    keep_resolved = keep.resolve() if keep is not None else None

    def entries() -> list[tuple[float, int, Path]]:
        result = []
        for candidate in policy.root.glob(CACHE_GLOB):
            try:
                if not _owned_cache_file(candidate):
                    continue
                info = candidate.stat()
                result.append((info.st_mtime, info.st_size, candidate))
            except OSError:
                continue
        return sorted(result)

    for mtime, _, path in entries():
        if path.resolve() == keep_resolved:
            continue
        if current - mtime > policy.max_age_seconds:
            try:
                path.unlink()
            except OSError:
                pass
    while True:
        current_entries = entries()
        if not current_entries:
            return
        total_bytes = sum(size for _, size, _ in current_entries)
        if len(current_entries) <= policy.max_files and total_bytes <= policy.max_bytes:
            return
        oldest = None
        for item in current_entries:
            if item[2].resolve() != keep_resolved:
                oldest = item
                break
        if oldest is None:
            return
        try:
            oldest[2].unlink()
        except OSError:
            return


def enforce_after_write(policy: AcceleratorPolicy, path: Path) -> bool:
    """Return False and remove the new file if the policy budget cannot hold it."""
    try:
        new_size = path.stat().st_size
    except OSError:
        return False
    if new_size > policy.max_bytes:
        try:
            path.unlink()
        except OSError:
            pass
        return False
    prune(policy, keep=path)
    entries = []
    for candidate in policy.root.glob(CACHE_GLOB):
        try:
            info = candidate.stat()
        except OSError:
            continue
        entries.append((info.st_size, candidate))
    if sum(size for size, _ in entries) > policy.max_bytes or len(entries) > policy.max_files:
        try:
            path.unlink()
        except OSError:
            pass
        return False
    return path.is_file()


def fsync_dir(path: Path) -> None:
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def atomic_replace(staged: Path, destination: Path) -> None:
    os.replace(staged, destination)
    fsync_dir(destination.parent)
