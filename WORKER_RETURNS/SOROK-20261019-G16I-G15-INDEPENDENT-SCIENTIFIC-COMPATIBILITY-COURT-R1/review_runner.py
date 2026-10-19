"""Independent review execution and same-node witnesses; never repair a candidate."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
def dump(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,node):
    out=ROOT/'execution/independent';out.mkdir(parents=True,exist_ok=True)
    obs=out/(label+'_observations.json');xml=out/(label+'.xml')
    cmd=[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','--tb=short',node,'--junitxml='+str(xml)]
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',G16I_OBSERVATIONS=str(obs.relative_to(ROOT)))
    t=time.monotonic();p=subprocess.run(cmd,cwd=REPO,env=env,capture_output=True,text=True)
    text=p.stdout+p.stderr
    # Only filesystem prefix and hostname are sanitized; assertion evidence kept.
    text=text.replace(str(REPO),'$WORKTREE')
    (out/(label+'.txt')).write_text(text)
    cases=[]
    for c in ET.parse(xml).iter('testcase'):
        f=c.find('failure');e=c.find('error');s=c.find('skipped')
        cases.append(dict(classname=c.get('classname'),name=c.get('name'),status='RED' if f is not None else 'ERROR' if e is not None else 'SKIP' if s is not None else 'PASS',failure_type=f.get('type') if f is not None else None,failure_message=f.get('message') if f is not None else None))
    return dict(command=[x.replace(str(REPO),'$WORKTREE') for x in cmd],exit=p.returncode,seconds=time.monotonic()-t,junit=str(xml.relative_to(ROOT)),observations=str(obs.relative_to(ROOT)),cases=cases)
def main():
    shutil.copytree(ROOT/'sources/g15/candidate',ROOT/'sandbox/candidate',dirs_exist_ok=True)
    proof=json.loads((ROOT/'test_g16i_science.py.proof.json').read_text());rows=[]
    for claim in proof['claims']:
        label=claim['claim_id'].lower();f=claim['fault'];p=REPO/f['path'];before=p.read_bytes();sha=digest(p)
        old=f['old'].encode();new=f['new'].encode();assert before.count(old)==1
        positive=run(label+'_positive',claim['positive_node']);assert positive['exit']==0,positive
        try:
            p.write_bytes(before.replace(old,new,1));fault_sha=digest(p)
            fault=run(label+'_fault',claim['positive_node'])
        finally:p.write_bytes(before)
        restored=run(label+'_restored',claim['positive_node'])
        assert digest(p)==sha and restored['exit']==0
        assert fault['exit']==1 and len(fault['cases'])==1 and (fault['cases'][0]['failure_type']=='AssertionError' or (fault['cases'][0]['failure_message'] or '').startswith(('assert ','AssertionError'))),fault
        rows.append(dict(claim=claim,positive=positive,fault=fault,restored=restored,before_sha256=sha,fault_sha256=fault_sha,restore_sha256=digest(p),proof_grade='CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED'))
        dump(ROOT/'execution/independent/fault_receipts.json',rows)
        print(label,'positive PASS -> same assertion RED -> restored PASS',flush=True)
    all_results=run('final_court',str(ROOT/'test_g16i_science.py'));dump(ROOT/'execution/independent/results.json',all_results)
    print('INDEPENDENT',[(s,sum(c['status']==s for c in all_results['cases'])) for s in ['PASS','RED','ERROR','SKIP']],flush=True)
    checker=ROOT/'sources/g15/frozen/shared/CROSS_HQ_CONTROL_ROOM/proof_integrity_gate_r1.py'
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',G16I_OBSERVATIONS='execution/shared_observations.json')
    for label,args in [('lint',['lint',str(ROOT/'test_g16i_science.py')]),('witness',['witness',str(ROOT/'test_g16i_science.py.proof.json'),'--root',str(REPO),'--receipt',str(ROOT/'execution/shared_witness.json')])]:
        p=subprocess.run([sys.executable,'-B',str(checker),*args],cwd=REPO,env=env,capture_output=True,text=True)
        (ROOT/'execution'/('shared_'+label+'.txt')).write_text((p.stdout+p.stderr).replace(str(REPO),'$WORKTREE'))
        assert p.returncode==0,p.stdout+p.stderr
        print('shared checker',label,'PASS',flush=True)
if __name__=='__main__':main()
