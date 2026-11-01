"""Explicit J/E import closure and immutable-source audit.

The join deliberately loads the J closure first, then the E closure.  Several
vendored packages use the same module names (``bp4``, ``bp2p4``, ``r29p``), so a
green test is not proof that the intended bytes were imported.  This module
records the actual ``__file__`` of every load-bearing module and verifies the
vendored files against the candidate's immutable source manifest.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = next(path for path in RETURN.parents if (path / ".git").exists())
J_ROOT = (RETURN / "vendor" / "j").resolve()
E_ROOT = (RETURN / "vendor" / "e").resolve()
LIVE_ROOT = (REPO / "rawlsing_next").resolve()
SOURCE_MANIFEST = RETURN / "SOURCE_MANIFEST.json"

# Module -> the only lawful closure root for that module in this join.
EXPECTED = {
    "r31j.build": "J",
    "r31j.product": "J",
    "r31j.pre_c9": "J",
    "r31j.scenarios": "J",
    "historical_actor_producer": "J",
    "bp2p4": "J",
    "bp2p4.bootstrap": "J",
    "bp2p4.product": "J",
    "bp2_joined": "J",
    "bp2_joined.producer": "J",
    "bp2_joined.binding": "J",
    "bp2_joined.ports": "J",
    "bp4": "J",
    "bp4.product": "J",
    "bp4.world": "J",
    "bp4.perception": "J",
    "bp4.store": "J",
    "r29p.product": "J",
    "r26e.c12_integrity": "J",
    "r30a.bootstrap": "E",
    "r30a.first_session": "E",
    "r30a.phenomenal": "E",
    "r31e.bootstrap": "E",
    "r31e.session": "E",
    "r31e.expression": "E",
    "rawlsing_next.m6_actor_safe_expression": "LIVE",
}

ROOT_BY_CLASS = {"J": J_ROOT, "E": E_ROOT, "LIVE": LIVE_ROOT}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def source_manifest_sha256() -> str:
    """Return the immutable candidate manifest digest used by this join."""
    return _sha256(SOURCE_MANIFEST)


def audit_manifest() -> dict:
    """Verify every vendored file against the candidate's recorded Git blob."""
    document = json.loads(SOURCE_MANIFEST.read_text(encoding="utf8"))
    rows = []
    problems = []
    for row in document["files"]:
        path = (RETURN / row["path"]).resolve()
        if not path.is_file():
            problems.append("MISSING:" + row["path"])
            continue
        actual = _blob_sha1(path)
        if actual != row["git_blob"]:
            problems.append("BLOB_MISMATCH:" + row["path"])
        rows.append({
            "path": row["path"],
            "source_commit": row["source_commit"],
            "expected_blob": row["git_blob"],
            "actual_blob": actual,
            "ok": actual == row["git_blob"],
        })
    return {
        "schema": "SOROK_JOIN_E_SOURCE_AUDIT@1",
        "manifest": str(SOURCE_MANIFEST),
        "manifest_sha256": source_manifest_sha256(),
        "files": len(rows),
        "problems": problems,
        "ok": not problems,
        "rows": rows,
    }


def _path_class(path: Path) -> str:
    for name, root in ROOT_BY_CLASS.items():
        if path.is_relative_to(root):
            return name
    return "UNEXPECTED"


def audit_loaded() -> dict:
    """Verify the actual imported modules, not merely sys.path entries."""
    rows = []
    problems = []
    for name, expected_class in EXPECTED.items():
        module = sys.modules.get(name)
        if module is None:
            problems.append("NOT_IMPORTED:" + name)
            continue
        raw = getattr(module, "__file__", "")
        if not raw:
            problems.append("NO_FILE:" + name)
            continue
        path = Path(raw).resolve()
        actual_class = _path_class(path)
        if actual_class != expected_class:
            problems.append(
                f"WRONG_CLOSURE:{name}:expected={expected_class}:actual={actual_class}:{path}")
        if not path.is_file():
            problems.append("FILE_MISSING:" + name)
            continue
        rows.append({
            "module": name,
            "expected_closure": expected_class,
            "actual_closure": actual_class,
            "path": str(path),
            "sha256": _sha256(path),
            "ok": actual_class == expected_class,
        })
    return {
        "schema": "SOROK_JOIN_E_LOADED_CLOSURE@1",
        "problems": problems,
        "ok": not problems,
        "rows": rows,
    }


def require_loaded() -> dict:
    """Return the closure audit or raise a typed refusal."""
    result = audit_loaded()
    if not result["ok"]:
        raise RuntimeError("JOIN_E_IMPORT_CLOSURE_INVALID: " + "; ".join(result["problems"]))
    return result
