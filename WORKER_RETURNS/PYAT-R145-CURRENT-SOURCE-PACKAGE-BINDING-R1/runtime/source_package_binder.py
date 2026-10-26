"""R145 metadata-only source-package binder.

This is a pre-execution transport. It consumes exact staged codebook documents
and never opens, stats, hashes or decodes a survey response file. It creates no
source read grant, scientific role, U/Epre root or NativePreimageBundle.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity

SCHEMA = "PYAT_R145_SOURCE_PACKAGE_BINDER@1"
ROW_ACCOUNTING_SCHEMA = "PYAT_R145_CODEBOOK_ROW_ACCOUNTING@1"
PENDING = "PENDING_USER_AUTHORIZED_IDENTITY_RECEIPT"
SOURCE_READ_OPERATION = "SOURCE_RESPONSE_DECODE"
EXACT_FILE = "EXACT_FILE"
REQUIRED_COLUMNS = frozenset({
    "source", "wave", "module_guess", "var_name", "question_text",
    "storage_type", "measure", "response_options_substantive",
    "response_options_special", "response_options_all", "note",
})


class PackageBindingRefusal(ValueError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _bytes_sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _ref(kind: str, namespace: str, material: Any):
    digest = _sha(material)
    from rawlsing_next.pre553_empirical_objects import ExactRef
    return ExactRef(kind, f"urn:rawlsing:pre553:r145:{namespace}:sha256:{digest}", digest)


@dataclass(frozen=True)
class DictionarySpec:
    source_id: str
    family: str
    wave: str
    metadata_path: Path
    sha256: str
    bytes: int
    codebook_rows: int
    survey_locator: str
    source_format: str
    scope: str

    @classmethod
    def from_scope_entry(cls, entry: Mapping[str, Any]) -> "DictionarySpec":
        path = Path(str(entry["staged_metadata_path"]))
        locator = str(entry["survey_locator_requested_for_metadata_only"])
        suffix = Path(locator).suffix.lower()
        if suffix not in {".sav", ".dta"}:
            raise PackageBindingRefusal("SOURCE_FORMAT_UNSUPPORTED", locator)
        return cls(
            source_id=str(entry["source_id"]), family=str(entry["family"]),
            wave=str(entry["wave"]), metadata_path=path,
            sha256=str(entry["sha256"]), bytes=int(entry["bytes"]),
            codebook_rows=int(entry["codebook_rows"]),
            survey_locator=locator, source_format=suffix[1:].upper(),
            scope=str(entry.get("scope", "")),
        )


def load_metadata_scope(scope_path: str | Path) -> tuple[dict, ...]:
    path = Path(scope_path)
    document = json.loads(path.read_text(encoding="utf-8"))
    entries = document.get("candidate_inputs")
    if not isinstance(entries, list) or not entries:
        raise PackageBindingRefusal("METADATA_SCOPE_INPUTS_REQUIRED")
    return tuple(DictionarySpec.from_scope_entry(entry) for entry in entries)


def _read_pinned_dictionary(spec: DictionarySpec) -> tuple[bytes, list[dict[str, str]], list[str]]:
    raw = spec.metadata_path.read_bytes()
    if len(raw) != spec.bytes or _bytes_sha(raw) != spec.sha256:
        raise PackageBindingRefusal("DICTIONARY_HASH_OR_BYTES_MISMATCH", str(spec.metadata_path))
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text))
    fields = tuple(reader.fieldnames or ())
    missing = REQUIRED_COLUMNS - set(fields)
    if missing:
        raise PackageBindingRefusal("DICTIONARY_COLUMNS_MISSING", repr(sorted(missing)))
    rows = [dict(row) for row in reader]
    if len(rows) != spec.codebook_rows:
        raise PackageBindingRefusal("DICTIONARY_ROW_COUNT_MISMATCH",
                                    f"{len(rows)} != {spec.codebook_rows}")
    for index, row in enumerate(rows, 1):
        if not str(row.get("var_name", "")).strip():
            raise PackageBindingRefusal("ROW_IDENTITY_MISSING", str(index))
        if str(row.get("source", "")) != spec.family or str(row.get("wave", "")) != spec.wave:
            raise PackageBindingRefusal("ROW_SOURCE_WAVE_MISMATCH", str(index))
    return raw, rows, list(fields)


def _role(row: Mapping[str, str]) -> tuple[str, tuple[str, ...]]:
    var = str(row.get("var_name", "")).strip()
    module = str(row.get("module_guess", "")).strip()
    question = str(row.get("question_text", "")).strip()
    storage = str(row.get("storage_type", "")).strip().lower()
    measure = str(row.get("measure", "")).strip().lower()
    note = str(row.get("note", "")).strip().lower()
    options = str(row.get("response_options_substantive", "")).strip()
    labels = str(row.get("value_labels_count", "")).strip()
    lower = var.lower()
    evidence = [f"var_name={var}", f"module_guess={module}"]
    if "weight" in lower or any(token in lower for token in (
            "wtss", "wgt", "vstrat", "vpsu", "psu", "oversamp", "rweight", "wtssall", "wtssnr")):
        return "WEIGHT_OR_DESIGN", tuple(evidence + [f"var_name_token=weight/design", f"question={question[:80]}"])
    if module == "weighting":
        return "WEIGHT_OR_DESIGN", tuple(evidence + ["module_guess=weighting"])
    if module == "household_roster" or lower in {"hhid", "hompop", "adults", "babies", "childsinhh"}:
        return "HOUSEHOLD_OR_ROSTER", tuple(evidence + [f"question={question[:80]}", f"note={note[:80]}"])
    if module == "repeated_person_block" or any(
            lower.startswith(prefix) and lower[len(prefix):].isdigit()
            for prefix in ("advisor", "child", "cowork", "away", "child")):
        return "PERSON_OR_REPEATED_BLOCK", tuple(evidence + [f"question={question[:80]}"])
    if "rank" in lower or lower.startswith("mr"):
        return "RANKED_OR_MR_RESPONSE", tuple(evidence + [f"var_name_token=rank/mr"])
    if lower in {"fileversion", "id", "year", "country", "sampapp", "mode", "sample", "ballot", "form", "hhid", "interviewerid"}:
        return "SOURCE_ADMINISTRATIVE_IDENTITY", tuple(evidence + [f"question={question[:80]}", f"note={note[:80]}"])
    if module == "administrative":
        return "SOURCE_ADMINISTRATIVE_OR_METADATA", tuple(evidence + [f"question={question[:80]}", f"note={note[:80]}"])
    if storage != "numeric":
        return "TEXT_OR_NONNUMERIC_HELD", tuple(evidence + [f"storage_type={storage}", f"measure={measure}"])
    if measure == "unknown":
        return "UNKNOWN_MEASURE_HELD", tuple(evidence + ["measure=unknown"])
    if options or labels not in {"", "0"}:
        return "SUBSTANTIVE_QUESTION_CANDIDATE", tuple(evidence + [
            f"question={question[:120]}", f"substantive_option_count_field={labels}",
            f"has_substantive_options={bool(options)}",
        ])
    return "HELD_NO_GROUNDED_QUESTION_OR_OPTIONS", tuple(evidence + [f"question={question[:80]}"])


def _row_account(spec: DictionarySpec, index: int, row: Mapping[str, str]) -> dict[str, Any]:
    role, evidence = _role(row)
    material = {key: str(row.get(key, "")) for key in sorted(row)}
    return {
        "schema": ROW_ACCOUNTING_SCHEMA,
        "source_id": spec.source_id,
        "family": spec.family,
        "wave": spec.wave,
        "dictionary_sha256": spec.sha256,
        "metadata_row_index": index,
        "var_name": row["var_name"],
        "row_hash": _sha(material),
        "row_identity": f"{spec.source_id}:{spec.family}:{spec.wave}:{index}:{row['var_name']}",
        "storage_type": row.get("storage_type", ""),
        "measure": row.get("measure", ""),
        "module_guess": row.get("module_guess", ""),
        "question_text": row.get("question_text", ""),
        "question_text_full": row.get("question_text_full", ""),
        "value_labels_count": row.get("value_labels_count", ""),
        "response_options_substantive": row.get("response_options_substantive", ""),
        "response_options_special": row.get("response_options_special", ""),
        "response_options_all": row.get("response_options_all", ""),
        "note": row.get("note", ""),
        "role_proposal": role,
        "role_evidence": list(evidence),
        "role_state": "PROPOSED_FROM_ROW_EVIDENCE__NOT_SCIENTIFIC_AUTHORITY",
        "scientific_role": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
        "topology": "UNRESOLVED_PENDING_HEADER_AND_SEMANTIC_AUTHORITY",
        "retained": True,
    }


def _source_unit(rows: Sequence[Mapping[str, str]]) -> str:
    by_name = {str(row.get("var_name", "")): row for row in rows}
    identity = by_name.get("id")
    household = by_name.get("hhid")
    if identity is not None and "respondent" in str(identity.get("question_text", "")).lower():
        return "PERSON_RESPONDENT_IDENTIFIED_BY_ROW_EVIDENCE"
    if household is not None and "household" in str(household.get("question_text", "")).lower():
        return "HOUSEHOLD_ID_WITH_RESPONDENT_ITEMS_BY_ROW_EVIDENCE"
    return "UNRESOLVED_PENDING_HEADER_IDENTITY_EVIDENCE"


def _consumer_requirements(spec: DictionarySpec) -> list[dict[str, Any]]:
    return [
        {
            "consumer_id": "F1_EMPIRICAL_CLOSURE",
            "owner": "rawlsing_next.pre553_carrier_execution.CarrierNeutralResearchExecutor.execute_i03",
            "required_outputs": ["EmpiricalQuerySpec", "EmpiricalPredicate", "EmpiricalFact@1.0.0",
                                 "exact source_scope/replay/provenance refs"],
            "source_id": spec.source_id,
            "state": "PREREGISTERED_PENDING_ACTUAL_SOURCE",
        },
        {
            "consumer_id": "F2_DISCOVERY_AND_NO_DROP",
            "owner": "rawlsing_next.pre553_carrier_execution.CarrierNeutralResearchExecutor.execute_i05; rawlsing_next.universal_grammar.native_map.native_receipt_anti_join",
            "required_outputs": ["DiscoveryResultReceipt@1.0.0", "complete declared-frontier candidate accounting",
                                 "no missing/duplicate/unexpected candidates", "typed negative receipts where applicable"],
            "source_id": spec.source_id,
            "state": "PREREGISTERED_PENDING_ACTUAL_SOURCE",
        },
        {
            "consumer_id": "F3_M1_LEARNED_DISPOSITION",
            "owner": "rawlsing_next.pre553_learned_empirical_adjudication.adjudicate_learned_empirical",
            "required_outputs": ["M1AdjudicationInputBundle", "exact family-rule binding",
                                 "LearnedEmpiricalDisposition@1.0.0"],
            "source_id": spec.source_id,
            "state": "PREREGISTERED_PENDING_EXACT_FAMILY_RULE_AND_EMPIRICAL_EVIDENCE",
        },
        {
            "consumer_id": "F4_FF_V553_CONFRONTATION",
            "owner": "rawlsing_next.pre553_universal_empirical_extension.provide_empirical_possibility_slice_ext",
            "required_outputs": ["exact I03/I05 evidence", "M1 disposition", "source-local permitted FF/V553 inputs",
                                 "explicit refusal/typed absence when source-local law is not satisfied"],
            "source_id": spec.source_id,
            "state": "PREREGISTERED_PENDING_UPSTREAM_EVIDENCE_AND_SEPARATE_USE_AUTHORITY",
        },
    ]


def build_preparation(spec: DictionarySpec) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw, rows, fields = _read_pinned_dictionary(spec)
    accounts = [_row_account(spec, index, row) for index, row in enumerate(rows, 1)]
    codes = [row["var_name"] for row in rows]
    duplicates = sorted({code for code in codes if codes.count(code) > 1})
    if duplicates:
        raise PackageBindingRefusal("DICTIONARY_DUPLICATE_NATIVE_CODES", repr(duplicates))
    counts: dict[str, int] = {}
    for account in accounts:
        counts[account["role_proposal"]] = counts.get(account["role_proposal"], 0) + 1
    freeze_ref = _ref("R145_METADATA_FREEZE", f"{spec.source_id}-dictionary", {
        "source": spec.source_id, "family": spec.family, "wave": spec.wave,
        "sha256": spec.sha256, "bytes": spec.bytes, "columns": fields,
    })
    dictionary_ref = _ref("R145_CODEBOOK_DOCUMENT", f"{spec.source_id}-codebook", {
        "sha256": spec.sha256, "bytes": spec.bytes, "source": spec.source_id,
    })
    preparation = {
        "schema": SCHEMA,
        "status": "PENDING_AUTHORIZED_SOURCE_METADATA_RECEIPT__NO_SURVEY_FILE_OPENED",
        "source_id": spec.source_id,
        "family": spec.family,
        "wave": spec.wave,
        "source_format": spec.source_format,
        "source_unit": _source_unit(rows),
        "dictionary": {
            "filename": spec.metadata_path.name,
            "sha256": spec.sha256,
            "bytes": spec.bytes,
            "rows": len(rows),
            "duplicate_native_codes": duplicates,
            "columns": fields,
            "document_ref": dictionary_ref.as_dict(),
            "scope": spec.scope,
        },
        "row_accounting": {
            "total_rows": len(accounts),
            "retained_rows": sum(1 for account in accounts if account["retained"]),
            "role_counts": dict(sorted(counts.items())),
            "row_records_path": f"records/{spec.source_id}_ROW_ACCOUNTING.jsonl",
            "all_rows_retained": True,
        },
        "edition_sha256": None,
        "edition_sha256_status": PENDING,
        "survey_locator_requested_for_metadata_only": spec.survey_locator,
        "survey_file_touched": False,
        "source_read_request_template": {
            "source_id": spec.source_id,
            "source_sha256": None,
            "source_sha256_status": PENDING,
            "source_format": spec.source_format,
            "custody_locator_binding": "PENDING_AUTHORIZED_SOURCE_IDENTITY_RECEIPT",
            "host": "PENDING_EXTERNAL_TRUSTED_SOURCE_READ_DECISION",
            "purpose": "R145_CURRENT_SOURCE_PACKAGE_PREPARATION",
            "consumer_use": "R134_SOURCE_LOCAL_EMPIRICAL_AND_LEARNED_PIPELINE",
            "read_operation": SOURCE_READ_OPERATION,
            "physical_read_extent": EXACT_FILE,
            "metadata_freeze_refs": [freeze_ref.as_dict()],
            "semantic_use_scope": ["SOURCE_LOCAL_ONLY", "NO_POPULATION_OR_CAUSAL_INFERENCE"],
            "status": "TEMPLATE_ONLY_DO_NOT_SEND_UNTIL_EDITION_SHA_AND_EXTERNAL_GRANT",
        },
        "prospective_source_role_contract": {
            "role_source": "row evidence; module_guess is only one retained evidence field",
            "scientific_target_conditioner_roles": "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY",
            "topology": "UNRESOLVED_PENDING_HEADER_AND_SEMANTIC_AUTHORITY",
            "eligible_work": {
                "substantive_question_candidates": counts.get("SUBSTANTIVE_QUESTION_CANDIDATE", 0),
                "all_retained_rows": len(accounts),
                "operations_compiled": 0,
                "reason": "source identity/header, value semantics, roles and U/Epre are not yet bound",
            },
            "native_owner_refs": [
                "rawlsing_next.pre553_source_native_preimage_adapter.NativeSourcePackage",
                "rawlsing_next.pre553_source_native_preimage_adapter.materialize_native_preimages",
                "rawlsing_next.universal_grammar.types.SourceInventory",
                "rawlsing_next.pre553_source_local_universe_admission.materialize_source_local_universe",
                "rawlsing_next.pre553_native_workload_binding.build_frontier_native_catalog",
                "rawlsing_next.pre553_universal_workload.compile_governed_frontier",
            ],
            "u_e_pre": {
                "u_root": None,
                "e_pre_root": None,
                "status": "PENDING_AUTHORIZED_SOURCE_IDENTITY_AND_ROLE_SEMANTICS",
            },
        },
        "producer_product_learned_ff_sequence": [
            {"step": 1, "owner": "R145 source_package_binder", "output": "metadata preparation + full row accounting", "state": "READY_FROM_DICTIONARY"},
            {"step": 2, "owner": "external source identity/header grant", "output": "authorized metadata receipt + NativeSourceIdentity", "state": PENDING},
            {"step": 3, "owner": "rawlsing_next.pre553_source_read_admission", "output": "authorized whole-file incidence", "state": "PENDING_SEPARATE_RESPONSE_GRANT"},
            {"step": 4, "owner": "rawlsing_next.pre553_source_native_preimage_adapter.materialize_native_preimages", "output": "source-native bundle/projection", "state": "PENDING_HEADER_AND_SEMANTICS"},
            {"step": 5, "owner": "R01 SourceInventory/GrammarPolicy/frontier + build_frontier_native_catalog", "output": "exact query/discovery plan", "state": "PENDING_SOURCE_ROLES_AND_U_EPRE"},
            {"step": 6, "owner": "I03/I05/Batch", "output": "EmpiricalFact + DiscoveryResultReceipt + no-drop ledger", "state": "PENDING_ACTUAL_EXECUTION"},
            {"step": 7, "owner": "pre553_learned_empirical_adjudication.adjudicate_learned_empirical", "output": "LearnedEmpiricalDisposition (M1)", "state": "PENDING_FAMILY_RULE"},
            {"step": 8, "owner": "pre553_learned_product_release + pre553_universal_empirical_extension", "output": "separately governed learned/product/FF-V553 receiving use", "state": "PENDING_SEPARATE_USE_AUTHORITY"},
        ],
        "consumer_requirements": _consumer_requirements(spec),
        "missing_prerequisites": [
            "user-authorized survey identity/header metadata receipt with exact edition SHA",
            "physical header-vs-codebook reconciliation and typed row accounting",
            "exact source read grant/resolver for response decode; metadata receipt alone is insufficient",
            "exact source semantic roles/topology, U/Epre and design/weight/country/population/time authority",
            "exact empirical query/fact and frontier candidate law for this source",
            "M1 family rule/binding and separate FF/V553 receiving-use authority",
        ],
        "next_call": {
            "command": "python3 runtime/bind_authorized_metadata_receipt.py --scope .r61/r145-current-source-packages/inputs/METADATA_INPUTS.json --source-id <SRC> --receipt <authorized_metadata_receipt.json>",
            "requires": "externally authorized metadata/header receipt; no raw response open",
        },
    }
    return preparation, accounts, freeze_ref


def _native_identity_from_receipt(spec: DictionarySpec, receipt: Mapping[str, Any]) -> NativeSourceIdentity:
    required = {
        "schema", "source_id", "family", "wave", "edition_sha256", "source_format",
        "dictionary_sha256", "header_variables", "row_count", "authority_state",
        "issuer_ref", "source_identity_receipt_ref",
    }
    missing = required - set(receipt)
    if missing:
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_MISSING", repr(sorted(missing)))
    if receipt["authority_state"] != "EXTERNALLY_AUTHORIZED_METADATA_ONLY":
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_NOT_AUTHORIZED")
    for key, expected in (
        ("source_id", spec.source_id), ("family", spec.family), ("wave", spec.wave),
        ("dictionary_sha256", spec.sha256), ("source_format", spec.source_format),
    ):
        if receipt[key] != expected:
            raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_MISMATCH", key)
    sha = str(receipt["edition_sha256"])
    if len(sha) != 64 or sha.lower() != sha or any(c not in "0123456789abcdef" for c in sha):
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_EDITION_SHA_INVALID")
    header = receipt["header_variables"]
    if not isinstance(header, list) or not header or any(not isinstance(x, str) or not x for x in header):
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_HEADER_INVALID")
    row_count = receipt["row_count"]
    if not isinstance(row_count, int) or isinstance(row_count, bool) or row_count < 1:
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_ROW_COUNT_INVALID")
    return NativeSourceIdentity(
        source_id=spec.source_id, family=spec.family, wave=spec.wave,
        canonical_filename=Path(spec.survey_locator).name, declared_sha256=sha,
        source_format=spec.source_format, expected_rows=row_count,
    )


def bind_authorized_metadata_receipt(
    spec: DictionarySpec, receipt: Mapping[str, Any], *, codebook_variables: Sequence[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(receipt, Mapping):
        raise PackageBindingRefusal("AUTHORIZED_METADATA_RECEIPT_MAPPING_REQUIRED")
    identity = _native_identity_from_receipt(spec, receipt)
    header = tuple(receipt["header_variables"])
    if codebook_variables is not None:
        known = set(codebook_variables)
        added = tuple(sorted(set(header) - known))
        absent = tuple(sorted(known - set(header)))
    else:
        added, absent = (), ()
    return {
        "schema": "PYAT_R145_AUTHORIZED_METADATA_BINDING@1",
        "source_id": spec.source_id,
        "native_source_identity": {
            "source_id": identity.source_id, "family": identity.family, "wave": identity.wave,
            "canonical_filename": identity.canonical_filename,
            "declared_sha256": identity.declared_sha256,
            "source_format": identity.source_format, "expected_rows": identity.expected_rows,
        },
        "header_variable_count": len(header),
        "header_codes_added_beyond_codebook": list(added),
        "codebook_variables_absent_from_header": list(absent),
        "reconciliation_state": ("EXACT_HEADER_CODEBOOK" if not added and not absent
                                 else "HEADER_CODEBOOK_MISMATCH_RETAINED_FOR_HQ"),
        "survey_file_touched": False,
        "response_decode_authorized": False,
        "source_read_grant_present": False,
        "next_gate": "SOURCE_RESPONSE_DECODE_REQUIRES_EXTERNAL_EXACT_GRANT_AND_CURRENT_RESOLVER",
    }


def build_all(scope_path: str | Path, output_root: str | Path) -> dict[str, Any]:
    specs = load_metadata_scope(scope_path)
    out = Path(output_root)
    out.mkdir(parents=True, exist_ok=True)
    records = out / "records"
    records.mkdir(exist_ok=True)
    results = []
    for spec in specs:
        preparation, accounts, _freeze = build_preparation(spec)
        row_path = records / f"{spec.source_id}_ROW_ACCOUNTING.jsonl"
        with row_path.open("w", encoding="utf-8") as handle:
            for account in accounts:
                handle.write(_canonical(account) + "\n")
        (records / f"{spec.source_id}_PACKAGE_PREPARATION.json").write_text(
            json.dumps(preparation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        results.append({
            "source_id": spec.source_id, "family": spec.family, "wave": spec.wave,
            "dictionary_sha256": spec.sha256, "rows": len(accounts),
            "role_counts": preparation["row_accounting"]["role_counts"],
            "preparation_record": f"records/{spec.source_id}_PACKAGE_PREPARATION.json",
            "row_accounting": f"records/{spec.source_id}_ROW_ACCOUNTING.jsonl",
        })
    summary = {
        "schema": "PYAT_R145_METADATA_PACKAGE_SUMMARY@1",
        "status": "METADATA_PREPARATION_COMPLETE__SOURCE_ACCESS_AND_SEMANTICS_PENDING",
        "source_count": len(results),
        "sources": results,
        "survey_files_touched": 0,
        "source_read_grants_created": 0,
        "native_preimage_bundles_created": 0,
        "limits": ["dictionary documents only", "no raw survey file", "no source/science grant"],
    }
    (records / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary
