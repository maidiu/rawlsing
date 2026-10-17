from pathlib import Path
import subprocess,hashlib,json
R=Path(__file__).resolve().parents[1];REPO=R.parents[1];records=[]
def stage(ref,src,dst):
 b=subprocess.check_output(['git','show',f'{ref}:{src}'],cwd=REPO);p=R/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 records.append(dict(commit=ref,source=src,path=dst,blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
f='5ed8e5389dd3510cf29a4947b04bd05901c8d213';prefix='WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/'
for p in ['inherited/F6C/02_TESTS/f6c_worlds.py','inherited/F6L/02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json','inherited/F6L/02_PHASE_A/03_SCRIPTS/f6l_worlds.py','inherited/F6C/02_TESTS/run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py']:
 stage(f,prefix+p,'inherited/F6M/'+p)
pe='b94f0f9813dda34c4707e5e13b38d24e92b4d8f8';prefix='WORKER_RETURNS/PYAT-R3-PE-GENERIC-WORLD-POSSIBILITY-R1/probe/'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',pe,prefix],cwd=REPO).decode().splitlines()
for p in paths:
 if p.endswith('.py'):stage(pe,p,'inherited/PE2/probe/'+p[len(prefix):])
# Recover J04's missing actual producer; no use of its real-item grant.
stage('8fc2a8d859a67fff81ff829c8acc2729064a12f7','rawlsing_next/prev3_objective_position_materializer.py','native/rawlsing_next/prev3_objective_position_materializer.py')
# Actual F7 owner resides in data/ddm_build_copy, not the PRE553 package.
for p in ['data/ddm_build_copy/ddm_v553_temporal_pressure.py','data/ddm_build_copy/ddm_v553_temporal_identity.py','data/ddm_build_copy/compile_v553_temporal_pressure_field.py']:
 stage('7b2eaf6cb',p,'temporal/'+p.rsplit('/',1)[1])
(R/'discovery/supplement_manifest.json').write_text(json.dumps(records,indent=2)+'\n')
print(len(records),'supplemental exact owners/fixtures')
