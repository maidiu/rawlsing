"""Fresh CLI for the pinned S45 encounter and S46/S47 interval-C9 product spine."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .bootstrap import PRODUCT, install, roots
from .audit import loaded_modules, verify_sources

SCHEMA = "SOROK_S45_S47_PRODUCT_CLI@1"
SCRIPT = PRODUCT / "run_s45_s47.py"
PROJECTION_RETURN = Path(
    os.environ.get(
        "SOROK_S45_S47_PROJECTION_ROOT",
        str(PRODUCT.parents[1] / "SOROK-S45-S47-PROJECTION-20261105-R1"),
    )
)


def _json(value) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _session_types():
    install()
    from s45.session import S45Session
    from s47.session import S47Session

    return S45Session, S47Session


def _fixture_helpers():
    install()
    from s37.harness import case_for, source_for
    from s45.fixtures import root_bundle

    return case_for, source_for, root_bundle


def _start_s45(state: Path, seed: str = "01" * 32):
    S45Session, _ = _session_types()
    case_for, source_for, root_bundle = _fixture_helpers()
    case = case_for(True)
    return S45Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _start_s47(state: Path, seed: str = "01" * 32):
    _, S47Session = _session_types()
    case_for, source_for, root_bundle = _fixture_helpers()
    case = case_for(True)
    return S47Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )



def _projection(session):
    install()
    text = str(PROJECTION_RETURN)
    if text not in sys.path:
        sys.path.insert(0, text)
    from s45_projection.adapter import S45Projection

    return S45Projection(session)


def _open_s47(state: Path):
    _, S47Session = _session_types()
    return S47Session.open(state)


def _admit(session, event_ref: str | None = None):
    case_for, source_for, _ = _fixture_helpers()
    event = session.event(event_ref) if event_ref else session.read_events()[0]
    case = case_for(True)
    return session.admit_event(
        case=case,
        source=source_for(case),
        history_event_refs=(event["e1_event_id"],),
        event_time=session.clock() + 1,
    )


def _encounter_summary(session) -> list[dict]:
    return [
        {
            "kind": row.get("kind"),
            "status": row.get("status"),
            "reason": row.get("reason"),
            "strategy": row.get("strategy"),
            "accepted": None,
            "speech_event_id": row.get("speech_event_id"),
            "action_event_id": row.get("action_event_id"),
            "native_text": row.get("native_text"),
            "translation_text": row.get("translation_text"),
        }
        for row in session.read_encounters()
    ]


def _do_help_summary(result: dict) -> dict:
    return {
        "status": result.get("status"),
        "accepted": result.get("accepted"),
        "reason": result.get("reason"),
        "strategy": result.get("strategy"),
        "speech_event_id": (result.get("admission") or {}).get("speech_event_id"),
        "action_event_id": (result.get("admission") or {}).get("action_event_id"),
        "native_text": (result.get("language") or {}).get("native_text"),
        "translation_text": (result.get("language") or {}).get("translation_text"),
    }


def _c9_summary(read: dict) -> dict:
    return {
        "event_ref": read.get("event_ref"),
        "selected_event_ref": read.get("selected_event_ref"),
        "response_status": read.get("response_status"),
        "s47_source_ref": read.get("s47_source_ref"),
        "s47_source_hash": read.get("s47_source_hash"),
        "s47_source_in_readset": read.get("s47_source_in_readset"),
        "s47_source_currentness": read.get("s47_source_currentness"),
        "s47_source_coverage": read.get("s47_source_coverage"),
        "current_source_ref": read.get("current_source_ref"),
        "current_source_hash": read.get("current_source_hash"),
        "objective_material_eligible": read.get("objective_material_eligible"),
        "objective_material_refs": read.get("objective_material_refs"),
        "target_branch": read.get("target_branch"),
        "target_reason": read.get("target_reason"),
        "target_proposals": read.get("target_proposals"),
        "readset_refs": read.get("readset_refs"),
        "present_condition_revoked": read.get("present_condition_revoked"),
        "historical_condition_revoked": read.get("historical_condition_revoked"),
    }


def _interval_summary(produced: dict) -> dict:
    return {
        "state_id": produced.get("state_id"),
        "status": produced.get("status"),
        "coverage": produced.get("coverage"),
        "segment_statuses": [row.get("status") for row in produced.get("segments", [])],
        "mode": (produced.get("domain") or {}).get("mode"),
        "start": produced.get("start"),
        "end": produced.get("end"),
        "actual_daily_events_invented": produced.get("actual_daily_events_invented"),
        "actor_knowledge_inferred": produced.get("actor_knowledge_inferred"),
        "psychology_state_written": produced.get("psychology_state_written"),
    }



def _privacy_ok(value) -> bool:
    from s45_projection import projection as projection_module

    def walk(item) -> bool:
        if isinstance(item, dict):
            for key, child in item.items():
                if key in projection_module.PRIVATE_KEYS:
                    return False
                if not walk(child):
                    return False
        elif isinstance(item, (list, tuple)):
            for child in item:
                if not walk(child):
                    return False
        elif isinstance(item, str):
            if any(marker in item for marker in projection_module.FORBIDDEN_VALUE_MARKERS):
                return False
        return True

    return walk(value)

def _scenario_s45(root: Path) -> dict:
    S45Session, _ = _session_types()
    state = root / "s45"
    session = _start_s45(state)
    adapter = _projection(session)
    try:
        said = adapter.say("Can I help?")
        helped = adapter.do_help()
        attended = adapter.attend()
        view = adapter.view()
        encounters = _encounter_summary(session)
        event_count = len(session.read_events())
        verify = session.verify()
        root_hash = session.read_root()["root_hash"]
    finally:
        adapter.close()
    cold = S45Session.open(state)
    try:
        cold_verify = cold.verify()
        cold_counts = (len(cold.read_events()), len(cold.read_encounters()))
        cold_root_hash = cold.read_root()["root_hash"]
    finally:
        cold.close()
    checks = {
        "say_ok_invite": said.get("status") == "OK"
        and (said.get("actor_response") or {}).get("strategy") == "HELP_INVITE",
        "do_help_accept": helped.get("status") == "OK"
        and (helped.get("actor_response") or {}).get("strategy") == "HELP_ACCEPT"
        and (helped.get("actor_response") or {}).get("performed") is True,
        "attend_no_change": attended.get("status") == "NO_CHANGE"
        and attended.get("world_event_created") is False,
        "three_scenes": [row["kind"] for row in encounters] == ["SAY", "DO_HELP", "ATTEND"],
        "privacy": _privacy_ok({
            "say": said, "do_help": helped, "attend": attended, "view": view,
        }),
        "verify_ok": bool(verify.get("ok") and cold_verify.get("ok")),
        "cold_same_root": cold_root_hash == root_hash,
        "cold_same_counts": cold_counts == (event_count, len(encounters)),
    }
    return {
        "state": str(state),
        "root_hash": root_hash,
        "event_count": event_count,
        "encounters": encounters,
        "say": said,
        "do_help": helped,
        "attend": attended,
        "view": view,
        "cold_event_and_encounter_counts": list(cold_counts),
        "checks": checks,
        "ok": all(checks.values()),
    }


def _scenario_mode(root: Path, mode: str) -> dict:
    state = root / ("s47-" + mode.lower())
    session = _start_s47(state)
    adapter = _projection(session)
    try:
        domain_start = session.clock()
        from s46.model import make_domain

        produced = session.produce_interval(
            make_domain(mode=mode, start=domain_start, end=domain_start + 4)
        )
        material_after_interval = session.world().actor_state["A"]["material_remaining"]
        source = session.c9_interval_source()
        admitted = _admit(session)
        event_ref = admitted["event"]["e1_event_id"]
        c9 = session.read_c9_conditioning(event_ref)
        said = adapter.say("Can I help?")
        helped = adapter.do_help()
        attended = adapter.attend()
        view = adapter.view()
        encounters = _encounter_summary(session)
        verify = session.verify()
        root_hash = session.read_root()["root_hash"]
    finally:
        adapter.close()
    cold = _open_s47(state)
    try:
        cold_c9 = cold.read_c9_conditioning(event_ref)
        cold_verify = cold.verify()
        cold_root_hash = cold.read_root()["root_hash"]
    finally:
        cold.close()
    expected_material = 0 if mode == "ACTUAL" else 1
    expected_c9 = mode != "ACTUAL"
    expected_accept = mode != "ACTUAL"
    say_response = said.get("actor_response") or {}
    help_response = helped.get("actor_response") or {}
    checks = {
        "material_after_interval": material_after_interval == expected_material,
        "c9_source_in_readset": c9.get("s47_source_in_readset") is True,
        "c9_objective_material": c9.get("objective_material_eligible") is expected_c9,
        "c9_targetless": c9.get("target_branch") == "NO_CHANGE"
        and c9.get("target_reason") == "NO_PROPOSAL",
        "say_attempt_not_performance": said.get("attempted") is True
        and said.get("performed") is False,
        "say_response_matches_material": (
            say_response.get("strategy") == "HELP_INVITE"
            if expected_accept
            else say_response.get("strategy") == "HELP_REFUSE"
        ),
        "do_help_matches_material": (
            helped.get("status") == "OK"
            and help_response.get("strategy") == "HELP_ACCEPT"
            and help_response.get("performed") is True
            and helped.get("refusal") is False
            if expected_accept
            else helped.get("status") == "REFUSED"
            and help_response.get("strategy") == "HELP_REFUSE"
            and help_response.get("performed") is False
            and helped.get("refusal") is True
        ),
        "attend_no_change": attended.get("status") == "NO_CHANGE"
        and attended.get("world_event_created") is False,
        "three_scenes": [row["kind"] for row in encounters] == ["SAY", "DO_HELP", "ATTEND"],
        "privacy": _privacy_ok({
            "say": said, "do_help": helped, "attend": attended, "view": view,
        }),
        "c9_source_is_event_local": c9.get("s47_source_ref") == (source or {}).get("source_ref"),
        "cold_c9_same_source": cold_c9.get("s47_source_hash") == c9.get("s47_source_hash"),
        "verify_ok": bool(verify.get("ok") and cold_verify.get("ok")),
        "cold_same_root": cold_root_hash == root_hash,
    }
    return {
        "state": str(state),
        "mode": mode,
        "root_hash": root_hash,
        "material_after_interval": material_after_interval,
        "interval": _interval_summary(produced),
        "source": {
            "source_ref": (source or {}).get("source_ref"),
            "source_hash": (source or {}).get("source_hash"),
            "access": ((source or {}).get("content") or {}).get("access"),
        },
        "admission": {
            "status": admitted.get("status"),
            "event_ref": event_ref,
            "selected_option": admitted["event"].get("selected_option"),
            "attempt_status": admitted["event"].get("attempt_status"),
        },
        "c9": _c9_summary(c9),
        "say": said,
        "do_help": helped,
        "attend": attended,
        "view": view,
        "encounters": encounters,
        "cold_c9": _c9_summary(cold_c9),
        "checks": checks,
        "ok": all(checks.values()),
    }


def _scenario_event_local(root: Path) -> dict:
    state = root / "event-local"
    session = _start_s47(state)
    try:
        from s46.model import make_domain

        session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        first_source = session.c9_interval_source()
        first_admitted = _admit(session)
        first_ref = first_admitted["event"]["e1_event_id"]

        session.produce_interval(
            make_domain(
                mode="SCHEDULED_ONLY", start=session.clock(), end=session.clock() + 2
            )
        )
        second_source = session.c9_interval_source()
        second_admitted = _admit(session)
        second_ref = second_admitted["event"]["e1_event_id"]

        first_read = session.read_c9_conditioning(first_ref)
        second_read = session.read_c9_conditioning(second_ref)
        verify = session.verify()
    finally:
        session.close()
    cold = _open_s47(state)
    try:
        cold_first = cold.read_c9_conditioning(first_ref)
        cold_verify = cold.verify()
    finally:
        cold.close()
    checks = {
        "distinct_sources": first_source["source_ref"] != second_source["source_ref"],
        "first_event_keeps_first_source": first_read.get("s47_source_hash")
        == first_source.get("source_hash"),
        "second_event_uses_second_source": second_read.get("s47_source_hash")
        == second_source.get("source_hash"),
        "first_event_current_source_is_later": first_read.get("current_source_hash")
        == second_source.get("source_hash"),
        "cold_first_keeps_first_source": cold_first.get("s47_source_hash")
        == first_source.get("source_hash"),
        "verify_ok": bool(verify.get("ok") and cold_verify.get("ok")),
    }
    return {
        "state": str(state),
        "first_event_ref": first_ref,
        "second_event_ref": second_ref,
        "first_source": {
            "ref": first_source.get("source_ref"),
            "hash": first_source.get("source_hash"),
            "coverage": ((first_source.get("content") or {}).get("coverage")),
        },
        "second_source": {
            "ref": second_source.get("source_ref"),
            "hash": second_source.get("source_hash"),
            "coverage": ((second_source.get("content") or {}).get("coverage")),
        },
        "first_read": _c9_summary(first_read),
        "second_read": _c9_summary(second_read),
        "cold_first_read": _c9_summary(cold_first),
        "checks": checks,
        "ok": all(checks.values()),
    }


def _scenario_cut_restore(root: Path) -> dict:
    state = root / "cut-restore"
    session = _start_s47(state)
    try:
        from s46.errors import S46Refusal
        from s46.model import make_domain

        produced = session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        before = session.c9_interval_source()
        session.revoke_interval_condition(produced["state_id"], reason="TEST_ONLY_CUT")
        cut_code = ""
        try:
            _admit(session)
        except S46Refusal as exc:
            cut_code = exc.code
        session.restore_interval_condition(
            produced["state_id"], reason="TEST_ONLY_RESTORE"
        )
        restored = session.c9_interval_source()
        admitted = _admit(session)
        c9 = session.read_c9_conditioning(admitted["event"]["e1_event_id"])
        verify = session.verify()
    finally:
        session.close()
    checks = {
        "cut_refused": cut_code == "S46_INTERVAL_CONDITION_REVOKED",
        "restored_source_same": restored.get("source_hash") == before.get("source_hash"),
        "restored_admission_ok": admitted.get("status") == "OK",
        "restored_c9_uses_source": c9.get("s47_source_hash") == before.get("source_hash"),
        "restored_c9_material_false": c9.get("objective_material_eligible") is False,
        "verify_ok": bool(verify.get("ok")),
    }
    return {
        "state": str(state),
        "cut_code": cut_code,
        "before_source": {
            "ref": before.get("source_ref"),
            "hash": before.get("source_hash"),
        },
        "restored_source": {
            "ref": restored.get("source_ref"),
            "hash": restored.get("source_hash"),
        },
        "c9": _c9_summary(c9),
        "checks": checks,
        "ok": all(checks.values()),
    }


def _scenario_admission_source(root: Path) -> dict:
    state = root / "admission-source"
    session = _start_s47(state)
    try:
        from s46.model import make_domain

        session.produce_interval(
            make_domain(
                mode="SCHEDULED_ONLY", start=session.clock(), end=session.clock() + 4
            )
        )
        interval_end = session.c9_interval_source()
        helped = session.do_help()
        admission_source = session.c9_interval_source()
        admitted = _admit(session)
        read = session.read_c9_conditioning(admitted["event"]["e1_event_id"])
        verify = session.verify()
    finally:
        session.close()
    checks = {
        "help_accepted": helped.get("accepted") is True,
        "interval_end_access_granted": ((interval_end.get("content") or {}).get("access"))
        == "granted",
        "admission_access_denied": ((admission_source.get("content") or {}).get("access"))
        == "denied",
        "source_changed_after_material": interval_end.get("source_hash")
        != admission_source.get("source_hash"),
        "c9_uses_admission_source": read.get("s47_source_hash")
        == admission_source.get("source_hash"),
        "c9_not_interval_end_source": read.get("s47_source_hash")
        != interval_end.get("source_hash"),
        "c9_material_false": read.get("objective_material_eligible") is False,
        "verify_ok": bool(verify.get("ok")),
    }
    return {
        "state": str(state),
        "interval_end_source": {
            "ref": interval_end.get("source_ref"),
            "hash": interval_end.get("source_hash"),
            "access": ((interval_end.get("content") or {}).get("access")),
        },
        "admission_source": {
            "ref": admission_source.get("source_ref"),
            "hash": admission_source.get("source_hash"),
            "access": ((admission_source.get("content") or {}).get("access")),
        },
        "do_help": _do_help_summary(helped),
        "c9": _c9_summary(read),
        "checks": checks,
        "ok": all(checks.values()),
    }


def _cold_subprocess(state: Path, event_ref: str) -> dict:
    command = [
        sys.executable,
        str(SCRIPT),
        "c9",
        "--state",
        str(state),
        "--event-ref",
        event_ref,
    ]
    completed = subprocess.run(
        command,
        cwd=str(PRODUCT),
        env=dict(os.environ),
        text=True,
        capture_output=True,
        timeout=120,
    )
    payload = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {"raw_stdout": completed.stdout}
    return {
        "command": command,
        "returncode": completed.returncode,
        "payload": payload,
        "stderr": completed.stderr,
    }


def demo(args) -> int:
    root = None
    if args.root:
        root = Path(args.root).expanduser().resolve()
        root.mkdir(parents=True, exist_ok=True)
    run_root = Path(tempfile.mkdtemp(prefix="sorok-s45-s47-cli-", dir=str(root) if root else None))
    try:
        s45 = _scenario_s45(run_root)
        actual = _scenario_mode(run_root, "ACTUAL")
        scheduled = _scenario_mode(run_root, "SCHEDULED_ONLY")
        event_local = _scenario_event_local(run_root)
        cut_restore = _scenario_cut_restore(run_root)
        admission_source = _scenario_admission_source(run_root)
        subprocess_read = _cold_subprocess(
            Path(event_local["state"]), event_local["first_event_ref"]
        )
        subprocess_hash = (
            ((subprocess_read.get("payload") or {}).get("c9") or {}).get(
                "s47_source_hash"
            )
        )
        source_audit = verify_sources()
        import_audit = loaded_modules()
        checks = {
            "s45": s45["ok"],
            "actual": actual["ok"],
            "scheduled": scheduled["ok"],
            "event_local": event_local["ok"],
            "cut_restore": cut_restore["ok"],
            "admission_source": admission_source["ok"],
            "cold_subprocess_ok": subprocess_read["returncode"] == 0,
            "cold_subprocess_same_source": subprocess_hash
            == event_local["first_source"]["hash"],
            "source_manifest": source_audit["ok"],
            "import_closure": import_audit["ok"],
        }
        report = {
            "schema": SCHEMA,
            "grade": "TEST_ONLY_SOURCEFREE_S45_S47_PRODUCT_CLOSURE_NOT_NATIVE",
            "native": False,
            "provider_calls": 0,
            "product_model_calls": 0,
            "state_root": str(run_root),
            "retained": bool(args.keep),
            "closure": roots(),
            "scenarios": {
                "s45": s45,
                "actual": actual,
                "scheduled": scheduled,
                "event_local": event_local,
                "cut_restore": cut_restore,
                "admission_source": admission_source,
            },
            "cold_subprocess": subprocess_read,
            "source_audit": source_audit,
            "import_audit": {
                key: import_audit[key]
                for key in (
                    "schema", "modules", "local_modules", "stdlib_modules",
                    "external_modules", "ok",
                )
            },
            "checks": checks,
            "target_proposals": [],
            "native_grants": {
                "actor": False, "rule": False, "source": False, "human": False,
                "c8": False, "c9": False, "c12": False,
            },
            "ok": all(checks.values()),
        }
        print(_json(report))
        return 0 if report["ok"] else 1
    finally:
        if not args.keep:
            shutil.rmtree(run_root, ignore_errors=True)


def command_new(args) -> int:
    state = Path(args.state).expanduser().resolve()
    session = _start_s47(state, args.seed)
    adapter = _projection(session)
    try:
        report = {
            "schema": "SOROK_S45_S47_CLI_ACTION@1",
            "action": "new",
            "state": str(state),
            "root_hash": session.read_root()["root_hash"],
            "clock": session.clock(),
            "events": len(session.read_events()),
            "encounters": len(session.read_encounters()),
            "verify_ok": bool(session.verify().get("ok")),
            "view": adapter.view(),
        }
    finally:
        adapter.close()
    print(_json(report))
    return 0


def command_view(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    adapter = _projection(session)
    try:
        view = adapter.view()
    finally:
        adapter.close()
    if args.text:
        from wp19.interface import render_text

        print(render_text(view))
    else:
        print(_json(view))
    return 0


def command_status(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    adapter = _projection(session)
    try:
        status = adapter.status()
    finally:
        adapter.close()
    print(_json(status))
    return 0


def command_say(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    adapter = _projection(session)
    try:
        result = adapter.say(args.text)
    finally:
        adapter.close()
    print(_json(result))
    return 0


def command_do_help(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    adapter = _projection(session)
    try:
        result = adapter.do_help()
    finally:
        adapter.close()
    print(_json(result))
    return 0


def command_attend(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    adapter = _projection(session)
    try:
        result = adapter.attend()
    finally:
        adapter.close()
    print(_json(result))
    return 0


def _command_hold(adapter, name: str) -> dict:
    return {
        "wait": adapter.wait,
        "exit": adapter.exit,
        "return": adapter.return_,
        "absence": adapter.absence,
    }[name]()


def _run_hold(state: str, name: str) -> int:
    session = _open_s47(Path(state).expanduser().resolve())
    adapter = _projection(session)
    try:
        result = _command_hold(adapter, name)
    finally:
        adapter.close()
    print(_json(result))
    return 0


def command_wait(args) -> int:
    return _run_hold(args.state, "wait")


def command_exit(args) -> int:
    return _run_hold(args.state, "exit")


def command_return(args) -> int:
    return _run_hold(args.state, "return")


def command_absence(args) -> int:
    return _run_hold(args.state, "absence")


def command_interval(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    try:
        from s46.model import make_domain

        start = session.clock() if args.start is None else args.start
        produced = session.produce_interval(
            make_domain(mode=args.mode, start=start, end=start + args.span)
        )
        report = {
            "schema": "SOROK_S45_S47_CLI_ACTION@1",
            "action": "interval",
            "state": str(Path(args.state).expanduser().resolve()),
            "material_after_interval": session.world().actor_state["A"]["material_remaining"],
            "interval": _interval_summary(produced),
            "source": {
                "source_ref": (session.c9_interval_source() or {}).get("source_ref"),
                "source_hash": (session.c9_interval_source() or {}).get("source_hash"),
            },
        }
    finally:
        session.close()
    print(_json(report))
    return 0


def command_admit(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    try:
        admitted = _admit(session, args.event_ref)
        report = {
            "schema": "SOROK_S45_S47_CLI_ACTION@1",
            "action": "admit",
            "state": str(Path(args.state).expanduser().resolve()),
            "status": admitted.get("status"),
            "event_ref": admitted["event"].get("e1_event_id"),
            "event_hash": admitted["event"].get("e1_event_hash"),
            "selected_option": admitted["event"].get("selected_option"),
            "attempt_status": admitted["event"].get("attempt_status"),
        }
    finally:
        session.close()
    print(_json(report))
    return 0


def command_c9(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    try:
        read = session.read_c9_conditioning(args.event_ref)
        report = {
            "schema": "SOROK_S45_S47_CLI_ACTION@1",
            "action": "c9",
            "state": str(Path(args.state).expanduser().resolve()),
            "c9": _c9_summary(read),
            "verify_ok": bool(session.verify().get("ok")),
        }
    finally:
        session.close()
    print(_json(report))
    return 0


def command_verify(args) -> int:
    session = _open_s47(Path(args.state).expanduser().resolve())
    try:
        report = {
            "schema": "SOROK_S45_S47_CLI_ACTION@1",
            "action": "verify",
            "state": str(Path(args.state).expanduser().resolve()),
            "verify": session.verify(),
            "events": len(session.read_events()),
            "encounters": _encounter_summary(session),
            "root_hash": session.read_root()["root_hash"],
        }
    finally:
        session.close()
    print(_json(report))
    return 0


def command_manifest(args) -> int:
    report = {
        "schema": "SOROK_S45_S47_CLI_ACTION@1",
        "action": "manifest",
        "closure": roots(),
        "source_audit": verify_sources(),
        "import_audit": loaded_modules(),
    }
    print(_json(report))
    return 0 if report["source_audit"]["ok"] and report["import_audit"]["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sorok-s45-s47",
        description="Pinned TEST_ONLY S45-S47 sourcefree product spine.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="create a fresh pinned person state")
    new.add_argument("--state", required=True)
    new.add_argument("--seed", default="01" * 32)
    new.set_defaults(func=command_new)

    view = sub.add_parser("view", help="projected WP19 encounter view")
    view.add_argument("--state", required=True)
    view.add_argument("--text", action="store_true")
    view.set_defaults(func=command_view)

    status_parser = sub.add_parser("status", help="projected adapter status")
    status_parser.add_argument("--state", required=True)
    status_parser.set_defaults(func=command_status)

    say = sub.add_parser("say", help="projected user SAY attempt")
    say.add_argument("--state", required=True)
    say.add_argument("text")
    say.set_defaults(func=command_say)

    do_help = sub.add_parser("do-help", help="user DO_HELP through the S45 encounter")
    do_help.add_argument("--state", required=True)
    do_help.set_defaults(func=command_do_help)

    attend = sub.add_parser("attend", help="projected user ATTEND action")
    attend.add_argument("--state", required=True)
    attend.set_defaults(func=command_attend)

    wait = sub.add_parser("wait", help="typed WAIT hold without time advance")
    wait.add_argument("--state", required=True)
    wait.set_defaults(func=command_wait)

    exit_parser = sub.add_parser("exit", help="local exit without actor/world event")
    exit_parser.add_argument("--state", required=True)
    exit_parser.set_defaults(func=command_exit)

    return_parser = sub.add_parser("return", help="typed RETURN hold")
    return_parser.add_argument("--state", required=True)
    return_parser.set_defaults(func=command_return)

    absence = sub.add_parser("absence", help="typed ABSENCE hold")
    absence.add_argument("--state", required=True)
    absence.set_defaults(func=command_absence)

    interval = sub.add_parser("interval", help="produce a real S46 interval")
    interval.add_argument("--state", required=True)
    interval.add_argument("--mode", default="ACTUAL", choices=[
        "ACTUAL", "SCHEDULED_ONLY", "DECLINED", "CONSTRAINED", "BLOCKED", "UNKNOWN",
    ])
    interval.add_argument("--start", type=int, default=None)
    interval.add_argument("--span", type=int, default=4)
    interval.set_defaults(func=command_interval)

    admit = sub.add_parser("admit", help="admit a real later S42 event")
    admit.add_argument("--state", required=True)
    admit.add_argument("--event-ref", default=None)
    admit.set_defaults(func=command_admit)

    c9 = sub.add_parser("c9", help="read event-local C9 conditioning")
    c9.add_argument("--state", required=True)
    c9.add_argument("--event-ref", default=None)
    c9.set_defaults(func=command_c9)

    verify = sub.add_parser("verify", help="verify and read encounters")
    verify.add_argument("--state", required=True)
    verify.set_defaults(func=command_verify)

    manifest = sub.add_parser("manifest", help="verify pinned sources and import paths")
    manifest.set_defaults(func=command_manifest)

    demo_parser = sub.add_parser(
        "demo", help="fresh end-to-end S45/S46/S47 causal and cold proof"
    )
    demo_parser.add_argument("--root", default=None)
    demo_parser.add_argument("--keep", action="store_true")
    demo_parser.set_defaults(func=demo)
    return parser


def main(argv=None) -> int:
    install()
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
