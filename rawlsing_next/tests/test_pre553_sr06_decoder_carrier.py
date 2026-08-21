import hashlib
import json
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_duckdb_direct import query_canonical_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    DecoderError,
    PhysicalMissingState,
    _compatibility_config,
    decode_dta,
    decode_sav,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def test_sav_preserves_raw_values_missing_classes_and_metadata(tmp_path: Path):
    path = tmp_path / "hostile.sav"
    pyreadstat.write_sav(
        pd.DataFrame({"score": [1, -1, -2, 999, None], "text": ["a", "b", "c", "d", "e"]}),
        str(path), column_labels=["Raw score", "Raw text"], variable_value_labels={"score": {-1: "refused", 1: "yes"}},
        missing_ranges={"score": [{"lo": -2, "hi": -1}, 999]},
    )
    decoded = decode_sav(path)
    score = [c for c in decoded.cells if c.variable_name == "score"]
    assert [c.row_ordinal for c in score] == [1, 2, 3, 4, 5]
    assert [c.raw_value for c in score] == [1, -1, -2, 999, None]
    assert [c.missing_state for c in score] == [
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
        PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
        PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
        PhysicalMissingState.SYSTEM_MISSING,
    ]
    assert decoded.variables[0].ordinal == 1
    assert decoded.variables[0].name == "score"
    assert decoded.variables[0].variable_label == "Raw score"
    assert decoded.variables[0].value_labels["-1.0"] == "refused"
    assert decoded.reader_configuration["user_missing"] is True
    assert decoded.reader_configuration["apply_value_formats"] is False


def test_dta_keeps_ordinary_nonresponse_like_code_ordinary(tmp_path: Path):
    path = tmp_path / "hostile.dta"
    pyreadstat.write_dta(
        pd.DataFrame({"answer": [1, 98, None], "text": ["ok", "DK", "missing"]}),
        str(path), variable_value_labels={"answer": {98: "Don't know"}},
    )
    decoded = decode_dta(path)
    answer = [c for c in decoded.cells if c.variable_name == "answer"]
    assert answer[0].missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
    assert answer[1].raw_value == 98
    assert answer[1].missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
    assert answer[2].missing_state is PhysicalMissingState.SYSTEM_MISSING
    assert decoded.source_format == "DTA"
    assert decoded.variables[0].ordinal == 1


def test_compatibility_allowlist_is_exact_and_nonsemantic():
    sha, encoding = next(iter(COMPATIBILITY_ALLOWLIST.items()))
    assert _compatibility_config(sha, encoding) == {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}
    with pytest.raises(DecoderError):
        _compatibility_config("0" * 64, encoding)
    with pytest.raises(DecoderError):
        _compatibility_config(sha, "auto")
    with pytest.raises(DecoderError):
        _compatibility_config(sha, "utf-8")


def test_parquet_roundtrip_atomicity_corruption_and_direct_duckdb(tmp_path: Path):
    release = validate_c11_source_release(_candidate("sr06"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    assert carrier.persist(release) == directory
    reopened = carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    assert reopened.release_ref == release.release_ref
    assert reopened.semantic_release_hash == release.semantic_release_hash
    assert reopened.source_artifact_ref == release.source_artifact_ref
    assert reopened.public_objects == release.public_objects
    assert reopened.internal_records == release.internal_records
    assert reopened.replay_manifest == release.replay_manifest
    assert reopened.m01_m18_coverage == release.m01_m18_coverage
    assert query_canonical_release(
        carrier, source_sha256=release.source_artifact_ref.content_hash, release_id=release.release_id,
        semantic_hash=release.semantic_release_hash, sql="select count(*) from objects",
    ) == [(len(release.public_objects) + len(release.internal_records) + 1,)]
    assert not list(tmp_path.rglob("*.duckdb"))

    manifest = directory / "manifest.json"
    original_manifest = manifest.read_bytes()
    manifest.write_bytes(original_manifest.replace(b"PRE553_PARQUET", b"BROKEN_PARQUET", 1))
    with pytest.raises(ParquetCarrierError, match="manifest"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    manifest.write_bytes(original_manifest)
    member = directory / "objects.parquet"
    original_member = member.read_bytes()
    member.write_bytes(original_member + b"corrupt")
    with pytest.raises(ParquetCarrierError, match="corrupt"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    member.write_bytes(original_member)
    with pytest.raises(ParquetCarrierError):
        carrier.reopen("0" * 64, release.release_id, release.semantic_release_hash)
    with pytest.raises(ParquetCarrierError, match="exact"):
        carrier.reopen("latest", release.release_id, release.semantic_release_hash)
    with pytest.raises(ParquetCarrierError, match="DATABASE_URL"):
        query_canonical_release(carrier, source_sha256=release.source_artifact_ref.content_hash,
                                release_id=release.release_id, semantic_hash=release.semantic_release_hash,
                                sql="select * from DATABASE_URL")
