"""Fresh MS3 reconstruction from pinned shared-store objects; never old live files."""
from pathlib import Path
import subprocess,sys,json,hashlib,uuid,datetime,os
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
SHA='34b96ea98de181ca5264f0eed3824cad2db7cfc0';PREFIX='WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=ROOT)
def run():
    assert not (R/'staging').exists(),'Preserve existing staged runtime; do not overwrite it'
    rows=[]
    for path in git('ls-tree','-r','--full-tree','--name-only',SHA,PREFIX).decode().splitlines():
        b=git('show',SHA+':'+path);h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert h==git('rev-parse',SHA+':'+path).decode().strip()
        dest=R/'staging/ms2'/path[len(PREFIX)+1:];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
        rows.append(dict(commit=SHA,path=path,blob_sha1=h,sha256=hashlib.sha256(b).hexdigest(),local=str(dest.relative_to(R))))
    (R/'01_SOURCE_PACKET_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
    subprocess.run([sys.executable,str(R/'staging/ms2/repro/stage.py')],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
    (R/'staging/runtime_marker.json').write_text(json.dumps(dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),owner='MS3_AUTHOR_NOT_MS4',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source='FRESH_PINNED_GIT_RECONSTRUCTION'),indent=2)+'\n')
    print('MS3_FRESH_PINNED_SOURCE_READY; baseline candidate not installed')
if __name__=='__main__':run()
