"""Actual OS worker. Crash occurs after fsync of one genuine native receipt."""
import json,os,pathlib,sys
from dataclasses import asdict
from common_v1 import w,plan,values
mode,directory=sys.argv[1:];d=pathlib.Path(directory);d.mkdir(parents=True,exist_ok=True)
if mode=='crash':owner=w.FixtureOwner.provision(d/'trusted_fixture_owner',w.COHORTS)
else:owner=w.FixtureOwner(d/'trusted_fixture_owner')
p=plan(releases=w.build_all_releases(fixture_owner=owner))
calls=[]
def trace(frame,event,arg):
    if event=='call' and frame.f_code.co_name in ['execute_empirical_query','run'] and 'pinned/rawlsing_next/' in frame.f_code.co_filename:calls.append({'function':frame.f_code.co_name,'module':pathlib.Path(frame.f_code.co_filename).name})
sys.settrace(trace)
if mode=='crash':
    runner,rs=w.run_plan(p,w.make_executor(p),max_units=1)
    assert len(rs)==1 and rs[0].state=='COMPLETED' and runner.summary().completed_units==1
    cp=w.create_checkpoint(p,rs)
    w.atomic_write(d/'checkpoint.json',cp.to_json().encode())
    w.atomic_write(d/'crash_proof.json',w.canonical({'pid':os.getpid(),'manifest':p.manifest.manifest_hash,'unit_count':len(p.manifest.units),'receipts':[w.receipt_to_json(r) for r in rs],'summary':asdict(runner.summary()),'source_frontier_root':p.science_root,'actual_calls':calls,'exit':23,'fsync_atomic_replace_and_directory_fsync':True}))
    os._exit(23)
elif mode=='resume':
    cp=w.ColdCheckpoint.from_json((d/'checkpoint.json').read_text(),fixture_owner=owner)
    result=w.resume_plan(p,cp,w.make_executor(p));sys.settrace(None)
    payload={'pid':os.getpid(),'manifest':p.manifest.manifest_hash,'unit_count':len(p.manifest.units),'source_frontier_root':p.science_root,'summary':asdict(result['summary']),'receipts':[w.receipt_to_json(r) for r in result['receipts']],'values':values(result['consumer']),'remaining_executed':result['remaining_units'],'actual_calls':calls,'current_grant':'INDEPENDENT_TEST_ONLY_FIXTURE_OWNER','checkpoint_fact_count':result['restored_facts']}
    w.atomic_write(d/'resume_proof.json',w.canonical(payload));print(json.dumps(payload))
else:raise SystemExit('Unknown worker mode')
