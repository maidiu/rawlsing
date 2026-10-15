from common import *
from collections import Counter
import sys
rows=[];names={'execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility'}
for mutation in ['numeric_stale_hash','numeric_rehashed','foreign_release_stale_hash','foreign_release_rehashed']:
 s,ss,a,b=full();key=('Y',(('A',1),));original=deepcopy(s.provider.cache[key]);anchor=s.provider._accepted[key];entry=s.provider.cache[key]
 if mutation.startswith('numeric'):entry['cells'][1]['raw_numerator_support']=999
 else:entry['release_ref']={'kind':'C11LogicalRelease','object_id':'urn:e04r:foreign-release','content_hash':'f'*64}
 if mutation.endswith('_rehashed'):entry['content_hash']=semantic_hash({k:v for k,v in entry.items() if k!='content_hash'})
 attacks=[]
 for label,call in [('nonparent',lambda:consume(s,ss)),('scenario',lambda:evaluate(s,ss,PROPOSALS))]:
  calls=Counter();start=len(s.value_reads);receipts=set(s.receipts)
  def trace(frame,event,arg):
   if event=='call' and frame.f_code.co_name in names:calls[frame.f_code.co_name]+=1
  sys.setprofile(trace)
  try:call()
  except ValueError as error:outcome=str(error)
  else:raise AssertionError('CORRUPT_CACHE_REACHED_CLIENT')
  finally:sys.setprofile(None)
  new=s.value_reads[start:];assert not any(x['channel']=='empirical' for x in new);assert set(s.receipts)==receipts
  attacks.append(dict(client=label,refusal=outcome,new_empirical_value_reads=0,new_product_receipts=0,actual_owner_entry_counts=dict(calls),structural_reads_permitted=sum(x['channel']=='structural' for x in new)))
 assert s.provider._accepted[key] is anchor
 assert s.historical_receipt(a['receipt_hash'])['material']==a['material']
 rows.append(dict(mutation=mutation,before=original,untrusted_after=entry,trusted_projection=json.loads(anchor.projection),immutable_owner_material=json.loads(anchor.native_owner_material),both_client_results=attacks,historical_receipt_preserved=True))
dump('two_RED_closure_probe.json',dict(schema='E04R_TWO_PRIOR_RED_NATIVE_CLOSURE@1',real_owner_generation=True,cases=rows,scope='SOURCEFREE_IMPLEMENTER_CANDIDATE_REQUIRES_DISTINCT_REVIEW'))
print('FOUR_MUTATIONS_REFUSED_IN_BOTH_REAL_CLIENTS_BEFORE_EMPIRICAL_READ')
