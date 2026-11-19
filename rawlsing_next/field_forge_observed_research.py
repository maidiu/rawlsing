"""S04->FF01 exact observed-sample descriptive research over one I03 joint.

Operates ONLY on an independently received FF01ObservedJoint, without another
respondent executor, source parser, surrogate model or ranking estimator.
Counts are conditioned COMPLETE-CASE samples, not representative probabilities.
A reproducible research request may change axes/conditions without resampling.
"""
from __future__ import annotations

from dataclasses import dataclass
from json import loads
from typing import Any, Mapping, Sequence

from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01ObservedJoint, FAMILY as FF01_FAMILY,
)
from rawlsing_next.pre553_empirical_objects import (
    ExactRef, canonical_json, canonicalize, semantic_hash,
)

CONTRACT = "S04_FF01_EXACT_DESCRIPTIVE_QUERY@1.0.0"
STATE_SUPPORTED = "OBSERVED_COMPLETE_CASE_SUPPORT"
STATE_ZERO = "ZERO_OBSERVED_COMPLETE_CASE_SUPPORT"
STATE_BLOCKED = "UPSTREAM_TYPED_NONPOSITIVE"
ESTIMAND = "RAW_WITHIN_FULLY_RESOLVED_JOINT__NOT_SURVEY_DESIGN"
UNISSUED_SCIENCE = (
    "POPULATION_CONFIDENCE_UNISSUED",
    "COMPARATIVE_DETERMINICITY_ESTIMAND_UNISSUED",
    "POST_SELECTION_RANK_STABILITY_UNISSUED",
    "ADAPTIVE_RECURSIVE_MINORITY_DISCOVERY_UNISSUED",
    "STRUCTURAL_CAUSATION_UNISSUED",
    "ACTOR_AND_PERSON_GENERATION_UNISSUED",
)


class ObservedResearchError(ValueError):
    """Unsupported or contradicted source-exact research request."""


@dataclass(frozen=True)
class ExactDescriptiveResearchAnswer:
    """Content-addressed immutable read receipt; no own empirical authority."""

    canonical_payload: str
    content_hash: str

    def __post_init__(self) -> None:
        obj = loads(self.canonical_payload)
        if canonical_json(obj) != self.canonical_payload:
            raise ObservedResearchError("noncanonical research answer")
        if obj.get("contract") != CONTRACT or semantic_hash(obj) != self.content_hash:
            raise ObservedResearchError("research answer identity mismatch")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(CONTRACT, f"urn:rawlsing:s04:ff01-descriptive:sha256:{self.content_hash}", self.content_hash)

    def material(self) -> dict[str, Any]:
        return loads(self.canonical_payload)


def _selected_indices(conditions: Mapping[int, Any], arity: int, target_index: int) -> tuple[tuple[int, Any], ...]:
    if not isinstance(conditions, Mapping):
        raise ObservedResearchError("conditions must bind explicit target indices")
    selected: list[tuple[int, Any]] = []
    for raw_idx, value in conditions.items():
        if type(raw_idx) is not int or not (0 <= raw_idx < arity) or raw_idx == target_index:
            raise ObservedResearchError("invalid conditioner index or target leakage")
        selected.append((raw_idx, canonicalize(value)))
    return tuple(sorted(selected))


def _source_joint(received: FF01ObservedJoint) -> dict[str, Any]:
    if type(received) is not FF01ObservedJoint:
        raise ObservedResearchError("actual FF01 receipt required")
    material = received.semantic_projection()
    if material["family"] != FF01_FAMILY:
        raise ObservedResearchError("wrong FF01 evidence family")
    if received.ref.content_hash != semantic_hash(material):
        raise ObservedResearchError("mutated or substituted FF01 receipt")
    if material["joint_arity"] != len(material["target_refs"]):
        raise ObservedResearchError("FF01 joint arity mismatch")
    return material


def ask_exact_descriptive_support(
    *,
    received: FF01ObservedJoint,
    target_index: int,
    conditions: Mapping[int, Any],
) -> ExactDescriptiveResearchAnswer:
    """Return all target-state counts conditioned on explicit observed states.

    The only denominator here is sum of fully resolved joint cells *within*
    the conditioning selection.  The I03 original risk/eligible denominator is
    preserved separately.  Missing/repeating/routing cannot be backfilled;
    when I03 has no positive joint the result stays blocked, not zero.
    """
    m = _source_joint(received)
    arity = m["joint_arity"]
    if type(target_index) is not int or not 0 <= target_index < arity:
        raise ObservedResearchError("target_index must be an actual joint dimension")
    selected = _selected_indices(conditions, arity, target_index)
    if len(selected) != len(set(i for i, _ in selected)):
        raise ObservedResearchError("duplicate conditioning axis")
    counts: dict[str, int] = {}
    target_states: dict[str, Any] = {}
    if m["producer_state"] == "SUPPORTED":
        if not m["complete_cells"]:
            raise ObservedResearchError("supported FF01 without complete joint cells")
        for row in m["complete_cells"]:
            state = row["cell"][target_index]
            target_key = canonical_json(state)
            # A state can occur in many compatible joint cells. Its exact
            # canonical representation identifies the public target state.
            target_states[target_key] = state
            counts.setdefault(target_key, 0)
            if all(row["cell"][index] == value for index, value in selected):
                counts[target_key] += row["raw_support"]
        denominator = sum(counts.values())
        state = STATE_SUPPORTED if denominator > 0 else STATE_ZERO
        # With positive original joint support, absent context support is a
        # zero *within this resolved complete-case population*, not a source
        # routing proof that the context never occurs in the full population.
        cells = []
        for key in sorted(counts):
            n = counts[key]
            cells.append({
                "target_state": target_states[key],
                "raw_count": n,
                "observed_cell_state": "POSITIVE" if n else "OBSERVED_ZERO_WITHIN_COMPLETE_CASE",
                "fraction_of_condition_complete_case": (
                    {"$exact_fraction": [n, denominator]} if denominator > 0 else None
                ),
            })
    else:
        denominator = None
        state = STATE_BLOCKED
        cells = []

    answer = {
        "contract": CONTRACT,
        "scope": "SOURCEFREE_OR_ISSUED_AS_PRODUCER__NO_NEW_SOURCE_RIGHT",
        "kind": "DESCRIPTIVE_OBSERVED_SUPPORT_NOT_DETERMINICITY",
        "state": state,
        "upstream_typed_state": m["producer_state"],
        "source_ff01_ref": received.ref.as_dict(),
        "source_query_ref": m["producer_query_ref"],
        "source_fact_ref": m["producer_fact_ref"],
        "source_release_ref": m["release_ref"],
        "source_universe_ref": m["universe_ref"],
        "source_risk_set_ref": m["risk_set_ref"],
        "source_measure_basis_ref": m["measure_basis_ref"],
        "target_index": target_index,
        "target_ref": m["target_refs"][target_index],
        "conditions": [
            {"index": index, "target_ref": m["target_refs"][index], "exact_state": value}
            for index, value in selected
        ],
        "joint_arity": arity,
        "risk_eligible_denominator": m["raw_eligible_condition_denominator"],
        "all_fully_resolved_joint_n": m["raw_fully_resolved_joint_n"],
        "condition_fully_resolved_n": denominator,
        "denominator_grade": ESTIMAND,
        "complete_case_cells": cells,
        "limits": list(UNISSUED_SCIENCE),
    }
    digest = semantic_hash(answer)
    return ExactDescriptiveResearchAnswer(canonical_json(answer), digest)


def ask_observed_minor_cell_candidates(
    *,
    received: FF01ObservedJoint,
    selected_condition_index: int,
    max_observed_support: int,
) -> ExactDescriptiveResearchAnswer:
    """Enumerate observed small-cell *candidates*, not discover social minorities.

    The caller declares a positive integer ceiling. This makes selection
    auditable but is not an inferred minority boundary or significance rule.
    It does not recurse or infer interactions. Zero is not a discovered cohort.
    """
    m = _source_joint(received)
    if type(max_observed_support) is not int or max_observed_support < 1:
        raise ObservedResearchError("positive caller-declared ceiling required")
    if type(selected_condition_index) is not int or not 0 <= selected_condition_index < m["joint_arity"]:
        raise ObservedResearchError("condition axis not in joint")
    supported = m["producer_state"] == "SUPPORTED"
    cells = [
        {"observed_joint_cell": row["cell"], "raw_support": row["raw_support"]}
        for row in m["complete_cells"]
        if supported and 0 < row["raw_support"] <= max_observed_support
    ]
    answer = {
        "contract": CONTRACT,
        "kind": "EXACT_SMALL_CELL_CANDIDATE_SELECTION_NOT_MINORIY_DISCOVERY",
        "state": STATE_SUPPORTED if supported else STATE_BLOCKED,
        "upstream_typed_state": m["producer_state"],
        "source_ff01_ref": received.ref.as_dict(),
        "source_query_ref": m["producer_query_ref"],
        "source_fact_ref": m["producer_fact_ref"],
        "source_release_ref": m["release_ref"],
        "source_universe_ref": m["universe_ref"],
        "source_risk_set_ref": m["risk_set_ref"],
        "selected_condition_index": selected_condition_index,
        "max_observed_support": max_observed_support,
        "all_fully_resolved_joint_n": m["raw_fully_resolved_joint_n"],
        "candidate_cells": sorted(cells, key=lambda row: canonical_json(row["observed_joint_cell"])),
        "selection_grade": "CALLER_DECLARED_SMALL_COUNT_INSPECTION_NO_SIGNIFICANCE",
        "limits": list(UNISSUED_SCIENCE),
    }
    return ExactDescriptiveResearchAnswer(canonical_json(answer), semantic_hash(answer))


def ask_unissued_comparative_ranking(
    *,
    received: FF01ObservedJoint,
    candidate_indices: Sequence[int],
    target_index: int,
) -> ExactDescriptiveResearchAnswer:
    """Preserve a concrete ranking research request WITHOUT manufacturing scores.

    The caller gets an immutable, source-anchored typed SCIENCE_OWNER_HOLD
    suitable for handing to the existing EE07/EE08 scientific owner.
    """
    m = _source_joint(received)
    if type(target_index) is not int or not 0 <= target_index < m["joint_arity"]:
        raise ObservedResearchError("target index outside exact joint")
    if isinstance(candidate_indices, (str, bytes)) or not isinstance(candidate_indices, Sequence):
        raise ObservedResearchError("candidate indices must be an exact sequence")
    items = tuple(candidate_indices)
    if not items or any(type(i) is not int or i == target_index or not 0 <= i < m["joint_arity"] for i in items):
        raise ObservedResearchError("invalid comparative candidate set")
    if len(items) != len(set(items)):
        raise ObservedResearchError("duplicate comparative candidate axis")
    answer = {
        "contract": CONTRACT,
        "kind": "COMPARATIVE_PREDICTOR_RESEARCH_REQUEST",
        "state": "SCIENTIFIC_METHOD_OWNER_HOLD",
        "source_ff01_ref": received.ref.as_dict(),
        "source_release_ref": m["release_ref"],
        "source_risk_set_ref": m["risk_set_ref"],
        "target_index": target_index,
        "target_ref": m["target_refs"][target_index],
        "candidate_indices": list(items),
        "candidate_refs": [m["target_refs"][i] for i in items],
        "comparable_population_assertion": "NOT_SCIENTIFICALLY_ADJUDICATED",
        "ranked_results": None,
        "required_issuance": [
            "TARGET_AND_SCOPE_ESTIMAND",
            "PREDICTOR_METRIC_AND_COMPARABLE_RISK",
            "SAMPLING_WEIGHT_VARIANCE_AND_DESIGN",
            "MULTIPLICITY_POSTSELECTION_AND_STABILITY",
            "RECURSIVE_CANDIDATE_AND_STOPPING_AUTHORITY",
        ],
        "limits": list(UNISSUED_SCIENCE),
    }
    return ExactDescriptiveResearchAnswer(canonical_json(answer), semantic_hash(answer))


__all__ = [
    "CONTRACT", "STATE_SUPPORTED", "STATE_ZERO", "STATE_BLOCKED",
    "ObservedResearchError", "ExactDescriptiveResearchAnswer",
    "ask_exact_descriptive_support", "ask_observed_minor_cell_candidates",
    "ask_unissued_comparative_ranking",
]
