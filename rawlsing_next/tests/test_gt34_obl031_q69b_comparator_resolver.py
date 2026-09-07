from dataclasses import replace

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.gt34_obl031_q69b_comparator_resolver import (
    ACTOR_FACT_MISSING_OR_UNAUTHORIZED,
    AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING,
    AUTHORITY_CONTENT_HASH,
    AUTHORITY_ID,
    AUTHORITY_VERSION,
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
    SyntheticEncounterFixture,
    D08GrammarBinding,
    authority_identity,
    current_obl048_proof,
    prove_noncurrent_synthetic,
    resolve_current,
)


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
    return SyntheticEncounterFixture.build("urn:test:actor:first-canary", time)


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


def test_authority_identity_is_content_addressed_and_one_field():
    assert authority_identity() == (AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH)
    assert len(AUTHORITY_CONTENT_HASH) == 64


def test_real_current_invocation_is_typed_missing_without_actor_fact():
    result = resolve_current(
        actor_record=None,
        expected_actor_id="urn:test:actor:first-canary",
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=None,
        respondent_windows=(),
    )
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None
    assert result.receipt is None


def test_synthetic_positive_proof_resolves_only_noncurrent_preview_and_receipt():
    result = synth()
    assert result.outcome == NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.synthetic_preview is not None
    assert result.synthetic_preview.fixture_mode == NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.synthetic_preview.predicate_ast["canonical_value"] == "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
    assert result.receipt is not None
    assert result.receipt.currentness == NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.obl048_authority_hash == OBL048_AUTHORITY_HASH
    assert result.receipt.obl048_proposition_hash == OBL048_PROPOSITION_HASH
    assert result.receipt.source_release_scope[-1] == Q69B_ACCEPTED_RELEASE_HASH


def test_synthetic_fixture_is_mechanically_rejected_by_current_resolver():
    result = resolve_current(
        actor_record=fixture(),  # deliberately wrong type for the current API
        expected_actor_id="urn:test:actor:first-canary",
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(currentness=CURRENT_ACCEPTED),
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE
    assert result.predicate is None


def test_synthetic_preview_is_not_a_pre553_empirical_predicate():
    result = synth()
    from rawlsing_next.pre553_empirical_objects import EmpiricalPredicate
    assert not isinstance(result.synthetic_preview, EmpiricalPredicate)
    assert result.predicate is None


def test_fixture_hash_drift_fails_closed():
    bad = replace(fixture(), fixture_hash=h("f"))
    assert synth(fixture=bad).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_wrong_adp010_owner_fails_closed():
    f = fixture()
    bad = replace(f, authority_id="NOT_ADP010")
    assert synth(fixture=bad).outcome != NONCURRENT_SYNTHETIC_PROOF


def test_wrong_state_fails_closed():
    bad = replace(fixture(), realization_state="OPPORTUNITY")
    assert synth(fixture=bad).outcome != NONCURRENT_SYNTHETIC_PROOF


def test_wrong_effect_fails_closed():
    bad = replace(fixture(), event_effect_kind="NOT_ENCOUNTER")
    assert synth(fixture=bad).outcome != NONCURRENT_SYNTHETIC_PROOF


def test_wrong_subject_fails_closed():
    bad = replace(fixture(), subject_ref="urn:test:wrong-subject")
    assert synth(fixture=bad).outcome != NONCURRENT_SYNTHETIC_PROOF


def test_wrong_obl048_subject_fails_noncomparable():
    proof = replace(current_obl048_proof(), subject_ref="urn:test:wrong-subject")
    assert synth(classification_proof=proof).outcome == NONCOMPARABLE


def test_wrong_obl048_authority_hash_fails_noncomparable():
    proof = replace(current_obl048_proof(), authority_hash=h("9"))
    assert synth(classification_proof=proof).outcome == NONCOMPARABLE


def test_wrong_obl048_proposition_hash_fails_noncomparable():
    proof = replace(current_obl048_proof(), proposition_hash=h("8"))
    assert synth(classification_proof=proof).outcome == NONCOMPARABLE


def test_stale_mutated_q69b_release_fails_integrity():
    bad = replace(Q69BSourceBinding(), release_hash=h("7"))
    assert synth(q69b_binding=bad).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_stale_mutated_q69b_coordinate_authority_fails_integrity():
    bad = replace(Q69BSourceBinding(), coordinate_authority_hash=h("6"))
    assert synth(q69b_binding=bad).outcome == INTEGRITY_REF_HASH_REPLAY_FAILURE


def test_unresolved_d08_grammar_missing_operator_fails_closed():
    bad = replace(grammar(), operator_semantics_refs=())
    assert synth(grammar_binding=bad).outcome == D08_GRAMMAR_UNRESOLVED


def test_wrong_d08_authority_kind_fails_closed():
    assert synth(grammar_binding=grammar(kind="COORDINATE_SEMANTICS")).outcome == D08_GRAMMAR_UNRESOLVED


def test_wrong_d08_operation_fails_closed():
    assert synth(grammar_binding=grammar(op="FUZZY_EQ")).outcome == D08_GRAMMAR_UNRESOLVED


def test_synthetic_grammar_cannot_be_passed_as_current_grammar():
    result = resolve_current(
        actor_record=None,
        expected_actor_id="urn:test:actor:first-canary",
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=grammar(),
        respondent_windows=(window(),),
    )
    # Missing current actor fact is prior and remains typed distinctly; no predicate can leak.
    assert result.outcome == ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_dateintr_lower_edge_unknown_is_noncomparable():
    w = window(start="2024-06-15T12:00:00Z", lower=None)
    assert synth(respondent_windows=(w,)).outcome == NONCOMPARABLE


def test_dateintr_outside_all_windows_is_no_exact_match():
    w = window(start="2023-01-01T00:00:00Z", end="2023-12-31T23:59:59Z")
    assert synth(respondent_windows=(w,)).outcome == NO_EXACT_MATCH


def test_empty_empirical_frontier_is_lawful_valid_empty():
    assert synth(respondent_windows=()).outcome == LAWFUL_VALID_EMPTY


def test_conflicting_duplicate_respondent_window_is_ambiguous():
    a = window("r1", start="2024-01-01T00:00:00Z")
    b = window("r1", start="2024-02-01T00:00:00Z")
    assert synth(respondent_windows=(a, b)).outcome == AMBIGUOUS_CARDINALITY_CONFLICTING_MAPPING


def test_wrong_window_currentness_fails_closed():
    w = window(currentness=CURRENT_ACCEPTED)
    assert synth(respondent_windows=(w,)).outcome != NONCURRENT_SYNTHETIC_PROOF


def test_receipt_replay_identity_binds_actor_time_and_predicate():
    a = synth(fixture=fixture("2024-06-15T12:00:00Z"))
    b = synth(fixture=fixture("2024-06-16T12:00:00Z"))
    assert a.receipt.deterministic_replay_identity != b.receipt.deterministic_replay_identity
    assert a.receipt.receipt_hash != b.receipt.receipt_hash


def test_predicate_hash_changes_with_exact_respondent_scope():
    a = synth(respondent_windows=(window("r1"),))
    b = synth(respondent_windows=(window("r2"),))
    assert a.synthetic_preview.predicate_hash != b.synthetic_preview.predicate_hash


def test_no_absent_branch_is_generated():
    result = synth()
    dumped = repr(result.synthetic_preview.predicate_ast)
    assert "ABSENT" not in dumped
    assert "PUBLIC_CLINIC_EXPERIENCE_PRESENT" in dumped


def test_no_forbidden_similarity_or_structural_position_material_in_preview():
    result = synth()
    dumped = repr(result.synthetic_preview).lower()
    for forbidden in ("fuzzy", "embedding", "nearest", "structural_position", "llm"):
        assert forbidden not in dumped
