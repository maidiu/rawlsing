"""G14 exact Git-object materialization and isolated, offline reproduction.

Run from repository root: python3 WORKER_RETURNS/SOROK-V2-HQ322-G14-G13-INDEPENDENT-COURT-R1/review_runner.py
Only writes within this return. No source/model acquisition or production edits.
"""
from pathlib import Path
import hashlib, json, os, subprocess, sys, time, uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
TARGET = '47bca2a56d34ed37186a436e7490cbaa417bfe5c'
G13 = 'WORKER_RETURNS/SOROK-R3-HQ320-G13-K11-LAB-MECHANISM-REPAIR-R1/'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def stage():
    rows = []
    mappings = [('03_POSTREPAIR_COURT/', 'reproduction/03_POSTREPAIR_COURT/'),
                ('04_G13_AUTHOR_COURT/', 'reproduction/04_G13_AUTHOR_COURT/')]
    paths = git('ls-tree','-r','--name-only',TARGET,G13).decode().splitlines()
    for src, dst in mappings:
        for p in paths:
            if not p.startswith(G13+src): continue
            tail = p[len(G13+src):]
            if tail.startswith('evidence/'): continue
            out = ROOT/dst/tail
            out.parent.mkdir(parents=True, exist_ok=True)
            b = git('show', TARGET+':'+p)
            out.write_bytes(b)
            blob = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            assert blob == git('rev-parse',TARGET+':'+p).decode().strip()
            rows.append(dict(commit=TARGET,source=p,staged=str(out.relative_to(ROOT)),blob_sha1=blob))
    # Original SGI1 needs its own exact pre-repair source closure and frozen records.
    original = ROOT/'historical/03_POSTREPAIR_COURT'
    import shutil
    shutil.copytree(ROOT/'reproduction/03_POSTREPAIR_COURT', original, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('evidence','__pycache__'))
    for p in paths:
        prefix=G13+'00_SOURCES/sgi1/'
        if not p.startswith(prefix): continue
        out=original/'sources/sgi1'/p[len(prefix):]
        out.parent.mkdir(parents=True,exist_ok=True)
        b=git('show',TARGET+':'+p);out.write_bytes(b)
        rows.append(dict(commit=TARGET,source=p,staged=str(out.relative_to(ROOT)),blob_sha1=git('rev-parse',TARGET+':'+p).decode().strip()))
    for d in [ROOT/'reproduction/03_POSTREPAIR_COURT/evidence', original/'evidence', ROOT/'execution']:
        d.mkdir(parents=True, exist_ok=True)
    dump(ROOT/'custody/staged_objects.json',rows)

def run(label, cwd, paths):
    out=ROOT/'execution'
    cmd=[sys.executable,'-B','-m','pytest','-q','-s','-p','no:cacheprovider','--tb=short',*paths,
         '--junitxml='+os.path.relpath(out/(label+'.xml'),cwd)]
    t=time.monotonic()
    proc=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'))
    # Portable logs substitute only the local checkout prefix/interpreter path.
    stdout=(proc.stdout+proc.stderr).replace(str(REPO),'$WORKTREE')
    (out/(label+'.txt')).write_text(stdout)
    junit=out/(label+'.xml')
    if junit.exists(): junit.write_text(junit.read_text().replace(str(REPO),'$WORKTREE'))
    tests=[]
    if junit.exists():
        for c in ET.parse(junit).iter('testcase'):
            status='RED' if c.find('failure') is not None else 'ERROR' if c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
            tests.append(dict(classname=c.get('classname'),name=c.get('name'),status=status))
    row=dict(suite=label,cwd=str(cwd.relative_to(ROOT)),command=['python3',*cmd[1:]],exit_status=proc.returncode,seconds=time.monotonic()-t,
             tests=tests,stdout='execution/'+label+'.txt',junit='execution/'+label+'.xml',
             portability_substitution='$WORKTREE replaces absolute checkout prefix only; python3 names selected interpreter')
    print(label,proc.returncode,{s:sum(c['status']==s for c in tests) for s in ['PASS','RED','ERROR','SKIP']},flush=True)
    return row

if __name__=='__main__':
    stage()
    court=ROOT/'reproduction/03_POSTREPAIR_COURT'
    suites=[('sgi1_target',['test_original_sgi1.py']),('g11',['sources/g11/test_g11_solver.py']),
            ('g12_controls',['test_g12_controls.py']),('g12_literal',['test_g12_literal_contract.py']),
            ('g12_supplemental',['test_g12_supplemental.py']),('candidate_boundary',['test_candidate_boundary.py'])]
    rows=[run(label,court,paths) for label,paths in suites]
    author=ROOT/'reproduction/04_G13_AUTHOR_COURT'
    for label,path in [('g13_author','test_g13_author_court.py'),('g13_postrepair','test_g13_postrepair_original.py')]:
        rows.append(run(label,author,[path]))
    rows.append(run('sgi1_historical',ROOT/'historical/03_POSTREPAIR_COURT',['test_original_sgi1.py']))
    dump(ROOT/'execution/reproduction.json',rows)
    marker=str(uuid.uuid4())
    (ROOT/'.runtime_marker').write_text(marker+'\n')
    dump(ROOT/'custody/runtime_probe.json',dict(epoch_id=marker,python=sys.version.split()[0],pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),git=git('--version').decode().strip(),marker_sha256=hashlib.sha256((marker+'\n').encode()).hexdigest()))
