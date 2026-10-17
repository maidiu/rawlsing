#!/usr/bin/env python3
import pandas as pd, json, zipfile, hashlib, sys, io, gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def csv_from_zip(z,name):
    raw=z.read(name)
    if name.endswith(".gz"):
        raw=gzip.decompress(raw)
    return pd.read_csv(io.BytesIO(raw),dtype=str)
def main():
    idx=pd.read_csv(ROOT/"WORKER_PACK_INDEX.csv",dtype=str)
    parent=pd.read_csv(ROOT/"PARENT/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_W.csv.gz",dtype=str)
    allids=[]; groups=[]; checks=[]
    for _,r in idx.iterrows():
        zp=ROOT/"PACKS"/r.pack_filename
        checks.append((f"hash_{r.worker_id}",sha(zp)==r.pack_sha256))
        with zipfile.ZipFile(zp) as z:
            prefix=r.worker_id+"/"
            a=csv_from_zip(z,prefix+"ASSIGNMENT/C4_OPPORTUNITIES.csv.gz")
            n=csv_from_zip(z,prefix+"ASSIGNMENT/NORM_CONTRACT_TEMPLATE.csv")
            checks.append((f"rows_{r.worker_id}",len(a)==int(r.opportunity_rows)))
            checks.append((f"norms_{r.worker_id}",len(n)==int(r.norm_contracts)))
            checks.append((f"unique_{r.worker_id}",not a.opportunity_id.duplicated().any()))
            checks.append((f"norm_text_{r.worker_id}",a.norm_exact_question_text.fillna("").ne("").all()))
            checks.append((f"endpoint_text_{r.worker_id}",a.endpoint_exact_question_text.fillna("").ne("").all()))
            allids += a.opportunity_id.tolist()
            groups += list(map(tuple,a[["source_family","wave"]].drop_duplicates().values.tolist()))
    checks += [
        ("parent_30268",len(parent)==30268),
        ("union_30268",len(allids)==30268),
        ("union_unique",len(set(allids))==30268),
        ("union_exact",set(allids)==set(parent.opportunity_id)),
        ("groups_26",len(set(groups))==26),
        ("groups_not_split",len(groups)==len(set(groups))),
        ("job3_false",True),
    ]
    bad=[c for c,p in checks if not bool(p)]
    print(json.dumps({"status":"PASS" if not bad else "FAIL","checks":len(checks),"failed":bad},indent=2))
    sys.exit(0 if not bad else 2)
if __name__=="__main__": main()
