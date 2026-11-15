"""S06G repair expectations. Synthetic records; no issuer credentials or CURRENT."""
from copy import deepcopy
from dataclasses import replace
from threading import Barrier, Event, Thread

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor as B5, LearnedProductLifecycleConflict,
    LearnedProductLifecycleError,
)
from rawlsing_next.pre553_learned_product_release import (
    M2Repository, M2ReleaseError, RepresentationRecord, PublicationBinding,
    M2_PUBLICATION_CONTRACT_REF, publish_binding, resolve_release_exact,
)
from rawlsing_next.tests.s06g_fixtures import (
    ref, subject, register, checkpoint_with_publication, m2_fixture,
)
from rawlsing_next.tests.test_pre553_learned_product_lifecycle import _key, _select
from rawlsing_next.tests.test_pre553_learned_product_release import build_fixture, bind_representation


def authority():
    return dict(event_authority_ref=ref('Authority', 'local'), event_rule_ref=ref('Rule', 'local'))


def resign(cp):
    cp['checkpoint_hash'] = semantic_hash(cp['checkpoint_payload'])
    return cp


def test_nested_payload_and_history_are_detached_immutable_and_refs_stable():
    x, s, _ = checkpoint_with_publication()
    event = x.events[-1]
    old = event.ref
    with pytest.raises(TypeError):
        event.payload['replay_root_ref']['object_id'] = 'alien'
    with pytest.raises(TypeError):
        x.release_history(s.release_ref)[-1].payload['authority_snapshot_refs'][0]['authority_id'] = 'alien'
    assert event.ref == old
    exported = event.as_dict()
    exported['payload']['replay_root_ref']['object_id'] = 'export-only'
    assert event.ref == old
    external = {'nested': [{'value': 1}]}
    detached = replace(event, payload=external)
    external['nested'][0]['value'] = 2
    assert detached.payload['nested'][0]['value'] == 1


@pytest.mark.parametrize('field', ['replay_root_ref', 'determinant_set_hash', 'producer_permission_ceiling', 'authority_snapshot_refs'])
def test_publication_payload_must_match_subject_even_rehashed(field):
    x, _, cp = checkpoint_with_publication()
    payload = x.events[-1].as_dict()['payload']
    payload[field] = semantic_hash('alien') if field == 'determinant_set_hash' else (
        [] if field == 'authority_snapshot_refs' else ref('Alien', field).as_dict())
    cp['checkpoint_payload']['events'][-1] = replace(x.events[-1], payload=payload).as_dict()
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(resign(cp))


@pytest.mark.parametrize('receipt_kind', ['rebuild_eligibility', 'rebuild_links', 'gc_eligibility', 'selection_receipts', 'no_current_receipts'])
def test_receipts_must_bind_event_release_and_all_fields(receipt_kind):
    x = B5()
    a = register(x, replace(subject('a'), materialization_class='RECOMPUTABLE_PRODUCT_PAYLOAD'), publish=True)
    b = register(x, subject('b'), publish=True)
    key = _key(x, a)
    selected = _select(x, key, a)
    x.record_rebuild_eligibility(a.release_ref, execution_mechanism_ref=ref('Mechanism', 'a'),
        source_or_upstream_refs=(ref('Input', 'a'),), **authority())
    x.link_rebuild(a.release_ref, new_release_ref=b.release_ref, rebuild_state='REBUILT',
        rebuild_determinant_set_hash=b.determinant_set_hash,
        replay_or_execution_receipt_ref=ref('Receipt', 'rebuild'), **authority())
    x.attest_gc_eligibility(a.release_ref, **gc_proofs(), **authority())
    x.declare_no_current(key.ref, expected_previous_receipt_ref=selected.ref,
        selection_attestation_ref=ref('Attest', 'clear'), reason_ref=ref('Reason', 'clear'), **authority())
    cp = x.export_checkpoint()
    assert B5.from_checkpoint(cp).export_checkpoint() == cp
    row = cp['checkpoint_payload'][receipt_kind][0]
    if receipt_kind in ('selection_receipts', 'no_current_receipts'):
        row['selection_authority_refs'] = [ref('Authority', 'alien').as_dict()]
        record = next(iter(x._selection_receipts.values())) if receipt_kind == 'selection_receipts' else next(iter(x._no_current_receipts.values()))
        forged = replace(record, selection_authority_refs=(ref('Authority', 'alien'),))
    else:
        record = next(iter(getattr(x, '_' + receipt_kind).values()))
        forged = replace(record, **({'old_release_ref': b.release_ref} if receipt_kind == 'rebuild_links' else {'release_ref': b.release_ref}))
    cp['checkpoint_payload'][receipt_kind][0] = forged.as_dict()
    # Selection indexes must also name the rewritten receipt to bypass hash-only checks.
    for entry in cp['checkpoint_payload']['selection_index']:
        if entry['receipt_ref'] == record.ref.as_dict():
            entry['receipt_ref'] = forged.ref.as_dict()
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(resign(cp))


def gc_proofs():
    return {name: ref('Proof', name) for name in (
        'reconstruction_proof_ref', 'historical_retention_proof_ref',
        'serving_reconstruction_proof_ref', 'downstream_byte_dependency_absence_proof_ref',
        'source_carrier_retention_proof_ref')}


def test_concurrent_select_has_one_winner_one_conflict_and_recoverable_history():
    for attempt in range(12):
        x = B5()
        a = register(x, subject('a'), publish=True)
        b = register(x, subject('b'), publish=True)
        key = _key(x, a)
        start = Barrier(2)
        winners, errors = [], []
        def select(item):
            start.wait(timeout=5)
            try:
                winners.append(_select(x, key, item, previous=None))
            except Exception as exc:
                errors.append(exc)
        threads = [Thread(target=select, args=(item,)) for item in (a, b)]
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=6)
        assert all(not thread.is_alive() for thread in threads)
        assert len(winners) == len(errors) == 1
        assert isinstance(errors[0], LearnedProductLifecycleConflict)
        cp = x.export_checkpoint()
        assert B5.from_checkpoint(cp).export_checkpoint() == cp


def b5_operation(name):
    x = B5()
    a = register(x, replace(subject('a'), materialization_class='RECOMPUTABLE_PRODUCT_PAYLOAD'), publish=True)
    b = register(x, subject('b'), publish=True)
    cache = register(x, replace(subject('cache'), materialization_class='OPTIONAL_CACHE_ACCELERATOR'))
    unpublished = register(x, subject('unpublished'))
    staged = subject('staged')
    x.stage_release(staged)
    key = _key(x, a)
    selected = _select(x, key, a)
    eligible = x.record_rebuild_eligibility(a.release_ref, execution_mechanism_ref=ref('Mechanism', 'a'),
        source_or_upstream_refs=(ref('Input', 'a'),), **authority())
    gc = x.attest_gc_eligibility(a.release_ref, **gc_proofs(), **authority())
    common = authority()
    attestation = ref('Attest', 'a')
    operations = {
        'register_product': lambda: x.register_product(staged.release_ref, **common),
        'publish_product': lambda: x.publish_product(unpublished.release_ref, **common),
        'record_recertification': lambda: x.record_recertification(a.release_ref, attestation_ref=attestation, **common),
        'select_current': lambda: x.select_current(key.ref, b.release_ref,
            expected_previous_receipt_ref=selected.ref, selection_attestation_ref=attestation, **common),
        'declare_no_current': lambda: x.declare_no_current(key.ref, expected_previous_receipt_ref=selected.ref,
            selection_attestation_ref=attestation, reason_ref=ref('Reason', 'clear'), **common),
        'supersede_current': lambda: x.supersede_current(key.ref, predecessor_release_ref=a.release_ref,
            successor_release_ref=b.release_ref, expected_previous_receipt_ref=selected.ref,
            selection_attestation_ref=attestation, supersession_basis_ref=ref('Basis', 'a'), **common),
        'withdraw_product': lambda: x.withdraw_product(a.release_ref, withdrawal_reason_ref=ref('Reason', 'withdraw'),
            withdrawal_scope_ref=ref('Scope', 'withdraw'), selection_attestation_ref=attestation,
            current_transitions={key.ref.key: None}, **common),
        'declare_invalidation': lambda: x.declare_invalidation(a.determinant_refs,
            dependency_closure_receipt_ref=ref('Closure', 'inv'), selection_attestation_ref=attestation,
            current_transitions={key.ref.key: None}, **common),
        'record_rebuild_eligibility': lambda: x.record_rebuild_eligibility(b.release_ref,
            execution_mechanism_ref=None, **common),
        'link_rebuild': lambda: x.link_rebuild(a.release_ref, new_release_ref=b.release_ref, rebuild_state='REBUILT',
            rebuild_determinant_set_hash=b.determinant_set_hash, replay_or_execution_receipt_ref=ref('Receipt', 'b'), **common),
        'record_cache_materialized': lambda: x.record_cache_materialized(cache.release_ref, cache_ref=ref('Cache', 'a'), **common),
        'record_cache_dropped': lambda: x.record_cache_dropped(cache.release_ref, cache_ref=ref('Cache', 'a'), **common),
        'attest_gc_eligibility': lambda: x.attest_gc_eligibility(a.release_ref, **gc_proofs(), **common),
        'record_payload_gc': lambda: x.record_payload_gc(gc.ref, **common),
    }
    return x, operations[name]


@pytest.mark.parametrize('name', [
    'register_product', 'publish_product', 'record_recertification', 'select_current',
    'declare_no_current', 'supersede_current', 'withdraw_product', 'declare_invalidation',
    'record_rebuild_eligibility', 'link_rebuild', 'record_cache_materialized', 'record_cache_dropped',
    'attest_gc_eligibility', 'record_payload_gc',
])
def test_each_event_mutator_rolls_back_post_append_exception(name, monkeypatch):
    x, operation = b5_operation(name)
    cp = x.export_checkpoint()
    original = x._append_events
    def interrupted(events):
        original(events)
        raise RuntimeError('injected after append')
    monkeypatch.setattr(x, '_append_events', interrupted)
    with pytest.raises(RuntimeError, match='injected after append'):
        operation()
    assert x.export_checkpoint() == cp
    assert B5.from_checkpoint(cp).export_checkpoint() == cp


@pytest.mark.parametrize('name', ['stage_release', 'stage_protocol', 'selection_key'])
def test_non_event_mutators_rollback_after_write(name, monkeypatch):
    x, s, cp = checkpoint_with_publication()
    class InterruptedDict(dict):
        def __setitem__(self, key, value):
            super().__setitem__(key, value)
            raise RuntimeError('injected after store write')
    if name == 'selection_key':
        monkeypatch.setattr(x, '_selection_keys', InterruptedDict(x._selection_keys))
        operation = lambda: _key(x, s)
    else:
        monkeypatch.setattr(x, '_repository_subjects', InterruptedDict(x._repository_subjects))
        if name == 'stage_release':
            operation = lambda: x.stage_release(subject('new'))
        else:
            # Use the accepted subject protocol itself; it exposes the required fields.
            operation = lambda: x.stage_protocol(subject('new'))
    with pytest.raises(RuntimeError, match='injected after store write'):
        operation()
    assert x.export_checkpoint() == cp


def test_saved_internal_helpers_refuse_without_transaction():
    x, s, cp = checkpoint_with_publication()
    event = x._event(event_kind='PRODUCT_PUBLISHED', subject=subject('unregistered'), **authority())
    with pytest.raises(LearnedProductLifecycleConflict, match='transaction'):
        x._append_events((event,))
    with pytest.raises(LearnedProductLifecycleConflict, match='transaction'):
        x._commit_selection_transition_receipts(())
    assert x.export_checkpoint() == cp
    repo = M2Repository()
    with pytest.raises(M2ReleaseError, match='requires native writer transaction'):
        repo._insert(repo._releases, ref('Release', 'alien'), 'untyped', 'COLLISION')
    assert repo.releases == ()


def m2_snapshot(repo):
    return {name: dict(getattr(repo, name)) for name in repo._store_names}


@pytest.mark.parametrize('name', ['register_subject', 'register_closure', 'register_release', 'register_representation', 'register_binding'])
def test_each_m2_writer_rolls_back_post_insert_exception(name, monkeypatch):
    repo, release, source, producer, closures = m2_fixture()
    record = RepresentationRecord(release_ref=release.ref, resolved_subject_ref=source,
        producer_contract_ref=producer, resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',
        resolver_or_locator_ref=ref('Locator', 'new'), representation_integrity_ref=ref('Integrity', 'new'))
    repo.register_representation(record)
    binding = PublicationBinding(release_ref=release.ref, publication_contract_ref=M2_PUBLICATION_CONTRACT_REF,
        resolution_mode=record.resolution_mode, resolver_or_locator_ref=record.resolver_or_locator_ref,
        representation_integrity_ref=record.representation_integrity_ref)
    values = {'register_subject': replace(repo.subject_exact(source), ref=ref('Subject', 'new')),
        'register_closure': replace(closures['DEPENDENCY'], member_refs=(ref('Member', 'new'),)),
        'register_release': release, 'register_representation': replace(record, resolver_or_locator_ref=ref('Locator', 'other')),
        'register_binding': binding}
    # Exercise new release insertion by lawfully removing the existing indexed release.
    if name == 'register_release': repo._releases.clear()
    cp = m2_snapshot(repo)
    insert = repo._insert
    def interrupted(*args):
        insert(*args)
        raise RuntimeError('injected after insert')
    monkeypatch.setattr(repo, '_insert', interrupted)
    with pytest.raises(RuntimeError, match='injected after insert'):
        getattr(repo, name)(values[name])
    assert m2_snapshot(repo) == cp


def test_m2_competing_subject_preimages_have_one_winner_no_overwrite():
    repo, _, source, _, _ = m2_fixture()
    first = replace(repo.subject_exact(source), ref=ref('Subject', 'collision'))
    second = replace(first, typed_state='UNKNOWN')
    start = Barrier(2)
    winners, errors = [], []
    def write(record):
        start.wait(timeout=5)
        try: winners.append(repo.register_subject(record))
        except Exception as exc: errors.append(exc)
    threads = [Thread(target=write, args=(record,)) for record in (first, second)]
    for thread in threads: thread.start()
    for thread in threads: thread.join(timeout=6)
    assert all(not thread.is_alive() for thread in threads)
    assert len(winners) == len(errors) == 1
    assert isinstance(errors[0], M2ReleaseError) and errors[0].code == 'SEMANTIC_REOWNERSHIP_ATTEMPT'
    assert repo.subject_exact(first.ref) == winners[0]


def import_release(target, source, release):
    target.register_subject(source.subject_exact(release.release_subject_ref))
    for field in ('authority_closure_ref', 'dependency_closure_ref', 'determinant_closure_ref',
                  'replay_reconstruction_ref', 'explanation_lineage_ref'):
        target.register_closure(source.closure_exact(getattr(release, field)))
    target.register_release(release)


def test_reconciled_m2_17_early_refusal_and_lawful_downstream_mismatch():
    repo, first, _, _, _, _ = build_fixture(subject_label='first')
    foreign, second, source, producer, _, _ = build_fixture(subject_label='second')
    record = RepresentationRecord(release_ref=second.ref, resolved_subject_ref=source,
        producer_contract_ref=producer, resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',
        resolver_or_locator_ref=ref('Locator', 'foreign'), representation_integrity_ref=ref('Integrity', 'foreign'))
    with pytest.raises(M2ReleaseError) as exc:
        repo.register_representation(record)
    assert exc.value.code == 'RELEASE_UNAVAILABLE'
    import_release(repo, foreign, second)
    repo.register_representation(record)
    with pytest.raises(M2ReleaseError) as exc:
        publish_binding(repo, release_ref=first.ref, resolution_mode=record.resolution_mode,
            resolver_or_locator_ref=record.resolver_or_locator_ref, representation_integrity_ref=record.representation_integrity_ref)
    assert exc.value.code == 'PUBLICATION_BINDING_MISMATCH'


def test_reconciled_m2_18_early_refusal_and_lawful_failover_mismatch():
    repo, release, source, producer, _, _ = build_fixture(subject_label='main')
    first, _, _ = bind_representation(repo, release, source, producer, label='first', mode='CONTENT_ADDRESSED_MATERIALIZATION')
    second, _, _ = bind_representation(repo, release, source, producer, label='second', mode='CONTENT_ADDRESSED_MATERIALIZATION')
    result = resolve_release_exact(repo, release.ref, publication_binding_refs=(first.ref, second.ref), unavailable_binding_refs=(first.ref,))
    assert result.receipt.used_publication_binding_ref == second.ref
    foreign, other, osource, oproducer, _, _ = build_fixture(subject_label='foreign')
    binding, locator, _ = bind_representation(foreign, other, osource, oproducer, label='foreign', mode='CONTENT_ADDRESSED_MATERIALIZATION')
    with pytest.raises(M2ReleaseError) as exc:
        repo.register_binding(binding)
    assert exc.value.code == 'RELEASE_UNAVAILABLE'
    import_release(repo, foreign, other)
    repo.register_representation(foreign.representation_exact(locator))
    repo.register_binding(binding)
    with pytest.raises(M2ReleaseError) as exc:
        resolve_release_exact(repo, release.ref, publication_binding_refs=(first.ref, binding.ref), unavailable_binding_refs=(first.ref,))
    assert exc.value.code == 'PUBLICATION_BINDING_MISMATCH'


def test_invalidation_receipt_closure_cannot_be_rewritten_or_dropped():
    x = B5()
    a = register(x, subject('root'))
    b = register(x, subject('child', dependency=(a.release_ref,)))
    sibling = register(x, subject('sibling'))
    receipt = x.declare_invalidation(a.determinant_refs,
        dependency_closure_receipt_ref=ref('Closure', 'inv'), selection_attestation_ref=ref('Attest', 'inv'), **authority())
    cp = x.export_checkpoint()
    assert B5.from_checkpoint(cp).export_checkpoint() == cp
    forged = replace(receipt, unaffected_product_refs=())
    cp['checkpoint_payload']['invalidations'][0] = forged.as_dict()
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(resign(cp))
    cp = x.export_checkpoint()
    cp['checkpoint_payload']['invalidations'].clear()
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(resign(cp))


def test_noop_invalidation_before_later_registration_remains_replayable():
    x = B5()
    a = register(x, subject('a'))
    x.declare_invalidation((ref('Determinant', 'absent'),),
        dependency_closure_receipt_ref=ref('Closure', 'noop'), selection_attestation_ref=ref('Attest', 'noop'), **authority())
    register(x, subject('later'))
    cp = x.export_checkpoint()
    assert B5.from_checkpoint(cp).export_checkpoint() == cp


def test_reader_waits_for_transaction_and_sees_complete_rollback(monkeypatch):
    x = B5()
    s = register(x, subject('a'))
    cp = x.export_checkpoint()
    appended, release, attempted, read_finished = Event(), Event(), Event(), Event()
    original = x._append_events
    failures, observations = [], []
    def interruption(events):
        original(events)
        appended.set()
        assert release.wait(timeout=5)
        raise RuntimeError('injected before projection')
    monkeypatch.setattr(x, '_append_events', interruption)
    def writer():
        try: x.publish_product(s.release_ref, **authority())
        except RuntimeError as exc: failures.append(exc)
    def reader():
        attempted.set()
        observations.append(x.export_checkpoint())
        read_finished.set()
    writing = Thread(target=writer)
    writing.start()
    assert appended.wait(timeout=5)
    reading = Thread(target=reader)
    reading.start()
    assert attempted.wait(timeout=5)
    assert not read_finished.wait(timeout=0.05)
    release.set()
    writing.join(timeout=6); reading.join(timeout=6)
    assert not writing.is_alive() and not reading.is_alive()
    assert len(failures) == 1 and observations == [cp]


def test_m2_closure_descendants_are_immutable():
    from rawlsing_next.pre553_learned_product_release import ClosureObject
    payload = {'nested': [{'value': 'first'}]}
    closure = ClosureObject('DEPENDENCY', (ref('Member', 'a'),), True, metadata=payload)
    old = closure.ref
    payload['nested'][0]['value'] = 'outside'
    with pytest.raises(TypeError):
        closure.metadata['nested'][0]['value'] = 'inside'
    assert closure.metadata['nested'][0]['value'] == 'first' and closure.ref == old


def test_unwrapped_saved_public_bodies_cannot_bypass_transaction():
    x = B5()
    with pytest.raises(LearnedProductLifecycleConflict, match='transaction'):
        B5.stage_release.__wrapped__(x, subject('outside'))
    assert x.staged_release_refs == ()
    repo, _, source, _, _ = m2_fixture()
    before = m2_snapshot(repo)
    with pytest.raises(M2ReleaseError, match='transaction'):
        M2Repository.register_subject.__wrapped__(repo, replace(repo.subject_exact(source), ref=ref('Subject', 'outside')))
    assert m2_snapshot(repo) == before
