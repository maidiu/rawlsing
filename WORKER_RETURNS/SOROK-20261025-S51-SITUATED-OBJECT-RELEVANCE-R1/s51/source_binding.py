"""Verified source custody for the S48/S49/S51/S52 and accepted G18 seams.

The manifest is authored in the F0-R2-owned portability directory.  It contains
only relative paths and content hashes; absolute checkout roots are resolved at
runtime and must remain inside an explicitly allowed root.  Stdlib hashing is
deliberately out of scope: the bounded nonstdlib closure is the F0-managed
S48/S49/S51/S52 packages, the accepted G18 package and the accepted R30A
package.  A preloaded managed module or a changed/unlisted file fails closed
before the S49/S51/G18/R30A imports are allowed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

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
    "lab_sgi1/__init__.py": "c9c5dbab3d2409f022df3794257418d0b85a14fe28a18a7c3652fbe86005ed92",
    "lab_sgi1/core.py": "87f8e0554d467a6395ce1dfcc5a346b12074b85a39757e153bd975e2f9c4237d",
    "lab_sgi1/proposal.py": "fe97a4166d52fcd6f21b8ab0c776edbfc5a0763747954a9e2e645e597713f0f5",
    "lab_sgi1/joint.py": "755820d7d703cd459aec8271a784c39a69e9374aae501da1cd9f37bbccc21ee9",
    "lab_sgi1/history.py": "2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1",
}

# The manifest is the portable registry.  It lives in the new R2-owned
# directory, not in any accepted author return.
MANIFEST_RELATIVE = Path(
    "WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json"
)

ROOT_PROVENANCE = {
    "repo": {
        "role": "F0_R2_SOURCE_TREE",
        "owner": "SOROK_SYN02_F0_R2_IMPLEMENTER",
        "scope": "sourcefree_test_only",
        "origin": "agent/sorok-syn02-f0-r2-source-custody-repair-r1",
        "effective_from": "2026-10-27",
    },
    "g18": {
        "role": "ACCEPTED_G18_PACKAGE",
        "owner": "R31J_GM01_SOURCE_PERSON",
        "scope": "accepted_vendor_source",
        "origin": "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1",
        "effective_from": "2026-10-21",
    },
    "r30a": {
        "role": "ACCEPTED_R30A_PACKAGE",
        "owner": "R30A_FIRST_NEIGHBOR_SESSION",
        "scope": "accepted_dependency_source",
        "origin": "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1",
        "effective_from": "2026-10-22",
    },
}
_ROOT_KEYS = ("role", "owner", "scope", "origin", "effective_from")
_MANAGED_PREFIXES = ("s48", "s49", "s51", "s52", "lab_sgi1", "r30a")
_ENV_NAMES = ("S52_G18_SOURCE", "S51_G18_SOURCE", "G18_SOURCE", "M35_G18_SOURCE")


class SourceBindingError(RuntimeError):
    """The source dependency is absent, unverifiable, or outside its root."""

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


def _normalise_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    if path.is_symlink():
        raise SourceBindingError("SOURCE_ROOT_SYMLINK", str(path))
    resolved = path.resolve()
    if not resolved.is_dir():
        raise SourceBindingError("SOURCE_ROOT_MISSING", str(resolved))
    return resolved


def _env_root(name: str) -> Path | None:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    return _normalise_path(raw)


def _allowed_roots(repo: Path, common: Path, join_e: Path) -> list[Path]:
    values = [repo, common, join_e]
    for parent in (common / "rawlsing-r31j", repo / "rawlsing-r31j",
                   repo / "rawlsing-join-e"):
        if parent.is_dir():
            values.append(parent)
    extra = os.environ.get("S52_ALLOWED_ROOTS", "").strip()
    if extra:
        for raw in extra.split(os.pathsep):
            if raw.strip():
                values.append(_normalise_path(raw.strip()))
    seen: set[str] = set()
    out: list[Path] = []
    for value in values:
        resolved = value.resolve()
        key = str(resolved)
        if key not in seen:
            seen.add(key)
            out.append(resolved)
    return out


def _resolve_join_e(repo: Path, common: Path) -> Path:
    explicit = os.environ.get("S37_JOIN_E_RETURN", "").strip() or os.environ.get(
        "S52_JOIN_E_SOURCE", ""
    ).strip()
    if explicit:
        return _normalise_path(explicit)
    candidates = (
        common / "rawlsing-join-e" / "WORKER_RETURNS"
        / "SOROK-20261022-SAME-PERSON-JOIN-R1",
        repo / "rawlsing-join-e" / "WORKER_RETURNS"
        / "SOROK-20261022-SAME-PERSON-JOIN-R1",
        repo.parent / "rawlsing-join-e" / "WORKER_RETURNS"
        / "SOROK-20261022-SAME-PERSON-JOIN-R1",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return _normalise_path(candidate)
    raise SourceBindingError("SOURCE_ROOT_MISSING", "join_e accepted root")


def _resolve_r30a(join_e: Path) -> Path:
    explicit = os.environ.get("S52_R30A_SOURCE", "").strip()
    if explicit:
        return _normalise_path(explicit)
    candidate = join_e / "vendor" / "e" / "vendor" / "r30a"
    if not candidate.is_dir():
        raise SourceBindingError("SOURCE_ROOT_MISSING", str(candidate))
    return _normalise_path(candidate)


def _candidates(return_root: Path, repo_root: Path, common: Path | None) -> list[Path]:
    roots = [return_root, repo_root, return_root.parent]
    if common is not None:
        roots.insert(0, common)
    seen: set[str] = set()
    out: list[Path] = []
    for root in roots:
        candidate = root / G18_RELATIVE
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        out.append(candidate)
    return out


def resolve_g18(return_root: str | Path, repo_root: str | Path | None = None) -> Path:
    """Resolve G18 without a PATH lookup or a silent laptop-specific default."""
    return_root = Path(return_root).resolve()
    repo_root = Path(repo_root).resolve() if repo_root is not None else return_root.parents[1]
    common = _git_common_root(return_root)

    explicit: list[tuple[str, Path]] = []
    for name in _ENV_NAMES:
        raw = os.environ.get(name, "").strip()
        if not raw:
            continue
        path = Path(raw).expanduser()
        if path.is_symlink():
            raise SourceBindingError("G18_SOURCE_SYMLINK", f"{name}: {path}")
        path = path.resolve()
        if not path.is_dir():
            raise SourceBindingError(
                "G18_SOURCE_ENV_INVALID", f"{name} is not a directory: {path}"
            )
        explicit.append((name, path))
    if explicit:
        first_name, first_path = explicit[0]
        for other_name, other_path in explicit[1:]:
            if other_path != first_path:
                raise SourceBindingError(
                    "G18_SOURCE_ENV_CONFLICT",
                    f"{first_name}={first_path} != {other_name}={other_path}",
                )
        return first_path

    for candidate in _candidates(return_root, repo_root, common):
        if candidate.is_symlink():
            raise SourceBindingError("G18_SOURCE_SYMLINK", str(candidate))
        if candidate.is_dir():
            return candidate.resolve()
    raise SourceBindingError(
        "G18_SOURCE_UNRESOLVED",
        "set S52_G18_SOURCE (or S51_G18_SOURCE) to the accepted G18 checkout",
    )


def _check_relative(relpath: str) -> tuple[str, ...]:
    path = PurePosixPath(relpath)
    parts = path.parts
    if not parts or path.is_absolute() or ".." in parts:
        raise SourceBindingError("SOURCE_PATH_INVALID", relpath)
    return parts


def _check_no_symlinks(root: Path, relpath: str) -> Path:
    current = root
    for part in _check_relative(relpath):
        current = current / part
        if current.is_symlink():
            raise SourceBindingError("SOURCE_PATH_SYMLINK", str(current))
    return current


def verify_expected(root: str | Path, expected: Mapping[str, str]) -> None:
    """Verify named files by SHA-256, rejecting traversal and symlink paths."""
    root_path = Path(root)
    if root_path.is_symlink():
        raise SourceBindingError("SOURCE_ROOT_SYMLINK", str(root_path))
    root_path = root_path.resolve()
    if not root_path.is_dir():
        raise SourceBindingError("SOURCE_ROOT_MISSING", str(root_path))
    for relpath, digest in expected.items():
        path = _check_no_symlinks(root_path, relpath)
        if not path.is_file():
            raise SourceBindingError("SOURCE_FILE_MISSING", str(path))
        actual = sha256_file(path)
        if actual != digest:
            raise SourceBindingError(
                "SOURCE_HASH_MISMATCH", f"{path}: {actual} != {digest}"
            )


def verify_g18(root: str | Path) -> None:
    verify_expected(root, G18_EXPECTED)


def source_roots(
    return_root: str | Path | None = None,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    """Resolve the bounded nonstdlib roots without importing their packages."""
    if return_root is None:
        return_root = Path(__file__).resolve().parents[1]
    return_root = Path(return_root).resolve()
    repo = Path(repo_root).resolve() if repo_root is not None else return_root.parents[1]
    common = _git_common_root(return_root) or repo
    join_e = _resolve_join_e(repo, common)
    r30a = _resolve_r30a(join_e)
    g18 = resolve_g18(return_root, repo)
    manifest = repo / MANIFEST_RELATIVE
    allowed = _allowed_roots(repo, common, join_e)
    return {
        "repo": str(repo),
        "common": str(common),
        "join_e": str(join_e),
        "r30a": str(r30a),
        "g18": str(g18),
        "allowed_roots": [str(path) for path in allowed],
        "manifest": str(manifest),
    }


def _normalised_roots(roots: Mapping[str, Any] | None) -> dict[str, Any]:
    if roots is None:
        return source_roots()
    value = dict(roots)
    repo_raw = value.get("repo")
    if not repo_raw:
        for key in ("s52_return", "s51_return", "s49_return", "s48_return"):
            if value.get(key):
                repo_raw = str(Path(value[key]).parents[1])
                break
    if not repo_raw:
        return source_roots()
    repo = Path(repo_raw).resolve()
    common_raw = value.get("common")
    common = Path(common_raw).resolve() if common_raw else (
        _git_common_root(repo) or repo
    )
    join_e_raw = value.get("join_e") or value.get("join_e_return")
    join_e = Path(join_e_raw).resolve() if join_e_raw else _resolve_join_e(repo, common)
    r30a_raw = value.get("r30a") or value.get("r30a_return")
    r30a = Path(r30a_raw).resolve() if r30a_raw else _resolve_r30a(join_e)
    g18_raw = value.get("g18") or value.get("g18_source")
    g18 = Path(g18_raw).resolve() if g18_raw else resolve_g18(repo, repo)
    allowed_raw = value.get("allowed_roots")
    if allowed_raw:
        allowed = [Path(item).resolve() for item in allowed_raw]
    else:
        allowed = _allowed_roots(repo, common, join_e)
    manifest = Path(value.get("manifest") or repo / MANIFEST_RELATIVE).resolve()
    return {
        "repo": str(repo),
        "common": str(common),
        "join_e": str(join_e),
        "r30a": str(r30a),
        "g18": str(g18),
        "allowed_roots": [str(path) for path in allowed],
        "manifest": str(manifest),
    }


def _assert_allowed(root: Path, allowed: list[Path], label: str) -> None:
    if root.is_symlink():
        raise SourceBindingError("SOURCE_ROOT_SYMLINK", f"{label}: {root}")
    resolved = root.resolve()
    if not resolved.is_dir():
        raise SourceBindingError("SOURCE_ROOT_MISSING", f"{label}: {resolved}")
    if not any(resolved == parent or resolved.is_relative_to(parent) for parent in allowed):
        raise SourceBindingError(
            "SOURCE_ROOT_OUTSIDE_ALLOWED", f"{label}: {resolved}"
        )


def _check_import_cache(
    roots: Mapping[str, str],
    expected: Mapping[str, str],
    sources: list[Any],
) -> None:
    prefix_root = {
        "s48": "repo",
        "s49": "repo",
        "s51": "repo",
        "s52": "repo",
        "lab_sgi1": "g18",
        "r30a": "r30a",
    }
    listed = {
        (entry.get("root"), entry.get("path"))
        for entry in sources
        if isinstance(entry, Mapping)
    }
    for name, module in list(sys.modules.items()):
        prefix = name.split(".", 1)[0]
        if prefix not in _MANAGED_PREFIXES:
            continue
        filename = getattr(module, "__file__", None)
        if not filename:
            continue
        path = Path(filename).resolve()
        label = prefix_root[prefix]
        root = Path(expected[label]).resolve()
        if not path.is_relative_to(root):
            raise SourceBindingError(
                "SOURCE_IMPORT_CACHE_FOREIGN", f"{name}: {path}"
            )
        relpath = str(path.relative_to(root))
        if (label, relpath) not in listed:
            raise SourceBindingError(
                "SOURCE_IMPORT_CACHE_UNLISTED", f"{name}: {path}"
            )


def _load_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SourceBindingError("SOURCE_MANIFEST_MISSING", str(path))
    try:
        value = json.loads(path.read_text(encoding="utf8"))
    except (OSError, ValueError) as exc:
        raise SourceBindingError("SOURCE_MANIFEST_INVALID", str(exc)) from exc
    if not isinstance(value, dict) or value.get("schema") != "SOROK_F0_R2_SOURCE_MANIFEST@1":
        raise SourceBindingError("SOURCE_MANIFEST_INVALID", "schema")
    if not isinstance(value.get("roots"), dict) or not isinstance(value.get("sources"), list):
        raise SourceBindingError("SOURCE_MANIFEST_INVALID", "roots/sources")
    return value


def _validate_provenance(manifest: Mapping[str, Any]) -> None:
    roots = manifest.get("roots")
    if not isinstance(roots, Mapping):
        raise SourceBindingError("SOURCE_PROVENANCE_INVALID", "roots")
    for label, expected in ROOT_PROVENANCE.items():
        actual = roots.get(label)
        if not isinstance(actual, Mapping):
            raise SourceBindingError("SOURCE_PROVENANCE_INVALID", label)
        for key in _ROOT_KEYS:
            if actual.get(key) != expected[key]:
                raise SourceBindingError(
                    "SOURCE_PROVENANCE_INVALID", f"{label}.{key}"
                )


def verify_sources(
    roots: Mapping[str, Any] | None = None,
    *,
    manifest_path: str | Path | None = None,
    check_cache: bool = True,
) -> dict[str, Any]:
    """Verify the full bounded closure before any managed package import."""
    resolved = _normalised_roots(roots)
    manifest_file = Path(manifest_path).resolve() if manifest_path else Path(resolved["manifest"])
    manifest = _load_manifest(manifest_file)
    _validate_provenance(manifest)
    allowed = [Path(path) for path in resolved["allowed_roots"]]
    root_paths = {
        label: Path(resolved[label]).resolve() for label in ("repo", "g18", "r30a")
    }
    for label, root in root_paths.items():
        _assert_allowed(root, allowed, label)
    if check_cache:
        _check_import_cache(resolved, root_paths, manifest["sources"])
    seen: set[str] = set()
    count = 0
    for entry in manifest["sources"]:
        if not isinstance(entry, Mapping):
            raise SourceBindingError("SOURCE_MANIFEST_INVALID", "source entry")
        label = entry.get("root")
        relpath = entry.get("path")
        digest = entry.get("sha256")
        if label not in root_paths or not isinstance(relpath, str) or not isinstance(digest, str):
            raise SourceBindingError("SOURCE_MANIFEST_INVALID", str(entry))
        key = f"{label}:{relpath}"
        if key in seen:
            raise SourceBindingError("SOURCE_MANIFEST_INVALID", "duplicate " + key)
        seen.add(key)
        verify_expected(root_paths[label], {relpath: digest})
        count += 1
    return {
        "schema": "SOROK_F0_R2_SOURCE_VERIFICATION@1",
        "manifest": str(manifest_file),
        "verified": count,
        "roots": {key: str(value) for key, value in root_paths.items()},
    }


__all__ = [
    "G18_EXPECTED",
    "G18_RELATIVE",
    "MANIFEST_RELATIVE",
    "ROOT_PROVENANCE",
    "SourceBindingError",
    "resolve_g18",
    "sha256_file",
    "source_roots",
    "verify_expected",
    "verify_g18",
    "verify_sources",
]
