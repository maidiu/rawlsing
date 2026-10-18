"""Verify executable evidence and exact bytes independently of suite exit status."""
from pathlib import Path
import subprocess,json,hashlib,xml.etree.ElementTree as ET,tarfile,io
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent;OUT=ROOT/'evidence'
FIX='8f7966d6d0bbb1ea2e57359de9defbcf552268bd';OLD='358fd1086eac0a4aa7791ca14abc25c45b935ddd'
B2='WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
def read(p):return json.loads(p.read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def totals(p):
 s=ET.parse(p).find('testsuite');return {k:int(s.get(k)) for k in ('tests','failures','errors','skipped')}
def audit():
 # Repair only portable placeholder escaping in evidence XML from the initial sanitizer.
 for p in OUT.rglob('*.xml'):
  try:ET.parse(p)
  except ET.ParseError:
   s=p.read_text()
   for token in ('E3','WORKTREE','HOME','TEMP'):s=s.replace('<'+token+'>','&lt;'+token+'&gt;')
   p.write_text(s);ET.parse(p)
 frozen=read(OUT/'frozen_manifest.json')
 for row in frozen:
  data=git('show',row['commit']+':'+row['path']);assert sha(data)==row['sha256']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
  assert (ROOT/row['staged']).read_bytes()==data
 x2=git('show','931aec3497c60114444806c375d1bb51ec7c0e7d:WORKER_RETURNS/SOROK-V2-HQ326-X2-B2-INDEPENDENT-EXECUTABLE-R1/test_hostile_x2.py')
 assert (ROOT/'.runtime/tests_after/R1/frozen/test_hostile_x2.py').read_bytes()==x2
 for phase,commit in [('old',OLD),('fixed',FIX)]:
  dest=OUT/phase;manifest=read(dest/'source_manifest.json');imports=read(ROOT/'.runtime'/phase/'imported_sources.json');assert len(imports)==69
  for row in manifest:
   if '/evidence/' in row['staged_path'] or row['staged_path'].endswith('execution_receipt.json'):continue
   data=(ROOT/row['staged_path']).read_bytes();assert sha(data)==row['sha256']
   if 'git_blob_sha1' in row:assert git('cat-file','blob',row['git_blob_sha1'])==data
  loaded=read(dest/'loaded_modules.json')
  for module,row in loaded['modules'].items():
   data=(ROOT/'.runtime'/phase/row['path']).read_bytes();assert sha(data)==row['sha256']
  assert loaded['modules']['bridge']['sha256']==sha(git('show',commit+':'+B2+'/bridge.py'))
  receipt=read(dest/'execution_receipt.json');assert sum(r['tests'] for r in receipt['totals'].values())==330
  for label,n in [('b1',39),('p1',74),('f1',97),('integration',81)]:assert totals(dest/'inherited'/(label+'.xml'))==dict(tests=n,failures=0,errors=0,skipped=0)
  native=read(dest/'inherited/f1_native_gate.log');assert native['status']=='RED' and len(native['failures'])==17
  assert next(c for c in receipt['commands'] if c['label']=='f1_native_gate')['exit_code']==1
  # Supplementary JUnit mirrors raw native JSON, without changing the native oracle.
  suites=ET.Element('testsuites');suite=ET.SubElement(suites,'testsuite',name='F1 raw native summary (derived)',tests='36',failures='17',errors='0',skipped='0')
  failures={r['case_id']:r['errors'] for r in native['failures']}
  for row in read(dest/'inherited/f1_applicability.json'):
   case=ET.SubElement(suite,'testcase',name=row['case_id'])
   if row['case_id'] in failures:ET.SubElement(case,'failure',message=';'.join(failures[row['case_id']])).text='Raw native STATUS_MISMATCH; not a native-positive pass.'
  ET.ElementTree(suites).write(dest/'native_f1_derived.xml',encoding='utf-8',xml_declaration=True)
 for mode in ('positive','journal_only'):
  assert (OUT/'old/inherited/vertical'/mode/'trace.json').read_bytes()==(OUT/'fixed/inherited/vertical'/mode/'trace.json').read_bytes()
 expected={'old/strict':(2,2),'fixed/strict':(2,0),'fixed/r1':(45,0),'fixed/e2_full':(44,2),'fixed/x2':(17,1),'fixed/repair5':(5,0),'fixed/independent':(26,0)}
 for name,(n,f) in expected.items():
  t=totals(OUT/(name+'.xml'));assert t==dict(tests=n,failures=f,errors=0,skipped=0),(name,t)
 commands=read(OUT/'commands.json');assert all(c['exit']==c['expected_exit'] for c in commands)
 for committed in (False,True):
  lock=read(OUT/'fixed/e3_sql'/('lock_conflict_'+str(committed)+'.json'))
  assert len({r['pid'] for r in lock['processes']})==2 and lock['committed']==lock['after']
  assert all(r['trace'][0]=='BEGIN IMMEDIATE' for r in lock['processes'])
  for phase in ('old','fixed'):
   strict=read(OUT/phase/'sql'/('strict_legacy_after_'+str(committed)+'.json'));assert strict['before']==strict['after']
   assert (strict['receipt']['event_admission']=='NOT_PERFORMED')==(phase=='fixed')
 fixdelta=git('diff-tree','--no-commit-id','--name-only','-r',FIX).decode().splitlines()
 prefix='WORKER_RETURNS/SOROK-V2-USERDIRECT-B2-LEGACY-REENTRY-REPAIR-R1/'
 assert all(p==B2+'/bridge.py' or p.startswith(prefix) for p in fixdelta)
 compare=git('diff','--name-only','950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883',OLD,'--',B2).decode().splitlines();assert compare==[B2+'/bridge.py']
 changes=git('diff','--name-only','ccc84471c27b6dbe3ff1040dcaf78a3070746e99','--').decode().splitlines()
 assert all(p.startswith(str(ROOT.relative_to(REPO))+'/') for p in changes)
 (ROOT/'candidate_diff.patch').write_bytes(git('diff',FIX+'^',FIX,'--',B2))
 dump(ROOT/'verification_receipt.json',dict(verdict='SOURCEFREE_BFIRST_EVENT_CUSTODY_ACCEPT_SCOPED',candidate=FIX,old=OLD,source_and_frozen_preimages_verified=True,inherited_per_phase=330,independent=26,remaining_native_reds=list(failures),historical_observational_failures=3,exact_suite_results=read(OUT/'summary.json'),candidate_delta=fixdelta,limits=['synthetic SQLite B2 ingress only','trusted fixture registrar and well-formed B1 ledger records','privileged B1/SQL writes remain possible','no production event signer or owner grant','full occurrence scan under writer lock','SIGKILL is not power loss']))
 print('E3 audit PASS; scoped event-custody acceptance only')
if __name__=='__main__':audit()
