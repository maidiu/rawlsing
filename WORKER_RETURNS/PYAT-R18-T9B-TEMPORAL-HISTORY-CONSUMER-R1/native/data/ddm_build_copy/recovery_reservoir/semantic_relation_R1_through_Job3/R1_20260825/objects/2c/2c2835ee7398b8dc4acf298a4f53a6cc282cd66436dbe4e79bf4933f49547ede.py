from pathlib import Path
import pandas as pd, json, hashlib, sys
P=Path(__file__).resolve().parent
errs=[]
led=pd.read_csv(P/'JOB3_R3_TERMINAL_DECISION_LEDGER_R1.csv',dtype=str).fillna('')
acc=pd.read_csv(P/'JOB3_R3_ACCEPTED_RELATION_AUTHORITY_R1.csv',dtype=str).fillna('')
rej=pd.read_csv(P/'JOB3_R3_REJECTED_CANDIDATE_LEDGER_R1.csv',dtype=str).fillna('')
blk=pd.read_csv(P/'JOB3_R3_BLOCKED_CANDIDATE_LEDGER_R1.csv',dtype=str).fillna('')
obs=pd.read_csv(P/'O12_R3_SUCCESSOR_OBLIGATIONS_FROM_JOB3_R1.csv',dtype=str).fillna('')
fin=pd.read_csv(P/'JOB3_R3_FINAL_GOVERNED_RELATION_TOPOLOGY_R1.csv',dtype=str).fillna('')
den=pd.read_csv(P/'FROZEN_INPUTS/O12_JOB3_CANDIDATE_DENOMINATOR_T15_SUCCESSOR_R3.csv',dtype=str).fillna('')
gov=pd.read_csv(P/'FROZEN_INPUTS/O12_EXISTING_GOVERNED_RELATION_TOPOLOGY_R3.csv',dtype=str).fillna('')
if len(led)!=1264 or led.candidate_id.nunique()!=1264: errs.append('terminal ledger cardinality')
if set(led.candidate_id)!=set(den.candidate_id): errs.append('denominator exact-set mismatch')
vc=led.job3_disposition.value_counts().to_dict()
if vc!={'REJECT':697,'ACCEPT':552,'BLOCKED':15}: errs.append('disposition counts '+str(vc))
if len(acc)!=552 or acc.authority_id.nunique()!=552: errs.append('accepted authority count/id')
if len(rej)!=697 or len(blk)!=15: errs.append('reject/block count')
flag=led.candidate_scope_defect_suspected.str.lower().isin(['true','1','yes','y'])
if flag.sum()!=125 or not (led.loc[flag,'job3_disposition']=='REJECT').all(): errs.append('scope flag discipline')
if len(obs)!=125 or set(obs.candidate_id)!=set(led.loc[flag,'candidate_id']): errs.append('successor obligations')
if len(gov)!=638 or len(fin)!=1190 or fin.authority_id.nunique()!=1190: errs.append('final topology cardinality')
if set(gov.authority_id)-set(fin.authority_id): errs.append('existing authority not preserved')
if set(acc.authority_id)-set(fin.authority_id): errs.append('new authority absent final topology')
if (acc.relation_type=='').any() or (acc.semantic_rationale=='').any(): errs.append('accepted semantic fields blank')
if (blk.blocker_code=='').any() or (blk.blocker_detail=='').any(): errs.append('blocked detail blank')
status={'status':'PASS' if not errs else 'FAIL','errors':errs,'error_count':len(errs),'candidate_count':len(led),'accepted':len(acc),'rejected':len(rej),'blocked':len(blk),'scope_defect_obligations':len(obs),'final_positive_topology':len(fin)}
print(json.dumps(status,indent=2))
sys.exit(1 if errs else 0)
