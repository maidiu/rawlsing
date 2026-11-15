#!/usr/bin/env python3
"""POSTG5-W02A regressions for V550 -> V551 raw response direction transport."""
from __future__ import annotations

import pandas as pd
import pytest

from data.ddm_build_copy import ddm_v551_atoms as v551
from data.ddm_build_copy.ddm_v550_bridge import (
    _apply_directionality_overlay,
    _base_bridge_row,
    build_v551_bridge_index_for_table,
)
from data.ddm_build_copy.ddm_v550_distributions import build_distribution_tables
from data.ddm_build_copy.ddm_v550_schema import V551_BRIDGE_INDEX_SCHEMA


def _qmeta() -> dict[str, object]:
    return {
        "run_id": "run-w02a",
        "source": "GSS",
        "source_family": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "country_code": "US",
        "survey_year": 1972,
        "analysis_scope": "country",
        "question_id": "Q1",
        "var_code": "Q1",
        "question_text": "Governed directional item",
        "n_respondents": 4,
        "semantic_role": "RELATION_EVIDENCE",
        "driver_id": "driver::test",
        "driver_facet_id": "facet::test",
        "relation_axis_id": "axis::test",
        "target_entity_id": "target::test",
    }


def _semantics(direction: str, *, label: str, special: bool = False) -> dict[str, object]:
    return {
        "response_label": label,
        "normalized_response_label": label,
        "response_family": "agreement_scale",
        "response_direction": direction,
        "response_intensity": None if special else (0.0 if direction == "neutral" else 0.75),
        "polarity": "" if special else direction,
        "ordinal_rank": None if special else 1,
        "scale_min": None if special else 1,
        "scale_max": None if special else 3,
        "scale_direction": "" if special else "ascending",
        "directionality_status": "NOT_CERTIFIED_SPECIAL" if special else "certified",
        "is_substantive": not special,
        "is_missing": special,
        "is_special": special,
        "is_dk": special,
        "is_refusal": False,
        "is_iap": False,
        "is_not_asked": False,
        "is_inapplicable": False,
        "response_semantics_status": "curated",
        "response_semantics_source": "response_option_map",
        "response_semantics_contract_hash": "semantics-hash",
        "normalization_confidence": "high",
    }


def _distribution_and_bridge() -> tuple[pd.DataFrame, pd.DataFrame]:
    respondent_rows = pd.DataFrame(
        {
            "country_code": ["US", "US", "US", "US"],
            "response_value_normalized": ["1", "2", "3", "99"],
            "response_label": ["Agree", "Disagree", "Neither", "Don't know"],
        }
    )
    semantics_lookup = {
        ("GSS", "1972", "Q1", "1"): _semantics("positive", label="Agree"),
        ("GSS", "1972", "Q1", "2"): _semantics("negative", label="Disagree"),
        ("GSS", "1972", "Q1", "3"): _semantics("neutral", label="Neither"),
        # Deliberately poison the input direction: governed special handling must blank it.
        ("GSS", "1972", "Q1", "99"): _semantics("positive", label="Don't know", special=True),
    }
    _weight_status, _weights, answer_distribution, _country, _gaps, _underpowered = build_distribution_tables(
        respondent_rows,
        _qmeta(),
        min_answer_n=1,
        min_cell_n=1,
        semantics_lookup=semantics_lookup,
    )
    bridge = build_v551_bridge_index_for_table(
        answer_distribution,
        run_id="run-w02a",
        shard_id="GSS__1972",
        table_name="answer_distribution",
        directionality_overlay_lookup={},
        question_contract_lookup={},
    )
    return answer_distribution, bridge


def _bridge_direction_by_value(bridge: pd.DataFrame) -> dict[str, str]:
    return {
        str(row["response_value_normalized"]): str(row["response_direction"] or "")
        for row in bridge.to_dict("records")
    }


def test_governed_response_direction_survives_distribution_to_bridge_positive_negative_neutral():
    distribution, bridge = _distribution_and_bridge()
    dist_direction = {
        str(row["response_value_normalized"]): str(row["response_direction"] or "")
        for row in distribution.to_dict("records")
    }
    assert dist_direction["1"] == "positive"
    assert dist_direction["2"] == "negative"
    assert dist_direction["3"] == "neutral"

    bridge_direction = _bridge_direction_by_value(bridge)
    assert bridge_direction["1"] == "positive"
    assert bridge_direction["2"] == "negative"
    assert bridge_direction["3"] == "neutral"


def test_special_missing_response_does_not_acquire_direction():
    distribution, bridge = _distribution_and_bridge()
    special_dist = distribution.loc[distribution["response_value_normalized"].astype(str).eq("99")].iloc[0]
    special_bridge = bridge.loc[bridge["response_value_normalized"].astype(str).eq("99")].iloc[0]
    assert bool(special_dist["is_special"])
    assert bool(special_dist["is_missing"])
    assert str(special_dist["response_direction"] or "") == ""
    assert str(special_bridge["response_direction"] or "") == ""


@pytest.mark.parametrize("special_field", ["is_special", "is_missing", "is_dk", "is_refusal", "is_iap"])
def test_bridge_fail_closed_special_flags_strip_even_poisoned_direction(special_field: str):
    row = {
        **_qmeta(),
        "response_value_raw": "99",
        "response_value_normalized": "99",
        "response_label": "Special",
        "normalized_response_label": "Special",
        "response_family": "agreement_scale",
        "response_direction": "positive",
        "response_intensity": 0.9,
        "response_option_map_matched": True,
        "is_substantive": False,
        "is_special": False,
        "is_missing": False,
        "is_dk": False,
        "is_refusal": False,
        "is_iap": False,
        "n_unweighted": 1,
    }
    row[special_field] = True
    bridged = _base_bridge_row(
        row,
        run_id="run-w02a",
        shard_id="GSS__1972",
        empirical_object_type="answer_distribution",
        source_table="answer_distribution",
        directionality_overlay_lookup={},
    )
    assert bridged["response_direction"] == ""


def test_question_relation_polarity_or_certification_cannot_manufacture_category_direction():
    row = {
        **_qmeta(),
        "response_value_raw": "1",
        "response_value_normalized": "1",
        "response_label": "Agree",
        "normalized_response_label": "Agree",
        "response_family": "agreement_scale",
        "response_direction": "",
        "response_intensity": 0.75,
        "response_option_map_matched": True,
        "is_substantive": True,
        "is_special": False,
        "is_missing": False,
        "polarity": "positive",
        "relation_projection_polarity": "positive",
        "directional_certification_status": "CERTIFIED",
        "current_directional_atom_eligible": True,
        "directionality_authority_status": "CERTIFIED",
        "n_unweighted": 1,
    }
    bridged = _base_bridge_row(
        row,
        run_id="run-w02a",
        shard_id="GSS__1972",
        empirical_object_type="answer_distribution",
        source_table="answer_distribution",
        directionality_overlay_lookup={},
    )
    assert bridged["response_direction"] == ""


def test_unmatched_response_option_cannot_manufacture_raw_direction():
    row = {
        **_qmeta(),
        "response_value_raw": "1",
        "response_value_normalized": "1",
        "response_label": "Agree",
        "response_family": "agreement_scale",
        "response_direction": "positive",
        "response_intensity": 0.75,
        "response_option_map_matched": False,
        "is_substantive": True,
        "is_special": False,
        "is_missing": False,
        "n_unweighted": 1,
    }
    bridged = _base_bridge_row(
        row,
        run_id="run-w02a",
        shard_id="GSS__1972",
        empirical_object_type="answer_distribution",
        source_table="answer_distribution",
        directionality_overlay_lookup={},
    )
    assert bridged["response_direction"] == ""


def test_schema_limited_parquet_preserves_raw_direction(tmp_path):
    _distribution, bridge = _distribution_and_bridge()
    limited = pd.DataFrame.from_records(
        bridge.to_dict("records"),
        columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"],
    )
    path = tmp_path / "v551_bridge_index.parquet"
    limited.to_parquet(path, index=False)
    reloaded = pd.read_parquet(path)
    directions = _bridge_direction_by_value(reloaded)
    assert directions["1"] == "positive"
    assert directions["2"] == "negative"
    assert directions["3"] == "neutral"
    assert directions["99"] == ""


def test_v550_bridge_does_not_emit_v551_signed_projection_fields():
    _distribution, bridge = _distribution_and_bridge()
    forbidden = {
        "v551_signed_side",
        "v551_signed_intensity",
        "v551_projection_rule_id",
        "v551_projection_authority_hash",
    }
    assert forbidden.isdisjoint(bridge.columns)
    assert set(bridge["directionality_status"].astype(str)).issubset({"NOT_PROJECTED_V550", "NOT_CERTIFIED_SPECIAL"})


def test_legacy_directionality_overlay_helper_is_not_a_raw_direction_transport_path():
    direction, intensity, polarity, scale_direction, status = _apply_directionality_overlay(
        response_family="agreement_scale",
        response_label="Neither",
        response_direction="neutral",
        response_intensity=0.0,
        polarity="positive",
        scale_direction="ascending",
        directionality_status="certified",
        ordinal_rank=2,
        scale_min=1,
        scale_max=3,
        overlay_row={"manual_review_required": False},
    )
    assert direction == ""
    assert intensity == 0.0
    assert polarity == ""
    assert scale_direction == ""
    assert status == "NOT_PROJECTED_V550"


def test_v551_consumes_delivered_raw_direction_without_missing_direction_repair(monkeypatch):
    _distribution, bridge = _distribution_and_bridge()
    producer = bridge.loc[bridge["response_value_normalized"].astype(str).eq("1")].iloc[0].to_dict()
    record = {column: "" for column in V551_BRIDGE_INDEX_SCHEMA["required_columns"]}
    record.update(producer)
    record.update(
        run_id="run-w02a",
        source="GSS",
        source_family="GSS",
        wave="1972",
        canonical_wave="1972",
        country_code="US",
        analysis_scope="country",
        source_table="answer_distribution",
        question_id="Q1",
        var_code="Q1",
        response_family="agreement_scale",
        response_direction="positive",
        response_intensity=0.75,
        directional_applicability_status="APPLICABLE_BY_AUTHORITY",
        bridge_evidence_lane="direct_relation_response",
        is_substantive=True,
        is_missing=False,
        is_special=False,
        response_semantics_contract_hash="semantics-hash",
        semantic_role="RELATION_EVIDENCE",
        semantic_role_authority_status="CERTIFIED",
        response_semantics_authority_status="CERTIFIED",
        directionality_authority_status="CERTIFIED",
        structural_mapping_status="COMPLETE",
        response_option_map_matched=True,
        usable_for_evidence=True,
        allowed_as_v551_relation_evidence=True,
        manual_review_flag=False,
        source_structure_review_required=False,
        n_unweighted=10,
        n_weighted=10.0,
        pct_unweighted=1.0,
        pct_weighted=1.0,
        weight_status="weighted",
    )
    bridge_input = pd.DataFrame([record], columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
    monkeypatch.setattr(
        v551,
        "_load_registry",
        lambda: {
            "semantics-hash": {
                "response_semantics_contract_hash": "semantics-hash",
                "authority_intensity_semantics": "DIRECTIONAL_MAGNITUDE",
                "projection_rule_id": "test_directional_magnitude",
                "authority_status": "CERTIFIED",
                "review_status": "",
            }
        },
    )
    adjudication = v551.build_v551_directional_candidate_adjudication(bridge_input)
    assert len(adjudication) == 1
    row = adjudication.iloc[0]
    assert row["raw_response_direction"] == "positive"
    assert row["adjudication_outcome"] == "PROMOTABLE"
    assert "missing_certified_response_direction" not in str(row["adjudication_reason"])
    assert row["v551_signed_side"] == "positive"
    assert float(row["v551_signed_intensity"]) == pytest.approx(0.75)
