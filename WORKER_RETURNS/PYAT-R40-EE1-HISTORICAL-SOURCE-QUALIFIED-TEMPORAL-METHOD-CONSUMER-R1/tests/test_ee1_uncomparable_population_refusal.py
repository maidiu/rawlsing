"""C3 non-comparability refusals: source family, country, structural
disjointness, and the population/estimand gate with the naive counterexample."""
from __future__ import annotations

import ee1_fixtures as F
from ee1_temporal_owner import (
    build_overlay_table, compare_periods, harmonization, identity_report,
)


def test_mixed_source_family_is_identity_refused():
    result = identity_report(F.mixed_family())
    assert result["state"] == "NONCOMPARABLE_SOURCE_FAMILY"
    assert "survey famil" in result["reason"]


def test_mixed_country_is_identity_refused():
    result = identity_report(F.mixed_country())
    assert result["state"] == "NONCOMPARABLE_COUNTRY"
    assert "countr" in result["reason"]


def test_report_builder_refuses_mixed_family(tmp_path):
    result = harmonization(build_overlay_table(F.mixed_family(), tmp_path))
    assert result["state"] == "REPORT_REFUSED"
    assert "requires one survey family per report" in result["reason"]


def test_report_builder_refuses_mixed_country(tmp_path):
    result = harmonization(build_overlay_table(F.mixed_country(), tmp_path))
    assert result["state"] == "REPORT_REFUSED"
    assert "requires one country per report" in result["reason"]


def test_population_change_is_typed_refusal(tmp_path):
    verdict = compare_periods(F.population_change(), F.ASOF, tmp_path)
    assert verdict["state"] == "NONCOMPARABLE_POPULATION_OR_ESTIMAND"
    assert "target_population" in verdict["population"]["differing_fields"]
    naive = round(0.55 - 0.40, 6)
    assert naive == F.NAIVE_DELTA != 0
    assert "delta" not in verdict


def test_estimand_change_is_typed_refusal(tmp_path):
    verdict = compare_periods(F.estimand_change(), F.ASOF, tmp_path)
    assert verdict["state"] == "NONCOMPARABLE_POPULATION_OR_ESTIMAND"
    assert "estimand" in verdict["population"]["differing_fields"]
    assert "delta" not in verdict


def test_disjoint_semantic_structure_is_noncomparable(tmp_path):
    periods = F.comparable_pair()
    periods[1]["disjoint_semantic"] = True
    verdict = compare_periods(periods, F.ASOF, tmp_path)
    assert verdict["state"] == "NONCOMPARABLE_SOURCE_STRUCTURE"
    report = verdict["report"]
    assert report["ready_for_v553"] is False
    assert report["comparison_authority_status"] == "insufficient_multi_wave_authority"
    assert report["overall_status"] == \
        "STATUS: V553_WAVE_HARMONIZATION_NEEDS_SHARED_SEMANTIC_STRUCTURE"
    assert report["cross_wave_noncomparability_matrix"][0]["noncomparability_reason"] == \
        "insufficient_shared_semantic_structure"
    assert "delta" not in verdict
