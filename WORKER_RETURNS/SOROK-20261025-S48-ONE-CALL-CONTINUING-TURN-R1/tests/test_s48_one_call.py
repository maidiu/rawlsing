"""Focused S48 one-call product orchestration tests."""
from __future__ import annotations

from copy import deepcopy

import pytest

from s48.bootstrap import install

install()

from s45.fixtures import root_bundle  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s48.errors import ProductCallError, S48Refusal  # noqa: E402
from s48.product import build_payload, parse_envelope  # noqa: E402
from s48.session import S48Session, SCI05_REASON  # noqa: E402


def _start(state, seed="01" * 32):
    case = case_for(True)
    return S48Session.start(
        state,
        bundle=root_bundle(seed),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _envelope(self_account=None, candidate="OTHER_SHARES_TOOL"):
    return {
        "schema": "S48_PRODUCT_ENVELOPE@1",
        "narrative": "The prior turn is retained.",
        "self_account": self_account,
        "self_account_present": bool(self_account),
        "prospective": ([{
            "candidate_id": candidate,
            "rationale": "A unique allowed world proposal.",
        }] if candidate else []),
    }


def _runner(envelope=None, *, calls=None, receipt=None, error=None):
    def run(prompt, *, workdir, log_dir, timeout):
        if calls is not None:
            calls.append({
                "prompt": prompt,
                "workdir": str(workdir),
                "log_dir": str(log_dir),
                "timeout": timeout,
            })
        if error:
            raise error
        return {
            "status": "OK",
            "envelope": dict(envelope or _envelope()),
            "call_receipt": dict(receipt or {
                "actual_provider_call": False,
                "provider_call_count": 1,
                "step_count": 1,
                "output_sha256": "fixture",
            }),
            "prompt_hash": "fixture-prompt",
        }
    return run


def test_positive_absent_self_account_realizes_one_independent_event_and_is_idempotent(tmp_path):
    state = tmp_path / "positive"
    session = _start(state)
    calls = []
    try:
        session.produce_interval(
            make_domain(mode="SCHEDULED_ONLY", start=session.clock(), end=session.clock() + 4)
        )
        before_events = session.read_events()
        before_root = session.read_root()["root_hash"]
        result = session.run_turn(product_runner=_runner(calls=calls))
        assert result["status"] == "REALIZED"
        assert result["provider_call_count"] == 1
        assert result["no_input_barrier"] == "SELF_ACCOUNT_ABSENT_NO_NEW_INTERPRETIVE_INPUT"
        assert result["candidate_id"] == "OTHER_SHARES_TOOL"
        assert result["event_ref"]
        assert len(calls) == 1
        assert len(session.read_events()) == len(before_events) + 1
        assert session.read_root()["root_hash"] == before_root
        assert session.verify()["ok"] is True
        c9 = session.read_c9_conditioning(result["event_ref"])
        assert c9["s47_source_in_readset"] is True
        assert c9["target_branch"] == "NO_CHANGE"
        event_ref = result["event_ref"]
        session.close()

        cold = S48Session.open(state)
        try:
            cached = cold.run_turn(product_runner=_runner(calls=calls))
            assert cached["status"] == "REALIZED"
            assert cached["cached"] is True
            assert cached["provider_call_count"] == 0
            assert cached["event_ref"] == event_ref
            assert len(calls) == 1
            assert len(cold.read_events()) == len(before_events) + 1
            assert cold.verify()["ok"] is True
        finally:
            cold.close()
    finally:
        try:
            session.close()
        except Exception:
            pass


def test_nonempty_self_account_holds_sci05_and_does_not_realize_dependent_event(tmp_path):
    session = _start(tmp_path / "hold")
    calls = []
    try:
        before = len(session.read_events())
        result = session.run_turn(
            product_runner=_runner(
                envelope=_envelope(self_account="I propose a private self-account."),
                calls=calls,
            )
        )
        assert result["status"] == "SCI05_HOLD"
        assert result["sci05_hold"] is True
        assert result["reason"] == SCI05_REASON
        assert result["prospective_not_realized"] is True
        assert result["event_ref"] == ""
        assert len(session.read_events()) == before
        assert len(calls) == 1
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = S48Session.open(tmp_path / "hold")
    try:
        cached = cold.run_turn(product_runner=_runner(calls=calls))
        assert cached["status"] == "SCI05_HOLD"
        assert cached["cached"] is True
        assert cached["provider_call_count"] == 0
        assert len(calls) == 1
    finally:
        cold.close()


@pytest.mark.parametrize("candidate,status", [
    ("", "NO_PROSPECTIVE_PROPOSAL"),
    ("OTHER_SHARES_TOOL,OTHER_REFUSES_TOOL", "UNRESOLVED"),
])
def test_multiple_or_absent_prospective_options_are_unresolved_not_inaction(tmp_path, candidate, status):
    session = _start(tmp_path / status)
    try:
        before = len(session.read_events())
        if candidate:
            ids = candidate.split(",")
            envelope = _envelope(candidate=ids[0])
            envelope["prospective"] = [
                {"candidate_id": item, "rationale": "candidate"} for item in ids
            ]
        else:
            envelope = _envelope(candidate="")
        result = session.run_turn(product_runner=_runner(envelope=envelope))
        assert result["status"] == status
        assert result["event_ref"] == ""
        assert len(session.read_events()) == before
        assert result["cached"] is False
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_call_failure_is_persisted_without_realizing_next_event(tmp_path):
    session = _start(tmp_path / "failure")
    calls = []
    try:
        before = len(session.read_events())
        failure = ProductCallError(
            "S48_PRODUCT_CALL_FAILED", "fixture",
            {"actual_provider_call": False, "provider_call_count": 0},
        )
        result = session.run_turn(
            product_runner=_runner(calls=calls, error=failure)
        )
        assert result["status"] == "CALL_FAILED"
        assert result["provider_call_count"] == 0
        assert result["event_ref"] == ""
        assert len(session.read_events()) == before
        assert len(calls) == 1
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = S48Session.open(tmp_path / "failure")
    try:
        cached = cold.run_turn(product_runner=_runner(calls=calls))
        assert cached["status"] == "CALL_FAILED"
        assert cached["cached"] is True
        assert len(calls) == 1
    finally:
        cold.close()


def test_prompt_payload_is_bounded_to_public_event_world_and_finite_candidates(tmp_path):
    session = _start(tmp_path / "payload")
    try:
        payload = build_payload(session)
        assert payload["schema"] == "S48_ACTOR_PRODUCT_INPUT@1"
        assert payload["event_ref"]
        assert payload["c9_result"]["target_branch"] == "NO_CHANGE"
        assert "source" not in payload
        assert "generation" not in payload
        assert "private" not in str(payload).lower()
        assert {
            row["candidate_id"] for row in payload["allowed_prospective_candidates"]
        } == {"OTHER_SHARES_TOOL"}
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


def test_injected_runner_envelope_is_not_treated_as_actual_provider_call(tmp_path):
    session = _start(tmp_path / "fixture-mark")
    try:
        result = session.run_turn(product_runner=_runner())
        assert result["provider_call_count"] == 1
        turn = session.product_turn(result["source_event_ref"])
        assert turn["body"]["call_receipt"]["actual_provider_call"] is False
    finally:
        session.close()
