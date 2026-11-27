#!/usr/bin/env python3
"""Native S2 F03 authority experiment for ZAK01-HOSTILE.

This script imports the *actual historical* module blob
62084cbed10a5975f79bd504bf4fb99025e4e64e and calls
apply_question_relation_authority() on an immutable synthetic bridge_row.

It is an author-side S2 execution on synthetic data only.  It does not read
respondent data, does not run S3, and does not prove the original historical
production first reader.
"""

from __future__ import annotations

import argparse
import copy
import csv
import getpass
import hashlib
import importlib.util
import inspect
import json
import os
import platform
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

sys.dont_write_bytecode = True

EXPECTED_SOURCE = {
    "path": "data/ddm_build_copy/ddm_v550_question_relation_authority.py",
    "historical_commit": "9253064bc9423a0f0ccda4fbdea43c2f54f800c6",
    "git_blob_sha1": "62084cbed10a5975f79bd504bf4fb99025e4e64e",
    "sha256": "2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c",
    "bytes": 38858,
    "input_head_commit": "52206dc889e094c48c610e30f72824630c697560",
    "input_head_blob_sha1": "62084cbed10a5975f79bd504bf4fb99025e4e64e",
}
EXPECTED_REGISTRY = {
    "path": "data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv",
    "historical_commit": "9253064bc9423a0f0ccda4fbdea43c2f54f800c6",
    "sha256": "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b",
    "bytes": 1119028,
    "input_head_blob_sha1": "daac001bb8da645c7d99408e2239f4e04b6e9f9b",
}
EXPECTED_FIXTURE_CANONICAL_SHA256 = "bc1f8cda38c83615d0a8ae077976790cb0423dd37ef553095bf8657528363f38"
EXPECTED_FIXTURE_FILE_SHA256 = "eb8b734bf76d959d5de67c3a5a0593d5c1d3a94336533a6a1ef68ce35da982a7"
STRUCTURAL_COORDINATES = (
    "driver_id",
    "driver_facet_id",
    "question_block_id",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
)
QUC_PRESERVED = "QUC_AUTHORITY_PRESERVED_ACTIVE_REGISTRY_NO_MATCH"
CANONICAL_SERIALIZATION = (
    "json.dumps(value, sort_keys=True, ensure_ascii=False, "
    "separators=(',', ':'), allow_nan=False).encode('utf-8')"
)
PRETTY_SERIALIZATION = (
    "json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, "
    "allow_nan=False) + '\\n'"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            ensure_ascii=False,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


class AssertionLog:
    def __init__(self) -> None:
        self.items: list[dict[str, Any]] = []

    def check(
        self,
        case: str,
        assertion_id: str,
        description: str,
        expected: Any,
        actual: Any,
        predicate: Callable[[Any, Any], bool] | None = None,
    ) -> bool:
        passed = (
            bool(predicate(expected, actual))
            if predicate is not None
            else actual == expected
        )
        self.items.append(
            {
                "case": case,
                "assertion_id": assertion_id,
                "description": description,
                "expected": expected,
                "actual": actual,
                "pass": passed,
            }
        )
        return passed

    @property
    def failures(self) -> list[dict[str, Any]]:
        return [item for item in self.items if not item["pass"]]

    def summary(self) -> dict[str, int]:
        return {
            "total": len(self.items),
            "passed": sum(1 for item in self.items if item["pass"]),
            "failed": sum(1 for item in self.items if not item["pass"]),
        }


def load_historical_module(source_path: Path) -> Any:
    module_name = "ddm_v550_question_relation_authority"
    spec = importlib.util.spec_from_file_location(module_name, source_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot construct import spec for {source_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def registry_direct_key_scan(
    module: Any, registry_path: Path, family: str, wave: str, country: str
) -> dict[str, Any]:
    """Scan every selected-registry row using the historical module's own key code."""
    family_key = module.canonical_source_family(family).casefold()
    wave_key = module.canonical_wave(family, wave).casefold()
    country_key = module.canonical_country_code(country).casefold()
    matching_rows: list[dict[str, str]] = []
    with registry_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = module._resolution_key(
                row.get("source_family"),
                row.get("canonical_wave"),
                row.get("country_code_scope"),
                row.get("var_code") or row.get("question_id"),
            )
            if key[:3] == (family_key, wave_key, country_key):
                matching_rows.append(
                    {
                        "question_id": row.get("question_id", ""),
                        "var_code": row.get("var_code", ""),
                        "key": "|".join(key),
                    }
                )
    return {
        "family_key": family_key,
        "wave_key": wave_key,
        "country_key": country_key,
        "rows_matching_family_wave_country": len(matching_rows),
        "matching_rows": matching_rows[:10],
        "truncated": len(matching_rows) > 10,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="repository root containing the pinned historical source and registry",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="directory for WITNESS.json and case outputs",
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    source_path = repo_root / EXPECTED_SOURCE["path"]
    registry_path = repo_root / EXPECTED_REGISTRY["path"]
    fixture_path = out_dir / "fixture.json"
    assertions = AssertionLog()

    source_bytes = read_bytes(source_path)
    registry_bytes = read_bytes(registry_path)
    fixture_file_bytes = read_bytes(fixture_path)
    fixture = json.loads(fixture_file_bytes)
    fixture_canonical = canonical_json_bytes(fixture)

    assertions.check(
        "GLOBAL",
        "GLOBAL.SOURCE.BYTES",
        "historical F03 source byte count equals pinned blob size",
        EXPECTED_SOURCE["bytes"],
        len(source_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.SOURCE.SHA256",
        "historical F03 source SHA-256 equals pinned runner bytes",
        EXPECTED_SOURCE["sha256"],
        sha256_bytes(source_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.SOURCE.GIT_BLOB_SHA1",
        "historical F03 source Git blob SHA-1 equals commissioned blob",
        EXPECTED_SOURCE["git_blob_sha1"],
        git_blob_sha1(source_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.REGISTRY.BYTES",
        "selected active registry byte count equals pinned selected registry",
        EXPECTED_REGISTRY["bytes"],
        len(registry_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.REGISTRY.SHA256",
        "selected active registry SHA-256 equals commissioned selected registry",
        EXPECTED_REGISTRY["sha256"],
        sha256_bytes(registry_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.FIXTURE.FILE_SHA256",
        "immutable fixture file SHA-256 equals pinned synthetic fixture",
        EXPECTED_FIXTURE_FILE_SHA256,
        sha256_bytes(fixture_file_bytes),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.FIXTURE.CANONICAL_SHA256",
        "immutable fixture canonical JSON SHA-256 equals pinned synthetic fixture",
        EXPECTED_FIXTURE_CANONICAL_SHA256,
        sha256_bytes(fixture_canonical),
    )

    fixture_values = [fixture.get(field) for field in STRUCTURAL_COORDINATES]
    assertions.check(
        "GLOBAL",
        "GLOBAL.FIXTURE.SIX_NONEMPTY_COORDINATES",
        "all six synthetic structural coordinates are nonempty strings",
        True,
        all(isinstance(value, str) and value.strip() for value in fixture_values),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.FIXTURE.SIX_DISTINCT_COORDINATES",
        "all six synthetic structural coordinates are distinguishable",
        6,
        len(set(fixture_values)),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.FIXTURE.FIVE_INBOUND_CONDITIONS",
        "fixture carries the five commissioned inbound conditions",
        {
            "semantic_role_authority_status": "CERTIFIED",
            "semantic_role": "RELATION_EVIDENCE",
            "current_directional_atom_eligible": True,
            "allowed_as_v551_relation_evidence": True,
            "structural_mapping_status": "COMPLETE",
        },
        {
            "semantic_role_authority_status": fixture.get("semantic_role_authority_status"),
            "semantic_role": fixture.get("semantic_role"),
            "current_directional_atom_eligible": fixture.get("current_directional_atom_eligible"),
            "allowed_as_v551_relation_evidence": fixture.get("allowed_as_v551_relation_evidence"),
            "structural_mapping_status": fixture.get("structural_mapping_status"),
        },
    )

    module = load_historical_module(source_path)
    function = module.apply_question_relation_authority
    function_source_file = Path(inspect.getsourcefile(function) or "").resolve()
    function_lines, function_start_line = inspect.getsourcelines(function)
    assertions.check(
        "GLOBAL",
        "GLOBAL.FUNCTION.SOURCE_FILE",
        "test-time function object resolves to the pinned historical source file",
        str(source_path.resolve()),
        str(function_source_file),
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.FUNCTION.MODULE_ROOT",
        "historical module ROOT resolves to the execution repository root",
        str(repo_root),
        str(Path(module.ROOT).resolve()),
    )

    index = module.load_question_relation_authority(registry_path)
    assertions.check(
        "GLOBAL",
        "GLOBAL.REGISTRY.LOADED_SHA256",
        "historical loader independently reports the pinned selected registry SHA-256",
        EXPECTED_REGISTRY["sha256"],
        index.file_sha256,
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.REGISTRY.ROW_COUNT",
        "historical loader accepts the selected registry row count",
        700,
        len(index.rows),
    )

    no_match_scan = registry_direct_key_scan(
        module,
        registry_path,
        fixture["source_family"],
        fixture["canonical_wave"],
        fixture["country_code"],
    )
    assertion = module.resolve_question_relation_authority(
        source_family=fixture["source_family"],
        canonical_wave_value=fixture["canonical_wave"],
        country_code=fixture["country_code"],
        question_id=fixture["question_id"],
        var_code=fixture["var_code"],
        authority_path=registry_path,
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.NO_MATCH.DIRECT_SCAN",
        "no selected-registry row shares the synthetic family/wave/country scope",
        0,
        no_match_scan["rows_matching_family_wave_country"],
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.NO_MATCH.RESOLVER_STATUS",
        "historical resolver returns BLOCKED_MISSING_AUTHORITY for the synthetic identity",
        "BLOCKED_MISSING_AUTHORITY",
        assertion.status,
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.NO_MATCH.RESOLVER_COUNT",
        "historical resolver finds zero matching authority rows",
        0,
        assertion.match_count,
    )
    assertions.check(
        "GLOBAL",
        "GLOBAL.NO_MATCH.REGISTRY_MATCH_FALSE",
        "historical resolver does not resolve an authority row",
        False,
        assertion.resolved,
    )

    def recheck_fixture(case: str) -> None:
        current_bytes = read_bytes(fixture_path)
        current_fixture = json.loads(current_bytes)
        assertions.check(
            case,
            f"{case}.FIXTURE.FILE_UNCHANGED",
            "immutable fixture file bytes remain unchanged during execution",
            EXPECTED_FIXTURE_FILE_SHA256,
            sha256_bytes(current_bytes),
        )
        assertions.check(
            case,
            f"{case}.FIXTURE.CANONICAL_UNCHANGED",
            "immutable fixture canonical JSON remains unchanged during execution",
            EXPECTED_FIXTURE_CANONICAL_SHA256,
            sha256_bytes(canonical_json_bytes(current_fixture)),
        )

    def execute_case(
        case_id: str,
        mutate: dict[str, Any],
        output_filename: str,
    ) -> dict[str, Any]:
        recheck_fixture(case_id)
        case_input = copy.deepcopy(fixture)
        case_input.update(mutate)
        input_canonical = canonical_json_bytes(case_input)
        output = function(MappingProxyType(case_input), authority_path=registry_path)
        output_canonical = canonical_json_bytes(output)
        output_pretty = pretty_json_bytes(output)
        output_path = out_dir / output_filename
        output_path.write_bytes(output_pretty)

        assertions.check(
            case_id,
            f"{case_id}.INPUT.IMMUTABLE",
            "historical function did not mutate the immutable synthetic input",
            sha256_bytes(input_canonical),
            sha256_bytes(canonical_json_bytes(case_input)),
        )
        recheck_fixture(case_id)
        return {
            "case_id": case_id,
            "mutation": mutate,
            "input": case_input,
            "input_canonical_sha256": sha256_bytes(input_canonical),
            "input_file_sha256": sha256_bytes(pretty_json_bytes(case_input)),
            "output": output,
            "output_file": output_filename,
            "output_file_sha256": sha256_bytes(output_pretty),
            "output_canonical_sha256": sha256_bytes(output_canonical),
        }

    case_a = execute_case("A_POSITIVE", {}, "OUTPUT_A_POSITIVE.json")
    case_b = execute_case(
        "B_DENIED_PERMISSION",
        {"allowed_as_v551_relation_evidence": False},
        "OUTPUT_B_DENIED_PERMISSION.json",
    )
    case_c = execute_case(
        "C_PARTIAL_MAPPING",
        {"structural_mapping_status": "PARTIAL"},
        "OUTPUT_C_PARTIAL_MAPPING.json",
    )
    case_d = execute_case("D_RESTORED", {}, "OUTPUT_D_RESTORED.json")
    case_h = execute_case(
        "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
        {"semantic_role_authority_status": "NOT_CERTIFIED"},
        "OUTPUT_HOSTILE_CONTROL.json",
    )

    out_a = case_a["output"]
    out_b = case_b["output"]
    out_c = case_c["output"]
    out_d = case_d["output"]
    out_h = case_h["output"]

    for field in STRUCTURAL_COORDINATES:
        assertions.check(
            "A_POSITIVE",
            f"A_POSITIVE.COORD.{field}",
            f"positive branch preserves incoming {field}",
            fixture[field],
            out_a.get(field),
        )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.RESOLUTION",
        "positive branch reports the no-match preservation resolution",
        QUC_PRESERVED,
        out_a.get("question_relation_authority_resolution"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.REGISTRY_MATCH",
        "positive branch explicitly reports no selected-registry match",
        False,
        out_a.get("question_relation_registry_match"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.COVERAGE",
        "positive branch marks coverage eligible",
        True,
        out_a.get("question_relation_coverage_eligible"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.PRESSURE",
        "positive branch marks pressure eligible",
        True,
        out_a.get("question_relation_pressure_eligible"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.CURRENT_DIRECTIONAL",
        "positive branch retains inbound directional eligibility",
        True,
        out_a.get("current_directional_atom_eligible"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.V551_EVIDENCE",
        "positive branch retains inbound V551 relation-evidence permission",
        True,
        out_a.get("allowed_as_v551_relation_evidence"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.SEMANTIC_ROLE_AUTHORITY_STATUS",
        "positive branch preserves the inbound certified status",
        "CERTIFIED",
        out_a.get("semantic_role_authority_status"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.SEMANTIC_ROLE",
        "positive branch preserves the inbound relation-evidence role",
        "RELATION_EVIDENCE",
        out_a.get("semantic_role"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.STRUCTURAL_MAPPING",
        "positive branch preserves the inbound COMPLETE mapping label",
        "COMPLETE",
        out_a.get("structural_mapping_status"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.NO_MATCH_METADATA",
        "positive output separately records the underlying missing-authority status",
        "BLOCKED_MISSING_AUTHORITY",
        out_a.get("question_relation_authority_resolution_status"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.NO_AUTHORITY_PAYLOAD_HASH",
        "positive preservation branch does not acquire a signed authority row payload hash",
        "",
        out_a.get("authority_row_payload_hash"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.NO_RELATION_USE_STATUS",
        "positive preservation branch does not acquire a relation_use_status",
        "",
        out_a.get("relation_use_status"),
    )
    assertions.check(
        "A_POSITIVE",
        "A_POSITIVE.NO_AUTHORITY_STATUS",
        "positive preservation branch does not acquire an authority_status",
        "",
        out_a.get("authority_status"),
    )
    for field in STRUCTURAL_COORDINATES:
        assertions.check(
            "B_DENIED_PERMISSION",
            f"B_DENIED_PERMISSION.CLEARED.{field}",
            f"denied-permission branch clears {field}",
            "",
            out_b.get(field),
        )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.CURRENT_DIRECTIONAL",
        "denied-permission branch sets directional eligibility false",
        False,
        out_b.get("current_directional_atom_eligible"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.V551_EVIDENCE",
        "denied-permission branch sets V551 relation-evidence eligibility false",
        False,
        out_b.get("allowed_as_v551_relation_evidence"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.COVERAGE",
        "denied-permission branch sets coverage eligibility false",
        False,
        out_b.get("question_relation_coverage_eligible"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.PRESSURE",
        "denied-permission branch sets pressure eligibility false",
        False,
        out_b.get("question_relation_pressure_eligible"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.SEMANTIC_ROLE",
        "denied-permission branch does not retain relation-evidence role",
        "UNKNOWN",
        out_b.get("semantic_role"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.SEMANTIC_ROLE_AUTHORITY_STATUS",
        "denied-permission branch does not retain certified status",
        "NOT_CERTIFIED",
        out_b.get("semantic_role_authority_status"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.NO_PRESERVATION_LABEL",
        "denied-permission branch does not take the no-match preservation label",
        None,
        out_b.get("question_relation_authority_resolution"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.STRUCTURAL_MAPPING",
        "denied-permission branch records the missing-authority status as mapping status",
        "BLOCKED_MISSING_AUTHORITY",
        out_b.get("structural_mapping_status"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.NO_AUTHORITY_PAYLOAD_HASH",
        "denied-permission output does not acquire a signed authority row payload hash",
        "",
        out_b.get("authority_row_payload_hash"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.NO_RELATION_USE_STATUS",
        "denied-permission output does not acquire a relation_use_status",
        "",
        out_b.get("relation_use_status"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.NO_AUTHORITY_STATUS",
        "denied-permission output does not acquire an authority_status",
        "",
        out_b.get("authority_status"),
    )
    for field in STRUCTURAL_COORDINATES:
        assertions.check(
            "C_PARTIAL_MAPPING",
            f"C_PARTIAL_MAPPING.CLEARED.{field}",
            f"PARTIAL-mapping branch clears {field}",
            "",
            out_c.get(field),
        )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.NO_PRESERVATION_LABEL",
        "PARTIAL mapping does not take the no-match preservation label",
        None,
        out_c.get("question_relation_authority_resolution"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.CURRENT_DIRECTIONAL",
        "PARTIAL mapping sets directional eligibility false",
        False,
        out_c.get("current_directional_atom_eligible"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.V551_EVIDENCE",
        "PARTIAL mapping does not authorize V551 relation evidence",
        False,
        out_c.get("allowed_as_v551_relation_evidence"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.COVERAGE",
        "PARTIAL mapping sets coverage eligibility false",
        False,
        out_c.get("question_relation_coverage_eligible"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.PRESSURE",
        "PARTIAL mapping sets pressure eligibility false",
        False,
        out_c.get("question_relation_pressure_eligible"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.SEMANTIC_ROLE",
        "PARTIAL mapping does not retain relation-evidence role",
        "UNKNOWN",
        out_c.get("semantic_role"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.SEMANTIC_ROLE_AUTHORITY_STATUS",
        "PARTIAL mapping does not retain certified status",
        "NOT_CERTIFIED",
        out_c.get("semantic_role_authority_status"),
    )
    assertions.check(
        "C_PARTIAL_MAPPING",
        "C_PARTIAL_MAPPING.STRUCTURAL_MAPPING",
        "PARTIAL mapping is normalised to the missing-authority status",
        "BLOCKED_MISSING_AUTHORITY",
        out_c.get("structural_mapping_status"),
    )
    for field in STRUCTURAL_COORDINATES:
        assertions.check(
            "D_RESTORED",
            f"D_RESTORED.COORD.{field}",
            f"restored exact positive input preserves {field}",
            fixture[field],
            out_d.get(field),
        )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.OUTPUT_DICT_EQUALITY",
        "restored output is equal to the original positive output as a data structure",
        out_a,
        out_d,
    )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.CANONICAL_HASH_EQUALITY",
        "restored output canonical hash equals the positive canonical hash",
        case_a["output_canonical_sha256"],
        case_d["output_canonical_sha256"],
    )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.FILE_HASH_EQUALITY",
        "restored output file SHA-256 equals the positive output file SHA-256",
        case_a["output_file_sha256"],
        case_d["output_file_sha256"],
    )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.INPUT_HASH_EQUALITY",
        "restored input canonical hash equals the immutable positive fixture hash",
        EXPECTED_FIXTURE_CANONICAL_SHA256,
        case_d["input_canonical_sha256"],
    )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.REGISTRY_MATCH",
        "restored output still reports no selected-registry match",
        False,
        out_d.get("question_relation_registry_match"),
    )
    assertions.check(
        "D_RESTORED",
        "D_RESTORED.RESOLUTION",
        "restored output still reports the no-match preservation resolution",
        QUC_PRESERVED,
        out_d.get("question_relation_authority_resolution"),
    )
    for field in STRUCTURAL_COORDINATES:
        assertions.check(
            "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
            f"HOSTILE_CONTROL.CLEARED.{field}",
            f"removing inbound certification clears {field}",
            "",
            out_h.get(field),
        )
    assertions.check(
        "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
        "HOSTILE_CONTROL.NO_PRESERVATION_LABEL",
        "removing inbound certification prevents the no-match preservation branch",
        None,
        out_h.get("question_relation_authority_resolution"),
    )
    assertions.check(
        "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
        "HOSTILE_CONTROL.SEMANTIC_ROLE_AUTHORITY_STATUS",
        "F03 does not manufacture certification from its own no-match path",
        "NOT_CERTIFIED",
        out_h.get("semantic_role_authority_status"),
    )
    assertions.check(
        "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
        "HOSTILE_CONTROL.V551_EVIDENCE",
        "F03 does not manufacture V551 relation evidence without inbound certification",
        False,
        out_h.get("allowed_as_v551_relation_evidence"),
    )
    assertions.check(
        "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
        "HOSTILE_CONTROL.CURRENT_DIRECTIONAL",
        "F03 does not manufacture directional eligibility without inbound certification",
        False,
        out_h.get("current_directional_atom_eligible"),
    )
    assertions.check(
        "B_DENIED_PERMISSION",
        "B_DENIED_PERMISSION.OUTPUT_CONVERGES_WITH_PARTIAL",
        "denied-permission and PARTIAL inputs converge on the same normalised fail-closed output",
        case_c["output_canonical_sha256"],
        case_b["output_canonical_sha256"],
    )

    hostile_interpretation = {
        "rejected_conclusion": (
            "Because F03 preserved six coordinates and marked the inbound row "
            "certified, F03 itself established original source authority."
        ),
        "rejected": True,
        "positive_output_registry_match": out_a.get("question_relation_registry_match"),
        "positive_output_registry_match_is_false": out_a.get("question_relation_registry_match") is False,
        "positive_output_underlying_resolution_status": out_a.get(
            "question_relation_authority_resolution_status"
        ),
        "positive_output_authority_row_payload_hash": out_a.get("authority_row_payload_hash"),
        "positive_output_relation_use_status": out_a.get("relation_use_status"),
        "positive_output_authority_status": out_a.get("authority_status"),
        "inbound_certification_removed_control": {
            "output_file": case_h["output_file"],
            "output_canonical_sha256": case_h["output_canonical_sha256"],
            "preservation_label": out_h.get("question_relation_authority_resolution"),
            "semantic_role_authority_status": out_h.get("semantic_role_authority_status"),
            "allowed_as_v551_relation_evidence": out_h.get(
                "allowed_as_v551_relation_evidence"
            ),
        },
        "conclusion": (
            "The preservation branch conditionally preserves six already-present "
            "inbound coordinates and the inbound CERTIFIED/RELATION_EVIDENCE labels. "
            "It explicitly reports question_relation_registry_match=false and "
            "question_relation_authority_resolution_status=BLOCKED_MISSING_AUTHORITY. "
            "It does not establish who certified the source, whether that issuer was "
            "competent, or whether original source/scientific permissions exist."
        ),
        "limitation": (
            "The supplemental control removes inbound certification and shows F03 "
            "fails closed; this is consistent with F03 consuming, not creating, "
            "semantic authority. It does not by itself prove the provenance of the "
            "inbound flags in the original historical production run."
        ),
    }

    execution_record = {
        "command": [sys.executable, *sys.argv],
        "cwd": os.getcwd(),
        "test_script": str(Path(__file__).resolve()),
        "module_import_path": str(source_path),
        "module_import_method": "importlib.util.spec_from_file_location",
        "function": f"{function.__module__}.{function.__qualname__}",
        "function_source_file": str(function_source_file),
        "function_source_start_line": function_start_line,
        "function_source_end_line": function_start_line + len(function_lines) - 1,
        "function_source_sha256": sha256_bytes("".join(function_lines).encode("utf-8")),
        "test_time_invocation_path": (
            "run_f03_s2_native.py::execute_case -> "
            "ddm_v550_question_relation_authority.apply_question_relation_authority"
        ),
        "test_time_first_reader": (
            "run_f03_s2_native.py::execute_case and the assertion checks in "
            "AssertionLog are the first code that reads the returned output"
        ),
        "original_historical_production_first_reader": "NOT_PROVED",
        "test_time_reader_is_not_original_first_reader": True,
        "first_reader_caveat": (
            "The test-time invocation path and first reader prove only how this "
            "author-side synthetic experiment called and read the historical "
            "function. They are not proof of the original historical production "
            "first reader, its call site, its inputs, or its authority."
        ),
        "canonical_serialization": CANONICAL_SERIALIZATION,
        "pretty_serialization": PRETTY_SERIALIZATION,
    }

    environment = {
        "runner_user": getpass.getuser(),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "system": platform.system(),
        "release": platform.release(),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "python_version_info": list(sys.version_info),
        "pandas_version": __import__("pandas").__version__,
        "process_id": os.getpid(),
        "timezone": datetime.now(timezone.utc).astimezone().tzname(),
        "utc_observation": datetime.now(timezone.utc).isoformat(),
        "cwd": os.getcwd(),
        "relevant_env": {
            "RAWLSING_QUESTION_RELATION_AUTHORITY_PATH": os.environ.get(
                "RAWLSING_QUESTION_RELATION_AUTHORITY_PATH"
            ),
            "DDM_AUTHORITY_ROOT": os.environ.get("DDM_AUTHORITY_ROOT"),
            "PYTHONHASHSEED": os.environ.get("PYTHONHASHSEED"),
        },
    }

    cases = [case_a, case_b, case_c, case_d, case_h]
    cases_public = []
    for case in cases:
        cases_public.append(
            {
                "case_id": case["case_id"],
                "mutation": case["mutation"],
                "input": case["input"],
                "input_canonical_sha256": case["input_canonical_sha256"],
                "input_file_sha256": case["input_file_sha256"],
                "output_file": case["output_file"],
                "output_file_sha256": case["output_file_sha256"],
                "output_canonical_sha256": case["output_canonical_sha256"],
                "output": case["output"],
            }
        )

    witness = {
        "witness_id": "ZAK01-S2-F03-NATIVE-20261111-R1",
        "contract_id": "ZAK01-MCR-AF-INVESTIGATION-20261110",
        "obligation_id": "ZAK01-HOSTILE",
        "receipt_kind": "AUTHOR_SIDE_CANDIDATE_EVIDENCE_ONLY",
        "minimum_grade_required": "S2",
        "actual_grade": "S2_NATIVE_SYNTHETIC_FIXTURE_EXECUTION",
        "not_an_independent_reviewer": True,
        "independent_receiving": "PENDING",
        "status": "PASS" if not assertions.failures else "FAIL",
        "result_code": (
            "F03_S2_POSITIVE_DENIED_PARTIAL_RESTORED_PROVED__"
            "PENDING_INDEPENDENT_RECEIVING"
            if not assertions.failures
            else "F03_S2_NATIVE_EXECUTION_FAILED__SEE_ASSERTIONS"
        ),
        "scope": (
            "S2 synthetic-fixture execution of the actual historical "
            "apply_question_relation_authority function. No respondent data, "
            "no S3, and no original production first-reader proof."
        ),
        "excluded_scope": [
            "S3",
            "original respondent-data execution",
            "original historical production first reader",
            "independent semantic/scientific/source issuance",
            "independent receiving",
        ],
        "source_pin": {
            **EXPECTED_SOURCE,
            "executed_path": str(source_path),
            "observed_bytes": len(source_bytes),
            "observed_sha256": sha256_bytes(source_bytes),
            "observed_git_blob_sha1": git_blob_sha1(source_bytes),
            "loaded_index_sha256": index.file_sha256,
        },
        "registry_pin": {
            **EXPECTED_REGISTRY,
            "executed_path": str(registry_path),
            "observed_bytes": len(registry_bytes),
            "observed_sha256": sha256_bytes(registry_bytes),
            "observed_git_blob_sha1": git_blob_sha1(registry_bytes),
            "loaded_index_sha256": index.file_sha256,
        },
        "environment": environment,
        "execution": execution_record,
        "fixture": {
            "path": str(fixture_path),
            "file_sha256": sha256_bytes(fixture_file_bytes),
            "canonical_sha256": sha256_bytes(fixture_canonical),
            "canonical_bytes": len(fixture_canonical),
            "git_blob_sha1": git_blob_sha1(fixture_file_bytes),
            "question_identity": {
                "source_family": fixture["source_family"],
                "canonical_wave": fixture["canonical_wave"],
                "country_code": fixture["country_code"],
                "question_id": fixture["question_id"],
                "var_code": fixture["var_code"],
            },
            "no_match_proof": {
                "direct_scan": no_match_scan,
                "resolver_status": assertion.status,
                "resolver_match_count": assertion.match_count,
                "resolver_lookup_key": assertion.lookup_key,
                "resolver_resolved": assertion.resolved,
            },
        },
        "cases": cases_public,
        "case_convergence": {
            "cases_with_equal_output": [
                "B_DENIED_PERMISSION",
                "C_PARTIAL_MAPPING",
                "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED",
            ],
            "output_canonical_sha256": case_b["output_canonical_sha256"],
            "input_canonical_sha256": {
                "B_DENIED_PERMISSION": case_b["input_canonical_sha256"],
                "C_PARTIAL_MAPPING": case_c["input_canonical_sha256"],
                "HOSTILE_CONTROL_INBOUND_CERTIFICATION_REMOVED": case_h[
                    "input_canonical_sha256"
                ],
            },
            "explanation": (
                "The three inputs are distinct, as their input hashes show. B "
                "changes only allowed_as_v551_relation_evidence, C changes only "
                "structural_mapping_status, and the supplemental control changes "
                "only semantic_role_authority_status. Each fails the same "
                "quc_is_certified gate, and the historical function normalises "
                "all three into the same fail-closed cleared-coordinate output. "
                "The equal output hashes are therefore an observed property of "
                "the historical branch, not duplicated case execution."
            ),
        },
        "restoration": {
            "positive_case": "A_POSITIVE",
            "restored_case": "D_RESTORED",
            "positive_output_file_sha256": case_a["output_file_sha256"],
            "restored_output_file_sha256": case_d["output_file_sha256"],
            "positive_output_canonical_sha256": case_a["output_canonical_sha256"],
            "restored_output_canonical_sha256": case_d["output_canonical_sha256"],
            "output_dicts_equal": out_a == out_d,
            "file_hashes_equal": case_a["output_file_sha256"]
            == case_d["output_file_sha256"],
            "canonical_hashes_equal": case_a["output_canonical_sha256"]
            == case_d["output_canonical_sha256"],
            "documented_serialization": CANONICAL_SERIALIZATION,
        },
        "hostile_interpretation": hostile_interpretation,
        "assertions": assertions.items,
        "assertion_summary": assertions.summary(),
        "failures": assertions.failures,
    }

    witness_path = out_dir / "WITNESS.json"
    witness_path.write_bytes(pretty_json_bytes(witness))

    print("ZAK01-S2-F03-NATIVE")
    print(f"status={witness['status']}")
    print(f"result_code={witness['result_code']}")
    print(f"source_sha256={witness['source_pin']['observed_sha256']}")
    print(f"registry_sha256={witness['registry_pin']['observed_sha256']}")
    print(f"fixture_canonical_sha256={witness['fixture']['canonical_sha256']}")
    for case in cases_public:
        print(
            f"{case['case_id']} output_sha256={case['output_canonical_sha256']} "
            f"file_sha256={case['output_file_sha256']}"
        )
    print(
        "restoration_equal="
        f"{witness['restoration']['canonical_hashes_equal'] and witness['restoration']['file_hashes_equal']}"
    )
    print(f"assertions={witness['assertion_summary']}")
    print(f"witness={witness_path}")
    if assertions.failures:
        for failure in assertions.failures:
            print(
                "FAILED "
                f"{failure['case']} {failure['assertion_id']} "
                f"expected={failure['expected']!r} actual={failure['actual']!r}",
                file=sys.stderr,
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
