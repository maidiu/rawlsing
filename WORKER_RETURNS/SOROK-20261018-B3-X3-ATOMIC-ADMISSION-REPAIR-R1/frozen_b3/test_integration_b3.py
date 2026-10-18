from copy import deepcopy
from dataclasses import replace,asdict
from pathlib import Path
import json,subprocess,sys
import pytest
from sources import m2,b2,ROOT,RUNTIME,load
from integration import Integration,digest
from f2_adapter import inputs,run_case
from fixture_authority import FixtureAuthority
from developmental_loop import execute,permission_for,World
import target_owner,source_guard

CASES=json.loads((RUNTIME/'f2/cases.json').read_text())['cases']
BY_ID={x['id']:x for x in CASES}

def engine(tmp_path,frame):
 a=FixtureAuthority();a.register_observed(frame);return Integration(tmp_path/'b3.sqlite',a),a

def projection(r):
 return {k:r.get(k) for k in ('status','code','original_event_hash','material_actor_activity','accessible_readset','independent_offer_refs','admissible_routes','history_material_hash','owner_effect_committed')}

@pytest.mark.parametrize('case',CASES,ids=[c['id'] for c in CASES])
def test_frozen_f2_on_actual_b3(case):
 actual=run_case(case)
 # The frozen oracle runs only here, after actual independent simulation returns.
 oracle=load('b3_f2_review',RUNTIME/'f2/reference_oracle.py')
 assert oracle.validate_native_receipt(case,actual)==[]
 assert actual['imports'][0]['relative_file']=='.runtime/b2/bridge.py'
 if actual['status']=='ELIGIBLE_NONCAUSAL':
  assert actual['admission']['b1_invoked'] is False
  assert len(actual['M2_temporal_traces'])>=1

@pytest.mark.parametrize('a,b',[('F2-001','F2-002'),('F2-003','F2-004'),('F2-005','F2-006'),('F2-001','F2-021')])
def test_labels_and_demography_cannot_cause_response(a,b):
 assert projection(run_case(BY_ID[a]))==projection(run_case(BY_ID[b]))

def test_material_act_changes_lineage_without_requiring_affect():
 a,b=(run_case(BY_ID[x]) for x in ('F2-001','F2-003'))
 assert a['history_material_hash']!=b['history_material_hash']
 assert a['selected_affect']==b['selected_affect']==None

def test_actual_material_offer_changes_available_action():
 a,b=(run_case(BY_ID[x]) for x in ('F2-001','F2-005'))
 assert 'JOINT_PRACTICAL_ACTION_POSSIBLE' in a['admissible_routes']
 assert 'JOINT_PRACTICAL_ACTION_POSSIBLE' not in b['admissible_routes']

def test_early_loss_cannot_use_future_speech():
 r=run_case(BY_ID['F2-007']);early,later=r['M2_temporal_traces']
 assert early['actual_speech_ids']==[]
 assert not any(c['mode']=='RECONSIDER' for c in early['candidates'])
 assert {(c['source'],c['stance']) for c in later['candidates'] if c['mode']=='RECONSIDER'}=={(u,s) for u in ('U-CARE','U-PEER') for s in ('ACCEPT','REJECT','SUSPEND')}
 assert len(r['source_admissions'])==5

def test_menu_does_not_use_m2_durable_append_or_reference_oracle(monkeypatch):
 def forbidden(*args,**kwargs):raise AssertionError('FORBIDDEN_SIMULATION_ENGINE')
 monkeypatch.setattr(m2,'append_test_only',forbidden);monkeypatch.setattr(m2,'fixture_grant',forbidden)
 oracle=load('b3_f2_reference_forbidden',RUNTIME/'f2/reference_oracle.py');monkeypatch.setattr(oracle,'evaluate',forbidden)
 r=run_case(BY_ID['F2-007'])
 assert not r['owner_effect_committed'] and r['CAN011_transition']['status']=='VALID_EMPTY'
 assert r['CAN008_response']['selected_belief'] is None

def test_poison_expected_outcomes_do_not_generate_behavior():
 c=deepcopy(BY_ID['F2-001']);c['expected']={'status':'REFUSED','code':'POISON'};c['group']='POISON'
 assert projection(run_case(c))==projection(run_case(BY_ID['F2-001']))

def test_idempotence_is_physical_and_cold(tmp_path):
 f=inputs(BY_ID['F2-001']);e,a=engine(tmp_path,f);r=e.run(f);before=e.snapshot();e.close()
 e=Integration(tmp_path/'b3.sqlite',a);again=e.run(f)
 assert again['exact_replay'] and again['new_event_count']==0 and e.snapshot()==before
 rows=e.db.execute('SELECT count(*) FROM b2_event_identity WHERE event_id=?',(f['event']['id'],)).fetchone()[0]
 assert rows==1 and r['new_event_count']==1;e.close()

@pytest.mark.parametrize('kind',['speech','history','affect'])
def test_renewed_fixture_attestation_cannot_rewrite_past_source(tmp_path,kind):
 f=inputs(BY_ID['F2-001'])
 if kind=='affect':
  f['evidence'].append(__import__('integration').seal(dict(id='old_affect',actor='child',owner='child',act='BIKE_CARE',time=7,source='WORLD',object='bike',note='distress')))
 e,a=engine(tmp_path,f);e.run(f);before=e.snapshot();forged=deepcopy(f)
 if kind=='speech':forged['utterances'][0]['claim']='rewritten group accusation'
 else:
  x=forged['evidence'][-1] if kind=='affect' else forged['evidence'][0]
  x['note']='opposite affect' if kind=='affect' else 'substantively rewritten history'
  x['hash']=digest({k:v for k,v in x.items() if k!='hash'})
 a.register_observed(forged) # even a malicious renewed source attestation cannot retcon
 r=e.run(forged)
 assert r['code']=='SOURCE_PREIMAGE_IDENTITY_COLLISION' and e.snapshot()==before;e.close()

@pytest.mark.parametrize('field',['heard_by','speaker','claim'])
def test_forged_speak_or_exposure_cannot_self_register(tmp_path,field):
 f=inputs(BY_ID['F2-001']);e,a=engine(tmp_path,f);before=e.snapshot();bad=deepcopy(f)
 bad['utterances'][1][field]=['child'] if field=='heard_by' else 'forged'
 r=e.run(bad)
 assert r['status']=='REFUSED' and e.snapshot()==before;e.close()

def test_unregistered_source_cannot_issue_occurrence(tmp_path):
 e=Integration(tmp_path/'x.sqlite');r=e.run(inputs(BY_ID['F2-001']));assert r['code']=='SYNTHETIC_SOURCE_ISSUER_NOT_REGISTERED';e.close()

def test_later_counterpart_independently_refuses_and_durable_history_is_recruited(tmp_path):
 yes=execute(tmp_path/'yes.sqlite',True);no=execute(tmp_path/'no.sqlite',False)
 a,b=yes['episodes'][-1]['receipt'],no['episodes'][-1]['receipt']
 assert a['CAN008_response']['practical_actions']==['CHECK_LOCK'] and b['CAN008_response']['practical_actions']==[]
 assert a['CAN008_response']['recruited'] and a['ADP016_memory']=='NOT_GRANTED'
 assert 'CONTACT_POSSIBLE' not in a['admissible_routes']
 assert yes['episodes'][-1]['actor_actions'][-1]['action']=='DECLINE_CONTACT'
 assert a['immutable_history']['source']==b['immutable_history']['source']
 for result in (yes,no):
  root=[rows for rows in result['final_snapshot']['b3_source'] if rows[0]=='loss:t3'][0]
  assert json.loads(root[1])['content']['fact']=='stolen'
 assert yes['episodes'][0]['receipt']['M2_temporal_traces'][0]['actual_speech_ids']==[]
 assert len(yes['episodes'][3]['receipt']['M2_temporal_traces'][-1]['candidates'])>=7
 assert len(yes['final_middle'])==1 and not no['final_middle']

def test_no_compulsory_counterpart_refusal(tmp_path):
 b=execute(tmp_path/'allow.sqlite',False,other_due=False)
 assert b['episodes'][-1]['actor_actions'][-1]['action']=='ALLOW_CONTACT'
 assert 'CONTACT_POSSIBLE' in b['episodes'][-1]['receipt']['admissible_routes']
 assert b['final_middle']==[]

def test_cold_process_replay_exact_receipts_and_sql(tmp_path):
 bundle=execute(tmp_path/'live.sqlite');p=tmp_path/'trace.json';p.write_text(json.dumps(bundle))
 cmd=[sys.executable,str(ROOT/'developmental_loop.py'),'replay',str(p),str(tmp_path/'replay.sqlite')]
 replay=json.loads(subprocess.check_output(cmd,cwd=ROOT))
 assert replay['snapshot_hash']==bundle['snapshot_hash']
 assert digest(replay['receipts'])==digest([e['receipt'] for e in bundle['episodes']])

@pytest.mark.parametrize('source',['speech','history','affect'])
def test_m3_source_rewrites_block_at_b3_quarantine(source):
 s=m2.seed_scene();old=source_guard.preimages(s)
 if source=='speech':
  x=replace(s.speech[0],words='different prior words');s=replace(s,speech=(x,)+s.speech[1:])
 else:
  index=1 if source=='history' else 2;child=s.actors[0];x=replace(child.history[index],activity='changed source')
  history=list(child.history);history[index]=x
  s=replace(s,actors=(replace(child,history=tuple(history)),)+s.actors[1:],history_witnesses=tuple(replace(w,history_hash=digest(asdict(x))) if w.actor=='child' and w.history_id==x.id else w for w in s.history_witnesses))
 with pytest.raises(m2.Refusal,match='SOURCE_PREIMAGE_IDENTITY_COLLISION'):source_guard.check(old,s)

def test_target_owner_independent_rule_refuses_forged_or_stale_permission():
 w=World()
 for t in range(1,8):w.tick(t)
 f=w.frame();good=permission_for([],f)
 proposal=dict(actor='child',before=digest([]),rule_hash=target_owner.RULE_HASH,time=7,parents=[x['hash'] for x in f['evidence'] if x['act']=='PRACTICE_COMPLETED'])
 with pytest.raises(target_owner.Denied,match='PERMISSION_DENIED'):target_owner.validate([],f['event'],f['evidence'],proposal,good,())
 rec=target_owner.validate([],f['event'],f['evidence'],proposal,good,(good,))
 assert rec['kind']=='V3MS_PRACTICE'
 with pytest.raises(target_owner.Denied,match='STALE|UNBOUND'):target_owner.validate([rec],f['event'],f['evidence'],proposal,good,(good,))
 bad=deepcopy(f['evidence']);bad=[x for x in bad if x['id']!='check:7']
 with pytest.raises(target_owner.Denied,match='PRACTICE_MISSING'):target_owner.validate([],f['event'],bad,proposal,good,(good,))

@pytest.mark.parametrize('conflicting',[False,True])
def test_real_two_process_duplicate_race(tmp_path,conflicting):
 import os,select
 frames=[inputs(BY_ID['F2-001']) for _ in range(2)]
 if conflicting:
  frames[1]['event']['content']['object']='a-different-bicycle'
  frames[1]['event']['content_hash']=digest(frames[1]['event']['content'])
 workers=[];ready=[]
 for i,f in enumerate(frames):
  p=tmp_path/(str(i)+'.json');p.write_text(json.dumps(f))
  worker=subprocess.Popen([sys.executable,str(ROOT/'process_b3.py'),str(p),str(tmp_path/'race.sqlite')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,cwd=ROOT)
  assert select.select([worker.stdout],[],[],20)[0]
  ready.append(json.loads(worker.stdout.readline()));workers.append(worker)
 for worker in workers:worker.stdin.write('GO\n');worker.stdin.flush()
 results=[]
 for worker in workers:
  output,err=worker.communicate(timeout=30);assert worker.returncode==0,err
  results.append(json.loads(output))
 assert len({x['pid'] for x in ready})==2
 statuses=sorted(x['receipt']['status'] for x in results)
 assert statuses==(['ELIGIBLE_NONCAUSAL','REFUSED'] if conflicting else ['ELIGIBLE_NONCAUSAL']*2)
 e=Integration(tmp_path/'race.sqlite');snapshot=e.snapshot();e.close()
 roots=[r for r in snapshot['b2_event_identity'] if r[0]==frames[0]['event']['id']]
 assert len(roots)==1
 evidence=ROOT/'evidence/races';evidence.mkdir(exist_ok=True)
 (evidence/('conflicting.json' if conflicting else 'same.json')).write_text(json.dumps({'ready':ready,'results':results,'snapshot':snapshot},indent=2)+'\n')

def test_heard_by_without_actual_exposure_receipt_is_not_access(tmp_path):
 f=inputs(BY_ID['F2-007']);f['exposures']=[];e,a=engine(tmp_path,f);before=e.snapshot()
 r=e.run(f);assert r['status']=='REFUSED' and r['code']=='OTHER_ACTOR_PRIVATE_READ' and e.snapshot()==before;e.close()

def test_later_hearing_is_not_inserted_back_into_processed_past(tmp_path):
 f=inputs(BY_ID['F2-001']);e,a=engine(tmp_path,f);e.run(f);before=e.snapshot()
 late=deepcopy(f);late['as_of']=100;late['utterances'][1]['heard_by']=['child'];late['readset'].append('E-P-SPEECH')
 x=next(x for x in late['evidence'] if x['id']=='E-P-SPEECH')
 late['exposures'].append(dict(id='heard:U-PEER',speech_id='U-PEER',listener='child',time=62,observer='child',speech_witness=x['id'],source_hash=x['hash'],issuer='B3_TEST_ONLY_EXPOSURE_REGISTRY'))
 a.register_observed(late);r=e.run(late)
 assert r['code']=='PAST_EXPOSURE_INSERTION' and e.snapshot()==before
 late['exposures'][-1]['time']=95;a.register_observed(late);r=e.run(late)
 assert r['status']=='ELIGIBLE_NONCAUSAL'
 assert 'U-PEER' in r['M2_temporal_traces'][-1]['exposure_ids'];e.close()

def test_future_exposure_is_refused_without_state_change(tmp_path):
 f=inputs(BY_ID['F2-001']);f['exposures'][0]['time']=100;e,a=engine(tmp_path,f);before=e.snapshot()
 r=e.run(f);assert r['code']=='EXPOSURE_TIME_OR_SOURCE_INVALID' and e.snapshot()==before;e.close()
