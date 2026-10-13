"""S04R independent source-free F7 temporal acceptance probes.

Author: independent HQ283 S04R reviewer.
This file is a *review artifact*, NOT a claim of execution.
The xfail(strict=True) cases describe unclosed acceptance defects in the
S04 candidate at 9ae87f2227384e0567190c6a2d5f3a33a60d4b4c.

They deliberately do not access original survey rows, instrument data,
external services, a protected current or any V3 actor.
"""
from dataclasses import replace

import pytest

from rawlsing_next.s04_temporal_policy import (
    Anchor,
    EvidenceMode,
    TemporalPolicyDecision as D,
    TemporalRequest,
    content_hash,
    evaluate_temporal,
    linear_interpolation,
    nearest_anchor_backoff,
)


def a(year, value, *, population="adult", polarity="high_good",
      mode=EvidenceMode.MEASURED, source="wave", qualified=True,
      semantics="category_0_to_4_ascending"):
    return Anchor(
        year=year, value=value, population=population, polarity=polarity,
        evidence_mode=mode, source_ref=source, qualified=qualified,
        category_semantics=semantics,
    )


def req(year, **kw):
    return TemporalRequest(target_year=year, population="adult",
                           polarity="high_good", **kw)


@pytest.mark.xfail(strict=True, reason="S04 exact anchor overwrites declared PRIOR/TRANSFORMED mode with MEASURED")
@pytest.mark.parametrize("mode", [EvidenceMode.PRIOR, EvidenceMode.TRANSFORMED, EvidenceMode.INFERRED])
def test_hq283_s04r_exact_anchor_does_not_relabel_evidence_as_measured(mode):
    result = nearest_anchor_backoff([a(2010, 0.4, mode=mode)], req(2010))
    assert result.evidence_mode == mode


@pytest.mark.xfail(strict=True, reason="S04 global break detector includes unrelated population and unqualified anchors")
def test_hq283_s04r_unrelated_population_cannot_create_adult_break():
    anchors = [
        a(2000, 0.2), a(2010, 0.3),
        a(2005, 0.9, population="child", polarity="high_bad"),
    ]
    result = nearest_anchor_backoff(anchors, req(2004))
    assert result.decision == D.NEAREST_BACKOFF
    assert result.value == 0.2


@pytest.mark.xfail(strict=True, reason="S04 accepts incompatible category semantics when nominal polarity strings match")
def test_hq283_s04r_no_unqualified_ordinal_reversal_backoff():
    anchors = [
        a(2000, 0.3, semantics="ascending_satisfaction"),
        a(2010, 0.7, semantics="descending_satisfaction"),
    ]
    result = nearest_anchor_backoff(anchors, req(2005))
    assert result.value is None
    assert result.decision != D.NEAREST_BACKOFF


@pytest.mark.xfail(strict=True, reason="S04 content hash omits provenance and evidence mode")
def test_hq283_s04r_input_hash_tracks_source_and_mode():
    left = [a(2010, 0.4, source="release_v1", mode=EvidenceMode.MEASURED)]
    right = [a(2010, 0.4, source="release_v2", mode=EvidenceMode.TRANSFORMED)]
    assert content_hash(left, req(2010)) != content_hash(right, req(2010))


@pytest.mark.xfail(strict=True, reason="S04 content hash omits allow_interpolation/backoff/prior flags")
def test_hq283_s04r_input_hash_tracks_operation_permission():
    anchors = [a(2010, 0.4)]
    assert content_hash(anchors, req(2012, allow_backoff=True)) != content_hash(
        anchors, req(2012, allow_backoff=False)
    )


@pytest.mark.xfail(strict=True, reason="S04 exact-year duplicate uses insertion order without ambiguity court")
def test_hq283_s04r_same_year_conflicting_sources_require_refusal():
    result = nearest_anchor_backoff(
        [a(2010, 0.2, source="release_a"), a(2010, 0.8, source="release_b")],
        req(2010),
    )
    assert result.value is None


@pytest.mark.xfail(strict=True, reason="S04 silently chooses nearest for unknown method")
def test_hq283_s04r_unknown_method_fails_closed():
    with pytest.raises(ValueError):
        evaluate_temporal([a(2010, 0.3)], req(2011), method="unregistered_temporal_rule")


@pytest.mark.xfail(strict=True, reason="S04 3x heuristic does not review jump from zero baseline")
def test_hq283_s04r_zero_baseline_change_requires_method_review():
    result = nearest_anchor_backoff(
        [a(2000, 0.0), a(2010, 0.9)], req(2005)
    )
    assert result.value is None


def test_hq283_s04r_linear_is_not_gap_insensitive():
    result = linear_interpolation(
        [a(2000, 0.2), a(2020, 0.6)],
        req(2010, max_gap_years=5),
    )
    assert result.decision == D.GAP_REFUSAL


def test_hq283_s04r_prior_permission_does_not_conjure_prior_anchor():
    result = nearest_anchor_backoff([], req(2010, allow_prior=True))
    assert result.decision == D.MISSING_ANCHOR
    assert result.value is None


def test_hq283_s04r_single_anchor_extrapolation_is_inferred_not_measured():
    result = nearest_anchor_backoff([a(2010, 0.4)], req(2014))
    assert result.decision == D.NEAREST_BACKOFF
    assert result.evidence_mode == EvidenceMode.INFERRED
    assert result.value == 0.4

