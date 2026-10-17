"""Stage exact Git preimages, never respondent/source files. Run from repository."""
from pathlib import Path
import ast, hashlib, json, subprocess

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parents[1]
PIN = 'eede2b8bdb9fcdcc1d4187912f8e00773869c22c'
START = '246fcdf7b25c6b160c0a167e4284e08d04194505'
RUNTIME = HERE / 'runtime' / 'pinned'
QRA = 'data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'
SEEDS = [
 'rawlsing_next/tests/test_pre553_route_b_production.py',
 'rawlsing_next/tests/test_pre553_batch_runner.py',
 'rawlsing_next/tests/test_objective_consumer_bounded_evidence_d07.py',
 'rawlsing_next/objective_consumer_bounded_evidence.py',
 'data/ddm_build_copy/ddm_v550_question_relation_authority.py', QRA,
 'data/ddm_build_copy/manifests/source_dataset_manifest.csv',
 'data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv',
 'data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.csv',
 'data/ddm_build_copy/authority/response_scale_encoding_registry_35wave_active_v1.manifest.json',
]

def git(*args):
 return subprocess.check_output(['git', *args], cwd=REPO)

def stage():
 paths = set(git('ls-tree','-r','--name-only',PIN).decode().splitlines())
 todo = list(SEEDS)
 done = {}
 while todo:
  path = todo.pop()
  if path in done: continue
  assert path in paths, path
  assert not path.lower().endswith(('.sav','.dta','.por','.zsav'))
  data = git('show', f'{PIN}:{path}')
  dst=RUNTIME/path; dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
  sha=hashlib.sha256(data).hexdigest()
  blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  assert blob == git('rev-parse',f'{PIN}:{path}').decode().strip()
  done[path]={'sha256':sha,'git_blob':blob,'size':len(data),
   'startup_blob':git('rev-parse',f'{START}:{path}').decode().strip()}
  if path.endswith('.py'):
   for node in ast.walk(ast.parse(data)):
    mods=[]
    if isinstance(node,ast.Import): mods=[n.name for n in node.names]
    if isinstance(node,ast.ImportFrom) and node.module: mods=[node.module]
    for mod in mods:
     if mod.startswith('rawlsing_next'):
      p=mod.replace('.','/')+'.py'
      if p in paths: todo.append(p)
   # Keep package initialization exact, rather than manufacturing an empty package.
   for parent in Path(path).parents:
    p=str(parent/'__init__.py')
    if p in paths: todo.append(p)
 out={'pin':PIN,'startup':START,'stage_root':'runtime/pinned','files':dict(sorted(done.items()))}
 (HERE/'SOURCE_INPUTS.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'staged_files':len(done),'changed_since_startup':[p for p,v in done.items() if v['startup_blob']!=v['git_blob']]}))

if __name__=='__main__': stage()
