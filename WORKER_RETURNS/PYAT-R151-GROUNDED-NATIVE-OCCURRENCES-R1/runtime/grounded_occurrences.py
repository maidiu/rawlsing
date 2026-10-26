"""R151 evidence-aware resolution over R150 B49 item records.

Consumes exact typed surfaces and existing source-specific native metadata where
scope matches. It reads no survey file and creates no current grant/U/Epre.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule
from rawlsing_next.universal_grammar.types import (
    ADMINISTRATION_UNKNOWN, Occurrence, OccurrenceKey, SourceInventory,
)

SCHEMA = "PYAT_R151_GROUNDED_NATIVE_OCCURRENCE@1"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
R150_BASE = "WORKER_RETURNS/PYAT-R150-SCIENTIFIC-NATIVE-INPUT-R1/records"
R150_INPUTS = REPO_ROOT / ".r61" / "r150-scientific-native-input" / "inputs"
R151_INPUTS = REPO_ROOT / ".r61" / "r151-grounded-native-occurrences" / "inputs"
WVS_PACKAGE = REPO_ROOT / "rawlsing_next" / "runtime" / "ee_p2x" / "02_WVS7_P2F2_RUNTIME_PACKAGE.json"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _git_json(path: str) -> Any:
    completed = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO_ROOT,
                               capture_output=True, check=False)
    if completed.returncode != 0:
        raise ValueError(f"GIT_OBJECT_UNAVAILABLE:{path}")
    return json.loads(completed.stdout.decode("utf-8"))


def _r150_records() -> dict[str, Any]:
    return {f"SRC{n:02d}": _git_json(f"{R150_BASE}/SRC{n:02d}_SCIENTIFIC_NATIVE_INPUT.json")
            for n in range(1, 36)}


def _numeric_source_id(source_id: str) -> str:
    return str(int(source_id[3:]))


def _r148_rows(source_id: str) -> dict[str, dict[str, Any]]:
    rec = _git_json(f"WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/records/{source_id}_CURRENT_METADATA_PREPARATION.json")
    path = rec["current_metadata"]["row_accounting_path"]
    path = str(path).replace("/records/records/", "/records/")
    if not path.startswith("WORKER_RETURNS/"):
        if path.startswith("records/ROW_ACCOUNTING/"):
            path = f"WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/{path}"
        else:
            path = f"WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/{path}"
    completed = subprocess.run(["git", "show", f"HEAD:{path}"], cwd=REPO_ROOT,
                               capture_output=True, check=False)
    if completed.returncode != 0:
        return {}
    rows = [json.loads(line) for line in completed.stdout.decode("utf-8").splitlines() if line]
    return {row.get("var_name") or row.get("raw_row", {}).get("var_name"): row for row in rows}


def _typed_surface_map() -> dict[tuple[str, str], dict[str, Any]]:
    corpus = json.loads((R150_INPUTS / "source_authority_corpus.json").read_text(encoding="utf-8"))
    out = {}
    for surface in corpus.get("typed_surfaces", []):
        sid = f"SRC{int(surface['source_id']):02d}"
        try:
            domain = json.loads(surface.get("rule_native_domain_json") or "null")
        except json.JSONDecodeError:
            domain = None
        out[(sid, surface["variable_name"])] = {**surface, "parsed_domain": domain}
    if len(out) != 38:
        raise ValueError("TYPED_SURFACE_DENOMINATOR_MISMATCH")
    return out


def _raw_codebook_domain(item: Mapping[str, Any]) -> list[Any]:
    text = item.get("response_options_all") or ""
    values = []
    for match in re.finditer(r"(?<!\w)(-?\d+)\s*=", str(text)):
        try:
            values.append(int(match.group(1)))
        except ValueError:
            values.append(match.group(1))
    return sorted(set(values))


def _wvs_package() -> dict[str, Any]:
    doc = json.loads(WVS_PACKAGE.read_text(encoding="utf-8"))
    if doc.get("source_sha256") != "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d":
        raise ValueError("WVS7_PACKAGE_SOURCE_MISMATCH")
    risk = None
    source_auth = None
    routing_auth = None
    for obj in doc.get("authority_documents", []):
        fields = obj.get("semantic_fields", {})
        kind = fields.get("authority_kind")
        if kind == "SOURCE_SEMANTICS_TOPOLOGY":
            source_auth = fields.get("authority_id")
        if kind == "ROUTING_RISK_SET":
            routing_auth = fields.get("authority_id")
    # The package's predicate/query documents bind the exact risk set.
    def walk(x):
        nonlocal risk
        if isinstance(x, dict):
            if x.get("kind") == "WVS7RiskSetBinding@1.0.0" and risk is None:
                risk = ExactRef(x["kind"], x["object_id"], x["content_hash"])
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(doc)
    if risk is None or not source_auth or not routing_auth:
        raise ValueError("WVS7_PACKAGE_RISK_OR_AUTH_MISSING")
    return {
        "risk_ref": risk, "source_auth_id": source_auth, "routing_auth_id": routing_auth,
        "topology": "SCALAR_SINGULAR",
        "unit_law": "SOURCE_ROW_IDENTITY__EXACT_SAME_WVS7_RECORD",
    }


def _wvs_surfaces(typed: Mapping[tuple[str, str], dict[str, Any]], pkg: Mapping[str, Any], rows: Mapping[str, dict[str, Any]]):
    from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import Q0_REF, Q1_REF
    qrefs = {"Q291G5": Q0_REF, "Q291P5": Q1_REF}
    out = {}
    for var in ("Q291G5", "Q291P5"):
        surface = typed[("SRC35", var)]
        row = rows.get(var, {})
        raw = row.get("raw_row", {})
        domain = tuple(surface["parsed_domain"])
        occ = Occurrence(
            key=OccurrenceKey(var), label=raw.get("question_text") or var,
            unit=pkg["unit_law"], topology=pkg["topology"],
            forms=("DEFAULT_FORM",), domain=domain,
            target_role=None, conditioner_role=None,
            administration=ADMINISTRATION_UNKNOWN,
            route_state="ROUTED_APPLICABLE_RISK_SET", scope="WVS7_W7_SOURCE_LOCAL",
            risk_set_refs=(pkg["risk_ref"].key,),
        )
        rule = NativeSourceRule(
            implementation_id=qrefs[var].object_id, source_variable_code=var,
            unit=pkg["unit_law"], administered=True,
            semantic_direction="NOT_CERTIFIED", value_aliases={},
        )
        item = {
            "schema": "PYAT_R151_PENDING_NATIVE_OCCURRENCE@1",
            "source_id": "SRC35",
            "implementation_id": qrefs[var].object_id,
            "source_variable_code": var,
            "p2_row": None,
            "p2_evidence_id": None,
            "exact_identity_sha256": surface.get("representation_authority") or _sha(surface),
            "overlay_evidence_ids": [],
            "disposition": "SOURCE_SPECIFIC_TYPED_SURFACE_RESPONSE",
            "binding_grade": "SOURCE_SPECIFIC_CURRENT_RUNTIME_PACKAGE__NOT_CURRENT_SOURCE_GRANT",
            "semantic_direction": "NOT_CERTIFIED",
            "directional_certification_status": "NOT_CERTIFIED",
            "current_directional_atom_eligible": False,
            "routing_status": "ROUTED_APPLICABLE_RISK_SET",
            "response_binding_status": "bound_exact_wvs7_response_binding",
            "relation_evidence_id": None,
            "relation_scope": "NO_RELATION_EVIDENCE",
            "compiler_status": "SOURCE_SPECIFIC_TYPED_SURFACE_ONLY",
            "compiler_reason": "NO_B49_ITEM_RECORD__SOURCE_SPECIFIC_WVS7_RUNTIME_SURFACE",
            "codebook_join_status": "EXACT_CODEBOOK_VAR_JOIN" if row else "CODEBOOK_VARIABLE_NOT_FOUND",
            "codebook_collision": None,
            "codebook_row_hash": row.get("row_hash"),
            "codebook_var_name": var,
            "question_text": raw.get("question_text"),
            "response_options_substantive": raw.get("response_options_substantive"),
            "response_options_special": raw.get("response_options_special"),
            "value_labels_count": raw.get("value_labels_count"),
            "measure": raw.get("measure"),
            "storage_type": raw.get("storage_type"),
            "domain_values": list(domain),
            "domain_status": "EXACT_TYPED_SURFACE_DOMAIN",
            "typed_surface_id": surface["surface_id"],
            "surface_kind": surface["surface_kind"],
            "representation_authority": surface["representation_authority"],
            "ordinal": surface.get("ordinal"),
            "typed_surface_consumed": True,
            "unit": pkg["unit_law"],
            "unit_status": "EXACT_WVS7_RESPONDENT_ROW_UNIT",
            "unit_evidence": "WVS7_PACKAGE_RESPONDENT_IDENTITY_LAW",
            "topology": pkg["topology"],
            "topology_status": "EXACT_WVS7_SOURCE_TOPOLOGY",
            "risk_set_ref": pkg["risk_ref"].key,
            "risk_set_status": "EXACT_WVS7_RISK_SET",
            "resolved_fields": ["domain", "unit", "topology", "risk_set"],
            "unresolved_fields": [],
            "field_owner": {},
            "native_occurrence_constructed": True,
            "native_occurrence_status": "CONSTRUCTED_EXACT_GROUNDED_OCCURRENCE",
            "native_source_rule_constructed": True,
            "conditioning_context_retained": False,
            "retained": True,
            "scientific_role": "TARGET_ROLE_UNASSIGNED__SOURCE_SPECIFIC_RESPONSE_REPRESENTATION_ONLY",
            "current_acceptance_status": "NOT_ISSUED__SOURCE_SPECIFIC_RUNTIME_EVIDENCE_ONLY",
        }
        out[var] = {"occurrence": occ, "rule": rule, "surface": surface, "item": item, "domain": domain}
    inventory = SourceInventory(
        inventory_id=f"R151-WVS7-GROUNDED-SUBSET-{pkg['risk_ref'].content_hash[:12]}",
        source_id="35", wave="W7", edition="W7",
        source_sha256="2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",
        scope="WVS7_SOURCE_LOCAL_DOCUMENTARY_SUBSET",
        occurrences=tuple(v["occurrence"] for v in out.values()),
        measure_plans=(), risk_set_refs=(pkg["risk_ref"].key,),
        unit_transforms=(), state_map={},
        authority_refs=(pkg["source_auth_id"], pkg["routing_auth_id"]),
        current_selection=None, inventory_complete=False,
        inventory_gaps=("GROUNDED_2_OF_613_WVS7_ITEMS", "CURRENT_SOURCE_GRANT_AND_FRONTIER_ROLES_PENDING"),
        unresolved=("REMAINING_611_ITEMS_PENDING_ITEM_UNIT_TOPOLOGY_DOMAIN_RISK",),
        dataset_id="WVS_W7", instrument_ref="WVS Wave 7",
    )
    return out, inventory


def _typed_only_item(source_id: str, surface: Mapping[str, Any], rows: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    var = surface["variable_name"]
    row = rows.get(var, {})
    raw = row.get("raw_row", {})
    domain = surface.get("parsed_domain")
    resolved = []
    if domain is not None:
        domain_values = list(domain)
        domain_status = ("EXACT_TYPED_SURFACE_DOMAIN" if domain_values
                         else "EXACT_TYPED_SURFACE_REPRESENTATION__DOMAIN_EMPTY")
        resolved.append("domain")
    else:
        domain_values = _raw_codebook_domain({"response_options_all": raw.get("response_options_all")})
        domain_status = ("CODEBOOK_NATIVE_OPTION_VALUES__TYPED_DECODE_PENDING"
                         if domain_values else "PENDING_EXACT_TYPED_DOMAIN")
    return {
        "schema": "PYAT_R151_PENDING_NATIVE_OCCURRENCE@1",
        "source_id": source_id,
        "implementation_id": surface["surface_id"],
        "source_variable_code": var,
        "p2_row": None, "p2_evidence_id": None,
        "exact_identity_sha256": surface.get("representation_authority") or _sha(surface),
        "overlay_evidence_ids": [],
        "disposition": surface["surface_kind"],
        "binding_grade": surface["surface_kind"],
        "semantic_direction": "NOT_CERTIFIED",
        "directional_certification_status": "NOT_CERTIFIED",
        "current_directional_atom_eligible": False,
        "routing_status": "TYPED_SURFACE_REPRESENTATION_ONLY",
        "response_binding_status": "TYPED_SURFACE_REPRESENTATION_ONLY",
        "relation_evidence_id": None, "relation_scope": "NO_RELATION_EVIDENCE",
        "compiler_status": "TYPED_SURFACE_ONLY",
        "compiler_reason": "NO_B49_ITEM_RECORD__TYPED_SURFACE_REPRESENTATION_EVIDENCE",
        "codebook_join_status": "EXACT_CODEBOOK_VAR_JOIN" if row else "CODEBOOK_VARIABLE_NOT_FOUND",
        "codebook_collision": None,
        "codebook_row_hash": row.get("row_hash"), "codebook_var_name": var,
        "question_text": raw.get("question_text"),
        "response_options_substantive": raw.get("response_options_substantive"),
        "response_options_special": raw.get("response_options_special"),
        "value_labels_count": raw.get("value_labels_count"),
        "measure": raw.get("measure"), "storage_type": raw.get("storage_type"),
        "domain_values": domain_values, "domain_status": domain_status,
        "typed_surface_id": surface["surface_id"], "surface_kind": surface["surface_kind"],
        "representation_authority": surface["representation_authority"],
        "ordinal": surface.get("ordinal"), "typed_surface_consumed": True,
        "unit_status": "PENDING_EXACT_ITEM_UNIT",
        "topology_status": "PENDING_EXACT_ITEM_TOPOLOGY",
        "risk_set_status": "PENDING_EXACT_RISK_SET",
        "resolved_fields": sorted(set(resolved)),
        "unresolved_fields": ["unit", "topology", "risk_set"],
        "field_owner": {"unit": "SOURCE_ITEM_UNIT_AUTHORITY_OWNER",
                        "topology": "SOURCE_TOPOLOGY_AUTHORITY_OWNER",
                        "risk_set": "SOURCE_RISK_SET_AUTHORITY_OWNER"},
        "native_occurrence_constructed": False,
        "native_occurrence_status": "PENDING_EXACT_FIELDS",
        "native_source_rule_constructed": False,
        "conditioning_context_retained": False, "retained": True,
        "scientific_role": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        "current_acceptance_status": "NOT_ISSUED__TYPED_SURFACE_EVIDENCE_ONLY",
    }


def resolve_source(source_id: str, base: Mapping[str, Any], typed: Mapping[tuple[str, str], dict[str, Any]], wvs=None, wvs_rows=None, typed_only=()):
    items = []
    b49_item_count = len(base["pending_native_occurrences"])
    resolved_counts = Counter()
    for item in base["pending_native_occurrences"]:
        row = dict(item)
        surface = typed.get((source_id, row["source_variable_code"]))
        resolved = []
        if surface and surface.get("parsed_domain") is not None:
            row["domain_values"] = surface["parsed_domain"]
            row["domain_status"] = "EXACT_TYPED_SURFACE_DOMAIN"
            row["typed_surface_id"] = surface["surface_id"]
            row["surface_kind"] = surface["surface_kind"]
            row["representation_authority"] = surface["representation_authority"]
            row["ordinal"] = surface.get("ordinal")
            resolved.append("domain")
        else:
            raw_domain = _raw_codebook_domain(row)
            if raw_domain:
                row["domain_values"] = raw_domain
                row["domain_status"] = "CODEBOOK_NATIVE_OPTION_VALUES__TYPED_DECODE_PENDING"
                resolved.append("domain_raw")
        if surface:
            row["typed_surface_consumed"] = True
            row["typed_surface_id"] = surface["surface_id"]
            row["surface_kind"] = surface["surface_kind"]
            row["representation_authority"] = surface["representation_authority"]
            row["ordinal"] = surface.get("ordinal")
            if surface.get("parsed_domain") is None:
                row["domain_status"] = "EXACT_TYPED_SURFACE_REPRESENTATION__DOMAIN_EMPTY"
        if source_id == "SRC27" and row["source_variable_code"] in {"q301_2", "q301_7"}:
            from rawlsing_next.fiabc_lits_i_d03_risk_set_authority import (
                RESPONDENT_KEY_PREFIX, RISK_SET_REF,
            )
            row["unit_status"] = "EXACT_LITS_I_SELECTED_RESPONDENT_UNIT"
            row["unit"] = "LITS1_SELECTED_RESPONDENT"
            row["unit_evidence"] = RESPONDENT_KEY_PREFIX
            row["risk_set_status"] = "EXACT_LITS_I_D03_RISK_SET"
            row["risk_set_ref"] = RISK_SET_REF.key
            resolved.extend(["unit", "risk_set"])
        if source_id == "SRC35" and row["source_variable_code"] in {"Q291G5", "Q291P5"} and wvs:
            row["unit_status"] = "EXACT_WVS7_RESPONDENT_ROW_UNIT"
            row["unit"] = wvs["unit_law"]
            row["unit_evidence"] = "WVS7_PACKAGE_RESPONDENT_IDENTITY_LAW"
            row["topology"] = wvs["topology"]
            row["topology_status"] = "EXACT_WVS7_SOURCE_TOPOLOGY"
            row["risk_set_status"] = "EXACT_WVS7_RISK_SET"
            row["risk_set_ref"] = wvs["risk_ref"].key
            resolved.extend(["unit", "topology", "risk_set"])
        missing = [f for f in ("unit", "topology", "risk_set") if f not in row or str(row.get(f + "_status", "")).startswith("PENDING")]
        row["resolved_fields"] = sorted(set(resolved))
        row["unresolved_fields"] = missing
        row["field_owner"] = {
            "unit": "SOURCE_ITEM_UNIT_AUTHORITY_OWNER",
            "topology": "SOURCE_TOPOLOGY_AUTHORITY_OWNER",
            "risk_set": "SOURCE_RISK_SET_AUTHORITY_OWNER",
        }
        if row.get("domain_status") == "EXACT_TYPED_SURFACE_DOMAIN":
            resolved_counts["exact_typed_domain"] += 1
        elif row.get("domain_values"):
            resolved_counts["raw_codebook_domain"] += 1
        if "unit" in row.get("resolved_fields", []): resolved_counts["unit"] += 1
        if "risk_set" in row.get("resolved_fields", []): resolved_counts["risk_set"] += 1
        if "topology" in row.get("resolved_fields", []): resolved_counts["topology"] += 1
        items.append(row)
    native_objects = None
    if source_id == "SRC35" and wvs:
        wvs_items, inventory = _wvs_surfaces(typed, wvs, wvs_rows or {})
        items.extend(v["item"] for v in wvs_items.values())
        native_objects = {
            "occurrences": [v["occurrence"].material() for v in wvs_items.values()],
            "native_source_rules": [dataclasses.asdict(v["rule"]) for v in wvs_items.values()],
            "source_inventory": inventory.material(),
        }
        for row in items:
            if row["source_variable_code"] in wvs_items and row.get("source_id") == "SRC35":
                row["native_occurrence_constructed"] = True
                row["native_occurrence_status"] = "CONSTRUCTED_EXACT_GROUNDED_OCCURRENCE"
                row["native_source_rule_constructed"] = True
            elif row.get("source_id") != "SRC35":
                row["native_occurrence_constructed"] = False
                row["native_occurrence_status"] = "PENDING_EXACT_FIELDS"
                row["native_source_rule_constructed"] = False
    else:
        for row in items:
            row["native_occurrence_constructed"] = False
            row["native_occurrence_status"] = "PENDING_EXACT_FIELDS"
            row["native_source_rule_constructed"] = False
    if typed_only:
        items.extend(typed_only)
    report = dict(base)
    report["schema"] = SCHEMA
    report["b49_item_count"] = b49_item_count
    report["typed_surface_only_count"] = len(typed_only) + (2 if source_id == "SRC35" and wvs else 0)
    report["item_counts"] = dict(base["item_counts"])
    report["item_counts"]["total_preparation"] = len(items)
    report["pending_native_occurrences"] = items
    report["conditioner_context_items"] = [r for r in items if r["conditioning_context_retained"]]
    report["evidence_resolution"] = {
        "typed_surfaces_consumed": sum(1 for r in items if r.get("typed_surface_consumed")),
        "field_counts": dict(sorted(resolved_counts.items())),
        "native_occurrence_count": 2 if native_objects else 0,
        "native_source_rule_count": 2 if native_objects else 0,
        "source_inventory_count": 1 if native_objects else 0,
        "native_objects": native_objects,
        "planner_invocation_status": (
            "NOT_INVOKED__PARTIAL_INVENTORY_INCOMPLETE_AND_FRONTIER_ROLES_PENDING"
            if native_objects else "NOT_INVOKED__NO_COMPLETE_NATIVE_OCCURRENCE_PREMISES"),
    }
    report["binding_hash"] = _sha({k: v for k, v in report.items() if k != "binding_hash"})
    return report


def build_all():
    records = _r150_records()
    typed = _typed_surface_map()
    wvs = _wvs_package()
    out = {}
    for sid, base in sorted(records.items()):
        present = {i["source_variable_code"] for i in base["pending_native_occurrences"]}
        needs_rows = any(tsid == sid for tsid, _ in typed)
        rows = _r148_rows(sid) if needs_rows else {}
        extra = [_typed_only_item(sid, s, rows) for (tsid, var), s in typed.items()
                 if tsid == sid and var not in present and not (sid == "SRC35" and var in {"Q291G5", "Q291P5"})]
        out[sid] = resolve_source(sid, base, typed, wvs if sid == "SRC35" else None,
                                  _r148_rows("SRC35") if sid == "SRC35" else None, extra)
    total = sum(len(r["pending_native_occurrences"]) for r in out.values())
    b49_total = sum(r["b49_item_count"] for r in out.values())
    typed_only_total = sum(r["typed_surface_only_count"] for r in out.values())
    if b49_total != 4460 or typed_only_total != 33 or total != 4493:
        raise ValueError("R151_ITEM_DENOMINATOR_MISMATCH")
    summary = {
        "schema": "PYAT_R151_GROUNDED_NATIVE_OCCURRENCES_SUMMARY@1",
        "status": "R150_PENDING_FIELDS_REPAIRED_WITH_GROUNDED_NATIVE_OCCURRENCES_WHERE_SUPPORTED",
        "source_count": 35,
        "b49_item_records": b49_total,
        "typed_surface_only_items": total - b49_total,
        "preparation_items": total,
        "typed_surfaces_consumed": sum(r["evidence_resolution"]["typed_surfaces_consumed"] for r in out.values()),
        "preparation_items": total,
        "typed_surface_only_items": typed_only_total,
        "exact_typed_domains": sum(1 for r in out.values() for i in r["pending_native_occurrences"]
                                   if i.get("domain_status") == "EXACT_TYPED_SURFACE_DOMAIN"),
        "raw_codebook_domains": sum(1 for r in out.values() for i in r["pending_native_occurrences"]
                                    if i.get("domain_status", "").startswith("CODEBOOK_NATIVE")),
        "resolved_units": sum(1 for r in out.values() for i in r["pending_native_occurrences"]
                              if "unit" in i.get("resolved_fields", [])),
        "resolved_topologies": sum(1 for r in out.values() for i in r["pending_native_occurrences"]
                                   if "topology" in i.get("resolved_fields", [])),
        "resolved_risk_sets": sum(1 for r in out.values() for i in r["pending_native_occurrences"]
                                  if "risk_set" in i.get("resolved_fields", [])),
        "native_occurrences_constructed": sum(1 for r in out.values() for i in r["pending_native_occurrences"] if i.get("native_occurrence_constructed")),
        "native_source_rules_constructed": sum(len(r["evidence_resolution"]["native_objects"]["native_source_rules"]) if r["evidence_resolution"]["native_objects"] else 0 for r in out.values()),
        "source_inventories_constructed": sum(1 for r in out.values() if r["evidence_resolution"]["native_objects"]),
        "context_items_retained": sum(len(r["conditioner_context_items"]) for r in out.values()),
        "unmatched_relation_ids": sum(len(r["unmatched_relation_ids"]) for r in out.values()),
        "current_source_grants": 0,
        "survey_files_touched": 0,
        "native_execution_authorized": False,
        "limits": ["B49 historical evidence grade only", "partial native objects only where source-specific fields grounded", "no source read or U/Epre"],
    }
    return {"summary": summary, "records": out}


def write_records(result, out_root=RETURN_ROOT):
    root=Path(out_root); recdir=root/"records"; itemsdir=recdir/"ITEMS"
    itemsdir.mkdir(parents=True,exist_ok=True)
    for sid,rec in sorted(result["records"].items()):
        (recdir/f"{sid}_GROUNDED_NATIVE_INPUT.json").write_text(json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        with (itemsdir/f"{sid}.jsonl").open("w",encoding="utf-8") as h:
            for item in rec["pending_native_occurrences"]: h.write(_canonical(item)+"\n")
    (recdir/"SUMMARY.json").write_text(json.dumps(result["summary"],indent=2,sort_keys=True)+"\n",encoding="utf-8")
    with (recdir/"ALL35_GROUNDED_ACCOUNTING.jsonl").open("w",encoding="utf-8") as h:
        for sid,rec in sorted(result["records"].items()):
            row={"source_id":sid,"item_counts":rec["item_counts"],"evidence_resolution":rec["evidence_resolution"],"resolved_fields":rec["evidence_resolution"]["field_counts"],"native_occurrence_count":rec["evidence_resolution"]["native_occurrence_count"],"native_source_rule_count":rec["evidence_resolution"]["native_source_rule_count"],"source_inventory_count":rec["evidence_resolution"]["source_inventory_count"],"binding_hash":rec["binding_hash"]}
            h.write(_canonical(row)+"\n")
