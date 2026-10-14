"""Actual unchanged predecessor and independent-RED replay; no model calls."""
from pathlib import Path
import json,subprocess,hashlib,gzip,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent

def main():
 (R/'receipts/baseline').mkdir(parents=True,exist_ok=True)
 p=R/'imports/RMB/imports';p.mkdir(exist_ok=True)
 for label in ['LAB1','LAB2']:
  dest=p/label
  if not dest.exists():dest.symlink_to(R/'imports'/label,target_is_directory=True)
 runs=[('lab1',['python3','-m','pytest','lab/test_lab.py','-q','--junitxml=../../receipts/baseline/lab1.xml'],'LAB1',0),('machine',['python3','lab/run_lab.py'],'LAB1',0),('lab2',['python3','-m','pytest','lab2/test_lab2.py','-q','--junitxml=../../receipts/baseline/lab2.xml'],'LAB2',0),('rmb',['python3','-m','pytest','test_independent.py','-q','--tb=short','--junitxml=../../receipts/baseline/rmb.xml'],'RMB',1)]
 for name,args,label,want in runs:
  result=subprocess.run(args,cwd=R/'imports'/label,text=True,capture_output=True)
  text=(result.stdout+result.stderr).replace(str(R.parents[1]),'<WORKTREE>')
  (R/f'receipts/baseline/{name}.txt').write_text(' '.join(args)+'\nexit='+str(result.returncode)+'\n'+text)
  print(name,result.returncode,text[-160:]);assert result.returncode==want
  xml=R/f'receipts/baseline/{name}.xml'
  if xml.exists():
   tree=ET.parse(xml)
   for el in tree.iter():
    el.attrib.pop('hostname',None)
    if el.text:el.text=el.text.replace(str(R.parents[1]),'<WORKTREE>')
   tree.write(xml,encoding='unicode')
 old=json.loads(subprocess.check_output(['git','show','d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09:WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/outputs/primary_results.json']))
 new=json.loads((R/'imports/LAB1/outputs/primary_results.json').read_text())
 equal={k:old[k]==new[k] for k in ['scores','integrity','null_controls','opacity','comparison']}
 assert new['trial_count']==576 and all(equal.values())
 (R/'receipts/baseline/primary_results.json.gz').write_bytes(gzip.compress(json.dumps(new,sort_keys=True).encode(),mtime=0))
 r1=R/'imports/LAB2/01_PREREGISTRATION_FROZEN.json'
 receipt={'trial_count':576,'semantic_sections_equal':equal,'r1_freeze_sha256':hashlib.sha256(r1.read_bytes()).hexdigest(),'RMB_tests':36,'RMB_pass':13,'RMB_red':23,'model_calls':0,'claims':'Synthetic machine reproduction only; original R1 and its 23 REDs remain unchanged'}
 assert receipt['r1_freeze_sha256']=='880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330'
 (R/'receipts/baseline/summary.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
