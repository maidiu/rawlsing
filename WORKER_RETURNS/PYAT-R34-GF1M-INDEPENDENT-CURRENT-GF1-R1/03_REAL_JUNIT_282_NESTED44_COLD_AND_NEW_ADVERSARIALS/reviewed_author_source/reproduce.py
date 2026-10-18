"""Retained repair replay and historical diagnostics; use qualify.py for the current gate.
Only ignored stage seating is mutable. Old review evidence is never overwritten.
"""
import hashlib,io,json,os,subprocess,sys,tarfile,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent; REVIEW=R.parent;REPO=REVIEW.parents[1];S=REVIEW/'stage'
ARTIFACTS=Path(os.environ.get('GF1_REPAIR_ARTIFACT_DIR',str(R))).resolve()
assert ARTIFACTS.is_relative_to(R.resolve()), 'repair artifacts must stay within repair return'
ARTIFACTS.mkdir(parents=True,exist_ok=True)
OUT=ARTIFACTS/'evidence';OUT.mkdir(exist_ok=True)
E='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G='WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
H='WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1'
J='WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1'
K='WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1'
F='WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
I='WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1'
PINS={E:'eeb726357204653b22458dc267dd70ba0009bd77',G:'ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7',H:'cc41ad4553d189a3c4c8152179b3d1977327c07f',J:'f3f34bc1b7b9fd97a3ae8a9b24dd2201f42f38f5',K:'1399a475e54ea33355cf641979829424625c511d',F:'3dcc7d7dddfff4f1be8b4293cab92e5b4275007d',I:'c6a55f0dd5b327c40d64f96e0705ab5485559e90'}
def gitbytes(sha,path):return subprocess.check_output(['git','show',sha+':'+path],cwd=REPO)
def ids(b):return dict(git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def archive(sha,path,dest=S):
    dest.mkdir(parents=True,exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',sha,path],cwd=REPO))) as t:
        for m in t.getmembers():
            assert not m.issym() and not m.islnk() and (dest/m.name).resolve().is_relative_to(dest.resolve())
        t.extractall(dest)
# Reconstruct source bytes only if absent. Never run old report writers to bootstrap.
for path,sha in PINS.items():
    if not (S/path).is_dir():archive(sha,path)
if not (S/I/'court/runtime_root').is_dir():
    archive('9f4a23cef1482e0a81afb1e7a65df90879931465',E+'/court',S/'pre')
    import shutil
    shutil.copytree(S/'pre'/E/'court',S/I/'court',dirs_exist_ok=True)
from staging import stage_gf1i_parent_metadata
metadata=stage_gf1i_parent_metadata(REPO,S/I)
(ARTIFACTS/'staged_parent_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
C=S/E/'court'; RT=C/'runtime_root'
selector=json.loads((C/'source_selector.json').read_text());native=[]
for row in selector['files']:
    b=(RT/row['staged_path']).read_bytes();assert b==gitbytes(row['commit'],row['source_path'])
    assert all(ids(b)[k]==row[k] for k in ids(b))
    native.append(dict(row,original_git_bytes_match=True))
assert len(native)==74
# Exact immutable inherited test bytes, including the four new RED witnesses.
frozen=[]
for sha,path in [
 (PINS[E],E+'/court/repro/test_gf1_generic_pair.py'),
 (PINS[G],G+'/phase_a/test_gf1g_precommitted.py'),
 (PINS[H],H+'/test_gf1h_adversarial.py'),
 (PINS[J],J+'/repro/test_gf1j_postfreeze_native_identity_hostiles.py'),
 (PINS[K],K+'/test_gf1k_native_identity.py'),
 (PINS[F],F+'/tests/test_gf1f_independent_consumer.py'),
 (PINS[I],I+'/court/test_gf1i_independent.py'),
 ('4d3566081e4f552c14327bd3f1d1ec57fb13e762',str(REVIEW.relative_to(REPO)/'phase_a/test_gf1l_executable_v2.py')),
 ('6a52f266da7261c9fee777af5505a86709b005f6',str(REVIEW.relative_to(REPO)/'postinspection/test_gf1l_typed_domain_conservation.py'))]:
    p=REPO/path if path.startswith(str(REVIEW.relative_to(REPO))+'/phase_a') or path.startswith(str(REVIEW.relative_to(REPO))+'/postinspection') else S/path
    b=p.read_bytes();assert b==gitbytes(sha,path)
    frozen.append(dict(commit=sha,path=path,unchanged=True,**ids(b)))
prior=gitbytes(PINS[K],K+'/gf1_pair_support_consumer.py');repaired=(R/'gf1_pair_support_consumer.py').read_bytes()
seats=[RT/'gf1_pair_support_consumer.py',S/F/'candidate/court/runtime_root/gf1_pair_support_consumer.py',S/I/'court/runtime_root/gf1_pair_support_consumer.py']
saved={p:p.read_bytes() for p in seats}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(S/E),GF1G_ORACLE=str(S/G/'01_FROZEN_ORACLE.json'),GF1H_COURT=str(S/E),GF1H_GF1G=str(S/G),GF1J_GF1G_TEST=str(S/G/'phase_a/test_gf1g_precommitted.py'),GF1K_COURT=str(S/E),GF1K_GF1G=str(S/G))
py=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider'];results=[]
def run(name,test,cwd):
    args=py+[str(test),'--import-mode=importlib','--junitxml='+str(OUT/(name+'.xml'))]
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
    (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
    results.append(dict(name=name,exit=p.returncode,command=args,cwd=str(cwd)))
    print(name,p.returncode,p.stdout[-650:],flush=True)
def summary(name):
    root=ET.parse(OUT/(name+'.xml')).getroot(); suites=[root] if root.tag=='testsuite' else list(root.findall('testsuite'))
    counts={k:sum(int(v.attrib.get(k,0)) for v in suites) for k in ('tests','failures','errors','skipped')}
    nodes=[v.attrib['name'] for v in root.iter('testcase') if v.find('failure') is not None or v.find('error') is not None]
    return dict(name=name,**counts,failed_nodes=nodes,junit_sha256=ids((OUT/(name+'.xml')).read_bytes())['sha256'])
try:
    for p in seats:p.write_bytes(prior)
    run('before_supplemental',REVIEW/'postinspection/test_gf1l_typed_domain_conservation.py',C/'repro')
    assert (summary('before_supplemental')['tests'],summary('before_supplemental')['failures'])==(10,4)
    for p in seats:p.write_bytes(repaired)
    for name,test,cwd in [
        ('original44','test_gf1_generic_pair.py',C/'repro'),
        ('gf1g26',S/G/'phase_a/test_gf1g_precommitted.py',C/'repro'),
        ('gf1h26',S/H/'test_gf1h_adversarial.py',C/'repro'),
        ('gf1j_native_two_plus_positive',S/J/'repro/test_gf1j_postfreeze_native_identity_hostiles.py',C/'repro'),
        ('gf1l_frozen14',REVIEW/'phase_a/test_gf1l_executable_v2.py',C/'repro'),
        ('gf1k_author12',S/K/'test_gf1k_native_identity.py',C/'repro'),
        ('supplemental10',REVIEW/'postinspection/test_gf1l_typed_domain_conservation.py',C/'repro'),
        ('repair_storage_guard26',R/'test_storage_guard.py',C/'repro'),
        ('historical_gf1f100','tests/test_gf1f_independent_consumer.py',S/F),
        ('historical_gf1i19','test_gf1i_independent.py',S/I/'court')]:run(name,test,cwd)
    cold=[]
    for i in (0,1):
        p=subprocess.run([sys.executable,str(REVIEW/'cold_native.py')],cwd=C/'repro',env=env,text=True,capture_output=True)
        (OUT/f'cold_{i}.json').write_text(p.stdout);(OUT/f'cold_{i}.stderr').write_text(p.stderr)
        assert p.returncode==0,p.stderr
        receipt=json.loads(p.stdout);cold.append(receipt)
        assert Path(receipt['consumer_file']).read_bytes()==repaired
        assert Path(receipt['producer_file']).read_bytes()==gitbytes(PINS[E],E+'/court/runtime_root/generic_native_pair_relation.py')
        assert receipt['custody']['native_reattested']==74
        for imp in receipt['custody']['imports']:
            path=(S/E)/imp['file'];b=path.read_bytes();identity=ids(b)
            assert path.resolve().is_relative_to((S/E).resolve())
            assert identity['git_blob_sha1']==imp['blob_sha1'] and identity['sha256']==imp['sha256']
            expected=repaired if path.name=='gf1_pair_support_consumer.py' else gitbytes(PINS[E],str(path.relative_to(S)))
            assert b==expected
        original=json.loads((REVIEW/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT/gf1k_cold_0.log').read_text())
        assert receipt['result']==original['result'],'baseline result/hash changed'
    a,b=[dict(v) for v in cold];assert a.pop('pid')!=b.pop('pid');assert a==b
    checks=[summary(v['name']) for v in results]
    expected={'original44':44,'gf1g26':26,'gf1h26':26,'gf1j_native_two_plus_positive':3,'gf1l_frozen14':14,'gf1k_author12':12,'supplemental10':10,'repair_storage_guard26':26}
    for name,n in expected.items():
        got=summary(name);assert (got['tests'],got['failures'],got['errors'],got['skipped'])==(n,0,0,0),got
    baseline=json.loads((REVIEW/'court_summary.json').read_text())
    for name,old,n,fail in [('historical_gf1f100','gf1k_gf1f100',100,4),('historical_gf1i19','gf1k_gf1i19',19,2)]:
        got=summary(name);was=next(c for c in baseline if c['court']==old)
        assert (got['tests'],got['failures'],got['errors'],got['skipped'])==(n,fail,0,0),got
        assert set(got['failed_nodes'])=={v['node'] for v in was['failures_by_node']}
    (ARTIFACTS/'native_sources_imports_and_tests.json').write_text(json.dumps(dict(role='AUTHOR_REPAIR_NOT_INDEPENDENT_I2',candidate=ids(repaired),prior_candidate=dict(commit=PINS[K],**ids(prior)),native_files=native,native_file_count=74,python_files=sum(row['staged_path'].endswith('.py') for row in native),frozen_tests=frozen,cold_processes=cold,distinct_cold_pids=True,equal_non_pid_receipts=True,baseline_output_hash_unchanged=True,physical_import_hashes_verified_while_repair_seated=True,restore_original_seating_after_execution=True),indent=2)+'\n')
    (ARTIFACTS/'court_summary.json').write_text(json.dumps(checks,indent=2)+'\n')
    print('RETAINED REPLAY VERIFIED; HISTORICAL DIAGNOSTICS PRESERVED; CURRENT GATE: RUN qualify.py',flush=True)
finally:
    (ARTIFACTS/'run_results.json').write_text(json.dumps(results,indent=2)+'\n')
    for p,b in saved.items():p.write_bytes(b);assert p.read_bytes()==b
