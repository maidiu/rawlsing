"""Generate the bounded B0 consumer-preparation evidence and return."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from campaign_b0_src04 import adapter

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = adapter.EVIDENCE
RETURN_PATH = adapter.CAMPAIGN / "RETURN.json"
TEST_RESULTS_PATH = EVIDENCE / "TEST_RESULTS.json"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_tests() -> dict[str, Any]:
    command = [sys.executable, "-m", "pytest", "campaign_b0_src04/tests", "-q", "-o", "addopts="]
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    result = {
        "schema": "PYAT_CAMPAIGN_B0_SRC04_TEST_RESULTS@1.0.0",
        "command": "python3 -m pytest campaign_b0_src04/tests -q -o addopts=",
        "returncode": done.returncode,
        "stdout_tail": done.stdout.strip().splitlines()[-8:],
        "stderr_tail": done.stderr.strip().splitlines()[-8:],
        "passed": done.returncode == 0,
    }
    write_json(TEST_RESULTS_PATH, result)
    if not result["passed"]:
        raise RuntimeError(f"B0 focused tests failed: {result}")
    return result


def manifest() -> list[dict[str, Any]]:
    files = [
        "campaign_b0_src04/__init__.py",
        "campaign_b0_src04/adapter.py",
        "campaign_b0_src04/run.py",
        "campaign_b0_src04/tests/test_adapter.py",
        "campaign_b0_src04/README.md",
        "campaign_b0_src04/COMMANDS.md",
        "campaign_b0_src04/evidence/REQUEST_SET.json",
        "campaign_b0_src04/evidence/AUTHORITY_DEPENDENCIES.json",
        "campaign_b0_src04/evidence/FIXTURE_POSITIVE.json",
        "campaign_b0_src04/evidence/NEGATIVE_RELEASE_MISMATCH.json",
        "campaign_b0_src04/evidence/NEGATIVE_FIXTURE_TARGET.json",
        "campaign_b0_src04/evidence/TEST_RESULTS.json",
    ]
    out = []
    for rel in files:
        path = ROOT / rel
        if path.is_file():
            out.append({"path": rel, "sha256": sha(path), "bytes": path.stat().st_size})
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", required=True)
    args = parser.parse_args(argv)
    plan = adapter.prepare_original_request_plan()
    fixture = adapter.build_fixture_positive()
    fixture_mismatch = adapter.fixture_target_mismatch()
    release_mismatch = adapter.original_release_mismatch_negative()
    tests = run_tests()

    write_json(EVIDENCE / "REQUEST_SET.json", plan)
    write_json(EVIDENCE / "AUTHORITY_DEPENDENCIES.json", {
        "schema": "PYAT_CAMPAIGN_B0_SRC04_AUTHORITY_DEPENDENCIES@1.0.0",
        "source_id": adapter.SOURCE_ID,
        "source_release_ref": plan["source_release_ref"],
        "request_set_sha256": plan["request_set_sha256"],
        "authority_requirements": plan["authority_requirements"],
        "missing_authority": plan["missing_authority"],
        "minimal_remaining_authority": plan["minimal_remaining_authority"],
        "next_invocation": plan["next_invocation"],
        "canonicalization": plan["canonicalization"],
    })
    write_json(EVIDENCE / "FIXTURE_POSITIVE.json", fixture)
    write_json(EVIDENCE / "NEGATIVE_RELEASE_MISMATCH.json", release_mismatch)
    write_json(EVIDENCE / "NEGATIVE_FIXTURE_TARGET.json", fixture_mismatch)

    request_set_path = EVIDENCE / "REQUEST_SET.json"
    authority_path = EVIDENCE / "AUTHORITY_DEPENDENCIES.json"
    fixture_path = EVIDENCE / "FIXTURE_POSITIVE.json"
    release_mismatch_path = EVIDENCE / "NEGATIVE_RELEASE_MISMATCH.json"
    fixture_mismatch_path = EVIDENCE / "NEGATIVE_FIXTURE_TARGET.json"
    return_document = {
        "schema": "PYAT_CAMPAIGN_B0_SRC04_RETURN@1.0.0",
        "campaign": "B0",
        "status": "CONSUMER_PREPARATION_READY__BLOCKED_MISSING_EXACT_AUTHORITY__FIXTURE_CONSTRUCTION_POSITIVE",
        "artifact_commit": args.artifact_commit,
        "milestone_claimed": "NONE_SELF_CLAIMED",
        "source_scope": {
            "source_id": adapter.SOURCE_ID,
            "source_sha256": adapter.EXPECTED_SOURCE_SHA256,
            "source_release_ref": plan["source_release_ref"],
            "source_release_manifest_hash": plan["source_release_manifest_hash"],
            "source_config_path": plan["source_config_path"],
            "source_config_file_sha256": plan["source_config_file_sha256"],
            "source_config_canonical_sha256": plan["source_config_canonical_sha256"],
            "source_read_performed_by_a1": plan["source_read_performed_by_a1"],
            "source_read_performed_by_b0": False,
            "local_original_release_read_by_b0": False,
            "accepted_response_slots": plan["accepted_response_slots"],
            "accepted_question_ids": plan["accepted_question_ids"],
            "accepted_coordinate_slots": plan["accepted_coordinate_slots"],
        },
        "request_preparation": {
            "status": plan["status"],
            "request_count": plan["request_count"],
            "request_set_path": str(request_set_path.relative_to(ROOT)),
            "request_set_sha256": sha(request_set_path),
            "request_set_canonical_sha256": plan["request_set_sha256"],
            "query_constructed": False,
            "empirical_query_spec_ref": None,
            "runtime_catalog_identity": None,
            "historical_parent_snapshot_ref": None,
            "authority_dependencies_path": str(authority_path.relative_to(ROOT)),
            "authority_dependencies_sha256": sha(authority_path),
            "canonicalization": plan["canonicalization"],
            "canonical_response_values": 0,
            "canonical_question_values": 0,
            "weight_slots": 0,
        },
        "fixture_positive": {
            "scope": fixture["scope"],
            "path": str(fixture_path.relative_to(ROOT)),
            "sha256": sha(fixture_path),
            "fixture_source_sha256": fixture["fixture_source_sha256"],
            "fixture_release_ref": fixture["fixture_release_ref"],
            "catalog_identity": fixture["catalog_identity"],
            "query_ref": fixture["query_ref"],
            "predicate_ref": fixture["predicate_ref"],
            "test_only_query_authority_used": fixture["test_only_query_authority_used"],
            "execution": fixture["execution"],
            "construction_positive": True,
            "product_positive": False,
            "original_source_or_release_read": False,
        },
        "negatives": {
            "release_identity_mismatch": {
                "path": str(release_mismatch_path.relative_to(ROOT)),
                "sha256": sha(release_mismatch_path),
                "status": release_mismatch["status"],
                "actual_code": release_mismatch["actual_code"],
            },
            "fixture_target_mismatch": {
                "path": str(fixture_mismatch_path.relative_to(ROOT)),
                "sha256": sha(fixture_mismatch_path),
                "status": fixture_mismatch["status"],
                "actual_code": fixture_mismatch["actual_code"],
            },
            "missing_authority_is_not_a_query": {
                "status": plan["status"],
                "query_constructed": False,
                "roles": [x["role"] for x in plan["missing_authority"]],
            },
        },
        "minimal_remaining_authority": plan["minimal_remaining_authority"],
        "next_consuming_edge": plan["next_invocation"],
        "actual_apis": [
            {
                "api": "rawlsing_next.source_configuration.schema.load_source_config",
                "result": "SRC04 source configuration validated",
            },
            {
                "api": "campaign_b0_src04.adapter.prepare_original_request_plan",
                "result": "42 exact request identities; query intentionally not constructed because authority/catalog/historical parent are absent",
            },
            {
                "api": "rawlsing_next.pre553_native_workload_binding.build_projection_catalog",
                "result": "fixture-only EmpiricalQuerySpec and RuntimeObjectCatalog constructed",
                "fixture_only": True,
                "query_ref": fixture["query_ref"],
                "catalog_identity": fixture["catalog_identity"],
            },
            {
                "api": "rawlsing_next.pre553_empirical_query.execute_empirical_query",
                "result": fixture["execution"],
                "fixture_only": True,
                "original_execution": False,
            },
        ],
        "tests": tests,
        "artifact_manifest": manifest(),
        "fixture_vs_original_scope": {
            "fixture": "SRC04 nonrespondent fixture used only to construct/execute the existing catalog/query seam",
            "original": "SRC04 committed C11 metadata/receipt only; no original SAV or local original release read; no original query issued",
            "fixture_authority_not_reused_for_original": True,
        },
        "limits": [
            "B0 is consumer preparation, not B completion, M1/M2, I03/I05 execution, or final acceptance.",
            "The original request remains blocked until an exact competent issuer supplies the adopted source-native unary-distribution operation/authority, target use if needed, runtime catalog, historical parent, and routing/risk-set decision.",
            "No new semantic predicate, eligibility rule, canonical/directional mapping, estimand, weight, or population claim is invented.",
            "The permitted SRC04 fixture only demonstrates existing catalog/query construction; its test-only authority is not an original authority.",
            "No original SAV, original local release, respondent cells, or row-wise artifacts were read or committed.",
            "No FF/M1/N11/N12/actor/CI/prod/Sorok/J52W52 or other source-family action.",
        ],
        "next_consumer": "Existing I03 owner after exact authority/catalog/historical-parent issuance; I05 remains downstream and separately authorized.",
    }
    write_json(RETURN_PATH, return_document)
    print(json.dumps({
        "return_path": str(RETURN_PATH.relative_to(ROOT)),
        "return_sha256": sha(RETURN_PATH),
        "artifact_commit": args.artifact_commit,
        "release_ref": plan["source_release_ref"],
        "request_count": plan["request_count"],
        "fixture_query_ref": fixture["query_ref"],
        "fixture_execution": fixture["execution"],
        "tests_passed": tests["passed"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
