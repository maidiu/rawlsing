from pathlib import Path
import pandas as pd,json,sys
r=Path(sys.argv[1])
p=pd.read_csv(r/'RESOLUTION/C3B7_SOURCE_NATIVE_SIBLING_POSITIVE_RR_NORM_AUTHORITY_R16C_H.csv',dtype=str,keep_default_na=False)
x=pd.read_csv(r/'QUEUE/C3B7_SOURCE_NATIVE_SIBLING_T06_LINK_OBLIGATION_ROWS_R16C_H.csv.gz',dtype=str,keep_default_na=False)
rem=pd.read_csv(r/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_H.csv',dtype=str,keep_default_na=False)
q=pd.read_csv(r/'QUEUE/R16C_H_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str,keep_default_na=False)
ctrl=pd.read_csv(r/'PROVENANCE/C3B7_HETEROGENEOUS_OBJECT_HARD_CONTROLS_R16C_H.csv',dtype=str,keep_default_na=False)
qc=pd.read_csv(r/'PROVENANCE/C3B7_CROSSWAVE_SHARED_SEMANTIC_ID_HARD_CONTROL_R16C_H.csv',dtype=str,keep_default_na=False)
s=json.load(open(r/'CURRENT_STATUS_R16C_H.json'))
keys=set(zip(x.source_family,x.wave,x.semantic_unit_id))
expected={('Asian Barometer','W4','p2xsafe__393c192afeaf72f8'),('WVS','W4','p2xsafe__5145943a4c10d3be')}
c={'p2':len(p)==2,'x49':len(x)==49 and x.opportunity_id.nunique()==49,'exact_link_keys':keys==expected,
   'r1478':len(rem)==1478,'q125_survives':((rem.source_family=='Asian Barometer')&(rem.wave=='W1')&(rem.semantic_unit_id=='p2xsafe__393c192afeaf72f8')).sum()==1,
   'q114':len(q)==114,'controls5':len(ctrl)==5,'crosswave_control1':len(qc)==1,'atoms':int(pd.to_numeric(q.decision_atom_count).sum())==33532,
   'link_total':s['c3_positive_link_rows_total']==14270,'job3':s['job3_authorized'] is False}
c={k:bool(v) for k,v in c.items()};print(json.dumps({'passed':all(c.values()),'checks':c},indent=2));sys.exit(0 if all(c.values()) else 1)
