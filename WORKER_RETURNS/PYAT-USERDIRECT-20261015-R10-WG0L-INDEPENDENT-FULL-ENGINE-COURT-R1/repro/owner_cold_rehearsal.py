"""Real accepted owner API rehearsal, not candidate WG0P4 cold qualification.
Independent harness restores exact historical sourcefree fact JSON. It does not
issue any source permission or claim candidate implements this restoration.
"""
from pathlib import Path
from dataclasses import asdict
import sys,os,json,subprocess,hashlib
import wg0p2_workload as w
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner,UnitExecutionReceipt,ExecutorBinding
R=Path(__file__).resolve().parents[1];D=R/'observations';mode=sys.argv[1]
def build():
 b=w.WorkloadBuilder();items=w.independent_oracle_items()
 for item in items:assert b.add_item(item)=='OK'
 return w.build_executable_plan(b.enumerate(),w.build_all_releases(),freeze_hash=b.freeze(),items_by_id={i.item_id:i for i in items})
def atomic(path,obj):
 data=json.dumps(obj,sort_keys=True).encode();tmp=path.with_suffix('.tmp')
 with tmp.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path);fd=os.open(str(path.parent),os.O_RDONLY)
 try:os.fsync(fd)
 finally:os.close(fd)
 return hashlib.sha256(data).hexdigest()
if mode=='orchestrate':
 first=subprocess.run([sys.executable,__file__,'checkpoint'],capture_output=True,text=True)
 assert first.returncode==23,(first.returncode,first.stderr)
 cp=D/'owner_rehearsal_checkpoint.json';anchor=hashlib.sha256(cp.read_bytes()).hexdigest()
 second=subprocess.run([sys.executable,__file__,'resume',anchor],capture_output=True,text=True);assert second.returncode==0,second.stderr
 result=json.loads((D/'owner_rehearsal_resume.json').read_text());result['checkpoint_exit']=first.returncode;result['subprocesses']=[{'argv':[sys.executable,__file__,'checkpoint'],'exit':first.returncode,'stdout':first.stdout,'stderr':first.stderr},{'argv':[sys.executable,__file__,'resume',anchor],'exit':second.returncode,'stdout':second.stdout,'stderr':second.stderr}]
 atomic(D/'owner_cold_rehearsal.json',result);print('REAL_OWNER_ORIGINAL_MANIFEST_COLD_REHEARSAL_PASS; NOT_WG0P4');sys.exit(0)
p=build();prior=[];old=None
if mode=='resume':
 data=(D/'owner_rehearsal_checkpoint.json').read_bytes();assert hashlib.sha256(data).hexdigest()==sys.argv[2];old=json.loads(data)
 assert p.manifest.manifest_ref.as_dict()==old['manifest']
 assert p.frontier_receipts==tuple(old['frontier'])
 for raw in old['receipt_preimages']:
  fields={k:v for k,v in raw.items() if k not in ('receipt_hash','receipt_ref')}
  for key in ('unit_ref','executor_ref'):
   if fields[key] is not None:fields[key]=w.ExactRef(**fields[key])
  for key in ('result_refs','provenance_refs'):fields[key]=tuple(w.ExactRef(**x) for x in fields[key])
  receipt=UnitExecutionReceipt(**fields);assert receipt.receipt_hash==raw['receipt_hash'];prior.append(receipt)
 p.fact_registry=json.loads(json.dumps(old['fact_registry'])) # explicitly REVIEWER harness custody transport
 for ref in prior[0].result_refs:assert ref.key in p.fact_registry
calls=[]
def profiler(frame,event,arg):
 if event=='call' and frame.f_code.co_name=='execute_empirical_query' and frame.f_code.co_filename.endswith('pre553_empirical_query.py'):calls.append(frame.f_code.co_filename)
sys.setprofile(profiler)
r=BatchExecutionRunner(manifest=p.manifest,repository=p.repository,prior_receipts=prior)
r.run(executors={'QUERY':ExecutorBinding(w._ref('EXECUTOR','wg0p2-query'),w.make_executor(p))},max_units=1 if mode=='checkpoint' else None)
sys.setprofile(None);rs=r.receipts
out={'pid':os.getpid(),'manifest':p.manifest.manifest_ref.as_dict(),'manifest_units':len(p.manifest.units),'frontier':p.frontier_receipts,'receipt_preimages':[x.projection()|{'receipt_hash':x.receipt_hash,'receipt_ref':x.receipt_ref.as_dict()} for x in rs],'fact_registry':p.fact_registry,'I03_calls':len(calls),'summary':asdict(r.summary())}
if mode=='checkpoint':
 assert len(rs)==1 and len(calls)==1
 atomic(D/'owner_rehearsal_checkpoint.json',out);os._exit(23)
e=w.consumer_effects(p,rs)
out.update({'qualification':'PHASE_A_ACCEPTED_OWNER_API_REHEARSAL_WITH_EXPLICIT_REVIEWER_FACT_RESTORE; NOT_WG0P4_PRODUCT','first_pid':old['pid'],'second_pid':os.getpid(),'first_I03_calls':old['I03_calls'],'second_I03_calls':len(calls),'manifest_before':old['manifest'],'manifest_after':p.manifest.manifest_ref.as_dict(),'original_receipt_hash':old['receipt_preimages'][0]['receipt_hash'],'final_receipt_hashes':[x.receipt_hash for x in rs],'owner_receipt_class':type(rs[0]).__module__+'.'+type(rs[0]).__name__,'fsync_file':True,'fsync_directory':True,'atomic_replace':True,'original_receipt_preimage_verified':True,'all_original_results_resolved':len(e)==3,'consumer':e,'permission_limit':'Historical fixture token only; current independent trusted grant, edition/clock, candidate restore all pending PhaseB'})
assert len(calls)==2 and len(rs)==3 and len(e)==3 and old['pid']!=os.getpid()
assert old['receipt_preimages'][0]['receipt_hash'] in out['final_receipt_hashes']
atomic(D/'owner_rehearsal_resume.json',out)
