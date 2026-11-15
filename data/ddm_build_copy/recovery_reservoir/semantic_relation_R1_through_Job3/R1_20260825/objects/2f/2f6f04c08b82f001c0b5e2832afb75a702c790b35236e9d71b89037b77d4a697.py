from pathlib import Path
import pandas as pd
PARENT=Path('/mnt/data/r16c_q')
key=['source_family','wave','semantic_unit_id']
res=pd.read_csv(PARENT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_Q.csv').fillna('')
res['wave']=res['wave'].astype(str)
front=pd.read_csv(PARENT/'PROVENANCE/C3B16_PRESERVED_BOUNDARY_FRONTIER_R16C_Q.csv').fillna('')
front['wave']=front['wave'].astype(str)
assert len(res)==390 and len(front)==390

# Non-proposition edge front: exact positive exceptions. Every other non-proposition edge
# is negative under the refined approval doctrine, after source/content review.
EDGE_POS=[
 ('Arab Barometer','I','q2454'),
 ('Arab Barometer','VIII','QPAL21'),
 ('GSS','2024','experts'),
 ('LiTS','IV','q836f'),
 ('WVS','W1','V115'),
 ('WVS','W1','V113'),
 ('WVS','W4','V131'),
]
edge=front[front['is_prop_boundary'].astype(str).str.lower().eq('false')].copy()
assert len(edge)==147
edge_pos=pd.DataFrame(columns=edge.columns)
for sf,wv,code in EDGE_POS:
 x=edge[(edge.source_family==sf)&(edge.wave==str(wv))&(edge.source_variable_code==code)]
 assert len(x)==1,(sf,wv,code,len(x))
 edge_pos=pd.concat([edge_pos,x],ignore_index=True)
edge_pos_keys=set(map(tuple,edge_pos[key].astype(str).values.tolist()))
edge_neg=edge[~pd.MultiIndex.from_frame(edge[key].astype(str)).isin(pd.MultiIndex.from_tuples(list(edge_pos_keys),names=key))].copy()
assert len(edge_pos)==7 and len(edge_neg)==140

# Proposition-boundary front indexed in a fixed source/wave order recovered from Q.
pb=front[front['is_prop_boundary'].astype(str).str.lower().eq('true')].copy().reset_index(drop=True)
assert len(pb)==243
pb['pb_i']=range(len(pb))
# Positive RR_NORM: explicit norm/obligation/permission/rejection/approval about an action,
# rule, role, policy, social/political arrangement, or explicit epistemic/religious rule.
PB_POS_I={
 5,6,12,14,16,18,21,29,30,31,36,40,41,49,53,71,73,89,97,
 108,126,130,158,181,182,185,210,230
}
# Fail-closed source-shorthand residuals. Exact stem/polarity is not sufficiently recovered
# to distinguish normative approval from descriptive or conduct/cost semantics.
PB_RESID_I={
 3,9,51,65,74,78,110,113,116,122,124,129,141,143,144,155,169
}
assert PB_POS_I.isdisjoint(PB_RESID_I)
pb_pos=pb[pb.pb_i.isin(PB_POS_I)].copy()
pb_resid=pb[pb.pb_i.isin(PB_RESID_I)].copy()
pb_neg=pb[~pb.pb_i.isin(PB_POS_I|PB_RESID_I)].copy()
assert len(pb_pos)==28 and len(pb_resid)==17 and len(pb_neg)==198

P=pd.concat([edge_pos,pb_pos.drop(columns=['pb_i'])],ignore_index=True)
N=pd.concat([edge_neg,pb_neg.drop(columns=['pb_i'])],ignore_index=True)
remaining=pb_resid.drop(columns=['pb_i']).copy()
# preserve original 15-column residual schema only
base_cols=res.columns.tolist()
P=P[base_cols]; N=N[base_cols]; remaining=remaining[base_cols]
P['wave']=P.wave.astype(str); N['wave']=N.wave.astype(str); remaining['wave']=remaining.wave.astype(str)
selected=pd.concat([P.assign(_decision='POSITIVE_RR_NORM'),N.assign(_decision='NEGATIVE_RR_NORM')],ignore_index=True)
# exact partition
assert len(P)==35 and len(N)==338 and len(selected)==373 and len(remaining)==17
assert not selected.duplicated(key).any()
assert not remaining.duplicated(key).any()
assert set(map(tuple,selected[key].astype(str).values.tolist())).isdisjoint(set(map(tuple,remaining[key].astype(str).values.tolist())))
assert set(map(tuple,selected[key].astype(str).values.tolist()))|set(map(tuple,remaining[key].astype(str).values.tolist())) == set(map(tuple,res[key].astype(str).values.tolist()))
