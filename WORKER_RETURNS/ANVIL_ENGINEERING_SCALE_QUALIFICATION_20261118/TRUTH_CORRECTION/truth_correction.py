#!/usr/bin/env python3
"""Frozen-payload truth correction; no native run/build/query."""
from __future__ import annotations
import gzip,hashlib,json,sys
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2];MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
SC=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118'/'SEMANTIC_CLOSURE';W=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118'/'WIDTH128'
sys.path[:0]=[str(REPO),str(MP),str(MP/'vendor')]
from rawlsing_next.pre553_empirical_objects import canonical_json,exact_ref
from fixture_1006 import ShapeSpec,build_context
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(gzip.decompress(p.read_bytes()))
def actual_sem(label):
 d=load(SC/f'{label}.payload.json.gz');s=d['semantic_fields'];return {'payload':d,'risk_set_member_refs':[exact_ref(r,'risk').key for r in s['risk_set_member_refs']],'denominator_member_refs':[exact_ref(r,'denom').key for r in s['denominator_member_refs']],'cells':s['target_topology']['complete_cell_semantic_projection'],'replay_ref':exact_ref(s['replay_ref'],'replay').key,'provenance_refs':[exact_ref(r,'prov').key for r in s['source_empirical_provenance_refs']]}
def branch_expected(kind,N,ctx):
 ids=[ctx._respondent(i).ref.key for i in range(N)]
 if kind in ('selected_weighted','f2_forward_raw'):
  elig=[i for i in range(N) if i%2==1];counts={}
  for i in elig:c=str((i%2)^((i//3)%2));counts[c]=counts.get(c,0)+1
  cells=[{'cell':c,'cell_state':'OBSERVED_POSITIVE','raw_numerator_support':counts.get(c,0)} for c in ('0','1')]
  if kind=='selected_weighted':
   wc={}
   for i in elig:c=str((i%2)^((i//3)%2));wc[c]=wc.get(c,Fraction(0))+Fraction(1+(i%4),1)
   for c in cells:
    f=wc.get(c['cell'],Fraction(0));c['weighted_numerator_support_if_authorized']={'$exact_fraction':[f.numerator,f.denominator]}
  return {'cells':cells,'risk':ids,'denom':[ids[i] for i in elig]}
 if kind=='f2_reverse_raw':
  elig=[i for i in range(N) if ((i%2)^((i//3)%2))==1];counts={}
  for i in elig:counts[str(i%2)]=counts.get(str(i%2),0)+1
  return {'cells':[{'cell':c,'cell_state':'OBSERVED_POSITIVE','raw_numerator_support':counts.get(c,0)} for c in ('0','1')],'risk':ids,'denom':[ids[i] for i in elig]}
 risk=[i for i in range(N) if i%13==0];elig=[i for i in risk if i%2==1];cells=[]
 for i in risk:
  cells.append({'cell':[{'event_id':f'{i:08d}-MR-{o}','multiplicity_order_rank_fields':{'kind':'REPEATED_EVENT','multiplicity_index':o,'rank':o+1},'value':str((i+o)%3)} for o in range(2)],'cell_state':'OBSERVED_POSITIVE' if i%2==1 else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET','raw_numerator_support':1 if i%2==1 else 0})
 return {'cells':cells,'risk':[ids[i] for i in risk],'denom':[ids[i] for i in elig]}
def norm(cells, weighted=False):
 out=[]
 for c in cells:
  d={'cell':c['cell'],'cell_state':c['cell_state'],'raw_numerator_support':c['raw_numerator_support']}
  if weighted:d['weighted_numerator_support_if_authorized']=c.get('weighted_numerator_support_if_authorized')
  out.append(d)
 return out
ctx=build_context(ShapeSpec('scale-10k',10000,include_weights=True,tag='PYAT-1006-SCALE-10K-20261118'));res=json.loads((SC/'RESULT.json').read_text());semantic={};allok=True
for label,kind in (('selected_weighted','selected_weighted'),('f2_forward_raw','f2_forward_raw'),('f2_reverse_raw','f2_reverse_raw'),('repeated_mr_raw','repeated_mr_raw')):
 a=actual_sem(label);e=branch_expected(kind,10000,ctx);row=next(r for r in res['operations'] if r['label']==label)
 checks={'risk_set':set(a['risk_set_member_refs'])==set(e['risk']),'denom_set':set(a['denominator_member_refs'])==set(e['denom']),'cells':norm(a['cells'],label=='selected_weighted')==norm(e['cells'],label=='selected_weighted'),'raw_num':row['raw_numerator_support']==sum(c['raw_numerator_support'] for c in e['cells']),'raw_denom':row['raw_denominator_support']==len(e['denom']),'replay_ref':a['replay_ref']==row['replay_ref'],'payload_sha':sha(canonical_json(a['payload']).encode())==row['payload_sha256']}
 if label=='selected_weighted':
  checks['weighted_cells']=all(Fraction(*c.get('weighted_numerator_support_if_authorized',{'$exact_fraction':[0,1]})['$exact_fraction'])==Fraction(*x.get('weighted_numerator_support_if_authorized',{'$exact_fraction':[0,1]})['$exact_fraction']) for c,x in zip(a['cells'],e['cells']))
 semantic[label]={'checks':checks,'all':all(checks.values()),'expected':{'cells':e['cells'],'risk_set_member_refs':e['risk'],'denominator_member_refs':e['denom']},'actual':{'cells':a['cells'],'risk_set_member_refs':a['risk_set_member_refs'],'denominator_member_refs':a['denominator_member_refs'],'replay_ref':a['replay_ref']}};allok &= semantic[label]['all']
 # same-count expected-member replacement must FAIL
 mut=dict(semantic[label]['expected']);rs=list(mut['risk_set_member_refs']);rs[0]=rs[1] if len(rs)>1 else 'BAD';mut['risk_set_member_refs']=rs;semantic[label]['negative_member_replacement_fails']=set(a['risk_set_member_refs'])!=set(rs)
# width
wd=load(W/'f4.payload.json.gz');ws=wd['semantic_fields'];actual={'cells':ws['target_topology']['complete_cell_semantic_projection'],'risk':[exact_ref(r,'risk').key for r in ws['risk_set_member_refs']],'denom':[exact_ref(r,'denom').key for r in ws['denominator_member_refs']],'replay':exact_ref(ws['replay_ref'],'replay').key}
ctxw=build_context(ShapeSpec('width128',128,include_weights=True,tag='PYAT-1006-WIDTH128-600-20261118'));ids=[ctxw._respondent(i).ref.key for i in range(128)];elig=[];counts={}
for i in range(128):
 if i%2==1 and i%17!=0 and ((i//3)%2)==1:elig.append(i);c=str((i%2)^((i//3)%2));counts[c]=counts.get(c,0)+1
wexp={'cells':[{'cell':c,'cell_state':'OBSERVED_POSITIVE' if counts.get(c,0) else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET','raw_numerator_support':counts.get(c,0)} for c in ('0','1')],'risk_set_member_refs':ids,'denominator_member_refs':[ids[i] for i in elig]}
wchecks={'cells':norm(actual['cells'])==norm(wexp['cells']),'risk_set':set(actual['risk'])==set(ids),'denom_set':set(actual['denom'])==set(wexp['denominator_member_refs']),'replay_ref':actual['replay']==json.loads((W/'RESULT.json').read_text())['replay_ref'],'payload_sha':sha(canonical_json(wd).encode())==json.loads((W/'RESULT.json').read_text())['payload_sha256']}
wzero_removed={'cells':[c for c in wexp['cells'] if c['cell']!='1'],'risk_set_member_refs':ids,'denominator_member_refs':wexp['denominator_member_refs']}
width={'checks':wchecks,'all':all(wchecks.values()),'expected':wexp,'actual':actual,'negative_zero_cell_deletion_fails':norm(actual['cells'])!=norm(wzero_removed['cells'])}
# serializations
(HERE/'EXPECTED_SETS.json.gz').write_bytes(gzip.compress((json.dumps({k:{'risk':v['expected']['risk_set_member_refs'],'denom':v['expected']['denominator_member_refs'],'cells':v['expected']['cells']} for k,v in semantic.items()},sort_keys=True)+'\n').encode()))
(HERE/'ACTUAL_SETS.json.gz').write_bytes(gzip.compress((json.dumps({k:{'risk':v['actual']['risk_set_member_refs'],'denom':v['actual']['denominator_member_refs'],'cells':v['actual']['cells']} for k,v in semantic.items()},sort_keys=True)+'\n').encode()))
out={'schema':'ANVIL_TRUTH_CORRECTION@1','semantic':semantic,'width':width,'all_semantic':allok,'all_width':width['all'],'all':allok and width['all'],'source_open_classification':'one os.open is temporary native I03 session directory, not raw source','no_native_run':True}
(HERE/'VERIFICATION.json').write_text(json.dumps(out,indent=2,default=str,sort_keys=True)+'\n');print(json.dumps({'all':out['all'],'semantic':{k:v['checks'] for k,v in semantic.items()},'width':wchecks},indent=2,default=str))
