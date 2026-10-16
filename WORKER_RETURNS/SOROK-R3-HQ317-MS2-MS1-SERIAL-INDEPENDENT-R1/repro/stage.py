"""Authenticated reconstruction of MS1's complete34-file packet, no substitutions."""
from pathlib import Path
import subprocess, hashlib, json
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
SOURCE='d40cc32ecec8f681dcced6a482b6438a86080899'
PREFIX='WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=ROOT)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def verify():
    rows=json.loads((R/'01_SOURCE_PACKET_IDENTITIES.json').read_text())
    for row in rows:
        b=(R/row['local']).read_bytes();assert b==git('show',row['commit']+':'+row['path'])
        assert blob(b)==row['blob_sha1']
    native=[]
    for row in json.loads((R/'staging/ms1/evidence/native_source_ledger.json').read_text()):
        b=(R/'staging/ms1'/row['local']).read_bytes();assert b==git('show',row['commit']+':'+row['authoritative_path'])
        assert blob(b)==row['git_blob_sha1'];native.append(row)
    assert len(native)==10 # nine CAN2 files plus one separate EMPTY guard
    law=R/'staging/accepted_law';law.mkdir(exist_ok=True)
    pins={'CAN008_R2':'b80dd6925066510ecbbfec7b427bf9f688475663','ADP016':'c6619a286e115d060ab4830889e7fc23762167a5','ADP017':'eece4f3f2f3f9288ab9bbc645dc81e20a99e1280'}
    for name,h in pins.items():
        b=git('cat-file','blob',h);assert blob(b)==h;(law/(name+'.txt')).write_bytes(b)
    (R/'evidence/NATIVE_BLOB_VERIFICATION.json').write_text(json.dumps(dict(native_CAN2=9,production_guard=1,total_verified=10,files=native,accepted_law_blobs=pins,law_maps_not_inserted_into_original_runtime=True),indent=2)+'\n')
    print('MS1_PACKET34_NATIVE9_GUARD1_VERIFIED')
def materialize():
    assert not (R/'staging').exists(),'Preserve an existing staged runtime; do not overwrite it'
    rows=[]
    for path in git('ls-tree','-r','--full-tree','--name-only',SOURCE,PREFIX).decode().splitlines():
        rel=path[len(PREFIX)+1:];b=git('show',SOURCE+':'+path);h=git('rev-parse',SOURCE+':'+path).decode().strip();assert blob(b)==h
        p=R/'staging/ms1'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        rows.append(dict(commit=SOURCE,path=path,blob_sha1=h,sha256=hashlib.sha256(b).hexdigest(),local=str(p.relative_to(R))))
    (R/'01_SOURCE_PACKET_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n');verify()
if __name__=='__main__':
    import sys
    verify() if sys.argv[1:]==['verify'] else materialize()
