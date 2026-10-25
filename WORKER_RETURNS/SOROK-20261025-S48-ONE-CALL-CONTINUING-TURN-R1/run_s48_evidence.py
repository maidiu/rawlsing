"""Generate S48 actual-call, controlled-branch, test and source evidence.

This script intentionally does not invoke the product provider again. It reads
the already captured actual entrypoint call and produces only focused tests and
controlled local orchestration evidence.
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
EVID = RET / "evidence"
JUNIT = RET / "junit"
LOGS = RET / "logs"
PY = sys.executable
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
ENV["PYTHONPATH"] = str(RET)
ENV.setdefault(
    "M35_JOIN_E_RETURN",
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
    "SOROK-20261022-SAME-PERSON-JOIN-R1",
)
for path in (str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s48.bootstrap import CUTS, install, roots  # noqa: E402
from s48.errors import ProductCallError  # noqa: E402
from s48.product import parse_envelope  # noqa: E402

install()

from s37.harness import case_for, source_for  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s48.session import S48Session, SCI05_REASON  # noqa: E402

S47_RETURN = Path(roots()["s47_return"])
S48_FILES = [
    ".gitignore", "00_RETURN.md", "run_s48.py", "run_s48_evidence.py",
    "s48/__init__.py", "s48/bootstrap.py", "s48/errors.py", "s48/product.py",
    "s48/session.py", "tests/conftest.py", "tests/test_s48_one_call.py",
]
S47_FILES = [
    "s47/__init__.py", "s47/bootstrap.py", "s47/conditioning.py",
    "s47/errors.py", "s47/session.py",
    "tests/conftest.py", "tests/test_s47_interval_c9_conditioning.py",
]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(RET), capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, log_name, env=None):
    proc = subprocess.run(cmd, cwd=str(RET), env=env or ENV,
                          capture_output=True, text=True)
    (LOGS / log_name).write_text(proc.stdout + proc.stderr)
    return proc


def _junit_counts(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tests = sum(int(s.attrib.get("tests", 0)) for s in suites)
    failures = sum(int(s.attrib.get("failures", 0)) for s in suites)
    errors = sum(int(s.attrib.get("errors", 0)) for s in suites)
    skips = sum(int(s.attrib.get("skipped", 0)) for s in suites)
    cases = []
    for case in root.iter("testcase"):
        status = "PASS"
        if case.find("failure") is not None:
            status = "RED"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        cases.append({
            "classname": case.attrib.get("classname", ""),
            "name": case.attrib.get("name", ""), "status": status,
        })
    return {
        "tests": tests, "PASS": tests - failures - errors - skips,
        "RED": failures, "ERROR": errors, "SKIP": skips, "cases": cases,
    }


def _start(state):
    case = case_for(True)
    return S48Session.start(
        state, bundle=root_bundle("01" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )


def _fake(envelope=None, *, calls, receipt=None, error=None):
    def run(prompt, *, workdir, log_dir, timeout):
        calls.append({"prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()})
        if error is not None:
            raise error
        return {
            "status": "OK",
            "envelope": envelope,
            "call_receipt": receipt or {
                "actual_provider_call": False,
                "provider_call_count": 1,
                "step_count": 1,
            },
            "prompt_hash": "fixture",
        }
    return run


def controlled_branches():
    root = Path(tempfile.mkdtemp(prefix="s48-controlled-", dir=str(RET / "logs")))
    try:
        hold_state = root / "hold"
        hold = _start(hold_state)
        try:
            calls = []
            before = len(hold.read_events())
            result = hold.run_turn(product_runner=_fake({
                "schema": "S48_PRODUCT_ENVELOPE@1",
                "narrative": "A bounded narrative.",
                "self_account": "A proposed internal self-account remains unsupported.",
                "self_account_present": True,
                "prospective": [],
            }, calls=calls))
            hold_body = {
                "status": result.get("status"),
                "sci05_hold": result.get("sci05_hold"),
                "reason": result.get("reason"),
                "event_ref": result.get("event_ref"),
                "events_before": before,
                "events_after": len(hold.read_events()),
                "fixture_call_count": result.get("provider_call_count"),
                "actual_provider_call": False,
                "verify_ok": hold.verify()["ok"],
            }
        finally:
            hold.close()

        fail_state = root / "failure"
        fail = _start(fail_state)
        try:
            calls = []
            before = len(fail.read_events())
            error = ProductCallError(
                "S48_PRODUCT_CALL_FAILED", "controlled fixture",
                {"actual_provider_call": False, "provider_call_count": 0},
            )
            result = fail.run_turn(product_runner=_fake(calls=calls, error=error))
            fail_body = {
                "status": result.get("status"),
                "reason": result.get("reason"),
                "event_ref": result.get("event_ref"),
                "events_before": before,
                "events_after": len(fail.read_events()),
                "fixture_call_count": result.get("provider_call_count"),
                "actual_provider_call": False,
                "verify_ok": fail.verify()["ok"],
            }
        finally:
            fail.close()
        return {
            "schema": "SOROK_S48_CONTROLLED_BRANCHES@1",
            "sci05_hold": hold_body,
            "call_failure": fail_body,
            "note": "Controlled non-provider fixtures; actual call is entrypoint.json.",
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_evidence():
    xml = JUNIT / "s48_full.xml"
    tmp = LOGS / "tmp"
    tmp.mkdir(exist_ok=True)
    env = dict(ENV, TMPDIR=str(tmp))
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s48_full.log", env=env,
    )
    counts = _junit_counts(xml)
    shutil.rmtree(tmp, ignore_errors=True)
    return {
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in
                   ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def actual_entrypoint():
    path = LOGS / "entrypoint.log"
    if not path.is_file():
        raise RuntimeError("S48_ENTRYPOINT_LOG_MISSING")
    report = json.loads(path.read_text())
    receipt = report.get("event_call_receipt") or {}
    if not receipt.get("actual_provider_call"):
        raise RuntimeError("S48_ACTUAL_CALL_NOT_PROVEN")
    if report.get("turn_status") != "REALIZED":
        raise RuntimeError("S48_ACTUAL_POSITIVE_NOT_REALIZED:" + str(report.get("turn_status")))
    if receipt.get("provider_call_count") != 1:
        raise RuntimeError("S48_ACTUAL_CALL_COUNT_INVALID")
    if report.get("cached_on_cold") is not True:
        raise RuntimeError("S48_COLD_CACHE_NOT_PROVEN")
    if report.get("cold_provider_call_count") != 0:
        raise RuntimeError("S48_COLD_CALL_REPEATED")
    if not (report.get("c9") or {}).get("s47_source_in_readset"):
        raise RuntimeError("S48_S47_SOURCE_NOT_IN_C9")
    return report


def actual_envelope(report):
    receipt = report.get("event_call_receipt") or {}
    path = RET / receipt.get("stdout_path", "")
    if not path.is_file():
        raise RuntimeError("S48_ACTUAL_PRODUCT_LOG_MISSING")
    text_parts = []
    import json as _json
    for line in path.read_text().splitlines():
        try:
            event = _json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "text":
            text_parts.append(str((event.get("part") or {}).get("text", "")))
    envelope = parse_envelope("".join(text_parts))
    return {
        "schema": "SOROK_S48_ACTUAL_ENVELOPE@1",
        "source_event_ref": report.get("source_event", {}).get("event_ref"),
        "product_session_ids": receipt.get("session_ids"),
        "output_sha256": receipt.get("output_sha256"),
        "envelope": envelope,
    }


def source_manifest(report):
    s47_rows = []
    for rel in S47_FILES:
        local = S47_RETURN / rel
        pinned = _git("rev-parse", f"{CUTS['s47']}:WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/{rel}")
        local_blob = _git("hash-object", str(local))
        s47_rows.append({
            "path": rel,
            "pinned_git_blob_sha1": pinned,
            "local_git_blob_sha1": local_blob,
            "exact": pinned == local_blob,
            "sha256": _sha(local),
        })
    local_rows = [
        {
            "path": rel,
            "sha256": _sha(RET / rel),
            "git_blob_sha1": _git("hash-object", str(RET / rel)),
        }
        for rel in S48_FILES if (RET / rel).exists()
    ]
    receipt = report.get("event_call_receipt") or {}
    stdout_path = RET / receipt.get("stdout_path", "")
    return {
        "schema": "SOROK_S48_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s47_reused": {
            "rows": s47_rows,
            "all_exact": all(row["exact"] for row in s47_rows),
        },
        "s48_local": local_rows,
        "old_cut_evidence": [
            {
                "path": str(path.relative_to(RET)),
                "sha256": _sha(path),
            }
            for path in sorted((EVID / "old_cut_ae021e").glob("*"))
            if path.is_file()
        ],
        "actual_call": {
            "provider_call_count": receipt.get("provider_call_count"),
            "actual_envelope_sha256": _sha(EVID / "actual_envelope.json")
            if (EVID / "actual_envelope.json").is_file() else "",
            "actual_provider_call": receipt.get("actual_provider_call"),
            "model": receipt.get("model"),
            "variant": receipt.get("variant"),
            "prompt_sha256": receipt.get("prompt_sha256"),
            "output_sha256": receipt.get("output_sha256"),
            "stdout_path": receipt.get("stdout_path"),
            "stdout_sha256": _sha(stdout_path) if stdout_path.is_file() else "",
        },
        "product_gateway": {
            "cli": receipt.get("cli"),
            "model": receipt.get("model"),
            "variant": receipt.get("variant"),
            "provider": receipt.get("provider"),
        },
        "native_grants": {
            "actor": False, "rule": False, "source": False, "human": False,
            "c8": False, "c9": False, "c12": False,
        },
    }


def main():
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    report = actual_entrypoint()
    _write(EVID / "entrypoint.json", report)
    envelope = actual_envelope(report)
    _write(EVID / "actual_envelope.json", envelope)
    _write(EVID / "controlled.json", controlled_branches())
    _write(EVID / "source_manifest.json", source_manifest(report))
    tests = test_evidence()
    _write(EVID / "test_run.json", {
        "schema": "SOROK_S48_TEST_RUN@1", "s48": tests,
    })
    print(json.dumps({
        "actual_envelope": envelope["envelope"],
        "actual": {
            "status": report.get("turn_status"),
            "provider_call_count": report.get("provider_call_count"),
            "cached_on_cold": report.get("cached_on_cold"),
            "cold_provider_call_count": report.get("cold_provider_call_count"),
            "event_ref": report.get("event", {}).get("event_ref"),
            "event_ordinal": report.get("event", {}).get("event_ordinal"),
            "turn_id": report.get("turn_id"),
            "source_owner": report.get("source_owner"),
            "source_actor": report.get("source_actor"),
            "s47_source_in_readset": report.get("c9", {}).get("s47_source_in_readset"),
            "output_sha256": (report.get("event_call_receipt") or {}).get("output_sha256"),
        },
        "controlled": json.loads((EVID / "controlled.json").read_text()),
        "tests": tests["counts"],
    }, sort_keys=True))
    return 0 if tests["exit"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
