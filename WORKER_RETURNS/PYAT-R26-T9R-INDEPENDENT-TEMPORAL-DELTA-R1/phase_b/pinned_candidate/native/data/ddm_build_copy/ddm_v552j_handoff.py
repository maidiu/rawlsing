#!/usr/bin/env python3
"""Producer-bound V552J join of V551J packets to V552 structural facts."""
from __future__ import annotations
import hashlib, json
from typing import Any, Mapping
import pandas as pd

V552J_JOIN_SCHEMA_VERSION = "v1.0"
V552J_JOIN_COMPILER_VERSION = "v552j_structural_join_v1"
JOIN_COLUMNS = """run_id v552j_join_id packet_id source_packet_kind source wave canonical_wave country_code shard_id v551j_lane v551j_certification_status v551j_review_status support_status directionality_status authority_status v552_structural_fact_id source_v552_artifact source_v552_structural_fact_ids_json source_v552_structural_fact_lane source_v552_structural_fact_grain source_v552_temporal_key_source_id relation_axis_id target_entity_id driver_facet_id structural_channel_id horizon_constraint_id question_id pressure_score pressure_score_status measurement_evidence_status observed_zero v552_structural_match_status v552_structural_match_score matched_fact_count structural_dimension_status structural_dimensions_resolved_for_v553 resolution_status join_status join_permission repair_debt_status allowed_downstream_use ready_for_v553_probe ready_for_v553_temporal_field allowed_for_v553_probe allowed_for_v553_temporal_field v553_handoff_mode v553_handoff_allowed v553_probe_allowed v553_temporal_field_allowed v553_handoff_blocked_reason certification_score support_score directionality_score authority_score comparability_score confidence_score readiness_score source_v551j_manifest_sha256 source_v552_manifest_sha256 schema_version compiler_version""".split()
AUDIT_COLUMNS = "run_id packet_id source_packet_kind source canonical_wave country_code join_status reason scope_candidate_count semantic_match_count schema_version compiler_version".split()

def _clean(v: Any) -> str:
    if v is None: return ""
    try:
        if pd.isna(v): return ""
    except Exception: pass
    s=str(v).strip(); return "" if s.lower() in {"nan","none","null"} else s

def _number(v: Any) -> float|None:
    try:
        if v is None or pd.isna(v): return None
        x=float(v); return x if pd.notna(x) else None
    except Exception: return None

def _truthy(v: Any)->bool:
    return v if isinstance(v,bool) else _clean(v).lower() in {"1","true","t","yes","y","on"}

def _parse_json_array(v: Any)->list[str]:
    if isinstance(v,(list,tuple,set)): return [_clean(x) for x in v if _clean(x)]
    s=_clean(v)
    if not s:return []
    try: p=json.loads(s)
    except Exception:return [x.strip() for x in s.split("|") if x.strip()]
    return [_clean(x) for x in p if _clean(x)] if isinstance(p,list) else ([_clean(p)] if _clean(p) else [])

def _json_array(values: Any)->str:
    out=[]
    for v in values or []:
        s=_clean(v)
        if s and s not in out: out.append(s)
    return json.dumps(out,sort_keys=True,ensure_ascii=False)

def _first_nonempty(*values: Any, fallback: str="")->str:
    """The module's sole first-value helper."""
    for v in values:
        for x in (v if isinstance(v,(list,tuple,set)) else (v,)):
            s=_clean(x)
            if s:return s
    return fallback

def _row_value(row: Mapping[str,Any]|pd.Series,names:tuple[str,...])->str:
    return _first_nonempty(*[row.get(n) for n in names])

def _scope_identity(row: Mapping[str,Any]|pd.Series)->dict[str,str]:
    return {"run_id":_row_value(row,("run_id","source_run_id","producer_run_id")),"source":_row_value(row,("source","source_family")),"wave":_row_value(row,("canonical_wave","wave")),"country_code":_row_value(row,("country_code","country")),"shard_id":_row_value(row,("shard_id",))}

def _same_scope(packet: Mapping[str,Any]|pd.Series,fact: Mapping[str,Any]|pd.Series)->bool:
    p,f=_scope_identity(packet),_scope_identity(fact)
    if any(not p[k] or not f[k] or p[k]!=f[k] for k in ("run_id","source","wave")):return False
    if p["country_code"] or f["country_code"]:return bool(p["country_code"] and f["country_code"] and p["country_code"]==f["country_code"])
    return bool(p["shard_id"] and f["shard_id"] and p["shard_id"]==f["shard_id"])

def _semantic_values(row: Mapping[str,Any]|pd.Series,plural:str,singular:str)->set[str]:
    vals=set(_parse_json_array(row.get(plural))); one=_clean(row.get(singular))
    if one:vals.add(one)
    return vals

def _structural_fact_match_score(packet_row:pd.Series,fact_row:pd.Series)->int:
    if not _same_scope(packet_row,fact_row):return -1
    score=0
    for plural,singular,weight in (("relation_axis_ids_json","relation_axis_id",4),("target_entity_ids_json","target_entity_id",3),("driver_facet_ids_json","driver_facet_id",3),("question_ids_json","question_id",2)):
        if _clean(fact_row.get(singular)) in _semantic_values(packet_row,plural,singular) and _clean(fact_row.get(singular)):score+=weight
    return score

def _structural_fact_match_policy(score:int)->str:
    return "scope_mismatch" if score<0 else "exact_structural_match" if score>=8 else "partial_structural_match" if score>=5 else "question_match_only" if score>=2 else "broad_context_match" if score>=1 else "no_match"

def _packet_structural_dimension_resolution(packet_row:pd.Series,v552_structural_fact_index:pd.DataFrame,v552_temporal_key_source_index:pd.DataFrame)->dict[str,Any]:
    """Resolve only inside exact run/source/wave/country-or-shard scope; kept public for V553."""
    existing=_clean(packet_row.get("source_v552_structural_fact_id") or packet_row.get("v552_structural_fact_id"))
    prejoined=_clean(packet_row.get("join_status"))=="MATCHED_EXACT_SCOPE" and bool(existing)
    base={"source_v552_artifact":_clean(packet_row.get("source_v552_artifact")),"source_v552_structural_fact_id":existing,"source_v552_structural_fact_ids_json":_json_array([existing] if existing else []),"source_v552_structural_fact_ids_diagnostic_json":_json_array([existing] if existing else []),"source_v552_temporal_key_source_id":_clean(packet_row.get("source_v552_temporal_key_source_id")),"source_v552_temporal_key_source_ids_json":"[]","source_v552_temporal_key_source_row_ids_json":"[]","source_v552_structural_fact_status":_clean(packet_row.get("measurement_evidence_status")),"source_v552_structural_fact_lane":_clean(packet_row.get("source_v552_structural_fact_lane")),"source_v552_structural_fact_grain":_clean(packet_row.get("source_v552_structural_fact_grain")),"structural_dimension_status":"resolved" if prejoined else "missing","structural_dimension_blocker_reason":"" if prejoined else "no_exact_scope_v552_structural_fact","relation_axis_id":_clean(packet_row.get("relation_axis_id")) if prejoined else "","target_entity_id":_clean(packet_row.get("target_entity_id")) if prejoined else "","driver_facet_id":_clean(packet_row.get("driver_facet_id")) if prejoined else "","structural_channel_id":_clean(packet_row.get("structural_channel_id")) if prejoined else "","horizon_constraint_id":_clean(packet_row.get("horizon_constraint_id")) if prejoined else "","semantic_signature":_clean(packet_row.get("semantic_signature")) if prejoined else "","v552_structural_match_status":"preserved_joined_v552_fact" if prejoined else "no_match","v552_structural_match_score":int(packet_row.get("v552_structural_match_score",0) or 0) if prejoined else 0,"v552_structural_match_reason":"producer_bound_v552j_join" if prejoined else "no_exact_scope_v552_structural_fact","matched_fact_count":1 if prejoined else 0,"broad_match_count":0,"temporal_key_basis":json.dumps(_scope_identity(packet_row),sort_keys=True),"temporal_key_candidate_status":"resolved" if prejoined else "blocked","temporal_key_blocker_reason":"" if prejoined else "no_exact_scope_v552_structural_fact","fallback_permission_profile_key":"","fallback_used":False,"resolution_status":"preserved_joined_v552_fact" if prejoined else "no_exact_scope_match","allowed_downstream_use":bool(prejoined and _truthy(packet_row.get("allowed_downstream_use"))),"source_v552_fact_matches":[]}
    if v552_structural_fact_index.empty:return base
    facts=v552_structural_fact_index.copy(); facts["_match_score"]=facts.apply(lambda r:_structural_fact_match_score(packet_row,r),axis=1); facts=facts.loc[facts["_match_score"].ge(0)]
    if facts.empty:return base
    matched=facts.loc[facts["_match_score"].gt(0)].copy()
    if matched.empty:return {**base,"v552_structural_match_reason":"exact_scope_but_no_semantic_match"}
    matched=matched.sort_values(["_match_score"]+(["v552_structural_fact_id"] if "v552_structural_fact_id" in matched else []),ascending=False,kind="mergesort").reset_index(drop=True)
    primary=matched.iloc[0]; score=int(primary["_match_score"]); policy=_structural_fact_match_policy(score); resolved=policy in {"exact_structural_match","partial_structural_match"}; fid=_clean(primary.get("v552_structural_fact_id")); tid=""; rowids=[]
    if resolved and fid and not v552_temporal_key_source_index.empty and "v552_structural_fact_id" in v552_temporal_key_source_index:
        t=v552_temporal_key_source_index.loc[v552_temporal_key_source_index["v552_structural_fact_id"].astype(str).eq(fid)]
        if not t.empty:
            tid=_first_nonempty(t.get("v552_temporal_key_source_id",pd.Series(dtype=str)).tolist()); rowids=[_clean(x) for x in t.get("source_row_id",pd.Series(dtype=str)).tolist() if _clean(x)]
    return {**base,"source_v552_artifact":_clean(primary.get("source_artifact")),"source_v552_structural_fact_id":fid if resolved else "","source_v552_structural_fact_ids_json":_json_array([fid] if resolved and fid else []),"source_v552_structural_fact_ids_diagnostic_json":_json_array([_clean(x) for x in matched.get("v552_structural_fact_id",pd.Series(dtype=str)).tolist() if _clean(x)]),"source_v552_temporal_key_source_id":tid if resolved else "","source_v552_temporal_key_source_ids_json":_json_array([tid] if resolved and tid else []),"source_v552_temporal_key_source_row_ids_json":_json_array(rowids if resolved else []),"source_v552_structural_fact_status":_clean(primary.get("structural_fact_status")) if resolved else "","source_v552_structural_fact_lane":_clean(primary.get("structural_fact_lane")) if resolved else "","source_v552_structural_fact_grain":_clean(primary.get("structural_fact_grain")) if resolved else "","structural_dimension_status":"resolved" if resolved else "probe_only","structural_dimension_blocker_reason":"" if resolved else "semantic_match_below_structural_threshold","relation_axis_id":_clean(primary.get("relation_axis_id")) if resolved else "","target_entity_id":_clean(primary.get("target_entity_id")) if resolved else "","driver_facet_id":_clean(primary.get("driver_facet_id")) if resolved else "","structural_channel_id":_clean(primary.get("structural_channel_id")) if resolved else "","horizon_constraint_id":_clean(primary.get("horizon_constraint_id")) if resolved else "","semantic_signature":_clean(primary.get("semantic_signature")) if resolved else "","v552_structural_match_status":policy,"v552_structural_match_score":score,"v552_structural_match_reason":"matched_inside_exact_scope" if resolved else "semantic_match_below_structural_threshold","matched_fact_count":len(matched),"broad_match_count":int(matched["_match_score"].lt(5).sum()),"temporal_key_basis":json.dumps({**_scope_identity(packet_row),"v552_structural_fact_id":fid},sort_keys=True),"temporal_key_candidate_status":"resolved" if resolved else "probe_only","temporal_key_blocker_reason":"" if resolved else "semantic_match_below_structural_threshold","resolution_status":"resolved_structural_match" if resolved else "probe_only_structural_context","allowed_downstream_use":resolved,"source_v552_fact_matches":matched.to_dict("records")}

def _score(value:Any,mapping:Mapping[str,float],default:float=0.0)->float:return float(mapping.get(_clean(value),default))
def _packet_score_bundle(row:pd.Series,comparability_context:dict[str,Any]|None=None,ready_for_v553:bool=True)->dict[str,float]:
    cert=_score(_first_nonempty(row.get("normalized_v551j_certification_status"),row.get("certification_status")),{"certified":1,"CERTIFIED_JOINT_RELATION_EVIDENCE":1,"CERTIFIED_JOINT_RELATION_EVIDENCE_WITH_CONTEXT":1},.65 if _truthy(row.get("review_required")) else 0)
    sup=_score(_first_nonempty(row.get("normalized_support_status"),row.get("joint_support_status"),row.get("support_status")),{"sufficient_support":1,"supported":1,"underpowered":.45,"low_support":.45,"not_applicable":.6})
    dire=_score(_first_nonempty(row.get("normalized_directionality_status"),row.get("joint_directionality_authority_status"),row.get("directionality_status")),{"known_directional":1,"CERTIFIED":1,"partial_directionality":.6,"REVIEW_REQUIRED":.6,"not_applicable":.45})
    auth=_score(_first_nonempty(row.get("normalized_authority_status"),row.get("joint_evidence_authority_status"),row.get("authority_status")),{"exact_registry":1,"CERTIFIED":1,"manual_review":.75,"REVIEW_REQUIRED":.75,"computed_context":.5})
    comp=_score((comparability_context or {}).get("status"),{"READY_V551J_CROSS_WAVE_DIFF":1,"READY_V551J_CROSS_WAVE_DIFF_WITH_GAPS":.75,"READY_V551J_SINGLE_WAVE_ONLY":.5}); conf=(cert+sup+dire+auth)/4; ready=(.28*cert+.24*sup+.24*dire+.14*auth+.10*comp)*(1 if ready_for_v553 else .85)
    return {"certification_score":round(cert,6),"support_score":round(sup,6),"directionality_score":round(dire,6),"authority_score":round(auth,6),"comparability_score":round(comp,6),"confidence_score":round(conf,6),"readiness_score":round(max(0,min(1,ready)),6)}

def _stable_id(payload:Mapping[str,Any])->str:return "v552jjoin__"+hashlib.sha256(json.dumps(dict(payload),sort_keys=True,default=str,separators=(",",":")).encode()).hexdigest()[:24]
def _packet_lane(row:Mapping[str,Any],kind:str)->tuple[str,str,str]:
    cert=_clean(row.get("certification_status") or row.get("v551j_evidence_certification_status")); review=_clean(row.get("review_surface_status") or row.get("v551j_review_surface_status"))
    return ("certified_spine",cert or "certified",review) if kind=="certified" else ("reviewable_context",cert or "reviewable",review or "reviewable")
def _packet_rows(certified:pd.DataFrame,review:pd.DataFrame)->list[tuple[str,dict[str,Any]]]:
    out=[];seen=set()
    for kind,frame in (("certified",certified),("review",review)):
        for row in ([] if frame.empty else frame.to_dict("records")):
            pid=_clean(row.get("packet_id") or row.get("v551j_packet_id"))
            if pid and pid not in seen:out.append((kind,row));seen.add(pid)
    return out

def _derive_join_state(a:Mapping[str,Any],b:Mapping[str,Any],join:pd.DataFrame)->dict[str,str]:
    evidence={_clean(a.get("evidence_status")),_clean(b.get("evidence_status"))}; perms={_clean(a.get("downstream_permission_status")),_clean(b.get("downstream_permission_status"))}
    if "APPLICABLE_UNRESOLVED" in evidence:return {"run_integrity_status":"PASS","evidence_status":"APPLICABLE_UNRESOLVED","downstream_permission_status":"DENY","state_detail":"UPSTREAM_APPLICABLE_UNRESOLVED"}
    if not join.empty and join["join_permission"].eq("ALLOW").any():return {"run_integrity_status":"PASS","evidence_status":"PRESENT","downstream_permission_status":"ALLOW","state_detail":"EXACT_SCOPE_JOIN_PRESENT"}
    if not join.empty:return {"run_integrity_status":"PASS","evidence_status":"PRESENT","downstream_permission_status":"DENY","state_detail":"REVIEW_OR_NONPERMITTED_JOIN_PRESENT"}
    if "NOT_APPLICABLE" in evidence:return {"run_integrity_status":"PASS","evidence_status":"NOT_APPLICABLE","downstream_permission_status":"NOT_APPLICABLE","state_detail":"JOIN_NOT_APPLICABLE_FROM_UPSTREAM"}
    if "VALID_EMPTY" in evidence:return {"run_integrity_status":"PASS","evidence_status":"VALID_EMPTY","downstream_permission_status":"NOT_APPLICABLE","state_detail":"VALID_EMPTY_UPSTREAM_JOIN_INPUT"}
    if evidence=={"PRESENT"} and perms.issubset({"ALLOW","DENY","NOT_APPLICABLE"}):return {"run_integrity_status":"PASS","evidence_status":"APPLICABLE_UNRESOLVED","downstream_permission_status":"DENY","state_detail":"PRESENT_BRANCHES_WITHOUT_EXACT_JOIN"}
    return {"run_integrity_status":"PASS","evidence_status":"VALID_EMPTY","downstream_permission_status":"NOT_APPLICABLE","state_detail":"VALID_EMPTY_JOIN"}
def _mean_or_none(df:pd.DataFrame,col:str)->float|None:
    if df.empty or col not in df:return None
    v=pd.to_numeric(df[col],errors="coerce").dropna(); return None if v.empty else round(float(v.mean()),6)

def build_v552j_join(*,run_id:str,v551j_certified:pd.DataFrame,v551j_review:pd.DataFrame,v552_structural_facts:pd.DataFrame,v552_temporal_keys:pd.DataFrame|None=None,v551j_state:Mapping[str,Any],v552_state:Mapping[str,Any],v551j_manifest_sha256:str="",v552_manifest_sha256:str="")->dict[str,Any]:
    temporal=v552_temporal_keys if v552_temporal_keys is not None else pd.DataFrame(); rows=[]; audits=[]; present=_clean(v551j_state.get("evidence_status"))=="PRESENT" and _clean(v552_state.get("evidence_status"))=="PRESENT"
    if present:
        for kind,p in _packet_rows(v551j_certified,v551j_review):
            ps=pd.Series(p); res=_packet_structural_dimension_resolution(ps,v552_structural_facts,temporal); pid=_clean(p.get("packet_id") or p.get("v551j_packet_id")); scope_count=sum(_same_scope(p,f) for f in v552_structural_facts.to_dict("records")); matches=res.get("source_v552_fact_matches") or []
            if not res["source_v552_structural_fact_id"]:
                audits.append({"run_id":run_id,"packet_id":pid,"source_packet_kind":kind,"source":_scope_identity(p)["source"],"canonical_wave":_scope_identity(p)["wave"],"country_code":_scope_identity(p)["country_code"],"join_status":"UNRESOLVED_NO_STRUCTURAL_MATCH","reason":res["v552_structural_match_reason"],"scope_candidate_count":scope_count,"semantic_match_count":int(res.get("matched_fact_count",0)),"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION});continue
            fact=matches[0] if matches else {}; lane,cert,review=_packet_lane(p,kind); scores=_packet_score_bundle(ps); pstatus=_clean(fact.get("pressure_score_status") or fact.get("pressure_computation_status")); pvalue=_number(fact.get("pressure_score")); mstatus=_clean(fact.get("measurement_evidence_status") or fact.get("structural_fact_status")); producer_allow=_clean(v551j_state.get("downstream_permission_status"))=="ALLOW" and _clean(v552_state.get("downstream_permission_status"))=="ALLOW"; observed=pstatus in {"OBSERVED_ZERO","OBSERVED_NONZERO"} and mstatus not in {"APPLICABLE_BUT_UNRESOLVED","NOT_APPLICABLE"}; allow=kind=="certified" and producer_allow and _clean(fact.get("downstream_permission_status"))=="ALLOW" and observed; permission="ALLOW" if allow else ("REVIEW_ONLY" if kind=="review" else "DENY"); debt="APPLICABLE_BUT_UNRESOLVED" if "APPLICABLE_BUT_UNRESOLVED" in {pstatus,mstatus} else ("REVIEW_REQUIRED" if kind=="review" else "NONE"); fid=_clean(res["source_v552_structural_fact_id"]); scope=_scope_identity(p)
            row={"run_id":run_id,"v552j_join_id":_stable_id({"run_id":run_id,"packet_id":pid,"v552_structural_fact_id":fid}),"packet_id":pid,"source_packet_kind":kind,"source":scope["source"],"wave":scope["wave"],"canonical_wave":scope["wave"],"country_code":scope["country_code"],"shard_id":scope["shard_id"],"v551j_lane":lane,"v551j_certification_status":cert,"v551j_review_status":review,"support_status":_first_nonempty(p.get("joint_support_status"),p.get("support_status")),"directionality_status":_first_nonempty(p.get("joint_directionality_authority_status"),p.get("directionality_status")),"authority_status":_first_nonempty(p.get("joint_evidence_authority_status"),p.get("authority_status")),"v552_structural_fact_id":fid,"source_v552_artifact":_clean(res["source_v552_artifact"]),"source_v552_structural_fact_ids_json":res["source_v552_structural_fact_ids_json"],"source_v552_structural_fact_lane":res["source_v552_structural_fact_lane"],"source_v552_structural_fact_grain":res["source_v552_structural_fact_grain"],"source_v552_temporal_key_source_id":res["source_v552_temporal_key_source_id"],"relation_axis_id":res["relation_axis_id"],"target_entity_id":res["target_entity_id"],"driver_facet_id":res["driver_facet_id"],"structural_channel_id":res["structural_channel_id"],"horizon_constraint_id":res["horizon_constraint_id"],"question_id":_clean(fact.get("question_id")),"pressure_score":pvalue,"pressure_score_status":pstatus,"measurement_evidence_status":mstatus,"observed_zero":bool(pstatus=="OBSERVED_ZERO" and pvalue is not None and abs(pvalue)<=1e-12),"v552_structural_match_status":res["v552_structural_match_status"],"v552_structural_match_score":res["v552_structural_match_score"],"matched_fact_count":res["matched_fact_count"],"structural_dimension_status":res["structural_dimension_status"],"structural_dimensions_resolved_for_v553":res["structural_dimension_status"]=="resolved","resolution_status":res["resolution_status"],"join_status":"MATCHED_EXACT_SCOPE","join_permission":permission,"repair_debt_status":debt,"allowed_downstream_use":permission=="ALLOW","ready_for_v553_probe":permission=="ALLOW","ready_for_v553_temporal_field":False,"allowed_for_v553_probe":permission=="ALLOW","allowed_for_v553_temporal_field":False,"v553_handoff_mode":"probe_only" if permission=="ALLOW" else "blocked_context","v553_handoff_allowed":permission=="ALLOW","v553_probe_allowed":permission=="ALLOW","v553_temporal_field_allowed":False,"v553_handoff_blocked_reason":"" if permission=="ALLOW" else (debt if debt!="NONE" else "producer_permission_denied"),**scores,"source_v551j_manifest_sha256":v551j_manifest_sha256,"source_v552_manifest_sha256":v552_manifest_sha256,"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION};rows.append(row);audits.append({"run_id":run_id,"packet_id":pid,"source_packet_kind":kind,"source":row["source"],"canonical_wave":row["canonical_wave"],"country_code":row["country_code"],"join_status":row["join_status"],"reason":permission,"scope_candidate_count":scope_count,"semantic_match_count":int(res.get("matched_fact_count",0)),"schema_version":V552J_JOIN_SCHEMA_VERSION,"compiler_version":V552J_JOIN_COMPILER_VERSION})
    join=pd.DataFrame(rows,columns=JOIN_COLUMNS); audit=pd.DataFrame(audits,columns=AUDIT_COLUMNS); st=_derive_join_state(v551j_state,v552_state,join); constraints=join.loc[join["join_permission"].eq("ALLOW")].copy() if not join.empty else join.copy(); metrics={"constraint_count":len(constraints),"review_context_count":int(join["join_permission"].eq("REVIEW_ONLY").sum()) if not join.empty else 0,"denied_join_count":int(join["join_permission"].eq("DENY").sum()) if not join.empty else 0,"observed_zero_count":int(join["observed_zero"].map(_truthy).sum()) if not join.empty else 0,"unresolved_join_count":int(audit["join_status"].eq("UNRESOLVED_NO_STRUCTURAL_MATCH").sum()) if not audit.empty else 0}
    for col in ("certification_score","support_score","directionality_score","authority_score","comparability_score","confidence_score","readiness_score"):metrics[f"mean_{col}"]=_mean_or_none(constraints,col)
    return {"join_index":join,"join_audit":audit,"state":st,"metrics":metrics}

def build_v552j_structural_handoff(**kwargs:Any)->dict[str,Any]:
    required={"run_id","v551j_certified","v551j_review","v552_structural_facts","v551j_state","v552_state"}
    if not required.issubset(kwargs):raise RuntimeError("V552J_PRODUCER_BOUND_JOIN_REQUIRES_VERIFIED_FRAMES:"+",".join(sorted(required-set(kwargs))))
    keep=required|{"v552_temporal_keys","v551j_manifest_sha256","v552_manifest_sha256"};return build_v552j_join(**{k:v for k,v in kwargs.items() if k in keep})
