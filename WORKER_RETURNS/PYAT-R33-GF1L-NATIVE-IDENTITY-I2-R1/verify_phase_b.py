"""Verify independent evidence, actual imported candidate, and frozen test bytes."""
import hashlib,json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent; REPO=R.parents[1];S=R/'stage'
E='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G='WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
H='WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1'
J='WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1'
F='WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
I='WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1'
K='WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1';SHA='1399a475e54ea33355cf641979829424625c511d'
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT';C=S/E/'court'
def gitbytes(sha,p):return subprocess.check_output(['git','show',sha+':'+p],cwd=REPO)
def identity(b):return dict(git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
sel=json.loads((C/'source_selector.json').read_text());native=[]
for row in sel['files']:
    b=(C/'runtime_root'/row['staged_path']).read_bytes()
    assert b==gitbytes(row['commit'],row['source_path'])
    ids=identity(b)
    assert all(ids[k]==row[k] for k in ids)
    native.append(dict(row,original_git_bytes_match=True))
assert len(native)==74
candidate_path=K+'/gf1_pair_support_consumer.py';candidate=gitbytes(SHA,candidate_path);candidate_id=identity(candidate)
producer_path=E+'/court/runtime_root/generic_native_pair_relation.py';producer=gitbytes('eeb726357204653b22458dc267dd70ba0009bd77',producer_path)
assert (C/'runtime_root/generic_native_pair_relation.py').read_bytes()==producer
before=gitbytes('cc41ad4553d189a3c4c8152179b3d1977327c07f',H+'/gf1_pair_support_consumer.py')
assert (S/K/'before/gf1_pair_support_consumer.py').read_bytes()==before
assert identity(before)['git_blob_sha1']=='66658149fd7362e17c064a3fc1f9029d638f9ed9'
tests=[]
for sha,path in [
 ('eeb726357204653b22458dc267dd70ba0009bd77',E+'/court/repro/test_gf1_generic_pair.py'),
 ('ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7',G+'/phase_a/test_gf1g_precommitted.py'),
 ('cc41ad4553d189a3c4c8152179b3d1977327c07f',H+'/test_gf1h_adversarial.py'),
 ('f3f34bc1b7b9fd97a3ae8a9b24dd2201f42f38f5',J+'/repro/test_gf1j_postfreeze_native_identity_hostiles.py'),
 ('3dcc7d7dddfff4f1be8b4293cab92e5b4275007d',F+'/tests/test_gf1f_independent_consumer.py'),
 ('c6a55f0dd5b327c40d64f96e0705ab5485559e90',I+'/court/test_gf1i_independent.py'),
 (SHA,K+'/test_gf1k_native_identity.py')]:
    b=(S/path).read_bytes();assert b==gitbytes(sha,path)
    tests.append(dict(commit=sha,path=path,unchanged=True,**identity(b)))
for sha,path in [('8dbf894109d0d81b5b0b936939484ab95771ddd3','phase_a/test_gf1l_frozen.py'),('4d3566081e4f552c14327bd3f1d1ec57fb13e762','phase_a/test_gf1l_executable_v2.py'),('6a52f266da7261c9fee777af5505a86709b005f6','postinspection/test_gf1l_typed_domain_conservation.py'),('8dbf894109d0d81b5b0b936939484ab95771ddd3','01_INDEPENDENT_PHASE_A_FROZEN_SHA_AND_ORACLE.json')]:
    b=(R/path).read_bytes();assert b==gitbytes(sha,str(R.relative_to(REPO)/path))
    tests.append(dict(commit=sha,path=path,unchanged=True,**identity(b)))
cold=[json.loads((OUT/f'gf1k_cold_{i}.log').read_text()) for i in (0,1)]
a,b=[dict(v) for v in cold];assert a.pop('pid')!=b.pop('pid');assert a==b
for receipt in cold:
    assert Path(receipt['producer_file']).read_bytes()==producer
    assert Path(receipt['consumer_file']).read_bytes()==candidate
    assert receipt['result']['production_owner_commit'] is False
    assert receipt['custody']['native_reattested']==74
    for row in receipt['custody']['imports']:
        p=C.parent/row['file'];ids=identity(p.read_bytes())
        assert p.resolve().is_relative_to((S/E).resolve())
        assert ids['git_blob_sha1']==row['blob_sha1'] and ids['sha256']==row['sha256']
        # Every local Python import in the native receipt must match its exact
        # transported original Git source, except the deliberately seated consumer.
        relative=str(p.relative_to(S))
        src=candidate if p.name=='gf1_pair_support_consumer.py' else gitbytes('eeb726357204653b22458dc267dd70ba0009bd77',relative)
        assert src==p.read_bytes(),relative
summary=[]
for xml in sorted(OUT.glob('*.xml')):
    root=ET.parse(xml).getroot();suites=[root] if root.tag=='testsuite' else list(root.findall('testsuite'))
    counts={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}
    failures=[dict(node=t.attrib.get('name'),class_name=t.attrib.get('classname'),message=(t.find('failure') if t.find('failure') is not None else t.find('error')).attrib.get('message')) for t in root.iter('testcase') if t.find('failure') is not None or t.find('error') is not None]
    summary.append(dict(court=xml.stem,**counts,failures_by_node=failures,sha256=hashlib.sha256(xml.read_bytes()).hexdigest()))
# Exact historical node identities, no new failures hidden by an equal count.
byname={s['court']:s for s in summary}
for key,expected in [('gf1f100',4),('gf1i19',2)]:
    base=byname['gf1h_'+key];now=byname['gf1k_'+key]
    assert now['failures']==expected and now['errors']==0 and now['skipped']==0
    assert {v['node'] for v in base['failures_by_node']}=={v['node'] for v in now['failures_by_node']}
for key,n in [('original44',44),('gf1g26',26),('gf1h26',26),('gf1j_native_two_plus_positive',3),('gf1l_executable_v2',14),('author12_independent_execution',12)]:
    court=byname['gf1k_'+key];assert court['tests']==n and court['failures']==court['errors']==court['skipped']==0,court
baseline_supp=byname['gf1h_postinspection_typed_domains'];assert (baseline_supp['tests'],baseline_supp['failures'],baseline_supp['errors'],baseline_supp['skipped'])==(10,0,0,0)
supp=byname['gf1k_postinspection_typed_domains'];assert (supp['tests'],supp['failures'],supp['errors'],supp['skipped'])==(10,4,0,0)
obj=dict(candidate_commit=SHA,candidate_path=candidate_path,candidate_identity=candidate_id,original_generic_producer=dict(commit='eeb726357204653b22458dc267dd70ba0009bd77',path=producer_path,**identity(producer)),prior_GF1H_consumer=identity(before),native_files=native,native_file_count=74,python_file_count=sum(row['staged_path'].endswith('.py') for row in native),frozen_tests=tests,cold_processes=cold,distinct_pid=True,identical_non_pid_receipts=True,source_qualification='Original native sourcefree fixture chain; supplemental typed-domain variants are self-rehashed original-constructor TEST_ONLY objects, not source-qualified source outputs',issuer_scope='Structural self-hash is not authenticated signatory; no source/owner/method/FF/actor/OC05/N11/N12/V3 grant',GF1G_original_phase_a_full_sha='ecd975ad5b424f952ac248dfcf1b7a83aa867a6a')
(R/'02_EXACT_NATIVE_SOURCE_IMPORTS_AND_ISSUER_SCOPE.json').write_text(json.dumps(obj,indent=2)+'\n')
(R/'court_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(dict(candidate=candidate_id,native_files=74,python_files=obj['python_file_count'],actual_native_imports=len(cold[0]['custody']['imports']),cold_pids=[v['pid'] for v in cold],unchanged_test_files=len(tests),required_positive_cases=125,historical_failures=6,postinspection=dict(pass_count=6,fail_count=4)),indent=2))
