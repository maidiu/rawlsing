"""Generate S43 integration, boundary, compatibility and source evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
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

from s43.bootstrap import CUTS, install, roots  # noqa: E402

install()

from language_mediation.plan import competent_languages  # noqa: E402
from s40.language import S40_PAIRS, S40_UNITS  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402
from s43.fixtures import seed_histories  # noqa: E402
from s43.planner import compile_historical_plan  # noqa: E402
from s43.session import S43Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s39.sources import context_records  # noqa: E402

S42_RETURN = Path(roots()["s42_return"])
S41_RETURN = Path(roots()["s41_return"])
S40_RETURN = Path(roots()["s40_return"])
REVIEW_FIRST_READER = Path(
    "/Users/matthewsmith/repos/rawlsing-controller/.worktrees/"
    "sorok-incumbent-review/SOROK_REVIEW/S43/evidence/repro_s40_first_reader.py"
)
S42_MANIFEST = S42_RETURN / "evidence" / "source_manifest.json"
S41_MANIFEST = S41_RETURN / "evidence" / "source_manifest.json"
S42_FILES = [
    "s42/__init__.py",
    "s42/bindings.py",
    "s42/bootstrap.py",
    "s42/event.py",
    "s42/reader.py",
    "s42/session.py",
]
LOCAL_FILES = [
    ".gitignore",
    "00_RETURN.md",
    "run_s43.py",
    "run_s43_evidence.py",
    "s43/__init__.py",
    "s43/bootstrap.py",
    "s43/errors.py",
    "s43/fixtures.py",
    "s43/performer.py",
    "s43/planner.py",
    "s43/reader.py",
    "s43/registry.py",
    "s43/repertoire.py",
    "s43/session.py",
    "tests/conftest.py",
    "tests/test_s43_historical_language.py",
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
        cases.append({
            "classname": case.attrib.get("classname", ""),
            "name": case.attrib.get("name", ""),
            "status": status,
        })
    return {
        "tests": tests,
        "PASS": tests - failures - errors - skips,
        "RED": failures,
        "ERROR": errors,
        "SKIP": skips,
        "cases": cases,
    }


def _start(state):
    case = case_for(True)
    session = S43Session.start(state, case=case, source=source_for(case))
    histories = seed_histories(session)
    session.close()
    return histories


def _admit(session, *, context, share=True, history_ordinal=1,
           source_records=None):
    events = session.read_events()
    return session.admit_event(
        language_context={"milieu_id": context},
        case=case_for(share),
        source=source_for(case_for(share)),
        history_event_refs=(events[history_ordinal - 1]["e1_event_id"],),
        source_records=source_records,
    )


def _b_speech_count(session):
    return len([
        event for event in session.events()
        if event.get("actor_id") == "B" and event.get("kind") == "SPEECH"
    ])


def _event_summary(session, result):
    read = session.read_s43_event(result["event"]["e1_event_id"])
    language = read.get("language") or {}
    s43 = read.get("s43") or {}
    return {
        "event_ordinal": read["event_ordinal"],
        "status": read["status"],
        "selected_option": read.get("selected_option"),
        "attempt_status": read.get("attempt_status"),
        "performed": read.get("performed"),
        "native_text": language.get("native_text", ""),
        "translation_text": language.get("translation_text", ""),
        "plan_hash": language.get("plan_hash", ""),
        "source_event_id": language.get("source_event_id", ""),
        "access_receipt_id": language.get("access_receipt_id", ""),
        "repertoire_id": s43.get("repertoire_id", ""),
        "repertoire_hash": s43.get("repertoire_hash", ""),
        "context": s43.get("context"),
        "selected_relation_ids": s43.get("selected_relation_ids", []),
        "selected_relations": s43.get("selected_relations", []),
        "contrary_relation_ids": s43.get("contrary_relation_ids", []),
        "contrary_relations": s43.get("contrary_relations", []),
        "source_grades": s43.get("source_grades", {}),
        "source_event_ids": sorted(
            row.get("event_id", "") for row in s43.get("source_event_refs", [])
        ),
        "generation_source_refs": list(read.get("generation_source_refs") or []),
        "currently_available": s43.get("currently_available"),
        "current_cache_status": s43.get("current_cache_status", ""),
        "target_branch": (read.get("c9") or {}).get("target_branch"),
        "target_reason": (read.get("c9") or {}).get("target_reason"),
        "target_proposals": (read.get("c9") or {}).get("target_proposals", []),
    }


def chain_evidence(root: Path) -> dict:
    state = root / "person"
    histories = _start(state)
    session = S43Session.open(state)
    try:
        before_b = _b_speech_count(session)
        second = _admit(session, context="family")
        second_read = _event_summary(session, second)
        after_b = _b_speech_count(session)
        second_event_hash = second["event"]["action_event_hash"]
        session.set_display_locale("es")
        view_en = session.language_view(second["event"]["action_event_id"], locale="en")
        view_es = session.language_view(second["event"]["action_event_id"], locale="es")
        locale_event_hash = session.event(second["event"]["action_event_id"])["hash"]
    finally:
        session.close()

    session = S43Session.open(state)
    try:
        third = _admit(session, context="workshop", share=False)
        third_read = _event_summary(session, third)
    finally:
        session.close()

    session = S43Session.open(state)
    try:
        fourth = _admit(session, context="family")
        fourth_read = _event_summary(session, fourth)
        index = session.language_index()
        verify = session.verify()
        clock = session.clock()
        tools = session.world().actor_state["A"]["tools_remaining"]
        root_actors = sorted(session.product.store.branch("root")["actor_ids"])
        branch_actors = sorted(session.product.store.branch(session.branch_id)["actor_ids"])
    finally:
        session.close()

    return {
        "schema": "SOROK_S43_HISTORICAL_LANGUAGE_CHAIN@1",
        "histories": {
            "family_independence_relation": histories["family_independence"]["encounter"]["encounter_id"],
            "work_independence_relation": histories["work_independence"]["encounter"]["encounter_id"],
            "family_independence_source": histories["family_independence"]["event"]["event_id"],
            "work_independence_source": histories["work_independence"]["event"]["event_id"],
            "family_request_relation": histories["family_request_relation"],
            "work_request_relation": histories["work_request_relation"],
            "family_request_source": histories["family_request_source"],
            "work_request_source": histories["work_request_source"],
        },
        "events": [second_read, third_read, fourth_read],
        "index_relations": len(index["relations"]),
        "index_contradictions": len(index["contradictions_preserved"]),
        "index_cache_status": index["cache_status"],
        "verify_ok": verify["ok"],
        "clock": clock,
        "tools_remaining": tools,
        "root_actors": root_actors,
        "branch_actors": branch_actors,
        "cold_reopen_per_admission": True,
        "no_new_b_source_during_event2": before_b == after_b,
        "second_event_hash": second_event_hash,
        "locale_view_en": {
            "display_mode": view_en.get("display_mode"),
            "translation_text": view_en.get("translation_text"),
            "source_event_hash": view_en.get("source_event_hash"),
        },
        "locale_view_es": {
            "display_mode": view_es.get("display_mode"),
            "translation_text": view_es.get("translation_text"),
            "source_event_hash": view_es.get("source_event_hash"),
        },
        "locale_did_not_change_event": locale_event_hash == second_event_hash,
        "checks": {
            "family_and_work_selected_differently": (
                second_read["selected_relation_ids"] != third_read["selected_relation_ids"]
            ),
            "family_work_contrary_preserved": (
                histories["work_request_relation"] in second_read["contrary_relation_ids"]
                and histories["family_request_relation"] in third_read["contrary_relation_ids"]
            ),
            "same_native_english_pair": (
                second_read["native_text"] == third_read["native_text"] == "¿Puedo usar la herramienta?"
                and second_read["translation_text"] == third_read["translation_text"] == "May I use the tool?"
            ),
            "source_grades_present": bool(second_read["source_grades"]),
            "zero_targets": all(
                row["target_branch"] == "NO_CHANGE"
                and row["target_reason"] == "NO_PROPOSAL"
                and row["target_proposals"] == []
                for row in (second_read, third_read, fourth_read)
            ),
            "private_generation_sources_absent": all(
                not (set(row["source_event_ids"]) & set(row["generation_source_refs"]))
                for row in (second_read, third_read, fourth_read)
            ),
        },
    }


def boundary_evidence(root: Path) -> dict:
    state = root / "required-source"
    histories = _start(state)
    session = S43Session.open(state)
    try:
        before_b = _b_speech_count(session)
        second = _admit(session, context="family")
        second_language = second["event"]["language"]
        source_id = second_language["source_event_id"]
        source_hash = second_language["source_event_hash"]
        receipt_id = second_language["access_receipt_id"]
        second_action_hash = second["event"]["action_event_hash"]
        clock_before = session.clock()
        cache_before_revoke = session.language_index()["cache_status"]
        session.revoke_language_access(receipt_id, reason="TEST_ONLY_REQUIRED_SOURCE")
        clock_after = session.clock()
        cache_after_revoke = session.language_index()["cache_status"]
        denied = _admit(session, context="family")
        denied_attempt = binding_episodes(session)[-1]["attempt"]
        b_after_denied = _b_speech_count(session)
        second_current = session.read_s43_event(
            second["event"]["e1_event_id"]
        )["s43"]
        session.restore_language_access(receipt_id, reason="TEST_ONLY_RESTORE_REQUIRED")
        restored = _admit(session, context="family")
        cache_after_restore = session.language_index()["cache_status"]
        restored_language = restored["event"]["language"]
        restored_s43 = session.read_s43_event(
            restored["event"]["e1_event_id"]
        )["s43"]
        b_after_restored = _b_speech_count(session)
        second_event_after = session.event(second["event"]["action_event_id"])
    finally:
        session.close()

    state = root / "contrary-source"
    contrary_histories = _start(state)
    session = S43Session.open(state)
    try:
        session.revoke_language_access(
            contrary_histories["family_counter_receipt"],
            reason="TEST_ONLY_CONTRARY_SOURCE",
        )
        index = session.language_index()
        work = _admit(session, context="workshop")
        work_s43 = session.read_s43_event(work["event"]["e1_event_id"])["s43"]
        family = _admit(session, context="family")
        session.restore_language_access(
            contrary_histories["family_counter_receipt"],
            reason="TEST_ONLY_RESTORE_CONTRARY",
        )
        restored_family = _admit(session, context="family")
        restored_family_s43 = session.read_s43_event(
            restored_family["event"]["e1_event_id"]
        )["s43"]
    finally:
        session.close()

    return {
        "schema": "SOROK_S43_HISTORICAL_LANGUAGE_BOUNDARY@1",
        "zero_targets": all(
            row["event"].get("c9", {}).get("target_branch") == "NO_CHANGE"
            and row["event"].get("c9", {}).get("target_reason") == "NO_PROPOSAL"
            and row["event"].get("c9", {}).get("target_proposals") == []
            for row in (denied, restored)
        ),
        "required_source": {
            "event_time_fixed": clock_before == clock_after,
            "cache_status_before_revoke": cache_before_revoke,
            "cache_status_after_revoke": cache_after_revoke,
            "cache_status_after_restore": cache_after_restore,
            "denied_attempt_status": denied["event"].get("attempt_status"),
            "denied_performed": denied["event"].get("performed"),
            "denied_reason": denied_attempt.get("reason"),
            "no_replacement_b_source": before_b == b_after_denied == b_after_restored,
            "earlier_source_hash_preserved": second_event_after["hash"] == second_action_hash,
            "earlier_repertoire_available_after_revoke": second_current.get("currently_available"),
            "restored_source_same": restored_language.get("source_event_id") == source_id,
            "restored_source_hash_same": restored_language.get("source_event_hash") == source_hash,
            "restored_relation_ids_same": (
                restored_s43.get("selected_relation_ids")
                == second_current.get("selected_relation_ids")
            ),
            "restored_repertoire_hash_same": (
                restored_s43.get("repertoire_hash")
                == second_current.get("repertoire_hash")
            ),
        },
        "contrary_source": {
            "family_invalidated": contrary_histories["family_request_relation"] not in {
                row["relation_id"] for row in index["relations"]
            },
            "work_preserved": contrary_histories["work_request_relation"] in {
                row["relation_id"] for row in index["relations"]
            },
            "work_still_admitted": work["event"].get("attempt_status"),
            "family_refused": family["event"].get("attempt_status"),
            "work_selected": work_s43.get("selected_relation_ids"),
            "family_invalidated_ids": work_s43.get("invalidated_relation_ids"),
            "restored_family_selected": restored_family_s43.get("selected_relation_ids"),
        },
        "world_person_clock_preserved_on_revoke": clock_before == clock_after,
    }


def wrong_binding_evidence(root: Path) -> dict:
    rows = {}
    for name, declared_branch, declared_hash in (
        ("wrong_branch", "other-branch", None),
        ("wrong_hash", None, "0" * 64),
    ):
        state = root / name
        case = case_for(True)
        session = S43Session.start(state, case=case, source=source_for(case))
        try:
            session.admit_language_encounter(
                text="¿Puedo usar la herramienta?",
                concept_id="concept:request-tool",
                milieu_id="family",
                sense_id="sense:family-request",
                relation_label="AFFIRMED",
                atoms=["TOOL_REQUEST_WORKSHOP"],
                access_declared_branch=declared_branch,
                access_declared_hash=declared_hash,
            )
            try:
                session.language_index()
                code = "ACCEPTED"
            except Exception as exc:
                code = getattr(exc, "code", type(exc).__name__)
            rows[name] = code
        finally:
            session.close()
    for name, field, value in (
        ("wrong_source_hash", "source_event_hash", "0" * 64),
        ("wrong_source_branch", "branch_id", "other-branch"),
    ):
        state = root / name
        case = case_for(True)
        session = S43Session.start(state, case=case, source=source_for(case))
        try:
            encounter = session.admit_language_encounter(
                text="¿Puedo usar la herramienta?",
                concept_id="concept:request-tool",
                milieu_id="family",
                sense_id="sense:family-request",
                relation_label="AFFIRMED",
                atoms=["TOOL_REQUEST_WORKSHOP"],
            )
            body = dict(encounter["encounter"])
            body[field] = value
            body["encounter_id"] = "S43_TAMPERED_" + name.upper()
            session.product._append_episode(
                session.branch_id, "A", "LANGUAGE_ENCOUNTER",
                session.clock(), body,
            )
            try:
                session.language_index()
                code = "ACCEPTED"
            except Exception as exc:
                code = getattr(exc, "code", type(exc).__name__)
            rows[name] = code
        finally:
            session.close()
    return {"schema": "SOROK_S43_WRONG_BINDINGS@1", "rows": rows}


def comparison_evidence(root: Path) -> dict:
    state = root / "compare"
    _start(state)
    session = S43Session.open(state)
    try:
        second = _admit(session, context="family")
        read = session.read_s43_event(second["event"]["e1_event_id"])
        s43 = read["s43"]
        index = session.language_index()
        contract = {}
        baseline_iterations = 1000
        start = time.perf_counter()
        for _ in range(baseline_iterations):
            unit = S40_UNITS["REQUEST_TOOL"]
            pair = S40_PAIRS[unit["pair_id"]]
            _ = (unit["unit_id"], pair["native_text"], pair["target_text"])
        baseline_seconds = time.perf_counter() - start
        source_iterations = 3
        start = time.perf_counter()
        for _ in range(source_iterations):
            current_index = session.language_index()
            compile_historical_plan(
                session,
                intent="REQUEST_TOOL",
                context={"milieu_id": "family"},
                contract=contract,
                index=current_index,
            )
        source_seconds = time.perf_counter() - start
    finally:
        session.close()
    source_ids = {row["event_id"] for row in s43.get("source_event_refs", [])}
    generation_ids = set(read.get("generation_source_refs") or [])
    return {
        "schema": "SOROK_S43_LIMITED_COMPARISON@1",
        "quality_benchmark": "NOT_RUN",
        "cultural_superiority_claim": False,
        "baseline": {
            "name": "S40_FINITE_REGISTRY_LOOKUP",
            "source_event_coverage": 0,
            "auto_creates_source_at_speech": True,
            "contradiction_groups": 0,
            "contrary_relations": 0,
            "private_generation_sources_in_plan": False,
            "ordinary_native_text": S40_PAIRS["pair_s40_request_tool"]["native_text"],
            "ordinary_translation_text": S40_PAIRS["pair_s40_request_tool"]["target_text"],
            "measured_ms": baseline_seconds * 1000.0,
            "iterations": baseline_iterations,
        },
        "source_bound": {
            "name": "S43_HISTORICAL_REPERTOIRE",
            "source_event_coverage": len(source_ids),
            "auto_creates_source_at_speech": False,
            "contradiction_groups": len(s43.get("contradictions") or []),
            "contrary_relations": len(s43.get("contrary_relation_ids") or []),
            "private_generation_sources_in_plan": bool(
                source_ids & generation_ids
            ),
            "ordinary_native_text": read["language"]["native_text"],
            "ordinary_translation_text": read["language"]["translation_text"],
            "measured_ms": source_seconds * 1000.0 / source_iterations,
            "iterations": source_iterations,
        },
        "limited_reading": {
            "source_coverage_delta": len(source_ids),
            "contradiction_retention_delta": len(s43.get("contradictions") or []),
            "private_exclusion_holds": not bool(source_ids & generation_ids),
            "same_ordinary_wording": (
                read["language"]["native_text"]
                == S40_PAIRS["pair_s40_request_tool"]["native_text"]
                and read["language"]["translation_text"]
                == S40_PAIRS["pair_s40_request_tool"]["target_text"]
            ),
            "runtime_not_a_quality_claim": True,
        },
    }


def first_reader_evidence() -> dict:
    env = dict(ENV, S43_RETURN=str(RET))
    proc = subprocess.run(
        [PY, str(REVIEW_FIRST_READER)], cwd=str(RET), env=env,
        capture_output=True, text=True,
    )
    (LOGS / "repro_s40_first_reader.log").write_text(proc.stdout + proc.stderr)
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        report = {}
    return {
        "schema": "SOROK_S43_S40_FIRST_READER_REPRO@1",
        "oracle": str(REVIEW_FIRST_READER),
        "oracle_sha256": _sha256(REVIEW_FIRST_READER),
        "exit": proc.returncode,
        "refused": proc.returncode != 0,
        "report": report,
        "stderr_tail": proc.stderr.strip().splitlines()[-3:],
    }


def test_evidence() -> dict:
    xml = JUNIT / "s43_full.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", "tests"],
        "s43_full.log",
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S43_TEST_RUN@1",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
        "cases": counts["cases"],
    }


def s42_compat_evidence() -> dict:
    xml = JUNIT / "s42_compat.xml"
    proc = _run(
        [PY, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml}", str(S42_RETURN / "tests")],
        "s42_compat.log",
        env=dict(ENV, PYTHONPATH=str(S42_RETURN)),
    )
    counts = _junit_counts(xml)
    return {
        "schema": "SOROK_S43_S42_COMPAT@1",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
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
        "schema": "SOROK_S43_S41_COMPAT@1",
        "exit": proc.returncode,
        "junit": str(xml.relative_to(RET)),
        "counts": {key: counts[key] for key in ("tests", "PASS", "RED", "ERROR", "SKIP")},
    }


def source_manifest() -> dict:
    s42_manifest = json.loads(S42_MANIFEST.read_text()) if S42_MANIFEST.is_file() else {}
    s41_manifest = json.loads(S41_MANIFEST.read_text()) if S41_MANIFEST.is_file() else {}
    s42_rows = []
    for rel in S42_FILES:
        local = S42_RETURN / rel
        pinned = _git(
            "rev-parse",
            f"{CUTS['s42']}:WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/{rel}",
        )
        local_blob = _git("hash-object", str(local))
        s42_rows.append({
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
        "candidate", "language_mediation.session", "s37", "s39", "s40",
        "s41", "s42", "s43", "s43.session", "s43.planner", "s43.repertoire",
    ):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    return {
        "schema": "SOROK_S43_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s42_reused": s42_rows,
        "s42_all_exact": all(row["exact"] for row in s42_rows),
        "accepted_manifests": {
            "s42": {
                "path": str(S42_MANIFEST),
                "s41_all_exact": s42_manifest.get("s41_all_exact"),
            },
            "s41": {
                "path": str(S41_MANIFEST),
                "s40_all_exact": s41_manifest.get("s40_all_exact"),
            },
        },
        "s43_local": local_rows,
        "imported_origins": origins,
        "s42_origin_accepted": "SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1" in (
            origins.get("s42.session") or origins.get("s42", "")
        ),
        "s43_origin_local": "SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1" in origins.get("s43.session", ""),
        "language_origin_accepted": "LANGUAGE_MEDIATION_R1" in origins.get("language_mediation.session", ""),
    }


def main() -> None:
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s43-evidence-", dir=str(RET)))
    try:
        chain = chain_evidence(work / "chain")
        boundary = boundary_evidence(work / "boundary")
        wrong = wrong_binding_evidence(work / "wrong")
        comparison = comparison_evidence(work / "comparison")
        tests = test_evidence()
        first_reader = first_reader_evidence()
        s42_compat = s42_compat_evidence()
        s41_compat = s41_compat_evidence()
        entry = _run([PY, "-B", "run_s43.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S43_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        manifest = source_manifest()
        _write(EVID / "chain.json", chain)
        _write(EVID / "boundary.json", boundary)
        _write(EVID / "wrong_bindings.json", wrong)
        _write(EVID / "comparison.json", comparison)
        _write(EVID / "test_run.json", tests)
        _write(EVID / "repro_s40_first_reader.json", first_reader)
        _write(EVID / "s42_compat.json", s42_compat)
        _write(EVID / "s41_compat.json", s41_compat)
        _write(EVID / "source_manifest.json", manifest)
        print(json.dumps({
            "tests": tests["counts"],
            "first_reader_refused": first_reader["refused"],
            "first_reader_report": first_reader["report"],
            "s42_compat": s42_compat["counts"],
            "s41_compat": s41_compat["counts"],
            "entrypoint_exit": entry.returncode,
            "chain_checks": chain["checks"],
            "boundary": boundary,
            "wrong_bindings": wrong["rows"],
            "comparison": comparison["limited_reading"],
            "s42_all_exact": manifest["s42_all_exact"],
            "origins": {
                "s42": manifest["s42_origin_accepted"],
                "s43": manifest["s43_origin_local"],
                "language": manifest["language_origin_accepted"],
            },
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
