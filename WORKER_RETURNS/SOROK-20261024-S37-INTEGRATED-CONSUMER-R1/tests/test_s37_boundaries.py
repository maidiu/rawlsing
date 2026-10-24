"""Focused S37 source/access/response/language boundary tests."""
from __future__ import annotations

import pytest

from s37.bootstrap import install

install()

from candidate import ResponseStatus, digest
from candidate.actor_access_response import (
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    RECEIVABLE_NO_OBSERVED_UPTAKE,
    UNKNOWN_RECEIVABILITY,
    make_actor_local_access_witness,
    make_actor_owned_response_witness,
)
from firstclass import MaterialSourceRefusal
from language_mediation.artifacts import (
    build_native_artifact,
    build_translation_artifact,
)
from language_mediation.equivalence import evaluate_pair
from s37.harness import (
    NATIVE_SELF,
    TRIGGER,
    case_for,
    fresh_store,
    producer_for,
    reseal_with,
    setup_neutral_language,
    setup_source_language,
    source_for,
    start_session,
)
from s37.producer import IntegratedProducer


def _access(producer, **overrides):
    values = {
        "actor_id": producer.occurrence.actor_id,
        "event_ref": producer.e1_event["hash"],
        "access_time": producer.event_time,
        "source_ref": "TEST_ONLY_ADP017_ACCESS_S37_TEST",
        "access_status": "ACCESSIBLE",
        "scene": producer.e1_event["content"]["scene"],
        "content": {"c8_occurrence_id": producer.out9.occurrence_id},
        "revoked": False,
    }
    values.update(overrides)
    return make_actor_local_access_witness(**values)


def _response(producer, **overrides):
    values = {
        "actor_id": producer.occurrence.actor_id,
        "event_ref": producer.e1_event["hash"],
        "response_ref": "TEST_ONLY_S37_A_REQUEST_TOOL",
        "response_kind": "REQUEST_TOOL",
        "response_time": producer.event_time + 1,
        "source_ref": "TEST_ONLY_A_RESPONSE_S37_TEST",
        "content": {"c8_occurrence_id": producer.out9.occurrence_id},
        "revoked": False,
    }
    values.update(overrides)
    return make_actor_owned_response_witness(**values)


@pytest.fixture(scope="module")
def share_producer(tmp_path_factory):
    root = tmp_path_factory.mktemp("s37-boundary-producer")
    producer, case, source = producer_for(root, share=True)
    yield producer, case, source
    producer.close()


def _tables_empty(store) -> bool:
    return all(not rows for rows in store.snapshot().values())


def test_access_severance_same_c8_e1_fault_restore(share_producer, tmp_path):
    producer, _, _ = share_producer
    c8 = producer.out9.readset["state_digest"]
    e1 = producer.e1_event["hash"]
    with fresh_store(tmp_path / "positive.sqlite") as store:
        positive = producer.evaluate_s36(store=store)
    with fresh_store(tmp_path / "fault.sqlite") as store:
        fault = producer.evaluate_s36(store=store, access_witness=None)
    with fresh_store(tmp_path / "restored.sqlite") as store:
        restored = producer.evaluate_s36(store=store)
    assert positive.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert positive.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    assert fault.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
    assert fault.response.reason == UNKNOWN_RECEIVABILITY
    assert restored.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert restored.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    for result in (positive, fault, restored):
        assert result.response.target_proposals == ()
        assert result.decision.branch.value == "NO_CHANGE"
        assert result.decision.reason.value == "NO_PROPOSAL"
    assert producer.out9.readset["state_digest"] == c8
    assert producer.e1_event["hash"] == e1


def test_missing_own_response_is_valid_empty(share_producer, tmp_path):
    producer, _, _ = share_producer
    with fresh_store(tmp_path / "no-response.sqlite") as store:
        result = producer.evaluate_s36(store=store, response_witness=None)
        assert result.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert result.response.reason == RECEIVABLE_NO_OBSERVED_UPTAKE
        assert result.response.target_proposals == ()
        assert result.decision.branch.value == "NO_CHANGE"
        assert result.decision.reason.value == "NO_PROPOSAL"
        assert store.committed_target_ids() == frozenset()


def _mutate_access(producer, case: str):
    if case == "wrong_actor":
        return _access(producer, actor_id="TEST_ONLY_OTHER_ACTOR")
    if case == "wrong_event":
        return _access(producer, event_ref="TEST_ONLY_WRONG_EVENT")
    if case == "wrong_hash":
        return reseal_with(_access(producer), source_hash=digest({"tampered": "access"}))
    if case == "wrong_scene":
        return _access(producer, scene="TEST_ONLY_OTHER_ROOM")
    if case == "before_event":
        return _access(producer, access_time=producer.event_time - 1)
    if case == "after_as_of":
        return _access(producer, access_time=producer.as_of + 1)
    if case == "revoked_field":
        return _access(producer, revoked=True)
    raise AssertionError(case)


def _mutate_response(producer, case: str):
    if case == "wrong_actor":
        return _response(producer, actor_id="TEST_ONLY_OTHER_ACTOR")
    if case == "wrong_event":
        return _response(producer, event_ref="TEST_ONLY_WRONG_EVENT")
    if case == "wrong_hash":
        return reseal_with(_response(producer), source_hash=digest({"tampered": "response"}))
    if case == "before_access":
        return _response(producer, response_time=producer.event_time - 1)
    if case == "after_as_of":
        return _response(producer, response_time=producer.as_of + 1)
    if case == "revoked_field":
        return _response(producer, revoked=True)
    if case == "bad_kind":
        return _response(producer, response_kind="INFERRED_GRATITUDE")
    raise AssertionError(case)


@pytest.mark.parametrize(
    "kind,case",
    [
        ("access", "wrong_actor"),
        ("access", "wrong_event"),
        ("access", "wrong_hash"),
        ("access", "wrong_scene"),
        ("access", "before_event"),
        ("access", "after_as_of"),
        ("access", "revoked_field"),
        ("response", "wrong_actor"),
        ("response", "wrong_event"),
        ("response", "wrong_hash"),
        ("response", "before_access"),
        ("response", "after_as_of"),
        ("response", "revoked_field"),
        ("response", "bad_kind"),
    ],
)
def test_wrong_witness_is_refused_without_positive_or_target(
    kind, case, share_producer, tmp_path
):
    producer, _, _ = share_producer
    access = _access(producer)
    response = _response(producer)
    if kind == "access":
        access = _mutate_access(producer, case)
    else:
        response = _mutate_response(producer, case)
    with fresh_store(tmp_path / f"{kind}-{case}.sqlite") as store:
        result = producer.evaluate_s36(
            store=store, access_witness=access, response_witness=response
        )
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.target_proposals == ()
        assert result.decision is None
        assert result.receipt is None
        assert result.committed is False
        assert result.no_ghost is True
        assert _tables_empty(store)


def test_revoked_source_ref_is_refused(share_producer, tmp_path):
    producer, _, _ = share_producer
    access = _access(producer)
    with fresh_store(tmp_path / "revoked-source.sqlite") as store:
        result = producer.evaluate_s36(
            store=store,
            access_witness=access,
            response_witness=_response(producer),
            revoked_source_refs=frozenset({access["source_ref"]}),
        )
        assert result.response.status is ResponseStatus.REFUSED
        assert result.response.reason == "S35_ACCESS_REVOKED"
        assert _tables_empty(store)


def test_m35_source_preimage_rejected_before_c8(tmp_path):
    case = case_for(True)
    source = source_for(case)
    mutations = {
        "wrong_owner": {"b_owner": "FAKE_OWNER"},
        "wrong_event_hash": {"b_event_hash": "0" * 64},
        "wrong_clock": {"b_clock": 999},
        "wrong_operation": {"b_operation": "REFUSE_TOOL", "b_quantity": 0},
        "wrong_quantity": {"b_quantity": 5},
        "wrong_e1_hash": {"a_e1_hash": "0" * 64},
    }
    for label, mutation in mutations.items():
        changed = dict(source)
        changed.update(mutation)
        root = tmp_path / label
        with pytest.raises(MaterialSourceRefusal) as exc:
            IntegratedProducer(root, case=case, source=changed)
        assert exc.value.code == "MATERIAL_SOURCE_PREIMAGE_MISMATCH"
        assert not (root / "bp2").exists()


def test_language_semantic_guard_rejects_unsupported_strengthening(tmp_path):
    session = start_session(tmp_path / "guard", share=True)
    try:
        setup_neutral_language(session)
        plan = session.expression_plan(trigger_kind="SAY", text="Hello.")
        assert plan.unit["unit_id"] == "SAFE_BENCH"
        native = build_native_artifact(
            plan, atoms=["BENCH_PRESENT", "SELF_RELIANCE_FAMILY"]
        )
        translation = build_translation_artifact(
            plan, native, atoms=["BENCH_PRESENT", "SELF_RELIANCE_FAMILY"]
        )
        receipt = evaluate_pair(plan, native, translation)
        assert receipt["status"] == "REJECTED"
        assert "UNAUTHORIZED_MEANING_STRENGTHENED" in receipt["codes"]
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_language_access_loss_preserves_fallback_and_source(tmp_path):
    session = start_session(tmp_path / "language-loss", share=True)
    try:
        data = setup_source_language(session)
        first = session.say(TRIGGER)
        assert first["strategy"] == "SELF_RELIANCE"
        assert first["candidate"]["speech"] == NATIVE_SELF
        assert first["language"]["fallback"] is False
        before = session.read_s36()
        session.revoke_language_access(data["family_receipt"])
        refused = session.say(TRIGGER)
        assert refused["strategy"] == "SAFE_GREETING"
        assert refused["language"]["fallback"] is True
        assert refused["language"]["fallback_reason"] == (
            "SOURCE_DEPENDENT_UNIT_UNAVAILABLE"
        )
        assert refused["language"]["source_dependent_refused"] is True
        assert data["family_relation"] in refused["language"]["plan"]["readset"][
            "invalidated_relation_ids"
        ]
        session.restore_language_access(data["family_receipt"])
        restored = session.say(TRIGGER)
        assert restored["strategy"] == "SELF_RELIANCE"
        assert restored["language"]["fallback"] is False
        after = session.read_s36()
        assert after["response_ref"] == before["response_ref"]
        assert after["target_branch"] == "NO_CHANGE"
        assert session.verify()["ok"] is True
    finally:
        session.close()
