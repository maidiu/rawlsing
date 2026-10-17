"""Reviewer invariants. Failures expose original candidate defects, no xfails."""
import json,copy,dataclasses,hashlib
import pytest
from court_support import *
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyReadError

@pytest.mark.parametrize('label,access,exit_cost',[('CURRENT_TEST_CLOCK',False,8),('HISTORICAL_AS_OF',True,2)])
def test_original_positive_values_and_actual_same_snapshot_clients(label,access,exit_cost):
 a,q,s,acc,r=run(label=label);save(label,dict(request=q.binding(),acceptance=acc.binding(),receipt=r,service_value_reads=a.service.value_reads,catalog_trace=a.service.catalog.trace,provider_trace=a.service.provider.trace))
 assert r['state']=='SELECTED_WORLD_VALUES_SERVED';assert count(r)==[(18,32),(10,16),(6,8)]
 assert r['structural_values']['training_access']['value'] is access;assert r['structural_values']['exit_cost']['value']==exit_cost
 n=native(r);assert n[GSS]['values']['numerator']==2388192;assert n[GSS]['values']['denominator']==3288063;assert n[GSS]['values']['published_percent']==72.6;assert n[NCA]['values']['active_subscriptions']==23414527
 assert n[GSS]['native_unit']!=n[NCA]['native_unit'];assert n[GSS]['native_geography']!=n[NCA]['native_geography']
 assert n[GSS]['publication_date']=='2022-02-24';assert n[NCA]['publication_date']=='2022-07-08'
 for c in r['consumers']:
  m=c['consumer_material'];assert m['snapshot_ref']==s.snapshot_hash
  assert all(v['snapshot_ref']==s.snapshot_hash for v in m['values_read'])
  assert [x['denominator'] for x in m['empirical']['steps']]==[32,16,8]
 assert r['consumers'][0]['consumer_material']['route_probability'] is None
 assert all(x['selection_weight'] is None for x in r['consumers'][1]['consumer_material']['scenarios'])
 assert r['request_hash']==q.request_hash;assert r['acceptance_hash']==acc.acceptance_hash;integrity(r)

@pytest.mark.parametrize('date,gss,nca',[('2022-02-23',False,False),('2022-02-24',True,False),('2022-07-07',True,False),('2022-07-08',True,True)])
def test_original_publication_boundary(date,gss,nca):
 out=fresh_read(TestOnlyRegistry(rows()),date);save('publication_'+date,out)
 assert {v['role'] for v in out['values_read']}==({GSS} if gss else set())|({NCA} if nca else set());assert len(out['dependency_readset'])==2

def test_typed_partial_preserves_exact_failed_arm():
 a,q,s,acc,r=run(label='TYPED_PARTIAL_PRE_NCA_PUBLICATION');save('typed_partial',r)
 assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD';n=r['native_field_readset'];assert len(n['dependency_readset'])==2;assert len(n['successful_value_refset'])==1;assert [x['role'] for x in n['values_read']]==[GSS];assert n['refusals'][0]['reason']=='NOT_PUBLISHED_AT_SELECTED_ASOF'

@pytest.mark.parametrize('valid,pub,expected',[('2027-05-31','2027-05-31',True),('2027-01-01','2027-06-01',False),('2026-12-31','2027-06-01',True),('2028-01-01','2028-01-01',None)])
def test_effective_and_publication_are_separate(valid,pub,expected):
 a=adapter();q=dataclasses.replace(E.standard_request(label='HISTORICAL_AS_OF'),clock=E.SelectedWorldClock(mode='AS_OF',valid_at=valid,published_asof=pub));_,_,_,_,r=run(a,request=q);save('clock_'+valid+'_'+pub,r)
 if expected is None:assert 'state' in r['structural_values']['training_access']
 else:assert r['structural_values']['training_access']['value'] is expected

def test_empirical_Y_mutation_and_both_clients_actual_values():
 _,_,_,_,base=run();_,_,_,_,changed=run(adapter(empirical_changed=True));save('empirical_perturbation',dict(base=base,changed=changed))
 assert count(changed)==[(19,32),(11,16),(7,8)];assert base['structural_values']==changed['structural_values'];assert base['native_field_readset']==changed['native_field_readset']
 for i in [0,1]:
  x=base['consumers'][i]['consumer_material'];y=changed['consumers'][i]['consumer_material'];assert x['empirical']['steps']!=y['empirical']['steps']
 assert [x['source_balance_count'] for x in changed['consumers'][0]['consumer_material']['source_balance_reads']]==[6,6,6]

def test_structural_alone_changes_eligibility_only():
 a=E.N9SelectedWorldAdapter(service=GenericSelectedWorldService(structural_revision=False),registry=TestOnlyRegistry(rows()));_,_,_,_,old=run(a);_,_,_,_,new=run();save('structural_perturbation',dict(base=old,changed=new))
 assert old['empirical_steps']==new['empirical_steps'];assert old['native_field_readset']==new['native_field_readset'];assert old['consumers'][0]['consumer_material']['structural_routes']!=new['consumers'][0]['consumer_material']['structural_routes']

@pytest.mark.parametrize('role',[GSS,NCA])
def test_separately_native_mutation_changes_only_that_field(role):
 data=rows();v=next(x for x in data if x['role']==role)['values']
 if role==GSS:v['numerator']-=1;v['electricity_subtypes']['mains']-=1
 else:v['active_subscriptions']+=1;v['prepaid']+=1
 _,_,_,_,base=run();_,_,_,_,changed=run(adapter(data));save('native_mutation_'+role,dict(base=base,changed=changed))
 assert base['structural_values']==changed['structural_values'];assert base['empirical_steps']==changed['empirical_steps'];assert base['consumers']==changed['consumers'];other=NCA if role==GSS else GSS
 assert native(base)[other]==native(changed)[other];assert native(base)[role]!=native(changed)[role]

def test_null_bit_identical():
 _,_,_,_,a=run();_,_,_,_,b=run();assert a==b

def test_zero_support_stays_typed_without_numeric_fabrication():
 a=adapter(support_loss=True);q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);cs=clients(a,s);emp=a.service.possibilities(s);save('zero_support_before_adapter',dict(empirical=emp,consumers=cs));assert [x['denominator'] for x in emp['steps']]==[24,8,0];assert emp['steps'][-1]['state']=='ZERO_SUPPORT'
 r=a.serve(q,acc,s,consumers=cs);assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD';assert r['empirical_state']!='PRODUCTIVE_TEST_ONLY'

@pytest.mark.parametrize('field,value,reason',[('issuer_ref','FAKE_SIGNER','EXTERNAL_CUSTODY_OR_ISSUER_FORGERY'),('permission','GRANTED_BY_REQUESTER','REAL_USE_PERMISSION_NOT_ISSUED'),('issued',True,'FIELD_ISSUANCE_LAUNDERING'),('source_pdf_sha256','f'*64,'EXTERNAL_CUSTODY_OR_ISSUER_FORGERY'),('family','WRONG_SOURCE','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),('native_unit','UNIQUE_PERSONS','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),('native_geography','GHANA_RURAL','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),('unique_persons',True,'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'),('publication_date','2022-02-24','PUBLICATION_OR_OBSERVATION_CLOCK_SUBSTITUTION')])
def test_forged_source_permission_unit_publication_refused(field,value,reason):
 data=rows();next(x for x in data if x['role']==NCA)[field]=value
 with pytest.raises(TestOnlyReadError,match=reason):TestOnlyRegistry(data)

@pytest.mark.parametrize('flag',['requested_pooling','requested_person_exposure','requested_model_use'])
def test_explicit_inference_request_refused(flag):
 with pytest.raises(E.N9SelectedWorldRefusal):E.standard_request(label='CURRENT_TEST_CLOCK',**{flag:True})

def test_native_role_swap_refused():
 a=adapter();refs=a._field_refs;a._field_refs={GSS:refs[NCA],NCA:refs[GSS]};a._relation['ordered_refs']=[a._field_refs[GSS],a._field_refs[NCA]]
 _,_,_,_,r=run(a);save('role_swap',r);assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD';assert len(r['native_field_readset']['values_read'])==0

def test_acceptance_substitution_refused():
 a,q,s,acc,r=run();other=dataclasses.replace(acc,request_hash='0'*64)
 with pytest.raises(E.SelectedWorldInconsistency):a.serve(q,other,s)

@pytest.mark.parametrize('alter',['target','readset','clock'])
def test_serve_must_bind_actual_request_to_acceptance(alter):
 a,q,s,acc,_=run()
 if alter=='target':foreign=dataclasses.replace(q,empirical_target='A',empirical_conditions=(('Y',1),))
 elif alter=='readset':foreign=dataclasses.replace(q,structural_keys=('civil_open',))
 else:foreign=dataclasses.replace(q,clock=E.SelectedWorldClock(mode='AS_OF',valid_at='2026-06-01',published_asof='2026-03-01'))
 try:r=a.serve(foreign,acc,s)
 except E.N9SelectedWorldRefusal:return
 save('DEFECT_request_substitution_'+alter,dict(original_request=q.binding(),foreign_request=foreign.binding(),acceptance=acc.binding(),receipt=r))
 assert r['state']!='SELECTED_WORLD_VALUES_SERVED' or r['request_hash']==foreign.request_hash,'UNACCEPTED_REQUEST_SERVED_UNDER_OLD_REQUEST_HASH'

def test_accept_must_bind_snapshot_clocks_to_request():
 a=adapter();current=E.standard_request(label='CURRENT_TEST_CLOCK');historical=E.standard_request(label='HISTORICAL_AS_OF');s=a.build_snapshot(current)
 try:acc=a.accept(historical,s);r=a.serve(historical,acc,s)
 except E.N9SelectedWorldRefusal:return
 save('DEFECT_accept_clock_substitution',dict(request=historical.binding(),acceptance=acc.binding(),receipt=r))
 assert r['state']!='SELECTED_WORLD_VALUES_SERVED' or r['selection']['published_asof']==historical.clock.published_asof,'HISTORICAL_REQUEST_ACCEPTED_AGAINST_CURRENT_SNAPSHOT'

@pytest.mark.parametrize('scope',['training_access','empirical'])
def test_late_world_revocation_remains_typed(scope):
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);a.invalidate(scope);r=a.serve(q,acc,s,consumers=clients(a,s));save('late_revocation_'+scope,r);assert r['state']=='TYPED_PARTIAL_SELECTED_WORLD'

def test_late_native_revocation_must_be_reread():
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s)
 data=rows();next(x for x in data if x['role']==NCA)['status']='REVOKED_TEST_ONLY';a.registry=TestOnlyRegistry(data);fresh=fresh_read(a.registry);r=a.serve(q,acc,s,consumers=clients(a,s))
 save('DEFECT_late_native_revocation',dict(fresh_native_read=fresh,receipt=r,acceptance=acc.binding()))
 assert r['state']!='SELECTED_WORLD_VALUES_SERVED' and NCA not in native(r),'CACHED_NATIVE_VALUE_SERVED_AFTER_WITHDRAWAL'

def test_native_invalidate_scope_supported():
 a,q,s,acc,r=run()
 try:out=a.invalidate(NCA)
 except ValueError as e:save('DEFECT_native_invalidation_scope',dict(error=str(e)));pytest.fail('NATIVE_FIELD_PERMISSION_SCOPE_NOT_SUPPORTED:'+str(e))
 assert r['receipt_hash'] in out['invalidated_for_fresh_use']

@pytest.mark.parametrize('alter',['foreign_snapshot','partial_as_complete','forged_joint_probability'])
def test_consumer_material_must_be_bound_not_copied(alter):
 a,q,s,acc,r=run();cs=clients(a,s)
 if alter=='foreign_snapshot':cs[0]['snapshot_ref']='FOREIGN_SNAPSHOT'
 elif alter=='partial_as_complete':cs[0]['state']='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
 else:cs[0]['route_probability']={'$exact_fraction':[1,1]};cs[1]['scenarios'][0]['selection_weight']={'$exact_fraction':[1,1]}
 try:out=a.serve(q,acc,s,consumers=cs)
 except E.N9SelectedWorldRefusal:return
 save('DEFECT_consumer_'+alter,out)
 assert out['state']!='SELECTED_WORLD_VALUES_SERVED','UNVERIFIED_CONSUMER_PAYLOAD_ENDORSED_AS_COMPLETE'

def test_decimal_literal_change_invalidates_both_hashes():
 _,_,_,_,r=run();bad=copy.deepcopy(r);next(v for v in bad['native_field_readset']['values_read'] if v['role']==GSS)['values']['published_percent']=72.7
 save('decimal_integrity_attack',bad)
 with pytest.raises(AssertionError):integrity(bad)
 x=copy.deepcopy(bad);x.pop('receipt_payload_sha256');x.pop('receipt_hash');assert E.semantic_hash(E._float_free(x))!=r['receipt_hash']

def test_same_value_native_coherent_rekey_is_fixture_only_not_signer_authority():
 data=rows();data[0]['reviewer_nonce']='SAME_VALUES_NEW_FIXTURE_ID';_,_,_,_,base=run();_,_,_,_,changed=run(adapter(data));save('coherent_fixture_rekey',dict(base=base,changed=changed))
 assert native(base)[GSS]['values']==native(changed)[GSS]['values'];assert native(base)[GSS]['fixture_ref']!=native(changed)[GSS]['fixture_ref'];assert changed['operative_OC05'] is False;assert changed['new_issuer'] is False

def test_actual_oc05_disabled():
 from rawlsing_next.objective_consumer_bounded_evidence import installation_manifest,OC05,evaluate_current_consumer,NotYetApplicableConsumer
 m={x['policy_id']:x for x in installation_manifest()};save('actual_oc05_manifest',m);assert m[OC05]['current_applicability']=='NOT_YET_APPLICABLE';assert m[OC05]['consumer_seam'] is None
 with pytest.raises(NotYetApplicableConsumer):evaluate_current_consumer(policy_id=OC05,operation_id='E05I_READ',inputs=(),requested_claim_ceiling='OBJECTIVE_FACT',partial_allowed=False)

@pytest.mark.parametrize('what',['release','source','risk_set','permission_root','query_permit'])
def test_empirical_identity_and_permission_changes_not_silently_reauthorized(what):
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);w=a.service.catalog.empirical
 if what=='permission_root':w['permission_root']='REQUESTER_SELF_MINTED_ROOT'
 elif what=='query_permit':w['query_permits']['Y']['max_conditioners']=4
 else:
  key={'release':'release_ref','source':'universe','risk_set':'risk_refs'}[what]
  if key=='universe':
   u=w['source'][key];fields=dict(u.semantic_fields);fields['raw_source_identity']='REQUESTER_COHERENT_REKEY';w['source'][key]=type(u)(typed_state=u.typed_state,authority_snapshot_refs=u.authority_snapshot_refs,dependency_refs=u.dependency_refs,producer_replay_locator_or_reference_root=u.producer_replay_locator_or_reference_root,**fields)
  elif key=='release_ref':w['source'][key]=dataclasses.replace(w['source'][key],object_id='REQUESTER_COHERENT_REKEY')
  else:w['source'][key]['R']=dataclasses.replace(w['source'][key]['R'],object_id='REQUESTER_COHERENT_REKEY')
 try:result=a.serve(q,acc,s)
 except Exception as e:
  save('identity_attack_'+what,dict(exception=type(e).__name__,message=str(e)));assert isinstance(e,ValueError);return
 save('DEFECT_identity_attack_'+what,result);assert result['state']!='SELECTED_WORLD_VALUES_SERVED'

def test_direct_ungranted_target_remains_refused():
 a=adapter();q=dataclasses.replace(E.standard_request(label='CURRENT_TEST_CLOCK'),empirical_target='B',empirical_conditions=(('Y',1),));s=a.build_snapshot(q);acc=a.accept(q,s)
 with pytest.raises(ValueError,match='TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE'):a.serve(q,acc,s)

def test_fresh_provider_with_self_minted_permit_is_not_signer_proof():
 from product.empirical import GenericProgressiveProvider,build_source
 w=build_source();s=w['source'];w['query_permits']['B']=dict(target_ref=s['qrefs']['B'].as_dict(),conditioner_refs={'Y':s['qrefs']['Y'].as_dict()},allowed_values=[0,1],max_conditioners=1,scope='REQUESTER_SELF_MINTED')
 try:out=GenericProgressiveProvider(w).progressive('B',(('Y',1),))
 except ValueError as e:save('self_minted_fresh_provider',dict(refused=True,message=str(e)));return
 save('self_minted_fresh_provider',dict(refused=False,result=out,interpretation='Fixture constructor accepts caller supplied query permit. Hash integrity provides no signer attestation. No real issuer authority follows.'))
 # Sourcefree test fixture trust seam documented; not a claim of real permission.
 assert out and all(x['permission_root']=='TEST_ONLY_E04_SOURCE_ROOT' for x in out)

def test_native_stale_content_ref_cannot_be_dereferenced():
 registry=TestOnlyRegistry(rows());ref=registry.refs_by_role()[GSS]
 # Attack only: coherent numeric edit leaves the exact frozen content ref old.
 registry._records[ref]['values']['numerator']-=1;registry._records[ref]['values']['electricity_subtypes']['mains']-=1
 with pytest.raises(TestOnlyReadError,match='FIELD_CONTENT_REF_MISMATCH'):registry.dereference(ref)

def test_native_same_value_new_release_registry_must_not_silently_use_old_acceptance():
 a=adapter();q=E.standard_request(label='CURRENT_TEST_CLOCK');s=a.build_snapshot(q);acc=a.accept(q,s);data=rows();data[1]['release_nonce']='NEW_SAME_VALUE_RELEASE';a.registry=TestOnlyRegistry(data)
 r=a.serve(q,acc,s);save('DEFECT_native_rekey_after_acceptance',dict(fresh_native_read=fresh_read(a.registry),receipt=r))
 assert r['state']!='SELECTED_WORLD_VALUES_SERVED' or native(r)[NCA]['fixture_ref']==a.registry.refs_by_role()[NCA],'STALE_NATIVE_ACCEPTANCE_WITH_NEW_RELEASE'

def test_native_row_oracle_independent_reaggregation():
 from rawlsing_next.pre553_n9_n10w_progressive_candidate import synthetic_world_rows
 data=synthetic_world_rows();assert len(data)==58
 expected=[(18,32),(10,16),(6,8)];counts=[]
 for depth in [1,2,3]:
  matched=[x for x in data if all(x['responses'][k]==1 for k in ['A','B','C'][:depth])];counts.append((sum(x['responses']['Y']==1 for x in matched),len(matched)))
 save('independent_row_reaggregation',dict(rows=data,counts=counts,expected=expected));assert counts==expected
