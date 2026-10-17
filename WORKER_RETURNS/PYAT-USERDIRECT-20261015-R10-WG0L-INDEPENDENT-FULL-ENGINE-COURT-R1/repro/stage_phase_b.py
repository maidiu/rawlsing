"""Exact published candidate in a separate reviewer staging closure."""
from pathlib import Path
import json,hashlib,subprocess,shutil,datetime
R=Path(__file__).resolve().parents[1];WT=R.parents[1]
SHA='20d781c8502662bf788b60b828e46df55898d687'
START='c1e88fb26f3ef757f13bad7cf901cd6529a368c8'
P='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R9-WG0P4-EXACT-FRONTIER-COLD-REPAIR-R1'
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(WT),*a])
def main():
    remote=git('ls-remote','https://github.com/maidiu/rawlsing.git','refs/heads/agent/userdirect-pyat-20261015-r9-wg0p4-frontier-fact-receipt-repair-r1').decode().split()[0]
    assert remote==SHA
    changed=git('diff','--name-only',START,SHA).decode().splitlines();assert all(p.startswith(P+'/') for p in changed)
    for row in json.loads((R/'observations/PRECOMMITTED_TEST_ROOT.json').read_text())['files']:
        assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
    rt=R/'runtime_phase_b';assert not rt.exists(),'Preserve existing phase B closure'
    dest=rt/'candidate';rows=[]
    for line in git('ls-tree','-r',SHA,P).decode().splitlines():
        meta,path=line.split('\t');blob=meta.split()[2];rel=path[len(P)+1:]
        if rel.startswith('observations/'):continue
        b=git('cat-file','blob',blob)
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
        out=dest/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
        rows.append(dict(commit=SHA,path=path,git_blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),staged_path=str(out.relative_to(R))))
    (dest/'observations').mkdir(exist_ok=True)
    (R/'observations/phase_b').mkdir(exist_ok=True)
    cut=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sha=SHA,candidate_direct_remote_sha=remote,
             candidate_startup=START,changed_paths=changed,return_only=True,reviewer_precommit='aa4e361e9fbed79c395cb986c51798354bb3d6cd',
             oracle_sha256=hashlib.sha256((R/'01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json').read_bytes()).hexdigest(),
             source_import_not_yet_executed=True,source_rows=rows)
    (R/'observations/phase_b/candidate_read_cut.json').write_text(json.dumps(cut,indent=2)+'\n')
    print(json.dumps({'candidate_sha':SHA,'verified_staged_files':len(rows),'return_only':True}))
if __name__=='__main__':main()
