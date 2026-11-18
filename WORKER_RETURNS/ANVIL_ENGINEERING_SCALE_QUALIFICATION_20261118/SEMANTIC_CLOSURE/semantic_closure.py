#!/usr/bin/env python3
"""Export full payloads and controlled expected truth for four 10k ops."""
from __future__ import annotations
import gzip, hashlib, json, os, sys, time, builtins
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[2]
MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
EX=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118'/'EXECUTION'
SNAP=Path((EX/'SNAPSHOT_PATH.txt').read_text().strip())
sys.path[:0]=[str(SNAP),str(MP),str(MP/'vendor')]
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import exact_ref, canonical_json
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle
from court_instrumentation import CourtInstrumentation
contract=json.loads((EX/'fixture_contract_10k.json').read_text())
shape=ShapeSpec('scale-10k',contract['respondents'],include_weights=True,tag=contract['tag']);ctx=build_context(shape);bundle=build_query_bundle(ctx)
root=Path(contract['root']);grant={'ok':True}
opens=[]
def _open(*a,**k):
    opens.append({'call':'builtins.open','arg':str(a[0]) if a else None});return _orig_open(*a,**k)
def _osopen(*a,**k):
    opens.append({'call':'os.open','arg':str(a[0]) if a else None});return _orig_osopen(*a,**k)
_orig_open=builtins.open;_orig_osopen=os.open;builtins.open=_open;os.open=_osopen
try:
    h0=time.monotonic();adm=PreparedSavedC11Admission.open(root=root,exact_path=contract['exact_path'],independently_held_manifest_sha256=contract['manifest_sha256'],independently_held_i02=ExternalI02Roots(**contract['i02']),release_ref=exact_ref(contract['reconstructed_v1_release_ref']),runtime_catalog=bundle.catalog,current_authorizer=lambda _r:grant['ok']);H=time.monotonic()-h0
    entry=time.monotonic()
    with adm.prepared_i03() as session:
        S=time.monotonic()-entry
        rows=[]
        for label,key in (('selected_weighted','weighted'),('f2_forward_raw','f2_forward'),('f2_reverse_raw','f2_reverse'),('repeated_mr_raw','repeated')):
            q,p=bundle.by_name(key);q0=time.monotonic();res=session.execute_i03(query_ref=q.ref,predicate_ref=p.ref);Q=time.monotonic()-q0
            f=res.facts[0];payload=f.as_dict();sem=f.semantic_projection()
            o0=time.monotonic();serialized=canonical_json(payload);O=time.monotonic()-o0
            refs=lambda n:[exact_ref(r,n).key for r in getattr(f,n,())]
            row={'label':label,'query_ref':q.ref.key,'predicate_ref':p.ref.key,'Q_seconds':Q,'O_seconds':O,'fact_ref':f.ref.key,'typed_state':f.typed_state,'raw_numerator_support':f.raw_numerator_support,'raw_denominator_support':f.raw_denominator_support,'weighted_numerator':getattr(f,'weighted_numerator_support_if_authorized',None),'weighted_denominator':getattr(f,'weighted_denominator_support_if_authorized',None),'semantic_fields':sem,'risk_set_member_refs':refs('risk_set_member_refs'),'denominator_member_refs':refs('denominator_member_refs'),'provenance_refs':refs('source_empirical_provenance_refs'),'replay_ref':exact_ref(f.replay_ref,'replay').key,'payload_sha256':hashlib.sha256(serialized.encode()).hexdigest(),'payload_bytes':len(serialized.encode())}
            gz=HERE/f'{label}.payload.json.gz';gz.write_bytes(gzip.compress((json.dumps(payload,default=str,sort_keys=True)+'\n').encode()))
            rows.append(row);(HERE/'progress.json').write_text(json.dumps({'completed':[r['label'] for r in rows],'last':label},indent=2)+'\n')
        receipt=session.receipt().as_dict()
finally:
    builtins.open=_orig_open;os.open=_orig_osopen

def frac(v):
    if isinstance(v,dict) and '$exact_fraction' in v:return Fraction(*v['$exact_fraction'])
    return v
# Controlled fixture truth, independent of evaluator: pattern-derived counts/member sets.
def expected():
    out={}
    all_ids=[ctx._respondent(i).ref.key for i in range(contract['respondents'])]
    for label,kind in (('selected_weighted','weighted'),('f2_forward_raw','f2_forward'),('f2_reverse_raw','f2_reverse'),('repeated_mr_raw','repeated')):
        eligible=[];cells={}
        if kind in ('weighted','f2_forward'):
            for i in range(contract['respondents']):
                if i%2==1:
                    eligible.append(i);c=str((i%2)^((i//3)%2));cells[c]=cells.get(c,0)+1
            cells_expected={k:v for k,v in cells.items()}
        elif kind=='f2_reverse':
            for i in range(contract['respondents']):
                if ((i%2)^((i//3)%2))==1:eligible.append(i);cells[str(i%2)]=cells.get(str(i%2),0)+1
            cells_expected={k:v for k,v in cells.items()}
        else:
            for i in range(contract['respondents']):
                if i%13==0 and i%2==1:
                    eligible.append(i)
                    for occ in range(2):c=str((i+occ)%3);cells[c]=cells.get(c,0)+1
            cells_expected={k:v for k,v in cells.items()}
        out[label]={'eligible_indices':eligible,'eligible_count':len(eligible),'denominator_member_refs':[all_ids[i] for i in eligible],'cells':cells_expected}
    # Weighted masses for selected: exact weight 1+(i%4), no normalization.
    wc={}
    for i in range(contract['respondents']):
        if i%2==1:
            c=str((i%2)^((i//3)%2));wc[c]=wc.get(c,Fraction(0))+Fraction(1+(i%4),1)
    out['selected_weighted']['weighted_cells']={k:[v.numerator,v.denominator] for k,v in wc.items()}
    out['selected_weighted']['risk_set_member_refs']=all_ids
    for label in ('f2_forward_raw','f2_reverse_raw','repeated_mr_raw'):out[label]['risk_set_member_refs']=all_ids
    return out
exp=expected()
# compare expected counts and member sets; actual payload cells extracted.
for row in rows:
    e=exp[row['label']];facts_cells=row['semantic_fields'].get('target_topology',{}).get('complete_cell_semantic_projection')
    row['expected']=e
    row['expected_match']={'denominator_count':row['raw_denominator_support']==e['eligible_count'],'risk_count':len(row['risk_set_member_refs'])==len(e['risk_set_member_refs']),'risk_set':set(row['risk_set_member_refs'])==set(e['risk_set_member_refs']),'denom_set':set(row['denominator_member_refs'])==set(e['denominator_member_refs'])}
out={'schema':'ANVIL_SEMANTIC_CLOSURE_10K_FOUR_OPS@1','estate_manifest':contract['manifest_sha256'],'H_seconds':H,'S_seconds':S,'operations':rows,'source_open_events':opens[:2000],'source_open_event_count':len(opens),'source_open_visibility':'Python builtins.open/os.open captured; Arrow C++/SQLite internal opens and mmap not fully observable','admission_receipt':adm.binding_receipt().as_dict(),'session_receipt':receipt,'all_expected_match':all(all(v.values()) for r in rows for v in [r['expected_match']]),'limits':['four positive ops; no F4 rerun','expected values are controlled fixture derivation, not native oracle','OS cache uncontrolled']}
(HERE/'RESULT.json').write_text(json.dumps(out,indent=2,default=str,sort_keys=True)+'\n');print(json.dumps({'H':H,'S':S,'completed':[r['label'] for r in rows],'all_expected':out['all_expected_match'],'opens':len(opens)},indent=2))
