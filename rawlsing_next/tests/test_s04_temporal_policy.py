"""Tests for S04 temporal policy: linear interpolation vs nearest-anchor backoff.

All tests are source-free interface tests. No V3 execution.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rawlsing_next.s04_temporal_policy import (
    Anchor,
    EvidenceMode,
    TemporalPolicyDecision,
    TemporalRequest,
    content_hash,
    evaluate_temporal,
    linear_interpolation,
    nearest_anchor_backoff,
    _find_breaks,
)


def make_anchors():
    return [
        Anchor(year=2000, value=0.5, population="adults_18plus", polarity="high_good",
               qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w1"),
        Anchor(year=2005, value=0.6, population="adults_18plus", polarity="high_good",
               qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w2"),
        Anchor(year=2010, value=0.7, population="adults_18plus", polarity="high_good",
               qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w3"),
        Anchor(year=2015, value=0.8, population="adults_18plus", polarity="high_good",
               qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w4"),
    ]


def make_request(year=2007, **kw):
    defaults = {"target_year": year, "population": "adults_18plus", "polarity": "high_good"}
    defaults.update(kw)
    return TemporalRequest(**defaults)


def test_exact_anchor_observed():
    anchors = make_anchors()
    result = nearest_anchor_backoff(anchors, make_request(year=2005))
    assert result.decision == TemporalPolicyDecision.OBSERVED
    assert result.value == 0.6
    assert result.drift_uncertainty == 0.0
    assert result.evidence_mode == EvidenceMode.MEASURED


def test_linear_interpolation_between_anchors():
    anchors = make_anchors()
    result = linear_interpolation(anchors, make_request(year=2007))
    assert result.decision == TemporalPolicyDecision.INTERPOLATED
    assert result.value is not None
    assert abs(result.value - 0.64) < 0.01
    assert result.evidence_mode == EvidenceMode.INFERRED


def test_nearest_anchor_backoff():
    anchors = make_anchors()
    result = nearest_anchor_backoff(anchors, make_request(year=2007))
    assert result.decision == TemporalPolicyDecision.NEAREST_BACKOFF
    assert result.value == 0.6
    assert result.drift_uncertainty == 0.1
    assert result.evidence_mode == EvidenceMode.INFERRED


def test_changed_qualified_anchor_affects_result():
    anchors1 = make_anchors()
    anchors2 = make_anchors()
    anchors2[1] = Anchor(year=2005, value=0.9, population="adults_18plus", polarity="high_good",
                         qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w2")
    r1 = nearest_anchor_backoff(anchors1, make_request(year=2005))
    r2 = nearest_anchor_backoff(anchors2, make_request(year=2005))
    assert r1.value != r2.value


def test_changed_irrelevant_anchor_no_effect():
    anchors1 = make_anchors()
    anchors2 = make_anchors()
    anchors2.append(Anchor(year=2005, value=0.9, population="children_under18", polarity="high_good",
                           qualified=True, evidence_mode=EvidenceMode.MEASURED, source_ref="w2"))
    r1 = nearest_anchor_backoff(anchors1, make_request(year=2005))
    r2 = nearest_anchor_backoff(anchors2, make_request(year=2005))
    assert r1.value == r2.value


def test_break_aware_fallback():
    anchors = [
        Anchor(year=2000, value=0.5, population="adults_18plus", polarity="high_good", qualified=True),
        Anchor(year=2010, value=0.8, population="adults_18plus", polarity="high_bad", qualified=True),
    ]
    breaks = _find_breaks(anchors)
    assert len(breaks) == 1
    result = nearest_anchor_backoff(anchors, make_request(year=2005))
    assert result.decision == TemporalPolicyDecision.BREAK_REFUSAL


def test_excessive_gap_refusal():
    anchors = [
        Anchor(year=2000, value=0.5, population="adults_18plus", polarity="high_good", qualified=True),
        Anchor(year=2030, value=0.8, population="adults_18plus", polarity="high_good", qualified=True),
    ]
    result = nearest_anchor_backoff(anchors, make_request(year=2015, max_gap_years=10))
    assert result.decision == TemporalPolicyDecision.GAP_REFUSAL


def test_unsupported_extrapolation_horizon():
    anchors = [
        Anchor(year=2000, value=0.5, population="adults_18plus", polarity="high_good", qualified=True),
    ]
    result = nearest_anchor_backoff(anchors, make_request(year=2030, max_horizon_years=20, max_gap_years=30))
    assert result.decision == TemporalPolicyDecision.HORIZON_REFUSAL


def test_wrong_population_refusal():
    anchors = [
        Anchor(year=2005, value=0.6, population="children_under18", polarity="high_good", qualified=True),
    ]
    result = nearest_anchor_backoff(anchors, make_request(year=2005))
    assert result.decision == TemporalPolicyDecision.MISSING_ANCHOR


def test_polarity_change_detected():
    anchors = [
        Anchor(year=2000, value=0.5, population="adults_18plus", polarity="high_good", qualified=True),
        Anchor(year=2005, value=0.6, population="adults_18plus", polarity="high_bad", qualified=True),
    ]
    breaks = _find_breaks(anchors)
    assert len(breaks) == 1


def test_missing_anchors():
    result = nearest_anchor_backoff([], make_request(year=2005))
    assert result.decision == TemporalPolicyDecision.MISSING_ANCHOR


def test_replay_deterministic():
    anchors = make_anchors()
    req = make_request(year=2007)
    r1 = nearest_anchor_backoff(anchors, req)
    r2 = nearest_anchor_backoff(anchors, req)
    assert r1.to_json() == r2.to_json()


def test_content_hash_deterministic():
    anchors = make_anchors()
    req = make_request(year=2007)
    h1 = content_hash(anchors, req)
    h2 = content_hash(anchors, req)
    assert h1 == h2


def test_uncertainty_distinction():
    anchors = make_anchors()
    observed = nearest_anchor_backoff(anchors, make_request(year=2005))
    inferred = nearest_anchor_backoff(anchors, make_request(year=2007))
    assert observed.evidence_mode == EvidenceMode.MEASURED
    assert inferred.evidence_mode == EvidenceMode.INFERRED
    assert observed.drift_uncertainty == 0.0
    assert inferred.drift_uncertainty > 0.0


def test_unqualified_anchor_ignored():
    anchors = [
        Anchor(year=2005, value=0.6, population="adults_18plus", polarity="high_good", qualified=False),
        Anchor(year=2010, value=0.7, population="adults_18plus", polarity="high_good", qualified=True),
    ]
    result = nearest_anchor_backoff(anchors, make_request(year=2005))
    assert result.decision == TemporalPolicyDecision.NEAREST_BACKOFF
    assert result.value == 0.7


def test_evaluate_temporal_dispatch():
    anchors = make_anchors()
    req = make_request(year=2007)
    r_linear = evaluate_temporal(anchors, req, method="linear_interpolation")
    r_nearest = evaluate_temporal(anchors, req, method="nearest_anchor_backoff")
    assert r_linear.decision == TemporalPolicyDecision.INTERPOLATED
    assert r_nearest.decision == TemporalPolicyDecision.NEAREST_BACKOFF


def test_provenance_recorded():
    anchors = make_anchors()
    result = nearest_anchor_backoff(anchors, make_request(year=2007))
    assert "method" in result.provenance
    assert "gap_years" in result.provenance
    assert result.anchor_refs
