"""Reviewer-owned versioned API transport for the unchanged 65 assertions.
Every case writes its actual stimulus and output. Author helpers are not used.
"""
import copy, hashlib, json, os, pathlib, shutil, subprocess, sys, uuid
from dataclasses import replace
from phase_b_support_v1 import *

class Adapter:
 candidate_sha='20d781c8502662bf788b60b828e46df55898d687'
 def __init__(self,oracle):
  self.oracle=oracle;self.physical=verified_modules()
  self.owner_source_hashes_verified=True;self.actual_imports_verified=True
  self.out=R/'observations/phase_b/controls_v1_final';self.out.mkdir(parents=True,exist_ok=True)
  self.cold_folder=None
 def refusal(self,fn):
  try:
   value=fn()
   return {'attempted':True,'exception_type':None,'typed_state':None,'served_positive':True,'returned':w._plain(value)}
  except AdmissionRefused as e:
   return {'attempted':True,'exception_type':None,'typed_state':'HELD','served_positive':False,'actual_admission_return':e.value,'mapping':'Candidate add_item returned CONFLICTING_NATIVE_ITEM_IDENTITY; no executable plan or positive result was admitted.'}
  except (w.IdentityError,w.FrontierError,w.RevocationError,w.ColdRestartError,w.NativeDataError,w.BatchIntegrityError,KeyError,ValueError,TypeError) as e:
   return {'attempted':True,'exception_type':type(e).__name__,'reason':str(e),'typed_state':None,'served_positive':False}
 def execute_case(self,group,case):
  initial=copy.deepcopy(w.COHORTS);calls=[]
  sys.setprofile(profile_calls(calls))
  try:
   result=getattr(self,'case_'+group)(case)
  finally:
   sys.setprofile(None);w.COHORTS.clear();w.COHORTS.update(initial)
  path=self.out/(group+'__'+case+'.json')
  result.update(case=case,group=group,candidate_sha=self.candidate_sha,actual_command=[sys.executable,'-m','pytest','tests/test_precommitted_phase_b.py'],physical_module_files=self.physical,execution_evidence_path=str(path),calls=calls)
  dump(path,result);return result
 def case_frontier(self,case):
  b=builder();ops=b.enumerate();held=next(o for o in ops if o.disposition.value=='HELD');inad=next(o for o in ops if o.disposition.value=='INADMISSIBLE')
  if case=='consumer_frontier_mutation':
   p=plan();_,rs,_=execute(p);rr=copy.deepcopy(list(p.frontier_receipts));rr[0]['disposition_reason']='FORGED'
   return self.refusal(lambda:w.consumer_effects(replace(p,frontier_receipts=tuple(rr)),rs))
  if case=='equal_count_source_permission_swap':
   its=items();its[0]=replace(its[0],grant='CALLER_FORGED_PERMISSION')
   out=self.refusal(lambda:plan(its,ops=ops));out['submitted_frontier']=rows(ops);out['mutated_native_item']=vars(its[0]);return out
  if case=='circular_expected_list':
   altered=[o for o in ops if o is not held]
   return self.refusal(lambda:w.validate_frontier_receipts([w.receipt_row(o) for o in altered],altered))
  if case=='duplicate_changed_semantics':altered=ops+[replace(held,target='FOREIGN')]
  elif case=='omit_HELD':altered=[o for o in ops if o is not held]
  elif case=='omit_INADMISSIBLE':altered=[o for o in ops if o is not inad]
  else:
   field,value={'equal_count_HELD_identity_swap':('op_id','FOREIGN-HELD'),'equal_count_reason_forgery':('disposition_reason','FORGED'),'equal_count_target_swap':('target','FOREIGN'),'equal_count_source_permission_swap':('disposition',w.Disposition.PRODUCED)}[case]
   altered=[replace(o,**{field:value}) if o is held else o for o in ops]
  out=self.refusal(lambda:plan(ops=altered));out['submitted_frontier']=rows(altered);return out
 def case_native(self,case):
  fields={'options':('options',('1','0','2','3','9')),'missing_codes':('missing_codes',()),'routing':('route_evidence','FORGED_ROUTING'),'wave':('wave','W2'),'unit':('unit','household'),'response_kind':('response_kind','MULTIPLE_RESPONSE'),'source_id':('source_id','WG0P-SRC-B'),'form_id':('form_id','Q-RT-C')}
  if case in fields:
   its=items();field,value=fields[case];its[0]=replace(its[0],**{field:value})
   out=self.refusal(lambda:execute(plan(its)));out['mutated_native_item']=vars(its[0]);return out
  cohort=w.COHORTS['REL-A-W1']
  if case=='MR_indicator_disagreement':
   cohort['native_option_sets']['H1']={'none'}
   return self.refusal(lambda:w.build_all_releases())
  if case in ('invalid_negative','invalid_foreign'):
   cohort['rows'][0]['responses']['Q-ORD-A']='-1' if case=='invalid_negative' else 'FOREIGN'
   return self.refusal(lambda:w.build_all_releases())
  if case=='zero_risk_vs_observed_zero':
   p=plan();_,rs,e=execute(p);rel=p.releases['REL-A-W1'];pred=w._branch_predicate_for(rel,(),tag='WG0L-empty',risk_name='R_ORD');q=w._query_for(rel,pred,(('Q-ORD-A',('0','1','2','3','9')),),risk='R_ORD',tag='WG0L-empty')
   f=w.execute_empirical_query(repository=rel.repo,query=q,predicate=pred,authority_registry=w._registry_for(rel),release_refs=(rel.release_ref,)).facts[0]
   zero=next(c for c in e[OP][0]['cells'] if c['cell']=='9')
   return {'empty_state':f.typed_state,'empty_denominator':f.raw_denominator_support,'observed_zero_state':zero['state'],'supported_denominator':e[OP][0]['denominator'],'empty_fact':f.semantic_projection(),'observed_fact':e[OP][0]}
  if case=='missing9_not_substantive':cohort['rows'][0]['responses']['Q-ORD-A']='9'
  elif case=='missing_observation':del cohort['rows'][0]['responses']['Q-ORD-A']
  else:raise RuntimeError('unmapped native case '+case)
  p=plan();_,rs,e=execute(p);rel=p.releases['REL-A-W1'];actual=rel.repo.resolve_release_exact(rel.release_ref)
  events=[o for o in (*actual.public_objects,*actual.internal_records) if type(o).__name__=='RespondentEvent']
  if case=='missing9_not_substantive':
   n=sum(o.raw_response_value=='9' and o.response_state=='SUBSTANTIVE_RESPONSE' for o in events)
   return {'missing9_substantive_events':n,'cell9_numerator':next(c['n'] for c in e[OP][0]['cells'] if c['cell']=='9'),'consumer':e,'events':[o.semantic_projection() for o in events]}
  invented=[o for o in events if w._plain(o.scoped_respondent_ref)==rel.respondent_keys['R1'].as_dict() and w._plain(o.native_question_ref)==rel.qrefs['Q-ORD-A'].as_dict()]
  risk=set(cohort['risk_sets']['R_ORD']['Q-ORD-A'])
  return {'invented_observation_count':len(invented),'denominator':e[OP][0]['denominator'],'typed_state':e[OP][0]['typed_state'],'independently_reconstructed_risk_denominator':len(risk),'consumer':e}
 def case_binding(self,case):
  if case in ('source_leaf_mutation','unrelated_W2_exact_stability'):
   p=plan();_,rs,before=execute(p)
   w.COHORTS['REL-A-W1']['rows'][0]['responses']['Q-ORD-A']='3'
   q=plan();_,tt,after=execute(q)
   if case=='source_leaf_mutation':
    return {'affected_counts_before':before[OP][0]['cells'],'affected_counts_after':after[OP][0]['cells'],'source_bytes_hash_before':p.releases['REL-A-W1'].source_artifact_ref.content_hash,'source_bytes_hash_after':q.releases['REL-A-W1'].source_artifact_ref.content_hash,'actual_fact_ref_before':before[OP][0]['fact_ref'],'actual_fact_ref_after':after[OP][0]['fact_ref']}
   return {'W2_release_before':p.releases['REL-A-W2'].release_ref.as_dict(),'W2_release_after':q.releases['REL-A-W2'].release_ref.as_dict(),'W2_values_before':before['OP-WG0P-ORD-05-MARGINAL'],'W2_values_after':after['OP-WG0P-ORD-05-MARGINAL']}
  p=plan()
  if case=='W2_wave_identity':return {'raw_waves':{tag:p.releases[tag].repo.resolve_object_exact(p.releases[tag].universe_ref).raw_wave for tag in ('REL-A-W2','REL-B-W2')}}
  unit=p.units_by_op[OP]
  if case.startswith('wrong_unit'):
   field,value={'wrong_unit_release':('release_refs',(p.releases['REL-A-W2'].release_ref,)),'wrong_unit_job_ref':('job_ref',p.units_by_op['OP-WG0P-ORD-05-MARGINAL'].job_ref),'wrong_unit_semantic_input':('semantic_input_refs',())}[case]
   return self.refusal(lambda:w.make_executor(p)(replace(unit,**{field:value})))
  _,rs,_=execute(p)
  if case=='query_predicate_swap':
   specs=dict(p.op_specs);specs[OP]=replace(specs[OP],predicate=specs['OP-WG0P-ORD-05-MARGINAL'].predicate)
   return self.refusal(lambda:w.consumer_effects(replace(p,op_specs=specs),rs))
  if case=='result_reference_swap':
   old=next(r for r in rs if r.unit_ref==unit.unit_ref);other=next(r for r in rs if r is not old)
   return self.refusal(lambda:w.consumer_effects(p,[replace(r,result_refs=other.result_refs) if r is old else r for r in rs]))
  if case=='source_authority_change':
   rels=dict(p.releases);rels['REL-A-W1']=replace(rels['REL-A-W1'],qauth=rels['REL-A-W2'].qauth)
   return self.refusal(lambda:w.consumer_effects(replace(p,releases=rels),rs))
  raise RuntimeError('unmapped binding '+case)
 def case_custody(self,case):
  p=plan();_,rs,e=execute(p);entry=copy.deepcopy(e[OP][0]);key=w.ref(entry['fact_ref']).key
  if case in ('store_alias','read_alias','snapshot_alias','restore_alias'):
   c=w.FactCustody();c.store(key,entry);before=c.read(key)
   if case=='store_alias':entry['cells'][0]['n']=991
   elif case=='read_alias':c.read(key)['cells'][0]['n']=992
   elif case=='snapshot_alias':c.snapshot()['facts'][key]['cells'][0]['n']=993
   else:
    snap=c.snapshot();other=w.FactCustody();other.restore(snap);snap['facts'][key]['cells'][0]['n']=994;c=other
   # Read the unchanged archived bytes through the real consumer, not only a dict comparison.
   for r in rs:
    for f in r.result_refs:
     if f.key!=key:c.store(f.key,p.fact_custody.read(f.key))
   after=w.consumer_effects(replace(p,fact_custody=c),rs)[OP][0]
   return {'original_fact_before':before,'original_fact_after':c.read(key),'read_support_before':e[OP][0]['denominator'],'read_support_after':after['denominator']}
  if case=='same_key_collision':
   entry['denominator']=999;return self.refusal(lambda:p.fact_custody.store(key,entry))
  if case=='immediate_restore_validation':
   snap=p.fact_custody.snapshot();snap['facts'][key]['denominator']=999
   return self.refusal(lambda:w.FactCustody().restore(snap))
  if case=='fact_projection_ref_hash':
   entry['native_fact']['semantic_fields']['raw_denominator_support']=999
   return self.refusal(lambda:w._validate_entry(key,entry,p))
  if case=='rehashed_changed_fact':
   proj=entry['native_fact'];proj['semantic_fields']['raw_denominator_support']=999
   native=w.EmpiricalFact(**{k:v for k,v in proj.items() if k!='semantic_fields'},**proj['semantic_fields'])
   forged=w._plain(w._fact_entry(OP,p.op_specs[OP],native))
   # A fresh internally valid ref is still not an issued native computation result.
   w._validate_entry(native.ref.key,forged,p)
   return self.refusal(lambda:p.fixture_owner.assert_fact_issued(native.ref.key,forged))
  raise RuntimeError('unmapped custody '+case)
 def case_authority(self,case):
  if case=='fresh_process_revocation':return self.cold_attack('revoked_owner')
  p=plan();_,rs,e=execute(p)
  if case=='requester_forged_grant':
   p.source_issuer_grant['grant']='ISSUED_ORIGINAL_SOURCE_PERMISSION'
  elif case=='self_rehashed_issuer':
   snap=json.loads(p.owner_snapshot);snap['owner']='CALLER_ISSUER';p=replace(p,owner_snapshot=w.canonical(snap))
  elif case in ('historical_snapshot_after_revocation','current_grant_independent_of_plan'):
   p.fixture_owner.revoke('REL-A-W1');p.source_issuer_grant['grant']='GRANTED_FIXTURE'
  elif case=='stale_source_edition':
   rels=dict(p.releases);rels['REL-A-W1']=replace(rels['REL-A-W1'],source_edition='STALE-EDITION');p=replace(p,releases=rels)
  elif case=='stale_knowledge_clock':
   state=p.fixture_owner.state();state['known_at']='2026-02-01';w.atomic_write(p.fixture_owner.directory/'current.json',w.canonical(state))
  else:raise RuntimeError('unmapped authority '+case)
  return self.refusal(lambda:w.consumer_effects(p,rs))
 def case_conditional(self,case):
  if case=='original25_unchanged':return {'frontier':rows(builder().enumerate())}
  if case in ('same_grain_without_person_HOLD','split_ballot_HOLD','cross_wave_HOLD','household_person_INADMISSIBLE'):
   ops=builder().enumerate()
   if case=='same_grain_without_person_HOLD':o=next(o for o in ops if o.op_class=='CONDITIONAL' and o.target=='WG0P-ORD-01' and o.conditioners==('WG0P-ROUTED-03',))
   elif case=='split_ballot_HOLD':
    its=items();its[2]=replace(its[2],route_evidence='SPLIT_BALLOT_NO_JOINT_PERSON');o=next(o for o in builder(its).enumerate() if o.op_class=='CONDITIONAL' and o.target=='WG0P-ORD-01' and o.conditioners==('WG0P-ROUTED-03',))
   elif case=='cross_wave_HOLD':o=next(o for o in ops if o.op_class=='CONDITIONAL' and o.target=='WG0P-ORD-01' and o.conditioners==('WG0P-ORD-05',))
   else:o=next(o for o in ops if o.op_class=='CONDITIONAL' and o.target=='WG0P-ORD-01' and o.conditioners==('WG0P-HH-MR-02',))
   return {'attempted':True,'exception_type':None,'typed_state':o.disposition.value,'served_positive':o.disposition.value=='PRODUCED','operation':w.receipt_row(o)}
  if case=='second_frontier_exact_no_drop':
   actual=rows(builder(joint_items(),True).enumerate());forged=copy.deepcopy(actual);forged[0]['disposition_reason']='FORGED'
   f=self.refusal(lambda:w.validate_frontier_receipts(forged,mode='conditional4'))
   missing=self.refusal(lambda:w.validate_frontier_receipts(actual[1:],mode='conditional4'))
   return {'submitted_second_frontier':actual,'independently_frozen_second_frontier':SECOND['operations'],'register_frozen_before_execution':self.register_committed(),'equal_count_forgery_rejected':f['exception_type'] is not None,'omission_rejected':missing['exception_type'] is not None,'forgery_result':f,'omission_result':missing}
  if case=='ordinary_full_chain_yes1_no1_over2':
   calls=[];sys.setprofile(profile_calls(calls));p=plan(joint=True);_,rs,e=execute(p);sys.setprofile(None)
   f=e[JOP][0];refs=f['native_fact']['semantic_fields']['denominator_member_refs'];rel=p.releases['REL-A-W1']
   members=sorted(k for k,v in rel.respondent_keys.items() if v.as_dict() in refs)
   names=[c['name'] for c in calls]
   route=[]
   for name,label in [('__init__','WorkloadBuilder'),('build_executable_plan','build_executable_plan'),('make_executor','make_executor'),('run_plan','run_plan'),('run','accepted_BatchExecutionRunner'),('consumer_effects','consumer_effects')]:
    if name=='run_plan':present='run_plan' in names
    elif name=='__init__':present=any(c['name']=='__init__' and c['file'].endswith('wg0p4_workload.py') for c in calls)
    else:present=name in names
    if present:route.append(label)
   return {'route':route,'separate_demo_function_called':any(x in names for x in ('execute_positive_conditional','build_positive_conditional_frontier')),'denominator':f['denominator'],'counts':{c['cell']:c['n'] for c in f['cells']},'same_respondents':members,'owner_query_calls':sum(c['name']=='execute_empirical_query' and c['file'].endswith('pre553_empirical_query.py') for c in calls),'owner_batch_calls':sum(c['name']=='run' and c['file'].endswith('pre553_batch_runner.py') for c in calls),'second_frontier_verified_against_independent_register':sorted(list(p.frontier_receipts),key=lambda x:x['op_id'])==SECOND['operations'],'original_frontier':rows(builder().enumerate()),'conditional_calls':calls,'consumer':e}
  raise RuntimeError('unmapped conditional '+case)
 def register_committed(self):
  path='WORKER_RETURNS/'+R.name+'/observations/phase_b/reviewer_second_frontier_register.json'
  cut=subprocess.run(['git','show','HEAD:'+path],cwd=R,capture_output=True)
  return cut.returncode==0 and cut.stdout==(R/'observations/phase_b/reviewer_second_frontier_register.json').read_bytes()
 def ensure_cold(self):
  if self.cold_folder is not None:return
  self.cold_folder=self.out/('cold-'+uuid.uuid4().hex);self.cold_folder.mkdir()
  worker=R/'repro/phase_b_cold_worker_v1.py';commands=[]
  for mode in ('crash','resume'):
   cmd=[sys.executable,str(worker),mode,str(self.cold_folder)]
   proc=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
   commands.append({'command':cmd,'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
   dump(self.cold_folder/'commands.json',commands)
   if proc.returncode!=(23 if mode=='crash' else 0):raise RuntimeError('cold child failed '+str(commands[-1]))
 def case_cold(self,case):
  if case.endswith('_refuse'):
   return self.cold_attack({'missing_fact_refuse':'missing_fact','changed_receipt_provenance_refuse':'receipt','self_rehashed_checkpoint_refuse':'self_rehash','source_edition_currentness_refuse':'source_edition'}[case])
  self.ensure_cold();a=json.loads((self.cold_folder/'crash.json').read_text());b=json.loads((self.cold_folder/'resume.json').read_text());cmd=json.loads((self.cold_folder/'commands.json').read_text())
  durable=a['durability_calls'];original=a['receipt'];roundtrip=w.receipt_to_json(w.receipt_from_json(original))
  return {'checkpoint_exit':cmd[0]['exit'],'first_pid':a['pid'],'second_pid':b['pid'],'first_I03_calls':sum(c['name']=='execute_empirical_query' and c['file'].endswith('pre553_empirical_query.py') for c in a['calls']),'second_I03_calls':sum(c['name']=='execute_empirical_query' and c['file'].endswith('pre553_empirical_query.py') for c in b['calls']),'manifest_before':a['manifest'],'manifest_after':b['manifest'],'manifest_units':a['unit_count'],'original_receipt_hash':original['receipt_hash'],'final_receipt_hashes':[r['receipt_hash'] for r in b['receipts']],'owner_receipt_class':b['receipt_class'],'fsync_file':any(c.get('kind')=='file' for c in durable),'fsync_directory':any(c.get('kind')=='directory' for c in durable),'atomic_replace':any(c['call']=='replace' for c in durable),'original_receipt_preimage_verified':roundtrip==original==b['restored_receipt'] and original in b['receipts'],'all_original_results_resolved':set(b['consumer'])=={o['op_id'] for o in self.oracle['operations'] if o['disposition']=='PRODUCED'},'frontier':b['frontier'],'consumer':b['consumer'],'shared_cold_execution_path':str(self.cold_folder),'shared_execution_disclosure':'Seven positive cold controls inspect one actual crash/resume experiment, not seven independent crashes.'}
 def cold_attack(self,variant):
  self.ensure_cold();folder=self.out/('attack-'+variant+'-'+uuid.uuid4().hex);folder.mkdir();shutil.copytree(self.cold_folder/'owner',folder/'owner')
  cp=json.loads((self.cold_folder/'checkpoint.json').read_text())
  if variant=='missing_fact':cp['fact_custody_snapshot']={'facts':{},'hashes':{}}
  elif variant=='receipt':cp['prior_receipts'][0]['provenance_refs']=[]
  elif variant=='self_rehash':
   key=next(iter(cp['fact_custody_snapshot']['facts']));cp['fact_custody_snapshot']['facts'][key]['denominator']=999;cp['fact_custody_snapshot']['hashes'][key]=w.digest(cp['fact_custody_snapshot']['facts'][key])
  elif variant=='source_edition':cp['source_editions']['REL-A-W1']='STALE-EDITION'
  elif variant=='revoked_owner':w.FixtureOwner(folder/'owner').revoke('REL-A-W1')
  else:raise RuntimeError('unknown cold attack')
  cp['checkpoint_hash']=w.digest({k:v for k,v in cp.items() if k not in ('signature','checkpoint_hash')});dump(folder/'checkpoint.json',cp)
  cmd=[sys.executable,str(R/'repro/phase_b_cold_worker_v1.py'),'attack',str(folder)]
  child=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  dump(folder/'command.json',{'command':cmd,'exit':child.returncode,'stdout':child.stdout,'stderr':child.stderr})
  if child.returncode:raise RuntimeError(child.stderr)
  result=json.loads((folder/'attack.json').read_text());result['child_command']=cmd;result['attack_variant']=variant;result['raw_execution_path']=str(folder);return result
