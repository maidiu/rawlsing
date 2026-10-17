"""Fresh C0I reconstruction from exact Git objects; no previous live files."""
from pathlib import Path
import subprocess,hashlib,json,os,sys
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
TARGET='154a4dd5615d47f014ca90eb1234b16e983bf5c1';PREFIX='WORKER_RETURNS/SOROK-R3-HQ319-C0P-GENERIC-PORT-POSITIVE-R1'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=ROOT)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if __name__=='__main__':
    out=R/'staging/c0p';assert not out.exists()
    rows=[]
    for path in git('ls-tree','-r','--full-tree','--name-only',TARGET,PREFIX).decode().splitlines():
        b=git('show',TARGET+':'+path);h=git('rev-parse',TARGET+':'+path).decode().strip();assert blob(b)==h
        p=out/path[len(PREFIX)+1:];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        rows.append(dict(commit=TARGET,path=path,blob_sha1=h,sha256=hashlib.sha256(b).hexdigest(),local=str(p.relative_to(R))))
    (R/'01_TARGET_PACKET_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
    env=dict(os.environ,C0P_REPO=str(ROOT),C0P_RUNTIME=str(R/'staging/runtime'),C0P_STAGE=str(R/'staging/oracles'),PYTHONDONTWRITEBYTECODE='1')
    for name in ['c0p_stage.py','c0p_stage_runtime.py']:
        p=subprocess.run([sys.executable,str(out/'repro'/name)],cwd=R,env=env,capture_output=True,text=True)
        dest=R/'evidence/bootstrap';dest.mkdir(parents=True,exist_ok=True);(dest/(name+'.stdout.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,(name,p.returncode)
    print('C0I fresh target and exact closure staged',len(rows))
