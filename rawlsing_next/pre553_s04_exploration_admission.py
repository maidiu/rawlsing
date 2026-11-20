"""Conservative information/cost admission for *search*, not scientific truth.

Prevents positive finite-sample mutual information at a tiny node from
automatically branching across all source-observed category combinations.

For categorical X and Y, description-length-inspired screening uses
 n * I(Y;X|D) - ((states(X)-1)*(states(Y)-1)/2)*log2(n) - log2(m)
in bits, with m including the queried singles/pairs and previously pursued
search branches. It is only a discovery-routing heuristic: cannot certify
statistical inference, model assumptions, independence, causal mechanisms,
survey-design variance or population estimates.

The raw source observed joint/alternatives are retained regardless of a
negative routing outcome. No source-dependent ungoverned sampling occurs.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from math import log2, prod
from typing import Any, Mapping, Sequence

SCREEN_CONTRACT = "PYAT_S04_SOURCE_SAMPLE_EXPLORATION_ADMISSION@1"


class ExplorationAdmissionError(ValueError):
    pass


def _finite_nonnegative(value: Any) -> Decimal:
    try:
        x = Decimal(str(value))
    except (InvalidOperation, ValueError) as e:
        raise ExplorationAdmissionError("INVALID_INFORMATION_BITS") from e
    if not x.is_finite() or x < 0:
        raise ExplorationAdmissionError("NEGATIVE_OR_NONFINITE_INFORMATION")
    return x


@dataclass(frozen=True)
class SearchEvidence:
    common_case_n: int
    target_observed_states: int
    joint_predictor_observed_states: int
    information_bits: Any
    candidate_family_size: int
    previous_search_nodes: int

    def __post_init__(self) -> None:
        for x in (self.common_case_n, self.target_observed_states,
                  self.joint_predictor_observed_states,
                  self.candidate_family_size, self.previous_search_nodes):
            if type(x) is not int or x < 0:
                raise ExplorationAdmissionError("INVALID_SOURCE_RISK_OR_COMPLEXITY")
        _finite_nonnegative(self.information_bits)


def route_exploratory_split(evidence: SearchEvidence) -> dict[str, Any]:
    if type(evidence) is not SearchEvidence:
        raise ExplorationAdmissionError("TYPED_SEARCH_EVIDENCE_REQUIRED")
    n = evidence.common_case_n
    df = max(0, evidence.target_observed_states - 1) * max(
        0, evidence.joint_predictor_observed_states - 1)
    family = max(1, evidence.candidate_family_size)
    # Repeatedly visited contexts do not receive a fresh free alpha/bit
    # budget. This is a *minimum* complexity accounting rather than a
    # validated sequential familywise-error correction.
    exposure = family * max(1, evidence.previous_search_nodes + 1)
    info = _finite_nonnegative(evidence.information_bits)
    raw_gain = Decimal(n) * info
    model_cost = Decimal(str(df * log2(n) / 2)) if n > 1 else Decimal(0)
    selection_cost = Decimal(str(log2(exposure)))
    net = raw_gain - model_cost - selection_cost
    # Too few observations for the effective model dimensions? Preserve
    # diagnostic interest, but don't automatically recurse on memorization.
    underspecified = n < max(8, 2 * df + 2)
    admitted = bool(df > 0 and n > 0 and not underspecified and net > 0)
    return {
        "contract": SCREEN_CONTRACT,
        "sample_n": n,
        "target_observed_states": evidence.target_observed_states,
        "joint_predictor_observed_states": evidence.joint_predictor_observed_states,
        "model_degrees_of_freedom": df,
        "declared_candidate_family_size": family,
        "sequential_search_exposure_floor": exposure,
        "raw_information_bits_per_respondent": info,
        "raw_total_information_bits": raw_gain,
        "complexity_codelength_bits": model_cost,
        "multiple_inquiries_codelength_bits": selection_cost,
        "net_search_codelength_bits": net,
        "too_sparse_for_automatic_recursion": underspecified,
        "admit_automatic_recursion": admitted,
        "grade": (
            "PROVISIONAL_SOURCE_SAMPLE_ROUTING_NOT_INFERENTIAL_APPROVAL"
            if admitted else "DIAGNOSTIC_ONLY_OR_NO_NET_DISCOVERY_GAIN"
        ),
        "estimator_bias_not_removed_from_source_MI": True,
        "survey_design_qualification": "NOT_ISSUED",
        "source_observed_alternatives_preserved": True,
    }


def source_observed_group_states(
    *, positive_cells: Sequence[tuple[tuple[Any, ...], int]],
    target_axis: int, predictor_axes: Sequence[int],
) -> tuple[int, int, int]:
    """Count nonzero states in actual respondent-coherent selected risk."""
    if not positive_cells:
        return 0, 0, 0
    if not predictor_axes or len(set(predictor_axes)) != len(predictor_axes):
        raise ExplorationAdmissionError("SOURCE_PREDICTOR_GROUP_INVALID")
    arity = len(positive_cells[0][0])
    if (not 0 <= target_axis < arity
            or any(type(a) is not int or not 0 <= a < arity
                   for a in predictor_axes)
            or target_axis in predictor_axes):
        raise ExplorationAdmissionError("SOURCE_AXIS_INVALID")
    y, x, n = set(), set(), 0
    for row, count in positive_cells:
        if len(row) != arity or type(count) is not int or count < 0:
            raise ExplorationAdmissionError("SOURCE_JOINT_INCONSISTENT")
        if count == 0:
            continue
        from rawlsing_next.pre553_empirical_objects import canonical_json
        y.add(canonical_json(row[target_axis]))
        x.add(canonical_json(tuple(row[a] for a in predictor_axes)))
        n += count
    return n, len(y), len(x)
