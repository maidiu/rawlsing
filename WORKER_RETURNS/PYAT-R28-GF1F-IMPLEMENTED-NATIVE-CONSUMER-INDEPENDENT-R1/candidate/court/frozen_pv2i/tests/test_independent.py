"""Fresh independently authored PV2I acceptance guards; no candidate test imports."""
from common import *
import pytest
from collections import Counter
@pytest.fixture(scope='module')
def court(tmp_path_factory):
 fx=F.pv2_sourcefree_fixture(tmp_path_factory.mktemp('independent-baseline'));r=run(fx);return fx,r

def test_exact_independent_inventory_and_six_real_consumers(court):
 fx,r=court;keys=[]
 for w in fx['records']:
  row=next(o for o in O['obligations'] if o['respondent_namespace']==w.original.respondent_namespace and o['slot']==w.legacy.slot)
  for k in ('form','respondent_unit','language','instrument_release','administered_occurrence','option_scope','respondent_namespace'):
   assert json.loads(json.dumps(getattr(w.original,k)))==row[k]
  for k in ('state','hold_reason','target','item','semantic_op_class','condition_order','semantic_roles'):
   assert json.loads(json.dumps(getattr(w.legacy,k)))==row[k]
  for role,expected_ref in row['issuer_identities'].items():
   actual=getattr(w,role);assert actual.kind==expected_ref['kind'] and actual.object_id==expected_ref['object_id']
  keys.append((w.original.respondent_namespace,w.legacy.slot))
 assert Counter(keys)==Counter((o['respondent_namespace'],o['slot']) for o in O['obligations'])
 assert r['ok'] and len(r['links'])==6 and len(r['nonrunnable'])==2
 assert len({l['consumer_ref']['content_hash'] for l in r['links']})==6
 assert len({l['original_expected_work_key'] for l in r['links']})==6
 assert len({l['legacy_expected_work_key'] for l in r['links']})==3
 for l in r['links']:
  assert l['producer_result_ref']==l['consumer_material']['producer_fact_ref']
  if l['original_identity']['operation']['slot'] in ('PAIR','B'):
   assert profile(l['consumer_material'])=={'0':{'denominator':1,'targets':{'0':1,'1':0}},'1':{'denominator':1,'targets':{'0':0,'1':1}}}

@pytest.mark.parametrize('field',['original_U_ref','independent_E_ref','independent_custody_ref','original_operation_scope_ref'])
def test_foreign_reference_with_fixed_register_refused(court,field):
 fx,_=court;old=slot(fx);new=replace(old,**{field:ref('new-'+field)});e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

@pytest.mark.parametrize('field',['original_U_ref','independent_E_ref','independent_custody_ref','original_operation_scope_ref'])
def test_coherently_reissued_register_cannot_authenticate_itself(court,field):
 fx,_=court;old=slot(fx);foreign=ref('coherent-'+field);new=replace(old,**{field:foreign});e,p=mutate_work(fx,old,new)
 reg=replace(fx['register'],obligations=tuple(replace(o,**{field:foreign}) if o.obligation_key==('PV2-ADULT-A','PAIR') else o for o in fx['register'].obligations))
 with pytest.raises(ValueError):run(fx,e,p,reg)

@pytest.mark.parametrize('field,value',[('form','PV2I-FOREIGN-FORM'),('respondent_unit','HOUSEHOLD'),('language','PV2I-OTHER'),('instrument_release','EDITION2'),('administered_occurrence','SECOND'),('option_scope',('1','0'))])
def test_fixed_register_rejects_original_metadata_mutation(court,field,value):
 fx,_=court;old=slot(fx);new=replace(old,original=replace(old.original,**{field:value}),legacy=replace(old.legacy,form=value) if field=='form' else old.legacy);e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

def test_two_held_omission_same_six_runnable_refused(court):
 fx,_=court;e=K.FrozenOriginalExpected.from_records(tuple(w for w in fx['records'] if w.legacy.is_runnable),input_origin=K.ORIGIN)
 with pytest.raises(ValueError):run(fx,e)

def test_A_only_scope_refused(court):
 fx,_=court;e=K.FrozenOriginalExpected.from_records(tuple(w for w in fx['records'] if w.original.respondent_namespace=='PV2-ADULT-A'),input_origin=K.ORIGIN)
 with pytest.raises(ValueError):run(fx,e)

def test_equal_count_held_relabel_with_fixed_register_refused(court):
 fx,_=court;old=slot(fx,kind='ORDERED');new=replace(old,legacy=replace(old.legacy,slot='PV2I-UNEXPECTED-HELD'));e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

def test_equal_count_held_relabel_with_self_reissued_register_refused(court):
 fx,_=court;old=slot(fx,kind='ORDERED');new=replace(old,legacy=replace(old.legacy,slot='PV2I-UNEXPECTED-HELD'));e,p=mutate_work(fx,old,new)
 reg=replace(fx['register'],obligations=tuple(replace(o,slot='PV2I-UNEXPECTED-HELD') if o.obligation_key==('PV2-ADULT-A','ORDERED') else o for o in fx['register'].obligations))
 with pytest.raises(ValueError):run(fx,e,p,reg)

@pytest.mark.parametrize('field',['source_release_ref','empirical_universe_ref','original_item_scope_ref','routing_refs'])
def test_complete_original_source_binding(court,field):
 fx,_=court;old=slot(fx)
 value=(ref('route'),) if field=='routing_refs' else replace(old.original.source_release_ref,object_id='urn:pv2i:wrong-source-edition') if field=='source_release_ref' else ref(field)
 new=replace(old,original=replace(old.original,**{field:value}));e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

def test_swapped_actual_query_target_conditioner_refused(court):
 fx,_=court;old=slot(fx);new=replace(old,legacy=replace(old.legacy,query_ref=fx['inputs'][0]['reverse_query'].ref));e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

def test_reversed_role_mask_refused(court):
 fx,_=court;old=slot(fx);new=replace(old,legacy=replace(old.legacy,semantic_roles=('TARGET','CONDITIONER')));e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):run(fx,e,p)

@pytest.mark.parametrize('field,value',[('issuer','PV2I-SELF-ISSUER'),('grant','SIGNED_REAL_SOURCE_GRANT'),('ceiling',('PRODUCTION',))])
def test_current_read_refuses_foreign_or_widened_fixture_grant(court,field,value):
 fx,r=court;reg=replace(fx['register'],fixture_use_grant=replace(fx['register'].fixture_use_grant,**{field:value}))
 try:reading=V.read_current_consumer_material(reg,r)
 except ValueError:return
 assert reading['servable'] is False

@pytest.mark.parametrize('field,value',[('issuer','PV2I-SELF-ISSUER'),('grant','SIGNED_REAL_SOURCE_GRANT'),('ceiling',('PRODUCTION',))])
def test_execution_refuses_self_rehashed_fixture_grant(court,field,value):
 fx,_=court;reg=replace(fx['register'],fixture_use_grant=replace(fx['register'].fixture_use_grant,**{field:value}))
 with pytest.raises(ValueError):run(fx,register=reg)

def test_explicit_revoked_register_blocks(court):
 fx,r=court;reg=replace(fx['register'],fixture_use_grant=replace(fx['register'].fixture_use_grant,revoked=True,revocation_reason='PV2I-REVOKED'))
 assert V.read_current_consumer_material(reg,r)['servable'] is False
 with pytest.raises(ValueError):run(fx,register=reg)

def test_historical_register_cannot_restore_current_authorization(court):
 fx,r=court;revoked=replace(fx['register'],fixture_use_grant=replace(fx['register'].fixture_use_grant,revoked=True))
 assert V.read_current_consumer_material(revoked,r)['servable'] is False
 assert V.read_current_consumer_material(fx['register'],r)['servable'] is False, 'Old unrevoked snapshot reauthorizes after revocation; no independent current registry'

def test_current_consumer_rejects_payload_tamper_same_ref(court):
 fx,r=court;fake=copy.deepcopy(r);fake['links'][0]['consumer_material']['conditional_count_profile'][0]['condition_denominator_support']=999
 try:reading=V.read_current_consumer_material(fx['register'],fake)
 except ValueError:return
 assert reading['servable'] is False,'Current read serves changed payload under unchanged consumer reference'

def test_current_read_does_not_alias_historical_report(court):
 fx,r=court;history=copy.deepcopy(r);reading=V.read_current_consumer_material(fx['register'],history)
 reading['links'][0]['consumer_material']['conditional_count_profile'][0]['condition_denominator_support']=999
 assert history==r,'Read result aliases original historical material'

@pytest.mark.parametrize('mode',['missing_material','missing_roles','missing_conditioner'])
def test_role_validation_fails_closed_on_incomplete_material(court,mode):
 fx,r=court;links=copy.deepcopy(r['links'])
 if mode=='missing_material':links[0].pop('consumer_material')
 elif mode=='missing_roles':links[0]['consumer_material'].pop('roles')
 else:links[0]['consumer_material']['roles'].pop('CONDITIONER')
 with pytest.raises(ValueError):V.validate_consumer_roles_against_declared(links,fx['register'])

def test_generic_native_labels_not_specialized_Q86(court):
 _,r=court
 for l in r['links']:
  role=l['consumer_material']['roles']
  assert role['CONDITIONER']['source_native_variable'] in ('X','Y') and role['TARGET']['source_native_variable'] in ('X','Y')

def test_independent_row_mutation_reaches_actual_consumers(court,tmp_path):
 fx,before=court;new=make_numeric_fixture(tmp_path/'mutant');after=run(new)
 results={}
 for l in after['links']:
  ident=l['original_identity'];ns=ident['original']['respondent_namespace'];slotname=ident['operation']['slot'];results[ns+'|'+slotname]=profile(l['consumer_material'])
  if ns=='PV2-ADULT-A' and slotname=='PAIR':assert profile(l['consumer_material'])=={'0':{'denominator':1,'targets':{'0':0,'1':1}},'1':{'denominator':1,'targets':{'0':0,'1':1}}}
  if ns=='PV2-ADULT-A' and slotname=='B':assert profile(l['consumer_material'])['1']=={'denominator':2,'targets':{'0':1,'1':1}}
  if ns=='PV2-ADULT-B':
   old=next(x for x in before['links'] if x['original_identity']['original']['respondent_namespace']==ns and x['original_identity']['operation']['slot']==slotname)
   assert l==old,'Unrelated B exact consumer changed'
 dump('numeric_mutation.json',{'row':'R2 Y0->1; pre-execution erratum preserved','source_cells':[{'namespace':x['universe'].respondent_namespace,'cells':[{'row':c.row_ordinal,'item':c.variable_name,'value':c.raw_value} for c in x['fx']['stream'].cell_iter_factory()]} for x in new['inputs']],'profiles':results,'before':before,'after':after})

def test_coherent_household_relabel_cannot_reuse_respondent_fact(court):
 fx,_=court;old=slot(fx);new=replace(old,original=replace(old.original,respondent_unit='HOUSEHOLD'));e,p=mutate_work(fx,old,new)
 reg=replace(fx['register'],obligations=tuple(replace(o,respondent_unit='HOUSEHOLD') if o.obligation_key==('PV2-ADULT-A','PAIR') else o for o in fx['register'].obligations))
 with pytest.raises(ValueError):run(fx,e,p,reg)

def test_genuine_cold_process_preserves_journal_and_no_new_durable_units():
 d=json.loads((R/'observations/cold_court.json').read_text())
 assert d['distinct_pids'] and d['same_ledger_bytes'] and d['links_exact'] and d['held_exact'] and d['register_exact'] and d['no_new_durable_units']

def test_changed_actual_journal_result_reference_is_not_ignored():
 d=json.loads((R/'observations/cold_actual_result_ref_tamper.json').read_text())
 assert d['exit']!=0, 'Changed result_refs in actual side-effect journal ignored by successful replay'

def test_changed_checkpoint_receipt_payload_refused():
 assert json.loads((R/'observations/cold_checkpoint_payload_tamper.json').read_text())['exit']!=0

def test_fresh_process_current_read_refuses_self_issued_grant():
 d=json.loads((R/'observations/cold_forged_current_grant.json').read_text())
 assert not d['servable'], 'Fresh process serves persisted history under requester-created production-ceiling grant'

def test_missing_source_and_changed_edition_never_fake_cold_success():
 d=json.loads((R/'observations/cold_court.json').read_text());assert d['missing_source']['exit']!=0 and d['changed_edition']['exit']!=0

def test_real_empty_risk_I03_and_Field_Forge_typed_states(court):
 from rawlsing_next.pre553_empirical_query import execute_empirical_query
 from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
 from rawlsing_next.field_forge_conditional_support import produce_exact_conditional_support_profile
 fx,_=court;data=fx['inputs'][0];stub={'universe':data['universe'],'respondents':{r.respondent_key:r for r in data['projection'].respondents},'qrefs':data['fx']['qrefs'],'risk_refs':{'R':data['fx']['risk']},'source_auth':data['projection'].authority_snapshots[0]};qa=data['fx']['qauth'];da=data['fx']['dauth']
 pred=F._branch_predicate(stub,qa,members=(),tag='pv2i-independent-empty');query=F._query(stub,qa,pred,('X','Y'),measure='RAW',tag='pv2i-independent-empty');session=fx['plans'][0].p01_kwargs['session']
 result=execute_empirical_query(repository=session.repository,query=query,predicate=pred,authority_registry=AuthorityRegistry((*data['projection'].authority_snapshots,qa,da)),release_refs=session.identity.release_refs)
 fact=result.facts[0];assert fact.typed_state=='ZERO_SUPPORT' and fact.raw_denominator_support==0
 consumer=produce_exact_conditional_support_profile(joint_fact=fact,joint_query=query,conditioner_ref=data['fx']['qrefs']['X'],target_ref=data['fx']['qrefs']['Y'],producer_permission_ceiling=('SOURCE_FREE_DEV',))
 assert consumer.typed_state=='ZERO_SUPPORT'
 dump('empty_risk_owner_consumer.json',{'fact':fact.semantic_projection(),'fact_ref':fact.ref.as_dict(),'consumer':consumer.as_dict()})

def test_second_independent_row_mutation_changes_I05_winning_consumer(court,tmp_path):
 fx,before=court;new=make_numeric_fixture(tmp_path/'i05-mutant',row=1,new_value='0');after=run(new)
 profiles={}
 for l in after['links']:
  ns=l['original_identity']['original']['respondent_namespace'];kind=l['original_identity']['operation']['slot'];profiles[ns+'|'+kind]=profile(l['consumer_material'])
  old=next(x for x in before['links'] if x['original_identity']['original']['respondent_namespace']==ns and x['original_identity']['operation']['slot']==kind)
  if ns=='PV2-ADULT-A' and kind in ('PAIR','DISCOVERY'):
   assert profile(l['consumer_material'])['1']=={'denominator':1,'targets':{'0':1,'1':0}}
   assert l['producer_result_ref']!=old['producer_result_ref'] and l['consumer_ref']!=old['consumer_ref']
  elif ns=='PV2-ADULT-B':assert l==old
 dump('numeric_I05_mutation.json',{'fresh_extension':'R1 Y1->0, targets same-person X1 branch; independently specified before this execution, original R2 oracle unchanged','profiles':profiles,'after':after})
