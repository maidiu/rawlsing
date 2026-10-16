"""Independent read-only evidence adjudication and source custody audit."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as ET,re,platform,sys,datetime,uuid
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];M2=R/'runtime/m02';M1=M2/'runtime/m01'
START='2f4482ae23960037da4ebee84501916dc6e5b422'
M03='e1f7a74e51201b9614bcc578348b4e9db7be7bd3';P3='WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1'
M02='0216d9036a87e2f60f42fd5b2870556027808419';P2='WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1'
M01='02187a14e75ff30dd953d3c7185d689b80e62304';P1='WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def matrix(folder):
 rows=[]
 for p in sorted((R/folder).rglob('junit.xml')):
  tree=ET.parse(p).getroot()
  for c in tree.iter('testcase'):
   status=next((s for tag,s in [('failure','FAIL'),('error','ERROR'),('skipped','SKIP')] if c.find(tag) is not None),'PASS')
   rows.append(dict(suite=str(p.relative_to(R/folder)),classname=c.get('classname'),name=c.get('name'),status=status))
 return rows
b=matrix('evidence/before');a=matrix('evidence/after');author=matrix('evidence/author');hist=matrix('evidence/historical_nine');fresh=matrix('evidence/fresh')
assert len(a)==len(b)==513 and len(author)==74
assert [tuple(x[k] for k in ['suite','classname','name']) for x in a]==[tuple(x[k] for k in ['suite','classname','name']) for x in b]
assert sum(x['status']=='PASS' for x in b)==511 and sum(x['status']=='FAIL' for x in b)==2
assert all(x['status']=='PASS' for x in a+author)
assert len(hist)==9 and all(x['status']=='FAIL' for x in hist)
assert len(fresh)==51 and sum(x['status']=='FAIL' for x in fresh)==10 and sum(x['status']=='PASS' for x in fresh)==41
for x,y in zip(a,b):x['baseline_status']=y['status']
write('04_LITERAL_587_CASE_MATRIX.json',a+[dict(x,baseline_status='AUTHOR_NEW_NOT_IN_M01') for x in author])
write('05_FRESH_51_CASE_MATRIX.json',fresh);write('06_SEPARATE_HISTORICAL_NINE.json',hist)
# Independent literal test preimages for all 587 executable test cases.
known={x['blob_sha1']:x for x in json.loads((M1/'02_SOURCE_IDENTITIES.json').read_text())}
known[blob((M1/'repro/test_m01.py').read_bytes())]=dict(commit=M01,path=P1+'/repro/test_m01.py')
cp='WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/repro/test_repair.py';cc='ee6a48b40247b113c614fe2099d4c443e8dd7bb7'
known[blob(git('show',cc+':'+cp))]=dict(commit=cc,path=cp)
source_refs=[]
for suite in ['new','can3','author','owners']:
 d=load('evidence/after/original_413/'+suite+'/execution.json')
 assert d['guard_byte_unchanged'] and d['guard_empty'] and d['exit_code']==0
 for arg in d['pytest_args']:
  if not arg.endswith('.py'):continue
  rel=re.split(r'(?:<RETURN>|\[RETURN\])/',arg)[-1];p=M1/rel;v=p.read_bytes();ref=known[blob(v)]
  assert v==git('show',ref['commit']+':'+ref['path'])
  source_refs.append(dict(suite=suite,actual_file=str(p.relative_to(R)),commit=ref['commit'],source_path=ref['path'],blob_sha1=blob(v),sha256=sha(v)))
for suite,p,c,source in [('M02_100',M2/'repro/test_independent.py',M02,P2+'/repro/test_independent.py'),('M03_74',R/'repro/test_author.py',M03,P3+'/repro/test_author.py')]:
 v=p.read_bytes();assert v==git('show',c+':'+source);source_refs.append(dict(suite=suite,actual_file=str(p.relative_to(R)),commit=c,source_path=source,blob_sha1=blob(v),sha256=sha(v)))
# Preserve and authenticate the historical court's actual source files and exact nine IDs.
historical_execution=load('evidence/historical_nine/execution.json')
assert historical_execution['exit']==1 and historical_execution['guard_empty_and_unchanged']
assert {x['name'] for x in hist}=={x['name'] for x in historical_execution['exact_original_cases']}
historical_original=cp.replace('repro/test_repair.py','inherited/repro/test_independent.py')
known[blob(git('show',cc+':'+historical_original))]=dict(commit=cc,path=historical_original)
historical_source_refs=[]
for arg in historical_execution['pytest_args']:
 if '.py::' not in arg:continue
 rel=re.split(r'(?:<RETURN>|\[RETURN\])/',arg)[-1].split('::')[0];p=M2/rel;v=p.read_bytes();ref=known[blob(v)]
 assert v==git('show',ref['commit']+':'+ref['path'])
 row=dict(actual_file=str(p.relative_to(R)),commit=ref['commit'],source_path=ref['path'],blob_sha1=blob(v),sha256=sha(v))
 if row not in historical_source_refs:historical_source_refs.append(row)
write('evidence/historical_nine/EXACT_TEST_SOURCE_IDENTITIES.json',historical_source_refs)
write('07_LITERAL_TEST_SOURCE_IDENTITIES.json',source_refs)
# Trace physical function sources and imported module bytes, independent of asserted counts.
trace=load('evidence/after/independent_100/actual_function_calls.json')
assert trace['no_response_monkeypatch'] and trace['production_guard']['registry_empty'] and trace['production_guard']['byte_unchanged']
for p,row in trace['physical_function_sources'].items():assert blob((M2/p).read_bytes())==row['git_blob_sha1']
actual=load('evidence/author/observations/actual_imports.json')
imports=[]
for name,row in actual['files'].items():
 p=R/row['file'];v=p.read_bytes();assert blob(v)==row['blob_sha1'] and sha(v)==row['sha256'];assert v==git('cat-file','blob',blob(v))
 imports.append(dict(module=name,actual_import_file=row['file'],blob_sha1=blob(v),sha256=sha(v)))
for name,pin in [('cell.py','3eb2d02aee8dc840e7cac1f99230d7c69adc2f58'),('claim_provenance.py','2434bda6f4b00e6ea5881291f5422227e8045e74')]:
 assert (M1/'repro'/name).read_bytes()==(R/'candidate'/name).read_bytes()==git('cat-file','blob',pin)
# Independent live import identities in this audit process; no new experiment outcomes used.
sys.path.insert(0,str(M1/'repro'));import bootstrap,cell,claim_provenance
from rawlsing_next import v3_psepf_zero_positive_guard as guard
assert not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
assert blob(Path(guard.__file__).read_bytes())=='e0528d65215cb431196570c38bac4eae94217a1b'
live=[]
for name,module in sorted(sys.modules.items()):
 f=getattr(module,'__file__',None)
 if f and Path(f).suffix=='.py' and name.startswith(('candidate','rawlsing_next','cell','claim_provenance','bootstrap')):
  p=Path(f).resolve();v=p.read_bytes();assert v==git('cat-file','blob',blob(v));live.append(dict(module=name,actual_module_file=str(p.relative_to(R)),blob_sha1=blob(v),sha256=sha(v)))
assert cell.source_hash()==actual['source_hash']
for name,h in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
 assert (M1/'runtime/can3/runtime/law'/(name+'.txt')).read_bytes()==git('cat-file','blob',h)
write('08_SOURCE_AND_IMPORT_AUDIT.json',dict(live_imports=live,author_execution_imports=imports,actual_source_grant=cell.source_hash(),physical_function_trace_verified=True,guard_empty_unchanged=True,guard_blob='e0528d65215cb431196570c38bac4eae94217a1b',tests_unchanged=True,actual_author_body_mutation_control='evidence/author/observations/provenance_source_body_mutation.json'))
# Verify all M01 and M02 executable harness bytes beyond explicit M03 overlay.
for c,source,root in [(M01,P1,M1),(M02,P2,M2),(M03,P3,R)]:
 for p in git('ls-tree','-r','--name-only',c,source+'/repro').decode().splitlines():
  rel=p[len(source)+1:]
  if c==M01 and rel=='repro/cell.py':continue
  assert (root/rel).read_bytes()==git('show',c+':'+p),rel
freeze=load('03_FREEZE_MANIFEST.json')
for p,h in freeze['files'].items():assert sha((R/p).read_bytes())==h
assert git('show','3b529996ddd05c3c84225d2054428ff943091aef:'+str(R.relative_to(ROOT))+'/review/test_falsifiers.py')==(R/'review/test_falsifiers.py').read_bytes()
# Preserve causal factorial, source->commit->read->response, and historical comparator.
fac=[]
for p in sorted((R/'evidence/after/independent_100/observations').glob('factorial_*.json')):
 after=json.loads(p.read_text());before=load('evidence/before/independent_100/observations/'+p.name)
 assert before['arm']==after['arm'] and before['pre']['owner_state']==after['pre']['owner_state']
 assert before['pre']['history']==after['pre']['history']
 for d in [before,after]:
  assert d['pre']['owner_state']==d['actual_result']['read']['actual_state']==d['post']['owner_state']
  assert d['actual_result']['streams']==d['arm']['expected_streams']
  kinds=[x['kind'] for x in d['post']['journal']]
  assert 'FIRST_EVENT_COMPLETE' in kinds and kinds[-1]=='M01_CAN008_CURRENT_RESPONSE_GRAPH'
  assert d['actual_result']['receipt']['payload']['read']==d['actual_result']['read']
 fac.append(dict(arm=after['arm'],streams=after['actual_result']['streams'],owner_hash=after['pre']['owner_hash'],same_before_after_owner=True,same_before_after_history=True,actual_owner_read=True,source_event=after['first_admitted_event'],receipt=str(p.relative_to(R))))
assert len(fac)==36
comp=load('evidence/after/independent_100/observations/independent_CAN3_comparator.json')
write('09_FACTORIAL_AND_COMPARATOR.json',dict(arms=fac,comparator_receipt='evidence/after/independent_100/observations/independent_CAN3_comparator.json',comparator_top_level_keys=list(comp),parallel_not_serial=True))
# Analyze frozen failures from saved actual packets, without substituting an expected result.
proofs=[]
for p in sorted((R/'evidence/fresh/observations').glob('*.json')):
 d=json.loads(p.read_text())
 if not p.stem.startswith(('erase_owner','resurrect_','forged_ancestry')):continue
 assert d['refusal'] is None
 s=d['before']['ctx']['state'];out=d['observed'];jid=d['before']['journal'][0]
 first=next(x for x in jid if x['kind']=='FIRST_EVENT_COMPLETE')['payload']['state']
 if p.stem.startswith('erase_owner'):
  assert len(first['stances'])==1 and len(s['stances'])==0 and not s['epistemic_transitions']
  assert out['streams']['epistemic']=='AMPLIFY'
  detail='Actual first committed BELIEF remains in journal; replacement current owner has zero stances/transitions, accepted as NONE.'
 elif p.stem.startswith('resurrect_'):
  assert len(s['epistemic_transitions'])==2
  snap=s['state_sets'][d['before']['claim_id']]
  assert snap['last_transition_ref']!=s['epistemic_transitions'][-1]['transition_id']
  assert out['streams']['epistemic']=='REROUTE'
  detail='Later native revision remains in transitions, but snapshot points to prior ADD; permit and REROUTE resurrected.'
 else:
  actual_pre=next(x for x in jid if x['kind']=='ADP017_COMMIT')['payload']['before']
  forged=s['epistemic_transitions'][0]['pre_state_hash'];assert forged!=actual_pre
  assert out['streams']['epistemic']=='REROUTE'
  detail='Effect/transition/snapshot rehashed around unrelated pre-state, different from actual ADP017 commit pre-state, yet accepted.'
 proofs.append(dict(receipt=str(p.relative_to(R)),observed_streams=out['streams'],committed_response='receipt' in out,detail=detail))
assert len(proofs)==10
write('10_FAILURE_PROOFS.json',proofs)
changed=set(git('diff','--name-only',START).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
assert all(p.startswith(str(R.relative_to(ROOT))+'/') for p in changed),changed
write('11_REVIEW_RESULTS.json',dict(verdict='REVIEW_REVISE',baseline=dict(inherited=413,m02_pass=98,m02_fail=2),published=dict(tests=587,passed=587,failed=0,skipped=0,errors=0),independent=dict(tests=51,passed=41,failed=10,errors=0,skipped=0),historical=dict(tests=9,passed=0,failed=9,separate=True),blocker_families=3,frozen_commit='3b529996ddd05c3c84225d2054428ff943091aef',actual_law_collision=False,I3_escalation_required=False,write_scope_verified=True))
print('M04_AUDIT_OK: published 587 PASS; fresh 41 PASS / 10 FAIL; historical nine FAIL separately; REVIEW_REVISE')
