"""Verify source identities, outcomes, unchanged failures and delivered artifacts."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
def load(p):return json.loads((ROOT/p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
kernel=sha((ROOT/'m2_patch/kernel.py').read_bytes())
assert kernel=='88bb8c65dfd88efd1843f16e1bb6d51e1fa01a0dc1fdccb13e03a9b2b394d8d3'
for row in load('input_sources.json'):
    data=(ROOT/row['local']).read_bytes()
    assert data==git('show',row['commit']+':'+row['path']) and sha(data)==row['sha256']
for row in load('source_refs.json'):
    b=git('show',row['commit']+':'+row['path'])
    assert sha(b)==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
expected={'M2_41':(41,0),'M3_lawful_32':(32,0),'packaged_M3_three':(3,0),'additional_15':(15,0),'exact_git_M3_patch':(3,0),'exact_git_M3_original':(3,3),'M1_original':(37,0),'I2_on_M1':(23,9),'M1_on_original_M2':(37,19),'I2_on_original_M2':(23,10),'M1_on_patch':(37,19),'I2_on_patch':(23,10),'local_hostile':(11,0),'relation_regressions':(14,0)}
for row in load('execution_receipts.json'):
    n,fail=expected.pop(row['label']);tree=ET.parse(ROOT/'evidence'/(row['label']+'.xml'))
    counts={k:sum(int(x.get(k,0)) for x in tree.iter('testsuite')) for k in ('tests','failures','errors','skipped')}
    assert counts==row['counts']==dict(tests=n,failures=fail,errors=0,skipped=0)
    assert row['exit']==(1 if fail else 0)
    actual=json.loads(next(x.removeprefix('LOADED_KERNEL ') for x in (ROOT/'evidence'/(row['label']+'.log')).read_text().splitlines() if x.startswith('LOADED_KERNEL ')))
    if row['label'] in ('M2_41','M3_lawful_32','packaged_M3_three','additional_15','exact_git_M3_patch','M1_on_patch','I2_on_patch','local_hostile','relation_regressions'):assert actual['sha256']==kernel
assert not expected
def failures(tree):return [x.get('name') for x in tree.iter('testcase') if x.find('failure') is not None]
parent='6805da13bf2291837c9620784b2d31b82103c3a3'
prefix='WORKER_RETURNS/SOROK-M2-PREIMAGE-CUSTODY-EXPERIMENTAL-R1/evidence/'
for name in ('M1_on_patch','I2_on_patch'):
    old=ET.fromstring(git('show',parent+':'+prefix+name+'.xml'))
    assert failures(old)==failures(ET.parse(ROOT/'evidence'/(name+'.xml')))
assert len(failures(ET.parse(ROOT/'evidence/baseline/local_hostile.xml')))==3
probe=load('evidence/later_relation_probe.json')
assert probe['state_hash_before']==probe['state_hash_after']
assert len(probe['controls'])==3 and all(x['result']=='REFUSED' and x['code']=='SOURCE_PREIMAGE_IDENTITY_COLLISION' for x in probe['controls'])
for row in load('artifact_manifest.json')['files']:
    p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256'],row['path']
print('Verified R2 source custody, 14 graded courts, unchanged frozen tests/compatibility REDs, and artifact hashes.')
