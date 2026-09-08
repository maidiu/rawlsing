"""OBL059 R9 bounded repair: coherent nested snapshots and safe negative receipts.

R9 preserves frozen R8/R7/R6 applicability semantics for ordinary exact-dict
inputs and stable Mapping carriers. It changes only two review-proven boundaries:

1. all consumed nested nodes are captured from one outer/evidence frame before
   custom nested traversal can rewrite a later parent binding; aliased custom
   carriers are snapshotted at most once per evaluation;
2. when the prepared packet is semantically negative but its proof material is
   not stably JSON-encodable across supported integer-conversion settings, the
   negative receipt is constructed through the inherited R6 stable projection.

No project-current state or runtime effect is created.
"""

from __future__ import annotations

import hashlib
import importlib.util
from copy import deepcopy
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

_R8_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R8"
    / "positive_applicability_authority_r8.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r8_authority_for_r9", _R8_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R8 authority: {_R8_PATH}")
_r8 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r8)

_r7 = _r8._r7
_r6 = _r7._r6
_r1 = _r6._r5._r4._r3._r2._r1

AUTHORITY_ID = _r8.AUTHORITY_ID
RECEIPT_VERSION = _r8.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r8.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r8.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r8.ADP007_OWNER
ADP008_OWNER = _r8.ADP008_OWNER
ADP010_CONSUMER = _r8.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r8.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r8.POSITIVE_DECISION
NEGATIVE_DECISION = _r8.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r8.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r8._REQUIRED_BINDINGS)
_EVIDENCE_COMPONENT_KEYS = tuple(_r8._EVIDENCE_COMPONENT_KEYS)

R9_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R9"


def _snapshot_mapping_once(value: ABCMapping) -> dict[str, Any] | None:
    """Take exactly one bounded Mapping snapshot; None means traversal failed."""
    try:
        return dict(value)
    except Exception:
        return None


def _snapshot_custom_memoized(
    value: Any,
    memo: dict[int, dict[str, Any] | None],
) -> Tuple[Any, bool]:
    """Snapshot an admitted custom Mapping at most once in this evaluation."""
    if type(value) is dict:
        return dict.copy(value), False
    if not isinstance(value, ABCMapping):
        return value, False

    marker = id(value)
    if marker not in memo:
        memo[marker] = _snapshot_mapping_once(value)
    return memo[marker], True


def _prepare_coherent_consumed_view(packet: dict[str, Any]) -> dict[str, Any]:
    """Build one exact-dict working view without rereading mutable parent slots.

    Phase 1 captures the outer packet and all exact-dict parent bindings before
    custom nested traversal. Phase 2 snapshots custom Mapping carriers only from
    those captured references. Parent slots are never reread after traversal
    begins, so one carrier cannot replace a later consumed node and have the new
    value admitted in the same evaluation.

    Aliased custom carriers reuse one memoized snapshot.
    """
    outer_frame = dict.copy(packet)

    opportunity_source = dict.get(outer_frame, "opportunity")
    evidence_source = dict.get(outer_frame, "evidence")

    opportunity_exact = (
        dict.copy(opportunity_source)
        if type(opportunity_source) is dict
        else None
    )
    evidence_exact = (
        dict.copy(evidence_source)
        if type(evidence_source) is dict
        else None
    )

    memo: dict[int, dict[str, Any] | None] = {}
    evidence_custom = (
        type(evidence_source) is not dict
        and isinstance(evidence_source, ABCMapping)
    )

    if evidence_custom:
        evidence_exact = _snapshot_mapping_once(evidence_source)
        memo[id(evidence_source)] = evidence_exact

    component_sources: dict[str, Any] = {}
    component_exact: dict[str, dict[str, Any]] = {}
    if type(evidence_exact) is dict:
        for key in _EVIDENCE_COMPONENT_KEYS:
            source = dict.get(evidence_exact, key)
            component_sources[key] = source
            if type(source) is dict:
                component_exact[key] = dict.copy(source)

    if opportunity_exact is not None:
        safe_opportunity: Any = opportunity_exact
    else:
        safe_opportunity, _ = _snapshot_custom_memoized(opportunity_source, memo)

    if type(evidence_exact) is dict:
        evidence_working = dict.copy(evidence_exact)
        for key in _EVIDENCE_COMPONENT_KEYS:
            if key in component_exact:
                safe_component: Any = component_exact[key]
            else:
                safe_component, _ = _snapshot_custom_memoized(
                    component_sources.get(key),
                    memo,
                )
            dict.__setitem__(evidence_working, key, safe_component)
        safe_evidence: Any = evidence_working
    elif evidence_custom:
        safe_evidence = None
    else:
        safe_evidence = evidence_source

    working = dict.copy(outer_frame)
    dict.__setitem__(working, "opportunity", safe_opportunity)
    dict.__setitem__(working, "evidence", safe_evidence)
    return working


def _semantic_negative_reason_and_ownership(
    packet: dict[str, Any],
) -> Tuple[str | None, list[dict[str, str]]]:
    """Run frozen semantic checks without constructing or hashing a receipt."""
    scope_error = _r1._check_exact_scope(packet)
    if scope_error:
        return scope_error, []

    evidence, evidence_error = _r1._require_evidence_mapping(packet)
    if evidence_error:
        return evidence_error, []

    proof_error, ownership = _r1._check_evidence(packet, evidence)
    if proof_error:
        return proof_error, ownership

    return None, ownership


def _stable_projected_negative_receipt(
    packet: dict[str, Any],
    reason: str,
    ownership: list[dict[str, str]],
) -> Dict[str, Any]:
    """Construct one deterministic negative receipt via frozen R6 projection."""
    projected_packet = _r6._project_total_stable(packet)
    proof = hashlib.sha256(
        _r6._canonical(projected_packet).encode("utf-8")
    ).hexdigest()
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": _r6._project_total_stable(
            dict.get(packet, "execution_scope")
        ),
        "decision": NEGATIVE_DECISION,
        "reason": reason,
        "bindings": {
            key: _r6._project_total_stable(dict.get(packet, key))
            for key in _REQUIRED_BINDINGS
        },
        "consumer_rule": ADP010_CONSUMER,
        "proof_sha256": proof,
        "evidence_ownership": deepcopy(ownership),
        "project_current_state_created": False,
        "actor_created_or_activated": False,
        "adp008_phase_transition_executed": False,
        "adp019_occurrence_admitted": False,
        "causal_use_permission_owned": False,
        "contact_witness_independence_owned": False,
        "encounter_created": False,
        "oee_realized": False,
        "obl055_executed": False,
        "current_positive_obl056_installed": False,
    }


def _evaluate_prepared(packet: dict[str, Any]) -> Dict[str, Any]:
    """Preserve inherited behavior unless a negative receipt needs projection."""
    reason, ownership = _semantic_negative_reason_and_ownership(packet)
    if (
        reason is not None
        and not _r6._structurally_json_safe_across_supported_limits(packet)
    ):
        return _stable_projected_negative_receipt(packet, reason, ownership)

    return _r7.evaluate_direct_positive_applicability(packet)


def evaluate_direct_positive_applicability(
    packet: Mapping[str, Any],
) -> Dict[str, Any]:
    """Evaluate R8 semantics with the two bounded R9 repairs."""
    if type(packet) is dict:
        prepared = _prepare_coherent_consumed_view(packet)
        return _evaluate_prepared(prepared)

    if not isinstance(packet, ABCMapping):
        return _r7.evaluate_direct_positive_applicability(packet)

    outer_snapshot = _r7._snapshot_outer_mapping(packet)
    if outer_snapshot is None:
        return _r7._existing_packet_malformed_receipt()

    prepared = _prepare_coherent_consumed_view(outer_snapshot)
    return _evaluate_prepared(prepared)
