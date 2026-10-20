#!/usr/bin/env python3
"""Run the inherited G18 courts against the exact vendored G18 candidate.

This is preservation evidence for BP1: the G18 source-issued material/action
receipt boundary and the historical 73 RED identities must not regress when the
new historical actor composer is added alongside them. The vendored G18 files
are byte-identical copies; this runner stages them, never edits them.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
G18 = RETURN / "vendor" / "g18"
CAND = G18 / "candidate"
C9 = G18 / "c9_handoff_consumer.py"
STAGE = G18 / "stage"
RUNTIME = RETURN / "runtime" / "g18_regression"
EVID = RETURN / "evidence" / "g18_regression"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
           PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def clean(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_candidate(dst: Path, source: Path = CAND, c9: Path = C9):
    shutil.copytree(source, dst / "candidate", ignore=IGNORE)
    shutil.copyfile(c9, dst / "c9_handoff_consumer.py")


def parse_junit(path: Path):
    cases = []
    if not path.exists():
        return dict(PASS=0, RED=0, ERROR=0, SKIP=0), cases
    root = ET.parse(path).getroot()
    for c in root.iter("testcase"):
        if c.find("failure") is not None:
            status = "RED"
        elif c.find("error") is not None:
            status = "ERROR"
        elif c.find("skipped") is not None:
            status = "SKIP"
        else:
            status = "PASS"
        cases.append(dict(
            id=c.get("classname", "") + "::" + c.get("name", ""),
            name=c.get("name"), status=status))
    counts = {s: sum(c["status"] == s for c in cases)
              for s in ("PASS", "RED", "ERROR", "SKIP")}
    return counts, cases


def run(label, cwd: Path, node: str, expect, env_extra=None):
    EVID.mkdir(parents=True, exist_ok=True)
    xml = EVID / f"{label}.xml"
    cmd = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--tb=short", node, "--junitxml=" + str(xml)]
    proc = subprocess.run(cmd, cwd=str(cwd), env=dict(ENV, **(env_extra or {})),
                          capture_output=True, text=True)
    (EVID / f"{label}.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(RETURN), "$RETURN"))
    counts, cases = parse_junit(xml)
    assert (counts["PASS"], counts["RED"], counts["ERROR"], counts["SKIP"]) == expect, (
        label, counts, (proc.stdout + proc.stderr)[-2500:])
    print(label, counts, flush=True)
    return dict(label=label, counts=counts, cases=cases, exit=proc.returncode,
                junit=str(xml.relative_to(RETURN)))


def stage_main():
    dst = RUNTIME / "main"
    clean(dst)
    (dst / "tests" / "reviewer_oracle").mkdir(parents=True, exist_ok=True)
    copy_candidate(dst)
    shutil.copyfile(G18 / "tests/test_g17_material_history_consumer.py",
                    dst / "tests/test_g17_material_history_consumer.py")
    shutil.copyfile(G18 / "tests/test_g18_authenticated_material.py",
                    dst / "tests/test_g18_authenticated_material.py")
    shutil.copyfile(G18 / "tests/reviewer_oracle/test_g17i_independent.py",
                    dst / "tests/reviewer_oracle/test_g17i_independent.py")
    return dst


def stage_oracle(dst: Path, candidate: Path, c9: Path):
    clean(dst)
    (dst / "tests").mkdir(parents=True, exist_ok=True)
    (dst / "target_candidate").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(G18 / "tests/reviewer_oracle/test_g17i_independent.py",
                    dst / "tests/test_g17i_independent.py")
    shutil.copytree(candidate, dst / "target_candidate/candidate", ignore=IGNORE)
    shutil.copyfile(c9, dst / "target_candidate/c9_handoff_consumer.py")
    return dst


def stage_g17(dst: Path, candidate: Path, c9: Path):
    clean(dst)
    (dst / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(G18 / "tests/test_g17_material_history_consumer.py",
                    dst / "tests/test_g17_material_history_consumer.py")
    shutil.copytree(candidate, dst / "candidate", ignore=IGNORE)
    shutil.copyfile(c9, dst / "c9_handoff_consumer.py")
    return dst


def run_181():
    dst = RUNTIME / "g181"
    clean(dst)
    shutil.copyfile(STAGE / "court_runner.py", dst / "court_runner.py")
    shutil.copytree(STAGE / "frozen", dst / "frozen", ignore=IGNORE)
    copy_candidate(dst)
    shutil.copyfile(STAGE / "frozen/g14/test_g14_science.py",
                    dst / "test_g14_science.py")
    proc = subprocess.run([sys.executable, "-B", "court_runner.py", "candidate"],
                          cwd=str(dst), env=ENV, capture_output=True, text=True)
    (EVID / "g181_runner.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(RETURN), "$RETURN"))
    results = json.loads((dst / "execution/candidate/results.json").read_text())
    suites = {}
    for row in results:
        suites[row["suite"]] = dict(counts=row["counts"], cases=row["cases"])
        shutil.copyfile(dst / row["junit"],
                        EVID / f"g13_181_{row['suite']}.xml")
    court = {k: v for k, v in suites.items() if k != "g14_science"}
    g13 = {s: sum(v["counts"][s] for v in court.values())
           for s in ("PASS", "RED", "ERROR", "SKIP")}
    g14 = suites["g14_science"]["counts"]
    assert (g13["PASS"], g13["RED"]) == (108, 73), g13
    assert (g14["PASS"], g14["RED"]) == (67, 0), g14
    red_ids = sorted(c.get("classname", "") + "::" + c.get("name", "")
                     for v in court.values() for c in v["cases"]
                     if c["status"] == "RED")
    return dict(g13_counts=g13, g14_counts=g14, g13_red_ids=red_ids,
                suites=suites)


def run_g15():
    dst = RUNTIME / "g15"
    clean(dst)
    shutil.copyfile(STAGE / "test_g15_causal.py", dst / "test_g15_causal.py")
    copy_candidate(dst)
    return run("g15_75", dst, "test_g15_causal.py", (75, 0, 0, 0))


def run_g16i(label: str, candidate: Path, expect):
    dst = RUNTIME / label
    clean(dst)
    shutil.copyfile(STAGE / "test_g16i_science.py", dst / "test_g16i_science.py")
    (dst / "sandbox").mkdir(parents=True, exist_ok=True)
    shutil.copytree(candidate, dst / "sandbox/candidate", ignore=IGNORE)
    return run(label, dst, "test_g16i_science.py", expect,
               env_extra=dict(G16I_OBSERVATIONS=str(dst / "observations.json")))


def main():
    clean(RUNTIME)
    clean(EVID)
    main_stage = stage_main()
    g17 = run("g17_13", main_stage, "tests/test_g17_material_history_consumer.py",
              (13, 0, 0, 0))
    g18 = run("g18_20", main_stage, "tests/test_g18_authenticated_material.py",
              (20, 0, 0, 0))
    oracle_main = stage_oracle(RUNTIME / "oracle_main", CAND, C9)
    g17i = run("g17i_14", oracle_main, "tests/test_g17i_independent.py",
               (14, 0, 0, 0))

    baseline = STAGE / "g17_baseline_candidate"
    g17b = run("g17_13_baseline",
               stage_g17(RUNTIME / "g17_baseline", baseline / "candidate",
                         baseline / "c9_handoff_consumer.py"),
               "tests/test_g17_material_history_consumer.py", (13, 0, 0, 0))
    oracle_baseline = stage_oracle(RUNTIME / "oracle_baseline",
                                   baseline / "candidate",
                                   baseline / "c9_handoff_consumer.py")
    g17ib = run("g17i_14_baseline", oracle_baseline,
                "tests/test_g17i_independent.py", (11, 3, 0, 0))
    g16ib = run_g16i("g16i_24_baseline", baseline / "candidate", (22, 2, 0, 0))
    g16i = run_g16i("g16i_24_strict", CAND, (21, 3, 0, 0))
    g181 = run_181()
    g15 = run_g15()

    preserved = json.loads(
        (STAGE / "g17i_oracle/preserved_red_ids.json").read_text())
    ours = set(g181["g13_red_ids"])
    exact = ours == set(preserved["red_ids"])
    compat = set(preserved["compatibility_56_ids"])
    original = set(preserved["original_17_ids"])
    assert exact is True
    assert compat <= ours and original <= ours
    g17i_baseline_reds = sorted(c["name"] for c in g17ib["cases"]
                                if c["status"] == "RED")
    assert g17i_baseline_reds == [
        "test_c9_forged_material_event_must_be_refused",
        "test_forged_material_event_supplying_cash_must_be_refused",
        "test_future_child_nested_alias_must_be_refused"], g17i_baseline_reds
    g16i_strict_reds = sorted(c["name"] for c in g16i["cases"]
                              if c["status"] == "RED")
    assert g16i_strict_reds == [
        "test_archived_m2_can_continue_legitimate_prior_life",
        "test_known_counterpart_has_positive_history_reuse_path",
        "test_variable_task_cost_reaches_continued_context"], g16i_strict_reds

    receipt = dict(
        schema="BP1_G18_REGRESSION@1",
        source="G18 61713eafe0e7a5386a8f0aed4836b15f3d921ed5 vendored byte-identical",
        g13_181=dict(counts=g181["g13_counts"],
                     red_ids=g181["g13_red_ids"]),
        g14_67=dict(counts=g181["g14_counts"]),
        g15_75=dict(counts=g15["counts"]),
        g16i_24=dict(baseline=g16ib["counts"], strict=g16i["counts"],
                     typed_holds=[
                         "test_archived_m2_can_continue_legitimate_prior_life",
                         "test_known_counterpart_has_positive_history_reuse_path"],
                     documented_legacy_supersession=[
                         "test_variable_task_cost_reaches_continued_context"]),
        g17_13=dict(counts=g17["counts"]),
        g18_20=dict(counts=g18["counts"]),
        g17i_14=dict(baseline=g17ib["counts"], repaired=g17i["counts"],
                     baseline_reds=g17i_baseline_reds),
        red_identity=dict(exact_set_equal=exact,
                          compatibility_56=dict(count=len(compat),
                                                all_present=compat <= ours),
                          original_17=dict(count=len(original),
                                           all_present=original <= ours)),
        native_authority="NOT_GRANTED",
    )
    (RETURN / "evidence/g18_regression_matrix.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v["counts"] for k, v in {
        "g17": g17, "g18": g18, "g17i": g17i, "g16i": g16i,
        "g16i_baseline": g16ib, "g15": g15,
    }.items()}, sort_keys=True))
    print("g13", g181["g13_counts"], "g14", g181["g14_counts"],
          "red_exact", exact)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
