#!/usr/bin/env python3
"""Validate immutable original S1-S5 returns against all five six-axis regrade returns.

Historical Git blobs are read as untrusted DATA only; never import/execute branch code.
A passing machine receipt proves roster, row and structural custody, not scientific merit.
"""
from __future__ import annotations
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

SHARDS = {
  "S1": ("c85db39772a8ac09fd70c6bb94a39dd04274d2cb","6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5",175,1279),
  "S2": ("ab303ee446c87beca32dc2c322704f6cf0dc7b79","3042fca8a2165e07871d408118e1741686020cdc",175,218),
  "S3": ("65b83dee3385fc85d5d283c19acd270dea50a27d","ebdb51a5c79209b2e552cfce648f7847b19386c2",174,398),
  "S4": ("8f4ad92aa47b7ae53d625bc2587357092af96e27","d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb",161,897),
  "S5": ("1aa0407869620cd8ba2e8ca1f1533b99fd097162","32dac59b3741dcc54f507321c7826e65174af372",160,343),
}
ROSTER="becf0bfb04705b8fe0927dd56e7290e1dcd180a8"
ROOT=Path(__file__).resolve().parents[2]
def g(*args):
    p=subprocess.run(["git", *args],cwd=ROOT,capture_output=True,check=False)
    if p.returncode: raise RuntimeError("git object failed "+repr(args[:3])+p.stderr.decode(errors="replace")[-180:])
    return p.stdout
def rows(sha,path):
    return [json.loads(line) for line in g("show",sha+":"+path).splitlines() if line.strip()]
def records(sha,path):
    return json.loads(g("show",sha+":"+path))
def find_name(row):
    for k in ("branch","branch_name","branch_ref","original_branch","name"):
        if isinstance(row.get(k),str) and row[k]:return row[k]
    return None
def first(row,ks):
    for k in ks:
        if k in row:return row[k]
    return None
def canonical(row):
    return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def main():
    out=[];errors=[]
    for s,(old,new,nb,nf) in SHARDS.items():
        initial=f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/{s}"
        repair=f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/{s}_EVIDENCE_REPAIR"
        old_f=rows(old,initial+"/FUNCTION_COURT.jsonl")
        new_f=rows(new,repair+"/FUNCTION_GRADE_CORRECTIONS.jsonl")
        old_b=rows(old,initial+"/BRANCH_DISPOSITIONS.jsonl")
        new_b=rows(new,repair+"/BRANCH_RECONCILIATION.jsonl")
        roster=records(ROSTER, f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/SCOPED_ROSTER/11_{s}_HEAD_ONLY_ROSTER.json")["branch_heads"]
        expected={r["branch"]:r["tip_sha"] for r in roster}
        seen=[find_name(r) for r in new_b]
        fissues=[];bissues=[]
        if len(old_f)!=nf or len(new_f)!=nf:fissues.append("FUNCTION_ROW_COUNT")
        if len(old_b)!=nb or len(new_b)!=nb:bissues.append("BRANCH_ROW_COUNT")
        if len(set(seen))!=len(seen) or set(seen)!=set(expected):bissues.append("BRANCH_NAME_CUSTODY")
        if len(set(find_name(r) for r in old_b))!=nb:bissues.append("ORIGINAL_BRANCH_CUSTODY")
        bad_tips=0
        for row in new_b:
            name=find_name(row)
            tip=first(row,("tip_sha","original_tip_sha","pinned_tip","tip"))
            if tip is not None and expected.get(name)!=tip:bad_tips+=1
        if bad_tips:bissues.append(f"WRONG_TIPS_{bad_tips}")
        same_id=0;missing_hash=0;hash_fails=0;key_mismatch=0
        for j,(o,n) in enumerate(zip(old_f,new_f)):
            oid=first(o,("function_id","id","symbol_id"))
            nid=first(n,("original_function_id","function_id","original_id","id"))
            if oid is not None and nid is not None and oid==nid:same_id+=1
            elif oid is not None and nid is not None and oid!=nid:key_mismatch+=1
            digest=first(n,("original_row_sha256","source_original_row_sha256","original_sha256"))
            if digest:
                if digest not in (canonical(o), hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=True).encode()).hexdigest(),hashlib.sha256(json.dumps(o,sort_keys=True).encode()).hexdigest()):
                    hash_fails+=1
            else:missing_hash+=1
        if key_mismatch:fissues.append(f"ROW_KEYS_MISMATCH_{key_mismatch}")
        # Hash-representation variations explicitly reported, not accepted as proof of defect.
        if hash_fails:fissues.append(f"ROW_HASH_FORMAT_OR_MISMATCH_{hash_fails}")
        cf=collections.Counter()
        for item in new_f:
            st=first(item,("corrected_disposition","corrected_primary_label","corrected_label","CORRECTED_OUTCOME","disposition"))
            if st:cf[str(st)]+=1
        status_suspicious=collections.Counter()
        adoption_axis=collections.Counter()
        presence_axis=collections.Counter()
        contested_examples=[]
        for k,item in enumerate(new_f):
            axes=item.get("corrected_axes",{})
            if isinstance(axes,dict):
                for key in ("ADOPTION","CURRENT_FUNCTIONAL_PRESENCE"):
                    v=axes.get(key)
                    if isinstance(v,str):
                        (adoption_axis if key=="ADOPTION" else presence_axis)[v]+=1
                    elif isinstance(v,dict):
                        for vv in v.values():
                            if isinstance(vv,str) and ("CURRENT_PRODUCTION_ACCEPTED" in vv or "RENAMED_EQUIVALENT_PROVEN" in vv):
                                contested_examples.append({"ordinal":k+1,"axis":key,"value":vv,"original_path":item.get("original_path"),"symbol":item.get("original_symbol") or item.get("symbol"),"proof_sources":item.get("proof_sources",[])[:2]})
            if len(contested_examples)>8:
                break
        
        for item in new_f:
            t=json.dumps(item,sort_keys=True,ensure_ascii=True)
            for term in ("CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE","RENAMED_EQUIVALENT_PROVEN","READY_FOR_SOURCEFREE_INTEGRATION_COURT","SUPERSEDED_BETTER"):
                if term in t:status_suspicious[term]+=1
        report={"shard":s,"original_ref":old,"corrected_ref":new,"expected_branch_rows":nb,
                "original_branch_rows":len(old_b),"correction_branch_rows":len(new_b),
                "original_function_rows":len(old_f),"correction_function_rows":len(new_f),
                "original_function_id_alignment":same_id,"misaligned_function_ids":key_mismatch,
                "missing_original_row_hash":missing_hash,"hash_format_or_mismatch":hash_fails,
                "bad_tip_count":bad_tips,"function_row_schema_first":list(new_f[0]) if new_f else [],
                "original_row_schema_first":list(old_f[0]) if old_f else [],
                "adoption_axis_actual_values":dict(adoption_axis),
                "presence_axis_actual_values":dict(presence_axis),
                "contested_axis_examples":contested_examples,
                "branch_row_schema_first":list(new_b[0]) if new_b else [],
                "corrected_labels":dict(cf),"potential_overclaim_string_occurrences":dict(status_suspicious),
                "errors":fissues+bissues,
                "SCIENTIFIC_OR_ADOPTION_ACCEPTANCE":False}
        if report["errors"]:errors.append({"shard":s,"reasons":report["errors"]})
        out.append(report)
    artifact={"schema":"PYAT_845_RETURN_REGRADE_INDEPENDENT_SOURCE_IDENTITY@1",
              "frozen_roster":ROSTER,"branches_expected":845,
              "all_original_function_rows":3135,"actual_corrected_rows":sum(x["correction_function_rows"] for x in out),
              "branch_rows":sum(x["correction_branch_rows"] for x in out),
              "mechanical_custody_pass":not errors,
              "rows":out,"machine_errors":errors,
              "not_current_abi_or_science_or_first_consumer_test":True}
    dst=Path("pyat-regrade-acceptance")
    dst.mkdir(exist_ok=True)
    (dst/"REGRADES_VS_ORIGINAL_REPORT.json").write_text(json.dumps(artifact,indent=2),encoding="utf-8")
    print(json.dumps({"schema":artifact["schema"],"branches":artifact["branch_rows"],"function_rows":artifact["actual_corrected_rows"],"pass":artifact["mechanical_custody_pass"],"rows":[{k:v for k,v in r.items() if k in ("shard","original_function_id_alignment","misaligned_function_ids","missing_original_row_hash","hash_format_or_mismatch","bad_tip_count","potential_overclaim_string_occurrences","adoption_axis_actual_values","presence_axis_actual_values","contested_axis_examples","original_row_schema_first","errors")} for r in out]},indent=2))
    raise SystemExit(2 if errors else 0)
if __name__=="__main__":main()
