from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
import rawlsing_next.gt34_obl031_q69b_comparator_resolver_r3 as target

ACTOR = "urn:hostile:actor"


def h(ch):
    return ch * 64


def exact_window(currentness=target.NONCURRENT_SYNTHETIC_TEST_ONLY):
    return target.RespondentDateIntrWindow(
        respondent_ref=ExactRef("RESPONDENT", "urn:hostile:r1", h("a")),
        dateintr_ref=ExactRef("DATEINTR", "urn:hostile:r1:date", h("b")),
        window_start="2024-01-01T00:00:00Z",
        window_end="2024-12-31T23:59:59Z",
        lower_edge_inclusive=True,
        currentness=currentness,
    )


def fixture():
    return target.SyntheticEncounterFixture.build(ACTOR, "2024-06-15T12:00:00Z")


def fake_actor():
    class Record:
        pass
    return Record()


def current_call(grammar):
    return target.resolve_current(
        actor_record=fake_actor(),
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=grammar,
        respondent_windows=(exact_window(target.CURRENT_ACCEPTED),),
    )


def synthetic_call(grammar):
    return target.prove_noncurrent_synthetic(
        fixture=fixture(),
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=grammar,
        respondent_windows=(exact_window(),),
    )


def mutation_cases():
    g = target.current_d08_grammar_binding()
    first, second = g.operator_semantics_refs
    owner = g.owner_jurisdiction_ref
    return [
        ("authority_id_empty", replace(g, authority_id="")),
        ("authority_id_historical", replace(g, authority_id="D08@db03fcbcb5e34c28b486070628377ead0408e13a")),
        ("authority_id_q69b", replace(g, authority_id="R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY")),
        ("authority_id_fixture", replace(g, authority_id="HOSTILE_FIXTURE_AUTHORITY")),
        ("authority_version_old", replace(g, authority_version="0.9.0")),
        ("authority_version_latest", replace(g, authority_version="latest")),
        ("authority_hash_zero", replace(g, authority_hash=h("0"))),
        ("authority_hash_q69b_shape", replace(g, authority_hash="cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c")),
        ("kind_coordinate", replace(g, authority_kind="COORDINATE_SEMANTICS")),
        ("kind_empty", replace(g, authority_kind="")),
        ("operation_any", replace(g, governed_operation="RESOLVE_ANY_PREDICATE")),
        ("operation_prefix", replace(g, governed_operation="RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE")),
        ("family_coordinate", replace(g, governed_object_family="EmpiricalCoordinateFact@1.0.0")),
        ("family_version", replace(g, governed_object_family="EmpiricalPredicate@2.0.0")),
        ("leaf_structural", replace(g, predicate_leaf_type="STRUCTURAL_POSITION")),
        ("leaf_empty", replace(g, predicate_leaf_type="")),
        ("operator_ne", replace(g, comparison_operator="NE")),
        ("operator_fuzzy", replace(g, comparison_operator="FUZZY_EQ")),
        ("semantics_empty", replace(g, operator_semantics_refs=())),
        ("semantics_one", replace(g, operator_semantics_refs=(first,))),
        ("semantics_reversed", replace(g, operator_semantics_refs=(second, first))),
        ("semantics_duplicate", replace(g, operator_semantics_refs=(first, first))),
        ("semantics_first_hash", replace(g, operator_semantics_refs=(ExactRef(first.kind, first.object_id, h("1")), second))),
        ("semantics_second_hash", replace(g, operator_semantics_refs=(first, ExactRef(second.kind, second.object_id, h("2"))))),
        ("semantics_first_id", replace(g, operator_semantics_refs=(ExactRef(first.kind, "OTHER_POSITION", first.content_hash), second))),
        ("semantics_second_id", replace(g, operator_semantics_refs=(first, ExactRef(second.kind, "OTHER_EQ", second.content_hash)))),
        ("owner_id", replace(g, owner_jurisdiction_ref=ExactRef(owner.kind, "OTHER_OWNER", owner.content_hash))),
        ("owner_hash", replace(g, owner_jurisdiction_ref=ExactRef(owner.kind, owner.object_id, h("3")))),
        ("owner_kind", replace(g, owner_jurisdiction_ref=ExactRef("OTHER_KIND", owner.object_id, owner.content_hash))),
        ("adoption_commit", replace(g, hq_adoption_commit=h("4"))),
        ("adoption_artifact", replace(g, hq_adoption_artifact_blob="0" * 40)),
        ("adoption_json", replace(g, hq_adoption_json_blob="1" * 40)),
        ("selection_receipt", replace(g, hq_current_selection_receipt_blob="2" * 40)),
        ("currentness_stale", replace(g, currentness="STALE")),
        ("currentness_candidate", replace(g, currentness="CANDIDATE_NOT_ADOPTED")),
        ("resolution_latest", replace(g, resolution_contract="LATEST")),
        ("resolution_default", replace(g, resolution_contract="DEFAULT")),
        ("resolution_fuzzy", replace(g, resolution_contract="FUZZY")),
        ("resolution_fallback", replace(g, resolution_contract="FALLBACK")),
        ("provenance_empty", replace(g, provenance_refs=())),
        ("provenance_drop_first", replace(g, provenance_refs=g.provenance_refs[1:])),
        ("provenance_drop_last", replace(g, provenance_refs=g.provenance_refs[:-1])),
        ("provenance_reordered", replace(g, provenance_refs=tuple(reversed(g.provenance_refs)))),
        ("provenance_fixture", replace(g, provenance_refs=("HOSTILE_FIXTURE",))),
    ]


@pytest.mark.parametrize("label,binding", mutation_cases(), ids=[x[0] for x in mutation_cases()])
def test_mutated_or_substituted_grammar_never_reaches_current_comparator(label, binding):
    result = current_call(binding)
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED, label
    assert result.predicate is None and result.receipt is None


@pytest.mark.parametrize("label,binding", mutation_cases(), ids=[x[0] for x in mutation_cases()])
def test_mutated_or_substituted_grammar_never_reaches_synthetic_positive_mechanics(label, binding):
    result = synthetic_call(binding)
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED, label
    assert result.predicate is None and result.synthetic_preview is None and result.receipt is None


def test_real_missing_actor_fact_remains_controlling_negative_even_with_no_grammar():
    result = target.resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=None,
        respondent_windows=(),
    )
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None and result.receipt is None


def test_real_missing_actor_fact_cannot_be_overridden_by_exact_grammar():
    result = target.resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=target.current_d08_grammar_binding(),
        respondent_windows=(),
    )
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED


def test_exact_current_grammar_with_nonmissing_unvalidated_actor_still_fails_actor_gate():
    result = current_call(target.current_d08_grammar_binding())
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_synthetic_positive_path_is_explicitly_noncurrent_and_eq_only():
    result = synthetic_call(target.current_d08_grammar_binding())
    assert result.outcome == target.NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.synthetic_preview.fixture_mode == target.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.currentness == target.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.synthetic_preview.predicate_ast["leaf_type"] == "EMPIRICAL_POSITION_COORDINATE"
    assert result.synthetic_preview.predicate_ast["comparison_operator"] == "EQ"


def test_receipt_closure_contains_exact_hq_selection_evidence_and_no_neighbor_authority_substitution():
    receipt = synthetic_call(target.current_d08_grammar_binding()).receipt
    closure = receipt.d08_hq_selection_closure
    for exact in (
        target.D08_AUTHORITY_ID,
        target.D08_AUTHORITY_VERSION,
        target.D08_AUTHORITY_CONTENT_HASH,
        target.D08_HQ_ADOPTION_COMMIT,
        target.D08_HQ_ADOPTION_ARTIFACT_BLOB,
        target.D08_HQ_ADOPTION_JSON_BLOB,
        target.D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB,
        target.D08_RESOLUTION_CONTRACT,
    ):
        assert exact in closure
    dumped = repr(closure)
    assert "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY" not in dumped
    assert "HOSTILE_FIXTURE_AUTHORITY" not in dumped


def test_string_dict_and_none_are_not_accepted_as_grammar_resolution_shortcuts():
    for bad in (None, "latest", "default", "fuzzy", {}, {"authority_id": target.D08_AUTHORITY_ID}):
        result = current_call(bad)
        assert result.outcome == target.D08_GRAMMAR_UNRESOLVED


class EqualitySpoof:
    """Hostile TOCTOU/type-confusion object: equality lies, attributes substitute Q69B."""
    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    authority_id = "R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY"
    authority_version = "1.0.0"
    authority_hash = "cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c"
    authority_kind = "PREDICATE_GRAMMAR"
    governed_operation = target.D08_GOVERNED_OPERATION
    governed_object_family = target.D08_GOVERNED_OBJECT_FAMILY
    predicate_leaf_type = target.D08_PREDICATE_LEAF_TYPE
    comparison_operator = target.D08_COMPARISON_OPERATOR
    operator_semantics_refs = target.D08_OPERATOR_SEMANTICS_REFS
    owner_jurisdiction_ref = target.current_d08_grammar_binding().owner_jurisdiction_ref
    hq_adoption_commit = target.D08_HQ_ADOPTION_COMMIT
    hq_adoption_artifact_blob = target.D08_HQ_ADOPTION_ARTIFACT_BLOB
    hq_adoption_json_blob = target.D08_HQ_ADOPTION_JSON_BLOB
    hq_current_selection_receipt_blob = target.D08_HQ_CURRENT_SELECTION_RECEIPT_BLOB
    currentness = target.CURRENT_ACCEPTED
    resolution_contract = target.D08_RESOLUTION_CONTRACT
    provenance_refs = target.current_d08_grammar_binding().provenance_refs


def test_equality_spoof_type_confusion_cannot_bypass_exact_binding():
    result = current_call(EqualitySpoof())
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED
    assert result.predicate is None and result.receipt is None


def test_no_latest_default_fuzzy_lookup_surface_exists():
    names = set(dir(target))
    for forbidden in (
        "resolve_latest_grammar",
        "get_latest_grammar",
        "default_grammar",
        "fuzzy_grammar_lookup",
        "fallback_grammar",
    ):
        assert forbidden not in names
