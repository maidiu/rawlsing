"""New independent RED: live native-grant loss, cache-hit/miss contrast."""
from common import *
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from observer import Observer
from collections import Counter
obs=Observer(detailed=True);obs.start()
s,ss,a,b=full();w=s.provider.world;original_binding=s.provider._identity();query_ref=w['qauth'].authority_ref.as_dict()
original_authority=w['registry'].resolve_exact(w['qauth'].authority_ref).snapshot.as_dict()
w['registry']=AuthorityRegistry(w['source']['authorities'])
assert s.provider._identity()==original_binding
try:w['registry'].resolve_exact(w['qauth'].authority_ref)
except ValueError as exc:withheld=dict(refused=True,error=type(exc).__name__,message=str(exc))
else:raise AssertionError('Control query authority still present')
results={}
def phase_calls(before):return [dict(file=k[0],line=k[1],function=k[2],count=v-before.get(k,0)) for k,v in obs.counts.items() if v>before.get(k,0)]
for name,call in [('nonparent',lambda:consume(s,ss)),('scenario',lambda:evaluate(s,ss,PROPOSALS))]:
 start=len(s.value_reads);before=dict(obs.counts);prior=set(s.receipts)
 try:out=call();results[name]=dict(returned=True,state=out['material']['state'],empirical=out['material']['empirical'],product=out)
 except ValueError as e:results[name]=dict(returned=False,error=type(e).__name__,message=str(e))
 results[name].update(new_reads=s.value_reads[start:],actual_native_call_delta=phase_calls(before),new_receipts=sorted(set(s.receipts)-prior))
s.provider.cache.clear();before=dict(obs.counts)
try:out=s.possibilities(ss);results['cache_miss']=dict(returned=True,result=out)
except ValueError as e:results['cache_miss']=dict(returned=False,error=type(e).__name__,message=str(e))
results['cache_miss']['actual_native_call_delta']=phase_calls(before)
obs.stop();results.update(required_query_authority=query_ref,original_authority=original_authority,withheld_registry_exact_resolution=withheld,original_request_and_source_binding_unchanged=True,actual=obs.material(),interpretation='Attached native query grant unavailable, not a competent real-world issuer revocation. Hit still certifies numbers; fresh native production returns typed UNAVAILABLE without numeric support.')
assert results['nonparent']['returned'] and results['scenario']['returned']
assert not results['nonparent']['actual_native_call_delta'] and not results['scenario']['actual_native_call_delta']
assert all(x['state']=='UNAVAILABLE' and x['denominator']==0 and x['cells']==[] for x in results['cache_miss']['result']['steps'])
assert any(x['function']=='execute_empirical_query' for x in results['cache_miss']['actual_native_call_delta'])
dump('authority_registry_withdrawal_probe.json',results)
print('LIVE_REGISTRY_QUERY_GRANT_UNAVAILABLE__CACHED_BOTH_CLIENTS_PRODUCTIVE__FRESH_NATIVE_UNAVAILABLE')
print('cached owner calls',0,'fresh owner calls',sum(x['count'] for x in results['cache_miss']['actual_native_call_delta']))
