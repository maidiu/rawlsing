import pandas as pd
import pytest
import hashlib
import json

from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, verify_frame_source_wave_identity_coherence
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.ddm_v552_structural import (
    V551_ATOM_REQUIRED_COLUMNS, V551_COVERAGE_REQUIRED_COLUMNS, V551_ADJUDICATION_REQUIRED_COLUMNS,
    build_v552_pressure_component_index, build_v552_pressure_observation_index,
    build_relation_axis_pressure_from_observations, build_target_entity_pressure_from_observations,
    build_v552_structural_outputs, recompute_v552_component_measurement_hash, recompute_v552_pressure_measurement_hash,
    validate_v552_v551_input_contract,
)
from data.ddm_build_copy.compile_v552_structural_ddm import _scope_from_manifest


def identity(source, wave):
    return resolve_source_wave_identity(source, wave)


@pytest.mark.parametrize("source,waves", [
    ("Arab Barometer", ["I", "W1", "Wave 1", "1"]),
    ("EVS", ["1981", "W1"]),
    ("Afrobarometer", ["R1", "ROUND1", "Round 1"]),
])
def test_aliases_resolve_to_one_uid_pair(source, waves):
    pairs = {(identity(source, wave).source_family_uid, identity(source, wave).wave_uid) for wave in waves}
    assert len(pairs) == 1


def test_evs_1999_and_w3_resolve_to_one_uid_pair():
    assert {(identity("EVS", wave).source_family_uid, identity("EVS", wave).wave_uid)
            for wave in ["1999", "W3"]} == {("sf_evs_v1", "wv_evs_1999_v1")}


def test_contradictory_redundant_identity_fails_closed():
    row = {"source": "Arab Barometer", "source_family": "EVS", "wave": "I", "canonical_wave": "W1",
           "source_family_uid": "sf_arab_barometer_v1", "wave_uid": "wv_arab_barometer_i_v1"}
    with pytest.raises(BoundaryContractError):
        verify_frame_source_wave_identity_coherence(pd.DataFrame([row]), allow_empty=False)


def test_asian_barometer_w6_is_recognized_but_not_closed_35():
    assert identity("Asian Barometer", "W6").governance_state == "RECOGNIZED_EXCLUDED"
    assert not identity("Asian Barometer", "W6").closed_35_member


def test_latinobarometro_unicode_and_unaccented_aliases_resolve():
    pairs = {(identity(source, "1995").source_family_uid, identity(source, "1995").wave_uid)
             for source in ["Latinobarómetro", "Latinobarometro", "Latinobaro\u0301metro"]}
    assert len(pairs) == 1


def test_v552_input_contract_rejects_nonproduction_identity():
    row = {"run_id":"r", "atom_id":"a", "candidate_id":"c", "empirical_distribution_id":"d",
           "source":"Asian Barometer", "source_family":"Asian Barometer", "source_family_uid":"sf_asian_barometer_v1",
           "wave":"W6", "canonical_wave":"W6", "wave_uid":"wv_asian_barometer_w6_v1", "schema_version":"v3.0", "compiler_version":"v3.0"}
    atoms = pd.DataFrame([row])
    for col in ["response_value_normalized","response_family","response_topology","response_direction","response_intensity","response_intensity_status","authority_intensity_semantics","v551_signed_side","v551_signed_intensity","v551_projection_rule_id","v551_projection_authority_hash","semantic_role","driver_id","driver_facet_id","relation_axis_id","target_entity_id","n_unweighted","response_semantics_contract_hash","measurement_contract_hash","atom_contract_hash","evidence_basis","provenance_basis","country_code","analysis_scope","empirical_object_type","empirical_object_id","source_table","source_row_hash","question_id","var_code"]:
        atoms[col] = "x"
    report = validate_v552_v551_input_contract(atoms)
    assert report["status"].startswith("BLOCKED")


def _frames(waves, source="Arab Barometer"):
    atoms=[]
    for i, wave in enumerate(waves):
        ident=identity(source, wave)
        row={c:"x" for c in V551_ATOM_REQUIRED_COLUMNS}
        row.update(run_id="run-1", atom_id=f"a{i}", candidate_id=f"c{i}", empirical_distribution_id="d1",
                   source=source, source_family=source, source_family_uid=ident.source_family_uid,
                   wave=wave, canonical_wave=wave, wave_uid=ident.wave_uid, country_code="EGY", n_unweighted=1,
                   response_intensity=0.5, v551_signed_side="positive", v551_signed_intensity=0.5,
                   schema_version="v3.0", compiler_version="v3.0")
        atoms.append(row)
    atom_df=pd.DataFrame(atoms)
    coverage={c:"x" for c in V551_COVERAGE_REQUIRED_COLUMNS}
    coverage.update(run_id="run-1", empirical_distribution_id="d1", source=source, source_family=source,
                    source_family_uid=atoms[0]["source_family_uid"], canonical_wave=waves[0], wave_uid=atoms[0]["wave_uid"],
                    applicable_candidate_count=len(atoms), promotable_candidate_count=len(atoms), nonpromotable_candidate_count=0,
                    candidate_count_conserved=True, unweighted_mass_conserved=True, weighted_mass_conserved=True,
                    selected_surface_status="SELECTED_SUBSTANTIVE_SURFACE", directional_adjudication_status="COMPLETE")
    coverage["schema_version"]="v3.0"; coverage["compiler_version"]="v3.0"
    adjud=[]
    for i in range(len(atoms)):
        row={c:"x" for c in V551_ADJUDICATION_REQUIRED_COLUMNS}
        row.update(run_id="run-1", candidate_id=f"c{i}", empirical_distribution_id="d1", source=source,
                   source_family=source, source_family_uid=atoms[i]["source_family_uid"], canonical_wave=waves[i],
                   wave_uid=atoms[i]["wave_uid"], adjudication_outcome="PROMOTABLE", promotable=True)
        row["schema_version"]="v3.0"; row["compiler_version"]="v3.0"
        adjud.append(row)
    return atom_df, pd.DataFrame([coverage]), pd.DataFrame(adjud)


def test_actual_v552_outputs_propagate_uids_and_preserve_measurement_surface():
    atoms, coverage, adjudication = _frames(["I"])
    components=build_v552_pressure_component_index(atoms, coverage, run_id="run-1")
    observations=build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run-1")
    assert {"source_family_uid", "wave_uid"} <= set(components.columns)
    assert {"source_family_uid", "wave_uid"} <= set(observations.columns)
    assert observations.pressure_score.iloc[0] == 0.5
    assert observations.pressure_score_status.iloc[0] == "OBSERVED_NONZERO"
    assert observations.pressure_measurement_hash.iloc[0]


@pytest.mark.parametrize("source,waves", [
    ("Arab Barometer", ["I", "W1", "Wave 1", "1"]),
    ("EVS", ["1981", "W1"]),
    ("EVS", ["1999", "W3"]),
    ("Afrobarometer", ["R1", "ROUND1", "Round 1"]),
    ("Latinobarómetro", ["Latinobarómetro", "Latinobarometro", "Latinobaro\u0301metro"]),
])
def test_actual_rollup_coalesces_required_alias_families(source, waves):
    if source == "Latinobarómetro":
        source_aliases=waves
        atoms, coverage, adjudication = _frames(["1995"] * len(source_aliases), source=source_aliases[0])
        for i, alias in enumerate(source_aliases):
            ident=identity(alias, "1995")
            for frame in [atoms, coverage, adjudication]:
                if frame is coverage:
                    frame.loc[:, "source"] = alias
                else:
                    frame.loc[i, "source"] = alias
            atoms.loc[i, "source_family_uid"] = ident.source_family_uid
            atoms.loc[i, "wave_uid"] = ident.wave_uid
            adjudication.loc[i, "source_family_uid"] = ident.source_family_uid
            adjudication.loc[i, "wave_uid"] = ident.wave_uid
    else:
        atoms, coverage, adjudication = _frames(waves, source=source)
    components=build_v552_pressure_component_index(atoms, coverage, run_id="run-1")
    observations=build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run-1")
    assert len(build_relation_axis_pressure_from_observations(observations, "run-1")) == 1


def test_complete_v552_output_contract_carries_identity_into_readiness_and_structural_surfaces():
    atoms, coverage, adjudication = _frames(["I"])
    outputs=build_v552_structural_outputs(atoms, coverage, adjudication, run_id="run-1")
    expected=("sf_arab_barometer_v1","wv_arab_barometer_i_v1")
    for name in ["v552_pressure_component_index", "v552_pressure_observation_index", "relation_axis_pressure", "target_entity_pressure", "v552_structural_fact_index"]:
        assert {"source_family_uid", "wave_uid"} <= set(outputs[name].columns)
        assert not outputs[name].empty
        assert set(zip(outputs[name].source_family_uid, outputs[name].wave_uid)) == {expected}
        assert outputs[name].source_family_uid.notna().all() and outputs[name].wave_uid.notna().all()
    for name in ["v552_temporal_key_source_index", "v552_to_v552j_pressure_observation_handoff_index", "v552_to_v552j_handoff_index"]:
        assert set(zip(outputs[name].source_family_uid, outputs[name].wave_uid)) == {expected}
        assert outputs[name].source_family_uid.notna().all() and outputs[name].wave_uid.notna().all()
    readiness=outputs["v552_readiness_report"].iloc[0]
    assert readiness.run_id == "run-1"
    assert (readiness.source_family_uid, readiness.wave_uid) == expected
    assert readiness.evidence_status == "PRESENT"
    assert readiness.downstream_permission_status == "ALLOW"


def test_manifest_scope_contract_carries_governed_uid_pair():
    ident=identity("EVS", "1999")
    payload={"source":"EVS", "wave":"W3", "canonical_wave":"1999", "source_family_uid":ident.source_family_uid,
             "wave_uid":ident.wave_uid, "country_code":"DEU", "producer_scope_identity":
             {"source":"EVS", "wave":"W3", "canonical_wave":"1999", "source_family_uid":ident.source_family_uid,
              "wave_uid":ident.wave_uid, "country_code":"DEU", "scope_kind":"country"}}
    scope=_scope_from_manifest(payload)
    assert scope["source_family_uid"] == ident.source_family_uid
    assert scope["wave_uid"] == ident.wave_uid


def test_uid_metadata_is_excluded_from_frozen_v552_hash_payloads():
    atoms, coverage, adjudication = _frames(["I"])
    components=build_v552_pressure_component_index(atoms, coverage, run_id="run-1")
    observations=build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run-1")
    component=components.iloc[0].to_dict(); observation=observations.iloc[0].to_dict()
    component_hash=recompute_v552_component_measurement_hash(component)
    observation_hash=recompute_v552_pressure_measurement_hash(observation, components)
    component.update(source_family_uid="different", wave_uid="different")
    observation.update(source_family_uid="different", wave_uid="different")
    assert recompute_v552_component_measurement_hash(component) == component_hash
    assert recompute_v552_pressure_measurement_hash(observation, components) == observation_hash


def test_rollups_keep_run_and_country_boundaries_independent_of_uid():
    atoms, coverage, adjudication = _frames(["I"])
    components=build_v552_pressure_component_index(atoms, coverage, run_id="run-1")
    observations=build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run-1")
    second=observations.copy()
    second.loc[:, "run_id"]="run-2"
    second.loc[:, "country_code"]="TUN"
    combined=pd.concat([observations, second], ignore_index=True)
    rollup=build_relation_axis_pressure_from_observations(combined, "run-1")
    assert set(rollup.run_id) == {"run-1", "run-2"}
    assert set(rollup.country_code) == {"EGY", "TUN"}
    assert len(rollup) == 2


def test_uid_grouping_is_order_invariant_and_legacy_rollup_payload_is_frozen():
    atoms, coverage, adjudication = _frames(["I", "W1", "Wave 1", "1"])
    components=build_v552_pressure_component_index(atoms, coverage, run_id="run-1")
    observations=build_v552_pressure_observation_index(atoms, components, coverage, adjudication, run_id="run-1")
    first=build_relation_axis_pressure_from_observations(observations, "run-1").iloc[0]
    second=build_relation_axis_pressure_from_observations(observations.iloc[::-1].reset_index(drop=True), "run-1").iloc[0]
    assert first.relation_axis_pressure_id == second.relation_axis_pressure_id
    assert first.source_family_uid == second.source_family_uid
    assert first.wave_uid == second.wave_uid
    legacy={"source":"Arab Barometer", "wave":"I", "canonical_wave":"I", "country_code":"EGY", "relation_axis_id":"x"}
    expected="v552ru__"+hashlib.sha256(json.dumps(legacy,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()[:24]
    assert first.relation_axis_pressure_id == expected
    target=build_target_entity_pressure_from_observations(observations, "run-1").iloc[0]
    legacy_target=dict(legacy); legacy_target.pop("relation_axis_id"); legacy_target["target_entity_id"]="x"
    expected_target="v552ru__"+hashlib.sha256(json.dumps(legacy_target,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()[:24]
    assert target.target_entity_pressure_id == expected_target
