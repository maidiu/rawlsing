"""Population-relative support policy for the country-scoped S04/DHIKR cycle.

Preserves every exact observed positive source cell. Separates:
  1. observation existence (n > 0);
  2. exploratory eligibility (country-question-relative threshold OR
     exceptional locally contrasting minority);
  3. *candidate* inference review (a higher support threshold, never proof).

No percentage/number alone supplies scientific certainty. The default curves
are provisional engineering choices reviving V550's relative support method;
complex-survey variance, missingness, weight/design, multiplicity and source
permissions remain separate. Crucially N is the COUNTRY-QUESTION exact
eligible common-case population, never the pooled multi-country survey.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from typing import Any, Mapping, Sequence


class AdaptiveSupportError(ValueError):
    pass


def _rate(text: str) -> Decimal:
    if not isinstance(text, str):
        raise AdaptiveSupportError("SUPPORT_RATE_MUST_BE_DECIMAL_STRING")
    try:
        d = Decimal(text)
    except InvalidOperation as exc:
        raise AdaptiveSupportError("INVALID_SUPPORT_RATE") from exc
    if not d.is_finite() or not Decimal(0) <= d <= Decimal(1):
        raise AdaptiveSupportError("INVALID_SUPPORT_RATE")
    return d


@dataclass(frozen=True)
class AdaptiveSupportPolicy:
    """Sourcefree provisional coefficients, explicit and independently tuned.

    Default exploration 0.5%, [3,15]; review 0.5%, [5,30].
    A 2+ person minority under the country exploration threshold can
    qualify for exploratory protection if >=10% of its immediate observed
    parent AND response total variation >=0.25. These are routing
    heuristics, not population evidence. Never force a normal confidence
    tier on such a branch or erase an unvisited observation.
    """
    explore_rate: str = "0.005"
    explore_floor: int = 3
    explore_cap: int = 15
    review_rate: str = "0.005"
    review_floor: int = 5
    review_cap: int = 30
    protected_min_n: int = 2
    protected_parent_fraction: str = "0.10"
    protected_min_target_tv: str = "0.25"
    max_protected_children_per_split: int = 0  # never auto-expand raw-contrast noise

    def __post_init__(self) -> None:
        for x in (self.explore_rate, self.review_rate,
                  self.protected_parent_fraction, self.protected_min_target_tv):
            _rate(x)
        for x in (self.explore_floor, self.explore_cap,
                  self.review_floor, self.review_cap,
                  self.protected_min_n):
            if type(x) is not int or x < 1:
                raise AdaptiveSupportError("INVALID_SUPPORT_COUNT_LIMIT")
        if (type(self.max_protected_children_per_split) is not int
                or self.max_protected_children_per_split < 0):
            raise AdaptiveSupportError("INVALID_PROTECTED_DIAGNOSTIC_QUOTA")
        if (self.explore_floor > self.explore_cap
                or self.review_floor > self.review_cap
                or self.review_floor < self.explore_floor
                or self.review_cap < self.explore_cap):
            raise AdaptiveSupportError("NONMONOTONE_EXPLORATION_REVIEW_LIMITS")


def threshold(country_question_n: int, *, rate: str,
              floor: int, cap: int) -> int:
    if type(country_question_n) is not int or country_question_n < 0:
        raise AdaptiveSupportError("COUNTRY_QUESTION_DENOMINATOR_INVALID")
    raw = int((Decimal(country_question_n) * _rate(rate)).to_integral_value(
        rounding=ROUND_CEILING))
    return min(cap, max(floor, raw))


def thresholds(country_question_n: int, policy: AdaptiveSupportPolicy) -> dict[str, Any]:
    if type(policy) is not AdaptiveSupportPolicy:
        raise AdaptiveSupportError("EXPLICIT_ADAPTIVE_POLICY_REQUIRED")
    explore = threshold(
        country_question_n, rate=policy.explore_rate,
        floor=policy.explore_floor, cap=policy.explore_cap)
    review = threshold(
        country_question_n, rate=policy.review_rate,
        floor=policy.review_floor, cap=policy.review_cap)
    if review < explore:
        raise AdaptiveSupportError("COUNTRY_POPULATION_NONMONOTONE_THRESHOLDS")
    return {
        "country_question_common_case_n": country_question_n,
        "explore_min_n": explore, "review_candidate_min_n": review,
        "not_population_inference": True,
        "policy": "COUNTRY_RELATIVE_V550_RECOVERY_TWO_GATES_PROVISIONAL@1",
    }


def _shares_from_counts(counts: Mapping[str, int]) -> dict[str, Decimal]:
    if any(type(v) is not int or v < 0 for v in counts.values()):
        raise AdaptiveSupportError("NONEXACT_RESPONSE_COUNT")
    total = sum(counts.values())
    return ({k: Decimal(n) / Decimal(total) for k, n in counts.items()}
            if total else {})


def target_total_variation(
    parent_counts: Mapping[str, int],
    child_counts: Mapping[str, int],
) -> Decimal:
    """TV in [0,1], comparing *same question and parent-child risk*.

    This is a contrast magnitude for allocating *inquiry*, never a
    significance test or a claim that small-n differences generalize.
    """
    p = _shares_from_counts(parent_counts)
    q = _shares_from_counts(child_counts)
    if not p or not q:
        return Decimal(0)
    return sum((abs(p.get(k, Decimal(0)) - q.get(k, Decimal(0)))
                for k in set(p) | set(q)), Decimal(0)) / Decimal(2)


def classify_observed_branch(
    *, country_question_n: int, parent_n: int, observed_n: int,
    parent_target_counts: Mapping[str, int],
    child_target_counts: Mapping[str, int],
    policy: AdaptiveSupportPolicy,
) -> dict[str, Any]:
    """Never convert underpowered/source-observed branch into nonexistent."""
    rule = thresholds(country_question_n, policy)
    if (type(parent_n) is not int or type(observed_n) is not int
            or parent_n < 0 or observed_n < 0 or observed_n > parent_n):
        raise AdaptiveSupportError("PARENT_CHILD_COUNTS_INCONSISTENT")
    if (sum(parent_target_counts.values()) != parent_n
            or sum(child_target_counts.values()) != observed_n):
        raise AdaptiveSupportError("PARENT_CHILD_TARGET_DENOMINATOR_MISMATCH")
    share = Decimal(observed_n) / Decimal(parent_n) if parent_n else Decimal(0)
    contrast = target_total_variation(parent_target_counts, child_target_counts)
    eligible = observed_n >= rule["explore_min_n"]
    protected = (
        0 < observed_n < rule["explore_min_n"]
        and observed_n >= policy.protected_min_n
        and share >= _rate(policy.protected_parent_fraction)
        and contrast >= _rate(policy.protected_min_target_tv)
    )
    review = observed_n >= rule["review_candidate_min_n"]
    return {
        "source_observed_positive": observed_n > 0,
        "observed_raw_n": observed_n,
        "country_question_common_case_n": country_question_n,
        "parent_raw_n": parent_n,
        "parent_fraction": share,
        "target_total_variation_vs_parent": contrast,
        "explore_min_n": rule["explore_min_n"],
        "review_candidate_min_n": rule["review_candidate_min_n"],
        "routine_exploration_eligible": eligible,
        "protected_minor_exploration_candidate": protected,
        "initial_review_support_candidate": review,
        "scientific_grade": (
            "SOURCE_SAMPLE_REVIEWABLE_NOT_POPULATION_INFERENCE" if review
            else "SOURCE_SAMPLE_EXPLORATORY_NOT_INFERENTIALLY_QUALIFIED"
            if (eligible or protected) else
            "SOURCE_OBSERVED_UNDERPOWERED_UNVISITED"
            if observed_n > 0 else
            "EXACT_SOURCE_SAMPLE_ZERO_NOT_STRUCTURAL_IMPOSSIBILITY"
        ),
    }


def order_child_probes(
    candidates: Sequence[tuple[Any, Mapping[str, Any]]],
    policy: AdaptiveSupportPolicy,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Choose affordable/interesting probes; retain every other source row.

    Returns (scheduled, conserved_unvisited), both with source-native values.
    A protected minority reserve is bounded, but *all* underpowered
    uninvestigated observations are present in the explicit inventory.
    """
    regular = []
    protected = []
    held = []
    for value, data in candidates:
        item = {"source_value": value, "support": dict(data)}
        if data["routine_exploration_eligible"]:
            regular.append(item)
        elif data["protected_minor_exploration_candidate"]:
            protected.append(item)
        else:
            held.append({**item, "reason": "SOURCE_OBSERVED_NOT_ROUTINELY_EXPLORED"})
    protected.sort(key=lambda i: (
        -i["support"]["target_total_variation_vs_parent"],
        -i["support"]["parent_fraction"],
        -i["support"]["observed_raw_n"], str(i["source_value"])))
    quota = policy.max_protected_children_per_split
    for item in protected[quota:]:
        held.append({**item, "reason": "PROTECTED_MINOR_PROBE_QUOTA_NOT_NEGATIVE"})
    # A statistical surprise from n=2 or n=4 is overwhelmingly likely
    # without independent corroboration. The default quota is zero.
    # Any nonzero experimental quota must be explicitly requested by
    # the competent source-science owner, never inferred from TV alone.
    scheduled = regular + protected[:quota]
    return scheduled, held
