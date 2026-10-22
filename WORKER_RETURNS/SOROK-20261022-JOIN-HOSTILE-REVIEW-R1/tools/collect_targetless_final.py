import hashlib
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
DEFAULT_CANDIDATE = REPO / "WORKER_RETURNS" / "SOROK-20261022-SAME-PERSON-JOIN-R1"
CANDIDATE = Path(
    os.environ.get("SOROK_JOIN_CANDIDATE_ROOT", str(DEFAULT_CANDIDATE))
).resolve()
EVIDENCE = RETURN / "evidence" / "targetless_final"
ENV = {
    **os.environ,
    "PYTHONDONTWRITEBYTECODE": "1",
    "SOROK_JOIN_CANDIDATE_ROOT": str(CANDIDATE),
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_blob(path):
    return subprocess.run(
        ["git", "-C", str(CANDIDATE), "hash-object", str(path)],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def run_pytest(cwd, target, junit):
    command = [
        sys.executable,
        "-B",
        "-m",
        "pytest",
        "-q",
        target,
        "-p",
        "no:cacheprovider",
        f"--junitxml={junit}",
    ]
    run = subprocess.run(
        command,
        cwd=cwd,
        env=ENV,
        text=True,
        capture_output=True,
        timeout=300,
    )
    return {
        "command": " ".join(command),
        "cwd": str(cwd),
        "returncode": run.returncode,
        "stdout": run.stdout,
        "stderr": run.stderr,
    }


def parse_junit(path):
    root = ET.parse(path).getroot()
    suite = root.find("testsuite")
    cases = []
    for case in suite.findall("testcase"):
        failure = case.find("failure")
        cases.append({
            "name": case.attrib.get("name"),
            "classname": case.attrib.get("classname"),
            "outcome": "failed" if failure is not None else "passed",
            "message": (failure.attrib.get("message", "") if failure is not None else ""),
        })
    return {
        "tests": suite.attrib.get("tests"),
        "failures": suite.attrib.get("failures"),
        "errors": suite.attrib.get("errors"),
        "skipped": suite.attrib.get("skipped"),
        "cases": cases,
    }


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    frozen = json.loads((RETURN / "FROZEN_ORACLES.json").read_text())
    frozen_hashes = {
        name: sha256(RETURN / name) for name in frozen["test_files_sha256"]
    }
    frozen_match = {
        name: frozen_hashes[name] == expected
        for name, expected in frozen["test_files_sha256"].items()
    }

    frozen_positive = run_pytest(
        RETURN, "tests/test_join_v_positive.py", EVIDENCE / "frozen_positive.xml"
    )
    frozen_hostile = run_pytest(
        RETURN, "tests/test_join_v_hostile.py", EVIDENCE / "frozen_hostile.xml"
    )
    targeted = run_pytest(
        RETURN, "tests/test_join_v_final_cut.py", EVIDENCE / "targeted_c367.xml"
    )
    repaired = run_pytest(
        RETURN, "tests/test_join_v_repaired_cut.py", EVIDENCE / "repaired_targeted.xml"
    )
    targetless = run_pytest(
        RETURN, "tests/test_join_v_targetless_final.py", EVIDENCE / "targetless_final.xml"
    )
    candidate_own = run_pytest(
        CANDIDATE, "tests", EVIDENCE / "candidate_own.xml"
    )
    inherited = {
        "r31j": run_pytest(
            CANDIDATE / "vendor" / "j", "tests/test_r31j.py",
            EVIDENCE / "j_r31j.xml",
        ),
        "r31e": run_pytest(
            CANDIDATE / "vendor" / "e", "tests/test_r31e_expression.py",
            EVIDENCE / "e_expression.xml",
        ),
        "r30a": run_pytest(
            CANDIDATE / "vendor" / "e" / "vendor" / "r30a",
            "tests/test_r30a_first_session.py",
            EVIDENCE / "e_r30a.xml",
        ),
    }

    manifest = json.loads((CANDIDATE / "SOURCE_MANIFEST.json").read_text())
    missing = []
    mismatched = []
    verified = 0
    for row in manifest["files"]:
        path = CANDIDATE / row["path"]
        if not path.exists():
            missing.append(row["path"])
            continue
        if git_blob(path) != row["git_blob"]:
            mismatched.append(row["path"])
            continue
        verified += 1

    source_files = [
        "joined/session.py",
        "joined/imports.py",
        "joined/provenance.py",
        "joined/refusal.py",
        "joined/readonly.py",
        "joined/closure.py",
        "joined/assertion.py",
        "joined/cli.py",
        "joined/__init__.py",
        "tests/test_join.py",
        "tests/test_join.py.proof.json",
        "SOURCE_MANIFEST.json",
        "RESUME_CHECKPOINT.md",
    ]
    source = {
        "candidate_commit": subprocess.run(
            ["git", "-C", str(CANDIDATE), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip(),
        "candidate_root": str(CANDIDATE),
        "source_files_sha256": {
            name: sha256(CANDIDATE / name) for name in source_files
        },
        "source_manifest": {
            "rows": len(manifest["files"]),
            "verified": verified,
            "missing": missing,
            "mismatched": mismatched,
        },
        "frozen_test_hashes": frozen_hashes,
        "frozen_test_hashes_match": frozen_match,
        "targeted_c367_test_hash": sha256(RETURN / "tests" / "test_join_v_final_cut.py"),
        "repaired_targeted_test_hash": sha256(RETURN / "tests" / "test_join_v_repaired_cut.py"),
        "targetless_final_test_hash": sha256(RETURN / "tests" / "test_join_v_targetless_final.py"),
    }
    (EVIDENCE / "source.json").write_text(
        json.dumps(source, indent=2, sort_keys=True) + "\n"
    )

    results = {
        "candidate": str(CANDIDATE),
        "candidate_commit": source["candidate_commit"],
        "frozen_test_hashes_match": frozen_match,
        "frozen_positive": {
            **frozen_positive,
            "summary": parse_junit(EVIDENCE / "frozen_positive.xml"),
        },
        "frozen_hostile": {
            **frozen_hostile,
            "summary": parse_junit(EVIDENCE / "frozen_hostile.xml"),
        },
        "targeted_c367": {
            **targeted,
            "summary": parse_junit(EVIDENCE / "targeted_c367.xml"),
        },
        "repaired_targeted": {
            **repaired,
            "summary": parse_junit(EVIDENCE / "repaired_targeted.xml"),
        },
        "targetless_final": {
            **targetless,
            "summary": parse_junit(EVIDENCE / "targetless_final.xml"),
        },
        "candidate_own_suite": {
            "returncode": candidate_own["returncode"],
            "stdout": candidate_own["stdout"],
            "stderr": candidate_own["stderr"],
            "summary": parse_junit(EVIDENCE / "candidate_own.xml"),
        },
        "inherited": {
            name: {
                "returncode": value["returncode"],
                "stdout": value["stdout"],
                "stderr": value["stderr"],
                "summary": parse_junit(EVIDENCE / xml_name),
            }
            for (name, value), xml_name in zip(
                inherited.items(),
                ("j_r31j.xml", "e_expression.xml", "e_r30a.xml"),
            )
        },
    }
    (EVIDENCE / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "candidate_commit": results["candidate_commit"],
        "frozen_hashes_match": frozen_match,
        "frozen_positive": results["frozen_positive"]["summary"],
        "frozen_hostile": results["frozen_hostile"]["summary"],
        "targeted_c367": results["targeted_c367"]["summary"],
        "repaired_targeted": results["repaired_targeted"]["summary"],
        "targetless_final": results["targetless_final"]["summary"],
        "candidate_own": results["candidate_own_suite"]["summary"],
        "inherited": {
            name: value["summary"]["tests"]
            for name, value in results["inherited"].items()
        },
        "manifest": source["source_manifest"],
    }, indent=2))


if __name__ == "__main__":
    main()
