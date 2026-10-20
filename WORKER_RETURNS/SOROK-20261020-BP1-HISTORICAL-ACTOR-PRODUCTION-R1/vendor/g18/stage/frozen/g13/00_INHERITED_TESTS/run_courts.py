"""Keep literal exits/stdout/JUnit, including expected scientific REDs."""
from pathlib import Path
import subprocess,os,sys,time,json,hashlib
ROOT=Path(__file__).resolve().parent
def main():
    rows=[]
    suites=[('sgi1',['test_original_sgi1.py']),
            ('g11',['sources/g11/test_g11_solver.py']),
            ('g12_controls',['test_g12_controls.py']),
            ('g12_literal_contract',['test_g12_literal_contract.py']),
            ('g12_supplemental',['test_g12_supplemental.py']),
            ('candidate_boundary',['test_candidate_boundary.py'])]
    requested=set(sys.argv[1:])
    if requested:
        assert requested <= {label for label,_ in suites}
        prior=ROOT/'evidence/execution.json'
        if prior.exists():rows=[r for r in json.loads(prior.read_text()) if r['suite'] not in requested]
    for label,paths in suites:
        if requested and label not in requested:continue
        cmd=[sys.executable,'-m','pytest','-q','-s','-p','no:cacheprovider',*paths,'--junitxml=evidence/'+label+'_junit.xml']
        t=time.perf_counter()
        p=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        output=p.stdout+p.stderr;(ROOT/'evidence'/f'{label}_stdout.txt').write_text(output)
        row=dict(suite=label,command=['python3',*cmd[1:]],exit_status=p.returncode,wall_seconds=time.perf_counter()-t,
                 stdout=f'evidence/{label}_stdout.txt',junit=f'evidence/{label}_junit.xml',
                 stdout_sha256=hashlib.sha256(output.encode()).hexdigest())
        rows.append(row);print(json.dumps(row))
    (ROOT/'evidence/execution.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
