from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

REPO = Path(__file__).resolve().parents[2]
RUNTIME = REPO / "35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE/runtime_reproducibility_code"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
BUILD = RUNTIME / "data/ddm_build_copy"
if str(BUILD) not in sys.path:
    sys.path.insert(0, str(BUILD))

from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (
    canonicalize_shared_respondent_substrate,
    enrich_shared_respondent_substrate_with_question_use_contract,
)
from data.ddm_build_copy.ddm_v551j_packets import _v2_component_denominator_requirement
from data.ddm_build_copy.ddm_v552_structural import build_v552_structural_outputs, validate_v552_v2_1_output_contract
from data.ddm_build_copy.ddm_v552j_exact_integration import build_exact_v552j_integration, validate_exact_v552j_integration
import run_20var_allwaves_v550_552j_smoke as smoke

FIXTURES = Path(__file__).parent / "fixtures/pre553_v552_atoms"


@pytest.mark.parametrize(
    ("filename", "expected_observations"),
    [
        ("afro_r1_ls.csv", 5),
        ("latinobarometro_1995_br.csv", 1),
        ("south_asia_w1_in.csv", 2),
        ("gss_2010_us.csv", 6),
    ],
)
def test_real_v551_atom_surfaces_compile_valid_v552_pressure(filename: str, expected_observations: int) -> None:
    atoms = pd.read_csv(FIXTURES / filename, dtype=object, keep_default_na=False)
    outputs = build_v552_structural_outputs(atoms, run_id=f"fixture_{filename}")
    assert validate_v552_v2_1_output_contract(outputs) == []
    assert len(outputs["v552_pressure_observation_index"]) == expected_observations
    assert len(outputs["v552_to_v552j_pressure_observation_handoff_index"]) == expected_observations
    readiness = outputs["v552_readiness_report"].iloc[0]
    assert readiness["final_status"] == "READY_V552_STRUCTURAL_PRESSURE_CONTRACT"


def test_v551j_denominator_requirement_is_relation_scoped() -> None:
    assert _v2_component_denominator_requirement({
        "component_certification_contribution": "context_component",
        "v551_atom_match_status": "NO_MATCH",
        "v551_allowed_as_v551_relation_evidence": False,
    }) == (False, "NOT_APPLICABLE_NONRELATION_COMPONENT")
    assert _v2_component_denominator_requirement({
        "component_certification_contribution": "relation_component",
        "v551_atom_match_status": "MATCHED_V551_ATOM",
        "v551_allowed_as_v551_relation_evidence": True,
    }) == (True, "RELATION_COMPONENT_DENOMINATOR_REQUIRED")


def test_current_v551j_gate_accepts_current_contract_and_review_lane(tmp_path: Path) -> None:
    root = tmp_path / "v551j"
    (root / "manifest").mkdir(parents=True)
    (root / "packets").mkdir(parents=True)
    for name in [
        "v551j_joint_packet_candidate_index.parquet",
        "v551j_joint_component_index.parquet",
        "v551j_certified_joint_packet_index.parquet",
        "v551j_review_surface.parquet",
    ]:
        (root / "packets" / name).write_bytes(b"fixture")
    (root / "manifest/v551j_readiness_report.json").write_text(json.dumps({
        "final_status": "PARTIAL_READY_V551J_CONTEXT_ONLY",
        "candidate_packet_count": 4,
        "component_row_count": 8,
        "certified_packet_count": 0,
        "review_required_packet_count": 0,
        "context_only_packet_count": 4,
        "blocked_packet_count": 0,
        "candidate_contract_valid": True,
        "component_contract_valid": True,
        "ready_for_review": True,
        "ready_for_v552j_joint_evidence": False,
    }))
    (root / "manifest/v551j_packet_contract_validation_report.json").write_text(json.dumps({
        "candidate_contract_valid": True,
        "component_contract_valid": True,
    }))
    (root / "manifest/manifest.json").write_text(json.dumps({"row_counts": {"candidate": 4, "component": 8}}))
    (root / "manifest/v551j_input_provenance_manifest.json").write_text(json.dumps({
        "final_status": "PARTIAL_READY_V551J_CONTEXT_ONLY"
    }))
    gate = smoke.summarize_v551j_functional_gate(root)
    assert gate["diagnostic_contract_valid"] is True
    assert gate["certified_ready"] is False
    assert gate["review_or_context_ready"] is True
    assert gate["passed"] is True


def test_exact_v552j_preserves_pressure_and_attaches_certified_context() -> None:
    pressure = pd.DataFrame([{
        "v552_pressure_observation_id": "p1",
        "pressure_observation_identity_hash": "ph1",
        "empirical_distribution_id": "d1",
        "source": "GSS",
        "source_family": "GSS",
        "wave": "2010",
        "canonical_wave": "2010",
        "country_code": "US",
        "question_id": "q1",
        "var_code": "v1",
        "source_atom_ids_json": '["a1"]',
        "source_atom_contract_hashes_json": '["ah1"]',
        "source_measurement_contract_hashes_json": '["mh1"]',
        "component_response_surface_signature": "rs1",
        "response_surface_completeness_status": "COMPLETE",
        "pressure_measure_class": "distribution_mean_signed_intensity",
        "pressure_score": 0.25,
        "pressure_score_status": "OBSERVED_NONZERO",
        "pressure_formula_id": "f1",
        "pressure_formula_version": "1",
        "pressure_scale_id": "s1",
        "pressure_measurement_hash": "pmh1",
        "v552j_pressure_linkage_eligible": True,
        "known_absences_json": "[]",
        "forbidden_inference_json": "[]",
    }])
    components = pd.DataFrame([{
        "packet_id": "pkt1",
        "pattern_id": "pat1",
        "family_id": "fam1",
        "component_id": "c1",
        "component_contract_hash": "ch1",
        "source": "GSS",
        "source_family": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "v551_empirical_distribution_id": "d1",
        "v551_atom_id": "a1",
        "v551_atom_contract_hash": "ah1",
        "v551_measurement_contract_hash": "mh1",
    }])
    certified = pd.DataFrame([{
        "packet_id": "pkt1",
        "certification_status": "CERTIFIED_JOINT_RELATION_EVIDENCE",
        "packet_contract_hash": "pkh1",
        "joint_support_score": 0.7,
        "joint_confidence_score": 0.8,
        "joint_evidence_authority_status": "CERTIFIED",
        "joint_directionality_authority_status": "CERTIFIED",
        "allowed_future_targets_json": '["v552j"]',
        "forbidden_claim_ids_json": '["joint_pressure"]',
    }])
    facts = pd.DataFrame([{
        "v552_structural_fact_id": "sf1",
        "source": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "empirical_distribution_id": "d1",
        "source_pressure_observation_ids_json": '["p1"]',
        "relation_axis_id": "ra1",
        "target_entity_id": "t1",
        "driver_facet_id": "df1",
        "structural_channel_id": "sc1",
        "horizon_constraint_id": "h1",
        "semantic_signature": "sem1",
    }])
    temporal = pd.DataFrame([{"v552_temporal_key_source_id": "tk1", "v552_structural_fact_id": "sf1"}])
    outputs = build_exact_v552j_integration(
        run_id="r1",
        pressure_handoff=pressure,
        components=components,
        certified_packets=certified,
        review_packets=pd.DataFrame(),
        candidate_packets=certified,
        structural_facts=facts,
        temporal_sources=temporal,
    )
    assert validate_exact_v552j_integration(outputs) == []
    row = outputs["pressure_observation_index"].iloc[0]
    assert row["pressure_score"] == pressure.iloc[0]["pressure_score"]
    assert row["pressure_measurement_hash"] == "pmh1"
    assert row["joint_context_status"] == "CERTIFIED_JOINT_CONTEXT_ATTACHED"
    assert outputs["readiness"]["ready_for_v553_temporal_field"] is False
    v553 = outputs["v553_input_index"].iloc[0]
    assert v553["source_v552_pressure_observation_id"] == "p1"
    assert v553["pressure_score"] == 0.25
    assert v553["support_score"] == 0.7
    assert v553["confidence_score"] == 0.8
    assert v553["support_score_projection_status"] == "UNANIMOUS_SCALAR_PROJECTION"
    assert "joint_pressure" in v553["joint_context_packet_contracts_json"]
    assert not bool(v553["ready_for_runtime_consumption"])


def test_exact_v552j_keeps_unlinked_pressure_probe_eligible() -> None:
    pressure = pd.DataFrame([{
        "v552_pressure_observation_id": "p2",
        "pressure_observation_identity_hash": "ph2",
        "empirical_distribution_id": "d2",
        "source_family": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "pressure_score": 0.0,
        "pressure_score_status": "OBSERVED_ZERO",
        "pressure_measurement_hash": "pmh2",
        "v552j_pressure_linkage_eligible": True,
    }])
    facts = pd.DataFrame([{
        "v552_structural_fact_id": "sf2",
        "source_family": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "empirical_distribution_id": "d2",
        "source_pressure_observation_ids_json": '["p2"]',
    }])
    temporal = pd.DataFrame([{"v552_temporal_key_source_id": "tk2", "v552_structural_fact_id": "sf2"}])
    outputs = build_exact_v552j_integration(
        run_id="r2",
        pressure_handoff=pressure,
        components=pd.DataFrame(),
        certified_packets=pd.DataFrame(),
        review_packets=pd.DataFrame(),
        candidate_packets=pd.DataFrame(),
        structural_facts=facts,
        temporal_sources=temporal,
    )
    assert validate_exact_v552j_integration(outputs) == []
    assert len(outputs["unlinked_pressure_index"]) == 1
    assert outputs["pressure_observation_index"].iloc[0]["joint_context_status"] == "NO_JOINT_CONTEXT_MATCH"
    assert outputs["v553_input_index"].iloc[0]["ready_for_v553_probe"]


def test_shared_substrate_finalization_preserves_quc_authority() -> None:
    raw = pd.DataFrame([
        {
            "respondent_id": "1",
            "var_code": "trust",
            "question_id": "q-trust",
            "response_value_normalized": "2",
            "is_missing": False,
            "is_dk": False,
            "is_refusal": False,
            "is_iap": False,
        },
        {
            "respondent_id": "2",
            "var_code": "trust",
            "question_id": "q-trust",
            "response_value_normalized": "",
            "is_missing": True,
            "is_dk": False,
            "is_refusal": False,
            "is_iap": False,
        },
    ])
    substrate = canonicalize_shared_respondent_substrate(
        raw,
        run_id="r",
        shard_id="s",
        source="WVS",
        wave="W1",
        canonical_wave="W1",
        country_code="SE",
        base_var_codes=["trust"],
    )
    quc = pd.DataFrame([{
        "question_id": "q-trust",
        "var_code": "trust",
        "semantic_role": "RELATION_EVIDENCE",
        "v551_evidence_role": "relation_evidence",
        "question_use_contract_hash": "quc-hash",
        "allowed_as_response_distribution": True,
        "allowed_as_context_distribution": False,
        "allowed_as_v551_relation_evidence": True,
        "allowed_as_temporal_pressure_indicator": True,
        "semantic_role_authority_status": "CERTIFIED",
        "response_semantics_authority_status": "CERTIFIED",
        "directionality_authority_status": "CERTIFIED",
        "structural_mapping_status": "CERTIFIED",
        "eligibility_gate_status": "CERTIFIED",
        "relation_axis_id": "institutional_trust",
        "driver_facet_id": "trust",
    }])
    enriched, report = enrich_shared_respondent_substrate_with_question_use_contract(substrate, quc, country_code="SE")
    assert report["enrichment_status"] == "PASS"
    assert enriched["question_use_contract_joined"].all()
    assert enriched["allowed_as_v551_relation_evidence"].all()
    assert set(enriched["semantic_role"]) == {"RELATION_EVIDENCE"}
    assert set(enriched["question_use_contract_hash"]) == {"quc-hash"}
    assert enriched.loc[0, "is_valid_substantive_response"]
    assert not enriched.loc[1, "is_valid_substantive_response"]


def test_shared_substrate_boolean_strings_are_not_truthy_by_accident() -> None:
    raw = pd.DataFrame([{
        "respondent_id": "1",
        "var_code": "ctx",
        "question_id": "q-ctx",
        "response_value_normalized": "1",
        "is_missing": "False",
        "is_dk": "False",
        "is_refusal": "False",
        "is_iap": "False",
        "allowed_as_v551_relation_evidence": "False",
    }])
    substrate = canonicalize_shared_respondent_substrate(
        raw, run_id="r", shard_id="s", source="EVS", wave="1981",
        canonical_wave="1981", country_code="BE", base_var_codes=["ctx"],
    )
    assert not bool(substrate.loc[0, "is_missing"])
    assert not bool(substrate.loc[0, "allowed_as_v551_relation_evidence"])


def test_exact_v552j_audits_hash_mismatch_without_false_link() -> None:
    pressure = pd.DataFrame([{
        "v552_pressure_observation_id": "p3",
        "pressure_observation_identity_hash": "ph3",
        "empirical_distribution_id": "d3",
        "source_family": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "source_atom_ids_json": '["a3"]',
        "source_atom_contract_hashes_json": '["correct"]',
        "source_measurement_contract_hashes_json": '["m3"]',
        "pressure_score": 0.1,
        "pressure_score_status": "OBSERVED_NONZERO",
        "pressure_measurement_hash": "pmh3",
        "v552j_pressure_linkage_eligible": True,
    }])
    components = pd.DataFrame([{
        "packet_id": "pkt3",
        "component_id": "c3",
        "source_family": "GSS",
        "canonical_wave": "2010",
        "country_code": "US",
        "v551_empirical_distribution_id": "d3",
        "v551_atom_id": "a3",
        "v551_atom_contract_hash": "wrong",
        "v551_measurement_contract_hash": "m3",
    }])
    outputs = build_exact_v552j_integration(
        run_id="r3", pressure_handoff=pressure, components=components,
        certified_packets=pd.DataFrame(), review_packets=pd.DataFrame(),
        candidate_packets=pd.DataFrame([{"packet_id": "pkt3"}]),
        structural_facts=pd.DataFrame(), temporal_sources=pd.DataFrame(),
    )
    assert outputs["joint_context_link_index"].empty
    audit = outputs["component_linkage_audit"].iloc[0]
    assert audit["link_status"] == "NOT_LINKED"
    assert "atom_contract_hash_mismatch" in audit["reason_codes_json"]
    assert outputs["readiness"]["rejected_component_link_rows"] == 1
