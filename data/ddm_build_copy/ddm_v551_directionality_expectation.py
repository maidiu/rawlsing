#!/usr/bin/env python3
"""V551 applicability-denominator and raw directional stamp coverage."""
from __future__ import annotations
from typing import Any
import pandas as pd

APPLICABLE_BY_AUTHORITY="APPLICABLE_BY_AUTHORITY"
APPROVED_DIRECT_RELATION_SOURCE_TABLES={"answer_distribution","country_answer_distribution"}
CERTIFIED_RESPONSE_DIRECTIONS={"agree","disagree","graded","intermediate","negative","neutral","oppose","positive","support"}
AUDIT_COLUMNS=["source","source_family","wave","canonical_wave","country_code","question_id","var_code","position_field","position_value","source_table","response_value_raw","response_value_normalized","response_label","source_row_hash","directional_applicability_status","directionality_authority_status","response_option_map_matched","response_direction","response_intensity","directionality_stamp_status","directionality_stamp_failure_reason"]

def _clean(v:Any)->str:
    if v is None:return ""
    try:
        if pd.isna(v):return ""
    except Exception:pass
    s=str(v).strip();return "" if s.lower() in {"nan","none","null"} else s

def _bool(v:Any)->bool:return _clean(v).lower() in {"1","true","t","yes","y","on"} if not isinstance(v,bool) else v

def _float(v:Any):
    try:
        if v is None or pd.isna(v):return None
        return float(v)
    except Exception:return None

def build_v551_directionality_expected_bridge(bridge:pd.DataFrame)->pd.DataFrame:
    required={"directional_applicability_status","bridge_evidence_lane","source_table","is_substantive","is_missing","is_special"}
    missing=sorted(required-set(bridge.columns))
    if missing: raise ValueError("BLOCKED_V551_MISSING_DIRECTIONAL_EXPECTATION_CONTRACT:"+",".join(missing))
    if bridge.empty:return bridge.copy()
    mask=(bridge.directional_applicability_status.fillna("").astype(str).str.upper().eq(APPLICABLE_BY_AUTHORITY)&bridge.bridge_evidence_lane.fillna("").astype(str).eq("direct_relation_response")&bridge.source_table.fillna("").astype(str).isin(APPROVED_DIRECT_RELATION_SOURCE_TABLES)&bridge.is_substantive.map(_bool)&~bridge.is_missing.map(_bool)&~bridge.is_special.map(_bool))
    out=bridge.loc[mask].copy().reset_index(drop=True);out["v551_directionality_expected"]=True;return out

def build_v551_directionality_stamp_audit(bridge:pd.DataFrame)->pd.DataFrame:
    expected=build_v551_directionality_expected_bridge(bridge)
    required={"response_option_map_matched","response_direction","response_intensity"};missing=sorted(required-set(expected.columns))
    if missing:raise ValueError("BLOCKED_V551_MISSING_DIRECTIONAL_STAMP_CONTRACT:"+",".join(missing))
    rows=[]
    for r in expected.to_dict("records"):
        failures=[]; matched=_bool(r.get("response_option_map_matched")); direction=_clean(r.get("response_direction")).lower(); intensity=_float(r.get("response_intensity"))
        if not matched:failures.append("response_option_map_unmatched")
        if direction not in CERTIFIED_RESPONSE_DIRECTIONS:failures.append("missing_certified_response_direction")
        if direction!="neutral" and intensity is None:failures.append("missing_response_intensity")
        rows.append({**{c:_clean(r.get(c)) for c in AUDIT_COLUMNS if c not in {"response_option_map_matched","response_intensity","directionality_stamp_status","directionality_stamp_failure_reason"}},"response_option_map_matched":matched,"response_intensity":intensity,"directionality_stamp_status":"STAMPED" if not failures else "MISSING_OR_INCOMPLETE_STAMP","directionality_stamp_failure_reason":"|".join(failures)})
    return pd.DataFrame(rows,columns=AUDIT_COLUMNS)

def summarize_v551_directionality_stamp_coverage(audit:pd.DataFrame)->dict[str,Any]:
    n=len(audit);stamped=0 if audit.empty else int(audit.directionality_stamp_status.eq("STAMPED").sum());missing=n-stamped
    return {"directionality_expected_rows":n,"directionality_stamped_rows":stamped,"directionality_missing_stamp_rows":missing,"directionality_stamp_coverage":1.0 if n==0 else stamped/n,"directionality_stamp_coverage_complete":missing==0}
