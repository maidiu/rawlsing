from pathlib import Path
import subprocess,sys,json,hashlib,time,os,shutil
R=Path(__file__).resolve().parents[1];C=R/'runtime/candidate_checkout';W=C/'WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1';O=R/'04_ORIGINAL_NEW_REAL_JUNIT_COLD';O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(C),*args],text=True).strip()
def run(label,cmd,cwd=C,env=None):
 t=time.monotonic();p=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);pid=p.pid;out,_=p.communicate();(O/(label+'.log')).write_text(out);v=dict(label=label,argv=list(map(str,cmd)),cwd=str(cwd),pid=pid,exit=p.returncode,seconds=time.monotonic()-t);(O/(label+'.command.json')).write_text(json.dumps(v,indent=2)+'\n');print(label,p.returncode,out[-800:],flush=True);return v
assert git('rev-parse','HEAD')=='f7824794bc6674c662734c9a8b110dd3df224be7'
tracked=git('ls-files').splitlines();skip=[x for x in git('ls-files','-v').splitlines() if x.startswith('S ')]
identity=dict(candidate_head=git('rev-parse','HEAD'),candidate_remote=git('remote','get-url','origin'),tracked_files=len(tracked),missing_tracked=[p for p in tracked if not (C/p).exists() and not (C/p).is_symlink()],sparse_skip=skip,python=sys.executable,python_version=sys.version,phase_a='947da9aa64d83ca8cd18cccfd037f12b049d1946')
records=[]
for manifest in ['staged_manifest.json','selected_manifest.json','supplement_manifest.json','readonly_and_temporal_manifest.json']:
 rows=json.loads((W/'discovery'/manifest).read_text())
 if isinstance(rows,dict): rows=rows.get('records',rows.get('files',[]))
 for row in rows:
  if not all(k in row for k in ['commit','source','path','blob']):continue
  records.append(dict(manifest=manifest,**row))
specs=[v['commit']+':'+v['source'] for v in records]
p=subprocess.run(['git','-C',str(C),'cat-file','--batch-check=%(objectname) %(objecttype)'],input='\n'.join(specs)+'\n',text=True,capture_output=True,check=True)
for row,line in zip(records,p.stdout.splitlines()):
 path=W/row['path'];b=path.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row.update(independent_git_preimage=line,actual_blob=actual,actual_sha256=sha(b),exact=actual==row['blob']==line.split()[0])
identity['closure_records']=records;identity['nonexact']=[x for x in records if not x['exact']];(R/'02_ACTUAL_FULL_OWNER_IMPORTS_AND_SHAS.json').write_text(json.dumps(identity,indent=2)+'\n')
assert not identity['missing_tracked'] and not skip
assert not [x for x in identity['nonexact'] if x['path'].endswith('.py')],identity['nonexact']
runs=[]
for name in ['independent_cold_a','independent_cold_b']:
 runs.append(run(name,[sys.executable,'-B',str(W/'repro/wp2.py'),str(O/(name+'.json'))],cwd=W))
 if runs[-1]['exit']:raise SystemExit(runs[-1]['exit'])
a,b=[O/(name+'.json') for name in ['independent_cold_a','independent_cold_b']]
receipt=dict(runs=runs,distinct_processes=runs[0]['pid']!=runs[1]['pid'],byte_identical=a.read_bytes()==b.read_bytes(),sha256_a=sha(a.read_bytes()),sha256_b=sha(b.read_bytes()))
(O/'independent_cold_replay.json').write_text(json.dumps(receipt,indent=2)+'\n')
identity['cold_imports']=[json.loads((O/(name+'.imports.json')).read_text()) for name in ['independent_cold_a','independent_cold_b']];(R/'02_ACTUAL_FULL_OWNER_IMPORTS_AND_SHAS.json').write_text(json.dumps(identity,indent=2)+'\n')
env=dict(os.environ,WP2_PRODUCT=str(a),PYTHONDONTWRITEBYTECODE='1')
wp2_test=run('wp2_unchanged',[sys.executable,'-m','pytest','-q',str(W/'tests/test_wp2.py'),'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/'wp2_unchanged.xml')],cwd=W,env=env)
r=run('original_full_owner_suites',[sys.executable,'-B',str(W/'repro/run_suites.py')],cwd=W)
for row in json.loads((W/'05_REAL_PYTEST_COLD_JUNIT/suite_results.json').read_text()):
 for suffix in ['.xml','.log']:
  src=W/'05_REAL_PYTEST_COLD_JUNIT'/(row['label']+suffix)
  if src.exists():shutil.copyfile(src,O/('independent_'+row['label']+suffix))
shutil.copyfile(W/'05_REAL_PYTEST_COLD_JUNIT/suite_results.json',O/'independent_suite_results.json')
run('owner_import_probe',[sys.executable,'-B',str(W/'repro/owner_import_probe.py')],cwd=W)
src=W/'05_REAL_PYTEST_COLD_JUNIT/owner_import_probe.json'
if src.exists():shutil.copyfile(src,O/'independent_owner_import_probe.json')

assert wp2_test['exit']==0,wp2_test
assert r['exit']==0,r
