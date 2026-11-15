#!/usr/bin/env python3
"""Rebuild R16C-T C4a from R16C-S parent artifacts and R10A spine."""
import argparse, pandas as pd, zipfile, io, hashlib
from pathlib import Path
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--parent-links", required=True); ap.add_argument("--parent-positive", required=True)
    ap.add_argument("--parent-queue", required=True); ap.add_argument("--r10a-zip", required=True); ap.add_argument("--out", required=True)
    a=ap.parse_args(); out=Path(a.out); (out/"RESOLUTION").mkdir(parents=True,exist_ok=True); (out/"QUEUE").mkdir(parents=True,exist_ok=True)
    links=pd.read_csv(a.parent_links); pos=pd.read_csv(a.parent_positive); queue=pd.read_csv(a.parent_queue)
    mask=(links.source_family=="South Asia")&(links.wave.astype(str)=="W1")
    resolved=links.loc[mask].copy(); remaining=links.loc[~mask].copy()
    assert len(resolved)==9 and resolved.semantic_unit_id.nunique()==1
    norm=pos[(pos.source_family=="South Asia")&(pos.wave.astype(str)=="W1")]
    assert len(norm)==1 and norm.iloc[0].source_variable_code=="c17"
    with zipfile.ZipFile(a.r10a_zip) as z:
        name=[n for n in z.namelist() if n.endswith("SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz")][0]
        spine=pd.read_csv(io.BytesIO(z.read(name)),compression="gzip",low_memory=False)
    ep=spine[["question_implementation_id","source_variable_code","exact_question_text","o04__s2b_actor","o04__s2b_target","o04__s2b_action_or_exposure"]].drop_duplicates("question_implementation_id")
    neg=resolved.merge(ep,left_on="endpoint_implementation_id",right_on="question_implementation_id",how="left")
    assert neg.exact_question_text.notna().all()
    neg.insert(0,"t06_relation_authority_id",[f"T06NEG-R16CT-{hashlib.sha256(x.encode()).hexdigest()[:16]}" for x in neg.opportunity_id])
    neg["relation_disposition"]="NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL"
    neg["authority_ceiling"]="EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE"
    neg.to_csv(out/"RESOLUTION/C4A_T06_NEGATIVE_RELATION_AUTHORITY_R16C_T_REBUILD.csv",index=False)
    remaining.to_csv(out/"QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_T_REBUILD.csv.gz",index=False,compression="gzip")
    qmask=(queue.work_family=="T06_RR_NORM_POSITIVE_LINK_REVIEW")&(queue.source_family=="South Asia")&(queue.wave.astype(str)=="W1")
    assert qmask.sum()==1
    queue.loc[~qmask].to_csv(out/"QUEUE/R16C_T_VOZHD_CENTRAL_QUEUE_SUCCESSOR_REBUILD.csv",index=False)
if __name__=="__main__": main()
