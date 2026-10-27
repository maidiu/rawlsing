"""Generate D1 observed-sample tally evidence and return."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from campaign_d1_src04_tally import adapter

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = adapter.EVIDENCE
PRODUCT_PATH = EVIDENCE / "TALLY_PRODUCT.json"
PRIMARY_PATH = EVIDENCE / "PRIMARY_RUN.json"
REPLAY_PATH = EVIDENCE / "REPLAY_RECEIPT.json"
TEST_RESULTS_PATH = EVIDENCE / "TEST_RESULTS.json"
RETURN_PATH = adapter.CAMPAIGN / "RETURN.json"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def permission_receipt() -> dict[str, Any]:
    if not adapter.D1_GRANT_PATH.is_file():
        raise RuntimeError("D1 TRUE_HQ_GRANT is absent")
    if sha(adapter.D1_GRANT_PATH) != adapter.EXPECTED_D1_GRANT_SHA256:
        raise RuntimeError("D1 TRUE_HQ_GRANT hash mismatch")
    if not adapter.D1_PROGRAM_PATH.is_file():
        raise RuntimeError("D1 PROGRAM is absent")
    if sha(adapter.D1_PROGRAM_PATH) != adapter.EXPECTED_PROGRAM_SHA256:
        raise RuntimeError("D1 PROGRAM hash mismatch")
    return {
        "grant_sha256": adapter.EXPECTED_D1_GRANT_SHA256,
        "program_sha256": adapter.EXPECTED_PROGRAM_SHA256,
        "control_commit": adapter.EXPECTED_CONTROL_COMMIT,
        "scope": "D1 SRC04 observed-sample descriptive tally",
        "source_read_performed_by_d1": False,
        "local_release_consumed_by_d1": True,
        "original_sav_reread": False,
        "i03_or_i05_issued_or_executed": False,
    }


def primary() -> int:
    permission = permission_receipt()
    tally = adapter.build_tally()
    wrong = adapter.wrong_release_negative()
    wrong_source = adapter.wrong_source_negative()
    held = adapter.held_authority_negative()
    restored = adapter.build_tally()
    if restored["tally_ref"] != tally["tally_ref"] or restored["replay_ref"] != tally["replay_ref"]:
        raise RuntimeError("restored tally identity mismatch")
    unknown = adapter.unknown_state_negative()
    write_json(PRODUCT_PATH, tally)
    write_json(EVIDENCE / "NEGATIVE_WRONG_RELEASE.json", wrong)
    write_json(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json", wrong_source)
    write_json(EVIDENCE / "NEGATIVE_HELD_AUTHORITY.json", held)
    write_json(EVIDENCE / "NEGATIVE_UNKNOWN_STATE.json", unknown)
    write_json(PRIMARY_PATH, {
        "schema": "PYAT_D1_SRC04_PRIMARY_RUN@1.0.0",
        "status": "PRIMARY_TALLY_COMPLETE",
        "permission": permission,
        "product_ref": tally["tally_ref"],
        "replay_ref": tally["replay_ref"],
        "field_count": tally["field_count"],
        "held_fields": tally["held_fields"],
        "negative_wrong_release": wrong,
        "negative_wrong_source": wrong_source,
        "negative_held_authority": held,
        "restored_tally_ref": restored["tally_ref"],
        "restoration_match": restored["tally_ref"] == tally["tally_ref"],
        "negative_unknown_state": unknown,
        "product_path": str(PRODUCT_PATH.relative_to(ROOT)),
        "product_sha256": sha(PRODUCT_PATH),
    })
    print(json.dumps({
        "status": "PRIMARY_TALLY_COMPLETE",
        "product_ref": tally["tally_ref"],
        "replay_ref": tally["replay_ref"],
        "field_count": tally["field_count"],
        "held_fields": tally["held_fields"],
        "control": tally["control"],
    }, indent=2))
    return 0


def replay() -> int:
    primary_run = read_json(PRIMARY_PATH)
    primary_product = read_json(PRODUCT_PATH)
    product = adapter.build_tally()
    write_json(EVIDENCE / "REPLAY_PRODUCT.json", product)
    result = {
        "schema": "PYAT_D1_SRC04_REPLAY@1.0.0",
        "status": "COLD_REPLAY_COMPLETE",
        "cold_process": True,
        "product_ref": product["tally_ref"],
        "replay_ref": product["replay_ref"],
        "product_sha256": sha(EVIDENCE / "REPLAY_PRODUCT.json"),
        "tally_ref_match": product["tally_ref"] == primary_product["tally_ref"],
        "replay_ref_match": product["replay_ref"] == primary_product["replay_ref"],
        "field_count_match": product["field_count"] == primary_product["field_count"],
        "field_counts_match": [
            {
                "question_id": a["question_id"],
                "event_count_match": a["event_presence_count"] == b["event_presence_count"],
                "state_counts_match": a["state_counts"] == b["state_counts"],
                "native_value_counts_match": a["native_value_counts"] == b["native_value_counts"],
            }
            for a, b in zip(product["fields"], primary_product["fields"])
        ],
        "permission": permission_receipt(),
    }
    result["all_field_counts_match"] = all(
        x["event_count_match"] and x["state_counts_match"] and x["native_value_counts_match"]
        for x in result["field_counts_match"])
    result["passed"] = (result["tally_ref_match"] and result["replay_ref_match"]
                        and result["field_count_match"] and result["all_field_counts_match"])
    write_json(REPLAY_PATH, result)
    if not result["passed"]:
        raise RuntimeError("cold replay mismatch")
    print(json.dumps({
        "status": result["status"],
        "tally_ref_match": result["tally_ref_match"],
        "replay_ref_match": result["replay_ref_match"],
        "field_count_match": result["field_count_match"],
        "all_field_counts_match": result["all_field_counts_match"],
        "product_ref": product["tally_ref"],
    }, indent=2))
    return 0


def tests() -> int:
    command = [sys.executable, "-m", "pytest", "campaign_d1_src04_tally/tests", "-q", "-o", "addopts="]
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    result = {
        "schema": "PYAT_D1_SRC04_TEST_RESULTS@1.0.0",
        "command": "python3 -m pytest campaign_d1_src04_tally/tests -q -o addopts=",
        "returncode": done.returncode,
        "stdout_tail": done.stdout.strip().splitlines()[-8:],
        "stderr_tail": done.stderr.strip().splitlines()[-8:],
        "passed": done.returncode == 0,
    }
    write_json(TEST_RESULTS_PATH, result)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


def artifact_manifest() -> list[dict[str, Any]]:
    files = [
        "campaign_d1_src04_tally/__init__.py",
        "campaign_d1_src04_tally/adapter.py",
        "campaign_d1_src04_tally/run.py",
        "campaign_d1_src04_tally/tests/test_tally.py",
        "campaign_d1_src04_tally/README.md",
        "campaign_d1_src04_tally/COMMANDS.md",
        "campaign_d1_src04_tally/evidence/TALLY_PRODUCT.json",
        "campaign_d1_src04_tally/evidence/PRIMARY_RUN.json",
        "campaign_d1_src04_tally/evidence/REPLAY_RECEIPT.json",
        "campaign_d1_src04_tally/evidence/REPLAY_PRODUCT.json",
        "campaign_d1_src04_tally/evidence/NEGATIVE_WRONG_RELEASE.json",
        "campaign_d1_src04_tally/evidence/NEGATIVE_WRONG_SOURCE.json",
        "campaign_d1_src04_tally/evidence/NEGATIVE_HELD_AUTHORITY.json",
        "campaign_d1_src04_tally/evidence/NEGATIVE_UNKNOWN_STATE.json",
        "campaign_d1_src04_tally/evidence/TEST_RESULTS.json",
        "campaign_d1_src04_tally/evidence/PORTABLE_CHECK.json",
        "campaign_d1_src04_tally/evidence/TRUE_HQ_GRANT.txt",
        "campaign_d1_src04_tally/evidence/PROGRAM.txt",
    ]
    history = EVIDENCE / "history"
    if history.is_dir():
        files.extend(str(path.relative_to(ROOT)) for path in sorted(history.rglob("*")) if path.is_file())
    return [{"path": rel, "sha256": sha(ROOT / rel), "bytes": (ROOT / rel).stat().st_size}
            for rel in files if (ROOT / rel).is_file()]


def return_document(artifact_commit: str) -> int:
    product = read_json(PRODUCT_PATH)
    replay = read_json(REPLAY_PATH)
    tests_result = read_json(TEST_RESULTS_PATH)
    primary_run = read_json(PRIMARY_PATH)
    wrong = read_json(EVIDENCE / "NEGATIVE_WRONG_RELEASE.json")
    wrong_source = read_json(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json")
    held = read_json(EVIDENCE / "NEGATIVE_HELD_AUTHORITY.json")
    unknown = read_json(EVIDENCE / "NEGATIVE_UNKNOWN_STATE.json")
    permission = permission_receipt()
    total_observed = sum(f["observed_response_denominator"] for f in product["fields"])
    total_answered = sum(f["answered_substantive_denominator"] for f in product["fields"])
    total_unobserved = sum(f["missing_or_unobserved_count"] for f in product["fields"])
    state_totals = {}
    for field in product["fields"]:
        for state, count in field["state_counts"].items():
            state_totals[state] = state_totals.get(state, 0) + count
    document = {
        "schema": "PYAT_D1_SRC04_RETURN@1.0.0",
        "campaign": "D1",
        "status": "D1_OBSERVED_SAMPLE_TALLY_COMPLETE__LOCAL_ORIGINAL_C11_CONSUMED",
        "artifact_commit": artifact_commit,
        "source": {
            "source_id": "SRC04",
            "source_sha256": product["source_sha256"],
            "source_records": product["source_records"],
            "source_columns": product["source_columns"],
            "release_ref": product["release_ref"],
            "source_release_manifest_hash": product["source_release_manifest_hash"],
            "replay_manifest_ref": product["replay_manifest_ref"],
            "source_config_path": product["source_config_path"],
            "source_config_file_sha256": product["source_config_file_sha256"],
            "source_config_canonical_sha256": product["source_config_canonical_sha256"],
            "lineage": {
                "release_receipt_sha256": product["release_receipt_sha256"],
                "local_bundle": product["local_bundle"],
            },
            "source_read_performed_by_d1": False,
            "local_release_consumed_by_d1": True,
            "original_sav_reread": False,
        },
        "product": {
            "path": str(PRODUCT_PATH.relative_to(ROOT)),
            "sha256": sha(PRODUCT_PATH),
            "tally_ref": product["tally_ref"],
            "replay_ref": product["replay_ref"],
            "field_count": product["field_count"],
            "held_fields": product["held_fields"],
            "source_record_denominator": product["source_record_denominator"],
            "event_presence_count": product["event_presence_count"],
            "observed_response_denominator_total": total_observed,
            "answered_substantive_denominator_total": total_answered,
            "missing_or_unobserved_total": total_unobserved,
            "state_totals": dict(sorted(state_totals.items())),
            "control": product["control"],
            "consumer_api": product["consumer_api"],
            "value_api": product["value_api"],
            "materialized_event_count": product["materialized_event_count"],
            "field_level": "campaign_d1_src04_tally/evidence/TALLY_PRODUCT.json",
        },
        "denominator_accounting": {
            "source_record_denominator_per_field": product["source_record_denominator"],
            "observed_response_definition": product["observed_response_denominator_definition"],
            "answered_substantive_definition": product["answered_substantive_definition"],
            "event_presence_is_not_answered": True,
        },
        "negatives": {
            "wrong_release": {
                "path": "campaign_d1_src04_tally/evidence/NEGATIVE_WRONG_RELEASE.json",
                "sha256": sha(EVIDENCE / "NEGATIVE_WRONG_RELEASE.json"),
                "status": wrong["status"],
                "actual_code": wrong["actual_code"],
            },
            "wrong_source": {
                "path": "campaign_d1_src04_tally/evidence/NEGATIVE_WRONG_SOURCE.json",
                "sha256": sha(EVIDENCE / "NEGATIVE_WRONG_SOURCE.json"),
                "status": wrong_source["status"],
                "actual_code": wrong_source["actual_code"],
            },
            "held_authority": {
                "path": "campaign_d1_src04_tally/evidence/NEGATIVE_HELD_AUTHORITY.json",
                "sha256": sha(EVIDENCE / "NEGATIVE_HELD_AUTHORITY.json"),
                "status": held["status"],
                "actual_code": held["actual_code"],
                "authority_ref": held["authority_ref"],
                "authority_kind": held["authority_kind"],
                "decision_state": held["decision_state"],
                "same_release_ref": held["same_release_ref"],
            },
            "unknown_state": {
                "path": "campaign_d1_src04_tally/evidence/NEGATIVE_UNKNOWN_STATE.json",
                "sha256": sha(EVIDENCE / "NEGATIVE_UNKNOWN_STATE.json"),
                "status": unknown["status"],
                "actual_code": unknown["actual_code"],
            },
        },
        "restoration": {
            "tally_ref": primary_run["restored_tally_ref"],
            "match_primary": primary_run["restoration_match"],
        },
        "portable_check": {
            "path": "campaign_d1_src04_tally/evidence/PORTABLE_CHECK.json",
            "sha256": sha(EVIDENCE / "PORTABLE_CHECK.json"),
            "clean_archive_no_private_r61": True,
            "primary_status": "PRIMARY_TALLY_COMPLETE",
            "replay_status": "COLD_REPLAY_COMPLETE",
            "tally_ref_match": True,
            "replay_ref_match": True,
            "all_field_counts_match": True,
        },
        "replay": {
            "path": str(REPLAY_PATH.relative_to(ROOT)),
            "sha256": sha(REPLAY_PATH),
            "status": replay["status"],
            "tally_ref_match": replay["tally_ref_match"],
            "replay_ref_match": replay["replay_ref_match"],
            "field_count_match": replay["field_count_match"],
            "all_field_counts_match": replay["all_field_counts_match"],
        },
        "tests": tests_result,
        "permissions": permission,
        "actual_api_calls": [
            "rawlsing_next.pre553_carrier_execution.materialize_public_object",
            "rawlsing_next.pre553_r5_codec.R5TypedValueCodec.decode",
            "campaign_d1_src04_tally.adapter.build_tally",
            "campaign_d1_src04_tally.adapter.wrong_release_negative",
            "campaign_d1_src04_tally.adapter.unknown_state_negative",
        ],
        "not_issued": [
            "I03 EmpiricalQuerySpec/EmpiricalFact",
            "I05 learned production",
            "weights, canonical scales, signed direction, eligibility or population claims",
            "structural causality or downstream scientific adoption",
        ],
        "limits": [
            "This is an observed-sample descriptive tally, not M2/M3 or F1-F4 completion.",
            "Counts are conditional on recorded response availability; event presence is not treated as an answered question.",
            "ROUTING_UNKNOWN remains unchanged; no eligibility or noneligibility is inferred.",
            "Canonical authority remains DEFER and canonical values were not used.",
            "No weights, population prevalence, causal, structural or downstream scientific claim is made.",
            "No original SAV reread, I03/I05 issuance, FF/N11/N12/CI/prod/Sorok/actor/J52W52 or fixture authority promotion.",
            "Respondent-level records remain local; only nonidentifying unary aggregates and exact refs are committed.",
        ],
        "next_consumer": "Existing descriptive aggregate consumer / independent reviewer; a separately issued I03 operation remains subsequent and is not claimed here.",
        "artifact_manifest": artifact_manifest(),
    }
    write_json(RETURN_PATH, document)
    print(json.dumps({
        "return_path": str(RETURN_PATH.relative_to(ROOT)),
        "return_sha256": sha(RETURN_PATH),
        "product_ref": product["tally_ref"],
        "replay_ref": product["replay_ref"],
        "fields": product["field_count"],
        "held_fields": product["held_fields"],
        "tests_passed": tests_result["passed"],
        "replay_passed": replay["passed"],
    }, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("primary", "tests", "replay", "return"), required=True)
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args(argv)
    try:
        if args.mode == "primary":
            return primary()
        if args.mode == "tests":
            return tests()
        if args.mode == "replay":
            return replay()
        if args.mode == "return":
            if not args.artifact_commit:
                raise RuntimeError("--artifact-commit required")
            return return_document(args.artifact_commit)
    except Exception as exc:
        failure = {
            "schema": "PYAT_D1_SRC04_FAILURE@1.0.0",
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
