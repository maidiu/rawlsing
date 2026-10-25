"""Runnable S47 interval-to-C9 conditioning on the accepted S46 person."""
from __future__ import annotations

import json
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s47.bootstrap import install  # noqa: E402

install()

from s37.harness import case_for, source_for  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s46.errors import S46Refusal  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s47.conditioning import qualify_source  # noqa: E402
from s47.errors import S47Refusal  # noqa: E402
from s47.session import S47Session  # noqa: E402


def _start(state):
    case = case_for(True)
    return S47Session.start(
        state, bundle=root_bundle("01" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )


def _admit(session):
    first = session.read_events()[0]
    return session.admit_event(
        case=case_for(True), source=source_for(case_for(True)),
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
        "interval_state_id": content.get("interval_state_id"),
        "interval_receipt_hash": content.get("interval_receipt_hash"),
        "domain_issuance_id": content.get("domain_issuance_id"),
        "material_after_interval": content.get("material_after_interval"),
        "private_b_motive_included": content.get("private_b_motive_included"),
        "actor_knowledge_inferred": content.get("actor_knowledge_inferred"),
        "native_authority_claimed": content.get("native_authority_claimed"),
    }


def _scene_report(session):
    return [
        {"kind": row.get("kind"), "status": row.get("status")}
        for row in session.read_encounters()
    ]


def _run_mode(root, mode):
    state = root / mode.lower()
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        before_b = dict(session.world().actor_state["B"])
        before_material = session.world().actor_state["A"]["material_remaining"]
        domain = make_domain(mode=mode, start=session.clock(), end=session.clock() + 4)
        produced = session.produce_interval(domain)
        material_after_interval = session.world().actor_state["A"]["material_remaining"]
        source = _source_summary(session.c9_interval_source())
        result = _admit(session)
        c9 = session.read_c9_conditioning()
        said = session.say("Can I help?")
        helped = session.do_help()
        attended = session.attend()
        scenes = _scene_report(session)
        after_b = dict(session.world().actor_state["B"])
        verify = session.verify()
        after_material = session.world().actor_state["A"]["material_remaining"]
    finally:
        session.close()
    cold = S47Session.open(state)
    try:
        cold_c9 = cold.read_c9_conditioning()
        cold_source = _source_summary(cold.c9_interval_source())
        cold_verify = cold.verify()
        cold_root = cold.read_root()["root_hash"]
    finally:
        cold.close()
    return {
        "schema": "SOROK_S47_INTERVAL_C9_MODE@1",
        "mode": mode,
        "root_hash": root_hash,
        "root_hash_after": cold_root,
        "root_unchanged": cold_root == root_hash,
        "material_before": before_material,
        "material_after_interval": material_after_interval,
        "material_after": after_material,
        "interval": {
            "state_id": produced["state_id"],
            "status": produced["status"],
            "coverage": produced["coverage"],
            "segment_statuses": [row["status"] for row in produced["segments"]],
        },
        "conditioning_source": source,
        "s42_admission": {
            "status": result.get("status"),
            "selected_option": result["event"].get("selected_option"),
            "attempt_status": result["event"].get("attempt_status"),
        },
        "c9": {
            "event_ref": c9["event_ref"],
            "response_status": c9["response_status"],
            "s47_source_ref": c9["s47_source_ref"],
            "s47_source_hash": c9["s47_source_hash"],
            "s47_source_in_readset": c9["s47_source_in_readset"],
            "s47_source_currentness": c9["s47_source_currentness"],
            "s47_source_coverage": c9["s47_source_coverage"],
            "objective_material_eligible": c9["objective_material_eligible"],
            "objective_material_refs": c9["objective_material_refs"],
            "target_branch": c9["target_branch"],
            "target_reason": c9["target_reason"],
            "target_proposals": c9["target_proposals"],
            "readset_refs": c9["readset_refs"],
        },
        "s45": {
            "say_status": said.get("status"),
            "do_help_status": helped.get("status"),
            "do_help_accepted": helped.get("accepted"),
            "do_help_strategy": helped.get("strategy"),
            "attend_status": attended.get("status"),
            "scenes": scenes,
        },
        "other_actor_preserved": before_b == after_b,
        "cold_c9": {
            "s47_source_ref": cold_c9["s47_source_ref"],
            "s47_source_in_readset": cold_c9["s47_source_in_readset"],
            "objective_material_eligible": cold_c9["objective_material_eligible"],
            "target_branch": cold_c9["target_branch"],
            "source": cold_source,
        },
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "target_proposals": [],
        "native_grants": {
            "actor": False, "rule": False, "source": False, "human": False,
            "c8": False, "c9": False, "c12": False,
        },
    }


def condition_evidence(root):
    state = root / "condition"
    session = _start(state)
    try:
        produced = session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        before = _source_summary(session.c9_interval_source())
        session.revoke_interval_condition(produced["state_id"], reason="TEST_ONLY_CUT")
        try:
            _admit(session)
            cut = {"accepted": True}
        except S46Refusal as exc:
            cut = {"accepted": False, "code": exc.code}
        session.restore_interval_condition(produced["state_id"], reason="TEST_ONLY_RESTORE")
        restored = _source_summary(session.c9_interval_source())
        admitted = _admit(session)
        c9 = session.read_c9_conditioning()
        source_same = before == restored
    finally:
        session.close()
    return {
        "schema": "SOROK_S47_CONDITION_EVIDENCE@1",
        "cut": cut,
        "restored_source_same": source_same,
        "restored_source": restored,
        "admission_status": admitted.get("status"),
        "c9_source_ref": c9["s47_source_ref"],
        "c9_source_in_readset": c9["s47_source_in_readset"],
        "c9_objective_material_eligible": c9["objective_material_eligible"],
        "c9_target_branch": c9["target_branch"],
    }


def no_interval_evidence(root):
    state = root / "no-interval"
    session = _start(state)
    try:
        assert session.c9_interval_source() is None
        admitted = _admit(session)
        c9 = session.read_c9_conditioning()
        verify = session.verify()
    finally:
        session.close()
    return {
        "schema": "SOROK_S47_NO_INTERVAL_EVIDENCE@1",
        "admission_status": admitted.get("status"),
        "s47_source": c9["s47_source_ref"],
        "s47_source_in_readset": c9["s47_source_in_readset"],
        "objective_material_eligible": c9["objective_material_eligible"],
        "target_branch": c9["target_branch"],
        "target_reason": c9["target_reason"],
        "verify_ok": verify["ok"],
    }


def source_faults(root):
    state = root / "source-faults"
    session = _start(state)
    try:
        session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        real = session.c9_interval_source()
        cases = {}
        for label, field, value in [
            ("actor", "actor_id", "WRONG_ACTOR"),
            ("branch", "branch_id", "WRONG_BRANCH"),
            ("coverage", "coverage", [[1, 2]]),
            ("currentness", "currentness", "SUPERSEDED"),
            ("access", "access", "granted"),
            ("as_of", "as_of", 0),
            ("material_after_interval", "material_after_interval", True),
            ("source_ref", "source_ref", "WRONG_SOURCE_REF"),
            ("source_hash", "source_hash", "0" * 64),
        ]:
            forged = deepcopy(real)
            if field in {"source_ref", "source_hash"}:
                forged[field] = value
            else:
                forged["content"][field] = value
            try:
                qualify_source(session, forged)
                cases[label] = "ACCEPTED"
            except S47Refusal as exc:
                cases[label] = exc.code
        assert qualify_source(session, real)["source_hash"] == real["source_hash"]
        original_still_current = (
            session.c9_interval_source()["source_hash"] == real["source_hash"]
        )
    finally:
        session.close()
    return {
        "schema": "SOROK_S47_SOURCE_FAULT_EVIDENCE@1",
        "refusals": cases,
        "original_still_current": original_still_current,
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s47-"))
    report = {
        "schema": "SOROK_S47_INTERVAL_C9_RUN@1",
        "grade": "TEST_ONLY_S47_INTERVAL_MATERIAL_C9_CONDITIONING_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "actual": _run_mode(root, "ACTUAL"),
        "scheduled": _run_mode(root, "SCHEDULED_ONLY"),
        "condition": condition_evidence(root),
        "no_interval": no_interval_evidence(root),
        "source_faults": source_faults(root),
    }
    report["checks"] = {
        "actual_material_consumed": (
            report["actual"]["material_after_interval"] == 0
            and report["actual"]["c9"]["objective_material_eligible"] is False
        ),
        "scheduled_material_retained": (
            report["scheduled"]["material_after_interval"] == 1
            and report["scheduled"]["c9"]["objective_material_eligible"] is True
        ),
        "source_in_c9_readset": (
            report["actual"]["c9"]["s47_source_in_readset"]
            and report["scheduled"]["c9"]["s47_source_in_readset"]
        ),
        "targetless": (
            report["actual"]["c9"]["target_branch"] == "NO_CHANGE"
            and report["scheduled"]["c9"]["target_branch"] == "NO_CHANGE"
        ),
        "condition_restores": report["condition"]["restored_source_same"],
        "faults_refused": all(
            value != "ACCEPTED" for value in report["source_faults"]["refusals"].values()
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all(report["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
