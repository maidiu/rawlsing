import pandas as pd

from data.ddm_build_copy.ddm_source_wave_identity import resolve_source_wave_identity
from data.ddm_build_copy.ddm_v552j_handoff import build_v552j_join


IDENTITY = resolve_source_wave_identity("Arab Barometer", "I")


def test_actual_builder_rejects_scope_without_country_or_shard():
    packet = {
        "run_id": "run-c",
        "packet_id": "packet-legacy",
        "source": "Arab Barometer",
        "canonical_wave": "I",
        "source_family_uid": IDENTITY.source_family_uid,
        "wave_uid": IDENTITY.wave_uid,
        "country_code": "",
        "shard_id": "",
        "relation_axis_ids_json": '["axis-1"]',
        "target_entity_ids_json": '["target-1"]',
        "driver_facet_ids_json": '["facet-1"]',
        "question_ids_json": '["q-1"]',
        "certification_status": "CERTIFIED",
        "joint_support_status": "sufficient_support",
        "joint_directionality_authority_status": "known_directional",
        "joint_evidence_authority_status": "exact_registry",
        "allowed_downstream_use": True,
    }
    fact = {
        "run_id": "run-c",
        "source": "Arab Barometer",
        "canonical_wave": "I",
        "source_family_uid": IDENTITY.source_family_uid,
        "wave_uid": IDENTITY.wave_uid,
        "country_code": "",
        "shard_id": "",
        "v552_structural_fact_id": "fact-legacy",
        "relation_axis_id": "axis-1",
        "target_entity_id": "target-1",
        "driver_facet_id": "facet-1",
        "question_id": "q-1",
        "pressure_score": 0.25,
        "pressure_score_status": "OBSERVED_NONZERO",
        "measurement_evidence_status": "PRESENT",
        "structural_fact_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
    }
    state = {
        "run_integrity_status": "PASS",
        "evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
    }
    result = build_v552j_join(
        run_id="run-c",
        v551j_certified=pd.DataFrame([packet]),
        v551j_review=pd.DataFrame(),
        v552_structural_facts=pd.DataFrame([fact]),
        v552_temporal_keys=pd.DataFrame(),
        v551j_state=state,
        v552_state=state,
    )
    assert result["join_index"].empty
