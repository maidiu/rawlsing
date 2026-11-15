import hashlib, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
cli=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(cli.parent))
from run_p4 import open_owner
from p3 import test_rules
p=Path(tempfile.mkdtemp(prefix="p4-independent-"))
def run(state,*args,sever=False):
    cmd=[sys.executable,str(cli)]
    if sever:
        cmd=[sys.executable,'-c','import run_p4; from p3 import test_rules; test_rules.B1_PATH=test_rules.B1_PATH.with_name("reviewer-absent-B1.py"); raise SystemExit(run_p4.main())']
    t=time.perf_counter()
    proc=subprocess.run(cmd+['--state',str(state),*args], cwd=cli.parent, capture_output=True,text=True,check=False)
    assert proc.returncode==(2 if sever else 0), (proc.stderr,proc.stdout)
    print('CLI',state.name,args,proc.returncode,round(time.perf_counter()-t,3),flush=True)
    return json.loads(proc.stdout)
def read(s):
    return json.loads((s/'p4_receipts.json').read_text())
def save(s,label,obj):
    (p/f'{s.name}-{label}.json').write_text(json.dumps(obj,indent=2))
def footing(x):
    return [x[k] for k in ('clock','tool_available','location','choices')], [{k:v for k,v in e.items() if k!='event_id'} for e in x['observations']]
def boundary(s, *, expected_material=1, actual=False):
    owner=open_owner(s/'actual-p2')
    try:
        session=owner.base_owner.fanin.session
        assert session.clock()==(232 if actual else 230)
        assert session.world().actor_state['A']['material_remaining']==expected_material
        intervals=[row for row in session.read_interval_states() if row['domain']['mode']=='ACTUAL']
        assert len(intervals)==int(actual)
        return list(session.events())
    finally:
        owner.close()
print('SCRATCH',p,'SOURCE',str(test_rules.B1_PATH),hashlib.sha256(test_rules.B1_PATH.read_bytes()).hexdigest(),flush=True)
s=p/'live'
opening=run(s,'new')
initial=read(s)
assert opening['choices']==['SAY','REQUEST_EDGE'] and all(x['kind']=='ARRIVAL' for x in opening['observations'])
assert not initial['turns'] and initial['antecedent']['psychology_head']['count']==1
assert run(s,'view')==opening
shutil.copytree(s,p/'baseline')
action=('say','  Please let me examine the bench edge.  ','--request-edge','--request-id','owner-input')
red=run(s,*action,sever=True)
assert red['reason']=='P3_B1_SOURCE_SEVERED' and read(s)==initial
assert not run(s,'inspect-edge','invented-before-invitation')['performed']
s.rename(p/'temporary')
shutil.copytree(p/'baseline',s)
accepted=run(s,*action)
assert run(s,'view')==accepted['next']
first=read(s)['turns'][0]
speech=first['receipt']['speech']
assert speech['attempt']['text']==speech['performed']['body']['text']==action[1]
assert speech['actor_access']['event_id']==speech['performed']['event_id']
assert speech['performed']['hash'] in first['receipt']['uptake']['readset']
assert test_rules.B1_SHA256 in first['receipt']['uptake']['readset']
assert first['before']==initial['antecedent']['identity']
assert all(first['before'][k]==first['after'][k] for k in ['actor','root','branch'])
assert first['after']['clock']==accepted['next']['clock']==accepted['observation']['clock']==230
assert first['receipt']['interval'] is None
assert all(e['kind'] != 'INSPECT' for e in boundary(s) if e['clock'] >= 230)
assert accepted['next']['invitation']==accepted['observation']['event_id']
assert run(s,*action)==accepted
owner=open_owner(s/'actual-p2')
try:
    sess=owner.base_owner.fanin.session
    assert sess.event(speech['performed']['event_id'])==speech['performed']
    assert sess.event(accepted['observation']['event_id'])==first['receipt']['expression']
    assert owner.snapshot().document()==first['after']
    from bp4.world import make_event
    actor=first['receipt']['uptake']['actor_alias']
    user=sess.meta['user_actor']
    world=sess.world()
    sentinels=('P4_REVIEW_ACTOR_ONLY_41e5','P4_REVIEW_USER_ONLY_2cbe')
    e=make_event(clock=world.clock,kind='INSPECT',actor_id=actor,location=world.positions[actor],summary=sentinels[0],body={'text':sentinels[0]},sequence=len(world.events))
    world.add_event(e)
    sess._append_event(e,perceive=(actor,))
    sess.product._append_episode(sess.branch_id,user,'PRIVATE_NOTE',world.clock,{'text':sentinels[1]})
    sess.product._checkpoint(sess.branch_id,world.clock,world)
    assert sess.event(e['event_id'])['summary']==sentinels[0]
    assert sess.episodes(user)[-1]['body']['text']==sentinels[1]
    ledger=read(s)
    ledger['turns'][-1]['after']=owner.snapshot().document()
    (s/'p4_receipts.json').write_text(json.dumps(ledger))
finally:
    owner.close()
privacy=run(s,'view')
assert all(k not in json.dumps(privacy) for k in (*sentinels,'actor_access','attempt_hash','readset','joint_check'))
blank=run(s,'say',' \t ')
assert blank['admission']=='EMPTY_SPEECH' and not blank['performed'] and blank['next']==privacy
assert read(s)['turns'][-1]['receipt']['speech']['performed'] is None
bad=run(s,'inspect-edge','foreign-invitation','--then-wait')
assert not bad['performed'] and bad['next']==privacy
assert read(s)['turns'][-1]['receipt']['interval'] is None
assert run(s,'view')==privacy
boundary(s)
second=run(s,'inspect-edge',accepted['next']['invitation'])
assert second['performed'] and second['observation']['body_public']['changed'] is False
assert second['next']['clock']==second['observation']['clock']==230 and second['next']['invitation'] is None
assert read(s)['turns'][-1]['receipt']['interval'] is None
assert any(e['event_id']==second['observation']['event_id'] for e in boundary(s))
assert run(s,'view')==second['next']
assert not run(s,'inspect-edge',accepted['next']['invitation'],'--then-wait')['performed']
boundary(s)
save(s,'final',read(s))
s.rename(p/'positive')
shutil.copytree(p/'baseline',s)
assert run(s,*action)==accepted
assert run(s,'view')==accepted['next']
boundary(s)
waited=run(s,'inspect-edge',accepted['next']['invitation'],'--then-wait','--request-id','owner-wait')
assert waited['performed'] and waited['observation']['body_public']['changed'] is False
assert waited['observation']['clock']==230 and waited['next']['clock']==232
assert waited['next']['invitation'] is None
turn=read(s)['turns'][-1]
assert turn['action']['then_wait'] is True
material=turn['receipt']['interval']['segments'][0]['world']
assert material['state_before']['material_remaining']==1 and material['state_after']['material_remaining']==0
events=boundary(s, expected_material=0, actual=True)
ids=[e['event_id'] for e in events]
assert ids.index(waited['observation']['event_id']) < ids.index(material['actual_action_event_id'])
assert events[ids.index(material['actual_action_event_id'])]['hash']==material['actual_action_event_hash']
assert run(s,'view')==waited['next']
assert run(s,'inspect-edge',accepted['next']['invitation'],'--then-wait','--request-id','owner-wait')==waited
boundary(s, expected_material=0, actual=True)
save(s,'waited',read(s))
s.rename(p/'restored')
shutil.copytree(p/'baseline',s)
different=run(s,'say','Do not invite me to inspect. I am leaving the edge.')
turn=read(s)['turns'][0]
assert turn['receipt']['speech']['performed']['hash']!=speech['performed']['hash']
assert turn['receipt']['speech']['performed']['hash'] in turn['receipt']['uptake']['readset']
assert turn['receipt']['uptake']['mode'] is None
assert turn['receipt']['uptake']['status']=='PERCEIVED_NO_INSPECTION_REQUEST'
assert different['observation'] is None and different['next']['invitation'] is None
assert turn['receipt']['speech']['attempt']['request_edge'] is False
s.rename(p/'decline')
shutil.copytree(p/'baseline',s)
no_request=run(s,'say',action[1])
assert no_request['observation'] is None and no_request['next']['invitation'] is None
assert first['receipt']['speech']['attempt']['request_edge'] is True
assert read(s)['turns'][0]['receipt']['speech']['attempt']['text']==action[1]
for history,expected in [('imposed_plan','private_check'),('','inspect_alone')]:
    sr=p/(history or 'empty')
    op=run(sr,'new','--history',history)
    assert footing(op)==footing(opening)
    if not history:
        assert read(sr)['antecedent']['psychology_head']['count']==0
    result=run(sr,*action)
    t=read(sr)['turns'][0]
    assert t['receipt']['interval']['segments'][0]['world']['state_before']==material['state_before']
    assert t['receipt']['uptake']['mode']==expected and result['next']['choices']==['SAY','REQUEST_EDGE']
    assert not run(sr,'inspect-edge',accepted['next']['invitation'])['performed']
    save(sr,'result',result)
print('PASS',p, 'material',material['state_before']['material_remaining'],material['state_after']['material_remaining'], 'event',speech['performed']['event_id'],'readset',first['receipt']['uptake']['readset'],'invitation',accepted['next']['invitation'],'inspection',second['observation']['event_id'],flush=True)
