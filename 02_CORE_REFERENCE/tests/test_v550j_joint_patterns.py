from __future__ import annotations

from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

import pandas as pd
import pytest
import yaml

import data.ddm_build_copy.compile_v550j_joint_response_patterns as compile_v550j_joint_response_patterns
from data.ddm_build_copy.compile_v550j_joint_response_patterns import _family_wave_is_eligible, _family_wave_values, _family_waves
from data.ddm_build_copy.compile_v550j_joint_response_patterns import _expand_response_semantics_lookup
from data.ddm_build_copy.compile_v550j_joint_response_patterns import _load_cached_country_slice
from data.ddm_build_copy.build_determinicity_repository_v550 import _lookup_response_semantics
from data.ddm_build_copy.build_v550j_prepared_substrate import build_family_item_lookup, load_or_build_v550j_prepared_substrate
from data.ddm_build_copy.compile_v550j_joint_response_patterns import _append_family_table_frames, _validate_v550j_run_outputs
from data.ddm_build_copy.ddm_v550j_joint_patterns import (
    _association_candidate_trace_rows,
    _association_publication_mask,
    _validate_association_index_publication_constraints,
    _association_rows,
    _association_eligibility_funnel,
    _association_review_surface_rows,
    _boundary_pattern_type,
    _evaluate_boundary_rules,
    _pattern_meaning_summary_rows,
    _relation_signature_rows,
    classify_association_lane,
    get_associated_var_code,
    _normalize_semantic_response,
    _position_signature_rows,
    _resolve_family_item_semantics,
    compile_v550j_family_tables,
)
from data.ddm_build_copy.numeric_formulas import confidence_score_v1


TEST_CODE_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = TEST_CODE_ROOT / "data/ddm_build_copy/manifests/question_family_registry.yaml"
PARQUET_ENGINE_AVAILABLE = bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))
requires_parquet = pytest.mark.skipif(not PARQUET_ENGINE_AVAILABLE, reason="Parquet engine unavailable in handoff sandbox")


def _family_cfg(minimum_items_answered: int = 3) -> dict[str, object]:
    return {
        "family_id": "gss_abortion_condition_family",
        "family_type": "conditional_attitude_battery",
        "family_label": "GSS abortion conditions",
        "eligible_waves": ["1984"],
        "minimum_items_answered": minimum_items_answered,
        "boundary_rules": [
            {
                "boundary_pattern_type": "broad_support",
                "support_share_min": 0.75,
                "oppose_share_max": 0.25,
            },
            {
                "boundary_pattern_type": "broad_opposition",
                "oppose_share_min": 0.75,
                "support_share_max": 0.25,
            },
            {
                "boundary_pattern_type": "exception_support_elective_opposition",
                "require_all": [
                    {"role": "exception_case", "semantic_response_role": "support"},
                    {"role": "elective_case", "semantic_response_role": "oppose"},
                ],
            },
        ],
        "item_role_groups": {
            "exception_case": [
                {"var_code": "abrape", "condition_label": "rape"},
                {"var_code": "abhlth", "condition_label": "woman_health"},
                {"var_code": "abdefect", "condition_label": "fetal_defect"},
            ],
            "elective_case": [{"var_code": "abany", "condition_label": "any_reason"}],
            "social_condition": [{"var_code": "absingle", "condition_label": "unmarried"}],
            "family_size_condition": [{"var_code": "abnomore", "condition_label": "no_more_children"}],
            "economic_condition": [{"var_code": "abpoor", "condition_label": "low_income"}],
        },
    }


def _family_questions(wave: str = "1984") -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"var_code": "abrape", "question_id": "Q1", "question_text": "rape?", "wave": wave, "canonical_wave": wave, "source": "GSS"},
            {"var_code": "abhlth", "question_id": "Q2", "question_text": "health?", "wave": wave, "canonical_wave": wave, "source": "GSS"},
            {"var_code": "abdefect", "question_id": "Q3", "question_text": "defect?", "wave": wave, "canonical_wave": wave, "source": "GSS"},
        ]
    )


def _registry_family_cfg(family_id: str) -> dict[str, object]:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return next(entry for entry in registry["families"] if entry["family_id"] == family_id)


def _family_questions_from_registry(family_cfg: dict[str, object], wave: str = "1972") -> pd.DataFrame:
    rows = []
    for role_items in (family_cfg.get("item_role_groups") or {}).values():
        for item in role_items or []:
            rows.append(
                {
                    "var_code": item["var_code"],
                    "question_id": f"Q_{item['var_code'].upper()}",
                    "question_text": item.get("condition_label", item["var_code"]),
                    "wave": wave,
                    "canonical_wave": wave,
                    "source": "GSS",
                }
            )
    return pd.DataFrame(rows)


def _registry_family_frame(
    family_cfg: dict[str, object],
    *,
    respondent_id: str = "r1",
    response_value_map: dict[str, str] | None = None,
    wave: str = "1972",
    canonical_wave: str = "1972",
) -> pd.DataFrame:
    response_value_map = response_value_map or {}
    rows = []
    for role_items in (family_cfg.get("item_role_groups") or {}).values():
        for item in role_items or []:
            var_code = item["var_code"]
            rows.append(
                {
                    "respondent_id": respondent_id,
                    "var_code": var_code,
                    "question_id": f"Q_{var_code.upper()}",
                    "response_value_normalized": response_value_map.get(var_code.upper(), response_value_map.get(var_code.lower(), "1")),
                    "response_label": response_value_map.get(f"{var_code.upper()}_label", response_value_map.get(f"{var_code.lower()}_label", "yes")),
                    "normalized_response_label": response_value_map.get(f"{var_code.upper()}_label", response_value_map.get(f"{var_code.lower()}_label", "yes")),
                    "response_direction": "",
                    "response_intensity": 1.0,
                    "polarity": "",
                    "weight_value": 1.0,
                    "weight_status": "weighted_valid",
                    "is_substantive": True,
                    "directionality_status": "unknown",
                    "response_semantics_status": "observed_only",
                    "response_semantics_source": "observed_response_row",
                    "source": "GSS",
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": "US",
                    "survey_year": 1972,
                    "semantic_role": "RELATION_EVIDENCE",
                    "v551_evidence_role": "DIRECT_RELATION_RESPONSE",
                    "source_structure_classification": "substantive",
                    "source_structure_source": "question_structure_register",
                    "source_structure_fields_joined": True,
                }
            )
    return pd.DataFrame(rows)


def test_family_item_lookup_builds_normalized_codes_once() -> None:
    family_cfg = _family_cfg()
    lookup = build_family_item_lookup(family_cfg)
    assert not lookup.empty
    assert set(lookup["var_code_norm"].astype(str)) == {"ABRAPE", "ABHLTH", "ABDEFECT", "ABANY", "ABSINGLE", "ABNOMORE", "ABPOOR"}
    assert set(lookup["family_id"].astype(str)) == {"gss_abortion_condition_family"}


@pytest.mark.parametrize(
    "record,expected",
    [
        ({"associated_var_code": "RACE", "semantic_role": "substantive"}, "RACE"),
        ({"var_code_norm": "OCC10"}, "OCC10"),
        ({"var_code": "partyid"}, "PARTYID"),
    ],
)
def test_get_associated_var_code_prefers_associated_and_fallback_codes(record: dict[str, object], expected: str) -> None:
    assert get_associated_var_code(record) == expected


@pytest.mark.parametrize(
    "record,expected_lane",
    [
        ({"associated_var_code": "RACE", "semantic_role": "substantive"}, "identity_coordinate_association"),
        ({"associated_var_code": "REG16"}, "position_context_association"),
        ({"associated_var_code": "OCC10"}, "occupational_status_association"),
        ({"associated_var_code": "PAEDUC"}, "family_background_association"),
        ({"associated_var_code": "AGEWED"}, "life_course_context_association"),
        ({"associated_var_code": "PARTYID", "semantic_role": "attitude"}, "political_orientation_association"),
    ],
)
def test_classify_association_lane_known_variables_do_not_collapse(record: dict[str, object], expected_lane: str) -> None:
    lane, lane_status, rule_id = classify_association_lane(
        associated_var_code=str(record.get("associated_var_code", "")),
        source="GSS",
        source_structure_classification=str(record.get("source_structure_classification", "")),
        semantic_role=str(record.get("semantic_role", "")),
        direct_evidence_status="direct_or_not_flagged",
        question_type=str(record.get("question_type", "")),
        response_semantics_status=str(record.get("response_semantics_status", "")),
    )
    assert lane == expected_lane
    assert lane_status in {"var_code_rule", "semantic_role_rule", "question_type_rule", "diagnostic"}


def test_classify_association_lane_observed_only_without_semantic_or_question_hint_stays_unknown() -> None:
    lane, lane_status, rule_id = classify_association_lane(
        associated_var_code="OTHER1",
        source="GSS",
        source_structure_classification="substantive",
        semantic_role="",
        direct_evidence_status="direct_or_not_flagged",
        question_type="",
        response_semantics_status="observed_only",
    )
    assert lane == "unknown_association_lane"
    assert lane_status == "observed_response_semantics_insufficient_for_lane"


def test_classify_association_lane_missing_code_stays_unknown() -> None:
    lane, lane_status, rule_id = classify_association_lane(
        associated_var_code="",
        source="GSS",
        source_structure_classification="",
        semantic_role="",
        direct_evidence_status="direct_or_not_flagged",
        question_type="",
        response_semantics_status="",
    )
    assert lane == "unknown_association_lane"
    assert lane_status == "missing_associated_var_code"


def test_classify_association_lane_registry_override_wins() -> None:
    lane, lane_status, rule_id = classify_association_lane(
        associated_var_code="RACE",
        source="GSS",
        source_structure_classification="substantive",
        semantic_role="attitude",
        direct_evidence_status="direct_or_not_flagged",
        question_type="attitude",
        response_semantics_status="observed_only",
        registry_override="identity_coordinate_association",
    )
    assert lane == "identity_coordinate_association"
    assert lane_status == "registry_override"


def test_association_publication_mask_requires_full_gate_stack() -> None:
    common = {
        "association_publication_status": "publishable",
        "would_emit_as_publishable": True,
        "association_support_gate_status": "sufficient_support",
        "association_lane_publishability": "publishable_lane",
        "association_lane_resolution_type": "exact_registry",
        "association_lane_rule_id": "rule-1",
        "association_support_n_unweighted": 35,
        "association_support_threshold": 30,
        "associated_response_total_n": 100,
        "associated_var_distinct_response_count": 5,
        "is_high_cardinality_associated_var": False,
        "is_sparse_associated_response": False,
        "is_raw_occupational_status_code": False,
        "is_same_family_association": False,
        "is_same_variable_association": False,
        "pattern_member_n_unweighted": 40,
        "association_support_ratio": 0.35,
        "difference_from_baseline": 0.2,
    }
    frame = pd.DataFrame(
        [
            {**common, "association_lane": "substantive_attitude_association"},
            {**common, "association_lane": "identity_coordinate_association"},
        ]
    )
    mask = _association_publication_mask(frame, publishable_lanes={"substantive_attitude_association"})
    assert mask.tolist() == [True, False]


def test_association_index_validation_rejects_lane_only_publication() -> None:
    frame = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source_id": "GSS",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "family_id": "fam",
                "pattern_id": "p1",
                "association_publication_status": "publishable",
                "would_emit_as_publishable": True,
                "association_support_gate_status": "sufficient_support",
                "association_lane_publishability": "publishable_lane",
                "association_lane": "identity_coordinate_association",
                "association_support_n_unweighted": 35,
                "association_support_threshold": 30,
            }
        ]
    )
    with pytest.raises(RuntimeError, match="violates publication constraints"):
        _validate_association_index_publication_constraints(frame, publishable_lanes={"substantive_attitude_association"})


def test_association_review_surface_captures_supported_nonpublishable_lanes() -> None:
    candidate_trace = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source_id": "GSS",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "family_id": "fam",
                "pattern_id": "p1",
                "associated_var_code": "RACE",
                "associated_response_value": "1",
                "associated_response_label": "white",
                "association_lane": "identity_coordinate_association",
                "association_lane_status": "var_code_rule",
                "association_lane_authority_source": "lane_classifier",
                "association_lane_basis": "RACE",
                "association_lane_publishability": "diagnostic_only_lane",
                "association_support_n_unweighted": 25,
                "association_support_threshold": 30,
                "associated_response_total_n": 50,
                "associated_var_distinct_response_count": 3,
                "p_response_given_pattern": 0.5,
                "p_response_baseline": 0.2,
                "difference_from_baseline": 0.3,
                "lift": 2.5,
                "mutual_information": 0.1,
                "association_publication_status": "diagnostic_only_raw_component",
                "review_surface_reason": "lane_not_publishable_but_supported",
                "review_surface_priority": "medium",
            }
        ]
    )
    review = _association_review_surface_rows(candidate_trace)
    assert not review.empty
    assert set(review["association_lane"].astype(str)) == {"identity_coordinate_association"}
    assert set(review["review_surface_reason"].astype(str)) == {"lane_not_publishable_but_supported"}


def test_pattern_meaning_summary_emits_structured_json() -> None:
    pattern_df = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source_id": "GSS",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "pattern_id": "p1",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "target_selective_tolerance_battery",
                "boundary_pattern_type": "selective_tolerance",
                "support_status": "clears_threshold",
                "pattern_count_unweighted": 40,
                "semantic_role_resolved_share": 1.0,
                "target_structure_status": "target_selective_battery",
                "target_selectivity_profile": "target_selective_tolerance",
            }
        ]
    )
    candidate_trace = pd.DataFrame(
        [
            {
                "pattern_id": "p1",
                "family_id": "fam",
                "associated_var_code": "PARTYID",
                "associated_response_value": "1",
                "associated_response_label": "democrat",
                "association_lane": "substantive_attitude_association",
                "association_publication_status": "publishable",
                "association_support_n_unweighted": 35,
                "association_support_threshold": 30,
                "p_response_given_pattern": 0.6,
                "p_response_baseline": 0.2,
                "difference_from_baseline": 0.4,
                "lift": 3.0,
                "mutual_information": 0.2,
                "review_surface_reason": "",
            },
            {
                "pattern_id": "p1",
                "family_id": "fam",
                "associated_var_code": "RACE",
                "associated_response_value": "1",
                "associated_response_label": "white",
                "association_lane": "identity_coordinate_association",
                "association_publication_status": "diagnostic_only_raw_component",
                "association_support_n_unweighted": 12,
                "association_support_threshold": 30,
                "p_response_given_pattern": 0.4,
                "p_response_baseline": 0.2,
                "difference_from_baseline": 0.2,
                "lift": 2.0,
                "mutual_information": 0.1,
                "review_surface_reason": "lane_not_publishable_but_supported",
            },
        ]
    )
    association_index = candidate_trace[candidate_trace["association_publication_status"].astype(str).eq("publishable")].copy()
    summary = _pattern_meaning_summary_rows(
        pattern_df,
        candidate_trace,
        candidate_trace[~candidate_trace["association_publication_status"].astype(str).eq("publishable")].copy(),
        association_index,
    )
    assert not summary.empty
    row = summary.iloc[0]
    assert row["meaning_summary_status"] == "summary_available_publishable_only"
    assert row["meaning_summary_confidence"] == "low"
    assert json.loads(row["top_publishable_attitude_associations_json"])
    assert json.loads(row["top_identity_context_signals_json"])


@requires_parquet
def test_prepared_substrate_skips_harmonization_for_already_enriched_frame(monkeypatch, tmp_path) -> None:
    source_frame = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source": "GSS",
                "source_id": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "respondent_id": "r1",
                "weight_value": 1.0,
                "weight_status": "weighted_valid",
                "var_code": "ABHLTH",
                "question_id": "Q_ABHLTH",
                "question_text": "abortion health",
                "response_value": "1",
                "response_value_normalized": "1",
                "response_label": "yes",
                "normalized_response_label": "yes",
                "is_missing": False,
                "is_dk": False,
                "is_refusal": False,
                "is_iap": False,
                "is_valid_substantive_response": True,
                "semantic_response_role": "support",
                "semantic_response_role_status": "family_registry_fallback_authorized",
                "response_semantics_authority_source": "question_family_registry.response_role_rules",
                "semantic_response_role_authority": "question_family_registry.response_role_rules",
                "response_direction": "allow_directionality",
                "polarity": "positive",
                "directionality_status": "manually_authorized_directionality",
                "directionality_authority_source": "question_family_registry.response_role_rules",
                "directionality_basis_source": "manually_verified_gss_codebook",
                "target_entity_id": "abortion_permission",
                "target_domain": "reproductive_moral_regulation",
                "target_condition_label": "woman_health",
                "target_group_label": "",
                "permission_domain": "abortion_permission",
                "target_resolution_grain": "condition_label",
                "target_resolution_status": "family_registry_resolved_condition",
                "target_resolution_authority_source": "question_family_registry.target_resolution_rules",
                "target_resolution_basis_source": "question_family_registry.target_resolution_rules",
                "driver_id": "",
                "driver_facet_id": "",
                "relation_axis_id": "",
                "semantic_role": "relation_evidence",
                "v551_evidence_role": "relation_evidence",
                "mapping_status": "mapped",
                "source_structure_classification": "substantive",
                "question_type": "attitude",
                "handling_rule": "observe",
                "recommended_computation": "direct",
                "is_substantive": True,
                "not_direct_evidence": False,
                "allowed_as_association_feature": True,
                "allowed_as_attitude_cloud_feature": True,
                "association_lane": "substantive_attitude_association",
            }
        ]
    )

    calls = {"n": 0}

    def fake_harmonize(*args, **kwargs):
        calls["n"] += 1
        raise AssertionError("prepared substrate should not re-harmonize an already enriched frame")

    monkeypatch.setattr("data.ddm_build_copy.build_v550j_prepared_substrate._harmonize_question_frame", fake_harmonize)
    prepared, manifest = load_or_build_v550j_prepared_substrate(
        run_id="run-1",
        source="GSS",
        source_id="GSS",
        wave="1972",
        canonical_wave="1972",
        country_code="US",
        source_frame=source_frame,
        semantics_lookup={},
        response_semantics_contract_hash="contract-hash",
        output_root=tmp_path,
        question_family_registry_hash="registry-hash",
        authority_compendium_hash="authority-hash",
        view_schema_hash="view-hash",
        substrate_mode="prepared_or_build",
    )
    assert calls["n"] == 0
    assert not prepared.empty
    assert manifest["cache_valid"] is True
    assert int(manifest["harmonization_calls"]) == 0
    assert "var_code_norm" in prepared.columns
    assert "respondent_id_norm" in prepared.columns
    assert (tmp_path / "cache" / "prepared_response_substrate" / "source=GSS" / "wave=1972" / "country_code=US" / "v550j_prepared_substrate_validation_report.json").exists()


def test_family_tables_emit_reusable_membership_artifact() -> None:
    family_cfg = _family_cfg(minimum_items_answered=1)
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=1.0),
            _row("r1", "abhlth", "2", "disallow_directionality", sex="F", weight_value=1.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=family_frame, emit_diagnostics=True)
    membership = tables["joint_pattern_respondent_membership"]
    assert not membership.empty
    assert {"pattern_id", "respondent_id", "respondent_id_norm", "pattern_signature", "pattern_support_status"}.issubset(set(membership.columns))
    assert membership["family_id"].astype(str).eq("gss_abortion_condition_family").all()
    assert membership["respondent_id"].astype(str).eq("r1").any()


def _row(
    respondent_id: str,
    var_code: str,
    response_value: str,
    response_direction: str,
    *,
    sex: str,
    weight_value: float,
    directionality_status: str = "inferred_from_directionality_overlay",
    wave: str = "1984",
    canonical_wave: str = "1984",
    country_code: str = "US",
    survey_year: int = 1984,
) -> dict[str, object]:
    return {
        "respondent_id": respondent_id,
        "var_code": var_code,
        "question_id": {"abrape": "Q1", "abhlth": "Q2", "abdefect": "Q3"}.get(var_code, "QX"),
        "response_value_normalized": response_value,
        "response_label": response_value,
        "normalized_response_label": response_value,
        "response_direction": response_direction,
        "response_intensity": 1.0,
        "polarity": "positive" if response_direction == "allow_directionality" else "negative",
        "weight_value": weight_value,
        "weight_status": "weighted",
        "is_substantive": True,
        "directionality_status": directionality_status,
        "response_semantics_source": "directionality_overlay",
        "source": "GSS",
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "survey_year": survey_year,
        "sex": sex,
    }


def test_confidence_score_v1_is_already_on_0_to_100_scale() -> None:
    assert confidence_score_v1(50, 50, 50, 50, 50) == 50
    assert confidence_score_v1(1, 1, 1, 1, 1) == 1


def test_registry_governed_boundary_rules_are_used() -> None:
    family_cfg = _family_cfg()
    item_rows = [
        {"item_role": "exception_case", "semantic_response_role": "support"},
        {"item_role": "elective_case", "semantic_response_role": "oppose"},
        {"item_role": "social_condition", "semantic_response_role": "support"},
    ]
    semantic_counts = Counter(row["semantic_response_role"] for row in item_rows)
    assert _boundary_pattern_type(family_cfg, semantic_counts, item_rows) == "exception_support_elective_opposition"
    assert _boundary_pattern_type(
        family_cfg,
        Counter({"support": 1, "oppose": 1, "neutral": 1}),
        [
            {"item_role": "social_condition", "semantic_response_role": "support"},
            {"item_role": "elective_case", "semantic_response_role": "oppose"},
        ],
    ) == "mixed_unclassified"


def test_live_registry_abortion_boundary_requires_exception_support() -> None:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    family_cfg = next(entry for entry in registry["families"] if entry["family_id"] == "gss_abortion_condition_family")
    semantic_counts = Counter({"support": 1, "oppose": 1})
    item_rows = [
        {"item_role": "social_condition", "semantic_response_role": "support"},
        {"item_role": "elective_case", "semantic_response_role": "oppose"},
    ]
    assert _boundary_pattern_type(family_cfg, semantic_counts, item_rows) == "mixed_unclassified"


def test_semantic_fallback_requires_direction_authority() -> None:
    assert _normalize_semantic_response("", "", "yes") == "unknown"
    assert _normalize_semantic_response("positive", "positive", "yes", "inferred_from_directionality_overlay") == "support"
    assert _normalize_semantic_response("negative", "negative", "no", "inferred_from_directionality_overlay") == "oppose"
    assert _normalize_semantic_response("positive", "positive", "yes", "forced_unsigned_by_directionality_overlay") == "unknown"
    assert _normalize_semantic_response("negative", "negative", "no", "manual_review_required_by_directionality_overlay") == "unknown"
    assert _normalize_semantic_response("positive", "positive", "yes", "") == "unknown"
    assert _normalize_semantic_response("", "", "neutral") == "neutral"


def test_response_semantics_lookup_aliases_match_var_code_and_wave_variants() -> None:
    response_map = pd.DataFrame(
        [
            {
                "source": "GSS",
                "wave": "1972.0",
                "canonical_wave": "1972",
                "var_name": "abhlth",
                "var_code": "ABHLTH",
                "value_code_normalized": "1",
                "value_label_clean": "yes",
                "normalized_response_label": "yes",
            }
        ]
    )
    base_lookup = _lookup_response_semantics(response_map)
    lookup = _expand_response_semantics_lookup(response_map, base_lookup)
    assert ("GSS", "1972.0", "abhlth", "1") in base_lookup
    assert ("GSS", "1972", "ABHLTH", "1") in lookup
    assert ("GSS", "1972", "abhlth", "1") in lookup


@requires_parquet
def test_cached_country_slice_falls_back_to_db_when_cache_misses(monkeypatch) -> None:
    calls = {"sql": None}

    def fake_load_cached_frame(*args, **kwargs):
        return None

    def fake_read_sql_query(sql, conn):
        calls["sql"] = sql
        return pd.DataFrame(
            [
                {
                    "source": "GSS",
                    "canonical_wave": "1972",
                    "var_code": "OTHER1",
                    "respondent_id": "r1",
                    "response_value_normalized": "A",
                }
            ]
        )

    monkeypatch.setattr("data.ddm_build_copy.compile_v550j_joint_response_patterns.load_cached_frame", fake_load_cached_frame)
    monkeypatch.setattr("data.ddm_build_copy.compile_v550j_joint_response_patterns.pd.read_sql_query", fake_read_sql_query)
    out = _load_cached_country_slice(
        source="GSS",
        waves=["1972"],
        country_code="US",
        response_semantics_contract_hash="hash",
        db_conn=object(),
    )
    assert calls["sql"] is not None
    assert not out.empty
    assert "var_code" in out.columns
    assert out.iloc[0]["var_code"] == "OTHER1"


@requires_parquet
def test_cached_country_slice_force_db_bypasses_family_only_cache(monkeypatch) -> None:
    cached_df = pd.DataFrame(
        [
            {
                "source": "GSS",
                "canonical_wave": "1972",
                "var_code": "ABHLTH",
                "respondent_id": "r1",
                "response_value_normalized": "1",
            }
        ]
    )
    live_df = pd.DataFrame(
        [
            {
                "source": "GSS",
                "canonical_wave": "1972",
                "var_code": "OTHER1",
                "respondent_id": "r1",
                "response_value_normalized": "A",
            }
        ]
    )

    def fake_load_cached_frame(*args, **kwargs):
        return cached_df

    def fake_read_sql_query(sql, conn):
        return live_df

    monkeypatch.setattr("data.ddm_build_copy.compile_v550j_joint_response_patterns.load_cached_frame", fake_load_cached_frame)
    monkeypatch.setattr("data.ddm_build_copy.compile_v550j_joint_response_patterns.pd.read_sql_query", fake_read_sql_query)
    out = _load_cached_country_slice(
        source="GSS",
        waves=["1972"],
        country_code="US",
        response_semantics_contract_hash="hash",
        db_conn=object(),
        force_db=True,
    )
    assert not out.empty
    assert out.iloc[0]["var_code"] == "OTHER1"


def test_family_registry_fallback_resolves_library_semantics_and_targets() -> None:
    family_cfg = _registry_family_cfg("gss_civil_liberties_library_family")
    family_questions = _family_questions_from_registry(family_cfg)
    family_frame = _registry_family_frame(
        family_cfg,
        response_value_map={
            "LIBATH": "1",
            "LIBATH_label": "remove",
            "LIBCOM": "2",
            "LIBCOM_label": "not remove",
            "LIBHOMO": "1",
            "LIBHOMO_label": "remove",
        },
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    item_index = tables["joint_response_pattern_item_index"]
    assert not item_index.empty
    libath = item_index[item_index["var_code"].astype(str).str.lower().eq("libath")].iloc[0]
    libcom = item_index[item_index["var_code"].astype(str).str.lower().eq("libcom")].iloc[0]
    assert libath["semantic_response_role"] == "oppose"
    assert libcom["semantic_response_role"] == "support"
    assert libath["target_resolution_status"] == "family_registry_resolved_group"
    assert libcom["target_resolution_status"] == "family_registry_resolved_group"
    assert str(libath["target_entity_id"]) == "outgroup_anti_religionist"
    assert str(libcom["target_entity_id"]) == "outgroup_communist"
    assert str(libath["target_group_label"]) == "anti_religionist"
    assert str(libcom["target_group_label"]) == "communist"
    assert str(libath["permission_domain"]) == "institutional_library_access"
    relation_index = tables["joint_pattern_relation_signature"]
    assert not relation_index.empty
    assert set(relation_index["target_resolution_status"].astype(str)) == {"family_registry_resolved_group"}
    assert float(relation_index.iloc[0]["target_group_share"]) == 1.0
    assert float(relation_index.iloc[0]["permission_domain_share"]) == 1.0
    assert float(relation_index.iloc[0]["registry_resolved_share"]) == 0.0


def test_abortion_target_resolution_uses_permission_object_and_condition_grain() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    row = pd.Series(
        {
            "var_code": "ABHLTH",
            "response_value_normalized": "1",
            "response_label": "yes",
            "normalized_response_label": "yes",
            "response_direction": "",
            "polarity": "",
            "response_option_map_matched": False,
            "response_semantics_source": "observed_response_row",
            "directionality_status": "unknown",
            "response_semantics_status": "observed_only",
            "wave": "1984",
            "canonical_wave": "1984",
        }
    )
    resolved = _resolve_family_item_semantics(
        row,
        family_cfg=family_cfg,
        item_meta={"item_role": "exception_case", "condition_label": "woman_health"},
    )
    assert resolved["target_entity_id"] == "abortion_permission"
    assert resolved["target_condition_label"] == "woman_health"
    assert resolved["target_resolution_grain"] == "condition_label"
    assert resolved["target_resolution_status"] == "family_registry_resolved_condition"
    assert resolved["target_resolution_authority_source"] == "question_family_registry.target_resolution_rules"
    assert resolved["target_resolution_basis_source"] == "question_family_registry.item_role_groups"
    assert resolved["response_semantics_authority_source"] == "question_family_registry.response_role_rules"
    assert resolved["directionality_authority_source"] == "question_family_registry.response_role_rules"


def test_civil_liberties_target_groups_keep_permission_domain_separate() -> None:
    speak_cfg = _registry_family_cfg("gss_civil_liberties_speak_family")
    library_cfg = _registry_family_cfg("gss_civil_liberties_library_family")
    speak_row = pd.Series(
        {
            "var_code": "SPKATH",
            "response_value_normalized": "1",
            "response_label": "yes",
            "normalized_response_label": "yes",
            "response_direction": "",
            "polarity": "",
            "response_option_map_matched": False,
            "response_semantics_source": "observed_response_row",
            "directionality_status": "unknown",
            "response_semantics_status": "observed_only",
            "wave": "1972",
            "canonical_wave": "1972",
        }
    )
    library_row = pd.Series(
        {
            "var_code": "LIBATH",
            "response_value_normalized": "1",
            "response_label": "no",
            "normalized_response_label": "no",
            "response_direction": "",
            "polarity": "",
            "response_option_map_matched": False,
            "response_semantics_source": "observed_response_row",
            "directionality_status": "unknown",
            "response_semantics_status": "observed_only",
            "wave": "1972",
            "canonical_wave": "1972",
        }
    )
    resolved_speak = _resolve_family_item_semantics(
        speak_row,
        family_cfg=speak_cfg,
        item_meta={"item_role": "target_case", "condition_label": "anti_religionist"},
    )
    resolved_library = _resolve_family_item_semantics(
        library_row,
        family_cfg=library_cfg,
        item_meta={"item_role": "target_case", "condition_label": "anti_religionist"},
    )
    assert resolved_speak["target_entity_id"] == "outgroup_anti_religionist"
    assert resolved_library["target_entity_id"] == "outgroup_anti_religionist"
    assert resolved_speak["target_group_label"] == "anti_religionist"
    assert resolved_library["target_group_label"] == "anti_religionist"
    assert resolved_speak["permission_domain"] == "public_expression_permission"
    assert resolved_library["permission_domain"] == "institutional_library_access"
    assert resolved_speak["target_resolution_grain"] == "target_group"
    assert resolved_library["target_resolution_grain"] == "target_group"
    assert resolved_speak["target_resolution_status"] == "family_registry_resolved_group"
    assert resolved_library["target_resolution_status"] == "family_registry_resolved_group"
    assert resolved_speak["target_resolution_basis_source"] == "question_family_registry.item_role_groups"
    assert resolved_library["target_resolution_basis_source"] == "question_family_registry.item_role_groups"


def test_pattern_level_semantic_authority_summarizes_item_level_authority() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    family_questions = _family_questions_from_registry(family_cfg, wave="1972")
    family_frame = _registry_family_frame(
        family_cfg,
        wave="1972",
        canonical_wave="1972",
        response_value_map={
            "ABHLTH_label": "yes",
            "ABRAPE_label": "yes",
            "ABDEFECT_label": "yes",
            "ABANY_label": "no",
            "ABSINGLE_label": "yes",
            "ABNOMORE_label": "yes",
            "ABPOOR_label": "yes",
        },
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=family_frame)
    pattern_index = tables["joint_response_pattern_index"]
    assert not pattern_index.empty
    assert "unknown" not in set(pattern_index["semantic_response_role_status"].astype(str).str.lower())
    assert "none" not in set(pattern_index["response_semantics_authority_source"].astype(str).str.lower())
    assert "none" not in set(pattern_index["directionality_authority_source"].astype(str).str.lower())
    assert float(pattern_index["semantic_role_resolved_share"].min()) > 0.0
    assert float(pattern_index["semantic_role_unknown_share"].max()) < 1.0
    assert set(pattern_index["response_semantics_authority_source"].astype(str)) == {"question_family_registry.response_role_rules"}


def test_association_candidate_trace_records_low_support_suppression_and_funnel_reason() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    family_var_codes = {
        str(item["var_code"]).upper()
        for role_items in (family_cfg.get("item_role_groups") or {}).values()
        for item in role_items or []
    }
    respondent_ids = [f"r{i}" for i in range(1, 202)]
    family_rows = []
    for respondent_id in respondent_ids:
        family_rows.append(
            {
                "respondent_id": respondent_id,
                "var_code": "ABHLTH",
                "question_id": "Q_ABHLTH",
                "response_value_normalized": "1",
                "response_label": "yes",
                "normalized_response_label": "yes",
                "response_direction": "allow_directionality",
                "response_intensity": 1.0,
                "polarity": "positive",
                "weight_value": 1.0,
                "weight_status": "weighted_valid",
                "is_substantive": True,
                "directionality_status": "inferred_from_directionality_overlay",
                "response_semantics_source": "response_option_map",
                "semantic_role": "relation_evidence",
                "source_structure_classification": "substantive",
                "allowed_as_association_feature": True,
                "allowed_as_attitude_cloud_feature": True,
                "not_direct_evidence": False,
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "survey_year": 1972,
            }
        )
    outside_row = {
        "respondent_id": "r1",
        "var_code": "PARTYID",
        "question_id": "Q_PARTYID",
        "response_value_normalized": "democrat",
        "response_label": "democrat",
        "normalized_response_label": "democrat",
        "response_direction": "",
        "response_intensity": 1.0,
        "polarity": "",
        "weight_value": 1.0,
        "weight_status": "weighted_valid",
        "is_substantive": True,
        "directionality_status": "inferred_from_response_family",
        "response_semantics_source": "response_option_map",
        "semantic_role": "relation_evidence",
        "source_structure_classification": "substantive",
        "allowed_as_association_feature": True,
        "allowed_as_attitude_cloud_feature": True,
        "not_direct_evidence": False,
        "source": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "country_code": "US",
        "survey_year": 1972,
    }
    respondent_df = pd.DataFrame(family_rows)
    context_frame = pd.concat([respondent_df, pd.DataFrame([outside_row])], ignore_index=True, sort=False)
    pattern_df = pd.DataFrame(
        [
            {
                "run_id": "run1",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "family_id": family_cfg["family_id"],
                "pattern_id": "pattern_1",
                "respondent_ids": respondent_ids,
                "pattern_count_unweighted": len(respondent_ids),
                "pattern_count_weighted": float(len(respondent_ids)),
                "support_status": "sufficient_support",
                "confidence_score": 80.0,
                "boundary_pattern_type": "broad_support",
                "item_rows": [],
            }
        ]
    )
    candidate_trace = _association_candidate_trace_rows(
        pattern_df,
        respondent_df,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
        association_support_threshold=30,
    )
    assert not candidate_trace.empty
    assert int(candidate_trace.attrs["candidate_pairs_formed"]) > 0
    assert int(candidate_trace.attrs["candidate_pairs_published"]) == 0
    assert "below publishable support threshold" in set(candidate_trace["association_publication_reason"].astype(str))
    assert set(candidate_trace["association_lane"].astype(str)) == {"substantive_attitude_association"}
    funnel = _association_eligibility_funnel(
        family_cfg=family_cfg,
        respondent_df=respondent_df,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
        association_index=pd.DataFrame(columns=["family_id", "pattern_id"]),
        candidate_trace=candidate_trace,
        run_id="run1",
        source_id="GSS",
        source="GSS",
        wave="1972",
        canonical_wave="1972",
        country_code="US",
    )
    assert not funnel.empty
    row = funnel.iloc[0]
    assert int(row["candidate_pairs_formed"]) == int(candidate_trace.attrs["candidate_pairs_formed"])
    assert int(row["candidate_pairs_published"]) == 0
    assert row["association_empty_reason"] == "eligible_rows_below_support_threshold"
    assert row["association_lane_summary"]["substantive_attitude_association"] == 1


def test_association_candidate_trace_recovers_response_value_from_raw_context_columns() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    family_var_codes = {
        str(item["var_code"]).upper()
        for role_items in (family_cfg.get("item_role_groups") or {}).values()
        for item in role_items or []
    }
    respondent_ids = [f"r{i}" for i in range(1, 202)]
    family_rows = []
    for respondent_id in respondent_ids:
        family_rows.append(
            {
                "respondent_id": respondent_id,
                "var_code": "ABHLTH",
                "question_id": "Q_ABHLTH",
                "response_value_normalized": "1",
                "response_label": "yes",
                "normalized_response_label": "yes",
                "response_direction": "allow_directionality",
                "response_intensity": 1.0,
                "polarity": "positive",
                "weight_value": 1.0,
                "weight_status": "weighted_valid",
                "is_substantive": True,
                "directionality_status": "inferred_from_directionality_overlay",
                "response_semantics_source": "response_option_map",
                "semantic_role": "relation_evidence",
                "source_structure_classification": "substantive",
                "allowed_as_association_feature": True,
                "allowed_as_attitude_cloud_feature": True,
                "not_direct_evidence": False,
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "survey_year": 1972,
            }
        )
    outside_row = {
        "respondent_id": "r1",
        "var_code": "PARTYID",
        "question_id": "Q_PARTYID",
        "value_raw": "1",
        "value_text": "democrat",
        "response_label": "",
        "normalized_response_label": "",
        "response_direction": "",
        "response_intensity": 1.0,
        "polarity": "",
        "weight_value": 1.0,
        "weight_status": "weighted_valid",
        "is_substantive": True,
        "directionality_status": "inferred_from_response_family",
        "response_semantics_source": "response_option_map",
        "semantic_role": "relation_evidence",
        "source_structure_classification": "substantive",
        "allowed_as_association_feature": True,
        "allowed_as_attitude_cloud_feature": True,
        "not_direct_evidence": False,
        "source": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "country_code": "US",
        "survey_year": 1972,
    }
    respondent_df = pd.DataFrame(family_rows)
    context_frame = pd.concat([respondent_df, pd.DataFrame([outside_row])], ignore_index=True, sort=False)
    pattern_df = pd.DataFrame(
        [
            {
                "run_id": "run1",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "family_id": family_cfg["family_id"],
                "pattern_id": "pattern_1",
                "respondent_ids": respondent_ids,
                "pattern_count_unweighted": len(respondent_ids),
                "pattern_count_weighted": float(len(respondent_ids)),
                "support_status": "sufficient_support",
                "confidence_score": 80.0,
                "boundary_pattern_type": "broad_support",
                "item_rows": [],
            }
        ]
    )
    candidate_trace = _association_candidate_trace_rows(
        pattern_df,
        respondent_df,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
    )
    assert not candidate_trace.empty
    assert int(candidate_trace.attrs["eligible_rows_with_response_value"]) > 0
    assert int(candidate_trace.attrs["eligible_rows_missing_response_value"]) == 0
    assert "democrat" in set(candidate_trace["associated_response_value_normalized"].astype(str))
    assert "low_response_overlap" in set(candidate_trace["suppression_reason"].astype(str))
    assert set(candidate_trace["association_lane"].astype(str)) == {"substantive_attitude_association"}


def test_association_candidate_trace_keeps_underpowered_candidate_nonpublishable() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    family_var_codes = {
        str(item["var_code"]).upper()
        for role_items in (family_cfg.get("item_role_groups") or {}).values()
        for item in role_items or []
    }
    respondent_id = "r1"
    family_frame = pd.DataFrame(
        [
            {
                "respondent_id": respondent_id,
                "var_code": "ABDEFECT",
                "question_id": "Q_ABDEFECT",
                "response_value_normalized": "1",
                "response_label": "1.0",
                "normalized_response_label": "1.0",
                "response_direction": "allow_directionality",
                "response_intensity": 1.0,
                "polarity": "positive",
                "weight_value": 1.0,
                "weight_status": "weighted_valid",
                "is_substantive": True,
                "directionality_status": "inferred_from_directionality_overlay",
                "response_semantics_source": "response_option_map",
                "semantic_role": "relation_evidence",
                "source_structure_classification": "substantive",
                "allowed_as_association_feature": True,
                "allowed_as_attitude_cloud_feature": True,
                "not_direct_evidence": False,
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "survey_year": 1972,
            }
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": respondent_id,
                        "var_code": "PARTYID",
                        "question_id": "Q_PARTYID",
                        "value_raw": "2.0",
                        "value_text": "2.0",
                        "response_label": "",
                        "normalized_response_label": "",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 1.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "directionality_status": "inferred_from_response_family",
                        "response_semantics_source": "response_option_map",
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "allowed_as_association_feature": True,
                        "allowed_as_attitude_cloud_feature": True,
                        "not_direct_evidence": False,
                        "source": "GSS",
                        "wave": "1972",
                        "canonical_wave": "1972",
                        "country_code": "US",
                        "survey_year": 1972,
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    pattern_df = pd.DataFrame(
        [
            {
                "run_id": "run1",
                "source": "GSS",
                "wave": "1972",
                "canonical_wave": "1972",
                "country_code": "US",
                "family_id": family_cfg["family_id"],
                "pattern_id": "pattern_1",
                "respondent_ids": [respondent_id],
                "pattern_count_unweighted": 1,
                "pattern_count_weighted": 1.0,
                "support_status": "sufficient_support",
                "confidence_score": 80.0,
                "boundary_pattern_type": "broad_support",
                "item_rows": [],
            }
        ]
    )
    candidate_trace = _association_candidate_trace_rows(
        pattern_df,
        family_frame,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
    )
    assert not candidate_trace.empty
    assert int(candidate_trace.attrs["candidate_pairs_formed"]) == 1
    assert int(candidate_trace.attrs["candidate_pairs_published"]) == 0
    assert "candidate_pair_suppressed" in set(candidate_trace["candidate_stage"].astype(str))
    assert set(candidate_trace["association_publication_status"].astype(str)) == {"diagnostic_only_low_overlap"}
    association_index = _association_rows(
        pattern_df,
        family_frame,
        context_frame=context_frame,
        family_var_codes=family_var_codes,
    )
    assert association_index.empty


def test_relation_signature_summarizes_target_grain_fields() -> None:
    pattern_df = pd.DataFrame(
        [
            {
                "pattern_id": "p1",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "battery",
                "item_rows": [
                    {
                        "target_entity_id": "abortion_permission",
                        "target_domain": "reproductive_moral_regulation",
                        "target_condition_label": "woman_health",
                        "permission_domain": "abortion_permission",
                        "target_resolution_grain": "condition_label",
                        "target_resolution_status": "family_registry_resolved_condition",
                    },
                    {
                        "target_entity_id": "abortion_permission",
                        "target_domain": "reproductive_moral_regulation",
                        "target_condition_label": "rape",
                        "permission_domain": "abortion_permission",
                        "target_resolution_grain": "condition_label",
                        "target_resolution_status": "family_registry_resolved_condition",
                    },
                ],
                "support_status": "clears_threshold",
                "confidence_score": 90.0,
            }
        ]
    )
    relation_index = _relation_signature_rows(pattern_df)
    assert not relation_index.empty
    row = relation_index.iloc[0]
    assert row["target_resolution_status"] == "family_registry_resolved_condition"
    assert float(row["condition_label_share"]) == 1.0
    assert float(row["target_group_share"]) == 0.0
    assert float(row["permission_domain_share"]) == 1.0
    assert row["target_resolution_grain_summary"]["condition_label"] == 2
    assert row["target_condition_label_set"] == ["rape", "woman_health"]


def test_response_role_rule_validation_guards_block_and_allow() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    blocked_cfg = {
        **family_cfg,
        "response_role_rules": [
            {
                **family_cfg["response_role_rules"][0],
                "validated_waves": ["1984"],
                "expected_response_label_contains_any": ["yes"],
                "allow_unlabeled_numeric_fallback": False,
            }
        ],
    }
    allowed_numeric_cfg = {
        **family_cfg,
        "response_role_rules": [
            {
                **family_cfg["response_role_rules"][0],
                "validated_waves": ["1984"],
                "expected_response_label_contains_any": ["yes"],
                "allow_unlabeled_numeric_fallback": True,
            }
        ],
    }
    item_meta = {"item_role": "exception_case", "condition_label": "woman_health"}
    base_row = {
        "var_code": "ABHLTH",
        "response_value_normalized": "1",
        "response_direction": "",
        "polarity": "",
        "response_option_map_matched": False,
        "response_semantics_source": "observed_response_row",
        "directionality_status": "unknown",
        "response_semantics_status": "observed_only",
        "canonical_wave": "1984",
    }
    allowed = _resolve_family_item_semantics(
        pd.Series({**base_row, "response_label": "yes", "wave": "1984"}),
        family_cfg=blocked_cfg,
        item_meta=item_meta,
    )
    blocked_wave = _resolve_family_item_semantics(
        pd.Series({**base_row, "response_label": "yes", "wave": "1972"}),
        family_cfg=blocked_cfg,
        item_meta=item_meta,
    )
    blocked_label = _resolve_family_item_semantics(
        pd.Series({**base_row, "response_label": "maybe", "wave": "1984"}),
        family_cfg=blocked_cfg,
        item_meta=item_meta,
    )
    numeric_fallback = _resolve_family_item_semantics(
        pd.Series({**base_row, "response_label": "1.0", "wave": "1984"}),
        family_cfg=allowed_numeric_cfg,
        item_meta=item_meta,
    )
    blocked_missing_label = _resolve_family_item_semantics(
        pd.Series({**base_row, "response_label": "", "wave": "1984"}),
        family_cfg=blocked_cfg,
        item_meta=item_meta,
    )
    assert allowed["semantic_response_role"] == "support"
    assert allowed["semantic_response_role_status"] == "family_registry_fallback_authorized"
    assert blocked_wave["semantic_response_role"] == "unknown"
    assert blocked_wave["semantic_response_role_status"] == "family_registry_rule_wave_not_validated"
    assert blocked_label["semantic_response_role"] == "unknown"
    assert blocked_label["semantic_response_role_status"] == "family_registry_rule_label_mismatch"
    assert numeric_fallback["semantic_response_role"] == "support"
    assert numeric_fallback["semantic_response_role_status"] == "family_registry_fallback_authorized"
    assert numeric_fallback["response_semantics_authority_source"] == "question_family_registry.response_role_rules"
    assert numeric_fallback["directionality_authority_source"] == "question_family_registry.response_role_rules"
    assert blocked_missing_label["semantic_response_role"] == "unknown"
    assert blocked_missing_label["semantic_response_role_status"] == "family_registry_rule_missing_label_guard"


def test_upstream_response_option_map_authority_wins_over_fallback() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    row = pd.Series(
        {
            "var_code": "ABHLTH",
            "response_value_normalized": "1",
            "response_label": "yes",
            "normalized_response_label": "yes",
            "response_direction": "positive",
            "polarity": "positive",
            "response_option_map_matched": True,
            "response_semantics_source": "response_option_map",
            "directionality_status": "inferred_from_directionality_overlay",
            "response_semantics_status": "curated",
            "wave": "1984",
            "canonical_wave": "1984",
        }
    )
    resolved = _resolve_family_item_semantics(
        row,
        family_cfg=family_cfg,
        item_meta={"item_role": "exception_case", "condition_label": "woman_health"},
    )
    assert resolved["semantic_response_role"] == "support"
    assert resolved["response_semantics_authority_source"] == "response_option_map"
    assert resolved["directionality_authority_source"] == "response_option_map"


def test_boundary_rule_diagnostics_report_match_and_failure() -> None:
    family_cfg = _registry_family_cfg("gss_abortion_condition_family")
    matched_rows = [
        {"item_role": "exception_case", "semantic_response_role": "support", "condition_label": "woman_health"},
        {"item_role": "elective_case", "semantic_response_role": "oppose", "condition_label": "any_reason"},
        {"item_role": "social_condition", "semantic_response_role": "support", "condition_label": "unmarried"},
    ]
    matched_type, matched_diag = _evaluate_boundary_rules(family_cfg, Counter({"support": 2, "oppose": 1}), matched_rows)
    assert matched_type == "exception_support_elective_opposition"
    assert matched_diag["boundary_rule_status"] == "exception_support_elective_opposition"
    assert matched_diag["boundary_rule_evaluation_summary"]
    assert matched_diag["rules_matched"]
    failed_rows = [
        {"item_role": "social_condition", "semantic_response_role": "support", "condition_label": "unmarried"},
        {"item_role": "elective_case", "semantic_response_role": "oppose", "condition_label": "any_reason"},
    ]
    failed_type, failed_diag = _evaluate_boundary_rules(family_cfg, Counter({"support": 1, "oppose": 1}), failed_rows)
    assert failed_type == "mixed_unclassified"
    assert failed_diag["boundary_rule_status"] == "mixed_unclassified"
    assert "missing_exception_case_support" in set(failed_diag["boundary_rule_failure_reasons"].values())
    assert failed_diag["rules_failed"]


def test_association_funnel_reports_missing_authority_and_empty_reason() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=None)
    funnel = _association_eligibility_funnel(
        family_cfg=family_cfg,
        respondent_df=family_frame,
        context_frame=None,
        family_var_codes={"ABRAPE", "ABHLTH", "ABDEFECT"},
        association_index=tables["joint_pattern_association_index"],
        run_id="run1",
        source_id="GSS",
        source="GSS",
        wave="1984",
        canonical_wave="1984",
        country_code="US",
    )
    assert not funnel.empty
    row = funnel.iloc[0]
    assert row["association_context_status"] == "association_context_unavailable"
    assert row["association_empty_reason"] == "association_context_unavailable"


def test_association_funnel_reports_missing_authority_and_metadata_blocks() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    ).assign(allowed_as_association_feature=True, is_substantive=True)
    missing_authority_context = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    missing_authority_funnel = _association_eligibility_funnel(
        family_cfg=family_cfg,
        respondent_df=family_frame,
        context_frame=missing_authority_context,
        family_var_codes={"ABRAPE", "ABHLTH", "ABDEFECT"},
        association_index=pd.DataFrame(columns=["family_id"]),
        run_id="run1",
        source_id="GSS",
        source="GSS",
        wave="1984",
        canonical_wave="1984",
        country_code="US",
    )
    assert missing_authority_funnel.iloc[0]["association_empty_reason"] == "association_context_authority_missing"
    assert int(missing_authority_funnel.iloc[0]["outside_family_rows_blocked_missing_authority"]) == 1

    metadata_context = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "meta1",
                        "question_id": "QM",
                        "response_value_normalized": "context",
                        "response_label": "context",
                        "normalized_response_label": "context",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": False,
                        "allowed_as_association_feature": False,
                        "semantic_role": "metadata",
                        "source_structure_classification": "metadata",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    metadata_funnel = _association_eligibility_funnel(
        family_cfg=family_cfg,
        respondent_df=family_frame,
        context_frame=metadata_context,
        family_var_codes={"ABRAPE", "ABHLTH", "ABDEFECT"},
        association_index=pd.DataFrame(columns=["family_id"]),
        run_id="run1",
        source_id="GSS",
        source="GSS",
        wave="1984",
        canonical_wave="1984",
        country_code="US",
    )
    assert metadata_funnel.iloc[0]["association_empty_reason"] == "all_rows_blocked_metadata_context"
    assert int(metadata_funnel.iloc[0]["outside_family_rows_blocked_metadata_context"]) == 1



def test_selective_tolerance_requires_distinct_condition_labels() -> None:
    family_cfg = _registry_family_cfg("gss_civil_liberties_speak_family")
    item_rows = [
        {"item_role": "target_case", "condition_label": "communist", "semantic_response_role": "support"},
        {"item_role": "target_case", "condition_label": "communist", "semantic_response_role": "oppose"},
    ]
    semantic_counts = Counter(row["semantic_response_role"] for row in item_rows)
    assert _boundary_pattern_type(family_cfg, semantic_counts, item_rows) == "mixed_unclassified"


def test_minimum_items_answered_gate_excludes_short_respondents_and_audits() -> None:
    family_cfg = _family_cfg(minimum_items_answered=3)
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=1.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    assert tables["joint_response_pattern_index"].empty
    assert not tables["joint_pattern_audit"].empty
    issue_types = tables["joint_pattern_audit"]["issue_type"].astype(str).tolist()
    assert issue_types.count("respondents_below_minimum_items_answered") == 1


def test_position_signature_rows_populate_and_use_weighting() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abhlth", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abdefect", "2", "disallow_directionality", sex="M", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    position_index = tables["joint_pattern_position_signature"]
    assert not position_index.empty
    female_rows = position_index[position_index["indicator_name"].astype(str).eq("sex") & position_index["indicator_value"].astype(str).eq("F")]
    assert not female_rows.empty
    assert float(female_rows.iloc[0]["n_weighted"]) == 10.0
    assert int(female_rows.iloc[0]["n_unweighted"]) == 1


def test_pattern_probabilities_keep_weighted_and_unweighted_separate() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abhlth", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abdefect", "2", "disallow_directionality", sex="M", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    assert any(abs(row.pattern_probability_weighted - row.pattern_probability_unweighted) > 1e-6 for row in pattern_df.itertuples(index=False))


def test_item_index_carries_directionality_authority_fields() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    item_index = tables["joint_response_pattern_item_index"]
    assert not item_index.empty
    for field in [
        "directionality_status",
        "directionality_authority_source",
        "directionality_basis_source",
        "response_semantics_authority_source",
        "semantic_response_role",
        "semantic_response_role_status",
        "semantic_response_role_authority",
        "response_direction",
        "polarity",
        "target_entity_id",
        "target_domain",
        "target_condition_label",
        "target_group_label",
        "permission_domain",
        "target_resolution_grain",
        "target_resolution_status",
        "target_resolution_authority_source",
        "target_resolution_basis_source",
    ]:
        assert field in item_index.columns


def test_position_signature_separates_pattern_and_cell_support() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abhlth", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abdefect", "2", "disallow_directionality", sex="M", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    position_index = tables["joint_pattern_position_signature"]
    assert not position_index.empty
    for field in [
        "pattern_support_status",
        "pattern_support_n_unweighted",
        "pattern_support_n_weighted",
        "pattern_support_gate_status",
        "position_cell_support_status",
        "position_cell_n_unweighted",
        "position_cell_n_weighted",
        "position_cell_support_ratio",
        "position_cell_support_gate_status",
    ]:
        assert field in position_index.columns
    sex_f = position_index[position_index["indicator_name"].astype(str).eq("sex") & position_index["indicator_value"].astype(str).eq("F")]
    assert not sex_f.empty
    assert sex_f.iloc[0]["pattern_support_status"] in {"sufficient_support", "underpowered", "missing_support", "not_applicable", "zero_support"}
    assert sex_f.iloc[0]["position_cell_support_status"] in {"sufficient_support", "underpowered", "missing_support", "not_applicable", "zero_support"}


def test_outside_family_associations_do_not_emit_family_items() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abhlth", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abdefect", "2", "disallow_directionality", sex="M", weight_value=1.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 1.0,
                        "weight_status": "weighted",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    },
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    association_index = tables["joint_pattern_association_index"]
    candidate_trace = tables["joint_pattern_association_candidate_trace"]
    assert association_index.empty
    assert not candidate_trace.empty
    assert set(candidate_trace["var_code"].astype(str).str.upper()) == {"OTHER1"}
    assert set(candidate_trace["association_publication_status"].astype(str)) == {"diagnostic_only_raw_component"}
    assert set(candidate_trace["association_strength_status"].astype(str)) == {"not_computed_phase4_pending"}
    assert set(candidate_trace["denominator_basis"].astype(str)) == {"answered_var_within_pattern"}


def test_metadata_context_rows_are_suppressed_from_associations() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "meta1",
                        "question_id": "QM",
                        "response_value_normalized": "context",
                        "response_label": "context",
                        "normalized_response_label": "context",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": False,
                        "semantic_role": "metadata",
                        "source_structure_classification": "metadata",
                        "allowed_as_attitude_cloud_feature": False,
                        "allowed_as_runtime_persona_evidence": False,
                        "allowed_as_association_feature": False,
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "allowed_as_attitude_cloud_feature": True,
                        "allowed_as_runtime_persona_evidence": True,
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    association_index = tables["joint_pattern_association_index"]
    candidate_trace = tables["joint_pattern_association_candidate_trace"]
    assert association_index.empty
    assert not candidate_trace.empty
    assert set(candidate_trace["var_code"].astype(str).str.upper()) == {"OTHER1"}
    assert set(candidate_trace["association_publication_status"].astype(str)) == {"diagnostic_only_raw_component"}


def test_metadata_blocked_rows_are_audited_and_not_emitted() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "meta1",
                        "question_id": "QM",
                        "response_value_normalized": "context",
                        "response_label": "context",
                        "normalized_response_label": "context",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "semantic_role": "metadata",
                        "source_structure_classification": "metadata",
                        "allowed_as_association_feature": True,
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "allowed_as_attitude_cloud_feature": True,
                        "allowed_as_runtime_persona_evidence": True,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    assert tables["joint_pattern_association_index"].empty
    assert "association_rows_suppressed_metadata_context" in set(tables["joint_pattern_audit"]["issue_type"].astype(str))


def test_association_rows_fail_closed_without_positive_authority() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": True,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    assert tables["joint_pattern_association_index"].empty
    audit_issues = set(tables["joint_pattern_audit"]["issue_type"].astype(str))
    assert "association_context_authority_missing" in audit_issues or "family_vars_missing_in_wave" in audit_issues


def test_association_context_unavailable_is_audited_when_directly_compiled() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=None)
    audit = tables["joint_pattern_audit"]
    assert not audit.empty
    assert "association_context_unavailable" in set(audit["issue_type"].astype(str))
    assert tables["joint_pattern_association_index"].empty


def test_not_direct_evidence_allowed_emits_diagnostic_association() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": True,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    association_index = tables["joint_pattern_association_index"]
    candidate_trace = tables["joint_pattern_association_candidate_trace"]
    assert association_index.empty
    assert not candidate_trace.empty
    assert set(candidate_trace["association_eligibility_status"].astype(str)) == {"eligible_diagnostic_association"}
    assert set(candidate_trace["direct_evidence_status"].astype(str)) == {"not_direct_evidence"}
    assert set(candidate_trace["association_lane"].astype(str)) == {"diagnostic_numeric_context"}
    assert set(candidate_trace["association_lane_status"].astype(str)) == {"diagnostic"}
    assert set(candidate_trace["association_publication_status"].astype(str)) == {"diagnostic_only_raw_component"}


def test_not_direct_evidence_without_permission_is_blocked_and_audited() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": False,
                        "allowed_as_attitude_cloud_feature": False,
                        "not_direct_evidence": True,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": True,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    assert tables["joint_pattern_association_index"].empty
    assert "blocked_not_direct_evidence" in set(tables["joint_pattern_audit"]["issue_type"].astype(str))


def test_thin_compile_skips_diagnostics_and_refuses_unauthorized_association_rows() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "partyid",
                        "question_id": "QX",
                        "response_value_normalized": "democrat",
                        "response_label": "democrat",
                        "normalized_response_label": "democrat",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(
        family_cfg,
        family_questions,
        family_frame,
        context_frame=context_frame,
        emit_diagnostics=False,
    )
    assert tables["joint_pattern_association_index"].empty
    assert tables["joint_pattern_association_candidate_trace"].empty
    assert tables["joint_pattern_audit"].empty


def test_family_tables_funnel_only_skips_association_candidate_loop(monkeypatch: pytest.MonkeyPatch) -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "partyid",
                        "question_id": "QX",
                        "response_value_normalized": "democrat",
                        "response_label": "democrat",
                        "normalized_response_label": "democrat",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    monkeypatch.setattr(
        "data.ddm_build_copy.ddm_v550j_joint_patterns._association_candidate_trace_rows",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("candidate trace should not run in funnel_only mode")),
    )
    monkeypatch.setattr(
        "data.ddm_build_copy.ddm_v550j_joint_patterns._association_rows",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("association rows should not run in funnel_only mode")),
    )
    tables = compile_v550j_family_tables(
        family_cfg,
        family_questions,
        family_frame,
        context_frame=context_frame,
        association_mode="funnel_only",
        emit_diagnostics=True,
    )
    assert tables["joint_pattern_association_index"].empty
    assert tables["joint_pattern_association_candidate_trace"].empty
    assert "association_mode_funnel_only" in set(tables["joint_pattern_audit"]["issue_type"].astype(str))


def test_not_direct_evidence_direct_row_remains_eligible() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    context_frame = pd.concat(
        [
            family_frame,
            pd.DataFrame(
                [
                    {
                        "respondent_id": "r1",
                        "var_code": "other1",
                        "question_id": "QX",
                        "response_value_normalized": "A",
                        "response_label": "A",
                        "normalized_response_label": "A",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "F",
                    },
                    {
                        "respondent_id": "r2",
                        "var_code": "other1",
                        "question_id": "QY",
                        "response_value_normalized": "B",
                        "response_label": "B",
                        "normalized_response_label": "B",
                        "response_direction": "",
                        "response_intensity": 1.0,
                        "polarity": "",
                        "weight_value": 10.0,
                        "weight_status": "weighted_valid",
                        "is_substantive": True,
                        "allowed_as_association_feature": True,
                        "not_direct_evidence": False,
                        "semantic_role": "relation_evidence",
                        "source_structure_classification": "substantive",
                        "source": "GSS",
                        "wave": "1984",
                        "canonical_wave": "1984",
                        "country_code": "US",
                        "survey_year": 1984,
                        "sex": "M",
                    }
                ]
            ),
        ],
        ignore_index=True,
        sort=False,
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=context_frame)
    association_index = tables["joint_pattern_association_index"]
    candidate_trace = tables["joint_pattern_association_candidate_trace"]
    assert association_index.empty
    assert not candidate_trace.empty
    assert set(candidate_trace["association_eligibility_status"].astype(str)) == {"eligible"}
    assert set(candidate_trace["direct_evidence_status"].astype(str)) == {"direct_or_not_flagged"}
    assert set(candidate_trace["association_lane"].astype(str)) == {"substantive_attitude_association"}
    assert set(candidate_trace["association_lane_status"].astype(str)) == {"semantic_role_rule"}
    assert set(candidate_trace["association_publication_status"].astype(str)) == {"diagnostic_only_low_overlap"}


def test_weight_status_invalid_when_zero_or_negative_weights_present() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "1", "allow_directionality", sex="M", weight_value=0.0),
            _row("r2", "abhlth", "1", "allow_directionality", sex="M", weight_value=0.0),
            _row("r2", "abdefect", "1", "allow_directionality", sex="M", weight_value=0.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    assert set(pattern_df["weight_status"].astype(str)).issubset({"weighted_valid", "weighted_partial", "weights_invalid", "weights_missing"})
    assert "weights_invalid" in set(pattern_df["weight_status"].astype(str))
    assert not bool(pattern_df["weighted_count_validation_passed"].all())
    assert float(pattern_df.loc[pattern_df["weight_status"].astype(str).eq("weights_invalid"), "n_weighted"].min()) == float(pattern_df.loc[pattern_df["weight_status"].astype(str).eq("weights_invalid"), "n_unweighted"].min())


def test_all_missing_weights_use_unweighted_fallback_counts() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=float("nan")),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=float("nan")),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=float("nan")),
            _row("r2", "abrape", "1", "allow_directionality", sex="M", weight_value=float("nan")),
            _row("r2", "abhlth", "1", "allow_directionality", sex="M", weight_value=float("nan")),
            _row("r2", "abdefect", "1", "allow_directionality", sex="M", weight_value=float("nan")),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    row = pattern_df.iloc[0]
    assert row["weight_status"] == "weights_missing"
    assert row["pattern_probability_basis"] == "unweighted_fallback"
    assert row["weighted_count_basis"] == "unweighted_fallback"
    assert float(row["pattern_count_weighted"]) == float(row["pattern_count_unweighted"])
    assert float(row["n_weighted"]) == float(row["n_unweighted"])


def test_partial_weights_preserve_partial_basis() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=1.2),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=float("nan")),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=0.8),
            _row("r2", "abrape", "1", "allow_directionality", sex="M", weight_value=1.1),
            _row("r2", "abhlth", "1", "allow_directionality", sex="M", weight_value=float("nan")),
            _row("r2", "abdefect", "1", "allow_directionality", sex="M", weight_value=0.9),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    assert "weighted_partial" in set(pattern_df["weight_status"].astype(str))
    assert "weighted_partial" in set(pattern_df["pattern_probability_basis"].astype(str))
    assert "weighted_partial" in set(pattern_df["weighted_count_basis"].astype(str))


def test_valid_weights_use_weighted_valid_basis() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=1.2),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=1.2),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=1.2),
            _row("r2", "abrape", "1", "allow_directionality", sex="M", weight_value=0.8),
            _row("r2", "abhlth", "1", "allow_directionality", sex="M", weight_value=0.8),
            _row("r2", "abdefect", "1", "allow_directionality", sex="M", weight_value=0.8),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    assert not pattern_df.empty
    assert "weighted_valid" in set(pattern_df["weight_status"].astype(str))
    assert "weighted_valid" in set(pattern_df["pattern_probability_basis"].astype(str))
    assert "weighted_valid" in set(pattern_df["weighted_count_basis"].astype(str))


def test_relation_signature_is_aggregated_and_flags_mixed_mapping() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    relation_index = tables["joint_pattern_relation_signature"]
    assert not relation_index.empty
    row = relation_index.iloc[0]
    assert "aggregated_pattern_relation_signature" == str(row["relation_signature_status"])
    assert isinstance(row["driver_id_set"], list)
    assert isinstance(row["target_entity_id_set"], list)
    assert "target_resolution_status_summary" in relation_index.columns
    assert "infer_placeholder_share" in relation_index.columns
    assert "registry_resolved_share" in relation_index.columns
    assert "mapping_coverage_score" in relation_index.columns


def test_relation_signature_marks_expected_multi_target_batteries_cleanly() -> None:
    pattern_df = pd.DataFrame(
        [
            {
                "pattern_id": "p1",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "target_selective_tolerance_battery",
                "family_structure_type": "target_selective_battery",
                "expected_multi_target": True,
                "item_rows": [
                    {
                        "driver_id": "driver1",
                        "driver_facet_id": "facet1",
                        "relation_axis_id": "axis1",
                        "target_entity_id": "target_a",
                        "target_group_label": "group_a",
                        "target_resolution_grain": "target_group",
                        "target_resolution_status": "family_registry_resolved_group",
                        "mapping_status": "mapped",
                        "semantic_role": "target_case",
                        "v551_evidence_role": "DIRECT_RELATION_RESPONSE",
                    },
                    {
                        "driver_id": "driver1",
                        "driver_facet_id": "facet1",
                        "relation_axis_id": "axis1",
                        "target_entity_id": "target_b",
                        "target_group_label": "group_b",
                        "target_resolution_grain": "target_group",
                        "target_resolution_status": "family_registry_resolved_group",
                        "mapping_status": "mapped",
                        "semantic_role": "target_case",
                        "v551_evidence_role": "DIRECT_RELATION_RESPONSE",
                    },
                ],
                "support_status": "clears_threshold",
                "confidence_score": 90.0,
            }
        ]
    )
    relation_index = _relation_signature_rows(pattern_df)
    assert not relation_index.empty
    row = relation_index.iloc[0]
    assert row["semantic_conflict_status"] == "expected_multi_target_battery"
    assert row["target_structure_status"] == "target_selective_battery"
    assert row["target_selectivity_profile"] == "target_selective_tolerance"


def test_relation_signature_classifies_blank_targets_as_unresolved() -> None:
    pattern_df = pd.DataFrame(
        [
            {
                "pattern_id": "p1",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "battery",
                "item_rows": [
                    {"target_entity_id": ""},
                    {"target_entity_id": None},
                    {"target_entity_id": "unknown"},
                ],
                "support_status": "clears_threshold",
                "confidence_score": 90.0,
            }
        ]
    )
    relation_index = _relation_signature_rows(pattern_df)
    assert not relation_index.empty
    row = relation_index.iloc[0]
    assert row["target_resolution_status"] == "unresolved"
    assert float(row["unresolved_target_share"]) == 1.0
    assert float(row["registry_resolved_share"]) == 0.0
    assert float(row["infer_placeholder_share"]) == 0.0


def test_relation_signature_distinguishes_mixed_resolution_and_no_target_items() -> None:
    mixed_df = pd.DataFrame(
        [
            {
                "pattern_id": "p2",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "battery",
                "item_rows": [
                    {"target_entity_id": "state_authority"},
                    {"target_entity_id": "infer_family"},
                    {"target_entity_id": ""},
                ],
                "support_status": "clears_threshold",
                "confidence_score": 90.0,
            }
        ]
    )
    mixed_relation = _relation_signature_rows(mixed_df).iloc[0]
    assert mixed_relation["target_resolution_status"] == "mixed_resolution"
    assert float(mixed_relation["registry_resolved_share"]) == 1 / 3
    assert float(mixed_relation["infer_placeholder_share"]) == 1 / 3
    assert float(mixed_relation["unresolved_target_share"]) == 1 / 3

    empty_df = pd.DataFrame(
        [
            {
                "pattern_id": "p3",
                "family_id": "fam",
                "family_label": "fam",
                "family_type": "battery",
                "item_rows": [],
                "support_status": "clears_threshold",
                "confidence_score": 90.0,
            }
        ]
    )
    empty_relation = _relation_signature_rows(empty_df).iloc[0]
    assert empty_relation["target_resolution_status"] == "no_target_items"
    assert float(empty_relation["unresolved_target_share"]) == 1.0
    assert float(empty_relation["registry_resolved_share"]) == 0.0
    assert float(empty_relation["infer_placeholder_share"]) == 0.0


def test_boundary_and_probability_fields_keep_weighted_and_unweighted_separate() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r2", "abrape", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abhlth", "2", "disallow_directionality", sex="M", weight_value=1.0),
            _row("r2", "abdefect", "2", "disallow_directionality", sex="M", weight_value=1.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame)
    pattern_df = tables["joint_response_pattern_index"]
    boundary_df = tables["question_family_boundary_pattern_index"]
    assert not pattern_df.empty
    assert not boundary_df.empty
    assert "pattern_probability_unweighted" in pattern_df.columns
    assert "pattern_probability_weighted" in pattern_df.columns
    assert set(pattern_df["pattern_probability_basis"].astype(str)).issubset({"weighted_valid", "weighted_partial", "unweighted_fallback"})
    assert "pct_unweighted" in boundary_df.columns
    assert "pct_weighted" in boundary_df.columns
    assert "pct_basis" in boundary_df.columns


def test_multi_family_frame_aggregation_preserves_all_family_ids() -> None:
    run_tables = {
        "joint_response_pattern_index": [],
        "joint_response_pattern_item_index": [],
        "question_family_boundary_pattern_index": [],
        "joint_pattern_position_signature": [],
        "joint_pattern_relation_signature": [],
        "joint_pattern_association_index": [],
        "joint_pattern_audit": [],
    }
    family_a = pd.DataFrame([{"family_id": "family_a", "pattern_id": "p1"}])
    family_b = pd.DataFrame([{"family_id": "family_b", "pattern_id": "p2"}])
    _append_family_table_frames(
        run_tables,
        {
            "joint_response_pattern_index": family_a,
            "joint_response_pattern_item_index": family_a,
            "question_family_boundary_pattern_index": family_a,
            "joint_pattern_position_signature": family_a,
            "joint_pattern_relation_signature": family_a,
            "joint_pattern_association_index": pd.DataFrame(columns=["family_id", "pattern_id"]),
            "joint_pattern_audit": family_a,
        },
    )
    _append_family_table_frames(
        run_tables,
        {
            "joint_response_pattern_index": family_b,
            "joint_response_pattern_item_index": family_b,
            "question_family_boundary_pattern_index": family_b,
            "joint_pattern_position_signature": family_b,
            "joint_pattern_relation_signature": family_b,
            "joint_pattern_association_index": pd.DataFrame(columns=["family_id", "pattern_id"]),
            "joint_pattern_audit": family_b,
        },
    )
    combined = pd.concat(run_tables["joint_response_pattern_index"], ignore_index=True, sort=False)
    assert set(combined["family_id"].astype(str)) == {"family_a", "family_b"}
    assert len(combined) == 2


def test_empty_association_index_has_canonical_schema() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    family_frame = pd.DataFrame(
        [
            _row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=10.0),
            _row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=10.0),
        ]
    )
    tables = compile_v550j_family_tables(family_cfg, family_questions, family_frame, context_frame=None)
    association_index = tables["joint_pattern_association_index"]
    assert association_index.empty
    required_columns = {
        "run_id",
        "source_id",
        "wave",
        "country_code",
        "family_id",
        "pattern_id",
        "associated_var_code",
        "association_status",
        "association_eligibility_status",
        "association_context_status",
        "association_gate_status",
        "association_strength_status",
        "direct_evidence_status",
        "pattern_member_n_unweighted",
        "pattern_member_n_weighted",
        "pattern_var_answered_n_unweighted",
        "pattern_var_answered_n_weighted",
        "response_overlap_n_unweighted",
        "response_overlap_n_weighted",
        "p_response_given_pattern",
        "p_response_baseline",
        "difference_from_baseline",
        "lift",
        "mutual_information",
        "denominator_basis",
        "baseline_denominator_basis",
        "support_status",
        "support_gate_status",
        "formula_id",
        "formula_version",
    }
    assert required_columns.issubset(set(association_index.columns))


def test_v550j_validation_report_fails_on_family_coverage_mismatch(tmp_path: Path) -> None:
    family_summaries = [
        {"family_id": "family_a"},
        {"family_id": "family_b"},
        {"family_id": "family_c"},
    ]
    family_a = pd.DataFrame([{"family_id": "family_a", "pattern_id": "p1"}])
    family_b = pd.DataFrame([{"family_id": "family_b", "pattern_id": "p2"}])
    table_frames = {
        "joint_response_pattern_index": pd.concat([family_a, family_b], ignore_index=True),
        "question_family_boundary_pattern_index": pd.concat([family_a, family_b], ignore_index=True),
        "joint_pattern_relation_signature": pd.concat([family_a, family_b], ignore_index=True),
        "joint_pattern_position_signature": pd.concat([family_a, family_b], ignore_index=True),
        "joint_pattern_audit": pd.concat([family_a, family_b], ignore_index=True),
        "joint_response_pattern_item_index": pd.concat([family_a, family_b], ignore_index=True),
        "joint_pattern_association_index": pd.DataFrame(columns=["family_id", "pattern_id"]),
    }
    written_tables = {
        key: {"rows": len(value), "schema_path": str(tmp_path / f"{key}.schema.json")}
        for key, value in table_frames.items()
    }
    report = _validate_v550j_run_outputs(
        run_id="gss1972_revalidation_20260612T090403Z",
        shard_id="GSS__1972",
        family_summaries=family_summaries,
        written_tables=written_tables,
        table_frames=table_frames,
        output_dir=tmp_path,
    )
    assert report["validation_status"] == "fail"
    assert "family_c" in report["validation_message"]


@requires_parquet
def test_compile_main_uses_prepared_substrate_without_hot_path_harmonization(monkeypatch, tmp_path: Path) -> None:
    shard_dir = tmp_path / "v550" / "shard_runs" / "gss1972_revalidation_20260612T090403Z" / "GSS__1972"
    core_dir = shard_dir / "core"
    core_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {"var_code": "ABRAPE", "question_id": "Q1", "question_text": "rape?", "wave": "1972", "canonical_wave": "1972", "source": "GSS"},
            {"var_code": "ABHLTH", "question_id": "Q2", "question_text": "health?", "wave": "1972", "canonical_wave": "1972", "source": "GSS"},
            {"var_code": "ABDEFECT", "question_id": "Q3", "question_text": "defect?", "wave": "1972", "canonical_wave": "1972", "source": "GSS"},
        ]
    ).to_parquet(core_dir / "question_use_contract.parquet", index=False)
    pd.DataFrame([{"country_code": "US"}]).to_parquet(shard_dir / "shard_scope.parquet", index=False)

    prepared_frame = pd.DataFrame(
        [
            {
                **_row("r1", "abrape", "1", "allow_directionality", sex="F", weight_value=1.0, wave="1972", canonical_wave="1972", country_code="US"),
                "source_id": "GSS",
                "respondent_id_norm": "r1",
                "var_code_norm": "ABRAPE",
                "source_norm": "GSS",
                "wave_norm": "1972",
                "canonical_wave_norm": "1972",
                "country_code_norm": "US",
                "response_value_norm": "1",
            },
            {
                **_row("r1", "abhlth", "1", "allow_directionality", sex="F", weight_value=1.0, wave="1972", canonical_wave="1972", country_code="US"),
                "source_id": "GSS",
                "respondent_id_norm": "r1",
                "var_code_norm": "ABHLTH",
                "source_norm": "GSS",
                "wave_norm": "1972",
                "canonical_wave_norm": "1972",
                "country_code_norm": "US",
                "response_value_norm": "1",
            },
            {
                **_row("r1", "abdefect", "1", "allow_directionality", sex="F", weight_value=1.0, wave="1972", canonical_wave="1972", country_code="US"),
                "source_id": "GSS",
                "respondent_id_norm": "r1",
                "var_code_norm": "ABDEFECT",
                "source_norm": "GSS",
                "wave_norm": "1972",
                "canonical_wave_norm": "1972",
                "country_code_norm": "US",
                "response_value_norm": "1",
            },
            {
                **_row("r1", "partyid", "3", "allow_directionality", sex="F", weight_value=1.0, wave="1972", canonical_wave="1972", country_code="US"),
                "source_id": "GSS",
                "respondent_id_norm": "r1",
                "var_code_norm": "PARTYID",
                "source_norm": "GSS",
                "wave_norm": "1972",
                "canonical_wave_norm": "1972",
                "country_code_norm": "US",
                "response_value_norm": "3",
            },
        ]
    )

    calls = {"harmonize": 0}

    def forbidden_harmonize(*args, **kwargs):
        calls["harmonize"] += 1
        raise AssertionError("hot-path harmonization should not run in prepared mode")

    def fake_load_cached_country_slice(**kwargs):
        return prepared_frame.copy()

    def fake_load_or_build_substrate(**kwargs):
        frame = kwargs["source_frame"].copy()
        manifest = {
            "cache_loaded": True,
            "cache_valid": True,
            "harmonization_calls": 0,
            "row_count": len(frame),
            "respondent_count": frame["respondent_id_norm"].nunique(),
            "var_count": frame["var_code_norm"].nunique(),
        }
        return frame, manifest

    monkeypatch.setattr(compile_v550j_joint_response_patterns, "_load_response_map", lambda *args, **kwargs: pd.DataFrame())
    monkeypatch.setattr(compile_v550j_joint_response_patterns, "_load_cached_country_slice", fake_load_cached_country_slice)
    monkeypatch.setattr(compile_v550j_joint_response_patterns, "load_or_build_v550j_prepared_substrate", fake_load_or_build_substrate)
    monkeypatch.setattr(compile_v550j_joint_response_patterns, "_harmonize_question_frame", forbidden_harmonize)
    monkeypatch.setattr("data.ddm_build_copy.ddm_v550j_joint_patterns._association_candidate_trace_rows", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("candidate trace should not run in default funnel_only mode")))
    monkeypatch.setattr("data.ddm_build_copy.ddm_v550j_joint_patterns._association_rows", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("association rows should not run in default funnel_only mode")))
    monkeypatch.setattr(compile_v550j_joint_response_patterns, "connect_from_env", lambda *args, **kwargs: None)
    monkeypatch.setattr(sys, "argv", [
        "compile_v550j_joint_response_patterns.py",
        "--v550-shard-dir",
        str(shard_dir),
        "--output-root",
        str(tmp_path / "v550j"),
        "--registry-path",
        str(REGISTRY_PATH),
        "--v550j-substrate-mode",
        "prepared_required",
        "--association-mode",
        "funnel_only",
        "--no-write-csv",
    ])

    exit_code = compile_v550j_joint_response_patterns.main()
    assert exit_code == 0
    assert calls["harmonize"] == 0
    perf_path = tmp_path / "v550j" / "runs" / "gss1972_revalidation_20260612T090403Z" / "GSS__1972" / "joint_patterns" / "v550j_performance_profile.json"
    assert perf_path.exists()
    perf = json.loads(perf_path.read_text(encoding="utf-8"))
    assert int(perf["harmonization_call_count_hot_path"]) == 0
    assert int(perf["substrate_harmonization_calls"]) == 0


def test_family_wave_eligibility_helpers() -> None:
    family_cfg = _family_cfg()
    family_questions = _family_questions()
    assert _family_waves(family_cfg, "GSS") == {"1984"}
    assert _family_wave_values(family_questions, "GSS") == {"1984"}
    assert _family_wave_is_eligible(family_cfg, family_questions, "GSS") is True
    assert _family_wave_is_eligible({**family_cfg, "eligible_waves": ["1972"]}, family_questions, "GSS") is False
