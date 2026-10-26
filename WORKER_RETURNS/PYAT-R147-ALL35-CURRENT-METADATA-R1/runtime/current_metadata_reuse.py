"""R147 current metadata + historical-label reconciliation adapter.

Reads staged metadata documents only. No survey file is opened, stat'ed, hashed
or decoded. Reuses the existing R146 binding records and R145 packager records
through exact git objects; creates no current grant, U/Epre or scientific role.
"""
from __future__ import annotations

import csv
import functools
import hashlib
import io
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "PYAT_R147_ALL35_CURRENT_METADATA@1"
PENDING = "PENDING_EXACT_CURRENT_SOURCE_ISSUANCE"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = REPO_ROOT / ".r61" / "r147-all35-current-metadata" / "inputs"
R146_BASE = "WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/records"
R145_BASE = "WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/records"
csv.field_size_limit(10**9)

TREATMENT_IDS = {
    "SRC02": "s35_packet_AFR5", "SRC03": "s35_packet_AFR9",
    "SRC13": "s35_packet_EVS1999", "SRC14": "s35_packet_EVS2008",
    "SRC16": "s35_packet_GSS1972", "SRC17": "s35_packet_GSS1973",
    "SRC24": "s35_packet_LAT1995",
}
L2_CLOSED = frozenset({"SRC13", "SRC16", "SRC17"})
L2_RESIDUAL = frozenset({"SRC02", "SRC03", "SRC24"})
PRIOR_R145 = frozenset({"SRC22", "SRC23", "SRC30"})


class CurrentMetadataRefusal(ValueError):
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


def _git_bytes_at(ref: str, relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{relpath}"], cwd=REPO_ROOT,
        capture_output=True, check=False,
    )
    if completed.returncode != 0:
        raise CurrentMetadataRefusal("GIT_OBJECT_UNAVAILABLE", f"{ref}:{relpath}")
    return completed.stdout


def _git_bytes(relpath: str) -> bytes:
    return _git_bytes_at("HEAD", relpath)


def _git_json(relpath: str) -> Any:
    return json.loads(_git_bytes(relpath).decode("utf-8"))


@functools.lru_cache(maxsize=None)
def _git_blob_actual(ref: str, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", f"{ref}:{path}"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _index_ref(entry: Mapping[str, Any], role: str) -> dict[str, Any]:
    actual = _git_blob_actual(entry["ref"], entry["path"])
    return {
        "role": role, "id": entry["id"],
        **{k: entry[k] for k in ("ref", "path", "git_blob", "content_sha256")},
        "git_object_verified": actual == entry["git_blob"],
        "git_blob_actual": actual,
    }


def load_inputs(input_root: str | Path = INPUT_ROOT) -> dict[str, Any]:
    root = Path(input_root)
    staged = json.loads((root / "STAGED_METADATA.json").read_text(encoding="utf-8"))
    index = json.loads((root / "INDEPENDENT_SOURCE_INDEX.json").read_text(encoding="utf-8"))
    closed = json.loads((root / "CLOSED35_DOCUMENTARY_RECONCILIATION.json").read_text(encoding="utf-8"))
    packets = json.loads((root / "original35_issuer_decision_packets.json").read_text(encoding="utf-8"))
    if not isinstance(staged, list):
        raise CurrentMetadataRefusal("STAGED_METADATA_LIST_REQUIRED")
    if not isinstance(index, dict) or not isinstance(index.get("entries"), list):
        raise CurrentMetadataRefusal("SOURCE_INDEX_INVALID")
    if not isinstance(closed, dict) or not isinstance(closed.get("rows"), list):
        raise CurrentMetadataRefusal("CLOSED35_INVALID")
    if not isinstance(packets, list):
        raise CurrentMetadataRefusal("U43_ROSTER_INVALID")
    return {
        "root": root,
        "staged": staged,
        "index": index,
        "index_entries": {entry["id"]: entry for entry in index["entries"]},
        "closed": {row["source_id"]: row for row in closed["rows"]},
        "packets": {packet["atlas_id"]: packet for packet in packets},
        "pins": {
            "STAGED_METADATA.json": _bytes_sha((root / "STAGED_METADATA.json").read_bytes()),
            "INDEPENDENT_SOURCE_INDEX.json": _bytes_sha((root / "INDEPENDENT_SOURCE_INDEX.json").read_bytes()),
            "CLOSED35_DOCUMENTARY_RECONCILIATION.json": _bytes_sha((root / "CLOSED35_DOCUMENTARY_RECONCILIATION.json").read_bytes()),
            "original35_issuer_decision_packets.json": _bytes_sha((root / "original35_issuer_decision_packets.json").read_bytes()),
        },
    }


def _r146_record(source_id: str) -> dict[str, Any]:
    return _git_json(f"{R146_BASE}/{source_id}_REUSE_PREPARATION.json")


def _r145_record(source_id: str) -> dict[str, Any] | None:
    try:
        prep = _git_json(f"{R145_BASE}/{source_id}_PACKAGE_PREPARATION.json")
        rows = _git_bytes(f"{R145_BASE}/{source_id}_ROW_ACCOUNTING.jsonl")
    except CurrentMetadataRefusal:
        return None
    return {
        "preparation": prep,
        "preparation_sha256": _bytes_sha(_git_bytes(f"{R145_BASE}/{source_id}_PACKAGE_PREPARATION.json")),
        "row_accounting_sha256": _bytes_sha(rows),
        "row_accounting_bytes": len(rows),
    }


def _parse_metadata(spec: Mapping[str, Any], source_id: str) -> tuple[list[dict[str, str]], bytes]:
    path = Path(str(spec["path"]))
    raw = path.read_bytes()
    if len(raw) != int(spec["bytes"]) or _bytes_sha(raw) != spec["sha256"]:
        raise CurrentMetadataRefusal("CURRENT_METADATA_HASH_OR_BYTES_MISMATCH", source_id)
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig", errors="replace")))
    rows = [dict(row) for row in reader]
    if not rows:
        raise CurrentMetadataRefusal("CURRENT_METADATA_EMPTY", source_id)
    if any(not str(row.get("var_name", "")).strip() for row in rows):
        raise CurrentMetadataRefusal("CURRENT_METADATA_VAR_NAME_MISSING", source_id)
    return rows, raw


def _row_records(source_id: str, spec: Mapping[str, Any], rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out = []
    for index, row in enumerate(rows, 1):
        material = {str(k): str(v) for k, v in sorted(row.items())}
        out.append({
            "schema": "PYAT_R147_CODEBOOK_ROW_EVIDENCE@1",
            "source_id": source_id,
            "metadata_row_index": index,
            "var_name": row.get("var_name", ""),
            "row_hash": _sha(material),
            "row_identity": f"{source_id}:{spec['sha256']}:{index}:{row.get('var_name', '')}",
            "raw_row": material,
            "retained": True,
            "scientific_role": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        })
    return out


def _treatment(source_id: str, inputs: Mapping[str, Any]) -> dict[str, Any] | None:
    entry_id = TREATMENT_IDS.get(source_id)
    if entry_id is None:
        return None
    entry = inputs["index_entries"].get(entry_id)
    if entry is None:
        return None
    try:
        packet = json.loads(_git_bytes_at(entry["ref"], entry["path"]).decode("utf-8"))
    except Exception as exc:
        return {"index_ref": _index_ref(entry, "source_treatment_packet"), "status": "TREATMENT_PACKET_UNREADABLE", "detail": str(exc)}
    return {
        "index_ref": _index_ref(entry, "source_treatment_packet"),
        "status": packet.get("status") or packet.get("terminal"),
        "terminal": packet.get("terminal"),
        "selected_fields": packet.get("later_packet_selected_fields") or packet.get("residual_summary") or {},
    }


def _representation_status(source_id: str, row: Mapping[str, Any], treatment: Mapping[str, Any] | None) -> tuple[str, str]:
    historical = row["historical_representation"]["census"]
    if source_id == "SRC35":
        return ("HISTORICAL_EXCLUSION_PROVENANCE_ONLY__INCLUDED_IN_FULL35_DENOMINATOR",
                "HISTORICAL_NOT_CURRENT_AUTOMATIC_DENIAL")
    if source_id in L2_RESIDUAL:
        return ("PARTIAL_DOCUMENTARY_AUTHORITY__EXACT_RESIDUAL_SET_STILL_FROZEN",
                "HISTORICAL_LABEL_PLUS_EXACT_CURRENT_RESIDUAL_GAP")
    if source_id in L2_CLOSED:
        return ("DOCUMENTARY_AUTHORITY_CLOSED__CURRENT_SOURCE_ACCESS_AND_U_EPRE_PENDING",
                "HISTORICAL_LABEL_SUPERSEDED_BY_COMPLETED_L2_TREATMENT")
    if source_id == "SRC14":
        return ("DOCUMENTARY_REALIZATION_AUTHORIZED__CURRENT_RELEASE_HASH_PENDING",
                "HISTORICAL_LABEL_SUPERSEDED_BY_L2R_TREATMENT")
    if historical == "BLOCKED":
        return ("HISTORICAL_BLOCKER_PROVENANCE_ONLY__CURRENT_REPRESENTATION_AUTHORITY_NOT_ESTABLISHED",
                "HISTORICAL_LABEL_NOT_CURRENT_AUTOMATIC_DENIAL")
    return ("HISTORICAL_PASS_PROVENANCE_ONLY__CURRENT_SOURCE_ACCESS_PENDING",
            "HISTORICAL_LABEL_NOT_CURRENT_AUTOMATIC_DENIAL")


def build_source(source_id: str, inputs: Mapping[str, Any] | None = None) -> dict[str, Any]:
    inputs = inputs or load_inputs()
    if source_id not in inputs["closed"] or source_id not in inputs["packets"]:
        raise CurrentMetadataRefusal("UNKNOWN_OR_INCOMPLETE_SOURCE_ID", source_id)
    base = _r146_record(source_id)
    row = inputs["closed"][source_id]
    packet = inputs["packets"][source_id]
    staged_by_id = {item["source_id"]: item for item in inputs["staged"]}
    staged = staged_by_id.get(source_id)
    r145 = _r145_record(source_id) if source_id in PRIOR_R145 else None
    treatment = _treatment(source_id, inputs)
    current_rows = None
    current_document = None
    contradiction = None
    if staged is not None:
        rows, raw = _parse_metadata(staged, source_id)
        row_records = _row_records(source_id, staged, rows)
        current_rows = len(rows)
        current_document = {
            "status": "CURRENT_METADATA_DOCUMENT_STAGED_AND_PINNED",
            "path": staged["path"], "original_path": staged.get("original_path"),
            "sha256": staged["sha256"], "bytes": staged["bytes"], "rows": len(rows),
            "columns": list(rows[0].keys()),
            "duplicate_native_codes": [k for k, v in Counter(r.get("var_name") for r in rows).items() if v > 1],
            "row_accounting_path": f"records/ROW_ACCOUNTING/{source_id}.jsonl",
            "source_values": dict(sorted(Counter(r.get("source") for r in rows).items())),
            "wave_values": dict(sorted(Counter(r.get("wave") for r in rows).items())),
            "module_guess_counts": dict(sorted(Counter(r.get("module_guess") for r in rows).items())),
            "scientific_roles": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        }
    elif r145 is not None:
        prep = r145["preparation"]
        current_rows = prep["row_accounting"]["total_rows"]
        current_document = {
            "status": "PRIOR_R145_CURRENT_METADATA_BINDING_REUSED",
            "path": f"{R145_BASE}/{source_id}_PACKAGE_PREPARATION.json",
            "sha256": r145["preparation_sha256"],
            "row_accounting_path": f"{R145_BASE}/{source_id}_ROW_ACCOUNTING.jsonl",
            "row_accounting_sha256": r145["row_accounting_sha256"],
            "rows": current_rows,
            "role_counts": prep["row_accounting"]["role_counts"],
            "dictionary": prep["dictionary"],
            "scientific_roles": "PROPOSED_METADATA_ROLES_ONLY_PENDING_EXACT_SEMANTIC_AUTHORITY",
        }
    else:
        hist = base["existing_u43_binding"]["historical_structure"] or {}
        current_document = {
            "status": "CURRENT_METADATA_DOCUMENT_NOT_STAGED__EXACT_DOCUMENT_NAMED",
            "source_id": source_id,
            "needed_document": f"current codebook/metadata document for {source_id} ({row['family']} {row['wave_or_release']})",
            "historical_codebook_path": hist.get("codebook_path"),
            "historical_codebook_exists": hist.get("codebook_exists"),
            "historical_audit_status": hist.get("audit_status"),
        }
    if current_rows is not None:
        research_count = packet["source"].get("research_identity_count")
        if research_count is not None and int(research_count) != int(current_rows):
            contradiction = {
                "kind": "CURRENT_CODEBOOK_ROW_COUNT_DIFFERS_FROM_U43_RESEARCH_IDENTITY_COUNT",
                "current_codebook_rows": current_rows,
                "research_identity_count": int(research_count),
                "disposition": "EXACT_SOURCE_SPECIFIC_RECONCILIATION_REQUIRED__DO_NOT_SILENTLY_DROP_EITHER",
            }
    rep_status, label_effect = _representation_status(source_id, row, treatment)
    unresolved = [
        u for u in base["unresolved"]
        if u not in {"HISTORICAL_REPRESENTATION_AUTHORITY", "L2_RESIDUAL_SURFACES"}
    ]
    if current_document["status"].startswith(("CURRENT_METADATA_DOCUMENT_STAGED", "PRIOR_R145")):
        unresolved = [u for u in unresolved if u != "STAGED_CURRENT_METADATA_DOCUMENT"]
    if source_id in L2_RESIDUAL:
        unresolved.append("EXACT_L2_RESIDUAL_SEMANTIC_SET")
    if source_id == "SRC14":
        unresolved.append("CURRENT_RELEASE_HASH")
    if source_id not in L2_RESIDUAL and source_id not in L2_CLOSED and source_id != "SRC14" and row["historical_representation"]["census"] == "BLOCKED":
        unresolved.append("CURRENT_REPRESENTATION_AUTHORITY_NOT_ESTABLISHED")
    if contradiction:
        unresolved.append("CODEBOOK_RESEARCH_IDENTITY_COUNT_CONTRADICTION")
    candidate = {
        "schema": SCHEMA,
        "source_id": source_id,
        "family": row["family"],
        "wave_or_release": row["wave_or_release"],
        "format": row["format"],
        "full35_denominator": True,
        "excluded_from_full35_denominator": False,
        "historical_label_provenance": {
            "census": row["historical_representation"]["census"],
            "classification": row["historical_representation"]["classification"],
            "prep72_launch_class": row["historical_prep72_launch_class"],
            "later_l2_disposition": row["later_l2_disposition"],
            "historical_label_effect": label_effect,
        },
        "current_representation_status": rep_status,
        "completed_treatment_reuse": treatment,
        "current_metadata": current_document,
        "row_count_contradiction": contradiction,
        "existing_binding_reuse": {
            "r146_binding_state": base["binding_state"],
            "native_original_wave_identity": base["native_original_wave_identity"],
            "source_specific_index_refs": base["source_specific_index_refs"],
            "governing_index_refs": base["governing_index_refs"],
            "country_resolution": base["country_resolution"],
            "existing_closed35_binding": base["existing_closed35_binding"],
            "existing_u43_binding": base["existing_u43_binding"],
            "r145_codebook_reuse": base["r145_codebook_reuse"],
        },
        "current_unresolved": sorted(set(unresolved)),
        "source_read_request_template": {
            **base["source_read_request_template"],
            "current_metadata_path": current_document.get("path"),
            "current_metadata_sha256": current_document.get("sha256"),
            "status": "TEMPLATE_ONLY_CURRENT_SOURCE_GRANT_AND_EDITION_HASH_PENDING",
        },
        "native_preparation": {
            "original_wave_identity": base["native_original_wave_identity"],
            "current_metadata_document": current_document,
            "native_source_identity_status": "CURRENT_EDITION_SHA_AND_HEADER_RECEIPT_PENDING",
            "native_preimage_bundle_status": "NOT_CREATED__SOURCE_ACCESS_AND_ROLE_SEMANTICS_PENDING",
            "source_package_owner": "rawlsing_next.pre553_source_native_preimage_adapter.NativeSourcePackage",
            "prospective_u_e_pre": base["prospective_u_e_pre"],
        },
        "consumer_requirements": base["consumer_requirements"],
        "survey_file_touched": False,
        "source_read_grant_present": False,
        "native_execution_authorized": False,
        "next_runnable_invocation": (
            f"PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/runtime/render_current_source_preparation.py --source-id {source_id}"
        ),
    }
    candidate["binding_hash"] = _sha(candidate)
    candidate["_row_records"] = row_records if staged is not None else None
    return candidate


def build_all35(*, input_root: str | Path = INPUT_ROOT) -> dict[str, Any]:
    inputs = load_inputs(input_root)
    ids = sorted(inputs["closed"])
    if len(ids) != 35:
        raise CurrentMetadataRefusal("ALL35_SOURCE_SET_NOT_EXACT", str(len(ids)))
    records = {source_id: build_source(source_id, inputs=inputs) for source_id in ids}
    state_counts: dict[str, int] = {}
    unresolved_counts: dict[str, int] = {}
    for rec in records.values():
        state_counts[rec["current_representation_status"]] = state_counts.get(rec["current_representation_status"], 0) + 1
        for key in rec["current_unresolved"]:
            unresolved_counts[key] = unresolved_counts.get(key, 0) + 1
    summary = {
        "schema": "PYAT_R147_ALL35_CURRENT_METADATA_SUMMARY@1",
        "status": "ALL35_CURRENT_METADATA_ADAPTED__HISTORICAL_LABELS_RECONCILED__CURRENT_SOURCE_ISSUANCE_PENDING",
        "source_count": len(records),
        "source_ids": ids,
        "full35_denominator": 35,
        "excluded_from_full35_denominator": 0,
        "historical_exclusion_provenance_only": ["SRC35"],
        "input_pins": inputs["pins"],
        "staged_current_metadata_count": len(inputs["staged"]),
        "prior_r145_metadata_count": len(PRIOR_R145),
        "current_metadata_available_count": sum(
            1 for rec in records.values()
            if rec["current_metadata"]["status"].startswith(("CURRENT_METADATA_DOCUMENT_STAGED", "PRIOR_R145"))),
        "missing_current_metadata_count": sum(
            1 for rec in records.values()
            if rec["current_metadata"]["status"].startswith("CURRENT_METADATA_DOCUMENT_NOT_STAGED")),
        "current_metadata_rows": sum(
            rec["current_metadata"].get("rows", 0) for rec in records.values()),
        "row_count_contradictions": {
            sid: rec["row_count_contradiction"]
            for sid, rec in records.items() if rec["row_count_contradiction"] is not None
        },
        "current_representation_status_counts": dict(sorted(state_counts.items())),
        "current_unresolved_counts": dict(sorted(unresolved_counts.items())),
        "source_read_grants_created": 0,
        "survey_files_touched": 0,
        "native_execution_authorized": False,
        "limits": ["metadata documents only", "no source response access", "no source/science grant"],
    }
    return {"summary": summary, "records": records, "inputs": inputs}


def write_records(result: Mapping[str, Any], out_root: str | Path = RETURN_ROOT) -> None:
    root = Path(out_root)
    records_dir = root / "records"
    rows_dir = records_dir / "ROW_ACCOUNTING"
    rows_dir.mkdir(parents=True, exist_ok=True)
    matrix = {}
    with (records_dir / "ALL35_CURRENT_INDEX.jsonl").open("w", encoding="utf-8") as handle:
        for source_id, record in sorted(result["records"].items()):
            row_records = record.pop("_row_records", None)
            if row_records is not None:
                with (rows_dir / f"{source_id}.jsonl").open("w", encoding="utf-8") as rows_handle:
                    for row in row_records:
                        rows_handle.write(_canonical(row) + "\n")
            (records_dir / f"{source_id}_CURRENT_METADATA_PREPARATION.json").write_text(
                json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            row = {
                "source_id": source_id,
                "family": record["family"],
                "wave_or_release": record["wave_or_release"],
                "format": record["format"],
                "full35_denominator": True,
                "current_representation_status": record["current_representation_status"],
                "current_metadata_status": record["current_metadata"]["status"],
                "current_metadata_rows": record["current_metadata"].get("rows"),
                "row_count_contradiction": record["row_count_contradiction"],
                "current_unresolved": record["current_unresolved"],
                "binding_hash": record["binding_hash"],
            }
            matrix[source_id] = row
            handle.write(_canonical(row) + "\n")
    (records_dir / "SUMMARY.json").write_text(
        json.dumps(result["summary"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (records_dir / "STATE_MATRIX.json").write_text(
        json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
