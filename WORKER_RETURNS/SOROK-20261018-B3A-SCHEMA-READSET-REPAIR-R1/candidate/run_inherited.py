"""Run unchanged source courts; retain historical assertion failures as actual failures."""
from pathlib import Path
import os,json,subprocess,sys,xml.etree.ElementTree as ET
from materialize import ROOT,RUNTIME,git,dump
OUT=ROOT/'evidence/inherited'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir').decode().strip(),B2_REVIEW_ROOT=str(RUNTIME/'b2'),E2_EVIDENCE=str(OUT/'e2_sql'),R1_EVIDENCE=str(OUT/'r1_sql'),REPAIR_EVIDENCE=str(OUT/'repair_sql'),PYTHONDONTWRITEBYTECODE='1')
 for key in ('E2_EVIDENCE','R1_EVIDENCE','REPAIR_EVIDENCE'):Path(env[key]).mkdir(exist_ok=True)
 commands=json.loads((OUT/'commands.json').read_text()) if '--resume' in sys.argv and (OUT/'commands.json').exists() else []
 def run(label,args,cwd,expected):
  if any(c['label']==label and c['exit']==expected for c in commands):return
  for suffix in ('.log','.xml'):
   previous=OUT/(label+suffix)
   if previous.exists() and not (OUT/(label+'.development'+suffix)).exists():previous.rename(OUT/(label+'.development'+suffix))
  runenv=dict(env,PYTHONPATH=os.pathsep.join([str(cwd),str(Path(args[4]).parent) if len(args)>4 else str(cwd)]))
  p=subprocess.run(args,cwd=cwd,env=runenv,text=True,capture_output=True)
  (OUT/(label+'.log')).write_text(p.stdout+p.stderr)
  commands.append(dict(label=label,command=args,cwd=str(cwd),exit=p.returncode,expected=expected));dump(OUT/'commands.json',commands)
  assert p.returncode==expected,(label,p.stdout[-1500:],p.stderr[-1000:])
 def suite(label,source,cwd,expected=0,extra=()):run(label,[sys.executable,'-m','pytest','-q',str(source),*extra,'--junitxml='+str(OUT/(label+'.xml'))],cwd,expected)
 run('b2_330',[sys.executable,'run_courts.py'],RUNTIME/'b2',0)
 # Preserve B2 reference and native17 evidence, including the nonzero native exit.
 __import__('shutil').copytree(RUNTIME/'b2/evidence',OUT/'b2',dirs_exist_ok=True)
 suite('r1_45',RUNTIME/'tests_after/R1/test_identity.py',RUNTIME/'b2')
 suite('repair_5',RUNTIME/'repair/test_regression.py',RUNTIME/'b2')
 suite('e2_full',RUNTIME/'tests_after/E2/test_e2.py',RUNTIME/'b2',1)
 suite('e2_strict',RUNTIME/'tests_after/E2/test_e2.py',RUNTIME/'b2',0,('-k','legacy_after_mapping_must_fail_closed_at_b2_reentry'))
 suite('x2',RUNTIME/'tests_after/R1/frozen/test_hostile_x2.py',RUNTIME/'b2',1)
 suite('m2_41','test_m2.py',RUNTIME/'m2')
 m1=next((RUNTIME/'m1_original').rglob('test_kernel.py')).parent
 strict=next((RUNTIME/'i2_strict').rglob('test*.py'))
 # Frozen tests load kernel using local import; target M2 by explicit PYTHONPATH.
 env['PYTHONPATH']=str(RUNTIME/'m2')
 # Running original test dir otherwise shadows kernel with original; use --import-mode=importlib.
 suite('m1_37_on_m2',m1/'test_kernel.py',RUNTIME/'m2',1,('--import-mode=importlib',))
 suite('i2_23_on_m2',strict,RUNTIME/'m2',1,('--import-mode=importlib',))
 suite('m3_source_preimage_3_red',RUNTIME/'m3/05_SOURCE_PREIMAGE_RED_REPRODUCER.py',RUNTIME/'m2',1,('--import-mode=importlib',))
 __import__('shutil').copyfile(RUNTIME/'b2/execution_receipt.json',OUT/'b2_execution_receipt.json')
 summary={}
 for p in OUT.glob('*.xml'):
  suites=ET.parse(p).getroot();summary[p.stem]=[{k:s.get(k) for k in ('tests','failures','errors','skipped')} for s in suites.iter('testsuite')]
 dump(OUT/'summary.json',summary)
 print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
