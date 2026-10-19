"""C2 inherited V553 method reuse: identity, harmonization, multi-wave key,
delta permission semantics and the absent-gap register."""
from __future__ import annotations

import ee1_fixtures as F
from ee1_temporal_owner import (
    build_overlay_table, delta_observation_rows, harmonization, identity_report,
    missing_gap_rows, multi_wave_authorization, probe_or_authorized_delta,
    readiness_errors,
)


def test_identity_accepts_comparable_pair():
    result = identity_report(F.comparable_pair())
    assert result["state"] == "IDENTITY_OK"
    assert result["wave_count"] == 2
    assert result["years"] == [2020, 2022]


def test_identity_refuses_duplicate_year_anchor():
    result = identity_report(F.duplicate_year())
    assert result["state"] == "DUPLICATE_YEAR_ANCHOR"
    assert "anchor per calendar year" in result["reason"]


def test_harmonization_report_authorizes_comparable_pair(tmp_path):
    result = harmonization(build_overlay_table(F.comparable_pair(), tmp_path))
    assert result["state"] == "REPORT_OK"
    report = result["report"]
    assert report["ready_for_v553"] is True
    assert report["comparison_authority_status"] == "multi_wave_authorized"
    assert report["comparability_status"] == "comparability_authorized"
    assert report["overall_status"] == "STATUS: READY_FOR_V553_WAVE_HARMONIZATION"
    pair = report["wave_pair_evidence"][0]
    assert pair["pair_harmonization_status"] == "aligned"
    assert pair["pair_missing_authority_count"] == 0
    assert report["cross_wave_comparability_matrix"][0]["comparability_status"] == "comparable"
    assert report["cross_wave_noncomparability_matrix"] == []
    assert report["shared_semantic_columns"] == \
        ["evidence_lane", "semantic_lane", "semantic_role"]
    assert report["shared_directionality_columns"] == \
        ["directionality_policy", "signed_polarity_status"]
    assert report["shared_position_columns"] == \
        ["position_conditioning", "structural_mapping_status"]
    assert abs(report["harmonization_score"] - 0.60) < 1e-6
    assert abs(report["readiness_score"] - 0.70) < 1e-6


def test_multi_wave_key_authorized_after_harmonization(tmp_path):
    rows = build_overlay_table(F.comparable_pair(), tmp_path)
    report = harmonization(rows)["report"]
    authorization = multi_wave_authorization(report, F.comparable_pair())
    assert authorization["multi_wave_authorization_status"] == \
        "AUTHORIZED_SPARSE_TEMPORAL_KEY"
    assert authorization["multi_wave_authorization_reason"] == \
        "at_least_two_probe_ready_resolved_structural_anchors"
    assert authorization["ready_for_v554"] is True
    assert authorization["eligible_wave_count"] == 2
    assert authorization["semantic_compatibility_status"] == \
        "compatible_by_canonical_key"
    assert authorization["directionality_compatibility_status"] == \
        "compatible_by_harmonizer_shared_contract"
    assert authorization["position_compatibility_status"] == \
        "compatible_by_harmonizer_shared_contract"
    assert authorization["structural_identity_compatibility_status"] == \
        "compatible_by_comparable_temporal_key"


def test_multi_wave_key_blocked_without_harmonization(tmp_path):
    periods = F.comparable_pair()
    periods[1]["disjoint_semantic"] = True
    rows = build_overlay_table(periods, tmp_path)
    report = harmonization(rows)["report"]
    assert report["ready_for_v553"] is False
    authorization = multi_wave_authorization(report, periods)
    assert authorization["multi_wave_authorization_status"] == "BLOCKED_TEMPORAL_KEY"
    assert authorization["multi_wave_authorization_reason"] == \
        "harmonization_not_authorized"
    assert authorization["ready_for_v554"] is False


def test_delta_permission_probe_vs_authorized_control():
    probe = probe_or_authorized_delta(
        delta_observation_rows(F.comparable_pair(), authorized=False))
    assert probe["delta_value"] == 0.15
    assert probe["delta_value_kind"] == "probe_delta"
    assert probe["delta_interpretation_permission"] is False
    assert probe["blocked_reason"] == "probe_only_temporal_field"
    assert probe["comparability_status"] == "probe_only"
    assert probe["delta_direction"] == "up"
    assert probe["delta_magnitude_class"] == "small"
    assert (probe["from_year"], probe["to_year"]) == (2020, 2022)
    assert (probe["from_wave_id"], probe["to_wave_id"]) == ("2020", "2022")

    authorized = probe_or_authorized_delta(
        delta_observation_rows(F.comparable_pair(), authorized=True))
    assert authorized["delta_value_kind"] == "authorized_structural"
    assert authorized["delta_interpretation_permission"] is True
    assert authorized["blocked_reason"] == ""
    assert authorized["comparability_status"] == "authorized_comparable"


def test_missing_gap_stays_unknown_noncomparable():
    rows = missing_gap_rows([2020, 2022])
    assert len(rows) == 1
    row = rows[0]
    assert (int(row["year"]), row["register_kind"], row["register_status"]) == \
        (2021, "missing_year", "unknown_noncomparable")
    assert row["register_reason"] == "missing_gap_stays_unknown_noncomparable"
    assert row["comparability_status"] == "unknown_noncomparable"
    interpolated = missing_gap_rows([2020, 2022], allow_interpolation=True)
    assert interpolated[0]["comparability_status"] == "interpolated_with_authority"


def test_thin_layer_readiness_is_typed_not_consumable():
    errors = readiness_errors()
    assert len(errors) >= 40
    assert errors[0] == "V553 thin temporal pressure layer missing packet path"
    assert any("missing cross-wave delta index path" in error for error in errors)
    assert all(isinstance(error, str) for error in errors)


def test_naive_subtraction_is_untyped_while_method_withholds_measurement():
    pair = F.comparable_pair()
    naive = round(pair[1]["probe_value"] - pair[0]["probe_value"], 6)
    assert naive == F.NAIVE_DELTA != 0
    probe = probe_or_authorized_delta(
        delta_observation_rows(pair, authorized=False))
    assert probe["delta_value"] == naive
    assert probe["delta_interpretation_permission"] is False
    assert probe["delta_value_kind"] == "probe_delta"
