"""Frozen native-consumer claims and upstream severance controls."""
import json
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
import pytest
import bootstrap
from world_join import SelectedWorld, t35
from fixture import ref
from product.nonparent import consume
from rawlsing_next import pre553_empirical_query as pq

FROZEN=json.loads((Path(__file__).parent/'01_FROZEN_EXPECTATIONS.json').read_text())
def cell_counts(output):
    return [{c['cell']:c['raw_numerator_support'] for c in s['cells']}
            for s in output['material']['empirical']['steps']]

def attempt(world, snapshot):
    try:
        return {'state':'PRODUCT', 'result':consume(world.service,snapshot)}
    except ValueError as exc:
        return {'state':'REFUSED', 'reason':str(exc)}

def test_actual_selected_release_reaches_original_consumer():
    w=SelectedWorld();snapshot=w.snapshot(t35.E1)
    value=attempt(w,snapshot)
    assert value['state']=='PRODUCT', 'SELECTED_RELEASE_TO_ORIGINAL_CONSUMER_NOT_PRODUCTIVE'
    output=value['result']
    assert cell_counts(output)==FROZEN['base_cells']
    assert [s['denominator'] for s in output['material']['empirical']['steps']]==FROZEN['denominators']
    reads=[r for r in output['material']['values_read'] if r['channel']=='empirical']
    assert len(reads)==3
    for read,step in zip(reads,output['material']['empirical']['steps']):
        assert read['learned_release_binding']['learned_release_ref']==snapshot.material['empirical']['selected_learned_product']['release_ref']
        assert read['value_read']==step['cells']
        assert step['source_universe_ref']==snapshot.material['empirical']['source_universe_ref']
    assert w.service.catalog.empirical is w.service.provider.world

def test_two_epochs_original_training_observable():
    w=SelectedWorld();a=w.epoch(t35.E1);b=w.epoch(t35.E2)
    for year,out in [('2026',a),('2027',b)]:
        expected=FROZEN['epochs'][year];m=out['nonparent']['material'];slots=out['snapshot']['fields']
        assert m['structural_routes']['training']['state']==expected['training']
        assert m['structural_routes']['exit_constraint']['state']==expected['exit_constraint']
        assert m['structural_routes']['civil']['state']==FROZEN['civil']
        for key in ('training_access','training_fee','exit_cost'):
            assert slots[key]['value']==expected[key]
    assert a['nonparent']['material']['empirical']==b['nonparent']['material']['empirical']
    assert a['learned_binding']==b['learned_binding']
    assert a['snapshot']['empirical']==b['snapshot']['empirical']
    assert b['snapshot']['fields']['training_fee']['payload']['publication']=='2027-06-01'
    assert b['snapshot']['fields']['training_fee']['payload']['effective_from']=='2027-01-01'

def test_named_m4_m5_structural_owner_reaches_original_consumer():
    w=SelectedWorld();out=w.epoch(t35.E2);m=out['nonparent']['material']
    assert m['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE', 'STRUCTURAL_OWNER_NOT_CONSUMED'
    assert m['state']=='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED'
    for key,slot in out['snapshot']['fields'].items():
        assert slot['state']=='SUPPORTED_TEST_ONLY'
        assert slot['rsc_ref']['kind']=='SCR5578_RESOLVED_STRUCTURAL_CONTEXT@1.0.0'
        read=next(r for r in m['values_read'] if r['channel']=='structural' and r['scope']==key)
        assert read['source_ref']==slot['field_ref']
        assert read['value_read']==slot['value']
    assert any(r['call']=='resolve_v558' for r in out['structural_trace'])
    assert any(r['call']=='materialize_resolved_structural_context+validate_resolved_structural_context+producer_payload_read' for r in out['structural_trace'])

def test_remove_selected_release_refuses_and_restores_without_source_fallback():
    w=SelectedWorld();snapshot=w.snapshot(t35.E2);first=attempt(w,snapshot)
    p=w.prepared;source_before=deepcopy(p.native_provider.world['rows_hash']);rules_before=deepcopy(w.service.catalog.records)
    selected=p.composition.m2_artifacts.release
    p.repository._releases.clear()
    failed=attempt(w,snapshot)
    assert failed['state']=='REFUSED'
    assert 'release' in failed['reason'].lower()
    assert source_before==p.native_provider.world['rows_hash']
    assert rules_before==w.service.catalog.records
    p.repository.register_release(selected)
    assert attempt(w,snapshot)==first

def test_rule_only_same_clock_control():
    a=SelectedWorld(rules='base').epoch(t35.E2)
    b=SelectedWorld().epoch(t35.E2)
    assert a['nonparent']['material']['structural_routes']['training']['state']=='ELIGIBLE'
    assert b['nonparent']['material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
    assert a['learned_binding']==b['learned_binding']
    assert a['nonparent']['material']['empirical']==b['nonparent']['material']['empirical']
    assert a['snapshot']['empirical']==b['snapshot']['empirical']

def test_release_selection_changes_empirical_with_rules_fixed():
    a=SelectedWorld()
    a.stage_release('alternate')
    sources={name:p.native_provider.world['rows_hash'] for name,p in a.release_bank.items()}
    left=a.epoch(t35.E2)
    catalog=a.service.catalog
    a.select_release('alternate')
    right=a.epoch(t35.E2)
    assert a.service.catalog is catalog
    assert sources=={name:p.native_provider.world['rows_hash'] for name,p in a.release_bank.items()}
    assert cell_counts(left['nonparent'])==FROZEN['base_cells']
    assert cell_counts(right['nonparent'])==FROZEN['alternate_cells']
    assert left['learned_binding']['release_ref']!=right['learned_binding']['release_ref']
    assert left['snapshot']['fields']==right['snapshot']['fields']
    assert left['nonparent']['material']['structural_routes']==right['nonparent']['material']['structural_routes']

def test_no_native_recomputation_or_cache_fallback():
    w=SelectedWorld();p=w.prepared;snapshot=w.snapshot(t35.E2)
    with patch.object(p.native_provider,'step',side_effect=AssertionError('NATIVE_SOURCE_RECOMPUTED')),patch.object(pq,'execute_empirical_query',side_effect=AssertionError('NATIVE_SOURCE_RECOMPUTED')):
        out=consume(w.service,snapshot)
    assert cell_counts(out)==FROZEN['base_cells']
    assert [x['call'] for x in w.service.provider.trace]==['SELECTED_RELEASE_FACT_VALUES_READ']*3

def test_withdrawn_historical_evidence_is_archival_never_fresh():
    w=SelectedWorld();snapshot=w.snapshot(t35.E1);out=consume(w.service,snapshot)
    p=w.prepared;s=p.composition.b5_selection_receipt;checkpoint=p.lifecycle.export_checkpoint()
    p.lifecycle.withdraw_product(s.selected_release_ref,withdrawal_reason_ref=ref('Reason','revoke'),withdrawal_scope_ref=p.contract.selection_scope_ref,event_authority_ref=ref('LifecycleAuthority','withdraw'),event_rule_ref=ref('LifecycleRule','withdraw'),selection_attestation_ref=ref('SelectionAttestation','withdraw'),current_transitions={s.selection_key_ref.key:None})
    assert attempt(w,snapshot)['state']=='REFUSED'
    assert p.lifecycle.resolve_current_as_of(s.selection_key_ref,as_of_checkpoint=checkpoint).selected_release_ref==s.selected_release_ref
    archive=w.service.historical_receipt(out['receipt_hash'])
    assert archive['material']==out['material']
    assert archive['archival_only'] is True
    assert archive['fresh_use_authorized'] is False
    assert attempt(w,w.snapshot(t35.E1))['state']=='REFUSED'

def test_publication_effective_and_current_clocks_are_distinct():
    w=SelectedWorld()
    for valid,pub,fee in [('2027-09-01','2027-05-31',2),('2027-09-01','2027-06-01',6),('2026-12-31','2027-09-01',2),('2027-01-01','2027-06-01',6)]:
        out=w.epoch(t35.clock('AS_OF',valid,pub))
        assert out['snapshot']['fields']['training_fee']['value']==fee
    with pytest.raises(ValueError,match='EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED'):
        t35.clock('TEST_CURRENT','2026-06-01','2027-09-01',test_now='2027-09-01')

def test_r13_zero_support_and_permission_holds():
    w=SelectedWorld(support_loss=True);out=w.epoch(t35.E2)
    last=out['nonparent']['material']['empirical']['steps'][-1]
    assert last['state']=='ZERO_SUPPORT' and last['denominator']==0 and last['cells']==[]
    assert out['nonparent']['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    assert out['acceptance']['contract']=='R13_E05R_N9_SELECTED_WORLD_INTERFACE@2'
    assert out['proposal']=={'state':'HOLD','reason':'TEST_ONLY_CONSUMER_PERMISSION_UNAVAILABLE','consumer':'CONCEPTION_SCENARIO_PROPOSALS'}
    assert out['F6P']['join']=='NO_AUTHORIZED_JOIN'
    assert out['nonparent']['material']['route_probability'] is None
    assert out['nonparent']['material']['actor_executions']==0
    # The R13 receipt itself is unavailable: its exact consumer purpose is held.
    request=t35.make_request(t35.E2);snapshot=w.adapter.build_snapshot(request);acceptance=w.adapter.accept(request,snapshot)
    with pytest.raises(ValueError,match='TEST_ONLY_CONSUMER_PERMISSION_UNAVAILABLE'):
        w.adapter.serve(request,acceptance,snapshot)

@pytest.mark.parametrize('fault', ['remove', 'substitute'])
def test_live_structural_owner_change_refuses_old_snapshot_and_restores(fault):
    w=SelectedWorld();snapshot=w.snapshot(t35.E2);before=attempt(w,snapshot)
    catalog=w.service.catalog
    ref_hash=snapshot.material['fields']['training_fee']['field_ref']['content_hash']
    owner=catalog.handles[ref_hash]
    source=deepcopy(snapshot.material['empirical'])
    if fault=='remove':
        catalog.handles.pop(ref_hash)
    else:
        other_hash=snapshot.material['fields']['civil_open']['field_ref']['content_hash']
        catalog.handles[ref_hash]=catalog.handles[other_hash]
    assert attempt(w,snapshot)['state']=='REFUSED'
    assert snapshot.material['empirical']==source
    catalog.handles[ref_hash]=owner
    assert attempt(w,snapshot)==before
