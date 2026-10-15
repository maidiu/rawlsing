"""M01 finite TEST_ONLY construction. No operative owner grant is asserted.

Intervention controls exist only in prepare(). Later response accepts no labels,
refs, desired outcomes or callbacks: it reads applied owner state and history.
"""
import bootstrap
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
import hashlib,json
from candidate import can008_candidate_rule as old,owner_transitions as owner
from candidate.positive_chain import ChainEventLedger,seal_event
from candidate.candidate_registry_fixture import CandidateRegistryFixture,digest,canon,parse_time
from candidate.adopted_contract import GeneratedMemoryState

RULE_ID='M01_PARALLEL_OWNER_READ';VERSION='1.0.0-TEST_ONLY'
MEMORY={'NONE':None,'CERTAIN':'AVAILABLE_SOURCE_BOUND','UNCERTAIN':'AVAILABLE_UNCERTAIN','UNAVAILABLE':'UNAVAILABLE'}
ACCESS={'NONE':None,'BELIEF':'CLAIM_ACCESSIBLE','INACCESSIBLE':'CLAIM_INACCESSIBLE','UNKNOWN':'CLAIM_ACCESS_UNKNOWN'}
class Refusal(Exception):
 def __init__(self,code):self.code=code;super().__init__(code)
def need(ok,code):
 if not ok:raise Refusal(code)
def definition():
 return dict(id=RULE_ID,version=VERSION,authority='TEST_ONLY_M01_LOCAL_GRANT',law=old.PINS,
  eligible_issuers=['ISSUER_AUTH_WORLD_SCHED@1','ISSUER_AUTH_INSTITUTION@1'],roles=['PRECIPITATING_EVENT_STREAM'],
  actor='ACTOR_SYNTH_1',world='W_SYNTH_1998',as_of='1998-10-03T16:00:00Z',temporal='1998 through 2000',
  receivability='exact feedback then exact shift request features',owners=['ADP016','ADP017'],
  use_roles=['HIDDEN_CAUSAL_TRACE_SOURCE_FEATURE_READ','PRIVATE_BELIEF_AND_CURRENT_PERMISSION_READ'],
  counterpart='NONE_USED',modality='NONE_USED',uptake='evaluation-local shift request; no durable belief',
  recruitment='retain distinct memory and epistemic paths',multiplicity='two independent streams preserved',
  closure='one finite pass',history_predicate='verified read only, no output dependence',effort='NONE_USED',
  effects=['BUFFER','AMPLIFY','DEFLECT','REROUTE','BLOCK'],target='TEST_ONLY_CAN008_CURRENT',
  validation='all streams before atomic synchronous commit',pff='NOT_EMITTED',valid_empty='not used in this finite cell',
  failure='typed refusal; unknown access HOLD',quantity='NONE_USED',rng='NONE_USED',atomicity='rollback owner+registry+journals',
  provenance='complete source/event/owner transition/read hashes, deterministic replay',
  formation_variants=MEMORY,epistemic_variants=ACCESS,
  production='MECHANISM_IDENTIFICATION_HOLD_NO_OPERATIVE_OWNER_AUTHORITY',serial='MECHANISM_IDENTIFICATION_HOLD_NO_CONTENT_SENSITIVE_MEMORY_TO_BELIEF_RULE')
def source_hash():
 return digest(dict(definition=definition(),implementation={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(owner.__file__),Path(old.__file__),Path(bootstrap.__file__)]}))
def events():
 common=dict(issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',actor_scope='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',admission_state='ADMITTED')
 e1=seal_event(**common,event_id='M01_FEEDBACK',issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',effective_causal_time='1998-10-03T16:00:00Z',public_features=('shift_feedback_window_open','supervisor_solicits_comment'))
 e2=seal_event(**common,event_id='M01_LATER_SHIFT_REQUEST',issuer_authority_id='ISSUER_AUTH_INSTITUTION',effective_causal_time='1998-11-20T09:00:00Z',public_features=('shift_change_request_window',),causal_parent_event_ids=(e1.event_id,))
 return e1,e2

class Cell:
 def __init__(self):
  self.reg=CandidateRegistryFixture();need(old.register_default_rule(self.reg)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE','OLD_RULE_UNBOUND')
  self.ctx=owner.FixtureOwnerState(self.reg);self.history=ChainEventLedger();self.journal=ChainEventLedger();self.reads=[]
  self.binding=old.build_default_binding();self.e1,self.e2=events();self.grant=source_hash();self.initial=self.ctx.state_hash
  self.claim_id=None;self.first_receipt=None;self.formation=None;self.epistemic=None
 def checkpoint(self):
  return deepcopy(dict(reg=self.reg.checkpoint(),ctx=self.ctx.checkpoint(),history=self.history.checkpoint(),journal=self.journal.checkpoint(),reads=self.reads,claim_id=self.claim_id,first_receipt=self.first_receipt,formation=self.formation,epistemic=self.epistemic))
 def restore(self,s):
  self.reg.restore(s['reg']);self.ctx.restore(s['ctx']);self.history.restore(s['history']);self.journal.restore(s['journal'])
  for k in ('reads','claim_id','first_receipt','formation','epistemic'):setattr(self,k,deepcopy(s[k]))
 def verify_grant(self,rule_version=VERSION,authority='TEST_ONLY_M01_LOCAL_GRANT'):
  need(rule_version==VERSION and authority==definition()['authority'] and self.grant==source_hash(),'UNAUTHORIZED_RULE_OR_SOURCE')
 def fault(self,where,failure):
  need(where!=failure,'TEST_FAULT_'+where)
 def form(self,content='AVAILABLE_SOURCE_BOUND',**overrides):
  args=dict(actor_id=self.ctx.actor_id,basis_event=self.e1,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state=content,owning_rule_id=self.binding.rule_id,owning_rule_version=self.binding.rule_version,owning_rule_hash=self.binding.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=self.ctx.state_hash,context=self.ctx)
  args.update(overrides);return owner.adp016_form_causal_trace(**args)
 def epi_args(self,access='CLAIM_ACCESSIBLE'):
  return dict(actor_id=self.ctx.actor_id,claim_ref=self.claim_id,stance_kind='BELIEF',stance_operation='ADD',causal_parent_refs=[self.e1.event_id],actor_facing_basis_refs=[self.e1.event_id+':'+self.e1.event_hash],memory_basis_refs=[],owning_rule_id=self.binding.rule_id,owning_rule_version=self.binding.rule_version,owning_rule_hash=self.binding.rule_content_hash,effective_causal_time=self.e1.effective_causal_time,context=self.ctx,pre_state_hash=self.ctx.state_hash,claim_accessibility=access)
 def prepare(self,memory='CERTAIN',epistemic='BELIEF',history='STORED',failure=None):
  need(memory in MEMORY and epistemic in ACCESS and history in ('STORED','OMITTED','WITHHELD'),'INVALID_INTERVENTION')
  self.verify_grant();s=self.checkpoint()
  try:
   p=old.OwnerPrestate(actor_id=self.e1.actor_scope,world_ref=self.e1.world_ref,world_as_of=self.e1.world_as_of)
   coupling=old.coupline_evaluate(self.e1,p,self.binding,self.reg);need(coupling.get('decision_state')=='COUPLING_EVALUATED',coupling.get('code','FIRST_EVENT_REFUSED'))
   self.fault('admission',failure)
   response=old.response_rule_apply(coupling,p,self.binding,'BUFFER');self.first_receipt=old.build_response_receipt(self.e1,p,self.binding,coupling,response)
   if history!='OMITTED':self.history.commit('CAN008_CURRENT_RESPONSE_EFFECT',dict(effect_kind='BUFFER',receipt=self.first_receipt),self.e1.effective_causal_time,[self.e1.event_id])
   self.fault('history',failure)
   if MEMORY[memory] is not None:
    self.formation=self.form(MEMORY[memory]);before=self.ctx.state_hash;commit=self.ctx.commit_memory(self.formation)
    self.journal.commit('ADP016_COMMIT',dict(before=before,after=self.ctx.state_hash,proposal=self.formation,commit=commit),self.e1.effective_causal_time,[self.e1.event_id])
   self.fault('memory',failure)
   claim=owner.canonical_claim(self.ctx.actor_id,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',self.e1.effective_causal_time,self.ctx.actor_id,[self.e1.event_id]);self.claim_id=self.ctx.bind_claim(claim,self.e1)
   self.fault('claim',failure)
   if ACCESS[epistemic] is not None:
    before=self.ctx.state_hash;self.epistemic=owner.adp017_apply_epistemic_effect(**self.epi_args(ACCESS[epistemic]));need(self.epistemic['decision_state']=='APPLIED_EPISTEMIC_TRANSITION',self.epistemic['decision_state'])
    self.journal.commit('ADP017_COMMIT',dict(before=before,after=self.ctx.state_hash,result=self.epistemic),self.e1.effective_causal_time,[self.e1.event_id])
   self.fault('epistemic',failure)
   self.journal.commit('FIRST_EVENT_COMPLETE',dict(state=self.ctx.data(),state_hash=self.ctx.state_hash,source_rule=self.grant),self.e1.effective_causal_time,[self.e1.event_id]);self.fault('publish',failure)
   return dict(status='FIRST_EVENT_COMMITTED',state_hash=self.ctx.state_hash,event=asdict(self.e1),history_mode=history)
  except Exception:
   self.restore(s);raise
 def read_owner(self,expected_state,at):
  need(self.ctx.verify() and self.ctx.state_hash==expected_state,'STALE_OR_CORRUPT_OWNER_STATE')
  need(self.ctx.actor_id==definition()['actor'],'WRONG_ACTOR')
  need(self.reg.verify_event(self.e1),'SOURCE_EVENT_UNBOUND')
  need(parse_time(at)>parse_time(self.e1.effective_causal_time),'STALE_CAUSAL_TIME')
  # Read through owner checkpoint, not caller references or receipt reconstruction.
  state=self.ctx.checkpoint()['state'];memories=list(state['memories'].values())
  need(len(memories)<=1,'UNSUPPORTED_MULTIPLICITY')
  ym='AMPLIFY';memory_permission=None
  for m in memories:
   need(m['actor_id']==self.ctx.actor_id and m['current_state_hash']==owner.memory_semantic_hash(m),'MEMORY_INTEGRITY')
   need(m['representation_kind']=='CAUSAL_TRACE_MEMORY' and m['retention_state']=='RETAINED' and m['memory_accessibility_state']=='NOT_APPLICABLE_CAUSAL_TRACE','UNAUTHORIZED_MEMORY_CLASS')
   t=state['memory_transitions'].get(m['last_transition_id']);need(t and t['post_state_hash']==m['current_state_hash'] and t['authority_or_rule_hash']==self.binding.rule_content_hash,'MEMORY_TRANSITION_UNBOUND')
   need(m['objective_source_event_refs']==(self.e1.event_id+':'+self.e1.event_hash,),'MEMORY_SOURCE_UNBOUND')
   features=[json.loads(x) for x in m['source_feature_bindings']]
   need([x['feature'] for x in features]==list(self.e1.public_features) and all(x['source_event']==self.e1.event_id+':'+self.e1.event_hash for x in features),'FEATURE_SOURCE_UNBOUND')
   states={x['state'] for x in features};need(len(states)==1,'AMBIGUOUS_SOURCE_FEATURES');value=next(iter(states))
   ym={'AVAILABLE_SOURCE_BOUND':'BUFFER','AVAILABLE_UNCERTAIN':'DEFLECT','UNAVAILABLE':'AMPLIFY'}.get(value)
   need(ym is not None,'UNKNOWN_SOURCE_FEATURE_STATE')
   need(m['uncertainty_state']==('UNCERTAIN' if value=='AVAILABLE_UNCERTAIN' else 'CERTAIN'),'UNCERTAINTY_INTEGRITY')
   memory_permission=owner.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',m['representation_kind'],m['memory_accessibility_state'],context=self.ctx,claim_ref=self.claim_id,state_hash=expected_state)
   need(memory_permission['first_person_permission']=='DENY_FIRST_PERSON_CLAIM','K3_TRACE_EXPORT')
  ye='AMPLIFY';permission=None
  snapshot=state['state_sets'].get(self.claim_id)
  if snapshot:
   need(snapshot['current_state_hash']==digest({k:v for k,v in snapshot.items() if k!='current_state_hash'}),'EPISTEMIC_SNAPSHOT_INTEGRITY')
   active=snapshot['active_stance_records'];need(active==[v for k,v in sorted(state['stances'].items()) if v['claim_ref']==self.claim_id],'STANCE_SET_INTEGRITY')
   if active:
    need(len(active)==1 and active[0]['stance_kind']=='BELIEF' and active[0]['memory_basis_refs']==(),'UNAUTHORIZED_EPISTEMIC_MECHANISM')
    need(owner.verify_claim(state['claims'][self.claim_id]),'CLAIM_INTEGRITY')
    access=snapshot['current_claim_accessibility']
    permission=owner.adp017_first_person_check('BELIEF',access,context=self.ctx,claim_ref=self.claim_id,state_hash=snapshot['current_state_hash'])
    need(access!='CLAIM_ACCESS_UNKNOWN','MECHANISM_IDENTIFICATION_HOLD_ACCESS_UNKNOWN')
    if access=='CLAIM_INACCESSIBLE':need(permission['first_person_permission']=='DENY_FIRST_PERSON_CLAIM','EPISTEMIC_PERMISSION');ye='BLOCK'
    else:need(permission['first_person_permission']=='PERMIT_FIRST_PERSON_BELIEF','EPISTEMIC_PERMISSION');ye='REROUTE'
  read=dict(actor=self.ctx.actor_id,at=at,state_hash=expected_state,actual_state=state,memory_first_person=memory_permission,private_permission=permission,streams=dict(memory=ym,epistemic=ye))
  self.reads.append(deepcopy(read));return read
 def later(self,expected_state,*,history_access=True,event=None,rule_version=VERSION,authority='TEST_ONLY_M01_LOCAL_GRANT',failure=None):
  self.verify_grant(rule_version,authority);s=self.checkpoint();e=event if event is not None else self.e2
  try:
   need(e.actor_scope==self.ctx.actor_id,'WRONG_ACTOR')
   need((e.world_ref,e.world_as_of)==(self.e1.world_ref,self.e1.world_as_of),'STALE_WORLD')
   need(tuple(e.public_features)==('shift_change_request_window',),'UNRECEIVABLE_EVENT')
   gate=self.reg.admit_event(e);need(gate.get('status')=='EVENT_IDENTITY_ADMITTED_IN_FIXTURE',gate.get('code','EVENT_REFUSED'))
   self.fault('later_admission',failure)
   actual=self.history.read_effects('CAN008_CURRENT_RESPONSE_EFFECT')
   for row in actual:
    rc=row['payload']['receipt'];need(rc==self.first_receipt and row['payload']['effect_kind']==rc['effect_kind']=='BUFFER','HISTORY_BINDING')
   delivered=actual if history_access else []
   read=self.read_owner(expected_state,e.effective_causal_time);self.fault('later_read',failure)
   payload=dict(rule_id=RULE_ID,version=VERSION,source_hash=self.grant,event=asdict(e),read=read,history_stored=actual,history_delivered=delivered,streams=read['streams'],durability='NON_DURABLE_CURRENT_CONSEQUENCE',public_standing='HOLD_NO_PUBLIC_RATIFICATION_OWNER',production_owner='MECHANISM_IDENTIFICATION_HOLD_NO_OPERATIVE_OWNER_AUTHORITY',validated=True)
   out=self.journal.commit('M01_CAN008_CURRENT_RESPONSE_GRAPH',payload,e.effective_causal_time,[e.event_id,self.e1.event_id]);need(out['status']=='COMMITTED_IN_CAUSAL_ORDER','COMMIT_REFUSED')
   self.fault('later_emission',failure)
   return dict(status='COMMITTED_TEST_ONLY',streams=read['streams'],read=read,history_stored=actual,history_delivered=delivered,receipt=out['entry'],state_hash=self.ctx.state_hash)
  except Exception:
   self.restore(s);raise
 def export(self):
  need(self.ctx.verify(),'STATE_INTEGRITY');self.journal.verify();self.history.verify()
  return deepcopy(dict(owner_state=self.ctx.data(),owner_hash=self.ctx.state_hash,events=self.reg._events,history=self.history.entries,journal=self.journal.entries,reads=self.reads,rule=definition(),rule_hash=self.grant,initial_owner_hash=self.initial))
