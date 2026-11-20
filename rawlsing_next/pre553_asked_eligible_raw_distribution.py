"""Reusable asked-eligible RAW response distribution policy on EXISTING I03.

The denominator is proven condition-true respondents who have exact,
authority-validated ELIGIBLE_APPLICABLE routing for the target. This module
does not infer administration from non-null responses, create routing facts,
decode an original survey, or issue source/science permission.

SUBSTANTIVE, DK, REFUSAL, source-declared MISSING/no recorded answer, and
SOURCE_SPECIFIC_SPECIAL are distinct target outcomes. A respondent with
no event is still in the asked denominator if routing proves eligibility,
but is UNRESOLVED: absence does not manufacture a "MISSING" response event.

The same profile applies to each scalar component of unary/conditional/
same-respondent joint RAW I03 queries. Other topologies retain their
already-governed native semantics; no covert scalar collapse.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, EmpiricalQuerySpec, canonical_json, canonicalize,
    exact_ref,
)

POLICY = "ASKED_ELIGIBLE_RAW_DISTRIBUTION@1"
STATE_SET = (
    "SUBSTANTIVE_RESPONSE",
    "MISSING",
    "DK",
    "REFUSAL",
    "SOURCE_SPECIFIC_SPECIAL",
)
SPECIAL = STATE_SET[1:]
PROFILE_FIELD = "descriptive_denominator_policy"


class AskedEligibleDistributionError(ValueError):
    """Source or query lacks the exact proof required by this profile."""


def typed_state_cell(state: str) -> dict[str, str]:
    if type(state) is not str or state not in SPECIAL:
        raise AskedEligibleDistributionError("NONANSWER_STATE_NOT_ISSUED")
    return {"typed_response_state": state}


def include_asked_eligible_states(
    component: Mapping[str, Any],
) -> dict[str, Any]:
    """Prepare an existing source-issuer component; does NOT issue a query.

    The initial domain must be source-authenticated SUBSTANTIVE values.
    Explicit nonresponse classes are added as typed, disjoint cells. A
    verified source codebook/routing mapper must still type the actual
    physical event (e.g. 98 as DK); this function never guesses code values.
    """
    if not isinstance(component, Mapping):
        raise AskedEligibleDistributionError("SOURCE_COMPONENT_REQUIRED")
    if component.get("topology") != "SCALAR_SINGULAR":
        raise AskedEligibleDistributionError("SCALAR_SINGULAR_TARGET_REQUIRED")
    original_states = component.get("included_states")
    if not isinstance(original_states, (tuple, list)) or list(original_states) != [
        "SUBSTANTIVE_RESPONSE"
    ]:
        raise AskedEligibleDistributionError(
            "SOURCE_COMPONENT_NOT_SUBSTANTIVE_ONLY_BEFORE_POLICY"
        )
    domain = component.get("domain")
    if not isinstance(domain, (tuple, list)):
        raise AskedEligibleDistributionError("EXACT_SOURCE_SUBSTANTIVE_DOMAIN_REQUIRED")
    # A legitimately asked question can have no substantive answers.
    # In that case the typed DK/refusal/missing outcomes still form a
    # nonempty and fully accountable I03 target domain.
    values = [canonicalize(x) for x in domain]
    if any(isinstance(v, Mapping) and "typed_response_state" in v for v in values):
        raise AskedEligibleDistributionError(
            "SUBSTANTIVE_DOMAIN_COLLIDES_WITH_TYPED_NONANSWER"
        )
    full = values + [typed_state_cell(s) for s in SPECIAL]
    if len({canonical_json(v) for v in full}) != len(full):
        raise AskedEligibleDistributionError("DUPLICATE_SOURCE_RESPONSE_DOMAIN")
    return {
        **dict(component),
        "domain": full,
        "included_states": list(STATE_SET),
    }


def enforce_asked_eligible_query_shape(
    *,
    measure: str,
    topology: str,
    included_states: frozenset[str],
    domain: Sequence[Any],
) -> None:
    """I03's own parser calls this when an issuer claims POLICY.

    The policy cannot be a cosmetic label concealing a denominator that
    counts only substantive respondents. Unknown/missing admin remains
    I03's existing typed source-side refusal/held state.
    """
    if measure != "RAW":
        raise AskedEligibleDistributionError("ASKED_ELIGIBLE_REQUIRES_RAW_MEASURE")
    if topology != "SCALAR_SINGULAR":
        raise AskedEligibleDistributionError(
            "ASKED_ELIGIBLE_UNSUPPORTED_TARGET_TOPOLOGY"
        )
    if included_states != frozenset(STATE_SET):
        raise AskedEligibleDistributionError(
            "ASKED_ELIGIBLE_MUST_INCLUDE_ALL_DOCUMENTED_NONANSWER_STATES"
        )
    keys = [canonical_json(canonicalize(x)) for x in domain]
    for state in SPECIAL:
        if canonical_json(typed_state_cell(state)) not in keys:
            raise AskedEligibleDistributionError(
                "ASKED_ELIGIBLE_DECLARED_DOMAIN_MISSING_NONANSWER_CELL"
            )


def summarize_asked_eligible_raw_fact(
    *,
    query: EmpiricalQuerySpec,
    fact: EmpiricalFact,
) -> dict[str, Any]:
    """Read a real, already-executed I03 fact; NEVER recompute respondents.

    A positive result reports both denominators. Anything partially
    resolved remains HELD, with no promoted probability/cell statistics.
    This function does not authenticate issuer competence on its own;
    the caller must retain the native I03 execution and replay chain.
    """
    if type(query) is not EmpiricalQuerySpec or type(fact) is not EmpiricalFact:
        raise AskedEligibleDistributionError("EXACT_I03_QUERY_AND_FACT_REQUIRED")
    if (query.requested_output_grain.get(PROFILE_FIELD) != POLICY
            or query.requested_output_grain.get("measure_kind") != "RAW"):
        raise AskedEligibleDistributionError("NOT_AN_ASKED_ELIGIBLE_RAW_QUERY")
    # CanonicalSemanticObject freezes its semantic refs as *mappings*,
    # while query.ref is a live ExactRef. Compare reconstructed identities,
    # never unequal raw representation types.
    if exact_ref(fact.empirical_query_spec_ref) != query.ref:
        raise AskedEligibleDistributionError("FACT_QUERY_IDENTITY_MISMATCH")
    if (exact_ref(fact.risk_set_ref) != exact_ref(query.risk_set_ref)
            or exact_ref(fact.response_state_semantics_ref)
            != exact_ref(query.requested_output_grain[
                "response_state_semantics_ref"
            ])):
        raise AskedEligibleDistributionError("FACT_SOURCE_RISK_OR_SEMANTICS_MISMATCH")
    if len(query.target_refs) != 1 or fact.target_topology["arity"] != 1:
        raise AskedEligibleDistributionError(
            "SUMMARY_REQUIRES_SINGLE_TARGET__JOINT_I03_REMAINS_UNCHANGED"
        )
    n = fact.raw_numerator_support
    d = fact.raw_denominator_support
    result = {
        "contract": POLICY,
        "query_ref": query.ref.as_dict(),
        "fact_ref": fact.ref.as_dict(),
        "risk_set_ref": exact_ref(fact.risk_set_ref).as_dict(),
        "denominator_definition": (
            "KNOWN_CONDITION_TRUE_AND_ROUTING_ELIGIBLE__"
            "DO_NOT_INFER_ASKED_FROM_RECORDED_RESPONSE"
        ),
        "known_condition_true_risk_n": d,
        "resolved_target_event_n": n,
        "source_fact_state": fact.typed_state,
        "asked_eligible_n": None,
        "substantive_response_n": None,
        "source_typed_response_counts": None,
        "substantive_only_denominator_n": None,
        "raw_asked_share": None,
        "raw_substantive_share": None,
        "population_inference": None,
        "weighting": "NONE_RAW",
    }
    if fact.typed_state != "SUPPORTED":
        result["state"] = "UPSTREAM_HELD__NO_COMPLETE_DISTRIBUTION"
        return result
    if d <= 0 or n != d:
        raise AskedEligibleDistributionError(
            "SUPPORTED_COMPLETE_ASKED_RISK_REQUIRES_RESOLVED_EQUALS_ELIGIBLE"
        )
    rows = fact.target_topology["complete_cell_semantic_projection"]
    counts: list[dict[str, Any]] = []
    total = substantive = 0
    seen = set()
    for row in rows:
        cell = canonicalize(row["cell"])
        key = canonical_json(cell)
        if key in seen:
            raise AskedEligibleDistributionError("DUPLICATE_I03_CELL")
        seen.add(key)
        count = row["raw_numerator_support"]
        if type(count) is not int or count < 0:
            raise AskedEligibleDistributionError("INVALID_I03_CELL_COUNT")
        total += count
        if isinstance(cell, Mapping):
            if set(cell) != {"typed_response_state"} or cell["typed_response_state"] not in SPECIAL:
                raise AskedEligibleDistributionError("UNISSUED_TARGET_NONANSWER_CELL")
            state = cell["typed_response_state"]
        else:
            state = "SUBSTANTIVE_RESPONSE"
            substantive += count
        counts.append({
            "response_state": state,
            "exact_target_cell": cell,
            "raw_n": count,
            "asked_share_exact": {"numerator": count, "denominator": d},
            "substantive_share_exact": (
                {"numerator": count, "denominator": None}
                if state == "SUBSTANTIVE_RESPONSE" else None
            ),
        })
    if total != d:
        raise AskedEligibleDistributionError("I03_CELL_SUM_DISAGREES_WITH_ASKED_RISK")
    for item in counts:
        if item["response_state"] == "SUBSTANTIVE_RESPONSE":
            item["substantive_share_exact"] = (
                {"numerator": item["raw_n"], "denominator": substantive}
                if substantive else None
            )
    result.update({
        "state": "SOURCE_COHERENT_RAW_ASKED_ELIGIBLE_DISTRIBUTION",
        "asked_eligible_n": d,
        "substantive_response_n": substantive,
        "source_typed_response_counts": counts,
        "substantive_only_denominator_n": substantive,
        "raw_asked_share": "EXACT_NUMERATOR_OVER_ASKED_ELIGIBLE",
        "raw_substantive_share": (
            "EXACT_NUMERATOR_OVER_SUBSTANTIVE_ONLY"
            if substantive else "NO_SUBSTANTIVE_RESPONSES"
        ),
    })
    return result


__all__ = [
    "POLICY", "PROFILE_FIELD", "STATE_SET", "SPECIAL",
    "AskedEligibleDistributionError", "typed_state_cell",
    "include_asked_eligible_states", "enforce_asked_eligible_query_shape",
    "summarize_asked_eligible_raw_fact",
]
