"""Native execution, retained assertion-level mutants, restored greens and cold replay."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;W=R.parents[1];E=R/'evidence'
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONPATH':str(W)}
def clean(s):
    return re.sub(r'hostname="[^"]*"','hostname="e04l-host"',s.replace(str(R),'RETURN').replace(str(W),'WORKTREE').replace(sys.executable,'PYTHON'))
def run(name,args):
    cmd=[sys.executable,*args];p=subprocess.run(cmd,cwd=W,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (E/(name+'.log')).write_text(clean(p.stdout))
    row=dict(name=name,command=[clean(x) for x in cmd],exit_code=p.returncode)
    for i,s in enumerate(args):
        if s.startswith('--junitxml='):
            x=W/s.split('=',1)[1];x.write_text(clean(x.read_text()));suites=ET.parse(x).getroot()
            row['testcases']=len(list(suites.iter('testcase')));row['failures']=len(list(suites.iter('failure')));row['errors']=len(list(suites.iter('error')));row['skips']=len(list(suites.iter('skipped')))
    return row
def pytest_args(test,name):return ['-B','-m','pytest','-q','-p','no:cacheprovider',test,'--junitxml='+str((E/(name+'.xml')).relative_to(W))]
def main():
    rows=[];test=str((R/'test_readthrough_consumer.py').relative_to(W))
    rows.append(run('final_court',pytest_args(test,'final_court')));assert rows[-1]['exit_code']==0
    original=str((R/'.runtime/e04jr/tests/test_e04j_native_original_consumer_join.py').relative_to(W))
    rows.append(run('original_native',pytest_args(original,'original_native')));assert rows[-1]['exit_code']==0
    contract=json.loads((R/'test_readthrough_consumer.py.proof.json').read_text())
    for n,claim in enumerate(contract['claims'],1):
        source=W/claim['fault']['path'];before=source.read_text();assert before.count(claim['fault']['old'])==1
        base=run(f'claim{n}_positive',pytest_args(claim['positive_node'],f'claim{n}_positive'));assert base['exit_code']==0
        try:
            source.write_text(before.replace(claim['fault']['old'],claim['fault']['new'],1))
            mutant=run(f'claim{n}_mutant',pytest_args(claim['positive_node'],f'claim{n}_mutant'))
        finally:source.write_text(before)
        assert mutant['exit_code']==1 and mutant['failures']==1 and mutant['errors']==0 and mutant['skips']==0
        expected='RELEASE_EDGE_SEVERED_BUT_ORIGINAL_CONSUMER_STILL_PRODUCTIVE' if n==1 else 'DID NOT RAISE'
        assert expected in (E/f'claim{n}_mutant.log').read_text()
        restored=run(f'claim{n}_restored',pytest_args(claim['positive_node'],f'claim{n}_restored'));assert restored['exit_code']==0
        rows.extend([base,mutant,restored])
    rows.append(run('proof_gate',['-B','CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py','witness',str((R/'test_readthrough_consumer.py.proof.json').relative_to(W)),'--root','.', '--receipt',str((E/'proof_witness.json').relative_to(W))]));assert rows[-1]['exit_code']==0
    (E/'execution_receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
