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
EVIDENCE = RETURN / "evidence"
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def run_pytest(cwd, target, junit=None):
    command = [
        sys.executable,
        "-B",
        "-m",
        "pytest",
        "-q",
        target,
        "-p",
        "no:cacheprovider",
    ]
    if junit:
        command.append(f"--junitxml={junit}")
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
    tests = []
    for case in suite.findall("testcase"):
        failure = case.find("failure")
        tests.append({
            "name": case.attrib.get("name"),
            "classname": case.attrib.get("classname"),
            "outcome": "failed" if failure is not None else "passed",
            "message": (failure.attrib.get("message", "") if failure is not None else ""),
            "detail": (failure.text or "" if failure is not None else ""),
        })
    return {
        "tests": suite.attrib.get("tests"),
        "failures": suite.attrib.get("failures"),
        "errors": suite.attrib.get("errors"),
        "skipped": suite.attrib.get("skipped"),
        "cases": tests,
    }


def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    positive = run_pytest(
        RETURN, "tests/test_join_v_positive.py", EVIDENCE / "positive.xml"
    )
    hostile = run_pytest(
        RETURN, "tests/test_join_v_hostile.py", EVIDENCE / "hostile.xml"
    )
    candidate = run_pytest(CANDIDATE, "tests/test_join.py")
    inherited = {
        "r31j": run_pytest(CANDIDATE / "vendor" / "j", "tests/test_r31j.py"),
        "r31e": run_pytest(
            CANDIDATE / "vendor" / "e", "tests/test_r31e_expression.py"
        ),
        "r30a": run_pytest(
            CANDIDATE / "vendor" / "e" / "vendor" / "r30a",
            "tests/test_r30a_first_session.py",
        ),
    }
    document = {
        "candidate": str(CANDIDATE),
        "positive": {
            **positive,
            "summary": parse_junit(EVIDENCE / "positive.xml"),
        },
        "hostile": {
            **hostile,
            "summary": parse_junit(EVIDENCE / "hostile.xml"),
        },
        "candidate_own_suite": {
            "returncode": candidate["returncode"],
            "stdout": candidate["stdout"],
            "stderr": candidate["stderr"],
        },
        "inherited": {
            name: {
                "returncode": result["returncode"],
                "stdout": result["stdout"],
                "stderr": result["stderr"],
            }
            for name, result in inherited.items()
        },
    }
    path = EVIDENCE / "test_results.json"
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "positive": document["positive"]["summary"],
        "hostile": document["hostile"]["summary"],
        "candidate_own": document["candidate_own_suite"]["returncode"],
        "inherited": {
            name: value["returncode"]
            for name, value in document["inherited"].items()
        },
    }, indent=2))


if __name__ == "__main__":
    main()
