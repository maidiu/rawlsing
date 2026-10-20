#!/usr/bin/env python3
"""Run the complete BP1 historical actor production campaign.

Stages no frozen source edits. Runs the BP1 author court, the exact vendored C9R
consumer, the exact vendored G18 regression (including the historical 73 RED
identities), the six same-edge source-fault witnesses, and a two-process cold
C4→C9 positive. Writes JUnit/JSON evidence and the environment passport.
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
EVID = RETURN / "evidence"
JUNIT = EVID / "junit"
LOGS = EVID / "logs"
RUNTIME = RETURN / "runtime"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
           PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: Path) -> str:
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()


def clean(path: Path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


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
        cases.append(dict(id=c.get("classname", "") + "::" + c.get("name", ""),
                          name=c.get("name"), status=status))
    counts = {s: sum(c["status"] == s for c in cases)
              for s in ("PASS", "RED", "ERROR", "SKIP")}
    return counts, cases


def run_pytest(label, cwd: Path, node: str, expect, env_extra=None):
    xml = JUNIT / f"{label}.xml"
    cmd = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
           "--tb=short", node, "--junitxml=" + str(xml)]
    proc = subprocess.run(cmd, cwd=str(cwd), env=dict(ENV, **(env_extra or {})),
                          capture_output=True, text=True)
    (LOGS / f"{label}.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(REPO), "$REPO"))
    counts, cases = parse_junit(xml)
    assert (counts["PASS"], counts["RED"], counts["ERROR"], counts["SKIP"]) == expect, (
        label, counts, (proc.stdout + proc.stderr)[-3000:])
    print(label, counts, flush=True)
    return dict(label=label, counts=counts, cases=cases, exit=proc.returncode,
                junit=str(xml.relative_to(RETURN)),
                command=[x.replace(str(REPO), "$REPO") for x in cmd])


def run_script(label, cmd, cwd=RETURN, expect=0):
    proc = subprocess.run(cmd, cwd=str(cwd), env=ENV,
                          capture_output=True, text=True)
    (LOGS / f"{label}.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(REPO), "$REPO"))
    assert proc.returncode == expect, (label, proc.returncode,
                                       (proc.stdout + proc.stderr)[-3000:])
    print(label, "exit", proc.returncode, flush=True)
    return proc


def g18_regression():
    proc = run_script("g18_regression", [sys.executable, "-B",
                                         "tools/run_g18_regression.py"])
    matrix = json.loads((EVID / "g18_regression_matrix.json").read_text())
    assert matrix["g13_181"]["counts"] == {"PASS": 108, "RED": 73,
                                          "ERROR": 0, "SKIP": 0}
    assert matrix["g14_67"]["counts"] == {"PASS": 67, "RED": 0,
                                          "ERROR": 0, "SKIP": 0}
    assert matrix["g15_75"]["counts"] == {"PASS": 75, "RED": 0,
                                          "ERROR": 0, "SKIP": 0}
    assert matrix["g16i_24"]["strict"] == {"PASS": 21, "RED": 3,
                                           "ERROR": 0, "SKIP": 0}
    assert matrix["g16i_24"]["baseline"] == {"PASS": 22, "RED": 2,
                                             "ERROR": 0, "SKIP": 0}
    assert matrix["g17_13"]["counts"] == {"PASS": 13, "RED": 0,
                                          "ERROR": 0, "SKIP": 0}
    assert matrix["g18_20"]["counts"] == {"PASS": 20, "RED": 0,
                                          "ERROR": 0, "SKIP": 0}
    assert matrix["g17i_14"]["repaired"] == {"PASS": 14, "RED": 0,
                                             "ERROR": 0, "SKIP": 0}
    assert matrix["red_identity"]["exact_set_equal"] is True
    return matrix, proc


def proof_witness():
    contract = RETURN / "tests/test_bp1_actor_production.py.proof.json"
    proc = subprocess.run(
        [sys.executable, "-B", str(RETURN / "tools/proof_integrity_gate_r1.py"),
         "witness", str(contract), "--root", str(REPO)],
        cwd=str(REPO), env=ENV, capture_output=True, text=True)
    (LOGS / "proof_witness_bp1.txt").write_text(
        (proc.stdout + proc.stderr).replace(str(REPO), "$REPO"))
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    payload = json.loads(proc.stdout)
    assert payload["status"] == "MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION"
    assert len(payload["claims"]) == 6
    (EVID / "proof_witness_bp1.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def cold_probe():
    dst = RUNTIME / "cold"
    clean(dst)
    db = dst / "bp1.sqlite"
    receipt = dst / "receipt.json"
    run_script("bp1_cold_build",
               [sys.executable, "-B", "tools/bp1_cold_probe.py", "build",
                str(db), str(receipt)])
    run_script("bp1_cold_verify",
               [sys.executable, "-B", "tools/bp1_cold_probe.py", "verify",
                str(db), str(receipt)])
    payload = json.loads(receipt.read_text())
    (EVID / "c9_positive.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    out = dict(
        schema="BP1_COLD_REPLAY@1",
        build_process="fresh interpreter",
        verify_process="separate fresh interpreter",
        cold_record_equal=True,
        c9_committed=payload["c9"]["committed"],
        e2_admitted=payload["c9"]["e2_admitted"],
        target_id=payload["target_id"],
        consumed_state_hash=payload["c9"]["consumed_state_hash"],
        actor_id=payload["c9"]["actor_id"],
        actor_source_grade=payload["c9"]["actor_source_grade"],
        native_grant=payload["c9"]["native_grant"],
    )
    (EVID / "cold_replay.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


def source_manifest():
    roots = [CAND / "bp1", RETURN / "tests", RETURN / "tools",
             RETURN / "vendor/g18", RETURN / "vendor/c9r"]
    rows = []
    for root in roots:
        for p in sorted(root.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or p.suffix == ".pyc":
                continue
            rows.append(dict(path=str(p.relative_to(RETURN)),
                             sha256=sha256(p), git_blob_sha1=blob(p),
                             bytes=p.stat().st_size))
    tree = dict(
        schema="BP1_SOURCE_MANIFEST@1",
        g18_source="61713eafe0e7a5386a8f0aed4836b15f3d921ed5",
        c9r_source="6fa2939972ce5a2c0cc4f2b033946b276f1c2934",
        c9ri_review="5753d9b4f8fad9f2175b1e285733f95bb8387888",
        bp1_parent_dispatch="529232d9867a5bdc0889f43fb5293131ef806055",
        files=rows,
        tree_hash=hashlib.sha256(
            json.dumps(sorted((r["path"], r["sha256"]) for r in rows),
                       sort_keys=True).encode()).hexdigest(),
    )
    (EVID / "source_manifest.json").write_text(
        json.dumps(tree, indent=2, sort_keys=True) + "\n")
    return dict(files=len(rows), tree_hash=tree["tree_hash"])


def environment_passport():
    import importlib
    import pytest
    sys.path.insert(0, str(CAND))
    sys.path.insert(0, str(RETURN / "vendor/g18/candidate"))
    sys.path.insert(0, str(RETURN / "vendor/c9r"))
    modules = []
    for name in ("bp1", "bp1.source", "bp1.ledger", "bp1.composer", "bp1.c9_bridge"):
        m = importlib.import_module(name)
        modules.append(dict(module=name,
                            file=str(Path(m.__file__).relative_to(RETURN)),
                            sha256=sha256(Path(m.__file__))))
    for name in ("lab_sgi1.joint", "lab_sgi1.history", "candidate.identity",
                 "candidate.pipeline", "candidate.action_admission"):
        m = importlib.import_module(name)
        modules.append(dict(module=name,
                            file=str(Path(m.__file__).relative_to(RETURN)),
                            sha256=sha256(Path(m.__file__))))
    git = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO),
                          capture_output=True, text=True).stdout.strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=str(REPO),
                            capture_output=True, text=True).stdout.strip()
    passport = dict(
        schema="BP1_ENVIRONMENT_PASSPORT@1",
        python=sys.version,
        python_executable=sys.executable,
        pytest=pytest.__version__,
        git=git,
        git_head_at_run=head,
        git_branch=branch,
        platform=platform.platform(),
        machine=platform.machine(),
        time_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        env=dict(PYTHONDONTWRITEBYTECODE="1",
                 PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"),
        imported_modules=modules,
        native_authority="NOT_GRANTED",
        model="DeepSeek V4.1-Flash reasoning MAX (user-selected local editor)",
        external_api_calls=0,
        cash_quota="UNKNOWN",
    )
    (EVID / "environment_passport.json").write_text(
        json.dumps(passport, indent=2, sort_keys=True) + "\n")
    return passport


def main():
    clean(RUNTIME)
    clean(EVID)
    JUNIT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    bp1 = run_pytest("bp1_15", RETURN, "tests/test_bp1_actor_production.py",
                     (15, 0, 0, 0))
    c9r = run_pytest("c9r_10", RETURN / "vendor/c9r",
                     "tests/test_c9r_consumer.py", (10, 0, 0, 0))
    g18_matrix, _ = g18_regression()
    proof = proof_witness()
    export = run_script("export_bp1_life",
                        [sys.executable, "-B", "tools/export_bp1_life.py"])
    cold = cold_probe()
    two = json.loads((EVID / "two_actor_life.json").read_text())
    no_change = json.loads((EVID / "no_change_life.json").read_text())
    denied = json.loads((EVID / "denied_life.json").read_text())
    passport = environment_passport()
    manifest = source_manifest()

    matrix = dict(
        schema="BP1_COURT_MATRIX@1",
        generated_utc=passport["time_utc"],
        branch=passport["git_branch"],
        parent_dispatch=passport["git_head_at_run"],
        bp1_actor_court=dict(counts=bp1["counts"], cases=bp1["cases"]),
        c9r_consumer_recourse=dict(counts=c9r["counts"], cases=c9r["cases"]),
        g18_regression=g18_matrix,
        proof=dict(counts=len(proof["claims"]),
                   status=proof["status"],
                   claims=[c["claim_id"] for c in proof["claims"]]),
        two_actor=dict(
            actor_ids=two["actor_ids"],
            state_hashes=two["state_hashes"],
            history_hashes=two["history_hashes"],
            shared_objective_ref=two["shared_objective_ref"],
            shared_objective_hash=two["shared_objective_hash"],
            witness_status=two["witness_status"],
            performed_actions=two["performed_actions"],
            states=[s["state"] for s in two["snapshots"]],
            claim=two["claim"],
            native_actor_claim=False,
            psychology_claim=False,
        ),
        no_change=dict(state_unchanged=no_change["state_unchanged"],
                       refusal=no_change["refusal"],
                       ledger_event_kinds=no_change["ledger_event_kinds"]),
        deny=dict(state_unchanged=denied["state_unchanged"],
                  refusal=denied["refusal"],
                  ledger_event_kinds=denied["ledger_event_kinds"]),
        cold_replay=cold,
        source_manifest=manifest,
        environment=dict(python=passport["python"], pytest=passport["pytest"],
                         git=passport["git"], platform=passport["platform"]),
        native_authority="NOT_GRANTED",
        adoption="NOT_SELF_ADOPTED",
        productive_adequacy="EXECUTABLE_PRODUCER_AND_ACTUAL_CHANGED_HISTORY",
    )
    (EVID / "bp1_court_matrix.json").write_text(
        json.dumps(matrix, indent=2, sort_keys=True) + "\n")
    run_script("write_bp1_evidence",
               [sys.executable, "-B", "tools/write_bp1_evidence.py"])
    print("BP1", bp1["counts"], "C9R", c9r["counts"])
    print("G18", {k: v.get("counts") for k, v in g18_matrix.items()
                  if isinstance(v, dict) and "counts" in v})
    print("PROOF", len(proof["claims"]), "COLD", cold["e2_admitted"])
    print("TWO", two["state_hashes"])
    print("SOURCE", manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
