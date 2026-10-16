"""M05 author controls; frozen before source implementation or first execution."""
from pathlib import Path
import sys,json
from copy import deepcopy
import pytest
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'repro'))
from author_bootstrap import Cell,Refusal,owner,apply,alternative,canon,digest
O=R/'evidence/m05_author/observations'
def save(name,**kw):
 O.mkdir(parents=True,exist_ok=True);(O/(name+'.json')).write_text(json.dumps(kw,indent=2,default=str)+'\n')
def ready(m='CERTAIN',e='BELIEF'):
 c=Cell();c.prepare(m,e);return c
def deny(c,packet,name,direct=False):
 old=c.checkpoint()
 try:c.restore(packet)
 except Refusal as e:
  assert c.checkpoint()==old;save(name,refusal=str(e),phase='restore',before=old,packet=packet);return
 before=c.checkpoint()
 with pytest.raises(Refusal) as e:
  if direct:c.read_owner(c.ctx.state_hash,c.e2.effective_causal_time)
  else:c.later(c.ctx.state_hash)
 assert c.checkpoint()==before;save(name,refusal=str(e.value),phase='read',packet=packet)

@pytest.mark.parametrize('m',['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'])
@pytest.mark.parametrize('op',['ADD_AFTER_NONE','WITHDRAW_READD','SUPERSEDE_WITHDRAW_READD'])
def test_legitimate_native_sequences_preserve_real_terminal_state(m,op):
 c=ready(m,'NONE' if op=='ADD_AFTER_NONE' else 'BELIEF')
 if op=='ADD_AFTER_NONE':apply(c)
 else:
  if op=='SUPERSEDE_WITHDRAW_READD':apply(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',next(iter(c.ctx.stances)))
  apply(c,operation='WITHDRAW',target=next(iter(c.ctx.stances)));apply(c)
 out=c.later(c.ctx.state_hash);assert out['streams']['epistemic']=='REROUTE'
 proof=out['read']['claim_selection_provenance']['native_owner_ancestry']
 assert proof['current_owner_state_hash']==c.ctx.state_hash and proof['rooted_in_first_journal']
 assert proof['terminal_transition_refs'][c.claim_id]==c.ctx.epistemic_transitions[-1]['transition_id']
 save('native_'+m+'_'+op,result=out)

@pytest.mark.parametrize('access',['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'])
def test_multiple_native_revisions_survive_complete_checkpoint_replay(access):
 c=ready();apply(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',next(iter(c.ctx.stances)))
 apply(c,access,'SUPERSEDE_EXACT_RECORD',next(iter(c.ctx.stances)))
 clone=Cell();clone.restore(c.checkpoint());assert clone.ctx.data()==c.ctx.data()
 if access=='CLAIM_ACCESS_UNKNOWN':
  old=clone.checkpoint()
  with pytest.raises(Refusal):clone.later(clone.ctx.state_hash)
  assert clone.checkpoint()==old
 else:
  a=c.later(c.ctx.state_hash);b=clone.later(clone.ctx.state_hash);assert a==b
  assert a['streams']['epistemic']==('REROUTE' if access=='CLAIM_ACCESSIBLE' else 'BLOCK')

@pytest.mark.parametrize('when',['BEFORE_EPI','AFTER_EPI'])
@pytest.mark.parametrize('tag',[None,'M05_DISTINCT_MEMORY'])
def test_native_memory_after_first_commit_is_not_blanket_forbidden(when,tag):
 c=ready('NONE','NONE');before=c.ctx.state_hash
 if when=='AFTER_EPI':apply(c)
 p=c.form('AVAILABLE_UNCERTAIN',memory_id_override=tag);assert c.ctx.commit_memory(p)['status']=='ADP016_TRACE_COMMITTED_IN_FIXTURE'
 if when=='BEFORE_EPI':apply(c)
 clone=Cell();clone.restore(c.checkpoint());out=clone.later(clone.ctx.state_hash)
 assert out['streams']=={'memory':'DEFLECT','epistemic':'REROUTE'} and clone.ctx.state_hash!=before
 save('late_memory_'+when+'_'+str(tag),result=out)

@pytest.mark.parametrize('at',['1998-09-01T10:00:00Z','1999-01-20T10:00:00Z'])
def test_other_admitted_native_claim_does_not_contaminate_selected_first_claim(at):
 c=ready('CERTAIN','NONE');e,ref,_=alternative(c,at,'M05_EXTRA_'+at[:4]);out=c.later(c.ctx.state_hash)
 assert out['streams']=={'memory':'BUFFER','epistemic':'AMPLIFY'}
 clone=Cell();clone.restore(c.checkpoint());assert clone.ctx.data()==c.ctx.data()
 save('alternative_'+at[:4],result=out)

@pytest.mark.parametrize('mode',['REORDER','DUPLICATE','DELETE_FIRST','DELETE_LAST','OLD_TERMINAL','PERMISSION'])
@pytest.mark.parametrize('direct',[False,True])
def test_retained_native_history_and_terminal_snapshot_cannot_disagree(mode,direct):
 c=ready();apply(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',next(iter(c.ctx.stances)))
 p=c.checkpoint();s=p['ctx']['state'];ts=s['epistemic_transitions']
 if mode=='REORDER':ts.reverse()
 elif mode=='DUPLICATE':ts.append(deepcopy(ts[-1]))
 elif mode=='DELETE_FIRST':del ts[0]
 elif mode=='DELETE_LAST':ts.pop()
 elif mode=='OLD_TERMINAL':s['state_sets'][c.claim_id]['last_transition_ref']=ts[0]['transition_id']
 else:s['permissions'][c.claim_id]['permission']='PERMIT_FIRST_PERSON_BELIEF'
 deny(c,p,'history_'+mode+'_'+str(direct),direct)

@pytest.mark.parametrize('field',['pre_state_hash','post_stance_set_hash','target_record_ref','authority_hash'])
def test_coherent_last_transition_identity_cannot_replace_actual_native_operation(field):
 c=ready();apply(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',next(iter(c.ctx.stances)))
 p=c.checkpoint();s=p['ctx']['state'];t=s['epistemic_transitions'][-1];t[field]='M05_FORGED'
 t['transition_id']=digest({k:v for k,v in t.items() if k not in ('transition_id','post_state_set_hash')})
 snap=s['state_sets'][c.claim_id];snap['last_transition_ref']=t['transition_id'];snap['current_state_hash']=digest({k:v for k,v in snap.items() if k!='current_state_hash'})
 t['post_state_set_hash']=snap['current_state_hash'];s['permissions'][c.claim_id]['epistemic_state_hash']=snap['current_state_hash']
 deny(c,p,'coherent_'+field)

@pytest.mark.parametrize('m',['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'])
def test_original_none_and_real_withdrawal_are_distinct_valid_trajectories(m):
 a=ready(m,'NONE');b=ready(m);apply(b,operation='WITHDRAW',target=next(iter(b.ctx.stances)))
 for c in [a,b]:
  clone=Cell();clone.restore(c.checkpoint());out=clone.later(clone.ctx.state_hash)
  assert out['streams']['epistemic']=='AMPLIFY'
  assert out['read']['claim_selection_provenance']['native_owner_ancestry']['rooted_in_first_journal']

@pytest.mark.parametrize('stage',['later_admission','later_read','later_emission'])
def test_native_revised_state_failure_rolls_back_without_poisoning_retry(stage):
 c=ready();apply(c,operation='WITHDRAW',target=next(iter(c.ctx.stances)));apply(c)
 before=c.checkpoint()
 with pytest.raises(Refusal):c.later(c.ctx.state_hash,failure=stage)
 assert c.checkpoint()==before and c.reg.event(c.e2.event_id) is None
 assert c.later(c.ctx.state_hash)['status']=='COMMITTED_TEST_ONLY'

def test_rehashed_first_journal_cannot_change_real_native_predecessor():
 c=ready();p=c.checkpoint();rows=p['journal'][0];j=next(x for x in rows if x['kind']=='ADP017_COMMIT');j['payload']['before']='UNRELATED'
 previous=None
 for row in rows:
  row['prev_entry_hash']=previous;row['entry_hash']=digest({k:v for k,v in row.items() if k!='entry_hash'});previous=row['entry_hash']
 p['journal']=(rows,digest(rows));binding=json.loads(p['claim_selection_binding']);binding['first_event_entry_hash']=rows[-1]['entry_hash'];p['claim_selection_binding']=canon(binding)
 deny(c,p,'rehashed_original_commit')

@pytest.mark.parametrize('mutation',['DROP','CHANGE_INPUT','OTHER_CELL'])
def test_formation_input_witness_is_not_self_authenticating(mutation):
 c=ready();p=c.checkpoint();w=p['native_formation_inputs'];key=next(iter(w))
 if mutation=='DROP':w.clear()
 elif mutation=='CHANGE_INPUT':w[key]['content_state']='AVAILABLE_UNCERTAIN'
 else:p['native_formation_inputs']=ready('UNCERTAIN').checkpoint()['native_formation_inputs']
 deny(c,p,'formation_witness_'+mutation)
