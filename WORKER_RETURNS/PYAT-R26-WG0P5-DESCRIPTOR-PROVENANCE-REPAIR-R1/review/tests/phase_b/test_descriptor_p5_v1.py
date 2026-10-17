"""Prospective P5 law: every forged descriptor refuses BEFORE I03.
First2 WG0L counterexamples originally asserted absence of forged served metadata;
this explicit versioned repair wrapper accepts only typed early rejection, with
no native query and no issuance. Original test source stays unchanged.
"""
import copy,json,sys,importlib.util
from dataclasses import fields,replace
import pytest
from phase_b_support_v1 import *
P5ROOT=R.parent
FROZEN=json.loads((P5ROOT/'HOSTILE_EXPECTATIONS.json').read_text())

def mutate_spec(p,field,value):
 specs=dict(p.op_specs);specs[OP]=replace(specs[OP],**{field:value});return replace(p,op_specs=specs)
def value_for(p,field,value):
 if field=='query':return p.op_specs['OP-WG0P-ORD-05-MARGINAL'].query
 if field=='predicate':return p.op_specs['OP-WG0P-ORD-05-MARGINAL'].predicate
 if field=='disposition':return w.Disposition.HELD
 if field in ('targets','native_item_ids','member_ids'):return tuple((tuple(v) if isinstance(v,list) else v) for v in value)
 return value

def deny_before_i03(p,fn):
 calls=[];before=p.fact_custody.snapshot();journal=copy.deepcopy(p.fixture_owner._issued())
 sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises(w.IdentityError):fn()
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)
 assert p.fact_custody.snapshot()==before and p.fixture_owner._issued()==journal
 return calls

@pytest.mark.parametrize('attack',FROZEN['attacks'],ids=[x['field'] for x in FROZEN['attacks']])
def test_every_bound_descriptor_field_rejects_before_i03(attack):
 p=plan();field=attack['field'];bad=mutate_spec(p,field,value_for(p,field,attack['replacement']))
 assert bad.contract==p.contract
 calls=deny_before_i03(p,lambda:w.make_executor(bad)(p.units_by_op[OP]))
 dump(P5ROOT/'observations'/('descriptor_'+field+'.json'),{'field':field,'refused_before_I03':True,'calls':calls,'bound_fields':[f.name for f in fields(w.BoundSpec)],'actual_type':'IdentityError'})

@pytest.mark.parametrize('field,value',[('source_edition','FORGED_CALLER_EDITION'),('native_item_ids',('FOREIGN_NATIVE_ITEM',)),('release_tag','REL-A-W2')])
def test_same_three_wg0l_failures_cannot_publish_forged_metadata(field,value):
 p=plan();bad=mutate_spec(p,field,value)
 deny_before_i03(p,lambda:w.run_plan(bad,w.make_executor(bad)))
 _,rs,_=execute(p)
 with pytest.raises(w.IdentityError):w.consumer_effects(bad,rs)

@pytest.mark.parametrize('field,value',[('source_edition','FORGED_CALLER_EDITION'),('release_tag','REL-A-W2'),('qrefs',{}),('risk_refs',{})])
def test_mutated_ingest_view_cannot_self_sign_a_compiled_plan(field,value):
 releases=w.build_all_releases();releases['REL-A-W1']=replace(releases['REL-A-W1'],**{field:value})
 with pytest.raises(w.IdentityError):plan(releases=releases)

@pytest.mark.parametrize('field,value',[('source_edition','FORGED_CALLER_EDITION'),('native_item_ids',('FOREIGN_NATIVE_ITEM',)),('release_tag','REL-A-W2')])
def test_recomputed_caller_contract_is_not_independent_authority(field,value):
 p=plan();bad=mutate_spec(p,field,value)
 recomputed=w._registered_contract(bad.manifest,bad.science_root,bad.freeze_hash,bad.units_by_op,bad.op_specs)
 bad=replace(bad,contract=w.canonical(recomputed))
 deny_before_i03(p,lambda:w.make_executor(bad)(p.units_by_op[OP]))

def test_registered_descriptor_binds_all_dataclass_fields_and_native_refs():
 p=plan();payload=json.loads(p.contract)
 for key,spec in p.op_specs.items():
  d=payload['bindings'][key]['descriptor'];assert set(d)=={f.name for f in fields(w.BoundSpec)}
  assert d['source_edition']==p.releases[spec.release_tag].source_edition
  assert d['query']['ref']==spec.query.ref.as_dict() and d['predicate']['ref']==spec.predicate.ref.as_dict()
  assert set(d['native_item_ids'])==set(spec.native_item_ids)

# Preserve and execute the original release-tag counterexample body unchanged.
sp=importlib.util.spec_from_file_location('_original_descriptor_court',R/'tests/phase_b/test_additional_descriptor_binding_red.py')
old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
test_original_release_tag_counterexample=old.test_copied_release_descriptor_refused_before_native_query

@pytest.mark.parametrize('field,value',[('source_edition','FORGED_CALLER_EDITION'),('native_item_ids',('FOREIGN_NATIVE_ITEM',))])
def test_original_edition_and_item_body_with_explicit_early_refusal_wrapper(field,value):
 calls=[];sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises(w.IdentityError):old.test_bound_descriptor_cannot_change_served_provenance(field,value)
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)
