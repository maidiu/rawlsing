"""Portable full reproduction. The default actually reruns every inherited court."""
from pathlib import Path
import json,subprocess,sys
from materialize import ROOT,dump

def main():
 (ROOT/'evidence').mkdir(exist_ok=True);commands=[]
 def run(label,args,expected=0):
  p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
  (ROOT/'evidence'/(label+'.log')).write_text(p.stdout+p.stderr)
  commands.append(dict(label=label,command=args,exit_code=p.returncode,expected_exit=expected))
  dump(ROOT/'evidence/run_commands.json',commands)
  assert p.returncode==expected,(label,p.stdout[-1200:],p.stderr[-1200:])
 run('materialize',[sys.executable,'materialize.py'])
 run('inherited',[sys.executable,'run_inherited.py']+(['--resume'] if '--reuse-inherited' in sys.argv else []))
 run('b3_final',[sys.executable,'-m','pytest','-q','test_integration_b3.py','--junitxml=evidence/b3_final.xml'])
 run('f2_run',[sys.executable,'run_f2.py'])
 run('b3_mutation',[sys.executable,'mutation_audit_b3.py'])
 run('loop_execution',[sys.executable,'developmental_loop.py','evidence/loop'])
 for label in ('positive','permission_absent'):
  db=ROOT/'evidence/loop'/(label+'_cold.sqlite')
  if db.exists():db.unlink()
  run(label+'_cold',[sys.executable,'developmental_loop.py','replay','evidence/loop/'+label+'.json',str(db)])
  live=json.loads((ROOT/'evidence/loop'/(label+'.json')).read_text())
  cold=json.loads((ROOT/'evidence'/(label+'_cold.log')).read_text())
  assert cold['receipts']==[e['receipt'] for e in live['episodes']]
  assert cold['snapshot_hash']==live['snapshot_hash']
 subprocess.run([sys.executable,'finalize.py'],cwd=ROOT,check=True)
 # Finalizer records its own command via this durable driver manifest.
 print('Completed sourcefree B3 reproduction; preserved native and historical REDs.')
if __name__=='__main__':main()
