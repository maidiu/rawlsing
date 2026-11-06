import hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-cold-702')
EVID=Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/r01-receive-evidence')
f=ROOT/'rawlsing_next/pre553_universal_world_binding.py'
before=f.read_text(); old='''    if request.temporal_pair_ref is not None:
        snapshots["T1"] = catalog.select('''; new='''    if False:
        snapshots["T1"] = catalog.select('''
assert before.count(old)==1, before.count(old)
sha=hashlib.sha256(before.encode()).hexdigest()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
env['PYTHONPATH']=str(EVID/'pydeps')+os.pathsep+env.get('PYTHONPATH','')
try:
    f.write_text(before.replace(old,new,1))
    p=subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--tb=long',
      'rawlsing_next/tests/test_universal_world_binding.py::test_r06r2_actual_r05_learned_to_p41_world_with_synthetic_pair'],
      cwd=ROOT,env=env,text=True,capture_output=True,timeout=1200)
finally:
    f.write_text(before)
restored=hashlib.sha256(f.read_text().encode()).hexdigest()==sha
out=p.stdout+p.stderr
lines=[l for l in out.splitlines() if l.startswith('E   ') or l.startswith('>') or 'assert' in l or 'reason_code' in l][-15:]
rec={'mutation':'T1 snapshot not constructed under temporal pair','returncode':p.returncode,'source_restored':restored,'failure_lines':lines,'tail':out.splitlines()[-20:]}
print(json.dumps(rec,indent=2))
(EVID/'p41-nonconsumption-probe.json').write_text(json.dumps(rec,indent=2)+'\n')
