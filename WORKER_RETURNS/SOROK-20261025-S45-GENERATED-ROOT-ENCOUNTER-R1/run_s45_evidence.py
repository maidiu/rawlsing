"""Generate S45 consumer, fault, unsupported, denied and source evidence."""
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

from s45.bootstrap import CUTS, install, roots  # noqa: E402

install()

from s44.root import generate_root  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s45.session import S45Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402

S44_RETURN = Path(roots()["s44_return"])
S43_RETURN = Path(roots()["s43_return"])
S44_FILES = [
    "s44/__init__.py", "s44/bootstrap.py", "s44/bundle.py", "s44/errors.py",
    "s44/rng.py", "s44/root.py", "s44/session.py",
]
S45_FILES = [
    ".gitignore", "00_RETURN.md", "run_s45.py", "run_s45_evidence.py",
    "s45/__init__.py", "s45/bootstrap.py", "s45/errors.py", "s45/fixtures.py",
    "s45/language.py", "s45/session.py",
    "tests/conftest.py", "tests/test_s45_generated_root_encounter.py",
]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=str(RET), capture_output=True, text=True, check=True
    ).stdout.strip()


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def _run(cmd, log_name: str, env=None):
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
        cases.append({"classname": case.attrib.get("classname", ""),
                      "name": case.attrib.get("name", ""), "status": status})
    return {"tests": tests, "PASS": tests - failures - errors - skips,
            "RED": failures, "ERROR": errors, "SKIP": skips, "cases": cases}


def _start(state, *, seed="01" * 32, bundle=None):
    case = case_for(True)
    return S45Session.start(
        state, bundle=bundle or root_bundle(seed), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )


def _b_speech(session):
    return len([
        event for event in session.events()
        if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
    ])


def _a_speech(session):
    return len([
        event for event in session.events()
        if event.get("actor_id") == "A" and event.get("kind") == "SPEECH"
    ])


def _encounter(session, row):
    return {
        "encounter_id": row.get("encounter_id"),
        "kind": row.get("kind"),
        "status": row.get("status"),
        "strategy": row.get("strategy"),
        "user_event_id": row.get("user_event_id"),
        "user_event_hash": row.get("user_event_hash"),
        "speech_event_id": row.get("speech_event_id"),
        "speech_event_hash": row.get("speech_event_hash"),
        "action_event_id": row.get("action_event_id"),
        "admission_id": row.get("admission_id"),
        "plan_hash": row.get("plan_hash"),
        "native_text": row.get("native_text"),
        "translation_text": row.get("translation_text"),
        "source_event_refs": row.get("source_event_refs", []),
        "access_receipt_ids": row.get("access_receipt_ids", []),
    }


def consumer_evidence(state):
    session = _start(state)
    try:
        root = session.read_root()
        root_hash = root["root_hash"]
        before_b = _b_speech(session)
        first_event = session.read_events()[0]
        said = session.say("Can I help?")
        state_say = dict(session.world().actor_state["A"])
    finally:
        session.close()
    session = S45Session.open(state)
    try:
        helped = session.do_help()
        state_help = dict(session.world().actor_state["A"])
    finally:
        session.close()
    session = S45Session.open(state)
    try:
        attended = session.attend()
        events = session.read_events()
        encounters = session.read_encounters()
        root_after = session.read_root()
        verify = session.verify()
        state_attend = dict(session.world().actor_state["A"])
        clock = session.clock()
        after_b = _b_speech(session)
        view = session.language_view(
            said["language"]["speech_event_id"], locale="en"
        )
    finally:
        session.close()
    cold = S45Session.open(state)
    try:
        cold_root = cold.read_root()
        cold_verify = cold.verify()
        cold_events = len(cold.read_events())
        cold_encounters = len(cold.read_encounters())
    finally:
        cold.close()
    return {
        "schema": "SOROK_S45_CONSUMER_EVIDENCE@1",
        "root_hash": root_hash,
        "root_hash_after": root_after["root_hash"],
        "root_unchanged": root_after["root_hash"] == root_hash,
        "cold_root_same": cold_root["root_hash"] == root_hash,
        "root_event_id": first_event["e1_event_id"],
        "root_event_hash": first_event["e1_event_hash"],
        "events_before": 1,
        "events_after": len(events),
        "encounter_count": len(encounters),
        "encounters": [
            {
                "kind": row.get("kind"), "status": row.get("status"),
                "strategy": row.get("strategy"),
                "user_event_id": row.get("user_event_id"),
                "speech_event_id": row.get("speech_event_id"),
                "action_event_id": row.get("action_event_id"),
                "native_text": row.get("native_text"),
                "translation_text": row.get("translation_text"),
                "source_event_refs": row.get("source_event_refs", []),
                "access_receipt_ids": row.get("access_receipt_ids", []),
            }
            for row in encounters
        ],
        "say": {
            "status": said.get("status"), "strategy": said.get("strategy"),
            "native_text": (said.get("language") or {}).get("native_text"),
            "translation_text": (said.get("language") or {}).get("translation_text"),
            "source_event_id": (said.get("language") or {}).get("source_event_id"),
            "surface": said.get("surface"),
        },
        "do_help": {
            "status": helped.get("status"), "accepted": helped.get("accepted"),
            "strategy": helped.get("strategy"),
            "action_event_id": (helped.get("admission") or {}).get("action_event_id"),
            "native_text": (helped.get("language") or {}).get("native_text"),
            "translation_text": (helped.get("language") or {}).get("translation_text"),
            "surface": helped.get("surface"),
        },
        "attend": {
            "status": attended.get("status"),
            "new_knowledge": attended.get("new_knowledge"),
            "surface": attended.get("surface"),
        },
        "material_state": {
            "after_say": state_say, "after_help": state_help,
            "after_attend": state_attend,
        },
        "no_new_b_speech": before_b == after_b,
        "clock": clock,
        "view": {
            "status": view.get("status"),
            "display_mode": view.get("display_mode"),
            "translation_text": view.get("translation_text"),
            "source_event_hash": view.get("source_event_hash"),
        },
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "cold_events": cold_events,
        "cold_encounters": cold_encounters,
        "target_proposals": [],
    }


def fault_evidence(state):
    session = _start(state)
    try:
        first = session.say("Can I help?")
        root_evidence = session.read_root()["language_evidence"]
        receipts = [
            row["access_receipt_id"]
            for row in root_evidence
            if "HELP_INVITE" in row["evidence_id"]
        ]
        before_a = _a_speech(session)
        before_b = _b_speech(session)
        for receipt in receipts:
            session.revoke_language_access(receipt, reason="TEST_ONLY_S45_FAULT")
        failed = session.say("Can I help?")
        after_fail_a = _a_speech(session)
        after_fail_b = _b_speech(session)
        for receipt in receipts:
            session.restore_language_access(receipt, reason="TEST_ONLY_S45_RESTORE")
        restored = session.say("Can I help?")
        verify = session.verify()
    finally:
        session.close()
    return {
        "schema": "SOROK_S45_FAULT_EVIDENCE@1",
        "first_source_event_id": first["language"]["source_event_id"],
        "failed_status": failed.get("status"),
        "failed_reason": failed.get("reason"),
        "failed_has_language": bool(failed.get("language")),
        "failed_had_new_a_speech": after_fail_a != before_a,
        "failed_had_new_b_speech": after_fail_b != before_b,
        "restored_status": restored.get("status"),
        "restored_strategy": restored.get("strategy"),
        "restored_source_event_id": restored["language"]["source_event_id"],
        "restored_source_is_help_root": restored["language"]["source_event_id"] in {
            row["source_event_id"] for row in root_evidence
            if "HELP_INVITE" in row["evidence_id"]
        },
        "verify_ok": verify["ok"],
    }


def unsupported_evidence(state):
    session = _start(state)
    try:
        before_a = _a_speech(session)
        result = session.say("What is the weather?")
        after_a = _a_speech(session)
        encounter = session.read_encounters()[-1]
        verify = session.verify()
    finally:
        session.close()
    return {
        "schema": "SOROK_S45_UNSUPPORTED_EVIDENCE@1",
        "status": result.get("status"),
        "reason": result.get("reason"),
        "has_language": bool(result.get("language")),
        "new_a_speech": after_a != before_a,
        "encounter_status": encounter.get("status"),
        "encounter_speech_event_id": encounter.get("speech_event_id"),
        "verify_ok": verify["ok"],
    }


def denied_evidence(state):
    session = _start(state, seed="00" * 32)
    try:
        result = session.do_help()
        encounter = session.read_encounters()[-1]
        verify = session.verify()
        material = session.world().actor_state["A"]["material_remaining"]
    finally:
        session.close()
    return {
        "schema": "SOROK_S45_DENIED_EVIDENCE@1",
        "material_remaining": material,
        "status": result.get("status"),
        "accepted": result.get("accepted"),
        "strategy": result.get("strategy"),
        "action_event_id": (result.get("admission") or {}).get("action_event_id"),
        "native_text": (result.get("language") or {}).get("native_text"),
        "encounter_action_event_id": encounter.get("action_event_id"),
        "verify_ok": verify["ok"],
    }


def test_evidence():
    rows = {}
    for name, path, env in (
        ("s45", "tests", ENV),
        ("s44", str(S44_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S44_RETURN))),
        ("s43", str(S43_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S43_RETURN))),
    ):
        xml = JUNIT / f"{name}_full.xml"
        proc = _run(
            [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={xml}", path],
            f"{name}_full.log", env=env,
        )
        counts = _junit_counts(xml)
        rows[name] = {
            "exit": proc.returncode,
            "junit": str(xml.relative_to(RET)),
            "counts": {key: counts[key] for key in
                       ("tests", "PASS", "RED", "ERROR", "SKIP")},
        }
    return rows


def source_manifest():
    s44_rows = []
    for rel in S44_FILES:
        local = S44_RETURN / rel
        pinned = _git(
            "rev-parse",
            f"{CUTS['s44']}:WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1/{rel}",
        )
        local_blob = _git("hash-object", str(local))
        s44_rows.append({
            "path": rel,
            "pinned_git_blob_sha1": pinned,
            "local_git_blob_sha1": local_blob,
            "exact": pinned == local_blob,
            "sha256": _sha256(local),
        })
    local_rows = [{
        "path": rel,
        "sha256": _sha256(RET / rel),
        "git_blob_sha1": _git("hash-object", str(RET / rel)),
    } for rel in S45_FILES]
    origins = {}
    for name in ("s37", "s39", "s40", "s41", "s42", "s43", "s44", "s45", "s45.session"):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    bundle = root_bundle()
    root = generate_root(bundle)
    return {
        "schema": "SOROK_S45_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s44_reused": s44_rows,
        "s44_all_exact": all(row["exact"] for row in s44_rows),
        "s45_local": local_rows,
        "model_bundle_hash": bundle["bundle_hash"],
        "root_hash": root.root_hash,
        "root_seed_sha256": root.receipt["root_seed_sha256"],
        "imported_origins": origins,
        "s44_origin_accepted": "SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1"
        in origins.get("s44", ""),
        "s45_origin_local": "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1"
        in origins.get("s45.session", ""),
    }


def main():
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s45-evidence-", dir=str(RET)))
    try:
        consumer = consumer_evidence(work / "consumer")
        faults = fault_evidence(work / "faults")
        unsupported = unsupported_evidence(work / "unsupported")
        denied = denied_evidence(work / "denied")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s45.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S45_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        _write(EVID / "consumer.json", consumer)
        _write(EVID / "faults.json", faults)
        _write(EVID / "unsupported.json", unsupported)
        _write(EVID / "denied.json", denied)
        _write(EVID / "test_run.json", {
            "schema": "SOROK_S45_TEST_RUN@1", "rows": tests,
            "entrypoint_exit": entry.returncode,
        })
        _write(EVID / "source_manifest.json", source_manifest())
        print(json.dumps({
            "tests": {key: value["counts"] for key, value in tests.items()},
            "entrypoint_exit": entry.returncode,
            "consumer": {
                "root_hash": consumer["root_hash"],
                "events_after": consumer["events_after"],
                "encounter_count": consumer["encounter_count"],
                "do_help_accepted": consumer["do_help"]["accepted"],
                "no_new_b_speech": consumer["no_new_b_speech"],
                "verify_ok": consumer["verify_ok"],
                "cold_events": consumer["cold_events"],
                "cold_encounters": consumer["cold_encounters"],
            },
            "faults": faults,
            "unsupported": unsupported,
            "denied": denied,
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
