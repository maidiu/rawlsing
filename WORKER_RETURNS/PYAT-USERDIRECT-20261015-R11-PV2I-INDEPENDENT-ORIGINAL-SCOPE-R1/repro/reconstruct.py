"""Independent arithmetic/provenance reconstruction from actual captured C11.
No candidate register/oracle helpers imported.
"""
from pathlib import Path
from collections import Counter
import json,hashlib
R=Path(__file__).resolve().parents[1];d=json.loads((R/'observations/physical_baseline.json').read_text());out=[]
def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
for c in d['C11_ingests']:
 assert c['accepted'];u=next(x['semantic_fields'] for x in c['public'] if x['schema_id']=='EmpiricalUniverse');ns=u['respondent_namespace']
 people={h(p):p['semantic_fields']['respondent_key'] for p in c['respondents']};events=[p['semantic_fields'] for p in c['public'] if p['schema_id']=='RespondentEvent'];routes=[p['semantic_fields'] for p in c['public'] if p['schema_id']=='RoutingEligibilityFact']
 responses={};eligible={}
 for q in ('X','Y'):
  values={people[e['scoped_respondent_ref']['content_hash']]:e['raw_response_value']['$raw_physical_value']['token']['v'] for e in events if e['native_question_ref']['object_id'].endswith('-'+q) and e['response_state']=='SUBSTANTIVE_RESPONSE'}
  assert values=={'R1':'1','R2':'0','R3':'1'}
  responses[q]=values;eligible[q]={people[r['scoped_respondent_ref']['content_hash']] for r in routes if r['question_or_target_ref']['object_id'].endswith('-'+q) and r['routing_state']=='ELIGIBLE_APPLICABLE'}
 joint=eligible['X']&eligible['Y'];assert joint=={'R1','R2'}
 cells=Counter((responses['X'][p],responses['Y'][p]) for p in joint);assert cells=={('0','0'):1,('1','1'):1}
 out.append({'namespace':ns,'C11_release_ref':c['release_ref'],'source_artifact_ref':c['source_artifact_ref'],'actual_native_responses':responses,'eligible':{q:sorted(x) for q,x in eligible.items()},'joint_exact_same_people':sorted(joint),'joint_counts':[{'cell':list(k),'n':v} for k,v in sorted(cells.items())]})
facts={f['ref']['content_hash']:f for f in d['I03_facts']};produced_refs={x['ref']['content_hash'] for x in d['actual_Field_Forge_producer_returns'] if isinstance(x.get('ref'),dict)};links=d['report']['links']
for l in links:
 assert l['producer_result_ref']['content_hash'] in facts
 assert l['producer_result_ref']==l['consumer_material']['producer_fact_ref']
 assert l['consumer_ref']['content_hash'] in produced_refs
 original=l['original_identity']['original'];c=next(c for c in d['C11_ingests'] if c['release_ref'] in l['c11_release_refs'])
 assert original['source_release_ref']==c['source_artifact_ref']
 for q in original['native_item_refs']:assert any(e['schema_id']=='RespondentEvent' and e['semantic_fields']['native_question_ref']==q for e in c['public'])
 roles=l['consumer_material']['roles'];assert roles['CONDITIONER']['ref']==original['native_item_refs'][0] and roles['TARGET']['ref']==original['native_item_refs'][1]
(R/'observations/independent_C11_provenance_reconstruction.json').write_text(json.dumps({'source_reconstruction':out,'actual_distinct_consumer_refs':len({l['consumer_ref']['content_hash'] for l in links}),'all6_actual_I03_fact_and_Field_Forge_returns_bound':True,'lexical_gap':'Participant exact refs bind X/Y; semantic projection still labels them Q86B/Q86A.'},indent=2)+'\n');print('INDEPENDENT_SOURCE_ARITHMETIC_AND_ALL6_PRODUCER_CONSUMER_REFS_PASS')
