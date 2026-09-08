"""OBL059 R7 bounded repair: safe outer Mapping snapshot boundary.

R7 preserves frozen R6 semantics for exact-dict packets and for well-behaved
Mapping carriers.  The only change is the outer non-exact-dict Mapping boundary.

Frozen R1 authority accepts Mapping carriers, so R7 does not narrow that carrier
law.  Instead, a non-exact Mapping is snapshotted exactly once inside a bounded
traversal boundary.  If that traversal raises an ordinary Exception, R7 returns
the existing deterministic PACKET_MALFORMED negative receipt without consulting
the caller object again.  A successful snapshot is an exact dict and is then
evaluated by frozen R6 unchanged.

No project-current state or runtime effect is created.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping

_R6_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R6"
    / "positive_applicability_authority_r6.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r6_authority_for_r7", _R6_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R6 authority: {_R6_PATH}")
_r6 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r6)

AUTHORITY_ID = _r6.AUTHORITY_ID
RECEIPT_VERSION = _r6.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r6.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r6.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r6.ADP007_OWNER
ADP008_OWNER = _r6.ADP008_OWNER
ADP010_CONSUMER = _r6.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r6.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r6.POSITIVE_DECISION
NEGATIVE_DECISION = _r6.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r6.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r6._REQUIRED_BINDINGS)

R7_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R7"


def _existing_packet_malformed_receipt() -> Dict[str, Any]:
    """Return the exact frozen R1 malformed-carrier receipt from safe input."""
    return _r6._r5._r4._r3._r2._r1.evaluate_direct_positive_applicability(None)


def _snapshot_outer_mapping(packet: ABCMapping) -> dict[str, Any] | None:
    """Snapshot one authorized Mapping carrier; None means traversal failed.

    The exception boundary is deliberately limited to caller-controlled carrier
    traversal.  Evaluation of the resulting exact dict occurs outside this
    boundary so unrelated implementation errors remain visible.
    """
    try:
        return dict(packet)
    except Exception:
        return None


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate R6 unchanged except at the outer custom-Mapping boundary."""
    if type(packet) is dict:
        return _r6.evaluate_direct_positive_applicability(packet)

    if not isinstance(packet, ABCMapping):
        return _r6.evaluate_direct_positive_applicability(packet)

    snapshot = _snapshot_outer_mapping(packet)
    if snapshot is None:
        return _existing_packet_malformed_receipt()

    return _r6.evaluate_direct_positive_applicability(snapshot)
