"""Generate S40 native-speech/language/chain/boundary/source evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
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
for path in (str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s40.bootstrap import CUTS, install, roots  # noqa: E402

install()

from s40.language import S40LanguageRefusal  # noqa: E402
from s40.reader import S40ReadRefusal  # noqa: E402
from s40.session import S40GeneratedSession  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from run_s40 import run_one  # noqa: E402

S39_RETURN = Path(roots()["s39_return"])
S37_RETURN = Path(roots()["s37_return"])
S39_MANIFEST = S39_RETURN / "evidence" / "source_manifest.json"
S37_MANIFEST = S37_RETURN / "evidence" / "source_manifest.json"
S39_FILES = [
    "s39/__init__.py",
    "s39/bootstrap.py",
    "s39/model.py",
    "s39/performer.py",
    "s39/producer.py",
    "s39/reader.py",
    "s39/session.py",
    "s39/sources.py",
]
LOCAL_FILES = [
    ".gitignore",
    "00_RETURN.md",
    "run_s40.py",
    "run_s40_evidence.py",
    "s40/__init__.py",
    "s40/bootstrap.py",
    "s40/language.py",
    "s40/performer.py",
    "s40/reader.py",
    "s40/session.py",
    "tests/conftest.py",
    "tests/test_s40_native_speech.py",
    "tests/test_s40_boundaries.py",
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


def _run(cmd, log_name: str):
    proc = subprocess.run(cmd, cwd=str(RET), env=ENV, capture_output=True, text=True)
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


def test_evidence() -> dict:
    xml = JUNIT / "s40_full.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s40_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S40_TEST_RUN@1",
        "command": f"{PY} -B -m pytest -q -p no:cacheprovider --junitxml={xml} tests",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def chain_evidence(root: Path) -> dict:
    chains = [
        run_one(root, label="share-request", share=True, context="request"),
        run_one(root, label="share-refusal-speech", share=True, context="refusal"),
        run_one(root, label="refuse-denied", share=False, context="request"),
        run_one(root, label="share-attend-nonverbal", share=True, context="attend"),
    ]
    return {
        "schema": "SOROK_S40_CHAIN_EVIDENCE@1",
        "grade": "TEST_ONLY_S40_GENERATED_INTENT_LANGUAGE_MODEL_PREMISE_NOT_GENERAL_TRANSLATION",
        "native": False,
        "provider_calls": 0,
        "chains": chains,
        "generated_request_speech": (
            chains[0]["selected_option"] == "REQUEST_TOOL"
            and chains[0]["attempt_status"] == "ADMITTED"
            and chains[0]["language_status"] == "ACCEPTED"
            and chains[0]["native_text"] == "¿Puedo usar la herramienta?"
            and chains[0]["translation_text"] == "May I use the tool?"
            and chains[0]["s36_outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        ),
        "generated_refusal_speech": (
            chains[1]["selected_option"] == "EXPLICIT_REFUSAL"
            and chains[1]["language_status"] == "ACCEPTED"
            and chains[1]["native_text"] == "No, ahora no."
            and chains[1]["translation_text"] == "No, not now."
            and chains[1]["s36_outcome"] == "OBSERVED_CURRENT_REFUSAL"
        ),
        "denied_no_speech": (
            chains[2]["attempt_status"] == "DENIED"
            and chains[2]["language_status"] == "NONE"
            and chains[2]["speech_event_id"] == ""
            and chains[2]["s36_outcome"] == "RECEIVABLE_NO_OBSERVED_UPTAKE"
        ),
        "nonverbal_no_speech": (
            chains[3]["selected_option"] == "ATTEND_OBJECT"
            and chains[3]["language_status"] == "NONVERBAL"
            and chains[3]["speech_event_id"] == ""
            and chains[3]["s36_outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        ),
        "both_zero_target": all(
            row["target_branch"] == "NO_CHANGE"
            and row["target_reason"] == "NO_PROPOSAL"
            and row["target_proposals"] == []
            and row["target_state_rows"] == 0
            for row in chains
        ),
        "both_cold_verify": all(row["cold"]["verify_ok"] for row in chains),
    }


def language_evidence(root: Path) -> dict:
    case = case_for(True)
    state = root / "language"
    session = S40GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        s40 = session.read_s40()
        event = session.event(s40["speech_event_id"])
        lme = event["body"]["lme"]
        admission = session._admission_for(s40["plan_hash"], s40["speech_event_id"])
        projection = session._projection(s40["speech_event_id"])
        view = session.language_view(s40["speech_event_id"], locale="en")
        generation = session.read_generation()["generation"]
        plan = admission.get("plan") or {}
        facts = (plan.get("readset") or {}).get("public_outward_facts") or []
        e1_fact = next(
            (row for row in facts if row.get("kind") == "ADMITTED_E1"), None
        )
        private_refs = set(generation["source_refs"])
        language_refs = {row.get("event_id", "") for row in lme["source_event_refs"]}
        evidence = {
            "selected_option": s40["selected_option"],
            "intent": s40["selected_option"],
            "native_text": s40["native_text"],
            "translation_text": s40["translation_text"],
            "language_tag": s40["language_tag"],
            "target_language_tag": s40["target_language_tag"],
            "plan_hash": s40["plan_hash"],
            "native_artifact_hash": s40["native_artifact_hash"],
            "translation_artifact_hash": s40["translation_artifact_hash"],
            "equivalence_receipt_hash": s40["equivalence_receipt_hash"],
            "equivalence_status": view["equivalence"]["status"],
            "source_event_id": s40["source_event_id"],
            "source_event_hash": s40["source_event_hash"],
            "access_receipt_id": s40["access_receipt_id"],
            "speech_event_id": s40["speech_event_id"],
            "speech_event_hash": s40["speech_event_hash"],
            "admission_id": s40["admission_id"],
            "projection_episode_id": s40["projection_episode_id"],
            "plan_public_e1_fact": e1_fact,
            "actual_c8_e1_event_id": session.meta["c8"]["e1_event_id"],
            "actual_c8_e1_event_hash": session.meta["c8"]["e1_event_hash"],
            "plan_e1_fact_matches_actual": bool(
                e1_fact
                and e1_fact.get("event_id") == session.meta["c8"]["e1_event_id"]
                and e1_fact.get("event_hash") == session.meta["c8"]["e1_event_hash"]
            ),
            "lme_source_event_refs": lme["source_event_refs"],
            "lme_access_receipt_ids": lme["access_receipt_ids"],
            "admission_plan_hash": (admission.get("plan") or {}).get("plan_hash"),
            "projection_plan_hash": projection.get("plan_hash"),
            "view_status": view["status"],
            "view_display_mode": view["display_mode"],
            "view_translation_text": view["translation_text"],
            "private_generation_refs": sorted(private_refs),
            "private_refs_exposed": bool(private_refs.intersection(language_refs)),
            "s36": s40["s36"],
            "provenance": s40["provenance"],
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()
    cold = S40GeneratedSession.open(state)
    try:
        cold_s40 = cold.read_s40()
        cold_view = cold.language_view(cold_s40["speech_event_id"], locale="en")
        evidence["cold"] = {
            "speech_event_hash": cold_s40["speech_event_hash"],
            "plan_hash": cold_s40["plan_hash"],
            "native_text": cold_s40["native_text"],
            "translation_text": cold_s40["translation_text"],
            "view_status": cold_view["status"],
            "view_translation_text": cold_view["translation_text"],
            "agrees": (
                cold_s40["speech_event_hash"] == evidence["speech_event_hash"]
                and cold_s40["plan_hash"] == evidence["plan_hash"]
                and cold_s40["translation_text"] == evidence["translation_text"]
            ),
            "verify_ok": cold.verify()["ok"],
        }
    finally:
        cold.close()
    return {"schema": "SOROK_S40_LANGUAGE_EVIDENCE@1", **evidence}


def competence_evidence(root: Path) -> dict:
    case = case_for(True)
    state = root / "no-competence"
    try:
        S40GeneratedSession.start(
            state, case=case, source=source_for(case), language_competence=False
        )
        status = "ACCEPTED"
        code = ""
    except S40LanguageRefusal as exc:
        status = "REFUSED"
        code = exc.code
    speech_events = 0
    c12 = state / "product" / "c12.sqlite"
    if c12.is_file():
        conn = sqlite3.connect(c12)
        try:
            speech_events = sum(
                1 for (body,) in conn.execute("SELECT body FROM world_event")
                if json.loads(body).get("kind") == "SPEECH"
            )
        finally:
            conn.close()
    responses = 0
    c9 = state / "source" / "bp2" / "c9.sqlite"
    if c9.is_file():
        conn = sqlite3.connect(c9)
        try:
            responses = conn.execute("SELECT count(*) FROM response").fetchone()[0]
        finally:
            conn.close()
    restored = S40GeneratedSession.start(
        root / "restored", case=case, source=source_for(case)
    )
    try:
        restored_s40 = restored.read_s40()
        restored_ok = restored.verify()["ok"]
    finally:
        restored.close()
    return {
        "schema": "SOROK_S40_COMPETENCE_FAILURE_EVIDENCE@1",
        "refusal_status": status,
        "refusal_code": code,
        "speech_events_after_refusal": speech_events,
        "c9_responses_after_refusal": responses,
        "restored_language_status": restored_s40["language_status"],
        "restored_native_text": restored_s40["native_text"],
        "restored_verify_ok": restored_ok,
    }


def mismatch_evidence(root: Path) -> dict:
    case = case_for(True)
    state = root / "mismatch"
    session = S40GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        s40 = session.read_s40()
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "LANGUAGE_TRANSLATION_PROJECTION"
        ]
        assert len(rows) == 1
        body = dict(rows[0]["body"])
        body["plan_hash"] = "0" * 64
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
            session.clock(), body,
        )
        try:
            session.read_s40()
            status = "ACCEPTED"
            code = ""
        except S40ReadRefusal as exc:
            status = "REFUSED"
            code = exc.code
        verify_ok = session.verify()["ok"]
    finally:
        session.close()
    try:
        S40GeneratedSession.open(state)
        cold_status = "ACCEPTED"
        cold_code = ""
    except Exception as exc:
        cold_status = "REFUSED"
        cold_code = getattr(exc, "code", type(exc).__name__)
    return {
        "schema": "SOROK_S40_MISMATCH_EVIDENCE@1",
        "warm_status": status,
        "warm_code": code,
        "warm_verify_ok": verify_ok,
        "cold_status": cold_status,
        "cold_code": cold_code,
    }


def source_manifest() -> dict:
    s39_manifest = json.loads(S39_MANIFEST.read_text()) if S39_MANIFEST.is_file() else {}
    s37_manifest = json.loads(S37_MANIFEST.read_text()) if S37_MANIFEST.is_file() else {}
    s39_rows = []
    for rel in S39_FILES:
        local = S39_RETURN / rel
        pinned = _git("rev-parse", f"{CUTS['s39']}:WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/{rel}")
        local_blob = _git("hash-object", str(local))
        s39_rows.append({
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
    } for rel in LOCAL_FILES]
    origins = {}
    for name in (
        "candidate", "bp2_joined", "joined.session", "language_mediation.session",
        "s37", "s37.session", "s39", "s39.session", "s39.performer", "s39.reader",
        "s40", "s40.session", "s40.performer", "s40.reader", "s40.language",
    ):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S40_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s39_reused": s39_rows,
        "s39_all_exact": all(row["exact"] for row in s39_rows),
        "accepted_manifests": {
            "s39": {
                "path": str(S39_MANIFEST),
                "s37_all_exact": s39_manifest.get("s37_all_exact"),
                "m35_all_exact": (s39_manifest.get("s37_accepted_manifest") or {}).get("m35_all_exact"),
                "s36_all_exact": (s39_manifest.get("s37_accepted_manifest") or {}).get("s36_all_exact"),
                "language_all_exact": (s39_manifest.get("s37_accepted_manifest") or {}).get("language_all_exact"),
                "join_e_all_exact": (s39_manifest.get("s37_accepted_manifest") or {}).get("join_e_all_exact"),
            },
            "s37": {
                "path": str(S37_MANIFEST),
                "m35_all_exact": s37_manifest.get("m35_all_exact"),
                "s36_all_exact": s37_manifest.get("s36_all_exact"),
                "language_all_exact": s37_manifest.get("language_all_exact"),
                "join_e_all_exact": s37_manifest.get("join_e_all_exact"),
            },
        },
        "s40_local": local_rows,
        "imported_origins": origins,
        "candidate_origin_s36": "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1" in origins.get("candidate", ""),
        "s39_origin_accepted": "SOROK-20261024-S39-GENERATED-RESPONSE-R1" in origins.get("s39.session", ""),
        "s40_origin_local": "SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1" in origins.get("s40.session", ""),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s40-evidence-", dir=str(RET)))
    try:
        chains = chain_evidence(work / "chains")
        language = language_evidence(work / "language")
        competence = competence_evidence(work / "competence")
        mismatch = mismatch_evidence(work / "mismatch")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s40.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S40_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain.json", chains)
        _write(EVID / "language.json", language)
        _write(EVID / "competence.json", competence)
        _write(EVID / "mismatch.json", mismatch)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "source_manifest.json", manifest)
        print(json.dumps({
            "tests": tests["counts"],
            "entrypoint_exit": entry.returncode,
            "generated_request_speech": chains["generated_request_speech"],
            "generated_refusal_speech": chains["generated_refusal_speech"],
            "denied_no_speech": chains["denied_no_speech"],
            "nonverbal_no_speech": chains["nonverbal_no_speech"],
            "both_zero_target": chains["both_zero_target"],
            "both_cold_verify": chains["both_cold_verify"],
            "language_private_refs_exposed": language["private_refs_exposed"],
            "language_cold_agrees": language["cold"]["agrees"],
            "competence_refusal": competence["refusal_code"],
            "competence_no_speech": competence["speech_events_after_refusal"] == 0,
            "competence_no_c9": competence["c9_responses_after_refusal"] == 0,
            "competence_restored": competence["restored_verify_ok"],
            "mismatch_warm": mismatch["warm_status"],
            "mismatch_cold": mismatch["cold_status"],
            "s39_all_exact": manifest["s39_all_exact"],
            "source_roots": manifest["candidate_origin_s36"]
            and manifest["s39_origin_accepted"] and manifest["s40_origin_local"],
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
