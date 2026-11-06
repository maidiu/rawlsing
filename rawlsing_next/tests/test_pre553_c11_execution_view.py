from dataclasses import replace
import json
import shutil
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rawlsing_next import _pre553_c11_execution_view as compact
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture


def _material(result):
    return (
        result.c11_release.release_ref,
        result.c11_release.replay_manifest.ref,
        tuple(fact.as_dict() for fact in result.object_graph.empirical_facts),
        tuple(receipt.as_dict() for receipt in result.object_graph.discovery_receipts),
        result.replay_receipt,
    )


def _cache(monkeypatch, tmp_path):
    root = tmp_path / "cache"
    monkeypatch.setenv(compact._CACHE_ENV, str(root))
    return root


def test_compact_hot_route_uses_no_native_event_reconstruction_and_exact_lookup(tmp_path, monkeypatch):
    fx = _fixture()
    expected = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    directory = _cache(monkeypatch, tmp_path)

    def unexpected(*_args):
        pytest.fail("Route B and the I03/I05 hot path reconstructed a full native event")

    with monkeypatch.context() as patch:
        patch.setattr(compact._EventLane, "materialize", unexpected)
        observed = _execute(fx)
        assert len(tuple(directory.glob("c11-events-*.parquet"))) == 1
        compact_public = observed.c11_release.public_objects
        assert isinstance(compact_public, compact._CompactPublicObjects)
        assert sum(isinstance(entry, int) for entry in compact_public.entries) == sum(
            obj.schema_id == "RespondentEvent" for obj in expected.public_objects
        ) > 0
        assert observed.c11_release.release_ref == expected.release_ref

    assert [obj.as_dict() for obj in compact_public] == [obj.as_dict() for obj in expected.public_objects]
    repository = C11Repository((observed.c11_release,))
    for obj in expected.public_objects:
        assert repository.resolve_object_exact(obj.ref).as_dict() == obj.as_dict()


def test_cache_hit_delete_and_rehashed_same_key_poison_rebuild(tmp_path, monkeypatch):
    fx = _fixture()
    directory = _cache(monkeypatch, tmp_path)
    baseline = _material(_execute(fx))
    path, = directory.glob("c11-events-*.parquet")
    original_bytes = path.read_bytes()
    with monkeypatch.context() as patch:
        def unexpected(_value):
            pytest.fail("a warm accelerator reserialized current I02 event bodies")

        patch.setattr(compact, "canonical_json", unexpected)
        assert _material(_execute(fx)) == baseline

    table = pq.read_table(path)
    bodies = table.column(compact._EVENT_BODY_COLUMN).to_pylist()
    changed = json.loads(bodies[0])
    fields = changed["semantic_fields"]
    fields["raw_response_value"] = "forged-response"
    fields["canonical_response_value_if_authorized"] = "forged-response"
    bodies[0] = compact.canonical_json(changed).encode("utf-8")
    forged = pa.table({compact._EVENT_BODY_COLUMN: pa.array(bodies, type=pa.binary())})
    pq.write_table(forged.replace_schema_metadata(table.schema.metadata), path, compression="zstd")
    assert path.read_bytes() != original_bytes
    assert _material(_execute(fx)) == baseline
    assert path.read_bytes() == original_bytes

    path.unlink()
    assert _material(_execute(fx)) == baseline
    assert path.read_bytes() == original_bytes


def test_stale_cache_and_torn_publication_keep_previous_complete_slot(tmp_path, monkeypatch):
    fx = _fixture()
    directory = _cache(monkeypatch, tmp_path)
    baseline = _material(_execute(fx))
    path, = directory.glob("c11-events-*.parquet")
    original_bytes = path.read_bytes()
    changed = {**fx, "stream": replace(fx["stream"], decoder_metadata_digest="e" * 64)}

    destinations = []

    def interrupted(staged, destination):
        assert Path(staged).is_file() and destination.parent == directory
        destinations.append(destination)
        raise OSError("test-only interrupted publication")

    with monkeypatch.context() as patch:
        patch.setattr(compact.os, "replace", interrupted)
        assert _material(_execute(changed)) == baseline
    assert path.read_bytes() == original_bytes
    assert tuple(directory.iterdir()) == (path,)
    destination, = destinations
    if destination != path:
        shutil.copy2(path, destination)  # Structurally intact member with a stale key.
    assert _material(_execute(changed)) == baseline
    assert destination.read_bytes() != original_bytes
    assert _material(_execute(fx)) == baseline
    assert path.read_bytes() == original_bytes


def test_revoked_workload_never_opens_warmed_accelerator(tmp_path, monkeypatch):
    from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError
    from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
    from rawlsing_next.tests.test_universal_workload_custody import HOST, PURPOSE, _issued_workloads

    directory = _cache(monkeypatch, tmp_path)
    bundle, issued = _issued_workloads(tmp_path)

    def execute(packet):
        return execute_test_only_workload(
            issued=packet, source_factory=lambda _ref: bundle.physical_stream,
            host=HOST, purpose=PURPOSE,
        )

    original = execute(issued[0])
    assert any(directory.glob("c11-events-*.parquet"))
    revoked = replace(issued[0], record=replace(issued[0].record, currentness="REVOKED"))

    def unexpected(*_args):
        pytest.fail("revoked issuance reached the warmed cache")

    with monkeypatch.context() as patch:
        patch.setattr(compact, "_read_bodies", unexpected)
        with pytest.raises(WorkloadAdmissionError, match="CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED"):
            execute(revoked)
    assert execute(issued[0]).output_refs == original.output_refs


def test_compact_warm_index_preserves_e3_same_identity_fault_recovery(monkeypatch):
    from types import MappingProxyType

    monkeypatch.delenv(compact._CACHE_ENV, raising=False)
    fx = _fixture()
    route = _execute(fx)
    executor = route.repository_binding.executor
    repo = executor.repository
    key, = repo._i03_release_indices
    before = repo._i03_release_indices[key]
    dropped = min(before.respondents)
    repo._i03_release_indices[key] = replace(
        before, respondents=MappingProxyType({
            key: value for key, value in before.respondents.items() if key != dropped
        }),
    )
    request = fx["requests"][0]
    observed = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
    expected = route.i03_results[0]
    assert tuple(fact.as_dict() for fact in observed.facts) == tuple(
        fact.as_dict() for fact in expected.facts
    )
    assert repo._i03_release_indices[key].respondents == before.respondents


def test_legacy_in_memory_incidence_does_not_require_file_decoder_receipt(tmp_path, monkeypatch):
    from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
    from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture as incidence_fixture

    directory = _cache(monkeypatch, tmp_path)
    fx = incidence_fixture("compact-in-memory")
    repository, release = build_source_backed_c11_repository(fx["incidence"], fx["projection"])
    assert isinstance(release.public_objects, compact._CompactPublicObjects)
    assert repository.resolve_release_exact(release.release_ref) is release
    assert not tuple(directory.iterdir())


def test_selector_reference_exports_cannot_forge_supported_provenance(monkeypatch):
    from rawlsing_next._pre553_query_predicate import _select_respondent_events
    from rawlsing_next.pre553_empirical_objects import ExactRef

    monkeypatch.delenv(compact._CACHE_ENV, raising=False)
    fx = _fixture()
    route = _execute(fx)
    executor = route.repository_binding.executor
    repository = executor.repository
    index, = repository._i03_release_indices.values()
    assert len(index.respondents) > 1
    selectors = [event for key in index.respondents for target in fx["qrefs"].values()
                 for event in _select_respondent_events(index, key, target, native_only=True)]
    # The O question has repeated ordered occurrences for each respondent.
    assert len(selectors) > len(index.respondents) * len(fx["qrefs"])
    native = {event.ref.key: repository.resolve_object_exact(event.ref).as_dict() for event in selectors}
    request = fx["requests"][0]

    def facts():
        return [fact.as_dict() for fact in executor.execute_i03(
            query_ref=request.query_ref, predicate_ref=request.predicate_ref,
        ).facts]

    before = facts()
    for event in selectors:
        for field in ("ref", "native_question_ref", "authority_snapshot_refs"):
            exported = getattr(event, field)
            if field == "authority_snapshot_refs":
                exported = exported[0]
            original = exported.as_dict()
            for name in original:
                exported.__dict__[name] = "f" * 64 if "hash" in name else "urn:test:forged"
            assert facts() == before
            fresh = getattr(event, field)
            if field == "authority_snapshot_refs":
                fresh = fresh[0]
            assert fresh.as_dict() == original
            assert repository.resolve_object_exact(event.ref).as_dict() == native[event.ref.key]
            exported.__dict__.update(original)
            assert facts() == before
        assert isinstance(event.ref, ExactRef)


def test_selector_v1_dimensions_and_occurrences_match_native_after_descendant_faults(monkeypatch):
    from rawlsing_next._pre553_query_predicate import (
        _SELECTOR_CONTRACT_VERSION, _build_release_index, _select_respondent_events,
    )
    from rawlsing_next.pre553_empirical_objects import RespondentEvent, exact_ref
    from rawlsing_next.tests.test_pre553_empirical_query import _ref

    monkeypatch.delenv(compact._CACHE_ENV, raising=False)
    fx = _fixture()
    mapping_authority = next(authority.authority_ref for authority in fx["projection"].authority_snapshots
                             if authority.authority_kind == "NATIVE_CANONICAL_MAPPING_HARMONIZATION")
    questions = tuple(replace(
        question,
        semantic_authority_ref=mapping_authority,
        canonical_question_ref_or_typed_absence=_ref("QUESTION_CANONICAL", question.native_question_ref.key),
        component_subitem_ref_or_typed_absence=_ref("COMPONENT", question.native_question_ref.key),
    ) for question in fx["projection"].questions)
    bindings = {question.native_question_ref: question for question in questions}
    projection = replace(fx["projection"], questions=questions, response_slots=tuple(
        replace(slot, question_binding=bindings[slot.question_binding.native_question_ref])
        for slot in fx["projection"].response_slots
    ))
    native = build_validated_source_backed_c11_release_from_stream(fx["stream"], projection)
    public = compact._compact_public_objects(native, physical_binding=lambda: None, projection_binding="selector-v1-test")
    universe, = projection.universes
    eager = _build_release_index(native, universe.ref)
    selected = _build_release_index(replace(native, public_objects=public), universe.ref)
    assert _SELECTOR_CONTRACT_VERSION == 1
    fields = (
        "ref", "native_question_ref", "canonical_question_ref_if_authorized", "component_or_subitem_ref",
    )
    for key in eager.respondents:
        expected = tuple(eager.events_by_respondent[key])
        assert all(isinstance(event, RespondentEvent) for event in selected.events_by_respondent[key])
        targets = {exact_ref(getattr(event, field)) for event in expected for field in fields[1:]}
        for target in targets:
            for native_only in (False, True):
                for include_component in (False, True):
                    for states in (None, frozenset(), frozenset({"SUBSTANTIVE_RESPONSE"})):
                        flags = dict(native_only=native_only, include_component=include_component, states=states)
                        a = tuple(_select_respondent_events(eager, key, target, **flags))
                        b = tuple(_select_respondent_events(selected, key, target, **flags))
                        assert [event.ref for event in a] == [event.ref for event in b]
                        for full, event in zip(a, b):
                            for field in fields:
                                exported = getattr(event, field)
                                original = exact_ref(getattr(full, field)).as_dict()
                                exported.__dict__.update(object_id="urn:test:forged", content_hash="f" * 64)
                                assert getattr(event, field).as_dict() == original
                                exported.__dict__.update(original)
                            assert event.raw_response_value == full.raw_response_value
                            assert event.canonical_response_value_if_authorized == full.canonical_response_value_if_authorized
                            assert event.multiplicity_order_rank_fields == full.multiplicity_order_rank_fields
                            assert event.response_event_id_or_deterministic_index == full.response_event_id_or_deterministic_index
                        assert [event.ref for event in _select_respondent_events(selected, key, target, **flags)] == [event.ref for event in a]
    with pytest.raises(KeyError):
        tuple(_select_respondent_events(selected, "absent-respondent", next(iter(targets))))


def test_compressed_event_bodies_exact_bounded_chunks_and_old_cache_read(tmp_path, monkeypatch):
    from rawlsing_next import _pre553_c11_execution_view as compact
    from rawlsing_next.pre553_empirical_objects import canonical_json

    fx = _fixture()
    expected = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    directory = _cache(monkeypatch, tmp_path)
    observed = _execute(fx)
    public = observed.c11_release.public_objects
    assert isinstance(public, compact._CompactPublicObjects)
    assert isinstance(public.lane.bodies, compact._CompressedBodies)
    expected_events = {
        obj.ref.key: obj for obj in expected.public_objects if obj.schema_id == "RespondentEvent"
    }
    assert len(public.lane.selectors) == len(expected_events)
    chunk_rows = []
    for row, selector in enumerate(public.lane.selectors):
        rebuilt = public.lane.materialize(row)
        assert rebuilt.ref == selector.ref
        assert rebuilt.as_dict() == expected_events[selector.ref.key].as_dict()
        body = public.lane.bodies.body_bytes(row)
        assert body == canonical_json(rebuilt.semantic_projection()).encode("utf-8")
    for compressed, raw_size, start, count in public.lane.bodies.chunks:
        assert count <= compact._EVENT_BODY_CHUNK_EVENTS
        assert raw_size > 0
        chunk_rows.append((start, count))
    assert sum(count for _, count in chunk_rows) == len(public.lane.selectors)
    path, = directory.glob("c11-events-*.parquet")
    schema = pq.read_schema(path)
    key = schema.metadata[compact._CACHE_METADATA_KEY].decode("ascii")
    old_rows = pq.read_table(path).to_pylist()
    old_style = pa.table({
        compact._EVENT_BODY_COLUMN: pa.array(
            [row[compact._EVENT_BODY_COLUMN] for row in old_rows], type=pa.binary(),
        ),
    }).replace_schema_metadata(schema.metadata)
    pq.write_table(old_style, path, compression="zstd", compression_level=3)
    reread = compact._read_bodies(path, key, public.lane.selectors)
    assert isinstance(reread, compact._CompressedBodies)
    for row in range(len(public.lane.selectors)):
        assert reread.body_bytes(row) == public.lane.bodies.body_bytes(row)


def test_compressed_bodies_exact_across_routed_state_topology_and_weight_shapes(tmp_path, monkeypatch):
    from rawlsing_next.pre553_empirical_objects import RespondentEvent, canonical_json, exact_ref
    from rawlsing_next.tests import pre553_query_frontier_fixtures as frontier
    from rawlsing_next.tests.pre553_query_frontier_fixtures import (
        raw_weighted_divergence_fixture,
        special_state_fixture,
        topology_fixture,
    )
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    ids = [f"W{i:04d}" for i in range(70)]
    rows = [{
        "id": rid,
        "responses": {
            "A": i & 1,
            "B": (i >> 1) & 1,
            "C": (i >> 2) & 1,
            "K": (i & 1) ^ ((i >> 1) & 1) ^ ((i >> 2) & 1),
            "X": i & 1,
            "Y": (i >> 1) & 1,
            "Z": (i & 1) ^ ((i >> 1) & 1),
            "U": (i >> 2) & 1,
        },
        "coords": {"G": "A" if i % 5 else "B", "H": i & 1},
    } for i, rid in enumerate(ids)]
    weighted = _build_source(
        "shape-weighted-routed",
        rows,
        risk_sets={
            "R": {question: set(ids) for question in ("A", "B", "C", "K", "X", "Y", "Z", "U")},
            "S": {
                question: {rid for index, rid in enumerate(ids) if index % 2 == 0}
                for question in ("A", "B", "C", "K", "X", "Y", "Z", "U")
            },
        },
        weights={rid: ("WEIGHT_VALID_AUTHORIZED", str(1 + (index % 4))) for index, rid in enumerate(ids)},
    )
    original_universe = frontier.EmpiricalUniverse

    def country_universe(*args, **kwargs):
        kwargs.update(country_geography="ZZ", sampling_geography="ZZ-NATIONAL")
        return original_universe(*args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(frontier, "EmpiricalUniverse", country_universe)
        country = frontier._build_event_source(
            "shape-country-zz",
            [
                {"id": "C1", "events": {"Q": ({"value": "1"},)}},
                {"id": "C2", "events": {"Q": ({"value": "0"},)}},
            ],
            {"Q": "SCALAR_SINGULAR"},
        )
    sources = (
        ("weighted-routed-kway", weighted),
        ("typed-states-and-routing", special_state_fixture()[0]),
        ("ordered-ranked-repeated", topology_fixture()[0]),
        ("raw-weighted-divergence", raw_weighted_divergence_fixture()[0]),
        ("country-zz-scalar", country),
    )
    directory = _cache(monkeypatch, tmp_path)

    def events_of(objects):
        return tuple(obj for obj in objects if isinstance(obj, RespondentEvent))

    def check(public, expected):
        expected_events = events_of(expected)
        assert isinstance(public, compact._CompactPublicObjects)
        assert isinstance(public.lane.bodies, compact._CompressedBodies)
        assert len(public.lane.selectors) == len(expected_events)
        assert sum(count for _, _, _, count in public.lane.bodies.chunks) == len(expected_events)
        assert tuple(start for _, _, start, _ in public.lane.bodies.chunks) == tuple(
            range(0, len(expected_events), compact._EVENT_BODY_CHUNK_EVENTS)
        )
        assert all(
            0 < count <= compact._EVENT_BODY_CHUNK_EVENTS
            for _, _, _, count in public.lane.bodies.chunks
        )
        assert tuple(obj.as_dict() for obj in public.non_events) == tuple(
            obj.as_dict() for obj in expected if not isinstance(obj, RespondentEvent)
        )
        for row, event in enumerate(expected_events):
            rebuilt = public.lane.materialize(row)
            assert rebuilt.ref == event.ref
            assert rebuilt.as_dict() == event.as_dict()
            assert public.lane.bodies.body_bytes(row) == canonical_json(
                rebuilt.semantic_projection()
            ).encode("utf-8")
        for key, group in public.by_respondent.items():
            expected_group = tuple(
                event for event in expected_events
                if (exact_ref(event.empirical_universe_ref), exact_ref(event.scoped_respondent_ref).key) == key
            )
            assert tuple(event.ref for event in group) == tuple(event.ref for event in expected_group)

    for name, source in sources:
        release = source["repo"].resolve_release_exact(source["release_ref"])
        def binding(name=name):
            return f"shape-binding-{name}"

        first = compact._compact_public_objects(
            release, physical_binding=binding, projection_binding=f"shape-{name}",
        )
        check(first, release.public_objects)
        with monkeypatch.context() as patch:
            def unexpected(_value):
                pytest.fail("warm cross-shape cache reserialized exact event bodies")

            patch.setattr(compact, "canonical_json", unexpected)
            second = compact._compact_public_objects(
                release, physical_binding=binding, projection_binding=f"shape-{name}",
            )
        check(second, release.public_objects)
        assert tuple(
            (compressed, raw_size, start, count)
            for compressed, raw_size, start, count in second.lane.bodies.chunks
        ) == tuple(first.lane.bodies.chunks)
        if len(events_of(release.public_objects)) > compact._EVENT_BODY_CHUNK_EVENTS:
            assert len(first.lane.bodies.chunks) > 1

    for label, missing_weight in (("physical-routed-weight", False), ("physical-missing-weight", True)):
        fx = _fixture(missing_weight=missing_weight)
        expected = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
        observed = _execute(fx)
        check(observed.c11_release.public_objects, expected.public_objects)
    assert len(tuple(directory.glob("c11-events-*.parquet"))) == len(sources) + 2
