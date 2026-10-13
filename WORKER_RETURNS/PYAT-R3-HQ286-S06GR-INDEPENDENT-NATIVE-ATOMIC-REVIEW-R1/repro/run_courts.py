"""Run exact bounded source-free courts and retain exits/commands/JUnit.
Baseline overlays ONLY the two old Python owners, never modifies working owners.
"""
import datetime, hashlib, json, os, pathlib, subprocess, sys, tempfile
root=pathlib.Path(__file__).resolve().parents[3]
out=pathlib.Path(__file__).resolve().parent
own='rawlsing_next/tests/test_hq286_s06gr_independent_atomic_review.py'
prior='WORKER_RETURNS/PYAT-R3-HQ285-S06G-NATIVE-ATOMIC-INTEGRITY-REPAIR-R1/repro/reviewer_overlay/test_hq284_s06fr_native_review.py'
accepted=['rawlsing_next/tests/'+p for p in ('test_pre553_s06f_native_owner_security.py','test_pre553_learned_product_lifecycle.py','test_pre553_learned_product_release.py','test_pre553_s06g_atomic_integrity.py','test_pre553_ee14_selected_current_asof_hq260.py','test_pre553_learned_world_composition.py')]
records=json.loads((out/'executions.json').read_text()) if (out/'executions.json').exists() else []
def run(label,paths,env=None,extra=()):
    cmd=[sys.executable,'-m','pytest',*paths,'-q','-p','no:cacheprovider','--import-mode=importlib',f'--junitxml={out / (label+".xml")}',*extra]
    proc=subprocess.run(cmd,cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1',**(env or {})},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/(label+'.log')).write_text(proc.stdout)
    record=dict(label=label,command=cmd,cwd=str(root),env=env or {},exit=proc.returncode,timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    records.append(record);print(label,proc.returncode,proc.stdout.splitlines()[-1],flush=True)
    (out/'executions.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':
    baseline='1b5b6072f855a74864c82d0f1b3923327bfb8b99'
    with tempfile.TemporaryDirectory(prefix='baseline_',dir=out) as tmp:
        pkg=pathlib.Path(tmp)/'rawlsing_next';pkg.mkdir()
        (pkg/'__init__.py').write_text('__path__.append('+repr(str(root/'rawlsing_next'))+')\n')
        identities={}
        for name in ('pre553_learned_product_lifecycle.py','pre553_learned_product_release.py'):
            data=subprocess.check_output(['git','show',f'{baseline}:rawlsing_next/{name}'],cwd=root)
            (pkg/name).write_bytes(data);identities[name]=hashlib.sha256(data).hexdigest()
        (out/'baseline_owners.json').write_text(json.dumps(dict(sha=baseline,files=identities),indent=2)+'\n')
        # Execute through -c so worktree cwd cannot preempt the temporary package.
        code=f"import sys; sys.path.insert(0,{tmp!r}); import rawlsing_next.pre553_learned_product_lifecycle as b; import rawlsing_next.pre553_learned_product_release as m; print('BASELINE_LOADED',b.__file__,m.__file__,flush=True); assert b.__file__.startswith({tmp!r}); import pytest; raise SystemExit(pytest.main(sys.argv[1:]))"
        cmd=[sys.executable,'-c',code,str(root/own),'-q','-p','no:cacheprovider','--import-mode=importlib',f'--junitxml={out / "independent_before_final.xml"}']
        proc=subprocess.run(cmd,cwd=root,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (out/'independent_before_final.log').write_text(proc.stdout)
        records.append(dict(label='independent_before_final',command=cmd,cwd=str(root),exit=proc.returncode,baseline=baseline,overlay='two exact owners with package path fallback; recreate via this runner',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        print('independent_before',proc.returncode,proc.stdout.splitlines()[-1],flush=True)
    run('independent_after_final',[own])
    run('unfiltered_final',accepted+[prior,own])
