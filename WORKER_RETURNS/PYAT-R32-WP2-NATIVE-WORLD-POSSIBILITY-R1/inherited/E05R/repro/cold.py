"""Independent fresh interpreter reconstruction and old/fresh fixture grants."""
import os,sys,pathlib,json,copy
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';sys.path[:0]=list(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro']))
from court_support import *
mode=sys.argv[1]
results={};grants={}
for label in ['CURRENT_TEST_CLOCK','HISTORICAL_AS_OF','TYPED_PARTIAL_PRE_NCA_PUBLICATION']:
 a,q,s,acc,r=run(label=label);results[label]=dict(request=q.binding(),acceptance=acc.binding(),receipt=r)
# Fresh source grant/release constructed separately, not reuse of old process cache.
a,q,s,acc,base=run();fresh=adapter(empirical_changed=True);_,fq,fs,fa,fr=run(fresh);results['FRESH_EMPIRICAL_SOURCE']=dict(request=fq.binding(),acceptance=fa.binding(),receipt=fr)
try:fresh.service.possibilities(s)
except ValueError as e:grants['old_snapshot_on_fresh_source']=dict(refused=True,error=str(e))
else:grants['old_snapshot_on_fresh_source']=dict(refused=False)
for role in [GSS,NCA]:
 data=rows();next(x for x in data if x['role']==role)['status']='REVOKED_TEST_ONLY';a=adapter(data);_,q,s,acc,r=run(a);results['WITHDRAWN_'+role]=dict(request=q.binding(),acceptance=acc.binding(),receipt=r)
# Old fresh-use world revocation survives same-object reads; separately constructed
# fixture root restores only test-only use. There is no durable issuer/revocation store.
a,q,s,acc,r=run();a.invalidate('empirical');withdrawn=a.serve(q,acc,s,consumers=clients(a,s));b,bq,bs,ba,new=run();grants['reconstructed_fixture_after_local_revocation']=dict(old_state=withdrawn['state'],new_state=new['state'],same_permission_roots=withdrawn['permission_roots']==new['permission_roots'],new_issuer=new['new_issuer'],operative_OC05=new['operative_OC05'],interpretation='Fresh fixture construction resets in-memory revocation. This is test-only reconstruction, not a durable authority renewal guarantee.')
results=json.loads(json.dumps(results));grants=json.loads(json.dumps(grants))
out=dict(pid=os.getpid(),mode=mode,results=results,old_and_fresh_grants=grants)
if mode=='replay':
 prior=json.loads((O/'independent_cold_first.json').read_text());assert prior['pid']!=os.getpid()
 assert results==prior['results'];assert grants==prior['old_and_fresh_grants']
 out['replay_bit_identical']=True;out['first_pid']=prior['pid']
save('independent_cold_'+mode,out);print(json.dumps(dict(mode=mode,pid=os.getpid(),receipt_hashes={k:v['receipt']['receipt_hash'] for k,v in results.items()},old_and_fresh_grants=grants,replay_bit_identical=out.get('replay_bit_identical')),indent=2))
