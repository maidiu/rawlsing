"""GF1L author repair — preserve native key identity at the result storage boundary.

`compute_pair_support_signature(relation) -> dict` reads an immutable
``GenericNativePairRelation`` and COMPUTES a downstream support-signature value.
It never copies the relation's own material and never emits a constant label.

This repair is minimal and strictly additive over GF1H: native domain/row/target
category identity is compared by exact type + value, never by ``str()`` coercion,
bool/int folding, or auto-normalisation. A spoofed row or target category is
rejected with ``CONSUMER_RELATION_INTEGRITY_REJECTED`` before any total, class,
result hash or downstream value is produced.

GRAIN: SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY. UNISSUED. NOT ACCEPTED.
GENERIC_NATIVE_SEMANTICS_HOLD RETAINED. No Field Forge semantic issue, no
original source, no OC05/N11/N12/actor/V3.
"""
from __future__ import annotations

from math import isfinite
from typing import Any

from rawlsing_next._gf1_candidate.generic_native_pair_relation import (
    GENERIC_CONSUMER_ID,
    GENERIC_RESULT_FAMILY,
    GenericNativePairRelation,
    GenericNativePairError,
    semantic_hash,
)

REPAIR_VERSION = "GF1M_NONFINITE_NATIVE_CATEGORY_GUARD@1"

# The four lawful downstream separation classes.
SEPARATION_CLASSES = (
    "EXACT_PAIR_SEPARATION",
    "NO_PAIR_SEPARATION",
    "UNDETERMINED_NO_ELIGIBLE_RISK",
    "UNDETERMINED_ZERO_SUPPORT_RISK",
)

_DECISION_COMPUTED = "PAIR_SUPPORT_SIGNATURE_COMPUTED"
_DECISION_INVALID_INPUT = "CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION"
_DECISION_EMPTY = "RESPONSE_INPUTS_VALID_EMPTY"
_DECISION_IDENTITY_MISMATCH = "CONSUMER_RELATION_IDENTITY_MISMATCH"
_DECISION_PRODUCER_BLOCKED = "CONSUMER_PRODUCER_TYPED_STATE_BLOCKING"
_DECISION_INTEGRITY = "CONSUMER_RELATION_INTEGRITY_REJECTED"

_OBJECT_ID_PREFIX = "urn:rawlsing:gf1:generic-pair-relation:sha256:"


def _refusal(decision_state: str) -> dict:
    """Minimal, decision-only refusal. Carries no copied or computed science."""
    return {
        "consumer_id": GENERIC_CONSUMER_ID,
        "consumer_output_family": GENERIC_RESULT_FAMILY,
        "decision_state": decision_state,
        "separation_class": None,
        "downstream_value_produced": False,
        "generic_native_semantics_hold": "RETAINED",
        "is_population_evidence_not_actor_fact": True,
        "makes_no_causal_or_psychological_claim": True,
        "production_owner_commit": False,
    }


def _verify_identity(relation: GenericNativePairRelation) -> None:
    """Defence-in-depth: the relation's committed identity must match its bytes."""
    digest = semantic_hash(relation.semantic_projection())
    if relation.content_hash != digest:
        raise GenericNativePairError(
            "consumer relation content_hash does not match semantic projection")
    if relation.object_id != _OBJECT_ID_PREFIX + digest:
        raise GenericNativePairError(
            "consumer relation object_id does not match semantic projection")


def _exact_count(value: Any, name: str) -> int:
    if type(value) is not int or value < 0:
        raise GenericNativePairError(f"{name} must be an exact nonnegative integer")
    return value


def _same_native(a: Any, b: Any) -> bool:
    """Exact native-category identity: same Python type AND equal value.

    Deliberately does not use ``str()`` coercion, does not let ``bool`` fold into
    ``int`` (``type(False) is bool != type(0) is int``), and never auto-normalises.
    """
    return type(a) is type(b) and a == b


def _distinct_native_pair(values: list[Any]) -> bool:
    return len(values) == 2 and not _same_native(values[0], values[1])


def _require_lossless_mapping_keys(values: list[Any]) -> None:
    """Refuse domains the existing mapping/result serializer cannot preserve.

    Strict row membership alone does not stop Python dict keys such as 0 and
    False from merging. The inherited result serializer also sorts mapping
    keys and encodes them as strings. Probe that same serializer, without
    converting a category or changing the result schema. Unsupported key
    combinations must be refused before support aggregation or classification.
    """
    # The inherited semantic hash accepts Infinity/NaN. A successful hash is
    # therefore insufficient evidence that native states can be exchanged as
    # strict JSON. Refuse these categories before creating a scientific value.
    if any(isinstance(value, float) and not isfinite(value) for value in values):
        raise GenericNativePairError("nonfinite native states are not JSON representable")
    probe = {value: None for value in values}
    if len(probe) != len(values):
        raise GenericNativePairError("native states collide as Python mapping keys")
    key_identities = [semantic_hash({value: None}) for value in values]
    if len(set(key_identities)) != len(values):
        raise GenericNativePairError("native states collide in result key serialization")
    # An individually serializable key can still be incompatible with another
    # key during canonical sorting. The caller maps those errors to typed refusal.
    semantic_hash(probe)


def _decode_profile(relation: GenericNativePairRelation):
    """Check the full 2×2 conservation boundary before computing any science."""
    eligible = _exact_count(relation.eligible_joint_risk_total, "eligible_joint_risk_total")
    excluded = _exact_count(relation.excluded_ineligible_target_count,
                            "excluded_ineligible_target_count")
    profile = relation.conditional_count_profile
    if not isinstance(profile, (list, tuple)) or len(profile) != 2:
        raise GenericNativePairError("pair support requires an exact 2x2 profile")
    condition_order = list(relation.conditioner_domain)
    target_order = list(relation.target_domain)
    if (not _distinct_native_pair(condition_order)
            or not _distinct_native_pair(target_order)):
        raise GenericNativePairError("pair domains must each have two distinct typed states")
    _require_lossless_mapping_keys(condition_order)
    _require_lossless_mapping_keys(target_order)
    denominators: dict = {}
    counts: dict = {}
    cell_states: dict = {}
    for expected_c, row in zip(condition_order, profile, strict=True):
        if not isinstance(row, dict) or not _same_native(row.get("condition_state"), expected_c):
            raise GenericNativePairError("condition row typed order/domain mismatch")
        if row.get("source_native_conditioner") != relation.conditioner_source_native_variable:
            raise GenericNativePairError("condition source role mismatch")
        denominator = _exact_count(row.get("condition_denominator_support"),
                                   "condition_denominator_support")
        targets = row.get("target_counts")
        if not isinstance(targets, (list, tuple)) or len(targets) != 2:
            raise GenericNativePairError("target row is not an exact two-cell profile")
        counts[expected_c] = {}
        cell_states[expected_c] = {}
        for expected_t, cell in zip(target_order, targets, strict=True):
            if not isinstance(cell, dict) or not _same_native(cell.get("target_state"), expected_t):
                raise GenericNativePairError("target cell typed order/domain mismatch")
            if cell.get("source_native_target") != relation.target_source_native_variable:
                raise GenericNativePairError("target source role mismatch")
            n = _exact_count(cell.get("joint_support_count"), "joint_support_count")
            state = cell.get("joint_cell_state")
            if n > 0 and state != "OBSERVED_POSITIVE":
                raise GenericNativePairError("positive cell has inconsistent state")
            if n == 0 and state not in ("ZERO_SUPPORT", "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"):
                raise GenericNativePairError("zero cell has inconsistent state")
            counts[expected_c][expected_t] = n
            cell_states[expected_c][expected_t] = state
        if denominator != sum(counts[expected_c].values()):
            raise GenericNativePairError("condition denominator differs from target counts")
        denominators[expected_c] = denominator
    support = sum(denominators.values())
    if support > eligible:
        raise GenericNativePairError("joint support exceeds eligible joint risk")
    return condition_order, target_order, denominators, counts, cell_states, eligible, excluded, support


def compute_pair_support_signature(relation: Any) -> dict:
    """Compute the pair-support signature from an authentic generic relation.

    Returns a fresh downstream value (never a copy of the relation).  Invalid
    input is refused with ``CONSUMER_INPUT_NOT_GENERIC_PAIR_RELATION``; an
    empty (but well-typed) profile is refused with
    ``RESPONSE_INPUTS_VALID_EMPTY``.
    """
    if not isinstance(relation, GenericNativePairRelation):
        return _refusal(_DECISION_INVALID_INPUT)

    try:
        _verify_identity(relation)
    except GenericNativePairError:
        return _refusal(_DECISION_IDENTITY_MISMATCH)

    try:
        _exact_count(relation.eligible_joint_risk_total, "eligible_joint_risk_total")
        _exact_count(relation.excluded_ineligible_target_count,
                     "excluded_ineligible_target_count")
    except GenericNativePairError:
        return _refusal(_DECISION_INTEGRITY)

    if relation.producer_state_blocking or relation.typed_state != "SUPPORTED":
        out = _refusal(_DECISION_PRODUCER_BLOCKED)
        out["producer_typed_state"] = relation.typed_state
        if relation.typed_state == "ZERO_SUPPORT":
            out["separation_class"] = "UNDETERMINED_ZERO_SUPPORT_RISK"
        return out

    profile = relation.conditional_count_profile
    if not profile:
        out = _refusal(_DECISION_EMPTY)
        out.update(
            read_relation_owner=relation.semantic_owner,
            read_relation_family=relation.family,
            read_relation_object_id=relation.object_id,
            read_relation_content_hash=relation.content_hash,
        )
        return out

    # ---- decode the ordered 2x2 profile (SEMANTIC_ORDERED) -----------------
    try:
        (condition_order, target_order, denominators, counts, cell_states,
         eligible_total, excluded_total, joint_support_total) = _decode_profile(relation)
    except (GenericNativePairError, TypeError, ValueError, KeyError):
        return _refusal(_DECISION_INTEGRITY)

    # ---- computed fields (genuinely derived, not copied) -------------------
    support_vectors = {
        c: {t: counts[c][t] for t in target_order} for c in condition_order
    }
    zero_cell_semantics = {
        c: {t: cell_states[c][t] for t in target_order} for c in condition_order
    }
    condition_states_with_positive_denominator = [
        c for c in condition_order if denominators[c] > 0]

    # ---- separation classification ----------------------------------------
    positive_denom = condition_states_with_positive_denominator

    if eligible_total == 0:
        # The whole eligible risk set is empty: nothing can separate anything.
        separation_class = "UNDETERMINED_NO_ELIGIBLE_RISK"
    elif joint_support_total == 0:
        # Risk exists but there are no supported observations.
        separation_class = "UNDETERMINED_ZERO_SUPPORT_RISK"
    elif len(positive_denom) < 2:
        # At least one conditioner level has no eligible members, so the pair
        # cannot be separated along that level.
        separation_class = "UNDETERMINED_NO_ELIGIBLE_RISK"
    else:
        # Both conditioner levels carry eligible members: can X separate Y?
        winners: list[list[str]] = []
        for c in condition_order:
            winners.append([t for t in target_order if counts[c][t] > 0])
        if (all(len(w) == 1 for w in winners)
                and len({w[0] for w in winners}) == 2):
            # each conditioner state maps to exactly one distinct target state
            separation_class = "EXACT_PAIR_SEPARATION"
        else:
            # target does not vary with conditioner (collapsed / mixed)
            separation_class = "NO_PAIR_SEPARATION"

    separation_signature = (
        f"{relation.conditioner_source_native_variable}"
        f"|{relation.target_source_native_variable}"
        f"|{relation.operation_role_order}"
        f"|{separation_class}"
        f"|{'.'.join(f'{c}{t}={counts[c][t]}' for c in condition_order for t in target_order)}"
    )

    result = {
        "consumer_id": GENERIC_CONSUMER_ID,
        "consumer_output_family": GENERIC_RESULT_FAMILY,
        "decision_state": _DECISION_COMPUTED,
        "downstream_value_produced": True,
        "generic_native_semantics_hold": "RETAINED",
        "read_relation_owner": relation.semantic_owner,
        "read_relation_family": relation.family,
        "read_relation_object_id": relation.object_id,
        "read_relation_content_hash": relation.content_hash,
        "separation_class": separation_class,
        "separation_signature": separation_signature,
        "support_vectors": support_vectors,
        "zero_cell_semantics": zero_cell_semantics,
        "joint_support_total": joint_support_total,
        "eligible_joint_risk_total": eligible_total,
        "excluded_ineligible_target_count": excluded_total,
        "condition_states_with_positive_denominator": condition_states_with_positive_denominator,
        "measure_kind": relation.measure_kind,
        "measure_basis_ref": (relation.measure_basis_ref.as_dict()
                              if hasattr(relation.measure_basis_ref, "as_dict")
                              else dict(relation.measure_basis_ref)),
        "operation_role_order": relation.operation_role_order,
        "native_component_order": list(relation.native_component_order),
        "permission_ceilings": {
            "producer": list(relation.producer_permission_ceiling),
            "relation": list(relation.relation_permission_ceiling),
        },
        "is_population_evidence_not_actor_fact": True,
        "makes_no_causal_or_psychological_claim": True,
        "production_owner_commit": False,
    }

    # Total deterministic identity over the result content (excluding itself).
    body = {k: v for k, v in result.items() if k != "result_hash"}
    result["result_hash"] = semantic_hash(body)
    return result
