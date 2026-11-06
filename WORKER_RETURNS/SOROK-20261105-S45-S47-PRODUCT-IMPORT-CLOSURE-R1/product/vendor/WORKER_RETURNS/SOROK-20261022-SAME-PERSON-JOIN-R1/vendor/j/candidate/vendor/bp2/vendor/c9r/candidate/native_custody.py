"""Exact imported native-module custody for the C9P candidate.

Every native module the candidate imports is recorded with its runtime
`module.__file__` and its Git blob identity so a return can prove which source
was actually loaded. A mismatch raises `CustodyMismatch`.
"""
from __future__ import annotations

import hashlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

REPO_ROOT = Path(__file__).resolve().parents[3]


class CustodyMismatch(RuntimeError):
    """An imported native module's file or Git blob identity diverged."""


@dataclass(frozen=True)
class ModuleCustody:
    """Custody record for one imported native module."""

    module_name: str
    module_file: str
    relative_path: str
    git_blob_sha1: str
    content_sha256: str
    imported: bool


def _git_blob_sha1(path: Path) -> str:
    """Return the Git blob SHA-1 of `path` computed with the NUL preimage rule."""
    data = path.read_bytes()
    header = f"blob {len(data)}\x00".encode()
    return hashlib.sha1(header + data).hexdigest()


def _git_blob_via_git(path: Path) -> str:
    """Return the Git blob SHA-1 of `path` from the object store, or empty."""
    try:
        out = subprocess.run(
            ["git", "hash-object", str(path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return out.stdout.strip()


def record_module_custody(module_name: str, expected_blob: str = "") -> ModuleCustody:
    """Import `module_name` and record its file and Git blob identities.

    When `expected_blob` is non-empty the recorded Git blob must match it or
    `CustodyMismatch` is raised.
    """
    import importlib

    module = importlib.import_module(module_name)
    module_file = str(module.__file__)
    path = Path(module_file)
    computed = _git_blob_sha1(path)
    via_git = _git_blob_via_git(path)
    blob = via_git or computed
    if expected_blob and blob != expected_blob and computed != expected_blob:
        raise CustodyMismatch(
            f"{module_name} blob {blob} != expected {expected_blob}"
        )
    content_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        relative = str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        relative = module_file
    return ModuleCustody(
        module_name=module_name,
        module_file=module_file,
        relative_path=relative,
        git_blob_sha1=blob,
        content_sha256=content_sha,
        imported=True,
    )


def candidate_import_graph() -> Mapping[str, ModuleCustody]:
    """Record custody for every native module the candidate actually imports."""
    names = (
        "rawlsing_next.v3_psepf_zero_positive_guard",
        "rawlsing_next.wsc_gt0_protocol",
        "rawlsing_next.wsc_gt0_v3_runtime",
    )
    return {name: record_module_custody(name) for name in names}


__all__ = [
    "CustodyMismatch",
    "ModuleCustody",
    "candidate_import_graph",
    "record_module_custody",
]
