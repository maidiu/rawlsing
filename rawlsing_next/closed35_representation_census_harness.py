"""Deterministic CLOSED35 qualified representation census harness.

Source semantics are out of scope.  This module measures only exact physical
decoder representation, R5 typed material, physical missing/declaration state,
physical binding keys, and authority-bounded join status.

The module is import-safe in source-free environments. pyreadstat and pyarrow
are imported only after the exact Darwin runtime gate passes.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ALLOWLIST,
    PhysicalMissingState,
    _jsonable as decoder_jsonable,
    _missing_declarations as decoder_missing_declarations,
    _sav_header_layout,
    classify_physical_value,
)
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_bytes as r5_canonical_bytes
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


CONTRACT = "PREMAIN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS_HARNESS@1.0.0"
PATH_MANIFEST_SCHEMA = "CLOSED35_SOURCE_PATH_MANIFEST@1.0.0"
SOURCE_RECEIPT_SCHEMA = "CLOSED35_SOURCE_REPRESENTATION_RECEIPT@1.0.0"
OBSERVATIONS_SCHEMA = "CLOSED35_REPRESENTATION_OBSERVATIONS@1.0.0"
EDGE_RECEIPT_SCHEMA = "CLOSED35_EDGE_PRESERVATION_RECEIPT@1.0.0"
DEPENDENCY_RECEIPT_SCHEMA = "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE@1.0.0"
RUNTIME_RECEIPT_SCHEMA = "CLOSED35_RUNTIME_RECEIPT@1.0.0"
SUMMARY_SCHEMA = "CLOSED35_CENSUS_SUMMARY@1.0.0"

EXPECTED_BRANCH = "agent/rabochii-premain-closed35-qualified-representation-census-harness-r1"
EXPECTED_RUNTIME = {
    "platform": "Darwin",
    "machine": "x86_64",
    "cpython": "3.11.3",
    "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1",
}
CLASSIFICATIONS = (
    "EXACT_EXISTING_REGIME_APPLIES",
    "EXACT_BOUNDED_SUCCESSOR_BRIDGE_APPLIES",
    "NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED",
    "SOURCE_BOUNDED_REPRESENTATION_BRIDGE_REQUIRED",
    "TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY",
    "SOURCE_BYTES_UNAVAILABLE",
)
GLOBAL_INTEGRITY_FAILURES = (
    "RUNTIME_GATE_FAILED",
    "REGISTRY_INVALID",
    "SURFACE_REGISTRY_INVALID",
    "REPOSITORY_GUARD_FAILED",
    "HISTORICAL_DEPENDENCY_AUDIT_FAILED",
)
GENERIC_DEBTS = (
    "GENERIC_RAW_HEADER_METADATA_CARRIER_GAP",
    "GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP",
)
ALLOWED_DEPENDENCY_ORIGINS = frozenset({
    "HISTORICAL_PINNED",
    "CURRENT_SUCCESSOR_PINNED",
    "PINNED_EXTERNAL_EVIDENCE_IN_AUTHORITY",
})
FORBIDDEN_IMPORT_FRAGMENTS = (
    "ee_p2x_candidate_",
    "measured_six_cell",
    "candidate_a",
    "candidate_b",
    "candidate_c",
)
R5 = R5TypedValueCodec()


class CensusError(RuntimeError):
    pass


class GlobalIntegrityError(CensusError):
    pass


@dataclass(frozen=True)
class RuntimeFacts:
    platform: str
    machine: str
    cpython: str
    pyreadstat: str
    pyarrow: str

    def as_dict(self) -> dict[str, str]:
        return {
            "platform": self.platform,
            "machine": self.machine,
            "cpython": self.cpython,
            "pyreadstat": self.pyreadstat,
            "pyarrow": self.pyarrow,
        }


def _canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(repo_root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode:
        raise GlobalIntegrityError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_runtime_facts(facts: Mapping[str, str]) -> None:
    if dict(facts) != EXPECTED_RUNTIME:
        raise GlobalIntegrityError(
            "RUNTIME_GATE_FAILED: expected " + json.dumps(EXPECTED_RUNTIME, sort_keys=True)
            + " got " + json.dumps(dict(facts), sort_keys=True)
        )


def require_qualified_runtime() -> RuntimeFacts:
    facts = RuntimeFacts(
        platform=platform.system(),
        machine=platform.machine(),
        cpython=platform.python_version(),
        pyreadstat=importlib.metadata.version("pyreadstat"),
        pyarrow=importlib.metadata.version("pyarrow"),
    )
    validate_runtime_facts(facts.as_dict())
    return facts


def require_repository_guard(repo_root: Path, qualified_code_head: str) -> Mapping[str, Any]:
    if len(qualified_code_head) != 40 or any(c not in "0123456789abcdef" for c in qualified_code_head):
        raise GlobalIntegrityError("REPOSITORY_GUARD_FAILED: invalid qualified code head")
    branch = _git(repo_root, "branch", "--show-current")
    head = _git(repo_root, "rev-parse", "HEAD")
    if branch != EXPECTED_BRANCH:
        raise GlobalIntegrityError(f"REPOSITORY_GUARD_FAILED: branch {branch!r} != {EXPECTED_BRANCH!r}")
    ancestry = subprocess.run(
        ["git", "-C", str(repo_root), "merge-base", "--is-ancestor", qualified_code_head, head],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if ancestry.returncode:
        raise GlobalIntegrityError("REPOSITORY_GUARD_FAILED: qualified code head is not an ancestor")
    changed = [x for x in _git(repo_root, "diff", "--name-only", f"{qualified_code_head}..{head}").splitlines() if x]
    return {"branch": branch, "head": head, "qualified_code_head": qualified_code_head, "post_qualification_paths": changed}


def validate_post_qualification_paths(paths: Sequence[str]) -> None:
    prefix = "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1/"
    allowed = {
        prefix + "00_RETURN.md",
        prefix + "02_RUN_CLOSED35_QUALIFIED_REPRESENTATION_CENSUS.sh",
        prefix + "05_SOURCE_FREE_HOSTILE_QUALIFICATION.md",
        prefix + "06_EXPECTED_FANIN_CONTRACT.json",
        prefix + "07_RUNTIME_AND_NONEXECUTION_GUARDS.md",
        prefix + "RETURN.json",
    }
    unexpected = sorted(set(paths) - allowed)
    if unexpected:
        raise GlobalIntegrityError("REPOSITORY_GUARD_FAILED: post-qualification code/data drift: " + ", ".join(unexpected))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_source_registry(path: Path) -> Mapping[str, Any]:
    value = load_json(path)
    if value.get("schema") != "PREMAIN_CLOSED35_CENSUS_INPUT_REGISTRY@1.0.0":
        raise GlobalIntegrityError("REGISTRY_INVALID: schema")
    sources = value.get("sources")
    if not isinstance(sources, list) or len(sources) != 35:
        raise GlobalIntegrityError("REGISTRY_INVALID: exact 35-source registry required")
    ids = [s.get("source_id") for s in sources]
    if ids != [f"{i:02d}" for i in range(1, 36)]:
        raise GlobalIntegrityError("REGISTRY_INVALID: ordered source IDs 01..35 required")
    if len({s.get("canonical_sha256") for s in sources}) != 35:
        raise GlobalIntegrityError("REGISTRY_INVALID: canonical SHA identities must be unique")
    for source in sources:
        sha = source.get("canonical_sha256")
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise GlobalIntegrityError("REGISTRY_INVALID: malformed SHA")
        if source.get("source_format") not in {"SAV", "DTA"}:
            raise GlobalIntegrityError("REGISTRY_INVALID: unsupported format")
        resolve_decoder_lane(source)
    return value


def load_surface_registry(path: Path) -> tuple[Mapping[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(dict(row) for row in csv.DictReader(handle))
    if len(rows) != 34:
        raise GlobalIntegrityError(f"SURFACE_REGISTRY_INVALID: expected 34 surfaces, got {len(rows)}")
    ids = [x["surface_id"] for x in rows]
    if ids != [f"S{i:03d}" for i in range(1, 35)]:
        raise GlobalIntegrityError("SURFACE_REGISTRY_INVALID: ordered S001..S034 required")
    for row in rows:
        if row["owner_key_status"] not in {"EXACT_BOUNDED_OWNER", "NATIVE_LITERAL_RULE_OWNER", "MISSING_EXACT_VALUE_KEY_AUTHORITY"}:
            raise GlobalIntegrityError("SURFACE_REGISTRY_INVALID: owner-key state")
        if row["rule_native_domain_json"]:
            domain = json.loads(row["rule_native_domain_json"])
            if not isinstance(domain, list) or not domain:
                raise GlobalIntegrityError("SURFACE_REGISTRY_INVALID: rule domain")
    return rows


def validate_path_manifest(value: Mapping[str, Any]) -> Mapping[str, str]:
    if value.get("schema") != PATH_MANIFEST_SCHEMA:
        raise GlobalIntegrityError("path manifest schema mismatch")
    raw = value.get("sources")
    if isinstance(raw, list):
        items = {}
        for item in raw:
            if not isinstance(item, Mapping) or set(item) < {"source_id", "path"}:
                raise GlobalIntegrityError("path manifest list item malformed")
            sid = str(item["source_id"])
            if sid in items:
                raise GlobalIntegrityError("duplicate source_id in path manifest")
            items[sid] = str(item["path"])
    elif isinstance(raw, Mapping):
        items = {str(k): str(v) for k, v in raw.items()}
    else:
        raise GlobalIntegrityError("path manifest sources must be mapping or list")
    bad = sorted(set(items) - {f"{i:02d}" for i in range(1, 36)})
    if bad:
        raise GlobalIntegrityError("path manifest contains unknown source IDs: " + ",".join(bad))
    return items


def resolve_decoder_lane(source: Mapping[str, Any]) -> Mapping[str, Any]:
    lane = source.get("decoder_lane")
    if not isinstance(lane, Mapping):
        raise GlobalIntegrityError("REGISTRY_INVALID: decoder lane missing")
    reader = lane.get("reader")
    encoding = lane.get("encoding")
    admission = lane.get("generic_decoder_admission")
    if reader not in {"pyreadstat.read_sav", "pyreadstat.read_dta"}:
        raise GlobalIntegrityError("REGISTRY_INVALID: decoder reader unresolved")
    if source.get("source_format") == "SAV" and reader != "pyreadstat.read_sav":
        raise GlobalIntegrityError("REGISTRY_INVALID: SAV reader mismatch")
    if source.get("source_format") == "DTA" and reader != "pyreadstat.read_dta":
        raise GlobalIntegrityError("REGISTRY_INVALID: DTA reader mismatch")
    if admission == "SUPPORTED_EXACT_SHA_COMPATIBILITY_ONLY":
        if COMPATIBILITY_ALLOWLIST.get(source["canonical_sha256"]) != encoding:
            raise GlobalIntegrityError("REGISTRY_INVALID: exact-SHA compatibility lane absent from current decoder")
    if admission == "GAP" and lane.get("generic_debt") != "GENERIC_SAV_DECLARED_ENCODING_ADMISSION_GAP":
        raise GlobalIntegrityError("REGISTRY_INVALID: declared encoding gap must be explicit")
    return lane


def classification(value: str) -> str:
    if value not in CLASSIFICATIONS:
        raise CensusError("unknown classification: " + str(value))
    return value


def classify_surface(*, owner_key_status: str, representation_authority: str, exact_join: bool,
                     observed_physical_types: Sequence[str], rule_native_python_type: str,
                     bounded_bridge_pass: bool = False, representation_owner_pass: bool = False) -> str:
    if owner_key_status == "MISSING_EXACT_VALUE_KEY_AUTHORITY":
        return classification("TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY")
    if representation_authority and "LITS-I-Q301" in representation_authority:
        return classification(
            "EXACT_BOUNDED_SUCCESSOR_BRIDGE_APPLIES"
            if bounded_bridge_pass else "SOURCE_BOUNDED_REPRESENTATION_BRIDGE_REQUIRED"
        )
    if representation_authority and "WVS7-Q291" in representation_authority:
        return classification(
            "EXACT_EXISTING_REGIME_APPLIES"
            if representation_owner_pass else "TYPED_JOIN_BLOCKED_BY_MISSING_AUTHORITY"
        )
    if exact_join:
        return classification("EXACT_EXISTING_REGIME_APPLIES")
    if rule_native_python_type == "int" and observed_physical_types and set(observed_physical_types) <= {"float"}:
        return classification("NEW_GENERIC_REPRESENTATION_REGIME_REQUIRED")
    return classification("SOURCE_BOUNDED_REPRESENTATION_BRIDGE_REQUIRED")


def _reader_for(source: Mapping[str, Any]):
    import pyreadstat
    return pyreadstat.read_sav if source["source_format"] == "SAV" else pyreadstat.read_dta


def _reader_kwargs(source: Mapping[str, Any]) -> dict[str, Any]:
    lane = resolve_decoder_lane(source)
    return {
        "apply_value_formats": False,
        "user_missing": True,
        "encoding": lane.get("encoding"),
    }


def _metadata_only(source: Mapping[str, Any], source_path: Path):
    reader = _reader_for(source)
    frame, metadata = reader(str(source_path), metadataonly=True, **_reader_kwargs(source))
    return frame, metadata


def _bounded_surface_read(source: Mapping[str, Any], source_path: Path, variables: Sequence[str]):
    if not variables:
        return None, None
    reader = _reader_for(source)
    frame, metadata = reader(str(source_path), usecols=list(variables), **_reader_kwargs(source))
    return frame, metadata


def _source_declarations(metadata: Any, variable: str, source_format: str) -> tuple[Mapping[str, Any], ...]:
    return decoder_missing_declarations(metadata, variable, source_format)


def _token_record(value: Any) -> Mapping[str, Any]:
    token = R5.encode(value)
    return {
        "python_type": type(value).__name__,
        "r5_token": token,
        "r5_token_sha256": _sha256_bytes(r5_canonical_bytes(token)),
    }


def _domain_key(raw: Any, state: PhysicalMissingState, declaration: Mapping[str, Any] | None) -> str:
    material = {
        "raw": R5.encode(raw),
        "state": state.value,
        "declaration": R5.encode(declaration),
    }
    return _sha256_bytes(r5_canonical_bytes(material))


def _observe_variable_domain(frame: Any, metadata: Any, variable: str, source_format: str) -> Mapping[str, Any]:
    declarations = _source_declarations(metadata, variable, source_format)
    domain: dict[str, dict[str, Any]] = {}
    pre_types: set[str] = set()
    for value in frame[variable].tolist():
        pre_types.add(type(value).__name__)
        raw = decoder_jsonable(value)
        state, declaration = classify_physical_value(raw, declarations)
        key = _domain_key(raw, state, declaration)
        if key not in domain:
            domain[key] = {
                "raw_value_r5": R5.encode(raw),
                "r5_input_python_type": type(raw).__name__,
                "physical_missing_state": state.value,
                "source_missing_declaration_r5": R5.encode(declaration),
                "physical_binding_key": physical_value_binding_key(raw, state, declaration),
                "count": 0,
            }
        domain[key]["count"] += 1
    label_map = (getattr(metadata, "variable_value_labels", {}) or {}).get(variable, {}) or {}
    dictionary_tokens = []
    for key in label_map:
        raw_key = decoder_jsonable(key)
        dictionary_tokens.append({
            "python_type": type(raw_key).__name__,
            "r5_token": R5.encode(raw_key),
        })
    dictionary_tokens.sort(key=lambda x: r5_canonical_bytes(x["r5_token"]))
    return {
        "variable": variable,
        "decoder_native_python_types_before_normalization": sorted(pre_types),
        "physical_domain": sorted(domain.values(), key=lambda x: x["physical_binding_key"]),
        "source_missing_declarations": list(declarations),
        "dictionary_key_tokens": dictionary_tokens,
        "complete_domain_scan": True,
        "scan_scope": "ONE_GOVERNED_VARIABLE_ACROSS_SOURCE_ROWS",
    }


def _rule_native_domain(surface: Mapping[str, str]) -> list[Any]:
    return json.loads(surface["rule_native_domain_json"]) if surface["rule_native_domain_json"] else []


def _exact_rule_join_diagnostic(surface: Mapping[str, str], observation: Mapping[str, Any]) -> Mapping[str, Any]:
    domain = _rule_native_domain(surface)
    if not domain:
        return {"exact_join": False, "reason": "EXACT_VALUE_KEY_AUTHORITY_NOT_ENUMERATED", "rule_results": []}
    results = []
    all_exact = True
    physical = observation["physical_domain"]
    for literal in domain:
        literal_token = R5.encode(literal)
        exact = [x for x in physical if x["raw_value_r5"] == literal_token]
        float_representation = []
        if type(literal) is int:
            float_token = R5.encode(float(literal))
            float_representation = [x for x in physical if x["raw_value_r5"] == float_token]
        if not exact:
            all_exact = False
        results.append({
            "native_rule_literal_r5": literal_token,
            "exact_typed_matches": [x["physical_binding_key"] for x in exact],
            "non_authoritative_float_representation_diagnostic_matches": [
                x["physical_binding_key"] for x in float_representation
            ],
        })
    return {"exact_join": all_exact, "rule_results": results}


def _lits_bridge_check(surface: Mapping[str, str], source_sha: str, observation: Mapping[str, Any]) -> bool:
    from rawlsing_next.fiabc_lits_i_representation_authority import authorized_banked_raw_value
    ordinal = int(surface["ordinal"])
    for item in observation["physical_domain"]:
        raw = R5.decode(item["raw_value_r5"])
        state = PhysicalMissingState(item["physical_missing_state"])
        declaration = R5.decode(item["source_missing_declaration_r5"])
        try:
            authorized_banked_raw_value(
                source_sha256=source_sha,
                variable_name=surface["variable_name"],
                ordinal=ordinal,
                raw_value=raw,
                missing_state=state,
                source_missing_declaration=declaration,
            )
        except ValueError:
            return False
    return True


def _wvs_representation_check(surface: Mapping[str, str], observation: Mapping[str, Any]) -> bool:
    from rawlsing_next.fiabc_lm2_r1j_wvs7_representation_authority import AUTHORIZED_R5_TOKENS
    allowed = {r5_canonical_bytes(token) for token in AUTHORIZED_R5_TOKENS.values()}
    for item in observation["physical_domain"]:
        if item["physical_missing_state"] != PhysicalMissingState.OBSERVED_STORAGE_VALUE.value:
            return False
        if r5_canonical_bytes(item["raw_value_r5"]) not in allowed:
            return False
        if R5.decode(item["source_missing_declaration_r5"]) is not None:
            return False
    return True


def _surface_observation(surface: Mapping[str, str], variable_observation: Mapping[str, Any], source_sha: str) -> Mapping[str, Any]:
    join = _exact_rule_join_diagnostic(surface, variable_observation)
    observed_types = sorted({x["r5_input_python_type"] for x in variable_observation["physical_domain"]})
    bridge_pass = False
    representation_pass = False
    if "LITS-I-Q301" in surface["representation_authority"]:
        bridge_pass = _lits_bridge_check(surface, source_sha, variable_observation)
    if "WVS7-Q291" in surface["representation_authority"]:
        representation_pass = _wvs_representation_check(surface, variable_observation)
    result = classify_surface(
        owner_key_status=surface["owner_key_status"],
        representation_authority=surface["representation_authority"],
        exact_join=bool(join["exact_join"]),
        observed_physical_types=observed_types,
        rule_native_python_type=surface["rule_native_python_type"],
        bounded_bridge_pass=bridge_pass,
        representation_owner_pass=representation_pass,
    )
    return {
        "surface_id": surface["surface_id"],
        "variable_name": surface["variable_name"],
        "ordinal_registry": int(surface["ordinal"]) if surface["ordinal"] else None,
        "surface_kind": surface["surface_kind"],
        "authority_locator": surface["authority_locator"],
        "owner_key_status": surface["owner_key_status"],
        "representation_authority": surface["representation_authority"] or None,
        "rule_native_domain_r5": [R5.encode(x) for x in _rule_native_domain(surface)],
        "variable_physical_observation": variable_observation,
        "join_diagnostic": join,
        "classification": result,
        "semantic_inference_performed": False,
        "numeric_coercion_used_for_join": False,
    }


def _metadata_receipt(source: Mapping[str, Any], source_path: Path, metadata: Any) -> Mapping[str, Any]:
    names = list(getattr(metadata, "column_names", ()) or ())
    raw_header = None
    if source["source_format"] == "SAV":
        with source_path.open("rb") as handle:
            raw_header = _sav_header_layout(handle.read(176))
    return {
        "number_rows": int(getattr(metadata, "number_rows", 0) or 0),
        "logical_variable_count": len(names),
        "ordered_variable_inventory_sha256": _sha256_bytes(
            _canonical_json_bytes([{"ordinal": i + 1, "name": name} for i, name in enumerate(names)])
        ),
        "file_encoding": decoder_jsonable(getattr(metadata, "file_encoding", None)),
        "file_format": decoder_jsonable(getattr(metadata, "file_format", None)),
        "raw_sav_fixed_header": raw_header,
        "mr_sets": decoder_jsonable(getattr(metadata, "mr_sets", {}) or {}),
    }


def _shape_check(source: Mapping[str, Any], metadata_receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    expected = source.get("expected_shape") or {}
    mismatches = []
    if isinstance(expected.get("rows"), int) and expected["rows"] != metadata_receipt["number_rows"]:
        mismatches.append({"field": "rows", "expected": expected["rows"], "observed": metadata_receipt["number_rows"]})
    expected_vars = expected.get("variables", expected.get("logical_variables"))
    if isinstance(expected_vars, int) and expected_vars != metadata_receipt["logical_variable_count"]:
        mismatches.append({"field": "variables", "expected": expected_vars, "observed": metadata_receipt["logical_variable_count"]})
    return {"expected": expected, "mismatches": mismatches, "pass": not mismatches}


def _edge_receipt_for_source(source: Mapping[str, Any], metadata_receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    result = {
        "edge_classes": source["edge_classes"],
        "accepted_physical_hazards": source["accepted_physical_hazards"],
        "documentary_unknowns_preserved": source["documentary_unknowns"],
        "semantic_interpretation_authorized": False,
        "generic_debts": [],
        "special_witnesses": {},
    }
    if source["source_id"] == "26":
        raw = (metadata_receipt.get("raw_sav_fixed_header") or {}).get("nominal_case_size")
        width = metadata_receipt["logical_variable_count"]
        result["special_witnesses"]["latinobarometro_2024_raw_header_vs_stream"] = {
            "raw_nominal_case_size": raw,
            "normalized_dictionary_stream_width": width,
            "expected": [174, 332],
            "pass": raw == 174 and width == 332,
        }
        if raw != 174 or width != 332:
            result["generic_debts"].append("GENERIC_RAW_HEADER_METADATA_CARRIER_GAP")
    lane = resolve_decoder_lane(source)
    if lane.get("generic_decoder_admission") == "GAP":
        result["generic_debts"].append(lane["generic_debt"])
        result["special_witnesses"]["declared_encoding_candidate_lane"] = {
            "encoding": lane.get("encoding"),
            "current_generic_decoder_admission": "GAP",
        }
    return result


def _source_status(surface_observations: Sequence[Mapping[str, Any]], edge: Mapping[str, Any], shape: Mapping[str, Any]) -> str:
    acceptable = {"EXACT_EXISTING_REGIME_APPLIES", "EXACT_BOUNDED_SUCCESSOR_BRIDGE_APPLIES"}
    if not shape["pass"] or edge["generic_debts"]:
        return "BLOCKED"
    if any(x["classification"] not in acceptable for x in surface_observations):
        return "BLOCKED"
    return "PASS"


def immutable_json(path: Path, payload: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _canonical_json_bytes(payload)
    if path.exists():
        if path.read_bytes() != data:
            raise GlobalIntegrityError(f"immutable receipt drift: {path}")
        return "RESUMED_IDENTICAL"
    fd, tmp_name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            if path.read_bytes() != data:
                raise GlobalIntegrityError(f"immutable receipt race/drift: {path}")
            return "RESUMED_IDENTICAL"
        return "CREATED"
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass


def validate_source_receipt(receipt: Mapping[str, Any]) -> None:
    if receipt.get("schema") != SOURCE_RECEIPT_SCHEMA:
        raise CensusError("source receipt schema mismatch")
    if receipt.get("status") not in {"PASS", "BLOCKED"}:
        raise CensusError("source receipt status")
    for surface in receipt.get("surfaces", ()):
        classification(surface["classification"])


def _blocked_source_receipt(source: Mapping[str, Any], *, reason: str, runtime: Mapping[str, Any],
                            manifest_hash: str) -> Mapping[str, Any]:
    receipt = {
        "schema": SOURCE_RECEIPT_SCHEMA,
        "contract": CONTRACT,
        "source_id": source["source_id"],
        "source_file": source["canonical_filename"],
        "canonical_sha256": source["canonical_sha256"],
        "status": "BLOCKED",
        "blocker": reason,
        "source_classification": "SOURCE_BYTES_UNAVAILABLE",
        "runtime": runtime,
        "path_manifest_sha256": manifest_hash,
        "surfaces": [],
        "edge_preservation": {
            "edge_classes": source["edge_classes"],
            "documentary_unknowns_preserved": source["documentary_unknowns"],
            "semantic_interpretation_authorized": False,
        },
    }
    validate_source_receipt(receipt)
    return receipt


def observe_source(*, source: Mapping[str, Any], source_path_text: str | None,
                   surfaces: Sequence[Mapping[str, str]], runtime: Mapping[str, Any],
                   manifest_hash: str) -> Mapping[str, Any]:
    if not source_path_text:
        return _blocked_source_receipt(source, reason="SOURCE_PATH_NOT_IN_MANIFEST", runtime=runtime, manifest_hash=manifest_hash)
    source_path = Path(source_path_text).expanduser()
    if not source_path.is_file():
        return _blocked_source_receipt(source, reason="SOURCE_PATH_NOT_A_FILE", runtime=runtime, manifest_hash=manifest_hash)
    actual_sha = _sha256_file(source_path)
    if actual_sha != source["canonical_sha256"]:
        return _blocked_source_receipt(source, reason="CANONICAL_SHA256_MISMATCH", runtime=runtime, manifest_hash=manifest_hash)
    _, metadata = _metadata_only(source, source_path)
    meta = _metadata_receipt(source, source_path, metadata)
    shape = _shape_check(source, meta)
    names = list(getattr(metadata, "column_names", ()) or ())
    by_name = {name: i + 1 for i, name in enumerate(names)}
    missing = [s["variable_name"] for s in surfaces if s["variable_name"] not in by_name]
    if missing:
        receipt = {
            "schema": SOURCE_RECEIPT_SCHEMA,
            "contract": CONTRACT,
            "source_id": source["source_id"],
            "source_file": source["canonical_filename"],
            "canonical_sha256": source["canonical_sha256"],
            "actual_sha256": actual_sha,
            "status": "BLOCKED",
            "blocker": "GOVERNED_SURFACE_VARIABLE_MISSING:" + ",".join(sorted(missing)),
            "runtime": runtime,
            "path_manifest_sha256": manifest_hash,
            "metadata": meta,
            "shape_check": shape,
            "surfaces": [],
            "edge_preservation": _edge_receipt_for_source(source, meta),
        }
        validate_source_receipt(receipt)
        return receipt
    for surface in surfaces:
        if surface["ordinal"] and int(surface["ordinal"]) != by_name[surface["variable_name"]]:
            raise GlobalIntegrityError(
                f"SURFACE_REGISTRY_INVALID: ordinal drift {surface['surface_id']} expected {surface['ordinal']} got {by_name[surface['variable_name']]}"
            )
    variable_names = [s["variable_name"] for s in surfaces]
    surface_observations = []
    if variable_names:
        frame, data_metadata = _bounded_surface_read(source, source_path, variable_names)
        observations = {
            name: _observe_variable_domain(frame, data_metadata, name, source["source_format"])
            for name in variable_names
        }
        surface_observations = [
            _surface_observation(surface, observations[surface["variable_name"]], actual_sha)
            for surface in surfaces
        ]
    edge = _edge_receipt_for_source(source, meta)
    status = _source_status(surface_observations, edge, shape)
    receipt = {
        "schema": SOURCE_RECEIPT_SCHEMA,
        "contract": CONTRACT,
        "source_id": source["source_id"],
        "source_file": source["canonical_filename"],
        "canonical_sha256": source["canonical_sha256"],
        "actual_sha256": actual_sha,
        "size_bytes": source_path.stat().st_size,
        "status": status,
        "runtime": runtime,
        "path_manifest_sha256": manifest_hash,
        "decoder_lane": source["decoder_lane"],
        "metadata": meta,
        "shape_check": shape,
        "surfaces": surface_observations,
        "edge_preservation": edge,
        "semantic_inference_performed": False,
        "candidate_execution_performed": False,
        "measured_p2x_performed": False,
    }
    validate_source_receipt(receipt)
    return receipt


def dependency_provenance_records() -> tuple[Mapping[str, Any], ...]:
    return (
        {
            "dependency": "current_r5_codec",
            "origin": "CURRENT_SUCCESSOR_PINNED",
            "path": "rawlsing_next/pre553_r5_codec.py",
            "blob": "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
            "key_role": "R5_TYPED_TOKEN_PRODUCER",
        },
        {
            "dependency": "current_physical_binding_key",
            "origin": "CURRENT_SUCCESSOR_PINNED",
            "path": "rawlsing_next/pre553_source_backed_c11_facade.py",
            "blob": "8a761119e4a8d68eb291fc4edfadb52e027f8284",
            "key_role": "CURRENT_PHYSICAL_KEY_OWNER",
        },
        {
            "dependency": "current_physical_decoder",
            "origin": "CURRENT_SUCCESSOR_PINNED",
            "path": "rawlsing_next/pre553_physical_decoder.py",
            "blob": "86109c4a0b7ebd9b66e3b531b6334bfb48f03f78",
            "key_role": "DECODER_NORMALIZATION_AND_MISSING_STATE",
        },
        {
            "dependency": "lits_legacy_facade",
            "origin": "HISTORICAL_PINNED",
            "commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
            "path": "rawlsing_next/pre553_source_backed_c11_facade.py",
            "blob": "7c509c2098d0030f253344eb3f682471378812a8",
            "key_role": "LITS_ACCEPTED_HISTORICAL_PHYSICAL_KEY_OWNER",
        },
        {
            "dependency": "lits_legacy_canonicalize_semantic_hash",
            "origin": "HISTORICAL_PINNED",
            "commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
            "path": "rawlsing_next/pre553_empirical_objects.py",
            "blob": "a61365b994e5c3c50de0f598fcf40e90abf757b6",
            "key_role": "LITS_HISTORICAL_KEY_CANONICALIZATION_DEPENDENCY",
        },
        {
            "dependency": "lits_legacy_missing_state_enum",
            "origin": "HISTORICAL_PINNED",
            "commit": "0b96b8de9aac774566f872cf0630ebd4ddeb70e6",
            "path": "rawlsing_next/pre553_physical_decoder.py",
            "blob": "13aa733b511dc23e00bfcdf288c5b920e3f09983",
            "key_role": "LITS_HISTORICAL_KEY_STATE_DEPENDENCY",
        },
        {
            "dependency": "wvs7_pyreadstat_readstat_version_evidence",
            "origin": "PINNED_EXTERNAL_EVIDENCE_IN_AUTHORITY",
            "path": "rawlsing_next/fiabc_lm2_r1j_wvs7_representation_authority.py",
            "blob": "220c646df5b85eb927af70961c5d05be97edfb73",
            "key_role": "WVS7_NUMERIC_REPRESENTATION_PROVENANCE",
        },
    )


def audit_dependency_origins(records: Sequence[Mapping[str, Any]]) -> None:
    for record in records:
        if record.get("origin") not in ALLOWED_DEPENDENCY_ORIGINS:
            raise GlobalIntegrityError(
                "HISTORICAL_DEPENDENCY_AUDIT_FAILED: accidental current dependency leak: "
                + str(record.get("dependency"))
            )


def _verify_git_blob(repo_root: Path, record: Mapping[str, Any]) -> Mapping[str, Any]:
    path = record.get("path")
    expected = record.get("blob")
    if record["origin"] == "CURRENT_SUCCESSOR_PINNED":
        actual = _git(repo_root, "hash-object", str(repo_root / str(path)))
        return {**record, "verified_blob": actual, "pass": actual == expected}
    if record["origin"] == "HISTORICAL_PINNED":
        commit = str(record["commit"])
        data = subprocess.run(
            ["git", "-C", str(repo_root), "show", f"{commit}:{path}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if data.returncode:
            return {**record, "verified_blob": None, "pass": False, "failure": "PINNED_GIT_OBJECT_UNAVAILABLE"}
        actual = subprocess.run(
            ["git", "-C", str(repo_root), "hash-object", "--stdin"],
            input=data.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        ).stdout.decode().strip()
        return {**record, "verified_blob": actual, "pass": actual == expected}
    return {**record, "pass": True, "verification": "PINNED_BY_CURRENT_AUTHORITY_FILE"}


def build_dependency_receipt(repo_root: Path) -> Mapping[str, Any]:
    records = dependency_provenance_records()
    audit_dependency_origins(records)
    verified = [_verify_git_blob(repo_root, r) for r in records]
    failures = [x for x in verified if not x.get("pass")]
    if failures:
        raise GlobalIntegrityError("HISTORICAL_DEPENDENCY_AUDIT_FAILED: " + json.dumps(failures, sort_keys=True))
    return {
        "schema": DEPENDENCY_RECEIPT_SCHEMA,
        "records": verified,
        "ambient_current_dependency_leaks": [],
        "pass": True,
    }


def build_aggregate_outputs(receipts: Sequence[Mapping[str, Any]], runtime_receipt: Mapping[str, Any],
                            dependency_receipt: Mapping[str, Any], output_root: Path) -> None:
    observations = {
        "schema": OBSERVATIONS_SCHEMA,
        "source_receipt_count": len(receipts),
        "sources": list(receipts),
    }
    immutable_json(output_root / "CLOSED35_REPRESENTATION_OBSERVATIONS.json", observations)
    edge = {
        "schema": EDGE_RECEIPT_SCHEMA,
        "sources": [
            {"source_id": r["source_id"], "source_file": r["source_file"], "edge_preservation": r["edge_preservation"]}
            for r in receipts
        ],
        "semantic_interpretation_authorized": False,
    }
    immutable_json(output_root / "CLOSED35_EDGE_PRESERVATION_RECEIPT.json", edge)
    immutable_json(output_root / "CLOSED35_HISTORICAL_DEPENDENCY_PROVENANCE.json", dependency_receipt)
    immutable_json(output_root / "CLOSED35_RUNTIME_RECEIPT.json", runtime_receipt)

    matrix_path = output_root / "CLOSED35_TYPED_JOIN_MATRIX.csv"
    rows = []
    for receipt in receipts:
        for surface in receipt.get("surfaces", ()):
            rows.append({
                "source_id": receipt["source_id"],
                "source_file": receipt["source_file"],
                "surface_id": surface["surface_id"],
                "variable_name": surface["variable_name"],
                "classification": surface["classification"],
                "owner_key_status": surface["owner_key_status"],
                "exact_join": surface["join_diagnostic"]["exact_join"],
                "numeric_coercion_used_for_join": surface["numeric_coercion_used_for_join"],
            })
    headers = ["source_id", "source_file", "surface_id", "variable_name", "classification",
               "owner_key_status", "exact_join", "numeric_coercion_used_for_join"]
    text = []
    from io import StringIO
    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    data = buf.getvalue().encode("utf-8")
    if matrix_path.exists():
        if matrix_path.read_bytes() != data:
            raise GlobalIntegrityError("immutable aggregate matrix drift")
    else:
        matrix_path.write_bytes(data)

    counts = {name: 0 for name in CLASSIFICATIONS}
    pass_count = 0
    for receipt in receipts:
        if receipt["status"] == "PASS":
            pass_count += 1
        if "source_classification" in receipt:
            counts[receipt["source_classification"]] += 1
        for surface in receipt.get("surfaces", ()):
            counts[surface["classification"]] += 1
    summary = {
        "schema": SUMMARY_SCHEMA,
        "source_count": len(receipts),
        "source_pass_count": pass_count,
        "source_blocked_count": len(receipts) - pass_count,
        "classification_counts": counts,
        "candidate_abc_run": False,
        "measured_p2x_run": False,
        "p3_run": False,
        "architecture_selection_run": False,
        "terminal": "CLOSED35_REPRESENTATION_CENSUS_COMPLETE",
    }
    immutable_json(output_root / "CLOSED35_CENSUS_SUMMARY.json", summary)


def run_census(*, repo_root: Path, manifest_path: Path, output_root: Path, qualified_code_head: str,
               observer=observe_source) -> int:
    guard = require_repository_guard(repo_root, qualified_code_head)
    validate_post_qualification_paths(guard["post_qualification_paths"])
    runtime = require_qualified_runtime()
    runtime_receipt = {
        "schema": RUNTIME_RECEIPT_SCHEMA,
        "expected": EXPECTED_RUNTIME,
        "observed": runtime.as_dict(),
        "repository_guard": guard,
        "pass": True,
    }
    return_dir = repo_root / "WORKER_RETURNS/PREMAIN-CLOSED35-QUALIFIED-REPRESENTATION-CENSUS-HARNESS-R1"
    registry = load_source_registry(return_dir / "01_CLOSED35_CENSUS_INPUT_REGISTRY.json")
    surfaces = load_surface_registry(return_dir / "03_GOVERNED_TYPED_SURFACE_REGISTRY.csv")
    by_source: dict[str, list[Mapping[str, str]]] = {f"{i:02d}": [] for i in range(1, 36)}
    for surface in surfaces:
        if surface["source_id"] not in by_source:
            raise GlobalIntegrityError("SURFACE_REGISTRY_INVALID: source id")
        by_source[surface["source_id"]].append(surface)
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    paths = validate_path_manifest(manifest)
    manifest_hash = _sha256_bytes(_canonical_json_bytes(manifest))
    dependency_receipt = build_dependency_receipt(repo_root)

    output_root.mkdir(parents=True, exist_ok=True)
    receipt_root = output_root / "source_receipts"
    receipts = []
    for source in registry["sources"]:
        sid = source["source_id"]
        receipt_path = receipt_root / f"SOURCE_{sid}_REPRESENTATION_RECEIPT.json"
        try:
            receipt = observer(
                source=source,
                source_path_text=paths.get(sid),
                surfaces=tuple(by_source[sid]),
                runtime=runtime.as_dict(),
                manifest_hash=manifest_hash,
            )
        except GlobalIntegrityError:
            raise
        except Exception as exc:
            receipt = {
                "schema": SOURCE_RECEIPT_SCHEMA,
                "contract": CONTRACT,
                "source_id": sid,
                "source_file": source["canonical_filename"],
                "canonical_sha256": source["canonical_sha256"],
                "status": "BLOCKED",
                "blocker": "SOURCE_LOCAL_MEASUREMENT_FAILURE:" + type(exc).__name__ + ":" + str(exc),
                "runtime": runtime.as_dict(),
                "path_manifest_sha256": manifest_hash,
                "surfaces": [],
                "edge_preservation": {
                    "edge_classes": source["edge_classes"],
                    "documentary_unknowns_preserved": source["documentary_unknowns"],
                    "semantic_interpretation_authorized": False,
                },
            }
        validate_source_receipt(receipt)
        immutable_json(receipt_path, receipt)
        receipts.append(receipt)
        print(
            f"CLOSED35_REP_CENSUS {int(sid):02d}/35 {source['canonical_filename']} {receipt['status']}",
            flush=True,
        )
    build_aggregate_outputs(receipts, runtime_receipt, dependency_receipt, output_root)
    print("CLOSED35_REP_CENSUS COMPLETE", flush=True)
    return 0


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--qualified-code-head", required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    return run_census(
        repo_root=Path(args.repo_root).resolve(),
        manifest_path=Path(args.manifest).resolve(),
        output_root=Path(args.output_root).resolve(),
        qualified_code_head=args.qualified_code_head,
    )


if __name__ == "__main__":
    raise SystemExit(main())
