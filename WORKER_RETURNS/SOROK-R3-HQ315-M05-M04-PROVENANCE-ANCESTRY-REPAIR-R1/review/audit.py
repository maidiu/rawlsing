"""Audit literal courts, native ancestry receipts and immutable source preimages."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as ET,sys,re
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];M2=R/'runtime/m02';M1=M2/'runtime/m01'
START='a03927a05631f5706059a09f7a8575d63399933c';FREEZE='b13db9054533856e6710c647719efa29e8eaee5a'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def bh(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
def cases(folder):
 out={}
 for p in sorted((R/folder).rglob('junit.xml')):
  for c in ET.parse(p).getroot().iter('testcase'):
   k=(str(p.relative_to(R/folder)),c.get('classname'),c.get('name'));assert k not in out
   out[k]=next((v for tag,v in [('failure','FAIL'),('error','ERROR'),('skipped','SKIP')] if c.find(tag) is not None),'PASS')
 return out
before=cases('evidence/before');after=cases('evidence/after')
# Historical court remains a separate namespace/denominator throughout.
bh9={k:v for k,v in before.items() if k[0].startswith('historical_nine/')};ah9={k:v for k,v in after.items() if k[0].startswith('historical_nine/')}
b={k:v for k,v in before.items() if k not in bh9};a={k:v for k,v in after.items() if k not in ah9}
assert len(b)==len(a)==638 and b.keys()==a.keys()
assert list(b.values()).count('PASS')==628 and list(b.values()).count('FAIL')==10 and set(a.values())=={'PASS'}
assert bh9==ah9 and len(bh9)==9 and set(bh9.values())=={'FAIL'}
new=cases('evidence/m05_author');assert len(new)==48 and set(new.values())=={'PASS'}
write('04_LITERAL_638_BEFORE_AFTER.json',[dict(junit=k[0],classname=k[1],case=k[2],before=b[k],after=a[k]) for k in b])
write('05_NEW_AUTHOR_48_AND_HISTORICAL_NINE.json',dict(author=[dict(junit=k[0],classname=k[1],case=k[2],status=v) for k,v in new.items()],historical=[dict(junit=k[0],classname=k[1],case=k[2],before=v,after=ah9[k]) for k,v in bh9.items()]))
assert {k[2] for k,v in b.items() if v=='FAIL'}=={k[2] for k in b if k[0].startswith('m04_51/') and (k[2].startswith('test_cross_cell_none_owner_') or k[2].startswith('test_revoked_or_withdrawn_') or k[2].startswith('test_fully_rehashed_transition_'))}
# Unchanged scientific test/harness and source preimages.
rows=load('01_INPUT_SOURCE_IDENTITIES.json');src=[]
for row in rows:
 local=row['local'];p=R/local
 if local in ['candidate/cell.py','candidate/claim_provenance.py']:p=R/'runtime/m03_original'/Path(local).name
 data=p.read_bytes();assert bh(data)==row['blob_sha1'] and sha(data)==row['sha256'];assert data==git('show',row['commit']+':'+row['path'])
 src.append(dict(row,verified_original_local=str(p.relative_to(R))))
write('06_ORIGINAL_SOURCE_IDENTITIES_VERIFIED.json',src)
for family,commit,prefix in [(M2,'0216d9036a87e2f60f42fd5b2870556027808419','WORKER_RETURNS/SOROK-R3-HQ312-M02-MEMORY-MEDIATION-INDEPENDENT-R1'),(M1,'02187a14e75ff30dd953d3c7185d689b80e62304','WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1')]:
 for p in (family/'repro').glob('*.py'):
  if family==M1 and p.name in ('cell.py','claim_provenance.py'):continue
  assert p.read_bytes()==git('show',commit+':'+prefix+'/repro/'+p.name),p
freeze=load('03_AUTHOR_FREEZE.json')
for p,h in freeze['files'].items():assert sha((R/p).read_bytes())==h and (R/p).read_bytes()==git('show',FREEZE+':'+str(R.relative_to(ROOT))+'/'+p)
known={x['blob_sha1']:x for x in json.loads((M1/'02_SOURCE_IDENTITIES.json').read_text())}
refs=[]
for phase in ('before','after'):
 for suite in ('new','can3','author','owners'):
  d=load('evidence/'+phase+'/inherited413/'+suite+'/execution.json')
  assert d['exit_code']==0 and d['guard_byte_unchanged'] and d['guard_empty']
  for arg in d['pytest_args']:
   if not arg.endswith('.py'):continue
   rel=re.split(r'(?:<RETURN>|\[RETURN\])/',arg)[-1];p=M1/rel;data=p.read_bytes();h=bh(data)
   if p.name=='test_m01.py':row=dict(commit='02187a14e75ff30dd953d3c7185d689b80e62304',path='WORKER_RETURNS/SOROK-R3-HQ310-M01-MEMORY-MEDIATION-CAUSAL-CELL-R1/repro/test_m01.py')
   elif p.name=='test_repair.py':row=dict(commit='ee6a48b40247b113c614fe2099d4c443e8dd7bb7',path='WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/repro/test_repair.py')
   else:row=known[h]
   assert data==git('show',row['commit']+':'+row['path']);refs.append(dict(phase=phase,suite=suite,actual_file=str(p.relative_to(R)),source_commit=row['commit'],source_path=row['path'],blob_sha1=h,sha256=sha(data)))
write('07_LITERAL_EXECUTED_TEST_PREIMAGES.json',refs)
# Actual phase import receipts distinguish source overlay and native modules.
imports=[]
for phase in ('before','after'):
 actual=load('evidence/'+phase+'/m03_74/observations/actual_imports.json')
 for name,row in actual['files'].items():
  p=R/row['file'];original=R/'runtime/m03_original'/p.name if phase=='before' and name in ('cell','claim_provenance') else p
  data=original.read_bytes();assert bh(data)==row['blob_sha1'] and sha(data)==row['sha256']
  imports.append(dict(phase=phase,module=name,actual_import_file=row['file'],source_preimage=str(original.relative_to(R)),blob_sha1=bh(data),sha256=sha(data)))
 for p,row in load('evidence/'+phase+'/m02_100/actual_function_calls.json')['physical_function_sources'].items():
  f=M2/p;f=R/'runtime/m03_original'/f.name if phase=='before' and f.name=='cell.py' else f
  assert bh(f.read_bytes())==row['git_blob_sha1']
for name in ('cell.py','claim_provenance.py'):assert (R/'candidate'/name).read_bytes()==(M1/'repro'/name).read_bytes()
sys.path.insert(0,str(M1/'repro'));import bootstrap,cell,claim_provenance
from rawlsing_next import v3_psepf_zero_positive_guard as guard
assert not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
assert bh(Path(guard.__file__).read_bytes())=='e0528d65215cb431196570c38bac4eae94217a1b'
for phase in ('before','after'):
 for row in load('evidence/'+phase+'/inherited413/new/execution.json')['imports']:
  if row['module']=='cell':continue
  data=(M1/row['file']).read_bytes();assert bh(data)==row['blob_sha1'] and data==git('cat-file','blob',bh(data))
assert cell.source_hash()==load('evidence/after/m03_74/observations/actual_imports.json')['source_hash']
write('08_ACTUAL_IMPORT_AND_PATCH_AUDIT.json',dict(imports=imports,actual_source_grant=cell.source_hash(),guard_empty_and_unchanged=True,guard_blob='e0528d65215cb431196570c38bac4eae94217a1b',response_monkeypatch=False,native_owners_changed=False,changed_source=[dict(path='candidate/'+n,blob_sha1=bh((R/'candidate'/n).read_bytes()),sha256=sha((R/'candidate'/n).read_bytes())) for n in ('cell.py','claim_provenance.py')]))
# Full actual 36-arm conservation: unchanged raw owner/history; validated native reconstruction.
arms=[]
for p in sorted((R/'evidence/after/m02_100/observations').glob('factorial_*.json')):
 aft=json.loads(p.read_text());bef=load('evidence/before/m02_100/observations/'+p.name)
 assert bef['arm']==aft['arm'] and bef['pre']['owner_state']==aft['pre']['owner_state'] and bef['pre']['history']==aft['pre']['history']
 assert bef['actual_result']['streams']==aft['actual_result']['streams']==aft['arm']['expected_streams']
 assert aft['pre']['owner_state']==aft['actual_result']['read']['actual_state']==aft['post']['owner_state']
 proof=aft['actual_result']['read']['claim_selection_provenance']['native_owner_ancestry'];assert proof['rooted_in_first_journal'] and proof['current_owner_state_hash']==aft['pre']['owner_hash']
 arms.append(dict(arm=aft['arm'],streams=aft['actual_result']['streams'],native_owner_ancestry=proof,receipt=str(p.relative_to(R))))
assert len(arms)==36
comp=load('evidence/after/m02_100/observations/independent_CAN3_comparator.json');assert comp['stored']['state']==comp['omitted']['state']
write('09_FACTORIAL_NATIVE_ANCESTRY_AND_COMPARATOR.json',dict(arms=arms,comparator='evidence/after/m02_100/observations/independent_CAN3_comparator.json',parallel_not_serial=True))
closures=[]
for k,v in b.items():
 if v!='FAIL':continue
 name=k[2];tag='erase_owner_' if name.startswith('test_cross_cell') else 'resurrect_' if name.startswith('test_revoked') else 'forged_ancestry_'
 for p in sorted((R/'evidence/after/m04_51/observations').glob(tag+'*.json')):
  d=json.loads(p.read_text());assert d.get('restore_refusal') is not None or d.get('refusal') is not None
  # Public restore refusal retains its exact pre-call state; consumption refusals do likewise.
  if 'restore_refusal' in d:assert d['before']==d['after']
  elif 'after' in d:assert d['before']==d['after']
 closures.append(dict(case=name,before='FAIL',after='PASS',source_family=tag))
write('10_TEN_REDS_AND_ATOMICITY_CLOSURE.json',closures)
for family,pin in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:assert (M1/'runtime/can3/runtime/law'/(family+'.txt')).read_bytes()==git('cat-file','blob',pin)
changed=set(git('diff','--name-only',START).decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
foreign=[p for p in changed if not p.startswith(str(R.relative_to(ROOT))+'/')]
# Earlier completed PV3A and M04 ignored warm caches are preserved, not authored or imported as implementation.
assert all(p.startswith('WORKER_RETURNS/SOROK-R3-HQ314-M04-M03-INDEPENDENT-R1/') or p.startswith('WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-PV3A-HQ-METHOD-ACCESSION-EVIDENCE-R1/') for p in foreign),foreign
assert not any(not p.startswith(str(R.relative_to(ROOT))+'/') for p in git('diff','--name-only',START).decode().splitlines())
write('11_EXECUTED_RESULTS.json',dict(verdict='SOURCEFREE_NATIVE_OWNER_ANCESTRY_REPAIR_CANDIDATE_ONLY',before=dict(tests=638,passed=628,failed=10),after=dict(tests=638,passed=638,failed=0),new_author=dict(tests=48,passed=48,failed=0),current_total=dict(tests=686,passed=686,failed=0),historical=dict(tests=9,failed=9,separate=True),errors=0,skipped=0,published_portable_freeze_commit=FREEZE,actual_local_preexecution_freeze='15a25d19df648ab17b4af9e3dd28f3336fc5374e',portable_counterpart_created_after_execution=True,scientific_ceiling='FINITE_SOURCEFREE_PARALLEL_CONDITIONING_ONLY',serial_mediation='UNPROVED',M06_independent_review_required=True,source_role_overlap='This M05 implementation chat previously authored M04; it cannot independently accept this repair.',tracked_write_scope_verified=True,preexisting_foreign_untracked_cache_paths=len(foreign)))
print('AUDIT_OK: 628/10 -> 638/0 unchanged, new48 PASS, nine historical FAIL separately; candidate only')
