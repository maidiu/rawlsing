from __future__ import annotations

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v552j_structural_handoff import _verify_frame_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_v551j_io import (
    bind_v551j_active_uid_transport_schema,
    write_frame_artifact,
)
from data.ddm_build_copy.ddm_v551j_packets import _uid_payload
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_JOINT_COMPONENT_INDEX_SCHEMA,
    V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA,
    V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA,
)


AFRO_SOURCE_UID = "sf_afrobarometer_v1"
AFRO_R1_WAVE_UID = "wv_afrobarometer_r1_v1"
AFRO_R1_SHARD_ID = "Afrobarometer__R1"


def _packet_row(*, canonical_wave: str = "R1") -> dict[str, object]:
    row: dict[str, object] = {
        "run_id": "run-1",
        "packet_id": "packet-1",
        "pattern_id": "pattern-1",
        "family_id": "JCFG-AFRO-R1-MIP-RANKED",
        "source": "Afrobarometer",
        "source_family": "Afrobarometer",
        "wave": canonical_wave,
        "canonical_wave": canonical_wave,
        "country_code": "LS",
    }
    row.update(_uid_payload(row))
    return row


def _component_row() -> dict[str, object]:
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


def _expected_scope() -> dict[str, str]:
    return {
        "run_id": "run-1",
        "source": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "source_family_uid": AFRO_SOURCE_UID,
        "wave_uid": AFRO_R1_WAVE_UID,
        "country_code": "LS",
        "shard_id": AFRO_R1_SHARD_ID,
        "scope_kind": "shard",
    }


def _write(frame: pd.DataFrame, tmp_path, name: str) -> pd.DataFrame:
    path = tmp_path / f"{name}.parquet"
    write_frame_artifact(
        frame,
        path=path,
        schema_path=tmp_path / f"{name}.schema.json",
        name=name,
        run_id="run-1",
        write_csv=False,
        write_parquet=True,
    )
    return pd.read_parquet(path)


def test_active_v22_packet_review_component_schemas_require_shard_id() -> None:
    bind_v551j_active_uid_transport_schema()
    assert "shard_id" in V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    assert "shard_id" in V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"]
    assert "shard_id" in V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"]
    assert V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"].count("shard_id") == 1
    assert V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"].count("shard_id") == 1
    assert V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"].count("shard_id") == 1


def test_publication_binds_frozen_shard_without_mutating_labels_or_input(tmp_path) -> None:
    candidate = pd.DataFrame([_packet_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    review = candidate.assign(
        review_priority="medium",
        review_triage_priority_score=0.5,
    ).reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
    component = pd.DataFrame([_component_row()]).reindex(
        columns=V551J_JOINT_COMPONENT_INDEX_SCHEMA["required_columns"]
    )

    assert candidate.iloc[0]["shard_id"] != AFRO_R1_SHARD_ID
    written_candidate = _write(candidate, tmp_path, "candidate")
    written_review = _write(review, tmp_path, "review")
    written_component = _write(component, tmp_path, "component")

    for frame in (written_candidate, written_review, written_component):
        assert frame.iloc[0]["source_family_uid"] == AFRO_SOURCE_UID
        assert frame.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
        assert frame.iloc[0]["shard_id"] == AFRO_R1_SHARD_ID
        assert frame.iloc[0]["canonical_wave"] == "R1"

    # Publication transport works on a copy; packet assembly state is untouched.
    assert candidate.iloc[0]["canonical_wave"] == "R1"
    assert pd.isna(candidate.iloc[0]["shard_id"]) or str(candidate.iloc[0]["shard_id"]).strip() == ""


def test_alias_equivalent_label_resolves_frozen_canonical_shard_without_rewrite(tmp_path) -> None:
    candidate = pd.DataFrame([_packet_row(canonical_wave="Round 1")]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    written = _write(candidate, tmp_path, "alias_candidate")

    assert written.iloc[0]["canonical_wave"] == "Round 1"
    assert written.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
    assert written.iloc[0]["shard_id"] == AFRO_R1_SHARD_ID


def test_v552j_accepts_serialized_exact_uid_and_shard_scope(tmp_path) -> None:
    candidate = pd.DataFrame([_packet_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    review = candidate.assign(
        review_priority="medium",
        review_triage_priority_score=0.5,
    ).reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])

    written_candidate = _write(candidate, tmp_path, "candidate_scope")
    written_review = _write(review, tmp_path, "review_scope")

    _verify_frame_scope(written_candidate, _expected_scope(), "PG8_014_CANDIDATE")
    _verify_frame_scope(written_review, _expected_scope(), "PG8_014_REVIEW")


def test_conflicting_prepopulated_shard_fails_closed(tmp_path) -> None:
    candidate = pd.DataFrame([_packet_row()]).reindex(
        columns=V551J_JOINT_PACKET_CANDIDATE_INDEX_SCHEMA["required_columns"]
    )
    candidate.loc[:, "shard_id"] = "Afrobarometer__WRONG"

    with pytest.raises(BoundaryContractError, match="V551J_SHARD_ID_TRANSPORT_CONFLICT"):
        _write(candidate, tmp_path, "wrong_shard")
