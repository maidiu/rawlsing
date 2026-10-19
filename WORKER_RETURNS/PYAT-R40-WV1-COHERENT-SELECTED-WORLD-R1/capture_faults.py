"""Retain claim-specific assertion RED XML/logs, exact restore and cold greens."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUT=ROOT/'evidence/faults'
def run(node, stem):
    xml=OUT/(stem+'.xml')
    result=subprocess.run([sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',node,'--junitxml='+str(xml)],cwd=REPO,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
    text=result.stdout.replace(str(REPO),'<ISOLATED_WORKTREE>')
    (OUT/(stem+'.log')).write_text(text)
    data=xml.read_text().replace(str(REPO),'<ISOLATED_WORKTREE>')
    xml.write_text(data)
    return result.returncode,ET.parse(xml).getroot()
if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    contract=json.loads((ROOT/'test_world_consumer.py.proof.json').read_text())
    receipts=[]
    for claim in contract['claims']:
        fault=claim['fault'];path=REPO/fault['path'];before=path.read_bytes();old=fault['old'].encode();new=fault['new'].encode()
        assert before.count(old)==1
        node=claim['positive_node'];stem=claim['claim_id'].lower()
        code,_=run(node,stem+'_positive');assert code==0
        try:
            path.write_bytes(before.replace(old,new,1))
            code,tree=run(node,stem+'_mutant')
            failures=list(tree.iter('failure'))
            assert code==1 and len(failures)==1
            assert failures[0].get('message','').startswith('AssertionError:'),ET.tostring(failures[0],encoding='unicode')
            assert not list(tree.iter('error'))
            failure=failures[0].get('message')
        finally:
            path.write_bytes(before)
        code,_=run(node,stem+'_restored');assert code==0
        assert path.read_bytes()==before
        receipts.append(dict(claim_id=claim['claim_id'],positive_node=node,
                             positive='PASS',mutant='ASSERTION_RED',assertion=failure,
                             restored='PASS',original_bytes_restored=True,
                             restored_sha256=hashlib.sha256(before).hexdigest()))
    (OUT/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
