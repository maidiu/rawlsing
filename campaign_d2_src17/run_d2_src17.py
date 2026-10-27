"""D2 bounded original SRC17 source read and C11 construction.

Reads only the TRUE-HQ-authorized SRC17 file through the existing source-read
admission and SHA-checked SAV decoder. Builds the largest qualified slice whose
observed cells are fully covered by the accepted R157 SRC17 rules. Raw
respondent cells and row-wise products remain in a local runtime bundle outside
Git; committed evidence is nonidentifying refs/counts/code.
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

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    WeightMeasureFact,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import (
    PhysicalMissingState,
    classify_physical_value,
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
    row_native_keys_from_transport,
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
CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC17/SRC17.source.config.json"
METADATA_PATH = ROOT / "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/SRC17_PHYSICAL_METADATA.json"
PROGRAM_PATH = EVIDENCE / "PROGRAM.txt"
GRANT_TEXT_PATH = EVIDENCE / "TRUE_HQ_GRANT.txt"
GRANT_JSON_PATH = EVIDENCE / "USER_GRANT.json"

SOURCE_ID = "SRC17"
EXPECTED_SOURCE_SHA256 = "59e65801dc26818bbcf15f9ed985cf8f1faafa65a3eb59e2d3180a7b13a5c1c2"
EXPECTED_SOURCE_ROWS = 1504
EXPECTED_SOURCE_COLUMNS = 339
EXPECTED_SOURCE_BYTES = 1984639
EXPECTED_CONFIG_FILE_SHA256 = "ca791189e208c9b311a7261ac254ce5ffea35e9c13b4d6e2ec87e9e55a1ecca8"
EXPECTED_CONFIG_CANONICAL_SHA256 = "3f1eb83abe61415e01b2f67bcfe34ee6fe61d69d3aef7161be5e6e41e2a7be07"
EXPECTED_METADATA_SHA256 = "e7a8515c6473b43b9a8f9233ca7aac5cd8ec246e8f7dcf9ecb42b23d92c89c52"
EXPECTED_GRANT_SHA256 = "f51de87818f8fd1365d347da3aee73005fe9ab8ae0c8d2a607487395016d48ae"
EXPECTED_PROGRAM_SHA256 = "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
CONTROL_COMMIT = "3b703e878946a442b5c880f318b929365865ed00"
PURPOSE = "SECOND_FAMILY_ORIGINAL_SOURCE_C11_POSITIVE"
CONSUMER = "EXISTING_PRE553_SOURCE_BACKED_C11"
SEMANTIC_USE_SCOPE = (
    "SOURCE_NATIVE_RESPONSE_INCIDENCE",
    "NO_SEMANTIC_ADOPTION",
    "SRC17",
    "CAMPAIGN_D2",
)
SOURCE_PATH_SENTINEL = "/nonexistent/campaign-d2-src17-wrong-source.sav"
CURRENTNESS_TEXT = "2026-10-27/TRUE_HQ_D1_D2_PINNED_CONTROL_3b703e8"

PRIMARY_PATH = EVIDENCE / "PRIMARY_RUN.json"
AUDIT_PATH = EVIDENCE / "PHYSICAL_METADATA_AUDIT.json"
RUNTIME_CONFIG_PATH = EVIDENCE / "SRC17.d2_runtime.config.json"
SELECTION_PATH = EVIDENCE / "SLICE_SELECTION.json"
GRANT_AUTH_PATH = EVIDENCE / "GRANT_AUTHENTICATION.json"
NEG_WRONG_PATH = EVIDENCE / "NEGATIVE_WRONG_SOURCE.json"
NEG_CANONICAL_PATH = EVIDENCE / "NEGATIVE_CANONICAL_AUTHORITY.json"
NEG_HELD_PATH = EVIDENCE / "NEGATIVE_HELD_SLICE.json"
RELEASE_PATH = EVIDENCE / "RELEASE_RECEIPT.json"
LOCAL_PATH = EVIDENCE / "LOCAL_RELEASE_RECEIPT.json"
REPLAY_PATH = EVIDENCE / "REPLAY_RECEIPT.json"
TEST_PATH = EVIDENCE / "TEST_RESULTS.json"
RETURN_PATH = CAMPAIGN / "RETURN.json"


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


def _norm_width(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return str(value)


def _norm_missing(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, Mapping):
        return [dict(value)]
    return [dict(x) for x in value]


def verify_control() -> dict[str, Any]:
    command = ["git", "show", f"{CONTROL_COMMIT}:PYAT_CONTROL_ROOM/TRUE_HQ_D1_D2_DISPOSITION_20261027.txt"]
    grant = subprocess.run(command, cwd=ROOT, capture_output=True, check=True)
    command2 = ["git", "show", f"{CONTROL_COMMIT}:PYAT_CONTROL_ROOM/PYAT_STANDING_EXECUTION_PROGRAM_R1.txt"]
    program = subprocess.run(command2, cwd=ROOT, capture_output=True, check=True)
    result = {
        "control_commit": CONTROL_COMMIT,
        "grant_from_control_sha256": hashlib.sha256(grant.stdout).hexdigest(),
        "program_from_control_sha256": hashlib.sha256(program.stdout).hexdigest(),
    }
    if result["grant_from_control_sha256"] != EXPECTED_GRANT_SHA256:
        raise CampaignError("pinned control grant hash mismatch")
    if result["program_from_control_sha256"] != EXPECTED_PROGRAM_SHA256:
        raise CampaignError("pinned control program hash mismatch")
    return result


def load_grant() -> dict[str, Any]:
    for path, expected in ((GRANT_TEXT_PATH, EXPECTED_GRANT_SHA256),
                           (PROGRAM_PATH, EXPECTED_PROGRAM_SHA256),
                           (GRANT_JSON_PATH, None)):
        if not path.is_file():
            raise CampaignError(f"missing committed grant artifact {path}")
        if expected is not None and sha_file(path) != expected:
            raise CampaignError(f"committed grant artifact hash mismatch: {path.name}")
    document = load_json(GRANT_JSON_PATH)
    if document.get("source_id") != SOURCE_ID:
        raise CampaignError("grant source_id mismatch")
    if document.get("expected_source_sha256") != EXPECTED_SOURCE_SHA256:
        raise CampaignError("grant source SHA mismatch")
    if document.get("expected_rows") != EXPECTED_SOURCE_ROWS or document.get("expected_columns") != EXPECTED_SOURCE_COLUMNS:
        raise CampaignError("grant shape expectation mismatch")
    if document.get("expected_bytes") != EXPECTED_SOURCE_BYTES:
        raise CampaignError("grant byte expectation mismatch")
    if document.get("host") != "USER_LOCAL_MAC":
        raise CampaignError("grant host mismatch")
    if document.get("purpose") != PURPOSE or document.get("consumer") != CONSUMER:
        raise CampaignError("grant purpose/consumer mismatch")
    if document.get("control_commit") != CONTROL_COMMIT:
        raise CampaignError("grant control commit mismatch")
    grant_ref = ExactRef("USER_SOURCE_READ_GRANT", "urn:rawlsing:campaign-d2:src17:grant", EXPECTED_GRANT_SHA256)
    decision_ref = ExactRef(
        "USER_SOURCE_READ_DECISION",
        "urn:rawlsing:campaign-d2:src17:decision",
        semantic_hash({
            "grant_sha256": EXPECTED_GRANT_SHA256,
            "program_sha256": EXPECTED_PROGRAM_SHA256,
            "control_commit": CONTROL_COMMIT,
            "source_id": SOURCE_ID,
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "host": "USER_LOCAL_MAC",
            "purpose": PURPOSE,
            "consumer": CONSUMER,
            "semantic_use_scope": SEMANTIC_USE_SCOPE,
            "read_operation": SOURCE_RESPONSE_DECODE,
            "physical_read_extent": EXACT_FILE,
        }),
    )
    return {
        "document": document,
        "primary_path": str(GRANT_JSON_PATH),
        "grant_ref": grant_ref,
        "decision_ref": decision_ref,
        "source_path": Path(document["source_path"]),
        "grant_text_path": str(GRANT_TEXT_PATH),
        "program_path": str(PROGRAM_PATH),
        "control_commit": CONTROL_COMMIT,
    }


def make_request(config: SourceConfig, grant: Mapping[str, Any]) -> SourceReadRequest:
    return source_read_request_from_config(
        config,
        host=grant["document"]["host"],
        purpose=grant["document"]["purpose"],
        consumer_use=grant["document"]["consumer"],
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
        effective_interval=CURRENTNESS_TEXT,
        currentness=CURRENT_GRANTED,
        revocation_ref=None,
        retention_export_limits={
            "export": "DENY",
            "rowwise_response_artifacts": "DENY",
            "retention": "LOCAL_RUNTIME_ONLY",
            "source_bytes_in_git": "DENY",
        },
    )


class AuthenticatedGrantResolver:
    """Bounded adapter authenticating the exact pinned human grant copies."""

    def __init__(self, grant: Mapping[str, Any], request: SourceReadRequest):
        self.grant = grant
        self.request = request
        self.calls = 0
        self.decision = make_decision(request, grant)

    def resolve_current(self, request: SourceReadRequest) -> IssuedSourceReadDecision:
        self.calls += 1
        if request != self.request:
            raise SourceReadAdmissionRefusal("D2_GRANT_REQUEST_MISMATCH")
        if sha_file(GRANT_TEXT_PATH) != EXPECTED_GRANT_SHA256:
            raise SourceReadAdmissionRefusal("D2_GRANT_CURRENTNESS_MISMATCH")
        if sha_file(PROGRAM_PATH) != EXPECTED_PROGRAM_SHA256:
            raise SourceReadAdmissionRefusal("D2_PROGRAM_CURRENTNESS_MISMATCH")
        return self.decision


def grant_evidence(grant: Mapping[str, Any], request: SourceReadRequest, control: Mapping[str, Any]) -> dict[str, Any]:
    document = grant["document"]
    return {
        "schema": "PYAT_D2_SRC17_GRANT_AUTHENTICATION@1.0.0",
        "source_id": SOURCE_ID,
        "control_commit": CONTROL_COMMIT,
        "control": control,
        "grant_text_path": grant["grant_text_path"],
        "grant_text_sha256": EXPECTED_GRANT_SHA256,
        "program_path": grant["program_path"],
        "program_sha256": EXPECTED_PROGRAM_SHA256,
        "grant_json_path": grant["primary_path"],
        "source_path": document["source_path"],
        "expected_source_sha256": EXPECTED_SOURCE_SHA256,
        "expected_rows": EXPECTED_SOURCE_ROWS,
        "expected_columns": EXPECTED_SOURCE_COLUMNS,
        "expected_bytes": EXPECTED_SOURCE_BYTES,
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
        "effective_interval": CURRENTNESS_TEXT,
        "dummy_test_only_resolver_used": False,
        "scientific_ALLOW_claimed": False,
        "source_io_before_decision": False,
        "no_other_original_reads": True,
        "note": "Human source-read approval authorizes this exact SRC17 read; it does not promote DEFER semantic authorities or issue I03/I05.",
    }


def wrong_source_negative(config: SourceConfig, grant: Mapping[str, Any]) -> dict[str, Any]:
    request = make_request(config, grant)
    resolver = AuthenticatedGrantResolver(grant, request)
    decision = resolver.decision
    wrong = replace(decision, source_sha256="0" * 64)
    class _WrongResolver:
        calls = 0
        def resolve_current(self, req: SourceReadRequest):
            self.calls += 1
            return wrong
    wrong_resolver = _WrongResolver()
    result = {
        "schema": "PYAT_D2_SRC17_WRONG_SOURCE_NEGATIVE@1.0.0",
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
    resolver = AuthenticatedGrantResolver(grant, request)
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
    custody = dict(incidence.source_custody or {})
    return incidence, {
        "schema": "PYAT_D2_SRC17_DECODE_RECEIPT@1.0.0",
        "source_id": SOURCE_ID,
        "source_sha256": incidence.source_sha256,
        "source_format": incidence.source_format,
        "rows": incidence.row_count,
        "columns": len(incidence.variables),
        "expected_rows": EXPECTED_SOURCE_ROWS,
        "expected_columns": EXPECTED_SOURCE_COLUMNS,
        "expected_bytes": EXPECTED_SOURCE_BYTES,
        "source_custody": custody,
        "snapshot_size": custody.get("snapshot_size"),
        "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
        "transport": "rawlsing_next.source_configuration.reader.decode_config_with_source_read_permission",
        "reader_configuration": dict(incidence.reader_configuration),
        "physical_metadata_digest": incidence.physical_metadata_digest,
        "resolver_calls": resolver.calls,
        "decision_ref": grant["decision_ref"].as_dict(),
        "read_elapsed_seconds": elapsed,
        "source_read_performed": True,
    }


def apply_reader_binding(config: SourceConfig, incidence: Any) -> SourceConfig:
    """Bind the accepted config to the actual decoder missing-state classification.

    The accepted R157 config recorded the source special codes as observed
    storage values with no format declaration.  The SHA-checked reader reports
    the exact SAV user-missing range; this derived runtime copy changes only the
    physical binding state/declaration, not response-state meaning or authority.
    """
    document = deepcopy(config.document)
    variables = {int(v.ordinal): v for v in incidence.variables}
    for slot in document["physical_slots"]:
        var = variables[int(slot["ordinal"])]
        declarations = [jsonable(x) for x in var.missing_declarations]
        slot["missing_declarations"] = declarations or None
    for section in document["response_slots"]:
        var = variables[int(section["slot"]["ordinal"])]
        for value in section["values"]:
            raw = value.get("raw_value")
            if raw is None:
                value["missing_state"] = PhysicalMissingState.SYSTEM_MISSING.value
                value["source_missing_declaration"] = None
                continue
            state, declaration = classify_physical_value(raw, var.missing_declarations)
            value["missing_state"] = state.value
            value["source_missing_declaration"] = jsonable(declaration) if declaration else None
    RUNTIME_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_CONFIG_PATH.write_text(
        json.dumps(document, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return SourceConfig(document)


def physical_audit(config: SourceConfig, accepted_config: SourceConfig, incidence: Any) -> dict[str, Any]:
    document = config.document
    config_slots = {int(x["ordinal"]): x for x in document["physical_slots"]}
    actual = {int(v.ordinal): v for v in incidence.variables}
    metadata_document = load_json(METADATA_PATH)
    metadata = metadata_document["metadata"]
    meta_sha = sha_file(METADATA_PATH)
    checks = {
        "metadata_witness_sha_matches_config": meta_sha == document["identity"]["metadata_witness_ref"]["content_hash"] == EXPECTED_METADATA_SHA256,
        "metadata_witness_source_sha_matches": metadata_document.get("sha256") == EXPECTED_SOURCE_SHA256,
        "metadata_witness_bytes": metadata_document.get("bytes") == EXPECTED_SOURCE_BYTES,
        "metadata_witness_rows": metadata.get("number_rows") == EXPECTED_SOURCE_ROWS,
        "metadata_witness_columns": metadata.get("number_columns") == EXPECTED_SOURCE_COLUMNS,
        "source_sha_matches": incidence.source_sha256 == EXPECTED_SOURCE_SHA256,
        "source_rows_match": incidence.row_count == EXPECTED_SOURCE_ROWS,
        "source_columns_match": len(incidence.variables) == EXPECTED_SOURCE_COLUMNS,
        "source_bytes_match": (incidence.source_custody or {}).get("snapshot_size") == EXPECTED_SOURCE_BYTES,
        "ordinal_set_matches": set(actual) == set(config_slots),
        "config_names_match_actual": True,
        "config_labels_match_actual": True,
        "config_storage_types_match_actual": True,
        "config_value_labels_match_actual": True,
        "config_missing_declarations_match_actual": True,
        "config_original_types_match_metadata": True,
        "config_storage_widths_match_metadata": True,
        "config_measures_match_metadata": True,
        "metadata_names_match_actual": True,
        "metadata_labels_match_actual": True,
        "metadata_value_labels_match_actual": True,
        "metadata_storage_types_match_actual": True,
        "items_count": len(document["items"]) == 339,
        "items_unique": len({x["implementation_id"] for x in document["items"]}) == 339,
        "items_cover_all_slots": {x["source_variable_code"] for x in document["items"]} == {x["name"] for x in document["physical_slots"]},
    }
    meta_names = list(metadata.get("column_names") or [])
    meta_labels = metadata.get("column_names_to_labels") or {}
    meta_types = metadata.get("readstat_variable_types") or {}
    meta_vl = metadata.get("variable_value_labels") or {}
    meta_original = metadata.get("original_variable_types") or {}
    meta_width = metadata.get("variable_storage_width") or {}
    meta_measure = metadata.get("variable_measure") or {}
    issues = []
    for ordinal in sorted(config_slots):
        slot = config_slots[ordinal]
        var = actual.get(ordinal)
        if var is None:
            issues.append(f"missing actual ordinal {ordinal}")
            continue
        if slot["name"] != var.name:
            checks["config_names_match_actual"] = False; issues.append(f"name mismatch {ordinal}")
        if slot["label"] != var.variable_label:
            checks["config_labels_match_actual"] = False; issues.append(f"label mismatch {slot['name']}")
        if slot["storage_type"] != var.storage_type:
            checks["config_storage_types_match_actual"] = False; issues.append(f"storage mismatch {slot['name']}")
        if _norm_vl(slot.get("value_labels")) != _norm_vl(var.value_labels):
            checks["config_value_labels_match_actual"] = False; issues.append(f"value labels mismatch {slot['name']}")
        if _norm_missing(slot.get("missing_declarations")) != list(var.missing_declarations or []):
            checks["config_missing_declarations_match_actual"] = False; issues.append(f"missing declarations mismatch {slot['name']}")
        if slot.get("original_type") != meta_original.get(var.name):
            checks["config_original_types_match_metadata"] = False; issues.append(f"original type mismatch {slot['name']}")
        if _norm_width(slot.get("storage_width")) != _norm_width(meta_width.get(var.name)):
            checks["config_storage_widths_match_metadata"] = False; issues.append(f"storage width mismatch {slot['name']}")
        if slot.get("measure") != meta_measure.get(var.name):
            checks["config_measures_match_metadata"] = False; issues.append(f"measure mismatch {slot['name']}")
        if ordinal - 1 >= len(meta_names) or meta_names[ordinal - 1] != var.name:
            checks["metadata_names_match_actual"] = False; issues.append(f"metadata name mismatch {slot['name']}")
        if meta_labels.get(var.name) != var.variable_label:
            checks["metadata_labels_match_actual"] = False; issues.append(f"metadata label mismatch {slot['name']}")
        if meta_types.get(var.name) != var.storage_type:
            checks["metadata_storage_types_match_actual"] = False; issues.append(f"metadata storage mismatch {slot['name']}")
        if _norm_vl(meta_vl.get(var.name)) != _norm_vl(var.value_labels):
            checks["metadata_value_labels_match_actual"] = False; issues.append(f"metadata value labels mismatch {slot['name']}")
    result = {
        "schema": "PYAT_D2_SRC17_PHYSICAL_METADATA_AUDIT@1.0.0",
        "source_id": SOURCE_ID,
        "source_sha256": incidence.source_sha256,
        "rows": incidence.row_count,
        "columns": len(incidence.variables),
        "expected_rows": EXPECTED_SOURCE_ROWS,
        "expected_columns": EXPECTED_SOURCE_COLUMNS,
        "expected_bytes": EXPECTED_SOURCE_BYTES,
        "source_custody": dict(incidence.source_custody or {}),
        "metadata_witness_path": str(METADATA_PATH.relative_to(ROOT)),
        "metadata_witness_sha256": meta_sha,
        "accepted_config_path": str(CONFIG_PATH.relative_to(ROOT)),
        "accepted_config_file_sha256": sha_file(CONFIG_PATH),
        "accepted_config_canonical_sha256": canonical_config_hash(accepted_config),
        "runtime_config_path": str(RUNTIME_CONFIG_PATH.relative_to(ROOT)),
        "runtime_config_file_sha256": sha_file(RUNTIME_CONFIG_PATH),
        "runtime_config_canonical_sha256": canonical_config_hash(config),
        "physical_metadata_digest": incidence.physical_metadata_digest,
        "checks": checks,
        "issues": issues[:50],
        "issue_count": len(issues),
        "passed": all(checks.values()) and not issues,
        "source_read_performed": True,
        "source_native_agreement": "339_OF_339",
    }
    write_json(AUDIT_PATH, result)
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
    response_counts = {o: {"cells": 0, "unbound": 0, "nonobserved": 0} for o in response_slots}
    coordinate_counts = {o: {"cells": 0, "unbound": 0, "nonobserved": 0} for o in coordinate_slots}
    all_cells = 0
    for cell in incidence.iter_cells():
        all_cells += 1
        ordinal = cell.variable_ordinal
        key = physical_value_binding_key(cell.raw_value, cell.missing_state, cell.source_missing_declaration)
        if ordinal in response_counts:
            response_counts[ordinal]["cells"] += 1
            if cell.missing_state.value != "OBSERVED_STORAGE_VALUE":
                response_counts[ordinal]["nonobserved"] += 1
            if key not in response_keys[ordinal]:
                response_counts[ordinal]["unbound"] += 1
        if ordinal in coordinate_counts:
            coordinate_counts[ordinal]["cells"] += 1
            if cell.missing_state.value != "OBSERVED_STORAGE_VALUE":
                coordinate_counts[ordinal]["nonobserved"] += 1
            copy_raw = bool(coordinate_slots[ordinal].get("copy_observed_raw"))
            if not copy_raw and key not in coordinate_keys[ordinal]:
                coordinate_counts[ordinal]["unbound"] += 1
    complete_response = [o for o in sorted(response_slots) if response_counts[o]["unbound"] == 0]
    complete_coordinate = []
    for o in sorted(coordinate_slots):
        section = coordinate_slots[o]
        count = coordinate_counts[o]
        if count["unbound"] == 0 and (section.get("values") or (section.get("copy_observed_raw") and count["nonobserved"] == 0)):
            complete_coordinate.append(o)
    response_rows = []
    for o in sorted(response_slots):
        section = response_slots[o]
        count = response_counts[o]
        if count["unbound"] == 0:
            status, reason = "ELIGIBLE_COMPLETE", "all observed values/states have exact configured rules"
        else:
            status, reason = "HELD_UNBOUND_OBSERVED_VALUES", "observed value/state has no exact configured rule"
        response_rows.append({
            "ordinal": o, "name": section["slot"]["name"], "question_id": section["question_id"],
            "cells": count["cells"], "unbound_cells": count["unbound"],
            "nonobserved_cells": count["nonobserved"], "status": status, "reason": reason,
        })
    coordinate_rows = []
    for o in sorted(coordinate_slots):
        section = coordinate_slots[o]
        count = coordinate_counts[o]
        status = "ELIGIBLE_COMPLETE" if o in complete_coordinate else "HELD_UNBOUND_OR_MISSING"
        reason = "configured coordinate rule fully covers observed cells" if o in complete_coordinate else "observed coordinate value/missing cell is not fully bound"
        coordinate_rows.append({
            "ordinal": o, "name": section["slot"]["name"], "cells": count["cells"],
            "unbound_cells": count["unbound"], "nonobserved_cells": count["nonobserved"],
            "copy_observed_raw": bool(section.get("copy_observed_raw")), "status": status, "reason": reason,
        })
    response_ordinals = set(response_slots)
    coordinate_ordinals = set(coordinate_slots)
    selected_response = complete_response
    selected_coordinate = complete_coordinate
    physical_rows = []
    for slot in document["physical_slots"]:
        ordinal = int(slot["ordinal"])
        if ordinal in selected_response:
            status = "INCLUDED_RESPONSE"
        elif ordinal in response_ordinals:
            status = "HELD_RESPONSE_UNBOUND"
        elif ordinal in selected_coordinate:
            status = "INCLUDED_COORDINATE"
        elif ordinal in coordinate_ordinals:
            status = "HELD_COORDINATE"
        else:
            status = "HELD_ITEM_OR_ROLE"
        physical_rows.append({
            "ordinal": ordinal, "name": slot["name"],
            "disposition": slot.get("disposition"),
            "status": status,
            "reason": slot.get("disposition_reason"),
        })
    item_rows = []
    response_by_name = {x["slot"]["name"]: x for x in document["response_slots"]}
    coord_by_name = {x["slot"]["name"]: x for x in document["coordinate_slots"]}
    for item in document["items"]:
        name = item["source_variable_code"]
        if name in selected_response:
            status = "INCLUDED_RESPONSE"
        elif name in response_by_name:
            status = "HELD_RESPONSE_UNBOUND"
        elif name in selected_coordinate:
            status = "INCLUDED_COORDINATE"
        elif name in coord_by_name:
            status = "HELD_COORDINATE"
        else:
            status = "HELD_ITEM_OR_ROLE"
        item_rows.append({
            "implementation_id": item["implementation_id"], "source_variable_code": name,
            "disposition": item.get("disposition"), "status": status,
        })
    selection = {
        "schema": "PYAT_D2_SRC17_SLICE_SELECTION@1.0.0",
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
        "selected_response_question_ids": [response_slots[o]["question_id"] for o in selected_response],
        "selected_coordinate_slots": selected_coordinate,
        "response_slots": response_rows,
        "coordinate_slots": coordinate_rows,
        "physical_slot_ledger": physical_rows,
        "item_ledger": item_rows,
        "held_response_slots": [o for o in sorted(response_slots) if o not in selected_response],
        "held_coordinate_slots": [o for o in sorted(coordinate_slots) if o not in selected_coordinate],
        "accounting": {
            "all_physical_slots_accounted": len(physical_rows) == 339,
            "all_items_accounted": len(item_rows) == 339,
            "selected_response_slots": len(selected_response),
            "held_response_slots": len(response_slots) - len(selected_response),
            "selected_coordinate_slots": len(selected_coordinate),
            "held_coordinate_slots": len(coordinate_slots) - len(selected_coordinate),
            "held_items_or_roles": sum(1 for x in physical_rows if x["status"] == "HELD_ITEM_OR_ROLE"),
        },
        "selection_rule": "include every configured response/coordinate slot whose complete observed cell set is exactly covered by existing rules; preserve all unbound slots in the held ledger",
        "source_read_performed": True,
    }
    write_json(SELECTION_PATH, selection)
    return selection


def build_slice_config(config: SourceConfig, selection: Mapping[str, Any], *, strip_canonical: bool) -> tuple[SourceConfig, int]:
    document = deepcopy(config.document)
    selected_response = list(selection["selected_response_slots"])
    selected_coordinate = list(selection["selected_coordinate_slots"])
    response = [x for x in document["response_slots"] if int(x["slot"]["ordinal"]) in selected_response]
    qids = {x["question_id"] for x in response}
    document["response_slots"] = response
    document["coordinate_slots"] = [x for x in document["coordinate_slots"] if int(x["slot"]["ordinal"]) in selected_coordinate]
    document["questions"] = [x for x in document["questions"] if x["question_id"] in qids]
    document["routing"] = [x for x in document["routing"] if x["question_id"] in qids]
    document["supported_scope"]["supported_question_ids"] = [x for x in document["supported_scope"]["supported_question_ids"] if x in qids]
    withheld = 0
    if strip_canonical:
        for slot in document["response_slots"]:
            for value in slot["values"]:
                if value.get("canonical_value") is not None or value.get("transform_authority_ref") is not None:
                    withheld += 1
                value["canonical_value"] = None
                value["transform_authority_ref"] = None
                value["extra_authority_refs"] = []
        for question in document["questions"]:
            if "typed_absence_state" not in question["canonical_question_ref_or_typed_absence"]:
                withheld += 1
            question["canonical_question_ref_or_typed_absence"] = {"typed_absence_state": "NOT_AUTHORIZED", "detail": None}
    return SourceConfig(document), withheld


def release_audit(release: C11LogicalRelease, selection: Mapping[str, Any]) -> dict[str, Any]:
    public_counts = Counter(type(obj).__name__ for obj in release.public_objects)
    internal_counts = Counter(type(record).__name__ for record in release.internal_records)
    canonical_events = sum(1 for x in release.public_objects if isinstance(x, RespondentEvent)
                           and (x.canonical_response_value_if_authorized is not None or x.canonical_question_ref_if_authorized is not None))
    canonical_coords = sum(1 for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)
                           and (x.canonical_coordinate_value_if_authorized is not None or x.canonical_coordinate_ref_if_authorized is not None))
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
        "expected_counts": expected,
        "checks": checks,
        "passed": all(checks.values()),
    }


def canonical_negative(config: SourceConfig, selection: Mapping[str, Any], incidence: Any) -> dict[str, Any]:
    slice_doc = deepcopy(config.document)
    ordinal = selection["selected_response_slots"][0]
    section = next(x for x in slice_doc["response_slots"] if int(x["slot"]["ordinal"]) == ordinal)
    qid = section["question_id"]
    slice_doc["response_slots"] = [deepcopy(section)]
    slice_doc["coordinate_slots"] = [deepcopy(slice_doc["coordinate_slots"][0])]
    slice_doc["questions"] = [x for x in slice_doc["questions"] if x["question_id"] == qid]
    slice_doc["routing"] = [x for x in slice_doc["routing"] if x["question_id"] == qid]
    slice_doc["supported_scope"]["supported_question_ids"] = [qid]
    for value in slice_doc["response_slots"][0]["values"]:
        if value.get("raw_value") is not None:
            value["canonical_value"] = "INJECTED_NEGATIVE_ONLY"
    negative_config = SourceConfig(slice_doc)
    result = {
        "schema": "PYAT_D2_SRC17_CANONICAL_AUTHORITY_NEGATIVE@1.0.0",
        "source_id": SOURCE_ID,
        "selected_response_ordinal": ordinal,
        "selected_question_id": qid,
        "canonical_value_injected_for_negative_only": True,
        "source_read_performed": True,
    }
    try:
        release = build_validated_c11_release_from_config(negative_config, incidence=incidence)
    except Exception as exc:
        result.update({"status": "REFUSED", "error_type": type(exc).__name__, "error": str(exc), "release_created": False})
        write_json(NEG_CANONICAL_PATH, result)
        return result
    result.update({"status": "UNEXPECTED_SUCCESS", "release_ref": release.release_ref.as_dict()})
    write_json(NEG_CANONICAL_PATH, result)
    raise CampaignError("canonical authority negative unexpectedly succeeded")


def held_slice_negative(config: SourceConfig, selection: Mapping[str, Any], incidence: Any) -> dict[str, Any]:
    response_names = {x["slot"]["name"] for x in config.document["response_slots"]}
    coord_names = {x["slot"]["name"] for x in config.document["coordinate_slots"]}
    held_item = next(item for item in config.document["items"]
                     if item["source_variable_code"] not in response_names | coord_names)
    qid = held_item.get("item_id") or next(q["question_id"] for q in config.document["questions"]
                                            if q["item_evidence"]["implementation_id"] == held_item["implementation_id"])
    question = next(q for q in config.document["questions"] if q["question_id"] == qid)
    slot_name = held_item["source_variable_code"]
    slot = next(x for x in config.document["physical_slots"] if x["name"] == slot_name)
    first_response = deepcopy(config.document["response_slots"][0])
    occurrence = deepcopy(first_response["values"][0]["occurrences"])
    negative_doc = deepcopy(config.document)
    negative_doc["response_slots"] = [{
        "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
        "question_id": qid,
        "values": [{
            "raw_value": 999999.0,
            "missing_state": "OBSERVED_STORAGE_VALUE",
            "source_missing_declaration": None,
            "response_state": "SUBSTANTIVE_RESPONSE",
            "occurrences": occurrence,
            "canonical_value": None,
            "transform_authority_ref": None,
            "extra_authority_refs": [],
        }],
    }]
    negative_doc["coordinate_slots"] = [deepcopy(config.document["coordinate_slots"][0])]
    negative_doc["questions"] = [deepcopy(question)]
    routing = deepcopy(config.document["routing"][0])
    routing["question_id"] = qid
    negative_doc["routing"] = [routing]
    negative_doc["supported_scope"]["supported_question_ids"] = [qid]
    negative_config = SourceConfig(negative_doc)
    result = {
        "schema": "PYAT_D2_SRC17_HELD_SLICE_NEGATIVE@1.0.0",
        "source_id": SOURCE_ID,
        "held_variable": slot_name,
        "held_ordinal": slot["ordinal"],
        "held_disposition": held_item.get("disposition"),
        "fabricated_rule_for_negative_only": True,
        "source_read_performed": True,
    }
    try:
        release = build_validated_c11_release_from_config(negative_config, incidence=incidence)
    except Exception as exc:
        result.update({"status": "REFUSED", "error_type": type(exc).__name__, "error": str(exc), "release_created": False})
        write_json(NEG_HELD_PATH, result)
        return result
    result.update({"status": "UNEXPECTED_SUCCESS", "release_ref": release.release_ref.as_dict()})
    write_json(NEG_HELD_PATH, result)
    raise CampaignError("held-slice negative unexpectedly succeeded")


def _bundle_root() -> Path:
    configured = os.environ.get("D2_SRC17_RUNTIME_ROOT")
    root = Path(configured) if configured else (Path.home() / "Library/Application Support/Rawlsing/campaign-d2-src17")
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
                line = json.dumps(jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"
                gz.write(line)
                raw_bytes += len(line)
                count += 1
    return count, path.stat().st_size, sha_file(path)


def persist_local_release(release: C11LogicalRelease, selection: Mapping[str, Any], decode_receipt: Mapping[str, Any]) -> dict[str, Any]:
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
    receipt = {
        "schema": "PYAT_D2_SRC17_LOCAL_RELEASE@1.0.0",
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
        "replay_manifest": {"file": replay_path.name, "sha256": sha_file(replay_path)},
        "source_custody": dict(decode_receipt.get("source_custody") or {}),
        "local_only": True,
        "raw_respondent_cells_committed": False,
    }
    write_json(bundle_dir / "receipt.json", receipt)
    write_json(LOCAL_PATH, receipt)
    return receipt


def run_primary(scan_only: bool = False) -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    control = verify_control()
    config = load_source_config(CONFIG_PATH)
    if sha_file(CONFIG_PATH) != EXPECTED_CONFIG_FILE_SHA256:
        raise CampaignError("SRC17 config file SHA mismatch")
    if canonical_config_hash(config) != EXPECTED_CONFIG_CANONICAL_SHA256:
        raise CampaignError("SRC17 canonical config hash mismatch")
    if config.document["binding"]["row_count"] != EXPECTED_SOURCE_ROWS:
        raise CampaignError("config row count mismatch")
    if len(config.document["physical_slots"]) != EXPECTED_SOURCE_COLUMNS:
        raise CampaignError("config column count mismatch")
    grant = load_grant()
    request = make_request(config, grant)
    write_json(GRANT_AUTH_PATH, grant_evidence(grant, request, control))
    wrong = wrong_source_negative(config, grant)
    write_json(NEG_WRONG_PATH, wrong)
    if wrong.get("status") != "REFUSED":
        raise CampaignError("wrong-source negative did not refuse")
    incidence, decode_receipt = decode_original(config, grant)
    try:
        if decode_receipt["source_sha256"] != EXPECTED_SOURCE_SHA256:
            raise CampaignError("decoded source SHA mismatch")
        if decode_receipt["rows"] != EXPECTED_SOURCE_ROWS or decode_receipt["columns"] != EXPECTED_SOURCE_COLUMNS:
            raise CampaignError("decoded source shape mismatch")
        if decode_receipt["snapshot_size"] != EXPECTED_SOURCE_BYTES:
            raise CampaignError("decoded source byte size mismatch")
        runtime_config = apply_reader_binding(config, incidence)
        audit = physical_audit(runtime_config, config, incidence)
        selection = scan_slots(runtime_config, incidence)
        if not selection["accounting"]["all_physical_slots_accounted"] or not selection["accounting"]["all_items_accounted"]:
            raise CampaignError("source slot/item accounting failed")
        if scan_only:
            write_json(PRIMARY_PATH, {
                "schema": "PYAT_D2_SRC17_PRIMARY_SCAN@1.0.0",
                "status": "SCAN_COMPLETE_RELEASE_NOT_BUILT",
                "grant": grant_evidence(grant, request, control),
                "decode_receipt": decode_receipt,
                "physical_audit_path": str(AUDIT_PATH.relative_to(ROOT)),
                "selection_path": str(SELECTION_PATH.relative_to(ROOT)),
                "selected_response_slots": selection["selected_response_slots"],
                "selected_coordinate_slots": selection["selected_coordinate_slots"],
                "source_read_performed": True,
            })
            print(json.dumps({
                "status": "SCAN_COMPLETE",
                "rows": decode_receipt["rows"],
                "columns": decode_receipt["columns"],
                "selected_response_slots": len(selection["selected_response_slots"]),
                "held_response_slots": len(selection["held_response_slots"]),
                "selected_coordinate_slots": len(selection["selected_coordinate_slots"]),
            }, indent=2))
            return 0
        held = held_slice_negative(runtime_config, selection, incidence)
        if held.get("status") != "REFUSED":
            raise CampaignError("held-slice negative did not refuse")
        canonical = canonical_negative(runtime_config, selection, incidence)
        if canonical.get("status") != "REFUSED":
            raise CampaignError("canonical authority negative did not refuse")
        slice_config, withheld = build_slice_config(runtime_config, selection, strip_canonical=True)
        started = time.monotonic()
        release = build_validated_c11_release_from_config(slice_config, incidence=incidence)
        build_seconds = round(time.monotonic() - started, 3)
        release_info = release_audit(release, selection)
        if not release_info["passed"]:
            raise CampaignError(f"release audit failed: {release_info['checks']}")
        if release_info["source_artifact_ref"]["content_hash"] != EXPECTED_SOURCE_SHA256:
            raise CampaignError("release source identity mismatch")
        keys = row_native_keys_from_transport(slice_config, incidence=incidence)
        if len(keys) != EXPECTED_SOURCE_ROWS:
            raise CampaignError("source-native key extraction count mismatch")
        local = persist_local_release(release, selection, decode_receipt)
        release_receipt = {
            "schema": "PYAT_D2_SRC17_RELEASE_RECEIPT@1.0.0",
            "source_id": SOURCE_ID,
            "source_path": str(grant["source_path"]),
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "source_rows": EXPECTED_SOURCE_ROWS,
            "source_columns": EXPECTED_SOURCE_COLUMNS,
            "source_bytes": decode_receipt["snapshot_size"],
            "configured_response_slots": len(config.document["response_slots"]),
            "configured_coordinate_slots": len(config.document["coordinate_slots"]),
            "selected_response_slots": selection["selected_response_slots"],
            "selected_question_ids": selection["selected_response_question_ids"],
            "selected_coordinate_slots": selection["selected_coordinate_slots"],
            "held_response_slots": selection["held_response_slots"],
            "held_coordinate_slots": selection["held_coordinate_slots"],
            "source_read_performed": True,
            "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
            "transport": "rawlsing_next.source_configuration.reader.decode_config_with_source_read_permission",
            "accepted_config_path": str(CONFIG_PATH.relative_to(ROOT)),
            "accepted_config_file_sha256": sha_file(CONFIG_PATH),
            "accepted_config_canonical_sha256": canonical_config_hash(config),
            "runtime_config_path": str(RUNTIME_CONFIG_PATH.relative_to(ROOT)),
            "runtime_config_file_sha256": sha_file(RUNTIME_CONFIG_PATH),
            "runtime_config_canonical_sha256": canonical_config_hash(runtime_config),
            "slice_config_canonical_sha256": canonical_config_hash(slice_config),
            "grant_sha256": EXPECTED_GRANT_SHA256,
            "program_sha256": EXPECTED_PROGRAM_SHA256,
            "control_commit": CONTROL_COMMIT,
            "decision_ref": grant["decision_ref"].as_dict(),
            "source_native_key_slots": len(keys),
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
            "canonical_values_withheld": withheld,
            "release": release_info,
            "build_seconds": build_seconds,
            "source_read_receipt": decode_receipt,
            "physical_audit": {
                "path": str(AUDIT_PATH.relative_to(ROOT)),
                "sha256": sha_file(AUDIT_PATH),
                "passed": audit["passed"],
                "checks": audit["checks"],
                "source_native_agreement": "339_OF_339",
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
            "held_slice_negative": held,
            "canonical_authority_negative": canonical,
        }
        write_json(RELEASE_PATH, release_receipt)
        write_json(PRIMARY_PATH, {
            "schema": "PYAT_D2_SRC17_PRIMARY_RUN@1.0.0",
            "status": "PRIMARY_COMPLETE",
            "grant": grant_evidence(grant, request, control),
            "physical_audit_path": str(AUDIT_PATH.relative_to(ROOT)),
            "selection_path": str(SELECTION_PATH.relative_to(ROOT)),
            "negative_wrong_source_path": str(NEG_WRONG_PATH.relative_to(ROOT)),
            "negative_held_slice_path": str(NEG_HELD_PATH.relative_to(ROOT)),
            "negative_canonical_path": str(NEG_CANONICAL_PATH.relative_to(ROOT)),
            "release_receipt_path": str(RELEASE_PATH.relative_to(ROOT)),
            "local_release_receipt_path": str(LOCAL_PATH.relative_to(ROOT)),
            "release_ref": release_info["release_ref"],
            "semantic_release_hash": release_info["semantic_release_hash"],
            "source_read_performed": True,
        })
        print(json.dumps({
            "status": "PRIMARY_COMPLETE",
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "rows": EXPECTED_SOURCE_ROWS,
            "columns": EXPECTED_SOURCE_COLUMNS,
            "selected_response_slots": len(selection["selected_response_slots"]),
            "held_response_slots": len(selection["held_response_slots"]),
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
    primary = load_json(PRIMARY_PATH)
    receipt = load_json(RELEASE_PATH)
    config = load_source_config(CONFIG_PATH)
    grant = load_grant()
    incidence, decode_receipt = decode_original(config, grant)
    try:
        runtime_config = apply_reader_binding(config, incidence)
        audit = physical_audit(runtime_config, config, incidence)
        if not audit["passed"]:
            raise CampaignError("cold replay physical audit failed")
        selection = scan_slots(runtime_config, incidence)
        expected = receipt["release"]
        if selection["selected_response_slots"] != receipt["selected_response_slots"]:
            raise CampaignError("cold replay response selection changed")
        if selection["selected_coordinate_slots"] != receipt["selected_coordinate_slots"]:
            raise CampaignError("cold replay coordinate selection changed")
        slice_config, withheld = build_slice_config(runtime_config, selection, strip_canonical=True)
        release = build_validated_c11_release_from_config(slice_config, incidence=incidence)
        audit = release_audit(release, selection)
        local = load_json(LOCAL_PATH)
        bundle = _bundle_root() / "releases" / local["bundle_id"]
        local_ok = all((bundle / local[key]["file"]).is_file() and sha_file(bundle / local[key]["file"]) == local[key]["sha256"]
                       for key in ("public_objects", "internal_records", "replay_manifest"))
        result = {
            "schema": "PYAT_D2_SRC17_REPLAY_RECEIPT@1.0.0",
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
            "wrong_source_negative_status": load_json(NEG_WRONG_PATH).get("status"),
            "source_read_receipt": decode_receipt,
        }
        if not (result["release_match"] and result["release_audit_passed"] and local_ok):
            raise CampaignError("cold replay did not match primary release")
        write_json(REPLAY_PATH, result)
        print(json.dumps(result, indent=2))
        return 0
    finally:
        incidence.close()


def run_tests() -> int:
    command = [sys.executable, "-m", "pytest", "campaign_d2_src17/tests", "-q", "-o", "addopts="]
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    result = {
        "schema": "PYAT_D2_SRC17_TEST_RESULTS@1.0.0",
        "command": "python3 -m pytest campaign_d2_src17/tests -q -o addopts=",
        "returncode": done.returncode,
        "stdout_tail": done.stdout.strip().splitlines()[-12:],
        "stderr_tail": done.stderr.strip().splitlines()[-12:],
        "passed": done.returncode == 0,
    }
    write_json(TEST_PATH, result)
    print(json.dumps(result, indent=2))
    return 0 if done.returncode == 0 else 1


def _manifest_files() -> list[dict[str, Any]]:
    files = [
        "campaign_d2_src17/run_d2_src17.py",
        "campaign_d2_src17/tests/test_campaign_d2_src17.py",
        "campaign_d2_src17/README.md",
        "campaign_d2_src17/COMMANDS.md",
        "campaign_d2_src17/evidence/USER_GRANT.json",
        "campaign_d2_src17/evidence/TRUE_HQ_GRANT.txt",
        "campaign_d2_src17/evidence/PROGRAM.txt",
        "campaign_d2_src17/evidence/GRANT_AUTHENTICATION.json",
        "campaign_d2_src17/evidence/PHYSICAL_METADATA_AUDIT.json",
        "campaign_d2_src17/evidence/SLICE_SELECTION.json",
        "campaign_d2_src17/evidence/NEGATIVE_WRONG_SOURCE.json",
        "campaign_d2_src17/evidence/NEGATIVE_HELD_SLICE.json",
        "campaign_d2_src17/evidence/NEGATIVE_CANONICAL_AUTHORITY.json",
        "campaign_d2_src17/evidence/RELEASE_RECEIPT.json",
        "campaign_d2_src17/evidence/LOCAL_RELEASE_RECEIPT.json",
        "campaign_d2_src17/evidence/REPLAY_RECEIPT.json",
        "campaign_d2_src17/evidence/TEST_RESULTS.json",
        "campaign_d2_src17/evidence/PRIMARY_RUN.json",
    ]
    out = []
    for rel in files:
        path = ROOT / rel
        if path.is_file():
            out.append({"path": rel, "sha256": sha_file(path), "bytes": path.stat().st_size})
    return out


def run_return(artifact_commit: str) -> int:
    primary = load_json(PRIMARY_PATH)
    receipt = load_json(RELEASE_PATH)
    replay = load_json(REPLAY_PATH)
    tests = load_json(TEST_PATH)
    grant = load_json(GRANT_AUTH_PATH)
    audit = load_json(AUDIT_PATH)
    selection = load_json(SELECTION_PATH)
    wrong = load_json(NEG_WRONG_PATH)
    held = load_json(NEG_HELD_PATH)
    canonical = load_json(NEG_CANONICAL_PATH)
    local = load_json(LOCAL_PATH)
    release = receipt["release"]
    return_document = {
        "schema": "PYAT_D2_SRC17_RETURN@1.0.0",
        "campaign": "D2",
        "source_id": SOURCE_ID,
        "status": "ORIGINAL_SOURCE_C11_RELEASE_COMPLETED__LARGEST_QUALIFIED_SLICE__INDEPENDENT_QUALIFICATION_PENDING",
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
            "accepted_config_path": receipt["accepted_config_path"],
            "accepted_config_file_sha256": receipt["accepted_config_file_sha256"],
            "accepted_config_canonical_sha256": receipt["accepted_config_canonical_sha256"],
            "runtime_config_path": receipt["runtime_config_path"],
            "runtime_config_file_sha256": receipt["runtime_config_file_sha256"],
            "runtime_config_canonical_sha256": receipt["runtime_config_canonical_sha256"],
            "slice_config_canonical_sha256": receipt["slice_config_canonical_sha256"],
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
            "source_read_owner": receipt["source_read_owner"],
            "transport": receipt["transport"],
            "source_io_before_decision": grant["source_io_before_decision"],
        },
        "custody": {
            "source_custody": receipt["source_read_receipt"]["source_custody"],
            "physical_metadata_digest": receipt["source_read_receipt"]["physical_metadata_digest"],
            "physical_audit_passed": audit["passed"],
            "physical_audit_sha256": sha_file(AUDIT_PATH),
            "source_native_agreement": audit["source_native_agreement"],
        },
        "scope": {
            "configured_response_slots": receipt["configured_response_slots"],
            "selected_response_slots": len(selection["selected_response_slots"]),
            "held_response_slots": len(selection["held_response_slots"]),
            "selected_coordinate_slots": len(selection["selected_coordinate_slots"]),
            "held_coordinate_slots": len(selection["held_coordinate_slots"]),
            "selected_question_ids": selection["selected_response_question_ids"],
            "selected_response_ordinals": selection["selected_response_slots"],
            "selected_coordinate_ordinals": selection["selected_coordinate_slots"],
            "held_response_ordinals": selection["held_response_slots"],
            "held_coordinate_ordinals": selection["held_coordinate_slots"],
            "all_339_physical_slots_accounted": selection["accounting"]["all_physical_slots_accounted"],
            "all_339_items_accounted": selection["accounting"]["all_items_accounted"],
            "selection_path": str(SELECTION_PATH.relative_to(ROOT)),
            "selection_sha256": sha_file(SELECTION_PATH),
            "selection_rule": selection["selection_rule"],
        },
        "native": {
            "release_ref": release["release_ref"],
            "semantic_release_hash": release["semantic_release_hash"],
            "source_release_manifest_hash": release["source_release_manifest_hash"],
            "source_artifact_ref": release["source_artifact_ref"],
            "replay_manifest_ref": release["replay_manifest_ref"],
            "public_object_count": release["public_object_count"],
            "internal_record_count": release["internal_record_count"],
            "public_counts": release["public_counts"],
            "internal_counts": release["internal_counts"],
            "m01_m18_coverage_counts": release["m01_m18_coverage_counts"],
            "canonical_response_values": release["canonical_response_values"],
            "canonical_coordinate_values": release["canonical_coordinate_values"],
            "source_native_key_slots": receipt["source_native_key_slots"],
            "checks": release["checks"],
            "passed": release["passed"],
            "release_receipt_sha256": sha_file(RELEASE_PATH),
        },
        "negative_checks": {
            "wrong_source": {"path": str(NEG_WRONG_PATH.relative_to(ROOT)), "sha256": sha_file(NEG_WRONG_PATH), "status": wrong.get("status"), "before_source_io": wrong.get("before_source_io"), "refusal_code": wrong.get("refusal_code")},
            "held_slice": {"path": str(NEG_HELD_PATH.relative_to(ROOT)), "sha256": sha_file(NEG_HELD_PATH), "status": held.get("status"), "held_variable": held.get("held_variable"), "error_type": held.get("error_type")},
            "canonical_authority": {"path": str(NEG_CANONICAL_PATH.relative_to(ROOT)), "sha256": sha_file(NEG_CANONICAL_PATH), "status": canonical.get("status"), "error_type": canonical.get("error_type")},
        },
        "local_release": {
            "bundle_id": local["bundle_id"],
            "replay_manifest_ref": local["replay_manifest_ref"],
            "public_objects": local["public_objects"],
            "internal_records": local["internal_records"],
            "replay_manifest": local["replay_manifest"],
            "local_only": True,
            "raw_respondent_cells_committed": False,
            "local_receipt_path": str(LOCAL_PATH.relative_to(ROOT)),
            "local_receipt_sha256": sha_file(LOCAL_PATH),
        },
        "replay": {
            "status": replay["status"],
            "cold_process": replay["cold_process"],
            "release_match": replay["release_match"],
            "release_audit_passed": replay["release_audit_passed"],
            "local_bundle_exists_and_hashes_match": replay["local_bundle_exists_and_hashes_match"],
            "replay_receipt_sha256": sha_file(REPLAY_PATH),
        },
        "tests": {
            "command": tests["command"],
            "returncode": tests["returncode"],
            "passed": tests["passed"],
            "stdout_tail": tests["stdout_tail"],
            "stderr_tail": tests["stderr_tail"],
            "test_results_sha256": sha_file(TEST_PATH),
        },
        "authority_and_limits": {
            "original_snapshots_unchanged": True,
            "canonical_semantic_ALLOW_claimed": False,
            "canonical_values_withheld": receipt["canonical_values_withheld"],
            "routing_state": "ROUTING_UNKNOWN",
            "weight_scope": "NOT_DECLARED",
            "population_estimation": "NOT_PERFORMED",
            "original_i03_i05": "NOT_ISSUED",
            "additional_source_reads": "NONE",
            "other_holds_unchanged": True,
        },
        "limits": [
            "This is an original SRC17 source-native C11 construction over the largest observed-cell-qualified configured slice; it is not an I03/I05 workload or population estimate.",
            "Original respondent cells and row-wise C11 products remain in the local runtime bundle outside Git.",
            "Canonical authority remains DEFER; no canonical semantic ALLOW is issued.",
            "ROUTING_UNKNOWN and weight-design held premises are preserved.",
            "Held/unbound response/coordinate slots are exact in SLICE_SELECTION.json.",
        ],
        "next_consumer": "Distinct reviewer qualification of the actual original-bound C11 release and D2 acceptance; then Campaign A2/C11 product consumers as separately authorized.",
        "changed_artifacts": _manifest_files(),
        "receipts": {
            "primary": {"path": str(PRIMARY_PATH.relative_to(ROOT)), "sha256": sha_file(PRIMARY_PATH)},
            "grant_authentication": {"path": str(GRANT_AUTH_PATH.relative_to(ROOT)), "sha256": sha_file(GRANT_AUTH_PATH)},
            "physical_metadata_audit": {"path": str(AUDIT_PATH.relative_to(ROOT)), "sha256": sha_file(AUDIT_PATH)},
            "slice_selection": {"path": str(SELECTION_PATH.relative_to(ROOT)), "sha256": sha_file(SELECTION_PATH)},
            "release": {"path": str(RELEASE_PATH.relative_to(ROOT)), "sha256": sha_file(RELEASE_PATH)},
            "local_release": {"path": str(LOCAL_PATH.relative_to(ROOT)), "sha256": sha_file(LOCAL_PATH)},
            "replay": {"path": str(REPLAY_PATH.relative_to(ROOT)), "sha256": sha_file(REPLAY_PATH)},
            "tests": {"path": str(TEST_PATH.relative_to(ROOT)), "sha256": sha_file(TEST_PATH)},
        },
        "no_raw_cells_in_git": True,
        "source_read_performed": True,
        "original_workload_issued": False,
    }
    write_json(RETURN_PATH, return_document)
    print(json.dumps({
        "status": return_document["status"],
        "artifact_commit": artifact_commit,
        "release_ref": release["release_ref"],
        "selected_response_slots": len(selection["selected_response_slots"]),
        "held_response_slots": len(selection["held_response_slots"]),
        "return_path": str(RETURN_PATH.relative_to(ROOT)),
        "return_sha256": sha_file(RETURN_PATH),
    }, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", action="store_true")
    parser.add_argument("--scan-only", action="store_true")
    parser.add_argument("--replay", action="store_true")
    parser.add_argument("--tests", action="store_true")
    parser.add_argument("--return", dest="return_commit")
    args = parser.parse_args(argv)
    if args.scan_only:
        return run_primary(scan_only=True)
    if args.primary:
        return run_primary(scan_only=False)
    if args.replay:
        return run_replay()
    if args.tests:
        return run_tests()
    if args.return_commit:
        return run_return(args.return_commit)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
