"""Pinned source-free reconstruction, writes only within this return."""
from pathlib import Path
import subprocess, hashlib, json, sys
R=Path(__file__).resolve().parents[1]
CAN3='ef12349defe22a50e053a7a8080a67ab45673417'
BASE='WORKER_RETURNS/SOROK-R3-HQ309-CAN3-CAN008-INDEPENDENT-R1'
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
rows=[]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',CAN3,BASE],text=True).splitlines():
 b=subprocess.check_output(['git','show',CAN3+':'+p]); h=subprocess.check_output(['git','rev-parse',CAN3+':'+p],text=True).strip(); assert blob(b)==h
 d=R/'runtime/can3'/p[len(BASE)+1:];d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
 rows.append(dict(commit=CAN3,path=p,blob_sha1=h,sha256=hashlib.sha256(b).hexdigest(),local=str(d.relative_to(R))))
subprocess.run([sys.executable,str(R/'runtime/can3/repro/stage.py')],check=True)
rows+=json.loads((R/'runtime/can3/01_SOURCE_RECEIPTS.json').read_text())
(R/'02_SOURCE_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
print('CAN3 published evidence preserved byte-exact; pinned closure reconstructed')
