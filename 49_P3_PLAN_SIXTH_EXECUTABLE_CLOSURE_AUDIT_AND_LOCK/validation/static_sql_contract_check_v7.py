from __future__ import annotations
from pathlib import Path
import json,re,sys

FORBIDDEN = {
  'direct_pair_fact_id':'stale internal-pair column',
  'e.pair_fact_id':'component edge has projection_id, not pair_fact_id',
  'candidate_family_id IS NULL':'stale lineage-disposition candidate column',
  "membership_role NOT IN ('PROPOSED_MEMBER','HIERARCHICAL_RELATIVE')":'stale membership vocabulary',
  'r.canonical_family_revision_id':'stale canonical revision column',
}

def _table_columns(sql:str):
    out={}
    for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',sql,re.I|re.S):
        table,body=m.group(1),m.group(2)
        cols=set()
        depth=0; start=0; parts=[]
        for i,ch in enumerate(body):
            if ch=='(': depth+=1
            elif ch==')': depth-=1
            elif ch==',' and depth==0:
                parts.append(body[start:i]); start=i+1
        parts.append(body[start:])
        for part in parts:
            token=part.strip().split(None,1)[0].strip('"') if part.strip() else ''
            if token.upper() not in {'PRIMARY','FOREIGN','UNIQUE','CHECK','CONSTRAINT','EXCLUDE'} and re.match(r'^\w+$',token): cols.add(token)
        out[table]=cols
    return out

def check(ddl_path,queries_path):
    ddl=Path(ddl_path).read_text(); queries=Path(queries_path).read_text(); issues=[]
    if len(re.findall(r'^BEGIN;\s*$',ddl,re.M))!=1: issues.append('DDL must contain exactly one top-level BEGIN')
    roll=[m.start() for m in re.finditer(r'^ROLLBACK;\s*$',ddl,re.M)]
    if len(roll)!=1: issues.append('DDL must contain exactly one top-level ROLLBACK')
    elif ddl[roll[0]+len('ROLLBACK;'):].strip(): issues.append('ROLLBACK must be the final executable statement')
    cols=_table_columns(ddl)
    for m in re.finditer(r'ALTER TABLE\s+(\w+).*?FOREIGN KEY\s*\((\w+)\)',ddl,re.I):
        table,col=m.groups()
        if table in cols and col not in cols[table]: issues.append(f'ALTER TABLE references missing column {table}.{col}')
    for token,msg in FORBIDDEN.items():
        if token in ddl or token in queries: issues.append(f'{msg}: {token}')
    required={
      'p3_candidate_revision':{'origin_key'},
      'p3_candidate_status_event':{'occurred_at'},
      'p3_component_connectivity_edge':{'projection_id'},
      'p3_internal_pair_matrix':{'direct_pair_projection_id'},
    }
    for table,need in required.items():
        missing=need-cols.get(table,set())
        if missing: issues.append(f'{table} missing required columns {sorted(missing)}')
    required_snippets=[
      'JOIN p3_pair_projection pr ON pr.projection_id=e.projection_id',
      'LEFT JOIN p3_pair_projection pr ON pr.projection_id=x.direct_pair_projection_id',
      'p3_candidate_origin_revision_closure',
      'p3_adjudication_partition_decision_closure',
      'PERFORM p3_assert_candidate_origin(rid)',
      'PERFORM p3_assert_adjudication_member_partition(aid)',
      'PERFORM p3_assert_split_result_partition(aid)',
      'PERFORM p3_assert_canonical_promotion_closure(aid)',
    ]
    for snippet in required_snippets:
        if snippet not in ddl: issues.append(f'missing executable closure wiring: {snippet}')
    return {'status':'PASS' if not issues else 'FAIL','issues':issues,'table_count':len(cols),'rollback_count':len(roll)}

if __name__=='__main__':
    result=check(sys.argv[1],sys.argv[2]); print(json.dumps(result,indent=2)); raise SystemExit(0 if result['status']=='PASS' else 1)
