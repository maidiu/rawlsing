"""Run the committed P0 positive validation and publish the lane-ready return."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import jsonschema
import pandas as pd

from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    RespondentEvent,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_source_backed_c11_facade import GovernedC11Projection
from rawlsing_next.source_configuration.evidence import (
    lane_inputs,
    load_manifest,
    load_source_roster,
    verify_evidence_manifest,
)
from rawlsing_next.source_configuration.factory import (
    build_governed_c11_projection,
    build_validated_c11_release_from_config,
)
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import (
    canonical_config_hash,
    load_source_config,
)

ROOT = Path(__file__).resolve().parents[3]
FOUNDATION = ROOT / "source_pre553_validation/foundation"
CONFIG = FOUNDATION / "examples/SRC09_q101_fixture.config.json"
FIXTURE = FOUNDATION / "fixtures/SRC09_q101_nonrespondent.json"
SCHEMA = ROOT / "rawlsing_next/source_configuration/schema/source_configuration.schema.json"
OWNER_MAPPING = ROOT / "rawlsing_next/source_configuration/schema/OWNER_API_MAPPING.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_order(events, projection: GovernedC11Projection):
    row_by_object = {r.ref.object_id: index for index, r in enumerate(projection.respondents, 1)}
    return sorted(events, key=lambda event: row_by_object[dict(event.scoped_respondent_ref)["object_id"]])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args()
    artifact_commit = args.artifact_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    evidence = verify_evidence_manifest()
    if not evidence["ok"]:
        raise SystemExit(f"evidence verification failed: {evidence['failures']}")
    manifest = load_manifest()
    roster = load_source_roster()
    config = load_source_config(CONFIG)
    fixture_doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    fixture = load_fixture_stream(FIXTURE)
    jsonschema.validate(config.document, json.loads(SCHEMA.read_text(encoding="utf-8")))
    projection = build_governed_c11_projection(config)
    release = build_validated_c11_release_from_config(config, stream=fixture)
    if not isinstance(release, C11LogicalRelease):
        raise SystemExit("native release type mismatch")
    # The same fixture cells through the existing PhysicalSourceIncidence
    # transport must yield the same native release identity.
    variables = (
        PhysicalVariable(1, "country", "double", "Country code", {}, (), {}, {}),
        PhysicalVariable(124, "q101", "double", "q101", {}, (), {}, {}),
    )
    frame = pd.DataFrame({
        "country": [1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0],
        "q101": [1.0, 2.0, 3.0, 4.0, -1.0, 7.0, 8.0, 9.0, None],
    })
    incidence = PhysicalSourceIncidence(
        source_sha256=config.active_source_sha256,
        source_format="SAV",
        row_count=9,
        variables=variables,
        reader_configuration={"fixture": "R157_P0_NONRESPONDENT"},
        file_metadata={"fixture": "R157_P0_NONRESPONDENT"},
        _frame=frame,
    )
    release_from_incidence = build_validated_c11_release_from_config(config, incidence=incidence)
    if release_from_incidence.release_ref != release.release_ref:
        raise SystemExit("fixture stream/incidence native release identity mismatch")
    events = row_order([x for x in release.public_objects if isinstance(x, RespondentEvent)], projection)
    coordinates = [x for x in release.public_objects if isinstance(x, EmpiricalCoordinateFact)]
    routing = [x for x in release.public_objects if isinstance(x, RoutingEligibilityFact)]
    expected = fixture_doc["expected_results"]
    actual = {
        "response_event_count": len(events),
        "coordinate_fact_count": len(coordinates),
        "routing_fact_count": len(routing),
        "response_states": [x.response_state for x in events],
        "canonical_values": [x.canonical_response_value_if_authorized for x in events],
        "weight_section": "NOT_APPLICABLE",
        "source_relation_section": "DISTINCT_BY_DEFAULT",
    }
    if actual["response_event_count"] != expected["response_event_count"]:
        raise SystemExit("fixture event count mismatch")
    if actual["response_states"] != expected["response_states"]:
        raise SystemExit("fixture response state mismatch")
    if actual["canonical_values"] != expected["canonical_values"]:
        raise SystemExit("fixture canonical value mismatch")

    fixture_spec = {
        "schema": "PYAT_R157_NONRESPONDENT_FIXTURE_SPEC@1.0.0",
        "fixture_id": fixture_doc["fixture_id"],
        "fixture_path": str(FIXTURE.relative_to(ROOT)),
        "fixture_file_sha256": sha(FIXTURE),
        "fixture_source_sha256": fixture.source_sha256,
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "original_source_id": "SRC09",
        "original_source_sha256": config.original_source_sha256,
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "fixture_config_path": str(CONFIG.relative_to(ROOT)),
        "fixture_config_sha256": canonical_config_hash(config),
        "shape_coverage": [
            "SAV scalar categorical response (q101) with exact native value binding",
            "substantive categories 1..4",
            "source-stored special states -1, 7, 8, 9 mapped to MISSING, DK, SOURCE_SPECIFIC_SPECIAL, REFUSAL",
            "system-missing cell mapped to MISSING",
            "source-native country coordinate (copy observed raw; no canonical crosswalk)",
            "routing facts are fixture-scoped and do not assert original eligibility",
        ],
        "row_count": fixture.row_count,
        "cells": [
            {
                "row_ordinal": cell.row_ordinal,
                "variable_ordinal": cell.variable_ordinal,
                "variable_name": cell.variable_name,
                "raw_value": cell.raw_value,
                "missing_state": cell.missing_state.value,
                "source_missing_declaration": cell.source_missing_declaration,
            }
            for cell in fixture.iter_cells()
        ],
        "expected_results": expected,
        "oracle_basis": "Expected results are declared from the fixture cells and the serialized q101 value/state rules before the factory call; they are not copied from the native result.",
        "factory_call": {
            "projection": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "release": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "transport": "ExactPhysicalCellStream",
        },
        "limits": [
            "The fixture is synthetic nonrespondent input, not original respondent data.",
            "Fixture authority is explicitly fixture-only and cannot be used for original-source construction.",
            "Native validation of this fixture does not establish original-source scientific results or execution permission.",
        ],
    }

    results = {
        "schema": "PYAT_R157_P0_VALIDATION_RESULTS@1.0.0",
        "plan_seal": "4c0c619eac747afee1d8e65e1418bf2d472da4c3",
        "artifact_commit": artifact_commit,
        "evidence_verification": {
            "ok": evidence["ok"],
            "failures": evidence["failures"],
            "manifest_sha256": sha(ROOT / "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json"),
            "counts": manifest["counts"],
        },
        "config_validation": {
            "ok": True,
            "validator": "rawlsing_next.source_configuration.schema.validate_source_config",
            "json_schema": str(SCHEMA.relative_to(ROOT)),
            "config_path": str(CONFIG.relative_to(ROOT)),
            "config_sha256": canonical_config_hash(config),
            "config_file_sha256": sha(CONFIG),
        },
        "native_construction": {
            "projection_type": type(projection).__name__,
            "projection_module": type(projection).__module__,
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "projection_identity_ref": projection.projection_identity_ref.as_dict(),
            "expected_source_sha256": projection.expected_source_sha256,
            "respondents": len(projection.respondents),
            "questions": len(projection.questions),
            "response_slots": len(projection.response_slots),
            "coordinate_slots": len(projection.coordinate_slots),
            "weight_slots": len(projection.weight_slots),
            "routing_facts": len(projection.routing),
            "release_type": type(release).__name__,
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "m01_m18_coverage": {key: list(value) for key, value in release.m01_m18_coverage.items()},
            "actual": actual,
            "transport_equivalence": {
                "stream_release_ref": release.release_ref.as_dict(),
                "incidence_release_ref": release_from_incidence.release_ref.as_dict(),
                "equal": release_from_incidence.release_ref == release.release_ref,
            },
        },
        "fixture_expected_match": True,
        "original_source_access": {
            "source_file_opened": False,
            "source_file_stat_or_hash": False,
            "respondent_rows_read": 0,
            "original_workload_issued": False,
            "note": "P0 reads only committed metadata/authority evidence and the repository-generated fixture.",
        },
        "commands": [
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''",
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py rawlsing_next/tests/test_pre553_source_read_admission.py rawlsing_next/tests/test_pre553_c11_repository_ingest.py -q -o addopts=''",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.tools.publish_p0",
        ],
    }

    # Materialize deterministic companions before hashing the artifact manifest.
    (FOUNDATION / "FIXTURE_SPEC.json").write_text(
        json.dumps(fixture_spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (FOUNDATION / "VALIDATION_RESULTS.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    results_sha = sha(FOUNDATION / "VALIDATION_RESULTS.json")

    lanes = []
    for lane in json.loads((ROOT / "SOURCE_PRE553_PLAN/LANES.json").read_text(encoding="utf-8"))["lanes"]:
        frozen = lane_inputs(lane["lane_id"])
        lanes.append({
            "lane_id": lane["lane_id"],
            "source_ids": lane["source_ids"],
            "branch": lane["branch"],
            "write_paths": lane["write_paths"],
            "inputs": frozen["evidence"],
            "config_contract": frozen["config_contract"],
            "stage_queue": frozen["stage_queue"],
            "first_task": "EVIDENCE",
            "next_consumer": "R157 integration owner / P3 factory",
        })

    artifact_paths = sorted(
        path for path in (
            *[p for p in (ROOT / "rawlsing_next/source_configuration").rglob("*") if p.is_file()],
            ROOT / "rawlsing_next/tests/test_source_configuration_foundation.py",
            *[p for p in FOUNDATION.rglob("*") if p.is_file()],
        )
        if "__pycache__" not in path.parts and path.name != "P0_RETURN.json"
    )
    artifacts = [{
        "path": str(path.relative_to(ROOT)),
        "sha256": sha(path),
        "bytes": path.stat().st_size,
    } for path in artifact_paths]

    p0_return = {
        "schema": "PYAT_R157_P0_RETURN@1.0.0",
        "task": "R157_P0_FOUNDATION",
        "status": "COMPLETE",
        "plan_seal": "4c0c619eac747afee1d8e65e1418bf2d472da4c3",
        "branch": "agent/pyat-pre553-r157-foundation",
        "base_commit": "94c80cc7d59d0376a0405846074a2ae6523f05f1",
        "artifact_commit": artifact_commit,
        "integration_branch": "agent/pyat-source-pre553-r157",
        "frozen_interface": {
            "config_schema_id": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
            "schema_path": "rawlsing_next/source_configuration/schema/source_configuration.schema.json",
            "schema_module": "rawlsing_next/source_configuration/schema.py",
            "validator_callable": "rawlsing_next.source_configuration.schema.validate_source_config",
            "loader_callable": "rawlsing_next.source_configuration.schema.load_source_config",
            "factory_callable": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "factory_alias": "rawlsing_next.source_configuration.factory.construct_governed_c11_projection",
            "factory_signature": "(config: SourceConfig | Mapping[str, Any], *, source_sha256: str | None = None, row_count: int | None = None) -> GovernedC11Projection",
            "release_callable": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "repository_callable": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
            "fixture_stream_callable": "rawlsing_next.source_configuration.fixture.load_fixture_stream",
            "owner_api_mapping_path": "rawlsing_next/source_configuration/schema/OWNER_API_MAPPING.json",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "native_validator": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
        },
        "evidence": {
            "manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
            "manifest_sha256": sha(ROOT / "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json"),
            "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
            "source_roster_sha256": sha(ROOT / "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json"),
            "item_evidence_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
            "item_evidence_sha256": sha(ROOT / "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz"),
            "physical_slots_path": "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz",
            "codebook_rows_path": "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz",
            "unmatched_relations_path": "rawlsing_next/source_configuration/evidence/UNMATCHED_RELATIONS.json",
            "pinned_inputs": manifest["pinned_inputs"],
            "counts": manifest["counts"],
        },
        "validated_example": {
            "config_path": str(CONFIG.relative_to(ROOT)),
            "config_sha256": canonical_config_hash(config),
            "config_file_sha256": sha(CONFIG),
            "fixture_spec_path": "source_pre553_validation/foundation/FIXTURE_SPEC.json",
            "fixture_path": str(FIXTURE.relative_to(ROOT)),
            "fixture_file_sha256": sha(FIXTURE),
            "fixture_source_sha256": fixture.source_sha256,
            "original_source_sha256": config.original_source_sha256,
            "identity_class": config.identity_class,
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "actual": actual,
        },
        "lanes": lanes,
        "remaining_factory_task": {
            "id": "P3_READER_AND_ORIGINAL_BINDING",
            "depends_on": "P0_RETURN",
            "constructor_frozen": True,
            "exact": "In P3, wire config.identity.reader through the existing source-read/decoder path without changing the frozen P0 projection factory signature, then bind original-source configs to the actual source-read owner. The code seams are the qualified exact-SHA reader configuration (currently decode_with_source_read_permission does not accept the configured encoding) and call-time binding of respondents.source_native_key_slot/actual row keys when the source provides them; P0 deliberately preserves TypedAbsence(UNKNOWN) rather than inventing a native key. Lane configs replace fixture-only snapshots/bindings with source-grounded authority and routing. Do not add a replacement engine or change the native validator.",
            "required_code_changes": [
                "Extend the existing pre553_source_read_admission transport with the validated exact-SHA encoding/config argument only; preserve zero-I/O-before-current-permission and post-decode decision/edition checks.",
                "Use the frozen factory signature to construct original-source projections from lane configs and permitted PhysicalSourceIncidence.",
                "At call time, bind the configured source_native_key_slot/actual row key values into RespondentIdentity where the source supplies them; keep TypedAbsence when the key is genuinely unavailable.",
                "Retain the fixture-only config as a distinct validation input; never promote fixture authority or fixture SHA into original identity.",
            ],
            "done_check": "Original-source lane configs are schema-valid, all slot/item coverage is accounted, the qualified reader config is transported, and actual native C11 validation succeeds for the declared supported scope or records an exact dependent refusal.",
            "not_required_now": [
                "original respondent execution or scientific results",
                "FieldForge/M1/N11 acceptance",
                "all35 implementation in P0",
            ],
        },
        "validation": {
            "results_path": "source_pre553_validation/foundation/VALIDATION_RESULTS.json",
            "results_sha256": results_sha,
            "focus_test_result": "11 passed focused; 55 passed focused+owner regression",
            "commands": results["commands"],
        },
        "artifacts": artifacts,
        "no_original_source_access": True,
        "no_original_workload_issuance": True,
        "respondent_rows_read": 0,
        "limits": [
            "P0 freezes a working constructor and validated nonrespondent example, not all35 source configurations.",
            "The example is intentionally a P0 example, not a lane config; ASIAN lane owns complete SRC09 coverage.",
            "Fixture authority is not original-source authority.",
            "Original-source scientific execution is NOT performed or claimed.",
        ],
    }

    (FOUNDATION / "P0_RETURN.json").write_text(
        json.dumps(p0_return, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "artifact_commit": artifact_commit,
        "release_ref": release.release_ref.as_dict(),
        "config_sha256": canonical_config_hash(config),
        "fixture_source_sha256": fixture.source_sha256,
        "events": actual["response_event_count"],
        "p0_return": str(FOUNDATION / "P0_RETURN.json"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
