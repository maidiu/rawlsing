import hashlib
import json
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_duckdb_direct import query_canonical_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError, _logical_digest
from rawlsing_next.pre553_physical_c11_bridge import (
    PhysicalC11BridgeError, PhysicalSourceAuthorityProjection, build_validated_c11_release,
)
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    COMPATIBILITY_ONLY,
    DecoderError,
    PhysicalMissingState,
    classify_physical_value,
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
    score = [c for c in decoded.iter_cells(batch_size=2) if c.variable_name == "score"]
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
    answer = [c for c in decoded.iter_cells(batch_size=2) if c.variable_name == "answer"]
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


def test_extended_missing_is_distinct_and_token_preserving():
    state, declaration = classify_physical_value(".a", ({"kind": "extended", "token": ".a"},))
    assert state is PhysicalMissingState.FORMAT_EXTENDED_MISSING
    assert declaration == {"kind": "extended", "token": ".a"}


def test_physical_batches_have_stable_digest_and_no_complete_cell_tuple(tmp_path: Path):
    path = tmp_path / "batch.sav"
    pyreadstat.write_sav(pd.DataFrame({"a": list(range(8)), "b": list(range(8, 16))}), str(path))
    decoded = decode_sav(path)
    assert not hasattr(decoded, "cells")

    def digest(batch_size):
        cells = []
        for batch in decoded.iter_batches(batch_size):
            assert len(batch) <= batch_size
            cells.extend((cell.row_ordinal, cell.variable_ordinal, cell.variable_name,
                          cell.raw_value, cell.missing_state.value) for cell in batch)
        return hashlib.sha256(json.dumps(cells, sort_keys=True).encode()).hexdigest(), cells

    first, cells = digest(3)
    second, same_cells = digest(11)
    assert first == second
    assert cells == same_cells
    assert len(cells) == decoded.row_count * len(decoded.variables)


def test_parquet_roundtrip_atomicity_corruption_and_direct_duckdb(tmp_path: Path):
    release = validate_c11_source_release(_candidate("sr06"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow.parquet as pq
    assert {"field_response_state", "field_raw_response_value", "field_scoped_respondent_ref_json"}.issubset(
        set(pq.read_schema(directory / "respondent_events.parquet").names)
    )
    assert not (directory / "release.parquet").exists()
    assert not (directory / "objects.parquet").exists()
    assert carrier.persist(release) == directory
    reopened = carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    assert reopened.release_ref == release.release_ref
    assert reopened.semantic_release_hash == release.semantic_release_hash
    assert reopened.source_artifact_ref == release.source_artifact_ref
    assert reopened.public_objects == release.public_objects
    assert reopened.internal_records == release.internal_records
    assert reopened.replay_manifest == release.replay_manifest
    assert dict(reopened.m01_m18_coverage) == dict(release.m01_m18_coverage)
    assert query_canonical_release(
        carrier, source_sha256=release.source_artifact_ref.content_hash, release_id=release.release_id,
        semantic_hash=release.semantic_release_hash, sql="select count(*) from respondent_events where field_response_state = 'SUBSTANTIVE_RESPONSE'",
    ) == [(2,)]
    assert query_canonical_release(
        carrier, source_sha256=release.source_artifact_ref.content_hash, release_id=release.release_id,
        semantic_hash=release.semantic_release_hash, sql="select count(*) from release_identity",
    ) == [(1,)]
    assert not list(tmp_path.rglob("*.duckdb"))

    manifest = directory / "manifest.json"
    original_manifest = manifest.read_bytes()
    manifest.write_bytes(original_manifest.replace(b"PRE553_PARQUET", b"BROKEN_PARQUET", 1))
    with pytest.raises(ParquetCarrierError, match="manifest"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    manifest.write_bytes(original_manifest)
    member = directory / "respondent_events.parquet"
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


def test_physical_to_i02_bridge_requires_explicit_authority(tmp_path: Path):
    path = tmp_path / "bridge.sav"
    pyreadstat.write_sav(pd.DataFrame({"a": [1]}), str(path))
    incidence = decode_sav(path)
    with pytest.raises(PhysicalC11BridgeError, match="authority"):
        build_validated_c11_release(incidence, None)

    candidate = _candidate("bridge")
    authority = PhysicalSourceAuthorityProjection(
        required_authority_refs=("EXPLICIT_SOURCE_AUTHORITY",),
        candidate_builder=lambda source, cells, projection: candidate,
    )
    release = build_validated_c11_release(incidence, authority, batch_size=1)
    assert release.release_ref == validate_c11_source_release(candidate).release_ref


def test_relation_semantic_mutation_fails_even_when_manifest_is_rewritten(tmp_path: Path):
    release = validate_c11_source_release(_candidate("relation-integrity"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow as pa
    import pyarrow.parquet as pq
    table = pq.read_table(directory / "respondent_events.parquet")
    rows = table.to_pylist()
    rows[0]["field_response_state"] = "REFUSAL"
    pq.write_table(pa.Table.from_pylist(rows), directory / "respondent_events.parquet", compression="zstd", compression_level=3)
    manifest_path = directory / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["members"]["respondent_events.parquet"] = hashlib.sha256((directory / "respondent_events.parquet").read_bytes()).hexdigest()
    manifest["relation_digests"]["respondent_events"] = _logical_digest(rows)
    unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
    manifest["manifest_hash"] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n")
    with pytest.raises(ParquetCarrierError):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
