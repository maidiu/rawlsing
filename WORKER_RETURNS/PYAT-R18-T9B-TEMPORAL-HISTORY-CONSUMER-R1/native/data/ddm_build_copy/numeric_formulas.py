#!/usr/bin/env python3
"""Numeric-first score helpers used by the registry and V550 companions."""

from __future__ import annotations

import math
from collections.abc import Iterable
from typing import Any

from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP, support_status_from_count, support_threshold_from_total


SUPPORT_FORMULA_ID = "support_score_v1"
SUPPORT_FORMULA_VERSION = "v1"
SUPPORT_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.support_score_v1"
SUPPORT_SCORE_FAMILY = "support_adequacy"
SUPPORT_HIGHEST_BETTER = True
SUPPORT_DECISION_ROLE = "eligibility"

PREVALENCE_FORMULA_ID = "prevalence_score_v1"
PREVALENCE_FORMULA_VERSION = "v1"
PREVALENCE_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.prevalence_score_v1"
PREVALENCE_SCORE_FAMILY = "prevalence"
PREVALENCE_HIGHEST_BETTER = True
PREVALENCE_DECISION_ROLE = "context"

CONFIDENCE_FORMULA_ID = "confidence_score_v1"
CONFIDENCE_FORMULA_VERSION = "v1"
CONFIDENCE_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.confidence_score_v1"
CONFIDENCE_SCORE_FAMILY = "confidence"
CONFIDENCE_HIGHEST_BETTER = True
CONFIDENCE_DECISION_ROLE = "routing_and_display"

WEIGHT_VALIDITY_FORMULA_ID = "weight_validity_score_v1"
WEIGHT_VALIDITY_FORMULA_VERSION = "v1"
WEIGHT_VALIDITY_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.weight_validity_score_v1"
WEIGHT_VALIDITY_SCORE_FAMILY = "support_adequacy"
WEIGHT_VALIDITY_HIGHEST_BETTER = True
WEIGHT_VALIDITY_DECISION_ROLE = "eligibility"

PATTERN_PROBABILITY_FORMULA_ID = "pattern_probability_v1"
PATTERN_PROBABILITY_FORMULA_VERSION = "v1"
PATTERN_PROBABILITY_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.pattern_probability_v1"
PATTERN_PROBABILITY_SCORE_FAMILY = "prevalence"
PATTERN_PROBABILITY_HIGHEST_BETTER = True
PATTERN_PROBABILITY_DECISION_ROLE = "context"

COMPLETION_RATE_FORMULA_ID = "completion_rate_v1"
COMPLETION_RATE_FORMULA_VERSION = "v1"
COMPLETION_RATE_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.completion_rate_v1"
COMPLETION_RATE_SCORE_FAMILY = "prevalence"
COMPLETION_RATE_HIGHEST_BETTER = True
COMPLETION_RATE_DECISION_ROLE = "context"

MISSINGNESS_RATE_FORMULA_ID = "missingness_rate_v1"
MISSINGNESS_RATE_FORMULA_VERSION = "v1"
MISSINGNESS_RATE_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.missingness_rate_v1"
MISSINGNESS_RATE_SCORE_FAMILY = "risk_penalty"
MISSINGNESS_RATE_HIGHEST_BETTER = False
MISSINGNESS_RATE_DECISION_ROLE = "penalty"

EFFECTIVE_N_FORMULA_ID = "effective_n_v1"
EFFECTIVE_N_FORMULA_VERSION = "v1"
EFFECTIVE_N_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.effective_n_v1"
EFFECTIVE_N_SCORE_FAMILY = "confidence"
EFFECTIVE_N_HIGHEST_BETTER = True
EFFECTIVE_N_DECISION_ROLE = "context"

EFFECTIVE_N_RATIO_FORMULA_ID = "effective_n_ratio_v1"
EFFECTIVE_N_RATIO_FORMULA_VERSION = "v1"
EFFECTIVE_N_RATIO_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.effective_n_ratio_v1"
EFFECTIVE_N_RATIO_SCORE_FAMILY = "confidence"
EFFECTIVE_N_RATIO_HIGHEST_BETTER = True
EFFECTIVE_N_RATIO_DECISION_ROLE = "context"

JOINT_PATTERN_CONFIDENCE_FORMULA_ID = "joint_pattern_confidence_score_v1"
JOINT_PATTERN_CONFIDENCE_FORMULA_VERSION = "v1"
JOINT_PATTERN_CONFIDENCE_IMPLEMENTATION_FUNCTION = "data.ddm_build_copy.numeric_formulas.joint_pattern_confidence_score_v1"
JOINT_PATTERN_CONFIDENCE_SCORE_FAMILY = "confidence"
JOINT_PATTERN_CONFIDENCE_HIGHEST_BETTER = True
JOINT_PATTERN_CONFIDENCE_DECISION_ROLE = "routing_and_display"


def _to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        parsed = float(value)
        if math.isnan(parsed) or math.isinf(parsed):
            return None
        return parsed
    except Exception:
        return None


def _clamp(value: float | None, lower: float, upper: float) -> float | None:
    if value is None:
        return None
    return float(max(lower, min(upper, value)))


def _sign(value: float | None) -> float | None:
    if value is None:
        return None
    if value > 0:
        return 1.0
    if value < 0:
        return -1.0
    return 0.0


def weighted_mean(values: Iterable[Any], weights: Iterable[Any] | None = None) -> float | None:
    parsed_values = [_to_float(value) for value in values]
    if any(value is None for value in parsed_values):
        return None
    if weights is None:
        return sum(parsed_values) / len(parsed_values) if parsed_values else None
    parsed_weights = [_to_float(value) for value in weights]
    if len(parsed_weights) != len(parsed_values) or any(weight is None for weight in parsed_weights):
        return None
    weight_sum = sum(parsed_weights)
    if weight_sum <= 0:
        return None
    return sum(value * weight for value, weight in zip(parsed_values, parsed_weights)) / weight_sum


def support_score_v1(support_ratio: Any, support_ratio_margin: Any) -> float | None:
    ratio = _to_float(support_ratio)
    margin = _to_float(support_ratio_margin)
    if ratio is None or margin is None:
        return None
    return _clamp(100.0 * min(1.0, ratio) + 10.0 * _sign(margin), 0.0, 100.0)


def prevalence_score_v1(population_share: Any) -> float | None:
    share = _to_float(population_share)
    if share is None:
        return None
    return _clamp(100.0 * share, 0.0, 100.0)


def confidence_score_v1(
    confidence_component_support: Any,
    confidence_component_mapping: Any,
    confidence_component_directionality: Any,
    confidence_component_weight: Any,
    confidence_component_missingness: Any,
) -> float | None:
    score = weighted_mean(
        [
            confidence_component_support,
            confidence_component_mapping,
            confidence_component_directionality,
            confidence_component_weight,
            confidence_component_missingness,
        ]
    )
    if score is None:
        return None
    return _clamp(score, 0.0, 100.0)


def pattern_probability_v1(pattern_share: Any) -> float | None:
    share = _to_float(pattern_share)
    if share is None:
        return None
    return _clamp(share, 0.0, 1.0)


def completion_rate_v1(n_items_answered: Any, n_family_items: Any) -> float | None:
    answered = _to_float(n_items_answered)
    family_items = _to_float(n_family_items)
    if answered is None or family_items is None or family_items <= 0:
        return None
    return _clamp(answered / family_items, 0.0, 1.0)


def missingness_rate_v1(completion_rate: Any) -> float | None:
    completed = _to_float(completion_rate)
    if completed is None:
        return None
    return _clamp(1.0 - completed, 0.0, 1.0)


def effective_n_v1(sum_weights: Any, sum_weight_squares: Any) -> float | None:
    total = _to_float(sum_weights)
    total_squares = _to_float(sum_weight_squares)
    if total is None or total_squares is None or total_squares <= 0:
        return None
    return _clamp((total * total) / total_squares, 0.0, float("inf"))


def effective_n_ratio_v1(effective_n: Any, n_unweighted: Any) -> float | None:
    eff = _to_float(effective_n)
    count = _to_float(n_unweighted)
    if eff is None or count is None or count <= 0:
        return None
    return _clamp(eff / count, 0.0, 1.0)


def weight_validity_score_v1(
    weight_nonnull_ratio: Any,
    weight_positive_ratio: Any,
    weight_variability_score: Any,
    weight_concentration_risk_score: Any,
    effective_n_ratio: Any,
) -> float | None:
    values = [
        _to_float(weight_nonnull_ratio),
        _to_float(weight_positive_ratio),
        _to_float(weight_variability_score),
        _to_float(weight_concentration_risk_score),
        _to_float(effective_n_ratio),
    ]
    if any(value is None for value in values):
        return None
    nonnull, positive, variability, concentration_risk, eff_ratio = values
    score = (nonnull + positive + variability + (1.0 - concentration_risk) + eff_ratio) / 5.0
    return _clamp(100.0 * score, 0.0, 100.0)


def joint_pattern_confidence_score_v1(
    support_ratio: Any,
    completion_rate: Any,
    effective_n_ratio: Any,
    pattern_probability: Any,
) -> float | None:
    values = [_to_float(support_ratio), _to_float(completion_rate), _to_float(effective_n_ratio), _to_float(pattern_probability)]
    if any(value is None for value in values):
        return None
    support_ratio_value, completion_rate_value, effective_n_ratio_value, pattern_probability_value = values
    support_component = min(1.0, support_ratio_value)
    score = (support_component + completion_rate_value + effective_n_ratio_value + pattern_probability_value) / 4.0
    return _clamp(100.0 * score, 0.0, 100.0)


def support_gate_status_from_count(
    support_count: Any,
    *,
    total_respondents: Any = None,
    lane: str = "relation",
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_rate: float = 0.005,
    support_floor: int = 1,
) -> str:
    support_status = support_status_from_count(
        support_count,
        total_respondents=total_respondents,
        lane=lane,
        support_rate=support_rate,
        support_cap=support_cap,
        support_floor=support_floor,
    )
    if support_status == "sufficient_support":
        return "clears_threshold"
    if support_status == "underpowered":
        return "below_threshold"
    return support_status


def support_ratio_from_count(
    support_count: Any,
    *,
    total_respondents: Any = None,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_rate: float = 0.005,
    support_floor: int = 1,
) -> float | None:
    support = _to_float(support_count)
    if support is None:
        return None
    threshold = support_threshold_from_total(
        total_respondents,
        support_rate=support_rate,
        support_cap=support_cap,
        support_floor=support_floor,
    )
    if threshold <= 0:
        return None
    return float(support / float(threshold))


def support_ratio_margin_from_count(
    support_count: Any,
    *,
    total_respondents: Any = None,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_rate: float = 0.005,
    support_floor: int = 1,
) -> float | None:
    ratio = support_ratio_from_count(
        support_count,
        total_respondents=total_respondents,
        support_cap=support_cap,
        support_rate=support_rate,
        support_floor=support_floor,
    )
    if ratio is None:
        return None
    return float(ratio - 1.0)


def population_share_from_count(support_count: Any, *, total_respondents: Any = None) -> float | None:
    support = _to_float(support_count)
    total = _to_float(total_respondents)
    if support is None or total is None or total <= 0:
        return None
    return float(support / total)


def support_prevalence_companions(
    support_count: Any,
    *,
    total_respondents: Any = None,
    lane: str = "relation",
    support_cap: int = DEFAULT_SUPPORT_CAP,
) -> dict[str, Any]:
    support_count_value = _to_float(support_count)
    support_threshold = support_threshold_from_total(total_respondents, support_cap=support_cap)
    support_ratio = support_ratio_from_count(
        support_count_value,
        total_respondents=total_respondents,
        support_cap=support_cap,
    )
    support_ratio_margin = None if support_ratio is None else float(support_ratio - 1.0)
    population_share = population_share_from_count(support_count_value, total_respondents=total_respondents)
    support_status = support_status_from_count(
        support_count_value,
        total_respondents=total_respondents,
        lane=lane,
        support_cap=support_cap,
    )
    return {
        "support_threshold": int(support_threshold),
        "support_status": support_status,
        "support_gate_status": support_gate_status_from_count(
            support_count_value,
            total_respondents=total_respondents,
            lane=lane,
            support_cap=support_cap,
        ),
        "support_ratio": support_ratio,
        "support_ratio_margin": support_ratio_margin,
        "support_score": support_score_v1(support_ratio, support_ratio_margin),
        "support_formula_id": SUPPORT_FORMULA_ID,
        "support_formula_version": SUPPORT_FORMULA_VERSION,
        "support_implementation_function": SUPPORT_IMPLEMENTATION_FUNCTION,
        "support_score_family": SUPPORT_SCORE_FAMILY,
        "support_higher_is_better": SUPPORT_HIGHEST_BETTER,
        "support_decision_role": SUPPORT_DECISION_ROLE,
        "population_share": population_share,
        "prevalence_score": prevalence_score_v1(population_share),
        "prevalence_formula_id": PREVALENCE_FORMULA_ID,
        "prevalence_formula_version": PREVALENCE_FORMULA_VERSION,
        "prevalence_implementation_function": PREVALENCE_IMPLEMENTATION_FUNCTION,
        "prevalence_score_family": PREVALENCE_SCORE_FAMILY,
        "prevalence_higher_is_better": PREVALENCE_HIGHEST_BETTER,
        "prevalence_decision_role": PREVALENCE_DECISION_ROLE,
    }
