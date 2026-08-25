import pandas as pd, json, hashlib, sys
from itertools import product
role_path, spine_path, out_path=sys.argv[1:4]
r=pd.read_csv(role_path,dtype=str).fillna('')
s=pd.read_csv(spine_path,dtype=str,low_memory=False).fillna('')
YES={'YES','LOCKED_YES'}
rows=[]
def cid(parts): return 'R16D-CAND-'+hashlib.sha256('|'.join(parts).encode()).hexdigest()[:20]
def add(sf,w,rule,branch,l='',rr='',ep='',basis=''):
    rows.append(dict(candidate_id=cid([sf,w,rule,branch,l,rr,ep]),source_family=sf,wave=w,rule_id=rule,branch=branch,left_semantic_unit_id=l,right_semantic_unit_id=rr,right_endpoint_implementation_id=ep,candidate_basis=basis,adjudication_status='',mismatch_dimension='',authority_gap='',relation_id_if_positive='',decision_basis='',evidence_refs_json='',propagation_rule_id='',confidence=''))
for (sf,w),g in r.groupby(['source_family','wave'],sort=False):
    def ids(c): return sorted(g.loc[g[c].isin(YES),'semantic_unit_id'].astype(str).unique())
    pairs=[('T03','PRINCIPLE_APPLICATION','t03_principle','t03_application'),('T04','GOAL_MEANS','t04_goal','t04_means'),('T05','COMMITMENT_COST','t05_commitment','t05_cost'),('T06','STATED_INTENDED','t06_norm','t06_stated_intended_conduct'),('T09','RECIPROCAL_DIRECTION','t09_directional_actor_recipient','t09_directional_actor_recipient'),('T11','COMPLEMENTARY_COMPONENTS','t11_complementary_component','t11_complementary_component')]
    for rule,branch,a,b in pairs:
        A,B=ids(a),ids(b)
        for x in A:
            for y in B:
                if x==y: continue
                # for symmetric candidate shores dedupe order
                if rule in {'T09','T11'} and x>y: continue
                add(str(sf),str(w),rule,branch,x,y,'','ROLE_COMPATIBLE_EXHAUSTIVE_WITHIN_SOURCE_WAVE')
    norms=ids('t06_norm')
    eps=s[(s.source_family==sf)&(s.wave==w)&(s.o04__central_s2b_disposition=='ACCEPT_ENDPOINT')]['question_implementation_id'].astype(str).unique()
    for n in norms:
        for ep in sorted(eps): add(str(sf),str(w),'T06','REALIZED_O04_ENDPOINT',n,'',ep,'RR_NORM_X_ALL_ACCEPTED_O04_ENDPOINTS')
out=pd.DataFrame(rows).drop_duplicates('candidate_id').sort_values(['source_family','wave','rule_id','branch','candidate_id']) if rows else pd.DataFrame(columns=['candidate_id','source_family','wave','rule_id','branch','left_semantic_unit_id','right_semantic_unit_id','right_endpoint_implementation_id','candidate_basis','adjudication_status','mismatch_dimension','authority_gap','relation_id_if_positive','decision_basis','evidence_refs_json','propagation_rule_id','confidence'])
out.to_csv(out_path,index=False)
print(json.dumps({'rows':len(out),'by_rule':out.rule_id.value_counts().to_dict() if len(out) else {}},indent=2))
