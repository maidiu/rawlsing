"""Independent arithmetic from the actual C11 event preimages, no estimator stubs."""
from pathlib import Path
from collections import Counter,defaultdict
import json,hashlib
R=Path(__file__).resolve().parents[1];d=json.loads((R/'observations/full_native_probe.json').read_text());records=defaultdict(dict)
for item in d['C11_ingests'][0]['source_events']:
 e=item['semantic_fields'];q=e['native_question_ref']['object_id'].rsplit('-',1)[-1];person=e['scoped_respondent_ref']['content_hash'];records[person][q]=int(e['raw_response_value'])
assert len(records)==58 and all(set(r)==set('ABCY') for r in records.values())
strata=Counter((''.join(str(r[q]) for q in 'ABC'),r['Y']) for r in records.values());expected={'111':(6,2),'110':(4,4),'101':(5,3),'100':(3,5),'011':(4,2),'010':(2,4),'001':(3,3),'000':(2,6)}
assert all(strata[(k,1)]==yes and strata[(k,0)]==no for k,(yes,no) in expected.items())
out=[]
for depth in (1,2,3):
 selected=[r for r in records.values() if all(r[q]==1 for q in 'ABC'[:depth])];counts=Counter(str(r['Y']) for r in selected);assert len(selected)==[32,16,8][depth-1] and counts['1']==[18,10,6][depth-1]
 out.append({'conditions':[[q,1] for q in 'ABC'[:depth]],'denominator':len(selected),'counts':dict(counts)})
facts={f['ref']['content_hash']:f for f in d['I03_facts']};evidence={c['evidence_ref']['content_hash']:c for c in d['composition_returns']}
for step in d['baseline']['nonparent']['material']['empirical']['steps']:
 assert step['producer_fact_ref']['content_hash'] in facts
 assert step['evidence_ref']['content_hash'] in evidence
 c=evidence[step['evidence_ref']['content_hash']];assert c['fact_ref']==step['producer_fact_ref'] and c['query_ref']==step['producer_query_ref']
 assert any(c['id'] in a['ids'] and c['evidence_ref'] in a['evidence_refs'] for a in d['F8_actual_inputs'])
(R/'observations/independent_C11_native_reconstruction.json').write_text(json.dumps({'actual_respondents':58,'actual_event_count':len(d['C11_ingests'][0]['source_events']),'strata':{k:{'Y1':strata[(k,1)],'Y0':strata[(k,0)]} for k in expected},'progressive':out,'exact_I03_C1_F8_ref_and_object_identity_verified':True},indent=2)+'\n');print('ACTUAL_C11_58_ROWS_AND_232_EVENTS_RECONSTRUCTED__SAME_EVIDENCE_TO_F8_VERIFIED')
