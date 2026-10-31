#!/usr/bin/env python3
"""HQ read-only original-vs-corrected source identity check.
Reads pinned Git objects as DATA. Does not import or execute worker source.
PASS is documentary custody only, not current ABI/science/actor adoption.
"""
import collections,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
S6="2c5cf86beb12b7dbeda5532614784737ad30d89d"
FIX="80bc5d9bf6624c2ea04027322947a41c347330aa"
S6P="PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S6/"
FIXP="PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR/"
SPLITS={"FAM_b8e8a1c5bac3370d","FAM_1427a684892de839","FAM_214c6eaf1fe2a42d","FAM_6813a575a7ce67c0","FAM_c0d48f7daa8cc28d"}
JOIN={"FAM_bd6118ca46930519","S6FAM-23dd9c27fe2a7c60"}
def object_bytes(sha,path):
    p=subprocess.run(["git","show",sha+":"+path],cwd=ROOT,capture_output=True)
    if p.returncode:raise RuntimeError("UNAVAILABLE_PINNED_GIT_BLOB "+sha+" "+path+" "+p.stderr.decode(errors="replace")[-200:])
    return p.stdout
def jsonl(sha,path):
    return [json.loads(line) for line in object_bytes(sha,path).splitlines() if line.strip()]
def main():
    original=jsonl(S6,S6P+"CROSS_SHARD_FUNCTION_GROUPS.jsonl")
    old={g["group_id"]:g for g in original}
    source_ids=collections.Counter(str(v) for g in original for v in g.get("member_function_ids",[]))
    mapped=jsonl(FIX,FIXP+"FUNCTION_ID_TO_CORRECTED_FAMILY.jsonl")
    oldmap=jsonl(FIX,FIXP+"OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl")
    huge=object_bytes(FIX,FIXP+"CORRECTED_RECEIVER_AND_INTEGRATABILITY.json")
    doc=json.loads(huge)
    families=doc["corrected_families"]
    newids=collections.Counter(str(v) for f in families for v in f.get("member_function_ids",[]))
    family_for={str(v):f["family_id"] for f in families for v in f.get("member_function_ids",[])}
    byold=collections.defaultdict(list)
    for f in families:
        for legacy in f.get("legacy_group_ids",[]):byold[legacy].append(f)
    errors=[]
    if len(original)!=1881 or len(families)!=1885:errors.append("BAD_FAMILY_COUNT")
    if len(source_ids)!=3135 or len(newids)!=3135 or sum(newids.values())!=3135:errors.append("BAD_MEMBER_CENSUS")
    if source_ids!=newids:errors.append("SOURCE_IDS_LOST_CHANGED_DUPLICATED")
    if len(mapped)!=3135 or len(oldmap)!=1881:errors.append("BAD_CROSSWALK_RECORD_COUNT")
    if set(byold)!=set(old):errors.append("OLD_GROUP_SET_CHANGED")
    boundary={}
    for gid in SPLITS:
        new=byold.get(gid,[])
        boundary[gid]={"new":len(new),"new_ids":[f.get("family_id") for f in new],
                       "qualnames":[sorted(set(m.get("identity",{}).get("actual_qualname","") for m in f.get("members",[]))) for f in new]}
        if len(new)!=2:errors.append("SPLIT_NOT_TWO_"+gid)
        oldmembers=collections.Counter(old[gid]["member_function_ids"])
        corrected=collections.Counter(str(v) for f in new for v in f.get("member_function_ids",[]))
        if oldmembers!=corrected:errors.append("SPLIT_ID_MEMBERS_CHANGE_"+gid)
        quals=[set(q for q in r) for r in boundary[gid]["qualnames"]]
        if len(quals)==2 and (any(len(q)!=1 for q in quals) or not any(any("._make_sealed_source_relation_owner" in t or t.startswith("_make_sealed_source_relation_owner.") for t in q) for q in quals)):
            errors.append("SPLIT_NESTING_UNPROVEN_"+gid)
    joined=[f for f in families if JOIN.issubset(set(f.get("legacy_group_ids",[])))]
    if len(joined)!=1:errors.append("JOIN_NOT_UNIQUE")
    else:
        jj=joined[0]
        expected=collections.Counter(str(v) for gid in JOIN for v in old[gid].get("member_function_ids",[]))
        if collections.Counter(str(v) for v in jj.get("member_function_ids",[]))!=expected:errors.append("JOIN_SOURCE_MEMBERS_CHANGE")
        if any(m.get("identity",{}).get("actual_qualname")!="PhysicalSourceIncidence.iter_batches.emit" for m in jj.get("members",[])):
            errors.append("JOIN_WRONG_QUALNAME")
    modified=SPLITS|JOIN
    for gid in set(old)-modified:
        new=byold.get(gid,[])
        if len(new)!=1:errors.append("UNTOUCHED_GROUP_REASSIGNED_"+gid);continue
        if collections.Counter(old[gid]["member_function_ids"])!=collections.Counter(new[0].get("member_function_ids",[])):
            errors.append("UNTOUCHED_GROUP_MEMBERS_CHANGED_"+gid)
    for f in families:
        if f.get("correction",{}).get("behavioral_equivalence")!="NOT_CLAIMED" or f.get("correction",{}).get("science_acceptance")!="NOT_CLAIMED":
            errors.append("INVENTED_BEHAVIOR_SCIENCE_"+f["family_id"])
        if len(f.get("member_function_ids",[]))!=f.get("member_count"):errors.append("MEMBER_COUNT_WRONG_"+f["family_id"])
    new_fam_set={f["family_id"] for f in families}
    if len(new_fam_set)!=len(families):errors.append("DUPLICATE_CORRECTED_FAMILY_IDS")
    for row in mapped:
        fid=row.get("function_id")
        if fid not in source_ids:errors.append("MAPPING_UNKNOWN_ID")
        claimed=row.get("corrected_family_id")
        if claimed and claimed!=family_for.get(fid):errors.append("MAPPING_FAMILY_DIFFERS_"+str(fid))
    receipt={
      "schema":"PYAT_S7FIX_INDEPENDENT_SOURCE_CHECK@1",
      "source_refs":{"S6":S6,"S7FIX":FIX},
      "original_groups":len(original),"corrected_groups":len(families),
      "original_member_count":sum(source_ids.values()),"corrected_member_count":sum(newids.values()),
      "unique_original_ids":len(source_ids),"unique_corrected_ids":len(newids),
      "mapped_function_rows":len(mapped),"old_group_map_rows":len(oldmap),
      "five_splits":boundary,"join_family":joined[0]["family_id"] if len(joined)==1 else None,
      "source_47mb_blob_sha256":hashlib.sha256(huge).hexdigest(),
      "source_json_bytes":len(huge),"errors":errors[:35],
      "status":"PASS_SOURCE_IDENTITY_ONLY" if not errors else "FAIL_UNVERIFIED_SOURCE_IDENTITY",
      "never_executed_worker_code":True,"current_abi_or_science_adoption":False
    }
    out=Path("pyat-hq-s7fix-receipts");out.mkdir(exist_ok=True)
    (out/"INDEPENDENT_S7FIX_SOURCE_CUSTODY.json").write_text(json.dumps(receipt,indent=2),encoding="utf-8")
    print(json.dumps({k:v for k,v in receipt.items() if k!="five_splits"},indent=2))
    if errors:raise SystemExit(2)
if __name__=="__main__":main()
