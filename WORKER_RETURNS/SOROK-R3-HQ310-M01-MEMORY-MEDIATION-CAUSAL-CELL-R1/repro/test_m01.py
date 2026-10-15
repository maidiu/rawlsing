"""Author causal/hostile tests, prospective predictions frozen in 01_PREREGISTRATION."""
import json,itertools,subprocess,sys,shutil,os
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import pytest
from cell import Cell,Refusal,owner,old,digest,source_hash,VERSION,events
from candidate.candidate_registry_fixture import event_digest
from candidate.positive_chain import run_positive_chain,LedgerIntegrityError
from candidate.adopted_contract import GeneratedMemoryState
from bootstrap import R
OUT=R/'evidence/new/observations'
def save(name,value):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
def trial(m='CERTAIN',e='BELIEF',h='STORED'):
 c=Cell();c.prepare(m,e,h);pre=c.export();out=c.later(c.ctx.state_hash,history_access=h!='WITHHELD');return c,pre,out

@pytest.mark.parametrize('m,e,h',list(itertools.product(['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'],['NONE','BELIEF','INACCESSIBLE'],['STORED','OMITTED','WITHHELD'])))
def test_full_factorial(m,e,h):
 c,pre,out=trial(m,e,h)
 assert out['streams']==dict(memory={'NONE':'AMPLIFY','CERTAIN':'BUFFER','UNCERTAIN':'DEFLECT','UNAVAILABLE':'AMPLIFY'}[m],epistemic={'NONE':'AMPLIFY','BELIEF':'REROUTE','INACCESSIBLE':'BLOCK'}[e])
 assert pre['owner_state']==out['read']['actual_state']==c.ctx.data();assert c.reads==[out['read']]
 assert bool(out['history_stored'])==(h!='OMITTED');assert bool(out['history_delivered'])==(h=='STORED')
 assert c.reg.verify_event(c.e1) and c.reg.verify_event(c.e2)
 assert all(x['memory_basis_refs']==() for x in c.ctx.stances.values())
 assert out['receipt']['payload']['public_standing']=='HOLD_NO_PUBLIC_RATIFICATION_OWNER'
 save('factorial_'+m+'_'+e+'_'+h,dict(pre=pre,result=out,post=c.export()))

@pytest.mark.parametrize('e',['NONE','BELIEF','INACCESSIBLE'])
def test_fixed_history_content_intervention_same_memory_identity(e):
 a,ap,ao=trial('CERTAIN',e);b,bp,bo=trial('UNCERTAIN',e)
 assert ap['history']==bp['history'] and a.e1==b.e1 and a.e2==b.e2
 assert set(a.ctx.memories)==set(b.ctx.memories) # ref placebo: SAME ID, different actual content
 assert ao['streams']['memory']!=bo['streams']['memory'];assert ao['streams']['epistemic']==bo['streams']['epistemic']
 # Epistemic semantics stay fixed, though whole-owner provenance hashes differ.
 for c in (a,b):assert all(not x['memory_basis_refs'] for x in c.ctx.stances.values())
 save('same_ref_content_'+e,dict(left=ao,right=bo))

@pytest.mark.parametrize('m',['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'])
def test_fixed_owner_state_history_variation(m):
 cases=[trial(m,'BELIEF',h) for h in ['STORED','OMITTED','WITHHELD']]
 assert len({p['owner_hash'] for c,p,o in cases})==1
 assert cases[0][1]['owner_state']==cases[1][1]['owner_state']==cases[2][1]['owner_state']
 assert cases[0][2]['streams']==cases[1][2]['streams']==cases[2][2]['streams']
 assert cases[0][1]['history']!=cases[1][1]['history'];assert cases[2][2]['history_stored'] and not cases[2][2]['history_delivered']

def test_fixed_memory_history_independent_epistemic_update_and_placebo():
 a,ap,ao=trial('CERTAIN','NONE');b,bp,bo=trial('CERTAIN','BELIEF');c,cp,co=trial('CERTAIN','INACCESSIBLE')
 assert ap['history']==bp['history']==cp['history']
 assert ap['owner_state']['memories']==bp['owner_state']['memories']==cp['owner_state']['memories']
 assert ap['owner_state']['claims']==bp['owner_state']['claims']==cp['owner_state']['claims']
 assert ap['owner_state']['emissions']==bp['owner_state']['emissions']==cp['owner_state']['emissions']
 assert [x['streams']['epistemic'] for x in (ao,bo,co)]==['AMPLIFY','REROUTE','BLOCK']
 assert not a.ctx.stances and a.claim_id in a.ctx.claims # mere reference/claim never suffices
 save('isolated_epistemic',dict(absent=ao,accessible=bo,inaccessible=co))

@pytest.mark.parametrize('m',['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'])
def test_unknown_access_holds_and_rolls_back(m):
 c=Cell();c.prepare(m,'UNKNOWN');s=c.checkpoint()
 with pytest.raises(Refusal,match='MECHANISM_IDENTIFICATION_HOLD_ACCESS_UNKNOWN'):c.later(c.ctx.state_hash)
 assert c.checkpoint()==s and c.reg.event(c.e2.event_id) is None
 save('unknown_'+m,dict(state=c.export(),code='MECHANISM_IDENTIFICATION_HOLD_ACCESS_UNKNOWN'))

def test_original_history_mechanism_positive_comparator():
 a=run_positive_chain(_comparison=False);b=run_positive_chain(_comparison=False,omit_first_effect=True,later_event_requires_prior_effect=False)
 assert a['later_event_response']['effect_kind']=='DEFLECT';assert b['later_event_response']['effect_kind']=='AMPLIFY';assert a['state']==b['state']
 save('CAN3_history_comparator',dict(stored=a,omitted=b))

@pytest.mark.parametrize('point',['admission','history','memory','claim','epistemic','publish'])
def test_first_atomicity(point):
 c=Cell();s=c.checkpoint()
 with pytest.raises(Refusal,match='TEST_FAULT'):c.prepare(failure=point)
 assert c.checkpoint()==s and not c.ctx.memories and not c.ctx.stances
 save('rollback_first_'+point,c.export())

@pytest.mark.parametrize('point',['later_admission','later_read','later_emission'])
def test_later_atomicity_failed_emission(point):
 c=Cell();c.prepare();s=c.checkpoint()
 with pytest.raises(Refusal,match='TEST_FAULT'):c.later(c.ctx.state_hash,failure=point)
 assert c.checkpoint()==s and c.reg.event(c.e2.event_id) is None
 assert c.later(c.ctx.state_hash)['status']=='COMMITTED_TEST_ONLY' # positive retry
 save('rollback_later_'+point,c.export())

@pytest.mark.parametrize('field,value,reseal',[('event_hash','tampered',False),('actor_scope','OTHER',True),('world_as_of','1999-01-01T00:00:00Z',True),('issuer_authority_id','M01_FAKE_OWNER',True),('issuer_authority_version','99',True),('admission_state','REJECTED',True),('event_kind','DRAFT_RESPONSE',True),('derived_from_future_partition',True,True),('effective_causal_time','1998-10-02T00:00:00Z',True),('public_features',('invented',),True)])
def test_actual_later_event_hostility(field,value,reseal):
 c=Cell();c.prepare();s=c.checkpoint();bad=replace(c.e2,**{field:value})
 if reseal:bad=replace(bad,event_hash=event_digest(bad))
 with pytest.raises(Refusal):c.later(c.ctx.state_hash,event=bad)
 assert c.checkpoint()==s
 assert c.later(c.ctx.state_hash)['status']=='COMMITTED_TEST_ONLY'

@pytest.mark.parametrize('override',[{'authority_id':'FORGED'},{'owning_rule_version':'9'},{'owning_rule_hash':'forged'},{'actor_id':'OTHER'},{'parent_state_hash':'stale'},{'stochastic':True},{'content_state':'V2_TRANSCRIPT'},{'basis_event':None}])
def test_memory_owner_gate(override):
 c=Cell();c.prepare('NONE','NONE');s=c.checkpoint()
 with pytest.raises(owner.OwnerTransitionError):c.form(**override)
 assert c.checkpoint()==s

def test_memory_idempotence_and_epistemic_replay_ceiling():
 c=Cell();c.prepare();s=c.ctx.checkpoint();replay=c.ctx.commit_memory(c.formation)
 assert replay['status']=='IDEMPOTENT_REPLAY' and c.ctx.checkpoint()==s
 # Reconstruct exact original epistemic call's prestate; stale replay rejects.
 args=c.epi_args();args['pre_state_hash']=c.epistemic['transition']['pre_state_hash']
 rejected=owner.adp017_apply_epistemic_effect(**args);assert rejected['decision_state']=='BLOCKED_INTEGRITY_FAILURE';assert c.ctx.checkpoint()==s
 save('owner_replay',dict(memory=replay,epistemic=rejected,state=c.ctx.data(),hold='No general ADP017 idempotent replay receipt'))

def test_later_duplicate_event_and_deterministic_replay():
 a,ap,ao=trial();s=a.checkpoint()
 with pytest.raises(Refusal,match='BLOCK_DUPLICATE_EVENT_IDENTITY'):a.later(a.ctx.state_hash)
 assert a.checkpoint()==s
 b,bp,bo=trial();assert a.export()==b.export() and ao==bo
 save('deterministic_replay',dict(left=a.export(),right=b.export(),digest=digest(a.export())))

@pytest.mark.parametrize('target',['memory','permission','history','stance'])
def test_actual_stored_corruption_never_absence(target):
 c=Cell();c.prepare()
 if target=='memory':next(iter(c.ctx.memories.values()))['source_feature_bindings']=('forged',)
 if target=='permission':c.ctx.permissions[c.claim_id]['permission']='PERMIT_FIRST_PERSON_KNOWLEDGE'
 if target=='stance':next(iter(c.ctx.stances.values()))['stance_kind']='KNOWLEDGE'
 if target=='history':c.history.entries[0]['payload']['effect_kind']='AMPLIFY'
 # A corrupted owner cannot even furnish a valid checkpoint. Fail before any event admission.
 before=deepcopy(c.reg._events)
 with pytest.raises((Refusal,owner.OwnerTransitionError,LedgerIntegrityError)):c.later(c.ctx.state_hash)
 assert c.reg._events==before

@pytest.mark.parametrize('args',[{'expected_state':'stale'},{'rule_version':'2'},{'authority':'PRODUCTION_OWNER'}])
def test_stale_and_unissued_later(args):
 c=Cell();c.prepare();s=c.checkpoint();kw=dict(expected_state=c.ctx.state_hash);kw.update(args)
 with pytest.raises(Refusal):c.later(**kw)
 assert c.checkpoint()==s

def test_k3_k5_and_boundary_unknown_no_lifecycle_claim():
 c,pre,out=trial();m=GeneratedMemoryState(**next(iter(c.ctx.memories.values())))
 assert out['read']['memory_first_person']['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'
 assert out['read']['private_permission']['first_person_permission']=='PERMIT_FIRST_PERSON_BELIEF'
 assert out['read']['private_permission']['self_explanation_of_hidden_origin']=='BLOCKED'
 for changes in [{'retention_state':'RETENTION_UNKNOWN'},{'memory_accessibility_state':'ACCESS_UNKNOWN'},{'memory_accessibility_state':'INACCESSIBLE'},{'retention_state':'CONTENT_UNAVAILABLE'}]:
  probe=replace(m,**changes);p=owner.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESSIBLE',probe)
  assert p['first_person_permission']==('DEFER_MISSING_AUTHORITY' if 'UNKNOWN' in str(changes) else 'DENY_FIRST_PERSON_CLAIM')
 with pytest.raises(owner.OwnerTransitionError,match='UNAUTHORIZED_RECALL_CUE'):owner.adp016_attempt_transition(m,'RECALL',parent_event=c.e1,pre_state_hash=m.current_state_hash,context=c.ctx)
 assert c.ctx.data()==pre['owner_state']
 save('K3_boundary',dict(probes='Unapplied boundary objects only; access lifecycle MECHANISM_IDENTIFICATION_HOLD',read=out['read']))

@pytest.mark.parametrize('relation',['OBJECTIVE_SUPPORTED','OBJECTIVE_CONTRADICTED','OBJECTIVE_UNRESOLVED'])
def test_k5_objective_labels_never_ratify(relation):
 c=Cell();c.prepare('NONE','NONE');before=c.ctx.state_hash;args=c.epi_args();args['claim_objective_relation']=relation
 out=owner.adp017_apply_epistemic_effect(**args)
 assert out['public_ratification']=='HOLD_NO_PUBLIC_STANDING_OWNER';assert not out['production_owner_commit']
 assert c.ctx.state_sets[c.claim_id]['analyst_relation']=='OBJECTIVE_UNRESOLVED'
 result=c.later(c.ctx.state_hash);assert result['streams']=={'memory':'AMPLIFY','epistemic':'REROUTE'}
 h=c.ctx.state_sets[c.claim_id]['current_state_hash'];p=owner.adp017_first_person_check('KNOWLEDGE','CLAIM_ACCESSIBLE',context=c.ctx,claim_ref=c.claim_id,state_hash=h)
 assert p['first_person_permission']=='DEFER_MISSING_AUTHORITY'
 save('K5_'+relation,dict(before=before,state=c.ctx.data(),result=result,knowledge=p))

def test_unauthorized_epistemic_and_failed_emission():
 c=Cell();c.prepare('NONE','NONE');s=c.ctx.checkpoint()
 for kw in [{'owning_rule_hash':'forged'},{'stance_kind':'KNOWLEDGE'},{'actor_facing_basis_refs':[]},{'memory_basis_refs':['fake']},{'effective_causal_time':c.e2.effective_causal_time}]:
  args=c.epi_args();args.update(kw);out=owner.adp017_apply_epistemic_effect(**args)
  assert out['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and c.ctx.checkpoint()==s
  save('epistemic_denial_'+str(len(kw))+'_'+next(iter(kw)),out)

def test_no_ref_callback_or_hint_api_and_alias():
 c=Cell();c.prepare();s=c.checkpoint()
 with pytest.raises(TypeError):c.later(c.ctx.state_hash,memory_refs=['fake'],requested_effect='BUFFER')
 assert c.checkpoint()==s
 exported=c.export();exported['owner_state']['memories'].clear();assert c.ctx.memories
 out=c.later(c.ctx.state_hash);out['read']['actual_state']['memories'].clear();assert c.ctx.memories and c.reads[0]['actual_state']['memories']

def test_actual_source_body_change_rejected_isolated_process():
 target=R/'runtime/m01_body_probe';target.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(Path(__file__).with_name('cell.py'),target/'cell.py');shutil.copyfile(Path(__file__).with_name('bootstrap.py'),target/'bootstrap.py')
 # bootstrap location is significant: import original bootstrap first, then isolated cell.
 script='''
import bootstrap,sys
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from cell import Cell,Refusal
c=Cell();c.prepare();s=c.checkpoint()
p=Path(sys.argv[1])/'cell.py';p.write_bytes(p.read_bytes()+b'\\n# hostile mutation\\n')
try:c.later(c.ctx.state_hash)
except Refusal as e:assert e.code=='UNAUTHORIZED_RULE_OR_SOURCE'
else:raise AssertionError('mutated source accepted')
assert c.checkpoint()==s
print('actual source mutation refused')
'''
 run=subprocess.run([sys.executable,'-c',script,str(target)],cwd=Path(__file__).parent,capture_output=True,text=True)
 save('source_body_mutation',dict(returncode=run.returncode,stdout=run.stdout,stderr=run.stderr));assert run.returncode==0


def test_legitimate_owner_revision_invalidates_old_state_snapshot():
 c=Cell();c.prepare('CERTAIN','NONE');old_hash=c.ctx.state_hash
 applied=owner.adp017_apply_epistemic_effect(**c.epi_args())
 assert applied['decision_state']=='APPLIED_EPISTEMIC_TRANSITION' and c.ctx.state_hash!=old_hash
 before=c.checkpoint()
 with pytest.raises(Refusal,match='STALE_OR_CORRUPT_OWNER_STATE'):c.later(old_hash)
 assert c.checkpoint()==before
 out=c.later(c.ctx.state_hash);assert out['streams']['epistemic']=='REROUTE'
 save('legitimate_stale_state',dict(old_hash=old_hash,applied=applied,later=out))


def test_serial_owner_probe_refs_do_not_identify_content_sensitive_link():
 results=[]
 for memory in ['CERTAIN','UNCERTAIN']:
  c=Cell();c.prepare(memory,'NONE');args=c.epi_args();args['memory_basis_refs']=list(c.ctx.memories)
  applied=owner.adp017_apply_epistemic_effect(**args)
  assert applied['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
  active=list(c.ctx.stances.values());assert len(active)==1 and active[0]['stance_kind']=='BELIEF'
  h=c.ctx.state_sets[c.claim_id]['current_state_hash']
  permission=owner.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',context=c.ctx,claim_ref=c.claim_id,state_hash=h)
  results.append(dict(memory=memory,transition=applied,state=c.ctx.data(),permission=permission))
 assert results[0]['permission']==results[1]['permission']
 save('serial_attempt',dict(results=results,verdict='MECHANISM_IDENTIFICATION_HOLD',reason='The pinned owner accepts reference provenance but emits identical direct-event BELIEF; no content-sensitive memory-to-belief intervention grant'))
