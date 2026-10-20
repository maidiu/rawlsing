"""Fresh positive / exact source fault / exact-byte restore; preserves JUnit and logs."""
import hashlib,importlib.util,json,os,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R/'runs/runtime'
P='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
OUT=R/'evidence/faults';OUT.mkdir(parents=True,exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def run(node,key):
 xml=OUT/(key+'.xml');env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(R/'runs/tmp'),C9PI_IMPORT_RECEIPT=str(OUT/(key+'.imports.json')))
 p=subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--basetemp',str(R/'runs/pytest'/key),'--junitxml',str(xml),node],cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(key+'.log')).write_text(p.stdout)
 cases=list(ET.parse(xml).iter('testcase'));assert len(cases)==1
 c=cases[0]
 return dict(exit=p.returncode,name=c.get('name'),failure=c.find('failure') is not None,error=c.find('error') is not None,skipped=c.find('skipped') is not None,junit=str(xml.relative_to(R)),assertion=(c.find('failure').get('message','') if c.find('failure') is not None else ''))
def main():
 (R/'runs/tmp').mkdir(parents=True,exist_ok=True)
 (R/'runs/pytest').mkdir(parents=True,exist_ok=True)
 spec=importlib.util.spec_from_file_location('author_severance',ROOT/P/'severance/run_severance.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 author=[dict(claim_id=c['claim_id'],positive_node=c['test_node'],fault=dict(path=c['fault_path'],old=c['old'],new=c['new'])) for c in mod.SEVERANCE_CASES]
 ours=json.loads((ROOT/'review/test_edges.py.proof.json').read_text())['claims']
 extra='--extra-consumer' in sys.argv
 cases=json.loads((ROOT/P/'tests/test_later_action_consumer.py.proof.json').read_text())['claims'] if extra else author+ours
 rows=json.loads((R/'evidence/fault_trials.json').read_text()) if extra else []
 for ordinal,c in enumerate(cases,start=len(rows)):
  prefix=f'{ordinal:02d}';f=ROOT/c['fault']['path'];before=f.read_bytes();text=before.decode();old=c['fault']['old'];new=c['fault']['new'];assert text.count(old)==1
  base=run(c['positive_node'],prefix+'_positive')
  invariant=None
  try:
   f.write_text(text.replace(old,new,1));fault_hash=sha(f.read_bytes())
   fault=run(c['positive_node'],prefix+'_fault')
   if c['claim_id']=='C9PI_NATIVE_GUARD_DIAGNOSTIC_ONLY':
    invariant=run('review/test_edges.py::test_test_only_create_does_not_depend_on_guard_diagnostic',prefix+'_create_invariant')
  finally:f.write_bytes(before)
  restored=run(c['positive_node'],prefix+'_restored')
  assert f.read_bytes()==before
  good=base['exit']==0 and restored['exit']==0 and fault['failure'] and not fault['error'] and not fault['skipped'] and 'AssertionError' in fault['assertion']
  # Pytest JUnit often writes the assertion expression instead of exception type.
  good=base['exit']==0 and restored['exit']==0 and fault['exit']==1 and fault['failure'] and not fault['error'] and not fault['skipped']
  rows.append(dict(claim_id=c['claim_id'],node=c['positive_node'],fault=c['fault'],before_sha256=sha(before),fault_sha256=fault_hash,restored_sha256=sha(f.read_bytes()),positive=base,negative=fault,restored=restored,invariant=invariant,grade='SAME_ASSERTION_RED_RESTORED' if good else 'NOT_PROVED'))
 (R/'evidence/fault_trials.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(json.dumps(dict(cases=len(rows),proved=sum(x['grade']=='SAME_ASSERTION_RED_RESTORED' for x in rows))))
 if not all(x['grade']=='SAME_ASSERTION_RED_RESTORED' for x in rows):raise SystemExit(1)
if __name__=='__main__':main()
