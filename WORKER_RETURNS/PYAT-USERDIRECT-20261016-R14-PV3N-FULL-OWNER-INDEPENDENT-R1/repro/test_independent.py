"""PV3N independently authored physical full-owner/custody tests."""
from physical import *
from dataclasses import FrozenInstanceError
import pytest,copy
from rawlsing_next.pre553_empirical_objects import ExactRef
from pv3_candidate import validate_consumer_roles_against_declared
from common import slot,mutate_work,ref
E=R/'evidence/independent'

@pytest.fixture(scope='module')
def court(tmp_path_factory):
 with Trace() as t:
  owner,api,fx,installed=prepare(tmp_path_factory.mktemp('pv3n-original'))
  report=api.run_sourcefree_with_register(**args(fx));current=api.read_current_consumer_material(fx['register'],report)
  actual=receipts(fx)
 write(E/'actual_six_native_calls.json',dict(installation=installed,report=report,current=current,durable_calls=[len(x) for x in fx['calls']],original_receipt_objects=actual,trace=t.data()))
 return owner,api,fx,report,current

def test_all_eight_exact_identities_six_actual_values_and_receipts(court):
 o,a,fx,r,current=court;oracle=json.loads((R/'01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json').read_text())
 assert len(r['links'])==6 and len(r['nonrunnable'])==2 and len({x['consumer_ref']['content_hash'] for x in r['links']})==6
 assert current['servable'] and current['links']==r['links']
 assert {w.key for w in fx['records']}=={x['complete_exact_fixture_identity']['expected_work_key'] for x in oracle['inventory']}
 assert len({l['legacy_expected_work_key'] for l in r['links']})==3
 assert [len(x) for x in fx['calls']]==[3,3]
 for l in r['links']:
  m=l['consumer_material'];orig=l['original_identity']['original']
  assert m['producer_fact_ref']==l['producer_result_ref']
  assert m['roles']['CONDITIONER']['ref']==orig['native_item_refs'][0] and m['roles']['TARGET']['ref']==orig['native_item_refs'][1]
  assert m['producer_permission_ceiling']==m['relation_permission_ceiling']==['SOURCE_FREE_DEV']
  assert m['roles']['CONDITIONER']['source_native_variable']=='Q86B' and m['roles']['TARGET']['source_native_variable']=='Q86A'
 assert a.read_current_consumer_material(fx['register'],r,semantics='GENERIC_NATIVE')['claim']=='GENERIC_NATIVE_SEMANTICS_HOLD'

@pytest.mark.parametrize('field',['original_U_ref','independent_E_ref','independent_custody_ref','original_operation_scope_ref'])
def test_independent_coherent_foreign_principal_denied(court,field):
 o,a,fx,r,_=court;old=slot(fx);foreign=ref('PV3N-coherent-'+field);new=replace(old,**{field:foreign});e,p=mutate_work(fx,old,new)
 reg=replace(fx['register'],obligations=tuple(replace(x,**{field:foreign}) if x.obligation_key==('PV2-ADULT-A','PAIR') else x for x in fx['register'].obligations))
 with pytest.raises(ValueError,match='REQUEST_REGISTER_NOT_INSTALLED_ROOT'):a.run_sourcefree_with_register(**dict(args(fx),expected=e,selected_scopes=p,register=reg))
 assert a.read_current_consumer_material(fx['register'],r)['servable']

@pytest.mark.parametrize('mode',['unknown_item','household','form','role','query','held','drop_held'])
def test_independent_scientific_identity_denials(court,mode):
 o,a,fx,r,_=court;old=slot(fx,kind='ORDERED' if mode=='held' else 'PAIR')
 if mode=='drop_held':
  from rawlsing_next.pre553_original_identity_v2k_successor_candidate import FrozenOriginalExpected,ORIGIN
  e=FrozenOriginalExpected.from_records(tuple(x for x in fx['records'] if x.legacy.is_runnable),input_origin=ORIGIN);p=fx['plans']
 else:
  if mode=='unknown_item':new=replace(old,original=replace(old.original,original_item_scope_ref=ref('UNKNOWN-ITEM-SCOPE')))
  elif mode=='household':new=replace(old,original=replace(old.original,respondent_unit='HOUSEHOLD'))
  elif mode=='form':new=replace(old,original=replace(old.original,form='F2'),legacy=replace(old.legacy,form='F2'))
  elif mode=='role':new=replace(old,legacy=replace(old.legacy,semantic_roles=('TARGET','CONDITIONER')))
  elif mode=='query':new=replace(old,legacy=replace(old.legacy,query_ref=fx['inputs'][0]['reverse_query'].ref))
  else:new=replace(old,legacy=replace(old.legacy,slot='PV3N-HELD-SWAP'))
  e,p=mutate_work(fx,old,new)
 with pytest.raises(ValueError):a.run_sourcefree_with_register(**dict(args(fx),expected=e,selected_scopes=p))
 assert a.read_current_consumer_material(fx['register'],r)['servable']

@pytest.mark.parametrize('field,value',[('issuer','FOREIGN'),('grant','REAL_ORIGINAL'),('ceiling',('PRODUCTION',)),('revoked',True)])
def test_independent_grant_denials_do_not_mutate_owner(court,field,value):
 o,a,fx,r,_=court;before=copy.deepcopy(o._state);reg=replace(fx['register'],fixture_use_grant=replace(fx['register'].fixture_use_grant,**{field:value}))
 with pytest.raises(ValueError):a.read_current_consumer_material(reg,r)
 with pytest.raises(ValueError):a.run_sourcefree_with_register(**dict(args(fx),register=reg))
 assert o._state==before

@pytest.mark.parametrize('mode',['support999','material','roles','conditioner','query','fact','risk'])
def test_independent_current_payload_and_role_rejections(court,mode):
 o,a,fx,r,_=court;bad=copy.deepcopy(r);m=bad['links'][0]['consumer_material']
 if mode=='support999':m['conditional_count_profile'][0]['condition_denominator_support']=999
 if mode=='material':bad['links'][0].pop('consumer_material')
 if mode=='roles':m.pop('roles')
 if mode=='conditioner':m['roles'].pop('CONDITIONER')
 if mode in ('query','fact','risk'):m.pop({'query':'producer_query_ref','fact':'producer_fact_ref','risk':'risk_set_ref'}[mode])
 with pytest.raises(ValueError):a.read_current_consumer_material(fx['register'],bad)
 with pytest.raises(ValueError):validate_consumer_roles_against_declared(bad['links'],fx['register'])
 assert a.read_current_consumer_material(fx['register'],r)['servable']

def test_independent_current_nested_alias_and_request_owner_replacement(court):
 o,a,fx,r,current=court;read=a.read_current_consumer_material(fx['register'],r);read['links'][0]['consumer_material']['conditional_count_profile'][0]['condition_denominator_support']=999
 assert a.read_current_consumer_material(fx['register'],r)==current
 with pytest.raises(TypeError):a.run_sourcefree_with_register(**args(fx),fixture_owner=FixtureOwnerControl('R2_Y1'))
 with pytest.raises(FrozenInstanceError):a._owner=FixtureOwnerControl('R2_Y1').client()

@pytest.mark.parametrize('profile_name',['R2_Y1','R1_Y0'])
def test_independent_real_source_counterfactuals(court,tmp_path,profile_name):
 o,a,fx,base,_=court
 with Trace() as trace:
  owner,api,mutant,installed=prepare(tmp_path/'ledger',profile_name)
  result=api.run_sourcefree_with_register(**args(mutant));reading=api.read_current_consumer_material(mutant['register'],result)
 assert reading['servable'];profiles={}
 for l in result['links']:
  ns=l['original_identity']['original']['respondent_namespace'];slotname=l['original_identity']['operation']['slot'];p=profile(l['consumer_material']);profiles[ns+'|'+slotname]=p
  prev=next(x for x in base['links'] if x['original_identity']['original']['respondent_namespace']==ns and x['original_identity']['operation']['slot']==slotname)
  if ns=='PV2-ADULT-B':assert l==prev
  elif profile_name=='R2_Y1' and slotname=='PAIR':assert p=={'0':{'denominator':1,'targets':{'0':0,'1':1}},'1':{'denominator':1,'targets':{'0':0,'1':1}}}
  elif profile_name=='R2_Y1' and slotname=='B':assert p['1']=={'denominator':2,'targets':{'0':1,'1':1}}
  elif profile_name=='R1_Y0' and slotname in ('PAIR','DISCOVERY'):
   assert p['1']=={'denominator':1,'targets':{'0':1,'1':0}}
   assert l['producer_result_ref']!=prev['producer_result_ref'] and l['consumer_ref']!=prev['consumer_ref']
 write(E/(profile_name+'.json'),dict(installed=installed,report=result,current=reading,profiles=profiles,trace=trace.data(),source_cells=[dict(namespace=x['universe'].respondent_namespace,cells=[dict(row=c.row_ordinal,item=c.variable_name,value=c.raw_value) for c in x['fx']['stream'].cell_iter_factory()]) for x in mutant['inputs']]))

def test_actual_installed_policy_filesystem_writer_is_outside_issuer_boundary(court,tmp_path):
 _,_,fx,_,_=court;policy=tmp_path/'trusted_owner.json';o=FixtureOwnerControl(policy_path=policy,provision=True);api=RequestAPI(o.client(),o._attest);r=api.run_sourcefree_with_register(**args(fx));history=copy.deepcopy(r)
 b_before=api.read_current_consumer_material(fx['register'],r,namespace='PV2-ADULT-B');o.withdraw('PV2-ADULT-A')
 assert not api.read_current_consumer_material(fx['register'],r,namespace='PV2-ADULT-A')['servable']
 assert api.read_current_consumer_material(fx['register'],r,namespace='PV2-ADULT-B')==b_before
 # Explicit stronger attacker: actual arbitrary write to trusted deployment policy.
 payload=json.loads(policy.read_text());payload['decisions']['PV2-ADULT-A'].update(withdrawn=False,clock=3,asof=3,reason=None);policy.write_text(json.dumps(payload))
 actual=api.read_current_consumer_material(fx['register'],r,namespace='PV2-ADULT-A');assert actual['servable'] and r==history
 write(E/'actual_policy_writer_outside_perimeter.json',dict(attacker='OS filesystem writer of trusted owner policy, outside request API',observed=actual,scope_verdict='REAL_ORIGINAL_SIGNED_MONOTONIC_ISSUER_HOLD',scoped_request_RED=False))

def test_independent_edition_epoch_and_revocation_current_reads(court,tmp_path):
 _,_,fx,_,_=court;o=FixtureOwnerControl(policy_path=tmp_path/'owner.json',provision=True);a=RequestAPI(o.client(),o._attest);r=a.run_sourcefree_with_register(**args(fx));historical=copy.deepcopy(r);oldreg=copy.deepcopy(fx['register'])
 b=a.read_current_consumer_material(oldreg,r,namespace='PV2-ADULT-B');o.advance('PV2-ADULT-A')
 assert not a.read_current_consumer_material(oldreg,r,namespace='PV2-ADULT-A',clock=1,asof=1)['servable']
 o.advance('PV2-ADULT-A',edition='DIFFERENT_NATIVE_EDITION');assert not a.read_current_consumer_material(oldreg,r,namespace='PV2-ADULT-A')['servable']
 o.withdraw('PV2-ADULT-A');assert not a.read_current_consumer_material(oldreg,r,namespace='PV2-ADULT-A')['servable']
 assert a.read_current_consumer_material(oldreg,r,namespace='PV2-ADULT-B')==b and r==historical
