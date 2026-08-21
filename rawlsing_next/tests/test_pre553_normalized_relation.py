from pathlib import Path

import pyarrow.parquet as pq

from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_normalized_relation import (
    NormalizedRespondentEventReader,
    NormalizedRespondentEventWriter,
    query_normalized_relation,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate


def test_normalized_fact_has_typed_columns_and_exact_reconstruction(tmp_path: Path):
    release = validate_c11_source_release(_candidate("normalized-parity"))
    original = [obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent")]
    base = original[0]
    variants = []
    for index, (state, raw, topology) in enumerate((
        ("SUBSTANTIVE_RESPONSE", "observed", "UNORDERED_MULTISELECT_SET"),
        ("MISSING", None, "UNORDERED_MULTISELECT_SET"),
        ("DK", "DK", "RANKED_RESPONSE"),
        ("IAP", "ordinary-dta-absence-looking", "ORDERED_SEQUENCE"),
    )):
        fields = dict(base.semantic_fields)
        fields.update(response_event_id_or_deterministic_index=f"variant-{index}", raw_response_value=raw,
                      response_state=state, multiplicity_order_rank_fields={"kind": topology, "rank": index})
        variants.append(RespondentEvent(
            typed_state=state, authority_snapshot_refs=base.authority_snapshot_refs,
            dependency_refs=base.dependency_refs,
            producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
            **fields))

    writer = NormalizedRespondentEventWriter(tmp_path, row_group_size=2)
    writer.append(variants)
    members = writer.close()
    names = pq.ParquetFile(tmp_path / "respondent_events.normalized.parquet").schema_arrow.names
    assert "compact_payload" not in names
    assert "object_id" not in names
    assert "content_hash" not in names
    assert {"respondent_key", "question_key", "raw_value_kind", "raw_value_text",
            "raw_value_int64", "topology_key", "producer_root_content_hash"}.issubset(names)

    reader = NormalizedRespondentEventReader(tmp_path)
    rebuilt = [reader.reconstruct(row) for row in reader.iter_facts()]
    assert rebuilt == variants
    assert [obj.semantic_projection() for obj in rebuilt] == [obj.semantic_projection() for obj in variants]
    assert reader.audit() == {"respondent_events": 4}
    assert query_normalized_relation(tmp_path, "select count(*), count(distinct question_key) from respondent_events") == [(4, 1)]
    assert members["respondent_events.normalized.parquet"].row_count == 4


def test_normalized_local_keys_are_replay_deterministic(tmp_path: Path):
    release = validate_c11_source_release(_candidate("normalized-keys"))
    events = [obj for obj in release.public_objects if obj.FAMILY.startswith("RespondentEvent")]
    first = NormalizedRespondentEventWriter(tmp_path / "first")
    first.append(events); first.close()
    second = NormalizedRespondentEventWriter(tmp_path / "second")
    second.append(events); second.close()
    for name in ("universe_dimension.parquet", "respondent_dimension.parquet", "question_dimension.parquet",
                 "topology_dimension.parquet", "authority_dimension.parquet"):
        assert pq.read_table(tmp_path / "first" / name).to_pylist() == pq.read_table(tmp_path / "second" / name).to_pylist()
