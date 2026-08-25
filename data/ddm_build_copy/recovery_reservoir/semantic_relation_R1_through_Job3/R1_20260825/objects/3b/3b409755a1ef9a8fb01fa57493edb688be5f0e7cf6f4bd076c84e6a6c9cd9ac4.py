import pandas as pd, json, sys, subprocess, tempfile, pathlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
RET=BASE/'RETURN'
errs=[]
def req(name):
 p=RET/name
 if not p.exists(): errs.append('MISSING '+name); return None
 return p
role=req('SEMANTIC_ROLE_ASSIGNMENT.csv')
if role:
 r=pd.read_csv(role,dtype=str).fillna('')
 t=pd.read_csv(BASE/'TEMPLATES/SEMANTIC_ROLE_ASSIGNMENT.csv',dtype=str).fillna('')
 if len(r)!=len(t): errs.append(f'ROLE_ROWCOUNT {len(r)} != {len(t)}')
 keys=['source_family','wave','semantic_unit_id']
 if len(r)==len(t) and not r[keys].equals(t[keys]): errs.append('ROLE_KEYS_MUTATED')
 allowed={'YES','NO','BLOCKED','LOCKED_YES','LOCKED_NO','NA'}
 for c in ['t03_principle', 't03_application', 't04_goal', 't04_means', 't05_commitment', 't05_cost', 't06_norm', 't06_stated_intended_conduct', 't09_directional_actor_recipient', 't11_complementary_component']:
  if c not in r: errs.append('MISSING_ROLE_COL '+c); continue
  bad=~r[c].isin(allowed)
  if bad.any(): errs.append(f'BAD_ROLE_STATUS {c} {int(bad.sum())}')
  lock=t[c].str.startswith('LOCKED_')
  if lock.any() and not r.loc[lock,c].equals(t.loc[lock,c]): errs.append('LOCK_MUTATED '+c)
# compile expected candidates and compare
cand=req('CANDIDATE_ADJUDICATION.csv')
if role and cand:
 with tempfile.TemporaryDirectory() as td:
  tmp=Path(td)/'x.csv'
  subprocess.run([sys.executable,str(BASE/'CODE/compile_role_compatible_candidates.py'),str(role),str(BASE/'AUTHORITY/IMPLEMENTATION_SPINE.csv.gz'),str(tmp)],check=True,capture_output=True)
  exp=pd.read_csv(tmp,dtype=str).fillna(''); got=pd.read_csv(cand,dtype=str).fillna('')
  if set(exp.candidate_id)!=set(got.candidate_id): errs.append(f'CANDIDATE_ID_SET_MISMATCH expected={len(exp)} got={len(got)}')
  if len(got):
   allowed2={'POSITIVE_RELATION','PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP'}
   if (~got.adjudication_status.isin(allowed2)).any(): errs.append('BAD_OR_BLANK_CANDIDATE_STATUS')
   neg=got.adjudication_status=='PROVEN_NEGATIVE'
   if (got.loc[neg,'mismatch_dimension']=='').any() or (got.loc[neg,'decision_basis']=='').any(): errs.append('NEGATIVE_WITHOUT_PROOF_FIELDS')
   blk=got.adjudication_status=='BLOCKED_AUTHORITY_GAP'
   if (got.loc[blk,'authority_gap']=='').any(): errs.append('BLOCK_WITHOUT_AUTHORITY_GAP')
   pos=got.adjudication_status=='POSITIVE_RELATION'
   if (got.loc[pos,'relation_id_if_positive']=='').any() or (got.loc[pos,'decision_basis']=='').any(): errs.append('POSITIVE_WITHOUT_RELATION_OR_BASIS')
# source object
op=req('SOURCE_OBJECT_RULE_REVIEW.csv')
if op:
 g=pd.read_csv(op,dtype=str).fillna(''); t=pd.read_csv(BASE/'TEMPLATES/SOURCE_OBJECT_RULE_REVIEW.csv',dtype=str).fillna('')
 if len(g)!=len(t): errs.append('SOURCE_OBJECT_ROWCOUNT')
 ok={'POSITIVE_STRUCTURE','PROVEN_NEGATIVE','BLOCKED_AUTHORITY_GAP','NOT_APPLICABLE','RETAIN_EXISTING_GOVERNED_AUTHORITY'}
 if len(g) and (~g.worker_structure_status.isin(ok)).any(): errs.append('BAD_OR_BLANK_SOURCE_OBJECT_STATUS')
 neg=g.worker_structure_status=='PROVEN_NEGATIVE' if len(g) else []
 if len(g) and ((g.loc[neg,'mismatch_dimension']=='').any() or (g.loc[neg,'decision_basis']=='').any()): errs.append('OBJECT_NEGATIVE_WITHOUT_PROOF')
 blk=g.worker_structure_status=='BLOCKED_AUTHORITY_GAP' if len(g) else []
 if len(g) and (g.loc[blk,'authority_gap']=='').any(): errs.append('OBJECT_BLOCK_WITHOUT_GAP')
# canaries
cp=req('CANARY_RECALL.csv')
if cp:
 c=pd.read_csv(cp,dtype=str).fillna('')
 if len(c) and (~c.worker_recall_status.isin({'RETAIN_EXISTING_GOVERNED_AUTHORITY','REDISCOVERED_POSITIVE'})).any(): errs.append('CANARY_RECALL_FAILURE')
# coverage
cv=req('RULE_WAVE_COVERAGE.csv')
if cv:
 c=pd.read_csv(cv,dtype=str).fillna('')
 if len(c)!=54: errs.append('COVERAGE_ROWCOUNT')
 if (c.semantic_role_scan_complete!='YES').any(): errs.append('SEMANTIC_SCAN_NOT_COMPLETE')
 if (c.source_object_scan_complete!='YES').any(): errs.append('OBJECT_SCAN_NOT_COMPLETE')
 if (c.coverage_status=='').any(): errs.append('BLANK_COVERAGE_STATUS')
# relation implementations
ri=req('RELATION_IMPLEMENTATIONS.csv')
if ri:
 x=pd.read_csv(ri,dtype=str).fillna('')
 if len(x) and x.relation_id.duplicated().any(): errs.append('DUP_RELATION_ID')
 if len(x) and (~x.rule_id.isin({f'T{i:02d}' for i in range(3,12)})).any(): errs.append('BAD_RULE_ID')
# required auxiliary files
for n in ['EXPLICIT_ANTIJOINS.csv','AUTHORITY_GAPS.csv','PROPAGATION_LEDGER.csv','HOSTILE_QA.csv']:
 req(n)
print(json.dumps({'worker':'S14W04','status':'PASS' if not errs else 'FAIL','errors':errs},indent=2))
sys.exit(1 if errs else 0)
