#!/usr/bin/env python3
"""Reproduce the Phase-D successor archetype freeze from nonrespondent authority only."""
from __future__ import annotations
import argparse, collections, hashlib, json, re
from pathlib import Path
import pandas as pd

EXPECTED_SHA = "5ae32c7cdfd68d3e0c1816abd85fc6f77387f65a383e5b860d2ab9cf814235b2"
COLS = [
    'archetype','frozen_rank','candidate_key','semantic_posture','semantic_ref_id',
    'source_family','wave','member_implementation_ids_json','source_variables_json',
    'routing_statuses_json','structural_allowance_proof_type','structural_allowance_proof_json',
    'respondent_contract_status','blocker_code','blocker_detail','routing_proof_type',
    'routing_proof_json','blocked_scopes_json','selection_outcome_fields_used'
]

def compact(x): return json.dumps(x, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
def jd(x): return None if pd.isna(x) else json.loads(x)
def boolish(x): return False if pd.isna(x) else (x if isinstance(x,bool) else str(x).strip().lower() in {'1','true','yes'})
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def native_pages(row):
    try: p=json.loads(row['provenance'])
    except Exception: return []
    sp=p.get('source_provenance')
    if isinstance(sp,str):
        try: sp=json.loads(sp)
        except Exception: sp=None
    if isinstance(sp,list):
        return [int(x['page_number']) for x in sp if isinstance(x,dict) and x.get('page_number') not in (None,'')]
    fp=p.get('flattened_native_pages')
    if isinstance(fp,dict):
        return [int(v) for vs in fp.values() if isinstance(vs,list) for v in vs]
    return []

def parse_or_eq(expr):
    if not expr: return None
    var=None; vals=set()
    for part in re.split(r'\s+Or\s+', expr, flags=re.I):
        m=re.fullmatch(r'([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_.-]+)', part.strip())
        if not m or (var is not None and var != m.group(1)): return None
        var=m.group(1); vals.add(m.group(2))
    return var, vals

def excluded_countries(summary):
    marker='ASK ALL EXCEPT '; idx=summary.upper().find(marker)
    if idx < 0: return []
    txt=summary[idx+len(marker):].strip().rstrip('.')
    txt=re.sub(r'\s+AND\s+WEST BANK AND GAZA$', ', WEST BANK AND GAZA', txt, flags=re.I)
    return [x.strip(' ,') for x in txt.split(',') if x.strip(' ,')]

def build(a):
    blocked=pd.read_csv(a.blocked)
    accepted=pd.read_csv(a.accepted)
    struct=pd.read_csv(a.structure)
    routes={o['question_implementation_id']:o for o in load_jsonl(a.routing) if o.get('question_implementation_id')}
    clauses=collections.defaultdict(list)
    for o in load_jsonl(a.clauses):
        if o.get('question_implementation_id'): clauses[o['question_implementation_id']].append(o)
    contracts={(o.get('source_family'),str(o.get('wave'))):o for o in load_jsonl(a.contracts)}
    source_vars=lambda ids:[routes.get(i,{}).get('source_variable_code','') for i in ids]

    def same_respondent(row, ids):
        fam,wave=str(row['source_family']),str(row['active_wave']); c=contracts.get((fam,wave),{})
        status,unit=c.get('respondent_contract_status',''),c.get('respondent_unit',''); pages=native_pages(row)
        if fam=='LiTS' and wave=='II' and pages:
            s=struct[(struct.source_family=='LiTS')&(struct.wave.astype(str)=='II')&(struct.object_type=='SECTION_OR_MODULE_HEADING')]
            s3=s[s.source_text.astype(str).str.contains('SECTION 3 ATTITUDES AND VALUES RESPONDENT: THE PERSON SELECTED',case=False,regex=False)]
            s4=s[s.source_text.astype(str).str.contains('SECTION 4 CLIMATE CHANGE RESPONDENT: THE PERSON SELECTED',case=False,regex=False)]
            if len(s3) and len(s4):
                p3,p4=int(s3.iloc[0].page_number),int(s4.iloc[0].page_number)
                if all(p3 <= p < p4 for p in pages):
                    return True,'NATIVE_SECTION_SAME_RESPONDENT',{'section3_start_page':p3,'section4_start_page':p4,'member_pages':pages,'respondent_contract_status':status,'respondent_unit':unit,'section3_structure_object_id':s3.iloc[0].structure_object_id}
        lowu=unit.lower()
        if ('survey respondent' in lowu or 'one selected adult respondent' in lowu) and 'two questionnaire respondent roles' not in lowu and status in {'SOURCE_PROVEN','PARTIAL_SOURCE_PROVEN'}:
            return True,'SINGLE_RESPONDENT_WAVE_CONTRACT',{'respondent_contract_status':status,'respondent_unit':unit,'member_native_pages':pages}
        return False,'',{}

    anti=[]
    for _,r in blocked.iterrows():
        if str(r.get('job3_disposition'))!='BLOCKED' or boolish(r.get('candidate_scope_defect_suspected')): continue
        ids=jd(r.get('implementation_ids')) or []; rr=[routes.get(i) for i in ids]
        if len(ids)<2 or any(x is None for x in rr) or not all(x.get('routing_status')=='UNCONDITIONAL_SOURCE_PROVEN' for x in rr): continue
        fam,wave=str(r.source_family),str(r.active_wave); c=contracts.get((fam,wave))
        if not c or c.get('respondent_contract_status') not in {'SOURCE_PROVEN','PARTIAL_SOURCE_PROVEN'}: continue
        ok,ptype,pdetail=same_respondent(r,ids)
        if not ok: continue
        anti.append(dict(archetype='empirical_survives_semantic_block_or_absence',candidate_key=str(r.candidate_id),semantic_posture='BLOCKED_TYPED_RELATION',semantic_ref_id=str(r.candidate_id),source_family=fam,wave=wave,member_implementation_ids_json=compact(ids),source_variables_json=compact(source_vars(ids)),routing_statuses_json=compact([x.get('routing_status') for x in rr]),structural_allowance_proof_type=ptype,structural_allowance_proof_json=compact(pdetail),respondent_contract_status=c.get('respondent_contract_status',''),blocker_code=str(r.get('blocker_code','')),blocker_detail=str(r.get('blocker_detail','')),selection_outcome_fields_used='NONE'))
    anti=pd.DataFrame(anti)
    anti['_rank']=anti.respondent_contract_status.map({'SOURCE_PROVEN':0,'PARTIAL_SOURCE_PROVEN':1}).fillna(9)
    anti=anti.sort_values(['_rank','source_family','wave','candidate_key']).drop(columns='_rank').reset_index(drop=True)
    anti.insert(1,'frozen_rank',range(1,len(anti)+1))

    local=[]
    for _,r in accepted.iterrows():
        ids=jd(r.member_implementation_ids_json) or []; rr=[routes.get(i) for i in ids]
        if len(ids)<2 or any(x is None for x in rr): continue
        statuses=[x.get('routing_status') for x in rr]; sv=source_vars(ids)
        if all(s=='SPLIT_SAMPLE_CONDITIONAL' for s in statuses):
            parsed=[]; exprs=[]; refs=[]
            for iid in ids:
                ps=[(c,parse_or_eq(c.get('source_expression'))) for c in clauses.get(iid,[]) if c.get('source_expression')]
                ps=[(c,p) for c,p in ps if p]
                if len(ps)!=1: parsed=[]; break
                c,p=ps[0]; parsed.append(p); exprs.append(c['source_expression']); refs.append(c['clause_id'])
            if parsed and len({v for v,_ in parsed})==1 and not set.intersection(*(s for _,s in parsed)):
                local.append(dict(archetype='local_block_preserved',candidate_key=str(r.authority_id)+'::SPLIT_EMPTY_INTERSECTION',semantic_posture='GOVERNED_POSITIVE',semantic_ref_id=str(r.authority_id),source_family=str(r.source_family),wave=str(r.wave),member_implementation_ids_json=compact(ids),source_variables_json=compact(sv),routing_statuses_json=compact(statuses),routing_proof_type='EXACT_SPLIT_SAMPLE_EMPTY_INTERSECTION',routing_proof_json=compact({'control_variable':parsed[0][0],'member_allowed_values':[sorted(s) for _,s in parsed],'intersection':[],'source_expressions':exprs,'clause_ids':refs}),blocked_scopes_json=compact([{'scope_kind':'wave_configuration','scope_value':f'{r.source_family}::{r.wave}::full_relation_configuration'}]),selection_outcome_fields_used='NONE'))
        if all(s=='COUNTRY_CONDITIONAL' for s in statuses):
            summaries=[]; refs=[]
            for iid in ids:
                cs=[c for c in clauses.get(iid,[]) if c.get('condition_summary')]
                summaries.append([c['condition_summary'] for c in cs]); refs.append([c['clause_id'] for c in cs])
            common=set(summaries[0]) if summaries and summaries[0] else set()
            for xs in summaries[1:]: common &= set(xs)
            for summary in sorted(common):
                exc=excluded_countries(summary)
                if exc: local.append(dict(archetype='local_block_preserved',candidate_key=str(r.authority_id)+'::COUNTRY_EXCLUSION',semantic_posture='GOVERNED_POSITIVE',semantic_ref_id=str(r.authority_id),source_family=str(r.source_family),wave=str(r.wave),member_implementation_ids_json=compact(ids),source_variables_json=compact(sv),routing_statuses_json=compact(statuses),routing_proof_type='EXPLICIT_COMMON_COUNTRY_EXCLUSION',routing_proof_json=compact({'condition_summary':summary,'member_clause_ids':refs}),blocked_scopes_json=compact([{'scope_kind':'country','scope_value':x} for x in exc]),selection_outcome_fields_used='NONE'))
    local=pd.DataFrame(local)
    local['_rank']=local.routing_proof_type.map({'EXACT_SPLIT_SAMPLE_EMPTY_INTERSECTION':0,'EXPLICIT_COMMON_COUNTRY_EXCLUSION':1}).fillna(9)
    local=local.sort_values(['_rank','source_family','wave','semantic_ref_id']).drop(columns='_rank').reset_index(drop=True)
    local.insert(1,'frozen_rank',range(1,len(local)+1))

    freeze=pd.concat([anti,local],ignore_index=True,sort=False)
    for c in COLS:
        if c not in freeze.columns: freeze[c]=''
    freeze=freeze[COLS].fillna('')
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    freeze.to_csv(out,index=False,lineterminator='\n')
    got=sha(out)
    print(json.dumps({'anti_erase':len(anti),'local_block':len(local),'sha256':got,'expected_sha256':EXPECTED_SHA,'matches_frozen_r1':got==EXPECTED_SHA},indent=2))
    if a.require_r1 and got != EXPECTED_SHA: raise SystemExit(2)

def main():
    p=argparse.ArgumentParser()
    for name in ['blocked','accepted','routing','clauses','contracts','structure','out']:
        p.add_argument('--'+name,required=True)
    p.add_argument('--require-r1',action='store_true')
    build(p.parse_args())
if __name__=='__main__': main()
