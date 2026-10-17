from __future__ import annotations

import ast
import inspect

import pandas as pd

from data.ddm_build_copy import ddm_v552_structural as v552
from data.ddm_build_copy import ddm_v552_validation as validation


def _atom(i: int, side: str, signed: float, *, raw=None, n: int = 10, n_respondents: int = 100) -> dict:
    row = {column: "" for column in v552.V551_ATOM_REQUIRED_COLUMNS}
    row.update(
        run_id="run", atom_id=f"atom-{i}", candidate_id=f"candidate-{i}", empirical_distribution_id="dist",
        source="TEST", source_family="TEST", wave="W1", canonical_wave="W1", country_code="XX", survey_year=2020,
        analysis_scope="country", empirical_object_type="answer_distribution", empirical_object_id=f"object-{i}",
        source_table="answer_distribution", source_row_hash=f"source-{i}", question_id="q1", var_code="q1",
        position_field="", position_value="", response_value_raw=str(i), response_value_normalized=str(i),
        normalized_response_label=str(i), response_family="ordinal_scale", response_topology="scalar", response_direction=side,
        response_intensity=raw, response_intensity_status="MISSING" if raw is None else "OBSERVED_NUMERIC",
        authority_intensity_semantics="ORDINAL_COORDINATE", v551_signed_side=side, v551_signed_intensity=signed,
        v551_projection_rule_id="rule", v551_projection_authority_hash="authority-hash", semantic_role="RELATION_EVIDENCE",
        semantic_subrole="attitude", semantic_tags="test", directionality_policy="signed_attitude", driver_id="driver",
        driver_facet_id="facet", relation_axis_id="axis", target_entity_id="target", strata_relevance="", strata_path="",
        subject_position_signature="", position_conditioning="", position_modifiers="", conditional_strata_weights="",
        horizon_affordance="", n_unweighted=n, n_respondents=n_respondents, n_weighted=None,
        pct_unweighted=n / n_respondents, pct_weighted=None, weight_status="unweighted_only", support_status="supported",
        confidence_tier="high", response_semantics_contract_hash="response-contract", measurement_contract_hash=f"measurement-{i}",
        atom_contract_hash=f"atom-contract-{i}", evidence_basis="V551_DIRECT_RESPONSE_DISTRIBUTION",
        provenance_basis=f"provenance-{i}", schema_version="v3.0", compiler_version="v3.0",
    )
    return row


def _coverage(*, promotable: int, nonpromotable: int, selected_n: int, promotable_n: int, nonpromotable_n: int, neutral_n: int, status: str) -> pd.DataFrame:
    row = {column: "" for column in v552.V551_COVERAGE_REQUIRED_COLUMNS}
    row.update(
        run_id="run", empirical_distribution_id="dist", source="TEST", source_family="TEST", canonical_wave="W1",
        country_code="XX", analysis_scope="country", source_table="answer_distribution", question_id="q1", var_code="q1",
        position_field="", position_value="", applicable_candidate_count=promotable + nonpromotable,
        promotable_candidate_count=promotable, nonpromotable_candidate_count=nonpromotable,
        neutral_candidate_count=1 if neutral_n else 0, selected_substantive_n_unweighted=selected_n,
        promotable_n_unweighted=promotable_n, nonpromotable_n_unweighted=nonpromotable_n, neutral_n_unweighted=neutral_n,
        selected_substantive_n_weighted=None, promotable_n_weighted=None, nonpromotable_n_weighted=None, neutral_n_weighted=None,
        selected_surface_status="SELECTED_SUBSTANTIVE_SURFACE", directional_adjudication_status=status,
        candidate_count_conserved=True, unweighted_mass_conserved=True, weighted_mass_conserved=True,
        schema_version="v3.0", compiler_version="v3.0",
    )
    return pd.DataFrame([row])


def _adjudication(atoms: pd.DataFrame, *, add_nonpromotable: bool = False, repair_n: int = 0) -> pd.DataFrame:
    rows = []
    for atom in atoms.to_dict("records"):
        row = {column: "" for column in v552.V551_ADJUDICATION_REQUIRED_COLUMNS}
        row.update(
            run_id="run", candidate_id=atom["candidate_id"], empirical_distribution_id="dist", source="TEST", source_family="TEST",
            canonical_wave="W1", country_code="XX", analysis_scope="country", source_table="answer_distribution",
            question_id="q1", var_code="q1", response_family="ordinal_scale", directional_applicability_status="APPLICABLE_BY_AUTHORITY",
            v551_signed_side=atom["v551_signed_side"], v551_signed_intensity=atom["v551_signed_intensity"],
            adjudication_outcome="PROMOTABLE", adjudication_reason="", promotable=True, n_unweighted=atom["n_unweighted"],
            n_weighted=None, relation_axis_id="axis", target_entity_id="target", driver_id="driver", driver_facet_id="facet",
            schema_version="v3.0", compiler_version="v3.0",
        )
        rows.append(row)
    if add_nonpromotable:
        repair = dict(rows[0]) if rows else {column: "" for column in v552.V551_ADJUDICATION_REQUIRED_COLUMNS}
        repair.update(
            run_id="run", candidate_id="repair-candidate", empirical_distribution_id="dist", source="TEST", source_family="TEST",
            canonical_wave="W1", country_code="XX", analysis_scope="country", source_table="answer_distribution",
            question_id="q1", var_code="q1", response_family="ordinal_scale", directional_applicability_status="APPLICABLE_BY_AUTHORITY",
            v551_signed_side="", v551_signed_intensity=None, adjudication_outcome="NONPROMOTABLE_REPAIRABLE",
            adjudication_reason="missing_projection_authority", promotable=False, n_unweighted=repair_n, relation_axis_id="axis",
            target_entity_id="target", driver_id="driver", driver_facet_id="facet", schema_version="v3.0", compiler_version="v3.0",
        )
        rows.append(repair)
    return pd.DataFrame(rows, columns=v552.V551_ADJUDICATION_REQUIRED_COLUMNS)


def _empty_atoms() -> pd.DataFrame:
    return pd.DataFrame(columns=v552.V551_ATOM_REQUIRED_COLUMNS)


def _empty_coverage() -> pd.DataFrame:
    return pd.DataFrame(columns=v552.V551_COVERAGE_REQUIRED_COLUMNS)


def _empty_adjudication() -> pd.DataFrame:
    return pd.DataFrame(columns=v552.V551_ADJUDICATION_REQUIRED_COLUMNS)


def test_single_effective_builder_and_no_old_scale_contract_engine():
    tree = ast.parse(inspect.getsource(v552))
    names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
    assert names.count("build_v552_structural_outputs") == 1
    source = inspect.getsource(v552)
    assert "ddm_v552_contract" not in source
    assert "infer_response" not in source


def test_neutral_raw_intensity_missing_is_zero_and_neutral_mass_stays_in_denominator():
    atoms = pd.DataFrame([_atom(1, "positive", 1.0, raw=1.0, n=10), _atom(2, "negative", 1.0, raw=0.0, n=10), _atom(3, "neutral", 0.0, raw=None, n=80)])
    coverage = _coverage(promotable=3, nonpromotable=0, selected_n=100, promotable_n=100, nonpromotable_n=0, neutral_n=80, status="COMPLETE")
    adjudication = _adjudication(atoms)
    components = v552.build_v552_pressure_component_index(atoms, coverage, run_id="run")
    neutral = components.loc[components["v551_signed_side"].eq("neutral")].iloc[0]
    assert pd.isna(neutral["response_intensity"])
    assert neutral["canonical_signed_component"] == 0.0
    observations = v552.build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run")
    row = observations.iloc[0]
    assert row["pressure_score"] == 0.0
    assert row["pressure_score_status"] == "OBSERVED_ZERO"
    assert abs(row["neutral_component_share"] - 0.8) < 1e-12


def test_repair_debt_is_explicit_and_never_renormalized_away():
    atoms = pd.DataFrame([_atom(1, "positive", 1.0, raw=1.0, n=40), _atom(2, "neutral", 0.0, raw=None, n=40)])
    coverage = _coverage(promotable=2, nonpromotable=1, selected_n=100, promotable_n=80, nonpromotable_n=20, neutral_n=40, status="PARTIAL_WITH_REPAIR_DEBT")
    adjudication = _adjudication(atoms, add_nonpromotable=True, repair_n=20)
    components = v552.build_v552_pressure_component_index(atoms, coverage, run_id="run")
    observations = v552.build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run")
    row = observations.iloc[0]
    assert pd.isna(row["pressure_score"])
    assert row["pressure_score_status"] == "APPLICABLE_BUT_UNRESOLVED"
    assert row["unresolved_n_unweighted"] == 20
    assert row["downstream_permission_status"] == "DENY"
    assert components["distribution_weight_normalized"].isna().all()


def test_selected_surface_partiality_remains_lawful_when_adjudication_complete():
    atoms = pd.DataFrame([_atom(1, "positive", 1.0, raw=1.0, n=30, n_respondents=100), _atom(2, "neutral", 0.0, raw=None, n=20, n_respondents=100)])
    coverage = _coverage(promotable=2, nonpromotable=0, selected_n=50, promotable_n=50, nonpromotable_n=0, neutral_n=20, status="COMPLETE")
    adjudication = _adjudication(atoms)
    components = v552.build_v552_pressure_component_index(atoms, coverage, run_id="run")
    observations = v552.build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run")
    row = observations.iloc[0]
    assert row["response_surface_completeness_status"] == "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE"
    assert row["pressure_measure_class"] == "conditional_selected_response_surface_pressure"
    assert row["pressure_score_status"] == "OBSERVED_NONZERO"
    assert row["downstream_permission_status"] == "ALLOW"


def test_valid_empty_is_integrity_pass_not_applicable():
    outputs = v552.build_v552_structural_outputs(_empty_atoms(), _empty_coverage(), _empty_adjudication(), run_id="run")
    readiness = outputs["v552_readiness_report"].iloc[0]
    assert readiness["run_integrity_status"] == "PASS"
    assert readiness["evidence_status"] == "NOT_APPLICABLE"
    assert readiness["downstream_permission_status"] == "NOT_APPLICABLE"


def test_applicable_but_no_promotable_atoms_is_integrity_pass_unresolved():
    coverage = _coverage(promotable=0, nonpromotable=1, selected_n=20, promotable_n=0, nonpromotable_n=20, neutral_n=0, status="NO_PROMOTABLE")
    adjudication = _adjudication(_empty_atoms(), add_nonpromotable=True, repair_n=20)
    outputs = v552.build_v552_structural_outputs(_empty_atoms(), coverage, adjudication, run_id="run")
    readiness = outputs["v552_readiness_report"].iloc[0]
    observation = outputs["v552_pressure_observation_index"].iloc[0]
    assert readiness["run_integrity_status"] == "PASS"
    assert readiness["evidence_status"] == "APPLICABLE_UNRESOLVED"
    assert readiness["downstream_permission_status"] == "DENY"
    assert observation["pressure_score_status"] == "APPLICABLE_BUT_UNRESOLVED"
    assert pd.isna(observation["pressure_score"])


def test_invocation_permission_does_not_mutate_measurement_or_evidence_state():
    atoms = pd.DataFrame([_atom(1, "positive", 1.0, raw=1.0, n=100)])
    coverage = _coverage(promotable=1, nonpromotable=0, selected_n=100, promotable_n=100, nonpromotable_n=0, neutral_n=0, status="COMPLETE")
    adjudication = _adjudication(atoms)
    outputs = v552.build_v552_structural_outputs(atoms, coverage, adjudication, run_id="run")
    obs = outputs["v552_pressure_observation_index"]
    before = (obs.iloc[0]["pressure_score"], obs.iloc[0]["pressure_score_status"], outputs["v552_readiness_report"].iloc[0]["evidence_status"])
    v552.apply_v552_downstream_permission(outputs, allow_downstream=False)
    after = (obs.iloc[0]["pressure_score"], obs.iloc[0]["pressure_score_status"], outputs["v552_readiness_report"].iloc[0]["evidence_status"])
    assert before == after
    assert outputs["v552_readiness_report"].iloc[0]["downstream_permission_status"] == "DENY"
    issues = validation.validate_v552_v2_1_4_outputs(outputs, input_atoms=atoms, directional_coverage=coverage, directional_adjudication=adjudication, execution_mode="diagnostic")
    assert issues == []


def test_v3_input_rejects_stale_v2_and_validator_rejects_tampered_measurement_hash():
    atoms = pd.DataFrame([_atom(1, "positive", 1.0, raw=1.0, n=100)])
    coverage = _coverage(promotable=1, nonpromotable=0, selected_n=100, promotable_n=100, nonpromotable_n=0, neutral_n=0, status="COMPLETE")
    adjudication = _adjudication(atoms)
    stale = atoms.copy(); stale.loc[:, "schema_version"] = "v2.1"
    report = v552.validate_v552_v551_input_contract(stale, coverage, adjudication, run_id="run")
    assert report["status"] != "PASS"
    outputs = v552.build_v552_structural_outputs(atoms, coverage, adjudication, run_id="run")
    outputs["v552_pressure_component_index"].loc[0, "component_measurement_hash"] = "stale-contract-signature"
    issues = validation.validate_v552_v2_1_4_outputs(outputs, input_atoms=atoms, directional_coverage=coverage, directional_adjudication=adjudication, execution_mode="acceptance")
    assert any(issue.code == "component_measurement_hash_mismatch" for issue in issues)


def test_compiler_requires_v551_manifest_hashes_and_all_canonical_surfaces():
    compiler_path = inspect.getsourcefile(v552)
    assert compiler_path is not None
    source = __import__('pathlib').Path(compiler_path).with_name('compile_v552_structural_ddm.py').read_text(encoding='utf-8')
    for token in ['verify_v551_producer_bundle', 'directional_candidate_adjudication.parquet', 'relation_evidence_atoms.parquet', 'directional_distribution_coverage.parquet', 'artifact_file_sha256', 'publish_staged_directory', 'validate_machine_output_policy']:
        assert token in source
    assert 'canonical_signed_projection_owner' in source
    assert 'V551' in source


def test_validator_uses_compiler_emitted_v3_contract_not_ghost_v21_signatures():
    source = inspect.getsource(validation)
    assert 'ddm_v552_contract' not in source
    assert 'recompute_v552_pressure_measurement_hash' in source
    assert 'recompute_v552_component_measurement_hash' in source
