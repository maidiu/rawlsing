from dataclasses import replace
from types import ModuleType, SimpleNamespace
import sys

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.gt34_obl031_q69b_comparator_resolver_r2 import (
    ACTOR_FACT_MISSING_OR_UNAUTHORIZED,
    CURRENT_ACCEPTED,
    D08_GRAMMAR_UNRESOLVED,
    INTEGRITY_REF_HASH_REPLAY_FAILURE,
    NONCOMPARABLE,
    NONCURRENT_SYNTHETIC_PROOF,
    NONCURRENT_SYNTHETIC_TEST_ONLY,
    Q69BSourceBinding,
    RespondentDateIntrWindow,
    SyntheticEncounterFixture,
    D08GrammarBinding,
    current_obl048_proof,
    prove_noncurrent_synthetic,
    resolve_current,
)

ACTOR = "urn:hostile:first-canary:actor"
VALIDATOR_MODULE = "rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical"


def _h(c):
    return c * 64


def _ref(kind, key, c):
    return ExactRef(kind, f"urn:hostile:{key}", _h(c))


def _grammar(*, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY, authority_hash=None,
             provenance=("HOSTILE_EXACT_D08_PROVENANCE",)):
    return D08GrammarBinding(
        authority_id="HOSTILE_D08_GRAMMAR",
        authority_version="9.9.9",
        authority_hash=authority_hash or _h("b"),
        authority_kind="PREDICATE_GRAMMAR",
        governed_operation="RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE",
        governed_object_family="EmpiricalPredicate@1.0.0",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "eq", "c"),),
        currentness=currentness,
        provenance_refs=provenance,
    )


def _window(*, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY,
            start="2024-01-01T00:00:00Z", end="2024-12-31T23:59:59Z", lower=True):
    return RespondentDateIntrWindow(
        respondent_ref=_ref("RESPONDENT", "r1", "d"),
        dateintr_ref=_ref("DATEINTR", "r1", "e"),
        window_start=start,
        window_end=end,
        lower_edge_inclusive=lower,
        currentness=currentness,
    )


def _fixture(t="2024-06-01T12:00:00Z"):
    return SyntheticEncounterFixture.build(ACTOR, t)


def _synthetic(**overrides):
    args = dict(
        fixture=_fixture(),
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=_grammar(),
        respondent_windows=(_window(),),
    )
    args.update(overrides)
    return prove_noncurrent_synthetic(**args)


def _fake_record(**changes):
    data = dict(
        authority_id="V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE",
        authority_version="1.0.0",
        realization_state="ENCOUNTER",
        event_effect_kind="OEE_ENCOUNTER_OCCURRED",
        actor_id=ACTOR,
        subject_ref="urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33",
        effective_from="2024-06-01T12:00:00Z",
        record_id="urn:hostile:record",
        record_hash=_h("f"),
    )
    data.update(changes)
    return SimpleNamespace(**data)


def _install_accepting_validator(monkeypatch, returned):
    mod = ModuleType(VALIDATOR_MODULE)
    mod.validate_record = lambda _record: returned
    monkeypatch.setitem(sys.modules, VALIDATOR_MODULE, mod)


def _current(monkeypatch, record):
    _install_accepting_validator(monkeypatch, record)
    return resolve_current(
        actor_record=record,
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=_grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(_window(currentness=CURRENT_ACCEPTED),),
    )


def test_hostile_real_lane_cannot_turn_missing_fact_into_any_output():
    sys.modules.pop(VALIDATOR_MODULE, None)
    result = resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=None,
        respondent_windows=(),
    )
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None and result.receipt is None and result.synthetic_preview is None


def test_hostile_synthetic_to_current_laundering_is_rejected_before_validation():
    result = resolve_current(
        actor_record=_fixture(),
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=_grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(_window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.predicate is None and result.receipt is None


def test_hostile_fixture_mode_forgery_fails_closed():
    forged = replace(_fixture(), fixture_mode=CURRENT_ACCEPTED)
    result = _synthetic(fixture=forged)
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.synthetic_preview is None


def test_hostile_fixture_hash_replay_forgery_fails_closed():
    forged = replace(_fixture(), fixture_hash=_h("0"))
    assert _synthetic(fixture=forged).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_hostile_obl048_proposition_mutation_is_noncomparable():
    proof = replace(current_obl048_proof(), proposition="SUBJECT_IS_SOMETHING_ELSE")
    result = _synthetic(classification_proof=proof)
    assert result.outcome == NONCOMPARABLE
    assert result.synthetic_preview is None


def test_hostile_q69b_release_replay_drift_cannot_emit_preview():
    source = replace(Q69BSourceBinding(), replay_hash=_h("1"))
    result = _synthetic(q69b_binding=source)
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.synthetic_preview is None


def test_hostile_empty_d08_provenance_is_integrity_failure():
    result = _synthetic(grammar_binding=_grammar(provenance=()))
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.synthetic_preview is None


def test_hostile_d08_authority_hash_mutation_must_not_remain_authorized():
    canonical = _synthetic(grammar_binding=_grammar(authority_hash=_h("2")))
    mutated = _synthetic(grammar_binding=_grammar(authority_hash=_h("3")))
    assert canonical.outcome == NONCURRENT_SYNTHETIC_PROOF
    assert mutated.outcome in (D08_GRAMMAR_UNRESOLVED, INTEGRITY_REF_HASH_REPLAY_FAILURE)


def test_hostile_naive_actor_effective_time_must_fail_closed_not_escape(monkeypatch):
    record = _fake_record(effective_from="2024-06-01T12:00:00")
    result = _current(monkeypatch, record)
    assert result.outcome in (NONCOMPARABLE, INTEGRITY_REF_HASH_REPLAY_FAILURE)
    assert result.predicate is None


def test_hostile_wrong_subject_after_accepting_validator_still_cannot_compose(monkeypatch):
    record = _fake_record(subject_ref="urn:hostile:wrong-subject")
    result = _current(monkeypatch, record)
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_hostile_unknown_dateintr_lower_edge_never_defaults_to_inclusion():
    w = _window(start="2024-06-01T12:00:00Z", lower=None)
    result = _synthetic(respondent_windows=(w,))
    assert result.outcome == NONCOMPARABLE
    assert result.synthetic_preview is None
