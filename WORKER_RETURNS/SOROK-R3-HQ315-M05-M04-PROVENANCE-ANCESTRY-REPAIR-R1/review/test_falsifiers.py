"""M04 independent falsifiers. Freeze this file before its first execution."""
from pathlib import Path
import sys,json,hashlib
from copy import deepcopy
from dataclasses import replace
import pytest
R=Path(__file__).resolve().parents[1]
M=R/'runtime/m02/runtime/m01'
sys.path.insert(0,str(M/'repro'))
import bootstrap,cell,claim_provenance
from cell import Cell,Refusal,owner,digest
from candidate.candidate_registry_fixture import canon
from candidate.positive_chain import seal_event
OUT=R/'evidence/fresh/observations'

def save(name,**data):
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/(name+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')
def ready(m='CERTAIN',e='BELIEF'):
 c=Cell();c.prepare(m,e);return c

def apply(c,access='CLAIM_ACCESSIBLE',op='ADD',target=None):
 a=c.epi_args(access);a.update(stance_operation=op,target_record_ref=target)
 out=owner.adp017_apply_epistemic_effect(**a)
 assert out['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
 return out

def response(c,direct=False,at='1998-11-20T09:00:00Z'):
 return c.read_owner(c.ctx.state_hash,at) if direct else c.later(c.ctx.state_hash)

def refuse_read(c,name,direct=False):
 before=c.checkpoint();observed=None;code=None
 try:observed=response(c,direct)
 except Refusal as e:code=str(e)
 save(name,before=before,after=c.checkpoint(),observed=observed,refusal=code)
 assert code is not None,'unearned response accepted: '+str(observed and observed['streams'])
 assert c.checkpoint()==before,'refusal failed atomic rollback'

def restore_then_refuse(c,packet,name,direct=False):
 before=c.checkpoint()
 try:c.restore(packet)
 except Refusal as e:
  save(name,restore_refusal=str(e),before=before,after=c.checkpoint(),packet=packet)
  assert c.checkpoint()==before
  return
 refuse_read(c,name,direct)

@pytest.mark.parametrize('value',[None,'','unknown-claim',17,[],{'claim':'forged'}])
def test_outer_selector_cannot_remove_existing_belief(value):
 c=ready();c.claim_id=value
 refuse_read(c,'selector_'+hashlib.sha256(str(value).encode()).hexdigest()[:8])

@pytest.mark.parametrize('field',['subject_scope','subject_ref','object_or_value','referent_refs'])
def test_foreign_canonical_claim_is_not_none(field):
 c=ready();base=deepcopy(c.ctx.claims[c.claim_id]);args={k:base[k] for k in ('subject_ref','predicate_ref','object_or_value','temporal_scope','subject_scope','referent_refs','polarity')}
 args[field]=['OTHER_EVENT'] if field=='referent_refs' else 'FOREIGN'
 foreign=owner.canonical_claim(**args);p=c.checkpoint();p['ctx']['state']['claims'][foreign['claim_id']]=foreign;p['claim_id']=foreign['claim_id']
 restore_then_refuse(c,p,'foreign_'+field)

@pytest.mark.parametrize('m',['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'])
def test_cross_cell_none_owner_cannot_erase_first_committed_belief(m):
 c=ready(m);donor=ready(m,'NONE');p=c.checkpoint();p['ctx']=donor.checkpoint()['ctx']
 # The real first-event journal/binding still attests BELIEF. No withdrawal occurred.
 restore_then_refuse(c,p,'erase_owner_'+m)

@pytest.mark.parametrize('op',['SUPERSEDE_EXACT_RECORD','WITHDRAW'])
@pytest.mark.parametrize('direct',[False,True])
def test_revoked_or_withdrawn_state_cannot_be_resurrected_by_partial_rollback(op,direct):
 c=ready();old=c.ctx.checkpoint()['state'];apply(c,'CLAIM_INACCESSIBLE',op,next(iter(c.ctx.stances)))
 p=c.checkpoint();s=p['ctx']['state']
 for k in ('stances','state_sets','permissions'):s[k]=deepcopy(old[k])
 # Keep both actual native transitions: the last real revision must not disappear.
 assert len(s['epistemic_transitions'])==2
 restore_then_refuse(c,p,'resurrect_'+op+'_'+str(direct),direct)

@pytest.mark.parametrize('direct',[False,True])
def test_fully_rehashed_transition_requires_actual_prestate_ancestry(direct):
 c=ready();p=c.checkpoint();s=p['ctx']['state'];t=s['epistemic_transitions'][0];e=t['effect'];oldkey=e['effect_id']
 t['pre_state_hash']=digest(['M04_UNRELATED_OWNER_STATE'])
 e['effect_id']=digest(['EPISTEMIC_EFFECT',{k:v for k,v in e.items() if k!='effect_id'},t['pre_state_hash'],t['target_record_ref']])
 s['stances']={e['effect_id']:deepcopy(e)};t['post_stance_set_hash']=digest(s['stances'])
 t['transition_id']=digest({k:v for k,v in t.items() if k not in ('transition_id','post_state_set_hash')})
 snap=s['state_sets'][c.claim_id];snap['active_stance_records']=[deepcopy(e)];snap['last_transition_ref']=t['transition_id'];snap['current_state_hash']=digest({k:v for k,v in snap.items() if k!='current_state_hash'})
 s['permissions'][c.claim_id]['epistemic_state_hash']=snap['current_state_hash'];t['post_state_set_hash']=snap['current_state_hash']
 restore_then_refuse(c,p,'forged_ancestry_'+str(direct),direct)

@pytest.mark.parametrize('at',['not-a-time','1998-11-20T09:00:00','1998-10-03T15:59:59Z','1998-10-03T16:00:00Z','2001-01-01T00:00:00Z',None,{},'1998-02-30T12:00:00Z'])
def test_invalid_or_out_of_scope_response_cut_refuses_without_read(at):
 c=ready();before=c.checkpoint()
 with pytest.raises(Refusal):c.read_owner(c.ctx.state_hash,at)
 assert c.checkpoint()==before

@pytest.mark.parametrize('at',['1998-11-20T04:00:00-05:00','1998-11-20T10:00:00+01:00','1998-10-03T12:00:00.000001-04:00'])
def test_equivalent_aware_time_cuts_preserve_valid_belief(at):
 c=ready();out=c.read_owner(c.ctx.state_hash,at)
 assert out['streams']=={'memory':'BUFFER','epistemic':'REROUTE'}
 save('aware_'+hashlib.sha256(at.encode()).hexdigest()[:8],result=out)

@pytest.mark.parametrize('at',['1999-06-01T10:00:00Z','2000-12-31T23:59:59Z'])
def test_genuinely_later_admitted_response_cut_is_allowed(at):
 c=ready();e=replace(c.e2,event_id='M04_MOVED_RESPONSE',effective_causal_time=at,event_hash='')
 d={k:v for k,v in e.__dict__.items() if k!='event_hash'};e=seal_event(**d)
 out=c.later(c.ctx.state_hash,event=e)
 assert out['streams']=={'memory':'BUFFER','epistemic':'REROUTE'} and out['read']['at']==at and c.reg.verify_event(e)
 save('moved_'+at[:10],result=out)

def test_irrelevant_future_native_claim_preserves_bound_none():
 c=ready(e='NONE');e=replace(c.e1,event_id='M04_FUTURE',effective_causal_time='1999-06-01T10:00:00Z',event_hash='',causal_parent_event_ids=(c.e1.event_id,))
 e=seal_event(**{k:v for k,v in e.__dict__.items() if k!='event_hash'});assert c.reg.admit_event(e)['status']=='EVENT_IDENTITY_ADMITTED_IN_FIXTURE'
 claim=owner.canonical_claim(c.ctx.actor_id,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e.effective_causal_time,c.ctx.actor_id,[e.event_id]);ref=c.ctx.bind_claim(claim,e)
 a=c.epi_args();a.update(claim_ref=ref,causal_parent_refs=[e.event_id],actor_facing_basis_refs=[e.event_id+':'+e.event_hash],effective_causal_time=e.effective_causal_time)
 assert owner.adp017_apply_epistemic_effect(**a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
 out=c.later(c.ctx.state_hash);assert out['streams']['epistemic']=='AMPLIFY'
 save('unselected_future',result=out,future_claim=claim)

@pytest.mark.parametrize('field',['actor_scope','world_ref','world_as_of','effective_causal_time'])
def test_rehashed_first_receipt_source_substitution_refuses(field):
 c=ready();p=c.checkpoint();rc=p['first_receipt'];rc['precipitating_event'][field]='M04_SUBSTITUTED'
 rc['receipt_hash']=cell.old._sha(cell.old._canon({k:v for k,v in rc.items() if k!='receipt_hash'}))
 # Also update untrusted outer selection binding, retaining actual committed journal.
 b=json.loads(p['claim_selection_binding']);b['basis']['first_response_receipt_hash']=rc['receipt_hash'];p['claim_selection_binding']=canon(b)
 restore_then_refuse(c,p,'receipt_source_'+field)

@pytest.mark.parametrize('stage',['later_admission','later_read','later_emission'])
def test_failure_retry_restores_all_state_then_commits_once(stage):
 c=ready();before=c.checkpoint()
 with pytest.raises(Refusal):c.later(c.ctx.state_hash,failure=stage)
 assert c.checkpoint()==before
 out=c.later(c.ctx.state_hash);entries=c.journal.read_effects('M01_CAN008_CURRENT_RESPONSE_GRAPH')
 assert len(entries)==1 and len(c.reads)==1 and out['status']=='COMMITTED_TEST_ONLY'
 save('retry_'+stage,result=out)

@pytest.mark.parametrize('e',['NONE','BELIEF','INACCESSIBLE','UNKNOWN'])
def test_real_native_state_retains_none_permit_deny_defer_distinction(e):
 c=ready('UNCERTAIN',e)
 if e=='UNKNOWN':
  refuse_read(c,'native_unknown');return
 out=c.later(c.ctx.state_hash);assert out['streams']=={'memory':'DEFLECT','epistemic':{'NONE':'AMPLIFY','BELIEF':'REROUTE','INACCESSIBLE':'BLOCK'}[e]}
 save('native_'+e,result=out)

def test_coherent_full_checkpoint_clone_is_lawful_replay():
 a=ready('UNCERTAIN');b=Cell();b.restore(a.checkpoint())
 assert a.later(a.ctx.state_hash)==b.later(b.ctx.state_hash)

@pytest.mark.parametrize('field',['rule_version','authority'])
def test_source_rule_version_or_authority_substitution_refuses(field):
 c=ready();before=c.checkpoint()
 with pytest.raises(Refusal):c.later(c.ctx.state_hash,**{field:'M04_FORGED'})
 assert c.checkpoint()==before

def test_duplicate_source_event_conflict_does_not_mutate_registry():
 c=ready();before=c.checkpoint();e=replace(c.e1,public_features=('different',),event_hash='')
 e=seal_event(**{k:v for k,v in e.__dict__.items() if k!='event_hash'})
 assert c.reg.admit_event(e)['status']!='EVENT_IDENTITY_ADMITTED_IN_FIXTURE'
 assert c.checkpoint()==before

def test_duplicate_effect_transition_is_not_validated_as_single_effect():
 c=ready();p=c.checkpoint();p['ctx']['state']['epistemic_transitions']*=2
 restore_then_refuse(c,p,'duplicate_transition')

def test_native_no_change_preserves_current_stance_and_owner_hash():
 c=ready();before=c.checkpoint();a=c.epi_args();a['stance_operation']='NO_CHANGE'
 assert owner.adp017_apply_epistemic_effect(**a)['decision_state']=='NO_EPISTEMIC_TRANSITION'
 assert c.checkpoint()==before and c.later(c.ctx.state_hash)['streams']['epistemic']=='REROUTE'
