#!/usr/bin/env python3
"""Focused launcher proof tamper variants; no secret is printed."""
from __future__ import annotations
import hashlib, json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK"))
import operational_currentness_runtime_r1 as rt

OUT = HERE.parent / "evidence/launcher_proof_variants_report.json"
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-launch-auth-repair-20261116-r4/launcher-proof-variants"


def verdict(call):
    try:
        return {"result": "ACCEPTED", "call": call()}
    except rt.CurrentnessError as exc:
        return {"result": "REFUSED", "error": str(exc).split(":", 1)[0]}


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True)
    identity = rt._launcher_identity()
    spec = {
        "run_dir": str(SCRATCH / "run"),
        "job_id": "job-a",
        "session": "session-a",
        "grant_id": "grant-a",
        "argv_sha256": "a" * 64,
        "worktree": str(SCRATCH / "work"),
        "role": "REVIEWER",
        "task_id": "AUTOMATIC_CURRENTNESS_R1",
        "expected_session": "session-a",
        "expected_source_commit": "b" * 40,
    }
    token = rt._launcher_token(spec)
    good = {"path": identity["path"], "sha256": identity["sha256"],
            "token": token}
    copy = SCRATCH / "launch.py"
    shutil.copy2(identity["path"], copy)
    cases = {
        "positive_exact": (spec, good),
        "same_basename_different_path": (spec, {**good, "path": str(copy)}),
        "bytecopy_different_path": (spec, {**good, "path": str(copy),
                                           "sha256": hashlib.sha256(copy.read_bytes()).hexdigest()}),
        "wrong_hash": (spec, {**good, "sha256": "0" * 64}),
        "wrong_token": (spec, {**good, "token": "0" * 64}),
        "mismatched_session": (spec, {**good, "token": rt._launcher_token(
            {**spec, "session": "session-b"})}),
        "mismatched_job": (spec, {**good, "token": rt._launcher_token(
            {**spec, "job_id": "job-b"})}),
        "mismatched_source": (spec, {**good, "token": rt._launcher_token(
            {**spec, "expected_source_commit": "c" * 40})}),
        "mismatched_role": (spec, {**good, "token": rt._launcher_token(
            {**spec, "role": "IMPLEMENTER"})}),
    }
    results = {name: verdict(lambda s=spec_, p=proof: rt._verify_launcher_proof(s, p))
               for name, (spec_, proof) in cases.items()}
    report = {
        "schema": "SOROK_AUTOMATIC_CURRENTNESS_R4_LAUNCHER_PROOF_VARIANTS@1",
        "launcher_path": identity["path"],
        "launcher_sha256": identity["sha256"],
        "results": results,
        "positive_exact": results["positive_exact"]["result"] == "ACCEPTED",
        "all_negative_refused": all(
            results[name]["result"] == "REFUSED"
            and results[name]["error"] in (
                "LAUNCHER_PATH_MISMATCH", "LAUNCHER_HASH_MISMATCH",
                "LAUNCHER_TOKEN_MISMATCH")
            for name in cases if name != "positive_exact"),
        "verdict": "PASS" if (
            results["positive_exact"]["result"] == "ACCEPTED"
            and all(results[name]["result"] == "REFUSED"
                    for name in cases if name != "positive_exact")
        ) else "GAP",
    }
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"positive_exact": report["positive_exact"],
                      "all_negative_refused": report["all_negative_refused"],
                      "verdict": report["verdict"],
                      "errors": {k: v.get("error") for k, v in results.items()}},
                     indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
