from dataclasses import replace

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.gt34_obl031_q69b_comparator_resolver_r3 import (
    ACTOR_FACT_MISSING_OR_UNAUTHORIZED,
    AUTHORITY_CONTENT_HASH,
    CURRENT_ACCEPTED,
    D08_AUTHORITY_CONTENT_HASH,
    D08_AUTHORITY_ID,
    D08_AUTHORITY_VERSION,
    D08_COMPARISON_OPERATOR,
    D08_CURRENT_SELECTION_STATUS,
    D08_GOVERNED_OBJECT_FAMILY,
    D08_GOVERNED_OPERATION,
    D08_GRAMMAR_UNRESOLVED,
    D08_HQ_ADOPTION_ARTIFACT_BLOB,
    D08_HQ_ADOPTION_COMMIT,
    D08_HQ_ADOPTION_JSON_BLOB,
    D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
    D08_OPERATOR_SEMANTICS_REFS,
    D08_PREDICATE_LEAF_TYPE,
    D08_RESOLUTION_CONTRACT,
    NONCURRENT_SYNTHETIC_PROOF,
    NONCURRENT_SYNTHETIC_TEST_ONLY,
    Q69BSourceBinding,
    RespondentDateIntrWindow,
    SyntheticEncounterFixture,
    authority_identity,
    current_d08_grammar_binding,
    current_obl048_proof,
    prove_noncurrent_synthetic,
    resolve_current,
)

ACTOR = "urn:test:actor:first-canary"


def h(ch):
    return ch * 64


def ref(kind, tag, ch="a"):
    return ExactRef(kind, f"urn:test:{tag}", h(ch))


def window(tag="r1", *, currentness=NONCURRENT_SYNTHETIC_TEST_ONLY):
    return RespondentDateIntrWindow(
        respondent_ref=ref("RESPONDENT", tag, "d"),
        dateintr_ref=ref("DATEINTR", tag, "e"),
        window_start="2024-01-01T00:00:00Z",
        window_end="2024-12-31T23:59:59Z",
        lower_edge_inclusive=True,
        currentness=currentness,
    )


def fixture():
    return SyntheticEncounterFixture.build(ACTOR, "2024-06-15T12:00:00Z")


def synth(grammar=None):
    return prove_noncurrent_synthetic(
        fixture=fixture(),
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=current_d08_grammar_binding() if grammar is None else grammar,
        respondent_windows=(window(),),
    )


def fake_actor():
    class Record:
        pass
    return Record()


def assert_grammar_rejected(binding):
    result = resolve_current(
        actor_record=fake_actor(),
        expected_actor_id=ACTOR,
        classification_proof=current_obl048_proof(),
        q69b_binding=Q69BSourceBinding(),
        grammar_binding=binding,
        respondent_windows=(window(currentness=CURRENT_ACCEPTED),),
    )
    assert result.outcome == D08_GRAMMAR_UNRESOLVED
    assert result.predicate is None and result.receipt is None


def test_r3_authority_identity_is_content_addressed_successor():
    assert authority_identity()[2] == AUTHORITY_CONTENT_HASH
    assert len(AUTHORITY_CONTENT_HASH) == 64
    assert authority_identity()[1] == "1.1.2"


def test_exact_current_d08_tuple_is_pinned():
    g = current_d08_grammar_binding()
    assert (g.authority_id, g.authority_version, g.authority_hash) == (
        D08_AUTHORITY_ID, D08_AUTHORITY_VERSION, D08_AUTHORITY_CONTENT_HASH
    )
    assert g.currentness == D08_CURRENT_SELECTION_STATUS == CURRENT_ACCEPTED


def test_exact_kind_family_operation_leaf_and_eq_are_pinned():
    g = current_d08_grammar_binding()
    assert g.authority_kind == "PREDICATE_GRAMMAR"
    assert g.governed_object_family == D08_GOVERNED_OBJECT_FAMILY == "EmpiricalPredicate@1.0.0"
    assert g.governed_operation == D08_GOVERNED_OPERATION
    assert g.predicate_leaf_type == D08_PREDICATE_LEAF_TYPE == "EMPIRICAL_POSITION_COORDINATE"
    assert g.comparison_operator == D08_COMPARISON_OPERATOR == "EQ"


def test_exact_hq_selection_evidence_is_pinned():
    g = current_d08_grammar_binding()
    assert g.hq_adoption_commit == D08_HQ_ADOPTION_COMMIT
    assert g.hq_adoption_artifact_blob == D08_HQ_ADOPTION_ARTIFACT_BLOB
    assert g.hq_adoption_json_blob == D08_HQ_ADOPTION_JSON_BLOB
    assert g.hq_current_selection_receipt_blob == D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB
    assert g.resolution_contract == D08_RESOLUTION_CONTRACT


def test_exact_two_operator_semantics_refs_are_pinned():
    assert current_d08_grammar_binding().operator_semantics_refs == D08_OPERATOR_SEMANTICS_REFS
    assert len(D08_OPERATOR_SEMANTICS_REFS) == 2


def test_real_current_first_canary_missing_actor_fact_still_fails_closed_first():
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


def test_noncurrent_synthetic_mechanics_still_produce_only_preview_and_receipt():
    result = synth()
    assert result.outcome == NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.synthetic_preview is not None
    assert result.synthetic_preview.fixture_mode == NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.currentness == NONCURRENT_SYNTHETIC_TEST_ONLY


def test_synthetic_receipt_resealed_under_r3_and_binds_hq_selection_closure():
    result = synth()
    receipt = result.receipt
    assert receipt.authority_version == "1.1.2"
    assert receipt.authority_content_hash == AUTHORITY_CONTENT_HASH
    assert receipt.comparator_rule_identity == authority_identity()
    assert D08_HQ_ADOPTION_COMMIT in receipt.d08_hq_selection_closure
    assert D08_HQ_ADOPTION_ARTIFACT_BLOB in receipt.d08_hq_selection_closure
    assert D08_HQ_ADOPTION_JSON_BLOB in receipt.d08_hq_selection_closure
    assert D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB in receipt.d08_hq_selection_closure
    assert receipt.predecessor_r2_receipt_hash


def test_mutated_authority_hash_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), authority_hash=h("0")))


def test_wrong_authority_id_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), authority_id="WRONG_D08"))


def test_wrong_authority_version_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), authority_version="9.9.9"))


def test_historical_d08_substitution_rejected():
    assert_grammar_rejected(replace(
        current_d08_grammar_binding(),
        authority_id="HISTORICAL_D08_AT_db03fcbcb5e34c28b486070628377ead0408e13a",
    ))


def test_q69b_authority_substitution_rejected():
    assert_grammar_rejected(replace(
        current_d08_grammar_binding(),
        authority_id="R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY",
    ))


def test_hostile_fixture_authority_substitution_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), authority_id="HOSTILE_FIXTURE_D08_GRAMMAR"))


def test_authority_kind_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), authority_kind="COORDINATE_SEMANTICS"))


def test_object_family_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), governed_object_family="EmpiricalCoordinateFact@1.0.0"))


def test_governed_operation_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), governed_operation="RESOLVE_ANY_PREDICATE"))


def test_predicate_leaf_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), predicate_leaf_type="STRUCTURAL_POSITION"))


def test_non_eq_operator_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), comparison_operator="NE"))


def test_operator_semantics_order_or_membership_drift_rejected():
    g = current_d08_grammar_binding()
    assert_grammar_rejected(replace(g, operator_semantics_refs=tuple(reversed(g.operator_semantics_refs))))
    assert_grammar_rejected(replace(g, operator_semantics_refs=g.operator_semantics_refs[:1]))


def test_operator_semantics_hash_drift_rejected():
    g = current_d08_grammar_binding()
    bad = ExactRef(g.operator_semantics_refs[0].kind, g.operator_semantics_refs[0].object_id, h("1"))
    assert_grammar_rejected(replace(g, operator_semantics_refs=(bad, g.operator_semantics_refs[1])))


def test_owner_jurisdiction_drift_rejected():
    g = current_d08_grammar_binding()
    bad = ExactRef(g.owner_jurisdiction_ref.kind, "OTHER_OWNER", g.owner_jurisdiction_ref.content_hash)
    assert_grammar_rejected(replace(g, owner_jurisdiction_ref=bad))


def test_hq_adoption_commit_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), hq_adoption_commit=h("2")))


def test_hq_adoption_artifact_blob_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), hq_adoption_artifact_blob=h("3")[:40]))


def test_hq_adoption_json_blob_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), hq_adoption_json_blob=h("4")[:40]))


def test_current_selection_receipt_blob_drift_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), hq_current_selection_receipt_blob=h("5")[:40]))


def test_stale_currentness_rejected():
    assert_grammar_rejected(replace(current_d08_grammar_binding(), currentness="STALE"))


def test_missing_or_mutated_provenance_rejected():
    g = current_d08_grammar_binding()
    assert_grammar_rejected(replace(g, provenance_refs=()))
    assert_grammar_rejected(replace(g, provenance_refs=g.provenance_refs[:-1]))


def test_latest_default_fuzzy_resolution_contract_rejected():
    for bad in ("LATEST", "DEFAULT", "FUZZY", "FALLBACK"):
        assert_grammar_rejected(replace(current_d08_grammar_binding(), resolution_contract=bad))


def test_missing_grammar_binding_rejected_for_nonmissing_actor_input():
    assert_grammar_rejected(None)


def test_noncurrent_synthetic_cannot_smuggle_mutated_grammar():
    bad = replace(current_d08_grammar_binding(), authority_hash=h("6"))
    result = synth(bad)
    assert result.outcome == D08_GRAMMAR_UNRESOLVED
    assert result.synthetic_preview is None and result.receipt is None


def test_synthetic_output_is_exact_eq_present_not_absent_or_fuzzy():
    result = synth()
    ast = result.synthetic_preview.predicate_ast
    assert ast["leaf_type"] == "EMPIRICAL_POSITION_COORDINATE"
    assert ast["comparison_operator"] == "EQ"
    assert ast["canonical_value"] == "PUBLIC_CLINIC_EXPERIENCE_PRESENT"
    dumped = repr(ast).lower()
    for forbidden in ("absent", "fuzzy", "latest", "default", "embedding", "structural_position"):
        assert forbidden not in dumped
