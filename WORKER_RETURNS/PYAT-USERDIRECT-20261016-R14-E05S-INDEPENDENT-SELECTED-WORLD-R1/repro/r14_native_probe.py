"""Read-only actual-frame observer, including concrete C1 -> F8 objects."""
import sys,pathlib,json,collections
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime'
sys.path[:0]=list(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro']))
from court_support import *
held=[];compositions=[];f8=[];calls=[];client_calls=[];ingests=[];facts=[]
names={'ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','read_historical_test_only','consume','evaluate'}
def profile(frame,event,arg):
 name=frame.f_code.co_name;file=frame.f_code.co_filename
 if name not in names or str(RT) not in file:return
 if event=='call':
  calls.append(dict(function=name,file=file,line=frame.f_code.co_firstlineno))
  if name=='evaluate_positioned_subject_possibility':
   es=tuple(frame.f_locals['evidence']);held.extend(es);f8.append(dict(ids=[id(e) for e in es],refs=[e.evidence_ref.as_dict() for e in es]))
  if frame.f_globals.get('__name__') in ('product.nonparent','product.scenario'):
   snap=frame.f_locals['snapshot'];client_calls.append(dict(module=frame.f_globals['__name__'],function=name,snapshot_id=id(snap),snapshot_hash=snap.snapshot_hash))
 if event=='return' and arg is not None:
  if name=='compose_positioned_subject_possibility':
   e=arg.possibility_slice_evidence_or_null
   if e is not None:
    held.append(e);compositions.append(dict(id=id(e),evidence_ref=e.evidence_ref.as_dict(),fact_ref=arg.producer_fact_ref.as_dict(),query_ref=frame.f_locals['empirical_query'].ref.as_dict()))
  elif name=='ingest_c11_source_release':
   ingests.append(dict(accepted=arg.accepted,events=[e.semantic_projection() for e in frame.f_locals['candidate'].respondent_events]))
  elif name=='execute_empirical_query':facts.extend(dict(ref=f.ref.as_dict(),projection=f.semantic_projection()) for f in arg.facts)
sys.setprofile(profile)
results={}
for label,kwargs in [('CURRENT_TEST_CLOCK',{}),('HISTORICAL_AS_OF',{}),('TYPED_PARTIAL_PRE_NCA_PUBLICATION',{}),('ZERO_SUPPORT',{'support_loss':True})]:
 a=adapter(**kwargs);q=E.standard_request(label='CURRENT_TEST_CLOCK' if label=='ZERO_SUPPORT' else label);s=a.build_snapshot(q);acc=a.accept(q,s);supplied=clients(a,s);r=a.serve(q,acc,s,consumers=supplied)
 for c in r['consumers']:assert c['consumer_material']['empirical']['steps']==r['empirical_steps']
 results[label]=dict(snapshot_id=id(s),snapshot=s.material,receipt=r,source_identity=acc.empirical_source_identity)
sys.setprofile(None)
assert compositions and all(any(c['id'] in x['ids'] and c['evidence_ref'] in x['refs'] for x in f8) for c in compositions)
assert all({c['module'] for c in client_calls if c['snapshot_id']==r['snapshot_id']}=={'product.nonparent','product.scenario'} for r in results.values())
save('r14_actual_native_probe',dict(results=results,calls=calls,counts=dict(collections.Counter(c['function'] for c in calls)),concrete_composition_returns=compositions,actual_f8_inputs=f8,same_concrete_evidence_verified=True,client_calls=client_calls,C11_ingests=ingests,I03_facts=facts,method='sys.setprofile frame observation; original functions unchanged; strong evidence references held against id reuse'))
print(json.dumps(dict(counts=dict(collections.Counter(c['function'] for c in calls)),same_concrete_C1_F8=len(compositions),client_calls=len(client_calls),C11_ingests=len(ingests))))
