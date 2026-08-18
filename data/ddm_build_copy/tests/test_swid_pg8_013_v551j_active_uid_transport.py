from __future__ import annotations

import pandas as pd
import pytest

# Production import order loads ddm_v551j_io before packet construction.  The
# binding is intentionally idempotent so an already-imported schema module is
# repaired in place as well.
from data.ddm_build_copy.ddm_v551j_io import bind_v551j_active_uid_transport_schema
from data.ddm_build_copy.ddm_v551j_packets import _uid_payload
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA,
    V551J_JOINT_COMPONENT_INDEX_SCHEMA,
    V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA,
    V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA,
)
from data.ddm_build_copy.compile_v552j_structural_handoff import _verify_frame_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError


AFRO_SOURCE_UID = "sf_afrobarometer_v1"
AFRO_R1_WAVE_UID = "wv_afrobarometer_r1_v1"


def _packet_identity_row() -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": "run-1",
        "packet_id": "packet-1",
        "pattern_id": "pattern-1",
        "family_id": "JCFG-AFRO-R1-MIP-RANKED",
        "source": "Afrobarometer",
        "source_family": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "country_code": "LS",
    }
    row.update(_uid_payload(row))
    return row


def _component_identity_row() -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": "run-1",
        "packet_id": "packet-1",
        "pattern_id": "pattern-1",
        "family_id": "JCFG-AFRO-R1-MIP-RANKED",
        "item_order": 1,
        "component_id": "component-1",
        "source": "Afrobarometer",
        "source_family": "Afrobarometer",
        "canonical_wave": "R1",
        "country_code": "LS",
        "v550j_item_question_id": "question_impl.phase0.e8dc21a068cc141b3efd",
        "v550j_item_var_code": "mip1",
        "v550j_item_response_value_normalized": "10",
    }
    row.update(_uid_payload(row))
    return row


def _v552j_scope() -> dict[str, str]:
    return {
        "run_id": "run-1",
        "source": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "source_family_uid": AFRO_SOURCE_UID,
        "wave_uid": AFRO_R1_WAVE_UID,
        "country_code": "LS",
        "shard_id": "",
        "scope_kind": "country",
    }


def test_active_v22_schemas_retain_additive_uid_identity_fields() -> None:
    bind_v551j_active_uid_transport_schema()
    bind_v551j_active_uid_transport_schema()

    packet_fields = {
        "source_family_uid",
        "wave_uid",
        "uid_key",
        "uid_native_packet_id_v1",
        "cross_wave_homology_key_v1",
    }
    component_fields = {
        "source_family_uid",
        "wave_uid",
        "uid_key",
        "uid_native_component_id_v1",
    }

    assert packet_fields.issubset(V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"])
    assert packet_fields.issubset(V551J_CERTIFIED_JOINT_PACKET_INDEX_SCHEMA["required_columns"])
    assert packet_fields.issubset(V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
    assert component_fields.issubset(V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"])

    for field in packet_fields:
        assert V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"].count(field) == 1
        assert V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"].count(field) == 1
    for field in component_fields:
        assert V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"].count(field) == 1


def test_packet_review_and_component_reindex_preserve_computed_uid_pair() -> None:
    packet = pd.DataFrame([_packet_identity_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    review = packet.assign(
        review_priority="medium",
        review_triage_priority_score=0.5,
    ).reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
    component = pd.DataFrame([_component_identity_row()]).reindex(
        columns=V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"]
    )

    for frame in (packet, review, component):
        assert frame.iloc[0]["source_family_uid"] == AFRO_SOURCE_UID
        assert frame.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
        assert frame.iloc[0]["uid_key"]
        assert frame.iloc[0]["canonical_wave"] == "R1"

    assert packet.iloc[0]["uid_native_packet_id_v1"]
    assert packet.iloc[0]["cross_wave_homology_key_v1"]
    assert component.iloc[0]["uid_native_component_id_v1"]


def test_v552j_accepts_uid_bound_review_packet_without_widening_permission() -> None:
    packet = pd.DataFrame([_packet_identity_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    review = packet.assign(
        review_priority="medium",
        review_triage_priority_score=0.5,
    ).reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])

    _verify_frame_scope(review, _v552j_scope(), "PG8_013_REVIEW")
    assert review.iloc[0]["source_family_uid"] == AFRO_SOURCE_UID
    assert review.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
    assert review.iloc[0]["canonical_wave"] == "R1"


def test_v552j_still_rejects_wrong_uid() -> None:
    packet = pd.DataFrame([_packet_identity_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    packet.loc[:, "wave_uid"] = "wv_deliberately_wrong_pg8_013"

    with pytest.raises(BoundaryContractError):
        _verify_frame_scope(packet, _v552j_scope(), "PG8_013_WRONG_UID")
