"""Reviewer OS boundary: genuine accepted receipts, measured durable checkpoint."""
import json, os, pathlib, stat, sys
from dataclasses import asdict
from phase_b_support_v1 import w,plan,rows,builder,dump,profile_calls
mode=sys.argv[1];folder=pathlib.Path(sys.argv[2]);folder.mkdir(parents=True,exist_ok=True)
calls=[];sys.setprofile(profile_calls(calls))
try:
 owner=w.FixtureOwner.provision(folder/'owner',w.COHORTS) if mode in ('crash','full','shard0','shard1') else w.FixtureOwner(folder/'owner')
 p=plan(releases=w.build_all_releases(fixture_owner=owner))
 if mode in ('full','shard0','shard1'):
  if mode=='full':
   runner,rs=w.run_plan(p,w.make_executor(p))
  else:
   selected={u.unit_ref.key for n,u in enumerate(p.manifest.units) if n%2==int(mode[-1])}
   executor=w.make_executor(p)
   from rawlsing_next.pre553_batch_runner import BatchDeferred
   def shard_executor(u):
    if u.unit_ref.key not in selected:raise BatchDeferred('OTHER_REVIEWER_PARTITION')
    return executor(u)
   runner=w.BatchExecutionRunner(manifest=p.manifest,repository=p.repository)
   runner.run(executors={'QUERY':w.ExecutorBinding(w.EXECUTOR_REF,shard_executor)})
   rs=runner.receipts; p.fixture_owner._record_native_batch_receipts(rs)
  consumer=w.consumer_effects(p,rs);sys.setprofile(None)
  dump(folder/'full.json',{'pid':os.getpid(),'manifest':p.manifest.manifest_hash,'frontier':list(p.frontier_receipts),'receipts':[w.receipt_to_json(r) for r in rs],'consumer':consumer,'unit_keys':sorted(r.unit_ref.key for r in rs if r.state=='COMPLETED'),'summary':asdict(runner.summary()),'calls':calls})
 elif mode=='crash':
  runner,rs=w.run_plan(p,w.make_executor(p),max_units=1)
  if len(rs)!=1 or rs[0].state!='COMPLETED':raise RuntimeError('not a genuine one-unit checkpoint')
  cp=w.create_checkpoint(p,rs);durable=[]
  fsync=os.fsync;replace=os.replace
  def measured_fsync(fd):
   durable.append({'call':'fsync','kind':'directory' if stat.S_ISDIR(os.fstat(fd).st_mode) else 'file'});return fsync(fd)
  def measured_replace(a,b):
   durable.append({'call':'replace','source':str(a),'target':str(b)});return replace(a,b)
  os.fsync=measured_fsync;os.replace=measured_replace
  w.atomic_write(folder/'checkpoint.json',cp.to_json().encode())
  os.fsync=fsync;os.replace=replace
  dump(folder/'crash.json',{'pid':os.getpid(),'manifest':p.manifest.manifest_hash,'unit_count':len(p.manifest.units),'receipt':w.receipt_to_json(rs[0]),'receipt_class':type(rs[0]).__module__+'.'+type(rs[0]).__name__,'frontier':list(p.frontier_receipts),'calls':calls,'durability_calls':durable,'summary':asdict(runner.summary())})
  os._exit(23)
 else:
  cp=w.ColdCheckpoint.from_json((folder/'checkpoint.json').read_text(),fixture_owner=owner)
  native=w.receipt_from_json(cp.prior_receipts[0])
  result=w.resume_plan(p,cp,w.make_executor(p));sys.setprofile(None)
  out={'pid':os.getpid(),'manifest':p.manifest.manifest_hash,'unit_count':len(p.manifest.units),'receipts':[w.receipt_to_json(r) for r in result['receipts']],'restored_receipt':w.receipt_to_json(native),'receipt_class':type(native).__module__+'.'+type(native).__name__,'frontier':list(p.frontier_receipts),'consumer':result['consumer'],'remaining':result['remaining_units'],'calls':calls,'summary':asdict(result['summary']),'attempted':True,'exception_type':None,'typed_state':None,'served_positive':bool(result['consumer'])}
  dump(folder/('resume.json' if mode=='resume' else 'attack.json'),out)
except (w.IdentityError,w.ColdRestartError,w.RevocationError,w.FrontierError,KeyError,ValueError) as e:
 sys.setprofile(None)
 dump(folder/'attack.json',{'pid':os.getpid(),'attempted':True,'exception_type':type(e).__name__,'reason':str(e),'typed_state':None,'served_positive':False,'calls':calls})
 if mode in ('crash','resume','full','shard0','shard1'):raise
