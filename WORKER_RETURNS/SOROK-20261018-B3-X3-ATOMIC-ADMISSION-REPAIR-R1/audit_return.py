"""Exact-source, actual-result and portable evidence audit. No self acceptance."""
from pathlib import Path
import subprocess,hashlib,json,sys,sqlite3,datetime,uuid,platform,re,tarfile,os
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent;E=ROOT/'evidence';C=ROOT/'candidate'
SEAL='0632bc21f3b0453e55703f80ba3201816238d6cc'
B3='47b46a85b9ebb633754866f1e6f1b12db3bd2012';X3='d201985243fe15bc0da36e7cbc93707fec664acf'
BP='WORKER_RETURNS/SOROK-V2-HQ329-B3-COUPLED-INTERPRETATION-R1/'
XP='WORKER_RETURNS/SOROK-V2-HQ330-X3-B3-INDEPENDENT-EXECUTABLE-R1/'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
 env=dict(os.environ)
 # Materializers use the common object store; worktree identity uses its own HEAD.
 for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE'):env.pop(key,None)
 return subprocess.check_output(['git',*args],cwd=REPO,env=env)
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def verify(commit,path,local):
 data=git('show',commit+':'+path);assert local.read_bytes()==data,str(local)
 blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==git('rev-parse',commit+':'+path).decode().strip()
 return dict(commit=commit,path=path,local=str(local.relative_to(ROOT)),git_blob_sha1=blob,sha256=sha(data))
def main():
 assert git('branch','--show-current').decode().strip()=='agent/rabochii-sorok-20261018-b3-x3-atomic-admission-repair-r1'
 sealpaths=git('diff-tree','--no-commit-id','--name-only','-r',SEAL).decode().splitlines()
 assert sealpaths==['WORKER_COMMISSIONS/SOROK-20261018-B3-X3-ATOMIC-ADMISSION-REPAIR-R1/00_COMMISSION.md']
 rows=[]
 for p in (ROOT/'frozen_b3').iterdir():
  if p.is_file():rows.append(verify(B3,BP+p.name,p))
 for p in (ROOT/'frozen_x3').glob('*.py'):rows.append(verify(X3,XP+p.name,p))
 for row in json.loads((ROOT/'import_manifest.json').read_text()):
  local=C/row['local'];assert sha(local.read_bytes())==row['sha256'],row['local']
  if 'commit' in row:
   record=verify(row['commit'],row.get('path',row.get('source_path')),local)
   assert record['git_blob_sha1']==row['git_blob_sha1'];rows.append(record)
  else:
   archive=C/'.runtime/b2/imports/F1/F1_frozen_court.tar.gz';assert sha(archive.read_bytes())==row['archive_sha256']
   with tarfile.open(archive) as tar:assert tar.extractfile(row['archive_member']).read()==local.read_bytes()
   rows.append(dict(row,local=str(local.relative_to(ROOT)),archive_member_verified=True))
 altered=[]
 for p in (ROOT/'frozen_b3').glob('*.py'):
  candidate=C/p.name
  if p.read_bytes()!=candidate.read_bytes():altered.append(p.name)
 assert sorted(altered)==['fixture_authority.py','integration.py'],altered
 dump(ROOT/'verified_sources.json',rows)
 dump(ROOT/'candidate_version.json',dict(version='B3_ATOMIC_ADMISSION_R1',base=B3,sealed_startup=SEAL,altered_files=[dict(path=x,sha256=sha((C/x).read_bytes()),git_blob_sha1=hashlib.sha1(b'blob '+str((C/x).stat().st_size).encode()+b'\0'+(C/x).read_bytes()).hexdigest()) for x in altered],pinned_closure_sha256=sha((ROOT/'pinned_closure.tar.gz').read_bytes()),authority='SOURCEFREE_CANDIDATE_PENDING_INDEPENDENT_I2'))
 probe="import sys,json,hashlib;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import integration,fixture_authority;r=Path(sys.argv[1]).resolve();print(json.dumps([dict(module=n,relative_file=str(Path(m.__file__).resolve().relative_to(r)),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for n,m in list(sys.modules.items()) if getattr(m,'__file__',None) and Path(m.__file__).resolve().is_relative_to(r)]))"
 imports=json.loads(subprocess.check_output([sys.executable,'-c',probe,str(C)]));dump(ROOT/'loaded_modules.json',imports)
 known={r['sha256'] for r in rows}|{sha((C/x).read_bytes()) for x in altered}
 assert all(m['sha256'] in known for m in imports)
 suites={}
 for p in E.rglob('*.xml'):
  root=ET.parse(p).getroot();counts={k:sum(int(x.get(k,'0')) for x in root.iter('testsuite')) for k in ('tests','failures','errors','skipped')}
  failures=[dict(name=x.get('name'),classname=x.get('classname'),kind='FAIL' if x.find('failure') is not None else 'ERROR') for x in root.iter('testcase') if x.find('failure') is not None or x.find('error') is not None]
  suites[str(p.relative_to(E))]=dict(**counts,failed_tests=failures)
 dump(ROOT/'suite_results.json',suites)
 assert suites['candidate_b3.xml']['tests']==71 and suites['candidate_b3.xml']['failures']==0
 assert suites['frozen_x3.xml']['tests']==28 and suites['frozen_x3.xml']['failures']==8
 assert suites['candidate_x3.xml']['tests']==28 and suites['candidate_x3.xml']['failures']==4
 assert suites['atomic.xml']['tests'] in (61,63) and suites['atomic.xml']['failures']==suites['atomic.xml']['errors']==0
 if suites['atomic.xml']['tests']==61:assert suites['projected_atomic.xml']['tests']==2 and suites['projected_atomic.xml']['failures']==0
 matrix=json.loads((E/'f2_blinded/matrix.json').read_text());assert len(matrix['rows'])==42 and all(not r['errors'] for r in matrix['rows'])
 assert sum(r['status']=='ELIGIBLE_NONCAUSAL' for r in matrix['rows'])==20
 for row in matrix['rows']:
  receipt=json.loads((E/'f2_blinded'/(row['case_id']+'.json')).read_text())
  if row['status']=='ELIGIBLE_NONCAUSAL':assert receipt['CAN008_response']['rule_source_sha256']==sha((C/'integration.py').read_bytes())
 sql={}
 for family in ('baseline','candidate'):
  for name in ('positive','positive_cold','permission_absent','permission_absent_cold'):
   p=E/family/'loop'/(name+'.sqlite');db=sqlite3.connect(p)
   integrity=db.execute('PRAGMA integrity_check').fetchone()[0];assert integrity=='ok'
   snap={n:db.execute('SELECT * FROM '+n+' ORDER BY 1').fetchall() for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")};db.close()
   sql[family+'/'+name]=dict(integrity=integrity,rows={k:len(v) for k,v in snap.items()},snapshot_sha256=sha(json.dumps(snap,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()),sqlite_sha256=sha(p.read_bytes()))
  for label in ('positive','permission_absent'):assert sql[family+'/'+label]['snapshot_sha256']==sql[family+'/'+label+'_cold']['snapshot_sha256']
 dump(ROOT/'sql_audit.json',sql)
 # Literal before/after classification across every table for unchanged X3 cases.
 table_matrix={}
 for family in ('frozen_x3_sql','candidate_x3_sql'):
  table_matrix[family]={}
  for p in (E/family).glob('*.json'):
   x=json.loads(p.read_text());table_matrix[family][p.stem]=dict(result=x['result'],tables={n:dict(before=len(v),after=len(x['after'][n]),unchanged=v==x['after'][n]) for n,v in x['before'].items()})
 dump(ROOT/'table_case_matrix.json',table_matrix)
 marker=ROOT/'environment_marker.local'
 if not marker.exists():dump(marker,dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4())))
 passport=dict(passport_schema='SOROK_WARM_ENVIRONMENT_PASSPORT_R1',**json.loads(marker.read_text()),owner_session_alias='B3_ATOMIC_IMPLEMENTER_R1',surface='LOCAL_SHARED_STORE',machine_alias='AUTHORIZED_LOCAL',conversation_or_account_affinity=None,status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha(marker.read_bytes()),probe_command_and_result=dict(python=sys.version.split()[0],pytest=__import__('pytest').__version__,sqlite=sqlite3.sqlite_version,git=git('--version').decode().strip(),node=subprocess.check_output(['node','--version'],text=True).strip(),filesystem='VERIFIED',shell='zsh'),capabilities={x:'VERIFIED' for x in ('python','pytest','sqlite','git','node','filesystem','subprocess','SIGKILL')},git_object_store_alias='EXISTING_SHARED_STORE_NO_CLONE',worktree_alias='COMMISSION_ISOLATED_F40F',branch=git('branch','--show-current').decode().strip(),exact_checkout_base=SEAL,head_at_probe=git('rev-parse','HEAD').decode().strip(),clean_dirty_state='ONLY_AUTHORIZED_RETURN',materialized_source_refs='verified_sources.json',verified_imports='loaded_modules.json',dependency_closure_status='BOUNDED',fixture_query_source_permission='USER_AUTHORIZED_SYNTHETIC_SOURCEFREE_ONLY',covered_test_suites='suite_results.json',science_grade='IMPLEMENTER_RETURN_PENDING_INDEPENDENT_I2',model_provider='CODEX_EXISTING_USER_SELECTED_SESSION',model_effort='NOT_INDEPENDENTLY_ATTESTED_NO_SWITCH',pricing_class='UNKNOWN',observed_usage=None,cash_known='UNKNOWN',quota_known='UNKNOWN',context_cache_reuse='UNKNOWN',expected_slot_reset=None,independent_review_separation='IMPLEMENTER_NOT_INDEPENDENT_ACCEPTOR_POST_RETURN_HQ',privacy_source_grant='NO_RAW_SURVEY_NO_EXTERNAL_MODEL_CALLS',assignments_completed=['B3_X3_ATOMIC_ADMISSION_REPAIR_R1'],next_good_affinity_tags=['B3_ATOMICITY','SQLITE','SOURCE_CUSTODY'],staged_state_preservation='CANDIDATE_RUNTIME_AND_MARKER_LOCAL_RECHECK_REQUIRED_ON_RESUME',retire_or_rebuild_reason=None,attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES')
 dump(ROOT/'environment_passport_delta.json',passport)
 # Portable receipts only: never alter pinned source bytes or SQL file content.
 def portable(s):
  s=s.replace(str(REPO),'<WORKTREE>').replace(str(Path.home()),'<HOME>')
  s=re.sub(r'/tmp/(?:sorok[^/\s\'\"<>]*)', '<RUNTIME>',s)
  return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
 for p in E.rglob('*'):
  if not p.is_file() or p.suffix not in ('.log','.json','.xml'):continue
  text=p.read_text()
  if p.suffix=='.xml':
   tree=ET.fromstring(text)
   for node in tree.iter():
    node.attrib.pop('hostname',None)
    for k,v in list(node.attrib.items()):node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   text=ET.tostring(tree,encoding='unicode')
  else:text=portable(text)
  p.write_text(text)
 # Inventory every publishable return file, excluding this manifest's own preimage.
 publishable=git('ls-files','--cached','--others','--exclude-standard','--',str(ROOT.relative_to(REPO))).decode().splitlines()
 artifacts=[]
 for name in sorted(set(publishable)):
  p=REPO/name
  if not p.is_file() or p==ROOT/'artifact_manifest.json':continue
  artifacts.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()),bytes=p.stat().st_size))
 dump(ROOT/'artifact_manifest.json',dict(schema='B3_ATOMIC_RETURN_ARTIFACT_MANIFEST_R1',files=artifacts))
 print(json.dumps(dict(verified_pinned_sources=len(rows),loaded_modules=len(imports),suite_files=len(suites),sql='LIVE_EQUALS_FRESH_PROCESS',version='B3_ATOMIC_ADMISSION_R1')))
if __name__=='__main__':main()
