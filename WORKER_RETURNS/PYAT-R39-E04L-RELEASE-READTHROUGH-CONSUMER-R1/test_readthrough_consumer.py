"""Frozen positive and direct selected-release dependency falsifiers."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bootstrap
from copy import deepcopy
from unittest.mock import patch
import pytest
from fixture import prepare,ref,CONDITIONS
from readthrough import ReadThroughService,ReadThroughError
from product.nonparent import consume
from rawlsing_next.pre553_empirical_objects import canonicalize,semantic_hash
import rawlsing_next.pre553_empirical_query as pq

def cells(receipt):return [{x['cell']:x['raw_numerator_support'] for x in s['cells']} for s in receipt['material']['empirical']['steps']]
def sever_and_restore(p,service):
    original=p.composition.m2_artifacts.release
    before=semantic_hash(p.native_provider.world['rows_hash'])
    p.repository._releases.clear()
    refused=False
    try:consume(service,p.snapshot)
    except ValueError:refused=True
    assert refused,'RELEASE_EDGE_SEVERED_BUT_ORIGINAL_CONSUMER_STILL_PRODUCTIVE'
    assert semantic_hash(p.native_provider.world['rows_hash'])==before
    p.repository.register_release(original)

def test_selected_release_drives_original_consumer_and_severance():
    p=prepare();service=ReadThroughService(p);first=consume(service,p.snapshot)
    assert cells(first)==[{'0':14,'1':18},{'0':6,'1':10},{'0':2,'1':6}]
    assert [s['denominator'] for s in first['material']['empirical']['steps']]==[32,16,8]
    empirical=[x for x in first['material']['values_read'] if x['channel']=='empirical']
    assert len(empirical)==3
    for read in empirical:
        binding=read['learned_release_binding']
        assert binding['learned_release_ref']==p.composition.b5_selection_receipt.selected_release_ref.as_dict()
        assert binding['m1_subject_ref']==p.composition.m1_disposition.ref.as_dict()
        assert binding['producer_fact_ref'] in [x.as_dict() for x in p.composition.m1_disposition.empirical_fact_refs]
        assert read['value_read']==first['material']['empirical']['steps'][empirical.index(read)]['cells']
    sever_and_restore(p,service)
    restored=consume(service,p.snapshot)
    assert restored==first

def test_original_source_cache_is_not_read_after_release():
    p=prepare();service=ReadThroughService(p)
    before=deepcopy(p.native_provider.trace)
    with patch.object(p.native_provider,'step',side_effect=AssertionError('SOURCE_RECOMPUTED')),patch.object(p.native_provider,'progressive',side_effect=AssertionError('SOURCE_CACHE_FALLBACK')),patch.object(pq,'execute_empirical_query',side_effect=AssertionError('SOURCE_RECOMPUTED')):
        result=consume(service,p.snapshot)
    assert cells(result)[-1]=={'0':2,'1':6}
    assert p.native_provider.trace==before
    assert [x['call'] for x in service.provider.trace]==['SELECTED_RELEASE_FACT_VALUES_READ']*3

def test_changed_joint_same_marginals_preserves_structural_routes():
    a=prepare();b=prepare(same_marginals=True)
    left=consume(ReadThroughService(a),a.snapshot);right=consume(ReadThroughService(b),b.snapshot)
    assert cells(right)==[{'0':13,'1':19},{'0':5,'1':11},{'0':1,'1':7}]
    assert cells(left)!=cells(right)
    assert left['material']['structural_routes']==right['material']['structural_routes']
    assert a.composition.m2_artifacts.release.ref!=b.composition.m2_artifacts.release.ref
    assert left['material']['route_probability'] is None and right['material']['route_probability'] is None

@pytest.mark.parametrize('fault',['release','subject','missing_fact','catalog_identity','predicate','query','template_denominator','template_target','risk_identity','source_person','permission'])
def test_hostile_readthrough_binding_refusals(fault):
    p=prepare();service=ReadThroughService(p);provider=service.provider
    key=('Y',CONDITIONS);record=provider.records[key]
    if fault=='release':provider.expected_release=ref('LearnedProductReleaseCore','forged')
    elif fault=='subject':provider.expected_subject=ref('LearnedEmpiricalDisposition','wrong-root')
    elif fault=='missing_fact':provider.catalog.objects.pop(record['fact_ref'].key)
    elif fault=='catalog_identity':provider.catalog.objects[record['fact_ref'].key]=provider.catalog.get(provider.records[('Y',CONDITIONS[:1])]['fact_ref'])
    elif fault in ('predicate','query'):record[fault+'_ref']=provider.records[('Y',CONDITIONS[:1])][fault+'_ref']
    else:
        template=record['template']
        if fault=='template_denominator':template['denominator']=9
        elif fault=='template_target':template['target']='B'
        elif fault=='risk_identity':template['risk_set_ref']=ref('RiskSet','changed').as_dict()
        elif fault=='source_person':template['source_universe_ref']=ref('EmpiricalUniverse','other-person-source').as_dict()
        else:template['permission_root']='PRODUCTION_OR_ACTOR'
        record['template_hash']=semantic_hash(template)
    with pytest.raises(ValueError):consume(service,p.snapshot)

def test_revocation_current_and_historical_have_distinct_use():
    p=prepare();service=ReadThroughService(p);first=consume(service,p.snapshot)
    checkpoint=p.lifecycle.export_checkpoint();selected=p.composition.b5_selection_receipt
    p.lifecycle.withdraw_product(selected.selected_release_ref,withdrawal_reason_ref=ref('Reason','revoke'),withdrawal_scope_ref=p.contract.selection_scope_ref,event_authority_ref=ref('LifecycleAuthority','withdraw'),event_rule_ref=ref('LifecycleRule','withdraw'),selection_attestation_ref=ref('SelectionAttestation','withdraw'),current_transitions={selected.selection_key_ref.key:None})
    with pytest.raises(ValueError):consume(service,p.snapshot)
    history=p.lifecycle.resolve_current_as_of(selected.selection_key_ref,as_of_checkpoint=checkpoint)
    assert history.selected_release_ref==selected.selected_release_ref
    archived=service.historical_receipt(first['receipt_hash'])
    assert archived['material']==first['material'] and archived['fresh_use_authorized'] is False

def test_stale_selection_cache_replay_refuses():
    p=prepare();service=ReadThroughService(p);first=consume(service,p.snapshot)
    selected=p.composition.b5_selection_receipt
    p.lifecycle.declare_no_current(selected.selection_key_ref,expected_previous_receipt_ref=selected.ref,event_authority_ref=ref('LifecycleAuthority','none'),event_rule_ref=ref('LifecycleRule','none'),reason_ref=ref('Reason','none'),selection_attestation_ref=ref('SelectionAttestation','none'))
    with pytest.raises(ValueError):consume(service,p.snapshot)
    assert service.historical_receipt(first['receipt_hash'])['archival_only'] is True

def test_roles_minorities_same_person_and_denominator_members():
    p=prepare();service=ReadThroughService(p);result=consume(service,p.snapshot)
    for step in result['material']['empirical']['steps']:
        fact=service.provider.catalog.get(p.records[(step['target'],tuple(map(tuple,step['conditioners'])))]['fact_ref'])
        members=canonicalize(fact.denominator_member_refs)
        assert len(members)==step['denominator'] and len({semantic_hash(x) for x in members})==len(members)
        assert all(x['raw_numerator_support']>0 for x in step['cells'])
    with pytest.raises(ValueError,match='TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE'):service.provider.progressive('B',(('A',1),))
    with pytest.raises(ValueError,match='RELEASE_QUERY_NOT_INCLUDED'):service.provider.progressive('A',(('Y',1),))

def test_zero_support_is_not_null_and_absent_artifact_is_not_zero():
    p=prepare(support_loss=True);service=ReadThroughService(p);receipt=consume(service,p.snapshot)
    last=receipt['material']['empirical']['steps'][-1]
    assert last['state']=='ZERO_SUPPORT' and last['denominator']==0 and last['cells']==[]
    assert receipt['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    fact_ref=p.records[('Y',CONDITIONS)]['fact_ref'];service.provider.catalog.objects.pop(fact_ref.key)
    with pytest.raises(ValueError,match='PRODUCER_OBJECT_UNAVAILABLE'):consume(service,p.snapshot)

def test_measured_null_is_a_product_and_permission_ceiling_remains():
    p=prepare(measured_null=True);service=ReadThroughService(p);receipt=consume(service,p.snapshot)
    assert cells(receipt)==[{'0':16,'1':16},{'0':8,'1':8},{'0':4,'1':4}]
    assert [x['source_balance_count'] for x in receipt['material']['source_balance_reads']]==[0,0,0]
    assert receipt['material']['state']=='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED'
    assert receipt['material']['new_issuer'] is False
    assert receipt['material']['actor_executions']==0 and receipt['material']['model_calls']==0
    assert receipt['material']['route_probability_reason']=='NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL'
    assert p.composition.receipt.side_effects['consumer_permission_effect'] is False
    with pytest.raises(ValueError,match='TEST_ONLY_CONSUMER_PERMISSION_UNAVAILABLE'):service.possibilities(p.snapshot,consumer='SOROK_ACTOR')

def test_source_permission_revocation_cannot_be_overridden_by_release():
    p=prepare();service=ReadThroughService(p);service.catalog.revoke('empirical')
    result=consume(service,p.snapshot)
    assert result['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    assert result['material']['empirical']['steps']==[]

def test_actual_producer_preimage_tamper_refuses_even_with_old_identity():
    p=prepare();service=ReadThroughService(p);provider=service.provider
    fact=provider.catalog.get(p.records[('Y',CONDITIONS)]['fact_ref'])
    fields=dict(fact.semantic_fields);fields['raw_denominator_support']=9
    object.__setattr__(fact,'_semantic_fields',fields)
    with pytest.raises(ValueError,match='PRODUCER_PREIMAGE_MISMATCH'):consume(service,p.snapshot)

def test_forged_catalog_object_cannot_supply_a_self_asserted_identity():
    from types import SimpleNamespace
    p=prepare();service=ReadThroughService(p);provider=service.provider
    reference=p.records[('Y',CONDITIONS)]['fact_ref']
    provider.catalog.objects[reference.key]=SimpleNamespace(ref=reference)
    with pytest.raises(ValueError,match='PRODUCER_OBJECT_TYPE_MISMATCH'):consume(service,p.snapshot)
