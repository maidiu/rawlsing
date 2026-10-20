"""C9R evidence driver: cold replay, fault trials, ledgers and source hashes.

Runs only disposable local processes and databases inside this return. Writes
machine-readable evidence under `evidence/` and JUnit under `junit/`.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parent
REPRO = RET / "repro"
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = os.pathsep.join([str(RET), str(RET / "runtime" / "native")])


def run(cmd, cwd, log_name, timeout=600):
    proc = subprocess.run(
        cmd, cwd=str(cwd), env=ENV, capture_output=True, text=True, timeout=timeout
    )
    (LOGS / log_name).write_text(proc.stdout + proc.stderr)
    return proc


def junit_counts(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    cases = []
    for case in root.iter("testcase"):
        name = case.attrib.get("name", "")
        classname = case.attrib.get("classname", "")
        status = "PASS"
        if case.find("failure") is not None:
            status = "RED"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        cases.append({"classname": classname, "name": name, "status": status})
    return {
        "tests": tests,
        "PASS": tests - failures - errors - skips,
        "RED": failures,
        "ERROR": errors,
        "SKIP": skips,
        "cases": cases,
    }


def cold_replay():
    work = Path(tempfile.mkdtemp(prefix="c9r-cold-", dir=str(RET / "runtime")))
    db1, db2 = work / "a.sqlite", work / "b.sqlite"
    out1 = run([PY, "-B", str(REPRO / "c9r_cold_worker.py"), "build", str(db1)], RET, "cold_build_a.log")
    out2 = run([PY, "-B", str(REPRO / "c9r_cold_worker.py"), "build", str(db2)], RET, "cold_build_b.log")
    if out1.returncode or out2.returncode:
        raise RuntimeError((out1.returncode, out1.stderr, out2.returncode, out2.stderr))
    build_a = json.loads(out1.stdout.strip().splitlines()[-1])
    build_b = json.loads(out2.stdout.strip().splitlines()[-1])
    i1 = run([PY, "-B", str(REPRO / "c9r_cold_worker.py"), "inspect", str(db1)], RET, "cold_inspect_a.log")
    i2 = run([PY, "-B", str(REPRO / "c9r_cold_worker.py"), "inspect", str(db2)], RET, "cold_inspect_b.log")
    if i1.returncode or i2.returncode:
        raise RuntimeError((i1.returncode, i1.stderr, i2.returncode, i2.stderr))
    inspect_a = json.loads(i1.stdout.strip().splitlines()[-1])
    inspect_b = json.loads(i2.stdout.strip().splitlines()[-1])
    record_a = next(iter(inspect_a["records"].values()))
    evidence = {
        "schema": "SOROK_C9R_COLD_REPLAY@1",
        "processes": {
            "build_a_pid_mode": "fresh interpreter",
            "build_b_pid_mode": "fresh interpreter",
            "inspect_a": "fresh interpreter",
            "inspect_b": "fresh interpreter",
        },
        "build_a": {k: build_a[k] for k in build_a if k != "logical_readset"},
        "build_b": {k: build_b[k] for k in build_b if k != "logical_readset"},
        "logical_snapshots_equal": build_a["logical_readset"] == build_b["logical_readset"]
        and inspect_a["logical_readset"] == inspect_b["logical_readset"],
        "record_identity_equal": record_a.get("record_hash") == build_a.get("record_hash"),
        "record_state_hash_equal": inspect_a["reads"][next(iter(inspect_a["reads"]))]["state_hash"]
        == inspect_b["reads"][next(iter(inspect_b["reads"]))]["state_hash"],
        "read_status_a": inspect_a["reads"][next(iter(inspect_a["reads"]))]["status"],
        "read_status_b": inspect_b["reads"][next(iter(inspect_b["reads"]))]["status"],
        "integrity_check_a": inspect_a["integrity_check"],
        "integrity_check_b": inspect_b["integrity_check"],
        "record_preimage_digest_ok": build_a["record_hash"]
        == record_a.get("record_hash"),
    }
    (EVID / "cold_replay.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    shutil.rmtree(work, ignore_errors=True)
    return evidence


def fault_trials():
    contract = json.loads((RET / "tests" / "test_c9r_consumer.py.proof.json").read_text())
    faults_dir = JUNIT / "faults"
    faults_dir.mkdir(parents=True, exist_ok=True)
    trials = []
    for index, claim in enumerate(contract["claims"]):
        node = claim["positive_node"]
        fault = claim["fault"]
        target = RET / fault["path"]
        original = target.read_text()
        if original.count(fault["old"]) != 1:
            raise RuntimeError(f"mutation not unique: {claim['claim_id']}")
        trial = {"claim_id": claim["claim_id"], "positive_node": node, "phases": {}}
        for phase, mutate in (("positive", False), ("fault", True), ("restored", False)):
            xml = faults_dir / f"{index:02d}_{phase}.xml"
            if mutate:
                target.write_text(original.replace(fault["old"], fault["new"], 1))
            try:
                proc = run(
                    [
                        PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                        f"--junitxml={xml}", node.split("::")[0] + "::" + node.split("::")[1],
                    ],
                    RET,
                    f"fault_{index:02d}_{phase}.log",
                )
            finally:
                target.write_text(original)
            counts = junit_counts(xml)
            named = next(
                (c for c in counts["cases"] if c["name"] == node.split("::")[-1].split("[")[0]),
                None,
            )
            trial["phases"][phase] = {
                "exit": proc.returncode,
                "named_status": named["status"] if named else "MISSING",
                "junit": str(xml.relative_to(RET)),
            }
        trial["pass"] = (
            trial["phases"]["positive"]["named_status"] == "PASS"
            and trial["phases"]["fault"]["named_status"] == "RED"
            and trial["phases"]["restored"]["named_status"] == "PASS"
        )
        trials.append(trial)
    evidence = {
        "schema": "SOROK_C9R_FAULT_TRIALS@1",
        "trials": trials,
        "all_pass": all(t["pass"] for t in trials),
    }
    (EVID / "fault_trials.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return evidence


def ledger():
    baseline_hostile = junit_counts(JUNIT / "baseline_hostile.xml")
    repaired_hostile = junit_counts(JUNIT / "repaired_hostile.xml")
    baseline_custody = junit_counts(JUNIT / "baseline_record_custody.xml")
    repaired_custody = junit_counts(JUNIT / "repaired_record_custody.xml")
    base_map = {(c["classname"], c["name"]): c["status"] for c in baseline_hostile["cases"]}
    rep_map = {(c["classname"], c["name"]): c["status"] for c in repaired_hostile["cases"]}
    custody_base = {(c["classname"], c["name"]): c["status"] for c in baseline_custody["cases"]}
    custody_rep = {(c["classname"], c["name"]): c["status"] for c in repaired_custody["cases"]}
    rows = []
    for key, base in base_map.items():
        rows.append(
            {
                "court": "hostile",
                "test": key[1],
                "baseline": base,
                "repaired": rep_map.get(key, "MISSING"),
            }
        )
    for key, base in custody_base.items():
        rows.append(
            {
                "court": "record_custody",
                "test": key[1],
                "baseline": base,
                "repaired": custody_rep.get(key, "MISSING"),
            }
        )
    reds = [r for r in rows if r["baseline"] == "RED"]
    repaired_reds = [r for r in reds if r["repaired"] != "PASS"]
    evidence = {
        "schema": "SOROK_C9R_HOSTILE_LEDGER@1",
        "baseline_reds": len(reds),
        "repaired_reds": len(repaired_reds),
        "rows": rows,
        "unrepaired": repaired_reds,
        "baseline_counts": {
            "hostile": {k: baseline_hostile[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
            "record_custody": {k: baseline_custody[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        },
        "repaired_counts": {
            "hostile": {k: repaired_hostile[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
            "record_custody": {k: repaired_custody[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        },
    }
    (EVID / "hostile_ledger.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")

    author_base = junit_counts(JUNIT / "baseline_author_90.xml")
    author_rep = junit_counts(JUNIT / "repaired_author_90.xml")
    base_author_map = {(c["classname"], c["name"]): c["status"] for c in author_base["cases"]}
    rep_author_map = {(c["classname"], c["name"]): c["status"] for c in author_rep["cases"]}
    divergences = [
        {"test": key[1], "baseline": status, "repaired": rep_author_map.get(key, "MISSING")}
        for key, status in sorted(base_author_map.items())
        if rep_author_map.get(key) != status
    ]
    author_evidence = {
        "schema": "SOROK_C9R_AUTHOR_DIVERGENCE@1",
        "baseline": {k: author_base[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "repaired": {k: author_rep[k] for k in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "divergences": divergences,
        "note": (
            "Author tests that encode the pre-repair permissive caller-label contract "
            "change status under the hardened candidate. They are baseline evidence, "
            "not the repair acceptance oracle; no frozen author test was edited."
        ),
    }
    (EVID / "author_divergence.json").write_text(
        json.dumps(author_evidence, indent=2, sort_keys=True) + "\n"
    )
    return evidence, author_evidence


def source_ledger():
    def blob(path):
        return subprocess.run(
            ["git", "hash-object", str(path)],
            cwd=str(Path.cwd()),
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def sha256(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    rows = []
    for rel in sorted(
        [p for p in (RET / "candidate").glob("*.py")]
        + [p for p in (RET / "tests").glob("*.py")]
        + [p for p in (RET / "repro").glob("*.py")]
    ):
        rows.append(
            {
                "role": "C9R_NEW_SOURCE",
                "path": str(rel.relative_to(RET)),
                "git_blob_sha1": blob(rel),
                "sha256": sha256(rel),
            }
        )
    pinned = {
        "runtime/c9p/candidate/transaction.py": "P_C9P",
        "runtime/c9pi/review/test_hostile.py": "P_C9PI",
        "runtime/c9pi/review/test_record_custody.py": "P_C9PI",
        "runtime/native/rawlsing_next/v3_psepf_zero_positive_guard.py": "P_NATIVE",
    }
    for rel, role in pinned.items():
        rel_path = RET / rel
        rows.append(
            {
                "role": role,
                "path": rel,
                "git_blob_sha1": blob(rel_path),
                "sha256": sha256(rel_path),
            }
        )
    b3as = subprocess.run(
        ["git", "rev-parse", "16f15a125ba54cdf17f5d41be2d851bbcd2240d7:WORKER_RETURNS/SOROK-20261018-B3A-SCHEMA-READSET-REPAIR-R1/candidate/integration.py"],
        cwd=str(Path.cwd()),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    ledger = {
        "schema": "SOROK_C9R_SOURCE_IMPORT_LEDGER@1",
        "rows": rows,
        "b3as_reused_readset_source_blob": b3as,
        "pinned": {
            "c9p_target_commit": "38fba47614e82a86fc5a3fa3f50c27048493e808",
            "c9pi_review_commit": "df2382b8d9478f0a904dcff06ee45bb0119a1bda",
            "b3as_repair_commit": "16f15a125ba54cdf17f5d41be2d851bbcd2240d7",
            "shared_proof_gate_blob": "774d338cdbeea68ab09006807431cc8d17a22345",
        },
    }
    (EVID / "source_import_ledger.json").write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n"
    )
    return ledger


def main():
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    cold = cold_replay()
    faults = fault_trials()
    hostile, author = ledger()
    sources = source_ledger()
    print(json.dumps({
        "cold_logical_equal": cold["logical_snapshots_equal"],
        "cold_status_a": cold["read_status_a"],
        "cold_integrity": cold["integrity_check_a"],
        "faults_all_pass": faults["all_pass"],
        "baseline_reds": hostile["baseline_reds"],
        "repaired_reds": hostile["repaired_reds"],
        "author_divergences": len(author["divergences"]),
        "source_rows": len(sources["rows"]),
    }, indent=2))


if __name__ == "__main__":
    main()
