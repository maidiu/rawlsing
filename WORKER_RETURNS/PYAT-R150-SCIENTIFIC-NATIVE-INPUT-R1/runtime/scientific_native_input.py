"""R150 B49 item-authority compiler -> current native typed scientific input.

The inherited B49 compiler/corpus is loaded read-only from private staged inputs.
This adapter reads staged metadata/current records through git objects and never
opens a survey file. It creates no source grant, administered U, Epre or adoption.
"""
from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "PYAT_R150_SCIENTIFIC_NATIVE_INPUT@1"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = REPO_ROOT / ".r61" / "r150-scientific-native-input" / "inputs"
R148_BASE = "WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/records"


class ScientificNativeInputRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git_bytes(ref: str, path: str) -> bytes:
    completed = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=REPO_ROOT,
                               capture_output=True, check=False)
    if completed.returncode != 0:
        raise ScientificNativeInputRefusal("GIT_OBJECT_UNAVAILABLE", f"{ref}:{path}")
    return completed.stdout


def _git_json(ref: str, path: str) -> Any:
    return json.loads(_git_bytes(ref, path).decode("utf-8"))


def _load_b49():
    path = INPUT_ROOT / "pre553_inherited_source_rules.py"
    spec = importlib.util.spec_from_file_location("r150_b49_inherited", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["r150_b49_inherited"] = module
    spec.loader.exec_module(module)
    return module


def load_inputs() -> dict[str, Any]:
    pins = json.loads((INPUT_ROOT / "PINS.json").read_text(encoding="utf-8"))
    for item in pins:
        path = Path(item["staged"])
        raw = path.read_bytes()
        if len(raw) != int(item["bytes"]) or _bytes_sha(raw) != item["sha256"]:
            raise ScientificNativeInputRefusal("STAGED_B49_PIN_MISMATCH", str(path))
    corpus_doc = json.loads((INPUT_ROOT / "source_authority_corpus.json").read_text(encoding="utf-8"))
    b49 = _load_b49()
    corpus = b49.SourceAuthorityCorpus.from_document(corpus_doc)
    if len(corpus.items) != 4460 or len(corpus.sources) != 35:
        raise ScientificNativeInputRefusal("B49_CORPUS_DENOMINATOR_MISMATCH")
    return {"pins": pins, "corpus_doc": corpus_doc, "corpus": corpus, "b49": b49}


def _source_id(source) -> str:
    try:
        return f"SRC{int(source.source_id):02d}"
    except ValueError as exc:
        raise ScientificNativeInputRefusal("B49_SOURCE_ID_NOT_NUMERIC", source.source_id) from exc


def _current_records() -> dict[str, Any]:
    out = {}
    for n in range(1, 36):
        sid = f"SRC{n:02d}"
        out[sid] = _git_json("HEAD", f"{R148_BASE}/{sid}_CURRENT_METADATA_PREPARATION.json")
    return out


def _row_lookup(record: Mapping[str, Any], source_id: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    path = record["current_metadata"].get("row_accounting_path")
    if not path:
        return {}, []
    path = str(path).replace("/records/records/", "/records/")
    if not path.startswith("WORKER_RETURNS/"):
        if path.startswith("records/ROW_ACCOUNTING/"):
            path = f"WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/{path}"
        else:
            path = f"WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/{path}"
    raw = _git_bytes("HEAD", path)
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    by_var: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_var.setdefault(str(row.get("var_name") or row.get("raw_row", {}).get("var_name")), []).append(row)
    collisions = sorted(var for var, values in by_var.items() if len(values) > 1)
    return {var: values[0] for var, values in by_var.items() if len(values) == 1}, collisions


def _native_identity(source, source_id: str):
    from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity
    return NativeSourceIdentity(
        source_id=source_id, family=source.family, wave=source.wave,
        canonical_filename=source.canonical_filename,
        declared_sha256=source.declared_sha256,
        source_format=source.source_format, expected_rows=source.expected_rows,
    )


def _pending_item(item, rule, codebook_row, join_status, collision, source_id):
    row = codebook_row or {}
    raw = row.get("raw_row", {})
    return {
        "schema": "PYAT_R150_PENDING_NATIVE_OCCURRENCE@1",
        "source_id": source_id,
        "implementation_id": item.implementation_id,
        "source_variable_code": item.source_variable_code,
        "p2_row": item.p2_row,
        "p2_evidence_id": item.p2_evidence_id,
        "exact_identity_sha256": item.exact_identity_sha256,
        "overlay_evidence_ids": list(item.overlay_evidence_ids),
        "disposition": item.disposition,
        "binding_grade": item.binding_grade,
        "semantic_direction": item.semantic_direction(),
        "directional_certification_status": item.directional_certification_status,
        "current_directional_atom_eligible": item.current_directional_atom_eligible,
        "routing_status": item.routing_status,
        "response_binding_status": item.response_binding_status,
        "relation_evidence_id": item.relation_evidence_id,
        "relation_scope": "RELATION_EVIDENCE_PRESENT" if item.relation_evidence_id else "NO_RELATION_EVIDENCE",
        "compiler_status": rule.status,
        "compiler_reason": rule.reason,
        "codebook_join_status": join_status,
        "codebook_collision": collision,
        "codebook_row_hash": row.get("row_hash"),
        "codebook_var_name": row.get("var_name"),
        "question_text": raw.get("question_text"),
        "response_options_substantive": raw.get("response_options_substantive"),
        "response_options_special": raw.get("response_options_special"),
        "value_labels_count": raw.get("value_labels_count"),
        "measure": raw.get("measure"),
        "storage_type": raw.get("storage_type"),
        "unit_status": "PENDING_EXACT_ITEM_UNIT",
        "topology_status": "PENDING_EXACT_ITEM_TOPOLOGY",
        "domain_status": ("CODEBOOK_OPTIONS_PRESENT__TYPED_DOMAIN_DECODE_PENDING"
                          if raw.get("response_options_all") else "PENDING_EXACT_TYPED_DOMAIN"),
        "risk_set_status": "PENDING_EXACT_RISK_SET",
        "native_occurrence_status": "NOT_CONSTRUCTED__PENDING_UNIT_TOPOLOGY_DOMAIN_RISK",
        "target_measurement_eligible": (
            rule.status == "ADMINISTERED_MEASUREMENT_U_CANDIDATE"
            and join_status == "EXACT_CODEBOOK_VAR_JOIN" and not collision),
        "conditioning_context_retained": rule.status == "EXCLUDED_NOT_ADMINISTERED_U",
        "retained": True,
        "scientific_role": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        "current_acceptance_status": "NOT_ISSUED__HISTORICAL_B49_EVIDENCE_GRADE_ONLY",
    }


def build_source(source, record, b49, corpus_view, source_id, original_by_id):
    try:
        package = b49.select_source_rules(
            corpus_view, family=source.family, wave=source.wave, as_of="2026-10-26",
            promote_unmatched=False,
        )
    except Exception as exc:
        raise ScientificNativeInputRefusal("B49_SELECTION_REFUSED", f"{source_id}: {exc}") from exc
    rows, collisions = _row_lookup(record, source_id)
    items = list(package.selected) + list(package.held) + list(package.excluded) + list(package.superseded) + list(package.unknown)
    original_items = original_by_id
    pending = []
    joined = 0
    missing = []
    for rule in items:
        item = original_items.get(rule.implementation_id)
        if item is None:
            missing.append(rule.implementation_id)
            continue
        row = rows.get(item.source_variable_code)
        join_status = "EXACT_CODEBOOK_VAR_JOIN" if row else "CODEBOOK_VARIABLE_NOT_FOUND"
        collision = item.source_variable_code in collisions
        if row and not collision:
            joined += 1
        pending.append(_pending_item(item, rule, row, join_status, collision, source_id))
    native_identity = _native_identity(source, source_id)
    rep = {
        "schema": SCHEMA,
        "source_id": source_id,
        "family": source.family,
        "wave": source.wave,
        "b49_source_identity": source.identity_material(),
        "native_source_identity": {
            "source_id": native_identity.source_id, "family": native_identity.family,
            "wave": native_identity.wave, "canonical_filename": native_identity.canonical_filename,
            "declared_sha256": native_identity.declared_sha256,
            "source_format": native_identity.source_format,
            "expected_rows": native_identity.expected_rows,
            "scope": "INHERITED_DOCUMENTARY_IDENTITY__NOT_CURRENT_EDITION_OR_GRANT",
        },
        "selected_source_rule_package": package.as_dict(),
        "item_counts": {
            "total": len(items), "selected_u_candidate": len(package.selected),
            "held": len(package.held), "excluded_non_u_context": len(package.excluded),
            "superseded": len(package.superseded), "unknown": len(package.unknown),
            "codebook_joined": joined, "codebook_missing": len(items) - joined,
            "implementation_id_missing": len(missing),
        },
        "unmatched_relation_ids": sorted(corpus_view.unmatched_ids.intersection(
            {rule.implementation_id for rule in items})),
        "codebook_collisions": collisions,
        "family_label_resolution": (
            "LATINOBAROMETRO_ACCENTED_ITEM_LABEL_RESOLVED_TO_EXACT_SOURCE_WAVE_IDENTITY__NO_ID_CASEFOLD"
            if source.family == "Latinobarometro" else "EXACT_FAMILY_LABEL"),
        "pending_native_occurrences": pending,
        "conditioner_context_items": [p for p in pending if p["conditioning_context_retained"]],
        "native_source_rule_status": "PENDING_UNIT_TOPOLOGY_DOMAIN_RISK__NO_NATIVE_RULE_CONSTRUCTED",
        "native_source_inventory_status": "NOT_CONSTRUCTED__NO_COMPLETE_SOURCE_INVENTORY_PREMISES",
        "current_metadata": record["current_metadata"],
        "current_source_identity_or_grant": {
            "current_source_access_permission": None,
            "current_source_edition_sha256": None,
            "u_root": None, "e_pre_root": None,
            "status": "PENDING_EXACT_CURRENT_SOURCE_ISSUANCE",
        },
        "frontier_status": "UNSIGNED_PENDING_GROUNDED_ROLES_RISK_EPRE",
        "consumer_requirements": record.get("consumer_requirements", []),
        "already_grounded": [
            "B49 item authority corpus/compiler package",
            "NativeSourceIdentity from inherited documentary identity",
            "exact codebook row join by source/wave/var_name",
            "item disposition/direction/routing/response/relation evidence",
            "R148 current metadata document/row accounting",
        ],
        "indispensable_unbound": [
            "current source access permission", "current edition SHA-256",
            "complete native U", "scientific Epre", "source response-read grant/current resolver",
            "per-item unit/topology/typed domain/risk set",
            "current source-specific semantic roles and quantum of target/conditioner use",
            "representative empirical and learned-to-FF owner outputs",
        ],
        "next_original_source_read_call": {
            "function": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "resolved_arguments": {
                "source_id": source_id,
                "historical_canonical_sha256": source.declared_sha256,
                "source_format": source.source_format,
                "metadata_document": record["current_metadata"].get("path"),
            },
            "unbound_arguments": ["source_path", "SourceReadRequest.host", "SourceReadRequest.purpose",
                                  "SourceReadRequest.consumer_use", "SourceReadRequest.edition_sha256",
                                  "SourceReadRequest.metadata_freeze_refs", "SourceReadRequest.semantic_use_scope",
                                  "external current decision resolver"],
            "status": "NOT_RUN__EXACT_CURRENT_GRANT_PENDING",
        },
        "next_native_workload_call": {
            "function": "rawlsing_next.pre553_production_binding.prepare_production_discovery",
            "resolved_arguments": {"source_id": source_id, "b49_selected_package_hash": package.package_hash},
            "unbound_arguments": ["NativePreimageBundle", "SourceInventory/GrammarPolicy/ScientificFrontier",
                                  "external query/discovery AuthoritySnapshots", "U/Epre roots",
                                  "IssuedWorkloadRecord", "current edition/header reconciliation"],
            "status": "UNSIGNED_PLANNING_ONLY__DO_NOT_EXECUTE",
        },
        "survey_file_touched": False,
        "source_read_grant_present": False,
        "native_execution_authorized": False,
        "successor_target": record.get("completed_treatment_reuse") or record.get("existing_binding_reuse", {}).get("source_specific_index_refs"),
    }
    rep["binding_hash"] = _sha({k: v for k, v in rep.items() if k != "binding_hash"})
    return rep


def build_all():
    inputs = load_inputs()
    b49 = inputs["b49"]
    corpus = inputs["corpus"]
    normalized = []
    for item in corpus.items:
        family = "Latinobarometro" if item.source_family == "Latinobarómetro" else item.source_family
        normalized.append(dataclasses.replace(item, source_family=family))
    view = dataclasses.replace(corpus, items=tuple(normalized))
    current = _current_records()
    records = {}
    # grounded available LiTS records first, then other covered items, then all35 accounting
    order = [f"SRC{n:02d}" for n in (27, 28, 29, 30, 24, 26, 1)] + [
        f"SRC{n:02d}" for n in range(1, 36) if f"SRC{n:02d}" not in {f"SRC{x:02d}" for x in (27,28,29,30,24,26,1)}]
    for source_id in order:
        source = next((s for s in view.sources if _source_id(s) == source_id), None)
        if source is None:
            raise ScientificNativeInputRefusal("B49_SOURCE_NOT_FOUND", source_id)
        records[source_id] = build_source(
            source, current[source_id], b49, view, source_id,
            {item.implementation_id: item for item in corpus.items})
    total_items = sum(r["item_counts"]["total"] for r in records.values())
    if total_items != 4460:
        raise ScientificNativeInputRefusal("B49_ITEM_DENOMINATOR_MISMATCH", str(total_items))
    summary = {
        "schema": "PYAT_R150_SCIENTIFIC_NATIVE_INPUT_SUMMARY@1",
        "status": "B49_ITEM_AUTHORITY_WIRED_TO_PENDING_NATIVE_INPUTS__NO_SOURCE_OR_SCIENCE_ISSUANCE",
        "source_count": 35,
        "b49_item_records": total_items,
        "b49_sources_with_items": sorted(sid for sid, r in records.items() if r["item_counts"]["total"]),
        "b49_sources_without_items": sorted(sid for sid, r in records.items() if not r["item_counts"]["total"]),
        "selected_u_candidate": sum(r["item_counts"]["selected_u_candidate"] for r in records.values()),
        "held": sum(r["item_counts"]["held"] for r in records.values()),
        "excluded_non_u_context": sum(r["item_counts"]["excluded_non_u_context"] for r in records.values()),
        "unmatched_relation_ids": sum(len(r["unmatched_relation_ids"]) for r in records.values()),
        "codebook_joined": sum(r["item_counts"]["codebook_joined"] for r in records.values()),
        "codebook_missing": sum(r["item_counts"]["codebook_missing"] for r in records.values()),
        "native_identities": 35,
        "selected_packages": 35,
        "native_source_rules_constructed": 0,
        "source_inventories_constructed": 0,
        "pending_occurrences": sum(len(r["pending_native_occurrences"]) for r in records.values()),
        "current_source_grants": 0,
        "survey_files_touched": 0,
        "native_execution_authorized": False,
        "frontier_status": "UNSIGNED_PENDING_GROUNDED_ROLES_RISK_EPRE",
        "limits": ["B49 evidence grade is historical, not current adoption", "no source response access", "no fabricated U/Epre/current grant/roles"],
    }
    return {"summary": summary, "records": records, "inputs": inputs}


def write_records(result, out_root=RETURN_ROOT):
    root = Path(out_root); records_dir = root / "records"
    items_dir = records_dir / "ITEMS"; packages_dir = records_dir / "PACKAGES"
    items_dir.mkdir(parents=True, exist_ok=True); packages_dir.mkdir(parents=True, exist_ok=True)
    for sid, rec in sorted(result["records"].items()):
        (records_dir / f"{sid}_SCIENTIFIC_NATIVE_INPUT.json").write_text(
            json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        with (items_dir / f"{sid}.jsonl").open("w", encoding="utf-8") as handle:
            for item in rec["pending_native_occurrences"]:
                handle.write(_canonical(item) + "\n")
        (packages_dir / f"{sid}.json").write_text(
            json.dumps(rec["selected_source_rule_package"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (records_dir / "SUMMARY.json").write_text(json.dumps(result["summary"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (records_dir / "ALL35_B49_ACCOUNTING.jsonl").open("w", encoding="utf-8") as handle:
        for sid, rec in sorted(result["records"].items()):
            row = {
                "source_id": sid,
                "family": rec["family"],
                "wave": rec["wave"],
                "item_counts": rec["item_counts"],
                "unmatched_relation_ids": rec["unmatched_relation_ids"],
                "codebook_collisions": rec["codebook_collisions"],
                "native_source_rule_status": rec["native_source_rule_status"],
                "native_source_inventory_status": rec["native_source_inventory_status"],
                "frontier_status": rec["frontier_status"],
                "current_source_grant": rec["current_source_identity_or_grant"],
                "successor_target": rec.get("successor_target"),
                "binding_hash": rec["binding_hash"],
            }
            handle.write(_canonical(row) + "\n")
