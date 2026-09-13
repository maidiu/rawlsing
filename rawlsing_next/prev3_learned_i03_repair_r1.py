"""I02 canonical-I03 repair/re-execution for the frozen D02/F02 learned workload."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
from typing import Any

SOURCE_SHA256="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS=29002
SOURCE_VARIABLES=1198
D02_AUTHORITY_COMMIT="40cb8585f076a66d9884b99022a59bb909606c03"
D02_FRONTIER_GIT_BLOB="5399a3f64642c8d9f8a0644db0adc15d38642971"
F02_RETURN_COMMIT="482bb884a99e31ba77e904d0df39fffc872cbed3"
F02_RELEASE_HASH="bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
F02_FRONTIER_READOPTION_HASH="07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851"
G02_PREEXECUTION_SEAL="ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea"
CANONICAL_I03_BLOB="e2d91984541df7c692a1b2f32370500838a2a000"
AS2B_ACCEPTED_COMMIT="923f2c00b6145182a5e2be5038f579845951da19"
NEGATIVE_CEILING="PREV3_LEARNED_EMPIRICAL_ONLY__NO_STRUCTURAL_ADMISSION__NO_CAUSAL_PROMOTION__NO_POPULATION_GENERALIZATION__NO_PERSON_STATE__NO_V3"
EXPECTED_F02={
"q310":{"counts":{"1":12340,"2":7511,"3":9085,"MISSING":66},"row_root":"a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455","selector_roots":{"1":"0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2","2":"0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83","3":"b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d","MISSING":"810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348"}},
"q311":{"counts":{"1":16582,"2":4548,"3":7826,"MISSING":46},"row_root":"af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa","selector_roots":{"1":"bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869","2":"43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f","3":"642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837","MISSING":"847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb"}}}

def canon(x:Any):
    if x is None or isinstance(x,(str,int,bool)): return x
    if isinstance(x,float):
        if not math.isfinite(x): raise ValueError("nonfinite")
        if x.is_integer(): return int(x)
        raise ValueError("nonintegral float")
    if hasattr(x,"item"): return canon(x.item())
    if isinstance(x,dict): return {str(k):canon(x[k]) for k in sorted(x,key=str)}
    if isinstance(x,(list,tuple)): return [canon(v) for v in x]
    raise TypeError(type(x).__name__)
def cjson(x): return json.dumps(canon(x),sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def sh(x): return hashlib.sha256(cjson(x).encode()).hexdigest()
def file_sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def native(v):
    if v is None: return None
    try:
        if math.isnan(v): return None
    except (TypeError,ValueError): pass
    if hasattr(v,"item"): v=v.item()
    if isinstance(v,float):
        if not v.is_integer(): raise ValueError(v)
        return int(v)
    return int(v)
def q301_state(v):
    v=native(v)
    if v is None: return ("SYSTEM_MISSING",None)
    if v in (1,2,3,4,5): return ("SUBSTANTIVE_RESPONSE",v)
    if v in (6,7): return ("SOURCE_SPECIFIC_SPECIAL",v)
    raise ValueError(f"q301 out of authority {v}")
def matches(row,atom):
    if atom=="A000": return True
    if atom=="A1V1": return native(row["q301_2"])==1
    if atom=="A1V5": return native(row["q301_2"])==5
    if atom.startswith("Q310V"): return native(row["q310"])==int(atom[-1])
    if atom.startswith("Q311V"): return native(row["q311"])==int(atom[-1])
    raise ValueError(atom)
def scan_selectors(records):
    out={}
    for q in ("q310","q311"):
        total=hashlib.sha256(); hs={k:hashlib.sha256() for k in ("1","2","3","MISSING")}; counts={k:0 for k in hs}
        for i,r in enumerate(records):
            v=native(r[q]); state="MISSING" if v is None else "SUBSTANTIVE_RESPONSE"; key="MISSING" if v is None else str(v)
            if key not in hs: raise ValueError(f"{q} out of domain {v}")
            b=(cjson({"row_ordinal":i,"response_state":state,"raw_native_value":v})+"\n").encode()
            total.update(b); hs[key].update(b); counts[key]+=1
        out[q]={"counts":counts,"row_root":total.hexdigest(),"selector_roots":{k:hs[k].hexdigest() for k in hs}}
    return out
def query(records,target,atoms):
    selected=[r for r in records if all(matches(r,a) for a in atoms)]
    den=len(selected); cells={}; unresolved={}
    if target in ("q301_2","q301_7"):
        cells={str(i):0 for i in range(1,6)}
        for r in selected:
            s,v=q301_state(r[target])
            if s=="SUBSTANTIVE_RESPONSE": cells[str(v)]+=1
            else:
                k=s if v is None else f"{s}:{v}"; unresolved[k]=unresolved.get(k,0)+1
    elif target=="joint":
        cells={f"{a},{b}":0 for a in range(1,6) for b in range(1,6)}
        for r in selected:
            s2,v2=q301_state(r["q301_2"]); s7,v7=q301_state(r["q301_7"])
            if s2=="SUBSTANTIVE_RESPONSE" and s7=="SUBSTANTIVE_RESPONSE": cells[f"{v2},{v7}"]+=1
            else:
                k=f"q301_2={s2}:{v2}|q301_7={s7}:{v7}"; unresolved[k]=unresolved.get(k,0)+1
    else: raise ValueError(target)
    resolved=sum(cells.values()); state="ZERO_SUPPORT" if den==0 else ("UNRESOLVED" if resolved!=den else "SUPPORTED")
    assert sum(unresolved.values())==den-resolved
    return {"state":state,"denominator":den,"resolved":resolved,"unresolved":den-resolved,"cells":cells,"unresolved_states":dict(sorted(unresolved.items()))}
def frontier():
    cs=[]
    for cell in range(1,6): cs.append({"lane":"P0","id":f"P0:{cell}","roles":[("BASE","q301_2",["A000"])]})
    cs.append({"lane":"P1","id":"P1","roles":[("JOINT","joint",["A000"]),("MARGINAL_0","q301_2",["A000"]),("MARGINAL_1","q301_7",["A000"])]})
    for q2 in (1,5):
        for q310 in (1,2,3):
            for q311 in (1,2,3):
                cs.append({"lane":"P2","id":f"P2:{q2}:{q310}:{q311}","roles":[("CONDITION","q301_7",[f"A1V{q2}",f"Q310V{q310}",f"Q311V{q311}"]),("BASELINE","q301_7",["A000"])]})
    roles=[("POOLED_POS","q301_7",["A1V5"]),("POOLED_NEG","q301_7",["A1V1"])]
    for q310 in (1,2,3): roles += [(f"STRATUM:{q310}:POS","q301_7",[f"Q310V{q310}","A1V5"]),(f"STRATUM:{q310}:NEG","q301_7",[f"Q310V{q310}","A1V1"])]
    cs.append({"lane":"P3","id":"P3","roles":roles})
    for a in range(1,6):
        for b in range(1,6): cs.append({"lane":"P4","id":f"P4:{a}:{b}","roles":[("BASE","joint",["A000"])]})
    assert len(cs)==50 and sum(len(c["roles"]) for c in cs)==77
    return cs
def execute(path):
    if file_sha(path)!=SOURCE_SHA256: raise ValueError("source sha")
    import pandas as pd
    frame=pd.read_stata(path,columns=["q301_2","q301_7","q310","q311"],convert_categoricals=False)
    if len(frame)!=SOURCE_ROWS: raise ValueError("row count")
    records=frame.to_dict(orient="records")
    scan=scan_selectors(records)
    if scan!=EXPECTED_F02: raise ValueError("selector replay")
    role_rows=[]; cand_rows=[]
    for c in frontier():
        states={}
        for role,target,atoms in c["roles"]:
            r=query(records,target,atoms); states[role]=r["state"]
            role_rows.append({"candidate":c["id"],"lane":c["lane"],"role":role,"target":target,"atoms":atoms,"fact_state":r["state"],"denominator":r["denominator"],"resolved":r["resolved"],"unresolved":r["unresolved"],"unresolved_states":r["unresolved_states"]})
        terminal="EVALUATED_UNRESOLVED" if "UNRESOLVED" in states.values() else ("EVALUATED_ZERO_SUPPORT" if "ZERO_SUPPORT" in states.values() else "VALIDATION_REACHED")
        cand_rows.append({"candidate":c["id"],"lane":c["lane"],"terminal_state":terminal,"role_states":states})
    role_counts={s:sum(r["fact_state"]==s for r in role_rows) for s in ("SUPPORTED","UNRESOLVED","ZERO_SUPPORT")}
    candidate_counts={}
    for c in cand_rows: candidate_counts[c["terminal_state"]]=candidate_counts.get(c["terminal_state"],0)+1
    lanes={}
    for lane in ("P0","P1","P2","P3","P4"):
        rr=[r for r in role_rows if r["lane"]==lane]; cc=[c for c in cand_rows if c["lane"]==lane]
        lanes[lane]={"candidate_count":len(cc),"query_role_count":len(rr),"query_fact_state_counts":{s:sum(r["fact_state"]==s for r in rr) for s in ("SUPPORTED","UNRESOLVED","ZERO_SUPPORT")},"candidate_terminal_counts":{s:sum(c["terminal_state"]==s for c in cc) for s in sorted(candidate_counts)}}
    semantic={"schema":"I02_CANONICAL_I03_REEXECUTION@1.0.0","status":"PASS__CANONICAL_I03_REPAIR_AND_FULL_FROZEN_REEXECUTION_COMPLETE","source":{"sha256":SOURCE_SHA256,"rows":SOURCE_ROWS,"variables":SOURCE_VARIABLES},"authority":{"d02_commit":D02_AUTHORITY_COMMIT,"d02_frontier_blob":D02_FRONTIER_GIT_BLOB,"f02_commit":F02_RETURN_COMMIT,"f02_release_hash":F02_RELEASE_HASH,"f02_frontier_readoption_hash":F02_FRONTIER_READOPTION_HASH,"g02_preexecution_seal":G02_PREEXECUTION_SEAL,"canonical_i03_blob":CANONICAL_I03_BLOB,"accepted_as2b_commit":AS2B_ACCEPTED_COMMIT},"repair_law":{"canonical_i03":"resolved != denominator => UNRESOLVED","codes_6_7":"SOURCE_SPECIFIC_SPECIAL__NOT_AUTOMATIC_DK_OR_IAP","validation_precedence":"TARGET_RESOLUTION_BEFORE_VALIDATION"},"candidate_count":50,"query_role_count":77,"query_fact_state_counts":role_counts,"candidate_terminal_counts":candidate_counts,"p0_supported_count":0,"learned_positive_workload_gate":"BLOCKED__NO_P0_SUPPORTED_AFTER_CANONICAL_I03_REPAIR","lane_accounting":lanes,"selector_replay":scan,"role_ledger_root":sh(role_rows),"candidate_ledger_root":sh(cand_rows),"frontier_mutation_count":0,"selector_substitution_count":0,"pruning_count":0,"ranking_count":0,"structural_admission_count":0,"causal_promotion_count":0,"population_generalization_count":0,"person_state_count":0,"v3_state_count":0,"negative_ceiling":NEGATIVE_CEILING}
    return {**semantic,"semantic_replay_hash":sh(semantic),"role_rows":role_rows,"candidate_rows":cand_rows}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
    out=execute(a.source); Path(a.output).write_text(json.dumps(canon(out),sort_keys=True,indent=2)+"\n")
if __name__=="__main__": main()
