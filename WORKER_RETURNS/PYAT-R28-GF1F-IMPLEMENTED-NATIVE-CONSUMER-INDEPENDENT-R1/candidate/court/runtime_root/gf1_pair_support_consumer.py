"""R27 GF1E — the named downstream consumer for the GF1 generic PAIR relation.

`compute_pair_support_signature(relation) -> dict` reads an immutable
``GenericNativePairRelation`` and COMPUTES a downstream support-signature value.
It never copies the relation's own material and never emits a constant label.

GRAIN: SOURCEFREE_GENERIC_PAIR_CANDIDATE_TEST_ONLY. UNISSUED. NOT ACCEPTED.
GENERIC_NATIVE_SEMANTICS_HOLD RETAINED. No Field Forge semantic issue, no
original source, no OC05/N11/N12/actor/V3.
"""
from __future__ import annotations

from typing import Any

from generic_native_pair_relation import (
    GENERIC_CONSUMER_ID,
    GENERIC_RESULT_FAMILY,
    GenericNativePairRelation,
    GenericNativePairError,
    semantic_hash,
)

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

_OBJECT_ID_PREFIX = "urn:rawlsing:gf1:generic-pair-relation:sha256:"


def _refusal(decision_state: str) -> dict:
    """Minimal, decision-only refusal. Carries no copied or computed science."""
    return {
        "consumer_id": GENERIC_CONSUMER_ID,
        "consumer_output_family": GENERIC_RESULT_FAMILY,
        "decision_state": decision_state,
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
    condition_order: list[str] = []
    target_order: list[str] | None = None
    denominators: dict[str, int] = {}
    counts: dict[str, dict[str, int]] = {}
    cell_states: dict[str, dict[str, str]] = {}

    for row in profile:
        c = str(row["condition_state"])
        if c in condition_order:
            raise GenericNativePairError("duplicate condition_state in profile")
        condition_order.append(c)
        denominators[c] = int(row["condition_denominator_support"])
        counts[c] = {}
        cell_states[c] = {}
        tcs = [str(t["target_state"]) for t in row["target_counts"]]
        if target_order is None:
            target_order = tcs
        elif tcs != target_order:
            raise GenericNativePairError("inconsistent target order across profile rows")
        for t in row["target_counts"]:
            tkey = str(t["target_state"])
            counts[c][tkey] = int(t["joint_support_count"])
            cell_states[c][tkey] = str(t["joint_cell_state"])
    if target_order is None or len(condition_order) != 2 or len(target_order) != 2:
        raise GenericNativePairError("pair support requires an exact 2x2 profile")

    # ---- computed fields (genuinely derived, not copied) -------------------
    support_vectors = {
        c: {t: counts[c][t] for t in target_order} for c in condition_order
    }
    zero_cell_semantics = {
        c: {t: cell_states[c][t] for t in target_order} for c in condition_order
    }
    joint_support_total = sum(
        counts[c][t] for c in condition_order for t in target_order)
    condition_states_with_positive_denominator = [
        c for c in condition_order if denominators[c] > 0]

    # ---- separation classification ----------------------------------------
    eligible_total = int(relation.eligible_joint_risk_total)
    positive_denom = condition_states_with_positive_denominator

    if eligible_total <= 0:
        # The whole eligible risk set is empty: nothing can separate anything.
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
        "excluded_ineligible_target_count": int(relation.excluded_ineligible_target_count),
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
