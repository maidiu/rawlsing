#!/usr/bin/env python3
"""WG0P10 BEFORE harness — reproduces D1..D5 exactly as they fail as published.

Uses the SAME environment variables and pytest invocation as
`wg0p8_publication.py:run_suites`, but bypasses the `probe_import()` gate so the
frozen suites can be observed even while D1 blocks the shipped runner.

Frozen test sources are never edited, xfailed or skipped.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Runs against EITHER the pristine WG0P8 return (BEFORE) or this return's
# derived candidate (AFTER); the target is supplied via WG0P_RET.
RET = Path(os.environ["WG0P_RET"]).resolve()
ROOT = RET.parent.parent
C = RET / "candidate"
COURT = C / "court"
P5 = COURT / "runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py"

# Paths mirror wg0p8_publication.py:REVIEW / SUITES exactly.
REVIEW = RET / "reviewer_frozen" / "02_WG0P7_STAGED" / "reviewer"
SUITES = {
    "wg0o17": [REVIEW / "tests/test_authority_seam_court.py"],
    "wg0q36": [REVIEW / "tests/test_authority_body_delta_court.py"],
    "wg0m33": [COURT / "tests/test_descriptor_delta_frozen.py"],
    "original65": [COURT / "tests/test_precommitted_phase_b.py"],
    "original3": [COURT / "tests/p5_mapping/test_original_three_adapter_v1.py"],
    "j44_k11": [COURT / "tests/phase_b/test_original_j_adapter_v1.py",
                COURT / "tests/phase_b/test_original_k_adapter_v1.py"],
    "owners80": [COURT / "runtime_phase_b/owner_tests"],
    "fresh42": [C / "tests/test_source_view_binding.py"],
    "cold_pointer": [C / "tests/test_cold_pointer_process.py"],
}


def suite_env():
    # Reproduces the published invocation contract exactly (see candidate/court/
    # 02_ACTUAL_EXECUTION_OR_TYPED_HOLD.json and repro/run_court.py).
    return dict(os.environ,
                PYTHONDONTWRITEBYTECODE="1",
                PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
                PYTHONPATH=os.pathsep.join([str(COURT / "bootstrap_p6"), str(COURT / "repro")]),
                WG0O_WG0N_ROOT=str(RET / "reviewer_frozen" / "03_INHERITED" / "WG0N"),
                WG0L_PHASE_B_ADAPTER="phase_b_adapter_v1",
                WG0M_RUN="phase_b_P5")


def run_suite(name, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-B", "-m", "pytest",
           "-c", str(COURT / "runtime_phase_b/candidate/pytest.ini"),
           "-q", "--tb=line", f"--junitxml={outdir / (name + '.xml')}",
           *map(str, SUITES[name])]
    p = subprocess.run(cmd, cwd=COURT, env=suite_env(),
                       capture_output=True, text=True)
    (outdir / (name + ".stdout")).write_text(p.stdout + "\n--- STDERR ---\n" + p.stderr)
    tail = [l for l in p.stdout.splitlines() if l.strip()][-1] if p.stdout.strip() else ""
    return dict(suite=name, exit=p.returncode, tail=tail,
                cmd=" ".join(cmd), cwd=str(COURT))


def probe_import_state():
    """The D1 assertion in isolation, without the verify() gate."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
               PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
               PYTHONPATH=os.pathsep.join([str(COURT / "bootstrap_p6"), str(COURT / "repro")]))
    code = ("import wg0p4_workload as m,pathlib;"
            "print(m.VERSION);"
            "print(pathlib.Path(m.__file__).resolve())")
    p = subprocess.run([sys.executable, "-B", "-c", code], cwd=COURT,
                       env=env, capture_output=True, text=True)
    lines = [l for l in p.stdout.splitlines() if l.strip()]
    return dict(exit=p.returncode, observed_version=lines[0] if lines else None,
                observed_path=lines[1] if len(lines) > 1 else None,
                expected_by_probe="WG0P4_NATIVE_FRONTIER_COLD@1",
                p5_path=str(P5), match=(lines[1] if len(lines) > 1 else None) == str(P5))


def bootstrap_receipt_state():
    """D2: does the atexit import-audit receipt actually get emitted?"""
    target = C / "observations" / "imports"
    if target.exists():
        import shutil
        shutil.rmtree(target)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
               PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
               PYTHONPATH=os.pathsep.join([str(COURT / "bootstrap_p6"), str(COURT / "repro")]))
    p = subprocess.run([sys.executable, "-B", "-c", "import wg0p4_workload"],
                       cwd=COURT, env=env, capture_output=True, text=True)
    emitted = sorted(str(x.relative_to(C)) for x in target.rglob("*")) if target.exists() else []
    return dict(exit=p.returncode, receipt_dir_exists=target.exists(),
                emitted_files=emitted,
                stderr_tail=p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "")


def scaffold_state():
    """D3: are the two directories versioned in the published tree?"""
    return dict(
        candidate_observations_present=(C / "observations").is_dir(),
        candidate_runtime_present=(C / "runtime").is_dir(),
        fresh42_result=(C / "observations" / "fresh_process_source_pointer_refusal.json").exists())


def cold_state():
    """D4: what does cold_comparison.json point at, and does owner/ exist?"""
    cmp_path = C / "court/observations/phase_b/inherited_v1/observations/cold_comparison.json"
    summary = json.loads(cmp_path.read_text())
    cd = summary.get("cold_directory", "")
    owner = Path(cd.replace("<WORKTREE>", str(ROOT.parents[3]))) / "owner"
    return dict(cold_directory_literal=cd,
                has_placeholder="<WORKTREE>" in cd,
                resolves_as_literal=Path(cd).exists(),
                expected_owner_dir=str(owner),
                owner_present=owner.is_dir(),
                crash_json_present=(Path(cd.replace("<WORKTREE>", str(ROOT.parents[3]))) / "crash.json").exists())


def wg0n_state():
    """D5: is the inherited WG0N Phase B verdict present?"""
    f = RET / "reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md"
    return dict(present=f.exists(), path=str(f),
                expected_sha256="839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b")


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "before"
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else (HERE / mode)
    outdir.mkdir(parents=True, exist_ok=True)

    report = {
        "mode": mode,
        "D1_probe_import": probe_import_state(),
        "D2_bootstrap_receipt": bootstrap_receipt_state(),
        "D3_scaffold": scaffold_state(),
        "D4_cold": cold_state(),
        "D5_wg0n": wg0n_state(),
        "suites": [],
    }
    for name in sys.argv[3:] or list(SUITES):
        if name not in SUITES:
            continue
        r = run_suite(name, outdir)
        report["suites"].append(r)
        print(f"{name:16s} exit={r['exit']}  {r['tail'][:80]}")

    (outdir / f"{mode}_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "suites"}, indent=2)[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
