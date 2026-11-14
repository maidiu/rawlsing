"""Fresh-process verification of #1006 author artifacts and representative estate.

Reads author files only; every generated file lands under this review path.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle, execute_bundle_oracle
from review_common import AUTHOR, REVIEW, host_info, sha256_file, write_json

DATA = REVIEW / "data"
EVIDENCE = REVIEW / "evidence"
EXPECTED_BLOBS = {
    "rawlsing_next/pre553_source_direct_parquet_estate.py": "0e4b34ce4973bb4d23b6105faea55b9056ecf373",
    "rawlsing_next/pre553_direct_estate_i03.py": "8b4d5ca2c865e4ef5f5fb609cce15ca3ba64899e",
    "rawlsing_next/_pre553_direct_i02_sourcefree.py": "451727511af7f727b082c518aae2f4a3dbe2ba3a",
    "rawlsing_next/_pre553_external_i02_certificate.py": "cd5368e46a5f2d6016afc2d421717b4191a03005",
    "rawlsing_next/pre553_saved_c11_admission.py": "22749addc1fca5f0b90e12728847c390aafa7a84",
    "rawlsing_next/pre553_saved_workload_integration.py": "cc8aa32512378261406d765f0b049c748cb3e11f",
    "rawlsing_next/pre553_issued_workload.py": "b02810677ae66231e5e59b09aefe9bd63a31aaa3",
    "rawlsing_next/pre553_batch_runner.py": "49e3974c658d66a270815d9faa3798b40d4488b1",
    "rawlsing_next/pre553_carrier_execution.py": "ad1164f21f5f7422a03a19b1b856636edb89cb03",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REVIEW.parents[1], text=True).strip()


def verify_manifest() -> dict:
    manifest = json.loads((AUTHOR / "MANIFEST.json").read_text())
    bad = []
    missing = []
    for item in manifest["files"]:
        path = AUTHOR / item["path"]
        if not path.is_file():
            missing.append(item["path"])
            continue
        digest = sha256_file(path)
        size = path.stat().st_size
        if digest != item["sha256"] or size != item["bytes"]:
            bad.append({
                "path": item["path"], "actual_bytes": size, "actual_sha256": digest,
                "declared_bytes": item["bytes"], "declared_sha256": item["sha256"],
            })
    actual = {
        str(path.relative_to(AUTHOR))
        for path in AUTHOR.rglob("*")
        if path.is_file()
        and ".venv" not in path.parts
        and ".local-data" not in path.parts
        and "__pycache__" not in path.parts
    }
    listed = {item["path"] for item in manifest["files"]}
    return {
        "file_count": manifest["file_count"],
        "listed_count": len(manifest["files"]),
        "verified_count": len(manifest["files"]) - len(bad) - len(missing),
        "missing": missing,
        "bad": bad,
        "unlisted": sorted(actual - listed),
        "declared_total_bytes": manifest["total_bytes"],
        "listed_total_bytes": sum(item["bytes"] for item in manifest["files"]),
    }


def verify_git() -> dict:
    head = git("rev-parse", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    blobs = {}
    for path, expected in EXPECTED_BLOBS.items():
        actual = git("rev-parse", f"HEAD:{path}")
        blobs[path] = {"expected": expected, "actual": actual, "equal": actual == expected}
    production_diff = git(
        "diff", "--name-only",
        "9d96a9cac7d10f59f2c30d8045dd1696fa3ab969", "HEAD", "--", "rawlsing_next",
    )
    post_code_diff = git(
        "diff", "--name-only",
        "05e9ceacfd1a43aa8c21ff3144502550916deadd", "HEAD",
    )
    code_tests = git("show", "--stat", "--oneline", "--no-renames", "05e9ceacfd1a43aa8c21ff3144502550916deadd")
    return {
        "head": head,
        "branch": branch,
        "production_blobs": blobs,
        "all_blobs_equal": all(item["equal"] for item in blobs.values()),
        "production_diff_vs_9d96a9ca": [line for line in production_diff.splitlines() if line],
        "post_code_docs_diff_05e9ceac_to_head": [line for line in post_code_diff.splitlines() if line],
        "code_tests_commit_stat": code_tests,
    }


def copy_estate(receipt: dict) -> Path:
    source = AUTHOR / receipt["root"]
    target_root = DATA / "representative-estate"
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target_root)
    for path in [target_root, *target_root.rglob("*")]:
        path.chmod(0o700 if path.is_dir() else 0o600)
    return target_root


def verify_estate(target_root: Path, receipt: dict) -> dict:
    exact = target_root / receipt["exact_path"]
    member_results = {}
    for name, expected in sorted(receipt["members_sha256"].items()):
        path = exact / name
        actual = sha256_file(path) if path.is_file() else "MISSING"
        member_results[name] = {
            "bytes": path.stat().st_size if path.is_file() else None,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "equal": actual == expected,
        }
    manifest_bytes = (exact / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    manifest_sha = sha256_file(exact / "manifest.json")
    return {
        "root": str(target_root),
        "exact_path": str(exact),
        "members": member_results,
        "all_members_equal": all(item["equal"] for item in member_results.values()),
        "recomputed_manifest_sha256": manifest_sha,
        "held_manifest_sha256": receipt["manifest_sha256"],
        "manifest_equal": manifest_sha == receipt["manifest_sha256"],
        "manifest": manifest,
        "exact_file_set": sorted(path.name for path in exact.iterdir()),
        "no_sqlite": not list(exact.glob("*.sqlite")),
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result: dict = {
        "schema": "PYAT1006_G5_ARTIFACT_VERIFY@1",
        "reviewer_session": "ses_e285e6d52ffe5iAGMQAUd17dSx",
        "host": host_info(),
        "author_manifest": verify_manifest(),
        "git": verify_git(),
    }
    write_json(EVIDENCE / "artifact_verify_partial.json", result)

    receipt = json.loads((AUTHOR / "evidence" / "representative_receipt.json").read_text())
    target_root = copy_estate(receipt)
    estate_result = verify_estate(target_root, receipt)
    result["representative_estate"] = estate_result
    write_json(EVIDENCE / "artifact_verify_partial.json", result)
    if not (
        result["author_manifest"]["missing"] == []
        and result["author_manifest"]["bad"] == []
        and result["git"]["all_blobs_equal"]
        and not result["git"]["production_diff_vs_9d96a9ca"]
        and estate_result["all_members_equal"]
        and estate_result["manifest_equal"]
        and estate_result["no_sqlite"]
    ):
        result["status"] = "FAILED_IDENTITY_CHECK"
        write_json(EVIDENCE / "artifact_verify.json", result)
        print(json.dumps({"status": result["status"]}, indent=2))
        return 2

    exact = Path(estate_result["exact_path"])
    ctx = build_context(ShapeSpec(
        "representative", 64, include_weights=True, tag="PYAT1006-REPRESENTATIVE",
    ))
    bundle = build_query_bundle(ctx)
    admission = SavedC11Admission.open(
        root=target_root,
        exact_path=exact,
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**receipt["i02"]),
        release_ref=exact_ref(receipt["reconstructed_v1_release_ref"]),
        runtime_catalog=bundle.catalog,
        current_authorizer=lambda _roots: True,
    )
    result["reconstructed_release_ref"] = admission.release_ref.as_dict()
    result["release_equal"] = (
        admission.release_ref.as_dict() == receipt["reconstructed_v1_release_ref"]
    )
    result["binding_receipt"] = admission.binding_receipt()
    write_json(EVIDENCE / "artifact_verify_partial.json", result)

    native_repo, native_release = ctx.native_oracle()
    oracle = execute_bundle_oracle(
        native_repo, native_release, bundle,
        qa=bundle.catalog.authorities[-2], dauth=bundle.catalog.authorities[-1],
    )
    result["native_oracle_release"] = native_release.as_dict()
    result["native_release_matches_receipt"] = (
        native_release.as_dict() == receipt["native_oracle_release"]
    )
    queries = {}
    all_equal = True
    for name in (
        "selected", "f2_forward", "f2_reverse", "f4_three", "f4_four",
        "weighted", "repeated",
    ):
        query, predicate = bundle.by_name(name)
        saved = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        expected = receipt["queries"][name]
        native = oracle[name]
        facts_equal = tuple(f.ref for f in saved.facts) == tuple(
            f.ref for f in native.facts
        )
        projections_equal = tuple(
            canonical_json(f.semantic_projection()) for f in saved.facts
        ) == tuple(canonical_json(f.semantic_projection()) for f in native.facts)
        receipt_refs_equal = [
            f.ref.as_dict() for f in saved.facts
        ] == expected["fact_refs"]
        release_refs_equal = saved.release_refs == native.release_refs
        equal = facts_equal and projections_equal and receipt_refs_equal and release_refs_equal
        all_equal = all_equal and equal
        queries[name] = {
            "equal": equal,
            "facts_equal_native": facts_equal,
            "projections_equal_native": projections_equal,
            "fact_refs_equal_author_receipt": receipt_refs_equal,
            "release_refs_equal": release_refs_equal,
            "fact_refs": [f.ref.as_dict() for f in saved.facts],
            "fact_states": [f.typed_state for f in saved.facts],
            "denominators": [getattr(f, "raw_denominator_support", None) for f in saved.facts],
        }
    saved_i05 = admission.execute_i05(
        discovery_authority_ref=bundle.discovery_authority.ref,
    )
    i05_equal = (
        tuple(r.ref for r in saved_i05.receipts)
        == tuple(r.ref for r in oracle["i05"].receipts)
        and tuple(f.ref for f in saved_i05.empirical_facts)
        == tuple(f.ref for f in oracle["i05"].empirical_facts)
        and [f.ref.as_dict() for f in saved_i05.empirical_facts]
        == receipt["i05"]["fact_refs"]
        and [r.ref.as_dict() for r in saved_i05.receipts]
        == receipt["i05"]["receipt_refs"]
    )
    result["queries"] = queries
    result["all_queries_equal"] = all_equal
    result["i05"] = {
        "equal": i05_equal,
        "candidate_count": saved_i05.candidate_count,
        "covered_candidate_count": saved_i05.covered_candidate_count,
        "fact_refs": [f.ref.as_dict() for f in saved_i05.empirical_facts],
        "receipt_refs": [r.ref.as_dict() for r in saved_i05.receipts],
    }
    result["typed_absences"] = dict(ctx.typed_absences())
    result["family_counts"] = dict(ctx.shape.family_counts())
    result["status"] = (
        "MEASURED" if (all_equal and i05_equal and result["release_equal"]
                       and result["native_release_matches_receipt"]) else "FAILED_PARITY"
    )
    result["seconds"] = time.monotonic() - started
    write_json(EVIDENCE / "artifact_verify.json", result)
    print(json.dumps({
        "status": result["status"],
        "manifest": {
            "verified": result["author_manifest"]["verified_count"],
            "bad": len(result["author_manifest"]["bad"]),
        },
        "estate_all_members_equal": estate_result["all_members_equal"],
        "all_queries_equal": all_equal,
        "i05_equal": i05_equal,
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "MEASURED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
