from __future__ import annotations
import hashlib, json
from typing import Any, Mapping

HARNESS_SCHEMA="RAWLSING_EE_W4_ABC_MEASUREMENT_HARNESS@1.0.0"
WORKLOAD_SCHEMA="RAWLSING_EE_W4_FROZEN_WORKLOAD_EXECUTION_PROFILE@1.0.0"
CANDIDATE_IDS=("A","B","C")
EE_REQUIREMENTS=tuple(f"EE{i:02d}" for i in range(1,17))
ELIGIBLE="ELIGIBLE"
INELIGIBLE_STATES={"MISSING_AUTHORITY","INELIGIBLE","NONCOMPARABLE","OUTSIDE_REQUESTED_JURISDICTION","SOURCE_CELL_UNAVAILABLE","UNRESOLVED_AUTHORITY"}
PHASES={"cold","warm_1","warm_2","warm_5","hostile","delete_rebuild","selective_source_invalidation","selective_authority_invalidation","replay","audit","other"}
HARNESS_ACTIONS={"DELETE_DURABLE","DELETE_SCRATCH","RESET_CANDIDATE_STATE"}
CANDIDATE_ACTIONS={"EXECUTE","REBUILD","REPLAY","INVALIDATE_SOURCE","INVALIDATE_AUTHORITY","AUDIT"}
HOSTILE_CASE_IDS={
"H01_RECURSIVE_SUBGROUP_FORK","H02_MINORITY_SUPPORTED_STRUCTURE","H03_EQUAL_MARGINALS_DIFFERENT_KWAY_JOINT","H04_XOR_ZERO_LOWER_ORDER_SIGNAL","H05_DENOMINATOR_CONFLICT","H06_SOURCE_ZERO_VS_SEMANTIC_ZERO","H07_NULL_VS_OBSERVED_ZERO","H08_CERTIFIED_VS_REVIEW_LANE","H09_LAWFUL_PARALLEL_TARGET_LAYERS","H10_INCOMPLETE_COMPONENT_VECTOR","H11_HETEROGENEOUS_COMPONENT_VECTOR_NOT_SCALARIZABLE","H12_ROUTING_SIGNAL_WITHOUT_LAWFUL_EXECUTABLE_PREDICATE","H13_SYNTHETIC_JOINT_FAMILY_CONTAMINATION","H14_RANKED_MULTISELECT_TOPOLOGY","H15_CROSS_SOURCE_SEMANTIC_CONTRACT_INCOMPATIBILITY","H16_EQUAL_VALUE_DISTINCT_SOURCE_SLOTS","H17_MISSING_SEMANTIC_ROUTING_AUTHORITY","H18_EXPLICIT_NONCOMPARABILITY","H19_DELETE_REBUILD_REPLAY_IDENTITY","H20_SELECTIVE_INVALIDATION_EXACT_DETERMINANT_CHANGE"}
class HarnessContractError(ValueError): pass

def canonical_json_bytes(v:Any)->bytes:
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":"))+"\n").encode()
def sha256_bytes(v:bytes)->str: return hashlib.sha256(v).hexdigest()
def hex64(v:Any)->bool: return isinstance(v,str) and len(v)==64 and all(c in "0123456789abcdef" for c in v)
def safe_component(v:str,label:str)->str:
    if not v or v in {".",".."} or "/" in v or "\\" in v or "\x00" in v: raise HarnessContractError(f"unsafe {label}: {v!r}")
    return v

def validate_workload_manifest(m:Mapping[str,Any])->dict[str,Any]:
    if m.get("schema")!=WORKLOAD_SCHEMA: raise HarnessContractError(f"unexpected workload schema: {m.get('schema')!r}")
    wid=m.get("workload_id"); steps=m.get("steps")
    if not isinstance(wid,str) or not wid: raise HarnessContractError("workload_id must be nonempty")
    if not isinstance(steps,list) or not steps: raise HarnessContractError("steps must be a nonempty fully-unrolled list")
    seen=set(); out=[]
    for i,raw in enumerate(steps):
        if not isinstance(raw,dict): raise HarnessContractError(f"step {i} is not an object")
        s=dict(raw); sid=s.get("step_id")
        if not isinstance(sid,str) or not sid or sid in seen: raise HarnessContractError(f"invalid/duplicate step_id {sid!r}")
        seen.add(sid); safe_component(sid,"step_id")
        if not isinstance(s.get("universe_id"),str) or not s["universe_id"]: raise HarnessContractError(f"{sid}: universe_id required")
        if not isinstance(s.get("operation_id"),str) or not s["operation_id"]: raise HarnessContractError(f"{sid}: operation_id required")
        req=s.get("ee_requirement_ids")
        if not isinstance(req,list) or not req or any(x not in EE_REQUIREMENTS for x in req): raise HarnessContractError(f"{sid}: invalid EE requirements")
        if s.get("phase") not in PHASES: raise HarnessContractError(f"{sid}: unsupported phase")
        if s.get("action") not in HARNESS_ACTIONS|CANDIDATE_ACTIONS: raise HarnessContractError(f"{sid}: unsupported action")
        e=s.get("eligibility")
        if not isinstance(e,dict): raise HarnessContractError(f"{sid}: eligibility required")
        state=e.get("state")
        if state!=ELIGIBLE and state not in INELIGIBLE_STATES: raise HarnessContractError(f"{sid}: invalid eligibility")
        if not isinstance(e.get("exact_basis"),str) or not e["exact_basis"]: raise HarnessContractError(f"{sid}: exact_basis required")
        h=s.get("hostile_case_id")
        if h is not None and h not in HOSTILE_CASE_IDS: raise HarnessContractError(f"{sid}: unknown hostile case")
        if state==ELIGIBLE and s["action"] in CANDIDATE_ACTIONS:
            if "request" not in s or not isinstance(s.get("oracle"),dict): raise HarnessContractError(f"{sid}: request/oracle required")
            if not hex64(s["oracle"].get("semantic_output_sha256")): raise HarnessContractError(f"{sid}: semantic SHA required")
        out.append(s)
    payload={"schema":m["schema"],"workload_id":wid,"steps":out}
    return {"workload_id":wid,"steps":out,"plan_sha256":sha256_bytes(canonical_json_bytes(payload)),"manifest_sha256":sha256_bytes(canonical_json_bytes(dict(m)))}

def validate_candidate_config(c:Mapping[str,Any])->dict[str,list[str]]:
    if set(c)!=set(CANDIDATE_IDS): raise HarnessContractError("candidate config must contain exactly A/B/C")
    out={}
    for k in CANDIDATE_IDS:
        row=c[k]
        if not isinstance(row,dict) or not isinstance(row.get("argv"),list) or not row["argv"] or not all(isinstance(x,str) and x for x in row["argv"]): raise HarnessContractError(f"candidate {k}: argv list required")
        out[k]=list(row["argv"])
    return out
