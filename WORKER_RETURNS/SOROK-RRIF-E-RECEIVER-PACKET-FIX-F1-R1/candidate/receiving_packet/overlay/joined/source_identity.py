"""Honest candidate-preimage verification with explicit self-exclusion.

A file cannot contain its own SHA-256/size without an impossible fixed point.
The repaired preimage therefore excludes exactly itself, states that exclusion
machine-readably, and pins the immutable vendor manifest and a source commit.
Every other candidate file is content-addressed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PREIMAGE = "RRIF_R2_CANDIDATE_SOURCE_PREIMAGE.json"
SOURCE_MANIFEST = "SOURCE_MANIFEST.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_candidate_preimage(root: str | Path) -> dict[str, Any]:
    root = Path(root)
    preimage_path = root / PREIMAGE
    document = json.loads(preimage_path.read_text(encoding="utf8"))
    errors: list[str] = []
    exclusion = document.get("self_exclusion") or {}
    if exclusion.get("path") != PREIMAGE:
        errors.append("SELF_EXCLUSION_PATH_MISMATCH")
    if not exclusion.get("rationale"):
        errors.append("SELF_EXCLUSION_RATIONALE_MISSING")
    if exclusion.get("content_addressed") is not False:
        errors.append("SELF_EXCLUSION_NOT_DECLARED_NON_CONTENT_ADDRESSED")
    listed = {row["path"] for row in document.get("files", [])}
    actual = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    if PREIMAGE in listed:
        errors.append("SELF_ENTRY_FORBIDDEN")
    unlisted = sorted(actual - listed - {PREIMAGE})
    missing = sorted(listed - actual)
    if unlisted:
        errors.append("UNLISTED_FILES:" + ",".join(unlisted))
    if missing:
        errors.append("MISSING_FILES:" + ",".join(missing))
    for row in document.get("files", []):
        path = root / row["path"]
        if not path.is_file():
            errors.append("MISSING:" + row["path"])
            continue
        if path.stat().st_size != row.get("size"):
            errors.append("SIZE_MISMATCH:" + row["path"])
        if _sha256(path) != row.get("sha256"):
            errors.append("SHA256_MISMATCH:" + row["path"])
    manifest_path = root / SOURCE_MANIFEST
    manifest_sha = _sha256(manifest_path) if manifest_path.is_file() else ""
    if document.get("source_manifest_sha256") != manifest_sha:
        errors.append("SOURCE_MANIFEST_SHA256_MISMATCH")
    counts = document.get("counts") or {}
    if counts.get("files") != len(document.get("files", [])):
        errors.append("COUNT_MISMATCH")
    if counts.get("vendor_manifest_files") != 444:
        errors.append("VENDOR_MANIFEST_COUNT_MISMATCH")
    if not document.get("source_candidate_commit"):
        errors.append("SOURCE_CANDIDATE_COMMIT_MISSING")
    return {
        "schema": "RRIF_E_CANDIDATE_PREIMAGE_AUDIT@1",
        "ok": not errors,
        "errors": errors,
        "files": len(document.get("files", [])),
        "self_excluded": PREIMAGE,
        "source_manifest_sha256": manifest_sha,
        "self_exclusion": exclusion,
        "listed_files": len(listed),
        "actual_files": len(actual),
        "unlisted_files": unlisted,
        "external_pin": {
            "source_candidate_commit": document.get("source_candidate_commit"),
            "dispatch_commit": document.get("dispatch_commit"),
        },
    }


__all__ = ["PREIMAGE", "SOURCE_MANIFEST", "audit_candidate_preimage"]
