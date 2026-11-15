"""Import bootstrap for the BP2 joined producer.

Puts the exact staged upstream closures on ``sys.path`` in a fixed order and
verifies that every staged file still matches its pinned SHA-256. The layout is:

    vendor/bp3      BP3 keyed exclusive writer, OUT9 bridge, C9 event ingress
    vendor/bp1      BP1 two-actor historical producer (package ``bp1``)
    vendor/g18      minimal ``lab_sgi1`` subset imported by BP1
    vendor/c9r      C9R repaired candidate package (package ``candidate``)
    vendor/native   C9R-pinned ``rawlsing_next`` zero-positive guard

No upstream file is patched. ``verify_sources`` reads the manifest and hashes
what is actually on disk, so a silent divergence from the origin is detectable.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPO = next(p for p in RETURN.parents if (p / ".git").exists())
# Reuse the warm R31J/BP2 vendored closure rather than copying immutable bytes.
DEFAULT_VENDOR = Path(
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-r31j/"
    "WORKER_RETURNS/SOROK-20261021-R31J-GM01-PREC9-SOURCE-PERSON-R1/"
    "candidate/vendor/bp2/vendor")
VENDOR = Path(os.environ.get("M35_BP2_VENDOR", str(DEFAULT_VENDOR))).resolve()
MANIFEST = VENDOR / "source_manifest.json"

# Order matters: the staged native guard is preferred over any ambient copy.
PATH_ENTRIES = (
    VENDOR / "native",
    VENDOR / "c9r",
    VENDOR / "bp1",
    VENDOR / "g18",
    VENDOR / "bp3",
)


class SourceClosureDrift(RuntimeError):
    pass


def install() -> None:
    for entry in reversed(PATH_ENTRIES):
        text = str(entry)
        if text in sys.path:
            sys.path.remove(text)
        sys.path.insert(0, text)
    if str(RETURN) not in sys.path:
        sys.path.insert(0, str(RETURN))


def verify_sources() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
    problems: list[str] = []
    for row in manifest["files"]:
        target = VENDOR / row["staged_path"]
        if not target.exists():
            problems.append("MISSING:" + row["staged_path"])
            continue
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            problems.append("SHA256_DRIFT:" + row["staged_path"])
    if problems:
        raise SourceClosureDrift(";".join(problems))
    return manifest


def module_origin(module) -> dict:
    """Describe where an imported upstream module actually came from."""
    path = Path(getattr(module, "__file__", "")).resolve()
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
    try:
        relative = str(path.relative_to(VENDOR))
    except ValueError:
        relative = str(path)
    return {"module": getattr(module, "__name__", ""), "path": str(path),
            "vendor_relative": relative, "sha256": digest}


__all__ = [
    "MANIFEST", "PATH_ENTRIES", "REPO", "RETURN", "VENDOR", "SourceClosureDrift",
    "install", "module_origin", "verify_sources",
]
