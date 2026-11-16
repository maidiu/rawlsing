#!/usr/bin/env python3
"""Positive: the actual installed launcher auto-attests a sandbox run."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-r4-receiving-20261116-r1/installed-launcher-positive"
LAUNCHER = Path("/Users/matthewsmith/.local/share/rawlsing-controller/local-automation/64d52127/launch.py")
PYTHON = "/private/tmp/rawlsing-oct28-p1r1/venv/bin/python"
OUT = HERE.parent / "evidence/installed_launcher_positive_report.json"


def digest_argv(argv):
    return hashlib.sha256(json.dumps(argv, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    repo = SCRATCH / "repo"
    (repo / "state").mkdir(parents=True)
    (repo / "controller-state").mkdir()
    (repo / "work").mkdir()
    for name in ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md"):
        shutil.copy2(REPO / "SOROK_PRODUCT_CONTROL_ROOM" / name, repo / name)
    config = {
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(repo),
        "pair_json": "CURRENT_PROGRESS.json",
        "pair_md": "CURRENT_PROGRESS.md",
        "state_root": "state",
        "controller_state_root": "controller-state",
    }
    cfg = repo / "config.json"; cfg.write_text(json.dumps(config, indent=2) + "\n")
    job_id = "r4-installed-launcher-positive"
    session = "ses_r4_installed_positive"
    argv = ["/bin/sleep", "3"]
    job = {"job_id": job_id, "session": session, "grant_id": "r4-positive-grant", "argv": argv}
    binding = {
        "schema": "LOCAL_COMPLETION_BINDING_V1",
        "recipient_thread": "00000000-0000-4000-8000-000000000000",
        "worktree": str(repo / "work"),
        "session": session,
        "state_root": str(repo / "controller-state"),
        "codex_binary": "/usr/bin/true",
        "notify": False,
        "grant": {"id": "r4-positive-grant", "scope": "R4 POSITIVE TEST ONLY",
                  "expires_utc": "2099-01-01T00:00:00+00:00",
                  "job_ids": [job_id], "argv_sha256": digest_argv(argv)},
        "sorok_currentness": {
            "runtime_script": str(REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"),
            "config_path": str(cfg),
            "python": PYTHON,
            "return_filename": "return.json",
            "task_id": "AUTOMATIC_CURRENTNESS_R1",
            "role": "IMPLEMENTER",
            "expected_session": session,
            "expected_source_commit": subprocess.check_output(["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip(),
            "scope": "R4 POSITIVE INSTALLED LAUNCHER TEST ONLY",
        },
    }
    bp = SCRATCH / "binding.json"; jp = SCRATCH / "job.json"
    bp.write_text(json.dumps(binding, indent=2) + "\n")
    jp.write_text(json.dumps(job, indent=2) + "\n")
    proc = subprocess.run([sys.executable, "-B", str(LAUNCHER), "--binding", str(bp),
                           "--job", str(jp)], capture_output=True, text=True, timeout=120)
    run = repo / "controller-state" / job_id
    attestation_path = run / "attestation.json"
    attestation = json.loads(attestation_path.read_text()) if attestation_path.exists() else None
    registry_path = repo / "state/trusted_launches.json"
    registry = json.loads(registry_path.read_text()) if registry_path.exists() else {}
    entry = next(iter(registry.get("entries", {}).values()), None)
    report = {
        "schema": "SOROK_AUTOMATIC_CURRENTNESS_R4_INSTALLED_LAUNCHER_POSITIVE@1",
        "launcher_path": str(LAUNCHER),
        "launcher_sha256": hashlib.sha256(LAUNCHER.read_bytes()).hexdigest(),
        "launch_exit": proc.returncode,
        "launch_stdout": proc.stdout,
        "launch_stderr": proc.stderr,
        "attestation": attestation,
        "registry_entry": ({key: entry.get(key) for key in (
            "provenance", "role", "task_id", "session", "expected_session",
            "run_dir", "launcher_path", "launcher_sha256", "authorization",
            "migration")} if entry else None),
        "positive": bool(
            proc.returncode == 0 and attestation
            and attestation.get("exit_code") == 0
            and entry
            and entry.get("provenance") == "TRUSTED_LAUNCHER_ATTESTATION"
            and entry.get("launcher_sha256") == hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
            and entry.get("session") == session
            and entry.get("expected_session") == session),
        "verdict": "PASS" if (
            proc.returncode == 0 and attestation
            and attestation.get("exit_code") == 0
            and entry
            and entry.get("provenance") == "TRUSTED_LAUNCHER_ATTESTATION"
            and entry.get("launcher_sha256") == hashlib.sha256(LAUNCHER.read_bytes()).hexdigest()
            and entry.get("session") == session
            and entry.get("expected_session") == session) else "GAP",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"launch_exit": proc.returncode,
                      "attestation_exit": attestation.get("exit_code") if attestation else None,
                      "provenance": entry.get("provenance") if entry else None,
                      "verdict": report["verdict"]}, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
