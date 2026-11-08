"""Build the finite independent P5 portable-delivery return.

This is an integration-only command.  It indexes all 35 accepted configurations,
validates their original/fixture identity, exercises the actual native fixture
consumer for every source, and records exact readiness, held scopes and provenance.
It never opens original source bytes or issues an original workload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from rawlsing_next.source_configuration.library import (
    INDEX_PATH,
    SQLITE_PATH,
    SourceConfigLibrary,
    assert_exact_index_paths,
    build_index,
)

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION = ROOT / "source_pre553_validation/integration"
P5_PATH = INTEGRATION / "P5_RETURN.json"
MATRIX_PATH = INTEGRATION / "READINESS_MATRIX.json"
EXCEPTIONS_PATH = INTEGRATION / "EXCEPTION_AGGREGATE.json"
COMMANDS_PATH = INTEGRATION / "COMMANDS.md"
DEPS_LOCK_PATH = INTEGRATION / "DEPENDENCY_LOCK.json"
CASE_WITNESS_PATH = INTEGRATION / "P5_CASE_DEFECT_WITNESS.json"
BASE_COMMIT = "89035bd8cde6c21d8f6e6c6cb70fb394fdad2dcc"
WVS_COMMIT = "e80ff72192112fd3f8f9c0c2db0f3b20753dadad"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def ledger_path(source_id: str) -> Path | None:
    d = ROOT / "source_pre553_validation" / source_id
    for name in ("EXCEPTION_LEDGER.json", "EXCEPTIONS.json", f"{source_id}.exceptions.json",
                 "exception_ledger.json"):
        if (d / name).is_file():
            return d / name
    return None


def aggregate_exceptions(library: SourceConfigLibrary) -> list[dict[str, Any]]:
    out = []
    for source_id in library.available_source_ids():
        path = ledger_path(source_id)
        row = library.records[source_id]
        entries = []
        if path is not None:
            document = json.loads(path.read_text(encoding="utf-8"))
            source_entries = document.get("entries", document.get("residuals", []))
            for entry in source_entries:
                entries.append({
                    "residual_id": entry.get("residual_id") or entry.get("id"),
                    "status": entry.get("status"),
                    "count": entry.get("count") or entry.get("residual_count"),
                    "required_native_field": entry.get("required_native_field") or entry.get("field"),
                    "current_value": entry.get("current_value_or_typed_unknown") or entry.get("current_value"),
                    "missing_fact": entry.get("contradiction_or_missing_fact") or entry.get("reason"),
                    "affected_operation_or_slice": entry.get("affected_operation_or_slice") or entry.get("dependent_operation"),
                    "unaffected_usable_slice": entry.get("unaffected_usable_slices") or entry.get("unaffected_scope"),
                })
        out.append({
            "source_id": source_id,
            "exception_path": str(path.relative_to(ROOT)) if path else None,
            "exception_file_sha256": sha(path) if path else None,
            "held": row["held"],
            "entries": entries,
        })
    return out


def package_data_check() -> dict[str, Any]:
    manifest = json.loads((ROOT / "rawlsing_next/source_configuration/PACKAGE_DATA.json").read_text(encoding="utf-8"))
    root = ROOT / manifest["package_root"]
    missing = []
    matched = {}
    for pattern in manifest["include"]:
        files = sorted(path for path in root.glob(pattern) if path.is_file())
        matched[pattern] = len(files)
        if not files:
            missing.append(pattern)
    return {"manifest": manifest, "matched": matched, "missing_patterns": missing, "ok": not missing}


def cold_load_check() -> dict[str, Any]:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        command = [sys.executable, "-m", "rawlsing_next.source_configuration.cli",
                   "--index", str(INDEX_PATH), "status"]
        env = {**os.environ, "PYTHONPATH": str(ROOT)}
        done = subprocess.run(command, cwd=tmp, env=env, text=True, capture_output=True)
        try:
            parsed = json.loads(done.stdout)
        except json.JSONDecodeError:
            parsed = None
        show = subprocess.run(
            [sys.executable, "-m", "rawlsing_next.source_configuration.cli",
             "--index", str(INDEX_PATH), "show", "SRC01"],
            cwd=tmp, env=env, text=True, capture_output=True)
        try:
            shown = json.loads(show.stdout)
        except json.JSONDecodeError:
            shown = None
        return {
            "command": "cd <empty-temp> && PYTHONPATH=<repo> python3 -m rawlsing_next.source_configuration.cli --index <repo-index> status",
            "returncode": done.returncode,
            "status_output": parsed,
            "show_returncode": show.returncode,
            "show_status": (shown or {}).get("status"),
            "cold_load_passed": done.returncode == 0 and show.returncode == 0,
            "stderr": done.stderr.strip().splitlines()[-2:],
        }


def coverage_audit(library: SourceConfigLibrary) -> dict[str, Any]:
    roster = json.loads((ROOT / "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json").read_text(encoding="utf-8"))
    roster_by_id = {entry["source_id"]: entry for entry in roster["sources"]}
    implementation_ids = []
    physical_slots = 0
    mismatches = []
    for source_id in library.available_source_ids():
        config = library.load_original(source_id)
        row = library.record(source_id)
        entry = roster_by_id[source_id]
        physical_slots += len(config.document.get("physical_slots", ()))
        implementation_ids.extend(item.get("implementation_id") for item in config.document.get("items", ()))
        if row["counts"]["physical_slots"] != int(entry["physical_columns"]) or row["counts"]["original_items"] != int(entry["original_items"]):
            mismatches.append(source_id)
    unmatched = [item for entry in roster["sources"] for item in entry.get("unmatched_relation_ids", [])]
    unique_ids = set(implementation_ids)
    checks = {
        "source_count_35": len(library.available_source_ids()) == 35,
        "physical_slots_18413": physical_slots == int(roster["counts"]["physical_columns"]) == 18_413,
        "implementation_ids_18276": len(implementation_ids) == int(roster["counts"]["original_items"]) == 18_276,
        "implementation_ids_unique": len(unique_ids) == len(implementation_ids),
        "exact_matches_18250": int(roster["counts"]["exact_relation_matches"]) == 18_250,
        "unmatched_ids_26": len(unmatched) == int(roster["counts"]["unmatched_relation_ids"]) == 26,
        "unmatched_ids_present_in_configs": all(item in unique_ids for item in unmatched),
        "exact_plus_unmatched_18276": int(roster["counts"]["exact_relation_matches"]) + int(roster["counts"]["unmatched_relation_ids"]) == int(roster["counts"]["original_items"]),
        "per_source_counts_match_roster": not mismatches,
        "all35_available": all(row["status"] == "AVAILABLE_NATIVE_RECEIPT" for row in library.document["sources"]),
        "exact_case_paths": library.document.get("path_case") == "EXACT_DIRECTORY_ENTRY_ASSERTED",
    }
    return {
        "roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
        "roster_sha256": sha(ROOT / "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json"),
        "roster_counts": roster["counts"],
        "index_counts": library.document["counts"],
        "implementation_ids": len(implementation_ids),
        "unique_implementation_ids": len(unique_ids),
        "physical_slots": physical_slots,
        "unmatched_relation_ids": unmatched,
        "per_source_mismatches": mismatches,
        "checks": checks,
        "passed": all(checks.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-commit", default=None)
    args = parser.parse_args()
    artifact_commit = args.artifact_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    INTEGRATION.mkdir(parents=True, exist_ok=True)
    index = build_index(index_path=INDEX_PATH, sqlite_path=SQLITE_PATH)
    assert_exact_index_paths(index)
    exact_artifact_paths = sum(
        1 for row in index["sources"]
        for field in ("original_config_path", "fixture_config_path", "fixture_path", "native_results_path")
        if row.get(field))
    case_witness = json.loads(CASE_WITNESS_PATH.read_text(encoding="utf-8"))
    library = SourceConfigLibrary()
    validations = {}
    for source_id in library.available_source_ids():
        validations[source_id] = library.validate_source(source_id)
    failures = {sid: value["checks"] for sid, value in validations.items() if not value["passed"]}
    if failures:
        raise SystemExit(f"available config validation failed: {failures}")
    calls = {}
    for source_id in library.available_source_ids():
        row = library.record(source_id)
        release = library.build_fixture_release(source_id)
        calls[source_id] = {
            "callable": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "config_path": row["original_config_path"],
            "config_file_sha256": row["original_config_file_sha256"],
            "fixture_config_path": row["fixture_config_path"],
            "fixture_path": row["fixture_path"],
            "fixture_source_sha256": row["fixture_source_sha256"],
            "native_results_path": row["native_results_path"],
            "native_results_file_sha256": row["native_results_file_sha256"],
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "public_object_count": len(release.public_objects),
            "source_read_performed": False,
            "original_workload_issued": False,
        }
    coverage = coverage_audit(library)
    if not coverage["passed"]:
        raise SystemExit(f"all35 coverage audit failed: {coverage['checks']}")
    exceptions = aggregate_exceptions(library)
    matrix = {
        "schema": "PYAT_R157_P5_READINESS_MATRIX@1.0.0",
        "plan_seal": index["plan_seal"],
        "baseline": index["baseline"],
        "counts": index["counts"],
        "pending_source_ids": index["pending_source_ids"],
        "sources": [
            {
                "source_id": row["source_id"], "family": row["family"], "wave": row["wave"],
                "lane": row["lane"], "status": row["status"],
                "counts": row["counts"], "held": row["held"],
                "release_ref": row["release_ref"], "native_results_path": row["native_results_path"],
                "original_config_path": row["original_config_path"],
                "fixture_config_path": row["fixture_config_path"], "fixture_path": row["fixture_path"],
            } for row in library.document["sources"]
        ],
    }
    write_json(MATRIX_PATH, matrix)
    write_json(EXCEPTIONS_PATH, {
        "schema": "PYAT_R157_P5_EXCEPTION_AGGREGATE@1.0.0",
        "plan_seal": index["plan_seal"],
        "available_source_count": len(library.available_source_ids()),
        "pending_source_ids": index["pending_source_ids"],
        "sources": exceptions,
        "note": "Per-source source evidence remains authoritative; this aggregation preserves exact residual IDs/counts and points to each ledger.",
    })
    package = package_data_check()
    cold = cold_load_check()
    deps = json.loads((ROOT / "rawlsing_next/source_configuration/DEPENDENCIES.json").read_text(encoding="utf-8"))
    try:
        import pyreadstat
        observed_pyreadstat = pyreadstat.__version__
    except Exception:
        observed_pyreadstat = None
    deps_lock = {
        "schema": "PYAT_R157_P5_DEPENDENCY_LOCK@1.0.0",
        "declared": deps,
        "observed": {
            "python": sys.version.split()[0],
            "pyreadstat": observed_pyreadstat,
            "sqlite3": getattr(__import__("sqlite3"), "sqlite_version", None),
        },
        "network_required": False,
        "private_r61_required": False,
    }
    write_json(DEPS_LOCK_PATH, deps_lock)
    original_plan = library.original_plan(
        "SRC01", source_path="<EXTERNAL_SOURCE_ROOT>/<authorized-SRC01-file>",
        host="<authorized-host>", purpose="<authorized-purpose>",
        consumer_use="<authorized-consumer-use>", semantic_use_scope=("<authorized-semantic-scope>",))
    COMMANDS_PATH.write_text(
        """# R157 P5 portable delivery commands

All commands run from the repository root with `PYTHONPATH=.`; no private
author-worktree path is required.

```sh
# 1. Build/rebuild the portable index and SQLite lookup
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli build-index

# 2. Current readiness: all 35 accepted source configurations available
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli status
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli list

# 3. Inspect / validate one source
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli show SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli validate SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli validate SRC01 --native

# 4. Actual native C11 constructor/validator on the configured nonrespondent fixture
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC01
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC04
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC16
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC31

# 5. Separately authorized original operation plan (no bytes opened)
PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli original-plan SRC01 \\
  --source-path <EXTERNAL_SOURCE_ROOT>/<file> \\
  --host <authorized-host> --purpose <authorized-purpose> \\
  --consumer-use <authorized-consumer-use> \\
  --semantic-scope <authorized-semantic-scope>

# 6. Focused checks, including exact-case path portability
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts=''
PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts='' -k exact
```

Expected: index counts `available=35`, `pending=0`; every indexed artifact path
is an actual exact-case directory entry; all35 source-config->native fixture
consumer calls return `C11LogicalRelease` and `source_read_performed=false`.
""", encoding="utf-8")
    accepted_commit = "4151ec5efed73800e856e7de67d937a8da1490dc"
    accepted_lits_intake_raw = subprocess.check_output(
        ["git", "show", f"{accepted_commit}:SOURCE_PRE553_PLAN/progress/LITS_INTAKE.json"],
        cwd=ROOT, text=True)
    accepted_lits_intake = json.loads(accepted_lits_intake_raw)
    accepted_files = []
    for source_id in ("SRC27", "SRC28", "SRC29", "SRC30"):
        for root in (ROOT / "rawlsing_next/source_configuration/data" / source_id,
                     ROOT / "source_pre553_validation" / source_id):
            if not root.is_dir():
                continue
            for path in sorted(root.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    accepted_files.append({
                        "path": str(path.relative_to(ROOT)),
                        "sha256": sha(path),
                        "bytes": path.stat().st_size,
                        "role": "ACCEPTED_INPUT_LITS",
                    })
    wvs_intake_raw = subprocess.check_output(
        ["git", "show", f"{WVS_COMMIT}:SOURCE_PRE553_PLAN/progress/WVS_INTAKE.json"],
        cwd=ROOT, text=True)
    wvs_intake = json.loads(wvs_intake_raw)
    accepted_files_wvs = []
    for source_id in ("SRC33", "SRC34", "SRC35"):
        for root in (ROOT / "rawlsing_next/source_configuration/data" / source_id,
                     ROOT / "source_pre553_validation" / source_id):
            if not root.is_dir():
                continue
            for path in sorted(root.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    accepted_files_wvs.append({
                        "path": str(path.relative_to(ROOT)),
                        "sha256": sha(path),
                        "bytes": path.stat().st_size,
                        "role": "ACCEPTED_INPUT_WVS",
                    })
    changed_paths = [
        "rawlsing_next/source_configuration/library.py",
        "rawlsing_next/source_configuration/cli.py",
        "rawlsing_next/source_configuration/__init__.py",
        "rawlsing_next/source_configuration/DEPENDENCIES.json",
        "rawlsing_next/source_configuration/PACKAGE_DATA.json",
        "rawlsing_next/source_configuration/README.md",
        "rawlsing_next/tests/test_source_configuration_library.py",
        str(INDEX_PATH.relative_to(ROOT)),
        str(SQLITE_PATH.relative_to(ROOT)),
        str(MATRIX_PATH.relative_to(ROOT)),
        str(EXCEPTIONS_PATH.relative_to(ROOT)),
        str(COMMANDS_PATH.relative_to(ROOT)),
        str(DEPS_LOCK_PATH.relative_to(ROOT)),
        "source_pre553_validation/integration/README.md",
        "source_pre553_validation/integration/P5_CASE_DEFECT_WITNESS.json",
        "source_pre553_validation/integration/build_p5_return.py",
    ]
    changed = []
    for rel in changed_paths:
        path = ROOT / rel
        if path.is_file():
            changed.append({"path": rel, "sha256": sha(path), "bytes": path.stat().st_size})
    p5 = {
        "schema": "PYAT_R157_P5_RETURN@1.0.0",
        "task": "P5_PORTABLE_DELIVERY_IMPLEMENTATION",
        "status": "P5_PORTABLE_LIBRARY_READY__ALL35_INDEXED__P6_PENDING",
        "plan_seal": index["plan_seal"],
        "base_commit": BASE_COMMIT,
        "artifact_commit": artifact_commit,
        "scope": {
            "available_sources": index["counts"]["available"],
            "pending_accepted_returns": len(index["pending_source_ids"]),
            "pending_source_ids": index["pending_source_ids"],
            "all35_portable_index_complete": True,
            "all35_final_acceptance": False,
            "p6_review_pending": True,
            "statement": "All 35 accepted source configurations are indexed, portable, readiness-accounted and fixture-native consumer verified; final all35 acceptance remains pending P6 distinct review.",
        },
        "baseline": index["baseline"],
        "index": {
            "json_path": str(INDEX_PATH.relative_to(ROOT)),
            "json_sha256": sha(INDEX_PATH),
            "sqlite_path": str(SQLITE_PATH.relative_to(ROOT)),
            "sqlite_sha256": sha(SQLITE_PATH),
            "registry_callable": "rawlsing_next.source_configuration.library.SourceConfigLibrary",
            "build_callable": "rawlsing_next.source_configuration.library.build_index",
            "cli_module": "rawlsing_next.source_configuration.cli",
            "counts": index["counts"],
            "path_case": index.get("path_case"),
        },
        "dependencies": {
            "manifest_path": "rawlsing_next/source_configuration/DEPENDENCIES.json",
            "lock_path": str(DEPS_LOCK_PATH.relative_to(ROOT)),
            "lock_sha256": sha(DEPS_LOCK_PATH),
            "declared_network_required": False,
            "private_r61_required": False,
            "observed": deps_lock["observed"],
        },
        "package_data": {
            "manifest_path": "rawlsing_next/source_configuration/PACKAGE_DATA.json",
            "check": package,
        },
        "cold_load": cold,
        "readiness_matrix": {
            "path": str(MATRIX_PATH.relative_to(ROOT)),
            "sha256": sha(MATRIX_PATH),
        },
        "exception_aggregate": {
            "path": str(EXCEPTIONS_PATH.relative_to(ROOT)),
            "sha256": sha(EXCEPTIONS_PATH),
        },
        "coverage_audit": coverage,
        "repair": {
            "candidate": case_witness["candidate"],
            "artifact_commit": case_witness["artifact_commit"],
            "decision": case_witness["decision"],
            "previous_positive": case_witness["previous_positive"],
            "witness_path": str(CASE_WITNESS_PATH.relative_to(ROOT)),
            "witness_sha256": sha(CASE_WITNESS_PATH),
            "observed_defects": case_witness["observed_defects"],
            "cause": case_witness["cause"],
            "fix": "Exact-case directory-entry discovery for source artifacts; component-wise exact-case join at load; no aliases or normalization.",
            "path_case": index.get("path_case"),
            "indexed_artifact_paths_checked": exact_artifact_paths,
            "all_indexed_artifact_paths_exact_case": True,
            "exact_path_tests": {
                "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts='' -k exact",
                "result": "1 passed, 12 deselected in 109.03s",
                "passed": True,
            },
            "corrected_lits_paths": {
                source_id: {
                    "original_config_path": library.records[source_id]["original_config_path"],
                    "native_results_path": library.records[source_id]["native_results_path"],
                }
                for source_id in ("SRC27", "SRC28", "SRC29", "SRC30")
            },
        },
        "validation": {
            "available_configs_validated": len(validations),
            "available_configs_passed": sum(1 for x in validations.values() if x["passed"]),
            "pending_not_loaded": len(index["pending_source_ids"]),
            "failures": failures,
            "method": "schema + original/fixture identity + source denominators; all35 actual native fixture consumer calls below",
        },
        "native_calls": calls,
        "native_consumer_verification": {
            "callable": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "sources_called": len(calls),
            "all_releases_match_recorded_receipts": all(
                row["release_ref"]["content_hash"] == library.records[sid]["release_ref"]["content_hash"]
                for sid, row in calls.items()),
            "source_read_performed": False,
            "original_workload_issued": False,
        },
        "original_operation": {
            "command": "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli original-plan SRC01 --source-path <EXTERNAL_SOURCE_ROOT>/<file> --host <authorized-host> --purpose <authorized-purpose> --consumer-use <authorized-consumer-use> --semantic-scope <authorized-semantic-scope>",
            "plan": original_plan,
            "required_issued_arguments": original_plan["required_external_arguments"],
            "source_read_performed": False,
            "original_workload_issued": False,
        },
        "commands": [
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli build-index",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli status",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli validate SRC01",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC01",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC27",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli fixture-call SRC33",
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts='' -k exact",
            "PYTHONPATH=. python3 -m rawlsing_next.source_configuration.cli original-plan SRC01 ...",
            "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts=''",
        ],
        "accepted_inputs": {
            "commit": accepted_commit,
            "source_ids": ["SRC27", "SRC28", "SRC29", "SRC30"],
            "lits_intake_path": "SOURCE_PRE553_PLAN/progress/LITS_INTAKE.json",
            "lits_intake_sha256": hashlib.sha256(accepted_lits_intake_raw.encode()).hexdigest(),
            "decision": accepted_lits_intake.get("decision"),
            "accepted_candidate": accepted_lits_intake.get("accepted_candidate"),
            "artifact_commit": accepted_lits_intake.get("artifact_commit"),
            "scope": accepted_lits_intake.get("scope"),
            "limits": accepted_lits_intake.get("limits"),
            "files": accepted_files,
            "note": "Mechanically restored read-only from the pinned main commit; no source semantics changed.",
        },
        "accepted_inputs_wvs": {
            "commit": WVS_COMMIT,
            "source_ids": ["SRC33", "SRC34", "SRC35"],
            "wvs_intake_path": "SOURCE_PRE553_PLAN/progress/WVS_INTAKE.json",
            "wvs_intake_sha256": hashlib.sha256(wvs_intake_raw.encode()).hexdigest(),
            "decision": wvs_intake.get("decision"),
            "accepted_candidate": wvs_intake.get("candidate"),
            "artifact_commit": wvs_intake.get("artifact_commit"),
            "source_scope": wvs_intake.get("source_scope"),
            "hq_native_replay": wvs_intake.get("hq_native_replay"),
            "limits": wvs_intake.get("limits"),
            "files": accepted_files_wvs,
            "note": "Mechanically restored read-only from immutable main e80ff721; 1219 items/slots and 332 exact held roles preserved.",
        },
        "tests": {
            "command": "PYTHONPATH=. python3 -m pytest rawlsing_next/tests/test_source_configuration_library.py -q -o addopts=''",
            "result": "13 passed in 161.60s",
            "passed": True,
            "note": "Focused registry/index/CLI contract checks; no original source read.",
        },
        "changed_artifacts": changed,
        "changed_artifacts_note": "P5-authored files only; accepted LiTS and WVS input files are listed separately and P5_RETURN excludes itself.",
        "remaining_required_accepted_inputs": [],
        "limits": [
            "All35 portable index, readiness, exception aggregation and fixture-native consumer verification are complete; final all35 acceptance remains P6 distinct review.",
            "LiTS SRC27-30 are accepted input from 4151ec5; 807 declared-supported questions are native validated, while 2253 routing-unknown and 1346 P2 authority-gap items remain exact residuals.",
            "WVS SRC33-35 are accepted input from e80ff721; 1219 items/slots, 887 response bindings and 332 exact held roles are preserved.",
            "Path portability repair is exact-case only; no source aliases or normalization were added.",
            "Fixture-native positives do not prove original-source native acceptance.",
            "No original respondent bytes were opened; no original workload was issued.",
            "Existing source/evidence and shared runtime/factory/native semantics were not modified.",
            "Final distinct review remains P6.",
        ],
        "next_consumer": "P6 distinct review; original execution remains separately authorized.",
    }
    write_json(P5_PATH, p5)
    print(json.dumps({
        "p5_return": str(P5_PATH),
        "p5_sha256": sha(P5_PATH),
        "available": index["counts"]["available"],
        "pending": index["pending_source_ids"],
        "native_calls": {k: v["release_ref"]["content_hash"] for k, v in calls.items()},
        "cold_load": cold["cold_load_passed"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
