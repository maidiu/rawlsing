"""E04S independent physical source/evidence/consumer probe, no owner wrappers."""
from common import *
from observer import Observer
from collections import Counter,defaultdict
from dataclasses import FrozenInstanceError
obs=Observer(detailed=True);obs.start();outputs={}
def case(label,**options):
 s,ss,a,b=full(**options);outputs[label]=dict(snapshot=ss.material,snapshot_hash=ss.snapshot_hash,nonparent=a,scenario=b,structural_trace=s.catalog.trace,empirical_trace=s.provider.trace);return s,ss,a,b
s,ss,a,b=case('baseline')
outputs['reverse']=s.possibilities(ss,target='A',conditions=(('Y',1),))
t,ts,c,d=case('Y_mutation',empirical_changed=True)
u,us,e,f=case('access_exit_mutation',structural_revision=True)
v,vs,g,h=case('sanction_mutation',sanction_revision=True)
z,zs,za,zb=case('zero_support',support_loss=True)
fee=GenericSelectedWorldService();fee.catalog._publish('training_fee',9,'2027-01-01','2028-01-01','2027-06-01',revision=2);fee.catalog.catalog_hash=semantic_hash(dict(records=fee.catalog.records,empirical=fee.catalog.empirical_identity()));fs=fee.select();outputs['fee_mutation']=dict(nonparent=consume(fee,fs),scenario=evaluate(fee,fs,PROPOSALS),structural_trace=fee.catalog.trace)
outputs['clock']={}
for mode,valid,pub,now in [('AS_OF','2026-06-01','2026-03-01',None),('AS_OF','2027-02-01','2027-03-01',None),('TEST_CURRENT','2027-09-01','2027-09-01','2027-09-01')]:
 q=u.select(mode=mode,valid_at=valid,published_asof=pub,test_now=now);outputs['clock'][mode+'_'+pub]=dict(snapshot=q.material,nonparent=consume(u,q),scenario=evaluate(u,q,PROPOSALS))
# Native recomputation after deleting ONLY deepest projection, not static tables.
key=('Y',(('A',1),('B',1),('C',1)));prior_counts=dict(obs.counts);anchors=dict(s.provider._accepted);prior=deepcopy(s.provider.cache[key]);del s.provider.cache[key]
recomputed=s.possibilities(ss);delta={str(k):v-prior_counts.get(k,0) for k,v in obs.counts.items() if v>prior_counts.get(k,0)}
assert recomputed['steps'][-1]==prior and any('compose_positioned_subject_possibility' in k for k in delta)
outputs['selective_cache_miss']=dict(original=prior,recomputed=recomputed['steps'][-1],actual_native_call_delta=delta,unrelated_anchors_same_object=all(s.provider._accepted[k] is v for k,v in anchors.items() if k!=key))
# Both fresh consumers blocked at empirical scope; archival product unchanged.
history=s.historical_receipt(a['receipt_hash']);withdrawal=s.invalidate('empirical');ar=consume(s,ss);br=evaluate(s,ss,PROPOSALS)
assert ar['material']['empirical']['state']==br['material']['empirical']['state']=='REVOKED'
assert history==s.historical_receipt(a['receipt_hash'])
outputs['empirical_revocation']=dict(invalidation=withdrawal,nonparent=ar,scenario=br,archive=history)
world=GenericSelectedWorldService();ws=world.select();wa=consume(world,ws);world.invalidate('training_access');new=world.select();denial=world.structural(new,'training_access','E04S_REVOCATION')
assert denial['state']=='REVOKED'
assert new.material['fields']['training_access']['state']=='RESOLUTION_DENIED_OR_NOT_APPLICABLE'
outputs['structural_revocation']=dict(old=wa,new_snapshot=new.material,denied=denial,nonparent=consume(world,new),scenario=evaluate(world,new,PROPOSALS))
# Real retained I03 owner fact, after completion: ordinary mutation must refuse.
fact=next(x for x in obs.held if getattr(x,'schema_id',None)=='EmpiricalFact')
fact_before=fact.as_dict()
try:fact.typed_state='FABRICATED'
except AttributeError:immutable_assignment=True
else:immutable_assignment=False
try:fact.semantic_fields['raw_denominator_support']=999
except TypeError:immutable_descendants=True
else:immutable_descendants=False
assert immutable_assignment and immutable_descendants and fact.as_dict()==fact_before
outputs['actual_I03_fact_mutation']=dict(ref=fact.ref.as_dict(),normal_assignment_refused=immutable_assignment,descendant_mutation_refused=immutable_descendants,original_unchanged=True)
obs.stop();actual=obs.material()
assert actual['compositions']
for x in actual['compositions']:
 assert any(x['id'] in v['ids'] and x['evidence_ref'] in v['refs'] for v in actual['F8_actual_inputs'])
records=defaultdict(dict)
for event in actual['C11_ingests'][0]['source_events']:
 m=event['semantic_fields'];person=m['scoped_respondent_ref']['content_hash'];q=m['native_question_ref']['object_id'].rsplit('-',1)[-1];records[person][q]=int(m['raw_response_value'])
assert len(records)==58 and len(actual['C11_ingests'][0]['source_events'])==232
strata=Counter((''.join(str(r[q]) for q in 'ABC'),r['Y']) for r in records.values())
expected=json.loads((R/'01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json').read_text())['source']['strata']
assert all([strata[(k,1)],strata[(k,0)]]==v for k,v in expected.items())
for depth,step in enumerate(a['material']['empirical']['steps'],1):assert geometry(step)==direct(list(records.values()),'Y',[(q,1) for q in 'ABC'[:depth]])
facts={x['ref']['content_hash']:x for x in actual['I03_facts']};evidence={x['evidence_ref']['content_hash']:x for x in actual['compositions']}
for step in a['material']['empirical']['steps']:
 assert step['producer_fact_ref']['content_hash'] in facts
 ev=evidence[step['evidence_ref']['content_hash']];assert ev['fact_ref']==step['producer_fact_ref'] and ev['query_ref']==step['producer_query_ref']
assert [geometry(x)['cells']['1'] for x in c['material']['empirical']['steps']]==[19,11,7]
assert a['material']['structural_routes']==c['material']['structural_routes']
assert ss.material['fields']==ts.material['fields']
assert [x['denominator'] for x in za['material']['empirical']['steps']]==[24,8,0]
result=dict(actual=actual,outputs=outputs,source_reconstruction=dict(actual_respondents=len(records),actual_events=232,strata={k:[strata[(k,1)],strata[(k,0)]] for k in expected},same_exact_evidence_objects_into_F8=True,exact_I03_query_fact_evidence_refs=True))
dump('scientific_probe.json',result)
print('ACTUAL_OWNER_CALLS',sum(x['count'] for x in actual['counts']));print('SAME_OBJECT_EVIDENCE_TO_F8',len(actual['compositions']));print('RECONSTRUCTED',len(records),'respondents / 232 C11 events')
