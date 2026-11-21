"""DHIKRYMULCH F6: sharp, source-bound NON-OBSERVED two-proposition overlap.

Consume two already-received S04/I03 RAW unary observations.  A positive
SOURCE_UNIVERSE_RELATION authority must explicitly bind BOTH observations
to the SAME *complete finite eligible frame* before sample fractions may
be treated as exact marginals of that common frame.  Without that bridge,
return the two separate source-local findings and a typed HOLD.

This does not match respondents, create a synthetic C11 joint, pool sources,
select a coupling, infer causality, or construct a PYAT/SOROK person.  The
Fréchet interval is a mathematical constraint on unobserved overlap under
the exact common-population premise, NOT a survey design-based confidence
interval or a generative draw law.  Other target populations and surveys
with estimated (rather than exact census) rates require different science.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from json import loads
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry, Pre553AuthorityError,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, ExactRef, authority_ref, canonical_json, canonicalize,
    exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, _read,
)

CONTRACT = "S04_PARTIALLY_IDENTIFIED_UNOBSERVED_REPERTOIRE@1"
BRIDGE_OPERATION = "S04_UNOBSERVED_JOINT_COMMON_FINITE_FRAME"
BRIDGE_KIND = "SOURCE_UNIVERSE_RELATION"
GRADE = "EXACT_LOGICAL_FINITE_FRAME_BOUNDS__NO_RESPONDENT_JOINT__NO_POPULATION_SAMPLING"
UNISSUED = (
    "NO_RESPONDENT_COTRAVEL_OR_SYNTHETIC_CASES",
    "NO_INDEPENDENCE_OR_MAX_ENTROPY_COUPLING_SELECTED",
    "NO_ORIGINAL_SOURCE_AUTHORIZATION_FROM_THIS_CALCULATOR",
    "NO_SAMPLING_DESIGN_OR_TRANSPORT_VARIANCE_FROM_RAW_RATES",
    "NO_STRUCTURAL_POWER_CAUSALITY_OR_PERSON_CONSTRUCTION",
)


class PartialIdentificationError(ValueError):
    """Malformed, forged, or scientifically incompatible input."""


@dataclass(frozen=True)
class PartiallyIdentifiedRepertoire:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        material = loads(self.payload_json)
        if (not isinstance(material, dict)
                or material.get("contract") != CONTRACT
                or canonical_json(material) != self.payload_json
                or semantic_hash(material) != self.content_hash):
            raise PartialIdentificationError("PARTIAL_REPERTOIRE_SEAL_OR_CONTRACT_INVALID")

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT, f"urn:rawlsing:s04:partial:sha256:{self.content_hash}",
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _seal(payload: dict[str, Any]) -> PartiallyIdentifiedRepertoire:
    return PartiallyIdentifiedRepertoire(
        canonical_json(payload), semantic_hash(payload),
    )


def _fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def _exact_pair(value: Any, label: str) -> tuple[ExactRef, ExactRef]:
    # Exact left/right role identity, not a set: two distinct sources may
    # legitimately share a question, response grammar, or measure basis ref.
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise PartialIdentificationError(f"{label}_EXACT_TWO_ROLE_REFS_REQUIRED")
    return exact_ref(value[0]), exact_ref(value[1])


def _marginal(
    knowledge: S04ObservedKnowledge,
    *,
    positive_cell: Any,
    label: str,
) -> tuple[dict[str, Any], Fraction]:
    if type(knowledge) is not S04ObservedKnowledge:
        raise PartialIdentificationError(f"{label}_EXACT_S04_OBJECT_REQUIRED")
    m = _read(knowledge)  # Existing source meaning, replay, and hash checks.
    if (m.get("state") != "SUPPORTED_SAMPLE_DESCRIPTIVE"
            or m.get("measure_kind") != "RAW"
            or m.get("source_scope_mode") != "SINGLE_UNIVERSE"
            or m.get("target_arity") != 1
            or m.get("risk_set_type") not in (
                "WHOLE_QUESTION_RISK_SET", "COMMON_ELIGIBLE_RISK_SET",
                "ISSUED_SUBPOPULATION_RISK_SET",
            )):
        raise PartialIdentificationError(
            f"{label}_REQUIRES_POSITIVE_RAW_UNARY_SOURCE_OBSERVATION"
        )
    n = m.get("raw_eligible_condition_denominator")
    resolved = m.get("raw_fully_resolved_joint_n")
    if (type(n) is not int or n <= 0 or type(resolved) is not int
            or resolved != n):
        raise PartialIdentificationError(
            f"{label}_INCOMPLETE_OR_ZERO_ELIGIBLE_FRAME"
        )
    domains = m.get("target_domains")
    rows = m.get("complete_cells")
    if (not isinstance(domains, list) or len(domains) != 1
            or not isinstance(domains[0], list) or not domains[0]
            or not isinstance(rows, list)):
        raise PartialIdentificationError(f"{label}_EXACT_DOMAIN_REQUIRED")
    chosen = canonicalize(positive_cell)
    domain_keys = {canonical_json(canonicalize(v)) for v in domains[0]}
    if canonical_json(chosen) not in domain_keys:
        raise PartialIdentificationError(f"{label}_POSITIVE_CELL_NOT_IN_SOURCE_DOMAIN")
    counts = {}
    for row in rows:
        if (not isinstance(row, Mapping)
                or not isinstance(row.get("cell"), list)
                or len(row["cell"]) != 1
                or type(row.get("raw_count")) is not int
                or row["raw_count"] < 0):
            raise PartialIdentificationError(f"{label}_MALFORMED_UNARY_CELL")
        key = canonical_json(canonicalize(row["cell"][0]))
        if key in counts:
            raise PartialIdentificationError(f"{label}_DUPLICATED_SOURCE_CELL")
        counts[key] = row["raw_count"]
    if set(counts) != domain_keys or sum(counts.values()) != n:
        raise PartialIdentificationError(
            f"{label}_MARGINAL_LOST_FULL_SOURCE_DENOMINATOR"
        )
    selected = counts[canonical_json(chosen)]
    value = Fraction(selected, n)
    return {
        "s04_observation_ref": knowledge.ref.as_dict(),
        "source_universe_ref": exact_ref(m["universe_ref"]).as_dict(),
        "release_ref": exact_ref(m["release_ref"]).as_dict(),
        "risk_set_ref": exact_ref(m["risk_set_ref"]).as_dict(),
        "query_ref": exact_ref(m["query_ref"]).as_dict(),
        "fact_ref": exact_ref(m["fact_ref"]).as_dict(),
        "replay_ref": exact_ref(m["replay_ref"]).as_dict(),
        "predicate_ref": exact_ref(m["predicate_ref"]).as_dict(),
        "response_semantics_ref": exact_ref(m["response_semantics_ref"]).as_dict(),
        "measure_basis_ref": exact_ref(m["measure_basis_ref"]).as_dict(),
        "target_ref": exact_ref(m["target_refs"][0]).as_dict(),
        "event_cell": chosen,
        "event_raw_n": selected,
        "eligible_raw_n": n,
        "source_local_raw_fraction": _fraction(value),
        "source_local_grade": m["grade"],
    }, value


def _bridge(
    left: Mapping[str, Any], right: Mapping[str, Any],
    registry: AuthorityRegistry,
    authority: AuthorityRef,
) -> tuple[ExactRef, dict[str, Any]]:
    if not isinstance(registry, AuthorityRegistry):
        raise PartialIdentificationError("EXACT_AUTHORITY_REGISTRY_REQUIRED")
    if not isinstance(authority, AuthorityRef):
        raise PartialIdentificationError("EXACT_COMMON_FRAME_AUTHORITY_REF_REQUIRED")
    try:
        # Require an *already selected exact*, current-in-registry positive
        # source relation, for both universe scopes. Do not self-issue one.
        for source in (left, right):
            registry.require(
                authority,
                authority_kind=BRIDGE_KIND,
                operation=BRIDGE_OPERATION,
                object_family="EmpiricalFact@1.0.0",
                source_universe_ref=source["source_universe_ref"],
            )
        snapshot = registry.resolve_exact(authority).snapshot
    except Pre553AuthorityError as exc:
        raise PartialIdentificationError("COMMON_FRAME_AUTHORITY_NOT_POSITIVE") from exc
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise PartialIdentificationError("COMMON_FRAME_SCOPE_REQUIRED")
    required_sets = (
        ("source_universe_refs", "source_universe_ref"),
        ("release_refs", "release_ref"),
        ("s04_knowledge_refs", "s04_observation_ref"),
        ("risk_set_refs", "risk_set_ref"),
        ("target_refs", "target_ref"),
        ("response_semantics_refs", "response_semantics_ref"),
        ("measure_basis_refs", "measure_basis_ref"),
        ("predicate_refs", "predicate_ref"),
    )
    for key, field in required_sets:
        target = (exact_ref(left[field]), exact_ref(right[field]))
        if _exact_pair(scope.get(key), key) != target:
            raise PartialIdentificationError(f"COMMON_FRAME_{key.upper()}_MISMATCH")
    n = scope.get("finite_population_n")
    if (type(n) is not int or n <= 0
            or n != left["eligible_raw_n"]
            or n != right["eligible_raw_n"]):
        raise PartialIdentificationError("COMMON_FRAME_NOT_FULLY_ENUMERATED")
    if scope.get("frame_coverage") != "BOTH_COMPLETE_FINITE_FRAME_CENSUS":
        raise PartialIdentificationError("EXACT_COMMON_FRAME_CENSUS_NOT_ISSUED")
    if scope.get("joint_observation") != "NO_RESPONDENT_LINKAGE":
        raise PartialIdentificationError("UNOBSERVED_JOINT_CLAIM_NOT_SUPPORTED")
    if (not isinstance(scope.get("frame_period"), str)
            or not scope["frame_period"].strip()
            or scope["frame_period"].upper() in {"UNKNOWN", "LATEST"}):
        raise PartialIdentificationError("EXACT_COMMON_FRAME_PERIOD_REQUIRED")
    frame = exact_ref(scope.get("common_frame_ref"), "common_frame_ref")
    # Source assertions are still the external issuer's responsibility. The
    # calculator only verifies that its *exact two inputs* are in the scope.
    return frame, {
        "authority_ref": authority.as_dict(),
        "common_frame_ref": frame.as_dict(),
        "finite_population_n": n,
        "frame_period": scope["frame_period"],
        "frame_coverage": scope["frame_coverage"],
        "joint_observation": "NO_RESPONDENT_LINKAGE",
    }


def identify_unobserved_overlap(
    *,
    left: S04ObservedKnowledge,
    right: S04ObservedKnowledge,
    left_event_cell: Any,
    right_event_cell: Any,
    authority_registry: AuthorityRegistry | None = None,
    common_frame_authority_ref: AuthorityRef | None = None,
) -> PartiallyIdentifiedRepertoire:
    """Sharp 2x2 Fréchet logical range conditional on exact common frame.

    Missing/inadequate source bridge produces a *typed held product*, never
    a fake zero, a unique joint, or a normalized independent sampler.
    """
    l, p = _marginal(left, positive_cell=left_event_cell, label="LEFT")
    r, q = _marginal(right, positive_cell=right_event_cell, label="RIGHT")
    if (exact_ref(l["release_ref"]) == exact_ref(r["release_ref"])
            or exact_ref(l["source_universe_ref"])
            == exact_ref(r["source_universe_ref"])
            or left.ref == right.ref):
        raise PartialIdentificationError(
            "SAME_SOURCE_MUST_USE_ACTUAL_RESPONDENT_JOINT_INSTEAD"
        )
    base = {
        "contract": CONTRACT,
        "marginal_left": l, "marginal_right": r,
        "joint_observation_state": "NOT_OBSERVED_NO_LINKED_RESPONDENTS",
        "source_local_marginals_not_a_joint": True,
        "unissued": list(UNISSUED),
        "first_consumer_policy": (
            "NO_FF01_SUPPORTED_JOINT_NO_V3_SAMPLING_OR_CO_PARENT_PAIRING"
        ),
        "next_warranted_question": (
            "SEEK_QUALIFIED_COMMON_FRAME_AND_COADMINISTERED_JOINT"
        ),
        "bounds": None,
        "countercouplings": None,
        "common_frame": None,
    }
    if common_frame_authority_ref is None or authority_registry is None:
        return _seal({
            **base, "state": "HELD_POPULATION_BRIDGE_UNPROVEN",
            "hold_reason": "NO_EXACT_POSITIVE_COMMON_FRAME_AUTHORITY",
        })
    try:
        frame, bridge = _bridge(l, r, authority_registry, common_frame_authority_ref)
    except (PartialIdentificationError, KeyError, ValueError) as exc:
        return _seal({
            **base, "state": "HELD_POPULATION_BRIDGE_UNPROVEN",
            "hold_reason": (
                str(exc) if isinstance(exc, PartialIdentificationError)
                else "MALFORMED_OR_STALE_COMMON_FRAME_AUTHORITY"
            ),
        })
    lower = max(Fraction(0), p + q - 1)
    upper = min(p, q)
    if lower > upper:
        raise PartialIdentificationError("INCONSISTENT_MARGINAL_PREMISES")
    def coupling(joint: Fraction) -> dict[str, dict[str, int]]:
        return {
            "A_AND_B": _fraction(joint),
            "A_ONLY": _fraction(p - joint),
            "B_ONLY": _fraction(q - joint),
            "NEITHER": _fraction(1 - p - q + joint),
        }
    def interval(den: Fraction) -> dict[str, Any] | None:
        return (
            {"lower": _fraction(lower / den), "upper": _fraction(upper / den)}
            if den else None
        )
    return _seal({
        **base,
        "state": "SHARP_PARTIAL_IDENTIFICATION_CONDITIONAL_ON_COMMON_FINITE_FRAME",
        "grade": GRADE,
        "common_frame": bridge,
        "bounds": {
            "A_AND_B": {"lower": _fraction(lower), "upper": _fraction(upper)},
            "A_GIVEN_B": interval(q),
            "B_GIVEN_A": interval(p),
            "positive_overlap_logically_necessary": lower > 0,
            "zero_overlap_logically_possible": lower == 0,
            "point_identified_logically_not_observed": lower == upper,
        },
        "countercouplings": {
            "LOWER_EXTREME": coupling(lower),
            "UPPER_EXTREME": coupling(upper),
        },
        "relation_not_person_or_sampler": (
            "LOGICAL_FEASIBLE_SET_ONLY_NO_SELECTED_JOINT_DISTRIBUTION"
        ),
    })


def replay_unobserved_overlap(
    *,
    relation: PartiallyIdentifiedRepertoire,
    left: S04ObservedKnowledge,
    right: S04ObservedKnowledge,
    left_event_cell: Any,
    right_event_cell: Any,
    authority_registry: AuthorityRegistry | None = None,
    common_frame_authority_ref: AuthorityRef | None = None,
) -> PartiallyIdentifiedRepertoire:
    """Recompute from actual S04 sources and CURRENT exact common-frame issuer.

    A content-consistent hash is not evidence of authorization. A changed
    observation, withdrawn bridge, or self-rehashed forged bound must fail.
    """
    if type(relation) is not PartiallyIdentifiedRepertoire:
        raise PartialIdentificationError("EXACT_PARTIAL_RELATION_REQUIRED")
    fresh = identify_unobserved_overlap(
        left=left, right=right,
        left_event_cell=left_event_cell,
        right_event_cell=right_event_cell,
        authority_registry=authority_registry,
        common_frame_authority_ref=common_frame_authority_ref,
    )
    if fresh.ref != relation.ref:
        raise PartialIdentificationError("F6_SOURCE_AND_ISSUER_REPLAY_MISMATCH")
    return fresh


def ask_partial_repertoire_configuration(
    *,
    relation: PartiallyIdentifiedRepertoire,
    event_a: bool,
    event_b: bool,
    left: S04ObservedKnowledge | None = None,
    right: S04ObservedKnowledge | None = None,
    left_event_cell: Any = None,
    right_event_cell: Any = None,
    authority_registry: AuthorityRegistry | None = None,
    common_frame_authority_ref: AuthorityRef | None = None,
) -> dict[str, Any]:
    """Consumer-facing *possibility constraint*, NOT a sampler or case.

    The four exclusive configurations admit different marginal-compatible
    feasible intervals. Even a point-identified frequency does NOT certify
    one person or couple. This reader never selects a coupling, creates a
    survey row, or converts a sampled finite frame into universal impossibility.
    """
    if type(relation) is not PartiallyIdentifiedRepertoire:
        raise PartialIdentificationError("EXACT_PARTIAL_RELATION_REQUIRED")
    if type(event_a) is not bool or type(event_b) is not bool:
        raise PartialIdentificationError("EXACT_BINARY_EVENT_ROLES_REQUIRED")
    m = relation.material()
    if m["state"] == "SHARP_PARTIAL_IDENTIFICATION_CONDITIONAL_ON_COMMON_FINITE_FRAME":
        if (type(left) is not S04ObservedKnowledge
                or type(right) is not S04ObservedKnowledge
                or type(authority_registry) is not AuthorityRegistry
                or type(common_frame_authority_ref) is not AuthorityRef):
            raise PartialIdentificationError("F6_EXACT_SOURCE_AND_AUTHORITY_REPLAY_REQUIRED")
        replay_unobserved_overlap(
            relation=relation, left=left, right=right,
            left_event_cell=left_event_cell,
            right_event_cell=right_event_cell,
            authority_registry=authority_registry,
            common_frame_authority_ref=common_frame_authority_ref,
        )
    base = {
        "contract": "S04_PARTIAL_REPERTOIRE_CONFIGURATION_CONSTRAINT@1",
        "relation_ref": relation.ref.as_dict(),
        "event_a": event_a,
        "event_b": event_b,
        "not_an_observed_joint_or_person": True,
        "selected_coupling": None,
        "source_grade": "NO_ORIGINAL_SOURCE_OR_ACTOR_PERMISSION_INFERRED",
        "interval": None,
    }
    if m["state"] != "SHARP_PARTIAL_IDENTIFICATION_CONDITIONAL_ON_COMMON_FINITE_FRAME":
        return {
            **base, "state": "HELD_COMMON_POPULATION_UNPROVEN",
            "configuration_status": "UNASSESSABLE_NOT_IMPOSSIBLE",
        }
    low = m["countercouplings"]["LOWER_EXTREME"]
    high = m["countercouplings"]["UPPER_EXTREME"]
    name = (
        "A_AND_B" if event_a and event_b
        else "A_ONLY" if event_a else "B_ONLY" if event_b else "NEITHER"
    )
    def as_fraction(material: Mapping[str, Any]) -> Fraction:
        return Fraction(material["numerator"], material["denominator"])
    # A_ONLY and B_ONLY move in the *opposite* direction of overlap.
    v1, v2 = as_fraction(low[name]), as_fraction(high[name])
    lo, hi = min(v1, v2), max(v1, v2)
    return {
        **base,
        "state": "CONSTRAINT_CALCULATED_FOR_EXACT_FINITE_FRAME",
        "configuration_status": (
            "NO_OCCURRENCE_COMPATIBLE_WITH_THIS_EXACT_FRAME"
            if hi == 0 else
            "SOME_OCCURRENCE_LOGICALLY_REQUIRED_WITHIN_FRAME"
            if lo > 0 else
            "POSSIBLE_BUT_NOT_LOGICALLY_REQUIRED_WITHIN_FRAME"
        ),
        "interval": {"lower": _fraction(lo), "upper": _fraction(hi)},
        "requested_configuration": name,
    }


__all__ = [
    "CONTRACT", "BRIDGE_OPERATION", "BRIDGE_KIND", "GRADE",
    "PartialIdentificationError", "PartiallyIdentifiedRepertoire",
    "identify_unobserved_overlap", "replay_unobserved_overlap",
    "ask_partial_repertoire_configuration",
]
