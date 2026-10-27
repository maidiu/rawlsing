"""Portable, fail-closed source binding for the S51/S52 G18 dependency.

The accepted G18 source is an external worker-return checkout, not a package in
the S51/S52 tree.  No absolute user path is embedded here.  Resolution order:

1. explicit ``S52_G18_SOURCE`` / ``S51_G18_SOURCE`` / ``G18_SOURCE``;
2. a ``rawlsing-r31j`` sibling discovered from the Git common worktree root;
3. the same relative source under the repository/worktree roots.

Every resolved file is hashed against the accepted source identity.  An
explicit environment path that is missing or forged fails closed rather than
silently falling back to a different checkout.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path
from typing import Iterable, Mapping

G18_RELATIVE = (
    Path("rawlsing-r31j")
    / "WORKER_RETURNS"
    / "SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1"
    / "candidate"
    / "vendor"
    / "bp2"
    / "vendor"
    / "g18"
)

G18_EXPECTED = {
    "lab_sgi1/joint.py": "755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9",
    "lab_sgi1/history.py": "2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1",
}

_ENV_NAMES = ("S52_G18_SOURCE", "S51_G18_SOURCE", "G18_SOURCE", "M35_G18_SOURCE")


class SourceBindingError(RuntimeError):
    """The source dependency is absent, unreadable, or not the accepted source."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git_common_root(return_root: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(return_root), "rev-parse", "--git-common-dir"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    if not value:
        return None
    common = Path(value)
    if not common.is_absolute():
        common = (return_root / common).resolve()
    else:
        common = common.resolve()
    return common.parent if common.name == ".git" else common


def _candidates(return_root: Path, repo_root: Path) -> Iterable[Path]:
    seen: set[str] = set()
    roots = [return_root, repo_root, return_root.parent]
    common = _git_common_root(return_root)
    if common is not None:
        roots.insert(0, common)
    for root in roots:
        candidate = (root / G18_RELATIVE).resolve()
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            yield candidate


def resolve_g18(return_root: str | Path, repo_root: str | Path | None = None) -> Path:
    """Resolve the accepted G18 source without embedding a user-specific path."""
    return_root = Path(return_root).resolve()
    repo_root = Path(repo_root).resolve() if repo_root is not None else return_root.parents[1]

    for name in _ENV_NAMES:
        raw = os.environ.get(name)
        if raw is None or not raw.strip():
            continue
        candidate = Path(raw).expanduser().resolve()
        if not candidate.is_dir():
            raise SourceBindingError(
                "G18_SOURCE_ENV_INVALID",
                f"{name} is not a directory: {candidate}",
            )
        return candidate

    for candidate in _candidates(return_root, repo_root):
        if candidate.is_dir():
            return candidate

    raise SourceBindingError(
        "G18_SOURCE_UNRESOLVED",
        "set S52_G18_SOURCE (or S51_G18_SOURCE) to the accepted G18 checkout",
    )


def verify_expected(root: str | Path, expected: Mapping[str, str]) -> None:
    """Verify every required relative file by SHA-256; fail closed on any drift."""
    root = Path(root)
    for relpath, digest in expected.items():
        path = root / relpath
        if not path.is_file():
            raise SourceBindingError("SOURCE_FILE_MISSING", str(path))
        actual = sha256_file(path)
        if actual != digest:
            raise SourceBindingError(
                "SOURCE_HASH_MISMATCH",
                f"{path}: {actual} != {digest}",
            )


def verify_g18(root: str | Path) -> None:
    verify_expected(root, G18_EXPECTED)


__all__ = [
    "G18_EXPECTED",
    "G18_RELATIVE",
    "SourceBindingError",
    "resolve_g18",
    "sha256_file",
    "verify_expected",
    "verify_g18",
]
