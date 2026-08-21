from pathlib import Path

import pyarrow.parquet as pq
import pyarrow as pa

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_r4_compaction import R4LocatorLaw, R4RespondentEventReader, R4RespondentEventWriter, query_r4
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def test_r4_sparse_compaction_reconstructs_exact_old_objects(tmp_path: Path):
    release = validate_c11_source_release(_candidate("r4-parity"))
    old = [obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent")]
    replay_ref, release_ref, semantic_hash, coverage = release.replay_manifest.ref, release.release_ref, release.semantic_release_hash, release.m01_m18_coverage
    writer = R4RespondentEventWriter(tmp_path)
    writer.append(old)
    members = writer.close()
    reader = R4RespondentEventReader(tmp_path)
    rebuilt = [reader.reconstruct(row) for row in reader.iter_rows()]
    assert rebuilt == old
    assert [obj.semantic_projection() for obj in rebuilt] == [obj.semantic_projection() for obj in old]
    assert (release.replay_manifest.ref, release.release_ref, release.semantic_release_hash, release.m01_m18_coverage) == (replay_ref, release_ref, semantic_hash, coverage)
    assert reader.audit() == len(old)
    assert query_r4(tmp_path, "select count(*) from respondent_events") == [(2,)]
    assert "typed_state" not in pq.ParquetFile(tmp_path / "respondent_events.r4.parquet").schema_arrow.names
    assert "response_state" not in pq.ParquetFile(tmp_path / "respondent_events.r4.parquet").schema_arrow.names
    assert members["respondent_events.r4.parquet"] > 0


def test_r4_locator_law_removes_event_identity_and_root_overrides(tmp_path: Path):
    release = validate_c11_source_release(_candidate("r4-law"))
    base = next(obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent"))
    events = []
    label = "COURT"
    import hashlib
    from rawlsing_next.pre553_empirical_objects import ExactRef
    def ref(kind, value):
        return ExactRef(kind, f"urn:r4:{kind}:{value}", hashlib.sha256(f"{kind}:{value}".encode()).hexdigest())
    law = R4LocatorLaw(event_id_template=label + "-{locator}", event_group_prefix="G-", event_group_modulus=100,
                       producer_root_kind="REPLAY_ROOT", producer_root_object_template="urn:r4:REPLAY_ROOT:" + label + "-{locator}",
                       producer_root_hash_seed_template="REPLAY_ROOT:" + label + "-{locator}")
    for i in range(20):
        fields = dict(base.semantic_fields)
        fields.update(scoped_respondent_ref=ref("RESPONDENT", i % 4), native_question_ref=ref("QUESTION_NATIVE", i % 3),
                      event_group_id=f"G-{i % 100}", response_event_id_or_deterministic_index=f"{label}-{i}",
                      producer_replay_locator_or_reference_root=ref("REPLAY_ROOT", f"{label}-{i}"),
                      raw_response_value=None if i % 5 == 0 else i, response_state="MISSING" if i % 5 == 0 else "SUBSTANTIVE_RESPONSE")
        state = fields["response_state"]
        events.append(RespondentEvent(typed_state=state, authority_snapshot_refs=base.authority_snapshot_refs,
                                      dependency_refs=base.dependency_refs, producer_replay_locator_or_reference_root=fields.pop("producer_replay_locator_or_reference_root"), **fields))
    writer = R4RespondentEventWriter(tmp_path, locator_law=law)
    writer.append(events); writer.close()
    reader = R4RespondentEventReader(tmp_path)
    assert [reader.reconstruct(row).ref for row in reader.iter_rows()] == [obj.ref for obj in events]
    assert writer.cardinalities["event_overrides"] < 20
    assert pq.ParquetFile(tmp_path / "respondent_events.r4.parquet").schema_arrow.field("question_ordinal").type == pa.uint16()
