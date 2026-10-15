"""E04 author court: numerical and structural products must actually work."""
from pathlib import Path
import sys,copy,json
import pytest
RET=Path(__file__).resolve().parents[1];sys.path[:0]=[str(RET),str(RET/'runtime_root/source')]
from product.service import GenericSelectedWorldService
from product.empirical import GenericProgressiveProvider,build_source
from product.world import SelectedSnapshot
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_empirical_objects import semantic_hash
PROPOSALS=[dict(scenario_id='P_INSTITUTIONAL',route='institutional'),dict(scenario_id='P_CIVIL',route='civil')]

def cells(step):return {c['cell']:c['raw_numerator_support'] for c in step['cells']}
def run(**options):
    service=GenericSelectedWorldService(**options);snapshot=service.select();return service,snapshot,consume(service,snapshot),evaluate(service,snapshot,PROPOSALS)


def test_actual_three_step_geometry_and_same_evidence_f8_consumption():
    s,snap,a,b=run();steps=a['material']['empirical']['steps']
    assert [x['denominator'] for x in steps]==[32,16,8]
    assert [cells(x) for x in steps]==[{'0':14,'1':18},{'0':6,'1':10},{'0':2,'1':6}]
    assert [next(c['raw_probability_exact_fraction']['$exact_fraction'] for c in x['cells'] if c['cell']=='1') for x in steps]==[[9,16],[5,8],[3,4]]
    assert len({semantic_hash(x['release_ref']) for x in steps})==len({semantic_hash(x['risk_set_ref']) for x in steps})==1
    assert [x['binding_order'] for x in steps]==[['a'],['a','b'],['a','b','c']]
    assert all(x['uncertainty']=='UNCERTAINTY_UNQUANTIFIED' for x in steps)
    calls=s.provider.trace;assert any(x['call']=='provide_empirical_possibility_slice' for x in calls) and any(x['call']=='compose_positioned_subject_possibility' for x in calls)
    consumed=[x for x in calls if x['call']=='evaluate_positioned_subject_possibility'];assert len(consumed)==3 and all(x['produced_evidence_ref']==x['consumed_evidence_ref'] and x['same_evidence_object'] for x in consumed)
    assert all(x['state']=='EXACT_SUPPORTED' for x in steps)


def test_numeric_source_intervention_changes_actual_both_consumer_values_not_routes():
    s,snap,a,b=run();t,other,c,d=run(empirical_changed=True)
    assert [cells(x)['1'] for x in c['material']['empirical']['steps']]==[19,11,7]
    assert [x['denominator'] for x in c['material']['empirical']['steps']]==[32,16,8]
    assert a['material']['structural_routes']==c['material']['structural_routes']
    assert [x['source_balance_count'] for x in a['material']['source_balance_reads']]==[4,4,4]
    assert [x['source_balance_count'] for x in c['material']['source_balance_reads']]==[6,6,6]
    assert b['material']['scenarios'][0]['empirical_profiles']!=d['material']['scenarios'][0]['empirical_profiles']
    assert [x['feasibility'] for x in b['material']['scenarios']]==[x['feasibility'] for x in d['material']['scenarios']]


def test_structural_intervention_changes_routes_not_empirical_geometry():
    s,snap,a,b=run();t,other,c,d=run(structural_revision=True)
    assert a['material']['empirical']==c['material']['empirical']
    assert a['material']['structural_routes']['training']['state']=='ELIGIBLE' and c['material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
    assert c['material']['structural_routes']['exit_constraint']['state']=='RESOURCE_CONSTRAINED'
    assert a['material']['structural_routes']['civil']==c['material']['structural_routes']['civil']
    assert b['material']['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE' and d['material']['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
    assert b['material']['scenarios'][1]==d['material']['scenarios'][1]


def test_null_replay_is_bitwise_identical_and_minorities_not_pruned():
    _,_,a,b=run();_,_,c,d=run();assert a==c and b==d
    assert all(min(cells(step).values())>0 for step in a['material']['empirical']['steps'])
    assert a['material']['route_probability'] is None
    assert all(x['selection_weight'] is None for x in b['material']['scenarios'])


def test_irrelevant_native_field_has_no_semantic_dependency_effect():
    _,_,a,b=run();_,_,c,d=run(extra_field=999)
    assert a['material']['empirical']==c['material']['empirical']
    assert a['material']['structural_routes']==c['material']['structural_routes']
    assert b['material']['scenarios']==d['material']['scenarios']
    assert 'unrelated_stock' not in c['material']['dependencies']


def test_real_selected_producer_values_are_read_not_snapshot_ids_only():
    s,snap,a,b=run();trace=s.catalog.trace
    reads=[x for x in trace if x['call'].endswith('producer_payload_read')]
    assert len(reads)==5 and {x['field'] for x in reads}=={'civil_open','civil_sanction','exit_cost','training_access','training_fee'}
    assert all(x['producer_ref']['content_hash'] for x in reads)
    used=a['material']['values_read']+b['material']['values_read']
    assert any(x.get('denominator')==8 and x['value_read'] for x in used)
    assert any(x['scope']=='training_fee' and x['value_read']==2 and x['native_unit']=='modeled resource tokens' for x in used)


def test_current_historical_asof_and_publication_not_observation_clock():
    s=GenericSelectedWorldService(structural_revision=True)
    old=s.select(mode='HISTORICAL',valid_at='2026-09-01',published_asof='2027-09-01')
    delayed=s.select(mode='AS_OF',valid_at='2027-02-01',published_asof='2027-03-01')
    revised=s.select(mode='AS_OF',valid_at='2027-02-01',published_asof='2027-07-01')
    current=s.select(mode='TEST_CURRENT',valid_at='2027-09-01',published_asof='2027-09-01',test_now='2027-09-01')
    assert s.structural(old,'training_access','TEST')['value'] is True
    assert s.structural(delayed,'training_access','TEST')['value'] is True
    assert s.structural(revised,'training_access','TEST')['value'] is False
    assert s.structural(current,'training_access','TEST')['value'] is False
    unavailable=s.select(valid_at='2026-01-15',published_asof='2026-02-01')
    assert s.possibilities(unavailable)['steps']==[]
    assert s.structural(unavailable,'training_access','TEST')['state']=='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
    assert old.material['empirical']['field_time']=='2026-01'


def test_counterfactual_empirical_release_cannot_be_read_before_its_publication():
    s=GenericSelectedWorldService(empirical_changed=True)
    early=s.select(valid_at='2026-05-01',published_asof='2026-03-15')
    late=s.select(valid_at='2026-05-01',published_asof='2026-04-01')
    assert s.possibilities(early)['state']=='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
    assert cells(s.possibilities(late)['steps'][0])['1']==19


def test_permission_revocation_invalidates_only_actual_readsets_retains_history():
    s,snap,a,b=run();civil=evaluate(s,snap,[PROPOSALS[1]]);structural=s.structural_product(snap)
    before=copy.deepcopy(a);r=s.invalidate('training_access')
    assert a['receipt_hash'] in r['invalidated_for_fresh_use'] and b['receipt_hash'] in r['invalidated_for_fresh_use']
    assert civil['receipt_hash'] in r['unaffected'] and structural['receipt_hash'] in r['unaffected']
    current=s.select();result=consume(s,current)
    assert result['material']['structural_routes']['training']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
    assert result['material']['structural_routes']['civil']==a['material']['structural_routes']['civil']
    assert result['material']['empirical']==a['material']['empirical']
    assert current.material['fields']['training_access']['state']=='RESOLUTION_DENIED_OR_NOT_APPLICABLE'
    assert s.historical_receipt(a['receipt_hash'])['material']==before['material'] and s.historical_receipt(a['receipt_hash'])['fresh_use_authorized'] is False
    assert s.structural(snap,'training_access','OLD_SNAPSHOT_REUSE')['state']=='REVOKED'


def test_empirical_revoke_blocks_cached_values_preserves_structural_positive():
    s,snap,a,b=run();structural=s.structural_product(snap);native_calls=len([x for x in s.provider.trace if x['call'].startswith(('compose_','provide_'))])
    r=s.invalidate('empirical');assert structural['receipt_hash'] in r['unaffected']
    updated=consume(s,snap);assert updated['material']['empirical']['state']=='REVOKED' and updated['material']['empirical']['steps']==[]
    assert updated['material']['structural_routes']==a['material']['structural_routes']
    assert len([x for x in s.provider.trace if x['call'].startswith(('compose_','provide_'))])==native_calls
    assert s.historical_receipt(a['receipt_hash'])['material']==a['material']


def test_legal_reverse_is_new_owner_query_not_inverted_number():
    s=GenericSelectedWorldService();snap=s.select()
    forward=s.possibilities(snap,target='Y',conditions=[('A',1)])['steps'][0]
    reverse=s.possibilities(snap,target='A',conditions=[('Y',1)])['steps'][0]
    assert forward['denominator']==32 and reverse['denominator']==29
    assert cells(reverse)=={'0':11,'1':18}
    assert forward['target_ref']!=reverse['target_ref'] and forward['evidence_ref']!=reverse['evidence_ref']


@pytest.mark.parametrize('target,conditions',[('B',[('Y',1)]),('A',[('B',1),('Y',1)]),('Y',[('A',1),('A',1)]),('Y',{('A',1)}),('Y',[('A',True)]),('Y',[])])
def test_unavailable_or_unordered_query_authority_refuses(target,conditions):
    s=GenericSelectedWorldService()
    with pytest.raises(ValueError):s.possibilities(s.select(),target=target,conditions=conditions)


def test_condition_order_is_retained_in_a_new_valid_witness():
    s=GenericSelectedWorldService();snap=s.select()
    a=s.possibilities(snap,conditions=[('A',1),('B',1)])['steps'][-1]
    b=s.possibilities(snap,conditions=[('B',1),('A',1)])['steps'][-1]
    assert a['cells']==b['cells'] and a['denominator']==b['denominator']
    assert a['binding_order']==['a','b'] and b['binding_order']==['b','a'] and a['evidence_ref']!=b['evidence_ref']


@pytest.mark.parametrize('mode,purpose',[('CURRENT','TEST_ONLY_CONTEXT'),('AS_OF','MODEL_USE'),('AS_OF','V3_ACTOR')])
def test_no_operative_clock_or_use_promotion(mode,purpose):
    with pytest.raises(ValueError):GenericSelectedWorldService().select(mode=mode,purpose=purpose)


@pytest.mark.parametrize('value',['2027-9-01','2027-02-30','garbage',None])
def test_malformed_clock_refuses(value):
    with pytest.raises((ValueError,TypeError)):GenericSelectedWorldService().select(valid_at=value)


def test_foreign_tampered_or_rehashed_snapshot_cannot_supply_values():
    s=GenericSelectedWorldService();snap=s.select();t=GenericSelectedWorldService(empirical_changed=True)
    with pytest.raises(ValueError):t.structural(snap,'training_access','TEST')
    fake=copy.deepcopy(snap.material);fake['fields']['training_fee']['value']=999
    with pytest.raises(ValueError):s.structural(SelectedSnapshot(fake,semantic_hash(fake)),'training_fee','TEST')
    snap.material['fields']['training_fee']['value']=123
    with pytest.raises(ValueError):s.structural(snap,'training_fee','TEST')


@pytest.mark.parametrize('bad',[{'scenario_id':'S','route':'civil','desired_child':'X'},{'scenario_id':'S','route':'civil','mother':{}},{'scenario_id':'S','route':'civil','selection_weight':.5}])
def test_scenario_person_or_teleological_inputs_refuse(bad):
    s=GenericSelectedWorldService()
    with pytest.raises(ValueError):evaluate(s,s.select(),[bad])


def test_defensive_copies_and_actor_firewall():
    s,snap,a,b=run();before=s.historical_receipt(a['receipt_hash'])
    a['material']['empirical']['steps'][0]['cells'].clear()
    assert s.historical_receipt(a['receipt_hash'])==before
    for result in (before,b):
        m=result['material'];assert m['actor_executions']==m['model_calls']==0 and not m['operative_N9'] and not m['operative_N10W'] and not m['new_issuer']
    assert not b['material']['person_generation'] and not b['material']['actual_conception']


def test_measured_support_loss_preserves_earlier_positive_steps_and_null():
    s=GenericSelectedWorldService(support_loss=True);p=s.possibilities(s.select())
    assert [x['denominator'] for x in p['steps']]==[24,8,0]
    assert p['steps'][0]['cells'][0]['raw_probability_exact_fraction']['$exact_fraction']==[1,2]
    assert p['steps'][0]['state']==p['steps'][1]['state']=='EXACT_SUPPORTED'
    assert p['steps'][2]['state']=='ZERO_SUPPORT' and p['steps'][2]['geometry'] is None and p['steps'][2]['cells']==[]
    assert p['state']=='PARTIAL_TYPED_EMPIRICAL_SUPPORT'


def test_same_marginal_different_conditional_is_not_flattened():
    s=GenericSelectedWorldService();t=GenericSelectedWorldService(same_marginals=True)
    a=s.possibilities(s.select(),target='A',conditions=[('Y',1)])['steps'][0]
    b=t.possibilities(t.select(),target='A',conditions=[('Y',1)])['steps'][0]
    assert a['denominator']==b['denominator']==29
    assert cells(a)['1']==18 and cells(b)['1']==19
    assert cells(t.possibilities(t.select())['steps'][0])['1']==19


def test_source_query_permission_mutation_cannot_reuse_cached_values():
    s=GenericSelectedWorldService();snap=s.select();s.possibilities(snap)
    s.provider.world['query_permits']['Y']['target_ref']=s.provider.world['source']['qrefs']['A'].as_dict()
    with pytest.raises(ValueError):s.possibilities(snap)


def test_invalid_whole_progressive_request_and_proposal_do_not_read_partial_values():
    s=GenericSelectedWorldService();snap=s.select()
    with pytest.raises(ValueError):s.possibilities(snap,conditions=[('A',1),('A',1)])
    assert s.provider.trace==[] and s.value_reads==[]
    with pytest.raises(ValueError):evaluate(s,snap,[dict(scenario_id='S',route='civil',mother='UNAUTHORIZED')])
    assert s.provider.trace==[] and s.value_reads==[]


def test_generic_facade_uses_explicit_native_role_data_not_abc_names():
    from product import empirical as e
    aliases={'A':'POSITION_CODE','B':'GROUP_CODE','C':'CONTEXT_CODE','Y':'RESPONSE_CODE'}
    rows=e.e03.synthetic_world_rows()
    for row in rows:row['responses']={aliases[k]:v for k,v in row['responses'].items()}
    tag='e04-generic-renamed-native';source=e.fx._build_source(tag,rows,question_namespace=tag,risk_sets={'R_ALL':{q:{r['id'] for r in rows} for q in aliases.values()}},risk_namespace=tag);source['risk_refs']['R']=source['risk_refs']['R_ALL']
    authority=e.fx._query_authority(tag)
    world=dict(tag=tag,source=source,qauth=authority,registry=e.fx._registry(source,authority),pairing=e.c1.make_pairing_authority(tag),model_rule=e.c1.make_model_rule(source['universe'].ref,tag),permission_root='TEST_ONLY_E04_SOURCE_ROOT')
    world['query_permits']={target:dict(target_ref=source['qrefs'][target].as_dict(),conditioner_refs={q:source['qrefs'][q].as_dict() for q in conditions},allowed_values=[0,1],max_conditioners=len(conditions),scope='TEST_ONLY_EXACT_QUERY_ROLES') for target,conditions in [('RESPONSE_CODE',['POSITION_CODE','GROUP_CODE','CONTEXT_CODE']),('POSITION_CODE',['RESPONSE_CODE'])]}
    provider=GenericProgressiveProvider(world)
    forward=provider.step('RESPONSE_CODE',[('POSITION_CODE',1),('GROUP_CODE',1)])
    reverse=provider.step('POSITION_CODE',[('RESPONSE_CODE',1)])
    assert forward['state']=='EXACT_SUPPORTED' and forward['denominator']==16 and cells(forward)=={'0':6,'1':10}
    assert reverse['denominator']==29 and cells(reverse)=={'0':11,'1':18}
    assert forward['target_ref']==source['qrefs']['RESPONSE_CODE'].as_dict()


def test_partial_upstream_is_not_reported_as_complete_product():
    s=GenericSelectedWorldService();snap=s.select();s.invalidate('empirical')
    assert consume(s,snap)['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    assert evaluate(s,snap,PROPOSALS)['material']['state']=='PARTIAL_PROPOSALS_EVALUATED'
    t=GenericSelectedWorldService(support_loss=True);part=consume(t,t.select())['material']
    assert part['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    assert part['source_balance_reads'][-1]['source_balance_count'] is None and part['source_balance_reads'][-1]['source_balance_null_reason']
    with pytest.raises(ValueError):t.structural_product(t.select(),keys=())


def test_sanction_only_intervention_is_selective_and_not_empirical():
    _,_,base,proposals=run();_,_,changed,other=run(sanction_revision=True)
    a=base['material'];b=changed['material']
    assert a['empirical']==b['empirical']
    assert a['structural_routes']['training']==b['structural_routes']['training'] and a['structural_routes']['exit_constraint']==b['structural_routes']['exit_constraint']
    assert a['structural_routes']['civil']['state']=='ELIGIBLE' and b['structural_routes']['civil']['state']=='BLOCKED_BY_MODELED_RULE'
    assert proposals['material']['scenarios'][0]==other['material']['scenarios'][0]
    assert other['material']['scenarios'][1]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
