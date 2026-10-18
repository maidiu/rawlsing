"""Read-only verification; preserves compatibility and residual failed assertions."""
from pathlib import Path
import hashlib,json,subprocess,tarfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads((ROOT/p).read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
m=load('input_package/manifest.json')
with tarfile.open(ROOT/'m2_patch/frozen_inputs/M1_original_exact_7e91c198.tar.gz') as archive:
    original_m1=next(archive.extractfile(x).read() for x in archive.getmembers() if x.name=='kernel.py')
for name in ('kernel.py','test_m2.py','test_m3_independent.py','test_m3_unresolved.py','test_source_preimages.py','frozen_inputs/M1_original_exact_7e91c198.tar.gz','frozen_inputs/I2_strict_exact_19f1e86a.tar.gz'):
    p=ROOT/'m2_patch'/name;r=m['files']['m2_patch/'+name]
    assert p.stat().st_size==r['bytes'] and sha(p.read_bytes())==r['sha256'],name
assert sha((ROOT/'m2_patch/kernel.py').read_bytes())=='56388b0c1ef71c1b77886932ca473d12bc3ff9232f630371858809e1289eeb0c'
for row in load('source_refs.json'):
    original=git('show',row['commit']+':'+row['path'])
    assert sha(original)==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()==row['git_blob_sha1']
    p=ROOT/row['local']
    if p.exists():assert p.read_bytes()==original
expected={'M2_41':(41,0),'M3_lawful_32':(32,0),'packaged_M3_three':(3,0),'additional_15':(15,0),'exact_git_M3_patch':(3,0),'exact_git_M3_original':(3,3),'M1_original':(37,0),'I2_on_M1':(23,9),'M1_on_original_M2':(37,19),'I2_on_original_M2':(23,10),'M1_on_patch':(37,19),'I2_on_patch':(23,10),'local_hostile':(11,3)}
for row in load('execution_receipts.json'):
    label=row['label'];n,fail=expected[label]
    tree=ET.parse(ROOT/'evidence'/(label+'.xml'))
    counts={k:sum(int(x.get(k,0)) for x in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')}
    assert counts==dict(tests=n,failures=fail,errors=0,skipped=0)==row['counts']
    assert row['exit']==(1 if fail else 0)
    line=next(x for x in (ROOT/'evidence'/(label+'.log')).read_text().splitlines() if x.startswith('LOADED_KERNEL '))
    actual=json.loads(line.removeprefix('LOADED_KERNEL '));assert actual['file'].endswith('/kernel.py')
    if label in ('M2_41','M3_lawful_32','packaged_M3_three','additional_15','exact_git_M3_patch','M1_on_patch','I2_on_patch','local_hostile'):
        assert actual['sha256']==m['files']['m2_patch/kernel.py']['sha256']
    elif label in ('M1_original','I2_on_M1'):assert actual['sha256']==sha(original_m1)
    else:assert actual['sha256']=='888d73fff63f70a22932f1001f5c9003104b0e5a9cdef84e93456151428676c8'
failed=[x.get('name') for x in ET.parse(ROOT/'evidence/local_hostile.xml').iter('testcase') if x.find('failure') is not None]
assert len(failed)==3 and all(x.startswith('test_consumed_later_relation_source_must_remain_bound') for x in failed)
probe=load('evidence/later_relation_probe.json')
assert probe['state_hash_before']==probe['state_hash_after'] and all(x['result']=='NOT_REFUSED' for x in probe['controls'])
for row in load('artifact_manifest.json')['files']:
    p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256'],row['path']
print('Verified supplied kernel/tests/archives, exact Git preimages, 13 graded executions, and retained 3 local REDs.')
