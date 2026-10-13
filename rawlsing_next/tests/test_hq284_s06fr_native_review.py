"""Independent native review. OBSERVED tests reproduce defects, not acceptance.

Only source-free record constructors are reused from the author fixture module;
the assertions, fault injection and schedules below are reviewer-owned.
"""
from copy import deepcopy
from dataclasses import replace
from inspect import signature, Parameter
from threading import Barrier, Thread, local

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import (
    LearnedProductLifecycleExecutor as B5, LearnedProductLifecycleError,
    LearnedProductLifecycleConflict,
)
from rawlsing_next.pre553_learned_product_release import M2Repository as M2, M2ReleaseError
from rawlsing_next.tests.test_pre553_s06f_native_owner_security import (
    ref, subject, register, checkpoint_with_publication, m2_fixture,
)

B5_METHODS = (
    'stage_release', 'stage_protocol', 'register_product', 'publish_product',
    'record_recertification', 'selection_key', 'select_current',
    'declare_no_current', 'supersede_current', 'withdraw_product',
    'declare_invalidation', 'record_rebuild_eligibility', 'link_rebuild',
    'record_cache_materialized', 'record_cache_dropped',
    'attest_gc_eligibility', 'record_payload_gc',
)
M2_METHODS = ('register_subject', 'register_closure', 'register_release',
              'register_representation', 'register_binding')

@pytest.mark.parametrize('owner,names', [(B5, B5_METHODS), (M2, M2_METHODS)])
@pytest.mark.parametrize('mode', ['PROTECTED_CURRENT', 'EXTERNAL_CUSTODY', 'arbitrary-token'])
def test_all_saved_native_writers_refuse_external_mode_before_validation(owner, names, mode):
    instance = owner()
    saved = {name: getattr(owner, name) for name in names}
    instance._native_security_mode = mode  # Negative refusal probe, no protected issuance.
    for name, method in saved.items():
        args, kwargs = [instance], {}
        for param in list(signature(method).parameters.values())[1:]:
            if param.default is not Parameter.empty:
                continue
            if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD):
                args.append(None)
            elif param.kind == Parameter.KEYWORD_ONLY:
                kwargs[param.name] = None
        with pytest.raises((LearnedProductLifecycleError, M2ReleaseError), match='EXTERNAL_ISSUER_HOLD'):
            method(*args, **kwargs)

def test_predecessor_and_ordinal_refusal_is_atomic():
    x, s, cp = checkpoint_with_publication()
    event = x._event(event_kind='RECERTIFIES', subject=s,
                     event_authority_ref=ref('Authority', 'probe'), event_rule_ref=ref('Rule', 'probe'))
    for bad in (replace(event, ordinal=99), replace(event, parent_lifecycle_event_ref=x.events[0].ref)):
        with pytest.raises(LearnedProductLifecycleConflict):
            x._append_events((bad,))
        assert x.export_checkpoint() == cp

def test_diamond_invalidation_preserves_sibling_and_cold_replay():
    x = B5()
    a = register(x, subject('a'))
    b = register(x, subject('b', dependency=(a.release_ref,)))
    c = register(x, subject('c', dependency=(a.release_ref,)))
    d = register(x, subject('d', dependency=(b.release_ref, c.release_ref)))
    sibling = register(x, subject('sibling'))
    x.declare_invalidation(a.determinant_refs, event_authority_ref=ref('Authority', 'inv'),
        event_rule_ref=ref('Rule', 'inv'), dependency_closure_receipt_ref=ref('Closure', 'inv'),
        selection_attestation_ref=ref('Attestation', 'inv'))
    restored = B5.from_checkpoint(x.export_checkpoint())
    for item in (a, b, c, d):
        assert restored.lifecycle_state(item.release_ref).validity == 'INVALIDATED_REBUILD_REQUIRED'
    assert restored.lifecycle_state(sibling.release_ref).validity == 'VALID'

def test_public_snapshots_are_immutable():
    x, s, cp = checkpoint_with_publication()
    snapshot = x.export_checkpoint()
    snapshot['checkpoint_payload']['events'][0]['payload']['attacker'] = True
    assert x.export_checkpoint() == cp
    with pytest.raises((TypeError, AttributeError)):
        x.events[-1].payload['attacker'] = True

@pytest.mark.parametrize('kind', ['RECERTIFIES', 'CURRENT_SELECTED', 'PRODUCT_PUBLISHED'])
def test_OBSERVED_direct_b5_append_bypasses_native_preflight(kind):
    x, s, _ = checkpoint_with_publication()
    saved = x._append_events
    event = x._event(event_kind=kind, subject=subject('unregistered-direct-event'),
        event_authority_ref=ref('Authority', 'unissued'), event_rule_ref=ref('Rule', 'unissued'))
    x._native_security_mode = 'EXTERNAL_CUSTODY'
    saved((event,))
    assert x.events[-1] == event

def test_OBSERVED_direct_m2_insert_bypasses_type_and_preflight():
    repo = M2()
    repo._native_security_mode = 'EXTERNAL_CUSTODY'
    fake = ref('Release', 'unissued')
    repo._insert(repo._releases, fake, 'not-a-ReleaseCore', 'COLLISION')
    assert repo._releases[fake.key] == 'not-a-ReleaseCore'

@pytest.mark.parametrize('field', ['replay_root_ref', 'determinant_set_hash', 'producer_permission_ceiling'])
def test_OBSERVED_publication_payload_not_bound_to_subject_on_cold_replay(field):
    x, s, cp = checkpoint_with_publication()
    event = x.events[-1]
    payload = dict(event.payload)
    payload[field] = semantic_hash('alien') if field == 'determinant_set_hash' else ref('Alien', field).as_dict()
    forged_event = replace(event, payload=payload)
    cp['checkpoint_payload']['events'][-1] = forged_event.as_dict()
    cp['checkpoint_hash'] = semantic_hash(cp['checkpoint_payload'])
    restored = B5.from_checkpoint(cp)
    assert restored.events[-1].payload[field] == payload[field]
    assert restored.lifecycle_state(s.release_ref).publication == 'PUBLISHED'

def test_OBSERVED_publication_torn_after_event_append(monkeypatch):
    x = B5()
    s = register(x, subject('torn'))
    prior = x.export_checkpoint()
    append = x._append_events
    def crash(events):
        append(events)
        raise RuntimeError('simulated process interruption after ledger append')
    monkeypatch.setattr(x, '_append_events', crash)
    with pytest.raises(RuntimeError):
        x.publish_product(s.release_ref, event_authority_ref=ref('Authority', 'pub'), event_rule_ref=ref('Rule', 'pub'))
    assert x.events[-1].event_kind == 'PRODUCT_PUBLISHED'
    assert x.lifecycle_state(s.release_ref).publication == 'UNPUBLISHED'
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(x.export_checkpoint())
    assert B5.from_checkpoint(prior).lifecycle_state(s.release_ref).publication == 'UNPUBLISHED'

def test_OBSERVED_m2_check_then_insert_race_overwrites_collision():
    repo = M2()
    barrier = Barrier(2)
    class RacingDict(dict):
        def get(self, key, default=None):
            result = super().get(key, default)
            barrier.wait(timeout=5)
            return result
    store = RacingDict()
    identity = ref('TestIdentity', 'same')
    errors = []
    def insert(value):
        try:
            repo._insert(store, identity, value, 'COLLISION')
        except Exception as exc:
            errors.append(exc)
    threads = [Thread(target=insert, args=(value,)) for value in ('A', 'B')]
    for thread in threads: thread.start()
    for thread in threads: thread.join(timeout=6)
    assert not errors and all(not thread.is_alive() for thread in threads)
    assert store[identity.key] in ('A', 'B')

def test_coherent_local_replacement_never_establishes_authenticity():
    x, _, cp = checkpoint_with_publication()
    other = B5()
    register(other, subject('replacement'), publish=True)
    restored = B5.from_checkpoint(other.export_checkpoint())
    assert restored.native_security_mode == 'LOCAL_UNAUTHENTICATED'
    with pytest.raises(LearnedProductLifecycleError, match='EXTERNAL_ISSUER_HOLD'):
        restored.require_external_issuer('cold-recovery')

def test_m2_exact_foreign_release_rejected_at_repository_boundary():
    from rawlsing_next.pre553_learned_product_release import RepresentationRecord
    repo, release, source, producer, _ = m2_fixture()
    wrong = replace(release, release_subject_ref=ref('LearnedEmpiricalDisposition', 'foreign'))
    with pytest.raises(M2ReleaseError):
        repo.register_release(wrong)
    record = RepresentationRecord(release_ref=wrong.ref, resolved_subject_ref=source,
        producer_contract_ref=producer, resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',
        resolver_or_locator_ref=ref('Locator', 'foreign'), representation_integrity_ref=ref('Integrity', 'foreign'))
    with pytest.raises(M2ReleaseError, match='RELEASE_UNAVAILABLE'):
        repo.register_representation(record)

def test_OBSERVED_concurrent_b5_selection_accepts_two_stale_predecessors(monkeypatch):
    x = B5()
    a = register(x, subject('race-a'), publish=True)
    b = register(x, subject('race-b'), publish=True)
    key = x.selection_key(product_family_ref=a.product_family_ref,
        selection_scope_ref=a.selection_scope_ref, selection_purpose_ref=ref('Purpose', 'race'))
    barrier = Barrier(2)
    original = x._assert_expected_previous
    def checked(*args, **kwargs):
        result = original(*args, **kwargs)
        barrier.wait(timeout=5)  # Both real checks finish before either commits.
        return result
    monkeypatch.setattr(x, '_assert_expected_previous', checked)
    receipts, errors = [], []
    def select(item):
        try:
            receipts.append(x.select_current(key.ref, item.release_ref,
                expected_previous_receipt_ref=None, event_authority_ref=ref('Authority', 'race'),
                event_rule_ref=ref('Rule', 'race'), selection_attestation_ref=ref('Attestation', 'race')))
        except Exception as exc:
            errors.append(exc)
    threads = [Thread(target=select, args=(item,)) for item in (a, b)]
    for thread in threads: thread.start()
    for thread in threads: thread.join(timeout=6)
    assert not errors and len(receipts) == 2
    assert all(receipt.previous_selection_receipt_ref is None for receipt in receipts)
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(x.export_checkpoint())

def test_OBSERVED_public_event_payload_changes_internal_identity():
    x, s, cp = checkpoint_with_publication()
    old_ref = x.events[-1].ref
    x.events[-1].payload['attacker'] = True
    assert x.events[-1].ref != old_ref
    assert x.export_checkpoint() != cp
    assert old_ref.key in x._events_by_ref

def test_checkpoint_changed_subject_scope_is_rejected_even_rehashed():
    x, s, cp = checkpoint_with_publication()
    cp['checkpoint_payload']['repository_subjects'][0] = replace(s, selection_scope_ref=ref('Scope', 'alien')).as_dict()
    cp['checkpoint_hash'] = semantic_hash(cp['checkpoint_payload'])
    with pytest.raises(LearnedProductLifecycleConflict):
        B5.from_checkpoint(cp)

def test_unknown_event_kind_is_rejected_without_mutation():
    x, s, cp = checkpoint_with_publication()
    with pytest.raises(LearnedProductLifecycleError, match='unknown lifecycle event'):
        replace(x.events[-1], event_kind='UNISSUED')
    assert x.export_checkpoint() == cp

def test_OBSERVED_rebuild_receipt_can_link_event_for_different_release():
    x = B5()
    a = register(x, subject('receipt-a'))
    b = register(x, subject('receipt-b'))
    receipt = x.record_rebuild_eligibility(a.release_ref, event_authority_ref=ref('Authority', 'rebuild'),
        event_rule_ref=ref('Rule', 'rebuild'), execution_mechanism_ref=None)
    cp = x.export_checkpoint()
    cp['checkpoint_payload']['rebuild_eligibility'] = [replace(receipt, release_ref=b.release_ref).as_dict()]
    cp['checkpoint_hash'] = semantic_hash(cp['checkpoint_payload'])
    restored = B5.from_checkpoint(cp)
    forged = next(iter(restored._rebuild_eligibility.values()))
    assert forged.release_ref == b.release_ref
    assert restored._events_by_ref[forged.event_ref.key].release_ref == a.release_ref

def test_duplicate_subject_identity_and_invalid_recertification_refuse():
    x, s, cp = checkpoint_with_publication()
    with pytest.raises(LearnedProductLifecycleConflict):
        x.stage_release(replace(s, replay_root_ref=ref('ReplayRoot', 'alien')))
    assert x.export_checkpoint() == cp
    x.declare_invalidation(s.determinant_refs, event_authority_ref=ref('Authority', 'inv'),
        event_rule_ref=ref('Rule', 'inv'), dependency_closure_receipt_ref=ref('Closure', 'inv'),
        selection_attestation_ref=ref('Attestation', 'inv'))
    before = x.export_checkpoint()
    with pytest.raises(LearnedProductLifecycleError, match='new qualified authority'):
        x.record_recertification(s.release_ref, event_authority_ref=ref('Authority', 'recert'),
            event_rule_ref=ref('Rule', 'recert'), attestation_ref=ref('Attestation', 'recert'))
    assert x.export_checkpoint() == before

def test_actual_m2_release_to_subject_route_and_b5_crosscheck():
    from rawlsing_next.pre553_learned_product_release import resolve_subject_exact
    repo, release, source, producer, _ = m2_fixture()
    resolved = resolve_subject_exact(repo, release.ref)
    assert resolved.ref == source and resolved.producer_contract_ref == producer
    x = B5()
    s = replace(subject('cross-owner'), release_ref=release.ref, producer_contract_ref=producer)
    x.stage_release(s)
    assert x.verify_m2_release_subject_exact(repo, release.ref) == s
    with pytest.raises(M2ReleaseError):
        repo.subject_exact(release.ref)  # Release identity is not producer subject identity.

def test_current_asof_stale_selection_and_withdrawal_are_distinct():
    from rawlsing_next.tests.test_pre553_learned_product_lifecycle import _key, _select
    x = B5()
    a = register(x, subject('asof-a'), publish=True)
    b = register(x, subject('asof-b'), publish=True)
    key = _key(x, a)
    first = _select(x, key, a)
    cp = x.export_checkpoint()
    with pytest.raises(LearnedProductLifecycleConflict):
        _select(x, key, b, previous=None)
    assert x.export_checkpoint() == cp
    x.withdraw_product(a.release_ref, withdrawal_reason_ref=ref('Reason', 'withdraw'),
        withdrawal_scope_ref=ref('Scope', 'withdraw'), event_authority_ref=ref('Authority', 'withdraw'),
        event_rule_ref=ref('Rule', 'withdraw'), selection_attestation_ref=ref('Attestation', 'withdraw'),
        current_transitions={key.ref.key: None})
    historical = x.resolve_current_as_of(key.ref, as_of_event_ref=first.current_select_event_ref)
    assert historical.selected_release_ref == a.release_ref
    latest = x.resolve_current_as_of(key.ref, as_of_event_ref=x.events[-1].ref)
    assert latest.state == 'NO_CURRENT' and latest.selected_release_ref is None
    restored = B5.from_checkpoint(x.export_checkpoint())
    assert restored.lifecycle_state(a.release_ref).validity == 'WITHDRAWN'

def test_cache_and_rebuild_link_native_local_roundtrip():
    x = B5()
    cached = register(x, replace(subject('cache'), materialization_class='OPTIONAL_CACHE_ACCELERATOR'))
    common = dict(cache_ref=ref('Cache', 'cache'), event_authority_ref=ref('Authority', 'cache'),
                  event_rule_ref=ref('Rule', 'cache'))
    x.record_cache_dropped(cached.release_ref, **common)
    assert x.lifecycle_state(cached.release_ref).payload_materialized is False
    x.record_cache_materialized(cached.release_ref, **common)
    assert x.lifecycle_state(cached.release_ref).payload_materialized is True
    successor = register(x, subject('successor'))
    receipt = x.link_rebuild(cached.release_ref, new_release_ref=successor.release_ref,
        rebuild_state='REBUILT', rebuild_determinant_set_hash=successor.determinant_set_hash,
        replay_or_execution_receipt_ref=ref('ExecutionReceipt', 'rebuild'),
        event_authority_ref=ref('Authority', 'rebuild'), event_rule_ref=ref('Rule', 'rebuild'))
    cp = x.export_checkpoint()
    restored = B5.from_checkpoint(cp)
    assert restored.export_checkpoint() == cp
    assert receipt.ref.key in restored._rebuild_links
