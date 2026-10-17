import subprocess,json,hashlib,ast
from pathlib import Path
R=Path(__file__).resolve().parents[1];REPO=R.parents[1];out=[]
def get(ref,path):return subprocess.check_output(['git','show',ref+':'+path],cwd=REPO)
def save(ref,src,dst):
 b=get(ref,src);p=R/dst;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);out.append(dict(commit=ref,source=src,path=dst,blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()));return b
for src in ['WORKER_RETURNS/PYAT-R3-HQ297-K9K10-EXECUTION-RECOVERY-R1/06_MINIMUM_VALUE_BEARING_N9_PROVIDER_PROPOSAL.md','WORKER_RETURNS/PYAT-R3-HQ297-K9K10-SC0-PE-INDEPENDENT-R1/04_PYAT_SOROK_PORT_CROSS_OWNER_DELTA.md','rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py']:
 save('e61a26ce24f023a53d6b116bb9eca2fb7b6f8e65',src,'readonly_shapes/'+src.rsplit('/',1)[1])
for src in ['WORKER_RETURNS/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1/repro/stage.py','WORKER_RETURNS/SOROK-R3-HQ320-C0I-C0P-INDEPENDENT-R1/repro/test_c0i.py']:
 save('2dacd87636352a6c805e03b3d07581193a06264b',src,'readonly_shapes/c0i_'+src.rsplit('/',1)[1])
# Inspectable complete internal import closure for F7. No compiler execution or data reads.
ref='7b2eaf6cb';ref=subprocess.check_output(['git','rev-parse',ref],cwd=REPO).decode().strip()
queue=['data/ddm_build_copy/ddm_v553_temporal_pressure.py'];done=set()
while queue:
 src=queue.pop()
 if src in done:continue
 done.add(src);b=save(ref,src,'temporal/closure/'+src)
 for n in ast.walk(ast.parse(b)):
  if isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('data.ddm_build_copy.'):
   dep=n.module.replace('.','/')+'.py'
   if dep not in done:queue.append(dep)
(R/'discovery/readonly_and_temporal_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(out),'read-only source/shape objects')
