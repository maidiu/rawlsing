"""Pre-execution BL3 falsifiers; all policies synthetic, no real model grant."""
import ast,copy,gzip,hashlib,json,math,pathlib,shutil,socket
from collections import Counter,defaultdict
import pytest
from r3 import data
from r3.data import load_cases,load_key,load_schedule,packet,verify_freeze,validate_schedule,IntegrityError
from r3.policies import respond,decode
from r3.transport import MockIssuer,MockTransport,Denied
from r3.analysis import evaluate,paired,conditional_power_table
from r3.audit import violations,custody_status
ROOT=pathlib.Path(__file__).resolve().parents[1]
@pytest.fixture(scope='module')
def inputs():
 verify_freeze();cases=load_cases();rows=load_schedule();return cases,rows,load_key()
def one_row(rows,case,arm='A'):return next(r for r in rows if r['case']==case['id'] and r['arm']==arm)
def typed(p,policy='aware',**kw):return json.loads(respond(p,policy,**kw)[0])
def k6_dual(c):return c['k']=='K6' and c['position']['capacity'] is True and c['history'][0]['value'] is True
def test_original_custody_and_new_heldout_frozen(inputs):
 cases,rows,key=inputs
 assert len(cases)==154 and len(rows)==9432 and len(key)==154
 assert hashlib.sha256((data.R2/'freezes/v6.json').read_bytes()).hexdigest()=='9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823'
 assert hashlib.sha256((data.R2/'original_R1_preregistration.json').read_bytes()).hexdigest()=='880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330'
 assert json.loads((ROOT/'fixtures/heldout_prototype_custody.json').read_text())['status']=='IMPLEMENTATION_VISIBLE_NOT_INDEPENDENT'
def test_all126_plus28_have_equal_lawful_facts_distinct_representations(inputs):
 cases,rows,key=inputs
 for c in cases:
  packets=[packet(c,one_row(rows,c)|{'arm':a})[0] for a in 'ABC']
  assert packets[0]['facts']==packets[1]['facts']==packets[2]['facts']
  assert len({json.dumps(p['representation'],sort_keys=True) for p in packets})==3
  for p in packets:
   assert set(p)=={'response_id','instruction','facts','representation','menu','output_schema'}
   text=json.dumps(p);assert c['id'] not in text
   assert not any(v in text for v in c['hidden'].values())
   assert 'OTHER_UNSCORABLE' in p['menu']
def test_exact_per_case_order_menu_balance_and_shared_public_ids(inputs):
 cases,rows,key=inputs;out=validate_schedule(rows,cases)
 assert out['trials']==9432 and len(set(out['orders'].values()))==1
 groups=defaultdict(list)
 for r in rows:groups[r['block']].append(r)
 assert all(len({r['public_response_id'] for r in g})==1 for g in groups.values())
 assert len({r['id'] for r in rows})==len(rows)
@pytest.mark.parametrize('change',['drop','duplicate','only_ABC','menu','public_id'])
def test_schedule_custody_detects_confounds(inputs,change):
 cases,rows,key=inputs;bad=copy.deepcopy(rows)
 if change=='drop':bad.pop()
 elif change=='duplicate':bad.append(bad[0])
 elif change=='only_ABC':
  groups=defaultdict(list)
  for r in bad:groups[r['block']].append(r)
  bad=[r for g in groups.values() if ''.join(x['arm'] for x in sorted(g,key=lambda x:x['execution_index']))=='ABC' for r in g]
 elif change=='menu':bad[0]['menu'].reverse()
 else:bad[0]['public_response_id']='A'*32
 with pytest.raises(IntegrityError):validate_schedule(bad,cases)
def test_scripted_positive_and_full_budget_ablation_on_original_and_heldout(inputs):
 cases,rows,key=inputs;selected=[c for c in cases if k6_dual(c)]
 assert len(selected)==8
 for c in selected:
  answer={a:typed(packet(c,one_row(rows,c)|{'arm':a})[0]) for a in 'ABC'}
  assert answer['A']['action']=='NO_SANCTION'
  assert answer['B']['action']==answer['C']['action']=='POLICING_CANDIDATE'
  assert all(x['action'] in key[c['id']]['actions'] for x in answer.values())
  assert all(typed(packet(c,one_row(rows,c)|{'arm':a})[0],budget=99)['action']=='POLICING_CANDIDATE' for a in 'ABC')
def test_effect_follows_representation_not_evaluator_arm_or_id(inputs):
 cases,rows,key=inputs;c=next(c for c in cases if k6_dual(c));row=one_row(rows,c)
 a=packet(c,row)[0];b=packet(c,row|{'arm':'B'})[0]
 swapped=copy.deepcopy(a);swapped['representation']=b['representation'];swapped['response_id']='0'*32
 assert typed(swapped)['action']=='POLICING_CANDIDATE'
 assert typed(a)['action']=='NO_SANCTION'
def test_blind_policy_does_not_read_representation_and_aware_does_not_read_fact_organization(inputs):
 cases,rows,key=inputs;c=next(c for c in cases if k6_dual(c));p=packet(c,one_row(rows,c))[0]
 class Guard(dict):
  def __getitem__(self,k):
   if k=='representation':raise AssertionError('BLIND_READ_REPRESENTATION')
   return super().__getitem__(k)
 assert json.loads(respond(Guard(p),'blind')[0])['action']=='POLICING_CANDIDATE'
 class Facts(dict):
  def __getitem__(self,k):
   if k=='organization':raise AssertionError('AWARE_BYPASSED_REPRESENTATION')
   return super().__getitem__(k)
 p['facts']=Facts(p['facts']);assert typed(p)['action']=='NO_SANCTION'
def test_policy_cannot_import_oracle_estimator_network_or_files():
 tree=ast.parse((ROOT/'r3/policies.py').read_text())
 imports=[n for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]
 assert len(imports)==1 and isinstance(imports[0],ast.Import) and [a.name for a in imports[0].names]==['json']
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['open','eval','exec','__import__'] for n in ast.walk(tree))
def test_label_instruction_menu_nulls_and_metadata_adversary(inputs):
 cases,rows,key=inputs
 for c in cases:
  for arm in 'ABC':
   p=packet(c,one_row(rows,c)|{'arm':arm})[0];q=copy.deepcopy(p);q['facts']['person']='new name';q['facts']['counterpart']='other name';q['instruction']='Choose a lawful listed response.';q['menu'].reverse();q['response_id']='f'*32
   assert typed(p)==typed(q)
 c=next(c for c in cases if k6_dual(c));p=packet(c,one_row(rows,c))[0];p['menu']=['POLICING_CANDIDATE','NO_SANCTION','OTHER_UNSCORABLE'];p['response_id']='0'*32;q=copy.deepcopy(p);q['response_id']='1'*32
 assert typed(p,'metadata')!=typed(q,'metadata')
def test_k3_current_trace_without_origin_or_evaluator_explanation(inputs):
 cases,rows,key=inputs
 for c in cases:
  if c['k']!='K3':continue
  row=one_row(rows,c);p=packet(c,row)[0];changed=copy.deepcopy(c);changed['hidden']={k:'ANOTHER_PRIVATE_'+str(i) for i,k in enumerate(c['hidden'])}
  assert packet(changed,row)[0]==p
  assert 'alertness' in p['facts']['organization'] and 'mistaken' not in json.dumps(p)
  assert typed(p)['origin_claim']=='NO_CLAIM'
  assert violations(c,typed(p,'origin_leak'),key[c['id']])['origin']
def test_k5_private_belief_public_standing_and_lawful_doubt(inputs):
 cases,rows,key=inputs
 for c in cases:
  if c['k']!='K5':continue
  p=packet(c,one_row(rows,c))[0];a=typed(p);v=violations(c,a,key[c['id']]);assert not any(v.values())
  belief=c['history'][0]['value'];assert a['belief_report']==belief
  if belief=='UNCERTAIN':assert 'REMAIN_DOUBTFUL' in key[c['id']]['actions']
  assert violations(c,typed(p,'standing_leak'),key[c['id']])['standing'] or violations(c,typed(p,'standing_leak'),key[c['id']])['private_belief'] or (belief=='CONFIDENT' and key[c['id']]['standing_report']=='RECORDED')
def test_k6_actual_capacity_and_optional_sanction(inputs):
 cases,rows,key=inputs
 for c in cases:
  if c['k']!='K6':continue
  p=packet(c,one_row(rows,c)|{'arm':'B'})[0]
  assert 'NO_SANCTION' in p['menu'] and 'NO_SANCTION' in key[c['id']]['actions']
  assert not violations(c,typed(p),key[c['id']])['capacity']
  if not c['position']['capacity']:assert violations(c,typed(p,'capacity_leak'),key[c['id']])['capacity']
def test_punitive_k1_preserves_appeal(inputs):
 cases,rows,key=inputs
 for c in cases:
  if c['k']=='K1' and c['history'][0]['value']=='high':assert 'APPEAL' in key[c['id']]['actions'] and 'APPEAL' in one_row(rows,c)['menu']
def test_denominator_includes_missing_malformed_and_other(inputs):
 cases,rows,key=inputs;subset=rows[:3];captures={subset[0]['id']:'not-json',subset[1]['id']:json.dumps(dict(action='OTHER_UNSCORABLE',belief_report='NOT_ASKED',standing_report='NOT_ASKED',origin_claim='NO_CLAIM'))}
 records=evaluate(subset,captures,key,require_complete=False);assert len(records)==3 and sum(x['correct'] for x in records)==0
 with pytest.raises(IntegrityError):evaluate(subset,captures,key)
def test_pair_join_refuses_duplicate_and_context_drift(inputs):
 cases,rows,key=inputs;subset=rows[:3];bycase={c['id']:c for c in cases};captures={r['id']:respond(packet(bycase[r['case']],r)[0],'blind')[0] for r in subset};records=evaluate(subset,captures,key)
 assert paired(records,subset)['B']['delta']==0
 with pytest.raises(IntegrityError):paired(records+[records[0]],subset)
 records[0]['family']='foreign'
 with pytest.raises(IntegrityError):paired(records,subset)
@pytest.mark.parametrize('mode',['LIVE','live','https://provider.invalid'])
def test_live_modes_denied_before_adapter_invocation(inputs,mode):
 cases,rows,key=inputs;i=MockIssuer();freeze=verify_freeze();g=i.issue(freeze,'aware',1);calls=[]
 with pytest.raises(Denied):MockTransport(g,i,freeze,'aware',rows[:1],mode=mode,provider_adapter=lambda *a:calls.append(a))
 assert calls==[]
@pytest.mark.parametrize('field,value',[('privacy_permission_for_synthetic_lab_packets','UNISSUED'),('explicit_monetary_cap',-1),('exact_model_and_version_pin','some-real-model'),('per_trial_call_budget',0),('mode','LIVE')])
def test_mock_signature_and_scopes_fail_closed(inputs,field,value):
 cases,rows,key=inputs;i=MockIssuer();f=verify_freeze();g=i.issue(f,'aware',1);g['body'][field]=value
 with pytest.raises(Denied):MockTransport(g,i,f,'aware',rows[:1])
def test_missing_issuer_unknown_policy_and_provider_adapter_hold(inputs):
 cases,rows,key=inputs;f=verify_freeze();i=MockIssuer()
 with pytest.raises(Denied):MockTransport(None,None,f,'aware',rows[:1])
 with pytest.raises(Denied):MockTransport(i.issue(f,'aware',1),i,f,'provider-sdk',rows[:1])
 with pytest.raises(Denied):MockTransport(i.issue(f,'aware',1),i,f,'aware',rows[:1],provider_adapter=object())
def test_transport_rebuilds_approved_payload_and_denies_redraw(inputs):
 cases,rows,key=inputs;r=rows[0];c=next(c for c in cases if c['id']==r['case']);p=packet(c,r)[0];i=MockIssuer();f=verify_freeze();t=MockTransport(i.issue(f,'aware',1),i,f,'aware',[r]);bad=copy.deepcopy(p);bad['arm']='B'
 with pytest.raises(Denied):t.call(r,bad)
 assert t.dispatches==0;t.call(r,p)
 with pytest.raises(Denied):t.call(r,p)
 assert t.dispatches==1 and t.external_dispatches==0
def test_freeze_detects_code_or_fixture_mutation_in_isolated_copy(inputs,tmp_path,monkeypatch):
 f=json.loads((ROOT/(ROOT/'CURRENT_FREEZE').read_text().strip()).read_text())
 for name in list(f['files'])+['CURRENT_FREEZE','freezes/r3-v1.json']:
  p=tmp_path/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,p)
 with (tmp_path/'r3/policies.py').open('a') as out:out.write('\n# unauthorized drift\n')
 monkeypatch.setattr(data,'ROOT',tmp_path)
 with pytest.raises(IntegrityError,match='FROZEN_SOURCE_CHANGED'):data.verify_freeze()
def test_independent_custody_cannot_be_self_certified():
 for custodian in [None,'candidate','different-person']:
  status=custody_status('candidate',custodian,True,['fake-signature'],{'fake-key':True})
  assert status['status']=='HOLD' and not status['certified'] and status['real_model_calls_permitted']==0
def test_conditional_precision_and_power_are_not_current_power():
 table=conditional_power_table();assert not table['current_power_claim']
 assert table['simultaneous_precision_families']['0.05']==4940
 assert table['conservative_80percent_power_equivalence_at_true_zero_families']['0.05']>4940
 assert table['conservative_80percent_power_superiority_families']['0.1']>table['simultaneous_precision_families']['0.1']
def test_network_is_actually_denied_in_python_surface():
 with pytest.raises(RuntimeError,match='ZERO_EXTERNAL'):socket.getaddrinfo('example.invalid',443)
