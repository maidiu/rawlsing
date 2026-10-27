"""Bounded Campaign A1 SRC04 original-source C11 runner.

This runner reads only the user-authorized SRC04 file through the existing
source-read admission and SHA-checked physical decoder.  It constructs a
source-native C11LogicalRelease over a transparent eligible configured slice.
It does not issue an empirical workload and does not commit source cells or
row-wise response artifacts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import replace
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_c11_integrity import (
    C11IntegrityError,
    QuestionVariableBinding,
    RespondentIdentity,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    ExactRef,
    RespondentEvent,
    WeightMeasureFact,
    semantic_hash,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    physical_value_binding_key,
)
from rawlsing_next.pre553_source_read_admission import (
    CURRENT_GRANTED,
    EXACT_FILE,
    SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision,
    SourceReadAdmissionRefusal,
    SourceReadRequest,
    decode_with_source_read_permission,
)
from rawlsing_next.source_configuration.factory import (
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.reader import (
    decode_config_with_source_read_permission,
    reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import (
    SourceConfig,
    canonical_config_hash,
    load_source_config,
)

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = Path(__file__).resolve().parent
EVIDENCE = CAMPAIGN / "evidence"
CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
CROSSWALK_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/crosswalk.json"
METADATA_PATH = ROOT / "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/SRC04_PHYSICAL_METADATA.json"
PROGRAM_PATH = EVIDENCE / "PROGRAM.txt"
COMMITTED_GRANT_PATH = EVIDENCE / "USER_GRANT.json"

SOURCE_ID = "SRC04"
EXPECTED_SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
EXPECTED_SOURCE_ROWS = 7337
EXPECTED_SOURCE_COLUMNS = 181
EXPECTED_RESPONSE_SLOTS = 178
EXPECTED_COORDINATE_SLOTS = 3
EXPECTED_CONFIG_FILE_SHA256 = "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900"
EXPECTED_CONFIG_CANONICAL_SHA256 = "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
EXPECTED_METADATA_SHA256 = "6b98d33a8c7598934fcad38cecb3b23e0db7a3031990b302c3df113d295351fb"
EXPECTED_GRANT_SHA256 = "feb8320a149315fdfe74ae97f0aa91a3720aa141e5a1d5cbd5e2b97746c594f1"
EXPECTED_PROGRAM_SHA256 = "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
CONTROL_COMMIT = "2d2814df614018dbca5687839fe562d16bf900e7"
SLICE_MAX_ORDINAL = 45
SEMANTIC_USE_SCOPE = (
    "SOURCE_NATIVE_RESPONSE_INCIDENCE",
    "NO_SEMANTIC_ADOPTION",
    "SRC04",
    "CAMPAIGN_A1",
)
SOURCE_PATH_SENTINEL = "/nonexistent/campaign-a-src04-wrong-source.sav"

PRIMARY_RUN_PATH = EVIDENCE / "PRIMARY_RUN.json"
RELEASE_RECEIPT_PATH = EVIDENCE / "RELEASE_RECEIPT.json"
LOCAL_RECEIPT_PATH = EVIDENCE / "LOCAL_RELEASE_RECEIPT.json"
REPLAY_PATH = EVIDENCE / "REPLAY_RECEIPT.json"
RETURN_PATH = CAMPAIGN / "RETURN.json"
TEST_RESULTS_PATH = EVIDENCE / "TEST_RESULTS.json"


class CampaignError(RuntimeError):
    pass


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def jsonable(value: Any) -> Any:
    if isinstance(value, ExactRef):
        return value.as_dict()
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if isinstance(value, Mapping):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def _norm_vl(value: Any) -> dict[str, str]:
    result = {}
    for key, label in (value or {}).items():
        try:
            key_text = str(int(float(key)))
        except (TypeError, ValueError):
            key_text = str(key)
        result[key_text] = str(label)
    return result


def _grant_paths() -> tuple[Path, list[dict[str, Any]]]:
    path = COMMITTED_GRANT_PATH
    if not path.is_file():
        raise CampaignError("committed authorized USER_GRANT.json is absent")
    grant_sha = sha_file(path)
    if grant_sha != EXPECTED_GRANT_SHA256:
        raise CampaignError("USER_GRANT hash mismatch")
    if not PROGRAM_PATH.is_file():
        raise CampaignError("committed governing PROGRAM.txt is absent")
    program_sha = sha_file(PROGRAM_PATH)
    if program_sha != EXPECTED_PROGRAM_SHA256:
        raise CampaignError("governing PROGRAM SHA mismatch")
    return path, [{"path": str(path), "role": "COMMITTED_EVIDENCE", "sha256": grant_sha}]


def load_grant() -> dict[str, Any]:
    primary, copies = _grant_paths()
    document = load_json(primary)
    if document.get("source_id") != SOURCE_ID:
        raise CampaignError("grant source_id is not SRC04")
    if document.get("expected_source_sha256") != EXPECTED_SOURCE_SHA256:
        raise CampaignError("grant source SHA does not match canonical SRC04 identity")
    if document.get("host") != "USER_LOCAL_MAC":
        raise CampaignError("grant host is not the authorized local host")
    if document.get("purpose") != "FIRST_ORIGINAL_SOURCE_C11_POSITIVE":
        raise CampaignError("grant purpose mismatch")
    if document.get("consumer") != "EXISTING_PRE553_SOURCE_BACKED_C11":
        raise CampaignError("grant consumer mismatch")
    if not document.get("user_authorization") or not document.get("authorization_context"):
        raise CampaignError("grant lacks explicit authorization evidence")
    # No source stat/hash/open occurs here. The exact source identity is checked
    # by the SHA-qualified decoder only after the current resolver admits the read.
    source_path = Path(document["source_path"])
    grant_ref = ExactRef("USER_SOURCE_READ_GRANT",
                         "urn:rawlsing:campaign-a:src04:USER_GRANT",
                         EXPECTED_GRANT_SHA256)
    decision_ref = ExactRef(
        "USER_SOURCE_READ_DECISION",
        "urn:rawlsing:campaign-a:src04:USER_GRANT:decision",
        semantic_hash({
            "grant_sha256": EXPECTED_GRANT_SHA256,
            "program_sha256": EXPECTED_PROGRAM_SHA256,
            "control_commit": CONTROL_COMMIT,
            "source_id": SOURCE_ID,
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "read_operation": SOURCE_RESPONSE_DECODE,
            "physical_read_extent": EXACT_FILE,
        }),
    )
    return {
        "document": document,
        "primary_path": str(primary),
        "copies": copies,
        "grant_ref": grant_ref,
        "decision_ref": decision_ref,
        "source_path": source_path,
        "program_sha256": EXPECTED_PROGRAM_SHA256,
        "control_commit": CONTROL_COMMIT,
    }


def make_request(config: SourceConfig, grant: Mapping[str, Any]) -> SourceReadRequest:
    document = grant["document"]
    return source_read_request_from_config(
        config,
        host=document["host"],
        purpose=document["purpose"],
        consumer_use=document["consumer"],
        semantic_use_scope=SEMANTIC_USE_SCOPE,
    )


def make_decision(request: SourceReadRequest, grant: Mapping[str, Any]) -> IssuedSourceReadDecision:
    return IssuedSourceReadDecision(
        decision_ref=grant["decision_ref"],
        source_permission_refs=(grant["grant_ref"],),
        source_id=request.source_id,
        source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        read_operation=SOURCE_RESPONSE_DECODE,
        physical_read_extent=EXACT_FILE,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-10-27/USER_GRANT_PINNED_CONTROL_2d2814",
        currentness=CURRENT_GRANTED,
        revocation_ref=None,
        retention_export_limits={
            "export": "DENY",
            "rowwise_response_artifacts": "DENY",
            "retention": "LOCAL_RUNTIME_ONLY",
            "source_bytes_in_git": "DENY",
        },
    )


class AuthenticatedUserGrantResolver:
    """Bounded adapter authenticating this exact immutable user grant."""

    def __init__(self, grant: Mapping[str, Any], request: SourceReadRequest):
        self.grant = grant
        self.request = request
        self.calls = 0
        self.decision = make_decision(request, grant)

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        self.calls += 1
        if request != self.request:
            raise SourceReadAdmissionRefusal("USER_GRANT_REQUEST_MISMATCH")
        for copy in self.grant["copies"]:
            path = Path(copy["path"])
            if not path.is_file() or sha_file(path) != EXPECTED_GRANT_SHA256:
                raise SourceReadAdmissionRefusal("USER_GRANT_CURRENTNESS_MISMATCH")
        if not PROGRAM_PATH.is_file() or sha_file(PROGRAM_PATH) != EXPECTED_PROGRAM_SHA256:
            raise SourceReadAdmissionRefusal("PROGRAM_CURRENTNESS_MISMATCH")
        return self.decision


def wrong_source_negative(config: SourceConfig, grant: Mapping[str, Any]) -> dict[str, Any]:
    request = make_request(config, grant)
    resolver = AuthenticatedUserGrantResolver(grant, request)
    decision = resolver.decision
    wrong = replace(decision, source_sha256="0" * 64)
    class _WrongResolver:
        calls = 0
        def resolve_current(self, req: SourceReadRequest):
            self.calls += 1
            return wrong
    wrong_resolver = _WrongResolver()
    result = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_WRONG_SOURCE_NEGATIVE@1.0.0",
        "source_id": SOURCE_ID,
        "requested_source_sha256": request.source_sha256,
        "wrong_decision_source_sha256": "0" * 64,
        "source_path_sentinel": SOURCE_PATH_SENTINEL,
        "source_read_performed": False,
        "resolver_calls": 0,
    }
    try:
        decode_with_source_read_permission(
            source_path=SOURCE_PATH_SENTINEL,
            request=request,
            resolver=wrong_resolver,
            reader=reader_configuration_from_config(config),
        )
    except SourceReadAdmissionRefusal as exc:
        result.update({
            "status": "REFUSED",
            "refusal_code": exc.code,
            "refusal_detail": exc.detail,
            "resolver_calls": wrong_resolver.calls,
            "before_source_io": True,
        })
        return result
    raise CampaignError("wrong-source negative was not refused")


def decode_original(config: SourceConfig, grant: Mapping[str, Any]) -> tuple[Any, dict[str, Any]]:
    request = make_request(config, grant)
    resolver = AuthenticatedUserGrantResolver(grant, request)
    started = time.monotonic()
    incidence = decode_config_with_source_read_permission(
        config,
        source_path=grant["source_path"],
        resolver=resolver,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        semantic_use_scope=SEMANTIC_USE_SCOPE,
    )
    elapsed = round(time.monotonic() - started, 3)
    return incidence, {
        "source_id": incidence.source_sha256 and SOURCE_ID,
        "source_sha256": incidence.source_sha256,
        "source_format": incidence.source_format,
        "rows": incidence.row_count,
        "columns": len(incidence.variables),
        "decoder": "rawlsing_next.pre553_physical_decoder.decode_sav",
        "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
        "transport": "rawlsing_next.source_configuration.reader.decode_config_with_source_read_permission",
        "resolver_calls": resolver.calls,
        "decision_ref": grant["decision_ref"].as_dict(),
        "reader_configuration": dict(incidence.reader_configuration),
        "source_custody": dict(incidence.source_custody or {}),
        "physical_metadata_digest": incidence.physical_metadata_digest,
        "file_metadata": {
            "number_rows": incidence.file_metadata.get("number_rows"),
            "number_columns": incidence.file_metadata.get("number_columns"),
            "file_format": incidence.file_metadata.get("file_format"),
            "file_encoding": incidence.file_metadata.get("file_encoding"),
            "decoder_identity": incidence.file_metadata.get("decoder_identity"),
        },
        "read_elapsed_seconds": elapsed,
        "source_read_performed": True,
    }


def physical_audit(config: SourceConfig, incidence: Any) -> dict[str, Any]:
    document = config.document
    config_slots = {int(x["ordinal"]): x for x in document["physical_slots"]}
    actual = {int(v.ordinal): v for v in incidence.variables}
    metadata_document = load_json(METADATA_PATH)
    metadata = metadata_document["metadata"]
    crosswalk = load_json(CROSSWALK_PATH)
    crosswalk_by_ordinal = {int(x["physical_ordinal"]): x for x in crosswalk["entries"]}
    metadata_ref = document["identity"]["metadata_witness_ref"]
    meta_sha = sha_file(METADATA_PATH)
    checks = {
        "metadata_witness_sha_matches_config": meta_sha == metadata_ref["content_hash"] == EXPECTED_METADATA_SHA256,
        "metadata_witness_source_sha_matches": metadata_document.get("sha256") == EXPECTED_SOURCE_SHA256,
        "metadata_witness_rows": metadata.get("number_rows") == EXPECTED_SOURCE_ROWS,
        "metadata_witness_columns": metadata.get("number_columns") == EXPECTED_SOURCE_COLUMNS,
        "source_sha_matches": incidence.source_sha256 == EXPECTED_SOURCE_SHA256,
        "source_rows_match": incidence.row_count == EXPECTED_SOURCE_ROWS,
        "source_columns_match": len(incidence.variables) == EXPECTED_SOURCE_COLUMNS,
        "ordinal_set_matches": set(actual) == set(config_slots),
        "crosswalk_entries": len(crosswalk_by_ordinal) == len(config_slots) == 181,
        "crosswalk_exact_names_labels": True,
        "config_names_match_actual": True,
        "config_storage_types_match_actual": True,
        "config_labels_match_actual": True,
        "config_value_labels_match_actual": True,
        "config_missing_declarations_match_actual": True,
        "metadata_names_match_actual": True,
        "metadata_labels_match_actual": True,
        "metadata_value_labels_match_actual": True,
        "metadata_storage_types_match_actual": True,
        "items_count": len(document["items"]) == 181,
        "items_unique": len({x["implementation_id"] for x in document["items"]}) == 181,
        "items_cover_all_slots": {x["source_variable_code"] for x in document["items"]} ==
                                {x["name"] for x in document["physical_slots"]},
    }
    issues = []
    meta_names = list(metadata.get("column_names") or [])
    meta_labels = metadata.get("column_names_to_labels") or {}
    meta_types = metadata.get("readstat_variable_types") or {}
    meta_vl = metadata.get("variable_value_labels") or {}
    for ordinal in sorted(config_slots):
        slot = config_slots[ordinal]
        var = actual.get(ordinal)
        cw = crosswalk_by_ordinal.get(ordinal, {})
        if var is None:
            issues.append(f"missing actual ordinal {ordinal}")
            continue
        if slot["name"] != var.name:
            checks["config_names_match_actual"] = False
            issues.append(f"name mismatch ordinal {ordinal}")
        if slot["storage_type"] != var.storage_type:
            checks["config_storage_types_match_actual"] = False
            issues.append(f"storage mismatch {slot['name']}")
        if slot["label"] != var.variable_label:
            checks["config_labels_match_actual"] = False
            issues.append(f"label mismatch {slot['name']}")
        if _norm_vl(slot.get("value_labels")) != _norm_vl(var.value_labels):
            checks["config_value_labels_match_actual"] = False
            issues.append(f"value labels mismatch {slot['name']}")
        if (slot.get("missing_declarations") or []) != list(var.missing_declarations or []):
            checks["config_missing_declarations_match_actual"] = False
            issues.append(f"missing declarations mismatch {slot['name']}")
        if cw.get("physical_name") != var.name or cw.get("physical_label") != var.variable_label:
            checks["crosswalk_exact_names_labels"] = False
            issues.append(f"crosswalk mismatch {slot['name']}")
        if ordinal - 1 >= len(meta_names) or meta_names[ordinal - 1] != var.name:
            checks["metadata_names_match_actual"] = False
            issues.append(f"metadata name mismatch {slot['name']}")
        if meta_labels.get(var.name) != var.variable_label:
            checks["metadata_labels_match_actual"] = False
            issues.append(f"metadata label mismatch {slot['name']}")
        if meta_types.get(var.name) != var.storage_type:
            checks["metadata_storage_types_match_actual"] = False
            issues.append(f"metadata storage mismatch {slot['name']}")
        if _norm_vl(meta_vl.get(var.name)) != _norm_vl(var.value_labels):
            checks["metadata_value_labels_match_actual"] = False
            issues.append(f"metadata value labels mismatch {slot['name']}")
    result = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_PHYSICAL_METADATA_AUDIT@1.0.0",
        "source_id": SOURCE_ID,
        "source_sha256": incidence.source_sha256,
        "rows": incidence.row_count,
        "columns": len(incidence.variables),
        "metadata_witness_path": str(METADATA_PATH.relative_to(ROOT)),
        "metadata_witness_sha256": meta_sha,
        "config_path": str(CONFIG_PATH.relative_to(ROOT)),
        "config_file_sha256": sha_file(CONFIG_PATH),
        "config_canonical_sha256": canonical_config_hash(config),
        "crosswalk_path": str(CROSSWALK_PATH.relative_to(ROOT)),
        "crosswalk_file_sha256": sha_file(CROSSWALK_PATH),
        "physical_metadata_digest": incidence.physical_metadata_digest,
        "checks": checks,
        "issues": issues[:50],
        "issue_count": len(issues),
        "passed": all(checks.values()) and not issues,
        "source_read_performed": True,
    }
    write_json(EVIDENCE / "PHYSICAL_METADATA_AUDIT.json", result)
    if not result["passed"]:
        raise CampaignError("physical metadata/source-native code agreement failed")
    return result


def scan_slots(config: SourceConfig, incidence: Any) -> dict[str, Any]:
    document = config.document
    response_slots = {int(x["slot"]["ordinal"]): x for x in document["response_slots"]}
    coordinate_slots = {int(x["slot"]["ordinal"]): x for x in document["coordinate_slots"]}
    response_keys = {
        ordinal: {physical_value_binding_key(v["raw_value"], v["missing_state"], v.get("source_missing_declaration"))
                  for v in section["values"]}
        for ordinal, section in response_slots.items()
    }
    coordinate_keys = {
        ordinal: {physical_value_binding_key(v["raw_value"], v["missing_state"], v.get("source_missing_declaration"))
                  for v in section.get("values", [])}
        for ordinal, section in coordinate_slots.items()
    }
    response_counts = {ordinal: {"cells": 0, "unbound": 0, "missing": 0} for ordinal in response_slots}
    coordinate_counts = {ordinal: {"cells": 0, "unbound": 0, "missing": 0} for ordinal in coordinate_slots}
    all_cells = 0
    for cell in incidence.iter_cells():
        all_cells += 1
        ordinal = cell.variable_ordinal
        key = physical_value_binding_key(cell.raw_value, cell.missing_state, cell.source_missing_declaration)
        if ordinal in response_counts:
            response_counts[ordinal]["cells"] += 1
            if cell.missing_state.value != "OBSERVED_STORAGE_VALUE":
                response_counts[ordinal]["missing"] += 1
            if key not in response_keys[ordinal]:
                response_counts[ordinal]["unbound"] += 1
        if ordinal in coordinate_counts:
            coordinate_counts[ordinal]["cells"] += 1
            if cell.missing_state.value != "OBSERVED_STORAGE_VALUE":
                coordinate_counts[ordinal]["missing"] += 1
            if key not in coordinate_keys[ordinal]:
                coordinate_counts[ordinal]["unbound"] += 1
    complete_response = [o for o in sorted(response_slots) if response_counts[o]["unbound"] == 0]
    selected_response = [o for o in complete_response if o <= SLICE_MAX_ORDINAL]
    selected_coordinate = []
    for ordinal in sorted(coordinate_slots):
        section = coordinate_slots[ordinal]
        count = coordinate_counts[ordinal]
        if count["unbound"] == 0 and count["missing"] == 0:
            selected_coordinate.append(ordinal)
        elif section.get("copy_observed_raw") and count["missing"] == 0:
            selected_coordinate.append(ordinal)
    response_rows = []
    for ordinal in sorted(response_slots):
        count = response_counts[ordinal]
        if ordinal in selected_response:
            status = "INCLUDED_IN_FIRST_ELIGIBLE_SLICE"
            reason = "all observed values/states have exact configured bindings; ordinal in first configured battery (3..45)"
        elif count["unbound"]:
            status = "EXCLUDED_UNBOUND_OBSERVED_VALUES"
            reason = "observed source value/state has no exact configured value rule"
        else:
            status = "ELIGIBLE_COMPLETE_NOT_INCLUDED_BOUNDED_FIRST_SLICE"
            reason = "complete binding but outside the bounded first-battery ordinal range; not a semantic gap"
        response_rows.append({
            "ordinal": ordinal,
            "name": response_slots[ordinal]["slot"]["name"],
            "question_id": response_slots[ordinal]["question_id"],
            "cells": count["cells"],
            "unbound_cells": count["unbound"],
            "nonobserved_cells": count["missing"],
            "status": status,
            "reason": reason,
        })
    coordinate_rows = []
    for ordinal in sorted(coordinate_slots):
        count = coordinate_counts[ordinal]
        section = coordinate_slots[ordinal]
        if ordinal in selected_coordinate:
            status = "INCLUDED_IN_FIRST_ELIGIBLE_SLICE"
            reason = "all observed values are copyable with the exact configured coordinate rule"
        else:
            status = "EXCLUDED_UNBOUND_OR_MISSING_COORDINATE"
            reason = "observed coordinate value or missing cell is not fully bound by the configured rule"
        coordinate_rows.append({
            "ordinal": ordinal,
            "name": section["slot"]["name"],
            "cells": count["cells"],
            "unbound_cells": count["unbound"],
            "nonobserved_cells": count["missing"],
            "copy_observed_raw": bool(section.get("copy_observed_raw")),
            "status": status,
            "reason": reason,
        })
    selected_qids = [response_slots[o]["question_id"] for o in selected_response]
    selection = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_ELIGIBLE_SLICE@1.0.0",
        "source_id": SOURCE_ID,
        "source_sha256": incidence.source_sha256,
        "rows": incidence.row_count,
        "physical_cells": all_cells,
        "configured": {
            "physical_slots": len(document["physical_slots"]),
            "items": len(document["items"]),
            "response_slots": len(response_slots),
            "coordinate_slots": len(coordinate_slots),
            "weight_slots": len(document["weight_slots"]),
        },
        "selected_response_slots": selected_response,
        "selected_response_question_ids": selected_qids,
        "selected_coordinate_slots": selected_coordinate,
        "response_slots": response_rows,
        "coordinate_slots": coordinate_rows,
        "incomplete_response_slots": [o for o in sorted(response_slots) if response_counts[o]["unbound"]],
        "incomplete_coordinate_slots": [
            o for o in sorted(coordinate_slots)
            if not (coordinate_counts[o]["unbound"] == 0 or
                    (coordinate_slots[o].get("copy_observed_raw") and coordinate_counts[o]["missing"] == 0))],
        "complete_response_slots": complete_response,
        "accounting": {
            "all_181_physical_slots_accounted": len(response_rows) + len(coordinate_rows) == 181,
            "all_178_response_slots_accounted": len(response_rows) == 178,
            "all_3_coordinate_slots_accounted": len(coordinate_rows) == 3,
            "selected_response_slots": len(selected_response),
            "excluded_unbound_response_slots": len([x for x in response_rows if x["status"] == "EXCLUDED_UNBOUND_OBSERVED_VALUES"]),
            "eligible_complete_response_not_selected": len([x for x in response_rows if x["status"] == "ELIGIBLE_COMPLETE_NOT_INCLUDED_BOUNDED_FIRST_SLICE"]),
            "selected_coordinate_slots": len(selected_coordinate),
            "excluded_coordinate_slots": len(coordinate_rows) - len(selected_coordinate),
            "held_slots_in_source_config": 0,
        },
        "selection_rule": "first configured response battery ordinals 3..45 with every observed value/state exactly bound; coordinates only when their configured rule fully covers observed/missing cells",
        "source_read_performed": True,
    }
    write_json(EVIDENCE / "SLICE_SELECTION.json", selection)
    return selection


def build_slice_config(config: SourceConfig, selection: Mapping[str, Any], *, strip_canonical: bool,
                       override_response: Sequence[int] | None = None) -> tuple[SourceConfig, int]:
    document = deepcopy(config.document)
    selected_response = list(override_response if override_response is not None else
                             selection["selected_response_slots"])
    selected_coordinate = list(selection["selected_coordinate_slots"])
    response = [x for x in document["response_slots"] if int(x["slot"]["ordinal"]) in selected_response]
    qids = {x["question_id"] for x in response}
    document["response_slots"] = response
    document["coordinate_slots"] = [x for x in document["coordinate_slots"]
                                    if int(x["slot"]["ordinal"]) in selected_coordinate]
    document["questions"] = [x for x in document["questions"] if x["question_id"] in qids]
    document["routing"] = [x for x in document["routing"] if x["question_id"] in qids]
    document["supported_scope"]["supported_question_ids"] = [
        x for x in document["supported_scope"]["supported_question_ids"] if x in qids]
    withheld = 0
    if strip_canonical:
        for slot in document["response_slots"]:
            for value in slot["values"]:
                if value.get("canonical_value") is not None or value.get("transform_authority_ref") is not None:
                    withheld += 1
                value["canonical_value"] = None
                value["transform_authority_ref"] = None
                value["extra_authority_refs"] = []
    return SourceConfig(document), withheld


def canonical_negative(config: SourceConfig, selection: Mapping[str, Any], incidence: Any) -> dict[str, Any]:
    q101 = next(x for x in selection["response_slots"] if x["question_id"] == "q101")
    slice_config, _ = build_slice_config(config, selection, strip_canonical=False,
                                         override_response=[q101["ordinal"]])
    result = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_CANONICAL_AUTHORITY_NEGATIVE@1.0.0",
        "source_id": SOURCE_ID,
        "selected_response_slot": q101["ordinal"],
        "selected_question_id": "q101",
        "canonical_values_retained": True,
        "source_read_performed": True,
    }
    try:
        release = build_validated_c11_release_from_config(slice_config, incidence=incidence)
    except Exception as exc:  # exact owner refusal is the evidence
        result.update({
            "status": "REFUSED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "release_created": False,
        })
        write_json(EVIDENCE / "NEGATIVE_CANONICAL_AUTHORITY.json", result)
        return result
    result.update({"status": "UNEXPECTED_SUCCESS", "release_ref": release.release_ref.as_dict()})
    write_json(EVIDENCE / "NEGATIVE_CANONICAL_AUTHORITY.json", result)
    raise CampaignError("canonical authority negative unexpectedly succeeded")


def full_config_negative(config: SourceConfig, incidence: Any, selection: Mapping[str, Any]) -> dict[str, Any]:
    result = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_FULL_CONFIG_NEGATIVE@1.0.0",
        "source_id": SOURCE_ID,
        "configured_response_slots": 178,
        "configured_coordinate_slots": 3,
        "incomplete_response_slots": selection["incomplete_response_slots"],
        "incomplete_coordinate_slots": selection["incomplete_coordinate_slots"],
        "source_read_performed": True,
    }
    try:
        release = build_validated_c11_release_from_config(config, incidence=incidence)
    except Exception as exc:
        result.update({
            "status": "REFUSED",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "release_created": False,
        })
        write_json(EVIDENCE / "NEGATIVE_FULL_CONFIG.json", result)
        return result
    result.update({"status": "UNEXPECTED_SUCCESS", "release_ref": release.release_ref.as_dict()})
    write_json(EVIDENCE / "NEGATIVE_FULL_CONFIG.json", result)
    raise CampaignError("full configured release unexpectedly succeeded")


def release_audit(release: C11LogicalRelease, selection: Mapping[str, Any]) -> dict[str, Any]:
    public_counts = Counter(type(obj).__name__ for obj in release.public_objects)
    internal_counts = Counter(type(record).__name__ for record in release.internal_records)
    canonical_events = 0
    canonical_coords = 0
    for obj in release.public_objects:
        if isinstance(obj, RespondentEvent):
            if obj.canonical_response_value_if_authorized is not None or obj.canonical_question_ref_if_authorized is not None:
                canonical_events += 1
        if isinstance(obj, EmpiricalCoordinateFact):
            if obj.canonical_coordinate_value_if_authorized is not None or obj.canonical_coordinate_ref_if_authorized is not None:
                canonical_coords += 1
    canonical_questions = sum(
        1 for record in release.internal_records
        if isinstance(record, QuestionVariableBinding)
        and not hasattr(record.canonical_question_ref_or_typed_absence, "state"))
    selected_response = len(selection["selected_response_slots"])
    selected_coord = len(selection["selected_coordinate_slots"])
    expected = {
        "RespondentEvent": selected_response * EXPECTED_SOURCE_ROWS,
        "RoutingEligibilityFact": selected_response * EXPECTED_SOURCE_ROWS,
        "EmpiricalCoordinateFact": selected_coord * EXPECTED_SOURCE_ROWS,
        "RespondentIdentity": EXPECTED_SOURCE_ROWS,
        "QuestionVariableBinding": selected_response,
    }
    checks = {
        "release_kind": release.release_ref.kind == "C11LogicalRelease",
        "release_id": release.release_id == "SRC04_ARAB_BAROMETER_I_PREPARATION",
        "source_artifact_sha": release.source_artifact_ref.content_hash == EXPECTED_SOURCE_SHA256,
        "semantic_hash_matches_ref": release.semantic_release_hash == release.release_ref.content_hash,
        "events_count": public_counts["RespondentEvent"] == expected["RespondentEvent"],
        "routing_count": public_counts["RoutingEligibilityFact"] == expected["RoutingEligibilityFact"],
        "coordinate_count": public_counts["EmpiricalCoordinateFact"] == expected["EmpiricalCoordinateFact"],
        "respondent_count": internal_counts["RespondentIdentity"] == expected["RespondentIdentity"],
        "question_count": internal_counts["QuestionVariableBinding"] == expected["QuestionVariableBinding"],
        "no_weight_facts": public_counts["WeightMeasureFact"] == 0,
        "no_canonical_events": canonical_events == 0,
        "no_canonical_coordinates": canonical_coords == 0,
        "no_canonical_questions": canonical_questions == 0,
        "m01_m18_complete": set(release.m01_m18_coverage) == {f"M{i:02d}" for i in range(1, 19)},
    }
    return {
        "release_ref": release.release_ref.as_dict(),
        "release_id": release.release_id,
        "semantic_release_hash": release.semantic_release_hash,
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "public_object_count": len(release.public_objects),
        "internal_record_count": len(release.internal_records),
        "public_counts": dict(sorted(public_counts.items())),
        "internal_counts": dict(sorted(internal_counts.items())),
        "m01_m18_coverage_counts": {k: len(v) for k, v in release.m01_m18_coverage.items()},
        "canonical_response_values": canonical_events,
        "canonical_coordinate_values": canonical_coords,
        "canonical_questions": canonical_questions,
        "expected_counts": expected,
        "checks": checks,
        "passed": all(checks.values()),
    }


def _bundle_root() -> Path:
    configured = os.environ.get("CAMPAIGN_A_RUNTIME_ROOT")
    root = Path(configured) if configured else (Path.home() / "Library/Application Support/Rawlsing/campaign-a-src04")
    root = root.resolve()
    repo = ROOT.resolve()
    if root == repo or repo in root.parents:
        raise CampaignError("original release runtime must be outside the Git worktree")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_jsonl_gz(path: Path, values: Sequence[Any]) -> tuple[int, int, str]:
    count = 0
    raw_bytes = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            for value in values:
                line = json.dumps(jsonable(value), sort_keys=True, separators=(",", ":"),
                                  ensure_ascii=False).encode("utf-8") + b"\n"
                gz.write(line)
                raw_bytes += len(line)
                count += 1
    return count, path.stat().st_size, sha_file(path)


def persist_local_release(release: C11LogicalRelease, selection: Mapping[str, Any]) -> dict[str, Any]:
    runtime = _bundle_root()
    bundle_id = f"{SOURCE_ID}-{release.semantic_release_hash[:16]}"
    bundle_dir = runtime / "releases" / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    public_path = bundle_dir / "public_objects.jsonl.gz"
    internal_path = bundle_dir / "internal_records.jsonl.gz"
    public_count, public_bytes, public_sha = _write_jsonl_gz(public_path, release.public_objects)
    internal_count, internal_bytes, internal_sha = _write_jsonl_gz(internal_path, release.internal_records)
    replay_path = bundle_dir / "replay_manifest.json"
    write_json(replay_path, release.replay_manifest.as_dict())
    replay_sha = sha_file(replay_path)
    receipt = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_LOCAL_RELEASE@1.0.0",
        "bundle_id": bundle_id,
        "runtime_scope": "LOCAL_FILESYSTEM_OUTSIDE_GIT",
        "source_id": SOURCE_ID,
        "source_sha256": release.source_artifact_ref.content_hash,
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "selected_response_slots": selection["selected_response_slots"],
        "selected_coordinate_slots": selection["selected_coordinate_slots"],
        "public_objects": {"file": public_path.name, "lines": public_count, "bytes": public_bytes, "sha256": public_sha},
        "internal_records": {"file": internal_path.name, "lines": internal_count, "bytes": internal_bytes, "sha256": internal_sha},
        "replay_manifest": {"file": replay_path.name, "sha256": replay_sha},
        "local_only": True,
        "raw_respondent_cells_committed": False,
    }
    write_json(bundle_dir / "receipt.json", receipt)
    write_json(LOCAL_RECEIPT_PATH, receipt)
    return receipt


def grant_evidence(grant: Mapping[str, Any], request: SourceReadRequest) -> dict[str, Any]:
    document = grant["document"]
    return {
        "schema": "PYAT_CAMPAIGN_A_SRC04_GRANT_AUTHENTICATION@1.0.0",
        "source_id": SOURCE_ID,
        "control_commit": CONTROL_COMMIT,
        "user_grant_sha256": EXPECTED_GRANT_SHA256,
        "program_sha256": EXPECTED_PROGRAM_SHA256,
        "grant_copies": [
            {"role": "COMMITTED_EVIDENCE",
             "path": "campaign_a_src04/evidence/USER_GRANT.json",
             "sha256": expected["sha256"]}
            for expected in grant["copies"]
        ],
        "authorization_present": True,
        "authorization_context_present": True,
        "source_path": str(grant["source_path"]),
        "expected_source_sha256": EXPECTED_SOURCE_SHA256,
        "host": document["host"],
        "purpose": document["purpose"],
        "consumer": document["consumer"],
        "request": {
            "source_id": request.source_id,
            "source_sha256": request.source_sha256,
            "source_format": request.source_format,
            "custody_locator_binding": request.custody_locator_binding,
            "host": request.host,
            "purpose": request.purpose,
            "consumer_use": request.consumer_use,
            "read_operation": request.read_operation,
            "physical_read_extent": request.physical_read_extent,
            "metadata_freeze_refs": [x.as_dict() for x in request.metadata_freeze_refs],
            "semantic_use_scope": list(request.semantic_use_scope),
        },
        "decision_ref": grant["decision_ref"].as_dict(),
        "source_permission_ref": grant["grant_ref"].as_dict(),
        "currentness": CURRENT_GRANTED,
        "revocation": "NONE_RECORDED",
        "effective_interval": "2026-10-27/USER_GRANT_PINNED_CONTROL_2d2814",
        "dummy_test_only_resolver_used": False,
        "scientific_ALLOW_claimed": False,
        "note": "Human source-read approval authorizes this exact read; it does not promote DEFER semantic authorities.",
    }


def run_primary() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    config = load_source_config(CONFIG_PATH)
    if sha_file(CONFIG_PATH) != EXPECTED_CONFIG_FILE_SHA256:
        raise CampaignError("SRC04 config file SHA mismatch")
    if canonical_config_hash(config) != EXPECTED_CONFIG_CANONICAL_SHA256:
        raise CampaignError("SRC04 canonical config hash mismatch")
    if config.document["binding"]["row_count"] != EXPECTED_SOURCE_ROWS:
        raise CampaignError("config row count mismatch")
    if len(config.document["response_slots"]) != EXPECTED_RESPONSE_SLOTS:
        raise CampaignError("config response-slot count mismatch")
    if len(config.document["coordinate_slots"]) != EXPECTED_COORDINATE_SLOTS:
        raise CampaignError("config coordinate-slot count mismatch")
    grant = load_grant()
    request = make_request(config, grant)
    write_json(EVIDENCE / "GRANT_AUTHENTICATION.json", grant_evidence(grant, request))

    wrong = wrong_source_negative(config, grant)
    write_json(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json", wrong)
    if wrong.get("status") != "REFUSED":
        raise CampaignError("wrong-source negative did not refuse")

    incidence, decode_receipt = decode_original(config, grant)
    try:
        audit = physical_audit(config, incidence)
        selection = scan_slots(config, incidence)
        if not selection["accounting"]["all_181_physical_slots_accounted"]:
            raise CampaignError("physical slot accounting failed")
        full_negative = full_config_negative(config, incidence, selection)
        canonical = canonical_negative(config, selection, incidence)
        slice_config, withheld = build_slice_config(config, selection, strip_canonical=True)
        started = time.monotonic()
        release = build_validated_c11_release_from_config(slice_config, incidence=incidence)
        build_seconds = round(time.monotonic() - started, 3)
        release_info = release_audit(release, selection)
        if not release_info["passed"]:
            raise CampaignError(f"release audit failed: {release_info['checks']}")
        if release_info["source_artifact_ref"]["content_hash"] != EXPECTED_SOURCE_SHA256:
            raise CampaignError("release source identity mismatch")
        local = persist_local_release(release, selection)
        release_receipt = {
            "schema": "PYAT_CAMPAIGN_A_SRC04_RELEASE_RECEIPT@1.0.0",
            "source_id": SOURCE_ID,
            "source_path": str(grant["source_path"]),
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "source_rows": EXPECTED_SOURCE_ROWS,
            "source_columns": EXPECTED_SOURCE_COLUMNS,
            "source_bytes": grant["source_path"].stat().st_size,
            "configured_response_slots": EXPECTED_RESPONSE_SLOTS,
            "configured_coordinate_slots": EXPECTED_COORDINATE_SLOTS,
            "source_read_performed": True,
            "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "transport": "rawlsing_next.source_configuration.reader.decode_config_with_source_read_permission",
            "config_path": str(CONFIG_PATH.relative_to(ROOT)),
            "config_file_sha256": sha_file(CONFIG_PATH),
            "config_canonical_sha256": canonical_config_hash(config),
            "slice_config_canonical_sha256": canonical_config_hash(slice_config),
            "grant_sha256": EXPECTED_GRANT_SHA256,
            "program_sha256": EXPECTED_PROGRAM_SHA256,
            "control_commit": CONTROL_COMMIT,
            "decision_ref": grant["decision_ref"].as_dict(),
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
            "canonical_values_withheld": withheld,
            "selected_response_slots": selection["selected_response_slots"],
            "selected_question_ids": selection["selected_response_question_ids"],
            "selected_coordinate_slots": selection["selected_coordinate_slots"],
            "excluded_unbound_response_slots": selection["incomplete_response_slots"],
            "excluded_coordinate_slots": selection["incomplete_coordinate_slots"],
            "eligible_complete_not_selected": [
                x["ordinal"] for x in selection["response_slots"]
                if x["status"] == "ELIGIBLE_COMPLETE_NOT_INCLUDED_BOUNDED_FIRST_SLICE"],
            "release": release_info,
            "build_seconds": build_seconds,
            "source_read_receipt": decode_receipt,
            "physical_audit": {
                "path": str((EVIDENCE / "PHYSICAL_METADATA_AUDIT.json").relative_to(ROOT)),
                "sha256": sha_file(EVIDENCE / "PHYSICAL_METADATA_AUDIT.json"),
                "passed": audit["passed"],
                "checks": audit["checks"],
                "source_native_agreement": "EXACT_181_OF_181",
            },
            "local_release": local,
            "authority": {
                "original_snapshots_unchanged": True,
                "canonical_semantic_ALLOW_claimed": False,
                "authority_states": dict(Counter(x["typed_state"] for x in config.document["authority"]["snapshots"])),
                "routing_state": "ROUTING_UNKNOWN",
                "weight_scope": "NOT_DECLARED",
                "population_claims": "NOT_MADE",
            },
            "full_config_negative": full_negative,
            "canonical_authority_negative": canonical,
        }
        write_json(RELEASE_RECEIPT_PATH, release_receipt)
        write_json(PRIMARY_RUN_PATH, {
            "schema": "PYAT_CAMPAIGN_A_SRC04_PRIMARY_RUN@1.0.0",
            "status": "PRIMARY_COMPLETE",
            "grant": grant_evidence(grant, request),
            "physical_audit_path": "campaign_a_src04/evidence/PHYSICAL_METADATA_AUDIT.json",
            "selection_path": "campaign_a_src04/evidence/SLICE_SELECTION.json",
            "negative_wrong_source_path": "campaign_a_src04/evidence/NEGATIVE_WRONG_SOURCE.json",
            "negative_full_config_path": "campaign_a_src04/evidence/NEGATIVE_FULL_CONFIG.json",
            "negative_canonical_path": "campaign_a_src04/evidence/NEGATIVE_CANONICAL_AUTHORITY.json",
            "release_receipt_path": "campaign_a_src04/evidence/RELEASE_RECEIPT.json",
            "local_release_receipt_path": "campaign_a_src04/evidence/LOCAL_RELEASE_RECEIPT.json",
            "release_ref": release_info["release_ref"],
            "source_read_performed": True,
        })
        print(json.dumps({
            "status": "PRIMARY_COMPLETE",
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "rows": EXPECTED_SOURCE_ROWS,
            "columns": EXPECTED_SOURCE_COLUMNS,
            "selected_response_slots": len(selection["selected_response_slots"]),
            "selected_coordinate_slots": len(selection["selected_coordinate_slots"]),
            "release_ref": release_info["release_ref"],
            "semantic_release_hash": release_info["semantic_release_hash"],
            "public_objects": release_info["public_object_count"],
            "internal_records": release_info["internal_record_count"],
        }, indent=2))
        return 0
    finally:
        incidence.close()


def run_replay() -> int:
    primary = load_json(PRIMARY_RUN_PATH)
    receipt = load_json(RELEASE_RECEIPT_PATH)
    config = load_source_config(CONFIG_PATH)
    grant = load_grant()
    request = make_request(config, grant)
    wrong = load_json(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json")
    incidence, decode_receipt = decode_original(config, grant)
    try:
        audit = physical_audit(config, incidence)
        if not audit["passed"]:
            raise CampaignError("cold replay physical metadata audit failed")
        selection = scan_slots(config, incidence)
        expected = receipt["release"]
        if selection["selected_response_slots"] != receipt["selected_response_slots"]:
            raise CampaignError("cold replay selection changed")
        if selection["selected_coordinate_slots"] != receipt["selected_coordinate_slots"]:
            raise CampaignError("cold replay coordinate selection changed")
        slice_config, withheld = build_slice_config(config, selection, strip_canonical=True)
        started = time.monotonic()
        release = build_validated_c11_release_from_config(slice_config, incidence=incidence)
        seconds = round(time.monotonic() - started, 3)
        audit = release_audit(release, selection)
        local = load_json(LOCAL_RECEIPT_PATH)
        bundle = _bundle_root() / "releases" / local["bundle_id"]
        local_ok = all((bundle / local[key]["file"]).is_file() and sha_file(bundle / local[key]["file"]) == local[key]["sha256"]
                       for key in ("public_objects", "internal_records", "replay_manifest"))
        result = {
            "schema": "PYAT_CAMPAIGN_A_SRC04_REPLAY@1.0.0",
            "status": "COLD_REPLAY_COMPLETE",
            "cold_process": True,
            "source_read_performed": True,
            "source_sha256": incidence.source_sha256,
            "rows": incidence.row_count,
            "resolver_calls": decode_receipt["resolver_calls"],
            "selection_match": True,
            "release_ref": audit["release_ref"],
            "semantic_release_hash": audit["semantic_release_hash"],
            "release_match": (
                audit["release_ref"] == expected["release_ref"]
                and audit["semantic_release_hash"] == expected["semantic_release_hash"]
                and audit["source_release_manifest_hash"] == expected["source_release_manifest_hash"]
                and audit["public_counts"] == expected["public_counts"]
                and audit["internal_counts"] == expected["internal_counts"]
            ),
            "release_audit_passed": audit["passed"],
            "canonical_values_withheld": withheld,
            "local_bundle_exists_and_hashes_match": local_ok,
            "wrong_source_negative_status": wrong.get("status"),
            "build_seconds": seconds,
            "source_read_receipt": decode_receipt,
        }
        if not (result["release_match"] and result["release_audit_passed"] and local_ok):
            raise CampaignError("cold replay did not match primary release")
        write_json(REPLAY_PATH, result)
        print(json.dumps(result, indent=2))
        return 0
    finally:
        incidence.close()


def _manifest_files() -> list[dict[str, Any]]:
    files = [
        "campaign_a_src04/run_campaign_a_src04.py",
        "campaign_a_src04/tests/test_campaign_a_src04.py",
        "campaign_a_src04/README.md",
        "campaign_a_src04/COMMANDS.md",
        "campaign_a_src04/evidence/USER_GRANT.json",
        "campaign_a_src04/evidence/PROGRAM.txt",
        "campaign_a_src04/evidence/GRANT_AUTHENTICATION.json",
        "campaign_a_src04/evidence/PHYSICAL_METADATA_AUDIT.json",
        "campaign_a_src04/evidence/SLICE_SELECTION.json",
        "campaign_a_src04/evidence/NEGATIVE_WRONG_SOURCE.json",
        "campaign_a_src04/evidence/NEGATIVE_FULL_CONFIG.json",
        "campaign_a_src04/evidence/NEGATIVE_CANONICAL_AUTHORITY.json",
        "campaign_a_src04/evidence/RELEASE_RECEIPT.json",
        "campaign_a_src04/evidence/LOCAL_RELEASE_RECEIPT.json",
        "campaign_a_src04/evidence/REPLAY_RECEIPT.json",
        "campaign_a_src04/evidence/TEST_RESULTS.json",
        "campaign_a_src04/evidence/PRIMARY_RUN.json",
    ]
    out = []
    for rel in files:
        path = ROOT / rel
        if path.is_file():
            out.append({"path": rel, "sha256": sha_file(path), "bytes": path.stat().st_size})
    return out


def run_tests() -> int:
    command = [sys.executable, "-m", "pytest", "campaign_a_src04/tests", "-q", "-o", "addopts="]
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    result = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_TEST_RESULTS@1.0.0",
        "command": "python3 -m pytest campaign_a_src04/tests -q -o addopts=",
        "returncode": done.returncode,
        "stdout_tail": done.stdout.strip().splitlines()[-8:],
        "stderr_tail": done.stderr.strip().splitlines()[-8:],
        "passed": done.returncode == 0,
    }
    write_json(TEST_RESULTS_PATH, result)
    print(json.dumps(result, indent=2))
    return 0 if done.returncode == 0 else 1


def run_return(artifact_commit: str) -> int:
    primary = load_json(PRIMARY_RUN_PATH)
    receipt = load_json(RELEASE_RECEIPT_PATH)
    replay = load_json(REPLAY_PATH)
    tests = load_json(TEST_RESULTS_PATH)
    grant = load_json(EVIDENCE / "GRANT_AUTHENTICATION.json")
    audit = load_json(EVIDENCE / "PHYSICAL_METADATA_AUDIT.json")
    selection = load_json(EVIDENCE / "SLICE_SELECTION.json")
    wrong = load_json(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json")
    full_negative = load_json(EVIDENCE / "NEGATIVE_FULL_CONFIG.json")
    canonical = load_json(EVIDENCE / "NEGATIVE_CANONICAL_AUTHORITY.json")
    local = load_json(LOCAL_RECEIPT_PATH)
    history_manifest_path = EVIDENCE / "history/red-92d4f793/MANIFEST.json"
    history_manifest = load_json(history_manifest_path)
    release = receipt["release"]
    return_document = {
        "schema": "PYAT_CAMPAIGN_A_SRC04_RETURN@1.0.0",
        "campaign": "A1",
        "source_id": SOURCE_ID,
        "status": "ORIGINAL_SOURCE_C11_RELEASE_COMPLETED__ELIGIBLE_SLICE__INDEPENDENT_ACCEPTANCE_PENDING",
        "artifact_commit": artifact_commit,
        "milestone_claimed": "NONE_SELF_CLAIMED",
        "source_read_performed": True,
        "source": {
            "path": receipt["source_path"],
            "sha256": receipt["source_sha256"],
            "rows": receipt["source_rows"],
            "columns": receipt["source_columns"],
            "bytes": receipt["source_bytes"],
            "configured_response_slots": receipt["configured_response_slots"],
            "configured_coordinate_slots": receipt["configured_coordinate_slots"],
            "config_path": receipt["config_path"],
            "config_file_sha256": receipt["config_file_sha256"],
            "config_canonical_sha256": receipt["config_canonical_sha256"],
        },
        "permission": {
            "grant_sha256": receipt["grant_sha256"],
            "program_sha256": receipt["program_sha256"],
            "control_commit": receipt["control_commit"],
            "decision_ref": receipt["decision_ref"],
            "currentness": grant["currentness"],
            "revocation": grant["revocation"],
            "host": grant["host"],
            "purpose": grant["purpose"],
            "consumer": grant["consumer"],
            "dummy_test_only_resolver_used": False,
            "scientific_ALLOW_claimed": False,
            "authorization_evidence": "campaign_a_src04/evidence/GRANT_AUTHENTICATION.json",
            "program_evidence": "campaign_a_src04/evidence/PROGRAM.txt",
            "program_evidence_sha256": sha_file(EVIDENCE / "PROGRAM.txt"),
        },
        "physical_audit": {
            "path": "campaign_a_src04/evidence/PHYSICAL_METADATA_AUDIT.json",
            "sha256": sha_file(EVIDENCE / "PHYSICAL_METADATA_AUDIT.json"),
            "passed": audit["passed"],
            "checks": audit["checks"],
            "source_native_agreement": "EXACT_181_OF_181",
            "physical_metadata_digest": audit["physical_metadata_digest"],
        },
        "slice": {
            "scope": "ELIGIBLE_CONFIGURED_SLICE_NOT_FULL_178_RESPONSE_SCOPE",
            "selection_rule": selection["selection_rule"],
            "selected_response_slots": selection["selected_response_slots"],
            "selected_question_ids": selection["selected_response_question_ids"],
            "selected_coordinate_slots": selection["selected_coordinate_slots"],
            "excluded_unbound_response_slots": selection["incomplete_response_slots"],
            "excluded_coordinate_slots": selection["incomplete_coordinate_slots"],
            "eligible_complete_not_selected": [
                x["ordinal"] for x in selection["response_slots"]
                if x["status"] == "ELIGIBLE_COMPLETE_NOT_INCLUDED_BOUNDED_FIRST_SLICE"],
            "accounting": selection["accounting"],
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
            "canonical_values_withheld": receipt["canonical_values_withheld"],
        },
        "c11": {
            "api": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "call_result": "C11LogicalRelease",
            "release_ref": release["release_ref"],
            "semantic_release_hash": release["semantic_release_hash"],
            "source_release_manifest_hash": release["source_release_manifest_hash"],
            "replay_manifest_ref": release["replay_manifest_ref"],
            "public_object_count": release["public_object_count"],
            "internal_record_count": release["internal_record_count"],
            "public_counts": release["public_counts"],
            "internal_counts": release["internal_counts"],
            "m01_m18_coverage_counts": release["m01_m18_coverage_counts"],
            "checks": release["checks"],
            "passed": release["passed"],
        },
        "premises": {
            "selected": "42 configured response slots with complete observed value/state bindings in the first battery ordinal range 3..45, plus country and ser coordinates",
            "excluded_unbound_response": "15 response slots have observed source values/states without an exact configured value rule; retained as exact residuals, not promoted",
            "excluded_coordinate": "q701 continuous coordinate has observed values and 1311 missing cells outside its exact configured rule; excluded",
            "eligible_complete_not_selected": "121 complete response slots outside the bounded first battery are not claimed in this release",
            "routing": "all selected routing facts remain ROUTING_UNKNOWN; no eligibility/form/population claim",
            "weights": "no weight slots are declared; no weighted or population claim",
            "row_keys": "source_native_key_slot is null; respondents remain source row-ordinal scoped with typed absence for native keys",
            "authority": "original authority snapshots unchanged; canonical semantic promotion withheld because mapping authority is DEFER",
        },
        "authority": {
            "original_snapshots_unchanged": True,
            "authority_states": receipt["authority"]["authority_states"],
            "scientific_semantic_ALLOW_claimed": False,
            "canonical_semantic_ALLOW_claimed": False,
            "routing_state": receipt["authority"]["routing_state"],
            "weight_scope": receipt["authority"]["weight_scope"],
            "population_claims": receipt["authority"]["population_claims"],
            "limits": [
                "A source read grant is not a scientific/semantic ALLOW.",
                "The release is a bounded eligible configured slice, not full 178-response original execution.",
                "Canonical values and signed-direction semantics were withheld; no semantic promotion.",
                "No eligibility, weight, population, or downstream empirical claim is made.",
            ],
        },
        "repair": {
            "review_candidate": "0daf4aa5d143cc3a4e95984620a39489ed2fa39c",
            "review_disposition": "EXTERNAL_INDEPENDENT_REVIEW_DISPOSITION",
            "d01_program_portability": {
                "status": "REPAIRED",
                "repair": "governing PROGRAM.txt is the committed pinned copy campaign_a_src04/evidence/PROGRAM.txt; runner/tests have no author-private .r61 program dependency",
                "program_sha256": EXPECTED_PROGRAM_SHA256,
            },
            "d02_source_preflight": {
                "status": "REPAIRED",
                "repair": "load_grant no longer stats or hashes the source path; source SHA/bytes are checked only by the SHA-qualified decoder after the current resolver admits the read",
                "direct_source_preflight_removed": True,
            },
            "release_identity_unchanged": "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec",
            "old_red_history": {
                "path": "campaign_a_src04/evidence/history/red-92d4f793/MANIFEST.json",
                "sha256": sha_file(history_manifest_path),
                "candidate": history_manifest["candidate"],
                "artifact_commit": history_manifest["artifact_commit"],
                "file_count": len(history_manifest["files"]),
            },
        },
        "negative_tests": {
            "wrong_source": {
                "path": "campaign_a_src04/evidence/NEGATIVE_WRONG_SOURCE.json",
                "sha256": sha_file(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json"),
                "status": wrong["status"],
                "refusal_code": wrong.get("refusal_code"),
                "source_read_performed": False,
            },
            "full_config_unbound": {
                "path": "campaign_a_src04/evidence/NEGATIVE_FULL_CONFIG.json",
                "sha256": sha_file(EVIDENCE / "NEGATIVE_FULL_CONFIG.json"),
                "status": full_negative["status"],
                "error_type": full_negative.get("error_type"),
                "error": full_negative.get("error"),
                "release_created": False,
            },
            "canonical_authority": {
                "path": "campaign_a_src04/evidence/NEGATIVE_CANONICAL_AUTHORITY.json",
                "sha256": sha_file(EVIDENCE / "NEGATIVE_CANONICAL_AUTHORITY.json"),
                "status": canonical["status"],
                "error_type": canonical.get("error_type"),
                "error": canonical.get("error"),
                "release_created": False,
            },
            "restore": "successful slice release after the negatives; original config and authority snapshots unchanged",
        },
        "replay": {
            "path": "campaign_a_src04/evidence/REPLAY_RECEIPT.json",
            "sha256": sha_file(REPLAY_PATH),
            "status": replay["status"],
            "cold_process": replay["cold_process"],
            "source_read_performed": replay["source_read_performed"],
            "release_match": replay["release_match"],
            "release_audit_passed": replay["release_audit_passed"],
            "local_bundle_exists_and_hashes_match": replay["local_bundle_exists_and_hashes_match"],
            "semantic_release_hash": replay["semantic_release_hash"],
        },
        "tests": {
            "path": "campaign_a_src04/evidence/TEST_RESULTS.json",
            "sha256": sha_file(TEST_RESULTS_PATH),
            "command": tests["command"],
            "returncode": tests["returncode"],
            "passed": tests["passed"],
            "stdout_tail": tests["stdout_tail"],
            "clean_checkout": tests.get("clean_checkout"),
        },
        "local_release": {
            "receipt_path": "campaign_a_src04/evidence/LOCAL_RELEASE_RECEIPT.json",
            "receipt_sha256": sha_file(LOCAL_RECEIPT_PATH),
            "bundle_id": local["bundle_id"],
            "runtime_scope": "LOCAL_FILESYSTEM_OUTSIDE_GIT",
            "public_objects_sha256": local["public_objects"]["sha256"],
            "internal_records_sha256": local["internal_records"]["sha256"],
            "raw_respondent_cells_committed": False,
            "source_bytes_committed": False,
        },
        "source_custody": {
            "read_owner": receipt["source_read_receipt"]["source_read_owner"],
            "transport": receipt["source_read_receipt"]["transport"],
            "reader_configuration": receipt["source_read_receipt"]["reader_configuration"],
            "source_custody": receipt["source_read_receipt"]["source_custody"],
            "resolver_calls": receipt["source_read_receipt"]["resolver_calls"],
            "source_read_performed": True,
            "source_preflight_io_before_admission": False,
        },
        "artifact_manifest": _manifest_files(),
        "limits": [
            "This is a first original-source C11 source-native slice release, not M1/M2 independent acceptance.",
            "42 response slots + 2 coordinates are included; 15 unbound response slots and q701 are exact residuals; 121 complete slots are outside this bounded first battery.",
            "Original config and all authority snapshots remain unchanged; DEFER is preserved.",
            "No original empirical workload, I03/I05 query, FF/M1/N11/N12/actor/CI/prod/Sorok/J52W52 execution.",
            "No respondent cells, row-wise artifacts, or original source bytes are committed.",
            "Independent HQ/distinct review remains pending.",
        ],
        "next_consumer": "HQ/distinct reviewer for independent A1 acceptance; then existing I03/I05 downstream owner if separately authorized.",
    }
    write_json(RETURN_PATH, return_document)
    print(json.dumps({
        "return_path": str(RETURN_PATH.relative_to(ROOT)),
        "return_sha256": sha_file(RETURN_PATH),
        "release_ref": release["release_ref"],
        "source_read_performed": True,
        "tests_passed": tests["passed"],
        "replay_release_match": replay["release_match"],
    }, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("primary", "replay", "tests", "return"), required=True)
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args(argv)
    try:
        if args.mode == "primary":
            return run_primary()
        if args.mode == "replay":
            return run_replay()
        if args.mode == "tests":
            return run_tests()
        if args.mode == "return":
            if not args.artifact_commit:
                raise CampaignError("--artifact-commit is required for return mode")
            return run_return(args.artifact_commit)
    except Exception as exc:
        failure = {
            "schema": "PYAT_CAMPAIGN_A_SRC04_FAILURE@1.0.0",
            "mode": args.mode,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        write_json(EVIDENCE / "FAILURE.json", failure)
        print(json.dumps(failure, indent=2), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
