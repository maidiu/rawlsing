#!/usr/bin/env python3
"""Independent controlled-fixture truth for the four exported 10k payloads."""
from __future__ import annotations
import gzip,json,pathlib,sys
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent;REPO=HERE.parents[2]
MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117';EX=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118'/'EXECUTION'
sys.path[:0]=[str(REPO),str(MP),str(MP/'vendor')]
from fixture_1006 import ShapeSpec,build_context
contract=json.loads((EX/'fixture_contract_10k.json').read_text());shape=ShapeSpec('scale-10k',contract['respondents'],include_weights=True,tag=contract['tag']);ctx=build_context(shape)
N=contract['respondents'];ids=[ctx._respondent(i).ref.key for i in range(N)]
def cellval(i):return str((i%2)^((i//3)%2))
def expected(label):
 if label in ('selected_weighted','f2_forward_raw'):
  elig=[i for i in range(N) if i%2==1];counts={}
  for i in elig:counts[cellval(i)]=counts.get(cellval(i),0)+1
  cells=[{'cell':v,'cell_state':'OBSERVED_POSITIVE','raw_numerator_support':counts[v]} for v in sorted(counts)]
  w=None
  if label=='selected_weighted':
   wc={}
   for i in elig:
    c=cellval(i);wc[c]=wc.get(c,Fraction(0))+Fraction(1+(i%4),1)
   for c in cells:
    f=wc[c['cell']];c['weighted_numerator_support_if_authorized']={'$exact_fraction':[f.numerator,f.denominator]}
   w={'cells':{k:[v.numerator,v.denominator] for k,v in wc.items()},'total':[sum(wc.values()).numerator,sum(wc.values()).denominator]}
  return {'eligible':elig,'cells':cells,'risk':ids,'denom':[ids[i] for i in elig],'weighted':w}
 if label=='f2_reverse_raw':
  elig=[i for i in range(N) if cellval(i)=='1'];counts={}
  for i in elig:counts[str(i%2)]=counts.get(str(i%2),0)+1
  cells=[{'cell':v,'cell_state':'OBSERVED_POSITIVE','raw_numerator_support':counts[v]} for v in sorted(counts)]
  return {'eligible':elig,'cells':cells,'risk':ids,'denom':[ids[i] for i in elig]}
 # repeated MR: risk all repeated indices; denominator A=1; each cell is a two-occurrence config.
 risk=[i for i in range(N) if i%13==0];elig=[i for i in risk if i%2==1];cells=[]
 for i in risk:
  cells.append({'cell':[{'event_id':f'{i:08d}-MR-{o}','multiplicity_order_rank_fields':{'kind':'REPEATED_EVENT','multiplicity_index':o,'rank':o+1},'value':str((i+o)%3)} for o in range(2)],'cell_state':'OBSERVED_POSITIVE' if i%2==1 else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET','raw_numerator_support':1 if i%2==1 else 0})
 return {'eligible':elig,'cells':cells,'risk':[ids[i] for i in risk],'denom':[ids[i] for i in elig]}
def norm_cells(cells):
 out=[]
 for c in cells:
  out.append({k:c[k] for k in ('cell','cell_state','raw_numerator_support')})
 return out
report={};allok=True
for label in ('selected_weighted','f2_forward_raw','f2_reverse_raw','repeated_mr_raw'):
 payload=json.loads(gzip.decompress((HERE/f'{label}.payload.json.gz').read_bytes()));actual=payload['semantic_fields']['target_topology']['complete_cell_semantic_projection'];e=expected(label)
 # actual member sets from RESULT row
 res=json.loads((HERE/'RESULT.json').read_text());row=next(r for r in res['operations'] if r['label']==label)
 checks={'cells':norm_cells(actual)==norm_cells(e['cells']),'risk_set':set(row['risk_set_member_refs'])==set(e['risk']),'denom_set':set(row['denominator_member_refs'])==set(e['denom']),'raw_numerator':row['raw_numerator_support']==sum(c['raw_numerator_support'] for c in e['cells']),'raw_denominator':row['raw_denominator_support']==len(e['eligible']),'state':row['typed_state']=='SUPPORTED'}
 if label=='selected_weighted':
  wc={c['cell']:Fraction(*c['weighted_numerator_support_if_authorized']['$exact_fraction']) for c in actual};checks['weighted_cells']=wc=={c['cell']:Fraction(*c['weighted_numerator_support_if_authorized']['$exact_fraction']) for c in e['cells']}
 report[label]={'checks':checks,'all':all(checks.values()),'expected_cells':norm_cells(e['cells']),'expected_denominator_count':len(e['eligible']),'expected_risk_count':len(e['risk']),'actual_risk_count':len(row['risk_set_member_refs']),'actual_denom_count':len(row['denominator_member_refs'])};allok &= report[label]['all']
out={'schema':'ANVIL_SEMANTIC_CLOSURE_EXPECTED_TRUTH@1','fixture':contract['tag'],'respondents':N,'questions':5,'operations':report,'all_expected_match':allok,'derivation':'controlled A/B/C/MR pattern, weights 1+(i%4), exact member ids; no native oracle rerun','payloads':'*.payload.json.gz full as_dict'}
(HERE/'EXPECTED_TRUTH.json').write_text(json.dumps(out,indent=2,default=str,sort_keys=True)+'\n');print(json.dumps({k:v['all'] for k,v in report.items()}|{'all':allok},indent=2));print(json.dumps({k:{'checks':v['checks'],'members':[v['actual_risk_count'],v['actual_denom_count']]} for k,v in report.items()},indent=1)[:3000])
