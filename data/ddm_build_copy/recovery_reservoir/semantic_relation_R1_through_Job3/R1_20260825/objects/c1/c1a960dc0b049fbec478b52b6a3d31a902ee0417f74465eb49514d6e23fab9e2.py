from pathlib import Path
import pandas as pd, json, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
led=pd.read_csv(root/'RESOLUTION/C3A_RR_NORM_NEGATIVE_AND_RESIDUAL_LEDGER_R16C_A.csv').fillna('')
neg=pd.read_csv(root/'RESOLUTION/C3A_NEGATIVE_RR_NORM_AUTHORITY_R16C_A.csv').fillna('')
res=pd.read_csv(root/'QUEUE/C3A_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_A.csv').fillna('')
q=pd.read_csv(root/'QUEUE/R16C_A_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv')
a=pd.read_csv(root/'RESOLUTION/C3A_SOURCE_WAVE_ACCOUNTING_R16C_A.csv')
checks={
'ledger_3119':len(led)==3119,
'partition_1411_1708':len(neg)==1411 and len(res)==1708 and len(neg)+len(res)==len(led),
'unique_parent_keys':led[['source_family','wave','semantic_unit_id']].duplicated().sum()==0,
'all_neg_authority':(neg.c3a_authority_ceiling=='NEGATIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY').all(),
'all_residual_fail_closed':(res.c3a_authority_ceiling=='NO_T06_ABSENCE_CLAIM').all(),
'primitive_accounting':int(a.parent_blocked_primitive_rows.sum())==209121 and int(a.c3a_closed_primitive_rows.sum())==88392 and int(a.c3a_residual_primitive_rows.sum())==120729,
'32_source_wave_cells':len(a)==32 and len(res.groupby(['source_family','wave']))==32,
'central_88':len(q)==88,
'central_atoms_33600':int(q.decision_atom_count.sum())==33600,
't06_residual_atoms_1708':int(q[q.work_family=='T06_NORM_ROLE_BLOCKER'].decision_atom_count.sum())==1708,
't07_12':int(q[q.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12,
'job3_false':json.load(open(root/'CURRENT_STATUS_R16C_A.json'))['job3_authorized'] is False,
}
checks={k:bool(v) for k,v in checks.items()}
print(json.dumps({'passed':all(checks.values()),'n_checks':len(checks),'checks':checks},indent=2))
sys.exit(0 if all(checks.values()) else 1)
