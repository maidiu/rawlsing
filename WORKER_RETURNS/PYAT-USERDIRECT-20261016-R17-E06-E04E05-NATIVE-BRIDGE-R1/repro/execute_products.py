from bootstrap import ROOT,RT
from support import *
from observe import Observer
from collections import defaultdict,Counter
from rawlsing_next.pre553_empirical_objects import semantic_hash
import hashlib,datetime
obs=Observer();obs.start();products={}
b=bridge();p=b.prepare(request());products['CURRENT']=b.read(p)
products['HISTORICAL']=b.execute(request('HISTORICAL_AS_OF'))
products['Y_CHANGED']=bridge(empirical_changed=True).execute(request())
products['ZERO_SUPPORT']=bridge(support_loss=True).execute(request())
products['REVERSE']=b.execute(request(target='A',conditions=(('Y',1),)),scalar_only=True)
products['PRE_NCA_PUBLICATION']=bridge().execute(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION'))
# Cross-boundary query grant loss on a still-warm cache with same acceptance.
life=bridge();lp=life.prepare(request());before=life.read(lp);w=life.provider.world
persisted=dict(schema='E06_TRUSTED_FIXTURE_CURRENT_GRANTS@1',permission_grade='TEST_ONLY_NO_EXTERNAL_USE_GRANT',grants=[x.as_dict() for x in grants(w)],projection=deepcopy(life.provider.cache[('Y',(('A',1),))]))
cache_before=deepcopy(life.provider.cache);accepted_before=dict(life.provider._accepted);archive=life.archive(before)
w['registry']=AuthorityRegistry(w['source']['authorities']);withdrawn=life.read(lp)
# Current use after withdrawal is typed, old archive retains its exact bytes.
assert life.archive(before)==archive
w['registry']=AuthorityRegistry(hydrate(x) for x in reversed(persisted['grants']));restored=life.read(lp)
products['QUERY_GRANT_LIFECYCLE']=dict(before=before,withdrawn=withdrawn,restored=restored,archive=archive,warm_cache_keys_before=[repr(k) for k in cache_before],accepted_anchors_before=len(accepted_before),warm_query_grant_validations_before=before['native_query_validation_count'],same_acceptance=before['acceptance']==restored['acceptance'])
selective={}
for role in [GSS,NCA]:
 n=bridge();np=n.prepare(request());a=n.read(np);rr=rows();next(x for x in rr if x['role']==role)['status']='REVOKED_TEST_ONLY';n.adapter.registry=TestOnlyRegistry(rr);z=n.read(np)
 selective[role]=dict(before=a,after=z,archive=n.archive(a))
products['SELECTIVE_NATIVE_REVOCATION']=selective
explicit={}
for role in [GSS,NCA]:
 n=bridge();np=n.prepare(request());a=n.read(np);invalidation=n.adapter.invalidate(role);z=n.read(np)
 explicit[role]=dict(before=a,after=z,invalidation=invalidation)
products['SELECTIVE_NATIVE_EXPLICIT_WITHDRAWAL']=explicit

# New modeled source fixtures produced by the original M4/M5 catalog methods.
products['BASE_STRUCTURAL']=bridge(structural_revision=False).execute(request())
products['SANCTION_CHANGED']=bridge(sanction_revision=True).execute(request())
fee=bridge(structural_revision=False);fee.service.catalog._publish('training_fee',9,'2027-01-01','2028-01-01','2027-06-01',revision=2);fee.service.catalog.catalog_hash=semantic_hash(dict(records=fee.service.catalog.records,empirical=fee.service.catalog.empirical_identity()));products['FEE_CHANGED']=fee.execute(request())
deny=bridge();deny.service.catalog.revoke('training_access');dp=deny.prepare(request());products['STRUCTURAL_DENIED']=dict(product=deny.read(dp),selected_native_state=dp.snapshot.material['fields']['training_access']['state'],native_trace=deny.service.catalog.trace)
zero_rows=rows();row=next(x for x in zero_rows if x['role']==NCA);row['values']['active_subscriptions']=0;row['values']['prepaid']=0;row['values']['postpaid']=0
products['OBSERVED_NATIVE_ZERO']=NativeBridge(zero_rows,enabled=True).execute(request())
# Weak/null branches are scalar inputs, not reverse-capable invented clients.
products['WEAK_NULL']={}
for cond in [(('A',0),('B',0),('C',0)),(('A',1),('B',0),('C',1))]:products['WEAK_NULL'][str(cond)]=bridge().execute(request(conditions=cond),scalar_only=True)
obs.stop();trace=obs.result();records=defaultdict(dict)
for event in trace['C11_ingests'][0]['events']:
 m=event['semantic_fields'];person=m['scoped_respondent_ref']['content_hash'];q=m['native_question_ref']['object_id'].rsplit('-',1)[-1];records[person][q]=int(m['raw_response_value'])
strata=Counter((''.join(str(x[q]) for q in 'ABC'),x['Y']) for x in records.values());oracle=json.loads((ROOT/'01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json').read_text())
assert len(records)==58 and len(trace['C11_ingests'][0]['events'])==232
assert all([strata[(k,1)],strata[(k,0)]]==v for k,v in oracle['source_strata'].items())
out=dict(schema='E06_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS@1',executed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),grade='TEST_ONLY_SOURCEFREE_BRIDGE_CANDIDATE',products=products,source_reconstruction=dict(actual_respondents=58,actual_C11_events=232,strata={k:[strata[(k,1)],strata[(k,0)]] for k in oracle['source_strata']}),native_trace=trace,original_product_empirical_unchanged=True,independent_bridge_acceptance=False)
from persist import save_products
save_products(out,trace)
for state in ['restored','withdrawn']:
 ledger=deepcopy(persisted);ledger['state']=state
 if state=='withdrawn':ledger['grants']=[x.as_dict() for x in w['source']['authorities']]
 (ROOT/'observations'/('current_grants_'+state+'.json')).write_text(json.dumps(ledger,indent=2)+'\n')
print('Actual bridge products',len(products),'native imports',len(trace['imports']),'58 respondents/232 events, concrete F8 inputs',trace['same_concrete_C1_evidence_into_F8'])
