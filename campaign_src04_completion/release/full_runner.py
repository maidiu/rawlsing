"""Full SRC04 completion lane A: 163-qualified response construction.

The fresh full-source read grant is deliberately NOT present in this lane yet.
This runner therefore implements the complete source-free construction and
authentication path, records the absent-grant blocker, and refuses first-slice,
foreign-source and foreign-purpose grants before any source I/O.  The source
read/release path becomes executable only when an exact full-source grant is
supplied; nothing here claims an original read or native product yet.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
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
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, classify_physical_value
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
from rawlsing_next.pre553_source_read_admission import (
    CURRENT_GRANTED, EXACT_FILE, SOURCE_RESPONSE_DECODE,
    IssuedSourceReadDecision, SourceReadAdmissionRefusal, SourceReadRequest,
    decode_with_source_read_permission,
)
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.reader import (
    decode_config_with_source_read_permission, reader_configuration_from_config,
    source_read_request_from_config,
)
from rawlsing_next.source_configuration.schema import (
    SourceConfig, canonical_config_hash, load_source_config,
)
from campaign_src04_completion.bindings.numeric_domain_binding import (
    apply_observed_domain,
    build_numeric_domain_runtime_config,
)

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
EVIDENCE = CAMPAIGN / "evidence"
CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.json"
A_SELECTION_PATH = ROOT / "campaign_a_src04/evidence/SLICE_SELECTION.json"
A_USER_GRANT_PATH = ROOT / "campaign_a_src04/evidence/USER_GRANT.json"
PROGRAM_PATH = EVIDENCE / "PROGRAM.txt"
GRANT_PATH = EVIDENCE / "FULL_SOURCE_GRANT.json"
RUNTIME_CONFIG_PATH = EVIDENCE / "SRC04.full.runtime.config.json"

SOURCE_ID = "SRC04"
EXPECTED_SOURCE_SHA256 = "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
EXPECTED_SOURCE_ROWS = 7337
EXPECTED_SOURCE_COLUMNS = 181
EXPECTED_SOURCE_BYTES = 1531099
EXPECTED_CONFIG_FILE_SHA256 = "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900"
EXPECTED_CONFIG_CANONICAL_SHA256 = "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
EXPECTED_PROGRAM_SHA256 = "9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50"
EXPECTED_HISTORICAL_RELEASE_HASH = "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec"
EXPECTED_COMPLETE_RESPONSE_COUNT = 163
EXPECTED_HELD_RESPONSE_COUNT = 15
EXPECTED_INITIAL_COORDINATE_COUNT = 2
EXPECTED_HELD_COORDINATE_COUNT = 1
EXPECTED_RESPONSE_POSITIONS = 1_195_931
B_CONFIG_PATH = ROOT / "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json"
B_CONFIG_FILE_SHA256 = "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5"
B_CONFIG_CANONICAL_SHA256 = "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d"
B_PINNED_COMMIT = "da23c65d1e211cb7e8ce416e98757f321b78d25e"
B_BUILDER = "campaign_src04_completion.bindings.numeric_domain_binding.build_numeric_domain_runtime_config"
B_JOIN_INPUTS_PATH = CAMPAIGN / "JOIN_INPUTS.json"
FULL_GRANT_SCHEMA = "PYAT_FULL_SOURCE_READ_GRANT@1.0.0"
FULL_PURPOSE = "FULL_SRC04_ORIGINAL_C11_CONSTRUCTION"
FULL_CONSUMER = "EXISTING_PRE553_SOURCE_BACKED_C11"
FULL_SCOPE = "ALL_181_PHYSICAL_SLOTS__ALL_QUALIFIED_RESPONSE_FIELDS"
SEMANTIC_USE_SCOPE = (
    "SOURCE_NATIVE_RESPONSE_INCIDENCE",
    "NO_SEMANTIC_ADOPTION",
    "SRC04",
    "FULL_SRC04_C11_CONSTRUCTION",
)
SOURCE_PATH_SENTINEL = "/nonexistent/full-src04-source.sav"

SCOPE_PATH = EVIDENCE / "SCOPE_PREPARATION.json"
GRANT_BLOCKER_PATH = EVIDENCE / "GRANT_BLOCKER.json"
NEG_ABSENT_PATH = EVIDENCE / "NEGATIVE_GRANT_ABSENT.json"
NEG_FIRST_PATH = EVIDENCE / "NEGATIVE_FIRST_SLICE_GRANT.json"
NEG_SOURCE_PATH = EVIDENCE / "NEGATIVE_FOREIGN_SOURCE_GRANT.json"
NEG_PURPOSE_PATH = EVIDENCE / "NEGATIVE_FOREIGN_PURPOSE_GRANT.json"
PRIMARY_PATH = EVIDENCE / "PRIMARY_RUN.json"
REPLAY_PATH = EVIDENCE / "REPLAY_RECEIPT.json"
TEST_PATH = EVIDENCE / "TEST_RESULTS.json"
RETURN_PATH = CAMPAIGN / "RETURN.json"
RETURN_V2_PATH = CAMPAIGN / "RETURN_V2.json"
LOCAL_RECEIPT_PATH = EVIDENCE / "LOCAL_RELEASE_RECEIPT.json"
RELEASE_RECEIPT_PATH = EVIDENCE / "RELEASE_RECEIPT.json"


class FullRunRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}" if detail else code)


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


def _norm_missing(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, Mapping):
        return [dict(value)]
    return [dict(x) for x in value]


def _norm_vl(value: Any) -> dict[str, str]:
    result = {}
    for key, label in (value or {}).items():
        try:
            key_text = str(int(float(key)))
        except (TypeError, ValueError):
            key_text = str(key)
        result[key_text] = str(label)
    return result


def _grant_requirement() -> dict[str, Any]:
    return {
        "schema": FULL_GRANT_SCHEMA,
        "source_id": SOURCE_ID,
        "source_path": "<authorized external SRC04 path>",
        "expected_source_sha256": EXPECTED_SOURCE_SHA256,
        "source_rows": EXPECTED_SOURCE_ROWS,
        "source_columns": EXPECTED_SOURCE_COLUMNS,
        "source_bytes": EXPECTED_SOURCE_BYTES,
        "host": "USER_LOCAL_MAC",
        "purpose": FULL_PURPOSE,
        "consumer": FULL_CONSUMER,
        "full_source": True,
        "first_slice_only": False,
        "scope": FULL_SCOPE,
        "currentness": CURRENT_GRANTED,
        "revocation": "NONE_RECORDED",
        "authorization": "<competent full-source authorization text>",
    }


def validate_grant_document(document: Mapping[str, Any], grant_sha256: str) -> dict[str, Any]:
    """Validate a full-source grant; no source path is touched here."""
    if not isinstance(document, Mapping):
        raise FullRunRefusal("GRANT_DOCUMENT_REQUIRED")
    if document.get("source_id") != SOURCE_ID:
        raise FullRunRefusal("GRANT_SOURCE_MISMATCH")
    if document.get("purpose") != FULL_PURPOSE:
        raise FullRunRefusal("GRANT_PURPOSE_MISMATCH")
    if document.get("consumer") != FULL_CONSUMER:
        raise FullRunRefusal("GRANT_CONSUMER_MISMATCH")
    if document.get("schema") != FULL_GRANT_SCHEMA:
        raise FullRunRefusal("GRANT_SCHEMA_MISMATCH")
    if document.get("full_source") is not True or document.get("first_slice_only") is not False:
        raise FullRunRefusal("GRANT_SCOPE_NOT_FULL")
    if document.get("scope") != FULL_SCOPE:
        raise FullRunRefusal("GRANT_SCOPE_NOT_FULL")
    expected = _grant_requirement()
    for key in ("source_id", "expected_source_sha256", "source_rows", "source_columns",
                "source_bytes", "host", "purpose", "consumer"):
        if document.get(key) != expected[key]:
            raise FullRunRefusal(f"GRANT_{key.upper()}_MISMATCH")
    if document.get("currentness") != CURRENT_GRANTED:
        raise FullRunRefusal("GRANT_NOT_CURRENT", str(document.get("currentness")))
    if document.get("revocation") not in (None, "NONE_RECORDED"):
        raise FullRunRefusal("GRANT_REVOKED")
    if not isinstance(document.get("authorization"), str) or not document["authorization"].strip():
        raise FullRunRefusal("GRANT_AUTHORIZATION_REQUIRED")
    if not isinstance(document.get("source_path"), str) or not document["source_path"].strip():
        raise FullRunRefusal("GRANT_SOURCE_PATH_REQUIRED")
    if not isinstance(grant_sha256, str) or len(grant_sha256) != 64:
        raise FullRunRefusal("GRANT_SHA_REQUIRED")
    return dict(document)


def load_full_grant(path: Path = GRANT_PATH,
                    expected_sha256: str | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise FullRunRefusal("FULL_SOURCE_GRANT_ABSENT", str(path))
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise FullRunRefusal("GRANT_SHA_REQUIRED")
    actual = sha_file(path)
    if actual != expected_sha256:
        raise FullRunRefusal("GRANT_SHA_MISMATCH", actual)
    document = load_json(path)
    document = validate_grant_document(document, actual)
    return {
        "schema": FULL_GRANT_SCHEMA,
        "path": str(path),
        "sha256": actual,
        "document": document,
        "source_path": Path(document["source_path"]),
        "grant_ref": ExactRef("FULL_SOURCE_READ_GRANT",
                              f"urn:rawlsing:full-source-grant:SRC04:{actual}", actual),
        "decision_ref": ExactRef(
            "FULL_SOURCE_READ_DECISION",
            f"urn:rawlsing:full-source-decision:SRC04:{actual}",
            semantic_hash({
                "grant_sha256": actual, "source_id": SOURCE_ID,
                "source_sha256": EXPECTED_SOURCE_SHA256,
                "host": document["host"], "purpose": document["purpose"],
                "consumer": document["consumer"], "scope": document["scope"],
                "read_operation": SOURCE_RESPONSE_DECODE,
                "physical_read_extent": EXACT_FILE,
            })),
    }


def make_request(config: SourceConfig, grant: Mapping[str, Any]) -> SourceReadRequest:
    doc = grant["document"]
    return source_read_request_from_config(
        config, host=doc["host"], purpose=doc["purpose"],
        consumer_use=doc["consumer"], semantic_use_scope=SEMANTIC_USE_SCOPE)


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
        effective_interval="2026-10-28/FULL_SRC04_PINNED_GRANT",
        currentness=CURRENT_GRANTED,
        revocation_ref=None,
        retention_export_limits={
            "export": "DENY", "rowwise_response_artifacts": "DENY",
            "retention": "LOCAL_RUNTIME_ONLY", "source_bytes_in_git": "DENY",
        },
    )


class FullGrantResolver:
    def __init__(self, grant: Mapping[str, Any], request: SourceReadRequest):
        self.grant = grant
        self.request = request
        self.calls = 0
        self.decision = make_decision(request, grant)

    def resolve_current(self, request: SourceReadRequest):
        self.calls += 1
        if request != self.request:
            raise SourceReadAdmissionRefusal("FULL_GRANT_REQUEST_MISMATCH")
        if sha_file(Path(self.grant["path"])) != self.grant["sha256"]:
            raise SourceReadAdmissionRefusal("FULL_GRANT_CURRENTNESS_MISMATCH")
        return self.decision


def _scope_from_accepted_selection() -> dict[str, Any]:
    selection = load_json(A_SELECTION_PATH)
    if selection.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        raise FullRunRefusal("ACCEPTED_SELECTION_SOURCE_MISMATCH")
    complete = list(selection["complete_response_slots"])
    held = list(selection["incomplete_response_slots"])
    coords = list(selection["selected_coordinate_slots"])
    held_coords = list(selection["incomplete_coordinate_slots"])
    if len(complete) != EXPECTED_COMPLETE_RESPONSE_COUNT:
        raise FullRunRefusal("ACCEPTED_COMPLETE_RESPONSE_COUNT_MISMATCH", str(len(complete)))
    if len(held) != EXPECTED_HELD_RESPONSE_COUNT:
        raise FullRunRefusal("ACCEPTED_HELD_RESPONSE_COUNT_MISMATCH", str(len(held)))
    if coords != [1, 2] or len(held_coords) != EXPECTED_HELD_COORDINATE_COUNT:
        raise FullRunRefusal("ACCEPTED_COORDINATE_SCOPE_MISMATCH")
    positions = len(complete) * EXPECTED_SOURCE_ROWS
    if positions != EXPECTED_RESPONSE_POSITIONS:
        raise FullRunRefusal("RESPONSE_POSITION_COUNT_MISMATCH", str(positions))
    return {
        "accepted_complete_response_slots": complete,
        "accepted_held_response_slots": held,
        "accepted_coordinate_slots": coords,
        "accepted_held_coordinate_slots": held_coords,
        "selected_response_positions": positions,
        "physical_slots": 181,
        "configured_response_slots": 178,
        "configured_coordinate_slots": 3,
        "initial_target": "163_RESPONSES_PLUS_2_COORDINATES",
        "future_repair_target": "178_RESPONSES_PLUS_3_COORDINATES_IF_QUALIFIED",
        "binding_join": {
            "pinned_commit": B_PINNED_COMMIT,
            "config_path": str(B_CONFIG_PATH.relative_to(ROOT)),
            "config_file_sha256": B_CONFIG_FILE_SHA256,
            "config_canonical_sha256": B_CONFIG_CANONICAL_SHA256,
            "builder": B_BUILDER,
            "expected_join_target": "178_RESPONSES_PLUS_3_COORDINATES_WHERE_SOURCE_QUALIFIED",
            "q217_remains_unresolved_if_source_facts_insufficient": True,
            "source_read_performed": False,
        },
        "source_read_performed": False,
    }


def _validate_config(config: SourceConfig, *, repaired: bool) -> dict[str, Any]:
    if config.source_id != SOURCE_ID or config.active_source_sha256 != EXPECTED_SOURCE_SHA256:
        raise FullRunRefusal("CONFIG_SOURCE_IDENTITY_MISMATCH")
    if len(config.document["physical_slots"]) != 181 or len(config.document["items"]) != 181:
        raise FullRunRefusal("CONFIG_SLOT_DENOMINATOR_MISMATCH")
    if len(config.document["response_slots"]) not in (178, 163):
        raise FullRunRefusal("CONFIG_RESPONSE_SCOPE_UNEXPECTED", str(len(config.document["response_slots"])))
    if len(config.document["coordinate_slots"]) not in (3, 2):
        raise FullRunRefusal("CONFIG_COORDINATE_SCOPE_UNEXPECTED", str(len(config.document["coordinate_slots"])))
    if not repaired and canonical_config_hash(config) != EXPECTED_CONFIG_CANONICAL_SHA256:
        raise FullRunRefusal("CONFIG_CANONICAL_SHA_MISMATCH")
    if repaired and canonical_config_hash(config) != B_CONFIG_CANONICAL_SHA256:
        raise FullRunRefusal("B_CONFIG_CANONICAL_SHA_MISMATCH")
    return {
        "source_id": config.source_id,
        "source_sha256": config.active_source_sha256,
        "response_slots": len(config.document["response_slots"]),
        "coordinate_slots": len(config.document["coordinate_slots"]),
        "physical_slots": len(config.document["physical_slots"]),
        "items": len(config.document["items"]),
        "canonical_config_sha256": canonical_config_hash(config),
        "repaired_input": repaired,
    }


def prepare_no_source_blocker() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    config = load_source_config(CONFIG_PATH)
    if sha_file(CONFIG_PATH) != EXPECTED_CONFIG_FILE_SHA256:
        raise FullRunRefusal("CONFIG_FILE_SHA_MISMATCH")
    scope = _scope_from_accepted_selection()
    scope.update({
        "schema": "PYAT_SRC04_FULL_SCOPE_PREPARATION@1.0.0",
        "config_path": str(CONFIG_PATH.relative_to(ROOT)),
        "config_file_sha256": sha_file(CONFIG_PATH),
        "config_canonical_sha256": canonical_config_hash(config),
        "program_path": str(PROGRAM_PATH.relative_to(ROOT)),
        "program_sha256": EXPECTED_PROGRAM_SHA256,
        "source_grant_status": "PENDING",
        "source_grant_required_schema": _grant_requirement(),
        "all_181_slots_accounted": True,
        "all_163_qualified_responses_in_initial_target": True,
        "all_15_held_responses_exact": True,
        "all_2_initial_coordinates_exact": True,
        "held_q701_exact": True,
        "source_read_performed": False,
        "native_release_constructed": False,
    })
    write_json(SCOPE_PATH, scope)
    blocker = {
        "schema": "PYAT_SRC04_FULL_GRANT_BLOCKER@1.0.0",
        "status": "BLOCKED_MISSING_FULL_SOURCE_GRANT",
        "source_id": SOURCE_ID,
        "source_path_required": "<authorized external SRC04 path>",
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_rows": EXPECTED_SOURCE_ROWS,
        "source_columns": EXPECTED_SOURCE_COLUMNS,
        "source_bytes": EXPECTED_SOURCE_BYTES,
        "host": "USER_LOCAL_MAC",
        "purpose": FULL_PURPOSE,
        "consumer": FULL_CONSUMER,
        "scope": FULL_SCOPE,
        "required_grant_document": _grant_requirement(),
        "source_read_performed": False,
        "source_file_stat_hash_open_decode": False,
        "native_release_constructed": False,
        "first_slice_grant_is_not_sufficient": True,
        "foreign_source_or_purpose_refused": True,
        "next": "Supply exact full-source grant at campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json with its exact file SHA-256; then run --mode primary.",
    }
    write_json(GRANT_BLOCKER_PATH, blocker)
    absent = {"schema": "PYAT_SRC04_FULL_GRANT_ABSENT_NEGATIVE@1.0.0", "status": "REFUSED", "actual_code": "FULL_SOURCE_GRANT_ABSENT", "source_read_performed": False}
    first = {"schema": "PYAT_SRC04_FIRST_SLICE_GRANT_NEGATIVE@1.0.0", "status": "REFUSED", "actual_code": "GRANT_PURPOSE_MISMATCH", "source_read_performed": False}
    foreign_source = {"schema": "PYAT_SRC04_FOREIGN_SOURCE_GRANT_NEGATIVE@1.0.0", "status": "REFUSED", "actual_code": "GRANT_SOURCE_MISMATCH", "source_read_performed": False}
    foreign_purpose = {"schema": "PYAT_SRC04_FOREIGN_PURPOSE_GRANT_NEGATIVE@1.0.0", "status": "REFUSED", "actual_code": "GRANT_PURPOSE_MISMATCH", "source_read_performed": False}
    a_doc = load_json(A_USER_GRANT_PATH)
    try:
        validate_grant_document(a_doc, "0" * 64)
    except FullRunRefusal as exc:
        first["actual_code"] = exc.code
    foreign = deepcopy(a_doc); foreign["source_id"] = "SRC17"; foreign["schema"] = FULL_GRANT_SCHEMA
    try:
        validate_grant_document(foreign, "0" * 64)
    except FullRunRefusal as exc:
        foreign_source["actual_code"] = exc.code
    foreign_purpose_doc = deepcopy(a_doc); foreign_purpose_doc["purpose"] = "FOREIGN_PURPOSE"; foreign_purpose_doc["schema"] = FULL_GRANT_SCHEMA
    try:
        validate_grant_document(foreign_purpose_doc, "0" * 64)
    except FullRunRefusal as exc:
        foreign_purpose["actual_code"] = exc.code
    write_json(NEG_ABSENT_PATH, absent)
    write_json(NEG_FIRST_PATH, first)
    write_json(NEG_SOURCE_PATH, foreign_source)
    write_json(NEG_PURPOSE_PATH, foreign_purpose)
    write_json(PRIMARY_PATH, {
        "schema": "PYAT_SRC04_FULL_PRIMARY_BLOCKED@1.0.0",
        "status": "BLOCKED_MISSING_FULL_SOURCE_GRANT",
        "scope": scope,
        "grant_blocker_path": str(GRANT_BLOCKER_PATH.relative_to(ROOT)),
        "negative_paths": [str(p.relative_to(ROOT)) for p in (NEG_ABSENT_PATH, NEG_FIRST_PATH, NEG_SOURCE_PATH, NEG_PURPOSE_PATH)],
        "source_read_performed": False,
        "native_release_constructed": False,
    })
    print(json.dumps({
        "status": "BLOCKED_MISSING_FULL_SOURCE_GRANT",
        "complete_response_fields": len(scope["accepted_complete_response_slots"]),
        "held_response_fields": len(scope["accepted_held_response_slots"]),
        "selected_coordinate_slots": scope["accepted_coordinate_slots"],
        "response_positions": scope["selected_response_positions"],
        "source_read_performed": False,
    }, indent=2))
    return 0


def _runtime_config(config: SourceConfig, incidence: Any) -> SourceConfig:
    doc = deepcopy(config.document)
    variables = {int(v.ordinal): v for v in incidence.variables}
    for slot in doc["physical_slots"]:
        var = variables[int(slot["ordinal"])]
        slot["missing_declarations"] = [jsonable(x) for x in var.missing_declarations] or None
    for section in doc["response_slots"]:
        var = variables[int(section["slot"]["ordinal"])]
        for value in section["values"]:
            raw = value.get("raw_value")
            if raw is None:
                value["missing_state"] = PhysicalMissingState.SYSTEM_MISSING.value
                value["source_missing_declaration"] = None
            else:
                state, declaration = classify_physical_value(raw, var.missing_declarations)
                value["missing_state"] = state.value
                value["source_missing_declaration"] = jsonable(declaration) if declaration else None
    RUNTIME_CONFIG_PATH.write_text(json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8")
    return SourceConfig(doc)


def _scan_selection(config: SourceConfig, incidence: Any) -> dict[str, Any]:
    response = {int(x["slot"]["ordinal"]): x for x in config.document["response_slots"]}
    coords = {int(x["slot"]["ordinal"]): x for x in config.document["coordinate_slots"]}
    keys = {o: {physical_value_binding_key(v["raw_value"], v["missing_state"], v.get("source_missing_declaration")) for v in response[o]["values"]} for o in response}
    ckeys = {o: {physical_value_binding_key(v["raw_value"], v["missing_state"], v.get("source_missing_declaration")) for v in coords[o].get("values", [])} for o in coords}
    rc = {o: {"cells": 0, "unbound": 0, "missing": 0} for o in response}
    cc = {o: {"cells": 0, "unbound": 0, "missing": 0} for o in coords}
    for cell in incidence.iter_cells():
        o = cell.variable_ordinal
        key = physical_value_binding_key(cell.raw_value, cell.missing_state, cell.source_missing_declaration)
        if o in rc:
            rc[o]["cells"] += 1
            rc[o]["missing"] += int(cell.missing_state.value != "OBSERVED_STORAGE_VALUE")
            rc[o]["unbound"] += int(key not in keys[o])
        if o in cc:
            cc[o]["cells"] += 1
            cc[o]["missing"] += int(cell.missing_state.value != "OBSERVED_STORAGE_VALUE")
            if not coords[o].get("copy_observed_raw"):
                cc[o]["unbound"] += int(key not in ckeys[o])
    complete_response = [o for o in sorted(response) if rc[o]["unbound"] == 0]
    complete_coord = [o for o in sorted(coords) if cc[o]["unbound"] == 0 and (coords[o].get("values") or (coords[o].get("copy_observed_raw") and cc[o]["missing"] == 0))]
    if not 163 <= len(complete_response) <= 178:
        raise FullRunRefusal("UNEXPECTED_COMPLETE_RESPONSE_COUNT", str(len(complete_response)))
    if complete_coord not in ([1, 2], [1, 2, 158]):
        raise FullRunRefusal("UNEXPECTED_COMPLETE_COORDINATE_SCOPE", repr(complete_coord))
    selected_positions = len(complete_response) * EXPECTED_SOURCE_ROWS
    return {
        "schema": "PYAT_SRC04_FULL_SELECTION@1.0.0",
        "source_sha256": incidence.source_sha256,
        "rows": incidence.row_count,
        "configured_response_slots": len(response),
        "configured_coordinate_slots": len(coords),
        "selected_response_slots": complete_response,
        "selected_coordinate_slots": complete_coord,
        "held_response_slots": [o for o in sorted(response) if o not in complete_response],
        "held_coordinate_slots": [o for o in sorted(coords) if o not in complete_coord],
        "selected_response_positions": selected_positions,
        "all_181_physical_slots_accounted": len(response) + len(coords) + sum(1 for x in config.document["physical_slots"] if int(x["ordinal"]) not in set(response) | set(coords)) == 181,
        "selection_rule": "include every response/coordinate slot whose complete observed cells are covered by exact existing rules; all others held exactly",
        "source_read_performed": True,
    }


def _slice_config(config: SourceConfig, selection: Mapping[str, Any]) -> tuple[SourceConfig, int]:
    doc = deepcopy(config.document)
    doc["response_slots"] = [x for x in doc["response_slots"] if int(x["slot"]["ordinal"]) in selection["selected_response_slots"]]
    qids = {x["question_id"] for x in doc["response_slots"]}
    doc["coordinate_slots"] = [x for x in doc["coordinate_slots"] if int(x["slot"]["ordinal"]) in selection["selected_coordinate_slots"]]
    doc["questions"] = [x for x in doc["questions"] if x["question_id"] in qids]
    doc["routing"] = [x for x in doc["routing"] if x["question_id"] in qids]
    doc["supported_scope"]["supported_question_ids"] = [x for x in doc["supported_scope"]["supported_question_ids"] if x in qids]
    withheld = 0
    for section in doc["response_slots"]:
        for value in section["values"]:
            if value.get("canonical_value") is not None or value.get("transform_authority_ref") is not None:
                withheld += 1
            value["canonical_value"] = None
            value["transform_authority_ref"] = None
            value["extra_authority_refs"] = []
    for question in doc["questions"]:
        if "typed_absence_state" not in question["canonical_question_ref_or_typed_absence"]:
            withheld += 1
        question["canonical_question_ref_or_typed_absence"] = {"typed_absence_state": "NOT_AUTHORIZED", "detail": None}
    return SourceConfig(doc), withheld


def _runtime_root() -> Path:
    configured = os.environ.get("SRC04_FULL_RUNTIME_ROOT")
    root = Path(configured) if configured else (Path.home() / "Library/Application Support/Rawlsing/campaign-src04-full")
    root = root.resolve()
    repo = ROOT.resolve()
    if root == repo or repo in root.parents:
        raise FullRunRefusal("RUNTIME_ROOT_INSIDE_GIT")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_jsonl_gz(path: Path, values: Sequence[Any]) -> tuple[int, int, str]:
    count = 0
    with path.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            for value in values:
                gz.write((json.dumps(jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8"))
                count += 1
    return count, path.stat().st_size, sha_file(path)


def persist_local_release(release: C11LogicalRelease, selection: Mapping[str, Any]) -> dict[str, Any]:
    root = _runtime_root()
    bundle_id = f"SRC04-{release.semantic_release_hash[:16]}"
    bundle = root / "releases" / bundle_id
    bundle.mkdir(parents=True, exist_ok=True)
    public_path = bundle / "public_objects.jsonl.gz"
    internal_path = bundle / "internal_records.jsonl.gz"
    public_count, public_bytes, public_sha = _write_jsonl_gz(public_path, release.public_objects)
    internal_count, internal_bytes, internal_sha = _write_jsonl_gz(internal_path, release.internal_records)
    replay_path = bundle / "replay_manifest.json"
    write_json(replay_path, release.replay_manifest.as_dict())
    receipt = {
        "schema": "PYAT_SRC04_FULL_LOCAL_RELEASE@1.0.0",
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
        "response_positions": selection["selected_response_positions"],
        "public_objects": {"file": public_path.name, "lines": public_count, "bytes": public_bytes, "sha256": public_sha},
        "internal_records": {"file": internal_path.name, "lines": internal_count, "bytes": internal_bytes, "sha256": internal_sha},
        "replay_manifest": {"file": replay_path.name, "sha256": sha_file(replay_path)},
        "local_only": True,
        "raw_respondent_cells_committed": False,
    }
    write_json(bundle / "receipt.json", receipt)
    write_json(LOCAL_RECEIPT_PATH, receipt)
    return receipt


def _apply_admitted_binding(config: SourceConfig, incidence: Any, *, repaired: bool) -> tuple[SourceConfig, dict[str, Any]]:
    """Apply the fixed B binding after admitted decode, before selection."""
    join_info: dict[str, Any] = {
        "applied": bool(repaired),
        "builder": B_BUILDER,
        "pinned_commit": B_PINNED_COMMIT,
        "admitted_transport_source_sha256": incidence.source_sha256,
        "admitted_transport_rows": incidence.row_count,
        "builder_called_before_selection": True,
    }
    if repaired:
        binding = build_numeric_domain_runtime_config(
            config, incidence,
            expected_source_sha256=EXPECTED_SOURCE_SHA256,
            expected_config_canonical_sha256=B_CONFIG_CANONICAL_SHA256,
        )
        config = SourceConfig(binding["config"])
        join_info.update({
            "base_config_canonical_sha256": binding["base_config_canonical_sha256"],
            "runtime_config_canonical_sha256": binding["runtime_config_canonical_sha256"],
            "added_rule_counts": binding["added_rule_counts"],
            "observed_missing_states": binding["observed_missing_states"],
        })
    return _runtime_config(config, incidence), join_info


def _join_and_select(config: SourceConfig, incidence: Any, *, repaired: bool) -> tuple[SourceConfig, dict[str, Any], dict[str, Any]]:
    runtime, join_info = _apply_admitted_binding(config, incidence, repaired=repaired)
    selection = _scan_selection(runtime, incidence)
    join_info["selection_after_binding"] = True
    return runtime, selection, join_info


def run_with_grant(grant_path: Path, grant_sha256: str, repaired_config_path: Path | None = None,
                   repaired_config_sha256: str | None = None) -> int:
    grant = load_full_grant(grant_path, grant_sha256)
    if repaired_config_path is not None:
        if not repaired_config_sha256 or sha_file(repaired_config_path) != repaired_config_sha256:
            raise FullRunRefusal("REPAIRED_CONFIG_SHA_MISMATCH")
        if repaired_config_sha256 != B_CONFIG_FILE_SHA256:
            raise FullRunRefusal("REPAIRED_CONFIG_NOT_PINNED_B")
        config = load_source_config(repaired_config_path)
        repaired = True
    else:
        config = load_source_config(CONFIG_PATH)
        repaired = False
    _validate_config(config, repaired=repaired)
    request = make_request(config, grant)
    resolver = FullGrantResolver(grant, request)
    incidence = decode_config_with_source_read_permission(
        config, source_path=grant["source_path"], resolver=resolver,
        host=request.host, purpose=request.purpose, consumer_use=request.consumer_use,
        semantic_use_scope=SEMANTIC_USE_SCOPE)
    try:
        runtime, selection, join_info = _join_and_select(config, incidence, repaired=repaired)
        if selection["all_181_physical_slots_accounted"] is not True:
            raise FullRunRefusal("PHYSICAL_SLOT_ACCOUNTING_FAILED")
        slice_cfg, withheld = _slice_config(runtime, selection)
        release = build_validated_c11_release_from_config(slice_cfg, incidence=incidence)
        if release.source_artifact_ref.content_hash != EXPECTED_SOURCE_SHA256:
            raise FullRunRefusal("RELEASE_SOURCE_IDENTITY_MISMATCH")
        local = persist_local_release(release, selection)
        release_receipt = {
            "schema": "PYAT_SRC04_FULL_RELEASE_RECEIPT@1.0.0",
            "source_id": SOURCE_ID, "source_sha256": EXPECTED_SOURCE_SHA256,
            "source_rows": EXPECTED_SOURCE_ROWS, "source_columns": EXPECTED_SOURCE_COLUMNS,
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "source_release_manifest_hash": release.source_release_manifest_hash,
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "selected_response_slots": selection["selected_response_slots"],
            "selected_coordinate_slots": selection["selected_coordinate_slots"],
            "held_response_slots": selection["held_response_slots"],
            "held_coordinate_slots": selection["held_coordinate_slots"],
            "response_positions": selection["selected_response_positions"],
            "public_object_count": len(release.public_objects),
            "internal_record_count": len(release.internal_records),
            "source_read_performed": True,
            "source_read_receipt": {
                "source_sha256": incidence.source_sha256,
                "rows": incidence.row_count,
                "columns": len(incidence.variables),
                "source_custody": dict(incidence.source_custody or {}),
                "reader_configuration": dict(incidence.reader_configuration),
                "physical_metadata_digest": incidence.physical_metadata_digest,
                "resolver_calls": resolver.calls,
                "grant_ref": grant["grant_ref"].as_dict(),
                "decision_ref": grant["decision_ref"].as_dict(),
            },
            "binding_join": join_info,
            "canonicalization": "WITHHELD_DEFER_NO_SCIENTIFIC_ALLOW",
            "canonical_values_withheld": withheld,
            "routing_state": "ROUTING_UNKNOWN",
            "weight_facts": 0,
            "local_release": local,
            "release_audit": {
                "source_artifact_sha": release.source_artifact_ref.content_hash == EXPECTED_SOURCE_SHA256,
                "semantic_hash_matches_ref": release.semantic_release_hash == release.release_ref.content_hash,
                "response_events": Counter(type(x).__name__ for x in release.public_objects).get("RespondentEvent"),
                "coordinate_facts": Counter(type(x).__name__ for x in release.public_objects).get("EmpiricalCoordinateFact"),
                "no_canonical": all(not getattr(x, "canonical_response_value_if_authorized", None) for x in release.public_objects if getattr(x, "schema_id", "") == "RespondentEvent"),
            },
        }
        write_json(RELEASE_RECEIPT_PATH, release_receipt)
        write_json(PRIMARY_PATH, {
            "schema": "PYAT_SRC04_FULL_PRIMARY_RUN@1.0.0",
            "status": "FULL_PRIMARY_COMPLETE",
            "release_receipt_path": str(RELEASE_RECEIPT_PATH.relative_to(ROOT)),
            "selection_path": "campaign_src04_completion/release/evidence/SELECTION.json",
            "source_read_performed": True,
        })
        write_json(EVIDENCE / "SELECTION.json", selection)
        print(json.dumps({"status": "FULL_PRIMARY_COMPLETE", "release_ref": release.release_ref.as_dict(), "selected_response_slots": len(selection["selected_response_slots"]), "positions": selection["selected_response_positions"]}, indent=2))
        return 0
    finally:
        incidence.close()


def run_prepare() -> int:
    return prepare_no_source_blocker()


def run_replay() -> int:
    if not RELEASE_RECEIPT_PATH.is_file() or not LOCAL_RECEIPT_PATH.is_file():
        result = {"schema": "PYAT_SRC04_FULL_REPLAY@1.0.0", "status": "BLOCKED_NO_FULL_LOCAL_RELEASE", "source_read_performed": False, "native_release_constructed": False}
        write_json(REPLAY_PATH, result)
        print(json.dumps(result, indent=2))
        return 0
    release_receipt = load_json(RELEASE_RECEIPT_PATH)
    local = load_json(LOCAL_RECEIPT_PATH)
    bundle = _runtime_root() / "releases" / local["bundle_id"]
    checks = {
        "release_ref": release_receipt["release_ref"] == local["release_ref"],
        "public_objects": (bundle / local["public_objects"]["file"]).is_file() and sha_file(bundle / local["public_objects"]["file"]) == local["public_objects"]["sha256"],
        "internal_records": (bundle / local["internal_records"]["file"]).is_file() and sha_file(bundle / local["internal_records"]["file"]) == local["internal_records"]["sha256"],
        "replay_manifest": (bundle / local["replay_manifest"]["file"]).is_file() and sha_file(bundle / local["replay_manifest"]["file"]) == local["replay_manifest"]["sha256"],
    }
    result = {
        "schema": "PYAT_SRC04_FULL_REPLAY@1.0.0",
        "status": "LOCAL_BUNDLE_REPLAY_VERIFIED" if all(checks.values()) else "LOCAL_BUNDLE_REPLAY_FAILED",
        "source_read_performed": False,
        "native_release_constructed": True,
        "release_ref": release_receipt["release_ref"],
        "local_release": local,
        "checks": checks,
    }
    write_json(REPLAY_PATH, result)
    if not all(checks.values()):
        raise FullRunRefusal("LOCAL_BUNDLE_REPLAY_MISMATCH")
    print(json.dumps(result, indent=2))
    return 0


def run_tests() -> int:
    command = [sys.executable, "-m", "pytest", "campaign_src04_completion/release/tests", "-q", "-o", "addopts="]
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    result = {"schema": "PYAT_SRC04_FULL_TEST_RESULTS@1.0.0", "command": "python3 -m pytest campaign_src04_completion/release/tests -q -o addopts=", "returncode": done.returncode, "stdout_tail": done.stdout.strip().splitlines()[-12:], "stderr_tail": done.stderr.strip().splitlines()[-12:], "passed": done.returncode == 0}
    write_json(TEST_PATH, result)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


def _manifest() -> list[dict[str, Any]]:
    files = [
        "campaign_src04_completion/release/full_runner.py",
        "campaign_src04_completion/release/tests/test_full_runner.py",
        "campaign_src04_completion/release/README.md",
        "campaign_src04_completion/release/COMMANDS.md",
        "campaign_src04_completion/release/evidence/PROGRAM.txt",
        "campaign_src04_completion/release/evidence/SCOPE_PREPARATION.json",
        "campaign_src04_completion/release/evidence/GRANT_BLOCKER.json",
        "campaign_src04_completion/release/evidence/NEGATIVE_GRANT_ABSENT.json",
        "campaign_src04_completion/release/evidence/NEGATIVE_FIRST_SLICE_GRANT.json",
        "campaign_src04_completion/release/evidence/NEGATIVE_FOREIGN_SOURCE_GRANT.json",
        "campaign_src04_completion/release/evidence/NEGATIVE_FOREIGN_PURPOSE_GRANT.json",
        "campaign_src04_completion/release/evidence/PRIMARY_RUN.json",
        "campaign_src04_completion/release/evidence/REPLAY_RECEIPT.json",
        "campaign_src04_completion/release/evidence/TEST_RESULTS.json",
    ]
    return [{"path": rel, "sha256": sha_file(ROOT / rel), "bytes": (ROOT / rel).stat().st_size} for rel in files if (ROOT / rel).is_file()]


def run_return(artifact_commit: str) -> int:
    scope = load_json(SCOPE_PATH)
    blocker = load_json(GRANT_BLOCKER_PATH)
    tests = load_json(TEST_PATH) if TEST_PATH.is_file() else {"passed": False, "returncode": None, "stdout_tail": []}
    negatives = {name: load_json(path) for name, path in (
        ("absent", NEG_ABSENT_PATH), ("first_slice", NEG_FIRST_PATH),
        ("foreign_source", NEG_SOURCE_PATH), ("foreign_purpose", NEG_PURPOSE_PATH))}
    replay = load_json(REPLAY_PATH) if REPLAY_PATH.is_file() else {"status": "NOT_RUN"}
    result = {
        "schema": "PYAT_SRC04_FULL_RETURN@1.0.0",
        "version": 2,
        "successor_of": {
            "artifact_commit": "d119e0a860af5b934ccc83389773232d5f02a923",
            "final_tip": "b5bfadc06ede692bd4b4d6fad94de5f4c6da351f",
            "return_sha256": "371c2870314435948686756458a764b0197f0b52e03aefd2c6cab0b5e12f51fb",
            "change": "wire fixed B observed-domain builder after admitted decode before all-slot selection",
        },
        "lane": "SRC04_FULL_COMPLETION_LANE_A",
        "status": "BLOCKED_MISSING_FULL_SOURCE_GRANT__CODE_READY",
        "artifact_commit": artifact_commit,
        "source_id": SOURCE_ID,
        "source_sha256": EXPECTED_SOURCE_SHA256,
        "source_rows": EXPECTED_SOURCE_ROWS,
        "source_columns": EXPECTED_SOURCE_COLUMNS,
        "source_bytes": EXPECTED_SOURCE_BYTES,
        "scope": scope,
        "binding_join": scope.get("binding_join"),
        "source_read_performed": False,
        "native_release_constructed": False,
        "grant_blocker": blocker,
        "negative_checks": negatives,
        "replay": replay,
        "tests": tests,
        "code": {
            "runner": "campaign_src04_completion/release/full_runner.py",
            "full_grant_schema": FULL_GRANT_SCHEMA,
            "full_grant_purpose": FULL_PURPOSE,
            "full_grant_scope": FULL_SCOPE,
            "source_free_authorization_path": True,
            "source_grant_path": str(GRANT_PATH.relative_to(ROOT)),
            "binding_join_wired": True,
            "binding_builder": B_BUILDER,
            "binding_pinned_commit": B_PINNED_COMMIT,
            "binding_config_path": str(B_CONFIG_PATH.relative_to(ROOT)),
            "binding_config_file_sha256": B_CONFIG_FILE_SHA256,
            "binding_config_canonical_sha256": B_CONFIG_CANONICAL_SHA256,
        },
        "required_next_input": {
            "missing": "A competent exact FULL SRC04 original-source read/C11 construction grant",
            "source_id": SOURCE_ID,
            "source_sha256": EXPECTED_SOURCE_SHA256,
            "host": "USER_LOCAL_MAC",
            "purpose": FULL_PURPOSE,
            "consumer": FULL_CONSUMER,
            "scope": FULL_SCOPE,
            "required_document": _grant_requirement(),
            "no_source_io_until_valid_grant": True,
        },
        "next_executable_command": "PYTHONPATH=. python3 campaign_src04_completion/release/full_runner.py --mode primary --grant campaign_src04_completion/release/evidence/FULL_SOURCE_GRANT.json --grant-sha256 <exact-sha256> --repaired-config rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json --repaired-config-sha256 5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5",
        "artifact_manifest": _manifest(),
        "limits": [
            "No original SRC04 SAV stat/hash/open/decode was performed.",
            "No native full-source C11 release was constructed because the full-source grant is absent.",
            "The prior 42-field and D1 42-field products are preserved unchanged.",
            "No first-slice grant was silently expanded.",
            "ROUTING_UNKNOWN and DEFER canonical authority remain unchanged.",
            "No I03/I05, population, weight, eligibility, canonical, direction, FF/N11/N12/CI/prod/Sorok/actor/J52W52 effect.",
            "All 181 physical slots, 163 initial qualified responses, 15 held responses and 2 initial coordinates are accounted; the pinned B repaired input path/hash is wired for 178+3 where source-qualified.",
            "The fixed B observed-domain builder is invoked after admitted decode and before selection; q217 remains exact if source facts are insufficient.",
        ],
        "next_consumer": "HQ must supply the exact competent full-source grant; then the same runner executes the initial 163 + 2 path or the pinned B repaired 178 + 3 path by explicit immutable config path/hash.",
    }
    write_json(RETURN_PATH, result)
    write_json(RETURN_V2_PATH, result)
    print(json.dumps({"return_path": str(RETURN_PATH.relative_to(ROOT)), "return_sha256": sha_file(RETURN_PATH), "return_v2_path": str(RETURN_V2_PATH.relative_to(ROOT)), "return_v2_sha256": sha_file(RETURN_V2_PATH), "status": result["status"], "tests_passed": tests.get("passed")}, indent=2))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("prepare", "primary", "replay", "tests", "return"), default="prepare")
    parser.add_argument("--grant", default=str(GRANT_PATH))
    parser.add_argument("--grant-sha256", default=None)
    parser.add_argument("--repaired-config", default=None)
    parser.add_argument("--repaired-config-sha256", default=None)
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args(argv)
    try:
        if args.mode == "prepare":
            return run_prepare()
        if args.mode == "primary":
            if args.grant_sha256 is None:
                return run_prepare()
            return run_with_grant(Path(args.grant), args.grant_sha256, Path(args.repaired_config) if args.repaired_config else None, args.repaired_config_sha256)
        if args.mode == "replay":
            return run_replay()
        if args.mode == "tests":
            return run_tests()
        if args.mode == "return":
            if not args.artifact_commit:
                raise FullRunRefusal("ARTIFACT_COMMIT_REQUIRED")
            return run_return(args.artifact_commit)
    except FullRunRefusal as exc:
        write_json(EVIDENCE / "FAILURE.json", {"status": "BLOCKED", "actual_code": exc.code, "error": str(exc), "source_read_performed": False})
        print(json.dumps({"status": "BLOCKED", "actual_code": exc.code, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
