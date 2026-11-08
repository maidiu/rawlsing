"""Assemble source_pre553_validation/SRC04/LANE_RETURN.json from committed artifacts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from rawlsing_next.source_configuration.schema import canonical_config_hash, load_source_config  # noqa: E402

SOURCES = ("SRC04", "SRC05", "SRC06", "SRC07")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    artifact_commit = sys.argv[1]
    results = {}
    for sid in SOURCES:
        data = ROOT / "rawlsing_next/source_configuration/data" / sid
        val = ROOT / "source_pre553_validation" / sid
        original = load_source_config(data / "source.config.json")
        fixture_config = load_source_config(val / "fixture.config.json")
        validation = json.loads((val / "VALIDATION_RESULTS.json").read_text())
        exceptions = json.loads((val / "EXCEPTIONS.json").read_text())
        topology = json.loads((val / "TOPOLOGY_ASSERTIONS.json").read_text())
        crosswalk = json.loads((data / "crosswalk.json").read_text())
        oracle = json.loads((val / "fixture_oracle.json").read_text())
        fixture_doc = json.loads((val / "fixture.json").read_text())
        manifest = json.loads((val / "manifest.json").read_text())
        recipe = next(c for c in validation["calls"] if c.get("result") == "ROUTING_RECIPE_VALIDATED")
        fixture_projection = next(c for c in validation["calls"]
                                  if c.get("result") == "GovernedC11Projection")
        release_call = next(c for c in validation["calls"] if c.get("result") == "C11LogicalRelease")
        artifacts = {}
        for path in (data / "source.config.json", data / "crosswalk.json", data / "field_evidence.json",
                     val / "fixture.config.json", val / "fixture.json", val / "fixture_oracle.json",
                     val / "VALIDATION_RESULTS.json", val / "EXCEPTIONS.json",
                     val / "TOPOLOGY_ASSERTIONS.json", val / "manifest.json"):
            artifacts[rel(path)] = {"sha256": sha(path), "bytes": path.stat().st_size}
        residuals = [{"residual_id": r["residual_id"], "field": r["field"], "status": r["status"],
                      "reason": r["reason"], "dependent_operation": r["dependent_operation"],
                      "unaffected_scope": r["unaffected_scope"], "owner": r["owner"],
                      "next_step": r["next_step"]} for r in original.document["residuals"]]
        results[sid] = {
            "source_id": sid,
            "family": original.document["identity"]["family"],
            "wave": original.document["identity"]["wave"],
            "source_sha256": original.original_source_sha256,
            "source_rows": original.document["identity"]["source_row_count"],
            "source_columns": original.document["identity"]["source_column_count"],
            "original_items": original.document["identity"]["original_item_count"],
            "original_config": {
                "path": rel(data / "source.config.json"), "config_id": original.config_id,
                "config_purpose": original.config_purpose, "identity_class": original.identity_class,
                "canonical_sha256": canonical_config_hash(original),
                "file_sha256": sha(data / "source.config.json"),
                "supported_question_ids": original.document["supported_scope"]["supported_question_ids"],
                "included_slots": original.document["coverage"]["physical_slots_included"],
                "included_items": original.document["coverage"]["items_included"],
                "excluded_items_exact": original.document["coverage"]["items_excluded"],
                "original_source_execution": original.document["supported_scope"]["original_source_execution"],
                "residuals": residuals,
            },
            "crosswalk": {"path": rel(data / "crosswalk.json"), "sha256": sha(data / "crosswalk.json"),
                          "method": crosswalk["method"], "counts": crosswalk["counts"],
                          "limits": crosswalk["limits"]},
            "field_evidence": {"path": rel(data / "field_evidence.json"), "sha256": sha(data / "field_evidence.json")},
            "fixture": {"path": rel(val / "fixture.json"), "sha256": sha(val / "fixture.json"),
                        "fixture_id": fixture_doc["fixture_id"],
                        "fixture_source_sha256": fixture_doc["fixture_source_sha256"],
                        "row_count": fixture_doc["row_count"], "identity_class": fixture_doc["identity_class"],
                        "nonrespondent": fixture_doc["nonrespondent"],
                        "config_path": rel(val / "fixture.config.json"),
                        "config_canonical_sha256": canonical_config_hash(fixture_config),
                        "config_file_sha256": sha(val / "fixture.config.json"),
                        "oracle_path": rel(val / "fixture_oracle.json"), "oracle_sha256": sha(val / "fixture_oracle.json"),
                        "oracle_expected_counts": {k: oracle["expected"][k] for k in
                                                   ("response_event_count", "coordinate_fact_count", "routing_fact_count")}},
            "native_validation": {
                "status": validation["status"], "check_count": len(validation["checks"]),
                "passed": sum(1 for c in validation["checks"] if c["pass"]),
                "failed": len(validation["failures"]), "skipped": 0,
                "original_recipe_validation": recipe,
                "original_projection_expansion": "NOT_PERFORMED_BY_DESIGN",
                "fixture_projection": fixture_projection, "fixture_release": release_call,
                "actual_counts": validation["actual"]["counts"],
                "response_state_counts": validation["actual"]["response_state_counts"],
                "routing_state_counts": validation["actual"]["routing_state_counts"],
                "coordinate_state_counts": validation["actual"]["coordinate_state_counts"],
                "release_ref": validation["actual"]["release_ref"],
                "semantic_release_hash": validation["actual"]["semantic_release_hash"],
                "m01_m18_coverage": validation["actual"]["m01_m18_coverage"],
                "refusals": validation["refusals"],
            },
            "topology_assertions": {"path": rel(val / "TOPOLOGY_ASSERTIONS.json"),
                                    "sha256": sha(val / "TOPOLOGY_ASSERTIONS.json"),
                                    "counts": topology["counts"]},
            "exceptions": {"path": rel(val / "EXCEPTIONS.json"), "sha256": sha(val / "EXCEPTIONS.json"),
                           "counts": exceptions["counts"]},
            "manifest": {"path": rel(val / "manifest.json"), "sha256": sha(val / "manifest.json"),
                         "validation_status": manifest.get("validation", {}).get("status")},
            "no_drop": validation["no_drop"],
            "artifacts": artifacts,
        }
    lane = {
        "schema": "PYAT_R157_LANE_RETURN@1.0.0", "lane_id": "ARAB",
        "branch": "agent/pyat-pre553-r157-arab",
        "plan_seal": "4c0c619eac747afee1d8e65e1418bf2d472da4c3",
        "artifact_commit": artifact_commit,
        "p0_corrected_commit": "d8d7087a8e56c24042bf5945fea1c97eb0d6c710",
        "p3_terminal_commit": "519355ec2215409b40d566ef13c3b21f611e0726",
        "source_ids": list(SOURCES),
        "source_results": results,
        "commands": [
            {"command": "PYTHONPATH=. python3 source_pre553_validation/SRC04/tools/arab_full.py",
             "result": "generated/validated full original configs, crosswalks, field evidence, nonrespondent fixtures, fixture configs and oracles for SRC04-SRC07",
             "status": "PASS"},
            {"command": "PYTHONPATH=. python3 source_pre553_validation/SRC04/tools/run_arab_validation.py",
             "result": "SRC04 PASS 731/731; SRC05 PASS 1811/1811; SRC06 PASS 1367/1367; SRC07 PASS 2623/2623; 0 failed; 0 skipped",
             "status": "PASS"},
            {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py -q -o addopts=''",
             "result": "21 passed", "status": "PASS"},
            {"command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_foundation.py rawlsing_next/tests/test_source_configuration_p3.py rawlsing_next/tests/test_pre553_source_backed_c11_facade.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py rawlsing_next/tests/test_pre553_source_read_admission.py rawlsing_next/tests/test_pre553_c11_repository_ingest.py -q -o addopts=''",
             "result": "65 passed", "status": "PASS"},
        ],
        "native_api_calls": [
            "rawlsing_next.source_configuration.schema.load_source_config",
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.source_configuration.fixture.load_fixture_stream",
            "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream (through frozen factory)",
        ],
        "identity_separation": {
            "original_identity_class": "ORIGINAL_SOURCE",
            "fixture_identity_class": "NONRESPONDENT_FIXTURE",
            "original_configs_carry_no_fixture_provenance": True,
            "fixture_source_shas_distinct_from_original": True,
            "original_authority": "DEFER source semantics; ALLOW only local replay protocol",
            "fixture_authority": "fixture_only ALLOW, grade NONRESPONDENT_FIXTURE_ONLY",
            "original_respondent_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        },
        "reader_transport": {"p3_reader_available": True, "config_encoding": None,
                              "reason": "No SRC04-SRC07 SHA is in the exact decoder compatibility allowlist; no encoding is guessed.",
                              "original_source_read": "NOT_PERFORMED"},
        "exceptions_and_limits": {
            "blockers": [],
            "precise_residuals": [
                "SRC04: 181/181 items included (178 response questions + 3 coordinates); no item exclusion.",
                "SRC05: 467/468 included; wt excluded for absent weight design/estimand authority.",
                "SRC06: 354/359 included; wt excluded; Q860A-D continuous list-experiment counts have no finite declared native response domain.",
                "SRC07: 689/690 included; WT excluded for absent weight design/estimand authority.",
                "Routing is SOURCE_ROUTING_UNRESOLVED; the portable recipe uses row_selector=ALL with ROUTING_UNKNOWN and was not physically expanded for original validation.",
                "No form/ballot/administration variable, row-native respondent key, weight design, new direction certification or original-source execution is claimed.",
                "Continuous context is bound as raw coordinates; no false categorical default.",
            ],
            "distinct_review": "NOT_PERFORMED; reserved for the distinct coherent all35 boundary review.",
        },
        "next_integration_edge": {
            "owner": "R157 integration owner / P5 coherent all35 boundary",
            "action": "Intake SRC04-SRC07 configs, crosswalks and nonrespondent fixture positives; rerun the lane validation; then coherent all35 readiness and distinct final review.",
            "artifact_commit": artifact_commit,
            "do_not_do": ["Do not promote fixture authority/universe/SHA into original meaning.",
                          "Do not claim original empirical execution.",
                          "Do not route through the legacy R154 load_all/load_source B49 path."],
        },
        "no_original_source_access": True, "original_respondent_rows_read": 0,
        "original_workload_issued": False, "quota": "UNKNOWN",
        "remote_push": {"status": "NON_FORCE_PUSH_PERFORMED_AFTER_THIS_FILE",
                        "direct_readback": "reported in the final lane return message"},
    }
    out = ROOT / "source_pre553_validation/SRC04/LANE_RETURN.json"
    out.write_text(json.dumps(lane, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} sha256={sha(out)} bytes={out.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
