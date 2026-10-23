"""Lawful alternatives, owner independence and refusal boundaries.

Every branch here is a real outcome of the exact upstream mechanisms: a lawful
NO_CHANGE, a lawful DENY, a genuinely distinct second actor, denied material
access, self-performer refusal, time boundaries, future-child refusal and
fabricated-psychology refusal. None of them mutates real state into a target.
"""
from __future__ import annotations

import copy

import pytest

import bp2_joined
from bp2_joined.binding import validate_occurrence_payload
from bp2_joined.producer import (
    ACTUATOR,
    OCCURRENCE_E2,
    JoinedProducer,
    JoinedRefusal,
    joined_consumer_assertion,
)


def _prepare(producer):
    producer.stage_world()
    producer.stage_c8()
    producer.stage_out9()


def _target_rows(producer) -> int:
    row = producer.c9.db.execute("SELECT count(*) FROM target_state").fetchone()
    return int(row[0])


def _occurrence_rows(producer) -> int:
    row = producer.c9.db.execute("SELECT count(*) FROM occurrence").fetchone()
    return int(row[0])


def test_no_change_on_empty_rule_registry_preserves_occurrence_without_target(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        _prepare(producer)
        pipeline = producer.stage_c9(rule_a_registry="empty")
        assert pipeline.committed is True
        assert pipeline.decision.branch.value == "NO_CHANGE"
        assert pipeline.decision.reason.value == "NO_PROPOSAL"
        assert pipeline.response.status.value == "REFUSED"
        assert pipeline.response.reason == "CAN008_RULE_ABSENT_FROM_REGISTRY"
        assert _target_rows(producer) == 0
        assert _occurrence_rows(producer) == 1
        with pytest.raises(JoinedRefusal) as excinfo:
            producer.stage_e2()
        assert excinfo.value.code == "NO_PROPOSAL"


def test_no_change_on_insufficient_enacted_history(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        _prepare(producer)
        refs = JoinedProducer._history_refs(producer.occurrence)
        pipeline = producer.stage_c9(enacted_override=refs[:1])
        assert pipeline.decision.branch.value == "NO_CHANGE"
        assert pipeline.decision.reason.value == "NO_PROPOSAL"
        assert pipeline.response.reason == "INSUFFICIENT_ENACTED_HISTORY"
        assert _target_rows(producer) == 0


def test_lawful_deny_on_self_issued_target_request(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        _prepare(producer)
        pipeline = producer.stage_c9(self_issued=True)
        assert pipeline.decision.branch.value == "DENY"
        assert pipeline.decision.reason.value == "PERMISSION_SELF_ISSUED"
        assert pipeline.committed is True
        assert _target_rows(producer) == 0
        assert _occurrence_rows(producer) == 1


def test_denied_material_access_is_no_eligible_material_not_a_target(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        _prepare(producer)
        pipeline = producer.stage_c9(material_access="denied")
        assert pipeline.material_eligible is False
        assert pipeline.material_reason == "NO_ELIGIBLE_MATERIAL_SOURCE"
        assert pipeline.decision.branch.value == "NO_CHANGE"
        assert pipeline.response.reason == "NO_ELIGIBLE_MATERIAL_SOURCE"
        assert _target_rows(producer) == 0


def test_two_actor_histories_produce_two_distinct_consumed_targets(tmp_path):
    receipts = {}
    for key in ("A", "B"):
        with JoinedProducer(tmp_path / key, actor=key) as producer:
            outcome = producer.run()
            assert outcome.ok is True, outcome.receipt()
            bp2_joined.joined_consumer_assertion(outcome)
            receipts[key] = outcome.receipt()
    a, b = receipts["A"], receipts["B"]
    assert a["actor_id"] == "TEST_ONLY_BP1_ACTOR_A"
    assert b["actor_id"] == "TEST_ONLY_BP1_ACTOR_B"
    assert a["actor_source_hash"] != b["actor_source_hash"]
    assert a["target_id"] != b["target_id"]
    assert a["target_record_hash"] != b["target_record_hash"]
    assert a["consumed_state_hash"] != b["consumed_state_hash"]
    assert a["response_hash"] != b["response_hash"]
    assert a["other_actor_id"] == b["actor_id"]
    assert b["other_actor_id"] == a["actor_id"]


def test_relation_views_are_honest_unknown_or_nonreciprocal(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        occurrence = producer.stage_world()
        for block in (occurrence.payload["actor"], occurrence.payload["other_actor"]):
            assert block["relation_view"], block
            for view in block["relation_view"]:
                assert view["perceived_state"] == "UNKNOWN_OR_NONRECIPROCAL"
                assert view["causal_basis"] == "NO_PSYCHIC_RELATION_OWNER_GRANT"
    with JoinedProducer(tmp_path / "other") as producer:
        occurrence = producer.stage_world()
        assert occurrence.payload["actor"]["actor_id"] != (
            occurrence.payload["other_actor"]["actor_id"])


def test_self_performer_impersonation_refused_then_lawful_e2_admitted(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        joined_consumer_assertion(outcome)
        with pytest.raises(bp2_joined.PortRefusal) as excinfo:
            producer.stage_e2(actuator_ref=producer.occurrence.actor_id)
        assert excinfo.value.code == "E2_ACTUATOR_SELF_BOUND"
        with pytest.raises(bp2_joined.PortRefusal) as excinfo:
            producer.stage_e2(occurrence_ref=producer.occurrence.actor_id)
        assert excinfo.value.code == "E2_OCCURRENCE_SELF_BOUND"
        admission = producer.stage_e2()
        assert admission.admitted is True
        assert admission.actuator_ref == ACTUATOR
        assert admission.occurrence_ref == OCCURRENCE_E2


def test_action_before_target_commit_refused(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        with pytest.raises(bp2_joined.PortRefusal) as excinfo:
            producer.stage_e2(action_time=producer.event_time - 1)
        assert excinfo.value.code == "RESOURCE_NOT_YET_EFFECTIVE"
        assert producer.stage_e2().admitted is True


def test_c9r_refuses_an_action_receipt_before_the_target_commit(tmp_path):
    from candidate import admit_performed_action, make_performed_action_receipt

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        consumed = producer.later_read.state_hash
        receipt = make_performed_action_receipt(
            actor_id=producer.occurrence.actor_id,
            act="inspect_with_tool",
            actuator_ref=ACTUATOR,
            occurrence_ref=OCCURRENCE_E2,
            action_time=producer.event_time - 1,
            consumed_state_hash=consumed,
            target_commit_time=producer.event_time,
        )
        admission = admit_performed_action(
            owner_receipt=receipt,
            expected_actor_id=producer.occurrence.actor_id,
            expected_act="inspect_with_tool",
            consumed_state_hash=consumed,
            as_of=producer.later_as_of,
            target_commit_time=producer.event_time,
        )
        assert getattr(admission, "admitted", False) is False
        assert admission.reason.value == "ACTION_BEFORE_TARGET_COMMIT"


def test_future_and_past_event_times_refused_by_c9r_ingress(tmp_path):
    from candidate import ingress_event

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        raw = producer.e1_event
        event_hash = raw["hash"]
        future = ingress_event(
            raw,
            as_of=producer.event_time - 1,
            last_time=0,
            prior_event_hashes=frozenset(),
            focal_actor_id=producer.occurrence.actor_id,
        )
        assert future.reason.value == "CLOCK_OUTSIDE_FRAME"
        past = ingress_event(
            raw,
            as_of=producer.as_of,
            last_time=producer.event_time,
            prior_event_hashes=frozenset(),
            focal_actor_id=producer.occurrence.actor_id,
        )
        assert past.reason.value == "TIME_REVERSED"
        ok = ingress_event(
            raw,
            as_of=producer.as_of,
            last_time=producer.event_time - 1,
            prior_event_hashes=frozenset(),
            focal_actor_id=producer.occurrence.actor_id,
        )
        assert ok.admitted is True
        assert ok.event_hash == event_hash


def test_future_child_information_refused_before_any_commit(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        occurrence = producer.stage_world()
        payload = copy.deepcopy(occurrence.payload)
        payload["future_child_outcome"] = "COLLEGE"
        with pytest.raises(bp2_joined.BindingRefusal) as excinfo:
            validate_occurrence_payload(payload)
        assert excinfo.value.code == "FUTURE_CHILD_INFORMATION_LEAK"
        nested = copy.deepcopy(occurrence.payload)
        nested["world"]["future_child_personality"] = ["trait"]
        with pytest.raises(bp2_joined.BindingRefusal):
            validate_occurrence_payload(nested)


def test_fabricated_psychology_and_owner_directives_refused(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        occurrence = producer.stage_world()
        psychology = copy.deepcopy(occurrence.payload)
        psychology["actor"]["traits"] = ["conscientious"]
        with pytest.raises(bp2_joined.BindingRefusal) as excinfo:
            validate_occurrence_payload(psychology)
        assert excinfo.value.code == "PSYCHOLOGY_CLAIM_IN_OCCURRENCE"
        directive = copy.deepcopy(occurrence.payload)
        directive["event_id"] = "ADP019-ADMITTED-1"
        with pytest.raises(bp2_joined.BindingRefusal) as excinfo:
            validate_occurrence_payload(directive)
        assert excinfo.value.code == "UNLICENSED_OWNER_DIRECTIVE_IN_OCCURRENCE"
        objective = copy.deepcopy(occurrence.payload)
        objective["world"]["objective_owner"] = "SELF"
        with pytest.raises(bp2_joined.BindingRefusal):
            validate_occurrence_payload(objective)


def test_no_fabricated_psychology_is_stored_in_the_committed_record(tmp_path):
    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        record = producer.c9.read_target_state(producer.pipeline.decision.target_id)
        payload = record["record_preimage"]["governed_payload"]
        assert payload["practice_label"] == "coordinated_material_inspection"
        text = str(record)
        for forbidden in ("personality", "trait", "affect", "attachment", "wound"):
            assert forbidden not in text
