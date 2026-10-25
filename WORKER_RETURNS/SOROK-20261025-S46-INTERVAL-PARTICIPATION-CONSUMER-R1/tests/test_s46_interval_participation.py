"""Focused S46 actual interval participation over the S45/S44 person."""
from __future__ import annotations

from copy import deepcopy

import pytest

from s46.bootstrap import install

install()

from s45.fixtures import root_bundle  # noqa: E402
from s46.errors import S46Refusal  # noqa: E402
from s46.model import make_domain, validate_domain  # noqa: E402
from s46.session import S46Session  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s42.bindings import binding_episodes  # noqa: E402


def _start(state, seed="01" * 32):
    case = case_for(True)
    return S46Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _scenes(session):
    return [
        row.get("kind")
        for row in session.read_encounters()
    ]


def _state(session):
    return session.read_interval_states()[-1]


def test_actual_interval_participation_changes_same_person_response_and_cold(tmp_path):
    state = tmp_path / "actual"
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        before = session.world_prerequisites()
        before_b = dict(session.world().actor_state["B"])
        domain = make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        produced = session.produce_interval(domain)
        after = session.world_prerequisites()
        assert produced["status"] == "PARTIAL"
        assert produced["coverage"] == [[domain["start"], domain["start"] + 1]]
        assert produced["coverage"] != [[domain["start"], domain["segments"][0][1]]]
        assert [row["status"] for row in produced["segments"]] == [
            "REALIZED", "NOT_PERFORMED",
        ]
        assert produced["segments"][0]["world"]["actual_action_event_id"]
        assert produced["segments"][1]["world"]["actual_action_event_id"] == ""
        assert produced["actual_daily_events_invented"] == 0
        assert before["material_available"] is True
        assert after["material_available"] is False
        assert session.world().actor_state["A"]["material_remaining"] == 0
        assert session.world().actor_state["B"] == before_b
        assert session.read_root()["root_hash"] == root_hash
        assert session.read_interval_states()[-1]["receipt_hash"]
        interval_hash = produced["receipt_hash"]
        session.close()
        session = S46Session.open(state)
        assert session.read_interval_states()[-1]["receipt_hash"] == interval_hash
        said = session.say("Can I help?")
        helped = session.do_help()
        attended = session.attend()
        assert said["status"] == "OK"
        assert helped["status"] == "OK"
        assert helped["accepted"] is False
        assert helped["strategy"] == "HELP_REFUSE"
        assert attended["status"] == "NO_CHANGE"
        assert _scenes(session) == ["SAY", "DO_HELP", "ATTEND"]
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = S46Session.open(state)
    try:
        cold_state = cold.read_interval_states()[-1]
        assert cold_state["receipt_hash"] == interval_hash
        assert cold_state["status"] == "PARTIAL"
        assert cold.read_root()["root_hash"] == root_hash
        assert len(cold.read_encounters()) == 3
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_same_four_scenes_under_scheduled_only_ecology(tmp_path):
    state = tmp_path / "scheduled"
    session = _start(state)
    try:
        root_hash = session.read_root()["root_hash"]
        domain = make_domain(
            mode="SCHEDULED_ONLY", start=session.clock(), end=session.clock() + 4
        )
        produced = session.produce_interval(domain)
        assert produced["status"] == "NOT_PERFORMED"
        assert produced["coverage"] == []
        assert all(row["status"] == "NOT_PERFORMED" for row in produced["segments"])
        assert session.world().actor_state["A"]["material_remaining"] == 1
        session.say("Can I help?")
        helped = session.do_help()
        session.attend()
        assert helped["accepted"] is True
        assert helped["strategy"] == "HELP_ACCEPT"
        assert _scenes(session) == ["SAY", "DO_HELP", "ATTEND"]
        assert session.read_root()["root_hash"] == root_hash
        assert session.verify()["ok"] is True
    finally:
        session.close()


@pytest.mark.parametrize("mode,expected", [
    ("ACTUAL", False), ("SCHEDULED_ONLY", True),
])
def test_interval_conditioning_reaches_real_s42_world_readset(tmp_path, mode, expected):
    state = tmp_path / mode.lower()
    session = _start(state)
    try:
        domain = make_domain(mode=mode, start=session.clock(), end=session.clock() + 4)
        session.produce_interval(domain)
        first = session.read_events()[0]
        result = session.admit_event(
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
            event_time=session.clock() + 1,
        )
        assert result["status"] == "OK"
        binding = binding_episodes(session)[-1]
        world = binding["generation"]["world_prerequisites"]
        assert world["material_available"] is expected
        assert world["s46_interval"]["state_id"]
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_interval_owner_model_and_segment_forgery_rejected_then_original_restored(tmp_path):
    state = tmp_path / "forgery"
    session = _start(state)
    try:
        domain = make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        real = session.produce_interval(domain)
        forged_model = deepcopy(real)
        forged_model["model_hash"] = "0" * 64
        forged_model["receipt_hash"] = __import__("candidate").digest(
            {k: v for k, v in forged_model.items() if k != "receipt_hash"}
        )
        with pytest.raises(S46Refusal) as exc:
            session.validate_interval_state(forged_model)
        assert exc.value.code == "S46_STATE_MODEL_MISMATCH"
        forged_segment = deepcopy(real)
        forged_segment["segments"][0]["world"]["source_owner"] = "FORGED_OWNER"
        forged_segment["state_id"] = "S46_STATE_" + __import__("candidate").digest({
            "domain": forged_segment["domain_hash"],
            "segments": forged_segment["segments"],
            "root": forged_segment["root_hash"],
        })[:24].upper()
        forged_segment["receipt_hash"] = __import__("candidate").digest({
            k: v for k, v in forged_segment.items()
            if k not in {"receipt_hash", "episode_id", "clock"}
        })
        with pytest.raises(S46Refusal) as exc:
            session.validate_interval_state(forged_segment)
        assert exc.value.code == "S46_WORLD_OWNER_MISMATCH"
        assert session.validate_interval_state(real)["receipt_hash"] == real["receipt_hash"]
        assert session.read_interval_states()[-1]["receipt_hash"] == real["receipt_hash"]
    finally:
        session.close()
    cold = S46Session.open(state)
    try:
        assert cold.read_interval_states()[-1]["status"] == "PARTIAL"
        assert cold.verify()["ok"] is True
    finally:
        cold.close()


def test_constrained_participation_has_no_consent_claim(tmp_path):
    state = tmp_path / "constrained"
    session = _start(state)
    try:
        domain = make_domain(mode="CONSTRAINED", start=session.clock(), end=session.clock() + 2)
        produced = session.produce_interval(domain)
        realized = [
            row for row in produced["segments"] if row["status"] == "REALIZED"
        ]
        assert realized
        assert realized[0]["attempt"]["attempt"] == "CONSTRAINED_ATTEMPT"
        assert realized[0]["attempt"]["consent_or_willingness_claimed"] is False
        assert produced["segments"][0]["world"]["welfare_or_consent_inferred"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_declined_interval_is_explicit_nonperformance_and_does_not_mutate_material(tmp_path):
    state = tmp_path / "declined"
    session = _start(state)
    try:
        before = session.world().actor_state["A"]["material_remaining"]
        domain = make_domain(mode="DECLINED", start=session.clock(), end=session.clock() + 2)
        produced = session.produce_interval(domain)
        assert produced["status"] == "NOT_PERFORMED"
        assert produced["segments"][0]["attempt"]["attempt"] == "DECLINED"
        assert produced["segments"][0]["world"]["actual_action_event_id"] == ""
        assert session.world().actor_state["A"]["material_remaining"] == before
        assert session.do_help()["accepted"] is True
    finally:
        session.close()


def test_supersession_changes_current_query_not_historical_interval(tmp_path):
    state = tmp_path / "supersession"
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
        assert rows[0]["state_id"] == first["state_id"]
        assert rows[0]["status"] == "PARTIAL"
        assert rows[0]["currentness"] == "SUPERSEDED"
        assert rows[0]["superseded_by"] == second["state_id"]
        assert rows[1]["currentness"] == "CURRENT"
        assert rows[1]["status"] == "NOT_PERFORMED"
        assert session.current_interval_state()["state_id"] == second["state_id"]
    finally:
        session.close()


def test_missing_or_invalid_interval_model_is_typed_refusal(tmp_path):
    state = tmp_path / "invalid-model"
    session = _start(state)
    try:
        domain = make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 2)
        bad = dict(domain)
        bad["model_hash"] = "0" * 64
        with pytest.raises(S46Refusal) as exc:
            session.produce_interval(bad)
        assert exc.value.code == "S46_MODEL_HASH_MISMATCH"
        with pytest.raises(S46Refusal):
            validate_domain({"schema": "WRONG"})
    finally:
        session.close()


def test_unknown_interval_is_not_a_negative_and_has_no_actor_effect(tmp_path):
    state = tmp_path / "unknown"
    session = _start(state)
    try:
        before = session.world().actor_state["A"]["material_remaining"]
        domain = make_domain(mode="UNKNOWN", start=session.clock(), end=session.clock() + 2)
        produced = session.produce_interval(domain)
        assert produced["status"] == "UNKNOWN"
        assert produced["segments"][0]["status"] == "UNKNOWN"
        assert produced["segments"][0]["attempt"]["attempt"] == "UNKNOWN"
        assert produced["segments"][0]["world"]["actual_action_event_id"] == ""
        assert session.world().actor_state["A"]["material_remaining"] == before
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_blocked_mode_has_no_actor_attempt_or_material_effect(tmp_path):
    state = tmp_path / "blocked"
    session = _start(state)
    try:
        before = session.world().actor_state["A"]["material_remaining"]
        domain = make_domain(
            mode="BLOCKED", start=session.clock(), end=session.clock() + 2
        )
        produced = session.produce_interval(domain)
        assert produced["status"] == "NOT_PERFORMED"
        assert produced["segments"][0]["attempt"]["attempt"] == "BLOCKED"
        assert produced["segments"][0]["world"]["status"] == "NOT_PERFORMED"
        assert produced["segments"][0]["world"]["actual_action_event_id"] == ""
        assert produced["coverage"] == []
        assert session.world().actor_state["A"]["material_remaining"] == before
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_interval_condition_revocation_refuses_then_restores_s42_path(tmp_path):
    state = tmp_path / "condition-revoke"
    session = _start(state)
    try:
        domain = make_domain(
            mode="ACTUAL", start=session.clock(), end=session.clock() + 4
        )
        produced = session.produce_interval(domain)
        state_id = produced["state_id"]
        first = session.read_events()[0]
        session.revoke_interval_condition(state_id, reason="TEST_ONLY_CUT")
        with pytest.raises(S46Refusal) as exc:
            session.admit_event(
                case=case_for(True), source=source_for(case_for(True)),
                history_event_refs=(first["e1_event_id"],),
                event_time=session.clock() + 1,
            )
        assert exc.value.code == "S46_INTERVAL_CONDITION_REVOKED"
        session.restore_interval_condition(state_id, reason="TEST_ONLY_RESTORE")
        result = session.admit_event(
            case=case_for(True), source=source_for(case_for(True)),
            history_event_refs=(first["e1_event_id"],),
            event_time=session.clock() + 1,
        )
        assert result["status"] == "OK"
        world = binding_episodes(session)[-1]["generation"]["world_prerequisites"]
        assert world["s46_interval"]["state_id"] == state_id
        assert session.verify()["ok"] is True
    finally:
        session.close()


@pytest.mark.parametrize("mode", ["domain", "span", "coverage", "status"])
def test_rehashed_domain_span_coverage_status_tamper_is_rejected(tmp_path, mode):
    from candidate import digest
    from s46.session import S46Refusal

    state = tmp_path / f"tamper-{mode}"
    session = _start(state)
    try:
        real = session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        forged = deepcopy(real)
        if mode == "domain":
            forged["domain_hash"] = "0" * 64
        elif mode == "span":
            forged["segments"][0]["end"] += 1
        elif mode == "coverage":
            forged["segments"][0]["coverage"] = [[
                forged["segments"][0]["start"], forged["segments"][0]["end"]
            ]]
        elif mode == "status":
            forged["segments"][0]["status"] = "BOGUS"
        forged["state_id"] = "S46_STATE_" + digest({
            "domain": forged["domain_hash"],
            "segments": forged["segments"],
            "root": forged["root_hash"],
        })[:24].upper()
        forged["receipt_hash"] = digest({
            key: value for key, value in forged.items()
            if key not in {"receipt_hash", "episode_id", "clock"}
        })
        with pytest.raises(S46Refusal):
            session.validate_interval_state(forged)
        assert session.read_interval_states()[-1]["status"] == real["status"]
    finally:
        session.close()


def test_self_rehashed_embedded_domain_is_refused_warm_and_cold(tmp_path):
    from candidate import digest
    from s46.session import S46Refusal

    state = tmp_path / "self-rehashed-domain"
    session = _start(state)
    try:
        real = session.produce_interval(
            make_domain(mode="ACTUAL", start=session.clock(), end=session.clock() + 4)
        )
        forged = deepcopy(real)
        forged.pop("episode_id", None)
        forged.pop("clock", None)
        domain = deepcopy(forged["domain"])
        domain["mode"] = "BLOCKED"
        domain["domain_id"] = "S46_DOMAIN_BLOCKED"
        domain.pop("domain_hash", None)
        domain.pop("hash", None)
        domain["domain_hash"] = digest(domain)
        forged["domain"] = domain
        forged["domain_id"] = domain["domain_id"]
        forged["domain_hash"] = domain["domain_hash"]
        forged["state_id"] = "S46_STATE_" + digest({
            "domain": forged["domain_hash"],
            "segments": forged["segments"],
            "root": forged["root_hash"],
        })[:24].upper()
        forged["receipt_hash"] = digest({
            key: value for key, value in forged.items() if key != "receipt_hash"
        })
        with pytest.raises(S46Refusal) as exc:
            session.validate_interval_state(forged)
        assert exc.value.code == "S46_DOMAIN_ISSUANCE_DOMAIN_MISMATCH"
        session.product._append_episode(
            session.branch_id, "A", "S46_INTERVAL_STATE",
            session.clock(), forged,
        )
        session.product._checkpoint(
            session.branch_id, session.clock(), session.world()
        )
        with pytest.raises(S46Refusal):
            session.read_interval_states()
        assert session.verify()["ok"] is False
    finally:
        session.close()
    with pytest.raises(Exception):
        cold = S46Session.open(state)
        cold.close()
