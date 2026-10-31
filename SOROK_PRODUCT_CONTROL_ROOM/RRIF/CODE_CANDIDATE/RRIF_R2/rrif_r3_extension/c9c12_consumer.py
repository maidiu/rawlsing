"""RRIF-R3 C9C12 reader consumption over an existing same-root C12 store.

The recovered C9C12-R2 reader is executed against the RRIF-R2 product's C12
store. The C12 cold read is a real consumer; the C9 actor snapshot remains
source-missing because the R2 product has no C9 actor SQLite.
"""
from __future__ import annotations

from pathlib import Path
import sqlite3
import sys
from typing import Any

R2 = Path(__file__).resolve().parents[1]
BP4 = R2 / "vendor" / "j" / "candidate" / "vendor" / "bp4"
for path in (str(BP4), str(R2)):
    if path not in sys.path:
        sys.path.insert(0, path)

import c9c12_reader


def _c12_path(root: str | Path) -> Path:
    root = Path(root)
    candidate = root / "c12.sqlite"
    if candidate.is_file():
        return candidate
    product = root / "product" / "c12.sqlite"
    if product.is_file():
        return product
    raise FileNotFoundError("C12_SQLITE_NOT_FOUND:" + str(root))


def read_r2_c12(root: str | Path, *, branch_id: str = "root") -> dict[str, Any]:
    """Actual C9C12-R2 C12 cold-read consumer over the existing R2 root."""
    result = c9c12_reader.guarded_c12_cold_read(
        _c12_path(root), branch_id=branch_id)
    result["consumer"] = "C9C12_R2_GUARDED_C12_COLD_READ_ON_RRIF_R2"
    result["r2_root"] = str(Path(root))
    return result


def read_r2_c9_snapshot(root: str | Path, *, actor_id: str = "TEST_ONLY_BP1_R26V_ACTOR_A") -> dict[str, Any]:
    """C9 actor snapshot is unavailable in the R2 C12-only product."""
    try:
        result = c9c12_reader.read_actor_snapshot(
            _c12_path(root), actor_id=actor_id, branch_id="root")
        result["consumer"] = "C9C12_R2_ACTOR_SNAPSHOT"
        return result
    except (sqlite3.Error, c9c12_reader.C9C12Refusal) as exc:
        return {
            "status": "C9_SOURCE_MISSING",
            "actor_id": actor_id,
            "reason": type(exc).__name__ + ":" + str(exc),
            "consumer": "C9C12_R2_ACTOR_SNAPSHOT",
            "sourcefree": True,
        }


__all__ = ["read_r2_c12", "read_r2_c9_snapshot"]
