"""DHIKRYMULCH F6: cross-source partial identification with issued intervals.

Reusable capital: actual I03->S04 unary RAW observations and the existing
F6 source-validating _marginal; existing AuthorityRegistry and exact refs.
No new source reader, empirical estimate, sampling/variance algorithm, joint
respondent table, coupling selector or actor is constructed here.

This operates ONLY when each separately sampled source has a *positively
issued* population-parameter interval (including post-selection/design
coverage), AND an independently issued source relation proves both intervals
refer to exactly the same population and time. A missing premise yields
typed HOLD with the separate valid source-local facts still visible.

Given simultaneous marginal interval coverage, the set of feasible four-cell
probability distributions is the exact 2x2 Fréchet polytope, not an observed
co-travel statistic or a generative distribution. Union-bound simultaneous
coverage is explicitly conditional on the external coverage guarantees.
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
    AuthorityRef, ExactRef, Pre553IntegrityError,
    canonical_json, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import S04ObservedKnowledge
from rawlsing_next.pre553_s04_partially_identified_repertoire import (
    PartialIdentificationError, _marginal, _fraction,
)

CONTRACT = "S04_SOURCE_QUALIFIED_UNCERTAIN_REPERTOIRE@1"
INTERVAL_OPERATION = "S04_ISSUED_POPULATION_EVENT_INTERVAL"
BRIDGE_OPERATION = "S04_UNOBSERVED_JOINT_COMMON_POPULATION_ESTIMAND"
INTERVAL_COVERAGE = (
    "DESIGN_AND_SELECTION_CALIBRATED_PARAMETER_COVERAGE_AT_LEAST_1_MINUS_ALPHA"
)
BRIDGE_KIND = "IDENTICAL_POPULATION_AND_PERIOD_NO_RESPONDENT_LINKAGE"
GRADE = "SHARP_PARAMETER_IDENTIFICATION_UNDER_ISSUED_INTERVALS__NOT_A_JOINT_SAMPLE"
UNISSUED = (
    "NO_RESPONDENT_LINKAGE_OR_OBSERVED_JOINT",
    "NO_INDEPENDENCE_COUPLING_OR_SYNTHETIC_PERSON",
    "NO_RAW_SAMPLE_RATE_AS_POPULATION_PREVALENCE",
    "NO_COUNTRY_YEAR_EQUIVALENCE_WITHOUT_EXACT_BRIDGE",
    "NO_INDEPENDENT_SURVEY_DESIGN_OR_SELECTION_CALIBRATION",
    "NO_FF01_STRUCTURAL_SOROK_PARENT_OR_ACTOR_GRANT",
)


class UncertainRepertoireError(ValueError):
    """Malformed source/authority or unsigned numerical claim."""


@dataclass(frozen=True)
class UncertainRepertoire:
    payload_json: str
    content_hash: str

    def __post_init__(self) -> None:
        try:
            m = loads(self.payload_json)
            if (type(m) is not dict
                    or m.get("contract") != CONTRACT
                    or m.get("unissued") != list(UNISSUED)
                    or canonical_json(m) != self.payload_json
                    or semantic_hash(m) != self.content_hash):
                raise UncertainRepertoireError("UNCERTAIN_REPERTOIRE_SEAL_INVALID")
        except (ValueError, TypeError) as exc:
            raise UncertainRepertoireError("UNCERTAIN_REPERTOIRE_SEAL_INVALID") from exc

    @property
    def ref(self) -> ExactRef:
        return ExactRef(
            CONTRACT,
            "urn:rawlsing:s04:uncertain-repertoire:sha256:" + self.content_hash,
            self.content_hash,
        )

    def material(self) -> dict[str, Any]:
        return loads(self.payload_json)


def _seal(material: dict[str, Any]) -> UncertainRepertoire:
    return UncertainRepertoire(canonical_json(material), semantic_hash(material))


def _rat(value: Any, label: str) -> Fraction:
    if (not isinstance(value, Mapping)
            or set(value) != {"numerator", "denominator"}
            or type(value["numerator"]) is not int
            or type(value["denominator"]) is not int
            or value["denominator"] <= 0):
        raise UncertainRepertoireError(f"{label}_EXACT_RATIONAL_REQUIRED")
    out = Fraction(value["numerator"], value["denominator"])
    if not 0 <= out <= 1:
        raise UncertainRepertoireError(f"{label}_NOT_A_PROBABILITY")
    return out


def _same_ref(value: Any, expected: Any, field: str) -> None:
    if exact_ref(value) != exact_ref(expected):
        raise UncertainRepertoireError(f"SOURCE_PIN_{field.upper()}_MISMATCH")


def _scope_for_source(
    source: Mapping[str, Any],
    registry: AuthorityRegistry,
    ref: AuthorityRef,
    role: str,
) -> tuple[dict[str, Any], Fraction, Fraction, Fraction]:
    if type(ref) is not AuthorityRef:
        raise UncertainRepertoireError(f"{role}_EXACT_INTERVAL_AUTHORITY_REQUIRED")
    snapshot = registry.require(
        ref,
        authority_kind="UNCERTAINTY_METHOD",
        operation=INTERVAL_OPERATION,
        object_family="EmpiricalFact@1.0.0",
        source_universe_ref=source["source_universe_ref"],
    )
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise UncertainRepertoireError(f"{role}_INTERVAL_SCOPE_MALFORMED")
    source_fields = (
        ("source_universe_ref", "source_universe_ref"),
        ("release_ref", "release_ref"),
        ("s04_observation_ref", "s04_observation_ref"),
        ("risk_set_ref", "risk_set_ref"),
        ("query_ref", "query_ref"),
        ("fact_ref", "fact_ref"),
        ("predicate_ref", "predicate_ref"),
        ("replay_ref", "replay_ref"),
        ("target_ref", "target_ref"),
        ("response_semantics_ref", "response_semantics_ref"),
        ("measure_basis_ref", "measure_basis_ref"),
    )
    for key, source_key in source_fields:
        _same_ref(scope.get(key), source[source_key], key)
    if canonical_json(scope.get("event_cell")) != canonical_json(source["event_cell"]):
        raise UncertainRepertoireError(f"{role}_EVENT_PROPOSITION_CHANGED")
    if scope.get("coverage_kind") != INTERVAL_COVERAGE:
        raise UncertainRepertoireError(f"{role}_METHOD_DESIGN_COVERAGE_UNISSUED")
    if scope.get("uses_observed_raw_as_population_prevalence") is not False:
        raise UncertainRepertoireError(f"{role}_RAW_SOURCE_RATE_PROMOTED_TO_POPULATION")
    period = scope.get("population_period")
    if (type(period) is not str or not period.strip()
            or period.upper() in {"UNKNOWN", "LATEST"}):
        raise UncertainRepertoireError(f"{role}_PERIOD_NOT_ISSUED")
    pop = exact_ref(scope.get("target_population_ref"))
    design = exact_ref(scope.get("survey_design_method_ref"))
    selection = exact_ref(scope.get("selection_coverage_method_ref"))
    lo = _rat(scope.get("parameter_lower"), role + "_LOWER")
    hi = _rat(scope.get("parameter_upper"), role + "_UPPER")
    alpha = _rat(scope.get("error_probability_upper"), role + "_ERROR")
    if lo > hi or alpha >= 1:
        raise UncertainRepertoireError(f"{role}_INVALID_ISSUED_PARAMETER_INTERVAL")
    return ({
        "authority_ref": ref.as_dict(),
        "population_ref": pop.as_dict(),
        "population_period": period,
        "survey_design_method_ref": design.as_dict(),
        "selection_coverage_method_ref": selection.as_dict(),
        "coverage_kind": INTERVAL_COVERAGE,
        "parameter_lower": _fraction(lo),
        "parameter_upper": _fraction(hi),
        "error_probability_upper": _fraction(alpha),
        "issuer_claimed_coverage": True,
    }, lo, hi, alpha)


def _common_population(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    li: Mapping[str, Any],
    ri: Mapping[str, Any],
    registry: AuthorityRegistry,
    bridge_ref: AuthorityRef,
) -> dict[str, Any]:
    if type(bridge_ref) is not AuthorityRef:
        raise UncertainRepertoireError("EXACT_COMMON_POPULATION_BRIDGE_REQUIRED")
    for source in (left, right):
        registry.require(
            bridge_ref,
            authority_kind="SOURCE_UNIVERSE_RELATION",
            operation=BRIDGE_OPERATION,
            object_family="EmpiricalFact@1.0.0",
            source_universe_ref=source["source_universe_ref"],
        )
    scope = registry.resolve_exact(bridge_ref).snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise UncertainRepertoireError("COMMON_POPULATION_SCOPE_MALFORMED")
    for field, sourcekey in (
        ("source_universe_refs", "source_universe_ref"),
        ("release_refs", "release_ref"),
        ("s04_knowledge_refs", "s04_observation_ref"),
        ("risk_set_refs", "risk_set_ref"),
        ("target_refs", "target_ref"),
        ("response_semantics_refs", "response_semantics_ref"),
        ("measure_basis_refs", "measure_basis_ref"),
        ("predicate_refs", "predicate_ref"),
    ):
        refs = scope.get(field)
        if (not isinstance(refs, (list, tuple)) or len(refs) != 2
                or exact_ref(refs[0]) != exact_ref(left[sourcekey])
                or exact_ref(refs[1]) != exact_ref(right[sourcekey])):
            raise UncertainRepertoireError(f"POPULATION_BRIDGE_{field.upper()}_MISMATCH")
    roles = scope.get("interval_authority_refs")
    if (not isinstance(roles, (list, tuple)) or len(roles) != 2
            or roles[0] != li["authority_ref"] or roles[1] != ri["authority_ref"]):
        raise UncertainRepertoireError("POPULATION_BRIDGE_INTERVAL_AUTHORITY_DRIFT")
    common = exact_ref(scope.get("target_population_ref"))
    if (common != exact_ref(li["population_ref"])
            or common != exact_ref(ri["population_ref"])):
        raise UncertainRepertoireError("POPULATION_BRIDGE_MISMATCHED_TARGET")
    period = scope.get("population_period")
    if (period != li["population_period"] or period != ri["population_period"]
            or scope.get("population_bridge_kind") != BRIDGE_KIND):
        raise UncertainRepertoireError("POPULATION_BRIDGE_PERIOD_OR_RELATION_UNISSUED")
    if scope.get("sample_pooling_state") != "NO_SOURCE_POOLING":
        raise UncertainRepertoireError("POPULATION_BRIDGE_MUST_NOT_POOL_SAMPLES")
    return {
        "authority_ref": bridge_ref.as_dict(),
        "target_population_ref": common.as_dict(),
        "population_period": period,
        "population_bridge_kind": BRIDGE_KIND,
        "sample_pooling_state": "NO_SOURCE_POOLING",
    }


def _interval(lo: Fraction, hi: Fraction) -> dict[str, dict[str, int]]:
    if lo > hi or lo < 0 or hi > 1:
        raise UncertainRepertoireError("IMPOSSIBLE_CONFIGURATION_INTERVAL")
    return {"lower": _fraction(lo), "upper": _fraction(hi)}


def _coupling(a: Fraction, b: Fraction, joint: Fraction) -> dict[str, dict[str, int]]:
    cells = {
        "A_AND_B": joint,
        "A_ONLY": a-joint,
        "B_ONLY": b-joint,
        "NEITHER": 1-a-b+joint,
    }
    if sum(cells.values()) != 1 or any(v < 0 for v in cells.values()):
        raise UncertainRepertoireError("INTERNAL_COUPLING_NOT_A_PROBABILITY")
    return {k: _fraction(v) for k,v in cells.items()}


def identify_uncertain_unobserved_overlap(
    *,
    left: S04ObservedKnowledge,
    right: S04ObservedKnowledge,
    left_event_cell: Any,
    right_event_cell: Any,
    registry: AuthorityRegistry | None = None,
    left_interval_authority: AuthorityRef | None = None,
    right_interval_authority: AuthorityRef | None = None,
    common_population_authority: AuthorityRef | None = None,
) -> UncertainRepertoire:
    """Sharply project the 2x2 feasible set, conditional on issued premises."""
    l, _ = _marginal(left, positive_cell=left_event_cell, label="LEFT")
    r, _ = _marginal(right, positive_cell=right_event_cell, label="RIGHT")
    if (left.ref == right.ref
            or exact_ref(l["release_ref"]) == exact_ref(r["release_ref"])
            or exact_ref(l["source_universe_ref"]) == exact_ref(r["source_universe_ref"])):
        raise UncertainRepertoireError("SAME_SOURCE_USE_RESPONDENT_LEVEL_I03_JOINT")
    base = {
        "contract": CONTRACT,
        "marginal_left": l,
        "marginal_right": r,
        "state": "HELD_ISSUED_POPULATION_INTERVALS_OR_BRIDGE_MISSING",
        "hold_reason": "MISSING_EXACT_AUTHORITIES",
        "left_issued_population_interval": None,
        "right_issued_population_interval": None,
        "common_population": None,
        "bounds": None,
        "simultaneous_coverage_lower_bound": None,
        "witness_couplings": None,
        "no_new_i03_query": True,
        "unissued": list(UNISSUED),
    }
    if (registry is None or left_interval_authority is None
            or right_interval_authority is None or common_population_authority is None):
        return _seal(base)
    if type(registry) is not AuthorityRegistry:
        raise UncertainRepertoireError("EXACT_AUTHORITY_REGISTRY_REQUIRED")
    try:
        li, al, au, alpha = _scope_for_source(
            l, registry, left_interval_authority, "LEFT"
        )
        ri, bl, bu, beta = _scope_for_source(
            r, registry, right_interval_authority, "RIGHT"
        )
        bridge = _common_population(
            l, r, li, ri, registry, common_population_authority
        )
    except (UncertainRepertoireError, Pre553AuthorityError,
            Pre553IntegrityError, TypeError, ValueError, KeyError) as exc:
        return _seal({
            **base, "hold_reason": (
                str(exc) if isinstance(exc, (UncertainRepertoireError, Pre553AuthorityError))
                else "INVALID_OR_STALE_EXACT_POPULATION_AUTHORITY"
            ),
        })
    lower = max(Fraction(0), al+bl-1)
    upper = min(au, bu)
    bounds = {
        "A_AND_B": _interval(lower, upper),
        "A_ONLY": _interval(max(Fraction(0), al-bu), min(au, 1-bl)),
        "B_ONLY": _interval(max(Fraction(0), bl-au), min(bu, 1-al)),
        "NEITHER": _interval(max(Fraction(0), 1-au-bu), min(1-al, 1-bl)),
    }
    # Extremal witnesses prove sharpness of the *A_AND_B* projection.
    # They are population probability configurations, never respondents.
    witnesses = {
        "MIN_A_AND_B": {
            "a_marginal": _fraction(al), "b_marginal": _fraction(bl),
            "cells": _coupling(al, bl, lower),
        },
        "MAX_A_AND_B": {
            "a_marginal": _fraction(au), "b_marginal": _fraction(bu),
            "cells": _coupling(au, bu, upper),
        },
    }
    simultaneous = max(Fraction(0), 1-alpha-beta)
    return _seal({
        **base,
        "state": "SHARP_PARTIAL_ID_UNDER_ISSUED_POPULATION_INTERVALS",
        "hold_reason": None,
        "grade": GRADE,
        "left_issued_population_interval": li,
        "right_issued_population_interval": ri,
        "common_population": bridge,
        "bounds": bounds,
        "witness_couplings": witnesses,
        "simultaneous_coverage_lower_bound": _fraction(simultaneous),
        "coverage_rule": (
            "BOOLE_UNION_BOUND_FROM_BOTH_ISSUED_MARGINAL_GUARANTEES"
            "__NOT_INDEPENDENCE_OR_NEW_VARIANCE_ESTIMATE"
        ),
        "selected_coupling": None,
        "population_joint_point_estimate": None,
    })


def replay_uncertain_unobserved_overlap(
    *,
    receipt: UncertainRepertoire,
    left: S04ObservedKnowledge,
    right: S04ObservedKnowledge,
    left_event_cell: Any,
    right_event_cell: Any,
    registry: AuthorityRegistry | None = None,
    left_interval_authority: AuthorityRef | None = None,
    right_interval_authority: AuthorityRef | None = None,
    common_population_authority: AuthorityRef | None = None,
) -> UncertainRepertoire:
    """Cold source-and-issuer replay: rehashing a counterfeit cannot issue it."""
    if type(receipt) is not UncertainRepertoire:
        raise UncertainRepertoireError("EXACT_UNCERTAIN_REPERTOIRE_RECEIPT_REQUIRED")
    rebuilt = identify_uncertain_unobserved_overlap(
        left=left, right=right,
        left_event_cell=left_event_cell, right_event_cell=right_event_cell,
        registry=registry,
        left_interval_authority=left_interval_authority,
        right_interval_authority=right_interval_authority,
        common_population_authority=common_population_authority,
    )
    if rebuilt.ref != receipt.ref:
        raise UncertainRepertoireError("UNCERTAIN_REPERTOIRE_SOURCE_REPLAY_FAILED")
    return rebuilt


def ask_uncertain_repertoire_configuration(
    *,
    relation: UncertainRepertoire,
    left: S04ObservedKnowledge,
    right: S04ObservedKnowledge,
    left_event_cell: Any,
    right_event_cell: Any,
    event_a: bool,
    event_b: bool,
    registry: AuthorityRegistry | None = None,
    left_interval_authority: AuthorityRef | None = None,
    right_interval_authority: AuthorityRef | None = None,
    common_population_authority: AuthorityRef | None = None,
) -> dict[str, Any]:
    """A source-replayed compatibility constraint; never a person sampler."""
    if type(event_a) is not bool or type(event_b) is not bool:
        raise UncertainRepertoireError("EXACT_BINARY_PROPOSITION_FLAGS_REQUIRED")
    replay_uncertain_unobserved_overlap(
        receipt=relation, left=left, right=right,
        left_event_cell=left_event_cell, right_event_cell=right_event_cell,
        registry=registry,
        left_interval_authority=left_interval_authority,
        right_interval_authority=right_interval_authority,
        common_population_authority=common_population_authority,
    )
    m = relation.material()
    key = ("A_AND_B" if event_a and event_b else
           "A_ONLY" if event_a else
           "B_ONLY" if event_b else "NEITHER")
    base = {
        "contract": "S04_UNCERTAIN_REPERTOIRE_CONFIGURATION_CONSTRAINT@1",
        "relation_ref": relation.ref.as_dict(),
        "event_a": event_a,
        "event_b": event_b,
        "requested_configuration": key,
        "selected_coupling": None,
        "person_or_respondent_created": False,
        "interval": None,
    }
    if m["state"] != "SHARP_PARTIAL_ID_UNDER_ISSUED_POPULATION_INTERVALS":
        return {**base, "state": "HELD_NOT_AN_IMPOSSIBLE_PERSON_CLAIM"}
    return {
        **base,
        "state": "QUALIFIED_PARAMETER_COMPATIBILITY_INTERVAL",
        "interval": m["bounds"][key],
        "simultaneous_coverage_lower_bound": m["simultaneous_coverage_lower_bound"],
        "not_an_observed_joint": True,
    }


__all__ = [
    "CONTRACT", "INTERVAL_OPERATION", "BRIDGE_OPERATION", "INTERVAL_COVERAGE",
    "BRIDGE_KIND", "GRADE", "UNISSUED", "UncertainRepertoireError",
    "UncertainRepertoire", "identify_uncertain_unobserved_overlap",
    "replay_uncertain_unobserved_overlap", "ask_uncertain_repertoire_configuration",
]
