"""Generate S42 ongoing-event chain, boundaries, compatibility and source evidence."""
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
for path in (str(RET), str(RET / "tests")):
    if path not in sys.path:
        sys.path.insert(0, path)

from s42.bootstrap import CUTS, install, roots  # noqa: E402

install()

from s42.bindings import binding_episodes  # noqa: E402
from s42.session import S42Session  # noqa: E402
from s41.bindings import binding_episodes as s41_binding_episodes  # noqa: E402
from s41.event import S41EventRefusal  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402

S41_RETURN = Path(roots()["s41_return"])
S40_RETURN = Path(roots()["s40_return"])
S39_RETURN = Path(roots()["s39_return"])
S37_RETURN = Path(roots()["s37_return"])
S41_MANIFEST = S41_RETURN / "evidence" / "source_manifest.json"
S40_MANIFEST = S40_RETURN / "evidence" / "source_manifest.json"
S41_FILES = [
    "s41/__init__.py",
    "s41/bindings.py",
    "s41/bootstrap.py",
    "s41/event.py",
    "s41/history.py",
    "s41/performer.py",
    "s41/reader.py",
    "s41/session.py",
]
LOCAL_FILES = [
    ".gitignore",
    "00_RETURN.md",
    "run_s42.py",
    "run_s42_evidence.py",
    "s42/__init__.py",
    "s42/bindings.py",
    "s42/bootstrap.py",
    "s42/event.py",
    "s42/reader.py",
    "s42/session.py",
    "tests/conftest.py",
    "tests/test_s42_ongoing.py",
]
REPRODUCERS = [
    ("bad_history", S41_RETURN / "evidence" / "repro_bad_history.json",
     Path("/Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S41/evidence/repro_bad_history_reader.py")),
    ("generation_readset", S41_RETURN / "evidence" / "repro_generation_readset.json",
     Path("/Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S41_CLOSURE/evidence/repro_generation_readset.py")),
    ("generation_input", S41_RETURN / "evidence" / "repro_generation_input_source.json",
     Path("/Users/matthewsmith/repos/rawlsing-controller/.worktrees/sorok-incumbent-review/SOROK_REVIEW/S41_FINAL_CLOSURE/evidence/repro_generation_input_source.py")),
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


def _event_summary(row: dict) -> dict:
    language = row.get("language") or {}
    c9 = row.get("c9") or {}
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
        "language": language,
        "c9": c9,
        "history_refs": row.get("history_refs", []),
        "history_predicates": row.get("history_predicates", []),
        "world_tools_remaining": row.get("world_tools_remaining"),
        "world_clock_before": row.get("world_clock_before"),
        "world_clock_after": row.get("world_clock_after"),
        "target_proposals": row.get("target_proposals", []),
    }


def _admit(session, *, share: bool, history_ordinals: tuple[int, ...] = ()) -> dict:
    events = session.read_events()
    refs = tuple(events[index - 1]["e1_event_id"] for index in history_ordinals)
    return session.admit_event(
        case=case_for(share), source=source_for(case_for(share)),
        history_event_refs=refs,
    )


def chain_evidence(root: Path, length: int) -> dict:
    state = root / f"person-{length}"
    case = case_for(True)
    session = S42Session.start(state, case=case, source=source_for(case))
    session.close()
    stream = [
        (False, (1,)),
        (True, (1,)),
        (False, (3,)),
        (True, (3,)),
    ][: length - 1]
    for share, history in stream:
        session = S42Session.open(state)
        try:
            result = _admit(session, share=share, history_ordinals=history)
            assert result["status"] == "OK"
        finally:
            session.close()
    session = S42Session.open(state)
    try:
        events = session.read_events()
        verify = session.verify()
        clock = session.clock()
        tools = session.world().actor_state["A"]["tools_remaining"]
        tool_available = session.world().resources["workshop"]["tool_available"]
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(session.product.store.branch(session.branch_id)["actor_ids"])
        latest = session.read_latest()
        first_response = events[0]["c9"]["response_ref"]
        first_after = session.read_event(events[0]["e1_event_id"])
    finally:
        session.close()
    return {
        "length": length,
        "events": [_event_summary(row) for row in events],
        "latest_ordinal": latest["event_ordinal"],
        "root_actors": root_actors,
        "branch_actors": branch_actors,
        "clock": clock,
        "tools_remaining": tools,
        "tool_available": tool_available,
        "verify_ok": verify["ok"],
        "first_response_preserved": first_after["c9"]["response_ref"] == first_response,
        "checks": {
            "distinct_e1": len({row["e1_event_id"] for row in events}) == length,
            "distinct_c8": len({row["c8_occurrence_id"] for row in events}) == length,
            "increasing_times": all(
                events[index]["event_time"] < events[index + 1]["event_time"]
                for index in range(length - 1)
            ),
            "zero_targets": all(
                row["c9"]["target_branch"] == "NO_CHANGE"
                and row["c9"]["target_reason"] == "NO_PROPOSAL"
                and row["c9"]["target_proposals"] == []
                and row["c9"]["target_state_rows"] == 0
                for row in events
            ),
            "speaking_fidelity": all(
                (row.get("language") or {}).get("native_text")
                in (None, "¿Puedo usar la herramienta?")
                for row in events
            ),
            "tool_retained": tools == 1 and tool_available is True,
        },
    }


def boundary_evidence(root: Path) -> dict:
    session = S42Session.start(
        root / "boundary", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        _admit(session, share=False, history_ordinals=(1,))
        _admit(session, share=True, history_ordinals=(1,))
        events = session.read_events()
        before_bindings = len(binding_episodes(session))
        before_actions = len([
            event for event in session.events()
            if event.get("actor_id") == "A"
            and event.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}
        ])
        refusals = {}
        for label, refs in (
            ("reorder", (events[2]["e1_event_id"], events[0]["e1_event_id"])),
            ("duplicate", (events[0]["e1_event_id"], events[0]["e1_event_id"])),
            ("missing", ("TEST_ONLY_MISSING_HISTORY",)),
            ("wrong_hash", ("0" * 64,)),
        ):
            try:
                session.admit_event(
                    case=case_for(False), source=source_for(case_for(False)),
                    history_event_refs=refs,
                )
                refusals[label] = "ACCEPTED"
            except S41EventRefusal as exc:
                refusals[label] = exc.code
        event2 = events[1]
        try:
            session.admit_event(
                case=case_for(False), source=source_for(case_for(False)),
                history_event_refs=(event2["e1_event_id"],),
                event_time=event2["event_time"],
            )
            replay = "ACCEPTED"
        except S41EventRefusal as exc:
            replay = exc.code
        after_bindings = len(binding_episodes(session))
        after_actions = len([
            event for event in session.events()
            if event.get("actor_id") == "A"
            and event.get("kind") in {"SPEECH", "INSPECT", "REFUSAL"}
        ])
        verify = session.verify()["ok"]
    finally:
        session.close()

    open_session = S42Session.start(
        root / "open", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        opened = open_session.admit_event(
            case=case_for(False), source=source_for(case_for(False)),
            history_event_refs=(),
        )
        before_c9 = _c9_count(open_session)
        continued = _admit(open_session, share=True, history_ordinals=(1,))
        opened_event = opened["event"]
        open_verify = open_session.verify()["ok"]
        c9_after = _c9_count(open_session)
    finally:
        open_session.close()
    return {
        "schema": "SOROK_S42_BOUNDARY_EVIDENCE@1",
        "history_ref_refusals": refusals,
        "replay_refusal": replay,
        "bindings_unchanged": before_bindings == after_bindings,
        "actions_unchanged": before_actions == after_actions,
        "verify_ok": verify,
        "open_status": opened["status"],
        "open_event_status": opened_event["status"],
        "open_c9_absent": opened_event.get("c9") is None,
        "open_actor_action": opened["actor_action_appended"],
        "continue_after_open": continued["status"],
        "open_c9_unchanged": before_c9 == c9_after - 1,
        "open_verify_ok": open_verify,
    }


def _c9_count(session):
    import sqlite3
    conn = sqlite3.connect(session._c9_path())
    try:
        return conn.execute("SELECT count(*) FROM response").fetchone()[0]
    finally:
        conn.close()


def test_evidence() -> dict:
    xml = JUNIT / "s42_full.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s42_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S42_TEST_RUN@1",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def s41_compat_evidence() -> dict:
    xml = JUNIT / "s41_compat.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", str(S41_RETURN / "tests")],
        "s41_compat.log",
        env=dict(ENV, PYTHONPATH=str(S41_RETURN)),
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S42_S41_COMPAT@1",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
    }


def reproduced_s41_refusals() -> dict:
    rows = {}
    for label, manifest, oracle in REPRODUCERS:
        env = dict(ENV, S41_RETURN=str(S41_RETURN))
        proc = subprocess.run(
            [PY, str(oracle)], cwd=str(RET), env=env, capture_output=True, text=True
        )
        code = ""
        for line in reversed(proc.stderr.strip().splitlines()):
            if "Refusal:" in line:
                code = line.split("Refusal:", 1)[1].strip()
                break
        rows[label] = {"exit": proc.returncode, "refused": proc.returncode != 0,
                       "code": code, "manifest": str(manifest)}
    return {"schema": "SOROK_S42_S41_REPRODUCERS@1", "rows": rows,
            "all_refused": all(row["refused"] for row in rows.values())}


def source_manifest() -> dict:
    s41_manifest = json.loads(S41_MANIFEST.read_text()) if S41_MANIFEST.is_file() else {}
    s40_manifest = json.loads(S40_MANIFEST.read_text()) if S40_MANIFEST.is_file() else {}
    s41_rows = []
    for rel in S41_FILES:
        local = S41_RETURN / rel
        pinned = _git("rev-parse", f"{CUTS['s41']}:WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1/{rel}")
        local_blob = _git("hash-object", str(local))
        s41_rows.append({
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
        "s37", "s39", "s40", "s41", "s41.session", "s42", "s42.session",
        "s42.reader",
    ):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S42_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s41_reused": s41_rows,
        "s41_all_exact": all(row["exact"] for row in s41_rows),
        "accepted_manifests": {
            "s41": {
                "path": str(S41_MANIFEST),
                "s40_all_exact": s41_manifest.get("s40_all_exact"),
                "s39_all_exact": (s41_manifest.get("accepted_manifests", {}).get("s40") or {}).get("s39_all_exact"),
                "m35_all_exact": (s41_manifest.get("accepted_manifests", {}).get("s39") or {}).get("m35_all_exact"),
                "s36_all_exact": (s41_manifest.get("accepted_manifests", {}).get("s39") or {}).get("s36_all_exact"),
                "language_all_exact": (s41_manifest.get("accepted_manifests", {}).get("s39") or {}).get("language_all_exact"),
                "join_e_all_exact": (s41_manifest.get("accepted_manifests", {}).get("s39") or {}).get("join_e_all_exact"),
            },
            "s40": {
                "path": str(S40_MANIFEST),
                "s39_all_exact": s40_manifest.get("s39_all_exact"),
            },
        },
        "s42_local": local_rows,
        "imported_origins": origins,
        "candidate_origin_s36": "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1" in origins.get("candidate", ""),
        "s41_origin_accepted": "SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1" in origins.get("s41.session", ""),
        "s42_origin_local": "SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1" in origins.get("s42.session", ""),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s42-evidence-", dir=str(RET)))
    try:
        three = chain_evidence(work / "chains", 3)
        five = chain_evidence(work / "chains", 5)
        boundary = boundary_evidence(work / "boundary")
        tests = test_evidence()
        compat = s41_compat_evidence()
        repros = reproduced_s41_refusals()
        entry = _run([PY, "-B", "run_s42.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S42_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain3.json", three)
        _write(EVID / "chain5.json", five)
        _write(EVID / "boundary.json", boundary)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "s41_compat.json", compat)
        _write(EVID / "s41_reproducers.json", repros)
        _write(EVID / "source_manifest.json", manifest)
        print(json.dumps({
            "tests": tests["counts"],
            "s41_compat": compat["counts"],
            "s41_reproducers_all_refused": repros["all_refused"],
            "entrypoint_exit": entry.returncode,
            "chain3": three["checks"],
            "chain5": five["checks"],
            "boundary": boundary,
            "s41_all_exact": manifest["s41_all_exact"],
            "source_roots": manifest["candidate_origin_s36"]
            and manifest["s41_origin_accepted"] and manifest["s42_origin_local"],
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
