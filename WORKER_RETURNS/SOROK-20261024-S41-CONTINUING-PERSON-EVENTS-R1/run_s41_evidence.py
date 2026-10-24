"""Generate S41 two-event continuation, boundary and source evidence."""
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

from s41.bootstrap import CUTS, install, roots  # noqa: E402

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from candidate.actor_access_response import make_actor_local_access_witness  # noqa: E402
from s41.bindings import binding_episodes  # noqa: E402
from s41.event import (  # noqa: E402
    ContinuationProducer,
    build_second_occurrence,
    history_record_from_prior,
    world_prerequisites,
)
from s41.reader import S41ReadRefusal  # noqa: E402
from s41.session import S41Session  # noqa: E402
from s39.model import S39GenerationRefusal  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402

S40_RETURN = Path(roots()["s40_return"])
S39_RETURN = Path(roots()["s39_return"])
S37_RETURN = Path(roots()["s37_return"])
S40_MANIFEST = S40_RETURN / "evidence" / "source_manifest.json"
S39_MANIFEST = S39_RETURN / "evidence" / "source_manifest.json"
S37_MANIFEST = S37_RETURN / "evidence" / "source_manifest.json"
S40_FILES = [
    "s40/__init__.py",
    "s40/bootstrap.py",
    "s40/language.py",
    "s40/performer.py",
    "s40/reader.py",
    "s40/session.py",
]
LOCAL_FILES = [
    ".gitignore",
    "00_RETURN.md",
    "run_s41.py",
    "run_s41_evidence.py",
    "s41/__init__.py",
    "s41/bindings.py",
    "s41/bootstrap.py",
    "s41/event.py",
    "s41/performer.py",
    "s41/reader.py",
    "s41/session.py",
    "tests/conftest.py",
    "tests/test_s41_continuation.py",
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
    xml = JUNIT / "s41_full.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s41_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S41_TEST_RUN@1",
        "command": f"{PY} -B -m pytest -q -p no:cacheprovider --junitxml={xml} tests",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def _event_summary(row: dict) -> dict:
    return {
        "event_ordinal": row["event_ordinal"],
        "status": row["status"],
        "e1_event_id": row["e1_event_id"],
        "e1_event_hash": row["e1_event_hash"],
        "c8_occurrence_id": row["c8_occurrence_id"],
        "c8_state_digest": row["c8_state_digest"],
        "source_operation": row["source_operation"],
        "event_time": row["event_time"],
        "selected_option": row.get("selected_option"),
        "attempt_status": row.get("attempt_status"),
        "performed": row.get("performed"),
        "action_event_id": row.get("action_event_id", ""),
        "action_event_hash": row.get("action_event_hash", ""),
        "language": row.get("language"),
        "c9": row.get("c9"),
        "history_refs": row.get("history_refs", []),
        "history_predicate": row.get("history_predicate"),
        "generation_source_refs": row.get("generation_source_refs", []),
        "world_tools_remaining": row.get("world_tools_remaining"),
        "world_clock_before": row.get("world_clock_before"),
        "world_clock_after": row.get("world_clock_after"),
        "target_proposals": row.get("target_proposals", []),
        "provenance": row.get("provenance"),
    }


def chain_evidence(root: Path) -> dict:
    state = root / "person"
    session = S41Session.start(state, case=case_for(True), source=source_for(case_for(True)))
    try:
        first = session.read_events()[0]
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(session.product.store.branch(session.branch_id)["actor_ids"])
        first_clock = session.clock()
        first_action = first["action_event_id"]
    finally:
        session.close()
    session = S41Session.open(state)
    try:
        result = session.continue_event(case=case_for(False), source=source_for(case_for(False)))
        events = session.read_events()
        latest = session.read_latest()
        verify = session.verify()
        clock = session.clock()
        tools = session.world().actor_state["A"]["tools_remaining"]
        tool_available = session.world().resources["workshop"]["tool_available"]
        first_after = session.read_event(first["e1_event_id"])
        second_read = session.read_event(events[1]["e1_event_id"])
        view = session.language_view(second_read["action_event_id"], locale="en")
    finally:
        session.close()
    cold = S41Session.open(state)
    try:
        cold_events = cold.read_events()
        cold_verify = cold.verify()
        cold_latest = cold.read_latest()
    finally:
        cold.close()
    return {
        "schema": "SOROK_S41_TWO_EVENT_CHAIN@1",
        "grade": "TEST_ONLY_SOURCEFREE_CONTINUING_PERSON_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "root_actors": root_actors,
        "branch_actors": branch_actors,
        "first_clock": first_clock,
        "first_action_event_id": first_action,
        "continue_status": result["status"],
        "actor_action_appended": result["actor_action_appended"],
        "events": [_event_summary(row) for row in events],
        "latest_ordinal": latest["event_ordinal"],
        "first_after_second": _event_summary(first_after),
        "second_language_view": {
            "status": view["status"],
            "display_mode": view["display_mode"],
            "translation_text": view["translation_text"],
        },
        "clock": clock,
        "tools_remaining": tools,
        "tool_available": tool_available,
        "verify_ok": verify["ok"],
        "checks": {
            "same_root": sorted(root_actors) == ["A", "B"],
            "same_branch": sorted(branch_actors) == ["A", "B", "U"],
            "distinct_e1": events[0]["e1_event_id"] != events[1]["e1_event_id"],
            "distinct_e1_hash": events[0]["e1_event_hash"] != events[1]["e1_event_hash"],
            "distinct_c8": events[0]["c8_occurrence_id"] != events[1]["c8_occurrence_id"],
            "increasing_clocks": events[1]["event_time"] > events[0]["event_time"]
            and clock > first_clock,
            "tool_retained": tools == 1 and tool_available is True,
            "first_bytes_preserved": first_after["c9"]["response_ref"]
            == first["c9"]["response_ref"] and first_after["e1_event_hash"]
            == first["e1_event_hash"],
            "prior_fact_cited": events[1]["history_predicate"] == "PRIOR_B_SHARE"
            and events[1]["history_refs"][0]["e1_event_id"] == events[0]["e1_event_id"]
            and any(ref.startswith("TEST_ONLY_S41_HIST_")
                    for ref in events[1]["generation_source_refs"]),
            "zero_targets": events[0]["c9"]["target_proposals"] == []
            and events[1]["c9"]["target_proposals"] == []
            and events[0]["c9"]["target_state_rows"] == 0
            and events[1]["c9"]["target_state_rows"] == 0,
            "speaking_fidelity": events[1]["language"]["native_text"]
            == "¿Puedo usar la herramienta?"
            and events[1]["language"]["translation_text"] == "May I use the tool?",
            "cold_both_valid": cold_verify["ok"] and len(cold_events) == 2
            and cold_latest["event_ordinal"] == 2,
        },
        "cold": {
            "events": [_event_summary(row) for row in cold_events],
            "latest_ordinal": cold_latest["event_ordinal"],
            "verify_ok": cold_verify["ok"],
        },
    }


def open_evidence(root: Path) -> dict:
    session = S41Session.start(
        root / "open", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        before = len([e for e in session.events()
                      if e.get("actor_id") == "A"
                      and e.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}])
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False)),
            source_records=[],
        )
        after = len([e for e in session.events()
                     if e.get("actor_id") == "A"
                     and e.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}])
        dup = None
        try:
            session.continue_event(
                case=case_for(False), source=source_for(case_for(False))
            )
        except Exception as exc:
            dup = getattr(exc, "code", type(exc).__name__)
        return {
            "schema": "SOROK_S41_OPEN_EVIDENCE@1",
            "continue_status": result["status"],
            "event_status": result["event"]["status"],
            "generation_status": result["event"]["generation_status"],
            "actor_action_appended": result["actor_action_appended"],
            "a_action_events_before": before,
            "a_action_events_after": after,
            "duplicate_code": dup,
            "bindings": len(binding_episodes(session)),
        }
    finally:
        session.close()


def denial_evidence(root: Path) -> dict:
    session = S41Session.start(
        root / "denial", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        take = session.product.take_tool("A")
        result = session.continue_event(
            case=case_for(False), source=source_for(case_for(False))
        )
        row = result["event"]
        return {
            "schema": "SOROK_S41_DENIAL_EVIDENCE@1",
            "take_tool_status": take["status"],
            "continue_status": result["status"],
            "attempt_status": row.get("attempt_status"),
            "performed": row.get("performed"),
            "language": row.get("language"),
            "action_event_id": row.get("action_event_id"),
            "c9": row.get("c9"),
            "world_tools_remaining": row.get("world_tools_remaining"),
            "world_tool_available": (row.get("world_after") or {}).get(
                "resources", {}
            ).get("workshop", {}).get("tool_available"),
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()


def tamper_evidence(root: Path) -> dict:
    session = S41Session.start(
        root / "tamper", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        first = session.read_events()[0]
        first_binding = binding_episodes(session)[0]
        first_binding_hash = first_binding["hash"]
        first_response = first["c9"]["response_ref"]
        c8_event = C8ReadOnlyConsumer(
            first_binding["c8"]["journal_path"]
        ).load().get(first_binding["c8"]["occurrence_id"])
        second_case = case_for(False)
        second_source = source_for(second_case)
        occurrence, _ = build_second_occurrence(
            session,
            first_binding=first_binding,
            first_payload=c8_event["payload"],
            second_source=second_source,
            event_time=session.clock() + 1,
        )
        producer = ContinuationProducer(
            session.state_root / "source",
            case=second_case,
            source=second_source,
            occurrence=occurrence,
            current_tools=session.world().actor_state["A"]["tools_remaining"],
        )
        try:
            producer.commit_incoming()
            as_of = occurrence.event_time + 5
            history = history_record_from_prior(
                session, first_binding=first_binding, as_of=as_of
            )
            records = context_records(
                actor_id=session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
                branch_id=session.branch_id,
                as_of=as_of,
                repair_urgent=True,
                avoid_debt=True,
            ) + [history]
            tampered = dict(history)
            tampered["content"] = {"mapped_from_e1_event_id": "WRONG"}
            try:
                producer.generate(
                    source_records=records[:-1] + [tampered],
                    branch_id=session.branch_id,
                    world=world_prerequisites(session),
                )
                history_status = "ACCEPTED"
                history_code = ""
            except S39GenerationRefusal as exc:
                history_status = "REFUSED"
                history_code = exc.code
            restored = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
            revoked = make_actor_local_access_witness(
                actor_id=producer.occurrence.actor_id,
                event_ref=producer.e1_event["hash"],
                access_time=producer.event_time,
                source_ref="TEST_ONLY_ADP017_ACCESS_S41_WRONG",
                access_status="ACCESSIBLE",
                scene="workshop",
                revoked=True,
            )
            try:
                producer.generate(
                    source_records=records,
                    branch_id=session.branch_id,
                    world=world_prerequisites(session),
                    access_witness=revoked,
                )
                access_status = "ACCEPTED"
                access_code = ""
            except S39GenerationRefusal as exc:
                access_status = "REFUSED"
                access_code = exc.code
            restored_again = producer.generate(
                source_records=records,
                branch_id=session.branch_id,
                world=world_prerequisites(session),
            )
        finally:
            producer.close()
        first_after = session.read_event(first["e1_event_id"])
        return {
            "schema": "SOROK_S41_TAMPER_EVIDENCE@1",
            "history_status": history_status,
            "history_code": history_code,
            "history_restored": restored["selected_option"],
            "access_status": access_status,
            "access_code": access_code,
            "access_restored": restored_again["selected_option"],
            "first_binding_hash_preserved": binding_episodes(session)[0]["hash"]
            == first_binding_hash,
            "first_response_preserved": first_after["c9"]["response_ref"]
            == first_response,
            "first_event_status": first_after["status"],
            "bindings_after_probe": len(binding_episodes(session)),
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()


def mismatch_evidence(root: Path) -> dict:
    session = S41Session.start(
        root / "mismatch", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        session.continue_event(case=case_for(False), source=source_for(case_for(False)))
        first, second = session.read_events()
        rows = [
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == "LANGUAGE_TRANSLATION_PROJECTION"
            and (row.get("body") or {}).get("source_speech_event_id")
            == second["action_event_id"]
        ]
        body = dict(rows[0]["body"])
        body["plan_hash"] = "0" * 64
        body["tamper_note"] = "s41-second-plan-mismatch"
        session.product._append_episode(
            session.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
            session.clock(), body,
        )
        try:
            session.read_event(second["e1_event_id"])
            warm_status = "ACCEPTED"
            warm_code = ""
        except S41ReadRefusal as exc:
            warm_status = "REFUSED"
            warm_code = exc.code
        first_status = session.read_event(first["e1_event_id"])["status"]
        verify = session.verify()["ok"]
    finally:
        session.close()
    try:
        S41Session.open(root / "mismatch")
        cold_status = "ACCEPTED"
    except Exception as exc:
        cold_status = "REFUSED"
    return {
        "schema": "SOROK_S41_MISMATCH_EVIDENCE@1",
        "warm_status": warm_status,
        "warm_code": warm_code,
        "first_event_status_after_second_mismatch": first_status,
        "warm_verify_ok": verify,
        "cold_status": cold_status,
    }


def source_manifest() -> dict:
    s40_manifest = json.loads(S40_MANIFEST.read_text()) if S40_MANIFEST.is_file() else {}
    s39_manifest = json.loads(S39_MANIFEST.read_text()) if S39_MANIFEST.is_file() else {}
    s37_manifest = json.loads(S37_MANIFEST.read_text()) if S37_MANIFEST.is_file() else {}
    s40_rows = []
    for rel in S40_FILES:
        local = S40_RETURN / rel
        pinned = _git("rev-parse", f"{CUTS['s40']}:WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1/{rel}")
        local_blob = _git("hash-object", str(local))
        s40_rows.append({
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
        "s37", "s37.session", "s39", "s39.session", "s40", "s40.session",
        "s40.performer", "s41", "s41.session", "s41.event", "s41.reader",
    ):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S41_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s40_reused": s40_rows,
        "s40_all_exact": all(row["exact"] for row in s40_rows),
        "accepted_manifests": {
            "s40": {
                "path": str(S40_MANIFEST),
                "s39_all_exact": s40_manifest.get("s39_all_exact"),
                "s37_all_exact": (s40_manifest.get("accepted_manifests", {}).get("s39") or {}).get("s37_all_exact"),
            },
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
        "s41_local": local_rows,
        "imported_origins": origins,
        "candidate_origin_s36": "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1" in origins.get("candidate", ""),
        "s40_origin_accepted": "SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1" in origins.get("s40.session", ""),
        "s41_origin_local": "SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1" in origins.get("s41.session", ""),
        "out9_note": "Accepted read_out9 hard-requires exactly one occurrence ID. S41 uses a bounded adapter over the same C8ReadOnlyConsumer/ingress for a later occurrence; prior bytes are retained.",
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s41-evidence-", dir=str(RET)))
    try:
        chain = chain_evidence(work / "chain")
        opened = open_evidence(work / "open")
        denial = denial_evidence(work / "denial")
        tamper = tamper_evidence(work / "tamper")
        mismatch = mismatch_evidence(work / "mismatch")
        tests = test_evidence()
        entry = _run([PY, "-B", "run_s41.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S41_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain.json", chain)
        _write(EVID / "open.json", opened)
        _write(EVID / "denial.json", denial)
        _write(EVID / "tamper.json", tamper)
        _write(EVID / "mismatch.json", mismatch)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "source_manifest.json", manifest)
        print(json.dumps({
            "tests": tests["counts"],
            "entrypoint_exit": entry.returncode,
            "chain_checks": chain["checks"],
            "open": opened,
            "denial": denial,
            "tamper": tamper,
            "mismatch": mismatch,
            "s40_all_exact": manifest["s40_all_exact"],
            "source_roots": manifest["candidate_origin_s36"]
            and manifest["s40_origin_accepted"] and manifest["s41_origin_local"],
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
