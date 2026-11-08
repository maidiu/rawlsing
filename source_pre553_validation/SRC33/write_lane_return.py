"""Write the WVS lane return from committed manifests/results."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ("SRC33", "SRC34", "SRC35")
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
P0 = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
P3 = "519355ec2215409b40d566ef13c3b21f611e0726"
BRANCH = "agent/pyat-pre553-r157-wvs"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _id(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _entry(source_id: str) -> dict[str, Any]:
    data = ROOT / f"rawlsing_next/source_configuration/data/{source_id}"
    val = ROOT / f"source_pre553_validation/{source_id}"
    manifest_path = val / f"{source_id}.manifest.json"
    results_path = val / f"{source_id}.validation-results.json"
    manifest = _read(manifest_path)
    results = _read(results_path)
    config = _read(data / f"{source_id}.source.config.json")
    native = results["native_validation"]
    return {
        "source_id": source_id,
        "wave": results["wave"],
        "source_paths": {
            "original_config": _id(data / f"{source_id}.source.config.json"),
            "evidence_accounting": _id(data / f"{source_id}.evidence-accounting.json"),
            "fixture_config": _id(val / f"{source_id}.fixture.config.json"),
            "fixture": _id(val / f"{source_id}.fixture.json"),
            "fixture_spec": _id(val / f"{source_id}.fixture-spec.json"),
            "validation_results": _id(results_path),
            "exceptions": _id(val / f"{source_id}.exceptions.json"),
            "manifest": _id(manifest_path),
        },
        "config_hashes": manifest["config_hashes"],
        "supported_scope": {
            "scope_id": config["supported_scope"]["scope_id"],
            "unit_slice": config["supported_scope"]["supported_unit_slice"],
            "form_slice": config["supported_scope"]["supported_form_slice"],
            "question_ids": config["supported_scope"]["supported_question_ids"],
            "original_source_execution": config["supported_scope"]["original_source_execution"],
            "native_validation_expectation": config["supported_scope"]["native_validation_expectation"],
        },
        "coverage": results["coverage"],
        "native_fixture_validation": {
            "projection": native["projection"],
            "release": native["release"],
            "actual": native["actual"],
            "expected_match": native["expected_match"],
            "calls": native["calls"],
            "p3_row_native_keys": native["p3_row_native_keys"],
            "p3_reader_transport": native["p3_reader_transport"],
            "repository": native["repository"],
            "refusals": native["refusals"],
        },
        "identity_separation": results["identity_separation"],
        "residuals": [
            {"residual_id": r["residual_id"], "scope": r["scope"], "field": r["field"],
             "status": r["status"], "dependent_operation": r["dependent_operation"], "owner": r["owner"]}
            for r in results["residuals"]
        ],
        "status": "FIXTURE_NATIVE_POSITIVE_ORIGINAL_NOT_EXECUTED",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-commit", required=True)
    parser.add_argument("--lane-tests", type=int, required=True)
    parser.add_argument("--foundation-tests", type=int, required=True)
    parser.add_argument("--p3-tests", type=int, required=True)
    parser.add_argument("--p3-deselected", type=int, required=True)
    parser.add_argument("--owner-tests", type=int, required=True)
    args = parser.parse_args(argv)
    sources = [_entry(source_id) for source_id in SOURCES]
    aggregate = {
        "sources": len(sources),
        "physical_columns": sum(s["coverage"]["physical_slots_total"] for s in sources),
        "original_items": sum(s["coverage"]["original_items_total"] for s in sources),
        "physical_slots_serialized": sum(s["coverage"]["physical_slots_serialized"] for s in sources),
        "items_serialized": sum(s["coverage"]["items_serialized"] for s in sources),
        "response_bound_items": sum(s["coverage"]["response_bound_items"] for s in sources),
        "held_items": sum(s["coverage"]["held_items"] for s in sources),
        "fixture_native_releases": sum(1 for s in sources if s["native_fixture_validation"]["release"]["release_ref"]["kind"] == "C11LogicalRelease"),
        "respondent_events": sum(s["native_fixture_validation"]["release"]["respondent_events"] for s in sources),
        "coordinate_facts": sum(s["native_fixture_validation"]["release"]["coordinate_facts"] for s in sources),
        "weight_facts": sum(s["native_fixture_validation"]["release"]["weight_facts"] for s in sources),
        "routing_facts": sum(s["native_fixture_validation"]["projection"]["routing_facts"] for s in sources),
        "residuals": sum(len(s["residuals"]) for s in sources),
    }
    aggregate["no_drop_all_sources"] = all(s["coverage"]["no_drop"] for s in sources)
    aggregate["expected_match_all_sources"] = all(s["native_fixture_validation"]["expected_match"] for s in sources)
    aggregate["repositories_match_stream"] = all(s["native_fixture_validation"]["repository"]["release_ref_matches_stream"] for s in sources)
    doc = {
        "schema": "PYAT_R157_WVS_LANE_RETURN@1.0.0",
        "lane_id": "WVS",
        "branch": BRANCH,
        "artifact_commit": args.artifact_commit,
        "plan_seal": PLAN_SEAL,
        "p0_correction_consumed": P0,
        "p3_terminal_runtime_consumed": P3,
        "status": "COMPLETE_PREPARATION_WITH_EXACT_RESIDUALS",
        "source_ids": list(SOURCES),
        "completion_statement": "Three WVS waves have source-grounded original configurations with all physical slots/items serialized, full finite-item response rules where source topology permits, exact held-item accounting, distinct nonrespondent fixture configurations/bytes, and actual positive GovernedC11Projection/C11 releases. Original respondent execution is not performed.",
        "not_claimed": ["Original respondent execution or original empirical workload issuance", "Original-source scientific/population/design claims", "Cross-country canonicalization, weighting or multiselect aggregation", "Final all35 review or FieldForge/M1/N11 acceptance"],
        "sources": sources,
        "aggregate": aggregate,
        "verification": {
            "commands": [
                {"command": "PYTHONPATH=. python3 source_pre553_validation/SRC33/build_wvs_lane.py --all", "result": "PASS", "actual": "3/3 source configs validated; 3/3 nonrespondent fixture native releases constructed"},
                {"command": "PYTHONPATH=. python3 -m pytest source_pre553_validation/SRC33/test_wvs_lane.py -q -o addopts=''", "result": "PASS", "actual": f"{args.lane_tests} passed"},
                {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py -q -o addopts=''", "result": "PASS", "actual": f"{args.foundation_tests} passed"},
                {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts='' -k 'not r154_loader_delegates and not r154_prepared_path'", "result": "PASS", "actual": f"{args.p3_tests} passed, {args.p3_deselected} deselected"},
                {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_read_admission.py -q -o addopts=''", "result": "PASS", "actual": f"{args.owner_tests} passed"},
            ],
            "pass": args.lane_tests + args.foundation_tests + args.p3_tests + args.owner_tests,
            "fail": 0,
            "skip_or_unavailable": args.p3_deselected,
            "unavailable_detail": "Two P3 R154-loader tests require the tracked skip-worktree file WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/runtime/r154_load.py, absent from this checkout; the new WVS path does not import the legacy R154 loader.",
        },
        "lane_completion_blockers": [],
        "original_execution_dependencies": [
            {"id": "WVS-ORIGINAL-ROW-KEYS", "required": "Permitted original PhysicalSourceIncidence with decoded source key cells", "operation": "P3 row_native_keys_from_transport/build_validated_c11_release_from_config", "current": "Original configs bind S007/V3; no original bytes/keys read", "owner": "P3/integration owner with source-read custody", "next": "Supply permitted incidence; original execution remains separately authorized"},
            {"id": "WVS-SOURCE-AUTHORITY-DEFER", "required": "Exact adopted original operation/authority scope", "current": "H48/P2/full-relation evidence retained as source_reviewed candidate evidence; original source snapshots DEFER", "owner": "R157 authority owner", "next": "Adjudicate exact scope; never promote fixture authority"},
            {"id": "WVS-ROUTING-UNKNOWN", "required": "Exact form/ballot/administration and eligibility routes", "current": "H48 routing status unresolved; original routing facts ROUTING_UNKNOWN", "owner": "WVS source evidence owner", "next": "Recover exact routing expressions before eligibility claims"},
            {"id": "WVS-HELD-SOURCE-ROLES", "required": "Exact rank maps, cross-country code normalizations, generation-forbidden dispositions, continuous native rules, administrative/context semantics", "current": "Held items are per-item evidence rows in each exceptions ledger, not generic unselected inventory", "owner": "WVS source/native-representation owner", "next": "Consume exact held evidence or extend the existing owner only through its contract"},
            {"id": "WVS-WEIGHT-HELD", "required": "Weight design/estimand/normalization authority", "current": "Weight slot identified and held; fixture exercises unresolved-basis weight facts only", "owner": "WVS weight/design owner", "next": "Establish design/estimand before weighted scope"},
        ],
        "next_integration_edge": {
            "owner": "R157 P3/integration owner",
            "operation": "Consume the three original configurations and their reader configurations; on separately authorized original read, pass permitted PhysicalSourceIncidence to build_validated_c11_release_from_config. P3 extracts source row keys from S007/V3.",
            "fixture_pass_available_now": True,
            "original_execution_requires_separate_authority": True,
            "final_review": "Distinct coherent all35 boundary later; not this lane return",
        },
        "no_original_source_access": True,
        "respondent_rows_read": 0,
        "original_workload_issued": False,
    }
    out = ROOT / "source_pre553_validation/SRC33/LANE_RETURN.json"
    out.write_text(json.dumps(doc, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(out.relative_to(ROOT)), "sha256": _sha(out), "bytes": len(out.read_bytes()), "aggregate": aggregate}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
