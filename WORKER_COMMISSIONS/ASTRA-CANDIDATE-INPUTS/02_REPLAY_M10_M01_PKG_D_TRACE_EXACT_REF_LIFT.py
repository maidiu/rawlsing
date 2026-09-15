#!/usr/bin/env python3
"""Replay D07 PKG-D exact refs from manifest + externalized payloads."""
from __future__ import annotations
import copy, hashlib, json, re, sys
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{64}$")
ORDINALS = [5, 6, 7, 8, 11, 15, 16, 17, 18]
DETS = [f"GBE-R4-{n:03d}" for n in ORDINALS]
FORBIDDEN = {"LATEST","DEFAULT","FUZZY","NEAREST","SEMVER","SEMVER_FALLBACK","*"}

def canon(v):
    def nofloat(x, p="root"):
        if isinstance(x, float): raise AssertionError(f"float forbidden at {p}")
        if isinstance(x, dict):
            for k,y in x.items(): nofloat(y, f"{p}.{k}")
        elif isinstance(x, list):
            for i,y in enumerate(x): nofloat(y, f"{p}[{i}]")
    nofloat(v)
    return json.dumps(v, sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False).encode()

def digest(v): return hashlib.sha256(canon(v)).hexdigest()
def key(r): return f"{r['kind']}|{r['object_id']}|{r['content_hash']}"

def refok(r, label):
    assert set(r)=={"kind","object_id","content_hash"}, f"{label}: fields"
    assert isinstance(r["kind"],str) and r["kind"].strip()
    assert isinstance(r["object_id"],str) and r["object_id"].strip()
    assert SHA.fullmatch(r["content_hash"])
    u=r["object_id"].upper()
    assert u not in FORBIDDEN
    assert not u.startswith(("LATEST:","DEFAULT:","FUZZY:","NEAREST:","SEMVER:"))

def main():
    here=Path(__file__).resolve().parent
    m=json.loads((here/"01_M10_M01_PKG_D_TRACE_EXACT_REF_LIFT.json").read_text())
    assert m["schema"]=="PSC06_M10_M01_PKG_D_EXACT_SOURCE_CLAIM_INPUT_CEILING_REF_CONSTRUCTION_R1"
    assert m["commission"]["commission_tip"]=="d805e3dcf21a5a8cac0ee6c2611bed46da8a3277"
    assert m["commission"]["hq_base"]=="98279580ffcccdd764663107aa65835fb6929228"
    assert m["commission"]["immutable_dispatch_return"]=="a70cd2ef7d2b77c700bd8795f491079be554ae6b"
    assert m["commission"]["library_used"] is False

    bindings=[]
    seen=set()
    for i,b in enumerate(m["binding_files"]):
        ref=b["ref"]; refok(ref, f"binding[{i}]")
        payload=json.loads((here/b["payload_file"]).read_text())
        assert digest(payload)==ref["content_hash"], f"{b['payload_file']}: payload hash"
        assert key(ref) not in seen
        seen.add(key(ref))
        bindings.append({"determinant_id":b["determinant_id"],"field_path":b["field_path"],"payload":payload,"ref":ref})
    bindings.sort(key=lambda x:(x["determinant_id"],x["ref"]["kind"],x["ref"]["object_id"]))

    rows=m["s03_rows"]
    assert [r["ordinal"] for r in rows]==ORDINALS
    assert [r["determinant_id"] for r in rows]==DETS
    assert all(r["state"]=="SATISFIED_CURRENT" and r["residuals"]==[] for r in rows)
    built={key(b["ref"]) for b in bindings}
    for r in rows:
        vals=r["resolved_value"] if isinstance(r["resolved_value"],list) else [r["resolved_value"]]
        assert vals
        keys=[key(x) for x in vals]
        assert keys==sorted(keys) and len(keys)==len(set(keys))
        assert all(k in built for k in keys)
        assert [key(x) for x in r["candidate_material_refs"]]==keys

    rb={r["ordinal"]:r for r in rows}
    def payload_for(ref):
        return next(b["payload"] for b in bindings if b["ref"]==ref)

    p5=payload_for(rb[5]["resolved_value"])
    assert p5["selected_contract_id"]=="SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0"
    assert p5["selected_implementation_blob_sha1"]=="c94997f5c7f2bbee9cd99c570554fd48c0f47556"
    assert p5["selection_evidence"]["hq_runtime_adoption_commit"]=="73f33a8a4c185c46faec5ac47332153ca079ca5f"
    assert "M10-M01_RULE_CURRENTNESS" in p5["does_not_select"]

    ps=payload_for(rb[6]["resolved_value"][0])
    assert ps["project_provenance"]["m10_source_worker_commit"]=="0ebca9ff111bea63838f9b68c8e5c3cb93d9d128"
    assert ps["project_provenance"]["m10_source_ledger_blob_sha1"]=="606de007e0f6dcb28e552bd8c959f3c4ec1fd2a7"

    cps=[payload_for(x) for x in rb[7]["resolved_value"]]
    assert sorted(x["source_locus"]["supplied_lines"] for x in cps)==["857-909","951-959","978-996"]

    p8=payload_for(rb[8]["resolved_value"])
    assert p8["status"]=="DOCUMENTARY_EXTRACTION_AND_ADJUDICATION_EVIDENCE_ONLY"
    assert "NO_CAUSAL_USE_AUTHORITY_FROM_CITATION_ALONE" in p8["negative_scope"]

    p11=payload_for(rb[11]["resolved_value"])
    assert p11["required_objective_predicates"]==[
        "PRODUCTIVE_ASSET_CONTROL_INSUFFICIENT_FOR_INDEPENDENT_PRODUCTION",
        "ACTIVE_WAGE_LABOUR_SALE_RELATION",
        "EXACT_EMPLOYER_OR_COUNTERPART_IDENTITY",
        "EXACT_INSTITUTIONAL_RULE_CONTEXT",
    ]
    assert p11["position_semantic_candidate"]["content_hash"]=="60e0f41b8cd1e3b22f43dbfc2cb8bbf97c81aec7f1664486ec4adf92533af505"
    assert p11["realization_boundary"]=={
        "actual_actor_or_entity_identity_supplied":False,
        "occupancy_asserted":False,
        "actor_fact_materialization_authorized":False,
        "application_requires_separate_D13_gate":True,
    }

    p15=payload_for(rb[15]["resolved_value"])
    assert p15["current_state_holding"]=={
        "constitution_contract_current":True,
        "m10_m01_rule_current":False,
        "application_current":False,
        "actor_fact_current":False,
        "witness_current":False,
    }

    p16=payload_for(rb[16]["resolved_value"])
    assert "EXACT_INSTITUTIONAL_RULE_CONTEXT_MUST_BE_BOUND_BEFORE_REALIZATION" in p16["validity_condition"]
    assert "NO_PRESENT_DAY_PERSISTENCE_INFERENCE_FROM_DOCUMENTARY_SOURCE_ALONE" in p16["ceiling"]

    p17=payload_for(rb[17]["resolved_value"])
    for x in [
        "SOURCE_CITATION_DOES_NOT_ISSUE_CAUSAL_USE_AUTHORITY",
        "POSITION_SEMANTIC_IDENTITY_DOES_NOT_ASSERT_OCCUPANT_ACTOR_FACT_IDENTITY",
        "NO_ACTOR_OR_ENTITY_OCCUPANCY_ASSERTION",
        "NO_EXPLOITATION_FACT_FROM_POSITION_ALONE",
        "NO_RULE_CURRENT_ACCEPTED_FROM_PKG_D",
        "NO_V3_OR_PERSON_STATE",
        "NO_OBL063_DRIVER_TYPE_OR_PERSON_TERMINAL_SEMANTICS",
    ]: assert x in p17["prohibitions"]

    p18=payload_for(rb[18]["resolved_value"])
    assert p18["boundary"]=="PRE_V3_OBJECTIVE_WORLD_ONLY"
    assert p18["realization_boundary"]=={"actor_fact_materialized":False,"person_state_consumed":False}

    assert m["package_holding"]=={
        "actor_position_fact_materialized":False,
        "actor_position_fact_supplied":False,
        "application_gate":"D13",
        "join_gate":"D10_AFTER_HQ_FANIN_WITH_OTHER_PACKAGES",
        "rule_currentness_selected":False,
        "rule_envelope_complete":False,
        "runtime_projection_authorized":False,
        "trace_ref_fields_satisfied":True,
    }
    assert all(v is False for v in m["boundaries"].values())

    identity={
        "schema":m["schema"],"schema_version":m["schema_version"],"commission":m["commission"],
        "contract":m["contract"],"candidate":m["candidate"],"accepted_inputs":m["accepted_inputs"],
        "binding_objects":bindings,"s03_rows":m["s03_rows"],"package_holding":m["package_holding"],
        "preserved_laws":m["preserved_laws"],"boundaries":m["boundaries"],
    }
    h=digest(identity)
    assert h==m["identity_material_sha256"]==m["package_ref"]["content_hash"]
    refok(m["package_ref"],"package_ref")

    # order invariance
    assert digest({k:identity[k] for k in reversed(list(identity))})==h

    # one governed mutation per row family
    reps={5:rb[5]["resolved_value"],6:rb[6]["resolved_value"][0],7:rb[7]["resolved_value"][0],
          8:rb[8]["resolved_value"],11:rb[11]["resolved_value"],15:rb[15]["resolved_value"],
          16:rb[16]["resolved_value"],17:rb[17]["resolved_value"],18:rb[18]["resolved_value"]}
    n=0
    for ordinal,ref in reps.items():
        p=copy.deepcopy(payload_for(ref)); p["_replay_probe"]=f"ordinal-{ordinal}"
        assert digest(p)!=ref["content_hash"]; n+=1
    assert n==9

    print("PASS",m["terminal"],h,f"rows={len(rows)}",f"binding_objects={len(bindings)}",
          f"claim_refs={len(rb[7]['resolved_value'])}",f"change_sensitivity_mutations={n}")

if __name__=="__main__":
    try: main()
    except Exception as exc:
        print(f"FAIL {type(exc).__name__}: {exc}",file=sys.stderr)
        raise
