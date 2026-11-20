"""Source-neutral, diagnostic-only reference for PYAT conditional-information admission.

Candidate for extension of existing pre553_diagnostics.py by its rightful owner.
NOT an EmpiricalFact producer, survey importer, authority issuer, source reader,
estimator of population uncertainty, cross-candidate ranker, or new data store.

The caller must supply an already source-qualified *one-domain* contingency
whose rows include ALL eligible Y-observed respondents under the selected
question/risk-set/estimand. No inference about unobserved X or Y is made.

Each cell is ((Y_label, X_observation_state, X_observed_value_or_None), count).
Counts should be exact I03 raw or authorized weighted fractions on ONE measure.
Missing kinds must come from real instrument/routing authority.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import isclose, log2
from typing import Mapping

CellKey = tuple[str, str, str | None]
Count = int | Fraction
OBSERVED = "OBSERVED"


@dataclass(frozen=True)
class InformationDecomposition:
    """Numerical descriptive diagnostics only; no scientific authorization."""

    domain_mass: Fraction
    observed_mass: Fraction
    observed_share: float
    observed_value_categories: int
    target_categories: int
    observation_states: tuple[str, ...]
    domain_target_entropy_bits: float
    observation_pattern_information_bits: float
    observed_value_information_bits: float
    domain_weighted_observed_value_information_bits: float
    combined_available_information_bits: float
    state: str = "AVAILABLE_DIAGNOSTIC_ONLY"


def _entropy_from_counts(counts: Mapping[str, Fraction]) -> float:
    total = sum(counts.values(), Fraction(0))
    if total <= 0:
        return 0.0
    return -sum(
        float(c / total) * log2(float(c / total))
        for c in counts.values()
        if c > 0
    )


def _mi_from_cells(cells: Mapping[tuple[str, str], Fraction]) -> float:
    nonzero = {(x, y): c for (x, y), c in cells.items() if c > 0}
    total = sum(nonzero.values(), Fraction(0))
    if total <= 0:
        return 0.0
    row = defaultdict(Fraction)
    col = defaultdict(Fraction)
    for (x, y), c in nonzero.items():
        row[x] += c
        col[y] += c
    return sum(
        float(c / total) * log2(float(c * total / (row[x] * col[y])))
        for (x, y), c in nonzero.items()
    )


def decompose_observation_value_information(
    cells: Mapping[CellKey, Count],
) -> InformationDecomposition:
    """Return I(Y;availability) + q * I(Y;X|X observed) on one common domain.

    Crucial: caller must already have issued and verified the common-domain
    rows and the source-origin observation-status semantics. Distinct candidate
    outputs MUST NOT be used as a global substantive-predictor rank without an
    additional legitimate comparability decision.
    """
    if not cells:
        raise ValueError("EMPTY_DOMAIN: no source-qualified eligible Y-observed cells")
    target = defaultdict(Fraction)
    observation = defaultdict(Fraction)
    values = defaultdict(Fraction)
    combined = defaultdict(Fraction)
    states: set[str] = set()
    targets: set[str] = set()
    observed_values: set[str] = set()
    seen_mass = Fraction(0)
    observed_mass = Fraction(0)

    for (y, status, value), raw_count in cells.items():
        if not isinstance(y, str) or not y:
            raise ValueError("Y target label must be a nonempty sourced string")
        if not isinstance(status, str) or not status:
            raise ValueError("X observation status must be a nonempty sourced string")
        if status == OBSERVED and (not isinstance(value, str) or not value):
            raise ValueError("OBSERVED_X_REQUIRES_SOURCED_VALUE")
        if status != OBSERVED and value is not None:
            raise ValueError("NONOBSERVED_X_MUST_HAVE_NO_INVENTED_VALUE")
        if isinstance(raw_count, bool) or not isinstance(raw_count, (int, Fraction)):
            raise TypeError("Counts must be exact int/Fraction; no rounded float weights")
        count = Fraction(raw_count)
        if count < 0:
            raise ValueError("NEGATIVE_CELL_MASS")
        if count == 0:
            continue
        target[y] += count
        observation[(status, y)] += count
        states.add(status)
        targets.add(y)
        seen_mass += count

        if status == OBSERVED:
            assert value is not None
            observed_mass += count
            observed_values.add(value)
            values[(value, y)] += count
            combined[(f"VALUE:{value}", y)] += count
        else:
            combined[(f"STATUS:{status}", y)] += count

    if seen_mass <= 0:
        raise ValueError("EMPTY_DOMAIN: no positive eligible mass")
    observed_share = float(observed_mass / seen_mass)
    state_info = _mi_from_cells(observation)
    value_info = _mi_from_cells(values)
    value_contribution = observed_share * value_info
    combined_info = _mi_from_cells(combined)
    if not isclose(state_info + value_contribution, combined_info, abs_tol=1e-10):
        raise ArithmeticError("OBSERVATION_VALUE_CHAIN_RULE_FAILED")
    if state_info < -1e-10 or value_info < -1e-10:
        raise ArithmeticError("INVALID_NEGATIVE_INFORMATION")

    return InformationDecomposition(
        domain_mass=seen_mass,
        observed_mass=observed_mass,
        observed_share=observed_share,
        observed_value_categories=len(observed_values),
        target_categories=len(targets),
        observation_states=tuple(sorted(states)),
        domain_target_entropy_bits=_entropy_from_counts(target),
        observation_pattern_information_bits=max(0.0, state_info),
        observed_value_information_bits=max(0.0, value_info),
        domain_weighted_observed_value_information_bits=max(0.0, value_contribution),
        combined_available_information_bits=max(0.0, combined_info),
    )
