"""Generate S48 source-owner hold, controlled tests and old transport evidence."""
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

install()

from s37.harness import case_for, source_for  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s48.errors import ProductCallError  # noqa: E402
from s48.product import build_payload  # noqa: E402
from s48.session import S48Session  # noqa: E402
from s48.sources import (  # noqa: E402
    MISSING_FUNCTION,
    SOURCE_OWNER_HOLD,
    candidate_specs,
    eligible_candidate_ids,
    issue_current_source,
)

S47_RETURN = Path(roots()["s47_return"])
S48_FILES = [
    ".gitignore", "00_RETURN.md", "run_s48.py", "run_s48_evidence.py",
    "s48/__init__.py", "s48/bootstrap.py", "s48/errors.py", "s48/product.py",
    "s48/session.py", "s48/sources.py",
    "tests/conftest.py", "tests/test_s48_one_call.py",
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


def _identity(session):
    world = session.world()
    return {
        "world_events": len(world.events),
        "clock": session.clock(),
        "material": dict(world.actor_state["A"]).get("material_remaining"),
        "b_material": dict(world.actor_state["B"]).get("material_remaining"),
        "c12_events": len(session.read_events()),
        "root_hash": session.read_root()["root_hash"],
    }


def _controlled_hold():
    root = Path(tempfile.mkdtemp(prefix="s48-hold-", dir=str(RET / "logs")))
    session = _start(root / "state")
    calls = []

    def runner(prompt, *, workdir, log_dir, timeout):
        calls.append(1)
        return {
            "status": "OK",
            "envelope": {
                "schema": "S48_PRODUCT_ENVELOPE@1",
                "narrative": "controlled fixture",
                "self_account": None,
                "self_account_present": False,
                "prospective": [{
                    "candidate_id": "OTHER_REFUSES_TOOL",
                    "rationale": "controlled unsupported proposal",
                }],
            },
            "call_receipt": {
                "actual_provider_call": False,
                "provider_call_count": 1,
                "step_count": 1,
            },
            "prompt_hash": "fixture",
        }

    try:
        before = _identity(session)
        result = session.run_turn(product_runner=runner)
        after = _identity(session)
        return {
            "schema": "SOROK_S48_CONTROLLED_HOLD@1",
            "actual_provider_call": False,
            "status": result.get("status"),
            "reason": result.get("reason"),
            "missing_function": result.get("missing_function"),
            "event_ref": result.get("event_ref"),
            "fixture_call_count": len(calls),
            "identity_before": before,
            "identity_after": after,
            "unchanged": before == after,
            "no_c8_or_world_event": result.get("event_ref") == "",
            "no_realized_result": all(
                row["body"].get("status") != "REALIZED"
                for row in session.product_turns()
            ),
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()
        shutil.rmtree(root, ignore_errors=True)


def _no_qualified_source():
    root = Path(tempfile.mkdtemp(prefix="s48-nosource-", dir=str(RET / "logs")))
    session = _start(root / "state")
    try:
        payload = build_payload(session)
        code = ""
        try:
            issue_current_source(session, "OTHER_REFUSES_TOOL")
        except Exception as exc:
            code = getattr(exc, "code", type(exc).__name__)
        return {
            "schema": "SOROK_S48_NO_QUALIFIED_SOURCE@1",
            "candidate_specs": candidate_specs(session),
            "eligible_candidate_ids": eligible_candidate_ids(session),
            "payload_allowed": payload.get("allowed_prospective_candidates"),
            "install_refusal": code,
            "missing_function": MISSING_FUNCTION,
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()
        shutil.rmtree(root, ignore_errors=True)


def _transport_proof():
    base = EVID / "superseded_824170e3"
    label = json.loads((base / "LABEL.json").read_text())
    report = json.loads((base / "entrypoint.json").read_text())
    receipt = report.get("event_call_receipt") or {}
    return {
        "schema": "SOROK_S48_OLD_TRANSPORT_PROOF@1",
        "cut": label.get("cut"),
        "actual_provider_call": bool(receipt.get("actual_provider_call")),
        "provider_call_count": receipt.get("provider_call_count"),
        "transport_only": True,
        "positive_independence_superseded": label.get(
            "positive_independence_superseded"
        ),
        "reason": label.get("reason"),
        "raw_stdout": str(
            (base / "product.stdout.jsonl").relative_to(RET)
        ),
        "raw_stdout_sha256": _sha(base / "product.stdout.jsonl"),
        "entrypoint_sha256": _sha(base / "entrypoint.json"),
        "not_current_positive": True,
    }


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


def source_manifest(transport):
    s47_rows = []
    for rel in S47_FILES:
        local = S47_RETURN / rel
        pinned = _git(
            "rev-parse",
            f"{CUTS['s47']}:WORKER_RETURNS/SOROK-20261025-S47-INTERVAL-C9-CONDITIONING-R1/{rel}",
        )
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
    old = []
    for directory in (
        EVID / "old_cut_ae021e",
        EVID / "old_cut_ee4b2dd9",
        EVID / "superseded_824170e3",
    ):
        for path in sorted(directory.glob("*")):
            if path.is_file():
                old.append({
                    "path": str(path.relative_to(RET)),
                    "sha256": _sha(path),
                })
    return {
        "schema": "SOROK_S48_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s47_reused": {
            "rows": s47_rows,
            "all_exact": all(row["exact"] for row in s47_rows),
        },
        "s48_local": local_rows,
        "old_and_superseded_proofs": old,
        "transport_proof": transport,
        "current_source": {
            "status": SOURCE_OWNER_HOLD,
            "missing_function": MISSING_FUNCTION,
            "current_positive": False,
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
    transport = _transport_proof()
    hold = _controlled_hold()
    no_source = _no_qualified_source()
    _write(EVID / "transport_proof.json", transport)
    _write(EVID / "controlled_hold.json", hold)
    _write(EVID / "no_source.json", no_source)
    _write(EVID / "source_manifest.json", source_manifest(transport))
    tests = test_evidence()
    _write(EVID / "test_run.json", {
        "schema": "SOROK_S48_TEST_RUN@1", "s48": tests,
    })
    print(json.dumps({
        "transport": transport,
        "hold": hold,
        "no_source": no_source,
        "tests": tests["counts"],
    }, sort_keys=True))
    return 0 if tests["exit"] == 0 and hold["status"] == "SOURCE_OWNER_HOLD" else 1


if __name__ == "__main__":
    raise SystemExit(main())
