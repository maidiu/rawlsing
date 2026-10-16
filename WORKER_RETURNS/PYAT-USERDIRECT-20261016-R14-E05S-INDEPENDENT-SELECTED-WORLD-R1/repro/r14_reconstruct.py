"""Independent aggregation of physically observed C11 event preimages."""
import pathlib,json,collections
R=pathlib.Path(__file__).resolve().parents[1];x=json.loads((R/'observations/r14_actual_native_probe.json').read_text());out=[]
for label,ing in zip(x['results'],x['C11_ingests']):
 rows={}
 for e in ing['events']:
  f=e['semantic_fields'];identity=f['scoped_respondent_ref']['content_hash'];key=f['native_question_ref']['object_id'].rsplit('-',1)[1]
  row=rows.setdefault(identity,{});assert key not in row;row[key]=int(f['raw_response_value'])
 assert all(set(r)=={'A','B','C','Y'} for r in rows.values())
 counts=[]
 for depth in (1,2,3):
  selected=[r for r in rows.values() if all(r[k]==1 for k in ('A','B','C')[:depth])]
  counts.append([sum(r['Y']==1 for r in selected),len(selected)])
 expected=[[12,24],[4,8],[0,0]] if label=='ZERO_SUPPORT' else [[18,32],[10,16],[6,8]]
 assert counts==expected
 if label not in ('ZERO_SUPPORT','TYPED_PARTIAL_PRE_NCA_PUBLICATION'):
  actual=x['results'][label]['receipt']['empirical_steps']
  assert [[next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='1'),s['denominator']] for s in actual]==counts
 if label=='ZERO_SUPPORT':assert [s['denominator'] for s in x['results'][label]['receipt']['empirical_steps']]==[24,8,0]
 reverse=[sum(r['A']==1 and r['Y']==1 for r in rows.values()),sum(r['Y']==1 for r in rows.values())]
 if label!='ZERO_SUPPORT':assert reverse==[18,29]
 out.append(dict(label=label,respondents=len(rows),events=len(ing['events']),counts=counts,reverse=reverse,strata=dict(collections.Counter(''.join(str(r[k]) for k in 'ABC')+':Y'+str(r['Y']) for r in rows.values()))))
facts={f['ref']['content_hash'] for f in x['I03_facts']}
for c in x['concrete_composition_returns']:
 assert c['fact_ref']['content_hash'] in facts
 assert any(c['id'] in i['ids'] and c['evidence_ref'] in i['refs'] for i in x['actual_f8_inputs'])
(R/'observations/r14_C11_preimage_reconstruction.json').write_text(json.dumps(dict(cases=out,concrete_C1_to_F8_and_actual_I03_fact_binding=True),indent=2)+'\n');print(out)
