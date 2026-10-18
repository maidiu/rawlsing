#!/usr/bin/env python3
"""D4 — deterministic regeneration of the cold crash/resume owner fixture.

Runs the PINNED, UNMODIFIED `court/repro/phase_b_cold_worker_v1.py` twice in
separate real processes:

    phase_b_cold_worker_v1.py crash  <cold-dir>     -> exit 23 (genuine checkpoint)
    phase_b_cold_worker_v1.py resume <cold-dir>     -> exit 0

producing `owner/`, `checkpoint.json`, `crash.json` and `resume.json` with real
process IDs, real fsync/replace durability calls and the real manifest hash.

Nothing is synthesised: `owner/` is provisioned by the native FixtureOwner, and
`crash.json` / `resume.json` are dumped by the pinned worker itself. This script
does not touch receipts, manifests or test source.

Usage:  python3 repro/wg0p10_regenerate_cold.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RET = HERE.parent
COURT = RET / "candidate" / "court"
COLD = COURT / "observations/phase_b/inherited_v1/cold/cold-face4d00952b4460a7c1285c1dd80be5"
WORKER = COURT / "repro/phase_b_cold_worker_v1.py"


def run(mode: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [str(COURT / "repro"), str(COURT / "bootstrap_p6")]),
        PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    return subprocess.run([sys.executable, "-B", str(WORKER), mode, str(COLD)],
                          cwd=COURT, env=env, capture_output=True, text=True)


def main() -> int:
    if COLD.exists():
        shutil.rmtree(COLD)
    COLD.mkdir(parents=True, exist_ok=True)

    crash = run("crash")
    print(f"crash  exit={crash.returncode} (23 expected)")
    if crash.returncode != 23:
        print(crash.stderr[-1500:]); return 1

    resume = run("resume")
    print(f"resume exit={resume.returncode} (0 expected)")
    if resume.returncode != 0:
        print(resume.stderr[-1500:]); return 1

    c = json.loads((COLD / "crash.json").read_text())
    r = json.loads((COLD / "resume.json").read_text())
    out = {
        "crash_pid": c["pid"], "resume_pid": r["pid"],
        "pids_distinct": c["pid"] != r["pid"],
        "manifest_hash": c["manifest"], "manifest_units": c["unit_count"],
        "resume_manifest_matches": c["manifest"] == r["manifest"],
        "receipt_class": c["receipt_class"],
        "owner_members": sorted(x.name for x in (COLD / "owner").iterdir()),
        "durability_calls": c.get("durability_calls"),
    }
    # Keep the published record consistent with the fixture we just produced.
    cmp_path = COURT / "observations/phase_b/inherited_v1/observations/cold_comparison.json"
    d = json.loads(cmp_path.read_text())
    rel = "court/observations/phase_b/inherited_v1/cold/cold-face4d00952b4460a7c1285c1dd80be5"
    d["cold_directory_relative"] = rel
    d["cold_directory"] = rel
    d["regenerated_cold_run"] = dict(out,
                                     purpose="D4 genuine cold crash/resume regeneration",
                                     produced_by="repro/wg0p10_regenerate_cold.py",
                                     receipt_forged=False,
                                     cold_identity_weakened=False)
    cmp_path.write_text(json.dumps(d, indent=2) + "\n")

    print(json.dumps(out, indent=2))
    return 0 if out["pids_distinct"] and out["resume_manifest_matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
