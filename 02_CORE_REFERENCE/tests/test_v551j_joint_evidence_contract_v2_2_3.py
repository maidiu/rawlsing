from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from data.ddm_build_copy.ddm_v551j_contract import (
    recompute_joint_component_measurement_signature,
    recompute_joint_empirical_distribution_signature,
    recompute_joint_measurement_contract_hash,
    recompute_joint_orientation_signature,
    recompute_joint_response_identity_signature,
    recompute_joint_semantic_signature,
    recompute_joint_structural_signature,
    recompute_joint_target_signature,
    recompute_joint_topology_signature,
    recompute_v551j_component_contract_hash,
    recompute_v551j_component_id,
    recompute_v551j_packet_id,
    recompute_v551j_v2_2_3_packet_contract_hash,
    v551j_v2_2_3_packet_contract_payload,
)
from data.ddm_build_copy.ddm_v551j_validation import (
    read_v551j_contract_csv,
    validate_v551j_v2_2_3_outputs,
    validate_written_v551j_artifacts,
)


HERE = Path(__file__).resolve()
PACKAGE_ROOT = HERE.parents[3] if (HERE.parents[3] / "outputs").exists() else HERE.parents[2]
PACKAGED_OUTPUTS = PACKAGE_ROOT / "outputs"
PACKAGED_FIXTURES = PACKAGE_ROOT / "tests" / "fixtures"
RUN_IDS = [f"gss_{w}_v551j_joint_evidence_contract_v2_2_3_acceptance" for w in (1972, 1973, 1984, 1993, 2002, 2010, 2016, 2024)]
OUTPUT_BASE = PACKAGED_OUTPUTS if (PACKAGED_OUTPUTS / RUN_IDS[0]).exists() else sorted(PACKAGED_OUTPUTS.glob("v551j_joint_evidence_contract_v2_2_3_acceptance_20*"))[-1]


@dataclass
class Fixture:
    root: Path
    atoms: Path
    pattern_index: Path
    pattern_items: Path
    relation_signature: Path
    manifest: Path
    readiness: Path
    registry: Path


def _run(run_id: str) -> Path:
    path = OUTPUT_BASE / run_id
    assert path.exists(), path
    return path


def _csv(run_id: str, rel: str) -> pd.DataFrame:
    return read_v551j_contract_csv(_run(run_id) / rel)


def _frames(run_id: str = RUN_IDS[0]) -> dict[str, pd.DataFrame]:
    return {
        "candidate": _csv(run_id, "packets/v551j_joint_packet_candidate_index.csv"),
        "certified": _csv(run_id, "packets/v551j_certified_joint_packet_index.csv"),
        "review_surface": _csv(run_id, "packets/v551j_review_surface.csv"),
        "certification_audit": _csv(run_id, "audits/v551j_certification_audit.csv"),
        "component": _csv(run_id, "packets/v551j_joint_component_index.csv"),
    }


def _expected_registry_hash(run_id: str = RUN_IDS[0]) -> str:
    return json.loads((_run(run_id) / "manifest/v551j_input_provenance_manifest.json").read_text())["registry_hash"]


def _issues(frames: dict[str, pd.DataFrame], mode: str = "acceptance") -> list[str]:
    return validate_v551j_v2_2_3_outputs(**frames, expected_registry_hash=_expected_registry_hash(), execution_mode=mode)


def _all_candidates() -> pd.DataFrame:
    return read_v551j_contract_csv(OUTPUT_BASE / "aggregate/candidate_packet_index.csv")


def _all_components() -> pd.DataFrame:
    return read_v551j_contract_csv(OUTPUT_BASE / "aggregate/component_index.csv")


def _packet_components(frames: dict[str, pd.DataFrame], row: pd.Series) -> list[dict[str, object]]:
    return frames["component"][frames["component"].packet_id.astype(str).eq(str(row.packet_id))].sort_values("item_order", kind="mergesort").to_dict("records")


def _copy_fixture(tmp_path: Path) -> Fixture:
    src = PACKAGED_FIXTURES / "v551j_v2_2_3/gss_1972"
    dst = tmp_path / "gss_1972"
    shutil.copytree(src, dst)
    return Fixture(
        root=dst,
        atoms=dst / "relation_evidence_atoms.parquet",
        pattern_index=dst / "joint_response_pattern_index.parquet",
        pattern_items=dst / "joint_response_pattern_item_index.parquet",
        relation_signature=dst / "joint_pattern_relation_signature.parquet",
        manifest=dst / "v550j_manifest.json",
        readiness=dst / "v550j_source_wave_readiness_report.json",
        registry=dst / "question_family_registry.yaml",
    )


def _compiler_command(fixture: Fixture, output_root: Path, strict: bool) -> list[str]:
    return [
        sys.executable, str(PACKAGE_ROOT / "code/data/ddm_build_copy/compile_v551j_joint_evidence_packets.py" if (PACKAGE_ROOT / "code").exists() else PACKAGE_ROOT / "data/ddm_build_copy/compile_v551j_joint_evidence_packets.py"),
        "--run-id", "gss_1972_v551j_test_proof", "--output-root", str(output_root),
        "--v551-atoms-path", str(fixture.atoms),
        "--v550j-pattern-index-path", str(fixture.pattern_index),
        "--v550j-pattern-item-index-path", str(fixture.pattern_items),
        "--v550j-relation-signature-path", str(fixture.relation_signature),
        "--v550j-manifest-path", str(fixture.manifest),
        "--v550j-readiness-report-path", str(fixture.readiness),
        "--registry-path", str(fixture.registry),
        "--emit-certified-index", "--emit-review-surface", "--write-csv", "--write-parquet",
        "--strict" if strict else "--no-strict",
    ]


def _written(root: Path) -> dict[str, object]:
    run = root / "gss_1972_v551j_test_proof"
    return {
        "run": run,
        "candidate": read_v551j_contract_csv(run / "packets/v551j_joint_packet_candidate_index.csv"),
        "certified": read_v551j_contract_csv(run / "packets/v551j_certified_joint_packet_index.csv"),
        "review": read_v551j_contract_csv(run / "packets/v551j_review_surface.csv"),
        "audit": read_v551j_contract_csv(run / "audits/v551j_certification_audit.csv"),
        "component": read_v551j_contract_csv(run / "packets/v551j_joint_component_index.csv"),
        "readiness": json.loads((run / "manifest/v551j_readiness_report.json").read_text()),
        "validation": json.loads((run / "manifest/v551j_packet_contract_validation_report.json").read_text()),
        "provenance": json.loads((run / "manifest/v551j_input_provenance_manifest.json").read_text()),
    }


def _assert_no_authority(candidate: pd.DataFrame) -> None:
    for column in ["ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"]:
        assert not candidate[column].astype(str).str.lower().isin({"true", "1", "yes", "y"}).any()
    assert candidate["allowed_future_targets_json"].eq("[]").all()
    assert candidate["runtime_use_class"].eq("not_runtime_consumable").all()


def _assert_hashes(frames: dict[str, pd.DataFrame]) -> None:
    for _, row in frames["component"].iterrows():
        assert recompute_v551j_component_id(row) == row.component_id
        assert recompute_v551j_component_contract_hash(row) == row.component_contract_hash
    for _, row in frames["candidate"].iterrows():
        comps = _packet_components({"component": frames["component"]}, row)
        assert recompute_v551j_v2_2_3_packet_contract_hash(row, comps) == row.packet_contract_hash
        assert recompute_joint_measurement_contract_hash(row) == row.joint_measurement_contract_hash


def test_01_packaged_outputs_exist(): assert all(_run(r).exists() for r in RUN_IDS)
def test_02_v2_2_2_packet_ids_are_preserved(): assert read_v551j_contract_csv(PACKAGED_FIXTURES / "v551j_v2_2_3/identity_baseline/v2_2_2_packet_ids.csv").merge(_all_candidates(), on=["source_family", "canonical_wave", "country_code", "pattern_id", "packet_id"]).shape[0] == 782
def test_03_v2_2_2_component_ids_are_preserved(): assert read_v551j_contract_csv(PACKAGED_FIXTURES / "v551j_v2_2_3/identity_baseline/v2_2_2_component_ids.csv").merge(_all_components(), on=["source_family", "canonical_wave", "country_code", "pattern_id", "item_order", "v550j_item_question_id", "v550j_item_var_code", "v550j_item_response_value_normalized", "component_id"]).shape[0] == 3883
def test_04_id_stability_audit_rows(): assert len(read_v551j_contract_csv(OUTPUT_BASE / "audits/v2_2_2_to_v2_2_3_id_stability.csv")) == 4665
def test_05_id_stability_audit_zero_mismatch(): assert read_v551j_contract_csv(OUTPUT_BASE / "audits/v2_2_2_to_v2_2_3_id_stability.csv")["id_match"].astype(str).str.lower().eq("true").all()
def test_06_packet_id_recomputation_detects_mutation(): f = _frames(); f["candidate"].loc[0, "packet_id"] = "v551j__" + "0" * 32; assert "packet_id_recomputation_mismatch" in _issues(f)
def test_07_component_id_recomputation_detects_mutation(): f = _frames(); f["component"].loc[0, "component_id"] = "v551jc__" + "0" * 32; assert "component_id_recomputation_mismatch" in _issues(f)
def test_08_permission_change_does_not_change_packet_id(): f = _frames(); before = f["candidate"].loc[0, "packet_id"]; f["candidate"].loc[0, "ready_for_v552j_joint_evidence"] = "False"; assert recompute_v551j_packet_id(f["candidate"].loc[0]) == before
def test_09_permission_change_changes_packet_contract_hash(): f = _frames(); f["candidate"].loc[0, "ready_for_v552j_joint_evidence"] = "False"; assert "packet_contract_hash_mismatch" in _issues(f)
def test_10_input_hash_change_does_not_change_packet_id(): f = _frames(); before = f["candidate"].loc[0, "packet_id"]; f["candidate"].loc[0, "v551_input_artifact_hash"] = "0" * 64; assert recompute_v551j_packet_id(f["candidate"].loc[0]) == before
def test_11_input_hash_change_changes_packet_contract_hash(): f = _frames(); f["candidate"].loc[0, "v551_input_artifact_hash"] = "0" * 64; assert "packet_contract_hash_mismatch" in _issues(f)
def test_12_component_contract_change_changes_packet_contract_hash(): f = _frames(); f["component"].loc[0, "component_contract_hash"] = "0" * 64; assert "packet_contract_hash_mismatch" in _issues(f)
def test_13_run_id_change_does_not_change_packet_id(): f = _frames(); before = f["candidate"].loc[0, "packet_id"]; f["candidate"].loc[0, "run_id"] = "changed"; assert recompute_v551j_packet_id(f["candidate"].loc[0]) == before
def test_14_run_id_change_does_not_change_packet_contract_hash(): f = _frames(); f["candidate"].loc[0, "run_id"] = "changed"; assert "packet_contract_hash_mismatch" not in _issues(f)
def test_15_packet_hash_recomputes_from_packaged_csv_evidence(): f = _frames(); row = f["candidate"].iloc[0]; assert recompute_v551j_v2_2_3_packet_contract_hash(row, _packet_components(f, row)) == row.packet_contract_hash
def test_16_packet_hash_payload_excludes_prior_hash(): f = _frames(); row = f["candidate"].iloc[0]; assert "prior_packet_contract_hash" not in v551j_v2_2_3_packet_contract_payload(row, _packet_components(f, row))
def test_17_packet_hash_payload_component_count_is_exact(): f = _frames(); row = f["candidate"].iloc[0]; assert len(v551j_v2_2_3_packet_contract_payload(row, _packet_components(f, row))["component_ids"]) == int(row.pattern_item_count)
def test_18_each_joint_signature_recomputes(): f = _frames(); row = f["candidate"].iloc[0]; comps = _packet_components(f, row); assert recompute_joint_response_identity_signature(comps) == row.joint_response_identity_signature and recompute_joint_empirical_distribution_signature(comps) == row.joint_empirical_distribution_signature and recompute_joint_semantic_signature(comps) == row.joint_semantic_signature and recompute_joint_orientation_signature(comps) == row.joint_orientation_signature and recompute_joint_topology_signature(row, comps) == row.joint_topology_signature and recompute_joint_target_signature(comps) == row.joint_target_signature and recompute_joint_structural_signature(row, comps) == row.joint_structural_signature and recompute_joint_component_measurement_signature(comps) == row.joint_component_measurement_signature
def test_19_valid_format_joint_signature_mutation_is_detected(): f = _frames(); f["candidate"].loc[0, "joint_response_identity_signature"] = "0" * 64; assert "joint_signature_recomputation_mismatch" in _issues(f)
def test_20_joint_measurement_hash_mutation_is_detected(): f = _frames(); f["candidate"].loc[0, "joint_measurement_contract_hash"] = "0" * 64; assert "joint_measurement_hash_mismatch" in _issues(f)
def test_21_actual_stance_direction_mismatch_is_detected(): f = _frames(); f["component"].loc[0, "v551_response_direction"] = "negative"; assert "stance_direction_conflict" in _issues(f)
def test_22_actual_response_semantics_hash_mismatch_is_detected(): f = _frames(); f["component"].loc[0, "v551_response_semantics_contract_hash"] = "0" * 64; assert "response_semantics_hash_conflict" in _issues(f)
def test_23_actual_registry_hash_mismatch_emits_root_token(): f = _frames(); f["candidate"]["question_family_registry_hash"] = "0" * 64; assert "registry_hash_mismatch" in _issues(f)
def test_24_actual_normalized_label_mismatch_is_detected(): f = _frames(); f["component"].loc[0, "v551_normalized_response_label"] = "MUTATED_LABEL"; assert "comparison_status_inconsistent_with_values" in _issues(f)
def test_25_actual_question_identity_mismatch_emits_comparison_token(): f = _frames(); f["component"].loc[0, "v551_question_id"] = "MUTATED_Q"; assert "comparison_status_inconsistent_with_values" in _issues(f)
def test_26_direct_pressure_field_present_emits_exact_token(): f = _frames(); f["component"]["pressure_score"] = "0.1"; assert "direct_pressure_field_present" in _issues(f)
def test_27_invalid_review_finalization_emits_candidate_status_token(): f = _frames(); idx = f["candidate"][f["candidate"].certification_status.eq("REVIEW_REQUIRED_COMPONENT_GAP")].index[0]; f["candidate"].loc[idx, "review_reason_codes_json"] = "[]"; assert "candidate_status_permission_mismatch" in _issues(f)
def test_28_false_cross_contract_gap_is_detected(): f = _frames(); f["component"].loc[0, "cross_contract_status"] = "CROSS_CONTRACT_GAP"; assert "unexpected_cross_contract_gap" in _issues(f)
def test_29_stored_comparison_status_cannot_override_actual_values(): f = _frames(); f["component"].loc[0, "joint_response_stance_alignment_status"] = "EXACT_GOVERNED_ALIGNMENT"; f["component"].loc[0, "v551_response_direction"] = "negative"; assert "stance_direction_conflict" in _issues(f)
def test_30_missing_empirical_distribution_emits_exact_token(): f = _frames(); f["component"].loc[0, "v551_empirical_distribution_id"] = ""; assert "missing_empirical_distribution_id" in _issues(f)
def test_31_ambiguous_match_emits_exact_token(): f = _frames(); f["component"].loc[0, "v551_atom_match_status"] = "AMBIGUOUS_V551_ATOM_MATCH"; assert "ambiguous_v551_atom_match" in _issues(f)
def test_32_invalid_denominator_emits_exact_token(): f = _frames(); f["component"].loc[0, "v551_n_respondents"] = "-1"; assert "invalid_component_denominator" in _issues(f)
def test_33_duplicate_component_id_emits_exact_token(): f = _frames(); f["component"].loc[1, "component_id"] = f["component"].loc[0, "component_id"]; assert "duplicate_component_id" in _issues(f)
def test_34_duplicate_item_order_emits_exact_token(): f = _frames(); f["component"].loc[1, "item_order"] = f["component"].loc[0, "item_order"]; assert "duplicate_item_order" in _issues(f)
def test_35_component_item_cardinality_emits_exact_token(): f = _frames(); f["component"] = f["component"].iloc[1:].copy(); assert "component_item_cardinality_mismatch" in _issues(f)
def test_36_ordered_array_cardinality_emits_exact_token(): f = _frames(); arr = json.loads(f["candidate"].loc[0, "component_empirical_distribution_ids_ordered_json"]); f["candidate"].loc[0, "component_empirical_distribution_ids_ordered_json"] = json.dumps(arr[:-1]); assert "ordered_array_cardinality_mismatch" in _issues(f)
def test_37_direct_v553_authorization_emits_exact_token(): f = _frames(); f["candidate"].loc[0, "ready_for_v553"] = "True"; assert "direct_v553_authorization" in _issues(f)
def test_38_pressure_anchor_authorization_emits_exact_token(): f = _frames(); f["candidate"].loc[0, "pressure_anchor_eligible"] = "True"; assert "pressure_anchor_authorization" in _issues(f)
def test_39_temporal_authorization_emits_exact_token(): f = _frames(); f["candidate"].loc[0, "temporal_pressure_authorized"] = "True"; assert "temporal_authorization" in _issues(f)
def test_40_runtime_authorization_emits_exact_token(): f = _frames(); f["candidate"].loc[0, "runtime_use_class"] = "runtime_safe_after_v552j"; assert "runtime_authorization" in _issues(f)
def test_41_noncertified_v552j_permission_emits_exact_token(): f = _frames(); idx = f["candidate"][f["candidate"].certification_status.eq("REVIEW_REQUIRED_COMPONENT_GAP")].index[0]; f["candidate"].loc[idx, "ready_for_v552j_joint_evidence"] = "True"; assert "noncertified_v552j_permission" in _issues(f)
def test_42_certified_missing_v552j_permission_emits_exact_token(): f = _frames(); idx = f["candidate"][f["candidate"].certification_status.str.startswith("CERTIFIED")].index[0]; f["candidate"].loc[idx, "ready_for_v552j_joint_evidence"] = "False"; f["certified"].loc[0, "ready_for_v552j_joint_evidence"] = "False"; assert "certified_missing_v552j_permission" in _issues(f)
def test_43_eight_wave_component_counts(): assert len(_all_components()) == 3883
def test_44_eight_wave_cross_contract_consistency(): assert _all_components().cross_contract_status.value_counts().to_dict() == {"CROSS_CONTRACT_CONSISTENT": 3883}
def test_45_eight_wave_stance_and_response_hash_counts(): c = _all_components(); assert int(((c.v550j_joint_response_stance == "support") & (c.v551_response_direction == "positive")).sum()) == 2032 and int(((c.v550j_joint_response_stance == "oppose") & (c.v551_response_direction == "negative")).sum()) == 1851 and c.response_semantics_hash_status.value_counts().to_dict() == {"EXACT_MATCH": 3883}
def test_46_eight_wave_certified_review_partition(): assert _all_candidates().certification_status.value_counts().to_dict() == {"REVIEW_REQUIRED_COMPONENT_GAP": 628, "CERTIFIED_JOINT_RELATION_EVIDENCE": 154}
def test_47_eight_wave_permission_boundary(): p = _all_candidates(); assert int(p.ready_for_v552j_joint_evidence.astype(str).str.lower().eq("true").sum()) == 154 and int((~p.certification_status.str.startswith("CERTIFIED") & p.ready_for_v552j_joint_evidence.astype(str).str.lower().eq("true")).sum()) == 0
def test_48_all_eight_final_written_artifacts_pass_authoritative_validator(): assert all(validate_written_v551j_artifacts(candidate_path=_run(r) / "packets/v551j_joint_packet_candidate_index.csv", component_path=_run(r) / "packets/v551j_joint_component_index.csv", certified_path=_run(r) / "packets/v551j_certified_joint_packet_index.csv", review_path=_run(r) / "packets/v551j_review_surface.csv", certification_audit_path=_run(r) / "audits/v551j_certification_audit.csv", expected_registry_hash=_expected_registry_hash(r)) == [] for r in RUN_IDS)
def test_49_gss_2016_final_csv_survives_authoritative_validator(): r = "gss_2016_v551j_joint_evidence_contract_v2_2_3_acceptance"; f = _frames(r); p = f["candidate"][f["candidate"].packet_id.eq("v551j__a0622a8472c54e8d69e94b1b1dccfdb0")]; assert not p.empty and p.iloc[0].joint_pattern_count_weighted == "19.3057389527615" and p.iloc[0].joint_n_weighted == "19.3057389527615" and validate_written_v551j_artifacts(candidate_path=_run(r) / "packets/v551j_joint_packet_candidate_index.csv", component_path=_run(r) / "packets/v551j_joint_component_index.csv", certified_path=_run(r) / "packets/v551j_certified_joint_packet_index.csv", review_path=_run(r) / "packets/v551j_review_surface.csv", certification_audit_path=_run(r) / "audits/v551j_certification_audit.csv", expected_registry_hash=_expected_registry_hash(r)) == []
def test_50_strict_failure_writes_blocked_artifacts_then_exits_nonzero(tmp_path): fixture = _copy_fixture(tmp_path); fixture.registry.write_text(fixture.registry.read_text() + "\n# mutated\n"); result = subprocess.run(_compiler_command(fixture, tmp_path / "strict_output", True), capture_output=True, text=True); w = _written(tmp_path / "strict_output"); assert result.returncode == 1 and w["readiness"]["final_status"] == "BLOCKED_V551J_OUTPUT_CONTRACT" and "registry_hash_mismatch" in w["validation"]["issues_json"] and len(w["candidate"]) == 119 and len(w["certified"]) == 0 and len(w["review"]) == 0 and w["candidate"]["review_required"].astype(str).str.lower().eq("true").sum() == 0 and w["candidate"]["certification_status"].str.startswith("BLOCKED").sum() == 119 and not w["readiness"]["ready_for_review"]; _assert_no_authority(w["candidate"]); _assert_hashes({"candidate": w["candidate"], "component": w["component"]})
def test_51_no_strict_always_removes_all_downstream_permissions(tmp_path): fixture = _copy_fixture(tmp_path); result = subprocess.run(_compiler_command(fixture, tmp_path / "diagnostic_output", False), capture_output=True, text=True); w = _written(tmp_path / "diagnostic_output"); assert result.returncode == 0 and w["readiness"]["final_status"] == "DIAGNOSTIC_V551J_NO_STRICT_NOT_READY" and len(w["candidate"]) == 119 and len(w["certified"]) == 0 and len(w["review"]) == 92 and w["candidate"]["certification_status"].value_counts().to_dict() == {"REVIEW_REQUIRED_COMPONENT_GAP": 92, "CERTIFIED_JOINT_RELATION_EVIDENCE": 27}; _assert_no_authority(w["candidate"]); _assert_hashes({"candidate": w["candidate"], "component": w["component"]}); assert validate_written_v551j_artifacts(candidate_path=w["run"] / "packets/v551j_joint_packet_candidate_index.csv", component_path=w["run"] / "packets/v551j_joint_component_index.csv", certified_path=w["run"] / "packets/v551j_certified_joint_packet_index.csv", review_path=w["run"] / "packets/v551j_review_surface.csv", certification_audit_path=w["run"] / "audits/v551j_certification_audit.csv", expected_registry_hash=w["provenance"]["registry_hash"], execution_mode="diagnostic") == []
def test_52_requirement_matrix_has_one_row_per_test(): m = pd.read_csv(OUTPUT_BASE / "reports/requirement_matrix.csv"); assert len(m) == 52 and m.test_function.nunique() == 52 and m.pytest_result.eq("PASS").all()
