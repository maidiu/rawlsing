"""User-authorized author follow-up. Does not change original review evidence."""
import ast,hashlib,io,json,os,shutil,subprocess,sys,tarfile,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
REPO=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip())
S=R/'stage';OUT=R/'evidence';OUT.mkdir(exist_ok=True)
AUTHOR='WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1'
def archive(sha,path,dest):
 raw=subprocess.check_output(['git','archive',sha,path],cwd=REPO)
 with tarfile.open(fileobj=io.BytesIO(raw)) as t:
  for m in t.getmembers():assert not m.issym() and not m.islnk() and (dest/m.name).resolve().is_relative_to(dest.resolve())
  t.extractall(dest)
archive('d97a5df8c03d02ca3c7433937550cdb6774537b5',AUTHOR,S)
V=S/AUTHOR;D=V/'stage';scope={}
for node in ast.parse((V/'repair/reproduce.py').read_text()).body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('E','G','H','J','K','F','I','PINS'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<pins>','exec'),scope)
for path,sha in scope['PINS'].items():archive(sha,path,D)
archive('9f4a23cef1482e0a81afb1e7a65df90879931465',scope['E']+'/court',D/'pre')
shutil.copytree(D/'pre'/scope['E']/'court',D/scope['I']/'court',dirs_exist_ok=True)
E=D/scope['E'];G=D/scope['G'];seat=E/'court/runtime_root/gf1_pair_support_consumer.py'
(D/scope['I']/'court/runtime_root/gf1_pair_support_consumer.py').write_bytes(seat.read_bytes())
candidate=(R/'gf1_pair_support_consumer.py').read_bytes();prior=(V/'repair/gf1_pair_support_consumer.py').read_bytes()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'),GF1M_HISTORICAL_HELPER=str(V/'phase_a/test_gf1l_executable_v2.py'),GF1M_ORIGINAL_PHASE_A=str(P/'03_REAL_JUNIT_282_NESTED44_COLD_AND_NEW_ADVERSARIALS/test_independent_domains.py'))
results=[]
def run(name,args,cwd):
 p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
 (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
 results.append(dict(name=name,command=args,cwd=str(cwd),exit=p.returncode))
 (OUT/'commands.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,p.returncode,p.stdout[-300:],flush=True)
 return p
original=Path(env['GF1M_ORIGINAL_PHASE_A'])
saved=seat.read_bytes()
try:
 seat.write_bytes(prior)
 run('before_author22',[sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',str(R/'test_nonfinite_refusal.py'),'--junitxml='+str(OUT/'before_author22.xml')],E/'court/repro')
 seat.write_bytes(saved)
 # The reviewed implementation is untouched. Only this follow-up's isolated
 # replay seat gets the new candidate; inherited qualification code is unchanged.
 (V/'repair/gf1_pair_support_consumer.py').write_bytes(candidate)
 p=run('qualify_repair282',[sys.executable,str(V/'repair/qualify.py')],REPO)
 assert p.returncode==0,p.stderr
 for name,test,n in [('original_phase_a26',original,26),('author_nonfinite22',R/'test_nonfinite_refusal.py',22)]:
  seat.write_bytes(candidate)
  p=run(name,[sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',str(test),'--junitxml='+str(OUT/(name+'.xml'))],E/'court/repro')
  assert p.returncode==0,p.stdout+p.stderr
  root=ET.parse(OUT/(name+'.xml')).getroot();cases=list(root.iter('testcase'))
  assert len(cases)==n and all(c.find('failure') is None and c.find('error') is None and c.find('skipped') is None for c in cases)
 for folder,src in [('qualification',V/'repair/current_qualification/evidence'),('retained',V/'repair/current_qualification/retained_replay/evidence')]:
  target=OUT/folder;target.mkdir(exist_ok=True)
  for file in src.iterdir():
   if file.is_file():shutil.copyfile(file,target/file.name)
 for i in (0,1):shutil.copyfile(V/f'repair/current_qualification/gf1f/observations/gf1f_cold_{i}.json',OUT/f'cold82_{i}.json')
 for source,name in [(V/'repair/current_qualification/CURRENT_QUALIFICATION_SUMMARY.json','current_qualification_summary.json'),(V/'repair/current_qualification/retained_replay/native_sources_imports_and_tests.json','native_source_provenance.json')]:shutil.copyfile(source,OUT/name)
 print('Author follow-up: current282, nested44, original PhaseA26 and new22 PASS',flush=True)
finally:seat.write_bytes(saved)
