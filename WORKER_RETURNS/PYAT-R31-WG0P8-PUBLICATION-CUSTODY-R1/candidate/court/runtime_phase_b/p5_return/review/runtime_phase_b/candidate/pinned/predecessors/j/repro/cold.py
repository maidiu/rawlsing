from common import *
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner,UnitExecutionReceipt,ExecutorBinding
import os,subprocess
mode=sys.argv[1]
if mode=='orchestrate':
 logs={}
 for m in ('full1','full2','checkpoint','resume','shard0','shard1'):
  c=subprocess.run([sys.executable,__file__,m],capture_output=True,text=True)
  logs[m]={'exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr}
 a=json.loads((R/'observations/cold_full1.json').read_text());b=json.loads((R/'observations/cold_full2.json').read_text())
 resume=json.loads((R/'observations/cold_resume.json').read_text())
 shards=[json.loads((R/f'observations/cold_shard{i}.json').read_text()) for i in (0,1)]
 dump('cold_comparison.json',{'processes':logs,'cold_identical_receipts':a['receipts']==b['receipts'],'cold_identical_values':a['values']==b['values'],'cold_frontier25':len(a['frontier'])==len(b['frontier'])==25,'resume':resume,'shard_combined_unit_keys_match_full':sorted(x for sh in shards for x in sh['unit_keys'])==a['unit_keys'],'shard_values_match_full':{k:v for sh in shards for k,v in sh['values'].items()}==a['values'],'scope':'Reviewer exercised accepted prior_receipts API; candidate run_plan does not expose this. Shards have different manifest identities; no claim their receipts share original manifest.'})
 print('COLD_RESULT',json.dumps({'replay_equal':a['receipts']==b['receipts'],'resume_error':resume.get('consumer_error'),'shard_units':sum(len(sh['unit_keys']) for sh in shards)}));sys.exit(0)
p=plan()
if mode.startswith('shard'):
 ix=int(mode[-1]);p.manifest=w.BatchManifest(tuple(u for n,u in enumerate(p.manifest.units) if n%2==ix))
prior=[]
if mode=='resume':
 saved=json.loads((R/'observations/cold_checkpoint.json').read_text())
 for raw in saved['receipt_projections']:
  raw=dict(raw)
  for key in ('unit_ref','executor_ref'):
   if raw[key] is not None:raw[key]=w.ExactRef(**raw[key])
  for key in ('result_refs','provenance_refs'):raw[key]=tuple(w.ExactRef(**r) for r in raw[key])
  prior.append(UnitExecutionReceipt(**raw))
r=BatchExecutionRunner(manifest=p.manifest,repository=p.repository,prior_receipts=prior)
r.run(executors={'QUERY':ExecutorBinding(w._ref('EXECUTOR','wg0p2-query'),w.make_executor(p))},max_units=1 if mode=='checkpoint' else None)
rec=r.receipts
out={'pid':os.getpid(),'receipts':sorted(x.receipt_hash for x in rec),'receipt_projections':[x.projection() for x in rec],'summary':asdict(r.summary()),'frontier':p.frontier_receipts,'unit_keys':sorted(u.unit_ref.key for u in p.manifest.units),'fact_registry_size':len(p.fact_registry)}
try:out['values']=values(w.consumer_effects(p,rec))
except Exception as e:out['consumer_error']=type(e).__name__+': '+str(e)
# PID is separate so replay identities compare meaningfully.
dump('cold_'+mode+'.json',out)
if mode=='checkpoint':os._exit(23) # deliberate interrupted process AFTER durable JSON checkpoint
print(mode,'COMPLETED',len(rec))
