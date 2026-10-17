"""Independent reconstruction solely from captured sealed C11 records."""
from pathlib import Path
from collections import Counter
import json
R=Path(__file__).resolve().parents[1];d=json.loads((R/'observations/baseline.json').read_text());out=[]
for tag,risk,questions,denominator in [('REL-A-W1','R_ORD',['Q-ORD-A'],6),('REL-A-W2','R_ORD2',['Q-ORD-A'],4),('REL-A-W1','R_HH',['Q-HH-food','Q-HH-rent','Q-HH-health','Q-HH-edu','Q-HH-none'],4)]:
 rel=next(r for r in d['releases'] if r['tag']==tag)
 records=rel['records'];events=[r['payload']['semantic_fields'] for r in records if r['type']=='RespondentEvent'];routing=[r['payload']['semantic_fields'] for r in records if r['type']=='RoutingEligibilityFact']
 eligible=[]
 for q in questions:
  eligible.append({r['scoped_respondent_ref']['content_hash'] for r in routing if r['risk_set_ref']['object_id'].endswith('-'+risk) and r['question_or_target_ref']['object_id'].endswith('-'+q) and r['routing_state']=='ELIGIBLE_APPLICABLE'})
 joint=set.intersection(*eligible);assert len(joint)==denominator
 responses={}
 for q in questions:
  responses[q]={e['scoped_respondent_ref']['content_hash']:e['raw_response_value'] for e in events if e['native_question_ref']['object_id'].endswith('-'+q) and e['scoped_respondent_ref']['content_hash'] in joint and e['response_state']=='SUBSTANTIVE_RESPONSE'}
 assert all(set(x)==joint for x in responses.values())
 profiles=Counter(tuple(responses[q][person] for q in questions) for person in joint)
 rec={'tag':tag,'risk':risk,'questions_in_semantic_order':questions,'exact_eligible_respondent_hashes':sorted(joint),'denominator':len(joint),'profiles':[{'cell':list(k),'n':v} for k,v in sorted(profiles.items())],'weights':'RAW; ingress WeightMeasureFact typed absence NOT_APPLICABLE'}
 if len(questions)==1:
  cells={v:profiles.get((v,),0) for v in ('0','1','2','3','9')};assert cells==({'0':1,'1':2,'2':2,'3':1,'9':0} if tag=='REL-A-W1' else {'0':0,'1':2,'2':1,'3':1,'9':0});rec['complete_cells']=cells
 else:
  rec['indicator_totals']={name:sum(n for profile,n in profiles.items() if profile[i]=='yes') for i,name in enumerate(('food','rent','health','education','none'))};assert rec['indicator_totals']=={'food':2,'rent':2,'health':2,'education':1,'none':1}
 out.append(rec)
assert all(x['weight_absence']['state']=='NOT_APPLICABLE' for x in d['ingest_inputs'])
(R/'observations/independent_native_reconstruction.json').write_text(json.dumps(out,indent=2)+'\n');print('INDEPENDENT_C11_NATIVE_RECONSTRUCTION_PASS_3')
