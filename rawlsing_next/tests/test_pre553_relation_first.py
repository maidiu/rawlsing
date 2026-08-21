from pathlib import Path

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_parquet_carrier import ParquetC11Carrier
from rawlsing_next.pre553_relation_first import open_relation_handle, query_relation_handle
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
