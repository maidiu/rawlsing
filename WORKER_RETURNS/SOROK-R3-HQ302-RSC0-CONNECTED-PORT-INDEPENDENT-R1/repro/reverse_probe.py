"""Actual reverse-path calls versus independent pinned reverse positive control."""
import json, os, pathlib, sys
import port.pinned_producer as P
from port.adapter import TwoContractAdapter
from port.provider_a import ProviderA
from port.provider_b import ProviderB
from port.world_baseline import REVERSAL_GRANT_SCOPED
from rawlsing_next.tests import n10e_empirical_slice_fixture as FX
codes={P._N10E.provide_empirical_possibility_slice.__code__:'N10E',P._C1.compose_positioned_subject_possibility.__code__:'C1',P._PE.serve_generic_world_situated_possibility.__code__:'PE'}
def trace_run(fn):
 calls={k:0 for k in ['N10E','C1','PE']};prior=sys.gettrace()
 def trace(frame,event,arg):
  if event=='call' and frame.f_code in codes:calls[codes[frame.f_code]]+=1
  return trace
 sys.settrace(trace)
 try:result=fn()
 finally:sys.settrace(prior)
 return result,calls
rows=[]
for provider in [ProviderA,ProviderB]:
 p=provider();bundle=TwoContractAdapter(p).run()
 result,calls=trace_run(lambda:p.request_role_reversal(bundle['world_receipt'],bundle['possibility_receipt'],REVERSAL_GRANT_SCOPED))
 rows.append(dict(provider=provider.__name__,actual_reverse_calls=calls,result=result))
case=FX.build_provider_case('reverse')
result,calls=trace_run(lambda:P._N10E.provide_empirical_possibility_slice(repository=case['source']['repo'],empirical_query=case['empirical_query'],predicate=case['predicate'],authority_registry=case['registry'],release_refs=case['release_refs'],consumer_query=case['consumer_query'],model_rule=case['model_rule'],condition_binding_witness=case['condition_binding_witness']))
obj=dict(schema='RSC0_REVERSE_EXECUTION_CONTROL@1',candidate_reverse_paths=rows,positive_control=dict(actual_calls=calls,geometry=result.generated_evidence_or_null.geometry),interpretation='Candidate reverse only hashes/copies caller grant values. Pinned control actually computes54/62; equal baseline numbers do not prove independent issuance.')
assert all(not any(x['actual_reverse_calls'].values()) for x in rows)
assert calls=={'N10E':1,'C1':1,'PE':0}
assert result.generated_evidence_or_null.geometry['denominator']['raw_denominator_support']==62
(pathlib.Path(os.environ['RSC0_RETURN'])/'repro/reverse_connection_probe.json').write_text(json.dumps(obj,indent=2,default=str)+'\n')
print('ACTUAL_CANDIDATE_REVERSE_OWNER_CALLS_ZERO_BOTH; POSITIVE_CONTROL_N10E1_C11_DENOMINATOR62')
