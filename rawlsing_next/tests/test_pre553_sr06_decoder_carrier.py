import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_duckdb_direct import open_direct_session, query_canonical_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier, ParquetCarrierError, _logical_digest, _object_row
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
from rawlsing_next.pre553_empirical_objects import AuthorityRef, canonical_json
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


def test_expected_source_identity_is_hashed_once_before_reader_decode(tmp_path: Path, monkeypatch):
    import rawlsing_next.pre553_physical_decoder as decoder

    path = tmp_path / "identity-gate.dta"
    path.write_bytes(b"not a stata file; identity must fail before reader access")
    hash_calls = []
    reader_calls = []
    original_hash = decoder._sha
    monkeypatch.setattr(
        decoder,
        "_sha",
        lambda source: (hash_calls.append(Path(source)) or original_hash(source)),
    )
    monkeypatch.setattr(
        pyreadstat,
        "read_dta",
        lambda *args, **kwargs: (reader_calls.append((args, kwargs)) or (_ for _ in ()).throw(AssertionError("reader called before source identity gate"))),
    )

    with pytest.raises(DecoderError, match="source sha256 mismatch before governed decode"):
        decode_dta(path, expected_source_sha256="0" * 64)
    assert hash_calls == [path]
    assert reader_calls == []


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
    candidate = _candidate("bridge")
    incidence = replace(incidence, source_sha256=candidate.source_release_manifest.source_artifact_content_hash)
    authority = PhysicalSourceAuthorityProjection(
        required_authority_refs=(candidate.authority_snapshots[0].authority_ref,),
        candidate_builder=lambda source, cells, projection: candidate,
    )
    release = build_validated_c11_release(incidence, authority, batch_size=1)
    assert release.release_ref == validate_c11_source_release(candidate).release_ref


def test_bridge_rejects_wrong_source_and_missing_or_nonexact_authority(tmp_path: Path):
    path = tmp_path / "bridge-r2.sav"
    pyreadstat.write_sav(pd.DataFrame({"a": [1]}), str(path))
    incidence = decode_sav(path)
    candidate = _candidate("bridge-r2")
    incidence = replace(incidence, source_sha256=candidate.source_release_manifest.source_artifact_content_hash)
    with pytest.raises(PhysicalC11BridgeError, match="exact AuthorityRef"):
        build_validated_c11_release(incidence, PhysicalSourceAuthorityProjection(
            required_authority_refs=("not-a-ref",), candidate_builder=lambda *_: candidate))
    with pytest.raises(PhysicalC11BridgeError, match="source artifact SHA"):
        build_validated_c11_release(incidence, PhysicalSourceAuthorityProjection(
            required_authority_refs=(candidate.authority_snapshots[0].authority_ref,),
            candidate_builder=lambda *_: replace(candidate, source_release_manifest=replace(
                candidate.source_release_manifest, source_artifact_content_hash="0" * 64))))
    other = AuthorityRef("AUTHORITY_NOT_PACKAGED", "1.0.0", "0" * 64)
    with pytest.raises(PhysicalC11BridgeError, match="absent"):
        build_validated_c11_release(incidence, PhysicalSourceAuthorityProjection(
            required_authority_refs=(other,), candidate_builder=lambda *_: candidate))


def test_direct_session_skips_full_reopen_and_supports_multiple_queries(tmp_path: Path, monkeypatch):
    release = validate_c11_source_release(_candidate("direct-session"))
    carrier = ParquetC11Carrier(tmp_path)
    carrier.persist(release)
    monkeypatch.setattr(carrier, "reopen", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("full reopen called")))
    monkeypatch.setattr(ParquetC11Carrier, "_read_rows", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("full relation read called")))
    with open_direct_session(carrier, source_sha256=release.source_artifact_ref.content_hash,
                             release_id=release.release_id, semantic_hash=release.semantic_release_hash) as session:
        assert session.release_ref == release.release_ref.as_dict()
        assert session.query("select count(*) from respondent_events") == [(2,)]
        assert session.query("select count(*) from routing_eligibility") == [(1,)]


def test_normal_decode_uses_chunk_path_and_compatibility_uses_full_read(tmp_path: Path, monkeypatch):
    import pyreadstat
    import rawlsing_next.pre553_physical_decoder as decoder
    path = tmp_path / "chunk.sav"
    pyreadstat.write_sav(pd.DataFrame({"a": [1, 2, 3]}), str(path))
    original_chunks = pyreadstat.read_file_in_chunks
    chunk_calls = []
    monkeypatch.setattr(pyreadstat, "read_file_in_chunks", lambda *args, **kwargs: (chunk_calls.append(kwargs) or original_chunks(*args, **kwargs)))
    decoded = decode_sav(path)
    list(decoded.iter_cells(2))
    assert chunk_calls and chunk_calls[0]["chunksize"] == 2

    source_sha = decoded.source_sha256
    monkeypatch.setitem(decoder.COMPATIBILITY_ALLOWLIST, source_sha, "latin1")
    full_calls = []
    original_read = pyreadstat.read_sav
    def tracked_read(*args, **kwargs):
        full_calls.append(kwargs.get("metadataonly", False))
        return original_read(*args, **kwargs)
    monkeypatch.setattr(pyreadstat, "read_sav", tracked_read)
    compat = decode_sav(path, encoding="latin1")
    list(compat.iter_cells(2))
    assert full_calls[:2] == [True, False]


def test_real_writer_dta_extended_missing_fixture_or_typed_dependency_limitation(tmp_path: Path):
    path = tmp_path / "extended.dta"
    pyreadstat.write_dta(pd.DataFrame({"answer": [1, float("nan"), 3]}), str(path), missing_user_values={"answer": ["a"]})
    decoded = decode_dta(path)
    declarations = decoded.variables[0].missing_declarations
    if not any(item.get("kind") == "extended" for item in declarations):
        pytest.skip("installed pyreadstat writer/readback does not expose missing_user_values in metadata")
    cell = [cell for cell in decoded.iter_cells() if cell.variable_name == "answer"][1]
    assert cell.missing_state is PhysicalMissingState.FORMAT_EXTENDED_MISSING
    assert cell.source_missing_declaration["reader_token"] == "a"
    assert cell.source_missing_declaration["stata_token"] == ".a"


def test_self_consistent_different_identity_under_old_path_is_rejected(tmp_path: Path):
    release = validate_c11_source_release(_candidate("selector-r2"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow as pa
    import pyarrow.parquet as pq
    identity = pq.read_table(directory / "release_identity.parquet").to_pylist()
    new_id = "REL-REWRITTEN"
    new_hash = hashlib.sha256(b"rewritten-release").hexdigest()
    ref = json.loads(identity[0]["release_ref_json"])
    ref["object_id"], ref["content_hash"] = new_id, new_hash
    identity[0]["release_id"] = new_id
    identity[0]["semantic_release_hash"] = new_hash
    identity[0]["release_ref_json"] = json.dumps(ref, sort_keys=True, separators=(",", ":"))
    pq.write_table(pa.Table.from_pylist(identity), directory / "release_identity.parquet", compression="zstd", compression_level=3)
    manifest = json.loads((directory / "manifest.json").read_text())
    manifest["members"]["release_identity.parquet"] = hashlib.sha256((directory / "release_identity.parquet").read_bytes()).hexdigest()
    manifest["relation_digests"]["release_identity"] = _logical_digest(identity)
    unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
    manifest["release_ref"] = ref
    unsigned["release_ref"] = ref
    manifest["manifest_hash"] = hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()
    (directory / "manifest.json").write_text(canonical_json(manifest) + "\n")
    with pytest.raises(ParquetCarrierError):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)


def test_fully_rehashed_alternate_relation_set_rejects_stale_root_in_reopen_and_direct_session(tmp_path: Path):
    release = validate_c11_source_release(_candidate("strong-root"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow as pa
    import pyarrow.parquet as pq
    event = next(obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent@"))
    altered_fields = dict(event.semantic_fields)
    altered_fields["raw_response_value"] = "REHASHED-ALTERNATE"
    altered = type(event)(typed_state=event.typed_state, authority_snapshot_refs=event.authority_snapshot_refs,
                          dependency_refs=event.dependency_refs,
                          producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
                          **altered_fields)
    event_rows = pq.read_table(directory / "respondent_events.parquet").to_pylist()
    event_rows[0] = _object_row(altered)
    pq.write_table(pa.Table.from_pylist(event_rows), directory / "respondent_events.parquet", compression="zstd", compression_level=3)
    old_replay = release.replay_manifest
    new_closure = tuple(altered.ref if ref == event.ref else ref for ref in old_replay.closure_refs)
    new_replay = replace(old_replay, semantic_projection_hash=hashlib.sha256(b"alternate-projection").hexdigest(), closure_refs=new_closure)
    pq.write_table(pa.Table.from_pylist([_object_row(new_replay)]), directory / "replay_manifest.parquet", compression="zstd", compression_level=3)
    manifest = json.loads((directory / "manifest.json").read_text())
    for member, relation, rows in (("respondent_events.parquet", "respondent_events", event_rows),
                                   ("replay_manifest.parquet", "replay_manifest", [_object_row(new_replay)])):
        manifest["members"][member] = hashlib.sha256((directory / member).read_bytes()).hexdigest()
        manifest["relation_digests"][relation] = _logical_digest(rows)
    unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
    manifest["manifest_hash"] = hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()
    (directory / "manifest.json").write_text(canonical_json(manifest) + "\n")
    with pytest.raises(ParquetCarrierError, match="root"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)
    with pytest.raises(ParquetCarrierError, match="root"):
        open_direct_session(carrier, source_sha256=release.source_artifact_ref.content_hash,
                            release_id=release.release_id, semantic_hash=release.semantic_release_hash)


def test_persisted_replay_manifest_row_identity_is_verified(tmp_path: Path):
    release = validate_c11_source_release(_candidate("replay-row"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow as pa
    import pyarrow.parquet as pq
    rows = pq.read_table(directory / "replay_manifest.parquet").to_pylist()
    rows[0]["content_hash"] = "0" * 64
    pq.write_table(pa.Table.from_pylist(rows), directory / "replay_manifest.parquet", compression="zstd", compression_level=3)
    manifest = json.loads((directory / "manifest.json").read_text())
    manifest["members"]["replay_manifest.parquet"] = hashlib.sha256((directory / "replay_manifest.parquet").read_bytes()).hexdigest()
    manifest["relation_digests"]["replay_manifest"] = _logical_digest(rows)
    unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
    manifest["manifest_hash"] = hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()
    (directory / "manifest.json").write_text(canonical_json(manifest) + "\n")
    with pytest.raises(ParquetCarrierError, match="identity"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)


def test_full_reopen_rejects_canonical_object_absent_from_replay_closure(tmp_path: Path):
    release = validate_c11_source_release(_candidate("closure-root"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    import pyarrow as pa
    import pyarrow.parquet as pq
    event = next(obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent@"))
    fields = dict(event.semantic_fields)
    fields["response_event_id_or_deterministic_index"] = "UNDECLARED-EVENT"
    extra = type(event)(typed_state=event.typed_state, authority_snapshot_refs=event.authority_snapshot_refs,
                        dependency_refs=event.dependency_refs,
                        producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
                        **fields)
    rows = pq.read_table(directory / "respondent_events.parquet").to_pylist() + [_object_row(extra)]
    pq.write_table(pa.Table.from_pylist(rows), directory / "respondent_events.parquet", compression="zstd", compression_level=3)
    manifest = json.loads((directory / "manifest.json").read_text())
    manifest["members"]["respondent_events.parquet"] = hashlib.sha256((directory / "respondent_events.parquet").read_bytes()).hexdigest()
    manifest["relation_digests"]["respondent_events"] = _logical_digest(rows)
    unsigned = {key: manifest[key] for key in ("schema_version", "release_ref", "source_artifact_ref", "members", "relation_digests")}
    manifest["manifest_hash"] = hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()
    (directory / "manifest.json").write_text(canonical_json(manifest) + "\n")
    with pytest.raises(ParquetCarrierError, match="replay closure"):
        carrier.reopen(release.source_artifact_ref.content_hash, release.release_id, release.semantic_release_hash)


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
