"""Independent SOURCEFREE courts; imports the exact candidate checkout via PYTHONPATH."""
from dataclasses import FrozenInstanceError, replace, fields
from types import MappingProxyType, SimpleNamespace
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from unittest.mock import patch
import builtins
import json
import os

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from rawlsing_next import _pre553_c11_execution_view as view
from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import RespondentEvent, ExactRef, canonical_json
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_source_backed_c11_repository, build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute


def compact(release, binding=None, projection="independent-projection"):
    public = view._compact_public_objects(release, physical_binding=lambda: binding,
                                          projection_binding=projection)
    assert public is not None
    return replace(release, public_objects=public)


def profile():
    packet = Path(__file__).parent
    inputs = packet / "inputs" if (packet / "inputs").is_dir() else packet.parent / "inputs"
    spec = spec_from_file_location("independent_pinned_profile", inputs / "profile_oct28.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_pinned_query_cases_compact_vs_native_and_selector_fields(monkeypatch):
    monkeypatch.delenv(view._CACHE_ENV, raising=False)
    count = 0
    for label, operations in profile().query_cases().items():
        for operation in operations:
            original = operation["repository"]
            native_result = execute_empirical_query(**operation)
            releases = [original.resolve_release_exact(ref) for ref in original.release_refs]
            converted = [compact(release) for release in releases]
            repository = C11Repository(converted)
            with patch.object(view._EventLane, "materialize", side_effect=AssertionError("hot native realization")):
                result = execute_empirical_query(**{**operation, "repository": repository})
            assert profile_material(result) == profile_material(native_result), label
            for native, candidate in zip(releases, converted):
                universes = [obj.ref for obj in native.public_objects if obj.schema_id == "EmpiricalUniverse"]
                for universe in universes:
                    a = _build_release_index(native, universe)
                    b = _build_release_index(candidate, universe)
                    assert a.respondents == b.respondents
                    assert a.coordinates_by_respondent == b.coordinates_by_respondent
                    assert a.routing_by_respondent == b.routing_by_respondent
                    assert a.weights_by_respondent == b.weights_by_respondent
                    for respondent in a.respondents:
                        events = tuple(a.events_by_respondent[respondent])
                        assert tuple(b.events_by_respondent[respondent]) == events
                        targets = {ExactRef("QUESTION_NATIVE", "absent", "f" * 64)}
                        for event in events:
                            for field in ("native_question_ref", "canonical_question_ref_if_authorized", "component_or_subitem_ref"):
                                value = getattr(event, field)
                                if value is not None:
                                    targets.add(value if isinstance(value, ExactRef) else ExactRef(**value))
                        for target in targets:
                            for native_only in (False, True):
                                for include_component in (False, True):
                                    for states in (None, frozenset(), frozenset({"SUBSTANTIVE_RESPONSE"}), frozenset({"MISSING", "DK", "REFUSAL", "NOT_ASKED"})):
                                        flags = dict(native_only=native_only, include_component=include_component, states=states)
                                        x = tuple(_select_respondent_events(a, respondent, target, **flags))
                                        y = tuple(_select_respondent_events(b, respondent, target, **flags))
                                        assert [e.ref for e in x] == [e.ref for e in y], (label, flags)
                                        assert all(isinstance(e, RespondentEvent) for e in x)
                                        for full, selected in zip(x, y):
                                            for f in (SimpleNamespace(name=name) for name in ('ref', 'typed_state', 'native_question_ref', 'canonical_question_ref_if_authorized', 'component_or_subitem_ref', 'authority_snapshot_refs', 'raw_response_value', 'canonical_response_value_if_authorized', 'multiplicity_order_rank_fields', 'response_event_id_or_deterministic_index')):
                                                expected = getattr(full, f.name)
                                                if f.name.endswith("question_ref") or f.name in {"canonical_question_ref_if_authorized", "component_or_subitem_ref"}:
                                                    if expected is not None and not isinstance(expected, ExactRef):
                                                        expected = ExactRef(**expected)
                                                assert canonical_json(getattr(selected, f.name)) == canonical_json(expected), (label, f.name)
            count += 1
    print("all pinned cases executed:", count)


def profile_material(result):
    return (result.query_ref, result.source_scope_mode,
            tuple(f.as_dict() for f in result.facts))


def test_compact_same_release_and_foreign_index_faults_rebuild(monkeypatch):
    monkeypatch.delenv(view._CACHE_ENV, raising=False)
    fx = _fixture()
    route = _execute(fx)
    executor = route.repository_binding.executor
    repo = executor.repository
    key, = repo._i03_release_indices
    original = repo._i03_release_indices[key]
    foreign = _execute(_fixture(missing_weight=True)).repository_binding.executor.repository
    foreign_index = next(iter(foreign._i03_release_indices.values()))
    corruptions = [replace(original, events_by_respondent=MappingProxyType({k: () for k in original.respondents})), foreign_index]
    request = fx["requests"][0]
    for bad in corruptions:
        repo._i03_release_indices[key] = bad
        result = executor.execute_i03(query_ref=request.query_ref, predicate_ref=request.predicate_ref)
        assert profile_material(result) == profile_material(route.i03_results[0])
        assert repo._i03_release_indices[key] is not bad


def test_selector_descendants_and_refs_immutable(monkeypatch):
    monkeypatch.delenv(view._CACHE_ENV, raising=False)
    fx = _fixture()
    _, release = build_source_backed_c11_repository(fx["stream"], fx["projection"])
    event = release.public_objects.lane.selectors[0]
    with pytest.raises((FrozenInstanceError, AttributeError)):
        event.raw_response_value = "forged"
    with pytest.raises((FrozenInstanceError, AttributeError)):
        event.ref.content_hash = "f" * 64
    with pytest.raises(TypeError):
        event.multiplicity_order_rank_fields["index"] = 100
    assert isinstance(event.authority_snapshot_refs, tuple)


def test_invalid_source_projection_precedes_cache(monkeypatch, tmp_path):
    fx = _fixture()
    monkeypatch.setenv(view._CACHE_ENV, str(tmp_path / "cache"))
    with patch.object(view, "_read_bodies", side_effect=AssertionError("invalid source reached cache")):
        with pytest.raises(ValueError):
            build_source_backed_c11_repository(replace(fx["stream"], source_sha256="f" * 64), fx["projection"])
    assert not (tmp_path / "cache").exists()


def test_arrow_unavailable_uses_native_compatibility(monkeypatch):
    fx = _fixture()
    monkeypatch.delenv(view._CACHE_ENV, raising=False)
    original = builtins.__import__
    def unavailable(name, *args, **kwargs):
        if name == "pyarrow":
            raise ModuleNotFoundError("test unsupported Arrow", name="pyarrow")
        return original(name, *args, **kwargs)
    with patch.object(builtins, "__import__", unavailable):
        observed = _execute(fx)
    expected = _execute(fx)
    assert isinstance(observed.c11_release.public_objects, tuple)
    assert profile_material(observed.i03_results[0]) == profile_material(expected.i03_results[0])


def test_cache_faults_slots_and_binding_invalidation(monkeypatch, tmp_path):
    fx = _fixture()
    release = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    root = tmp_path / "cache"
    monkeypatch.setenv(view._CACHE_ENV, str(root))
    binding = {"decoder_metadata": "a" * 64, "current_authorities": ["current"]}
    sealed = compact(release, binding)
    path, = root.glob("*.parquet")
    golden = path.read_bytes()
    assert root.stat().st_mode & 0o777 == 0o700
    assert path.stat().st_mode & 0o777 == 0o600
    for variant in ("metadata", "content", "truncated", "symlink"):
        if variant == "metadata":
            table = pq.read_table(path).replace_schema_metadata({view._CACHE_METADATA_KEY: b"foreign-key"})
            pq.write_table(table, path)
        elif variant == "content":
            table = pq.read_table(path)
            bodies = table.column(0).to_pylist()
            payload = json.loads(bodies[0]); payload["semantic_fields"]["raw_response_value"] = "forged"
            bodies[0] = canonical_json(payload).encode()
            table = pa.table({view._EVENT_BODY_COLUMN: pa.array(bodies, type=pa.binary())}).replace_schema_metadata(table.schema.metadata)
            pq.write_table(table, path)
        elif variant == "truncated":
            path.write_bytes(b"torn")
        else:
            outside = tmp_path / "outside"
            outside.write_bytes(b"outside-must-not-change")
            path.unlink(); path.symlink_to(outside)
        restored = compact(release, binding)
        assert [x.as_dict() for x in restored.public_objects] == [x.as_dict() for x in release.public_objects]
        assert path.read_bytes() == golden
        if variant == "symlink":
            assert outside.read_bytes() == b"outside-must-not-change"
            assert not path.is_symlink()
    for altered, projection in (({**binding, "decoder_metadata": "b" * 64}, "independent-projection"),
                                ({**binding, "current_authorities": ["new-current"]}, "independent-projection"),
                                (binding, "new-projection")):
        reads = []
        original = view._read_bodies
        def invalidated(*args):
            result = original(*args)
            reads.append(result is None)
            return result
        with patch.object(view, "_read_bodies", invalidated):
            compact(release, altered, projection)
        assert reads == [True]
    # Exercise all direct-mapped slots, including real collisions and a later miss.
    slots = {}; collisions = 0
    original_read = view._read_bodies
    outcomes = []
    def observed(path, key, selectors):
        result = original_read(path, key, selectors)
        outcomes.append((path.name, key, result is not None))
        return result
    with patch.object(view, "_read_bodies", observed):
        for n in range(96):
            compact(release, {**binding, "variant": n})
            slot, key, hit = outcomes[-1]
            if slot in slots and slots[slot] != key:
                collisions += 1
                assert not hit
            slots[slot] = key
    assert len(slots) == 16 and collisions > 0
    assert len(tuple(root.glob("c11-events-*.parquet"))) == 16
    assert not tuple(root.glob(".c11-events-*"))
    print("slots=16 collisions=", collisions)


@pytest.mark.parametrize("mode", ["relative", "public", "symlink"])
def test_unauthorized_cache_roots_ignored(monkeypatch, tmp_path, mode):
    root = tmp_path / "cache"
    root.mkdir(mode=0o700)
    if mode == "relative":
        configured = "relative-disallowed"
    elif mode == "public":
        root.chmod(0o755); configured = str(root)
    else:
        link = tmp_path / "link"; link.symlink_to(root, target_is_directory=True); configured = str(link)
    monkeypatch.setenv(view._CACHE_ENV, configured)
    assert view._cache_directory() is None
    assert not tuple(root.iterdir())
