"""Two independent fresh interpreters and deterministic full native output."""
from pathlib import Path
import sys,subprocess,json,hashlib,os,time
R=Path(__file__).resolve().parents[1];O=R/'05_REAL_PYTEST_COLD_JUNIT';runs=[]
for name in ['cold_a','cold_b']:
 target=O/(name+'.json');cmd=[sys.executable,'-B',str(R/'repro/wp2.py'),str(target)];t=time.monotonic()
 p=subprocess.Popen(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);pid=p.pid;stdout,stderr=p.communicate();(O/(name+'.log')).write_text(stdout+'\n'+stderr)
 row=dict(label=name,pid=pid,argv=cmd,cwd=str(R),exit=p.returncode,seconds=time.monotonic()-t)
 if target.exists():row['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
 runs.append(row);(O/'cold_replay.json').write_text(json.dumps(dict(runs=runs),indent=2)+'\n');print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
a,b=[O/(n+'.json') for n in ['cold_a','cold_b']];assert runs[0]['pid']!=runs[1]['pid'];assert a.read_bytes()==b.read_bytes()
# Deliver one concrete complete native product and exact import manifest.
(R/'03_REAL_C1_N10E_F6_N9_N10W_CONSUMER_RECEIPTS.json').write_bytes(a.read_bytes())
(R/'02_ACTUAL_NATIVE_IMPORT_AND_GIT_SHA_MANIFEST.json').write_bytes(a.with_suffix('.imports.json').read_bytes())
(O/'cold_replay.json').write_text(json.dumps(dict(runs=runs,byte_identical=True,distinct_processes=True,implementation_sha256=hashlib.sha256((R/'repro/wp2.py').read_bytes()).hexdigest()),indent=2)+'\n')
probe=O/'owner_import_probe.json'
if probe.exists():
 manifest=json.loads((R/'02_ACTUAL_NATIVE_IMPORT_AND_GIT_SHA_MANIFEST.json').read_text());manifest['separate_owner_import_probe']=json.loads(probe.read_text());(R/'02_ACTUAL_NATIVE_IMPORT_AND_GIT_SHA_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
env=dict(os.environ,WP2_PRODUCT=str(a),PYTHONDONTWRITEBYTECODE='1')
cmd=[sys.executable,'-m','pytest','-q',str(R/'tests/test_wp2.py'),'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/'wp2_final.xml')]
p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True);(O/'wp2_final.log').write_text(p.stdout+'\n'+p.stderr);(O/'wp2_final_command.json').write_text(json.dumps(dict(argv=cmd,exit=p.returncode,product=str(a)),indent=2)+'\n');print(p.stdout,flush=True);raise SystemExit(p.returncode)
