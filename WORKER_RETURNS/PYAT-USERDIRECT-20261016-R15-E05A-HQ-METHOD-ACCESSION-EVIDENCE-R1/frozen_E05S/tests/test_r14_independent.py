"""R14 reviewer authored hostiles. No owner implementation edits or doubles."""
import copy, dataclasses, hashlib, json
import pytest
from court_support import *
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyReadError

@pytest.mark.parametrize('change',['target','structural','native','order','value','clock','purpose','pool','person','model'])
def test_r14_detached_request_between_accept_and_serve(change):
 a,q,s,acc,old=run();foreign=copy.deepcopy(q)
 mutations={'target':('empirical_target','A'),'structural':('structural_keys',('civil_open',)),
 'native':('native_field_roles',(NCA,GSS)),'order':('empirical_conditions',(('C',1),('B',1),('A',1))),
 'value':('empirical_conditions',(('A',0),('B',1),('C',1))),
 'clock':('clock',E.standard_request(label='HISTORICAL_AS_OF').clock),
 'purpose':('purpose','FOREIGN_PURPOSE'),'pool':('requested_pooling',True),
 'person':('requested_person_exposure',True),'model':('requested_model_use',True)}
 key,value=mutations[change];object.__setattr__(foreign,key,value)
 with pytest.raises(E.N9SelectedWorldRefusal):a.serve(foreign,acc,s)
 assert a.receipts[old['receipt_hash']]==old

@pytest.mark.parametrize('label',['CURRENT_TEST_CLOCK','HISTORICAL_AS_OF'])
def test_r14_old_receipt_not_a_fresh_current_grant(label):
 a,q,s,acc,old=run(label=label);b=adapter();freshq=E.standard_request(label='CURRENT_TEST_CLOCK');freshs=b.build_snapshot(freshq)
 with pytest.raises(E.N9SelectedWorldRefusal):b.serve(freshq,acc,freshs)
 archive=a.historical_receipt(old['receipt_hash']);assert archive['archival_only'];assert archive['fresh_use_authorized'] is False
 newacc=b.accept(freshq,freshs);new=b.serve(freshq,newacc,freshs)
 assert new['structural_values']['training_access']['value'] is False
 assert new['structural_values']['exit_cost']['value']==8
 save('r14_fresh_'+label,dict(old=old,archive=archive,new=new))

@pytest.mark.parametrize('role',[GSS,NCA])
@pytest.mark.parametrize('mutation',['withdraw','rekey','remove','publisher'])
def test_r14_late_native_unchanged_snapshot_retains_other_arm(role,mutation):
 a,q,s,acc,before=run();data=rows();row=next(x for x in data if x['role']==role)
 if mutation=='withdraw':row['status']='REVOKED_TEST_ONLY'
 elif mutation=='rekey':row['release_nonce']='R14_INDEPENDENT_RELEASE'
 elif mutation=='publisher':row['publisher']='R14_FOREIGN_PUBLISHER'
 else:data.remove(row)
 a.registry=TestOnlyRegistry(data);after=a.serve(q,acc,s,consumers=clients(a,s))
 other=NCA if role==GSS else GSS
 assert after['snapshot_hash']==before['snapshot_hash'];assert after['acceptance_hash']==before['acceptance_hash']
 assert role not in native(after);assert native(after)[other]==native(before)[other]
 assert after['native_field_readset']['dependency_readset']==before['native_field_readset']['dependency_readset']
 assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 for k in ['structural_values','empirical_steps','consumers']:assert after[k]==before[k]
 save('r14_late_'+role+'_'+mutation,dict(before=before,after=after))

@pytest.mark.parametrize('role',[GSS,NCA])
def test_r14_rekey_requires_fresh_ref_and_acceptance(role):
 a,q,s,acc,before=run();data=rows();next(x for x in data if x['role']==role)['release_nonce']='R14_NEW_SOURCE_ID'
 b=adapter(data);bs=b.build_snapshot(q)
 with pytest.raises(E.N9SelectedWorldRefusal):b.serve(q,acc,bs)
 ba=b.accept(q,bs);after=b.serve(q,ba,bs)
 assert ba.acceptance_hash!=acc.acceptance_hash;assert native(after)[role]['fixture_ref']!=native(before)[role]['fixture_ref']
 assert native(after)[role]['values']==native(before)[role]['values']
 assert after['new_issuer'] is False

@pytest.mark.parametrize('mutation',['person','dyad','probability','readset','source_ref','client_order','single','scenario_id','budget'])
def test_r14_detached_client_after_acceptance(mutation):
 a,q,s,acc,_=run();cs=clients(a,s)
 if mutation=='person':cs[0]['person']={'id':'FORGED'}
 elif mutation=='dyad':cs[1]['dyad_probability']=0.5
 elif mutation=='probability':cs[0]['route_probability']=0.5
 elif mutation=='readset':cs[0]['dependencies']=[]
 elif mutation=='source_ref':cs[1]['values_read'][0]['source_ref']={'kind':'FOREIGN'}
 elif mutation=='client_order':cs.reverse()
 elif mutation=='single':cs=cs[:1]
 elif mutation=='scenario_id':cs[1]['scenarios'][1]['scenario_id']=cs[1]['scenarios'][0]['scenario_id']
 else:cs[0]=consume(a.service,s,budget_tokens=8)['material']
 with pytest.raises(E.N9SelectedWorldRefusal):a.serve(q,acc,s,consumers=cs)

def test_r14_empty_clients_have_no_client_execution_claim():
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);n=len(a.service.value_reads)
 r=a.serve(q,acc,s,consumers=[]);assert r['consumers']==[]
 assert {x['consumer'] for x in a.service.value_reads[n:]}=={'N9_SELECTED_WORLD'}
 save('r14_scalar_only',r)

@pytest.mark.parametrize('scope',['training_access','empirical'])
def test_r14_revocation_changes_only_dependent_channels(scope):
 a,q,s,acc,before=run();a.invalidate(scope);after=a.serve(q,acc,s,consumers=clients(a,s))
 assert after['native_field_readset']==before['native_field_readset'];assert after['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 if scope=='empirical':assert after['empirical_steps']==[];assert after['structural_values']==before['structural_values']
 else:assert after['empirical_steps']==before['empirical_steps'];assert after['structural_values'][scope]['state']=='REVOKED'
 save('r14_scope_'+scope,after)

@pytest.mark.parametrize('kind',['negative','missing','zero'])
@pytest.mark.parametrize('role',[GSS,NCA])
def test_r14_native_numeric_states_are_not_fabricated(role,kind):
 data=rows();v=next(x for x in data if x['role']==role)['values']
 key='numerator' if role==GSS else 'active_subscriptions'
 if kind=='negative':v[key]=-1
 elif kind=='missing':v.pop(key)
 elif role==GSS:v.update(numerator=0,published_percent=0.0,electricity_subtypes={k:0 for k in v['electricity_subtypes']})
 else:v.update(active_subscriptions=0,prepaid=0,postpaid=0)
 if kind!='zero':
  with pytest.raises(TestOnlyReadError):TestOnlyRegistry(data)
 else:
  _,_,_,_,r=run(adapter(data));assert native(r)[role]['values'][key]==0
  assert r['state']=='SELECTED_WORLD_VALUES_SERVED';assert count(r)==[(18,32),(10,16),(6,8)]
  save('r14_observed_zero_'+role,r)

def test_r14_zero_support_full_owner_and_two_clients():
 a=adapter(support_loss=True);q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);r=a.serve(q,acc,s,consumers=clients(a,s))
 assert [x['denominator'] for x in r['empirical_steps']]==[24,8,0]
 assert [len(x['cells']) for x in r['empirical_steps']]==[2,2,0]
 assert r['empirical_steps'][-1]['state']=='ZERO_SUPPORT';assert r['empirical_steps'][-1].get('evidence_ref') is None
 assert len(native(r))==2;assert len(r['consumers'])==2;assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD'
 for c in r['consumers']:assert c['consumer_material']['empirical']['steps']==r['empirical_steps']
 save('r14_zero_support',r)

@pytest.mark.parametrize('kind',['numeric','coherent','release'])
def test_r14_mutated_e04_cache_is_recomputed(kind):
 a,q,s,acc,before=run();item=a.service.provider.cache[('Y',(('A',1),))]
 if kind=='release':item['release_ref']['object_id']='R14_FOREIGN'
 else:item['cells'][0]['raw_numerator_support']=999
 if kind=='coherent':
  material=copy.deepcopy(item);material.pop('content_hash');item['content_hash']=E.semantic_hash(material)
 r=a.serve(q,acc,s)
 assert count(r)==[(18,32),(10,16),(6,8)];assert r['empirical_steps']==before['empirical_steps']
 save('r14_cache_'+kind,r)

def test_r14_independent_semantic_and_byte_hash_decimal_verification():
 _,_,_,_,r=run()
 def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
 def exact(v):
  if isinstance(v,float):return {'$exact_decimal':repr(v)}
  if isinstance(v,dict):return {k:exact(x) for k,x in sorted(v.items())}
  if isinstance(v,(list,tuple)):return [exact(x) for x in v]
  return v
 from rawlsing_next.pre553_empirical_objects import semantic_hash
 raw=copy.deepcopy(r);payload=raw.pop('receipt_payload_sha256');assert hashlib.sha256(canonical(raw).encode()).hexdigest()==payload
 sem=raw.pop('receipt_hash');assert semantic_hash(exact(raw))==sem
 assert native(r)[GSS]['values']['published_percent']==72.6
 for change in ['decimal','foreign']:
  bad=copy.deepcopy(raw)
  if change=='decimal':next(x for x in bad['native_field_readset']['values_read'] if x['role']==GSS)['values']['published_percent']=72.7
  else:bad['foreign_field']='UNACCEPTED'
  assert semantic_hash(exact(bad))!=sem
  bad['receipt_hash']=sem;assert hashlib.sha256(canonical(bad).encode()).hexdigest()!=payload
 save('r14_independent_hash',dict(semantic=sem,payload=payload,published_literal='72.6',source_issuer_attested=False))
