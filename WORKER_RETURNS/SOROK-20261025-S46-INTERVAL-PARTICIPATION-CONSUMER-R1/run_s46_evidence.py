"""Generate S46 actual/scheduled interval, fault, supersession and source evidence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from copy import deepcopy
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

from s46.bootstrap import CUTS, install, roots  # noqa: E402

install()

from candidate import digest  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s46.model import MODEL_HASH, OWNER_REGISTRY_HASH, make_domain  # noqa: E402
from s46.session import S46Session  # noqa: E402

S45_RETURN = Path(roots()["s45_return"])
S44_RETURN = Path(roots()["s44_return"])
S42_RETURN = Path(roots()["s42_return"])
S42_FILES = ["s42/session.py", "s42/event.py"]
REVIEW_DIR = Path(
    "/Users/matthewsmith/repos/rawlsing-controller/.worktrees/"
    "sorok-incumbent-review/SOROK_REVIEW/S46/evidence"
)
CLOSURE_REVIEW = Path(
    "/Users/matthewsmith/repos/rawlsing-controller/.worktrees/"
    "sorok-incumbent-review/SOROK_REVIEW/S46_CLOSURE/evidence/"
    "repro_self_rehashed_domain.py"
)
S45_FILES = [
    "s45/__init__.py", "s45/bootstrap.py", "s45/errors.py", "s45/fixtures.py",
    "s45/language.py", "s45/session.py", "tests/test_s45_generated_root_encounter.py",
]
S46_FILES = [
    ".gitignore", "00_RETURN.md", "run_s46.py", "run_s46_evidence.py",
    "s46/__init__.py", "s46/bootstrap.py", "s46/errors.py", "s46/model.py",
    "s46/producer.py", "s46/session.py",
    "tests/conftest.py", "tests/test_s46_interval_participation.py",
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


def _start(state):
    case = case_for(True)
    return S46Session.start(
        state, bundle=root_bundle("01" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )


def _scene_kinds(session):
    return [
        {"kind": row.get("kind"), "status": row.get("status")}
        for row in session.read_encounters()
    ]


def _run_one(state, mode):
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        before = session.world_prerequisites()
        before_b = dict(session.world().actor_state["B"])
        domain = make_domain(mode=mode, start=session.clock(),
                             end=session.clock() + 4)
        produced = session.produce_interval(domain)
        after = session.world_prerequisites()
        events = session.read_events()
        first = events[0]
        later = session.admit_event(
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
            event_time=session.clock() + 1,
        )
        world_readset = binding_episodes(session)[-1].get(
            "generation", {}
        ).get("world_prerequisites", {})
        said = session.say("Can I help?")
        helped = session.do_help()
        attended = session.attend()
        scenes = [
            {"kind": first.get("action_event_kind") or "SPEECH",
             "status": first.get("status")},
        ] + _scene_kinds(session)
        verify = session.verify()
        after_b = dict(session.world().actor_state["B"])
        interval = session.read_interval_states()[-1]
        state_event = session.event(interval["segments"][0]["world"].get(
            "actual_action_event_id", ""
        )) if interval["segments"][0]["world"].get(
            "actual_action_event_id"
        ) else None
    finally:
        session.close()
    cold = S46Session.open(state)
    try:
        cold_state = cold.read_interval_states()[-1]
        cold_verify = cold.verify()
    finally:
        cold.close()
    return {
        "schema": "SOROK_S46_ECOLOGY_EVIDENCE@1",
        "mode": mode,
        "root_hash": root_hash,
        "root_unchanged": cold_state["root_hash"] == root_hash,
        "interval_state_id": produced["state_id"],
        "interval_status": produced["status"],
        "coverage": produced["coverage"],
        "segment_statuses": [row["status"] for row in produced["segments"]],
        "attempts": [row["attempt"]["attempt"] for row in produced["segments"]],
        "action_event_ids": [
            row["world"]["actual_action_event_id"] for row in produced["segments"]
        ],
        "action_event_kind": state_event.get("kind") if state_event else "",
        "actual_daily_events_invented": produced["actual_daily_events_invented"],
        "actor_knowledge_inferred": produced["actor_knowledge_inferred"],
        "psychology_state_written": produced["psychology_state_written"],
        "world_prerequisites_before": before,
        "world_prerequisites_after": after,
        "s42_generation_world": world_readset,
        "s45_say_status": said.get("status"),
        "s45_do_help_status": helped.get("status"),
        "s45_do_help_accepted": helped.get("accepted"),
        "s45_do_help_strategy": helped.get("strategy"),
        "s45_attend_status": attended.get("status"),
        "scene_kinds": scenes,
        "later_s42_status": later.get("status"),
        "later_s42_selected_option": later["event"].get("selected_option"),
        "later_s42_attempt_status": later["event"].get("attempt_status"),
        "other_actor_preserved": before_b == after_b,
        "cold_interval_status": cold_state["status"],
        "cold_currentness": cold_state["currentness"],
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "target_proposals": [],
    }


def fault_evidence(state):
    session = _start(state)
    try:
        domain = make_domain(mode="ACTUAL", start=session.clock(),
                             end=session.clock() + 4)
        real = session.produce_interval(domain)
        forged_domain = deepcopy(real)
        forged_domain["domain_hash"] = "0" * 64
        forged_domain["state_id"] = "S46_STATE_" + digest({
            "domain": forged_domain["domain_hash"],
            "segments": forged_domain["segments"],
            "root": forged_domain["root_hash"],
        })[:24].upper()
        forged_domain["receipt_hash"] = digest({
            k: v for k, v in forged_domain.items()
            if k not in {"receipt_hash", "episode_id", "clock"}
        })
        try:
            session.validate_interval_state(forged_domain)
            domain_code = "ACCEPTED"
        except Exception as exc:
            domain_code = getattr(exc, "code", type(exc).__name__)
        forged_model = deepcopy(real)
        forged_model["model_hash"] = "0" * 64
        forged_model["receipt_hash"] = digest({
            k: v for k, v in forged_model.items()
            if k not in {"receipt_hash", "episode_id", "clock"}
        })
        try:
            session.validate_interval_state(forged_model)
            model_code = "ACCEPTED"
        except Exception as exc:
            model_code = getattr(exc, "code", type(exc).__name__)
        forged_owner = deepcopy(real)
        forged_owner["segments"][0]["world"]["source_owner"] = "FORGED_OWNER"
        forged_owner["state_id"] = "S46_STATE_" + digest({
            "domain": forged_owner["domain_hash"],
            "segments": forged_owner["segments"],
            "root": forged_owner["root_hash"],
        })[:24].upper()
        forged_owner["receipt_hash"] = digest({
            k: v for k, v in forged_owner.items()
            if k not in {"receipt_hash", "episode_id", "clock"}
        })
        try:
            session.validate_interval_state(forged_owner)
            owner_code = "ACCEPTED"
        except Exception as exc:
            owner_code = getattr(exc, "code", type(exc).__name__)
        forged_action = deepcopy(real)
        forged_action["segments"][0]["world"]["actual_action_event_id"] = (
            "TEST_ONLY_FORGED_ACTION"
        )
        forged_action["state_id"] = "S46_STATE_" + digest({
            "domain": forged_action["domain_hash"],
            "segments": forged_action["segments"],
            "root": forged_action["root_hash"],
        })[:24].upper()
        forged_action["receipt_hash"] = digest({
            k: v for k, v in forged_action.items()
            if k not in {"receipt_hash", "episode_id", "clock"}
        })
        try:
            session.validate_interval_state(forged_action)
            action_code = "ACCEPTED"
        except Exception as exc:
            action_code = getattr(exc, "code", type(exc).__name__)
        original = session.validate_interval_state(real)
        stored = session.read_interval_states()[-1]
        verify = session.verify()
    finally:
        session.close()
    cold = S46Session.open(state)
    try:
        cold_ok = cold.verify()["ok"]
        cold_status = cold.read_interval_states()[-1]["status"]
    finally:
        cold.close()
    return {
        "schema": "SOROK_S46_FAULT_EVIDENCE@1",
        "forged_domain_code": domain_code,
        "forged_model_code": model_code,
        "forged_owner_code": owner_code,
        "forged_action_code": action_code,
        "original_restored_status": original["status"],
        "stored_status": stored["status"],
        "stored_receipt_hash": stored["receipt_hash"],
        "warm_verify": verify["ok"],
        "cold_verify": cold_ok,
        "cold_status": cold_status,
    }


def blocked_evidence(state):
    session = _start(state)
    try:
        before = session.world().actor_state["A"]["material_remaining"]
        domain = make_domain(
            mode="BLOCKED", start=session.clock(), end=session.clock() + 2
        )
        produced = session.produce_interval(domain)
        return {
            "schema": "SOROK_S46_BLOCKED_EVIDENCE@1",
            "status": produced["status"],
            "attempts": [row["attempt"]["attempt"] for row in produced["segments"]],
            "world_statuses": [row["world"]["status"] for row in produced["segments"]],
            "action_event_ids": [
                row["world"]["actual_action_event_id"]
                for row in produced["segments"]
            ],
            "coverage": produced["coverage"],
            "material_before": before,
            "material_after": session.world().actor_state["A"][
                "material_remaining"
            ],
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()


def condition_evidence(state):
    session = _start(state)
    try:
        domain = make_domain(
            mode="ACTUAL", start=session.clock(), end=session.clock() + 4
        )
        produced = session.produce_interval(domain)
        state_id = produced["state_id"]
        first = session.read_events()[0]
        session.revoke_interval_condition(state_id, reason="TEST_ONLY_CUT")
        try:
            session.admit_event(
                case=case_for(True), source=source_for(case_for(True)),
                history_event_refs=(first["e1_event_id"],),
                event_time=session.clock() + 1,
            )
            refused = ""
        except Exception as exc:
            refused = getattr(exc, "code", type(exc).__name__)
        session.restore_interval_condition(state_id, reason="TEST_ONLY_RESTORE")
        restored = session.admit_event(
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
            event_time=session.clock() + 1,
        )
        world = binding_episodes(session)[-1]["generation"]["world_prerequisites"]
        return {
            "schema": "SOROK_S46_CONDITION_EVIDENCE@1",
            "state_id": state_id,
            "revoked_refusal": refused,
            "restored_s42_status": restored.get("status"),
            "restored_s46_state_id": world.get("s46_interval", {}).get(
                "state_id", ""
            ),
            "restored_s46_receipt": world.get("s46_interval", {}).get(
                "receipt_hash", ""
            ),
            "material_available": world.get("material_available"),
            "verify_ok": session.verify()["ok"],
        }
    finally:
        session.close()


def supersession_evidence(state):
    session = _start(state)
    try:
        first_domain = make_domain(
            mode="ACTUAL", start=session.clock(), end=session.clock() + 4
        )
        first = session.produce_interval(first_domain)
        second_domain = make_domain(
            mode="SCHEDULED_ONLY", start=session.clock(), end=session.clock() + 2
        )
        second = session.produce_interval(second_domain)
        rows = session.read_interval_states()
        current = session.current_interval_state()
        return {
            "schema": "SOROK_S46_SUPERSESSION_EVIDENCE@1",
            "first_state_id": first["state_id"],
            "first_status": rows[0]["status"],
            "first_currentness": rows[0]["currentness"],
            "first_superseded_by": rows[0]["superseded_by"],
            "second_state_id": second["state_id"],
            "second_status": rows[1]["status"],
            "second_currentness": rows[1]["currentness"],
            "current_state_id": current["state_id"] if current else "",
            "first_history_retained": rows[0]["coverage"] == first["coverage"],
        }
    finally:
        session.close()


def review_repro_evidence() -> dict:
    rows = {}
    for name in ("repro_blocked_mode", "repro_domain_forgery"):
        oracle = REVIEW_DIR / (name + ".py")
        env = dict(ENV, S46_RETURN=str(RET))
        proc = subprocess.run(
            [PY, str(oracle)], cwd=str(RET), env=env,
            capture_output=True, text=True,
        )
        (LOGS / (name + ".log")).write_text(proc.stdout + proc.stderr)
        code = ""
        for line in reversed(proc.stderr.strip().splitlines()):
            if "S46Refusal:" in line:
                code = line.split("S46Refusal:", 1)[1].strip()
                break
        rows[name] = {
            "oracle": str(oracle),
            "oracle_sha256": _sha256(oracle),
            "exit": proc.returncode,
            "refused": proc.returncode != 0,
            "code": code,
            "stdout": proc.stdout,
            "stderr_tail": proc.stderr.strip().splitlines()[-3:],
        }
    return {"schema": "SOROK_S46_REVIEW_REPRODUCERS@1", "rows": rows}


def closure_oracle_evidence() -> dict:
    env = dict(ENV, S46_RETURN=str(RET))
    proc = subprocess.run(
        [PY, str(CLOSURE_REVIEW)], cwd=str(RET), env=env,
        capture_output=True, text=True,
    )
    (LOGS / "repro_self_rehashed_domain.log").write_text(proc.stdout + proc.stderr)
    code = ""
    for line in reversed(proc.stderr.strip().splitlines()):
        if "S46Refusal:" in line:
            code = line.split("S46Refusal:", 1)[1].strip()
            break
    return {
        "schema": "SOROK_S46_SELF_REHASHED_DOMAIN_REPRO@1",
        "oracle": str(CLOSURE_REVIEW),
        "oracle_sha256": _sha256(CLOSURE_REVIEW),
        "exit": proc.returncode,
        "refused": proc.returncode != 0,
        "code": code,
        "stdout": proc.stdout,
        "stderr_tail": proc.stderr.strip().splitlines()[-3:],
    }


def test_evidence():
    rows = {}
    for name, path, env in (
        ("s46", "tests", ENV),
        ("s45", str(S45_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S45_RETURN))),
        ("s44", str(S44_RETURN / "tests"), dict(ENV, PYTHONPATH=str(S44_RETURN))),
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
    s45_rows = []
    for rel in S45_FILES:
        local = S45_RETURN / rel
        pinned = _git(
            "rev-parse",
            f"{CUTS['s45']}:WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1/{rel}",
        )
        local_blob = _git("hash-object", str(local))
        s45_rows.append({
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
    } for rel in S46_FILES]
    origins = {}
    for name in ("s37", "s39", "s40", "s41", "s42", "s43", "s44", "s45", "s46", "s46.session"):
        module = sys.modules.get(name)
        if module is not None:
            origins[name] = str(Path(getattr(module, "__file__", "")).resolve())
    bundle = root_bundle("01" * 32)
    return {
        "schema": "SOROK_S46_SOURCE_MANIFEST@1",
        "roots": roots(),
        "cuts": dict(CUTS),
        "s45_reused": s45_rows,
        "s45_all_exact": all(row["exact"] for row in s45_rows),
        "s42_seam": [
            {
                "path": rel,
                "sha256": _sha256(S42_RETURN / rel),
                "git_blob_sha1": _git("hash-object", str(S42_RETURN / rel)),
                "reason": "interval-condition hook used by S42 ongoing event admission",
            }
            for rel in S42_FILES
        ],
        "s46_local": local_rows,
        "model_hash": MODEL_HASH,
        "owner_registry_hash": OWNER_REGISTRY_HASH,
        "root_bundle_hash": bundle["bundle_hash"],
        "root_hash": __import__("s44.root", fromlist=["generate_root"]).generate_root(bundle).root_hash,
        "imported_origins": origins,
        "s45_origin_accepted": "SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1"
        in origins.get("s45", ""),
        "s46_origin_local": "SOROK-20261025-S46-INTERVAL-PARTICIPATION-CONSUMER-R1"
        in origins.get("s46.session", ""),
    }


def main():
    EVID.mkdir(exist_ok=True)
    JUNIT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="s46-evidence-", dir=str(RET)))
    try:
        actual = _run_one(work / "actual", "ACTUAL")
        scheduled = _run_one(work / "scheduled", "SCHEDULED_ONLY")
        faults = fault_evidence(work / "faults")
        blocked = blocked_evidence(work / "blocked")
        condition = condition_evidence(work / "condition")
        supersession = supersession_evidence(work / "supersession")
        tests = test_evidence()
        review_repros = review_repro_evidence()
        closure_oracle = closure_oracle_evidence()
        entry = _run([PY, "-B", "run_s46.py"], "entrypoint.log")
        if entry.returncode != 0:
            raise RuntimeError("S46_ENTRYPOINT_FAILED:" + entry.stderr)
        (EVID / "entrypoint.json").write_text(entry.stdout)
        _write(EVID / "actual.json", actual)
        _write(EVID / "scheduled.json", scheduled)
        _write(EVID / "faults.json", faults)
        _write(EVID / "blocked.json", blocked)
        _write(EVID / "condition.json", condition)
        _write(EVID / "supersession.json", supersession)
        _write(EVID / "test_run.json", {
            "schema": "SOROK_S46_TEST_RUN@1", "rows": tests,
            "entrypoint_exit": entry.returncode,
        })
        _write(EVID / "review_reproducers.json", review_repros)
        _write(EVID / "repro_self_rehashed_domain.json", closure_oracle)
        _write(EVID / "source_manifest.json", source_manifest())
        print(json.dumps({
            "tests": {key: value["counts"] for key, value in tests.items()},
            "entrypoint_exit": entry.returncode,
            "actual": {
                "root": actual["root_hash"], "status": actual["interval_status"],
                "coverage": actual["coverage"],
                "do_help_accepted": actual["s45_do_help_accepted"],
                "s42_material": actual["s42_generation_world"].get("material_available"),
                "cold": actual["cold_interval_status"],
            },
            "scheduled": {
                "root": scheduled["root_hash"], "status": scheduled["interval_status"],
                "coverage": scheduled["coverage"],
                "do_help_accepted": scheduled["s45_do_help_accepted"],
                "s42_material": scheduled["s42_generation_world"].get("material_available"),
            },
            "faults": faults,
            "review_reproducers": review_repros,
            "self_rehashed_domain": closure_oracle,
            "blocked": blocked,
            "condition": condition,
            "supersession": supersession,
        }, sort_keys=True))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
