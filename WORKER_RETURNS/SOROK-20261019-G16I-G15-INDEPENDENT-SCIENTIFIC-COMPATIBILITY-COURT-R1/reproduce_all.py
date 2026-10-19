"""Reproduce all commissioned courts from exact included source preimages.
Requires local pinned Git objects, Python3.11+ and pytest; no acquisition/provider call.
Only writes this return. The literal REDs are required evidence, not driver failure.
"""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
G15_NAME='SOROK-20261019-G15-G14-SEVEN-FAMILY-GENEALOGY-CAUSAL-REPAIR-R1'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
def main():
    replica=ROOT/'runs/replica/WORKER_RETURNS'/G15_NAME
    shutil.copytree(ROOT/'sources/g15',replica,dirs_exist_ok=True)
    for args in [[str(replica/'court_runner.py'),'baseline'],[str(replica/'final_validation.py')]]:
        subprocess.run([sys.executable,'-B',*args],cwd=REPO,env=ENV,check=True)
    # Original separate SGI1 epoch and both full retained-record audits.
    sys.path.insert(0,str(replica));import court_runner as cr
    dst=cr.stage('historical');court=dst/'reproduction/03_POSTREPAIR_COURT'
    shutil.copytree(replica/'frozen/g13/00_SOURCES/sgi1',court/'sources/sgi1',dirs_exist_ok=True)
    row=cr.run('preservation','sgi1_historical',court,['test_original_sgi1.py']);assert row['exit']==0
    cr.dump(replica/'execution/preservation/results.json',[row])
    for name,cwd in [('historical',court),('baseline',replica/'runs/baseline/reproduction/03_POSTREPAIR_COURT')]:
        p=subprocess.run([sys.executable,'-B','audit_replay.py'],cwd=cwd,env=ENV,capture_output=True,text=True)
        (replica/'execution/preservation'/('audit_'+name+'.txt')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
        cr.dump(replica/'execution/preservation'/('command_'+name+'.json'),dict(command=['python3','-B','audit_replay.py'],cwd=str(cwd.relative_to(replica)),exit=p.returncode))
        shutil.copyfile(cwd/'evidence/full_replay_audit.json',replica/'execution/preservation'/('full_replay_audit_'+name+'.json'))
    shutil.copytree(replica/'execution',ROOT/'execution/reproduced_g15',dirs_exist_ok=True)
    for epoch in ['baseline','candidate']:
        out=ROOT/'execution/historical_case_outputs'/epoch;out.mkdir(parents=True,exist_ok=True)
        for f in ['sgi1_actual.json','sgi1_replay.json','g12_observations.json','supplemental_actor_identity.json','supplemental_asymmetry.json']:
            shutil.copyfile(replica/'runs'/epoch/'reproduction/03_POSTREPAIR_COURT/evidence'/f,out/f)
    for script in ['review_runner.py','compatibility.py','verify_return.py']:
        subprocess.run([sys.executable,'-B',str(ROOT/script)],cwd=REPO,env=ENV,check=True)
    print('ALL COURTS REPRODUCED; EXPECTED HISTORICAL AND INDEPENDENT REDS RETAINED')
if __name__=='__main__':main()
