#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
def stable_hash(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def validate(path):
    d=json.loads(Path(path).read_text()); errs=[]; expected=d.get("authority_content_hash",""); body=dict(d); body.pop("authority_content_hash",None)
    if stable_hash(body)!=expected: errs.append("authority_content_hash_mismatch")
    den=d.get("global_recovery_denominator",{})
    if den.get("raw_source_structures")!=2499 or den.get("raw_memberships")!=15990: errs.append("global_denominator_mismatch")
    if den.get("source_family_slice_materialized") is not False: errs.append("source_family_slice_must_remain_unmaterialized")
    if d.get("full_family_completeness_claim") is not False: errs.append("forbidden_full_family_completeness_claim")
    if d.get("production_wide_execution_authorized") is not False: errs.append("forbidden_productwide_execution")
    if "NONAUTHORITATIVE" not in d.get("archive08_status",""): errs.append("archive08_must_remain_nonauthoritative")
    if d.get("registry_state")!="PARTIAL_GOVERNED_BOUNDED_CANARY__FULL_DENOMINATOR_BLOCKED": errs.append("registry_state_mismatch")
    cfgs=d.get("admitted_configurations",[])
    if len(cfgs)!=1: errs.append("exactly_one_independently_governed_canary_required")
    else:
        c=cfgs[0]
        if c.get("minimum_items_answered")!=2: errs.append("minimum_items_answered_mismatch")
        if len(c.get("members",[]))!=2: errs.append("member_count_mismatch")
        if c.get("routing_member_applicability_state")!="BOUNDED_SECTION85_CANARY_ONLY__NO_PRODUCTWIDE_ROUTING_CLAIM": errs.append("routing_ceiling_mismatch")
        if "cross-source portability" not in c.get("forbidden_inference",[]): errs.append("cross_source_ceiling_missing")
        if any(m.get("disposition")!="ADMITTED_BOUNDED_MEMBER" for m in c.get("members",[])): errs.append("member_disposition_mismatch")
    if d.get("unresolved_denominator",{}).get("state")!="STILL_UNRESOLVED__SOURCE_FAMILY_CANDIDATE_MEMBER_SLICE_NOT_MATERIALIZED": errs.append("denominator_blocker_missing")
    return errs
if __name__=="__main__":
    total=[]
    for p in sys.argv[1:]:
        e=validate(p); print(f"{p}: {'PASS' if not e else 'FAIL'}")
        for x in e: print(" ",x)
        total.extend(e)
    raise SystemExit(1 if total else 0)
