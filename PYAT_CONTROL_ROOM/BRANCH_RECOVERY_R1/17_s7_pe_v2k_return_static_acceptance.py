#!/usr/bin/env python3
"""Exact original Git-object source/receipt custody, no candidate code execution.
PASS asserts integrity of machine records, not behavior, authority or adoption.
"""
from __future__ import annotations
import collections,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
S7="026ca72c24d564d4dc203f68385df8c75b4bd3a7"
PE="9c030bf4c239d2e14f2b5a8a02ff7b44906cd0c7"
V2K="dd1c15063672787eaf6834161c03008fd62a0b0a"
def raw(sha,path):
    v=subprocess.run(["git","show",sha+":"+path],cwd=ROOT,capture_output=True)
    if v.returncode:raise RuntimeError("missing Git object "+sha+":"+path)
    return v.stdout
def lines(sha,path):return [json.loads(s) for s in raw(sha,path).splitlines() if s.strip()]
def doc(sha,path):return json.loads(raw(sha,path))
def main():
    sp="PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7/"
    pp="WORKER_RETURNS/PYAT-R3-PE-SC0-EIGHT-STRICT-REPAIR/"
    vp="WORKER_RETURNS/PYAT-R3-V2K-CURRENT-ABI-DECISION/"
    family=lines(S7,sp+"FUNCTION_FAMILY_FINAL_DISPOSITIONS.jsonl")
    blockers=lines(S7,sp+"OPEN_COMPATIBILITY_BLOCKERS.jsonl")
    account=doc(S7,sp+"845_BRANCH_ACCOUNTING.json")
    pe=lines(PE,pp+"EIGHT_STRICT_ASSERTION_ADJUDICATION.jsonl")
    results=doc(PE,pp+"repro/test_summary.json")
    v2k=lines(V2K,vp+"HISTORICAL_FUNCTION_VS_R61_CONTRACT.jsonl")
    junit_checks={}
    for k in ("author_21.junit.xml","original_strict_4_of_13.junit.xml","strict_13.junit.xml","overlay_faults.junit.xml"):
        v=results[k];junit_checks[k]={z:v[z] for z in ("tests","failures","errors","skipped")}
    expected={
       "author_21.junit.xml":(21,0,0,0),
       "original_strict_4_of_13.junit.xml":(13,9,0,0),
       "strict_13.junit.xml":(13,0,0,0),
       "overlay_faults.junit.xml":(9,0,0,0)}
    errors=[]
    if len(family)!=1881:errors.append("S7_GROUP_ROWS")
    if len(pe)!=8:errors.append("PE_EIGHT_ASSERTION_ROWS")
    if len(v2k)!=38:errors.append("V2K_38_FUNCTION_ROWS")
    if len(blockers)<6:errors.append("S7_BLOCKERS_TOO_FEW")
    for k,tup in expected.items():
        if tuple(junit_checks[k][x] for x in ("tests","failures","errors","skipped"))!=tup:
            errors.append("JUNIT_SUMMARY_"+k)
    ids=[x.get("blocker_id") for x in blockers]
    for k in ("S7-B04","S7-B05","S7-B06"):
        if k not in ids:errors.append("MISSING_BOUNDARY_OR_EQUIVALENCE_NEGATIVE_"+k)
    # Inspect JUnit XML itself, not only the potentially forged author's summary.
    for name,counts in expected.items():
        import xml.etree.ElementTree as ET
        x=ET.fromstring(raw(PE,pp+"repro/"+name))
        # pytest's JUnit suite is sometimes root <testsuites> with <testsuite> child.
        suite=x if x.tag=="testsuite" else x.find("testsuite")
        if suite is None:errors.append("MISSING_SUITE_"+name);continue
        for prop,val in zip(("tests","failures","errors","skipped"),counts):
            if int(suite.get(prop,"-1"))!=val:errors.append("XML_SUMMARY_MISMATCH_"+name+"_"+prop)
    state=collections.Counter(str(x.get("decision") or x.get("current_status") or "?") for x in v2k)
    out={"schema":"PYAT_S7_PE_V2K_SOURCE_RETURN_CUSTODY@1","refs":{"S7":S7,"PE":PE,"V2K":V2K},
    "S7_disposition_rows":len(family),"S7_blocker_rows":len(blockers),"S7_blocker_ids":ids,
    "S7_accounting_keys":list(account)[:32],
    "PE_eight_assertion_rows":len(pe),"PE_original_and_overlay_junit_counts":junit_checks,
    "V2K_function_rows":len(v2k),"V2K_decision_counter":dict(state),"errors":errors,
    "actual_code_or_runtime_integration_tested_by_this_audit":False,
    "sourcefree_test_receipts_are_from_returned_branch_not_independently_reexecuted":True}
    path=Path("pyat-return-s7-pe-v2k")
    path.mkdir(exist_ok=True)
    (path/"EXACT_RETURNS_AND_ORACLE_RECEIPTS.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))
    if errors:raise SystemExit(2)
if __name__=="__main__":main()
