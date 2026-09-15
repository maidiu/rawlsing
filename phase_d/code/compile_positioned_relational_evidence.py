#!/usr/bin/env python3
"""Compile fail-closed Phase-D positioned-relational-evidence sidecars.

This compiler is deliberately additive. It does not mutate V550/V550J/V551/V551J
outputs or semantic authority. It scans a completed bounded scope output for
non-respondent empirical artifacts, preserves semantic authority independently,
and only marks a semantic relation OBSERVED when exact implementation identifiers
co-occur in a single empirical artifact row.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

PRIVACY_PATH_RE = re.compile(r"(respondent_substrate|respondent_membership|raw_response|raw_responses|\.env$|data\.parquet$)", re.I)
IMPL_RE = re.compile(r"question_impl\.[A-Za-z0-9_.:-]+")
EMPIRICAL_ID_COLUMNS = ["empirical_object_id","atom_id","pattern_id","joint_pattern_id","joint_configuration_id","family_id","bridge_id","question_id"]
SUPPORT_COLUMNS = ["n_unweighted","support_n","n_respondents","count"]
WEIGHTED_COLUMNS = ["weighted_n","weighted_count"]
ESS_COLUMNS = ["kish_ess","effective_n","effective_sample_size"]

EVIDENCE_COLUMNS = [
    "evidence_id","source_family","wave","country_code","relation_authority_id","rule_id","relation_type",
    "member_implementation_ids_json","semantic_relation_posture","empirical_link_id","empirical_lane",
    "empirical_cotravel_posture","respondent_universe_status","routing_status","association_mode","association_metric",
    "association_score","p_value","q_value","n_unweighted","weighted_n","kish_ess","design_grade",
    "position_context_status","position_signature","strata_context_status","strata_ids_json","horizon_id",
    "uncertainty_status","downstream_eligibility_json","inference_ceiling","prohibited_inference","provenance_refs_json"
]

@dataclass
class RowEvidence:
    path: str
    row_index: int
    impl_ids: set[str]
    empirical_id: str
    lane: str
    n_unweighted: int | None
    weighted_n: float | None
    kish_ess: float | None
    strata_ids: list[str]
    horizon_id: str | None


def _clean(v: Any) -> str:
    if v is None: return ""
    try:
        if pd.isna(v): return ""
    except Exception: pass
    s = str(v).strip()
    return "" if s.lower() in {"nan","none","null"} else s


def _json_list(value: Any) -> list[str]:
    s = _clean(value)
    if not s: return []
    try:
        x = json.loads(s)
        if isinstance(x, list): return [_clean(v) for v in x if _clean(v)]
    except Exception: pass
    return [m.group(0) for m in IMPL_RE.finditer(s)]


def _impls_from_row(row: pd.Series) -> set[str]:
    out: set[str] = set()
    for value in row.tolist():
        s = _clean(value)
        if not s: continue
        out.update(m.group(0) for m in IMPL_RE.finditer(s))
    return out


def _first_numeric(row: pd.Series, names: Iterable[str], kind=float):
    for name in names:
        if name not in row.index: continue
        s = _clean(row[name])
        if not s: continue
        try: return kind(float(s)) if kind is int else float(s)
        except Exception: continue
    return None


def _empirical_id(row: pd.Series, path: str, idx: int) -> str:
    for name in EMPIRICAL_ID_COLUMNS:
        if name in row.index and _clean(row[name]): return _clean(row[name])
    return f"artifact:{path}#row={idx}"


def _lane(path: str, columns: Iterable[str]) -> str:
    t = (path + " " + " ".join(columns)).lower()
    if "joint" in t or "pattern" in t: return "JOINT_RESPONSE_CONFIGURATION"
    if "cloud" in t or "cosignature" in t or "co_signature" in t: return "ATTITUDE_CLOUD"
    if "branch" in t or "recursive" in t: return "RECURSIVE_BRANCH"
    if "position" in t or "strata" in t: return "POSITION_DISTRIBUTION"
    return "DIRECT_RESPONSE"


def _read_frame(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv": return pd.read_csv(path, dtype=str, low_memory=False).fillna("")
    if path.suffix.lower() == ".parquet": return pd.read_parquet(path).fillna("")
    return pd.DataFrame()


def scan_scope(scope_root: Path) -> tuple[list[RowEvidence], dict[str, Any]]:
    rows: list[RowEvidence] = []
    manifest_text: list[str] = []
    position_seen = False; branch_seen = False; cloud_seen = False; joint_seen = False
    for path in sorted(scope_root.rglob("*")):
        if not path.is_file() or PRIVACY_PATH_RE.search(path.as_posix()): continue
        rel = path.relative_to(scope_root).as_posix()
        if path.suffix.lower() == ".json" and path.stat().st_size < 5_000_000:
            try: manifest_text.append(path.read_text(encoding="utf-8", errors="ignore"))
            except Exception: pass
        if path.suffix.lower() not in {".csv", ".parquet"}: continue
        try: df = _read_frame(path)
        except Exception: continue
        lane = _lane(rel, df.columns)
        position_seen |= lane == "POSITION_DISTRIBUTION"
        branch_seen |= lane == "RECURSIVE_BRANCH"
        cloud_seen |= lane == "ATTITUDE_CLOUD"
        joint_seen |= lane == "JOINT_RESPONSE_CONFIGURATION"
        for idx, row in df.iterrows():
            impls = _impls_from_row(row)
            if len(impls) < 1: continue
            strata = []
            for c in ["strata_id","stratum_id","strata_ids_json"]:
                if c in row.index:
                    if c.endswith("_json"): strata.extend(_json_list(row[c]))
                    elif _clean(row[c]): strata.append(_clean(row[c]))
            horizon = None
            for c in ["horizon_id","absolute_horizon_id"]:
                if c in row.index and _clean(row[c]): horizon = _clean(row[c]); break
            rows.append(RowEvidence(
                path=rel,row_index=int(idx),impl_ids=impls,empirical_id=_empirical_id(row,rel,int(idx)),lane=lane,
                n_unweighted=_first_numeric(row,SUPPORT_COLUMNS,int),weighted_n=_first_numeric(row,WEIGHTED_COLUMNS,float),
                kish_ess=_first_numeric(row,ESS_COLUMNS,float),strata_ids=sorted(set(strata)),horizon_id=horizon,
            ))
    text = "\n".join(manifest_text).lower()
    fused = ("prepared_required" in text and ("forbid_database_access" in text or "forbid-database-access" in text or '"database_access_forbidden": true' in text))
    return rows, {
        "fused_manifest_verified": fused,
        "position_seen": position_seen,
        "branch_seen": branch_seen,
        "cloud_seen": cloud_seen,
        "joint_seen": joint_seen,
    }


def _make_id(parts: Iterable[str]) -> str:
    h = hashlib.sha256("|".join(parts).encode()).hexdigest()[:20]
    return f"PRE-{h}"


def _best_match(member_ids: set[str], rows: list[RowEvidence]) -> RowEvidence | None:
    exact = [r for r in rows if member_ids and member_ids.issubset(r.impl_ids)]
    if exact: return max(exact, key=lambda r: (r.n_unweighted or 0, len(r.impl_ids)))
    return None


def _base_row(source: str, wave: str, country: str, fused: bool) -> dict[str, Any]:
    return {
        "source_family": source,"wave": wave,"country_code": country,"association_mode": "DIAGNOSTIC",
        "association_metric": "","association_score": "","p_value": "","q_value": "",
        "respondent_universe_status": "EXACT_SAME_RESPONDENT_UNIVERSE" if fused else "BLOCKED",
        "routing_status": "COMPATIBLE" if fused else "BLOCKED","uncertainty_status": "EXPLICIT",
        "inference_ceiling": "Measured same-respondent configuration evidence only; no causality or individual personality assignment.",
        "prohibited_inference": "Do not create/negate typed semantic relations; do not infer causality; do not assign group patterns to generated individuals.",
    }


def compile_scope(scope_root: Path, topology: pd.DataFrame, blocked: pd.DataFrame, source: str, wave: str, country: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    empirical_rows, scan = scan_scope(scope_root)
    base = _base_row(source,wave,country,scan["fused_manifest_verified"])
    out: list[dict[str, Any]] = []
    matched_empirical: set[tuple[str,int]] = set()

    pos = topology[(topology.source_family.astype(str)==source) & (topology.wave.astype(str)==wave)]
    for _, rel in pos.iterrows():
        members = set(_json_list(rel.get("member_implementation_ids_json","")))
        match = _best_match(members, empirical_rows)
        if match: matched_empirical.add((match.path,match.row_index))
        row = dict(base)
        row.update({
            "evidence_id": _make_id([source,wave,_clean(rel.get("authority_id")),match.empirical_id if match else "not-observed"]),
            "relation_authority_id": _clean(rel.get("authority_id")),"rule_id": _clean(rel.get("rule_id")),
            "relation_type": _clean(rel.get("relation_type")),"member_implementation_ids_json": json.dumps(sorted(members)),
            "semantic_relation_posture": "GOVERNED_POSITIVE","empirical_link_id": match.empirical_id if match else "",
            "empirical_lane": match.lane if match else "NONE","empirical_cotravel_posture": "OBSERVED" if match else "NOT_TESTED",
            "n_unweighted": match.n_unweighted if match else "","weighted_n": match.weighted_n if match else "",
            "kish_ess": match.kish_ess if match else "","design_grade": "KISH_WEIGHTED_APPROXIMATION" if match and match.kish_ess is not None else "UNWEIGHTED_DIAGNOSTIC_ONLY" if match else "NOT_APPLICABLE",
            "position_context_status": "OBSERVED" if scan["position_seen"] else "EMPTY_VALID","position_signature": "artifact-presence" if scan["position_seen"] else "",
            "strata_context_status": "PLACED" if match and match.strata_ids else "UNPLACED_GOVERNED" if scan["position_seen"] else "NOT_APPLICABLE",
            "strata_ids_json": json.dumps(match.strata_ids if match else []),"horizon_id": match.horizon_id if match and match.horizon_id else "",
            "downstream_eligibility_json": json.dumps(["APP_GATE_A_EVIDENCE","V551J_JOINT_REVIEW"] if match and match.lane=="JOINT_RESPONSE_CONFIGURATION" else ["APP_GATE_A_EVIDENCE"]),
            "provenance_refs_json": json.dumps([f"semantic:{_clean(rel.get('authority_id'))}"] + ([f"empirical:{match.path}#row={match.row_index}"] if match else ["empirical:not-exactly-linked"]))
        })
        out.append(row)

    blk = blocked[(blocked.source_family.astype(str)==source) & (blocked.active_wave.astype(str)==wave)]
    for _, rel in blk.iterrows():
        members = set(_json_list(rel.get("implementation_ids","")))
        match = _best_match(members, empirical_rows)
        if not match: continue
        matched_empirical.add((match.path,match.row_index))
        row = dict(base)
        row.update({
            "evidence_id": _make_id([source,wave,_clean(rel.get("candidate_id")),match.empirical_id]),"relation_authority_id": _clean(rel.get("candidate_id")),
            "rule_id": _clean(rel.get("rule_id")),"relation_type": "","member_implementation_ids_json": json.dumps(sorted(members)),
            "semantic_relation_posture": "BLOCKED_TYPED_RELATION","empirical_link_id": match.empirical_id,"empirical_lane": match.lane,
            "empirical_cotravel_posture": "OBSERVED","n_unweighted": match.n_unweighted or "","weighted_n": match.weighted_n or "","kish_ess": match.kish_ess or "",
            "design_grade": "KISH_WEIGHTED_APPROXIMATION" if match.kish_ess is not None else "UNWEIGHTED_DIAGNOSTIC_ONLY",
            "position_context_status": "OBSERVED" if scan["position_seen"] else "EMPTY_VALID","position_signature": "artifact-presence" if scan["position_seen"] else "",
            "strata_context_status": "PLACED" if match.strata_ids else "UNPLACED_GOVERNED" if scan["position_seen"] else "NOT_APPLICABLE",
            "strata_ids_json": json.dumps(match.strata_ids),"horizon_id": match.horizon_id or "","downstream_eligibility_json": json.dumps(["APP_GATE_A_EVIDENCE"]),
            "provenance_refs_json": json.dumps([f"semantic-block:{_clean(rel.get('candidate_id'))}",f"empirical:{match.path}#row={match.row_index}"])
        })
        out.append(row)

    for er in empirical_rows:
        key=(er.path,er.row_index)
        if key in matched_empirical or len(er.impl_ids) < 2: continue
        row=dict(base)
        row.update({
            "evidence_id": _make_id([source,wave,"empirical-only",er.empirical_id]),"relation_authority_id":"","rule_id":"","relation_type":"",
            "member_implementation_ids_json":json.dumps(sorted(er.impl_ids)),"semantic_relation_posture":"NO_GOVERNED_TYPED_RELATION",
            "empirical_link_id":er.empirical_id,"empirical_lane":er.lane,"empirical_cotravel_posture":"OBSERVED",
            "n_unweighted":er.n_unweighted or "","weighted_n":er.weighted_n or "","kish_ess":er.kish_ess or "",
            "design_grade":"KISH_WEIGHTED_APPROXIMATION" if er.kish_ess is not None else "UNWEIGHTED_DIAGNOSTIC_ONLY",
            "position_context_status":"OBSERVED" if scan["position_seen"] else "EMPTY_VALID","position_signature":"artifact-presence" if scan["position_seen"] else "",
            "strata_context_status":"PLACED" if er.strata_ids else "UNPLACED_GOVERNED" if scan["position_seen"] else "NOT_APPLICABLE",
            "strata_ids_json":json.dumps(er.strata_ids),"horizon_id":er.horizon_id or "","downstream_eligibility_json":json.dumps(["APP_GATE_A_EVIDENCE"]),
            "provenance_refs_json":json.dumps([f"empirical:{er.path}#row={er.row_index}"])
        })
        out.append(row)

    df=pd.DataFrame(out)
    for c in EVIDENCE_COLUMNS:
        if c not in df.columns: df[c]=""
    return df[EVIDENCE_COLUMNS], scan


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--scope-root",type=Path,required=True); ap.add_argument("--source-family",required=True); ap.add_argument("--wave",required=True); ap.add_argument("--country-code",required=True)
    ap.add_argument("--topology",type=Path,required=True); ap.add_argument("--blocked-ledger",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--scan-report",type=Path,default=None)
    a=ap.parse_args()
    topology=pd.read_csv(a.topology,dtype=str).fillna(""); blocked=pd.read_csv(a.blocked_ledger,dtype=str).fillna("")
    evidence,scan=compile_scope(a.scope_root,topology,blocked,a.source_family,a.wave,a.country_code)
    a.output.parent.mkdir(parents=True,exist_ok=True); evidence.to_csv(a.output,index=False)
    if a.scan_report:
        a.scan_report.parent.mkdir(parents=True,exist_ok=True); a.scan_report.write_text(json.dumps(scan,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","evidence_rows":len(evidence),**scan},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
