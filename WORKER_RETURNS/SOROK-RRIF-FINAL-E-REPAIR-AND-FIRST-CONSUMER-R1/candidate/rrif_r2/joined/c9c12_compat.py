"""Exact typed C9/C12/R2 compatibility boundary.

The R3 C12 reader genuinely consumes the R2 root, but the C9 actor snapshot is
absent from the R2 product. CP-A5's sourcefree root also uses a different BP2
origin actor than R2. Neither condition is repaired by relabeling, hash
rewriting or a synthetic actor row.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "rrif_r3_extension"
if str(EXT) not in sys.path:
    sys.path.insert(0, str(EXT))

from .imports import install
install()

from c9c12_consumer import read_r2_c12, read_r2_c9_snapshot  # noqa: E402

INCOMPATIBLE = (
    "INCOMPATIBLE_WITHOUT_OWNER_MIGRATION__ROOT_COLD_READ_ONLY_UNDER_OWNER_ANCHOR_HOLD__FORK_LEGACY_ROOT_UNVERIFIED"
)
CP_A5_ORIGIN_MISMATCH = "BP2_ORIGIN_INVARIANT_MISMATCH"


def read_c9c12_compatibility(product_root: str | Path) -> dict[str, Any]:
    c12 = read_r2_c12(product_root, branch_id="root")
    c9 = read_r2_c9_snapshot(product_root)
    legacy = read_r2_c12(product_root, branch_id="first_session")
    incompatible = (
        c12.get("ok") is True
        and c9.get("status") == "C9_SOURCE_MISSING"
        and legacy.get("fork_status") == "LEGACY_HELD"
    )
    return {
        "schema": "RRIF_E_C9C12_COMPATIBILITY@1",
        "status": INCOMPATIBLE if incompatible else "UNEXPECTED_COMPATIBILITY",
        "c12_root": c12,
        "c9_actor": c9,
        "legacy_first_session": legacy,
        "cp_a5_same_root": {
            "status": "INCOMPATIBLE_EXACT_SOURCECUT",
            "code": CP_A5_ORIGIN_MISMATCH,
            "expected_actor": "TEST_ONLY_BP1_ACTOR_A",
            "actual_actor": "TEST_ONLY_BP1_R26V_ACTOR_A",
        },
        "owner_migration_required": True,
        "external_owner_anchor": "OWNER_ANCHOR_REQUIRED",
        "native_person": False,
        "fabricated_actor": False,
    }


__all__ = ["CP_A5_ORIGIN_MISMATCH", "INCOMPATIBLE", "read_c9c12_compatibility"]
