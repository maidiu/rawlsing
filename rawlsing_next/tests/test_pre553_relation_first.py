from pathlib import Path

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.pre553_relation_first import (
    RelationFirstParquetWriter, _compact_object_from_row, open_relation_handle,
    projection_only_storage, query_relation_handle, storage_budget,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def test_relation_handle_opens_without_full_reconstruction(tmp_path: Path):
    release = validate_c11_source_release(_candidate("relation-first"))
    carrier = ParquetC11Carrier(tmp_path)
    carrier.persist(release)
    handle = open_relation_handle(
        carrier,
        source_sha256=release.source_artifact_ref.content_hash,
        release_id=release.release_id,
        semantic_hash=release.semantic_release_hash,
    )
    assert handle.release_ref == release.release_ref
    assert handle.replay_manifest_ref == release.replay_manifest.ref
    assert query_relation_handle(handle, "select count(*) from respondent_events") == [(2,)]
    assert handle.audit()["row_counts"]["respondent_events"] == 2
    event = next(obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent"))
    assert handle.resolve_object_exact(event.ref) == event


def test_storage_budget_separates_fixed_and_event_scaled_bytes(tmp_path: Path):
    release = validate_c11_source_release(_candidate("storage-budget"))
    carrier = ParquetC11Carrier(tmp_path)
    directory = carrier.persist(release)
    handle = open_relation_handle(carrier, source_sha256=release.source_artifact_ref.content_hash,
                                  release_id=release.release_id, semantic_hash=release.semantic_release_hash)
    receipt = storage_budget(
        {name[:-8]: member for name, member in handle.members.items() if name.endswith(".parquet")},
        fixed_metadata_bytes=123, atomic_staging_peak_bytes=456,
        scratch_execution_peak_bytes=789, respondent_event_count=2,
    )
    assert receipt["FIXED_PER_RELEASE_METADATA_BYTES"] == 123
    assert receipt["EVENT_BEARING_RELATION_BYTES"] == directory.joinpath("respondent_events.parquet").stat().st_size
    assert receipt["POST_SUCCESS_RETAINED_BYTES"] == receipt["CANONICAL_STEADY_STATE_BYTES"]
    assert projection_only_storage(fixed_metadata_bytes=123, bytes_per_event=10,
                                   event_count=100, corpus="TEST")["status"] == "PROJECTION_ONLY"


def test_compact_event_rows_omit_derivable_identity_and_reconstruct_exactly(tmp_path: Path):
    release = validate_c11_source_release(_candidate("compact-parity"))
    events = [obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent")]
    writer = RelationFirstParquetWriter(tmp_path, row_group_size=8192, compression_level=3)
    writer.append("respondent_events", events)
    members = writer.close()
    import pyarrow.parquet as pq
    table = pq.read_table(tmp_path / "respondent_events.parquet")
    assert "compact_payload" in table.column_names
    assert "object_family" not in table.column_names
    assert "object_id" not in table.column_names
    assert "content_hash" not in table.column_names
    rows = table.to_pylist()
    rebuilt = [_compact_object_from_row(row, "respondent_events", writer.dictionaries["respondent_events"]) for row in rows]
    assert [obj.ref for obj in rebuilt] == [obj.ref for obj in events]
    assert [obj.semantic_projection() for obj in rebuilt] == [obj.semantic_projection() for obj in events]
    assert [obj.typed_state for obj in rebuilt] == [obj.typed_state for obj in events]
    assert [obj.authority_snapshot_refs for obj in rebuilt] == [obj.authority_snapshot_refs for obj in events]
    assert [obj.dependency_refs for obj in rebuilt] == [obj.dependency_refs for obj in events]
    assert [obj.producer_replay_locator_or_reference_root for obj in rebuilt] == [obj.producer_replay_locator_or_reference_root for obj in events]
    assert members["respondent_events"].row_count == len(events)


def test_compact_physical_configuration_comparison_is_semantically_identical(tmp_path: Path):
    release = validate_c11_source_release(_candidate("compact-config"))
    events = [obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent")]
    results = []
    for level, row_group in ((3, 4096), (9, 4096), (3, 16384)):
        target = tmp_path / f"z{level}-rg{row_group}"
        writer = RelationFirstParquetWriter(target, row_group_size=row_group, compression_level=level)
        writer.append("respondent_events", events)
        writer.close()
        rows = __import__("pyarrow.parquet", fromlist=["read_table"]).read_table(target / "respondent_events.parquet").to_pylist()
        assert [_compact_object_from_row(row, "respondent_events", writer.dictionaries["respondent_events"]).ref for row in rows] == [obj.ref for obj in events]
        results.append((level, row_group, (target / "respondent_events.parquet").stat().st_size))
    assert all(size > 0 for _, _, size in results)
