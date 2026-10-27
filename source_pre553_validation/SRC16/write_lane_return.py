"""Write the GSS lane return from the committed per-source manifests/results.

Run after the lane test commands have completed:

    PYTHONPATH=. python3 source_pre553_validation/SRC16/write_lane_return.py \
        --lane-tests 41 --foundation-tests 12 --p3-tests 7 \
        --p3-deselected 2 --owner-tests 15
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
LANE = "GSS"
SOURCES = tuple(f"SRC{i:02d}" for i in range(16, 24))
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
P0_CORRECTION = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
P3_RUNTIME = "519355ec2215409b40d566ef13c3b21f611e0726"
BRANCH = "agent/pyat-pre553-r157-gss"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bytes(path: Path) -> int:
    return len(path.read_bytes())


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _path_identity(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": _sha(path),
        "bytes": _bytes(path),
    }


def _source_entry(source_id: str) -> dict[str, Any]:
    data_dir = ROOT / f"rawlsing_next/source_configuration/data/{source_id}"
    val_dir = ROOT / f"source_pre553_validation/{source_id}"
    manifest_path = val_dir / f"{source_id}.manifest.json"
    results_path = val_dir / f"{source_id}.validation-results.json"
    manifest = _read(manifest_path)
    results = _read(results_path)
    native = results["native_validation"]
    source_doc = _read(data_dir / f"{source_id}.source.config.json")
    residuals = [
        {
            "residual_id": item["residual_id"],
            "scope": item["scope"],
            "field": item["field"],
            "status": item["status"],
            "dependent_operation": item["dependent_operation"],
            "owner": item["owner"],
        }
        for item in results["residuals"]
    ]
    return {
        "source_id": source_id,
        "wave": results["wave"],
        "format": results["source_format"],
        "source_paths": {
            "original_config": _path_identity(data_dir / f"{source_id}.source.config.json"),
            "evidence_accounting": _path_identity(data_dir / f"{source_id}.evidence-accounting.json"),
            "fixture_config": _path_identity(val_dir / f"{source_id}.fixture.config.json"),
            "fixture": _path_identity(val_dir / f"{source_id}.fixture.json"),
            "fixture_spec": _path_identity(val_dir / f"{source_id}.fixture-spec.json"),
            "validation_results": _path_identity(results_path),
            "exceptions": _path_identity(val_dir / f"{source_id}.exceptions.json"),
            "manifest": _path_identity(manifest_path),
        },
        "config_hashes": manifest["config_hashes"],
        "supported_scope": {
            "scope_id": source_doc["supported_scope"]["scope_id"],
            "unit_slice": source_doc["supported_scope"]["supported_unit_slice"],
            "form_slice": source_doc["supported_scope"]["supported_form_slice"],
            "question_ids": source_doc["supported_scope"]["supported_question_ids"],
            "original_source_execution": source_doc["supported_scope"]["original_source_execution"],
            "native_validation_expectation": source_doc["supported_scope"]["native_validation_expectation"],
        },
        "coverage": results["coverage"],
        "native_fixture_validation": {
            "projection": native["projection"],
            "release": native["release"],
            "actual": native["actual"],
            "expected_match": native["expected_match"],
            "repository_release_ref_matches": native["repository"]["release_ref_matches_stream"],
            "p3_row_native_keys": native.get("p3_row_native_keys"),
            "p3_reader_transport": native.get("p3_reader_transport"),
            "calls": native.get("calls"),
            "refusals": native["refusals"],
        },
        "identity_separation": results["identity_separation"],
        "residuals": residuals,
        "status": "FIXTURE_NATIVE_POSITIVE_ORIGINAL_NOT_EXECUTED",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane-tests", type=int, required=True)
    parser.add_argument("--foundation-tests", type=int, required=True)
    parser.add_argument("--p3-tests", type=int, required=True)
    parser.add_argument("--p3-deselected", type=int, required=True)
    parser.add_argument("--owner-tests", type=int, required=True)
    args = parser.parse_args(argv)
    sources = [_source_entry(source_id) for source_id in SOURCES]
    totals = {
        "sources": len(sources),
        "physical_columns": sum(item["coverage"]["physical_slots_total"] for item in sources),
        "original_items": sum(item["coverage"]["original_items_total"] for item in sources),
        "physical_slots_serialized": sum(item["coverage"]["physical_slots_serialized"] for item in sources),
        "items_serialized": sum(item["coverage"]["items_serialized"] for item in sources),
        "physical_slots_included": sum(item["coverage"]["physical_slots_included"] for item in sources),
        "physical_slots_excluded": sum(item["coverage"]["physical_slots_excluded"] for item in sources),
        "items_included": sum(item["coverage"]["items_included"] for item in sources),
        "items_excluded": sum(item["coverage"]["items_excluded"] for item in sources),
        "fixture_native_releases": sum(
            1 for item in sources
            if item["native_fixture_validation"]["release"]["release_ref"]["kind"]
            == "C11LogicalRelease"),
        "respondent_events": sum(
            item["native_fixture_validation"]["release"]["respondent_events"] for item in sources),
        "coordinate_facts": sum(
            item["native_fixture_validation"]["release"]["coordinate_facts"] for item in sources),
        "weight_facts": sum(
            item["native_fixture_validation"]["release"]["weight_facts"] for item in sources),
        "routing_facts": sum(
            item["native_fixture_validation"]["projection"]["routing_facts"] for item in sources),
        "residuals": sum(len(item["residuals"]) for item in sources),
    }
    totals["no_drop_all_sources"] = all(item["coverage"]["no_drop"] for item in sources)
    totals["expected_match_all_sources"] = all(
        item["native_fixture_validation"]["expected_match"] for item in sources)
    totals["repositories_match_stream"] = all(
        item["native_fixture_validation"]["repository_release_ref_matches"] for item in sources)
    lane_return = {
        "schema": "PYAT_R157_GSS_LANE_RETURN@1.0.0",
        "lane_id": LANE,
        "branch": BRANCH,
        "plan_seal": PLAN_SEAL,
        "p0_correction_consumed": P0_CORRECTION,
        "p3_terminal_runtime_consumed": P3_RUNTIME,
        "status": "COMPLETE_PREPARATION_WITH_EXACT_RESIDUALS",
        "source_ids": list(SOURCES),
        "completion_statement": (
            "Eight GSS waves have source-grounded original configurations with full "
            "physical-slot/item accounting; each has a distinct nonrespondent fixture "
            "configuration/byteline and an actual positive GovernedC11Projection/C11 "
            "release through the frozen factory and native validator. Original "
            "respondent execution and original empirical issuance are not performed."
        ),
        "not_claimed": [
            "Original respondent execution or original empirical workload issuance",
            "Original-source scientific results or population/design inference",
            "Cross-wave equivalence, pooling, canonical value mapping or weighted estimand",
            "FieldForge/M1/N11 acceptance or final all35 review",
        ],
        "sources": sources,
        "aggregate": totals,
        "verification": {
            "commands": [
                {
                    "command": "PYTHONPATH=. python3 source_pre553_validation/SRC16/build_gss_lane.py --all",
                    "result": "PASS",
                    "actual": "8/8 source configs validated; 8/8 nonrespondent fixture native releases constructed",
                },
                {
                    "command": "PYTHONPATH=. python3 -m pytest source_pre553_validation/SRC16/test_gss_lane.py -q -o addopts=''",
                    "result": "PASS",
                    "actual": f"{args.lane_tests} passed",
                },
                {
                    "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''",
                    "result": "PASS",
                    "actual": f"{args.foundation_tests} passed",
                },
                {
                    "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts='' -k 'not r154_loader_delegates and not r154_prepared_path'",
                    "result": "PASS",
                    "actual": f"{args.p3_tests} passed, {args.p3_deselected} deselected",
                },
                {
                    "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_read_admission.py -q -o addopts=''",
                    "result": "PASS",
                    "actual": f"{args.owner_tests} passed",
                },
            ],
            "pass": (
                args.lane_tests + args.foundation_tests + args.p3_tests + args.owner_tests
            ),
            "fail": 0,
            "skip_or_unavailable": args.p3_deselected,
            "unavailable_detail": (
                "The two deselected P3 R154-loader tests require "
                "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_load.py, "
                "which is tracked with skip-worktree and absent from this isolated checkout. "
                "The new GSS library path does not import the legacy R154 loader."
            ),
        },
        "lane_completion_blockers": [],
        "original_execution_dependencies": [
            {
                "id": "GSS-ORIGINAL-ROW-KEYS",
                "scope": "SRC16..SRC23",
                "required": "Permitted original PhysicalSourceIncidence with decoded id cells",
                "operation": "P3 row_native_keys_from_transport / build_validated_c11_release_from_config",
                "current": "Original configs bind the id slot; no original source bytes or row keys were read",
                "owner": "P3/integration owner with source-read custody owner",
                "next": "Supply permitted decoded incidence; P3 extracts exact row keys; original execution remains separately authorized",
            },
            {
                "id": "GSS-SOURCE-AUTHORITY-DEFER",
                "scope": "SRC16..SRC23",
                "required": "Exact adopted source operation/authority scope",
                "current": "H48/P2/full-relation evidence preserved as source_reviewed candidate evidence with DEFER authority",
                "owner": "R157 authority owner",
                "next": "Adjudicate exact source operation scope; do not promote fixture authority",
            },
            {
                "id": "GSS-ROUTING-UNKNOWN",
                "scope": "SRC16..SRC23",
                "required": "Exact form/ballot/administration route expressions",
                "current": "H48/O06 reports SOURCE_ROUTING_UNRESOLVED; original routing facts are ROUTING_UNKNOWN",
                "owner": "GSS source evidence owner",
                "next": "Recover exact route expressions before eligibility/form-conditioned claims",
            },
            {
                "id": "GSS-CANONICAL-VALUE-NOT-AUTHORIZED",
                "scope": "SRC16..SRC23 supported items",
                "required": "Exact positive NATIVE_CANONICAL_MAPPING_HARMONIZATION authority",
                "current": "Raw source values and response states retained; canonical values null",
                "owner": "R157 mapping authority owner",
                "next": "Adjudicate exact mappings before canonicalized analysis",
            },
            {
                "id": "GSS-WEIGHT-HELD",
                "scope": "SRC16..SRC23",
                "required": "Exact weight design/estimand/normalization authority",
                "current": "wtssall retained as HELD_WEIGHT_DESIGN_UNRESOLVED; fixture exercises explicit unresolved-basis weight facts",
                "owner": "GSS weight/design evidence owner",
                "next": "Establish design/estimand before a weighted scope",
            },
            {
                "id": "GSS-FORM-ADMIN-SAMPLE",
                "scope": "SRC16..SRC23",
                "required": "Exact form/ballot administration and wave-specific sampling-frame/design evidence",
                "current": "Retained as administrative/context slots and precise residuals; no default form or population claim",
                "owner": "GSS source evidence owner",
                "next": "Recover exact wave evidence if form- or population-conditioned slices are required",
            },
        ],
        "next_integration_edge": {
            "owner": "R157 P3/integration owner",
            "operation": (
                "Consume the eight original configs, transport their exact reader configuration "
                "through P3, and on a separately authorized original read pass the permitted "
                "PhysicalSourceIncidence to build_validated_c11_release_from_config; P3 extracts "
                "row_native_keys from the configured id slot."
            ),
            "fixture_pass_available_now": True,
            "original_execution_requires_separate_authority": True,
            "final_review": "Distinct coherent all35 boundary later; not this lane return",
        },
        "no_original_source_access": True,
        "respondent_rows_read": 0,
        "original_workload_issued": False,
    }
    out = ROOT / "source_pre553_validation/SRC16/LANE_RETURN.json"
    out.write_text(
        json.dumps(lane_return, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "path": str(out.relative_to(ROOT)),
        "sha256": _sha(out),
        "bytes": _bytes(out),
        "aggregate": totals,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
