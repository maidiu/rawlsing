#!/usr/bin/env python3
"""Materialize and validate exact R157 SourceConfig metadata for all 35 waves.

This reads only metadata/config blobs from immutable Git revisions.  It writes
no respondent/source body bytes and commits no config blob: exact revisions and
hashes are retained in CONFIG_INDEX.json; a private temporary staging directory
is used for parser input and removed at exit.

Current parser: aee95429609c372564e996c2d3d3eb30e9253cbf
load_source_config / canonical_config_hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
OWNER = ROOT / "OWNER"
IMPLEMENTER = ROOT / "IMPLEMENTER"
REUSE = OWNER / "WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_INPUT_REUSE_20261118/REUSE_RESULT.json"
BUNDLES = IMPLEMENTER / "WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/bundles"
SNAPSHOT = Path("/tmp/anvil_all35_aee")
R157_COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
SRC04_REPAIR_COMMIT = "da23c65d1e211cb7e8ce416e98757f321b78d25e"
SRC04_REPAIR_PATH = "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(IMPLEMENTER), "show", f"{commit}:{path}"]
    )


def parser_modules():
    import sys
    sys.path.insert(0, str(SNAPSHOT))
    from rawlsing_next.pre553_r157_projection_adapter import (
        canonical_config_hash, load_source_config,
    )
    return load_source_config, canonical_config_hash


def expected_shape(bundle):
    counts = bundle["counts"]
    return {
        "rows": bundle["declared_rows"],
        "columns": bundle["declared_columns"],
        "original_items": counts["original_items"],
        "physical_slots": counts["physical_slots"],
        "questions": counts["questions"],
        "response_slots": counts["response_slots"],
        "coordinate_slots": counts["coordinate_slots"],
        "weight_slots": counts["weight_slots"],
        "routing_rules": counts["routing_rules"],
    }


def actual_shape(document):
    return {
        "rows": document["identity"]["source_row_count"],
        "columns": document["identity"]["source_column_count"],
        "original_items": document["identity"]["original_item_count"],
        "physical_slots": len(document["physical_slots"]),
        "questions": len(document["questions"]),
        "response_slots": len(document["response_slots"]),
        "coordinate_slots": len(document["coordinate_slots"]),
        "weight_slots": len(document["weight_slots"]),
        "routing_rules": len(document["routing"]),
    }


def resolve(row):
    sid = row["source_id"]
    loc = row["source_config"]
    if sid == "SRC04":
        return {
            "source_id": sid, "commit": SRC04_REPAIR_COMMIT,
            "path": SRC04_REPAIR_PATH,
            "expected_file_sha": loc["file_sha256"],
            "expected_canonical_sha": loc["canonical_sha256"],
            "revision_basis": "REPAIRED_ACCEPTED_SRC04_PREFERRED_OVER_STALE_1924499",
        }
    return {
        "source_id": sid, "commit": loc["historical_r157_commit"],
        "path": loc["path"], "expected_file_sha": loc["file_sha256"],
        "expected_canonical_sha": loc["canonical_sha256"],
        "revision_basis": "EXACT_R157_ACCEPTED_LOCATOR",
    }


def compare(config, bundle, canonical_config_hash):
    d = config.document
    expected_source = bundle["source_sha256"]
    expected = expected_shape(bundle)
    actual = actual_shape(d)
    checks = {
        "source_id": config.source_id == bundle["source_id"],
        "identity_class": config.identity_class == "ORIGINAL_SOURCE",
        "binding_source_sha": config.active_source_sha256 == expected_source,
        "identity_expected_sha": d["identity"]["expected_source_sha256"] == expected_source,
        "binding_row_count": d["binding"]["row_count"] == bundle["declared_rows"],
        "declared_shape": actual == expected,
        "config_purpose": config.config_purpose == "SOURCE_PREPARATION",
        "schema": d.get("schema") == "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
    }
    canonical = canonical_config_hash(config)
    return {
        "checks": checks,
        "canonical_sha256": canonical,
        "canonical_matches_locator": canonical == bundle["source_config"]["canonical_sha256"],
        "declared_shape_expected": expected,
        "declared_shape_actual": actual,
        "q2_input_status": bundle.get("q2_input_status"),
        "missing_q2_inputs": bundle.get("missing_q2_inputs", []),
        "qualified_metadata": all(checks.values()) and canonical == bundle["source_config"]["canonical_sha256"],
        "authorized_executable_q2": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "CONFIG_INDEX.json")
    parser.add_argument("--validation", type=Path, default=Path(__file__).resolve().parent / "VALIDATION.json")
    parser.add_argument("--negative", type=Path, default=Path(__file__).resolve().parent / "NEGATIVE_EVIDENCE.json")
    args = parser.parse_args()
    load_source_config, canonical_config_hash = parser_modules()
    reuse = json.loads(REUSE.read_text())
    index_rows = []
    failures = []
    with tempfile.TemporaryDirectory(prefix="anvil-all35-configs-") as tmp:
        tmp = Path(tmp)
        for row in reuse["rows"]:
            sid = row["source_id"]
            bundle = json.loads((BUNDLES / f"{sid}.json").read_text())
            resolved = resolve(row)
            try:
                raw = git_bytes(resolved["commit"], resolved["path"])
                file_sha = sha(raw)
                if file_sha != resolved["expected_file_sha"]:
                    raise ValueError(f"FILE_HASH_MISMATCH expected {resolved['expected_file_sha']} actual {file_sha}")
                staged = tmp / f"{sid}.config.json"
                staged.write_bytes(raw)
                config = load_source_config(staged)
                comparison = compare(config, bundle, canonical_config_hash)
                if not comparison["qualified_metadata"]:
                    raise ValueError(f"CONFIG_QUALIFICATION_MISMATCH {comparison['checks']}")
                index_rows.append({
                    "source_id": sid, "source_config": {
                        "revision_commit": resolved["commit"],
                        "revision_path": resolved["path"],
                        "revision_ref": f"{resolved['commit']}:{resolved['path']}",
                        "file_sha256": file_sha,
                        "canonical_sha256": comparison["canonical_sha256"],
                        "revision_basis": resolved["revision_basis"],
                    },
                    "identity": {
                        "source_id": config.source_id,
                        "identity_class": config.identity_class,
                        "source_sha256": config.active_source_sha256,
                    },
                    "declared_shape": comparison["declared_shape_actual"],
                    "checks": comparison["checks"],
                    "q2_input_status": comparison["q2_input_status"],
                    "missing_q2_inputs": comparison["missing_q2_inputs"],
                    "qualified_metadata": True,
                    "authorized_executable_q2": False,
                    "staging": "PRIVATE_TEMP_ONLY__NO_CONFIG_BLOB_COMMITTED",
                })
            except Exception as exc:
                failures.append({"source_id": sid, "status": "FAILED", "detail": f"{type(exc).__name__}: {exc}", "revision_ref": f"{resolved['commit']}:{resolved['path']}"})
        # Negative 1: stale SRC04 sibling must fail the accepted repaired pin.
        negative = {"schema": "ANVIL_ALL35_CONFIG_NEGATIVE_EVIDENCE@1", "checks": []}
        stale = git_bytes(R157_COMMIT, "rawlsing_next/source_configuration/data/SRC04/source.config.json")
        stale_hash = sha(stale)
        expected_src04 = next(
            r["source_config"]["file_sha256"] for r in reuse["rows"]
            if r["source_id"] == "SRC04"
        )
        negative["checks"].append({
            "name": "stale_src04_sibling_rejected",
            "status": "PASS" if stale_hash != expected_src04 else "FAIL",
            "expected_accepted_file_sha256": expected_src04,
            "observed_stale_file_sha256": stale_hash,
        })
        # Negative 2: hold the accepted config fixed and supply a mismatched
        # pinned source SHA.  This exercises the source identity gate without
        # touching respondent/source bytes or rewriting a config blob.
        raw = git_bytes(R157_COMMIT, reuse["rows"][0]["source_config"]["path"])
        accepted = tmp / "SRC01.accepted.json"
        accepted.write_bytes(raw)
        config = load_source_config(accepted)
        bundle = json.loads((BUNDLES / "SRC01.json").read_text())
        wrong_bundle = dict(bundle)
        wrong_bundle["source_sha256"] = "0" * 64
        comp = compare(config, wrong_bundle, canonical_config_hash)
        negative["checks"].append({
            "name": "source_sha_mismatch_rejected",
            "status": "PASS" if comp["checks"]["binding_source_sha"] is False else "FAIL",
            "observed_source_sha256": config.active_source_sha256,
            "expected_source_sha256": wrong_bundle["source_sha256"],
        })
    index = {
        "schema": "ANVIL_ALL35_R157_CONFIG_INDEX@1",
        "source": "OWNER/WORKER_RETURNS/ANVIL_ALL35_ORIGINAL_INPUT_REUSE_20261118/REUSE_RESULT.json",
        "canonical_matrix_commit": "d4f0a6499432aa3186c0d92174fa228211759e44",
        "current_parser_commit": "aee95429609c372564e996c2d3d3eb30e9253cbf",
        "historical_config_commit": R157_COMMIT,
        "src04_repaired_commit": SRC04_REPAIR_COMMIT,
        "counts": {"total": 35, "qualified_metadata": len(index_rows), "failed": len(failures), "authorized_executable_q2": 0, "q2_held": sum(1 for r in index_rows if r["q2_input_status"] == "HELD")},
        "q2_boundary": "PARSED_QUALIFIED_METADATA_ONLY__Q2_CENSUS_FRONTIER_INVENTORY_POLICY_RESOLVER_NOT_ESTABLISHED__NO_EXECUTABLE_AUTHORITY",
        "rows": index_rows,
        "failures": failures,
    }
    validation = {
        "schema": "ANVIL_ALL35_R157_CONFIG_VALIDATION@1",
        "status": "PASS" if not failures and len(index_rows) == 35 else "FAILED",
        "counts": index["counts"],
        "rows": [{"source_id": r["source_id"], "status": "QUALIFIED_METADATA", "file_sha256": r["source_config"]["file_sha256"], "canonical_sha256": r["source_config"]["canonical_sha256"], "q2_input_status": r["q2_input_status"], "authorized_executable_q2": False} for r in index_rows],
        "failures": failures,
        "negative": negative["checks"],
    }
    args.out.write_text(json.dumps(index, indent=2) + "\n")
    args.validation.write_text(json.dumps(validation, indent=2) + "\n")
    args.negative.write_text(json.dumps(negative, indent=2) + "\n")
    print(json.dumps({"status": validation["status"], "qualified": len(index_rows), "failed": len(failures), "positive": [x["status"] for x in negative["checks"]]}, indent=2))
    return 0 if validation["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
