"""C12 custody boundary: self-hash integrity versus guarded row identity.

``QualifiedC12Store`` verifies content preimages but intentionally does not
cover raw SQLite column substitutions or perception identity. The R3
``GuardedC12Store`` checks row columns, origin branch, perception membership and
fork prefixes. Neither is an external owner anchor. The returned classification
keeps that distinction explicit.
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

from c12_guard import GuardedC12Store, verify_store  # noqa: E402
from r26e.c12_integrity import QualifiedC12Store  # noqa: E402

OWNER_ANCHOR = "OWNER_ANCHOR_REQUIRED"


def coordinated_guard_report(db_path: str | Path, *, branch_id: str = "root") -> dict[str, Any]:
    """Compare self-hash-only and guarded C12 identity on the same store."""
    path = Path(db_path)
    qualified_store = QualifiedC12Store(path)
    try:
        qualified = qualified_store.verify(branch_id)
    finally:
        qualified_store.close()
    guarded_store = GuardedC12Store(path)
    try:
        guarded = verify_store(guarded_store, branch_id)
    finally:
        guarded_store.close()
    if qualified.get("ok") and guarded.get("ok"):
        classification = "BOTH_GREEN__SELF_HASH_PLUS_GUARDED_ROWS__NO_OWNER_ANCHOR"
    elif qualified.get("ok") and not guarded.get("ok"):
        classification = "SELF_HASH_ONLY__TRUST_CUSTODY_HOLD"
    elif not qualified.get("ok") and not guarded.get("ok"):
        classification = "BOTH_RED_OR_CONTENT_TAMPERED"
    else:
        classification = "GUARDED_GREEN_QUALIFIED_RED__INVESTIGATE"
    return {
        "schema": "RRIF_E_C12_CUSTODY_REPORT@1",
        "classification": classification,
        "qualified": qualified,
        "guarded": guarded,
        "external_owner_anchor": OWNER_ANCHOR,
        "authenticity_claimed": False,
        "security_boundary": False,
        "trust_custody_hold": classification == "SELF_HASH_ONLY__TRUST_CUSTODY_HOLD",
    }


__all__ = ["OWNER_ANCHOR", "coordinated_guard_report"]
