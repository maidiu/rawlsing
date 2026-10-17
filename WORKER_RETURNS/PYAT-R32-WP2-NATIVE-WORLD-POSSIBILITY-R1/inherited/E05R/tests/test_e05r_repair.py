"""Additional E05R boundary regressions; original 55 cases stay byte-identical."""
import copy,dataclasses,json
import pytest
from court_support import *

@pytest.mark.parametrize('role',[GSS,NCA])
@pytest.mark.parametrize('mutation',['revoke','rekey','remove','numeric'])
def test_late_native_field_changes_are_selective(role,mutation):
 a,q,s,acc,before=run();data=rows();row=next(x for x in data if x['role']==role)
 if mutation=='revoke':row['status']='REVOKED_TEST_ONLY'
 elif mutation=='rekey':row['release_nonce']='EXPLICIT_LATE_RELEASE'
 elif mutation=='remove':data.remove(row)
 elif role==GSS:row['values']['numerator']-=1;row['values']['electricity_subtypes']['mains']-=1
 else:row['values']['active_subscriptions']+=1;row['values']['prepaid']+=1
 a.registry=TestOnlyRegistry(data)
 after=a.serve(q,acc,s,consumers=clients(a,s));other=NCA if role==GSS else GSS
 assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD';assert role not in native(after)
 assert native(after)[other]==native(before)[other]
 for key in ['structural_values','empirical_steps','consumers']:
  assert after[key]==before[key]
 assert after['native_field_readset']['dependency_readset']==before['native_field_readset']['dependency_readset']
 assert len(after['native_field_readset']['successful_value_refset'])==1
 save('repair_late_'+role+'_'+mutation,dict(before=before,after=after))

@pytest.mark.parametrize('role',[GSS,NCA])
def test_native_invalidate_blocks_fresh_use_and_retains_archive(role):
 a,q,s,acc,before=run();old=copy.deepcopy(before);out=a.invalidate(role)
 assert before['receipt_hash'] in out['invalidated_for_fresh_use']
 after=a.serve(q,acc,s,consumers=clients(a,s));assert role not in native(after)
 assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert a.receipts[old['receipt_hash']]==old
 archive=a.historical_receipt(old['receipt_hash']);assert archive['archival_only'] and not archive['fresh_use_authorized']
 save('repair_invalidate_'+role,dict(invalidation=out,after=after,archive=archive))

@pytest.mark.parametrize('change',['order','values','purpose','native_order'])
def test_full_request_content_is_bound(change):
 a,q,s,acc,_=run()
 if change=='order':other=dataclasses.replace(q,empirical_conditions=(('B',1),('A',1),('C',1)))
 elif change=='values':other=dataclasses.replace(q,empirical_conditions=(('A',0),('B',1),('C',1)))
 elif change=='native_order':other=dataclasses.replace(q,native_field_roles=(NCA,GSS))
 else:
  other=copy.deepcopy(q);object.__setattr__(other,'purpose','REQUESTER_FOREIGN_PURPOSE')
 with pytest.raises(E.N9SelectedWorldRefusal):a.serve(other,acc,s)

@pytest.mark.parametrize('label',['HISTORICAL_AS_OF','CURRENT_TEST_CLOCK'])
def test_crossed_snapshot_clock_rejected_at_acceptance(label):
 a=adapter();q=E.standard_request(label=label);other=E.standard_request(label='CURRENT_TEST_CLOCK' if label=='HISTORICAL_AS_OF' else 'HISTORICAL_AS_OF');s=a.build_snapshot(other)
 with pytest.raises(E.N9SelectedWorldRefusal,match='CLOCK_OR_PURPOSE'):a.accept(q,s)

@pytest.mark.parametrize('conditions',[(('A',0),('B',0),('C',0)),(('A',1),('B',0),('C',1)),(('A',1),('B',1),('C',1))])
def test_weak_null_minority_exact_owner_support(conditions):
 from rawlsing_next.pre553_n9_n10w_progressive_candidate import synthetic_world_rows
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK',conditions=conditions);s=a.build_snapshot(q);acc=a.accept(q,s);r=a.serve(q,acc,s)
 data=synthetic_world_rows()
 for depth,step in enumerate(r['empirical_steps'],1):
  selected=[x for x in data if all(x['responses'][k]==v for k,v in conditions[:depth])]
  assert step['denominator']==len(selected)
  assert {c['cell']:c['raw_numerator_support'] for c in step['cells']}=={str(v):sum(x['responses']['Y']==v for x in selected) for v in [0,1]}
 assert len(r['native_field_readset']['values_read'])==2
 save('repair_support_'+''.join(str(v) for k,v in conditions),r)

def test_zero_support_preserves_owner_null_and_early_steps_and_two_fields():
 a=adapter(support_loss=True);q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);cs=clients(a,s);owner=a.service.possibilities(s)
 r=a.serve(q,acc,s,consumers=cs)
 assert r['empirical_steps']==owner['steps'];assert [x['denominator'] for x in r['empirical_steps']]==[24,8,0]
 assert r['empirical_steps'][-1]['state']=='ZERO_SUPPORT';assert r['empirical_steps'][-1]['cells']==[]
 assert 'binding_order' not in r['empirical_steps'][-1];assert r['empirical_steps'][-1].get('evidence_ref') is None
 assert len(r['native_field_readset']['values_read'])==2;assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert all('PARTIAL' in x['state'] for x in r['consumers']);integrity(r);json.loads(json.dumps(r))
 save('repair_zero_support',r)

def test_reverse_target_uses_own_authorized_request():
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK',target='A',conditions=(('Y',1),));s=a.build_snapshot(q);acc=a.accept(q,s);r=a.serve(q,acc,s)
 assert count(r)==[(18,29)];assert r['request_hash']==q.request_hash
 save('repair_reverse_own_acceptance',r)

@pytest.mark.parametrize('kind',['numeric','foreign_release','coherent_numeric'])
def test_e04_cache_corruption_is_not_fresh_e05r_owner_proof(kind):
 a,q,s,acc,before=run();cached=a.service.provider.cache[('Y',(('A',1),))]
 if kind=='foreign_release':cached['release_ref']=dict(kind='C11_RELEASE',object_id='FOREIGN_RELEASE',content_hash='f'*64)
 else:cached['cells'][1]['raw_numerator_support']=999
 if kind=='coherent_numeric':
  material=copy.deepcopy(cached);material.pop('content_hash');cached['content_hash']=E.semantic_hash(material)
 after=a.serve(q,acc,s)
 assert count(after)==[(18,32),(10,16),(6,8)]
 assert after['empirical_steps']==before['empirical_steps']
 save('repair_e04_cache_'+kind,after)

@pytest.mark.parametrize('kind',['foreign_snapshot','partial','joint','extra','readset','stale_permission'])
def test_complete_consumer_material_authentication(kind):
 a,q,s,acc,_=run();cs=clients(a,s)
 if kind=='foreign_snapshot':cs[0]['snapshot_ref']='FOREIGN'
 elif kind=='partial':cs[1]['state']='PARTIAL_PROPOSALS_EVALUATED'
 elif kind=='joint':cs[0]['route_probability']=1
 elif kind=='extra':cs[0]['modeled_child']={'person':'fictional'}
 elif kind=='readset':cs[0]['values_read'][0]['source_ref']={'foreign':True}
 else:a.invalidate('training_access')
 with pytest.raises(E.N9SelectedWorldRefusal):a.serve(q,acc,s,consumers=cs)

@pytest.mark.parametrize('role',[GSS,NCA])
def test_late_dereference_content_mutation_never_serves_old_value(role):
 a,q,s,acc,_=run();ref=a.registry.refs_by_role()[role]
 a.registry._records[ref]['reviewer_nonce']='MUTATED_WITHOUT_REF'
 r=a.serve(q,acc,s);assert role not in native(r);assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 assert any(x['reason']=='FIELD_CONTENT_REF_MISMATCH' for x in r['native_field_readset']['refusals'])
