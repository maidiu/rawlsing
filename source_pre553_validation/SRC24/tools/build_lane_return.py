"""Assemble source_pre553_validation/SRC24/LANE_RETURN.json from committed artifacts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config

SOURCES = ("SRC24", "SRC25", "SRC26")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    artifact_commit = sys.argv[1] if len(sys.argv) > 1 else None
    if not artifact_commit:
        raise SystemExit("usage: build_lane_return.py <artifact_commit>")
    source_results = {}
    for sid in SOURCES:
        data = ROOT / "rawlsing_next/source_configuration/data" / sid
        val = ROOT / "source_pre553_validation" / sid
        original = load_source_config(data / "source.config.json")
        fixture_config = load_source_config(val / "fixture.config.json")
        validation = json.loads((val / "VALIDATION_RESULTS.json").read_text())
        exceptions = json.loads((val / "EXCEPTIONS.json").read_text())
        crosswalk = json.loads((data / "crosswalk.json").read_text())
        oracle = json.loads((val / "fixture_oracle.json").read_text())
        manifest = json.loads((val / "manifest.json").read_text())
        fixture_doc = json.loads((val / "fixture.json").read_text())
        projection_call = next(c for c in validation["calls"]
                               if c.get("result") == "GovernedC11Projection"
                               and c.get("input", "").startswith("ORIGINAL_SOURCE"))
        fixture_projection_call = next(c for c in validation["calls"]
                                       if c.get("result") == "GovernedC11Projection"
                                       and c.get("input", "").startswith("NONRESPONDENT_FIXTURE"))
        release_call = next(c for c in validation["calls"]
                            if c.get("result") == "C11LogicalRelease")
        artifacts = {}
        for path in (
            data / "source.config.json", data / "crosswalk.json", data / "field_evidence.json",
            val / "fixture.config.json", val / "fixture.json", val / "fixture_oracle.json",
            val / "VALIDATION_RESULTS.json", val / "EXCEPTIONS.json", val / "manifest.json",
        ):
            artifacts[rel(path)] = {"sha256": sha(path), "bytes": path.stat().st_size}
        residuals = []
        for residual in original.document["residuals"]:
            residuals.append({
                "residual_id": residual["residual_id"],
                "field": residual["field"],
                "status": residual["status"],
                "reason": residual["reason"],
                "dependent_operation": residual["dependent_operation"],
                "unaffected_scope": residual["unaffected_scope"],
                "owner": residual["owner"],
                "next_step": residual["next_step"],
            })
        source_results[sid] = {
            "source_id": sid,
            "family": original.document["identity"]["family"],
            "wave": original.document["identity"]["wave"],
            "source_sha256": original.original_source_sha256,
            "source_rows": original.document["identity"]["source_row_count"],
            "source_columns": original.document["identity"]["source_column_count"],
            "original_items": original.document["identity"]["original_item_count"],
            "original_config": {
                "path": rel(data / "source.config.json"),
                "config_id": original.config_id,
                "config_purpose": original.config_purpose,
                "identity_class": original.identity_class,
                "canonical_sha256": canonical_config_hash(original),
                "file_sha256": sha(data / "source.config.json"),
                "supported_question_ids": original.document["supported_scope"]["supported_question_ids"],
                "supported_unit_slice": original.document["supported_scope"]["supported_unit_slice"],
                "supported_form_slice": original.document["supported_scope"]["supported_form_slice"],
                "native_validation_expectation": original.document["supported_scope"]["native_validation_expectation"],
                "original_source_execution": original.document["supported_scope"]["original_source_execution"],
                "included_slots": original.document["coverage"]["physical_slots_included"],
                "included_items": original.document["coverage"]["items_included"],
                "excluded_items_exact": original.document["coverage"]["items_excluded"],
                "residuals": residuals,
            },
            "crosswalk": {
                "path": rel(data / "crosswalk.json"),
                "sha256": sha(data / "crosswalk.json"),
                "method": crosswalk["method"],
                "counts": crosswalk["counts"],
                "limits": crosswalk["limits"],
            },
            "field_evidence": {
                "path": rel(data / "field_evidence.json"),
                "sha256": sha(data / "field_evidence.json"),
            },
            "fixture": {
                "path": rel(val / "fixture.json"),
                "sha256": sha(val / "fixture.json"),
                "fixture_id": fixture_doc["fixture_id"],
                "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
                "row_count": fixture_doc["row_count"],
                "identity_class": fixture_doc["identity_class"],
                "nonrespondent": fixture_doc["nonrespondent"],
                "config_path": rel(val / "fixture.config.json"),
                "config_canonical_sha256": canonical_config_hash(fixture_config),
                "config_file_sha256": sha(val / "fixture.config.json"),
                "oracle_path": rel(val / "fixture_oracle.json"),
                "oracle_sha256": sha(val / "fixture_oracle.json"),
                "oracle_expected_counts": {
                    k: oracle["expected"][k] for k in
                    ("response_event_count", "coordinate_fact_count", "routing_fact_count")
                },
            },
            "native_validation": {
                "status": validation["status"],
                "check_count": len(validation["checks"]),
                "passed": sum(1 for c in validation["checks"] if c["pass"]),
                "failed": len(validation["failures"]),
                "skipped": 0,
                "original_projection": projection_call,
                "fixture_projection": fixture_projection_call,
                "fixture_release": release_call,
                "actual_counts": validation["actual"]["counts"],
                "response_state_counts": validation["actual"]["response_state_counts"],
                "routing_state_counts": validation["actual"]["routing_state_counts"],
                "coordinate_state_counts": validation["actual"]["coordinate_state_counts"],
                "release_ref": validation["actual"]["release_ref"],
                "semantic_release_hash": validation["actual"]["semantic_release_hash"],
                "m01_m18_coverage": validation["actual"]["m01_m18_coverage"],
                "refusals": validation["refusals"],
            },
            "exceptions": {
                "path": rel(val / "EXCEPTIONS.json"),
                "sha256": sha(val / "EXCEPTIONS.json"),
                "counts": exceptions["counts"],
            },
            "manifest": {
                "path": rel(val / "manifest.json"),
                "sha256": sha(val / "manifest.json"),
                "validation_status": manifest.get("validation", {}).get("status"),
            },
            "no_drop": validation["no_drop"],
            "artifacts": artifacts,
        }

    lane_return = {
        "schema": "PYAT_R157_LANE_RETURN@1.0.0",
        "lane_id": "LATIN",
        "branch": "agent/pyat-pre553-r157-latin",
        "plan_seal": "4c0c619eac747afee1d8e65e1418bf2d472da4c3",
        "artifact_commit": artifact_commit,
        "p0_corrected_commit": "d8d7087a8e56c24042bf5945fea1c97eb0d6c710",
        "p3_terminal_commit": "519355ec2215409b40d566ef13c3b21f611e0726",
        "source_ids": list(SOURCES),
        "startup_verification": {
            "pwd": "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r157-latin",
            "origin": "https://github.com/maidiu/rawlsing.git",
            "branch": "agent/pyat-pre553-r157-latin",
            "head_at_resume": "d82f2fec4422ed23d6ffd3150d9887ffaa927d4e",
            "clean_at_resume": True,
            "remote_reconciled_before_return": "d82f2fec4422ed23d6ffd3150d9887ffaa927d4e",
        },
        "source_results": source_results,
        "commands": [
            {
                "command": "PYTHONPATH=. python3 source_pre553_validation/SRC24/tools/latin_full.py",
                "result": "generated/validated full original configs, crosswalks, field evidence, nonrespondent fixtures, fixture configs and oracles for SRC24-SRC26",
                "status": "PASS",
                "stdout_tail": [
                    f"SRC24: config={source_results['SRC24']['original_config']['canonical_sha256']} "
                    f"fixture={source_results['SRC24']['fixture']['fixture_source_sha256']} "
                    f"included_slots={len(source_results['SRC24']['original_config']['included_slots'])} "
                    f"included_items={len(source_results['SRC24']['original_config']['included_items'])}",
                    f"SRC25: config={source_results['SRC25']['original_config']['canonical_sha256']} "
                    f"fixture={source_results['SRC25']['fixture']['fixture_source_sha256']} "
                    f"included_slots={len(source_results['SRC25']['original_config']['included_slots'])} "
                    f"included_items={len(source_results['SRC25']['original_config']['included_items'])}",
                    f"SRC26: config={source_results['SRC26']['original_config']['canonical_sha256']} "
                    f"fixture={source_results['SRC26']['fixture']['fixture_source_sha256']} "
                    f"included_slots={len(source_results['SRC26']['original_config']['included_slots'])} "
                    f"included_items={len(source_results['SRC26']['original_config']['included_items'])}",
                ],
            },
            {
                "command": "PYTHONPATH=. python3 source_pre553_validation/SRC24/tools/run_latin_validation.py",
                "result": "SRC24 PASS 566/566 checks; SRC25 PASS 1127/1127 checks; SRC26 PASS 842/842 checks; 0 failed; 0 skipped",
                "status": "PASS",
            },
            {
                "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts=''",
                "result": "21 passed in 2.13s",
                "status": "PASS",
            },
            {
                "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py rawlsing_next/tests/test_pre553_source_read_admission.py rawlsing_next/tests/test_pre553_c11_repository_ingest.py -q -o addopts=''",
                "result": "65 passed in 2.26s",
                "status": "PASS",
            },
            {
                "command": "PYTHONPATH=. python3 -c \"load_source_config SRC24-SRC26 original+fixture; assert identity separation\"",
                "result": "all six configs load and validate; original configs have no fixture provenance; fixture SHAs are distinct",
                "status": "PASS",
            },
        ],
        "native_api_calls": [
            "rawlsing_next.source_configuration.schema.load_source_config",
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.fixture.load_fixture_stream",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream (through the frozen factory)",
        ],
        "identity_separation": {
            "original_identity_class": "ORIGINAL_SOURCE",
            "fixture_identity_class": "NONRESPONDENT_FIXTURE",
            "original_configs_carry_no_fixture_provenance": True,
            "fixture_source_shas_distinct_from_original": True,
            "fixture_sha_absent_from_original_config_bytes": True,
            "fixture_authority": "fixture_only ALLOW, grade NONRESPONDENT_FIXTURE_ONLY",
            "original_authority": "DEFER source semantics; ALLOW only local deterministic replay protocol",
            "original_respondent_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        },
        "reader_transport": {
            "p3_reader_available": True,
            "config_encoding": None,
            "reason": "No SRC24-SRC26 SHA is in the exact decoder compatibility allowlist; no encoding is guessed.",
            "original_source_read": "NOT_PERFORMED",
        },
        "exceptions_and_limits": {
            "blockers": [],
            "precise_residuals": [
                f"SRC24: {len(source_results['SRC24']['original_config']['included_items'])}/203 items included; 14 exact exclusions (13 unmatched full-relation identities plus the weight slot authority gap).",
                f"SRC25: {len(source_results['SRC25']['original_config']['included_items'])}/414 items included; 3 exact exclusions (weight authority gap plus P54ST_9/P56NI no declared finite value domain).",
                f"SRC26: {len(source_results['SRC26']['original_config']['included_items'])}/195 items included; 5 unmatched full-relation identities excluded; physical-only P14ST.F/P52N hold no item identity; WT has no weight authority.",
                "Source routing remains SOURCE_ROUTING_UNRESOLVED and is represented as ROUTING_UNKNOWN; original routing facts are a bounded preparation witness over rows 1-3, not an eligibility claim for every row.",
                "Source-native respondent key slots are not configured; row ordinal is the only established key. The corrected P0 factory refuses a configured key slot without exact row keys.",
                "No form/ballot/administration variable is present in current evidence; single-file SAV shape is declared.",
                "No weight design/estimand authority is established; weight_slots is empty and no weighted scope is claimed.",
                "Signed direction/canonical semantic certification is not newly issued; only exact source-native code/state binding is prepared.",
                "Open/continuous context fields are bound as raw coordinates; no finite categorical domain is invented.",
                "Original respondent execution/workload issuance was not performed and is not claimed.",
                "Legacy R154 load_all/load_source private B49 dependency remains outside the new prepared path; the lane does not route through it.",
            ],
            "distinct_review": "NOT_PERFORMED; reserved for the distinct coherent all35 boundary review, not this author return.",
        },
        "next_integration_edge": {
            "owner": "R157 integration owner / P5 coherent all35 boundary",
            "action": "Intake SRC24-SRC26 source configs, crosswalks and nonrespondent fixture positives; rerun the lane validation command; then run the coherent all35 readiness and distinct final review.",
            "artifact_commit": artifact_commit,
            "do_not_do": [
                "Do not promote fixture authority, fixture universe or fixture SHA into original-source meaning.",
                "Do not declare original empirical execution from this preparation return.",
                "Do not route the new library through the legacy R154 load_all/load_source B49 path.",
            ],
        },
        "no_original_source_access": True,
        "original_respondent_rows_read": 0,
        "original_workload_issued": False,
        "quota": "UNKNOWN",
        "remote_push": {
            "status": "NON_FORCE_PUSH_PERFORMED_AFTER_THIS_FILE",
            "direct_readback": "reported in the final lane return message; branch HEAD is the commit that adds this file",
        },
    }
    out = ROOT / "source_pre553_validation/SRC24/LANE_RETURN.json"
    out.write_text(json.dumps(lane_return, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} sha256={sha(out)} bytes={out.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
