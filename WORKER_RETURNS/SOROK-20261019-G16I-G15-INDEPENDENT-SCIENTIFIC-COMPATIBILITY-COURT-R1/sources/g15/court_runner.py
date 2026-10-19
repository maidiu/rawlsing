"""Offline exact-source baseline and candidate courts; no live provider transport."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, time
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')

def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def stage(name):
 dst=ROOT/'runs'/name; g13=ROOT/'frozen/g13'
 for sub in ['03_POSTREPAIR_COURT','04_G13_AUTHOR_COURT']:
  shutil.copytree(g13/sub,dst/'reproduction'/sub,dirs_exist_ok=True,ignore=shutil.ignore_patterns('evidence','__pycache__'))
 for f in ['test_g14_science.py']:
  shutil.copyfile(ROOT/'frozen/g14'/f,dst/f)
 (dst/'execution').mkdir(parents=True,exist_ok=True)
 (dst/'reproduction/03_POSTREPAIR_COURT/evidence').mkdir(parents=True,exist_ok=True)
 if name=='candidate':
  shutil.copytree(ROOT/'candidate/lab_sgi1',dst/'reproduction/03_POSTREPAIR_COURT/sources/sgi1/01_LAB_IMPLEMENTATION/lab_sgi1',dirs_exist_ok=True)
  shutil.copytree(ROOT/'candidate/data',dst/'reproduction/03_POSTREPAIR_COURT/sources/sgi1/01_LAB_IMPLEMENTATION/data',dirs_exist_ok=True)
 return dst

def run(name,label,cwd,paths,extra_env=None):
 out=ROOT/'execution'/name;out.mkdir(parents=True,exist_ok=True)
 cmd=[sys.executable,'-B','-m','pytest','-q','-s','-p','no:cacheprovider','--tb=short',*paths,'--junitxml='+str(out/(label+'.xml'))]
 t=time.monotonic();p=subprocess.run(cmd,cwd=cwd,env=dict(ENV,**(extra_env or {})),capture_output=True,text=True)
 (out/(label+'.txt')).write_text((p.stdout+p.stderr).replace(str(REPO),'$WORKTREE'))
 xml=out/(label+'.xml');cases=[]
 if xml.exists():
  xml.write_text(xml.read_text().replace(str(REPO),'$WORKTREE'))
  for c in ET.parse(xml).iter('testcase'):
   cases.append(dict(classname=c.get('classname'),name=c.get('name'),status='RED' if c.find('failure') is not None else 'ERROR' if c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'))
 counts={s:sum(c['status']==s for c in cases) for s in ['PASS','RED','ERROR','SKIP']}
 row=dict(suite=label,command=['python3',*cmd[1:]],cwd=str(cwd.relative_to(ROOT)),exit=p.returncode,seconds=time.monotonic()-t,counts=counts,cases=cases,junit=str(xml.relative_to(ROOT)))
 # Commands and output remain portable; only checkout path is substituted.
 row['command']=[x.replace(str(REPO),'$WORKTREE') for x in row['command']]
 print(name,label,p.returncode,counts,flush=True);return row

def courts(name):
 dst=stage(name); court=dst/'reproduction/03_POSTREPAIR_COURT';author=dst/'reproduction/04_G13_AUTHOR_COURT'
 rows=[]
 for label,paths in [('sgi1_target',['test_original_sgi1.py']),('g11',['sources/g11/test_g11_solver.py']),('g12_controls',['test_g12_controls.py']),('g12_literal',['test_g12_literal_contract.py']),('g12_supplemental',['test_g12_supplemental.py']),('candidate_boundary',['test_candidate_boundary.py'])]:
  rows.append(run(name,label,court,paths))
 for label,f in [('g13_author','test_g13_author_court.py'),('g13_postrepair','test_g13_postrepair_original.py')]:rows.append(run(name,label,author,[f]))
 rows.append(run(name,'g14_science',dst,['test_g14_science.py']))
 dump(ROOT/'execution'/name/'results.json',rows)
 shutil.copyfile(dst/'execution/g14_observations.json',ROOT/'execution'/name/'g14_observations.json')
 return rows
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('name',choices=['baseline','candidate']);a=p.parse_args();courts(a.name)
