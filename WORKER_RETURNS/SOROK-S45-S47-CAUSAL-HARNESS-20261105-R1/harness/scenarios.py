"""Causal scenarios over the exact staged S45-S47 source closure."""
from __future__ import annotations

import shutil
from copy import deepcopy
from pathlib import Path

SEED = "01" * 32
WRONG_SEED = "02" * 32


def _start(state: Path, seed: str = SEED):
    from s37.harness import case_for, source_for
    from s45.fixtures import root_bundle
    from s47.session import S47Session

    case = case_for(True)
    return S47Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _admit(session):
    from s37.harness import case_for, source_for

    events = session.read_events()
    if not events:
        raise RuntimeError("S47_BASE_EVENT_MISSING")
    first = events[0]
    return session.admit_event(
        case=case_for(True),
        source=source_for(case_for(True)),
        history_event_refs=(first["e1_event_id"],),
        event_time=session.clock() + 1,
    )


def _source_summary(source):
    if not source:
        return None
    content = source.get("content") or {}
    return {
        "source_ref": source.get("source_ref"),
        "source_class": source.get("source_class"),
        "source_hash": source.get("source_hash"),
        "schema": content.get("schema"),
        "actor_id": content.get("actor_id"),
        "branch_id": content.get("branch_id"),
        "scene": content.get("scene"),
        "access": content.get("access"),
        "status": content.get("status"),
        "coverage": content.get("coverage"),
        "currentness": content.get("currentness"),
        "as_of": content.get("as_of"),
        "mode": content.get("mode"),
        "interval_state_id": content.get("interval_state_id"),
        "interval_receipt_hash": content.get("interval_receipt_hash"),
        "domain_issuance_id": content.get("domain_issuance_id"),
        "material_after_interval": content.get("material_after_interval"),
        "private_b_motive_included": content.get("private_b_motive_included"),
        "actor_knowledge_inferred": content.get("actor_knowledge_inferred"),
        "native_authority_claimed": content.get("native_authority_claimed"),
    }


def _encounter_summary(session):
    rows = []
    for row in session.read_encounters():
        rows.append({
            "kind": row.get("kind"),
            "status": row.get("status"),
            "strategy": row.get("strategy"),
            "action_event_id": row.get("action_event_id"),
            "speech_event_id": row.get("speech_event_id"),
            "root_hash": row.get("root_hash"),
            "current_access": row.get("current_access"),
        })
    return rows


def _c9_summary(read):
    return {
        "event_ref": read["event_ref"],
        "selected_event_ref": read["selected_event_ref"],
        "response_status": read["response_status"],
        "s47_source_ref": read["s47_source_ref"],
        "s47_source_hash": read["s47_source_hash"],
        "s47_source_in_readset": read["s47_source_in_readset"],
        "s47_source_currentness": read["s47_source_currentness"],
        "s47_source_coverage": read["s47_source_coverage"],
        "objective_material_eligible": read["objective_material_eligible"],
        "objective_material_refs": read["objective_material_refs"],
        "target_branch": read["target_branch"],
        "target_reason": read["target_reason"],
        "target_proposals": read["target_proposals"],
        "readset_refs": read["readset_refs"],
        "present_condition_revoked": read["present_condition_revoked"],
        "historical_condition_revoked": read["historical_condition_revoked"],
    }


def _run_mode(work_dir: Path, mode: str) -> dict:
    from s46.model import make_domain
    from s47.session import S47Session

    state = work_dir / "modes" / mode.lower()
    if state.exists():
        shutil.rmtree(state)
    state.parent.mkdir(parents=True, exist_ok=True)
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        before_b = dict(session.world().actor_state["B"])
        before_material = session.world().actor_state["A"]["material_remaining"]
        produced = session.produce_interval(
            make_domain(
                mode=mode,
                start=session.clock(),
                end=session.clock() + 4,
            )
        )
        material_after_interval = session.world().actor_state["A"][
            "material_remaining"
        ]
        source = _source_summary(session.c9_interval_source())
        result = _admit(session)
        c9 = session.read_c9_conditioning()
        said = session.say("Can I help?")
        helped = session.do_help()
        attended = session.attend()
        encounters = _encounter_summary(session)
        after_b = dict(session.world().actor_state["B"])
        after_material = session.world().actor_state["A"][
            "material_remaining"
        ]
        verify = session.verify()
        event_ref = c9["event_ref"]
    finally:
        session.close()

    cold = S47Session.open(state)
    try:
        cold_root = cold.read_root()["root_hash"]
        cold_event = cold.read_c9_conditioning(event_ref)
        cold_latest = cold.read_c9_conditioning()
        cold_source = _source_summary(cold.c9_interval_source())
        cold_encounters = _encounter_summary(cold)
        cold_verify = cold.verify()
        cold_material = cold.world().actor_state["A"]["material_remaining"]
        cold_b = dict(cold.world().actor_state["B"])
    finally:
        cold.close()

    return {
        "schema": "SOROK_S45_S47_HARNESS_MODE@1",
        "mode": mode,
        "root_hash": root_hash,
        "root_hash_after": cold_root,
        "root_unchanged": cold_root == root_hash,
        "material_before": before_material,
        "material_after_interval": material_after_interval,
        "material_after": after_material,
        "material_after_cold": cold_material,
        "interval": {
            "state_id": produced["state_id"],
            "status": produced["status"],
            "coverage": produced["coverage"],
            "segment_statuses": [
                row["status"] for row in produced["segments"]
            ],
            "domains": produced.get("domain"),
        },
        "conditioning_source": source,
        "s42_admission": {
            "status": result.get("status"),
            "selected_option": result["event"].get("selected_option"),
            "attempt_status": result["event"].get("attempt_status"),
        },
        "c9": _c9_summary(c9),
        "s45": {
            "say_status": said.get("status"),
            "do_help_status": helped.get("status"),
            "do_help_accepted": helped.get("accepted"),
            "do_help_strategy": helped.get("strategy"),
            "attend_status": attended.get("status"),
            "encounters": encounters,
        },
        "other_actor_preserved": before_b == after_b == cold_b,
        "cold": {
            "root_hash": cold_root,
            "event_c9": _c9_summary(cold_event),
            "latest_c9": _c9_summary(cold_latest),
            "current_source": cold_source,
            "encounters": cold_encounters,
            "verify_ok": cold_verify.get("ok"),
        },
        "verify_ok": bool(verify.get("ok")),
        "target_proposals": [],
        "native_grants": {
            "actor": False,
            "rule": False,
            "source": False,
            "human": False,
            "c8": False,
            "c9": False,
            "c12": False,
        },
    }


def _sever_restore(work_dir: Path) -> dict:
    from s46.errors import S46Refusal
    from s46.model import make_domain
    from s47.session import S47Session

    state = work_dir / "sever-restore"
    if state.exists():
        shutil.rmtree(state)
    session = _start(state)
    try:
        produced = session.produce_interval(
            make_domain(
                mode="ACTUAL",
                start=session.clock(),
                end=session.clock() + 4,
            )
        )
        before_source = _source_summary(session.c9_interval_source())
        first = _admit(session)
        first_e1 = first["event"]["e1_event_id"]
        first_c9 = _c9_summary(session.read_c9_conditioning(first_e1))
        session.revoke_interval_condition(
            produced["state_id"], reason="TEST_ONLY_DEPENDENCY_CUT"
        )
        try:
            _admit(session)
            cut = {"accepted": True}
        except S46Refusal as exc:
            cut = {"accepted": False, "code": exc.code}
        historical_after_cut = _c9_summary(
            session.read_c9_conditioning(first_e1)
        )
        session.restore_interval_condition(
            produced["state_id"], reason="TEST_ONLY_DEPENDENCY_RESTORE"
        )
        restored_source = _source_summary(session.c9_interval_source())
        second = _admit(session)
        second_e1 = second["event"]["e1_event_id"]
        second_c9 = _c9_summary(session.read_c9_conditioning(second_e1))
        event_refs = {
            "first": first_e1,
            "second": second_e1,
        }
    finally:
        session.close()

    cold = S47Session.open(state)
    try:
        cold_first = _c9_summary(cold.read_c9_conditioning(event_refs["first"]))
        cold_second = _c9_summary(cold.read_c9_conditioning(event_refs["second"]))
        cold_verify = cold.verify()
    finally:
        cold.close()

    return {
        "schema": "SOROK_S45_S47_HARNESS_SEVER_RESTORE@1",
        "cut": cut,
        "restored_source": restored_source,
        "restored_source_same": before_source == restored_source,
        "first_c9": first_c9,
        "historical_after_cut": historical_after_cut,
        "second_c9": second_c9,
        "cold_first_c9": cold_first,
        "cold_second_c9": cold_second,
        "cold_verify_ok": cold_verify.get("ok"),
        "event_refs": event_refs,
    }


def _wrong_root(work_dir: Path) -> dict:
    from candidate.conditioning import make_conditioning_source
    from s46.model import make_domain
    from s47.conditioning import qualify_source
    from s47.errors import S47Refusal

    base = work_dir / "wrong-root"
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True, exist_ok=True)
    a = _start(base / "a", SEED)
    b = _start(base / "b", WRONG_SEED)
    try:
        a_root = a.read_root()["root_hash"]
        b_root = b.read_root()["root_hash"]
        a.produce_interval(
            make_domain(mode="ACTUAL", start=a.clock(), end=a.clock() + 4)
        )
        b.produce_interval(
            make_domain(mode="ACTUAL", start=b.clock(), end=b.clock() + 4)
        )
        a_source = a.c9_interval_source()
        b_source = b.c9_interval_source()
        a_summary = _source_summary(a_source)
        b_summary = _source_summary(b_source)

        unresealed = {"accepted": True}
        try:
            qualify_source(b, a_source)
        except S47Refusal as exc:
            unresealed = {"accepted": False, "code": exc.code}

        forged = deepcopy(a_source)
        forged["content"]["as_of"] = b_source["content"]["as_of"]
        rebuilt = make_conditioning_source(
            source_ref=forged["source_ref"],
            source_class=forged["source_class"],
            subject=forged["subject"],
            body=forged["content"],
        )
        forged["source_hash"] = rebuilt["source_hash"]
        resealed = {"accepted": True}
        try:
            qualify_source(b, forged)
        except S47Refusal as exc:
            resealed = {"accepted": False, "code": exc.code}

        own = {"accepted": True}
        try:
            qualified = qualify_source(b, b_source)
            own = {
                "accepted": True,
                "source_hash": qualified["source_hash"],
                "same_as_own": qualified["source_hash"]
                == b_source["source_hash"],
            }
        except S47Refusal as exc:
            own = {"accepted": False, "code": exc.code}

        b_result = _admit(b)
        b_c9 = _c9_summary(b.read_c9_conditioning())
        b_source_after = _source_summary(b.c9_interval_source())
    finally:
        a.close()
        b.close()

    return {
        "schema": "SOROK_S45_S47_HARNESS_WRONG_ROOT@1",
        "a_root": a_root,
        "b_root": b_root,
        "roots_differ": a_root != b_root,
        "a_source": a_summary,
        "b_source": b_summary,
        "unresealed_foreign": unresealed,
        "resealed_foreign": resealed,
        "own_source": own,
        "b_admission_status": b_result.get("status"),
        "b_c9": b_c9,
        "b_source_after": b_source_after,
        "b_used_own_source": (
            b_c9["s47_source_hash"] == b_summary["source_hash"]
            and b_c9["s47_source_hash"] != a_summary["source_hash"]
        ),
    }


def run_scenarios(work_dir: Path) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    actual = _run_mode(work_dir, "ACTUAL")
    scheduled = _run_mode(work_dir, "SCHEDULED_ONLY")
    sever = _sever_restore(work_dir)
    wrong = _wrong_root(work_dir)

    checks = {
        "same_root_actual_scheduled": (
            actual["root_hash"] == scheduled["root_hash"]
        ),
        "actual_performed_material_consumed": (
            actual["material_after_interval"] == 0
            and actual["c9"]["objective_material_eligible"] is False
        ),
        "scheduled_material_retained": (
            scheduled["material_after_interval"] == 1
            and scheduled["c9"]["objective_material_eligible"] is True
        ),
        "actual_s47_source_in_c9_readset": (
            actual["c9"]["s47_source_in_readset"] is True
            and actual["c9"]["s47_source_hash"]
            == actual["conditioning_source"]["source_hash"]
        ),
        "scheduled_s47_source_in_c9_readset": (
            scheduled["c9"]["s47_source_in_readset"] is True
            and scheduled["c9"]["s47_source_hash"]
            == scheduled["conditioning_source"]["source_hash"]
        ),
        "actual_do_help_refused": (
            actual["s45"]["do_help_status"] == "OK"
            and actual["s45"]["do_help_accepted"] is False
            and actual["s45"]["do_help_strategy"] == "HELP_REFUSE"
        ),
        "scheduled_do_help_accepted": (
            scheduled["s45"]["do_help_status"] == "OK"
            and scheduled["s45"]["do_help_accepted"] is True
            and scheduled["s45"]["do_help_strategy"] == "HELP_ACCEPT"
        ),
        "both_targetless_no_change": (
            actual["c9"]["target_branch"] == "NO_CHANGE"
            and scheduled["c9"]["target_branch"] == "NO_CHANGE"
            and actual["c9"]["target_reason"] == "NO_PROPOSAL"
            and scheduled["c9"]["target_reason"] == "NO_PROPOSAL"
        ),
        "other_actor_preserved": (
            actual["other_actor_preserved"]
            and scheduled["other_actor_preserved"]
        ),
        "cold_replay_actual": (
            actual["root_unchanged"]
            and actual["cold"]["event_c9"]["s47_source_hash"]
            == actual["c9"]["s47_source_hash"]
            and actual["cold"]["event_c9"]["objective_material_eligible"]
            == actual["c9"]["objective_material_eligible"]
            and actual["cold"]["encounters"] == actual["s45"]["encounters"]
            and actual["cold"]["verify_ok"] is True
        ),
        "cold_replay_scheduled": (
            scheduled["root_unchanged"]
            and scheduled["cold"]["event_c9"]["s47_source_hash"]
            == scheduled["c9"]["s47_source_hash"]
            and scheduled["cold"]["event_c9"]["objective_material_eligible"]
            == scheduled["c9"]["objective_material_eligible"]
            and scheduled["cold"]["encounters"] == scheduled["s45"]["encounters"]
            and scheduled["cold"]["verify_ok"] is True
        ),
        "sever_dependency_red": (
            sever["cut"].get("accepted") is False
            and sever["cut"].get("code") == "S46_INTERVAL_CONDITION_REVOKED"
        ),
        "restore_dependency_pass": (
            sever["restored_source_same"] is True
            and sever["second_c9"]["s47_source_hash"]
            == sever["first_c9"]["s47_source_hash"]
            and sever["second_c9"]["s47_source_in_readset"] is True
            and sever["second_c9"]["objective_material_eligible"] is False
            and sever["second_c9"]["target_branch"] == "NO_CHANGE"
        ),
        "sever_preserves_historical_c9_source": (
            sever["historical_after_cut"]["s47_source_hash"]
            == sever["first_c9"]["s47_source_hash"]
            and sever["historical_after_cut"]["s47_source_in_readset"] is True
            and sever["historical_after_cut"]["present_condition_revoked"] is True
        ),
        "sever_restore_cold_replay": (
            sever["cold_first_c9"]["s47_source_hash"]
            == sever["first_c9"]["s47_source_hash"]
            and sever["cold_second_c9"]["s47_source_hash"]
            == sever["second_c9"]["s47_source_hash"]
            and sever["cold_verify_ok"] is True
        ),
        "wrong_root_roots_differ": wrong["roots_differ"] is True,
        "wrong_root_unresealed_refused": (
            wrong["unresealed_foreign"].get("accepted") is False
        ),
        "wrong_root_resealed_refused": (
            wrong["resealed_foreign"].get("accepted") is False
        ),
        "wrong_root_own_source_still_accepted": (
            wrong["own_source"].get("accepted") is True
            and wrong["own_source"].get("same_as_own") is True
        ),
        "wrong_root_c9_uses_own_source": (
            wrong["b_admission_status"] == "OK"
            and wrong["b_used_own_source"] is True
        ),
    }
    return {
        "schema": "SOROK_S45_S47_CAUSAL_HARNESS_SCENARIOS@1",
        "actual": actual,
        "scheduled": scheduled,
        "sever_restore": sever,
        "wrong_root": wrong,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


__all__ = ["run_scenarios"]
