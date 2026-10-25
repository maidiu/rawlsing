"""Focused S48 source-owner boundary and orchestration tests."""
from __future__ import annotations

import pytest

from s48.bootstrap import install

install()

from s45.fixtures import root_bundle  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s48.errors import ProductCallError, S48Refusal  # noqa: E402
from s48.product import build_payload, eligible_candidate_ids, parse_envelope  # noqa: E402
from s48.session import S48Session, SCI05_REASON  # noqa: E402
from s48.sources import (
    MISSING_FUNCTION,
    SOURCE_OWNER_HOLD,
    candidate_specs,
    issue_current_source,
)  # noqa: E402


def _start(state, seed="01" * 32):
    case = case_for(True)
    return S48Session.start(
        state, bundle=root_bundle(seed), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )


def _envelope(candidate="OTHER_REFUSES_TOOL", self_account=None):
    return {
        "schema": "S48_PRODUCT_ENVELOPE@1",
        "narrative": "The prior turn is retained.",
        "self_account": self_account,
        "self_account_present": bool(self_account),
        "prospective": ([{"candidate_id": candidate, "rationale": "fixture"}]
                        if candidate else []),
    }


def _runner(envelope=None, *, calls, receipt=None, error=None):
    def run(prompt, *, workdir, log_dir, timeout):
        calls.append(1)
        if error:
            raise error
        return {
            "status": "OK",
            "envelope": dict(envelope or _envelope()),
            "call_receipt": dict(receipt or {
                "actual_provider_call": False,
                "provider_call_count": 1,
                "step_count": 1,
            }),
            "prompt_hash": "fixture",
        }
    return run


def _identity(session):
    world = session.world()
    return {
        "events": len(world.events),
        "clock": session.clock(),
        "material": dict(world.actor_state["A"]).get("material_remaining"),
        "b_material": dict(world.actor_state["B"]).get("material_remaining"),
        "root_hash": session.read_root()["root_hash"],
        "c12_events": len(session.read_events()),
    }


def test_unsupported_fake_b_operation_is_source_owner_hold_with_no_world_or_c8_effect(tmp_path):
    session = _start(tmp_path / "hold")
    calls = []
    try:
        before = _identity(session)
        result = session.run_turn(product_runner=_runner(calls=calls))
        after = _identity(session)
        assert result["status"] == "SOURCE_OWNER_HOLD"
        assert result["reason"] == SOURCE_OWNER_HOLD
        assert result["missing_function"] == MISSING_FUNCTION
        assert result["event_ref"] == ""
        assert result["provider_call_count"] == 1
        assert before == after
        assert len(calls) == 1
        assert session.verify()["ok"] is True
        assert not any(
            row.get("status") == "REALIZED" for row in session.product_turns()
        )
    finally:
        session.close()


def test_explicit_replay_and_cold_replay_do_not_call_again(tmp_path):
    state = tmp_path / "replay"
    session = _start(state)
    calls = []
    try:
        first = session.run_turn(product_runner=_runner(calls=calls))
        source_ref = first["source_event_ref"]
        turn_id = first["turn_id"]
        replay = session.run_turn(
            source_event_ref=source_ref, product_runner=_runner(calls=calls)
        )
        by_id = session.run_turn(
            replay_turn_id=turn_id, product_runner=_runner(calls=calls)
        )
        assert replay["cached"] is True
        assert by_id["cached"] is True
        assert replay["event_ref"] == ""
        assert replay["provider_call_count"] == 0
        assert len(calls) == 1
        session.close()
        cold = S48Session.open(state)
        try:
            cold_replay = cold.run_turn(
                source_event_ref=source_ref, product_runner=_runner(calls=calls)
            )
            assert cold_replay["cached"] is True
            assert cold_replay["turn_id"] == turn_id
            assert len(calls) == 1
        finally:
            cold.close()
    finally:
        session.close()


def test_crash_after_provider_before_final_turn_is_pending_without_reissue(tmp_path):
    session = _start(tmp_path / "crash")
    calls = []
    try:
        original = session._append_turn

        def fail(body):
            raise RuntimeError("append failed after product call")

        session._append_turn = fail
        with pytest.raises(RuntimeError):
            session.run_turn(product_runner=_runner(calls=calls))
        session._append_turn = original
        assert len(calls) == 1
        assert session.product_dispatches()
        before = len(session.read_events())
        pending = session.run_turn(product_runner=_runner(calls=calls))
        assert pending["status"] == "PENDING_UNKNOWN"
        assert pending["reason"] == "S48_DISPATCH_WITHOUT_RESULT_NOT_REISSUED"
        assert pending["provider_call_count"] == 0
        assert len(calls) == 1
        assert len(session.read_events()) == before
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_call_failure_is_persisted_without_realizing_next_event(tmp_path):
    session = _start(tmp_path / "failure")
    calls = []
    try:
        before = _identity(session)
        error = ProductCallError(
            "S48_PRODUCT_CALL_FAILED", "fixture",
            {"actual_provider_call": False, "provider_call_count": 0},
        )
        result = session.run_turn(product_runner=_runner(calls=calls, error=error))
        assert result["status"] == "CALL_FAILED"
        assert result["event_ref"] == ""
        assert _identity(session) == before
        assert len(calls) == 1
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_nonempty_self_account_still_sci05_holds_without_event(tmp_path):
    session = _start(tmp_path / "sci05")
    calls = []
    try:
        before = _identity(session)
        result = session.run_turn(product_runner=_runner(
            envelope=_envelope(self_account="a proposed self-account"), calls=calls
        ))
        assert result["status"] == "SCI05_HOLD"
        assert result["sci05_hold"] is True
        assert result["reason"] == SCI05_REASON
        assert result["event_ref"] == ""
        assert _identity(session) == before
        assert len(calls) == 1
    finally:
        session.close()


def test_payload_has_no_qualified_candidates_and_no_foreign_source_json(tmp_path):
    session = _start(tmp_path / "payload")
    try:
        payload = build_payload(session)
        assert payload["allowed_prospective_candidates"] == []
        assert eligible_candidate_ids(session) == []
        assert candidate_specs(session) == []
        assert "TEST_ONLY_EVENT_share" not in str(payload)
        assert "TEST_ONLY_OWNER_share" not in str(payload)
        assert "private" not in str(payload).lower()
        with pytest.raises(S48Refusal) as exc:
            issue_current_source(session, "OTHER_REFUSES_TOOL")
        assert exc.value.code == SOURCE_OWNER_HOLD
        assert _identity(session)["events"] == 13
    finally:
        session.close()


def test_foreign_static_share_candidate_is_rejected_without_world_event(tmp_path):
    session = _start(tmp_path / "foreign")
    calls = []
    try:
        before = _identity(session)
        result = session.run_turn(product_runner=_runner(
            envelope=_envelope(candidate="OTHER_SHARES_TOOL"), calls=calls
        ))
        assert result["status"] == "SOURCE_OWNER_HOLD"
        assert _identity(session) == before
        assert len(calls) == 1
        with pytest.raises(S48Refusal):
            issue_current_source(session, "OTHER_SHARES_TOOL")
    finally:
        session.close()


def test_empty_prospective_also_holds_without_event(tmp_path):
    session = _start(tmp_path / "empty")
    try:
        before = _identity(session)
        result = session.run_turn(product_runner=_runner(
            envelope=_envelope(candidate=""), calls=[]
        ))
        assert result["status"] == "SOURCE_OWNER_HOLD"
        assert result["event_ref"] == ""
        assert _identity(session) == before
    finally:
        session.close()


@pytest.mark.parametrize("value,code", [
    ("not-json", "S48_PRODUCT_MALFORMED_JSON"),
    ('{"narrative":"x","self_account":null,"prospective":[],"extra":1}',
     "S48_PRODUCT_ENVELOPE_SHAPE"),
    ('{"narrative":"x","self_account":null,"prospective":[{"candidate_id":"BAD","rationale":"x"}]}',
     "S48_PRODUCT_CANDIDATE_UNAUTHORIZED"),
])
def test_malformed_or_unauthorized_product_output_is_typed(value, code):
    with pytest.raises(S48Refusal) as exc:
        parse_envelope(value)
    assert exc.value.code == code


def test_no_fake_positive_canonical_result_or_psyche_write(tmp_path):
    session = _start(tmp_path / "no-fake")
    try:
        before = _identity(session)
        result = session.run_turn(product_runner=_runner(calls=[]))
        assert result["status"] == "SOURCE_OWNER_HOLD"
        assert result["event_ref"] == ""
        assert _identity(session) == before
        assert all(row["body"].get("status") != "REALIZED"
                   for row in session.product_turns())
    finally:
        session.close()
