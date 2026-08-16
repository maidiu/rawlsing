#!/usr/bin/env python3
"""Canonical V551 directional adjudication and relation-evidence atom compiler.

V551 contract v3.0. Applicability is inherited from V550; V551 alone owns the
canonical signed projection. Candidate disposition is terminal before atom
emission, so repair debt cannot contaminate the atom pack.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

V551_SCHEMA_VERSION = "v3.0"
V551_COMPILER_VERSION = "v3.0"
APPLICABLE_BY_AUTHORITY = "APPLICABLE_BY_AUTHORITY"
APPROVED_DIRECT_TABLES = {"answer_distribution", "country_answer_distribution"}
CERTIFIED_DIRECTIONS = {"positive", "negative", "neutral", "support", "oppose", "agree", "disagree", "graded", "intermediate"}
POSITIVE_DIRECTIONS = {"positive", "support", "agree"}
NEGATIVE_DIRECTIONS = {"negative", "oppose", "disagree"}

SCALE_REGISTRY_PATH = Path(__file__).resolve().parent / "authority" / "response_scale_encoding_registry_35wave_active_v1.csv"
SCALE_REGISTRY_MANIFEST_PATH = Path(__file__).resolve().parent / "authority" / "response_scale_encoding_registry_35wave_active_v1.manifest.json"
SCALE_REGISTRY_SCHEMA_VERSION = "v551_scale_encoding_registry_35wave_active_v1"

CANDIDATE_ID_FIELDS = ["source","source_family","canonical_wave","country_code","analysis_scope","source_table","question_id","var_code","position_field","position_value","response_value_normalized","source_row_hash","response_semantics_contract_hash"]
DISTRIBUTION_ID_FIELDS = ["source","source_family","canonical_wave","country_code","analysis_scope","source_table","question_id","var_code","position_field","position_value","response_semantics_contract_hash","response_family","response_topology","relation_axis_id","target_entity_id","driver_id","driver_facet_id"]

ADJUDICATION_COLUMNS = ["run_id","candidate_id","empirical_distribution_id","source","source_family","wave","canonical_wave","country_code","survey_year","analysis_scope","source_table","source_row_hash","question_id","var_code","position_field","position_value","response_value_raw","response_value_normalized","response_label","response_family","directional_applicability_status","response_semantics_contract_hash","question_use_contract_row_hash","question_use_contract_artifact_hash","producer_lineage_status","raw_response_direction","raw_response_intensity","raw_response_intensity_status","authority_intensity_semantics","v551_signed_side","v551_signed_intensity","v551_projection_rule_id","v551_projection_authority_hash","adjudication_outcome","adjudication_reason","promotable","n_unweighted","n_weighted","pct_unweighted","pct_weighted","weight_status","relation_axis_id","target_entity_id","driver_id","driver_facet_id","strata_path","subject_position_signature","schema_version","compiler_version"]
ATOM_COLUMNS = ["run_id","atom_id","candidate_id","empirical_distribution_id","source","source_family","wave","canonical_wave","country_code","survey_year","analysis_scope","empirical_object_type","empirical_object_id","source_table","source_row_hash","question_id","var_code","position_field","position_value","response_value_raw","response_value_normalized","response_label","normalized_response_label","response_family","response_topology","response_direction","response_intensity","response_intensity_status","authority_intensity_semantics","v551_signed_side","v551_signed_intensity","v551_projection_rule_id","v551_projection_authority_hash","semantic_role","semantic_subrole","semantic_tags","directionality_policy","driver_id","driver_facet_id","relation_axis_id","target_entity_id","strata_relevance","strata_path","subject_position_signature","position_conditioning","position_modifiers","conditional_strata_weights","horizon_affordance","n_unweighted","n_respondents","n_weighted","pct_unweighted","pct_weighted","weight_status","support_status","confidence_tier","response_semantics_contract_hash","question_use_contract_row_hash","question_use_contract_artifact_hash","producer_lineage_status","evidence_basis","provenance_basis","measurement_contract_hash","atom_contract_hash","schema_version","compiler_version"]
COVERAGE_COLUMNS = ["run_id","empirical_distribution_id","source","source_family","canonical_wave","country_code","analysis_scope","source_table","question_id","var_code","position_field","position_value","applicable_candidate_count","promotable_candidate_count","nonpromotable_candidate_count","neutral_candidate_count","selected_substantive_n_unweighted","promotable_n_unweighted","nonpromotable_n_unweighted","neutral_n_unweighted","selected_substantive_n_weighted","promotable_n_weighted","nonpromotable_n_weighted","neutral_n_weighted","selected_surface_status","directional_adjudication_status","candidate_count_conserved","unweighted_mass_conserved","weighted_mass_conserved","schema_version","compiler_version"]
_registry_cache: dict[str, dict[str, str]] | None = None

def _clean(value: Any) -> str:
    if value is None:return ""
    try:
        if pd.isna(value):return ""
    except Exception:pass
    text=str(value).strip();return "" if text.lower() in {"nan","none","null"} else text

def _bool(value: Any, default: bool=False)->bool:
    if isinstance(value,bool):return value
    text=_clean(value).lower()
    if text in {"1","true","t","yes","y","on"}:return True
    if text in {"0","false","f","no","n","off",""}:return False
    return default

def _float(value: Any)->float|None:
    try:
        if value is None or pd.isna(value):return None
        out=float(value);return out if math.isfinite(out) else None
    except Exception:return None

def _hash(payload: Mapping[str,Any])->str:
    return hashlib.sha256(json.dumps(dict(payload),sort_keys=True,separators=(",",":"),default=str,ensure_ascii=False).encode()).hexdigest()

def _identity(prefix:str,row:Mapping[str,Any],fields:list[str])->str:
    return prefix+_hash({field:_clean(row.get(field)) for field in fields})[:24]

def _candidate_id(row:Mapping[str,Any])->str:return _identity("v551cand__",row,CANDIDATE_ID_FIELDS)
def _distribution_id(row:Mapping[str,Any])->str:return _identity("v551dist__",row,DISTRIBUTION_ID_FIELDS)

def _raw_direction(row:Mapping[str,Any])->str:
    value=_clean(row.get("response_direction")).lower();return value if value in CERTIFIED_DIRECTIONS else ""

def _raw_intensity(row:Mapping[str,Any])->float|None:return _float(row.get("response_intensity"))
def _intensity_status(value:float|None)->str:return "OBSERVED_NUMERIC" if value is not None else "MISSING"

def _load_registry()->dict[str,dict[str,str]]:
    global _registry_cache
    if _registry_cache is not None:return _registry_cache
    if not SCALE_REGISTRY_PATH.exists() or not SCALE_REGISTRY_MANIFEST_PATH.exists():raise RuntimeError("BLOCKED_MISSING_V551_SCALE_AUTHORITY")
    manifest=json.loads(SCALE_REGISTRY_MANIFEST_PATH.read_text(encoding="utf-8"))
    if _clean(manifest.get("schema_version"))!=SCALE_REGISTRY_SCHEMA_VERSION:raise RuntimeError("BLOCKED_SCALE_REGISTRY_MANIFEST_SCHEMA")
    actual=hashlib.sha256(SCALE_REGISTRY_PATH.read_bytes()).hexdigest()
    if _clean(manifest.get("registry_sha256"))!=actual:raise RuntimeError("BLOCKED_SCALE_REGISTRY_MANIFEST_HASH_MISMATCH")
    frame=pd.read_csv(SCALE_REGISTRY_PATH,dtype=str).fillna("")
    required={"response_semantics_contract_hash","authority_intensity_semantics","projection_rule_id","authority_status","review_status"};missing=sorted(required-set(frame.columns))
    if missing:raise RuntimeError("BLOCKED_SCALE_REGISTRY_SCHEMA:"+",".join(missing))
    keys=frame["response_semantics_contract_hash"].astype(str).str.strip()
    if keys.eq("").any() or keys.duplicated().any():raise RuntimeError("BLOCKED_SCALE_REGISTRY_IDENTITY")
    if frame["authority_status"].astype(str).str.upper().ne("CERTIFIED").any():raise RuntimeError("BLOCKED_UNCERTIFIED_SCALE_AUTHORITY")
    _registry_cache={str(r["response_semantics_contract_hash"]).strip():{c:str(r[c]).strip() for c in frame.columns} for _,r in frame.iterrows()};return _registry_cache

def _signed_projection(row:Mapping[str,Any],authority:Mapping[str,str])->tuple[str,float|None,str,str]:
    direction=_raw_direction(row);raw=_raw_intensity(row);semantics=_clean(authority.get("authority_intensity_semantics")).upper();rule=_clean(authority.get("projection_rule_id"))
    if not direction:return "",None,rule,"missing_certified_response_direction"
    if direction=="neutral":return "neutral",0.0,rule,""
    if semantics=="DIRECTIONAL_MAGNITUDE":
        if raw is None:return "",None,rule,"missing_required_response_intensity"
        side="positive" if direction in POSITIVE_DIRECTIONS else "negative" if direction in NEGATIVE_DIRECTIONS else ""
        if not side:return "",None,rule,"direction_requires_coordinate_geometry"
        if raw<0:return "",None,rule,"invalid_negative_response_intensity"
        return side,float(raw),rule,""
    if semantics=="ORDINAL_COORDINATE":
        if raw is None:return "",None,rule,"missing_required_response_intensity"
        neutral=_float(authority.get("neutral_coordinate"));boundary=_float(authority.get("neutral_boundary"));pivot=neutral if neutral is not None else boundary;neg=_float(authority.get("negative_endpoint"));pos=_float(authority.get("positive_endpoint"))
        if pivot is None or neg is None or pos is None or neg==pivot or pos==pivot:return "",None,rule,"invalid_authority_geometry"
        if direction in POSITIVE_DIRECTIONS:side="positive"
        elif direction in NEGATIVE_DIRECTIONS:side="negative"
        elif direction in {"graded","intermediate"}:
            if raw==pivot:side="neutral"
            else:side="negative" if abs(raw-neg)<abs(raw-pos) else "positive"
        else:return "",None,rule,"unsupported_response_direction"
        if side=="neutral":return "neutral",0.0,rule,""
        endpoint=neg if side=="negative" else pos;magnitude=abs(raw-pivot)/abs(endpoint-pivot)
        if magnitude<0 or magnitude>1.0000001:return "",None,rule,"coordinate_outside_authority_geometry"
        return side,round(min(1.0,magnitude),6),rule,""
    return "",None,rule,"unsupported_authority_intensity_semantics"

def validate_v551_bridge_input_contract(bridge:pd.DataFrame)->dict[str,Any]:
    required={"run_id","source","source_family","wave","canonical_wave","country_code","analysis_scope","source_table","source_row_hash","question_id","var_code","position_field","position_value","response_value_normalized","response_family","response_direction","response_intensity","directional_applicability_status","bridge_evidence_lane","is_substantive","is_missing","is_special","response_semantics_contract_hash","semantic_role","semantic_role_authority_status","response_semantics_authority_status","directionality_authority_status","structural_mapping_status","response_option_map_matched","usable_for_evidence","allowed_as_v551_relation_evidence","n_unweighted"}
    missing=sorted(required-set(bridge.columns));return {"status":"PASS" if not missing else "BLOCKED_V551_MISSING_BRIDGE_CONTRACT","bridge_rows":len(bridge),"missing_columns":missing}

def build_v551_certification_candidate_bridge(bridge:pd.DataFrame)->pd.DataFrame:
    contract=validate_v551_bridge_input_contract(bridge)
    if contract["status"]!="PASS":raise ValueError(contract["status"]+":"+",".join(contract["missing_columns"]))
    if bridge.empty:return bridge.copy()
    mask=(bridge["directional_applicability_status"].fillna("").astype(str).str.upper().eq(APPLICABLE_BY_AUTHORITY)&bridge["bridge_evidence_lane"].fillna("").astype(str).eq("direct_relation_response")&bridge["source_table"].fillna("").astype(str).isin(APPROVED_DIRECT_TABLES)&bridge["is_substantive"].map(_bool)&~bridge["is_missing"].map(_bool)&~bridge["is_special"].map(_bool))
    out=bridge.loc[mask].copy().reset_index(drop=True);out["candidate_id"]=[_candidate_id(r) for r in out.to_dict("records")]
    if out["candidate_id"].duplicated().any():raise RuntimeError("BLOCKED_DUPLICATE_V551_CANDIDATE_ID")
    return out

def _reasons(row:Mapping[str,Any],projection_reason:str,authority_found:bool)->list[str]:
    reasons=[]
    if not authority_found:reasons.append("missing_exact_response_semantics_contract_authority")
    if projection_reason:reasons.append(projection_reason)
    checks=[(_clean(row.get("semantic_role"))=="RELATION_EVIDENCE","semantic_role_not_relation_evidence"),(_clean(row.get("semantic_role_authority_status")).upper()=="CERTIFIED","semantic_role_authority_not_certified"),(_clean(row.get("response_semantics_authority_status")).upper()=="CERTIFIED","response_semantics_authority_not_certified"),(_clean(row.get("directionality_authority_status")).upper()=="CERTIFIED","directionality_authority_not_certified"),(_clean(row.get("structural_mapping_status")).upper()=="COMPLETE","structural_mapping_not_complete"),(_bool(row.get("response_option_map_matched")),"response_option_map_unmatched"),(_bool(row.get("usable_for_evidence")),"not_usable_for_evidence"),(_bool(row.get("allowed_as_v551_relation_evidence")),"question_use_contract_disallows_v551_relation_evidence"),(not _bool(row.get("manual_review_flag")),"manual_review_required"),(not _bool(row.get("source_structure_review_required")),"source_structure_review_required")]
    for ok,reason in checks:
        if not ok:reasons.append(reason)
    return list(dict.fromkeys(reasons))

def _producer_lineage(row:Mapping[str,Any])->tuple[str,str,str]:
    row_hash=_clean(row.get("question_use_contract_row_hash")) or _clean(row.get("question_use_contract_hash"));artifact_hash=_clean(row.get("question_use_contract_artifact_hash"))
    status="PRODUCER_ROW_AND_ARTIFACT_DECLARED" if row_hash and artifact_hash else "PRODUCER_ROW_HASH_ONLY" if row_hash else "PRODUCER_QUESTION_USE_HASH_UNAVAILABLE";return row_hash,artifact_hash,status

def build_v551_directional_candidate_adjudication(bridge:pd.DataFrame)->pd.DataFrame:
    candidates=build_v551_certification_candidate_bridge(bridge);registry=_load_registry();rows=[]
    for r in candidates.to_dict("records"):
        contract_hash=_clean(r.get("response_semantics_contract_hash"));authority=registry.get(contract_hash)
        if authority:
            side,signed,rule,projection_reason=_signed_projection(r,authority);semantics=_clean(authority.get("authority_intensity_semantics")).upper();authority_hash=_hash({k:authority[k] for k in sorted(authority)})
        else:side,signed,rule,projection_reason="",None,"","";semantics,authority_hash="",""
        reasons=_reasons(r,projection_reason,authority is not None);raw_i=_raw_intensity(r);raw_d=_raw_direction(r);qrow,qartifact,lineage=_producer_lineage(r)
        outcome="PROMOTABLE" if not reasons else "NONPROMOTABLE_REPAIRABLE"
        rows.append({"run_id":_clean(r.get("run_id")),"candidate_id":_candidate_id(r),"empirical_distribution_id":_distribution_id(r),"source":_clean(r.get("source")),"source_family":_clean(r.get("source_family")),"wave":_clean(r.get("wave")),"canonical_wave":_clean(r.get("canonical_wave")),"country_code":_clean(r.get("country_code")),"survey_year":r.get("survey_year"),"analysis_scope":_clean(r.get("analysis_scope")),"source_table":_clean(r.get("source_table")),"source_row_hash":_clean(r.get("source_row_hash")),"question_id":_clean(r.get("question_id")),"var_code":_clean(r.get("var_code")),"position_field":_clean(r.get("position_field")),"position_value":_clean(r.get("position_value")),"response_value_raw":_clean(r.get("response_value_raw")),"response_value_normalized":_clean(r.get("response_value_normalized")),"response_label":_clean(r.get("response_label")),"response_family":_clean(r.get("response_family")),"directional_applicability_status":_clean(r.get("directional_applicability_status")).upper(),"response_semantics_contract_hash":contract_hash,"question_use_contract_row_hash":qrow,"question_use_contract_artifact_hash":qartifact,"producer_lineage_status":lineage,"raw_response_direction":raw_d,"raw_response_intensity":raw_i,"raw_response_intensity_status":_intensity_status(raw_i),"authority_intensity_semantics":semantics,"v551_signed_side":side,"v551_signed_intensity":signed,"v551_projection_rule_id":rule,"v551_projection_authority_hash":authority_hash,"adjudication_outcome":outcome,"adjudication_reason":"|".join(reasons),"promotable":outcome=="PROMOTABLE","n_unweighted":_float(r.get("n_unweighted")),"n_weighted":_float(r.get("n_weighted")),"pct_unweighted":_float(r.get("pct_unweighted")),"pct_weighted":_float(r.get("pct_weighted")),"weight_status":_clean(r.get("weight_status")),"relation_axis_id":_clean(r.get("relation_axis_id")),"target_entity_id":_clean(r.get("target_entity_id")),"driver_id":_clean(r.get("driver_id")),"driver_facet_id":_clean(r.get("driver_facet_id")),"strata_path":_clean(r.get("strata_path")),"subject_position_signature":_clean(r.get("subject_position_signature")),"schema_version":V551_SCHEMA_VERSION,"compiler_version":V551_COMPILER_VERSION})
    return pd.DataFrame(rows,columns=ADJUDICATION_COLUMNS)

def _atom_from(row:Mapping[str,Any],adjud:Mapping[str,Any])->dict[str,Any]:
    result={"run_id":_clean(row.get("run_id")),"candidate_id":adjud["candidate_id"],"empirical_distribution_id":adjud["empirical_distribution_id"],"source":_clean(row.get("source")),"source_family":_clean(row.get("source_family")),"wave":_clean(row.get("wave")),"canonical_wave":_clean(row.get("canonical_wave")),"country_code":_clean(row.get("country_code")),"survey_year":row.get("survey_year"),"analysis_scope":_clean(row.get("analysis_scope")),"empirical_object_type":_clean(row.get("empirical_object_type")),"empirical_object_id":_clean(row.get("empirical_object_id")),"source_table":_clean(row.get("source_table")),"source_row_hash":_clean(row.get("source_row_hash")),"question_id":_clean(row.get("question_id")),"var_code":_clean(row.get("var_code")),"position_field":_clean(row.get("position_field")),"position_value":_clean(row.get("position_value")),"response_value_raw":_clean(row.get("response_value_raw")),"response_value_normalized":_clean(row.get("response_value_normalized")),"response_label":_clean(row.get("response_label")),"normalized_response_label":_clean(row.get("normalized_response_label")),"response_family":_clean(row.get("response_family")),"response_topology":_clean(row.get("response_topology")),"response_direction":adjud["raw_response_direction"],"response_intensity":adjud["raw_response_intensity"],"response_intensity_status":adjud["raw_response_intensity_status"],"authority_intensity_semantics":adjud["authority_intensity_semantics"],"v551_signed_side":adjud["v551_signed_side"],"v551_signed_intensity":adjud["v551_signed_intensity"],"v551_projection_rule_id":adjud["v551_projection_rule_id"],"v551_projection_authority_hash":adjud["v551_projection_authority_hash"],"semantic_role":_clean(row.get("semantic_role")),"semantic_subrole":_clean(row.get("semantic_subrole")),"semantic_tags":_clean(row.get("semantic_tags")),"directionality_policy":_clean(row.get("directionality_policy")),"driver_id":_clean(row.get("driver_id")),"driver_facet_id":_clean(row.get("driver_facet_id")),"relation_axis_id":_clean(row.get("relation_axis_id")),"target_entity_id":_clean(row.get("target_entity_id")),"strata_relevance":_clean(row.get("strata_relevance")),"strata_path":_clean(row.get("strata_path")),"subject_position_signature":_clean(row.get("subject_position_signature")),"position_conditioning":_clean(row.get("position_conditioning")),"position_modifiers":_clean(row.get("position_modifiers")),"conditional_strata_weights":_clean(row.get("conditional_strata_weights")),"horizon_affordance":_clean(row.get("horizon_affordance")),"n_unweighted":int(_float(row.get("n_unweighted")) or 0),"n_respondents":int(_float(row.get("n_respondents"))) if _float(row.get("n_respondents")) is not None else None,"n_weighted":_float(row.get("n_weighted")),"pct_unweighted":_float(row.get("pct_unweighted")),"pct_weighted":_float(row.get("pct_weighted")),"weight_status":_clean(row.get("weight_status")),"support_status":_clean(row.get("support_status")),"confidence_tier":_clean(row.get("confidence_tier")),"response_semantics_contract_hash":adjud["response_semantics_contract_hash"],"question_use_contract_row_hash":adjud["question_use_contract_row_hash"],"question_use_contract_artifact_hash":adjud["question_use_contract_artifact_hash"],"producer_lineage_status":adjud["producer_lineage_status"],"evidence_basis":_clean(row.get("evidence_basis")) or "V551_DIRECT_RESPONSE_DISTRIBUTION","provenance_basis":_clean(row.get("provenance_basis")) or _hash({"source_row_hash":_clean(row.get("source_row_hash")),"run_id":_clean(row.get("run_id"))}),"schema_version":V551_SCHEMA_VERSION,"compiler_version":V551_COMPILER_VERSION}
    result["atom_id"]=_identity("v551atom__",{**result,"candidate_id":result["candidate_id"]},["candidate_id","empirical_distribution_id","response_value_normalized"]);result["measurement_contract_hash"]=_hash({k:result.get(k) for k in ["response_direction","response_intensity","v551_signed_side","v551_signed_intensity","response_semantics_contract_hash","v551_projection_authority_hash","n_unweighted","n_weighted"]});result["atom_contract_hash"]=_hash({k:result.get(k) for k in ATOM_COLUMNS if k!="atom_contract_hash"});return result

def build_v551_relation_evidence_atoms(bridge:pd.DataFrame,**_:Any)->tuple[pd.DataFrame,pd.DataFrame]:
    adjud=build_v551_directional_candidate_adjudication(bridge);candidate=build_v551_certification_candidate_bridge(bridge);by_id={_candidate_id(r):r for r in candidate.to_dict("records")};atoms=[_atom_from(by_id[a["candidate_id"]],a) for a in adjud.to_dict("records") if a["adjudication_outcome"]=="PROMOTABLE"];atom_df=pd.DataFrame(atoms,columns=ATOM_COLUMNS);nonpromotable=adjud.loc[~adjud["promotable"].map(_bool)].copy() if not adjud.empty else adjud.copy();return atom_df,nonpromotable

def build_v551_directional_distribution_coverage(adjudication:pd.DataFrame)->pd.DataFrame:
    if adjudication.empty:return pd.DataFrame(columns=COVERAGE_COLUMNS)
    rows=[]
    for dist,g in adjudication.groupby("empirical_distribution_id",dropna=False,sort=True):
        promo=g["adjudication_outcome"].eq("PROMOTABLE");non=~promo;neutral=g["v551_signed_side"].eq("neutral");u=pd.to_numeric(g["n_unweighted"],errors="coerce").fillna(0);w=pd.to_numeric(g["n_weighted"],errors="coerce");base=g.iloc[0];selected_u=float(u.sum());promo_u=float(u[promo].sum());non_u=float(u[non].sum());neutral_u=float(u[neutral].sum());selected_w=float(w.fillna(0).sum()) if w.notna().any() else None;promo_w=float(w[promo].fillna(0).sum()) if w.notna().any() else None;non_w=float(w[non].fillna(0).sum()) if w.notna().any() else None;neutral_w=float(w[neutral].fillna(0).sum()) if w.notna().any() else None
        rows.append({"run_id":base["run_id"],"empirical_distribution_id":dist,"source":base["source"],"source_family":base["source_family"],"canonical_wave":base["canonical_wave"],"country_code":base["country_code"],"analysis_scope":base["analysis_scope"],"source_table":base["source_table"],"question_id":base["question_id"],"var_code":base["var_code"],"position_field":base["position_field"],"position_value":base["position_value"],"applicable_candidate_count":len(g),"promotable_candidate_count":int(promo.sum()),"nonpromotable_candidate_count":int(non.sum()),"neutral_candidate_count":int(neutral.sum()),"selected_substantive_n_unweighted":selected_u,"promotable_n_unweighted":promo_u,"nonpromotable_n_unweighted":non_u,"neutral_n_unweighted":neutral_u,"selected_substantive_n_weighted":selected_w,"promotable_n_weighted":promo_w,"nonpromotable_n_weighted":non_w,"neutral_n_weighted":neutral_w,"selected_surface_status":"SELECTED_SUBSTANTIVE_SURFACE","directional_adjudication_status":"COMPLETE" if not non.any() else ("NO_PROMOTABLE" if not promo.any() else "PARTIAL_WITH_REPAIR_DEBT"),"candidate_count_conserved":len(g)==int(promo.sum()+non.sum()),"unweighted_mass_conserved":abs(selected_u-(promo_u+non_u))<1e-9,"weighted_mass_conserved":True if selected_w is None else abs(selected_w-((promo_w or 0)+(non_w or 0)))<1e-9,"schema_version":V551_SCHEMA_VERSION,"compiler_version":V551_COMPILER_VERSION})
    return pd.DataFrame(rows,columns=COVERAGE_COLUMNS)

def validate_v551_atom_contract(df:pd.DataFrame)->list[str]:
    issues=[];missing=[c for c in ATOM_COLUMNS if c not in df.columns]
    if missing:issues.append("missing_columns="+",".join(missing))
    if df.empty:return issues
    if not df["schema_version"].eq(V551_SCHEMA_VERSION).all():issues.append("incompatible_v551_schema_version")
    if any(c.startswith("v552_") or c=="pressure_evidence_class" for c in df.columns):issues.append("v552_state_leaked_into_v551_atom_contract")
    raw=pd.to_numeric(df["response_intensity"],errors="coerce");st=df["response_intensity_status"].astype(str)
    if ((st=="MISSING")&raw.notna()).any():issues.append("raw_intensity_status_mismatch")
    side=df["v551_signed_side"].astype(str);signed=pd.to_numeric(df["v551_signed_intensity"],errors="coerce")
    if (side.eq("neutral")&signed.ne(0)).any():issues.append("neutral_signed_nonzero")
    if (side.isin(["positive","negative"])&(signed.isna()|signed.lt(0))).any():issues.append("invalid_directional_signed_intensity")
    if df["candidate_id"].duplicated().any():issues.append("duplicate_promotable_candidate")
    return issues

def validate_v551_adjudication_contract(adjud:pd.DataFrame)->list[str]:
    issues=[];missing=[c for c in ADJUDICATION_COLUMNS if c not in adjud.columns]
    if missing:issues.append("missing_columns="+",".join(missing))
    if adjud.empty:return issues
    if adjud["candidate_id"].duplicated().any():issues.append("duplicate_candidate_id")
    if not adjud["adjudication_outcome"].isin({"PROMOTABLE","NONPROMOTABLE_REPAIRABLE","NOT_APPLICABLE"}).all():issues.append("invalid_adjudication_outcome")
    if not adjud["schema_version"].eq(V551_SCHEMA_VERSION).all():issues.append("incompatible_v551_schema_version")
    return issues

def validate_v551_coverage_contract(coverage:pd.DataFrame)->list[str]:
    issues=[];missing=[c for c in COVERAGE_COLUMNS if c not in coverage.columns]
    if missing:issues.append("missing_columns="+",".join(missing))
    if coverage.empty:return issues
    if not coverage["candidate_count_conserved"].map(_bool).all():issues.append("candidate_count_not_conserved")
    if not coverage["unweighted_mass_conserved"].map(_bool).all():issues.append("unweighted_mass_not_conserved")
    if not coverage["weighted_mass_conserved"].map(_bool).all():issues.append("weighted_mass_not_conserved")
    return issues

def build_v551_exclusion_summary(nonpromotable:pd.DataFrame)->pd.DataFrame:
    if nonpromotable.empty:return pd.DataFrame(columns=["adjudication_outcome","adjudication_reason","candidate_count"])
    return nonpromotable.groupby(["adjudication_outcome","adjudication_reason"],dropna=False).size().reset_index(name="candidate_count")
def build_v551_exclusion_samples(nonpromotable:pd.DataFrame,sample_size:int=3)->pd.DataFrame:return nonpromotable.groupby("adjudication_reason",dropna=False).head(sample_size).reset_index(drop=True) if not nonpromotable.empty else nonpromotable.copy()
def build_v551_pressure_component_audit(atoms:pd.DataFrame)->pd.DataFrame:return pd.DataFrame(columns=["compatibility_status"])
def build_v551_numeric_wrapper_audit(bridge:pd.DataFrame,run_id:str="")->pd.DataFrame:return pd.DataFrame(columns=["run_id","source_row_hash","diagnostic_status"])
def build_v551_relation_review_surface(bridge:pd.DataFrame,run_id:str="")->pd.DataFrame:
    adjud=build_v551_directional_candidate_adjudication(bridge);return adjud.loc[~adjud["promotable"].map(_bool)].copy()
def build_v551_blocked_signal_audit(bridge:pd.DataFrame,run_id:str="")->pd.DataFrame:return build_v551_relation_review_surface(bridge,run_id=run_id)
def build_v551_lineage_basis_audit(candidate_bridge:pd.DataFrame,atoms:pd.DataFrame,exclusion_audit:pd.DataFrame)->pd.DataFrame:return pd.DataFrame(columns=["candidate_id","producer_lineage_status"])
def build_v551_eligible_bridge_atom_coverage_audit(candidate_bridge:pd.DataFrame,atoms:pd.DataFrame,exclusion_audit:pd.DataFrame)->pd.DataFrame:
    atom_ids=set(atoms.get("candidate_id",pd.Series(dtype=str)).astype(str));out=candidate_bridge.copy();out["candidate_id"]=[_candidate_id(r) for r in out.to_dict("records")];out["coverage_status"]=out["candidate_id"].map(lambda x:"EMITTED_V551_ATOM" if x in atom_ids else "NONPROMOTABLE_DIRECTIONAL_CANDIDATE");return out
def summarize_v551_denominator_contract(atoms:pd.DataFrame)->dict[str,Any]:return {"atom_count":int(len(atoms)),"empirical_distribution_count":int(atoms["empirical_distribution_id"].nunique()) if "empirical_distribution_id" in atoms else 0}
