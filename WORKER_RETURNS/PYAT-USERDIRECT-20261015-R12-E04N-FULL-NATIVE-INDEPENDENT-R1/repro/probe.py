from common import *
import sys,platform,pytest,subprocess
from collections import Counter
calls=[];compositions=[];f8=[];facts=[];structural=[];held=[];rows=[]
names={'ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context'}
def trace(frame,event,arg):
 name=frame.f_code.co_name;file=frame.f_code.co_filename
 if name not in names:return trace
 if event=='call':
  calls.append({'function':name,'file':file,'line':frame.f_code.co_firstlineno})
  if name=='evaluate_positioned_subject_possibility':
   values=tuple(frame.f_locals['evidence']);held.extend(values);f8.append({'ids':[id(e) for e in values],'evidence_refs':[e.evidence_ref.as_dict() for e in values],'query_ref':frame.f_locals['query'].ref.as_dict()})
 if event=='return' and arg is not None:
  if name=='compose_positioned_subject_possibility' and hasattr(arg,'possibility_slice_evidence_or_null'):
   e=arg.possibility_slice_evidence_or_null
   if e is not None:held.append(e);compositions.append({'id':id(e),'evidence_ref':e.evidence_ref.as_dict(),'fact_ref':arg.producer_fact_ref.as_dict(),'query_ref':frame.f_locals['empirical_query'].ref.as_dict()})
  if name=='execute_empirical_query':facts.extend([{'ref':f.ref.as_dict(),'projection':f.semantic_projection()} for f in arg.facts])
  if name=='ingest_c11_source_release':
   candidate=frame.f_locals['candidate'];rows.append({'accepted':arg.accepted,'ref':arg.release_ref.as_dict() if arg.release_ref else None,'source_events':[x.semantic_projection() for x in candidate.respondent_events],'routing':[x.semantic_projection() for x in candidate.routing_eligibility_facts_or_exact_rules]})
 return trace
sys.settrace(trace);s,snap,a,b=full();reverse=s.possibilities(snap,target='A',conditions=[('Y',1)])
t,other,c,d=full(empirical_changed=True);u,us,e,f=full(structural_revision=True);v,vs,g,h=full(sanction_revision=True);z,zs,za,zb=full(support_loss=True);sys.settrace(None)
imports=[]
for name,mod in sorted(sys.modules.items()):
 file=getattr(mod,'__file__',None)
 if file and Path(file).is_file() and ('runtime_root' in file) and file.endswith('.py'):
  data=Path(file).read_bytes();imports.append({'module':name,'file':file,'git_blob_sha1':subprocess.check_output(['git','hash-object',file]).decode().strip(),'sha256':hashlib.sha256(data).hexdigest()})
# Concrete evidence object identity, not the adapter's trace boolean.
assert all(any(x['id'] in f['ids'] and x['evidence_ref'] in f['evidence_refs'] for f in f8) for x in compositions)
dump('full_native_probe.json',{'versions':{'python':sys.version,'pytest':pytest.__version__,'platform':platform.platform()},'actual_calls':calls,'call_counts':dict(Counter(c['function'] for c in calls)),'imports':imports,'composition_returns':compositions,'F8_actual_inputs':f8,'same_concrete_evidence_objects_verified':True,'I03_facts':facts,'C11_ingests':rows,'baseline':{'snapshot':snap.material,'snapshot_hash':snap.snapshot_hash,'nonparent':a,'scenario':b,'provider_trace':s.provider.trace,'world_trace':s.catalog.trace},'reverse':reverse,'empirical_mutation':{'nonparent':c,'scenario':d},'structural_mutation':{'nonparent':e,'scenario':f},'sanction_mutation':{'nonparent':g,'scenario':h},'zero_support':{'nonparent':za,'scenario':zb}})
print('REAL_NATIVE_CALLS',dict(Counter(c['function'] for c in calls)));print('EXACT_C1_EVIDENCE_OBJECTS_TO_F8',len(compositions));print('SOURCE_ROWS',len(independent_rows()))
