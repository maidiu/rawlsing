"""Focused W03/W04 cold-path, compact-lane and topology tests.

Heavy 100k paired measurement is owned by the benchmark lane; these tests are
small, exact and deterministic.
"""
from __future__ import annotations

import pytest

from rawlsing_next._pre553_c11_execution_view import _CompactPublicObjects
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    SourceBackedC11FacadeError,
    build_cold_source_backed_c11_release,
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture as _route_fixture
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture as _facade_fixture


def _stream(fx):
    return ExactPhysicalCellStream(
        fx["source_sha"], fx["incidence"].row_count, lambda: iter(fx["cells"]))


def _compare_eager_cold(stream, projection):
    eager = build_validated_source_backed_c11_release_from_stream(stream, projection)
    cold = build_cold_source_backed_c11_release(stream, projection)
    assert cold.release_ref == eager.release_ref
    assert cold.replay_manifest.ref == eager.replay_manifest.ref
    assert cold.source_release_manifest_hash == eager.source_release_manifest_hash
    assert tuple(x.ref for x in cold.public_objects) == tuple(
        x.ref for x in eager.public_objects)
    assert tuple(x.ref for x in cold.internal_records) == tuple(
        x.ref for x in eager.internal_records)
    assert cold.m01_m18_coverage == eager.m01_m18_coverage
    return eager, cold


def test_cold_release_is_exact_and_compact_for_full_facade_fixture():
    fx = _facade_fixture()
    eager, cold = _compare_eager_cold(_stream(fx), fx["projection"])
    assert isinstance(cold.public_objects, _CompactPublicObjects)
    assert not any(isinstance(obj, RespondentEvent) for obj in cold.public_objects.non_events)
    assert any(isinstance(entry, int) for entry in cold.public_objects.entries)
    assert len(cold.public_objects) == len(eager.public_objects)
    # Materialization is exact, including zero-occurrence and repeated/ranked lanes.
    for left, right in zip(eager.public_objects, cold.public_objects):
        assert left.as_dict() == right.as_dict()
    event_states = {
        obj.response_state for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }
    assert {"SUBSTANTIVE_RESPONSE", "MISSING"} <= event_states
    assert "ORDERED_SEQUENCE" in {
        obj.multiplicity_order_rank_fields["kind"]
        for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }
    assert "REPEATED_EVENT" in {
        obj.multiplicity_order_rank_fields["kind"]
        for obj in eager.public_objects
        if isinstance(obj, RespondentEvent)
    }


def test_cold_repository_is_used_without_disk_cache_and_matches_eager():
    fx = _facade_fixture()
    stream = _stream(fx)
    eager = build_validated_source_backed_c11_release_from_stream(stream, fx["projection"])
    repository, cold = build_source_backed_c11_repository(stream, fx["projection"])
    assert isinstance(cold.public_objects, _CompactPublicObjects)
    assert cold.release_ref == eager.release_ref
    assert repository.release_refs == (eager.release_ref,)
    assert repository.resolve_release_exact(eager.release_ref).release_ref == eager.release_ref


@pytest.mark.parametrize(
    "kwargs",
    ({}, {"missing_weight": True}, {"valid_empty": True}),
    ids=("routed-ordered-repeated", "missing-optional-weight", "valid-empty"),
)
def test_cold_path_matches_eager_route_b_fixture(kwargs):
    fx = _route_fixture(**kwargs)
    _compare_eager_cold(fx["stream"], fx["projection"])


def test_cold_path_refuses_duplicate_physical_row_slot():
    fx = _facade_fixture()
    cells = tuple(fx["cells"]) + (fx["cells"][0],)
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells))
    with pytest.raises(SourceBackedC11FacadeError, match="duplicate physical row/slot"):
        build_cold_source_backed_c11_release(stream, fx["projection"])


def test_cold_path_refuses_incomplete_projected_slot():
    fx = _facade_fixture()
    cells = tuple(cell for cell in fx["cells"] if not (
        cell.variable_ordinal == 1 and cell.row_ordinal == 3))
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells))
    with pytest.raises(SourceBackedC11FacadeError, match="projected slot incomplete"):
        build_cold_source_backed_c11_release(stream, fx["projection"])


def test_cold_path_refuses_wrong_source_sha():
    fx = _facade_fixture()
    stream = ExactPhysicalCellStream("f" * 64, 3, lambda: iter(fx["cells"]))
    with pytest.raises(SourceBackedC11FacadeError, match="source SHA mismatch"):
        build_cold_source_backed_c11_release(stream, fx["projection"])
