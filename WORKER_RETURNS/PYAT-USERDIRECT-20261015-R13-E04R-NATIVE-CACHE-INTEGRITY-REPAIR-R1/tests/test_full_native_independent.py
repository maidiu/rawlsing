"""E04N independent full-native court. No E04I doubles imported."""
from common import *
import pytest
@pytest.fixture(scope='module')
def baseline():return full()

def test_preserved_independent_58_row_oracle_matches_actual_native(baseline):
 s,snap,a,b=baseline;data=independent_rows();assert len(data)==58
 for n,step in enumerate(a['material']['empirical']['steps'],1):
  assert geometry(step)==direct(data,'Y',[('A',1),('B',1),('C',1)][:n])
 assert [geometry(x)['cells']['1'] for x in a['material']['empirical']['steps']]==[18,10,6]
 assert [x['denominator'] for x in a['material']['empirical']['steps']]==[32,16,8]
 assert snap.snapshot_hash==a['material']['snapshot_ref']==b['material']['snapshot_ref']
 assert len({json.dumps(x['release_ref'],sort_keys=True) for x in a['material']['empirical']['steps']})==1
 assert all(x['authority_refs'] and x['provenance_refs'] and x['condition_witness_ref'] and x['producer_fact_ref'] for x in a['material']['empirical']['steps'])

def test_both_real_clients_read_all_values_and_minorities(baseline):
 s,snap,a,b=baseline
 assert a['material']['consumer']=='NONPARENT_OPTIONS' and b['material']['consumer']=='CONCEPTION_SCENARIO_PROPOSALS'
 assert [x['source_balance_count'] for x in a['material']['source_balance_reads']]==[4,4,4]
 for step in a['material']['empirical']['steps']:assert geometry(step)['cells']['0']>0 and geometry(step)['cells']['1']>0
 assert b['material']['scenarios'][0]['empirical_profiles']==b['material']['scenarios'][1]['empirical_profiles']
 assert len([x for x in s.catalog.trace if x['call'].endswith('producer_payload_read')])==5

def test_actual_empirical_mutation_independently_reaggregated(baseline):
 _,_,a,b=baseline;t,other,c,d=full(empirical_changed=True);rows=independent_rows();next(r for r in rows if all(r[q]==1 for q in 'ABC') and r['Y']==0)['Y']=1
 for n,step in enumerate(c['material']['empirical']['steps'],1):assert geometry(step)==direct(rows,'Y',[('A',1),('B',1),('C',1)][:n])
 assert [geometry(x)['cells']['1'] for x in c['material']['empirical']['steps']]==[19,11,7]
 assert a['material']['structural_routes']==c['material']['structural_routes']
 assert a['material']['empirical']!=c['material']['empirical'] and b['material']['scenarios'][0]['empirical_profiles']!=d['material']['scenarios'][0]['empirical_profiles']

def test_structural_access_exit_revision_changes_only_routes(baseline):
 _,_,a,b=baseline;t,ss,c,d=full(structural_revision=True)
 assert a['material']['empirical']==c['material']['empirical']
 assert c['material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert c['material']['structural_routes']['exit_constraint']['state']=='RESOURCE_CONSTRAINED'
 assert a['material']['structural_routes']['civil']==c['material']['structural_routes']['civil']
 assert b['material']['scenarios'][1]==d['material']['scenarios'][1]

def test_structural_sanction_revision_only_civil_changes(baseline):
 _,_,a,b=baseline;_,_,c,d=full(sanction_revision=True)
 assert a['material']['empirical']==c['material']['empirical']
 assert a['material']['structural_routes']['training']==c['material']['structural_routes']['training']
 assert c['material']['structural_routes']['civil']['state']=='BLOCKED_BY_MODELED_RULE'
 assert b['material']['scenarios'][0]==d['material']['scenarios'][0]

def test_fee_leaf_alone_uses_real_M4_M5_and_not_probability(baseline):
 s=GenericSelectedWorldService();s.catalog._publish('training_fee',9,'2027-01-01','2028-01-01','2027-06-01',revision=2)
 # Reviewer-authorised modeled structural intervention, not an empirical/source grant.
 s.catalog.catalog_hash=semantic_hash(dict(records=s.catalog.records,empirical=s.catalog.empirical_identity()));snap=s.select();a=consume(s,snap)
 assert a['material']['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
 assert a['material']['empirical']==baseline[2]['material']['empirical']
 assert a['material']['route_probability'] is None

def test_unrelated_and_null_inputs_do_not_change_dependent_results(baseline):
 _,_,a,b=baseline;_,_,c,d=full(extra_field=123456);_,_,e,f=full()
 assert a==e and b==f
 assert a['material']['empirical']==c['material']['empirical']
 assert a['material']['structural_routes']==c['material']['structural_routes'] and b['material']['scenarios']==d['material']['scenarios']

def test_empirical_structural_disjoint_effects_compose(baseline):
 _,_,emp_a,emp_b=full(empirical_changed=True);_,_,struct_a,struct_b=full(structural_revision=True);_,_,joint_a,joint_b=full(empirical_changed=True,structural_revision=True)
 assert joint_a['material']['empirical']==emp_a['material']['empirical']
 assert joint_a['material']['structural_routes']==struct_a['material']['structural_routes']
 assert [p['feasibility'] for p in joint_b['material']['scenarios']]==[p['feasibility'] for p in struct_b['material']['scenarios']]
 assert [p['empirical_profiles'] for p in joint_b['material']['scenarios']]==[p['empirical_profiles'] for p in emp_b['material']['scenarios']]

def test_real_ZERO_SUPPORT_at_depth3_has_no_probability():
 s,ss,a,b=full(support_loss=True);steps=a['material']['empirical']['steps']
 assert [x['denominator'] for x in steps]==[24,8,0]
 assert steps[-1]['state']=='ZERO_SUPPORT' and steps[-1]['geometry'] is None and steps[-1]['cells']==[]
 assert a['material']['source_balance_reads'][-1]['source_balance_count'] is None
 assert a['material']['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
 assert steps[0]['cells'][0]['raw_probability_exact_fraction']['$exact_fraction']==[1,2]

def test_reverse_is_separately_bound_real_18_over29(baseline):
 s,snap,a,b=baseline;r=s.possibilities(snap,target='A',conditions=(('Y',1),))['steps'][0]
 assert geometry(r)==direct(independent_rows(),'A',[('Y',1)])
 assert r['denominator']==29 and geometry(r)['cells']['1']==18
 assert r['producer_query_ref']!=a['material']['empirical']['steps'][0]['producer_query_ref']

@pytest.mark.parametrize('target,conditions',[('B',[('Y',1)]),('A',[('B',1)]),('Y',[('A',2)]),('Y',[('A',True)]),('Y',[('A','1')]),('Y',[('A',1),('A',1)]),('Y',[]),('Y',{('A',1)})])
def test_reverse_dyad_unsupported_value_or_order_refuses(target,conditions):
 s=GenericSelectedWorldService()
 with pytest.raises(ValueError):s.possibilities(s.select(),target=target,conditions=conditions)
 assert not s.provider.trace

@pytest.mark.parametrize('field',['permission_root','query_permits','release','risk','native_domain'])
def test_post_binding_source_role_rekeys_cannot_reuse_cache(field):
 s,ss,a,b=full();w=s.provider.world
 if field=='permission_root':w['permission_root']='SELF_ISSUED'
 elif field=='query_permits':w['query_permits']['Y']['scope']='SELF_ISSUED_REVERSE'
 elif field=='release':w['source']['release_ref']=w['source']['universe'].ref
 elif field=='risk':w['source']['risk_refs']['R']=w['source']['qrefs']['A']
 else:w['query_permits']['Y']['allowed_values']=[0,1,777]
 with pytest.raises(ValueError):s.possibilities(ss)

@pytest.mark.parametrize('key',['source_universe_ref','release_ref','risk_set_ref','permission_root','rows_hash'])
def test_coherently_rehashed_snapshot_source_rekey_refuses(baseline,key):
 s,snap,_,_=baseline;fake=deepcopy(snap.material);fake['empirical'][key]={'foreign':'PV2I'} if key.endswith('_ref') else 'FOREIGN_REISSUED';new=SelectedSnapshot(fake,semantic_hash(fake))
 with pytest.raises(ValueError):s.possibilities(new)

@pytest.mark.parametrize('key',['currentness_ref','rsc_ref','field_ref','value'])
def test_wrong_structural_currentness_snapshot_refuses(baseline,key):
 s,snap,_,_=baseline;fake=deepcopy(snap.material);fake['fields']['training_access'][key]={'foreign':'E04N'} if key!='value' else False
 with pytest.raises(ValueError):s.structural(SelectedSnapshot(fake,semantic_hash(fake)),'training_access','HOSTILE')

def test_publication_and_effective_clocks_actual_native_reads():
 s=GenericSelectedWorldService(structural_revision=True)
 for valid,published,expected in [('2026-09-01','2027-09-01',True),('2027-02-01','2027-03-01',True),('2027-02-01','2027-07-01',False)]:
  snap=s.select(valid_at=valid,published_asof=published);assert s.structural(snap,'training_access','CLOCK')['value'] is expected
 early=s.select(valid_at='2026-01-15',published_asof='2026-02-01');assert not s.possibilities(early)['steps']

@pytest.mark.parametrize('mode,purpose',[('CURRENT','TEST_ONLY_CONTEXT'),('AS_OF','OPERATIVE_N9'),('AS_OF','V3_ACTOR'),('AS_OF','MODEL_USE')])
def test_no_world_CURRENT_or_use_promotion(mode,purpose):
 with pytest.raises(ValueError):GenericSelectedWorldService().select(mode=mode,purpose=purpose)

def test_empirical_revocation_blocks_old_cache_and_keeps_structure():
 s,ss,a,b=full();history=s.historical_receipt(a['receipt_hash']);r=s.invalidate('empirical');fresh=consume(s,ss)
 assert fresh['material']['empirical']['state']=='REVOKED' and not fresh['material']['empirical']['steps']
 assert fresh['material']['structural_routes']==a['material']['structural_routes']
 assert s.historical_receipt(a['receipt_hash'])==history and not history['fresh_use_authorized']

def test_structural_revoke_is_selective_and_historical_copy_stable():
 s,ss,a,b=full();civil=evaluate(s,ss,[PROPOSALS[1]]);pure=s.structural_product(ss);history=s.historical_receipt(a['receipt_hash']);r=s.invalidate('training_access')
 assert civil['receipt_hash'] in r['unaffected'] and pure['receipt_hash'] in r['unaffected']
 assert s.structural(ss,'training_access','OLD')['state']=='REVOKED'
 assert s.possibilities(ss)==a['material']['empirical']
 assert s.historical_receipt(a['receipt_hash'])==history

@pytest.mark.parametrize('field',['person','mother','father','child','family','genealogy','traits','desired_child','selection_weight','dyad_probability'])
def test_no_person_family_trait_selection_input(field):
 s=GenericSelectedWorldService();ss=s.select()
 with pytest.raises(ValueError):evaluate(s,ss,[dict(scenario_id='hostile',route='civil',**{field:'UNSUPPORTED'})])
 assert s.value_reads==[] and s.provider.trace==[]

def test_cache_payload_corruption_cannot_reach_both_consumers():
 s,ss,a,b=full();key=('Y',(('A',1),));s.provider.cache[key]['cells'][1]['raw_numerator_support']=999
 try:
  changed=consume(s,ss);other=evaluate(s,ss,PROPOSALS)
 except ValueError:return
 assert geometry(changed['material']['empirical']['steps'][0])==geometry(a['material']['empirical']['steps'][0]), 'Corrupted cache delivers999 support through real client with original evidence/content hash'

def test_cached_foreign_release_cannot_bypass_snapshot_binding():
 s,ss,a,b=full();key=('Y',(('A',1),));s.provider.cache[key]['release_ref']={'kind':'C11LogicalRelease','object_id':'urn:foreign:release','content_hash':'f'*64}
 with pytest.raises(ValueError):s.possibilities(ss)
