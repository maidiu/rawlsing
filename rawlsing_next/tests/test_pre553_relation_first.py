from pathlib import Path

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.pre553_relation_first import (
    open_relation_handle, projection_only_storage, query_relation_handle, storage_budget,
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
