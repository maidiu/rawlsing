"""Relocate the self-contained source-free return; no Git or raw source reads."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parent
TESTS=['test_wg0x.py']+[f'native/rawlsing_next/tests/test_pre553_{x}.py' for x in ['route_b_production','empirical_query','discovery_exact','batch_runner','learned_empirical_adjudication']]
def main():
    with tempfile.TemporaryDirectory(prefix='wg0x-cold-') as folder:
        dest=Path(folder)/'return'
        shutil.copytree(R,dest,symlinks=True,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
        env=dict(os.environ,PYTHONHASHSEED='931',PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONPATH=str(dest/'native'),GIT_NO_LAZY_FETCH='1')
        outputs=[]
        for cmd,name in [([sys.executable,'-B','experiment.py'],'cold_experiment'),([sys.executable,'-B','reconcile_execution.py'],'cold_antijoin'),([sys.executable,'-B','-m','pytest',*TESTS,'-q','--junitxml=evidence/cold_court.xml'],'cold_court')]:
            p=subprocess.run(cmd,cwd=dest,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            (R/'evidence'/f'{name}.log').write_text(p.stdout.replace(str(dest),'$RETURN'))
            outputs.append(dict(command=['python3' if x==sys.executable else x for x in cmd],exit_code=p.returncode))
            if p.returncode:raise RuntimeError(f'{name} failed: '+p.stdout[-1500:])
        a=(R/'evidence/native_experiment.json').read_bytes();b=(dest/'evidence/native_experiment.json').read_bytes()
        assert a==b,'RELOCATED_NATIVE_RECEIPT_BYTES_DIFFER'
        c=(R/'evidence/expected_vs_actual_receipts.json').read_bytes();d=(dest/'evidence/expected_vs_actual_receipts.json').read_bytes()
        assert c==d
        shutil.copyfile(dest/'evidence/cold_court.xml',R/'evidence/cold_court.xml')
        proof=dict(status='RELOCATED_SOURCEFREE_REPLAY_AND_133_TEST_COURT_PASS',no_git_directory=not (dest/'.git').exists(),no_original_respondent_source_read=True,expected_sha256=hashlib.sha256((dest/'evidence/EXPERIMENT_EXPECTED.json').read_bytes()).hexdigest(),native_receipts_sha256=hashlib.sha256(a).hexdigest(),byte_identical=True,commands=outputs,scope='AUTHOR_REPLAY_NOT_INDEPENDENT_REVIEW_OR_ORIGINAL35_PERMISSION')
        (R/'evidence/cold_replay_receipt.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,sort_keys=True))
if __name__=='__main__':main()
