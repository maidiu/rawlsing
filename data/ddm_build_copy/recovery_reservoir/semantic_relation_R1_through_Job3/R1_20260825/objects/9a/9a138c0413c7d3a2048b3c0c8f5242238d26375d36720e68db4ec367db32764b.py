#!/usr/bin/env python3
import csv,json,sys
from pathlib import Path
root=Path(__file__).resolve().parent
assigned=list(csv.DictReader(open(root/'ASSIGNED_O12_R3_CANDIDATES.csv',encoding='utf-8-sig')))
ret=list(csv.DictReader(open(root/'JOB3_ADJUDICATION_RETURN.csv',encoding='utf-8-sig')))
manifest=json.load(open(root/'SHARD_MANIFEST.json',encoding='utf-8'))
wid=manifest['worker_id']
expected={r['candidate_id']:r for r in assigned}
errs=[]
if len(ret)!=len(assigned): errs.append(f'row_count {len(ret)} != {len(assigned)}')
ids=[r.get('candidate_id','') for r in ret]
if len(ids)!=len(set(ids)): errs.append('duplicate candidate_id in return')
missing=sorted(set(expected)-set(ids)); extra=sorted(set(ids)-set(expected))
if missing: errs.append(f'missing {len(missing)} candidate_ids; first={missing[:5]}')
if extra: errs.append(f'extra {len(extra)} candidate_ids; first={extra[:5]}')
for i,r in enumerate(ret,2):
    cid=r.get('candidate_id',''); disp=r.get('job3_disposition','').strip().upper()
    if r.get('worker_id','')!=wid: errs.append(f'line {i} wrong worker_id')
    if disp not in {'ACCEPT','REJECT','BLOCKED'}: errs.append(f'line {i} invalid disposition {disp!r}'); continue
    cand=expected.get(cid)
    if not cand: continue
    defect=r.get('candidate_scope_defect_suspected','').strip().lower()
    if defect not in {'true','false','yes','no','1','0'}: errs.append(f'line {i} invalid candidate_scope_defect_suspected')
    if defect in {'true','yes','1'} and not r.get('candidate_scope_defect_note','').strip(): errs.append(f'line {i} defect flag without note')
    if not r.get('semantic_rationale','').strip(): errs.append(f'line {i} missing semantic_rationale')
    if disp=='ACCEPT':
        if r.get('accepted_relation_type','').strip()!=cand['candidate_template_class']: errs.append(f'line {i} ACCEPT relation type must equal candidate_template_class')
        for col in ['member_roles_json','semantic_confidence','evidence_ceiling','prohibited_inference','evidence_refs_json']:
            if not r.get(col,'').strip(): errs.append(f'line {i} ACCEPT missing {col}')
        for col in ['member_roles_json','evidence_refs_json']:
            try: json.loads(r.get(col,''))
            except Exception: errs.append(f'line {i} invalid JSON in {col}')
    else:
        if r.get('accepted_relation_type','').strip(): errs.append(f'line {i} {disp} must not set accepted_relation_type')
    if disp=='REJECT' and not r.get('semantic_rationale','').strip(): errs.append(f'line {i} REJECT missing failed prerequisite rationale')
    if disp=='BLOCKED':
        if not r.get('blocker_code','').strip(): errs.append(f'line {i} BLOCKED missing blocker_code')
        if not r.get('blocker_detail','').strip(): errs.append(f'line {i} BLOCKED missing blocker_detail')
print(json.dumps({'worker_id':wid,'assigned':len(assigned),'returned':len(ret),'errors':errs[:100],'error_count':len(errs),'status':'PASS' if not errs else 'FAIL'},indent=2))
sys.exit(0 if not errs else 1)
