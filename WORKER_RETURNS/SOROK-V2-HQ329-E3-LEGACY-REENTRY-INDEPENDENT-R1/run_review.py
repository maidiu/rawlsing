"""E3 exact-object court; candidate and frozen oracle bytes are never edited."""
from pathlib import Path
import subprocess, sys, os, json, hashlib, importlib.util, shutil, uuid, platform, sqlite3, time
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent.parent
RUNTIME=ROOT/'.runtime'
OUT=ROOT/'evidence'
FIX='8f7966d6d0bbb1ea2e57359de9defbcf552268bd'
OLD='358fd1086eac0a4aa7791ca14abc25c45b935ddd'
E2='8983315b3aee130e9446d43bd983c4a91c6f0437'
B2='WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1'
PINS=[(E2,'SOROK-V2-HQ328-E2-R1-INDEPENDENT-CUSTODY-R1','tests_after/E2'),(OLD,'SOROK-V2-HQ327-R1-EVENT-IDENTITY-REPAIR-R1','tests_after/R1'),(FIX,'SOROK-V2-USERDIRECT-B2-LEGACY-REENTRY-REPAIR-R1','repair')]
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def portable(s):
 import re
 s=s.replace(str(ROOT),'<E3>').replace(str(REPO),'<WORKTREE>').replace(str(Path.home()),'<HOME>')
 return re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
def main():
 OUT.mkdir(exist_ok=True);RUNTIME.mkdir(exist_ok=True)
 marker=uuid.uuid4().hex;(RUNTIME/'marker').write_text(marker)
 frozen=[]
 for sha,folder,dest in PINS:
  prefix='WORKER_RETURNS/'+folder
  for p in git('ls-tree','-r','--name-only',sha,prefix).decode().splitlines():
   if not p.endswith('.py'):continue
   target=RUNTIME/dest/Path(p).relative_to(prefix);target.parent.mkdir(parents=True,exist_ok=True)
   data=git('show',sha+':'+p);target.write_bytes(data)
   frozen.append(dict(commit=sha,path=p,git_blob_sha1=git('rev-parse',sha+':'+p).decode().strip(),sha256=digest(data),staged=str(target.relative_to(ROOT))))
 dump(OUT/'frozen_manifest.json',frozen)
 spec=importlib.util.spec_from_file_location('frozen_materializer',RUNTIME/'tests_after/E2/run_e2.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 h.ROOT=ROOT;h.REPO=REPO;h.STAGE=RUNTIME;h.EVIDENCE=OUT
 commands=[];summary={}
 env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),PYTHONDONTWRITEBYTECODE='1')
 def run(args,cwd,label,expected,extra=None):
  t=time.monotonic();p=subprocess.run([str(a) for a in args],cwd=cwd,env=dict(env,**(extra or {})),text=True,capture_output=True)
  (OUT/(label+'.log')).write_text(portable(p.stdout+p.stderr))
  commands.append(dict(command=[portable(str(a)) for a in args],cwd=portable(str(cwd)),label=label,exit=p.returncode,expected_exit=expected,seconds=time.monotonic()-t))
  dump(OUT/'commands.json',commands)
  assert p.returncode==expected,(label,p.returncode,p.stdout[-1800:],p.stderr[-1800:])
 def test(path,name,expected=0,extra=()):
  run([sys.executable,'-m','pytest','-q',path,*extra,'--junitxml='+str(phaseout/(name+'.xml'))],stage,phase+'/'+name,expected,variables)
  suite=ET.parse(phaseout/(name+'.xml')).find('testsuite');summary[phase+'/'+name]=dict({k:v for k,v in suite.attrib.items() if k!='hostname'},failed=[c.get('name') for c in suite.findall('testcase') if c.find('failure') is not None])
 for phase in ('old','fixed'):
  phaseout=OUT/phase;phaseout.mkdir(exist_ok=True)
  stage,manifest=h.materialize(phase)
  sha=OLD if phase=='old' else FIX;data=git('show',sha+':'+B2+'/bridge.py');(stage/'bridge.py').write_bytes(data)
  # h stages original B2; identify the actual bridge replacement explicitly.
  manifest=[x for x in manifest if x['source_path']!=B2+'/bridge.py'] if all('source_path' in x for x in manifest) else [x for x in manifest if not x['staged_path'].endswith('/bridge.py')]
  manifest.append(dict(commit=sha,source_path=B2+'/bridge.py',git_blob_sha1=git('rev-parse',sha+':'+B2+'/bridge.py').decode().strip(),sha256=digest(data),staged_path=str((stage/'bridge.py').relative_to(ROOT))))
  dump(phaseout/'source_manifest.json',manifest)
  variables=dict(B2_REVIEW_ROOT=str(stage),E2_EVIDENCE=str(phaseout/'sql'),R1_EVIDENCE=str(phaseout/'r1_sql'),REPAIR_EVIDENCE=str(phaseout/'repair_sql'),E3_EVIDENCE=str(phaseout/'e3_sql'))
  for k,v in variables.items():
   if k.endswith('EVIDENCE'):Path(v).mkdir(exist_ok=True)
  test(RUNTIME/'tests_after/E2/test_e2.py','strict',1 if phase=='old' else 0,('-k','legacy_after_mapping_must_fail_closed_at_b2_reentry'))
  run([sys.executable,'run_courts.py'],stage,phase+'/inherited',0)
  shutil.copytree(stage/'evidence',phaseout/'inherited',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.sqlite','*.sqlite-*'))
  shutil.copyfile(stage/'execution_receipt.json',phaseout/'execution_receipt.json')
  if phase=='fixed':
   # Frozen repair control uses this specific sibling path for its process helper.
   test(RUNTIME/'tests_after/R1/test_identity.py','r1')
   test(RUNTIME/'tests_after/E2/test_e2.py','e2_full',1)
   assert summary['fixed/e2_full']['failed']==['test_direct_b1_after_wrapper_limit_is_measured[False]','test_direct_b1_after_wrapper_limit_is_measured[True]']
   test(RUNTIME/'tests_after/R1/frozen/test_hostile_x2.py','x2',1)
   assert summary['fixed/x2']['failed']==['test_same_event_id_accepts_distinct_objective_payload_hashes']
   test(RUNTIME/'repair/test_regression.py','repair5')
   test(ROOT/'test_independent.py','independent')
  run([sys.executable,str(RUNTIME/'tests_after/E2/runtime_probe.py'),str(phaseout/'loaded_modules.json')],stage,phase+'/loaded_modules',0,variables)
  for row in manifest:
   if '/evidence/' in row['staged_path'] or row['staged_path'].endswith('execution_receipt.json'):continue
   assert digest((ROOT/row['staged_path']).read_bytes())==row['sha256'],row
  print(phase+' completed',flush=True)
 for row in frozen:assert digest((ROOT/row['staged']).read_bytes())==row['sha256']
 dump(OUT/'summary.json',summary)
 dump(ROOT/'environment_passport_delta.json',dict(passport_schema='R1',environment_id=digest(marker.encode())[:16],epoch_id=uuid.uuid4().hex,owner_session_alias='E3-independent',surface='LOCAL_SHARED_STORE',machine_alias='oldMac-user-reported',status='LIVE_VERIFIED',runtime_marker_digest=digest(marker.encode()),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),sqlite=sqlite3.sqlite_version,node=subprocess.check_output(['node','--version'],text=True).strip(),git=subprocess.check_output(['git','--version'],text=True).strip(),git_object_store_alias='existing-shared-store',worktree_alias='E3-review',branch=git('branch','--show-current').decode().strip(),checkout_base=git('rev-parse','HEAD').decode().strip(),materialized_source_refs='evidence/{old,fixed}/source_manifest.json',covered_test_suites='evidence/commands.json',dependency_closure_status='BOUNDED',science_grade='sourcefree prototype',model_provider='OpenAI Codex',model_effort='user requested GPT-6 Medium; runtime selection not independently inspectable',cash_known=None,quota_known=None,independence='No candidate authorship in this review',privacy_source_grant='Commission synthetic fixtures only',staged_state_preservation='local .runtime ignored; recheck marker on resume',assignments_completed=['E3'],next_good_affinity_tags=['OCCURRENCE','SQLITE_CUSTODY']))
 for p in OUT.rglob('*'):
  if p.is_file() and p.suffix in ('.json','.log','.xml'):
   if p.suffix=='.xml':
    tree=ET.parse(p)
    for node in tree.iter():
     node.attrib.pop('hostname',None)
     for k,v in node.attrib.items():node.set(k,portable(v))
     if node.text:node.text=portable(node.text)
     if node.tail:node.tail=portable(node.tail)
    tree.write(p,encoding='utf-8',xml_declaration=True)
    continue
   p.write_text(portable(p.read_text()))
 print('E3 executable review complete',flush=True)
if __name__=='__main__':main()
