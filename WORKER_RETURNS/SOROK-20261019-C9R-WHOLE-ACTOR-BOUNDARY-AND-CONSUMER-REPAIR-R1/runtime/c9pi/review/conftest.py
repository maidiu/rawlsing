import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PREFIX='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
sys.path[:0]=[str(ROOT),str(ROOT/PREFIX)]
def pytest_sessionfinish(session,exitstatus):
 out=os.environ.get('C9PI_IMPORT_RECEIPT')
 if out:
  rows=[]
  for name,mod in sorted(sys.modules.items()):
   if name=='candidate' or name.startswith(('candidate.','rawlsing_next.')):
    p=Path(mod.__file__);b=p.read_bytes()
    rows.append(dict(module=name,file=str(p),sha256=hashlib.sha256(b).hexdigest(),blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
  Path(out).write_text(json.dumps(rows,indent=2)+'\n')
