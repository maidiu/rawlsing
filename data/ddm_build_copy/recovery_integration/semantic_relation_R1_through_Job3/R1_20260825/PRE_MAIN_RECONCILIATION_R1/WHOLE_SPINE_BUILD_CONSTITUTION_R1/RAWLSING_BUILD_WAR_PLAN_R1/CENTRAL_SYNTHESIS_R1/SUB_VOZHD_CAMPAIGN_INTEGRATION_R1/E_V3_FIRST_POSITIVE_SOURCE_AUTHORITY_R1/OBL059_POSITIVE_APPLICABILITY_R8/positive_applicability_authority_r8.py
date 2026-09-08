"""OBL059 R8 bounded repair: safe nested Mapping snapshot boundary.

R8 preserves frozen R7/R6 applicability semantics. It changes only nested
Mapping nodes that are actually consumed by OBL059 scope/evidence evaluation.

The outer carrier is handled exactly as in R7. After an exact outer dict exists,
R8 snapshots only ``opportunity``, top-level ``evidence``, and the three
evidence components read by the frozen evaluator. A successful snapshot is an
exact built-in dict and the original custom Mapping is never consulted again.
If one of those snapshots raises, that nested node is replaced by ``None`` and
the frozen evaluator produces its existing field-specific negative reason.

No project-current state or runtime effect is created.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

_R7_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R7"
    / "positive_applicability_authority_r7.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r7_authority_for_r8", _R7_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R7 authority: {_R7_PATH}")
_r7 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r7)

AUTHORITY_ID = _r7.AUTHORITY_ID
RECEIPT_VERSION = _r7.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r7.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r7.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r7.ADP007_OWNER
ADP008_OWNER = _r7.ADP008_OWNER
ADP010_CONSUMER = _r7.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r7.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r7.POSITIVE_DECISION
NEGATIVE_DECISION = _r7.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r7.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r7._REQUIRED_BINDINGS)

R8_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R8"
_EVIDENCE_COMPONENT_KEYS = (
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)


def _snapshot_mapping_once(value: ABCMapping) -> dict[str, Any] | None:
    """Take one bounded snapshot; None means caller traversal did not complete."""
    try:
        return dict(value)
    except Exception:
        return None


def _snapshot_if_custom_mapping(value: Any) -> Tuple[Any, bool]:
    """Return (safe_value, changed) without direct semantic field access."""
    if type(value) is dict:
        return value, False
    if isinstance(value, ABCMapping):
        return _snapshot_mapping_once(value), True
    return value, False


def _prepare_consumed_nested_mappings(packet: dict[str, Any]) -> dict[str, Any]:
    """Snapshot only nested Mapping nodes the frozen evaluator actually reads.

    Exact-dict packets with no custom nested Mapping nodes are returned
    unchanged. This preserves the ordinary R7/R6 path exactly.
    """
    working = packet
    changed = False

    opportunity = dict.get(packet, "opportunity")
    safe_opportunity, opportunity_changed = _snapshot_if_custom_mapping(opportunity)
    if opportunity_changed:
        working = dict.copy(packet)
        dict.__setitem__(working, "opportunity", safe_opportunity)
        changed = True

    evidence_source = dict.get(working, "evidence")
    safe_evidence, evidence_changed = _snapshot_if_custom_mapping(evidence_source)
    if evidence_changed:
        if not changed:
            working = dict.copy(packet)
            changed = True
        dict.__setitem__(working, "evidence", safe_evidence)

    if type(safe_evidence) is dict:
        evidence_working = safe_evidence
        evidence_component_changed = False

        for key in _EVIDENCE_COMPONENT_KEYS:
            component = dict.get(evidence_working, key)
            safe_component, component_changed = _snapshot_if_custom_mapping(component)
            if component_changed:
                if not evidence_component_changed:
                    evidence_working = dict.copy(evidence_working)
                    evidence_component_changed = True
                dict.__setitem__(evidence_working, key, safe_component)

        if evidence_component_changed:
            if not changed:
                working = dict.copy(packet)
                changed = True
            dict.__setitem__(working, "evidence", evidence_working)

    return working


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate R7 unchanged except at the consumed nested-Mapping boundary."""
    if type(packet) is dict:
        prepared = _prepare_consumed_nested_mappings(packet)
        return _r7.evaluate_direct_positive_applicability(prepared)

    if not isinstance(packet, ABCMapping):
        return _r7.evaluate_direct_positive_applicability(packet)

    outer_snapshot = _r7._snapshot_outer_mapping(packet)
    if outer_snapshot is None:
        return _r7._existing_packet_malformed_receipt()

    prepared = _prepare_consumed_nested_mappings(outer_snapshot)
    return _r7.evaluate_direct_positive_applicability(prepared)
