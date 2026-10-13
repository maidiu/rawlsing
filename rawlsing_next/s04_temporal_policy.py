"""Bounded temporal policy for PRE-V3 historical conditioning.

Implements two interchangeable temporal methods over qualified anchors:
  1. linear_interpolation -- inherited V553 method (gap-insensitive)
  2. nearest_anchor_backoff -- nearest qualified anchor with explicit drift uncertainty

Both are pure functions. No side effects. No invented survey waves.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EvidenceMode(str, Enum):
    MEASURED = "MEASURED"
    TRANSFORMED = "TRANSFORMED"
    INFERRED = "INFERRED"
    PRIOR = "PRIOR"


class TemporalPolicyDecision(str, Enum):
    OBSERVED = "OBSERVED"
    INTERPOLATED = "INTERPOLATED"
    NEAREST_BACKOFF = "NEAREST_BACKOFF"
    BREAK_REFUSAL = "BREAK_REFUSAL"
    GAP_REFUSAL = "GAP_REFUSAL"
    HORIZON_REFUSAL = "HORIZON_REFUSAL"
    PRIOR_BROAD = "PRIOR_BROAD"
    POPULATION_MISMATCH = "POPULATION_MISMATCH"
    POLARITY_DRIFT = "POLARITY_DRIFT"
    MISSING_ANCHOR = "MISSING_ANCHOR"


@dataclass(frozen=True)
class Anchor:
    year: int
    value: float
    population: str
    polarity: str
    qualified: bool = True
    evidence_mode: EvidenceMode = EvidenceMode.MEASURED
    source_ref: str = ""
    category_semantics: str = ""

    def key(self) -> str:
        return f"{self.year}:{self.population}:{self.polarity}"


@dataclass(frozen=True)
class TemporalRequest:
    target_year: int
    population: str
    polarity: str
    max_gap_years: int = 10
    max_horizon_years: int = 20
    allow_interpolation: bool = True
    allow_backoff: bool = True
    allow_prior: bool = False


@dataclass(frozen=True)
class TemporalResult:
    decision: TemporalPolicyDecision
    value: float | None
    drift_uncertainty: float | None
    evidence_mode: EvidenceMode | None
    anchor_refs: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({
            "decision": self.decision.value,
            "value": self.value,
            "drift_uncertainty": self.drift_uncertainty,
            "evidence_mode": self.evidence_mode.value if self.evidence_mode else None,
            "anchor_refs": list(self.anchor_refs),
            "provenance": self.provenance,
        }, sort_keys=True)


def _qualify(anchors: list[Anchor], request: TemporalRequest) -> list[Anchor]:
    return [
        a for a in anchors
        if a.qualified and a.population == request.population and a.polarity == request.polarity
    ]


def _find_breaks(anchors: list[Anchor]) -> list[tuple[int, int]]:
    """Detect abrupt breaks: consecutive anchors with >1 polarity change or >3x value jump."""
    breaks = []
    sorted_a = sorted(anchors, key=lambda a: a.year)
    for i in range(1, len(sorted_a)):
        prev, curr = sorted_a[i - 1], sorted_a[i]
        if prev.polarity != curr.polarity:
            breaks.append((prev.year, curr.year))
        elif prev.value != 0 and abs(curr.value - prev.value) / abs(prev.value) > 3.0:
            breaks.append((prev.year, curr.year))
    return breaks


def linear_interpolation(anchors: list[Anchor], request: TemporalRequest) -> TemporalResult:
    """Inherited V553 linear interpolation. Gap-insensitive; no drift uncertainty."""
    qualified = _qualify(anchors, request)
    if not qualified:
        return TemporalResult(
            decision=TemporalPolicyDecision.MISSING_ANCHOR,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"reason": "no qualified anchors for population/polarity"},
        )

    years = sorted([a.year for a in qualified])
    if request.target_year in years:
        anchor = next(a for a in qualified if a.year == request.target_year)
        return TemporalResult(
            decision=TemporalPolicyDecision.OBSERVED,
            value=anchor.value,
            drift_uncertainty=0.0,
            evidence_mode=EvidenceMode.MEASURED,
            anchor_refs=(anchor.key(),),
            provenance={"method": "linear_interpolation", "exact_anchor": True},
        )

    if not request.allow_interpolation:
        return TemporalResult(
            decision=TemporalPolicyDecision.GAP_REFUSAL,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"reason": "interpolation disabled"},
        )

    left = None
    right = None
    for a in sorted(qualified, key=lambda x: x.year):
        if a.year <= request.target_year:
            left = a
        if a.year >= request.target_year:
            right = a
            break

    if left is None and right is not None:
        gap = right.year - request.target_year
        if gap > request.max_gap_years:
            return TemporalResult(
                decision=TemporalPolicyDecision.GAP_REFUSAL,
                value=None,
                drift_uncertainty=None,
                evidence_mode=None,
                provenance={"gap_years": gap, "max_gap": request.max_gap_years},
            )
        return TemporalResult(
            decision=TemporalPolicyDecision.NEAREST_BACKOFF,
            value=right.value,
            drift_uncertainty=abs(gap) * 0.05,
            evidence_mode=EvidenceMode.INFERRED,
            anchor_refs=(right.key(),),
            provenance={"method": "left_edge_backoff", "gap_years": gap},
        )

    if right is None and left is not None:
        gap = request.target_year - left.year
        if gap > request.max_horizon_years:
            return TemporalResult(
                decision=TemporalPolicyDecision.HORIZON_REFUSAL,
                value=None,
                drift_uncertainty=None,
                evidence_mode=None,
                provenance={"extrapolation_gap": gap, "max_horizon": request.max_horizon_years},
            )
        return TemporalResult(
            decision=TemporalPolicyDecision.NEAREST_BACKOFF,
            value=left.value,
            drift_uncertainty=abs(gap) * 0.05,
            evidence_mode=EvidenceMode.INFERRED,
            anchor_refs=(left.key(),),
            provenance={"method": "right_edge_backoff", "extrapolation_gap": gap},
        )

    if left is None or right is None:
        return TemporalResult(
            decision=TemporalPolicyDecision.MISSING_ANCHOR,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"reason": "no bounding anchors"},
        )

    gap = right.year - left.year
    if gap > request.max_gap_years:
        return TemporalResult(
            decision=TemporalPolicyDecision.GAP_REFUSAL,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"gap_years": gap, "max_gap": request.max_gap_years},
        )

    fraction = (request.target_year - left.year) / (right.year - left.year)
    value = left.value + (right.value - left.value) * fraction

    return TemporalResult(
        decision=TemporalPolicyDecision.INTERPOLATED,
        value=round(value, 6),
        drift_uncertainty=round(abs(gap) * 0.05 * (1.0 - abs(0.5 - fraction)), 6),
        evidence_mode=EvidenceMode.INFERRED,
        anchor_refs=(left.key(), right.key()),
        provenance={
            "method": "linear_interpolation",
            "left_year": left.year,
            "right_year": right.year,
            "fraction": round(fraction, 6),
            "gap_years": gap,
        },
    )


def nearest_anchor_backoff(anchors: list[Anchor], request: TemporalRequest) -> TemporalResult:
    """Nearest qualified anchor with explicit drift uncertainty. No interpolation."""
    qualified = _qualify(anchors, request)
    if not qualified:
        return TemporalResult(
            decision=TemporalPolicyDecision.MISSING_ANCHOR,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"reason": "no qualified anchors for population/polarity"},
        )

    years = sorted([a.year for a in qualified])
    if request.target_year in years:
        anchor = next(a for a in qualified if a.year == request.target_year)
        return TemporalResult(
            decision=TemporalPolicyDecision.OBSERVED,
            value=anchor.value,
            drift_uncertainty=0.0,
            evidence_mode=EvidenceMode.MEASURED,
            anchor_refs=(anchor.key(),),
            provenance={"method": "nearest_anchor_backoff", "exact_anchor": True},
        )

    breaks = _find_breaks(anchors)
    for b in breaks:
        if b[0] < request.target_year < b[1]:
            return TemporalResult(
                decision=TemporalPolicyDecision.BREAK_REFUSAL,
                value=None,
                drift_uncertainty=None,
                evidence_mode=None,
                provenance={"break_between": list(b)},
            )

    best = min(qualified, key=lambda a: abs(a.year - request.target_year))
    gap = abs(best.year - request.target_year)

    if gap > request.max_gap_years:
        return TemporalResult(
            decision=TemporalPolicyDecision.GAP_REFUSAL,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"gap_years": gap, "max_gap": request.max_gap_years},
        )

    if gap > request.max_horizon_years:
        return TemporalResult(
            decision=TemporalPolicyDecision.HORIZON_REFUSAL,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"extrapolation_gap": gap, "max_horizon": request.max_horizon_years},
        )

    if not request.allow_backoff:
        return TemporalResult(
            decision=TemporalPolicyDecision.GAP_REFUSAL,
            value=None,
            drift_uncertainty=None,
            evidence_mode=None,
            provenance={"reason": "backoff disabled"},
        )

    drift = round(gap * 0.05, 6)
    return TemporalResult(
        decision=TemporalPolicyDecision.NEAREST_BACKOFF,
        value=best.value,
        drift_uncertainty=drift,
        evidence_mode=EvidenceMode.INFERRED,
        anchor_refs=(best.key(),),
        provenance={
            "method": "nearest_anchor_backoff",
            "anchor_year": best.year,
            "target_year": request.target_year,
            "gap_years": gap,
            "drift_uncertainty": drift,
        },
    )


def evaluate_temporal(
    anchors: list[Anchor],
    request: TemporalRequest,
    method: str = "nearest_anchor_backoff",
) -> TemporalResult:
    """Dispatch to the selected temporal method. Pure; no side effects."""
    if method == "linear_interpolation":
        return linear_interpolation(anchors, request)
    return nearest_anchor_backoff(anchors, request)


def content_hash(anchors: list[Anchor], request: TemporalRequest) -> str:
    """Deterministic hash of inputs for replay verification."""
    payload = json.dumps({
        "anchors": [{"year": a.year, "value": a.value, "population": a.population,
                      "polarity": a.polarity, "qualified": a.qualified} for a in anchors],
        "request": {"target_year": request.target_year, "population": request.population,
                    "polarity": request.polarity, "max_gap_years": request.max_gap_years,
                    "max_horizon_years": request.max_horizon_years},
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()
