"""S2-A hostile sourcefree I02→verified selector→real I03 tests.

The fixtures invoke the production I02 ingest and production execute_empirical_query,
not a made-up count/route engine. These are NOT saved-process/native original35 tests.
"""
from dataclasses import replace
from types import MappingProxyType
import tracemalloc

import pytest

from rawlsing_next._pre553_query_predicate import _build_release_index, _select_respondent_events
from rawlsing_next.pre553_empirical_query import _i03_index_attestation
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next._pre553_verified_semantic_range import (
    I02SemanticRangeWitness, SemanticRangeIntegrityError, certified_i03_events,
)
from rawlsing_next.tests.test_pre553_c11_repository_ingest import _candidate
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _query_authority, _branch_predicate, _predicate, _query, _run,
    _cell_map, _registry,
)


def _release(source):
    return source["repo"].resolve_release_exact(source["release_ref"])


def _trusted(source):
    release = _release(source)
    universe = source["universe"].ref
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    return witness, witness.root


def _install_i03(source, witness, root, *, postings=None):
    """Test-only I03 cache insertion under its exact existing attestation law."""
    release = _release(source)
    universe = source["universe"].ref
    selected = certified_i03_events(
        release, universe, witness=witness, independently_held_root=root,
        candidate_postings=postings,
    )
    index = replace(
        _build_release_index(release, universe),
        events_by_respondent=selected,
    )
    repo = source["repo"]
    key = (release.release_ref, universe)
    with repo._i03_index_lock:
        repo._i03_release_indices[key] = index
        repo._i03_index_attestations[key] = _i03_index_attestation(index)
    return selected


def test_h26_actual_i03_omitted_native_event_refuses_and_restores_full_fact():
    source = _build_source("s2a-h26", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa = _query_authority("s2a-h26")
    pred = _branch_predicate(source, qa, tag="s2a-h26")
    query = _query(source, qa, pred, ("Y",), tag="s2a-h26")
    before = _run(source, qa, pred, query)
    assert before.facts[0].typed_state == "SUPPORTED"
    assert _cell_map(before.facts[0])["1"]["raw_numerator_support"] == 2

    witness, root = _trusted(source)
    unmodified = _install_i03(source, witness, root)
    normal = _run(source, qa, pred, query)
    assert normal == before  # whole native fact/replay/provenance, not just count

    respondent_key = source["respondents"]["R2"].ref.key
    selector_key = (respondent_key, "native", source["qrefs"]["Y"].key)
    base = dict({key: value for key, value in
                 _canonical_postings(source, witness).items()})
    assert len(base[selector_key]) == 1
    base[selector_key] = ()  # all canonical native objects remain intact
    poisoned = _install_i03(source, witness, root, postings=MappingProxyType(base))
    assert len(poisoned[respondent_key].all_events) == 1
    refused = _run(source, qa, pred, query)
    assert refused.facts[0].typed_state == "INTEGRITY_FAILURE"
    assert refused != before

    _install_i03(source, witness, root)
    restored = _run(source, qa, pred, query)
    assert restored == before
    assert list(unmodified[respondent_key].select(source["qrefs"]["Y"]))


def _canonical_postings(source, witness):
    # Recompute fixture secondary postings ONLY for attack setup. The proof
    # witness is already frozen from the independent I02 source.
    from rawlsing_next._pre553_verified_semantic_range import _bindings
    _, postings = _bindings(_release(source), witness.universe_ref)
    return postings


def test_h26_same_respondent_duplicate_value_second_occurrence_survives():
    candidate = _candidate("s2a-multiple", event_kind="UNORDERED_MULTISELECT_SET")
    repository = C11Repository()
    accepted = ingest_c11_source_release(candidate, repository)
    assert accepted.accepted, accepted.errors
    release = repository.resolve_release_exact(accepted.release_ref)
    universe = candidate.empirical_universes[0].ref
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    rows = certified_i03_events(release, universe, witness=witness,
                                independently_held_root=witness.root)
    respondent = candidate.respondent_identities[0].ref.key
    target = candidate.question_variable_bindings[0].native_question_ref
    baseline = list(rows[respondent].select(target))
    assert len(baseline) == 2
    assert baseline[0].ref != baseline[1].ref
    assert baseline[0].raw_response_value == baseline[1].raw_response_value

    key = (respondent, "native", target.key)
    corrupted = dict(_canonical_postings(
        {"repo": repository, "release_ref": accepted.release_ref}, witness
    ))
    corrupted[key] = corrupted[key][:-1]
    poisoned = certified_i03_events(release, universe, witness=witness,
                                    independently_held_root=witness.root,
                                    candidate_postings=corrupted)
    with pytest.raises(SemanticRangeIntegrityError):
        list(poisoned[respondent].select(target))
    assert list(rows[respondent].select(target)) == baseline


def test_h27_authorized_alias_ranges_and_native_only_precedence_at_i03_selector():
    source = _build_source("s2a-alias", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    witness, root = _trusted(source)
    rows = _install_i03(source, witness, root)
    key = source["respondents"]["R1"].ref.key
    native = source["qrefs"]["Y"]
    assert len(list(rows[key].select(native, native_only=True))) == 1
    assert len(list(rows[key].select(native, include_component=True))) == 1
    # An unknown canonical/component selector is *certified empty* against
    # the complete I02 witness, not an accidental alias to a native question.
    from rawlsing_next.tests.test_pre553_empirical_query import _ref
    other = _ref("QUESTION_CANONICAL", "s2a-unissued")
    assert list(rows[key].select(other, include_component=True)) == []
    # A forged "canonical" posting cannot create a valid alias.
    corrupted = dict(_canonical_postings(source, witness))
    corrupted[(key, "canonical", other.key)] = corrupted[(key, "native", native.key)]
    wrong = certified_i03_events(_release(source), source["universe"].ref,
                                 witness=witness, independently_held_root=root,
                                 candidate_postings=corrupted)
    with pytest.raises(SemanticRangeIntegrityError):
        list(wrong[key].select(other))
    assert len(list(wrong[key].select(native, native_only=True))) == 1


def test_h28_empty_event_selection_does_not_override_routing_unknown():
    source = _build_source("s2a-unknown", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {}},
    ], risk_sets={"R": {"Y": {"R1"}}}, nonmember_routing_state="ROUTING_UNKNOWN")
    witness, root = _trusted(source)
    _install_i03(source, witness, root)
    k = source["respondents"]["R2"].ref.key
    assert list(_select_respondent_events(
        _build_release_index(_release(source), source["universe"].ref),
        k, source["qrefs"]["Y"],
    )) == []
    qa = _query_authority("s2a-unknown")
    pred = _branch_predicate(source, qa, tag="s2a-unknown")
    query = _query(source, qa, pred, ("Y",), tag="s2a-unknown")
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state not in ("SUPPORTED", "OBSERVED_ZERO", "NOT_APPLICABLE")


def test_h29_reject_wrong_source_release_universe_root_and_keyspace_tamper():
    a = _build_source("s2a-A", [{"id": "R1", "responses": {"Y": 1}}])
    b = _build_source("s2a-B", [{"id": "R1", "responses": {"Y": 1}}])
    witness, root = _trusted(a)
    with pytest.raises(SemanticRangeIntegrityError):
        certified_i03_events(_release(b), b["universe"].ref, witness=witness,
                             independently_held_root=root)
    with pytest.raises(SemanticRangeIntegrityError):
        certified_i03_events(_release(a), a["universe"].ref, witness=witness,
                             independently_held_root="f" * 64)
    bad_witness = replace(witness, range_digests=MappingProxyType({}))
    with pytest.raises(SemanticRangeIntegrityError):
        certified_i03_events(_release(a), a["universe"].ref, witness=bad_witness,
                             independently_held_root=root)


def test_h30_pages_are_bounded_and_no_inventory_method_exists():
    source = _build_source("s2a-bounded", [
        {"id": f"R{i}", "responses": {"Y": i % 2}} for i in range(64)
    ])
    witness, root = _trusted(source)
    tracemalloc.start()
    try:
        rows = certified_i03_events(_release(source), source["universe"].ref,
                                   witness=witness, independently_held_root=root)
        all_pages = 0
        for events in rows.values():
            for page in events.iter_pages(max_page_events=7):
                assert len(page) <= 7
                all_pages += len(page)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert all_pages == 64
    assert not hasattr(rows, "inventory_refs")
    assert peak < 64 * 1024 * 1024  # narrow pilot only, not 100k/6GiB S2-C
