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


def _multi_i03_source(tag):
    """Actual I02 accepted same-respondent 2-occurrence, repeated-value source."""
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import _authority
    from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
    from rawlsing_next.pre553_empirical_objects import RoutingEligibilityFact
    old = _candidate(tag, event_kind="UNORDERED_MULTISELECT_SET")
    routing_auth = _authority(
        tag + "-routing", "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    previous = old.routing_eligibility_facts_or_exact_rules[0]
    routing = RoutingEligibilityFact(
        typed_state=previous.typed_state,
        authority_snapshot_refs=(routing_auth.authority_ref,),
        dependency_refs=previous.dependency_refs,
        producer_replay_locator_or_reference_root=previous.producer_replay_locator_or_reference_root,
        **dict(previous.semantic_fields),
    )
    counts = dict(old.source_release_manifest.declared_record_counts_by_logical_family)
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        old.source_release_manifest,
        declared_authority_snapshot_refs=(
            *old.source_release_manifest.declared_authority_snapshot_refs,
            routing_auth.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        old, source_release_manifest=manifest,
        routing_eligibility_facts_or_exact_rules=(routing,),
        authority_snapshots=(*old.authority_snapshots, routing_auth),
        candidate_replay_manifest=None,
    )
    candidate = replace(
        candidate, candidate_replay_manifest=build_candidate_replay_manifest(
            candidate,
            replay_protocol_authority_ref=old.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=old.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version=old.candidate_replay_manifest.replay_protocol_version,
        ),
    )
    repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    assert result.accepted, result.errors
    return {
        "repo": repo, "release_ref": result.release_ref,
        "universe": candidate.empirical_universes[0],
        "respondents": {"R1": candidate.respondent_identities[0]},
        "qrefs": {"Y": candidate.question_variable_bindings[0].native_question_ref},
        "risk_refs": {"R": candidate.routing_eligibility_facts_or_exact_rules[0].risk_set_ref},
        "source_auth": candidate.authority_snapshots[0],
        "authorities": candidate.authority_snapshots,
    }


def test_h26_two_same_respondent_occurrences_actual_native_i03_fact_replay():
    source = _multi_i03_source("s2a-h26-real-multiple")
    qa = _query_authority("s2a-h26-real-multiple")
    pred = _branch_predicate(source, qa, tag="s2a-h26-real-multiple")
    initial = _query(source, qa, pred, ("Y",), tag="s2a-h26-real-multiple")
    shape = dict(initial.target_arity_and_topology)
    component = dict(shape["components"][0])
    component["topology"] = "UNORDERED_MULTISELECT_SET"
    component["domain"] = [["SAME-VALUE"]]
    shape["components"] = [component]
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec
    query = EmpiricalQuerySpec(
        typed_state=initial.typed_state,
        authority_snapshot_refs=initial.authority_snapshot_refs,
        dependency_refs=initial.dependency_refs,
        producer_replay_locator_or_reference_root=initial.producer_replay_locator_or_reference_root,
        **{**dict(initial.semantic_fields), "target_arity_and_topology": shape},
    )
    original = _run(source, qa, pred, query)
    assert original.facts[0].typed_state == "SUPPORTED", dict(original.facts[0].semantic_fields)
    assert original.facts[0].raw_denominator_support == 1

    witness, root = _trusted(source)
    _install_i03(source, witness, root)
    assert _run(source, qa, pred, query) == original
    respondent = source["respondents"]["R1"].ref.key
    key = (respondent, "native", source["qrefs"]["Y"].key)
    original_postings = _canonical_postings(source, witness)
    assert len(original_postings[key]) == 2
    corrupted = dict(original_postings)
    corrupted[key] = original_postings[key][:-1]  # same-value second occurrence disappears
    _install_i03(source, witness, root, postings=corrupted)
    denied = _run(source, qa, pred, query)
    assert denied.facts[0].typed_state == "INTEGRITY_FAILURE"
    assert denied != original
    _install_i03(source, witness, root)
    assert _run(source, qa, pred, query) == original


def test_h27_real_i02_authorized_canonical_and_component_binding_omission():
    """Do not count a fabricated alias as qualified: build it through I02."""
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import (
        _authority, _ref,
    )
    from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding
    from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    old = _candidate("s2a-authorized-alias", event_kind="UNORDERED_MULTISELECT_SET")
    mapping = _authority(
        "s2a-canonical", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    canonical = _ref("QUESTION_CANONICAL", "s2a-Q")
    component = _ref("QUESTION_COMPONENT", "s2a-Q-component")
    original_binding = old.question_variable_bindings[0]
    binding = QuestionVariableBinding(
        empirical_universe_ref=original_binding.empirical_universe_ref,
        native_question_ref=original_binding.native_question_ref,
        instrument_question_version=original_binding.instrument_question_version,
        canonical_question_ref_or_typed_absence=canonical,
        component_subitem_ref_or_typed_absence=component,
        semantic_authority_ref=mapping.authority_ref,
        topology_authority_ref=original_binding.topology_authority_ref,
    )
    new_events = []
    for event in old.respondent_events:
        fields = dict(event.semantic_fields)
        fields.update(
            canonical_question_ref_if_authorized=canonical,
            component_or_subitem_ref=component,
            value_transform_authority_ref=mapping.authority_ref,
        )
        new_events.append(RespondentEvent(
            typed_state=event.typed_state,
            authority_snapshot_refs=(*event.authority_snapshot_refs, mapping.authority_ref),
            dependency_refs=event.dependency_refs,
            producer_replay_locator_or_reference_root=event.producer_replay_locator_or_reference_root,
            **fields,
        ))
    counts = dict(old.source_release_manifest.declared_record_counts_by_logical_family)
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        old.source_release_manifest,
        declared_authority_snapshot_refs=(
            *old.source_release_manifest.declared_authority_snapshot_refs,
            mapping.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        old, source_release_manifest=manifest,
        question_variable_bindings=(binding,),
        respondent_events=tuple(new_events),
        authority_snapshots=(*old.authority_snapshots, mapping),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=old.candidate_replay_manifest.replay_protocol_authority_ref,
        deterministic_tie_order_rules_ref=old.candidate_replay_manifest.deterministic_tie_order_rules_ref,
        replay_protocol_version=old.candidate_replay_manifest.replay_protocol_version,
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    repo = C11Repository()
    accepted = ingest_c11_source_release(candidate, repo)
    assert accepted.accepted, accepted.errors
    release = repo.resolve_release_exact(accepted.release_ref)
    universe = candidate.empirical_universes[0].ref
    respondent = candidate.respondent_identities[0].ref.key
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    normal = certified_i03_events(release, universe, witness=witness,
                                 independently_held_root=witness.root)
    assert len(list(normal[respondent].select(canonical))) == 2
    assert len(list(normal[respondent].select(component, include_component=True))) == 2
    assert len(list(normal[respondent].select(component, native_only=True,
                                               include_component=True))) == 0
    from rawlsing_next._pre553_verified_semantic_range import _bindings
    _, postings = _bindings(release, universe)
    for kind, target in (("canonical", canonical), ("component", component)):
        key = (respondent, kind, target.key)
        poisoned = dict(postings)
        poisoned[key] = poisoned[key][:-1]
        reader = certified_i03_events(
            release, universe, witness=witness, independently_held_root=witness.root,
            candidate_postings=poisoned,
        )
        with pytest.raises(SemanticRangeIntegrityError):
            list(reader[respondent].select(target, include_component=True))
