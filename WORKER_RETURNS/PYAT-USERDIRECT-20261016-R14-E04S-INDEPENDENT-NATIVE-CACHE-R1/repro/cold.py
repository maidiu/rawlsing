"""Fresh interpreter replay plus cross-process cache and grant controls."""
from common import *
import sys,os
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
mode=sys.argv[1];out={}
for label,options in [('base',{}),('changed',dict(empirical_changed=True)),('historical',dict(structural_revision=True)),('zero',dict(support_loss=True))]:
 s=GenericSelectedWorldService(**options)
 ss=s.select(valid_at='2026-06-01',published_asof='2026-03-01') if label=='historical' else s.select()
 a=consume(s,ss);b=evaluate(s,ss,PROPOSALS);out[label]=dict(snapshot=ss.material,nonparent=a,scenario=b)
s,ss,a,b=full();rev=s.invalidate('empirical');denied=consume(s,ss);rebuilt=GenericSelectedWorldService();rs=rebuilt.select();rebuilt_product=consume(rebuilt,rs)
out['fixture_grants']=dict(withdrawn_state=denied['material']['empirical']['state'],archive=s.historical_receipt(a['receipt_hash']),fresh_fixture_state=rebuilt_product['material']['empirical']['state'],interpretation='Independent fresh fixture construction resets local revocations; no durable authority renewal guarantee or competent source rights')
# Capture a projection in the first interpreter and inject that exact serialized
# material into a fresh second process which has never produced its attestation.
cache_file=R/'observations/cross_process_cache.json'
if mode=='first':cache_file.write_text(json.dumps(rebuilt.provider.cache[('Y',(('A',1),))],indent=2)+'\n')
else:
 fresh=GenericSelectedWorldService();fs=fresh.select();fresh.provider.cache[('Y',(('A',1),))]=json.loads(cache_file.read_text())
 try:fresh.possibilities(fs)
 except ValueError as e:out['foreign_process_cache']=dict(refused=True,message=str(e))
 else:out['foreign_process_cache']=dict(refused=False)
 assert out['foreign_process_cache']['refused']
 fresh.provider.cache.clear();assert consume(fresh,fs)==rebuilt_product
# Current authority registry withdrawal differs from fresh producer outcome.
active,asnap,aa,ab=full();active.provider.world['registry']=AuthorityRegistry(active.provider.world['source']['authorities'])
hit=consume(active,asnap);active.provider.cache.clear();miss=consume(active,asnap)
out['authority_lifecycle']=dict(cached_state=hit['material']['state'],cached_empirical=hit['material']['empirical'],recomputed_state=miss['material']['state'],recomputed_empirical=miss['material']['empirical'],authority_missing=True)
normalized=json.loads(json.dumps(out));record=dict(pid=os.getpid(),mode=mode,results=normalized)
if mode=='replay':
 prior=json.loads((R/'observations/cold_first.json').read_text());assert prior['pid']!=os.getpid()
 # Cross-process injection is only performed by replay, all common results
 # compare exactly, including the independently observed RED lifecycle witness.
 compare=dict(normalized);compare.pop('foreign_process_cache')
 assert compare==prior['results'];record['replay_bit_identical']=True;record['first_pid']=prior['pid']
dump('cold_'+mode+'.json',record);print('COLD',mode,os.getpid(),record.get('replay_bit_identical'))
