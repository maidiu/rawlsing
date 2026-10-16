from common import *
from observer import Observer
cases=[]
for attack in ['F1_NUMERATOR_18_TO_999','F2_FOREIGN_C11_RELEASE']:
 for coherent in [False,True]:
  for client_name in ['nonparent','scenario']:
   s,ss,a,b=full();key=('Y',(('A',1),));before=deepcopy(s.provider.cache[key]);entry=s.provider.cache[key]
   if attack.startswith('F1'):next(c for c in entry['cells'] if c['cell']=='1')['raw_numerator_support']=999
   else:entry['release_ref']=dict(kind='C11LogicalRelease',object_id='urn:e04s:independent:foreign:release',content_hash='c'*64)
   if coherent:entry['content_hash']=semantic_hash({k:v for k,v in entry.items() if k!='content_hash'})
   obs=Observer();obs.start();start=len(s.value_reads)
   try:result=consume(s,ss) if client_name=='nonparent' else evaluate(s,ss,PROPOSALS)
   except ValueError as exc:error=str(exc)
   else:raise AssertionError('Original cache defect still serves '+client_name)
   finally:obs.stop()
   assert error=='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'
   reads=s.value_reads[start:];assert not any(r['channel']=='empirical' for r in reads)
   assert json.loads(s.provider._accepted[key].projection)==before
   cases.append(dict(attack=attack,coherently_rehashed=coherent,consumer=client_name,error=error,accepted_projection=before,hostile_projection=entry,reads_before_refusal=reads,actual_native_calls=obs.material()['counts'],private_owner_anchor_unchanged=True))
dump('F1_F2_exact_both_clients.json',dict(executed_controls=cases,control_count=len(cases),not_additional_pytest_cases=True))
print('F1/F2: all 8 exact stale/coherently-rehashed client controls refuse before empirical reads')
