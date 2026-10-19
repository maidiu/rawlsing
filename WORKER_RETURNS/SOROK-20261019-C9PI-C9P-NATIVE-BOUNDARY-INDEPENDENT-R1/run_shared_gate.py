from pathlib import Path
import os,subprocess,sys
R=Path(__file__).resolve().parent;ROOT=R/'runs/runtime';P=ROOT/'WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
for name,contract in [('author_severance',P/'tests/test_severance_witnesses.py.proof.json'),('author_consumer',P/'tests/test_later_action_consumer.py.proof.json'),('reviewer',ROOT/'review/test_edges.py.proof.json')]:
 p=subprocess.run([sys.executable,str(R/'proof_integrity_gate_r1.py'),'witness',str(contract),'--root',str(ROOT),'--receipt',str(R/'evidence'/('shared_'+name+'.json'))],cwd=ROOT,env=dict(os.environ,TMPDIR=str(R/'runs/tmp'),PYTHONDONTWRITEBYTECODE='1'),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/'evidence'/('shared_'+name+'.log')).write_text(p.stdout)
 print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
