#!/usr/bin/env python3
"""Run the exact reviewer fake-launcher witness on old R3 and corrected source."""
from __future__ import annotations
import json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ORIGINAL = HERE / "fake_attest_launch.original.py"
MATCHING = HERE / "fake_attest_launch.matching_session.py"
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-launch-auth-repair-20261116-r4/fake-attest-witness"
OLD_REPO = REPO / ".local-logs/sorok-programma-automatic-currentness-launch-auth-repair-20261116-r4/old-r3-source"
NEW_REPO = REPO
OUT = HERE.parent / "evidence/fake_attest_witness_report.json"


def prepare_sandbox(label: str, launcher_bytes: bytes) -> tuple[Path, Path]:
    root = SCRATCH / label
    if root.exists():
        shutil.rmtree(root)
    repo = root / "repo"
    (repo / "state").mkdir(parents=True)
    (repo / "controller-state").mkdir()
    for name in ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md"):
        shutil.copy2(NEW_REPO / "SOROK_PRODUCT_CONTROL_ROOM" / name,
                     repo / name)
    frozen_src = NEW_REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1"
    frozen_dst = repo / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1"
    shutil.copytree(frozen_src, frozen_dst)
    cfg = repo / "config.json"
    cfg.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(repo),
        "pair_json": "CURRENT_PROGRESS.json",
        "pair_md": "CURRENT_PROGRESS.md",
        "state_root": "state",
        "controller_state_root": "controller-state",
    }, indent=2) + "\n")
    launcher = root / "launch.py"
    launcher.write_bytes(launcher_bytes)
    return root, launcher


def run_case(label: str, candidate: Path, launcher_bytes: bytes) -> dict:
    root, launcher = prepare_sandbox(label, launcher_bytes)
    cfg = root / "repo/config.json"
    pair = root / "repo/CURRENT_PROGRESS.json"
    whole = json.loads(pair.read_text())
    whole.pop("operational_currentness_runtime_r1", None)
    pair.write_text(json.dumps(whole, indent=2) + "\n")
    subprocess.run(
        [sys.executable, "-B", str(candidate / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"),
         "--config", str(cfg), "init"], cwd=str(root), check=True,
        capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    env = dict(os.environ, FAKE_ROOT=str(root), REPO=str(candidate),
               PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, "-B", str(launcher), "--binding", "fake", "--job", "fake"],
        cwd=str(root), capture_output=True, text=True, env=env, timeout=180)
    return {
        "label": label,
        "candidate": str(candidate),
        "command": [sys.executable, "-B", str(launcher), "--binding", "fake",
                    "--job", "fake"],
        "exit": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "attest_out": (root / "attest.out").read_text() if (root / "attest.out").exists() else None,
        "attest_err": (root / "attest.err").read_text() if (root / "attest.err").exists() else None,
        "attest_exit": (root / "attest.exit").read_text().strip() if (root / "attest.exit").exists() else None,
        "sandbox": str(root),
        "run_dir": str(root / "repo/controller-state/fake-attest"),
    }


def fake_review(case: dict, candidate: Path) -> dict:
    root = Path(case["sandbox"])
    run = Path(case["run_dir"])
    receipt_target = root / "work/return/REVIEW_RECEIPT.json"
    receipt_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HERE.parent / "evidence/raw/r2_reviewer_receipt.ea5.json",
                 receipt_target)
    cfg = root / "repo/config.json"
    proc = subprocess.run(
        [sys.executable, "-B", str(candidate / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"),
         "--config", str(cfg), "intake-review", "--review-run-dir", str(run),
         "--receipt", str(receipt_target)],
        cwd=str(root), capture_output=True, text=True, timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return {"exit": proc.returncode, "stdout": proc.stdout,
            "stderr": proc.stderr}


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if not OLD_REPO.is_dir():
        raise SystemExit(f"missing old worktree: {OLD_REPO}")
    old = run_case("old-r3", OLD_REPO, ORIGINAL.read_bytes())
    new = run_case("corrected", NEW_REPO, ORIGINAL.read_bytes())
    matching = run_case("corrected-matching-session", NEW_REPO, MATCHING.read_bytes())
    old_review = fake_review(old, OLD_REPO)
    new_review = fake_review(new, NEW_REPO)
    report = {
        "schema": "SOROK_AUTOMATIC_CURRENTNESS_R4_FAKE_ATTEST_WITNESS@1",
        "original_launcher": {
            "path": "probes/fake_attest_launch.original.py",
            "sha256": __import__("hashlib").sha256(ORIGINAL.read_bytes()).hexdigest(),
            "source": "a49be6e8bf728262dad62753f3066e99351b7af9:WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/evidence/raw/fake_attest/launch.py",
        },
        "old": old,
        "corrected": new,
        "corrected_matching_session": matching,
        "old_fake_review_intake": old_review,
        "corrected_fake_review_intake": new_review,
        "old_bypass": str(old.get("attest_exit")) == "0" and "TRUSTED_LAUNCH_ATTESTED" in (old["stdout"] or "") + (old["attest_out"] or ""),
        "corrected_refused": str(new.get("attest_exit")) not in ("0", "")
            and "TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH" in (new["attest_err"] or ""),
        "corrected_matching_session_refused": str(matching.get("attest_exit")) not in ("0", "")
            and "LAUNCHER_PROOF_REQUIRED" in (matching["attest_err"] or ""),
        "verdict": "PASS" if (
            str(old.get("attest_exit")) == "0"
            and "TRUSTED_LAUNCH_ATTESTED" in (old["stdout"] or "") + (old["attest_out"] or "")
            and str(new.get("attest_exit")) not in ("0", "")
            and "TRUSTED_LAUNCH_ACTUAL_SESSION_MISMATCH" in (new["attest_err"] or "")
            and str(matching.get("attest_exit")) not in ("0", "")
            and "LAUNCHER_PROOF_REQUIRED" in (matching["attest_err"] or "")
            and old_review["exit"] == 0
            and "EVENT_RECORDED" in (old_review["stdout"] or "")
            and new_review["exit"] != 0
            and "UNTRUSTED_CONTROLLER_RUN" in (new_review["stderr"] or "")
        ) else "GAP",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"old_exit": old.get("attest_exit"),
                      "new_exit": new.get("attest_exit"),
                      "matching_exit": matching.get("attest_exit"),
                      "old_bypass": report["old_bypass"],
                      "corrected_refused": report["corrected_refused"],
                      "corrected_matching_session_refused": report["corrected_matching_session_refused"],
                      "old_fake_review_exit": old_review["exit"],
                      "new_fake_review_exit": new_review["exit"],
                      "verdict": report["verdict"]}, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
