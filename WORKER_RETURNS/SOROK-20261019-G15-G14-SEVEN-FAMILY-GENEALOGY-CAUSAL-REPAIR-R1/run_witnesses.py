"""Persist same-node positive/fault JUnit, exact source and restore custody.
Shared checker is also executed unchanged against the same eleven contracts.
"""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
import xml.etree.ElementTree as ET
from court_runner import ROOT,REPO,dump,ENV


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def one(label,node):
 out=ROOT/'execution/faults';out.mkdir(parents=True,exist_ok=True)
 cmd=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--tb=short',node,'--junitxml='+str(out/(label+'.xml'))]
 p=subprocess.run(cmd,cwd=REPO,env=ENV,capture_output=True,text=True)
 (out/(label+'.txt')).write_text((p.stdout+p.stderr).replace(str(REPO),'$WORKTREE'))
 xml=out/(label+'.xml');cases=list(ET.parse(xml).iter('testcase'));assert len(cases)==1
 failure=cases[0].find('failure');error=cases[0].find('error');skip=cases[0].find('skipped')
 xml.write_text(xml.read_text().replace(str(REPO),'$WORKTREE'))
 return dict(exit=p.returncode,assertion_failure=failure is not None and ('AssertionError' in failure.get('type','') or 'AssertionError' in failure.get('message','') or failure.get('message','').startswith('assert ')),error=error is not None,skip=skip is not None,node=node,command=[x.replace(str(REPO),'$WORKTREE') for x in cmd],junit=str(xml.relative_to(ROOT)),stdout='execution/faults/'+label+'.txt',failure_message=failure.get('message') if failure is not None else None)


def main():
 contract=ROOT/'test_g15_causal.py.proof.json';rows=[]
 for claim in json.loads(contract.read_text())['claims']:
  f=claim['fault'];p=REPO/f['path'];before=p.read_text();sha=digest(p)
  assert before.count(f['old'])==1
  label=claim['claim_id'].lower();positive=one(label+'_positive',claim['positive_node'])
  assert positive['exit']==0 and not positive['error'] and not positive['skip'],positive
  try:
   p.write_text(before.replace(f['old'],f['new'],1));fault_sha=digest(p)
   fault=one(label+'_fault',claim['positive_node'])
  finally:p.write_text(before)
  assert digest(p)==sha
  assert fault['exit']==1 and fault['assertion_failure'] and not fault['error'] and not fault['skip'],fault
  rows.append(dict(claim=claim,positive=positive,fault=fault,source_before_sha256=sha,source_fault_sha256=fault_sha,restored_sha256=digest(p),proof_grade='CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED'))
  print(claim['claim_id'],'PASS -> SAME_ASSERTION_RED -> RESTORED',flush=True)
 dump(ROOT/'execution/faults/receipts.json',rows)
 checker=ROOT/'frozen/shared/CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py'
 for label,args in [('lint',['lint',str(ROOT/'test_g15_causal.py')]),('witness',['witness',str(contract),'--root',str(REPO),'--receipt',str(ROOT/'execution/shared_proof_witness.json')])]:
  cmd=[sys.executable,'-B',str(checker),*args];p=subprocess.run(cmd,cwd=REPO,env=ENV,capture_output=True,text=True)
  (ROOT/'execution'/('shared_proof_'+label+'.txt')).write_text((p.stdout+p.stderr).replace(str(REPO),'$WORKTREE'))
  assert p.returncode==0,p.stdout+p.stderr
 print('Shared checker: LINT and WITNESS PASS',flush=True)
if __name__=='__main__':main()
