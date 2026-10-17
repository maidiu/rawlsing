"""Reviewer transport on inherited full module. Never imports WG0P5 by itself."""
from phase_b_support_v1 import *
from dataclasses import replace
from types import MappingProxyType

class DescriptorCourt:
 def __init__(self):
  self.physical=verified_modules();self.out=R/'observations/descriptor_runs'/os.environ.get('WG0M_RUN','phase_a_original_P4');self.out.mkdir(parents=True,exist_ok=True)
 def execute_case(self,group,case):
  p=plan();unit=p.units_by_op[OP];old=p.op_specs[OP];rs=None;stimulus={}
  if group=='fact':
   _,rs,consumer=execute(p);entry=copy.deepcopy(consumer[OP][0]);key=w.ref(entry['fact_ref']).key
   if case=='denominator_rehash':entry['denominator']=999;entry['native_fact']['semantic_fields']['raw_denominator_support']=999
   elif case=='numerator_same_total_swap':entry['cells'][0]['n'],entry['cells'][1]['n']=entry['cells'][1]['n'],entry['cells'][0]['n']
   elif case=='membership_same_cardinality':
    members=entry['native_fact']['semantic_fields']['denominator_member_refs'];members[0]=p.releases['REL-A-W2'].respondent_keys['R11'].as_dict()
   elif case=='native_item_ids_projection':entry['native_item_ids']=['FOREIGN_NATIVE_ITEM']
   elif case=='source_edition_projection':entry['source_edition']='FORGED_CALLER_EDITION'
   snapshot=p.fact_custody.snapshot();snapshot['facts'][key]=entry;snapshot['hashes'][key]=w.digest(entry)
   c=w.FactCustody();c.restore(snapshot);p=replace(p,fact_custody=c);stimulus={'forged_entry':entry}
  elif group=='descriptor':
   mutations={'source_edition':{'source_edition':'FORGED_CALLER_EDITION'},'native_item_ids':{'native_item_ids':('FOREIGN_NATIVE_ITEM',)},'release_tag':{'release_tag':'REL-A-W2'},'risk_name':{'risk_name':'R_ORD2'},'targets_other_form':{'targets':(('Q-RT-C',('yes','no')),)},'member_ids_same_cardinality':{'member_ids':('R1','R2','R3','R4','R5','FOREIGN')},'member_ids_denominator_drop':{'member_ids':old.member_ids[:-1]},'grant_withdrawn':{'grant':'WITHDRAWN'},'grant_foreign':{'grant':'REAL_SOURCE_SIGNED_PERMISSION'},'disposition_HELD':{'disposition':w.Disposition.HELD},'full_identity_hash':{'full_identity_hash':'0'*64},'op_id':{'op_id':'OP-FOREIGN'},'target_domain_same_cardinality':{'targets':(('Q-ORD-A',('9','1','2','3','0')),)},'foreign_release_tag':{'release_tag':'FOREIGN_RELEASE'}}
   specs=dict(p.op_specs)
   if case=='swapped_complete_spec':specs[OP]=specs['OP-WG0P-ORD-05-MARGINAL'];stimulus={'complete_spec_from':'OP-WG0P-ORD-05-MARGINAL'}
   else:stimulus=mutations[case];specs[OP]=replace(old,**stimulus)
   p=replace(p,op_specs=specs)
  elif group=='source':
   rels=dict(p.releases);rel=rels['REL-A-W1'];other=rels['REL-A-W2']
   if case=='owner_revocation':p.fixture_owner.revoke('REL-A-W1')
   elif case in ('owner_clock_change','owner_epoch_change'):
    state=p.fixture_owner.state();state['known_at' if case=='owner_clock_change' else 'epoch']='WG0M_CHANGED';w.atomic_write(p.fixture_owner.directory/'current.json',w.canonical(state))
   else:
    if case=='release_source_edition':rel=replace(rel,source_edition='FORGED_CALLER_EDITION')
    elif case=='release_source_artifact':rel=replace(rel,source_artifact_ref=other.source_artifact_ref)
    elif case=='release_universe':rel=replace(rel,universe_ref=other.universe_ref)
    elif case=='release_risk_ref':refs=dict(rel.risk_refs);refs['R_ORD']=other.risk_refs['R_ORD2'];rel=replace(rel,risk_refs=refs)
    elif case=='release_form_ref':refs=dict(rel.qrefs);refs['Q-ORD-A']=other.qrefs['Q-ORD-A'];rel=replace(rel,qrefs=refs)
    rels['REL-A-W1']=rel;p=replace(p,releases=rels)
   stimulus={'source_attack':case}
  elif group=='copy':
   specs=dict(p.op_specs)
   if case=='same_cardinality_spec_swap':
    a='OP-WG0P-ORD-05-MARGINAL';specs[OP],specs[a]=specs[a],specs[OP]
   else:specs[OP]=replace(old,source_edition='FORGED_CALLER_EDITION')
   if case=='shallow_copied_plan':p=copy.copy(p);object.__setattr__(p,'op_specs',specs)
   elif case=='copied_mapping':p=replace(p,op_specs=MappingProxyType(specs))
   elif case=='self_rehashed_contract':
    d=json.loads(p.contract);d['bindings'][OP]['descriptor']={'source_edition':'FORGED_CALLER_EDITION'};p=replace(p,op_specs=specs,contract=w.canonical(d))
   elif case=='changed_semantic_description':p=replace(p,op_specs=specs,freeze_hash=w.digest({'relabelled':'caller-controlled semantics'}))
   else:p=replace(p,op_specs=specs)
   stimulus={'copy_attack':case}
  else:raise RuntimeError('Unknown group')
  calls=[];exception=None;reason=None;effects={};receipts=[]
  sys.setprofile(profile_calls(calls))
  try:
   # The ordinary callback is called directly first: native Batch may otherwise
   # swallow an untyped exception and record FAILED, hiding admission defects.
   if group!='fact':w.make_executor(p)(unit)
   if group!='fact':_,receipts,effects=execute(p)
   else:effects=w.consumer_effects(p,rs)
  except Exception as e:exception=type(e).__name__;reason=str(e)
  finally:sys.setprofile(None)
  path=self.out/(group+'__'+case+'.json')
  result={'group':group,'case':case,'attempted':True,'exception_type':exception,'exception_reason':reason,'typed_refusal':None,'served_positive':bool(effects),'consumer':effects,'new_I03_calls':sum(c['name']=='execute_empirical_query' and c['file'].endswith('pre553_empirical_query.py') for c in calls),'calls':calls,'stimulus':w._plain(stimulus),'physical_modules':self.physical,'candidate_module':w.__file__,'actual_process_argv':[sys.executable,*sys.argv],'raw_path':str(path)}
  dump(path,result);return result
