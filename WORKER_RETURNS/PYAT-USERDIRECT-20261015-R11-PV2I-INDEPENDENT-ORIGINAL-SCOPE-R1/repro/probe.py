from common import *
import sys,platform,pytest
from collections import Counter
from dataclasses import asdict
calls=[];facts=[];releases=[];consumers=[]
interesting={'ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','execute_exact_bounded_discovery','run_integrated','execute_route_b_production','produce_exact_conditional_support_profile','replay_exact_conditional_support_profile','run_sourcefree_with_register'}
def trace(frame,event,arg):
 fn=frame.f_code.co_filename;name=frame.f_code.co_name
 if name not in interesting:return trace
 if event=='call':calls.append({'function':name,'file':fn,'line':frame.f_code.co_firstlineno})
 if event=='return' and arg is not None:
  if name=='execute_empirical_query':facts.extend([{'query':frame.f_locals['query'].ref.as_dict(),'predicate':frame.f_locals['predicate'].ref.as_dict(),'release_refs':[x.as_dict() for x in frame.f_locals['release_refs']],'fact':f.semantic_projection(),'ref':f.ref.as_dict()} for f in arg.facts])
  if name=='validate_c11_source_release':
   c=frame.f_locals['candidate'];releases.append({'accepted':type(arg).__name__=='C11LogicalRelease','release_ref':arg.release_ref.as_dict(),'source_manifest':str(c.source_release_manifest),'source_artifact_ref':arg.source_artifact_ref.as_dict(),'public':[x.semantic_projection() for x in (*c.empirical_universes,*c.respondent_events,*c.routing_eligibility_facts_or_exact_rules)],'respondents':[x.semantic_projection() for x in c.respondent_identities]})
  if name=='produce_exact_conditional_support_profile':consumers.append({'class':type(arg).__name__,'ref':arg.ref.as_dict() if hasattr(arg,'ref') else str(arg)})
 return trace
sys.settrace(trace);fx=F.pv2_sourcefree_fixture(RT/'probe_ledger_v3');report=run(fx);sys.settrace(None)
imports=[]
for n,m in sorted(sys.modules.items()):
 if n.startswith('rawlsing_next.') or n in ('pv2_original_scope_register','pv2_sourcefree_fixture') or n.startswith('a04'):
  path=getattr(m,'__file__',None)
  if not path or not Path(path).is_file():continue
  data=Path(path).read_bytes();imports.append({'module':n,'physical_file':path,'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'sha256':hashlib.sha256(data).hexdigest()})
dump('physical_baseline.json',{'versions':{'python':sys.version,'pytest':pytest.__version__,'platform':platform.platform()},'report':report,'calls':calls,'imports':imports,'C11_ingests':releases,'I03_facts':facts,'actual_Field_Forge_producer_returns':consumers,'durable_calls':[len(x) for x in fx['calls']],'input_source_rows':[{ 'namespace':x['universe'].respondent_namespace,'cells':[{'row':c.row_ordinal,'item':c.variable_name,'raw':c.raw_value} for c in x['fx']['stream'].cell_iter_factory()],'query':x['query'].semantic_projection(),'reverse_query':x['reverse_query'].semantic_projection()} for x in fx['inputs']]})
print('ACTUAL_CALLS',dict(Counter(c['function'] for c in calls)));print('LINKS',len(report['links']),'HELD',len(report['nonrunnable']))
