"""R2 entrypoint contracts; subsequent independent review still required."""
import copy
import json
from pathlib import Path
import socket
from collections import Counter,defaultdict
import pytest
from assay.architecture import build_packet,DerivedCache,form_owner,canonical,digest,Hold
from assay.transport import Frozen,MockIssuer,MockTransport,Runner,Denied
from assay.experiment import mock_permit,code_capture
from assay.scoring import score,paired,fraction,IntegrityError,UNIVERSE
from assay.oracle import proposed_key,check_key
from assay.corpus import MENUS

ROOT=Path(__file__).resolve().parent

@pytest.fixture(autouse=True)
def zero_network(monkeypatch):
 def deny(*a,**k):raise AssertionError('ZERO_REAL_MODEL_CALL_NETWORK_GUARD')
 monkeypatch.setattr(socket.socket,'connect',deny)
 monkeypatch.setattr(socket.socket,'connect_ex',deny)
 monkeypatch.setattr(socket,'getaddrinfo',deny)

@pytest.fixture
def frozen():
 return Frozen(ROOT,ROOT/(ROOT/'CURRENT_FREEZE').read_text().strip())

def sample(frozen,k='K1',phase='primary'):
 row=next(r for r in frozen.rows.values() if r['k']==k and r.get('phase','primary')==phase)
 return row,frozen.cases[row['case']],frozen.approved(row['id'])[0]

def dispatch(frozen,tmp_path,row,packet,changes=None,policy='lawful',fail_first=0):
 issuer=MockIssuer();grant=mock_permit(issuer,frozen,[row],**(changes or {}));t=MockTransport(policy,fail_first)
 with Runner(grant,issuer,frozen,t,tmp_path/'journal.jsonl') as runner:
  result=runner.call(row['id'],packet,row.get('max_tokens',256),row.get('response_format','typed'))
 return result,t

def test_rmb_01_opaque_ids_and_provider_payload(frozen):
 for row in frozen.rows.values():
  assert len(row['id'])==32 and all(c in '0123456789abcdef' for c in row['id'])
  p,_=frozen.approved(row['id'])
  assert set(p)=={'response_id','instruction','facts','representation','menu','output_schema'}
  assert row['case'] not in canonical(p).decode()
  assert 'expected' not in canonical(p).decode()

def test_rmb_02_menu_and_execution_balance(frozen):
 groups=defaultdict(Counter);orders=defaultdict(Counter);blocks=defaultdict(list)
 for r in frozen.rows.values():
  if r.get('phase','primary')!='primary':continue
  for code in r['menu']:groups[(r['case'],r['arm'],code)][r['menu'].index(code)]+=1
  orders[(r['case'],r['arm'])][r['execution_index']]+=1;blocks[r['block']].append(r)
 assert all(len(set(c.values()))==1 for c in groups.values())
 assert all(set(c)=={0,1,2} and len(set(c.values()))==1 for c in orders.values())
 assert all(len(v)==3 and len({tuple(x['menu']) for x in v})==1 for v in blocks.values())

def test_rmb_03_real_arm_mechanisms(frozen):
 row,case,_=sample(frozen);cache=DerivedCache();packets=[];receipts=[]
 for arm in ['A','B','C']:
  p,r=build_packet(case,row|{'arm':arm},cache);packets.append(p);receipts.append(r)
 assert len({digest(p['representation']) for p in packets})==3
 assert len({r['facts_digest'] for r in receipts})==1
 assert receipts[0]['owner']==receipts[1]['owner']==receipts[2]['owner']
 _,hot=build_packet(case,row|{'arm':'C'},cache);assert hot['cache']['cache_hit']
 cache.entries[next(iter(cache.entries))]['state']['asking_cost']='forged'
 with pytest.raises(Hold,match='CACHE_REBUILD'):build_packet(case,row|{'arm':'C'},cache)
 altered=copy.deepcopy(case);altered['history'][0]['value']='high'
 changed,_=build_packet(altered,row)
 assert changed['facts']['organization']!=packets[0]['facts']['organization']

def test_rmb_04_trace_origin_firewall(frozen):
 for case in frozen.cases.values():
  if case['k']!='K3':continue
  row=next(r for r in frozen.rows.values() if r['case']==case['id']);p,_=build_packet(case,row)
  text=canonical(p).decode()
  assert not any(secret in text for secret in case['hidden'].values())
  assert all(h['field']!='alertness' for h in p['facts']['accessible_history'])
  injected=copy.deepcopy(case);injected['hidden']['origin']='ANOTHER_PRIVATE_ORIGIN'
  other,_=build_packet(injected,row);assert other==p

def test_rmb_05_standing_belief_and_owner_separation(frozen):
 for case in frozen.cases.values():
  if case['k']!='K5':continue
  own=form_owner(case)
  prior=case['history'][0]['value'];assert own['state']['belief']==prior
  row=next(r for r in frozen.rows.values() if r['case']==case['id']);p,_=build_packet(case,row)
  assert 'PUBLIC_STANDING_CHANGE' not in canonical(p).decode()
  assert 'parents' not in p and 'owner' not in p and 'effects' not in p
  forged=copy.deepcopy(case);forged['world']['ratification']['issuer']='forged_registrar'
  assert not form_owner(forged)['public']['recorded']
  assert form_owner(forged)['state']['belief']==prior

def test_rmb_06_unadmitted_event_denied(frozen,tmp_path):
 row,case,p=sample(frozen);bad=copy.deepcopy(case);bad['history'][0]['admission']='DRAFT'
 with pytest.raises(Hold,match='UNADMITTED'):build_packet(bad,row)
 p['evaluator_only_metadata']={'origin':'secret'}
 with pytest.raises(Denied,match='UNFROZEN_REQUEST'):dispatch(frozen,tmp_path,row,p)

def test_rmb_07_all_trials_in_denominator(frozen):
 row,case,p=sample(frozen);rows=[row,row|{'id':'0'*32,'block':'1'*32}]
 expected=proposed_key([case]);ans=expected[case['id']]
 raw=json.dumps(dict(action=ans['actions'][0],**{k:v for k,v in ans.items() if k!='actions'}))
 records=score(rows,{row['id']:raw},expected)
 assert fraction(records)==.5 and len(records)==2

def test_rmb_08_independent_oracle_channel(frozen):
 cases=list(frozen.cases.values());key=proposed_key(cases)
 check_key(cases,key,UNIVERSE)
 corrupted=copy.deepcopy(key);sid=cases[0]['id'];corrupted[sid]['actions']=['NOT_A_VALID_CODE']
 with pytest.raises(IntegrityError):check_key(cases,corrupted,UNIVERSE)
 corrupted[sid]['actions']=['NO_SANCTION']
 with pytest.raises(IntegrityError,match='DISAGREEMENT'):check_key(cases,corrupted,UNIVERSE)

def test_rmb_09_pairing_requires_exact_ids():
 a=dict(id='a',block='a',case='x',family='f',k='K1',arm='A',correct=True)
 b=a|{'id':'b','block':'different','arm':'B'}
 with pytest.raises(IntegrityError):paired([a,b])

def test_rmb_10_honest_paired_interval():
 records=[]
 for i in range(6):
  a=dict(id=str(i),block=str(i),case=str(i),family=str(i),k='K1',arm='A',correct=False)
  records.extend([a,a|{'id':'b'+str(i),'arm':'B','correct':True}])
 out=paired(records)
 assert out['delta']==1 and out['paired_interval'][0]<1
 assert out['n_families']==6 and not out['promotion'] and not out['equivalence']
 assert out['minimum_clusters_for_5pp_precision']>1000

@pytest.mark.parametrize('changes',[
 {'privacy':'DENIED'},{'use':'DENIED'},{'model':'latest'},
 {'spend_cap_micro':-1},{'per_trial_call_budget':True},{'per_trial_call_budget':1.5},
])
def test_rmb_11_16_invalid_grant_zero_dispatch(frozen,tmp_path,changes):
 row,case,p=sample(frozen);issuer=MockIssuer();t=MockTransport();g=mock_permit(issuer,frozen,[row],**changes)
 with pytest.raises(Denied):Runner(g,issuer,frozen,t,tmp_path/'journal.jsonl')
 assert not t.requests

def test_rmb_17_full_mock_transport(frozen,tmp_path):
 row,case,p=sample(frozen)
 raw,t=dispatch(frozen,tmp_path,row,p)
 assert len(t.requests)==1 and json.loads(raw)['action'] in p['menu']
 journal=[json.loads(l) for l in (tmp_path/'journal.jsonl').read_text().splitlines()]
 assert [x['body']['op'] for x in journal]==['START','RESERVE','CAPTURE']
 assert journal[1]['body']['request_raw']==t.requests[0].decode()
 assert journal[2]['body']['response_raw']==raw

def test_rmb_18_executable_order_and_budget_nulls(frozen,tmp_path):
 for name in ['N3_ORDER','N7_BUDGET']:
  row,case,p=sample(frozen,'K3',name)
  raw,t=dispatch(frozen,tmp_path/name,row,p)
  req=json.loads(t.requests[0]);assert req['max_tokens']==(128 if name=='N7_BUDGET' else 256)
  assert json.loads(raw)['action'] in p['menu']

def test_rmb_19_secondary_free_text(frozen,tmp_path):
 row,case,p=sample(frozen,'K1','free_text')
 raw,t=dispatch(frozen,tmp_path,row,p)
 coded=code_capture(raw,row);assert 'text' in json.loads(raw)
 assert json.loads(coded)['action'] in p['menu']

def test_rmb_20_preserves_appeal(frozen):
 assert 'APPEAL' in MENUS['K1']
 for c in frozen.cases.values():
  if c['k']=='K1' and c['history'][0]['value']=='high':assert 'APPEAL' in proposed_key([c])[c['id']]['actions']

def test_rmb_21_preserves_private_doubt(frozen):
 assert 'REMAIN_DOUBTFUL' in MENUS['K5']
 for c in frozen.cases.values():
  if c['k']=='K5' and c['history'][0]['value']=='UNCERTAIN':assert 'REMAIN_DOUBTFUL' in proposed_key([c])[c['id']]['actions']

def test_rmb_22_policing_not_mandatory(frozen):
 for c in frozen.cases.values():
  if c['k']=='K6':assert 'NO_SANCTION' in proposed_key([c])[c['id']]['actions']

def test_rmb_23_capacity_factual_contrast(frozen):
 cases=[c for c in frozen.cases.values() if c['k']=='K6' and c['family']=='F0' and c['history'][0]['value'] is True]
 assert len(cases)==2
 packets=[]
 for c in cases:
  row=next(r for r in frozen.rows.values() if r['case']==c['id']);p,_=build_packet(c,row);packets.append(p['facts'])
 assert packets[0]!=packets[1]

def test_extra_retry_identical_and_persistent_ledger(frozen,tmp_path):
 row,case,p=sample(frozen);issuer=MockIssuer();g=mock_permit(issuer,frozen,[row]);t=MockTransport(fail_first=1)
 with Runner(g,issuer,frozen,t,tmp_path/'journal') as r:
  assert r.call(row['id'],p)
  assert r.used==2 and r.retries==1 and t.requests[0]==t.requests[1]
 with Runner(g,issuer,frozen,t,tmp_path/'journal') as r:
  with pytest.raises(Denied,match='REDRAW'):r.call(row['id'],p)
  assert r.used==2
 lines=(tmp_path/'journal').read_text().splitlines();x=json.loads(lines[-1]);x['body']['response_raw']='tampered';lines[-1]=json.dumps(x);(tmp_path/'journal').write_text('\n'.join(lines)+'\n')
 with pytest.raises(Denied):Runner(g,issuer,frozen,t,tmp_path/'journal')

@pytest.mark.parametrize('changes',[{'spend_cap_micro':0},{'total_call_budget':1,'spend_cap_micro':1},{'total_retry_budget':0}])
def test_extra_budget_no_bypass(frozen,tmp_path,changes):
 row,case,p=sample(frozen);issuer=MockIssuer();g=mock_permit(issuer,frozen,[row],**changes);t=MockTransport(fail_first=1)
 with Runner(g,issuer,frozen,t,tmp_path/'journal') as r:
  with pytest.raises(Denied):r.call(row['id'],p)
 assert len(t.requests)<2

@pytest.mark.parametrize('changes',[{'mode':'LIVE'},{'endpoint':'https://example.invalid'},{'issuer':'forged'},{'privacy':False},{'retention':False},{'freeze':'0'*64},{'per_trial_call_budget':3},{'total_call_budget':False},{'expires_at':'2000-01-01T00:00:00+00:00'}])
def test_extra_grant_scope_and_live_denials(frozen,tmp_path,changes):
 row,case,p=sample(frozen);issuer=MockIssuer();t=MockTransport()
 with pytest.raises(Denied):Runner(mock_permit(issuer,frozen,[row],**changes),issuer,frozen,t,tmp_path/'journal')
 assert not t.requests

def test_extra_bad_signature_and_custom_transport(frozen,tmp_path):
 row,case,p=sample(frozen);issuer=MockIssuer();g=mock_permit(issuer,frozen,[row]);g['signature']='bad';t=MockTransport()
 with pytest.raises(Denied):Runner(g,issuer,frozen,t,tmp_path/'journal')
 with pytest.raises(Denied):Runner(mock_permit(issuer,frozen,[row]),issuer,frozen,object(),tmp_path/'journal')
 with pytest.raises(Denied):MockTransport(lambda request:'network')

def test_extra_freeze_tamper_zero_dispatch(frozen,tmp_path):
 manifest=copy.deepcopy(frozen.manifest);manifest['files']={'data.txt':'0'*64}
 (tmp_path/'data.txt').write_text('tampered');(tmp_path/'freeze.json').write_text(json.dumps(manifest))
 with pytest.raises(Denied,match='FROZEN_BYTES'):Frozen(tmp_path,tmp_path/'freeze.json')

def test_extra_state_intervention_and_no_past_rewrite(frozen):
 c=copy.deepcopy(next(c for c in frozen.cases.values() if c['k']=='K4'))
 past=canonical(c['history'][0]);first=form_owner(c)
 c['history'][-1]['value']='same_authority';second=form_owner(c)
 assert first['state']['tension_scope']!=second['state']['tension_scope']
 assert canonical(c['history'][0])==past
