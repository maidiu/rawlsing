from pathlib import Path
import pandas as pd,json,sys
r=Path(sys.argv[1])
pos=pd.read_csv(r/'RESOLUTION/C3B1_CIVIL_LIBERTY_POSITIVE_RR_NORM_AUTHORITY_R16C_B.csv')
res=pd.read_csv(r/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_B.csv')
link=pd.read_csv(r/'QUEUE/C3B1_CIVIL_LIBERTY_T06_LINK_OBLIGATION_ROWS_R16C_B.csv.gz')
q=pd.read_csv(r/'QUEUE/R16C_B_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv')
c={'pos98':len(pos)==98,'res1610':len(res)==1610,'links9380':len(link)==9380,'queue96':len(q)==96,'atoms33600':int(q.decision_atom_count.sum())==33600,'no_relation_authority':link.r16c_b_authority_ceiling.eq('NO_T06_RELATION_AUTHORITY_YET').all(),'job3false':json.load(open(r/'CURRENT_STATUS_R16C_B.json'))['job3_authorized'] is False}
c={k:bool(v) for k,v in c.items()};print(json.dumps({'passed':all(c.values()),'n_checks':len(c),'checks':c},indent=2));sys.exit(0 if all(c.values()) else 1)
