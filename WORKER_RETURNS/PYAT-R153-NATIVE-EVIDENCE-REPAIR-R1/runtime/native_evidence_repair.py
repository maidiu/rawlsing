"""R153 repair of R152 WVS native-evidence promotion defects.

No survey file is opened. This adapter consumes R151 records and the exact WVS7
source-specific package; unsupported constructor premises are honestly held.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "PYAT_R153_NATIVE_EVIDENCE_REPAIR@1"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
R151_BASE = "WORKER_RETURNS/PYAT-R151-GROUNDED-NATIVE-OCCURRENCES-R1/records"
WVS_PACKAGE_PATH = REPO_ROOT / "rawlsing_next" / "runtime" / "ee_p2x" / "02_WVS7_P2F2_RUNTIME_PACKAGE.json"


class EvidenceRepairRefusal(ValueError):
    pass


def _canonical(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(v: Any) -> str:
    return hashlib.sha256(_canonical(v).encode()).hexdigest()


def _git_json(path: str) -> Any:
    done = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO_ROOT,
                          capture_output=True, check=False)
    if done.returncode != 0:
        raise EvidenceRepairRefusal(f"GIT_OBJECT_UNAVAILABLE:{path}")
    return json.loads(done.stdout.decode())


def load_inputs() -> dict[str, Any]:
    records = {f"SRC{n:02d}": _git_json(f"{R151_BASE}/SRC{n:02d}_GROUNDED_NATIVE_INPUT.json")
               for n in range(1, 36)}
    r148_summary = _git_json("WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/records/SUMMARY.json")
    wvs = json.loads(WVS_PACKAGE_PATH.read_text(encoding="utf-8"))
    return {"records": records, "r148_summary": r148_summary, "wvs": wvs,
            "wvs_package_sha256": hashlib.sha256(WVS_PACKAGE_PATH.read_bytes()).hexdigest()}


def _wvs_evidence(wvs: Mapping[str, Any]) -> dict[str, Any]:
    if wvs.get("source_sha256") != "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d":
        raise EvidenceRepairRefusal("WVS7_SOURCE_SCOPE_MISMATCH")
    topology = None
    risk = None
    source_auth = None
    routing_auth = None
    for doc in wvs.get("authority_documents", []):
        fields = doc.get("semantic_fields", {})
        if fields.get("authority_kind") == "SOURCE_SEMANTICS_TOPOLOGY":
            source_auth = fields.get("authority_id")
        if fields.get("authority_kind") == "ROUTING_RISK_SET":
            routing_auth = fields.get("authority_id")
    for doc in wvs.get("query_documents", []):
        fields = doc.get("semantic_fields", {})
        comps = (fields.get("target_arity_and_topology") or {}).get("components") or []
        for comp in comps:
            if comp.get("topology"):
                assert topology in (None, comp["topology"])
                topology = comp["topology"]
        grain = fields.get("requested_output_grain") or {}
        if grain.get("risk_set_type"):
            pass
    def walk(x):
        nonlocal risk
        if isinstance(x, dict):
            if x.get("kind") == "WVS7RiskSetBinding@1.0.0" and risk is None:
                risk = {"object_id": x["object_id"], "content_hash": x["content_hash"]}
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(wvs)
    if topology is None or risk is None or not source_auth or not routing_auth:
        raise EvidenceRepairRefusal("WVS7_EVIDENCE_INCOMPLETE")
    return {
        "source_sha256": wvs["source_sha256"], "topology": topology,
        "risk_ref": risk, "source_auth_id": source_auth, "routing_auth_id": routing_auth,
        "unit": None, "forms": None, "administration": None,
        "evidence_scope": "EXACT_WVS7_SOURCE_SPECIFIC_RUNTIME_PACKAGE",
        "package_sha256": hashlib.sha256(WVS_PACKAGE_PATH.read_bytes()).hexdigest(),
    }


def repair_source(record: Mapping[str, Any], evidence: Mapping[str, Any]) -> dict[str, Any]:
    rec = json.loads(_canonical(record))
    if rec["source_id"] != "SRC35":
        rec["schema"] = SCHEMA
        rec["evidence_resolution"] = dict(rec["evidence_resolution"])
        rec["evidence_resolution"]["native_objects"] = None
        rec["evidence_resolution"]["native_occurrence_count"] = 0
        rec["evidence_resolution"]["native_source_rule_count"] = 0
        rec["evidence_resolution"]["source_inventory_count"] = 0
        rec["evidence_resolution"]["held_native_reason"] = "R151 partial fields preserved; no new native object promoted"
        rec["binding_hash"] = _sha({k: v for k, v in rec.items() if k != "binding_hash"})
        return rec
    held = []
    for item in rec["pending_native_occurrences"]:
        if item["source_variable_code"] not in {"Q291G5", "Q291P5"}:
            item["native_occurrence_constructed"] = False
            item["native_source_rule_constructed"] = False
            held.append({"source_variable_code": item["source_variable_code"],
                         "reason": "R151_WVS_OBJECT_NOT_CONSTRUCTED"})
            continue
        item["native_occurrence_constructed"] = False
        item["native_source_rule_constructed"] = False
        item["unit_status"] = "PENDING_EXACT_WVS7_SOURCE_UNIT"
        item.pop("unit", None)
        item.pop("unit_evidence", None)
        item["topology_status"] = "EXACT_WVS7_SOURCE_TOPOLOGY"
        item["topology"] = evidence["topology"]
        item["risk_set_status"] = "EXACT_WVS7_RISK_SET"
        item["risk_set_ref"] = evidence["risk_ref"]["object_id"]
        item["forms_status"] = "PENDING_EXACT_WVS7_SOURCE_FORM"
        item["administration_status"] = "PENDING_EXACT_WVS7_SOURCE_ADMINISTRATION"
        item["resolved_fields"] = ["domain", "topology", "risk_set"]
        item["unresolved_fields"] = ["unit", "form", "administration"]
        item["field_owner"] = {
            "unit": "WVS7_SOURCE_UNIT_AUTHORITY_OWNER",
            "form": "WVS7_SOURCE_FORM_AUTHORITY_OWNER",
            "administration": "WVS7_SOURCE_ADMINISTRATION_AUTHORITY_OWNER",
        }
        item["native_occurrence_status"] = "HELD_PENDING_UNIT_FORM_ADMINISTRATION"
        held.append({"source_variable_code": item["source_variable_code"],
                     "reason": "PENDING_UNIT_FORM_ADMINISTRATION",
                     "resolved": ["domain", "topology", "risk_set"],
                     "unresolved": ["unit", "form", "administration"]})
    rec["schema"] = SCHEMA
    rec["evidence_resolution"] = dict(rec["evidence_resolution"])
    rec["evidence_resolution"]["native_objects"] = None
    rec["evidence_resolution"]["native_occurrence_count"] = 0
    rec["evidence_resolution"]["native_source_rule_count"] = 0
    rec["evidence_resolution"]["source_inventory_count"] = 0
    rec["evidence_resolution"]["held_native_objects"] = held
    rec["evidence_resolution"]["wvs_evidence"] = evidence
    rec["evidence_resolution"]["planner_invocation_status"] = "NOT_INVOKED__WVS_UNIT_FORM_ADMINISTRATION_PENDING"
    rec["already_grounded"] = [x for x in rec.get("already_grounded", []) if "NativeSourceIdentity" not in x]
    rec["already_grounded"].append("WVS7 exact typed domain/topology/risk-set evidence")
    rec["indispensable_unbound"] = list(dict.fromkeys(
        rec.get("indispensable_unbound", []) + ["WVS7 source-specific unit/form/administration"]))
    rec["next_native_workload_call"] = dict(rec.get("next_native_workload_call", {}))
    rec["next_native_workload_call"]["status"] = "UNSIGNED_PLANNING_ONLY__WVS_RULE_ADMINISTRATION_UNKNOWN"
    rec["binding_hash"] = _sha({k: v for k, v in rec.items() if k != "binding_hash"})
    return rec


def build_all():
    inputs = load_inputs()
    evidence = _wvs_evidence(inputs["wvs"])
    out = {sid: repair_source(rec, evidence) for sid, rec in sorted(inputs["records"].items())}
    total_items = sum(len(r["pending_native_occurrences"]) for r in out.values())
    if total_items != 4493:
        raise EvidenceRepairRefusal("PREPARATION_ITEM_DENOMINATOR_MISMATCH")
    summary = {
        "schema": "PYAT_R153_NATIVE_EVIDENCE_REPAIR_SUMMARY@1",
        "status": "R152_WVS_PROMOTION_REPAIRED__UNKNOWN_ADMINISTRATION_HELD__SUPPORTED_FIELDS_PRESERVED",
        "source_count": 35,
        "b49_item_records": 4460,
        "typed_surface_only_items": 33,
        "preparation_items": total_items,
        "codebook_rows": inputs["r148_summary"]["current_metadata_rows"],
        "typed_surfaces_consumed": 38,
        "context_items_retained": sum(len(r["conditioner_context_items"]) for r in out.values()),
        "unmatched_relation_ids": sum(len(r["unmatched_relation_ids"]) for r in out.values()),
        "native_occurrences_constructed": 0,
        "native_source_rules_constructed": 0,
        "source_inventories_constructed": 0,
        "native_objects_held": 1,
        "held_wvs_occurrences": 2,
        "held_wvs_native_source_rules": 2,
        "held_wvs_source_inventories": 1,
        "wvs_evidence": evidence,
        "current_source_grants": 0,
        "survey_files_touched": 0,
        "native_execution_authorized": False,
        "limits": ["no default form or administered promotion", "no source read or U/Epre", "partial documentary inputs only"],
    }
    return {"summary": summary, "records": out}


def write_records(result, out_root=RETURN_ROOT):
    root = Path(out_root); recdir = root / "records"; itemsdir = recdir / "ITEMS"
    itemsdir.mkdir(parents=True, exist_ok=True)
    for sid, rec in sorted(result["records"].items()):
        (recdir / f"{sid}_R153_NATIVE_INPUT.json").write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with (itemsdir / f"{sid}.jsonl").open("w", encoding="utf-8") as h:
            for item in rec["pending_native_occurrences"]:
                h.write(_canonical(item) + "\n")
    (recdir / "SUMMARY.json").write_text(json.dumps(result["summary"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (recdir / "ALL35_REPAIR_ACCOUNTING.jsonl").open("w", encoding="utf-8") as h:
        for sid, rec in sorted(result["records"].items()):
            h.write(_canonical({
                "source_id": sid,
                "b49_item_count": rec.get("b49_item_count"),
                "typed_surface_only_count": rec.get("typed_surface_only_count"),
                "preparation_items": len(rec["pending_native_occurrences"]),
                "current_unresolved": rec.get("current_unresolved"),
                "native_occurrence_count": rec["evidence_resolution"]["native_occurrence_count"],
                "native_source_rule_count": rec["evidence_resolution"]["native_source_rule_count"],
                "source_inventory_count": rec["evidence_resolution"]["source_inventory_count"],
                "held_native_objects": rec["evidence_resolution"].get("held_native_objects", []),
                "binding_hash": rec["binding_hash"],
            }) + "\n")
