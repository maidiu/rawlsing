"""S39 source-bound generation: positive, choices, labels and no-answer input."""
from __future__ import annotations

import pytest

from s39.bootstrap import install

install()

from s39.model import (  # noqa: E402
    FULL_RULE,
    ComparisonRule,
    S39GenerationRefusal,
)
from s39.producer import GeneratedProducer  # noqa: E402
from s39.session import S39GeneratedSession  # noqa: E402
from s39.sources import context_records, source_digest  # noqa: E402
from candidate import seal  # noqa: E402
from s37.harness import (  # noqa: E402
    case_for,
    setup_neutral_language,
    source_for,
)


@pytest.fixture(scope="module")
def producer(tmp_path_factory):
    root = tmp_path_factory.mktemp("s39-gen")
    case = case_for(True)
    instance = GeneratedProducer(root / "source", case=case, source=source_for(case))
    instance.stage_m35()
    yield instance
    instance.close()


def _records(producer, **flags):
    values = dict(
        actor_id=producer.occurrence.actor_id,
        branch_id="first_session",
        as_of=producer.as_of,
    )
    values.update(flags)
    return context_records(**values)


def test_generated_positive_has_no_supplied_answer_and_retains_contrary(producer):
    receipt = producer.generate(
        source_records=_records(
            producer, repair_urgent=True, avoid_debt=True, prior_b_share=True
        )
    )
    assert receipt["selection_status"] == "UNIQUE_SELECTED"
    assert receipt["selected_option"] == "REQUEST_TOOL"
    assert receipt["input_contains_desired_action"] is False
    assert receipt["attempt_request"]["option_id"] == "REQUEST_TOOL"
    assert receipt["attempt_request"]["target_proposals"] == []
    assert any(
        row["predicate"] == "AVOID_DEBT" for row in receipt["contrary_reasons"]
    )
    assert any(
        row["predicate"] == "PRIOR_B_SHARE" for row in receipt["supporting_reasons"]
    )
    assert receipt["provenance"] == (
        "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED"
    )


def test_same_consumer_end_to_end_and_language_does_not_choose(producer, tmp_path):
    session = S39GeneratedSession.start(
        tmp_path / "share", case=case_for(True), source=source_for(case_for(True))
    )
    try:
        generated = session.read_generation()
        assert generated["status"] == "OK"
        assert generated["selected_option"] == "REQUEST_TOOL"
        assert generated["attempt_status"] == "ADMITTED"
        assert generated["performed"] is True
        assert generated["event_id"]
        assert generated["s36"]["outcome"] == "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION"
        assert generated["s36"]["target_branch"] == "NO_CHANGE"
        assert generated["s36"]["target_reason"] == "NO_PROPOSAL"
        assert generated["s36"]["target_proposals"] == []
        assert generated["s36"]["target_state_rows"] == 0
        assert session.read_s36()["response_ref"] == generated["s36"]["response_ref"]
        assert session.verify()["ok"] is True

        setup_neutral_language(session)
        said = session.say("Hello.")
        assert said["strategy"] == "SAFE_GREETING"
        plan_refs = said["language"]["plan"]["readset"]["source_event_refs"]
        generation_refs = set(generated["generation"]["source_refs"])
        assert not generation_refs.intersection(
            {row.get("event_id") for row in plan_refs}
        )
        assert said["language"]["equivalence"]["status"] == "ACCEPTED"
        assert session.read_s36()["response_ref"] == generated["s36"]["response_ref"]
    finally:
        session.close()


def test_changing_only_actor_context_changes_choice_or_unresolves(producer):
    request = producer.generate(
        source_records=_records(
            producer, repair_urgent=True, avoid_debt=True, prior_b_share=True
        )
    )
    attend = producer.generate(
        source_records=_records(
            producer, avoid_debt=True, prefer_independent=True
        )
    )
    refusal = producer.generate(
        source_records=_records(producer, prior_b_refusal=True)
    )
    open_choice = producer.generate(source_records=_records(producer))
    cycle = producer.generate(
        source_records=_records(
            producer,
            repair_urgent=True,
            avoid_debt=True,
            prior_b_share=True,
            prefer_independent=True,
            prior_b_refusal=True,
        )
    )
    assert request["selected_option"] == "REQUEST_TOOL"
    assert attend["selected_option"] == "ATTEND_OBJECT"
    assert refusal["selected_option"] == "EXPLICIT_REFUSAL"
    assert open_choice["selection_status"] == "OPEN_CHOICE_SET"
    assert open_choice["attempt_request"] is None
    assert cycle["selection_status"] == "CONFLICT_UNRESOLVED"
    assert cycle["unresolved_reason"] == "COMPARISON_CYCLE"
    assert cycle["attempt_request"] is None


def test_missing_comparison_and_labels(producer):
    records = _records(
        producer, repair_urgent=True, avoid_debt=True, prior_b_share=True
    )
    missing = ComparisonRule(
        "S39_GUARDED_CONTEXTUAL_COMPARISON",
        "1-missing",
        (FULL_RULE.comparisons[0],),
        ("missing-coverage test",),
        "PARTIAL",
    )
    partial = producer.generate(source_records=records, rule=missing)
    assert partial["selection_status"] == "OPEN_CHOICE_SET"
    assert partial["unresolved_reason"] == "MISSING_COMPARISON"
    assert partial["attempt_request"] is None

    labelled = producer.generate(
        source_records=_records(
            producer,
            repair_urgent=True,
            avoid_debt=True,
            prior_b_share=True,
            labels={"class": "X", "Enneagram": "Y"},
        )
    )
    assert labelled["selected_option"] == producer.generate(
        source_records=records
    )["selected_option"]
    assert labelled["attempt_request"]["action"] == "REQUEST_TOOL"
    assert labelled["ignored_label_count"] == 2


def test_open_or_cycle_start_appends_no_actor_action(producer, tmp_path):
    open_records = _records(producer)
    state = tmp_path / "open"
    with pytest.raises(S39GenerationRefusal) as exc:
        S39GeneratedSession.start(
            state, case=case_for(True), source=source_for(case_for(True)),
            source_records=open_records,
        )
    assert exc.value.code == "S39_GENERATION_UNRESOLVED"
    assert not (state / "product").exists()
    assert not (state / "session.json").exists()

    cycle_records = _records(
        producer, repair_urgent=True, avoid_debt=True, prior_b_share=True,
        prefer_independent=True, prior_b_refusal=True,
    )
    state_cycle = tmp_path / "cycle"
    with pytest.raises(S39GenerationRefusal) as exc:
        S39GeneratedSession.start(
            state_cycle, case=case_for(True), source=source_for(case_for(True)),
            source_records=cycle_records,
        )
    assert exc.value.code == "S39_GENERATION_UNRESOLVED"
    assert not (state_cycle / "product").exists()
    assert not (state_cycle / "session.json").exists()


def test_missing_or_tampered_source_and_restore(producer, tmp_path):
    records = _records(
        producer, repair_urgent=True, avoid_debt=True, prior_b_share=True
    )
    missing = [dict(row) for row in records if row["predicate"] != "PRIOR_B_SHARE"]
    unresolved = producer.generate(source_records=missing)
    assert unresolved["selection_status"] == "OPEN_CHOICE_SET"
    assert unresolved["attempt_request"] is None

    tampered = [dict(row) for row in records]
    tampered[0] = dict(tampered[0])
    tampered[0]["content"] = {"tampered": True}
    with pytest.raises(S39GenerationRefusal) as exc:
        producer.generate(source_records=tampered)
    assert exc.value.code == "S39_SOURCE_INTEGRITY_REFUSAL"

    restored = producer.generate(source_records=records)
    assert restored["selected_option"] == "REQUEST_TOOL"

    state = tmp_path / "session"
    with pytest.raises(S39GenerationRefusal):
        S39GeneratedSession.start(
            state / "bad", case=case_for(True),
            source=source_for(case_for(True)), source_records=tampered,
        )
    assert not (state / "bad" / "product").exists()
    session = S39GeneratedSession.start(
        state / "good", case=case_for(True),
        source=source_for(case_for(True)), source_records=records,
    )
    try:
        assert session.read_generation()["selected_option"] == "REQUEST_TOOL"
        assert session.verify()["ok"] is True
    finally:
        session.close()


def test_answer_or_performed_response_input_is_refused(producer):
    records = _records(
        producer, repair_urgent=True, avoid_debt=True, prior_b_share=True
    )
    bad = dict(records[0])
    bad["content"] = {"selected_action": "REQUEST_TOOL"}
    bad["source_hash"] = source_digest(bad)
    bad = seal({key: value for key, value in bad.items() if key != "hash"})
    with pytest.raises(S39GenerationRefusal) as exc:
        producer.generate(source_records=[bad])
    assert exc.value.code == "S39_SOURCE_INTEGRITY_REFUSAL"
