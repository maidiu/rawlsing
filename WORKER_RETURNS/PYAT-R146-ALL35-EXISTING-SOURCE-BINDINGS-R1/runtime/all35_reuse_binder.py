"""R146 all35 existing-source-binding reuse adapter.

This adapter reuses the R145 metadata-only package binder and the independently
staged CLOSED35/U53A/U43 records. It opens no survey file and creates no source
right, scientific role, U/Epre or execution claim.
"""
from __future__ import annotations

import functools
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "PYAT_R146_ALL35_SOURCE_BINDING_REUSE@1"
PENDING = "PENDING_EXACT_CURRENT_SOURCE_ISSUANCE"
REPO_ROOT = Path(__file__).resolve().parents[3]
RETURN_ROOT = Path(__file__).resolve().parents[1]
R145_RETURN = REPO_ROOT / "WORKER_RETURNS" / "PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1"
INPUT_ROOT = REPO_ROOT / ".r61" / "r146-all35-reuse" / "inputs"
from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402

SHARED_INDEX_IDS = (
    "atlasY", "atlasE", "atlasX", "s35_roots", "s35_regime_registry",
    "s35_applicability", "s35_typed_join", "s35_acquisition", "s35_authority72",
    "I51", "B49rules", "B49preimage", "B49bind", "G50enum", "G50native",
    "G50map", "routeb", "exact", "batch", "issued", "binding", "c11", "c1",
    "i4", "empirical", "ff", "ff_ingress", "temporal", "cx_m1", "cx_m2",
    "cx_b5",
)

F1_F4 = (
    ("F1_EMPIRICAL_CLOSURE", "rawlsing_next.pre553_carrier_execution.CarrierNeutralResearchExecutor.execute_i03",
     ["EmpiricalQuerySpec", "EmpiricalPredicate", "EmpiricalFact@1.0.0", "exact source/replay refs"]),
    ("F2_DISCOVERY_AND_NO_DROP", "rawlsing_next.pre553_carrier_execution.CarrierNeutralResearchExecutor.execute_i05; rawlsing_next.universal_grammar.native_map.native_receipt_anti_join",
     ["DiscoveryResultReceipt@1.0.0", "complete declared candidate accounting", "no-drop ledger"]),
    ("F3_M1_LEARNED_DISPOSITION", "rawlsing_next.pre553_learned_empirical_adjudication.adjudicate_learned_empirical",
     ["M1AdjudicationInputBundle", "exact family-rule binding", "LearnedEmpiricalDisposition@1.0.0"]),
    ("F4_FF_V553_CONFRONTATION", "rawlsing_next.pre553_universal_empirical_extension.provide_empirical_possibility_slice_ext",
     ["exact I03/I05 evidence", "M1 disposition", "source-local FF/V553 inputs", "typed refusal where not permitted"]),
)


class All35BindingRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ref(kind: str, namespace: str, material: Any) -> ExactRef:
    digest = _sha(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:r146:{namespace}:sha256:{digest}", digest)


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise All35BindingRefusal("STAGED_INPUT_MISSING", str(path)) from exc
    except json.JSONDecodeError as exc:
        raise All35BindingRefusal("STAGED_INPUT_JSON_INVALID", str(path)) from exc


def load_inputs(input_root: str | Path = INPUT_ROOT) -> tuple[dict, list, dict, dict]:
    root = Path(input_root)
    index = _load(root / "INDEPENDENT_SOURCE_INDEX.json")
    closed = _load(root / "CLOSED35_DOCUMENTARY_RECONCILIATION.json")
    packets = _load(root / "original35_issuer_decision_packets.json")
    if not isinstance(index, dict) or not isinstance(index.get("entries"), list):
        raise All35BindingRefusal("SOURCE_INDEX_SCHEMA_INVALID")
    if not isinstance(closed, dict) or not isinstance(closed.get("rows"), list):
        raise All35BindingRefusal("CLOSED35_SCHEMA_INVALID")
    if not isinstance(packets, list):
        raise All35BindingRefusal("U43_ROSTER_SCHEMA_INVALID")
    pins = {
        "INDEPENDENT_SOURCE_INDEX.json": {"sha256": _file_sha(root / "INDEPENDENT_SOURCE_INDEX.json")},
        "CLOSED35_DOCUMENTARY_RECONCILIATION.json": {"sha256": _file_sha(root / "CLOSED35_DOCUMENTARY_RECONCILIATION.json")},
        "original35_issuer_decision_packets.json": {"sha256": _file_sha(root / "original35_issuer_decision_packets.json")},
    }
    return index, closed["rows"], {packet["atlas_id"]: packet for packet in packets}, pins


def _index_map(index: Mapping[str, Any]) -> dict[str, dict]:
    return {entry["id"]: entry for entry in index["entries"]}


@functools.lru_cache(maxsize=None)
def _git_blob_actual(ref: str, path: str) -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", f"{ref}:{path}"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=False,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def _index_ref(entry: Mapping[str, Any], role: str) -> dict[str, Any]:
    actual_blob = _git_blob_actual(entry["ref"], entry["path"])
    return {
        "role": role, "id": entry["id"],
        **{k: entry[k] for k in ("ref", "path", "git_blob", "content_sha256")},
        "git_object_verified": actual_blob == entry["git_blob"],
        "git_blob_actual": actual_blob,
    }


def _git_bytes(relpath: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"HEAD:{relpath}"], cwd=REPO_ROOT,
        capture_output=True, check=False,
    )
    if completed.returncode != 0:
        raise All35BindingRefusal("R145_GIT_OBJECT_UNAVAILABLE", relpath)
    return completed.stdout


def _r145_records(source_id: str) -> dict[str, Any]:
    prep_rel = f"WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/records/{source_id}_PACKAGE_PREPARATION.json"
    rows_rel = f"WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/records/{source_id}_ROW_ACCOUNTING.jsonl"
    try:
        prep_raw = _git_bytes(prep_rel)
        rows_raw = _git_bytes(rows_rel)
    except All35BindingRefusal:
        return {"status": "NO_STAGED_CODEBOOK_DOCUMENT", "row_accounting": None}
    prep = json.loads(prep_raw.decode("utf-8"))
    rows = rows_raw.count(b"\n")
    return {
        "status": "R145_FULL_CODEBOOK_ROW_ACCOUNTING_AVAILABLE",
        "preparation_path": prep_rel,
        "preparation_sha256": hashlib.sha256(prep_raw).hexdigest(),
        "row_accounting_path": rows_rel,
        "row_accounting_sha256": hashlib.sha256(rows_raw).hexdigest(),
        "row_accounting_bytes": len(rows_raw),
        "rows": rows,
        "role_counts": prep["row_accounting"]["role_counts"],
        "source_unit": prep.get("source_unit"),
        "dictionary": prep["dictionary"],
        "source_read_request_template": prep["source_read_request_template"],
        "note": "codebook rows are not the administered universe; header/semantics remain pending",
    }


def _binding_state(row: Mapping[str, Any], packet: Mapping[str, Any], r145_record: Mapping[str, Any]) -> str:
    if row["source_id"] == "SRC35":
        return "INTENTIONALLY_EXCLUDED_BY_AUTHORITY72"
    if row["historical_representation"]["census"] == "BLOCKED":
        return "EXISTING_BINDING_WITH_HISTORICAL_REPRESENTATION_BLOCKER"
    if row["later_packet_selected_fields"]:
        return "EXISTING_PARTIAL_BINDING_WITH_L2_RESIDUAL_SET"
    if r145_record["status"].startswith("R145_"):
        return "EXISTING_USABLE_METADATA_BINDING_WITH_FULL_CODEBOOK"
    if row["historical_prep72_launch_class"].startswith("L0_") or row["historical_prep72_launch_class"].startswith("L1_"):
        return "EXISTING_USABLE_METADATA_BINDING__NO_STAGED_CODEBOOK"
    return "EXISTING_BINDING_SOURCE_ACCESS_AND_U_EPRE_PENDING"


def _unresolved(row: Mapping[str, Any], packet: Mapping[str, Any], r145_record: Mapping[str, Any]) -> list[str]:
    source = packet["source"]
    out = []
    if source.get("current_source_access_permission") is None:
        out.append("CURRENT_SOURCE_ACCESS_PERMISSION")
    if source.get("current_source_edition_hash") is None:
        out.append("CURRENT_SOURCE_EDITION_HASH")
    if source.get("eligible_E_pre_count") is None:
        out.append("SCIENTIFIC_E_PRE")
    if source.get("original_U_count") is None:
        out.append("COMPLETE_NATIVE_U")
    if row["historical_representation"]["census"] == "BLOCKED":
        out.append("HISTORICAL_REPRESENTATION_AUTHORITY")
    if row["later_packet_selected_fields"]:
        out.append("L2_RESIDUAL_SURFACES")
    if r145_record["status"] == "NO_STAGED_CODEBOOK_DOCUMENT":
        out.append("STAGED_CURRENT_METADATA_DOCUMENT")
    out.append("SOURCE_RESPONSE_READ_GRANT_AND_CURRENT_RESOLVER")
    return out


def _country_summary(source: Mapping[str, Any]) -> dict[str, Any]:
    rows = source.get("historical_country_rows") or []
    statuses: dict[str, int] = {}
    for row in rows:
        status = str(row.get("source_mapping_status", "UNKNOWN"))
        statuses[status] = statuses.get(status, 0) + 1
    return {
        "row_count": len(rows),
        "mapping_status_counts": dict(sorted(statuses.items())),
        "authority_artifacts": sorted({
            (row.get("authority_path"), row.get("authority_artifact_sha256"))
            for row in rows
        }),
        "rows_sha256": _sha(rows),
        "rows": rows,
    }


def build_source(
    source_id: str, *, inputs: tuple[dict, list, dict, dict] | None = None,
) -> dict[str, Any]:
    index, closed_rows, packets, pins = inputs or load_inputs()
    rows = {row["source_id"]: row for row in closed_rows}
    if source_id not in rows or source_id not in packets:
        raise All35BindingRefusal("UNKNOWN_OR_INCOMPLETE_SOURCE_ID", source_id)
    row = rows[source_id]
    packet = packets[source_id]
    packet_hash = packet["source"]["original_manifest_identity"].get("recorded_source_sha256")
    if packet_hash not in (None, "", "UNBOUND") and packet_hash != row["canonical_sha256"]:
        raise All35BindingRefusal("SOURCE_HASH_MISMATCH_BETWEEN_CLOSED35_AND_U43", source_id)
    hash_binding_status = (
        "CLOSED35_AND_U43_HISTORICAL_HASH_MATCH"
        if packet_hash == row["canonical_sha256"]
        else "U43_ORIGINAL_MANIFEST_HASH_UNBOUND__CLOSED35_HISTORICAL_HASH_USED_FOR_NAVIGATION_ONLY"
    )
    wave = packet["required_original_wave_identity"]
    original_wave_identity = OriginalWaveIdentity(
        wave["atlas_id"], wave["dataset_id"], wave["source_family"], wave["wave"])
    r145_record = _r145_records(source_id)
    entries = _index_map(index)
    source_refs = []
    for entry_id in (f"s35_dossier_{source_id}",):
        entry = entries.get(entry_id)
        if entry:
            source_refs.append(_index_ref(entry, "source_dossier"))
    packet_aliases = {
        "SRC02": "s35_packet_AFR5", "SRC03": "s35_packet_AFR9",
        "SRC13": "s35_packet_EVS1999", "SRC14": "s35_packet_EVS2008",
        "SRC16": "s35_packet_GSS1972", "SRC17": "s35_packet_GSS1973",
        "SRC24": "s35_packet_LAT1995",
    }
    if source_id in packet_aliases:
        entry = entries.get(packet_aliases[source_id])
        if entry:
            source_refs.append(_index_ref(entry, "source_admission_packet"))
    source = packet["source"]
    structure = source.get("historical_structure") or {}
    candidate = {
        "schema": SCHEMA,
        "source_id": source_id,
        "atlas_id": source_id,
        "family": row["family"],
        "wave_or_release": row["wave_or_release"],
        "format": row["format"],
        "canonical_filename": row["canonical_filename"],
        "historical_canonical_sha256": row["canonical_sha256"],
        "historical_size_bytes": row["size_bytes"],
        "historical_identity_status": "HISTORICAL_NAVIGATION_ONLY_NOT_CURRENT_GRANT_OR_EDITION",
        "historical_hash_binding_status": hash_binding_status,
        "binding_state": _binding_state(row, packet, r145_record),
        "native_original_wave_identity": {
            "atlas_id": original_wave_identity.atlas_id,
            "dataset_id": original_wave_identity.dataset_id,
            "source_family": original_wave_identity.source_family,
            "wave": original_wave_identity.wave,
        },
        "existing_closed35_binding": {
            "census": row["historical_representation"]["census"],
            "classification": row["historical_representation"]["classification"],
            "governed_surfaces": row["historical_representation"]["governed_surfaces"],
            "prep72_launch_class": row["historical_prep72_launch_class"],
            "later_l2_disposition": row["later_l2_disposition"],
            "later_packet_selected_fields": row["later_packet_selected_fields"],
            "debt": row["historical_representation"]["debt"],
            "exceptions": row["historical_representation"]["exceptions"],
            "decoder_lane": row["decoder_lane"],
            "accepted_decoder_mode": row["accepted_decoder_mode"],
            "compatibility_scope": row["compatibility_scope"],
            "current_usage_rights": row["current_usage_rights"],
            "current_original_U_E_pre": row["current_original_U_E_pre"],
        },
        "existing_u43_binding": {
            "native_entrypoint": packet["native_entrypoint"],
            "required_original_wave_identity": wave,
            "research_identity_root": source.get("research_identity_root"),
            "research_identity_count": source.get("research_identity_count"),
            "historical_structure": structure,
            "original_manifest_identity": source.get("original_manifest_identity"),
            "native_BatchManifest": source.get("native_BatchManifest"),
            "permitted_native_execution_manifests": source.get("permitted_native_execution_manifests"),
            "raw_source_opened": source.get("raw_source_opened"),
            "reason": source.get("reason"),
            "current_source_access_permission": source.get("current_source_access_permission"),
            "current_source_edition_hash": source.get("current_source_edition_hash"),
            "eligible_E_pre_count": source.get("eligible_E_pre_count"),
            "original_U_count": source.get("original_U_count"),
        },
        "country_resolution": _country_summary(source),
        "source_specific_index_refs": source_refs,
        "governing_index_refs": [
            _index_ref(entries[entry_id], "shared_governing_reference")
            for entry_id in SHARED_INDEX_IDS if entry_id in entries
        ],
        "r145_codebook_reuse": r145_record,
        "source_read_request_template": {
            "source_id": source_id,
            "source_sha256": None,
            "source_sha256_status": PENDING,
            "source_format": row["format"],
            "historical_canonical_sha256": row["canonical_sha256"],
            "custody_locator_binding": "PENDING_CURRENT_SOURCE_IDENTITY_AND_EXTERNAL_GRANT",
            "host": "PENDING_EXTERNAL_TRUSTED_SOURCE_READ_DECISION",
            "purpose": "R146_SOURCE_BINDING_REUSE_PREPARATION",
            "consumer_use": "R134_SOURCE_LOCAL_EMPIRICAL_AND_LEARNED_PIPELINE",
            "read_operation": "SOURCE_RESPONSE_DECODE",
            "physical_read_extent": "EXACT_FILE",
            "status": "TEMPLATE_ONLY_NO_GRANT",
        },
        "prospective_u_e_pre": {
            "u_root": None, "e_pre_root": None,
            "state": "NULL_WITH_CAUSE",
            "cause": source.get("reason"),
            "scientific_roles": "UNASSIGNED_PENDING_EXACT_SOURCE_ISSUER",
            "topology": "PENDING_EXACT_HEADER_AND_SEMANTIC_AUTHORITY",
        },
        "consumer_requirements": [
            {"consumer_id": name, "owner": owner, "required_outputs": outputs,
             "state": "PREREGISTERED_PENDING_ACTUAL_SOURCE"}
            for name, owner, outputs in F1_F4
        ],
        "unresolved": _unresolved(row, packet, r145_record),
        "mechanical_wiring": (
            "ADAPTED_BY_R146_ALL35_REUSE_RUNTIME"
            if source_id in {"SRC23", "SRC22", "SRC30"}
            else "ADAPTED_RECORD_READY__METADATA_DOCUMENT_NOT_STAGED"
        ),
        "survey_file_touched": False,
        "source_read_grant_present": False,
        "native_execution_authorized": False,
        "next_runnable_invocation": (
            "PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R146-ALL35-EXISTING-SOURCE-BINDINGS-R1/runtime/render_source_preparation.py "
            f"--source-id {source_id}" if source_id in {"SRC23", "SRC22", "SRC30"}
            else "stage exact current codebook/header document, then rerun runtime/render_source_preparation.py "
                 f"--source-id {source_id}"
        ),
    }
    candidate["binding_hash"] = _sha({k: v for k, v in candidate.items() if k != "binding_hash"})
    return candidate


def build_all35(*, input_root: str | Path = INPUT_ROOT) -> dict[str, Any]:
    inputs = load_inputs(input_root)
    index, closed_rows, packets, pins = inputs
    ids = sorted({row["source_id"] for row in closed_rows} | set(packets))
    if len(ids) != 35 or len({row["source_id"] for row in closed_rows}) != 35:
        raise All35BindingRefusal("ALL35_SOURCE_SET_NOT_EXACT", str(len(ids)))
    records = {}
    for source_id in ids:
        records[source_id] = build_source(source_id, inputs=inputs)
    entries = _index_map(index)
    states: dict[str, int] = {}
    unresolved: dict[str, int] = {}
    for record in records.values():
        states[record["binding_state"]] = states.get(record["binding_state"], 0) + 1
        for key in record["unresolved"]:
            unresolved[key] = unresolved.get(key, 0) + 1
    summary = {
        "schema": "PYAT_R146_ALL35_REUSE_SUMMARY@1",
        "status": "ALL35_EXISTING_BINDING_REUSE_ADAPTED__CURRENT_SOURCE_ISSUANCE_PENDING",
        "source_count": len(records),
        "source_ids": ids,
        "input_pins": pins,
        "binding_state_counts": dict(sorted(states.items())),
        "unresolved_counts": dict(sorted(unresolved.items())),
        "shared_governing_index_refs": [
            _index_ref(entries[entry_id], "shared_governing_reference")
            for entry_id in SHARED_INDEX_IDS if entry_id in entries
        ],
        "sources_with_r145_full_codebook": sorted(
            source_id for source_id, record in records.items()
            if record["r145_codebook_reuse"]["status"].startswith("R145_")),
        "sources_without_staged_codebook": sorted(
            source_id for source_id, record in records.items()
            if record["r145_codebook_reuse"]["status"] == "NO_STAGED_CODEBOOK_DOCUMENT"),
        "total_codebook_rows_reused": sum(
            record["r145_codebook_reuse"].get("rows", 0) for record in records.values()),
        "sources_with_current_access_permission": sum(
            1 for record in records.values()
            if record["existing_u43_binding"]["current_source_access_permission"] is not None),
        "sources_with_current_edition_hash": sum(
            1 for record in records.values()
            if record["existing_u43_binding"]["current_source_edition_hash"] is not None),
        "sources_with_current_u_e_pre": sum(
            1 for record in records.values()
            if record["prospective_u_e_pre"]["u_root"] is not None
            and record["prospective_u_e_pre"]["e_pre_root"] is not None),
        "survey_files_touched": 0,
        "source_read_grants_created": 0,
        "native_execution_authorized": False,
        "limits": ["existing metadata/binding reuse only", "no survey response access", "no source/science grant"],
    }
    return {"summary": summary, "records": records, "inputs": inputs}


def write_records(result: Mapping[str, Any], out_root: str | Path = RETURN_ROOT) -> None:
    root = Path(out_root)
    records_dir = root / "records"
    records_dir.mkdir(parents=True, exist_ok=True)
    for source_id, record in sorted(result["records"].items()):
        (records_dir / f"{source_id}_REUSE_PREPARATION.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (records_dir / "SUMMARY.json").write_text(
        json.dumps(result["summary"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    matrix = {}
    with (records_dir / "ALL35_INDEX.jsonl").open("w", encoding="utf-8") as handle:
        for source_id, record in sorted(result["records"].items()):
            row = {
                "source_id": source_id,
                "family": record["family"],
                "wave_or_release": record["wave_or_release"],
                "format": record["format"],
                "binding_state": record["binding_state"],
                "native_original_wave_identity": record["native_original_wave_identity"],
                "r145_codebook_rows": record["r145_codebook_reuse"].get("rows"),
                "r145_codebook_status": record["r145_codebook_reuse"]["status"],
                "unresolved": record["unresolved"],
                "binding_hash": record["binding_hash"],
            }
            matrix[source_id] = row
            handle.write(_canonical(row) + "\n")
    (records_dir / "STATE_MATRIX.json").write_text(
        json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
