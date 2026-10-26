"""R148 complete all35 current-metadata preparation from staged codebooks.

No survey file is opened, stat'ed, hashed or decoded. Reuses R147/R146/R145
records through exact git objects and writes only this return's runtime/records.
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

SCHEMA = "PYAT_R148_ALL35_COMPLETE_METADATA@1"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
INPUT_ROOT = REPO_ROOT / ".r61" / "r148-all35-complete-metadata" / "inputs"
R147_BASE = "WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/records"
csv.field_size_limit(10**9)


class CompleteMetadataRefusal(ValueError):
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


def _git_bytes(ref: str, relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{relpath}"], cwd=REPO_ROOT,
        capture_output=True, check=False,
    )
    if completed.returncode != 0:
        raise CompleteMetadataRefusal("GIT_OBJECT_UNAVAILABLE", f"{ref}:{relpath}")
    return completed.stdout


def _git_json(ref: str, relpath: str) -> Any:
    return json.loads(_git_bytes(ref, relpath).decode("utf-8"))


def load_inputs(root: str | Path = INPUT_ROOT) -> dict[str, Any]:
    root = Path(root)
    staged = json.loads((root / "STAGED_METADATA.json").read_text(encoding="utf-8"))
    if not isinstance(staged, list) or len(staged) != 6:
        raise CompleteMetadataRefusal("SIX_NEW_CODEBOOKS_REQUIRED", str(len(staged)))
    packets = json.loads((root / "original35_issuer_decision_packets.json").read_text(encoding="utf-8"))
    return {
        "root": root,
        "staged": staged,
        "packets": {packet["atlas_id"]: packet for packet in packets},
        "pins": {
            "STAGED_METADATA.json": _bytes_sha((root / "STAGED_METADATA.json").read_bytes()),
            "INDEPENDENT_SOURCE_INDEX.json": _bytes_sha((root / "INDEPENDENT_SOURCE_INDEX.json").read_bytes()),
            "CLOSED35_DOCUMENTARY_RECONCILIATION.json": _bytes_sha((root / "CLOSED35_DOCUMENTARY_RECONCILIATION.json").read_bytes()),
            "original35_issuer_decision_packets.json": _bytes_sha((root / "original35_issuer_decision_packets.json").read_bytes()),
        },
    }


def _r147_record(source_id: str) -> dict[str, Any]:
    return _git_json("HEAD", f"{R147_BASE}/{source_id}_CURRENT_METADATA_PREPARATION.json")


def _parse_new(spec: Mapping[str, Any], source_id: str) -> tuple[list[dict[str, str]], bytes]:
    path = Path(str(spec["path"]))
    raw = path.read_bytes()
    if len(raw) != int(spec["bytes"]) or _bytes_sha(raw) != spec["sha256"]:
        raise CompleteMetadataRefusal("NEW_METADATA_HASH_OR_BYTES_MISMATCH", source_id)
    rows = [dict(row) for row in csv.DictReader(io.StringIO(raw.decode("utf-8-sig", errors="replace")))]
    if not rows:
        raise CompleteMetadataRefusal("NEW_METADATA_EMPTY", source_id)
    if any(not str(row.get("var_name", "")).strip() for row in rows):
        raise CompleteMetadataRefusal("NEW_METADATA_VAR_NAME_MISSING", source_id)
    if len({row["var_name"] for row in rows}) != len(rows):
        raise CompleteMetadataRefusal("NEW_METADATA_DUPLICATE_VAR_NAME", source_id)
    return rows, raw


def _row_records(source_id: str, sha: str, rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out = []
    for index, row in enumerate(rows, 1):
        material = {str(k): str(v) for k, v in sorted(row.items())}
        out.append({
            "schema": "PYAT_R148_CODEBOOK_ROW_EVIDENCE@1",
            "source_id": source_id,
            "metadata_row_index": index,
            "var_name": row.get("var_name", ""),
            "row_hash": _sha(material),
            "row_identity": f"{source_id}:{sha}:{index}:{row.get('var_name', '')}",
            "raw_row": material,
            "retained": True,
            "scientific_role": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        })
    return out


def _augment_new(source_id: str, base: Mapping[str, Any], spec: Mapping[str, Any], packet: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rows, raw = _parse_new(spec, source_id)
    row_records = _row_records(source_id, spec["sha256"], rows)
    current_metadata = {
        "status": "CURRENT_METADATA_DOCUMENT_STAGED_AND_PINNED",
        "path": spec["path"],
        "original_path": spec.get("original_path"),
        "sha256": spec["sha256"],
        "bytes": spec["bytes"],
        "rows": len(rows),
        "columns": list(rows[0].keys()),
        "duplicate_native_codes": [],
        "row_accounting_path": f"records/ROW_ACCOUNTING/{source_id}.jsonl",
        "source_values": dict(sorted(Counter(r.get("source") for r in rows).items())),
        "wave_values": dict(sorted(Counter(r.get("wave") for r in rows).items())),
        "module_guess_counts": dict(sorted(Counter(r.get("module_guess") for r in rows).items())),
        "scientific_roles": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
    }
    research_count = packet["source"].get("research_identity_count")
    contradiction = None
    if research_count is not None and int(research_count) != len(rows):
        contradiction = {
            "kind": "CURRENT_CODEBOOK_ROW_COUNT_DIFFERS_FROM_U43_RESEARCH_IDENTITY_COUNT",
            "current_codebook_rows": len(rows),
            "research_identity_count": int(research_count),
            "disposition": "EXACT_SOURCE_SPECIFIC_RECONCILIATION_REQUIRED__DO_NOT_SILENTLY_DROP_EITHER",
        }
    unresolved = [u for u in base["current_unresolved"] if u != "STAGED_CURRENT_METADATA_DOCUMENT"]
    if contradiction:
        unresolved.append("CODEBOOK_RESEARCH_IDENTITY_COUNT_CONTRADICTION")
    candidate = dict(base)
    candidate["schema"] = SCHEMA
    candidate["current_metadata"] = current_metadata
    candidate["row_count_contradiction"] = contradiction
    candidate["current_unresolved"] = sorted(set(unresolved))
    candidate["native_preparation"] = dict(base["native_preparation"])
    candidate["native_preparation"]["current_metadata_document"] = current_metadata
    candidate["next_runnable_invocation"] = (
        "PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/runtime/render_all35_current_preparation.py "
        f"--source-id {source_id}"
    )
    candidate["binding_hash"] = _sha({k: v for k, v in candidate.items() if k != "binding_hash"})
    return candidate, row_records


def _normalise_prior(base: Mapping[str, Any]) -> dict[str, Any]:
    candidate = dict(base)
    candidate["schema"] = SCHEMA
    md = dict(base["current_metadata"])
    if md.get("row_accounting_path") and not str(md["row_accounting_path"]).startswith("WORKER_RETURNS/"):
        md["row_accounting_path"] = f"{R147_BASE}/{md['row_accounting_path']}"
    candidate["current_metadata"] = md
    candidate["next_runnable_invocation"] = (
        "PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R148-ALL35-COMPLETE-METADATA-R1/runtime/render_all35_current_preparation.py "
        f"--source-id {base['source_id']}"
    )
    return candidate


def build_all35(input_root: str | Path = INPUT_ROOT) -> dict[str, Any]:
    inputs = load_inputs(input_root)
    staged = {item["source_id"]: item for item in inputs["staged"]}
    ids = [f"SRC{i:02d}" for i in range(1, 36)]
    records: dict[str, Any] = {}
    new_rows: dict[str, list[dict[str, Any]]] = {}
    for source_id in ids:
        base = _r147_record(source_id)
        if source_id in staged:
            record, rows = _augment_new(source_id, base, staged[source_id], inputs["packets"][source_id])
            new_rows[source_id] = rows
        else:
            record = _normalise_prior(base)
        records[source_id] = record
    contradictions = {
        sid: rec["row_count_contradiction"]
        for sid, rec in records.items() if rec.get("row_count_contradiction") is not None
    }
    unresolved_counts: dict[str, int] = {}
    status_counts: dict[str, int] = {}
    for rec in records.values():
        status_counts[rec["current_representation_status"]] = status_counts.get(rec["current_representation_status"], 0) + 1
        for key in rec["current_unresolved"]:
            unresolved_counts[key] = unresolved_counts.get(key, 0) + 1
    summary = {
        "schema": "PYAT_R148_ALL35_COMPLETE_METADATA_SUMMARY@1",
        "status": "ALL35_CURRENT_METADATA_COMPLETE__NATIVE_PREPARATION_GROUNDED__CURRENT_SOURCE_ISSUANCE_PENDING",
        "source_count": 35,
        "source_ids": ids,
        "full35_denominator": 35,
        "excluded_from_full35_denominator": 0,
        "historical_exclusion_provenance_only": ["SRC35"],
        "current_metadata_available_count": 35,
        "missing_current_metadata_count": 0,
        "newly_completed_metadata_sources": sorted(staged),
        "prior_reused_metadata_sources": sorted(set(ids) - set(staged)),
        "current_metadata_rows": sum(
            int(rec["current_metadata"].get("rows", 0)) for rec in records.values()),
        "new_current_metadata_rows": sum(len(rows) for rows in new_rows.values()),
        "row_accounting_available_count": 35,
        "row_count_contradictions": contradictions,
        "current_representation_status_counts": dict(sorted(status_counts.items())),
        "current_unresolved_counts": dict(sorted(unresolved_counts.items())),
        "input_pins": inputs["pins"],
        "survey_files_touched": 0,
        "source_read_grants_created": 0,
        "native_execution_authorized": False,
        "limits": ["metadata documents only", "no source response access", "no source/science grant"],
    }
    return {"summary": summary, "records": records, "new_rows": new_rows, "inputs": inputs}


def write_records(result: Mapping[str, Any], out_root: str | Path = RETURN_ROOT) -> None:
    root = Path(out_root)
    records_dir = root / "records"
    rows_dir = records_dir / "ROW_ACCOUNTING"
    rows_dir.mkdir(parents=True, exist_ok=True)
    for source_id, rows in sorted(result["new_rows"].items()):
        with (rows_dir / f"{source_id}.jsonl").open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(_canonical(row) + "\n")
    for source_id, record in sorted(result["records"].items()):
        (records_dir / f"{source_id}_CURRENT_METADATA_PREPARATION.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (records_dir / "SUMMARY.json").write_text(
        json.dumps(result["summary"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    matrix = {
        sid: {
            "source_id": sid,
            "family": rec["family"],
            "wave_or_release": rec["wave_or_release"],
            "current_metadata_status": rec["current_metadata"]["status"],
            "current_metadata_rows": rec["current_metadata"].get("rows"),
            "row_accounting_path": rec["current_metadata"].get("row_accounting_path"),
            "current_representation_status": rec["current_representation_status"],
            "row_count_contradiction": rec.get("row_count_contradiction"),
            "current_unresolved": rec["current_unresolved"],
            "binding_hash": rec["binding_hash"],
        }
        for sid, rec in sorted(result["records"].items())
    }
    (records_dir / "STATE_MATRIX.json").write_text(
        json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (records_dir / "ALL35_COMPLETE_INDEX.jsonl").open("w", encoding="utf-8") as handle:
        for sid, row in matrix.items():
            handle.write(_canonical(row) + "\n")
