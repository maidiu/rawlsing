from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
import rawlsing_next.gt34_obl031_q69b_comparator_resolver_r4 as target

ACTOR = "urn:r4:hostile:actor"


def h(ch):
    return ch * 64


def exact_window(currentness=target.NONCURRENT_SYNTHETIC_TEST_ONLY):
    return target.RespondentDateIntrWindow(
        respondent_ref=ExactRef("RESPONDENT", "urn:r4:hostile:r1", h("a")),
        dateintr_ref=ExactRef("DATEINTR", "urn:r4:hostile:r1:date", h("b")),
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
        ("id_empty", replace(g, authority_id="")),
        ("id_historical", replace(g, authority_id="D08@db03fcbcb5e34c28b486070628377ead0408e13a")),
        ("id_q69b", replace(g, authority_id="R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY")),
        ("id_fixture", replace(g, authority_id="HOSTILE_FIXTURE_AUTHORITY")),
        ("version_old", replace(g, authority_version="0.9.0")),
        ("version_latest", replace(g, authority_version="latest")),
        ("hash_zero", replace(g, authority_hash=h("0"))),
        ("hash_q69b", replace(g, authority_hash="cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c")),
        ("kind_coordinate", replace(g, authority_kind="COORDINATE_SEMANTICS")),
        ("kind_comparator", replace(g, authority_kind="COMPARATOR")),
        ("operation_any", replace(g, governed_operation="RESOLVE_ANY_PREDICATE")),
        ("operation_prefix", replace(g, governed_operation="RESOLVE_EXACT_EMPIRICAL_POSITION_COORDINATE")),
        ("family_coordinate", replace(g, governed_object_family="EmpiricalCoordinateFact@1.0.0")),
        ("family_v2", replace(g, governed_object_family="EmpiricalPredicate@2.0.0")),
        ("leaf_structural", replace(g, predicate_leaf_type="STRUCTURAL_POSITION")),
        ("leaf_response", replace(g, predicate_leaf_type="RESPONSE_EVENT")),
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
def test_current_rejects_every_exact_tuple_or_selection_mutation(label, binding):
    result = current_call(binding)
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED, label
    assert result.predicate is None and result.receipt is None


@pytest.mark.parametrize("label,binding", mutation_cases(), ids=[x[0] for x in mutation_cases()])
def test_synthetic_rejects_every_exact_tuple_or_selection_mutation(label, binding):
    result = synthetic_call(binding)
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED, label
    assert result.predicate is None and result.synthetic_preview is None and result.receipt is None


class EqualitySpoof:
    def __eq__(self, other):
        return True
    def __ne__(self, other):
        return False
    authority_id = target.D08_AUTHORITY_ID
    authority_version = target.D08_AUTHORITY_VERSION
    authority_hash = target.D08_AUTHORITY_CONTENT_HASH
    authority_kind = target.D08_AUTHORITY_KIND
    governed_operation = target.D08_GOVERNED_OPERATION
    governed_object_family = target.D08_GOVERNED_OBJECT_FAMILY
    predicate_leaf_type = target.D08_PREDICATE_LEAF_TYPE
    comparison_operator = target.D08_COMPARISON_OPERATOR
    operator_semantics_refs = target.D08_OPERATOR_SEMANTICS_REFS


def test_equality_spoof_defect_from_r3_is_closed():
    result = current_call(EqualitySpoof())
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED
    assert result.predicate is None and result.receipt is None


def test_equality_spoof_cannot_enter_synthetic_mechanics_either():
    result = synthetic_call(EqualitySpoof())
    assert result.outcome == target.D08_GRAMMAR_UNRESOLVED
    assert result.synthetic_preview is None and result.receipt is None


def test_subclass_with_exact_fields_is_rejected_by_exact_type_gate():
    class Subclass(target.D08GrammarBinding):
        pass
    g = target.current_d08_grammar_binding()
    sub = Subclass(**{name: getattr(g, name) for name in g.__dataclass_fields__})
    assert current_call(sub).outcome == target.D08_GRAMMAR_UNRESOLVED
    assert synthetic_call(sub).outcome == target.D08_GRAMMAR_UNRESOLVED


def test_string_dict_none_and_latest_shortcuts_are_rejected():
    for bad in (None, "latest", "default", "fuzzy", "fallback", {}, {"authority_id": target.D08_AUTHORITY_ID}):
        assert current_call(bad).outcome == target.D08_GRAMMAR_UNRESOLVED
        assert synthetic_call(bad).outcome == target.D08_GRAMMAR_UNRESOLVED


def test_real_missing_actor_encounter_remains_controlling_negative():
    result = target.resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=target.current_d08_grammar_binding(),
        respondent_windows=(),
    )
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None and result.receipt is None


def test_missing_actor_cannot_be_manufactured_by_malicious_grammar_object():
    result = target.resolve_current(
        actor_record=None,
        expected_actor_id=ACTOR,
        classification_proof=target.current_obl048_proof(),
        q69b_binding=target.Q69BSourceBinding(),
        grammar_binding=EqualitySpoof(),
        respondent_windows=(),
    )
    assert result.outcome == target.ACTOR_FACT_MISSING_OR_UNAUTHORIZED
    assert result.predicate is None


def test_exact_binding_positive_mechanics_remain_noncurrent_preview_only():
    result = synthetic_call(target.current_d08_grammar_binding())
    assert result.outcome == target.NONCURRENT_SYNTHETIC_PROOF
    assert result.predicate is None
    assert result.synthetic_preview.fixture_mode == target.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.receipt.currentness == target.NONCURRENT_SYNTHETIC_TEST_ONLY
    assert result.synthetic_preview.predicate_ast["leaf_type"] == "EMPIRICAL_POSITION_COORDINATE"
    assert result.synthetic_preview.predicate_ast["comparison_operator"] == "EQ"
    assert result.synthetic_preview.predicate_ast["canonical_value"] == "PUBLIC_CLINIC_EXPERIENCE_PRESENT"


def test_r4_receipt_is_resealed_and_retains_exact_hq_selection_closure():
    receipt = synthetic_call(target.current_d08_grammar_binding()).receipt
    assert receipt.comparator_rule_identity == target.authority_identity()
    assert receipt.authority_version == "1.1.3"
    assert receipt.authority_content_hash == target.authority_identity()[2]
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
        assert exact in receipt.d08_hq_selection_closure


def test_no_latest_default_fuzzy_lookup_surface_exists():
    names = set(dir(target))
    for forbidden in (
        "resolve_latest_grammar", "get_latest_grammar", "default_grammar",
        "fuzzy_grammar_lookup", "fallback_grammar",
    ):
        assert forbidden not in names


def test_owner_split_not_collapsed_in_successful_synthetic_receipt_or_preview():
    result = synthetic_call(target.current_d08_grammar_binding())
    dumped = (repr(result.receipt) + repr(result.synthetic_preview)).lower()
    assert "public_clinic_experience_present" in dumped
    for forbidden in (
        "actor_is_public_clinic", "q69b_is_actor", "obl057_is_q69b",
        "psepf", "v3_mutation", "positive_obl056_entry",
    ):
        assert forbidden not in dumped
