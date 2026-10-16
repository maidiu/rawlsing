"""Reconstruct pinned source only under this review's ignored runtime."""
from pathlib import Path
import subprocess, hashlib, json, os, sys
R = Path(__file__).resolve().parents[1]
ROOT = R.parents[1]
SHA = '8b7f3ed2ad095eee060fd040dcab88e59d4ca255'
PREFIX = 'WORKER_RETURNS/SOROK-R3-HQ315-M05-M04-PROVENANCE-ANCESTRY-REPAIR-R1'
def blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def materialize():
    assert not (R/'runtime').exists(), 'Preserve an existing runtime; do not overwrite it'
    rows=[]
    for path in subprocess.check_output(['git','ls-tree','-r','--full-tree','--name-only',SHA,PREFIX],cwd=ROOT,text=True).splitlines():
        rel=path[len(PREFIX)+1:]
        if rel.startswith('evidence/'): continue
        data=subprocess.check_output(['git','show',SHA+':'+path],cwd=ROOT)
        expected=subprocess.check_output(['git','rev-parse',SHA+':'+path],cwd=ROOT,text=True).strip()
        assert blob(data)==expected
        target=R/'runtime/m05'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        rows.append(dict(commit=SHA,path=path,blob_sha1=expected,sha256=hashlib.sha256(data).hexdigest(),local=str(target.relative_to(R))))
    (R/'01_STAGING_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
    m=R/'runtime/m05';(m/'evidence').mkdir(exist_ok=True)
    for script in ['review/stage.py','repro/install_candidate.py']:
        subprocess.run([sys.executable,str(m/script)],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
if __name__=='__main__': materialize()
