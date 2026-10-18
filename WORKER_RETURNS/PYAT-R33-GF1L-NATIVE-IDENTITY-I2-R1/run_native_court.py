"""GF1L independent sourcefree replay. No GF1K bytes read until remote freeze."""
import hashlib, io, json, os, shutil, subprocess, sys, tarfile
from pathlib import Path
R=Path(__file__).resolve().parent
REPO=R.parents[1]
S=R/'stage'; S.mkdir(exist_ok=True)
OUT=R/'03_REAL_FROZEN_ALL_COURTS_AND_COLD_JUNIT'; OUT.mkdir(exist_ok=True)
E='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
G='WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
H='WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1'
J='WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1'
F='WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
I='WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1'
PIN={E:'eeb726357204653b22458dc267dd70ba0009bd77',G:'ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7',H:'cc41ad4553d189a3c4c8152179b3d1977327c07f',J:'f3f34bc1b7b9fd97a3ae8a9b24dd2201f42f38f5',F:'3dcc7d7dddfff4f1be8b4293cab92e5b4275007d',I:'c6a55f0dd5b327c40d64f96e0705ab5485559e90'}
transport=[]
def archive(sha,path,dest=S):
    data=subprocess.check_output(['git','archive',sha,path],cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        for m in t.getmembers():
            assert not m.issym() and not m.islnk()
            assert (dest/m.name).resolve().is_relative_to(dest.resolve())
            if m.isfile():
                b=t.extractfile(m).read()
                transport.append(dict(commit=sha,path=m.name,git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
        t.extractall(dest)
for p,sha in PIN.items(): archive(sha,p)
pre=S/'pre'; pre.mkdir(exist_ok=True)
archive('9f4a23cef1482e0a81afb1e7a65df90879931465',E+'/court',pre)
shutil.copytree(pre/E/'court',S/I/'court',dirs_exist_ok=True)
# Exact GF1H consumer only, over untouched original native dependency tree.
for target in (S/E/'court/runtime_root/gf1_pair_support_consumer.py',S/F/'candidate/court/runtime_root/gf1_pair_support_consumer.py',S/I/'court/runtime_root/gf1_pair_support_consumer.py'):
    shutil.copyfile(S/H/'gf1_pair_support_consumer.py',target)
(R/'source_transport.json').write_text(json.dumps(transport,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(S/E),GF1G_ORACLE=str(S/G/'01_FROZEN_ORACLE.json'),GF1H_COURT=str(S/E),GF1H_GF1G=str(S/G),GF1J_GF1G_TEST=str(S/G/'phase_a/test_gf1g_precommitted.py'))
py=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider']
results=[]
def run(name,args,cwd):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
    (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
    results.append(dict(name=name,exit=p.returncode,command=args,cwd=str(cwd)))
    (R/'run_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name,p.returncode,p.stdout[-350:],flush=True)
for name,test,cwd in [
 ('gf1h_original44','test_gf1_generic_pair.py',S/E/'court/repro'),
 ('gf1h_gf1g26',str(S/G/'phase_a/test_gf1g_precommitted.py'),S/E/'court/repro'),
 ('gf1h_gf1h26',str(S/H/'test_gf1h_adversarial.py'),S/E/'court/repro'),
 ('gf1h_gf1j_native_two_plus_positive',str(S/J/'repro/test_gf1j_postfreeze_native_identity_hostiles.py'),S/E/'court/repro'),
 ('gf1h_gf1l_frozen',str(R/'phase_a/test_gf1l_frozen.py'),S/E/'court/repro'),
 ('gf1h_gf1l_executable_v2',str(R/'phase_a/test_gf1l_executable_v2.py'),S/E/'court/repro'),
 ('gf1h_gf1f100','tests/test_gf1f_independent_consumer.py',S/F),
 ('gf1h_gf1i19','test_gf1i_independent.py',S/I/'court')]:
    run(name,py+[test,'--import-mode=importlib','--junitxml='+str(OUT/(name+'.xml'))],cwd)
for n in (0,1):
    run('gf1h_cold_'+str(n),[sys.executable,str(R/'cold_native.py')],S/E/'court/repro')
