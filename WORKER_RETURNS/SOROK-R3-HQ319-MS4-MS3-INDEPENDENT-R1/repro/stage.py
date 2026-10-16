"""MS4 fresh source reconstruction, exact Git bytes; no prior live runtime reuse."""
from pathlib import Path
import subprocess, hashlib, json, sys, os
R=Path(__file__).resolve().parents[1]
TARGET='48200cf0b8e9b69ce27bf0151cb43fde5133322f'
PREFIX='WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1'
def git(*a): return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=R)
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if __name__=='__main__':
    out=R/'staging/ms3'; assert not out.exists()
    rows=[]
    for path in git('ls-tree','-r','--full-tree','--name-only',TARGET,PREFIX).decode().splitlines():
        b=git('show',TARGET+':'+path); h=git('rev-parse',TARGET+':'+path).decode().strip(); assert blob(b)==h
        p=out/path[len(PREFIX)+1:]; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
        rows.append(dict(commit=TARGET,path=path,blob_sha1=h,sha256=hashlib.sha256(b).hexdigest(),local=str(p.relative_to(R))))
    (R/'01_SOURCE_PACKET_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
    subprocess.run([sys.executable,str(out/'repro/stage.py')],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
    print('MS4 exact target packet staged',len(rows))
