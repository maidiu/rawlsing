"""Independent GF1L Phase B, exact returned GF1K over the original native tree."""
import hashlib,io,json,os,shutil,subprocess,sys,tarfile
from pathlib import Path
R=Path(__file__).resolve().parent; REPO=R.parents[1]; S=R/'stage'
SHA='1399a475e54ea33355cf641979829424625c511d'
K='WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1'
E='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G='WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
H='WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1'
J='WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1'
F='WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
I='WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1'
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT'; OUT.mkdir(exist_ok=True)
# Reconstruct exact predecessor if not already available. Original baseline outputs
# and frozen files remain retained, independently of candidate-stage products.
if not (S/E/'court/source_selector.json').is_file():
    subprocess.run([sys.executable,str(R/'run_native_court.py')],cwd=REPO,check=True)
for commit in ('8dbf894109d0d81b5b0b936939484ab95771ddd3','4d3566081e4f552c14327bd3f1d1ec57fb13e762'):
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=REPO,check=True)
# Native closure must still match all frozen selector identities before seating.
selector=json.loads((S/E/'court/source_selector.json').read_text())
for row in selector['files']:
    b=(S/E/'court/runtime_root'/row['staged_path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
    assert b==subprocess.check_output(['git','show',row['commit']+':'+row['source_path']],cwd=REPO)
transport=[]
data=subprocess.check_output(['git','archive',SHA,K],cwd=REPO)
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    for m in t.getmembers():
        assert not m.issym() and not m.islnk() and (S/m.name).resolve().is_relative_to(S.resolve())
        if m.isfile():
            b=t.extractfile(m).read()
            oid=subprocess.check_output(['git','rev-parse',SHA+':'+m.name],cwd=REPO,text=True).strip()
            assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
            transport.append(dict(commit=SHA,path=m.name,git_blob_sha1=oid,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
    t.extractall(S)
(R/'gf1k_source_transport.json').write_text(json.dumps(transport,indent=2)+'\n')
source=S/K/'gf1_pair_support_consumer.py'
for target in (S/E/'court/runtime_root/gf1_pair_support_consumer.py',S/F/'candidate/court/runtime_root/gf1_pair_support_consumer.py',S/I/'court/runtime_root/gf1_pair_support_consumer.py'):
    shutil.copyfile(source,target)
    assert target.read_bytes()==subprocess.check_output(['git','show',SHA+':'+K+'/gf1_pair_support_consumer.py'],cwd=REPO)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(S/E),GF1G_ORACLE=str(S/G/'01_FROZEN_ORACLE.json'),GF1H_COURT=str(S/E),GF1H_GF1G=str(S/G),GF1J_GF1G_TEST=str(S/G/'phase_a/test_gf1g_precommitted.py'),GF1K_COURT=str(S/E),GF1K_GF1G=str(S/G))
py=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider']
results=[]
def run(name,args,cwd):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
    (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
    results.append(dict(name=name,exit=p.returncode,command=args,cwd=str(cwd)))
    (R/'gf1k_run_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,p.returncode,p.stdout[-500:],flush=True)
for name,test,cwd in [
 ('gf1k_original44','test_gf1_generic_pair.py',S/E/'court/repro'),
 ('gf1k_gf1g26',str(S/G/'phase_a/test_gf1g_precommitted.py'),S/E/'court/repro'),
 ('gf1k_gf1h26',str(S/H/'test_gf1h_adversarial.py'),S/E/'court/repro'),
 ('gf1k_gf1j_native_two_plus_positive',str(S/J/'repro/test_gf1j_postfreeze_native_identity_hostiles.py'),S/E/'court/repro'),
 ('gf1k_gf1l_executable_v2',str(R/'phase_a/test_gf1l_executable_v2.py'),S/E/'court/repro'),
 ('gf1k_author12_independent_execution',str(S/K/'test_gf1k_native_identity.py'),S/E/'court/repro'),
 ('gf1k_gf1f100','tests/test_gf1f_independent_consumer.py',S/F),
 ('gf1k_gf1i19','test_gf1i_independent.py',S/I/'court')]:
    run(name,py+[test,'--import-mode=importlib','--junitxml='+str(OUT/(name+'.xml'))],cwd)
for n in (0,1):
    run('gf1k_cold_'+str(n),[sys.executable,str(R/'cold_native.py')],S/E/'court/repro')
