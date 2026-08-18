from __future__ import annotations

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v552_structural_ddm import _bind_v552j_handoff_shard_scope
from data.ddm_build_copy.compile_v552j_structural_handoff import _verify_frame_scope


AFRO_SOURCE_UID = "sf_afrobarometer_v1"
AFRO_R1_WAVE_UID = "wv_afrobarometer_r1_v1"
AFRO_R1_SHARD_ID = "Afrobarometer__R1"


def _scope() -> dict[str, str]:
    return {
        "source": "Afrobarometer",
        "wave": "R1",
        "canonical_wave": "R1",
        "source_family_uid": AFRO_SOURCE_UID,
        "wave_uid": AFRO_R1_WAVE_UID,
        "country_code": "LS",
        "shard_id": AFRO_R1_SHARD_ID,
        "scope_kind": "shard",
    }


def _structural_fact() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "v552_structural_fact_id": "fact-1",
                "source": "Afrobarometer",
                "source_family": "Afrobarometer",
                "wave": "ROUND1",
                "canonical_wave": "ROUND1",
                "source_family_uid": AFRO_SOURCE_UID,
                "wave_uid": AFRO_R1_WAVE_UID,
                "country_code": "LS",
                "measurement_evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
            }
        ]
    )


def _temporal_key() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "v552_temporal_key_source_id": "temporal-1",
                "v552_structural_fact_id": "fact-1",
                "source": "Afrobarometer",
                "source_family": "Afrobarometer",
                "wave": "ROUND1",
                "canonical_wave": "ROUND1",
                "source_family_uid": AFRO_SOURCE_UID,
                "wave_uid": AFRO_R1_WAVE_UID,
                "country_code": "LS",
                "measurement_evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
            }
        ]
    )


def _outputs() -> dict[str, pd.DataFrame]:
    return {
        "v552_structural_fact_index": _structural_fact(),
        "v552_temporal_key_source_index": _temporal_key(),
    }


def _v552j_scope() -> dict[str, str]:
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


def test_binds_manifest_authenticated_shard_to_both_v552j_handoff_grains() -> None:
    outputs = _outputs()
    _bind_v552j_handoff_shard_scope(outputs, run_id="run-1", scope=_scope())

    for name in ("v552_structural_fact_index", "v552_temporal_key_source_index"):
        frame = outputs[name]
        assert frame.iloc[0]["source_family_uid"] == AFRO_SOURCE_UID
        assert frame.iloc[0]["wave_uid"] == AFRO_R1_WAVE_UID
        assert frame.iloc[0]["country_code"] == "LS"
        assert frame.iloc[0]["shard_id"] == AFRO_R1_SHARD_ID
        # Raw/provenance label remains untouched; UID pair is machine identity.
        assert frame.iloc[0]["canonical_wave"] == "ROUND1"
        assert frame.iloc[0]["wave"] == "ROUND1"


def test_bound_v552_surfaces_pass_existing_v552j_exact_scope_verifier() -> None:
    outputs = _outputs()
    _bind_v552j_handoff_shard_scope(outputs, run_id="run-1", scope=_scope())

    _verify_frame_scope(outputs["v552_structural_fact_index"], _v552j_scope(), "PG8_015_FACT")
    _verify_frame_scope(outputs["v552_temporal_key_source_index"], _v552j_scope(), "PG8_015_TEMPORAL")


def test_conflicting_existing_shard_fails_closed() -> None:
    outputs = _outputs()
    outputs["v552_structural_fact_index"].loc[:, "shard_id"] = "Afrobarometer__WRONG"

    with pytest.raises(RuntimeError, match="SHARD_BIND_CONFLICT"):
        _bind_v552j_handoff_shard_scope(outputs, run_id="run-1", scope=_scope())


def test_wrong_uid_fails_before_shard_is_bound() -> None:
    outputs = _outputs()
    outputs["v552_temporal_key_source_index"].loc[:, "wave_uid"] = "wv_deliberately_wrong_pg8_015"

    with pytest.raises(RuntimeError, match="SHARD_BIND_IDENTITY"):
        _bind_v552j_handoff_shard_scope(outputs, run_id="run-1", scope=_scope())


def test_country_scope_mismatch_fails_closed() -> None:
    outputs = _outputs()
    outputs["v552_structural_fact_index"].loc[:, "country_code"] = "ZA"

    with pytest.raises(RuntimeError, match="SHARD_BIND_SCOPE_MISMATCH"):
        _bind_v552j_handoff_shard_scope(outputs, run_id="run-1", scope=_scope())
