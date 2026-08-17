from __future__ import annotations

import hashlib
import json
import unicodedata
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy import build_v550j_prepared_substrate as prepared
from data.ddm_build_copy import compile_v550j_joint_response_patterns as compiler
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_source_wave_identity import (
    SourceWaveIdentityError,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.ddm_v550j_joint_patterns import _pattern_id


def _identity(source: str, wave: str):
    return resolve_source_wave_identity(source, wave, require_closed_35=True)


def _uid_pattern(source: str, wave: str) -> str:
    identity = _identity(source, wave)
    return compiler._uid_native_pattern_id(
        source_family_uid=identity.source_family_uid,
        wave_uid=identity.wave_uid,
        country_code="ZZ",
        family_id="fam",
        signature_raw="Q1=1|Q2=2",
    )


def _cache_manifest(
    *,
    run_id: str,
    source: str,
    wave: str,
    country_code: str,
    source_family_uid: str,
    wave_uid: str,
    shard_id: str,
    compiler_version: str,
    raw_source: str | None = None,
    raw_wave: str | None = None,
    canonical_display_source: str | None = None,
    canonical_display_wave: str | None = None,
    scope_kind: str = "country",
    identity_contract_version: str | None = None,
) -> dict[str, object]:
    metadata = prepared.v550j_identity_contract_metadata()
    if identity_contract_version is not None:
        metadata["identity_contract_version"] = identity_contract_version
    return {
        "cache_valid": True,
        "run_id": run_id,
        "producer_run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": wave,
        "raw_source": raw_source or source,
        "raw_wave": raw_wave or wave,
        "canonical_display_source": canonical_display_source or source,
        "canonical_display_wave": canonical_display_wave or wave,
        "source_family_uid": source_family_uid,
        "wave_uid": wave_uid,
        "country_code": country_code,
        "shard_id": shard_id,
        "scope_kind": scope_kind,
        "prepared_cache_identity_binding_version": prepared.V550J_PREPARED_CACHE_IDENTITY_BINDING_VERSION,
        "authority_compendium_hash": "authority",
        "question_family_registry_hash": "registry",
        "response_semantics_contract_hash": "semantics",
        "view_schema_hash": "view",
        "compiler_version": compiler_version,
        "substrate_schema_version": prepared.SUBSTRATE_SCHEMA_VERSION,
        **metadata,
    }


def _plant_stale_cache(tmp_path: Path, manifest: dict[str, object], *, source: str, wave: str, country: str) -> None:
    cache_dir = prepared._prepared_cache_dir(
        output_root=tmp_path,
        source=source,
        wave=wave,
        country_code=country,
    )
    cache_dir.mkdir(parents=True, exist_ok=True)
    prepared._prepared_manifest_path(cache_dir).write_text(json.dumps(manifest), encoding="utf-8")
    prepared._prepared_parquet_path(cache_dir).write_bytes(b"stale-cache-placeholder")


def _load_required(tmp_path: Path, *, identity, country: str = "DE", run_id: str = "run-1", shard_id: str = "shard-1"):
    return prepared.load_or_build_v550j_prepared_substrate(
        run_id=run_id,
        source=identity.canonical_display_source,
        source_id=identity.canonical_display_source,
        wave=identity.canonical_display_wave,
        canonical_wave=identity.canonical_display_wave,
        country_code=country,
        source_family_uid=identity.source_family_uid,
        wave_uid=identity.wave_uid,
        raw_source=identity.canonical_display_source,
        raw_wave=identity.canonical_display_wave,
        canonical_display_source=identity.canonical_display_source,
        canonical_display_wave=identity.canonical_display_wave,
        shard_id=shard_id,
        scope_kind="country",
        source_frame=pd.DataFrame(),
        semantics_lookup={},
        response_semantics_contract_hash="semantics",
        output_root=tmp_path,
        question_family_registry_hash="registry",
        authority_compendium_hash="authority",
        view_schema_hash="view",
        compiler_version="compiler-v1",
        substrate_mode="prepared_required",
    )


def test_stale_prepared_cache_from_another_uid_is_rejected(tmp_path: Path) -> None:
    evs = _identity("EVS", "1981")
    arab = _identity("Arab Barometer", "I")
    manifest = _cache_manifest(
        run_id="run-1",
        source="EVS",
        wave="1981",
        country_code="DE",
        source_family_uid=arab.source_family_uid,
        wave_uid=arab.wave_uid,
        shard_id="shard-1",
        compiler_version="compiler-v1",
    )
    _plant_stale_cache(tmp_path, manifest, source="EVS", wave="1981", country="DE")
    with pytest.raises(RuntimeError, match="V550J_PREPARED_CACHE_IDENTITY_OR_CONTRACT_MISMATCH"):
        _load_required(tmp_path, identity=evs)


def test_same_uid_wrong_country_or_scope_cache_is_rejected(tmp_path: Path) -> None:
    evs = _identity("EVS", "1981")
    manifest = _cache_manifest(
        run_id="run-1",
        source="EVS",
        wave="1981",
        country_code="FR",
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        shard_id="wrong-shard",
        scope_kind="shard",
        compiler_version="compiler-v1",
    )
    _plant_stale_cache(tmp_path, manifest, source="EVS", wave="1981", country="DE")
    with pytest.raises(RuntimeError, match="V550J_PREPARED_CACHE_IDENTITY_OR_CONTRACT_MISMATCH"):
        _load_required(tmp_path, identity=evs, country="DE", shard_id="shard-1")


def test_same_uid_stale_nonblank_raw_identity_is_rejected(tmp_path: Path) -> None:
    evs = _identity("EVS", "1981")
    manifest = _cache_manifest(
        run_id="run-1",
        source="EVS",
        wave="1981",
        country_code="DE",
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        shard_id="shard-1",
        compiler_version="compiler-v1",
        raw_wave="W1",
    )
    _plant_stale_cache(tmp_path, manifest, source="EVS", wave="1981", country="DE")
    with pytest.raises(RuntimeError, match="V550J_PREPARED_CACHE_IDENTITY_OR_CONTRACT_MISMATCH"):
        _load_required(tmp_path, identity=evs)


def test_identity_contract_version_mismatch_rejects_required_cache(tmp_path: Path) -> None:
    evs = _identity("EVS", "1981")
    manifest = _cache_manifest(
        run_id="run-1",
        source="EVS",
        wave="1981",
        country_code="DE",
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        shard_id="shard-1",
        compiler_version="compiler-v1",
        identity_contract_version="obsolete_identity_contract",
    )
    _plant_stale_cache(tmp_path, manifest, source="EVS", wave="1981", country="DE")
    with pytest.raises(RuntimeError, match="V550J_PREPARED_CACHE_IDENTITY_OR_CONTRACT_MISMATCH"):
        _load_required(tmp_path, identity=evs)


def test_identity_contract_version_mismatch_rebuilds_in_build_mode(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    evs = _identity("EVS", "1981")
    manifest = _cache_manifest(
        run_id="run-1",
        source="EVS",
        wave="1981",
        country_code="DE",
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        shard_id="shard-1",
        compiler_version="compiler-v1",
        identity_contract_version="obsolete_identity_contract",
    )
    _plant_stale_cache(tmp_path, manifest, source="EVS", wave="1981", country="DE")
    monkeypatch.setattr(prepared, "_should_harmonize", lambda _frame: False)
    monkeypatch.setattr(pd.DataFrame, "to_parquet", lambda self, path, index=False: Path(path).write_bytes(b"fresh"))
    source_frame = pd.DataFrame(
        [
            {
                "run_id": "run-1",
                "source": "EVS",
                "wave": "1981",
                "canonical_wave": "1981",
                "country_code": "DE",
                "respondent_id": "r1",
                "var_code": "Q1",
                "response_value_normalized": "1",
            }
        ]
    )
    rebuilt, fresh_manifest = prepared.load_or_build_v550j_prepared_substrate(
        run_id="run-1",
        source="EVS",
        source_id="EVS",
        wave="1981",
        canonical_wave="1981",
        country_code="DE",
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        raw_source="EVS",
        raw_wave="W1",
        canonical_display_source="EVS",
        canonical_display_wave="1981",
        shard_id="shard-1",
        scope_kind="country",
        source_frame=source_frame,
        semantics_lookup={},
        response_semantics_contract_hash="semantics",
        output_root=tmp_path,
        question_family_registry_hash="registry",
        authority_compendium_hash="authority",
        view_schema_hash="view",
        compiler_version="compiler-v1",
        substrate_mode="prepared_or_build",
    )
    assert not rebuilt.empty
    assert fresh_manifest["cache_loaded"] is False
    assert fresh_manifest["identity_contract_version"] == prepared.v550j_identity_contract_metadata()["identity_contract_version"]
    assert fresh_manifest["raw_wave"] == "W1"


@pytest.mark.parametrize("a,b", [("1981", "W1"), ("1999", "W3")])
def test_evs_aliases_produce_one_uid_native_pattern_identity(a: str, b: str) -> None:
    assert _uid_pattern("EVS", a) == _uid_pattern("EVS", b)


def test_arab_aliases_produce_one_uid_native_pattern_identity() -> None:
    ids = {_uid_pattern("Arab Barometer", value) for value in ("I", "W1", "Wave 1", "1")}
    assert len(ids) == 1


def test_afro_aliases_produce_one_uid_native_pattern_identity() -> None:
    ids = {_uid_pattern("Afrobarometer", value) for value in ("R1", "ROUND1", "Round 1")}
    assert len(ids) == 1


def test_latinobarometro_unicode_and_unaccented_aliases_produce_one_uid_native_identity() -> None:
    nfc = unicodedata.normalize("NFC", "Latinobarómetro")
    nfd = unicodedata.normalize("NFD", "Latinobarómetro")
    ids = {_uid_pattern(source, "2011") for source in (nfc, nfd, "Latinobarometro")}
    assert len(ids) == 1


def test_legacy_pattern_id_is_byte_unchanged_and_uid_id_is_additive() -> None:
    payload = {
        "family_id": "fam",
        "source": "EVS",
        "wave": "1981",
        "country_code": "DE",
        "signature_raw": "Q1=1|Q2=2",
    }
    expected_legacy = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    legacy = _pattern_id(**payload)
    assert legacy == expected_legacy
    evs = _identity("EVS", "1981")
    migrated = compiler._attach_v550j_uid_identity(
        {
            "joint_response_pattern_index": pd.DataFrame(
                [
                    {
                        "pattern_id": legacy,
                        "family_id": "fam",
                        "country_code": "DE",
                        "pattern_signature_raw": "Q1=1|Q2=2",
                        "support_score": 0.7,
                    }
                ]
            )
        },
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        identity_contract_version="swid_uid_v1",
        raw_source="EVS",
        raw_wave="W1",
        canonical_display_source="EVS",
        canonical_display_wave="1981",
    )["joint_response_pattern_index"]
    assert migrated.loc[0, "pattern_id"] == expected_legacy
    assert migrated.loc[0, compiler.V550J_UID_PATTERN_ID_FIELD].startswith("v550juid1__")
    assert migrated.loc[0, "pattern_uid_namespace"] == compiler.V550J_UID_PATTERN_ID_NAMESPACE
    assert migrated.loc[0, "pattern_uid_version"] == compiler.V550J_UID_PATTERN_ID_VERSION


def test_raw_and_canonical_roles_are_explicit_not_lexically_assigned() -> None:
    evs = _identity("EVS", "1981")
    shard = pd.DataFrame(
        [
            {
                "source": "EVS",
                "raw_db_source": "EVS",
                "wave": "W1",
                "raw_db_wave": "W1",
                "canonical_wave": "1981",
                "source_family_uid": evs.source_family_uid,
                "wave_uid": evs.wave_uid,
            }
        ]
    )
    resolved = compiler._resolve_v550j_source_wave_identity(shard, shard.copy())
    assert resolved["raw_wave"] == "W1"
    assert resolved["canonical_display_wave"] == "1981"
    assert compiler._ordered_wave_query_values("W1", "1981") == ["W1", "1981"]
    assert compiler._legacy_wave_compatibility_token("W1", "1981") == "1981"


def test_contradictory_populated_identity_fails_closed() -> None:
    evs = _identity("EVS", "1981")
    arab = _identity("Arab Barometer", "I")
    shard = pd.DataFrame(
        [
            {
                "source": "EVS",
                "wave": "1981",
                "source_family_uid": arab.source_family_uid,
                "wave_uid": evs.wave_uid,
            }
        ]
    )
    with pytest.raises(BoundaryContractError, match="CONTRADICTION"):
        compiler._resolve_v550j_source_wave_identity(shard, shard.copy())


def test_asian_barometer_w6_cannot_become_production_v550j_work() -> None:
    w6 = resolve_source_wave_identity("Asian Barometer", "W6")
    frame = pd.DataFrame(
        [
            {
                "source": "Asian Barometer",
                "raw_db_source": "Asian Barometer",
                "wave": "W6",
                "raw_db_wave": "W6",
                "canonical_wave": "W6",
                "source_family_uid": w6.source_family_uid,
                "wave_uid": w6.wave_uid,
            }
        ]
    )
    with pytest.raises(SourceWaveIdentityError):
        compiler._resolve_v550j_source_wave_identity(frame, frame.copy())


def test_identity_attachment_does_not_change_semantic_or_publishability_fields() -> None:
    evs = _identity("EVS", "1981")
    legacy = _pattern_id("fam", "EVS", "1981", "DE", "Q1=1|Q2=2")
    pattern = pd.DataFrame(
        [
            {
                "pattern_id": legacy,
                "family_id": "fam",
                "country_code": "DE",
                "pattern_signature_raw": "Q1=1|Q2=2",
                "boundary_pattern_type": "bounded",
                "support_score": 0.75,
            }
        ]
    )
    association = pd.DataFrame(
        [
            {
                "pattern_id": legacy,
                "family_id": "fam",
                "country_code": "DE",
                "association_lane": "substantive_attitude_association",
                "association_lane_publishability": "publishable_lane",
                "association_publication_status": "publishable",
                "n_overlap_unweighted": 42,
            }
        ]
    )
    before_pattern = pattern.copy(deep=True)
    before_association = association.copy(deep=True)
    migrated = compiler._attach_v550j_uid_identity(
        {
            "joint_response_pattern_index": pattern,
            "joint_pattern_association_index": association,
        },
        source_family_uid=evs.source_family_uid,
        wave_uid=evs.wave_uid,
        identity_contract_version="swid_uid_v1",
        raw_source="EVS",
        raw_wave="W1",
        canonical_display_source="EVS",
        canonical_display_wave="1981",
    )
    for column in before_pattern.columns:
        assert migrated["joint_response_pattern_index"][column].equals(before_pattern[column])
    for column in before_association.columns:
        assert migrated["joint_pattern_association_index"][column].equals(before_association[column])


def test_legacy_prepared_cache_path_remains_label_derived() -> None:
    path = prepared._prepared_cache_dir(
        output_root=Path("/tmp/v550j"),
        source="EVS",
        wave="1981",
        country_code="DE",
    )
    assert str(path).endswith("cache/prepared_response_substrate/source=EVS/wave=1981/country_code=DE")
    assert "source_family_uid=" not in str(path)
    assert "wave_uid=" not in str(path)
