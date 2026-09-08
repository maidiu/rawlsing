from dataclasses import replace
from types import ModuleType, SimpleNamespace
import sys

from rawlsing_next.pre553_empirical_objects import EmpiricalPredicate, ExactRef
from rawlsing_next.gt34_obl031_q69b_comparator_resolver_r2 import (
    ACTOR_FACT_MISSING_OR_UNAUTHORIZED,
    AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING,
    AUTHORITY_CONTENT_HASH,
    CURRENT_ACCEPTED,
    D08_GRAMMAR_UNRESOLVED,
    INTEGRITY_REF_HASH_REPLAY_FAILURE,
    LAWFUL_VALID_EMPTY,
    NO_EXACT_MATCH,
    NONCOMPARABLE,
    NONCURRENT_SYNTHETIC_PROOF,
    NONCURRENT_SYNTHETIC_TEST_ONLY,
    OBL048_AUTHORITY_HASH,
    OBL048_PROPOSITION_HASH,
    Q69B_ACCEPTED_RELEASE_HASH,
    Q69BSourceBinding,
    RespondentDateIntrWindow,
    SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED,
    SyntheticEncounterFixture,
    D08GrammarBinding,
    authority_identity,
    current_obl048_proof,
    prove_noncurrent_synthetic,
    resolve_current,
)

MODULE = "rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical"
ACTOR = "urn:test:actor:first-canary"


def h(ch):
    return ch * 64


def ref(kind, tag, ch="a"):
    return ExactRef(kind, f"urn:test:{tag}", h(ch))


def grammar(*, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY, kind="PREDICATE_GRAMMAR",
            op="RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE_EQ_PREDICATE"):
    return D08GrammarBinding(
        authority_id="TEST_D08_EXACT_GRAMMAR",
        authority_version="1.0.0",
        authority_hash=h("b"),
        authority_kind=kind,
        governed_operation=op,
        governed_object_family="EmpiricalPredicate@1.0.0",
        operator_semantics_refs=(ref("OPERATOR_SEMANTICS", "eq", "c"),),
        currentness=currentness,
        provenance_refs=("NONCURRENT_SYNTHETIC_TEST_ONLY",),
    )


def window(tag="r1", *, start="2024-01-01T00:00:00Z", end="2024-12-31T23:59:59Z",
           lower=True, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY):
    return RespondentDateIntrWindow(
        respondent_ref=ref("RESPONDENT", tag, "d"),
        dateintr_ref=ref("DATEINTR", tag, "e"),
        window_start=start,
        window_end=end,
        lower_edge_inclusive=lower,
        currentness=currentness,
    )


def fixture(time="2024-06-15T12:00:00Z"):
    return SyntheticEncounterFixture.build(ACTOR, time)


def synth(**kwargs):
    args = dict(
        fixture=fixture(),
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(),
        respondent_windows=(window(),),
    )
    args.update(kwargs)
    return prove_noncurrent_synthetic(**args)


def fake_current_record(**changes):
    base = dict(
        authority_id="V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE",
        authority_version="1.0.0",
        realization_state="ENCOUNTER",
        event_effect_kind="OEE_ENCOUNTER_OCCURRED",
        actor_id=ACTOR,
        subject_ref="urn:rawlsing:v3:subject:sha256:a0d7805874dc8449fa81770254a59accde050871aed13501902502e317273f33",
        effective_from="2024-06-15T12:00:00Z",
        record_id="urn:test:record",
        record_hash=h("f"),
    )
    base.update(changes)
    return SimpleNamespace(**base)


def install_validator(monkeypatch, record=None, *, raises=None):
    mod = ModuleType(MODULE)
    if raises is not None:
        def validate_record(_):
            raise raises
    else:
        def validate_record(x):
            return record if record is not None else x
    mod.validate_record = validate_record
    monkeypatch.setitem(sys.modules, MODULE, mod)


def current_negative(monkeypatch, record, **kwargs):
    install_validator(monkeypatch, record)
    args = dict(
        actor_record=record,
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    args.update(kwargs)
    return resolve_current(**args)


def test_r2_authority_identity_content_addressed():
    assert authority_identity()[2] == AUTHORITY_CONTENT_HASH
    assert len(AUTHORITY_CONTENT_HASH) == 64


def test_real_current_invocation_missing_fact_is_exact_typed_negative_without_hq_module():
    sys.modules.pop(MODULE, None)
    result = resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=None,
        respondent_windows=(),
    )
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None and result.receipt is None


def test_noncurrent_synthetic_positive_proves_only_preview_plus_receipt():
    result = synth()
    assert result.outcome == NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.synthetic_preview is not None
    assert not isinstance(result.synthetic_preview, EmpiricalPredicate)
    assert result.synthetic_preview.fixture_mode == NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.synthetic_preview.predicate_ast["canonical_value"] == "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
    assert result.receipt.currentness == NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.obl048_authority_hash == OBL048_AUTHORITY_HASH
    assert result.receipt.obl048_proposition_hash == OBL048_PROPOSITION_HASH
    assert result.receipt.source_release_scope[-1] == Q69B_ACCEPTED_RELEASE_HASH


def test_synthetic_fixture_mechanically_rejected_by_current_api():
    result = resolve_current(
        actor_record=fixture(), expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(), q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.predicate is None


def test_missing_current_obl055_validator_fails_closed_for_nonmissing_record():
    sys.modules.pop(MODULE, None)
    result = resolve_current(
        actor_record=fake_current_record(), expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(), q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_current_obl055_validator_rejection_fails_closed(monkeypatch):
    install_validator(monkeypatch, raises=ValueError("bad replay"))
    result = resolve_current(
        actor_record=fake_current_record(), expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(), q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_wrong_adp010_owner_fails_closed_after_validator(monkeypatch):
    assert current_negative(monkeypatch, fake_current_record(authority_id="WRONG")).outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_wrong_state_fails_closed_after_validator(monkeypatch):
    assert current_negative(monkeypatch, fake_current_record(realization_state="OPPORTUNITY")).outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_wrong_effect_fails_closed_after_validator(monkeypatch):
    assert current_negative(monkeypatch, fake_current_record(event_effect_kind="WRONG")).outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_wrong_actor_fails_closed_after_validator(monkeypatch):
    assert current_negative(monkeypatch, fake_current_record(actor_id="urn:test:other")).outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_wrong_subject_fails_closed_after_validator(monkeypatch):
    assert current_negative(monkeypatch, fake_current_record(subject_ref="urn:test:other-subject")).outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_wrong_obl048_subject_proof_fails_noncomparable(monkeypatch):
    proof = replace(current_obl048_proof(), subject_ref="urn:test:other-subject")
    assert current_negative(monkeypatch, fake_current_record(), classification_proof=proof).outcome == NONCOMPARABLE


def test_wrong_obl048_authority_hash_fails_noncomparable(monkeypatch):
    proof = replace(current_obl048_proof(), authority_hash=h("9"))
    assert current_negative(monkeypatch, fake_current_record(), classification_proof=proof).outcome == NONCOMPARABLE


def test_stale_q69b_release_fails_integrity(monkeypatch):
    bad = replace(Q69BSourceBinding(), release_hash=h("8"))
    assert current_negative(monkeypatch, fake_current_record(), q69b_binding=bad).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_stale_q69b_coordinate_authority_fails_integrity(monkeypatch):
    bad = replace(Q69BSourceBinding(), coordinate_authority_hash=h("7"))
    assert current_negative(monkeypatch, fake_current_record(), q69b_binding=bad).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_unresolved_d08_grammar_fails_closed_before_predicate(monkeypatch):
    bad = grammar(currentness=CURRENT_ACCEPTED, kind="COORDINATE_SEMANTICS")
    assert current_negative(monkeypatch, fake_current_record(), grammar_binding=bad).outcome == D08_GRAMMAR_UNRESOLVED


def test_missing_d08_operator_semantics_fails_closed(monkeypatch):
    bad = replace(grammar(currentness=CURRENT_ACCEPTED), operator_semantics_refs=())
    assert current_negative(monkeypatch, fake_current_record(), grammar_binding=bad).outcome == D08_GRAMMAR_UNRESOLVED


def test_temporal_lower_edge_unknown_is_noncomparable_without_positive_predicate(monkeypatch):
    w = window(start="2024-06-15T12:00:00Z", lower=None, currentness=CURRENT_ACCEPTED)
    result = current_negative(monkeypatch, fake_current_record(), respondent_windows=(w,))
    assert result.outcome == NONCOMPARABLE and result.predicate is None


def test_temporal_wrong_currentness_fails_source_time_equivalence(monkeypatch):
    result = current_negative(monkeypatch, fake_current_record(), respondent_windows=(window(),))
    assert result.outcome == SOURCE_TIME_GEOGRAPHY_EQUIVALENCE_UNRESOLVED
    assert result.predicate is None


def test_empty_empirical_frontier_is_lawful_valid_empty_synthetic():
    assert synth(respondent_windows=()).outcome == LAWFUL_VALID_EMPTY


def test_outside_all_windows_is_no_exact_match_synthetic():
    w = window(start="2023-01-01T00:00:00Z", end="2023-12-31T23:59:59Z")
    assert synth(respondent_windows=(w,)).outcome == NO_EXACT_MATCH


def test_conflicting_duplicate_respondent_window_is_ambiguous_synthetic():
    a = window("r1", start="2024-01-01T00:00:00Z")
    b = window("r1", start="2024-02-01T00:00:00Z")
    assert synth(respondent_windows=(a, b)).outcome == AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING


def test_synthetic_fixture_replay_hash_drift_fails_closed():
    assert synth(fixture=replace(fixture(), fixture_hash=h("6"))).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_synthetic_receipt_replay_binds_actor_time_and_predicate():
    a = synth(fixture=fixture("2024-06-15T12:00:00Z"))
    b = synth(fixture=fixture("2024-06-16T12:00:00Z"))
    assert a.receipt.deterministic_replay_identity != b.receipt.deterministic_replay_identity
    assert a.receipt.receipt_hash != b.receipt.receipt_hash


def test_synthetic_predicate_hash_binds_exact_respondent_scope():
    a = synth(respondent_windows=(window("r1"),))
    b = synth(respondent_windows=(window("r2"),))
    assert a.synthetic_preview.predicate_hash != b.synthetic_preview.predicate_hash


def test_no_actor_to_q69b_absent_branch():
    dumped = repr(synth().synthetic_preview.predicate_ast)
    assert "ABSENT" not in dumped
    assert "PUBLIC_CLINIC_EXPERIENCE_PRESENT" in dumped


def test_no_similarity_or_structural_position_material_in_positive_preview():
    dumped = repr(synth().synthetic_preview).lower()
    for forbidden in ("fuzzy", "embedding", "nearest", "structural_position", "llm"):
        assert forbidden not in dumped
