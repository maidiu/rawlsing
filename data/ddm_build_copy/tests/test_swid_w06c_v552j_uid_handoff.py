import hashlib
import json

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v552j_structural_handoff import _coherent_scope, _scope_from_manifest, _v553_compatibility_frame, _verify_frame_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.ddm_v552j_handoff import build_v552j_join


UIDS = resolve_source_wave_identity("Arab Barometer", "I")
PAIR = (UIDS.source_family_uid, UIDS.wave_uid)


def _packet(**extra):
    row = {
        "run_id": "run-c", "packet_id": "packet-legacy", "source": "Arab Barometer", "wave": "W1",
        "canonical_wave": "W1", "source_family_uid": PAIR[0], "wave_uid": PAIR[1], "country_code": "EGY",
        "relation_axis_ids_json": json.dumps(["axis-1"]), "target_entity_ids_json": json.dumps(["target-1"]),
        "driver_facet_ids_json": json.dumps(["facet-1"]), "question_ids_json": json.dumps(["q-1"]),
        "certification_status": "CERTIFIED", "joint_support_status": "sufficient_support",
        "joint_directionality_authority_status": "known_directional", "joint_evidence_authority_status": "exact_registry",
        "allowed_downstream_use": True,
    }
    row.update(extra)
    return row


def _fact(**extra):
    row = {
        "run_id": "run-c", "source": "Arab Barometer", "wave": "I", "canonical_wave": "I",
        "source_family_uid": PAIR[0], "wave_uid": PAIR[1], "country_code": "EGY", "shard_id": "",
        "v552_structural_fact_id": "fact-legacy", "v552_pressure_observation_id": "obs-1",
        "source_artifact": "v552_pressure_observation_index", "source_v551_run_id": "run-v551",
        "source_row_hash": "row-hash", "pressure_measurement_hash": "measurement-hash",
        "relation_axis_id": "axis-1", "target_entity_id": "target-1", "driver_facet_id": "facet-1",
        "question_id": "q-1", "measurement_evidence_status": "PRESENT", "structural_fact_status": "PRESENT",
        "pressure_score": 0.25, "pressure_score_status": "OBSERVED_NONZERO", "downstream_permission_status": "ALLOW",
        "structural_fact_lane": "primary_pressure", "structural_fact_grain": "empirical_distribution_pressure_observation",
    }
    row.update(extra)
    return row


def _states():
    state = {"run_integrity_status": "PASS", "evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"}
    return state.copy(), state.copy()


def test_actual_v552j_builder_propagates_one_uid_pair_through_join_and_audit():
    a, b = _states()
    result = build_v552j_join(
        run_id="run-c", v551j_certified=pd.DataFrame([_packet()]), v551j_review=pd.DataFrame(),
        v552_structural_facts=pd.DataFrame([_fact()]),
        v552_temporal_keys=pd.DataFrame([{"v552_structural_fact_id": "fact-legacy", "v552_temporal_key_source_id": "temporal-legacy"}]),
        v551j_state=a, v552_state=b,
    )
    join = result["join_index"]
    audit = result["join_audit"]
    assert len(join) == 1
    assert tuple(join.loc[0, ["source_family_uid", "wave_uid"]]) == PAIR
    assert tuple(audit.loc[0, ["source_family_uid", "wave_uid"]]) == PAIR


def test_uid_scope_is_required_before_semantic_matching():
    a, b = _states()
    packet = _packet(source_family_uid="", wave_uid="")
    result = build_v552j_join(
        run_id="run-c", v551j_certified=pd.DataFrame([packet]), v551j_review=pd.DataFrame(),
        v552_structural_facts=pd.DataFrame([_fact()]), v552_temporal_keys=pd.DataFrame(),
        v551j_state=a, v552_state=b,
    )
    assert result["join_index"].empty
    assert result["join_audit"].iloc[0]["join_status"] == "UNRESOLVED_NO_STRUCTURAL_MATCH"


def test_manifest_and_cross_producer_scope_use_uid_pair_and_preserve_boundaries():
    payload = {"contract_version": "rawlsing_pipeline_boundary_v1", "run_id": "run-c", "producer_run_id": "run-c",
               "source": "Arab Barometer", "wave": "W1", "canonical_wave": "I", "source_family_uid": PAIR[0],
               "wave_uid": PAIR[1], "country_code": "EGY", "producer_scope_identity":
               {"run_id": "run-c", "source": "Arab Barometer", "wave": "W1", "canonical_wave": "I",
                "source_family_uid": PAIR[0], "wave_uid": PAIR[1], "country_code": "EGY"},
               "run_integrity_status": "PASS", "evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"}
    scope = _scope_from_manifest(payload, "V552")
    assert (scope["source_family_uid"], scope["wave_uid"]) == PAIR
    assert _coherent_scope("run-c", scope, {**scope, "source": "Arab Barometer", "wave": "1"})["wave_uid"] == PAIR[1]
    with pytest.raises(BoundaryContractError):
        _coherent_scope("run-c", scope, {**scope, "wave_uid": "wrong-wave"})
    with pytest.raises(BoundaryContractError):
        _coherent_scope("run-c", scope, {**scope, "country_code": "TUN"})


def test_label_only_v551j_manifest_is_resolved_to_governed_uid_scope():
    payload = {"run_id": "run-c", "source": "Arab Barometer", "wave": "Wave 1", "country_code": "EGY",
               "run_integrity_status": "PASS", "evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"}
    scope = _scope_from_manifest(payload, "V551J")
    assert (scope["source_family_uid"], scope["wave_uid"]) == PAIR


def test_frame_scope_rejects_label_match_with_wrong_uid():
    scope = {"run_id": "run-c", "source": "Arab Barometer", "wave": "I", "source_family_uid": PAIR[0],
             "wave_uid": PAIR[1], "country_code": "EGY", "shard_id": ""}
    frame = pd.DataFrame([{"run_id": "run-c", "source": "Arab Barometer", "canonical_wave": "I",
                           "source_family_uid": PAIR[0], "wave_uid": "wrong-wave", "country_code": "EGY"}])
    with pytest.raises(BoundaryContractError):
        _verify_frame_scope(frame, scope, "TEST")


def test_historical_v552j_join_id_payload_remains_packet_fact_only():
    payload = {"run_id": "run-c", "packet_id": "packet-legacy", "v552_structural_fact_id": "fact-legacy"}
    expected = "v552jjoin__" + hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]
    a, b = _states()
    result = build_v552j_join(run_id="run-c", v551j_certified=pd.DataFrame([_packet()]), v551j_review=pd.DataFrame(), v552_structural_facts=pd.DataFrame([_fact()]), v551j_state=a, v552_state=b)
    assert result["join_index"].iloc[0]["v552j_join_id"] == expected
    compat = _v553_compatibility_frame(result["join_index"])
    assert tuple(compat.loc[0, ["source_family_uid", "wave_uid"]]) == PAIR


def test_uid_native_packet_id_and_homology_key_do_not_replace_same_wave_scope():
    a, b = _states()
    packet = _packet(uid_native_packet_id_v1="uid-native-different", cross_wave_homology_key_v1="homology-shared")
    other_wave = resolve_source_wave_identity("Arab Barometer", "II")
    fact = _fact(source_family_uid=other_wave.source_family_uid, wave_uid=other_wave.wave_uid)
    result = build_v552j_join(run_id="run-c", v551j_certified=pd.DataFrame([packet]), v551j_review=pd.DataFrame(), v552_structural_facts=pd.DataFrame([fact]), v551j_state=a, v552_state=b)
    assert result["join_index"].empty
