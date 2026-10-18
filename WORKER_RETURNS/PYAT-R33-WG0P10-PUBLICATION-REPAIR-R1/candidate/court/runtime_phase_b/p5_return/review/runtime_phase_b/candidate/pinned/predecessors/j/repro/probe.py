from common import *
import inspect,platform,pytest
from collections import Counter
calls=[]; returned=[];ingests=[]
def trace(frame,event,arg):
 name=frame.f_code.co_name; path=frame.f_code.co_filename
 if name in ('ingest_c11_source_release','execute_empirical_query','run','_commit_validated') and ('pre553_c11_ingest.py' in path or 'pre553_empirical_query.py' in path or 'pre553_batch_runner.py' in path or 'pre553_c11_repository.py' in path):
  if event=='call':
   calls.append({'function':name,'file':path,'line':frame.f_code.co_firstlineno})
   if name=='ingest_c11_source_release':
    c=frame.f_locals['candidate'];ingests.append({'source_manifest':{'source_artifact_id':c.source_release_manifest.source_artifact_id,'source_artifact_content_hash':c.source_release_manifest.source_artifact_content_hash,'declared_counts':dict(c.source_release_manifest.declared_record_counts_by_logical_family)},'weight_absence':asdict(c.weight_measure_facts_or_typed_absence)})
  if event=='return' and name=='execute_empirical_query' and arg is not None:
   returned.append({'query_ref':frame.f_locals['query'].ref.as_dict(),'release_refs':[r.as_dict() for r in frame.f_locals['release_refs']], 'facts':[{'ref':f.ref.as_dict(),'state':f.typed_state,'denominator':f.raw_denominator_support,'projection':f.target_topology['complete_cell_semantic_projection']} for f in arg.facts]})
 return trace
sys.settrace(trace);p=plan();runner,rs,e=execute(p);sys.settrace(None)
imports=[]
for name,m in sorted(sys.modules.items()):
 if name.startswith('rawlsing_next.') or name=='wg0p2_workload':
  path=Path(m.__file__);data=path.read_bytes();imports.append({'module':name,'file':str(path),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()})
releases=[]
for tag,rel in p.releases.items():
 r=rel.repo.resolve_release_exact(rel.release_ref)
 records=[{'type':type(o).__name__,'ref':o.ref.as_dict(),'payload':o.semantic_projection()} for o in (*r.public_objects,*r.internal_records)]
 releases.append({'tag':tag,'class':type(r).__name__,'ref':r.release_ref.as_dict(),'source_artifact':r.source_artifact_ref.as_dict(),'records':records})
dump('baseline.json',{'versions':{'python':sys.version,'pytest':pytest.__version__,'platform':platform.platform()},'imports':imports,'owner_calls':calls,'owner_query_returns':returned,'ingest_inputs':ingests,'one_repository':len({id(r.repo) for r in p.releases.values()})==1,'releases':releases,'frontier':p.frontier_receipts,'consumer':e,'receipts':[asdict(r) for r in rs],'summary':asdict(runner.summary())})
print('OWNER_CALLS',dict(Counter(c['function'] for c in calls)));print('BASELINE_RECORDED')
