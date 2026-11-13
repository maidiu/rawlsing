"""SOROK #1023 independent G5 immutable source/test provenance collector."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
B_HEAD = "1161e5f74081888bd813825b3df4afab3e2f5ca7"
CODE_CUT = "c724d1a89626f3e177acd004c0be20029dc7ade4"
DOC_CUT = "fb061dec16c8386b9caa1b5ea75ec7645aff88a7"
PACKETS = "227ce149fc7864c83c179a7d3ecaef2b92c5bdab"
OVERLAY = "f5c43c80675f2556e1287bf55d25052d11e8746e"

B_FILES = [
    "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py",
    "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py",
    "WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py",
    "WORKER_RETURNS/SOROK-DUEL-B04-R1/material_operations.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/rolling_reproduction.py",
]
B_TESTS = [
    "WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py",
    "WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py",
    "WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py",
    "WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_incremental.py",
    "WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py",
    "WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py",
    "WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_operations.py",
    "WORKER_RETURNS/SOROK-DUEL-B04-R1/test_b04_composition.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rolling.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_rollback.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_batch_cycle.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_cross_batch.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_zero_and_held.py",
    "WORKER_RETURNS/SOROK-DUEL-B05-R1/test_b05_interleave_retry.py",
]
C_FILES = [
    "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_activity.py",
    "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_decision.py",
    "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/parent_speech.py",
    "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py",
]
J1_FILES = [
    "WORKER_RETURNS/SOROK-E01-J1-995-R1/j1_join.py",
    "WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py",
    "WORKER_RETURNS/SOROK-E01-J1-995-R1/SOURCE_DERIVATION.json",
    "WORKER_RETURNS/SOROK-E01-J1-995-R1/SOURCE_DERIVATION.md",
]
OVERLAY_FILES = [
    "SOROK_PRODUCT_CONTROL_ROOM/00_READ_ME_FIRST.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_PROGRAMMA_SOROK.md",
    "CROSS_HQ_CONTROL_ROOM/MCR_LITE_EXECUTION_DISCIPLINE_R1.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_UM_SOROK_GOVERNING_BRAIN_AND_GROKKING_R1.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/00_UM_SOROK_GROKKING_DECISION_SCHEMA_R1.json",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CG_B_G_SEMANTIC_RECONCILIATION_AND_CAMPAIGNS_20261112_R2.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CG_B_G_SEMANTIC_RECONCILIATION_AND_CAMPAIGNS_20261112_R2.json",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CG_B_G_TASK_SEMANTIC_LABELS_AND_DECISION_HIERARCHY_20261112_R1.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CG_B_G_TASK_SEMANTIC_LABELS_AND_DECISION_HIERARCHY_20261112_R1.json",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/UM_SOROK_25_ISSUE_POWER_PASS_R1.md",
    "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/UM_SOROK_25_ISSUE_POWER_PASS_R1.json",
]
PACKET_FILE = "SOROK_PRODUCT_CONTROL_ROOM/ADVERSARIAL_IMPLEMENTATION_20261112_R1/03_TASK_PACKETS_R1.json"


def run(*args: str) -> str:
    return subprocess.run(
        list(args), cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def git_blob(rev: str, path: str) -> str | None:
    try:
        return run("git", "rev-parse", f"{rev}:{path}")
    except subprocess.CalledProcessError:
        return None


def git_sha256(rev: str, path: str) -> str | None:
    try:
        data = subprocess.run(
            ["git", "cat-file", "-p", f"{rev}:{path}"],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
    except subprocess.CalledProcessError:
        return None
    return hashlib.sha256(data).hexdigest()


def sha256(path: str) -> str | None:
    target = ROOT / path
    if not target.exists():
        return None
    return hashlib.sha256(target.read_bytes()).hexdigest()


def rows(paths: list[str]) -> dict:
    result = {}
    for path in paths:
        result[path] = {
            "worktree_git_blob": (run("git", "hash-object", path)
                                  if (ROOT / path).exists() else None),
            "HEAD": git_blob("HEAD", path),
            "B_head": git_blob(B_HEAD, path),
            "code_cut_c724d1a8": git_blob(CODE_CUT, path),
            "code_cut_c724d1a8_sha256": git_sha256(CODE_CUT, path),
            "doc_cut_fb061dec": git_blob(DOC_CUT, path),
            "worktree_sha256": sha256(path),
        }
    return result


def main() -> int:
    pins = {
        "schema": "SOROK1023_G5_BLOB_PINS@1",
        "reviewer_session": "ses_e28ef72f9ffelBx7qet6BAina3",
        "reviewer_branch": run("git", "branch", "--show-current"),
        "host": platform.node(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "git_head_at_review_start": "fb061dec16c8386b9caa1b5ea75ec7645aff88a7",
        "assigned_branch_start": DOC_CUT,
        "source_B_head": B_HEAD,
        "composed_code_cut": CODE_CUT,
        "documentary_cut": DOC_CUT,
        "packets_commit": PACKETS,
        "overlay_commit": OVERLAY,
        "B_product_blobs": rows(B_FILES),
        "B_test_blobs": rows(B_TESTS),
        "C_integration_blobs": rows(C_FILES),
        "J1_blobs": rows(J1_FILES),
        "overlay_and_law_blobs": {
            path: {
                "worktree_git_blob": (run("git", "hash-object", path)
                                      if (ROOT / path).exists() else None),
                "current_HEAD": git_blob("HEAD", path),
                "overlay_f5c43c8": git_blob(OVERLAY, path),
                "worktree_sha256": sha256(path),
            }
            for path in OVERLAY_FILES
        },
        "packets_file": {
            "git_blob_at_227ce149": git_blob(PACKETS, PACKET_FILE),
            "worktree_sha256": sha256(PACKET_FILE),
        },
        "checks": {},
    }
    checks = pins["checks"]
    checks["B_product_equal_source_head"] = all(
        row["worktree_git_blob"] == row["B_head"] == row["code_cut_c724d1a8"]
        for row in pins["B_product_blobs"].values())
    checks["B_tests_equal_source_head"] = all(
        row["worktree_git_blob"] == row["B_head"]
        for row in pins["B_test_blobs"].values())
    checks["composed_code_preserves_B"] = checks["B_product_equal_source_head"]
    checks["doc_cut_product_equals_code_cut"] = all(
        row["doc_cut_fb061dec"] == row["code_cut_c724d1a8"]
        for row in (*pins["B_product_blobs"].values(),
                    *pins["C_integration_blobs"].values()))
    parent_row = pins["C_integration_blobs"][
        "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/"
        "developmental_recursion/parent_decision.py"]
    checks["parent_decision_code_cut_sha256"] = parent_row[
        "code_cut_c724d1a8_sha256"]
    checks["parent_decision_expected"] = (
        checks["parent_decision_code_cut_sha256"]
        == "0fa40ee88f4f32e12a05fb687b7da4ff75b27717782797557239741356c034d4")
    checks["C_worktree_sha256_equals_code_cut"] = all(
        row["worktree_sha256"] == row["code_cut_c724d1a8_sha256"]
        for row in pins["C_integration_blobs"].values())
    product_changed = run("git", "diff", "--name-only", DOC_CUT, "--", ".",
                          ":!WORKER_REVIEWS/SOROK1023_MATERIAL_WORLD_G5_R1")
    checks["product_paths_changed_from_doc_cut"] = [
        line for line in product_changed.splitlines() if line.strip()]
    checks["product_unmodified"] = not checks["product_paths_changed_from_doc_cut"]
    output = HERE / "BLOB_PINS.json"
    output.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(json.dumps({"written": str(output.relative_to(ROOT)),
                      "checks": checks}, indent=2, sort_keys=True))
    return 0 if checks["product_unmodified"] and checks["B_product_equal_source_head"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
