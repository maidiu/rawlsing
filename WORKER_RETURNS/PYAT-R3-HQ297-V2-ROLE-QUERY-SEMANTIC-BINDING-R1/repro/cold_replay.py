import json,os,pathlib,subprocess,sys,time,shutil
RET=pathlib.Path(__file__).resolve().parents[1]
if len(sys.argv)>1:
    from rawlsing_next.tests import test_hq297_v2r_role_query_binding as T
    from rawlsing_next.pre553_empirical_objects import ExactRef
    phase=sys.argv[1];ledger=pathlib.Path(sys.argv[2]);ledger.mkdir(exist_ok=True)
    previous=(ledger/'prospective_register.json').read_bytes() if phase=='replay' else None
    records,expected,plans,calls,register=T.fixture(ledger,held_bj=True)
    if previous is not None:assert previous==(ledger/'prospective_register.json').read_bytes()
    prior=None
    if phase=='replay':
        first=json.loads((RET/'repro/cold_first.json').read_text())
        prior={l['original_expected_work_key']:ExactRef(**l['consumer_ref']) for l in first['report']['links']}
    report=T.R.run_sourcefree(expected=expected,selected_scopes=plans,register=register,prior_consumer_refs=prior)
    assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==4
    assert [len(c) for c in calls]==([3,3] if phase=='first' else [0,0])
    if phase=='replay':assert report['links']==first['report']['links'] and report['nonrunnable']==first['report']['nonrunnable'] and report['register_digest']==first['report']['register_digest']
    (RET/'repro'/('cold_'+phase+'.json')).write_text(json.dumps(dict(phase=phase,calls=[len(c) for c in calls],report=report,fixture_reconstruction_executed=True),indent=2))
    print(phase,'six links four held', [len(c) for c in calls])
else:
    selector=json.loads((RET/'repro/selector_green.json').read_text());runtime=pathlib.Path(selector['runtime']);scratch=runtime/'WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1';ledger=runtime/'cold-v2r';results=[]
    for phase in ['first','replay']:
        cmd=[sys.executable,str(pathlib.Path(__file__).resolve()),phase,str(ledger)];t=time.time()
        env=dict(os.environ,PYTHONPATH=str(runtime),PV_RUNTIME=str(runtime),PV_RETURN=str(scratch),PV_SUITE='cold_'+phase,V2R_STAGE='green',V2R_RETURN=str(RET),PYTHONDONTWRITEBYTECODE='1')
        with (RET/'repro'/('cold_'+phase+'.log')).open('w') as f:r=subprocess.run(cmd,cwd=runtime,env=env,stdout=f,stderr=subprocess.STDOUT)
        results.append(dict(command=cmd,cwd=str(runtime),exit_code=r.returncode,seconds=time.time()-t));print((RET/'repro'/('cold_'+phase+'.log')).read_text())
    out=RET/'repro/audit_cold/child_audits';out.mkdir(parents=True,exist_ok=True)
    for p in (scratch/'repro/child_audits').glob('cold_*.json'):shutil.copyfile(p,out/p.name)
    (RET/'repro/cold_execution.json').write_text(json.dumps(results,indent=2))
