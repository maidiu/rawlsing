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
    assert len(list(rows[key].select(native, states=frozenset()))) == 0
    assert len(list(rows[key].select(native, states=frozenset({"SUBSTANTIVE_RESPONSE"})))) == 1
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
    selected = _install_i03(source, witness, root)
    k = source["respondents"]["R2"].ref.key
    # EMPTY_CERTIFIED for *events* remains distinct from ROUTING_UNKNOWN.
    assert list(selected[k].select(source["qrefs"]["Y"])) == []
    assert list(selected[k].select(source["qrefs"]["Y"], states=frozenset())) == []
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


def _s2a_contradictory_alias_fixture(
    tag: str, *, binding_has_alias: bool = True, event_uses_binding: bool = False,
    conflicting_version_alias: bool = False,
):
    """A genuine I02-accepted sourcefree release with conflicting alias claims.

    I02 currently verifies positive mapping authority and native-question
    membership independently; this sourcefree fixture tests whether the
    S2-A witness can misrepresent an event's *different* canonical alias as
    the alias authorized by the release's QuestionVariableBinding.
    """
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import _authority, _ref
    from rawlsing_next.pre553_c11_integrity import TypedAbsence
    from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    old = _candidate(tag, event_kind="UNORDERED_MULTISELECT_SET")
    mapping = _authority(
        tag + "-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    declared = _ref("QUESTION_CANONICAL", tag + "-DECLARED")
    invented = _ref("QUESTION_CANONICAL", tag + "-INVENTED")
    binding = replace(
        old.question_variable_bindings[0],
        semantic_authority_ref=mapping.authority_ref,
        canonical_question_ref_or_typed_absence=(
            declared if binding_has_alias else TypedAbsence("NOT_APPLICABLE")
        ),
    )
    new_events = []
    for original in old.respondent_events:
        fields = dict(original.semantic_fields)
        fields.update(
            canonical_question_ref_if_authorized=(
                declared if event_uses_binding else invented
            ),
            value_transform_authority_ref=mapping.authority_ref,
        )
        new_events.append(RespondentEvent(
            typed_state=original.typed_state,
            authority_snapshot_refs=(*original.authority_snapshot_refs, mapping.authority_ref),
            dependency_refs=original.dependency_refs,
            producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
            **fields,
        ))
    counts = dict(old.source_release_manifest.declared_record_counts_by_logical_family)
    counts["AuthoritySnapshot"] += 1
    if conflicting_version_alias:
        counts["QuestionVariableBinding"] += 1
    manifest = replace(
        old.source_release_manifest,
        declared_authority_snapshot_refs=(
            *old.source_release_manifest.declared_authority_snapshot_refs,
            mapping.authority_ref,
        ),
        declared_record_counts_by_logical_family=counts,
    )
    candidate = replace(
        old,
        source_release_manifest=manifest,
        question_variable_bindings=(
            (binding, replace(
                binding, instrument_question_version="CONFLICTING_VERSION_2",
                canonical_question_ref_or_typed_absence=invented,
            )) if conflicting_version_alias else (binding,)
        ),
        respondent_events=tuple(new_events),
        authority_snapshots=(*old.authority_snapshots, mapping),
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
    accepted = ingest_c11_source_release(candidate, repo)
    assert accepted.accepted, accepted.errors
    release = repo.resolve_release_exact(accepted.release_ref)
    return release, candidate.empirical_universes[0].ref, declared, invented


def test_h31_i02_accepted_event_alias_disagrees_with_question_binding_must_refuse():
    release, universe, declared, invented = _s2a_contradictory_alias_fixture(
        "s2a-h31-binding-disagreement"
    )
    # Exactly this inconsistency survives native I02: we assert acceptance
    # inside the helper. A source-backed S2-A certificate MUST NOT accept
    # an independently positive yet differently named mapping alias.
    with pytest.raises(SemanticRangeIntegrityError, match="binding|canonical"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h32_i02_accepted_unmapped_event_canonical_alias_must_refuse():
    release, universe, declared, invented = _s2a_contradictory_alias_fixture(
        "s2a-h32-absent-binding", binding_has_alias=False,
    )
    # An ALLOW value-transform authority cannot invent a native→canonical
    # QuestionVariableBinding where the release explicitly says absent.
    with pytest.raises(SemanticRangeIntegrityError, match="binding|canonical"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h33_native_i03_owner_installer_binds_normal_first_consumer_and_refuses_poison():
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    from rawlsing_next._pre553_verified_semantic_range import CertifiedRespondentEvents

    source = _build_source("s2a-h33-owner", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa = _query_authority("s2a-h33-owner")
    pred = _branch_predicate(source, qa, tag="s2a-h33-owner")
    query = _query(source, qa, pred, ("Y",), tag="s2a-h33-owner")
    oracle = _run(source, qa, pred, query)
    release = _release(source)
    universe = source["universe"].ref
    witness, root = _trusted(source)
    # The new production entry point owns cache/attestation publication:
    # callers do NOT hand a self-attested _ReleaseIndex to I03.
    install_sourcefree_i02_certified_i03_range(
        source["repo"], release_ref=release.release_ref,
        universe_ref=universe, witness=witness, independently_held_root=root,
    )
    index = source["repo"]._i03_release_indices[(release.release_ref, universe)]
    respondent = source["respondents"]["R2"].ref.key
    selected = index.events_by_respondent[respondent]
    assert isinstance(selected, CertifiedRespondentEvents)
    assert _run(source, qa, pred, query) == oracle

    # Adverse post-install change of only the derived selector: the I02
    # release and the I03 attestation identities are otherwise unchanged.
    key = (respondent, "native", source["qrefs"]["Y"].key)
    assert len(selected._postings[key]) == 1
    selected._postings[key] = ()
    denied = _run(source, qa, pred, query)
    assert denied.facts[0].typed_state == "INTEGRITY_FAILURE"
    assert denied != oracle

    # Reinstall from the genuine I02 corpus without altering science.
    install_sourcefree_i02_certified_i03_range(
        source["repo"], release_ref=release.release_ref,
        universe_ref=universe, witness=witness, independently_held_root=root,
    )
    assert _run(source, qa, pred, query) == oracle


def test_h34_owner_installer_wrong_root_is_transactionally_nonmutating():
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    source = _build_source("s2a-h34-rollback", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    release = _release(source)
    universe = source["universe"].ref
    witness, root = _trusted(source)
    install_sourcefree_i02_certified_i03_range(
        source["repo"], release_ref=release.release_ref,
        universe_ref=universe, witness=witness, independently_held_root=root,
    )
    k = (release.release_ref, universe)
    prior_index = source["repo"]._i03_release_indices[k]
    prior_attestation = source["repo"]._i03_index_attestations[k]
    with pytest.raises(SemanticRangeIntegrityError):
        install_sourcefree_i02_certified_i03_range(
            source["repo"], release_ref=release.release_ref,
            universe_ref=universe, witness=witness, independently_held_root="0" * 64,
        )
    assert source["repo"]._i03_release_indices[k] is prior_index
    assert source["repo"]._i03_index_attestations[k] is prior_attestation
    qa = _query_authority("s2a-h34-rollback")
    pred = _branch_predicate(source, qa, tag="s2a-h34-rollback")
    query = _query(source, qa, pred, ("Y",), tag="s2a-h34-rollback")
    assert _run(source, qa, pred, query).facts[0].typed_state == "SUPPORTED"


def test_h35_positive_question_binding_alias_through_native_owner_first_reader():
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    release, universe, declared, invented = _s2a_contradictory_alias_fixture(
        "s2a-h35-admitted", event_uses_binding=True,
    )
    repo = C11Repository((release,))
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    install_sourcefree_i02_certified_i03_range(
        repo, release_ref=release.release_ref, universe_ref=universe,
        witness=witness, independently_held_root=witness.root,
    )
    index = repo._i03_release_indices[(release.release_ref, universe)]
    respondent = next(iter(index.respondents))
    assert len(list(_select_respondent_events(index, respondent, declared))) == 2
    assert len(list(_select_respondent_events(index, respondent, declared,
                                              native_only=True))) == 0
    # An invented alias still has no selector events; no semantic permission
    # to treat its emptiness as a certified question from this fact alone.
    assert list(_select_respondent_events(index, respondent, invented)) == []


def test_h36_multiple_accepted_instrument_versions_same_native_are_preserved():
    """The S2-A alias gate must not collapse legitimate per-instrument bindings."""
    from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
    original = _candidate("s2a-h36-versions", event_kind="UNORDERED_MULTISELECT_SET")
    first = original.question_variable_bindings[0]
    version = replace(first, instrument_question_version="S2A_ADDITIONAL_INSTRUMENT_VERSION")
    counts = dict(original.source_release_manifest.declared_record_counts_by_logical_family)
    counts["QuestionVariableBinding"] += 1
    candidate = replace(
        original,
        source_release_manifest=replace(
            original.source_release_manifest,
            declared_record_counts_by_logical_family=counts,
        ),
        question_variable_bindings=(first, version),
        candidate_replay_manifest=None,
    )
    candidate = replace(
        candidate, candidate_replay_manifest=build_candidate_replay_manifest(
            candidate,
            replay_protocol_authority_ref=original.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=original.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version=original.candidate_replay_manifest.replay_protocol_version,
        ),
    )
    repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    assert result.accepted, result.errors
    release = repo.resolve_release_exact(result.release_ref)
    universe = candidate.empirical_universes[0].ref
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    rows = certified_i03_events(
        release, universe, witness=witness, independently_held_root=witness.root
    )
    respondent = candidate.respondent_identities[0].ref.key
    target = first.native_question_ref
    assert len(list(rows[respondent].select(target))) == 2


def test_h37_conflicting_instrument_version_canonical_mappings_refuse_ambiguous_event():
    release, universe, declared, invented = _s2a_contradictory_alias_fixture(
        "s2a-h37-conflicting-versions",
        event_uses_binding=True, conflicting_version_alias=True,
    )
    # I02 accepts two positive QuestionVariableBinding versions for one native
    # question and universe with conflicting canonical aliases. RespondentEvent
    # has no instrument_question_version field: S2-A cannot guess which
    # approved mapping produced this event.
    with pytest.raises(SemanticRangeIntegrityError, match="ambiguous|version|binding"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def _s2a_relation_source(
    tag: str, *, bindings, event_canonical=None, event_component=None,
):
    """Native-I02 accepted fixture with version-qualified paired alias grants.

    bindings: (instrument version, canonical tag/None, component tag/None).
    These are sourcefree real QuestionVariableBinding records, never fabricated
    CertifiedRespondentEvents or presealed release objects.
    """
    from rawlsing_next.tests.test_pre553_c11_repository_ingest import _authority, _ref
    from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, TypedAbsence
    from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    old = _candidate(tag, event_kind="UNORDERED_MULTISELECT_SET")
    mapping = _authority(
        tag + "-alias-authority", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    def cref(key):
        return _ref("QUESTION_CANONICAL", tag + "-" + key) if key is not None else None
    def sref(key):
        return _ref("QUESTION_COMPONENT", tag + "-" + key) if key is not None else None
    q0 = old.question_variable_bindings[0]
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=q0.empirical_universe_ref,
            native_question_ref=q0.native_question_ref,
            instrument_question_version=version,
            canonical_question_ref_or_typed_absence=(
                cref(canonical) if canonical is not None else TypedAbsence("NOT_APPLICABLE")
            ),
            component_subitem_ref_or_typed_absence=(
                sref(component) if component is not None else TypedAbsence("NOT_APPLICABLE")
            ),
            semantic_authority_ref=(
                mapping.authority_ref if canonical is not None else q0.semantic_authority_ref
            ),
            topology_authority_ref=q0.topology_authority_ref,
        )
        for version, canonical, component in bindings
    )
    events = []
    for e in old.respondent_events:
        fields = dict(e.semantic_fields)
        fields.update(
            canonical_question_ref_if_authorized=cref(event_canonical),
            component_or_subitem_ref=sref(event_component),
            value_transform_authority_ref=(
                mapping.authority_ref if event_canonical is not None else None
            ),
        )
        events.append(RespondentEvent(
            typed_state=e.typed_state,
            authority_snapshot_refs=(
                (*e.authority_snapshot_refs, mapping.authority_ref)
                if event_canonical is not None else e.authority_snapshot_refs
            ),
            dependency_refs=e.dependency_refs,
            producer_replay_locator_or_reference_root=e.producer_replay_locator_or_reference_root,
            **fields,
        ))
    counts = dict(old.source_release_manifest.declared_record_counts_by_logical_family)
    counts["QuestionVariableBinding"] = len(questions)
    counts["AuthoritySnapshot"] += 1
    manifest = replace(
        old.source_release_manifest,
        declared_record_counts_by_logical_family=counts,
        declared_authority_snapshot_refs=(
            *old.source_release_manifest.declared_authority_snapshot_refs,
            mapping.authority_ref,
        ),
    )
    candidate = replace(
        old, source_release_manifest=manifest,
        question_variable_bindings=questions,
        respondent_events=tuple(events),
        authority_snapshots=(*old.authority_snapshots, mapping),
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
    repository = C11Repository()
    result = ingest_c11_source_release(candidate, repository)
    assert result.accepted, result.errors
    release = repository.resolve_release_exact(result.release_ref)
    return release, old.empirical_universes[0].ref, repository, cref, sref


def test_h38_i02_accepts_wrong_component_but_witness_must_refuse():
    release, universe, _, _, _ = _s2a_relation_source(
        "s2a-h38-component", bindings=(("V1", None, "A"),),
        event_component="B",
    )
    with pytest.raises(SemanticRangeIntegrityError, match="component|binding"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h39_i02_accepts_component_despite_explicit_absent_binding():
    release, universe, _, _, _ = _s2a_relation_source(
        "s2a-h39-unmapped", bindings=(("V1", None, None),),
        event_component="A",
    )
    with pytest.raises(SemanticRangeIntegrityError, match="component|binding"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h40_conflicting_component_grants_across_versions_refused():
    release, universe, _, _, _ = _s2a_relation_source(
        "s2a-h40-versions",
        bindings=(("V1", None, "A"), ("V2", None, "B")),
        event_component="A",
    )
    with pytest.raises(SemanticRangeIntegrityError, match="component|ambiguous|version"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h41_same_version_distinct_approved_components_preserved():
    release, universe, repository, _, sref = _s2a_relation_source(
        "s2a-h41-siblings",
        bindings=(("V1", None, "A"), ("V1", None, "B")),
        event_component="A",
    )
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    install_sourcefree_i02_certified_i03_range(
        repository, release_ref=release.release_ref,
        universe_ref=universe, witness=witness,
        independently_held_root=witness.root,
    )
    index = repository._i03_release_indices[(release.release_ref, universe)]
    respondent = next(iter(index.respondents))
    assert len(list(_select_respondent_events(
        index, respondent, sref("A"), include_component=True,
    ))) == 2
    assert list(_select_respondent_events(
        index, respondent, sref("B"), include_component=True,
    )) == []


def test_h42_pairwise_cross_grant_alias_composition_must_refuse():
    """Even separately authorized refs cannot be joined across binding rows."""
    release, universe, _, _, _ = _s2a_relation_source(
        "s2a-h42-cross-product",
        bindings=(("V1", "C1", "A"), ("V1", "C2", "B")),
        event_canonical="C1", event_component="B",
    )
    with pytest.raises(SemanticRangeIntegrityError, match="binding|pair|component"):
        I02SemanticRangeWitness.from_validated_release(release, universe)


def test_h43_same_version_two_canonical_grants_paired_component_disambiguates():
    """One version, two component-specific canonical grants: not version ambiguity."""
    release, universe, repository, cref, sref = _s2a_relation_source(
        "s2a-h43-paired-siblings",
        bindings=(("V1", "C1", "A"), ("V1", "C2", "B")),
        event_canonical="C1", event_component="A",
    )
    witness = I02SemanticRangeWitness.from_validated_release(release, universe)
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    install_sourcefree_i02_certified_i03_range(
        repository, release_ref=release.release_ref,
        universe_ref=universe, witness=witness, independently_held_root=witness.root,
    )
    index = repository._i03_release_indices[(release.release_ref, universe)]
    respondent = next(iter(index.respondents))
    assert len(list(_select_respondent_events(index, respondent, cref("C1")))) == 2
    assert len(list(_select_respondent_events(
        index, respondent, sref("A"), include_component=True,
    ))) == 2
    assert list(_select_respondent_events(index, respondent, cref("C2"))) == []


def test_h44_same_component_grant_across_versions_preserved():
    release, universe, _, _, _ = _s2a_relation_source(
        "s2a-h44-agreed-versions",
        bindings=(("V1", None, "A"), ("V2", None, "A")),
        event_component="A",
    )
    assert I02SemanticRangeWitness.from_validated_release(release, universe).root


def test_h45_changed_i02_value_changes_actual_i03_fact_and_restores():
    """Source change—not a poisoned index—must change the real first consumer."""
    from rawlsing_next.pre553_empirical_query import install_sourcefree_i02_certified_i03_range
    qa = _query_authority("s2a-h45-changed")
    results = []
    for tag, value in (("s2a-h45-before", 0), ("s2a-h45-after", 1), ("s2a-h45-before", 0)):
        source = _build_source(tag, [{"id": "R1", "responses": {"Y": value}}])
        witness, root = _trusted(source)
        install_sourcefree_i02_certified_i03_range(
            source["repo"], release_ref=source["release_ref"],
            universe_ref=source["universe"].ref,
            witness=witness, independently_held_root=root,
        )
        pred = _branch_predicate(source, qa, tag="s2a-h45")
        query = _query(source, qa, pred, ("Y",), tag="s2a-h45")
        results.append(_run(source, qa, pred, query))
    assert _cell_map(results[0].facts[0])["1"]["raw_numerator_support"] == 0
    assert _cell_map(results[1].facts[0])["1"]["raw_numerator_support"] == 1
    assert results[0] == results[2]


def test_h46_sourcebacked_occurrence_component_without_question_grant_remains_native_only():
    """Explicit producer occurrence rule is not the same as a persisted QVB grant.

    The source-backed C11 producer may legally put a component on an
    OccurrenceRule while QVB.component is typed absent. I02 accepts the source
    and the native first reader retains the event. S2-A cannot authenticate
    the extra component alias from I02-only records: refuse its *opt-in*
    certificate, do not erase the native release or promote the occurrence
    without source/sidecar provenance from Pair 1.
    """
    pytest.importorskip("pandas")
    from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture
    from rawlsing_next.tests.test_pre553_empirical_query import _ref
    from rawlsing_next.pre553_source_backed_c11_facade import (
        build_validated_source_backed_c11_release,
    )
    from rawlsing_next.pre553_empirical_objects import RespondentEvent

    fx = _fixture("s2a-h46-occurrence-qualified")
    projection = fx["projection"]
    old_slots = list(projection.response_slots)
    m_idx = next(i for i, row in enumerate(old_slots)
                 if row.slot.name == "M")
    old_slot = old_slots[m_idx]
    values = list(old_slot.values)
    first_value = values[0]
    first_occ = first_value.occurrences[0]
    alternate = _ref("QUESTION_COMPONENT", "s2a-h46-explicit-occurrence")
    values[0] = replace(
        first_value,
        occurrences=(replace(first_occ, component_ref=alternate),
                     *first_value.occurrences[1:]),
    )
    old_slots[m_idx] = replace(old_slot, values=tuple(values))
    projection = replace(projection, response_slots=tuple(old_slots))
    native_release = build_validated_source_backed_c11_release(fx["incidence"], projection)
    events = [
        e for e in native_release.public_objects
        if isinstance(e, RespondentEvent)
        and e.component_or_subitem_ref == alternate.as_dict()
    ]
    assert events  # actual producer emits source-qualified occurrence component
    repo = C11Repository((native_release,))
    index = _build_release_index(native_release, fx["universe"].ref)
    native_scoped = next(k for k, value in index.respondents.items()
                         if value.ref.as_dict() == events[0].scoped_respondent_ref)
    assert list(_select_respondent_events(
        index, native_scoped, alternate, include_component=True,
    ))
    # An I02-only witness cannot inspect the source projection that supplied
    # this occurrence grant. Refuse additional certification, preserve native.
    with pytest.raises(SemanticRangeIntegrityError, match="component|binding"):
        I02SemanticRangeWitness.from_validated_release(native_release, fx["universe"].ref)
    assert repo.resolve_release_exact(native_release.release_ref) is native_release


def test_h47_untrusted_posting_changes_after_witness_check_must_refuse_real_i03():
    """H26 range integrity, not a new grant: a digest cannot seal a second iterator.

    Both event objects come from the same real I02-accepted sourcefree
    release. Only the derived range accessor is adversarial: first iteration
    supplies the correct R1 event for _digest, second supplies R2's genuine
    event to native I03. One ordinary mutable list would have the same
    check/use window under a concurrent writer.
    """
    source = _build_source("s2a-h47-check-use", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa = _query_authority("s2a-h47-check-use")
    pred = _branch_predicate(source, qa, tag="s2a-h47-check-use")
    query = _query(source, qa, pred, ("Y",), tag="s2a-h47-check-use")
    oracle = _run(source, qa, pred, query)
    assert oracle.facts[0].typed_state == "SUPPORTED"

    witness, root = _trusted(source)
    postings = _canonical_postings(source, witness)
    target = source["qrefs"]["Y"]
    r1 = source["respondents"]["R1"].ref.key
    r2 = source["respondents"]["R2"].ref.key
    key1, key2 = (r1, "native", target.key), (r2, "native", target.key)
    assert len(postings[key1]) == len(postings[key2]) == 1
    correct, wrong = postings[key1][0], postings[key2][0]
    assert correct.ref != wrong.ref

    class FlipAfterDigest(list):
        def __init__(self):
            super().__init__((correct,))
            self.iterations = 0

        def __iter__(self):
            self.iterations += 1
            return iter((correct if self.iterations % 2 else wrong,))

    candidate = dict(postings)
    candidate[key1] = FlipAfterDigest()
    # Direct original selector and actual I03 owner must both fail closed:
    # the event value served after digest is not the event that was hashed.
    reader = certified_i03_events(
        _release(source), source["universe"].ref,
        witness=witness, independently_held_root=root,
        candidate_postings=candidate,
    )
    with pytest.raises(SemanticRangeIntegrityError):
        list(reader[r1].select(target, native_only=True))

    candidate[key1] = FlipAfterDigest()
    _install_i03(source, witness, root, postings=candidate)
    denied = _run(source, qa, pred, query)
    assert denied.facts[0].typed_state == "INTEGRITY_FAILURE"
    _install_i03(source, witness, root)
    assert _run(source, qa, pred, query) == oracle
