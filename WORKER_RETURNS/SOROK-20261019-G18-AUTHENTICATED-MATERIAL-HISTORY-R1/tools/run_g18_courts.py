#!/usr/bin/env python3
"""Run the complete G18 court: frozen baselines, repaired candidate, proof faults.

This runner is deliberately plain: staged copies of the frozen test/source trees,
real subprocess pytest runs, cold replay, and exact JUnit/JSON receipts. It never
edits a frozen test or the authored candidate. Runnable from any host checkout of
this return.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
CAND = RETURN / "candidate"
C9 = RETURN / "c9_handoff_consumer.py"
STAGE = RETURN / "stage"
RUNTIME = RETURN / "runtime"
EVID = RETURN / "evidence"
JUNIT = EVID / "junit"
LOGS = EVID / "logs"
PROOF_GATE = RETURN / "tools/proof_integrity_gate_r1.py"
ORACLE = RETURN / "tests/reviewer_oracle/test_g17i_independent.py"
ORACLE_SHA256 = "0e4535a708d83a85d763c592f3d206f0b21dbc599846d7ffcd89cd82f145a5e6"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
           PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
COUNTS = {}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()


def clean(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_candidate(dst: Path, source: Path = CAND):
    shutil.copytree(source, dst / "candidate", ignore=IGNORE)
    shutil.copyfile(C9, dst / "c9_handoff_consumer.py")


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


def run_pytest(label, cwd: Path, node: str, env_extra=None, expect=None):
    xml = JUNIT / f"{label}.xml"
    cmd = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--tb=short", node, "--junitxml=" + str(xml)]
    started = time.monotonic()
    proc = subprocess.run(cmd, cwd=str(cwd), env=dict(ENV, **(env_extra or {})),
                          capture_output=True, text=True)
    text = (proc.stdout + proc.stderr).replace(str(REPO), "$WORKTREE")
    (LOGS / f"{label}.txt").write_text(text)
    counts, cases = parse_junit(xml)
    portable_cmd = [x.replace(str(REPO), "$WORKTREE") for x in cmd]
    row = dict(label=label, node=node, cwd=str(cwd).replace(str(REPO), "$WORKTREE"),
               command=portable_cmd, exit=proc.returncode,
               seconds=round(time.monotonic() - started, 3), counts=counts,
               cases=cases, junit=str(xml.relative_to(RETURN)))
    COUNTS[label] = counts
    print(label, proc.returncode, counts, flush=True)
    if expect is not None:
        assert (counts["PASS"], counts["RED"], counts["ERROR"], counts["SKIP"]) == expect, (
            label, counts, text[-2500:])
    return row, proc


def stage_181():
    dst = RUNTIME / "g181"
    clean(dst)
    shutil.copyfile(STAGE / "g15_repro/court_runner.py", dst / "court_runner.py")
    shutil.copytree(STAGE / "g15_repro/frozen", dst / "frozen", ignore=IGNORE)
    copy_candidate(dst, CAND)
    shutil.copyfile(STAGE / "g15_repro/frozen/g14/test_g14_science.py",
                    dst / "test_g14_science.py")
    return dst


def run_181():
    dst = stage_181()
    proc = subprocess.run([sys.executable, "-B", "court_runner.py", "candidate"],
                          cwd=str(dst), env=ENV, capture_output=True, text=True)
    (LOGS / "g13_181_runner.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(REPO), "$WORKTREE"))
    results = json.loads((dst / "execution/candidate/results.json").read_text())
    suites = {}
    for row in results:
        label = row["suite"]
        suites[label] = dict(counts=row["counts"], cases=row["cases"], exit=row["exit"])
        src = dst / row["junit"]
        shutil.copyfile(src, JUNIT / f"g13_181_{label}.xml")
    court = {k: v for k, v in suites.items() if k != "g14_science"}
    g13_counts = {s: sum(v["counts"][s] for v in court.values())
                  for s in ("PASS", "RED", "ERROR", "SKIP")}
    g14_counts = suites["g14_science"]["counts"]
    assert (g13_counts["PASS"], g13_counts["RED"]) == (108, 73), g13_counts
    assert (g14_counts["PASS"], g14_counts["RED"]) == (67, 0), g14_counts
    COUNTS["g13_181"] = g13_counts
    COUNTS["g14_67"] = g14_counts
    return dict(
        g13_181=dict(counts=g13_counts, suites=suites, exit=proc.returncode,
                     red_ids=[(c.get("classname", "") + "::" + c.get("name", ""))
                              for v in court.values()
                              for c in v["cases"] if c["status"] == "RED"]),
        g14_67=dict(counts=g14_counts, cases=suites["g14_science"]["cases"]),
    )


def run_g15():
    dst = RUNTIME / "g15"
    clean(dst)
    shutil.copyfile(STAGE / "g15_repro/test_g15_causal.py",
                    dst / "test_g15_causal.py")
    copy_candidate(dst, CAND)
    row, _ = run_pytest("g15_75", dst, "test_g15_causal.py",
                        expect=(75, 0, 0, 0))
    shutil.copyfile(dst / "execution/prospective_observations.json",
                    EVID / "g15_prospective_observations.json")
    return row


def run_g16i(label, candidate: Path, expect):
    dst = RUNTIME / label
    clean(dst)
    shutil.copyfile(STAGE / "g16i/test_g16i_science.py", dst / "test_g16i_science.py")
    (dst / "sandbox").mkdir(parents=True, exist_ok=True)
    shutil.copytree(candidate, dst / "sandbox/candidate", ignore=IGNORE)
    row, _ = run_pytest(label, dst, "test_g16i_science.py",
                        env_extra=dict(G16I_OBSERVATIONS=str(dst / "observations.json")),
                        expect=expect)
    full = dst / "observations.json"
    data = json.loads(full.read_text())
    observations = {}
    for key, value in sorted(data.get("observations", {}).items()):
        encoded = json.dumps(value, sort_keys=True, default=str)
        observations[key] = dict(
            sha256=hashlib.sha256(encoded.encode()).hexdigest(),
            bytes=len(encoded),
            type=type(value).__name__,
            top_keys=sorted(value)[:20] if isinstance(value, dict) else None,
        )
    summary = dict(
        schema="SOROK_G18_G16I_OBSERVATION_SUMMARY@1",
        label=label,
        full_observation_sha256=sha256(full),
        full_observation_bytes=full.stat().st_size,
        imports=data.get("imports"),
        network_attempts=data.get("network_attempts"),
        observations=observations,
        note=("Full observation JSON is retained under the gitignored runtime/ "
              "directory; this summary and the JUnit bind the executed run."),
    )
    (EVID / f"{label}_observations_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return row


def run_g17(label, candidate: Path, expect):
    dst = RUNTIME / label
    clean(dst)
    (dst / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RETURN / "tests/test_g17_material_history_consumer.py",
                    dst / "tests/test_g17_material_history_consumer.py")
    shutil.copytree(candidate, dst / "candidate", ignore=IGNORE)
    shutil.copyfile(RETURN / "stage/g17_baseline_candidate/c9_handoff_consumer.py"
                    if candidate != CAND else C9,
                    dst / "c9_handoff_consumer.py")
    row, _ = run_pytest(label, dst, "tests/test_g17_material_history_consumer.py",
                        expect=expect)
    return row


def run_g17i(label, candidate: Path, expect):
    dst = RUNTIME / label
    clean(dst)
    (dst / "tests").mkdir(parents=True, exist_ok=True)
    (dst / "target_candidate").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ORACLE, dst / "tests/test_g17i_independent.py")
    shutil.copytree(candidate, dst / "target_candidate/candidate", ignore=IGNORE)
    shutil.copyfile(
        RETURN / "stage/g17_baseline_candidate/c9_handoff_consumer.py"
        if candidate != CAND else C9,
        dst / "target_candidate/c9_handoff_consumer.py")
    assert sha256(dst / "tests/test_g17i_independent.py") == ORACLE_SHA256
    row, _ = run_pytest(label, dst, "tests/test_g17i_independent.py",
                        expect=expect)
    return row


def run_g18(expect=(20, 0, 0, 0)):
    row, _ = run_pytest("g18_20", RETURN, "tests/test_g18_authenticated_material.py",
                        expect=expect)
    return row


def proof_gate():
    receipts = {}
    for label, contract, claims in (
            ("g17", RETURN / "tests/test_g17_material_history_consumer.py.proof.json", 7),
            ("g18", RETURN / "tests/test_g18_authenticated_material.py.proof.json", 7)):
        proc = subprocess.run(
            [sys.executable, "-B", str(PROOF_GATE), "witness", str(contract),
             "--root", str(REPO)], cwd=str(REPO),
            env=ENV, capture_output=True, text=True)
        (LOGS / f"proof_witness_{label}.txt").write_text(
            (proc.stdout + proc.stderr).replace(str(REPO), "$WORKTREE"))
        assert proc.returncode == 0, (label, proc.stdout, proc.stderr)
        payload = json.loads(proc.stdout)
        assert payload["status"] == "MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION"
        assert len(payload["claims"]) == claims
        (EVID / f"proof_witness_{label}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n")
        receipts[label] = payload
    return receipts


def cold_replay():
    dst = RUNTIME / "cold_replay"
    clean(dst)
    first, replay, tampered, tamper_out = (dst / "first.json", dst / "replay.json",
                                           dst / "tampered.json", dst / "tamper_out.json")
    cmd = [sys.executable, "-B", str(CAND / "run_candidate.py")]
    p1 = subprocess.run(cmd + ["--output", str(first)], cwd=str(REPO),
                        env=ENV, capture_output=True, text=True)
    p2 = subprocess.run(cmd + ["--replay", str(first), "--output", str(replay)],
                        cwd=str(REPO), env=ENV, capture_output=True, text=True)
    packet = json.loads(first.read_text())
    packet["frozen_inputs"]["joint_material_opportunity"]["payment_per_actor"] = 100000
    tampered.write_text(json.dumps(packet))
    p3 = subprocess.run(cmd + ["--replay", str(tampered), "--output", str(tamper_out)],
                        cwd=str(REPO), env=ENV, capture_output=True, text=True)
    saved, replayed, bad = (json.loads(first.read_text()),
                            json.loads(replay.read_text()),
                            json.loads(tamper_out.read_text()))
    assert p1.returncode == 0 and p2.returncode == 0 and p3.returncode == 1
    assert replayed["complete_causal_record_equal"] is True
    assert bad["complete_causal_record_equal"] is False
    assert saved["result"]["terminal"]["status"] == "COMMITTED"
    assert bad["result"]["terminal"]["status"] == "UNAUTHENTICATED_MATERIAL_SOURCE"
    receipt = dict(
        schema="SOROK_G18_COLD_REPLAY@1",
        positive_processes=[p1.returncode, p2.returncode],
        tamper_process=p3.returncode,
        positive_terminal=saved["result"]["terminal"]["status"],
        replayed_equal=replayed["complete_causal_record_equal"],
        tampered_equal=bad["complete_causal_record_equal"],
        tampered_terminal=bad["result"]["terminal"]["status"],
        tampered_reason=bad["result"]["terminal"]["reason"],
        stdout=[p1.stdout.strip(), p2.stdout.strip(), p3.stdout.strip()],
    )
    (EVID / "cold_replay.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def two_actor():
    proc = subprocess.run([sys.executable, "-B", str(RETURN / "tools/two_actor_contrast.py")],
                          cwd=str(RETURN), env=ENV, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    receipt = json.loads(proc.stdout)
    assert receipt["witness"]["status"] == "WITNESSED"
    assert receipt["witness"]["material_verified"] is True
    assert all(x["accepted"] for x in receipt["witness"]["action_receipt_checks"])
    assert receipt["native_grant"] == "NOT_GRANTED"
    assert receipt["human_life_or_genealogy_claim"] is False
    (EVID / "two_actor_contrast.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def source_manifest():
    roots = [CAND, RETURN / "tests", RETURN / "tools", STAGE]
    rows = []
    for root in roots:
        for p in sorted(root.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            if p.name in {"BASELINE_SOURCE.json"}:
                continue
            rows.append(dict(path=str(p.relative_to(RETURN)),
                             sha256=sha256(p), git_blob_sha1=git_blob_sha1(p),
                             bytes=p.stat().st_size))
    rows.append(dict(path="c9_handoff_consumer.py", sha256=sha256(C9),
                     git_blob_sha1=git_blob_sha1(C9), bytes=C9.stat().st_size))
    tree = dict(
        schema="SOROK_G18_SOURCE_MANIFEST@1",
        oracle=dict(path=str(ORACLE.relative_to(RETURN)), sha256=sha256(ORACLE),
                    expected_g17i_sha256=ORACLE_SHA256),
        baseline=json.loads((STAGE / "g17_baseline_candidate/BASELINE_SOURCE.json").read_text()),
        files=rows,
        tree_hash=hashlib.sha256(
            json.dumps(sorted((r["path"], r["sha256"]) for r in rows),
                       sort_keys=True).encode()).hexdigest(),
    )
    (EVID / "source_manifest.json").write_text(
        json.dumps(tree, indent=2, sort_keys=True) + "\n")
    return dict(files=len(rows), tree_hash=tree["tree_hash"])


def environment_passport():
    import pytest
    modules = []
    sys.path.insert(0, str(CAND))
    import importlib
    for name in sorted(p.stem for p in (CAND / "lab_sgi1").glob("*.py")
                       if p.stem != "__init__"):
        m = importlib.import_module("lab_sgi1." + name)
        modules.append(dict(module="lab_sgi1." + name,
                            file=str(Path(m.__file__).relative_to(RETURN)),
                            sha256=sha256(Path(m.__file__))))
    git = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO),
                          capture_output=True, text=True).stdout.strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=str(REPO),
                            capture_output=True, text=True).stdout.strip()
    passport = dict(
        schema="SOROK_G18_ENVIRONMENT_PASSPORT@1",
        python=sys.version,
        python_executable=sys.executable,
        pytest=pytest.__version__,
        git=git,
        git_head_at_run=head,
        git_branch=branch,
        platform=platform.platform(),
        machine=platform.machine(),
        processor=platform.processor(),
        time_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        env=dict(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"),
        imported_modules=modules,
        native_authority="NOT_GRANTED",
    )
    (EVID / "environment_passport.json").write_text(
        json.dumps(passport, indent=2, sort_keys=True) + "\n")
    return passport


def bypass_before_after():
    def probe(candidate, c9):
        proc = subprocess.run(
            [sys.executable, "-B", str(RETURN / "tools/bypass_probe.py"),
             str(candidate), str(c9)], cwd=str(RETURN), env=ENV,
            capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        payload = json.loads(proc.stdout)
        for key in ("candidate_dir", "c9_dir"):
            if key in payload:
                payload[key] = payload[key].replace(str(REPO), "$WORKTREE")
        return payload

    base = probe(STAGE / "g17_baseline_candidate/candidate", STAGE / "g17_baseline_candidate")
    fixed = probe(CAND, RETURN)
    out = dict(
        schema="SOROK_G18_G17I_BYPASS_BEFORE_AFTER@1",
        oracle=dict(path="tests/reviewer_oracle/test_g17i_independent.py",
                    sha256=ORACLE_SHA256,
                    origin_commit="156b84cc8481b65c4196b42574010eb7920d6f44",
                    unmodified=True),
        baseline=dict(source_commit="90d0eb7925de54635559a879ee76fc1b97b9ff61",
                      candidate="stage/g17_baseline_candidate/candidate",
                      result=base),
        repaired=dict(candidate="candidate", result=fixed),
        per_bypass=[
            dict(id="FORGED_MATERIAL_100058",
                 test="test_forged_material_event_supplying_cash_must_be_refused",
                 before=("continue_person accepted the forged source and returned "
                         "cash 100058"),
                 after="continue_person returned None; material receipt refused",
                 before_status=base["forged_material_cash"]["status"],
                 before_cash=base["forged_material_cash"]["continuation_cash"],
                 after_status=fixed["forged_material_cash"]["status"],
                 after_cash=fixed["forged_material_cash"]["continuation_cash"]),
            dict(id="NESTED_FUTURE_CHILD_COMMITTED",
                 test="test_future_child_nested_alias_must_be_refused",
                 before="nested joint_material_opportunity.metadata produced COMMITTED",
                 after=("recursive partition scan refuses before any proposal/"
                        "selection/construction"),
                 before_status=base["nested_future_child"]["status"],
                 after_status=fixed["nested_future_child"]["status"]),
            dict(id="C9_FORGED_MATERIAL_100055",
                 test="test_c9_forged_material_event_must_be_refused",
                 before="C9.receive_handoff accepted the forged source with cash 100055",
                 after="C9.build_handoff refuses the unauthenticated material source",
                 before_status=base["c9_fabricated_cash"]["status"],
                 before_cash=base["c9_fabricated_cash"]["received_cash"],
                 after_status=fixed["c9_fabricated_cash"]["status"],
                 after_refusal=fixed["c9_fabricated_cash"].get("refusal")),
        ],
        conclusion=("All three independent alternate-interface bypasses are closed; "
                    "the genuine positive paths and the exact 181/67/75/13 matrices "
                    "survive."),
        native_authority="NOT_GRANTED",
    )
    (EVID / "g17i_bypass_before_after.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


def legacy_schedule_supersession():
    code = r'''
import json
from copy import deepcopy
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.history import PersonHistoryBuilder
from lab_sgi1.joint import (material_joint_opportunity, observe_joint_actions,
                            verify_material_source)
from lab_sgi1.core import h_obj
m = material_joint_opportunity(); m["payment_per_actor"] = 7; m["task_hours"] = 2
m["event_id"] = h_obj({k: v for k, v in m.items() if k != "event_id"})
a = build_mother_checkpoint("FIX_M0", "M0").anchor_dict()
e = PersonHistoryBuilder("G16I_ADULT", "G16I_SEED").build()
ok, reason, payload = verify_material_source(m)
w = observe_joint_actions(a, e, m)
print(json.dumps(dict(
    schema="SOROK_G18_LEGACY_SCHEDULE_SUPERSESSION@1",
    frozen_test="test_variable_task_cost_reaches_continued_context",
    frozen_test_behavior=("mutates payment_per_actor=7 task_hours=2 after issuance "
                          "and recomputes only the public event_id"),
    strict_material_verify=dict(accepted=ok, reason=reason),
    strict_joint_witness=dict(status=w["status"],
                             action_statuses=[x["status"] for x in w["actions"]]),
    superseded_interface=True,
    same_science_authenticated_path=dict(
        test="test_source_issued_variable_schedule_reaches_continued_context",
        issuer="material_joint_opportunity(payment_per_actor=7, task_hours=2)",
        expected_effect=("cash +7, free_hours -2, continued context cash_after "
                         "= before.cash + 11")),
    conclusion=("strict candidate refuses caller-mutated schedule; the identical "
                "scientific effect is proved through the source-issued schedule API"),
    native_grant="NOT_GRANTED"), indent=2, sort_keys=True))
'''
    env = dict(ENV, PYTHONPATH=str(CAND))
    proc = subprocess.run([sys.executable, "-B", "-c", code], cwd=str(RETURN),
                          env=env, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    (EVID / "legacy_schedule_supersession.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def red_identity_comparison(matrix):
    oracle = json.loads((STAGE / "g17i_oracle/preserved_red_ids.json").read_text())
    ours = set(matrix["g13_181"]["g13_181"]["red_ids"])
    preserved = set(oracle["red_ids"])
    compat = set(oracle["compatibility_56_ids"])
    original = set(oracle["original_17_ids"])
    out = dict(
        schema="SOROK_G18_RED_IDENTITY_COMPARISON@1",
        g13_total=len(ours),
        preserved_total=len(preserved),
        exact_set_equal=ours == preserved,
        missing_from_g18=sorted(preserved - ours),
        extra_in_g18=sorted(ours - preserved),
        compatibility_56=dict(count=len(compat), all_present=compat <= ours),
        original_17=dict(count=len(original), all_present=original <= ours),
        union_equals_73=(compat | original) == ours,
        source=("stage/g17i_oracle/preserved_red_ids.json from G17I "
                "156b84cc8481b65c4196b42574010eb7920d6f44"),
        red_ids=sorted(ours),
    )
    assert out["exact_set_equal"] is True
    assert out["compatibility_56"]["all_present"] is True
    assert out["original_17"]["all_present"] is True
    assert out["union_equals_73"] is True
    (EVID / "red_identity_comparison.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


def main():
    clean(RUNTIME)
    clean(EVID)
    JUNIT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    matrix = {}
    matrix["g13_181"] = run_181()
    matrix["g15_75"] = run_g15()
    matrix["g16i_24_baseline"] = run_g16i(
        "g16i_24_baseline", STAGE / "g17_baseline_candidate/candidate",
        expect=(22, 2, 0, 0))
    matrix["g16i_24_strict"] = run_g16i(
        "g16i_24_strict", CAND, expect=(21, 3, 0, 0))
    matrix["g17_13_baseline"] = run_g17(
        "g17_13_baseline", STAGE / "g17_baseline_candidate/candidate",
        expect=(13, 0, 0, 0))
    matrix["g17_13"] = run_g17("g17_13", CAND, expect=(13, 0, 0, 0))
    matrix["g17i_14_baseline"] = run_g17i(
        "g17i_14_baseline", STAGE / "g17_baseline_candidate/candidate",
        expect=(11, 3, 0, 0))
    matrix["g17i_14"] = run_g17i("g17i_14", CAND, expect=(14, 0, 0, 0))
    matrix["g18_20"] = run_g18()

    g17_baseline_reds = [c["name"] for c in matrix["g17i_14_baseline"]["cases"]
                         if c["status"] == "RED"]
    assert g17_baseline_reds == [
        "test_forged_material_event_supplying_cash_must_be_refused",
        "test_future_child_nested_alias_must_be_refused",
        "test_c9_forged_material_event_must_be_refused"], g17_baseline_reds
    g16i_strict_reds = [c["name"] for c in matrix["g16i_24_strict"]["cases"]
                        if c["status"] == "RED"]
    assert sorted(g16i_strict_reds) == sorted([
        "test_archived_m2_can_continue_legitimate_prior_life",
        "test_known_counterpart_has_positive_history_reuse_path",
        "test_variable_task_cost_reaches_continued_context"]), g16i_strict_reds
    g16i_baseline_reds = [c["name"] for c in matrix["g16i_24_baseline"]["cases"]
                          if c["status"] == "RED"]
    assert sorted(g16i_baseline_reds) == sorted([
        "test_archived_m2_can_continue_legitimate_prior_life",
        "test_known_counterpart_has_positive_history_reuse_path"])

    passport = environment_passport()
    manifest = source_manifest()
    red_ids = red_identity_comparison(matrix)
    cold = cold_replay()
    two = two_actor()
    bypass = bypass_before_after()
    legacy = legacy_schedule_supersession()
    hold_evidence = subprocess.run(
        [sys.executable, "-B", str(RETURN / "tools/write_hold_evidence.py")],
        cwd=str(RETURN), env=ENV, capture_output=True, text=True)
    assert hold_evidence.returncode == 0, hold_evidence.stderr

    fault_paths = set()
    for contract in (RETURN / "tests/test_g17_material_history_consumer.py.proof.json",
                     RETURN / "tests/test_g18_authenticated_material.py.proof.json"):
        for claim in json.loads(contract.read_text())["claims"]:
            fault_paths.add(claim["fault"]["path"])
    before = {p: sha256(REPO / p) for p in sorted(fault_paths)}
    proofs = proof_gate()
    after = {p: sha256(REPO / p) for p in sorted(fault_paths)}
    assert before == after, "proof gate did not restore every mutated source"
    restoration = dict(
        schema="SOROK_G18_PROOF_SOURCE_RESTORATION@1",
        mutated_files=sorted(fault_paths),
        before=before, after=after, restored=before == after,
        claims=[c["claim_id"] for c in proofs["g17"]["claims"] + proofs["g18"]["claims"]],
    )
    (EVID / "proof_source_restoration.json").write_text(
        json.dumps(restoration, indent=2, sort_keys=True) + "\n")

    # Post-gate cold reruns: the restored candidate must still pass the two whole
    # source-authentication courts and the reviewer oracle.
    post = {}
    post["g17i_14_post_gate"] = run_pytest(
        "g17i_14_post_gate", RUNTIME / "g17i_14",
        "tests/test_g17i_independent.py", expect=(14, 0, 0, 0))[0]
    post["g18_20_post_gate"] = run_pytest(
        "g18_20_post_gate", RETURN, "tests/test_g18_authenticated_material.py",
        expect=(20, 0, 0, 0))[0]
    post["g17_13_post_gate"] = run_pytest(
        "g17_13_post_gate", RUNTIME / "g17_13",
        "tests/test_g17_material_history_consumer.py", expect=(13, 0, 0, 0))[0]

    receipt = dict(
        schema="SOROK_G18_COURT_MATRIX@1",
        generated_utc=passport["time_utc"],
        branch=passport["git_branch"],
        parent_head=passport["git_head_at_run"],
        matrix={k: (dict(counts=v["counts"], cases=v["cases"])
                    if isinstance(v, dict) and "counts" in v else v)
                for k, v in matrix.items()},
        g13_181=matrix["g13_181"]["g13_181"],
        g14_67=matrix["g13_181"]["g14_67"],
        red_identity=dict(exact_set_equal=red_ids["exact_set_equal"],
                          compatibility_56=red_ids["compatibility_56"],
                          original_17=red_ids["original_17"],
                          union_equals_73=red_ids["union_equals_73"]),
        g16i_24=dict(
            baseline=matrix["g16i_24_baseline"]["counts"],
            strict=matrix["g16i_24_strict"]["counts"],
            typed_coverage_holds=[
                "test_archived_m2_can_continue_legitimate_prior_life",
                "test_known_counterpart_has_positive_history_reuse_path"],
            superseded_legacy_interface=[
                "test_variable_task_cost_reaches_continued_context"],
            superseded_reason=("the frozen test mutates payment_per_actor/task_hours "
                               "after source issuance and recomputes only the public "
                               "event_id; G18 refuses that unauthenticated schedule "
                               "and proves the same science through the source-issued "
                               "variable-schedule positive"),
        ),
        g17i_14=dict(
            baseline=matrix["g17i_14_baseline"]["counts"],
            repaired=matrix["g17i_14"]["counts"],
            baseline_reds=g17_baseline_reds,
            oracle_sha256=ORACLE_SHA256,
            oracle_unmodified=True,
        ),
        post_gate=post,
        cold_replay=cold,
        g17i_bypass=bypass,
        legacy_schedule=legacy,
        two_actor=dict(
            claim=two["claim"],
            witness_status=two["witness"]["status"],
            performed_units=two["continuation"]["performed_units"],
            after_completed_units=two["continuation"]["after_completed_units"],
            lawful_no_change_alternative=two["lawful_no_change_alternative"],
            native_grant=two["native_grant"],
        ),
        source_manifest=manifest,
        environment=dict(python=passport["python"], pytest=passport["pytest"],
                         git=passport["git"], platform=passport["platform"]),
        native_authority="NOT_GRANTED",
        adoption="NOT_SELF_ADOPTED",
    )
    (EVID / "court_matrix.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("MATRIX", json.dumps({k: v["counts"] for k, v in matrix.items()
                                if isinstance(v, dict) and "counts" in v},
                               sort_keys=True))
    print("PROOF", {k: len(v["claims"]) for k, v in proofs.items()})
    print("COLD", cold["positive_terminal"], cold["tampered_terminal"])
    print("TWO_ACTOR", two["continuation"]["performed_units"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
