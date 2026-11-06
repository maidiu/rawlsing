"""L01 actual current sourcefree R08/E41 -> N9+N10E -> N10W assertions."""
from dataclasses import replace
import pytest
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_universal_evidence_binding import EvidenceAssociationError
from rawlsing_next.pre553_evidence_world_consumer import configure_evidence_world_context
from rawlsing_next.pre553_universal_world_binding import (
    WorldBindingError, ProgressiveWorldRequest, progressive_world_view,
)
from rawlsing_next.tests.test_l01_reviewed_progressive_world import _progressive_fixture_parts
from rawlsing_next.tests.l01_evidence_world_fixture import admit_readers, evidence_fixture_parts


def build_evidence_world():
    target, conditions, prefixes, world = evidence_fixture_parts()
    readers, resolver, bindings = admit_readers(prefixes, world)
    handle = configure_evidence_world_context(
        target_ref=target, conditions=conditions, prefixes=prefixes,
        world_empirical=world, evidence_readers=readers,
    )
    return handle, readers, resolver, bindings, (target, conditions, prefixes, world)


def view(handle, key='T0'):
    return progressive_world_view(ProgressiveWorldRequest(handle, key))


def test_signed_r08_evidence_reaches_actual_nonparent_numbers_and_world_routes():
    handle, readers, _, _, _ = build_evidence_world()
    selected = view(handle)
    assert selected.state == 'PROGRESSIVE_WORLD_SELECTED_VIEW'
    for step, native, reader in zip(selected.n10e_steps, selected.n10w['world_conditioned_prefixes'], readers):
        assert step['request_key'] == reader.request.key
        assert step['producer_receipt_ref'] == reader.result.producer_receipt_ref.as_dict()
        actual = native['native_material']
        assert actual['state'] == 'OPTIONS_AND_SOURCE_SUPPORT_PRODUCED'
        assert actual['route_probability'] is None
        numbers = actual['source_balance_reads'][0]
        assert numbers['denominator'] == 4
        assert numbers['source_balance_count'] == 4
        assert {c['cell']: c['raw_numerator_support'] for c in numbers['all_alternatives']} == {'0': 0, '1': 4}
        assert {v['channel'] for v in actual['values_read']} == {'structural', 'empirical'}
    later = view(handle, 'T1')
    assert later.world_routes != selected.world_routes
    assert later.n10e_steps == selected.n10e_steps


@pytest.mark.parametrize('mutation', ['condition_value','condition_item','source','edition','permission','clock','model','risk','producer'])
def test_actual_request_mutation_refuses_and_restores(mutation):
    handle, readers, _, _, _ = build_evidence_world()
    original = readers[0].request
    if mutation.startswith('condition'):
        condition = original.ordered_conditions[0]
        if mutation == 'condition_value':
            from rawlsing_next.pre553_universal_evidence_binding import TypedValue
            condition = replace(condition, value=TypedValue.build(0))
        else: condition = replace(condition, occurrence=replace(condition.occurrence, item='C'))
        changed = replace(original, ordered_conditions=(condition,))
    elif mutation in {'risk', 'producer'}:
        changed = replace(original, **{('risk_set_ref' if mutation == 'risk' else 'producer_query_ref'):
            ExactRef('FOREIGN', 'urn:test:foreign', 'f'*64)})
    elif mutation == 'permission': changed = replace(original, permission_ref=ExactRef('DENIED', 'urn:test:denied', 'd'*64))
    elif mutation == 'clock': changed = replace(original, as_of_clock='2099-01-01')
    elif mutation == 'model': changed = replace(original, model_rule_hash='e'*64)
    else: changed = replace(original, **{('source_id' if mutation == 'source' else 'edition'): 'FOREIGN'})
    before = view(handle)
    readers[0].request = changed
    assert view(handle).state == 'REFUSED'
    readers[0].request = original
    assert view(handle).view_hash == before.view_hash


@pytest.mark.parametrize('state', ['ZERO_SUPPORT','UNKNOWN','UNSUPPORTED','VALID_EMPTY'])
def test_status_mutation_never_produces_supported_world(state):
    handle, readers, _, _, _ = build_evidence_world()
    result = readers[0].result
    before = view(handle)
    readers[0].result = replace(result, result_state=state,
        evidence_ref=None, consumer_values_read=None, consumer_result_hash=None,
        typed_refusal='L01_MUTATED_' + state,
        denominator=0 if state == 'ZERO_SUPPORT' else result.denominator)
    assert view(handle).state == 'REFUSED'
    readers[0].result = result
    assert view(handle).view_hash == before.view_hash


def test_wrong_claimed_prefix_condition_cannot_consume_signed_other_value():
    _, readers, _, _, (target, conditions, prefixes, world) = build_evidence_world()
    bad_conditions = ((conditions[0][0], 0), conditions[1])
    bad_prefixes = tuple(replace(prefix, conditions=bad_conditions[:i+1]) for i,prefix in enumerate(prefixes))
    with pytest.raises(WorldBindingError, match='R08_PREFIX_CONDITION_VALUE_MISMATCH'):
        configure_evidence_world_context(target_ref=target, conditions=bad_conditions,
            prefixes=bad_prefixes, world_empirical=world, evidence_readers=readers)


def test_no_signed_reader_or_unknown_handle_cannot_succeed():
    _, _, _, _, (target, conditions, prefixes, world) = build_evidence_world()
    with pytest.raises(WorldBindingError, match='R08_ADMITTED_READER_REQUIRED'):
        configure_evidence_world_context(target_ref=target, conditions=conditions,
            prefixes=prefixes, world_empirical=world, evidence_readers=(None,None))


def test_actual_empty_risk_is_zero_support_and_cannot_become_world_success():
    target, conditions, prefixes, world = evidence_fixture_parts(empty_risk=True)
    readers, _, _ = admit_readers(prefixes, world)
    assert all(reader.result.result_state == 'ZERO_SUPPORT' for reader in readers)
    assert all(reader.result.denominator == 0 for reader in readers)
    with pytest.raises(EvidenceAssociationError):
        configure_evidence_world_context(target_ref=target, conditions=conditions,
            prefixes=prefixes, world_empirical=world, evidence_readers=readers)


def test_actual_missing_structural_authority_is_not_supported(monkeypatch):
    handle, _, _, _, _ = build_evidence_world()
    from rawlsing_next import pre553_universal_world_binding as owner
    catalog = owner._PROGRESSIVE_CONTEXTS[handle].catalog
    original = catalog.read
    def missing_state(snapshot, key):
        material = original(snapshot, key)
        if key == 'training_access': material.pop('state', None)
        return material
    monkeypatch.setattr(catalog, 'read', missing_state)
    assert view(handle).state == 'REFUSED'
    monkeypatch.setattr(catalog, 'read', original)
    assert view(handle).state == 'PROGRESSIVE_WORLD_SELECTED_VIEW'


@pytest.mark.parametrize('mutation', ['condition_item','condition_value','ZERO_SUPPORT','ROUTING_UNKNOWN','empty_risk'])
def test_current_p41_receipt_owner_closes_historical_r53_failures(mutation):
    from copy import deepcopy
    from types import SimpleNamespace
    from rawlsing_next.sourcefree_world.p41_service import P41Service, P41ServiceError
    handle, _, _, _, _ = build_evidence_world()
    selected = view(handle)
    steps = deepcopy(list(selected.n10e_steps))
    ordered = tuple(tuple(condition) for condition in steps[-1]['conditioners'])
    target = steps[0]['target']
    if mutation.startswith('condition'):
        # The supplied step remains actual X=1; the requested identity changes.
        ordered = tuple((('C' if mutation == 'condition_item' else key),
                         ('0' if mutation == 'condition_value' else value))
                        if index == 0 else (key,value)
                        for index,(key,value) in enumerate(ordered))
    elif mutation == 'empty_risk': steps[0]['denominator'] = 0
    else: steps[0]['state'] = mutation
    provider = SimpleNamespace(world={'query_permits': {target: {'target_ref': selected.target_ref.as_dict()}}},
                               progressive=lambda *args: steps, trace=[])
    service = P41Service(provider=provider, readthrough=None)
    with pytest.raises(P41ServiceError): service.progressive(target, ordered)
