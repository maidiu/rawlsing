from __future__ import annotations

import hashlib
import json
import unicodedata

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_pipeline_boundary_consumer import (
    verify_producer_boundary_manifest,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    validate_source_wave_identity_coherence,
    verify_boundary_manifest,
    verify_exact_identity,
    verify_frame_source_wave_identity_coherence,
)


EVS_UID = "sf_evs_v1"
EVS_1981_UID = "wv_evs_1981_v1"
EVS_1990_UID = "wv_evs_1990_v1"
ARAB_UID = "sf_arab_barometer_v1"
ARAB_I_UID = "wv_arab_barometer_i_v1"
AFRO_UID = "sf_afrobarometer_v1"
AFRO_R1_UID = "wv_afrobarometer_r1_v1"
LATIN_UID = "sf_latinobarometro_v1"
LATIN_1995_UID = "wv_latinobarometro_1995_v1"


def _typed_manifest(**overrides):
    payload = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "run_integrity_status": "PASS",
        "evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
        "run_id": "run-1",
        "source": "EVS",
        "wave": "1981",
        "country_code": "LS",
        "shard_id": "shard-1",
        "schema_version": "v1",
        "compiler_version": "compiler-v1",
        "artifacts": [],
    }
    payload.update(overrides)
    return payload


def _write_manifest(tmp_path, payload, name="manifest.json"):
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_evs_1981_and_w1_redundant_representations_resolve_to_one_uid():
    payload = _typed_manifest(
        source="EVS",
        source_family="European Values Study",
        canonical_source="evs",
        wave="1981",
        canonical_wave="W1",
        wave_id="Wave 1",
    )

    identity = verify_exact_identity(
        payload,
        run_id="run-1",
        source="EVS",
        wave="W1",
        country_code="LS",
        shard_id="shard-1",
    )

    assert identity["source_family_uid"] == EVS_UID
    assert identity["wave_uid"] == EVS_1981_UID


def test_evs_1981_and_w2_contradiction_fails_closed():
    payload = _typed_manifest(wave="1981", canonical_wave="W2")

    with pytest.raises(BoundaryContractError, match="WAVE_IDENTITY_CONTRADICTION"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_source_evs_and_source_family_arab_contradiction_fails_closed():
    payload = _typed_manifest(
        source="EVS",
        source_family="Arab Barometer",
        wave="1981",
    )

    with pytest.raises(BoundaryContractError, match="SOURCE_IDENTITY_CONTRADICTION"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_arab_i_w1_wave1_are_equivalent_representations():
    payload = _typed_manifest(
        source="Arab Barometer",
        source_family="ArabBarometer",
        wave="I",
        canonical_wave="W1",
        wave_id="Wave 1",
    )

    coherence = validate_source_wave_identity_coherence(payload, require_complete=True)

    assert coherence.source_family_uid == ARAB_UID
    assert coherence.wave_uid == ARAB_I_UID


def test_afro_r1_round1_are_equivalent_representations():
    payload = _typed_manifest(
        source="Afrobarometer",
        source_family="Afro Barometer",
        wave="R1",
        canonical_wave="ROUND1",
        wave_id="Round 1",
    )

    coherence = validate_source_wave_identity_coherence(payload, require_complete=True)

    assert coherence.source_family_uid == AFRO_UID
    assert coherence.wave_uid == AFRO_R1_UID


def test_latinobarometro_nfc_nfd_unaccented_are_equivalent():
    nfc = "Latinobarómetro"
    nfd = unicodedata.normalize("NFD", nfc)
    payload = _typed_manifest(
        source=nfc,
        source_family=nfd,
        canonical_source="Latinobarometro",
        wave="1995",
        canonical_wave="1995",
    )

    coherence = validate_source_wave_identity_coherence(payload, require_complete=True)

    assert coherence.source_family_uid == LATIN_UID
    assert coherence.wave_uid == LATIN_1995_UID


def test_explicit_uids_matching_historical_labels_are_accepted():
    payload = _typed_manifest(
        source="EVS",
        source_family="European Values Survey",
        wave="1981",
        canonical_wave="W1",
        source_family_uid=EVS_UID,
        wave_uid=EVS_1981_UID,
    )

    identity = verify_exact_identity(
        payload,
        run_id="run-1",
        source="EVS",
        wave="W1",
        source_family_uid=EVS_UID,
        wave_uid=EVS_1981_UID,
    )

    assert identity["source_family_uid"] == EVS_UID
    assert identity["wave_uid"] == EVS_1981_UID


def test_explicit_source_uid_contradicting_historical_label_fails():
    payload = _typed_manifest(
        source="EVS",
        wave="1981",
        source_family_uid=ARAB_UID,
        wave_uid=ARAB_I_UID,
    )

    with pytest.raises(BoundaryContractError, match="SOURCE_IDENTITY_CONTRADICTION"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_explicit_wave_uid_contradicting_historical_label_fails():
    payload = _typed_manifest(
        source="EVS",
        wave="1981",
        canonical_wave="W1",
        source_family_uid=EVS_UID,
        wave_uid=EVS_1990_UID,
    )

    with pytest.raises(BoundaryContractError, match="WAVE_IDENTITY_CONTRADICTION"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_nested_scope_identity_is_not_allowed_to_conflict_with_top_level():
    payload = _typed_manifest(
        source="EVS",
        wave="1981",
        producer_scope_identity={
            "source_family": "Arab Barometer",
            "canonical_wave": "I",
        },
    )

    with pytest.raises(BoundaryContractError, match="SOURCE_IDENTITY_CONTRADICTION"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_run_id_sibling_mismatch_still_fails_exactly():
    payload = _typed_manifest(run_id="run-1", producer_run_id="run-other")

    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:run_id"):
        verify_exact_identity(payload, run_id="run-1", source="EVS", wave="1981")


def test_country_and_shard_mismatch_still_fail_independently():
    country_payload = _typed_manifest(country_code="LS", country="ZA")
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:country_code"):
        verify_exact_identity(
            country_payload,
            run_id="run-1",
            source="EVS",
            wave="1981",
            country_code="LS",
        )

    shard_payload = _typed_manifest(
        shard_id="shard-1",
        producer_scope_identity={"shard_id": "shard-other"},
    )
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:shard_id"):
        verify_exact_identity(
            shard_payload,
            run_id="run-1",
            source="EVS",
            wave="1981",
            shard_id="shard-1",
        )


def test_schema_mismatch_still_fails_consumer_boundary(tmp_path):
    path = _write_manifest(tmp_path, _typed_manifest(schema_version="v2"))

    with pytest.raises(BoundaryContractError, match="PRODUCER_SCHEMA_VERSION_MISMATCH"):
        verify_producer_boundary_manifest(
            path,
            run_id="run-1",
            source="EVS",
            wave="W1",
            country_code="LS",
            shard_id="shard-1",
            required_schema_version="v1",
            required_compiler_version="compiler-v1",
        )


def test_artifact_file_hash_mismatch_still_fails_boundary(tmp_path):
    artifact = tmp_path / "payload.json"
    artifact.write_text("{}\n", encoding="utf-8")
    payload = _typed_manifest(
        artifacts=[
            {
                "path": "payload.json",
                "artifact_file_sha256": "0" * 64,
            }
        ]
    )
    manifest = _write_manifest(tmp_path, payload)

    with pytest.raises(BoundaryContractError, match="ARTIFACT_FILE_SHA256_MISMATCH"):
        verify_boundary_manifest(
            manifest,
            run_id="run-1",
            source="EVS",
            wave="W1",
            country_code="LS",
            shard_id="shard-1",
            required_artifacts=("payload.json",),
        )


def test_correct_artifact_hash_and_alias_equivalent_identity_pass_together(tmp_path):
    artifact = tmp_path / "payload.json"
    artifact.write_text("{}\n", encoding="utf-8")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    payload = _typed_manifest(
        wave="1981",
        canonical_wave="W1",
        artifacts=[
            {
                "path": "payload.json",
                "artifact_file_sha256": digest,
            }
        ],
    )
    manifest = _write_manifest(tmp_path, payload)

    verified = verify_boundary_manifest(
        manifest,
        run_id="run-1",
        source="EVS",
        wave="W1",
        country_code="LS",
        shard_id="shard-1",
        required_artifacts=("payload.json",),
    )

    assert verified.identity["source_family_uid"] == EVS_UID
    assert verified.identity["wave_uid"] == EVS_1981_UID
    assert verified.verified_artifacts[0].artifact_file_sha256 == digest


def test_blank_optional_sibling_fields_do_not_invent_contradictions():
    payload = _typed_manifest(
        source="EVS",
        source_family="",
        survey_family=None,
        canonical_source="",
        wave="1981",
        canonical_wave="",
        wave_id=None,
        source_family_uid="",
        wave_uid="",
    )

    identity = verify_exact_identity(payload, run_id="run-1", source="EVS", wave="W1")

    assert identity["source_family_uid"] == EVS_UID
    assert identity["wave_uid"] == EVS_1981_UID


def test_frame_validator_checks_every_row_and_accepts_equivalent_aliases():
    frame = pd.DataFrame(
        [
            {
                "source": "EVS",
                "source_family": "European Values Study",
                "wave": "1981",
                "canonical_wave": "W1",
                "source_family_uid": EVS_UID,
                "wave_uid": EVS_1981_UID,
            },
            {
                "source": "European Values Survey",
                "canonical_source": "evs",
                "wave": "Wave 1",
                "canonical_wave": "1981",
                "source_family_uid": EVS_UID,
                "wave_uid": EVS_1981_UID,
            },
        ]
    )

    result = verify_frame_source_wave_identity_coherence(
        frame,
        expected_source="EVS",
        expected_wave="W1",
        expected_source_family_uid=EVS_UID,
        expected_wave_uid=EVS_1981_UID,
    )

    assert result["row_count"] == 2
    assert result["source_family_uid"] == EVS_UID
    assert result["wave_uid"] == EVS_1981_UID


def test_frame_validator_fails_on_later_row_contradiction_not_first_row_precedence():
    frame = pd.DataFrame(
        [
            {"source": "EVS", "wave": "1981"},
            {"source": "EVS", "wave": "1981", "canonical_wave": "W2"},
        ]
    )

    with pytest.raises(BoundaryContractError, match="FRAME_SOURCE_WAVE_IDENTITY_INVALID"):
        verify_frame_source_wave_identity_coherence(
            frame,
            expected_source="EVS",
            expected_wave="W1",
        )


def test_generic_consumer_returns_uid_machine_identity_for_alias_equivalent_manifest(tmp_path):
    path = _write_manifest(
        tmp_path,
        _typed_manifest(
            source="EVS",
            source_family="European Values Study",
            wave="1981",
            canonical_wave="W1",
            source_family_uid=EVS_UID,
            wave_uid=EVS_1981_UID,
        ),
    )

    verified = verify_producer_boundary_manifest(
        path,
        run_id="run-1",
        source="EVS",
        wave="W1",
        country_code="LS",
        shard_id="shard-1",
        source_family_uid=EVS_UID,
        wave_uid=EVS_1981_UID,
        required_schema_version="v1",
        required_compiler_version="compiler-v1",
    )

    assert verified.identity["source_family_uid"] == EVS_UID
    assert verified.identity["wave_uid"] == EVS_1981_UID
