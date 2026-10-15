"""Exact immutable historical courts, isolated originals and repaired overlays."""
from pathlib import Path
import shutil,sys,json,hashlib,subprocess
RET=Path(__file__).resolve().parents[1]
# Native source/test oracles are rehydrated from exact Git objects, never copied
# into another worker's tracked terrain. Old ignored states are not assumed live.
for row in json.loads((RET/'lineage/00_ORIGINAL_SOURCE_MANIFEST.json').read_text()):
    destination=RET/'runtime_root/original'/Path(row['local']).relative_to('runtime_root/source')
    destination.parent.mkdir(parents=True,exist_ok=True)
    raw=subprocess.check_output(['git','show',row['commit']+':'+row['path']])
    assert hashlib.sha256(raw).hexdigest()==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['blob_sha1']
    destination.write_bytes(raw)
for name,blob in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
    destination=RET/'runtime_root/law'/(name+'.txt');destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_bytes(subprocess.check_output(['git','cat-file','blob',blob]))
for label in ('original','repaired'):
    court=RET/'runtime_root'/('court_'+label)
    source=court/'runtime_root/source'
    shutil.copytree(RET/'runtime_root/original',source,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
    (court/'repro').mkdir(parents=True,exist_ok=True)
    for n in ('run_suite.py','causal_probe.py','test_independent.py'):
        shutil.copyfile(RET/'inherited/repro'/n,court/'repro'/n)
    shutil.copyfile(RET/'00_INHERITED_FROZEN_PREREG.json',court/'00_INHERITED_FROZEN_PREREG.json')
    shutil.copytree(RET/'runtime_root/law',court/'runtime_root/law',dirs_exist_ok=True)
    if label=='repaired':
        candidate=source/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1/candidate'
        for f in (RET/'candidate').glob('*.py'):shutil.copyfile(f,candidate/f.name)
    for n in ('test_independent.py','causal_probe.py'):
        assert (court/'repro'/n).read_bytes()==(RET/'inherited/repro'/n).read_bytes()
print('Original64 closure and repaired overlay ready; all historical test bytes unchanged')
