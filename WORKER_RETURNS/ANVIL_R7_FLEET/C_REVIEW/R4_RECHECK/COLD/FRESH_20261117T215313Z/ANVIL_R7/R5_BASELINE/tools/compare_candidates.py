#!/usr/bin/env python3
"""ANVIL R5: compare a PREDECLARED complete material cell set.
Checks comparability and interval arithmetic; cannot authenticate the runner, source rights, or measured truth.
Use --frozen with an H0/P15 externally frozen JSON file. Missing/weak evidence => no winner.
"""
import argparse,hashlib,json,pathlib,sys,math
ROOT=pathlib.Path(__file__).resolve().parents[1]
CASES={x['id'] for x in json.loads((ROOT/'13_WORKLOAD_AND_DISCRIMINATORS.json').read_text())['cases']}
METRICS={'build_wall_s','cold_open_wall_s','query_1_wall_s','query_10_wall_s','query_100_wall_s','process_tree_peak_rss_bytes','retained_bytes','scratch_peak_bytes','cross_world_100_wall_s'}

def full_comparison(data,frozen,strict_receipts=None):
    errors=[]
    if not isinstance(data,dict) or not isinstance(frozen,dict):return {'status':'RED','errors':['BAD_INPUT_OBJECT']}
    if data.get('schema')!='ANVIL_R5_COMPARATOR_INPUT' or frozen.get('schema')!='ANVIL_R5_FROZEN_MATERIAL_CELLS':errors.append('SCHEMA_MISMATCH')
    cells=frozen.get('cells',[])
    if not isinstance(cells,list) or not cells:errors.append('NO_FROZEN_MATERIAL_CELLS');cells=[]
    ids=[x.get('id') for x in cells if isinstance(x,dict)];byid={x.get('id'):x for x in cells if isinstance(x,dict)}
    if len(ids)!=len(set(ids)):errors.append('DUPLICATE_FROZEN_CELLS')
    exclusions=frozen.get('exclusions',[])
    accounted={x.get('workload_case_id') for x in cells if isinstance(x,dict)} | {x.get('workload_case_id') for x in exclusions if isinstance(x,dict)}
    if accounted != CASES:errors.append('NOT_ALL_WORKLOAD_SHAPES_ACCOUNTED')
    for x in exclusions:
        if not isinstance(x,dict) or not all(isinstance(x.get(k),str) and len(x[k])>=30 for k in ('reason_not_material','consumer_consequence','owner')):errors.append('UNJUSTIFIED_WORKLOAD_EXCLUSION')
    for cell in cells:
        if not isinstance(cell,dict):errors.append('BAD_FROZEN_CELL');continue
        if cell.get('workload_case_id') not in CASES or cell.get('metric') not in METRICS:errors.append('BAD_CELL_ID_OR_METRIC:'+str(cell.get('id')))
        for field in ('input_identity','runner_identity','negative_restore_oracle','decision_reversal_if_A','decision_reversal_if_B','required_claim_grade'):
            if not isinstance(cell.get(field),str) or len(cell[field])<15:errors.append('CELL_MISSING_SPECIFIC_'+field+':'+str(cell.get('id')))
    obs=data.get('measurements',[])
    if not isinstance(obs,list):obs=[];errors.append('NO_MEASUREMENTS')
    bids=[x.get('cell_id') for x in obs if isinstance(x,dict)];obs_by={x.get('cell_id'):x for x in obs if isinstance(x,dict)}
    if len(obs)!=len(obs_by):errors.append('DUPLICATE_MEASUREMENT')
    if set(bids)-set(ids):errors.append('UNDECLARED_MEASUREMENTS')
    missing=sorted(set(ids)-set(obs_by))
    if data.get('candidate_ids')!=['A','B']:errors.append('CANDIDATE_MAP_NOT_EXACT_AB')
    if data.get('frozen_sha256') and data['frozen_sha256']!=hashlib.sha256(json.dumps(frozen,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest():errors.append('FROZEN_CELL_CONTENT_HASH_MISMATCH')
    hard=data.get('hard_vetoes',{})
    if not isinstance(hard,dict) or set(hard)!={'A','B'} or any(not isinstance(hard[k],list) for k in ('A','B')):errors.append('UNRESOLVED_HARD_VETO_STATUS');hard={'A':[],'B':[]}
    advantages={'A':[],'B':[]};overlap=[];nonmeasured=[]
    for key,cell in obs_by.items():
        if key not in byid:continue
        for k in ('source_cut','source_grade','fixture_id','runner_id'):
            if cell.get(k)!=byid[key].get(k):errors.append('FROZEN_CELL_SCOPE_DRIFT:'+str(key)+':'+k)
        for side in ('A','B'):
            v=cell.get(side,{});
            if not isinstance(v,dict):errors.append('MISSING_SIDE_'+side+':'+str(key));nonmeasured.append(key);continue
            if v.get('status')!='MEASURED':nonmeasured.append(key);continue
            try:
                lo,x,hi=(v[q] for q in ('low','value','high'))
                if not all(type(z) in (int,float) and math.isfinite(z) and z>=0 for z in (lo,x,hi)) or not lo<=x<=hi:raise ValueError()
            except (ValueError,TypeError,KeyError):errors.append('INVALID_INTERVAL_'+side+':'+str(key))
            receipt=v.get('receipt_path');sha=v.get('receipt_sha256')
            if not isinstance(receipt,str) or not isinstance(sha,str) or len(sha)!=64:errors.append('NO_EXECUTED_RECEIPT_'+side+':'+str(key))
            elif strict_receipts is not None:
                root=pathlib.Path(strict_receipts).resolve();path=(root/receipt).resolve()
                if not path.is_relative_to(root) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:errors.append('ACTUAL_RECEIPT_HASH_FAILURE_'+side+':'+str(key))
        a=cell.get('A',{});b=cell.get('B',{})
        if isinstance(a,dict) and isinstance(b,dict) and a.get('status')=='MEASURED' and b.get('status')=='MEASURED':
            if all(type(v) in (int,float) for v in (a.get('high'),b.get('low'),b.get('high'),a.get('low'))):
                if a['high'] < b['low']:advantages['A'].append(key)
                elif b['high'] < a['low']:advantages['B'].append(key)
                else:overlap.append(key)
    if errors:return {'status':'RED','errors':sorted(set(errors)),'missing_cells':missing}
    if hard['A'] and hard['B']:return {'status':'BOTH_HARD_VETO','winner':None,'failed_vetoes':hard,'missing_cells':missing}
    if hard['A'] and not hard['B']:return {'status':'A_HARD_VETO','winner':'B' if not missing and not nonmeasured else None,'failed_vetoes':hard,'missing_cells':missing}
    if hard['B'] and not hard['A']:return {'status':'B_HARD_VETO','winner':'A' if not missing and not nonmeasured else None,'failed_vetoes':hard,'missing_cells':missing}
    if missing or nonmeasured:return {'status':'MISSING_DECISIVE_EVIDENCE','winner':None,'missing_cells':missing,'unmeasured_cells':sorted(set(nonmeasured)),'observed_advantages':advantages}
    if advantages['A'] and advantages['B']:status='TRADEOFF';winner=None
    elif advantages['A'] and not advantages['B'] and not overlap:status='A_DOMINATES_FULL_FROZEN_SET';winner='A'
    elif advantages['B'] and not advantages['A'] and not overlap:status='B_DOMINATES_FULL_FROZEN_SET';winner='B'
    else:status='PARETO_NONDECISIVE';winner=None
    return {'status':status,'winner':winner,'A_advantages':advantages['A'],'B_advantages':advantages['B'],'uncertain_cells':overlap,'measured_cells':len(obs),'warning':'Relative to declared frozen material set only. External C must authenticate relevance, source/runner/rights and scientific validity.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('--frozen',required=True);p.add_argument('--evidence-root');a=p.parse_args()
    try:r=full_comparison(json.loads(pathlib.Path(a.input).read_text()),json.loads(pathlib.Path(a.frozen).read_text()),a.evidence_root)
    except (OSError,ValueError,TypeError) as ex:r={'status':'RED','errors':[type(ex).__name__+':'+str(ex)]}
    print(json.dumps(r,indent=2));return 2 if r['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
