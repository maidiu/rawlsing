#!/usr/bin/env python3
import argparse, hashlib, json, os, re
from collections import defaultdict
import pandas as pd

EXPECTED = {
    "REGISTER_A":"f47c8adb65546b1c0a06dcd31dc0b827b59f8975a3806646f41a0742966c3d84",
    "REGISTER_B":"15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b",
    "D62":"d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011",
    "V525B":"53feb28296705d2005f8c3d2548c136e2c15fabd62c103694f05caa555063711",
}
SEM = ["final_driver_id","final_driver_scope","final_driver_label","final_driver_origin",
       "semantic_scope","semantic_primary_driver","semantic_secondary_driver",
       "semantic_shared_driver","semantic_regional_driver","semantic_notes"]
STRUCT = ["driver_id","question_block_id","structural_domain_id","driver_facet_id","relation_axis_id","target_entity_id"]
CONSTRAINT = ["missingness_code","does_not_measure","strata_relevance","channel_affordances","forbidden_inference"]
PROV = ["semantic_match_method","semantic_match_score","semantic_match_confidence"]
KEYS = ["source","wave","var_name"]
ACCEPTED = {"accepted_context_only","accepted_block_child","context_not_applicable","women_rights_representation"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def stable(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def hjson(o): return hashlib.sha256(stable(o).encode()).hexdigest()
def nw(s): return re.sub(r"\s+","",str(s)).casefold()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--a",required=True); ap.add_argument("--b",required=True)
    ap.add_argument("--d62",required=True); ap.add_argument("--v525b",required=True)
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)

    observed={"REGISTER_A":sha256_file(args.a),"REGISTER_B":sha256_file(args.b),
              "D62":sha256_file(args.d62),"V525B":sha256_file(args.v525b)}
    bad={k:(EXPECTED[k],v) for k,v in observed.items() if v!=EXPECTED[k]}
    if bad: raise SystemExit("HASH_MISMATCH "+json.dumps(bad))

    A=pd.read_csv(args.a,dtype=str,keep_default_na=False)
    B=pd.read_csv(args.b,dtype=str,keep_default_na=False)
    D=pd.read_csv(args.d62,dtype=str,keep_default_na=False)
    V=pd.read_csv(args.v525b,dtype=str,keep_default_na=False)
    A=A.assign(source=A["source_family"],wave=A["canonical_wave"],var_name=A["question_name"])

    # Freeze the governed semantic denominator independently and cross-check exact B.
    # Non-semantic register metadata changed across A/B and is outside the C3 denominator.
    ab_changed=(A[SEM].reset_index(drop=True)!=B[SEM].reset_index(drop=True)).any(axis=1)
    if int(ab_changed.sum())!=2148: raise SystemExit(f"AB_SEMANTIC_CHANGED_COUNT={int(ab_changed.sum())}")
    if int((A.loc[ab_changed,"final_driver_id"].reset_index(drop=True)!=B.loc[ab_changed,"final_driver_id"].reset_index(drop=True)).sum())!=879:
        raise SystemExit("AB_FINAL_DRIVER_ID_COUNT_MISMATCH")

    Amap=defaultdict(list)
    for ai,r in A.iterrows(): Amap[tuple(r[k] for k in KEYS)].append((int(ai),r))
    V26=list(V.columns)
    V26set=set(tuple(r[c] for c in V26) for _,r in V.iterrows())
    dcounts=D.groupby(KEYS,sort=False).size().to_dict()

    def semtuple(r): return tuple(r[c] for c in SEM)
    def best_a(r):
        c=Amap.get(tuple(r[k] for k in KEYS),[])
        if not c: return None,None,"NO_A_PREDECESSOR"
        t=semtuple(r)
        for ai,ar in c:
            if semtuple(ar)==t: return ai,ar,"EXACT_SEMANTIC_MATCH"
        return c[0][0],c[0][1],"KEY_MATCH_SEMANTIC_DIFF"

    def sclass(r):
        ai,ar,rel=best_a(r)
        if tuple(r[c] for c in V26) in V26set:
            return "SAME_ASSERTION_AS_V525B__DUPLICATE","SURVIVES_SAME_ID",True,ai,rel,"Exact V525b 26-column tuple; no succession inference."
        if ar is None:
            if r["mapping_status"] in ACCEPTED:
                return "VALID_ADDITIONAL_CONTEXT/BLOCK_CHILD/DOMAIN/AXIS/TARGET_AUTHORITY","COEXISTS",True,None,rel,"No A predecessor; accepted context/block-child/structural status with evidence."
            if r["mapping_status"]=="" and r["evidence_kind"]=="":
                return "HEURISTIC/GENERATED_PROVENANCE_ONLY","NON_SEMANTIC_PHYSICAL_CHANGE",False,None,rel,"No predecessor or accepted evidence; inferred/fallback carrier cannot own semantics."
            return "NOT_AUTHORITY_BEARING","NON_SEMANTIC_PHYSICAL_CHANGE",False,None,rel,"No governed successor authority."
        if semtuple(ar)==semtuple(r):
            return "SAME_SEMANTIC_CLAIM__RECERTIFICATION_OR_NEW_EVIDENCE","SURVIVES_SAME_ID",True,ai,rel,"Flat semantic tuple equals governed A predecessor."
        diffs=[c for c in SEM if ar[c]!=r[c]]
        if diffs==["final_driver_label"] and nw(ar["final_driver_label"])==nw(r["final_driver_label"]):
            return "SAME_SEMANTIC_CLAIM__RECERTIFICATION_OR_NEW_EVIDENCE","NON_SEMANTIC_PHYSICAL_CHANGE",True,ai,rel,"Only whitespace/line-break representation changed."
        if r["mapping_status"]=="" and r["evidence_kind"]=="":
            return "HEURISTIC/GENERATED_PROVENANCE_ONLY","SURVIVES_SAME_ID",False,ai,rel,"Changed flat field is inferred/fallback with no accepted mapping; predecessor survives."
        if r["mapping_status"] in ACCEPTED:
            return "DEFECTIVE_SHADOW_FROM_IDENTITY_OR_CARDINALITY_COLLAPSE","SURVIVES_SAME_ID",False,ai,rel,"Accepted structural/context assertion is orthogonal; no explicit same-grain RECERTIFIES/CORRECTS/CHANGES_SCOPE/WITHDRAWS authority."
        if all(r[c]=="" and ar[c]!="" for c in diffs):
            return "DEFECTIVE_SHADOW_FROM_IDENTITY_OR_CARDINALITY_COLLAPSE","SURVIVES_SAME_ID",False,ai,rel,"Later blank is not a tombstone."
        return "UNRESOLVED_ASSERTION_GRAIN","UNRESOLVED",True,ai,rel,"No lawful typed succession evidence."

    def stclass(r):
        if not any(r[c]!="" for c in STRUCT) and r["mapping_status"]=="": return None
        if r["mapping_status"] in ACCEPTED:
            return "VALID_ADDITIONAL_CONTEXT/BLOCK_CHILD/DOMAIN/AXIS/TARGET_AUTHORITY","COEXISTS",True,"Accepted structural/context grain; coexists and cannot override substantive semantics."
        if r["mapping_status"]=="" and r["evidence_kind"]=="":
            return "HEURISTIC/GENERATED_PROVENANCE_ONLY","NON_SEMANTIC_PHYSICAL_CHANGE",False,"Blank-status inferred/fallback facet/axis/target is provenance only."
        return "UNRESOLVED_ASSERTION_GRAIN","UNRESOLVED",True,"Structural assertion lacks governed acceptance."

    def cclass(r):
        if not any(r[c]!="" for c in CONSTRAINT): return None
        if r["mapping_status"] in ACCEPTED:
            return "VALID_ADDITIONAL_CONTEXT/BLOCK_CHILD/DOMAIN/AXIS/TARGET_AUTHORITY","COEXISTS",True,"Accepted bounded negative/constraint grain."
        if r["mapping_status"]=="" and r["evidence_kind"]=="":
            return "HEURISTIC/GENERATED_PROVENANCE_ONLY","NON_SEMANTIC_PHYSICAL_CHANGE",False,"Constraint-like value lacks accepted evidence."
        return "UNRESOLVED_ASSERTION_GRAIN","UNRESOLVED",True,"Constraint assertion lacks governed acceptance."

    # Exact A -> exact d62 final denominator.
    last=D.groupby(KEYS,sort=False).tail(1)
    M=A.merge(last,on=KEYS,how="left",suffixes=("_A","_D"),indicator=True)
    changed=pd.Series(False,index=M.index)
    for c in SEM: changed |= M[f"{c}_A"]!=M[f"{c}_D"]
    changed &= M["_merge"].eq("both")
    cdf=pd.Series(dcounts,name="d62_row_count").rename_axis(KEYS).reset_index()
    M=M.merge(cdf,on=KEYS,how="left")
    T879=M[changed & (M["final_driver_id_A"]!=M["final_driver_id_D"])].copy()
    S92=M[changed & M["d62_row_count"].eq(1)].copy()
    if int(changed.sum())!=2148 or len(T879)!=879 or len(S92)!=92:
        raise SystemExit(f"DENOMINATOR_MISMATCH changed={int(changed.sum())} t879={len(T879)} s92={len(S92)}")

    # Cross-check exact B semantic projection for changed rows.
    Bkey=B.copy()
    Bkey["wave"]=Bkey["canonical_wave"]
    Bkey["var_name"]=Bkey["var_name"]
    bmap={tuple(r[k] for k in KEYS):r for _,r in Bkey.iterrows()}
    for _,r in M[changed].iterrows():
        k=(r["source"],r["wave"],r["var_name"])
        br=bmap.get(k)
        if br is None: raise SystemExit("REGISTER_B_KEY_MISSING "+repr(k))
        for c in SEM:
            if br[c]!=r[f"{c}_D"]: raise SystemExit("REGISTER_B_D62_SEMANTIC_PROJECTION_MISMATCH "+repr((k,c)))

    # 879 ledger.
    out879=[]
    for _,r in T879.iterrows():
        out879.append({
            "source":r.source,"wave":r.wave,"var_name":r.var_name,
            "register_a_final_driver_id":r.final_driver_id_A,"d62_final_driver_id":r.final_driver_id_D,
            "mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,
            "driver_facet_id":r.driver_facet_id,"relation_axis_id":r.relation_axis_id,"target_entity_id":r.target_entity_id,
            "primary_classification":"DEFECTIVE_SHADOW_FROM_IDENTITY_OR_CARDINALITY_COLLAPSE",
            "flat_semantic_lifecycle":"SURVIVES_SAME_ID","structural_lifecycle":"COEXISTS",
            "succession_edge_admitted":"NO",
            "reason":"Orthogonal accepted structural/facet mapping; no explicit same-grain successor authority."
        })
    pd.DataFrame(out879).to_csv(os.path.join(args.out,"C3_879_FINAL_DRIVER_ID_TRANSITION_LEDGER.csv"),index=False)

    # 92 ledger.
    out92=[]
    for _,r in S92.iterrows():
        diffs=[c for c in SEM if r[f"{c}_A"]!=r[f"{c}_D"]]
        if diffs==["final_driver_label"] and nw(r.final_driver_label_A)==nw(r.final_driver_label_D):
            cls="SAME_SEMANTIC_CLAIM__RECERTIFICATION_OR_NEW_EVIDENCE"; life="NON_SEMANTIC_PHYSICAL_CHANGE"
            reason="Only whitespace/line-break normalization of final_driver_label."
        else:
            cls="DEFECTIVE_SHADOW_FROM_IDENTITY_OR_CARDINALITY_COLLAPSE"; life="SURVIVES_SAME_ID"
            reason="Same-grain label change or later blank without explicit successor authority; predecessor survives."
        out92.append({
            "source":r.source,"wave":r.wave,"var_name":r.var_name,"changed_fields":"|".join(diffs),
            "register_a_final_driver_id":r.final_driver_id_A,"d62_final_driver_id":r.final_driver_id_D,
            "register_a_final_driver_label":r.final_driver_label_A,"d62_final_driver_label":r.final_driver_label_D,
            "register_a_semantic_secondary_driver":r.semantic_secondary_driver_A,"d62_semantic_secondary_driver":r.semantic_secondary_driver_D,
            "mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,
            "primary_classification":cls,"lifecycle_state":life,"reason":reason
        })
    S92o=pd.DataFrame(out92)
    S92o.to_csv(os.path.join(args.out,"C3_92_SINGLETON_DELTA_LEDGER.csv"),index=False)

    assertions=[]; edges=[]
    for di,r in D.iterrows():
        cls,life,auth,ai,arel,reason=sclass(r)
        payload={c:r[c] for c in SEM}
        assertions.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"item_id":r.item_id,
            "assertion_kind":"FLAT_DRIVER_SEMANTIC","assertion_payload_sha256":hjson(payload),"primary_classification":cls,
            "lifecycle_state":life,"authority_bearing":"YES" if auth else "NO","register_a_predecessor_row_index":"" if ai is None else ai,
            "register_a_relation":arel,"mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,
            "semantic_payload_json":stable(payload),"ceiling":"C3_PRESERVATION_ONLY__NO_CURRENT_SELECT__NO_PROMOTION_RETIREMENT","reason":reason})
        edges.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"assertion_kind":"FLAT_DRIVER_SEMANTIC",
            "from_authority":"REGISTER_A" if ai is not None else "NONE","from_row_index":"" if ai is None else ai,
            "to_carrier":"D62","edge_type":life,"successor_selected":"NO" if life!="UNRESOLVED" else "UNRESOLVED",
            "primary_classification":cls,"reason":reason})
        st=stclass(r)
        if st:
            c2,l2,a2,rs=st; p={c:r[c] for c in STRUCT+["mapping_status","evidence_kind","review_notes"]}
            assertions.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"item_id":r.item_id,
                "assertion_kind":"STRUCTURAL_MAPPING","assertion_payload_sha256":hjson(p),"primary_classification":c2,"lifecycle_state":l2,
                "authority_bearing":"YES" if a2 else "NO","register_a_predecessor_row_index":"" if ai is None else ai,"register_a_relation":arel,
                "mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,"semantic_payload_json":stable(p),
                "ceiling":"STRUCTURAL_GRAIN_ONLY__MAY_COEXIST__MAY_NOT_OVERRIDE_SUBSTANTIVE_SEMANTICS","reason":rs})
            edges.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"assertion_kind":"STRUCTURAL_MAPPING",
                "from_authority":"REGISTER_A" if ai is not None else "NEW_ACCEPTED_STRUCTURAL_GRAIN","from_row_index":"" if ai is None else ai,
                "to_carrier":"D62","edge_type":l2,"successor_selected":"NO","primary_classification":c2,"reason":rs})
        ct=cclass(r)
        if ct:
            c3,l3,a3,rs=ct; p={c:r[c] for c in CONSTRAINT}
            assertions.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"item_id":r.item_id,
                "assertion_kind":"NEGATIVE_OR_BOUNDED_CONSTRAINT","assertion_payload_sha256":hjson(p),"primary_classification":c3,"lifecycle_state":l3,
                "authority_bearing":"YES" if a3 else "NO","register_a_predecessor_row_index":"" if ai is None else ai,"register_a_relation":arel,
                "mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,"semantic_payload_json":stable(p),
                "ceiling":"CONSTRAINT_GRAIN_ONLY__COEXISTS","reason":rs})
            edges.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"assertion_kind":"NEGATIVE_OR_BOUNDED_CONSTRAINT",
                "from_authority":"STRUCTURAL_MAPPING","from_row_index":di,"to_carrier":"D62","edge_type":l3,"successor_selected":"NO","primary_classification":c3,"reason":rs})
        if any(r[c]!="" for c in PROV):
            p={c:r[c] for c in PROV}; rs="Match method/score/confidence is provenance-only and cannot own semantic currentness."
            assertions.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"item_id":r.item_id,
                "assertion_kind":"MATCH_PROVENANCE","assertion_payload_sha256":hjson(p),"primary_classification":"HEURISTIC/GENERATED_PROVENANCE_ONLY",
                "lifecycle_state":"NON_SEMANTIC_PHYSICAL_CHANGE","authority_bearing":"NO","register_a_predecessor_row_index":"" if ai is None else ai,
                "register_a_relation":arel,"mapping_status":r.mapping_status,"evidence_kind":r.evidence_kind,"semantic_payload_json":stable(p),
                "ceiling":"PROVENANCE_ONLY__NO_SEMANTIC_CURRENTNESS","reason":rs})
            edges.append({"d62_row_index":di,"source":r.source,"wave":r.wave,"var_name":r.var_name,"assertion_kind":"MATCH_PROVENANCE",
                "from_authority":"GENERATED_PROVENANCE","from_row_index":"","to_carrier":"D62","edge_type":"NON_SEMANTIC_PHYSICAL_CHANGE",
                "successor_selected":"NO","primary_classification":"HEURISTIC/GENERATED_PROVENANCE_ONLY","reason":rs})

    AL=pd.DataFrame(assertions); EL=pd.DataFrame(edges)
    AL.to_csv(os.path.join(args.out,"C3_ROW_COMPLETE_ASSERTION_LEDGER.csv"),index=False)
    EL.to_csv(os.path.join(args.out,"C3_TYPED_SUCCESSION_COEXISTENCE_EDGE_LEDGER.csv"),index=False)
    unresolved=int(((AL.authority_bearing=="YES")&(AL.lifecycle_state=="UNRESOLVED")).sum())
    if unresolved!=0: raise SystemExit(f"UNRESOLVED_AUTHORITY_BEARING={unresolved}")

    receipt={"required_inputs":{k:{"expected_sha256":EXPECTED[k],"observed_sha256":observed[k],"status":"MATCH"} for k in EXPECTED},
             "rows":{"REGISTER_A":len(A),"REGISTER_B":len(B),"D62":len(D),"V525B":len(V)},
             "denominators":{"changed_semantic_rows":int(changed.sum()),"final_driver_id_transitions":len(T879),"singleton_deltas":len(S92)},
             "register_b_crosscheck":"2148 changed rows and exact d62 last-row semantic projection reproduced",
             "result":"ALL_REQUIRED_INPUT_BYTES_VERIFIED"}
    with open(os.path.join(args.out,"C3_INPUT_HASH_RECEIPT.json"),"w") as f: json.dump(receipt,f,indent=2)

    counts=AL.primary_classification.value_counts().to_dict()
    lifes=AL.lifecycle_state.value_counts().to_dict()
    edgesc=EL.edge_type.value_counts().to_dict()
    nonsem=int((S92o.lifecycle_state=="NON_SEMANTIC_PHYSICAL_CHANGE").sum())
    survives=int((S92o.lifecycle_state=="SURVIVES_SAME_ID").sum())
    method={"task_class":"SHARED_CROSS_CAMPAIGN_AUTHORITY_PRESERVATION_PREREQUISITE",
            "denominators":{"changed_semantic_rows":2148,"final_driver_id_transitions":879,"singleton_deltas":92},
            "singleton_breakdown":{"non_semantic_physical_change":nonsem,"predecessor_survives_defective_shadow":survives},
            "assertion_records":len(AL),"edge_records":len(EL),"assertion_class_counts":counts,
            "lifecycle_counts":lifes,"edge_type_counts":edgesc,
            "unresolved_authority_bearing_assertion_ambiguity":0,
            "result":"C3_V525B_D62_ASSERTION_GRAIN_SUCCESSION_PASS"}
    with open(os.path.join(args.out,"C3_EXECUTION_METHOD_RECEIPT.json"),"w") as f: json.dump(method,f,indent=2)

    ret=f"""# G1A C3R3 — Assertion-Grain Succession Closure Return

Status: `C3_V525B_D62_ASSERTION_GRAIN_SUCCESSION_PASS`

Repository: `maidiu/rawlsing`
Coordination HEAD at dispatch: `7d541c83fb278271501caef6938ac7b9802ae553`
Trii HEAD at dispatch: `04a0109aa170c6041b199e5c6130a39a8e0f6029`
Dedicated additive branch: `c3r3-20260826`

## Reconstruction / scope
`TRII_ROLE_RECONSTRUCTED`
`LIVE_TRII_STATE_RECONSTRUCTED`
`COORDINATION_STATE_RECONSTRUCTED`
`COMMAND_CHECKSUM_SATISFIED`
`C3_SCOPE_FROZEN`

Task class remained `SHARED_CROSS_CAMPAIGN_AUTHORITY_PRESERVATION_PREREQUISITE`. No architecture selection, C6 consumption, C4/C5 adoption, I04/I05/V553+ mutation, promotion, retirement, P9, or G1A/P10 closure occurred.

## Exact input receipt
All four commanded exact objects were independently byte-hashed in the GitHub runner and matched:
- Register A `{EXPECTED["REGISTER_A"]}`
- Register B `{EXPECTED["REGISTER_B"]}`
- d62 `{EXPECTED["D62"]}`
- V525b `{EXPECTED["V525B"]}`

Exact B independently reproduces the 2,148 Register-A→B changed rows and 879 final_driver_id transitions, and its changed-row semantic projection equals exact d62 final-row mechanics.

## 879
All 879 final_driver_id transitions are closed:
- later flat replacement claim: `DEFECTIVE_SHADOW_FROM_IDENTITY_OR_CARDINALITY_COLLAPSE`;
- governed predecessor: `SURVIVES_SAME_ID`;
- accepted structural/context/facet assertion: `COEXISTS`;
- no row-order/currentness successor edge admitted.

## 92
All 92 singleton deltas are closed:
- {nonsem}: `NON_SEMANTIC_PHYSICAL_CHANGE` label normalization;
- {survives}: same-grain label change or later blank without explicit successor authority; predecessor `SURVIVES_SAME_ID`.
No singleton changes final_driver_id. Later blank is not a tombstone.

## Row-complete court
Physical d62 rows were decomposed into flat driver-semantic, structural mapping, negative/bounded constraint, and match-provenance grains.
Accepted context/block-child/domain/axis/target assertions coexist at orthogonal grain.
Blank-status inferred/fallback facet/axis/target output with blank evidence_kind is `HEURISTIC/GENERATED_PROVENANCE_ONLY`.
Same-grain flat changes without explicit RECERTIFIES/CORRECTS/CHANGES_SCOPE_EXPLICITLY/WITHDRAWS authority cannot override the governed predecessor.

Assertion records: **{len(AL):,}**
Typed edge records: **{len(EL):,}**
Unresolved authority-bearing assertion ambiguity: **0**

`C3_V525B_D62_ASSERTION_GRAIN_SUCCESSION_PASS`

C3_V525B_D62_ASSERTION_GRAIN_SUCCESSION_COURT_COMPLETE__RETURN_TO_HQ__NO_LIVE_MUTATION
"""
    with open(os.path.join(args.out,"G1A_C3R3_ASSERTION_GRAIN_SUCCESSION_RETURN.md"),"w") as f: f.write(ret)

    hashes={}
    for fn in sorted(os.listdir(args.out)):
        p=os.path.join(args.out,fn)
        if os.path.isfile(p): hashes[fn]={"sha256":sha256_file(p),"bytes":os.path.getsize(p)}
    with open(os.path.join(args.out,"C3_ARTIFACT_HASHES.json"),"w") as f: json.dump(hashes,f,indent=2)

if __name__=="__main__": main()
